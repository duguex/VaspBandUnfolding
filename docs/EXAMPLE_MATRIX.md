# Example Matrix

| ID | Slug path | Runner | C1 | C2 | Notes |
|---|---|---|---|---|---|
| W1 | `examples/wfc_r/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: WAVECAR I/O, gamma-only, ncl |
| W2 | `examples/wfc_r/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: G-vector set / cutoff sphere |
| W3 | `examples/wfc_r/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: real-space PS wavefunction |
| W4 | `examples/tdm/` | `bash run.sh` | ok | todo | New: transition dipole matrix elements (PS) |
| W5 | `examples/ipr/` | `bash run.sh` | skip | todo | not scaffolded; New: inverse participation ratio |
| W6 | `examples/elf_test/` | `bash run.sh` | ok | todo | ELF from WAVECAR; ELFCAR metric in ref |
| B1 | `examples/unfold/sup_3x3x1/` | `bash run.sh` | ok | todo | spectral_weight.npy shape/sum metric in ref |
| B2 | `examples/unfold/Ce@BL-MoS2_3x3x1/` | `bash run.sh` | ok | todo | sw.npy + awht.npy shapes in ref |
| B3 | `examples/band_reorder/` | `bash run.sh` | ok | todo | runner validates WAVECAR existence; reorder TBD |
| B4 | `examples/procar/` | `bash run.sh` | skip | todo | not scaffolded; New: PROCAR orbital projections |
| B5 | `examples/hse_kpts/` | `bash run.sh` | skip | todo | not scaffolded; New: irreducible k-points (IBZ) |
| P1 | `examples/potplot/` | `bash run.sh` | ok | todo | regenerates ti_pot.png from POTCAR (copied from projectors if needed) |
| P2 | `examples/projectors/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: nonlocal projectors |
| P3 | `examples/projectors/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: PAW Qij, nablaij |
| P4 | `examples/aewfc/co2/` | `bash run.sh` | ok | todo | AE wavefunction plot; exit 2 if pySBT missing |
| P5 | `examples/tdm/` | `bash run.sh` | skip | todo | not scaffolded; New: AE transition dipole |
| O1 | `examples/spinor/` | `bash run.sh` | ok | todo | SocCar/NormalCar check; exit 2 without Soc files |
| O2 | `examples/spinor/` | `bash run.sh` | ok | todo | shares O1 runner; Soc files required |
| O3 | `examples/spinor/` | `bash run.sh` | ok | todo | shares O1 runner; exit 2 if Soc files missing |
| X1 | `examples/bsematrix/BP/` | `bash run.sh` | ok | todo | counts lines in py_pw_only_both_AMAT.txt to ref |
| X2 | `examples/bsematrix/BP/` | `bash run.sh` | ok | todo | shares X1 runner; AMAT text artifacts present |
| X3 | `examples/bsematrix/BP/` | `bash run.sh` | ok | todo | shares X1 runner; finite-q AMATs in directory |
| X4 | `examples/wfull/` | `bash run.sh` | skip | todo | not scaffolded; New: screened potential (WFULL) |
| X5 | `examples/bseplot/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: BSEFATBAND / exciton BZ |
| X6 | `examples/bseplot/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: exciton real-space density |
| D1 | `examples/nac/` | `bash run.sh` | skip | todo | not scaffolded; New: non-adiabatic couplings |
| D2 | `examples/neb/` | `bash run.sh` | skip | todo | not scaffolded; New: NEB path plot |
| D3 | `examples/ewald/` | `bash run.sh` | ok | todo | not scaffolded; Extend existing: Ewald / Madelung |
