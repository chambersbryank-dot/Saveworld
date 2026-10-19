#!/usr/bin/env python3
"""Generate /fr/, /es/, /ar/, /it/ translations of the pages in PAGES from the English originals.
Translations live in i18n/<lang>.json (English string -> translation; missing = English kept).
Run from repo root:  python3 scripts/i18n-build.py   then  node scripts/i18n-check.js
Needs: pip install beautifulsoup4"""
import json, re, os, hashlib, sys
from bs4 import BeautifulSoup, Comment

SITE = 'https://www.savingplanets.com/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import langs as L10N  # Oct 17: shared language lists + HE_PUBLIC launch switch (scripts/langs.py)
LANGS = L10N.BUILD          # languages built (incl. Hebrew)
PUBLIC = L10N.PUBLIC        # languages linked (switcher, hreflang); Hebrew only once L10N.HE_PUBLIC is True
CUR_PAGES = None            # pages being built for the current language (Hebrew: i18n/he-pages.txt only)
PAGES = [l.strip() for l in open('i18n/pages.txt', encoding='utf8') if l.strip() and not l.startswith('#')]  # pages to translate
LABEL = {'en': 'EN', 'fr': 'FR', 'es': 'ES', 'ar': 'العربية', 'it': 'IT', 'he': 'עברית'}
LANGNAME = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية', 'it': 'Italiano', 'he': 'עברית'}
SWITCH_ARIA = {'en': 'Language', 'fr': 'Langue', 'es': 'Idioma', 'ar': 'اللغة', 'it': 'Lingua', 'he': 'שפה'}
ATTRS = ('alt', 'aria-label', 'title', 'data-title', 'data-image-alt', 'placeholder', 'data-status', 'data-arrival-label')
META = {'description', 'twitter:description', 'twitter:title', 'og:description', 'og:title'}
FFI = 'For Further Information: '

GL_RE = re.compile(r'<span class="gl"><button[^>]*>(.*?)</button><span class="gl-pop"[^>]*>.*?</span></span>', re.S)
def unglossary(src):
    """Strip glossary tap/hover markup (added after translation by scripts/build-batch-b.py --glossary)."""
    return GL_RE.sub(r'\1', src)

def normalize(src):
    """English source minus parts that change for site-wide/nav reasons (kept in sync with scripts/i18n-check.js)."""
    src = unglossary(src)
    src = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', src)
    src = re.sub(r'<!-- PROJECT-R-MENU:START -->[\s\S]*?<!-- PROJECT-R-MENU:END -->', '', src)
    src = re.sub(r'<!-- (LEARNLINK|SIHELPER|REPORTFORM|LICENSE|LICABOUT|CLSHARE|NLCALL|GROWNUPS|STARTHERE|EMBED|EMBEDMODE|STDTAGS|STDMAP|HEROTHEME|SPTOPIC|LCPPRE|KIDSP1|ANIMBAN):START -->[\s\S]*?<!-- \1:END -->', '', src)  # Oct 16: build-learn.py adds this per language
    src = re.sub(r'<!-- SOLUTIONS-MENU:START -->[\s\S]*?<!-- SOLUTIONS-MENU:END -->', '', src)
    src = re.sub(r'<nav id="topnav">[\s\S]*?</nav>', '', src)  # Oct 16: header nav regenerated per language by build-nav.py
    src = re.sub(r'<li class="lang-switch"[\s\S]*?</li>', '', src)
    src = re.sub(r'\?v=[0-9a-z]+', '', src)
    src = re.sub(r'<script type="application/ld\+json"[^>]*>[\s\S]*?</script>\n?', '', src)  # JSON-LD is regenerated per language (seo-fix / add-video-schema)
    src = re.sub(r'<!-- RELATED:START -->[\s\S]*?<!-- RELATED:END -->', '', src)  # Related Solutions block is regenerated from the semantic index
    return src

def src_hash(page):
    return hashlib.sha1(normalize(open(page, encoding='utf8').read()).encode('utf8')).hexdigest()[:12]

