# All-Electron Wavefunction Reconstruction (CO2)

Demonstrates all-electron (AE) wavefunction reconstruction from PAW
pseudo-wavefunction data using the spherical Bessel transform (`pySBT`).

## Feature IDs

| ID | Description |
|----|-------------|
| P4 | AE wavefunction: `aewfc.vasp_ae_wfc` reconstruction |

## Level

**L1 — partial.** The AE reconstruction code exists and runs, but the workflow
depends on the optional `pySBT` library. Without it, the runner skips cleanly.

## Citation

This demo follows the PAW all-electron reconstruction described in
the VASP AE-wavefunction post by Qijing Zheng. See the main project
[README](/README.md) for citation guidance on the base PAW implementation.

## Runner

```bash
bash run.sh        # requires pySBT; writes ref/co2_homo_aeps_wfc.png
```

Exit codes: `0` success, `2` missing data (no pySBT), `1` failure.
