# wfc_r: Real-Space Pseudo-Wavefunction

Compute and visualise the real-space pseudo-wavefunction from a VASP WAVECAR via FFT.

## Feature IDs

| ID | Description |
|----|-------------|
| W1 | WAVECAR I/O: read plane-wave coefficients, band energies, occupations |
| W2 | G-vector set / cutoff sphere: transform reciprocal-plane-wave to real space |
| W3 | Real-space pseudo-wavefunction: `wfc_r()` FFT and VESTA-format export |

## Level

**L2 — experimental.** Core `wfc_r()` machinery works for standard (nspin=1) VASP
WAVECARs. Extended support for non-collinear (nspin=4) with SOC, and gamma-only
formats, is in progress.

## Citation

See the main project [README](/README.md) for citation guidance. The `wfc_r`
implementation follows standard plane-wave FFT reconstruction. No separate
publication exists for this demo — cite the base reference.

## Runner

```bash
bash run.sh        # requires WAVECAR; writes ref/norm.txt
```
