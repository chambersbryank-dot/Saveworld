#!/usr/bin/env python3
"""Oct 16 2026: Careers.html, Cadets.html (JROTC + CAP), AP_IB_Physics.html, Homeschool.html in 5 languages, plus the Learn hub
"Start here" block. Text: scripts/paths_text*.py (official, cited facts only). Shell reused from build-learn.py. Cadets and
Homeschool are kid-facing: build-share.py gives them data-no-newsletter + the grown-ups link (no sign-up). Idempotent."""
import re, os, sys, html, datetime, importlib.util
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
import paths_text as P, paths_text2 as P2, paths_text3 as P3, calc_text as CT, learn_text as LT
SITE, LANGS, d, rd, wr, esc = BL.SITE, BL.LANGS, BL.d, BL.rd, BL.wr, BL.esc
PLAYL = {'en': 'Play & Learn', 'fr': 'Jouer et apprendre', 'es': 'Juega y aprende', 'ar': 'العب وتعلّم', 'it': 'Gioca e impara'}
SPOT = P.T('Spot the Fire', 'Repère le feu', 'Encuentra el fuego', 'اكتشف الحريق', 'Trova l’incendio')
FACTS = P.T('Amazing Facts', 'Faits étonnants', 'Datos asombrosos', 'حقائق مدهشة', 'Fatti sorprendenti')
MYTH = P.T('Myth vs Fact', 'Mythe ou réalité', 'Mito o realidad', 'خرافة أم حقيقة', 'Mito o realtà')
CALC = {c['page']: c for c in CT.C}
def noemoji(s): return re.sub(r'^[^\w(]+', '', re.sub('<[^>]+>', '', s)).strip()
def label(l, p):
    b, _, frag = p.partition('#')
    if b in CALC: t = re.split(r' \(|: | – ', CALC[b]['title'][l])[0]
    elif b == 'Calculators.html': t = CT.UI['idx_title'][l]
    elif b in P.NAV: t = noemoji(P.NAV[b][l])
    elif b in LT.NAV_ITEMS: t = noemoji(LT.NAV_ITEMS[b][l])
    elif b == 'Play_and_Learn.html': t = PLAYL[l]
    elif b == 'Spot_the_Fire.html': t = SPOT[l]
    elif b == 'Amazing_Facts.html': t = FACTS[l]
    elif b == 'Myth_vs_Fact.html': t = MYTH[l]
    else: t = html.unescape(noemoji(BL.nav_label(l, b)))
    return t
def h(l, p):
    b, _, frag = p.partition('#')
    return (b if l == 'en' or os.path.exists(d(l) + b) else '../' + b) + ('#' + frag if frag else '')
def md(s, l):  # [label](link) + **bold**; everything else escaped
    out, i = '', 0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*', s):
        out += esc(s[i:m.start()]); i = m.end()
        if m.group(3): out += f'<strong>{esc(m.group(3))}</strong>'
        else:
            u = m.group(2); href = u if u.startswith('http') else h(l, u)
            out += f'<a href="{esc(href)}">{esc(m.group(1))}</a>'
    return out + esc(s[i:])
def links(l, pages): return ' · '.join(f'<a href="{esc(h(l, p))}">{esc(label(l, p))}</a>' for p in pages)
def bdi(s): return f'<bdi dir="ltr">{s}</bdi>'
def money(v, l):
    s = f'{v:,}'
    return bdi({'fr': s.replace(',', '\u202f') + '\u00a0$', 'es': s.replace(',', '.') + '\u00a0US$', 'it': s.replace(',', '.') + '\u00a0$'}.get(l, '$' + s))
