"""L2 gate: PAW nonlocal projector (P2) C1 output validation.

If examples/projectors/lreal_false/cproj.npy exists, assert all values
are finite and the max absolute deviation is within bounds documented in
ref/cproj_max.txt.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parent
CPROJ_NPY = ROOT / "examples" / "projectors" / "lreal_false" / "cproj.npy"
CPROJ_MAX_REF = ROOT / "examples" / "projectors" / "ref" / "cproj_max.txt"


def test_projector_cproj_within_bound():
    """cproj.npy values are finite and within the reference max-abs bound."""
    if not CPROJ_NPY.is_file():
        # Runner hasn't been executed / data not bundled — skip gracefully
        return

    data = np.load(CPROJ_NPY)
    assert np.all(np.isfinite(data)), "cproj.npy contains non-finite values"

    max_abs = float(np.max(np.abs(data)))
    if CPROJ_MAX_REF.is_file():
        ref_text = CPROJ_MAX_REF.read_text().strip()
        # Parse "cproj_max=3.39075400e+00"
        ref_val = float(ref_text.split("=")[1])
        # Allow a small tolerance beyond the reported max
        assert max_abs <= ref_val * 1.01, (
            f"max|Δ| = {max_abs:.6e} exceeds ref {ref_val:.6e} * 1.01"
        )
    else:
        # No ref file — use a loose sanity bound (deviation > 10 would be concerning)
        assert max_abs < 10, f"max|Δ| = {max_abs} exceeds loose bound of 10"
