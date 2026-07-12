from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCIENCE_IDS = [
    "W1", "W2", "W3", "W4", "W5", "W6",
    "B1", "B2", "B3", "B4", "B5",
    "P1", "P2", "P3", "P4", "P5",
    "O1", "O2", "O3",
    "X1", "X2", "X3", "X4", "X5", "X6",
    "D1", "D2", "D3",
]


def test_all_science_ids_appear_in_matrix():
    text = (ROOT / "docs" / "EXAMPLE_MATRIX.md").read_text()
    missing = [i for i in SCIENCE_IDS if not re.search(rf"\b{i}\b", text)]
    assert missing == [], f"IDs missing from EXAMPLE_MATRIX: {missing}"
