#!/usr/bin/env python3
"""Oct 15: standing rule: every SI-generated image shows the visible credit 'Created by SI and Biological SI Partner' next to that image
(not one banner per page). SI_IMAGES lists the SI-generated stills (any extension/size variant, e.g. WebP srcset copies).
Owner photos credited 'SI Partner' (Threetrees3, Yishan_Tree, ThreeTrees2) are NOT SI-generated and are left alone.
For every <img> of an SI image (all languages) with no SI credit right after it, a <span class="si-credit"> caption is inserted after the
image (after </picture> when wrapped). Idempotent; run late in weekly-sync.sh (after apply-heroes/optimize-images/build-ux)."""
import re, glob, os
SI_IMAGES = {'OceanBeach', 'StreamLog', 'theoceancleanup', 'SungaiRiver', 'spot-fire-pixels', 'spot-fire-steps'}
SI_T = {'en': 'Created by SI and Biological SI Partner', 'fr': 'Créé par SI et Biological SI Partner', 'es': 'Creado por SI y Biological SI Partner',
        'ar': 'أُنشئ بواسطة SI وBiological SI Partner', 'it': 'Creato da SI e Biological SI Partner'}
MARK = re.compile(r'SI Partner|SI وBiological')
CSS = '.si-credit{display:block;font-size:.75rem;line-height:1.3;opacity:.85;font-style:italic;margin:.25rem 0 0}'

def is_si(src):
    stem = os.path.splitext(os.path.basename(src.split('?')[0]))[0]
    stem = re.sub(r'-\d+w$|_\d+$', '', stem)
    return stem in SI_IMAGES

def fix(s, l):
    out = []; pos = 0; n = 0
    for m in re.finditer(r'<img\b[^>]*>', s):
        src = re.search(r'\bsrc="([^"]+)"', m.group(0))
        if not src or not is_si(src.group(1)): continue
        end = m.end()
        pic = re.match(r'\s*</picture>', s[end:])
        if pic: end += pic.end()
        nxt = s.find('<img', end); window = s[end: min(end + 450, nxt if nxt != -1 else len(s))]
        if MARK.search(window): continue
        out.append(s[pos:end]); out.append(f'<span class="si-credit">{SI_T[l]}</span>'); pos = end; n += 1
    out.append(s[pos:]); s = ''.join(out)
    if n or 'class="si-credit"' in s:
        if '.si-credit{' not in s: s = s.replace('</head>', f'<style>{CSS}</style>\n</head>', 1)
    return s, n

if __name__ == '__main__':
    tot = 0; pages = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in SI_T or os.path.basename(f).startswith('google'): continue
        s = open(f, encoding='utf8').read()
        if 'http-equiv="refresh"' in s: continue
        s2, n = fix(s, l)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); pages += 1; tot += n
    print(f'si-credits: {tot} captions added on {pages} pages')
