# Design: All Components Runnable + Example Showcase (G1)

**Date:** 2026-07-13  
**Status:** Approved for implementation planning (C1→C2; G1 bar)
**Goals alignment:** [`docs/GOALS.md`](../../GOALS.md) G1 (scientific soundness) + G2 (reusable components)  
**Inventory:** [`FEATURES.md`](../../../FEATURES.md) · Assumptions: [`docs/ASSUMPTIONS.md`](../../ASSUMPTIONS.md) · Roadmap: [`docs/ACADEMIC_ROADMAP.md`](../../ACADEMIC_ROADMAP.md)

---

## 1. Problem

Not every feature ID has:

- a runnable demonstration,
- stored showcase output,
- or a path to paper-grade (L2) evidence.

Secondary development requires **every science component** to be demonstrable and, where claimed for publication use, **scientifically validated**; incomplete modes must be explicitly quarantined.

---

## 2. Success criteria (agreed)

| Choice | Value |
|---|---|
| Bar | **G1 / paper-facing** — not mere smoke-only forever |
| Delivery | **Two phases: C1 → C2** |
| Approach | Unified `examples/<slug>/` template + matrix registry (not single cookbook / not notebook-first) |
| Runtime | Python ≥3.10, mainstream numpy/scipy/matplotlib/ase only |

### Phase C1 — “Has been run + has a showcase”

For each **science** feature ID (W*, B*, P*, O*, X*, D*):

1. An example directory exists (may share a folder with sibling IDs if README lists all IDs covered).
2. One command runs successfully when required inputs are present: `bash run.sh` or `python run.py`.
3. Run produces or validates at least one artifact under `ref/` (png, txt, small npy, or short log).
4. README states: Feature ID(s), Level, inputs, command, **citation allowed? (yes / experimental only / no)**.
5. Root smoke driver discovers all C1 examples; missing heavy data → **explicit skip** recorded in the matrix (not silent pass).

**Infrastructure I1–I4:** covered by `tests/test_infra_*.py` (pytest green = “run”), no mandatory science example.

**CLI C1–C7:** need not each own a directory; must be invoked from the owning feature example’s `run.sh` at least once where applicable.

### Phase C2 — “G1 ready or quarantined”

For each science ID:

- **Claimed for papers / default use:** Level ≥ **L2** with in-repo table/fixture **or** `docs/repro/<ID>.md` + pinned expected numbers.
- **Not L2:** marked `experimental` or `quarantine` in FEATURES + example README + ASSUMPTIONS; default API/docs must not present them as production-ready.
- Matches GOALS “definition of done” for G1+G2-ready components where Level is L2.

---

## 3. Non-goals

- Replacing VASP.
- Beginner curriculum / lesson plans.
- Committing full production WAVECARs / GW trees into git.
- L3 multi-system literature proof for every ID in C2.
- Supporting obsolete Python/numpy stacks.
- Large architectural rewrite of `vaspwfc` / packaging layout (flat `py-modules` stays).

---

## 4. Architecture

```
examples/
  _template/                 # copy-paste skeleton (optional, tracked)
    README.md
    run.sh
    ref/.gitkeep
  <slug>/                    # one slug per demo unit
    README.md                # contract + Level + IDs
    run.sh | run.py          # single entry
    ref/                     # showcase + regression goldens (small)
    # inputs: POSCAR, tiny WAVECAR, … or document external path

docs/
  EXAMPLE_MATRIX.md          # ID → path → C1/C2 status → skip reason
  repro/<ID>.md              # heavy VASP / crisp recipes (C2)

scripts/
  smoke_examples.py          # discover + run examples; honor SKIP/REQUIRES

tests/
  test_infra_*.py            # I1–I4
  test_example_matrix.py     # matrix completeness vs FEATURES science IDs
  test_l2_*.py               # optional C2 gates (e.g. ewald, projectors)

FEATURES.md                  # Level / status updated as gates land
```

