# CommunityOne — Gemma 4 Good (hackathon demo)

Standalone repo for the **Gemma 4 Good** municipal meeting pipeline (Colab + local Jupyter).

Data lives on **Google Drive**, not in git:

`My Drive/CommunityOne/hackathons/2026_Gemma_4_Good/`

## Quick start (local WSL)

```bash
cd ~/projects/c1_gemma_4_good
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
bash scripts/colab/mount_drive.sh   # mount G: → /mnt/g
```

Copy `.env.example` → `.env` (or use the provided `.env`) and set:

- `GOVERNANCE_PIPELINE_DATA_ROOT=/mnt/g/My Drive/CommunityOne/hackathons/2026_Gemma_4_Good`

Open `scripts/colab/02_run_meeting_llm.ipynb` → kernel **`.venv`** → run **§1–§6**.

## Colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb)

## Layout

| Path | Purpose |
|------|---------|
| `scripts/colab/` | Notebooks + pipeline Python |
| `scripts/utils/gdrive_paths.py` | Drive / pipeline path resolution |
| `prompts/policy_analysis_v1.md` | Demo 3 policy JSON schema |

See `scripts/colab/README.md` for step-by-step sync and env vars.

## Related

Full platform code remains in [open-navigator](https://github.com/getcommunityone/open-navigator).
