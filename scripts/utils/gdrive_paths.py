"""
Path helpers shared with ``scripts/utils/log_sync.py`` and ``export_bronze_to_json.py``.

- ``LOG_GDRIVE_MOUNT`` / ``gdrive_mount_path()`` — configured path (may not exist yet).
  ``resolved_gdrive_mount_path()`` — when the configured path is missing, may pick another
  ``/mnt/<letter>/My Drive`` or ``/mnt/c/Users/*/Google Drive/My Drive`` (Drive layout varies).
- ``resolve_scraped_meetings_output_root()`` — **meetings scraper** default is the repo cache
  (``data/cache/scraped_meetings``), same family as ``data/cache/wikidata``. Override with
  ``SCRAPED_MEETINGS_ROOT`` (e.g. a mounted Drive path) when you want artifacts outside the repo.
- ``scraped_meetings_gdrive_mirror_root()`` — default Drive mirror folder
  ``CommunityOne/hackathons/2026_Gemma_4_Good/01_raw_inputs`` under ``resolved_gdrive_mount_path()``
  (see ``scripts/colab/01_copy_scraped_meetings_cache_to_gdrive.py``). Override with
  ``SCRAPED_MEETINGS_GDRIVE_MIRROR`` (absolute path to the *mirror root* folder).
- ``GovernancePipelinePaths`` — same numbered folder layout as
  ``scripts/colab/02_init_drive_layout.ipynb`` (ingestion / reference data / processed).
  On **Google Colab**, set ``GOVERNANCE_PIPELINE_DATA_ROOT`` to e.g.
  ``/content/drive/MyDrive/CommunityOne/hackathons/2026_Gemma_4_Good`` before importing.
"""
from __future__ import annotations

import glob
import os
import re
import string
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_DEFAULT_LOG_GDRIVE_MOUNT = "/mnt/g/My Drive"

# ``scripts/utils/gdrive_paths.py`` → repo root is two parents up from ``scripts/``.
_REPO_ROOT = Path(__file__).resolve().parents[2]

_DRIVE_FOLDER_ID_RE = re.compile(r"/folders/([A-Za-z0-9_-]+)")


def _extract_drive_folder_id(raw: str) -> str:
    """Extract a Google Drive folder id from either a URL or plain id text."""
    value = (raw or "").strip()
    if not value:
        return ""
    if "drive.google.com" not in value:
        return value
    m = _DRIVE_FOLDER_ID_RE.search(value)
    if m:
        return m.group(1)
    try:
        parsed = urlparse(value)
    except ValueError:
        return ""
    q = parse_qs(parsed.query or "")
    for key in ("id", "folder"):
        vals = q.get(key)
        if vals and vals[0].strip():
            return vals[0].strip()
    return ""


def _resolve_drive_folder_id_path(folder_id: str) -> Path | None:
    """
    Resolve a Drive folder id to a local mounted path when available.

    On Colab, shared folders/shortcuts are typically exposed via
    ``/content/drive/.shortcut-targets-by-id/<id>``.
    """
    fid = (folder_id or "").strip()
    if not fid:
        return None
    candidates = (
        Path("/content/drive/.shortcut-targets-by-id") / fid,
        Path("/content/drive/MyDrive/.shortcut-targets-by-id") / fid,
        resolved_gdrive_mount_path() / ".shortcut-targets-by-id" / fid,
    )
    for cand in candidates:
        if cand.is_dir():
            return cand
    return None


