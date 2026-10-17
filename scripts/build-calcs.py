#!/usr/bin/env python3
"""Oct 16 2026: search-named calculator pages + Calculators.html index (5 languages).
Text: scripts/calc_text.py. Numbers: scripts/calc_check.py (asserts textbook checks at build time; writes calc-vectors.json for
scripts/test-calcs.js). Widget: assets/calc.js. Page shell, KaTeX and CSS reused from build-learn.py. Embed button + ?embed=1
mode come from build-embed.py; share bar from build-share.py; standards chips from build-standards.py. Idempotent."""
import re, os, sys, json, datetime, subprocess, importlib.util
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
import calc_text as CT, calc_check as CK
SITE, LANGS, d, rd, wr, esc = BL.SITE, BL.LANGS, BL.d, BL.rd, BL.wr, BL.esc
REFS = {**BL.OM.REFS, **BL.LA.REFS, **BL.LP.REFS}
REFS['faa_phak'] = 'FAA, <a href="https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak">Pilot’s Handbook of Aeronautical Knowledge</a> (FAA-H-8083-25C).'
REFS['nssdc'] = 'NASA NSSDCA, <a href="https://nssdc.gsfc.nasa.gov/planetary/factsheet/">Planetary Fact Sheets</a>.'
EXTRA_REFS = {'stall': ['faa_phak'], 'vel': ['nssdc'], 'tw': ['nssdc']}
V = '20261016c'
PLANETS = [('9.80665', CT.T('Earth (9.80665)', 'Terre (9,80665)', 'Tierra (9,80665)', 'الأرض (9.80665)', 'Terra (9,80665)')),
           ('1.62', CT.T('Moon (1.62)', 'Lune (1,62)', 'Luna (1,62)', 'القمر (1.62)', 'Luna (1,62)')), ('3.71', CT.T('Mars (3.71)', 'Mars (3,71)', 'Marte (3,71)', 'المريخ (3.71)', 'Marte (3,71)'))]
def h(l, p):
    base, _, frag = p.partition('#')
    return (base if l == 'en' or os.path.exists(d(l) + base) else '../' + base) + ('#' + frag if frag else '')
def num(v, dig, l): return BL.num(v, dig, l)
def unit(u): return CT.U[u]
CSS = ('.cx{border-radius:16px;padding:1rem 1.2rem;border:1px solid rgba(255,213,74,.55);background:rgba(255,255,255,.05);margin:1rem 0}'
       '.cx-in{display:grid;gap:.8rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));align-items:end}.cx label{display:flex;flex-direction:column;gap:.3rem;font-weight:700}'
       '.cx input,.cx select{min-height:44px;font:inherit;font-size:1.05rem;padding:.3rem .6rem;border-radius:10px;border:1px solid #7aa7c2;background:#0b1620;color:#e8eef5;box-sizing:border-box;width:100%}'
       '.cx input:focus-visible,.cx select:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}.cx-out{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:.6rem;margin:1rem 0 .3rem;padding:0;list-style:none}'
       '.cx-out li{background:rgba(0,0,0,.25);border-radius:12px;padding:.6rem .8rem}.cx-out .k{display:block;font-size:.88rem;opacity:.9}.cx-out .v{font-size:1.35rem;font-weight:800}.cx-msg{color:#ffb4a8;font-weight:700;min-height:1.2em}'
       '.cxg{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:1rem;list-style:none;padding:0}.cxg li a{display:block;height:100%;box-sizing:border-box;border-radius:16px;padding:1rem;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);font-weight:800;text-decoration:none;color:inherit;min-height:44px}'
       '.cxg li a span{display:block;font-weight:400;font-size:.92rem;margin-top:.35rem;opacity:.9}.cxg li a:hover,.cxg li a:focus-visible{border-color:#ffd54a}')
def field(c, n, lab, u, l):
    val = CK.EX[c['id']][n]; v = f'{val:.10g}'
    if n == 'g' and c['id'] == 'tw':
        opts = ''.join(f'<option value="{k}"{" selected" if float(k) == val else ""}>{esc(t[l])}</option>' for k, t in PLANETS)
        return f'<label>{esc(lab[l])}<select name="g">{opts}</select></label>'
    return f'<label>{esc(lab[l])}<input name="{n}" type="text" inputmode="decimal" dir="ltr" autocomplete="off" value="{v}"></label>'
