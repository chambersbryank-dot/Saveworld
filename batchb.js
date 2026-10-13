/* Batch B (Oct 12): glossary tap/hover popovers, Cite This Page, teacher-sheet printing. */
(function () {
  var L = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  var T = { fr: { copied: 'Copié !', retrieved: 'Consulté le', from: 'sur', accessed: 'Consulté le' },
            es: { copied: '¡Copiado!', retrieved: 'Recuperado el', from: 'de', accessed: 'Consultado el' },
            ar: { copied: 'تم النسخ!', retrieved: 'استُرجع في', from: 'من', accessed: 'تاريخ الوصول' },
            en: { copied: 'Copied!', retrieved: 'Retrieved', from: 'from', accessed: 'Accessed' } }[L] || null;
  T = T || { copied: 'Copied!', retrieved: 'Retrieved', from: 'from', accessed: 'Accessed' };
  // --- glossary popovers: tap/click toggles (works on iPad), hover on mouse devices, Esc / outside tap closes
  var open = null, canHover = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  function pop(b) { return document.getElementById(b.getAttribute('aria-controls')); }
  function close() { if (open) { open.setAttribute('aria-expanded', 'false'); var p = pop(open); if (p) p.hidden = true; open = null; } }
  function show(b) { if (open === b) return; close(); var p = pop(b); if (!p) return; p.hidden = false; b.setAttribute('aria-expanded', 'true'); open = b;
    var r = p.getBoundingClientRect(); if (r.right > innerWidth - 8) p.style.insetInlineStart = Math.min(0, innerWidth - 8 - r.right) + 'px'; }
  document.querySelectorAll('.gl-term').forEach(function (b) {
    b.addEventListener('click', function (e) { e.stopPropagation(); if (open === b) close(); else show(b); });
    if (canHover) { var w = b.parentNode, t; w.addEventListener('mouseenter', function () { clearTimeout(t); show(b); }); w.addEventListener('mouseleave', function () { t = setTimeout(function () { if (open === b) close(); }, 200); }); }
  });
  document.addEventListener('click', function (e) { if (open && !open.parentNode.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && open) { var b = open; close(); b.focus(); } });
  // --- cite this page
  var box = document.querySelector('.cite-box');
  if (box) {
    var h1 = document.querySelector('h1'), title = h1 ? h1.textContent.trim() : document.title.split('|')[0].trim();
    var url = location.origin + location.pathname, d = new Date();
    var loc = L === 'en' ? 'en-US' : L, apaDate = d.toLocaleDateString(loc, { year: 'numeric', month: 'long', day: 'numeric' });
    var mlaDate = L === 'en' ? d.getDate() + ' ' + d.toLocaleDateString('en-US', { month: 'short' }) + (d.getMonth() === 4 ? '' : '.') + ' ' + d.getFullYear() : apaDate;
    var apa = box.querySelector('[data-cite="apa"]'), mla = box.querySelector('[data-cite="mla"]');
    if (apa) apa.textContent = 'Saving Planets. (n.d.). ' + title + '. ' + T.retrieved + ' ' + apaDate + ', ' + T.from + ' ' + url;
    if (mla) mla.textContent = '\u201C' + title + '.\u201D Saving Planets, ' + url + '. ' + T.accessed + ' ' + mlaDate + '.';
    box.querySelectorAll('.cite-copy').forEach(function (b) {
      b.addEventListener('click', function () {
        var txt = b.parentNode.querySelector('.cite-text').textContent, orig = b.textContent;
        function done() { b.textContent = T.copied; setTimeout(function () { b.textContent = orig; }, 1800); }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, fallback); else fallback();
        function fallback() { var r = document.createRange(), s = getSelection(); r.selectNodeContents(b.parentNode.querySelector('.cite-text')); s.removeAllRanges(); s.addRange(r); try { document.execCommand('copy'); done(); } catch (e) {} }
      });
    });
  }
  // --- teacher sheet printing
  var tb = document.querySelector('.teacher-box');
  if (tb && !tb.querySelector('.print-only')) { var p = document.createElement('p'); p.className = 'print-only'; p.textContent = 'Saving Planets \u00B7 ' + location.origin + location.pathname; tb.appendChild(p); }
  document.querySelectorAll('.print-sheet').forEach(function (b) { b.addEventListener('click', function () { close(); window.print(); }); });
  if (/[?&]print=1\b/.test(location.search) && tb) setTimeout(function () { window.print(); }, 600);
})();
