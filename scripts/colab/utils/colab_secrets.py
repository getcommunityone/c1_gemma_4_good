"""
Resolve notebook API keys without hard-failing on Colab ``userdata`` timeouts.

Order: ``.env`` (repo root) → ``os.environ`` → Colab Secrets (optional).

Set ``GOVERNANCE_NOTEBOOK_SECRETS=env_only`` to skip Colab Secrets entirely
(local Jupyter, Cursor, or flaky Colab secret UI).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]


def in_colab_runtime() -> bool:
    """
    True only on **Google Colab cloud** (``colab.research.google.com``).

    The VS Code / Cursor **Colab extension** installs ``google.colab`` locally but
    ``userdata.get`` times out — that is **not** Colab cloud. Use ``.env`` locally.
    """
    if os.environ.get("GOVERNANCE_FORCE_COLAB_SECRETS", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        return True
    return bool(os.environ.get("COLAB_RELEASE_TAG")) and Path("/content").is_dir()


def notebook_runs_locally() -> bool:
    """True for local Jupyter / Cursor / Colab extension (keys from ``.env``)."""
    return not in_colab_runtime()


def default_local_secrets_mode() -> None:
    """Skip Colab ``userdata`` on local Jupyter / Cursor / Colab extension, not on Colab cloud."""
    if notebook_runs_locally():
        os.environ.setdefault("GOVERNANCE_NOTEBOOK_SECRETS", "env_only")
        return
    if (os.environ.get("GEMINI_API_KEY") or "").strip():
        os.environ.setdefault("GOVERNANCE_NOTEBOOK_SECRETS", "env_only")


def load_api_keys_to_environ(
    *,
    repo: Optional[PathLike] = None,
    pipeline_root: Optional[PathLike] = None,
    extra_dotenv_paths: Optional[tuple[PathLike, ...]] = None,
) -> bool:
    """
    Load ``GEMINI_API_KEY`` / ``HF_TOKEN`` from ``.env`` files. Returns True if GEMINI is set.

    Never calls Colab Secrets (use :func:`get_notebook_secret` only when you need Secrets).
    """
    default_local_secrets_mode()
    load_dotenv_all_candidates(repo=repo, pipeline_root=pipeline_root)
    if extra_dotenv_paths:
        for p in extra_dotenv_paths:
            load_dotenv_file(p)
    explicit = (os.environ.get("GOVERNANCE_DOTENV_PATH") or "").strip()
    if explicit:
        load_dotenv_file(explicit)
    return bool((os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip())


def prefer_env_over_colab_secrets() -> None:
    """Force ``.env`` / paste only — no ``userdata`` (avoids Cursor/Colab extension timeouts)."""
    os.environ["GOVERNANCE_NOTEBOOK_SECRETS"] = "env_only"


def bootstrap_api_keys(
    *,
    repo: Optional[PathLike] = None,
    pipeline_root: Optional[PathLike] = None,
    extra_dotenv_paths: Optional[tuple[PathLike, ...]] = None,
) -> bool:
    """§0 helper: same as :func:`load_api_keys_to_environ` after :func:`prefer_env_over_colab_secrets`."""
    prefer_env_over_colab_secrets()
    return load_api_keys_to_environ(
        repo=repo,
        pipeline_root=pipeline_root,
        extra_dotenv_paths=extra_dotenv_paths,
    )


def load_dotenv_file(dotenv_path: PathLike, *, override: bool = False) -> bool:
    """Load a ``.env`` file into ``os.environ`` (stdlib only — no ``python-dotenv`` required)."""
    path = Path(dotenv_path).expanduser()
    if not path.is_file():
        return False
    loaded = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if override or key not in os.environ or not str(os.environ.get(key, "")).strip():
            os.environ[key] = value
            loaded += 1
    return loaded > 0


def load_repo_dotenv(repo: Optional[PathLike] = None) -> bool:
    """Load ``<repo>/.env`` if present. Returns True when a file was loaded."""
    root = _resolve_repo(repo)
    dotenv_path = root / ".env"
    if not dotenv_path.is_file():
        return False
    try:
        from dotenv import load_dotenv

        load_dotenv(dotenv_path, override=False)
        return True
    except ImportError:
        return load_dotenv_file(dotenv_path, override=False)


def load_dotenv_from_parents(start: Optional[PathLike] = None) -> Optional[Path]:
    """Walk parents from ``start`` (default ``cwd``) and load the first ``.env`` found."""
    anchor = Path(start or Path.cwd()).resolve()
    for folder in (anchor, *anchor.parents):
        if load_dotenv_file(folder / ".env"):
            marker = folder / "scripts" / "colab" / "utils" / "colab_paths.py"
            if marker.is_file():
                os.environ.setdefault("OPEN_NAVIGATOR_ROOT", str(folder.resolve()))
            return folder
    return None


def load_first_project_dotenv() -> Optional[Path]:
    """Load the nearest ``.env`` and set ``OPEN_NAVIGATOR_ROOT`` when the repo marker exists."""
    return load_dotenv_from_parents(Path.cwd())


def load_dotenv_all_candidates(
    *,
    repo: Optional[PathLike] = None,
    pipeline_root: Optional[PathLike] = None,
) -> Optional[Path]:
    """
    Load the first ``.env`` found across repo, pipeline data root, Drive, and ``cwd`` parents.

    Returns the directory that contained the loaded file (if any).
    """
    default_local_secrets_mode()
    seen: set[Path] = set()
    loaded_from: Optional[Path] = None

    def _try(dotenv: Path) -> bool:
        parent = dotenv.parent.resolve()
        if parent in seen:
            return False
        seen.add(parent)
        if not load_dotenv_file(dotenv):
            return False
        nonlocal loaded_from
        if loaded_from is None:
            loaded_from = parent
        marker = parent / "scripts" / "colab" / "utils" / "colab_paths.py"
        if marker.is_file():
            os.environ.setdefault("OPEN_NAVIGATOR_ROOT", str(parent))
        return True

    for start in (Path.cwd(), *Path.cwd().parents):
        _try(start / ".env")

    if repo is not None:
        _try(Path(repo).expanduser() / ".env")

    for raw in (
        os.environ.get("GOVERNANCE_PIPELINE_DATA_ROOT", "").strip(),
        str(pipeline_root) if pipeline_root else "",
    ):
        if not raw:
            continue
        root = Path(raw).expanduser()
        _try(root / ".env")
        _try(root.parent / ".env")

    if in_colab_runtime():
        for guess in (
            Path("/content/c1_gemma_4_good"),
            Path("/content/governance_pipeline_local"),
            Path("/content/drive/MyDrive/CommunityOne/hackathons/2026_Gemma_4_Good"),
            Path("/content/drive/MyDrive/CommunityOne"),
            Path("/content/drive/MyDrive"),
        ):
            _try(guess / ".env")

    return loaded_from


def _resolve_repo(repo: Optional[PathLike]) -> Path:
    if repo is not None:
        return Path(repo).expanduser().resolve()
    for key in ("OPEN_NAVIGATOR_ROOT", "REPO_PATH"):
        raw = os.environ.get(key, "").strip()
        if raw:
            return Path(raw).expanduser().resolve()
    return Path.cwd().resolve()


def _secrets_from_env_only() -> bool:
    raw = os.environ.get("GOVERNANCE_NOTEBOOK_SECRETS", "").strip().lower()
    return raw in ("env", "env_only", "dotenv", "local", "environment")


def _skip_colab_userdata() -> bool:
    return os.environ.get("GOVERNANCE_SKIP_COLAB_SECRETS", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def get_notebook_secret(name: str, *, repo: Optional[PathLike] = None) -> Optional[str]:
    """
    Return a secret value or ``None``.

    Order: ``.env`` / ``os.environ`` first, then Colab Secrets only when allowed.
    Never prints on ``TimeoutException`` when ``GOVERNANCE_NOTEBOOK_SECRETS=env_only``.
    """
    default_local_secrets_mode()
    load_dotenv_all_candidates(repo=repo)

    env_val = (os.environ.get(name) or "").strip()
    if env_val:
        return env_val

    if _secrets_from_env_only() or _skip_colab_userdata() or not in_colab_runtime():
        return None

    try:
        from google.colab import userdata

        val = (userdata.get(name) or "").strip()
        return val or None
    except Exception:
        return None


def sanitize_api_key(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    cleaned = (
        value.strip().replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "")
    )
    if cleaned != value.strip():
        print("   ⚠ API key whitespace stripped — re-copy the key to silence this.")
    return cleaned or None
