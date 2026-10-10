// Build assets/data/solutions.json from sitemap.xml + per-page <meta name="sp:..."> tags.
// Run via: node build-search-index.js   (it calls this file), or directly: node build-stats.js
//
// Per-page metadata (in <head>):
//   <meta name="sp:category" content="ocean|lakes|rivers|forests|space|planetary-defense|space-weather|earth-observation|project-r">
//   <meta name="sp:type" content="hub|solution">
//   <meta name="sp:classification" content="natural|corporate|agency|nonprofit">   (solutions)
//   <meta name="sp:status" content="active|horizon">   horizon = no confirmed contract/funding yet
//   <meta name="sp:item" content="name|classification|status">   a solution presented as a section of a hub; repeatable
//   <meta name="sp:stat" content="label|value|unit|kind|sourceUrl">   kind = impact (summable) or fact; repeatable
// Upcoming missions are read from [data-mission] elements (data-launch / data-arrival in the future).
// Horizon pages are counted separately and their impact numbers are never summed.
const fs = require('fs');
const path = require('path');

const CATEGORIES = { ocean: 'Ocean', lakes: 'Lakes', rivers: 'Rivers', forests: 'Forests', space: 'Space',
  'planetary-defense': 'Planetary Defense', 'space-weather': 'Space Weather & Shields',
  'earth-observation': 'Earth Observation', 'project-r': 'Project R' };
const SKIP = ['Search.html', '404.html', 'index.html', 'About.html', 'Contact.html', 'Amazing_Facts.html'];
// Pages another worker owns and that cannot carry tags yet. Remove an entry once the page has its own sp: tags.
const FALLBACK = {
};


// ---- Project R nav dropdown (single source: solutions.json "projectRMenu") ----
// Hubs shown, in order. Items come from elements on each hub page carrying
//   id="anchor" data-menu-item="Name|active|horizon"   (attribute order: id first)
// and are listed alphabetically. The HTML is written into every page between
// <!-- PROJECT-R-MENU:START --> and <!-- PROJECT-R-MENU:END -->.
const PROJECT_R_HUBS = [['Space_Disposal.html', 'Space Disposal'], ['Planetary_Defense.html', 'Planetary Defense'], ['Space_Weather.html', 'Space Weather & Shields']];
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
function buildProjectRMenu(warnings) {
  return PROJECT_R_HUBS.filter(([f]) => fs.existsSync(f)).map(([file, name]) => {
    const html = fs.readFileSync(file, 'utf8');
    const items = [...html.matchAll(/id="([^"]+)" data-menu-item="([^"|]+)\|(active|horizon)"/g)]
      .map(m => ({ name: m[2].replace(/&amp;/g, '&'), anchor: m[1], href: `${file}#${m[1]}`, status: m[3] }))
      .sort((a, b) => a.name.localeCompare(b.name, 'en', { sensitivity: 'base' }));
    if (!items.length) warnings.push(`${file}: no data-menu-item entries for the Project R menu`);
    return { hub: name, href: file, items };
  });
}
function menuHtml(menu) {
  const groups = menu.map(g => `<li class="menu-group"><a class="menu-hub" href="${g.href}">${esc(g.hub)}</a><ul>` +
    g.items.map(i => `<li><a href="${i.href}">${esc(i.name)}${i.status === 'horizon' ? ' <span class="menu-tag">horizon</span>' : ''}</a></li>`).join('') + '</ul></li>').join('');
  return '<li class="nav-dropdown nav-dropdown-wide"><a href="Project-R.html" class="dropdown-toggle" aria-haspopup="true" aria-expanded="false">Project R</a>' +
    '<ul class="dropdown-menu"><li><a class="menu-overview" href="Project-R.html">Project R overview</a></li>' + groups + '</ul></li>';
}
function writeProjectRMenu(menu) {
  const html = menuHtml(menu); let n = 0;
  const re = /<!-- PROJECT-R-MENU:START -->[\s\S]*?<!-- PROJECT-R-MENU:END -->/;
  fs.readdirSync('.').filter(f => f.endsWith('.html')).forEach(f => {
    const src = fs.readFileSync(f, 'utf8'); if (!re.test(src)) return;
    const next = src.replace(re, `<!-- PROJECT-R-MENU:START -->${html}<!-- PROJECT-R-MENU:END -->`);
    if (next !== src) { fs.writeFileSync(f, next); n++; }
  });
  return n;
}

