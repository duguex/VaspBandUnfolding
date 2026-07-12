# Projectors: PAW Non-Local Projector Overlap

Demonstrates reciprocal-space (`lreal_false`) and real-space (`lreal_true`)
PAW non-local projector coefficients and their agreement with VASP's NormalCar
cproj output.

## Feature IDs

| ID | Description |
|----|-------------|
| P2 | Nonlocal projectors: compute `beta = <p_i|psi>` in reciprocal space |
| P3 | PAW Qij, nablaij: all-electron inner-product corrections |

## Level

**L2 — experimental.** The projection code runs but is not yet validated across
different pseudopotential sets. The `lreal_false` directory contains the primary
C1 runner. Real-space projector tests in `lreal_true` are available but not
included in the default runner.

## Citation

See the main project [README](/README.md) for citation of the PAW projector
implementation. The underlying formalism follows Bloechl (1994) and Kresse &
Joubert (1999).

## Runner

```bash
bash run.sh        # requires lreal_false/cproj.npy; writes ref/cproj_max.txt and ref/qij_norm.txt
```

### Output files

| File | Source | Description |
|------|--------|-------------|
| `ref/cproj_max.txt` | `run_check.py` | Max deviation between computed and VASP cproj (P2) |
| `ref/qij_norm.txt` | `run_qij.py` | Frobenius norm of PAW Qij matrix per element (P3) |

The **P3** target (`run_qij.py`) reads PAW partial-wave data from the POTCAR to
compute the on-site overlap-correction matrices \(Q_{ij}\) and reports their
Frobenius norms. No WAVECAR is required for this step.
