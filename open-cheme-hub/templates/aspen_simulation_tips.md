# Version-controlling Aspen Plus and HYSYS work

**Why there's no `aspen_plus_skeleton.bkp` in this repository.**

Aspen `.bkp`, `.apw`, and `.apwz` files are binary. So are HYSYS `.hsc` files. Git will store
them, but it cannot diff them, cannot merge them, and cannot tell you what changed between two
revisions. A repository full of `.bkp` files is a pile of opaque blobs with commit messages you
have to trust.

There is also a licensing point: Aspen's licence terms cover the software, and simulation files
are your work product, but company models routinely embed proprietary property data,
confidential stream compositions, and customer information. Think before pushing one anywhere,
including a private repository that contractors can read.

This guide covers how to get real version control over commercial simulation work.

---

## The short version

1. Commit the **binary** for reproducibility (`.bkp`, not `.apw` — see below).
2. Commit a **text export** alongside it, in the same commit, so the diff is readable.
3. Commit a **`MODEL.md`** describing intent, basis, and what changed and why.
4. Use **Git LFS** if the files are large or change often.
5. Never branch a simulation expecting to merge it. Simulations don't merge.

---

## 1. Which file format to commit

| Extension | What it is | Commit it? |
| --- | --- | --- |
| `.bkp` | Backup file — flowsheet, specs, and configuration, portable across versions | **Yes.** This is the one. |
| `.apw` | Full working file including converged results and the solver state | No. Large, version-locked, changes on every run |
| `.apwz` | Compressed composite | Occasionally, if you must ship results with the model |
| `.inp` | Text input language export | **Yes** — this is what makes diffs work |
| `.hsc` | HYSYS case | Yes, with the same reservations as `.bkp` |
| `.edr` | Exchanger Design & Rating | Yes |
| `*.def`, `*.appdf` | Property definitions | Yes if you use custom property data |

`.bkp` is version-portable in a way `.apw` is not: a `.apw` written by V12 will not open in V11,
and often complains across minor versions. `.bkp` degrades more gracefully. If your team
straddles versions, `.bkp` is the only sane choice.

**Always record the Aspen version in the commit message.** `.bkp` is more portable, not
portable.

---

## 2. Making diffs readable

Aspen Plus can export the flowsheet as its **input language** — a plain text representation of
blocks, streams, specs, and property methods.

**Manual export:** `File → Export → Input File (.inp)`

**Scripted export**, which is what you actually want, via the Aspen Plus COM automation
interface:

```python
"""Export an Aspen Plus .bkp to text so git can diff it.

Requires: Windows, a licensed Aspen Plus installation, pywin32.
    pip install pywin32

Run this as a pre-commit hook and the text export can never drift from the binary.
"""

import os
import sys

import win32com.client


def export_input_file(bkp_path: str, inp_path: str) -> None:
    """Open a .bkp and write its input-language representation to .inp."""
    aspen = win32com.client.Dispatch("Apwn.Document")
    try:
        # visible=0 runs it headless; readonly=1 guarantees we can't corrupt the source
        aspen.InitFromArchive2(os.path.abspath(bkp_path))
        aspen.Visible = 0
        aspen.SuppressDialogs = 1
        aspen.Export(None, os.path.abspath(inp_path))
        print(f"Exported {bkp_path} -> {inp_path}")
    finally:
        aspen.Close()
        aspen.Quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: export_aspen.py model.bkp model.inp")
    export_input_file(sys.argv[1], sys.argv[2])
```

Now `git diff model.inp` shows you that someone changed the RadFrac stage count from 30 to 34
and switched the property method from `NRTL` to `NRTL-RK`. That second change is the kind that
silently moves every result in the flowsheet, and it is invisible in a binary diff.

### Pre-commit hook

`.git/hooks/pre-commit` (or a `pre-commit` framework entry):

