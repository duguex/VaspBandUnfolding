# Reproduction Recipes

Heavy VASP inputs and local binaries are **not** stored in git. Recipes:

| ID | Doc | Status |
|---|---|---|
| **O2** | [`O2_spinor_patch.md`](O2_spinor_patch.md) | Public patch + `rsgrad` NormalCAR |
| **O2 local** | [`O2_local_vasp_patch_build.md`](O2_local_vasp_patch_build.md) | This host: patched 5.4.4 build + MoSe2 dump verified |
| **O2 regen** | `scripts/regen_spinor_mose2.sh` | One-shot dump + spinormaker; `REGEN_NCL_REF=1` optional |
| **W4** | [`W4_dipole.md`](W4_dipole.md) + `examples/tdm/vasp_optics/` | Local LOPTICS workdir (gitignored); `run_l2.sh` |
| **X6** | [`X6_exciton_rs.md`](X6_exciton_rs.md) | Needs matching BSE WAVECAR; `run_realspace.sh` |
| **X1** | [`X1_bse_bp.md`](X1_bse_bp.md) | BP text refs; full rebuild is multi-step GW/BSE |
| **B1** | [`B1_unfold.md`](B1_unfold.md) | Outline only |

## Gitignored local trees (regenerate, do not commit)

```text
third_party/vasp.5.4.4.pl2/          # sources + vasp_std / vasp_ncl
examples/spinor/**/soc_dump_work/
examples/spinor/**/ncl_ref_work/
examples/tdm/vasp_optics/work/
examples/nac/md_frames/
```

## Policy

Personal fork only; **no upstream PRs** unless requested.
