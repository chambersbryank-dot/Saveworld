#!/usr/bin/env python3
"""Oct 25 2026 (founder, upgrade 5): 'Real numbers from the field' strip on the homepage, directly below the locked hero
(inserted just before <template id="home-parked">, i.e. after the hero section closes; the hero itself is not touched). Data: assets/data/home-numbers.json (only figures the
organization publishes itself, each with its source link and an 'as of' date). Writes <!-- HOMENUM:START/END --> in index.html of
all 6 languages with that language's strings (below), then re-stamps the translated pages' i18n-source hash (the block is
replaced per language after i18n-build, so English changes here never leave translations stale). Idempotent. Run from repo root."""
import os, re, json, html, datetime, importlib.util
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
E_ = lambda s: html.escape(str(s), quote=True)
D = json.load(open('assets/data/home-numbers.json', encoding='utf8'))['items']
T = {
 'h': {'en': 'Real Numbers from the Field', 'fr': 'Des chiffres réels, sur le terrain', 'es': 'Cifras reales sobre el terreno', 'ar': 'أرقام حقيقية من الميدان', 'it': 'Numeri reali dal campo', 'he': 'מספרים אמיתיים מהשטח'},
 'note': {'en': 'Figures published by each organization on its own site. We check them by hand and show the date we last checked.',
          'fr': 'Chiffres publiés par chaque organisation sur son propre site. Nous les vérifions nous-mêmes et indiquons la date de la dernière vérification.',
          'es': 'Cifras publicadas por cada organización en su propio sitio. Las revisamos a mano y mostramos la fecha de la última revisión.',
          'ar': 'أرقام تنشرها كل منظمة على موقعها. نراجعها يدويًا ونعرض تاريخ آخر مراجعة.',
          'it': 'Dati pubblicati da ogni organizzazione sul proprio sito. Li controlliamo a mano e mostriamo la data dell\'ultimo controllo.',
          'he': 'נתונים שכל ארגון מפרסם באתר שלו. אנחנו בודקים אותם ידנית ומציגים את תאריך הבדיקה האחרונה.'},
 'toc': {'en': 'kilograms of trash removed from the environment by The Ocean Cleanup', 'fr': 'kilogrammes de déchets retirés de l\'environnement par The Ocean Cleanup',
         'es': 'kilogramos de basura retirados del medio ambiente por The Ocean Cleanup', 'ar': 'كيلوغرام من النفايات أزالتها The Ocean Cleanup من البيئة',
         'it': 'chilogrammi di rifiuti rimossi dall\'ambiente da The Ocean Cleanup', 'he': 'קילוגרם פסולת ש-The Ocean Cleanup הוציאה מהסביבה'},
 'seabin': {'en': 'items captured by Seabin\'s floating bins in Sydney Harbour since 2020', 'fr': 'déchets captés par les poubelles flottantes Seabin dans le port de Sydney depuis 2020',
            'es': 'objetos capturados por los contenedores flotantes de Seabin en el puerto de Sídney desde 2020', 'ar': 'قطعة التقطتها حاويات Seabin العائمة في ميناء سيدني منذ 2020',
            'it': 'oggetti catturati dai cestini galleggianti Seabin nel porto di Sydney dal 2020', 'he': 'פריטים שנאספו בפחים הצפים של Seabin בנמל סידני מאז 2020'},
 'gan': {'en': 'night-sky observations sent to Globe at Night by people tracking light pollution', 'fr': 'observations du ciel nocturne envoyées à Globe at Night pour suivre la pollution lumineuse',
         'es': 'observaciones del cielo nocturno enviadas a Globe at Night para seguir la contaminación lumínica', 'ar': 'رصدًا لسماء الليل أرسله الناس إلى Globe at Night لتتبع التلوث الضوئي',
         'it': 'osservazioni del cielo notturno inviate a Globe at Night per seguire l\'inquinamento luminoso', 'he': 'תצפיות בשמי הלילה שנשלחו ל-Globe at Night למעקב אחר זיהום אור'},
 'src': {'en': 'Source:', 'fr': 'Source :', 'es': 'Fuente:', 'ar': 'المصدر:', 'it': 'Fonte:', 'he': 'מקור:'},
 'asof': {'en': 'as of {d}', 'fr': 'au {d}', 'es': 'al {d}', 'ar': 'حتى {d}', 'it': 'al {d}', 'he': 'נכון ל-{d}'},
 'million': {'en': 'million', 'fr': 'millions', 'es': 'millones', 'ar': 'مليون', 'it': 'milioni', 'he': 'מיליון'},
}
MON = {'en': 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec', 'fr': 'janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.',
       'es': 'ene. feb. mar. abr. may. jun. jul. ago. sept. oct. nov. dic.', 'it': 'gen. feb. mar. apr. mag. giu. lug. ago. set. ott. nov. dic.',
       'ar': 'يناير فبراير مارس أبريل مايو يونيو يوليو أغسطس سبتمبر أكتوبر نوفمبر ديسمبر', 'he': 'בינואר בפברואר במרץ באפריל במאי ביוני ביולי באוגוסט בספטמבר באוקטובר בנובמבר בדצמבר'}
