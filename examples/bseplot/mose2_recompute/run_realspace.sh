#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../../.. && pwd)"
export PYTHONPATH="$ROOT:${PYTHONPATH:-}"
VASP="${VASP_STD:-$ROOT/third_party/vasp.5.4.4.pl2/bin/vasp_std}"
mkdir -p work ref
# POTCAR: local copy or parent bseplot POTCAR
if [[ ! -f POTCAR && -f ../POTCAR ]]; then cp -f ../POTCAR POTCAR; fi
cp -f POSCAR KPOINTS work/ 2>/dev/null || true
cp -f POTCAR work/ 2>/dev/null || true
if [[ ! -f work/INCAR ]]; then
  [[ -f work/INCAR.scf ]] && cp -f work/INCAR.scf work/INCAR
fi
if [[ ! -s work/WAVECAR ]]; then
  [[ -x "$VASP" ]] || { echo "MISSING vasp_std at $VASP" >&2; exit 2; }
  (cd work && OMP_NUM_THREADS=1 mpirun -np "${NP:-8}" "$VASP" > vasp_scf.log 2>&1)
fi
[[ -s work/WAVECAR && -f work/OUTCAR ]] || { echo "MISSING work/WAVECAR or OUTCAR" >&2; exit 2; }
if [[ "${FORCE:-0}" == "1" || ! -s BSEFATBAND ]]; then
  python "$ROOT/bsematrix.py" \
    --wavecar work/WAVECAR --outcar work/OUTCAR --kpoints work/KPOINTS \
    --mode pw_only --interaction hartree \
    --vb-num 2 --cb-num 3 --ewin 0 12 --epsilon 8.0 \
    --bsefatband-output BSEFATBAND --output-prefix AMAT
fi
python "$ROOT/bin/bseplot" realspace \
  --bsefatband BSEFATBAND --wavecar work/WAVECAR --poscar POSCAR \
  --exciton 1 --hole-from-max-akcv --cumulative-weight 0.5 \
  --fft-grid '16 16 32' --output-dir ref --prefix mose2_x1
# refresh compact metrics
python - <<'PY'
from pathlib import Path
import numpy as np
rho = Path("ref/mose2_x1_001_electron_rho.vasp")
assert rho.is_file(), rho
vals = []
for ln in rho.read_text().splitlines():
    for tok in ln.split():
        try:
            vals.append(float(tok))
        except ValueError:
            pass
arr = np.asarray(vals, float)
Path("ref/realspace_summary.txt").write_text(
    f"system=MoSe2_primitive\n"
    f"density_file={rho.name}\n"
    f"density_bytes={rho.stat().st_size}\n"
    f"n_floats_parsed={arr.size}\n"
    f"min={arr.min():.6e}\nmax={arr.max():.6e}\nsum={arr.sum():.6e}\n"
    f"note=self-consistent recompute pipeline\n"
)
print(Path("ref/realspace_summary.txt").read_text())
PY
echo "mose2_recompute realspace PASS"
