"""
Inject every immediate subfolder of ``scripts/colab/`` onto :data:`sys.path`.

The hackathon pipeline is organized into thematic subfolders (``engine/``,
``triage/``, ``demos/``, …), but notebooks and modules import one another by
**bare name** (``from governance_meeting_llm import ...``). Rather than
rewriting every import, we keep bare-name imports working by ensuring each
thematic subfolder (and ``utils/``) is on ``sys.path``.

Called from :mod:`scripts.colab.utils.colab_bootstrap` during §1 bootstrap.
"""
from __future__ import annotations

import sys
from pathlib import Path


def colab_root(colab_dir: Path | str | None = None) -> Path:
    """Resolve ``scripts/colab`` (parent of this ``utils/`` package)."""
    if colab_dir is not None:
        return Path(colab_dir).resolve()
    here = Path(__file__).resolve().parent
    if here.name == "utils":
        return here.parent
    return here


def inject_subfolder_paths(colab_dir: Path | str | None = None) -> list[str]:
    """Add ``scripts/colab`` and each immediate subfolder to ``sys.path``.

    Returns paths newly inserted, for logging.
    """
    base = colab_root(colab_dir)
    if str(base) not in sys.path:
        sys.path.insert(0, str(base))
    inserted: list[str] = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if name.startswith(".") or name == "__pycache__":
            continue
        if name.startswith("__") and name.endswith("__"):
            continue
        entry = str(child)
        if entry not in sys.path:
            sys.path.insert(0, entry)
            inserted.append(entry)
    return inserted
