#!/usr/bin/env python3
"""Import the legacy Markdown awesome lists into canonical YAML records.

This is a ONE-WAY migration tool, run once per list. After a list is imported,
`lists/<name>.md` becomes a GENERATED file and must not be hand-edited —
`scripts/generate_markdown_lists.py` rewrites it from the YAML.

    python scripts/import_markdown_lists.py --list awesome-chemical-engineering
    python scripts/import_markdown_lists.py --all --dry-run

What it does NOT do
-------------------
It does not invent metadata. A Markdown line carries a name, a URL, a sentence,
and some tags — nothing about licence, maintenance status, or platform support.
Those fields are written as `unknown`, and every imported record starts at
verification tier 0.

That is deliberate, and it is the whole point of the migration: an honest
`unknown` is a work item somebody can close, while a plausible guess is a lie
that survives review because it looks like data.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import yaml  # noqa: E402

from openche import catalog  # noqa: E402

# `- [Name](url) — description. \`tag\` \`tag\``
# The URL group allows one level of balanced parentheses: real links contain
# them (LibreTexts book paths end in "(Woolf)") and a naive [^)]+ truncates
# them into a 404.
ENTRY_RE = re.compile(
    r"^- \[(?P<name>[^\]]+)\]"
    r"\((?P<url>(?:[^()\s]|\([^()\s]*\))+)\)"
    r"\s*(?:[—-]\s*(?P<rest>.*))?$"
)
TAG_RE = re.compile(r"`([^`]+)`")

# Section heading -> category slug, per domain. Anything unmapped falls back to
# a slugified heading and is reported, so new sections surface rather than
# silently creating uncontrolled categories.
SECTION_MAP: dict[str, str] = {
    "process simulation": "process-simulation",
    "thermodynamics & physical properties": "thermodynamics",
    "reaction engineering & kinetics": "reaction-engineering",
    "unit operations & equipment design": "unit-operations",
    "optimisation & numerical solvers": "optimisation",
    "process control & safety": "process-control",
    "computational fluid dynamics": "computational-fluid-dynamics",
    "data & benchmarks": "data-and-benchmarks",
    "learning resources": "learning-resources",
    "community & conferences": "community",
    "molecular representations & toolkits": "molecular-toolkits",
    "file formats & interoperability": "file-formats",
    "cheminformatics pipelines & workflow tools": "pipelines",
    "descriptors & fingerprints": "descriptors-and-fingerprints",
    "qsar / qspr": "qsar",
    "machine learning for chemistry": "machine-learning",
    "reaction prediction & retrosynthesis": "reaction-prediction",
    "molecular simulation & quantum chemistry": "quantum-chemistry",
    "chemical databases": "chemical-databases",
    "visualisation": "visualisation",
    "benchmarks & evaluation": "benchmarks",
    "community": "community",
    "bioprocess modelling & control": "bioprocess-modelling",
    "genome-scale metabolic models": "genome-scale-models",
    "kinetic & whole-cell modelling": "kinetic-modelling",
    "synthetic biology": "synthetic-biology",
    "protein & enzyme engineering": "protein-engineering",
    "biomaterials": "biomaterials",
    "tissue engineering & biofabrication": "tissue-engineering",
    "bioinformatics crossover": "bioinformatics",
    "standards, data & reproducibility": "standards-and-data",
    "medical device design & development": "device-design",
    "biomechanics": "biomechanics",
    "medical imaging": "medical-imaging",
    "physiological modelling & signals": "physiological-signals",
    "regulatory & standards": "regulatory-and-standards",
    "quality systems & risk management": "quality-and-risk",
    "clinical engineering": "clinical-engineering",
    "health informatics & interoperability": "health-informatics",
    "datasets": "datasets",
    "cad & geometry": "cad-and-geometry",
    "cae, fea & meshing": "cae-and-fea",
    "control systems": "control-systems",
    "signal processing & instrumentation": "signal-processing",
    "embedded & iot": "embedded-and-iot",
    "numerical computing & units": "numerical-computing",
    "data acquisition, scada & industrial protocols": "industrial-protocols",
    "reliability & maintenance engineering": "reliability",
    "documentation & technical writing": "documentation",
    "project & requirements management": "project-management",
    "engineering ethics & professional practice": "engineering-ethics",
}

# Tags that describe a language rather than a general property.
LANGUAGE_TAGS = {
    "python", "c++", "c", "java", "javascript", "typescript", "julia", "matlab",
    "fortran", "r", "octave", "ruby", "go", "groovy", "sql", "yaml", "c#",
    "vb-dotnet", "modelica", "knime", "nextflow", "snakemake",
}

PLATFORM_TAGS = {"windows", "macos", "linux", "web", "cross-platform", "docker"}

# Tag -> resource kind. First match wins, in this order.
KIND_TAGS: list[tuple[str, str]] = [
    ("dataset", "dataset"),
    ("database", "dataset"),
    ("benchmark", "benchmark"),
    ("book", "book"),
    ("course", "course"),
    ("tutorial", "tutorial"),
    ("notebooks", "tutorial"),
    ("standard", "standard"),
    ("regulatory", "regulatory-source"),
    ("forum", "community"),
    ("conference", "community"),
    ("community", "community"),
    ("mailing-list", "community"),
    ("hardware", "hardware"),
    ("api", "api"),
    ("blog", "article"),
    ("solver", "library"),
    ("gui", "software"),
    ("platform", "software"),
]


def infer_kind(tags: list[str], section: str) -> str:
    for tag, kind in KIND_TAGS:
        if tag in tags:
            return kind
    if "learning" in section or "resource" in section:
        return "tutorial"
    if "communit" in section or "conference" in section:
        return "community"
    if "database" in section or "dataset" in section or "benchmark" in section:
        return "dataset"
    return "library"


def infer_access(tags: list[str]) -> dict[str, Any]:
    """Infer only what the tag vocabulary actually encodes."""
    if "commercial-free-tier" in tags:
        return {
            "model": "free-tier",
            "free_tier": True,
            "paid_features_exist": True,
            "notes": "Imported from the legacy list tag `commercial-free-tier`. "
                     "The exact free-tier boundary has not been confirmed.",
        }
    if "public-domain" in tags:
        return {"model": "public-domain", "open_source_release": True, "free_tier": True}
    # Everything else: the list only guaranteed "free to use", which is not the
    # same as open source. Say so rather than assuming a licence.
    return {
        "model": "unknown",
        "free_tier": True,
        "notes": "The legacy list guaranteed the resource is free to use, but the "
                 "access model was never recorded. Needs confirmation.",
    }


def parse_list(path: pathlib.Path, domain: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Return (records, warnings)."""
    records: list[dict[str, Any]] = []
    warnings: list[str] = []
    section = ""
    section_slug = ""
    in_related = False

    allowed = catalog.allowed_categories()

    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## "):
            section = raw[3:].strip()
            key = section.lower()
            # "Related Lists" is navigation, not resources.
            in_related = key in {"related lists", "contents", "contributing", "licence", "license", "disclaimer"}
            section_slug = SECTION_MAP.get(key, catalog.slugify(section))
            if not in_related and section_slug not in allowed:
                warnings.append(f"section {section!r} -> unmapped category {section_slug!r}")
            continue

        if in_related or not raw.startswith("- ["):
            continue

        m = ENTRY_RE.match(raw)
        if not m:
            warnings.append(f"unparsed line: {raw[:80]}")
            continue

        name = m.group("name").strip()
        url = m.group("url").strip()
        rest = (m.group("rest") or "").strip()

        tags = [t.strip().lower() for t in TAG_RE.findall(rest)]
        summary = TAG_RE.sub("", rest).strip().rstrip(".").strip()
        # Strip the backtick-decoration some names carry, e.g. "`fluids`".
        display = name.replace("`", "").strip()

        if len(summary) < 20:
            warnings.append(f"{display}: summary shorter than 20 chars, padded for schema")
            summary = (summary + ". Description needs expanding during curation.").strip()

        languages = sorted({t for t in tags if t in LANGUAGE_TAGS})
        platforms = sorted({t for t in tags if t in PLATFORM_TAGS})
        other = [t for t in tags if t not in LANGUAGE_TAGS and t not in PLATFORM_TAGS]

        record: dict[str, Any] = {
            "schema_version": 1,
            "slug": catalog.slugify(display),
            "name": display,
            "kind": infer_kind(tags, section.lower()),
            "canonical_url": url,
            "summary": summary,
            "domains": [domain],
            "categories": [section_slug],
            "audiences": ["student", "researcher", "industry"],
            "access": infer_access(tags),
            "license": {
                "spdx": "UNKNOWN",
                "source": "unknown",
                "notes": "Not recorded in the legacy list. Confirm from the project "
                         "before promoting this record above verification tier 1.",
            },
            "maturity": "unknown",
            "maintenance_status": "unknown",
            "verification": {
                "tier": 0,
                "status": "submitted",
                "notes": [
                    "Imported from the legacy Markdown list; no field has been "
                    "independently confirmed.",
                ],
            },
            "link_status": "unknown",
            "source_list": path.stem,
            "source_section": section,
            "tags": other or ["uncategorised"],
        }

        if languages:
            record["languages"] = languages
        if platforms:
            record["platforms"] = platforms

        records.append(record)

    return records, warnings


