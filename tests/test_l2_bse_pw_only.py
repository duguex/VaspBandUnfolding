"""L2 gate: BSE pw_only benchmark artifacts exist.

Asserts that examples/bsematrix/BP contains both vasp_* and py_pw_only_*
AMAT text files for at least the three core interaction cases
(direct-only, exchange-only, both).
"""
from __future__ import annotations

from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parent
BP_DIR = ROOT / "examples" / "bsematrix" / "BP"

# Core benchmark cases that must have both VASP and py_pw_only AMATs
CORE_CASES = ["direct_only", "exchange_only", "both"]
VASP_FILES = [f"vasp_{case}_AMAT.txt" for case in CORE_CASES]
PY_FILES = [f"py_pw_only_{case}_AMAT.txt" for case in CORE_CASES]


def test_bp_amat_vasp_refs_present():
    """VASP reference AMAT files exist for all core cases."""
    missing = [f for f in VASP_FILES if not (BP_DIR / f).is_file()]
    assert missing == [], f"Missing VASP AMAT refs: {missing}"


def test_bp_amat_py_pw_only_present():
    """Python pw_only AMAT files exist for all core cases."""
    missing = [f for f in PY_FILES if not (BP_DIR / f).is_file()]
    assert missing == [], f"Missing py_pw_only AMAT outputs: {missing}"
