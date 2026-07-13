#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
# Prefer env VBU_BSE_WAVECAR, else local WAVECAR
WAV="${VBU_BSE_WAVECAR:-WAVECAR}"
if [[ ! -f "$WAV" ]]; then
  cat >&2 <<'MSG'
MISSING: WAVECAR for exciton realspace (X6)

Need WAVECAR from the same BSE/GW run that produced BSEFATBAND.
Place it here as ./WAVECAR or set VBU_BSE_WAVECAR=/path/to/WAVECAR

See docs/repro/X6_exciton_rs.md
MSG
  exit 2
fi
mkdir -p ref
python bin/bseplot realspace \
  --bsefatband BSEFATBAND \
  --wavecar "$WAV" \
  --poscar POSCAR \
  --exciton 1 \
  --hole 0.5,0.5,0.5 \
  --output-dir ref 2>/dev/null || \
python ../../bin/bseplot realspace \
  --bsefatband BSEFATBAND \
  --wavecar "$WAV" \
  --poscar POSCAR \
  --exciton 1 \
  --hole 0.5,0.5,0.5 \
  --output-dir ref
echo "bseplot realspace PASS"
