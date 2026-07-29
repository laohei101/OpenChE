#!/usr/bin/env python3
"""Validate the canonical catalog.

    python scripts/validate_catalog.py            # validate everything
    python scripts/validate_catalog.py --strict   # warnings become errors

Checks, per spec section 19.1:

  schema        every record validates against schemas/*.schema.json
  slugs         unique, and matching the filename
  urls          well-formed, and no two records claim the same canonical URL
  taxonomy      categories drawn from catalog/taxonomies/categories.yaml
  references    alternatives / related / requirements point at records that exist
  dates         ISO-8601, not in the future
  verification  tier and status agree, and a claim above tier 0 carries evidence

Exit codes
----------
0  clean (warnings may still be printed)
1  errors found
2  could not run at all

The distinction between an error and a warning is deliberate. Errors are things
that are definitely wrong and that a contributor can fix from the message alone.
Warnings are incompleteness — an unknown licence, a missing evidence link — which
is the expected state of a freshly imported record and must not block CI, or the
migration would be unmergeable.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import pathlib
import re
import sys
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import jsonschema  # noqa: E402

from openche import catalog  # noqa: E402

# A permissive SPDX subset: enough to catch typos and placeholders without
# vendoring the full 600-entry licence list, which would rot.
KNOWN_SPDX = {
    "UNKNOWN", "MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0",
    "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
    "LGPL-2.1-only", "LGPL-3.0-only", "LGPL-3.0-or-later", "MPL-2.0",
    "AGPL-3.0-only", "AGPL-3.0-or-later", "EPL-2.0", "CDDL-1.0",
    "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0", "Unlicense",
    "ISC", "Zlib", "BSL-1.0", "PSF-2.0", "NCSA", "Artistic-2.0",
    "proprietary", "custom", "multiple",
}

TIER_STATUS = {
    0: {"submitted"},
    1: {"link-checked", "needs-recheck"},
    2: {"metadata-verified", "needs-recheck"},
    3: {"quickstart-reproduced", "needs-recheck"},
    4: {"domain-validated", "needs-recheck"},
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def check_schema(records: list[catalog.Record], schema_name: str, rep: Report) -> None:
    schema = catalog.load_schema(schema_name)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for rec in records:
        for err in sorted(validator.iter_errors(rec.data), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(root)"
            rep.error(rec.rel_path, f"schema at {location}: {err.message}")


def check_slugs(records: list[catalog.Record], rep: Report) -> None:
    by_slug: dict[str, list[catalog.Record]] = collections.defaultdict(list)
    for rec in records:
        by_slug[rec.slug].append(rec)
        if rec.path.stem != rec.slug:
            rep.error(rec.rel_path, f"filename does not match slug {rec.slug!r}")
    for slug, group in by_slug.items():
        if len(group) > 1:
            paths = ", ".join(r.rel_path for r in group)
            rep.error(slug, f"duplicate slug in {paths}")


def _normalise_url(url: str) -> str:
    """Compare URLs ignoring differences that do not change the destination."""
    p = urlparse(url.lower())
    host = p.netloc.removeprefix("www.")
    path = p.path.rstrip("/")
    return f"{host}{path}"


def check_urls(records: list[catalog.Record], rep: Report) -> None:
    by_url: dict[str, list[str]] = collections.defaultdict(list)
    for rec in records:
        for field in ("canonical_url", "repository_url", "docs_url", "download_url"):
            url = rec.data.get(field)
            if not url:
                continue
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                rep.error(rec.rel_path, f"{field} is not a valid http(s) URL: {url!r}")
            if " " in url:
                rep.error(rec.rel_path, f"{field} contains a space: {url!r}")
        canonical = rec.data.get("canonical_url")
        if canonical:
            by_url[_normalise_url(canonical)].append(rec.slug)

    for url, slugs in by_url.items():
        if len(slugs) > 1:
            rep.error("catalog", f"duplicate canonical URL {url!r} in: {', '.join(sorted(slugs))}")


def check_taxonomy(records: list[catalog.Record], rep: Report) -> None:
    allowed = catalog.allowed_categories()
    per_domain = catalog.load_categories()
    if not allowed:
        rep.warn("catalog", "no category taxonomy found; category checks skipped")
        return
    for rec in records:
        for cat in rec.data.get("categories", []):
            if cat not in allowed:
                rep.error(rec.rel_path, f"category {cat!r} is not in the taxonomy")
                continue
            domains = rec.data.get("domains", [])
            if domains and not any(cat in per_domain.get(d, []) for d in domains):
                rep.warn(
                    rec.rel_path,
                    f"category {cat!r} is not listed under any of this record's "
                    f"domains {domains}",
                )


def check_references(
    resources: list[catalog.Record], projects: list[catalog.Record], rep: Report
) -> None:
    known = {r.slug for r in resources}
    known_projects = {p.slug for p in projects}

    for rec in resources:
        for field in ("alternatives", "related_projects", "related_datasets", "archived_replacement"):
            value = rec.data.get(field)
            if value is None:
                continue
            targets = [value] if isinstance(value, str) else value
            pool = known_projects if field == "related_projects" else known
            for target in targets:
                if target not in pool:
                    rep.error(rec.rel_path, f"{field} points at unknown slug {target!r}")

    for proj in projects:
        reqs = proj.data.get("requirements", {}) or {}
        for target in reqs.get("resources", []) or []:
            if target not in known:
                rep.error(proj.rel_path, f"requirements.resources -> unknown resource {target!r}")


def check_dates(records: list[catalog.Record], rep: Report) -> None:
    today = dt.date.today()
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def check(where: str, value: Any, label: str) -> None:
        if value is None:
            return
        if not isinstance(value, (str, dt.date)):
            rep.error(where, f"{label} is not a date: {value!r}")
            return
        if isinstance(value, dt.date):
            parsed = value
        else:
            if not pattern.match(value):
                rep.error(where, f"{label} is not ISO-8601 (YYYY-MM-DD): {value!r}")
                return
            try:
                parsed = dt.date.fromisoformat(value)
            except ValueError as exc:
                rep.error(where, f"{label} is not a real date: {value!r} ({exc})")
                return
        if parsed > today:
            rep.error(where, f"{label} is in the future: {parsed.isoformat()}")

    for rec in records:
        check(rec.rel_path, rec.data.get("verification", {}).get("checked_at"), "verification.checked_at")
        for ev in rec.data.get("evidence", []) or []:
            check(rec.rel_path, ev.get("retrieved_at"), "evidence.retrieved_at")
        for qs in rec.data.get("quickstarts", []) or []:
            check(rec.rel_path, (qs.get("verified_on") or {}).get("date"), "quickstarts.verified_on.date")


def check_verification(records: list[catalog.Record], rep: Report) -> None:
    for rec in records:
        v = rec.data.get("verification", {}) or {}
        tier = v.get("tier")
        status = v.get("status")
        if tier is None or status is None:
            continue  # schema already reported it
        allowed = TIER_STATUS.get(tier, set())
        if status not in allowed:
            rep.error(
                rec.rel_path,
                f"verification tier {tier} is inconsistent with status {status!r} "
                f"(expected one of {sorted(allowed)})",
            )
        if tier >= 1 and not rec.data.get("evidence"):
            rep.error(rec.rel_path, f"verification tier {tier} claimed without any evidence entries")
        if tier >= 2 and rec.data.get("license", {}).get("spdx") == "UNKNOWN":
            rep.error(
                rec.rel_path,
                "verification tier 2 means the licence was confirmed, but spdx is UNKNOWN",
            )


def check_completeness(records: list[catalog.Record], rep: Report) -> None:
    """Incompleteness is a warning, never an error. See the module docstring."""
    for rec in records:
        lic = rec.data.get("license", {}) or {}
        if lic.get("spdx") == "UNKNOWN":
            rep.warn(rec.rel_path, "licence not confirmed (spdx: UNKNOWN)")
        elif lic.get("spdx") not in KNOWN_SPDX:
            rep.warn(rec.rel_path, f"spdx {lic.get('spdx')!r} is not in the known-identifier list")
        if rec.data.get("maintenance_status") == "unknown":
            rep.warn(rec.rel_path, "maintenance status not confirmed")
        if (rec.data.get("access", {}) or {}).get("model") == "unknown":
            rep.warn(rec.rel_path, "access model not confirmed")
        if rec.tier == 0:
            rep.warn(rec.rel_path, "verification tier 0 (nothing independently checked)")


def summarise(resources: list[catalog.Record]) -> None:
    tiers = collections.Counter(r.tier for r in resources)
    domains = collections.Counter(d for r in resources for d in r.data.get("domains", []))
    kinds = collections.Counter(r.data.get("kind") for r in resources)

    print(f"\n  {len(resources)} resource record(s)")
    print("\n  verification tiers")
    for tier in range(5):
        n = tiers.get(tier, 0)
        bar = "#" * min(40, n // 5)
        print(f"    {tier} {catalog.VERIFICATION_LABELS[tier]:<24} {n:>4}  {bar}")
    print("\n  domains")
    for domain, n in sorted(domains.items()):
        print(f"    {domain:<30} {n:>4}")
    print("\n  kinds")
    for kind, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f"    {str(kind):<30} {n:>4}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.add_argument("--quiet", action="store_true", help="only print the summary line")
    p.add_argument("--max-warnings", type=int, default=25, help="warnings to print before truncating")
    args = p.parse_args()

    rep = Report()

    try:
        resources = catalog.load_resources()
        projects = catalog.load_projects()
    except Exception as exc:  # malformed YAML, unreadable file
        print(f"fail  could not load the catalog: {exc}", file=sys.stderr)
        return 2

    if not resources:
        print("fail  no resource records found in catalog/resources", file=sys.stderr)
        return 2

    check_schema(resources, "resource.schema.json", rep)
    check_schema(projects, "project.schema.json", rep)
    check_slugs(resources + projects, rep)
    check_urls(resources, rep)
    check_taxonomy(resources, rep)
    check_references(resources, projects, rep)
    check_dates(resources + projects, rep)
    check_verification(resources, rep)
    check_completeness(resources, rep)

    if not args.quiet:
        summarise(resources)
        if projects:
            print(f"\n  {len(projects)} project record(s)")

    if rep.warnings:
        shown = rep.warnings[: args.max_warnings]
        print(f"\n  {len(rep.warnings)} warning(s) — incompleteness, not breakage:")
        for w in shown:
            print(f"    {w}")
        if len(rep.warnings) > len(shown):
            print(f"    ... and {len(rep.warnings) - len(shown)} more")

    if rep.errors:
        print(f"\n  {len(rep.errors)} ERROR(S):")
        for e in rep.errors:
            print(f"    {e}")
        return 1

    if args.strict and rep.warnings:
        print("\nfail  --strict: warnings are errors")
        return 1

    print("\n  Catalog is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
