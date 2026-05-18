"""Regression tests for audio inventory discovery in the Colab engine."""

from __future__ import annotations

import sys
from pathlib import Path


_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from scripts.colab.engine.governance_meeting_llm import mime_for, walk_raw_inputs  # noqa: E402


def test_walk_raw_inputs_includes_mp3_files(tmp_path) -> None:
    raw_root = tmp_path / "01_raw_inputs"
    jur_dir = raw_root / "AL" / "county" / "county_01125"
    jur_dir.mkdir(parents=True)
    mp3_path = jur_dir / "meeting_audio.MP3"
    mp3_path.write_bytes(b"fake mp3 bytes")

    inventories = list(walk_raw_inputs(raw_root))

    assert len(inventories) == 1
    assert inventories[0].jurisdiction.relative_label == "AL/county/county_01125"
    assert inventories[0].audio == [mp3_path]
    assert inventories[0].has_media is True


def test_mime_for_mp3_is_audio_mpeg(tmp_path) -> None:
    mp3_path = tmp_path / "clip.mp3"
    mp3_path.write_bytes(b"fake mp3 bytes")

    assert mime_for(mp3_path) == "audio/mpeg"