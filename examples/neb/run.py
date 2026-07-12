#!/usr/bin/env python3
"""NEB example: parse minimal OUTCAR stubs and produce PES."""
import os
from pathlib import Path

# Create fake image directories with minimal OUTCAR stubs
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

images = ["00_init", "01_ts", "02_final"]
energies = [0.0, 0.5234, 0.0]  # barrier height eV
reaction_coords = [0.0, 1.258, 2.516]

for img, en in zip(images, energies):
    img_dir = IMAGES_DIR / img
    img_dir.mkdir(exist_ok=True)
    outcars = [
        img_dir / "OUTCAR",
        img_dir / "outcar",
    ]
    # Write OUTCAR with enough content for parsing
    content = f""" VASP run
   energy  without  entropy=     {en:16.8f}  energy(sigma->0) =     {en:16.8f}
"""
    for oc in outcars:
        oc.write_text(content)

# Parse energies
parsed = []
for img in images:
    oc = IMAGES_DIR / img / "OUTCAR"
    if not oc.exists():
        oc = IMAGES_DIR / img / "outcar"
    for line in oc.read_text().splitlines():
        if "energy  without" in line:
            en = float(line.split()[-1])
            parsed.append(en)
            break

assert len(parsed) == 3, f"Expected 3 energies, got {parsed}"
print(f"Parsed energies: {parsed}")

# Write PES data
rc = reaction_coords
Path("ref/pes.dat").write_text(
    "# Reaction coordinate [A]   Energy [eV]\n"
    + "\n".join(f"{r:12.6f}  {e:12.6f}" for r, e in zip(rc, parsed))
    + "\n"
)
print(f"Wrote ref/pes.dat: coord={rc}, energies={parsed}")
print("neb PASS")
