#!/usr/bin/env python3
"""Homepage showcase images stay at the master's full resolution.

WebP and AVIF srcsets are encoded at high quality (no 800px cap, no heavy compression).
Smaller widths are only for narrow screens. The Saturn hero CSS file (assets/Saturn.jpg)
and the R2 hero srcsets are left alone. Below-the-fold cards keep loading=lazy.

Also writes the Saturn hero credit ("Made from SI and Biological SI Partner" in the page
language) with the Cassini source links, and the homepage Space-card link for PIA06193.
"""
import os, re, glob
from PIL import Image

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
V = '20261102q'
WEBP_Q = 95
AVIF_Q = 80
SATS = 'https://photojournal.jpl.nasa.gov/catalog/PIA11141'
RINGS = 'https://photojournal.jpl.nasa.gov/catalog/PIA06175'
CARD = 'https://photojournal.jpl.nasa.gov/catalog/PIA06193'
HERO3840 = 'https://media.savingplanets.com/images/hero-space/saturn-cassini-3840.5c1a15f7e10c.webp 3840w'
MADE = {
    'en': 'Made from SI and Biological SI Partner',
    'fr': 'Réalisé à partir de SI et Biological SI Partner',
    'es': 'Hecho a partir de SI y Biological SI Partner',
    'ar': 'صُنع من SI وBiological SI Partner',
    'it': 'Realizzato a partire da SI e Biological SI Partner',
    'he': 'עשוי מ-SI ושותף SI ביולוגי',
}

def widths_for(w):
    out = []
    if w > 480:
        out.append(480)
    if w > 800:
        out.append(800)
    out.append(w)
    return out

def master_of(local):
    """local is assets/... without a query. Prefer the original JPEG/PNG over a derivative."""
    folder, fname = os.path.split(local)
    stem = re.sub(r'-\d+$', '', os.path.splitext(fname)[0])
    found = []
    for ext in ('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.webp'):
        cand = os.path.join(folder, stem + ext)
        if os.path.exists(cand):
            found.append(cand)
    photos = [p for p in found if not p.lower().endswith('.webp')]
    return (photos or found or [None])[0]

ENCODED = {}

def encode(master):
    if master in ENCODED:
        return ENCODED[master]
    im = Image.open(master).convert('RGB')
    folder, fname = os.path.split(master)
    stem = os.path.splitext(fname)[0]
    made = []
    for w in widths_for(im.width):
        frame = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        web = os.path.join(folder, f'{stem}-{w}.webp')
        avif = os.path.join(folder, f'{stem}-{w}.avif')
        frame.save(web, quality=WEBP_Q, method=6)
        frame.save(avif, quality=AVIF_Q)
        made.append((w, web, avif))
    ENCODED[master] = (im.width, im.height, made)
    return ENCODED[master]

def attr(tag, name):
    m = re.search(r'\s' + name + r'="([^"]*)"', tag)
    return m.group(1) if m else ''

def picture_for(tag, pre):
    src = attr(tag, 'src')
    if not src or src.startswith('http') or 'brand/' in src or '/hero/' in src:
        return None
    local = src.split('?')[0]
    if local.startswith('../'):
        local = local[3:]
    if not local.startswith('assets/'):
        return None
    ss = attr(tag, 'srcset')
    if 'media.savingplanets.com' in ss and any(int(w) >= 1920 for w in re.findall(r'(\d+)w', ss)):
        return None
    master = master_of(local)
    if not master:
        return None
    mw, mh, made = encode(master)
    sizes = attr(tag, 'sizes') or '(max-width: 700px) 92vw, (max-width: 1100px) 46vw, 280px'
    alt = attr(tag, 'alt')
    loading = attr(tag, 'loading') or 'lazy'
    decoding = attr(tag, 'decoding') or 'async'
    width = attr(tag, 'width') or str(mw)
    height = attr(tag, 'height') or str(mh)

    def url(path, w):
        rel = path if pre == '' else pre + path
        return f'{rel}?v={V} {w}w'

    avif = ', '.join(url(a, w) for w, web, a in made)
    webp = ', '.join(url(web, w) for w, web, a in made)
    full = made[-1][1]
    full_rel = full if pre == '' else pre + full
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="{full_rel}?v={V}" alt="{alt}" width="{width}" height="{height}" '
            f'loading="{loading}" decoding="{decoding}"></picture>')

def add_hero_3840(s):
    def repl(m):
        val = m.group(1)
        if '3840' in val or 'saturn-cassini-2560' not in val:
            return m.group(0)
        return f'data-srcset="{val},{HERO3840}"'
    return re.sub(r'data-srcset="([^"]*saturn-cassini-2560[^"]*)"', repl, s)

def hero_credit(s, lang):
    made = MADE[lang]
    inner = (f'{made} · <a href="{SATS}" rel="noopener">Saturn: NASA/JPL-Caltech/Space Science Institute</a>'
             f' · <a href="{RINGS}" rel="noopener">Rings: NASA/JPL-Caltech/Space Science Institute</a>')
    return re.sub(r'<p class="hero-video-credit">.*?</p>',
                  f'<p class="hero-video-credit">{inner}</p>', s, count=1)

def space_card_link(s):
    def repl(m):
        p = m.group(0)
        if 'photojournal.jpl.nasa.gov/catalog/PIA06193' in p:
            return p
        return p.replace('NASA/JPL/Space Science Institute',
                         f'<a href="{CARD}" rel="noopener">NASA/JPL/Space Science Institute</a>', 1)
    return re.sub(r'<p class="photo-credit nasa-credit">.*?</p>', repl, s)

def rewrite(path, lang):
    s = open(path, encoding='utf8').read()
    pre = '' if lang == 'en' else '../'
    n = 0
    def one(m):
        nonlocal n
        window = s[max(0, m.start() - 1200):m.start()]
        if window.rfind('<picture') > window.rfind('</picture>'):
            return m.group(0)
        pic = picture_for(m.group(0), pre)
        if not pic:
            return m.group(0)
        n += 1
        return pic
    s2 = re.sub(r'<img\b[^>]*>', one, s)
    s2 = add_hero_3840(s2)
    s2 = hero_credit(s2, lang)
    s2 = space_card_link(s2)
    if s2 != s:
        open(path, 'w', encoding='utf8').write(s2)
    print(f'homepage-showcase: {path} pictures={n}')

if __name__ == '__main__':
    pages = [('index.html', 'en')] + [(f'{l}/index.html', l) for l in ('fr', 'es', 'ar', 'it', 'he')]
    for path, lang in pages:
        if os.path.exists(path):
            rewrite(path, lang)
