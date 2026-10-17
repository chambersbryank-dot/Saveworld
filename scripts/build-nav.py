#!/usr/bin/env python3
"""Oct 16: header navigation v2 (two right-aligned rows, kidSAFE-style pattern, Saving Planets colours/fonts).
Replaces <nav id="topnav">...</nav> on every page in en/fr/es/ar/it. Idempotent. Run LAST among page generators
(after build-new.py) so pages copied from templates get the right current-page state and language links.
Structure: brand | [utility row: language switch, Search, Weekly Brief, Find a Cleanup, Contact]
                   [main row: Solutions v, Space v, Learn v, Kids v, Teachers v, About v, CTA Help / Donate]
Under 1140px (was 992 until the Oct 16 t886 larger font): brand + menu button; the panel slides down (utility, main items as tap accordions, full-width CTA).
CSS/JS live between SPNAV markers in styles.css / site.js. Keeps <nav id="topnav"> and <li class="lang-switch">
so older generators that copy the nav keep working. No social icons: the site has no social accounts to link."""
import re, os, glob, html, importlib.util, sys
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('ux', 'scripts/build-ux.py'); UX = importlib.util.module_from_spec(spec); spec.loader.exec_module(UX)
import learn_text as LT
LANGS = UX.LANGS; T = UX.T; d = UX.d; rd = UX.rd; wr = UX.wr
X = {
 'en': dict(kids='Kids', teachers='Teachers', si='SI Helper (pilot)', open='Open menu', close='Close menu', util='Site links', main='Main menu', lang='Language'),
 'fr': dict(kids='Enfants', teachers='Enseignants', si='SI Helper (pilote)', open='Ouvrir le menu', close='Fermer le menu', util='Liens du site', main='Menu principal', lang='Langue'),
 'es': dict(kids='Niños', teachers='Docentes', si='SI Helper (piloto)', open='Abrir el menú', close='Cerrar el menú', util='Enlaces del sitio', main='Menú principal', lang='Idioma'),
 'ar': dict(kids='الأطفال', teachers='المعلمون', si='SI Helper (تجريبي)', open='فتح القائمة', close='إغلاق القائمة', util='روابط الموقع', main='القائمة الرئيسية', lang='اللغة'),
 'it': dict(kids='Bambini', teachers='Insegnanti', si='SI Helper (pilota)', open='Apri il menu', close='Chiudi il menu', util='Link del sito', main='Menu principale', lang='Lingua'),
}
# Every link from the previous nav (build-ux GROUPS) stays reachable; About pages (were footer-only) added.
GROUPS = [
 ('sol', ['Solutions.html', 'Oceans.html', 'Rivers.html', 'Lakes.html', 'Deforestation.html', 'Earth_Observation.html', 'World_Map.html', 'Topics.html']),
 ('space', ['Space.html', 'Enceladus.html', 'Artemis_II.html#launches', 'Planetary_Defense.html', 'Space_Weather.html', 'Space_Disposal.html']),
 # Oct 16 6:15 PM (user): Project Rawane back as its own top-level menu right after Space; label links to the overview,
 # first tap/click opens the dropdown (second follows the link); overview pinned first, the rest alphabetical.
 # 6:17/6:18 PM (user): Myth vs Fact listed here AND kept in Kids.
 ('pr', ['Project-Rawane.html', 'Rawanes_Mission_Log.html', 'Myth_vs_Fact.html']),
 ('le', ['Learn.html', 'Orbits_Guide.html', 'Orbit_Math.html', 'Orbit_Lab.html', 'Aero_Guide.html', 'Aero_Math.html', 'Aero_Lab.html', 'Physics_Guide.html', 'Physics_Math.html', 'Physics_Lab.html', 'Calculators.html', 'Cadets.html', 'Homeschool.html', 'AP_IB_Physics.html', 'Careers.html']),
 ('kids', ['Play_and_Learn.html', 'Kids_Map.html', 'Amazing_Facts.html', 'Satellite_Explorer.html', 'Myth_vs_Fact.html', 'Glossary.html']),
 ('teach', ['Teachers.html', 'Lesson_Builder.html', 'SI_Helper.html']),
 ('ab', ['About.html', 'Editorial_Policy.html', 'Corrections.html', 'Press.html', 'Privacy.html']),
]
UTIL = ['Search.html', 'index.html#newsletter', 'Find_a_Cleanup.html', 'Contact.html']
LABEL = {'en': 'EN', 'fr': 'FR', 'es': 'ES', 'ar': 'عربي', 'it': 'IT'}  # ar: 'عربي' is inside 'العربية' (label-in-name)
LANGNAME = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية', 'it': 'Italiano'}
SEARCH_SVG = '<svg aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.6"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>'

