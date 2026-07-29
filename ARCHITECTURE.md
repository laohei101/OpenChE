# Architecture

How the pieces fit, and why they are arranged this way.

---

## The shape of it

```
catalog/resources/*.yaml ─── one record per resource, the ONLY source of truth
catalog/projects/*.yaml  ─── guided project records
catalog/taxonomies/      ─── controlled category vocabulary
        │
        │  validated by  scripts/validate_catalog.py  against  schemas/*.json
        │
        ├──> scripts/generate_markdown_lists.py  ──> lists/awesome-*.md
        ├──> scripts/generate_search_index.py    ──> public/assets/data/resources.json
        └──> scripts/generate_resource_pages.py  ──> public/r/*.html
                                                     public/explore.html
                                                     public/compare.html

public/  ─── the site: 3 hand-written pages + ~361 generated ones. Vercel serves this.
templates/ ─ runnable engineering material, checked by scripts/run_template_smoke_tests.py
workflows/ ─ Snakemake pipeline, reusable Actions, pinned Docker image
```

## Why one source of truth

The predecessor kept resources in two places: hand-edited Markdown lists, and a hand-maintained
Python tuple list inside the site build script. They diverged — the site indexed about 200 of
roughly 446 entries — and nobody noticed, because nothing compared them.

Now there is one place to edit and everything else is generated, with `--check` modes that fail
CI on drift. This is the central architectural decision and most of the rest follows from it.

## Why YAML, one file per record

- **Reviewable.** A pull request adding a resource is one new file. A change to a resource is a
  small diff in a named file. Compare with a 400-entry JSON array, where every change touches the
  same file and merge conflicts are constant.
- **Mergeable.** Two people adding different resources never conflict.
- **Commentable.** YAML takes comments, and the provenance notes on imported records matter.
- **Greppable.** `grep -l "spdx: UNKNOWN" catalog/resources/*.yaml` is the verification backlog.

The cost is ~361 small files, which is fine — the loader sorts them and the generators are
deterministic.

## Why the schema is strict about verification

`schemas/resource.schema.json` contains a conditional: a `verification.tier` of 1 or more
*requires* `checked_at`, `checked_by`, and at least one evidence entry. The validator adds that
tier 2 with `spdx: UNKNOWN` is a contradiction.

This is deliberate belt-and-braces. The failure mode this project is built to avoid is a
confident-looking claim nobody checked, and the cheapest place to stop it is at the schema, before
it ever reaches a page.

## Why the site is plain static HTML

No Jekyll, no framework, no build step, no dependencies.

- Vercel serves `public/` with zero configuration, and GitHub Pages would serve it with a
  `.nojekyll` file. Deployment cannot break in an interesting way.
- Contributors can edit a page without installing Ruby or Node.
- It loads fast on conference wifi, which is where people actually open it.

The cost: the header and footer are duplicated across the three hand-written pages
(`index.html`, `get-started.html`, `search.html`). That is a real cost, accepted knowingly. The
361 generated pages share a single header function in the generator, so the duplication is
bounded at three.

**`public/` rather than `site/`** — the spec suggests `site/`. Vercel's zero-config default is
`public/`, `vercel.json` names it explicitly, and this deployment 404'd until that was set up.
Renaming for consistency would risk re-breaking it for no visible gain. See MIGRATION.md §5.

## Why search runs in the browser

`public/assets/js/search.js` fetches a ~150 KB JSON index and scores in the browser: no server,
no tracking, works offline once loaded, and nothing to operate.

Matching is a **weighted token score**, not fuzzy similarity — every typed token must appear
somewhere, and a hit in the name outranks a hit in the description. For a few hundred records
this is more predictable than a similarity threshold somebody would have to tune, and it never
surfaces a confusing near-miss. The budget (spec §20) is 500 KB; a test enforces it.

## Why the template tests check identities, not outputs

`scripts/run_template_smoke_tests.py` does not compare against recorded outputs. It checks:

- **Analytical identities** — for a second-order reaction at equimolar feed,
  `V_CSTR/V_PFR = 1/(1−X)` exactly, independent of rate constant and concentration.
- **Conservation laws** — mass closes; a CSTR cascade approaches the PFR from above, never below.
- **Round trips** — every unit converts out and back to itself across all 131 units.
- **Refusals** — the converter must reject affine temperature and cross-quantity conversion.

A regression baseline tells you the output changed. These tell you whether it was ever right.
That distinction is the difference between a test suite and a snapshot.

## Data flow when you add a resource

```
1. write catalog/resources/your-tool.yaml
2. validate_catalog.py     → schema, slug, URL uniqueness, taxonomy, references
3. generate_*.py           → lists, search index, detail page
4. commit YAML + generated output together
5. CI re-runs every generator with --check and fails if they disagree
```

Step 4 matters: a commit with the YAML but not the regenerated output fails CI, by design.

## What is deliberately absent

No database, no authentication, no server-side code, no user accounts, no analytics, no external
requests from any page. Adding any of these needs a reason stronger than "we might want it" —
each one turns a repository anyone can fork and run into a service somebody has to operate.
