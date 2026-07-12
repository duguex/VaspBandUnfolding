#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref
python run.py
echo "neb PASS"
