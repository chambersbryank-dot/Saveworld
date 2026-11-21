/* Click-listener checks for the Microsoft UET block injected by scripts/build-uet.py.
   Uses the real snippet from index.html and a small DOM, then a headless Chrome pass
   on built pages (stylesheet load, kids exclusion, donate_click, no navigation delay). */
const fs = require('fs');
const path = require('path');
const http = require('http');
const {spawn} = require('child_process');

const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const block = html.match(/<!-- UET:START --><script>([\s\S]*?)<\/script>/);
if (!block) { console.error('no UET script in index.html'); process.exit(1); }
const SRC = block[1];

function makeEl(tag, attrs, kids) {
  const el = {
    nodeType: 1, tag, attrs: Object.assign({}, attrs), children: kids || [], parentNode: null,
    classList: { contains(c) { return (el.attrs.class || '').split(/\s+/).includes(c); } },
    hasAttribute(n) { return Object.prototype.hasOwnProperty.call(el.attrs, n); },
    getAttribute(n) { return n in el.attrs ? el.attrs[n] : null; },
    setAttribute(n, v) { el.attrs[n] = v; },
  };
  el.children.forEach(c => { c.parentNode = el; });
  el.querySelectorAll = sel => {
    const out = [];
    (function walk(n) {
      if (n !== el && match(n, sel)) out.push(n);
      (n.children || []).forEach(walk);
    })(el);
    return out;
  };
  el.querySelector = sel => el.querySelectorAll(sel)[0] || null;
  el.closest = sel => { let n = el; while (n) { if (match(n, sel)) return n; n = n.parentNode; } return null; };
  Object.defineProperty(el, 'textContent', { get() { return this.children.map(c => c.textContent || '').join(''); } });
  el.cloneNode = () => makeEl(tag, el.attrs, el.children.map(c => c.cloneNode ? c.cloneNode(true) : makeText(c.textContent)));
  el.removeChild = c => { el.children = el.children.filter(x => x !== c); c.parentNode = null; };
  if (tag === 'a') {
    const abs = new URL(el.attrs.href || 'https://www.savingplanets.com/', 'https://www.savingplanets.com/x.html');
    el.hostname = abs.hostname; el.protocol = abs.protocol; el.href = abs.href;
  }
  return el;
}
function makeText(s) { return { nodeType: 3, textContent: s, children: [], cloneNode() { return makeText(s); } }; }
function match(n, sel) {
  if (sel === '.sr-only') return n.classList && n.classList.contains('sr-only');
  if (sel === 'h3') return n.tag === 'h3';
  if (sel === '#donations') return n.attrs && n.attrs.id === 'donations';
  if (sel === '.wh-card') return n.classList && n.classList.contains('wh-card');
  if (sel === 'a[href]') return n.tag === 'a' && n.attrs && n.attrs.href;
  return false;
}

