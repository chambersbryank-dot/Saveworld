#!/usr/bin/env python3
"""Oct 16 2026 (user: "Center page. Other than search bar and floating examples how to frame a AI question, get rid of
everything else but bottom information."). Rebuilds <main> of Search.html in en/fr/es/ar/it: a centred stage with only the
search bar and gently floating example-question chips (search/featured-questions.json via search/search-ui.js), results
below after a search, and the small credits at the bottom (Pagefind/model licences + the SI background credit). The h1 and
the "how to frame an SI question" note stay for screen readers only. Strings are read back from each language's page (the
i18n-build translations), so the generator is idempotent. Run after i18n-build.py and build-nav.py."""
import re, os, html, json
LANGS = ['en', 'fr', 'es', 'ar', 'it']; V = '20261016q'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import search_topics as ST
# Oct 16 7:12 PM (user): topic tabs (All / Aero / Orbital / Physics, ?topic=), chips placed at build time (no layout shift).
TOPIC_HEAD = ('<script>(function(){var t=(new URLSearchParams(location.search).get("topic")||"all").toLowerCase();'
              'if(!document.querySelector(\'.sp-tabs [data-t="\'+t+\'"]\'))t="all";document.documentElement.setAttribute("data-sp-topic",t)})();</script>')
TOPIC_JS = r"""<script>(function(){var d=document.documentElement,tl=document.querySelector('.sp-tabs');if(!tl)return;
var tabs=[].slice.call(tl.querySelectorAll('[role=tab]')),h1=document.getElementById('sp-h1'),baseH=h1.getAttribute('data-base'),baseT=document.title;
var alts=[].slice.call(document.querySelectorAll('link[rel=alternate][hreflang],#topnav .lang-switch a'));alts.forEach(function(a){a.setAttribute('data-href0',a.getAttribute('href'))});
function set(t,push,focus){var tab=tl.querySelector('[data-t="'+t+'"]')||tabs[0];t=tab.getAttribute('data-t');d.setAttribute('data-sp-topic',t);
 tabs.forEach(function(x){var on=x===tab;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1});if(focus)tab.focus();
 var nm=t==='all'?'':tab.textContent.trim();h1.textContent=nm?baseH+' · '+nm:baseH;document.title=nm?nm+' · '+baseT:baseT;
 alts.forEach(function(a){var h=a.getAttribute('data-href0');a.setAttribute('href',t==='all'?h:h.replace(/[?#].*$/,'')+'?topic='+t)});
 if(push){var u=new URLSearchParams(location.search);if(t==='all')u.delete('topic');else u.set('topic',t);var qs=u.toString();history.pushState({t:t},'',location.pathname+(qs?'?'+qs:''))}
 document.dispatchEvent(new CustomEvent('sp-topic',{detail:t}))}
tabs.forEach(function(x){x.addEventListener('click',function(e){e.preventDefault();if(x.getAttribute('aria-selected')!=='true')set(x.getAttribute('data-t'),true,false)})});
tl.addEventListener('keydown',function(e){var i=tabs.indexOf(document.activeElement);if(i<0)return;var r=getComputedStyle(tl).direction==='rtl',n=null;
 if(e.key==='ArrowRight')n=r?i-1:i+1;else if(e.key==='ArrowLeft')n=r?i+1:i-1;else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;else return;
 e.preventDefault();n=(n+tabs.length)%tabs.length;set(tabs[n].getAttribute('data-t'),true,true)});
window.addEventListener('popstate',function(){set((new URLSearchParams(location.search).get('topic')||'all').toLowerCase(),false,false)});
window.SP_TOPIC_BOOST=JSON.parse(tl.getAttribute('data-boost'));set(d.getAttribute('data-sp-topic')||'all',false,false)})();</script>"""
FEAT = json.load(open('search/featured-questions.json', encoding='utf8'))
def topic_sets(l):
    allq = FEAT.get(l) or (ST.IT_ALL if l == 'it' else FEAT['en'])
    return [('all', ST.ALL[l], allq[:12])] + [(t['id'], t['label'][l], t['q'][l]) for t in ST.TOPICS]
def chip(t, q, i):
    pre = '' if t == 'all' else f'topic={t}&amp;'
    return f'<a class="sp-q" data-t="{t}" href="?{pre}q={html.escape(__import__("urllib.parse").parse.quote(q))}" style="--i:{i}">{html.escape(q)}</a>'
