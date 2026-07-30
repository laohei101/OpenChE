# OpenChemE

**"GitHub" for Chemical Engineers** — a verified, open engineering commons.

Chemical engineers keep rebuilding the same material balance, hunting the same dead SourceForge
link, and writing the same HAZOP checklist from memory. OpenChemE turns scattered open-source
tools into a **structured, verifiable catalog** with runnable templates and reproducible
workflows attached.

The thing that makes it different is not the number of resources. It is that every record tells
you **what has actually been checked** — and, right now, mostly says "nothing yet", because that
is the truth.

```bash
git clone https://github.com/laohei101/OpenChemE && cd OpenChemE
python -m http.server 8000 --directory public     # the site, no build step
python templates/unit_conversions.py              # a template, no dependencies
```

---

## What's here

| | |
| --- | --- |
| **361 resource records** | Structured YAML across chemical engineering, chemoinformatics, bioengineering, medical engineering, and general engineering |
| **9 runnable templates** | Material balance notebook, reactor sizing, PID tuning, unit conversions, lab report, ELN entry, HAZOP checklist |
| **Reproducible workflows** | Snakemake conformer pipeline, CI actions for chemical data, a pinned Docker image |
| **A static site** | Search, explore, compare, and a detail page for every record |
| **Verification tiers** | Every claim carries a tier, a date, and evidence — or says plainly that it has none |

```
catalog/     ← the single source of truth (edit this)
  resources/   361 YAML records
  projects/    guided project records
  taxonomies/  controlled vocabulary
schemas/     JSON Schema; the validator enforces it
scripts/     validator, generators, smoke tests
lists/       GENERATED Markdown lists
public/      the website (public/r/ is GENERATED) — Vercel serves this
templates/   runnable engineering material
workflows/   Snakemake, GitHub Actions, Docker
tools/legacy/ superseded scripts, kept for reference
```

## How it works

**One source of truth.** `catalog/resources/*.yaml` is the only thing you edit. Everything else
is generated and CI fails if a generated file drifts:

```
catalog/resources/*.yaml
      ├─ scripts/generate_markdown_lists.py   → lists/awesome-*.md
      ├─ scripts/generate_search_index.py     → public/assets/data/resources.json
      └─ scripts/generate_resource_pages.py   → public/r/*.html, explore, compare
```

The previous structure kept resources in two hand-maintained places. They drifted to 45%
coverage before anyone noticed. That is the mistake this design exists to prevent — see
[ARCHITECTURE.md](ARCHITECTURE.md).

## Read this before trusting the catalog

**All 361 records are at verification tier 0. Licence and maintenance status are `unknown` on
nearly all of them.**

They were imported from Markdown bullets, which never recorded those fields, and the migration
environment could not reach the sources needed to confirm them — its egress policy denied roughly
99% of hosts, including all of `github.com`. An automated link check returned 403 on 358 of 386
URLs, which is indistinguishable from a dead link and therefore useless as evidence.

The alternative was to mark well-known projects as verified from memory. That would look like
progress and would be fabrication, so the catalog says tier 0 and explains why. Unknown fields
render as *not confirmed* in italics on every page, never as blanks that read like answers.

**Verifying records is the most useful contribution available right now**, and it needs no
special skill — pick a tool you know, confirm its licence from the project itself, open a PR.
[How verification works.](docs/verification-methodology.md)

## Quick start

```bash
pip install -r requirements-dev.txt

python scripts/validate_catalog.py             # 361 records, 0 errors
python -m pytest tests -q                      # 33 tests
python scripts/run_template_smoke_tests.py     # 16 checks on the templates

python -m http.server 8899 --directory public  # preview at localhost:8899
```

After changing anything in `catalog/`, regenerate and commit both halves together:

```bash
python scripts/generate_markdown_lists.py
python scripts/generate_search_index.py
python scripts/generate_resource_pages.py
```

## The website

Plain static HTML — no framework, no build step, no external requests. `vercel.json` points
Vercel at `public/`; pushing to the default branch deploys.

> **If a deployment 404s**, check *Vercel → Settings → General → Root Directory*. It must be
> **empty** (the repository root). Vercel looks for `vercel.json` and `public/` relative to that
> setting and finds neither if it points into a subdirectory.

## Contributing

| I want to… | Do this |
| --- | --- |
| Verify a record I know well | Confirm its licence and maintenance from the project, raise its tier, open a PR — **most valuable thing right now** |
| Add a resource | Copy an existing YAML in `catalog/resources/`, regenerate, PR |
| Fix a dead link | Edit the record's `canonical_url`, or open an issue |
| Add a guided project | See the [pilot record](catalog/projects/material-balance-with-recycle.yaml) and the [project schema](schemas/project.schema.json) |
| Ask something | [Discussions](https://github.com/laohei101/OpenChemE/discussions) |

Full guide: [CONTRIBUTING.md](CONTRIBUTING.md) · [Governance](GOVERNANCE.md) · [Roadmap](ROADMAP.md)

**We are looking for a process safety reviewer.** Several files touch HAZOP methodology and
regulatory material. They carry careful disclaimers, but no qualified process safety engineer has
reviewed them — see [MAINTAINERS.md](MAINTAINERS.md).

## Documentation

| Document | What it covers |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | How the pieces fit and why |
| [MIGRATION.md](MIGRATION.md) | What moved where, and the naming decision |
| [CLAUDE.md](CLAUDE.md) | Instructions for coding agents |
| [docs/verification-methodology.md](docs/verification-methodology.md) | What each tier means and how to promote a record |
| [docs/catalog-methodology.md](docs/catalog-methodology.md) | What gets in, what stays out |
| [ROADMAP.md](ROADMAP.md) | What is next, and what is deliberately not being built |

## Status

Phase 0 complete, Phase 1 started. The catalog, the generation pipeline, CI, and the trust UI
exist. Raising records above tier 0 is the current work.

The nine-repository split is **deferred** — `tools/legacy/setup_github.sh` still performs it, but
a monorepo is right until there are enough contributors to justify nine issue trackers.

## Licence

Prose, documentation, and catalog content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code, templates, workflows, and the website: MIT.
Linked projects keep their own licences — check before building on any of them.

Nothing here is engineering, clinical, or regulatory advice. Work affecting a real plant, patient,
or safety case needs review by a qualified professional who is accountable for it.

Contact: **yu.dai@mail.utoronto.ca**
