"""Force-field optimise, energy-filter, RMSD-prune, and Boltzmann-weight.

Called by the `optimise_prune` rule, once per molecule.

Order of operations matters and is deliberate:

  1. optimise every embedded conformer
  2. drop anything that failed to converge
  3. sort by energy
  4. drop anything outside the energy window
  5. prune by heavy-atom RMSD, keeping the lower-energy member of each pair
  6. Boltzmann-weight what remains and truncate to n_final_max

Pruning before optimising would be faster and wrong: two embeddings that look
different can relax into the same minimum, and two that look similar can relax
apart.
"""

from __future__ import annotations

import csv
import math
import sys

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, rdMolAlign

RDLogger.DisableLog("rdApp.warning")

R_KCAL = 1.987204259e-3  # kcal/(mol*K)

log_path = snakemake.log[0]  # noqa: F821
params = snakemake.params  # noqa: F821
mol_id = snakemake.wildcards.mol_id  # noqa: F821


def log(msg: str) -> None:
    with open(log_path, "a") as fh:
        fh.write(msg + "\n")


def optimise(mol: Chem.Mol) -> tuple[list[tuple[int, float]], str]:
    """Optimise all conformers. Returns ([(conf_id, energy_kcal)], field_used)."""
    field = params.force_field

    if field.startswith("MMFF"):
        mp = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant=field)
        if mp is None:
            # MMFF cannot type every molecule -- organometallics, hypervalent
            # sulfur, unusual valences. UFF covers more of the periodic table
            # at the cost of accuracy. Record the fallback: UFF and MMFF
            # energies are not comparable, so a mixed set must not be ranked
            # against each other.
            log(f"  MMFF typing failed; falling back to UFF")
            field = "UFF"

    if field == "UFF":
        results = AllChem.UFFOptimizeMoleculeConfs(
            mol, maxIters=params.max_iters, numThreads=snakemake.threads  # noqa: F821
        )
    else:
        results = AllChem.MMFFOptimizeMoleculeConfs(
            mol,
            maxIters=params.max_iters,
            numThreads=snakemake.threads,  # noqa: F821
            mmffVariant=params.force_field,
        )

    # results is [(converged_flag, energy)]; converged_flag == 0 means success.
    energies, n_failed = [], 0
    for cid, (not_converged, energy) in zip([c.GetId() for c in mol.GetConformers()], results):
        if not_converged:
            n_failed += 1
            continue
        energies.append((cid, float(energy)))

    if n_failed:
        log(f"  {n_failed} conformer(s) did not converge in {params.max_iters} steps "
            f"and were discarded")

    return energies, field


def prune_by_rmsd(mol: Chem.Mol, ranked: list[tuple[int, float]]) -> list[tuple[int, float]]:
    """Keep conformers separated by more than the RMSD threshold.

    Uses GetBestRMS, which finds the best alignment allowing for molecular
    symmetry -- without that, two identical conformers of a para-substituted
    ring differing only by a 180-degree flip look distinct, and the ensemble
    fills up with duplicates.

    Hydrogens are removed before comparison: heavy-atom RMSD is what conformer
    identity conventionally means, and methyl rotation is not a conformer.
    """
    heavy = Chem.RemoveHs(Chem.Mol(mol))
    kept: list[tuple[int, float]] = []

    for cid, energy in ranked:  # ranked lowest-energy first
        duplicate_of = None
        for kept_cid, _ in kept:
            rms = rdMolAlign.GetBestRMS(heavy, heavy, prbId=cid, refId=kept_cid)
            if rms < params.rmsd_threshold:
                duplicate_of = kept_cid
                break
        if duplicate_of is None:
            kept.append((cid, energy))

    return kept


