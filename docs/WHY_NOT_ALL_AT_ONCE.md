# Why not everything finishes in one shot

This is an engineering/physics reality check for secondary development (G1+G2), not a lack of permission.

## What “all done” means here

| Layer | Done means |
|---|---|
| C1 smoke | Every science ID runs or **explicitly skips** with a reason |
| C2 G1 | Claimed paths are **L2** (same-input vs VASP/reference) or **quarantined** |
| Research complete | Open residuals (BSE PAW/q, SOC dumps, …) fixed or abandoned with evidence |

C1 is largely done (smoke ≈ 18 pass / 1 skip). **C2 G1 is not fully done.**

## Hard limits (crisp does not remove them)

### 1. `SocCar` / `SocRadCar` are not stock VASP products

`spinormaker` needs **`WAVECAR` + `NormalCAR` + `SocCar` + `SocRadCar`**.

- `NormalCAR`-like projector dumps appear in some setups (we already have NormalCAR under `examples/projectors/`).
- **`SocCar` / `SocRadCar` come from a specialized SOC / spinor dump path** (project README: “spinor patch” style workflow), **not** from a normal `crisp submit` of scalar/ISPIN=2 INCAR.

So: crisp can re-run SCF for MoSe2 spinless/ispin2 WAVECARs (already done), but **cannot magically invent Soc\* files** without the matching VASP binary/workflow that writes them.

### 2. Full BSE L2 is a multi-day pipeline

True matrix parity needs SCF → WAVEDER → GW → BSE (+ optional FAST_AUG dumps).  
`examples/bsematrix/BP` already holds **text AMAT references**; regenerating from scratch is a **campaign**, not one job.

### 3. Scientific L2 needs tolerances and judgment

Even with crisp outputs, “PASS L2” requires agreed thresholds (e.g. dipole vs OPTICS). That is a **decision**, not pure automation.

### 4. Throughput / job cap

Cluster side may only allow a small number of concurrent crisp jobs. Work is **serialized** by queue, not by “agent willingness.”

## Soft limits (can push in one session)

- Install optional deps (`pySBT`, `spglib`)
- Fix library bugs blocking demos (`get_kpath` kbound)
- Wire examples to existing WAVECARs (band_reorder, nac smoke)
- Submit **standard** VASP jobs (LOPTICS, ELF, bands) for new L2 tables
- Keep quarantine honest so papers do not over-claim

## Current skip / residual map

| Item | Blocker | crisp help? |
|---|---|---|
| spinor full O1–O2 | SocCar/SocRadCar | Only if your VASP build writes them |
| dipole true L2 | OPTICS reference job + comparison script | **Yes** (LOPTICS run) |
| ELF vs ELFCAR | VASP LEPSILON/ELF job | **Yes** if tags supported |
| BSE paw/q parity | Algorithm + long GW/BSE | Partial (long campaign) |
| NAC real MD | Two MD WAVECARs | Yes (MD traj) — separate project |

## Policy

- Push only to **personal fork** (`fork`); **never** open PRs to upstream unless you reverse that policy.
