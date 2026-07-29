# Contributing to Awesome Chemical Engineering

The [organisation-wide guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md)
applies here. This file covers what's specific to this list.

## The one-line format

```markdown
- [Name](canonical-url) — What it does, in one sentence. `tag` `tag`
```

Em dash (`—`), not a hyphen. Description under ~140 characters. Tags lower-case in backticks.

## Section-specific expectations

**Process Simulation.** Say what kind of simulator it is — sequential-modular, equation-oriented,
or dynamic — because that determines whether it can do what a reader needs. If it's CAPE-OPEN
compliant, say so; interoperability is often the deciding factor.

**Thermodynamics & Physical Properties.** Name the model families it implements (cubic EOS, SAFT,
activity coefficient models, Helmholtz). "Thermodynamic property library" tells a reader nothing.
Note the compound coverage if it's a database.

**Reaction Engineering.** Mention what mechanism formats it reads (Chemkin, YAML, CTI) and whether
surface chemistry is supported.

**Unit Operations & Equipment Design.** Say which correlations or standards the sizing follows —
Bell–Delaware, TEMA, API 520 — since that's what a reader will be checked against.

**Process Control & Safety.** Safety entries carry extra weight. Regulatory documents should link
to the issuing body, never a mirror. Consequence models should say which correlations they
implement and that they are screening tools, not a substitute for a validated study.

**Data & Benchmarks.** State the licence and whether bulk download is permitted. A database you
can only query one compound at a time through a web form is worth listing, but say so.

**Learning Resources.** Free to the reader, no registration wall. Give the level: undergraduate,
graduate, or professional. Course entries should note whether materials are complete or just a
syllabus.

**Community & Conferences.** Established meetings and forums only. We don't list predatory
conferences — if the call for papers arrived by unsolicited email promising publication in two
weeks, it isn't going in.

## Additional rules for this list

1. **Units and standards matter.** If a tool is hard-wired to one unit system or one code of
   practice, say so in the description. Readers get burned by this.
2. **Don't list wrappers as if they were tools.** A thin Python binding belongs as a mention in the
   parent project's entry, not its own line.
3. **Commercial tools with academic licences** are borderline. Free-for-teaching, install-anywhere
   tools are fine with `commercial-free-tier`. Tools requiring a named-institution licence server
   are not.
4. **Nothing that circumvents licensing.** Cracks, keygens, and "free Aspen" mirrors are closed
   without discussion and may result in a block.

## Checking your PR

The CI link checker runs `lychee` over changed Markdown. Some publisher and government sites block
automated requests and will show as failures — comment saying you verified by hand and a maintainer
will confirm.

## Removing an entry

Removals are contributions too. Open a PR deleting the line, with the reason: dead project, dead
link, superseded by another entry, or licence change that puts it out of scope. Removals of
maintained projects need a maintainer's agreement; obvious rot doesn't.
