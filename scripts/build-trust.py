#!/usr/bin/env python3
"""Oct 14 2026: trust pages (Privacy, Editorial_Policy, Corrections) + A-Z Topics index, from the Press.html template.
Writes EN pages, merges fr/es/ar strings into i18n/<lang>.json and adds the pages to i18n/pages.txt (i18n-build.py then
renders fr/es/ar). Content: scripts/trust-content.py (policy text approved Oct 14 2026). Idempotent."""
import re, html, json, os, importlib.util
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
spec = importlib.util.spec_from_file_location('c', 'scripts/trust-content.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
E = html.escape
TPL = open('Press.html', encoding='utf8').read()
FOOT = TPL[TPL.index('<footer>'):]
TR = {'fr': {}, 'es': {}, 'ar': {}}
def T(t):  # register translation tuple, return English
    for i, l in enumerate(('fr', 'es', 'ar'), 1): TR[l][t[0]] = t[i]
    return t[0]
PRESS_DESC = re.search(r'<meta name="description" content="([^"]*)"', TPL).group(1)
PRESS_TITLE = re.search(r'<title>([^<]*)</title>', TPL).group(1)
def page(slug, h1, sub, body):
    head = TPL[:TPL.index('<section class="page-hero')]
    head = head.replace(PRESS_DESC, E(sub, quote=True)).replace(PRESS_TITLE, E(h1) + ' | Saving Planets').replace('Press.html', slug + '.html')
    head = head.replace('"Press and Media"', json.dumps(h1)).replace('Press and Media', E(h1))
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    crumbs = f'<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">Home</a></li><li><span aria-current="page">{E(h1)}</span></li></ol></nav>'
    mid = f'<section class="page-hero"><div class="page-hero-content"><h1>{E(h1)}</h1><p>{E(sub)}</p></div></section>\n' + crumbs + '\n' + body + '\n</main>\n'
    f = slug + '.html'
    if os.path.exists(f):
        cur = open(f, encoding='utf8').read(); a = cur.index('<section class="page-hero'); b = cur.index('<footer>')
        new = cur[:a] + mid + cur[b:]
    else:
        new = head + mid + FOOT
    if not os.path.exists(f) or open(f, encoding='utf8').read() != new: open(f, 'w', encoding='utf8').write(new); print('wrote', slug)
upd = T(C.UPDATED)
for slug, p in C.PAGES.items():
    secs = []
    for i, (h, paras) in enumerate(p['sections']):
        ps = ''.join(f'<p>{E(T(x))}</p>' for x in paras)
        secs.append(f'<section class="five-ws" id="s{i+1}"><h2>{E(T(h))}</h2>{ps}</section>')
    links = '<section class="help-actions" id="more"><p><a class="btn" href="Privacy.html">' + T(C.PAGES['Privacy']['title']) + '</a> <a class="btn" href="Editorial_Policy.html">' + E(T(C.PAGES['Editorial_Policy']['title'])) + '</a> <a class="btn" href="Corrections.html">' + T(C.PAGES['Corrections']['title']) + '</a> <a class="btn" href="Press.html">' + T(('Press kit', 'Kit presse', 'Kit de prensa', 'الملف الصحفي')) + '</a></p></section>'
    page(slug, T(p['title']), T(p['sub']), '<p class="trust-updated">' + E(upd) + '</p>' + ''.join(secs) + links)
# ---- A-Z Topics index (solutions + hubs + glossary terms)
D = json.load(open('assets/data/solutions.json', encoding='utf8'))
hubname = {k: v['name'] for k, v in D['categories'].items()}
items = []
for pg in D['pages']:
    if not os.path.exists(pg['url']): continue
    kind = 'Hub' if pg.get('type') == 'hub' else hubname.get(pg.get('category'), '')
    items.append((pg['title'], pg['url'], kind))
g = open('Glossary.html', encoding='utf8').read()
for gid, term in re.findall(r'<dt id="([^"]+)">([^<]+)<', g): items.append((html.unescape(term), 'Glossary.html#' + gid, 'Glossary'))
for t in ('Hub', 'Glossary'): pass
T(('Hub', 'Pôle', 'Centro', 'محور')); T(('Glossary', 'Glossaire', 'Glosario', 'المسرد'))
items.sort(key=lambda x: re.sub(r'^(the|a|an)\s+', '', x[0].lower()))
groups = {}
for t, u, k in items:
    key = re.sub(r'^(the|a|an)\s+', '', t, flags=re.I)[:1].upper()
    groups.setdefault(key if key.isalpha() else '#', []).append((t, u, k))
letters = sorted(groups)
nav = '<nav class="az-nav" aria-label="' + T(('Jump to a letter', 'Aller à une lettre', 'Ir a una letra', 'انتقل إلى حرف')) + '">' + ''.join(f'<a href="#az-{l}">{l}</a>' for l in letters) + '</nav>'
body = [nav]
for l in letters:
    lis = ''.join(f'<li><a href="{u}">{E(t)}</a> <span class="az-kind">{E(k)}</span></li>' for t, u, k in groups[l])
    body.append(f'<section class="az-group" id="az-{l}"><h2>{l}</h2><ul class="az-list">{lis}</ul></section>')
page('Topics', T(('Topics A to Z', 'Sujets de A à Z', 'Temas de la A a la Z', 'الموضوعات من الألف إلى الياء')),
     T(('Every solution, hub and science word on Saving Planets, from A to Z.', 'Toutes les solutions, tous les pôles et les mots de science de Saving Planets, de A à Z.', 'Todas las soluciones, centros y palabras de ciencia de Saving Planets, de la A a la Z.', 'كل الحلول والمحاور والمصطلحات العلمية في Saving Planets من الألف إلى الياء.')),
     ''.join(body))
for x in getattr(C, 'EXTRA', []): T(x)
# ---- merge translations + register pages
for l, d in TR.items():
    f = f'i18n/{l}.json'; m = json.load(open(f, encoding='utf8')); ch = False
    for k, v in d.items():
        if m.get(k) != v: m[k] = v; ch = True
    if ch: json.dump(m, open(f, 'w', encoding='utf8'), ensure_ascii=False, indent=0); print('i18n', l, len(d))
pl = open('i18n/pages.txt', encoding='utf8').read().split('\n')
add = [s + '.html' for s in ('Privacy', 'Editorial_Policy', 'Corrections', 'Topics') if s + '.html' not in pl]
if add: open('i18n/pages.txt', 'a', encoding='utf8').write(('' if pl[-1] == '' else '\n') + '\n'.join(add) + '\n'); print('pages.txt +', add)
# ---- English sitemap entries (i18n-sitemap.py adds the fr/es/ar URLs and alternates)
sm = open('sitemap.xml', encoding='utf8').read()
for slug in ('Privacy', 'Editorial_Policy', 'Corrections', 'Topics'):
    loc = f'<loc>https://www.savingplanets.com/{slug}.html</loc>'
    if loc not in sm: sm = sm.replace('</urlset>', f'  <url>{loc}<lastmod>2026-10-14</lastmod></url>\n</urlset>', 1)
open('sitemap.xml', 'w', encoding='utf8').write(sm)
