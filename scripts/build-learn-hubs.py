#!/usr/bin/env python3
"""Oct 26 2026 (founder): Learn information architecture, 6 languages (en fr es ar it he), runs right after build-nav.py.
- Learn.html landing: vision statement in the hero, six topic cards (Aeronautical Engineering first), a short "More ways to learn" row.
  No Start-here block, no flat course list, no calculator entries, no long intro.
- Topic hubs Learn_{Aero,Orbits,Physics,Math,Engineering,Chemistry}.html built from each language's Learn.html chrome.
  Learn_Aero.html holds the four-year roadmap (year/semester, prerequisites, localStorage progress, up next, upcoming checks/exams).
  Every hub embeds the calculator widget (assets/learn-hubs.js): subject tabs + calculator tabs (ARIA tabs, arrow keys), auto-primed
  by the hub topic or by #calc-<id> from a course page; it iframes the existing <Calc>_Calculator.html?embed=1 pages (formulas unchanged).
- Learn nav dropdown (every page): Learn, the six hubs, Courses, Cadets, AP/IB, Careers. Homeschool and Calculators removed
  (their pages stay reachable by URL; Homeschool.html is no longer linked from anywhere).
- Course pages: breadcrumb Learn › topic hub › code, plus roadmap position and calculator link.
Text: scripts/learn_hubs_text.py. Course names/codes come from each language's Courses.html. Idempotent."""
import re, os, sys, html, datetime
sys.path.insert(0, 'scripts')
import learn_hubs_text as X
import rocket_path_text as R  # Oct 28 2026 (founder): Rocket Propulsion track page (+ 'Learn from the best' on both tracks)
import jet_path_text as J  # Oct 27/28 (founder): separate Aerospace (Jet Propulsion) track page + planet tie-in on both paths
from courses import roadmap as RM
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
SITE = 'https://www.savingplanets.com/'
JSV = '20261026a'
d = lambda l: '' if l == 'en' else l + '/'
def rd(f): return open(f, encoding='utf-8').read()
def wr(f, s):
    if os.path.exists(f) and rd(f) == s: return 0
    open(f, 'w', encoding='utf-8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
IDS = [c[0] for _, cs in RM.YEARS for c in cs]
def courses(l):
    s = rd(d(l) + 'Courses.html')
    cs = re.findall(r'<h3><a href="(?:\.\./)?([\w_]+\.html)">(.*?)</a></h3><p>(.*?)</p><p class="crs-kicker">(.*?)</p>', s)
    assert len(cs) == len(IDS) == 30, (l, len(cs))
    years = re.findall(r'<section id="y\d"><h2>(.*?)</h2>', s)
    return {i: dict(page=p, name=n, desc=t, code=k) for i, (p, n, t, k) in zip(IDS, cs)}, years
def navlabels(l):
    s = rd(d(l) + 'index.html'); out = {}
    for p, t in re.findall(r'<a href="(?:\.\./)?([\w_-]+\.html)"[^>]*>([^<]+)</a>', s):
        out.setdefault(p, t)
    c = rd(d(l) + 'Calculators.html')
    for p, t in re.findall(r'<li><a href="(?:\.\./)?(\w+_Calculator\.html)">(.*?)<span>', c): out[p] = t
    return out
TOP = {t[0]: t for t in X.TOPICS}
ROAD = {r[0]: r for r in X.ROAD}
CALCPAGE = {cid: (subj, p) for subj, cl in X.CALCS for cid, p in cl}
def u(k, l, **kw):
    s = X.UI[k][l]
    for a, b in kw.items(): s = s.replace('{' + a + '}', str(b))
    return s
def calc_widget(l, subj, NL):
    tabs = ''.join(f'<button type="button" role="tab" id="lhs-{s}" aria-controls="lhp" aria-selected="false" tabindex="-1" data-subj="{s}">{esc(TOP[s][3][l])}</button>' for s, _ in X.CALCS)
    data = ''.join(f'<li data-subj="{s}" data-calc="{c}" data-src="{p}?embed=1" data-full="{p}">{NL.get(p, p)}</li>' for s, cl in X.CALCS for c, p in cl)
    return (f'<section class="lhc" id="calc" aria-labelledby="lhc-h" data-default="{subj}"><h2 id="lhc-h">🧮 {esc(u("calc", l))}</h2>'
            f'<p class="lhc-lab" id="lhs-lab">{esc(u("subject", l))}</p><div class="lhc-tabs" role="tablist" aria-labelledby="lhs-lab">{tabs}</div>'
            f'<p class="lhc-lab" id="lhk-lab">{esc(u("tool", l))}</p><div class="lhc-tabs lhc-k" role="tablist" aria-labelledby="lhk-lab"></div>'
            f'<div id="lhp" role="tabpanel" tabindex="0"><iframe title="" loading="lazy"></iframe><p><a class="lhc-full" href="#">{esc(u("full", l))} ↗</a></p></div>'
            f'<ul hidden class="lhc-data">{data}</ul></section>')
CSS = ('<style>.lhv{font-size:1.12rem;max-width:46rem}.lht{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:.9rem;list-style:none;padding:0;margin:1rem 0}'
       '.lht a{display:flex;flex-direction:column;gap:.3rem;height:100%;box-sizing:border-box;padding:1rem 1.1rem;border-radius:18px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);text-decoration:none;color:inherit}'
       '.lht a:hover,.lht a:focus-visible{border-color:#ffd54a}.lht b{font-size:1.15rem}.lht small{opacity:.85}.lht .lht-main{grid-column:1/-1}.lht .lht-main a{border-color:#ffd54a;background:rgba(255,213,74,.09)}'
       '.lhm{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;padding:0}.lhm a{display:inline-flex;align-items:center;min-height:44px;padding:.3rem .9rem;border-radius:999px;border:1px solid rgba(255,255,255,.35);text-decoration:none;color:inherit;font-weight:700}'
       '.lhc{margin:1.6rem 0;padding:1rem;border-radius:18px;border:1px solid rgba(255,213,74,.5);background:rgba(255,255,255,.04)}.lhc-lab{margin:.4rem 0 .2rem;font-weight:700;font-size:.9rem}'
       '.lhc-tabs{display:flex;flex-wrap:wrap;gap:.4rem}.lhc-tabs button{min-height:44px;padding:.3rem .9rem;border-radius:999px;font:inherit;cursor:pointer;border:1px solid rgba(255,255,255,.4);background:transparent;color:inherit}'
       '.lhc-tabs button[aria-selected=true]{background:#ffd54a;color:#1a1300;font-weight:800}.lhc-tabs button:focus-visible,#lhp:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}'
       '#lhp iframe{width:100%;height:760px;border:0;border-radius:14px;background:#0b1620;margin-top:.8rem}@media(max-width:600px){#lhp iframe{height:980px}}'
       '.lhy{margin:1.2rem 0;padding:.2rem 1rem 1rem;border-radius:18px;border:1px solid rgba(255,255,255,.18)}.lhs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1rem}'
       '.lhs h4{margin:.6rem 0 .3rem}.lhs ol{list-style:none;padding:0;margin:0;display:grid;gap:.5rem}.lhs li{padding:.55rem .75rem;border-radius:12px;background:rgba(0,0,0,.22);border-inline-start:4px solid #8fd3ff}'
       '.lhs li.is-done{border-inline-start-color:#7cfc98;opacity:.8}.lhs li a{font-weight:800}.lhs .k{display:block;font-size:.82rem;opacity:.85}.lhs label{display:inline-flex;align-items:center;gap:.4rem;min-height:44px;font-size:.9rem}'
       '.lhs input{width:22px;height:22px}.lhp-bar{height:14px;border-radius:999px;background:rgba(255,255,255,.15);overflow:hidden}.lhp-bar span{display:block;height:100%;background:#7cfc98;width:0}'
       '.lhn{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:1rem}.lhn>div{padding:.8rem 1rem;border-radius:14px;background:rgba(255,255,255,.05)}.lhn ul{margin:.3rem 0;padding-inline-start:1.1rem}'
       '.lhr button{min-height:44px;border-radius:999px;padding:.3rem 1rem;font:inherit;cursor:pointer}.lhyt{display:flex;flex-wrap:wrap;gap:.4rem;list-style:none;padding:0}.lhyt a{display:inline-flex;min-height:44px;align-items:center;padding:.2rem .9rem;border-radius:999px;border:1px solid rgba(255,255,255,.35);font-weight:700;text-decoration:none;color:inherit}</style>')
def nav_block(l, NL, cur=None):
    items = [('Learn.html', '🎓 ' + u('learn', l))] + [(t[1], f'{t[2]} {t[3][l]}') for t in X.TOPICS[:1]] + [(J.PAGE, '🔥 ' + J.SHORT[l]), (R.PAGE, '🚀 ' + R.SHORT[l])] + [(t[1], f'{t[2]} {t[3][l]}') for t in X.TOPICS[1:]] + [(p, NL[p]) for p in ('Courses.html', 'Cadets.html', 'AP_IB_Physics.html', 'Careers.html') if p in NL]
    return ''.join(f'<li><a href="{p}"' + (' aria-current="page"' if p == cur else '') + f'>{t if "&" in t else esc(t)}</a></li>' for p, t in items)
def set_nav(s, l, NL, cur):
    return re.sub(r'(<ul class="spn-sub" id="spn-le">).*?(</ul>)', lambda m: m.group(1) + nav_block(l, NL, cur) + m.group(2), s, count=1, flags=re.S)
def page_from_learn(l, page, title, desc, main_inner, NL):
    s = rd(d(l) + 'Learn.html')
    hi = s.index('</head>'); head = s[:hi]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(title) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = head.replace('/Learn.html', '/' + page).replace('/Learn.jpg', '/Learn.jpg')
    rest = s[hi:]
    b0 = rest.index('<main'); b1 = rest.index('</main>')
    pre = rest[:b0]; post = rest[b1:]
    pre = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Learn.html', page), pre, flags=re.S)
    pre = set_nav(pre.replace(' aria-current="page"', ''), l, NL, page)
    hero = re.search(r'<section class="page-hero.*?</section>', rest[b0:b1], re.S).group(0)
    hero = re.sub(r'<div class="page-hero-content">.*?</div>', f'<div class="page-hero-content"><h1>{esc(title)}</h1><p>{esc(desc)}</p></div>', hero, count=1, flags=re.S)
    ld = '{"@context":"https://schema.org","@type":"CollectionPage","name":%s,"url":"%s","inLanguage":"%s","isAccessibleForFree":true}' % (
        __import__('json').dumps(title, ensure_ascii=False), SITE + d(l) + page, l)
    return head + CSS + f'<script type="application/ld+json">{ld}</script>\n' + pre + '<main id="main">\n' + hero + '\n<div class="lw">' + main_inner + '</div>\n' + post.replace('</body>', f'<script src="{"" if l == "en" else "../"}assets/learn-hubs.js?v={JSV}" defer></script></body>', 1)
def roadmap(l, C, years):
    yt = ''.join(f'<li><a href="#y{y}">{esc(u("year", l, n=y))}</a></li>' for y in range(1, 5))
    out = [f'<h2 id="roadmap">🗺️ {esc(u("road", l))}</h2><p>{esc(u("road_t", l))}</p>',
           f'<div class="lhr" data-of="{esc(u("of", l))}" data-done="{esc(u("alldone", l))}" data-units="{esc(u("units", l))}" data-exam="{esc(u("exam", l))}">',
           f'<p id="lhp-l"><strong>{esc(u("progress", l))}:</strong> <span class="lhp-t" aria-live="polite"></span></p><div class="lhp-bar" role="progressbar" aria-labelledby="lhp-l" aria-valuemin="0" aria-valuemax="30" aria-valuenow="0"><span></span></div>',
           f'<div class="lhn"><div><h3>{esc(u("next", l))}</h3><ul class="lh-next"></ul></div><div><h3>{esc(u("exams", l))}</h3><ul class="lh-exams"></ul></div></div>',
           f'<p><button type="button" class="lh-reset">{esc(u("reset", l))}</button></p></div><ul class="lhyt" aria-label="{esc(u("yeartabs", l))}">{yt}</ul>']
    for y in range(1, 5):
        out.append(f'<section class="lhy" id="y{y}"><h3>{years[y - 1]}</h3><div class="lhs">')
        for sem in ('fall', 'spring'):
            out.append(f'<div><h4>{esc(u(sem, l))}</h4><ol>')
            for cid, yy, ss, top, pre, calc in X.ROAD:
                if yy != y or ss != sem: continue
                c = C[cid]; after = ', '.join(re.sub('<[^>]+>', '', C[p]['name']) for p in pre)
                out.append(f'<li id="c-{cid}" data-id="{cid}" data-pre="{" ".join(pre)}" data-href="{c["page"]}"><a href="{c["page"]}">{c["name"]}</a><span class="k">{c["code"]}</span>'
                           + (f'<span class="k">{esc(u("after", l))} {esc(after)}</span>' if after else '')
                           + f'<label><input type="checkbox" data-id="{cid}"> {esc(u("done", l))}</label></li>')
            out.append('</ol></div>')
        out.append('</div></section>')
    return ''.join(out)
def hub(l, key, C, years, NL):
    k, page, emo, name, line, guides, subj = TOP[key]
    mine = [r for r in X.ROAD if r[3] == key]
    inner = ''
    if key == 'aero': inner += roadmap(l, C, years) + planet_block(l, J.AERO_PINTRO[l]) + f'<p><a href="{J.PAGE}">🔥 {esc(J.UI["to_jet"][l])}</a></p>'
    else:
        n = len(mine)
        inner += f'<h2>{esc(u("courses", l))}</h2><ul class="lht">' + ''.join(
            f'<li><a href="{C[r[0]]["page"]}"><b>{C[r[0]]["name"]}</b><small>{C[r[0]]["code"]} · {esc(u("year", l, n=r[1]))}, {esc(u(r[2], l))}</small><small>{C[r[0]]["desc"]}</small></a></li>' for r in mine) + '</ul>'
        inner += f'<p><a href="Learn_Aero.html#roadmap">🗺️ {esc(u("inroad", l))}: {esc(TOP["aero"][3][l])}</a></p>'
    if guides:
        inner += f'<h2>{esc(u("guides", l))}</h2><ul class="lhm">' + ''.join(f'<li><a href="{g}">{NL.get(g, g) if "&" in NL.get(g, g) else esc(NL.get(g, g))}</a></li>' for g in guides if os.path.exists(d(l) + g)) + '</ul>'
    if key in ('math', 'eng', 'chem'): inner += f'<p class="lnote">{esc(u("nocalc", l))}</p>'
    inner += calc_widget(l, subj, NL)
    inner += f'<h2>{esc(u("topics", l))}</h2><ul class="lhm">' + ''.join(f'<li><a href="{t[1]}">{t[2]} {esc(t[3][l])}</a></li>' for t in X.TOPICS if t[0] != key) + '</ul>'
    return page_from_learn(l, page, name[l], line[l], inner, NL)
def links(l, txt):  # {Page.html|label} -> link, only if the page exists in this language
    def f(m):
        p, lab = m.group(1), m.group(2)
        return f'<a href="{p}">{esc(lab)}</a>' if os.path.exists(d(l) + p.split('#')[0]) else esc(lab)
    parts = re.split(r'(\{[\w_.#-]+\|[^}]*\})', txt)
    return ''.join(re.sub(r'\{([\w_.#-]+)\|([^}]*)\}', f, x) if x.startswith('{') else esc(x) for x in parts)
def planet_block(l, intro):
    rows = ''.join(f'<li><strong>{esc(u("year", l, n=y))}:</strong> {links(l, J.PNOTE[y][l])}</li>' for y in range(1, 5))
    return f'<section class="lhy" id="planet"><h2>🌍 {esc(J.UI["planet_h"][l])}</h2><p>{esc(intro)}</p><ul>{rows}</ul></section>'
JET_SVG = ('<svg class="jpa" viewBox="0 0 640 120" role="img" aria-label="{lab}" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="jpg" x1="0" x2="1"><stop offset="0" stop-color="#ffe27a"/><stop offset=".35" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></linearGradient></defs>'
    '<g class="jpa-x"><ellipse class="jpa-f" cx="330" cy="60" rx="70" ry="13" fill="url(#jpg)"/>'
    '<circle class="jpa-p p1" cx="300" cy="60" r="9"/><circle class="jpa-p p2" cx="300" cy="56" r="7"/><circle class="jpa-p p3" cx="300" cy="64" r="8"/><circle class="jpa-p p4" cx="300" cy="60" r="6"/></g>'
    '<path d="M40 38 L230 30 Q262 30 268 44 L282 50 L282 70 L268 76 Q262 90 230 90 L40 82 Q24 60 40 38Z" fill="#c9d6e3" stroke="#0b1620" stroke-width="2"/>'
    '<ellipse cx="44" cy="60" rx="12" ry="22" fill="#2a3a4a"/><g class="jpa-fan"><path d="M44 40 L48 60 L40 60Z M44 80 L40 60 L48 60Z M26 60 L44 56 L44 64Z M62 60 L44 64 L44 56Z" fill="#8fd3ff"/></g>'
    '<path d="M90 36 V84 M140 34 V86 M190 32 V88" stroke="#7d8fa3" stroke-width="2"/></svg>')
JET_CSS = ('<style>.jpa{display:block;width:min(100%,560px);height:auto;margin:.8rem auto 0}.jpa-p{fill:rgba(230,236,245,.55)}'
    '@media (prefers-reduced-motion:no-preference){.jpa-f{transform-origin:290px 60px;animation:jpf .18s ease-in-out infinite alternate}'
    '.jpa-p{animation:jpp 1.6s linear infinite}.p2{animation-delay:.4s}.p3{animation-delay:.8s}.p4{animation-delay:1.2s}'
    '.jpa-fan{transform-origin:44px 60px;animation:jps .5s linear infinite}}'
    '@keyframes jpf{from{transform:scaleX(.85)}to{transform:scaleX(1.08)}}@keyframes jps{to{transform:rotate(360deg)}}'
    '@keyframes jpp{0%{transform:translateX(0) scale(.6);opacity:.9}100%{transform:translateX(330px) scale(2.6);opacity:0}}'
    '[dir=rtl] .jpa{transform:scaleX(-1)}.lhs li.jp-m{border-inline-start-color:#ffd54a}</style>')
def jet_page(l, C, NL):
    U = lambda k: esc(J.UI[k][l])
    def item(x):
        if x.startswith('mod:'):
            n, t = J.MOD[x[4:]]
            return f'<li class="jp-m"><b>{esc(n[l])}</b><span class="k">{U("mod")}</span><span class="k">{esc(t[l])}</span></li>'
        cid, part = (x.split(':') + [None])[:2]
        c = C[cid]; extra = f'<span class="k">{esc(J.UI["part"][l].replace("{n}", part))}</span>' if part else ''
        return f'<li><a href="{c["page"]}">{c["name"]}</a><span class="k">{c["code"]}</span>{extra}</li>'
    yt = ''.join(f'<li><a href="#y{y}">{esc(u("year", l, n=y))}</a></li>' for y in range(1, 5))
    o = [JET_CSS, f'<h2 id="roadmap">🗺️ {U("plan_h")}</h2><p>{U("plan_t")}</p><ul class="lhyt" aria-label="{esc(u("yeartabs", l))}">{yt}</ul>']
    for y in range(1, 5):
        o.append(f'<section class="lhy" id="y{y}"><h3>{esc(u("year", l, n=y))}</h3><div class="lhs">')
        for sem in ('fall', 'spring'):
            o.append(f'<div><h4>{esc(u(sem, l))}</h4><ol>' + ''.join(item(x) for x in J.PLAN[y][sem]) + '</ol></div>')
        o.append('</div></section>')
    o.append(f'<p class="lnote" role="note">🧪 <strong>{U("labs_h")}:</strong> {U("labs")}</p>')
    o.append(planet_block(l, J.PINTRO[l]))
    o.append(calc_widget(l, 'aero', NL))
    o.append(best_block(l, [b for b in R.BEST if b[1] in R.JET_BEST_IDS]))
    o.append(f'<p><a href="Learn_Aero.html#roadmap">✈️ {U("to_aero")}</a> · <a href="{R.PAGE}">🚀 {esc(R.UI["to_rocket"][l])}</a></p>')
    o.append(f'<h2>{esc(u("topics", l))}</h2><ul class="lhm">' + ''.join(f'<li><a href="{t[1]}">{t[2]} {esc(t[3][l])}</a></li>' for t in X.TOPICS) + '</ul>')
    o.append(f'<p class="lnote"><small>{U("credit")}</small></p>')
    s = page_from_learn(l, J.PAGE, J.NAME[l], J.LINE[l], ''.join(o), NL)
    return s.replace('</p></div>', '</p>' + JET_SVG.replace('{lab}', U('anim')) + '</div>', 1)
BEST_CSS = ('<style>.lfb{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1rem}.lfb>div{padding:.6rem 1rem;border-radius:14px;background:rgba(255,255,255,.05)}'
    '.lfb h3{margin:.3rem 0 .4rem;font-size:1rem}.lfb ul{list-style:none;margin:0;padding:0;display:grid;gap:.55rem}.lfb a{font-weight:800}.lfb small{display:block;opacity:.88}</style>')
def best_block(l, items):  # Oct 28 (founder): "Learn from the best" (links checked with curl; one line each, no rankings)
    UR = lambda k: esc(R.UI[k][l]); out = ''
    for g in ('g_free', 'g_uni', 'g_nasa', 'g_job'):
        xs = [b for b in items if b[0] == g]
        if xs: out += f'<div><h3>{UR(g)}</h3><ul>' + ''.join(f'<li><a href="{esc(u_)}" rel="noopener" lang="en">{esc(n)}</a> ↗<small>{esc(w[l])}</small></li>' for _, n, u_, w in xs) + '</ul></div>'
    return BEST_CSS + f'<section class="lhy" id="learn-from-the-best"><h2>🏆 {UR("best_h")}</h2><p>{UR("best_t")}</p><div class="lfb">{out}</div></section>'
ROCKET_SVG = ('<svg class="rpa" viewBox="0 0 640 150" role="img" aria-label="{lab}" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="rpg" x1="0" x2="1"><stop offset="0" stop-color="#fff6d0"/><stop offset=".25" stop-color="#ffb347"/><stop offset=".7" stop-color="#ff6a3d" stop-opacity=".6"/><stop offset="1" stop-color="#ff6a3d" stop-opacity="0"/></linearGradient>'
    '<radialGradient id="rpd"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#9fd8ff"/><stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></radialGradient></defs>'
    '<g class="rpa-x"><path class="rpa-f" d="M150 52 L600 70 Q620 75 600 80 L150 98 Z" fill="url(#rpg)"/>'
    '<ellipse class="rpa-d d1" cx="215" cy="75" rx="15" ry="11" fill="url(#rpd)"/><ellipse class="rpa-d d2" cx="285" cy="75" rx="13" ry="10" fill="url(#rpd)"/>'
    '<ellipse class="rpa-d d3" cx="350" cy="75" rx="11" ry="8" fill="url(#rpd)"/><ellipse class="rpa-d d4" cx="410" cy="75" rx="9" ry="7" fill="url(#rpd)"/><ellipse class="rpa-d d5" cx="465" cy="75" rx="7" ry="5" fill="url(#rpd)"/></g>'
    '<path d="M150 46 Q100 58 70 66 L70 84 Q100 92 150 104 Z" fill="#b9c6d3" stroke="#0b1620" stroke-width="2"/>'
    '<rect x="30" y="62" width="40" height="26" rx="4" fill="#7d8fa3" stroke="#0b1620" stroke-width="2"/><path d="M84 64 Q118 56 148 50 M84 86 Q118 94 148 100" stroke="#8a99a9" stroke-width="2" fill="none"/></svg>')
ROCKET_CSS = ('<style>.rpa{display:block;width:min(100%,560px);height:auto;margin:.8rem auto 0}'
    '@media (prefers-reduced-motion:no-preference){.rpa-f{transform-origin:150px 75px;animation:rpf .12s ease-in-out infinite alternate}.rpa-d{animation:rpd .9s ease-in-out infinite alternate}'
    '.d2{animation-delay:.15s}.d3{animation-delay:.3s}.d4{animation-delay:.45s}.d5{animation-delay:.6s}}'
    '@keyframes rpf{from{transform:scaleX(.94);opacity:.9}to{transform:scaleX(1.04);opacity:1}}@keyframes rpd{from{opacity:.55}to{opacity:1}}[dir=rtl] .rpa{transform:scaleX(-1)}'
    '.rfc{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:1rem;list-style:none;padding:0}.rfc li{padding:.8rem 1rem;border-radius:14px;background:rgba(255,255,255,.05);border-inline-start:4px solid #ff8a3d}'
    '.rfc b{font-size:1.05rem}.rfc code{display:block;margin:.4rem 0;font-size:1rem;direction:ltr;unicode-bidi:isolate}.rtb{overflow-x:auto}.rtb table{border-collapse:collapse;width:100%;min-width:560px;font-size:.92rem}'
    '.rtb th,.rtb td{border:1px solid rgba(255,255,255,.2);padding:.45rem .55rem;text-align:start;vertical-align:top}.rtb th{background:rgba(255,255,255,.08)}.rtb .pl{font-style:italic;color:#ffd54a}'
    '.rsrc{font-size:.82rem;opacity:.9}.rclips{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1rem;list-style:none;padding:0}'
    '.rclips li{border-radius:14px;background:rgba(0,0,0,.25);padding:.6rem}.rclips video,.rclips iframe,.rclips .ytf{width:100%;aspect-ratio:16/9;border:0;border-radius:10px;background:#000;display:block}'
    '.ytf{display:flex!important;align-items:center;justify-content:center;font:700 1rem inherit;color:#fff;cursor:pointer;background:radial-gradient(circle,#26384a,#000)!important;min-height:44px}'
    '.rclips h3{font-size:.98rem;margin:.5rem 0 .2rem}.rclips small{display:block;opacity:.85}.rbar{list-style:none;padding:0;display:grid;gap:.45rem}.rbar li{display:grid;grid-template-columns:minmax(9rem,12rem) 1fr;gap:.6rem;align-items:center}'
    '.rbar span.b{display:block;height:20px;border-radius:6px;background:linear-gradient(90deg,#ff8a3d,#ffd54a);color:#1a1300;font-size:.78rem;font-weight:800;padding-inline-start:.4rem;line-height:20px;white-space:nowrap}'
    '.rbar span.b.pl{background:rgba(255,213,74,.12);color:#ffd54a;border:2px dashed #ffd54a;line-height:16px}</style>')
YT_JS = ("<script>document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.ytf');if(!b)return;var id=b.getAttribute('data-yt');if(!/^[A-Za-z0-9_-]{11}$/.test(id))return;var f=document.createElement('iframe');"
         "f.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';f.title=b.getAttribute('data-title');f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.loading='lazy';b.replaceWith(f)});</script>")
def srcs(xs): return '<span class="rsrc">' + ' · '.join(f'<a href="{esc(u_)}" rel="noopener" lang="en">{esc(t)}</a>' for t, u_ in xs) + '</span>'
def rocket_page(l, NL):
    UR = lambda k: esc(R.UI[k][l]); dash = '—'
    o = [ROCKET_CSS]
    if R.UI['mt'][l]: o.append(f'<p class="lnote" role="note"><small>🤖 {UR("mt")}</small></p>')
    # fundamentals
    def lk(h, k): return f'<a href="{h}">{UR("unit")} {R.UNITLAB[k]}</a>' if k in R.UNITLAB else f'<a href="{h}">🧮 {UR("calc")}</a>'
    cards = ''.join(f'<li><b>{e} {esc(t[l])}</b><p>{esc(d_[l])}</p>' + (f'<code>{esc(f)}</code>' if f else '') + ' · '.join(lk(h, k) for h, k in ls) + '</li>' for e, t, d_, f, ls in R.FUND)
    cyc = ''.join(f'<li><b>{esc(n[l])}</b><p>{esc(d_[l])}</p></li>' for n, d_ in R.CYC)
    o.append(f'<section id="fundamentals"><h2>⚙️ {UR("fund_h")}</h2><ul class="rfc">{cards}</ul><h3>{esc(R.CYC_H[l])}</h3><ul class="rfc">{cyc}</ul>'
             f'<p><a href="Propulsion.html#u8">{UR("unit")} 8</a> · {srcs(R.CYC_SRC)}</p></section>')
    # Raptor
    st = {'flown': UR('flown'), 'flying': UR('flying'), 'planned': f'<span class="pl">{UR("planned")}</span>'}
    rows = ''.join(f'<tr><th scope="row">{v}</th><td dir="ltr">{sl}</td><td dir="ltr">{vac or dash}</td><td>{UR("same") if m == "same" else m}</td><td>{st[k]}</td><td>{srcs(ss)}</td></tr>' for v, sl, vac, m, k, ss in R.RAPTOR)
    notes = ''.join(f'<li>{esc(n[l])} {srcs(ss)}</li>' for n, ss in zip(R.NOTES, R.NOTE_SRC))
    o.append(f'<section class="lhy" id="raptor"><h2>🔥 {UR("new_h")}</h2><p>{UR("new_t")}</p><div class="rtb"><table><thead><tr><th scope="col">{UR("ver")}</th><th scope="col">{UR("sl")}</th>'
             f'<th scope="col">{UR("vac")}</th><th scope="col">{UR("mass")}</th><th scope="col">{UR("status")}</th><th scope="col">{UR("src")}</th></tr></thead><tbody>{rows}</tbody></table></div>'
             f'<h3>{UR("notes_h")}</h3><ul>{notes}</ul></section>')
    # 30 years of raw power
    clips = ''
    for c in R.CLIPS:
        title = esc(c['t'][l]); cr = 'Video: ' + c['cr']
        if c['kind'] == 'nasa':
            base = R.NASA_V + c['id'].replace(' ', '%20') + '/' + c['id'].replace(' ', '%20')
            det = 'https://images.nasa.gov/details/' + c['id'].replace(' ', '%20')
            media = f'<video controls preload="none" playsinline poster="{base}~thumb.jpg" aria-label="{title}"><source src="{base}~mobile.mp4" type="video/mp4"></video>'
            more = f'<a href="{det}" rel="noopener" lang="en">images.nasa.gov</a> · {esc(cr)} (public domain)'
        elif c['kind'] == 'yt':
            media = f'<button type="button" class="ytf" data-yt="{c["id"]}" data-title="{title}">▶ {UR("play")}</button>'
            more = f'<a href="https://www.youtube.com/watch?v={c["id"]}" rel="noopener">YouTube · SpaceX</a> · {esc(cr)}'
        else:
            media = ''; more = f'<a href="{c["id"]}" rel="noopener">{UR("watch")} ↗</a> · {esc(cr)}'
        clips += f'<li>{media}<h3>{title}</h3><small dir="ltr">{c["date"]}</small><small>{more}</small></li>'
    brow = ''.join(f'<tr><th scope="row" lang="en">{esc(v)}</th><td dir="ltr">{dt}</td><td lang="en">{esc(e)}</td><td dir="ltr">{esc(p)}</td><td dir="ltr">{esc(t or dash)}</td><td dir="ltr">{esc(pc or dash)}</td>'
                   f'<td>{esc(i or dash)}</td><td dir="ltr">{esc(pr)}</td><td>{srcs(ss)}</td></tr>' for v, dt, e, p, t, pc, i, pr, ss in R.BENCH)
    mx = max(k for _, k, _ in R.CHART)
    bars = ''.join(f'<li><span lang="en">{esc(n)}</span><span class="b{" pl" if pl else ""}" style="width:{round(100 * k / mx)}%">{k:,} kN{" · " + UR("planned") if pl else ""}</span></li>' for n, k, pl in R.CHART)
    o.append(f'<section class="lhy" id="raw-power"><h2>📽️ {UR("bench_h")}</h2><p>{UR("bench_t")}</p><ul class="rclips">{clips}</ul>'
             f'<div class="rtb"><table><thead><tr><th scope="col">{UR("rocket")}</th><th scope="col">{UR("date")}</th><th scope="col">{UR("eng")}</th><th scope="col">{UR("per")}</th><th scope="col">{UR("tot")}</th>'
             f'<th scope="col">{UR("pc")}</th><th scope="col">{UR("isp")}</th><th scope="col">{UR("prop")}</th><th scope="col">{UR("src")}</th></tr></thead><tbody>{brow}</tbody></table></div>'
             f'<p><small>{UR("pc_n")}</small></p><h3 id="rbar-h">{UR("chart_h")}</h3><ul class="rbar" aria-labelledby="rbar-h">{bars}</ul><p><small>{UR("chart_n")}</small></p></section>')
    o.append(best_block(l, R.BEST))
    o.append(planet_block(l, J.PINTRO[l]))
    o.append(calc_widget(l, 'orbits', NL))
    o.append(f'<p><a href="{J.PAGE}">🔥 {UR("to_jet")}</a> · <a href="Propulsion.html">Propulsion</a> · <a href="Search.html?topic=rocket">🔎</a></p>')
    o.append(f'<h2>{esc(u("topics", l))}</h2><ul class="lhm">' + ''.join(f'<li><a href="{t[1]}">{t[2]} {esc(t[3][l])}</a></li>' for t in X.TOPICS) + '</ul>')
    o.append(f'<p class="lnote"><small>{UR("credit")}</small></p>' + YT_JS)
    s_ = page_from_learn(l, R.PAGE, R.NAME[l], R.LINE[l], ''.join(o), NL)
    return s_.replace('</p></div>', '</p>' + ROCKET_SVG.replace('{lab}', UR('anim')) + '</div>', 1)
def landing(l, NL):
    f = d(l) + 'Learn.html'; s = rd(f)
    s = re.sub(r'(<div class="page-hero-content"><h1>[^<]*</h1>)<p[^>]*>.*?</p>', lambda m: m.group(1) + f'<p class="lhv">{esc(X.VISION[l])}</p>', s, count=1, flags=re.S)
    cnt = lambda k: 30 if k == 'aero' else sum(1 for r in X.ROAD if r[3] == k)  # the aero roadmap holds all 30 courses
    cards = ''.join(f'<li{" class=\"lht-main\"" if t[0] == "aero" else ""}><a href="{t[1]}"><b>{t[2]} {esc(t[3][l])}</b><small>{esc(t[4][l])}</small><small>{esc(u("ncourses", l, n=cnt(t[0])) if cnt(t[0]) != 1 else u("ncourse1", l))}</small></a></li>' for t in X.TOPICS)
    more = [(J.PAGE, esc(J.SHORT[l])), (R.PAGE, esc(R.SHORT[l])), ('Courses.html', NL.get('Courses.html')), ('Play_and_Learn.html', NL.get('Play_and_Learn.html')), ('Teachers.html', NL.get('Teachers.html')), ('Lesson_Builder.html', NL.get('Lesson_Builder.html')),
            ('Cadets.html', NL.get('Cadets.html')), ('AP_IB_Physics.html', NL.get('AP_IB_Physics.html')), ('Careers.html', NL.get('Careers.html'))]
    blk = (f'<!-- LEARNHUB:START -->{CSS}<h2 id="topics">{esc(u("topics", l))}</h2><ul class="lht">{cards}</ul>'
           f'<h2>{esc(u("more", l))}</h2><ul class="lhm">' + ''.join(f'<li><a href="{p}">{t}</a></li>' for p, t in more if t) + '</ul><!-- LEARNHUB:END -->')
    if '<!-- LEARNHUB:START -->' in s: s = re.sub(r'<!-- LEARNHUB:START -->.*?<!-- LEARNHUB:END -->', lambda m: blk, s, flags=re.S)
    else:
        a = s.index('<div class="lw">') + len('<div class="lw">'); b = s.index('<!-- STDMAP:START -->', a) if '<!-- STDMAP:START -->' in s[a:] else s.index('</div>', a)
        s = s[:a] + blk + s[b:]
    return wr(f, s)
def crumbs(l, C):
    ch = 0
    for cid, y, sem, top, pre, calc in X.ROAD:
        f = d(l) + C[cid]['page']
        if not os.path.exists(f): continue
        s = rd(f); t = TOP[top]
        road = f'<a href="Learn_Aero.html#c-{cid}">🗺️ {esc(u("road", l))} · {esc(u("year", l, n=y))}, {esc(u(sem, l))}</a>'
        if calc: road += f' · <a href="{t[1]}#calc-{calc}">🧮 {esc(u("calc", l))}</a>'
        s2 = re.sub(r'<p class="crs-crumb crs-road">.*?</p>', '', s)
        s2 = re.sub(r'<p class="crs-crumb">.*?</p>', lambda m: f'<p class="crs-crumb"><a href="Learn.html">{esc(u("learn", l))}</a> › <a href="{t[1]}">{esc(t[3][l])}</a> › {C[cid]["code"]}</p><p class="crs-crumb crs-road">{road}</p>', s2, count=1)
        ch += wr(f, s2)
    return ch
def embed_mode(l):  # Oct 26: he/ calculator pages had no EMBEDMODE block (build-embed covers 5 langs), so the hub iframe showed full chrome
    import importlib.util
    sp = importlib.util.spec_from_file_location('be', 'scripts/build-embed.py'); be = importlib.util.module_from_spec(sp); sp.loader.exec_module(be)
    ch = 0
    for _, cl in X.CALCS:
        for _, p in cl:
            f = d(l) + p
            if os.path.exists(f):
                s = rd(f)
                if '<!-- EMBEDMODE:START -->' not in s: ch += wr(f, s.replace('</head>', be.MODE_HEAD + '</head>', 1))
    return ch
def main():
    ch = 0
    for l in LANGS:
        C, years = courses(l); NL = navlabels(l); ch += embed_mode(l)
        ch += landing(l, NL); ch += crumbs(l, C)
        for f in sorted(os.listdir(d(l) or '.')):
            if not f.endswith('.html'): continue
            p = d(l) + f; s = rd(p)
            if 'id="spn-le"' not in s: continue
            cur = f if f in [t[1] for t in X.TOPICS] + [J.PAGE, R.PAGE, 'Learn.html', 'Courses.html', 'Cadets.html', 'AP_IB_Physics.html', 'Careers.html'] else None
            s2 = set_nav(s, l, NL, cur)
            s2 = re.sub(r'<li><a href="(?:\.\./)?Homeschool\.html"[^>]*>.*?</a></li>', '', s2) if f != 'Homeschool.html' else s2
            ch += wr(p, s2)
        for t in X.TOPICS: ch += wr(d(l) + t[1], hub(l, t[0], C, years, NL))
        ch += wr(d(l) + J.PAGE, jet_page(l, C, NL))
        ch += wr(d(l) + R.PAGE, rocket_page(l, NL))
    sm = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        for t in X.TOPICS + [(None, J.PAGE), (None, R.PAGE)]:
            loc = f'{SITE}{d(l)}{t[1]}'
            if f'<loc>{loc}</loc>' not in sm: sm = sm.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', sm)
    print(f'build-learn-hubs: writes={ch}')
if __name__ == '__main__': main(); main()  # second pass: hubs copy Learn.html chrome, so one more pass converges (second prints writes=0)
