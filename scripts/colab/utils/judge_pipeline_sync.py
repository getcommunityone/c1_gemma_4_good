"""
Judge / public-demo path: copy a **shared** Google Drive folder to local disk.

Judges do not need Google Drive for Desktop or a personal Drive mount. Set
``GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL`` (§0) and a writable
``GOVERNANCE_PIPELINE_DATA_ROOT`` (default ``/content/governance_pipeline_local`` on Colab).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]

# Hackathon read-only corpus (Tuscaloosa + Big Timber) — see JUDGES.md
DEFAULT_JUDGE_PUBLIC_FOLDER_URL = (
    "https://drive.google.com/drive/folders/1H_narmvkEUEalAyvl1P2oY7XbzaVMD7_?usp=sharing"
)

DEFAULT_COLAB_PIPELINE_ROOT = Path("/content/governance_pipeline_local")


def judge_mode_enabled() -> bool:
    """True when inputs should come from a public/shared Drive folder, not My Drive."""
    return bool(
        (os.environ.get("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL") or "").strip()
        or (os.environ.get("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_ID") or "").strip()
        or os.environ.get("GOVERNANCE_JUDGE_MODE", "").strip().lower() in ("1", "true", "yes")
    )


def default_pipeline_root_for_judge() -> Path:
    raw = (os.environ.get("GOVERNANCE_PIPELINE_DATA_ROOT") or "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    try:
        from colab_paths import in_colab

        if in_colab():
            return DEFAULT_COLAB_PIPELINE_ROOT
    except ImportError:
        pass
    from scripts.utils.gdrive_paths import default_hackathon_pipeline_root_in_repo

    return default_hackathon_pipeline_root_in_repo().resolve()


def _folder_url() -> str:
    return (
        (os.environ.get("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL") or "").strip()
        or (os.environ.get("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_ID") or "").strip()
        or (
            DEFAULT_JUDGE_PUBLIC_FOLDER_URL
            if os.environ.get("GOVERNANCE_JUDGE_MODE", "").strip().lower()
            in ("1", "true", "yes")
            else ""
        )
    )


def _sync_stamp(dest: Path) -> Path:
    return dest / ".judge_public_sync_stamp"


def _corpus_looks_ready(dest: Path) -> bool:
    if not dest.is_dir():
        return False
    if not _sync_stamp(dest).is_file():
        return False
    from scripts.utils.gdrive_paths import (
        raw_inputs_has_media_files,
        resolve_effective_raw_inputs_root,
    )

    effective = resolve_effective_raw_inputs_root(dest)
    return raw_inputs_has_media_files(effective)


def _ensure_gdown() -> None:
    try:
        import gdown  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "gdown>=5.0"],
        )


def sync_public_folder_to_local(
    folder_url_or_id: str,
    dest: PathLike,
    *,
    force: bool = False,
) -> Path:
    """
    Download a **public** Drive folder tree into ``dest`` (creates parents).

    Uses ``gdown`` (no OAuth). Skips when ``.judge_public_sync_stamp`` exists unless
    ``force=True`` or ``GOVERNANCE_JUDGE_FORCE_SYNC=1``.
    """
    from scripts.utils.gdrive_paths import _extract_drive_folder_id

    dest_path = Path(dest).expanduser().resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    force = force or os.environ.get("GOVERNANCE_JUDGE_FORCE_SYNC", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    if not force and _corpus_looks_ready(dest_path):
        print(f"Judge corpus: reuse local copy at {dest_path}")
        return dest_path

    folder_id = _extract_drive_folder_id(folder_url_or_id)
    if not folder_id:
        raise ValueError(f"Could not parse Drive folder id from {folder_url_or_id!r}")

    print(f"Judge corpus: downloading public Drive folder → {dest_path}")
    print("  (first run may take several minutes; no personal Google Drive needed)")

    _ensure_gdown()
    import gdown

    print("Downloading folder with the following details:")
    print("  folder_url_or_id:", folder_url_or_id)
    print("  folder_id:", folder_id)

    url = (
        folder_url_or_id
        if "drive.google.com" in folder_url_or_id
        else f"https://drive.google.com/drive/folders/{folder_id}"
    )
    print("  Resolved URL:", url)  # Log the resolved URL

    try:
        downloaded_files = gdown.download_folder(url=url, output=str(dest_path), quiet=False, remaining_ok=True)
        print("Downloaded files:", downloaded_files)  # Log all downloaded files
    except TypeError:
        print("  Retrying with folder_id:", folder_id)
        downloaded_files = gdown.download_folder(id=folder_id, output=str(dest_path), quiet=False, remaining_ok=True)
        print("Downloaded files:", downloaded_files)  # Log all downloaded files

    _sync_stamp(dest_path).write_text(folder_id, encoding="utf-8")
    print(f"Judge corpus: sync complete ({dest_path})")
    return dest_path


def ensure_judge_pipeline_layout(pipeline_root: PathLike) -> Path:
    """Create writable hackathon layout under ``pipeline_root``."""
    root = Path(pipeline_root).expanduser().resolve()
    try:
        from scripts.utils.gdrive_paths import GovernancePipelinePaths

        paths = GovernancePipelinePaths(
            root=root,
            raw_inputs=root / "01_raw_inputs",
            meeting_data_by_jurisdiction_id=root / "02_reference_data" / "meeting_data_by_jurisdiction_id",
            contacts_by_jurisdiction_id=root / "02_reference_data" / "contacts_by_jurisdiction_id",
            transcripts=root / "03_processed_outputs" / "01_transcripts",
            gemma_json=root / "03_processed_outputs" / "02_gemma_json",
            human_summaries=root / "03_processed_outputs" / "03_human_summaries",
        )
        paths.ensure_dirs()
    except ImportError:
        for rel in (
            "01_raw_inputs",
            "02_reference_data/meeting_data_by_jurisdiction_id",
            "02_reference_data/contacts_by_jurisdiction_id",
            "03_processed_outputs/01_transcripts",
            "03_processed_outputs/02_gemma_json",
            "03_processed_outputs/03_human_summaries",
            "00_logs",
        ):
            (root / rel).mkdir(parents=True, exist_ok=True)
    (root / "00_logs").mkdir(parents=True, exist_ok=True)
    return root


def configure_judge_environment(
    *,
    folder_url: Optional[str] = None,
    pipeline_root: Optional[PathLike] = None,
) -> Path:
    """
    Set env vars for judge mode (§0 equivalent). Returns resolved pipeline root.
    """
    url = (folder_url or _folder_url() or DEFAULT_JUDGE_PUBLIC_FOLDER_URL).strip()
    root = Path(pipeline_root or default_pipeline_root_for_judge()).expanduser().resolve()

    os.environ["GOVERNANCE_JUDGE_MODE"] = "1"
    os.environ["GOVERNANCE_PIPELINE_DATA_ROOT"] = str(root)
    os.environ["GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL"] = url
    os.environ.setdefault(
        "GOVERNANCE_GATEKEEPER_LOG_DIR",
        str(root / "00_logs"),
    )
    os.environ.setdefault("GOVERNANCE_LOCAL_RAW_MIRROR", "0")
    return root


def prepare_judge_pipeline(
    pipeline_root: Optional[PathLike] = None,
    *,
    folder_url: Optional[str] = None,
    force_sync: bool = False,
) -> tuple[Path, Path]:
    """
    Layout + sync public Drive → ``<pipeline_root>/01_raw_inputs``.

    Returns ``(pipeline_root, raw_inputs_path)``.
    """
    root = configure_judge_environment(
        folder_url=folder_url,
        pipeline_root=pipeline_root,
    )
    ensure_judge_pipeline_layout(root)
    raw = root / "01_raw_inputs"
    url = _folder_url()
    if not url:
        raise RuntimeError(
            "Judge mode needs GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL or §0 SHARED_FOLDER_URL."
        )
    sync_public_folder_to_local(url, raw, force=force_sync)
    from scripts.utils.gdrive_paths import (
        diagnose_raw_inputs_layout,
        raw_inputs_has_jurisdiction_layout,
        raw_inputs_has_media_files,
        resolve_effective_raw_inputs_root,
    )

    effective = resolve_effective_raw_inputs_root(raw)
    if effective != raw.resolve():
        print(
            f"Judge corpus: nested Drive layout — inventory root is {effective}\n"
            f"  (download target was {raw})"
        )
    elif not raw_inputs_has_jurisdiction_layout(effective):
        print(diagnose_raw_inputs_layout(raw))
    elif not raw_inputs_has_media_files(effective):
        print(diagnose_raw_inputs_layout(raw))
    os.environ["GOVERNANCE_RAW_INPUTS_ROOT"] = str(effective)
    return root, effective
