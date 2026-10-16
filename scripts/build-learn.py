#!/usr/bin/env python3
"""Oct 16 Phase 1 education build: Learn.html (3-track hub: Orbital Mechanics live; Aeronautical Engineering + Physics coming),
Orbits_Guide.html (kids/teens/community college), Orbit_Math.html (undergraduate to PhD derivations, KaTeX pre-rendered at build
time with MathML), Orbit_Lab.html (assets/orbit-lab.js). All 5 languages. Every number comes from scripts/learn_calc.py.
No standalone math track (owner correction): math is woven into each track as step-by-step worked examples.
Content: scripts/learn_orbit_math.py, scripts/learn_text.py. KaTeX CSS + woff2 fonts copied to assets/vendor/katex/ from node_modules.
Nav door lives in build-ux.py GROUPS ('le'). Run after build-spotfire.py. Idempotent."""
import re, os, sys, json, glob, shutil, datetime, subprocess, importlib.util
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('sf', 'scripts/build-spotfire.py'); sf = importlib.util.module_from_spec(spec); spec.loader.exec_module(sf)
SITE, LANGS, d, rd, wr, esc = sf.SITE, sf.LANGS, sf.d, sf.rd, sf.wr, sf.esc
import learn_calc, learn_orbit_math as OM, learn_text as LT, learn_extras as LX
V = '20261016L'  # cache version for learn.css / orbit-lab.js / katex
PAGES = ['Learn.html', 'Orbits_Guide.html', 'Orbit_Math.html', 'Orbit_Lab.html']
LV = dict(LT.LEVELS)
def ex_values():
    e = dict(learn_calc.examples())
    e['h_tof_h'] = e['h_tof'] / 3600; e['mr_prop_pct'] = e['mr_prop'] * 100; e['kep_n'] = len(e['kep_steps'])
    for k in ('lam_v1', 'lam_v2'):
        for i in range(3): e[f'{k}_{i}'] = float(e[k][i])
    x = learn_calc.extras(); e.update({k: v for k, v in x.items() if k != 'k2_rows'})
    return {k: float(v) for k, v in e.items() if not isinstance(v, list)}
K2 = learn_calc.extras()['k2_rows']
TODAY = datetime.date.today().isoformat()
EX = ex_values()
def num(v, dig, l):
    s = f'{v:.{dig}f}'
    if s.startswith('-0') and float(s) == 0: s = s[1:]
    return s.replace('.', ',') if l in ('fr', 'es', 'it') else s
def fill(s, l):
    m, e = f'{EX["lam_err"]:.1e}'.split('e')
    sup = str(int(e)).translate(str.maketrans('-0123456789', '\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079'))
    s = s.replace('{lam_err_txt}', num(float(m), 1, l) + '\u00d710' + sup)
    def rep(mm):
        k = mm.group(1)
        if k not in EX: raise KeyError(f'learn: missing example value {k}')
        return num(EX[k], int(mm.group(2)), l)
    out = re.sub(r'\{(\w+):(\d)\}', rep, s)
    assert '{' not in out or 'tof}' in out or 'dv' in out, out
    return out
def tx(o, l): return esc(fill(o[l], l))
# ---- KaTeX (build time) ----
LAB_EQ = [r'v_c=\sqrt{\frac{\mu}{r}}', r'v^2=\mu\left(\frac{2}{r}-\frac{1}{a}\right)', r'a_t=\frac{r_1+r_2}{2},\qquad t_t=\pi\sqrt{\frac{a_t^3}{\mu}}']
CONSTS = [r'\mu_\oplus=398\,600.4418\ \text{km}^3/\text{s}^2', r'R_\oplus=6378.137\ \text{km}', r'J_2=1.08262668\times10^{-3}', r'g_0=9.80665\ \text{m/s}^2', r'T_{sid}=86\,164.0905\ \text{s}']
def vendor():
    ch = 0; src = 'node_modules/katex/dist'; dst = 'assets/vendor/katex'
    os.makedirs(dst + '/fonts', exist_ok=True)
    css = rd(src + '/katex.min.css')
    css = re.sub(r',url\(fonts/[^)]+\.woff\) format\("woff"\)|,url\(fonts/[^)]+\.ttf\) format\("truetype"\)', '', css)
    ch += wr(dst + '/katex.min.css', css)
    for f in glob.glob(src + '/fonts/*.woff2'):
        t = dst + '/fonts/' + os.path.basename(f)
        if not os.path.exists(t) or open(t, 'rb').read() != open(f, 'rb').read(): shutil.copyfile(f, t); ch += 1
    ch += wr(dst + '/LICENSE', rd('node_modules/katex/LICENSE'))
    return ch
