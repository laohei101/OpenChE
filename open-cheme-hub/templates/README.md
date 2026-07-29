# Templates

**Fork-and-edit starting points for calculations, reports, simulations, and lab records.**

Every chemical engineer rebuilds the same handful of files: a material balance notebook, a
reactor sizing script, a lab report skeleton, a HAZOP prompt list. These are those files,
written to be read by someone learning as well as run by someone in a hurry.

Nothing here needs installing. Clone the repository, or copy the one file you want.

```bash
git clone https://github.com/open-cheme-hub/templates
cd templates
python unit_conversions.py       # runs a self-test with worked examples
```

---

## What's here

| Template | What it does | Needs |
| --- | --- | --- |
| [`mass_balance_notebook.ipynb`](mass_balance_notebook.ipynb) | Steady-state material balances, from a two-stream mixer you can check by hand to a three-unit flowsheet with recycle, plus a reaction example | numpy, matplotlib |
| [`reactor_design_skeleton.py`](reactor_design_skeleton.py) | CSTR and PFR sizing for a liquid-phase reaction, with a CSTRs-in-series comparison and a Levenspiel plot | numpy, scipy, matplotlib |
| [`pid_tuning.py`](pid_tuning.py) | FOPDT identification from a step test, then four tuning rule sets compared on the same simulated loop | numpy, matplotlib |
| [`unit_conversions.py`](unit_conversions.py) | Conversions for flows, pressures, temperatures, viscosities, and duty, plus dimensionless groups | nothing — stdlib only |
| [`lab_report_template.md`](lab_report_template.md) | Undergraduate lab report with YAML front matter, worked structure, and an uncertainty section | pandoc or Quarto to render |
| [`eln_experiment_template.md`](eln_experiment_template.md) | Electronic lab notebook entry: hypothesis, materials with lot numbers, execution log, deviations, amendments | nothing |
| [`safety_checklist.md`](safety_checklist.md) | HAZOP-style guide-word matrix and prompt list, with a laboratory-scale supplement | nothing |
| [`aspen_simulation_tips.md`](aspen_simulation_tips.md) | How to version-control Aspen and HYSYS work so diffs are readable | nothing |
| [`dwsim_simulation.dwxml`](dwsim_simulation.dwxml) | An annotated DWSIM flowsheet in XML, showing why an open format is reviewable and a binary one isn't | DWSIM, to open it |

---

## The computational templates

### `mass_balance_notebook.ipynb`

Four sections, increasing in difficulty:

1. **A two-stream mixer** you should be able to do on paper in two minutes. Do that first — the
   point of this section is watching the code agree with your arithmetic.
2. **Balances as a linear system.** A three-unit flowsheet with recycle, built as an explicit
   `Ax = b` so you can read the physics off the matrix and so a singular `A` tells you the
   problem is under-specified rather than leaving you to hunt for a missing spec.
3. **Visualisation**, including a recycle sensitivity sweep — the plot that justifies or kills
   a recycle, since internal flows grow much faster than the recycle ratio does.
4. **Reaction**, with methanol synthesis at known conversion, showing that moles aren't
   conserved and mass always is.

It ends with a checklist for before you trust a balance, and a table of the three situations
that make a balance nonlinear and what to reach for in each.

**Change first:** the problem definitions in Sections 2 and 4. Everything else is machinery
that works unchanged.

### `reactor_design_skeleton.py`

Sizes a CSTR and a PFR for the same conversion and compares them. The worked case is ethyl
acetate saponification — second order, dilute aqueous, near-isothermal — with kinetics that are
a literature-consistent Arrhenius fit rather than a measurement, and the file says so.

```bash
python reactor_design_skeleton.py -X 0.90 --sweep --plot
python reactor_design_skeleton.py --existing-volume 0.5    # what can my existing vessel do?
python reactor_design_skeleton.py -T 313.15 --CA0 200      # different operating point
```

Includes a CSTRs-in-series comparison showing convergence towards PFR behaviour, and a
Levenspiel plot where the CSTR volume is a rectangle and the PFR volume is the area under the
curve.

**It solves no energy balance.** The file ends with a section explaining exactly what that
means you cannot conclude — cooling duty, multiple steady states, runaway potential — and how
to compute the adiabatic temperature rise that tells you whether the isothermal assumption was
ever defensible.

**Change first:** `Kinetics`, `Feed`, and `rate_of_disappearance_A()`.

### `pid_tuning.py`

Identifies a FOPDT model from a (simulated, noisy) step test, then computes settings from
Ziegler–Nichols, Cohen–Coon, AMIGO, and IMC/lambda tuning, and simulates each through a
setpoint change and a load disturbance.

```bash
python pid_tuning.py --identify --plot
python pid_tuning.py -K 1.8 --tau 120 --theta 45     # your own process
```

The comparison is the point. Z–N targets quarter-amplitude decay and lands around 70% overshoot
on this process; IMC lands under 1%. Seeing that side by side is the fastest way to understand
why plants detune the famous rules.

Implementation details usually skipped in textbook code and included here because they decide
whether the loop works: **anti-windup** (conditional integration when the output saturates),
**derivative on measurement** rather than error, and **derivative filtering**.

