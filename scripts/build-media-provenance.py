#!/usr/bin/env python3
"""Oct 26 2026 (founder-approved): Free Media Provenance page (Media_Provenance.html, 6 langs) + tracker assets/data/media-provenance.csv + footer link (MEDIAPROV markers).
Scans the built English pages for every third-party image/video and the credit shown next to it (data-image-credit, credit=, banner spx-cred, figcaption,
anim-banners.json). A credit found only in nearby text is marked 'needs verification'. Terms URLs are the publishers' own pages, read Oct 26 2026.
No release date is guessed: only a date written in the credit itself is used. Idempotent. Run after build-license.py.
  python3 scripts/build-media-provenance.py"""
import re, os, glob, html, json, csv, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SITE = 'https://www.savingplanets.com/'; PAGE = 'Media_Provenance.html'; LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']; CHECKED = 'October 2026'
import re,glob,html,json,collections
def key(u):
    u=html.unescape(u).split('?')[0]; b=u.rsplit('/',1)[-1]
    b=re.sub(r"\.[0-9a-f]{12}(?=\.)","",b); b=re.sub(r"-\d{3,4}(?=\.(webp|avif|jpe?g|png)$)","",b); return re.sub(r"\.(webp|avif|jpe?g|png)$","",b)
ab=json.load(open('assets/data/anim-banners.json'))
R=collections.defaultdict(lambda:{'pages':set(),'credits':set()})
SKIP=re.compile(r'sp-logo|/brand/|/og/|favicon|icon',re.I)
for f in sorted(x for x in glob.glob('*.html') if x != PAGE):
    s=open(f,encoding='utf8').read()
    for m in re.finditer(r'data-image="([^"]+)"[^>]*?data-image-credit="([^"]*)"',s): R[key(m.group(1))]['pages'].add(f); R[key(m.group(1))]['credits'].add(html.unescape(m.group(2)))
    for m in re.finditer(r'<[a-z]+ [^>]*>',s):
        t=m.group(0); c=re.search(r'\bcredit="([^"]*)"',t); im=re.search(r'(?:src|data-src|data-bg|data-img)="([^"]+\.(?:jpe?g|png|webp|gif|avif|mp4|webm))',t)
        if im and not SKIP.search(im.group(1)):
            k=key(im.group(1)); R[k]['pages'].add(f)
            if c: R[k]['credits'].add(html.unescape(c.group(1)))
    sl=re.findall(r'class="spx-slide spx-(\d+)".*?<img [^>]*src="([^"]+)"',s,re.S)
    cr=dict(re.findall(r'spx-cred spx-c(\d+)">([^<]*)<',s))
    for i,u in sl:
        if i in cr: R[key(u)]['credits'].add(html.unescape(cr[i]).strip())
    for m in re.finditer(r'<figure[^>]*>(.*?)</figure>',s,re.S):
        im=re.search(r'<img [^>]*src="([^"]+)"',m.group(1)); fc=re.search(r'<figcaption[^>]*>(.*?)</figcaption>',m.group(1),re.S)
        if im and fc and not SKIP.search(im.group(1)):
            t=re.sub('<[^>]+>','',fc.group(1)); cm=re.search(r'(?:Credit|Image|Photo)s?:\s*(.+)$',t)
            R[key(im.group(1))]['pages'].add(f)
            if cm: R[key(im.group(1))]['credits'].add(html.unescape(cm.group(1)).strip())
for f in sorted(x for x in glob.glob('*.html') if x != PAGE):
    s=open(f,encoding='utf8').read()
    for m in re.finditer(r'(?:src|data-src|href|poster|data-image)="([^"]+\.(?:jpe?g|png|webp|avif|mp4|webm))[^"]*"',s):
        k=key(m.group(1))
        if k in R and not R[k]['credits']:
            w=re.sub(r'<[^>]+>',' ',s[m.end():m.end()+2500])
            c=re.search(r'(?:Credit|Image|Photo|Video|Footage|Crédit)s?\s*(?:credit)?\s*:\s*([^|\n]{3,160}?)(?:\s{2,}|\.\s|$)',w)
            if c: R[k]['credits'].add('~'+html.unescape(c.group(1)).strip())
