"""Nov 16 2026 batch (10 new solutions): merge i18n/batch-1116.json into i18n/<lang>.json, plus the
localized APA/MLA cite lines for each page. Run once before scripts/i18n-build.py. Idempotent.
(Created by the Founder and SI)"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
T = json.load(open('i18n/batch-1116.json', encoding='utf8')); T.pop('_note', None)
PAGES = ['Cuyahoga_River_Cleanup.html', 'Lake_Washington_Cleanup.html', 'Minor_Planet_Center.html', 'NSIDC.html',
         'Phoenix_Islands_Protected_Area.html', 'Rare_Fish_Forever.html', 'Rewilding_Argentina_Ibera_Jaguars.html',
         'SMOS.html', 'Save_the_Elephants.html', 'Snow_Leopard_Trust.html']
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
    for en, tr in T.items():
        if lang in tr: m[en] = tr[lang]
    for pg in PAGES:
        s = open(pg, encoding='utf8').read()
        ti = re.search(r'data-cite="apa">Saving Planets\. \(2026\)\. (.*?)\. https://www\.savingplanets\.com/' + re.escape(pg), s).group(1)
        lt = T.get(ti, {}).get(lang, ti); url = f'https://www.savingplanets.com/{lang}/{pg}'
        m[f'Saving Planets. (2026). {ti}. https://www.savingplanets.com/{pg}'] = f'Saving Planets. (2026). {lt}. {url}'
        q = f'« {lt} »' if lang == 'fr' else f'"{lt}"'
        m[f'"{ti}." Saving Planets, https://www.savingplanets.com/{pg}.'] = f"{q}. Saving Planets{'،' if lang == 'ar' else ','} {url}."
    json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(lang, len(m))
