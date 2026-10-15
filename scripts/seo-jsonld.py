#!/usr/bin/env python3
"""Structured data enrichment (Oct 13). Called at the end of seo-fix.run() for each language, so every build path
(weekly-sync, i18n-build) keeps it. Idempotent: rewrites existing JSON-LD blocks by @type; never adds a person's name.
- Solution pages: Article + author/publisher Organization 'Saving Planets', dateModified = Last reviewed
  (assets/data/reviewed.json), citation[] = the page's source links, isPartOf hub, about; BreadcrumbList localized.
- Hub pages: CollectionPage with hasPart (the hub's solutions).  Homepage: Organization (raster logo).
- Glossary: DefinedTermSet (+ hasDefinedTerm).  Teachers: CollectionPage whose mainEntity is a LearningResource.
Run standalone: python3 scripts/seo-jsonld.py [en fr es ar]"""
import json, os, re, sys, html, importlib.util
SITE = 'https://www.savingplanets.com/'
LOGO = SITE + 'assets/SavePlanetLogo.jpg'
ORG = {'@type': 'Organization', 'name': 'Saving Planets', 'url': 'https://www.savingplanets.com', 'logo': {'@type': 'ImageObject', 'url': LOGO}}
_ld = lambda f: (lambda s: (s.loader.exec_module(m := importlib.util.module_from_spec(s)), m)[1])(importlib.util.spec_from_file_location(f, f'scripts/{f}.py'))
sol = _ld('build-solutions-index'); ba = _ld('build-batch-a')
HL = sol.hubs(); HUB_OF, HUB_NAME, PARTS = {}, {}, {}
for f, name, items in HL:
    HUB_NAME[f] = name; PARTS[f] = [h for h, _ in items]
    for h, _ in items: HUB_OF.setdefault(h, f)
REVIEWED = json.load(open('assets/data/reviewed.json')) if os.path.exists('assets/data/reviewed.json') else {}
RX = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
un = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def blocks(s):
    out = []
    for m in RX.finditer(s.split('</head>')[0]):
        try: out.append(json.loads(m.group(1)))
        except Exception: pass
    return out

def write(s, objs):
    head, rest = s.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    if not head.endswith('\n'): head += '\n'
    head += ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>\n' for o in objs)
    return head + '</head>' + rest

def url(lang, page): return SITE + ('' if lang == 'en' else lang + '/') + page

def crumbs(s, lang, page):
    nav = re.search(r'<nav [^>]*class="breadcrumb"[^>]*>(.*?)</nav>', s, re.S)
    if not nav: return None
    items = []
    for li in re.findall(r'<li>(.*?)</li>', nav.group(1), re.S):
        a = re.search(r'href="([^"]+)"', li); n = un(li)
        href = a.group(1) if a else page
        href = os.path.basename(href.split('#')[0]) or 'index.html'
        items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': n, 'item': url(lang, href)})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items} if items else None

