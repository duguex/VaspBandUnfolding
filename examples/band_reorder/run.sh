#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f WAVECAR ]]; then
    echo "MISSING: WAVECAR - band reordering requires a converged WAVECAR" >&2
    echo "Place a WAVECAR (from a VASP run with LORBIT>=11 and LWAVE=.TRUE.)" >&2
    echo "in this directory and re-run." >&2
    exit 2
fi

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

# TODO: implement band reordering by overlap once the API is stable.
# For now, validate that WAVECAR loads and I/O works.
python - <<'PY'
from vaspwfc import vaspwfc
from pathlib import Path

wfc = vaspwfc("WAVECAR")
nbands = wfc._nbands
nkpts = wfc._nkpts
Path("ref").mkdir(exist_ok=True)
Path("ref/wavecar_info.txt").write_text(
    f"nbands={nbands} nkpts={nkpts} nelect={wfc._nelect:.2f}\n"
)
print(f"WAVECAR: {nbands} bands, {nkpts} k-points, {wfc._nelect:.2f} electrons")
PY

echo "band_reorder PASS (WAVECAR I/O only; reorder TBD)"
