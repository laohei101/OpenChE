/* =========================================================================
 * Client-side search over the Open ChemE Hub resource index.
 *
 * No dependencies, no build step, no network calls beyond fetching the index.
 * Matching is a weighted token score rather than fuzzy similarity: for a few
 * hundred records, requiring every typed token to appear somewhere gives more
 * predictable results than a similarity threshold somebody has to tune.
 *
 * Licence: MIT
 * ========================================================================= */

(function () {
  'use strict';

  var input = document.getElementById('search-input');
  if (!input) return; // not on the search page

  var resultsEl = document.getElementById('search-results');
  var statusEl = document.getElementById('search-status');
  var clearBtn = document.getElementById('search-clear');
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll('.filter'));

  var index = [];
  var activeFilter = 'all';
  var MAX_RESULTS = 60;

  // ---------------------------------------------------------------------
  // Load the index
  // ---------------------------------------------------------------------

  // Resolve relative to this script so the page works under any baseurl —
  // a project site served from /hub-website/ would 404 on an absolute path.
  var scriptSrc = document.currentScript ? document.currentScript.src
    : (function () {
        var scripts = document.getElementsByTagName('script');
        return scripts[scripts.length - 1].src;
      })();
  var indexUrl = scriptSrc.replace(/assets\/js\/search\.js.*$/, 'assets/data/resources.json');

  fetch(indexUrl)
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      index = Array.isArray(data) ? data : (data.resources || []);
      setStatus(index.length + ' resources indexed. Type to search.');
      input.disabled = false;
      // Support deep links like /search/?q=cantera
      var params = new URLSearchParams(window.location.search);
      var q = params.get('q');
      if (q) {
        input.value = q;
        run();
      }
    })
    .catch(function (err) {
      setStatus(
        'Could not load the search index (' + err.message + '). ' +
        'The lists themselves are on GitHub and are plain Markdown — ' +
        "your browser's find-in-page works on them."
      );
      input.disabled = true;
    });

  // ---------------------------------------------------------------------
  // Scoring
  // ---------------------------------------------------------------------

  function tokenise(text) {
    return String(text || '')
      .toLowerCase()
      .split(/[^a-z0-9+#.]+/)
      .filter(Boolean);
  }

  /**
   * Score one record against the query tokens.
   * Returns 0 when any token is absent — every token must match somewhere.
   */
  function score(record, tokens) {
    var name = (record.name || '').toLowerCase();
    var desc = (record.description || '').toLowerCase();
    var section = (record.section || '').toLowerCase();
    var tags = (record.tags || []).join(' ').toLowerCase();
    var category = (record.category || '').toLowerCase();
    var haystack = name + ' ' + desc + ' ' + section + ' ' + tags + ' ' + category;

    var total = 0;

    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (haystack.indexOf(t) === -1) return 0;

      // Weights, most specific first. An exact name match should always beat
      // a passing mention in a description.
      if (name === t) total += 100;
      else if (name.indexOf(t) === 0) total += 50;
      else if (name.indexOf(t) !== -1) total += 30;

      if (tags.split(' ').indexOf(t) !== -1) total += 20;
      else if (tags.indexOf(t) !== -1) total += 10;

      if (section.indexOf(t) !== -1) total += 8;
      if (desc.indexOf(t) !== -1) total += 5;
      if (category.indexOf(t) !== -1) total += 3;
    }

    // Small nudge for shorter names, so "thermo" ranks the library above a
    // record that merely mentions thermodynamics at length.
    total += Math.max(0, 20 - name.length) / 10;

    return total;
  }

  // ---------------------------------------------------------------------
  // Rendering
  // ---------------------------------------------------------------------

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /** Highlight query tokens in already-escaped text. */
  function highlight(escaped, tokens) {
    if (!tokens.length) return escaped;
    var pattern = tokens
      .map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); })
      .sort(function (a, b) { return b.length - a.length; })
      .join('|');
    return escaped.replace(new RegExp('(' + pattern + ')', 'gi'), '<mark>$1</mark>');
  }

  function categoryLabel(cat) {
    return String(cat || '')
      .split('-')
      .map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); })
      .join(' ');
  }

  function render(matches, tokens) {
    if (!matches.length) {
      resultsEl.innerHTML =
        '<div class="no-results">' +
        '<p><strong>Nothing matched.</strong></p>' +
        '<p>Every word you type has to appear somewhere in the record, so a typo in ' +
        'one word hides everything. Try fewer words, or a broader one — ' +
        '<code>thermodynamics</code> rather than <code>thermophysical properties library</code>.</p>' +
        '<p>Certain the tool should be here? ' +
        '<a href="https://github.com/open-cheme-hub/.github/issues/new?template=add_resource.yml">' +
        'Suggest it</a> — that is how the lists grow.</p>' +
        '</div>';
      return;
    }

    var html = matches.slice(0, MAX_RESULTS).map(function (r) {
      var tags = (r.tags || []).map(function (t) {
        return '<li class="tag tag-sm">' + escapeHtml(t) + '</li>';
      }).join('');

      return '' +
        '<article class="result">' +
          '<div class="result-head">' +
            '<h3><a href="' + escapeHtml(r.url) + '" rel="noopener">' +
              highlight(escapeHtml(r.name), tokens) +
            '</a></h3>' +
            '<span class="result-cat cat-' + escapeHtml(r.category) + '">' +
              escapeHtml(categoryLabel(r.category)) +
            '</span>' +
          '</div>' +
          '<p class="result-desc">' + highlight(escapeHtml(r.description), tokens) + '</p>' +
          '<div class="result-meta">' +
            (r.section ? '<span class="result-section">' + escapeHtml(r.section) + '</span>' : '') +
            (tags ? '<ul class="tag-row">' + tags + '</ul>' : '') +
          '</div>' +
        '</article>';
    }).join('');

    resultsEl.innerHTML = html;
  }

  function setStatus(msg) {
    if (statusEl) statusEl.textContent = msg;
  }

  // ---------------------------------------------------------------------
  // Query handling
  // ---------------------------------------------------------------------

  function run() {
    var query = input.value.trim();
    var tokens = tokenise(query);

    var pool = activeFilter === 'all'
      ? index
      : index.filter(function (r) { return r.category === activeFilter; });

    if (!tokens.length) {
      // Empty query: show the pool alphabetically rather than nothing, so the
      // filter buttons are useful on their own.
      var listed = pool.slice().sort(function (a, b) {
        return a.name.localeCompare(b.name);
      });
      setStatus(
        pool.length + ' resource' + (pool.length === 1 ? '' : 's') +
        (activeFilter === 'all' ? '' : ' in ' + categoryLabel(activeFilter)) +
        (listed.length > MAX_RESULTS ? ' — showing the first ' + MAX_RESULTS : '')
      );
      render(listed, []);
      return;
    }

    var scored = [];
    for (var i = 0; i < pool.length; i++) {
      var s = score(pool[i], tokens);
      if (s > 0) scored.push({ record: pool[i], score: s });
    }
    scored.sort(function (a, b) {
      return b.score - a.score || a.record.name.localeCompare(b.record.name);
    });

    var matches = scored.map(function (x) { return x.record; });
    setStatus(
      matches.length + ' match' + (matches.length === 1 ? '' : 'es') +
      ' for "' + query + '"' +
      (activeFilter === 'all' ? '' : ' in ' + categoryLabel(activeFilter)) +
      (matches.length > MAX_RESULTS ? ' — showing the top ' + MAX_RESULTS : '')
    );
    render(matches, tokens);
  }

  // Debounce: typing is faster than rendering 60 cards.
  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 120);
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      input.value = '';
      run();
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      input.value = '';
      input.focus();
      run();
    });
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      activeFilter = btn.dataset.filter;
      run();
    });
  });

  // "/" focuses the search box, as long as the user isn't already typing.
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    if (e.key === '/' && tag !== 'input' && tag !== 'textarea') {
      e.preventDefault();
      input.focus();
    }
  });
})();
