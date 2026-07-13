# O2: How to produce Soc\* / NormalCAR (actionable)

VaspBandUnfolding **does not** ship a patched VASP. Related public sources:

| Source | Role |
|---|---|
| [ZhenfaZheng/NAMDwithSOC](https://github.com/ZhenfaZheng/NAMDwithSOC) `patches/soc_vasp_5.4.4/` | VASP **5.4.4** Fortran patches that **write** `SocCar`, `SocRadCar`, `SocAllCar`, `NormalCAR` |
| [Ionizing/rsgrad](https://github.com/Ionizing/rsgrad) `rsgrad normalcar` | Build **NormalCAR** from `WAVECAR`+`POSCAR`+`POTCAR` **without** a VASP patch |
| [realxiangjiang/paraHFNAMD](https://github.com/realxiangjiang/paraHFNAMD) | C++ NAMD/SOC code that **reads** dumps (same lineage as `spinor.py` / `soc.cpp`) |
| [QijingZheng/Hefei-NAMD](https://github.com/QijingZheng/Hefei-NAMD) | Parent NAMD project; **no** Soc\* writers in public tree |

## Files needed by `spinormaker`

```text
WAVECAR      # standard SCF (LWAVE=.TRUE.), scalar or ISPIN=2
NormalCAR    # PAW projector coeffs (patch VASP or rsgrad)
SocCar       # SOC matrix on AE partial-wave basis (patch VASP)
SocRadCar    # radial SOC factors (patch VASP)
```

## Path A — NormalCAR only (no VASP source)

```bash
# install rsgrad (binary from releases, or:)
cargo install --git https://github.com/Ionizing/rsgrad

cd /path/with/WAVECAR_POSCAR_POTCAR
rsgrad normalcar --wavecar WAVECAR --poscar POSCAR --potcar POTCAR -o NormalCAR
```

## Path B — SocCar / SocRadCar (needs licensed VASP 5.4.4 source)

1. Obtain **legal** VASP 5.4.4 sources (not on GitHub).
2. Clone patch set:
   ```bash
   git clone https://github.com/ZhenfaZheng/NAMDwithSOC
   # patches in: NAMD with SOC/patches/soc_vasp_5.4.4/
   #   main.F  paw.F  relativistic.F  stm.F
   ```
3. Merge/replace corresponding files in the VASP 5.4.4 tree (diff carefully; keep a backup).
4. Recompile VASP; use that binary for SOC-related runs.
5. Expect dumps such as `SocCar`, `SocRadCar` (and possibly `NormalCAR` / `SocAllCar`) in the run directory.
6. See also tutorials under `NAMDwithSOC/tutorials/` (PDF/PPT).

**Without VASP sources, Path B cannot be completed** — the patch alone is not a full binary.

## Path C — skip spinormaker; use official ncl WAVECAR

```python
from vaspwfc import vaspwfc
w = vaspwfc("WAVECAR", lsorbit=True)
```

This validates **reading** SOC spinor WAVECAR, not the spinormaker assembly path.

## After you have the four files

```bash
cp WAVECAR NormalCAR SocCar SocRadCar \
  /path/to/VaspBandUnfolding/examples/spinor/ispin2/
cd /path/to/VaspBandUnfolding/examples/spinor/ispin2
# adjust names if needed: NormalCar -> NormalCAR
spinormaker --mixwave-ibs 211 213 215 217 219 --correct-kpts 1
```

## Policy

Do **not** open PRs to upstream `QijingZheng/VaspBandUnfolding` for this workflow unless explicitly requested.
Work on personal fork only.
