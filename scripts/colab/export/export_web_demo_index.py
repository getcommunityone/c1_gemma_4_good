#!/usr/bin/env python3
"""Export static JSON for the hackathon web UI (search + meetings explorer).

Run from repo root after §6 pipeline outputs exist on Drive or local hackathon root::

  python scripts/colab/export/export_web_demo_index.py

Writes:
  web/public/data/gemma-demo/index.json
  web/public/data/search-index.json (merged with existing demo rows)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_repo = Path(__file__).resolve().parents[3]
if str(_repo) not in sys.path:
    sys.path.insert(0, str(_repo))

from scripts.utils.gdrive_paths import resolve_governance_pipeline_data_root  # noqa: E402

WEB_DATA = _repo / "web" / "public" / "data"
GEMMA_INDEX = WEB_DATA / "gemma-demo" / "index.json"
SEARCH_INDEX = WEB_DATA / "search-index.json"


def main() -> int:
    root = resolve_governance_pipeline_data_root()
    summaries = root / "03_processed_outputs" / "03_human_summaries"
    gemma_json = root / "03_processed_outputs" / "02_gemma_json"
    meetings: list[dict] = []
    search_items: list[dict] = []

    if summaries.is_dir():
        for summary_md in summaries.rglob("_meeting_summary.md"):
            parts = summary_md.relative_to(summaries).parts
            if len(parts) < 4:
                continue
            state, scope, slug = parts[0], parts[1], parts[2]
            meeting_folder = parts[3] if len(parts) > 3 else ""
            rel_summary = summary_md.relative_to(_repo) if summary_md.is_relative_to(_repo) else None
            meetings.append(
                {
                    "jurisdiction_label": f"{slug} ({state}/{scope})",
                    "jurisdiction_root": f"{state}/{scope}/{slug}",
                    "meeting_date": meeting_folder.replace("_", "-")[:10] if meeting_folder else "",
                    "calendar_year": meeting_folder[:4] if len(meeting_folder) >= 4 else "",
                    "summary_path": f"/{rel_summary.as_posix()}" if rel_summary else None,
                    "policy_json_path": None,
                    "notes": None,
                }
            )
            search_items.append(
                {
                    "type": "meeting",
                    "title": f"{slug} — {meeting_folder}",
                    "subtitle": f"{state}/{scope}",
                    "description": "Gemma pipeline meeting summary",
                    "url": "/data-explorer/meetings",
                    "score": 1,
                    "metadata": {"state": state, "slug": slug},
                }
            )

    GEMMA_INDEX.parent.mkdir(parents=True, exist_ok=True)
    GEMMA_INDEX.write_text(
        json.dumps(
            {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "meetings": meetings},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {GEMMA_INDEX} ({len(meetings)} meetings)")

    # Preserve hand-authored demo rows if file exists
    existing: list[dict] = []
    if SEARCH_INDEX.is_file():
        try:
            existing = json.loads(SEARCH_INDEX.read_text(encoding="utf-8")).get("items", [])
        except json.JSONDecodeError:
            pass
    seen = { (i.get("title"), i.get("type")) for i in existing }
    merged = list(existing)
    for item in search_items:
        key = (item.get("title"), item.get("type"))
        if key not in seen:
            merged.append(item)
            seen.add(key)
    SEARCH_INDEX.write_text(
        json.dumps(
            {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "items": merged},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {SEARCH_INDEX} ({len(merged)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
