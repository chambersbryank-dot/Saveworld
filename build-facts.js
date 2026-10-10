// Regenerate the facts list on Amazing_Facts.html (between <!-- FACTS:START --> and <!-- FACTS:END -->).
// Run via: node build-search-index.js (it calls this file), or directly: node build-facts.js
//
// Convention: any page in sitemap.xml can mark a fact with
//   <p class="amazing-fact" data-source="URL" data-source-name="NASA" data-title="Short heading">Fact text.</p>
// Optional: data-image, data-image-alt, data-image-credit add a card image.
// (add `hidden` to keep it off the page itself). data-title is optional (defaults to the first words).
// Facts without data-source are skipped with a warning. Duplicates (same text) are dropped.
// Hand-written cards inside the markers carry data-fact-origin="hand" and are kept as written.
// All cards are sorted alphabetically by heading; page facts link back to their page and the source.
const fs = require('fs');
const path = require('path');
const FILE = 'Amazing_Facts.html', START = '<!-- FACTS:START -->', END = '<!-- FACTS:END -->';

function buildFacts() {
  let html = fs.readFileSync(FILE, 'utf8');
  const a = html.indexOf(START), b = html.indexOf(END);
  if (a === -1 || b === -1 || b < a) { console.error(`${FILE}: FACTS markers missing; skipped.`); return; }
  const block = html.slice(a + START.length, b);
  const strip = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const esc = s => s.replace(/&(?!(#\d+|#x[0-9a-f]+|[a-z]+);)/gi, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  const attr = (tag, n) => { const m = tag.match(new RegExp('\\b' + n + '="([^"]*)"')); return m ? m[1] : ''; };

  const cards = [];
  for (const m of block.matchAll(/<div class="w-card" data-fact-origin="hand">[\s\S]*?<\/div>/g)) {
    const title = strip((m[0].match(/<h3>([\s\S]*?)<\/h3>/) || [])[1] || '');
    cards.push({ title, key: strip(m[0]).toLowerCase(), html: m[0] });
  }

  const pages = [...fs.readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)]
    .map(m => path.basename(m[1].trim())).filter(f => f.endsWith('.html') && f !== FILE && fs.existsSync(f));
  const seen = new Set();
  let found = 0, skipped = 0, dupes = 0;
  for (const page of pages) {
    const src = fs.readFileSync(page, 'utf8');
    const pageTitle = strip(((src.match(/<title>([^<]+)<\/title>/) || [])[1] || page).split('|')[0]);
    for (const m of src.matchAll(/<p\b([^>]*\bclass="[^"]*\bamazing-fact\b[^"]*"[^>]*)>([\s\S]*?)<\/p>/g)) {
      const tag = m[1], text = strip(m[2]);
      if (!text) continue;
      const source = attr(tag, 'data-source');
      if (!source) { console.warn(`Warning: ${page}: amazing-fact without data-source skipped: "${text.slice(0, 60)}"`); skipped++; continue; }
      const key = text.toLowerCase();
      if (seen.has(key)) { dupes++; continue; }
      seen.add(key); found++;
      const title = attr(tag, 'data-title') || text.split(' ').slice(0, 5).join(' ');
      const sourceName = attr(tag, 'data-source-name') || source.replace(/^https?:\/\/(www\.)?/, '').split('/')[0];
      cards.push({ title, html:
        `<div class="w-card" data-fact-origin="page" data-fact-page="${page}"><h3>${esc(title)}</h3>` +
        (attr(tag, 'data-image') ? `<img class="fact-img" src="${esc(attr(tag, 'data-image'))}" alt="${esc(attr(tag, 'data-image-alt') || '')}" loading="lazy" decoding="async">` + (attr(tag, 'data-image-credit') ? `<p class="fact-credit">Image: ${esc(attr(tag, 'data-image-credit'))}</p>` : '') : '') +
        `<p>${esc(text)}</p>` +
        `<p class="fact-source">From: <a href="${page}">${esc(pageTitle)}</a></p>` +
        `<p class="fact-source">Source: <a href="${esc(source)}" target="_blank" rel="noreferrer">${esc(sourceName)}</a></p></div>` });
    }
  }
  cards.sort((x, y) => x.title.localeCompare(y.title, 'en', { sensitivity: 'base' }));
  html = html.slice(0, a + START.length) + '\n' + cards.map(c => c.html).join('\n') + '\n' + html.slice(b);
  fs.writeFileSync(FILE, html);
  console.log(`${FILE}: ${cards.length} facts (${found} from pages, ${cards.length - found} hand-written; ${dupes} duplicates, ${skipped} skipped for no source).`);
}
module.exports = buildFacts;
if (require.main === module) buildFacts();
