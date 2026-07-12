#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f WAVECAR ]]; then
    echo "MISSING: WAVECAR" >&2
    exit 2
fi

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

# Run the existing ELF calculation example
python ex.py

# Write a reference metric from the ELFCAR
python - <<'PY'
from pathlib import Path

lines = Path("ELFCAR").read_text().splitlines()

# Find "Direct" line — atom coordinates start after it
coord_start = None
for i, ln in enumerate(lines):
    if ln.strip() == "Direct":
        coord_start = i
        break

if coord_start is None:
    print("ERROR: cannot find coordinate block in ELFCAR", file=open("/dev/stderr", "w"))
    raise SystemExit(1)

# Count atoms from the element counts line (the line before "Direct")
atoms_line = [int(x) for x in lines[coord_start - 1].split()]
natoms = sum(atoms_line)

# Grid dims are right after the coordinate block
grid_line_idx = coord_start + 1 + natoms
while grid_line_idx < len(lines) and lines[grid_line_idx].strip() == "":
    grid_line_idx += 1  # skip blank lines

if grid_line_idx >= len(lines):
    print("ERROR: grid dimensions not found after coordinates",
          file=open("/dev/stderr", "w"))
    raise SystemExit(1)

ngrid = tuple(int(x) for x in lines[grid_line_idx].split())
data = " ".join(lines[grid_line_idx+1:])
vals = [float(x) for x in data.split()]

Path("ref").mkdir(exist_ok=True)
Path("ref/elf_stats.txt").write_text(
    f"ngrid={ngrid} data_points={len(vals)} "
    f"min={min(vals):.6e} max={max(vals):.6e}\n"
)
print(f"ELFCAR: ngrid={ngrid}, data_points={len(vals)}, "
      f"min={min(vals):.6e}, max={max(vals):.6e}")
PY

echo "elf_test PASS"
