# Demos — *pick your speed*

Three demo surfaces, three different time budgets, **same Gemma 4 outputs** underneath. Open the one that fits your next few minutes.

| Time   | Surface                                       | What you see                                                              |
| ------ | --------------------------------------------- | ------------------------------------------------------------------------- |
| 30 s   | [Web UX (live)](#1-web-ux-30-seconds)         | The equalizer in a browser. Search, ACS map, Gemma meetings.              |
| 5 min  | [Colab notebook](#2-colab-pipeline-5-minutes-to-setup-45-min-to-run) | The pipeline running in real time on a free Colab key. |
| 15 min | [Offline mode](#3-offline-mode-15-minutes-on-an-l4-gpu) | Same notebook with `GOVERNANCE_LLM_BACKEND=huggingface`. Zero bytes leave the box. |

---

## 1) Web UX — *30 seconds*

> **<https://getcommunityone.github.io/c1_gemma_4_good/>**

Static React 18 + Vite app, built nightly from `web/` and published via GitHub Pages. No login. No API key. No backend at all — every byte ships in the static bundle.

Three tabs:

- **Search** — client-side search index over indexed jurisdictions.
- **Data Explorer** — ACS county map + Gemma-meeting overlay.
- **Gemma Meetings** — the Demo 1–4 JSON outputs for Tuscaloosa County, AL and Sweet Grass County, MT, rendered as decision cards + drift maps.

Run locally:

```bash
cd web
npm install
npm run dev
# open http://localhost:5173/c1_gemma_4_good/
```

Refresh the meeting/search index after a pipeline run:

```bash
python scripts/export_web_demo_index.py
```

## 2) Colab pipeline — *5 minutes to set up, 45 min to run*

> [**▶ Open in Colab**](https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb)

1. Get a free Gemini API key at <https://aistudio.google.com>.
2. In Colab, **🔑 Secrets → +** → name `GEMINI_API_KEY`, value = your key.
3. **Runtime → Run all**. Start on CPU; switch to **L4 GPU + High RAM** at §6 Phase 2.
4. Watch the logs in §6 — each demo logs `KEEP | AL/county/county_01125/...` as it works.
5. Outputs land on your Drive at `…/03_processed_outputs/02_gemma_json/`.

### What you'll see in 45 minutes

| Step             | Output file                                                | Gemma 4 capability shown                  |
| ---------------- | ---------------------------------------------------------- | ----------------------------------------- |
| §6 Demo 0        | `00_logs/triage_report_<UTC>.json`                          | E2B / E4B Gatekeeper                       |
| §6 Demo 1        | `<pdf>.visual_ocr.txt`                                      | Native multimodality on scanned PDFs       |
| §6 Demo 2        | `<pdf>/<page>.json` + `_token_budget_report.json`           | Adjustable per-page token budget           |
| §6 Demo 3        | `<pdf>.thinking.thoughts.md`                                | Built-in thinking mode, published         |
| §6 Demo 4        | `<audio>/policy_drift.mmd` (Mermaid diagram)                | Long-context audio chunking + drift       |
| End of §6        | `05_safety_review/<artifact>.shield.json`                   | ShieldGemma post-hoc review               |

## 3) Offline mode — *15 minutes on an L4 GPU*

> **Zero bytes leave the machine.** This is the mode that ships to a courthouse on a satellite connection.

Same notebook, two env vars set before §3 install:

```python
import os
os.environ["GOVERNANCE_LLM_BACKEND"] = "huggingface"
os.environ["HF_TOKEN"] = "hf_…"   # gated google/gemma-4-* repos
```

Then run normally. The pipeline downloads Gemma 4 weights once (~25 GB for `gemma-4-26b-a4b-it`), then operates entirely on the local GPU. No telemetry. No API call.

Smaller-laptop fallback:

```python
os.environ["GOVERNANCE_GENAI_MODEL"] = "google/gemma-4-E2B"
os.environ["GOVERNANCE_GATEKEEPER_FORCE_HF"] = "1"
```

`E2B` runs on commodity laptop CPU/GPU at the cost of throughput.

---

## What if a judge has only 30 seconds?

Open [the web URL](https://getcommunityone.github.io/c1_gemma_4_good/), click **Gemma Meetings**, pick *Sweet Grass County, MT*, read the first decision card. That's the entire pitch in one screen.
