# Remaining work

**Audience:** maintainers of this personal fork (`duguex/VaspBandUnfolding`).  
**Branch tip (when written):** `feature/c1-c2-examples`  
**Live snapshot:** [`STATUS.md`](STATUS.md) · **What you may claim:** [`CITATION_POLICY.md`](CITATION_POLICY.md) · **IDs:** [`FEATURES.md`](../FEATURES.md)

This file lists **what is still open**, with enough detail to schedule work without re-deriving context from chat history.  
It is **not** a claim that unfinished items are blocked forever—only that they are not done yet.

**Last verification baseline (update when you re-run):**

```text
python scripts/smoke_examples.py          → expect all matrix “ok” slugs to pass when local dumps exist
PYTHONPATH=. python -m pytest tests/ -q   → all unit tests green
```

---

## 1. How to read this document

| Label | Meaning |
|---|---|
| **Priority** | P0 = do soon if polishing the fork; P1 = next scientific milestone; P2 = nice-to-have / long horizon |
| **Effort** | S = hours; M = days; L = weeks+ or cluster campaign |
| **Blocker** | What stops a one-session finish |
| **Done means** | Observable acceptance criterion (not “code exists”) |
| **Out of scope** | Explicit non-goals unless policy changes |

**Policy that still applies**

- Development is **local + personal fork only**. Do **not** open PRs against upstream `QijingZheng/VaspBandUnfolding` unless the user explicitly reverses that rule.
- Do **not** commit VASP sources, large WAVECARs, or proprietary binaries (see root `.gitignore` and [`repro/`](repro/README.md)).

---

## 2. Already done (do not re-plan as “remaining”)

These are closed enough for C1 smoke and honest l2-partial citation. Details live in STATUS / FEATURES.

| Area | Where |
|---|---|
| Feature IDs, goals, assumptions, citation labels | `FEATURES.md`, `docs/GOALS.md`, `docs/ASSUMPTIONS.md`, `docs/CITATION_POLICY.md` |
| Example matrix + smoke runner | `docs/EXAMPLE_MATRIX.md`, `scripts/smoke_examples.py` |
| Unit / residual tests | `tests/` (incl. BSE CLI defaults, AMAT off-diag residuals, WAVEDER shapes) |
| Patched VASP 5.4.4 + MoSe2 Soc\* dumps + spinormaker path | `docs/repro/O2_local_vasp_patch_build.md`, `scripts/regen_spinor_mose2.sh` |
| CO2 LOPTICS gates (PS dipole selection rules) | `examples/tdm/ref/l2_*` |
| WAVEDER binary reader | `waveder.py`, `examples/tdm/compare_waveder.py` |
| AE/PAW dipole path exercised vs CDER (not element-wise L2) | `examples/tdm/compare_ae_waveder.py` |
| ELF vs ELFCAR gate | `examples/elf_test/` |
| Dual-frame NAC | `examples/nac/` (`md_frames/` gitignored) |
| BSE CLI default `pw_only`; paw/q marked quarantine | `bsematrix.py`, BP README |
| X6 realspace pipelines (CO2 + reduced MoSe2 recompute) | `examples/bseplot/co2_demo/`, `examples/bseplot/mose2_recompute/` |

---

## 3. Open scientific milestones

### 3.1 Dipole / optics: match VASP WAVEDER CDER (W4 / P5)

| Field | Content |
|---|---|
| **Problem** | VASP `WAVEDER` stores `CDER = −⟨r⟩` from the **optics k-derivative** path (PAW-complete). PyVaspWfc uses **momentum + molecular p–r** for both PS (`vaspwfc.get_dipole_mat`) and AE (`aewfc.get_dipole_mat`). On CO2, AE differs from PS (one-center terms fire) but **neither** matches CDER element-wise. |
| **Priority** | P1 |
| **Effort** | L (research + careful unit/phase/PAW audit) |
| **Blocker** | Physical path mismatch, not missing files (local `WAVECAR`+`WAVEDER`+`POTCAR` already exist under `examples/tdm/vasp_optics/work/`, gitignored). |
| **Done means** | Documented conversion (or new API) such that for a defined band window, `max‖r_py − r_CDER‖` (or equivalent velocity form) falls under an explicit tolerance **or** a written proof that p–r cannot equal CDER and citation stays “use CDER as reference only”. |
| **Concrete next steps** | 1) Map VASP `CDER` / velocity formulas in `linear_optics.F` to code symbols. 2) Compare `get_moment_mat` (AE) to energy×CDER with full unit table. 3) If still wrong, implement optics-consistent matrix elements or stop claiming length-gauge parity. 4) Extend `compare_ae_waveder.py` / tests with the chosen observable. |
| **Must not claim until done** | “Agrees with VASP WAVEDER element-wise.” |

