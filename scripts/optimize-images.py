#!/usr/bin/env python3
"""Oct 14 2026: responsive WebP variants (480w/800w) + srcset/sizes for homepage card images (all langs). Idempotent."""
import os, re
from PIL import Image
IMGS = ['assets/videos/great-bubble-barrier.jpg', 'assets/OceanBeach.JPG', 'assets/StreamLog.JPG', 'assets/SungaiRiver.jpg', 'assets/Threetrees3.jpg', 'assets/Saturn.jpg']
SIZES = '(max-width: 600px) 92vw, (max-width: 1100px) 45vw, 400px'
def variants(p):
    base = os.path.splitext(p)[0]; out = []
    im = Image.open(p).convert('RGB')
    for w in (480, 800):
        fn = f'{base}-{w}.webp'
        if not os.path.exists(fn) or os.path.getmtime(fn) < os.path.getmtime(p):
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
            r.save(fn, quality=70, method=6)
        out.append(f'{os.path.basename(fn)} {w}w')
    return out
for lang in ('', 'fr/', 'es/', 'ar/'):
    f = f'{lang}index.html'; s = open(f, encoding='utf-8').read(); o = s
    pre = '../' if lang else ''
    for p in IMGS:
        v = variants(p); d = os.path.dirname(p) + '/'
        srcset = ', '.join(pre + d + x for x in v)
        def rep(m):
            tag = m.group(0)
            if 'srcset=' in tag: return tag
            return tag.replace(' src=', f' srcset="{srcset}" sizes="{SIZES}" src=', 1).replace('<img src=', f'<img srcset="{srcset}" sizes="{SIZES}" src=', 1)
        s = re.sub(r'<img [^>]*src="' + re.escape(pre + p) + r'"[^>]*/?>', rep, s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); print('optimized', f)
