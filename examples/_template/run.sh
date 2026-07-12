#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
# if [[ ! -f WAVECAR ]]; then echo "MISSING: WAVECAR" >&2; exit 2; fi
mkdir -p ref
echo "template ok" | tee ref/smoke.txt
