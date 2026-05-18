"""
Re-export §6 runtime helpers when only ``<repo>/scripts/colab`` is on ``sys.path``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_RUNTIME_PY = Path(__file__).resolve().parent / "runtime" / "colab_runtime_phases.py"
_spec = importlib.util.spec_from_file_location("colab_runtime_phases", _RUNTIME_PY)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
sys.modules.setdefault("colab_runtime_phases", _mod)

SECTION6_REQUIRED_NAMES = _mod.SECTION6_REQUIRED_NAMES
apply_media_scope_for_phase = _mod.apply_media_scope_for_phase
confirm_gpu_for_demo4 = _mod.confirm_gpu_for_demo4
ensure_cpu_runtime = _mod.ensure_cpu_runtime
ensure_paths_from_bootstrap = _mod.ensure_paths_from_bootstrap
hydrate_api_and_models = _mod.hydrate_api_and_models
hydrate_pipeline_paths = _mod.hydrate_pipeline_paths
require_section6_prereqs = _mod.require_section6_prereqs

__all__ = [
    "SECTION6_REQUIRED_NAMES",
    "apply_media_scope_for_phase",
    "confirm_gpu_for_demo4",
    "ensure_cpu_runtime",
    "ensure_paths_from_bootstrap",
    "hydrate_api_and_models",
    "hydrate_pipeline_paths",
    "require_section6_prereqs",
]
