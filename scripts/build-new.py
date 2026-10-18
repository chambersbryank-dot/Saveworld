#!/usr/bin/env python3
"""Oct 15 item 10 (rev: batch dates from solutions.json "added"): dated "New this week" strip (homepage in all 5 languages, Solutions, World_Map) and a Changelog page (Changelog.html, 5 langs).
Dates are REAL: the day each solution page was first committed to git (git log --follow --diff-filter=A, Hawaii time), plus the dated
site-update entries in scripts/newsletter-updates.json. Nothing is typed by hand. The 142 total already includes every page listed here.
Run after build-ux.py / build-sol-directory.py. Idempotent (NEW-STRIP markers)."""
import re, os, json, html, subprocess, datetime, importlib.util
spec = importlib.util.spec_from_file_location('sf', 'scripts/build-spotfire.py'); sf = importlib.util.module_from_spec(spec); spec.loader.exec_module(sf)
SITE, LANGS, d, rd, wr, esc = sf.SITE, sf.LANGS, sf.d, sf.rd, sf.wr, sf.esc
PAGE = 'Changelog.html'; SHOW = 8
MON = {'en': 'January February March April May June July August September October November December',
       'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre',
       'es': 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre',
       'ar': 'يناير فبراير مارس أبريل مايو يونيو يوليو أغسطس سبتمبر أكتوبر نوفمبر ديسمبر',
       'it': 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'}
T = {'en': dict(h='New this week', sum='{n} new solutions added on {a}. They are already counted in the {t} total.', early='Solutions already on the site before the changelog started', all='See the full changelog',
                title='Changelog: what is new on Saving Planets', desc='Every solution page, with the date it was added.',
                lead='Every solution added to Saving Planets, newest first. Each batch is dated by the day it was released.',
                sols='Solutions added', upd='Site updates'),
     'fr': dict(h='Nouveau cette semaine', sum='{n} nouvelles solutions ajoutées le {a}. Elles sont déjà comptées dans le total de {t}.', early='Solutions déjà présentes avant le début du journal', all='Voir tout le journal des modifications',
                title='Journal des modifications : les nouveautés de Saving Planets', desc='Chaque page de solution, avec sa date d’ajout.',
                lead='Chaque solution ajoutée à Saving Planets, les plus récentes en premier. Les dates sont celles de publication de chaque page.',
                sols='Solutions ajoutées', upd='Mises à jour du site'),
     'es': dict(h='Novedades de esta semana', sum='{n} soluciones nuevas añadidas el {a}. Ya están incluidas en el total de {t}.', early='Soluciones que ya estaban en el sitio antes de iniciar el registro', all='Ver el registro de cambios completo',
                title='Registro de cambios: novedades de Saving Planets', desc='Cada página de solución, con la fecha en que se añadió.',
                lead='Cada solución añadida a Saving Planets, de la más reciente a la más antigua. Las fechas son las de publicación de cada página.',
                sols='Soluciones añadidas', upd='Actualizaciones del sitio'),
     'ar': dict(h='جديد هذا الأسبوع', sum='أُضيفت {n} حلول جديدة في {a}. وهي محسوبة بالفعل ضمن المجموع البالغ {t}.', early='حلول كانت على الموقع قبل بدء سجل التغييرات', all='عرض سجل التغييرات كاملًا',
                title='سجل التغييرات: ما الجديد في Saving Planets', desc='كل صفحة حل، مع تاريخ إضافتها.',
                lead='كل حل أُضيف إلى Saving Planets، الأحدث أولًا. التواريخ هي تواريخ نشر كل صفحة.',
                sols='حلول مضافة', upd='تحديثات الموقع'),
     'it': dict(h='Novità della settimana', sum='{n} nuove soluzioni aggiunte il {a}. Sono già incluse nel totale di {t}.', early='Soluzioni già presenti prima dell’inizio del registro', all='Vedi il registro completo delle modifiche',
                title='Registro delle modifiche: le novità di Saving Planets', desc='Ogni pagina di soluzione, con la data in cui è stata aggiunta.',
                lead='Ogni soluzione aggiunta a Saving Planets, dalla più recente. Le date sono quelle di pubblicazione di ogni pagina.',
                sols='Soluzioni aggiunte', upd='Aggiornamenti del sito')}
def fmt(l, iso, year=True):
    y, m, dd = map(int, iso.split('-')); mo = MON[l].split()[m - 1]
    s = f'{mo} {dd}' if l == 'en' else f'{dd} {mo}'
    return s + (f', {y}' if l == 'en' and year else f' {y}' if year else '')
def cards(l):
    s = rd(d(l) + 'Solutions.html'); out = {}
    for m in re.finditer(r'<article class="card sol-card"[^>]*data-url="(?:\.\./)?([^"#]+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', s, re.S):
        out.setdefault(m.group(1), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)).strip()))  # Oct 18: names are HTML in Solutions.html; unescape before esc() (was showing &quot;SHIKISAI&quot;)
    return out