def hr(l, i):
    return i if l == 'en' or os.path.exists(d(l) + i.split('#')[0]) else '../' + i

def label(l, key, i):
    t = T[l]
    if key == 'le': return LT.NAV_ITEMS[i][l]
    if i == 'Play_and_Learn.html': return UX.PLAYL[l]
    if i == 'Project-Rawane.html': return UX.PR[l][1][0]
    if i == 'SI_Helper.html': return X[l]['si']
    return t['items'][i]

# Oct 16 (user): sub-items alphabetical by displayed label in each language; Start-here entries + Careers stay pinned at the
# top of their dropdown as a group, in this order. Collation without ICU (weekly sync has no extra deps): leading emoji and
# punctuation ignored, accents folded (primary-strength, like fr/it/es/ar locale collation), Spanish ñ after n, Arabic
# hamza/alef forms folded. Articles are not stripped (raw label).
PINNED = ['Project-Rawane.html', 'Cadets.html', 'Homeschool.html', 'AP_IB_Physics.html', 'Careers.html']
def sort_key(l, lab):
    import unicodedata
    t = html.unescape(re.sub('<[^>]+>', '', lab))
    t = re.sub(r'^[^\w]+', '', t)
    if l == 'es': t = t.replace('ñ', 'n\uffff').replace('Ñ', 'N\uffff')
    if l == 'ar':
        t = re.sub('[أإآٱ]', 'ا', t).replace('ى', 'ي')
        if re.match('[A-Za-z]', t): t = '\uffff' + t  # ICU ar order: Arabic script before Latin
    t = ''.join(c for c in unicodedata.normalize('NFKD', t) if not unicodedata.combining(c))
    return t.casefold()
def sort_items(l, key, items):
    pin = [i for i in PINNED if i in items]
    rest = sorted((i for i in items if i not in pin), key=lambda i: sort_key(l, label(l, key, i)))
    return pin + rest

def gname(l, key):
    return {'sol': T[l]['sol'], 'space': T[l]['items']['Space.html'], 'pr': UX.PR[l][0], 'le': LT.NAV[l], 'kids': X[l]['kids'], 'teach': X[l]['teachers'], 'ab': T[l]['ab']}[key]

def switcher(l, page):
    """Oct 16 (user t886): one slide switch per language (role=switch on the language link, so it still works without JS).
    On = thumb at the inline END and green; off = inline start, grey. LTR: right = on (as asked). Arabic (RTL): mirrored like
    iOS/Android/Material switches in RTL, so on = thumb on the LEFT, still green. Visible text: short code on the desktop row,
    full native name in the mobile menu; the accessible name is always the native name (it starts with the visible code, so
    label-in-name holds). Keeps <li class="lang-switch"> with plain <a href> children for the older generators and Search.html."""
    pre = '' if l == 'en' else '../'
    out = []
    for k in LANGS:
        tgt = page if os.path.exists(d(k) + page) else 'index.html'
        href = pre + d(k) + tgt
        on = k == l
        cur = ' aria-current="true"' if on else ''
        out.append(f'<a class="spn-ls" draggable="false" role="switch" aria-checked="{"true" if on else "false"}" href="{href}" hreflang="{k}" lang="{k}"'
                   f'{cur} aria-label="{LANGNAME[k]}" title="{LANGNAME[k]}" data-lang="{k}">'
                   f'<span class="spn-ls-t" aria-hidden="true"><span class="spn-ls-k"></span></span>'
                   f'<span class="spn-ls-c" aria-hidden="true">{LABEL[k]}</span><span class="spn-ls-n" aria-hidden="true">{LANGNAME[k]}</span></a>')
    return f'<li class="lang-switch"><span class="spn-lt" role="group" aria-label="{X[l]["lang"]}">' + ''.join(out) + '</span></li>'

