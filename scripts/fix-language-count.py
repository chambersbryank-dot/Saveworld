#!/usr/bin/env python3
"""Oct 16: translations said 'four languages' where English says five. Fix only entries whose English key
says five languages (video descriptions that truly say 'homepage in four languages' are left alone).
Patches i18n/<lang>.json (translation memory) and the built <lang>/*.html. Idempotent."""
import json, glob, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIX = {'fr': [('en quatre langues', 'en cinq langues'), ('dans les quatre langues', 'dans les cinq langues')],
       'es': [('en cuatro idiomas', 'en cinco idiomas'), ('y cuatro idiomas', 'y cinco idiomas'), ('las cuatro versiones de idioma', 'las cinco versiones de idioma')],
       'ar': [('بأربع لغات', 'بخمس لغات')],
       'it': [('in quattro lingue', 'in cinque lingue'), ('e quattro lingue', 'e cinque lingue')]}
FIVE = re.compile(r'five[- ]language|five languages|five language versions', re.I)
total = 0
for lang, pairs in FIX.items():
    p = f'i18n/{lang}.json'; d = json.load(open(p)); changed = {}
    def walk(o):
        global total
        for k, v in list(o.items()):
            if isinstance(v, dict): walk(v)
            elif isinstance(v, str) and FIVE.search(k):
                nv = v
                for a, b in pairs: nv = nv.replace(a, b)
                if nv != v: o[k] = nv; changed[v] = nv; total += 1
    walk(d)
    if changed: json.dump(d, open(p, 'w'), ensure_ascii=False, indent=0)
    for h in glob.glob(f'{lang}/*.html'):
        s = open(h).read(); n = s
        for old, new in changed.items(): n = n.replace(old, new)
        if n != s: open(h, 'w').write(n)
# phrases from English 'live launches and five languages' that reach HTML via another path (a11y/video text)
HTML_FIX = {'fr': [('les lancements en direct et quatre langues', 'les lancements en direct et cinq langues')],
            'es': [('lanzamientos en vivo y cuatro idiomas', 'lanzamientos en vivo y cinco idiomas')]}
for lang, pairs in HTML_FIX.items():
    for h in glob.glob(f'{lang}/*.html') + ['assets/data/a11y.json']:
        s = open(h).read(); n = s
        for a, b in pairs: n = n.replace(a, b)
        if n != s: open(h, 'w').write(n)
# trust-content.py source string (FR Corrections)
p = 'scripts/trust-content.py'; s = open(p).read()
open(p, 'w').write(s.replace('corrigeons dans les quatre langues', 'corrigeons dans les cinq langues'))
print('fixed', total, 'translation entries')
