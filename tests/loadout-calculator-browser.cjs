/* Integration test: actual page markup, scripts, JSON and Web Worker served locally.
   npm install --no-save puppeteer-core (or set PUPPETEER_MODULE to its absolute module path).
   node --test tests/loadout-calculator-browser.cjs
   Optional: LOADOUT_PREVIEW_CSS=/absolute/path/to/compiled.css, LOADOUT_SCREENSHOT_DIR=...
*/
'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const puppeteer = require(process.env.PUPPETEER_MODULE || 'puppeteer-core');
const repo = path.resolve(__dirname, '..');
const mime = { '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.png': 'image/png' };
function pageHtml() {
  const md = fs.readFileSync(path.join(repo, 'content/loadout-calculator.md'), 'utf8');
  let body = md.slice(md.indexOf('<div class="vv lc"'), md.indexOf('<div class="vv-nojs"'));
  body = body.replace(/\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}/g, '$1')
    .replace(/\{\{\s*site\.time[^}]*\}\}/g, 'test');
  return '<!doctype html><html class="js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<title>Wardogs recoil optimizer preview</title><link rel="icon" href="data:,">' +
    (process.env.LOADOUT_PREVIEW_CSS ? '<link rel="stylesheet" href="/preview.css">' : '') +
    '</head><body><main class="main-content" style="padding:16px"><h1>Weapon Loadout Calculator</h1>' + body + '</main></body></html>';
}

