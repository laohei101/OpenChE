# Open ChemE Hub

**Open, curated, community-maintained resources for chemical engineering and the sciences next door.**

Chemical engineers, chemists, bioengineers, and biomedical researchers keep rebuilding the same
things: a material balance notebook, a thermodynamics lookup, a HAZOP checklist, a conformer
generation pipeline. Meanwhile the best open-source tooling in our fields — DWSIM, Cantera,
CoolProp, RDKit, COBRApy, OpenSim — is scattered across university pages, dead SourceForge links,
and a dozen half-abandoned wikis.

Open ChemE Hub is a single, opinionated, maintained index of what actually works, plus the
starter files and workflows to put it to use the same afternoon.

---

## What's here

| Repository | What it is |
| --- | --- |
| [`awesome-chemical-engineering`](https://github.com/OpenChemE/awesome-chemical-engineering) | Process simulation, thermodynamics, unit operations, control, safety, data, courses |
| [`awesome-chemoinformatics`](https://github.com/OpenChemE/awesome-chemoinformatics) | Molecular representation, QSAR/QSPR, reaction prediction, chemical databases, ML for chemistry |
| [`awesome-bioengineering`](https://github.com/OpenChemE/awesome-bioengineering) | Bioprocess modelling, genome-scale metabolic models, synthetic biology, biomaterials, tissue engineering |
| [`awesome-medical-engineering`](https://github.com/OpenChemE/awesome-medical-engineering) | Medical device design, biomechanics, imaging, regulatory standards, clinical engineering, health informatics |
| [`awesome-general-engineering`](https://github.com/OpenChemE/awesome-general-engineering) | CAD/CAE, control systems, signal processing, IoT and embedded, project management, ethics |
| [`templates`](https://github.com/OpenChemE/templates) | Fork-and-edit starting points: mass balance notebook, reactor design skeleton, lab report, safety checklist, ELN entry, PID tuning |
| [`workflows`](https://github.com/OpenChemE/workflows) | Reproducible Snakemake pipelines, reusable GitHub Actions, and a Docker image with RDKit + Open Babel + Cantera |
| [`hub-website`](https://github.com/OpenChemE/hub-website) | The static site at [opencheme.github.io](https://opencheme.github.io), with search across every list |
| [`.github`](https://github.com/OpenChemE/.github) | This profile, the code of conduct, and the shared contributing guide |

---

## Getting started

**I'm a student.** Start with [`templates`](https://github.com/OpenChemE/templates). Fork it,
open `mass_balance_notebook.ipynb`, and work a balance you already know how to do by hand — seeing
the two agree is the fastest way to trust the tooling. Then browse the *Learning Resources* section
of the chemical engineering list for free textbooks.

**I'm a researcher.** Go to [`workflows`](https://github.com/OpenChemE/workflows). The
Snakemake conformer-generation pipeline and the Docker image give you a reproducible environment
that a reviewer can actually rerun. Pair it with the ELN template from `templates`.

**I'm an industry engineer.** The *Process Simulation* and *Process Control & Safety* sections of
[`awesome-chemical-engineering`](https://github.com/OpenChemE/awesome-chemical-engineering)
are where most people land — open alternatives to licensed tools, plus `safety_checklist.md` in
`templates` for a HAZOP-style pre-read.

Full walkthrough: **[Get Started](https://opencheme.github.io/get-started/)**

---

## Contributing

Every list is a pull request away from being better. Adding a resource takes about two minutes:

1. Find the right list and the right section.
2. Add one line: `- [Name](url) — one-sentence description. \`tag\``
3. Open the PR. The checklist in the template tells you what a reviewer will look for.

Read [CONTRIBUTING.md](https://github.com/OpenChemE/.github/blob/main/CONTRIBUTING.md) first —
it covers what gets accepted (maintained, openly licensed, genuinely useful) and what doesn't
(paywalled tools, dead projects, self-promotion without substance).

Questions, "does anyone have a good X", teaching notes, and war stories go in
[Discussions](https://github.com/orgs/OpenChemE/discussions).

## Code of Conduct

We follow the [Contributor Covenant](https://github.com/OpenChemE/.github/blob/main/CODE_OF_CONDUCT.md).
Be the colleague you'd want on a startup team at 3am.

## Licence

Lists and documentation are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code, templates, and workflows are MIT. Attribution is appreciated; a link back is plenty.
