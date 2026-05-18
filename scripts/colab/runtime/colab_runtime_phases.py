"""
Colab two-phase runtime helpers: CPU for PDF/API work, GPU for Demo 4 (HF + ffmpeg).

Used by ``run_in_colab.ipynb`` §6 — not required for local runs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

# Notebook globals expected after §1–§5 (§5 may set ``_demo_date_cap`` separately).
SECTION6_REQUIRED_NAMES: Sequence[str] = (
    "PATHS",
    "PIPE",
    "API_KEY",
    "POLICY_PROMPT",
    "INVENTORIES",
    "RAW_ROOT",
    "PROCESSED_ROOT",
    "GEMMA_JSON_ROOT",
    "SUMMARIES_ROOT",
    "SCRATCH_AUDIO_ROOT",
    "GENAI_MODEL",
    "THINKING_MODEL",
    "DEMO4_MODEL",
    "GATEKEEPER_MODEL",
    "SHIELD_MODEL",
    "MAX_PDFS_PER_JUR",
    "MAX_PAGES_PER_PDF",
    "MAX_AUDIO_PER_JUR",
    "MAX_AUDIO_CHUNKS",
    "THINKING_BUDGET",
    "DRIFT_FOCUS",
    "GATEKEEPER_MAX_FILES",
)

_SECTION4_NAMES: frozenset[str] = frozenset(
    {
        "API_KEY",
        "GENAI_MODEL",
        "THINKING_MODEL",
        "DEMO4_MODEL",
        "GATEKEEPER_MODEL",
        "SHIELD_MODEL",
        "MAX_PDFS_PER_JUR",
        "MAX_PAGES_PER_PDF",
        "MAX_AUDIO_PER_JUR",
        "MAX_AUDIO_CHUNKS",
        "THINKING_BUDGET",
        "DRIFT_FOCUS",
        "GATEKEEPER_MAX_FILES",
    }
)

_SECTION5_PATH_NAMES: frozenset[str] = frozenset(
    {
        "RAW_ROOT",
        "PROCESSED_ROOT",
        "GEMMA_JSON_ROOT",
        "SUMMARIES_ROOT",
        "SCRATCH_AUDIO_ROOT",
        "INVENTORIES",
    }
)


def colab_two_phase_enabled() -> bool:
    """Notebook §6 runs PDF on CPU, then video on GPU (default on)."""
    return os.environ.get("GOVERNANCE_COLAB_TWO_PHASE", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )


def cuda_available() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except ImportError:
        return False


def runtime_label() -> str:
    if cuda_available():
        try:
            import torch

            return f"GPU ({torch.cuda.get_device_name(0)})"
        except Exception:
            return "GPU"
    return "CPU"


def ensure_cpu_runtime(*, phase: str = "PDFs, gatekeeper, Demo 3") -> None:
    """Raise if Colab is on a GPU runtime (phase 1 should use CPU)."""
    if cuda_available():
        raise RuntimeError(
            f"\n{'=' * 60}\n"
            f"Phase 1 ({phase}) must run on a **CPU** runtime.\n\n"
            "1. Runtime → Change runtime type → **CPU** (standard)\n"
            "2. Runtime → **Restart session**\n"
            "3. Re-run **§1 → §5**, then **§6 Phase 1** only\n"
            f"{'=' * 60}\n"
        )
    print(f"✓ Phase 1 runtime: {runtime_label()} (expected CPU)")


def confirm_gpu_for_demo4(*, interactive: bool = True) -> None:
    """
    Block until the user confirms a GPU runtime for Demo 4 / video.

    Uses an ipywidgets dropdown + **Continue** when available (see ``colab_confirm_ui``).
    Set ``GOVERNANCE_COLAB_SKIP_GPU_CONFIRM=1`` or ``GOVERNANCE_COLAB_SKIP_CONFIRM_UI=1`` to skip.
    """
    if os.environ.get("GOVERNANCE_COLAB_SKIP_GPU_CONFIRM", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        if not cuda_available():
            print(
                "⚠ GOVERNANCE_COLAB_SKIP_GPU_CONFIRM=1 but no GPU detected — "
                "Demo 4 HF will likely fail."
            )
        else:
            print(f"✓ Phase 2 runtime: {runtime_label()} (confirm skipped)")
        return

    gpu = cuda_available()
    if interactive:
        try:
            from colab_confirm_ui import confirm_phase2_gpu_checkpoint

            confirm_phase2_gpu_checkpoint(cuda_ok=gpu)
        except ImportError:
            try:
                from scripts.colab.utils.colab_confirm_ui import (
                    confirm_phase2_gpu_checkpoint,
                )

                confirm_phase2_gpu_checkpoint(cuda_ok=gpu)
            except ImportError:
                _confirm_gpu_for_demo4_text(interactive=interactive, gpu=gpu)
    else:
        if not gpu:
            raise RuntimeError("Phase 2 requires a GPU runtime.")

    print(f"✓ Phase 2 runtime: {runtime_label()}")


def _confirm_gpu_for_demo4_text(*, interactive: bool, gpu: bool) -> None:
    """Fallback when ipywidgets / colab_confirm_ui is unavailable."""
    if not gpu:
        msg = (
            "\nNo GPU detected.\n\n"
            "1. Finish **§6 Phase 1** on CPU (PDF outputs saved to Drive).\n"
            "2. Runtime → Change runtime type → **L4 GPU** (or T4), **High RAM** if offered\n"
            "3. Runtime → **Restart session**\n"
            "4. Re-run **§1 → §5**, then **§6 Phase 2** (confirm + run)\n"
        )
        if not interactive:
            raise RuntimeError(msg)
        answer = input(msg + "\nType YES to continue on CPU anyway (likely fails): ")
        if answer.strip().upper() != "YES":
            raise RuntimeError("Stopped — connect a GPU runtime first.")
        return

    answer = input(
        "\n**Phase 2 — video / Demo 4 (Hugging Face E2B on GPU)**\n\n"
        "Confirm:\n"
        "  • Phase 1 finished (PDF / Demo 3 on Drive), and\n"
        "  • You switched to **GPU + High RAM** and restarted.\n"
        "  • You re-ran **§1 → §5** after the restart.\n\n"
        "Type YES to run Phase 2: "
    )
    if answer.strip().upper() != "YES":
        raise RuntimeError(
            "Stopped — complete Phase 1 on CPU, switch to GPU, re-run §1–§5, then Phase 2."
        )


def apply_media_scope_for_phase(media_key: str, namespace: Optional[Dict[str, Any]] = None) -> Any:
    """Set ``GOVERNANCE_PIPELINE_MEDIA_SCOPE`` and optional notebook globals."""
    from pipeline_media_scope import apply_media_scope

    key = (media_key or "all").strip().lower()
    os.environ["GOVERNANCE_PIPELINE_MEDIA_SCOPE"] = key
    cfg = apply_media_scope(key)
    if namespace is not None:
        namespace["ACTIVE_MEDIA"] = cfg
        namespace["_media"] = key
    print(f"Pipeline media scope → {cfg.label} ({key!r})")
    return cfg


def print_after_video_cpu_recommendation() -> None:
    print(
        "\n"
        "=" * 60 + "\n"
        "Phase 2 complete — **switch back to CPU** (recommended)\n"
        "=" * 60 + "\n"
        "GPU sessions disconnect more often during peak hours. You do not need GPU for:\n"
        "  • optional §7–§9 reruns that only touch Google API text\n"
        "  • safety review, browsing Drive outputs, or judging summaries\n\n"
        "1. Runtime → Change runtime type → **CPU**\n"
        "2. Runtime → Restart session (optional)\n"
        "3. Open outputs on Drive under `03_processed_outputs/` and `03_human_summaries/`\n"
        "   (`GOVERNANCE_FORCE_REPROCESS=0` reuses work if you re-run later)\n"
    )


def _ensure_repo_on_syspath(repo_path: Path) -> None:
    root = repo_path.resolve()
    for entry in (
        str(root),
        str(root / "scripts" / "colab"),
        str(root / "scripts" / "colab" / "utils"),
    ):
        if entry not in sys.path:
            sys.path.insert(0, entry)


def resolve_colab_package_dir(namespace: Optional[Dict[str, Any]] = None) -> Path:
    """``scripts/colab`` directory for imports (works before ``PATHS`` exists)."""
    ns = namespace if namespace is not None else globals()
    if "PATHS" in ns:
        return Path(ns["PATHS"].project_path) / "scripts" / "colab"
    if "REPO_PATH" in ns:
        return Path(ns["REPO_PATH"]).resolve() / "scripts" / "colab"
    env = os.environ.get("OPEN_NAVIGATOR_ROOT", "").strip()
    if env:
        cand = Path(env).expanduser().resolve() / "scripts" / "colab"
        if (cand / "colab_runtime_phases.py").is_file():
            return cand
    for folder in (Path("/content/c1_gemma_4_good"), Path.cwd(), *Path.cwd().parents):
        cand = folder / "scripts" / "colab"
        if (cand / "colab_runtime_phases.py").is_file():
            return cand.resolve()
    raise RuntimeError(
        "Cannot find scripts/colab. Run **§1 Bootstrap**, then §2–§5, before §6."
    )


def ensure_paths_from_bootstrap(namespace: Optional[Dict[str, Any]] = None) -> None:
    """Restore ``PATHS`` when ``REPO_PATH`` exists but §1 globals were cleared."""
    ns = namespace if namespace is not None else globals()
    if "PATHS" in ns:
        return
    repo = ns.get("REPO_PATH")
    if repo is None:
        env = os.environ.get("OPEN_NAVIGATOR_ROOT", "").strip()
        if env:
            repo = Path(env).expanduser()
    if repo is None:
        return
    repo_path = Path(repo).resolve()
    os.environ.setdefault("OPEN_NAVIGATOR_ROOT", str(repo_path))
    _ensure_repo_on_syspath(repo_path)
    from scripts.colab.utils.colab_paths import maybe_mount_google_drive, setup_notebook_paths

    maybe_mount_google_drive()
    ns["PATHS"] = setup_notebook_paths()
    ns.setdefault("REPO_PATH", repo_path)


def _notebook_globals(namespace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """IPython user namespace (all prior cells), not a stale dict snapshot."""
    try:
        from IPython import get_ipython

        ip = get_ipython()
        if ip is not None:
            return ip.user_ns
    except Exception:
        pass
    return namespace if namespace is not None else globals()


def hydrate_pipeline_paths(namespace: Optional[Dict[str, Any]] = None) -> None:
    """Restore §3/§5 path globals when §1 ran but later cells were skipped."""
    ns = _notebook_globals(namespace)
    ensure_paths_from_bootstrap(ns)
    paths = ns.get("PATHS")
    if paths is None:
        return

    repo = Path(paths.project_path).resolve()
    _ensure_repo_on_syspath(repo)

    if "PIPE" not in ns:
        os.environ.setdefault(
            "GOVERNANCE_PIPELINE_DATA_ROOT", str(paths.governance_pipeline_data)
        )
        from scripts.utils.gdrive_paths import GovernancePipelinePaths

        ns["PIPE"] = GovernancePipelinePaths.resolve()

    pipe = ns["PIPE"]
    if "POLICY_PROMPT" not in ns:
        from governance_meeting_llm import load_text_file

        prompt_path = repo / "prompts" / "policy_analysis_v1.md"
        if not prompt_path.is_file():
            raise FileNotFoundError(f"Missing policy prompt: {prompt_path}")
        ns["POLICY_PROMPT"] = load_text_file(prompt_path)

    processed = pipe.root / "03_processed_outputs"
    ns.setdefault("PROCESSED_ROOT", processed)
    ns.setdefault("GEMMA_JSON_ROOT", processed / "02_gemma_json")
    ns.setdefault("SUMMARIES_ROOT", processed / "03_human_summaries")
    ns.setdefault("SCRATCH_AUDIO_ROOT", processed / "_scratch_audio_chunks")
    for p in (ns["GEMMA_JSON_ROOT"], ns["SUMMARIES_ROOT"], ns["SCRATCH_AUDIO_ROOT"]):
        Path(p).mkdir(parents=True, exist_ok=True)

    if "RAW_ROOT" not in ns:
        from scripts.utils.gdrive_paths import resolve_governance_raw_inputs_root

        ns["RAW_ROOT"] = resolve_governance_raw_inputs_root(pipe.root)


def _load_dotenv_everywhere(repo: Optional[Path] = None) -> None:
    """Load ``.env`` from repo, ``OPEN_NAVIGATOR_ROOT``, and parent folders of ``cwd``."""
    try:
        from colab_secrets import (
            default_local_secrets_mode,
            load_dotenv_from_parents,
            load_repo_dotenv,
        )
    except ImportError:
        from utils.colab_secrets import (  # type: ignore
            default_local_secrets_mode,
            load_dotenv_from_parents,
            load_repo_dotenv,
        )

    try:
        from colab_secrets import load_first_project_dotenv
    except ImportError:
        from utils.colab_secrets import load_first_project_dotenv  # type: ignore

    default_local_secrets_mode()
    load_first_project_dotenv()
    if repo is not None:
        load_repo_dotenv(repo)
    env_root = os.environ.get("OPEN_NAVIGATOR_ROOT", "").strip()
    if env_root:
        load_repo_dotenv(env_root)


def hydrate_api_and_models(namespace: Optional[Dict[str, Any]] = None) -> bool:
    """
    Restore §4 API keys and model ids from ``.env`` / ``os.environ`` when §4 did not finish.

    Returns True when ``API_KEY`` is set afterward.
    """
    ns = _notebook_globals(namespace)
    repo: Optional[Path] = None
    if ns.get("PATHS") is not None:
        repo = Path(ns["PATHS"].project_path).resolve()
        _ensure_repo_on_syspath(repo)
    elif ns.get("REPO_PATH") is not None:
        repo = Path(ns["REPO_PATH"]).resolve()
        _ensure_repo_on_syspath(repo)

    try:
        from colab_secrets import get_notebook_secret, sanitize_api_key
    except ImportError:
        from utils.colab_secrets import (  # type: ignore
            get_notebook_secret,
            sanitize_api_key,
        )

    _load_dotenv_everywhere(repo)

    if not ns.get("API_KEY"):
        gemini = sanitize_api_key(
            get_notebook_secret("GEMINI_API_KEY", repo=repo)
            or get_notebook_secret("GOOGLE_API_KEY", repo=repo)
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        if gemini:
            ns["API_KEY"] = gemini
            ns.setdefault("GEMINI_API_KEY", gemini)
            os.environ["GEMINI_API_KEY"] = gemini

    hf = sanitize_api_key(
        get_notebook_secret("HF_TOKEN", repo=repo) or os.environ.get("HF_TOKEN")
    )
    if hf:
        ns["HF_TOKEN"] = hf
        os.environ["HF_TOKEN"] = hf

    _apply_section4_defaults(ns)

    if not ns.get("API_KEY"):
        return False

    print(
        "§6 auto-config: restored §4 variables from .env / environment "
        "(re-run §4 for full model resolution if models look wrong)."
    )
    return True


def _apply_section4_defaults(ns: Dict[str, Any]) -> None:
    """Set §4 model/cap globals from env defaults (safe without running §4)."""
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
            or ns.get("GENAI_MODEL")
            or "gemma-4-26b-a4b-it"
        ),
    )

    if not str(ns.get("DEMO4_MODEL") or "").strip():
        try:
            from gemma_hf_backend import cuda_available, demo4_use_huggingface, resolve_demo4_hf_model

            if demo4_use_huggingface() and colab_two_phase_enabled() and not cuda_available():
                ns["DEMO4_MODEL"] = resolve_demo4_hf_model()
            elif demo4_use_huggingface() and cuda_available():
                from gemma_hf_backend import ensure_demo4_hf_ready

                ns["DEMO4_MODEL"] = ensure_demo4_hf_ready()
            else:
                ns["DEMO4_MODEL"] = (
                    os.environ.get("GOVERNANCE_DEMO4_MODEL", "").strip()
                    or ns.get("THINKING_MODEL")
                    or "gemma-4-31b-it"
                )
        except Exception:
            ns["DEMO4_MODEL"] = (
                os.environ.get("GOVERNANCE_DEMO4_HF_MODEL", "google/gemma-4-E2B-it").strip()
                or "google/gemma-4-E2B-it"
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


def require_section6_prereqs(namespace: Optional[Dict[str, Any]] = None) -> None:
    """Raise with a clear message if §1–§5 cells were not run in this session."""
    ns = _notebook_globals(namespace)
    ensure_paths_from_bootstrap(ns)
    hydrate_pipeline_paths(ns)
    hydrate_api_and_models(ns)

    missing = [name for name in SECTION6_REQUIRED_NAMES if name not in ns]

    if missing:
        if "INVENTORIES" in missing or _SECTION5_PATH_NAMES.intersection(missing):
            hint = (
                " Re-run **§5 Inventory** (and §3 Install if PIPE / POLICY_PROMPT are missing). "
                "After Runtime → Restart session: §1 → §3 → §4 → §5 → §6."
            )
        elif _SECTION4_NAMES.intersection(missing):
            hint = (
                " **§4 did not finish** (often HF_TOKEN / GEMINI Colab Secret timeout). "
                "Fix keys in Colab Secrets or repo `.env`, then **re-run §4** until you see "
                "model lines printed — then §6."
            )
        else:
            hint = " Run §1 → §5 in order, then §6."
        raise RuntimeError(
            "Missing " + ", ".join(missing) + "." + hint
        )