def zones(l):
    z = ['', '', '', '']
    for t, _, qs in topic_sets(l):
        for i, q in enumerate(qs): z[i // 3] += chip(t, q, i)
    return z
def tabs(l):
    pre = '' 
    items = ''.join(f'<a role="tab" class="sp-tab" data-t="{t}" href="Search.html{"" if t == "all" else "?topic=" + t}" aria-selected="{"true" if t == "all" else "false"}" tabindex="{0 if t == "all" else -1}" aria-controls="sp-ring">{html.escape(lab)}</a>'
                    for t, lab, _ in topic_sets(l))
    boost = html.escape(json.dumps({t['id']: t['boost'] for t in ST.TOPICS}, separators=(',', ':')))
    return f'<div class="sp-tabs" role="tablist" aria-label="{html.escape(ST.TAB_LABEL[l])}" data-boost="{boost}">{items}</div>'
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
       # Oct 16 7:25 PM (user): "Liquid Glass" chips (blur + saturate, tinted, inner highlight, specular edge, static sheen) that
       # orbit gently on small ellipses (transform only: no layout, no CLS). Same direction per zone + phase offsets so chips never
       # meet each other; amplitude (8px) is below the ring gaps, so they never touch the bar or the tabs. Pause on hover/focus.
       '.sp-z .sp-q{position:relative!important;inset:auto!important;transform:none;display:inline-flex;align-items:center;width:min(250px,100%);min-height:64px;box-sizing:border-box;padding:.6rem 1.05rem;border-radius:20px;overflow:hidden;isolation:isolate;'
       'color:#f4faff!important;font:500 .9rem/1.35 Montserrat,system-ui,sans-serif;text-decoration:none!important;text-align:start;text-shadow:0 1px 2px rgba(0,20,40,.45);'
       'background:linear-gradient(135deg,rgba(143,211,255,.24),rgba(0,156,222,.12) 45%,rgba(0,55,85,.30));border:1px solid rgba(255,255,255,.26);'
       'box-shadow:inset 0 1px 0 rgba(255,255,255,.5),inset 0 -1px 0 rgba(0,0,0,.28),inset 0 0 0 1px rgba(143,211,255,.10),0 10px 26px rgba(0,8,20,.40);'
       '-webkit-backdrop-filter:blur(14px) saturate(180%);backdrop-filter:blur(14px) saturate(180%);'
       'animation:spx-orbit 14s linear infinite!important;animation-delay:calc(var(--z,0) * -3.5s)!important;will-change:transform;opacity:1!important}'
       '.sp-z .sp-q::before{content:"";position:absolute;inset:0;z-index:-1;border-radius:inherit;pointer-events:none;background:radial-gradient(120% 70% at 18% 0%,rgba(255,255,255,.34),rgba(255,255,255,0) 55%),linear-gradient(115deg,rgba(255,255,255,0) 40%,rgba(255,255,255,.10) 50%,rgba(255,255,255,0) 60%)}'
       '.sp-z .sp-q::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;padding:1px;background:linear-gradient(160deg,rgba(255,255,255,.65),rgba(255,255,255,0) 35%,rgba(143,211,255,0) 65%,rgba(143,211,255,.45));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}'
       '@supports not ((-webkit-backdrop-filter:blur(1px)) or (backdrop-filter:blur(1px))){.sp-z .sp-q{background:linear-gradient(135deg,#1d5f86,#0b3a57)}}'
       '.sp-zt{--z:0}.sp-zr{--z:1}.sp-zb{--z:2}.sp-zl{--z:3}'
       '.sp-z .sp-q:hover,.sp-z .sp-q:focus-visible{border-color:rgba(255,213,74,.9);animation-play-state:paused!important;background:linear-gradient(135deg,rgba(143,211,255,.34),rgba(0,156,222,.26) 45%,rgba(0,55,85,.36))}'
       '.sp-z .sp-q:focus-visible{outline:3px solid #ffd54a;outline-offset:3px}'
       '@keyframes spx-orbit{0%{transform:translate3d(8px,0,0)}12.5%{transform:translate3d(5.7px,4.2px,0)}25%{transform:translate3d(0,6px,0)}37.5%{transform:translate3d(-5.7px,4.2px,0)}50%{transform:translate3d(-8px,0,0)}62.5%{transform:translate3d(-5.7px,-4.2px,0)}75%{transform:translate3d(0,-6px,0)}87.5%{transform:translate3d(5.7px,-4.2px,0)}100%{transform:translate3d(8px,0,0)}}'
       '[dir=rtl] .sp-z .sp-q{animation-direction:reverse!important}'
       '@media (prefers-reduced-motion:reduce){.sp-z .sp-q{animation:none!important;transform:none!important}}'
       '.sp-ring{display:grid;width:min(1180px,100%);gap:1.6rem 2rem;align-items:center;justify-items:center;grid-template-columns:minmax(0,1fr) minmax(0,640px) minmax(0,1fr);grid-template-areas:"t t t" "l c r" "b b b"}'
       '.sp-ring .sp-search-form{grid-area:c}.sp-zt{grid-area:t}.sp-zl{grid-area:l}.sp-zr{grid-area:r}.sp-zb{grid-area:b}'
       '.sp-z{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:1.1rem 1.2rem}.sp-zl,.sp-zr{flex-direction:column}'
       
       '@media (max-width:1099px){.sp-z{gap:1.1rem .7rem}.sp-ring{grid-template-columns:minmax(0,1fr);grid-template-areas:"t" "l" "c" "r" "b"}.sp-zl,.sp-zr{flex-direction:row}.sp-ring .sp-search-form{width:min(640px,100%)}}'
       '.sp-stage:has(#results li) .sp-z{display:none!important}.sp-stage:has(#results li) .sp-ring{grid-template-areas:"c";grid-template-columns:minmax(0,1fr)}.sp-stage .sp-results-wrap{width:min(860px,100%);text-align:start}.sp-stage .sp-results-wrap:empty{display:none}'
       '.sp-stage .sp-status:empty,.sp-stage .search-mode:empty{display:none}'
       '.sp-credits{max-width:860px;margin:0 auto;padding:.4rem 1rem 1.2rem;text-align:center;font-size:.75rem;opacity:.85}.sp-credits p{margin:.2rem 0}'
       '.sp-mini-foot{text-align:center;font-size:.75rem;opacity:.8;padding:.4rem 1rem .8rem}.sp-mini-foot p{margin:0}.sp-mini-foot a{display:inline-block;min-height:24px;padding:2px 0}'
       'body.sp-search-page .sticky-help{display:none!important}.sp-stage{min-height:calc(100svh - 40px)}'
       '.sp-tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:.5rem;max-width:min(980px,100%);margin:.5rem auto 0}'
       '.sp-tab{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 1.1rem;border-radius:999px;border:1px solid rgba(143,211,255,.5);background:rgba(11,22,32,.7);color:#cfe9ff!important;font:600 .92rem/1.2 Montserrat,system-ui,sans-serif;text-decoration:none!important;white-space:nowrap;transition:background-color .2s,border-color .2s}'
       '.sp-tab:hover{border-color:#8fd3ff;background:rgba(0,156,222,.2)}.sp-tab[aria-selected=true]{background:#009cde;border-color:#009cde;color:#fff!important;box-shadow:0 6px 18px rgba(0,156,222,.35)}'
       '.sp-tab:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}'
       '.sp-ring .sp-q{display:none!important}html:not([data-sp-topic]) .sp-ring .sp-q[data-t=all],html[data-sp-topic=all] .sp-q[data-t=all],html[data-sp-topic=aero] .sp-q[data-t=aero],html[data-sp-topic=orbital] .sp-q[data-t=orbital],html[data-sp-topic=physics] .sp-q[data-t=physics]{display:inline-flex!important}'
       '.sr-only-x{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
       '.sp-gh{list-style:none;margin:1.1rem 0 .3rem}.sp-stage .sp-results .sp-gh-t{font-size:1rem!important;letter-spacing:.04em;text-transform:uppercase;opacity:.9;margin:0 0 .4rem;text-align:start}.sp-gh>ol{list-style:none;padding:0;margin:0;display:grid;gap:inherit}'
       '.sp-stage .sp-search-form{position:relative}.sp-sugg{position:absolute;top:100%;inset-inline:0;z-index:5;list-style:none;margin:.3rem 0 0;padding:.3rem;border-radius:14px;background:#0b1620;border:1px solid rgba(143,211,255,.6);text-align:start;box-shadow:0 10px 28px rgba(0,0,0,.45)}.sp-sugg[hidden]{display:none}.sp-sugg li{padding:.55rem .8rem;border-radius:10px;cursor:pointer;color:#e8eef5}.sp-sugg li[aria-selected=true],.sp-sugg li:hover{background:rgba(0,156,222,.35)}.sp-sugg .sp-sg{font-size:.78rem;opacity:.8;margin-inline-start:.5rem}</style>')
