// Build the keyword search index in Search.html from sitemap.xml.
// Run locally: node build-search-index.js
// GitHub Pages is static-only, so this must run before pushing.

const fs = require('fs');
const path = require('path');

const sitemap = fs.readFileSync('sitemap.xml', 'utf8');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);

const pages = locs.map(url => {
  const file = path.basename(url);
  const html = fs.readFileSync(file, 'utf8').replace(/\s+/g, ' ');
  const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || file;
  const desc = (html.match(/name="description" content="([^"]+)"/) || [])[1] || '';
  const h1 = (html.match(/<h1[^>]*>([^<]+)<\/h1>/) || [])[1] || '';
  const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 500);
  return { file, title, desc, h1, text };
});

const index = pages.map(p => ({
  file: p.file,
  title: p.title,
  desc: p.desc,
  h1: p.h1,
  text: p.text
}));

let search = fs.readFileSync('Search.html', 'utf8);
const start = search.indexOf('const PAGES = [');
const end = search.indexOf('];', start) + 2;
if (start === -1 || end === 1) {
  console.error('Could not find PAGES array in Search.html');
  process.exit(1);
}
search = search.slice(0, start) + 'const PAGES = ' + JSON.stringify(index, null, 2) + search.slice(end);
fs.writeFileSync('Search.html', search);
console.log('Updated Search.html with ' + index.length + ' pages.');

// Warn about sitemap pages missing from the index data table
const missing = locs.filter(url => !search.includes(path.basename(url)));
if (missing.length) console.log('Warning: sitemap pages not referenced in Search.html:', missing.join(', '));
