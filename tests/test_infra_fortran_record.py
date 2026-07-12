import struct
from pathlib import Path
import numpy as np

from wfull import _read_fortran_record


def _write_record(path: Path, payload: bytes) -> None:
    n = len(payload)
    with path.open("wb") as f:
        f.write(struct.pack("<i", n))
        f.write(payload)
        f.write(struct.pack("<i", n))


def test_fortran_record_roundtrip_via_helper(tmp_path: Path):
    """Use the private wfull._read_fortran_record helper to verify round-trip."""
    p = tmp_path / "rec.bin"
    payload = np.arange(4, dtype=np.float64).tobytes()
    _write_record(p, payload)

    with p.open("rb") as f:
        data = _read_fortran_record(f)

    n = struct.unpack_from("<i", payload[:0] + payload)
    assert data == payload
    assert len(data) == 32  # 4 float64


def test_fortran_record_manual_roundtrip(tmp_path: Path):
    """Manual struct-based round-trip verification."""
    p = tmp_path / "rec.bin"
    payload = np.arange(4, dtype=np.float64).tobytes()
    _write_record(p, payload)

    data = p.read_bytes()
    n = struct.unpack_from("<i", data, 0)[0]
    assert n == len(payload)
    assert data[4:4 + n] == payload
