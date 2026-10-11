#!/usr/bin/env node
// IndexNow (Bing, Yandex, Seznam, Naver...): tell search engines which URLs changed.
// Key file: /aa19429b4f58f36d34c263abe996de09.txt (served at https://www.savingplanets.com/aa19429b4f58f36d34c263abe996de09.txt, contains the key).
// Usage:
//   node scripts/indexnow-ping.js                 dry run: list .html URLs changed since the last ping (or HEAD~1)
//   node scripts/indexnow-ping.js --since <ref>   changed since a git ref (e.g. origin/main~5)
//   node scripts/indexnow-ping.js --all          every <loc> in sitemap.xml (one-off full submission)
//   node scripts/indexnow-ping.js --send          submit (only AFTER the commit is live on the site)
// Don't spam: run once per deploy, only for changed pages. Last sent commit is kept in .indexnow-last.
const fs = require('fs'), { execSync } = require('child_process');
const HOST = 'www.savingplanets.com', SITE = 'https://' + HOST + '/', KEY = 'aa19429b4f58f36d34c263abe996de09';
const args = process.argv.slice(2), send = args.includes('--send');
const i = args.indexOf('--since');
const since = i >= 0 ? args[i + 1] : (fs.existsSync('.indexnow-last') ? fs.readFileSync('.indexnow-last', 'utf8').trim() : 'HEAD~1');
const NOINDEX = new Set(['Project-R.html', '404.html']);
const files = execSync('git diff --name-only --diff-filter=AM ' + since + ' HEAD', { encoding: 'utf8' }).split('\n')
  .filter(f => /^((fr|es|ar)\/)?[^/]+\.html$/.test(f) && !NOINDEX.has(f.split('/').pop()) && fs.existsSync(f));
let urls = files.map(f => SITE + (f === 'index.html' ? '' : f)).slice(0, 10000);
if (args.includes('--all')) urls = [...new Set([...fs.readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim()))].slice(0, 10000);
if (fs.existsSync('sitemap.xml') && files.includes('sitemap.xml')) urls.push(SITE + 'sitemap.xml');
console.log(urls.length + ' changed URL(s) since ' + since + (send ? '' : ' (dry run; add --send to submit)'));
urls.forEach(u => console.log('  ' + u));
if (!send || !urls.length) process.exit(0);
fetch('https://api.indexnow.org/indexnow', {
  method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: SITE + KEY + '.txt', urlList: urls })
}).then(r => {
  console.log('IndexNow:', r.status, r.statusText);
  if (r.status === 200 || r.status === 202) fs.writeFileSync('.indexnow-last', execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim());
}).catch(e => { console.error('IndexNow failed:', e.message); process.exit(1); });
