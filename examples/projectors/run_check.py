#!/usr/bin/env python3
"""Non-interactive projector sanity check: load cproj.npy, compute max absolute value."""
import numpy as np
from pathlib import Path

cproj = np.load("lreal_false/cproj.npy")
max_val = float(np.abs(cproj).max())
Path("ref").mkdir(exist_ok=True)
Path("ref/cproj_max.txt").write_text(f"cproj_max={max_val:.8e}\n")
print(f"cproj max abs: {max_val:.8e}")
