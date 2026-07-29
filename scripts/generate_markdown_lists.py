#!/usr/bin/env python3
"""Generate the awesome-style Markdown lists from the canonical catalog.

    python scripts/generate_markdown_lists.py            # write
    python scripts/generate_markdown_lists.py --check    # fail if stale (CI)

`lists/*.md` are GENERATED. Editing them by hand is a mistake the --check mode
exists to catch: CI regenerates and compares, so a hand edit fails the build
with a diff showing exactly what would be overwritten.

To change a list, edit the YAML record in catalog/resources/ and re-run this.
"""

from __future__ import annotations

import argparse
import collections
import difflib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from openche import catalog  # noqa: E402

GENERATED_BANNER = """<!--
  GENERATED FILE — DO NOT EDIT.

  Produced by scripts/generate_markdown_lists.py from the canonical records in
  catalog/resources/. Edit the YAML and re-run the generator; a hand edit here
  is overwritten on the next build and fails CI in the meantime.
-->
"""

INTROS: dict[str, str] = {
    "awesome-chemical-engineering":
        "Open-source software, data, and learning resources for chemical process "
        "engineering — simulation, thermodynamics, unit operations, control, and safety.",
    "awesome-chemoinformatics":
        "Open tools for representing, searching, predicting, and visualising molecules "
        "and reactions.",
    "awesome-bioengineering":
        "Open resources for bioprocess engineering, metabolic modelling, synthetic "
        "biology, biomaterials, and tissue engineering.",
    "awesome-medical-engineering":
        "Open tools and references for medical device design, biomechanics, medical "
        "imaging, regulatory affairs, clinical engineering, and health informatics.",
    "awesome-general-engineering":
        "Cross-cutting open tools every engineer eventually needs: CAD/CAE, control "
        "systems, signal processing, embedded and IoT, documentation, and ethics.",
}

# Section order within a list. Categories not named here are appended
# alphabetically, so a new category appears rather than vanishing.
SECTION_ORDER: list[str] = [
    "process-simulation", "flowsheeting", "thermodynamics", "physical-properties",
    "reaction-engineering", "kinetics", "unit-operations", "heat-transfer",
    "mass-transfer", "separations", "fluid-mechanics", "optimisation",
    "numerical-solvers", "process-control", "system-identification",
    "process-safety", "consequence-modelling", "computational-fluid-dynamics",
    "molecular-toolkits", "molecular-representations", "file-formats", "pipelines",
    "descriptors-and-fingerprints", "qsar", "machine-learning",
    "reaction-prediction", "retrosynthesis", "quantum-chemistry",
    "molecular-dynamics", "chemical-databases", "visualisation",
    "bioprocess-modelling", "genome-scale-models", "kinetic-modelling",
    "synthetic-biology", "protein-engineering", "biomaterials",
    "tissue-engineering", "bioinformatics", "standards-and-data",
    "device-design", "biomechanics", "medical-imaging", "physiological-signals",
    "regulatory-and-standards", "quality-and-risk", "clinical-engineering",
    "health-informatics",
    "cad-and-geometry", "cae-and-fea", "meshing", "control-systems",
    "signal-processing", "instrumentation", "embedded-and-iot",
    "industrial-protocols", "numerical-computing", "units-and-uncertainty",
    "reliability", "documentation", "project-management", "engineering-ethics",
    "datasets", "data-and-benchmarks", "benchmarks",
    "learning-resources", "community",
]