CSS = ('.lw{max-width:1000px;margin:0 auto;padding:1rem 1.25rem 2.5rem;line-height:1.6}.lw h2{margin-top:2.2rem;scroll-margin-top:5rem}.lw h3{margin:1.2rem 0 .4rem;font-size:1.05rem}'
       '.lchips{display:flex;flex-wrap:wrap;gap:.35rem;margin:.3rem 0 .8rem;padding:0;list-style:none}.lchip{font-size:.82rem;font-weight:700;padding:.15rem .6rem;border-radius:999px;background:rgba(124,170,255,.18);border:1px solid rgba(124,170,255,.5)}'
       '.lbox{border-radius:14px;padding:.9rem 1.1rem;margin:.9rem 0;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.05)}'
       '.lbox.obj{border-inline-start:5px solid #7cfc98}.lbox.pre{border-inline-start:5px solid #8fd3ff}.lbox.ex{border-inline-start:5px solid #ffd54a}.lbox.mist{border-inline-start:5px solid #ff8a80}'
       '.lbox>h3:first-child{margin-top:0}.lsteps{padding-inline-start:1.4rem}.lsteps li{margin:.6rem 0}.leq{overflow-x:auto;overflow-y:hidden;padding:.2rem 0;direction:ltr;text-align:left}'
       '.leq .katex-display{margin:.4rem 0}.lnote{display:block;font-size:.95rem;opacity:.92}.lw details{margin:.5rem 0;border-radius:10px;padding:.5rem .8rem;background:rgba(0,0,0,.18)}'
       '.lw summary{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center}.lrefs{font-size:.92rem}.lrefs li{margin:.3rem 0}'
       '.lfilter{display:flex;flex-wrap:wrap;gap:.45rem;margin:.6rem 0 1rem}.lfilter button{min-height:44px;padding:.35rem .9rem;border-radius:999px;font:inherit;cursor:pointer;border:1px solid rgba(255,255,255,.4);background:transparent;color:inherit}'
       '.lfilter button[aria-pressed=true]{background:#ffd54a;color:#1a1300;font-weight:800}.ltoc{columns:2 16rem;column-gap:2.5rem;font-size:.95rem;padding-inline-start:2rem}.ltoc li{break-inside:avoid}#ol [hidden]{display:none!important}.lw section[hidden]{display:none}'
       '.ltracks{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:1rem;list-style:none;padding:0}'
       '.ltrack{border-radius:20px;padding:1.2rem;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);display:flex;flex-direction:column;gap:.5rem}'
       '.ltrack h3{margin:0;font-size:1.3rem}.lstat{align-self:flex-start;font-size:.8rem;font-weight:800;padding:.2rem .65rem;border-radius:999px;background:#7cfc98;color:#06260f}.lstat.soon{background:#ffd54a;color:#1a1300}'
       '.ltrack ul{margin:.2rem 0;padding-inline-start:1.1rem}.ltrack a{font-weight:700}'
       '#ol form{display:grid;gap:.8rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));align-items:end}#ol label{display:flex;flex-direction:column;gap:.25rem;font-weight:700}'
       '#ol input[type=number]{min-height:44px;font:inherit;padding:.3rem .6rem;border-radius:10px}#ol fieldset{border:1px solid rgba(255,255,255,.3);border-radius:10px}#ol fieldset label{flex-direction:row;align-items:center;min-height:44px}'
       '#ol button{min-height:44px;border-radius:999px;padding:.4rem 1.1rem;font:inherit;font-weight:800;cursor:pointer}#ol canvas{width:100%;display:block;margin:1rem 0 .5rem;background:#050b1a;border-radius:16px}'
       '.ol-out{font-weight:700;font-size:1.05rem;min-height:2.5em}.ol-table{width:100%;border-collapse:collapse}.ol-table th,.ol-table td{padding:.4rem .6rem;border-bottom:1px solid rgba(255,255,255,.15);text-align:start}'
       '.ol-table td{direction:ltr;unicode-bidi:isolate}.lbox.intu{border-inline-start:5px solid #c9a7ff}.lmeta{font-size:.9rem;opacity:.85}'
       '.lwe dt{font-weight:800;margin-top:.6rem}.lwe dd{margin-inline-start:0}.lw pre{overflow-x:auto;background:#050b1a;padding:.8rem;border-radius:10px;text-align:left}'
       '.lnp{margin:.8rem 0}.lnp-row{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}.lnp input{min-height:44px;width:9rem;font:inherit;padding:.3rem .6rem;border-radius:10px}'
       '.lnp button,.lmcq button{min-height:44px;border-radius:999px;padding:.35rem 1rem;font:inherit;font-weight:700;cursor:pointer}.lnp-fb{font-weight:700;min-height:1.4em}'
       '.lnp-fb.is-ok{color:#7cfc98}.lnp-fb.is-no{color:#ffb4a8}.lmcq{border:1px solid rgba(255,255,255,.3);border-radius:12px;margin:.8rem 0;padding:.6rem 1rem}'
       '.lmcq label{display:flex;gap:.5rem;align-items:center;min-height:44px}.lw :focus-visible{outline:3px solid #ffd54a;outline-offset:2px}')
