# Maintainers

Areas and who owns them. An unowned area is marked as such rather than quietly assigned to
whoever last touched it — pretending an area has a reviewer is how pull requests rot.

---

## Project lead

| | |
| --- | --- |
| **Kevin Dai** | [@laohei101](https://github.com/laohei101) · yu.dai@mail.utoronto.ca |

Direction, maintainer appointments, conduct and security reports, tie-breaking.

## Areas

| Area | Paths | Maintainer |
| --- | --- | --- |
| Catalog and schema | `catalog/`, `schemas/`, `scripts/` | Project lead |
| Chemical engineering | records in `chemical-engineering` | **Seeking** |
| Chemoinformatics | records in `chemoinformatics` | **Seeking** |
| Bioengineering | records in `bioengineering` | **Seeking** |
| Medical engineering | records in `medical-engineering` | **Seeking** |
| General engineering | records in `general-engineering` | **Seeking** |
| Templates | `templates/` | Project lead |
| Workflows | `workflows/` | **Seeking** |
| Site | `public/`, `scripts/generate_*` | Project lead |
| Safety review | `templates/safety_checklist.md`, anything safety-adjacent | **Seeking — see below** |

## Safety review is the gap that matters

Several files touch process safety: the HAZOP-style checklist, the reactor template's runaway
caveat, the medical engineering regulatory section. They carry explicit disclaimers and they are
written carefully, but **no qualified process safety engineer has reviewed them.**

If you hold that qualification and would review this material, please get in touch. Until then
the disclaimers are doing work they should not have to do alone.

## Becoming a maintainer

No application form. The path is: contribute in an area, review other people's pull requests
there, and demonstrate the judgement the role needs — which is mostly knowing when *not* to
merge. The project lead invites you.

What an area maintainer does:

- Reviews pull requests touching their area, within about a week
- Verifies records: confirms metadata against real sources, raises tiers with evidence
- Says no to entries that do not meet the bar, and explains which criterion they missed
- Keeps their area's taxonomy coherent

What it does not require: a PhD, industry seniority, or being the best engineer in the room. It
requires care and follow-through.

## Declared interests

None currently. Maintainers with a commercial or employment interest in a listed tool declare it
here, and do not raise that tool's verification tier themselves.

## Emeritus

None yet. Maintainers who step back are listed here rather than deleted — the contribution
happened.
