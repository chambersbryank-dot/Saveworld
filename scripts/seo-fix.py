"""Idempotent SEO normalizer. Usage: python3 scripts/seo-fix.py [en|fr|es|ar|it ...]  (default: all)
Per page: meta robots, <=60-char localized title, 120-160-char localized description (og/twitter synced),
hand-written per-language title/description overrides from i18n/seo-meta.json (wins over generator text),
twitter:site, og:image width/height/type/alt, hreflang only for language versions that exist,
redirect stubs: html lang/dir + noindex (Oct 16 SEO pass; scripts/seo-lint.py checks the result).
canonical/og:url, hreflang set incl. x-default, og:locale(+alternates), JSON-LD dates/inLanguage, image
width/height/lazy. Run after build-stats.js and after scripts/i18n-build.py (which calls it for translations)."""
import glob, json, os, re, subprocess, sys
from bs4 import BeautifulSoup
import langs as L10N  # Oct 17: HE_PUBLIC — keep /he/ noindex while unlinked
SITE = 'https://www.savingplanets.com/'; LANGS = ['fr', 'es', 'ar', 'it']
NOINDEX = {'Project-R.html', '404.html'}
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR', 'it': 'it_IT'}
BRAND = ' | Saving Planets'
TWITTER_SITE = '@SISavingPlanets'
OVR = json.load(open('i18n/seo-meta.json', encoding='utf8')) if os.path.exists('i18n/seo-meta.json') else {}
# Oct 17: '{n}' in an override = live solution count (assets/data/solutions.json), so hand-written texts never go stale (fr Solutions said 142)
# Oct 18: '{h}' = live hub count (Polar made it 11; fr Solutions still said '10 pôles')
try: _SITE = json.load(open('assets/data/solutions.json', encoding='utf8'))['site']; _N, _H = str(_SITE['solutions']), str(_SITE['hubs'])
except Exception: _N = _H = None
if _N: OVR = json.loads(json.dumps(OVR, ensure_ascii=False).replace('{n}', _N).replace('{h}', _H))
MAIN_TYPES = ('Article', 'WebPage', 'CollectionPage', 'LearningResource', 'Course', 'DefinedTermSet', 'FAQPage', 'AboutPage', 'ContactPage', 'SearchResultsPage')
def page_url(lang, base):  # index.html is served at the directory URL
    return SITE + ('' if lang == 'en' else lang + '/') + ('' if base == 'index.html' else base)
def langs_of(base):  # languages that actually have this page
    return ['en'] + [l for l in LANGS if os.path.exists(f'{l}/{base}')] if os.path.exists(base) else [l for l in LANGS if os.path.exists(f'{l}/{base}')]
# Language tag added to translated titles that would otherwise equal the English title (proper names).
TAG = {'fr': ' · Français', 'es': ' · Español', 'ar': ' · بالعربية', 'it': ' · Italiano'}
# Learning pages (lessons, labs, calculators) get a pad that is true for them (no Five W's there)
PAD_LEARN = {'en': 'Free on Saving Planets, with no ads on learning pages.',
             'fr': 'Gratuit sur Saving Planets, sans publicité sur les pages d’apprentissage.',
             'es': 'Gratis en Saving Planets, sin anuncios en las páginas de aprendizaje.',
             'ar': 'مجاني على Saving Planets، بلا إعلانات في صفحات التعلّم.',
             'it': 'Gratis su Saving Planets, senza pubblicità nelle pagine di apprendimento.'}
UPDATED = re.compile(r'\s*(Last updated|Dernière mise à jour|Última actualización|Ultimo aggiornamento|آخر تحديث)\s*:?\s*[^.!?]*?\d{4}\.?')
PAD = {'en': 'Sourced facts, the Five W\'s and why it matters, on Saving Planets.',
       'fr': 'Faits sourcés, les cinq W et l\'impact, sur Saving Planets.',
       'es': 'Datos con fuentes, las cinco W y su impacto, en Saving Planets.',
       'ar': 'حقائق موثّقة والأسئلة الخمسة وأهمية الحل، على Saving Planets.',
       'it': 'Fatti con fonti, le cinque W e perché conta, su Saving Planets.'}
