#!/usr/bin/env python3
"""Bring indexable titles to about 60 characters and descriptions to about 155.

Titles drop a trailing brand or hub only when the remaining words still name the page.
Descriptions keep whole sentences already on the page. The Earth Satellite Explorer
translations already live in scripts/build-satellite-levels.py; those pages use them
instead of the English paragraph. Idempotent.
"""
import html, json, os, re, glob, importlib.util
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CAP = 155
TITLE = 60
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
spec = importlib.util.spec_from_file_location('sat', 'scripts/build-satellite-levels.py')
sat = importlib.util.module_from_spec(spec); spec.loader.exec_module(sat)
LEAD_KEY = next(k for k in sat.T if k.startswith('Pick a level'))
ORDER = ['fr', 'es', 'ar', 'it', 'he']

def unescape(s):
    return html.unescape(s or '')

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

_ABBR = re.compile(r'(?:\b[A-Z]\.|\b(?:[A-Z]\.){2,}|\b(?:e\.g|i\.e|Dr|St|Mt|No|vs|Inc|Ltd|Jr|Sr|Prof|U\.S|U\.K)\.)$')
def sentences(text):
    parts = re.split(r'(?<=[.!?؟。])\s+', text.strip())
    out = []
    for part in parts:
        if out and _ABBR.search(out[-1]):
            out[-1] += ' ' + part
        else:
            out.append(part.strip())
    return [p for p in out if p]

def shorten_desc(d):
    d = re.sub(r'\s+', ' ', unescape(d)).strip()
    if d.endswith('…'):
        d = d[:-1].rsplit(' ', 1)[0].rstrip(' ,;')
    whole = sentences(d)
    # One complete sentence a little past 155 stays whole. Cutting it would drop the point.
    if len(whole) == 1 and len(whole[0]) <= CAP + 10 and whole[0][-1:] in '.!?؟':
        return whole[0]
    if len(d) <= CAP and d and d[-1:] in '.!?؟':
        return d
    out = ''
    for s in sentences(d):
        if s[-1:] not in '.!?؟' and out:
            break
        cand = (out + ' ' + s).strip()
        if len(cand) <= CAP:
            out = cand
        else:
            break
    if len(out) >= 80:
        return out
    text = sentences(d)[0] if sentences(d) else d
    if len(text) <= CAP:
        return text if text[-1:] in '.!?؟' else text
    cut = text[:CAP - 1]
    for sep in ('; ', ', ', ' — ', ' – ', ' '):
        i = cut.rfind(sep)
        if i >= 90:
            piece = cut[:i].rstrip(' ,;:–—')
            if piece[-1:] not in '.!?؟':
                piece += '.'
            if len(piece) <= CAP:
                return piece
    return cut.rsplit(' ', 1)[0].rstrip(' ,;') + '.'

def shorten_title(t):
    t = re.sub(r'\s+', ' ', unescape(t)).strip()
    if len(t) <= TITLE and not t.endswith('…'):
        return t
    core = re.sub(r'\s*\|\s*Saving Planets(?:\s*·\s*.+)?\s*$', '', t).strip()
    core = re.sub(r'\s*·\s*(Français|Español|Italiano|بالعربية|עברית)\s*$', '', core).strip()
    if t.endswith('…'):
        core = core[:-1].rsplit(' ', 1)[0].rstrip(' ,;')
    if 12 <= len(core) <= TITLE:
        return core + (' | Saving Planets' if len(core) + 19 <= TITLE else '')
    for sep in (' – ', ' — ', ': ', ' | '):
        head = core.split(sep)[0].strip()
        if 12 <= len(head) <= TITLE:
            return head + (' | Saving Planets' if len(head) + 19 <= TITLE else '')
    return core[:TITLE].rsplit(' ', 1)[0].rstrip(' ,;|–—-')

def pages():
    out = []
    for l in LANGS:
        out += sorted(glob.glob('*.html' if l == 'en' else f'{l}/*.html'))
    return [p for p in out if not re.match(r'(?:.*/)?google[0-9a-f]+\.html$', p)]

def indexable(head):
    if 'http-equiv="refresh"' in head: return False
    m = re.search(r'name="robots"[^>]*content="([^"]*)"', head) or re.search(r'content="([^"]*)"[^>]*name="robots"', head)
    return not (m and 'noindex' in m.group(1).lower())

def attr(head, name=None, prop=None):
    if name:
        m = re.search(rf'<meta[^>]*name="{name}"[^>]*>', head, re.I)
    else:
        m = re.search(rf'<meta[^>]*property="{prop}"[^>]*>', head, re.I)
    if not m: return '', None
    c = re.search(r'content="([^"]*)"', m.group(0))
    return (unescape(c.group(1)) if c else ''), m