def count(v, l): return bdi(f'{v:,}'.replace(',', {'fr': '\u202f', 'es': '.', 'it': '.'}.get(l, ',')))
CSS = ('<style>.pw-card{border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:1rem 1.2rem;margin:1rem 0;background:rgba(255,255,255,.05)}.pw-card h3{margin-top:0}'
       '.pw-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:.6rem;margin:.6rem 0;padding:0;list-style:none}.pw-stats li{background:rgba(0,0,0,.25);border-radius:12px;padding:.5rem .8rem}'
       '.pw-stats .k{display:block;font-size:.85rem;opacity:.9}.pw-stats .v{font-weight:800;font-size:1.15rem}.pw-disc{border-inline-start:4px solid #ffd54a;padding:.6rem 1rem;background:rgba(255,213,74,.08);border-radius:8px}'
       '.pw-tbl{width:100%;border-collapse:collapse;margin:.6rem 0 1.2rem}.pw-tbl th,.pw-tbl td{border:1px solid rgba(255,255,255,.25);padding:.5rem .6rem;text-align:start;vertical-align:top}.pw-tbl th{background:rgba(255,255,255,.08)}'
       '.pw-tbl a{display:inline-block;min-height:24px;padding:2px 0}.pw-print{min-height:44px;padding:8px 18px;border-radius:999px;font:inherit;font-weight:700;cursor:pointer;border:1px solid #ffd54a;background:transparent;color:inherit}'
       '.pw-print:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}.pw-tick{display:inline-block;width:1.2em;height:1.2em;border:2px solid currentColor;border-radius:4px}'
       '@media print{#topnav,nav,footer,.shr,.nl-call,.pw-print,.share-bar,.sticky-help,.page-hero{display:none!important}body{background:#fff!important;color:#000!important}.pw-tbl th,.pw-tbl td{border-color:#000}a{color:#000}}</style>\n')
def table(l, head, rows):
    th = ''.join(f'<th scope="col">{esc(x)}</th>' for x in head)
    return f'<div style="overflow-x:auto"><table class="pw-tbl"><thead><tr>{th}</tr></thead><tbody>' + ''.join(
        f'<tr><td>{bdi(esc(a[l]))}</td><td>{esc(b[l])}</td><td>{links(l, c)}</td></tr>' for a, b, c in rows) + '</tbody></table></div>'
def printbtn(l): return f'<p><button type="button" class="pw-print" onclick="window.print()">🖨️ {esc(P.COMMON["print"][l])}</button></p>'
def srcs(items): return '<ul class="lrefs">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
def checked(l):
    t = datetime.date.today().isoformat(); return f'<p class="lmeta">{esc(P.COMMON["checked"][l])}: <time datetime="{t}">{t}</time></p>'
def careers(l):
    C = P.CL; out = ''
    toc = '<ul class="lchips">' + ''.join(f'<li class="lchip"><a href="#{c["id"]}">{c["icon"]} {esc(c["t"][l])}</a></li>' for c in P.CAREERS) + '</ul>'
    for c in P.CAREERS:
        stats = ''
        for k in c['bls']:
            name, url, pay, g, op = P.BLS[k]
            stats += (f'<ul class="pw-stats"><li><span class="k">{esc(C["related"][l] if c.get("nobls") else "BLS")}</span><span class="v"><a href="{url}" lang="en">{esc(name)}</a></span></li>'
                      f'<li><span class="k">{esc(C["pay"][l])}</span><span class="v">{money(pay, l)}</span></li>'
                      f'<li><span class="k">{esc(C["grow"][l])}</span><span class="v">{bdi("+" + str(g) + "%")} · {count(op, l)} {esc(C["open"][l])}</span></li></ul>')
        if c.get('nobls') or not c['bls']: stats = f'<p class="lnote">{esc(C["nobls"][l])}</p>' + stats
        out += (f'<section class="pw-card" id="{c["id"]}"><h3>{c["icon"]} {esc(c["t"][l])}</h3><p><strong>{esc(C["what"][l])}:</strong> {md(c["what"][l], l)}</p>'
                f'<p><strong>{esc(C["path"][l])}:</strong> {md(c["path"][l], l)}</p><p><strong>{esc(C["math"][l])}:</strong> {links(l, c["links"])}</p>{stats}</section>')
    vet = '<ul>' + ''.join(f'<li>{md(x[l], l)}</li>' for x in P.VET) + '</ul>'
    sch = f'<div style="overflow-x:auto"><table class="pw-tbl"><thead><tr><th scope="col">{esc(P.COMMON["prog"][l])}</th><th scope="col">{esc(C["who"][l])}</th><th scope="col">{esc(C["when"][l])}</th></tr></thead><tbody>'
    sch += ''.join(f'<tr><td><a href="{u}" lang="en">{esc(n)}</a></td><td>{esc(w[l])}</td><td>{esc(dt[l]) if dt else esc(C["check"][l])}</td></tr>' for n, u, w, dt in P.SCH) + '</tbody></table></div>'
    src = [f'U.S. Bureau of Labor Statistics, <a href="{u}">Occupational Outlook Handbook: {esc(n)}</a> (last modified August 27, 2026).' for n, u, *_ in P.BLS.values()]
    src += ['FAA, <a href="https://www.faa.gov/pilots/become">Become a Pilot</a>; <a href="https://www.faa.gov/mechanics/become">Become a Mechanic</a>; <a href="https://www.faa.gov/uas/commercial_operators/become_a_drone_pilot">Become a Drone Pilot</a>.',
            'U.S. Department of Veterans Affairs; DoD SkillBridge (links above).']
    main = (BL.hero(C['title'][l], C['kicker'][l]) + f'<div class="lw">{checked(l)}<p class="pw-disc">{esc(C["bls_date"][l])}</p>{toc}{out}'
            f'<h2 id="community-college">{esc(C["cc"][l])}</h2><p>{md(P.CC[l], l)}</p><h2 id="veterans">{esc(C["vet"][l])}</h2>{vet}'
            f'<h2 id="scholarships">{esc(C["sch"][l])}</h2><p class="lnote">{esc(C["sch_note"][l])}</p>{sch}<h2>{esc(P.COMMON["src"][l])}</h2>{srcs(src)}</div>\n')
    return BL.shell(l, 'Careers.html', C['title'][l], C['desc'][l], main, extra_head=CSS, ld_type='CollectionPage')
