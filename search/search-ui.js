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
  // GA4 'search' event (gtag + Consent Mode already on every page); sent on submit and on question/example clicks
  const track = q => { try { if (q && window.gtag) window.gtag('event', 'search', { search_term: q.slice(0, 100) }); } catch (e) { /* ignore */ } };
  input.closest('form')?.addEventListener('submit', e => { e.preventDefault(); input.blur(); track(input.value.trim()); go(); });

  // floating example questions (search/featured-questions.json, per language)
  fetch('/search/featured-questions.json').then(r => r.json()).then(d => {
    const box = $('sp-float'); const qs = (d[lang.slice(0, 2)] || d.en || []).slice(0, 12); if (!box) return;
    const chip = (q, i, dup) => `<a class="sp-q sp-q${i}" href="?q=${encodeURIComponent(q)}" style="--i:${i}"${dup ? ' aria-hidden="true" tabindex="-1"' : ''}>${esc(q)}</a>`;
    // second copy is only for the seamless marquee on narrow screens (hidden on desktop and for screen readers)
    box.innerHTML = `<div class="sp-track">${qs.map((q, i) => chip(q, i)).join('')}<span class="sp-dup">${qs.map((q, i) => chip(q, i, true)).join('')}</span></div>`;
    if (qs.length && empty && !input.value.trim()) empty.hidden = true; // floating questions replace the starter chips
    box.querySelectorAll('a').forEach(a => a.addEventListener('click', e => {
      e.preventDefault(); input.value = a.textContent; track(a.textContent); go();
      $('status')?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    }));
  }).catch(() => {});

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
  const keyTerms = q => [...new Set(q.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, ' ').split(/\s+/).filter(w => w.length > 2 && !STOP.has(w) && !/^\d+$/.test(w)))].slice(0, 8);

  async function keyword(q) {
    const r = await pf.search(q);
    if (r.results.length) return { partial: false, hits: r.results.slice(0, 15) };
    const terms = keyTerms(q);
    if (terms.length < 2) return { partial: false, hits: [] };
    const score = new Map(), keep = new Map();
    for (const t of terms) {
      const rr = await pf.search(t);
      rr.results.slice(0, 20).forEach((x, i) => { score.set(x.id, (score.get(x.id) || 0) + 1 / (5 + i)); keep.set(x.id, x); });
    }
    const hits = [...score.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15).map(([id]) => keep.get(id));
    return { partial: hits.length > 0, hits };
  }

  async function run(updateUrl = true, keepShown = false) {
    const q = input.value.trim(), my = ++seq;
    if (!keepShown) shown = 0;
    if (updateUrl) history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname);
    if (!q) { lastItems = []; paint(); list.innerHTML = ''; status.textContent = ''; if (empty) empty.hidden = !!$('sp-float')?.children.length; return; }
    const kwr = await keyword(q); await hubsReady;
    if (my !== seq) return;
    const kw = await Promise.all(kwr.hits.map(x => x.data()));
    let items = kw.map(d => ({ url: norm(d.url), title: d.meta.title || d.url, html: d.excerpt }));
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
