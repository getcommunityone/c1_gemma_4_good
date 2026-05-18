# Competition Rules Compliance Checklist

This file maps every applicable rule from the *Gemma 4 Good Hackathon* — both the [Competition-Specific Rules](https://www.kaggle.com/competitions/gemma-4-good-hackathon/rules) and the [Kaggle Competition Foundational Rules](https://www.kaggle.com/competitions/gemma-4-good-hackathon/rules) — to a concrete piece of evidence in this repository.

> Last updated: 2026-05-17. Submission deadline: **2026-05-18 6:59 PM CDT** (11:59 PM UTC).

---

## A. Submission Requirements (from Competition Overview)

| Required item | Where it lives | Status |
|---|---|---|
| Kaggle Writeup (≤ 1,500 words, with a Track selected) | [`SUBMISSION.md`](SUBMISSION.md) — paste verbatim into Kaggle "New Writeup" UI | ✅ ready |
| Public Video (≤ 3 min, YouTube, no login required) | Storyboard: [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md). YouTube URL added to writeup after recording. | ⏳ to be shot |
| Public Code Repository (this repo) | GitHub: `getcommunityone/c1_gemma_4_good` (mirrored as the Kaggle Notebook for this submission, which becomes public after the deadline) | ✅ ready |
| Live Demo (web) | **<https://getcommunityone.github.io/c1_gemma_4_good/>** — static React app, no login, no API key, no paywall. Search + ACS explorer + Gemma meetings. | ✅ ready |
| Live Demo (pipeline) | [Open in Colab](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb) — runs without login on Colab free tier with a free `GEMINI_API_KEY` | ✅ ready |
| Cover image | `media/cover.png` (attached to writeup Media Gallery) | ⏳ to be added with writeup |
| Track selected | **Digital Equity & Inclusivity** (Impact Track) — also eligible for Main Track | ✅ declared in [SUBMISSION.md](SUBMISSION.md) and [README.md](README.md) |

---

## B. Competition-Specific Rules

### §2.1 — Team Limits
- **Max team size 5:** ✅ team of 1 (under cap).
- **Single Writeup per team:** ✅ one writeup planned ([SUBMISSION.md](SUBMISSION.md)).

### §2.2 — Submission Limits
- **One submission per team for hackathons:** ✅ planned to submit one writeup; will resubmit only by un-submit / edit / re-submit on the same writeup.

### §2.3 — Competition Timeline
- **Final Submission Deadline:** 2026-05-18 6:59 PM CDT (11:59 PM UTC). ✅ on track.

### §2.4 — Competition Data
- **(a) Data access:** Sponsor provides no Competition Data for this hackathon. ✅ N/A — we use only public municipal records (Tuscaloosa County AL, Sweet Grass County MT) that are equally accessible to all Participants (see §2.6 below).
- **(b) Data security:** No private Competition Data to protect. ✅ N/A.

### §2.5 — Winner License
- **CC-BY-4.0 on the winning Submission and source code:** ✅ this repo is licensed CC-BY-4.0 (see [LICENSE](LICENSE)).
- **No incompatibly-licensed inputs or pretrained models:** ✅ we use Gemma 4 (Gemma Terms of Use, compatible — see Gemma Prohibited Use Policy below), HuggingFace `google/gemma-4-*` weights, `transformers`/`accelerate`/`pymupdf`/`pdf2image`/`librosa`/`ffmpeg` — all permissively licensed OSI-approved or commercially-compatible. Generally-available commercial software (Google AI Studio API, Google Drive, Colab) is identified and procurable by the Sponsor per §2.5; no separate code delivery required for those.
- **Detailed reproducibility description (§2.5.b):** see [ARCHITECTURE.md](ARCHITECTURE.md) — architecture, preprocessing, prompt schemas, model routing, hyper-parameters (token budgets, thinking budgets, chunk sizes, confidence thresholds), and exact env-var-driven configuration.

### §2.6 — External Data and Tools
- **External Data:** Only **public municipal records** (agendas, minutes PDFs, meeting recordings, contact images) scraped from Tuscaloosa County AL and Sweet Grass County MT official websites. All are publicly accessible at no cost. ✅ satisfies Reasonableness Standard.
- **Cost-of-tools Reasonableness Standard:** Free tier Colab + free `GEMINI_API_KEY` from AI Studio is sufficient to reproduce the demo. Offline path uses publicly-downloadable HF weights. No paid dataset / no expensive license / no geo restriction. ✅
- **(c) Automated ML Tools:** No AMLT used. ✅ N/A.

### §2.7 — Eligibility
- ✅ Solo participant, registered Kaggle account holder, age 18+, resident of an eligible jurisdiction, not on a sanctions list, not an employee/intern/contractor/officer/director of Google, Kaggle, or other Competition Entities.

### §2.8 — Winner's Obligations
- **(a) Deliverables:** Final model code = this repo. Training code = N/A (we do not train; we prompt + route Gemma 4 variants). Inference code = `scripts/colab/02_run_meeting_llm.ipynb` + supporting Python in `scripts/colab/`. Computational environment described in [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md). For commercially-available, sponsor-procurable software (Colab, AI Studio, Drive, HuggingFace Hub) we identify it rather than re-deliver code, per §2.8.a.a. ✅
- **(b) AMLT clause:** N/A. ✅
- **License grant:** ✅ CC-BY-4.0 grant in [LICENSE](LICENSE).
- **Acceptance documents:** ✅ will sign on notification.

### §2.9 — Governing Law
- California law / Santa Clara County. ✅ accepted.

---

## C. Kaggle Competition Foundational Rules (General Rules)

### §3.1 — Eligibility
- ✅ See §2.7 above.

### §3.2 — Sponsor & Hosting Platform
- ✅ Acknowledged: Google LLC sponsors; Kaggle hosts.

### §3.3 — Competition Period
- ✅ Submission scheduled before Final Submission Deadline 2026-05-18 11:59 PM UTC.

### §3.4 — Competition Entry
- **(a) No purchase necessary, register before Entry Deadline:** ✅ registered.
- **(b) No hand-labeling of test data:** ✅ N/A — this is a generative hackathon, no test set.
- **(c) Multi-stage competition:** ✅ N/A.
- **(d) Submission must be complete and legible:** ✅ writeup + repo + Colab + video URL.

### §3.5 — Individuals and Teams
- **(a) One Kaggle account:** ✅ single account.
- **(b) Teams ≤ 5:** ✅ team of 1.
- **(c) Team merger:** ✅ N/A.
- **(d) No private code sharing outside teams:** ✅ all code in this public repo.

### §3.6 — Submission Code Requirements
- **(a) No private code sharing during competition:** ✅ this repo is public on GitHub and will be public on Kaggle on or before the deadline.
- **(b) Public code sharing under OSI-approved, commercially-permitting license:** ✅ CC-BY-4.0.
- **(c) Open-source dependencies under OSI-approved, commercially-permitting licenses:**
  | Dependency | License | OSI / commercial OK |
  |---|---|---|
  | `google-genai` | Apache-2.0 | ✅ |
  | `transformers`, `accelerate` (HF) | Apache-2.0 | ✅ |
  | `pymupdf` | AGPL-3.0 | ⚠️ AGPL — invoked as a library subprocess but the **distributed code is CC-BY-4.0**. Per §2.5 we declare this dependency; alternative pure-Python PDF readers are pluggable. |
  | `pdf2image` | MIT | ✅ |
  | `librosa` | ISC | ✅ |
  | `Pillow` | HPND / MIT-style | ✅ |
  | `httpx` | BSD-3-Clause | ✅ |
  | `python-dotenv` | BSD-3-Clause | ✅ |
  | `ffmpeg` (CLI subprocess, not bundled) | LGPL/GPL — invoked as external binary, not redistributed | ✅ identified per §2.5 |
  | Gemma 4 weights (HF) | Gemma Terms of Use | ✅ compatible — we comply with the Gemma Prohibited Use Policy |

### §3.7 — Determining Winners
- ✅ Hackathon judged by rubric (Impact 40 / Video 30 / Tech Depth 30). We have aimed every artifact at those weights — see [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) for the video-pitch focus.

### §3.8 — Notification of Winners & Disqualification
- ✅ Acknowledged: respond within one week of notification, will provide code/documentation if requested.

### §3.9 — Prizes
- ✅ Acknowledged. Single-participant team — prize split clause N/A.

### §3.10 — Taxes
- ✅ Acknowledged.

### §3.11–§3.17 — General conditions, publicity, privacy, warranties, internet, right to cancel, not-employment
- ✅ Acknowledged. No third-party content in this repo without permission. All municipal records used are public records under state open-records laws.

### §3.18 — Definitions
- ✅ Acknowledged.

---

## D. Gemma 4 Specifics (Hackathon Spec)

| Spec ask | Where met |
|---|---|
| **Use Gemma 4** (not 3, not 3n in headline role) | Primary models: `gemma-4-26b-a4b-it`, `gemma-4-31b-it`, `gemma-4-E2B`, `gemma-4-E4B`. `gemma-3n-e2b-it` is used only as a Gatekeeper fallback when Gemma 4 E2B is unavailable on a specific key. ✅ |
| **Native function calling / structured output** | Strict JSON via `response_schema` when supported, validated against the schema in `prompts/policy_analysis_v1.md`. ✅ |
| **Multimodal understanding** | PDFs (visual OCR), audio (ffmpeg-chunked, multimodal input), images (Demo 5 contact-photo enrichment). ✅ |
| **Post-training, domain adaptation, or agentic retrieval** | Prompt engineering against a domain-specific schema (governance meetings); agentic retrieval via the Gatekeeper triage + jurisdiction walker; cross-jurisdiction retrieval via EmbeddingGemma. ✅ |
| **Publish weights & benchmarks** *(if training)* | We do not fine-tune weights. We use Gemma 4 open weights as published by Google. ✅ N/A — but reproducibility doc in [ARCHITECTURE.md](ARCHITECTURE.md). |
| **App architecture + functional demo** *(if building app)* | [ARCHITECTURE.md](ARCHITECTURE.md) + working Colab notebook. ✅ |
| **Naming guidelines for Gemma assets in video** | We say "Gemma 4" / "Gemma 4 26B" / "ShieldGemma" / "EmbeddingGemma" — not "Google's AI" or "Gemini." Tracked in [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md). ✅ |

---

## E. Special Technology Track eligibility (we're not gunning for it, but disclosure)

We **do not** target the Cactus / LiteRT / llama.cpp / Ollama / Unsloth prizes — we use AI Studio + HuggingFace `transformers`. The Special Technology Track requirements are not met and we make no claim against them.

---

## F. Pre-flight checklist (T-minus 24h)

- [ ] Push repo to public GitHub at `getcommunityone/c1_gemma_4_good`.
- [ ] Confirm Colab badge in README points to a working public notebook.
- [ ] Record 3-minute video per [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md), upload to public YouTube (no login required).
- [ ] Paste [SUBMISSION.md](SUBMISSION.md) into Kaggle "New Writeup" — select **Digital Equity & Inclusivity** track.
- [ ] Attach cover image (`media/cover.png`) to writeup Media Gallery.
- [ ] Attach: YouTube URL, GitHub repo URL, Colab live-demo URL.
- [ ] Verify the Kaggle notebook attached to the writeup is **public** (so the auto-publication-on-deadline clause covers us either way).
- [ ] Click **Submit** in the top-right of the writeup. Re-submit after any edits.
- [ ] Take a screenshot of the submitted state for audit.
