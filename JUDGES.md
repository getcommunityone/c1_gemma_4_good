# Judges — start here

Two ways to evaluate CommunityOne in under 10 minutes. Pick either.

## 1. Web UX (no install, no API key)

**▶ <https://getcommunityone.github.io/c1_gemma_4_good/>**

Static React app. Search every U.S. local-government website, browse ACS census data, and read pre-generated Gemma-4 meeting summaries. Loads in your browser; nothing to run.

## 2. Reproducible Gemma 4 pipeline (5 min setup, ~45 min run)

[**▶ Open `run_in_colab.ipynb` in Google Colab**](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/run_in_colab.ipynb)

1. Add `GEMINI_API_KEY` to **Colab Secrets** (free key from <https://aistudio.google.com>).
2. **Runtime → Run all.** CPU is fine for Phase 1; switch to L4 GPU for Phase 2 audio.
3. Pre-staged demo corpus (Tuscaloosa County AL + Big Timber MT) auto-mounts from a public Drive folder.
4. Outputs land in `03_processed_outputs/02_gemma_json/<STATE>/<scope>/<jurisdiction>/…`.

If your input folder is read-only (shared-link mode), set these before running the pipeline cells:

```python
import os

os.environ["GOVERNANCE_PIPELINE_DATA_ROOT"] = "/content/governance_pipeline_local"
os.environ["GOVERNANCE_RAW_INPUTS_DRIVE_FOLDER_URL"] = "https://drive.google.com/drive/folders/1H_narmvkEUEalAyvl1P2oY7XbzaVMD7_?usp=sharing"
os.environ["GOVERNANCE_GATEKEEPER_LOG_DIR"] = "/content/governance_pipeline_local/00_logs"
```

**No Google Drive for Desktop needed.** The notebook automatically uses the Drive API in Colab (safe, no broad permissions).

Total time: **45–75 minutes** end-to-end on Colab free tier with `SCOPE = "fast"`.

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
- **No API key on hand:** the web UX (entry point #1) requires neither a key nor an install.
- **Offline / no Colab:** set `GOVERNANCE_LLM_BACKEND=huggingface` and the same notebook runs end-to-end on a local L4 GPU with no network egress.
