"""
Interactive confirmation gates for Colab (ipywidgets dropdown + Continue button).

Blocks the notebook until the user picks the correct status — harder to skip than markdown alone.
"""

from __future__ import annotations

import os
import re
import threading
from typing import Sequence, Tuple

Choice = Tuple[str, str]  # (dropdown label, internal value)


def confirm_ui_skipped() -> bool:
    return os.environ.get("GOVERNANCE_COLAB_SKIP_CONFIRM_UI", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ) or os.environ.get("GOVERNANCE_COLAB_SKIP_GPU_CONFIRM", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def wait_for_dropdown_confirm(
    *,
    title: str,
    steps_html: str,
    choices: Sequence[Choice],
    allowed_value: str,
    button_label: str = "Continue ▶",
    cancel_raises: bool = True,
) -> str:
    """
    Show a dropdown + Continue button; block until ``allowed_value`` is selected and clicked.

    Falls back to ``input("Type YES…")`` when ipywidgets is unavailable.
    """
    if confirm_ui_skipped():
        print(f"⊘ Confirmation UI skipped ({title})")
        return allowed_value

    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        return _fallback_text_confirm(title, steps_html, allowed_value, cancel_raises)

    done = threading.Event()
    state = {"value": None, "confirmed": False}

    dd = widgets.Dropdown(
        options=[(label, val) for label, val in choices],
        description="Status:",
        style={"description_width": "72px"},
        layout=widgets.Layout(width="98%"),
    )
    btn = widgets.Button(
        description=button_label,
        button_style="success",
        disabled=True,
        layout=widgets.Layout(width="260px"),
    )
    status = widgets.HTML(
        value=(
            "<p style='margin:8px 0 0 0;color:#b45309'>"
            "<b>⏸ Stopped —</b> choose the accurate option, then click <b>Continue</b>.</p>"
        )
    )
    banner = widgets.HTML(
        value=(
            f"<div style='padding:12px 14px;border:2px solid #f59e0b;border-radius:8px;"
            f"background:#fffbeb'>"
            f"<h3 style='margin:0 0 8px 0'>{title}</h3>{steps_html}</div>"
        )
    )

    def _on_dropdown(change):
        btn.disabled = change.new != allowed_value
        if change.new == allowed_value:
            status.value = (
                "<p style='color:#15803d;margin:8px 0 0 0'>"
                "<b>OK —</b> click <b>Continue</b> to proceed.</p>"
            )
        else:
            status.value = (
                "<p style='color:#b45309;margin:8px 0 0 0'>"
                "<b>⏸ Stopped —</b> complete the checklist steps first.</p>"
            )

    def _on_button(_btn):
        if dd.value != allowed_value:
            status.value = (
                "<p style='color:#dc2626'><b>Cannot continue</b> — select the ✅ option.</p>"
            )
            return
        state["value"] = dd.value
        state["confirmed"] = True
        status.value = "<p style='color:#15803d'><b>Confirmed — proceeding…</b></p>"
        btn.disabled = True
        dd.disabled = True
        done.set()

    dd.observe(_on_dropdown, names="value")
    btn.on_click(_on_button)
    display(widgets.VBox([banner, dd, btn, status]))
    done.wait()
    if not state["confirmed"] and cancel_raises:
        raise RuntimeError(f"Stopped at gate: {title}")
    return state["value"] or allowed_value


def _fallback_text_confirm(
    title: str,
    steps_html: str,
    allowed_value: str,
    cancel_raises: bool,
) -> str:
    plain = re.sub(r"<[^>]+>", "", steps_html)
    print("\n" + "=" * 60)
    print(title)
    print(plain)
    print("=" * 60)
    answer = input('\nType YES (all steps done) to continue: ')
    if answer.strip().upper() != "YES":
        if cancel_raises:
            raise RuntimeError(f"Stopped at gate: {title}")
        return ""
    return allowed_value


def confirm_phase1_finished_checkpoint() -> None:
    """Run once after §6 Phase 1 — blocks before switching to GPU / Phase 2."""
    wait_for_dropdown_confirm(
        title="⏸ Checkpoint — Phase 1 must finish before Phase 2",
        steps_html=(
            "<ol style='margin:8px 0 0 18px;line-height:1.5'>"
            "<li>Phase 1 printed <code>Phase 1 complete</code></li>"
            "<li><b>Runtime → Change runtime type → L4 GPU</b> (or T4), <b>High RAM</b> if offered</li>"
            "<li><b>Runtime → Restart session</b></li>"
            "<li>Re-run <b>§1 → §5</b> (not Phase 2 yet)</li>"
            "</ol>"
        ),
        choices=[
            ("⛔ Not yet — Phase 1 still running or have not switched to GPU", "wait"),
            (
                "✅ Phase 1 complete · GPU runtime · restarted · re-ran §1–§5",
                "ready",
            ),
        ],
        allowed_value="ready",
        button_label="Continue to GPU confirm ▶",
    )


def confirm_phase2_gpu_checkpoint(*, cuda_ok: bool) -> None:
    """Final gate immediately before Phase 2 pipeline (GPU + HF Demo 4)."""
    if not cuda_ok:
        wait_for_dropdown_confirm(
            title="⚠ No GPU detected",
            steps_html=(
                "<p>Demo 4 (video) needs a <b>GPU</b> runtime. Switch runtime, restart, "
                "re-run §1–§5, then return here.</p>"
            ),
            choices=[
                ("⛔ Stop — I will switch to GPU first", "stop"),
                ("⚠ Continue on CPU anyway (likely fails)", "force"),
            ],
            allowed_value="force",
            button_label="Continue on CPU anyway ▶",
        )
        return

    wait_for_dropdown_confirm(
        title="▶ Phase 2 — video / Demo 4 (GPU)",
        steps_html=(
            "<ol style='margin:8px 0 0 18px;line-height:1.5'>"
            "<li>Phase 1 PDF outputs are on Drive</li>"
            "<li>This runtime shows a <b>GPU</b></li>"
            "<li><code>HF_TOKEN</code> is in Colab secrets (§4)</li>"
            "</ol>"
        ),
        choices=[
            ("⛔ Not ready — missing GPU, HF_TOKEN, or §1–§5 rerun", "no"),
            ("✅ Ready — run Phase 2 (ffmpeg + Demo 4)", "yes"),
        ],
        allowed_value="yes",
        button_label="Run Phase 2 ▶",
    )
