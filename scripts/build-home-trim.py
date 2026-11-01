#!/usr/bin/env python3
"""Oct 20 2026 (founder-approved clutter fix #1): homepage from 18 sections to 6, all languages.

Visible order after the (locked, untouched) hero:
  1 Hero  2 Find a solution (search + Water/Land/Space hub chips + World Map)  3 Featured solutions (#solutions)
  4 For teachers & kids (AUDIENCE + EDU-LINKS)  5 New this week (+ links to the video and all updates)  6 Help + newsletter (#actions)
Nothing is deleted. Removed blocks are PARKED in an inert <template id="home-parked"> (not rendered, images/videos not loaded)
with their generator markers intact, so every earlier generator keeps updating them; this script re-applies the layout
on every run (idempotent). Moved content: stats strip, What the Stats Show and Planet Scoreboard (+ its Use this data
bar) -> Amazing_Facts.html (HOME-MOVED markers); promo video -> About.html#whats-new-video (already there);
mission + criteria -> About.html#criteria; Partner With Us -> About.html#partner / #cohost; Latest Updates -> Changelog.html;
Solution of the Week -> its own page (Life_Terra.html etc.); footer Hubs/Explore -> nav + Sitemap.html.
Rollback: delete this script's line in weekly-sync.sh and run with --undo (restores the parked blocks in original order).
"""
import re, sys, glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LANGS = ['', 'fr/', 'es/', 'ar/', 'it/', 'he/']
UNDO = '--undo' in sys.argv
T = {  # new UI strings (SI-translated; flagged for native review under the corrections policy)
 '':   ('Find a solution', 'Search', 'Search Saving Planets', 'Water', 'Land', 'Space'),
 'fr/':('Trouver une solution', 'Rechercher', 'Rechercher sur Saving Planets'),
 'es/':('Encontrar una solución', 'Buscar', 'Buscar en Saving Planets'),
 'ar/':('ابحث عن حل', 'بحث', 'ابحث في Saving Planets'),
 'it/':('Trova una soluzione', 'Cerca', 'Cerca su Saving Planets'),
 'he/':('מצאו פתרון', 'חיפוש', 'חיפוש ב-Saving Planets'),
}
CSS = """/* HOME-TRIM:START (Oct 20 clutter fix #1) */
.home-find{max-width:1100px;margin:2rem auto;padding:0 1rem;text-align:center}
.home-find form{display:flex;gap:.5rem;justify-content:center;max-width:640px;margin:1rem auto}
.home-find input{flex:1;min-width:0;padding:.75rem 1rem;border-radius:999px;border:1px solid #9fb3c8;font:inherit}
.home-find button{padding:.75rem 1.25rem;border-radius:999px;border:0;background:#0b3d91;color:#fff;font:inherit;font-weight:700;cursor:pointer}
.home-find{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:1rem;max-width:960px;margin:2rem auto .25rem}
.home-find>h2,.home-find>form,.home-find>.wm-cta{grid-column:1/-1}
.home-find>form{width:100%;margin:.5rem auto .25rem}
.home-find .hf-row{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;align-content:flex-start;margin:0;padding:1rem;border-radius:14px;border:1px solid rgba(127,160,200,.35);background:rgba(127,160,200,.08)}
.home-find .hf-row:nth-of-type(3){grid-column:1/-1}
.home-find .hf-lab{flex:0 0 100%;font-weight:800;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .35rem;padding-bottom:.45rem;border-bottom:1px solid rgba(127,160,200,.3)}
.home-find .dom-chip{min-height:44px;display:inline-flex;align-items:center}
.home-find>.wm-cta{margin:.5rem 0 0}
body.toc-home .home-find+#solutions.card-band,.home-find+#solutions.card-band{padding-top:1.25rem}
@media (max-width:640px){.home-find{grid-template-columns:1fr;gap:.75rem}.home-find .hf-row{padding:.85rem .6rem}}
.ns-more{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1rem}
.home-join .newsletter-band{margin-top:1.5rem}
.solution-list li.sol-more-li{margin-top:.6rem}
.solution-list a.sol-more{display:inline-flex;align-items:center;gap:.35rem;min-height:44px;padding:.35rem .9rem;border-radius:999px;border:1px dashed currentColor;font-size:.95rem}
.solution-list a.sol-more:focus-visible{outline:3px solid #0b3d91;outline-offset:2px}
.solution-list a.sol-more .sm-dots{font-weight:800}
/* HOME-TRIM:END */"""
rd = lambda f: open(f, encoding='utf-8').read()
def wr(f, s): open(f, 'w', encoding='utf-8').write(s)