_END = re.compile(r'(?<=[.!?؟。])\s+')
_ABBR = re.compile(r'(?:\b[A-Z]\.|\b(?:[A-Z]\.){2,}|\b(?:e\.g|i\.e|Dr|St|Mt|No|vs|Inc|Ltd|Jr|Sr|Prof|approx|ca|av|apr|n°|Sra?|Sto|Ste|art|EE|UU)\.)$')
class _Splitter:
    """Sentence splitter that does not break after abbreviations (U.S., e.g., Dr., St.)."""
    def split(self, text):
        out = []
        for part in _END.split(text):
            if out and _ABBR.search(out[-1]): out[-1] += ' ' + part
            else: out.append(part)
        return out
END = _Splitter()
SKIP_P = re.compile(r'review|source|credit|cite|eyebrow|kicker|tag|crumb|share|caption|meta|note|disclaimer|lchip|badge|transcript|video|embed')
_git = {}
def gitdates(f):
    if f not in _git:
        out = subprocess.run(['git', 'log', '--follow', '--format=%as', '--', f], capture_output=True, text=True).stdout.split()
        today = __import__('datetime').date.today().isoformat()  # Oct 16: a new, not-yet-committed page has no git history -> date it today (was a max() crash)
        _git[f] = (out[-1], out[0]) if out else (today, today)
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
    for sep in (': ', ' (', ' – ', ' — ', ', ', ' : '):  # keep the head clause ("Delta-v Calculator (Tsiolkovsky…)" -> "Delta-v Calculator")
        head = core.split(sep)[0].strip()
        if 20 <= len(head) <= 60 and head != core:
            return head + BRAND if len(head + BRAND) <= 60 else head
    return core[:59].rsplit(' ', 1)[0].rstrip(' ,:;–-') + '…'

_STOP = set('a an the of and or to in on for with from by at is are was were it its their they this that as be has have not into across our your'.split())
def _words(x): return {w for w in re.findall(r"\w+", x.lower()) if len(w) > 2 and w not in _STOP}
def _dup(x, text):
    """Oct 16: a pad sentence that mostly repeats what the description already says ('Growing native forests from seed to canopy'
    after 'restores native forests from seed to canopy'), or a bare card label ('ESA (European Space Agency).'), adds nothing."""
    a, b = _words(x), _words(text)
    if len(x) < 35 or not a: return True
    return len(a & b) / len(a) >= 0.5

