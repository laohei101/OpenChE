# CLAUDE.md — instructions for coding agents

Read this before changing anything. It is short on purpose.

---

## What this repository is

A curated, verifiable catalog of open chemical engineering resources, plus the runnable templates
and the static site built from it. **It is not a simulator, a social network, or a chatbot.** It
organises and validates other people's tools.

## The one rule that matters

**`catalog/` is the only source of truth. Everything else is generated.**

```
catalog/resources/*.yaml   ← edit this
        │
        ├─ scripts/generate_markdown_lists.py   → lists/awesome-*.md
        ├─ scripts/generate_search_index.py     → public/assets/data/resources.json
        └─ scripts/generate_resource_pages.py   → public/r/*.html, explore.html, compare.html
```

Never hand-edit a generated file. CI runs each generator with `--check` and fails with a diff if
the committed output has drifted. The previous version of this project had two hand-maintained
copies of the resource list and they diverged to 45% coverage; that is the mistake this structure
exists to prevent.

## Commands

```bash
pip install -r requirements-dev.txt

python scripts/validate_catalog.py             # schema, slugs, URLs, taxonomy, references
python scripts/generate_markdown_lists.py      # add --check in CI
python scripts/generate_search_index.py        # add --check in CI
python scripts/generate_resource_pages.py      # add --check in CI
python -m pytest tests -q                      # generation code
python scripts/run_template_smoke_tests.py     # the engineering templates
python -m doctest templates/unit_conversions.py

python -m http.server 8899 --directory public  # preview; then:
node scripts/site_smoke_test.js                # needs playwright
```

Run the validator and the generators after any catalog change. The `--check` flags are what CI
uses; run them locally before pushing and you will not be surprised.

## Content rules

These are not style preferences. Violating them is the failure mode this project is built to
avoid.

1. **Never invent a resource, URL, licence, version, or benchmark number.** If you do not know,
   write `unknown` and open a follow-up issue. An honest gap is a work item; a plausible guess is
   a lie that survives review because it looks like data.

2. **Never claim verification that did not happen.** Tier 0 is the default and it is correct.
   Tiers 1–4 each require dated evidence, and the schema enforces it. See
   [`docs/verification-methodology.md`](docs/verification-methodology.md).

3. **Never state a numerical result without units, tolerance, and provenance.** "The duty is
   250 kW" is not a claim anyone can check. Say what version of what tool, with what inputs, and
   what it was compared against.

4. **Never pin a dependency loosely in a reproducible workflow.** `workflows/*/environment.yaml`
   and the Dockerfile pin exact versions. `requirements-dev.txt` is tooling and uses lower bounds;
   do not confuse the two.

5. **Never remove a limitation or a caveat to make something read better.** The isothermal
   warning in `reactor_design_skeleton.py` and the disclaimer atop `safety_checklist.md` are the
   most important text in those files.

6. **Never add a launch button, quick start, or "works with version X" claim that has not been
   run.** Spec §8.6: an untested launch button is worse than none.

## Safety constraints

- Nothing here signs off a HAZOP, a relief-device size, a regulatory submission, or a clinical
  decision. Every page carries that disclaimer; do not remove it.
- Do not reproduce copyrighted standards. Link to the issuing body, name the standard, summarise
  at a high level. ISO and IEC text does not go in this repository.
- Do not commit credentials, licence-server addresses, private plant data, or patient data.
- Safety templates state that they are prompts and educational aids, that they do not replace
  qualified review, and that a completed checklist is not evidence of safety. That framing is
  load-bearing.

## Architecture facts worth knowing before you change things

- **The site is plain static HTML.** No Jekyll, no framework, no build step. Three hand-written
  pages plus ~361 generated ones. Adding a build step needs a real reason.
- **The site lives in `public/`,** not `site/`, because Vercel serves it with zero configuration
  and `vercel.json` names it. This deviates from the spec deliberately — see
  [`MIGRATION.md`](MIGRATION.md) §5.
- **The header and footer are duplicated across the three hand-written pages.** That is the
  accepted cost of having no templating. Change one, change all three, or move them into the
  generator.
- **Verification tier colours are reinforcement, never the message.** Every tier shows a number
  and a word, because status must not be communicated by colour alone (spec §16.3).
- **The nine-repository split is deferred.** `tools/legacy/setup_github.sh` works but is not the
  deployment path. See [`ROADMAP.md`](ROADMAP.md).

## Adding a resource

```bash
cp catalog/resources/dwsim.yaml catalog/resources/your-tool.yaml
# edit: slug, name, canonical_url, summary, domains, categories, tags
# leave licence/maintenance/access as unknown unless you actually confirmed them
python scripts/validate_catalog.py
python scripts/generate_markdown_lists.py && python scripts/generate_search_index.py \
  && python scripts/generate_resource_pages.py
```

Commit the YAML **and** the regenerated output together. A commit with only one half fails CI.

## Where things are

| Path | What |
| --- | --- |
| `catalog/resources/` | 361 resource records — the source of truth |
| `catalog/projects/` | Guided project records |
| `catalog/taxonomies/` | Controlled category vocabulary |
| `schemas/` | JSON Schema for records; the validator enforces these |
| `scripts/` | Validator, generators, smoke tests |
| `scripts/openche/catalog.py` | Shared loading — start here to understand the data model |
| `lists/` | **Generated** Markdown lists |
| `public/` | The website; `public/r/` is **generated** |
| `templates/` | Runnable engineering templates |
| `workflows/` | Snakemake pipeline, GitHub Actions, Docker image |
| `tools/legacy/` | Superseded scripts, kept for reference |
| `tests/` | Tests for the generation code |

## Scope discipline

The [product spec](docs/) describes phases well beyond what exists. Implemented: Phase 0
(foundation, canonical catalog, CI) and part of Phase 1 (detail pages, comparison, explore).

Do **not** build, without being asked: authentication, a database, user profiles, an AI
assistant, a hosted notebook runner, a custom community backend, or a simulator. Spec §3.2 lists
these as non-goals and they are non-goals for good reasons.