```bash
#!/usr/bin/env bash
set -euo pipefail

# Regenerate the .inp for every staged .bkp so the two never diverge.
for bkp in $(git diff --cached --name-only --diff-filter=ACM | grep '\.bkp$' || true); do
    inp="${bkp%.bkp}.inp"
    python tools/export_aspen.py "$bkp" "$inp"
    git add "$inp"
done
```

---

## 3. Handle the binaries with Git LFS

`.bkp` files run from a few hundred kilobytes to tens of megabytes. Committing a 20 MB file
weekly for two years puts 2 GB of history in every clone, forever.

`.gitattributes`:

```gitattributes
# Aspen and HYSYS binaries via LFS
*.bkp   filter=lfs diff=lfs merge=lfs -text
*.apw   filter=lfs diff=lfs merge=lfs -text
*.apwz  filter=lfs diff=lfs merge=lfs -text
*.hsc   filter=lfs diff=lfs merge=lfs -text
*.edr   filter=lfs diff=lfs merge=lfs -text

# Text exports stay in git proper, where diffs work
*.inp   text
*.md    text
*.csv   text
```

Then:

```bash
git lfs install
git lfs track "*.bkp"
git add .gitattributes
```

Set this up **before** the first commit of a binary. Migrating existing history with
`git lfs migrate` rewrites every commit hash, which is disruptive on a shared repository.

---

## 4. Document the model, not just the file

A `.bkp` records *what* the model is. It does not record *why*. Keep a `MODEL.md` next to it:

```markdown
# C-101 Depropaniser — steady state model

**Aspen Plus V14.0** | Last converged 2026-04-02 | Owner: [name]

## Purpose
Rating case for the existing depropaniser at 110% of design throughput, to support the
debottlenecking study (Project PX-2201).

## Basis
- Feed: stream 4 from the 2025 plant test run, 2025-09-14 (see `data/plant_test_2025.xlsx`)
- Property method: **PENG-ROB** with the binary parameters in `props/pr_binaries.csv`,
  regressed from the DECHEMA VLE data cited there
- Column: 42 valve trays, 65% flood at design, tray efficiency 0.72 from the plant test
- Condenser: total, 45 °C outlet, fixed by the air cooler rating

## Validated against
Plant test 2025-09-14. Model predicts overhead C3 purity within 0.4 mol% and reboiler duty
within 3%. Predicted bottoms C3 content is consistently 1.2 mol% high — **the model is
optimistic on bottoms purity and should not be used to set a bottoms spec.**

## Known limitations
- No tray hydraulics below 60% turndown; the model converges but the trays would weep
- Assumes no fouling; the reboiler duty is a clean-condition number
- Feed composition is a single test point, not a range

## Convergence
Converges from the supplied initialisation in ~40 iterations. If it fails after a spec change,
reset the column to the saved initialisation before changing anything else.

## Change log
| Date | Change | Reason | By |
| --- | --- | --- | --- |
| 2026-04-02 | Tray efficiency 0.68 -> 0.72 | Regressed against the 2025 plant test | AB |
| 2026-03-11 | Property method SRK -> PENG-ROB | SRK under-predicted C3/C4 relative volatility vs the DECHEMA data | AB |
```

The property method line is the one that saves someone a week. Six months later nobody
remembers why the model uses PENG-ROB, and re-deriving it costs more than writing it down did.

---

## 5. Export results as text too

Don't make the next person open Aspen just to see what the model predicts. Export the stream
table and key block results to CSV on every significant commit:

```python
"""Pull a stream table out of a converged Aspen case into CSV."""

import csv

import win32com.client


def export_stream_table(apw_path: str, csv_path: str) -> None:
    aspen = win32com.client.Dispatch("Apwn.Document")
    aspen.InitFromArchive2(apw_path)
    aspen.Visible = 0

    streams = aspen.Tree.FindNode(r"\Data\Streams")
    rows = []
    for stream in streams.Elements:
        name = stream.Name
        node = lambda path: aspen.Tree.FindNode(  # noqa: E731
            rf"\Data\Streams\{name}\Output\{path}"
        )
        rows.append({
            "stream": name,
            "T_C": _value(node("TEMP_OUT\\MIXED")),
            "P_bar": _value(node("PRES_OUT\\MIXED")),
            "mass_flow_kg_h": _value(node("MASSFLMX\\MIXED")),
            "mole_flow_kmol_h": _value(node("MOLEFLMX\\MIXED")),
        })

    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    aspen.Close()
    aspen.Quit()


def _value(node):
    """Aspen returns None for unset nodes; don't let that become a silent zero."""
    return node.Value if node is not None else ""
```

