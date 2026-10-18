#!/usr/bin/env python3
"""Oct 17: Hebrew World Map data. build-map.py only builds public languages, and he/World_Map.html is made by
i18n-build from the English page (whose data-src is a root-relative path that breaks under he/).
Writes assets/data/map.he.json from map.en.json, translating UI strings, hub/solution names, summaries and
pin labels through i18n/he.json (English kept where no translation exists), then points he/World_Map.html at it.
Run after i18n-build.py he (and after build-map.py, which refreshes map.en.json)."""
import json, os, re
import langs as L10N
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
if not os.path.exists('he/World_Map.html'): raise SystemExit('build-map-he: no he/World_Map.html, skipped')
M = json.load(open('i18n/he.json', encoding='utf8'))
def t(s):
    if not isinstance(s, str): return s
    if s in M: return M[s]
    if '— ' + s in M: return M['— ' + s][2:]
    return s
d = json.load(open('assets/data/map.en.json', encoding='utf8'))
d['lang'] = 'he'
d['ui'] = {k: t(v) for k, v in d['ui'].items()}
for h in d['hubs']: h['n'] = t(h['n'])
for s in d['sols']:
    for k in ('n', 'hn', 's'): s[k] = t(s.get(k))
    ps = s.get('p', []); j = '— ' + '; '.join(p.get('label', '') for p in ps); hj = M.get(j, '')[2:].split('; ')
    for i, p in enumerate(ps): p['label'] = hj[i] if len(hj) == len(ps) and j in M else t(p.get('label'))
for site in d['sites']: site['name'] = t(site['name'])
json.dump(d, open('assets/data/map.he.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
f = 'he/World_Map.html'; h = open(f, encoding='utf8').read()
h2 = re.sub(r'data-src="(?:\.\./)?assets/data/map\.[a-z]+\.json', 'data-src="../assets/data/map.he.json', h)
if not L10N.HE_PUBLIC: h2 = L10N.ensure_hidden_robots(h2)
if h2 != h: open(f, 'w', encoding='utf8').write(h2)
ui = d['ui']; print('build-map-he: ui', sum(1 for v in ui.values() if re.search('[\u0590-\u05ff]', v)), '/', len(ui),
    'sols', sum(1 for s in d['sols'] if re.search('[\u0590-\u05ff]', s['n'] or '')), '/', len(d['sols']))
