# Security Policy

## Scope

Open ChemE Hub publishes documentation, curated links, templates, and workflow definitions. We
don't run a service, and we don't handle user data. The realistic risks are therefore:

- **Malicious code in a template, workflow, or Docker image** we ship.
- **A link in one of our lists that now points somewhere harmful** — domain expired and was
  re-registered, project repo taken over, installer replaced.
- **A supply-chain issue in a pinned dependency** of `workflows/docker` or a Snakemake environment.
- **A GitHub Actions workflow** in this organisation that could be abused (for example, script
  injection through an untrusted PR title into a `run:` block).

## Reporting

Email **yu.dai@mail.utoronto.ca**, or use GitHub's private vulnerability reporting on the
affected repository (Security → Report a vulnerability).

Please include:

- Which repository and file.
- What an attacker can do, concretely.
- Steps to reproduce, if there's something to run.
- Whether you've told anyone else, and any disclosure deadline you're working to.

**Don't open a public issue for a hijacked-link or malicious-code report.** Do open a public issue
for a link that's merely dead — that's a broken link, not a security problem.

## What to expect

| | Target |
| --- | --- |
| Acknowledgement | 3 working days |
| Initial assessment | 10 working days |
| Fix or removal for a confirmed high-severity issue | 30 days |

For a hijacked or malicious link, we remove the entry immediately on credible evidence and
investigate afterwards. Removing a link costs nothing; leaving it up while we deliberate could cost
a reader a compromised machine.

We'll credit you in the commit or release notes unless you'd rather we didn't. We have no bug
bounty — this is a volunteer project.

## For contributors

- Never commit credentials, API keys, licence files, or institutional server paths.
- Pin dependencies by version in `environment.yaml` and Docker images; `latest` is not a version.
- In GitHub Actions, pass untrusted input (issue titles, PR bodies, branch names) through `env:`
  variables rather than interpolating `${{ }}` directly into `run:` blocks.
- Third-party actions should be pinned to a full commit SHA, not a moving tag.