SECTION_TITLES: dict[str, str] = {
    "process-simulation": "Process Simulation",
    "flowsheeting": "Flowsheeting",
    "thermodynamics": "Thermodynamics & Physical Properties",
    "physical-properties": "Physical Properties",
    "reaction-engineering": "Reaction Engineering & Kinetics",
    "kinetics": "Kinetics",
    "unit-operations": "Unit Operations & Equipment Design",
    "heat-transfer": "Heat Transfer",
    "mass-transfer": "Mass Transfer",
    "separations": "Separations",
    "fluid-mechanics": "Fluid Mechanics",
    "optimisation": "Optimisation & Numerical Solvers",
    "numerical-solvers": "Numerical Solvers",
    "process-control": "Process Control & Safety",
    "system-identification": "System Identification",
    "process-safety": "Process Safety",
    "consequence-modelling": "Consequence Modelling",
    "computational-fluid-dynamics": "Computational Fluid Dynamics",
    "molecular-toolkits": "Molecular Representations & Toolkits",
    "molecular-representations": "Molecular Representations",
    "file-formats": "File Formats & Interoperability",
    "pipelines": "Pipelines & Workflow Tools",
    "descriptors-and-fingerprints": "Descriptors & Fingerprints",
    "qsar": "QSAR / QSPR",
    "machine-learning": "Machine Learning for Chemistry",
    "reaction-prediction": "Reaction Prediction & Retrosynthesis",
    "retrosynthesis": "Retrosynthesis",
    "quantum-chemistry": "Molecular Simulation & Quantum Chemistry",
    "molecular-dynamics": "Molecular Dynamics",
    "chemical-databases": "Chemical Databases",
    "visualisation": "Visualisation",
    "bioprocess-modelling": "Bioprocess Modelling & Control",
    "genome-scale-models": "Genome-Scale Metabolic Models",
    "kinetic-modelling": "Kinetic & Whole-Cell Modelling",
    "synthetic-biology": "Synthetic Biology",
    "protein-engineering": "Protein & Enzyme Engineering",
    "biomaterials": "Biomaterials",
    "tissue-engineering": "Tissue Engineering & Biofabrication",
    "bioinformatics": "Bioinformatics Crossover",
    "standards-and-data": "Standards, Data & Reproducibility",
    "device-design": "Medical Device Design & Development",
    "biomechanics": "Biomechanics",
    "medical-imaging": "Medical Imaging",
    "physiological-signals": "Physiological Modelling & Signals",
    "regulatory-and-standards": "Regulatory & Standards",
    "quality-and-risk": "Quality Systems & Risk Management",
    "clinical-engineering": "Clinical Engineering",
    "health-informatics": "Health Informatics & Interoperability",
    "cad-and-geometry": "CAD & Geometry",
    "cae-and-fea": "CAE, FEA & Meshing",
    "meshing": "Meshing",
    "control-systems": "Control Systems",
    "signal-processing": "Signal Processing & Instrumentation",
    "instrumentation": "Instrumentation",
    "embedded-and-iot": "Embedded & IoT",
    "industrial-protocols": "Data Acquisition, SCADA & Industrial Protocols",
    "numerical-computing": "Numerical Computing & Units",
    "units-and-uncertainty": "Units & Uncertainty",
    "reliability": "Reliability & Maintenance Engineering",
    "documentation": "Documentation & Technical Writing",
    "project-management": "Project & Requirements Management",
    "engineering-ethics": "Engineering Ethics & Professional Practice",
    "datasets": "Datasets",
    "data-and-benchmarks": "Data & Benchmarks",
    "benchmarks": "Benchmarks & Evaluation",
    "learning-resources": "Learning Resources",
    "community": "Community & Conferences",
}

RELATED = {
    "awesome-chemical-engineering": ["awesome-chemoinformatics", "awesome-bioengineering", "awesome-general-engineering"],
    "awesome-chemoinformatics": ["awesome-chemical-engineering", "awesome-bioengineering"],
    "awesome-bioengineering": ["awesome-chemical-engineering", "awesome-chemoinformatics", "awesome-medical-engineering"],
    "awesome-medical-engineering": ["awesome-bioengineering", "awesome-general-engineering", "awesome-chemoinformatics"],
    "awesome-general-engineering": ["awesome-chemical-engineering", "awesome-medical-engineering"],
}


def anchor(title: str) -> str:
    """GitHub's heading anchor rules: lowercase, spaces to hyphens, drop punctuation."""
    out = title.lower()
    for ch in "&/,()":
        out = out.replace(ch, "")
    return out.replace(" ", "-").replace("--", "--")


def section_title(cat: str) -> str:
    return SECTION_TITLES.get(cat, cat.replace("-", " ").title())


def tier_marker(rec: catalog.Record) -> str:
    """A compact, honest verification marker.

    Tier 0 gets nothing rather than a reassuring tick: an unchecked entry
    should not look the same as a checked one.
    """
    tier = rec.tier
    if tier == 0:
        return ""
    return f" `verified:T{tier}`"


