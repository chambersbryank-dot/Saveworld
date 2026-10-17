#!/usr/bin/env python3
"""Oct 16 2026 (user: "Center page. Other than search bar and floating examples how to frame a AI question, get rid of
everything else but bottom information."). Rebuilds <main> of Search.html in en/fr/es/ar/it: a centred stage with only the
search bar and gently floating example-question chips (search/featured-questions.json via search/search-ui.js), results
below after a search, and the small credits at the bottom (Pagefind/model licences + the SI background credit). The h1 and
the "how to frame an SI question" note stay for screen readers only. Strings are read back from each language's page (the
i18n-build translations), so the generator is idempotent. Run after i18n-build.py and build-nav.py."""
import re, os, html, json
LANGS = ['en', 'fr', 'es', 'ar', 'it']; V = '20261016q'
RING_JS = ('<script>(function(){var t=document.getElementById("sp-float");if(!t)return;var z=[".sp-zl",".sp-zr",".sp-zb"].map(function(c){return document.querySelector(c)});'
           'function spread(){var q=[].slice.call(t.querySelectorAll(".sp-track > .sp-q"));if(q.length<4)return false;var d=t.querySelector(".sp-dup");if(d)d.remove();'
           'var n=Math.ceil(q.length/4);q.forEach(function(a,i){var k=Math.floor(i/n);if(k>0)z[k-1].appendChild(a)});return true}'
           'if(!spread()){var mo=new MutationObserver(function(){if(spread())mo.disconnect()});mo.observe(t,{childList:true,subtree:true})}})();</script>')
def grab(s, pat, default=''):
    m = re.search(pat, s, re.S); return m.group(1).strip() if m else default
CSS = ('<style>/* SPSTAGE */body.sp-search-page main#main{display:block}'
       '.sp-stage{min-height:calc(100svh - 120px);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.4rem;padding:2rem 1rem 1.5rem;box-sizing:border-box;text-align:center;position:relative;z-index:0;isolation:isolate;overflow:hidden;padding-top:calc(var(--nav-height,96px) + 32px);'
       'background:radial-gradient(ellipse at 50% 35%,rgba(0,156,222,.18),transparent 60%)}'
       '.sp-stage:has(#results li){justify-content:flex-start;padding-top:2.5rem}'
       '.sp-stage .sp-search-form{display:flex;gap:.6rem;width:min(720px,100%);margin:0;position:static}'
       '.sp-stage .sp-search-form input{flex:1;min-width:0;min-height:52px;font:inherit;font-size:1.1rem;padding:.4rem 1.1rem;border-radius:999px;border:2px solid rgba(143,211,255,.75);background:rgba(11,22,32,.85);color:#e8eef5;box-sizing:border-box}'
       '.sp-stage .sp-search-form input:focus,.sp-stage .sp-search-form input:focus-visible{outline:none;border-color:#ffd54a;box-shadow:0 0 0 4px rgba(255,213,74,.28),0 8px 28px rgba(0,156,222,.35)}'
       '.sp-stage .sp-search-btn{min-height:52px;min-width:52px;padding:0 1.4rem;border-radius:999px;font:700 1.05rem Montserrat,system-ui,sans-serif;cursor:pointer;border:0;background:#009cde;color:#fff}'
       '.sp-stage .sp-search-btn:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}'
       '.spx-float{position:static!important;inset:auto!important;width:min(980px,100%);margin:0!important;padding:0!important;overflow:visible!important;-webkit-mask-image:none!important;mask-image:none!important;pointer-events:auto!important}'
       '.spx-float .sp-track{display:flex!important;flex-wrap:wrap;justify-content:center;gap:.7rem;animation:none!important;transform:none!important;width:auto!important}'
       '.spx-float .sp-dup{display:none!important}'
       '.sp-z .sp-q{position:static!important;inset:auto!important;transform:none;display:inline-flex;align-items:center;min-height:44px;width:min(250px,100%);min-height:64px;box-sizing:border-box;padding:.55rem 1rem;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.35);'
       'border:1px solid rgba(143,211,255,.45);background:rgba(0,55,85,.55);color:#e8f4ff!important;font:500 .9rem/1.35 Montserrat,system-ui,sans-serif;text-decoration:none!important;text-align:start;'
       'animation:spx-bob 9s ease-in-out infinite!important;will-change:transform;animation-delay:calc(var(--i,0) * -0.7s)!important;opacity:1!important;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}'
       '.sp-z .sp-q:nth-child(3n+2){animation-duration:11s!important}.sp-z .sp-q:nth-child(3n){animation-duration:13s!important}'
       '.sp-z .sp-q:hover,.sp-z .sp-q:focus-visible{border-color:#ffd54a;background:rgba(0,156,222,.35);animation-play-state:paused!important}'
       '.sp-z .sp-q:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}'
       '@keyframes spx-bob{0%,100%{transform:translate3d(0,0,0)}33%{transform:translate3d(3px,-4px,0)}66%{transform:translate3d(-3px,-2px,0)}}'
       '@media (prefers-reduced-motion:reduce){.sp-z .sp-q{animation:none!important}}'
       '.sp-ring{display:grid;width:min(1180px,100%);gap:1.1rem 1.4rem;align-items:center;justify-items:center;grid-template-columns:minmax(0,1fr) minmax(0,640px) minmax(0,1fr);grid-template-areas:"t t t" "l c r" "b b b"}'
       '.sp-ring .sp-search-form{grid-area:c}.sp-zt{grid-area:t}.sp-zl{grid-area:l}.sp-zr{grid-area:r}.sp-zb{grid-area:b}'
       '.sp-z{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:.7rem}.sp-zl,.sp-zr{flex-direction:column}'
       
       '@media (max-width:1099px){.sp-ring{grid-template-columns:minmax(0,1fr);grid-template-areas:"t" "l" "c" "r" "b"}.sp-zl,.sp-zr{flex-direction:row}.sp-ring .sp-search-form{width:min(640px,100%)}}'
       '.sp-stage:has(#results li) .sp-z{display:none!important}.sp-stage:has(#results li) .sp-ring{grid-template-areas:"c";grid-template-columns:minmax(0,1fr)}.sp-stage .sp-results-wrap{width:min(860px,100%);text-align:start}.sp-stage .sp-results-wrap:empty{display:none}'
       '.sp-stage .sp-status:empty,.sp-stage .search-mode:empty{display:none}'
       '.sp-credits{max-width:860px;margin:0 auto;padding:.4rem 1rem 1.2rem;text-align:center;font-size:.75rem;opacity:.85}.sp-credits p{margin:.2rem 0}'
       '.sp-mini-foot{text-align:center;font-size:.75rem;opacity:.8;padding:.4rem 1rem .8rem}.sp-mini-foot p{margin:0}.sp-mini-foot a{display:inline-block;min-height:24px;padding:2px 0}'
       'body.sp-search-page .sticky-help{display:none!important}.sp-stage{min-height:calc(100svh - 40px)}'
       '.sr-only-x{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}</style>')
