#!/usr/bin/env python3
"""SEO lint + audit for every page in en, fr, es, ar (RTL) and it (Oct 16).
Usage: python3 scripts/seo-lint.py [--list] [--report FILE.md] [--no-fail] [--live]
Exit 1 (unless --no-fail) on ERROR checks: missing/duplicate titles or descriptions, broken hreflang
reciprocity, invalid JSON-LD (unparseable, unknown schema.org type/property, missing required fields).
Everything else is a WARN gap, counted and listed. Pure local check (no network) except --live.
JSON-LD vocabulary: scripts/schemaorg-vocab.json (types + properties from schema.org; refresh with --refresh-vocab)."""
import glob, html, json, os, re, sys, collections
from bs4 import BeautifulSoup
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://www.savingplanets.com/'; LANGS = ['en', 'fr', 'es', 'ar', 'it']
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR', 'it': 'it_IT'}
TWITTER_SITE = '@SISavingPlanets'
NOINDEX = {'Project-R.html', '404.html'}
ERROR = {'title-missing', 'title-duplicate', 'desc-missing', 'desc-duplicate', 'hreflang-reciprocity', 'jsonld-invalid'}
MAIN_TYPES = {'Article', 'NewsArticle', 'BlogPosting', 'WebPage', 'CollectionPage', 'AboutPage', 'ContactPage', 'FAQPage',
              'LearningResource', 'Course', 'DefinedTermSet', 'SearchResultsPage', 'ItemList', 'Dataset', 'WebApplication'}
REQUIRED = {  # Google rich-result required fields (subset we can check locally)
    'BreadcrumbList': ['itemListElement'], 'ListItem': ['position', 'name'],
    'Article': ['headline', 'datePublished', 'author', 'image'], 'FAQPage': ['mainEntity'],
    'Question': ['name', 'acceptedAnswer'], 'Answer': ['text'], 'VideoObject': ['name', 'description', 'thumbnailUrl', 'uploadDate'],
    'Organization': ['name', 'url'], 'WebSite': ['name', 'url'], 'LearningResource': ['name'], 'Course': ['name', 'description', 'provider'],
    'SearchAction': ['target', 'query-input'], 'DefinedTerm': ['name'], 'ImageObject': ['url'],
}
VOCAB = json.load(open('scripts/schemaorg-vocab.json')) if os.path.exists('scripts/schemaorg-vocab.json') else None
EXTRA_PROPS = {'query-input'}  # Google SearchAction convention

def lang_of(p): return p.split('/')[0] if '/' in p else 'en'
def url_of(lang, base):
    pre = '' if lang == 'en' else lang + '/'
    return SITE + pre + ('' if base == 'index.html' else base)
def path_of(lang, base): return base if lang == 'en' else f'{lang}/{base}'

def ancestors(t, seen=None):
    seen = seen if seen is not None else set()
    for p in VOCAB['types'].get(t, []):
        if p not in seen: seen.add(p); ancestors(p, seen)
    return seen | {t}

NESTED_REQUIRED = {'ListItem', 'Question', 'Answer', 'SearchAction', 'DefinedTerm'}  # required fields checked when nested too
def validate_ld(node, p, add, path='$', depth=0):
    """schema.org vocabulary + required-field check (recursive). Rich-result required fields apply to top-level
    nodes (and to the nested types Google reads: ListItem, Question, Answer, SearchAction)."""
    if isinstance(node, list):
        for i, n in enumerate(node): validate_ld(n, p, add, f'{path}[{i}]', depth)
        return
    if not isinstance(node, dict): return
    t = node.get('@type'); ts = t if isinstance(t, list) else ([t] if t else [])
    if VOCAB:
        for x in ts:
            if x not in VOCAB['types']: add('jsonld-invalid', p, f'{path} unknown @type {x}')
        allowed = set().union(*[ancestors(x) for x in ts if x in VOCAB['types']]) if ts else None
        for k in node:
            if k.startswith('@') or k in EXTRA_PROPS: continue
            if k not in VOCAB['props']: add('jsonld-invalid', p, f'{path} unknown property {k}'); continue
            dom = set(VOCAB['props'][k])
            if allowed and dom and not (dom & allowed): add('jsonld-invalid', p, f'{path} {k} not valid on {"/".join(ts)}')
    for x in ts:
        if depth and x not in NESTED_REQUIRED: continue
        for r in REQUIRED.get(x, []):
            if node.get(r) in (None, '', []):
                if not (x == 'ListItem' and r == 'name' and node.get('item')): add('jsonld-invalid', p, f'{path} {x} missing {r}')
    for k, v in node.items():
        if isinstance(v, (dict, list)): validate_ld(v, p, add, f'{path}.{k}', depth + 1)

