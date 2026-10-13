#!/usr/bin/env python3
"""Build Solutions.html: every hub (alphabetical) with a card for each of its solutions, plus an on-page
search that filters the cards (instant keyword match, then semantic re-rank via /search/semantic.js).
Hub membership = <h3><a href="Page.html"> card titles on each hub page (same rule as build-stats.js).
Card text comes only from each solution page: meta description + its "What" card. Image = og:image + its photo credit.
Also replaces the old Solutions dropdown in the top nav of every English page with a plain link to Solutions.html.
Idempotent. Run from repo root: python3 scripts/build-solutions-index.py  (weekly-sync.sh runs it before i18n-build)."""
import re, os, html, datetime
HUBS = [('Earth_Observation.html', 'Earth Observation'), ('Deforestation.html', 'Forests'), ('Lakes.html', 'Lakes'),
        ('Oceans.html', 'Ocean'), ('Planetary_Defense.html', 'Planetary Defense'), ('Rivers.html', 'Rivers'),
        ('Space.html', 'Space'), ('Space_Disposal.html', 'Space Disposal'), ('Space_Weather.html', 'Space Weather'),
        ('Project-Rawane.html', 'Project Rawane')]  # Rawane last: lists only pages not under another hub
OUT = 'Solutions.html'
rd = lambda f: open(f, encoding='utf8').read()
un = html.unescape
esc = lambda s: html.escape(s, quote=True).replace('&#x27;', '&#x27;')

def m1(rx, s, d=''):
    m = re.search(rx, s, re.S); return m.group(1).strip() if m else d

def info(page):
    s = rd(page)
    img = m1(r'<meta property="og:image" content="https://www\.savingplanets\.com/([^"]+)"', s)
    alt = ''
    if img:
        for a in re.findall(r'<img [^>]*src="' + re.escape(img) + r'"[^>]*>', s):
            v = m1(r'alt="([^"]*)"', a)
            if v and not re.match(r'(Learn more about|Support|Donate|Join)\b', v): alt = v; break
    if not alt: alt = html.unescape(m1(r'<meta property="og:image:alt" content="([^"]*)"', s))
    credit = m1(r'<p class="photo-credit">(.*?)</p>', s)
    desc = un(m1(r'<meta name="description" content="([^"]*)"', s))
    what = m1(r'<h3>What</h3><p>(.*?)</p>', s)
    what = un(re.sub(r'<[^>]+>', '', what))
    if desc.endswith('...'): desc = desc[:-3] + '…'
    if desc.endswith('…'):  # meta descriptions are clipped; keep whole sentences only
        cut = max(desc.rfind('. ', 0, len(desc) - 1), desc.rfind('.) ', 0, len(desc) - 1))
        desc = desc[:cut + 1].strip() if cut > 0 else ''
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z])', what)
    what = ' '.join(sents[:2])
    return dict(img=img, alt=alt, credit=credit, desc=desc, what=what)

def hubs():
    listed, out = set(), []
    for f, name in HUBS:
        if not os.path.exists(f): continue
        seen = set(listed) if f == 'Project-Rawane.html' else set(); items = []
        for href, t in re.findall(r'<h3><a href="([A-Za-z0-9_.-]+\.html)">([^<]+)</a>', rd(f)):
            if href == f or href in seen or not os.path.exists(href): continue
            seen.add(href); listed.add(href)
            items.append((href, un(re.sub(r'^(Saving Moons|Natural Debris Solution): ', '', t))))
        items.sort(key=lambda x: x[1].lower())
        out.append((f, name, items))
    return sorted(out, key=lambda h: h[1].lower())