def switcher(page, cur, prefix):
    """Language switcher <li>. prefix = path from current page to site root ('' or '../')."""
    items = []
    for l in ['en'] + PUBLIC:
        if l == 'en':
            href = prefix + page
        else:
            href = prefix + l + '/' + (page if page in PAGES else 'Project-Rawane.html')
        a = f'<a href="{href}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == cur else '') + f' title="{LANGNAME[l]}">{LABEL[l]}</a>'
        items.append(a)
    return f'<li class="lang-switch" aria-label="{SWITCH_ARIA[cur]}">' + '<span aria-hidden="true"> · </span>'.join(items) + '</li>'

def hreflang_links(page):
    out = [f'<link rel="alternate" hreflang="en" href="{SITE}{page}">']
    out += [f'<link rel="alternate" hreflang="{l}" href="{SITE}{l}/{page}">' for l in PUBLIC]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{page}">')
    return '\n'.join(out)

# Templates: (regex on English, key in i18n/<lang>.json whose value contains {x}); {x} is translated if known.
PATTERNS = [(r'^(.+) \| Saving Planets$', '{x} | Saving Planets'),
            (r'^(.+) image$', '{x} image'), (r'^Image: (.+)$', 'Image: {x}'), (r'^Photo: (.+)$', 'Photo: {x}'),  # Oct 15: generic alts/credits
            (r'^Want to go deeper\? (.+) has the full story and the latest updates\.$', 'Want to go deeper? {x} has the full story and the latest updates.'),
            (r'^Learn more about (.+)$', 'Learn more about {x}'),
            (r'^(\d[\d,]*) Real Solutions Making a Difference Daily$', '{x} Real Solutions Making a Difference Daily'),  # Oct 18: Solutions title, live count
            (r"^Proof it's not too late: (\d[\d,]*) real, sourced solutions across (\d+) hubs, from ocean cleanups to Earth-observation satellites, making a difference daily\.$",
             "Proof it's not too late: {x} real, sourced solutions across {y} hubs, from ocean cleanups to Earth-observation satellites, making a difference daily."),
            (r'^Read more about (.+)$', 'Read more about {x}'),
            (r'^(.+): Mission Status$', '{x}: Mission Status'),
            (r"^The Five W's of (.+)$", "The Five W's of {x}"),
            (r'^What is (.+), and what problem does it help solve\?$', 'What is {x}, and what problem does it help solve?'),
            (r'^Who is behind (.+), and where does the work happen\?$', 'Who is behind {x}, and where does the work happen?'),
            (r'^How does (.+) help both people and nature\? Use one fact from this page\.$', 'How does {x} help both people and nature? Use one fact from this page.')]

def lookup(m, st):
    if st in m: return m[st]
    if st.startswith(FFI): return m.get(FFI, FFI) + st[len(FFI):]
    for rx, key in PATTERNS:
        g = re.match(rx, st)
        if g and key in m:
            x = g.group(1); t = m[key].replace('{x}', m.get(x, x))
            return t.replace('{y}', g.group(2)) if g.re.groups > 1 else t  # Oct 18: second number (hub count)
    return None

def tr(m, s):
    st = s.strip()
    if not st: return s
    if True:
        t = lookup(m, st)
        if t is None: return s
    lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
    return lead + t + trail

def fix_url(u):
    if not u or re.match(r'^(https?:|mailto:|tel:|#|/|data:|javascript:)', u): return u
    page = u.split('#')[0].split('?')[0]
    if page in (CUR_PAGES if CUR_PAGES is not None else PAGES): return u  # stay inside the language folder (Hebrew: only pages it has)
    return '../' + u

def localize_search(js, m):
    """Search.html inline index: translated titles; translated h1/intro of each page appended to the searchable text."""
    def ent(mt):
        title, url, text = mt.group(1), mt.group(2), mt.group(3)
        t_title = lookup(m, title.replace("\\'", "'")) or title
        extra = []
        if os.path.exists(url):
            sp = BeautifulSoup(open(url, encoding='utf8').read(), 'html.parser')
            for el in sp.select('h1, .page-hero-content p, .hub-hero p')[:3]:
                t = lookup(m, el.get_text(' ', strip=True))
                if t: extra.append(t)
        add = ' '.join([t_title] + extra).lower().replace('\\', ' ').replace("'", "\\'")
        return "{ title: '%s', url: '%s', text: '%s %s' }" % (t_title.replace("'", "\\'"), url, text, add)
    js = re.sub(r"\{ title: '((?:[^'\\]|\\.)*)', url: '([^']*)', text: '((?:[^'\\]|\\.)*)' \}", ent, js)
    return js.replace('return p.text.indexOf(q)', 'return p.text.toLowerCase().indexOf(q)')

