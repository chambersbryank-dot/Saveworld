"""Rebuild sitemap.xml from the pages on disk (Oct 16 SEO pass; replaces the i18n/pages.txt-only version).
Every indexable page in en, fr, es, ar, it gets a <url> with xhtml:link hreflang alternates for exactly the
language versions that exist (+ x-default = English) and <lastmod> = date of the file's last commit (today if
uncommitted). Skipped: redirect stubs (meta refresh), robots noindex pages, 404, Search Console verification files.
index.html is listed at its directory URL. Idempotent; other generators may still append entries, this one runs last."""
import glob, os, re, subprocess, datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://www.savingplanets.com/'; LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
SKIP = re.compile(r'^(google[0-9a-f]+|404)\.html$')
def url(l, b): return SITE + ('' if l == 'en' else l + '/') + ('' if b == 'index.html' else b)
def path(l, b): return b if l == 'en' else f'{l}/{b}'
def indexable(f):
    if SKIP.match(os.path.basename(f)): return False
    head = open(f, encoding='utf8').read().split('</head>')[0]
    if 'http-equiv="refresh"' in head: return False
    m = re.search(r'<meta name="robots" content="([^"]*)"', head) or re.search(r'<meta content="([^"]*)" name="robots"', head)
    return not (m and 'noindex' in m.group(1).replace(' ', '').lower())
today = datetime.date.today().isoformat()
dates = {}
try:
    log = subprocess.run(['git', 'log', '--format=@%as', '--name-only', '--', '*.html'], capture_output=True, text=True).stdout
    cur = None
    for ln in log.splitlines():
        if ln.startswith('@'): cur = ln[1:]
        elif ln and ln not in dates: dates[ln] = cur
    dirty = set(subprocess.run(['git', 'status', '--porcelain', '--', '*.html'], capture_output=True, text=True).stdout.split('\n'))
    for ln in dirty:
        if ln.strip(): dates[ln[3:].strip()] = today
except Exception: pass
have = {l: {os.path.basename(f) for f in glob.glob(path(l, '*.html')) if indexable(f)} for l in LANGS}
bases = sorted(set().union(*have.values()), key=lambda b: (b != 'index.html', b.lower()))
rows = []
for l in LANGS:
    for b in bases:
        if b not in have[l]: continue
        ls = [x for x in LANGS if b in have[x]]
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{url(x, b)}"/>' for x in ls)
        if 'en' in ls and len(ls) > 1: alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", b)}"/>'
        if len(ls) == 1: alts = ''
        rows.append(f'  <url><loc>{url(l, b)}</loc>{alts}<lastmod>{dates.get(path(l, b)) or today}</lastmod></url>\n')
out = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
       + ''.join(rows) + '</urlset>\n')
old = open('sitemap.xml', encoding='utf8').read() if os.path.exists('sitemap.xml') else ''
if out != old: open('sitemap.xml', 'w', encoding='utf8').write(out)
print(f'i18n-sitemap: {len(rows)} URLs, {len(out)//1024} KB' + ('' if out != old else ' (unchanged)'))
