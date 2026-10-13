"""Idempotent SEO normalizer. Usage: python3 scripts/seo-fix.py [en|fr|es|ar ...]  (default: all)
Per page: meta robots, <=60-char localized title, 120-155-char localized description (og/twitter synced),
canonical/og:url, hreflang set incl. x-default, og:locale(+alternates), JSON-LD dates/inLanguage, image
width/height/lazy. Run after build-stats.js and after scripts/i18n-build.py (which calls it for translations)."""
import glob, json, os, re, subprocess, sys
from bs4 import BeautifulSoup
SITE = 'https://www.savingplanets.com/'; LANGS = ['fr', 'es', 'ar']
NOINDEX = {'Project-R.html', '404.html'}
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR'}
BRAND = ' | Saving Planets'
# Language tag added to translated titles that would otherwise equal the English title (proper names).
TAG = {'fr': ' · Français', 'es': ' · Español', 'ar': ' · بالعربية'}
PAD = {'en': 'Sourced facts, the Five W\'s and why it matters, on Saving Planets.',
       'fr': 'Faits sourcés, les cinq W et l\'impact, sur Saving Planets.',
       'es': 'Datos con fuentes, las cinco W y su impacto, en Saving Planets.',
       'ar': 'حقائق موثّقة والأسئلة الخمسة وأهمية الحل، على Saving Planets.'}
END = re.compile(r'(?<=[.!?؟。])\s+')
_git = {}
def gitdates(f):
    if f not in _git:
        out = subprocess.run(['git', 'log', '--follow', '--format=%as', '--', f], capture_output=True, text=True).stdout.split()
        _git[f] = (out[-1], out[0]) if out else (None, None)
    return _git[f]

def fit_title(t, en_title=None, lang='en'):
    t = re.sub(r'\s+', ' ', t).strip()
    if lang != 'en' and en_title and (t == en_title or t.replace(BRAND, '') == en_title.replace(BRAND, '')):
        core = t.replace(BRAND, '')
        for cand in (core + BRAND + TAG[lang], core + TAG[lang]):
            if len(cand) <= 60: return cand
        t = core + TAG[lang]
    if len(t) <= 60: return t
    core = t.replace(BRAND, '')
    if len(core) <= 60: return core
    return core[:59].rsplit(' ', 1)[0].rstrip(' ,:;–-') + '…'

def fit_desc(base, extra, lang):
    """base sentence(s) first; add sentences from extra while <120; trim to <=155 at a sentence or word boundary."""
    text = re.sub(r'\s+', ' ', base).strip()
    for s in [x for e in extra for x in END.split(re.sub(r'\s+', ' ', e).strip()) if x] + [PAD[lang]]:
        if len(text) >= 120: break
        if s and s not in text: text = (text + ' ' + s).strip()
    if len(text) <= 155: return text
    sents = END.split(text); out = ''
    for s in sents:
        if len((out + ' ' + s).strip()) <= 155: out = (out + ' ' + s).strip()
        else: break
    if len(out) >= 120: return out
    cut = text[:154].rsplit(' ', 1)[0].rstrip(' ,;:–-')
    return cut + '…'

