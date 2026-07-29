# Contributing to Open ChemE Hub

Thanks for being here. This guide covers every repository in the organisation. It should take
under five minutes to read, and most contributions take less time than that to make.

---

## Table of contents

- [Ways to contribute](#ways-to-contribute)
- [Adding a resource to an awesome list](#adding-a-resource-to-an-awesome-list)
- [What we accept and what we don't](#what-we-accept-and-what-we-dont)
- [Contributing a template](#contributing-a-template)
- [Contributing a workflow](#contributing-a-workflow)
- [Working on the website](#working-on-the-website)
- [Style guide](#style-guide)
- [Pull request process](#pull-request-process)
- [Review and merge expectations](#review-and-merge-expectations)
- [Licensing of contributions](#licensing-of-contributions)

---

## Ways to contribute

> **Structure changed.** Resources now live as YAML in `catalog/resources/`, and the Markdown
> lists in `lists/` are **generated** from them. Editing a list by hand no longer works — CI
> regenerates and fails with a diff. See [MIGRATION.md](MIGRATION.md) and [CLAUDE.md](CLAUDE.md).

| I want to… | Do this |
| --- | --- |
| **Verify a record you know well** | Confirm its licence and maintenance from the project itself, raise the tier with evidence, open a PR. **Most valuable contribution right now** — see [verification methodology](docs/verification-methodology.md) |
| Add a tool, dataset, or course | Add a YAML file to `catalog/resources/`, run the generators, commit both |
| Report a dead link | Open a **Broken link** issue (or just fix it in a PR) |
| Share a spreadsheet, notebook, or script others rebuild constantly | PR to [`templates`](https://github.com/OpenChemE/templates) |
| Share a reproducible pipeline | PR to [`workflows`](https://github.com/OpenChemE/workflows) |
| Ask "does anyone know a good tool for X?" | [Discussions → Q&A](https://github.com/orgs/OpenChemE/discussions) |
| Propose a new list or a new section | [Discussions → Ideas](https://github.com/orgs/OpenChemE/discussions) |
| Fix a typo | PR, no issue needed, merged on sight |

You do not need permission to open a pull request. You do not need to open an issue first unless
you're proposing something structural (a new list, a renamed section, a policy change).

---

## Adding a resource to an awesome list

Copy an existing record and edit it:

```bash
cp catalog/resources/cantera.yaml catalog/resources/your-tool.yaml
$EDITOR catalog/resources/your-tool.yaml
python scripts/validate_catalog.py
python scripts/generate_markdown_lists.py
python scripts/generate_search_index.py
python scripts/generate_resource_pages.py
```

Commit the YAML **and** the regenerated output together — a commit with only one half fails CI.

**Leave `license`, `maintenance_status`, and `access.model` as `unknown` unless you actually
confirmed them from the project itself.** An honest `unknown` is a work item somebody can close.
A plausible guess is a lie that survives review because it looks like data.

The three parts:

1. **Link.** Canonical project home — the repo or the official docs, not a blog post about it,
   not a Google redirect, not a link with tracking parameters.
2. **Description.** One sentence, no trailing period after tags, starting with a noun or a verb
   phrase, not "A library that…". Say what it *does*, not that it's great. Under ~140 characters.
3. **Tags.** Backticked, lower-case, optional. Use them for language or type:
   `python` `julia` `c++` `matlab` `r` `gui` `web` `dataset` `book` `course` `commercial-free-tier`.

**Where it goes.** If a resource fits two sections, pick the one where someone would look for it
first, and don't list it twice. If it fits no section, propose the section in your PR description
rather than wedging it in.

---

## What we accept and what we don't

**We accept resources that are:**

- **Maintained or complete.** A commit in the last ~2 years, *or* a finished artefact that doesn't
  need maintenance (a textbook, a standard, a reference dataset).
- **Openly available.** Free to use for the reader, ideally under an OSI or Creative Commons
  licence. Free tiers of commercial tools are fine when the free tier is genuinely usable — tag
  them `commercial-free-tier` so nobody is surprised.
- **Relevant to the list.** Broadly useful to practitioners in that field, not just to your lab.
- **Real.** You have used it, or read it, or can point to someone who has.

**We decline:**

- **Paywalled or licence-gated tools** with no meaningful free path. (Aspen Plus itself doesn't get
  an entry; open alternatives to it do, and `templates/aspen_simulation_tips.md` covers working
  alongside it.)
- **Abandoned projects** — last release five years ago, open issues untouched, docs 404ing.
- **Self-promotion without substance.** Your own project is welcome. Say it's yours in the PR
  description, and hold it to the same bar: docs, a licence, an example that runs.
- **Link farms, SEO listicles, and content mills**, including "top 10 chemical engineering
  software" pages.
- **Predatory journals and pay-to-publish conferences** in the community sections.
- **Anything whose primary purpose is to circumvent a licence** — cracked binaries, licence
  servers, "free Aspen" repositories. These get closed without discussion.

Rejection is about fit, not about quality or about you. If a PR is declined, the reviewer will say
which criterion it missed.

---

## Contributing a template

A good template is something you'd hand a new hire on their first day.

Requirements:

- **It runs.** Clone-and-execute with the dependencies named in the file header, no manual edits
  needed to get *some* output.
- **It's commented for a learner.** Explain the engineering, not the Python. `# solve the linear
  system` is noise; `# Overall + component balances give 3 equations in 3 unknowns` is the point.
- **Units are explicit** in variable names or comments, everywhere. `m_dot_feed_kg_s`, not `m1`.
- **Numbers are plausible.** Reactor volumes in the litres-to-cubic-metres range, temperatures
  that don't decompose the feed, pressures a real vessel could hold.
- **It has a header block** with: purpose, author, licence (MIT), dependencies, and one line on
  what to change first.
- **Add it to `templates/README.md`** in the same PR, in the table, with a one-line description.

Notebooks: clear all outputs before committing (`jupyter nbconvert --clear-output --inplace`) so
diffs stay readable — except where a rendered plot is the point of the template, in which case say
so in the PR.

---

## Contributing a workflow

Workflows carry a higher bar because people will trust them with real analyses.

- **Pin your dependencies.** `environment.yaml` with versions, or a Docker tag, not `latest`.
- **Ship a tiny test case** that runs in under a minute on a laptop, so CI and newcomers can both
  verify it. Put inputs under `test_data/`.
- **Document the compute envelope**: expected runtime, memory, whether it needs a GPU or a cluster.
- **Declare the science**, not just the code: what method, what assumptions, what it is *not*
  valid for. A conformer generator that skips a DFT refinement step should say so loudly.
- **No credentials, no institutional paths, no licensed binaries** in the repo. Read from
  environment variables and document them.

---

## Working on the website

`hub-website` is plain Jekyll and builds with GitHub Pages' default toolchain.

```bash
cd hub-website/docs
bundle install          # first time only
bundle exec jekyll serve --livereload
# http://localhost:4000
```

The search index at `assets/data/resources.json` is the site's own copy of the lists. If you add a
resource to a list and want it searchable immediately, add the matching JSON entry in the same PR;
otherwise the next index refresh picks it up. Keep the JSON valid — a trailing comma silently
breaks search for everyone.

---

## Style guide

**Prose.** British or American spelling both fine, be consistent inside a file. Address the reader
as "you". Prefer short sentences. No exclamation marks in reference material.

**Markdown.** ATX headings (`##`), hyphen bullets, fenced code blocks with a language tag, one
sentence per line is welcome but not required. Wrap at 100 characters where practical.

**Python.** PEP 8, four spaces, type hints on public functions, docstrings in NumPy style. Format
with `black -l 100` and lint with `ruff` if you have them; nobody will block a PR over a line
length.

**Commits.** Imperative mood, scoped prefix where it helps:

```
list(cheme): add Ipopt to Process Simulation
templates: fix energy balance sign in reactor skeleton
docs: correct broken CoolProp link
```

**Commit history.** Messy history is fine — we squash-merge.

---

## Pull request process

1. **Fork** (or push a branch, if you have write access) and make your change.
2. **One topic per PR.** Adding six resources to one list is one topic. Adding resources *and*
   restructuring sections is two.
3. **Fill in the PR checklist.** It exists so reviewers don't have to ask the same four questions.
4. **CI runs a link checker** on list changes. If it flags your link, check whether the site
   blocks automated requests — say so in a comment and a maintainer will verify by hand.
5. **Respond to review.** Reviewers will suggest concrete edits you can accept with one click.

Draft PRs are welcome for work in progress. Mark them ready when you want eyes on them.

---

## Review and merge expectations

- A maintainer aims to respond within **one week**. This is volunteer-run; a quiet PR is a busy
  maintainer, not a rejected contribution. Ping the thread after a week — it's not rude.
- **Single-line list additions** need one approval.
- **New sections, templates, and workflows** need one approval plus a maintainer, and for
  workflows, evidence the test case runs.
- **Changes to `.github`** need two maintainer approvals, since they affect every repo.

---

## Licensing of contributions

By contributing you agree that your contribution is licensed to the project under:

- **CC BY 4.0** for list entries, documentation, and website prose.
- **MIT** for code, templates, workflows, and configuration.

Only contribute material you have the right to contribute. Do not paste text from a textbook, a
vendor manual, a standard, or a paper into a list description — write your own sentence. Correlations
and equations are facts and are fine to implement; the wording around them is not.