def fit_desc(base, extra, lang, learn=False):
    """Whole sentences, 120-160 chars. base sentence(s) first, then sentences from extra (page copy) that still fit,
    then the language pad. A description we truncated earlier (ends with an ellipsis) is rebuilt from the page copy.
    Ellipsis only when the first sentence alone is longer than 160."""
    norm = lambda x: re.sub(r'\s+', ' ', UPDATED.sub('', x or '')).strip()
    pad = (PAD_LEARN if learn else PAD)[lang]
    base = norm(base.replace(PAD[lang], '') if learn else base)
    if base.endswith('…') and len(base) <= 160: return base  # earlier cut whose full text is no longer on the page: keep it
    pool = [x for e in extra for x in END.split(norm(e)) if len(x) > 25 and not x.endswith('…')]
    sents = [x for x in END.split(base) if x] if base else []
    sents = [x for i, x in enumerate(sents) if i == 0 or not (len(_words(x)) >= 3 and len(_words(x) & _words(' '.join(sents[:i]))) / len(_words(x)) >= 0.6)]  # Oct 16: drop a repeated sentence
    if not sents and pool: sents = [pool.pop(0)]
    text = ''
    for x in sents:
        if len((text + ' ' + x).strip()) <= 160 or not text: text = (text + ' ' + x).strip()
        else: break
    if len(text) > 160:  # drop a trailing source attribution "(NASA)." before cutting
        t2 = re.sub(r'\s*\([^()]{2,60}\)(?=[.!?؟]?$)', '', text)
        if len(t2) <= 160: text = t2
        elif len(t2) <= 175 and len(sents) == 1 and t2[-1:] in '.!?؟': return t2  # one whole sentence a little over 160 (French/Spanish/Italian run longer) beats an ellipsis cut
    if len(text) > 160:  # a semicolon joins whole clauses: keep the clauses that fit, end with a full stop, re-pad
        parts = re.split(r'\s*[;؛]\s+', text)
        if len(parts) > 1:
            keep = ''
            for x in parts:
                cand = (keep + '; ' + x) if keep else x
                if len(cand) + 1 <= 160: keep = cand
                else: break
            if len(keep) >= 80:
                text = keep.rstrip(' ,.') + ('.' if lang != 'ar' else '.')
                for x in pool + [pad]:
                    if len(text) >= 120: break
                    if x not in text and (x == pad or not _dup(x, text)) and len(text) + 1 + len(x) <= 160: text = (text + ' ' + x).strip()
                return text
    if len(text) > 160:  # one long sentence: cut at a clause boundary, then a word boundary
        cut = text[:159]
        for sep in ('; ', ', ', ' – ', ' — ', ' ('):
            i = cut.rfind(sep)
            if i >= 110: return cut[:i].rstrip(' ,;:–—(') + '…'
        return cut.rsplit(' ', 1)[0].rstrip(' ,;:–—-') + '…'
    for x in pool + [pad]:
        if len(text) >= 120: break
        if x not in text and (x == pad or not _dup(x, text)) and len(text) + 1 + len(x) <= 160: text = (text + ' ' + x).strip()
    return text

def ptext(el):
    """Paragraph text without glossary pop-ups (.gl-pop), SI credits or screen-reader-only extras."""
    el = BeautifulSoup(str(el), 'html.parser')
    for x in el.select('.gl-pop, .si-credit, .sr-only, .visually-hidden, script, style'): x.decompose()
    return el.get_text(' ', strip=True)

def tidy(t, lang):
    """Undo get_text spacing at tag edges: no space before , . (and before ; : ! ? except in French typography)."""
    t = re.sub(r'\s+', ' ', t).strip()
    return re.sub(r'\s+([,.،])', r'\1', t) if lang == 'fr' else re.sub(r'\s+([,.;:!?،؛؟])', r'\1', t)

