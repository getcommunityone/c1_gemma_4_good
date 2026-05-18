"""
§6 notebook bootstrap — path + API globals when §4 failed or runtime was restarted.

Call ``prepare_section6_phase1()`` at the start of the §6 Phase 1 cell (after §1–§5).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _user_ns(namespace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if namespace is not None:
        return namespace
    try:
        from IPython import get_ipython

        ip = get_ipython()
        if ip is not None:
            return ip.user_ns
    except Exception:
        pass
    return globals()


def _ensure_import_paths(repo: Path) -> None:
    for entry in (
        str(repo),
        str(repo / "scripts" / "colab"),
        str(repo / "scripts" / "colab" / "utils"),
        str(repo / "scripts" / "colab" / "runtime"),
    ):
        if entry not in sys.path:
            sys.path.insert(0, entry)


def _repo_from_ns(ns: Dict[str, Any]) -> Optional[Path]:
    marker = Path("scripts/colab/utils/colab_paths.py")
    for folder in (Path.cwd(), *Path.cwd().parents):
        if (folder / marker).is_file():
            return folder.resolve()
    env = os.environ.get("OPEN_NAVIGATOR_ROOT", "").strip()
    if env and (Path(env).expanduser() / marker).is_file():
        return Path(env).expanduser().resolve()
    if ns.get("PATHS") is not None:
        return Path(ns["PATHS"].project_path).resolve()
    if ns.get("REPO_PATH") is not None:
        return Path(ns["REPO_PATH"]).resolve()
    for folder in (Path("/content/c1_gemma_4_good"),):
        if (folder / marker).is_file():
            return folder.resolve()
    return None


def load_api_keys_into_ns(ns: Dict[str, Any], repo: Optional[Path] = None) -> bool:
    """Load GEMINI + optional HF from .env / os.environ / Colab Secrets into ``ns``."""
    try:
        from colab_secrets import (
            default_local_secrets_mode,
            get_notebook_secret,
            load_repo_dotenv,
            sanitize_api_key,
        )
    except ImportError:
        from utils.colab_secrets import (  # type: ignore
            default_local_secrets_mode,
            get_notebook_secret,
            load_repo_dotenv,
            sanitize_api_key,
        )

    default_local_secrets_mode()
    try:
        from colab_secrets import load_dotenv_from_parents
    except ImportError:
        from utils.colab_secrets import load_dotenv_from_parents  # type: ignore

    load_dotenv_from_parents(Path.cwd())
    load_repo_dotenv(repo)
    env_root = os.environ.get("OPEN_NAVIGATOR_ROOT", "").strip()
    if env_root:
        load_repo_dotenv(env_root)
    gemini = sanitize_api_key(
        get_notebook_secret("GEMINI_API_KEY", repo=repo)
        or get_notebook_secret("GOOGLE_API_KEY", repo=repo)
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
    )
    if not gemini:
        return False

    ns["API_KEY"] = gemini
    ns["GEMINI_API_KEY"] = gemini
    os.environ["GEMINI_API_KEY"] = gemini

    hf = sanitize_api_key(
        get_notebook_secret("HF_TOKEN", repo=repo) or os.environ.get("HF_TOKEN")
    )
    if hf:
        ns["HF_TOKEN"] = hf
        os.environ["HF_TOKEN"] = hf

    ns.setdefault(
        "GENAI_MODEL",
        os.environ.get("GOVERNANCE_GENAI_MODEL", "gemma-4-26b-a4b-it").strip(),
    )
    ns.setdefault(
        "THINKING_MODEL",
        os.environ.get("GOVERNANCE_THINKING_MODEL", "gemma-4-31b-it").strip(),
    )
    ns.setdefault(
        "GATEKEEPER_MODEL",
        os.environ.get("GOVERNANCE_GATEKEEPER_MODEL", "gemma-4-e2b-it").strip(),
    )
    ns.setdefault(
        "SHIELD_MODEL",
        (
            os.environ.get("GOVERNANCE_SHIELD_MODEL", "shieldgemma-9b").strip()
            or ns["GENAI_MODEL"]
        ),
    )
    ns.setdefault(
        "DEMO4_MODEL",
        os.environ.get("GOVERNANCE_DEMO4_HF_MODEL", "google/gemma-4-E2B-it").strip()
        or "google/gemma-4-E2B-it",
    )
    ns.setdefault("MAX_PDFS_PER_JUR", int(os.environ.get("GOVERNANCE_DEMO_MAX_PDFS_PER_JUR", "3")))
    ns.setdefault(
        "MAX_PAGES_PER_PDF", int(os.environ.get("GOVERNANCE_DEMO_MAX_PAGES_PER_PDF", "8"))
    )
    ns.setdefault(
        "MAX_AUDIO_PER_JUR", int(os.environ.get("GOVERNANCE_DEMO_MAX_AUDIO_PER_JUR", "1"))
    )
    ns.setdefault(
        "MAX_AUDIO_CHUNKS", int(os.environ.get("GOVERNANCE_DEMO_MAX_AUDIO_CHUNKS", "4"))
    )
    ns.setdefault(
        "THINKING_BUDGET", int(os.environ.get("GOVERNANCE_DEMO_THINKING_BUDGET", "-1"))
    )
    if "DRIFT_FOCUS" not in ns:
        raw = os.environ.get("GOVERNANCE_DRIFT_FOCUS", "").strip()
        ns["DRIFT_FOCUS"] = raw or None
    if "GATEKEEPER_MAX_FILES" not in ns:
        _gate = os.environ.get("GOVERNANCE_GATEKEEPER_MAX_FILES", "").strip()
        ns["GATEKEEPER_MAX_FILES"] = int(_gate) if _gate else None

    print("§6: loaded API_KEY + model ids from .env / environment / Colab Secrets.")
    return True


def prepare_section6_phase1(namespace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ensure §1–§5 globals exist; restore §4 keys if missing. Returns notebook namespace.

    Raises ``RuntimeError`` with a short fix list when ``GEMINI_API_KEY`` / ``INVENTORIES`` missing.
    """
    ns = _user_ns(namespace)
    repo = _repo_from_ns(ns)
    if repo is not None:
        _ensure_import_paths(repo)
        os.environ.setdefault("OPEN_NAVIGATOR_ROOT", str(repo))

    try:
        from colab_runtime_phases import (
            ensure_paths_from_bootstrap,
            hydrate_pipeline_paths,
            require_section6_prereqs,
        )
    except ImportError:
        from runtime.colab_runtime_phases import (  # type: ignore
            ensure_paths_from_bootstrap,
            hydrate_pipeline_paths,
            require_section6_prereqs,
        )

    ensure_paths_from_bootstrap(ns)
    hydrate_pipeline_paths(ns)

    if not ns.get("API_KEY"):
        if not load_api_keys_into_ns(ns, repo):
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Before §6:\n"
                "  • Local / Colab extension: copy .env.example → .env with GEMINI_API_KEY=...\n"
                "  • Colab cloud: 🔑 Secrets → GEMINI_API_KEY (notebook access ON)\n"
                "Then re-run §4 (must print model lines) or run this §6 Phase 1 cell again."
            )

    require_section6_prereqs(ns)
    return ns
