#!/usr/bin/env python3
"""Structured data enrichment (Oct 13). Called at the end of seo-fix.run() for each language, so every build path
(weekly-sync, i18n-build) keeps it. Idempotent: rewrites existing JSON-LD blocks by @type; never adds a person's name.
- Solution pages: Article + author/publisher Organization 'Saving Planets', dateModified = Last reviewed
  (assets/data/reviewed.json), citation[] = the page's source links, isPartOf hub, about; BreadcrumbList localized.
- Hub pages: CollectionPage with hasPart (the hub's solutions).  Homepage: Organization (raster logo).
- Glossary: DefinedTermSet (+ hasDefinedTerm).  Teachers: CollectionPage whose mainEntity is a LearningResource.
- Oct 16 SEO pass: every indexable page carries WebSite (+ SearchAction -> Search.html?q=) and Organization nodes linked by
  @id; pages without a visible breadcrumb get a BreadcrumbList (Home > section hub > page, names in the page language);
  Myth_vs_Fact gets FAQPage built only from the visible myth cards; LearningResource gets educationalLevel from the
  visible level chips (.lchip) and publisher/dates; several blocks of one @type are kept (no silent drops).
Run standalone: python3 scripts/seo-jsonld.py [en fr es ar it]"""
import json, os, re, sys, html, importlib.util
SITE = 'https://www.savingplanets.com/'
LOGO = SITE + 'assets/SavePlanetLogo.jpg'
ORG = {'@type': 'Organization', 'name': 'Saving Planets', 'url': 'https://www.savingplanets.com', 'logo': {'@type': 'ImageObject', 'url': LOGO}}
ORG_ID, SITE_ID = SITE + '#organization', SITE + '#website'
ORG_REF = {'@id': ORG_ID}
ORG_FULL = dict(ORG, **{'@id': ORG_ID})  # Article author/publisher: full node, since stricter validators don't resolve @id references
SAME_AS = ['https://x.com/SISavingPlanets']
SITENAME = 'Saving Planets'
NOINDEX = {'Project-R.html', '404.html'}
# Section hub for pages that have no visible breadcrumb (BreadcrumbList = Home > hub > page)
SECTION = {}
for _f in ('Orbits_Guide', 'Orbit_Math', 'Orbit_Lab', 'Aero_Guide', 'Aero_Math', 'Aero_Lab', 'Physics_Guide', 'Physics_Math', 'Physics_Lab',
           'AP_IB_Physics', 'Cadets', 'Careers', 'Homeschool', 'Calculators', 'Glossary', 'Satellite_Explorer', 'Lesson_Builder', 'SI_Helper'):
    SECTION[_f + '.html'] = 'Learn.html'
for _f in ('Kids_Map', 'Spot_the_Fire'): SECTION[_f + '.html'] = 'Play_and_Learn.html'
def website(lang):
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE_ID, 'name': SITENAME, 'url': SITE, 'inLanguage': lang, 'publisher': ORG_REF,
            'potentialAction': {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + ('' if lang == 'en' else lang + '/') + 'Search.html?q={search_term_string}'},
                                'query-input': 'required name=search_term_string'}}
def org_node(full=False):
    o = {'@context': 'https://schema.org', '@id': ORG_ID, **ORG, 'sameAs': SAME_AS}
    if full: o.update({'image': LOGO, 'email': 'hello@savingplanets.com'})
    return o
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

