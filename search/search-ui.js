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

  // Starter chips sit on the arc (build-search-page.py). After a search they become follow-up questions
  // built only from the query and the top results' titles and hubs. Clicking one runs that question.
  const arc = $('sp-float');
  const starterHTML = arc ? arc.innerHTML : '';
  arc?.addEventListener('click', e => {
    const a = e.target.closest('.sp-q');
    if (!a) return;
    e.preventDefault();
    input.value = a.textContent.trim();
    go();
    $('status')?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  });
  // approved student-question answers (search/student-qa.json from scripts/build-student-qa.py)
  const QA_T = { rocket: 'rocket', aero: 'aero', orbit: 'orbital', phys: 'physics', all: 'all' };
  let qa = [];
  fetch('/search/student-qa.json').then(r => r.ok ? r.json() : {}).then(d => { qa = (d[lang.slice(0, 2)] || []).map(e => ({ ...e, tab: QA_T[e.topic] || 'all' })); }).catch(() => {});
  const topic = () => document.documentElement.getAttribute('data-sp-topic') || 'all';
  document.addEventListener('sp-topic', () => {
    if (!arc?.classList.contains('is-live')) placeArc();
    if (input.value.trim() && window.SP_SEARCH_ACTIVE) run(false, true);
  });

  // hub/category label for each result card (search/hubs.json, built from page breadcrumbs by scripts/build-search.mjs)
  const hubOf = new Map(), hubFileOf = new Map(), hubName = new Map();
  const hubsReady = fetch('/search/hubs.json').then(r => r.json()).then(d => {
    const names = d.hubNames[lang.slice(0, 2)] || d.hubNames.en || {};
    const en = d.hubNames.en || {};
    for (const [pg, hub] of Object.entries(d.hubOf)) {
      hubFileOf.set(pg, hub);
      const label = names[hub] || en[hub] || '';
      hubName.set(pg, label);
      hubOf.set(pg, pg === hub ? msg('hub') : (label || msg('hub')));
    }
  }).catch(() => {});
  function base(u) { return (u || '').replace(/[?#].*$/, '').split('/').pop(); }
  // Oct 25 (upgrade 4): result groups. search/result-types.json (scripts/build-search-page.py): page -> solution | course | fact | mission
  let typeOf = {};
  const typesReady = fetch('/search/result-types.json').then(r => r.json()).then(d => { typeOf = d; }).catch(() => {});
  const kind = u => typeOf[base(u)] || 'page';

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
    if (!q) { lastItems = []; paint(); list.innerHTML = ''; status.textContent = ''; showStarters(); syncTeach('', []); if (empty) empty.hidden = true; return; }
    const kwr = await keyword(q); await hubsReady; await typesReady;
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
  function card(it) {
    const hub = hubOf.get(base(it.url));
    return `<li class="sp-card"><a href="${esc(it.url)}">${hub ? `<span class="sp-hub">${esc(hub)}</span>` : ''}<span class="sp-title">${esc(it.title.split(' | ')[0])}</span><span class="sp-excerpt">${it.html || ''}</span></a></li>`;
  }
  function paint() {
    const items = lastItems.slice(0, shown);
    if (more) more.hidden = lastItems.length <= shown;
    if (refine) refine.hidden = !lastItems.length;
    const qNow = input.value.trim();
    if (qNow && lastItems.length) {
      const qs = followUps(qNow, lastItems);
      if (qs.length) showFollowUps(qs); else showStarters();
    }
    syncTeach(qNow, lastItems);
    // grouped by type; groups appear in the order of their best-ranked result, ranking kept inside each group
    const groups = new Map();
    items.forEach(it => { const k = kind(it.url); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(it); });
    list.innerHTML = [...groups.entries()].map(([k, its], gi) =>
      `<li class="sp-gh"><h2 class="sp-gh-t" id="sp-g${gi}">${esc(msg('g-' + k))}</h2><ol aria-labelledby="sp-g${gi}">${its.map(card).join('')}</ol></li>`).join('');
  }

  let t = 0;
  function go() { if (!window.SP_SEARCH_ACTIVE) return; closeSugg(); startSemantic(); clearTimeout(t); run(); }
  // Oct 25 (upgrade 4): as-you-type suggestions (page titles from this language's Pagefind index), ARIA combobox.
  // Arrow keys move, Enter opens the highlighted page, Escape closes; plain Enter still runs the full search.
  const sugg = document.createElement('ul');
  sugg.id = 'sp-sugg'; sugg.className = 'sp-sugg'; sugg.setAttribute('role', 'listbox'); sugg.setAttribute('aria-label', msg('sugg')); sugg.hidden = true;
  input.after(sugg);
  input.setAttribute('role', 'combobox'); input.setAttribute('aria-autocomplete', 'list'); input.setAttribute('aria-controls', 'sp-sugg'); input.setAttribute('aria-expanded', 'false');
  let sItems = [], sIdx = -1, sSeq = 0, sT = 0;
  function closeSugg() { sugg.hidden = true; sugg.innerHTML = ''; sItems = []; sIdx = -1; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); }
  function mark() {
    [...sugg.children].forEach((li, i) => li.setAttribute('aria-selected', i === sIdx ? 'true' : 'false'));
    if (sIdx >= 0) input.setAttribute('aria-activedescendant', 'sp-s' + sIdx); else input.removeAttribute('aria-activedescendant');
  }
  async function suggest() {
    const q = input.value.trim(), my = ++sSeq;
    if (q.length < 2) return closeSugg();
    let r; try { r = await pf.search(q); } catch (e) { return; }
    const ds = await Promise.all(r.results.slice(0, 6).map(x => x.data())); await typesReady;
    if (my !== sSeq || input.value.trim() !== q || document.activeElement !== input) return;
    sItems = ds.map(d => ({ url: norm(d.url), title: (d.meta.title || d.url).split(' | ')[0] }));
    if (!sItems.length) return closeSugg();
    sugg.innerHTML = sItems.map((it, i) => `<li id="sp-s${i}" role="option" aria-selected="false" data-i="${i}">${esc(it.title)}<span class="sp-sg">${esc(msg('g-' + kind(it.url)))}</span></li>`).join('');
    sIdx = -1; mark(); sugg.hidden = false; input.setAttribute('aria-expanded', 'true');
  }
  input.addEventListener('input', () => { if (!window.SP_SEARCH_ACTIVE) return; clearTimeout(sT); sT = setTimeout(suggest, 160); });
  input.addEventListener('keydown', e => {
    if (sugg.hidden) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); sIdx = (sIdx + 1) % sItems.length; mark(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); sIdx = (sIdx - 1 + sItems.length) % sItems.length; mark(); }
    else if (e.key === 'Escape') { e.preventDefault(); closeSugg(); }
    else if (e.key === 'Enter' && sIdx >= 0) { e.preventDefault(); location.href = sItems[sIdx].url; }
  });
  sugg.addEventListener('mousedown', e => { const li = e.target.closest('li[data-i]'); if (li) { e.preventDefault(); location.href = sItems[+li.dataset.i].url; } });
  input.addEventListener('blur', () => setTimeout(closeSugg, 120));
  // no live results while typing (suggestions only): search runs on Enter/Search, question/chip clicks and ?q= links
  input.addEventListener('focus', () => { if (window.SP_SEARCH_ACTIVE) startSemantic(); }, { once: true }); // quiet model preload
  if (input.value.trim()) { syncTeach(input.value.trim(), []); go(); }
  else syncTeach('', []);
  placeArc();
  let placeT = 0;
  window.addEventListener('resize', () => { clearTimeout(placeT); placeT = setTimeout(placeArc, 80); });