### Example unit contract

| File | Rules |
|---|---|
| `README.md` | Required sections: IDs, Level, Purpose, Inputs, Command, Expected outputs, Citation policy, Assumptions links |
| `run.sh` / `run.py` | Exit 0 on success; exit 2 if required data missing (smoke treats as skip); write under `ref/` or compare to goldens |
| `ref/` | Small only; large binaries documented as external |

### Data policy

| Data class | Storage |
|---|---|
| Text refs, tiny npy, PNG | git |
| Mini WAVECAR / clipped NormalCar for CI | git if small enough |
| Full supercell WAVECAR, Soc\*, GW/BSE trees | external + `docs/repro/<ID>.md` + optional `crisp submit` |

### Smoke driver behavior

1. Read `docs/EXAMPLE_MATRIX.md` (or generated YAML) listing example paths.  
2. For each entry: run command with timeout.  
3. Classify: **pass** / **skip (missing data)** / **fail**.  
4. Exit non-zero only on **fail**.  
5. Print summary table for CI logs.

---

## 5. Mapping: Feature ID → example slug (target)

| ID(s) | Target slug | C1 strategy | C2 strategy |
|---|---|---|---|
| W1–W3 | `wfc_r` (extend) | Existing WAVECAR + strengthen `run.py`/`ref` | Norm/G-count vs OUTCAR notes; optional mini fixtures for γ/ncl if available |
| W4, P5 | `tdm` (**new**) | Synthetic small system or molecule WAVECAR + `tdmplot`/`get_dipole_mat` → `ref/tdm.txt` | L2 vs VASP OPTICS or finite-molecule reference; document p–r limits |
| W5 | `ipr` (**new**) | Analytic grid field **or** wfc_r-derived IPR → `ref/ipr.txt` | Analytic limits + one defect case |
| W6 | `elf_test` (extend) | Existing run → `ref/` | Validate vs VASP ELFCAR **or** permanent experimental quarantine |
| B1 | `unfold/sup_3x3x1` (extend) | Prefer npy-based plot path always runnable; optional WAVECAR recompute | Weight sum rules + repro doc |
| B2 | `unfold/Ce@BL-MoS2_3x3x1` | `plt_unf.py` wrapped by `run.sh` | Document PROCAR alignment |
| B3 | `band_reorder` (extend) | Add `run.py` + WAVECAR (mini or external) | Overlap matrix dump; failure cases |
| B4 | `procar` (**new**) | Tiny/clipped PROCAR parse + table dump | Column check vs VASP file |
| B5 | `hse_kpts` (**new**) | `get_ir_kpts` on POSCAR → weights file | Compare to IBZKPT when available; declare spglib optional |
| P1 | `potplot` (extend) | `run.sh` calling `potplot` or library plot save | Regen script not image-only |
| P2 | `projectors` (extend) | Existing kaka scripts → formal `run.sh` + ref | Keep NormalCar L2 gate |
| P3 | `projectors` or `paw_matrices` | Dump Qij/nablaij norms to `ref/` | Identity checks / documentation |
| P4 | `aewfc/co2` (extend) | Formal run + ref metrics | Pin pySBT; AE–PS metrics |
| O1–O2 | `spinor` (extend) | Document Soc\* requirements; run spinormaker when data present; else skip with recipe | End-to-end mini case + README snapshot numbers |
| O3 | `spinor` or `soc_mae` | Toy call path if data allows; else skip + recipe | Formula + toy numbers in ref |
| X1–X2 | `bsematrix/BP` (extend) | Compare shipped AMAT text (no full rebuild required for C1) | `pw_only` L2 gate; quarantine weak modes |
| X3 | `bsematrix/BP` | Showcase qext artifacts | Remain quarantine until L2 recovered |
| X4 | `wfull` (**new** mini) | Golden tiny Fortran record fixture | Round-trip test |
| X5 | `bseplot` (extend) | `bseplot bz` → ref png or weight table | Deterministic weight table preferred over PNG hash |
| X6 | `bseplot` (extend) | realspace when WAVECAR present; else skip + PNG showcase of prior | Phase/OUTCAR repro doc |
| D1 | `nac` (**new**) | Two-frame mini WAVECARs or skip + synthetic overlap demo if feasible | Phase convention + finite-diff note |
| D2 | `neb` (**new**) | Minimal multi-image OUTCAR stubs → `nebplot` | Energy table ref |
| D3 | `ewald` (extend) | `madelung.py` → `ref/madelung.out` | Diff against golden |
| I1–I4 | `tests/` only | pytest | pytest |
| C1–C7 | via parent examples | Invoke once in parent `run.sh` | Packaging: register `bsematrix` or document only |

