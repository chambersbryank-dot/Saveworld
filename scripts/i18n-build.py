#!/usr/bin/env python3
"""Generate /fr/, /es/, /ar/ translations of the pages in PAGES from the English originals.
Translations live in i18n/<lang>.json (English string -> translation; missing = English kept).
Run from repo root:  python3 scripts/i18n-build.py   then  node scripts/i18n-check.js
Needs: pip install beautifulsoup4"""
import json, re, os, hashlib, sys
from bs4 import BeautifulSoup, Comment

SITE = 'https://www.savingplanets.com/'
LANGS = ['fr', 'es', 'ar']
PAGES = ['Project-Rawane.html', 'Oceans.html', 'Lakes.html', 'Rivers.html', 'Deforestation.html', 'Space.html',
         'Space_Disposal.html', 'Planetary_Defense.html', 'Space_Weather.html', 'Earth_Observation.html', 'Amazing_Facts.html']
LABEL = {'en': 'EN', 'fr': 'FR', 'es': 'ES', 'ar': 'العربية'}
LANGNAME = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية'}
SWITCH_ARIA = {'en': 'Language', 'fr': 'Langue', 'es': 'Idioma', 'ar': 'اللغة'}
ATTRS = ('alt', 'aria-label', 'title', 'data-title', 'data-image-alt', 'placeholder')
META = {'description', 'twitter:description', 'twitter:title', 'og:description', 'og:title'}
FFI = 'For Further Information: '

def normalize(src):
    """English source minus parts that change for site-wide/nav reasons (kept in sync with scripts/i18n-check.js)."""
    src = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', src)
    src = re.sub(r'<!-- PROJECT-R-MENU:START -->[\s\S]*?<!-- PROJECT-R-MENU:END -->', '', src)
    src = re.sub(r'<!-- SOLUTIONS-MENU:START -->[\s\S]*?<!-- SOLUTIONS-MENU:END -->', '', src)
    src = re.sub(r'<li class="lang-switch"[\s\S]*?</li>', '', src)
    src = re.sub(r'\?v=[0-9a-z]+', '', src)
    return src

def src_hash(page):
    return hashlib.sha1(normalize(open(page, encoding='utf8').read()).encode('utf8')).hexdigest()[:12]

def switcher(page, cur, prefix):
    """Language switcher <li>. prefix = path from current page to site root ('' or '../')."""
    items = []
    for l in ['en'] + LANGS:
        if l == 'en':
            href = prefix + page
        else:
            href = prefix + l + '/' + (page if page in PAGES else 'Project-Rawane.html')
        a = f'<a href="{href}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == cur else '') + f' title="{LANGNAME[l]}">{LABEL[l]}</a>'
        items.append(a)
    return f'<li class="lang-switch" aria-label="{SWITCH_ARIA[cur]}">' + '<span aria-hidden="true"> · </span>'.join(items) + '</li>'