def main() -> None:
    supplier = Chem.SDMolSupplier(snakemake.input.sdf, removeHs=False)  # noqa: F821
    mols = [m for m in supplier if m is not None]
    if not mols:
        raise RuntimeError(f"{mol_id}: no readable conformers in the embedded SDF")

    # Rebuild one molecule carrying every conformer, which is what the RDKit
    # multi-conformer optimisers and RMSD routines expect.
    mol = Chem.Mol(mols[0])
    mol.RemoveAllConformers()
    for m in mols:
        mol.AddConformer(m.GetConformer(), assignId=True)

    n_start = mol.GetNumConformers()
    log("=" * 70)
    log(f"OPTIMISE AND PRUNE: {mol_id}")
    log("=" * 70)
    log(f"  conformers in            {n_start}")
    log(f"  force field              {params.force_field}")
    log(f"  energy window            {params.energy_window_kcal} kcal/mol")
    log(f"  RMSD threshold           {params.rmsd_threshold} A")

    energies, field_used = optimise(mol)
    if not energies:
        raise RuntimeError(f"{mol_id}: no conformer converged")

    ranked = sorted(energies, key=lambda t: t[1])
    e_min = ranked[0][1]
    log(f"  converged                {len(ranked)}")
    log(f"  lowest energy            {e_min:.4f} kcal/mol")
    log(f"  energy spread            {ranked[-1][1] - e_min:.4f} kcal/mol")

    within = [(c, e) for c, e in ranked if (e - e_min) <= params.energy_window_kcal]
    log(f"  within energy window     {len(within)}")

    pruned = prune_by_rmsd(mol, within)
    log(f"  after RMSD pruning       {len(pruned)}")

    final = pruned[: params.max_final]
    if len(pruned) > params.max_final:
        log(f"  truncated to             {params.max_final} (n_final_max)")

    # Boltzmann populations at the configured temperature. Reported because
    # a conformer that exists is not the same as a conformer that matters:
    # 3 kcal/mol above the minimum is under 1% populated at 298 K.
    kT = R_KCAL * params.temperature
    rel = [e - e_min for _, e in final]
    boltz = [math.exp(-de / kT) for de in rel]
    z = sum(boltz)
    populations = [b / z for b in boltz]

    writer = Chem.SDWriter(snakemake.output.sdf)  # noqa: F821
    rows = []
    for rank, ((cid, energy), de, pop) in enumerate(zip(final, rel, populations)):
        mol.SetProp("_Name", f"{mol_id}_conf{rank:03d}")
        mol.SetProp("mol_id", mol_id)
        mol.SetProp("conformer_rank", str(rank))
        mol.SetProp("force_field", field_used)
        mol.SetProp("energy_kcal_mol", f"{energy:.6f}")
        mol.SetProp("relative_energy_kcal_mol", f"{de:.6f}")
        mol.SetProp("boltzmann_population", f"{pop:.6f}")
        writer.write(mol, confId=cid)
        rows.append({
            "mol_id": mol_id,
            "conformer_rank": rank,
            "conformer_id": cid,
            "force_field": field_used,
            "energy_kcal_mol": round(energy, 6),
            "relative_energy_kcal_mol": round(de, 6),
            "boltzmann_population": round(pop, 6),
            "n_embedded": n_start,
            "n_converged": len(ranked),
            "n_final": len(final),
        })
    writer.close()

    with open(snakemake.output.energies, "w", newline="") as fh:  # noqa: F821
        writer_csv = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer_csv.writeheader()
        writer_csv.writerows(rows)

    log("")
    log(f"  {'rank':>5s}{'E (kcal/mol)':>16s}{'dE':>10s}{'population':>13s}")
    for r in rows[:10]:
        log(f"  {r['conformer_rank']:>5d}{r['energy_kcal_mol']:>16.4f}"
            f"{r['relative_energy_kcal_mol']:>10.3f}{r['boltzmann_population']:>13.4f}")
    if len(rows) > 10:
        log(f"  ... and {len(rows) - 10} more")

    log("")
    log("  Reminder: these are force-field energies. Use them to RANK candidates")
    log("  for a better method, not to make a claim about relative populations.")

    print(f"{mol_id}: {n_start} -> {len(final)} conformers", file=sys.stderr)


main()
