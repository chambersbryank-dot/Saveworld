#!/usr/bin/env python3
"""Oct 18 2026 (owner approved, 7:33 PM HST): Project Rawane de-clutter. Idempotent EN-source pass (runs before i18n-build).
- 'New' callout off (assets/data/new-callout.json enabled=false; build-batch4 removes the block).
- Space Disposal: the Man-Made/Natural intro pair (repeated the two subheads) removed; Titan card removed (Dragonfly card
  covers it, and Titan stays listed under the Space Disposal hub); Europa Clipper + Juice moved to Voyages Outward.
- Jupiter listed once (kept under Made by Nature; removed from Planetary Defense).
- Artemis Program block (Artemis I-V cards, 'Last updated' note, tracker link) deleted (owner override of cut 4).
- By the Numbers (page-stats) deleted on this page only: site.js renders .page-stats only where the section exists, and the
  counts themselves (build-stats.js -> assets/data/solutions.json, homepage, other hubs) are unchanged.
- Launch widget replaced by one link to the Live Launch Tracker (Artemis_II.html#launches).
- Five W's: one or two sentences each, no repeat of the BLUF.
- Card rows: centred, no lone orphan card (grids whose count leaves 1 card on a 4-wide row get 3 per row).
- Cards hug their content (owner: 'flush with the text, tight'): CSS scoped to Project Rawane + the Artemis Program page."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PAGE = 'Project-Rawane.html'
# --- New callout off
nc = json.load(open('assets/data/new-callout.json', encoding='utf8'))
if nc.get('enabled'):
    nc['enabled'] = False; nc['note'] = nc['note'] + ' Oct 18: switched off on owner request (stale Oct 11 callout).'
    json.dump(nc, open('assets/data/new-callout.json', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
s = open(PAGE, encoding='utf-8').read(); s0 = s
s = re.sub(r'<!-- NEW-CALLOUT:START -->.*?<!-- NEW-CALLOUT:END -->\n?', '', s, flags=re.S)
def card(src, href):
    """(start, end) of the <article class="card"> whose <h3> links to href, or None."""
    m = re.search(r'<h3><a href="' + re.escape(href) + r'">', src)
    if not m: return None
    a = src.rfind('<article', 0, m.start()); b = src.find('</article>', m.end()) + len('</article>')
    return a, b
def sect(src, sid):
    a = src.find(f'id="{sid}"'); a = src.rfind('<section', 0, a); b = src.find('</section>', a) + len('</section>')
    return a, b
# --- Space Disposal intro pair (grid sd-split)
s = re.sub(r'<div class="grid sd-split">.*?</div>(?=<h2 class="sd-subhead)', '', s, count=1, flags=re.S)
# --- Titan out; Europa Clipper + Juice move to the end of Voyages Outward's card grid
a, b = sect(s, 'group-space-disposal'); sd = s[a:b]
t = card(sd, 'Titan.html')
if t: sd = sd[:t[0]] + sd[t[1]:]
moved = []
for h in ('Europa_Clipper.html', 'Juice.html'):
    c = card(sd, h)
    if c: moved.append(sd[c[0]:c[1]]); sd = sd[:c[0]] + sd[c[1]:]
s = s[:a] + sd + s[b:]
# --- Jupiter once: drop it from Planetary Defense
a, b = sect(s, 'group-planetary-defense'); pd = s[a:b]
c = card(pd, 'Jupiter.html')
if c: pd = pd[:c[0]] + pd[c[1]:]
s = s[:a] + pd + s[b:]
# --- Artemis Program block out
s = re.sub(r'<div class="artemis-program" id="artemis-program">.*?</div></div><p class="mw-note" id="artemis-syn-updated">.*?</p><p><a class="inline-link" href="Artemis_II.html">[^<]*</a></p></div>', '', s, count=1, flags=re.S)
if moved:
    a, b = sect(s, 'group-voyages-outward'); vo = s[a:b]
    end = vo.rfind('</article>') + len('</article>')
    vo = vo[:end] + ''.join(moved) + vo[end:]
    s = s[:a] + vo + s[b:]
# --- By the Numbers out (this page only)
s = re.sub(r'<section class="page-stats"[^>]*>\s*</section>\n?', '', s)
# --- Launch widget -> one link
LINK = ('<section class="pr-launch-link"><p><a class="pr-launch-btn" href="Artemis_II.html#launches">'
        'See the next launches on the Live Launch Tracker</a><span class="bluf-arrow" aria-hidden="true">→</span></p></section>')
s = re.sub(r'<section class="launch-widget" id="launches".*?</section>', lambda m: LINK, s, count=1, flags=re.S)
# --- Five W's, one or two sentences each
W = {
 'Who': "Six space agencies and the companies already doing the work. NASA, ESA, JAXA, ISRO, NOAA and CSA fly alongside Astroscale, Northrop Grumman and Starfish Space.",
 'What': "Real fixes for space, all on one page. One aims to grab an 11-meter, 3-ton dead rocket stage and bring it down: Astroscale's ADRAS-J2 (company figures).",
 'When': "Happening now, updated daily. Next up: Hera reaches its asteroid in November 2026, and Apophis passes about 20,000 miles from Earth on April 13, 2029.",
 'Where': "From low Earth orbit to Jupiter's moons. NASA's Europa Clipper will make 49 close flybys of Europa from 2030.",
 'Why': "Space and Earth are one system. NASA's IMAP can give about half an hour's warning of incoming solar radiation, and every voyage outward shows how precious home is.",
}
a, b = sect(s, 'solution'); fw = s[a:b]
for k, v in W.items():
    fw = re.sub(r'(<div class="w-card"><h3>' + k + r'</h3><p>)[^<]*(</p>)', lambda m: m.group(1) + v + m.group(2), fw, count=1)
s = s[:a] + fw + s[b:]
# --- Rebalance: a grid of 5 or 9 cards (1 left over at 4 per row) gets 3 per row
def tag(m):
    body = m.group(0); n = body.count('<article class="card"')
    cls = m.group(1).replace(' pr-cols-3', '')
    if n % 4 == 1 and n % 3 != 1: cls += ' pr-cols-3'
    return '<div class="' + cls + '">' + body[body.index('>') + 1:]
s = re.sub(r'<div class="(grid[^"]*)">(?:(?!<div class="grid).)*?</div>(?=</section>|<h2)', tag, s, flags=re.S)
if s != s0: open(PAGE, 'w', encoding='utf-8').write(s)
# --- translations
T = {
 W['Who']: ("Six agences spatiales et les entreprises qui agissent déjà. La NASA, l'ESA, la JAXA, l'ISRO, la NOAA et l'ASC travaillent aux côtés d'Astroscale, de Northrop Grumman et de Starfish Space.",
   "Seis agencias espaciales y las empresas que ya están haciendo el trabajo. La NASA, la ESA, la JAXA, la ISRO, la NOAA y la CSA trabajan junto a Astroscale, Northrop Grumman y Starfish Space.",
   "ست وكالات فضاء والشركات التي تعمل بالفعل. تعمل ناسا ووكالة الفضاء الأوروبية وجاكسا والمنظمة الهندية لأبحاث الفضاء والإدارة الوطنية للمحيطات والغلاف الجوي ووكالة الفضاء الكندية جنبًا إلى جنب مع Astroscale وNorthrop Grumman وStarfish Space.",
   "Sei agenzie spaziali e le aziende che stanno già facendo il lavoro. NASA, ESA, JAXA, ISRO, NOAA e CSA lavorano accanto ad Astroscale, Northrop Grumman e Starfish Space.",
   "שש סוכנויות חלל והחברות שכבר עושות את העבודה. NASA, ESA, JAXA, ISRO, NOAA ו-CSA פועלות לצד Astroscale, Northrop Grumman ו-Starfish Space."),
 W['What']: ("De vraies solutions pour l'espace, réunies sur une seule page. L'une vise à saisir un étage de fusée mort de 11 mètres et 3 tonnes pour le faire redescendre : ADRAS-J2 d'Astroscale (chiffres de l'entreprise).",
   "Soluciones reales para el espacio, todas en una página. Una busca atrapar una etapa de cohete muerta de 11 metros y 3 toneladas y hacerla bajar: ADRAS-J2 de Astroscale (cifras de la empresa).",
   "حلول حقيقية للفضاء في صفحة واحدة. يسعى أحدها إلى الإمساك بمرحلة صاروخ متوقفة طولها 11 مترًا ووزنها 3 أطنان وإنزالها: ADRAS-J2 من Astroscale (أرقام الشركة).",
   "Soluzioni reali per lo spazio, tutte in una pagina. Una punta ad agganciare uno stadio di razzo inattivo di 11 metri e 3 tonnellate e a farlo scendere: ADRAS-J2 di Astroscale (dati dell'azienda).",
   "פתרונות אמיתיים לחלל, כולם בעמוד אחד. אחד מהם שואף לתפוס שלב רקטה מת באורך 11 מטר ובמשקל 3 טון ולהוריד אותו: ADRAS-J2 של Astroscale (נתוני החברה)."),
 W['When']: ("Ça se passe maintenant, avec des mises à jour quotidiennes. Prochaines étapes : Hera atteint son astéroïde en novembre 2026, et Apophis passe à environ 32 000 km de la Terre le 13 avril 2029.",
   "Está pasando ahora, con actualizaciones diarias. Lo próximo: Hera llega a su asteroide en noviembre de 2026 y Apophis pasa a unos 32.000 km de la Tierra el 13 de abril de 2029.",
   "يحدث الآن، مع تحديث يومي. التالي: تصل Hera إلى كويكبها في نوفمبر 2026، ويمر أبوفيس على بعد نحو 32,000 كم من الأرض في 13 أبريل 2029.",
   "Succede adesso, con aggiornamenti quotidiani. Prossime tappe: Hera raggiunge il suo asteroide a novembre 2026 e Apophis passa a circa 32.000 km dalla Terra il 13 aprile 2029.",
   "זה קורה עכשיו, עם עדכון יומי. הבא בתור: Hera מגיעה לאסטרואיד שלה בנובמבר 2026, ואפופיס חולף כ-32,000 ק\"מ מכדור הארץ ב-13 באפריל 2029."),
 W['Where']: ("De l'orbite terrestre basse aux lunes de Jupiter. Europa Clipper, de la NASA, survolera Europe de près 49 fois à partir de 2030.",
   "Desde la órbita terrestre baja hasta las lunas de Júpiter. Europa Clipper, de la NASA, hará 49 sobrevuelos cercanos de Europa a partir de 2030.",
   "من المدار الأرضي المنخفض إلى أقمار المشتري. ستُجري مركبة Europa Clipper التابعة لناسا 49 تحليقًا قريبًا فوق القمر أوروبا ابتداءً من عام 2030.",
   "Dall'orbita terrestre bassa alle lune di Giove. Europa Clipper della NASA farà 49 sorvoli ravvicinati di Europa a partire dal 2030.",
   "ממסלול נמוך סביב כדור הארץ ועד ירחי צדק. Europa Clipper של NASA תבצע 49 מעברים קרובים ליד אירופה החל מ-2030."),
 W['Why']: ("L'espace et la Terre forment un seul système. IMAP, de la NASA, peut donner environ une demi-heure d'alerte avant l'arrivée d'un rayonnement solaire, et chaque voyage vers l'extérieur montre à quel point notre planète est précieuse.",
   "El espacio y la Tierra son un solo sistema. IMAP, de la NASA, puede avisar con una media hora de antelación de la llegada de radiación solar, y cada viaje hacia el exterior muestra lo valioso que es nuestro hogar.",
   "الفضاء والأرض نظام واحد. يمكن لمركبة IMAP التابعة لناسا أن تنذر قبل نحو نصف ساعة من وصول الإشعاع الشمسي، وكل رحلة إلى الفضاء البعيد تُظهر كم هو ثمين كوكبنا.",
   "Spazio e Terra sono un unico sistema. IMAP della NASA può dare circa mezz'ora di preavviso sull'arrivo di radiazioni solari, e ogni viaggio verso lo spazio profondo mostra quanto sia prezioso il nostro pianeta.",
   "החלל וכדור הארץ הם מערכת אחת. IMAP של NASA יכולה להתריע כחצי שעה מראש על קרינת שמש בדרך, וכל מסע אל החלל העמוק מראה כמה יקר הבית שלנו."),
 "See the next launches on the Live Launch Tracker": ("Voir les prochains lancements sur le suivi des lancements en direct",
   "Ver los próximos lanzamientos en el rastreador de lanzamientos en vivo",
   "شاهد الإطلاقات القادمة على متتبع الإطلاقات المباشر",
   "Guarda i prossimi lanci su Lanci in diretta",
   "צפו בשיגורים הבאים במעקב השיגורים החי"),
}
for i, lang in enumerate(('fr', 'es', 'ar', 'it', 'he')):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf-8')); before = dict(m)
    for k, v in T.items(): m[k] = v[i]
    if m != before: json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# --- CSS: centred card rows, 3-per-row grids, tight cards that hug their content (Rawane + Artemis Program pages only)
CSS = '''/* RAWANE-CUTS:START (generated by scripts/build-rawane-cuts.py) */
body.pr-page .card-band.hub-cards .grid { display: flex; flex-wrap: wrap; justify-content: center; align-items: flex-start; gap: 1rem; }
body.pr-page .card-band.hub-cards .grid > .card { flex: 0 0 calc((100% - 3rem) / 4); max-width: calc((100% - 3rem) / 4); min-width: 0; }
body.pr-page .card-band.hub-cards .grid.pr-cols-3 { max-width: calc(75% + .25rem); margin-left: auto; margin-right: auto; }
body.pr-page .card-band.hub-cards .grid.pr-cols-3 > .card { flex-basis: calc((100% - 2rem) / 3); max-width: calc((100% - 2rem) / 3); }
@media (max-width: 900px) { body.pr-page .card-band.hub-cards .grid > .card, body.pr-page .card-band.hub-cards .grid.pr-cols-3 > .card { flex-basis: calc((100% - 1rem) / 2); max-width: calc((100% - 1rem) / 2); } body.pr-page .card-band.hub-cards .grid.pr-cols-3 { max-width: none; } }
@media (max-width: 600px) { body.pr-page .card-band.hub-cards .grid > .card, body.pr-page .card-band.hub-cards .grid.pr-cols-3 > .card { flex-basis: 100%; max-width: 100%; } }
body.pr-page .card-band .card, body.artemis-page .card-band .card, body.artemis-page .card { height: auto !important; min-height: 0 !important; display: block; padding-bottom: .9rem; }
body.pr-page .card-band .card h3, body.artemis-page .card-band .card h3 { margin: .5rem .9rem .35rem; }
body.pr-page .card-band .card .sol-badges, body.artemis-page .card-band .card .sol-badges { margin: .55rem .9rem 0; }
body.pr-page .card-band .card-blurb, body.artemis-page .card-band .card-blurb { padding: 0 .9rem; margin: 0; }
body.pr-page .ws-grid, body.artemis-page .ws-grid { align-items: flex-start; padding-bottom: .4rem; }
body.pr-page .w-card, body.artemis-page .w-card { height: auto !important; min-height: 0 !important; padding: .9rem 1rem; }
body.pr-page .w-card h3, body.artemis-page .w-card h3 { margin: 0 0 .35rem; }
body.pr-page .w-card p, body.artemis-page .w-card p { margin: 0 0 .4rem; }
body.pr-page .w-card p:last-child, body.artemis-page .w-card p:last-child { margin-bottom: 0; }
body.pr-page .pr-launch-link { text-align: center; padding: 1.2rem 1rem 1.6rem; font-weight: 700; }
body.pr-page .pr-launch-link a { color: #8fd3ff; }
body.pr-page .pr-launch-link .bluf-arrow { display: inline-block; margin-inline-start: .35rem; color: #8fd3ff; }
[dir="rtl"] body.pr-page .pr-launch-link .bluf-arrow { transform: scaleX(-1); }
/* RAWANE-CUTS:END */'''
css = open('styles.css', encoding='utf-8').read()
css2 = re.sub(r'/\* RAWANE-CUTS:START.*?RAWANE-CUTS:END \*/', lambda m: CSS, css, flags=re.S) if 'RAWANE-CUTS:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
if css2 != css: open('styles.css', 'w', encoding='utf-8').write(css2)
print(f'build-rawane-cuts: page {"updated" if s != s0 else "unchanged"}')

# --- Oct 18 (owner, 7:51 PM HST: 'delete it wherever it appears'): no 'By the Numbers' block on any page, any language.
# site.js no longer renders .page-stats blocks (homepage overview [data-site-stats], live counts and solutions.json are
# untouched), and the empty hidden <section class="page-stats"> placeholders are removed from every built page.
# Also the leftover Artemis I-V renderer script on Project Rawane (its block is gone).
import glob as _g
js = open('site.js', encoding='utf-8').read()
js2 = js.replace("var blocks = document.querySelectorAll('.page-stats[data-stats-category]');",
                 "var blocks = [];  /* Oct 18: 'By the Numbers' blocks removed site-wide (owner); placeholders stripped by scripts/build-rawane-cuts.py */")
if js2 != js: open('site.js', 'w', encoding='utf-8').write(js2)
ART_JS = re.compile(r"<script>\s*\(function \(\) \{\s*var box = document\.getElementById\('artemis-syn'\);.*?</script>\n?", re.S)
nps = 0
for f in _g.glob('*.html') + _g.glob('*/*.html'):
    if f.split('/')[0] in ('node_modules', 'pagefind', 'search', 'docs'): continue
    t = open(f, encoding='utf-8').read(); t0 = t
    t = re.sub(r'<section class="page-stats"[^>]*>\s*</section>\n?', '', t)
    if f.endswith('Project-Rawane.html'): t = ART_JS.sub('', t)
    if t != t0: open(f, 'w', encoding='utf-8').write(t); nps += 1
print(f'build-rawane-cuts: page-stats placeholders removed from {nps} files')
