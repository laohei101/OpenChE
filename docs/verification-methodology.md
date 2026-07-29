# Verification methodology

**What "verified" means here, exactly, and what it does not.**

A curated list is worth what its curator has actually checked. Most lists paper over the gap
between "someone added this" and "someone confirmed this" with a green tick. OpenChemE does not:
every record carries a tier, and a tier above 0 is a specific claim backed by dated evidence.

---

## The tiers

| Tier | Name | What was actually done | What it does *not* mean |
| :-: | --- | --- | --- |
| **0** | Submitted | The record exists. Nothing has been checked. | Nothing. This is the default and it is honest. |
| **1** | Link checked | The canonical URL resolves, or a human confirmed it by hand. | Nothing about licence, quality, or maintenance. |
| **2** | Metadata checked | Name, licence, access model, repository, platform, and maintenance status confirmed against authoritative sources on the date shown. | Nobody ran it. |
| **3** | Quick start reproduced | A documented example was executed successfully in a pinned environment, by a named person, on a recorded date. | The scientific output was not checked against a reference. |
| **4** | Domain validated | Numerical or scientific output was compared with a cited benchmark, reference case, or independent implementation, by a qualified reviewer. | Not a warranty, and not a substitute for your own validation. |

**The site never shows a bare badge.** Every detail page states the tier, spells out in a sentence
what that tier means, gives the check date and the checker, and links the evidence. A tier-0
record says *"Nothing about it has been independently checked yet"* in plain words, and its
unknown fields render as *not confirmed* in italics rather than as blanks that read like answers.

## Current state of the catalog, stated plainly

**Every one of the 361 imported resource records is tier 0.** Licence, maintenance status, and
access model are `unknown` on almost all of them.

That is not a backlog nobody got to. The records were imported from Markdown bullets, which never
carried those fields, and the environment the migration ran in could not reach the sources needed
to fill them: the egress policy denied connections to roughly 99% of hosts, including all of
`github.com`. An automated link check returned 403 on 358 of 386 URLs — indistinguishable from a
dead link at the network layer, and therefore useless as evidence either way.

Two options were available. Mark 25 well-known projects as tier 2 from memory, which would look
like progress and would be fabrication. Or mark everything tier 0 and say why. The second is what
the spec asks for in §28 — *prefer transparent incompleteness over plausible fabrication* — and
it is what the catalog does.

The one exception is the pilot project record, which is **tier 3**: its starter notebook was
executed end to end in this environment and every balance closed to machine precision. That is a
claim about our own material, checkable by anyone running
`python scripts/run_template_smoke_tests.py`.

## Promoting a record

### To tier 1 — link checked

Confirm the canonical URL resolves and lands on the project, not a parked domain or a redirect to
something unrelated.

```yaml
verification:
  tier: 1
  status: link-checked
  checked_at: "2026-08-01"
  checked_by: your-github-handle
link_status: ok
evidence:
  - type: official-site
    url: https://example.org
    retrieved_at: "2026-08-01"
```

Evidence is required from tier 1 upward — the schema enforces it, and so does the validator.

### To tier 2 — metadata checked

Confirm each field from an **authoritative** source, meaning the project's own site, its
repository, or its package registry entry. Not a blog post, not another awesome list, not your
recollection.

```yaml
license:
  spdx: GPL-3.0-only
  source: repository
access:
  model: open-source-with-supporter-editions
  open_source_release: true
  free_tier: true
  paid_features_exist: true
maintenance_status: active
platforms: [windows, macos, linux]
verification:
  tier: 2
  status: metadata-verified
  checked_at: "2026-08-01"
  checked_by: your-github-handle
  notes:
    - Licence read from LICENSE in the repository at commit abc1234.
    - Supporter-only builds confirmed on the official download page.
evidence:
  - type: repository
    url: https://github.com/example/project
    retrieved_at: "2026-08-01"
  - type: official-release-page
    url: https://example.org/download
    retrieved_at: "2026-08-01"
```

The validator refuses tier 2 with `spdx: UNKNOWN`. Claiming you confirmed the licence while
recording that you don't know it is the contradiction the check exists to catch.

