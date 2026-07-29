"""Standardise input structures before conformer generation.

Called by the `standardise` rule. Reads the input CSV, sanitises every SMILES,
optionally strips salts and neutralises charges, applies size filters, and
writes the survivors plus a separate file of rejects with reasons.

Rejecting loudly beats fixing silently. A molecule that fails here is one you
should look at, not one the pipeline should guess about.
"""

from __future__ import annotations

import csv
import sys

from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors
from rdkit.Chem.MolStandardize import rdMolStandardize

# RDKit logs every sanitisation complaint to stderr. We capture the reasons
# ourselves and write them to the rejects file, so silence the duplicate noise.
RDLogger.DisableLog("rdApp.*")

log_path = snakemake.log[0]  # noqa: F821  (injected by Snakemake)
params = snakemake.params  # noqa: F821


def log(msg: str) -> None:
    with open(log_path, "a") as fh:
        fh.write(msg + "\n")
    print(msg, file=sys.stderr)


def standardise_one(smiles: str) -> tuple[Chem.Mol | None, str]:
    """Return (mol, reason). mol is None when the molecule was rejected."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "SMILES could not be parsed"

    try:
        # Normalise functional group representations (nitro, sulfoxide, ...) so
        # that two spellings of the same group give the same molecule.
        mol = rdMolStandardize.Normalize(mol)
        mol = rdMolStandardize.Reionize(mol)

        if params.strip_salts:
            before = Chem.MolToSmiles(mol)
            mol = rdMolStandardize.FragmentParent(mol)
            after = Chem.MolToSmiles(mol)
            if before != after:
                log(f"    salt stripped: {before} -> {after}")

        if params.neutralise:
            mol = rdMolStandardize.Uncharger().uncharge(mol)

        Chem.SanitizeMol(mol)
    except Exception as exc:  # RDKit raises a variety of types here
        return None, f"standardisation failed: {type(exc).__name__}: {exc}"

    n_heavy = mol.GetNumHeavyAtoms()
    if n_heavy == 0:
        return None, "no heavy atoms after standardisation"
    if n_heavy > params.max_heavy_atoms:
        return None, f"{n_heavy} heavy atoms exceeds limit of {params.max_heavy_atoms}"

    # A molecule with no ring and no rotatable bond has one conformer; the
    # pipeline still works, but flag it so nobody is surprised by an ensemble
    # of size 1.
    n_rot = Descriptors.NumRotatableBonds(mol)
    if n_rot == 0:
        log(f"    note: 0 rotatable bonds -- expect a single conformer")

    return mol, "ok"


def main() -> None:
    log("=" * 70)
    log("STANDARDISATION")
    log("=" * 70)
    log(f"  strip_salts      = {params.strip_salts}")
    log(f"  neutralise       = {params.neutralise}")
    log(f"  max_heavy_atoms  = {params.max_heavy_atoms}")
    log("")

    kept, rejected = [], []
    extra_fields: list[str] = []

    with open(snakemake.input.csv, newline="") as fh:  # noqa: F821
        reader = csv.DictReader(fh)
        extra_fields = [f for f in (reader.fieldnames or []) if f not in ("id", "smiles")]

        for row in reader:
            mol_id, smiles = row["id"].strip(), row["smiles"].strip()
            log(f"  {mol_id}: {smiles}")
            mol, reason = standardise_one(smiles)

            if mol is None:
                log(f"    REJECTED -- {reason}")
                rejected.append({"id": mol_id, "smiles": smiles, "reason": reason})
                continue

            canonical = Chem.MolToSmiles(mol)
            record = {
                "id": mol_id,
                "smiles": canonical,
                "original_smiles": smiles,
                "n_heavy_atoms": mol.GetNumHeavyAtoms(),
                "n_rotatable_bonds": Descriptors.NumRotatableBonds(mol),
                "mol_weight": round(Descriptors.MolWt(mol), 3),
                "formal_charge": Chem.GetFormalCharge(mol),
            }
            for f in extra_fields:
                record[f] = row.get(f, "")
            kept.append(record)
            log(f"    ok -- {record['n_heavy_atoms']} heavy atoms, "
                f"{record['n_rotatable_bonds']} rotatable bonds")

    fieldnames = [
        "id", "smiles", "original_smiles", "n_heavy_atoms",
        "n_rotatable_bonds", "mol_weight", "formal_charge", *extra_fields,
    ]
    with open(snakemake.output.csv, "w", newline="") as fh:  # noqa: F821
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept)

    with open(snakemake.output.rejected, "w", newline="") as fh:  # noqa: F821
        writer = csv.DictWriter(fh, fieldnames=["id", "smiles", "reason"])
        writer.writeheader()
        writer.writerows(rejected)

    log("")
    log(f"  kept     {len(kept)}")
    log(f"  rejected {len(rejected)}")

    if not kept:
        raise SystemExit(
            "Every input molecule was rejected. See "
            f"{snakemake.output.rejected} for the reasons."  # noqa: F821
        )

    # Downstream rules expect one output file per molecule id from the ORIGINAL
    # CSV. A rejection therefore breaks the DAG rather than silently producing
    # a short run -- which is the correct, if blunt, behaviour: you should know.
    if rejected:
        log("")
        log("  WARNING: rejected molecules will cause missing-output errors")
        log("  downstream. Fix or remove them from the input CSV and rerun.")


main()
