#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
mkdir -p ref

WORKDIR=""
for d in ispin2/soc_dump_work spinless/soc_dump_work; do
  if [[ -f "$d/WAVECAR" && -f "$d/NormalCAR" && -f "$d/SocCar" && -f "$d/SocRadCar" ]]; then
    WORKDIR="$d"
    break
  fi
done

if [[ -z "$WORKDIR" ]]; then
  echo "MISSING: WAVECAR+NormalCAR+SocCar+SocRadCar under spinless|ispin2/soc_dump_work" >&2
  echo "See docs/repro/O2_local_vasp_patch_build.md" >&2
  exit 2
fi

echo "Using $WORKDIR"
(
  cd "$WORKDIR"
  if [[ ! -f WAVECAR_spinor ]]; then
    python "$PYTHONPATH/bin/spinormaker" --mixwave-ibs 105 107 109 111 113 --correct-kpts 1 --full-kpts
  fi
)

python - <<PY
from pathlib import Path
import numpy as np
from vaspwfc import vaspwfc
wdir = Path("$WORKDIR")
w = vaspwfc(str(wdir / "WAVECAR_spinor"), lsorbit=True)
phi = w.wfc_r(ikpt=1, iband=1)
comps = phi if isinstance(phi, (list, tuple)) else [phi]
norms = [float(np.linalg.norm(p)) for p in comps]
ref = Path("ref")
ref.mkdir(exist_ok=True)
(ref / "spinor_summary.txt").write_text(
    f"workdir={wdir.resolve()}\n"
    f"nspin={w._nspin} nk={w._nkpts} nb={w._nbands} nplw={w._nplws[0]}\n"
    f"component_norms={norms}\n"
)
print("wrote", ref / "spinor_summary.txt")
PY
echo "spinor PASS"
