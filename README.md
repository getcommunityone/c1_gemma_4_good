# CommunityOne — Gemma 4 for the Places the Internet Forgot

> **Local government runs on PDFs, audio recordings, and three-hour meetings nobody watches. We feed all of it to Gemma 4 and hand the results back to the community — for free, in plain English, on any laptop with an API key or any GPU with Hugging Face.**

**Hackathon track:** Digital Equity & Inclusivity
**Submission:** see [SUBMISSION.md](SUBMISSION.md)
**Rules compliance:** see [RULES_CHECKLIST.md](RULES_CHECKLIST.md)
**Architecture & Gemma 4 feature map:** see [ARCHITECTURE.md](ARCHITECTURE.md)
**Three-minute video storyboard:** see [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)

---

## The problem

Half of all U.S. counties are now [news deserts](https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/2024/report/) — communities with **zero or one local newspaper**. When the press disappears, so does the only watchdog on the city council, the planning board, and the fire-district budget hearing. The decisions still happen. The PDFs still go up. The meetings are still recorded. Nobody is reading or watching.

Civic-tech tools (Granicus, SeeClickFix, Documenters.org) exist for the largest cities. They skip the **18,000 small townships, counties, school boards, and special districts** where most American policy actually gets made.

That gap *is* the digital-equity gap.

## What CommunityOne does

Point CommunityOne at a folder of agendas, minutes PDFs, audio recordings, and contact photos for any jurisdiction. Gemma 4 returns:

| Output                                              | Who uses it                                                                 |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| **Plain-text OCR of scanned PDFs** (Demo 1)         | Residents who can't decipher 1990s photocopies of zoning amendments         |
| **Per-page token-budget routing** (Demo 2)          | Pipeline cost control — financial tables get 1,120 image tokens, body text gets 64 |
| **Policy deconstruction with visible reasoning** (Demo 3) | Journalists & researchers — *who steered each decision and why*       |
| **Audio chunking + policy-drift detection** (Demo 4) | Citizens — *what changed between the agenda and the actual vote*           |
| **Plain transcripts in any language** (Demo 4a)      | Non-English-speaking residents                                              |
| **Contact-photo enrichment** (Demo 5)                | Demographic representation audits                                           |
| **Cross-jurisdiction embedding clusters** (Demo 6)   | Researchers — *are Tuscaloosa and Big Timber passing the same ordinance?*  |
| **ShieldGemma safety review** (final step)           | Anyone — *did the LLM hallucinate or stereotype before we published?*       |

The pipeline runs against **two real reference jurisdictions** we've already ingested for the demo:

- **Tuscaloosa County, Alabama** — mid-size urban county
- **Big Timber & Sweet Grass County, Montana** — rural, population ~3,500

Pick any other jurisdiction and the same code runs. Geography is encoded in the folder layout (`<STATE>/<scope>/<jurisdiction>/`) so FIPS codes, county names, and postal codes fall out of the path.

## Why Gemma 4 specifically

Eight distinct Gemma 4 capabilities, orchestrated against the same corpus:

1. **Native multimodality** — PDFs and audio go in as bytes; no separate OCR, no separate ASR.
2. **Adjustable media-resolution token budget** — HIGH (~1,120 tokens) for ledgers, LOW (~64) for body text. Cost-routing the model itself exposes.
3. **Built-in thinking mode** — `include_thoughts=True` returns the chain-of-reasoning beside the answer; we publish both.
4. **Long-context with alternating local + global attention** — 15-minute audio chunks stitched with a drift-detector pass for hours-long meetings.
5. **Strict-JSON / response-schema function calling** — every output validates against a Pydantic-style schema in [`prompts/policy_analysis_v1.md`](prompts/policy_analysis_v1.md).
6. **Mixed-size deployment** — Gatekeeper triage runs on **E2B / E4B** (edge); deep analysis on **26B-A4B-IT** or **31B**; safety review on **ShieldGemma**; clustering on **EmbeddingGemma**.
7. **Open-weights local fallback** — `GOVERNANCE_LLM_BACKEND=huggingface` swaps every call from AI Studio to local HF weights. The same notebook runs end-to-end **offline** on a single L4 GPU.
8. **Hybrid cloud + edge routing** — small files take the cheap E2B route; PDFs ≥1.5 MB and audio over 15 minutes get the heavyweight 31B/26B route automatically.