for k,v in ab.items():
    if isinstance(v,dict) and v.get('r2'): R[key(v['r2'])]['credits'].add(v['credit'])
R={k:{'pages':sorted(v['pages']),'credits':sorted(v['credits'])} for k,v in R.items() if v['pages']}
# Publisher terms (each page read Oct 26 2026). 'nc' = publisher excludes commercial/advertising use.
TERMS = [  # (test on credit text, publisher, terms URL, short statement, nc)
 (r'JAXA', 'JAXA (Japan Aerospace Exploration Agency) data', 'https://global.jaxa.jp/policy.html', 'JAXA terms; needs verification (flagged: JAXA application withdrawn)', True),
 (r'CC BY-SA 3\.0 IGO', 'ESA / Copernicus (EUMETSAT)', 'https://creativecommons.org/licenses/by-sa/3.0/igo/', 'CC BY-SA 3.0 IGO', False),
 (r'\bESA\b|Copernicus|EUMETSAT', 'ESA (European Space Agency)', 'https://www.esa.int/ESA_Multimedia/Terms_and_conditions_of_use_of_images_and_videos_available_on_the_esa_website', 'ESA terms: free for educational, editorial and informational use with credit; commercial use (including advertising) needs ESA authorisation', True),
 (r'CC BY-SA 4\.0', 'Creative Commons author', 'https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY-SA 4.0', False),
 (r'CC BY-SA 3\.0', 'Creative Commons author', 'https://creativecommons.org/licenses/by-sa/3.0/', 'CC BY-SA 3.0', False),
 (r'CC BY 4\.0', 'Creative Commons author', 'https://creativecommons.org/licenses/by/4.0/', 'CC BY 4.0', False),
 (r'CC BY 2\.0', 'Creative Commons author', 'https://creativecommons.org/licenses/by/2.0/', 'CC BY 2.0', False),
 (r'\bNASA\b|JPL|Goddard|GSFC|KSC|Landsat|ISS\d|iss\d|STS', 'NASA', 'https://www.nasa.gov/nasa-brand-center/images-and-media/', 'NASA Images and Media Usage Guidelines: generally not subject to U.S. copyright; free for educational and informational use with NASA credited', False),
 (r'Pexels', 'Pexels photographer', 'https://www.pexels.com/license/', 'Pexels License: free to use, attribution not required', False),
 (r'NOAA|USGS|USFWS|USFS|USACE|NPS|BLM|U\.S\. Government', 'U.S. federal agency', '', 'U.S. Government work; terms page needs verification', False),
]
MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?'
def classify(credits):
    c = ' | '.join(x.lstrip('~') for x in credits)
    for rx, who, url, st, nc in TERMS:
        if re.search(rx, c): return who, url, st, nc
    return '', '', 'needs verification', False
def when(credits):
    c = ' '.join(credits); m = re.search(rf'({MON}\s+\d{{1,2}},\s+(?:19|20)\d\d|{MON}\s+(?:19|20)\d\d|\b\d{{4}}-\d\d-\d\d\b)', c)
    return m.group(1) if m else ''
def rows():
    out = []
    for k, v in sorted(R.items(), key=lambda kv: kv[0].lower()):
        if k.startswith(('SavePlanetLogo', 'savingplanets-promo', 'spot-fire-', 'top-ten-')): continue  # our own artwork
        cr = [x for x in v['credits']]; inferred = bool(cr) and all(x.startswith('~') for x in cr)
        who, url, st, nc = classify(cr); dt = when([x for x in cr if not x.startswith('~')])
        flags = []
        if not cr: flags.append('no credit found on page')
        if inferred: flags.append('credit taken from nearby text')
        if re.search(r'JAXA|ALOS|H-IIA|Hayabusa', k + ' '.join(cr)): flags.append('JAXA-related media: terms unclear (application withdrawn)')
        if nc: flags.append('publisher excludes commercial/advertising use')
        if re.search(r'(^|_)ESA(_|$)', k) and cr and not re.search(r'ESA|Copernicus|EUMETSAT', ' '.join(cr)) and not re.search(r'NASA', k): flags.append('file name says ESA but credit does not')
        if not url: flags.append('terms URL needs verification')
        stmt = (f'As of {CHECKED}, {who} makes this media available for free use under {st} ({url}).' if url and who and not flags[:2]
                else 'Needs verification.')
        out.append({'media': k, 'what': ', '.join(sorted({x.lstrip('~') for x in cr})) or 'needs verification', 'pages': ' '.join(v['pages'][:12]) + (f' (+{len(v["pages"]) - 12} more)' if len(v['pages']) > 12 else ''),
                    'page_count': len(v['pages']), 'released_by': who or 'needs verification', 'release_date': dt or 'needs verification',
                    'terms_url': url or 'needs verification', 'statement': stmt, 'flags': '; '.join(flags)})
    return out
