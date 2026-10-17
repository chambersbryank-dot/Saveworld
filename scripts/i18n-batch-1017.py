#!/usr/bin/env python3
"""Merge the Oct 17 2026 batch hand translations (i18n/batch-1017.json: English -> {fr,es,ar,it})
into i18n/<lang>.json, plus the Cite This Page lines for the six new pages. Idempotent."""
import json, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
T = json.load(open('i18n/batch-1017.json', encoding='utf8'))
spec = importlib.util.spec_from_file_location('b', 'scripts/batch-1017-content.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ND = {'fr': 's.d.', 'es': 's.f.', 'ar': 'د.ت.', 'it': 's.d.'}
for lang in ('fr', 'es', 'ar', 'it'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items(): m[en] = tr[lang]
    for pg in b.PAGES:
        ti = T.get(pg['title'], {}).get(lang, pg['title']); url = f"https://www.savingplanets.com/{lang}/{pg['slug']}.html"
        m[f"Saving Planets. (n.d.). {pg['title']}. https://www.savingplanets.com/{pg['slug']}.html"] = f"Saving Planets. ({ND[lang]}). {ti}. {url}"
        q = f'« {ti} »' if lang == 'fr' else f'"{ti}"'
        m[f"\"{pg['title']}.\" Saving Planets, https://www.savingplanets.com/{pg['slug']}.html."] = f"{q}. Saving Planets{'،' if lang == 'ar' else ','} {url}."
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
