#!/usr/bin/env python3
"""Collapse each course section into a details/summary. Structure only.

Nov 24 2026. Runs after the OCW and export splices (those look for bare <section> tags).
Does not change course wording. Skips Propulsion.html (AERO 410, frozen for OER Commons).
The first overview (#about, or the first section if a page has no #about) stays open.
Expand all / Collapse all and the floating Back to top are SI drafts; no native speaker
has reviewed those two new labels yet. The Back to top words are the ones already on the page.
"""
import os, re, sys, html
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
from courses import roadmap as RM
from study_hub import CSS, FOLD_JS

LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
COURSE_IDS = {cid for _y, cs in RM.YEARS for cid, _t, _d in cs} - {'prop'}
# SI draft. No native speaker has reviewed these two labels yet.
LABELS = {
 'en': ('Expand all sections', 'Collapse all sections'),
 'fr': ('Ouvrir toutes les sections', 'Fermer toutes les sections'),
 'es': ('Abrir todas las secciones', 'Cerrar todas las secciones'),
 'ar': ('افتح كل الأقسام', 'أغلق كل الأقسام'),
 'it': ('Apri tutte le sezioni', 'Chiudi tutte le sezioni'),
 'he': ('פתחו את כל החלקים', 'סגרו את כל החלקים'),
}

def crs_span(s):
    i = s.find('<div class="crs"')
    if i < 0:
        return None
    pos, depth = i, 0
    while pos < len(s):
        m = re.search(r'</?div\b', s[pos:])
        if not m:
            return None
        a = pos + m.start()
        if s[a + 1] == '/':
            depth -= 1
            if depth == 0:
                return i, a
        else:
            depth += 1
        pos = a + 4
    return None

def top_sections(region):
    token = re.compile(r'<section\b|</section>')
    depth, start, found = 0, None, []
    for m in token.finditer(region):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0 and start is not None:
                found.append((start, m.end()))
                start = None
            if depth < 0:
                raise SystemExit('section depth went negative')
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    if depth != 0:
        raise SystemExit('unclosed section')
    return found

def wrap_region(region):
    sections = top_sections(region)
    has_about = any(re.search(r'\bid="about"', region[a:b]) for a, b in sections)
    repls, opened = [], False
    for a, b in sections:
        chunk = region[a:b]
        hm = re.search(r'<h2\b[^>]*>.*?</h2>', chunk, re.S)
        if not hm:
            continue
        body = chunk[:hm.start()] + chunk[hm.end():]
        is_about = bool(re.search(r'\bid="about"', chunk[:400]))
        open_it = is_about or (not has_about and not opened)
        if open_it:
            opened = True
        repls.append((a, b, '<details class="crs-fold"' + (' open' if open_it else '') + '><summary>' + hm.group(0) + '</summary>' + body + '</details>'))
    if not repls:
        raise SystemExit('no sections to fold')
    out = region
    for a, b, html_ in reversed(repls):
        out = out[:a] + html_ + out[b:]
    return out, len(repls)

def toolbar(lang):
    a, b = LABELS[lang]
    return ('<!-- FOLDS:BAR --><div class="crs-foldbar">'
            f'<button type="button" class="crs-btn" data-fold="all">{html.escape(a)}</button>'
            f'<button type="button" class="crs-btn" data-fold="none">{html.escape(b)}</button>'
            '</div>')

def insert_bar(region, lang):
    bar = toolbar(lang)
    if '<!-- OCW:END -->' in region:
        return region.replace('<!-- OCW:END -->', '<!-- OCW:END -->' + bar, 1)
    m = re.search(r'<div class="crs-toc"[^>]*>.*?</div>', region, re.S)
    if not m:
        raise SystemExit('no place for the expand bar')
    return region[:m.end()] + bar + region[m.end():]

def texts(s):
    s = re.sub(r'<script\b[^>]*>.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<style\b[^>]*>.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '\n', s)
    s = html.unescape(s)
    return [re.sub(r'\s+', ' ', line).strip() for line in s.split('\n') if re.sub(r'\s+', ' ', line).strip()]

def same_words(before, after, lang, back):
    extra = Counter({LABELS[lang][0]: 1, LABELS[lang][1]: 1, back: 1, '↑': 1})
    cb, ca = Counter(texts(before)), Counter(texts(after))
    ca.subtract(extra)
    ca = Counter({k: v for k, v in ca.items() if v})
    if ca != cb:
        lost = cb - ca
        gained = ca - cb
        raise SystemExit('course wording changed\n lost ' + repr(lost.most_common(8)) + '\n gained ' + repr(gained.most_common(8)))

def back_text(s):
    m = re.search(r'class="crs-top"><a href="#top"><span[^>]*>.*?</span>\s*([^<]+)</a>', s)
    if not m:
        raise SystemExit('Back to top link missing')
    return html.unescape(m.group(1)).strip()

def apply_one(path, lang):
    s = open(path, encoding='utf-8').read()
    if os.path.basename(path) == 'Propulsion.html':
        return False
    m = re.search(r'data-course="([^"]+)"', s)
    if not m or m.group(1) not in COURSE_IDS:
        return False
    if '<!-- FOLDS:ON -->' in s:
        return False
    span = crs_span(s)
    if not span:
        raise SystemExit(f'no .crs in {path}')
    i, j = span
    region, n = wrap_region(s[i:j])
    region = insert_bar(region, lang)
    back = back_text(s)
    btn = f'<a class="crs-totop" href="#top" hidden><span aria-hidden="true">&#8593;</span> {html.escape(back)}</a>'
    out = s[:i] + region + s[j:]
    if 'class="crs-totop"' not in out:
        if '<a class="sticky-help"' in out:
            out = out.replace('<a class="sticky-help"', btn + '<a class="sticky-help"', 1)
        elif '</main>' in out:
            out = out.replace('</main>', '</main>' + btn, 1)
        else:
            raise SystemExit(f'no place for Back to top in {path}')
    style = '<!-- FOLDS:ON --><style id="course-folds-css">' + CSS + '</style>'
    if '</head>' not in out:
        raise SystemExit(f'no head in {path}')
    out = out.replace('</head>', style + '</head>', 1)
    out = out.replace('</body>', FOLD_JS + '</body>', 1)
    same_words(s, out, lang, back)
    if out.count('<h2') != s.count('<h2'):
        raise SystemExit(f'h2 count changed in {path}')
    if out.count('<details class="crs-fold"') != n:
        raise SystemExit(f'fold count mismatch in {path}')
    if out.count('<details class="crs-fold" open>') != 1:
        raise SystemExit(f'expected one open section in {path}')
    open(path, 'w', encoding='utf-8').write(out)
    return True

def pages():
    found = []
    for lang in LANGS:
        base = '.' if lang == 'en' else lang
        for name in sorted(os.listdir(base)):
            if name.endswith('.html'):
                found.append((lang, name if lang == 'en' else f'{lang}/{name}'))
    return found

def apply(only=None):
    n = 0
    for lang, path in pages():
        if only and path not in only and os.path.basename(path) not in only:
            continue
        if apply_one(path, lang):
            n += 1
    print(f'course folds: {n} pages')
    return n

if __name__ == '__main__':
    apply(sys.argv[1:] or None)
