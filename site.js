/* i18n strings for script-drawn UI (translated pages set <html lang="fr|es|ar|it">). Keys are the English text. */
(function () {
  var L = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  var S = {
    fr: { 'Ocean': 'Océan', 'Lakes': 'Lacs', 'Rivers': 'Rivières', 'Forests': 'Forêts', 'Space': 'Espace', 'Planetary Defense': 'Défense planétaire', 'Space Weather & Shields': 'Météo spatiale et boucliers', 'Earth Observation': 'Observation de la Terre', 'Project Rawane': 'Projet Rawane', 'Mission Status': 'état de la mission', 'Reached': 'Atteint', 'News is unavailable right now.': 'Actualités indisponibles pour le moment.', 'Launch': 'Lancement', 'Arrival': 'Arrivée', 'Milestones': 'Étapes clés', 'Latest News': 'Dernières actualités', 'Loading…': 'Chargement…', 'Dates per': 'Dates selon', 'missions shift.': 'les missions évoluent.', 'Source:': 'Source :',
      'active solution': 'solution active', 'active solutions': 'solutions actives', 'on the horizon': 'à l\u2019horizon', 'active solutions featured': 'solutions actives présentées', 'hubs across': 'hubs dans', 'categories': 'catégories', 'upcoming space missions we track live': 'missions spatiales à venir suivies en direct', 'natural solutions, alongside': 'solutions naturelles, ainsi que', 'combined across': 'cumulés sur', 'solution': 'solution', 'solutions': 'solutions', 'each figure sourced on its page': 'chaque chiffre sourcé sur sa page', 'Last updated': 'Dernière mise à jour :', 'Counts are generated from every solution page on this site.': 'Les totaux sont générés à partir de chaque page de solution du site.', 'By the Numbers': 'En chiffres', 'upcoming mission': 'mission à venir', 'upcoming missions': 'missions à venir', 'combined, from sourced page figures': 'cumulés, à partir des chiffres sourcés des pages', 'Site-Wide': 'Sur tout le site', 'hub': 'hub', 'hubs': 'hubs', 'This Page': 'Cette page', 'source': 'source', 'Updated': 'Mis à jour le', 'Generated from every solution page on Saving Planets.': 'Généré à partir de chaque page de solution de Saving Planets.', 'government': 'gouvernement', 'other': 'autre', 'agency': 'agence', 'corporate': 'entreprise', 'nonprofit': 'association', 'natural': 'naturelle' },
    es: { 'Ocean': 'Océano', 'Lakes': 'Lagos', 'Rivers': 'Ríos', 'Forests': 'Bosques', 'Space': 'Espacio', 'Planetary Defense': 'Defensa planetaria', 'Space Weather & Shields': 'Clima espacial y escudos', 'Earth Observation': 'Observación de la Tierra', 'Project Rawane': 'Proyecto Rawane', 'Mission Status': 'estado de la misión', 'Reached': 'Alcanzado', 'News is unavailable right now.': 'Noticias no disponibles por ahora.', 'Launch': 'Lanzamiento', 'Arrival': 'Llegada', 'Milestones': 'Hitos', 'Latest News': 'Últimas noticias', 'Loading…': 'Cargando…', 'Dates per': 'Fechas según', 'missions shift.': 'las misiones cambian.', 'Source:': 'Fuente:',
      'active solution': 'solución activa', 'active solutions': 'soluciones activas', 'on the horizon': 'en el horizonte', 'active solutions featured': 'soluciones activas destacadas', 'hubs across': 'centros en', 'categories': 'categorías', 'upcoming space missions we track live': 'próximas misiones espaciales que seguimos en vivo', 'natural solutions, alongside': 'soluciones naturales, junto a', 'combined across': 'en conjunto entre', 'solution': 'solución', 'solutions': 'soluciones', 'each figure sourced on its page': 'cada cifra con fuente en su página', 'Last updated': 'Última actualización:', 'Counts are generated from every solution page on this site.': 'Los recuentos se generan a partir de cada página de solución del sitio.', 'By the Numbers': 'En cifras', 'upcoming mission': 'próxima misión', 'upcoming missions': 'próximas misiones', 'combined, from sourced page figures': 'en conjunto, a partir de cifras con fuente', 'Site-Wide': 'Todo el sitio', 'hub': 'centro', 'hubs': 'centros', 'This Page': 'Esta página', 'source': 'fuente', 'Updated': 'Actualizado el', 'Generated from every solution page on Saving Planets.': 'Generado a partir de cada página de solución de Saving Planets.', 'government': 'gobierno', 'other': 'otro', 'agency': 'agencia', 'corporate': 'empresa', 'nonprofit': 'sin ánimo de lucro', 'natural': 'natural' },
    ar: { 'Ocean': 'المحيط', 'Lakes': 'البحيرات', 'Rivers': 'الأنهار', 'Forests': 'الغابات', 'Space': 'الفضاء', 'Planetary Defense': 'الدفاع الكوكبي', 'Space Weather & Shields': 'الطقس الفضائي والدروع', 'Earth Observation': 'رصد الأرض', 'Project Rawane': 'مشروع Rawane', 'Mission Status': 'حالة المهمة', 'Reached': 'تحقّق', 'News is unavailable right now.': 'الأخبار غير متاحة حاليًا.', 'Launch': 'الإطلاق', 'Arrival': 'الوصول', 'Milestones': 'المحطات الرئيسية', 'Latest News': 'آخر الأخبار', 'Loading…': 'جارٍ التحميل…', 'Dates per': 'التواريخ وفق', 'missions shift.': 'والمواعيد قابلة للتغيّر.', 'Source:': 'المصدر:',
      'active solution': 'حل نشط', 'active solutions': 'حلول نشطة', 'on the horizon': 'في الأفق', 'active solutions featured': 'حلًا نشطًا معروضًا', 'hubs across': 'محاور ضمن', 'categories': 'فئات', 'upcoming space missions we track live': 'مهمة فضائية قادمة نتابعها مباشرة', 'natural solutions, alongside': 'حلول طبيعية، إلى جانب', 'combined across': 'مجموع عبر', 'solution': 'حل', 'solutions': 'حلول', 'each figure sourced on its page': 'كل رقم موثّق في صفحته', 'Last updated': 'آخر تحديث:', 'Counts are generated from every solution page on this site.': 'تُحسب الأعداد من كل صفحات الحلول في الموقع.', 'By the Numbers': 'بالأرقام', 'upcoming mission': 'مهمة قادمة', 'upcoming missions': 'مهام قادمة', 'combined, from sourced page figures': 'مجموع من الأرقام الموثّقة في الصفحات', 'Site-Wide': 'على مستوى الموقع', 'hub': 'محور', 'hubs': 'محاور', 'This Page': 'هذه الصفحة', 'source': 'المصدر', 'Updated': 'حُدّث في', 'Generated from every solution page on Saving Planets.': 'مُولَّد من كل صفحات الحلول في Saving Planets.', 'government': 'حكومة', 'other': 'أخرى', 'agency': 'وكالة', 'corporate': 'شركة', 'nonprofit': 'منظمة غير ربحية', 'natural': 'طبيعي' },
    it: { 'Ocean': 'Oceano', 'Lakes': 'Laghi', 'Rivers': 'Fiumi', 'Forests': 'Foreste', 'Space': 'Spazio', 'Planetary Defense': 'Difesa planetaria', 'Space Weather & Shields': 'Meteo spaziale e scudi', 'Earth Observation': 'Osservazione della Terra', 'Project Rawane': 'Progetto Rawane', 'Mission Status': 'stato della missione', 'Reached': 'Raggiunto', 'News is unavailable right now.': 'Notizie non disponibili al momento.', 'Launch': 'Lancio', 'Arrival': 'Arrivo', 'Milestones': 'Tappe principali', 'Latest News': 'Ultime notizie', 'Loading…': 'Caricamento…', 'Dates per': 'Date secondo', 'missions shift.': 'le missioni possono cambiare.', 'Source:': 'Fonte:',
      'active solution': 'soluzione attiva', 'active solutions': 'soluzioni attive', 'on the horizon': 'all\u2019orizzonte', 'active solutions featured': 'soluzioni attive presentate', 'hubs across': 'hub in', 'categories': 'categorie', 'upcoming space missions we track live': 'missioni spaziali in arrivo seguite in diretta', 'natural solutions, alongside': 'soluzioni naturali, insieme a', 'combined across': 'in totale su', 'solution': 'soluzione', 'solutions': 'soluzioni', 'each figure sourced on its page': 'ogni cifra con fonte nella sua pagina', 'Last updated': 'Ultimo aggiornamento:', 'Counts are generated from every solution page on this site.': 'I totali sono generati da ogni pagina di soluzione del sito.', 'By the Numbers': 'In cifre', 'upcoming mission': 'missione in arrivo', 'upcoming missions': 'missioni in arrivo', 'combined, from sourced page figures': 'in totale, dalle cifre con fonte delle pagine', 'Site-Wide': 'Su tutto il sito', 'hub': 'hub', 'hubs': 'hub', 'This Page': 'Questa pagina', 'source': 'fonte', 'Updated': 'Aggiornato il', 'Generated from every solution page on Saving Planets.': 'Generato da ogni pagina di soluzione di Saving Planets.', 'government': 'governo', 'other': 'altro', 'agency': 'agenzia', 'corporate': 'azienda', 'nonprofit': 'non profit', 'natural': 'naturale' }
  };
  window.spLang = L;
  window.spT = function (s) { var t = S[L]; return (t && t[s]) || s; };
})();
(function () {
  var root = document.documentElement;
  try { localStorage.removeItem('sp_consent'); } catch (e) {} // Oct 16: GA + consent banner removed
  root.classList.add('dark'); // site is permanently dark
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
  var NEWS_MS = 3600000;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmt(iso) { var d = new Date(iso); return isNaN(d) ? '' : d.toLocaleDateString(spLang === 'en' ? undefined : spLang, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' }); }
  function count(iso) {
    var diff = new Date(iso).getTime() - Date.now();
    if (isNaN(diff)) return '';
    if (diff <= 0) return spT('Reached');
    var s = Math.floor(diff / 1000), d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
    return d + 'd ' + h + 'h ' + m + 'm ' + x + 's';
  }
  function renderNews(box, items) {
    if (!items || !items.length) { box.innerHTML = '<li>' + spT('News is unavailable right now.') + '</li>'; return; }
    box.innerHTML = items.map(function (a) {
      var u = /^https?:\/\//.test(a.url) ? a.url : '#';
      return '<li><a href="' + esc(u) + '" target="_blank" rel="noreferrer">' + esc(a.title) + '</a> <span class="mw-date">' + esc(fmt(a.published_at)) + '</span></li>';
    }).join('');
  }
  function render(el) {
    var ds = el.dataset, key = 'mw-news-' + (ds.news || ds.mission);
    var ms = (ds.milestones || '').split(';').filter(Boolean).map(function (m) { var p = m.split('|'); return { d: p[0], l: p[1] || '' }; });
    el.innerHTML = '<h2>' + esc(ds.mission) + (spLang === 'fr' ? ' : ' : ': ') + spT('Mission Status') + '</h2>' +
      (ds.status ? '<p class="mw-status">' + esc(ds.status) + '</p>' : '') +
      '<div class="mw-grid">' +
      (ds.launch ? '<div class="mw-count"><small>' + spT('Launch') + ' (' + esc(fmt(ds.launch)) + ')</small><b data-t="' + esc(ds.launch) + '"></b></div>' : '') +
      (ds.arrival ? '<div class="mw-count"><small>' + spT('Arrival') + ' (' + esc(ds.arrivalLabel || fmt(ds.arrival)) + ')</small><b data-t="' + esc(ds.arrival) + '"></b></div>' : '') +
      '</div>' +
      (ms.length ? '<h3>' + spT('Milestones') + '</h3><ul class="mw-milestones">' + ms.map(function (m) { var past = new Date(m.d).getTime() < Date.now(); return '<li class="' + (past ? 'done' : '') + '"><span class="mw-date">' + esc(fmt(m.d)) + '</span> ' + esc(m.l) + '</li>'; }).join('') + '</ul>' : '') +
      (ds.news ? '<h3>' + spT('Latest News') + '</h3><ul class="mw-news"><li>' + spT('Loading…') + '</li></ul>' : '') +
      '<p class="mw-note">' + spT('Dates per') + ' ' + esc(ds.agency || 'NASA') + '; ' + spT('missions shift.') + (ds.source ? ' <a href="' + esc(ds.source) + '" target="_blank" rel="noreferrer">' + spT('Source:') + ' ' + esc(ds.sourceLabel || 'NASA') + '</a>' : '') + '</p>';
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
  }
  window.spRenderMission = render;
  Array.prototype.forEach.call(els, render);
})();

/* Stats engine: renders the homepage overview ([data-site-stats]) and contextual
   .page-stats blocks from assets/data/solutions.json (generated by build-stats.js).
   One fetch per session (sessionStorage); on failure the blocks stay hidden and the
   homepage keeps its static numbers. */
(function () {
  var site = document.querySelector('[data-site-stats]');
  var blocks = [];  /* Oct 18: 'By the Numbers' blocks removed site-wide (owner); placeholders stripped by scripts/build-rawane-cuts.py */
  var diffs = document.querySelectorAll('.diff-body');
  if (!site && !blocks.length && !diffs.length) return;
  var KEY = 'sp-solutions-v3';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function num(n) { return typeof n === 'number' ? n.toLocaleString(spLang === 'en' ? 'en-US' : spLang) : esc(n); }
  function plural(n, a, b) { return num(n) + ' ' + spT(n === 1 ? a : b); }
  function cls(by) {
    var names = { agency: 'agency', corporate: 'corporate', nonprofit: 'nonprofit', government: 'government', natural: 'natural', other: 'other' };
    return Object.keys(names).filter(function (k) { return by[k]; }).map(function (k) { return by[k] + ' ' + spT(names[k]); }).join(' · ');
  }
  function solLine(a) { return plural(a.solutions, 'active solution', 'active solutions') + (a.horizon ? ', ' + a.horizon + ' ' + spT('on the horizon') : ''); }
  function updated(d) { var t = new Date(d.generated); return isNaN(t) ? '' : t.toLocaleDateString(spLang === 'en' ? 'en-US' : spLang, { year: 'numeric', month: 'long', day: 'numeric' }); }
  function render(d) {
    Array.prototype.forEach.call(diffs, function (el) { var n = d.site && d.site.solutions, h = d.site && d.site.hubs; if (!n) return; el.textContent = el.textContent.replace(/^\d+/, String(n)); });
    if (site) {
      var s = d.site;
      site.innerHTML = '<div class="stat-row">' +
        '<div class="stat"><span class="stat-number">' + num(s.solutions) + '</span><span class="stat-label">' + spT('active solutions featured') + (s.horizon ? ' (+' + s.horizon + ' ' + spT('on the horizon') + ')' : '') + '</span></div>' +
        '<div class="stat"><span class="stat-number">' + num(s.hubs) + '</span><span class="stat-label">' + spT('hubs across') + ' ' + num(s.categories) + ' ' + spT('categories') + '</span></div>' +
        '<div class="stat"><span class="stat-number">' + num(s.upcomingMissions) + '</span><span class="stat-label">' + spT('upcoming space missions we track live') + '</span></div>' +
        '<div class="stat"><span class="stat-number">' + num((s.byClassification.natural || 0)) + '</span><span class="stat-label">' + spT('natural solutions, alongside') + ' ' + cls(Object.keys(s.byClassification).reduce(function (o, k) { if (k !== 'natural') o[k] = s.byClassification[k]; return o; }, {})) + '</span></div>' +
        '</div>' + ((s.impactTotals || []).length ? '<div class="stat-row impact-totals">' + s.impactTotals.map(function (t) { return '<div class="stat"><span class="stat-number">' + num(t.total) + ' ' + esc(t.unit) + '</span><span class="stat-label">' + spT('combined across') + ' ' + plural(t.pages.length, 'solution', 'solutions') + ', ' + spT('each figure sourced on its page') + '</span></div>'; }).join('') + '</div>' : '') +
        '<p class="stat-source">' + spT('Last updated') + ' ' + esc(updated(d)) + '. ' + spT('Counts are generated from every solution page on this site.') + '</p>';
      site.hidden = false;
    }
    Array.prototype.forEach.call(blocks, function (el) {
      var c = d.categories[el.getAttribute('data-stats-category')];
      if (!c) return;
      var page = null, url = el.getAttribute('data-stats-page');
      d.pages.forEach(function (p) { if (p.url === url && !p.section) page = p; });
      var html = '<h2>' + spT('By the Numbers') + '</h2><div class="ps-grid">' +
        '<div class="ps-card"><h3>' + esc(spT(c.name)) + '</h3><p>' + solLine(c) + (cls(c.byClassification) ? '<br><small>' + esc(cls(c.byClassification)) + '</small>' : '') + '</p>' +
        (c.upcomingMissions ? '<p>' + plural(c.upcomingMissions, 'upcoming mission', 'upcoming missions') + '</p>' : '') +
        c.impactTotals.map(function (t) { return '<p>' + num(t.total) + ' ' + esc(t.unit) + ' <small>' + spT('combined, from sourced page figures') + '</small></p>'; }).join('') + '</div>' +
        '<div class="ps-card"><h3>' + spT('Site-Wide') + '</h3><p>' + solLine(d.site) + '</p><p>' + plural(d.site.hubs, 'hub', 'hubs') + ' · ' + plural(d.site.upcomingMissions, 'upcoming mission', 'upcoming missions') + '</p></div>';
      if (page && page.stats.length) {
        html += '<div class="ps-card"><h3>' + spT('This Page') + '</h3>' + page.stats.map(function (s) {
          var u = /^https?:\/\//.test(s.sourceUrl) ? s.sourceUrl : '';
          return '<p><b>' + num(s.value) + '</b> ' + esc(s.unit) + '<br><small>' + esc(s.label) + (u ? ' · <a href="' + esc(u) + '" target="_blank" rel="noreferrer">' + spT('source') + '</a>' : '') + '</small></p>';
        }).join('') + '</div>';
      }
      el.innerHTML = html + '</div><p class="ps-note">' + spT('Updated') + ' ' + esc(updated(d)) + '. ' + spT('Generated from every solution page on Saving Planets.') + '</p>';
      el.hidden = false;
    });
  }
  var cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) {}
  if (cached && cached.site) { render(cached); return; }
  fetch((/\/(fr|es|ar|it)\//.test(location.pathname) ? '../' : '') + 'assets/data/solutions.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) { try { sessionStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} render(d); })
    .catch(function () { /* keep blocks hidden; homepage keeps its static numbers */ });
})();
/* Newsletter sign-up ("Weekly Saving Planets Brief"). Posts to MailerLite's public form endpoint (public form IDs only, no API key),
   one form/group per language, double opt-in. No cookies or tracking: fetch uses credentials:'omit'. Fills [data-sp-newsletter]
   placeholders (index, Amazing Facts); on other pages adds a compact block inside the footer. */
(function () {
  var ACCT = '2704021';
  var FORMS = { en: '201062861124929242', fr: '201062865506927746', es: '201062865837229281', ar: '201062866183259490', it: '201435178471523359' };
  var T = {
    en: ['Get the Weekly Saving Planets Brief', 'New sourced solutions, one amazing fact and upcoming launches, every Monday. Free; unsubscribe anytime.', 'Email address', 'you@example.com', 'Subscribe', 'Please enter a valid email address.', 'Almost done! Check your inbox and confirm your subscription.', 'Sorry, something went wrong. Please try again later.', 'Sending…', 'Privacy', 'Newsletter language'],
    fr: ['Recevez le Brief hebdomadaire Saving Planets', 'De nouvelles solutions sourcées, un fait étonnant et les prochains lancements, chaque lundi. Gratuit ; désabonnement à tout moment.', 'Adresse e-mail', 'vous@exemple.com', 'S\u2019abonner', 'Veuillez saisir une adresse e-mail valide.', 'Presque fini ! Vérifiez votre boîte de réception et confirmez votre abonnement.', 'Désolé, une erreur s\u2019est produite. Veuillez réessayer plus tard.', 'Envoi…', 'Confidentialité', 'Langue de la newsletter'],
    es: ['Recibe el Resumen semanal de Saving Planets', 'Nuevas soluciones con fuentes, un dato asombroso y los próximos lanzamientos, cada lunes. Gratis; cancela cuando quieras.', 'Correo electrónico', 'tu@ejemplo.com', 'Suscribirme', 'Introduce un correo electrónico válido.', '¡Casi listo! Revisa tu bandeja de entrada y confirma tu suscripción.', 'Lo sentimos, algo salió mal. Inténtalo más tarde.', 'Enviando…', 'Privacidad', 'Idioma del boletín'],
    ar: ['احصل على النشرة الأسبوعية من Saving Planets', 'حلول جديدة موثقة المصادر، وحقيقة مذهلة، وعمليات الإطلاق القادمة، كل يوم اثنين. مجانية، ويمكنك إلغاء الاشتراك في أي وقت.', 'البريد الإلكتروني', 'you@example.com', 'اشترك', 'يرجى إدخال بريد إلكتروني صالح.', 'أوشكت على الانتهاء! تحقق من بريدك الوارد وأكّد اشتراكك.', 'عذرًا، حدث خطأ ما. يرجى المحاولة لاحقًا.', 'جارٍ الإرسال…', 'الخصوصية', 'لغة النشرة'],
    it: ['Ricevi il Brief settimanale di Saving Planets', 'Nuove soluzioni con fonti, un fatto incredibile e i prossimi lanci, ogni lunedì. Gratis; puoi annullare l\u2019iscrizione in qualsiasi momento.', 'Indirizzo email', 'tu@esempio.it', 'Iscriviti', 'Inserisci un indirizzo email valido.', 'Ci siamo quasi! Controlla la tua casella di posta e conferma l\u2019iscrizione.', 'Spiacenti, qualcosa è andato storto. Riprova più tardi.', 'Invio…', 'Privacy', 'Lingua della newsletter']
  };
  var NAMES = { en: 'English', fr: 'Fran\u00e7ais', es: 'Espa\u00f1ol', ar: '\u0627\u0644\u0639\u0631\u0628\u064a\u0629', it: 'Italiano' };
  var L = window.spLang || 'en', t = T[L] || T.en; if (!FORMS[L]) L = 'en'; // Oct 15: Italian form/group live (group 201435173183555461)
  var about = 'Privacy.html'; // Oct 14: standalone Privacy page in every language folder
  var css = '.sp-nl{max-width:640px;margin:2.2rem auto 0;padding:1.4rem 1.5rem;border:1px solid rgba(0,156,222,.35);border-radius:12px;background:#f3f9fd;color:#003755;text-align:center;font-family:Montserrat,"Segoe UI",sans-serif;box-sizing:border-box}' +
    '.sp-nl h2,.sp-nl h3{margin:0 0 .35rem;font-size:1.35rem;color:#003755}.sp-nl p{margin:0 0 .8rem;font-size:.92rem;line-height:1.45}' +
    '.sp-nl form{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}.sp-nl input[type=email]{flex:1 1 220px;min-width:0;padding:10px 12px;font:inherit;font-size:.95rem;border:1px solid #7aa7c2;border-radius:6px;color:#003755;background:#fff}' +
    '.sp-nl select{flex:0 0 auto;max-width:100%;padding:10px 8px;font:inherit;font-size:.95rem;border:1px solid #7aa7c2;border-radius:6px;color:#003755;background:#fff}.sp-nl select:focus-visible{outline:2px solid #003755;outline-offset:2px}.sp-nl button{padding:10px 20px;font:700 .95rem Montserrat,system-ui,sans-serif;background:#009cde;color:#fff;border:0;border-radius:6px;cursor:pointer}.sp-nl button[disabled]{opacity:.6;cursor:wait}' +
    '.sp-nl input:focus-visible,.sp-nl button:focus-visible{outline:2px solid #003755;outline-offset:2px}.sp-nl .sp-nl-msg{min-height:1.3em;margin:.6rem 0 0;font-weight:600}.sp-nl .sp-nl-ok{color:#00805f}.sp-nl .sp-nl-err{color:#b3261e}' +
    '.sp-nl{position:relative}.sp-nl .sp-nl-hp{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}.sp-nl .sp-nl-hp input{width:1px}.newsletter-band{padding:0 1.25rem}.sp-nl small{display:block;margin-top:.5rem;font-size:.75rem}.sp-nl small a{color:#00699a}' +
    '.sp-nl.sp-nl-compact{margin:0 auto 1rem;padding:1rem;background:transparent;border-color:rgba(0,156,222,.3)}div.sp-nl:not(.sp-nl-compact) h2{color:#003755 !important;background:none !important;-webkit-text-fill-color:#003755}div.sp-nl:not(.sp-nl-compact) p:not(.sp-nl-msg){color:#003755}footer .sp-nl{color:inherit}footer .sp-nl .sp-nl-ok{color:#5fe0b5}footer .sp-nl .sp-nl-err{color:#ffb4ab}footer .sp-nl h3{color:inherit;font-size:1.1rem}footer .sp-nl small a{color:inherit}';
  function build(host, compact, n) {
    var id = 'sp-nl-email-' + n, sid = 'sp-nl-lang-' + n, mid = 'sp-nl-msg-' + n, hTag = compact ? 'h3' : 'h2';
    host.className = (host.className ? host.className + ' ' : '') + 'sp-nl' + (compact ? ' sp-nl-compact' : '');
    if (L === 'ar') host.setAttribute('dir', 'rtl');
    host.innerHTML = '<' + hTag + '>' + t[0] + '</' + hTag + '><p>' + t[1] + '</p>' +
      '<form novalidate><label class="sp-nl-hp" aria-hidden="true">Leave empty<input type="text" name="hp" tabindex="-1" autocomplete="off"></label>' +
      '<label class="sp-nl-hp" for="' + id + '">' + t[2] + '</label><input id="' + id + '" type="email" name="email" required autocomplete="email" inputmode="email" dir="ltr" placeholder="' + t[3] + '" aria-describedby="' + mid + '">' +
      '<label class="sp-nl-hp" for="' + sid + '">' + t[10] + '</label><select id="' + sid + '" name="lang" class="sp-nl-lang">' + ['en', 'fr', 'es', 'ar', 'it'].map(function (k) { return '<option value="' + k + '" lang="' + k + '" dir="' + (k === 'ar' ? 'rtl' : 'ltr') + '"' + (k === L ? ' selected' : '') + '>' + NAMES[k] + '</option>'; }).join('') + '</select>' +
      '<button type="submit">' + t[4] + '</button></form><p class="sp-nl-msg" id="' + mid + '" role="status" aria-live="polite"></p>' +
      '<small><a href="' + about + '">' + t[9] + '</a></small>';
    var f = host.querySelector('form'), inp = f.querySelector('input[type=email]'), btn = f.querySelector('button'), msg = host.querySelector('.sp-nl-msg');
    function say(s, ok) { msg.textContent = s; msg.className = 'sp-nl-msg ' + (ok ? 'sp-nl-ok' : 'sp-nl-err'); }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.hp.value) return;
      var v = inp.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { inp.setAttribute('aria-invalid', 'true'); say(t[5], false); inp.focus(); return; }
      inp.removeAttribute('aria-invalid'); btn.disabled = true; msg.className = 'sp-nl-msg'; msg.textContent = t[8];
      var fd = new FormData(); fd.append('fields[email]', v); fd.append('ml-submit', '1'); fd.append('anticsrf', 'true');
      fetch('https://assets.mailerlite.com/jsonp/' + ACCT + '/forms/' + FORMS[FORMS[f.lang.value] ? f.lang.value : L] + '/subscribe', { method: 'POST', body: fd, credentials: 'omit', headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) { if (d && d.success) { say(t[6], true); f.reset(); if (window.spTrack) spTrack('newsletter_signup', { form_lang: f.lang ? f.lang.value : L }); } else say(t[7], false); })
        .catch(function () { say(t[7], false); })
        .then(function () { btn.disabled = false; });
    });
  }
  function init() {
    if (/google[0-9a-f]+\.html$/.test(location.pathname)) return;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var hosts = document.querySelectorAll('[data-sp-newsletter]'), n = 0;
    if (hosts.length) { for (var i = 0; i < hosts.length; i++) build(hosts[i], false, ++n); return; }
    if (document.body.hasAttribute('data-no-newsletter')) return; // e.g. Search.html opts out of the footer block
    var ft = document.querySelector('footer'); if (!ft) return;
    var d = document.createElement('div'); ft.insertBefore(d, ft.firstChild); build(d, true, ++n);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

/* Planet Scoreboard count-up + Solution of the Week rotation (2026-10-11) */
(function () {
  function run() {
    var nums = document.querySelectorAll('.sb-num[data-count]');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var loc = (typeof spLang === 'string' && spLang !== 'en') ? spLang : 'en-US';
    function show(el, v) { el.textContent = Math.round(v).toLocaleString(loc) + (el.getAttribute('data-suffix') || ''); }
    function animate(el) {
      var end = +el.getAttribute('data-count'), t0 = null, dur = 1800;
      function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); show(el, end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); }
      requestAnimationFrame(step);
    }
    if (nums.length && !reduce && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); animate(e.target); } }); }, { threshold: 0.4 });
      Array.prototype.forEach.call(nums, function (el) { show(el, 0); io.observe(el); });
    }
    // Solution of the Week: static card is built by scripts/build-home-extras.py; English home refreshes it from the JSON between rebuilds
    var sw = document.querySelector('.sotw[data-sotw-page]');
    if (!sw || document.documentElement.lang !== 'en') return;
    fetch('assets/data/solution-of-week.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
      var now = new Date(Date.now() - 10 * 36e5), st = new Date(d.start + 'T00:00:00Z');
      var e = d.rotation[Math.floor(Math.floor((now - st) / 864e5) / 7) % d.rotation.length];
      if (!e || e.page === sw.getAttribute('data-sotw-page')) return;
      var href = e.page + (e.video ? '#video' : '');
      var img = sw.querySelector('.sotw-img img'); img.src = e.image; img.alt = e.imageAlt;
      sw.querySelector('.sotw-img').href = href;
      var h = sw.querySelector('h2 a'); h.href = e.page; h.textContent = e.title;
      sw.querySelector('.sotw-blurb').textContent = e.blurb;
      var b = sw.querySelector('.sotw-actions a'); b.href = href; b.textContent = e.video ? 'Watch and Learn More' : 'Learn More';
      sw.setAttribute('data-sotw-page', e.page);
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
// Hero background video: poster only under prefers-reduced-motion (no download, no playback).
(function () {
  var v = document.querySelector('.hero-video');
  if (!v) return;
  var mq = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');
  function apply() { if (mq && mq.matches) { v.pause(); v.removeAttribute('autoplay'); v.preload = 'none'; } else if (v.paused) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
  apply(); if (mq && mq.addEventListener) mq.addEventListener('change', apply);
})();

/* Batch 3: hub quizzes (no tracking). Text comes from the page so translations work. */
(function () {
  document.querySelectorAll('section.quiz').forEach(function (qz) {
    var qs = qz.querySelectorAll('.quiz-q'), res = qz.querySelector('.quiz-result'), score = 0, done = 0;
    function txt(cls, n) { var el = qz.querySelector(cls); return el ? el.textContent.replace('{n}', n) : ''; }
    qs.forEach(function (f) {
      var ans = +f.getAttribute('data-answer'), btns = f.querySelectorAll('.quiz-opt'), fb = f.querySelector('.quiz-fb');
      btns.forEach(function (b) {
        b.addEventListener('click', function () {
          if (f.classList.contains('answered')) return;
          var ok = +b.getAttribute('data-i') === ans;
          f.classList.add('answered');
          btns.forEach(function (x) {
            x.setAttribute('aria-disabled', 'true');
            if (+x.getAttribute('data-i') === ans) x.classList.add('is-right');
          });
          b.classList.add(ok ? 'is-right' : 'is-wrong'); b.setAttribute('aria-pressed', 'true');
          fb.querySelector('.quiz-ok').hidden = !ok; fb.querySelector('.quiz-no').hidden = ok; fb.hidden = false;
          if (ok) score++; done++;
          if (done === qs.length) {
            res.querySelector('.quiz-score').textContent = txt('.quiz-tpl-score', score);
            res.hidden = false;
          }
        });
      });
    });
    qz.querySelector('.quiz-share').addEventListener('click', function () {
      var url = 'https://www.savingplanets.com' + location.pathname.replace(/\/$/, '/index.html') + '#quiz';
      var t = txt('.quiz-tpl', score), copied = qz.querySelector('.quiz-copied');
      if (navigator.share) { navigator.share({ title: document.title, text: t, url: url }).catch(function () {}); return; }
      var full = t + ' ' + url;
      function show() { copied.hidden = false; setTimeout(function () { copied.hidden = true; }, 4000); }
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(full).then(show, fallback); else fallback();
      function fallback() { var ta = document.createElement('textarea'); ta.value = full; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); show(); } catch (e) {} document.body.removeChild(ta); }
    });
    qz.querySelector('.quiz-reset').addEventListener('click', function () {
      score = 0; done = 0; res.hidden = true;
      qs.forEach(function (f) {
        f.classList.remove('answered'); f.querySelector('.quiz-fb').hidden = true;
        f.querySelectorAll('.quiz-opt').forEach(function (x) { x.classList.remove('is-right', 'is-wrong'); x.removeAttribute('aria-disabled'); x.removeAttribute('aria-pressed'); });
      });
      var first = qz.querySelector('.quiz-opt'); if (first) first.focus();
    });
  });
})();

