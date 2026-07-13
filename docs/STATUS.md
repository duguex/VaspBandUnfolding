# Project status snapshot

**Branch (personal fork):** `feature/c1-c2-examples` → `duguex/VaspBandUnfolding`  
**Policy:** local + fork only; **no PRs** to `QijingZheng/VaspBandUnfolding` unless explicitly requested.

Last verified (local):

```text
python scripts/smoke_examples.py   → pass=19 skip=0 fail=0
PYTHONPATH=. python -m pytest tests/ -q  → 15 passed
```

## What is done

| Area | Status |
|---|---|
| Feature inventory + IDs | [`FEATURES.md`](../FEATURES.md) |
| Goals (G1 proof / G2 reuse) | [`GOALS.md`](GOALS.md) |
| Assumptions | [`ASSUMPTIONS.md`](ASSUMPTIONS.md) |
| Citation labels | [`CITATION_POLICY.md`](CITATION_POLICY.md) |
| Example matrix C1/C2 | [`EXAMPLE_MATRIX.md`](EXAMPLE_MATRIX.md) |
| Academic roadmap | [`ACADEMIC_ROADMAP.md`](ACADEMIC_ROADMAP.md) |
| Smoke runner | `scripts/smoke_examples.py` |
| Infra + BSE CLI tests | `tests/` |
| Patched VASP 5.4.4 (local, gitignored) | `third_party/vasp.5.4.4.pl2/bin/vasp_{std,ncl}` |
| MoSe2 Soc\* dumps + spinormaker | `examples/spinor/*/soc_dump_work/` (gitignored); `scripts/regen_spinor_mose2.sh` |
| CO2 dipole gates | `examples/tdm/ref/l2_*.md` |
| ELF vs ELFCAR | `examples/elf_test/ref/elf_vs_vasp.txt` |
| Dual-frame NAC | `examples/nac/md_frames/` (gitignored) |

## C1 smoke

All science example **slugs** run (`ok`) except where the matrix marks **skip** (currently none for smoke paths; X6 realspace is a **separate** runner `run_realspace.sh` that exits 2 without WAVECAR).

## C2 / citation (summary)

See [`CITATION_POLICY.md`](CITATION_POLICY.md). Short version:

- **Default BSE mode:** `pw_only` (CLI). `paw_*` and finite-q → **quarantine**.
- **l2-partial (usable with caveats):** W1–W4, W6, B1, P1–P4, O1–O2, X1, X5, D1, D3, …
- **experimental:** W5, B2–B5, P5, O3, X4, X6, D2, …
- **Not full paper L2:** WAVEDER element-wise dipole; BSE paw/q parity; X6 without matching WAVECAR.

## Large / proprietary (not in git)

| Path | Content |
|---|---|
| `vasp.5.4.4.pl2.tgz`, `third_party/vasp*` | VASP sources & binaries |
| `examples/spinor/**/soc_dump_work/` | MoSe2 WAVECAR + Soc\* + WAVECAR_spinor |
| `examples/spinor/**/ncl_ref_work/` | ncl+LSORBIT reference |
| `examples/tdm/vasp_optics/work/` | CO2 LOPTICS |
| `examples/nac/md_frames/` | Dual-geometry WAVECARs |

Regenerate: [`repro/O2_local_vasp_patch_build.md`](repro/O2_local_vasp_patch_build.md), `scripts/regen_spinor_mose2.sh`, [`repro/X6_exciton_rs.md`](repro/X6_exciton_rs.md).

## How to verify after pull

```bash
pip install -e .
pip install -r requirements-optional.txt   # pySBT, spglib as needed
python scripts/smoke_examples.py
PYTHONPATH=. python -m pytest tests/ -q
# optional L2-ish checks
bash examples/tdm/run_l2.sh                # needs local optics workdir or rebuild
python examples/elf_test/compare_elf.py
bash examples/spinor/run.sh                # needs soc_dump_work present
```
