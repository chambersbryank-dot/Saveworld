/* Shared Launch Library 2 feed for Upcoming_Launches.html (launch-tracker.js, launch-pick.js, launch-actions.js).
   Merges LL2 /launches/upcoming/ with /launches/previous/ so a launch does not vanish at T-0:
   a launch stays listed until the later of (a) the end of its launch day in Pacific/Honolulu,
   (b) 24 hours after liftoff, or (c) an optional "keepUntil" on its row in data/launch-streams.json.
   Data: The Space Devs (ll.thespacedevs.com). One shared fetch, cached 10 min per tab. */
(function () {
  var BASE = 'https://ll.thespacedevs.com/2.3.0/launches/';
  var UP = BASE + 'upcoming/?limit=20&mode=detailed';
  var PREV = BASE + 'previous/?limit=8&mode=detailed';
  var STREAMS_URL = 'data/launch-streams.json?v=20261113k3';
  var CACHE_KEY = 'sp-ll2-feed2';
  var CACHE_MS = 10 * 60 * 1000;
  var HOUR = 3600000, DAY = 24 * HOUR;
  var HNL = -10 * HOUR; /* Pacific/Honolulu: UTC-10 all year (no daylight saving). */
  var DONE = { 'in flight': 1, deployed: 1, success: 1, failure: 1, 'partial failure': 1 };
  var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  var prefix = (location.pathname.indexOf('/' + lang + '/') >= 0) ? '../' : '';

  var L = {
    en: { today: 'Launched today, {t}', on: 'Launched {d}', past: 'T-0 passed ({t})', pending: 'Status update pending', recent: 'Recent launch',
      st: { 'in flight': 'In flight', deployed: 'Payload deployed', success: 'Success', failure: 'Launch failure', 'partial failure': 'Partial failure' },
      f15: 'Launched Nov 13 · Ship returning — catch attempt Sat ~11:20 AM HST' },
    fr: { today: 'Lancé aujourd’hui, {t}', on: 'Lancé le {d}', past: 'T-0 passé ({t})', pending: 'Statut en attente de mise à jour', recent: 'Lancement récent',
      st: { 'in flight': 'En vol', deployed: 'Charge utile déployée', success: 'Succès', failure: 'Échec du lancement', 'partial failure': 'Échec partiel' },
      f15: 'Lancé le 13 nov. · Vaisseau en retour — tentative de capture sam. vers 11 h 20 HST' },
    es: { today: 'Lanzado hoy, {t}', on: 'Lanzado el {d}', past: 'T-0 superado ({t})', pending: 'Estado pendiente de actualización', recent: 'Lanzamiento reciente',
      st: { 'in flight': 'En vuelo', deployed: 'Carga desplegada', success: 'Éxito', failure: 'Fallo del lanzamiento', 'partial failure': 'Fallo parcial' },
      f15: 'Lanzado el 13 nov. · Nave en retorno — intento de captura sáb. hacia las 11:20 a. m. HST' },
    it: { today: 'Lanciato oggi, {t}', on: 'Lanciato il {d}', past: 'T-0 superato ({t})', pending: 'Stato in attesa di aggiornamento', recent: 'Lancio recente',
      st: { 'in flight': 'In volo', deployed: 'Carico rilasciato', success: 'Successo', failure: 'Lancio fallito', 'partial failure': 'Fallimento parziale' },
      f15: 'Lanciato il 13 nov. · Veicolo in rientro — tentativo di cattura sab. verso le 11:20 HST' },
    ar: { today: 'أُطلق اليوم، {t}', on: 'أُطلق في {d}', past: 'تجاوز موعد T-0 ({t})', pending: 'بانتظار تحديث الحالة', recent: 'إطلاق حديث',
      st: { 'in flight': 'في الرحلة', deployed: 'تم نشر الحمولة', success: 'نجاح', failure: 'فشل الإطلاق', 'partial failure': 'فشل جزئي' },
      f15: 'أُطلق في 13 نوفمبر · المركبة في طريق العودة — محاولة التقاط السبت نحو الساعة 11:20 صباحًا بتوقيت هاواي' },
    he: { today: 'שוגר היום, {t}', on: 'שוגר ב-{d}', past: 'מועד T-0 עבר ({t})', pending: 'ממתינים לעדכון סטטוס', recent: 'שיגור אחרון',
      st: { 'in flight': 'בטיסה', deployed: 'המטען שוחרר', success: 'הצלחה', failure: 'כישלון בשיגור', 'partial failure': 'כישלון חלקי' },
      f15: 'שוגר ב-13 בנובמבר · החללית בדרך חזרה — ניסיון תפיסה בשבת בסביבות 11:20 בבוקר לפי שעון הוואי' }
  };
  var tx = L[lang] || L.en;

  var streams = [];
  function abbrev(l) { return l && l.status && l.status.abbrev ? String(l.status.abbrev).toLowerCase() : ''; }
  function netMs(l) { return new Date(l && l.net).getTime(); }
  function nameBlob(l) { return (((l && l.name) || '') + ' ' + ((l && l.mission && l.mission.name) || '')).toLowerCase(); }
  function isF15(l) { return /starship flight 15|starlink group 31-2/.test(nameBlob(l)); }
  function row(l) {
    var n = nameBlob(l);
    for (var i = 0; i < streams.length; i++) {
      var s = streams[i];
      if (s && s.match && n.indexOf(String(s.match).toLowerCase()) >= 0) return s;
    }
    return null;
  }
  /* End of the Pacific/Honolulu calendar day that contains ms. */
  function hnlDayEnd(ms) { return Math.floor((ms + HNL) / DAY) * DAY + DAY - HNL; }
  function keepUntil(l) {
    var x = netMs(l);
    if (isNaN(x)) return Infinity;
    var until = Math.max(hnlDayEnd(x), x + DAY);
    var r = row(l), k = r && r.keepUntil ? new Date(r.keepUntil).getTime() : NaN;
    if (!isNaN(k)) until = Math.max(until, k);
    return until;
  }
  function isPast(l, now) {
    var x = netMs(l);
    now = now == null ? Date.now() : now;
    if (DONE[abbrev(l)] && (isNaN(x) || x <= now)) return true;
    return !isNaN(x) && x <= now;
  }
  function keep(l, now) {
    now = now == null ? Date.now() : now;
    var x = netMs(l);
    if (isNaN(x)) return !DONE[abbrev(l)];
    if (x > now) return true;
    return now < keepUntil(l);
  }
  function filter(results, now) {
    now = now == null ? Date.now() : now;
    return (results || []).filter(function (l) { return keep(l, now); });
  }
  function fmt(ms, opts) { return new Date(ms).toLocaleString(lang === 'en' ? undefined : lang, opts); }
  function sameLocalDay(a, b) {
    var x = new Date(a), y = new Date(b);
    return x.getFullYear() === y.getFullYear() && x.getMonth() === y.getMonth() && x.getDate() === y.getDate();
  }
  /* "Launched today, 12:47 PM HST · In flight" in the visitor's own time zone. */
  function f15Status() { return tx.f15; }
  function statusLine(l, now) {
    if (isF15(l)) return tx.f15;
    return statusText(l && l.net, abbrev(l), now);
  }
  function statusText(net, ab, now) {
    var x = new Date(net).getTime();
    now = now == null ? Date.now() : now;
    if (isNaN(x)) return '';
    ab = String(ab || '').toLowerCase();
    var time = fmt(x, { hour: 'numeric', minute: '2-digit', timeZoneName: 'short' });
    var st = tx.st[ab];
    if (!st) return tx.past.replace('{t}', time) + ' · ' + tx.pending;
    var when = sameLocalDay(x, now) ? tx.today.replace('{t}', time)
      : tx.on.replace('{d}', fmt(x, { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }));
    return when + ' · ' + st;
  }

  function merge(up, prev) {
    var seen = {}, out = [];
    [].concat((up && up.results) || [], (prev && prev.results) || []).forEach(function (l) {
      var id = l && (l.id || l.name);
      if (!id || seen[id]) return;
      seen[id] = 1; out.push(l);
    });
    out.sort(function (a, b) {
      var x = netMs(a), y = netMs(b);
      if (isNaN(x)) return 1; if (isNaN(y)) return -1;
      return x - y;
    });
    return { results: out };
  }
  function readCache() {
    try {
      var c = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      if (c && Date.now() - c.t < CACHE_MS && c.d && c.d.results) return c.d;
    } catch (e) {}
    return null;
  }
  function getJson(url, ms) {
    var ctl = window.AbortController ? new AbortController() : null;
    if (ctl) setTimeout(function () { ctl.abort(); }, ms || 10000);
    return fetch(url, { headers: { Accept: 'application/json' }, signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
  }
  var streamsP = fetch(prefix + STREAMS_URL, { credentials: 'omit', cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : { streams: [] }; })
    .catch(function () { return { streams: [] }; })
    .then(function (j) { streams = (j && j.streams) || []; return streams; });
  var loadP = null, last = null;
  function load() {
    if (loadP) return loadP;
    var c = readCache();
    var dataP = c ? Promise.resolve(c) : Promise.all([
      getJson(UP),
      getJson(PREV).catch(function () { return { results: [] }; })
    ]).then(function (a) {
      var d = merge(a[0], a[1]);
      try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
      return d;
    });
    dataP = dataP.then(function (d) { last = d; return d; });
    loadP = Promise.all([dataP, streamsP]).then(function (a) { return a[0]; });
    return loadP;
  }
  function cached() { var c = last || readCache(); return c ? c.results : null; }

  window.SPLaunchFeed = {
    load: load, cached: cached, streams: function () { return streamsP; },
    keep: keep, filter: filter, isPast: isPast, keepUntil: keepUntil, statusText: statusText,
    statusLine: statusLine, f15Status: f15Status, isF15: isF15,
    recentLabel: tx.recent, _merge: merge, _setStreams: function (s) { streams = s || []; }
  };
})();
