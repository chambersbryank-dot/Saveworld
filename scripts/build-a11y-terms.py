#!/usr/bin/env python3
"""Oct 28 2026 (founder-approved, directory prep): Accessibility statement + Terms of Use pages, and the home-page Standards Alignment block.
  python3 scripts/build-a11y-terms.py          EN pages (Press.html template, like build-trust.py) + fr/es/ar/it/he strings in i18n/<lang>.json,
                                               pages.txt + he-pages.txt + sitemap. Run BEFORE build-site-extras/i18n-build (footer links come from KEY there).
  python3 scripts/build-a11y-terms.py --home   Standards block + educationalAlignment JSON-LD on index.html in all 6 langs (AFTER i18n-build).
Text: scripts/a11y_terms_text.py. Codes: assets/data/standards.json only. Idempotent."""
import re, html, json, os, sys, importlib.util
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
spec = importlib.util.spec_from_file_location('t', 'scripts/a11y_terms_text.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
E = lambda s, quote=True: html.escape(html.unescape(s), quote=quote)

def home():
    STD = json.load(open('assets/data/standards.json', encoding='utf8'))['codes']
    fw = lambda c: ('Common Core State Standards', 'CCSS') if c.startswith('CCSS') else ('Next Generation Science Standards', 'NGSS')
    align = [{'@type': 'AlignmentObject', 'alignmentType': 'educationalSubject', 'educationalFramework': fw(c)[0], 'targetName': c.replace('CCSS.ELA-LITERACY.', 'CCSS.ELA-Literacy.'), 'targetUrl': v['url']} for c, v in STD.items()]
    align += [{'@type': 'AlignmentObject', 'alignmentType': 'educationalLevel', 'educationalFramework': 'US grade bands', 'targetName': 'Grades ' + b} for b in ('K-2', '3-5', '6-8', '9-12')]
    for i, l in enumerate(LANGS):
        f = ('' if l == 'en' else l + '/') + 'index.html'
        s = open(f, encoding='utf8').read()
        s2 = re.sub(r'<!-- HOMESTD:START -->.*?<!-- HOMESTD:END -->', '', s, flags=re.S)
        H = {k: E(v[i]) for k, v in C.HOME.items()}
        lis = ''.join(f'<li>{H[k]}</li>' for k in ('ESS3', 'ESS1', 'LS2', 'CCSS'))
        block = ('<!-- HOMESTD:START --><style>.home-std{max-width:960px;margin:2rem auto;padding:0 1rem}.home-std ul{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;padding:0;margin:.75rem 0}'
                 '.home-std li{border:1px solid currentColor;border-radius:999px;padding:.35rem .8rem;font-size:.95rem}</style>'
                 f'<section class="home-std" id="standards" aria-labelledby="std-h"><h2 id="std-h">{H["h"]}</h2><p>{H["p"]}</p><ul>{lis}</ul>'
                 f'<p>{H["bands"]} · <a href="Teachers.html">{H["link"]}</a></p></section>')
        ld = {'@context': 'https://schema.org', '@type': 'WebPage', 'url': 'https://www.savingplanets.com/' + ('' if l == 'en' else l + '/'), 'inLanguage': l,
              'audience': {'@type': 'EducationalAudience', 'educationalRole': 'teacher'}, 'educationalAlignment': align}
        block += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script><!-- HOMESTD:END -->'
        a = s2.find('<!-- AUDIENCE:END -->')
        if a < 0: print('skip (no AUDIENCE:END)', f); continue
        a += len('<!-- AUDIENCE:END -->'); s2 = s2[:a] + block + s2[a:]
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); print('home std', f)