function placeArc() {
  const box = document.getElementById('sp-float');
  if (!box) return;
  const chips = [...box.querySelectorAll('.sp-q')].filter(el => getComputedStyle(el).display !== 'none');
  const narrow = matchMedia('(max-width: 760px)').matches;
  const rtl = document.documentElement.dir === 'rtl';
  const n = chips.length;
  chips.forEach((c, i) => {
    if (narrow || !n) return;
    const u = n === 1 ? 0.5 : i / (n - 1);
    const t = rtl ? 1 - u : u;
    const x = (0.14 + t * 0.72) * 100;
    const y = (0.78 - Math.sin(t * Math.PI) * 0.66) * 100;
    c.style.setProperty('--x', x.toFixed(1) + '%');
    c.style.setProperty('--y', y.toFixed(1) + '%');
  });
}
function showStarters() {
  const box = document.getElementById('sp-float');
  if (!box || !box.classList.contains('is-live')) { placeArc(); return; }
  box.classList.remove('is-live');
  box.innerHTML = starterHTML;
  placeArc();
}
function showFollowUps(qs) {
  const box = document.getElementById('sp-float');
  if (!box) return;
  const topic = document.documentElement.getAttribute('data-sp-topic') || 'all';
  const pre = topic === 'all' ? '' : 'topic=' + encodeURIComponent(topic) + '&';
  box.classList.add('is-live');
  box.innerHTML = qs.map((q, i) => '<a class="sp-q sp-crystal" data-t="' + topic + '" href="?' + pre + 'q=' + encodeURIComponent(q) + '" style="--i:' + i + '">' + esc(q) + '</a>').join('');
  placeArc();
}
function dominantHub(items) {
  const counts = new Map();
  items.slice(0, 5).forEach(it => {
    const h = hubFileOf.get(base(it.url));
    if (!h) return;
    counts.set(h, (counts.get(h) || 0) + 1);
  });
  let best = '', n = 0;
  counts.forEach((c, h) => { if (c > n) { n = c; best = h; } });
  return best;
}
function syncTeach(q, items) {
  const lesson = document.getElementById('sp-lesson');
  const sheet = document.getElementById('sp-sheet');
  const hub = dominantHub(items || []);
  if (lesson) {
    const p = new URLSearchParams();
    if (q) p.set('q', q.slice(0, 180));
    if (hub) p.set('hub', hub);
    lesson.href = 'Lesson_Builder.html' + (p.toString() ? '?' + p : '');
  }
  if (sheet) {
    let heads = {};
    try { heads = JSON.parse(document.getElementById('sp-sheet-hubs').textContent); } catch (e) {}
    const name = hub && heads[hub];
    sheet.href = name ? 'Teachers.html#:~:text=' + encodeURIComponent(name) : 'Teachers.html';
  }
}
const PURPOSE = {
  en: /\bto\s+(.{8,90})$/i,
  fr: /\bpour\s+(.{8,90})$/i,
  es: /\bpara\s+(.{8,90})$/i,
  it: /\bper\s+(.{8,90})$/i,
  ar: /(?:لكي|من أجل)\s+(.{6,90})$/,
  he: /(?:כדי|על מנת)\s+(.{6,90})$/
};
const LEAD_Q = /^(what|how|which|who|why|when|where|can|could|should|do|does|que|quoi|comment|pourquoi|cómo|como|qué|cual|cuál|come|cosa|perché|perche|ما|ماذا|كيف|لماذا|هل|מה|איך|למה|אילו)\b/i;
function focusPhrase(q) {
  const langKey = (document.documentElement.lang || 'en').slice(0, 2);
  let s = String(q || '').replace(/[?؟]+/g, '').replace(/\s+/g, ' ').trim();
  if (langKey === 'ar') {
    const ar = s.match(/(?:^|\s)(ل[إأا]\S+(?:\s+\S+){0,5})/);
    if (ar) return ar[1].trim();
  }
  const m = s.match(PURPOSE[langKey] || PURPOSE.en);
  if (m) return m[1].trim();
  let guard = 0;
  while (LEAD_Q.test(s) && guard++ < 4) s = s.replace(LEAD_Q, '').trim();
  const words = s.split(' ').filter(Boolean);
  if (words.length > 10) s = words.slice(-8).join(' ');
  return s.trim();
}
function cleanTitle(t) {
  return String(t || '').split(' | ')[0].split(' – ')[0].replace(/\s+/g, ' ').trim();
}
const FOLLOW = {
  en: [
    c => c.title ? 'What does ' + c.title + ' add to this question?' : '',
    c => c.hub && c.focus ? 'Which ' + c.hub + ' pages should we open next for “' + c.focus + '”?' : '',
    c => c.title && c.focus ? 'How does ' + c.title + ' connect with “' + c.focus + '”?' : '',
    c => c.hub && c.focus ? 'Which other ' + c.hub + ' pages fit “' + c.focus + '”?' : '',
    c => c.focus ? 'What should we ask next about “' + c.focus + '”?' : ''
  ],
  fr: [
    c => c.title ? 'Qu’ajoute ' + c.title + ' à cette question ?' : '',
    c => c.hub && c.focus ? 'Quelles pages ' + c.hub + ' ouvrir ensuite pour « ' + c.focus + ' » ?' : '',
    c => c.title && c.focus ? 'Comment ' + c.title + ' se relie-t-il à « ' + c.focus + ' » ?' : '',
    c => c.hub && c.focus ? 'Quelles autres pages ' + c.hub + ' vont avec « ' + c.focus + ' » ?' : '',
    c => c.focus ? 'Que demander ensuite à propos de « ' + c.focus + ' » ?' : ''
  ],
  es: [
    c => c.title ? '¿Qué añade ' + c.title + ' a esta pregunta?' : '',
    c => c.hub && c.focus ? '¿Qué páginas de ' + c.hub + ' abrimos después sobre «' + c.focus + '»?' : '',
    c => c.title && c.focus ? '¿Cómo se conecta ' + c.title + ' con «' + c.focus + '»?' : '',
    c => c.hub && c.focus ? '¿Qué otras páginas de ' + c.hub + ' encajan con «' + c.focus + '»?' : '',
    c => c.focus ? '¿Qué más conviene preguntar sobre «' + c.focus + '»?' : ''
  ],
  ar: [
    c => c.title ? 'ماذا تضيف ' + c.title + ' إلى هذا السؤال؟' : '',
    c => c.hub && c.focus ? 'أي صفحات ' + c.hub + ' نفتح بعد ذلك عن «' + c.focus + '»؟' : '',
    c => c.title && c.focus ? 'كيف تتصل ' + c.title + ' بـ«' + c.focus + '»؟' : '',
    c => c.hub && c.focus ? 'أي صفحات أخرى في ' + c.hub + ' تناسب «' + c.focus + '»؟' : '',
    c => c.focus ? 'ماذا نسأل بعد ذلك عن «' + c.focus + '»؟' : ''
  ],
  it: [
    c => c.title ? 'Che cosa aggiunge ' + c.title + ' a questa domanda?' : '',
    c => c.hub && c.focus ? 'Quali pagine di ' + c.hub + ' apriamo dopo su «' + c.focus + '»?' : '',
    c => c.title && c.focus ? 'Come si collega ' + c.title + ' a «' + c.focus + '»?' : '',
    c => c.hub && c.focus ? 'Quali altre pagine di ' + c.hub + ' c’entrano con «' + c.focus + '»?' : '',
    c => c.focus ? 'Che cosa chiedere dopo su «' + c.focus + '»?' : ''
  ],
  he: [
    c => c.title ? 'מה מוסיף ' + c.title + ' לשאלה הזו?' : '',
    c => c.hub && c.focus ? 'אילו עמודים ב' + c.hub + ' לפתוח אחר כך על „' + c.focus + '”?' : '',
    c => c.title && c.focus ? 'איך ' + c.title + ' מתקשר ל„' + c.focus + '”?' : '',
    c => c.hub && c.focus ? 'אילו עמודים נוספים ב' + c.hub + ' מתאימים ל„' + c.focus + '”?' : '',
    c => c.focus ? 'מה כדאי לשאול אחר כך על „' + c.focus + '”?' : ''
  ]
};
function followUps(q, items) {
  const langKey = (document.documentElement.lang || 'en').slice(0, 2);
  const frames = FOLLOW[langKey] || FOLLOW.en;
  const focus = focusPhrase(q);
  const out = [], seen = new Set([q.trim().toLowerCase()]);
  function add(s) {
    s = String(s || '').replace(/\s+/g, ' ').trim();
    if (!s) return;
    if (!/[?؟]$/.test(s)) s += '?';
    const k = s.toLowerCase();
    if (k === q.trim().toLowerCase() || seen.has(k) || s.length > 180) return;
    seen.add(k);
    out.push(s);
  }
  items.slice(0, 4).forEach((it, i) => {
    const ctx = { title: cleanTitle(it.title), hub: hubName.get(base(it.url)) || '', focus: focus };
    for (let k = 0; k < frames.length && out.length < 5; k++) {
      const before = out.length;
      add(frames[(i + k) % frames.length](ctx));
      if (out.length > before) break;
    }
  });
  if (out.length < 3) add(frames[frames.length - 1]({ title: '', hub: '', focus: focus }));
  return out.slice(0, 5);
}
})();
