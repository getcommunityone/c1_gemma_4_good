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
        from colab_secrets import load_dotenv_all_candidates
    except ImportError:
        from utils.colab_secrets import load_dotenv_all_candidates  # type: ignore

    pipe_root = None
    if ns.get("PIPE") is not None:
        pipe_root = getattr(ns["PIPE"], "root", None)
    load_dotenv_all_candidates(repo=repo, pipeline_root=pipe_root)
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


def load_colab_confirm_ui(repo: Optional[Path] = None) -> Any:
    """Import ``colab_confirm_ui`` (ipywidgets checkpoint gates)."""
    import importlib
    import importlib.util

    r = repo or _repo_from_ns(_user_ns())
    if r is not None:
        _ensure_import_paths(r)
    try:
        import colab_confirm_ui

        return colab_confirm_ui
    except ImportError:
        pass
    if r is not None:
        path = r / "scripts" / "colab" / "utils" / "colab_confirm_ui.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location("colab_confirm_ui", path)
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)
            sys.modules["colab_confirm_ui"] = mod
            return mod
    try:
        from scripts.colab.utils import colab_confirm_ui

        return colab_confirm_ui
    except ImportError as exc:
        raise ModuleNotFoundError(
            "colab_confirm_ui.py not found. Re-run §1 (git pull) so "
            "scripts/colab/utils/colab_confirm_ui.py exists in your checkout."
        ) from exc


def run_phase1_finished_checkpoint(namespace: Optional[Dict[str, Any]] = None) -> None:
    """§6 Phase 1 checkpoint — dropdown gate before switching to GPU."""
    repo = _repo_from_ns(_user_ns(namespace))
    load_colab_confirm_ui(repo).confirm_phase1_finished_checkpoint()


def ensure_inventories(ns: Dict[str, Any], repo: Optional[Path] = None) -> list[Any]:
    """
    Build ``INVENTORIES`` when §5 was skipped or the kernel was restarted after §5.

    Syncs judge public corpus first when ``01_raw_inputs`` is empty.
    """
    existing = ns.get("INVENTORIES")
    if existing:
        return existing

    try:
        from colab_runtime_phases import hydrate_pipeline_paths
    except ImportError:
        from runtime.colab_runtime_phases import hydrate_pipeline_paths  # type: ignore

    hydrate_pipeline_paths(ns)

    pipe = ns.get("PIPE")
    if pipe is None:
        raise RuntimeError("PIPE missing — re-run §3 Install, then §5 Inventory.")

    try:
        from scripts.utils.gdrive_paths import resolve_governance_raw_inputs_root
    except ImportError:
        from utils.gdrive_paths import resolve_governance_raw_inputs_root  # type: ignore

    raw_root = Path(resolve_governance_raw_inputs_root(pipe.root))

    try:
        from judge_pipeline_sync import judge_mode_enabled, prepare_judge_pipeline
    except ImportError:
        from utils.judge_pipeline_sync import judge_mode_enabled, prepare_judge_pipeline  # type: ignore

    if judge_mode_enabled() and not any(raw_root.rglob("*.pdf")) and not any(
        raw_root.rglob("*.opus")
    ):
        print("§6: empty 01_raw_inputs — syncing public judge corpus (gdown)…")
        prepare_judge_pipeline()
        raw_root = Path(resolve_governance_raw_inputs_root(pipe.root))

    if not raw_root.is_dir():
        raise RuntimeError(
            f"Raw inputs missing: {raw_root}\n"
            "Re-run §0 → §1 (judge sync) → §5, or set GOVERNANCE_RAW_INPUTS_ROOT."
        )

    from governance_meeting_llm import walk_raw_inputs

    try:
        from demo_scope import filter_inventories_for_scope, get_active_preset
    except ImportError:
        sys.path.insert(0, str((repo or ns.get("PATHS").project_path) / "scripts" / "colab"))
        from demo_scope import filter_inventories_for_scope, get_active_preset

    all_inv = [inv for inv in walk_raw_inputs(raw_root) if inv.has_media]
    scoped = filter_inventories_for_scope(all_inv, get_active_preset())

    ns["DRIVE_RAW_ROOT"] = raw_root
    ns["RAW_ROOT"] = raw_root
    ns["INVENTORIES"] = scoped

    print(f"§6: built inventory from {raw_root} → {len(scoped)} jurisdiction(s) for active scope")
    if not scoped:
        raise RuntimeError(
            f"No PDF/audio found under {raw_root} for scope {get_active_preset().name!r}. "
            "Re-run §0 → §1 (wait for gdown), then §5."
        )
    return scoped


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
        try:
            from colab_runtime_phases import hydrate_api_and_models
        except ImportError:
            from runtime.colab_runtime_phases import hydrate_api_and_models  # type: ignore

        hydrate_api_and_models(ns)
    if not ns.get("API_KEY"):
        if not load_api_keys_into_ns(ns, repo):
            _repo_hint = str(repo or os.environ.get("OPEN_NAVIGATOR_ROOT", "/content/c1_gemma_4_good"))
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Before §6:\n"
                "  • Colab cloud: 🔑 Secrets → GEMINI_API_KEY (notebook access ON), then re-run §4\n"
                "  • Or upload .env to "
                f"{_repo_hint}/.env\n"
                "  • Or in §0 set: os.environ['GEMINI_API_KEY'] = 'AIza...'  (paste your key)\n"
                "  • Local / Cursor: copy .env.example → .env in the repo, re-run §1 and §4\n"
                "Then re-run §4 (must print model lines) or this §6 Phase 1 cell again."
            )

    ensure_inventories(ns, repo)
    require_section6_prereqs(ns)
    return ns
