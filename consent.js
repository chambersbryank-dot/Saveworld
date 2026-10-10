/* Consent-gated Google Analytics (GA4). Nothing from Google loads until the visitor clicks Accept.
   Choice is stored in localStorage as sp_consent = 'granted' | 'denied'. */
(function () {
  var GA_ID = 'G-M5L2259Z68', KEY = 'sp_consent';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function loadGA() {
    if (window.__spGaLoaded) return; window.__spGaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', GA_ID);
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  function banner() {
    var css = '.sp-consent{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:9999;width:calc(100% - 24px);max-width:640px;box-sizing:border-box;display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;padding:12px 16px;background:#0b1f33;color:#e8eef5;border:1px solid rgba(0,156,222,0.45);border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,0.45);font:500 0.875rem/1.45 Montserrat,system-ui,sans-serif}' +
      '.sp-consent p{margin:0;flex:1 1 260px}.sp-consent a{color:#8fd3ff}.sp-consent-btns{display:flex;gap:8px;margin-left:auto}' +
      '.sp-consent button{font:600 0.85rem Montserrat,system-ui,sans-serif;padding:7px 16px;border-radius:6px;cursor:pointer;border:1px solid #009cde}' +
      '.sp-consent .sp-accept{background:#009cde;color:#fff}.sp-consent .sp-decline{background:transparent;color:#e8eef5}' +
      '.sp-consent button:focus-visible{outline:2px solid #8fd3ff;outline-offset:2px}' +
      '@media (max-width:480px){.sp-consent{bottom:8px;padding:10px 12px;font-size:0.8rem}.sp-consent-btns{width:100%}.sp-consent button{flex:1}}';
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var d = document.createElement('div');
    d.className = 'sp-consent'; d.setAttribute('role', 'region'); d.setAttribute('aria-label', 'Analytics consent');
    d.innerHTML = '<p>We use Google Analytics to understand how visitors use the site. Accept or decline? <a href="About.html">About us</a></p>' +
      '<div class="sp-consent-btns"><button type="button" class="sp-accept">Accept</button><button type="button" class="sp-decline">Decline</button></div>';
    d.querySelector('.sp-accept').addEventListener('click', function () { set('granted'); d.remove(); loadGA(); });
    d.querySelector('.sp-decline').addEventListener('click', function () { set('denied'); d.remove(); });
    document.body.appendChild(d);
  }
  var c = get();
  if (c === 'granted') loadGA();
  else if (c !== 'denied') {
    if (document.body) banner(); else document.addEventListener('DOMContentLoaded', banner);
  }
})();
