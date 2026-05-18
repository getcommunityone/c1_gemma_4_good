"""Tests for Colab notebook path resolution."""

from __future__ import annotations

import sys
from pathlib import Path


_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from scripts.colab.utils import colab_paths  # noqa: E402


def test_setup_notebook_paths_falls_back_to_local_content_when_drive_missing(
    monkeypatch, tmp_path
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    fallback = tmp_path / "governance_pipeline_local"
    mount = tmp_path / "content_drive"
    mount.mkdir()

    monkeypatch.setattr(colab_paths, "repo_root_from_this_file", lambda: repo)
    monkeypatch.setattr(colab_paths, "in_colab", lambda: True)
    monkeypatch.setattr(
        colab_paths,
        "_colab_drive_candidates",
        lambda mount_point="/content/drive": [Path(mount_point) / "MyDrive" / "CommunityOne" / "hackathons" / "2026_Gemma_4_Good"],
    )
    monkeypatch.setattr(colab_paths, "_DEFAULT_COLAB_PIPELINE_ROOT", fallback)
    monkeypatch.delenv("GOVERNANCE_PIPELINE_DATA_ROOT", raising=False)

    paths = colab_paths.setup_notebook_paths(str(mount))

    assert paths.in_colab is True
    assert paths.project_path == repo
    assert paths.governance_pipeline_data == fallback
    assert fallback.is_dir()