"""
Re-export checkpoint UI so ``from colab_confirm_ui import …`` works when only
``<repo>/scripts/colab`` is on ``sys.path`` (§3 / §4), not ``…/utils``.
"""

from __future__ import annotations

try:
    from utils.colab_confirm_ui import (  # type: ignore
        confirm_phase1_finished_checkpoint,
        confirm_phase2_gpu_checkpoint,
        confirm_ui_skipped,
        wait_for_dropdown_confirm,
    )
except ImportError:
    from scripts.colab.utils.colab_confirm_ui import (  # type: ignore
        confirm_phase1_finished_checkpoint,
        confirm_phase2_gpu_checkpoint,
        confirm_ui_skipped,
        wait_for_dropdown_confirm,
    )

__all__ = [
    "confirm_phase1_finished_checkpoint",
    "confirm_phase2_gpu_checkpoint",
    "confirm_ui_skipped",
    "wait_for_dropdown_confirm",
]
