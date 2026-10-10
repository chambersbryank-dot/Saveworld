// Build the keyword search index in Search.html from sitemap.xml.
// Run locally: node build-search-index.js
// GitHub Pages is static-only, so this must run before pushing.
//
// Search.html holds a hand-curated list:  var pages = [ { title: '...', url: '...', text: '...' }, ... ];
// Existing entries are kept exactly as written (their keywords are curated).
// Pages in sitemap.xml that are missing from the list are appended, with a
// title and keywords taken from the page itself. Entries whose page no longer
// exists in sitemap.xml are reported but not removed.

const fs = require('fs');
const path = require('path');

const sitemap = fs.readFileSync('sitemap.xml', 'utf8');
const files = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)]
  .map(m => path.basename(m[1].trim()))
  .filter(f => f.endsWith('.html'))
  .filter(f => !['Search.html', '404.html', 'Project-R.html'].includes(f)); // never index these

let search = fs.readFileSync('Search.html', 'utf8');
const startMarker = 'var pages = [';
const start = search.indexOf(startMarker);
const end = start === -1 ? -1 : search.indexOf('];', start);
if (start === -1 || end === -1) {
  console.error('Could not find "var pages = [ ... ];" in Search.html');
  process.exit(1);
}

const body = search.slice(start + startMarker.length, end);
const entryRe = /\{\s*title:\s*'((?:\\'|[^'])*)',\s*url:\s*'((?:\\'|[^'])*)',\s*text:\s*'((?:\\'|[^'])*)'\s*\}/g;
const existing = [...body.matchAll(entryRe)].map(m => ({ title: m[1], url: m[2], text: m[3] }));
const leftover = body.replace(entryRe, '').replace(/[\s,]/g, '');
if (!existing.length || leftover) {
  console.error('Search.html pages list has entries this script cannot parse; aborting without changes.');
  process.exit(1);
}

const esc = s => s.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
const unesc = s => s.replace(/&amp;/g, '&').replace(/&#39;|&apos;/g, "'").replace(/&quot;/g, '"').replace(/&[a-z]+;/g, ' ');
const known = new Set(existing.map(e => e.url));
const added = [];

for (const file of files) {
  if (known.has(file) || !fs.existsSync(file)) continue;
  const html = fs.readFileSync(file, 'utf8').replace(/\s+/g, ' ');
  const rawTitle = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || file.replace(/\.html$/, '').replace(/_/g, ' ');
  const h1 = ((html.match(/<h1[^>]*>(.*?)<\/h1>/) || [])[1] || '').replace(/<[^>]+>/g, '').trim();
  const title = unesc(h1 || rawTitle.split('|')[0]).trim();
  const desc = (html.match(/name="description" content="([^"]+)"/) || [])[1] || '';
  const text = unesc(title + ' ' + desc).replace(/[^\w\s'-]/g, ' ').replace(/\s+/g, ' ').trim();
  existing.push({ title, url: file, text });
  added.push(file);
}

// Curated entries are written back exactly as found (already escaped);
// newly added entries are escaped here.
const curatedCount = existing.length - added.length;
const out = existing.map((e, i) => i < curatedCount
  ? `    { title: '${e.title}', url: '${e.url}', text: '${e.text}' }`
  : `    { title: '${esc(e.title)}', url: '${esc(e.url)}', text: '${esc(e.text)}' }`);

search = search.slice(0, start) + startMarker + '\n' + out.join(',\n') + '\n  ' + search.slice(end);
fs.writeFileSync('Search.html', search);

console.log(`Search.html: ${existing.length} pages (${added.length} added${added.length ? ': ' + added.join(', ') : ''}).`);
const stale = existing.filter(e => !files.includes(e.url)).map(e => e.url);
if (stale.length) console.log('Note: in Search.html but not in sitemap.xml (kept):', stale.join(', '));

// Also regenerate assets/data/solutions.json (stats engine).
require("./build-stats.js")();