def hreflang_links(page):
    out = [f'<link rel="alternate" hreflang="en" href="{SITE}{page}">']
    out += [f'<link rel="alternate" hreflang="{l}" href="{SITE}{l}/{page}">' for l in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{page}">')
    return '\n'.join(out)

def tr(m, s):
    st = s.strip()
    if not st: return s
    if st.startswith(FFI):
        t = m.get(FFI, FFI) + st[len(FFI):]
    else:
        t = m.get(st)
        if t is None: return s
    lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
    return lead + t + trail

def fix_url(u):
    if not u or re.match(r'^(https?:|mailto:|tel:|#|/|data:|javascript:)', u): return u
    page = u.split('#')[0].split('?')[0]
    if page in PAGES: return u            # stay inside the language folder
    return '../' + u

def build(page, lang, m):
    raw = open(page, encoding='utf8').read()
    soup = BeautifulSoup(raw, 'html.parser')
    html = soup.html
    html['lang'] = lang
    if lang == 'ar': html['dir'] = 'rtl'
    for t in soup.find_all(string=True):
        if isinstance(t, Comment) or t.parent.name in ('script', 'style'): continue
        new = tr(m, str(t))
        if new != str(t): t.replace_with(new)
    for tag in soup.find_all(True):
        for a in ATTRS:
            if tag.get(a): tag[a] = tr(m, tag[a])
        if tag.name == 'meta' and (tag.get('name') in META or tag.get('property') in META) and tag.get('content'):
            tag['content'] = tr(m, tag['content'])
        for a in ('href', 'src', 'data-image', 'data-fact-page'):
            if tag.get(a) and not (tag.name == 'link' and tag.get('rel') in (['canonical'], ['alternate'])):
                tag[a] = fix_url(tag[a])
    for s in soup.find_all('script'):
        if s.get('type') == 'application/ld+json' and s.string:
            s.string = s.string.replace(SITE + page, SITE + lang + '/' + page)
    for l in soup.find_all('link', rel='canonical'): l['href'] = SITE + lang + '/' + page
    for l in soup.find_all('meta', property='og:url'): l['content'] = SITE + lang + '/' + page
    for l in soup.find_all('link', rel='alternate'): l.decompose()
    for l in soup.find_all('meta', attrs={'name': 'i18n-source'}): l.decompose()
    for l in soup.find_all('meta', property='og:locale'): l.decompose()
    for li in soup.select('li.lang-switch'): li.decompose()
    head = soup.head
    can = head.find('link', rel='canonical')
    extra = BeautifulSoup(hreflang_links(page) + f'\n<meta name="i18n-source" content="{page} {src_hash(page)}">'
                          + f'\n<meta property="og:locale" content="{ {"fr":"fr_FR","es":"es_ES","ar":"ar_AR"}[lang] }">', 'html.parser')
    can.insert_after(extra)
    ul = soup.select_one('nav#topnav ul.nav-links')
    if ul: ul.append(BeautifulSoup(switcher(page, lang, '../'), 'html.parser'))
    # amazing-fact tags in translations must not be collected again: drop the class marker
    for p in soup.select('p.amazing-fact'):
        p['class'] = [c for c in p['class'] if c != 'amazing-fact'] + ['amazing-fact-i18n']
    out = str(soup)
    os.makedirs(lang, exist_ok=True)
    open(os.path.join(lang, page), 'w', encoding='utf8').write(out)

def english_head(page):
    """Add hreflang alternates to an English original (idempotent)."""
    src = open(page, encoding='utf8').read()
    src = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', src)
    src = src.replace(f'<link rel="canonical" href="{SITE}{page}">', f'<link rel="canonical" href="{SITE}{page}">\n' + hreflang_links(page), 1)
    open(page, 'w', encoding='utf8').write(src)

def missing(lang):
    """Print English strings on the PAGES that have no entry in i18n/<lang>.json (to translate next)."""
    m = json.load(open(f'i18n/{lang}.json', encoding='utf8')); seen = set()
    for page in PAGES:
        soup = BeautifulSoup(open(page, encoding='utf8').read(), 'html.parser')
        for li in soup.select('li.lang-switch'): li.decompose()
        vals = [str(t).strip() for t in soup.find_all(string=True) if not isinstance(t, Comment) and t.parent.name not in ('script', 'style')
                and not (t.find_parent('a') and t.find_parent('a').get('href', '').startswith('http') and not str(t).strip().startswith(FFI))]
        vals += [tag[a].strip() for tag in soup.find_all(True) for a in ATTRS if tag.get(a)]
        for v in vals:
            if v.startswith(FFI): v = FFI
            if v and re.search('[A-Za-z]{3}', v) and v not in m and v not in seen:
                seen.add(v); print(f'{page}\t{v}')

if __name__ == '__main__':
    if sys.argv[1:2] == ['--missing']:
        missing(sys.argv[2] if len(sys.argv) > 2 else 'fr'); sys.exit(0)
    langs = sys.argv[1:] or LANGS
    for page in PAGES: english_head(page)
    for lang in langs:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        for page in PAGES: build(page, lang, m)
        print(lang, 'built', len(PAGES), 'pages')
