#!/usr/bin/env python3
"""Topic keywords for every HTML page, taken only from that page's own title, heading, and description.

Nothing is invented. A word is kept only when it already appears in the title, the h1/h2, or the meta
description (or, when those are missing, the first visible sentence). Idempotent.
Also fills a missing description, canonical, and Twitter/OG title on pages that already have a real title
(404, the offline page, the private study pages, and the noindex redirects).
"""
import glob, html, os, re, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://www.savingplanets.com/'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
STOP = {
 'en': set('a an the of and or to in on for with from by at is are was were it its their they this that as be has have not into across our your about than then also more most some any each per via'.split()),
 'fr': set('les des une un et ou dans pour avec sur par que qui est sont aux du au en ce cette pas plus son ses leur leurs dans une'.split()),
 'es': set('el la los las un una de del y o en con por para que es son una al lo su sus como más mas'.split()),
 'it': set('il lo la i gli le un una di del della dei e o in con per che è sono dal sui sul come più non'.split()),
 'ar': set('في من على إلى هذا هذه التي الذي أو عن مع هو هي أن كان لم قد كل'.split()),
 'he': set('של על עם את זה לא גם או כי אם הם הן אני הוא היא אל מן'.split()),
}

def lang_of(p):
    if p.startswith('study/'): return 'en'
    return p.split('/')[0] if '/' in p else 'en'

def page_url(p):
    if p == 'index.html': return SITE
    if p.endswith('/index.html'): return SITE + p[:-len('index.html')]
    return SITE + p

