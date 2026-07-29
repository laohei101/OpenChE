# Migration map

**What moved, where it went, and why.** Written before the move, per spec §7.1.

Everything that used to live under the nested `open-cheme-hub/` tree is now at the repository
root. The nested tree is gone — nothing in it was deleted without a destination recorded here.

---

## 1. Path map

| Old path | New path | Notes |
| --- | --- | --- |
| `open-cheme-hub/templates/` | `templates/` | `git mv`, history preserved |
| `open-cheme-hub/workflows/` | `workflows/` | `git mv`, history preserved |
| `open-cheme-hub/.github/CONTRIBUTING.md` | `CONTRIBUTING.md` | Root community health file |
| `open-cheme-hub/.github/CODE_OF_CONDUCT.md` | `CODE_OF_CONDUCT.md` | |
| `open-cheme-hub/.github/SECURITY.md` | `SECURITY.md` | |
| `open-cheme-hub/.github/SUPPORT.md` | `SUPPORT.md` | |
| `open-cheme-hub/.github/profile/README.md` | `docs/org-profile-README.md` | Kept for if the org is created later |
| `open-cheme-hub/.github/.github/ISSUE_TEMPLATE/*` | `.github/ISSUE_TEMPLATE/` | |
| `open-cheme-hub/.github/.github/PULL_REQUEST_TEMPLATE.md` | `.github/PULL_REQUEST_TEMPLATE.md` | |
| `open-cheme-hub/awesome-*/README.md` | `lists/awesome-*.md` | **Now generated** — see §2 |
| `open-cheme-hub/awesome-chemical-engineering/CONTRIBUTING.md` | `docs/list-contributing-chemical-engineering.md` | Folded into the submission guide over time |
| `open-cheme-hub/awesome-*/.github/workflows/link-check.yml` | `.github/workflows/links.yml` | Five identical copies collapsed to one |
| `open-cheme-hub/setup_github.sh` | `tools/legacy/setup_github.sh` | **Not the deployment path** — see §4 |
| `open-cheme-hub/hub-website/build_index.py` | `tools/legacy/build_index_legacy.py` | Superseded by `scripts/generate_search_index.py` |
| `open-cheme-hub/hub-website/docs/` | *(deleted)* | Was a mirror of `public/`; the mirror was the drift risk |
| `open-cheme-hub/awesome-*/LICENSE` | *(deleted)* | Five copies of the root `LICENSE` |
| `open-cheme-hub/README.md` | Folded into root `README.md` | |

## 2. The lists became generated artifacts

This is the substantive change, not a file move.

**Before:** `awesome-*/README.md` was hand-edited, and `hub-website/build_index.py` held a second,
hand-maintained copy of the same resources as Python tuples. The two had already drifted — the
website indexed about 200 of roughly 446 entries.

**After:** `catalog/resources/*.yaml` is the single source of truth. One file per resource.
Everything else is generated:

```
catalog/resources/*.yaml   ← the only thing you edit
        │
        ├─ scripts/generate_markdown_lists.py   → lists/awesome-*.md
        ├─ scripts/generate_search_index.py     → public/assets/data/resources.json
        └─ scripts/generate_resource_pages.py   → public/r/*.html
                                                  public/explore.html
                                                  public/compare.html
```

CI runs each generator with `--check` and fails if the committed output differs, so the copies
cannot drift again.

### How the import went

| | |
| --- | --- |
| Entries parsed from the five lists | 383 |
| Records written | 371 |
| Cross-list duplicates merged (kept both domains) | 11 |
| Same-URL near-duplicates merged | 10 |
| **Final record count** | **361** |
| Unparsed lines needing manual attention | 1 |

The two merge classes were different problems:

- **Cross-list** — OpenFOAM appeared in both the chemical engineering and bioengineering lists.
  One resource, two domains. The record now carries both.
- **Same-URL** — `ht` and "HTRI alternatives — ht exchanger sizing" were one library under two
  names. The shorter slug won; the discarded description is preserved in
  `verification.notes` rather than thrown away.

The one unparsed line is a bullet containing two links (`[NumPy](…) / [SciPy](…)`), which is one
resource per line's worth of malformed. Tracked as follow-up; splitting it into two records is a
two-minute job for whoever gets there first.

### Every imported record is verification tier 0

Not laziness — accuracy. A Markdown bullet carries a name, a URL, a sentence and some tags.
It carries nothing about licence, maintenance status, or platform support. Those fields are
written as `unknown`, and the detail pages render them as *not confirmed* in italics rather than
leaving a blank that reads like an answer.

Promoting a record to tier 2 requires confirming its metadata against authoritative sources.
That could not be done during this migration: the build environment's egress policy denied
connections to roughly 99% of hosts, including all of `github.com`. Claiming tier 2 anyway would
have been fabrication. See [`docs/verification-methodology.md`](docs/verification-methodology.md).

## 3. Naming

The spec (§5.2) standardises on **OpenChE**. The repository, its Vercel deployment, and every
committed cross-reference use **OpenChemE**, which is what the maintainer confirmed and what
`github.com/laohei101/OpenChemE` actually is.

**Decision: OpenChemE.** Renaming to OpenChE would break every link in the tree until the GitHub
repository is also renamed, and would re-break a Vercel deployment that was just fixed. The
naming inconsistency the spec calls out (§1.1 item 8) is resolved by picking one name and using
it everywhere — which is done — not by picking the spec's spelling specifically.

Retired spellings: `open-cheme-hub`, `Open ChemE Hub` as a repository or URL component. The
display name "Open ChemE Hub" is retained in site prose and headings, because it reads better
than a bare token and appears nowhere that a machine resolves.

If you do want `OpenChE`: rename the GitHub repository (Vercel follows automatically), then run
`tools/legacy/setup_github.sh --org OpenChE --rewrite-urls`, whose rewrite pass handles the
lowercase forms needed for `ghcr.io` and GitHub Pages hostnames.

## 4. The nine-repository split is deferred

`tools/legacy/setup_github.sh` still works and still creates nine repositories. It is not the
deployment path.

Spec §5.1 is right that a monorepo is correct for this stage. Nine repositories means nine issue
trackers, nine CI configurations, and a cross-repository coordination problem for a project that
does not yet have enough contributors to fill one. Revisit when the conditions in
[`ROADMAP.md`](ROADMAP.md) are met: independent maintainers per area, and per-area issue traffic
that justifies the separation.

## 5. Deviation from the spec: the site lives in `public/`, not `site/`

Spec §8.1 suggests `/site` or `/docs`. The site is in `public/`.

The reason is concrete rather than aesthetic: Vercel serves `public/` with zero configuration,
`vercel.json` also names it explicitly, and this deployment 404'd until that was set up. Renaming
the directory for naming consistency would risk re-breaking a deployment that a user is waiting
on, in exchange for nothing a reader can see. Documented here so the next person knows it was a
decision and not an oversight.

## 6. What did not move

- `public/` — already at the root and already deployed.
- `vercel.json` — must be at the repository root for Vercel to read it.
- `LICENSE` — already correct.

## 7. Verifying the migration

```bash
pip install -r requirements-dev.txt
python scripts/validate_catalog.py            # 361 records, 0 errors
python scripts/generate_markdown_lists.py --check
python scripts/generate_search_index.py --check
python scripts/generate_resource_pages.py --check
python -m pytest tests -q                     # 33 passed
python scripts/run_template_smoke_tests.py    # 16/16 checks
```

Nothing was deleted that is not accounted for in §1. To confirm, `git log --follow` any moved
file: the history crosses the rename.
