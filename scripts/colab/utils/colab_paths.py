"""
Shared helpers for notebooks under ``scripts/colab/``.

Supports **Google Colab** (Drive mount + hackathon layout) and **local Jupyter /
VS Code** (repo checkout on ``sys.path``, pipeline data under ``data/hackathons/``).
"""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass
from pathlib import Path

# Single hackathon pipeline root (must match ``scripts/utils/gdrive_paths.py``).
HACKATHON_PIPELINE_ROOT_REL = Path("CommunityOne") / "hackathons" / "2026_Gemma_4_Good"
_DEFAULT_COLAB_PIPELINE_ROOT = Path("/content/governance_pipeline_local")


def in_colab() -> bool:
    """True on Colab cloud only — not the local Colab/Jupyter extension."""
    try:
        from colab_secrets import in_colab_runtime

        return in_colab_runtime()
    except ImportError:
        return bool(os.environ.get("COLAB_RELEASE_TAG")) and Path("/content").is_dir()


def repo_root_from_this_file() -> Path:
    """``c1_gemma_4_good`` root: ``.../scripts/colab/utils/colab_paths.py`` → ``parents[3]``."""
    return Path(__file__).resolve().parents[3]


def default_hackathon_pipeline_root_in_repo() -> Path:
    return repo_root_from_this_file() / "data" / "hackathons" / "2026_Gemma_4_Good"


# Colab: only ``CommunityOne/hackathons/2026_Gemma_4_Good`` (not ``governance_pipeline_data``).
_COLAB_DRIVE_CANDIDATES_REL = (
    "MyDrive/" + HACKATHON_PIPELINE_ROOT_REL.as_posix(),
)
_COLAB_SHARED_GLOBS_REL = (
    "Shareddrives/*/" + HACKATHON_PIPELINE_ROOT_REL.as_posix(),
)


def _colab_drive_candidates(mount_point: str = "/content/drive") -> list[Path]:
    """Ordered list of plausible governance-pipeline data roots under a mounted Drive."""
    mount = Path(mount_point)
    out: list[Path] = [mount / rel for rel in _COLAB_DRIVE_CANDIDATES_REL]
    for pattern in _COLAB_SHARED_GLOBS_REL:
        out.extend(sorted(Path(p) for p in glob.glob(str(mount / pattern))))
    return out


@dataclass(frozen=True)
class NotebookLayoutPaths:
    """Paths returned by :func:`setup_notebook_paths`."""

    in_colab: bool
    project_path: Path
    governance_pipeline_data: Path  # pipeline root (hackathon folder on Drive or in repo)


def setup_notebook_paths(mount_point: str = "/content/drive") -> NotebookLayoutPaths:
    """
    Resolve repo root and the governance pipeline data directory.

    - **project_path** — ``c1_gemma_4_good`` root (prompts, ``scripts.utils.gdrive_paths``, etc.).
    - **governance_pipeline_data** — hackathon root with ``01_raw_inputs``, ``02_reference_data``,
      ``03_processed_outputs``:

            - **Colab**: ``GOVERNANCE_PIPELINE_DATA_ROOT`` if set, else try
                ``/content/drive/MyDrive/CommunityOne/hackathons/2026_Gemma_4_Good`` when Drive is
                already mounted. If Drive is not mounted or the folder is missing, fall back to
                ``/content/governance_pipeline_local`` (no Drive auth required).
      - **Local**: ``<repo>/data/hackathons/2026_Gemma_4_Good`` unless ``GOVERNANCE_PIPELINE_DATA_ROOT`` is set.
    """
    repo = repo_root_from_this_file()
    explicit = (os.getenv("GOVERNANCE_PIPELINE_DATA_ROOT") or "").strip()
    if in_colab():
        if explicit:
            # Judge mode: use path even if it doesn't exist yet
            # (will be created by corpus download or §0 setup)
            return NotebookLayoutPaths(True, repo, Path(explicit).expanduser())
        candidates = _colab_drive_candidates(mount_point)
        for cand in candidates:
            if cand.is_dir():
                return NotebookLayoutPaths(True, repo, cand)
        # Demo-safe default: if Drive is unavailable or folder is missing, use local writable path.
        _DEFAULT_COLAB_PIPELINE_ROOT.mkdir(parents=True, exist_ok=True)
        return NotebookLayoutPaths(True, repo, _DEFAULT_COLAB_PIPELINE_ROOT)
    if explicit:
        return NotebookLayoutPaths(False, repo, Path(explicit).expanduser().resolve())
    # Local/WSL: prefer mounted Google Drive (same folder as Colab) when present.
    from scripts.utils.gdrive_paths import resolve_governance_pipeline_data_root

    pipeline_root = resolve_governance_pipeline_data_root()
    return NotebookLayoutPaths(False, repo, pipeline_root.resolve())


def maybe_mount_google_drive(mount_point: str = "/content/drive") -> None:
    """
    Call ``drive.mount`` only when explicitly enabled.

    Default is no Drive prompt (demo-safe). Enable only when you want personal Drive mode:

        ``GOVERNANCE_ENABLE_DRIVE_MOUNT=1``

    Skip mounting if read-only shared-folder judge mode is active via
    ``GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL`` / ``GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_ID``.
    """
    if not in_colab():
        return

    if os.environ.get("GOVERNANCE_ENABLE_DRIVE_MOUNT", "").strip().lower() not in (
        "1",
        "true",
        "yes",
    ):
        return

    if (os.getenv("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL") or "").strip() or (
        os.getenv("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_ID") or ""
    ).strip():
        return

    from google.colab import drive

    drive.mount(mount_point)
