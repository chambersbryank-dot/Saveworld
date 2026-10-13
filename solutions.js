/* Solutions directory search: filters the cards on this page.
   1) instant keyword match over each card's text; 2) semantic re-rank via /search/semantic.js (English only, replaceable module). Supports ?q= */
const input = document.getElementById('sol-q'), status = document.getElementById('sol-status');
const main = document.getElementById('directory'), empty = document.querySelector('.sol-empty');
const intro = document.querySelector('.sol-intro');
const hubs = [...document.querySelectorAll('.sol-hub')];
const cards = [...document.querySelectorAll('.sol-card')];
const lang = (document.documentElement.lang || 'en').slice(0, 2);
const tx = s => (window.spT ? window.spT(s) : s);
const norm = s => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const STOP = new Set('a an and the of to in on for with my me i is are how what that this ways near from by about or at be can do'.split(' '));
const data = cards.map(c => ({ el: c, url: c.dataset.url, text: norm(c.textContent), title: norm(c.querySelector('h3').textContent), hub: c.closest('.sol-hub') }));
const order = new Map(hubs.map((h, i) => [h, i]));
hubs.forEach(h => [...h.querySelectorAll('.sol-card')].forEach((c, i) => c.dataset.i = i));
let engine = null, loading = null, seq = 0, sem = null;

function keyword(q) {
  const terms = norm(q).split(/[^\p{L}\p{N}]+/u).filter(t => t.length > 1 && !STOP.has(t));
  const out = new Map(); if (!terms.length) return out;
  for (const d of data) {
    let s = 0;
    for (const t of terms) { const st = t.length > 4 ? t.slice(0, t.length - 1) : t; if (d.title.includes(st)) s += 2; else if (d.text.includes(st)) s += 1; }
    const v = s / (terms.length * 2);
    if (s && (terms.length < 3 || v >= 0.34)) out.set(d.el, v);
  }
  return out;
}
function render(q, scores) {
  if (!q) {
    cards.forEach(c => { c.hidden = false; c.style.order = ''; }); hubs.forEach(h => { h.hidden = false; h.style.order = ''; });
    empty.hidden = true; intro.hidden = false; status.textContent = ''; return;
  }
  intro.hidden = true;
  const best = new Map(); let n = 0; const seen = new Set();
  for (const d of data) {
    const s = scores.get(d.el); d.el.hidden = s === undefined;
    d.el.style.order = s === undefined ? '' : String(Math.round((1 - s) * 1000));
    if (s !== undefined) { if (!seen.has(d.url)) { seen.add(d.url); n++; } best.set(d.hub, Math.max(best.get(d.hub) || 0, s)); }
  }
  main.style.display = 'flex'; main.style.flexDirection = 'column';
  hubs.forEach(h => { h.hidden = !best.has(h); h.style.order = best.has(h) ? String(Math.round((1 - best.get(h)) * 1000) * 100 + order.get(h)) : ''; });
  empty.style.order = '-1'; empty.hidden = n > 0;
  status.textContent = n ? `${n} ${tx(n === 1 ? 'solution' : 'solutions')}` + (sem ? ' · ' + tx('matched by meaning') : '') : '';
}
async function semantic(q) {
  if (lang !== 'en') return null;
  try {
    if (!engine) { loading = loading || import('/search/semantic.js').then(m => m.load({ base: '/search/' })); engine = await loading; }
    const res = await engine.search(q, 40);
    const top = res.length ? res[0].score : 0, cut = Math.max(0.6, top - 0.1), m = new Map();
    res.forEach(r => { if (r.score >= cut) m.set(r.url.replace(/^\//, ''), r.score); });
    return m;
  } catch (e) { console.warn('semantic search unavailable', e); return null; }
}
async function run(push = true) {
  const q = input.value.trim(), my = ++seq; sem = null;
  if (push) { const u = new URL(location.href); q ? u.searchParams.set('q', q) : u.searchParams.delete('q'); history.replaceState(null, '', u); }
  const kw = keyword(q); render(q, kw);
  if (!q) return;
  if (lang === 'en' && !engine) status.textContent += (status.textContent ? ' · ' : '') + tx('Smart results loading…');
  const m = await semantic(q); if (my !== seq || !m) { if (my === seq) render(q, kw); return; }
  sem = m; const merged = new Map();
  for (const d of data) {
    const s = m.get(d.url), k = kw.get(d.el);
    if (s !== undefined) merged.set(d.el, s + (k || 0) * 0.15); else if (k >= 0.75) merged.set(d.el, 0.55 + k * 0.15);
  }
  const vals = [...merged.values()], hi = Math.max(...vals, 1e-9);
  merged.forEach((v, k) => merged.set(k, v / hi));
  render(q, merged);
}
let t; input.addEventListener('input', () => { clearTimeout(t); t = setTimeout(run, 250); });
input.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); clearTimeout(t); run(); } });
document.querySelectorAll('.sol-chip').forEach(b => b.addEventListener('click', () => { input.value = b.textContent; run(); input.focus(); }));
const q0 = new URLSearchParams(location.search).get('q'); if (q0) { input.value = q0; run(false); }
