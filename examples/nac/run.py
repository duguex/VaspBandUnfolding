#!/usr/bin/env python3
"""NAC example: import check and placeholder.

Writes ref/api_present.txt to confirm nac_from_vaspwfc is importable.
Full NAC computation needs two different WAVECARs (different ionic steps).
"""
import sys
from pathlib import Path

try:
    from nac import nac_from_vaspwfc
    api_ok = True
    print("nac_from_vaspwfc import OK")
except ImportError as e:
    print(f"nac_from_vaspwfc import FAILED: {e}")
    api_ok = False

Path("ref").mkdir(exist_ok=True)
Path("ref/api_present.txt").write_text(
    f"nac_from_vaspwfc importable={api_ok}\n"
    "NAC requires two WAVECARs from different ionic steps; skipped.\n"
)

if not api_ok:
    sys.exit(1)

# If we got two WAVECAR paths, report what we'd compute
if len(sys.argv) > 2:
    wave_a, wave_b = sys.argv[1], sys.argv[2]
    print(f"WAVECAR_A: {wave_a}")
    print(f"WAVECAR_B: {wave_b}")
    if wave_a == wave_b:
        print("Same file — not a valid NAC pair. Exit 2.")
        sys.exit(2)
    print("Two distinct WAVECARs provided — NAC computation pending real data.")
else:
    print("No WAVECAR args — import-only mode.")

print("nac import check OK")