def cadets(l):
    C = P2.CD; hd = [P.COMMON['prog'][l], P.COMMON['topic'][l], P.COMMON['ours'][l]]
    steps = '<ol>' + ''.join(f'<li>{esc(x[l])}</li>' for x in C['inst_steps']) + '</ol>'
    main = (BL.hero(C['title'][l], C['kicker'][l]) + f'<div class="lw">{checked(l)}<p class="pw-disc" role="note">{esc(C["disc"][l])}</p>'
            f'<h2 id="afjrotc">{esc(C["af"][l])}</h2><p>{esc(C["af_t"][l])}</p>{table(l, hd, P2.AF_ROWS)}'
            f'<h2 id="njrotc">{esc(C["nv"][l])}</h2><p>{esc(C["nv_t"][l])}</p>{table(l, hd, P2.NV_ROWS)}'
            f'<h2 id="army-marine">{esc(C["am"][l])}</h2><p>{esc(C["am_t"][l])}</p><p>{links(l, ["Calculators.html", "Orbit_Lab.html", "Aero_Lab.html", "Physics_Lab.html"])}</p>'
            f'<h2 id="cap">{esc(C["cap"][l])}</h2><p>{esc(C["cap_t"][l])}</p>{table(l, hd, P2.CAP_ROWS)}<p>{md(C["ace"][l], l)}</p><p>{md(C["aex"][l], l)}</p>'
            f'<h2 id="instructors">{esc(C["inst"][l])}</h2>{steps}<h3 id="topic-map">{esc(C["map"][l])}</h3>{printbtn(l)}{table(l, hd, P2.AF_ROWS + P2.NV_ROWS + P2.CAP_ROWS)}'
            f'<h2>{esc(P.COMMON["src"][l])}</h2>{srcs(P2.CD_SRC)}<p class="pw-disc">{esc(C["disc"][l])}</p></div>\n')
    return BL.shell(l, 'Cadets.html', C['title'][l], C['desc'][l], main, extra_head=CSS)
def apib(l):
    A = P2.AP; hd = [P.COMMON['unit'][l], P.COMMON['topic'][l], P.COMMON['ours'][l]]
    def rows(rs, pre): return [(P.S(pre + a['en']), b, c) for a, b, c in rs]
    main = (BL.hero(A['title'][l], A['kicker'][l]) + f'<div class="lw">{checked(l)}<p class="pw-disc" role="note">{esc(A["tm"][l])}</p><h2>{esc(A["how"][l])}</h2><p>{esc(A["how_t"][l])}</p>'
            f'<h2 id="ap1">{esc(A["ap1"][l])}</h2>{table(l, hd, rows(P2.AP1_ROWS, "Unit "))}<h2 id="apc">{esc(A["apc"][l])}</h2><p>{esc(A["apc_t"][l])}</p>'
            f'<h2 id="ap2">{esc(A["ap2"][l])}</h2>{table(l, hd, rows(P2.AP2_ROWS, "Unit "))}<h2 id="ib">{esc(A["ib"][l])}</h2>{table(l, hd, P2.IB_ROWS)}{printbtn(l)}'
            f'<h2>{esc(P.COMMON["src"][l])}</h2>{srcs(P2.AP_SRC)}<p class="pw-disc">{esc(A["tm"][l])}</p></div>\n')
    return BL.shell(l, 'AP_IB_Physics.html', A['title'][l], A['desc'][l], main, extra_head=CSS)
