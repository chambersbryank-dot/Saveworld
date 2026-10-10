(function () {
  var root = document.documentElement;
  var saved = localStorage.getItem('sp-theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    root.classList.add('dark');
  }
  var toggle = document.getElementById('theme-toggle');
  function paint() {
    if (toggle) toggle.textContent = root.classList.contains('dark') ? 'Light' : 'Dark';
  }
  paint();
  if (toggle) {
    toggle.addEventListener('click', function () {
      root.classList.toggle('dark');
      localStorage.setItem('sp-theme', root.classList.contains('dark') ? 'dark' : 'light');
      paint();
    });
  }
  var nav = document.getElementById('topnav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    });
  }
  var dropdown = document.querySelector('.nav-dropdown');
  var dropToggle = document.querySelector('.dropdown-toggle');
  if (dropdown && dropToggle) {
    dropToggle.addEventListener('click', function (e) {
      e.preventDefault();
      dropdown.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
    });
  }
  var navToggle = document.querySelector('.nav-toggle');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) {
        nav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
  if ('scrollBehavior' in document.documentElement.style) {
    document.documentElement.style.scrollBehavior = 'smooth';
  }
})();
/* Mission status widget: renders any [data-mission] element from data attributes
   data-launch / data-arrival (ISO dates), data-status, data-milestones ("ISO|label;ISO|label"),
   data-news (search term for Spaceflight News API v4), data-source / data-source-label. */
(function () {
  var els = document.querySelectorAll('[data-mission]');
  if (!els.length) return;
  var NEWS_MS = 3600000;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmt(iso) { var d = new Date(iso); return isNaN(d) ? '' : d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' }); }
  function count(iso) {
    var diff = new Date(iso).getTime() - Date.now();
    if (isNaN(diff)) return '';
    if (diff <= 0) return 'Reached';
    var s = Math.floor(diff / 1000), d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
    return d + 'd ' + h + 'h ' + m + 'm ' + x + 's';
  }
  function renderNews(box, items) {
    if (!items || !items.length) { box.innerHTML = '<li>News is unavailable right now.</li>'; return; }
    box.innerHTML = items.map(function (a) {
      var u = /^https?:\/\//.test(a.url) ? a.url : '#';
      return '<li><a href="' + esc(u) + '" target="_blank" rel="noreferrer">' + esc(a.title) + '</a> <span class="mw-date">' + esc(fmt(a.published_at)) + '</span></li>';
    }).join('');
  }
  Array.prototype.forEach.call(els, function (el) {
    var ds = el.dataset, key = 'mw-news-' + (ds.news || ds.mission);
    var ms = (ds.milestones || '').split(';').filter(Boolean).map(function (m) { var p = m.split('|'); return { d: p[0], l: p[1] || '' }; });
    el.innerHTML = '<h2>' + esc(ds.mission) + ': mission status</h2>' +
      (ds.status ? '<p class="mw-status">' + esc(ds.status) + '</p>' : '') +
      '<div class="mw-grid">' +
      (ds.launch ? '<div class="mw-count"><small>Launch (' + esc(fmt(ds.launch)) + ')</small><b data-t="' + esc(ds.launch) + '"></b></div>' : '') +
      (ds.arrival ? '<div class="mw-count"><small>Arrival (' + esc(ds.arrivalLabel || fmt(ds.arrival)) + ')</small><b data-t="' + esc(ds.arrival) + '"></b></div>' : '') +
      '</div>' +
      (ms.length ? '<h3>Milestones</h3><ul class="mw-milestones">' + ms.map(function (m) { var past = new Date(m.d).getTime() < Date.now(); return '<li class="' + (past ? 'done' : '') + '"><span class="mw-date">' + esc(fmt(m.d)) + '</span> ' + esc(m.l) + '</li>'; }).join('') + '</ul>' : '') +
      (ds.news ? '<h3>Latest news</h3><ul class="mw-news"><li>Loading…</li></ul>' : '') +
      '<p class="mw-note">Dates per ' + esc(ds.agency || 'NASA') + '; missions shift.' + (ds.source ? ' <a href="' + esc(ds.source) + '" target="_blank" rel="noreferrer">Source: ' + esc(ds.sourceLabel || 'NASA') + '</a>' : '') + '</p>';
    var counters = el.querySelectorAll('[data-t]');
    function tick() { Array.prototype.forEach.call(counters, function (c) { c.textContent = count(c.getAttribute('data-t')); }); }
    tick(); setInterval(tick, 1000);
    if (!ds.news) return;
    var box = el.querySelector('.mw-news'), cached = null;
    try { cached = JSON.parse(localStorage.getItem(key)); } catch (e) {}
    if (cached && cached.items) renderNews(box, cached.items);
    if (cached && Date.now() - cached.t < NEWS_MS) return;
    fetch('https://api.spaceflightnewsapi.net/v4/articles/?search=' + encodeURIComponent(ds.news) + '&limit=3')
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var items = (d.results || []).map(function (a) { return { title: a.title, url: a.url, published_at: a.published_at }; });
        if (!items.length) throw new Error('empty');
        try { localStorage.setItem(key, JSON.stringify({ t: Date.now(), items: items })); } catch (e) {}
        renderNews(box, items);
      })
      .catch(function () { if (!(cached && cached.items)) renderNews(box, []); });
  });
})();