def build(l, s):
    i, j = s.find('<main id="main">'), s.find('</main>')
    m = s[i:j]
    h1 = grab(m, r'<h1[^>]*data-base="([^"]*)"') or grab(m, r'<h1[^>]*>(.*?)</h1>'); lab = grab(m, r'<label[^>]*for="q"[^>]*>(.*?)</label>', h1)
    ph = grab(m, r'<input[^>]*placeholder="([^"]*)"'); btn = grab(m, r'<button[^>]*class="sp-search-btn"[^>]*>(.*?)</button>')
    fl = grab(m, r'id="sp-float"[^>]*aria-label="([^"]*)"') or grab(m, r'aria-label="([^"]*)"[^>]*id="sp-float"')
    note = grab(m, r'<p[^>]*(?:sp-float-note|id="sp-note")[^>]*>(.*?)</p>')
    more = grab(m, r'<button[^>]*id="sp-more"[^>]*>(.*?)</button>'); refine = grab(m, r'<p[^>]*id="sp-refine"[^>]*>(.*?)</p>')
    msg = grab(m, r'(<div[^>]*id="sp-msg"[^>]*>.*?</div>)'); credits = re.findall(r'<p class="search-credit[^"]*">.*?</p>', m, re.S)
    ex = grab(m, r'(<p class="sp-empty-title">.*?</ul>)')
    assert h1 and ph and btn and msg, (l, 'missing strings')
    h1 = re.sub(r' · .*$', '', h1); Z = zones(l)
    main = ('<main id="main">\n' + CSS +
            f'<section class="sp-stage" id="solution" aria-labelledby="sp-h1"><h1 id="sp-h1" class="sr-only-x" data-base="{h1}">{h1}</h1>'
            + tabs(l) + TOPIC_HEAD +
            f'<div class="sp-ring" id="sp-ring"><div id="sp-float" class="spx-float sp-z sp-zt" role="group" aria-label="{fl}" aria-describedby="sp-note">{Z[0]}</div>'
            '<div class="sp-z sp-zl" role="group" aria-label="' + fl + '">' + Z[1] + '</div>'
            f'<form class="sp-search-form" role="search" action="Search.html" method="get"><label for="q" class="sr-only-x">{lab}</label>'
            f'<input id="q" name="q" type="search" placeholder="{ph}" autocomplete="off" enterkeyhint="search" aria-describedby="status sp-note">'
            f'<button type="submit" class="sp-search-btn">{btn}</button></form>'
            '<div class="sp-z sp-zr" role="group" aria-label="' + fl + '">' + Z[2] + '</div><div class="sp-z sp-zb" role="group" aria-label="' + fl + '">' + Z[3] + '</div></div>'
            f'<p id="sp-note" class="sr-only-x">{note}</p>' + TOPIC_JS +
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
def tag_pages():
    # Pagefind filter "topic" on every math/Learn/calculator page of a topic (all languages), so a topic tab can pull
    # them to the top (search-ui.js runs a filtered search first). Marker is stripped by i18n-build/i18n-check normalize.
    pages = {}
    for t in ST.TOPICS:
        for b in t['boost']: pages.setdefault(b, []).append(t['id'])
    n = 0
    for l in LANGS:
        for b, ts in pages.items():
            f = ('' if l == 'en' else l + '/') + b
            if not os.path.exists(f): continue
            s = open(f, encoding='utf8').read()
            blk = '<!-- SPTOPIC:START -->' + ''.join(f'<meta data-pagefind-filter="topic[content]" content="{t}">' for t in ts) + '<!-- SPTOPIC:END -->'
            s2 = re.sub(r'<!-- SPTOPIC:START -->.*?<!-- SPTOPIC:END -->', '', s, flags=re.S).replace('</head>', blk + '</head>', 1)
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-search-page: topic tags on {n} pages')
# Oct 25 2026 (founder, upgrade 4): result groups (Solution, Course, Fact, Mission) + as-you-type suggestions in search/search-ui.js.
# search/result-types.json = page -> group, from existing data only: course modules (scripts/courses/*.py PAGE, live) + Courses hub;
# fact pages; hub membership from search/hubs.json (mission hubs = satellites, telescopes and spacecraft; the other hubs = solutions).
# Anything else is 'page' (shown last as More pages). Group labels per language live in the hidden #sp-msg list (MSG_X below).
FACT_PAGES = ['Amazing_Facts.html', 'Myth_vs_Fact.html', 'Top_Ten.html', 'Glossary.html']
MISSION_HUBS = {'Earth_Observation.html', 'Space.html', 'Planetary_Defense.html', 'Space_Weather.html'}
MSG_X = {'g-solution': {'en': 'Solutions', 'fr': 'Solutions', 'es': 'Soluciones', 'ar': 'الحلول', 'it': 'Soluzioni', 'he': 'פתרונות'},
         'g-course': {'en': 'Courses', 'fr': 'Cours', 'es': 'Cursos', 'ar': 'الدورات', 'it': 'Corsi', 'he': 'קורסים'},
         'g-fact': {'en': 'Facts', 'fr': 'Faits', 'es': 'Datos', 'ar': 'حقائق', 'it': 'Fatti', 'he': 'עובדות'},
         'g-mission': {'en': 'Missions', 'fr': 'Missions', 'es': 'Misiones', 'ar': 'المهمات', 'it': 'Missioni', 'he': 'משימות'},
         'g-page': {'en': 'More pages', 'fr': 'Autres pages', 'es': 'Más páginas', 'ar': 'صفحات أخرى', 'it': 'Altre pagine', 'he': 'דפים נוספים'},
         'sugg': {'en': 'Suggestions', 'fr': 'Suggestions', 'es': 'Sugerencias', 'ar': 'اقتراحات', 'it': 'Suggerimenti', 'he': 'הצעות'}}
def result_types():
    t = {}
    hubs = json.load(open('search/hubs.json', encoding='utf8'))['hubOf']
    for pg, hub in hubs.items(): t[pg] = 'mission' if hub in MISSION_HUBS else 'solution'
    for pg in FACT_PAGES: t[pg] = 'fact'
    t['Courses.html'] = 'course'
    for f in sorted(os.listdir('scripts/courses')):
        if not f.endswith('.py'): continue
        src = open('scripts/courses/' + f, encoding='utf8').read()
        pm = re.search(r"^PAGE = '([^']+)'", src, re.M)
        if pm and re.search(r"^STATUS = 'live'", src, re.M): t[pm.group(1)] = 'course'
    for extra in ('Artemis_II.html', 'Nancy_Grace_Roman.html'):
        if os.path.exists(extra): t[extra] = 'mission'
    json.dump(dict(sorted(t.items())), open('search/result-types.json', 'w', encoding='utf8'), separators=(',', ':'))
    return len(t)
def add_msg(l, s):  # group / suggestion labels into #sp-msg (idempotent; all 6 languages, he included)
    def fix(m):
        d = re.sub(r'<span data-k="(?:g-[a-z]+|sugg)">.*?</span>', '', m.group(0))
        return d[:-6] + ''.join(f'<span data-k="{k}">{v[l]}</span>' for k, v in MSG_X.items()) + '</div>'
    return re.sub(r'<div[^>]*id="sp-msg"[^>]*>.*?</div>', fix, s, count=1, flags=re.S)
SUI_V = '20261025a'
if __name__ == '__main__':
    print('build-search-page: result types for', result_types(), 'pages')
    for l in LANGS + ['he']:
        f = ('' if l == 'en' else l + '/') + 'Search.html'
        s = open(f, encoding='utf8').read()
        s2 = re.sub(r'search-ui\.js\?v=[\w.-]+', 'search-ui.js?v=' + SUI_V, add_msg(l, s))
        if s2 != s: open(f, 'w', encoding='utf8').write(s2)
    tag_pages()
    n = 0
    for l in LANGS:
        f = ('' if l == 'en' else l + '/') + 'Search.html'
        s = open(f, encoding='utf8').read(); s2 = add_msg(l, build(l, s))
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-search-page: {n} pages')
