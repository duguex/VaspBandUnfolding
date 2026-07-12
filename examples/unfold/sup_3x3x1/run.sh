#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f spectral_weight.npy ]]; then
    echo "MISSING: spectral_weight.npy" >&2
    exit 2
fi

export PYTHONPATH="$(cd ../../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

python - <<'PY'
import numpy as np
from pathlib import Path

w = np.load("spectral_weight.npy")
Path("ref").mkdir(exist_ok=True)
Path("ref/sw_shape.txt").write_text(f"shape={w.shape} sum={w.sum():.6f}\n")
print(f"spectral_weight shape={w.shape} sum={w.sum():.6f}")
PY

echo "unfold/sup_3x3x1 PASS"
