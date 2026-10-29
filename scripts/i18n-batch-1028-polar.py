#!/usr/bin/env python3
"""Merge the Oct 28 2026 polar batch translations (i18n/batch-1028-polar.json: English -> {fr,es,ar,it,he}) into i18n/<lang>.json,
plus the Cite This Page lines for the 20 new pages (fr/es/ar/it, as in batch 1023). MACHINE-DRAFTED: these strings were produced
with offline machine translation (Argos Translate) on 2026-10-28 and have NOT been reviewed by native speakers; see the _note in the
JSON. Idempotent."""
import json, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
T = json.load(open('i18n/batch-1028-polar.json', encoding='utf8')); T.pop('_note', None)
spec = importlib.util.spec_from_file_location('b', 'scripts/batch-1028-polar-content.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ND = {'fr': 's.d.', 'es': 's.f.', 'ar': 'د.ت.', 'it': 's.d.'}
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items(): m[en] = tr[lang]
    if lang in ND:
        for pg in b.PAGES:
            ti = T.get(pg['title'], {}).get(lang, pg['title']); url = f"https://www.savingplanets.com/{lang}/{pg['slug']}.html"
            m[f"Saving Planets. (n.d.). {pg['title']}. https://www.savingplanets.com/{pg['slug']}.html"] = f"Saving Planets. ({ND[lang]}). {ti}. {url}"
            q = f'« {ti} »' if lang == 'fr' else f'"{ti}"'
            m[f"\"{pg['title']}.\" Saving Planets, https://www.savingplanets.com/{pg['slug']}.html."] = f"{q}. Saving Planets{'،' if lang == 'ar' else ','} {url}."
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
