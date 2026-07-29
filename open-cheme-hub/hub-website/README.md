# hub-website

**The static site at [open-cheme-hub.github.io](https://open-cheme-hub.github.io) — entry point,
orientation, and search across every list.**

Jekyll, served by GitHub Pages from the `docs/` folder. No build step of our own, no npm, no
theme gem. Editing a Markdown file and pushing is the whole deployment process.

---

## Layout

```
hub-website/
├── README.md              # this file
├── build_index.py         # regenerates the search index from a compact source list
└── docs/                  # everything GitHub Pages serves
    ├── _config.yml        # site settings, navigation, and the list/tool card data
    ├── index.md           # homepage (uses the `home` layout)
    ├── get-started.md     # three paths: students, researchers, industry
    ├── search.md          # client-side search page
    ├── Gemfile            # local preview only; Pages ignores it
    ├── _layouts/
    │   ├── default.html   # shell: header, footer, theme toggle, mobile nav
    │   └── home.html      # homepage sections, built from _config.yml data
    └── assets/
        ├── css/style.css  # hand-written, ~700 lines, light and dark
        ├── js/search.js   # dependency-free weighted token search
        └── data/resources.json   # the search index
```

## Local preview

```bash
cd docs
bundle install                            # first time only
bundle exec jekyll serve --livereload
# http://localhost:4000
```

The `github-pages` gem pins Jekyll and every plugin to exactly what GitHub Pages runs, so a
local build and the deployed build agree. Installing a newer standalone Jekyll is the usual
reason a site works locally and renders differently in production.

No Ruby? Most changes can be checked without it — `assets/css/style.css` and
`assets/js/search.js` are plain files, and the Markdown pages render close enough in any
previewer. Only Liquid template changes really need a local build.

## Deploying

**Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/docs`.**

Then set `url` and `baseurl` in `_config.yml` for where it actually lives:

| Deployment | `url` | `baseurl` |
| --- | --- | --- |
| Org site at `open-cheme-hub.github.io` | `https://open-cheme-hub.github.io` | `""` |
| Project site at `user.github.io/hub-website` | `https://user.github.io` | `/hub-website` |
| Custom domain | `https://yourdomain.org` | `""` |

Getting `baseurl` wrong is the single most common Pages problem: the page renders but every
stylesheet, script, and internal link 404s. Every URL in the layouts goes through
`relative_url` so that one setting fixes all of them at once, and `search.js` resolves the
index path relative to its own `src` for the same reason.

For a custom domain, add a `CNAME` file containing the bare domain to `docs/`.

## Adding or changing content

### A new page

Create `docs/whatever.md` with front matter:

```yaml
---
layout: default
title: Whatever
permalink: /whatever/
description: One sentence — this becomes the meta description and the search snippet.
---
```

Add it to the `nav:` list in `_config.yml` if it belongs in the header.

### A new list or tool card

Both homepage card rows are generated from `_config.yml`. Add an entry under `lists:` or
`tools:` and the card, the footer link, and the search filter follow. Nothing in the HTML
needs touching.

### The search index

`docs/assets/data/resources.json` is the site's own copy of the lists — about 200 of the most
reached-for entries out of the 460-odd across all five. Regenerate it with:

```bash
python3 build_index.py
```

Entries live in `build_index.py` as one-line tuples, `(name, url, description, section, tags)`,
which keeps adding a resource to one line instead of six and validates for duplicates and
malformed URLs on the way out. Editing the JSON by hand works too — just keep it valid, because
a trailing comma silently breaks search for everyone.

If you add a resource to a list and want it searchable immediately, add it here in the same
pull request. Otherwise the next index refresh picks it up.

## How the search works

Loading `resources.json` and scoring in the browser. Roughly 60 KB of JSON, no server, no
tracking, and it keeps working offline once the page has loaded.

Matching is a **weighted token score**, not fuzzy similarity: every token you type must appear
somewhere in the record, and matches score higher in the name than in tags, higher in tags than
in the description. For a few hundred records this gives more predictable results than a
similarity threshold somebody would have to tune, and it never surfaces a confusing
near-miss.

Also implemented: category filters, deep links (`/search/?q=cantera`), `/` to focus the box,
`Escape` to clear, and a `<noscript>` fallback pointing at the Markdown lists, which your
browser's own find-in-page handles perfectly well.

## Design notes

**Hand-written CSS, ~700 lines.** A framework would be more code, not less, for six pages. The
whole palette is CSS custom properties, so re-theming means editing about twenty lines at the
top of `style.css`.

**Dark mode is first-class.** The theme comes from `prefers-color-scheme`, is overridable with
the header toggle, persists in `localStorage`, and is applied in a tiny inline script before
first paint so dark-mode readers never get a white flash.

**Accessibility.** Skip link, visible focus rings, `aria-current` on the active nav item,
live-region status on search results, and `prefers-reduced-motion` respected. Colour contrast
meets WCAG AA in both themes.

**No external requests.** No CDN, no web fonts, no analytics. System font stack, emoji favicon
as an inline SVG data URI. The site loads fast on conference wifi, which is where people
actually open it.

**Wide content scrolls itself.** Tables and code blocks get their own `overflow-x`, so the page
body never scrolls sideways on a phone.

## Contributing

See the [organisation contributing guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md).
Copy edits and clarifications are always welcome — this site's job is to get someone from
"a colleague mentioned this" to "I have something running" as fast as possible, and if any page
here fails at that, say so in an issue.

## Licence

Prose under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the layouts, CSS, and
JavaScript under MIT.
