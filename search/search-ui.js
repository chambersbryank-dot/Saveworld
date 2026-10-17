/* Saving Planets hybrid search UI (Search.html).
 * 1) Pagefind keyword results appear instantly (all four languages).
 *    If every-word matching finds nothing, retry with the query's key terms (partial matches).
 * 2) On English pages the semantic layer (search/semantic.js) loads after the first query;
 *    then results are re-ranked by reciprocal-rank fusion of keyword + meaning.
 * 3) ?q= deep links are supported and kept in the address bar.
 * The page's built-in list search is a fallback only (window.SP_START_FALLBACK), used if Pagefind fails. */
window.SP_SEARCH_STARTED = true;
(async function () {
  const $ = id => document.getElementById(id);
  const input = $('q'), list = $('results'), status = $('status'), note = $('search-mode'), empty = $('sp-empty');
  if (!input || !list) return;
  const fallback = () => { window.SP_SEARCH_STARTED = false; window.SP_START_FALLBACK && window.SP_START_FALLBACK(); };
  const msg = k => { const el = document.querySelector('#sp-msg [data-k="' + k + '"]'); return el ? el.textContent : k; };
  const lang = document.documentElement.lang || 'en';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const initial = new URLSearchParams(location.search).get('q') || '';
  if (initial) input.value = initial;

  // example queries: link text is the query (translated with the page)
  document.querySelectorAll('.sp-examples a').forEach(a => {
    a.href = '?q=' + encodeURIComponent(a.textContent.trim());
    a.addEventListener('click', e => { e.preventDefault(); input.value = a.textContent.trim(); track(input.value); input.focus(); go(); });
  });
  // Oct 16: GA removed site-wide; no search analytics.
  const track = () => {};  // Oct 16: GA removed; search text is never sent anywhere (COPPA)
  input.closest('form')?.addEventListener('submit', e => { e.preventDefault(); input.blur(); track(input.value.trim()); go(); });

  // floating example questions: placed at build time by scripts/build-search-page.py (all topics; CSS shows the active one).
  // Oct 16: no client-side rendering any more, so the ring never shifts the search bar (CLS).
  document.querySelectorAll('.sp-ring .sp-q').forEach(a => a.addEventListener('click', e => {
    e.preventDefault(); input.value = a.textContent; go();
    $('status')?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }));
  // approved SI Helper Q&A (search/student-qa.json from scripts/build-student-qa.py; absent until the first answer is approved)
  const QA_T = { aero: 'aero', orbit: 'orbital', phys: 'physics', all: 'all' };
  let qa = [];
  fetch('/search/student-qa.json').then(r => r.ok ? r.json() : {}).then(d => { qa = (d[lang.slice(0, 2)] || []).map(e => ({ ...e, tab: QA_T[e.topic] || 'all' })); }).catch(() => {});
  const topic = () => document.documentElement.getAttribute('data-sp-topic') || 'all';
  document.addEventListener('sp-topic', () => { if (input.value.trim() && window.SP_SEARCH_ACTIVE) run(false, true); });

  // hub/category label for each result card (search/hubs.json, built from page breadcrumbs by scripts/build-search.mjs)
  const hubOf = new Map();
  const hubsReady = fetch('/search/hubs.json').then(r => r.json()).then(d => {
    const names = d.hubNames[lang.slice(0, 2)] || d.hubNames.en;
    for (const [pg, hub] of Object.entries(d.hubOf)) hubOf.set(pg, pg === hub ? msg('hub') : (names[hub] || d.hubNames.en[hub]));
  }).catch(() => {});
  function base(u) { return (u || '').replace(/[?#].*$/, '').split('/').pop(); }

  let pf;
  try { pf = await import('/pagefind/pagefind.js'); await pf.options({ baseUrl: '/', excerptLength: 22 }); pf.init(); }
  catch (e) { console.info('Pagefind unavailable, using built-in list search', e); return fallback(); }
  if (window.SP_FALLBACK_ON) return;            // fallback already took over (very slow network)
  window.SP_SEARCH_ACTIVE = true;

  let sem = null, semLoading = null, seq = 0;
  const semantic = await import('/search/semantic.js').catch(() => null);
  function startSemantic() {
    if (semLoading || !semantic || !semantic.supports(lang)) return;
    if (note) note.textContent = msg('loading');
    semLoading = semantic.load().then(e => { sem = e; if (note) note.textContent = msg('smart'); if (input.value.trim() && lastItems.length) run(false, true); })
      .catch(e => { console.info('Semantic layer unavailable', e); if (note) note.textContent = ''; });
  }

  const norm = u => u.replace(/^https?:\/\/[^/]+/, '').replace(/[?#].*$/, '');
  const STOP = new Set('a an and are as at be been but by can do does for from had has have how i i\'m im in into is it its may me my of on or our so such that the their them there these they this to too was we were what when where which who why will with would you your about also any some very just get help people stay away years ago because interested'.split(' '));
  // fr / es / ar question words and fillers (keyword retry only)
  'comment les des une un est sont pour dans sur avec que qui quels quelles quel quelle ils elles nous notre nos votre vos faire peut ce cette ces du au aux et ou se il la le de en vers depuis leur leurs plus deux façons simplement expliquez comparez week-end hors'.split(' ').forEach(w => STOP.add(w));
  'cómo como los las del una uno es son para por con que qué quién cuál cuáles sus nuestro nuestra mi mis este esta estos fin semana puede puedo hacer y o se el la de en al desde más dos formas forma sencilla explica compara'.split(' ').forEach(w => STOP.add(w));
  'كيف ما ماذا من في على إلى عن مع هل التي الذي وكيف وما يمكن أن أو و بين نهاية الأسبوع عطلة اشرح ببساطة قارن طريقتين'.split(' ').forEach(w => STOP.add(w));
  // general/directory pages sink below solution & hub pages in keyword lists (they mention everything)
  const GENERAL = /\/(index|Solutions|About|Amazing_Facts|Myth_vs_Fact|Community|Contact|Press|Ways_to_Help|Find_a_Cleanup|Rawanes_Mission_Log)\.html$/;
  const keyTerms = q => [...new Set(q.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, ' ').split(/\s+/).filter(w => w.length > 2 && !STOP.has(w) && !/^\d+$/.test(w)))].slice(0, 8);

  async function keyword(q) {
    const r = await pf.search(q);
    const terms = keyTerms(q);
    // enough every-word hits (or a short query): use them. Otherwise add key-term matches after them.
    if (r.results.length >= 3 || terms.length < 2) return { partial: false, hits: r.results.slice(0, 15) };
    const exact = r.results;
    const score = new Map(), keep = new Map();
    for (const t of terms) {
      const rr = await pf.search(t);
      rr.results.slice(0, 20).forEach((x, i) => { score.set(x.id, (score.get(x.id) || 0) + 1 / (5 + i)); keep.set(x.id, x); });
    }
    const ids = new Set(exact.map(x => x.id));
    const hits = [...exact, ...[...score.entries()].sort((a, b) => b[1] - a[1]).map(([id]) => keep.get(id)).filter(x => !ids.has(x.id))].slice(0, 15);
    return { partial: hits.length > exact.length, hits };
  }

  async function run(updateUrl = true, keepShown = false) {
    const q = input.value.trim(), my = ++seq;
    if (!keepShown) shown = 0;
    if (updateUrl) { const u = new URLSearchParams(); if (topic() !== 'all') u.set('topic', topic()); if (q) u.set('q', q); const qs = u.toString(); history.replaceState(history.state, '', location.pathname + (qs ? '?' + qs : '')); }
    if (!q) { lastItems = []; paint(); list.innerHTML = ''; status.textContent = ''; if (empty) empty.hidden = !!$('sp-float')?.children.length; return; }
    const kwr = await keyword(q); await hubsReady;
    // topic tab: filtered Pagefind search over that topic's tagged math/Learn/calculator pages (meta data-pagefind-filter="topic")
    const tp = topic(); let topicHits = [];
    if (tp !== 'all') { try { topicHits = (await pf.search(q, { filters: { topic: tp } })).results.slice(0, 8); } catch (e) {} }
    if (my !== seq) return;
    const kw = await Promise.all(kwr.hits.map(x => x.data()));
    const th = await Promise.all(topicHits.map(x => x.data()));
    if (my !== seq) return;
    let items = kw.map(d => ({ url: norm(d.url), title: d.meta.title || d.url, html: d.excerpt }));
    const thItems = th.map(d => ({ url: norm(d.url), title: d.meta.title || d.url, html: d.excerpt }));
    items = [...items.filter(it => !GENERAL.test(it.url)), ...items.filter(it => GENERAL.test(it.url))];
    let usedSem = false;
    if (sem) {
      const hits = (await sem.search(q, 12)).filter(h => h.score > 0.45);
      if (my !== seq) return;
      const score = new Map(), info = new Map();
      const kwWeight = kwr.partial ? 0.6 : 1;   // partial keyword matches count less than meaning
      items.forEach((it, i) => { score.set(it.url, kwWeight / (60 + i)); info.set(it.url, it); });
      hits.forEach((h, i) => {
        score.set(h.url, (score.get(h.url) || 0) + 1.2 / (60 + i));
        if (!info.has(h.url)) info.set(h.url, { url: h.url, title: h.title, html: esc(h.desc) });
      });
      items = [...score.entries()].sort((a, b) => b[1] - a[1]).map(([u]) => info.get(u));
      usedSem = hits.length > 0;
    }
    // topic tab: that topic's Learn/math/lab/calculator pages first, the rest of the site after them (still a whole-site search)
    const boost = (window.SP_TOPIC_BOOST || {})[topic()];
    // Q&A entries whose question shares most key terms with the query; the active tab's entries go first
    const kt = keyTerms(q);
    const qaHits = kt.length ? qa.filter(e => { const w = e.q.toLowerCase(); return kt.filter(t => w.includes(t)).length >= Math.max(1, Math.ceil(kt.length / 2)); }) : [];
    if (qaHits.length) {
      const toItem = e => ({ url: norm(e.url), title: e.q, html: '' });
      const mine = qaHits.filter(e => e.tab === topic()).map(toItem), other = qaHits.filter(e => e.tab !== topic()).map(toItem);
      const qs = new Set(qaHits.map(e => norm(e.url)));
      items = items.filter(it => !qs.has(it.url));
      items = topic() !== 'all' ? [...mine, ...items.slice(0, 3), ...other, ...items.slice(3)] : [...items.slice(0, 3), ...mine, ...other, ...items.slice(3)];
    }
    if (boost) {
      const seen = new Set(thItems.map(it => it.url));
      items = [...thItems, ...items.filter(it => !seen.has(it.url))];
      const hit = it => boost.includes(base(it.url)) || (it.url.includes('Student_Questions.html') && qa.some(e => norm(e.url) === it.url && e.tab === topic()));
      items = [...items.filter(hit), ...items.filter(it => !hit(it))];
    }
    items = items.slice(0, 20);
    if (empty) empty.hidden = items.length > 0;
    lastItems = items; shown = Math.max(shown, 5);
    paint();
    status.textContent = !items.length ? msg('none')
      : items.length + ' ' + msg(items.length === 1 ? 'result' : 'results') + (kwr.partial && !usedSem ? ' · ' + msg('partial') : '');
  }
  let lastItems = [], shown = 0;
  const more = $('sp-more'), refine = $('sp-refine');
  more?.addEventListener('click', () => { shown += 5; paint(); });
  function paint() {
    const items = lastItems.slice(0, shown);
    if (more) more.hidden = lastItems.length <= shown;
    if (refine) refine.hidden = !lastItems.length;
    list.innerHTML = items.map(it => {
      const hub = hubOf.get(base(it.url));
      return `<li class="sp-card"><a href="${esc(it.url)}">${hub ? `<span class="sp-hub">${esc(hub)}</span>` : ''}<span class="sp-title">${esc(it.title.split(' | ')[0])}</span><span class="sp-excerpt">${it.html || ''}</span></a></li>`;
    }).join('');
  }

  let t = 0;
  function go() { if (!window.SP_SEARCH_ACTIVE) return; startSemantic(); clearTimeout(t); run(); }
  // no live results while typing: search runs on Enter/Search, question/chip clicks and ?q= links
  input.addEventListener('focus', () => { if (window.SP_SEARCH_ACTIVE) startSemantic(); }, { once: true }); // quiet model preload
  if (input.value.trim()) go();
})();
