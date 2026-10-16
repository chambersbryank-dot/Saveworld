"""Rewrite sitemap.xml i18n entries: every page in i18n/pages.txt gets fr/es/ar URLs, and English + translated
entries carry xhtml:link hreflang alternates. Idempotent; leaves other English entries untouched."""
import re, datetime
SITE = 'https://www.savingplanets.com/'; LANGS = ['fr', 'es', 'ar', 'it']
PAGES = [l.strip() for l in open('i18n/pages.txt', encoding='utf8') if l.strip() and not l.startswith('#')]
s = open('sitemap.xml', encoding='utf8').read()
def alts(p):
    return ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{pre}{p}"/>' for h, pre in [('en', ''), *[(l, l + '/') for l in LANGS], ('x-default', '')])
urls = []
for u in re.findall(r'<url>.*?</url>', s, flags=re.S):
    u = re.sub(r'<xhtml:link [^>]*/>', '', u)
    loc = re.search(r'<loc>([^<]+)</loc>', u).group(1)
    if re.match(re.escape(SITE) + r'(fr|es|ar|it)/', loc): continue
    p = loc[len(SITE):]
    if p in PAGES: u = u.replace('</loc>', '</loc>' + alts(p), 1)
    urls.append(u)
today = datetime.date.today().isoformat()
# Oct 15: English page missing its own <loc> (new pages were only listed as hreflang alternates) gets one.
have = {re.search(r'<loc>([^<]+)</loc>', u).group(1)[len(SITE):] for u in urls}
urls += [f'<url><loc>{SITE}{p}</loc>{alts(p)}<lastmod>{today}</lastmod></url>' for p in PAGES if p not in have]
urls += [f'<url><loc>{SITE}{l}/{p}</loc>{alts(p)}<lastmod>{today}</lastmod></url>' for l in LANGS for p in PAGES]
s = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
     + ''.join('  ' + u + '\n' for u in urls) + '</urlset>\n')
open('sitemap.xml', 'w', encoding='utf8').write(s)