def homeschool(l):
    H = P3.HS
    ages = ''.join(f'<section class="pw-card"><h3>{esc(a[l])}</h3><p>{esc(t[l])}</p><p>{links(l, ps)}</p></section>' for a, t, ps in P3.AGES)
    wk = (f'<div style="overflow-x:auto"><table class="pw-tbl"><thead><tr><th scope="col">{esc(H["week"][l])}</th><th scope="col">{esc(H["do"][l])}</th><th scope="col">{esc(P.COMMON["ours"][l])}</th><th scope="col">{esc(H["tick"][l])}</th></tr></thead><tbody>'
          + ''.join(f'<tr><td>{bdi(str(i))}</td><td>{esc(t[l])}</td><td>{links(l, ps)}</td><td><span class="pw-tick" aria-hidden="true"></span></td></tr>' for i, (t, ps) in enumerate(P3.WEEKS, 1)) + '</tbody></table></div>')
    main = (BL.hero(H['title'][l], H['kicker'][l]) + f'<div class="lw"><h2 id="ages">{esc(H["ages"][l])}</h2>{ages}<h2 id="plan">{esc(H["plan"][l])}</h2><p>{esc(H["plan_t"][l])}</p>{printbtn(l)}{wk}'
            f'<h2>{esc(H["more"][l])}</h2><p>{md(H["more_t"][l], l)}</p></div>\n')
    return BL.shell(l, 'Homeschool.html', H['title'][l], H['desc'][l], main, extra_head=CSS, ld_type='CollectionPage')
PAGES = {'Careers.html': careers, 'Cadets.html': cadets, 'AP_IB_Physics.html': apib, 'Homeschool.html': homeschool}
START = ['Cadets.html', 'AP_IB_Physics.html', 'Careers.html']  # Oct 26: Homeschool + Calculators links removed (pages stay reachable by URL)
def hub_block(l):  # injected into Learn.html (marker block, stripped by i18n tools)
    lis = ''.join(f'<li><a href="{h(l, p)}">{esc(P.NAV[p][l])}</a></li>' for p in START)
    return (f'<!-- STARTHERE:START --><h2 id="start-here">{esc(P.HUB["start"][l])}</h2><p>{esc(P.HUB["start_t"][l])}</p>'
            f'<ul class="cxg sh-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:.8rem;list-style:none;padding:0">{lis}</ul>'
            '<style>.sh-grid a{display:flex;align-items:center;min-height:56px;padding:.6rem 1rem;border-radius:14px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);font-weight:800;text-decoration:none;color:inherit}.sh-grid a:hover,.sh-grid a:focus-visible{border-color:#ffd54a}</style><!-- STARTHERE:END -->')
if __name__ == '__main__':
    ch = 0
    for l in LANGS:
        for p, fn in PAGES.items(): ch += wr(d(l) + p, fn(l))
        f = d(l) + 'Learn.html'; s = rd(f); s2 = re.sub(r'<!-- STARTHERE:START -->.*?<!-- STARTHERE:END -->', '', s, flags=re.S)
        ch += wr(f, s2)  # Oct 26: Learn.html landing is now built by build-learn-hubs.py (no Start-here block)
        f = d(l) + 'Teachers.html'  # Oct 16 (A): Start-here links on Teachers too
        if os.path.exists(f):
            s = rd(f); s2 = re.sub(r'<!-- STARTHERE:START -->.*?<!-- STARTHERE:END -->', '', s, flags=re.S)
            m = re.search(r'<section class="page-hero.*?</section>', s2, re.S)
            if m:
                blk = hub_block(l).replace('<!-- STARTHERE:START -->', '<!-- STARTHERE:START --><div style="max-width:1100px;margin:1.5rem auto;padding:0 1rem">', 1).replace('<!-- STARTHERE:END -->', '</div><!-- STARTHERE:END -->')
                s2 = s2[:m.end()] + blk + s2[m.end():]
            ch += wr(f, s2)
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        for p in PAGES:
            loc = f'{SITE}{d(l)}{p}'
            if f'<loc>{loc}</loc>' not in s and f'href="{loc}"' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-paths: writes={ch}')
