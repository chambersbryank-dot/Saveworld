// Search build. Runs in scripts/weekly-sync.sh (output committed: /pagefind/ and /search/semantic-*).
// Run after any page change:  npm ci && node scripts/build-search.mjs
// (An Actions version is ready in docs/static-with-search.yml.txt; it needs a token with `workflow` scope.)
// One step builds BOTH search layers from the same HTML so they ship together:
//   1) Pagefind keyword index  -> <out>/pagefind/   (MIT, https://pagefind.app)
//   2) Semantic vector index   -> <out>/search/semantic-index.json + semantic-vectors.bin
//      model: Xenova/bge-small-en-v1.5 (MIT), q8, CLS pooling, normalized (same as the browser).
// Usage: node scripts/build-search.mjs [siteDir=.] [outDir=siteDir]
// The browser contract for the semantic files is documented in search/semantic.js.
import fs from 'node:fs';
import path from 'node:path';
import * as pagefind from 'pagefind';

const SITE = path.resolve(process.argv[2] || '.');
const OUT = path.resolve(process.argv[3] || SITE);
const SKIP = new Set(['Search.html', '404.html', 'Project-R.html', 'Community.html']);
const isPage = f => f.endsWith('.html') && !SKIP.has(path.basename(f)) && !/^google[0-9a-f]+\.html$/.test(path.basename(f));

const files = [];
for (const dir of ['', 'fr', 'es', 'ar', 'it']) {
  for (const f of fs.readdirSync(path.join(SITE, dir))) if (isPage(f)) files.push(dir ? dir + '/' + f : f);
}

// ---------- 1) Pagefind ----------
fs.rmSync(path.join(OUT, 'pagefind'), { recursive: true, force: true }); // drop stale hashed chunks
const { index, errors } = await pagefind.createIndex({
  excludeSelectors: ['.share-bar', '.related-solutions', '.page-reviewed', '.diff-strip', 'nav', 'footer', 'script', 'style', '.skip-link', '.lang-switch', '[data-pagefind-ignore]', '.shr', '.nl-call', '.emb-bar', '.emb-attr', '.std-wrap', '.gu-link'],
  forceLanguage: undefined,
});
if (errors.length) throw new Error(errors.join('\n'));
for (const f of files) {
  const r = await index.addHTMLFile({ url: '/' + f, content: fs.readFileSync(path.join(SITE, f), 'utf8') });
  if (r.errors.length) console.warn('pagefind:', f, r.errors);
}
const w = await index.writeFiles({ outputPath: path.join(OUT, 'pagefind') });
if (w.errors.length) throw new Error(w.errors.join('\n'));
await pagefind.close();
console.log(`pagefind: indexed ${files.length} pages (en/fr/es/ar/it)`);