def hub_name(soup):
    """Second breadcrumb item (the hub, in the page language), e.g. 'Oceans' / 'Océans' / 'المحيطات'."""
    nav = soup.select_one('nav.breadcrumb')
    lis = nav.select('li') if nav else []
    return re.sub(r'\s+', ' ', lis[1].get_text(' ', strip=True)) if len(lis) >= 3 else None

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
    if 'http-equiv="refresh"' in raw:  # redirect stubs stay tiny: only html lang/dir + noindex (Oct 16)
        out = re.sub(r'<html[^>]*>', '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang in L10N.RTL else ''), raw, count=1)
        if not re.search(r'<meta name="robots"', out): out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="robots" content="noindex">', 1)
        if out != raw: open(p, 'w', encoding='utf8').write(out); return True
        return False
    src = raw
    src = re.sub(r'<html[^>]*>', lambda m: '<html lang="%s"%s class="dark">' % (lang, ' dir="rtl"' if lang in L10N.RTL else ''), src, count=1)
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
        url = page_url(lang, base)
        have_l = langs_of(base)
        translated = len(have_l) > 1
        ov = OVR.get(base, {}).get(lang, {})
        en = BeautifulSoup(open(base, encoding='utf8').read(), 'html.parser') if lang != 'en' and os.path.exists(base) else None
        en_title = en.title.get_text(strip=True) if en and en.title else None
        if ov.get('title'):  # hand-written (i18n/seo-meta.json): brand appended when it fits in 60
            t = ov['title'] if ov['title'].endswith(BRAND) or len(ov['title'] + BRAND) > 60 else ov['title'] + BRAND
        else:
            raw_t = soup.title.get_text() if soup.title else base.replace('_', ' ').replace('.html', '')
            core = re.sub(r'\s+', ' ', raw_t).replace(BRAND, '').replace(TAG.get(lang, '@@'), '').strip()
            en_core = (en_title or '').replace(BRAND, '').replace(TAG.get('en', '@@'), '').strip()
            hub = hub_name(soup)
            # Oct 16: English titles already carry ' – <English hub>' from an earlier seo-fix pass; i18n-build copies that
            # untranslated title into fr/es/ar/it, so strip it before re-adding the hub in the page language (idempotent).
            en_hub = hub_name(en) if en is not None else None
            if en_hub:
                sfx = f' – {en_hub}'
                if core.endswith(sfx): core = core[:-len(sfx)]; raw_t = core
                if en_core.endswith(sfx): en_core = en_core[:-len(sfx)]
                # Oct 16 fix: the English hub must also leave en_title, or fit_title() re-adds it with the language tag
                # ('NISAR (NASA–ISRO) – Earth Observation · Español'). Translated pages use their own breadcrumb hub.
                if en_title and lang != 'en':
                    en_title = en_title.replace(sfx + BRAND, BRAND)
                    if en_title.endswith(sfx): en_title = en_title[:-len(sfx)]
            if lang != 'en' and en_hub and hub == en_hub and core == en_core: hub = None  # untranslated breadcrumb: never put English in
            if hub and hub not in core and (len(core) < 30 or (lang != 'en' and core == en_core)) and len(f'{core} – {hub}{BRAND}') <= 60:
                t = f'{core} – {hub}{BRAND}'
            else: t = fit_title(raw_t if not (lang != 'en' and core == en_core) else en_title, en_title, lang)
        dm = soup.find('meta', attrs={'name': 'description'}); d = dm.get('content', '') if dm else ''
        en_d = ((en.find('meta', attrs={'name': 'description'}) or {}).get('content', '') if en else '')
        hero = soup.select_one('.page-hero-content p, .hub-hero p, .pr-hero p, header p')
        # Oct 15: never pad descriptions with image/video credits (the SI credit leaked into the Arabic homepage description)
        cands = [x for x in ([hero] if hero else []) + soup.select('.impact-box p, main p, section p')
                 if not any(SKIP_P.search(c) for c in (x.get('class') or [])) and not x.find_parent(class_=SKIP_P)
                 and not x.find_parent(['nav', 'footer', 'figure', 'aside', 'details'])][:6]
        extra = [tidy(ptext(x), lang) for x in cands]
        extra = [e for e in extra if 'Biological SI' not in e and 'SI Partner' not in e]
        extra = [e for e in extra if e and not e.startswith(('Image', 'Source', 'Image :', 'Imagen', 'الصورة'))]
        if lang != 'en' and (not d or d.strip() == en_d.strip()): d = extra[0] if extra else PAD[lang]
        if d.strip().endswith('…'):  # our earlier cut: restore the full sentence(s) from the page copy it came from
            key = lambda x: re.sub(r'[\s\u00a0\u202f]+', '', x.replace('’', "'").replace('«', '"').replace('»', '"'))
            stem = key(d.strip()[:-1])
            for x in [tidy(ptext(y), lang) for y in soup.select('main p, header p, section p, .page-hero-content p')]:
                if len(stem) > 25 and key(x).startswith(stem): d = x; break
            else:
                ss = END.split(re.sub(r'\s+', ' ', d.strip()))
                if len(ss) > 1: d = ' '.join(ss[:-1])  # keep the whole sentences, drop the cut one; fit_desc re-pads
        learn = bool(re.search(r'"@type": ?"(LearningResource|Course)"', raw)) or base.endswith('_Calculator.html')
        d = ov['description'].strip() if ov.get('description') else fit_desc(d or (extra[0] if extra else PAD[lang]), extra, lang, learn)
        img = (soup.find('meta', property='og:image') or {}).get('content') or SITE + 'assets/og-default.jpg'
        if not img.startswith('http'): img = SITE + img.lstrip('./')
        card = (soup.find('meta', attrs={'name': 'twitter:card'}) or {}).get('content') or 'summary_large_image'
        ogtype = (soup.find('meta', property='og:type') or {}).get('content') or 'website'
        rob = 'noindex,nofollow' if (lang == 'he' and not L10N.HE_PUBLIC) else 'index,follow'
        block = [f'<meta name="robots" content="{rob}">', f'<link rel="canonical" href="{url}">']
        block += [f'<link rel="alternate" hreflang="{h}" href="{page_url(h, base)}">' for h in have_l] + ([f'<link rel="alternate" hreflang="x-default" href="{page_url("en", base)}">'] if 'en' in have_l else [])
        iw = ih = None; lf = img[len(SITE):].split('?')[0] if img.startswith(SITE) else None
        if lf and os.path.exists(lf):
            try:
                from PIL import Image
                with Image.open(lf) as I: iw, ih = I.width, I.height
            except Exception: pass
        block += [f'<title>{esc(t)}</title>', f'<meta name="description" content="{esc(d)}">',
                  f'<meta property="og:title" content="{esc(t)}">', f'<meta property="og:description" content="{esc(d)}">',
                  f'<meta property="og:image" content="{esc(img)}">']
        if iw: block += [f'<meta property="og:image:width" content="{iw}">', f'<meta property="og:image:height" content="{ih}">',
                         f'<meta property="og:image:type" content="image/{"png" if lf.endswith(".png") else "webp" if lf.endswith(".webp") else "jpeg"}">']
        block += [f'<meta property="og:image:alt" content="{esc(t.replace(BRAND, ""))}">', f'<meta property="og:url" content="{url}">',
                  f'<meta property="og:type" content="{ogtype}">', f'<meta property="og:site_name" content="Saving Planets">',
                  f'<meta property="og:locale" content="{LOCALE[lang]}">']
        block += [f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in have_l if l != lang]
        block += [f'<meta name="twitter:card" content="{card}">', f'<meta name="twitter:site" content="{TWITTER_SITE}">', f'<meta name="twitter:title" content="{esc(t)}">',
                  f'<meta name="twitter:description" content="{esc(d)}">', f'<meta name="twitter:image" content="{esc(img)}">']
        # JSON-LD
        pub, mod = gitdates(base); have = []
        h1e = soup.find('h1'); h1 = re.sub(r'\s+', ' ', h1e.get_text(' ', strip=True)) if h1e else ''
        if len(h1) > 110: h1 = ''
        def ld(m):
            try: j = json.loads(m.group(1))
            except Exception: return m.group(0)
            typ = j.get('@type'); have.append(typ)
            if typ in MAIN_TYPES and typ not in ('DefinedTermSet', 'FAQPage'):
                j['inLanguage'] = lang
                if typ == 'Article' or typ in ('Article', 'WebPage', 'CollectionPage') or not j.get('name'):
                    j['headline' if typ == 'Article' else 'name'] = h1 or t.replace(BRAND, '').replace(TAG.get(lang, '@@'), '')
                j['description'] = d; j['url'] = url
                if typ == 'Article': j['mainEntityOfPage'] = url
                j['datePublished'] = j.get('datePublished') or pub or mod
                j['dateModified'] = max(filter(None, [j.get('dateModified'), mod, j['datePublished']]))
            elif typ == 'WebSite':
                j['inLanguage'] = lang; j['url'] = SITE
                j['potentialAction'] = {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + ('' if lang == 'en' else lang + '/') + 'Search.html?q={search_term_string}'}, 'query-input': 'required name=search_term_string'}
            return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
        head = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, head, flags=re.S)
        if base != 'index.html' and not (set(MAIN_TYPES) & set(have)):
            j = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': h1 or t.replace(BRAND, '').replace(TAG.get(lang, '@@'), ''), 'description': d, 'url': url,
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
