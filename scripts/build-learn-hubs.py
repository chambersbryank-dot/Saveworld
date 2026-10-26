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
    items = [('Learn.html', '🎓 ' + u('learn', l))] + [(t[1], f'{t[2]} {t[3][l]}') for t in X.TOPICS] + [(p, NL[p]) for p in ('Courses.html', 'Cadets.html', 'AP_IB_Physics.html', 'Careers.html') if p in NL]
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
    if key == 'aero': inner += roadmap(l, C, years)
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
def landing(l, NL):
    f = d(l) + 'Learn.html'; s = rd(f)
    s = re.sub(r'(<div class="page-hero-content"><h1>[^<]*</h1>)<p>.*?</p>', lambda m: m.group(1) + f'<p class="lhv">{esc(X.VISION[l])}</p>', s, count=1, flags=re.S)
    cnt = lambda k: 30 if k == 'aero' else sum(1 for r in X.ROAD if r[3] == k)  # the aero roadmap holds all 30 courses
    cards = ''.join(f'<li{" class=\"lht-main\"" if t[0] == "aero" else ""}><a href="{t[1]}"><b>{t[2]} {esc(t[3][l])}</b><small>{esc(t[4][l])}</small><small>{esc(u("ncourses", l, n=cnt(t[0])) if cnt(t[0]) != 1 else u("ncourse1", l))}</small></a></li>' for t in X.TOPICS)
    more = [('Courses.html', NL.get('Courses.html')), ('Play_and_Learn.html', NL.get('Play_and_Learn.html')), ('Teachers.html', NL.get('Teachers.html')), ('Lesson_Builder.html', NL.get('Lesson_Builder.html')),
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
            cur = f if f in [t[1] for t in X.TOPICS] + ['Learn.html', 'Courses.html', 'Cadets.html', 'AP_IB_Physics.html', 'Careers.html'] else None
            s2 = set_nav(s, l, NL, cur)
            s2 = re.sub(r'<li><a href="(?:\.\./)?Homeschool\.html"[^>]*>.*?</a></li>', '', s2) if f != 'Homeschool.html' else s2
            ch += wr(p, s2)
        for t in X.TOPICS: ch += wr(d(l) + t[1], hub(l, t[0], C, years, NL))
    sm = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        for t in X.TOPICS:
            loc = f'{SITE}{d(l)}{t[1]}'
            if f'<loc>{loc}</loc>' not in sm: sm = sm.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', sm)
    print(f'build-learn-hubs: writes={ch}')
if __name__ == '__main__': main(); main()  # second pass: hubs copy Learn.html chrome, so one more pass converges (second prints writes=0)
