/* Oct 16 2026: share bar on Learn and Teachers pages. Google Classroom = plain link to Google's official share URL (no Google
   script; nothing goes to Google unless clicked). Copy link uses the Clipboard API with a select() fallback. Clicks are counted
   (kind + page type only) through the privacy-safe events endpoint (site.js spTrack, skipped under DNT/GPC). */
(function () {
  var bars = document.querySelectorAll('.shr'); if (!bars.length) return;
  function track(kind, bar) { try { if (window.spTrack) window.spTrack('share', { kind: kind, page: bar.getAttribute('data-page') }); } catch (e) {} }
  Array.prototype.forEach.call(bars, function (bar) {
    var a = bar.querySelector('.shr-cr'), b = bar.querySelector('.shr-copy'), st = bar.querySelector('.shr-st'), url = bar.getAttribute('data-url');
    a.addEventListener('click', function () { track('classroom', bar); });
    b.addEventListener('click', function () {
      function ok() { st.textContent = b.getAttribute('data-ok'); b.classList.add('is-done'); setTimeout(function () { b.classList.remove('is-done'); st.textContent = ''; }, 4000); }
      function fallback() { var t = document.createElement('textarea'); t.value = url; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); ok(); } catch (e) { st.textContent = url; } document.body.removeChild(t); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, fallback); else fallback();
      track('copy', bar);
    });
  });
})();