T = {
 'en': ('Free media provenance', 'Where every free image and video on Saving Planets comes from, who released it, and the terms that let us use it. Checked {d}. Anything we could not confirm is marked “needs verification”, never guessed.', ['Media', 'Credit', 'Used on', 'Released by', 'Date in credit', 'Terms', 'Notes'], 'Download the full tracker (CSV)', 'Free media provenance', 'pages'),
 'fr': ('Provenance des médias libres', 'D’où vient chaque image et vidéo libre de Saving Planets, qui l’a publiée et les conditions qui nous permettent de l’utiliser. Vérifié en {d}. Ce que nous n’avons pas pu confirmer est marqué « à vérifier », jamais deviné.', ['Média', 'Crédit', 'Utilisé sur', 'Publié par', 'Date du crédit', 'Conditions', 'Remarques'], 'Télécharger le registre complet (CSV)', 'Provenance des médias libres', 'pages'),
 'es': ('Procedencia de los medios libres', 'De dónde viene cada imagen y video libre de Saving Planets, quién lo publicó y las condiciones que nos permiten usarlo. Revisado en {d}. Lo que no pudimos confirmar se marca como «por verificar», nunca se supone.', ['Medio', 'Crédito', 'Usado en', 'Publicado por', 'Fecha del crédito', 'Condiciones', 'Notas'], 'Descargar el registro completo (CSV)', 'Procedencia de los medios libres', 'páginas'),
 'ar': ('مصدر الوسائط المجانية', 'من أين تأتي كل صورة وفيديو مجاني على Saving Planets، ومن نشره، والشروط التي تسمح لنا باستخدامه. تمت المراجعة في {d}. كل ما لم نتمكن من تأكيده مُعلَّم بعبارة «يحتاج إلى تحقق» ولا نخمّنه أبدًا.', ['الوسائط', 'النسب', 'مستخدمة في', 'نشرها', 'التاريخ في النسب', 'الشروط', 'ملاحظات'], 'تنزيل السجل الكامل (CSV)', 'مصدر الوسائط المجانية', 'صفحات'),
 'it': ('Provenienza dei media liberi', 'Da dove viene ogni immagine e video libero di Saving Planets, chi l’ha pubblicato e le condizioni che ci permettono di usarlo. Verificato a {d}. Ciò che non abbiamo potuto confermare è segnato «da verificare», mai indovinato.', ['Media', 'Crediti', 'Usato in', 'Pubblicato da', 'Data nei crediti', 'Condizioni', 'Note'], 'Scarica il registro completo (CSV)', 'Provenienza dei media liberi', 'pagine'),
 'he': ('מקור המדיה החופשית', 'מאין מגיעים כל תמונה וסרטון חופשיים ב-Saving Planets, מי פרסם אותם ואילו תנאים מתירים לנו להשתמש בהם. נבדק ב{d}. כל מה שלא הצלחנו לאשר מסומן „דורש אימות”, ולעולם לא מנוחש.', ['מדיה', 'קרדיט', 'בשימוש ב', 'פורסם על ידי', 'תאריך בקרדיט', 'תנאים', 'הערות'], 'הורדת הרשומה המלאה (CSV)', 'מקור המדיה החופשית', 'עמודים'),
}
DATE = {'en': 'October 2026', 'fr': 'octobre 2026', 'es': 'octubre de 2026', 'ar': 'أكتوبر 2026', 'it': 'ottobre 2026', 'he': 'אוקטובר 2026'}
def d(l): return '' if l == 'en' else l + '/'
def page(l, data):
    h1, lead, cols, dl, _f, pg = T[l]; e = lambda s: html.escape(str(s), quote=True)
    shell = open(d(l) + 'Glossary.html', encoding='utf8').read()
    head = shell[:shell.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{e(h1)} | Saving Planets</title>', head, flags=re.S)
    for a in ('name="description"', 'property="og:description"', 'name="twitter:description"'): head = re.sub(rf'(<meta {a} content=")[^"]*"', lambda m: m.group(1) + e(lead.format(d=DATE[l])) + '"', head)
    for a in ('property="og:title"', 'name="twitter:title"', 'property="og:image:alt"'): head = re.sub(rf'(<meta {a} content=")[^"]*"', lambda m: m.group(1) + e(h1) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head).replace('Glossary.html', PAGE)
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}{PAGE}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{PAGE}">'
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    body_open = re.sub(r'class="[^"]*"', 'class="toc-sub provenance-page"', re.search(r'<body[^>]*>', shell).group(0), count=1)
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Glossary.html', PAGE), nav, flags=re.S)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', shell[shell.index('</main>'):])
    pre = '' if l == 'en' else '../'
    trs = ''
    for r in data:
        used = ' '.join(f'<a href="{pre}{p}">{e(p[:-5].replace("_", " "))}</a>' for p in r['pages'].split(' (+')[0].split()[:3]) + (f' +{r["page_count"] - 3}' if r['page_count'] > 3 else '')
        terms = f'<a href="{e(r["terms_url"])}" rel="noopener">{e(r["released_by"])}</a>' if r['terms_url'].startswith('http') else e(r['released_by'])
        trs += f'<tr><td>{e(r["media"])}</td><td>{e(r["what"])}</td><td>{used}</td><td>{e(r["released_by"])}</td><td>{e(r["release_date"])}</td><td>{terms}</td><td>{e(r["statement"])}{" " + e(r["flags"]) if r["flags"] else ""}</td></tr>'
    css = '<style>.prov-wrap{max-width:1200px;margin:0 auto;padding:1rem}.prov-tw{overflow-x:auto}.prov-tbl{border-collapse:collapse;font-size:.85rem;width:100%}.prov-tbl th,.prov-tbl td{border:1px solid rgba(127,127,127,.35);padding:.35rem .5rem;vertical-align:top;text-align:start}</style>'
    main = (f'<main id="main">\n{css}<div class="prov-wrap"><h1>{e(h1)}</h1><p class="edu-lead">{e(lead.format(d=DATE[l]))}</p>'
            f'<p><a href="{pre}assets/data/media-provenance.csv" download>{e(dl)}</a> · {len(data)}</p>'
            f'<div class="prov-tw"><table class="prov-tbl" lang="en" dir="ltr"><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in cols) + f'</tr></thead><tbody>{trs}</tbody></table></div></div>\n')
    return head + '</head>\n' + body_open + nav + main + foot
def footer():
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in T: continue
        s = open(f, encoding='utf8').read(); s2 = re.sub(r'<!-- MEDIAPROV:START -->.*?<!-- MEDIAPROV:END -->', '', s, flags=re.S)
        if '</footer>' not in s2: continue
        pre = '' if l == 'en' else '../'
        s2 = s2.replace('</footer>', f'<!-- MEDIAPROV:START --><p class="lic-foot mp-foot"><a href="{pre}{PAGE}">{T[l][4]}</a></p><!-- MEDIAPROV:END --></footer>', 1)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    return n
def main():
    data = rows(); pass
    with open('assets/data/media-provenance.csv', 'w', newline='', encoding='utf8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    for l in LANGS:
        if os.path.exists(d(l) + 'Glossary.html'): open(d(l) + PAGE, 'w', encoding='utf8').write(page(l, data))
    n = footer()
    fl = [r for r in data if r['flags']]
    print(f'build-media-provenance: {len(data)} media, {sum(r["statement"] != "Needs verification." for r in data)} confirmed, {len(fl)} flagged, footer {n} pages')
if __name__ == '__main__': main()