def build(page, lang, m):
    raw = re.sub(r'<!-- (LEARNLINK|SIHELPER|REPORTFORM|LICENSE|LICABOUT|CLSHARE|NLCALL|GROWNUPS|STARTHERE|EMBED|EMBEDMODE|STDTAGS|STDMAP|HEROTHEME|SPTOPIC|LCPPRE|KIDSP1|ANIMBAN):START -->[\s\S]*?<!-- \1:END -->', '', unglossary(open(page, encoding='utf8').read()))  # Oct 16: re-added per language by build-learn.py
    soup = BeautifulSoup(raw, 'html.parser')
    html = soup.html
    html['lang'] = lang
    if L10N.is_rtl(lang): html['dir'] = 'rtl'
    for t in soup.find_all(string=True):
        if isinstance(t, Comment) or t.parent.name in ('script', 'style'): continue
        new = tr(m, str(t))
        if new != str(t): t.replace_with(new)
    for tag in soup.find_all(True):
        for a in ATTRS:
            if tag.get(a): tag[a] = tr(m, tag[a])
        if tag.name == 'meta' and (tag.get('name') in META or tag.get('property') in META) and tag.get('content'):
            tag['content'] = tr(m, tag['content'])
        if tag.get('data-milestones'):  # "ISO|label;ISO|label"
            tag['data-milestones'] = ';'.join((lambda p: p[0] + ('|' + tr(m, p[1]) if len(p) > 1 else ''))(x.split('|', 1)) for x in tag['data-milestones'].split(';'))
        for a in ('href', 'src', 'poster', 'data-image', 'data-fact-page'):
            if tag.get(a) and not (tag.name == 'link' and tag.get('rel') in (['canonical'], ['alternate'])):
                tag[a] = fix_url(tag[a])
        if tag.get('srcset'):  # Oct 14: responsive images (comma list of "url width")
            tag['srcset'] = ', '.join(' '.join([fix_url(p.split()[0])] + p.split()[1:]) for p in tag['srcset'].split(','))
    ui = json.load(open('i18n/ui.json', encoding='utf8')).get(lang, {})
    for s in soup.find_all('script'):
        if not s.get('src') and s.get('type') != 'application/ld+json' and s.string:
            js = s.string.replace("'assets/data/artemis.json'", f"'../assets/data/artemis.{lang}.json'")
            if page == 'Search.html': js = localize_search(js, m)  # per-language data (scripts/i18n-data.py); static translated cards are the fallback
            for en, t in ui.items(): js = js.replace(en, t)
            s.string = js
            continue
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
    public = lang in PUBLIC
    extra = BeautifulSoup((hreflang_links(page) if public else
                           f'<meta name="robots" content="noindex,nofollow">\n<link rel="preconnect" href="https://fonts.googleapis.com">'
                           f'\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@400;600;700;800&amp;display=swap">') + f'\n<meta name="i18n-source" content="{page} {src_hash(page)}">'
                          + f'\n<meta property="og:locale" content="{L10N.LOCALE[lang]}">', 'html.parser')
    (can.insert_after(extra) if can else head.append(extra))
    ul = soup.select_one('nav#topnav ul.nav-links')
    if ul and public: ul.append(BeautifulSoup(switcher(page, lang, '../'), 'html.parser'))
    if not public:  # Oct 17: unlinked language (Hebrew before review): no robots index line from the English copy, no hreflang
        for mt in soup.find_all('meta', attrs={'name': 'robots'}):
            if mt.get('content') != 'noindex,nofollow': mt.decompose()
    if lang == 'he':  # Hebrew font stack (Montserrat has no Hebrew glyphs)
        st = soup.new_tag('style'); st.string = 'html[lang=he] body,html[lang=he] h1,html[lang=he] h2,html[lang=he] h3,html[lang=he] .hero-welcome{font-family:"Noto Sans Hebrew",Heebo,"Arial Hebrew",Arial,system-ui,sans-serif}'
        head.append(st)
    # amazing-fact tags in translations must not be collected again: drop the class marker
    for p in soup.select('p.amazing-fact'):
        p['class'] = [c for c in p['class'] if c != 'amazing-fact'] + ['amazing-fact-i18n']
    out = str(soup)
    if not public:  # BeautifulSoup reorders attrs; re-assert name-first noindex while HE_PUBLIC is False
        out = L10N.ensure_hidden_robots(out)
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
    for page in (L10N.pages_for(lang, PAGES) if len(sys.argv) < 4 else sys.argv[3:]):  # optional page list: --missing he Page.html ...
        soup = BeautifulSoup(unglossary(open(page, encoding='utf8').read()), 'html.parser')  # Oct 16: same source build() translates (no glossary fragments)
        for li in soup.select('li.lang-switch, nav#topnav'): li.decompose()
        vals = [str(t).strip() for t in soup.find_all(string=True) if not isinstance(t, Comment) and t.parent.name not in ('script', 'style')
                and not (t.find_parent('a') and t.find_parent('a').get('href', '').startswith('http') and not str(t).strip().startswith(FFI))]
        vals += [tag[a].strip() for tag in soup.find_all(True) for a in ATTRS if tag.get(a)]
        vals += [x.split('|', 1)[1].strip() for tag in soup.find_all(attrs={'data-milestones': True}) for x in tag['data-milestones'].split(';') if '|' in x]
        vals += [t['content'].strip() for t in soup.find_all('meta') if (t.get('name') in META or t.get('property') in META) and t.get('content')]
        for v in vals:
            if v.startswith(FFI): v = FFI
            if v and re.search('[A-Za-z]{3}', v) and lookup(m, v) is None and v not in seen:
                seen.add(v); print(f'{page}\t{v}')

