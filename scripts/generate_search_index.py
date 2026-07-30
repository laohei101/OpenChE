#!/usr/bin/env python3
"""Generate the website search index from the canonical catalog.

    python scripts/generate_search_index.py            # write
    python scripts/generate_search_index.py --check    # fail if stale (CI)

Replaces the old hand-maintained tuple list in the legacy build_index.py, which
was a second source of truth and had drifted to about 200 of 446 entries. Every
catalog record now appears, so "in the list" and "findable on the site" are the
same thing.

Output: public/assets/data/resources.json

The payload is deliberately trimmed. The full record has evidence URLs, notes,
and provenance that the search page never reads, and shipping them would push
the index past the 500 KB budget in spec section 20 for no benefit. The detail
pages carry the full record.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from openche import catalog  # noqa: E402

# Domain -> the filter key the search page uses. Kept aligned with the buttons
# in public/search.html; a mismatch silently yields an empty filter.
DOMAIN_FILTERS = {
    "chemical-engineering": "chemical-engineering",
    "process-systems-engineering": "chemical-engineering",
    "chemoinformatics": "chemoinformatics",
    "bioengineering": "bioengineering",
    "medical-engineering": "medical-engineering",
    "general-engineering": "general-engineering",
    "sustainability": "general-engineering",
    "electrochemistry": "general-engineering",
    "materials": "general-engineering",
    "energy": "general-engineering",
}


def to_search_record(rec: catalog.Record) -> dict:
    d = rec.data
    domains = d.get("domains", [])
    category = DOMAIN_FILTERS.get(domains[0], "general-engineering") if domains else "general-engineering"

    # Tags shown on a result card: language tags first (most useful for
    # filtering by eye), then descriptive tags, capped so cards stay scannable.
    tags = [t for t in (d.get("languages") or [])] + [
        t for t in d.get("tags", []) if t != "uncategorised"
    ]

    out = {
        "slug": d["slug"],
        "name": d["name"],
        "url": d["canonical_url"],
        "description": d.get("summary", ""),
        "category": category,
        "section": (d.get("categories") or [""])[0].replace("-", " ").title(),
        "tags": tags[:6],
        "kind": d.get("kind"),
        "tier": rec.tier,
        "detail": f"/r/{d['slug']}.html",
    }
    access = (d.get("access") or {}).get("model")
    if access and access != "unknown":
        out["access"] = access
    return out


def build(records: list[catalog.Record]) -> str:
    payload = [to_search_record(r) for r in records]
    payload.sort(key=lambda r: r["name"].lower())
    return json.dumps(payload, indent=1, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    records = catalog.load_resources()
    rendered = build(records)

    out = catalog.SITE_DATA_DIR / "resources.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    size_kb = len(rendered.encode("utf-8")) / 1024

    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            print(f"fail  {out.relative_to(catalog.ROOT)} is stale")
            print("      Run: python scripts/generate_search_index.py")
            return 1
        print(f"  ok     search index up to date ({len(records)} records, {size_kb:.0f} KB)")
        return 0

    out.write_text(rendered, encoding="utf-8")
    print(f"  wrote  {out.relative_to(catalog.ROOT)} — {len(records)} records, {size_kb:.0f} KB")

    # Spec section 20: search index under 500 KB for the first 1000 records.
    if size_kb > 500:
        print(f"  WARN   index is {size_kb:.0f} KB, over the 500 KB budget in the spec")
        print("         Trim fields in to_search_record() before adding more records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
