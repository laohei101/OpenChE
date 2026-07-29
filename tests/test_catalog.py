"""Tests for the catalog tooling.

Run with: python -m pytest

These test the GENERATION CODE, not the catalog content — content correctness is
what scripts/validate_catalog.py checks, and it runs in CI as its own step. The
split matters: a bad record should fail validation with a helpful message, and a
bad generator should fail here with a stack trace.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from openche import catalog  # noqa: E402

import generate_markdown_lists as gml  # noqa: E402
import generate_resource_pages as grp  # noqa: E402
import generate_search_index as gsi  # noqa: E402


# ---------------------------------------------------------------------------
# catalog loading
# ---------------------------------------------------------------------------

def test_catalog_loads():
    records = catalog.load_resources()
    assert records, "no resource records found"
    assert all(r.slug for r in records)


def test_records_sorted_by_slug():
    """Generators depend on stable ordering to avoid noise diffs."""
    records = catalog.load_resources()
    assert [r.slug for r in records] == sorted(r.slug for r in records)


def test_slug_matches_filename():
    for rec in catalog.load_resources():
        assert rec.path.stem == rec.slug, f"{rec.rel_path} filename does not match slug"


def test_no_duplicate_canonical_urls():
    seen: dict[str, str] = {}
    for rec in catalog.load_resources():
        url = rec.data["canonical_url"].lower().rstrip("/")
        assert url not in seen, f"{rec.slug} duplicates {seen[url]}"
        seen[url] = rec.slug


@pytest.mark.parametrize("text,expected", [
    ("DWSIM", "dwsim"),
    ("Open Babel", "open-babel"),
    ("C++ Toolkit", "c-plus-plus-toolkit"),
    ("  Spaced  Out  ", "spaced-out"),
    ("Trailing punctuation!!!", "trailing-punctuation"),
    ("Multiple---Hyphens", "multiple-hyphens"),
])
def test_slugify(text, expected):
    assert catalog.slugify(text) == expected


def test_slugify_never_yields_trailing_separator():
    """Truncation at 64 chars must not leave a hyphen that fails the pattern."""
    long_name = "Nick Higham's Handbook of Writing for the Mathematical Sciences notes"
    slug = catalog.slugify(long_name)
    assert len(slug) <= 64
    assert not slug.startswith("-") and not slug.endswith("-")
    assert "--" not in slug


# ---------------------------------------------------------------------------
# generators are deterministic and idempotent
# ---------------------------------------------------------------------------

def test_markdown_generation_is_deterministic():
    records = catalog.load_resources()
    first = gml.render_list("awesome-chemical-engineering", records)
    second = gml.render_list("awesome-chemical-engineering", records)
    assert first == second


def test_markdown_lists_are_current():
    """The committed lists must match what the generator produces."""
    records = catalog.load_resources()
    for stem in catalog.LIST_DOMAINS:
        path = catalog.LISTS_DIR / f"{stem}.md"
        assert path.exists(), f"{path} missing — run generate_markdown_lists.py"
        assert path.read_text(encoding="utf-8") == gml.render_list(stem, records), (
            f"{stem}.md is stale — run: python scripts/generate_markdown_lists.py"
        )


def test_every_record_appears_in_a_list():
    """A record nobody can reach through a list is invisible."""
    records = catalog.load_resources()
    rendered = "\n".join(gml.render_list(stem, records) for stem in catalog.LIST_DOMAINS)
    missing = [r.slug for r in records if r.data["canonical_url"] not in rendered]
    assert not missing, f"{len(missing)} record(s) render into no list: {missing[:5]}"


def test_generated_lists_carry_the_do_not_edit_banner():
    for stem in catalog.LIST_DOMAINS:
        text = (catalog.LISTS_DIR / f"{stem}.md").read_text(encoding="utf-8")
        assert "GENERATED FILE" in text, f"{stem}.md lost its banner"


# ---------------------------------------------------------------------------
# search index
# ---------------------------------------------------------------------------

def test_search_index_is_current():
    records = catalog.load_resources()
    path = catalog.SITE_DATA_DIR / "resources.json"
    assert path.exists()
    assert path.read_text(encoding="utf-8") == gsi.build(records), (
        "search index is stale — run: python scripts/generate_search_index.py"
    )


def test_search_index_covers_every_record():
    """The old hand-maintained index drifted to ~45% coverage. Never again."""
    records = catalog.load_resources()
    payload = json.loads(gsi.build(records))
    assert len(payload) == len(records)
    assert {p["slug"] for p in payload} == {r.slug for r in records}


def test_search_index_within_size_budget():
    """Spec section 20: under 500 KB for the first 1000 records."""
    records = catalog.load_resources()
    size_kb = len(gsi.build(records).encode("utf-8")) / 1024
    assert size_kb < 500, f"search index is {size_kb:.0f} KB, over the 500 KB budget"


def test_search_records_have_required_fields():
    for rec in catalog.load_resources():
        out = gsi.to_search_record(rec)
        for field in ("slug", "name", "url", "description", "category", "tags", "tier", "detail"):
            assert field in out, f"{rec.slug} search record missing {field}"
        assert out["detail"] == f"/r/{rec.slug}.html"


def test_search_categories_match_the_filter_buttons():
    """A category with no button is unreachable in the UI."""
    html = (catalog.SITE_DIR / "search.html").read_text(encoding="utf-8")
    for rec in catalog.load_resources():
        cat = gsi.to_search_record(rec)["category"]
        assert f'data-filter="{cat}"' in html, f"no filter button for category {cat!r}"


# ---------------------------------------------------------------------------
# generated HTML
# ---------------------------------------------------------------------------

def test_resource_pages_exist_for_every_record():
    for rec in catalog.load_resources():
        page = catalog.SITE_RESOURCE_DIR / f"{rec.slug}.html"
        assert page.exists(), f"missing detail page for {rec.slug}"


def test_no_orphan_resource_pages():
    """A page for a deleted record would 404 from search but still be indexable."""
    slugs = {r.slug for r in catalog.load_resources()}
    orphans = [p.stem for p in catalog.SITE_RESOURCE_DIR.glob("*.html") if p.stem not in slugs]
    assert not orphans, f"orphaned pages: {orphans[:5]}"


def test_resource_page_escapes_html():
    """Record text is contributor-supplied and must never be injected raw."""
    rec = catalog.Record(
        path=pathlib.Path("catalog/resources/xss-probe.yaml"),
        data={
            "slug": "xss-probe",
            "name": "<script>alert(1)</script>",
            "kind": "library",
            "canonical_url": "https://example.org",
            "summary": 'Quote " and <b>bold</b> and & ampersand.',
            "domains": ["chemical-engineering"],
            "categories": ["thermodynamics"],
            "audiences": ["student"],
            "access": {"model": "unknown"},
            "license": {"spdx": "UNKNOWN"},
            "maturity": "unknown",
            "maintenance_status": "unknown",
            "verification": {"tier": 0, "status": "submitted"},
            "tags": ["test"],
        },
    )
    html = grp.render_resource(rec, {})
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
    assert "<b>bold</b>" not in html


def test_tier_zero_page_says_nothing_was_checked():
    """The core trust rule: an unchecked record must say so, in words."""
    records = catalog.load_resources()
    tier0 = next(r for r in records if r.tier == 0)
    html = grp.render_resource(tier0, {})
    assert "Tier 0" in html
    assert "No check has been performed" in html
    assert "verify-t0" in html


def test_pages_do_not_claim_verification_without_evidence():
    """No page may show a tier above 0 unless the record carries evidence."""
    for rec in catalog.load_resources():
        if rec.tier >= 1:
            assert rec.data.get("evidence"), (
                f"{rec.slug} claims tier {rec.tier} with no evidence"
            )


def test_generated_pages_are_current():
    records = catalog.load_resources()
    by_slug = {r.slug: r for r in records}
    sample = records[:20] + records[-20:]
    for rec in sample:
        page = catalog.SITE_RESOURCE_DIR / f"{rec.slug}.html"
        assert page.read_text(encoding="utf-8") == grp.render_resource(rec, by_slug), (
            f"{rec.slug}.html is stale — run: python scripts/generate_resource_pages.py"
        )


def test_compare_page_lists_real_records():
    slugs = {r.slug for r in catalog.load_resources()}
    known = [s for s in grp.COMPARE_SETS if s in slugs]
    assert known, f"COMPARE_SETS {grp.COMPARE_SETS} contains no existing record"


# ---------------------------------------------------------------------------
# projects
# ---------------------------------------------------------------------------

def test_project_records_load():
    projects = catalog.load_projects()
    assert projects, "no project records found"


def test_project_validation_checks_are_specific():
    """A project without a way to check the answer is a tutorial, not engineering."""
    for proj in catalog.load_projects():
        checks = proj.data["validation"]["checks"]
        assert checks, f"{proj.slug} has no validation checks"
        for c in checks:
            assert c.get("method"), f"{proj.slug} check has no method"


def test_project_resume_bullets_are_concrete():
    """Spec 9.4: bullets must state what was built and measured, not adjectives."""
    banned = {"revolutionary", "cutting-edge", "world-class", "expert-level", "industry-leading"}
    for proj in catalog.load_projects():
        for bullet in proj.data.get("resume_bullets", []):
            low = bullet.lower()
            assert not any(w in low for w in banned), f"{proj.slug}: inflated bullet {bullet!r}"
            assert any(ch.isdigit() for ch in bullet), (
                f"{proj.slug}: bullet has no measured quantity: {bullet!r}"
            )


# ---------------------------------------------------------------------------
# the validator itself
# ---------------------------------------------------------------------------

def test_validator_passes_on_the_committed_catalog():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_catalog.py"), "--quiet"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"validator failed:\n{proc.stdout}\n{proc.stderr}"


def test_validator_rejects_a_bad_record(tmp_path, monkeypatch):
    """The validator must actually fail on a broken record, not just pass everything."""
    import validate_catalog as vc

    bad = catalog.Record(
        path=tmp_path / "bad.yaml",
        data={
            "schema_version": 1,
            "slug": "bad",
            "name": "Bad",
            "kind": "not-a-real-kind",          # enum violation
            "canonical_url": "not-a-url",       # pattern violation
            "summary": "too short",             # minLength violation
            "domains": [],                      # minItems violation
            "categories": ["nonexistent-category"],
            "audiences": ["student"],
            "access": {"model": "unknown"},
            "license": {"spdx": "UNKNOWN"},
            "maturity": "unknown",
            "maintenance_status": "unknown",
            "verification": {"tier": 3, "status": "submitted"},  # tier/status mismatch, no evidence
            "tags": ["x"],
        },
    )
    rep = vc.Report()
    vc.check_schema([bad], "resource.schema.json", rep)
    vc.check_taxonomy([bad], rep)
    vc.check_verification([bad], rep)
    assert len(rep.errors) >= 4, f"expected several errors, got: {rep.errors}"
    assert any("tier 3" in e for e in rep.errors)


def test_verification_tier_labels_cover_every_tier():
    for tier in range(5):
        assert tier in catalog.VERIFICATION_LABELS
        assert tier in catalog.VERIFICATION_BLURBS
