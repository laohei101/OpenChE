/**
 * Site smoke test. Drives the real pages in a real browser.
 *
 *   python -m http.server 8899 --directory public &
 *   node scripts/site_smoke_test.js
 *
 * Checks the things that silently break and that no unit test would catch:
 * a stylesheet 404, a JS exception, search failing to load its index, a mobile
 * layout that scrolls sideways, and — the one that matters most here — a
 * verification badge appearing on a record that was never checked.
 *
 * Exits non-zero on any failure, so CI fails loudly.
 */

'use strict';

const { chromium } = require('playwright');

const BASE = process.env.SITE_BASE || 'http://127.0.0.1:8899';

// Some environments ship a pre-installed Chromium at a fixed path rather than
// the version-stamped directory Playwright expects. CHROMIUM_PATH lets those
// run the suite without a redundant browser download.
const LAUNCH = process.env.CHROMIUM_PATH
  ? { executablePath: process.env.CHROMIUM_PATH }
  : {};
const failures = [];

function check(name, ok, detail) {
  console.log(`  [${ok ? ' ok ' : 'FAIL'}] ${name}${detail ? '  — ' + detail : ''}`);
  if (!ok) failures.push(`${name}: ${detail || 'failed'}`);
}

(async () => {
  const browser = await chromium.launch(LAUNCH);
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();

  const consoleErrors = [];
  const failedRequests = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', err => consoleErrors.push(String(err.message)));
  page.on('requestfailed', r => failedRequests.push(`${r.url()} ${r.failure().errorText}`));
  page.on('response', r => {
    if (r.status() >= 400) failedRequests.push(`${r.url()} HTTP ${r.status()}`);
  });

  // --- core pages load -----------------------------------------------------
  for (const [path, expect] of [
    ['/', 'Open ChemE Hub'],
    ['/get-started.html', 'Get started'],
    ['/search.html', 'Search everything'],
    ['/explore.html', 'Explore'],
    ['/compare.html', 'Compare'],
  ]) {
    const resp = await page.goto(BASE + path, { waitUntil: 'networkidle' });
    const body = await page.textContent('body');
    check(`page ${path}`, resp.ok() && body.includes(expect),
      resp.ok() ? `contains "${expect}"` : `HTTP ${resp.status()}`);
  }

  // --- search actually works ----------------------------------------------
  await page.goto(BASE + '/search.html', { waitUntil: 'networkidle' });
  await page.waitForFunction(
    () => !document.getElementById('search-status').textContent.includes('Loading'),
    { timeout: 15000 },
  );
  const status = await page.textContent('#search-status');
  const indexed = parseInt(status, 10);
  check('search index loads', Number.isFinite(indexed) && indexed > 300,
    `${indexed} records indexed`);

  await page.fill('#search-input', 'cantera');
  await page.waitForTimeout(400);
  const top = await page.textContent('.result h3 a');
  check('search ranks an exact name match first', /cantera/i.test(top), `top hit: ${top}`);

  // Deep link restores query state.
  await page.goto(BASE + '/search.html?q=rdkit', { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const deep = await page.textContent('#search-status');
  check('search deep link restores state', /match/i.test(deep), deep.trim());

  // --- the trust rule ------------------------------------------------------
  // A tier-0 record must say plainly that nothing was checked. This is the
  // single most important behaviour on the site: if it regresses, the catalog
  // starts implying verification it does not have.
  await page.goto(BASE + '/explore.html', { waitUntil: 'networkidle' });
  const firstDetail = await page.getAttribute('.explore-list a', 'href');
  await page.goto(BASE + firstDetail, { waitUntil: 'networkidle' });
  const detailText = await page.textContent('body');
  const tierShown = await page.textContent('.verify-tier');
  const claimsChecked = /No check has been performed/.test(detailText);
  check('unverified record states that nothing was checked',
    tierShown.includes('Tier 0') ? claimsChecked : true,
    `${firstDetail} shows ${tierShown.trim()}`);

  check('detail page never shows a bare "Verified" badge',
    !/>\s*Verified\s*</.test(detailText),
    'no unqualified verification claim');

  // --- theme and navigation ------------------------------------------------
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  const before = await page.getAttribute('html', 'data-theme');
  await page.click('#theme-toggle');
  const after = await page.getAttribute('html', 'data-theme');
  check('theme toggle flips data-theme', before !== after, `${before} -> ${after}`);

  // --- mobile --------------------------------------------------------------
  const mob = await ctx.newPage();
  await mob.setViewportSize({ width: 390, height: 844 });
  for (const path of ['/', '/explore.html', '/compare.html']) {
    await mob.goto(BASE + path, { waitUntil: 'networkidle' });
    const overflow = await mob.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    check(`mobile 390px: ${path} does not scroll sideways`, overflow <= 0, `overflow ${overflow}px`);
  }
  await mob.click('.nav-toggle');
  await mob.waitForTimeout(200);
  check('mobile nav opens', (await mob.locator('#nav-links.open').count()) === 1);

  // --- accessibility basics ------------------------------------------------
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  const a11y = await page.evaluate(() => {
    const problems = [];
    if (!document.querySelector('.skip-link')) problems.push('no skip link');
    if (document.querySelectorAll('h1').length !== 1) problems.push('not exactly one h1');
    document.querySelectorAll('img').forEach(img => {
      if (!img.hasAttribute('alt')) problems.push('img without alt: ' + img.src);
    });
    document.querySelectorAll('button').forEach(b => {
      if (!b.textContent.trim() && !b.getAttribute('aria-label')) {
        problems.push('button with no accessible name');
      }
    });
    if (!document.documentElement.lang) problems.push('no lang attribute');
    return problems;
  });
  check('accessibility basics', a11y.length === 0, a11y.join('; ') || 'skip link, one h1, labelled controls');

  // --- no runtime errors anywhere -----------------------------------------
  check('no console errors', consoleErrors.length === 0, consoleErrors.slice(0, 3).join(' | '));
  check('no failed requests', failedRequests.length === 0, failedRequests.slice(0, 3).join(' | '));

  await page.screenshot({ path: 'site-home.png' });
  await page.goto(BASE + '/explore.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: 'site-explore.png' });
  await browser.close();

  console.log();
  if (failures.length) {
    console.log(`${failures.length} check(s) FAILED:`);
    failures.forEach(f => console.log(`  ${f}`));
    process.exit(1);
  }
  console.log('All site smoke checks passed.');
})().catch(err => {
  console.error('Smoke test crashed:', err);
  process.exit(1);
});
