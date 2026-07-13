#!/usr/bin/env bash
# Regenerate MoSe2 spinor dumps with local SOC-patched VASP 5.4.4 and run spinormaker.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VASP_STD="${VASP_STD:-$ROOT/third_party/vasp.5.4.4.pl2/bin/vasp_std}"
NP="${NP:-8}"

if [[ ! -x "$VASP_STD" ]]; then
  echo "MISSING patched vasp_std at $VASP_STD" >&2
  echo "See docs/repro/O2_local_vasp_patch_build.md" >&2
  exit 2
fi

run_case () {
  local name=$1 ispin=$2 nbands=$3
  local base="$ROOT/examples/spinor/$name"
  local w="$base/soc_dump_work"
  mkdir -p "$w"
  cp -f "$base/POSCAR" "$base/POTCAR" "$base/KPOINTS" "$w/"
  cat > "$w/INCAR" <<EOF
SYSTEM = MoSe2 $name dump
PREC = Normal
ENCUT = 225
ISPIN = $ispin
ISTART = 0
ICHARG = 2
ISMEAR = 0
SIGMA = 0.1
ALGO = Normal
NELMIN = 4
NELM = 150
EDIFF = 1E-6
ISYM = 0
IBRION = -1
LORBIT = 11
LREAL = Auto
LWAVE = .TRUE.
LCHARG = .FALSE.
NBANDS = $nbands
NCORE = 4
EOF
  echo "=== $name: VASP dump ==="
  (
    cd "$w"
    export OMP_NUM_THREADS=1
    mpirun -np "$NP" "$VASP_STD" > vasp.log 2>&1
    test -s WAVECAR && test -s NormalCAR && test -s SocCar && test -s SocRadCar
    echo "=== $name: spinormaker ==="
    export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
    python "$ROOT/bin/spinormaker" \
      --mixwave-ibs 105 107 109 111 113 \
      --correct-kpts 1 \
      --full-kpts
    test -s WAVECAR_spinor
  )
  echo "=== $name OK ==="
}

run_case spinless 1 136
run_case ispin2 2 152

echo "=== examples/spinor/run.sh ==="
(cd "$ROOT/examples/spinor" && bash run.sh)
echo "DONE"

# Optional: SCF ncl+LSORBIT reference (expensive)
if [[ "${REGEN_NCL_REF:-0}" == "1" ]]; then
  VASP_NCL="${VASP_NCL:-$ROOT/third_party/vasp.5.4.4.pl2/bin/vasp_ncl}"
  W="$ROOT/examples/spinor/spinless/ncl_ref_work"
  mkdir -p "$W"
  cp "$ROOT/examples/spinor/spinless/POSCAR" "$ROOT/examples/spinor/spinless/POTCAR" \
     "$ROOT/examples/spinor/spinless/KPOINTS" "$W/"
  cat > "$W/INCAR" <<'IN'
SYSTEM = MoSe2 ncl LSORBIT ref
PREC = Normal
ENCUT = 225
ISTART = 0
ICHARG = 2
ISMEAR = 0
SIGMA = 0.1
ALGO = Normal
NELM = 120
EDIFF = 1E-6
ISYM = 0
LREAL = Auto
LWAVE = .TRUE.
LCHARG = .FALSE.
LNONCOLLINEAR = .TRUE.
LSORBIT = .TRUE.
SAXIS = 0 0 1
NBANDS = 272
NCORE = 4
IN
  (cd "$W" && OMP_NUM_THREADS=1 mpirun -np "$NP" "$VASP_NCL" > vasp.log 2>&1)
  export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
  python - <<PY
from pathlib import Path
import numpy as np
from vaspwfc import vaspwfc
ncl=vaspwfc("$W/WAVECAR", lsorbit=True)
sm=vaspwfc("$ROOT/examples/spinor/spinless/soc_dump_work/WAVECAR_spinor", lsorbit=True)
en=np.sort(ncl._bands[0,0,:]); es=np.sort(sm._bands[0,0,:])
n=min(en.size, es.size)
mae=float(np.mean(np.abs(en[:n]-es[:n])))
Path("$ROOT/examples/spinor/ref").mkdir(exist_ok=True)
Path("$ROOT/examples/spinor/ref/spinor_vs_ncl.txt").write_text(
    f"eig_mae_all={mae:.6e}\nncl_nb={ncl._nbands} sm_nb={sm._nbands}\n"
)
print("ncl compare MAE", mae)
PY
fi
