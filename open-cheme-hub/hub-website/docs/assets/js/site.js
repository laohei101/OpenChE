/* =========================================================================
 * Shared site behaviour: theme toggle and mobile navigation.
 *
 * Loaded on every page. The initial theme is applied by a tiny inline script
 * in <head> instead, so it lands before first paint and dark-mode readers
 * never see a white flash — this file only handles the toggle afterwards.
 *
 * Licence: MIT
 * ========================================================================= */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // --- Theme toggle -----------------------------------------------------
    var toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.dataset.theme = next;
        // Private browsing can throw on write; the toggle should still work.
        try { localStorage.setItem('theme', next); } catch (e) {}
      });
    }

    // --- Mobile navigation ------------------------------------------------
    var navToggle = document.querySelector('.nav-toggle');
    var navLinks = document.getElementById('nav-links');
    if (navToggle && navLinks) {
      navToggle.addEventListener('click', function () {
        var open = navLinks.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', String(open));
      });

      // Close the menu on outside click, so it doesn't sit over the content.
      document.addEventListener('click', function (e) {
        if (!navLinks.classList.contains('open')) return;
        if (navLinks.contains(e.target) || navToggle.contains(e.target)) return;
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    }
  });
})();
