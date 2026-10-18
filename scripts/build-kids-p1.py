#!/usr/bin/env python3
"""Oct 17 2026 Phase 1 kids quick wins (POA&M P-07, P-08, P-16, P-18), en/fr/es/ar/it + hidden he:
  Space_Passport.html      P-07 stamps per mission hub / Play & Learn tile / bonus; localStorage only ('sp-pass-v1' + existing 'sp-play-v1'); copy/paste code; printable
  Myth_or_Fact_Arcade.html P-08 tap game; claims read from each language's built Myth_vs_Fact.html + Amazing_Facts.html (every card keeps its source)
  Boarding_Pass.html       P-16 printable keepsake pass for the next real launch (assets/data/map-launches.json, Launch Library 2); name never stored or sent
  site.js SPOW block       P-18 Accessibility Superpowers panel on kids pages + passport visit recorder
  Play_and_Learn.html      <!-- KIDSP1 --> 'New' row linking the three pages
Shell = each language's built Play_and_Learn.html (nav/footer/analytics already final). Run late in weekly-sync.sh (after build-play/build-nav, before build-critical/seo-fix).
Counts are computed from the site's own pages/data, never typed. Idempotent."""
import re, os, json, html, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import langs as L
from kids_p1_text import PASS, ARC, BP, SPOW, NEW, CREDIT
SITE = 'https://www.savingplanets.com/'
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if (p.startswith('he/') or '/he/' in p) and not L.HE_PUBLIC:
        s = L.ensure_hidden_robots(s)
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
d = lambda l: '' if l == 'en' else l + '/'
LANGS = ['en'] + [l for l in L.BUILD if os.path.exists(d(l) + 'Play_and_Learn.html')]
PUB = ['en'] + [l for l in L.PUBLIC if l in LANGS]
PAGES = ['Space_Passport.html', 'Myth_or_Fact_Arcade.html', 'Boarding_Pass.html']
PAGE_STEMS = [p[:-5] for p in PAGES]
HUB_EMOJI = {'Project-Rawane.html': '🚀', 'Earth_Observation.html': '🛰️', 'Deforestation.html': '🌳', 'Lakes.html': '🏞️', 'Oceans.html': '🌊',
             'Planetary_Defense.html': '☄️', 'Rivers.html': '🏞', 'Space.html': '🔭', 'Space_Disposal.html': '♻️', 'Space_Weather.html': '☀️'}