def bdi(s): return f'<bdi dir="ltr">{s}</bdi>'
def calc_page(c, l, K):
    U = CT.UI; ex = CK.example(c['id']); x = CK.EX[c['id']]
    ins = ''.join(field(c, n, lab, u, l) for n, lab, u in c['inp'])
    outs = ''.join(f'<li><span class="k">{esc(lab[l])}</span><span class="v">{bdi(f"<output data-out=\"{k}\" data-d=\"{dg}\">{num(ex[k], dg, l)}</output> {unit(u)}")}</span></li>' for k, lab, u, dg in c['out'])
    widget = (f'<form class="cx" data-calc="{c["id"]}" data-bad="{esc(U["bad"][l])}" novalidate aria-labelledby="cx-h"><h2 id="cx-h">{esc(U["calc"][l])}</h2><div class="cx-in">{ins}</div>'
              f'<h3>{esc(U["res"][l])}</h3><ul class="cx-out" aria-live="polite">{outs}</ul><p class="cx-msg" role="status"></p><p class="lnote">{esc(U["live"][l])}</p></form>')
    eqs = ''.join(f'<div class="leq" dir="ltr">{K[e]}</div>' for e in c['eq'])
    def inval(n, u):
        v = x[n]
        if n == 'g' and c['id'] == 'tw': return next(esc(t[l]) for k, t in PLANETS if float(k) == v)
        return bdi(f'{num(v, 6, l).rstrip("0").rstrip(".,") if v != int(v) else str(int(v))} {unit(u)}')
    given = '<ul>' + ''.join(f'<li>{esc(lab[l])}: {inval(n, u)}</li>' for n, lab, u in c['inp']) + '</ul>'
    ans = '<ul>' + ''.join(f'<li>{esc(lab[l])}: <strong>{bdi(num(ex[k], dg, l) + " " + unit(u))}</strong></li>' for k, lab, u, dg in c['out']) + '</ul>'
    exbox = (f'<div class="lbox ex"><h2>{esc(U["ex"][l])}</h2><dl class="lwe"><dt>{esc(U["given"][l])}</dt><dd>{given}</dd><dt>{esc(U["ans"][l])}</dt><dd>{ans}</dd>'
             f'<dt>{esc(U["check"][l])}</dt><dd>{esc(c["chk"][l])}</dd></dl></div>')
    refs = ''.join(f'<li>{REFS[r]}</li>' for r in c['refs'] + EXTRA_REFS.get(c['id'], []))
    more = (f'<h2>{esc(U["more"][l])}</h2><ul><li><a href="{h(l, c["learn"])}">{esc(U["learn"][l])}</a></li><li><a href="{h(l, c["lab"])}">{esc(U["lab"][l])}</a></li>'
            f'<li><a href="{h(l, "Calculators.html")}">{esc(U["all"][l])}</a></li></ul>')
    today = datetime.date.today().isoformat()
    main = (BL.hero(c['title'][l], c['intro'][l]) + f'<div class="lw"><p class="lmeta">{esc(U["verified"][l])}: <time datetime="{today}">{today}</time></p>{widget}'
            f'<h2>{esc(U["eq"][l])}</h2>{eqs}{exbox}<div class="lbox pre"><h2>{esc(U["assume"][l])}</h2><p>{esc(c["asm"][l])}</p></div>{more}'
            f'<h2>{esc(U["src"][l])}</h2><ul class="lrefs">{refs}</ul></div>\n')
    pre = '' if l == 'en' else '../'
    return BL.shell(l, c['page'], c['title'][l], c['intro'][l], main, extra_head=BL.katex_head(l) + f'<style>{CSS}</style>\n',
                    tail=f'<script src="{pre}assets/calc.js?v={V}" defer></script>\n')
def index_page(l):
    U = CT.UI; secs = ''
    for g in ('orbit', 'aero', 'phys'):
        items = ''.join(f'<li><a href="{h(l, c["page"])}">{esc(c["title"][l])}<span>{esc(c["intro"][l].split(". ")[0].rstrip(".") + ".")}</span></a></li>' for c in CT.C if c['grp'] == g)
        secs += f'<h2>{esc(U["g_" + g][l])}</h2><ul class="cxg">{items}</ul>'
    main = BL.hero(U['idx_title'][l], U['idx_kick'][l]) + f'<div class="lw">{secs}</div>\n'
    return BL.shell(l, 'Calculators.html', U['idx_title'][l], U['idx_desc'][l], main, extra_head=f'<style>{CSS}</style>\n', ld_type='CollectionPage')
PAGES = ['Calculators.html'] + [c['page'] for c in CT.C]
if __name__ == '__main__':
    assert CK.checks()
    vec = [dict(id=k, x=x, y=CK.FN[k](**x)) for k, x in CK.VEC]
    ch = wr('scripts/calc-vectors.json', json.dumps(vec, indent=0))
    tl = [e for c in CT.C for e in c['eq']]
    K = dict(zip(tl, json.loads(subprocess.run(['node', 'scripts/katex-render.cjs'], input=json.dumps(tl), capture_output=True, text=True, check=True).stdout)))
    for l in LANGS:
        ch += wr(d(l) + 'Calculators.html', index_page(l))
        for c in CT.C: ch += wr(d(l) + c['page'], calc_page(c, l, K))
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        for p in PAGES:
            loc = f'{SITE}{d(l)}{p}'
            if f'<loc>{loc}</loc>' not in s and f'href="{loc}"' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-calcs: writes={ch}')
