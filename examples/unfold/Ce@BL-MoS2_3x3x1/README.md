# Band Unfolding: Ce@BL-MoS2 3x3x1

Spectral-weight band unfolding for Ce-doped bilayer MoS2 with atomic-orbital
projected weights.

## Feature IDs

| ID | Description |
|----|-------------|
| B2 | Unfold + atomic weights: `unfold.spectral_weight` with PROCAR weights |

## Level

**L1 — partial.** The npy archives are available for C1 validation.
Full end-to-end rebuild from WAVECAR + PROCAR requires a VASP run.

## Citation

Follows the same unfolding method as B1 (Popescu & Zunger 2010).
Atomic weight projection is described in the `unfold` module documentation.

## Runner

```bash
bash run.sh        # requires sw.npy or awht.npy; writes ref/unfold_data.txt
```

Exit codes: `0` success, `2` missing data (no .npy files), `1` failure.
