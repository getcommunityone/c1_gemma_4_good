# CommunityOne — Defying Gravity for Local Democracy

> *"You and I — defying gravity."*

**Hackathon track:** Digital Equity & Inclusivity
**Submission writeup:** [SUBMISSION.md](SUBMISSION.md) · **Pitch deck:** [PITCH_DECK.md](PITCH_DECK.md) · **3-min video:** [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)
**Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) · **Rules compliance:** [RULES_CHECKLIST.md](RULES_CHECKLIST.md)
**Live demos:** [Colab notebook](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/run_in_colab.ipynb) · [Web UI](https://getcommunityone.github.io/c1_gemma_4_good/) (GitHub Pages)
**Judges start here:** [JUDGES.md](JUDGES.md)

---

## Act 1 — The "Impossible" Reality

When I asked for a list of every city, county, and school-district website in my state, Google called it **"technically impossible."**

That reminded me of my wife Renee's favorite song, *Defying Gravity*. In that song, Elphaba says she is **"through with playing by the rules of someone else's game."**

"Impossible" didn't sit right with me.

**CommunityOne is now the only place where you can find a free, complete list of local-government websites for every state in the nation.** Size shouldn't dictate your importance. But without these facts, we are running our country on emotions. Our kids are currently on track for a worse financial future than we had. At CommunityOne, we believe in an AI revolution powerful enough to map a better path — one we have never tried before.

## Act 2 — The $500,000 "Public" Paywall

Information is a luxury good. The federal government charges fees **exceeding $500,000** for "public" health data. Nonprofit aggregators charge thousands a year just to *see* a registry.

When they do give you data, simple concepts — *who decided what and why* — are buried under expert jargon like *frame analysis*. It's a moat designed to keep the 99% of us without a PhD out of the conversation. **If you can't pay the toll or speak the jargon, you stay in the dark.**

## Act 3 — The Truly Free Equalizer

CommunityOne is the equalizer. Using **Gemma 4**, we've built a shared language.

We map the Southern *"fixin' to"* and the Northern *"about to."* We map the academic jargon and the small-town common sense. We map all of it **into one clear view we can all understand.**

We are the only truly free public platform that combines **meeting notes, donor dollars, and legislation** to measure what's actually working. We are breaking the technical *and* financial moats — replacing emotion with evidence.

We aren't just summarizing. **We are mapping a better path for the next generation.**

---

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

## Live demos (judges)

Two entry points — pick whichever fits the next 5 minutes:

### A) Web UX — *the equalizer in your browser*
Static React app (no API): **search** + **ACS data explorer** + **Gemma meetings** tab.

- **Live:** https://getcommunityone.github.io/c1_gemma_4_good/
- **Local:** `npm run install:web && npm run dev` (from repo root; UI lives in `web/`)
- **Deploy:** automatic on push to `main` ([GitHub Action](.github/workflows/deploy-github-pages.yml)); manual: `npm run deploy` ([web/README.md](web/README.md))
- After §6: `python scripts/colab/export/export_web_demo_index.py` refreshes meeting/search JSON

### B) Reproducible pipeline — *prove the technology is real*
[**▶ Open `run_in_colab.ipynb` in Google Colab**](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/run_in_colab.ipynb)

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
├── web/                             ← static React UI (GitHub Pages)
│   ├── public/data/                 ← census-map subset + search-index.json
│   └── src/                         ← Home, Search, Data explorer
├── scripts/
│   ├── colab/                       ← the working pipeline (battle-tested)
│   │   ├── run_in_colab.ipynb       ← judges run this
│   │   ├── export/                  ← pipeline outputs → web JSON
│   │   ├── utils/                   ← bootstrap, paths, WSL Drive mount
│   │   ├── governance_meeting_llm.py    (Gemma client, walker, drift detector)
│   │   ├── gatekeeper_triage.py         (Demo 0 — Gemma decides what counts)
│   │   ├── gemma_hf_backend.py          (offline / HF fallback)
│   │   ├── colab_safety_review.py       (ShieldGemma final pass)
│   │   ├── discovery/                   ← meeting PDF naming helpers
│   │   └── …                            (supporting modules)
│   └── utils/                       ← path resolution
└── tests/                           ← unit tests for bootstrap + UI
```

## Quick start (local WSL / Linux)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env  # fill in GEMINI_API_KEY (and HF_TOKEN for offline mode)
bash scripts/colab/utils/mount_drive.sh
jupyter lab scripts/colab/run_in_colab.ipynb
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
