# Workflows

**Reproducible computational pipelines, CI automation, and a container image for chemical
engineering and computational chemistry.**

Three things live here, each solving a different part of "it worked on my machine":

| Directory | What it gives you |
| --- | --- |
| [`snakemake/`](snakemake/) | A conformer generation pipeline that scales from a laptop to a cluster without changing the code |
| [`github_actions/`](github_actions/) | CI workflows for repositories containing chemical data — render structures, validate files on every push |
| [`docker/`](docker/) | One container with RDKit, Open Babel, Cantera, CoolProp, and the process engineering stack, pinned to exact versions |

---

## Quick start

### Run the conformer pipeline

```bash
git clone https://github.com/open-cheme-hub/workflows
cd workflows/snakemake

conda env create -f environment.yaml     # or: mamba env create -f environment.yaml
conda activate conformer-gen

snakemake -n --cores 4                   # dry run first, always
snakemake --cores 4                      # ~2 minutes on the 5-molecule test set
```

Output lands in `results/`. Start with `results/summary/report.md`.

### Use the container instead

```bash
docker pull ghcr.io/open-cheme-hub/chem-toolkit:1.2.0
docker run --rm -it -v "$PWD:/work" ghcr.io/open-cheme-hub/chem-toolkit:1.2.0
```

Or build it yourself:

```bash
cd docker && docker build -t chem-toolkit:1.2.0 .
```

The build runs a smoke test — aspirin embeds and optimises, methane's adiabatic flame
temperature comes out right, water boils at 373.15 K. A broken image fails at build time
rather than in someone's pipeline at 2am.

### Add structure rendering to your repository

```bash
mkdir -p .github/workflows
curl -o .github/workflows/render_mol.yml \
  https://raw.githubusercontent.com/open-cheme-hub/workflows/main/github_actions/render_mol.yml
```

Every changed `.mol`, `.sdf`, `.smi`, `.xyz`, or `.pdb` in a pull request gets rendered to SVG
and PNG, validated with RDKit, and attached as an artifact. Reviewing a diff of a connection
table is not a thing humans can do; looking at a picture is.

---

## `snakemake/conformer_generation_dft`

### What it does

```
molecules.csv (SMILES)
      |
      v
 standardise         strip salts, sanitise, filter by size -> rejected.csv for anything dropped
      |
      v
 embed_conformers    ETKDGv3, fixed seed, N initial embeddings per molecule
      |
      v
 optimise_and_prune  MMFF94s optimise -> energy window -> heavy-atom RMSD prune -> Boltzmann weight
      |
      +---> conformers/*.sdf      ranked ensemble with energies and populations
      +---> xyz/*.xyz             lowest-energy geometries, one file each
      +---> dft_inputs/*.inp      submittable ORCA jobs (and Psi4 equivalents)
      +---> summary/report.md     what was produced, what looks suspect, what it supports
```

### What it is and is not

**It is** a fast, defensible way to produce a diverse, deduplicated conformer ensemble —
good enough to feed docking, to pick DFT starting geometries, or to gauge conformational
flexibility.

**It is not** a source of accurate relative conformer energies. MMFF94s is a force field. It
gets geometries approximately right and energy ordering wrong often enough to matter,
especially with intramolecular hydrogen bonds, conjugation, or charges. Relative energies are
routinely off by 1–3 kcal/mol, which at 298 K is a factor of 5 to 150 in population.

The `dft` in the name is the step you do **next**, using the inputs this generates. The
pipeline writes them and deliberately does not run them: DFT on a real ensemble is a cluster
job with a queue, not a rule that quietly eats 40 CPU-hours on your laptop.