/* Batch 4: Do One Thing Today (pick by local date from the rendered list) + Community Wall (approved items from JSON). */
(function () {
  function run() {
    Array.prototype.forEach.call(document.querySelectorAll('.dot[data-start]'), function (box) {
      var items = box.querySelectorAll('.dot-item'); if (!items.length) return;
      var d = new Date(), today = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
      var p = box.getAttribute('data-start').split('-'), st = Date.UTC(+p[0], +p[1] - 1, +p[2]);
      var n = Math.floor((today - st) / 864e5), k = ((n % items.length) + items.length) % items.length;
      Array.prototype.forEach.call(items, function (li, i) { li.hidden = i !== k; });
    });
    var g = document.querySelector('.comm-grid[data-community]'); if (!g) return;
    var src = (/\/(fr|es|ar|it)\//.test(location.pathname) ? '../' : '') + g.getAttribute('data-community');
    var pre = /\/(fr|es|ar|it)\//.test(location.pathname) ? '../' : '';
    fetch(src, { cache: 'no-cache', credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (d) {
      var it = (d && d.items) || []; if (!it.length) return;
      it.forEach(function (x) {
        var f = document.createElement('figure'); f.className = 'comm-item';
        var im = document.createElement('img'); im.src = pre + x.img; im.alt = x.alt || ''; im.loading = 'lazy'; f.appendChild(im);
        var c = document.createElement('figcaption');
        var b = document.createElement('strong'); b.textContent = x.name + (x.place ? ', ' + x.place : ''); c.appendChild(b);
        if (x.caption) { var t = document.createElement('span'); t.textContent = x.caption; c.appendChild(t); }
        f.appendChild(c); g.appendChild(f);
      });
      var e = document.querySelector('.comm-empty'); if (e) e.hidden = true;
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();/* UX-OCT15:START */
(function(){
  document.addEventListener('click',function(e){document.querySelectorAll('.nav-group details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});
  document.querySelectorAll('.nav-group details').forEach(function(d){var sm=d.querySelector('summary');d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.removeAttribute('open');sm.focus()}});d.addEventListener('toggle',function(){if(sm)sm.setAttribute('aria-expanded',d.open?'true':'false');if(d.open)document.querySelectorAll('.nav-group details[open]').forEach(function(o){if(o!==d)o.removeAttribute('open')})})});
  var f=document.querySelector('.sol-filters');if(!f)return;
  var L=JSON.parse(f.getAttribute('data-i18n'));
  var hubs=[].slice.call(document.querySelectorAll('.sol-hub'));
  // Oct 18 (owner): no 'Show all N' collapse on Solutions; every card in every hub is always shown.
  var dom='all',hub='all',sel=f.querySelector('select');
  function apply(){hubs.forEach(function(h){var ok=(dom==='all'||h.getAttribute('data-domain')===dom)&&(hub==='all'||h.id===hub);h.style.display=ok?'':'none'});
    f.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.value===dom)})}
  f.querySelectorAll('button').forEach(function(b){b.onclick=function(){dom=b.value;hub='all';if(sel)sel.value='all';apply()}});
  if(sel)sel.onchange=function(){hub=sel.value;dom='all';apply();if(hub!=='all'){var t=document.getElementById(hub);t&&t.scrollIntoView({behavior:'smooth'})}};
  var q=new URLSearchParams(location.search).get('domain');if(q){dom=q;}apply();
})();
(function(){var sel='.w-card,.card,.sol-card,.rel-card,.mission-widget,canvas,video,iframe,table,fieldset,figure,input,select,textarea,button:not(.spow-b),.btn,.roman-jump';
 var fabs=[],tk=false;/* looked up on every pass: the Superpowers button is added later by the kids script */
 function hit(f){if(f.classList.contains('spow-b')&&f.getAttribute('aria-expanded')==='true')return false;var r=f.getBoundingClientRect();if(!r.width)return false;
  var y0=f.classList.contains('fab-off')?window.innerHeight-r.height/2-16:r.top+r.height/2,pts=[[r.left+4,y0-r.height/2+4],[r.right-4,y0-r.height/2+4],[r.left+r.width/2,y0],[r.left+4,y0+r.height/2-4],[r.right-4,y0+r.height/2-4]];
  for(var i=0;i<pts.length;i++){var es=document.elementsFromPoint(pts[i][0],pts[i][1]);for(var j=0;j<es.length;j++){var e=es[j];if(e===f||f.contains(e)||fabs.indexOf(e)>-1)continue;if(e.closest&&e.closest(sel))return true}}return false}
 function run(){tk=false;fabs=[].slice.call(document.querySelectorAll('.sticky-help,.spow-b'));if(fabs.length)document.documentElement.classList.add('sp-fab');fabs.forEach(function(f){f.classList.toggle('fab-off',hit(f))})}
 function q(){if(!tk){tk=true;requestAnimationFrame(run)}}window.addEventListener('scroll',q,{passive:true});window.addEventListener('resize',q);document.addEventListener('click',function(){setTimeout(q,50)});setTimeout(run,300);
})();
/* UX-OCT15:END */
/* PLAY:START */
(function(){var K='sp-play-v1',P=['Kids_Map','Spot_the_Fire','Satellite_Explorer','Amazing_Facts','Myth_vs_Fact','Glossary'];
function get(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
function put(o){try{localStorage.setItem(K,JSON.stringify(o))}catch(e){}}
var pg=(location.pathname.split('/').pop()||'').replace(/\.html$/,'');if(P.indexOf(pg)>-1){var o=get();if(!o[pg]){o[pg]=Date.now();put(o)}}
function draw(){var g=document.querySelector('.pl-grid');if(!g)return;var o=get(),n=0,w=document.querySelector('.pl-wrap'),L=JSON.parse(w.dataset.levels);
[].forEach.call(g.querySelectorAll('.pl-tile'),function(a){var on=!!o[a.dataset.page];if(on)n++;a.classList.toggle('is-done',on);a.querySelector('.pl-badge').textContent=on?'⭐ '+w.dataset.done:w.dataset.todo});
var t=P.length,lv=n>=t?3:n>=3?2:n>=1?1:0;w.querySelector('.pl-count').textContent=w.dataset.prog.replace('{n}',n).replace('{t}',t);w.querySelector('.pl-level').textContent=(lv?'🏅 ':'🚀 ')+L[lv]}
document.addEventListener('DOMContentLoaded',function(){draw();var r=document.querySelector('.pl-reset');if(r)r.addEventListener('click',function(){put({});draw()})});
window.addEventListener('pageshow',draw)})();
/* PLAY:END */
/* SPNAV:START */
(function(){var n=document.getElementById('topnav');if(!n||!n.querySelector('.spn'))return;
var tg=n.querySelector('.spn-toggle'),mq=window.matchMedia('(min-width:1140px)'),hv=window.matchMedia('(hover:hover) and (pointer:fine)');
var dds=[].slice.call(n.querySelectorAll('.spn-dd'));
function set(li,o){li.classList.toggle('is-open',o);li.querySelector('.spn-trig').setAttribute('aria-expanded',o?'true':'false');if(!o)li.removeAttribute('data-hov')}
function closeAll(x){dds.forEach(function(li){if(li!==x)set(li,false)})}
function panel(o){n.classList.toggle('spn-open',o);if(tg){tg.setAttribute('aria-expanded',o?'true':'false');tg.setAttribute('aria-label',tg.getAttribute(o?'data-close':'data-open'))}if(!o)closeAll()}
dds.forEach(function(li){var b=li.querySelector('.spn-trig'),t;
 b.addEventListener('click',function(e){e.stopPropagation();var desk=mq.matches;
  if(b.tagName==='A'){var hov=desk&&hv.matches&&li.getAttribute('data-hov')==='1';if(li.classList.contains('is-open')&&(hov||li.getAttribute('data-hov')!=='1'))return;e.preventDefault();if(desk)closeAll(li);li.setAttribute('data-hov','2');set(li,true);return}
  if(desk&&hv.matches&&li.getAttribute('data-hov')==='1'){li.setAttribute('data-hov','2');set(li,true);return}
  var o=!li.classList.contains('is-open');if(desk)closeAll(li);set(li,o)});
 li.addEventListener('mouseenter',function(){if(!mq.matches||!hv.matches)return;clearTimeout(t);if(!li.classList.contains('is-open')){closeAll(li);set(li,true);li.setAttribute('data-hov','1')}});
 li.addEventListener('mouseleave',function(){if(!mq.matches||!hv.matches)return;t=setTimeout(function(){set(li,false)},200)});
 li.addEventListener('focusout',function(e){if(mq.matches&&e.relatedTarget&&!li.contains(e.relatedTarget))set(li,false)});
});
if(tg)tg.addEventListener('click',function(e){e.stopPropagation();panel(!n.classList.contains('spn-open'))});
document.addEventListener('click',function(e){if(!n.contains(e.target)){closeAll();if(n.classList.contains('spn-open'))panel(false)}});
document.addEventListener('keydown',function(e){if(e.key!=='Escape'&&e.key!=='Esc')return;var o=n.querySelector('.spn-dd.is-open');
 if(o){set(o,false);o.querySelector('.spn-trig').focus();return}if(n.classList.contains('spn-open')){panel(false);tg&&tg.focus()}});
var mqc=function(){panel(false)};if(mq.addEventListener)mq.addEventListener('change',mqc);else if(mq.addListener)mq.addListener(mqc);
var tk=false;function sc(){tk=false;n.classList.toggle('spn-solid',(window.pageYOffset||0)>24)}/* Oct 16 perf: pageYOffset needs no layout; first check after paint */
window.addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(sc)}},{passive:true});if(window.pageYOffset>24)requestAnimationFrame(sc);
/* Oct 18: --spn-h = live header height, so sticky bars (e.g. nav.roman-jump) sit below the header, never over it */
var de=document.documentElement;function hh(){de.style.setProperty('--spn-h',n.offsetHeight+'px')}hh();if(window.ResizeObserver)new ResizeObserver(hh).observe(n);else window.addEventListener('resize',hh);
/* Oct 16 (t886) language slide switches: tap, drag/swipe (pointer events), Space/Enter, arrow toward 'on'. One on at a time;
   turning one on goes to that language's version of this page, keeping ?query and #hash. RTL: on = thumb left (mirrored). */
var rtl=(document.documentElement.getAttribute('dir')||'').toLowerCase()==='rtl',rm=window.matchMedia('(prefers-reduced-motion: reduce)');
var lss=[].slice.call(n.querySelectorAll('.spn-ls'));
function su(u){u=String(u==null?'':u).replace(/[<>"'`\s]/g,'');return /^(javascript|data|vbscript):/i.test(u)?'#':u}
function lurl(a){return su((a.getAttribute('data-href0')||a.getAttribute('href')).replace(/[?#].*$/,'')+location.search+location.hash)}
function lgo(a){lss.forEach(function(x){x.setAttribute('aria-checked',x===a?'true':'false')});var u=lurl(a);setTimeout(function(){location.href=u},rm.matches?0:220)}
window.spnLang=function(c){var a=n.querySelector('.spn-ls[data-lang="'+c+'"]');if(!a||a.getAttribute('aria-current'))return false;lgo(a);return true};
lss.forEach(function(a,ix){var k=a.querySelector('.spn-ls-k'),st=null,moved=false,TR=16;
 function on(){return a.getAttribute('aria-checked')==='true'}
 a.addEventListener('pointerdown',function(e){if(e.button>0)return;moved=false;st={x:e.clientX,y:e.clientY,b:on()?TR:0,v:on()?TR:0,id:e.pointerId,act:false}});
 a.addEventListener('pointermove',function(e){if(!st||e.pointerId!==st.id)return;var dx=e.clientX-st.x,dy=e.clientY-st.y;
  if(!st.act){if(Math.abs(dx)<5)return;if(Math.abs(dy)>Math.abs(dx)){st=null;return}st.act=true;moved=true;a.classList.add('spn-drag');try{a.setPointerCapture(e.pointerId)}catch(_){}}
  var v=Math.max(0,Math.min(TR,st.b+(rtl?-dx:dx)));st.v=v;k.style.setProperty('--spn-x',v+'px');a.classList.toggle('spn-half',v>TR/2);e.preventDefault()});
 function end(e){if(!st)return;var s0=st;st=null;if(!s0.act)return;a.classList.remove('spn-drag','spn-half');k.style.removeProperty('--spn-x');
  if(e.type==='pointerup'&&s0.v>TR/2&&!on())lgo(a)}
 a.addEventListener('pointerup',end);a.addEventListener('pointercancel',end);a.addEventListener('dragstart',function(e){e.preventDefault()});
 a.addEventListener('click',function(e){if(moved){e.preventDefault();moved=false;return}if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();if(!on())lgo(a)});
 a.addEventListener('keydown',function(e){var K=e.key,fw=rtl?'ArrowLeft':'ArrowRight',bk=rtl?'ArrowRight':'ArrowLeft';
  if(K===' '||K==='Spacebar'||K===fw){e.preventDefault();if(!on())lgo(a)}else if(K===bk){e.preventDefault()}
  else if(K==='ArrowDown'||K==='ArrowUp'){e.preventDefault();var j=(ix+(K==='ArrowDown'?1:lss.length-1))%lss.length;lss[j].focus()}});
});
})();
/* SPNAV:END */
/* SPOW:START */
(function(){var pg=(location.pathname.split('/').pop()||'index').replace(/\.html$/,'')||'index',lang=(document.documentElement.lang||'en').slice(0,2);
try{var K='sp-pass-v1',o=JSON.parse(localStorage.getItem(K))||{};o.p=o.p||{};o.l=o.l||{};o.p[pg]=1;o.l[lang]=1;localStorage.setItem(K,JSON.stringify(o))}catch(e){}
var KS='sp-pow-v1',S={};try{S=JSON.parse(localStorage.getItem(KS))||{}}catch(e){}var R=document.documentElement;
function apply(){R.classList.toggle('sp-big1',S.big===1);R.classList.toggle('sp-big2',S.big===2);['dys','hc','calm','tap'].forEach(function(k){R.classList.toggle('sp-'+k,!!S[k])});
if(S.tap)[].forEach.call(document.querySelectorAll('[draggable=true]'),function(e){e.setAttribute('draggable','false');e.dataset.spDrag='1'});
else[].forEach.call(document.querySelectorAll('[data-sp-drag]'),function(e){e.setAttribute('draggable','true');delete e.dataset.spDrag});
if(S.calm)[].forEach.call(document.querySelectorAll('video[autoplay]'),function(v){try{v.pause()}catch(e){}})}
apply();if(["Play_and_Learn", "Kids_Map", "Spot_the_Fire", "Satellite_Explorer", "Amazing_Facts", "Myth_vs_Fact", "Glossary", "Space_Passport", "Myth_or_Fact_Arcade", "Boarding_Pass", "Orbits_Guide", "Orbit_Lab", "Learn", "Teachers", "Lesson_Builder"].indexOf(pg)<0)return;R.classList.add('sp-kidspage');
var T={"en": {"btn": "Superpowers", "h": "Your superpowers", "read": "Read to me", "stop": "Stop reading", "big": "Bigger text", "dys": "Easy-read font", "hc": "High contrast", "calm": "Calm motion", "tap": "Tap instead of drag", "reset": "Turn all off", "novoice": "This device has no voice for this language yet.", "note": "Saved only on this device.", "close": "Close"}, "fr": {"btn": "Super-pouvoirs", "h": "Tes super-pouvoirs", "read": "Lis-moi la page", "stop": "Arrêter la lecture", "big": "Texte plus grand", "dys": "Police facile à lire", "hc": "Contraste élevé", "calm": "Mouvements calmes", "tap": "Toucher au lieu de glisser", "reset": "Tout désactiver", "novoice": "Cet appareil n’a pas encore de voix pour cette langue.", "note": "Enregistré seulement sur cet appareil.", "close": "Fermer"}, "es": {"btn": "Superpoderes", "h": "Tus superpoderes", "read": "Léeme la página", "stop": "Dejar de leer", "big": "Texto más grande", "dys": "Letra fácil de leer", "hc": "Alto contraste", "calm": "Movimiento tranquilo", "tap": "Tocar en vez de arrastrar", "reset": "Desactivar todo", "novoice": "Este dispositivo aún no tiene voz para este idioma.", "note": "Se guarda solo en este dispositivo.", "close": "Cerrar"}, "ar": {"btn": "قوى خارقة", "h": "قواك الخارقة", "read": "اقرأ لي", "stop": "أوقف القراءة", "big": "نص أكبر", "dys": "خط سهل القراءة", "hc": "تباين عالٍ", "calm": "حركة هادئة", "tap": "المس بدل السحب", "reset": "أوقف الكل", "novoice": "لا يتوفر على هذا الجهاز صوت لهذه اللغة بعد.", "note": "يُحفظ على هذا الجهاز فقط.", "close": "إغلاق"}, "it": {"btn": "Superpoteri", "h": "I tuoi superpoteri", "read": "Leggimi la pagina", "stop": "Ferma la lettura", "big": "Testo più grande", "dys": "Carattere facile da leggere", "hc": "Contrasto elevato", "calm": "Movimento calmo", "tap": "Tocca invece di trascinare", "reset": "Disattiva tutto", "novoice": "Questo dispositivo non ha ancora una voce per questa lingua.", "note": "Salvato solo su questo dispositivo.", "close": "Chiudi"}, "he": {"btn": "כוחות־על", "h": "כוחות־העל שלכם", "read": "הקראה", "stop": "עצירת ההקראה", "big": "טקסט גדול יותר", "dys": "גופן קל לקריאה", "hc": "ניגודיות גבוהה", "calm": "תנועה רגועה", "tap": "הקשה במקום גרירה", "reset": "כיבוי הכול", "novoice": "למכשיר הזה עדיין אין קול בשפה הזו.", "note": "נשמר רק במכשיר הזה.", "close": "סגירה"}}[lang]||{"en": {"btn": "Superpowers", "h": "Your superpowers", "read": "Read to me", "stop": "Stop reading", "big": "Bigger text", "dys": "Easy-read font", "hc": "High contrast", "calm": "Calm motion", "tap": "Tap instead of drag", "reset": "Turn all off", "novoice": "This device has no voice for this language yet.", "note": "Saved only on this device.", "close": "Close"}, "fr": {"btn": "Super-pouvoirs", "h": "Tes super-pouvoirs", "read": "Lis-moi la page", "stop": "Arrêter la lecture", "big": "Texte plus grand", "dys": "Police facile à lire", "hc": "Contraste élevé", "calm": "Mouvements calmes", "tap": "Toucher au lieu de glisser", "reset": "Tout désactiver", "novoice": "Cet appareil n’a pas encore de voix pour cette langue.", "note": "Enregistré seulement sur cet appareil.", "close": "Fermer"}, "es": {"btn": "Superpoderes", "h": "Tus superpoderes", "read": "Léeme la página", "stop": "Dejar de leer", "big": "Texto más grande", "dys": "Letra fácil de leer", "hc": "Alto contraste", "calm": "Movimiento tranquilo", "tap": "Tocar en vez de arrastrar", "reset": "Desactivar todo", "novoice": "Este dispositivo aún no tiene voz para este idioma.", "note": "Se guarda solo en este dispositivo.", "close": "Cerrar"}, "ar": {"btn": "قوى خارقة", "h": "قواك الخارقة", "read": "اقرأ لي", "stop": "أوقف القراءة", "big": "نص أكبر", "dys": "خط سهل القراءة", "hc": "تباين عالٍ", "calm": "حركة هادئة", "tap": "المس بدل السحب", "reset": "أوقف الكل", "novoice": "لا يتوفر على هذا الجهاز صوت لهذه اللغة بعد.", "note": "يُحفظ على هذا الجهاز فقط.", "close": "إغلاق"}, "it": {"btn": "Superpoteri", "h": "I tuoi superpoteri", "read": "Leggimi la pagina", "stop": "Ferma la lettura", "big": "Testo più grande", "dys": "Carattere facile da leggere", "hc": "Contrasto elevato", "calm": "Movimento calmo", "tap": "Tocca invece di trascinare", "reset": "Disattiva tutto", "novoice": "Questo dispositivo non ha ancora una voce per questa lingua.", "note": "Salvato solo su questo dispositivo.", "close": "Chiudi"}, "he": {"btn": "כוחות־על", "h": "כוחות־העל שלכם", "read": "הקראה", "stop": "עצירת ההקראה", "big": "טקסט גדול יותר", "dys": "גופן קל לקריאה", "hc": "ניגודיות גבוהה", "calm": "תנועה רגועה", "tap": "הקשה במקום גרירה", "reset": "כיבוי הכול", "novoice": "למכשיר הזה עדיין אין קול בשפה הזו.", "note": "נשמר רק במכשיר הזה.", "close": "סגירה"}}.en;
var css='.sp-big1{font-size:118%}.sp-big2{font-size:135%}.sp-dys body,.sp-dys body *:not(code):not(pre):not(.k1-ring):not([class*=emoji]){font-family:Verdana,Tahoma,"Trebuchet MS",Arial,sans-serif!important;font-style:normal!important;line-height:1.65!important}'
+'.sp-dys body *:not(:lang(ar)):not(:lang(he)){letter-spacing:.05em!important;word-spacing:.16em!important}.sp-dys main p,.sp-dys main li{max-width:70ch;text-align:start!important}'
+'.sp-hc body,.sp-hc main,.sp-hc main *:not(img):not(video):not(canvas):not(svg):not(svg *){background-color:#000!important;background-image:none!important;color:#fff!important;border-color:#fff!important;box-shadow:none!important;text-shadow:none!important}'
+'.sp-hc main a{color:#ffe14d!important;text-decoration:underline!important}.sp-hc main button,.sp-hc main .k1-btn{outline:2px solid #fff}'
+'.sp-calm *,.sp-calm *:before,.sp-calm *:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}'
+'html.sp-kidspage main{padding-bottom:84px}html.sp-has-lb .spow-b{bottom:calc(var(--sp-lb-h,0px) + 12px)}html.sp-has-lb .spow-p{bottom:calc(var(--sp-lb-h,0px) + 76px)}'
+'.spow-b{position:fixed;z-index:9990;bottom:16px;inset-inline-start:16px;min-height:48px;padding:.45rem .95rem;font-size:.95rem!important;border-radius:999px;border:2px solid #fff;background:#4a3aa8;color:#fff;font:inherit;font-weight:800;box-shadow:0 6px 18px rgba(0,0,0,.35);cursor:pointer}'
+'.spow-b:focus-visible,.spow-p button:focus-visible{outline:3px solid #ffd54a;outline-offset:3px}'
+'.spow-p{position:fixed;z-index:9991;bottom:80px;inset-inline-start:16px;width:min(340px,calc(100vw - 32px));max-height:calc(100vh - 110px);overflow:auto;padding:1rem;border-radius:20px;background:#13123a;color:#fff;border:2px solid rgba(255,255,255,.35);box-shadow:0 14px 40px rgba(0,0,0,.5)}'
+'.spow-p h2{font-size:1.2rem;margin:0 0 .6rem;color:#fff}.spow-p button{display:flex;width:100%;align-items:center;justify-content:space-between;gap:.6rem;min-height:48px;margin:.3rem 0;padding:.5rem .9rem;border-radius:14px;border:2px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:#fff;font:inherit;font-weight:700;cursor:pointer;text-align:start}'
+'.spow-p button[aria-pressed=true]{background:#ffd54a;color:#1a1300;border-color:#ffd54a}.spow-p p{font-size:.85rem;opacity:.85;margin:.5rem 0 0}.spow-p .spow-x{width:auto;display:inline-flex;margin:0;float:inline-end}'
+'@media print{.spow-b,.spow-p{display:none!important}}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
var b=el('button','spow-b','✨ '+T.btn);b.type='button';b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','spow-p');
var p=el('div','spow-p');p.id='spow-p';p.hidden=true;p.setAttribute('role','dialog');p.setAttribute('aria-label',T.h);
var x=el('button','spow-x','✕');x.type='button';x.setAttribute('aria-label',T.close);p.appendChild(x);p.appendChild(el('h2','',T.h));
var msg=el('p');msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');
var rd=el('button','','🔊 '+T.read);rd.type='button';p.appendChild(rd);
function tog(k,lab,ic){var e=el('button','',ic+' '+lab);e.type='button';function u(){e.setAttribute('aria-pressed',k==='big'?String(!!S.big):String(!!S[k]));if(k==='big')e.textContent=ic+' '+lab+['',' +',' ++'][S.big||0]}
e.onclick=function(){if(k==='big')S.big=((S.big||0)+1)%3;else S[k]=!S[k];save();u()};u();p.appendChild(e);return u}
function save(){try{localStorage.setItem(KS,JSON.stringify(S))}catch(e){}apply()}
var U=[tog('big',T.big,'🔠'),tog('dys',T.dys,'📖'),tog('hc',T.hc,'🌓'),tog('calm',T.calm,'🐢'),tog('tap',T.tap,'👆')];
var rs=el('button','','↺ '+T.reset);rs.type='button';rs.onclick=function(){S={};save();U.forEach(function(f){f()})};p.appendChild(rs);p.appendChild(msg);p.appendChild(el('p','','🔒 '+T.note));
var ss=window.speechSynthesis,speaking=false;
function stop(){if(ss)ss.cancel();speaking=false;rd.textContent='🔊 '+T.read;rd.setAttribute('aria-pressed','false')}
function text(){var s=window.getSelection&&String(window.getSelection()).trim();if(s)return s;var m=document.querySelector('main')||document.body,c=m.cloneNode(true);
[].forEach.call(c.querySelectorAll('script,style,nav,button,textarea,select,[hidden],[aria-hidden=true],.dt-mini,.visually-hidden,.k1-noprint'),function(e){e.remove()});return c.textContent.replace(/\s+/g,' ').trim()}
rd.onclick=function(){if(speaking){stop();return}if(!ss||!window.SpeechSynthesisUtterance){msg.textContent=T.novoice;return}
var vs=ss.getVoices(),v=vs.filter(function(v){return v.lang&&v.lang.toLowerCase().indexOf(lang)===0||(lang==='he'&&/^iw/i.test(v.lang))});if(vs.length&&!v.length){msg.textContent=T.novoice;return}
var parts=text().match(/[^.!?。؟]+[.!?。؟]*\s*/g)||[];if(!parts.length)return;speaking=true;rd.textContent='⏹ '+T.stop;rd.setAttribute('aria-pressed','true');msg.textContent='';
parts.forEach(function(t,i){var u=new SpeechSynthesisUtterance(t);u.lang=document.documentElement.lang||lang;if(v[0])u.voice=v[0];u.rate=.95;if(i===parts.length-1)u.onend=stop;ss.speak(u)})};
function open(o){p.hidden=!o;b.setAttribute('aria-expanded',String(o));if(o)(p.querySelector('button:not(.spow-x)')||x).focus()}
b.onclick=function(){open(p.hidden)};x.onclick=function(){open(false);b.focus()};p.addEventListener('keydown',function(e){if(e.key==='Escape'){open(false);b.focus()}});
window.addEventListener('pagehide',stop);
function mount(){document.body.appendChild(p);document.body.appendChild(b)}if(document.body)mount();else document.addEventListener('DOMContentLoaded',mount)})();
/* SPOW:END */
/* SPEV:START */
(function(){
  var N=navigator,W=window,D=document;
  if(N.doNotTrack==='1'||W.doNotTrack==='1'||N.msDoNotTrack==='1'||N.globalPrivacyControl===true){W.spTrack=function(){};return}
  var URL_='https://si-helper.chambersbryank.workers.dev/e',L=(D.documentElement.getAttribute('lang')||'en').slice(0,2),Q=[],once={};
  function flush(){if(!Q.length||!N.sendBeacon)return;var b=JSON.stringify({l:L,e:Q.splice(0,20)});try{N.sendBeacon(URL_,new Blob([b],{type:'text/plain'}))}catch(e){}}
  function add(o,key){if(key){if(once[key])return;once[key]=1}Q.push(o);if(Q.length>=10)flush()}
  W.spTrack=function(n,p){if(n==='newsletter_signup')add({n:'newsletter'});if(n==='share'&&p)add({n:'share',kind:p.kind,page:p.page});if(n==='calc'&&p)add({n:'calc',tool:p.tool},'c'+p.tool)};
  D.addEventListener('visibilitychange',function(){if(D.visibilityState==='hidden')flush()});
  W.addEventListener('pagehide',flush);
  var pg=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,''),m=/^(Orbits?|Aero|Physics)_(Guide|Math|Lab)$/.exec(pg);
  var TR={Orbit:'orbit',Orbits:'orbit',Aero:'aero',Physics:'phys'};
  if(pg==='Learn')add({n:'learn',track:'all',kind:'hub'},'lv');
  if(m){var tr=TR[m[1]],kind=m[2].toLowerCase();add({n:'learn',track:tr,kind:kind},'lv');
    if(kind==='lab'){var f=function(e){if(e.target.closest&&e.target.closest('main')){add({n:'lab',tool:tr},'lab');D.removeEventListener('input',f,true);D.removeEventListener('click',f,true)}};D.addEventListener('input',f,true);D.addEventListener('click',f,true)}
    D.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.lnp-check,.lmcq button');if(!b)return;
      var box=b.closest('.lnp,.lmcq'),fb=box&&box.querySelector('.lnp-fb');if(!fb)return;
      var res=/\bis-ok\b/.test(fb.className)?'correct':/\bis-no\b/.test(fb.className)?'attempt':'';if(!res)return;
      var sec=box.closest('section[id]'),topic=sec?String(sec.id).toLowerCase().replace(/[^a-z0-9-]/g,'').slice(0,32):'page';
      add({n:'practice',track:tr,result:res,topic:topic||'page'});if(res==='correct')add({n:'practice',track:tr,result:'attempt',topic:topic||'page'})},false)}
  if(pg==='Ways_to_Help')D.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="http"]');if(!a)return;
    var h=(a.hostname||'').toLowerCase().replace(/^www\./,'');if(!h||/savingplanets\.com$/.test(h))return;
    add({n:'partner',host:h.slice(0,64),kind:/help-btn-join/.test(a.className)?'join':/help-btn/.test(a.className)?'donate':'link'});flush()},true);
})();
/* SPEV:END */
/* LANGBANNER:START */
document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[hreflang],.spn-ls[data-lang]');if(!a)return;var c=(a.getAttribute('data-lang')||a.getAttribute('hreflang')||'').slice(0,2).toLowerCase();if(c)try{localStorage.setItem('sp-lang-chosen',c)}catch(_){}},true);
(function(){try{
var d=document.documentElement;if(/[?&]embed=1(&|$)/.test(location.search)||d.classList.contains('sp-embed'))return;
var L=['en','fr','es','ar','it','he'],cur=(d.lang||'en').slice(0,2).toLowerCase();if(L.indexOf(cur)<0)return;
var prefs=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']),tgt=null;
for(var i=0;i<prefs.length;i++){var c=String(prefs[i]).slice(0,2).toLowerCase();if(L.indexOf(c)>=0){tgt=c;break}}
if(!tgt||tgt===cur)return;
var alt=document.querySelector('link[rel="alternate"][hreflang="'+tgt+'"]');if(!alt||!alt.href)return;
var K='sp-langbanner-v1',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){}
if(st[cur+'>'+tgt]==='stay')return;
/* Oct 17: never suggest when the visitor already picked this page's language (nav switch, banner or earlier choice) */
var CH='';try{CH=localStorage.getItem('sp-lang-chosen')||''}catch(e){}if(CH===cur)return;
var N={en:{en:'English',fr:'French',es:'Spanish',ar:'Arabic',it:'Italian'},fr:{en:'anglais',fr:'français',es:'espagnol',ar:'arabe',it:'italien'},es:{en:'inglés',fr:'francés',es:'español',ar:'árabe',it:'italiano'},it:{en:'inglese',fr:'francese',es:'spagnolo',ar:'arabo',it:'italiano'}};
var T={en:['This page is available in English.','View in English','Stay in '+N.en[cur],'Close'],
fr:['Cette page est disponible en français.','Voir en français','Rester en '+N.fr[cur],'Fermer'],
es:['Esta página está disponible en español.','Ver en español','Seguir en '+N.es[cur],'Cerrar'],
ar:['هذه الصفحة متوفرة باللغة العربية.','اعرضها بالعربية','البقاء على هذه الصفحة','إغلاق'],
it:['Questa pagina è disponibile in italiano.','Vedi in italiano','Resta in '+N.it[cur],'Chiudi'],
he:['הדף הזה זמין בעברית.','הצגה בעברית','להישאר בדף הזה','סגירה']}[tgt];
function save(v){st[cur+'>'+tgt]=v;try{localStorage.setItem(K,JSON.stringify(st));localStorage.setItem('sp-lang-chosen',v==='go'?tgt:cur)}catch(e){}}
var b=document.createElement('div');b.className='sp-lb';b.setAttribute('role','region');b.setAttribute('aria-label',T[0]);b.lang=tgt;b.dir=(tgt==='ar'||tgt==='he')?'rtl':'ltr';
b.innerHTML='<div class="sp-lb-in"><p class="sp-lb-msg"></p><div class="sp-lb-btns"><a class="sp-lb-go"></a><button type="button" class="sp-lb-stay"></button><button type="button" class="sp-lb-x"><span aria-hidden="true">×</span></button></div></div>';
b.querySelector('.sp-lb-msg').textContent=T[0];var g=b.querySelector('.sp-lb-go');g.textContent=T[1];g.href=alt.href.replace(/[?#].*$/,'')+location.search+location.hash;g.hreflang=tgt;
b.querySelector('.sp-lb-stay').textContent=T[2];b.querySelector('.sp-lb-x').setAttribute('aria-label',T[3]);
var nav=document.getElementById('topnav');
function place(){d.style.setProperty('--sp-lb-h',b.offsetHeight+'px')}
function ping(){try{window.dispatchEvent(new Event('sp-lb'))}catch(e){}}
function close(){save('stay');b.remove();d.classList.remove('sp-has-lb');d.style.removeProperty('--sp-lb-h');ping();if(nav){var f=nav.querySelector('a,button');f&&f.focus({preventScroll:true})}}
g.addEventListener('click',function(e){save('go');/* Oct 16 t886: switch the same way as the nav language switches (green toggle, keeps ?query/#hash) */if(!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.altKey&&window.spnLang&&window.spnLang(tgt))e.preventDefault()});
b.querySelector('.sp-lb-stay').addEventListener('click',close);b.querySelector('.sp-lb-x').addEventListener('click',close);
function show(){if(!document.body)return;if(nav&&nav.parentNode)nav.parentNode.insertBefore(b,nav.nextSibling);else document.body.insertBefore(b,document.body.firstChild);
d.classList.add('sp-has-lb');place();ping();if(window.ResizeObserver){var ro=new ResizeObserver(place);ro.observe(b);nav&&ro.observe(nav)}window.addEventListener('resize',place,{passive:true});window.addEventListener('scroll',place,{passive:true})}
/* Oct 16 perf: overlay, so show it when the main thread is idle after load (never blocks first paint) */
function later(){(window.requestIdleCallback||function(f){setTimeout(f,200)})(show,{timeout:2500})}
if(document.readyState==='complete')later();else window.addEventListener('load',later);
}catch(e){}})();
/* LANGBANNER:END */
