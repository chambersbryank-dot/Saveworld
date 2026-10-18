#!/usr/bin/env python3
"""Oct 17: Amazing Facts images -> responsive WebP (480/800/1200 wide) in assets/resp/, with srcset+sizes and lazy loading,
on Amazing_Facts.html in every language folder. Idempotent; re-run after adding facts."""
import re, os, glob
from PIL import Image
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
W = (480, 800, 1200); OUT = 'assets/resp'; os.makedirs(OUT, exist_ok=True)
def variants(src):
    base = os.path.splitext(os.path.basename(src))[0]; im = None; got = []
    for w in W:
        dst = f'{OUT}/{base}-{w}.webp'
        if not os.path.exists(dst):
            im = im or Image.open(src).convert('RGB')
            if im.width < w and w != W[0]: continue
            r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(dst, 'WEBP', quality=72, method=6)
        got.append((dst, w))
    return got
def fix(f, pre):
    s = open(f, encoding='utf8').read()
    def rep(m):
        tag = m.group(0)
        if 'srcset=' in tag: return tag
        src = re.search(r'src="([^"?]+)', tag).group(1); real = src[len(pre):] if src.startswith(pre) else src
        if not real.startswith('assets/') or not real.lower().endswith(('.jpg', '.jpeg', '.png')) or not os.path.exists(real): return tag
        v = variants(real)
        ss = ', '.join(f'{pre}{d} {w}w' for d, w in v)
        tag = tag.replace(f'src="{src}"', f'src="{pre}{v[-1][0]}" srcset="{ss}" sizes="(max-width: 700px) 92vw, 420px"', 1)
        if 'loading=' not in tag: tag = tag.replace('<img', '<img loading="lazy"', 1)
        return tag
    t = re.sub(r'<img\b[^>]*class="fact-img"[^>]*>', rep, s)
    if t != s: open(f, 'w', encoding='utf8').write(t); return 1
    return 0
n = fix('Amazing_Facts.html', '')
for f in glob.glob('*/Amazing_Facts.html'): n += fix(f, '../')
print('build-af-images:', n, 'pages,', len(glob.glob(OUT + '/*.webp')), 'webp files')