def write_records(records: list[dict[str, Any]], dry_run: bool) -> tuple[int, list[str]]:
    """Write one YAML file per record. Returns (written, collisions)."""
    catalog.RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    seen: dict[str, str] = {}
    collisions: list[str] = []
    written = 0

    by_slug: dict[str, dict[str, Any]] = {}
    for rec in records:
        slug = rec["slug"]
        if slug in by_slug:
            # Same resource listed under two sections. Merge the categories and
            # tags rather than discarding the second mention, which is real
            # information about how the resource is used.
            prev = by_slug[slug]
            for cat in rec["categories"]:
                if cat not in prev["categories"]:
                    prev["categories"].append(cat)
            for tag in rec["tags"]:
                if tag not in prev["tags"]:
                    prev["tags"].append(tag)
            collisions.append(f"{slug}: merged a second mention from {rec['source_section']!r}")
            continue
        by_slug[slug] = rec
        seen[slug] = rec["name"]

    for rec in by_slug.values():
        slug = rec["slug"]

        out = catalog.RESOURCES_DIR / f"{slug}.yaml"
        if out.exists():
            # A resource that appears in two lists is genuinely cross-domain
            # (OpenFOAM is both chemical engineering and general engineering).
            # Merge the new domain and categories into the existing record
            # rather than dropping them; never overwrite curated fields.
            existing = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
            changed = False
            for key in ("domains", "categories", "tags"):
                for value in rec.get(key, []):
                    if value not in existing.get(key, []):
                        existing.setdefault(key, []).append(value)
                        changed = True
            if changed and not dry_run:
                with out.open("w", encoding="utf-8") as fh:
                    fh.write(
                        "# Generated by scripts/import_markdown_lists.py from the legacy\n"
                        "# Markdown list. Fields marked unknown were never recorded and need\n"
                        "# confirmation — see docs/verification-methodology.md.\n"
                    )
                    yaml.safe_dump(existing, fh, sort_keys=False, allow_unicode=True, width=100)
            verb = "merged into" if changed else "already covered by"
            collisions.append(f"{slug}: {verb} existing record")
            continue
        if not dry_run:
            with out.open("w", encoding="utf-8") as fh:
                fh.write(
                    "# Generated by scripts/import_markdown_lists.py from the legacy\n"
                    "# Markdown list. Fields marked unknown were never recorded and need\n"
                    "# confirmation — see docs/verification-methodology.md.\n"
                )
                yaml.safe_dump(rec, fh, sort_keys=False, allow_unicode=True, width=100)
        written += 1

    return written, collisions


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", dest="which", choices=sorted(catalog.LIST_DOMAINS), help="import one list")
    p.add_argument("--all", action="store_true", help="import every list")
    p.add_argument("--dry-run", action="store_true", help="report without writing")
    args = p.parse_args()

    if not args.which and not args.all:
        p.error("pass --list <name> or --all")

    stems = sorted(catalog.LIST_DOMAINS) if args.all else [args.which]
    total_written = 0
    all_warnings: list[str] = []

    for stem in stems:
        path = catalog.LISTS_DIR / f"{stem}.md"
        if not path.is_file():
            print(f"  !! missing {path}")
            continue
        domain = catalog.LIST_DOMAINS[stem]
        records, warnings = parse_list(path, domain)
        written, collisions = write_records(records, args.dry_run)
        total_written += written

        print(f"\n{stem}")
        print(f"  parsed    {len(records)} entries")
        print(f"  {'would write' if args.dry_run else 'wrote':<9} {written} records")
        for c in collisions:
            print(f"  skipped   {c}")
        for w in warnings:
            all_warnings.append(f"{stem}: {w}")

    if all_warnings:
        print(f"\n{len(all_warnings)} warning(s):")
        for w in all_warnings:
            print(f"  {w}")

    print(f"\nTotal: {total_written} record(s) {'would be ' if args.dry_run else ''}written "
          f"to {catalog.RESOURCES_DIR.relative_to(catalog.ROOT)}")
    print("Every imported record is verification tier 0 with unknown licence and "
          "maintenance status. That is accurate, not lazy — see docs/verification-methodology.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
