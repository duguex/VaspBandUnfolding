# Band Unfolding: Si 3x3 Supercell

Demonstrates spectral-weight-based band unfolding from a supercell
calculation to the primitive Brillouin zone.

## Feature IDs

| ID | Description |
|----|-------------|
| B1 | Band unfolding EBS: `unfold.spectral_weight` from npy archive |

## Level

**L1 — partial.** The spectral weight archive is available for C1 validation.
Full end-to-end rebuild from WAVECAR requires a VASP supercell run.

## Citation

Band unfolding follows the method of Popescu & Zunger (2010)
and Allen et al. (2013). See the project README for the base reference.

## Runner

```bash
bash run.sh        # requires spectral_weight.npy; writes ref/sw_shape.txt
```

Exit codes: `0` success, `2` missing data (no spectral_weight.npy), `1` failure.
