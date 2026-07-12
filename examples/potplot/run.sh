#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

# POTCAR is required; try common neighbours if not in this directory
if [[ ! -f POTCAR ]]; then
    for src in \
        ../projectors/lreal_false/POTCAR \
        ../projectors/lreal_true/POTCAR \
        ../band_reorder/POTCAR \
        ../aewfc/co2/POTCAR; do
        if [[ -f "$src" ]]; then
            cp "$src" POTCAR
            echo "Copied POTCAR from $src"
            break
        fi
    done
fi

if [[ ! -f POTCAR ]]; then
    echo "MISSING: POTCAR - copy one into this directory from examples/projectors/" >&2
    exit 2
fi

mkdir -p ref

# Generate the PAW projector / partial-wave plot with non-interactive Agg backend
MPLBACKEND=Agg python - <<'PY'
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from paw import pawpotcar
from pathlib import Path

potstrs = open("POTCAR").read().split("End of Dataset")[:-1]
pawpp = [pawpotcar(p) for p in potstrs]
pp = pawpp[0]
print(f"POTCAR element: {pp.element}, lmax={pp.lmax}")
pp.plot()
Path("ref").mkdir(exist_ok=True)
plt.savefig("ref/ti_pot.png", dpi=240, bbox_inches="tight")
print("Saved ref/ti_pot.png")
PY

echo "potplot PASS"
