---
layout: default
title: Get Started
permalink: /get-started/
description: >-
  Three paths into Open ChemE Hub — for students, for researchers, and for practising
  engineers — with the specific first thing to do in each.
---

<div class="page-header">
  <div class="container narrow">
    <h1>Get started</h1>
    <p class="lede">
      Three paths, depending on what you're trying to get done. Each starts with one concrete
      thing to do in the next twenty minutes, not a reading list.
    </p>
  </div>
</div>

<div class="container narrow prose">

<nav class="toc" aria-label="On this page">
  <strong>On this page</strong>
  <ul>
    <li><a href="#students">Students</a></li>
    <li><a href="#researchers">Researchers</a></li>
    <li><a href="#industry">Industry engineers</a></li>
    <li><a href="#educators">Educators</a></li>
    <li><a href="#common-questions">Common questions</a></li>
  </ul>
</nav>

---

## Students {#students}

**The problem you have:** the software your course teaches costs more than your degree, your
department has four floating licences, and the lab machine that runs it is booked.

**The first thing to do.** Fork [`templates`](https://github.com/open-cheme-hub/templates),
open `mass_balance_notebook.ipynb`, and work through Section 1 — a two-stream mixer you can
also do on paper in two minutes. Do the paper version first. Watching the code agree with your
own arithmetic is what makes the rest of the notebook trustworthy; skipping straight to Section
2 makes it a black box, which is the opposite of the point.

```bash
git clone https://github.com/open-cheme-hub/templates
cd templates
pip install numpy scipy matplotlib
jupyter lab mass_balance_notebook.ipynb
```

### Then, in rough order

1. **`reactor_design_skeleton.py`** — sizes a CSTR and a PFR and shows you why the CSTR is
   always bigger for a positive-order reaction. Run it with `--plot` for the Levenspiel plot,
   where the PFR volume is the area under a curve and the CSTR volume is a rectangle. That
   picture is worth a lecture.

   ```bash
   python reactor_design_skeleton.py -X 0.9 --sweep --plot
   ```

2. **`unit_conversions.py`** — needs nothing installed. Run it directly for worked examples
   across every unit you'll meet in a design project.

3. **[DWSIM](https://dwsim.org)** — a real flowsheet simulator, free, cross-platform, no dongle.
   Build the flowsheet from your design project in it. It is not Aspen, and for coursework the
   difference rarely matters.

4. **Free textbooks** — the *Learning Resources* section of
   [`awesome-chemical-engineering`](https://github.com/open-cheme-hub/awesome-chemical-engineering#learning-resources).
   [LearnChemE](https://learncheme.com) in particular has a screencast for almost every concept
   in the undergraduate curriculum.

5. **`lab_report_template.md`** — before your next lab write-up. The section notes say what
   markers actually look for. The uncertainty section is where most marks are lost, and the
   template shows a full worked propagation.

### Two pieces of advice worth more than any tool here

**Learn git before you need it.** Not for the hub — for your final year project, when your
laptop dies three days before submission.
[The Missing Semester](https://missing.csail.mit.edu) covers it in an afternoon.

**Check every computed answer against a hand estimate.** Order of magnitude is enough. Every
template in this repository is written to make that check easy, because the failure mode of
computational tools isn't being wrong — it's being confidently wrong in a plausible-looking
format.

---

## Researchers {#researchers}

**The problem you have:** your analysis ran on a laptop with a Python environment nobody can
reconstruct, and Reviewer 2 has asked how the conformers were generated.

**The first thing to do.** Run the pipeline in
[`workflows`](https://github.com/open-cheme-hub/workflows) end to end. It takes about ninety
seconds on the bundled test set, and it demonstrates the pattern you want for your own work:
pinned environment, fixed random seed, config file separate from code, per-rule logs.

```bash
git clone https://github.com/open-cheme-hub/workflows
cd workflows/snakemake
conda env create -f environment.yaml
conda activate conformer-gen
snakemake -n --cores 4        # dry run first, always
snakemake --cores 4
```

Read `results/summary/report.md` afterwards. Note that it says explicitly what the numbers do
*not* support — force-field conformer energies are wrong by 1–3 kcal/mol, which is a factor of
5 to 150 in population at room temperature. A pipeline that tells you its own limits is one you
can cite.

### The reproducibility checklist

Whatever you build, these five things are what let someone else — including you, in two years —
rerun it:

- [ ] **Pinned environment.** `environment.yaml` with exact versions, or a Docker digest.
      `latest` is not a version. RDKit's conformer defaults have changed across releases; an
      unpinned pipeline silently produces different science.
- [ ] **Fixed random seed**, recorded in the config. Without it you cannot tell whether a
      changed result came from your change or from the RNG.
- [ ] **Config separate from code.** Every scientifically meaningful parameter in one file, so
      a run is fully described by config + environment + inputs.
- [ ] **A tiny test case** that runs in under a minute. This is what makes CI possible and what
      lets a newcomer verify their install.
- [ ] **Commit hash in the paper.** Not "analysis performed in Python" — the hash.

### Also worth your time

- **[`eln_experiment_template.md`](https://github.com/open-cheme-hub/templates/blob/main/eln_experiment_template.md)**
  — an ELN entry structured so deviations get recorded as they happen. The example includes a
  drifting mass flow controller and a foaming problem, because those are what real entries
  contain and what makes an anomalous result explicable six months later.
- **The `chem-toolkit` container** — RDKit, Open Babel, Cantera, CoolProp, and the process
  engineering stack, all pinned, in one image:
  ```bash
  docker run --rm -it -v "$PWD:/work" ghcr.io/open-cheme-hub/chem-toolkit:1.2.0
  ```
- **[`awesome-chemoinformatics`](https://github.com/open-cheme-hub/awesome-chemoinformatics)** —
  particularly the *Benchmarks & Evaluation* section. If you're building molecular ML models,
  read the note on scaffold versus random splits before you report a number.

---

## Industry engineers {#industry}

**The problem you have:** you have Aspen and you're keeping it. What you don't have is a way to
review a simulation change, a quick answer at a desk without a licence seat, or something to
hand a graduate on day one.

**The first thing to do.** Read
[`aspen_simulation_tips.md`](https://github.com/open-cheme-hub/templates/blob/main/aspen_simulation_tips.md).
It covers getting real version control over binary simulation files: commit the `.bkp` plus a
scripted `.inp` text export in the same commit, keep a `MODEL.md` recording *why* the property
method is what it is, use Git LFS, and don't branch simulations because they don't merge.

The COM automation script in there turns "someone changed something in the depropaniser model"
into a readable diff showing the property method went from SRK to Peng–Robinson. That change
moves every number downstream and is invisible in a binary diff.

### What else earns its keep

- **[`fluids`](https://github.com/CalebBell/fluids) and [`ht`](https://github.com/CalebBell/ht)**
  — pressure drop, control valve sizing, exchanger rating with Bell–Delaware, all in Python,
  all free, all with the correlation source documented. For a desk check these beat opening a
  simulator.
- **[CoolProp](http://www.coolprop.org)** — properties for 122 fluids, with an Excel add-in.
  The Excel binding alone has saved more engineer-hours than anything else on this site.
- **[`safety_checklist.md`](https://github.com/open-cheme-hub/templates/blob/main/safety_checklist.md)**
  — a guide-word matrix and prompt list for preparing for a HAZOP. Read the disclaimer at the
  top: it is a prompt list, not a safety case, and it does not replace a formal study with a
  trained facilitator and someone who has actually operated the unit.
- **[`pid_tuning.py`](https://github.com/open-cheme-hub/templates/blob/main/pid_tuning.py)** —
  identify a FOPDT model from a bump test, then see Ziegler–Nichols, Cohen–Coon, AMIGO, and IMC
  tuning compared on the same loop. Useful for settling the recurring argument about why the
  textbook settings oscillate on a real column.
- **[DWSIM](https://dwsim.org)** — for the flowsheet you want to hand a customer, a contractor,
  or a student without also handing over a licence.

### For training a new engineer

Point them at `templates`. Every file is commented for the engineering rather than the syntax,
states what it can't do, and uses variable names with units in them. That last one is not a
style preference — `m_dot_feed_kg_s` instead of `m1` is the cheapest defence against the class
of error that loses hardware.

---

## Educators {#educators}

Everything here is CC BY 4.0 (prose) or MIT (code). Use it in a course without asking; a link
back is plenty.

- **`mass_balance_notebook.ipynb`** works as a first computational lab. It builds from a
  hand-checkable case to a linear system with recycle, and ends with the checklist for whether
  a balance is trustworthy.
- **`reactor_design_skeleton.py`** with `--sweep` generates the volume-versus-conversion data
  for a whole problem set, and the energy-balance caveat at the end is a ready-made discussion
  prompt about what an isothermal model cannot tell you.
- **`pid_tuning.py`** is a full lab on its own — identify, tune four ways, compare, argue about
  robustness.
- **The `chem-toolkit` container** removes the first-week install support burden entirely.

If you build course material on top of these, post it in
[Show and Tell](https://github.com/orgs/open-cheme-hub/discussions/categories/show-and-tell).
Teaching notes are the resource this field is shortest of.

---

## Common questions {#common-questions}

**Is this really all free?**
Yes. Everything listed is open source, open access, or has a genuinely usable free tier — and
free tiers are tagged `commercial-free-tier` so you know before you install.

**Can I use these templates in commercial work?**
Yes. MIT licence, no attribution required. The disclaimer stands: they're starting points, and
anything affecting a real plant needs review by a qualified engineer who is accountable for it.

**Something is broken / a link is dead.**
[Open an issue](https://github.com/open-cheme-hub/.github/issues), or just fix it in a pull
request — link fixes get merged quickly.

**I maintain a tool that belongs on a list.**
Add it. Say in the PR description that it's yours — that's fine and we just like knowing. Same
bar as everything else: docs, a licence, and an example that runs.

**Why isn't [commercial tool] listed?**
Because it's paywalled with no meaningful free path. Open alternatives to it are listed, and
`aspen_simulation_tips.md` covers working alongside what you already own.

**Where do I ask a question?**
[Discussions → Q&A](https://github.com/orgs/open-cheme-hub/discussions/categories/q-a).
Answers stay searchable there, which is worth more than a fast reply in a chat window.

</div>
