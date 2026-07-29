# Catalog methodology

What gets in, what stays out, and how records are structured.

---

## Inclusion

A resource belongs in the catalog if it is:

- **Freely usable.** Open source, open access, or a genuinely usable free tier. Free tiers are
  recorded as `access.model: free-tier` with `paid_features_exist: true`, so nobody is surprised
  at the licence dialog.
- **Maintained, or complete.** Activity in roughly the last two years — or a finished artefact
  that does not need maintenance, such as a textbook, a standard, or a reference dataset.
- **Relevant** to practitioners in one of the ten domains, not only to one research group.
- **Real.** Someone has used it, read it, or can point to someone who has.

## Exclusion

- **Paywalled tools with no meaningful free path.** Aspen Plus gets no record; open alternatives
  to it do, and `templates/aspen_simulation_tips.md` covers working alongside it.
- **Abandoned projects** — last release many years ago, issues untouched, docs 404ing. An
  *archived but historically important* project may stay, marked `archived` with its limitations
  recorded and a successor named.
- **Self-promotion without substance.** Your own project is welcome; disclose it and meet the
  same bar.
- **Link farms, SEO listicles, predatory conferences.**
- **Anything whose purpose is circumventing a licence.** Closed without discussion.

## One record per resource

Not per mention. During the migration, `ht` appeared under both thermodynamics and unit
operations; those merged into one record carrying both categories. A resource spanning two
domains (OpenFOAM: chemical engineering and bioengineering) carries both domains and appears in
both lists, generated from the same record.

The validator enforces this by rejecting duplicate canonical URLs.

## Field guidance

**`summary`** — one sentence, the contributor's own words, saying what it *does*. Not marketing
copy, not pasted from the project's site. "Thermodynamic property library" tells a reader nothing;
name the model families and the coverage.

**`license.spdx`** — an SPDX identifier, or `UNKNOWN`. **Never guess.** A wrong licence is worse
than an absent one, because someone may rely on it. `UNKNOWN` is a work item; a guess is a
liability.

**`access.model`** — how a reader actually gets to use it. The distinction between `open-source`,
`open-source-with-supporter-editions`, `free-tier`, and `free-for-academic-use` is exactly what a
reader needs before spending an afternoon installing something.

**`limitations`** — where it stops working. Often the most useful field on the page, and the one
most lists omit entirely.

**`use_when` / `avoid_when`** — plain guidance. "Avoid when you need dynamic simulation" saves
more time than any feature list.

**`categories`** — from `catalog/taxonomies/categories.yaml`. Adding a category is deliberate: an
unbounded list groups nothing. Propose new ones in a PR that also assigns at least two records.

## Provenance

Imported records carry `source_list` and `source_section`, recording which legacy Markdown list
they came from. Safe to drop once a record has been hand-curated; useful until then for knowing
how much scrutiny a record has had.

## Descriptions and copyright

Write your own sentence. Do not paste from a project's website, a textbook, a standard, or a
paper. Equations and correlations are facts and are fine to implement; the wording around them is
someone's copyrighted prose.

## Statistics, honestly

The catalog reports its own state, including the parts that look bad. Today: 361 records, all at
verification tier 0, with licence unknown on nearly all of them. That number appears on the
Explore page rather than being buried, because a reader deciding how much to trust the catalog
needs it more than we need it to look finished.