def day(l, iso):
    d = datetime.date.fromisoformat(iso); m = MON[l].split()[d.month - 1]
    return f'{m} {d.day}, {d.year}' if l == 'en' else f'{d.day} {m} {d.year}'
def num(l, it):
    v = it['value']
    if it['unit'] == 'million':
        s = (f'{v:g}' if l in ('en', 'ar', 'he') else f'{v:g}'.replace('.', ',')) + ' ' + T['million'][l]
    else:
        s = f'{v:,}'
        if l == 'fr': s = s.replace(',', '\u202f')
        elif l in ('es', 'it'): s = s.replace(',', '.')
    if it['plus'] and l in ('ar', 'he'): return {'ar': 'أكثر من ', 'he': 'יותר מ-'}[l] + s  # RTL: words, not a trailing '+'
    return s + ('+' if it['plus'] else '')
def block(l):
    pre = '' if l == 'en' else ''
    lis = ''.join(
        f'<li class="hn-item"><span class="hn-num">{E_(num(l, it))}</span><a class="hn-label" href="{pre}{E_(it["page"])}">{E_(T[it["id"]][l])}</a>'
        f'<span class="hn-src">{E_(T["src"][l])} <a href="{E_(it["source_url"])}" target="_blank" rel="noopener">{E_(it["source_name"])}</a>, {E_(T["asof"][l].replace("{d}", day(l, it["as_of"])))}</span></li>'
        for it in D)
    css = ('<style>.home-numbers{max-width:1100px;margin:1.5rem auto;padding:0 1rem}.home-numbers h2{text-align:center;margin:0 0 .8rem}'
           '.hn-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}'
           '.hn-item{border:1px solid rgba(127,127,127,.35);border-radius:14px;padding:1rem;display:flex;flex-direction:column;gap:.35rem;text-align:center}'
           '.hn-num{font-size:1.9rem;font-weight:800;line-height:1.1;unicode-bidi:isolate}.hn-label{font-weight:600}.hn-src{font-size:.82rem;opacity:.85}'
           '.hn-note{text-align:center;font-size:.85rem;opacity:.85;margin:.8rem 0 0}</style>')
    return (f'<!-- HOMENUM:START -->{css}<section class="home-numbers" aria-labelledby="hn-h" data-pagefind-ignore><h2 id="hn-h">{E_(T["h"][l])}</h2>'
            f'<ul class="hn-list">{lis}</ul><p class="hn-note">{E_(T["note"][l])}</p></section><!-- HOMENUM:END -->')
R = re.compile(r'<!-- HOMENUM:START -->.*?<!-- HOMENUM:END -->', re.S)
def put(f, l):
    s = open(f, encoding='utf8').read(); o = s
    if R.search(s): s = R.sub(lambda m: block(l), s)
    else:
        a = '<template id="home-parked"'  # directly after the hero section closes (the old impact strip is parked inside this template)
        assert a in s, f + ': no home-parked template after the hero'
        s = s.replace(a, block(l) + a, 1)
    return s, o
s, o = put('index.html', 'en')
if s != o: open('index.html', 'w', encoding='utf8').write(s)
sp = importlib.util.spec_from_file_location('ib', 'scripts/i18n-build.py'); ib = importlib.util.module_from_spec(sp); sp.loader.exec_module(ib)
H = ib.src_hash('index.html')
for l in ['fr', 'es', 'ar', 'it', 'he']:
    f = l + '/index.html'
    if not os.path.exists(f): continue
    s, o = put(f, l)
    s = re.sub(r'(<meta content="index\.html )[0-9a-f]{12}(" name="i18n-source"/?>)', lambda m: m.group(1) + H + m.group(2), s)
    if s != o: open(f, 'w', encoding='utf8').write(s)
print('home numbers:', len(D), 'items, 6 languages')