if __name__ == '__main__':
    if sys.argv[1:2] == ['--missing']:
        missing(sys.argv[2] if len(sys.argv) > 2 else 'fr'); sys.exit(0)
    langs = sys.argv[1:] or LANGS
    for page in PAGES: english_head(page)
    import importlib.util  # SEO pass on translations (titles/descriptions per language, og/hreflang/JSON-LD)
    spec = importlib.util.spec_from_file_location('seo', 'scripts/seo-fix.py'); seo = importlib.util.module_from_spec(spec); spec.loader.exec_module(seo)
    seo.run(['en'])  # finalize English first so the i18n-source hashes match the English that ships
    for lang in langs:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        CUR_PAGES = L10N.pages_for(lang, PAGES)
        for page in CUR_PAGES: build(page, lang, m)
        print(lang, 'built', len(CUR_PAGES), 'pages', '' if lang in PUBLIC else '(UNLINKED: noindex, not in switcher/hreflang/sitemap)')
    CUR_PAGES = None
    h0 = {p: src_hash(p) for p in PAGES}
    print('seo-fix:', seo.run(['en'] + [l for l in langs if l in PUBLIC]), 'pages updated')  # unlinked Hebrew stays out of seo-fix
    if not L10N.HE_PUBLIC and 'he' in langs:
        bad = L10N.assert_he_noindex()
        if bad: raise SystemExit('he noindex missing on %d pages (e.g. %s)' % (len(bad), bad[0]))
        print('he noindex: ok', len([x for x in os.listdir('he') if x.endswith('.html')]), 'pages')
    # Oct 16: a brand-new page's English changes once its translations exist (seo-fix adds the hreflang/alternate data it can
    # only see now), so its fresh i18n-source hashes went stale and the weekly-sync check failed on the first run. Rebuild just
    # those pages against the final English, then re-run the SEO pass once more.
    changed = [p for p in PAGES if src_hash(p) != h0[p]]
    if changed:
        for lang in langs:
            m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
            CUR_PAGES = L10N.pages_for(lang, PAGES)
            for page in changed:
                if page in CUR_PAGES: build(page, lang, m)
        CUR_PAGES = None
        print('re-stamped after final seo-fix:', ', '.join(changed), '| seo-fix:', seo.run(['en'] + [l for l in langs if l in PUBLIC]), 'pages updated')