def hub_summary(f, name):
    """Synopsis + impact taken only from the hub page itself (Five W's What/Why, first Impact Statement paragraph)."""
    s = rd(f)
    what, why = m1(r'<h3>What</h3><p>(.*?)</p>', s), m1(r'<h3>Why</h3><p>(.*?)</p>', s)
    imp = ''
    sec = m1(r'(<section[^>]*id="(?:saves|impact)"[^>]*>.*?</section>)', s)
    for cls, txt in re.findall(r'<p( class="[^"]*")?>(.*?)</p>', sec, re.S):
        plain = re.sub(r'<[^>]+>', '', txt)
        if 'fact-source' in cls or 'hub-label' in cls or 'inline-link' in txt or plain.startswith(('Source', 'Organization source', 'Company source')) or len(plain) < 40: continue
        imp = txt.strip(); break
    if not imp: imp = esc(un(m1(r'<meta name="description" content="([^"]*)"', s)))
    syn = ''.join(f'<p>{x}</p>' for x in (what, why) if x)
    return ('<div class="sol-hub-summary"><h3>Hub Summary</h3>' + syn +
            f'<p class="sol-impact"><strong>Impact:</strong> {imp}</p>'
            f'<p class="sol-hub-links"><a href="{f}">Read the hub&#x27;s 5 W&#x27;s</a> <span aria-hidden="true">·</span> <a href="Ways_to_Help.html">More: Ways to Help</a></p></div>')

def card(href, name, i, missing, also=()):
    if not i['img']: missing.append(f'{href}: no image')
    if not (i['desc'] or i['what']): missing.append(f'{href}: no description')
    alt = i['alt'] or f'{name} image'
    parts = [p for p in (i['desc'], i['what']) if p]
    if len(parts) == 2 and parts[1].lower() in parts[0].lower(): parts = parts[:1]
    desc = ' '.join(f'<span>{esc(p)}</span>' for p in parts)
    img = (f'<div class="image-container"><a class="photo-link" href="{href}"><img src="{i["img"]}" alt="{esc(alt)}" loading="lazy" decoding="async"></a></div>'
           + (f'<p class="photo-credit">{i["credit"]}</p>' if i['credit'] else '')) if i['img'] else ''
    return (f'<article class="card sol-card" data-url="{href}">{img}<h3><a href="{href}">{esc(name)}</a></h3>'
            f'<p class="sol-desc">{desc}</p>'
            + (('<p class="sol-also">Also in: ' + ', '.join(f'<a href="{f}">{esc(n)}</a>' for f, n in also) + '</p>') if also else '')
            + f'<p class="sol-more"><a href="{href}">Read the 5 W&#x27;s</a></p></article>')

NAV_RE = re.compile(r'<li class="nav-dropdown"><a [^>]*class="dropdown-toggle"[^>]*>Solutions</a><ul class="dropdown-menu solutions-menu">[\s\S]*?<!-- SOLUTIONS-MENU:END --></ul></li>')
NAV_RE2 = re.compile(r'<li class="nav-dropdown"><a class="dropdown-toggle" href="[^"]*">Solutions</a><ul class="dropdown-menu solutions-menu">[\s\S]*?<!-- SOLUTIONS-MENU:END --></ul></li>')
NAV_LINK = '<li class="nav-solutions"><a href="Solutions.html">Solutions</a></li>'

def fix_nav():
    n = 0
    for f in sorted(os.listdir('.')):
        if not f.endswith('.html'): continue
        s = rd(f); t = NAV_RE2.sub(NAV_LINK, NAV_RE.sub(NAV_LINK, s))
        if t != s: open(f, 'w', encoding='utf8').write(t); n += 1
    return n

