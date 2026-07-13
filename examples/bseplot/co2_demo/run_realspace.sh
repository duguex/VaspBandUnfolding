#!/usr/bin/env bash
# Self-contained X6 demo: BSEFATBAND from bsematrix (pw_only/hartree) + CO2 WAVECAR.
# Not a VASP BSE parity test — exercises the realspace pipeline end-to-end.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../../.. && pwd):${PYTHONPATH:-}"
ROOT="$(cd ../../.. && pwd)"
WORK="$ROOT/examples/tdm/vasp_optics/work"

if [[ ! -f "$WORK/WAVECAR" ]]; then
  echo "MISSING: $WORK/WAVECAR (run CO2 LOPTICS / tdm optics first)" >&2
  exit 2
fi

mkdir -p ref
ln -sfn "$WORK/WAVECAR" WAVECAR
cp -f "$WORK/POSCAR" POSCAR 2>/dev/null || true
[[ -f KPOINTS ]] || cat > KPOINTS <<'EOF'
Gamma
0
Gamma
1 1 1
0 0 0
EOF

python "$ROOT/bsematrix.py" \
  --wavecar WAVECAR \
  --outcar "$WORK/OUTCAR" \
  --kpoints KPOINTS \
  --mode pw_only \
  --interaction hartree \
  --vb-num 2 --cb-num 3 \
  --ewin 0 20 \
  --epsilon 5.0 \
  --bsefatband-output BSEFATBAND \
  --output-prefix AMAT

python "$ROOT/bin/bseplot" realspace \
  --bsefatband BSEFATBAND \
  --wavecar WAVECAR \
  --poscar POSCAR \
  --exciton 1 \
  --hole 0.5,0.5,0.5 \
  --supercell '1 1 1' \
  --fft-grid '48 48 48' \
  --output-dir ref \
  --prefix co2_x1

# compact metrics (no multi-MB density in git)
python - <<'PY'
from pathlib import Path
import numpy as np
rho = Path("ref/co2_x1_001_electron_rho.vasp")
assert rho.is_file(), rho
# CHGCAR-like: last block floats
text = rho.read_text().splitlines()
# find grid line: three ints after coordinates
# simple: all floats in file
vals = []
for ln in text:
    for tok in ln.split():
        try:
            vals.append(float(tok))
        except ValueError:
            pass
arr = np.asarray(vals, dtype=float)
# crude stats on trailing density numbers
Path("ref/realspace_summary.txt").write_text(
    f"density_file={rho.name}\n"
    f"n_floats_parsed={arr.size}\n"
    f"min={arr.min():.6e}\nmax={arr.max():.6e}\n"
    f"sum={arr.sum():.6e}\n"
    f"note=self-consistent CO2 BSE demo; not VASP BSE parity\n"
)
print(Path("ref/realspace_summary.txt").read_text())
PY
echo "co2_demo realspace PASS"