def visible_text(soup):
    b = soup.body
    if not b: return ''
    b = BeautifulSoup(str(b), 'lxml')
    for t in b(['script', 'style', 'noscript', 'template']): t.decompose()
    return ' '.join(b.get_text(' ').split())

def norm(s): return ' '.join(html.unescape(s or '').replace('\u2019', "'").split()).lower()

def main():
    args = sys.argv[1:]
    pages = [p for l in LANGS for p in sorted(glob.glob('*.html' if l == 'en' else f'{l}/*.html'))
             if not re.match(r'google[0-9a-f]+\.html$', os.path.basename(p))]
    exists = set(pages)
    issues = collections.defaultdict(list)
    def add(k, p, msg=''): issues[k].append(f'{p} {msg}'.strip())
    titles, descs, heads = collections.defaultdict(list), collections.defaultdict(list), {}
    sm = open('sitemap.xml', encoding='utf8').read() if os.path.exists('sitemap.xml') else ''
    sm_urls = {}
    for u in re.findall(r'<url>(.*?)</url>', sm, re.S):
        loc = re.search(r'<loc>([^<]+)</loc>', u).group(1).strip()
        sm_urls[loc] = dict(re.findall(r'<xhtml:link rel="alternate" hreflang="([^"]+)" href="([^"]+)"/>', u))
    en_meta = {}
    parsed = {}
    for p in pages:
        raw = open(p, encoding='utf8').read()
        parsed[p] = (raw, BeautifulSoup(raw, 'lxml'))
    stats = collections.Counter()
    for p in pages:
        raw, soup = parsed[p]; lang = lang_of(p); base = os.path.basename(p); U = url_of(lang, base)
        h = soup.html
        if not h or h.get('lang') != lang: add('html-lang', p)
        if (lang == 'ar') != bool(h and h.get('dir') == 'rtl'): add('html-dir', p)
        rob = soup.find('meta', attrs={'name': 'robots'}); rc = (rob.get('content', '') if rob else '').replace(' ', '').lower()
        stub = 'http-equiv="refresh"' in raw
        if stub or base in NOINDEX:
            stats['noindex/redirect'] += 1
            if 'noindex' not in rc: add('robots', p, 'redirect/noindex page should carry noindex')
            if U in sm_urls: add('sitemap-noindex', p)
            continue
        stats['indexable'] += 1
        head = raw.split('</head>')[0]; heads[p] = len(head.encode())
        if 'noindex' in rc: add('robots', p, 'indexable page marked noindex')
        t = soup.title.get_text(strip=True) if soup.title else ''
        d = (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', '').strip()
        if not t: add('title-missing', p)
        else:
            titles[t].append(p)
            if not 30 <= len(t) <= 60: add('title-length', p, f'{len(t)}: {t}')
            if t.endswith('…'): add('title-truncated', p, t)
        if not d: add('desc-missing', p)
        else:
            descs[d].append(p)
            if not 120 <= len(d) <= 160: add('desc-length', p, f'{len(d)}')
            if d.endswith('…'): add('desc-truncated', p, d[-40:])
        if lang == 'en': en_meta[base] = (t, d)
        c = soup.find_all('link', rel='canonical')
        if len(c) != 1 or c[0].get('href') != U: add('canonical', p, (c[0].get('href') if c else 'missing'))
        alts = {}
        for l in soup.find_all('link', rel='alternate'):
            if l.get('hreflang'):
                if l['hreflang'] in alts: add('hreflang', p, 'duplicate ' + l['hreflang'])
                alts[l['hreflang']] = l.get('href')
        want = {l: url_of(l, base) for l in LANGS if path_of(l, base) in exists}
        want['x-default'] = url_of('en', base)
        if alts != want: add('hreflang', p, f'have {sorted(alts)} want {sorted(want)}')
        for hl, u in alts.items():  # reciprocity: every alternate exists and links back
            if hl == 'x-default': continue
            tp = path_of(hl, base) if u == url_of(hl, base) else None
            if not tp or tp not in parsed: add('hreflang-reciprocity', p, f'{hl} -> {u} (missing page)'); continue
            back = {l.get('hreflang'): l.get('href') for l in parsed[tp][1].find_all('link', rel='alternate') if l.get('hreflang')}
            if back.get(lang) != U: add('hreflang-reciprocity', p, f'{tp} does not link back with hreflang={lang}')
        og = {}
        for m in soup.find_all('meta'):
            if m.get('property'): og.setdefault(m['property'], []).append(m.get('content', ''))
        g1 = lambda k: (og.get(k) or [''])[0]
        for k in ('og:title', 'og:description', 'og:image', 'og:url', 'og:type', 'og:site_name', 'og:locale'):
            if not g1(k): add('og-missing', p, k)
        if g1('og:url') and g1('og:url') != U: add('og-url', p, g1('og:url'))
        if g1('og:locale') and g1('og:locale') != LOCALE[lang]: add('og-locale', p, g1('og:locale'))
        want_alt = sorted(LOCALE[l] for l in LANGS if l != lang and path_of(l, base) in exists)
        if sorted(og.get('og:locale:alternate', [])) != want_alt: add('og-locale-alt', p)
        img = g1('og:image')
        if img and not img.startswith('https://'): add('og-image', p, 'not absolute https')
        try: w, hh = int(g1('og:image:width') or 0), int(g1('og:image:height') or 0)
        except ValueError: w = hh = 0
        if img and (w < 1200 or hh < 630): add('og-image-size', p, f'{w}x{hh} declared')
        if img.startswith(SITE):
            f = img[len(SITE):].split('?')[0]
            if not os.path.exists(f): add('og-image', p, 'file missing ' + f)
        if not g1('og:image:alt'): add('og-image-alt', p)
        tw = {m.get('name'): m.get('content', '') for m in soup.find_all('meta') if (m.get('name') or '').startswith('twitter:')}
        if tw.get('twitter:card') != 'summary_large_image': add('twitter-card', p, tw.get('twitter:card', 'missing'))
        if tw.get('twitter:site') != TWITTER_SITE: add('twitter-site', p)
        for k in ('twitter:title', 'twitter:description', 'twitter:image'):
            if not tw.get(k): add('twitter-missing', p, k)
        # JSON-LD
        nodes = []
        for s in soup.find_all('script', type='application/ld+json'):
            try: j = json.loads(s.string or '')
            except Exception as e: add('jsonld-invalid', p, f'parse error {e}'); continue
            validate_ld(j, p, add)
            items = j if isinstance(j, list) else j.get('@graph', [j])
            nodes += [i for i in items if isinstance(i, dict)]
            stats['jsonld-bytes'] += len((s.string or '').encode())
        T = collections.defaultdict(list)
        for n in nodes:
            for x in (n.get('@type') if isinstance(n.get('@type'), list) else [n.get('@type')]): T[x].append(n)
        if 'WebSite' not in T: add('jsonld-website', p, 'missing')
        elif not any('potentialAction' in n for n in T['WebSite']): add('jsonld-website', p, 'no SearchAction')
        else:
            tgt = json.dumps([n.get('potentialAction') for n in T['WebSite']])
            if 'Search.html?q={search_term_string}' not in tgt: add('jsonld-website', p, 'SearchAction target')
        if 'Organization' not in T and not any(isinstance(n.get('publisher'), dict) and n['publisher'].get('@id') for n in nodes): add('jsonld-organization', p)
        if base != 'index.html' and 'BreadcrumbList' not in T: add('jsonld-breadcrumb', p)
        mains = [n for k in MAIN_TYPES for n in T.get(k, [])]
        if base != 'index.html':
            if not mains: add('jsonld-main', p, 'no page-level type')
            for n in mains:
                if n.get('inLanguage') and n['inLanguage'] != lang: add('jsonld-main', p, f'inLanguage {n["inLanguage"]}')
                if not n.get('inLanguage'): add('jsonld-main', p, f'{n.get("@type")} no inLanguage')
        vis = None
        if base == 'Myth_vs_Fact.html':
            if 'FAQPage' not in T: add('jsonld-faq', p, 'Myth vs Fact has visible Q&A but no FAQPage')
        for n in T.get('FAQPage', []):  # FAQ must match visible content
            vis = vis or norm(visible_text(soup))
            for q in n.get('mainEntity', []):
                if norm(q.get('name'))[:60] not in vis: add('jsonld-faq', p, 'question not visible: ' + str(q.get('name'))[:50])
        has_video = bool(re.search(r'<!-- VIDEO:START -->', raw))
        if has_video and 'VideoObject' not in T: add('jsonld-video', p)
        # images
        for im in soup.find_all('img'):
            if im.get('alt') is None: add('img-alt', p, im.get('src', '')[:60])
        if U not in sm_urls: add('sitemap-missing', p)
        elif sm_urls[U] != {k: v for k, v in want.items()}: add('sitemap-hreflang', p)
    # untranslated titles/descriptions (identical to English)
    for p in pages:
        lang = lang_of(p); base = os.path.basename(p)
        if lang == 'en' or base not in en_meta or p not in heads: continue
        soup = parsed[p][1]
        t = soup.title.get_text(strip=True) if soup.title else ''
        d = (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', '').strip()
        if t and t == en_meta[base][0]: add('title-untranslated', p, t)
        if d and d == en_meta[base][1]: add('desc-untranslated', p)
    for t, ps in titles.items():
        if len(ps) > 1: add('title-duplicate', ' '.join(ps), t)
    for d, ps in descs.items():
        if len(ps) > 1: add('desc-duplicate', ' '.join(ps), d[:60])
    rt = open('robots.txt').read() if os.path.exists('robots.txt') else ''
    if 'Sitemap: ' + SITE + 'sitemap.xml' not in rt: add('robots-txt', 'robots.txt', 'no Sitemap line')
    for u in sm_urls:
        rel = u[len(SITE):]
        f = (rel + 'index.html') if (rel == '' or rel.endswith('/')) else rel
        if f not in exists: add('sitemap-dead', u)
    if sm.count('<lastmod>') != sm.count('<loc>'): add('sitemap-lastmod', 'sitemap.xml')
    key = [f for f in glob.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}\.txt', f)]
    if not key or open(key[0]).read().strip() != key[0][:-4]: add('indexnow-key', 'missing or mismatched key file')
    hs = sorted(heads.values())
    summary = {k: len(v) for k, v in sorted(issues.items())}
    total = sum(summary.values()); errors = sum(v for k, v in summary.items() if k in ERROR)
    print(f'pages: {len(pages)} ({stats["indexable"]} indexable, {stats["noindex/redirect"]} noindex/redirect)')
    if hs: print(f'head size: median {hs[len(hs)//2]} B, max {hs[-1]} B')
    for k, v in summary.items():
        print(f'{"ERROR" if k in ERROR else "warn ":5} {k:22} {v}')
        if '--list' in args:
            for i in issues[k][:500]: print('     ', i)
    print('TOTAL', total, 'ERRORS', errors)
    if '--report' in args:
        out = args[args.index('--report') + 1]
        with open(out, 'w', encoding='utf8') as f:
            f.write(f'# SEO lint report\n\nPages: {len(pages)} ({stats["indexable"]} indexable). Total gaps: **{total}** (errors: {errors}).\n\n| Check | Level | Count |\n|---|---|---|\n')
            for k, v in summary.items(): f.write(f'| {k} | {"ERROR" if k in ERROR else "warn"} | {v} |\n')
            for k, v in summary.items():
                f.write(f'\n## {k} ({v})\n\n'); f.write(''.join(f'- {i}\n' for i in issues[k][:60]))
                if v > 60: f.write(f'- … and {v - 60} more\n')
    if errors and '--no-fail' not in args: sys.exit(1)

if __name__ == '__main__':
    main()