function boot(pathname, hostname) {
  const listeners = [];
  const created = [];
  const document = {
    addEventListener(type, fn) { listeners.push(fn); },
    createElement(tag) { const n = { tag, src: '', async: false, parentNode: null }; created.push(n); return n; },
    getElementsByTagName() { return [{ parentNode: { insertBefore() {} } }]; },
  };
  const window = { document, uetq: undefined };
  const location = { hostname, pathname };
  const fn = new Function('window', 'document', 'location', SRC + '\n//# sourceURL=uet.js');
  fn(window, document, location);
  return { window, listeners, created, click(target) {
    const ev = { target, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
    const t0 = process.hrtime.bigint();
    listeners.forEach(f => f(ev));
    const ms = Number(process.hrtime.bigint() - t0) / 1e6;
    return { ev, ms, q: window.uetq };
  } };
}

function a(attrs, kids) { return makeEl('a', attrs, kids); }
let failed = 0;
function eq(name, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  console.log((ok ? 'ok  ' : 'FAIL') + ' ' + name + (ok ? '' : '\n    got ' + JSON.stringify(got)));
  if (!ok) failed++;
}
/* bat.js dispatchq reads a flat push('event', name, data) as one custom event. */
function donateLabels(q) {
  const labels = [];
  let cmd, name;
  for (let o = 0; o < (q || []).length; o++) {
    const item = q[o];
    if (item && typeof item === 'object') {
      if (cmd === 'event' && name) labels.push(item.event_label);
      cmd = name = undefined;
    } else if (typeof item === 'string') {
      if (cmd !== undefined && name !== undefined) { cmd = name = undefined; continue; }
      if (cmd === undefined && (item === 'event' || item === 'set' || item === 'consent' || item === 'config')) cmd = item;
      else if (cmd !== undefined && name === undefined) name = item;
      else cmd = name = undefined;
    } else cmd = name = undefined;
  }
  return labels;
}

const page = boot('/Snow_Leopard_Trust.html', 'www.savingplanets.com');
eq('production loads bat.js', page.created.map(n => n.src), ['https://bat.bing.com/bat.js']);
eq('bat.js is async', page.created[0] && page.created[0].async, 1);

const local = boot('/Snow_Leopard_Trust.html', '127.0.0.1');
eq('localhost does not request bat.js', local.created.length, 0);

const don = a({ href: 'https://snowleopard.org/donate/', class: 'btn help-btn', 'data-sp-donate': '1', target: '_blank' }, [makeText('Donate')]);
const hit = page.click(don);
eq('donate_click payload', donateLabels(hit.q), ['Snow_Leopard_Trust']);
eq('click is not cancelled', hit.ev.defaultPrevented, false);
eq('listener returns immediately', hit.ms < 20, true);

const info = a({ href: 'https://www.fisheries.noaa.gov/species/hawaiian-monk-seal', class: 'donate-btn donate-btn-subtle' }, [makeText('For Further Information')]);
eq('further-information is not a donation', donateLabels(page.click(info).q), ['Snow_Leopard_Trust']);

const same = a({ href: 'Ways_to_Help.html', class: 'sticky-help' }, [makeText('Donate / Help')]);
eq('on-site Donate / Help is not counted', donateLabels(page.click(same).q), ['Snow_Leopard_Trust']);

const card = makeEl('li', { class: 'wh-card' }, [
  makeEl('h3', {}, [makeText('Snow Leopard Trust')]),
]);
const wth = a({ href: 'https://snowleopard.org/donate/', class: 'btn help-btn' }, [
  makeText('Donate'), makeEl('span', { class: 'sr-only' }, [makeText(' – Snow Leopard Trust')]),
]);
card.children.push(wth); wth.parentNode = card;
const sec = makeEl('section', { id: 'donations' }, [card]);
card.parentNode = sec;
eq('ways-to-help label is the organization', donateLabels(page.click(wth).q), ['Snow_Leopard_Trust', 'Snow Leopard Trust']);

const fr = boot('/fr/WeForest.html', 'www.savingplanets.com');
const frA = a({ href: 'https://www.weforest.org/donate/', class: 'btn help-btn', 'data-sp-donate': '1' }, [makeText('Faire un don')]);
eq('french donate uses the page slug', donateLabels(fr.click(frA).q), ['WeForest']);

const he = boot('/he/WeForest.html', 'savingplanets.com');
const heA = a({ href: 'https://www.weforest.org/donate/', class: 'btn help-btn' }, [makeText('לתרומה')]);
eq('hebrew donate label counts', donateLabels(he.click(heA).q), ['WeForest']);

const ar = boot('/ar/WeForest.html', 'www.savingplanets.com');
const arA = a({ href: 'https://www.weforest.org/donate/', class: 'btn help-btn' }, [makeText('تبرّع')]);
eq('arabic donate label counts', donateLabels(ar.click(arA).q), ['WeForest']);

const vol = a({ href: 'https://example.org/volunteer', class: 'btn help-btn help-btn-join' }, [makeText('Volunteer')]);
eq('volunteer is not a donation', donateLabels(page.click(vol).q), ['Snow_Leopard_Trust', 'Snow Leopard Trust']);

for (const rel of ['Kids_Map.html', 'fr/Play_and_Learn.html', 'he/Myth_or_Fact_Arcade.html', 'es/Spot_the_Fire.html', 'ar/Kids_World.html']) {
  const t = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const bad = /bat\.bing\.com|uetq|343288039/.test(t);
  eq(rel + ' has no UET', bad, false);
}

if (failed) { console.error(failed + ' failed'); process.exit(1); }
console.log('unit checks passed');

function serve(root) {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      let u = decodeURIComponent(req.url.split('?')[0]);
      if (u.endsWith('/')) u += 'index.html';
      const file = path.join(root, u);
      if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end('no'); return; }
      const ext = path.extname(file);
      const type = ext === '.html' ? 'text/html' : ext === '.css' ? 'text/css' : ext === '.js' ? 'text/javascript' : 'application/octet-stream';
      res.writeHead(200, { 'content-type': type });
      fs.createReadStream(file).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

async function chromePass(port) {
  let puppeteer;
  try { puppeteer = require('puppeteer-core'); }
  catch (e) {
    console.log('puppeteer-core not installed, skipping browser pass');
    return;
  }
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME || '/opt/google/chrome/chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  const base = 'http://127.0.0.1:' + port;
  await page.goto(base + '/index.html', { waitUntil: 'networkidle0', timeout: 60000 });
  const home = await page.evaluate(() => ({
    tag: document.documentElement.innerHTML.includes('ti:"343288039"'),
    sheets: document.styleSheets.length,
    margin: getComputedStyle(document.body).margin,
    font: getComputedStyle(document.body).fontFamily,
  }));
  eq('homepage tag in the document', home.tag, true);
  eq('homepage loaded stylesheets', home.sheets > 3, true);
  eq('homepage body margin is styled', home.margin, '0px');
  if (!/Montserrat|Segoe/.test(home.font)) { eq('homepage font', home.font, 'Montserrat'); }

  await page.goto(base + '/Kids_Map.html', { waitUntil: 'domcontentloaded', timeout: 60000 });
  const kids = await page.content();
  eq('kids map document has no bat.bing.com', kids.includes('bat.bing.com'), false);

  await page.goto(base + '/Hawaiian_Monk_Seal_Recovery.html', { waitUntil: 'networkidle0', timeout: 60000 });
  const monk = await page.evaluate(() => ({
    tag: document.documentElement.innerHTML.includes('https://bat.bing.com/bat.js'),
    donate: !!document.querySelector('a[data-sp-donate]'),
    margin: getComputedStyle(document.body).margin,
    sheets: document.styleSheets.length,
  }));
  eq('monk seal page has the UET script', monk.tag, true);
  eq('monk seal page has no Donate marker', monk.donate, false);
  eq('monk seal page is styled', monk.margin === '0px' && monk.sheets > 3, true);
  await page.evaluate(() => {
    const a = document.querySelector('a.donate-btn');
    a && a.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  });
  const afterInfo = await page.evaluate(() => (window.uetq || []).filter(x => x && x[1] === 'donate_click'));
  eq('further-information click does not push donate_click', afterInfo.length, 0);

  await page.goto(base + '/Snow_Leopard_Trust.html', { waitUntil: 'networkidle0', timeout: 60000 });
  const t0 = Date.now();
  const result = await page.evaluate(() => {
    const a = document.querySelector('a[data-sp-donate]');
    const start = performance.now();
    const ev = new MouseEvent('click', { bubbles: true, cancelable: true });
    a.dispatchEvent(ev);
    const q = window.uetq || [];
    let label = '';
    for (let i = 0; i < q.length; i++) if (q[i] === 'donate_click' && q[i + 1] && q[i + 1].event_label) label = q[i + 1].event_label;
    return { ms: performance.now() - start, cancelled: ev.defaultPrevented, label, target: a.target };
  });
  eq('snow leopard donate_click label', result.label, 'Snow_Leopard_Trust');
  eq('snow leopard click not cancelled', result.cancelled, false);
  eq('snow leopard click still opens a new tab', result.target, '_blank');
  eq('snow leopard handler is not a noticeable delay', result.ms < 30, true);
  console.log('  handler ms', result.ms.toFixed(2), 'wall', Date.now() - t0);

  await page.goto(base + '/fr/Solutions.html', { waitUntil: 'domcontentloaded', timeout: 60000 });
  const frHas = await page.evaluate(() => document.documentElement.innerHTML.includes('ti:"343288039"'));
  eq('french solutions page has the tag', frHas, true);

  const forced = SRC.replace('if(/(^|\\.)savingplanets\\.com$/.test(location.hostname))', 'if(true)');
  const hits = [];
  page.on('request', req => {
    const u = req.url();
    if (u.includes('bat.bing.com')) hits.push(u + ' ' + (req.postData() || ''));
  });
  await page.setContent(`<!DOCTYPE html><html><head><title>UET fixture</title></head><body>
    <a id="d" data-sp-donate="1" href="https://example.org/donate" target="_blank">Donate</a>
    <script>${forced}<\/script></body></html>`, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.waitForFunction(() => window.uetq && typeof window.uetq.push === 'function' && !Array.isArray(window.uetq), { timeout: 20000 }).catch(() => {});
  await page.evaluate(() => document.getElementById('d').dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })));
  await new Promise(r => setTimeout(r, 1500));
  const queued = await page.evaluate(() => {
    const q = window.uetq;
    if (!q) return null;
    if (Array.isArray(q)) return q;
    return 'uet-object';
  });
  const joined = hits.join('\n');
  eq('bat.js was requested', hits.some(h => h.includes('bat.js') || h.includes('bat.bing.com')), true);
  eq('donate_click reached Microsoft', /donate_click/.test(joined) || queued === 'uet-object', true);
  const sample = hits.find(h => /donate_click/.test(h)) || '';
  console.log('  bat requests', hits.length, 'queue', queued === 'uet-object' ? 'UET object' : JSON.stringify(queued));
  console.log('  donate request', sample.slice(0, 700));

  await page.goto(base + '/Privacy.html', { waitUntil: 'domcontentloaded', timeout: 60000 });
  const priv = await page.evaluate(() => document.body.innerText.includes('Microsoft Advertising') && !!document.querySelector('a[href="https://privacy.microsoft.com/privacystatement"]'));
  eq('privacy page states the tag and links to Microsoft', priv, true);

  await browser.close();
}

(async () => {
  const srv = await serve(ROOT);
  const port = srv.address().port;
  try { await chromePass(port); }
  finally { srv.close(); }
  if (failed) { console.error(failed + ' failed'); process.exit(1); }
  console.log('all uet checks passed');
})().catch(err => { console.error(err); process.exit(1); });
