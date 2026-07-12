# Ewald / Madelung Summation

Compute Madelung constants for several standard crystal structures (NaCl, CsCl,
ZnO, TiO2, CaF2) using the Ewald summation method.

## Feature IDs

| ID | Description |
|----|-------------|
| D3 | Ewald / Madelung sum: compute electrostatic Madelung constants via Ewald summation |

## Level

**L2 — experimental.** The `ewald.py` module and the `madelung.py` demo run but
are not yet hardened as a C2 example.

## Citation

The Ewald summation follows the standard formulation (Ewald 1921). See the main
project [README](/README.md) for repository-level citation.

## Runner

```bash
bash run.sh        # writes ref/madelung.out
```