---

### 3.2 BSE `paw_*` and finite-q out of quarantine (X2 / X3)

| Field | Content |
|---|---|
| **Problem** | Off-diagonal AMAT residuals vs VASP BP tables are **regression-tested** and non-negligible for direct / both / finite-q. Exception: **exchange-only + `paw_full`** is *better* than `pw_only` for kernel residual, but eigenvalue / direct / q paths are not citation-grade. Work is **explicitly deferred**. |
| **Priority** | P1 (hard); currently **parked** |
| **Effort** | L |
| **Blocker** | Algorithm + VASP dump completeness (`BSE_*_FOCK.bin`, WFULL/response, q conventions), not missing residual tables. |
| **Done means** | For each mode/channel you want to un-quarantine: residual table + eigenvalue MAE within agreed bounds vs BP (or a new same-input suite), CLI default policy updated, CITATION_POLICY/FEATURES flipped off **quarantine**. |
| **Concrete next steps** | 1) Keep `tests/test_bse_amat_residuals.py` green as floor. 2) Bisect **direct** residual structure (worst entries). 3) Audit finite-q pair indexing / head of Coulomb / SETPHASE. 4) Only then change citation labels. |
| **Evidence already in-repo** | `examples/bsematrix/BP/README.md` AMAT summary + residual-structure note. |
| **Must not claim until done** | “Production BSE kernel for paw modes / finite-q.” |

---

### 3.3 MoSe2 production BSE parity for X6 (bundled fatband)

| Field | Content |
|---|---|
| **Problem** | Bundled `examples/bseplot/BSEFATBAND` (+ comparison PNGs) come from a **large** VASP BSE (historically dense k / high NBANDS / GW-class setup). We added a **reduced recompute** (`mose2_recompute/`: 6×6×1 SCF → `bsematrix` → realspace) that proves the **pipeline**, not bit-identity with the bundled VASP fatband. |
| **Priority** | P1 if papers need those PNGs; else P2 (pipeline already demos X6). |
| **Effort** | L (cluster time + disk) |
| **Blocker** | Matching production **WAVECAR** (and usually GW/BSE run tree) not in git; full remake is a multi-step VASP campaign. |
| **Done means** | Matching WAVECAR + `bseplot realspace` against bundled (or regenerated) BSEFATBAND with documented density metrics / side-by-side figures; or replace bundled assets with a fully reproducible reduced suite and update citation text. |
| **Concrete next steps** | 1) Locate original run directory if it still exists. 2) Or follow a full GW+BSE recipe (not the reduced Hartree demo). 3) Keep large files gitignored; only commit small `ref/*_summary.txt` and figures if desired. |
| **Already available** | `examples/bseplot/co2_demo/`, `examples/bseplot/mose2_recompute/`, [`repro/X6_exciton_rs.md`](repro/X6_exciton_rs.md). |

---

### 3.4 Raise weak / experimental features (optional science)

| ID | Feature | Gap | Done means | Priority |
|---|---|---|---|---|
| W5 | IPR | Demo only | Analytic limit + one defect ref table | P2 |
| B2 | Unfold + PROCAR weights | Experimental | Documented weight sum rules vs a VASP/ref case | P2 |
| B3 | Band reorder | Experimental | Multi-k case with known crossings + overlap metrics | P2 |
| B4 | PROCAR parse | Demo | Layout dialect tests (collinear / ncl) | P2 |
| B5 | IBZ k (`hse_kpts`) | Needs spglib | Optional dep install path + compare weights to `IBZKPT` | P2 |
| O3 | MAE helpers | Not gated | Occupations documented + meV-scale ref | P2 |
| X4 | WFULL reader | Infra | Round-trip / shape check vs a dump | P2 |
| D2 | NEB plot | Synthetic OUTCARs | Real multi-image OUTCAR fixture or clear synthetic-only label | P2 |

