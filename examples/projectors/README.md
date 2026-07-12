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
bash run.sh        # requires lreal_false/cproj.npy; writes ref/cproj_max.txt
```
