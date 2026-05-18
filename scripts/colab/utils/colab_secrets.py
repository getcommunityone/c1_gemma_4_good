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
    """On local runs, skip Colab ``userdata`` unless the user opted into cloud secrets."""
    if notebook_runs_locally():
        os.environ.setdefault("GOVERNANCE_NOTEBOOK_SECRETS", "env_only")


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

    Never raises on Colab ``TimeoutException`` — falls back to env / ``.env``.
    """
    default_local_secrets_mode()
    load_repo_dotenv(repo)
    env_val = (os.environ.get(name) or "").strip()
    if env_val:
        return env_val
    if _secrets_from_env_only() or not in_colab_runtime() or _skip_colab_userdata():
        return None
    try:
        from google.colab import userdata

        val = userdata.get(name)
        return (val or "").strip() or None
    except Exception as exc:
        print(
            f"   ⚠ Colab secret {name!r} unavailable ({type(exc).__name__}: {exc}). "
            f"Use repo .env, os.environ, or Colab 🔑 Secrets."
        )
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
