# Secondary Development Goals

Audience: maintainers and research users of **VaspBandUnfolding** (PyVaspWfc).  
Status: agreed direction for further development (expert / publication context).

Related: [`FEATURES.md`](../FEATURES.md) · [`ASSUMPTIONS.md`](ASSUMPTIONS.md) · [`ACADEMIC_ROADMAP.md`](ACADEMIC_ROADMAP.md)

---

## 1. Two primary goals

### G1 — Prove components are complete and scientifically sound

Each **feature component** (stable ID in `FEATURES.md`: W*, B*, P*, O*, X*, D*, I*, C*) should reach a state where experts can answer:

| Question | Required evidence |
|---|---|
| What does it compute? | Clear definition, units, inputs/outputs |
| Under what assumptions? | Entry in [`ASSUMPTIONS.md`](ASSUMPTIONS.md) or method card |
| Is the implementation feature-complete for that definition? | Documented scope + explicit non-goals (no silent half-support) |
| Is it scientifically trustworthy? | Validation level **L2+** for citation-facing claims; L1 only for internal/analytic limits |
| What must not be claimed? | Quarantine list (e.g. weak BSE modes, experimental ELF) |

**“完整”** means: complete relative to a **stated scientific contract**, not “every VASP code path reimplemented.”  
**“正确”** means: correct under that contract, with **reproducible comparison** (VASP same-input, analytic limit, or accepted reference)—not “runs without crashing.”

### G2 — Usable as low-cost components in other research projects and papers

Components must be easy to **import, call, cite, and pin** from external scientific workflows (scripts, pipelines, other repos, paper SI).

| Requirement | Practical meaning |
|---|---|
| **Low integration cost** | Stable import path; minimal boilerplate; deps explicit (`pyproject` / optional extras) |
| **Composable** | One concern per component (read WAVECAR ≠ build BSE ≠ plot); shared types/units documented |
| **Publication-ready** | Version/git commit pin; assumptions + level; small public fixtures or repro recipe |
| **Non-invasive** | No forced package layout on the host project; no hidden global state; CLI optional |
| **Honest packaging** | Unvalidated modes not exposed as default “production” API |
| **Mainstream stack** | Python ≥3.10 and current numpy/scipy/ase/… only (G2.1); papers freeze their own env |


Success looks like: *another paper’s methods section can say “spectral weights via PyVaspWfc `unfold` (commit …), validated as in …” without forking half the repo.*

### G2.1 Runtime & dependency support policy

**Support current / mainstream stacks only** — not long-tail legacy environments.

| Layer | Policy |
|---|---|
| **Python** | Current project floor is `requires-python >= 3.10` (`pyproject.toml`). Target **CPython 3.10+** in active upstream support (or the newest 2–3 minor releases commonly used in research). No commitment to 3.8/3.9 or end-of-life interpreters. |
| **Core libs** | `numpy`, `scipy`, `matplotlib`, `ase` — develop and test against **recent stable PyPI releases** (or the versions your lab’s default env already uses). Prefer modern APIs; do not keep shims solely for ancient numpy/scipy. |
| **Optional libs** | `pySBT`, `spglib`, etc. — document a **working recent version**; bump when broken by upstream, rather than multi-version matrix hell. |
| **OS / arch** | Linux + typical HPC/login nodes first; no special support contract for abandoned platform stacks. |
| **What we do *not* do** | CI matrices over many old pins; polyfills for removed stdlib/numpy APIs; “works on whatever was on the cluster in 2018.” |

**Paper reproducibility:** pin *your paper env* (environment.yml / requirements freeze / commit hash) at publication time. The library’s promise is compatibility with **mainstream current** tools, not eternal bitwise stability of every transitive dep forever.


---

## 2. Non-goals (explicit)

| Non-goal | Reason |
|---|---|
| Replace VASP | This is post-processing / analysis on VASP outputs |
| Teach DFT from zero | Audience is specialists; onboarding is secondary |
| Claim L3 for all IDs immediately | Full-matrix stewardship ≠ simultaneous paper-grade proof |
| Silent “best effort” physics | Contradicts G1 |
| Heavy framework / plugin bus | Raises cost for G2; prefer plain Python modules + thin CLI |
| Bundle all production WAVECARs in git | Use small fixtures + external/`crisp` repro docs |
| Long-term support for obsolete Python / numpy stacks | G2.1: mainstream current only |

