"""Read VASP unformatted ``WAVEDER`` (optical transition matrix CDER).

Physical model (VASP ``linear_optics.F``):

    CDER_BETWEEN_STATES(m, n, ik, ispin, j)
        = <u_m | -i d/dk_j | u_n>
        = - <u_m | r_j | u_n>

so the length-gauge position matrix element in Å is ``r = -CDER``.

Array layout on disk (single-precision complex ``GDEFS``)::

    record 1: NB_TOT, NBANDS_CDER, NKPTS, ISPIN   (4×int32)
    record 2: NODES_IN_DIELECTRIC_FUNCTION       (float64)
    record 3: WPLASMON(3,3)                      (float64)
    record 4: CDER(NB_TOT, NBANDS_CDER, NKPTS, ISPIN, 3)  (complex64)

Band indices in the file are **1-based** in VASP; NumPy arrays here are
**0-based**. The second band index ``n`` only runs over ``NBANDS_CDER``
(typically a valence-heavy window), while ``m`` runs over all bands.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import numpy as np
from numpy.typing import NDArray


def _read_fortran_record(handle: BinaryIO) -> bytes:
    """Read one little-endian Fortran unformatted record."""
    head = handle.read(4)
    if not head:
        raise EOFError("Unexpected EOF while reading Fortran record header")
    size = struct.unpack("<i", head)[0]
    if size < 0:
        raise ValueError(f"Invalid Fortran record size: {size}")
    data = handle.read(size)
    if len(data) != size:
        raise EOFError("Truncated Fortran record payload")
    tail = handle.read(4)
    if len(tail) != 4:
        raise EOFError("Missing Fortran record trailer")
    size2 = struct.unpack("<i", tail)[0]
    if size2 != size:
        raise ValueError(f"Fortran record length mismatch: {size} vs {size2}")
    return data


@dataclass(frozen=True)
class Waveder:
    """Optical transition elements from a VASP ``WAVEDER`` file."""

    nbands: int
    nbands_cder: int
    nkpts: int
    nspin: int
    nodes_in_dielectric_function: float
    wplasmon: NDArray[np.float64]
    cder: NDArray[np.complex128]

    @property
    def shape(self) -> tuple[int, int, int, int, int]:
        return tuple(int(x) for x in self.cder.shape)  # type: ignore[return-value]

    def r_matrix(
        self,
        *,
        m: int,
        n: int,
        ikpt: int = 1,
        ispin: int = 1,
    ) -> NDArray[np.complex128]:
        """Return ``<m|r|n>`` in Å for 1-based band / k / spin indices.

        Only valid when ``1 <= n <= nbands_cder``.
        """
        if not (1 <= m <= self.nbands):
            raise ValueError(f"m={m} out of range 1..{self.nbands}")
        if not (1 <= n <= self.nbands_cder):
            raise ValueError(f"n={n} out of range 1..{self.nbands_cder}")
        if not (1 <= ikpt <= self.nkpts):
            raise ValueError(f"ikpt={ikpt} out of range")
        if not (1 <= ispin <= self.nspin):
            raise ValueError(f"ispin={ispin} out of range")
        # CDER = -<r>
        return -np.asarray(
            self.cder[m - 1, n - 1, ikpt - 1, ispin - 1, :],
            dtype=np.complex128,
        )


def read_waveder(path: str | Path) -> Waveder:
    """Parse a binary VASP ``WAVEDER`` file."""
    path = Path(path)
    with path.open("rb") as handle:
        rec0 = _read_fortran_record(handle)
        if len(rec0) != 16:
            raise ValueError(f"Unexpected WAVEDER header size {len(rec0)} (want 16)")
        nb, nbc, nk, ns = struct.unpack("<4i", rec0)

        rec1 = _read_fortran_record(handle)
        if len(rec1) != 8:
            raise ValueError(f"Unexpected NODES record size {len(rec1)}")
        nodes = struct.unpack("<d", rec1)[0]

        rec2 = _read_fortran_record(handle)
        if len(rec2) != 72:
            raise ValueError(f"Unexpected WPLASMON record size {len(rec2)}")
        wplasmon = np.frombuffer(rec2, dtype="<f8").reshape(3, 3).copy()

        rec3 = _read_fortran_record(handle)
        expected = nb * nbc * nk * ns * 3 * 8  # complex64
        if len(rec3) != expected:
            # try complex128 fallback (rare double builds)
            expected128 = nb * nbc * nk * ns * 3 * 16
            if len(rec3) == expected128:
                cder = (
                    np.frombuffer(rec3, dtype="<c16")
                    .reshape(nb, nbc, nk, ns, 3)
                    .astype(np.complex128, copy=True)
                )
            else:
                raise ValueError(
                    f"CDER size {len(rec3)} incompatible with dims "
                    f"({nb},{nbc},{nk},{ns},3); expected {expected} (c64) "
                    f"or {expected128} (c128)"
                )
        else:
            cder = (
                np.frombuffer(rec3, dtype=np.complex64)
                .reshape(nb, nbc, nk, ns, 3)
                .astype(np.complex128, copy=True)
            )

    return Waveder(
        nbands=int(nb),
        nbands_cder=int(nbc),
        nkpts=int(nk),
        nspin=int(ns),
        nodes_in_dielectric_function=float(nodes),
        wplasmon=wplasmon,
        cder=cder,
    )


__all__ = ["Waveder", "read_waveder"]
