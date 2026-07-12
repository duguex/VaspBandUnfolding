#!/usr/bin/env python3
"""Tiny Fortran record round-trip using the same logic as wfull._read_fortran_record."""
from __future__ import annotations

import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from wfull import _read_fortran_record  # type: ignore[import-untyped]


def _write_record(path: Path, payload: bytes) -> None:
    n = len(payload)
    with path.open("wb") as f:
        f.write(struct.pack("<i", n))
        f.write(payload)
        f.write(struct.pack("<i", n))


def main() -> int:
    Path("ref").mkdir(exist_ok=True)

    # Create a tiny payload: 4 float64 values
    payload_orig = np.array([1.0, -2.5, 3.1415926535, 0.0], dtype=np.float64)
    rec_path = Path("record.bin")
    _write_record(rec_path, payload_orig.tobytes())

    # Read back using the wfull helper
    with rec_path.open("rb") as f:
        payload_read = _read_fortran_record(f)

    values_read = np.frombuffer(payload_read, dtype=np.float64)
    success = np.allclose(payload_orig, values_read)

    # Write round-trip report
    lines = [
        "# Fortran record round-trip test",
        f"Original payload: {payload_orig.tolist()}",
        f"Read back:        {values_read.tolist()}",
        f"Match:            {success}",
        f"nbytes:           {len(payload_read)}",
    ]
    report = "\n".join(lines) + "\n"
    Path("ref/roundtrip.txt").write_text(report)
    print(report)

    if not success:
        print("FAIL: round-trip mismatch", file=sys.stderr)
        return 1

    print("PASS: Fortran record round-trip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
