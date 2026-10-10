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
  var dropdowns = Array.prototype.slice.call(document.querySelectorAll('.nav-dropdown'));
  function closeDrop(d) { d.classList.remove('open'); var t = d.querySelector('.dropdown-toggle'); if (t) t.setAttribute('aria-expanded', 'false'); }
  dropdowns.forEach(function (dd) {
    var t = dd.querySelector('.dropdown-toggle');
    if (!t) return;
    t.setAttribute('aria-haspopup', 'true');
    t.setAttribute('aria-expanded', 'false');
    t.addEventListener('click', function (e) {
      e.preventDefault();
      var open = !dd.classList.contains('open');
      dropdowns.forEach(closeDrop);
      if (open) { dd.classList.add('open'); t.setAttribute('aria-expanded', 'true'); }
    });
    dd.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeDrop(dd); t.focus(); } });
  });
  document.addEventListener('click', function (e) {
    dropdowns.forEach(function (dd) { if (!dd.contains(e.target)) closeDrop(dd); });
  });
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

/* Stats engine: renders the homepage overview ([data-site-stats]) and contextual
   .page-stats blocks from assets/data/solutions.json (generated by build-stats.js).
   One fetch per session (sessionStorage); on failure the blocks stay hidden and the
   homepage keeps its static numbers. */
(function () {
  var site = document.querySelector('[data-site-stats]');
  var blocks = document.querySelectorAll('.page-stats[data-stats-category]');
  if (!site && !blocks.length) return;
  var KEY = 'sp-solutions-v2';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function num(n) { return typeof n === 'number' ? n.toLocaleString('en-US') : esc(n); }
  function plural(n, a, b) { return num(n) + ' ' + (n === 1 ? a : b); }
  function cls(by) {
    var names = { agency: 'agency', corporate: 'corporate', nonprofit: 'nonprofit', natural: 'natural' };
    return Object.keys(names).filter(function (k) { return by[k]; }).map(function (k) { return by[k] + ' ' + names[k]; }).join(' · ');
  }
  function solLine(a) { return plural(a.solutions, 'active solution', 'active solutions') + (a.horizon ? ', ' + a.horizon + ' on the horizon' : ''); }
  function updated(d) { var t = new Date(d.generated); return isNaN(t) ? '' : t.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }); }
  function render(d) {
    if (site) {
      var s = d.site;
      site.innerHTML = '<div class="stat-row">' +
        '<div class="stat"><span class="stat-number">' + num(s.solutions) + '</span><span class="stat-label">active solutions featured' + (s.horizon ? ' (+' + s.horizon + ' on the horizon)' : '') + '</span></div>' +
        '<div class="stat"><span class="stat-number">' + num(s.hubs) + '</span><span class="stat-label">hubs across ' + num(s.categories) + ' categories</span></div>' +
        '<div class="stat"><span class="stat-number">' + num(s.upcomingMissions) + '</span><span class="stat-label">upcoming space missions we track live</span></div>' +
        '<div class="stat"><span class="stat-number">' + num((s.byClassification.natural || 0)) + '</span><span class="stat-label">natural solutions, alongside ' + cls(Object.keys(s.byClassification).reduce(function (o, k) { if (k !== 'natural') o[k] = s.byClassification[k]; return o; }, {})) + '</span></div>' +
        '</div>' + ((s.impactTotals || []).length ? '<div class="stat-row impact-totals">' + s.impactTotals.map(function (t) { return '<div class="stat"><span class="stat-number">' + num(t.total) + ' ' + esc(t.unit) + '</span><span class="stat-label">combined across ' + plural(t.pages.length, 'solution', 'solutions') + ', each figure sourced on its page</span></div>'; }).join('') + '</div>' : '') +
        '<p class="stat-source">Last updated ' + esc(updated(d)) + '. Counts are generated from every solution page on this site.</p>';
      site.hidden = false;
    }
    Array.prototype.forEach.call(blocks, function (el) {
      var c = d.categories[el.getAttribute('data-stats-category')];
      if (!c) return;
      var page = null, url = el.getAttribute('data-stats-page');
      d.pages.forEach(function (p) { if (p.url === url && !p.section) page = p; });
      var html = '<h2>By the numbers</h2><div class="ps-grid">' +
        '<div class="ps-card"><h3>' + esc(c.name) + '</h3><p>' + solLine(c) + (cls(c.byClassification) ? '<br><small>' + esc(cls(c.byClassification)) + '</small>' : '') + '</p>' +
        (c.upcomingMissions ? '<p>' + plural(c.upcomingMissions, 'upcoming mission', 'upcoming missions') + '</p>' : '') +
        c.impactTotals.map(function (t) { return '<p>' + num(t.total) + ' ' + esc(t.unit) + ' <small>combined, from sourced page figures</small></p>'; }).join('') + '</div>' +
        '<div class="ps-card"><h3>Site-wide</h3><p>' + solLine(d.site) + '</p><p>' + plural(d.site.hubs, 'hub', 'hubs') + ' · ' + plural(d.site.upcomingMissions, 'upcoming mission', 'upcoming missions') + '</p></div>';
      if (page && page.stats.length) {
        html += '<div class="ps-card"><h3>This page</h3>' + page.stats.map(function (s) {
          var u = /^https?:\/\//.test(s.sourceUrl) ? s.sourceUrl : '';
          return '<p><b>' + num(s.value) + '</b> ' + esc(s.unit) + '<br><small>' + esc(s.label) + (u ? ' · <a href="' + esc(u) + '" target="_blank" rel="noreferrer">source</a>' : '') + '</small></p>';
        }).join('') + '</div>';
      }
      el.innerHTML = html + '</div><p class="ps-note">Updated ' + esc(updated(d)) + '. Generated from every solution page on Saving Planets.</p>';
      el.hidden = false;
    });
  }
  var cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) {}
  if (cached && cached.site) { render(cached); return; }
  fetch('assets/data/solutions.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) { try { sessionStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} render(d); })
    .catch(function () { /* keep blocks hidden; homepage keeps its static numbers */ });
})();
