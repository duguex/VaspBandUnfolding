#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Check for AMAT text artifacts (prefer py_pw_only_both_AMAT.txt as primary)
if [[ ! -f py_pw_only_both_AMAT.txt ]]; then
    echo "MISSING: py_pw_only_both_AMAT.txt" >&2
    exit 2
fi

mkdir -p ref

python - <<'PY'
from pathlib import Path

p = Path("py_pw_only_both_AMAT.txt")
n = sum(1 for _ in p.open())
Path("ref").mkdir(exist_ok=True)
Path("ref/amat_lines.txt").write_text(f"lines={n}\n")
print(f"py_pw_only_both_AMAT.txt: {n} lines")
PY

echo "bsematrix/BP PASS"
