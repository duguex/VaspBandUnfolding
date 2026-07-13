"""Off-diagonal AMAT residuals vs VASP text refs (examples/bsematrix/BP)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
BP = ROOT / "examples" / "bsematrix" / "BP"

# From BP README AMAT comparison summary (off-diagonal convention)
EXPECTED = {
    ("direct_only", "pw_only"): (0.00338936, 0.02105668),
    ("direct_only", "paw_orth_only"): (0.02125834, 0.12448971),
    ("direct_only", "paw_full"): (0.01587339, 0.08222105),
    ("exchange_only", "pw_only"): (0.00564986, 0.04682126),
    ("exchange_only", "paw_orth_only"): (0.00634830, 0.04821367),
    ("exchange_only", "paw_full"): (0.00183452, 0.01365123),
    ("both", "pw_only"): (0.00356970, 0.02356358),
    ("both", "paw_orth_only"): (0.01594623, 0.08810736),
    ("both", "paw_full"): (0.01391734, 0.07014263),
    ("qext_both", "pw_only"): (0.01898975, 0.05205552),
    ("qext_both", "paw_orth_only"): (0.03391579, 0.10749209),
    ("qext_both", "paw_full"): (0.01905383, 0.06847281),
}


def _load_amat(path: Path) -> np.ndarray:
    rows: dict[tuple[int, int], complex] = {}
    n = None
    for ln in path.read_text().splitlines():
        if ln.startswith("# shape"):
            n = int(ln.split()[2])
            continue
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        parts = ln.split()
        if len(parts) < 4:
            continue
        try:
            i, j = int(parts[0]), int(parts[1])
            re, im = float(parts[2]), float(parts[3])
        except ValueError:
            continue
        rows[(i, j)] = re + 1j * im
    if n is None:
        n = max(max(i, j) for i, j in rows)
    mat = np.zeros((n, n), dtype=np.complex128)
    for (i, j), val in rows.items():
        mat[i - 1, j - 1] = val
    return mat


def _offdiag_metrics(py: np.ndarray, vasp: np.ndarray) -> tuple[float, float]:
    d = py - vasp
    np.fill_diagonal(d, 0.0)
    return float(np.max(np.abs(d))), float(np.linalg.norm(d))


@pytest.mark.parametrize("case,mode", list(EXPECTED.keys()))
def test_amat_offdiag_residual(case: str, mode: str) -> None:
    vasp_path = BP / f"vasp_{case}_AMAT.txt"
    py_path = BP / f"py_{mode}_{case}_AMAT.txt"
    if not vasp_path.is_file() or not py_path.is_file():
        pytest.skip(f"missing {vasp_path.name} or {py_path.name}")
    vasp = _load_amat(vasp_path)
    py = _load_amat(py_path)
    mx, fr = _offdiag_metrics(py, vasp)
    exp_mx, exp_fr = EXPECTED[(case, mode)]
    assert mx == pytest.approx(exp_mx, rel=1e-4, abs=1e-7)
    assert fr == pytest.approx(exp_fr, rel=1e-4, abs=1e-7)


def test_exchange_only_paw_full_beats_pw_only() -> None:
    """Documented: exchange-only kernel residual is best with paw_full."""
    mx_pw, _ = EXPECTED[("exchange_only", "pw_only")]
    mx_pf, _ = EXPECTED[("exchange_only", "paw_full")]
    assert mx_pf < mx_pw


def test_finite_q_worse_than_q0_pw_only() -> None:
    mx_q0, _ = EXPECTED[("both", "pw_only")]
    mx_q, _ = EXPECTED[("qext_both", "pw_only")]
    assert mx_q > mx_q0
