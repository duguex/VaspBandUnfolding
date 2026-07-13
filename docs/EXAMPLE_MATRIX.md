# Example Matrix

| ID | Slug path | Runner | C1 | C2 | Notes |
|---|---|---|---|---|---|
| W1 | `examples/wfc_r/` | `bash run.sh` | ok | l2-partial | Extend existing: WAVECAR I/O, gamma-only, ncl |
| W2 | `examples/wfc_r/` | `bash run.sh` | ok | l2-partial | Extend existing: G-vector set / cutoff sphere |
| W3 | `examples/wfc_r/` | `bash run.sh` | ok | l2-partial | Extend existing: real-space PS wavefunction |
| W4 | `examples/tdm/` | `bash run.sh` | ok | l2-partial | CO2 gates in ref/l2_table.md; see docs/CITATION_POLICY.md |
| W5 | `examples/ipr/` | `bash run.sh` | ok | experimental | New: inverse participation ratio |
| W6 | `examples/elf_test/` | `bash run.sh` | ok | l2-partial | vs ELFCAR corr~0.986; see ref/elf_vs_vasp.txt |
| B1 | `examples/unfold/sup_3x3x1/` | `bash run.sh` | ok | l2-partial | spectral_weight.npy shape/sum metric in ref |
| B2 | `examples/unfold/Ce@BL-MoS2_3x3x1/` | `bash run.sh` | ok | experimental | sw.npy + awht.npy shapes in ref |
| B3 | `examples/band_reorder/` | `bash run.sh` | ok | experimental | multi-k reorder via wfc_r WAVECAR symlink; PS overlaps; see ASSUMPTIONS |
| B4 | `examples/procar/` | `bash run.sh` | ok | experimental | New: PROCAR orbital projections |
| B5 | `examples/hse_kpts/` | `bash run.sh` | ok | experimental | New: irreducible k-points (IBZ) |
| P1 | `examples/potplot/` | `bash run.sh` | ok | l2-partial | regenerates ti_pot.png from POTCAR (copied from projectors if needed) |
| P2 | `examples/projectors/` | `bash run.sh` | ok | l2-partial | Extend existing: nonlocal projectors |
| P3 | `examples/projectors/` | `bash run.sh` | ok | l2-partial | Extend existing: PAW Qij, nablaij |
| P4 | `examples/aewfc/co2/` | `bash run.sh` | ok | l2-partial | AE demo; requires pySBT; ref/ae_norm.txt |
| P5 | `examples/tdm/` | `bash run.sh` | skip | experimental | New: AE transition dipole |
| O1 | `examples/spinor/` | `bash run.sh` | ok | l2-partial | dumps in ispin2/soc_dump_work via patched vasp_std; spinormaker WAVECAR_spinor |
| O2 | `examples/spinor/` | `bash run.sh` | ok | l2-partial | spinormaker built WAVECAR_spinor; readable via vaspwfc(lsorbit=True) |
| O3 | `examples/spinor/` | `bash run.sh` | ok | experimental | dumps present; MAE helpers not separately gated |
| X1 | `examples/bsematrix/BP/` | `bash run.sh` | ok | l2-partial | counts lines in py_pw_only_both_AMAT.txt to ref |
| X2 | `examples/bsematrix/BP/` | `bash run.sh` | ok | quarantine | paw_* residual large; CLI default pw_only |
| X3 | `examples/bsematrix/BP/` | `bash run.sh` | ok | quarantine | finite-q residual; do not cite |
| X4 | `examples/wfull/` | `bash run.sh` | ok | experimental | New: screened potential (WFULL) |
| X5 | `examples/bseplot/` | `bash run.sh` | ok | l2-partial | Extend existing: BSEFATBAND / exciton BZ |
| X6 | `examples/bseplot/` | `bash run.sh` | skip | repro-pending | realspace needs WAVECAR not bundled (see docs/repro/X6.md) |
| D1 | `examples/nac/` | `bash run.sh` | ok | l2-partial | dual-frame CO2 md_frames (local); max|NAC|~2 |
| D2 | `examples/neb/` | `bash run.sh` | ok | experimental | New: NEB path PES with synthetic OUTCAR stubs |
| D3 | `examples/ewald/` | `bash run.sh` | ok | l2-partial | Extend existing: Ewald / Madelung |
