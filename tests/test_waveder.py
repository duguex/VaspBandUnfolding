from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from waveder import read_waveder

ROOT = Path(__file__).resolve().parents[1]
WAVEDER = ROOT / "examples" / "tdm" / "vasp_optics" / "work" / "WAVEDER"


@pytest.mark.skipif(not WAVEDER.is_file(), reason="local WAVEDER not present")
def test_read_waveder_shapes() -> None:
    wd = read_waveder(WAVEDER)
    assert wd.nbands == 24
    assert wd.nbands_cder == 16
    assert wd.nkpts == 1
    assert wd.nspin == 1
    assert wd.cder.shape == (24, 16, 1, 1, 3)
    assert wd.wplasmon.shape == (3, 3)
    r = wd.r_matrix(m=12, n=8)
    assert r.shape == (3,)
    assert np.isfinite(r).all()


def test_read_waveder_missing() -> None:
    with pytest.raises(FileNotFoundError):
        read_waveder(ROOT / "does_not_exist_WAVEDER")