def unescape(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    s = re.sub(r'([A-Za-z])(?=[\u0590-\u05FF\u0600-\u06FF])', r'\1 ', s)
    s = re.sub(r'([\u0590-\u05FF\u0600-\u06FF])(?=[A-Za-z])', r'\1 ', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()

def core_title(title):
    t = unescape(title)
    t = re.sub(r'\s*[|·–—-]\s*Saving Planets\s*$', '', t).strip()
    return t

def words(s):
    return re.findall(r"[\w''’-]+", s or '', flags=re.U)

VERBS = set('removes remove removed intercepts intercept caught catch helps help uses using make makes making working works worked provides provide providing includes include including based across through during after before about this that your you page pages head home find search link links already still reopen saved device reconnect browse mistyped printable every sheet sheets summary sources three discussion questions opened looking marchent'.split())

def keywords_from(title, heading, desc, lang):
    """Comma list. Every item is a phrase or word already written on the page."""
    items = []
    def add(phrase):
        phrase = re.sub(r'\s+', ' ', phrase).strip(' ,.;:|·–—-')
        if len(phrase) < 2 or len(phrase) > 70: return
        if phrase.casefold() in ('saving planets', 'home', '404'): return
        if any(x.casefold() == phrase.casefold() for x in items): return
        items.append(phrase)
    ct = core_title(title)
    add(ct)
    hd = unescape(heading)
    def overlap(a, b):
        wa = {w.casefold() for w in words(a)}; wb = {w.casefold() for w in words(b)}
        if not wa or not wb: return 0
        return len(wa & wb) / min(len(wa), len(wb))
    if hd and hd.casefold() != ct.casefold() and overlap(hd, ct) < 0.6:
        add(hd)
    have = {w.casefold() for w in words(ct + ' ' + hd)}
    stop = STOP.get(lang, set()) | STOP['en'] | VERBS | {'saving', 'planets'}
    for w in words(unescape(desc)):
        wl = w.casefold().strip("'’-")
        if "'" in w or "’" in w or "׳" in w: continue
        if len(wl) < 5 or wl in stop or wl in have or wl.isdigit(): continue
        if not re.search(r'\w', wl): continue
        add(w)
        have.add(wl)
        if len(items) >= 8: break
    out, n = [], 0
    for it in items:
        if n and n + len(it) + 2 > 200: break
        out.append(it); n += len(it) + 2
        if len(out) >= 8: break
    return ', '.join(out)

def first_sentence(raw):
    m = re.search(r'<section class="nf-wrap"[^>]*>.*?<p>(.*?)</p>', raw, re.S)
    if not m:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
    if not m: return ''
    return unescape(re.sub(r'<[^>]+>', '', m.group(1)))

def esc(v):
    return (v.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;'))

def upsert_meta(head, name, content):
    """Insert or replace a name= meta tag. Returns head."""
    tag = f'<meta name="{name}" content="{esc(content)}">'
    rx = re.compile(rf'<meta[^>]*name="{name}"[^>]*>', re.I)
    if rx.search(head):
        return rx.sub(tag, head, count=1)
    # place after description, else after title
    m = re.search(r'<meta[^>]*name="description"[^>]*>', head, re.I)
    if not m:
        m = re.search(r'</title>', head, re.I)
    if not m: return head
    return head[:m.end()] + tag + head[m.end():]

def ensure(raw, path):
    if 'http-equiv="refresh"' in raw.split('</head>', 1)[0] and '<title>' not in raw:
        return raw
    if '</head>' not in raw or '<title>' not in raw: return raw
    head, rest = raw.split('</head>', 1)
    title_m = re.search(r'<title>(.*?)</title>', head, re.S)
    if not title_m: return raw
    title = unescape(re.sub(r'<[^>]+>', '', title_m.group(1)))
    h = re.search(r'<h1[^>]*>(.*?)</h1>', rest, re.S) or re.search(r'<h2[^>]*>(.*?)</h2>', rest, re.S)
    heading = unescape(re.sub(r'<[^>]+>', ' ', h.group(1))) if h else ''
    if not heading:
        a = re.search(r'<a [^>]*>(.*?)</a>', rest, re.S)
        if a: heading = unescape(re.sub(r'<[^>]+>', ' ', a.group(1)))
    dm = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', head, re.I)
    if not dm:
        dm = re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"', head, re.I)
    desc = unescape(dm.group(1)) if dm else ''
    if not desc:
        desc = re.sub(r'<[^>]+>', ' ', first_sentence(raw))
        desc = unescape(desc)
        if desc:
            head = upsert_meta(head, 'description', desc)
            if 'property="og:description"' not in head:
                head = head.replace('</title>', '</title>' + f'<meta property="og:description" content="{esc(desc)}">', 1)
            if 'name="twitter:description"' not in head:
                head = upsert_meta(head, 'twitter:description', desc)
    if 'name="twitter:title"' not in head:
        head = upsert_meta(head, 'twitter:title', title)
    if 'rel="canonical"' not in head and 'http-equiv="refresh"' not in head:
        head = head.replace('</title>', '</title>' + f'<link rel="canonical" href="{page_url(path)}">', 1)
    if 'property="og:url"' not in head and 'http-equiv="refresh"' not in head:
        head = head.replace('</title>', '</title>' + f'<meta property="og:url" content="{page_url(path)}">', 1)
    lang = lang_of(path)
    kw = keywords_from(title, heading, desc or title, lang)
    if kw:
        head = upsert_meta(head, 'keywords', kw)
    if 'application/ld+json' not in head and 'http-equiv="refresh"' not in head and os.path.basename(path) != 'googlea5d3cc0c785fec04.html':
        import json
        name = core_title(title) or title
        ld = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': name,
              'description': desc or name, 'url': page_url(path), 'inLanguage': lang}
        head += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n'
    return head + '</head>' + rest

def pages():
    out = []
    for l in LANGS:
        out += sorted(glob.glob('*.html' if l == 'en' else f'{l}/*.html'))
    out += sorted(glob.glob('study/*.html'))
    return [p for p in out if not re.match(r'(?:.*/)?google[0-9a-f]+\.html$', p)]

def main():
    n = 0
    for p in pages():
        raw = open(p, encoding='utf8').read()
        nxt = ensure(raw, p)
        if nxt != raw:
            open(p, 'w', encoding='utf8').write(nxt); n += 1
    print('seo-keywords:', n, 'pages')

if __name__ == '__main__':
    main()
