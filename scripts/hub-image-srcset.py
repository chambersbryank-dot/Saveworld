#!/usr/bin/env python3
"""Oct 26 2026: responsive srcset/sizes for heavy hub content images (Earth Observation first).
Reads assets/data/media-manifest.json (R2 WebP/AVIF widths already uploaded). Idempotent.
- Adds srcset + sizes when missing (WebP widths from manifest).
- Prefer <picture> with AVIF/WebP <source> when srcset_avif or srcset exists.
- Keeps/repairs width+height from manifest (aspect ratio → CLS).
- loading=lazy + decoding=async below the fold; first in-main content img can stay eager if already fetchpriority=high.
- Fills empty alt=\"\" from nearby figcaption / .photo-credit / title attribute when the image is clearly content (not decorative logo).
- Never touches Cloudflare settings; never uploads (uses existing R2 derivatives only).
Run after apply-anim-banners / r2-cards in weekly-sync.
"""
from __future__ import annotations
import html as H
import json, os, re, sys
from urllib.parse import urlparse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
MF = json.load(open('assets/data/media-manifest.json', encoding='utf-8'))

# Hubs to process first (EO is the Lighthouse heavy page). Expand later as needed.
HUBS = [
    'Earth_Observation.html',
    # ready for a later pass:
    # 'Oceans.html', 'Deforestation.html', 'Polar.html', 'Space.html',
]
SIZES = '(max-width:700px) 92vw, (max-width:1100px) 640px, 720px'
LANGS = [''] + [f'{l}/' for l in ('fr', 'es', 'ar', 'it', 'he')]

# Map media URL (with or without content-hash infix) → manifest entry
BY_URL = {}
BY_STEM = {}
for k, e in MF.items():
    u = e.get('url') or ''
    if u:
        BY_URL[u] = e
        BY_URL[u.split('?')[0]] = e
    stem = os.path.basename(k)
    stem = re.sub(r'\.[^.]+$', '', stem)
    BY_STEM[stem.lower()] = e


def lookup(src: str):
    src = src.split('?')[0]
    if src in BY_URL:
        return BY_URL[src]
    # hash-infix: name.hash.ext → match stem
    base = os.path.basename(src)
    m = re.match(r'^(.+?)\.[0-9a-f]{8,}\.([a-z0-9]+)$', base, re.I)
    if m:
        stem = m.group(1)
        if stem.lower() in BY_STEM:
            return BY_STEM[stem.lower()]
    stem = re.sub(r'\.[^.]+$', '', base)
    stem = re.sub(r'\.[0-9a-f]{8,}$', '', stem)
    return BY_STEM.get(stem.lower())


def esc(s: str) -> str:
    return H.escape(s or '', quote=True)


def nearby_alt(html: str, start: int) -> str:
    window = html[max(0, start - 400): start + 800]
    for pat in (
        r'<figcaption[^>]*>(.*?)</figcaption>',
        r'class="photo-credit"[^>]*>(.*?)</',
        r'title="([^"]+)"',
    ):
        m = re.search(pat, window, re.I | re.S)
        if m:
            t = re.sub(r'<[^>]+>', '', m.group(1))
            t = H.unescape(re.sub(r'\s+', ' ', t)).strip(' .')
            if 8 <= len(t) <= 180:
                return t
    return ''


def picture_or_attrs(e: dict, alt: str, existing_style: str, eager: bool) -> str:
    """Build <picture>…</picture> or enhanced <img> from manifest entry."""
    w, h = e.get('width'), e.get('height')
    # Cap reported dimensions for CSS aspect-ratio friendliness while keeping ratio
    if w and h and w > 1600:
        h = max(1, round(h * 1600 / w))
        w = 1600
    src = e.get('url') or ''
    # Prefer a mid WebP as img src when master is TIFF/PNG huge
    if src.lower().endswith(('.tif', '.tiff', '.png')) and e.get('srcset'):
        parts = [p.strip().split() for p in e['srcset'].split(',') if p.strip()]
        mid = None
        for url, ww in parts:
            if ww.endswith('w') and int(ww[:-1]) >= 1280:
                mid = url
                break
        if mid:
            src = mid
        elif parts:
            src = parts[-1][0]
    style = f' style="{existing_style}"' if existing_style else ''
    pri = ' fetchpriority="high"' if eager else ' loading="lazy"'
    img = (f'<img{style} src="{esc(src)}" alt="{esc(alt)}"'
           + (f' width="{w}" height="{h}"' if w and h else '')
           + f'{pri} decoding="async">')
    sources = ''
    if e.get('srcset_avif'):
        sources += f'<source type="image/avif" srcset="{esc(e["srcset_avif"])}" sizes="{SIZES}">'
    if e.get('srcset'):
        sources += f'<source type="image/webp" srcset="{esc(e["srcset"])}" sizes="{SIZES}">'
        # also put srcset on img as fallback for older browsers without picture
        img = img.replace('<img', f'<img srcset="{esc(e["srcset"])}" sizes="{SIZES}"', 1)
    if sources:
        return f'<picture>{sources}{img}</picture>'
    return img


