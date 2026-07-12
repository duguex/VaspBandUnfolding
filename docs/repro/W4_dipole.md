# W4/P5: Transition Dipole — L2 Benchmark Requirements

## Current status

W4 (PS path) and P5 (AE one-center correction) are both at **L0–L1**.
Neither has been validated against a VASP reference optical calculation.

## What an L2 benchmark needs

A credible L2 gate for the transition dipole requires a VASP OPTICS
calculation on a **small, well-understood system** (e.g. a molecule in
a large box or a narrow-gap semiconductor with a known absorption
onset).  The workflow is:

1.  **VASP ground-state SCF** — converged `WAVECAR` and `CHGCAR`.
2.  **VASP OPTICS run** (`LOPTICS=.TRUE.`) — produces `WAVEDER` and
    the frequency-dependent dielectric function in `OUTCAR`.
3.  **Python dipole extraction** — `vaspwfc.get_dipole_mat()` on the
    same `WAVECAR`/`WAVEDER`.
4.  **Comparison** — cross-check oscillator strengths or the imaginary
    dielectric function \(\varepsilon_2(\omega)\) between VASP and
    Python at a set of well-separated band pairs.

### Particular challenges

- The **p–r relation** is approximate in periodic solids — the position
  operator is ill-defined in Bloch states (PRB 87, 125301).
- **Degenerate bands** (\(E_n \approx E_m\)) are zeroed by the current
  implementation — this needs a degenerate perturbation treatment
  before claiming L2.
- For the **AE path (P5)**, the PAW one-center nabla correction must
  also be exercised and compared against the VASP all-electron optical
  matrix.

## Data requirements (crisp)

| Artifact | Needed for |
|----------|------------|
| `WAVECAR` | PS dipole (W4) |
| `WAVEDER` | Velocity-gauge matrix elements |
| `OUTCAR` | Band energies, optics output |
| `POSCAR` / `KPOINTS` | System definition |
| `POTCAR` | PAW partial waves (P5 only) |

## Recommendation

Do **not** promote W4 or P5 to L2 until the benchmark above is
completed and documented in this directory.  Keep both at L0–L1
experimental for seminars.