HOME_NAME = {'en': 'Home', 'fr': 'Accueil', 'es': 'Inicio', 'ar': 'الرئيسية', 'it': 'Home', 'he': 'דף הבית'}
def page_name(lang, page):
    """Visible name of a page in that language: its <h1>, else its <title> without the brand."""
    f = page if lang == 'en' else f'{lang}/{page}'
    if not os.path.exists(f): return None
    s = open(f, encoding='utf8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S) or re.search(r'<title>(.*?)</title>', s, re.S)
    return re.sub(r'\s*[|·]\s*(Saving Planets|Français|Español|بالعربية|Italiano|עברית)\s*$', '', un(m.group(1))).strip() if m else None

def fallback_crumbs(s, lang, page):
    """Home > (section hub) > page, for pages without a visible breadcrumb nav."""
    items = [(HOME_NAME[lang], SITE + ('' if lang == 'en' else lang + '/'))]
    hub = SECTION.get(page) or HUB_OF.get(page) or ('Calculators.html' if page.endswith('_Calculator.html') else None)
    if hub and hub != page and page_name(lang, hub): items.append((page_name(lang, hub), url(lang, hub)))
    items.append((page_name(lang, page) or page[:-5].replace('_', ' '), url(lang, page)))
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}

def faq(s, lang, page):
    """FAQPage from the visible myth cards: question = the myth as printed (h2), answer = the fact + honest note."""
    qs = []
    for card in re.findall(r'<article class="myth-card" id="[^"]+">(.*?)</article>', s, re.S):
        h = re.search(r'<h2[^>]*>(.*?)</h2>', card, re.S)
        ps = re.findall(r'<p(?: class="(myth-honest)")?>(.*?)</p>', card.split('class="myth-source"')[0], re.S)
        ans = ' '.join(un(t) for c, t in ps if t and 'myth-tag' not in t)
        if h and ans: qs.append({'@type': 'Question', 'name': un(h.group(1)), 'acceptedAnswer': {'@type': 'Answer', 'text': ans}})
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'url': url(lang, page), 'inLanguage': lang, 'mainEntity': qs} if qs else None

def crumbs(s, lang, page):
    nav = re.search(r'<nav [^>]*class="breadcrumb"[^>]*>(.*?)</nav>', s, re.S)
    if not nav: return None
    items = []
    for li in re.findall(r'<li>(.*?)</li>', nav.group(1), re.S):
        a = re.search(r'href="([^"]+)"', li); n = un(li)
        href = a.group(1) if a else page
        href = os.path.basename(href.split('#')[0]) or 'index.html'
        items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': n, 'item': url(lang, href).replace('/index.html', '/')})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items} if items else None

