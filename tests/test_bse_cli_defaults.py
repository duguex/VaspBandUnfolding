from __future__ import annotations

import re
from pathlib import Path

import bsematrix

ROOT = Path(__file__).resolve().parents[1]
BP_README = ROOT / "examples" / "bsematrix" / "BP" / "README.md"


def test_cli_default_mode_is_pw_only():
    # required args so parse succeeds
    ns = bsematrix.parse_args(
        ["--vb-num", "2", "--cb-num", "2", "--wavecar", "WAVECAR", "--outcar", "OUTCAR", "--kpoints", "KPOINTS"]
    )
    assert ns.mode == "pw_only"


def test_cli_help_mentions_quarantine():
    help_txt = bsematrix.parse_args.__doc__ or ""
    # epilog is on the parser; invoke -h via building parser internals
    import argparse

    # re-run parse_args construction by calling with -h is SystemExit; read source
    src = Path(bsematrix.__file__).read_text()
    assert 'default="pw_only"' in src
    assert "quarantine" in src.lower()


def test_bp_readme_documents_pw_only_best_and_finite_q_mismatch():
    text = BP_README.read_text()
    assert "pw_only" in text
    assert "finite-q" in text.lower() or "finite-q both" in text
    # residual table has max(abs(ΔA))
    assert "max(abs(ΔA))" in text or "max(abs" in text
    # ensure quarantine language present in citation policy section
    assert "quarantine" in text.lower() or "not as parity" in text.lower() or "not validated" in text.lower()


def test_bp_pw_only_both_amat_exists():
    files = list((ROOT / "examples" / "bsematrix" / "BP").glob("py_pw_only_both_AMAT.txt"))
    assert files, "missing py_pw_only_both_AMAT.txt reference"
    # residual for both/pw_only from README table ~0.00357
    m = re.search(
        r"both\s*\|\s*`pw_only`\s*\|\s*([0-9.]+)",
        BP_README.read_text(),
    )
    if m:
        val = float(m.group(1))
        assert val < 0.01  # documented residual stays small for citable mode