test('calculator compares three recoil goals, applies a build, and shares it', { timeout: 180000 }, async () => {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    if (url.pathname === '/content/loadout-calculator.html') { res.setHeader('Content-Type', 'text/html'); res.end(pageHtml()); return; }
    const file = url.pathname === '/preview.css' ? process.env.LOADOUT_PREVIEW_CSS : path.resolve(repo, '.' + decodeURIComponent(url.pathname));
    if (!file || (url.pathname !== '/preview.css' && !file.startsWith(repo + path.sep)) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      res.writeHead(404); res.end('not found'); return;
    }
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const executablePath = process.env.BROWSER_EXECUTABLE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
  const profile = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'recoil-browser-'));
  let browser;
  try {
    browser = await puppeteer.launch({ executablePath, headless: true, userDataDir: profile, args: ['--no-first-run', '--no-default-browser-check', '--disable-extensions'] });
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.setViewport({ width: 1440, height: 1000 });
    await page.goto(origin + '/content/loadout-calculator.html#w=ID_AK74M&cls=Support&lvl=21');
    await page.waitForSelector('#lc.lc-ready');
    assert.equal(await page.$('#lc-recommendations') !== null, true, 'recoil comparison must exist above the manual editor');
    await page.waitForFunction(() => document.querySelectorAll('[data-recoil-goal]').length === 3 && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false', { timeout: 60000 });
    assert.deepEqual(await page.$$eval('[data-recoil-goal]', es => es.map(e => e.dataset.recoilGoal)), ['vertical', 'horizontal', 'overall']);
    assert.match(await page.$eval('#lc-recommendation-status', e => e.textContent), /combination/i);
    const before = await page.$eval('#lc-recommendations', e => e.textContent);
    assert.match(before, /Support/);
    assert.match(before, /Overall/);
    if (process.env.LOADOUT_PREVIEW_CSS) {
      assert.equal(await page.$eval('.lc-recoil-parts', e => getComputedStyle(e).display), 'block', 'theme definition-list grid must not scramble attachment rows');
      assert.equal(await page.$eval('.lc-recoil-metrics', e => getComputedStyle(e).display), 'block', 'metrics should align as a shared row layout');
    }
    // Remove progression cap and verify a real improvement is offered.
    await page.$eval('#lc-level', e => { e.value = ''; e.dispatchEvent(new Event('change', { bubbles: true })); });
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false' && !!document.querySelector('[data-recoil-goal="overall"] button:not(:disabled)'), { timeout: 60000 });
    // Keep an explicit optic and stance while applying a recoil recommendation.
    await page.select('#lc-slots select[data-key="Sight"]', 'ID_RedDot');
    await page.click('#lc-stance button[value="Crouch"]');
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false' && !!document.querySelector('[data-recoil-goal="overall"] button:not(:disabled)'), { timeout: 60000 });
    const expectedParts = await page.$$eval('[data-recoil-goal="overall"] .lc-recoil-parts > div', es => Object.fromEntries(es.map(e => [e.querySelector('dt').textContent, e.querySelector('dd').title || ''])));
    await page.click('[data-recoil-goal="overall"] button');
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false' && document.querySelector('[data-recoil-goal="overall"] button').disabled, { timeout: 60000 });
    assert.deepEqual(await page.$$eval('#lc-slots select[data-key]', es => Object.fromEntries(es.map(e => [e.dataset.key, e.value]))), expectedParts);
    assert.equal(await page.$eval('#lc-slots select[data-key="Sight"]', e => e.value), 'ID_RedDot');
    assert.equal(await page.$eval('#lc-stance button[aria-checked="true"]', e => e.value), 'Crouch');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'lc-recommendations-title');
    const hash = await page.evaluate(() => location.hash);
    assert.match(hash, /ID_AK74M/);
    assert.match(hash, /(?:Muzzle|Underbarrel|Magazine|Stock|Grip|Barrel)/);
    const table = await page.$eval('#lc-rows', e => e.textContent);
    await page.reload();
    await page.waitForFunction(() => document.querySelector('#lc.lc-ready') && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false', { timeout: 60000 });
    assert.equal(await page.$eval('#lc-rows', e => e.textContent), table, 'applied build survives a shared URL/reload');
    if (process.env.LOADOUT_SCREENSHOT_DIR) {
      fs.mkdirSync(process.env.LOADOUT_SCREENSHOT_DIR, { recursive: true });
      await page.screenshot({ path: path.join(process.env.LOADOUT_SCREENSHOT_DIR, 'calculator-unrestricted.png') });
    }
    // Class / level changes must discard stale results immediately.
    await page.select('#lc-slots select[data-key="Sight"]', '');
    await page.select('#lc-role', 'Support');
    await page.$eval('#lc-level', e => { e.value = '21'; e.dispatchEvent(new Event('change', { bubbles: true })); });
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false', { timeout: 60000 });
    assert.deepEqual(await page.evaluate(async () => {
      const extras = await (await fetch('/assets/data/loadout-extras.json')).json();
      return Array.from(document.querySelectorAll('.lc-recoil-parts dd[title]'), e => e.title).filter(id => {
        const u = extras.unlocks[id]; return u && !(u.Support && u.Support[0] <= 21);
      });
    }), [], 'recommendations must never retain locked parts from the previous build');
    for (const width of [1440, 390, 360]) {
      await page.setViewport({ width, height: 1000 });
      if (process.env.LOADOUT_PREVIEW_CSS) assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'styled page has no overflow at ' + width);
      if (process.env.LOADOUT_SCREENSHOT_DIR) {
        fs.mkdirSync(process.env.LOADOUT_SCREENSHOT_DIR, { recursive: true });
        await page.screenshot({ path: path.join(process.env.LOADOUT_SCREENSHOT_DIR, 'calculator-' + width + '.png'), fullPage: true });
      }
    }
    const weaponIds = await page.$$eval('#lc-weapon option', es => es.map(e => e.value));
    for (const id of weaponIds) {
      await page.evaluate(id => { location.hash = '#w=' + encodeURIComponent(id); }, id);
      await page.waitForFunction(id => document.querySelector('#lc-weapon').value === id && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false', { timeout: 10000 }, id);
      assert.ok(await page.$eval('#lc-recommendation-status', e => e.textContent.length > 0), 'explicit result or no-data state for ' + id);
    }
    assert.equal(weaponIds.length, 38, 'exercise every weapon in the current dataset');
    await page.evaluate(() => { location.hash = '#w=ID_M4'; });
    await page.waitForFunction(() => document.querySelector('#lc-weapon').value === 'ID_M4' && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    const m4Parts = await page.$$eval('[data-recoil-goal] .lc-recoil-parts', lists => lists.map(list => Object.fromEntries(Array.from(list.children, row => [row.querySelector('dt').textContent, row.querySelector('dd').title]))));
    assert.equal(m4Parts.length, 3);
    for (const parts of m4Parts) {
      assert.ok(parts['Barrel/Muzzle'], 'M4 shows its recommended muzzle');
      assert.ok(parts.Underbarrel, 'M4 shows its recommended foregrip');
      assert.notEqual(parts.Grip, 'ID_AR_02_GRP_05');
    }
    assert.match(await page.$eval('#lc-recommendation-status', e => e.textContent), /zero-recoil override/i);
    await page.click('[data-recoil-goal="overall"] button');
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    assert.equal(await page.$eval('#lc-slots select[data-key="Barrel/Muzzle"]', e => e.value), m4Parts[2]['Barrel/Muzzle']);
    assert.equal(await page.$eval('#lc-slots select[data-key="Underbarrel"]', e => e.value), m4Parts[2].Underbarrel);
    // Applying a build must not silently rewrite an unfolded/mounted setting.
    await page.evaluate(() => { location.hash = '#w=ID_AK74M'; });
    await page.waitForFunction(() => document.querySelector('#lc-weapon').value === 'ID_AK74M' && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    await page.select('#lc-slots select[data-key="Underbarrel"]', 'ID_FGP_04');
    await page.click('#lc-bipod button[value="unfolded"]');
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false' && !!document.querySelector('[data-recoil-goal="overall"] button:not(:disabled)'));
    await page.click('[data-recoil-goal="overall"] button');
    await page.waitForFunction(() => document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    assert.equal(await page.$eval('#lc-bipod button[aria-checked="true"]', e => e.value), 'unfolded');
    assert.match(await page.evaluate(() => location.hash), /bipod=unfolded/);
    // Failure states must not strand the page in an infinite loading state.
    await page.evaluateOnNewDocument(() => { window.Worker = undefined; });
    await page.reload();
    await page.waitForFunction(() => document.querySelector('#lc.lc-ready') && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    assert.match(await page.$eval('#lc-recommendation-status', e => e.textContent), /Workers are unavailable/);
    await page.click('#lc-stance button[value="Crouch"]');
    assert.equal(await page.$eval('#lc-stance button[aria-checked="true"]', e => e.value), 'Crouch');
    await page.setRequestInterception(true);
    page.on('request', request => {
      if (request.url().includes('/assets/data/loadout-extras.json')) request.respond({ status: 503, body: 'unavailable' });
      else request.continue();
    });
    await page.reload();
    await page.waitForFunction(() => document.querySelector('#lc.lc-ready') && document.querySelector('#lc-recommendations').getAttribute('aria-busy') === 'false');
    assert.match(await page.$eval('#lc-recommendation-status', e => e.textContent), /Unlock data could not be loaded/);
    assert.equal(await page.$$eval('[data-recoil-goal]', es => es.length), 0);
    assert.deepEqual(errors, [], 'no runtime errors');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 250 });
  }
});
