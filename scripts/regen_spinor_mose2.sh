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
