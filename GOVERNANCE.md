# Governance

Small project, light process. This describes how decisions are actually made, so that when it
grows the rules were written before they were needed rather than after an argument.

---

## Roles

**Contributor** — anyone who opens an issue or a pull request. No application, no permission
needed.

**Area maintainer** — reviews and merges within one area (see [MAINTAINERS.md](MAINTAINERS.md)).
Appointed by the project lead after a track record of good review, not by seniority or
credentials.

**Project lead** — resolves disagreements that stalled, sets direction, appoints maintainers.
Currently Kevin Dai (yu.dai@mail.utoronto.ca). This is a benevolent-dictator model, which is
honest for a project of this size; it should become a maintainer council if the project outgrows
one person's attention.

## Decisions

| Change | Needs |
| --- | --- |
| Fix a typo, a link, or a description | One approval. Merged on sight. |
| Add or edit a catalog record | One approval from any maintainer |
| Promote a verification tier | One approval **plus** the evidence in the record |
| New template or workflow | One approval plus evidence the test case runs |
| Schema change | Two maintainers — every record and generator depends on it |
| Taxonomy change | Two maintainers, and the PR must reassign existing records |
| Governance, licence, or code of conduct | Project lead, after a Discussion |
| Removing a resource | One approval, with the reason recorded in the PR |

Disagreement resolves by discussion first. If it stalls for a week, the project lead decides and
records why.

## Conflicts of interest

**Affiliation is fine. Concealing it is not.**

- Adding your own project is welcome. Say so in the PR description and set
  `affiliation_disclosure` in the record.
- Do not approve your own record. Anyone else may.
- Do not raise the verification tier of a project you maintain. Someone independent does that.
- Maintainers with a commercial interest in a listed tool declare it in MAINTAINERS.md.

The bar for your own project is the same as anyone else's: documentation, a licence, and an
example that runs.

## Verification integrity

Verification claims are the reason this project exists, so they carry the strictest rules:

- A tier above 0 requires dated evidence. The schema enforces it; the validator enforces it again.
- Claiming tier 2 while recording `spdx: UNKNOWN` is rejected automatically — you cannot say you
  confirmed the licence and that you don't know it.
- A verification claim found to be wrong is reverted to tier 0 the same day, with the reason
  recorded. No quiet edits.
- Repeatedly submitting unverifiable claims loses commit access. This is the one thing that would
  make the catalog worthless.

## Releases

Calendar versioned, `YYYY.MM`, cut when there is something worth tagging. Each release records
the record count, the tier distribution, and every schema change. A schema change is a breaking
change and says so.

## Deprecation

- An archived upstream project stays listed with `maintenance_status: archived`, its limitations
  recorded, and a pointer to a successor where one exists. Removing it loses the information that
  it existed and stopped.
- A removed record leaves a redirect from its detail page for at least one release.
- A retired script moves to `tools/legacy/` with a note, rather than being deleted.

## Code of Conduct

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), Contributor Covenant 2.1. Reports go to
yu.dai@mail.utoronto.ca and are handled by the project lead. Where the report concerns the
project lead, ask any area maintainer to handle it instead.

## Amending this document

Open a Discussion, then a pull request. The project lead decides. Changes are announced in the
release notes, because a governance change nobody noticed is not governance.