def section_end(s, i):
    """index just past the </section> matching the <section at i"""
    d, j = 0, i
    while True:
        a, b = s.find('<section', j), s.find('</section>', j)
        if a != -1 and a < b: d += 1; j = a + 8
        else:
            d -= 1; j = b + 10
            if d == 0: return j

def marker(s, n):
    i = s.find(f'<!-- {n}:START -->'); j = s.find(f'<!-- {n}:END -->')
    return (i, j + len(f'<!-- {n}:END -->')) if i != -1 and j != -1 else None

def sec(s, pat):
    m = re.search(pat, s)
    return (m.start(), section_end(s, m.start())) if m else None

def grab(region):
    """split the region after the hero into known blocks (canonical original order)"""
    B = {}
    def take(name, span):
        nonlocal region
        if span: B[name] = region[span[0]:span[1]]; region = region[:span[0]] + region[span[1]:]
    take('vision', marker(region, 'VISION'))  # Oct 30: stays visible, directly under the hero (scripts/build-home-vision.py)
    take('impact', marker(region, 'IMPACT'))
    take('promo', marker(region, 'PROMO'))
    take('wmap', marker(region, 'WMAP-LINK'))
    take('domains', marker(region, 'DOMAINS'))
    take('audience', marker(region, 'AUDIENCE'))
    take('edulinks', marker(region, 'EDU-LINKS'))
    take('sotw', marker(region, 'SOTW'))
    p = re.search(r'<section (?=[^>]*id="partner-teaser")[^>]*>', region)
    if p:
        e = region.find('<!-- PARTNER-TEASER:END -->'); take('partner', (p.start(), e + len('<!-- PARTNER-TEASER:END -->')))
    take('scoreboard', marker(region, 'SCOREBOARD'))
    take('news', marker(region, 'NEWS'))
    take('solutions', sec(region, r'<section (?=[^>]*id="solutions")[^>]*>'))
    take('stats', sec(region, r'<section [^>]*class="impact-bar"'))
    take('newsletter', sec(region, r'<section (?=[^>]*id="newsletter")[^>]*>'))
    take('actions', sec(region, r'<section (?=[^>]*id="actions")[^>]*>'))
    take('mission', sec(region, r'<section [^>]*class="mission-block"'))
    take('homstd', marker(region, 'HOMESTD'))
    take('homenum', marker(region, 'HOMENUM'))
    return B, region

ORDER = ['vision', 'impact', 'promo', 'mission', 'wmap', 'domains', 'audience', 'edulinks', 'sotw', 'partner', 'solutions', 'stats', 'scoreboard', 'news', 'newsletter', 'actions']
PARK = ['impact', 'promo', 'mission', 'wmap', 'domains', 'sotw', 'partner', 'stats', 'scoreboard', 'news', 'newsletter', 'actions']
nomark = lambda h: re.sub(r'<!-- [A-Z0-9-]+:(?:START|END) -->', '', h)
txt = lambda h: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()

def find_section(L, B):
    t = T[L]; heads = re.findall(r'<h2 [^>]*id="dom-\w+"[^>]*>(.*?)</h2>', B.get('domains', ''))
    chips = re.findall(r'<div [^>]*class="dom-chips"[^>]*>(.*?)</div>', B.get('domains', ''), re.S)
    rows = ''.join(f'<p class="hf-row"><span class="hf-lab">{txt(h)}</span>{c}</p>' for h, c in zip(heads, chips))
    return ('<!-- HOME-FIND:START --><section class="home-find" aria-labelledby="hf-h">'
            f'<h2 id="hf-h">{t[0]}</h2><form role="search" action="Search.html" method="get">'
            f'<label for="hf-q" class="visually-hidden">{t[2]}</label><input id="hf-q" name="q" type="search" enterkeyhint="search">'
            f'<button type="submit">{t[1]}</button></form>{rows}{nomark(B.get("wmap", ""))}</section><!-- HOME-FIND:END -->')

