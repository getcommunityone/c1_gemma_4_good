# CommunityOne Architecture

How an `01_raw_inputs/` folder of municipal records becomes `03_processed_outputs/02_gemma_json/` — and the eight Gemma 4 features that make each hop possible.

---

## 1. Data plane

```
            G-Drive  ⇆  WSL mount  ⇆  Colab Drive mount
                              │
                              ▼   (same path on every surface)
       …/CommunityOne/hackathons/2026_Gemma_4_Good/
         ├── 01_raw_inputs/<STATE>/<scope>/<jurisdiction>/<year>/<YYYY_MM_DD>/
         │       ├── agenda/    *.pdf
         │       ├── minutes/   *.pdf
         │       ├── audio/     *.mp4 *.mp3 *.opus *.webm
         │       └── _contact_images/  *.jpg *.png
         ├── 02_reference_data/orbis_files/orbis_lookup_by_jurisdiction_id.json
         └── 03_processed_outputs/
                 ├── 00_logs/triage_report_<UTC>.json
                 ├── 02_gemma_json/<mirrored path>/…
                 │       ├── <pdf>.visual_ocr.txt          (Demo 1)
                 │       ├── <pdf>/<page>.json             (Demo 2)
                 │       ├── <pdf>/_token_budget_report.json
                 │       ├── <pdf>.thinking.json           (Demo 3)
                 │       ├── <pdf>.thinking.thoughts.md
                 │       ├── <audio>/chunk_<n>.json        (Demo 4)
                 │       ├── <audio>/policy_drift.json
                 │       ├── <audio>/policy_drift.mmd
                 │       ├── <audio>/transcript.<lang>.txt (Demo 4a)
                 │       └── <image>.contact.json          (Demo 5)
                 ├── 04_embeddings/cross_jurisdiction_clusters.json   (Demo 6)
                 └── 05_safety_review/<artifact>.shield.json          (final)
```

Path resolution lives in `scripts/colab/colab_paths.py` (`maybe_mount_google_drive`, `setup_notebook_paths`) and `scripts/utils/gdrive_paths.py` (`GovernancePipelinePaths`). Folder layout is created idempotently by `01_init_drive_layout.ipynb` or `scripts/utils/ensure_governance_pipeline_drive_layout.py`.

---

## 2. Control plane

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  02_run_meeting_llm.ipynb                                                    │
│   §1 Bootstrap → §2 SCOPE → §3 install → §4 keys → §5 inventory              │
│                                                                              │
│   §6 Phase 1 (CPU) ─── run_governance_pipeline() in colab_runtime_phases.py  │
│   §6 Phase 2 (GPU) ─── audio + drift via Hugging Face gemma-4 weights        │
└──────────────┬──────────────────────────────────────────────────────────────┘
               │ orchestrates ↓
               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│   gatekeeper_triage.run_triage()         ← Demo 0 — does this file count?    │
