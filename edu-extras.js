/* Oct 14 2026: NGSS-style standards tags on generated lesson plans, plus no-account badges and a printable
   certificate for the Kids Planet Map and Satellite Explorer. Stores only badge flags in localStorage (no personal data). */
(function () {
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { std: 'Standards alignment (NGSS)', note: 'Performance expectations from the Next Generation Science Standards that this plan supports. Check your own state or national standards too.', uni: 'University level: no NGSS code; aligns with introductory Earth system and environmental science courses.', view: 'Look up on nextgenscience.org', badge: 'Badge earned!', map: 'Planet Explorer', sx: 'Satellite Builder', cert: 'Print my certificate', name: 'Your first name or class name (optional)', certT: 'Certificate of Discovery', certB: 'earned the', on: 'on', site: 'Saving Planets: real solutions that help people and nature' },
    fr: { std: 'Alignement sur les standards (NGSS)', note: 'Attendus de performance des Next Generation Science Standards (États-Unis) couverts par ce plan. Vérifiez aussi vos programmes nationaux.', uni: 'Niveau universitaire : pas de code NGSS ; correspond aux cours d’introduction aux sciences du système Terre et de l’environnement.', view: 'Voir sur nextgenscience.org', badge: 'Badge gagné !', map: 'Explorateur de la planète', sx: 'Constructeur de satellite', cert: 'Imprimer mon certificat', name: 'Ton prénom ou le nom de la classe (facultatif)', certT: 'Certificat de découverte', certB: 'a gagné le badge', on: 'le', site: 'Saving Planets : de vraies solutions qui aident les humains et la nature' },
    es: { std: 'Alineación con estándares (NGSS)', note: 'Expectativas de desempeño de los Next Generation Science Standards (EE. UU.) que apoya este plan. Revisa también tus estándares nacionales.', uni: 'Nivel universitario: sin código NGSS; se alinea con cursos introductorios de ciencias del sistema Tierra y ambientales.', view: 'Consultar en nextgenscience.org', badge: '¡Insignia ganada!', map: 'Explorador del planeta', sx: 'Constructor de satélites', cert: 'Imprimir mi certificado', name: 'Tu nombre o el de la clase (opcional)', certT: 'Certificado de descubrimiento', certB: 'ganó la insignia', on: 'el', site: 'Saving Planets: soluciones reales que ayudan a las personas y a la naturaleza' },
    ar: { std: 'التوافق مع المعايير (NGSS)', note: 'توقعات الأداء من معايير العلوم للجيل القادم (الولايات المتحدة) التي تدعمها هذه الخطة. راجع أيضًا معاييرك الوطنية.', uni: 'المستوى الجامعي: لا يوجد رمز NGSS، ويتوافق مع المقررات التمهيدية لعلوم نظام الأرض والبيئة.', view: 'ابحث في nextgenscience.org', badge: 'حصلت على شارة!', map: 'مستكشف الكوكب', sx: 'باني الأقمار الصناعية', cert: 'اطبع شهادتي', name: 'اسمك الأول أو اسم الصف (اختياري)', certT: 'شهادة اكتشاف', certB: 'حصل على شارة', on: 'في', site: 'Saving Planets: حلول حقيقية تساعد الناس والطبيعة' }
  }[lang] || null;
  if (!T) return;
  // NGSS performance expectations (codes and statements from nextgenscience.org)
  var PE = {
    'K-ESS3-3': 'Communicate solutions that will reduce the impact of humans on the land, water, air, and/or other living things in the local environment.',
    '1-ESS1-1': 'Use observations of the sun, moon, and stars to describe patterns that can be predicted.',
    '5-ESS3-1': "Obtain and combine information about ways individual communities use science ideas to protect the Earth's resources and environment.",
    '5-ESS2-1': 'Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or atmosphere interact.',
    '5-ESS1-2': 'Represent data in graphical displays to reveal patterns of daily changes in length and direction of shadows, day and night, and the seasonal appearance of some stars in the night sky.',
    'MS-ESS3-3': 'Apply scientific principles to design a method for monitoring and minimizing a human impact on the environment.',
    'MS-LS2-5': 'Evaluate competing design solutions for maintaining biodiversity and ecosystem services.',
    'MS-ESS1-2': 'Develop and use a model to describe the role of gravity in the motions within galaxies and the solar system.',
    'HS-ESS3-4': 'Evaluate or refine a technological solution that reduces impacts of human activities on natural systems.',
    'HS-LS2-7': 'Design, evaluate, and refine a solution for reducing the impacts of human activities on the environment and biodiversity.',
    'HS-ESS1-4': 'Use mathematical or computational representations to predict the motion of orbiting objects in the solar system.'
  };
  var SPACE = /Space|Rawane|Planetary_Defense/;
  function codes(band, hub) {
    var sp = SPACE.test(hub || '');
    return { k3: sp ? ['1-ESS1-1', 'K-ESS3-3'] : ['K-ESS3-3'], g45: sp ? ['5-ESS1-2', '5-ESS3-1'] : ['5-ESS3-1', '5-ESS2-1'],
      g68: sp ? ['MS-ESS1-2', 'MS-ESS3-3'] : ['MS-ESS3-3', 'MS-LS2-5'], g912: sp ? ['HS-ESS1-4', 'HS-ESS3-4'] : ['HS-ESS3-4', 'HS-LS2-7'], uni: [] }[band] || [];
  }
  var lb = document.getElementById('lb'), out = document.getElementById('lb-plan');
  if (lb && out) {
    var add = function () {
      if (!out.firstChild || out.querySelector('.lb-std')) return;
      var band = lb.elements.band ? lb.elements.band.value : '', hub = lb.elements.hub ? lb.elements.hub.value : '', c = codes(band, hub);
      var box = document.createElement('section'); box.className = 'lb-std';
      box.innerHTML = '<h3>' + T.std + '</h3>' + (c.length ? '<p class="lb-small">' + T.note + '</p><ul>' + c.map(function (k) {
        return '<li><span class="lb-std-code" dir="ltr">' + k + '</span> <span lang="en" dir="ltr">' + PE[k] + '</span> <a href="https://www.nextgenscience.org/search-standards?keys=' + encodeURIComponent(k) + '" target="_blank" rel="noopener">' + T.view + '</a></li>';
      }).join('') + '</ul>' : '<p>' + T.uni + '</p>');
      out.appendChild(box);
    };
    new MutationObserver(add).observe(out, { childList: true }); add();
  }
  // badges + certificate
  function store(k) { try { var b = JSON.parse(localStorage.getItem('sp_badges') || '{}'); if (b[k]) return false; b[k] = new Date().toISOString().slice(0, 10); localStorage.setItem('sp_badges', JSON.stringify(b)); } catch (e) {} return true; }
  function award(k, host) {
    store(k);
    if (!host || host.querySelector('.sp-badge')) return;
    var d = document.createElement('div'); d.className = 'sp-badge glass'; d.setAttribute('role', 'status');
    d.innerHTML = '<p class="sp-badge-t"><span aria-hidden="true">' + (k === 'map' ? '🌍' : '🛰️') + '</span> ' + T.badge + ' <b>' + T[k] + '</b></p>' +
      '<label class="sp-badge-l">' + T.name + '<input type="text" maxlength="40" autocomplete="off"></label><button type="button" class="btn">' + T.cert + '</button>';
    d.querySelector('button').addEventListener('click', function () { cert(k, d.querySelector('input').value.trim()); });
    host.appendChild(d);
  }
  function cert(k, who) {
    var w = window.open('', '_blank'); if (!w) return;
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var date = new Date().toLocaleDateString(document.documentElement.lang || 'en', { year: 'numeric', month: 'long', day: 'numeric' });
    w.document.write('<!doctype html><html lang="' + lang + '"' + (lang === 'ar' ? ' dir="rtl"' : '') + '><head><meta charset="utf-8"><title>' + esc(T.certT) + '</title><style>body{font-family:system-ui,sans-serif;margin:0;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#eaf6fc}.c{width:min(900px,92vw);aspect-ratio:1.414;border:10px double #009cde;border-radius:18px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2rem;box-sizing:border-box;color:#003755}h1{font-size:2.4rem;margin:.2rem}.em{font-size:4rem}.n{font-size:2rem;font-weight:800;border-bottom:2px solid #009cde;padding:0 1rem;min-width:50%}.s{margin-top:2rem;font-size:.9rem}@media print{body{background:#fff}}</style></head><body><div class="c"><div class="em">' + (k === 'map' ? '🌍' : '🛰️') + '</div><h1>' + esc(T.certT) + '</h1><p class="n">' + esc(who || '\u00a0') + '</p><p>' + esc(T.certB) + ' <b>' + esc(T[k]) + '</b> ' + esc(T.on) + ' ' + esc(date) + '</p><p class="s">' + esc(T.site) + '<br>www.savingplanets.com</p></div><script>setTimeout(function(){print()},300)<\/script></body></html>');
    w.document.close();
  }
  var km = document.getElementById('km');
  if (km) { var seen = {}; km.addEventListener('click', function (e) { var b = e.target.closest('[data-hub]'); if (!b) return; seen[b.dataset.hub] = 1;
    if (Object.keys(seen).length >= km.querySelectorAll('[data-hub]').length) award('map', document.getElementById('km-panel') ? document.getElementById('km-panel').parentNode : km); }); }
  document.addEventListener('sx:dock', function (e) { if (e.detail && e.detail.left === 0) { var sx = document.getElementById('sx'); award('sx', sx); } });
})();
