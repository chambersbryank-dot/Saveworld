#!/usr/bin/env python3
"""Nov 3 (founder): under 'Find a solution' on the homepage (6 langs), show what's NEW per hub, styled like the hub-count chips.
Counts + newest names come only from assets/data/solutions.json "added" dates (real release dates); window = last 30 days, Hawaii time.
Names come from each language's Solutions.html cards. Idempotent (HUB-NEW markers)."""
import re, json, html, datetime, os
from zoneinfo import ZoneInfo
TODAY = datetime.datetime.now(ZoneInfo('Pacific/Honolulu')).date(); START = TODAY - datetime.timedelta(days=30)
HUB = {'project-r': 'project-rawane'}
T = {'en': ('New in each hub', 'Added in the last 30 days, from the date each page went live.', 'new', 'Newest'),
     'fr': ('Nouveautés par thème', 'Ajoutées ces 30 derniers jours, selon la date de mise en ligne de chaque page.', 'nouv.', 'La plus récente'),
     'es': ('Novedades por tema', 'Añadidas en los últimos 30 días, según la fecha de publicación de cada página.', 'nuevas', 'La más reciente'),
     'it': ('Novità per tema', 'Aggiunte negli ultimi 30 giorni, in base alla data di pubblicazione di ogni pagina.', 'nuove', 'La più recente'),
     'ar': ('الجديد في كل محور', 'أُضيفت خلال آخر 30 يومًا، حسب تاريخ نشر كل صفحة.', 'جديد', 'الأحدث'),
     'he': ('מה חדש בכל תחום', 'נוספו ב-30 הימים האחרונים, לפי תאריך הפרסום של כל דף.', 'חדשים', 'החדש ביותר')}
pages = [p for p in json.load(open('assets/data/solutions.json', encoding='utf8'))['pages'] if p.get('type') == 'solution' and p.get('added')]
CSS = ('<style>.hub-new{margin:1rem 0 .4rem;grid-column:1/-1;width:100%;max-width:1100px;justify-self:center}.hub-new h3{margin:.2rem 0 .1rem;font-size:1.05rem}.hub-new .hn-sub{margin:0 0 .5rem;font-size:.85rem;opacity:.85}'
       '.hub-new ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.5rem}'
       '.hub-new li{display:flex;flex-direction:column;gap:.3rem;border:1px solid #9cc;border-radius:16px;padding:.55rem .8rem}'
       '.hub-new .hn-top{display:flex;align-items:center;justify-content:space-between;gap:.5rem;min-height:44px}'
       '.hub-new .hn-hub{font-weight:700;text-decoration:none;display:inline-flex;align-items:center;min-height:44px}'
       '.hub-new .hn-badge{background:linear-gradient(90deg,#5fd1ff,#7cf5c8);color:#04182c;font-weight:800;border-radius:999px;padding:.15rem .6rem;font-size:.85rem;white-space:nowrap;unicode-bidi:isolate}'
       '.hub-new .hn-new{font-size:.88rem}.hub-new .hn-new a{display:inline;min-height:0}</style>')
for l in ['en', 'fr', 'es', 'it', 'ar', 'he']:
    p = 'index.html' if l == 'en' else f'{l}/index.html'; s = open(p, encoding='utf8').read()
    s = re.sub(r'<!-- HUB-NEW:START -->.*?<!-- HUB-NEW:END -->', '', s, flags=re.S)
    sol = open('Solutions.html' if l == 'en' else f'{l}/Solutions.html', encoding='utf8').read(); names = {}
    for m in re.finditer(r'<article class="card sol-card"[^>]*data-url="(?:\.\./)?([^"#]+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', sol, re.S):
        names.setdefault(m.group(1), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)).strip()))
    i = s.index('<section class="home-find"'); j = s.index('</section>', i); find = s[i:j]
    lis = []
    for m in re.finditer(r'<a class="dom-chip" href="Solutions\.html#hub-([a-z-]+)">(.*?) \(\d+\)</a>', find):
        hub, lab = m.group(1), m.group(2)
        new = [x for x in pages if HUB.get(x['category'], x['category']) == hub and START.isoformat() <= x['added'] <= TODAY.isoformat()]
        if not new: continue
        top = max(x['added'] for x in new); nw = sorted([x for x in new if x['added'] == top], key=lambda x: x['url'])[0]
        nm = names.get(nw['url'], nw['title'])
        lis.append(f'<li><span class="hn-top"><a class="hn-hub" href="Solutions.html#hub-{hub}">{lab}</a><span class="hn-badge">+{len(new)} {T[l][2]}</span></span>'
                   f'<span class="hn-new">{T[l][3]}: <a href="{nw["url"]}">{html.escape(nm)}</a> <time datetime="{top}"></time></span></li>')
    blk = (f'<!-- HUB-NEW:START -->{CSS}<div class="hub-new" aria-labelledby="hubnew-h"><h3 id="hubnew-h">{T[l][0]}</h3><p class="hn-sub">{T[l][1]}</p>'
           f'<ul>{"".join(lis)}</ul></div><!-- HUB-NEW:END -->')
    k = s.index('<p class="wm-cta">', i); s = s[:k] + blk + s[k:]
    open(p, 'w', encoding='utf8').write(s); print(l, len(lis))
