# open-cheme-hub — local source tree

**This directory is the source for a nine-repository GitHub organisation.** Each subdirectory
becomes its own repository; `setup_github.sh` creates them and pushes.

Nothing here has been published yet. Read this file before running the script.

---

## What gets created

| Directory → repository | What it is |
| --- | --- |
| `.github/` | Organisation profile, contributing guide, code of conduct, issue and PR templates. Applies to every other repo |
| `awesome-chemical-engineering/` | 82 curated entries: process simulation, thermodynamics, reaction engineering, unit ops, optimisation, control, safety, CFD, data, courses |
| `awesome-chemoinformatics/` | 96 entries: molecular toolkits, descriptors, QSAR, ML for chemistry, retrosynthesis, quantum chemistry, databases, visualisation |
| `awesome-bioengineering/` | 82 entries: bioprocess modelling, genome-scale metabolic models, synthetic biology, protein engineering, biomaterials, tissue engineering |
| `awesome-medical-engineering/` | 93 entries: device design, biomechanics, medical imaging, physiological signals, regulatory standards, health informatics |
| `awesome-general-engineering/` | 93 entries: CAD/CAE, control, signal processing, embedded and IoT, industrial protocols, reliability, documentation, ethics |
| `templates/` | 9 fork-and-edit files: material balance notebook, reactor sizing, PID tuning, unit conversions, lab report, ELN entry, safety checklist, Aspen version-control guide, annotated DWSIM flowsheet |
| `workflows/` | Snakemake conformer pipeline, a structure-rendering GitHub Action, and a pinned Docker image with RDKit + Open Babel + Cantera |
| `hub-website/` | Jekyll site for GitHub Pages, with client-side search over ~200 indexed resources |

Around 446 curated entries in total, plus the runnable material.

---

## Publishing

```bash
# 1. Install and authenticate the GitHub CLI
gh auth login          # or: export GITHUB_TOKEN=ghp_xxx  (scopes: repo, admin:org, workflow)

# 2. See exactly what would happen
./setup_github.sh --dry-run --org your-org-name --rewrite-urls

# 3. Do it
./setup_github.sh --org your-org-name --rewrite-urls
```

`--rewrite-urls` matters. Every cross-reference in these files points at `open-cheme-hub`;
without the rewrite, your published copy links back to an organisation you don't control.

The script is idempotent — a second run reports what already exists and pushes only what
changed. Run `./setup_github.sh --help` for the rest of the options.

---

## Four things to change before you publish

1. **The organisation name.** `open-cheme-hub` is almost certainly taken. Pass `--org` with
   yours. GitHub's API has no endpoint for creating a free organisation, so if the org doesn't
   exist yet the script tells you where to click; it takes about thirty seconds. Or use
   `--user` to publish under your own account.

2. **The contact addresses.** `conduct@open-cheme-hub.org` and `security@open-cheme-hub.org`
   appear in `CODE_OF_CONDUCT.md` and `SECURITY.md` and do not exist. Replace them with
   addresses you actually monitor. A code of conduct with an unreachable reporting address is
   worse than not having one, because it looks like a promise.

3. **`baseurl` in `hub-website/docs/_config.yml`.** `""` for an organisation site at
   `<org>.github.io`, `/hub-website` for a project site. Getting this wrong is the most common
   Pages failure: the page renders and every stylesheet and link 404s.

4. **The list contents themselves.** See the verification status below — the links have
   **not** been machine-checked. Before you point colleagues at a list, check the entries in
   your own field and remove anything you wouldn't recommend in person. A curated list is
   worth exactly what its curator has actually checked, and once you publish, that curator
   is you.

---

## Verification status of the lists

**Read this before treating any entry as confirmed.**

Every URL was written from recall of the project, not from a live fetch. An automated check was
attempted and produced no usable signal: the build environment's egress policy denied the
connection for ~99% of hosts (HTTP 403 on CONNECT, including all of `github.com`), which is
indistinguishable from a dead link at the network layer. **No link in these lists has been
confirmed to resolve.**

What that means concretely:

- Expect some **URL drift** — projects that moved host, docs that reorganised, pages that
  renamed. The descriptions should still be accurate even where a link needs updating.
- A small number of entries were **removed before publication** because they were plausible-
  sounding names rather than projects I could actually place: 17 entries across the chemical
  engineering, bioengineering, medical and general lists. Six more had a real project behind
  them but the wrong name or URL and were corrected. The counts above are post-cleanup.
- The remaining entries are ones I can place as real projects. That is a weaker claim than
  "verified", and it is the honest one.

**Your first action after publishing** should be to run the link checker, which every list
repository already carries at `.github/workflows/link-check.yml`:

```
Actions -> Link check -> Run workflow
```

It runs `lychee` over every Markdown file, posts a report to the job summary, and on its weekly
schedule opens a tracking issue for anything broken. Expect a handful of failures on the first
run — publisher and government sites (ISO, IEC, FDA, Elsevier) routinely block automated
requests, and those are false positives to verify by hand rather than remove.

---

## Verifying the runnable material

Everything runnable here has been executed:

```bash
cd templates
python3 unit_conversions.py                  # worked examples + sanity checks
python3 -m doctest unit_conversions.py       # passes clean
python3 reactor_design_skeleton.py -X 0.9 --sweep
python3 pid_tuning.py --identify

cd ../hub-website
python3 build_index.py                       # regenerates the search index, validates it

cd ..
bash -n setup_github.sh                      # syntax check
./setup_github.sh --help
```

The notebook's cells execute in order and every material balance closes to machine precision.
The Snakemake pipeline and the Docker image need RDKit and Cantera, so they have not been
executed in this tree — build the image first if you want to verify them:

```bash
cd workflows/docker && docker build -t chem-toolkit:1.2.0 .
```

The build runs its own smoke test (aspirin embeds and optimises, methane's adiabatic flame
temperature lands above 2000 K, water boils at 373.15 K), so a broken image fails at build
time rather than in someone's pipeline later.

---

## What is deliberately absent

- **No `.bkp` or other binary simulation files.** They can't be diffed or merged, and company
  models often embed confidential data. `templates/aspen_simulation_tips.md` covers the
  alternative.
- **No cracked binaries, licence workarounds, or "free Aspen" links.** The contributing guide
  says these get closed without discussion, and the lists hold to that.
- **No paywalled tools presented as free.** Anything with a commercial edition is tagged
  `commercial-free-tier` and the description says what the free version can actually do.
- **No DFT execution in the workflow.** The pipeline writes submittable ORCA inputs and stops.
  A Snakemake rule that quietly consumes 40 CPU-hours is a bad neighbour.

---

## Licence

Prose, documentation, and list content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code, templates, workflows, and configuration: MIT.
Linked projects keep their own licences — check before you build on any of them.

Nothing here is engineering, clinical, or regulatory advice.