def esc(v): return v.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
HEAD_RX = [r'<meta name="robots"[^>]*>', r'<link rel="canonical"[^>]*>', r'<link rel="alternate" hreflang="[^"]*"[^>]*>',
           r'<title>.*?</title>', r'<meta name="description"[^>]*>', r'<meta property="og:[^"]*"[^>]*>', r'<meta name="twitter:[^"]*"[^>]*>',
           r'<link href="[^"]*" rel="canonical"/?>', r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/?>', r'<meta content="[^"]*" name="(?:robots|description|twitter:[^"]*)"/?>',
           r'<meta content="[^"]*" property="og:[^"]*"/?>', r'<link rel="alternate"[^>]*hreflang[^>]*>']

def fix(p):
    """Text-level edits (keeps the file's own formatting; only the SEO head block and JSON-LD/img attributes change)."""
    lang = p.split('/')[0] if '/' in p else 'en'; base = os.path.basename(p)
    raw = open(p, encoding='utf8').read(); soup = BeautifulSoup(raw, 'html.parser')
    if not soup.head: return False
    src = raw
    src = re.sub(r'<html[^>]*>', lambda m: '<html lang="%s"%s class="dark">' % (lang, ' dir="rtl"' if lang == 'ar' else ''), src, count=1)
    head_end = src.index('</head>'); head = src[:head_end]; rest = src[head_end:]
    for rx in HEAD_RX: head = re.sub(r'\n?' + rx, '', head, flags=re.S)
    block = []
    if base in NOINDEX:
        t = soup.title.get_text() if soup.title else 'Saving Planets'
        block = [f'<title>{esc(t)}</title>', '<meta name="robots" content="noindex">']
        c = soup.find('link', rel='canonical')
        if c: block.append(f'<link rel="canonical" href="{c["href"]}">')
        img = (soup.find('meta', property='og:image') or {}).get('content') or SITE + 'assets/SavePlanetLogo.jpg'  # Batch A: share card even on noindex pages
        block += [f'<meta property="og:title" content="{esc(t)}">', f'<meta property="og:image" content="{esc(img)}">',
                  '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:image" content="{esc(img)}">']
    else:
        url = SITE + p
        translated = all(os.path.exists(f'{l}/{base}') for l in LANGS)
        en = BeautifulSoup(open(base, encoding='utf8').read(), 'html.parser') if lang != 'en' and os.path.exists(base) else None
        en_title = en.title.get_text(strip=True) if en and en.title else None
        t = fit_title(soup.title.get_text() if soup.title else base.replace('_', ' ').replace('.html', ''), en_title, lang)
        dm = soup.find('meta', attrs={'name': 'description'}); d = dm.get('content', '') if dm else ''
        en_d = ((en.find('meta', attrs={'name': 'description'}) or {}).get('content', '') if en else '')
        hero = soup.select_one('.page-hero-content p, .hub-hero p, .pr-hero p, header p')
        extra = [x.get_text(' ', strip=True) for x in ([hero] if hero else []) + soup.select('.impact-box p, main p, section p')[:4]]
        extra = [e for e in extra if e and not e.startswith(('Image', 'Source', 'Image :', 'Imagen', 'الصورة'))]
        if lang != 'en' and (not d or d.strip() == en_d.strip()): d = extra[0] if extra else PAD[lang]
        d = fit_desc(d or (extra[0] if extra else PAD[lang]), extra, lang)
        img = (soup.find('meta', property='og:image') or {}).get('content') or SITE + 'assets/og-default.jpg'
        if not img.startswith('http'): img = SITE + img.lstrip('./')
        card = (soup.find('meta', attrs={'name': 'twitter:card'}) or {}).get('content') or 'summary_large_image'
        ogtype = (soup.find('meta', property='og:type') or {}).get('content') or 'website'
        block = [f'<meta name="robots" content="index,follow">', f'<link rel="canonical" href="{url}">']
        block += [f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in [('en', SITE + base)] + ([(l, f'{SITE}{l}/{base}') for l in LANGS] if translated else []) + [('x-default', SITE + base)]]
        block += [f'<title>{esc(t)}</title>', f'<meta name="description" content="{esc(d)}">',
                  f'<meta property="og:title" content="{esc(t)}">', f'<meta property="og:description" content="{esc(d)}">',
                  f'<meta property="og:image" content="{esc(img)}">', f'<meta property="og:url" content="{url}">',
                  f'<meta property="og:type" content="{ogtype}">', f'<meta property="og:site_name" content="Saving Planets">',
                  f'<meta property="og:locale" content="{LOCALE[lang]}">']
        if translated: block += [f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in ['en'] + LANGS if l != lang]
        block += [f'<meta name="twitter:card" content="{card}">', f'<meta name="twitter:title" content="{esc(t)}">',
                  f'<meta name="twitter:description" content="{esc(d)}">', f'<meta name="twitter:image" content="{esc(img)}">']
        # JSON-LD
        pub, mod = gitdates(base); have = []
        def ld(m):
            try: j = json.loads(m.group(1))
            except Exception: return m.group(0)
            typ = j.get('@type'); have.append(typ)
            if typ in ('Article', 'WebPage', 'CollectionPage'):
                j['inLanguage'] = lang
                j['headline' if typ == 'Article' else 'name'] = t.replace(BRAND, '').replace(TAG.get(lang, '@@'), '')
                j['description'] = d; j['url'] = url
                if typ == 'Article': j['mainEntityOfPage'] = url
                j['datePublished'] = j.get('datePublished') or pub or mod
                j['dateModified'] = max(filter(None, [j.get('dateModified'), mod, j['datePublished']]))
            elif typ == 'WebSite':
                j['inLanguage'] = lang; j['url'] = SITE
                j['potentialAction'] = {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + ('' if lang == 'en' else lang + '/') + 'Search.html?q={search_term_string}'}, 'query-input': 'required name=search_term_string'}
            return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
        head = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, head, flags=re.S)
        if base != 'index.html' and not ({'Article', 'WebPage', 'CollectionPage'} & set(have)):
            j = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': t.replace(BRAND, '').replace(TAG.get(lang, '@@'), ''), 'description': d, 'url': url,
                 'inLanguage': lang, 'datePublished': pub, 'dateModified': mod or pub, 'isPartOf': {'@type': 'WebSite', 'name': 'Saving Planets', 'url': SITE}}
            head += '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>\n'
    m = re.search(r'<meta name="viewport"[^>]*>|<meta content="[^"]*" name="viewport"/?>', head) or re.search(r'<meta charset[^>]*>', head)
    pos = m.end() if m else head.index('<head>') + 6
    head = head[:pos] + '\n' + '\n'.join(block) + head[pos:]
    # images: width/height from local file, lazy + async decoding
    def im(mt):
        tag = mt.group(0)
        sm = re.search(r'\ssrc="([^"]*)"', tag); srcv = sm.group(1) if sm else ''
        add = ''
        if not (re.search(r'\swidth=', tag) and re.search(r'\sheight=', tag)) and srcv and not srcv.startswith(('http', 'data:')):
            f = os.path.normpath(os.path.join(os.path.dirname(p), srcv.split('?')[0]))
            if os.path.exists(f):
                try:
                    from PIL import Image
                    with Image.open(f) as I: add += f' width="{I.width}" height="{I.height}"'
                except Exception: pass
        if 'fetchpriority="high"' not in tag and 'loading=' not in tag: add += ' loading="lazy"'
        if 'decoding=' not in tag: add += ' decoding="async"'
        return tag[:4] + add + tag[4:] if add else tag
    rest = re.sub(r'<img\b[^>]*>', im, rest)
    out = head + rest
    if out != raw: open(p, 'w', encoding='utf8').write(out); return True
    return False

def run(langs):
    n = 0
    for l in langs:
        files = sorted(glob.glob('*.html')) if l == 'en' else sorted(glob.glob(f'{l}/*.html')) ; files = [f for f in files if not re.match(r'google[0-9a-f]+\.html$', os.path.basename(f))]
        n += sum(fix(f) for f in files)
    import importlib.util  # structured-data enrichment (Article/CollectionPage/DefinedTermSet/...; Oct 13)
    sp = importlib.util.spec_from_file_location('seojsonld', 'scripts/seo-jsonld.py'); sj = importlib.util.module_from_spec(sp); sp.loader.exec_module(sj)
    sj.run(langs)
    return n

if __name__ == '__main__':
    print('seo-fix: updated', run(sys.argv[1:] or ['en'] + LANGS), 'pages')