def added(urls):
    # Oct 15: release batch dates come from solutions.json "added" (set by <meta name="sp:added"> via build-stats.js), not git history
    pages = json.load(open('assets/data/solutions.json', encoding='utf8'))['pages']
    return {p['url']: p['added'] for p in pages if p.get('added') and p['url'] in urls}
def strip(l, sols, dates, today, total, pre):
    t = T[l]; start = (today - datetime.timedelta(days=6)).isoformat()
    last = max(dates.values(), default='')
    if not last or last < start: return ''  # latest batch older than 7 days: no strip
    wk = sorted([u for u in dates if dates[u] == last], key=lambda u: sols.get(u, u).lower())
    a, b = min(dates[u] for u in wk), max(dates[u] for u in wk)
    lis = ''.join(f'<li><time datetime="{dates[u]}">{esc(fmt(l, dates[u], False))}</time> <a href="{sf.href(l, u)}">{esc(sols.get(u, u[:-5]))}</a></li>' for u in wk)
    return (f'<!-- NEW-STRIP:START --><section class="new-strip" aria-labelledby="new-h"><h2 id="new-h">🆕 {esc(t["h"])}</h2>'
            f'<p class="ns-sum">{esc(t["sum"].format(n=len(wk), a=fmt(l, a), b=fmt(l, b), t=total))}</p><ul class="ns-list">{lis}</ul>'
            f'<p class="ns-all"><a href="{pre}{PAGE}">{esc(t["all"])} {"←" if l == "ar" else "→"}</a></p></section><!-- NEW-STRIP:END -->')
def put(p, blk, anchor_re, before=True):
    if not os.path.exists(p): return 0
    s = rd(p); s = re.sub(r'<!-- NEW-STRIP:START -->.*?<!-- NEW-STRIP:END -->', '', s, flags=re.S)
    m = re.search(anchor_re, s)
    if m and blk: s = s[:m.start()] + blk + s[m.start():] if before else s[:m.end()] + blk + s[m.end():]
    return wr(p, s)
CSS = ('.new-strip{max-width:1100px;margin:1.6rem auto;padding:1rem 1.2rem;border-radius:18px;border:1px solid rgba(143,211,255,.45);background:rgba(0,60,95,.35)}'
       '.new-strip h2{margin:.1rem 0 .3rem;font-size:1.3rem}.ns-sum{margin:.2rem 0 .7rem}.ns-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));gap:.5rem .9rem}'
       '.ns-list li{display:flex;flex-direction:column;gap:.1rem;padding:.5rem .7rem;border-radius:12px;background:rgba(255,255,255,.06)}.ns-list time{font-size:.8rem;opacity:.85;font-weight:700}'
       '.ns-all{margin:.7rem 0 0;font-weight:700}html:not(.dark) body:not(.toc-home):not(.toc-sub) .new-strip{background:#eef7fc;color:#10202c}'
       '.cl-wrap{max-width:900px;margin:0 auto;padding:1rem 1.25rem 2rem}.cl-day{margin:1.4rem 0}.cl-day h2{font-size:1.25rem;border-bottom:1px solid rgba(255,255,255,.2);padding-bottom:.3rem}.cl-day h3{font-size:1rem;margin:.6rem 0 .3rem}')
