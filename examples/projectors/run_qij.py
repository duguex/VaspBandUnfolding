#!/usr/bin/env python3
"""Compute PAW Qij matrices from POTCAR and dump Frobenius norms.

Q_{ij} = <phi_i^AE|phi_j^AE> - <phi_i^PS|phi_j^PS>

This is a pure POTCAR operation — no WAVECAR needed.
"""
import numpy as np
from pathlib import Path
from paw import pawpotcar

potcar_dir = "lreal_false"
potcar = Path(potcar_dir) / "POTCAR"
if not potcar.exists():
    potcar = Path(potcar_dir) / "POTCAR"

potstrs = potcar.read_text().split("End of Dataset")[:-1]
print(f"Found {len(potstrs)} PAW datasets in {potcar}")

results = []
for i, potstr in enumerate(potstrs):
    if not potstr.strip():
        continue
    pp = pawpotcar(potstr)
    Qij = pp.get_Qij()
    frob = float(np.linalg.norm(Qij, "fro"))
    results.append((pp.element, Qij.shape, frob))
    print(f"  Element {pp.element}: Qij shape {Qij.shape}, Frobenius norm = {frob:.8e}")

Path("ref").mkdir(exist_ok=True)
with open("ref/qij_norm.txt", "w") as f:
    f.write("# element  Qij_shape  Frobenius_norm\n")
    for elem, shape, norm in results:
        f.write(f"{elem:8s}  {str(shape):12s}  {norm:.8e}\n")

print("Wrote ref/qij_norm.txt")
