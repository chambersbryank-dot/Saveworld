#!/usr/bin/env python3
"""Build Solutions.html: every hub (alphabetical) with a card for each of its solutions.
Oct 18 (owner): the page's own search box is gone (site-wide search stays in the top nav). The top is an animated banner
(SI-rendered 4K Earth loop on R2, poster first, static under prefers-reduced-motion / Save-Data) with the title
'<live count> Real Solutions Making a Difference Daily' + 'Proof it's not too late'. The count = the cards on this page
(same number as the homepage counter and assets/data/solutions.json). Card photos are each page's own photo (build-og.py
source()), never the share card, which has the title baked in.
Hub membership = <h3><a href="Page.html"> card titles on each hub page (same rule as build-stats.js).
Card text comes only from each solution page: meta description + its "What" card. Image = og:image + its photo credit.
Also replaces the old Solutions dropdown in the top nav of every English page with a plain link to Solutions.html.
Idempotent. Run from repo root: python3 scripts/build-solutions-index.py  (weekly-sync.sh runs it before i18n-build)."""
import re, os, html, datetime
HUBS = [('Earth_Observation.html', 'Earth Observation'), ('Deforestation.html', 'Forests'), ('Lakes.html', 'Lakes'),
        ('Oceans.html', 'Ocean'), ('Planetary_Defense.html', 'Planetary Defense'), ('Polar.html', 'Polar'), ('Rivers.html', 'Rivers'),
        ('Space.html', 'Space'), ('Space_Disposal.html', 'Space Disposal'), ('Space_Weather.html', 'Space Weather'),
        ('Project-Rawane.html', 'Project Rawane')]  # Rawane last: lists only pages not under another hub
OUT = 'Solutions.html'
rd = lambda f: open(f, encoding='utf8').read()
un = html.unescape
esc = lambda s: html.escape(html.unescape(s), quote=True).replace('&#x27;', '&#x27;')

def m1(rx, s, d=''):
    m = re.search(rx, s, re.S); return m.group(1).strip() if m else d