def render_entry(rec: catalog.Record) -> str:
    tags = " ".join(f"`{t}`" for t in rec.data.get("tags", []) if t != "uncategorised")
    langs = " ".join(f"`{t}`" for t in rec.data.get("languages", []) or [])
    trailing = " ".join(x for x in (langs, tags) if x)
    summary = rec.data.get("summary", "").strip().rstrip(".")
    line = f"- [{rec.name}]({rec.data['canonical_url']}) — {summary}."
    if trailing:
        line += f" {trailing}"
    return line + tier_marker(rec)


def render_list(stem: str, records: list[catalog.Record]) -> str:
    domain = catalog.LIST_DOMAINS[stem]
    mine = [r for r in records if domain in r.data.get("domains", [])]

    by_cat: dict[str, list[catalog.Record]] = collections.defaultdict(list)
    domain_cats = set(catalog.load_categories().get(domain, []))
    for rec in mine:
        cats = [c for c in rec.data.get("categories", []) if c in domain_cats] or rec.data.get("categories", [])
        by_cat[cats[0]].append(rec)

    ordered = [c for c in SECTION_ORDER if c in by_cat]
    ordered += sorted(c for c in by_cat if c not in SECTION_ORDER)

    out: list[str] = [GENERATED_BANNER]
    out.append(f"# {catalog.LIST_TITLES[stem]} [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)\n")
    out.append(f"> {INTROS[stem]}\n")
    out.append(
        f"**{len(mine)} entries.** Every entry is free to use. Descriptions say what a tool "
        "*does*, not how good it is.\n"
    )
    out.append(
        "Entries carry a verification marker only when something was actually checked — "
        "see [verification methodology](../docs/verification-methodology.md). "
        "An entry with no marker has not been independently verified.\n"
    )
    out.append("**Contributions welcome** — see [CONTRIBUTING.md](../CONTRIBUTING.md).\n")
    out.append("---\n")

    out.append("## Contents\n")
    for cat in ordered:
        t = section_title(cat)
        out.append(f"- [{t}](#{anchor(t)})")
    out.append("- [Related Lists](#related-lists)")
    out.append("\n---\n")

    for cat in ordered:
        out.append(f"## {section_title(cat)}\n")
        for rec in sorted(by_cat[cat], key=lambda r: r.name.lower()):
            out.append(render_entry(rec))
        out.append("")

    out.append("## Related Lists\n")
    for other in RELATED.get(stem, []):
        out.append(f"- [{catalog.LIST_TITLES[other]}]({other}.md)")
    out.append("")
    out.append("---\n")
    out.append(
        "## Licence\n\n"
        "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain "
        "their own licences.\n"
    )
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if any generated file is stale")
    args = ap.parse_args()

    records = catalog.load_resources()
    catalog.LISTS_DIR.mkdir(parents=True, exist_ok=True)

    stale: list[str] = []
    for stem in catalog.LIST_DOMAINS:
        rendered = render_list(stem, records)
        path = catalog.LISTS_DIR / f"{stem}.md"
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        n = sum(1 for line in rendered.splitlines() if line.startswith("- ["))

        if args.check:
            if current != rendered:
                stale.append(str(path.relative_to(catalog.ROOT)))
                diff = list(difflib.unified_diff(
                    current.splitlines(), rendered.splitlines(),
                    fromfile=f"{path.name} (on disk)", tofile=f"{path.name} (generated)",
                    lineterm="", n=1,
                ))
                for line in diff[:20]:
                    print(f"    {line}")
                if len(diff) > 20:
                    print(f"    ... {len(diff) - 20} more diff lines")
            else:
                print(f"  ok     {path.name} ({n} lines)")
        else:
            path.write_text(rendered, encoding="utf-8")
            print(f"  wrote  {path.name}")

    if stale:
        print(f"\nfail  {len(stale)} generated list(s) are stale: {', '.join(stale)}")
        print("      Run: python scripts/generate_markdown_lists.py")
        return 1

    print("\n  Markdown lists are up to date." if args.check else "\n  Markdown lists written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