function build() {
  const sitemap = fs.readFileSync('sitemap.xml', 'utf8');
  const files = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => path.basename(m[1].trim()))
    .filter(f => f.endsWith('.html') && !SKIP.includes(f) && fs.existsSync(f));
  const now = Date.now();
  const warnings = [];
  const pages = [];
  for (const file of files) {
    const html = fs.readFileSync(file, 'utf8');
    const metas = {};
    for (const m of html.matchAll(/<meta name="sp:([a-z]+)" content="([^"]*)">/g)) (metas[m[1]] = metas[m[1]] || []).push(m[2].replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&').replace(/&quot;/g, '"'));
    const one = k => (metas[k] || [])[0];
    let meta = { category: one('category'), type: one('type'), classification: one('classification'), status: one('status') || 'active' };
    if (!meta.category && FALLBACK[file]) { meta = Object.assign({}, FALLBACK[file]); warnings.push(`${file}: no sp: tags, using FALLBACK in build-stats.js`); }
    if (!meta.category || !CATEGORIES[meta.category]) { warnings.push(`${file}: missing or unknown sp:category, skipped`); continue; }
    if (!meta.type) warnings.push(`${file}: missing sp:type`);
    if (meta.type === 'solution' && !meta.classification) warnings.push(`${file}: missing sp:classification`);
    const title = ((html.match(/<h1[^>]*>(.*?)<\/h1>/s) || [])[1] || file).replace(/<[^>]+>/g, '').trim();
    const stats = (metas.stat || []).map(s => { const [label, value, unit, kind, sourceUrl] = s.split('|'); return { label, value: isNaN(+value) ? value : +value, unit, kind, sourceUrl }; });
    stats.forEach(s => { if (!/^https?:\/\//.test(s.sourceUrl || '')) warnings.push(`${file}: stat "${s.label}" has no source URL`); });
    const missions = [];
    for (const m of html.matchAll(/<[^>]*data-mission="([^"]+)"[^>]*>/g)) {
      const tag = m[0];
      const get = a => (tag.match(new RegExp(a + '="([^"]+)"')) || [])[1];
      const dates = [['launch', get('data-launch')], ['arrival', get('data-arrival')]].filter(d => d[1]);
      const next = dates.find(d => new Date(d[1]).getTime() > now);
      missions.push({ name: m[1], upcoming: !!next || !dates.length && /no earlier|NET|launch/i.test(get('data-status') || ''), next: next ? { event: next[0], date: next[1] } : null });
    }
    pages.push(Object.assign({ url: file, title }, meta, { stats, missions }));
    // Hub sections that each present a solution: <meta name="sp:item" content="name|classification|status">
    (metas.item || []).forEach(it => { const [name, classification, status] = it.split('|');
      pages.push({ url: file, title: name, category: meta.category, type: 'solution', classification, status: status || 'active', section: true, stats: [], missions: [] }); });
  }
  function agg(list) {
    const sol = list.filter(p => p.type === 'solution');
    const active = sol.filter(p => p.status !== 'horizon');
    const by = {};
    active.forEach(p => { by[p.classification] = (by[p.classification] || 0) + 1; });
    const impact = {};
    active.forEach(p => p.stats.filter(s => s.kind === 'impact' && typeof s.value === 'number').forEach(s => {
      const k = s.unit; impact[k] = impact[k] || { unit: k, total: 0, pages: [] }; impact[k].total += s.value; impact[k].pages.push(p.url);
    }));
    return { solutions: active.length, horizon: sol.length - active.length, hubs: list.filter(p => p.type === 'hub').length,
      byClassification: by, upcomingMissions: list.reduce((n, p) => n + p.missions.filter(m => m.upcoming).length, 0),
      impactTotals: Object.values(impact) };
  }
  const categories = {};
  Object.keys(CATEGORIES).forEach(c => { const l = pages.filter(p => p.category === c); if (l.length) categories[c] = Object.assign({ name: CATEGORIES[c] }, agg(l)); });
  const projectRMenu = buildProjectRMenu(warnings);
  const out = { generated: new Date().toISOString(), projectRMenu, site: Object.assign({ categories: Object.keys(categories).length }, agg(pages)), categories, pages };
  fs.mkdirSync('assets/data', { recursive: true });
  fs.writeFileSync('assets/data/solutions.json', JSON.stringify(out, null, 1) + '\n');
  console.log(`solutions.json: ${out.site.solutions} active solutions, ${out.site.horizon} on the horizon, ${out.site.hubs} hubs, ${out.site.upcomingMissions} upcoming missions, ${pages.length} pages.`);
  const menuPages = writeProjectRMenu(projectRMenu);
  console.log(`Project R menu: ${projectRMenu.reduce((n, g) => n + g.items.length, 0)} items in ${projectRMenu.length} hubs; ${menuPages} pages updated.`);
  warnings.forEach(w => console.warn('WARN ' + w));
  return out;
}
module.exports = build;
if (require.main === module) build();