def _try_gdrive_api_resolve(folder_id: str) -> Path | None:
    """
    Try to resolve a shared Drive folder via the Drive API (safe for public folders).

    In Colab, uses `google.colab.auth` and `googleapiclient` to list and sync files
    from a shared folder without requiring Google Drive for Desktop or broad permissions.

    Returns a local cache path under ``/tmp`` or Colab ``/content`` if successful,
    or None if the API is unavailable or the folder is not accessible.
    """
    fid = (folder_id or "").strip()
    if not fid:
        return None

    try:
        from google.colab import auth
        from googleapiclient.discovery import build
        import shutil
    except ImportError:
        return None

    try:
        auth.authenticate_user()
        drive_service = build("drive", "v3")
    except Exception:
        return None

    cache_root = Path("/tmp/colab_shared_drive_cache") if Path("/tmp").is_dir() else None
    if cache_root is None:
        try:
            cache_root = Path("/content/.shared_drive_cache")
        except Exception:
            return None

    cache_dir = cache_root / fid
    cache_dir.mkdir(parents=True, exist_ok=True)

    try:
        results = drive_service.files().list(
            q=f"'{fid}' in parents and trashed=false",
            spaces="drive",
            fields="files(id, name, mimeType, fileExtension, webViewLink)",
            pageSize=1000,
        ).execute()

        files = results.get("files", [])
        if not files:
            return None

        for file in files:
            mime = file.get("mimeType", "")
            name = file.get("name", "unknown")
            file_id = file.get("id")

            if (
                mime == "application/vnd.google-apps.folder"
                or not name.strip()
                or file_id is None
            ):
                continue

            dest = cache_dir / name
            if dest.exists():
                continue

            try:
                request = drive_service.files().get_media(fileId=file_id)
                with open(dest, "wb") as f:
                    f.write(request.execute())
            except Exception:
                pass

        return cache_dir if list(cache_dir.glob("*")) else None
    except Exception:
        return None


def gdrive_mount_path() -> Path:
    """Mounted Google Drive root (default ``/mnt/g/My Drive``)."""
    return Path(os.getenv("LOG_GDRIVE_MOUNT", _DEFAULT_LOG_GDRIVE_MOUNT)).expanduser()


def resolved_gdrive_mount_path() -> Path:
    """
    ``My Drive`` path for WSL when using Google Drive for Desktop.

    Returns ``gdrive_mount_path()`` when that path exists. Otherwise, if the user did **not**
    set ``LOG_GDRIVE_MOUNT`` to a **non-default** path, tries (in order): default ``/mnt/g/My Drive``,
    any ``/mnt/<letter>/My Drive``, then ``/mnt/c/Users/*/Google Drive/My Drive``. Scripts cannot
    mount Drive; this only discovers an already-mounted path.
    """
    configured = gdrive_mount_path()
    if configured.is_dir():
        return configured

    env_raw = (os.getenv("LOG_GDRIVE_MOUNT") or "").strip()
    default_norm = os.path.normpath(os.path.expanduser(_DEFAULT_LOG_GDRIVE_MOUNT))
    if env_raw and os.path.normpath(os.path.expanduser(env_raw)) != default_norm:
        return configured

    default = Path(_DEFAULT_LOG_GDRIVE_MOUNT)
    if default.is_dir():
        return default
    for letter in string.ascii_lowercase:
        candidate = Path(f"/mnt/{letter}/My Drive")
        if candidate.is_dir():
            return candidate
    for pattern in (
        "/mnt/c/Users/*/Google Drive/My Drive",
        "/mnt/d/Users/*/Google Drive/My Drive",
    ):
        for match in sorted(glob.glob(pattern)):
            found = Path(match)
            if found.is_dir():
                return found
    return configured


def default_scraped_meetings_data_cache() -> Path:
    """Default meetings artifact root: ``<repo>/data/cache/scraped_meetings`` (gitignored ``data/``)."""
    return _REPO_ROOT / "data" / "cache" / "scraped_meetings"


# 2026 Gemma hackathon Colab sync set (Tuscaloosa + Big Timber county/city). Used by
# ``scripts/colab/01_copy_scraped_meetings_cache_to_gdrive.py`` (default scope; pass ``--all-cache`` for full tree).
HACKATHON_SCRAPED_MEETINGS_INVENTORY_REL: tuple[str, ...] = (
    "AL/county/county_01125",
    "MT/county/county_30097",
    "AL/municipality/municipality_0177256",
    "MT/municipality/municipality_3006475",
)


