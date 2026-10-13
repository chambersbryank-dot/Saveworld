/* Saving Planets hybrid search UI (Search.html).
 * 1) Pagefind keyword results appear instantly (all four languages).
 * 2) On English pages the semantic layer (search/semantic.js) loads in the background;
 *    once ready, results are re-ranked by reciprocal-rank fusion of keyword + meaning.
 * If Pagefind cannot load, the page's built-in list search keeps working (fallback). */
(async function () {
  const input = document.getElementById('q'), list = document.getElementById('results'), status = document.getElementById('status');
  const note = document.getElementById('search-mode');
  if (!input || !list) return;
  const lang = document.documentElement.lang || 'en';
  let pf;
  try { pf = await import('/pagefind/pagefind.js'); await pf.options({ baseUrl: '/' }); pf.init(); }
  catch (e) { console.info('Pagefind unavailable, using built-in list search', e); return; }
  window.SP_SEARCH_ACTIVE = true;

  let sem = null, semLoading = null, seq = 0;
  const semantic = await import('/search/semantic.js').catch(() => null);
  function startSemantic() {
    if (semLoading || !semantic || !semantic.supports(lang)) return;
    if (note) note.textContent = 'Keyword results now · smart (meaning-based) results loading…';
    semLoading = semantic.load().then(e => { sem = e; if (note) note.textContent = 'Smart search on: keyword + meaning-based results, computed in your browser.'; run(); })
      .catch(e => { console.info('Semantic layer unavailable', e); if (note) note.textContent = ''; });
  }

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = u => u.replace(/^https?:\/\/[^/]+/, '').replace(/[?#].*$/, '');

  async function run() {
    const q = input.value.trim(), my = ++seq;
    if (!q) { list.innerHTML = ''; if (status) status.textContent = ''; return; }
    const r = await pf.debouncedSearch(q, {}, 120);
    if (r === null || my !== seq) return;
    const kw = await Promise.all(r.results.slice(0, 15).map(x => x.data()));
    let items = kw.map(d => ({ url: norm(d.url), title: d.meta.title || d.url, html: d.excerpt }));
    if (sem) {
      const hits = (await sem.search(q, 12)).filter(h => h.score > 0.45);
      if (my !== seq) return;
      const score = new Map(), info = new Map();
      items.forEach((it, i) => { score.set(it.url, 1 / (60 + i)); info.set(it.url, it); });
      hits.forEach((h, i) => {
        score.set(h.url, (score.get(h.url) || 0) + 1.2 / (60 + i));
        if (!info.has(h.url)) info.set(h.url, { url: h.url, title: h.title, html: esc(h.desc) });
      });
      items = [...score.entries()].sort((a, b) => b[1] - a[1]).map(([u]) => info.get(u));
    }
    items = items.slice(0, 15);
    list.innerHTML = items.map(it => `<li><a href="${esc(it.url)}">${esc(it.title)}</a><span class="match">${it.html || ''}</span></li>`).join('');
    if (status) status.textContent = items.length ? items.length + ' result' + (items.length === 1 ? '' : 's') : 'No matches for "' + q + '"';
  }

  input.addEventListener('input', () => { startSemantic(); run(); });
  if (input.value.trim()) { startSemantic(); run(); }
})();
