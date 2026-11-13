/* Share bar. Plain links only. Nothing from X, Facebook, or LinkedIn loads until a button is used. */
(function () {
  var bars = document.querySelectorAll('.share-bar');
  if (!bars.length) return;
  var canon = document.querySelector('link[rel="canonical"]');
  var url = (canon && canon.href) || location.href.split('#')[0];
  var title = document.title;
  var enc = encodeURIComponent;
  Array.prototype.forEach.call(bars, function (bar) {
    function set(sel, href) {
      var a = bar.querySelector(sel);
      if (a) a.href = href;
    }
    set('.share-x', 'https://twitter.com/intent/tweet?url=' + enc(url) + '&text=' + enc(title));
    set('.share-fb', 'https://www.facebook.com/sharer/sharer.php?u=' + enc(url));
    set('.share-li', 'https://www.linkedin.com/sharing/share-offsite/?url=' + enc(url));
    set('.share-mail', 'mailto:?subject=' + enc(title) + '&body=' + enc(title + '\n\n' + url));
    var nativeBtn = bar.querySelector('.share-native');
    if (nativeBtn && navigator.share) {
      nativeBtn.hidden = false;
      nativeBtn.addEventListener('click', function () {
        navigator.share({ title: title, url: url }).catch(function () {});
      });
    }
    var copyBtn = bar.querySelector('.share-copy');
    var status = bar.querySelector('.share-ok');
    if (!copyBtn) return;
    var label = copyBtn.getAttribute('data-label') || copyBtn.textContent;
    var copied = bar.getAttribute('data-copied') || 'Copied';
    copyBtn.addEventListener('click', function () {
      function done() {
        if (status) status.textContent = copied;
        copyBtn.setAttribute('aria-label', copied);
        setTimeout(function () {
          if (status) status.textContent = '';
          copyBtn.setAttribute('aria-label', label);
        }, 2500);
      }
      function fallback() {
        var area = document.createElement('textarea');
        area.value = url;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.left = '-9999px';
        document.body.appendChild(area);
        area.select();
        try { document.execCommand('copy'); done(); } catch (err) {}
        document.body.removeChild(area);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback);
      else fallback();
    });
  });
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var node = document.getElementById(btn.getAttribute('data-copy'));
    if (!node) return;
    var text = (node.getAttribute('data-copy-text') || node.textContent || '').replace(/^\s+|\s+$/g, '');
    var status = btn.parentNode.querySelector('.share-ok');
    var label = btn.getAttribute('data-label') || btn.textContent;
    var copied = btn.getAttribute('data-copied') || 'Copied';
    function done() {
      if (status) status.textContent = copied;
      btn.setAttribute('aria-label', copied);
      setTimeout(function () {
        if (status) status.textContent = '';
        btn.setAttribute('aria-label', label);
      }, 2500);
    }
    function fallback() {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.left = '-9999px';
      document.body.appendChild(area);
      area.select();
      try { document.execCommand('copy'); done(); } catch (err) {}
      document.body.removeChild(area);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  });
})();
