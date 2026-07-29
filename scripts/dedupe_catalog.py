#!/usr/bin/env python3
"""Merge catalog records that point at the same canonical URL.

    python scripts/dedupe_catalog.py --dry-run
    python scripts/dedupe_catalog.py

The legacy lists sometimes mentioned one resource twice under different display
names — "ht" in the thermodynamics section and "HTRI alternatives — ht exchanger
sizing" under unit operations. Those are one resource seen from two angles, not
two resources.

The keeper is the record with the shortest slug, which in practice is the one
named after the project rather than after the sentence someone wrote about it.
Domains, categories, tags, and languages from the discarded record are merged
in, so nothing about how the resource is used is lost. The discarded summary is
appended to the keeper's `verification.notes` rather than thrown away, because
it often contains the more specific description.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import sys
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import yaml  # noqa: E402

from openche import catalog  # noqa: E402

MERGE_LIST_FIELDS = ("domains", "categories", "tags", "languages", "platforms", "audiences")


def normalise(url: str) -> str:
    p = urlparse(url.lower())
    return f"{p.netloc.removeprefix('www.')}{p.path.rstrip('/')}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    records = catalog.load_resources()
    groups: dict[str, list[catalog.Record]] = collections.defaultdict(list)
    for rec in records:
        url = rec.data.get("canonical_url")
        if url:
            groups[normalise(url)].append(rec)

    merged = 0
    for url, group in sorted(groups.items()):
        if len(group) < 2:
            continue
        # Shortest slug wins: it is the project's name, not a description of it.
        group.sort(key=lambda r: (len(r.slug), r.slug))
        keeper, *dupes = group
        data = dict(keeper.data)

        for dupe in dupes:
            for field in MERGE_LIST_FIELDS:
                for value in dupe.data.get(field, []) or []:
                    if value not in (data.get(field) or []):
                        data.setdefault(field, []).append(value)
            note = (
                f"Merged duplicate record {dupe.slug!r} (same canonical URL). "
                f"Its description was: {dupe.data.get('summary', '').strip()}"
            )
            data.setdefault("verification", {}).setdefault("notes", []).append(note[:400])

        print(f"  {url}")
        print(f"    keep  {keeper.slug}")
        for d in dupes:
            print(f"    drop  {d.slug}")

        if not args.dry_run:
            with keeper.path.open("w", encoding="utf-8") as fh:
                fh.write("# Canonical catalog record. Edit this, not the generated views.\n")
                yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=True, width=100)
            for d in dupes:
                d.path.unlink()
        merged += len(dupes)

    verb = "would merge" if args.dry_run else "merged"
    print(f"\n{verb} {merged} duplicate record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