For work where conformer populations decide the answer, use [CREST](https://github.com/crest-lab/crest)
with GFN2-xTB for the search and treat this as the cheap first pass.

### Compute envelope

Measured on the 5-molecule test set, 4 cores, 200 initial embeddings each:

| | |
| --- | --- |
| Runtime | ~90 seconds total |
| Peak memory | ~1.2 GB |
| GPU | Not used |
| Scaling | Linear in molecules; roughly linear in `n_initial` |

A 1000-molecule set with 500 embeddings each is roughly 6–10 core-hours. The RMSD pruning step
is O(n²) in conformers per molecule and dominates for flexible compounds.

### Configuration

Everything that changes the scientific result is in `config.yaml` — nothing in the Snakefile or
the scripts. A run is fully described by `config.yaml` + `environment.yaml` + the input CSV.
Commit all three together.

The parameters worth understanding before you change anything else:

| Parameter | Default | Why it matters |
| --- | --- | --- |
| `random_seed` | `0xF00D` | The reproducibility parameter. Never unset it — a pipeline whose output changes run to run cannot be debugged |
| `n_initial` | 200 | Sampling adequacy. Rough guide: 50 for ≤2 rotatable bonds, 200 for 3–5, 500 for 6–8, and reconsider the approach above that |
| `rmsd_threshold` | 0.5 Å | What counts as "the same conformer". Standard for drug-like molecules; tighten to 0.3 for small rigid systems |
| `energy_window_kcal` | 10.0 | Deliberately generous. Force-field energies are unreliable enough that aggressive early pruning can discard the true minimum |
| `neutralise` | `false` | A carboxylate at pH 7.4 is not neutral. If your question is about binding at physiological pH, supply the protonation state yourself |

### Running on a cluster

Nothing in the pipeline changes. Add a profile:

```bash
snakemake --profile slurm --jobs 100
```

Per-rule `threads` and `resources` (memory, runtime) are already declared, so the profile has
what it needs to submit sensible jobs.

---

## `github_actions/render_mol.yml`

Renders and validates chemical structure files on push and pull request.

**What it does**

1. Identifies changed structure files by diffing against the base commit.
2. Renders each to SVG (Open Babel, `--gen2d`) and PNG.
3. Sanitises each with RDKit and **fails the check** if any won't sanitise — a file that draws
   fine but has a valence error will break every downstream tool.
4. Uploads everything as an artifact and posts (or updates) one PR comment.

**Security notes**, since a workflow anyone can trigger with a pull request is an attack
surface:

- Untrusted input — branch names, PR titles, file paths from forks — never reaches a `run:`
  block through `${{ }}` interpolation. It goes through `env:` or comes from git directly.
- Third-party actions are pinned to full commit SHAs, not moving tags.
- Permissions are minimal: `contents: read` plus `pull-requests: write` only for the comment
  step. Drop that and the step skips rather than failing.

---

## `docker/chem-toolkit`

| Component | Version | For |
| --- | --- | --- |
| RDKit | 2024.03.5 | Cheminformatics, conformers, descriptors |
| Open Babel | 3.1.1 | Format conversion across 110+ formats |
| Cantera | 3.0.0 | Kinetics, equilibrium, reactor networks |
| CoolProp | 6.6.0 | Thermophysical properties, ~122 fluids |
| thermo / chemicals / fluids / ht | pinned | Flashes, EOS, pressure drop, heat transfer |
| Pyomo + Ipopt + GLPK | pinned | Optimisation |
| Snakemake | 8.20.3 | Workflow execution |
| JupyterLab | 4.2.3 | Notebooks, with py3Dmol for structure views |

Built on micromamba rather than pip, because RDKit, Open Babel, and Cantera all ship compiled
extensions that conda-forge builds consistently against one another. Pip works until two
packages want different Boost versions.

Threading environment variables default to 1. On a shared cluster node, N processes each
spawning N threads is how you get a call from the sysadmin. Override with
`-e OMP_NUM_THREADS=8` when you want the cores.

---

## Contributing a workflow

Workflows carry a higher bar than list entries, because people will trust them with real
analyses. From the [organisation guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md):

- **Pin dependencies to versions.** `environment.yaml` with exact pins, or a Docker digest.
  `latest` is not a version.
- **Ship a test case** that runs in under a minute on a laptop, under `test_data/`.
- **Document the compute envelope**: runtime, memory, GPU or cluster requirements.
- **Declare the science**, not just the code — what method, what assumptions, what it is *not*
  valid for. A conformer generator that skips a DFT refinement should say so loudly, which is
  why this README does.
- **No credentials, licensed binaries, or institutional paths.** Read from environment
  variables and document them.

### Layout for a new workflow

```
your_workflow/
├── README.md              # purpose, envelope, assumptions, limitations
├── Snakefile              # or main.nf for Nextflow
├── config.yaml            # every scientifically meaningful parameter
├── environment.yaml       # pinned
├── scripts/
└── test_data/             # small, runs in under a minute
```

---

## Licence

MIT. See the [organisation licence](https://github.com/open-cheme-hub/.github/blob/main/LICENSE).
Dependencies keep their own licences — RDKit is BSD-3, Open Babel is GPL-2.0, Cantera is
BSD-3. If you redistribute the container image, GPL obligations from Open Babel travel with it.