PLAY_EMOJI = {'Kids_Map': '🗺️', 'Spot_the_Fire': '🔥', 'Satellite_Explorer': '🛰️', 'Amazing_Facts': '🤩', 'Myth_vs_Fact': '🕵️', 'Glossary': '📖'}
def href(l, p): return p if l == 'en' or os.path.exists(d(l) + p) else '../' + p
def strip(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

CSS = """.k1-hero{position:relative;overflow:hidden;padding:calc(var(--nav-height,88px) + clamp(1rem,3vw,2rem)) 1.25rem clamp(2rem,5vw,3.5rem);text-align:center;color:#fff;
background:radial-gradient(ellipse at 20% 10%,rgba(120,90,255,.55),transparent 55%),radial-gradient(ellipse at 85% 80%,rgba(0,190,255,.45),transparent 50%),linear-gradient(160deg,#07071d,#141047 55%,#04121f)}
.k1-hero:before{content:"";position:absolute;inset:0;background-image:radial-gradient(1.5px 1.5px at 12% 22%,#fff,transparent),radial-gradient(1px 1px at 32% 72%,#fff,transparent),radial-gradient(1.5px 1.5px at 58% 18%,#fff,transparent),radial-gradient(1px 1px at 76% 46%,#fff,transparent),radial-gradient(2px 2px at 90% 14%,#ffe9a8,transparent),radial-gradient(1px 1px at 44% 88%,#fff,transparent),radial-gradient(1.5px 1.5px at 6% 60%,#cfe8ff,transparent);opacity:.9;pointer-events:none}
.k1-hero>*{position:relative}.k1-art{font-size:clamp(3.6rem,10vw,6.5rem);line-height:1;filter:drop-shadow(0 8px 24px rgba(0,0,0,.5));margin-bottom:.4rem}
.k1-hero h1{font-size:clamp(2.1rem,5.4vw,3.6rem);margin:.2rem auto .5rem;max-width:18ch;line-height:1.08;letter-spacing:-.01em}
.k1-hero p{font-size:clamp(1.05rem,2.2vw,1.3rem);max-width:46ch;margin:0 auto;opacity:.95;line-height:1.45}
.k1-chip{display:inline-block;margin-top:1rem;padding:.4rem 1rem;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);font-weight:700}
.k1-wrap{max-width:1100px;margin:0 auto;padding:1.4rem 1.25rem 2.5rem}.k1-wrap h2{font-size:1.45rem;margin:1.8rem 0 .8rem}
.k1-btn{display:inline-flex;align-items:center;justify-content:center;gap:.4rem;min-height:48px;min-width:48px;padding:.6rem 1.25rem;border-radius:999px;border:2px solid transparent;font:inherit;font-weight:800;cursor:pointer;background:#ffd54a;color:#1a1300;text-decoration:none}
.k1-btn.alt{background:transparent;color:inherit;border-color:currentColor}.k1-btn:focus-visible{outline:3px solid #4fc3ff;outline-offset:3px}
.k1-note{font-size:.92rem;opacity:.85}.k1-row{display:flex;flex-wrap:wrap;gap:.7rem;align-items:center;margin:.8rem 0}
.k1-stamps{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:1rem;list-style:none;padding:0;margin:0}
.k1-stamp{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.35rem;padding:1rem .6rem;border-radius:20px;background:rgba(127,127,127,.1);border:2px dashed rgba(127,127,127,.45);text-decoration:none;color:inherit;min-height:170px}
.k1-ring{display:grid;place-items:center;width:84px;height:84px;border-radius:50%;font-size:2.4rem;border:4px double rgba(127,127,127,.6);filter:grayscale(1);opacity:.45}
.k1-stamp.on{border-style:solid;border-color:#ffd54a;background:linear-gradient(160deg,rgba(255,213,74,.16),rgba(120,90,255,.12))}
.k1-stamp.on .k1-ring{filter:none;opacity:1;border-color:#e0457b;transform:rotate(-8deg);box-shadow:0 0 0 3px rgba(224,69,123,.25)}
.k1-sname{font-weight:800;line-height:1.2}.k1-sstate{font-size:.85rem;font-weight:700;padding:.15rem .6rem;border-radius:999px;background:rgba(127,127,127,.18)}.k1-stamp.on .k1-sstate{background:#ffd54a;color:#1a1300}
.k1-meter{height:14px;border-radius:999px;background:rgba(127,127,127,.25);overflow:hidden;max-width:520px}.k1-meter i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffd54a,#e0457b);transition:width .6s}
.k1-rank{font-size:1.3rem;font-weight:900}.k1-code{width:100%;max-width:560px;min-height:3.2rem;font:inherit;font-size:.95rem;padding:.6rem;border-radius:12px;direction:ltr}
.k1-print-name{display:none}
.arc-card{max-width:760px;margin:0 auto;padding:clamp(1.2rem,3vw,2rem);border-radius:26px;background:linear-gradient(160deg,rgba(120,90,255,.18),rgba(0,190,255,.12));border:2px solid rgba(127,127,127,.3);box-shadow:0 10px 30px rgba(0,0,0,.2)}
.arc-claim{font-size:clamp(1.3rem,3vw,1.75rem);font-weight:800;line-height:1.3;margin:.6rem 0 1.2rem}.arc-step{font-weight:700;opacity:.8}
.arc-ans{display:grid;grid-template-columns:1fr 1fr;gap:1rem}.arc-ans button{min-height:88px;font-size:1.4rem;border-radius:20px}
.arc-ans .m{background:#ff8a65;color:#1d0700}.arc-ans .f{background:#69f0ae;color:#00210f}
.arc-ev{margin-top:1.2rem}.arc-ev h3{margin:.2rem 0 .5rem}.arc-ev img{width:100%;max-height:340px;object-fit:cover;border-radius:16px}.arc-verdict{font-size:1.3rem;font-weight:900}
.arc-start{text-align:center}.arc-start .arc-go{min-height:64px;font-size:1.3rem;padding:.8rem 2rem}.arc-ev .src{font-size:.95rem}.arc-filter{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin:1rem 0}.arc-filter button[aria-pressed=true]{background:#ffd54a;color:#1a1300}
.bp-form{display:flex;flex-wrap:wrap;gap:.8rem;align-items:flex-end;max-width:760px}.bp-form label{display:flex;flex-direction:column;gap:.3rem;font-weight:700;flex:1 1 260px}
.bp-form input,.bp-form select{min-height:48px;font:inherit;font-size:1.1rem;padding:.4rem .8rem;border-radius:12px}
.bp-form input{background:#fff;color:#0b1030;border:2px solid #ffd54a;box-shadow:0 0 0 3px rgba(255,213,74,.18)}.bp-form input::placeholder{color:#5a6390;opacity:1}
.bp-form input:focus-visible,.bp-form select:focus-visible{outline:3px solid #4fc3ff;outline-offset:2px}
.bp-card{display:grid;grid-template-columns:1fr auto;max-width:900px;margin:1.5rem auto;border-radius:24px;overflow:hidden;color:#0b1030;background:#fff;box-shadow:0 14px 40px rgba(0,0,0,.35)}
.bp-main{padding:1.4rem 1.6rem;background:linear-gradient(135deg,#fff 60%,#eef3ff)}.bp-top{display:flex;justify-content:space-between;align-items:center;gap:1rem;background:linear-gradient(90deg,#141047,#2a2fb0);color:#fff;margin:-1.4rem -1.6rem 1rem;padding:1rem 1.6rem}
.bp-top b{font-size:1.25rem;letter-spacing:.12em}.bp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.8rem 1.4rem}
.bp-grid dt{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#4a5280;font-weight:800}.bp-grid dd{margin:0;font-size:1.15rem;font-weight:800}
.bp-name{font-size:clamp(1.6rem,4vw,2.4rem)!important}.bp-stub{width:190px;padding:1.2rem;border-inline-start:3px dashed #9aa3d6;display:flex;flex-direction:column;justify-content:space-between;align-items:center;text-align:center;background:#f4f6ff}
.bp-rocket{font-size:4rem}.bp-bars{width:100%;height:56px;background:repeating-linear-gradient(90deg,#0b1030 0 3px,transparent 3px 6px,#0b1030 6px 7px,transparent 7px 11px)}
.bp-fine{font-size:.8rem;color:#4a5280;margin-top:1rem}@media (max-width:640px){.bp-card{grid-template-columns:1fr}.bp-stub{width:auto;border-inline-start:0;border-top:3px dashed #9aa3d6}}
.k1-new{margin:1.6rem 0 0}.k1-new ul{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:1.1rem;list-style:none;padding:0;margin:.6rem 0 0}
@media (prefers-reduced-motion:reduce){.k1-meter i{transition:none}}
@media print{body *{visibility:hidden}.k1-printable,.k1-printable *{visibility:visible}.k1-printable{position:absolute;inset:0 auto auto 0;width:100%}.k1-noprint,.k1-noprint *{display:none!important}.k1-print-name{display:block;font-size:1.3rem;margin:1rem 0}
.k1-stamp{break-inside:avoid;border-color:#999!important}.bp-card{box-shadow:none;border:2px solid #333}}"""

def shell(l, page, title, desc):
    s = rd(d(l) + 'Play_and_Learn.html')
    head = s[:s.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(title) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<style id="k1css">.*?</style>\n?', '', head, flags=re.S)
    head = head.replace('Play_and_Learn.jpg', '@@OG@@').replace('Play_and_Learn.html', page).replace('@@OG@@', 'Play_and_Learn.jpg')
    if l == 'he' and not L.HE_PUBLIC: head = L.ensure_hidden_robots(head)
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": f"{SITE}{d(l)}{page}", "inLanguage": l,
          "audience": {"@type": "EducationalAudience", "educationalRole": "student"}, "isAccessibleForFree": True}
    head += f'<style id="k1css">{CSS}</style>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    body = re.search(r'<body[^>]*>', s).group(0)
    nav = s[s.index(body) + len(body):s.index('<main')]
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Play_and_Learn.html', page), nav, flags=re.S)
    foot = s[s.index('</main>'):]
    return head + '</head>\n' + body + nav, foot

def hero(art, t, chip=''):
    c = f'<span class="k1-chip">{esc(chip)}</span>' if chip else ''
    return f'<section class="k1-hero"><div class="k1-art" aria-hidden="true">{art}</div><h1>{esc(t["title"])}</h1><p>{esc(t["kicker"])}</p>{c}</section>\n'

# ---------- P-07 Space Passport ----------
def hubs(l):
    m = json.load(open('assets/data/solutions.json', encoding='utf8'))['solutionsMenu']; out = []
    for h in m:
        p = d(l) + h['href']; name = h['hub']
        if os.path.exists(p):
            mm = re.search(r'<h1[^>]*>(.*?)</h1>', rd(p), re.S)
            if mm and strip(mm.group(1)): name = strip(mm.group(1))
        out.append(dict(k=h['href'][:-5], n=name, e=HUB_EMOJI.get(h['href'], '⭐'), h=href(l, h['href']), pages=[h['href'][:-5]] + [i['href'][:-5] for i in h['items']]))
    return out
def play_tiles(l):
    s = rd(d(l) + 'Play_and_Learn.html'); s = re.sub(r'<!-- KIDSP1:START -->.*?<!-- KIDSP1:END -->', '', s, flags=re.S)
    return [dict(k=k, n=strip(n), e=PLAY_EMOJI.get(k, '⭐'), h=href(l, k + '.html')) for k, n in re.findall(r'class="pl-tile" data-page="([^"]+)"[^>]*>.*?<span class="pl-name">(.*?)</span>', s, re.S)]
def stamp(x, t):
    return (f'<li><a class="k1-stamp" data-k="{esc(x["k"])}" href="{esc(x["h"])}"><span class="k1-ring" aria-hidden="true">{x["e"]}</span>'
            f'<span class="k1-sname">{esc(x["n"])}</span>{("<span class=k1-note>" + esc(x["t"]) + "</span>") if x.get("t") else ""}<span class="k1-sstate">{esc(t["not_yet"])}</span></a></li>')
PJS = r"""(function(){var w=document.getElementById('k1p');if(!w)return;var T=JSON.parse(w.dataset.t),H=JSON.parse(w.dataset.hubs),KP='sp-pass-v1',KY='sp-play-v1';
function g(k){try{return JSON.parse(localStorage.getItem(k))||{}}catch(e){return {}}}function s(k,o){try{localStorage.setItem(k,JSON.stringify(o))}catch(e){}}
function have(){var p=g(KP),y=g(KY),v=p.p||{},o={};H.forEach(function(h){h.pages.some(function(x){return v[x]})&&(o[h.k]=1)});
Object.keys(y).forEach(function(k){o[k]=1});['Myth_vs_Fact','Amazing_Facts','Kids_Map','Spot_the_Fire','Satellite_Explorer','Glossary'].forEach(function(k){v[k]&&(o[k]=1)});
if(Object.keys(p.l||{}).length>1)o.b_lang=1;v.Myth_or_Fact_Arcade&&(o.b_arcade=1);v.Boarding_Pass&&(o.b_pass=1);return o}
function draw(){var o=have(),a=w.querySelectorAll('.k1-stamp'),n=0;[].forEach.call(a,function(e){var on=!!o[e.dataset.k];on&&n++;e.classList.toggle('on',on);e.querySelector('.k1-sstate').textContent=on?'✓ '+T.got:T.not_yet});
var t=a.length,r=T.ranks,i=n?Math.min(r.length-1,1+Math.floor((n/t)*(r.length-1))):0;if(n>=t)i=r.length-1;
var ch=document.querySelector('.k1-hero .k1-chip');if(ch)ch.textContent=T.count.replace('{n}',n).replace('{t}',t);w.querySelector('.k1-count').textContent=T.count.replace('{n}',n).replace('{t}',t);w.querySelector('.k1-rank').textContent=(n?'🏅 ':'🚀 ')+r[i];w.querySelector('.k1-meter i').style.width=(t?100*n/t:0)+'%'}
function code(){var p=g(KP),y=g(KY);return 'SP1-'+btoa(unescape(encodeURIComponent(JSON.stringify({p:Object.keys(p.p||{}),l:Object.keys(p.l||{}),y:Object.keys(y)}))))}
w.querySelector('.k1-copy').addEventListener('click',function(){var c=code(),b=this,m=w.querySelector('.k1-msg');w.querySelector('.k1-code').value=c;
(navigator.clipboard?navigator.clipboard.writeText(c):Promise.reject()).then(function(){m.textContent=T.copied},function(){w.querySelector('.k1-code').select();m.textContent=c})});
w.querySelector('.k1-load').addEventListener('click',function(){var v=w.querySelector('.k1-code').value.trim(),m=w.querySelector('.k1-msg');try{if(v.indexOf('SP1-')!==0)throw 0;
var o=JSON.parse(decodeURIComponent(escape(atob(v.slice(4))))),ok=/^[\w.-]{1,60}$/,p=g(KP),y=g(KY);p.p=p.p||{};p.l=p.l||{};
(o.p||[]).forEach(function(k){ok.test(k)&&(p.p[k]=1)});(o.l||[]).forEach(function(k){/^[a-z]{2}$/.test(k)&&(p.l[k]=1)});(o.y||[]).forEach(function(k){ok.test(k)&&(y[k]=y[k]||1)});
s(KP,p);s(KY,y);draw();m.textContent=T.ok}catch(e){m.textContent=T.bad}});
w.querySelector('.k1-print').addEventListener('click',function(){window.print()});
w.querySelector('.k1-reset').addEventListener('click',function(){if(confirm(T.confirm)){try{localStorage.removeItem(KP);localStorage.removeItem(KY)}catch(e){}draw()}});
draw();window.addEventListener('pageshow',draw)})();"""
def passport(l):
    t = PASS[l]; P = 'Space_Passport.html'; top, foot = shell(l, P, t['title'], t['desc'])
    H = hubs(l); Y = play_tiles(l)
    B = [dict(k='b_lang', n=t['b_lang'], t=t['b_lang_t'], e='🌍', h='#'), dict(k='b_arcade', n=t['b_arcade'], t=t['b_arcade_t'], e='🕵️', h=href(l, 'Myth_or_Fact_Arcade.html')),
         dict(k='b_pass', n=t['b_pass'], t=t['b_pass_t'], e='🎫', h=href(l, 'Boarding_Pass.html'))]
    tot = len(H) + len(Y) + len(B)
    tj = {k: t[k] for k in ('count', 'got', 'not_yet', 'copied', 'ok', 'bad', 'confirm', 'ranks')}
    hj = [dict(k=h['k'], pages=h['pages']) for h in H]
    main = ('<main id="main">\n' + hero('🛂', t, t['count'].replace('{n}', '0').replace('{t}', str(tot))) +
        f'<div class="k1-wrap k1-printable" id="k1p" data-t="{esc(json.dumps(tj, ensure_ascii=False))}" data-hubs="{esc(json.dumps(hj))}">'
        f'<div class="k1-row" role="status" aria-live="polite"><span class="k1-rank">🚀 {esc(t["ranks"][0])}</span><span class="k1-count">{esc(t["count"].replace("{n}", "0").replace("{t}", str(tot)))}</span></div>'
        f'<div class="k1-meter" aria-hidden="true"><i></i></div><p class="k1-print-name">{esc(t["explorer"])} ____________________</p>'
        f'<h2>{esc(t["hubs"])}</h2><ul class="k1-stamps">' + ''.join(stamp(x, t) for x in H) + '</ul>'
        f'<h2>{esc(t["play"])}</h2><ul class="k1-stamps">' + ''.join(stamp(x, t) for x in Y) + '</ul>'
        f'<h2>{esc(t["bonus"])}</h2><ul class="k1-stamps">' + ''.join(stamp(x, t) for x in B) + '</ul>'
        f'<div class="k1-noprint"><div class="k1-row"><button type="button" class="k1-btn k1-print">🖨️ {esc(t["print"])}</button></div>'
        f'<h2>{esc(t["move"])}</h2><p>{esc(t["move_t"])}</p><label class="visually-hidden" for="k1code">{esc(t["paste"])}</label>'
        f'<textarea id="k1code" class="k1-code" placeholder="{esc(t["paste"])}" spellcheck="false" autocomplete="off"></textarea>'
        f'<div class="k1-row"><button type="button" class="k1-btn alt k1-copy">{esc(t["copy"])}</button><button type="button" class="k1-btn alt k1-load">{esc(t["load"])}</button>'
        f'<span class="k1-msg" role="status" aria-live="polite"></span></div>'
        f'<p class="k1-note">🔒 {esc(t["note"])}</p><button type="button" class="k1-btn alt k1-reset">{esc(t["reset"])}</button></div></div>\n'
        f'<script>{PJS}</script>\n')
    return top + main + foot

# ---------- P-08 Evidence Arcade ----------
def abs_url(u): return u if re.match(r'https?:|/', u) else '/' + re.sub(r'^(\.\./)+', '', u)
def claims(l):
    out = []
    s = rd(d(l) + 'Myth_vs_Fact.html')
    for mid, body in re.findall(r'<article class="myth-card" id="(myth-\d+)">(.*?)</article>', s, re.S):
        c = re.search(r'<h2[^>]*>(.*?)</h2>', body, re.S); ps = re.findall(r'<p(?: class="([^"]*)")?[^>]*>(.*?)</p>', body, re.S)
        ev = [strip(x) for cl, x in ps if not cl]; hon = [strip(x) for cl, x in ps if cl == 'myth-honest']
        src = re.search(r'<p class="myth-source">.*?<a href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
        if c and ev and src: out.append(dict(m=1, c=strip(c.group(1)), e=ev[0], x=hon[0] if hon else '', u=src.group(1), s=strip(src.group(2)), h=f'{href(l, "Myth_vs_Fact.html")}#{mid}'))
    s = rd(d(l) + 'Amazing_Facts.html')
    for fid, body in re.findall(r'<div class="w-card"[^>]*? id="(fact-[^"]+)"[^>]*>(.*?)<span class="dt-mini"', s, re.S):
        ps = re.findall(r'<p(?: class="([^"]*)")?[^>]*>(.*?)</p>', body, re.S); txt = [strip(x) for cl, x in ps if not cl]
        src = re.search(r'<p class="fact-source">[^<]*<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', body, re.S)
        img = re.search(r'<img[^>]*\bsrc="([^"]+)"[^>]*\balt="([^"]*)"|<img[^>]*\balt="([^"]*)"[^>]*\bsrc="([^"]+)"', body)
        cred = re.search(r'<p class="fact-credit">(.*?)</p>', body, re.S); h3 = re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S)
        if txt and src:
            i, a = ((img.group(1), img.group(2)) if img.group(1) else (img.group(4), img.group(3))) if img else ('', '')
            out.append(dict(m=0, c=txt[0], e=strip(h3.group(1)) if h3 else '', u=src.group(1), s=strip(src.group(2)), i=abs_url(i) if i else '', a=html.unescape(a), r=strip(cred.group(1)) if cred else '', h=f'{href(l, "Amazing_Facts.html")}#{fid}'))
    return out
AJS = r"""(function(){var w=document.getElementById('k1a');if(!w)return;var T=JSON.parse(w.dataset.t),A=JSON.parse(document.getElementById('k1a-data').textContent),Q=[],i=0,sc=0,mode='all';
var $=function(q){return w.querySelector(q)},card=$('.arc-card');
function sh(a){for(var j=a.length-1;j>0;j--){var k=Math.floor(Math.random()*(j+1)),t=a[j];a[j]=a[k];a[k]=t}return a}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function start(){Q=sh(A.filter(function(q){return mode==='all'||(mode==='m'?q.m:!q.m)}));i=0;sc=0;show()}
function show(){card.innerHTML='';var q=Q[i];if(!q){card.appendChild(el('p','arc-verdict','🏆 '+T.done));card.appendChild(el('p','arc-claim',T.score.replace('{s}',sc).replace('{n}',Q.length)));
var b=el('button','k1-btn',T.again);b.type='button';b.onclick=start;card.appendChild(b);b.focus();return}
card.appendChild(el('p','arc-step',T.claim.replace('{i}',i+1).replace('{n}',Q.length)));var c=el('p','arc-claim','“'+q.c+'”');c.tabIndex=-1;card.appendChild(c);
var g=el('div','arc-ans');[[1,'m','🙅 '+T.myth],[0,'f','✅ '+T.fact]].forEach(function(o){var b=el('button','k1-btn '+o[1],o[2]);b.type='button';b.onclick=function(){answer(o[0])};g.appendChild(b)});card.appendChild(g);c.focus()}
function answer(m){var q=Q[i],ok=(m===q.m);ok&&sc++;card.querySelector('.arc-ans').remove();var v=el('div','arc-ev');v.setAttribute('role','status');
v.appendChild(el('p','arc-verdict',(ok?'🎉 '+T.right:'🔎 '+T.wrong)+' '+(q.m?T.is_myth:T.is_fact)));v.appendChild(el('h3','',T.how));
if(q.i){var im=el('img');im.src=q.i;im.alt=q.a||'';im.loading='lazy';im.decoding='async';v.appendChild(im);q.r&&v.appendChild(el('p','fact-credit',q.r))}
if(q.m){v.appendChild(el('p','',q.e));q.x&&v.appendChild(el('p','',q.x))}else if(q.e)v.appendChild(el('p','',q.e));
var s=el('p','src',T.src+' ');var a=el('a','',q.s);a.href=q.u;a.target='_blank';a.rel='noopener';s.appendChild(a);v.appendChild(s);
var r=el('p');var b2=el('a','',T.more);b2.href=q.h;r.appendChild(b2);v.appendChild(r);var n=el('button','k1-btn',T.next+' →');n.type='button';n.onclick=function(){i++;show()};v.appendChild(n);card.appendChild(v);n.focus()}
[].forEach.call(w.querySelectorAll('.arc-filter button'),function(b){b.onclick=function(){mode=b.dataset.m;[].forEach.call(w.querySelectorAll('.arc-filter button'),function(x){x.setAttribute('aria-pressed',x===b)});start()}});
$('.arc-go').onclick=start})();"""
def arcade(l):
    t = ARC[l]; P = 'Myth_or_Fact_Arcade.html'; C = claims(l); n = len(C); top, foot = shell(l, P, t['title'], t['desc'])
    nm = sum(c['m'] for c in C)
    tj = {k: t[k] for k in ('myth', 'fact', 'right', 'wrong', 'is_myth', 'is_fact', 'how', 'src', 'more', 'next', 'score', 'done', 'again', 'claim')}
    main = ('<main id="main">\n' + hero('🕵️', t, t['cards'].replace('{n}', str(n))) +
        f'<div class="k1-wrap" id="k1a" data-t="{esc(json.dumps(tj, ensure_ascii=False))}" data-myths="{nm}" data-facts="{n - nm}">'
        f'<div class="arc-filter" role="group"><button type="button" class="k1-btn alt" data-m="all" aria-pressed="true">{esc(t["all"])} ({n})</button>'
        f'<button type="button" class="k1-btn alt" data-m="m" aria-pressed="false">{esc(t["only_m"])} ({nm})</button><button type="button" class="k1-btn alt" data-m="f" aria-pressed="false">{esc(t["only_f"])} ({n - nm})</button></div>'
        f'<div class="arc-card arc-start" aria-live="polite"><button type="button" class="k1-btn arc-go">▶ {esc(t["start"])}</button></div>'
        f'<p class="k1-note" style="text-align:center">🔒 {esc(t["note"])}</p></div>\n'
        f'<script type="application/json" id="k1a-data">{json.dumps(C, ensure_ascii=False).replace("</", "<\\/")}</script>\n<script>{AJS}</script>\n')
    return top + main + foot, n

# ---------- P-16 Boarding pass ----------
BJS = r"""(function(){var w=document.getElementById('k1b');if(!w)return;var T=JSON.parse(w.dataset.t),lang=document.documentElement.lang||'en',rtl=document.documentElement.dir==='rtl',L=[];
var $=function(q){return w.querySelector(q)},sel=$('#bp-l'),nm=$('#bp-n'),card=$('.bp-card');
function fmt(x){var o={year:'numeric',month:'long',day:'numeric'};if(x.exact){o.hour='numeric';o.minute='2-digit';o.timeZoneName='short'}try{return new Intl.DateTimeFormat(lang,o).format(new Date(x.net))}catch(e){return x.net.slice(0,10)}}
function fill(){var x=L[sel.value|0];if(!x)return;var n=(nm.value||'').trim().slice(0,24)||T.explorer;card.querySelector('.bp-name').textContent=n;
['mission','rocket','provider','site'].forEach(function(k){card.querySelector('[data-f='+k+']').textContent=x[k]||'—'});card.querySelector('[data-f=when]').textContent=fmt(x);card.hidden=false}
fetch('/assets/data/map-launches.json').then(function(r){return r.json()}).then(function(j){var now=Date.now();(j.sites||[]).forEach(function(s){(s.launches||[]).forEach(function(x){var t=Date.parse(x.net);if(t>now)L.push({net:x.net,exact:!!x.exact,t:t,mission:x.mission,rocket:x.rocket,provider:x.provider,site:s.name})})});
L.sort(function(a,b){return (b.exact-a.exact)||(a.t-b.t)});L=L.slice(0,12).sort(function(a,b){return a.t-b.t});
if(!L.length){$('.bp-none').hidden=false;$('.bp-form').hidden=true;return}L.forEach(function(x,i){var o=document.createElement('option');o.value=i;o.textContent=x.mission+' · '+x.rocket+' · '+fmt(x);sel.appendChild(o)});fill()})
.catch(function(){$('.bp-none').hidden=false;$('.bp-form').hidden=true});
$('.bp-make').onclick=function(){fill();card.querySelector('.bp-name').focus()};nm.oninput=fill;sel.onchange=fill;$('.bp-print').onclick=function(){fill();window.print()};
$('.bp-png').onclick=function(){fill();var x=L[sel.value|0];if(!x)return;var c=document.createElement('canvas'),W=1800,H=760,g=c.getContext('2d');c.width=W;c.height=H;
var gr=g.createLinearGradient(0,0,W,0);gr.addColorStop(0,'#141047');gr.addColorStop(1,'#2a2fb0');g.fillStyle='#fff';g.fillRect(0,0,W,H);g.fillStyle=gr;g.fillRect(0,0,W,130);
g.direction=rtl?'rtl':'ltr';g.textAlign=rtl?'right':'left';var X=rtl?W-470:70,F='system-ui,-apple-system,Segoe UI,Arial,sans-serif';
g.fillStyle='#fff';g.font='800 54px '+F;g.fillText('🚀 '+T.pass_h,rtl?W-70:70,88);g.fillStyle='#4a5280';g.font='800 28px '+F;g.fillText(T.passenger.toUpperCase(),X,200);
g.fillStyle='#0b1030';g.font='900 80px '+F;g.fillText(card.querySelector('.bp-name').textContent,X,285);
var rows=[[T.mission,x.mission],[T.rocket,x.rocket],[T.provider,x.provider],[T.site,x.site],[T.when,fmt(x)]],y=370;rows.forEach(function(r,k){var cx=rtl?X-(k%2)*560:X+(k%2)*560;if(k&&k%2===0)y+=110;
g.fillStyle='#4a5280';g.font='800 24px '+F;g.fillText(r[0].toUpperCase(),cx,y);g.fillStyle='#0b1030';g.font='800 36px '+F;var v=String(r[1]||'—');while(g.measureText(v).width>530&&v.length>4)v=v.slice(0,-2)+'…';g.fillText(v,cx,y+44)});
g.strokeStyle='#9aa3d6';g.setLineDash([14,10]);g.lineWidth=4;var sx=rtl?400:W-400;g.beginPath();g.moveTo(sx,130);g.lineTo(sx,H);g.stroke();g.setLineDash([]);
g.textAlign='center';g.font='160px '+F;g.fillText('🚀',rtl?200:W-200,360);g.fillStyle='#4a5280';g.font='700 22px '+F;g.textAlign=rtl?'right':'left';
g.fillText(T.keep,rtl?W-70:70,H-70);g.fillText('savingplanets.com · '+T.credit,rtl?W-70:70,H-32);
var a=document.createElement('a');a.download='boarding-pass.png';a.href=c.toDataURL('image/png');document.body.appendChild(a);a.click();a.remove()}})();"""
def boarding(l):
    t = BP[l]; P = 'Boarding_Pass.html'; top, foot = shell(l, P, t['title'], t['desc'])
    tj = {k: t[k] for k in ('explorer', 'pass_h', 'passenger', 'mission', 'rocket', 'provider', 'site', 'when', 'keep')}; tj['credit'] = CREDIT[l]
    f = lambda k: f'<div><dt>{esc(t[k])}</dt><dd data-f="{k}">—</dd></div>'
    main = ('<main id="main">\n' + hero('🎫', t) +
        f'<div class="k1-wrap" id="k1b" data-t="{esc(json.dumps(tj, ensure_ascii=False))}">'
        f'<p class="bp-none" hidden>{esc(t["none"])}</p><div class="bp-form k1-noprint">'
        f'<label for="bp-n">{esc(t["name"])}<input id="bp-n" type="text" placeholder="{esc(t["ph"])}" maxlength="24" autocomplete="off" autocapitalize="words" spellcheck="false" aria-describedby="bp-h"></label>'
        f'<label for="bp-l">{esc(t["pick"])}<select id="bp-l"></select></label><button type="button" class="k1-btn bp-make">{esc(t["make"])}</button></div>'
        f'<p id="bp-h" class="k1-note k1-noprint">🔒 {esc(t["hint"])}</p>'
        f'<div class="k1-printable"><div class="bp-card" hidden><div class="bp-main"><div class="bp-top"><b>{esc(t["pass_h"])}</b><span aria-hidden="true">🌍 → 🌌</span></div>'
        f'<dl class="bp-grid"><div style="grid-column:1/-1"><dt>{esc(t["passenger"])}</dt><dd class="bp-name" tabindex="-1">{esc(t["explorer"])}</dd></div>{f("mission")}{f("rocket")}{f("provider")}{f("site")}{f("when")}</dl>'
        f'<p class="bp-fine">⚠️ {esc(t["keep"])} {esc(t["shifts"])}</p></div><div class="bp-stub"><span class="bp-rocket" aria-hidden="true">🚀</span><div class="bp-bars" aria-hidden="true"></div>'
        f'<p class="bp-fine">{esc(CREDIT[l])}</p></div></div></div>'
        f'<div class="k1-row k1-noprint"><button type="button" class="k1-btn bp-print">🖨️ {esc(t["print"])}</button><button type="button" class="k1-btn alt bp-png">⬇️ {esc(t["png"])}</button>'
        f'<a class="k1-btn alt" href="{href(l, "World_Map.html")}">🗺️ {esc(t["tracker"])}</a></div>'
        f'<p class="k1-note">{esc(t["src"])} <a href="https://thespacedevs.com/llapi" target="_blank" rel="noopener">thespacedevs.com</a></p></div>\n<script>{BJS}</script>\n')
    return top + main + foot

# ---------- Play & Learn 'New' row ----------
def playrow(l):
    p = d(l) + 'Play_and_Learn.html'; s = rd(p); s = re.sub(r'<!-- KIDSP1:START -->.*?<!-- KIDSP1:END -->', '', s, flags=re.S)
    items = [('Space_Passport.html', '🛂', PASS[l]['title'], PASS[l]['kicker']), ('Myth_or_Fact_Arcade.html', '🕵️', ARC[l]['title'], ARC[l]['kicker']), ('Boarding_Pass.html', '🎫', BP[l]['title'], BP[l]['kicker'])]
    li = ''.join(f'<li><a class="pl-tile" href="{href(l, h)}"><span class="pl-emoji" aria-hidden="true">{e}</span><span class="pl-name">{esc(n)}</span><span class="pl-text">{esc(x)}</span></a></li>' for h, e, n, x in items)
    blk = (f'<!-- KIDSP1:START --><style>.k1-new{{margin:1.6rem 0 0}}.k1-new .pl-grid{{list-style:none;padding:0;margin:.6rem 0 0}}.k1-new .pl-tile{{min-height:0;height:100%}}'
           f'@media (min-width:760px){{.k1-new .pl-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}</style>'
           f'<section class="k1-new" aria-labelledby="k1new"><h2 id="k1new">✨ {esc(NEW[l])}</h2><ul class="pl-grid">{li}</ul></section><!-- KIDSP1:END -->')
    s = s.replace('<p class="pl-note">', blk + '\n<p class="pl-note">', 1)
    return wr(p, s)

# ---------- P-18 Superpowers + visit recorder (site.js) ----------
KIDS_ALL = ['Play_and_Learn', 'Kids', 'Kids_Map', 'Spot_the_Fire', 'Satellite_Explorer', 'Amazing_Facts', 'Myth_vs_Fact', 'Glossary', 'Space_Passport', 'Myth_or_Fact_Arcade',
        'Boarding_Pass', 'Orbits_Guide', 'Orbit_Lab', 'Learn', 'Teachers', 'Lesson_Builder', 'Student_Questions']
# Oct 17: list only pages that exist and are not redirect stubs (Kids.html -> Play_and_Learn); Student_Questions joins when it is built.
KIDS = [k for k in KIDS_ALL if k in PAGE_STEMS or (os.path.exists(k + '.html') and 'http-equiv="refresh"' not in rd(k + '.html'))]
SJS = r"""/* SPOW:START */
(function(){var pg=(location.pathname.split('/').pop()||'index').replace(/\.html$/,'')||'index',lang=(document.documentElement.lang||'en').slice(0,2);
try{var K='sp-pass-v1',o=JSON.parse(localStorage.getItem(K))||{};o.p=o.p||{};o.l=o.l||{};o.p[pg]=1;o.l[lang]=1;localStorage.setItem(K,JSON.stringify(o))}catch(e){}
var KS='sp-pow-v1',S={};try{S=JSON.parse(localStorage.getItem(KS))||{}}catch(e){}var R=document.documentElement;
function apply(){R.classList.toggle('sp-big1',S.big===1);R.classList.toggle('sp-big2',S.big===2);['dys','hc','calm','tap'].forEach(function(k){R.classList.toggle('sp-'+k,!!S[k])});
if(S.tap)[].forEach.call(document.querySelectorAll('[draggable=true]'),function(e){e.setAttribute('draggable','false');e.dataset.spDrag='1'});
else[].forEach.call(document.querySelectorAll('[data-sp-drag]'),function(e){e.setAttribute('draggable','true');delete e.dataset.spDrag});
if(S.calm)[].forEach.call(document.querySelectorAll('video[autoplay]'),function(v){try{v.pause()}catch(e){}})}
apply();if(KIDS_LIST.indexOf(pg)<0)return;R.classList.add('sp-kidspage');
var T=SPOW_T[lang]||SPOW_T.en;
var css='.sp-big1{font-size:118%}.sp-big2{font-size:135%}.sp-dys body,.sp-dys body *:not(code):not(pre):not(.k1-ring):not([class*=emoji]){font-family:Verdana,Tahoma,"Trebuchet MS",Arial,sans-serif!important;font-style:normal!important;line-height:1.65!important}'
+'.sp-dys body *:not(:lang(ar)):not(:lang(he)){letter-spacing:.05em!important;word-spacing:.16em!important}.sp-dys main p,.sp-dys main li{max-width:70ch;text-align:start!important}'
+'.sp-hc body,.sp-hc main,.sp-hc main *:not(img):not(video):not(canvas):not(svg):not(svg *){background-color:#000!important;background-image:none!important;color:#fff!important;border-color:#fff!important;box-shadow:none!important;text-shadow:none!important}'
+'.sp-hc main a{color:#ffe14d!important;text-decoration:underline!important}.sp-hc main button,.sp-hc main .k1-btn{outline:2px solid #fff}'
+'.sp-calm *,.sp-calm *:before,.sp-calm *:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}'
+'html.sp-kidspage main{padding-bottom:84px}html.sp-has-lb .spow-b{bottom:calc(var(--sp-lb-h,0px) + 12px)}html.sp-has-lb .spow-p{bottom:calc(var(--sp-lb-h,0px) + 76px)}'
+'.spow-b{position:fixed;z-index:9990;bottom:16px;inset-inline-start:16px;min-height:48px;padding:.45rem .95rem;font-size:.95rem!important;border-radius:999px;border:2px solid #fff;background:#4a3aa8;color:#fff;font:inherit;font-weight:800;box-shadow:0 6px 18px rgba(0,0,0,.35);cursor:pointer}'
+'.spow-b:focus-visible,.spow-p button:focus-visible{outline:3px solid #ffd54a;outline-offset:3px}'
+'.spow-p{position:fixed;z-index:9991;bottom:80px;inset-inline-start:16px;width:min(340px,calc(100vw - 32px));max-height:calc(100vh - 110px);overflow:auto;padding:1rem;border-radius:20px;background:#13123a;color:#fff;border:2px solid rgba(255,255,255,.35);box-shadow:0 14px 40px rgba(0,0,0,.5)}'
+'.spow-p h2{font-size:1.2rem;margin:0 0 .6rem;color:#fff}.spow-p button{display:flex;width:100%;align-items:center;justify-content:space-between;gap:.6rem;min-height:48px;margin:.3rem 0;padding:.5rem .9rem;border-radius:14px;border:2px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:#fff;font:inherit;font-weight:700;cursor:pointer;text-align:start}'
+'.spow-p button[aria-pressed=true]{background:#ffd54a;color:#1a1300;border-color:#ffd54a}.spow-p p{font-size:.85rem;opacity:.85;margin:.5rem 0 0}.spow-p .spow-x{width:auto;display:inline-flex;margin:0;float:inline-end}'
+'@media print{.spow-b,.spow-p{display:none!important}}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
var b=el('button','spow-b','✨ '+T.btn);b.type='button';b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','spow-p');
var p=el('div','spow-p');p.id='spow-p';p.hidden=true;p.setAttribute('role','dialog');p.setAttribute('aria-label',T.h);
var x=el('button','spow-x','✕');x.type='button';x.setAttribute('aria-label',T.close);p.appendChild(x);p.appendChild(el('h2','',T.h));
var msg=el('p');msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');
var rd=el('button','','🔊 '+T.read);rd.type='button';p.appendChild(rd);
function tog(k,lab,ic){var e=el('button','',ic+' '+lab);e.type='button';function u(){e.setAttribute('aria-pressed',k==='big'?String(!!S.big):String(!!S[k]));if(k==='big')e.textContent=ic+' '+lab+['',' +',' ++'][S.big||0]}
e.onclick=function(){if(k==='big')S.big=((S.big||0)+1)%3;else S[k]=!S[k];save();u()};u();p.appendChild(e);return u}
function save(){try{localStorage.setItem(KS,JSON.stringify(S))}catch(e){}apply()}
var U=[tog('big',T.big,'🔠'),tog('dys',T.dys,'📖'),tog('hc',T.hc,'🌓'),tog('calm',T.calm,'🐢'),tog('tap',T.tap,'👆')];
var rs=el('button','','↺ '+T.reset);rs.type='button';rs.onclick=function(){S={};save();U.forEach(function(f){f()})};p.appendChild(rs);p.appendChild(msg);p.appendChild(el('p','','🔒 '+T.note));
var ss=window.speechSynthesis,speaking=false;
function stop(){if(ss)ss.cancel();speaking=false;rd.textContent='🔊 '+T.read;rd.setAttribute('aria-pressed','false')}
function text(){var s=window.getSelection&&String(window.getSelection()).trim();if(s)return s;var m=document.querySelector('main')||document.body,c=m.cloneNode(true);
[].forEach.call(c.querySelectorAll('script,style,nav,button,textarea,select,[hidden],[aria-hidden=true],.dt-mini,.visually-hidden,.k1-noprint'),function(e){e.remove()});return c.textContent.replace(/\s+/g,' ').trim()}
rd.onclick=function(){if(speaking){stop();return}if(!ss||!window.SpeechSynthesisUtterance){msg.textContent=T.novoice;return}
var vs=ss.getVoices(),v=vs.filter(function(v){return v.lang&&v.lang.toLowerCase().indexOf(lang)===0||(lang==='he'&&/^iw/i.test(v.lang))});if(vs.length&&!v.length){msg.textContent=T.novoice;return}
var parts=text().match(/[^.!?。؟]+[.!?。؟]*\s*/g)||[];if(!parts.length)return;speaking=true;rd.textContent='⏹ '+T.stop;rd.setAttribute('aria-pressed','true');msg.textContent='';
parts.forEach(function(t,i){var u=new SpeechSynthesisUtterance(t);u.lang=document.documentElement.lang||lang;if(v[0])u.voice=v[0];u.rate=.95;if(i===parts.length-1)u.onend=stop;ss.speak(u)})};
function open(o){p.hidden=!o;b.setAttribute('aria-expanded',String(o));if(o)(p.querySelector('button:not(.spow-x)')||x).focus()}
b.onclick=function(){open(p.hidden)};x.onclick=function(){open(false);b.focus()};p.addEventListener('keydown',function(e){if(e.key==='Escape'){open(false);b.focus()}});
window.addEventListener('pagehide',stop);
function mount(){document.body.appendChild(p);document.body.appendChild(b)}if(document.body)mount();else document.addEventListener('DOMContentLoaded',mount)})();
/* SPOW:END */
"""
def sitejs():
    s = rd('site.js'); js = SJS.replace('KIDS_LIST', json.dumps(KIDS)).replace('SPOW_T', json.dumps({l: SPOW[l] for l in SPOW}, ensure_ascii=False))
    s2 = re.sub(r'\n?/\* SPOW:START \*/.*?/\* SPOW:END \*/\n?', '', s, flags=re.S).rstrip('\n') + '\n' + js
    return wr('site.js', s2)

if __name__ == '__main__':
    ch = sitejs(); counts = {}
    for l in LANGS:
        ch += playrow(l)
        ch += wr(d(l) + 'Space_Passport.html', passport(l))
        a, n = arcade(l); counts[l] = n; ch += wr(d(l) + 'Myth_or_Fact_Arcade.html', a)
        ch += wr(d(l) + 'Boarding_Pass.html', boarding(l))
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in PUB:
        for P in PAGES:
            loc = f'{SITE}{d(l)}{P}'
            if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-kids-p1: langs={LANGS} arcade claims={counts} writes={ch}')