def nav(l, page, brand_href, brand_txt):
    x = X[l]; t = T[l]
    util = switcher(l, page) + ''.join(
        f'<li><a href="{hr(l, i)}"{" aria-current=\"page\"" if i == page else ""}>{SEARCH_SVG if i == "Search.html" else ""}{t["items"][i]}</a></li>' for i in UTIL)
    main = []
    for key, items in GROUPS:
        cur = any(i.split('#')[0] == page for i in items if '#' not in i)
        items = sort_items(l, key, items)
        lis = ''.join(f'<li><a href="{hr(l, i)}"{" aria-current=\"page\"" if i == page else ""}>{label(l, key, i)}</a></li>' for i in items)
        trig = (f'<a class="spn-trig spn-trig-link" href="{hr(l, items[0])}" aria-expanded="false" aria-controls="spn-{key}">{gname(l, key)}<span class="spn-chev" aria-hidden="true"></span></a>' if key == 'pr' else
                f'<button type="button" class="spn-trig" aria-expanded="false" aria-controls="spn-{key}">{gname(l, key)}<span class="spn-chev" aria-hidden="true"></span></button>')
        main.append(f'<li class="spn-dd{" is-current" if cur else ""}">{trig}'
                    f'<ul class="spn-sub" id="spn-{key}">{lis}</ul></li>')
    main.append(f'<li class="spn-cta nav-help"><a href="Ways_to_Help.html"{" aria-current=\"page\"" if page == "Ways_to_Help.html" else ""}>{t["help"]}</a></li>')
    return (f'<nav id="topnav"><div class="spn"><a class="spn-brand" href="{brand_href}">{brand_txt}</a>'
            f'<button type="button" class="spn-toggle" aria-expanded="false" aria-controls="spn-panel" aria-label="{x["open"]}" data-open="{x["open"]}" data-close="{x["close"]}"><span></span><span></span><span></span></button>'
            f'<div class="spn-panel" id="spn-panel"><ul class="spn-util" aria-label="{x["util"]}">{util}</ul>'
            f'<ul class="spn-main" aria-label="{x["main"]}">{"".join(main)}</ul></div></div></nav>')

NAV_RE = re.compile(r'<nav id="topnav">.*?</nav>', re.S)
BRAND_RE = re.compile(r'<a class="(?:brand-word|spn-brand)" href="([^"]*)">(.*?)</a>', re.S)