def set_content(tag, new):
    return re.sub(r'content="[^"]*"', 'content="' + esc(new) + '"', tag, count=1)

def apply(raw, path):
    if '</head>' not in raw: return raw, None
    head, rest = raw.split('</head>', 1)
    if not indexable(head): return raw, None
    tm = re.search(r'<title>(.*?)</title>', head, re.S)
    if not tm: return raw, None
    old_t = unescape(re.sub(r'<[^>]+>', '', tm.group(1)))
    old_d, dm = attr(head, name='description')
    new_t, new_d = old_t, old_d
    lang = path.split('/')[0] if '/' in path else 'en'
    if os.path.basename(path) == 'Earth_Satellite_Explorer.html' and lang in ORDER:
        i = ORDER.index(lang)
        full = sat.T[LEAD_KEY][i]
        first = sentences(full)[0]
        new_d = first if len(first) <= CAP else shorten_desc(full)
        straight = LEAD_KEY.replace('’', "'").replace('‘', "'")
        rest = rest.replace(straight, full)
        head = head.replace(esc(straight), esc(full))
        name = sat.LINK[lang][0]
        titled = name + ' | Saving Planets'
        new_t = titled if len(titled) <= TITLE else name
        old_d, dm = attr(head, name='description')
    else:
        if len(old_t) > TITLE or old_t.endswith('…'):
            new_t = shorten_title(old_t)
        if old_d and (len(old_d) > CAP or old_d.endswith('…')):
            new_d = shorten_desc(old_d)
    changed = False
    if new_t != old_t:
        head = head.replace(tm.group(0), '<title>' + esc(new_t) + '</title>', 1)
        for prop in ('og:title', 'twitter:title'):
            kind = 'property' if prop.startswith('og:') else 'name'
            bit, m = attr(head, prop=prop) if kind == 'property' else attr(head, name=prop)
            if m and unescape(re.search(r'content="([^"]*)"', m.group(0)).group(1)) == old_t:
                head = head.replace(m.group(0), set_content(m.group(0), new_t), 1)
        changed = True
    if new_d and new_d != old_d:
        if dm:
            head = head.replace(dm.group(0), set_content(dm.group(0), new_d), 1)
        for prop, kind in (('og:description', 'property'), ('twitter:description', 'name')):
            bit, m = (attr(head, prop=prop) if kind == 'property' else attr(head, name=prop))
            if m and bit == old_d:
                head = head.replace(m.group(0), set_content(m.group(0), new_d), 1)
        def ld(m):
            block = m.group(0)
            try:
                j = json.loads(re.search(r'>(.*)<', block, re.S).group(1))
            except Exception:
                return block
            if j.get('description') == old_d:
                j['description'] = new_d
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
            return block
        head = re.sub(r'<script type="application/ld\+json">.*?</script>', ld, head, flags=re.S)
        changed = True
    out = head + '</head>' + rest
    return (out, (path, old_t, new_t, len(old_d or ''), len(new_d or ''))) if changed and out != raw else (raw, None)

def main():
    titles, descs = {}, {}
    plans = []
    files = {}
    for p in pages():
        raw = open(p, encoding='utf8').read()
        nxt, info = apply(raw, p)
        files[p] = nxt
        head = nxt.split('</head>', 1)[0]
        if not indexable(head): continue
        tm = re.search(r'<title>(.*?)</title>', head, re.S)
        title = unescape(re.sub(r'<[^>]+>', '', tm.group(1))) if tm else ''
        d, _ = attr(head, name='description')
        titles.setdefault(title, []).append(p)
        if d: descs.setdefault(d, []).append(p)
        if info: plans.append(info)
    # refuse a shortening that makes two indexable titles identical
    clashes = {t: ps for t, ps in titles.items() if len(ps) > 1}
    if clashes:
        print('TITLE CLASH', list(clashes.items())[:5])
        raise SystemExit(1)
    n = 0
    for p, nxt in files.items():
        old = open(p, encoding='utf8').read()
        if nxt != old:
            open(p, 'w', encoding='utf8').write(nxt); n += 1
    long_t = sum(1 for t in titles if len(t) > TITLE)
    long_d = sum(1 for d in descs if len(d) > CAP)
    print(f'seo-length: {n} pages rewritten, titles still >{TITLE}: {long_t}, descriptions still >{CAP}: {long_d}')
    for p, ot, nt, od, nd in plans[:12]:
        if ot != nt:
            print(f'  title {p}: {len(ot)}->{len(nt)} {nt}')

if __name__ == '__main__':
    main()
