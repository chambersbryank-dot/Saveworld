#!/usr/bin/env python3
"""Merge the Oct 24 2026 Ways to Help (every solution) hand translations (i18n/wth-1024.json: English -> {fr,es,ar,it,he}) into i18n/<lang>.json. Idempotent."""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open('i18n/wth-1024.json', encoding='utf8'))
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items(): m[en] = tr[lang]
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
