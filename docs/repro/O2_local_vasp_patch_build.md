# Local VASP 5.4.4 + SOC dump patch (this machine)

## Layout (gitignored — do not commit sources)

```text
vasp.5.4.4.pl2.tgz                 # user-provided tarball (gitignored)
third_party/vasp.5.4.4.pl2/        # extracted + patched tree
third_party/vasp_patch_backups/    # original .F before patch
third_party/NAMDwithSOC/           # patch source clone
```

## Patch applied

From [ZhenfaZheng/NAMDwithSOC](https://github.com/ZhenfaZheng/NAMDwithSOC)  
`patches/soc_vasp_5.4.4/{main,paw,relativistic,stm}.F` → `third_party/vasp.5.4.4.pl2/src/`.

Verified strings in tree:

- `relativistic.F`: `OPEN(FILE='SocCar'...)`, `SocAllCar`, `SocRadCar`
- `stm.F`: `OPEN(... FILE='NormalCAR'...)`

Originals saved under `third_party/vasp_patch_backups/*.orig`.

## Build

```bash
cd third_party/vasp.5.4.4.pl2
# makefile.include already points at system OpenMPI/OpenBLAS/FFTW
make std -j$(nproc)    # and/or make ncl
# binaries: bin/vasp_std  bin/vasp_ncl (if built)
```

If link errors appear, adjust `makefile.include` library names for this host.

## After binary exists

1. Run a small SCF (prefer ncl + LSORBIT if required by your dump path) in a work dir with POSCAR/POTCAR/KPOINTS/INCAR.
2. Expect dumps: `SocCar`, `SocRadCar`, `NormalCAR` (and maybe `SocAllCar`).
3. Copy into `examples/spinor/ispin2/` with WAVECAR and run `spinormaker`.

Alternatively generate **NormalCAR only** without this binary:

```bash
rsgrad normalcar --wavecar WAVECAR --poscar POSCAR --potcar POTCAR -o NormalCAR
```

## License

VASP sources are proprietary. Keep them **out of git** (see root `.gitignore`).

## Verified on this host (2026-07-13)

Built:

- `third_party/vasp.5.4.4.pl2/bin/vasp_std`
- `third_party/vasp.5.4.4.pl2/bin/vasp_ncl`

MoSe2 collinear dumps (`examples/spinor/{spinless,ispin2}/soc_dump_work/`, gitignored):

- `WAVECAR`, `NormalCAR`, `SocCar`, `SocRadCar` written by **patched `vasp_std`**
- `spinormaker` produced `WAVECAR_spinor` (readable with `vaspwfc(..., lsorbit=True)`)
- `examples/spinor/run.sh` → **PASS**; smoke **19/19**

Regenerate:

```bash
VASP=third_party/vasp.5.4.4.pl2/bin/vasp_std
# from examples/spinor/ispin2/soc_dump_work with POSCAR/POTCAR/KPOINTS/INCAR
mpirun -np 8 $VASP
spinormaker --mixwave-ibs 105 107 109 111 113 --correct-kpts 1 --full-kpts
```

## Verified MoSe2 spinor path (this host)

1. Collinear `vasp_std` dumps under `examples/spinor/{spinless,ispin2}/soc_dump_work/` (gitignored).
2. `spinormaker` → `WAVECAR_spinor` (readable with `vaspwfc(..., lsorbit=True)`).
3. Optional SCF ncl: set `REGEN_NCL_REF=1` when running `scripts/regen_spinor_mose2.sh`.
4. Eigenvalue compare: `examples/spinor/ref/spinor_vs_ncl.txt` (MAE ~ few meV — second-variation ≠ SCF identity).

One-shot:

```bash
bash scripts/regen_spinor_mose2.sh
bash examples/spinor/run.sh
```
