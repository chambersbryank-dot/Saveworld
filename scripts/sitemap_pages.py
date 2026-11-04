"""Page URLs live in sitemap-{lang}.xml. sitemap.xml is the sitemap index (PR #206).

Readers that want the English page list use read_lang('en').
Writers that insert or drop <url> entries use ensure_url(), strip_page(), or
rewrite() and never open sitemap.xml. i18n-sitemap.py owns the index.
"""
import os, re

LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')

def path_for(lang='en'):
    return f'sitemap-{lang}.xml'

def read_lang(lang='en'):
    p = path_for(lang)
    if os.path.exists(p):
        return open(p, encoding='utf-8').read()
    if lang == 'en' and os.path.exists('sitemap.xml'):
        legacy = open('sitemap.xml', encoding='utf-8').read()
        if '<urlset' in legacy and '<sitemapindex' not in legacy:
            return legacy
    return ''

def write_lang(lang, text):
    p = path_for(lang)
    old = open(p, encoding='utf-8').read() if os.path.exists(p) else None
    if text != old:
        open(p, 'w', encoding='utf-8').write(text)
        return 1
    return 0

def lang_of_loc(loc):
    m = re.search(r'https://www\.savingplanets\.com/(?:([a-z]{2})/)?', loc)
    code = m.group(1) if m else None
    return code if code in LANGS else 'en'

def ensure_url(loc, lastmod, changefreq=None, priority=None):
    """Insert one <url> into the language sitemap that owns loc, if it is missing."""
    lang = lang_of_loc(loc)
    s = read_lang(lang)
    if not s or f'<loc>{loc}</loc>' in s or '</urlset>' not in s:
        return 0
    bits = f'<lastmod>{lastmod}</lastmod>'
    if changefreq:
        bits += f'<changefreq>{changefreq}</changefreq>'
    if priority:
        bits += f'<priority>{priority}</priority>'
    block = f'  <url><loc>{loc}</loc>{bits}</url>\n'
    return write_lang(lang, s.replace('</urlset>', block + '</urlset>', 1))

def strip_page(filename):
    """Drop one HTML page from every language sitemap (its <url> and any hreflang to it)."""
    url_re = re.compile(
        r'\s*<url>\s*<loc>https://www\.savingplanets\.com/(?:(?:fr|es|ar|it|he)/)?'
        + re.escape(filename) + r'</loc>.*?</url>', re.S)
    link_re = re.compile(
        r'\s*<xhtml:link [^>]*href="https://www\.savingplanets\.com/(?:(?:fr|es|ar|it|he)/)?'
        + re.escape(filename) + r'"\s*/>')
    n = 0
    for lang in LANGS:
        s = read_lang(lang)
        if not s:
            continue
        s2 = link_re.sub('', url_re.sub('', s))
        n += write_lang(lang, s2)
    return n

def rewrite(fn):
    """Apply fn to each language sitemap. fn receives the file text and returns the new text."""
    n = 0
    for lang in LANGS:
        s = read_lang(lang)
        if not s:
            continue
        n += write_lang(lang, fn(s))
    return n

def joined_urlsets():
    """All language urlsets, for checks that need every page URL. Not the index."""
    return '\n'.join(read_lang(lang) for lang in LANGS if read_lang(lang))

def english_has(page):
    """True when sitemap-en.xml lists this English HTML file."""
    return f'savingplanets.com/{page}' in read_lang('en')