### To tier 3 — quick start reproduced

Run a documented example, in a pinned environment, and record what you ran it with.

```yaml
quickstarts:
  - title: Build a flash separator
    url: /projects/dwsim-flash-separator/
    verified_on:
      product_version: "9.0.5"
      date: "2026-08-01"
verification:
  tier: 3
  status: quickstart-reproduced
  checked_at: "2026-08-01"
  checked_by: your-github-handle
  notes:
    - Ran on Windows 11, DWSIM 9.0.5, default property package.
    - Outlet vapour fraction 0.34; the tutorial states 0.34.
```

"Pinned" means someone else can reconstruct the environment: exact versions, or a container
digest. If you cannot pin it, say so in the notes and the record stays tier 3 with a caveat
rather than silently implying more than was done.

### To tier 4 — domain validated

The highest tier and the rarest. Numerical output compared against a cited benchmark by someone
qualified to judge it.

Requires all of:

- The reference, cited precisely enough to look up — textbook, edition, example number, or DOI.
- The comparison, with numbers and a stated tolerance.
- The reviewer's name and their basis for reviewing it.
- The conditions under which the agreement holds, and where it stops.

```yaml
verification:
  tier: 4
  status: domain-validated
  checked_at: "2026-08-01"
  checked_by: a-reviewer (PhD, reaction engineering)
  notes:
    - Adiabatic flame temperature for stoichiometric CH4/air at 1 atm, 300 K inlet.
    - Computed 2225 K; Turns, An Introduction to Combustion, 3rd ed., Table 2.3 gives 2226 K.
    - Agreement within 0.05%. Holds for lean to stoichiometric; not checked rich of phi = 1.2.
```

## Re-checking, and going stale

Verification decays. A licence changes, a project is archived, a maintainer moves the repository.

- **Tier 2 and above expires after 12 months.** Set `status: needs-recheck`, keep the tier, and
  the page will show the original date so a reader can judge for themselves.
- **Never silently downgrade.** Removing a verification claim without saying why loses the
  information that it was once true.
- The scheduled link checker (`.github/workflows/links.yml`) reports rot weekly and opens a
  tracking issue.

## Link status is not the same as link validity

Spec §6.4, and a lesson learned the hard way during this migration. A failed HTTP request has
many causes and only one of them is a dead link:

| Status | Meaning | CI behaviour |
| --- | --- | --- |
| `ok` | Resolves | pass |
| `redirected` | Resolves via a redirect; the canonical URL may want updating | report |
| `blocked` | The host refuses automated requests — common for ISO, IEC, FDA, publishers | report, never fail |
| `rate-limited` | 429; try again later | report |
| `auth-required` | Real resource behind a login | report, review the access model |
| `manual-check-needed` | Automation cannot decide | report |
| `dead` | Confirmed gone by a human | fail |
| `unknown` | Not yet checked | neutral |

CI fails only on malformed URLs, confirmed-dead internal links, duplicate canonical URLs, and
schema violations. A blocked external host produces a report, not a red build — otherwise the
build breaks whenever a government website changes its bot policy, and everyone learns to ignore
the checker.

## What verification is not

- **Not an endorsement.** Tier 4 means the numbers matched a reference on one case. It is not a
  recommendation for your problem.
- **Not a warranty.** Everything here is reference material, offered as-is.
- **Not a safety sign-off.** No tier at any level makes a tool suitable for a safety-critical
  application. A licensed engineer accountable for the work makes that call.
- **Not a quality ranking.** A tier-0 record may be the best tool in its category and simply
  new to the catalog. The tier measures what *we* checked, not how good the project is.

## Reporting a wrong claim

If a record claims something untrue, that is the most serious kind of bug here — worse than a
dead link, because a reader may act on it.

[Open an issue](https://github.com/OpenChemE/issues/new?template=add_resource.yml) or edit the
YAML directly. Include what the record says, what is actually the case, and where you checked.
Verification claims that turn out to be wrong get the tier reverted to 0 the same day, and the
reason recorded in the notes.
