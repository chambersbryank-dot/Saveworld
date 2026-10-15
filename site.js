/* i18n strings for script-drawn UI (translated pages set <html lang="fr|es|ar">). Keys are the English text. */
(function () {
  var L = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  var S = {
    fr: { 'Ocean': 'Océan', 'Lakes': 'Lacs', 'Rivers': 'Rivières', 'Forests': 'Forêts', 'Space': 'Espace', 'Planetary Defense': 'Défense planétaire', 'Space Weather & Shields': 'Météo spatiale et boucliers', 'Earth Observation': 'Observation de la Terre', 'Project Rawane': 'Projet Rawane', 'Mission Status': 'état de la mission', 'Reached': 'Atteint', 'News is unavailable right now.': 'Actualités indisponibles pour le moment.', 'Launch': 'Lancement', 'Arrival': 'Arrivée', 'Milestones': 'Étapes clés', 'Latest News': 'Dernières actualités', 'Loading…': 'Chargement…', 'Dates per': 'Dates selon', 'missions shift.': 'les missions évoluent.', 'Source:': 'Source :',
      'active solution': 'solution active', 'active solutions': 'solutions actives', 'on the horizon': 'à l\u2019horizon', 'active solutions featured': 'solutions actives présentées', 'hubs across': 'hubs dans', 'categories': 'catégories', 'upcoming space missions we track live': 'missions spatiales à venir suivies en direct', 'natural solutions, alongside': 'solutions naturelles, ainsi que', 'combined across': 'cumulés sur', 'solution': 'solution', 'solutions': 'solutions', 'each figure sourced on its page': 'chaque chiffre sourcé sur sa page', 'Last updated': 'Dernière mise à jour :', 'Counts are generated from every solution page on this site.': 'Les totaux sont générés à partir de chaque page de solution du site.', 'By the Numbers': 'En chiffres', 'upcoming mission': 'mission à venir', 'upcoming missions': 'missions à venir', 'combined, from sourced page figures': 'cumulés, à partir des chiffres sourcés des pages', 'Site-Wide': 'Sur tout le site', 'hub': 'hub', 'hubs': 'hubs', 'This Page': 'Cette page', 'source': 'source', 'Updated': 'Mis à jour le', 'Generated from every solution page on Saving Planets.': 'Généré à partir de chaque page de solution de Saving Planets.', 'agency': 'agence', 'corporate': 'entreprise', 'nonprofit': 'association', 'natural': 'naturelle' },
    es: { 'Ocean': 'Océano', 'Lakes': 'Lagos', 'Rivers': 'Ríos', 'Forests': 'Bosques', 'Space': 'Espacio', 'Planetary Defense': 'Defensa planetaria', 'Space Weather & Shields': 'Clima espacial y escudos', 'Earth Observation': 'Observación de la Tierra', 'Project Rawane': 'Proyecto Rawane', 'Mission Status': 'estado de la misión', 'Reached': 'Alcanzado', 'News is unavailable right now.': 'Noticias no disponibles por ahora.', 'Launch': 'Lanzamiento', 'Arrival': 'Llegada', 'Milestones': 'Hitos', 'Latest News': 'Últimas noticias', 'Loading…': 'Cargando…', 'Dates per': 'Fechas según', 'missions shift.': 'las misiones cambian.', 'Source:': 'Fuente:',
      'active solution': 'solución activa', 'active solutions': 'soluciones activas', 'on the horizon': 'en el horizonte', 'active solutions featured': 'soluciones activas destacadas', 'hubs across': 'centros en', 'categories': 'categorías', 'upcoming space missions we track live': 'próximas misiones espaciales que seguimos en vivo', 'natural solutions, alongside': 'soluciones naturales, junto a', 'combined across': 'en conjunto entre', 'solution': 'solución', 'solutions': 'soluciones', 'each figure sourced on its page': 'cada cifra con fuente en su página', 'Last updated': 'Última actualización:', 'Counts are generated from every solution page on this site.': 'Los recuentos se generan a partir de cada página de solución del sitio.', 'By the Numbers': 'En cifras', 'upcoming mission': 'próxima misión', 'upcoming missions': 'próximas misiones', 'combined, from sourced page figures': 'en conjunto, a partir de cifras con fuente', 'Site-Wide': 'Todo el sitio', 'hub': 'centro', 'hubs': 'centros', 'This Page': 'Esta página', 'source': 'fuente', 'Updated': 'Actualizado el', 'Generated from every solution page on Saving Planets.': 'Generado a partir de cada página de solución de Saving Planets.', 'agency': 'agencia', 'corporate': 'empresa', 'nonprofit': 'sin ánimo de lucro', 'natural': 'natural' },
    ar: { 'Ocean': 'المحيط', 'Lakes': 'البحيرات', 'Rivers': 'الأنهار', 'Forests': 'الغابات', 'Space': 'الفضاء', 'Planetary Defense': 'الدفاع الكوكبي', 'Space Weather & Shields': 'الطقس الفضائي والدروع', 'Earth Observation': 'رصد الأرض', 'Project Rawane': 'مشروع Rawane', 'Mission Status': 'حالة المهمة', 'Reached': 'تحقّق', 'News is unavailable right now.': 'الأخبار غير متاحة حاليًا.', 'Launch': 'الإطلاق', 'Arrival': 'الوصول', 'Milestones': 'المحطات الرئيسية', 'Latest News': 'آخر الأخبار', 'Loading…': 'جارٍ التحميل…', 'Dates per': 'التواريخ وفق', 'missions shift.': 'والمواعيد قابلة للتغيّر.', 'Source:': 'المصدر:',
      'active solution': 'حل نشط', 'active solutions': 'حلول نشطة', 'on the horizon': 'في الأفق', 'active solutions featured': 'حلًا نشطًا معروضًا', 'hubs across': 'محاور ضمن', 'categories': 'فئات', 'upcoming space missions we track live': 'مهمة فضائية قادمة نتابعها مباشرة', 'natural solutions, alongside': 'حلول طبيعية، إلى جانب', 'combined across': 'مجموع عبر', 'solution': 'حل', 'solutions': 'حلول', 'each figure sourced on its page': 'كل رقم موثّق في صفحته', 'Last updated': 'آخر تحديث:', 'Counts are generated from every solution page on this site.': 'تُحسب الأعداد من كل صفحات الحلول في الموقع.', 'By the Numbers': 'بالأرقام', 'upcoming mission': 'مهمة قادمة', 'upcoming missions': 'مهام قادمة', 'combined, from sourced page figures': 'مجموع من الأرقام الموثّقة في الصفحات', 'Site-Wide': 'على مستوى الموقع', 'hub': 'محور', 'hubs': 'محاور', 'This Page': 'هذه الصفحة', 'source': 'المصدر', 'Updated': 'حُدّث في', 'Generated from every solution page on Saving Planets.': 'مُولَّد من كل صفحات الحلول في Saving Planets.', 'agency': 'وكالة', 'corporate': 'شركة', 'nonprofit': 'منظمة غير ربحية', 'natural': 'طبيعي' }
  };
  window.spLang = L;
  window.spT = function (s) { var t = S[L]; return (t && t[s]) || s; };
})();
(function () {
  var root = document.documentElement;
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
  var blocks = document.querySelectorAll('.page-stats[data-stats-category]');
  var diffs = document.querySelectorAll('.diff-body');
  if (!site && !blocks.length && !diffs.length) return;
  var KEY = 'sp-solutions-v3';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function num(n) { return typeof n === 'number' ? n.toLocaleString(spLang === 'en' ? 'en-US' : spLang) : esc(n); }
  function plural(n, a, b) { return num(n) + ' ' + spT(n === 1 ? a : b); }
  function cls(by) {
    var names = { agency: 'agency', corporate: 'corporate', nonprofit: 'nonprofit', natural: 'natural' };
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
  fetch((/\/(fr|es|ar)\//.test(location.pathname) ? '../' : '') + 'assets/data/solutions.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) { try { sessionStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} render(d); })
    .catch(function () { /* keep blocks hidden; homepage keeps its static numbers */ });
})();
/* Newsletter sign-up ("Weekly Saving Planets Brief"). Posts to MailerLite's public form endpoint (public form IDs only, no API key),
   one form/group per language, double opt-in. No cookies or tracking: fetch uses credentials:'omit'. Fills [data-sp-newsletter]
   placeholders (index, Amazing Facts); on other pages adds a compact block inside the footer. */
(function () {
  var ACCT = '2704021';
  var FORMS = { en: '201062861124929242', fr: '201062865506927746', es: '201062865837229281', ar: '201062866183259490' };
  var T = {
    en: ['Get the Weekly Saving Planets Brief', 'New sourced solutions, one amazing fact and upcoming launches, every Monday. Free; unsubscribe anytime.', 'Email address', 'you@example.com', 'Subscribe', 'Please enter a valid email address.', 'Almost done! Check your inbox and confirm your subscription.', 'Sorry, something went wrong. Please try again later.', 'Sending…', 'Privacy', 'Newsletter language'],
    fr: ['Recevez le Brief hebdomadaire Saving Planets', 'De nouvelles solutions sourcées, un fait étonnant et les prochains lancements, chaque lundi. Gratuit ; désabonnement à tout moment.', 'Adresse e-mail', 'vous@exemple.com', 'S\u2019abonner', 'Veuillez saisir une adresse e-mail valide.', 'Presque fini ! Vérifiez votre boîte de réception et confirmez votre abonnement.', 'Désolé, une erreur s\u2019est produite. Veuillez réessayer plus tard.', 'Envoi…', 'Confidentialité', 'Langue de la newsletter'],
    es: ['Recibe el Resumen semanal de Saving Planets', 'Nuevas soluciones con fuentes, un dato asombroso y los próximos lanzamientos, cada lunes. Gratis; cancela cuando quieras.', 'Correo electrónico', 'tu@ejemplo.com', 'Suscribirme', 'Introduce un correo electrónico válido.', '¡Casi listo! Revisa tu bandeja de entrada y confirma tu suscripción.', 'Lo sentimos, algo salió mal. Inténtalo más tarde.', 'Enviando…', 'Privacidad', 'Idioma del boletín'],
    ar: ['احصل على النشرة الأسبوعية من Saving Planets', 'حلول جديدة موثقة المصادر، وحقيقة مذهلة، وعمليات الإطلاق القادمة، كل يوم اثنين. مجانية، ويمكنك إلغاء الاشتراك في أي وقت.', 'البريد الإلكتروني', 'you@example.com', 'اشترك', 'يرجى إدخال بريد إلكتروني صالح.', 'أوشكت على الانتهاء! تحقق من بريدك الوارد وأكّد اشتراكك.', 'عذرًا، حدث خطأ ما. يرجى المحاولة لاحقًا.', 'جارٍ الإرسال…', 'الخصوصية', 'لغة النشرة']
  };
  var NAMES = { en: 'English', fr: 'Fran\u00e7ais', es: 'Espa\u00f1ol', ar: '\u0627\u0644\u0639\u0631\u0628\u064a\u0629' };
  var L = window.spLang || 'en'; if (!FORMS[L]) L = 'en';
  var t = T[L], about = 'Privacy.html'; // Oct 14: standalone Privacy page in every language folder
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
      '<label class="sp-nl-hp" for="' + sid + '">' + t[10] + '</label><select id="' + sid + '" name="lang" class="sp-nl-lang">' + ['en', 'fr', 'es', 'ar'].map(function (k) { return '<option value="' + k + '" lang="' + k + '" dir="' + (k === 'ar' ? 'rtl' : 'ltr') + '"' + (k === L ? ' selected' : '') + '>' + NAMES[k] + '</option>'; }).join('') + '</select>' +
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
    var src = (/\/(fr|es|ar)\//.test(location.pathname) ? '../' : '') + g.getAttribute('data-community');
    var pre = /\/(fr|es|ar)\//.test(location.pathname) ? '../' : '';
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
})();