import importlib.util, json
_og = importlib.util.spec_from_file_location('og', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-og.py'))
OG = importlib.util.module_from_spec(_og); _og.loader.exec_module(OG)
MAN = json.load(open('assets/data/media-manifest.json', encoding='utf8')) if os.path.exists('assets/data/media-manifest.json') else {}

_HP = dict(re.findall(r"\.hp-([A-Za-z0-9_-]+) \.page-hero\[class\]\{[^}]*?url\('([^']+)'\)", rd('styles.css')))
def hero_photo(s):
    """The page's hp- hero photo (same rule as build-ux.py hero_photo for the homepage cards)."""
    m = re.search(r'<body[^>]*class="[^"]*\bhp-([A-Za-z0-9_-]+)', s)
    ph = _HP.get(m.group(1)) if m else None
    return ph if ph and os.path.exists(ph) else None

def info(page):
    s = rd(page)
    img = m1(r'<meta property="og:image" content="https://www\.savingplanets\.com/([^"]+)"', s)
    if '/og/' in img.split('?')[0] or not img:  # Oct 18: share cards carry the page title (doubled, cropped on the card)
        s0 = re.sub(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->', '', s, flags=re.S)  # never another page's Related card photo
        src = hero_photo(s0) or OG.source(s0)
        if src == OG.LOGO or (src and ('/og/' in src or src.startswith('assets/hero/'))): src = None  # logo, a share card or the generic section hero
        img = src or img
    alt = ''
    if img:
        for a in re.findall(r'<img [^>]*src="' + re.escape(img) + r'"[^>]*>', s):
            v = m1(r'alt="([^"]*)"', a)
            if v and not re.match(r'(Learn more about|Support|Donate|Join)\b', v): alt = v; break
    if not alt: alt = html.unescape(m1(r'<meta property="og:image:alt" content="([^"]*)"', s))
    credit = m1(r'<p class="photo-credit">(.*?)</p>', s)
    if not credit and img:  # Oct 19: pages without a photo-credit line credit the photo next to it (SI span) or in data-image-credit
        q = re.escape(img)
        if re.search(r'<img [^>]*src="' + q + r'"[^>]*><span class="si-credit">', s): credit = 'Created by SI and Biological SI Partner'
        else: credit = m1(r'data-image="' + q + r'"[^>]*data-image-credit="([^"]+)"', s)
    desc = un(m1(r'<meta name="description" content="([^"]*)"', s))
    what = m1(r'<h3>What</h3><p>(.*?)</p>', s)
    what = re.sub(r'<span class="gl-pop"[^>]*>.*?</span></span>', '</span>', what, flags=re.S)  # Oct 15: drop glossary pop-up text ('radarA tool that...')
    what = un(re.sub(r'<[^>]+>', '', what))
    if desc.endswith('...'): desc = desc[:-3] + '…'
    if desc.endswith('…'):  # meta descriptions are clipped; keep whole sentences only
        ends = [m.start() for m in re.finditer(r'(?<!U\.S)(?<!\b[A-Z])\.\)? (?=[A-Z])', desc[:-1])]  # Oct 15: don't clip at 'U.S. '
        cut = ends[-1] if ends else -1
        desc = desc[:cut + 1].strip() if cut > 0 else ''
    sents = re.split(r'(?<!U\.S\.)(?<=[.!?])\s+(?=[A-Z])', what)
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

# Oct 19 (owner-approved Solutions cleanup): no photo on more than one card, one credit style, no '(Top)' / 'Read the 5 W's' links.
PHOTOS = json.load(open('assets/data/solutions-card-photos.json', encoding='utf8')) if os.path.exists('assets/data/solutions-card-photos.json') else {'keep': {}, 'photos': {}}
_AB = (json.load(open('assets/data/anim-banners.json', encoding='utf8')).get('images', {}) if os.path.exists('assets/data/anim-banners.json') else {})
CARD_SIZES = '(max-width:600px) 90vw, 260px'
CREDIT_TM = {'fr': 'Image :', 'es': 'Imagen:', 'ar': 'الصورة:', 'it': 'Immagine:', 'he': 'תמונה:'}  # the only translated word in a card credit
SI_CREDIT = 'Created by SI and Biological SI Partner'
_MON = r'(?:Jan|Feb|Mar|March|Apr|April|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?'
_ID = re.compile(r'^(?:PIA\d{5}|(?:iss|ISS|sts|STS|s|SL)\d[\w-]*|STS-\d+|(?:KSC|NHQ|GSFC|jsc|JSC|GRC|AFRC)[\w-]+|\d{4}-\d{3,5}|\d{6,})$')

def dhash(path):
    """Content fingerprint (64-bit difference hash) so one picture saved under two file names still counts as a repeat."""
    try:
        from PIL import Image
        im = Image.open(path).convert('L').resize((17, 16)); px = list(im.getdata())
        return tuple(px[r * 17 + c] > px[r * 17 + c + 1] for r in range(16) for c in range(16))
    except Exception: return None

def tidy_credit(raw, img):
    """One credit style for every card: 'Image:' + who made it + the source ID in brackets, no dates or captions. Keeps licence links
    and data notices (e.g. 'contains Copernicus Sentinel-1 data'). SI-made media keep the standard SI credit line."""
    if not raw and not img: return ''
    t = un(re.sub(r'<(?!/?a\b)[^>]+>', '', raw or '')).strip()
    if 'Created by SI' in t or 'Made from SI' in t: return SI_CREDIT
    ab = _AB.get(img or '') or {}
    if ab.get('credit') and (re.search(r'\d', ab['credit']) or os.path.splitext(os.path.basename(ab.get('r2', '')))[0] == os.path.splitext(os.path.basename(img or ''))[0]):
        t = ab['credit']  # banner credits were matched to the original by image content (Oct 18-19 banner batches)
    if not t: return ''
    t = re.sub(r'^(?:Image|Photo|Illustration|Images|Photos)\s*:\s*', '', t)
    if '<a ' in t:  # licence-linked credits: keep the attribution, drop the caption sentence after it
        t = re.split(r'(?<=\))\.\s|(?<=</a>)\.\s', t)[0].rstrip('. ')
        if 'Resized from the original' in (raw or ''): t = re.sub(r',?\s*Resized from the original\.?$', '', t).rstrip('., ') + ' (resized)'
        return re.sub(r',\s*(<a [^>]*>CC[^<]*</a>)', r' (\1', t).replace('</a> (resized)', '</a>, resized)') if re.search(r',\s*<a [^>]*>CC', t) else t
    ids = [x for x in re.split(r'[\s,();:]+', t) if _ID.match(x)]
    keep = [x.strip() for x in re.findall(r'\(([^()]*)\)', t) for x in x.split(',') if re.search(r'\bdata\b|\bCC[ -]BY|illustration|artist', x, re.I)]
    who = re.split(r'\s*\(|(?<!\b[A-Z])(?<!Univ)(?<!\bSt)\.\s+(?=[A-Z])|:\s|\.$', t)[0].strip().rstrip(',;: ')
    if who.endswith('.') and not re.search(r'(?:\b[A-Z]|Univ|\bSt)\.$', who): who = who[:-1]
    who = re.sub(r',\s*(?:via Wikimedia Commons|public domain).*$', '', who).strip()
    who = re.sub(r'\s*/\s*', '/', who)
    extra = list(dict.fromkeys([x for x in ids if x not in who] + [k for k in keep if k not in ids]))
    return who + (f' ({", ".join(extra)})' if extra else '')

def credit_html(c):
    if not c: return ''
    if c == SI_CREDIT: return f'<p class="photo-credit sol-credit">{SI_CREDIT}</p>'
    return f'<p class="photo-credit sol-credit"><span>Image:</span> <bdi>{c if "<a " in c else esc(c)}</bdi></p>'

def card_photo(href, i, owner_of):
    """(img_html, credit) for one card after the no-repeat rule."""
    new = PHOTOS['photos'].get(href)
    if i['img'] and owner_of.get(i['img'], href) == href and not new:
        return i['img'], i['alt'], None, tidy_credit(i['credit'], i['img'])
    if new:
        if new.get('r2'):
            e = MAN.get(new['r2'])
            if e and e.get('srcset'):
                ws = [x.rsplit(' ', 1) for x in e['srcset'].split(', ')]
                src = next((u for u, w in ws if w == '1280w'), ws[-1][0])
                h = round(e['height'] * 1280 / e['width']) if e['width'] > 1280 else e['height']
                return src, new['alt'], dict(srcset=e['srcset'], w=min(1280, e['width']), h=h), new['credit']
        elif new.get('src') and os.path.exists(new['src']):
            return new['src'], new['alt'], None, new.get('credit_html') or new.get('credit', '')
    return None, None, None, ''

def card(href, name, i, missing, also=(), owner_of=None):
    src, alt, r2, cred = card_photo(href, i, owner_of or {})
    if not src: missing.append(f'{href}: no image (photo repeated elsewhere or none on the page)')
    if not (i['desc'] or i['what']): missing.append(f'{href}: no description')
    alt = alt or f'{name} image'
    parts = [p for p in (i['desc'], i['what']) if p][:1]  # Oct 18 (owner cleanup): one short description per card, the full 5 W's are one tap away
    desc = ' '.join(f'<span>{esc(p)}</span>' for p in parts)
    extra = f' srcset="{r2["srcset"]}" sizes="{CARD_SIZES}" width="{r2["w"]}" height="{r2["h"]}"' if r2 else ''
    img = (f'<div class="image-container"><a class="photo-link" href="{href}"><img src="{src}"{extra} alt="{esc(alt)}" loading="lazy" decoding="async"></a></div>'
           + credit_html(cred)) if src else ''
    # Oct 19 (owner): 'Read the 5 W's' link removed; the title (and photo) open the solution page.
    return (f'<article class="card sol-card" data-url="{href}">{img}<h3><a href="{href}">{esc(name)}</a></h3>'
            f'<p class="sol-desc">{desc}</p>'
            + (('<p class="sol-also">Also in: ' + ', '.join(f'<a href="{f}">{esc(n)}</a>' for f, n in also) + '</p>') if also else '')
            + '</article>')

def owners(all_items):
    """Which card keeps each repeated photo: assets/data/solutions-card-photos.json 'keep', else the first card (A-Z by hub, then title)."""
    groups, fp = {}, {}
    for h, i in all_items:
        if not i['img'] or h in PHOTOS['photos']: continue
        k = i['img']
        if k not in fp: fp[k] = dhash(k.split('?')[0]) if os.path.exists(k.split('?')[0]) else None
        same = next((g for g in groups if g == k or (fp[k] and fp.get(g) and sum(a != b for a, b in zip(fp[k], fp[g])) <= 6)), k)
        groups.setdefault(same, []).append((h, k))
    own = {}
    for g, mem in groups.items():
        imgs = {k for _, k in mem}; pages = [h for h, _ in mem]
        keep = next((PHOTOS['keep'][k] for k in imgs if PHOTOS['keep'].get(k) in pages), pages[0])
        for k in imgs: own[k] = keep
    return own

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

BANNER_VID = [(w, f'videos/solutions-banner-earth-wide-{w}x{h}.mp4') for w, h in ((1280, 300), (1920, 450), (2560, 600), (3840, 900))]  # 90 s loop, one full turn
BANNER_POSTER = 'images/solutions-banner-earth-wide-poster-3840x900.png'
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sp_banner as SPB  # shared animated banner (same component as Top Ten)

import sol_flow as SF  # Oct 24 (owner-approved): flowing code-drawn banner + back-to-top links (scripts/sol_flow.py)

def banner(total):
    """Title banner. Oct 24 (owner): the Earth video loop is replaced by the SF flowing animation (space -> ocean -> land -> forest),
    title centred like the hub pages. (Oct 18 video/poster constants above are kept for build-top-ten.py history only.)"""
    return SF.banner(f'<span class="sol-n">{total}</span> <span class="sol-t">Real Solutions Making a Difference Daily</span>',
                     "Proof it's not too late", 'Created by SI and Biological SI Partner')

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
    INFO = {h: info(h) for _, _, items in hl for h, _ in items}
    OWN = owners([(h, INFO[h]) for _, _, items in hl for h, _ in items])
    for f, name, items in hl:
        sid = 'hub-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        jump.append(f'<li><a href="#{sid}">{esc(name)} <span class="sol-c">{len(items)}</span></a></li>')
        cards = ''.join(card(h, n, INFO[h], missing, also.get(h, []), OWN) for h, n in items); total += len(items)
        # Oct 24 (owner): a small 'Back to top' link closes each hub section (smooth scroll; instant under reduced motion).
        secs.append(f'<section class="card-band sol-hub" id="{sid}" data-hub="{f}"><h2><a href="{f}">{esc(name)}</a></h2><div class="grid">{cards}</div>{SF.toplink()}</section>')  # Oct 18 (owner cleanup): the long Hub Summary box after every hub is gone (the hub title links to the hub's 5 W's)
    desc = f'Proof it\'s not too late: {total} real, sourced solutions across {len(hl)} hubs, from ocean cleanups to Earth-observation satellites, making a difference daily.'
    title = f'{total} Real Solutions Making a Difference Daily'
    # head: retarget Contact -> Solutions
    h = head.replace('Contact.html', OUT)  # Oct 16: any Contact title (seo-meta override changed it)
    h = re.sub(r'<title>[^<]*</title>', lambda _m: f'<title>{title}</title>', h, count=1)
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', h)
    h = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*"', lambda m: m.group(1) + title + '"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    ld = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.savingplanets.com/index.html"}, {"@type": "ListItem", "position": 2, "name": "Solutions", "item": "https://www.savingplanets.com/Solutions.html"}]}</script>\n'
          '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "CollectionPage", "name": "' + title + '", "description": ' + '"' + desc.replace('"', '\\"') + '", "url": "https://www.savingplanets.com/Solutions.html", "inLanguage": "en", "datePublished": "2026-10-12", "dateModified": "2026-10-12", "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": "https://www.savingplanets.com/"}}</script>\n')
    h = h.replace('</head>', '<link rel="stylesheet" href="solutions.css?v=20261024c">\n' + ld + '</head>')
    nav = NAV_RE2.sub(NAV_LINK, NAV_RE.sub(NAV_LINK, nav)).replace(NAV_LINK, '<li class="nav-solutions"><a href="Solutions.html" aria-current="page">Solutions</a></li>')
    body_html = (f'<body class="toc-sub sol-page"><a class="skip-link" href="#directory">Skip to content</a>{nav}\n'
        + banner(total) + '\n'
        f'<main id="directory"><section class="sol-intro"><p class="sol-bluf">Every card is a real team doing hands-on work you can check: cleanups, restoration, satellites and missions, each with sources. Pick a hub below to start.</p><div class="sol-jump" role="navigation" aria-label="Hubs"><ul>{"".join(jump)}</ul></div></section>\n'
        + '\n'.join(secs) + '\n</main>\n'
        f'{footer}<script src="site.js?v={js_v}"></script>{SF.JS}</body></html>\n')
    page = h + body_html
    # Write only when the generated content changed, so later post-processing (seo-fix.py, add-gtag.py) is not undone
    # each run (which would leave the fr/es/ar copies permanently stale).
    import hashlib
    sig = hashlib.sha1(page.encode('utf8')).hexdigest()[:12]
    page = page.replace('<main id="directory">', f'<!-- SOL-BUILD {sig} --><main id="directory">', 1)
    if not (os.path.exists(OUT) and f'<!-- SOL-BUILD {sig} -->' in rd(OUT)):
        open(OUT, 'w', encoding='utf8').write(page)
    return hl, total, missing

def write_tm():
    """'Image:' is the only word in a card credit that changes with the language (who + ID stay as published)."""
    ch = 0
    for l, tr in CREDIT_TM.items():
        p = f'i18n/{l}.json'
        if not os.path.exists(p): continue
        T = json.load(open(p, encoding='utf8'))
        if T.get('Image:') != tr: T['Image:'] = tr; json.dump(T, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0); ch += 1
    return ch

if __name__ == '__main__':
    write_tm(); SF.write_tm(); SF.write_css()
    hl, total, missing = build()
    n = fix_nav()
    print(f'Solutions.html: {total} cards in {len(hl)} hubs ({", ".join(f"{x[1]} {len(x[2])}" for x in hl)}); nav updated on {n} pages')
    for m in missing: print('MISSING', m)