# Oct 24 (founder-approved): promo videos are English-only, translated About pages have no video section.
# Translated homepages link to the English video and say so in their own language.
VID_EN = {'fr/': '(vidéo en anglais)', 'es/': '(video en inglés)', 'it/': '(video in inglese)',
          'ar/': '(فيديو بالإنجليزية)', 'he/': '(סרטון באנגלית)'}
def vid_link(L, label):
    if not L or L not in VID_EN: return f'<a class="btn-nav" href="About.html#whats-new-video">{label}</a>'
    return f'<a class="btn-nav" href="../About.html#whats-new-video" hreflang="en">{label} {VID_EN[L]}</a>'

def new_section(B, L=''):
    n = B.get('news', ''); m = re.search(r'<section [^>]*class="new-strip".*?</section>', n, re.S)
    if not m: return ''
    strip = m.group(0)
    vid = re.search(r'<h2 [^>]*id="promo-title"[^>]*>(.*?)</h2>', B.get('promo', ''), re.S)
    upd = re.search(r'<h2 [^>]*id="news-h"[^>]*>(.*?)</h2>', n, re.S)
    more = '<p class="ns-more">'
    if vid: more += vid_link(L, txt(vid.group(1)))
    if upd: more += f'<a class="btn-nav" href="Changelog.html">{txt(upd.group(1))}</a>'
    more += '</p>'
    return '<!-- HOME-NEW:START -->' + strip[:-len('</section>')] + more + '</section><!-- HOME-NEW:END -->'

def join_section(B):
    # Oct 31: "Be Part of the Fix" (the actions block) stays parked, not copied into the visible
    # homepage. Weekly sync was surfacing that join block as English churn and stalling i18n.
    # The newsletter signup stays visible (index.html#newsletter).
    nl = B.get('newsletter', '')
    nlin = re.sub(r'^<section[^>]*>|</section>$', '', nl).strip()
    if not nlin: return ''
    return ('<!-- HOME-JOIN:START --><section class="home-join" aria-label="Newsletter">'
            f'<div id="newsletter" class="newsletter-band" aria-label="Newsletter">{nlin}</div></section><!-- HOME-JOIN:END -->')

def strip_ours(region):
    for n in ['HOME-FIND', 'HOME-NEW', 'HOME-JOIN']:
        sp = marker(region, n)
        if sp: region = region[:sp[0]] + region[sp[1]:]
    # Attribute order differs after BeautifulSoup (id first on English, data-why first on translations).
    region = re.sub(r'<template\b[^>]*\bid="home-parked"[^>]*>(.*?)</template>', r'\1', region, flags=re.S)
    # Oct 31: "What makes us different" is not a homepage section. Drop it so it cannot stay visible as unknown content.
    region = re.sub(r'<!-- DIFF:START -->.*?<!-- DIFF:END -->', '', region, flags=re.S)
    region = re.sub(r'<section class="diff-strip"[^>]*>.*?</section>', '', region, flags=re.S)
    return region

def do_home(L):
    f = L + 'index.html'; s = rd(f)
    h = re.search(r'<section class="hero[ "]', s); he = section_end(s, h.start()); me = s.find('</main>', he)
    region = strip_ours(s[he:me])
    B, rest = grab(region)
    if UNDO:
        new = ''.join(B[k] for k in ORDER if k in B) + rest
    else:
        if txt(rest): print(f'  {f}: unknown content kept visible: {txt(rest)[:80]!r}')
        parked = '<template id="home-parked" data-why="Oct 20 clutter fix #1: parked, not deleted; see scripts/build-home-trim.py">' + \
                 ''.join(B[k] for k in ORDER if k in PARK and k in B) + '</template>'
        new = (B.get('vision', '') + parked + find_section(L, B) + B.get('solutions', '') + B.get('audience', '') + B.get('edulinks', '') +
               new_section(B, L) + join_section(B) + B.get('homstd', '') + B.get('homenum', '') + rest)
    s = s[:he] + new + s[me:]
    fm = marker(s, 'FOOTER-MAP')
    if fm and not UNDO: s = s[:fm[0]] + '<!-- FOOTER-MAP:START --><!-- FOOTER-MAP:END -->' + s[fm[1]:]
    wr(f, s)
    return B

