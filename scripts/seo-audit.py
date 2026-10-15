"""SEO audit for every page (English + fr/es/ar). Prints issue counts per check and a total.
Usage: python3 scripts/seo-audit.py [--list]   (--list prints each issue)"""
import glob, json, os, re, sys, collections
from bs4 import BeautifulSoup
SITE = 'https://www.savingplanets.com/'; LANGS = ['fr', 'es', 'ar', 'it']
NOINDEX = {'Project-R.html', '404.html'}
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR', 'it': 'it_IT'}
pages = sorted(glob.glob('*.html')) + sorted(p for l in LANGS for p in glob.glob(f'{l}/*.html'))
pages = [p for p in pages if not re.match(r'google[0-9a-f]+\.html$', os.path.basename(p))]  # Search Console verification file
issues = collections.defaultdict(list); titles = collections.defaultdict(list); descs = collections.defaultdict(list)
sitemap = open('sitemap.xml', encoding='utf8').read() if os.path.exists('sitemap.xml') else ''
locs = set(re.findall(r'<loc>([^<]+)</loc>', sitemap))
def add(k, p, msg=''): issues[k].append(f'{p} {msg}'.strip())
for p in pages:
    lang = p.split('/')[0] if '/' in p else 'en'; base = os.path.basename(p)
    soup = BeautifulSoup(open(p, encoding='utf8').read(), 'html.parser')
    h = soup.html
    if not h or h.get('lang') != lang: add('html-lang', p)
    if (lang == 'ar') != (h is not None and h.get('dir') == 'rtl'): add('html-dir', p)
    rob = soup.find('meta', attrs={'name': 'robots'}); rc = (rob.get('content', '') if rob else '').replace(' ', '')
    noidx = base in NOINDEX
    if noidx:
        if 'noindex' not in rc: add('robots', p, 'should be noindex')
        continue
    if rc != 'index,follow': add('robots', p, rc or 'missing')
    url = SITE + p
    t = soup.title.get_text(strip=True) if soup.title else ''
    if not t: add('title-missing', p)
    elif len(t) > 60: add('title-length', p, f'{len(t)}')
    titles[t].append(p)
    d = soup.find('meta', attrs={'name': 'description'}); d = d.get('content', '').strip() if d else ''
    if not d: add('desc-missing', p)
    elif not 120 <= len(d) <= 155: add('desc-length', p, f'{len(d)}')
    descs[d].append(p)
    c = soup.find('link', rel='canonical')
    if not c or c.get('href') != url: add('canonical', p)
    alts = {l.get('hreflang'): l.get('href') for l in soup.find_all('link', rel='alternate') if l.get('hreflang')}
    translated = all(os.path.exists(f'{l}/{base}') for l in LANGS)
    want = {'en': SITE + base, 'x-default': SITE + base}
    if translated: want.update({l: f'{SITE}{l}/{base}' for l in LANGS})
    if alts != want: add('hreflang', p)
    og = {m.get('property'): m.get('content', '') for m in soup.find_all('meta') if m.get('property')}
    tw = {m.get('name'): m.get('content', '') for m in soup.find_all('meta') if m.get('name', '').startswith('twitter:')}
    if og.get('og:locale') != LOCALE[lang]: add('og-locale', p)
    if translated and len(soup.find_all('meta', property='og:locale:alternate')) != 3: add('og-locale-alt', p)
    for k in ('og:title', 'og:description', 'og:image', 'og:url'):
        if not og.get(k): add('og-missing', p, k)
    for k in ('twitter:title', 'twitter:description', 'twitter:image'):
        if not tw.get(k): add('twitter-missing', p, k)
    for v in (og.get('og:image', ''), og.get('og:url', ''), tw.get('twitter:image', '')):
        if v and not v.startswith('https://'): add('og-relative-url', p, v)
    if og.get('og:url') and og['og:url'] != url: add('og-url', p)
    types = []
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            j = json.loads(s.string or ''); items = j if isinstance(j, list) else j.get('@graph', [j])
            types += [(i.get('@type'), i) for i in items]
        except Exception: add('jsonld-invalid', p)
    T = dict(types)
    if base == 'index.html':
        for k in ('WebSite', 'Organization'):
            if k not in T: add('jsonld-home', p, k)
        if 'WebSite' in T and 'potentialAction' not in T['WebSite']: add('jsonld-home', p, 'SearchAction')
        if 'WebSite' in T and T['WebSite'].get('inLanguage') != lang: add('jsonld-home', p, 'inLanguage')
    else:
        if 'BreadcrumbList' not in T: add('jsonld-breadcrumb', p)
        a = T.get('Article') or T.get('WebPage') or T.get('CollectionPage')
        if not a: add('jsonld-article', p, 'missing')
        else:
            for k in ('datePublished', 'dateModified', 'inLanguage'):
                if not a.get(k): add('jsonld-article', p, k)
            if a.get('inLanguage') and a['inLanguage'] != lang: add('jsonld-article', p, 'inLanguage wrong')
    h1 = soup.find_all('h1')
    if len(h1) != 1: add('h1-count', p, str(len(h1)))
    for img in soup.find_all('img'):
        if img.get('alt') is None: add('img-alt', p, img.get('src', ''))
        if not (img.get('width') and img.get('height')): add('img-size', p, img.get('src', ''))
        if img.get('loading') != 'lazy' and img.get('fetchpriority') != 'high': add('img-lazy', p, img.get('src', ''))
    if lang != 'en' and os.path.exists(base):  # alt text identical to the English page's alt = not localized
        en_alts = {i.get('alt', '') for i in BeautifulSoup(open(base, encoding='utf8').read(), 'html.parser').find_all('img')}
        for img in soup.find_all('img'):
            a = img.get('alt', '')
            if a and a in en_alts and re.search(r'\b(the|of|and|with)\b', a): add('img-alt-english', p, a[:40])
    if url not in locs: add('sitemap-missing', p)
for t, ps in titles.items():
    if t and len(ps) > 1: add('title-duplicate', ' '.join(ps), t)
for d, ps in descs.items():
    if d and len(ps) > 1: add('desc-duplicate', ' '.join(ps), d[:50])
rt = open('robots.txt').read() if os.path.exists('robots.txt') else ''
if 'Sitemap: ' + SITE + 'sitemap.xml' not in rt: add('robots-txt', 'robots.txt')
for u in locs:
    if not os.path.exists(u[len(SITE):] or 'index.html'): add('sitemap-dead', u)
if 'hreflang' not in sitemap: add('sitemap-hreflang', 'sitemap.xml')
if sitemap.count('<lastmod>') != sitemap.count('<loc>'): add('sitemap-lastmod', 'sitemap.xml')
print(f'pages: {len(pages)}')
for k in sorted(issues):
    print(f'{k:20} {len(issues[k])}')
    if '--list' in sys.argv:
        for i in issues[k][:400]: print('   ', i)
print('TOTAL', sum(len(v) for v in issues.values()))
