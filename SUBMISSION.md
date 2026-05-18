# CommunityOne: Defying Gravity for Local Democracy

**Track:** Digital Equity & Inclusivity
**Team:** CommunityOne / `getcommunityone`
**Word count:** ~1,460

> *"You and I — defying gravity."* Replacing emotion with evidence for the 18,000 small-town councils, school boards, fire districts, and county commissions that frontier AI has refused to serve — for free, in plain English, on any laptop, and when you want it, with **zero bytes leaving the building**.

---

## 1. The problem — three acts

### Act 1. The "Impossible" Reality

When I asked Google for a list of every city, county, and school-district website in my state, the answer was: **"technically impossible."**

That reminded me of my wife Renee's favorite song, *Defying Gravity*. In it Elphaba says she's **"through with playing by the rules of someone else's game."** "Impossible" didn't sit right.

**CommunityOne is now the only place where you can find a free, complete list of local-government websites for every state in the nation.** Size shouldn't dictate your importance. But without these facts, we are running our country on emotions. Our kids are on track for a worse financial future than we had. We believe in an AI revolution powerful enough to map a better path — one we've never tried before.

### Act 2. The $500,000 "Public" Paywall

Information is a luxury good today. The federal government charges fees **exceeding $500,000** for "public" health data. Nonprofit aggregators charge thousands of dollars a year just to *see* a registry.

When they do release the data, simple concepts — *who decided what and why* — are buried under expert jargon like *frame analysis*. It is a moat designed to keep the 99% of us without a PhD out of the conversation. **If you can't pay the toll or speak the jargon, you stay in the dark.**

### Act 3. The Truly Free Equalizer

CommunityOne is the equalizer. Using **Gemma 4**, we built a shared language. We map the Southern *"fixin' to"* and the Northern *"about to."* We map academic jargon and small-town common sense. **All of it into one clear view we can all understand.**

We are the only truly free public platform that combines **meeting notes, donor dollars, and legislation** to measure what's actually working. Replacing emotion with evidence. We are not summarizing — we are mapping a better path for the next generation.

## 2. The solution

CommunityOne points Gemma 4 at the **whole pile** — agendas, minutes, audio, video, and contact photos — and returns structured, citable, audit-ready JSON the community can use:

- A **journalist** in Sweet Grass County, MT can search the last 18 months of council meetings by topic in five seconds.
- A **resident** in Tuscaloosa County, AL can ask "did anything change about my zoning between the agenda and the vote?" and get a Mermaid diagram of policy drift.
- A **non-English speaker** anywhere can get the full meeting transcript in their language.
- A **researcher** can cluster ordinances across jurisdictions to see who is copying whom.
- An **anti-bias auditor** can review every LLM output through ShieldGemma before publication.

The same pipeline runs end-to-end on **Colab free tier** in 45–75 minutes, or **fully offline** on an L4 GPU with no API key, with **zero code changes** — just `GOVERNANCE_LLM_BACKEND=huggingface`.

## 3. Why Gemma 4 (not a general LLM)

Eight Gemma 4 capabilities, each chosen because no general-purpose API replicates it:

1. **Native multimodality / "dark data."** ~30% of our reference PDFs are scanned photocopies with no text layer. PyMuPDF returns empty. Gemma 4 takes the file as `application/pdf` bytes and returns visually-grounded OCR (`extract_pdf_digital_text`, Demo 1).
2. **Adjustable per-page token budget.** A 60-page minutes PDF has four budget-table pages that need every token and 56 pages of *"Councilmember Jones moved to approve."* Gemma 4's `media_resolution` lets us route per page: HIGH (~1,120 tokens) for `financial_or_tabular`/`scanned`, LOW (~64) for `text_heavy` (`classify_pdf_page_heuristic`, Demo 2).
3. **Thinking mode, published.** `include_thoughts=True` returns the reasoning stream; Demo 3 writes `.thinking.thoughts.md` next to every JSON. Audit trail by default.
4. **Long-context with sliding-window + global attention.** Planning hearings run 2h45m. We chunk to 15-minute slices, run the prompt per chunk, then a drift-detector pass renders agenda-vs-vote divergence as a Mermaid timeline (`policy_drift_summarize`, Demo 4).
5. **Strict JSON / `response_schema`.** Every output validates against `prompts/policy_analysis_v1.md`. Clustering, embedding, and safety-review steps never defensively parse.
6. **Five-tier mixed-size deployment.** `gemma-4-E2B`/`E4B` for Gatekeeper, `gemma-4-26b-a4b-it` for PDF demos, `gemma-4-31b-it` for audio, `EmbeddingGemma` for clustering, `ShieldGemma` for review.
7. **Local-first, offline-capable.** `GOVERNANCE_LLM_BACKEND=huggingface` swaps every call to local HF weights. No telemetry, no API key. Ships to a courthouse on a satellite connection.
8. **ShieldGemma post-hoc review.** Every artifact passes `run_safety_review()` before it counts as done — a separate Gemma 4 model voting on the previous model's output. That is what grounded, explainable AI looks like.

## 4. Architecture — at a glance

