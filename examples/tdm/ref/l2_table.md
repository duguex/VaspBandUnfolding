# CO2 dipole L2-partial table

- workdir: `/home/duguex/VaspBandUnfolding/examples/tdm/vasp_optics/work`
- NELECT=16.0, nocc=8, nbands=24
- max |E_WAVECAR - E_OUTCAR| = 4.617e-05 eV → PASS (<1e-4 eV)
- HOMO→LUMO dark |r|_max = 2.478e-06 Debye → PASS (<1e-3)
- brightest |r|_max = 3.360e+00 Debye → PASS (>0.1)

| i | j | E_i (eV) | E_j (eV) | dE (eV) | |r|_max (Debye) |
|---:|---:|---:|---:|---:|---:|
| 6 | 9 | -12.387678 | -0.912540 | 11.475138 | 2.163428e+00 |
| 6 | 10 | -12.387678 | -0.423284 | 11.964394 | 2.622234e-07 |
| 6 | 11 | -12.387678 | -0.423284 | 11.964394 | 2.619662e-07 |
| 6 | 12 | -12.387678 | 0.608466 | 12.996144 | 1.309016e+00 |
| 6 | 13 | -12.387678 | 1.131860 | 13.519538 | 1.709717e-06 |
| 7 | 9 | -8.863004 | -0.912540 | 7.950463 | 2.478204e-06 |
| 7 | 10 | -8.863004 | -0.423284 | 8.439720 | 3.360386e+00 |
| 7 | 11 | -8.863004 | -0.423284 | 8.439720 | 2.290822e-01 |
| 7 | 12 | -8.863004 | 0.608466 | 9.471470 | 2.871665e-05 |
| 7 | 13 | -8.863004 | 1.131860 | 9.994863 | 2.928039e-01 |
| 8 | 9 | -8.863004 | -0.912540 | 7.950463 | 2.477511e-06 |
| 8 | 10 | -8.863004 | -0.423284 | 8.439720 | 2.290822e-01 |
| 8 | 11 | -8.863004 | -0.423284 | 8.439720 | 3.360386e+00 |
| 8 | 12 | -8.863004 | 0.608466 | 9.471470 | 2.871053e-05 |
| 8 | 13 | -8.863004 | 1.131860 | 9.994863 | 8.027162e-02 |

## Notes

- brightest pair: 8→11
- Im(ε) continuum onset is **not** used as a hard gate for this molecular supercell IPA spectrum.
- Length-gauge p–r for finite systems only (ASSUMPTIONS).

## Citation

- **l2-partial** if all three gates PASS.
- Not full L2 vs VASP element-wise optics matrix elements.

**Overall: PASS**