def enrich(p):
    lang = p.split('/')[0] if '/' in p else 'en'; page = os.path.basename(p)
    s = open(p, encoding='utf8').read(); objs = blocks(s)
    if not objs: return False
    by = {}
    for o in objs: by.setdefault(o.get('@type') if isinstance(o.get('@type'), str) else 'Multi', o)
    main = by.get('Article') or by.get('WebPage') or by.get('CollectionPage') or by.get('Multi')
    U = url(lang, page)
    bc = crumbs(s, lang, page)
    if bc: by['BreadcrumbList'] = bc
    if page in HUB_OF and main is not None:  # solution page
        a = {'@context': 'https://schema.org', '@type': 'Article', 'headline': main.get('headline') or main.get('name'), 'description': main.get('description'),
             'inLanguage': lang, 'url': U, 'mainEntityOfPage': {'@type': 'WebPage', '@id': U}}
        img = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        if img: a['image'] = img.group(1)
        pub = main.get('datePublished'); rv = REVIEWED.get(page, {}).get('date') or main.get('dateModified')
        if pub: a['datePublished'] = min(pub, rv) if rv else pub
        if rv: a['dateModified'] = rv
        a['author'] = ORG; a['publisher'] = ORG
        b = s.split('<body', 1)[-1]
        b = re.sub(r'<nav id="topnav">.*?</nav>|<footer>.*?</footer>|<section class="help-actions".*?</section>|<!-- (SHARE|RELATED|REVIEWED|CITE[A-Z-]*):START -->.*?<!-- \1:END -->|<section class="cite-box".*?</section>|<aside class="cite-box".*?</aside>', ' ', b, flags=re.S)
        cites = []
        for u in re.findall(r'href="(https?://[^"]+)"', b) + re.findall(r'data-source="(https?://[^"]+)"', b):
            u = html.unescape(u)
            if re.search(r'twitter\.com/intent|facebook\.com/sharer|linkedin\.com/sharing|donate|savingplanets\.com', u) or u in cites: continue
            cites.append(u)
        if cites: a['citation'] = [{'@type': 'CreativeWork', 'url': u} for u in cites]
        hub = HUB_OF[page]
        hub_name = un((re.search(r'<nav [^>]*class="breadcrumb"[^>]*>.*?<li>.*?</li>\s*<li>(.*?)</li>', s, re.S) or [None, HUB_NAME[hub]])[1]) if bc and len(bc['itemListElement']) >= 3 else HUB_NAME[hub]
        a['isPartOf'] = {'@type': 'CollectionPage', 'name': hub_name, 'url': url(lang, hub)}
        a['about'] = [{'@type': 'Thing', 'name': a['headline']}, {'@type': 'Thing', 'name': HUB_NAME[hub]}]
        by.pop('WebPage', None); by['Article'] = a
    elif page in PARTS and main is not None:  # hub page
        c = {k: v for k, v in main.items() if k not in ('headline', 'mainEntityOfPage', 'hasPart')}
        c['@type'] = 'CollectionPage'; c['name'] = main.get('name') or main.get('headline'); c['url'] = U; c['inLanguage'] = lang
        c['publisher'] = ORG
        c['hasPart'] = [{'@type': 'Article', 'url': url(lang, h), 'name': sol.NAME_CACHE.get(h, h) if hasattr(sol, 'NAME_CACHE') else h.replace('.html', '').replace('_', ' ')} for h in PARTS[page]]
        for k in ('Article', 'WebPage', 'Multi'): by.pop(k, None)
        by['CollectionPage'] = c
    elif page == 'index.html':
        by['Organization'] = {'@context': 'https://schema.org', **ORG, 'image': LOGO, 'email': 'hello@savingplanets.com'}
    elif page == 'Glossary.html' and main is not None:
        terms = [{'@type': 'DefinedTerm', 'name': un(dt), 'description': un(dd), 'url': U + '#' + i}
                 for i, dt, dd in re.findall(r'<dt id="([^"]+)">(.*?)</dt>\s*<dd>(.*?)</dd>', s, re.S)]
        g = {'@context': 'https://schema.org', '@type': 'DefinedTermSet', 'name': main.get('name'), 'description': main.get('description'), 'url': U, 'inLanguage': lang, 'hasDefinedTerm': terms}
        by['DefinedTermSet'] = g
    elif page == 'Teachers.html' and main is not None:
        t = {k: v for k, v in main.items() if k not in ('mainEntity',)}
        t['@type'] = 'CollectionPage'; t['inLanguage'] = lang; t['url'] = U; t['publisher'] = ORG
        t['mainEntity'] = {'@type': 'LearningResource', 'name': main.get('name'), 'description': main.get('description'), 'url': U, 'inLanguage': lang,
                           'learningResourceType': 'Worksheet', 'audience': {'@type': 'EducationalAudience', 'educationalRole': 'teacher'},
                           'isAccessibleForFree': True, 'publisher': ORG}
        for k in ('WebPage', 'CollectionPage', 'Multi'): by.pop(k, None)
        by['CollectionPage'] = t
    order = ['Organization', 'WebSite', 'BreadcrumbList', 'Article', 'CollectionPage', 'DefinedTermSet', 'WebPage', 'Multi']
    objs2 = [by[k] for k in order if k in by] + [v for k, v in by.items() if k not in order]
    out = write(s, objs2)
    if out != s: open(p, 'w', encoding='utf8').write(out); return True
    return False

NAMES = {h: n for _, _, items in HL for h, n in items}
sol.NAME_CACHE = NAMES

def run(langs):
    n = 0
    for l in langs:
        d = '.' if l == 'en' else l
        for f in sorted(os.listdir(d)):
            if f.endswith('.html') and not re.match(r'google[0-9a-f]+\.html$', f):
                n += enrich(f if l == 'en' else f'{l}/{f}')
    return n

if __name__ == '__main__':
    print('seo-jsonld: updated', run(sys.argv[1:] or ['en', 'fr', 'es', 'ar', 'it']), 'pages')
