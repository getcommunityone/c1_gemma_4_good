# Judges — start here

Two ways to evaluate CommunityOne in under 10 minutes. Pick either.

## 1. Web UX (no install, no API key)

**▶ <https://getcommunityone.github.io/c1_gemma_4_good/>**

Static React app. Search every U.S. local-government website, browse ACS census data, and read pre-generated Gemma-4 meeting summaries. Loads in your browser; nothing to run.

## 2. Reproducible Gemma 4 pipeline (~45–75 min on Colab)

[**▶ Open `run_in_colab.ipynb` in Google Colab**](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/run_in_colab.ipynb)

### Run order (one GPU — no CPU switch)

1. **Runtime → L4 GPU** (or T4), **High RAM** if offered — keep this for the whole notebook.
2. Colab **Secrets**: `GEMINI_API_KEY` and `HF_TOKEN` (notebook access **ON**).
3. Run **§0 → §1 → §2 → §3 → §4 → §5 → §6** (single §6 code cell — PDF + video).
4. Outputs: `03_processed_outputs/02_gemma_json/<STATE>/<scope>/<jurisdiction>/…` under `/content/governance_pipeline_local`.

**No Google Drive for Desktop** — §1 downloads the public demo corpus via `gdown`.

If the session restarts, re-run **§0 → §1 → §5 → §6** (do not change runtime type mid-run).

§0 sets (automatically on Colab):

```python
import os

os.environ["GOVERNANCE_PIPELINE_DATA_ROOT"] = "/content/governance_pipeline_local"
os.environ["GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL"] = "https://drive.google.com/drive/folders/1H_narmvkEUEalAyvl1P2oY7XbzaVMD7_?usp=sharing"
os.environ["GOVERNANCE_COLAB_SINGLE_RUNTIME"] = "1"
```

## What to read while it runs

| Document | What it answers |
| --- | --- |
| [README.md](README.md) | Project overview + the eight Gemma 4 capabilities exercised |
| [SUBMISSION.md](SUBMISSION.md) | The 1,460-word Kaggle writeup |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Data plane, control plane, Gemma 4 feature map |
| [RULES_CHECKLIST.md](RULES_CHECKLIST.md) | Every competition rule mapped to evidence |
| [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) | 3-minute pitch storyboard |
| [PITCH_DECK.md](PITCH_DECK.md) | Slide-form narrative |

## If something breaks

- **Colab badge 404s:** the notebook lives at [`scripts/colab/run_in_colab.ipynb`](scripts/colab/run_in_colab.ipynb).
- **No API key:** use the web UX (entry point #1) or add `GEMINI_API_KEY` / `HF_TOKEN` to Colab Secrets and re-run §4.
- **`ModuleNotFoundError` after restart:** re-run §0 → §1 (re-clones repo to `/content/c1_gemma_4_good`), then §5 → §6.
- **Offline / no Colab:** set `GOVERNANCE_LLM_BACKEND=huggingface` and run on a local L4 GPU.