---

## 3. Definition of done (per component)

A component is **G1+G2 ready** when all of the following hold:

1. **ID + Level** in [`FEATURES.md`](../FEATURES.md) (Level ≥ **L2** if the public docs encourage scientific use; otherwise Level labeled and API marked experimental).  
2. **Contract**: inputs, outputs, units, failure modes, ASSUMPTIONS cross-links.  
3. **Evidence**: in-repo table/fixture test **or** `docs/repro/<ID>.md` with pinned VASP version and expected numbers.  
4. **API surface**: one obvious entry (function/class/CLI) callable as:
   ```python
   from <module> import <symbol>  # after pip install -e .
   ```
5. **No packaging traps**: optional deps declared; missing optional dep → clear error, not corrupt numbers.  
6. **Citation stub**: one paragraph suitable for a paper methods section (what / version / validation pointer).

Infrastructure IDs (I1–I4) are G1+G2 ready at **L1–L2** with unit tests (they enable other components).

---

## 4. Priority order implied by G1 + G2

Work that **maximizes proof + reuse** first:

| Priority | Focus | Why |
|---|---|---|
| **P0** | Citation boundaries + quarantine; dipole L2; packaging/deps honesty; assumptions in workflow | Stops wrong claims; unblocks paper use of “safe” paths |
| **P1** | L1 unit tests; L2 gates on already-strong examples (projectors, wfc_r, BSE `pw_only`, bseplot bz, ewald); small installable API | Makes components regressable and importable |
| **P1** | Repro packs for high-demand science (unfold, spinor, exciton real-space) | Enables external projects without tribal knowledge |
| **P2** | Fill evidence holes (PROCAR, NAC, IPR, ELF decide validate-or-mark) | Completeness of the portfolio under G1 |
| **P3** | Method cards, seminar assets, research extensions on top of green L2 cores | After components are trustworthy |

Research extensions (new physics) are welcome **only on top of** a G1-ready base of the components they depend on.

---

## 5. Componentization guidelines (for G2)

| Do | Don't |
|---|---|
| Prefer pure functions / small classes with explicit paths | Hide required files in cwd magic without args |
| Return `numpy` arrays + dict/dataclass metadata | Print-only scientific results with no return value |
| Keep 1-based VASP indices at boundaries; document them | Mix 0- and 1-based silently |
| Version-pin in examples: package version + git hash helper | Rely on “latest main” for papers |
| Optional CLI wrappers around library code | Put sole logic only in `bin/` scripts |
| Thin deps for core import (`numpy`/`scipy`/`ase`) | Import `pySBT`/plotting at module top if optional |

**Target consumption pattern for external projects:**

```text
pip install git+https://github.com/<org>/VaspBandUnfolding@<tag>
# or pip install -e /path/to/VaspBandUnfolding

from vaspwfc import vaspwfc
from unfold import unfold
# … call with absolute paths; write own plotting/paper pipeline
```

---

## 6. Relationship to other repos / tools

| Tool | Role under G1/G2 |
|---|---|
| This repo | Implementation, tests, evidence, installable components |
| [`vasp_wiki`](~/vasp_wiki) (optional) | INCAR/wiki semantics when writing repro inputs—not a runtime dependency of VBU |
| `crisp` / HPC | Generate heavy VASP outputs for L2; not required at import time for consumers |
| Downstream science repos | Depend on **pinned** VBU; own physics narrative and figure pipeline |

---

## 7. Tracking

| Artifact | Use |
|---|---|
| `FEATURES.md` | Per-ID Level / status → G1 dashboard |
| `ASSUMPTIONS.md` | Scientific contract limits |
| `ACADEMIC_ROADMAP.md` | Full-coverage plan, seminars, phases |
| This file | **Why** we develop; acceptance for “done” |

When promoting an ID to L2, update `FEATURES.md` and add or link evidence in the same PR.

---

## 8. One-line summary

> **Prove each component’s scientific contract with evidence (G1), then ship it so other research code and papers can depend on it cheaply and honestly (G2).**
