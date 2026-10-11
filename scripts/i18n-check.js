// List English pages whose /fr/, /es/, /ar/ translation is missing or out of date.
// Each translation carries <meta name="i18n-source" content="<Page.html> <hash>"> written by
// scripts/i18n-build.py; the hash is of the normalized English source (hreflang links, nav menu
// block, language switcher and ?v= cache tags ignored). Run: node scripts/i18n-check.js [--all]
// --all also lists every English sitemap page that has no translation yet (informational).
// Exit 0 = all translated pages current, 1 = something missing/stale in the translated set.
const fs = require('fs'), crypto = require('crypto'), path = require('path');
const LANGS = ['fr', 'es', 'ar'];
const PAGES = fs.readFileSync('i18n/pages.txt', 'utf8').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
function normalize(src) {
  return src.replace(/<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?/g, '')
    .replace(/<!-- PROJECT-R-MENU:START -->[\s\S]*?<!-- PROJECT-R-MENU:END -->/g, '')
    .replace(/<!-- SOLUTIONS-MENU:START -->[\s\S]*?<!-- SOLUTIONS-MENU:END -->/g, '')
    .replace(/<li class="lang-switch"[\s\S]*?<\/li>/g, '')
    .replace(/\?v=[0-9a-z]+/g, '');
}
const hash = f => crypto.createHash('sha1').update(normalize(fs.readFileSync(f, 'utf8')), 'utf8').digest('hex').slice(0, 12);
let bad = 0;
for (const page of PAGES) {
  if (!fs.existsSync(page)) { console.log(`${page}: English page missing`); bad++; continue; }
  const h = hash(page);
  for (const l of LANGS) {
    const t = path.join(l, page);
    if (!fs.existsSync(t)) { console.log(`MISSING  ${t}`); bad++; continue; }
    const m = fs.readFileSync(t, 'utf8').match(/<meta content="([^ "]+) ([0-9a-f]+)" name="i18n-source"|<meta name="i18n-source" content="([^ "]+) ([0-9a-f]+)"/);
    const th = m ? (m[2] || m[4]) : null;
    if (th !== h) { console.log(`STALE    ${t} (English changed since translation)`); bad++; }
  }
}
if (process.argv.includes('--all')) {
  const all = [...fs.readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1])
    .filter(u => !/\/(fr|es|ar)\//.test(u)).map(u => path.basename(u)).filter(f => f.endsWith('.html') && !PAGES.includes(f));
  console.log(`Not translated (not in scope yet): ${all.length} pages`);
}
console.log(bad ? `${bad} translation(s) missing or stale. Update i18n/<lang>.json for new strings, then python3 scripts/i18n-build.py.` : 'All translations current.');
process.exit(bad ? 1 : 0);
