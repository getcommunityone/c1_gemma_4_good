#!/usr/bin/env bash
# CommunityOne — judge quickstart.
# Runs Gatekeeper triage + Demo 1 (visual OCR) against the
# pre-staged Tuscaloosa County, AL corpus.
#
# Usage:
#   GEMINI_API_KEY=...  bash demos/quickstart.sh
#   GEMINI_API_KEY=...  bash demos/quickstart.sh --dry-run
#
# Requirements:
#   - python3.10+
#   - ffmpeg, poppler-utils
#   - Drive-mounted (or local) corpus under
#     $GOVERNANCE_PIPELINE_DATA_ROOT/01_raw_inputs/
#
# This is a smoke-test path that proves the pipeline works end-to-end
# on one jurisdiction in <5 minutes. For the full multi-jurisdiction
# run, use scripts/colab/02_run_meeting_llm.ipynb.

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -z "${GEMINI_API_KEY:-}" ]] && [[ -z "${GOOGLE_API_KEY:-}" ]]; then
  echo "error: set GEMINI_API_KEY (free key at https://aistudio.google.com)" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt

if [[ -z "${GOVERNANCE_PIPELINE_DATA_ROOT:-}" ]]; then
  if [[ -d "/mnt/g/My Drive/CommunityOne/hackathons/2026_Gemma_4_Good" ]]; then
    export GOVERNANCE_PIPELINE_DATA_ROOT="/mnt/g/My Drive/CommunityOne/hackathons/2026_Gemma_4_Good"
  else
    export GOVERNANCE_PIPELINE_DATA_ROOT="$PWD/data/hackathons/2026_Gemma_4_Good"
  fi
fi
echo "→ GOVERNANCE_PIPELINE_DATA_ROOT=$GOVERNANCE_PIPELINE_DATA_ROOT"

# Default to the fast preset: Tuscaloosa county, one meeting date, PDF+video.
export GOVERNANCE_DEMO_SCOPE="${GOVERNANCE_DEMO_SCOPE:-fast}"
echo "→ SCOPE=$GOVERNANCE_DEMO_SCOPE"

echo
echo "==> Gatekeeper triage (Demo 0) — dry-run audit"
.venv/bin/python scripts/colab/gatekeeper_triage.py \
  --dry-run --max-files 20 --verbose "$@"

echo
echo "Quickstart complete. For the full pipeline (Demos 1–6 + ShieldGemma):"
echo "  jupyter lab scripts/colab/02_run_meeting_llm.ipynb"
echo
echo "Or open the static web UX (no install required):"
echo "  https://getcommunityone.github.io/c1_gemma_4_good/"
