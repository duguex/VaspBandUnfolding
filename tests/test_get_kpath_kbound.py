from __future__ import annotations

from pathlib import Path

from vaspwfc import vaspwfc

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "examples" / "wfc_r" / "WAVECAR"


def test_get_kpath_sets_kbound_single_segment():
    if not WAVE.is_file():
        return
    wfc = vaspwfc(str(WAVE))
    nk = int(wfc._nkpts)
    kpath, kbound = wfc.get_kpath(nkseg=nk)
    assert len(kpath) == nk
    assert kbound is not None
    assert len(kbound) >= 2
