#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f sw.npy ]] && [[ ! -f awht.npy ]]; then
    echo "MISSING: sw.npy or awht.npy" >&2
    exit 2
fi

export PYTHONPATH="$(cd ../../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

python - <<'PY'
import numpy as np
from pathlib import Path

Path("ref").mkdir(exist_ok=True)
lines = []

if Path("sw.npy").exists():
    sw = np.load("sw.npy")
    lines.append(f"sw.shape={sw.shape} sw.sum={sw.sum():.6f}")
    print(f"spectral_weight shape={sw.shape} sum={sw.sum():.6f}")

if Path("awht.npy").exists():
    awht = np.load("awht.npy", allow_pickle=True)
    if isinstance(awht, (list, tuple)):
        for i, a in enumerate(awht):
            lines.append(f"awht[{i}].shape={a.shape} awht[{i}].sum={a.sum():.6f}")
            print(f"atomic_weights[{i}] shape={a.shape} sum={a.sum():.6f}")
    else:
        lines.append(f"awht.shape={awht.shape} awht.sum={awht.sum():.6f}")
        print(f"atomic_weights shape={awht.shape} sum={awht.sum():.6f}")

Path("ref/unfold_data.txt").write_text("\n".join(lines) + "\n")
PY

echo "unfold/Ce@BL-MoS2 PASS"
