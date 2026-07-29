"""Shared catalog loading, for the validator and every generator.

One module owns "what is a record and where does it live", so a change to the
layout touches one file instead of five. Everything here is read-only: nothing
in this module writes to the catalog.
"""

from __future__ import annotations

import dataclasses
import functools
import pathlib
import re
from typing import Any, Iterator

import yaml

# Repository root, resolved from this file rather than the working directory, so
# the scripts work from anywhere.
ROOT = pathlib.Path(__file__).resolve().parents[2]

CATALOG_DIR = ROOT / "catalog"
RESOURCES_DIR = CATALOG_DIR / "resources"
PROJECTS_DIR = CATALOG_DIR / "projects"
TAXONOMY_DIR = CATALOG_DIR / "taxonomies"
SCHEMA_DIR = ROOT / "schemas"
LISTS_DIR = ROOT / "lists"
SITE_DIR = ROOT / "public"
SITE_DATA_DIR = SITE_DIR / "assets" / "data"
SITE_RESOURCE_DIR = SITE_DIR / "r"

# The five legacy lists, and the domain each maps onto. Kept explicit rather
# than derived from filenames so a renamed file fails loudly.
LIST_DOMAINS: dict[str, str] = {
    "awesome-chemical-engineering": "chemical-engineering",
    "awesome-chemoinformatics": "chemoinformatics",
    "awesome-bioengineering": "bioengineering",
    "awesome-medical-engineering": "medical-engineering",
    "awesome-general-engineering": "general-engineering",
}

LIST_TITLES: dict[str, str] = {
    "awesome-chemical-engineering": "Awesome Chemical Engineering",
    "awesome-chemoinformatics": "Awesome Chemoinformatics",
    "awesome-bioengineering": "Awesome Bioengineering",
    "awesome-medical-engineering": "Awesome Medical Engineering",
    "awesome-general-engineering": "Awesome General Engineering",
}

VERIFICATION_LABELS: dict[int, str] = {
    0: "Submitted",
    1: "Link checked",
    2: "Metadata checked",
    3: "Quick start reproduced",
    4: "Domain validated",
}

VERIFICATION_BLURBS: dict[int, str] = {
    0: "Recorded in the catalog. Nothing about it has been independently checked yet.",
    1: "The canonical URL was confirmed to resolve. Nothing else was checked.",
    2: "Name, licence, access model, repository, platform, and maintenance status "
       "were confirmed against authoritative sources on the date shown.",
    3: "A documented quick start was executed successfully in a pinned environment.",
    4: "Numerical or scientific output was compared against a cited benchmark by a "
       "qualified reviewer.",
}


@dataclasses.dataclass(frozen=True)
class Record:
    """A catalog record plus where it came from."""

    path: pathlib.Path
    data: dict[str, Any]

    @property
    def slug(self) -> str:
        return str(self.data.get("slug", self.path.stem))

    @property
    def name(self) -> str:
        return str(self.data.get("name", self.slug))

    @property
    def tier(self) -> int:
        return int(self.data.get("verification", {}).get("tier", 0))

    @property
    def rel_path(self) -> str:
        """Path relative to the repo root, for readable error messages.

        Falls back to the raw path for records constructed outside the tree,
        which tests do; an error message is never worth an exception.
        """
        try:
            return str(self.path.relative_to(ROOT))
        except ValueError:
            return str(self.path)


def _load_yaml(path: pathlib.Path) -> Any:
    """Parse YAML safely. yaml.safe_load never constructs arbitrary Python objects."""
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_records(directory: pathlib.Path) -> list[Record]:
    """Load every .yaml file in a directory, sorted by slug for stable output.

    Stable ordering matters: generated files are committed, and a generator whose
    output order depends on the filesystem produces noise diffs.
    """
    records: list[Record] = []
    if not directory.is_dir():
        return records
    for path in sorted(directory.glob("*.yaml")):
        data = _load_yaml(path)
        if data is None:
            raise ValueError(f"{path} is empty")
        if not isinstance(data, dict):
            raise ValueError(f"{path} must contain a YAML mapping, got {type(data).__name__}")
        records.append(Record(path=path, data=data))
    return sorted(records, key=lambda r: r.slug)


def load_resources() -> list[Record]:
    return load_records(RESOURCES_DIR)


def load_projects() -> list[Record]:
    return load_records(PROJECTS_DIR)


@functools.lru_cache(maxsize=1)
def load_categories() -> dict[str, list[str]]:
    path = TAXONOMY_DIR / "categories.yaml"
    if not path.is_file():
        return {}
    data = _load_yaml(path) or {}
    return {k: list(v or []) for k, v in data.items()}


def allowed_categories() -> set[str]:
    """Union of every category across all domains."""
    return {c for values in load_categories().values() for c in values}


def load_schema(name: str) -> dict[str, Any]:
    import json

    with (SCHEMA_DIR / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def slugify(text: str) -> str:
    """Turn a display name into a stable slug.

    Deterministic and lossy on purpose: two names that collide are a duplicate
    the validator should catch, not something to paper over with a suffix.
    """
    text = text.strip().lower()
    text = text.replace("+", " plus ").replace("&", " and ").replace("#", " sharp ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Strip AFTER truncating: cutting at 64 chars can land on a hyphen and
    # produce a trailing separator that fails the slug pattern.
    return re.sub(r"-{2,}", "-", text)[:64].strip("-")


def iter_list_files() -> Iterator[tuple[str, pathlib.Path]]:
    for stem in LIST_DOMAINS:
        yield stem, LISTS_DIR / f"{stem}.md"
