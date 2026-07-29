# `.github` — Open ChemE Hub community health files

This repository holds the files GitHub applies across **every** repository in the
[Open ChemE Hub](https://github.com/open-cheme-hub) organisation. Editing a file here changes the
default behaviour for all of our repositories at once.

## Layout

```
.
├── profile/
│   └── README.md              # Rendered on the organisation's public page
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── config.yml         # Issue chooser: routes questions to Discussions
│   │   ├── add_resource.yml   # Structured form for proposing a new list entry
│   │   ├── broken_link.yml    # Report a dead or moved link
│   │   └── bug_report.yml     # Something in templates/ or workflows/ is broken
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md            # Applies to every repo without its own
├── CODE_OF_CONDUCT.md         # Contributor Covenant v2.1
├── SECURITY.md                # How to report a vulnerability
├── SUPPORT.md                 # Where to ask for help
└── LICENSE                    # CC BY 4.0 for prose, MIT for code (see file)
```

## How the defaults work

GitHub falls back to this repository whenever an individual repo doesn't define its own copy:

- **`profile/README.md`** is special — it renders on <https://github.com/open-cheme-hub>. Nothing
  else in this repo does that.
- **`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`** are inherited by all
  repos. A repo that needs different rules (for example, a list with unusual entry criteria) adds
  its own file and that one wins.
- **`.github/ISSUE_TEMPLATE/`** and **`.github/PULL_REQUEST_TEMPLATE.md`** are likewise inherited.

Note the nesting: community health files live at the repository root, while issue and PR templates
live under `.github/`. That is a GitHub convention, not a mistake.

## Changing something here

Changes here affect contributors in eight other repositories, so:

1. Open an issue or a Discussion describing the problem before writing the PR — process changes
   benefit from disagreement early rather than late.
2. Keep the code of conduct textually identical to upstream Contributor Covenant v2.1 except for
   the contact address. Divergence makes it harder for people to know what they've agreed to.
3. When you change an issue form, open a test issue in a scratch repo first. A malformed
   `.yml` silently disables the form for everyone.

## Contact

Conduct reports and security disclosures: **conduct@open-cheme-hub.org** /
**security@open-cheme-hub.org** (update these in your fork — see `setup_github.sh` notes).
Everything else: [Discussions](https://github.com/orgs/open-cheme-hub/discussions).
