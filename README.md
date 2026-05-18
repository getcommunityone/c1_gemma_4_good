# CommunityOne — Defying Gravity for Local Democracy

> *"You and I — defying gravity."*

**Track:** Digital Equity & Inclusivity
**Submission:** [SUBMISSION.md](SUBMISSION.md) · [Pitch deck](PITCH_DECK.md) · [3-min video](VIDEO_SCRIPT.md)
**Reference:** [Architecture](ARCHITECTURE.md) · [Rules compliance](RULES_CHECKLIST.md)
**Live demos:** [Colab notebook](#b-reproducible-pipeline) · [Web UI](https://getcommunityone.github.io/c1_gemma_4_good/)

---

## The Pitch

When I asked Google for a list of every city, county, and school-district website in my state, the answer was **"technically impossible."** The federal government charges **$500,000+** for "public" health data. Nonprofit aggregators paywall basic registries behind thousand-dollar subscriptions. Where data does exist, it's buried in expert jargon — *frame analysis*, *fiscal incidence* — a moat designed to keep the 99% out of the conversation.

**CommunityOne is now the only place where you can find a free, complete list of local-government websites for every state in the nation** — and the only truly free public platform that fuses meeting minutes, donor dollars, and legislation to measure what's actually working in local democracy.

Built on **Gemma 4**, it speaks Southern *"fixin' to"* and Northern *"about to."* It reads a 1990s photocopied zoning amendment and a scholar's frame analysis with equal fluency, then maps both into one view anyone can understand. No PhD required. No toll.

Size shouldn't dictate importance. Information shouldn't be a luxury good. **CommunityOne is the equalizer.**

---

## What It Does

Point CommunityOne at a folder of agendas, minutes PDFs, audio recordings, and contact photos for any jurisdiction. **Gemma 4 returns:**

| Output | Who it serves |
|---|---|
| Plain-text OCR of scanned PDFs *(Demo 1)* | Residents decoding 1990s photocopies of zoning amendments |
| Per-page token-budget routing *(Demo 2)* | Cost control — tables get 1,120 image tokens, body text gets 64 |
| Policy deconstruction with visible reasoning *(Demo 3)* | Journalists & researchers — who steered each decision, and why |
| Audio chunking + policy-drift detection *(Demo 4)* | Citizens — what changed between the agenda and the actual vote |
| Plain transcripts in any language *(Demo 4a)* | Non-English-speaking residents |
| Contact-photo enrichment *(Demo 5)* | Representation audits |
| Cross-jurisdiction embedding clusters *(Demo 6)* | Researchers — is Tuscaloosa passing the same ordinance as Big Timber? |
| ShieldGemma safety review *(final step)* | Every output checked for hallucination & stereotyping before publication |

The pipeline runs against two real reference jurisdictions already ingested:

- **Tuscaloosa County, Alabama** — mid-size urban county
- **Big Timber & Sweet Grass County, Montana** — rural, population ~3,500

Geography is encoded in the folder layout (`<STATE>/<scope>/<jurisdiction>/`), so FIPS codes, county names, and postal codes fall out of the path. Point at any other jurisdiction and the same code runs.

---

## Why Gemma 4 — Eight Capabilities, One Corpus

1. **Native multimodality** — PDFs and audio go in as bytes. No separate OCR. No separate ASR.
2. **Adjustable media-resolution token budget** — HIGH (~1,120 tokens) for ledgers, LOW (~64) for body text. The model itself exposes cost-routing.
3. **Built-in thinking mode** — `include_thoughts=True` returns chain-of-reasoning beside the answer. We publish both, so residents can audit the logic.
4. **Long-context with alternating local + global attention** — 15-minute audio chunks stitched with a drift-detector pass for hours-long meetings.
5. **Strict-JSON / response-schema function calling** — every output validates against the Pydantic-style schema in `prompts/policy_analysis_v1.md`. No prose-parsing fragility.
6. **Mixed-size deployment** — Gatekeeper triage on **E2B/E4B** (edge); deep analysis on **26B-A4B-IT** or **31B**; safety on **ShieldGemma**; clustering on **EmbeddingGemma**.
7. **Open-weights local fallback** — `GOVERNANCE_LLM_BACKEND=huggingface` swaps every AI Studio call for local HF weights. The same notebook runs end-to-end **offline** on a single L4 GPU.
8. **Hybrid cloud + edge routing** — small files take the cheap E2B route; PDFs ≥1.5 MB and audio >15 min auto-escalate to 31B/26B.

Full feature mapping: [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Live Demos for Judges

Two entry points — pick whichever fits the next 5 minutes.

### A) Web UI — the equalizer in your browser
Static React app, **no API key needed**: search + ACS data explorer + Gemma meetings tab.

- **Live:** https://getcommunityone.github.io/c1_gemma_4_good/
- **Local:** `npm run install:web && npm run dev`
- After pipeline §6: `python scripts/export_web_demo_index.py` refreshes meeting/search JSON.

### B) Reproducible pipeline — prove the technology is real

1. Open [`02_run_meeting_llm.ipynb`](scripts/colab/02_run_meeting_llm.ipynb) in Google Colab.
2. Add `GEMINI_API_KEY` to Colab Secrets ([free key](https://aistudio.google.com)).
3. **Runtime → Run all.** CPU is fine for Phase 1; switch to L4 GPU for Phase 2 audio.
4. Pre-staged demo corpus auto-mounts from a public Drive folder.
5. Outputs land in `03_processed_outputs/02_gemma_json/AL/county/county_01125/…`.

**Total time: 45–75 minutes end-to-end on Colab free tier** (`SCOPE = "fast"`). A scripted, no-Colab entry point also exists — see [`demos/`](demos/).

---

## Quick Start (local WSL / Linux)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # fill in GEMINI_API_KEY (and HF_TOKEN for offline mode)
bash scripts/colab/mount_drive.sh
jupyter lab scripts/colab/02_run_meeting_llm.ipynb
```

Run cells §1 → §6. Outputs mirror to Drive at `…/03_processed_outputs/02_gemma_json/`.

---

## Privacy Stance

Built for communities where privacy is non-negotiable. Three guarantees:

1. **No login wall** for the demo or code. Public Kaggle Notebook, public Colab, CC-BY-4.0.
2. **No identifying data leaves the local machine in offline mode.** The entire pipeline runs against `google/gemma-4-E2B` / `E4B` / `26b-a4b-it` weights via Hugging Face. Toggle: `GOVERNANCE_LLM_BACKEND=huggingface`.
3. **ShieldGemma reviews every LLM output** before it lands on disk. Demographic enrichment (Demo 5) is opt-in, capped per jurisdiction, and labeled *model-perceived, not factual*.

---

## Repo Layout (essentials)

```
c1_gemma_4_good/
├── README.md                                ← you are here
├── SUBMISSION.md                            ← Kaggle writeup (≤ 1,500 words)
├── ARCHITECTURE.md                          ← system diagram + Gemma 4 feature map
├── RULES_CHECKLIST.md                       ← every rule mapped to evidence
├── VIDEO_SCRIPT.md                          ← 3-minute pitch storyboard
├── demos/quickstart.sh                      ← single-command judge entry point
├── prompts/policy_analysis_v1.md            ← deconstruction prompt + JSON schema
├── web/                                     ← static React UI (GitHub Pages)
├── scripts/colab/02_run_meeting_llm.ipynb   ← judges run this
├── scripts/colab/                           ← 38 supporting modules (Gemma client,
│                                              gatekeeper, HF backend, ShieldGemma)
└── tests/                                   ← bootstrap + UI tests
```

---

## License & Citation

**License:** [CC-BY-4.0](LICENSE) — per hackathon rules §2.5 (Winner License).

**Citation:** Ian Ballantyne, Glenn Cameron, María Cruz, Olivier Lacombe, Kristen Quan, and Omar Sanseviero. *The Gemma 4 Good Hackathon.* https://kaggle.com/competitions/gemma-4-good-hackathon, 2026. Kaggle.

**Related:** Full production platform (private): `open-navigator`. This repo is the hackathon-shaped, public, CC-BY-4.0 carve-out.

---

## Closing — Defying Gravity

My wife Renee's favorite song is *Defying Gravity*. In it, Elphaba says she's *"through with playing by the rules of someone else's game."*

So am I.

Our kids are on track for a worse financial future than we had — not because the data isn't there, but because it's locked away from the people who need it most. Without facts, we govern on emotion. Without a shared language, we can't even disagree productively.

CommunityOne replaces emotion with evidence. It maps a better path. And it does it for free, for every jurisdiction, in every language people actually speak.

**You and I — defying gravity.**