Architecture and feature mapping: [ARCHITECTURE.md](ARCHITECTURE.md).

## Live demo (judges)

The fastest way to see Gemma 4 work end-to-end:

[**▶ Open `02_run_meeting_llm.ipynb` in Google Colab**](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb)

1. Add `GEMINI_API_KEY` to **Colab Secrets** (free key from [aistudio.google.com](https://aistudio.google.com)).
2. **Runtime → Run all** (CPU is fine for Phase 1; switch to L4 GPU for Phase 2 audio).
3. Pre-staged demo corpus auto-mounts from a public Drive folder.
4. Outputs land in `03_processed_outputs/02_gemma_json/AL/county/county_01125/…`.

Total time: **45–75 minutes** end-to-end on Colab free tier (`SCOPE = "fast"`).

A scripted, no-Colab entry point also exists — see [`demos/`](demos/).

## Repo layout

```
c1_gemma_4_good/
├── README.md                        ← you are here (judges first)
├── SUBMISSION.md                    ← Kaggle writeup (≤ 1,500 words)
├── RULES_CHECKLIST.md               ← every competition rule mapped to evidence
├── ARCHITECTURE.md                  ← system diagram + Gemma 4 feature map
├── VIDEO_SCRIPT.md                  ← 3-minute pitch storyboard
├── demos/                           ← single-command judge entrypoints
│   ├── README.md
│   └── quickstart.sh
├── prompts/
│   ├── policy_analysis_v1.md        ← deconstruction prompt + JSON schema
│   └── policy_analysis_sample_inputs.md
├── scripts/
│   ├── colab/                       ← the working pipeline (battle-tested)
│   │   ├── 02_run_meeting_llm.ipynb ← judges run this
│   │   ├── governance_meeting_llm.py    (Gemma client, walker, drift detector)
│   │   ├── gatekeeper_triage.py         (Demo 0 — Gemma decides what counts)
│   │   ├── gemma_hf_backend.py          (offline / HF fallback)
│   │   ├── colab_safety_review.py       (ShieldGemma final pass)
│   │   └── …                            (38 supporting modules)
│   ├── discovery/                   ← naming-convention discovery
│   └── utils/                       ← path resolution
└── tests/                           ← unit tests for bootstrap + UI
```

## Quick start (local WSL / Linux)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env  # fill in GEMINI_API_KEY (and HF_TOKEN for offline mode)
bash scripts/colab/mount_drive.sh
jupyter lab scripts/colab/02_run_meeting_llm.ipynb
```

Run cells §1 → §6. Outputs mirror to your Drive at `…/03_processed_outputs/02_gemma_json/`.

## Privacy stance

CommunityOne is built for communities where **privacy is non-negotiable** (Hackathon spec). Three guarantees:

1. **No login wall** for the demo or the code. Public Kaggle Notebook, public Colab, CC-BY-4.0.
2. **No identifying data leaves the local machine** in offline mode — the entire pipeline runs against `google/gemma-4-E2B` / `gemma-4-E4B` / `gemma-4-26b-a4b-it` weights via Hugging Face. Toggle: `GOVERNANCE_LLM_BACKEND=huggingface`.
3. **ShieldGemma reviews every LLM output** before it lands on disk. Demographic enrichment of contact photos (Demo 5) is **opt-in** and capped per jurisdiction; results are flagged as model-perceived, not factual.

## License

CC-BY-4.0 (per hackathon rules §2.5 — Winner License). See [LICENSE](LICENSE).

## Citation

```
Ian Ballantyne, Glenn Cameron, María Cruz, Olivier Lacombe, Kristen Quan, and
Omar Sanseviero. The Gemma 4 Good Hackathon.
https://kaggle.com/competitions/gemma-4-good-hackathon, 2026. Kaggle.
```

## Related

Full production platform (private): [open-navigator](https://github.com/getcommunityone/open-navigator). This repo is the hackathon-shaped, public, CC-BY-4.0 carve-out.
