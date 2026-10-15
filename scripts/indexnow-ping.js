#!/usr/bin/env node
// IndexNow (Bing, Yandex, Seznam, Naver...): tell search engines which URLs changed.
// Key file (Option 1, site root): https://www.savingplanets.com/aa19429b4f58f36d34c263abe996de09.txt (contains exactly the key).
// Usage:
//   node scripts/indexnow-ping.js                 dry run: URLs changed since last successful ping (.indexnow-last) or HEAD~1
//   node scripts/indexnow-ping.js --since <ref>   changed since a git ref
//   node scripts/indexnow-ping.js --all           every <loc> in sitemap.xml (en/fr/es/ar)
//   node scripts/indexnow-ping.js --send          submit
//   --wait                                        before sending, poll the live key file (cache-busted) up to 10 min
// Fallback: if the last-ping ref is unknown (shallow/fresh clone), all sitemap URLs are sent.
// Never exits non-zero (errors are logged) so it can't fail the weekly sync.
const fs = require('fs'), { execSync } = require('child_process');
const HOST = 'www.savingplanets.com', SITE = 'https://' + HOST + '/', KEY = 'aa19429b4f58f36d34c263abe996de09';
const KEY_URL = SITE + KEY + '.txt', STATE = '.indexnow-last';
const args = process.argv.slice(2), send = args.includes('--send');
const i = args.indexOf('--since');
const sh = c => execSync(c, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
const NOINDEX = new Set(['Project-R.html', '404.html', 'Community.html']);
const sitemap = () => fs.existsSync('sitemap.xml') ? [...new Set([...fs.readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim()))] : [];
let since = i >= 0 ? args[i + 1] : (fs.existsSync(STATE) ? fs.readFileSync(STATE, 'utf8').trim() : 'HEAD~1');
let urls;
if (args.includes('--all')) urls = sitemap();
else {
  try {
    const files = sh('git diff --name-only --diff-filter=AM ' + since + ' HEAD').split('\n')
      .filter(f => /^((fr|es|ar|it)\/)?[^/]+\.html$/.test(f) && !NOINDEX.has(f.split('/').pop()) && fs.existsSync(f));
    urls = files.map(f => SITE + (f.replace(/(^|\/)index\.html$/, '$1')));
    if (files.length && fs.existsSync('sitemap.xml')) urls.push(SITE + 'sitemap.xml');
  } catch (e) { console.log('IndexNow: ref ' + since + ' unknown; falling back to sitemap'); since = 'sitemap'; urls = sitemap(); }
}
urls = [...new Set(urls)];
console.log('IndexNow: ' + urls.length + ' URL(s) since ' + since + (send ? '' : ' (dry run; add --send to submit)'));
if (!send) { urls.forEach(u => console.log('  ' + u)); process.exit(0); }
if (!urls.length) process.exit(0);
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  try {
    if (args.includes('--wait')) {
      let ok = false;
      for (let t = 0; t < 40 && !ok; t++) {
        try { const r = await fetch(KEY_URL + '?cb=' + Date.now(), { cache: 'no-store' }); ok = r.status === 200 && (await r.text()).trim() === KEY; } catch (_) {}
        if (!ok) await sleep(15000);
      }
      if (!ok) { console.error('IndexNow: key file not live at ' + KEY_URL + '; skipped'); return; }
    }
    let allOk = true;
    for (let b = 0; b < urls.length; b += 10000) {
      const r = await fetch('https://api.indexnow.org/indexnow', {
        method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({ host: HOST, key: KEY, keyLocation: KEY_URL, urlList: urls.slice(b, b + 10000) })
      });
      const body = (await r.text()).slice(0, 300);
      console.log('IndexNow batch ' + (b / 10000 + 1) + ': HTTP ' + r.status + ' ' + r.statusText + (body ? ' ' + body : ''));
      if (r.status !== 200 && r.status !== 202) allOk = false;
    }
    if (allOk) fs.writeFileSync(STATE, sh('git rev-parse HEAD').trim() + '\n');
  } catch (e) { console.error('IndexNow failed:', e.message); }
})();
