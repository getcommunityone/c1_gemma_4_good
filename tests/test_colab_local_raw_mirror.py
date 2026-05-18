"""Local mirror flattens nested judge gdown trees onto flat ``01_raw_inputs/AL/…``."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_COLAB = _REPO / "scripts" / "colab"
for _p in (_COLAB, _COLAB / "engine", _COLAB / "runtime", _COLAB / "utils"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from governance_meeting_llm import walk_raw_inputs  # noqa: E402
from colab_local_raw_mirror import mirror_inventories_to_local_raw  # noqa: E402
from scripts.utils.gdrive_paths import resolve_effective_raw_inputs_root  # noqa: E402


def test_mirror_flattens_nested_judge_tree_to_local_al_layout(tmp_path: Path, monkeypatch) -> None:
    pipeline = tmp_path / "governance_pipeline_local"
    download_target = pipeline / "01_raw_inputs"
    nested = (
        download_target
        / "2026_Gemma_4_Good"
        / "01_raw_inputs"
        / "AL"
        / "county"
        / "county_01125"
    )
    nested.mkdir(parents=True)
    pdf = nested / "2026_02_18-MINUTES.pdf"
    pdf.write_bytes(b"%PDF")

    local_flat = tmp_path / "local_mirror" / "01_raw_inputs"
    effective = resolve_effective_raw_inputs_root(download_target)
    inventories = [inv for inv in walk_raw_inputs(effective) if inv.has_media]
    assert len(inventories) == 1
    assert inventories[0].pdfs[0] == pdf

    monkeypatch.setenv("GOVERNANCE_JUDGE_MODE", "1")
    monkeypatch.setenv("GOVERNANCE_LOCAL_RAW_MIRROR", "1")
    monkeypatch.setenv("COLAB_RELEASE_TAG", "1")
    monkeypatch.setattr("colab_local_raw_mirror.in_colab", lambda: True)

    remapped, raw_root = mirror_inventories_to_local_raw(
        inventories,
        effective,
        local_raw_root=local_flat,
    )

    assert raw_root == local_flat.resolve()
    flat_pdf = local_flat / "AL" / "county" / "county_01125" / "2026_02_18-MINUTES.pdf"
    assert flat_pdf.is_file()
    assert remapped[0].pdfs[0] == flat_pdf
    assert remapped[0].jurisdiction.root == flat_pdf.parent
