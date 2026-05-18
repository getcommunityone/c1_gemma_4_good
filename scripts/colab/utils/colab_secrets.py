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
    """True when executing on Google Colab (not just when ``google.colab`` imports)."""
    if os.environ.get("COLAB_RELEASE_TAG"):
        return True
    try:
        import google.colab  # noqa: F401

        return True
    except ImportError:
        return False


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
        return False


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
