"""L2 gate: Ewald / Madelung against reference values.

Parses examples/ewald/ref/madelung.out and checks that a NaCl-like
Madelung constant is present and the file has at least one data row.
"""
from __future__ import annotations

from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parent
MADELUNG_REF = ROOT / "examples" / "ewald" / "ref" / "madelung.out"


def test_madelung_ref_has_entries():
    """ref/madelung.out exists, contains at least one data line and a NaCl value."""
    assert MADELUNG_REF.is_file(), f"Missing ref file: {MADELUNG_REF}"
    text = MADELUNG_REF.read_text()
    # madelung.out uses non-pipe aligned columns (leading spaces, not |)
    data_lines = [ln for ln in text.strip().splitlines()
                  if ln.strip() and "Crystal" not in ln and "---" not in ln
                  and ln.strip().startswith("NaCl")]
    assert len(data_lines) >= 1, f"Expected >= 1 NaCl data row, got {len(data_lines)}"
    assert "1.747" in text, "NaCl Madelung constant value (~1.7476) not found in madelung.out"