def changelog(l, sols, dates, ups):
    t = T[l]; shell = rd(d(l) + 'Glossary.html')
    head = shell[:shell.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(t["title"])} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(t['desc']) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(t['title']) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('Glossary.html', PAGE).replace(f'assets/og/{l}/Glossary.jpg', f'assets/og/{l}/Changelog.jpg')
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}{PAGE}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{PAGE}">'
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    body_open = re.sub(r'class="[^"]*"', 'class="toc-sub changelog-page"', re.search(r'<body[^>]*>', shell).group(0), count=1)
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Glossary.html', PAGE), nav, flags=re.S)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', shell[shell.index('</main>'):])
    days = sorted(set(dates.values()) | {e['date'] for e in ups}, reverse=True); body = ''
    early = sorted([u for u in sols if u not in dates and u in EN_URLS], key=lambda u: sols.get(u, u).lower())
    for day in days:
        ss = sorted([u for u in dates if dates[u] == day], key=lambda u: sols.get(u, u))
        uu = [e for e in ups if e['date'] == day]
        body += f'<section class="cl-day"><h2><time datetime="{day}">{esc(fmt(l, day))}</time></h2>'
        if ss: body += f'<h3>{esc(t["sols"])} ({len(ss)})</h3><ul>' + ''.join(f'<li><a href="{sf.href(l, u)}">{esc(sols.get(u, u[:-5]))}</a></li>' for u in ss) + '</ul>'
        if uu:
            body += f'<h3>{esc(t["upd"])}</h3><ul>'
            for e in uu:
                w = e['what'].get(l); lang = '' if w else ' lang="en" dir="ltr"'; w = w or e['what']['en']
                pg = e.get('page')
                if pg: pg = sf.href(l, pg.split('#')[0]) + ('#' + pg.split('#')[1] if '#' in pg else '')
                body += f'<li{lang}><a href="{esc(pg)}">{esc(w)}</a></li>' if pg else f'<li{lang}>{esc(w)}</li>'
            body += '</ul>'
        body += '</section>'
    if early: body += f'<section class="cl-day"><h2>{esc(t["early"])} ({len(early)})</h2><ul>' + ''.join(f'<li><a href="{sf.href(l, u)}">{esc(sols.get(u, u[:-5]))}</a></li>' for u in early) + '</ul></section>'
    main = (f'<main id="main">\n<div class="cl-wrap"><h1>{esc(t["title"])}</h1><p class="edu-lead">{esc(t["lead"])}</p>{body}</div>\n')
    return head + '</head>\n' + body_open + nav + main + foot
def unstrip(p):
    if not os.path.exists(p): return 0
    s = rd(p); return wr(p, re.sub(r'<!-- NEW-STRIP:START -->.*?<!-- NEW-STRIP:END -->', '', s, flags=re.S))
def main():
    global EN_URLS
    en = cards('en'); EN_URLS = set(en); dates = added(sorted(en)); today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-10))).date()
    ups = []  # newsletter-updates.json entries are internal build notes, not public copy; changelog lists solutions only
    total = len(en); ch = 0
    for l in LANGS:
        sols = {**en, **cards(l)}; pre = ''
        blk = strip(l, sols, dates, today, total, pre)
        ch += put(d(l) + 'index.html', blk, r'<section class="news-briefs"')
        ch += put(d(l) + 'Solutions.html', blk, r'<!-- SOL-DIR:END -->', before=False)
        ch += unstrip(d(l) + 'World_Map.html')  # Oct 17: the World Map is map-only now (user: "remove noise"); strip never goes there
        ch += wr(d(l) + PAGE, changelog(l, sols, dates, ups))
    css = rd('styles.css'); css2 = re.sub(r'\n?/\* NEWS:START \*/.*?/\* NEWS:END \*/', '', css, flags=re.S).rstrip('\n') + '\n/* NEWS:START */\n' + CSS + '\n/* NEWS:END */\n'
    ch += wr('styles.css', css2)
    s = rd('sitemap.xml')
    for l in LANGS:
        loc = f'{SITE}{d(l)}{PAGE}'
        if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today.isoformat()}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-new: {len(dates)} dated solutions, writes={ch}')
if __name__ == '__main__': main()