def pages():
    TPL = open('Press.html', encoding='utf8').read(); FOOT = TPL[TPL.index('<footer>'):]
    TR = {l: {} for l in LANGS[1:]}
    def T(t):
        for i, l in enumerate(LANGS[1:], 1): TR[l][t[0]] = t[i]
        return t[0]
    def page(slug, i, h1, sub, body):
        # Template = the already post-processed Privacy page in the same language (nav, head, footer, RTL, analytics stay identical).
        d = '' if i == 0 else LANGS[i] + '/'
        tpl = open(d + 'Privacy.html', encoding='utf8').read()
        a, b = tpl.index('<section class="page-hero'), tpl.index('<footer>')
        ph1 = re.search(r'<h1[^>]*>(.*?)</h1>', tpl[a:b], re.S).group(1); psub = re.search(r'<p>(.*?)</p>', tpl[a:b], re.S).group(1)
        head = tpl[:a].replace('Privacy.html', slug + '.html')
        for old, new_ in ((ph1, E(h1)), (psub, E(sub)), (html.unescape(psub), sub), (html.unescape(ph1), h1)):
            head = head.replace(old, new_)
        head = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + E(sub) + '"', head)
        head = re.sub(r'"description": "[^"]*"', lambda m: '"description": ' + json.dumps(sub, ensure_ascii=False), head, count=1)
        head = re.sub(r'assets/og/en/Privacy\.jpg\?v=[0-9a-f]+', 'assets/og/en/index.jpg?v=97dc5720', head)
        head = re.sub(r'"datePublished": "[0-9-]+"', '"datePublished": "2026-10-28"', head); head = re.sub(r'"dateModified": "[0-9-]+"', '"dateModified": "2026-10-28"', head)
        foot = tpl[b:].replace('%2FPrivacy.html', '%2F' + slug + '.html')
        crumbs = f'<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">{E(C.FOOT[3][i])}</a></li><li><span aria-current="page">{E(h1)}</span></li></ol></nav>'
        mid = f'<section class="page-hero"><div class="page-hero-content"><h1>{E(h1)}</h1><p>{E(sub)}</p></div></section>\n' + crumbs + '\n' + body + '\n</main>\n'
        f = d + slug + '.html'; new = head + mid + foot
        if not os.path.exists(f) or open(f, encoding='utf8').read() != new: open(f, 'w', encoding='utf8').write(new); print('wrote', f)
    for slug, p in C.PAGES.items():
        for i in range(len(LANGS)):
            if i and not os.path.exists(LANGS[i] + '/Privacy.html'): continue
            L = lambda t: t[i]
            secs = ''.join(f'<section class="five-ws" id="s{k+1}"><h2>{E(L(h))}</h2>' + ''.join(f'<p>{E(L(x))}</p>' for x in ps) + '</section>' for k, (h, ps) in enumerate(p['sections']))
            links = ('<section class="help-actions" id="more"><p><a class="btn" href="Accessibility.html">' + E(L(C.FOOT[0])) + '</a> <a class="btn" href="Terms.html">' + E(L(C.FOOT[1])) +
                     '</a> <a class="btn" href="Privacy.html">' + E(L(C.FOOT[2])) + '</a></p></section>')
            page(slug, i, L(p['title']), L(p['sub']), '<p class="trust-updated">' + E(L(C.UPDATED)) + '</p>' + secs + links)
    # translation memory so a future i18n-build reproduces the same pages
    T(C.UPDATED); T(C.FOOT[3])
    for p in C.PAGES.values():
        T(p['title']); T(p['sub']); [T(h) or [T(x) for x in ps] for h, ps in p['sections']]
    for t in C.FOOT: T(t)
    for l, d in TR.items():
        f = f'i18n/{l}.json'; m = json.load(open(f, encoding='utf8')); ch = False
        for k, v in d.items():
            for kk in {k, E(k)}:
                if m.get(kk) != v: m[kk] = v; ch = True
        if ch: json.dump(m, open(f, 'w', encoding='utf8'), ensure_ascii=False, indent=0); print('i18n', l)
    for pf in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        pl = open(pf, encoding='utf8').read().split('\n'); add = [s + '.html' for s in ('Accessibility', 'Terms') if s + '.html' not in pl]
        if add: open(pf, 'a', encoding='utf8').write(('' if pl[-1] == '' else '\n') + '\n'.join(add) + '\n'); print(pf, '+', add)
    sm = open('sitemap.xml', encoding='utf8').read()
    for slug in ('Accessibility', 'Terms'):
        loc = f'<loc>https://www.savingplanets.com/{slug}.html</loc>'
        if loc not in sm: sm = sm.replace('</urlset>', f'  <url>{loc}<lastmod>2026-10-28</lastmod></url>\n</urlset>', 1)
    open('sitemap.xml', 'w', encoding='utf8').write(sm)

def footer_links():
    """Footer map on every page (6 langs): add Terms + Accessibility after Privacy (same order as build-site-extras KEY, so a later full sync is a no-op)."""
    import glob
    n = 0
    for i, l in enumerate(LANGS):
        for f in glob.glob(('' if i == 0 else l + '/') + '*.html'):
            s = open(f, encoding='utf8').read()
            m = re.search(r'<li><a href="Privacy.html">[^<]*</a></li>', s[s.find('<!-- FOOTER-MAP:START -->'):]) if '<!-- FOOTER-MAP:START -->' in s else None
            if not m or 'FOOTER-MAP' not in s or re.search(r'<!-- FOOTER-MAP:START -->.*href="Terms.html".*<!-- FOOTER-MAP:END -->', s, re.S): continue
            add = f'<li><a href="Terms.html">{E(C.FOOT[1][i])}</a></li><li><a href="Accessibility.html">{E(C.FOOT[0][i])}</a></li>'
            k = s.find('<!-- FOOTER-MAP:START -->') + m.end()
            s = s[:k] + add + s[k:]; open(f, 'w', encoding='utf8').write(s); n += 1
    print('footer links on', n, 'translated pages')

def footer_fallback():
    """Pages whose footer has no site map (home after build-home-trim, Search mini-footer, etc.): add a marked Terms + Accessibility line before </footer>. Idempotent."""
    import glob
    n = 0
    for i, l in enumerate(LANGS):
        for f in glob.glob(('' if i == 0 else l + '/') + '*.html'):
            s = open(f, encoding='utf8').read()
            s0 = re.sub(r'<!-- A11YTERMS-FOOT -->.*?<!-- /A11YTERMS-FOOT -->', '', s, flags=re.S)
            a = s0.rfind('<footer'); b = s0.find('</footer>', a)
            if a < 0 or b < 0: continue
            if 'href="Terms.html"' in s0[a:b] and 'href="Accessibility.html"' in s0[a:b]: s2 = s0
            else:
                add = (f'<!-- A11YTERMS-FOOT --><p class="footer-legal"><a href="Terms.html">{E(C.FOOT[1][i])}</a> · '
                       f'<a href="Accessibility.html">{E(C.FOOT[0][i])}</a></p><!-- /A11YTERMS-FOOT -->')
                s2 = s0[:b] + add + s0[b:]
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print('footer fallback on', n, 'pages')

if '--home' in sys.argv: home(); footer_fallback()
else: pages(); footer_links(); footer_fallback()