def enrich(p):
    lang = p.split('/')[0] if '/' in p else 'en'; page = os.path.basename(p)
    s = open(p, encoding='utf8').read(); objs = blocks(s)
    by = {}; dup = []
    for o in objs:
        k = o.get('@type') if isinstance(o.get('@type'), str) else 'Multi'
        if k in by and k not in ('WebSite', 'Organization', 'BreadcrumbList', 'FAQPage'): dup.append(o)
        else: by.setdefault(k, o)
    main = by.get('Article') or by.get('WebPage') or by.get('CollectionPage') or by.get('Multi')
    U = url(lang, page)
    if page in NOINDEX or 'http-equiv="refresh"' in s: return False
    bc = crumbs(s, lang, page)
    if bc: by['BreadcrumbList'] = bc
    elif page != 'index.html': by['BreadcrumbList'] = fallback_crumbs(s, lang, page)
    by['WebSite'] = website(lang)
    by['Organization'] = org_node(page == 'index.html')
    if page == 'Myth_vs_Fact.html':
        fq = faq(s, lang, page)
        if fq: by['FAQPage'] = fq
    lr = by.get('LearningResource')
    if lr is not None:
        lv = []
        for c in re.findall(r'<li class="lchip">(.*?)</li>', s): c = un(c); lv.append(c) if c and c not in lv else None
        if lv and not lr.get('educationalLevel'): lr['educationalLevel'] = lv if len(lv) > 1 else lv[0]
        lr.setdefault('publisher', ORG_REF)
        if main is None: main = lr
    if page in HUB_OF and main is not None:  # solution page
        a = {'@context': 'https://schema.org', '@type': 'Article', 'headline': main.get('headline') or main.get('name'), 'description': main.get('description'),
             'inLanguage': lang, 'url': U, 'mainEntityOfPage': {'@type': 'WebPage', '@id': U}}
        img = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        if img: a['image'] = img.group(1)
        pub = main.get('datePublished'); rv = REVIEWED.get(page, {}).get('date') or main.get('dateModified')
        if pub: a['datePublished'] = min(pub, rv) if rv else pub
        if rv: a['dateModified'] = rv
        a['author'] = ORG_FULL; a['publisher'] = ORG_FULL
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
        c['publisher'] = ORG_REF
        c['hasPart'] = [{'@type': 'WebPage', 'url': url(lang, h), 'name': sol.NAME_CACHE.get(h, h) if hasattr(sol, 'NAME_CACHE') else h.replace('.html', '').replace('_', ' ')} for h in PARTS[page]]
        for k in ('Article', 'WebPage', 'Multi'): by.pop(k, None)
        by['CollectionPage'] = c
    elif page == 'index.html':
        pass  # full Organization node added above
    elif page == 'Glossary.html' and main is not None:
        terms = [{'@type': 'DefinedTerm', 'name': un(dt), 'description': un(dd), 'url': U + '#' + i}
                 for i, dt, dd in re.findall(r'<dt id="([^"]+)">(.*?)</dt>\s*<dd>(.*?)</dd>', s, re.S)]
        g = {'@context': 'https://schema.org', '@type': 'DefinedTermSet', 'name': main.get('name'), 'description': main.get('description'), 'url': U, 'inLanguage': lang, 'hasDefinedTerm': terms}
        by['DefinedTermSet'] = g
    elif page == 'Teachers.html' and main is not None:
        t = {k: v for k, v in main.items() if k not in ('mainEntity',)}
        t['@type'] = 'CollectionPage'; t['inLanguage'] = lang; t['url'] = U; t['publisher'] = ORG_REF
        t['mainEntity'] = {'@type': 'LearningResource', 'name': main.get('name'), 'description': main.get('description'), 'url': U, 'inLanguage': lang,
                           'learningResourceType': 'Worksheet', 'audience': {'@type': 'EducationalAudience', 'educationalRole': 'teacher'},
                           'isAccessibleForFree': True, 'publisher': ORG_REF}
        for k in ('WebPage', 'CollectionPage', 'Multi'): by.pop(k, None)
        by['CollectionPage'] = t
    me = main.get('mainEntity') if isinstance(main, dict) else None
    if isinstance(me, dict) and me.get('@type') == 'LearningResource' and lang != 'en':  # nested copy in the page language (was English)
        me['name'] = main.get('name') or me.get('name'); me['description'] = main.get('description') or me.get('description'); me['inLanguage'] = lang
        me['url'] = U
    for o in by.values():  # replace stale inline publisher/author copies with the shared @id
        for k in ('publisher', 'author'):
            if isinstance(o.get(k), dict) and o[k].get('@type') == 'Organization' and o[k].get('name') == SITENAME and o.get('@type') != 'Article': o[k] = ORG_REF
        if isinstance(o.get('isPartOf'), dict) and o['isPartOf'].get('@type') == 'WebSite': o['isPartOf'] = {'@id': SITE_ID}
    md = re.search(r'<meta name="description" content="([^"]*)"', s)
    if md:  # keep the main node's description identical to the (fitted) meta description
        for k in ('Article', 'WebPage', 'CollectionPage', 'LearningResource', 'DefinedTermSet'):
            if k in by and by[k].get('description'): by[k]['description'] = html.unescape(md.group(1))
    order = ['Organization', 'WebSite', 'BreadcrumbList', 'Article', 'LearningResource', 'CollectionPage', 'DefinedTermSet', 'FAQPage', 'WebPage', 'Multi']
    objs2 = [by[k] for k in order if k in by] + [v for k, v in by.items() if k not in order] + dup
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
    print('seo-jsonld: updated', run(sys.argv[1:] or ['en', 'fr', 'es', 'ar', 'it', 'he']), 'pages')