│   colab_demos.run_demo1 / run_demo2 / run_demo3 / run_demo4 / run_demo5      │
│   theme_audit / meeting_consolidated_summary / meeting_grouping              │
│   colab_safety_review.run_safety_review() ← ShieldGemma final pass           │
└──────────────────────────────────────────────────────────────────────────────┘
```

The notebook is a thin orchestrator. All logic lives in `scripts/colab/*.py` so the same code runs from the CLI (`python scripts/colab/gatekeeper_triage.py …`) or from a different driver.

---

## 3. The Gemma 4 feature map

| # | Gemma 4 capability                            | Where in code                                                                                | Where in output                                                  |
|---|-----------------------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| 1 | Native multimodality (PDF as bytes)           | `governance_meeting_llm.call_google_genai_multimodal`                                        | `*.visual_ocr.txt` (Demo 1)                                       |
| 2 | Adjustable media-resolution token budget      | `classify_pdf_page_heuristic`, `TOKEN_BUDGET_HIGH/MEDIUM/LOW`                                | `*/<page>.json`, `*/_token_budget_report.json` (Demo 2)           |
| 3 | Built-in thinking mode                        | `model_supports_thinking`, `include_thoughts=True`                                           | `*.thinking.{json,raw.txt,thoughts.md,summary.md}` (Demo 3)       |
| 4 | Long-context sliding-window + global attention| `chunk_audio_ffmpeg`, `policy_drift_summarize`                                               | `<audio>/chunk_<n>.json`, `policy_drift.json`, `policy_drift.mmd` |
| 5 | Strict JSON / `response_schema`               | `prompts/policy_analysis_v1.md` (schema), `call_google_genai_multimodal(response_schema=…)`  | Every JSON on disk                                                |
| 6 | Mixed-size deployment (E2B / 26B / 31B / Embedding / Shield) | `gemma_hf_backend.py`, `_default_gatekeeper_model`, `GOVERNANCE_GENAI_MODEL`     | Routed per file                                                   |
| 7 | Local open-weights fallback                   | `GOVERNANCE_LLM_BACKEND=huggingface`, `gemma_hf_backend.HFGemmaClient`                       | Same outputs, no network egress                                   |
| 8 | ShieldGemma safety review                     | `colab_safety_review.run_safety_review`                                                      | `05_safety_review/*.shield.json`                                  |

---

## 4. Prompt schema (governance domain adaptation)

`prompts/policy_analysis_v1.md` is the deconstruction prompt every demo binds to. It enforces:

- **Stable cross-query identifiers** — `person_<first>_<last>_<role>_<jurisdiction>`, `org_<short>_<jurisdiction>`, `leg_<type>_<num>_<year>_<jurisdiction>`, `subject_<descriptive>_<jurisdiction>`.
- **FIPS / postal-code extraction** — `county_fips`, `county`, `postal_code` on every decision, derived from the subject location or jurisdiction primary location.
- **Theme classification** — fixed 17-theme taxonomy.
- **Competing-interpretations capture** — every decision must record competing causal stories, dissenting diagnoses, and moral-value conflicts. This is what makes the output useful to a journalist and an academic, not just a clerk.
- **Media-citation grounding** — every decision heard in audio carries a `media_source_id` + `timestamp_start`/`timestamp_end` so playback links are deterministic.

`prompts/policy_analysis_sample_inputs.md` lists ten public YouTube meetings we used to develop and stress-test the prompt against actual recordings.

---

## 5. Routing rules (what runs where)

| Concern              | Default                                                | Override                                              |
|----------------------|--------------------------------------------------------|-------------------------------------------------------|
| Gatekeeper           | AI Studio `gemma-3n-e2b-it` (cheapest, fast)           | `GOVERNANCE_GATEKEEPER_FORCE_HF=1` → local `gemma-4-E2B` |
| Demos 1–3, 5 (PDF, image) | AI Studio `gemma-4-26b-a4b-it`                    | `GOVERNANCE_GENAI_MODEL=…` (any Gemma 4)              |
| Demo 4 (audio chunks) | Local HF `gemma-4-31b-it` (Gemma multimodal docs)     | `GOVERNANCE_DEMO4_PREFER_GEMMA_AUDIO=0` → Gemini fallback |
| Demo 6 (clustering)  | AI Studio `embedding-001` / `EmbeddingGemma`            | `GOVERNANCE_EMBED_MODEL=…`                            |
| Safety review        | ShieldGemma (AI Studio or HF)                          | `GOVERNANCE_SAFETY_REVIEW=0` to skip                  |

Full env-var table: [`scripts/colab/README.md`](scripts/colab/README.md).

---

## 6. Reproducibility (per §2.5.b — Winner's Obligations)

| Knob                                          | Default | Notes                                                                       |
|-----------------------------------------------|---------|-----------------------------------------------------------------------------|
| `SCOPE`                                       | `fast`  | Tuscaloosa county, 2026-02-18 only — ~45–75 min on Colab free tier          |
| `GOVERNANCE_DEMO_MAX_PDFS_PER_JUR`            | 3       | Demo 1 + 2 cap                                                              |
| `GOVERNANCE_DEMO_MAX_PAGES_PER_PDF`           | 8 / 12 / 16 | Per `SCOPE`                                                              |
| `GOVERNANCE_DEMO_MAX_AUDIO_PER_JUR`           | 1       | Demo 4 cap                                                                  |
| `GOVERNANCE_DEMO_MAX_AUDIO_CHUNKS`            | 4       | 15-min chunks per recording                                                 |
| `GOVERNANCE_DEMO_THINKING_BUDGET`             | `-1`    | Unlimited thinking tokens for Demo 3                                        |
| `GOVERNANCE_GATEKEEPER_AUDIO_WINDOW`          | 120     | Seconds of audio sent to triage                                             |
| `GOVERNANCE_GATEKEEPER_CONFIDENCE`            | 0.6     | Minimum confidence to keep a file                                           |
| `GOVERNANCE_GATEKEEPER_PDF_PAGES`             | 2       | First 1–2 pages sent to triage                                              |
| `GOVERNANCE_DEMO_YEAR_SCOPE`                  | on      | Only the newest `20xx/` folder per jurisdiction                             |
| `GOVERNANCE_DEMO_MEETING_DATES`               | 3       | Last N meeting dates per jurisdiction                                        |

These are the only hyper-parameters in the pipeline (we do not train). To reproduce the published outputs, run `02_run_meeting_llm.ipynb` with `SCOPE = "fast"` on Colab CPU + L4 GPU two-phase, with the demo corpus pre-staged on the shared Drive folder.

---

## 7. Failure handling

- **Per-call wall-clock timeouts** (`genai_quota_retry.call_with_wall_clock_timeout`) — a single hung socket can't kill a 200-file batch.
- **SIGALRM socket alarm** (Linux/Colab) — forces TCP abort after `timeout + buffer`.
- **Idempotency probes** — `demo2_pdf_outputs_complete`, `demo3_thinking_json_complete`, `demo4_drift_output_complete` skip already-done files. Disconnect-resume is automatic.
- **try/except around every API call, every `ffmpeg` subprocess, every `shutil.move`** — pipeline never aborts on a single bad PDF.
- **Two-phase Colab runtime** — Phase 1 (CPU, PDFs) → Phase 2 (L4 GPU, audio). Works around the one-runtime-at-a-time constraint.

---

## 8. What we explicitly did *not* build

- **No model fine-tuning.** We use Gemma 4 zero-shot with prompt + schema engineering. Less risk; more reproducible; faster to ship in 45 days.
- **No web UI.** Outputs are plain JSON / Markdown / Mermaid. Journalists and clerks consume them in whatever tool they already use; we don't add another login wall.
- **No paid services.** Free Colab + free AI Studio key reproduces everything. Offline mode reproduces it with zero API calls.
- **No bespoke evaluation harness.** Quality is judged by structural validation (schema), audit-trail visibility (thinking output), and ShieldGemma post-hoc review. We do not publish a "score on benchmark X" because there isn't one for *this* problem.