// ---------- 2) Semantic index (English pages) ----------
const decode = s => s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;|&#39;|&apos;/g, "'")
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n)).replace(/&[a-z]+;/g, ' ');
const text = h => decode(h.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const HUBS = /^(Oceans|Lakes|Rivers|Deforestation|Space|Earth_Observation|Planetary_Defense|Space_Disposal|Space_Weather|Project-Rawane)\.html$/;

// general/site pages rank slightly below solution and hub pages in the semantic layer
const GENERAL = /^(index|Solutions|Glossary|Teachers|About|Amazing_Facts|Myth_vs_Fact|Community|Contact|Press|Ways_to_Help|Find_a_Cleanup|Rawanes_Mission_Log)\.html$/;
const pages = [], chunks = [];
for (const f of files.filter(f => !f.includes('/'))) {
  let h = fs.readFileSync(path.join(SITE, f), 'utf8');
  const title = text((h.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || (h.match(/<title>([^<]*)/) || [])[1] || f).split('|')[0].trim();
  const desc = decode((h.match(/name="description" content="([^"]*)"/) || [])[1] || '');
  h = h.replace(/<!-- (SHARE|RELATED|REVIEWED|DIFF):START -->[\s\S]*?<!-- \1:END -->/g, ' ') // Batch A UI blocks: not page content
       .replace(/<head[\s\S]*?<\/head>/, '').replace(/<(script|style|nav|footer|noscript)[\s\S]*?<\/\1>/g, ' ')
       .replace(/<[^>]*data-pagefind-ignore[^>]*>/g, ' ');
  const blocks = [...h.matchAll(/<(h2|h3|p|li|td|blockquote)[^>]*>([\s\S]*?)<\/\1>/g)].map(m => text(m[2])).filter(t => t.length > 25);
  const kind = HUBS.test(f) ? 'hub' : GENERAL.test(f) ? 'page' : 'solution';
  const p = pages.push({ url: '/' + f, title, desc: desc.slice(0, 200), kind }) - 1;
  // chunk 1 = title + description; then ~90-word windows over body text (max 14 per page)
  chunks.push({ p, t: `${title}. ${desc}` });
  const words = blocks.join(' ').split(' ');
  for (let i = 0, n = 0; i < words.length && n < 14; i += 75, n++) chunks.push({ p, t: `${title}: ` + words.slice(i, i + 90).join(' ') });
}

// ---------- hub labels for result cards: page -> hub (from each page's BreadcrumbList), hub names per language ----------
const hubOf = {}, hubNames = { en: {}, fr: {}, es: {}, ar: {}, it: {} };
for (const f of files.filter(f => !f.includes('/'))) {
  const h = fs.readFileSync(path.join(SITE, f), 'utf8');
  const bc = (h.match(/"BreadcrumbList", "itemListElement": (\[[^\]]*\])/) || [])[1];
  if (HUBS.test(f)) { hubOf[f] = f; continue; }
  try { const items = JSON.parse(bc || '[]'); if (items.length >= 3) { const hub = path.basename(items[1].item); if (HUBS.test(hub)) hubOf[f] = hub; } } catch (e) { /* skip */ }
}
for (const hub of new Set(Object.values(hubOf))) for (const l of Object.keys(hubNames)) {
  const fp = path.join(SITE, l === 'en' ? '' : l, hub); if (!fs.existsSync(fp)) continue;
  hubNames[l][hub] = text((fs.readFileSync(fp, 'utf8').match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || hub);
}
fs.mkdirSync(path.join(OUT, 'search'), { recursive: true });
fs.writeFileSync(path.join(OUT, 'search', 'hubs.json'), JSON.stringify({ hubOf, hubNames }));
console.log(`hubs: ${Object.keys(hubOf).length} pages mapped to ${Object.keys(hubNames.en).length} hubs`);

const { pipeline, env } = await import('@huggingface/transformers');
env.cacheDir = path.resolve('.cache/hf');
const MODEL = 'Xenova/bge-small-en-v1.5';
const embed = await pipeline('feature-extraction', MODEL, { dtype: 'q8' });
const DIM = 384, vec = new Int8Array(chunks.length * DIM);
for (let i = 0; i < chunks.length; i += 32) {
  const batch = chunks.slice(i, i + 32).map(c => c.t);
  const out = await embed(batch, { pooling: 'cls', normalize: true });
  const data = out.data;
  for (let j = 0; j < batch.length; j++) for (let d = 0; d < DIM; d++)
    vec[(i + j) * DIM + d] = Math.max(-127, Math.min(127, Math.round(data[j * DIM + d] * 254)));
}
fs.mkdirSync(path.join(OUT, 'search'), { recursive: true });
fs.writeFileSync(path.join(OUT, 'search', 'semantic-vectors.bin'), Buffer.from(vec.buffer));
fs.writeFileSync(path.join(OUT, 'search', 'semantic-index.json'), JSON.stringify({
  version: 1, model: MODEL, dtype: 'q8', pooling: 'cls', dim: DIM, scale: 254,
  queryPrefix: 'Represent this sentence for searching relevant passages: ',
  pages, chunkPage: chunks.map(c => c.p),
}));
console.log(`semantic: ${pages.length} pages, ${chunks.length} chunks, ${(vec.length / 1024).toFixed(0)} KB vectors`);