def build():
    tpl = rd('Contact.html')
    head, body = tpl.split('<body', 1)
    nav = m1(r'(<nav id="topnav">.*?</nav>)', body)
    footer = m1(r'(<footer>.*?</footer>)', body)
    footer = re.sub(r'<script[^>]*></script>', '', footer)
    js_v = m1(r'site\.js\?v=([0-9a-z]+)', body, '1')
    missing, secs, jump, total = [], [], [], 0
    hl = hubs()
    # Each solution is listed once, under its primary hub (the hub in its breadcrumb; else the first hub listing it).
    where = {}
    for f, name, items in hl:
        for h, n in items: where.setdefault(h, []).append((f, name))
    primary = {}
    for h, hs in where.items():
        bc = re.findall(r'<nav aria-label="Breadcrumb"[^>]*>.*?</nav>', rd(h), re.S)
        bc_hubs = re.findall(r'href="([A-Za-z0-9_.-]+\.html)"', bc[0]) if bc else []
        primary[h] = next((x for x in hs if x[0] in bc_hubs), hs[0])
    also = {h: [x for x in hs if x != primary[h]] for h, hs in where.items()}
    hl = [(f, name, [(h, n) for h, n in items if primary[h][0] == f]) for f, name, items in hl]
    for f, name, items in hl:
        sid = 'hub-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        jump.append(f'<li><a href="#{sid}">{esc(name)}</a></li>')
        cards = ''.join(card(h, n, info(h), missing, also.get(h, [])) for h, n in items); total += len(items)
        secs.append(f'<section class="card-band sol-hub" id="{sid}" data-hub="{f}"><h2><a href="{f}">{esc(name)}</a> <a class="sol-top" href="#top">(Top)</a></h2><div class="grid">{cards}</div>{hub_summary(f, name)}</section>')
    desc = f'Every Saving Planets solution in one place: {total} sourced solutions across {len(hl)} hubs, from ocean cleanups to Earth-observation satellites.'
    # head: retarget Contact -> Solutions
    h = head.replace('Contact.html', OUT).replace('<title>Contact | Saving Planets</title>', '<title>Saving Planets Solutions | Saving Planets</title>')
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', h)
    h = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*"', r'\1Saving Planets Solutions | Saving Planets"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    ld = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.savingplanets.com/index.html"}, {"@type": "ListItem", "position": 2, "name": "Solutions", "item": "https://www.savingplanets.com/Solutions.html"}]}</script>\n'
          '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Saving Planets Solutions", "description": ' + '"' + desc.replace('"', '\\"') + '", "url": "https://www.savingplanets.com/Solutions.html", "inLanguage": "en", "datePublished": "2026-10-12", "dateModified": "2026-10-12", "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": "https://www.savingplanets.com/"}}</script>\n')
    h = h.replace('</head>', '<link rel="stylesheet" href="solutions.css?v=20261013a">\n' + ld + '</head>')
    nav = NAV_RE2.sub(NAV_LINK, NAV_RE.sub(NAV_LINK, nav)).replace(NAV_LINK, '<li class="nav-solutions"><a href="Solutions.html" aria-current="page">Solutions</a></li>')
    chips = ''.join(f'<button type="button" class="sol-chip">{c}</button>' for c in
                    ['ways to clean a river near me', 'how space tech helps farmers', 'protecting coasts from storms', 'junk satellites crowding orbit'])
    body_html = (f'<body class="toc-sub sol-page"><a class="skip-link" href="#directory">Skip to content</a>{nav}\n'
        '<section class="page-hero sol-hero" id="top"><div class="page-hero-content"><p class="sol-hero-title" data-pagefind-ignore>Search Saving Planets</p>'
        '<form class="sol-search-form" role="search" action="Solutions.html" onsubmit="return false"><label class="visually-hidden" for="sol-q">Search solutions</label>'
        '<input id="sol-q" name="q" type="search" autocomplete="off" placeholder="Try: protecting coasts from storms" aria-describedby="sol-status"></form>'
        '<p id="sol-status" class="sol-status" aria-live="polite"></p></div></section>\n'
        f'<main id="directory"><section class="sol-intro"><h1>Saving Planets Solutions</h1><div class="sol-jump" role="navigation" aria-label="Hubs"><ul>{"".join(jump)}</ul></div></section>\n'
        f'<section class="sol-empty" hidden><p>No matching solutions yet. Try one of these:</p><div class="sol-chips">{chips}</div></section>\n'
        + '\n'.join(secs) + '\n</main>\n'
        f'{footer}<script src="site.js?v={js_v}"></script><script type="module" src="solutions.js?v=20261012a"></script></body></html>\n')
    page = h + body_html
    # Write only when the generated content changed, so later post-processing (seo-fix.py, add-gtag.py) is not undone
    # each run (which would leave the fr/es/ar copies permanently stale).
    import hashlib
    sig = hashlib.sha1(page.encode('utf8')).hexdigest()[:12]
    page = page.replace('<main id="directory">', f'<!-- SOL-BUILD {sig} --><main id="directory">', 1)
    if not (os.path.exists(OUT) and f'<!-- SOL-BUILD {sig} -->' in rd(OUT)):
        open(OUT, 'w', encoding='utf8').write(page)
    return hl, total, missing

if __name__ == '__main__':
    hl, total, missing = build()
    n = fix_nav()
    print(f'Solutions.html: {total} cards in {len(hl)} hubs ({", ".join(f"{x[1]} {len(x[2])}" for x in hl)}); nav updated on {n} pages')
    for m in missing: print('MISSING', m)