---

## 4. Open engineering / product work

| Item | Description | Done means | Priority | Effort |
|---|---|---|---|---|
| **Doc consistency pass** | `STATUS.md` citation short-list can lag `CITATION_POLICY` / FEATURES (e.g. P5/X6 wording). | One pass: STATUS, FEATURES, EXAMPLE_MATRIX, CITATION_POLICY agree on every ID level. | P0 | S |
| **spglib packaging** | Optional IBZ feature; install story still easy to miss. | `requirements-optional.txt` unambiguous; B5 smoke or skip message if missing. | P1 | S |
| **Light fixtures without dumps** | Spinor / NAC / tdm L2 need large local WAVECARs. | Documented regenerate scripts + optional tiny fixtures **or** matrix C1=skip when absent (no false FAIL). | P1 | M |
| **Smoke vs long runners** | MoSe2 recompute caches BSEFATBAND; FORCE rebuild is slow. | Document FORCE/NP/VASP_STD env; smoke stays &lt; few minutes on warm cache. | P0 | S |
| **Branch hygiene** | Long-lived `feature/c1-c2-examples`. | Decision: keep, rename, or merge to fork `main` (still no upstream PR). | P2 | S |
| **CI** | Historically none. | Optional: GitHub Action on fork running `pytest` + smoke without VASP dumps. | P2 | M |
| **pySBT pin** | AE **real-space** reconstruction demos may need pySBT; moment/dipole path often works without it. | Optional dep version pin + clear error when missing for P4 demos. | P2 | S |

---

## 5. Deferred by decision (do not restart without intent)

| Item | Why deferred | Reopen when |
|---|---|---|
| BSE X2/X3 algorithm campaign | High cost, quarantine already honest | Someone prioritizes production paw/q kernels |
| Upstream PR to QijingZheng/VaspBandUnfolding | Explicit fork policy | User explicitly requests |
| Committing WAVECAR / VASP tarballs | License + size | Never (use repro recipes) |
| Claiming full L2 for PS dipole vs CDER | Physics path mismatch | After §3.1 done |

---

## 6. Suggested order of attack

Use this if you only want a default sequence:

1. **P0 doc consistency** (§4) — STATUS/CITATION/FEATURES aligned.  
2. **P0/P1 smoke + optional deps** — spglib story, skip-vs-fail when dumps missing.  
3. **P1 pick one science line** (do not parallelize all three hard ones):  
   - **Optics/CDER** (§3.1) if the goal is trustworthy dipoles; or  
   - **BSE paw/q** (§3.2) if the goal is BSE citation; or  
   - **Production MoSe2 X6** (§3.3) if the goal is paper figures matching the bundled fatband.  
4. **P2 experimental cleanup** (§3.4) as bandwidth allows.

---

## 7. Per-item checklist template

Copy when starting a remaining item:

```text
ID / title:
Owner:
Branch:
Blockers removed? (data / deps / policy):
Commands to reproduce baseline:
Acceptance criteria (numeric or doc):
Citation label before → after:
Files touched:
Verification: smoke / pytest / example ref paths:
```

---

## 8. Related docs

| Doc | Role |
|---|---|
| [`STATUS.md`](STATUS.md) | What currently runs on this machine |
| [`CITATION_POLICY.md`](CITATION_POLICY.md) | What you may claim in papers |
| [`EXAMPLE_MATRIX.md`](EXAMPLE_MATRIX.md) | C1 runners and C2 labels |
| [`ASSUMPTIONS.md`](ASSUMPTIONS.md) | Physics/numeric limits |
| [`GOALS.md`](GOALS.md) | G1 proof / G2 reuse targets |
| [`ACADEMIC_ROADMAP.md`](ACADEMIC_ROADMAP.md) | Seminar-scale coverage |
| [`repro/README.md`](repro/README.md) | How to regenerate large dumps |
| [`WHY_NOT_ALL_AT_ONCE.md`](WHY_NOT_ALL_AT_ONCE.md) | Why campaigns are staged |

---

## 9. One-line summary

**Runnable demos and honest partial validation are largely in place.**  
**Left:** (1) true VASP-optics dipole parity, (2) BSE paw/finite-q un-quarantine, (3) production MoSe2 BSE WAVECAR parity, (4) weaker features + packaging polish—not greenfield scaffolding.