---

## 6. Phase C1 workstreams (implementation plan will task-split)

1. **Scaffold:** `_template/`, `docs/EXAMPLE_MATRIX.md`, `scripts/smoke_examples.py`, `tests/test_example_matrix.py`.  
2. **Upgrade existing strong demos:** wfc_r, projectors, ewald, bseplot bz, aewfc, elf_test, unfold (npy path), bsematrix BP (text compare).  
3. **Fill missing demos:** tdm, ipr, procar, hse_kpts, nac, neb, wfull fixture, band_reorder/potplot run scripts.  
4. **Conditional demos:** spinor, bseplot realspace — skip-with-repro until data available.  
5. **FEATURES.md:** add “Example path” consistency; citation policy column optional.

---

## 7. Phase C2 workstreams

1. **Promote L2:** ewald golden, projectors, wfc smoke, BP `pw_only`, bseplot weights, dipole suite, unfold protocol.  
2. **Quarantine with teeth:** FEATURES Level + example README + default CLI help text for X2 residual modes, X3, W6 if unvalidated.  
3. **Repro docs + crisp:** B1, O2, X1 full rebuild, X6.  
4. **Packaging honesty:** optional deps (`spglib`, `pySBT`); C7 install policy.  
5. **Per-component citation stub** (one paragraph) in each L2 README.

---

## 8. Testing & quality gates

| Gate | When |
|---|---|
| `pytest tests/test_infra_*.py` | Always (I1–I4) |
| `pytest tests/test_example_matrix.py` | Every science ID appears in matrix |
| `python scripts/smoke_examples.py` | C1 complete; allows skips |
| L2 scripts/tests | C2 per-ID as promoted |
| No silent default to quarantined modes | C2 |

---

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Heavy data blocks “all green smoke” | Explicit skip + matrix; separate “full” profile later |
| Fake L2 by only shipping old text | C2 requires stated VASP version + method to regenerate |
| Scope explosion | C1 first closes “no example”; C2 prioritizes P0 IDs (dipole, BSE boundaries, core IO) |
| pySBT/spglib missing | optional-dep skip with clear message |

---

## 10. Approval record

| Decision | Selection |
|---|---|
| Done bar | G1 paper-facing |
| Phasing | C1 then C2 |
| Layout | Per-slug examples + matrix + smoke |
| Approaches rejected | Single cookbook; notebook-first |

---

## 11. Implementation plan

Detailed tasks: [`docs/superpowers/plans/2026-07-13-all-components-run-and-examples.md`](../plans/2026-07-13-all-components-run-and-examples.md)

Execute with **subagent-driven-development** (recommended) or **executing-plans**.

---

## 12. Spec self-review

| Check | Result |
|---|---|
| Placeholders | None intentional; IDs fully listed |
| Consistency | Aligns with GOALS G1/G2, FEATURES IDs, ASSUMPTIONS honesty |
| Scope | Large but phased: C1 tasks 1–9, C2 tasks 10–15 |
| Ambiguity | Citation ternary and skip vs fail defined |
