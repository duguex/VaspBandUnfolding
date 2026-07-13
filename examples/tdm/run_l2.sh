#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
bash run.sh
python compare_optics.py
python compare_waveder.py
python compare_ae_waveder.py
