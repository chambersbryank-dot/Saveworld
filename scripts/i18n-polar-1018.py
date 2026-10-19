#!/usr/bin/env python3
"""Merge the Oct 18 2026 Polar hub hand translations (i18n/polar-1018.json: English -> {fr,es,ar,it,he}) into i18n/<lang>.json. Idempotent;
only languages present for a string are written (two he-only gap fills)."""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open('i18n/polar-1018.json', encoding='utf8'))
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items():
        if lang in tr: m[en] = tr[lang]
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