def build(l, s):
    i, j = s.find('<main id="main">'), s.find('</main>')
    m = s[i:j]
    h1 = grab(m, r'<h1[^>]*>(.*?)</h1>'); lab = grab(m, r'<label[^>]*for="q"[^>]*>(.*?)</label>', h1)
    ph = grab(m, r'<input[^>]*placeholder="([^"]*)"'); btn = grab(m, r'<button[^>]*class="sp-search-btn"[^>]*>(.*?)</button>')
    fl = grab(m, r'id="sp-float"[^>]*aria-label="([^"]*)"') or grab(m, r'aria-label="([^"]*)"[^>]*id="sp-float"')
    note = grab(m, r'<p[^>]*(?:sp-float-note|id="sp-note")[^>]*>(.*?)</p>')
    more = grab(m, r'<button[^>]*id="sp-more"[^>]*>(.*?)</button>'); refine = grab(m, r'<p[^>]*id="sp-refine"[^>]*>(.*?)</p>')
    msg = grab(m, r'(<div[^>]*id="sp-msg"[^>]*>.*?</div>)'); credits = re.findall(r'<p class="search-credit[^"]*">.*?</p>', m, re.S)
    ex = grab(m, r'(<p class="sp-empty-title">.*?</ul>)')
    assert h1 and ph and btn and msg, (l, 'missing strings')
    main = ('<main id="main">\n' + CSS +
            f'<section class="sp-stage" id="solution" aria-labelledby="sp-h1"><h1 id="sp-h1" class="sr-only-x">{h1}</h1>'
            f'<div class="sp-ring"><div id="sp-float" class="spx-float sp-z sp-zt" role="group" aria-label="{fl}" aria-describedby="sp-note"></div>'
            '<div class="sp-z sp-zl" role="group" aria-label="' + fl + '"></div>'
            f'<form class="sp-search-form" role="search" action="Search.html" method="get"><label for="q" class="sr-only-x">{lab}</label>'
            f'<input id="q" name="q" type="search" placeholder="{ph}" autocomplete="off" enterkeyhint="search" aria-describedby="status sp-note">'
            f'<button type="submit" class="sp-search-btn">{btn}</button></form>'
            '<div class="sp-z sp-zr" role="group" aria-label="' + fl + '"></div><div class="sp-z sp-zb" role="group" aria-label="' + fl + '"></div></div>'
            f'<p id="sp-note" class="sr-only-x">{note}</p>' + RING_JS +
            f'<div class="sp-results-wrap"><p id="status" class="sp-status" aria-live="polite"></p><p id="search-mode" class="search-mode" aria-live="polite"></p>'
            f'<div id="sp-empty" class="sp-empty" hidden>{ex}</div><ol id="results" class="sp-results"></ol>'
            f'<button type="button" id="sp-more" class="sp-more" hidden>{more}</button><p id="sp-refine" class="sp-refine" hidden>{refine}</p>{msg}</div></section>\n'
            )
    out = s[:i] + main + s[j:]
    # Oct 16 6:07 PM (user): no footer on Search pages; keep one tiny legal line (licence + privacy).
    fm = re.search(r'<footer\b.*?</footer>', out, re.S)
    foot = fm.group(0)
    priv = grab(foot, r'<a[^>]*href="(?:\.\./)?Privacy\.html"[^>]*>(.*?)</a>') or grab(s, r'<p class="sp-mini-foot-p">.*?Privacy\.html"[^>]*>(.*?)</a>', 'Privacy')
    pre = '' if l == 'en' else '../'
    mini = (f'<footer class="sp-mini-foot" data-pagefind-ignore="all"><p class="sp-mini-foot-p">© 2026 Saving Planets · '
            f'<a rel="license" href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a> · <a href="{"Privacy.html" if l == "en" or os.path.exists(l + "/Privacy.html") else "../Privacy.html"}">{priv}</a></p></footer>')
    return out[:fm.start()] + mini + out[fm.end():]
if __name__ == '__main__':
    n = 0
    for l in LANGS:
        f = ('' if l == 'en' else l + '/') + 'Search.html'
        s = open(f, encoding='utf8').read(); s2 = build(l, s)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-search-page: {n} pages')