IMG_RE = re.compile(r'<img\b([^>]*)>', re.I)


def process(path: str) -> int:
    raw = open(path, encoding='utf-8').read()
    # Do not rewrite banner slides (already picture+srcset from apply-anim-banners)
    parts = re.split(r'(<!-- ANIMBAN:START -->.*?<!-- ANIMBAN:END -->)', raw, flags=re.S)
    changed = 0
    out = []
    content_i = 0
    for part in parts:
        if part.startswith('<!-- ANIMBAN:START -->'):
            out.append(part)
            continue

        def repl(m: re.Match) -> str:
            nonlocal changed, content_i
            attrs = m.group(1)
            if 'sp-logo' in attrs or 'brand/' in attrs or 'spb-media' in attrs:
                return m.group(0)
            # already a picture child handled? skip if parent context — we only see img tag
            if 'srcset=' in attrs:
                return m.group(0)
            sm = re.search(r'\ssrc="([^"]+)"', attrs)
            if not sm:
                return m.group(0)
            src = sm.group(1)
            host = (urlparse(src).hostname or '') if src.startswith(('http://', 'https://')) else ''
            if host not in ('media.savingplanets.com', 'www.media.savingplanets.com') and not src.startswith('assets/'):
                return m.group(0)
            e = lookup(src)
            if not e or not e.get('srcset'):
                return m.group(0)
            # Skip if already inside <picture> (heuristic: look back)
            # (handled by not double-processing)

            am = re.search(r'\salt="([^"]*)"', attrs)
            alt = H.unescape(am.group(1)) if am else ''
            if alt == '':
                # content photos: fill from nearby caption/credit; keep empty only if still unknown
                guess = nearby_alt(part, m.start())
                if guess:
                    alt = guess
                elif e.get('credit'):
                    alt = e['credit']
                else:
                    # leave empty decorative only when we truly have nothing
                    alt = ''
            st = re.search(r'\sstyle="([^"]*)"', attrs)
            style = st.group(1) if st else ''
            content_i += 1
            eager = content_i == 1 and 'fetchpriority="high"' in attrs
            # If this img is already wrapped in picture, replace whole picture
            # Simple path: replace img tag only; if previous chars are <picture…><source…>
            new = picture_or_attrs(e, alt, style, eager=False)
            # Avoid nesting picture in picture
            if part[max(0, m.start() - 80):m.start()].rstrip().endswith('</source>') or '<picture' in part[max(0, m.start() - 120):m.start()]:
                # only refresh attrs on the img inside picture
                add = ''
                if 'srcset=' not in attrs and e.get('srcset'):
                    add += f' srcset="{esc(e["srcset"])}" sizes="{SIZES}"'
                if alt and (not am or am.group(1) == ''):
                    if am:
                        tag = m.group(0).replace('alt=""', f'alt="{esc(alt)}"', 1).replace("alt=''", f'alt="{esc(alt)}"', 1)
                    else:
                        tag = m.group(0).replace('<img', f'<img alt="{esc(alt)}"', 1)
                    if add:
                        tag = tag.replace('<img', '<img' + add, 1)
                    if tag != m.group(0):
                        changed += 1
                    return tag
                return m.group(0)
            changed += 1
            return new

        out.append(IMG_RE.sub(repl, part))
    text = ''.join(out)
    # Collapse accidental <picture><picture>
    text2 = re.sub(r'<picture>\s*<picture>', '<picture>', text)
    text2 = re.sub(r'</picture>\s*</picture>', '</picture>', text2)
    if text2 != raw:
        open(path, 'w', encoding='utf-8').write(text2)
    return changed


def main():
    targets = sys.argv[1:] or HUBS
    n = 0
    files = 0
    for base in targets:
        for pre in LANGS:
            path = pre + base
            if not os.path.exists(path):
                continue
            c = process(path)
            if c:
                files += 1
                n += c
                print(f'hub-image-srcset: {path} +{c} imgs')
    print(f'hub-image-srcset: {n} images on {files} files')


if __name__ == '__main__':
    main()
