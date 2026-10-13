// Share bar (Batch A, Oct 12). No third-party scripts: plain links + the native Web Share API where available (iPad, phones).
(function () {
  var bars = document.querySelectorAll('.share-bar'); if (!bars.length) return;
  var link = document.querySelector('link[rel="canonical"]');
  var url = (link && link.href) || location.href.split('#')[0];
  var title = document.title, e = encodeURIComponent;
  bars.forEach(function (b) {
    var set = function (sel, href) { var a = b.querySelector(sel); if (a) a.href = href; };
    set('.share-x', 'https://twitter.com/intent/tweet?url=' + e(url) + '&text=' + e(title));
    set('.share-fb', 'https://www.facebook.com/sharer/sharer.php?u=' + e(url));
    set('.share-li', 'https://www.linkedin.com/sharing/share-offsite/?url=' + e(url));
    set('.share-mail', 'mailto:?subject=' + e(title) + '&body=' + e(url));
    var nat = b.querySelector('.share-native');
    if (nat && navigator.share) {
      nat.hidden = false;
      nat.addEventListener('click', function () { navigator.share({ title: title, url: url }).catch(function () {}); });
    }
    var cp = b.querySelector('.share-copy'), ok = b.querySelector('.share-ok');
    if (cp) cp.addEventListener('click', function () {
      var done = function () { if (ok) { ok.hidden = false; setTimeout(function () { ok.hidden = true; }, 2500); } };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { prompt('', url); });
      else { prompt('', url); }
    });
  });
})();
