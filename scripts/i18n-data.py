"""Build assets/data/artemis.<lang>.json from assets/data/artemis.json using i18n/<lang>.json.
Translates prose fields only (names, dates, URLs, agencies untouched). Untranslated strings stay English
and are listed with --missing. Run after scripts/update-artemis.js changes the English data."""
import json, sys, copy
FIELDS = ('missionType', 'synopsis', 'status', 'objective', 'hardware', 'targetLabel', 'target')
def strings(d):
    for m in d['missions']:
        for f in FIELDS:
            if m.get(f): yield m, f, m[f]
        for x in m.get('milestones') or []: yield x, 'label', x['label']
        for p in m.get('crew') or []: yield p, 'role', p['role']
src = json.load(open('assets/data/artemis.json', encoding='utf8'))
miss = '--missing' in sys.argv
for lang in ('fr', 'es', 'ar', 'it'):
    tm = json.load(open(f'i18n/{lang}.json', encoding='utf8')); d = copy.deepcopy(src); d['lang'] = lang
    for obj, k, v in strings(d):
        if v in tm: obj[k] = tm[v]
        elif miss and lang == 'fr': print(v)
    if not miss: json.dump(d, open(f'assets/data/artemis.{lang}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
