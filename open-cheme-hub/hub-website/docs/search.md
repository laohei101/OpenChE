---
layout: default
title: Search
permalink: /search/
description: >-
  Client-side search across every curated resource in the Open ChemE Hub lists —
  tools, databases, textbooks, courses, and templates.
---

<div class="page-header">
  <div class="container narrow">
    <h1>Search everything</h1>
    <p class="lede">
      One box across all five lists plus the templates and workflows. Runs entirely in your
      browser against a JSON index — no server, no tracking, works offline once the page has
      loaded. The index covers around 200 of the most-reached-for entries; the lists themselves
      are the complete set.
    </p>
  </div>
</div>

<div class="container">

  <div class="search-panel">
    <div class="search-box">
      <label class="visually-hidden" for="search-input">Search resources</label>
      <input type="search" id="search-input" autocomplete="off" spellcheck="false"
             placeholder="Try: thermodynamics, RDKit, free textbook, python, HAZOP…"
             aria-describedby="search-status">
      <button id="search-clear" type="button" aria-label="Clear search">×</button>
    </div>

    <div class="filter-row" role="group" aria-label="Filter by category">
      <button class="filter active" data-filter="all">All</button>
      <button class="filter" data-filter="chemical-engineering">Chemical Eng</button>
      <button class="filter" data-filter="chemoinformatics">Chemoinformatics</button>
      <button class="filter" data-filter="bioengineering">Bioengineering</button>
      <button class="filter" data-filter="medical-engineering">Medical Eng</button>
      <button class="filter" data-filter="general-engineering">General Eng</button>
      <button class="filter" data-filter="templates">Templates</button>
      <button class="filter" data-filter="workflows">Workflows</button>
    </div>

    <p id="search-status" class="search-status" role="status" aria-live="polite">
      Loading the index…
    </p>
  </div>

  <div id="search-results" class="search-results"></div>

  <noscript>
    <div class="callout callout-warning">
      <p>
        <strong>Search needs JavaScript.</strong> The index is a static JSON file and the
        matching happens in your browser, so there is no server-side fallback. You can browse
        the lists directly on GitHub instead — every one of them is a single Markdown file
        that your browser's own find-in-page will search:
      </p>
      <ul>
        {%- for list in site.lists %}
        <li><a href="{{ site.org_url }}/{{ list.repo }}">{{ list.name }}</a></li>
        {%- endfor %}
      </ul>
    </div>
  </noscript>

  <section class="search-help">
    <h2>How this works</h2>
    <p>
      <code>assets/data/resources.json</code> is the site's own copy of the lists. Matching is a
      simple weighted token score — name matches rank above description matches, and every token
      you type must appear somewhere in the record. It is deliberately not a fuzzy search: for a
      few hundred records, exact substring matching gives more predictable results than a
      similarity threshold anyone would have to tune.
    </p>
    <p>
      The index is regenerated when the lists change. If you add a resource and want it
      searchable immediately, add the matching JSON entry in the same pull request — and keep
      the JSON valid, because a trailing comma breaks search for everyone.
    </p>
    <p>
      Everything indexed here also lives in a plain Markdown file on GitHub. If the search is
      ever wrong, the list is the source of truth.
    </p>
  </section>

</div>