def hackathon_scraped_meetings_inventory_dirs(
    src_root: Path | None = None,
) -> tuple[Path, ...]:
    """Absolute paths for each hackathon inventory folder under ``src_root`` (default: repo cache)."""
    root = (
        src_root.expanduser().resolve()
        if src_root is not None
        else resolve_scraped_meetings_output_root()
    )
    return tuple(root / rel for rel in HACKATHON_SCRAPED_MEETINGS_INVENTORY_REL)


# Hackathon pipeline root on Drive (``01_raw_inputs``, ``03_processed_outputs``, …).
HACKATHON_PIPELINE_ROOT_REL = Path("CommunityOne") / "hackathons" / "2026_Gemma_4_Good"

# Default mirror location under ``My Drive`` when ``SCRAPED_MEETINGS_GDRIVE_MIRROR`` is unset.
SCRAPED_MEETINGS_GDRIVE_REL = HACKATHON_PIPELINE_ROOT_REL / "01_raw_inputs"


def scraped_meetings_gdrive_mirror_root() -> Path:
    """
    Default Google Drive mirror for scraped meetings (under the mounted Drive root).

    Resolves to ``<resolved My Drive>/CommunityOne/hackathons/2026_Gemma_4_Good/01_raw_inputs``.

    Override with ``SCRAPED_MEETINGS_GDRIVE_MIRROR`` (absolute path to the *mirror root* folder).
    """
    explicit = (os.getenv("SCRAPED_MEETINGS_GDRIVE_MIRROR") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    return resolved_gdrive_mount_path() / SCRAPED_MEETINGS_GDRIVE_REL


def scraped_meetings_gdrive_rclone_remote_subpath() -> str:
    """Path under the rclone remote root (no ``remote:`` prefix), POSIX ``/`` separators."""
    return SCRAPED_MEETINGS_GDRIVE_REL.as_posix()


def scraped_meetings_root_resolution_note() -> str:
    """Which env branch :pyfunc:`resolve_scraped_meetings_output_root` used (for logs / manifests)."""
    explicit = (os.getenv("SCRAPED_MEETINGS_ROOT") or "").strip()
    if explicit:
        return "SCRAPED_MEETINGS_ROOT"
    return "DATA_CACHE (repo data/cache/scraped_meetings/)"


def resolve_scraped_meetings_output_root() -> Path:
    """
    Resolve where meeting PDFs should be stored.

    - If ``SCRAPED_MEETINGS_ROOT`` is set → that path (full override, e.g. Google Drive mount).
    - Else → ``<open-navigator>/data/cache/scraped_meetings`` (with ``{state}/{type}/{id}/…`` under it).
    """
    explicit = (os.getenv("SCRAPED_MEETINGS_ROOT") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    return default_scraped_meetings_data_cache()


def default_hackathon_pipeline_root_in_repo() -> Path:
    """Local Jupyter/WSL default: ``<repo>/data/hackathons/2026_Gemma_4_Good``."""
    return _REPO_ROOT / "data" / "hackathons" / "2026_Gemma_4_Good"


def resolve_governance_pipeline_data_root() -> Path:
    """
    Root folder for governance hackathon / Gemma pipeline data on Drive (or any disk).

    Resolution order:

    1. ``GOVERNANCE_PIPELINE_DATA_ROOT`` — absolute path (use this on **Colab**:
       ``/content/drive/MyDrive/CommunityOne/hackathons/2026_Gemma_4_Good``).
    2. ``resolved_gdrive_mount_path()`` / ``GOVERNANCE_PIPELINE_GDRIVE_BASE`` — default
       ``CommunityOne/hackathons/2026_Gemma_4_Good`` (WSL + Google Drive Desktop).
    3. Repo checkout: ``data/hackathons/2026_Gemma_4_Good`` when no Drive mount.
    """
    explicit = (os.getenv("GOVERNANCE_PIPELINE_DATA_ROOT") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    rel = os.getenv(
        "GOVERNANCE_PIPELINE_GDRIVE_BASE",
        HACKATHON_PIPELINE_ROOT_REL.as_posix(),
    ).strip()
    mounted = resolved_gdrive_mount_path() / rel
    if mounted.is_dir():
        return mounted
    return default_hackathon_pipeline_root_in_repo()


def raw_inputs_has_jurisdiction_layout(raw: Path) -> bool:
    """True when ``raw`` has ``AL/county/…`` or ``AL/municipality/…`` jurisdiction dirs."""
    root = raw.expanduser().resolve()
    state = root / "AL"
    if not state.is_dir():
        return False
    for scope in ("county", "municipality"):
        scope_dir = state / scope
        if scope_dir.is_dir() and any(p.is_dir() for p in scope_dir.iterdir()):
            return True
    return False


def raw_inputs_has_media_files(raw: Path) -> bool:
    """True when any PDF or meeting audio/video exists under ``raw``."""
    root = raw.expanduser().resolve()
    if not root.is_dir():
        return False
    for pat in ("**/*.pdf", "**/*.opus", "**/*.mp4", "**/*.mp3"):
        if any(root.glob(pat)):
            return True
    return False


def resolve_effective_raw_inputs_root(raw: Path) -> Path:
    """
    Return the directory that actually contains ``AL/<scope>/<jurisdiction>/…``.

    ``gdown`` often nests the hackathon tree (e.g.
    ``CommunityOne/hackathons/2026_Gemma_4_Good/01_raw_inputs/AL/…``) inside the
    download target ``01_raw_inputs``. Inventory walks only the effective root.
    """
    root = raw.expanduser().resolve()
    if not root.is_dir():
        return root
    if raw_inputs_has_jurisdiction_layout(root):
        return root
    for candidate in sorted({root, *root.rglob("01_raw_inputs")}):
        if candidate.is_dir() and raw_inputs_has_jurisdiction_layout(candidate):
            return candidate.resolve()
    for rel in (
        HACKATHON_PIPELINE_ROOT_REL / "01_raw_inputs",
        Path("2026_Gemma_4_Good") / "01_raw_inputs",
    ):
        candidate = root / rel
        if candidate.is_dir() and raw_inputs_has_jurisdiction_layout(candidate):
            return candidate.resolve()
    return root


def publish_governance_raw_inputs_root(
    raw_or_pipeline: Path | None = None,
) -> Path:
    """
    Resolve the walkable ``01_raw_inputs`` root and pin ``GOVERNANCE_RAW_INPUTS_ROOT``.

    Call after judge sync or when §5/§6 (re)builds inventory so nested gdown layouts
    (``…/01_raw_inputs/2026_Gemma_4_Good/01_raw_inputs/AL/…``) are not joined twice.
    """
    resolved = resolve_governance_raw_inputs_root(raw_or_pipeline)
    os.environ["GOVERNANCE_RAW_INPUTS_ROOT"] = str(resolved)
    return resolved


def diagnose_raw_inputs_layout(raw: Path) -> str:
    """Human-readable hint when §5 inventory finds zero jurisdictions."""
    root = raw.expanduser().resolve()
    lines = [f"Raw inputs layout diagnostic ({root}):"]
    if not root.is_dir():
        lines.append("  Directory missing — run §0 → §1 (judge sync).")
        return "\n".join(lines)
    top = sorted(p.name for p in root.iterdir() if p.is_dir())[:15]
    lines.append(f"  Top-level folders: {top or '(none)'}")
    effective = resolve_effective_raw_inputs_root(root)
    if effective != root and raw_inputs_has_jurisdiction_layout(effective):
        lines.append(f"  Corpus is nested — inventory should use: {effective}")
        lines.append(
            "  Set os.environ['GOVERNANCE_RAW_INPUTS_ROOT'] to that path, or re-run §1 "
            "with an updated notebook (auto-fix)."
        )
    elif not raw_inputs_has_jurisdiction_layout(root):
        lines.append(
            "  Expected layout: …/01_raw_inputs/AL/county/county_01125/… "
            "(not CommunityOne/… alone at the top level)."
        )
        if not raw_inputs_has_media_files(root):
            lines.append(
                "  No PDF/audio found anywhere under this tree. "
                "Try GOVERNANCE_JUDGE_FORCE_SYNC=1 and re-run §1."
            )
    return "\n".join(lines)


def resolve_governance_raw_inputs_root(pipeline_root: Path | None = None) -> Path:
    """
    Folder walked by Gatekeeper / §5 inventory (``AL/county/county_…`` layout).

    1. ``GOVERNANCE_RAW_INPUTS_ROOT`` if set (path or Google Drive folder URL)
    2. ``GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL`` / ``..._ID`` via
       ``.shortcut-targets-by-id/<id>`` when mounted
    3. ``<pipeline_root>/01_raw_inputs`` when it exists
    4. ``<repo>/data/cache/scraped_meetings`` only when ``GOVERNANCE_PIPELINE_DATA_ROOT`` is
       **not** set and ``GOVERNANCE_USE_SCRAPED_CACHE_FALLBACK=1`` (opt-in; full cache is huge).
    5. else ``<pipeline_root>/01_raw_inputs`` (caller may raise if missing)
    """
    def _finalize(path: Path) -> Path:
        return resolve_effective_raw_inputs_root(path.expanduser())

    explicit = (os.getenv("GOVERNANCE_RAW_INPUTS_ROOT") or "").strip()
    if explicit:
        folder_id = _extract_drive_folder_id(explicit)
        if folder_id and folder_id != explicit:
            resolved = _resolve_drive_folder_id_path(folder_id)
            if resolved is not None:
                return _finalize(resolved)
        return _finalize(Path(explicit))

    folder_hint = (
        (os.getenv("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL") or "").strip()
        or (os.getenv("GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_ID") or "").strip()
    )
    if folder_hint:
        folder_id = _extract_drive_folder_id(folder_hint)
        if folder_id:
            resolved = _resolve_drive_folder_id_path(folder_id)
            if resolved is not None:
                return _finalize(resolved)
            resolved = _try_gdrive_api_resolve(folder_id)
            if resolved is not None:
                return _finalize(resolved)
    root = Path(pipeline_root) if pipeline_root else resolve_governance_pipeline_data_root()
    raw = root / "01_raw_inputs"
    if raw.is_dir():
        return _finalize(raw)
    pipeline_explicit = (os.getenv("GOVERNANCE_PIPELINE_DATA_ROOT") or "").strip()
    allow_cache = os.environ.get("GOVERNANCE_USE_SCRAPED_CACHE_FALLBACK", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    if not pipeline_explicit and allow_cache:
        cache = default_scraped_meetings_data_cache()
        if cache.is_dir():
            return _finalize(cache)
    return _finalize(raw)


@dataclass(frozen=True)
class GovernancePipelinePaths:
    """Mirror ``scripts/colab/02_init_drive_layout.ipynb`` directory tree."""

    root: Path
    raw_inputs: Path
    meeting_data_by_jurisdiction_id: Path
    contacts_by_jurisdiction_id: Path
    transcripts: Path
    gemma_json: Path
    human_summaries: Path

    @classmethod
    def resolve(cls) -> GovernancePipelinePaths:
        root = resolve_governance_pipeline_data_root()
        reference = root / "02_reference_data"
        return cls(
            root=root,
            raw_inputs=root / "01_raw_inputs",
            meeting_data_by_jurisdiction_id=reference / "meeting_data_by_jurisdiction_id",
            contacts_by_jurisdiction_id=reference / "contacts_by_jurisdiction_id",
            transcripts=root / "03_processed_outputs" / "01_transcripts",
            gemma_json=root / "03_processed_outputs" / "02_gemma_json",
            human_summaries=root / "03_processed_outputs" / "03_human_summaries",
        )

    def ensure_dirs(self) -> None:
        """Create all pipeline stage directories (idempotent)."""
        for p in (
            self.raw_inputs,
            self.meeting_data_by_jurisdiction_id,
            self.contacts_by_jurisdiction_id,
            self.transcripts,
            self.gemma_json,
            self.human_summaries,
        ):
            p.mkdir(parents=True, exist_ok=True)
