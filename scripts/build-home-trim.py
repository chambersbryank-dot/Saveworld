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
.home-find .hf-row{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;align-items:center;margin:.5rem 0}
.home-find .hf-lab{font-weight:800;margin-inline-end:.25rem}
.home-find .dom-chip{min-height:44px;display:inline-flex;align-items:center}
.ns-more{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1rem}
.home-join .newsletter-band{margin-top:1.5rem}
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
    return B, region

ORDER = ['impact', 'promo', 'mission', 'wmap', 'domains', 'audience', 'edulinks', 'sotw', 'partner', 'solutions', 'stats', 'scoreboard', 'news', 'newsletter', 'actions']
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

def new_section(B):
    n = B.get('news', ''); m = re.search(r'<section [^>]*class="new-strip".*?</section>', n, re.S)
    if not m: return ''
    strip = m.group(0)
    vid = re.search(r'<h2 [^>]*id="promo-title"[^>]*>(.*?)</h2>', B.get('promo', ''), re.S)
    upd = re.search(r'<h2 [^>]*id="news-h"[^>]*>(.*?)</h2>', n, re.S)
    more = '<p class="ns-more">'
    if vid: more += f'<a class="btn-nav" href="About.html#whats-new-video">{txt(vid.group(1))}</a>'
    if upd: more += f'<a class="btn-nav" href="Changelog.html">{txt(upd.group(1))}</a>'
    more += '</p>'
    return '<!-- HOME-NEW:START -->' + strip[:-len('</section>')] + more + '</section><!-- HOME-NEW:END -->'

def join_section(B):
    a = B.get('actions', ''); nl = B.get('newsletter', '')
    inner = re.sub(r'^<section[^>]*>|</section>$', '', a)
    nlin = re.sub(r'^<section[^>]*>|</section>$', '', nl)
    return ('<!-- HOME-JOIN:START --><section id="actions" class="home-join">' + inner +
            f'<div id="newsletter" class="newsletter-band" aria-label="Newsletter">{nlin}</div></section><!-- HOME-JOIN:END -->')

def strip_ours(region):
    for n in ['HOME-FIND', 'HOME-NEW', 'HOME-JOIN']:
        sp = marker(region, n)
        if sp: region = region[:sp[0]] + region[sp[1]:]
    m = re.search(r'<template id="home-parked"[^>]*>(.*?)</template>', region, re.S)
    if m: region = region[:m.start()] + m.group(1) + region[m.end():]
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
        new = (parked + find_section(L, B) + B.get('solutions', '') + B.get('audience', '') + B.get('edulinks', '') +
               new_section(B) + join_section(B) + rest)
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
    sb = nomark(B.get('scoreboard', '')); sb = re.sub(r'<script>.*?</script>', '', sb, flags=re.S)
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

for L in LANGS:
    if not os.path.exists(L + 'index.html'): continue
    B = do_home(L); do_facts(L, B)
    print(f'{L or "en/"}index.html: {"restored" if UNDO else "6 sections"}; parked {len([k for k in PARK if k in B])} blocks')
css_and_stylev()