Committing `results/stream_table.csv` alongside the model means a diff shows you that the
reboiler duty moved 8% — which is the review question, and you can answer it without a licence.

---

## 6. Branching and merging: don't

**Simulation files do not merge.** Two people editing the same `.bkp` on different branches
produces a conflict git cannot resolve and you cannot resolve by hand. Options, in order of
preference:

1. **One owner per model file.** Coordinate in the issue tracker, not in git. This is
   unfashionable advice and it is correct.
2. **Copy, don't branch.** `C101_case_A.bkp`, `C101_case_B.bkp` for genuine alternatives you
   intend to keep. Case studies are files, not branches.
3. **If you must branch**, agree in advance that one side will be discarded, and record which
   in the PR description.

Aspen's own Case Study and Sensitivity tools handle parametric variation inside one file.
Reach for those before you reach for branches.

---

## 7. Recommended repository layout

```
depropaniser-study/
├── README.md                 # what this study is, how to run it
├── MODEL.md                  # basis, validation, limitations, change log
├── .gitattributes            # LFS tracking
├── models/
│   ├── C101_base.bkp         # LFS
│   ├── C101_base.inp         # text export, diffable
│   ├── C101_case_110pct.bkp
│   └── C101_case_110pct.inp
├── props/
│   ├── pr_binaries.csv       # regressed parameters, with their source
│   └── regression_notes.md
├── data/
│   └── plant_test_2025.xlsx  # the measurements the model is validated against
├── results/
│   ├── stream_table.csv      # exported on each significant commit
│   └── column_profiles.csv
├── tools/
│   ├── export_aspen.py
│   └── export_results.py
└── reports/
    └── 2026-04_debottleneck.md
```

---

## 8. What not to commit

- **Licence files, licence server addresses, or anything from `SLM`/`LMTOOLS`.** Ever.
- **`.apw` files as the primary record** — they bloat history and lock you to a version.
- **Anything containing customer or partner data** without checking the confidentiality terms.
  A stream composition can be commercially sensitive on its own.
- **Cracked binaries or licence workarounds.** This is worth stating plainly: it is a firing
  offence at most employers and a licence violation everywhere.
- **Temporary and lock files.** Add to `.gitignore`:

```gitignore
# Aspen working files
*.apw
*.appdf
*.his
*.bkp.bak
~$*
*.lck
*.dfms
```

(Keep `*.apw` ignored by default; commit one deliberately with `git add -f` if you genuinely
need to ship converged results.)

---

## 9. Open alternatives worth knowing

If your work can move off a licensed simulator, everything above becomes unnecessary — open
formats diff and merge natively:

- **[DWSIM](https://dwsim.org)** — the `.dwxml` format is plain XML and diffs cleanly. See
  [`dwsim_simulation.dwxml`](dwsim_simulation.dwxml) in this repository for a worked example.
- **[COCO/COFE](https://www.cocosimulator.org)** — free, CAPE-OPEN, Windows.
- **[IDAES](https://github.com/IDAES/idaes-pse)** — flowsheets as Python. The model *is* the
  source code, so every git feature works normally.

For teaching and for published work, an open format that a reader can actually open is worth a
lot. For a plant model validated against twenty years of operating data, staying on Aspen is
usually the right call — just version-control it properly.

---

*Part of [open-cheme-hub/templates](https://github.com/open-cheme-hub/templates). MIT licence.
Aspen Plus, Aspen HYSYS, and Aspen EDR are trademarks of Aspen Technology, Inc. This document
is not affiliated with or endorsed by AspenTech.*
