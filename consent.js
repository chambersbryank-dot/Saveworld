/* Consent-gated Google Analytics (GA4). GA4 runs in Consent Mode: analytics_storage stays denied (no analytics cookies) until the visitor clicks Accept.
   Choice is stored in localStorage as sp_consent = 'granted' | 'denied'. */
(function () {
  var KEY = 'sp_consent';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function loadGA() {
    // GA4 tag (G-ZCJ7CEKN94) is in every page <head> with Consent Mode default denied; grant on Accept.
    if (window.__spGaLoaded) return; window.__spGaLoaded = true;
    if (typeof window.gtag === 'function') gtag('consent', 'update', { analytics_storage: 'granted' });
  }
  function banner() {
    var css = '.sp-consent{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:9999;width:calc(100% - 24px);max-width:640px;box-sizing:border-box;display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;padding:12px 16px;background:#0b1f33;color:#e8eef5;border:1px solid rgba(0,156,222,0.45);border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,0.45);font:500 0.875rem/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;min-height:68px}' +
      '.sp-consent p{margin:0;flex:1 1 260px}.sp-consent a{color:#8fd3ff}.sp-consent-btns{display:flex;gap:8px;margin-left:auto}.sp-consent[dir=rtl] .sp-consent-btns{margin-left:0;margin-right:auto}' +
      '.sp-consent button{font:600 0.9rem system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;min-height:44px;min-width:88px;padding:10px 18px;border-radius:6px;cursor:pointer;border:1px solid #009cde}' +
      '.sp-consent .sp-accept{background:#009cde;color:#fff}.sp-consent .sp-decline{background:transparent;color:#e8eef5}' +
      '.sp-consent button:focus-visible{outline:2px solid #8fd3ff;outline-offset:2px}' +
      '@media (max-width:480px){.sp-consent{bottom:8px;padding:10px 12px;font-size:0.8rem}.sp-consent-btns{width:100%}.sp-consent button{flex:1}}';
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var d = document.createElement('div');
    d.className = 'sp-consent'; d.setAttribute('role', 'region'); d.setAttribute('aria-label', 'Analytics consent');
    var T = {
      en: ['We use Google Analytics to understand how visitors use the site. Accept or decline?', 'Privacy', 'Accept', 'Decline', 'Analytics consent'],
      fr: ['Nous utilisons Google Analytics pour comprendre comment les visiteurs utilisent le site. Accepter ou refuser ?', 'Confidentialité', 'Accepter', 'Refuser', 'Consentement aux statistiques'],
      es: ['Usamos Google Analytics para entender cómo los visitantes usan el sitio. ¿Aceptar o rechazar?', 'Privacidad', 'Aceptar', 'Rechazar', 'Consentimiento de analítica'],
      ar: ['نستخدم Google Analytics لفهم كيفية استخدام الزوار للموقع. هل تقبل أم ترفض؟', 'الخصوصية', 'قبول', 'رفض', 'الموافقة على التحليلات'],
      it: ['Usiamo Google Analytics per capire come i visitatori usano il sito. Accetti o rifiuti?', 'Privacy', 'Accetta', 'Rifiuta', 'Consenso alle statistiche']
    };
    var lang = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2), t = T[lang] || T.en;
    var about = lang === 'en' ? 'Privacy.html' : 'Privacy.html'; // Privacy.html exists in every language folder
    d.setAttribute('aria-label', t[4]);
    if (lang === 'ar') d.setAttribute('dir', 'rtl');
    d.innerHTML = '<p>' + t[0] + ' <a href="' + about + '">' + t[1] + '</a></p>' +
      '<div class="sp-consent-btns"><button type="button" class="sp-accept">' + t[2] + '</button><button type="button" class="sp-decline">' + t[3] + '</button></div>';
    d.querySelector('.sp-accept').addEventListener('click', function () { set('granted'); d.remove(); loadGA(); try { document.dispatchEvent(new Event('sp-consent-granted')); } catch (e) {} });
    d.querySelector('.sp-decline').addEventListener('click', function () { set('denied'); d.remove(); });
    document.body.appendChild(d);
  }
  var c = get();
  if (c === 'granted') loadGA();
  else if (c !== 'denied') {
    if (document.body) banner(); else document.addEventListener('DOMContentLoaded', banner);
  }
})();
