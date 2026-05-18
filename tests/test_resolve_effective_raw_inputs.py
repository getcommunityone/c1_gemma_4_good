"""Layout helpers for judge gdown sync → §5 inventory."""

from pathlib import Path

from scripts.utils.gdrive_paths import (
    diagnose_raw_inputs_layout,
    raw_inputs_has_jurisdiction_layout,
    resolve_effective_raw_inputs_root,
)


def test_resolve_nested_hackathon_tree_under_01_raw_inputs(tmp_path: Path) -> None:
    download_target = tmp_path / "01_raw_inputs"
    effective = (
        download_target
        / "CommunityOne"
        / "hackathons"
        / "2026_Gemma_4_Good"
        / "01_raw_inputs"
        / "AL"
        / "county"
        / "county_01125"
    )
    (effective / "meetings").mkdir(parents=True)
    (effective / "meetings" / "minutes.pdf").write_bytes(b"%PDF")

    assert resolve_effective_raw_inputs_root(download_target) == (
        download_target
        / "CommunityOne"
        / "hackathons"
        / "2026_Gemma_4_Good"
        / "01_raw_inputs"
    ).resolve()
    assert raw_inputs_has_jurisdiction_layout(
        resolve_effective_raw_inputs_root(download_target)
    )


def test_resolve_2026_gemma_4_good_nested_without_communityone(tmp_path: Path) -> None:
    download_target = tmp_path / "01_raw_inputs"
    jur = (
        download_target
        / "2026_Gemma_4_Good"
        / "01_raw_inputs"
        / "AL"
        / "county"
        / "county_01125"
    )
    jur.mkdir(parents=True)
    (jur / "minutes.pdf").write_bytes(b"%PDF")
    assert resolve_effective_raw_inputs_root(download_target) == (
        download_target / "2026_Gemma_4_Good" / "01_raw_inputs"
    ).resolve()


def test_resolve_flat_al_layout_unchanged(tmp_path: Path) -> None:
    jur = tmp_path / "AL" / "county" / "county_01125"
    jur.mkdir(parents=True)
    (jur / "a.pdf").write_bytes(b"%PDF")
    assert resolve_effective_raw_inputs_root(tmp_path) == tmp_path.resolve()


def test_diagnose_mentions_nested_fix(tmp_path: Path) -> None:
    download_target = tmp_path / "01_raw_inputs"
    download_target.mkdir()
    (download_target / "CommunityOne").mkdir()
    msg = diagnose_raw_inputs_layout(download_target)
    assert "CommunityOne" in msg or "Expected layout" in msg
