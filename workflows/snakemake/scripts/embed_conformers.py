"""Generate an initial 3D conformer ensemble with ETKDGv3.

Called by the `embed_conformers` rule, once per molecule.

ETKDGv3 is distance geometry with torsion-angle preferences derived from the
CSD, plus specific handling for small rings and macrocycles. It is the current
RDKit default and there is no good reason to use an earlier version.
"""

from __future__ import annotations

import csv
import sys

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, Descriptors

RDLogger.DisableLog("rdApp.warning")

log_path = snakemake.log[0]  # noqa: F821
params = snakemake.params  # noqa: F821
mol_id = snakemake.wildcards.mol_id  # noqa: F821


def log(msg: str) -> None:
    with open(log_path, "a") as fh:
        fh.write(msg + "\n")


def load_molecule() -> Chem.Mol:
    with open(snakemake.input.csv, newline="") as fh:  # noqa: F821
        for row in csv.DictReader(fh):
            if row["id"] == mol_id:
                mol = Chem.MolFromSmiles(row["smiles"])
                if mol is None:
                    raise ValueError(f"{mol_id}: standardised SMILES failed to parse")
                mol.SetProp("_Name", mol_id)
                for key in ("original_smiles", "n_rotatable_bonds", "formal_charge"):
                    if key in row:
                        mol.SetProp(key, str(row[key]))
                return mol
    raise KeyError(f"{mol_id} not found in the standardised molecule file")


def main() -> None:
    mol = load_molecule()

    # Explicit hydrogens are required. Embedding without them gives geometries
    # that are wrong in ways that are not obvious until the force field pulls
    # them apart -- this is the single most common conformer-generation bug.
    mol = Chem.AddHs(mol)

    n_rot = Descriptors.NumRotatableBonds(mol)
    n_atoms = mol.GetNumAtoms()

    log("=" * 70)
    log(f"EMBEDDING: {mol_id}")
    log("=" * 70)
    log(f"  atoms (with H)     {n_atoms}")
    log(f"  rotatable bonds    {n_rot}")
    log(f"  requested embeds   {params.n_conformers}")
    log(f"  random seed        {params.random_seed}")

    if n_rot > 8:
        log(f"  WARNING: {n_rot} rotatable bonds. Conformational space grows")
        log(f"  roughly as 3^n_rot; {params.n_conformers} embeddings is likely")
        log("  to under-sample. Consider CREST for a metadynamics search.")

    ps = AllChem.ETKDGv3()
    ps.randomSeed = params.random_seed
    ps.pruneRmsThresh = params.prune_rms
    ps.useRandomCoords = params.use_random_coords
    ps.numThreads = snakemake.threads  # noqa: F821
    ps.enforceChirality = True
    ps.useSmallRingTorsions = True
    ps.useMacrocycleTorsions = True
    ps.maxIterations = 0  # 0 means "RDKit picks, scaled by molecule size"

    conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=params.n_conformers, params=ps)
    n_embedded = len(conf_ids)
    log(f"  embedded           {n_embedded}")

    if n_embedded == 0:
        # Retry with random coordinates. This rescues most failures, typically
        # cage-like or heavily bridged systems where distance geometry from the
        # default starting guess cannot satisfy the bounds matrix.
        log("  Embedding produced nothing. Retrying with random coordinates.")
        ps.useRandomCoords = True
        conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=params.n_conformers, params=ps)
        n_embedded = len(conf_ids)
        log(f"  embedded on retry  {n_embedded}")

    if n_embedded == 0:
        raise RuntimeError(
            f"{mol_id}: embedding failed even with random coordinates. "
            "Check the structure for impossible geometry -- over-constrained "
            "ring systems and bad stereochemistry are the usual causes."
        )

    if n_embedded < params.n_conformers * 0.5:
        log(f"  NOTE: only {n_embedded}/{params.n_conformers} embeddings succeeded.")
        log("  Either the RMSD pre-pruning is doing its job on a rigid molecule,")
        log("  or the geometry is hard. Check n_rotatable_bonds above to tell which.")

    writer = Chem.SDWriter(snakemake.output.sdf)  # noqa: F821
    for cid in conf_ids:
        mol.SetProp("conformer_id", str(cid))
        writer.write(mol, confId=cid)
    writer.close()

    log(f"  wrote              {snakemake.output.sdf}")  # noqa: F821
    print(f"{mol_id}: {n_embedded} conformers embedded", file=sys.stderr)


main()
