"""
Restore notebook state after a Colab **runtime restart** (CPU ↔ GPU).

Judges: set ``GOVERNANCE_COLAB_SINGLE_RUNTIME=1`` in §0 and use **one L4 GPU**
for the whole run — skip the Phase 1 checkpoint cell.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from notebook_section6 import (
    SECTION6_RUNTIME_MARKER,
    _ensure_import_paths,
    _user_ns,
    ensure_inventories,
    import_colab_runtime_phases,
    load_colab_confirm_ui,
    resolve_section6_repo,
)


def single_runtime_mode() -> bool:
    """When true, run PDF + video on one GPU session (no CPU phase 1 requirement)."""
    return os.environ.get("GOVERNANCE_COLAB_SINGLE_RUNTIME", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def configure_judge_single_runtime_defaults() -> None:
    """§0 helper: one GPU runtime, no dropdown gates, persist repo path hint."""
    os.environ.setdefault("GOVERNANCE_COLAB_SINGLE_RUNTIME", "1")
    os.environ.setdefault("GOVERNANCE_COLAB_SKIP_CONFIRM_UI", "1")
    os.environ.setdefault("GOVERNANCE_COLAB_SKIP_GPU_CONFIRM", "1")
    os.environ.setdefault("OPEN_NAVIGATOR_ROOT", "/content/c1_gemma_4_good")


def find_repo_root(namespace: Optional[Dict[str, Any]] = None) -> Path:
    """Locate checkout even when ``cwd`` is not the repo (common after GPU restart)."""
    try:
        return resolve_section6_repo(namespace)
    except ModuleNotFoundError:
        pass
    content = Path("/content")
    if content.is_dir():
        for py in sorted(content.glob("*/scripts/colab/runtime/colab_runtime_phases.py")):
            return py.parents[3].resolve()
        for py in sorted(content.glob("*/scripts/colab/utils/colab_confirm_ui.py")):
            return py.parents[3].resolve()
    raise ModuleNotFoundError(
        f"Cannot find repo ({SECTION6_RUNTIME_MARKER}). "
        "After a runtime change: re-run **§0** and **§1** (clones to /content/c1_gemma_4_good), "
        "then **§2–§5**, then §6."
    )


def restore_colab_session(
    namespace: Optional[Dict[str, Any]] = None,
    *,
    sync_judge_corpus: bool = True,
) -> Path:
    """
    Rehydrate paths, API keys, and ``INVENTORIES`` after kernel restart.

    Call at the top of any §6 cell (or the post-restart helper cell).
    """
    ns = _user_ns(namespace)
    repo = find_repo_root(ns)
    os.environ["OPEN_NAVIGATOR_ROOT"] = str(repo)
    ns["REPO_PATH"] = repo
    _ensure_import_paths(repo)

    try:
        from judge_pipeline_sync import judge_mode_enabled, prepare_judge_pipeline
    except ImportError:
        from utils.judge_pipeline_sync import judge_mode_enabled, prepare_judge_pipeline  # type: ignore

    if sync_judge_corpus and judge_mode_enabled():
        try:
            prepare_judge_pipeline()
        except Exception as exc:
            print(f"restore: judge sync skipped ({type(exc).__name__}: {exc})")

    crp = import_colab_runtime_phases(repo)
    crp.ensure_paths_from_bootstrap(ns)
    crp.hydrate_pipeline_paths(ns)
    if not crp.hydrate_api_and_models(ns):
        from notebook_section6 import load_api_keys_into_ns

        if not load_api_keys_into_ns(ns, repo):
            raise RuntimeError(
                "GEMINI_API_KEY missing after restore. Re-run §4, or in §0:\n"
                "  os.environ['GEMINI_API_KEY'] = 'AIza...'\n"
                "Colab Secrets must have GEMINI_API_KEY (notebook access ON)."
            )

    ensure_inventories(ns, repo)
    mode = "single GPU" if single_runtime_mode() else "two-phase (CPU then GPU)"
    print(f"✓ Session restored — repo={repo}  mode={mode}  "
          f"jurisdictions={len(ns.get('INVENTORIES') or [])}")
    return repo


def run_phase1_checkpoint_optional(namespace: Optional[Dict[str, Any]] = None) -> None:
    """Phase 1 → GPU gate; no-op in single-runtime / skip-confirm mode; never hard-fails on import."""
    if single_runtime_mode() or os.environ.get("GOVERNANCE_COLAB_SKIP_CONFIRM_UI", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        print(
            "⊘ Phase 1 checkpoint skipped (GOVERNANCE_COLAB_SINGLE_RUNTIME or "
            "GOVERNANCE_COLAB_SKIP_CONFIRM_UI)."
        )
        return

    restore_colab_session(namespace)
    try:
        load_colab_confirm_ui().confirm_phase1_finished_checkpoint()
    except ModuleNotFoundError:
        print(
            "\n⏸ After Phase 1: switch to **L4 GPU**, restart, re-run **§0 → §1 → §5**.\n"
            "Type YES when ready for Phase 2: "
        )
        if input().strip().upper() != "YES":
            raise RuntimeError("Stopped — complete GPU switch and §1–§5 first.")
