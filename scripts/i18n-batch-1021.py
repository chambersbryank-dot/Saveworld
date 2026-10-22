#!/usr/bin/env python3
"""Merge the Oct 21 2026 batch (A-J, M, N) hand translations (i18n/batch-1021.json: English -> {fr,es,ar,it,he})
into i18n/<lang>.json, plus the Cite This Page lines for the new pages in SHIP (fr/es/ar/it, as in batch 1017). Idempotent."""
import json, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
T = json.load(open('i18n/batch-1021.json', encoding='utf8'))
spec = importlib.util.spec_from_file_location('b', 'scripts/batch-1021-content.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ND = {'fr': 's.d.', 'es': 's.f.', 'ar': 'د.ت.', 'it': 's.d.'}
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items(): m[en] = tr[lang]
    if lang in ND:
        for pg in [x for x in b.PAGES if x['slug'] in b.SHIP]:
            ti = T.get(pg['title'], {}).get(lang, pg['title']); url = f"https://www.savingplanets.com/{lang}/{pg['slug']}.html"
            m[f"Saving Planets. (n.d.). {pg['title']}. https://www.savingplanets.com/{pg['slug']}.html"] = f"Saving Planets. ({ND[lang]}). {ti}. {url}"
            q = f'« {ti} »' if lang == 'fr' else f'"{ti}"'
            m[f"\"{pg['title']}.\" Saving Planets, https://www.savingplanets.com/{pg['slug']}.html."] = f"{q}. Saving Planets{'،' if lang == 'ar' else ','} {url}."
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