FILTER_JS = ("(function(){var f=document.querySelector('.lfilter');if(!f)return;f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var v=b.dataset.lv;"
             "[].forEach.call(f.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});"
             "[].forEach.call(document.querySelectorAll('section[data-lv]'),function(s){s.hidden=v!=='all'&&s.dataset.lv.split(' ').indexOf(v)<0});"
             "[].forEach.call(document.querySelectorAll('.ltoc li[data-lv]'),function(s){s.hidden=v!=='all'&&s.dataset.lv.split(' ').indexOf(v)<0})})})();")
def shell(l, page, title, desc, main, extra_head='', ld_type='LearningResource', tail=''):
    s = rd(d(l) + 'Kids_Map.html'); head = s[:s.index('</head>')]; pre = '' if l == 'en' else '../'
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(title) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('assets/og/' + l + '/Kids_Map.jpg', 'assets/og/' + l + '/' + page[:-5] + '.jpg').replace('Kids_Map.html', page)
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}{page}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{page}">'
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    if os.path.exists(d(l) + page):  # keep build-og.py's card version hash (idempotent with build-og)
        old = re.search(r'<meta property="og:image" content="([^"]+)"', rd(d(l) + page))
        if old and '/' + page[:-5] + '.jpg' in old.group(1):
            head = re.sub(r'(content=")[^"]*/assets/og/' + l + '/' + re.escape(page[:-5]) + r'\.jpg[^"]*"', lambda m: m.group(1) + old.group(1) + '"', head)
    ld = {"@context": "https://schema.org", "@type": ld_type, "name": title, "description": desc, "url": f"{SITE}{d(l)}{page}", "inLanguage": l,
          "isAccessibleForFree": True, "learningResourceType": "lesson" if ld_type == 'LearningResource' else None}
    ld = {k: v for k, v in ld.items() if v is not None}
    head += extra_head + f'<style>{CSS}</style>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    body = re.sub(r'class="[^"]*"', 'class="toc-sub learn-page"', re.search(r'<body[^>]*>', s).group(0), count=1)
    body = re.sub(r' data-glass-tint="[^"]*"', '', body)[:-1] + ' data-glass-tint="space">'
    nav = re.search(r'<a class="skip-link".*?</nav>', s, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Kids_Map.html', page), nav, flags=re.S)
    foot = s[s.index('</main>'):]
    foot = re.sub(r'<script src="(?:\.\./)?(?:edu|edu-extras)\.js[^"]*"[^>]*></script>', '', foot)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', foot)
    foot = foot.replace('</body>', tail + '</body>', 1)
    return head + '</head>\n' + body + nav + '<main id="main">\n' + main + foot
def hero(t, k): return f'<section class="page-hero hero-learn"><div class="page-hero-content"><h1>{esc(t)}</h1><p>{esc(k)}</p></div></section>\n'
def chips(lvs, l): return '<ul class="lchips">' + ''.join(f'<li class="lchip">{esc(LV[x][l])}</li>' for x in lvs) + '</ul>'
def katex_head(l):
    pre = '' if l == 'en' else '../'
    return f'<link rel="stylesheet" href="{pre}assets/vendor/katex/katex.min.css?v={V}">\n'
def learn_hub(l):
    H = LT.HUB; h = lambda p: sf.href(l, p)
    orbit = (f'<li class="ltrack"><span class="lstat">{esc(H["live"][l])}</span><h3>{esc(H["orbit"][l])}</h3><p>{esc(H["orbit_d"][l])}</p><ul>'
             f'<li><a href="{h("Orbits_Guide.html")}">{esc(H["guide"][l])}</a></li><li><a href="{h("Orbit_Math.html")}">{esc(H["math"][l])}</a></li>'
             f'<li><a href="{h("Orbit_Lab.html")}">{esc(H["lab"][l])}</a></li></ul></li>')
    soon = lambda k: (f'<li class="ltrack"><span class="lstat soon">{esc(H["soon"][l])}</span><h3>{esc(H[k][l])}</h3><p>{esc(H[k + "_d"][l])}</p>'
                      f'<p class="lnote">{esc(H[k + "_topics"][l])}</p></li>')
    main = (hero(H['title'][l], H['kicker'][l]) + '<div class="lw">'
            f'<h2>{esc(H["tracks"][l])}</h2><ul class="ltracks">{orbit}{soon("aero")}{soon("phys")}</ul>'
            f'<h2>{esc(H["levels"][l])}</h2>{chips([k for k, _ in LT.LEVELS], l)}'
            f'<h2>{esc(H["std"][l])}</h2><ul>' + ''.join(f'<li>{esc(x[l])}</li>' for x in H['std_items']) + '</ul>'
            f'<h2>{esc(H["teach"][l])}</h2><p>{esc(H["teach_t"][l])}</p><ul><li><a href="{h("Teachers.html")}">Teachers</a></li><li><a href="{h("Lesson_Builder.html")}">Lesson Builder</a></li></ul></div>\n')
    main = main.replace('>Teachers<', '>' + esc(re.sub('<[^>]+>', '', nav_label(l, 'Teachers.html'))) + '<').replace('>Lesson Builder<', '>' + esc(re.sub('<[^>]+>', '', nav_label(l, 'Lesson_Builder.html'))) + '<')
    return shell(l, 'Learn.html', H['title'][l], H['desc'][l], main, ld_type='CollectionPage')
def nav_label(l, p):
    spec2 = importlib.util.spec_from_file_location('ux', 'scripts/build-ux.py'); src = rd('scripts/build-ux.py')
    m = re.search(r"'" + l + r"': dict\(.*?items=\{(.*?)\}", src, re.S); mm = re.search(r"'" + re.escape(p) + r"':'([^']*)'", m.group(1))
    return mm.group(1).replace('&#x27;', '\u2019') if mm else p[:-5]
def guide(l):
    G = LT.GUIDE; secs = ''
    for i, (lv, t, body, q, a) in enumerate(G['sections']):
        secs += (f'<section id="g{i+1}"><h2>{tx(t, l)}</h2>{chips([lv], l)}<p>{tx(body, l)}</p>'
                 f'<details><summary>{esc(G["q"][l])}: {tx(q, l)}</summary><p>{tx(a, l)}</p></details></section>\n')
    main = (hero(G['title'][l], G['kicker'][l]) + f'<div class="lw">{secs}<p class="lbox ex"><a href="{sf.href(l, "Orbit_Math.html")}">{esc(G["next"][l])}</a> \u00b7 '
            f'<a href="{sf.href(l, "Orbit_Lab.html")}">{esc(OM.UI["tryit"][l])}</a></p></div>\n')
    return shell(l, 'Orbits_Guide.html', G['title'][l], G['desc'][l], main)
def fillv(o, l, vals):
    return esc(re.sub(r'\{(\w):(\d)\}', lambda m: num(vals[m.group(1)], int(m.group(2)), l), o[l]))
def worked(sid, l):
    w = LX.WE.get(sid); B = LX.LBL
    if not w: return None
    if w['steps'] == 'TABLE':
        rows = ''.join(f'<tr><td>{n}</td><td>{num(E, 10, l)}</td><td>{f"{dE:.2e}"}</td></tr>' for n, E, dE in K2)
        steps = f'<table class="ol-table" dir="ltr"><caption>{esc(B["iter"][l])}</caption><thead><tr><th scope="col">n</th><th scope="col">E_n (rad)</th><th scope="col">|ΔE|</th></tr></thead><tbody>{rows}</tbody></table>'
    else:
        steps = '<ol>' + ''.join(f'<li><bdi dir="ltr">{tx(x, l)}</bdi></li>' for x in w['steps']) + '</ol>'
    dl = ''.join(f'<dt>{esc(B[k][l])}</dt><dd>{v}</dd>' for k, v in [('given', tx(w['given'], l)), ('find', tx(w['find'], l)), ('strat', tx(w['strat'], l)),
        ('steps', steps), ('ans', '<strong>' + tx(w['ans'], l) + '</strong>'), ('sanity', tx(w['sanity'], l)), ('sig', tx(w['sig'], l))])
    return f'<dl class="lwe">{dl}</dl><details><summary>{esc(B["py"][l])}</summary><pre dir="ltr"><code>{esc(w["py"])}</code></pre></details>'
def practice(sid, l):
    B = LX.LBL; out = ''
    for i, q in enumerate(LX.NP.get(sid, [])):
        vals = dict(a=q['val'], **q.get('extra', {})); qid = f'np-{sid}-{i}'
        hints = ''.join(f'<li hidden>{tx(h, l)}</li>' for h in q['hints'])
        out += (f'<li class="lnp" data-ans="{q["val"]:.10g}" data-tol="{q["tol"]}" data-ok="{esc(B["ok"][l])}" data-no="{esc(B["no"][l])}" data-nan="{esc(B["nan"][l])}">'
                f'<p><label for="{qid}">{tx(q["q"], l)}</label></p><span class="lnp-row"><input id="{qid}" type="text" inputmode="decimal" dir="ltr" autocomplete="off" aria-describedby="{qid}-fb">'
                f'{(" <span>" + esc(q["unit"]) + "</span>") if q["unit"] else ""} <button type="button" class="lnp-check">{esc(B["check"][l])}</button>'
                f' <button type="button" class="lnp-hint">{esc(B["nexthint"][l])}</button></span>'
                f'<p class="lnp-fb" id="{qid}-fb" role="status" aria-live="polite"></p><ol class="lnp-hints">{hints}</ol>'
                f'<details><summary>{esc(B["full"][l])}</summary><p>{fillv(q["sol"], l, vals)}</p></details></li>')
    return f'<h3>{esc(B["auto"][l])}</h3><ol>{out}</ol>' if out else ''
def cyu(l):
    B = LX.LBL; out = ''
    for i, (q, opts, a, why) in enumerate(LX.MCQ):
        o = ''.join(f'<label><input type="radio" name="mcq{i}" value="{j}"> {esc(x[l])}</label>' for j, x in enumerate(opts))
        out += (f'<fieldset class="lmcq" data-ans="{a}" data-ok="{esc(B["ok"][l])}" data-no="{esc(LX.T("Not quite.", "Pas tout à fait.", "No del todo.", "ليس تمامًا.", "Non proprio.")[l])}" data-why="{esc(why[l])}">'
                f'<legend>{esc(q[l])}</legend>{o}<button type="button">{esc(LX.CYU_BTN[l])}</button><p class="lnp-fb" role="status" aria-live="polite"></p></fieldset>')
    return f'<section id="cyu"><h2>{esc(B["cyu"][l])}</h2>{out}</section>'
def math_page(l, K):
    U = OM.UI; toc = ''; body = ''
    for s in OM.S:
        lvs = ' '.join(s['lv'])
        toc += f'<li data-lv="{lvs}"><a href="#{s["id"]}">{tx(s["t"], l)}</a></li>'
        steps = ''.join(f'<li><div class="leq" dir="ltr">{K[t]}</div><span class="lnote">{tx(n, l)}</span></li>' for t, n in s['steps'])
        prac = ''.join(f'<li><p>{tx(q, l)}</p><details><summary>{esc(U["sol"][l])}</summary><p>{tx(a, l)}</p></details></li>' for q, a in s['prac'])
        refs = ''.join(f'<li>{OM.REFS[r]}</li>' for r in s['refs'])
        B = LX.LBL; we = worked(s['id'], l)
        exbox = we if we else f'<p>{tx(s["ex"], l)}</p>'
        meta = f'<p class="lmeta">{esc(B["track"][l])} · {esc(B["time"][l].replace("{n}", str(LX.TIME[s["id"]])))} · {esc(B["verified"][l])}: <time datetime="{TODAY}">{TODAY}</time></p>'
        body += (f'<section id="{s["id"]}" data-lv="{lvs}"><h2>{tx(s["t"], l)}</h2>{chips(s["lv"], l)}{meta}'
                 f'<div class="lbox obj"><h3>{esc(U["obj"][l])}</h3><p>{tx(s["obj"], l)}</p></div>'
                 f'<div class="lbox pre"><h3>{esc(U["pre"][l])}</h3><p>{tx(s["pre"], l)} <a href="{sf.href(l, "Orbits_Guide.html")}">{esc(LT.GUIDE["title"][l])}</a></p></div>'
                 f'<div class="lbox intu"><h3>{esc(B["intu"][l])}</h3><p>{tx(s["body"], l)}</p></div>'
                 f'<h3>{esc(U["deriv"][l])}</h3><ol class="lsteps">{steps}</ol>'
                 f'<div class="lbox ex"><h3>{esc(U["ex"][l])}</h3>{exbox}</div>'
                 f'{practice(s["id"], l)}<h3>{esc(U["prac"][l])}</h3><ol>{prac}</ol>'
                 f'<div class="lbox mist"><h3>{esc(U["mist"][l])}</h3><p>{tx(s["mist"], l)}</p></div>'
                 f'<h3>{esc(U["refs"][l])}</h3><ul class="lrefs">{refs}</ul></section>\n')
    lvset = []
    for s in OM.S:
        for x in s['lv']:
            if x not in lvset: lvset.append(x)
    filt = (f'<div class="lfilter" role="group" aria-label="{esc(U["level"][l])}"><button type="button" data-lv="all" aria-pressed="true">{esc(U["all"][l])}</button>'
            + ''.join(f'<button type="button" data-lv="{x}" aria-pressed="false">{esc(LV[x][l])}</button>' for x in [k for k, _ in LT.LEVELS] if x in lvset) + '</div>')
    consts = '<div class="lbox pre"><h3>' + esc(U['consts'][l]) + '</h3>' + ''.join(f'<div class="leq" dir="ltr">{K[c]}</div>' for c in CONSTS) + f'<p class="lnote">{esc(U["verify"][l])}</p></div>'
    allrefs = '<h2>' + esc(U['refs'][l]) + '</h2><ul class="lrefs">' + ''.join(f'<li>{v}</li>' for v in OM.REFS.values()) + '</ul>'
    main = (hero(U['title'][l], U['kicker'][l]) + f'<div class="lw">{filt}<nav aria-label="{esc(U["contents"][l])}"><h2>{esc(U["contents"][l])}</h2><ol class="ltoc">{toc}</ol></nav>'
            f'{consts}<p><a href="{sf.href(l, "Orbit_Lab.html")}">{esc(U["tryit"][l])}</a></p>{body}{cyu(l)}<h2>{esc(LX.LBL["deeper"][l])}</h2><p>{esc(LX.DEEPER[l])}</p><h2>{esc(LX.LBL["teach"][l])}</h2><p>{esc(LX.TEACH[l])}</p>{allrefs}</div>\n')
    desc = U['kicker'][l]
    return shell(l, 'Orbit_Math.html', U['title'][l], desc, main, extra_head=katex_head(l), tail=f'<script>{FILTER_JS}</script>\n<script src="{"" if l == "en" else "../"}assets/learn.js?v={V}" defer></script>\n')
def lab(l, K):
    L = LT.LAB; pre = '' if l == 'en' else '../'; tr = {k: v[l] for k, v in L['tr'].items()}
    form = (f'<div id="ol" data-t="{esc(json.dumps(tr, ensure_ascii=False))}"><form novalidate>'
            f'<label>{esc(L["h1"][l])}<input name="h1" type="number" inputmode="decimal" min="160" max="100000" step="any" value="300"></label>'
            f'<fieldset><legend>{esc(L["mode"][l])}</legend><label><input type="radio" name="mode" value="alt" checked> {esc(L["m_alt"][l])}</label>'
            f'<label><input type="radio" name="mode" value="dv"> {esc(L["m_dv"][l])}</label></fieldset>'
            f'<label class="ol-f-alt">{esc(L["h2"][l])}<input name="h2" type="number" inputmode="decimal" min="160" step="any" value="35786"></label>'
            f'<label class="ol-f-dv" hidden>{esc(L["dvin"][l])}<input name="dv" type="number" inputmode="decimal" step="any" value="1"></label>'
            f'<button type="submit">{esc(L["go"][l])}</button></form>'
            f'<p class="ol-out" role="status" aria-live="polite"></p><canvas role="img" aria-label="{esc(L["canvas"][l])}"></canvas>'
            f'<button type="button" class="ol-play">{esc(tr["play"])}</button>'
            f'<table class="ol-table"><caption>{esc(L["tcap"][l])}</caption><tbody></tbody></table></div>')
    how = f'<h2>{esc(L["how"][l])}</h2>' + ''.join(f'<div class="leq" dir="ltr">{K[e]}</div>' for e in LAB_EQ) + f'<p>{esc(L["how_t"][l])}</p><p><a href="{sf.href(l, "Orbit_Math.html")}#hohmann">{esc(L["learn"][l])}</a></p>'
    main = hero(L['title'][l], L['kicker'][l]) + f'<div class="lw">{form}{how}</div>\n'
    return shell(l, 'Orbit_Lab.html', L['title'][l], L['desc'][l], main, extra_head=katex_head(l), ld_type='LearningResource',
                 tail=f'<script src="{pre}assets/orbit-lab.js?v={V}" defer></script>\n')
if __name__ == '__main__':
    global_tex = LAB_EQ + CONSTS
    tl = [t for s in OM.S for t, _ in s['steps']] + global_tex
    K = dict(zip(tl, json.loads(subprocess.run(['node', 'scripts/katex-render.cjs'], input=json.dumps(tl), capture_output=True, text=True, check=True).stdout)))
    ch = vendor()
    for l in LANGS:
        ch += wr(d(l) + 'Learn.html', learn_hub(l)); ch += wr(d(l) + 'Orbits_Guide.html', guide(l))
        ch += wr(d(l) + 'Orbit_Math.html', math_page(l, K)); ch += wr(d(l) + 'Orbit_Lab.html', lab(l, K))
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        for p in PAGES:
            loc = f'{SITE}{d(l)}{p}'
            if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-learn: writes={ch}')