CSS = r"""
/* SPNAV:START */
/* Header nav v2 (scripts/build-nav.py). Colours: site navy/dark tokens (#003755, #071018, #0f1b26), accent #009cde / #8fd3ff; Montserrat. */
/* Oct 16: Learn 'On this page' TOC (.lw nav) was caught by the old body.toc-sub nav{position:fixed} rule and covered the hero */html body .lw nav:not(#topnav){position:static !important;background:none;box-shadow:none;z-index:auto;-webkit-backdrop-filter:none;backdrop-filter:none;height:auto}html body nav#topnav{position:fixed !important;top:0;left:0;right:0;z-index:1000;height:auto !important;background:transparent !important;-webkit-backdrop-filter:none !important;backdrop-filter:none !important;box-shadow:none !important;border:0 !important;transition:background-color .3s ease,box-shadow .3s ease !important}
html body nav#topnav::before{content:"";position:absolute;inset:0 0 -28px 0;background:linear-gradient(180deg,rgba(0,20,40,.72),rgba(0,20,40,.35) 70%,rgba(0,20,40,0));pointer-events:none;transition:opacity .3s ease;z-index:-1}
html body nav#topnav.spn-solid,html body nav#topnav.spn-open{background:rgba(7,16,24,.96) !important;box-shadow:0 6px 24px rgba(0,0,0,.35) !important}
html body nav#topnav.spn-open{z-index:1200 !important}
html body nav#topnav.spn-solid::before,html body nav#topnav.spn-open::before{opacity:0}
#topnav .spn{max-width:1280px;margin:0 auto;padding:8px clamp(12px,2.2vw,32px);display:flex;align-items:center;justify-content:space-between;gap:1rem;font-family:"Montserrat","Segoe UI",sans-serif;transition:padding .3s ease}
#topnav.spn-solid .spn{padding-top:2px;padding-bottom:2px}
#topnav .spn ul{list-style:none;margin:0;padding:0}
#topnav .spn a{text-decoration:none}
#topnav .spn-brand{color:#fff;font-weight:700;font-size:1.125rem;white-space:nowrap;min-height:44px;display:inline-flex;align-items:center;flex:none}
#topnav .spn-brand:hover{color:#8fd3ff}
#topnav .spn-toggle{display:none}
/* Oct 16 (t886, larger nav font): desktop = brand + utility row on top, the main menu gets the full width on row 2
   (the panel is display:contents, so util/main become grid items). Same look, room for FR/IT/ES labels at 15px. */
@media (min-width:1140px){#topnav .spn{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:1rem;row-gap:0}#topnav .spn-panel{display:contents}#topnav .spn-brand{grid-column:1;grid-row:1;min-height:32px}#topnav .spn-util{grid-column:2;grid-row:1;justify-self:end}#topnav .spn-main{grid-column:1/-1;grid-row:2;justify-self:end}}
@media (min-width:1140px) and (pointer:coarse){#topnav .spn-brand{min-height:44px}}
#topnav .spn-panel{display:flex;flex-direction:column;align-items:flex-end}
#topnav .spn-util{display:flex;align-items:center;gap:0 1.1rem;font-size:14px;font-weight:600}
#topnav .spn-util a{color:#e8eef5;display:inline-flex;align-items:center;gap:.35rem;min-height:32px;white-space:nowrap}
#topnav .spn-util a:hover{color:#8fd3ff}
#topnav .spn-util a[aria-current]{color:#8fd3ff}
/* Oct 16 (t886) language slide switches: on = green, thumb at the inline end (right in LTR, left in Arabic/RTL) */
#topnav .lang-switch{display:flex;align-items:center;padding:0}
#topnav .spn-lt{display:flex;align-items:center;gap:0 .15rem}
#topnav .spn-util a.spn-ls{position:relative;display:inline-flex;align-items:center;gap:.4rem;min-width:44px;min-height:32px;padding:0 .3rem;box-sizing:border-box;border-radius:999px;color:#c9d4df;font-size:13px;font-weight:700;letter-spacing:.03em;cursor:pointer;touch-action:pan-y;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}
#topnav .spn-ls-t{--spn-x:0px;position:relative;flex:none;width:36px;height:20px;border-radius:999px;background:#5b6774;box-shadow:inset 0 0 0 1px rgba(255,255,255,.28);transition:background-color .2s ease}
#topnav .spn-ls-k{position:absolute;top:2px;inset-inline-start:2px;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.45);transform:translateX(var(--spn-x));transition:transform .2s ease}
#topnav .spn-ls[aria-checked=true] .spn-ls-t{background:#1fa64a;box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
#topnav .spn-ls[aria-checked=true] .spn-ls-k{--spn-x:16px}
html[dir=rtl] #topnav .spn-ls-k{transform:translateX(calc(-1 * var(--spn-x)))}
#topnav .spn-ls[aria-checked=true]{color:#fff}
#topnav .spn-ls.spn-drag .spn-ls-k,#topnav .spn-ls.spn-drag .spn-ls-t{transition:none}
#topnav .spn-ls.spn-drag{cursor:grabbing}
#topnav .spn-ls.spn-drag .spn-ls-t{background:#5b6774}
#topnav .spn-ls.spn-drag.spn-half .spn-ls-t{background:#1fa64a}
#topnav .spn-ls-n{display:none}
#topnav .spn-ls:hover{color:#8fd3ff}
#topnav .spn-ls:hover .spn-ls-t{box-shadow:inset 0 0 0 1px #8fd3ff}
html body #topnav a.spn-ls:focus-visible{outline:3px solid #8fd3ff !important;outline-offset:1px}
#topnav .spn-main{display:flex;align-items:center;gap:.15rem}
#topnav .spn-dd{position:relative}
#topnav .spn-trig{appearance:none;background:transparent;border:0;border-radius:6px;color:#fff;font:700 15px/1 "Montserrat","Segoe UI",sans-serif;text-transform:uppercase;letter-spacing:.03em;min-height:44px;padding:0 .6rem;display:inline-flex;align-items:center;gap:.4rem;cursor:pointer;white-space:nowrap;transition:background-color .2s ease,color .2s ease}
#topnav .spn-chev{width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid currentColor;transition:transform .2s ease}
#topnav .spn-trig:hover{color:#8fd3ff}
#topnav a.spn-trig{text-decoration:none}
#topnav .spn-dd.is-current>.spn-trig{box-shadow:inset 0 -2px 0 #009cde}
#topnav .spn-dd.is-open>.spn-trig{background:#8fd3ff;color:#071018;box-shadow:none}
#topnav .spn-dd.is-open .spn-chev{transform:rotate(180deg)}
#topnav .spn-sub{position:absolute;top:100%;inset-inline-start:0;min-width:240px;margin-top:6px !important;padding:4px 0 !important;background:#0f1b26;border:1px solid rgba(255,255,255,.14);border-radius:10px;box-shadow:0 14px 34px rgba(0,0,0,.45);opacity:0;visibility:hidden;transform:translateY(-4px);transition:opacity .18s ease,transform .18s ease,visibility 0s linear .18s;z-index:5}
#topnav .spn-dd:nth-last-child(-n+3) .spn-sub{inset-inline-start:auto;inset-inline-end:0}
#topnav .spn-dd.is-open .spn-sub{opacity:1;visibility:visible;transform:none;transition:opacity .18s ease,transform .18s ease,visibility 0s}
#topnav .spn-sub li+li{border-top:1px solid rgba(255,255,255,.08)}
#topnav .spn-sub a{display:flex;align-items:center;min-height:44px;padding:0 1rem;color:#e8eef5;font-size:16px;font-weight:500;white-space:nowrap}
#topnav .spn-sub a:hover{background:rgba(0,156,222,.2);color:#fff}
#topnav .spn-sub a[aria-current]{color:#8fd3ff;font-weight:700}
#topnav .spn-cta{margin-inline-start:.6rem}
html body #topnav .spn-cta a{display:inline-flex;align-items:center;min-height:44px;padding:0 1.1rem !important;font:700 15px/1 "Montserrat","Segoe UI",sans-serif !important;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
#topnav a:focus-visible,#topnav button:focus-visible{outline:2px solid #8fd3ff !important;outline-offset:2px}
@media (pointer:coarse){#topnav .spn-util a,#topnav .spn-util a.spn-ls{min-height:44px}}
@media (min-width:1140px) and (max-width:1279px){#topnav .spn-trig{padding:0 .5rem;font-size:14px;letter-spacing:.02em}#topnav .spn-brand{font-size:1rem}html body #topnav .spn-cta a{padding:0 .8rem !important;font-size:14px !important}#topnav .spn-util{gap:0 .8rem;font-size:13px}}
@media (max-width:1139px){
 #topnav .spn{padding-top:6px;padding-bottom:6px}
 #topnav .spn-toggle{display:inline-flex;flex-direction:column;justify-content:center;align-items:center;gap:5px;width:44px;height:44px;padding:0;background:transparent;border:1px solid rgba(255,255,255,.6);border-radius:10px;cursor:pointer}
 #topnav .spn-toggle span{display:block;width:22px;height:2px;background:#fff;border-radius:2px;transition:transform .25s ease,opacity .2s ease}
 #topnav.spn-open .spn-toggle span:nth-child(1){transform:translateY(7px) rotate(45deg)}
 #topnav.spn-open .spn-toggle span:nth-child(2){opacity:0}
 #topnav.spn-open .spn-toggle span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
 #topnav .spn-panel{position:absolute;top:100%;left:0;right:0;align-items:stretch;padding:.5rem clamp(16px,4vw,32px) 1.2rem;background:#071018;box-shadow:0 14px 28px rgba(0,0,0,.4);max-height:calc(100vh - 60px);max-height:calc(100dvh - 60px);overflow-y:auto;overscroll-behavior:contain;opacity:0;visibility:hidden;transform:translateY(-10px);transition:opacity .22s ease,transform .22s ease,visibility 0s linear .22s}
 #topnav.spn-open .spn-panel{opacity:1;visibility:visible;transform:none;transition:opacity .22s ease,transform .22s ease,visibility 0s}
 #topnav .spn-util{flex-direction:column;align-items:stretch;font-size:17px;border-bottom:1px solid rgba(255,255,255,.12);padding-bottom:.4rem !important;margin-bottom:.3rem !important}
 #topnav .spn-util a{min-height:44px}
 #topnav .spn-lt{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.25rem .75rem;width:100%;padding:.25rem 0}
 #topnav .spn-util a.spn-ls{min-height:44px;font-size:17px;font-weight:600;letter-spacing:0;gap:.7rem;justify-content:flex-start}
 #topnav .spn-ls-c{display:none}
 #topnav .spn-ls-n{display:inline}
 #topnav .spn-main{flex-direction:column;align-items:stretch;gap:0}
 #topnav .spn-main>li+li{border-top:1px solid rgba(255,255,255,.08)}
 #topnav .spn-trig{width:100%;justify-content:space-between;min-height:48px;padding:0 .25rem;font-size:16px;border-radius:0}
 #topnav .spn-dd.is-current>.spn-trig{box-shadow:none;color:#8fd3ff}
 #topnav .spn-dd.is-open>.spn-trig{background:transparent;color:#8fd3ff}
 #topnav .spn-sub,#topnav .spn-dd:nth-last-child(-n+3) .spn-sub{position:static;display:none;min-width:0;margin:0 0 .5rem !important;padding:0 !important;background:rgba(255,255,255,.04);border:0;border-radius:8px;box-shadow:none;opacity:1;visibility:visible;transform:none;transition:none}
 #topnav .spn-dd.is-open .spn-sub{display:block}
 #topnav .spn-sub a{white-space:normal;padding:.4rem 1rem;font-size:17px}
 #topnav .spn-cta{margin:.8rem 0 0;border-top:0 !important}
 html body #topnav .spn-cta a{display:flex;justify-content:center;width:100%;min-height:48px;font-size:16px !important;box-sizing:border-box}
}
@media (prefers-reduced-motion:reduce){html body nav#topnav,#topnav *,#topnav::before{transition:none !important}}
@media (forced-colors:active){#topnav .spn-sub,#topnav .spn-panel{border:1px solid CanvasText}}
/* SPNAV:END */
"""
JS = r"""
/* SPNAV:START */
(function(){var n=document.getElementById('topnav');if(!n||!n.querySelector('.spn'))return;
var tg=n.querySelector('.spn-toggle'),mq=window.matchMedia('(min-width:1140px)'),hv=window.matchMedia('(hover:hover) and (pointer:fine)');
var dds=[].slice.call(n.querySelectorAll('.spn-dd'));
function set(li,o){li.classList.toggle('is-open',o);li.querySelector('.spn-trig').setAttribute('aria-expanded',o?'true':'false');if(!o)li.removeAttribute('data-hov')}
function closeAll(x){dds.forEach(function(li){if(li!==x)set(li,false)})}
function panel(o){n.classList.toggle('spn-open',o);if(tg){tg.setAttribute('aria-expanded',o?'true':'false');tg.setAttribute('aria-label',tg.getAttribute(o?'data-close':'data-open'))}if(!o)closeAll()}
dds.forEach(function(li){var b=li.querySelector('.spn-trig'),t;
 b.addEventListener('click',function(e){e.stopPropagation();var desk=mq.matches;
  if(b.tagName==='A'){var hov=desk&&hv.matches&&li.getAttribute('data-hov')==='1';if(li.classList.contains('is-open')&&(hov||li.getAttribute('data-hov')!=='1'))return;e.preventDefault();if(desk)closeAll(li);li.setAttribute('data-hov','2');set(li,true);return}
  if(desk&&hv.matches&&li.getAttribute('data-hov')==='1'){li.setAttribute('data-hov','2');set(li,true);return}
  var o=!li.classList.contains('is-open');if(desk)closeAll(li);set(li,o)});
 li.addEventListener('mouseenter',function(){if(!mq.matches||!hv.matches)return;clearTimeout(t);if(!li.classList.contains('is-open')){closeAll(li);set(li,true);li.setAttribute('data-hov','1')}});
 li.addEventListener('mouseleave',function(){if(!mq.matches||!hv.matches)return;t=setTimeout(function(){set(li,false)},200)});
 li.addEventListener('focusout',function(e){if(mq.matches&&e.relatedTarget&&!li.contains(e.relatedTarget))set(li,false)});
});
if(tg)tg.addEventListener('click',function(e){e.stopPropagation();panel(!n.classList.contains('spn-open'))});
document.addEventListener('click',function(e){if(!n.contains(e.target)){closeAll();if(n.classList.contains('spn-open'))panel(false)}});
document.addEventListener('keydown',function(e){if(e.key!=='Escape'&&e.key!=='Esc')return;var o=n.querySelector('.spn-dd.is-open');
 if(o){set(o,false);o.querySelector('.spn-trig').focus();return}if(n.classList.contains('spn-open')){panel(false);tg&&tg.focus()}});
var mqc=function(){panel(false)};if(mq.addEventListener)mq.addEventListener('change',mqc);else if(mq.addListener)mq.addListener(mqc);
var tk=false;function sc(){tk=false;n.classList.toggle('spn-solid',(window.pageYOffset||0)>24)}/* Oct 16 perf: pageYOffset needs no layout; first check after paint */
window.addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(sc)}},{passive:true});if(window.pageYOffset>24)requestAnimationFrame(sc);
/* Oct 16 (t886) language slide switches: tap, drag/swipe (pointer events), Space/Enter, arrow toward 'on'. One on at a time;
   turning one on goes to that language's version of this page, keeping ?query and #hash. RTL: on = thumb left (mirrored). */
var rtl=(document.documentElement.getAttribute('dir')||'').toLowerCase()==='rtl',rm=window.matchMedia('(prefers-reduced-motion: reduce)');
var lss=[].slice.call(n.querySelectorAll('.spn-ls'));
function lurl(a){return (a.getAttribute('data-href0')||a.getAttribute('href')).replace(/[?#].*$/,'')+location.search+location.hash}
function lgo(a){lss.forEach(function(x){x.setAttribute('aria-checked',x===a?'true':'false')});var u=lurl(a);setTimeout(function(){location.href=u},rm.matches?0:220)}
window.spnLang=function(c){var a=n.querySelector('.spn-ls[data-lang="'+c+'"]');if(!a||a.getAttribute('aria-current'))return false;lgo(a);return true};
lss.forEach(function(a,ix){var k=a.querySelector('.spn-ls-k'),st=null,moved=false,TR=16;
 function on(){return a.getAttribute('aria-checked')==='true'}
 a.addEventListener('pointerdown',function(e){if(e.button>0)return;moved=false;st={x:e.clientX,y:e.clientY,b:on()?TR:0,v:on()?TR:0,id:e.pointerId,act:false}});
 a.addEventListener('pointermove',function(e){if(!st||e.pointerId!==st.id)return;var dx=e.clientX-st.x,dy=e.clientY-st.y;
  if(!st.act){if(Math.abs(dx)<5)return;if(Math.abs(dy)>Math.abs(dx)){st=null;return}st.act=true;moved=true;a.classList.add('spn-drag');try{a.setPointerCapture(e.pointerId)}catch(_){}}
  var v=Math.max(0,Math.min(TR,st.b+(rtl?-dx:dx)));st.v=v;k.style.setProperty('--spn-x',v+'px');a.classList.toggle('spn-half',v>TR/2);e.preventDefault()});
 function end(e){if(!st)return;var s0=st;st=null;if(!s0.act)return;a.classList.remove('spn-drag','spn-half');k.style.removeProperty('--spn-x');
  if(e.type==='pointerup'&&s0.v>TR/2&&!on())lgo(a)}
 a.addEventListener('pointerup',end);a.addEventListener('pointercancel',end);a.addEventListener('dragstart',function(e){e.preventDefault()});
 a.addEventListener('click',function(e){if(moved){e.preventDefault();moved=false;return}if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();if(!on())lgo(a)});
 a.addEventListener('keydown',function(e){var K=e.key,fw=rtl?'ArrowLeft':'ArrowRight',bk=rtl?'ArrowRight':'ArrowLeft';
  if(K===' '||K==='Spacebar'||K===fw){e.preventDefault();if(!on())lgo(a)}else if(K===bk){e.preventDefault()}
  else if(K==='ArrowDown'||K==='ArrowUp'){e.preventDefault();var j=(ix+(K==='ArrowDown'?1:lss.length-1))%lss.length;lss[j].focus()}});
});
})();
/* SPNAV:END */
"""
def asset(path, txt):
    s = rd(path); s = re.sub(r'\n?/\* SPNAV:START \*/.*?/\* SPNAV:END \*/\n?', '', s, flags=re.S)
    wr(path, s.rstrip('\n') + '\n' + txt.strip('\n') + '\n')

def page_pass(p, l):
    s = rd(p); m = NAV_RE.search(s)
    if not m: return 0
    b = BRAND_RE.search(m.group(0))
    bh, bt = (b.group(1), b.group(2)) if b else ('index.html', 'Saving Planets')
    return wr(p, s[:m.start()] + nav(l, os.path.basename(p), bh, bt) + s[m.end():])

if __name__ == '__main__':
    n = 0
    for l in LANGS:
        for p in sorted(glob.glob(d(l) + '*.html')): n += page_pass(p, l)
    asset('styles.css', CSS); asset('site.js', JS)
    print(f'build-nav: {n} page writes')