```
┌──────────────────────────────────────────────────────────────────────┐
│  01_raw_inputs/  (Drive | local — same path, two surfaces)            │
│    AL/county/county_01125/2026/2026_02_18/{agenda,minutes,audio}/     │
│    MT/county/county_30097/2026/…                                      │
└─────────────────────────┬────────────────────────────────────────────┘
                          │  os.walk → MeetingInventory(jurisdiction_id)
                          ▼
            ┌──────────────────────────────────────┐
            │ Step 0 — Gatekeeper (E2B/E4B)        │  Demo 0
            │ "Is this a governance meeting?"      │
            └─────────────┬────────────────────────┘
                          ▼  KEEP verdicts
       ┌──────────────────┼──────────────────┬──────────────────┐
       ▼                  ▼                  ▼                  ▼
  Demo 1 OCR        Demo 2 token-budget   Demo 3 thinking   Demo 4 audio
  (multimodality)   (cost routing)        (.thoughts.md)    chunks + drift
       │                  │                  │                  │
       └─────────┬────────┴────────┬─────────┴──────┬──────────┘
                 ▼                 ▼                ▼
           Demo 5 photos      Demo 6 EmbeddingGemma   policy_drift.mmd
                 │             cross-jurisdiction
                 └────────────────────┬──────────────┘
                                      ▼
                             ShieldGemma (final pass)
                                      ▼
                03_processed_outputs/02_gemma_json/…  (CC-BY-4.0)
```

Detailed map: [ARCHITECTURE.md](ARCHITECTURE.md).

## 5. Technical depth — what we built, not what we sketched

- **39 Python modules / 16,000 lines** of production-grade pipeline code. None of it is mocked; the notebook runs end-to-end against a real corpus.
- **Bootstrap that works on Colab and local Jupyter from the same notebook** — `colab_paths.py` detects the runtime, mounts Drive only on Colab, resolves the repo root by walking parents.
- **Hybrid cloud + edge routing** — Gatekeeper defaults to AI Studio's `gemma-3n-e2b-it` (cheap, fast) but falls back to local HF weights when `HF_TOKEN` is set and `GOVERNANCE_GATEKEEPER_FORCE_HF=1`.
- **Wall-clock timeouts on every API call** — `genai_quota_retry.call_with_wall_clock_timeout`. A single hung socket cannot abort a 200-PDF batch.
- **Strict idempotency** — `demo2_pdf_outputs_complete`, `demo3_thinking_json_complete`, `demo4_drift_output_complete` skip already-processed files so a re-run after a Colab disconnect resumes mid-pipeline.
- **Two-phase runtime** — Phase 1 (CPU, ~30 min) processes PDFs; Phase 2 (L4 GPU, ~30 min) processes audio. Colab gives one runtime at a time, so we split.
- **`ffmpeg`-driven audio normalization** — every audio source (mp4, webm, mov, m4a, opus) is transcoded to Opus before chunking, so the model sees the same MIME shape regardless of upstream.
- **Tests** — `tests/test_colab_bootstrap.py`, `test_colab_notebook_ui.py`, `test_colab_runtime_phases.py`.

## 6. Real-world impact (what changes Monday morning)

| Persona                                  | Before CommunityOne                                  | After CommunityOne                                                      |
| ---------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Resident in a news desert                | "I don't know what they did"                         | One-page Markdown brief in 4 minutes per meeting                        |
| Reporter at a five-person paper          | Manually scrubs 3-hour videos                        | `policy_drift.mmd` shows the agenda vs. vote divergence visually        |
| Bilingual resident                       | English-only minutes                                 | `transcript.en.txt`, `transcript.es.txt`, `transcript.zh.txt` per audio |
| County clerk                             | Records vanish in scanner output                     | Visual-OCR JSON + flagged `dark_data` re-scans                          |
| State auditor                            | Spot-checks individual PDFs                          | EmbeddingGemma clusters identical ordinance language across counties     |

## 7. Limits & honesty

- Demographic enrichment of contact photos (Demo 5) is **model-perceived**, capped per jurisdiction, opt-in, and explicitly flagged as such in every JSON output. It is included so an auditor can run an underrepresentation analysis — not so anyone can profile a person.
- Policy-drift detection is a **lead generator**, not a verdict. Every flag points back to a timestamp in the audio for a human to verify.
- Offline mode requires ~24 GB GPU VRAM for the 26B-A4B path. The pipeline degrades to E2B-only for under-resourced sites.

## 8. Repository, license, deliverables

- **Public code repo:** the repo containing this writeup (CC-BY-4.0).
- **Live demo — Web UX (React, static, no API):** **<https://getcommunityone.github.io/c1_gemma_4_good/>** — no login, no paywall. Search + ACS data explorer + Gemma meetings tab. This is the equalizer in a browser.
- **Live demo — reproducible pipeline:** [Colab link](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb) — runs in 45–75 min with a free `GEMINI_API_KEY`. Proves the technology behind the web UX is real, working, and runs offline.
- **Video (3 min):** see Media Gallery on the Kaggle writeup; storyboard in [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md).
- **Rules compliance:** [RULES_CHECKLIST.md](RULES_CHECKLIST.md) maps every General + Competition-Specific rule to a piece of evidence in this repo.

**License:** CC-BY-4.0 (see [LICENSE](LICENSE)), satisfying §2.5 of the Competition-Specific Rules.

---

*Local democracy is the part of America that is most ignored by frontier AI and most damaged by its absence. CommunityOne is our attempt to close that gap with the only open-weights model family powerful enough to do it.*
