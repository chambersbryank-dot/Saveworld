"""Rebuild sitemap.xml from the pages on disk (Oct 16 SEO pass; replaces the i18n/pages.txt-only version).
Every indexable page in en, fr, es, ar, it, he gets a <url> with xhtml:link hreflang alternates for exactly the
language versions that exist (+ x-default = English) and <lastmod> = committer date of that file's last commit
(`git log -1 --format=%cs`), or today if the file is uncommitted. Skipped: redirect stubs (meta refresh), robots
noindex pages, 404, and Search Console verification files. index.html is listed at its directory URL. Idempotent;
other generators may still append entries, this one runs last. The Pages deploy workflow runs it before upload
(full git history required)."""
import glob, os, re, subprocess, datetime
from concurrent.futures import ThreadPoolExecutor
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://www.savingplanets.com/'; LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
SKIP = re.compile(r'^(google[0-9a-f]+|404|offline|GLOBE_Review|Style_Options)\.html$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
URL_LIMIT, BYTE_LIMIT = 50000, 50 * 1024 * 1024
def url(l, b): return SITE + ('' if l == 'en' else l + '/') + ('' if b == 'index.html' else b)
def path(l, b): return b if l == 'en' else f'{l}/{b}'
def indexable(f):
    if SKIP.match(os.path.basename(f)): return False
    head = open(f, encoding='utf8').read().split('</head>')[0]
    if 'http-equiv="refresh"' in head: return False
    m = re.search(r'<meta name="robots" content="([^"]*)"', head) or re.search(r'<meta content="([^"]*)" name="robots"', head)
    return not (m and 'noindex' in m.group(1).replace(' ', '').lower())
def dirty_html():
    """HTML paths with uncommitted changes. Renames report the new path."""
    r = subprocess.run(['git', 'status', '--porcelain', '-z'], capture_output=True, text=True)
    if r.returncode != 0: return set()
    parts = r.stdout.split('\0')
    out, i = set(), 0
    while i < len(parts):
        rec = parts[i]; i += 1
        if not rec: continue
        status, path_ = rec[:2], rec[3:] if len(rec) >= 3 else rec
        if 'R' in status or 'C' in status:
            if i < len(parts):
                path_ = parts[i]; i += 1
        if path_.endswith('.html'): out.add(path_)
    return out
def commit_date(p):
    """Committer date of the last commit that touched p. Empty when git has no history for it."""
    r = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', p], capture_output=True, text=True)
    line = (r.stdout or '').strip().splitlines()
    return p, line[0] if line and DATE_RE.match(line[0]) else None
def commit_dates(paths):
    shallow = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'], capture_output=True, text=True)
    if (shallow.stdout or '').strip() == 'true':
        msg = 'i18n-sitemap: checkout is shallow; lastmod needs full history (checkout fetch-depth: 0)'
        if os.environ.get('GITHUB_ACTIONS'): raise SystemExit(msg)
        print(msg)
    dirty = dirty_html()
    dates = {}
    workers = min(8, max(1, len(paths)))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for p, d in ex.map(commit_date, paths):
            dates[p] = today if p in dirty or not d else d
    for p in dirty:
        if p.endswith('.html'): dates[p] = today
    return dates
today = datetime.date.today().isoformat()
have = {}
page_paths = []
for l in LANGS:
    files = [f for f in glob.glob(path(l, '*.html')) if indexable(f)]
    have[l] = {os.path.basename(f) for f in files}
    page_paths.extend(files)
try:
    dates = commit_dates(page_paths)
except SystemExit:
    raise
except Exception as e:
    print('i18n-sitemap: git lastmod failed:', e)
    if os.environ.get('GITHUB_ACTIONS'): raise
    dates = {}
bases = sorted(set().union(*have.values()), key=lambda b: (b != 'index.html', b.lower()))
rows = []
for l in LANGS:
    for b in bases:
        if b not in have[l]: continue
        ls = [x for x in LANGS if b in have[x]]
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{url(x, b)}"/>' for x in ls)
        if 'en' in ls: alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", b)}"/>'
        rows.append((l, f'  <url><loc>{url(l, b)}</loc>{alts}<lastmod>{dates.get(path(l, b)) or today}</lastmod></url>\n'))
# One sitemap per language, plus a sitemap index at sitemap.xml.
# Google: https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps
# Bing reads the same sitemap index and lastmod: https://www.bing.com/webmasters/help/sitemaps-3b5cf6ed
head = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
index = ['<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n']
n = 0
for l in LANGS:
    body = ''.join(row for lang, row in rows if lang == l)
    name = f'sitemap-{l}.xml'
    doc = head + body + '</urlset>\n'
    raw = doc.encode('utf-8')
    nloc = body.count('<loc>')
    if nloc > URL_LIMIT or len(raw) > BYTE_LIMIT:
        raise SystemExit(f'i18n-sitemap: {name} exceeds sitemap limits ({nloc} urls, {len(raw)} bytes)')
    old = open(name, encoding='utf8').read() if os.path.exists(name) else ''
    if doc != old: open(name, 'w', encoding='utf8').write(doc)
    last = max((dates.get(path(l, b)) or today for b in sorted(have[l])), default=today)
    index.append(f'  <sitemap><loc>{SITE}{name}</loc><lastmod>{last}</lastmod></sitemap>\n')
    n += nloc
    print(f'  sitemap-{l}.xml {nloc} urls lastmod {last}')
index.append('</sitemapindex>\n')
idx = ''.join(index)
old = open('sitemap.xml', encoding='utf8').read() if os.path.exists('sitemap.xml') else ''
if idx != old: open('sitemap.xml', 'w', encoding='utf8').write(idx)
print(f'i18n-sitemap: {n} URLs in {len(LANGS)} language sitemaps')
