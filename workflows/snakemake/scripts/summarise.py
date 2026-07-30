"""Aggregate per-molecule results into one CSV and a readable report.

Called by the `summarise` rule. The report is written for someone who did not
run the pipeline: it says what was produced, flags what looks suspect, and
states the limits of what the numbers support.
"""

from __future__ import annotations

import csv
import datetime as dt
import pathlib

import pandas as pd

params = snakemake.params  # noqa: F821
log_path = snakemake.log[0]  # noqa: F821


def log(msg: str) -> None:
    with open(log_path, "a") as fh:
        fh.write(msg + "\n")


def main() -> None:
    frames = [pd.read_csv(p) for p in snakemake.input.energies]  # noqa: F821
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(snakemake.output.csv, index=False)  # noqa: F821
    log(f"Wrote {len(df)} conformer rows across {df['mol_id'].nunique()} molecules")

    per_mol = (
        df.groupby("mol_id")
        .agg(
            n_embedded=("n_embedded", "first"),
            n_converged=("n_converged", "first"),
            n_final=("n_final", "first"),
            force_field=("force_field", "first"),
            e_min=("energy_kcal_mol", "min"),
            energy_span=("relative_energy_kcal_mol", "max"),
            top_population=("boltzmann_population", "max"),
        )
        .reset_index()
    )

    # An ensemble whose top conformer holds nearly all the population is either
    # genuinely rigid or under-sampled; either way it is worth a look before
    # anyone spends DFT time on it.
    per_mol["flag"] = ""
    per_mol.loc[per_mol["n_final"] == 1, "flag"] += "single-conformer "
    per_mol.loc[per_mol["top_population"] > 0.95, "flag"] += "dominant-conformer "
    per_mol.loc[per_mol["n_converged"] < 0.5 * per_mol["n_embedded"], "flag"] += "poor-convergence "
    per_mol.loc[per_mol["force_field"] == "UFF", "flag"] += "uff-fallback "

    rejected = pd.read_csv(snakemake.input.rejected)  # noqa: F821

    report = pathlib.Path(snakemake.output.report)  # noqa: F821
    with report.open("w") as fh:
        fh.write(f"""# Conformer generation summary

Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} by
[conformer_generation_dft](https://github.com/OpenChemE/workflows).

## What was run

| | |
| --- | --- |
| Molecules processed | {per_mol.shape[0]} |
| Molecules rejected at standardisation | {len(rejected)} |
| Total conformers retained | {len(df)} |
| Boltzmann temperature | {params.temperature} K |

## Per-molecule results

| Molecule | Embedded | Converged | Final | Field | E_min (kcal/mol) | Span | Top pop. | Flags |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
""")
        for _, r in per_mol.iterrows():
            fh.write(
                f"| {r['mol_id']} | {r['n_embedded']} | {r['n_converged']} | "
                f"{r['n_final']} | {r['force_field']} | {r['e_min']:.2f} | "
                f"{r['energy_span']:.2f} | {r['top_population']:.3f} | "
                f"{r['flag'].strip() or '—'} |\n"
            )

        if len(rejected):
            fh.write("\n## Rejected molecules\n\n| ID | SMILES | Reason |\n| --- | --- | --- |\n")
            for _, r in rejected.iterrows():
                fh.write(f"| {r['id']} | `{r['smiles']}` | {r['reason']} |\n")

        fh.write("""
## Flags, and what to do about them

| Flag | Meaning | Action |
| --- | --- | --- |
| `single-conformer` | Only one conformer survived pruning | Expected for rigid molecules. Check the rotatable bond count; if it's above 2, the search under-sampled |
| `dominant-conformer` | One conformer holds >95% of the population | Often real, sometimes an artefact of force-field energies. Verify at a higher level before relying on it |
| `poor-convergence` | Under half the embeddings converged | Raise `max_iterations`, or look for strained geometry in the input |
| `uff-fallback` | MMFF could not type the molecule | UFF energies are not comparable with MMFF ones. Do not rank this molecule against the others |

## Limits of these results

These are **force-field** energies and geometries. Specifically:

- Relative conformer energies from MMFF94s are routinely wrong by 1–3 kcal/mol,
  which at 298 K is a factor of 5 to 150 in population. The Boltzmann weights
  above are indicative, not quantitative.
- Intramolecular hydrogen bonding, conjugation, and anything charged are handled
  poorly. If your molecules have these, treat the ranking as a shortlist only.
- The ensemble is as good as the sampling. A molecule with 10 rotatable bonds
  needs far more than 200 embeddings, and no amount of optimisation fixes a
  conformer that was never generated.

**The intended use** is to produce a diverse, deduplicated set of starting
geometries for a higher level of theory. The `dft_inputs/` directory has those
inputs ready to submit. For quantitative populations, run GFN2-xTB or DFT on
the ensemble and re-weight with those energies.

## Reproducing this

```bash
conda env create -f environment.yaml
conda activate conformer-gen
snakemake --cores 4
```

Everything that affects the result is in `config.yaml`, `environment.yaml`, and
the input CSV. The random seed is pinned, so a rerun with the same three files
gives the same ensemble.
""")

    log(f"Wrote report to {report}")
    print(per_mol.to_string(index=False))


main()
