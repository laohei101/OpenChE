# Roadmap

Honest about what exists, what is next, and what is deliberately not being built.
Dates are omitted on purpose: this is volunteer-run and a date nobody is accountable for is noise.

---

## Now — Phase 0 complete, Phase 1 started

**Done**

- Root migration: everything is at the repository root; the nested tree is gone ([MIGRATION.md](MIGRATION.md))
- Canonical catalog: 361 records as YAML, one file each, with a JSON Schema
- Generation pipeline: Markdown lists, search index, and 361 detail pages all built from the catalog
- Staleness checks in CI, so the generated views cannot drift from the source again
- Verification tiers with an enforced evidence requirement, and a UI that never shows a bare badge
- Explore and Compare pages
- Template smoke tests: 16 checks against analytical identities and conservation laws
- Five CI workflows: catalog, python, site, links, security

**In progress**

- Raising records above tier 0. All 361 are tier 0 today, for the reason set out in
  [the verification methodology](docs/verification-methodology.md) — the migration environment
  could not reach the sources needed to confirm metadata. This is the single highest-value
  contribution available right now and needs no special skill, just care.

## Next — finish Phase 1

Ordered by how much they unblock.

1. **25 records at tier 2.** Start with the ones people actually reach for: DWSIM, Cantera,
   CoolProp, RDKit, Pyomo, IDAES, OpenFOAM, COBRApy, 3D Slicer, OpenSim.
2. **10 records at tier 3** — a quick start actually executed, environment recorded.
3. **Explore page filters.** The data supports filtering by platform, licence, access model, and
   tier; the page currently only groups by domain.
4. **Search improvements** — synonyms (`HYSYS` → process simulation), acronym expansion, typo
   tolerance for common tool names.
5. **Interactive compare.** The comparison set is currently a constant in the generator.
6. **The remaining import gap** — one bullet containing two links still needs splitting into
   two records.

## Then — Phase 2

Only after the catalog is trustworthy. A project lab built on unverified resources inherits the
problem.

- **Project Lab.** One pilot record exists ([material balance with recycle](catalog/projects/material-balance-with-recycle.yaml), tier 3).
  Spec §9.3 lists twelve; the schema is ready for the other eleven.
- **Dataset registry** with leakage warnings, recommended splits, and starter notebooks.
- **Models and flowsheets gallery** — DWSIM XML with per-version compatibility, no proprietary binaries.
- **Excel/Python bridge pack.** Excel is where most engineers actually work and the current
  content largely ignores that.
- **Request board** through GitHub Discussions, turning demand into a visible backlog.

## Later — Phase 3 and beyond

- Learning paths, including a module on reading and checking AI-generated code
- A local-only workbook audit CLI — no upload, no macro execution
- An `openche` CLI sharing the same catalog

## Not building

From spec §3.2, and worth restating because these are the things a project like this drifts into:

- A GitHub replacement, or a competitor to DWSIM, Aspen, or HYSYS
- A hosted simulation environment, or execution of untrusted submitted code
- An unreviewed engineering-answer chatbot
- Anything that signs off a HAZOP, relief sizing, regulatory, or clinical decision
- Copies of copyrighted standards
- Accounts, a database, or a custom community backend before there is demand to justify them

A **cited assistant** (spec §15) is conceivable eventually, and only after the catalog is mostly
verified. An assistant answering from tier-0 records would launder unverified data into
confident prose, which is worse than no assistant.

## When the repository splits

Spec §5.1 defers the nine-repository split. Revisit when **all** of:

- the catalog has more than a handful of regular contributors;
- individual areas have maintainers who want their own issue tracker;
- per-area issue traffic is high enough that one tracker is genuinely confusing;
- the generation pipeline has been stable for a few months.

`tools/legacy/setup_github.sh` still performs the split when that day comes.

## Contributing to any of this

[CONTRIBUTING.md](CONTRIBUTING.md). The most useful thing right now is verifying a record you
know well — pick one, confirm its licence and maintenance status from the project itself, and
open a pull request. That is a ten-minute job that makes the catalog measurably more honest.