**Change first:** the `PROCESS` FOPDT parameters, or feed your own plant trend to
`identify_fopdt()`.

### `unit_conversions.py`

Dependency-free, so it can be copied into a project that isn't allowed to install packages.
Covers 17 physical quantities with the units chemical engineers actually use — `gpm`, `bbl/d`,
`MMBTU/h`, `BTU/(h.ft2.F)`, `klb/h` — plus gauge/absolute pressure handling, composition
conversion, and Reynolds/Prandtl/Nusselt.

```python
from unit_conversions import convert, convert_temperature, gauge_to_absolute

convert(10_000, "kg/h", "lb/h")          # 22046.2
gauge_to_absolute(150, "psi")            # 164.70 psia
convert_temperature(100, "degC", "degF") # 212.0
```

Temperature is deliberately separate: it's affine, not linear, and `convert()` raises rather
than silently returning nonsense. Cross-quantity conversion (kg/h to m³/h) is refused too,
because it needs a density this module doesn't know.

If you *can* install packages, use [`pint`](https://pint.readthedocs.io) instead — it tracks
dimensions through your whole calculation, not just at the boundaries.

Run it directly for a worked-example self-test; `python -m doctest unit_conversions.py` passes
clean.

---

## The document templates

### `lab_report_template.md`

Full undergraduate report structure with YAML front matter for pandoc or Quarto:

```bash
pandoc lab_report_template.md -o report.pdf --citeproc --number-sections
quarto render lab_report_template.md --to pdf
```

Each section carries a target length and a note on what markers actually look for — delete
those before submitting. The worked example throughout is a double-pipe heat exchanger, with a
real uncertainty analysis that identifies which measurement dominates and why improving the
other one would have been wasted effort.

**Your course handbook overrides this template** on structure, length, and referencing.

### `eln_experiment_template.md`

An entry from a real-shaped experiment — kLa measurement in a stirred bioreactor — written the
way a good notebook actually reads: hypothesis and success criteria fixed *before* the run,
deviations recorded as they happened (including a drifting mass flow controller and a foaming
problem), and an interpretation that separates what was shown from what was assumed.

The convention that makes a notebook worth keeping: **record what happened, not what was
supposed to happen.** Entries are append-only; corrections go in the Amendments table with a
date and a reason.

### `safety_checklist.md`

A guide-word matrix (parameter × NO/MORE/LESS/REVERSE/AS WELL AS/PART OF/OTHER THAN) plus prompt
lists for chemical hazards, pressure relief, instrumented protection, human factors, and
management systems. Includes a **laboratory and pilot-scale supplement** for work where a formal
HAZOP is disproportionate but the hazard is real.

> **This is a prompt list, not a safety case.** It helps a competent team remember to ask
> questions. It does not make anyone competent, and a completed copy is not evidence that a
> process is safe. Never use it to sign off a design, satisfy a regulator, or replace a formal
> HAZOP. Where a jurisdiction mandates a methodology, that mandate governs.

### `aspen_simulation_tips.md`

Why there's no `.bkp` file in this repository, and what to do instead: commit the `.bkp` plus a
scripted `.inp` text export in the same commit, keep a `MODEL.md` recording the property method
and *why*, use Git LFS, and don't branch simulations because they don't merge.

Includes working COM automation scripts for exporting the input file and the stream table, and
a pre-commit hook so the text export can never drift from the binary.

### `dwsim_simulation.dwxml`

An annotated mixer + heater flowsheet showing where compounds, property packages, unit
operations, and connections live in DWSIM's XML. **It's a hand-written teaching skeleton, not a
DWSIM export** — the file says so at the top, and tells you how to build the same flowsheet in
DWSIM in five minutes and diff yours against it.

The point survives that caveat: DWSIM's format is XML, Aspen's is binary, and only one of them
lets you review a simulation change.

---

## Contributing a template

A good template is something you'd hand a new hire on their first day.

- **It runs.** Clone-and-execute with the dependencies named in the header, no manual edits
  needed to get *some* output.
- **Comments explain the engineering, not the Python.** `# solve the linear system` is noise;
  `# Overall + component balances give 3 equations in 3 unknowns` is the point.
- **Units are explicit everywhere**, in variable names or comments. `m_dot_feed_kg_s`, not `m1`.
- **Numbers are physically plausible.** Reactor volumes a real vessel could be, temperatures
  that don't decompose the feed.
- **Header block**: purpose, author, licence, dependencies, and one line on what to change first.
- **Say what it can't do.** The reactor script's isothermal caveat and the safety checklist's
  disclaimer are the most important paragraphs in those files.
- **Add it to the table above** in the same PR.

Notebooks: clear outputs before committing (`jupyter nbconvert --clear-output --inplace`) so
diffs stay readable.

Full guide: [CONTRIBUTING.md](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md).

---

## Licence

MIT — use these in coursework, in industry, in a textbook, without asking. Attribution is
appreciated and not required.

**No warranty.** These are teaching and starting-point materials. Anything affecting a real
plant, a real patient, or a real safety case needs review by a qualified engineer who is
accountable for it. That's not a formality this repository can shortcut for you.