def do_facts(L, B):
    f = L + 'Amazing_Facts.html'
    if not os.path.exists(f): return
    s = rd(f); sp = marker(s, 'HOME-MOVED')
    if sp: s = s[:sp[0]] + s[sp[1]:]
    if UNDO: wr(f, s); return
    # The homepage parked scoreboard keeps its APA/MLA cite + embed script (B is not modified).
    # Drop a second copy on Amazing Facts only when that page already has the handler.
    # Oct 31: never strip the script unless a copy remains, or Cite/Embed buttons do nothing.
    sb = nomark(B.get('scoreboard', ''))
    if 'function cites' in s:
        sb = re.sub(r'<script\b[^>]*>.*?</script>', '', sb, count=1, flags=re.S | re.I)
    sb = sb.replace('data-dt-url="https://www.savingplanets.com/"', f'data-dt-url="https://www.savingplanets.com/{L}Amazing_Facts.html#scoreboard"')
    blk = '<!-- HOME-MOVED:START -->' + nomark(B.get('impact', '')) + sb + '<!-- HOME-MOVED:END -->'
    st = sec(s, r'<section [^>]*class="impact-bar"')
    if not st: print('  no impact-bar on', f); return
    s = s[:st[1]] + blk + s[st[1]:]
    wr(f, s)

def css_and_stylev():
    c = rd('styles.css'); c = re.sub(r'/\* HOME-TRIM:START.*?HOME-TRIM:END \*/\n?', '', c, flags=re.S)
    if not UNDO: c = c.rstrip('\n') + '\n' + CSS + '\n'
    wr('styles.css', c)
    v = re.search(r'STYLEV = "([\w.-]+)"', rd('scripts/build-ux.py')).group(1)
    for f in glob.glob('*.html') + glob.glob('*/*.html'):
        s = rd(f); s2 = re.sub(r'styles\.css\?v=[\w.-]+', 'styles.css?v=' + v, s)
        s2 = re.sub(r'(?<![\w-])site\.js\?v=[\w.-]+', 'site.js?v=' + v, s2)
        if s2 != s: wr(f, s2)

# Oct 22 (founder): Featured solutions Space card was much longer than the others. Photo tip = its first sentence only;
# list = 4 items like the other cards (the rest stays in the Solutions menu and on the Space hub). All languages
# (hrefs are language-independent; the tip's first sentence is the existing translation's first sentence). Idempotent.
SPACE_DROP = ('Orbital_Data_Centers.html', 'Jupiter.html', 'MMX.html', 'Earth_Observation.html')
import json as _json
def SAT_CREDIT(L):
    x = 'NASA/JPL/Space Science Institute'  # PIA06193 credit line (science.nasa.gov/photojournal/the-greatest-saturn-portrait-yet/)
    if not L: return 'Image: ' + x
    return _json.load(open(f'i18n/{L[:-1]}.json', encoding='utf-8')).get('Image: {x}', 'Image: {x}').replace('{x}', x)
def trim_space_card(L):
    f = L + 'index.html'; s = rd(f)
    m = re.search(r'<article[^>]*id="space-card"', s)
    if not m: return
    i = m.start()
    j = s.find('</article>', i); c = s[i:j]; o = c
    c = re.sub(r'(<span class="photo-tip">)(.*?)(</span>)', lambda m: m.group(1) + re.split(r'(?<=[.!?؟])\s+', m.group(2).strip(), maxsplit=1)[0] + m.group(3), c, count=1, flags=re.S)
    # Oct 23 (founder): the Cassini photo is NASA's PIA06193, not SI-made: NASA credit instead of the SI tag
    c = re.sub(r'<span class="si-credit">[^<]*</span>', '', c)
    if 'class="photo-credit nasa-credit"' not in c:
        c = c.replace('</a></div><h3>', '</a></div>' + f'<p class="photo-credit nasa-credit">{SAT_CREDIT(L)}</p><h3>', 1)
    for h in SPACE_DROP: c = re.sub(r'<li><a href="(?:\.\./)?' + re.escape(h) + r'">[^<]*</a></li>', '', c)
    if c != o: wr(f, s[:i] + c + s[j:]); print(f'{f}: Space card trimmed')

# Oct 24 (founder-approved): after the last solution in each homepage hub card (Ocean, Lakes, Rivers, Forests, Space) a
# '... Click here to view the additional N' link to that hub's page. N = solutions in that hub on <lang>/Solutions.html
# (#hub-<id> sol-card data-url) minus the ones already listed in the card, so it stays right as solutions are added.
# Inside the <ul>, so it follows the last item in reading order in RTL too (ar/he). Idempotent (SOLMORE markers).
HUB_MORE = {'ocean-card': 'ocean', 'lakes-card': 'lakes', 'rivers-card': 'rivers', 'forests-card': 'forests', 'space-card': 'space'}
MORE_T = {  # (visible label, aria-label); SI-translated, flagged for native review under the corrections policy
 '':    ('Click here to view the additional {n}', 'View the additional {n} {hub} solutions'),
 'fr/': ('Cliquez ici pour voir les {n} supplémentaires', 'Voir les {n} solutions supplémentaires : {hub}'),
 'es/': ('Haz clic aquí para ver las {n} adicionales', 'Ver las {n} soluciones adicionales: {hub}'),
 'ar/': ('انقر هنا لعرض الـ{n} الإضافية', 'عرض الحلول الإضافية وعددها {n}: {hub}'),
 'it/': ('Clicca qui per vedere le altre {n}', 'Vedi le altre {n} soluzioni: {hub}'),
 'he/': ('לחצו כאן לצפייה ב-{n} הנוספים', 'צפייה ב-{n} הפתרונות הנוספים: {hub}'),
}
def hub_urls(L, hub):
    s = rd(L + 'Solutions.html'); i = s.find(f'id="hub-{hub}"')
    if i < 0: return set()
    j = s.find('id="hub-', i + 5); seg = s[i:j if j > 0 else len(s)]
    return set(re.findall(r'<article class="card sol-card[^"]*" data-url="([^"]+)"', seg))
HUB_MORE_COUNTS = {}
def hub_more(L):
    f = L + 'index.html'; s = rd(f); o = s
    s = re.sub(r'<!-- SOLMORE:START -->.*?<!-- SOLMORE:END -->', '', s, flags=re.S)
    for cid, hub in HUB_MORE.items():
        m = re.search(r'<article[^>]*id="' + cid + r'"[^>]*>.*?</article>', s, flags=re.S)
        if not m: continue
        c = m.group(0)
        h = re.search(r'<h3><a href="([^"]+)">([^<]+)</a></h3>', c)
        ul = re.search(r'<ul class="solution-list">(.*?)</ul>', c, flags=re.S)
        if not h or not ul: continue
        allu = hub_urls(L, hub)
        shown = {u.split('/')[-1] for u in re.findall(r'<a href="([^"]+)"', ul.group(1))}
        n = len(allu - shown)
        HUB_MORE_COUNTS.setdefault(hub, (len(allu & shown), n))
        if n <= 0: continue
        lab, aria = (x.replace('{n}', str(n)).replace('{hub}', h.group(2)) for x in MORE_T[L])
        li = (f'<!-- SOLMORE:START --><li class="sol-more-li"><a class="sol-more" href="{h.group(1)}" aria-label="{aria}">'
              f'<span class="sm-dots" aria-hidden="true">…</span> {lab}</a></li><!-- SOLMORE:END -->')
        c2 = c[:ul.end(1)] + li + c[ul.end(1):]
        s = s[:m.start()] + c2 + s[m.end():]
    if s != o: wr(f, s); print(f'{f}: hub "view the additional" links')

if '--hub-more-only' in sys.argv:
    for L in LANGS:
        if os.path.exists(L + 'index.html'): hub_more(L)
    print('counts (shown, remaining):', HUB_MORE_COUNTS)
    sys.exit(0)

for L in LANGS:
    if not os.path.exists(L + 'index.html'): continue
    B = do_home(L); do_facts(L, B)
    if not UNDO: trim_space_card(L); hub_more(L)
    print(f'{L or "en/"}index.html: {"restored" if UNDO else "6 sections"}; parked {len([k for k in PARK if k in B])} blocks')
css_and_stylev()
