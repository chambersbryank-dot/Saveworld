#!/usr/bin/env python3
"""Oct 15: astroEDU-format classroom activity page 'Spot the Fire from Space: How big is a pixel?' (Spot_the_Fire.html in en + fr/es/ar/it),
with PDF/DOCX download links (assets/docs/Spot_the_Fire_astroEDU.*), astroEDU CC BY 4.0 credit, SI-image captions, sitemap entries and
idempotent link blocks (<!-- SPOTFIRE-LINK -->) on Teachers, Kids_Map, FireSat and Lesson_Builder. Run late in weekly-sync.sh (after build-ux.py),
so translation/post-processors can't drop it. Idempotent."""
import re, os, json, html, datetime
SITE = 'https://www.savingplanets.com/'
ASSETV = '20261015n'
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.exists(f'{l}/Kids_Map.html')]
d = lambda l: '' if l == 'en' else l + '/'
PAGE = 'Spot_the_Fire.html'
SI = {'en': 'Created by SI and Biological SI Partner', 'fr': 'Créé par SI et Biological SI Partner', 'es': 'Creado por SI y Biological SI Partner',
      'ar': 'أُنشئ بواسطة SI وBiological SI Partner', 'it': 'Creato da SI e Biological SI Partner'}
T = {
 'en': dict(title='Spot the Fire from Space: How big is a pixel?', kicker='Free classroom activity · ages 10–14 · about 60 minutes',
   desc='A free astroEDU-format classroom activity: students overlay coarse and fine grids on a paper landscape to learn why satellite pixel size matters for spotting wildfires, then compare with FireSat’s real 5×5 m detection scale.',
   intro='Can a satellite miss a wildfire because its “pixels” are too big? Students lay a coarse grid and a fine grid over a printed landscape with three hidden “fires” and test which fires each grid detects. Then they scale the fine grid to meters and compare it with FireSat, which can detect fires as small as 5×5 meters, about two parking spaces (Earth Fire Alliance, Sep 16, 2026).',
   h_learn='What students learn', learn=['What a pixel is in a satellite image, and why pixel size limits what can be detected.', 'How to apply a clear detection rule: a fire counts only if it fills about half or more of a grid square.', 'FireSat’s 5×5 m detection scale, and how it compares with the fine grid.', 'Why both fine detail and frequent revisits help wildfire response.'],
   h_need='What you need', need='Printed sheets (landscape, coarse grid, fine grid, exit ticket), pencils and rulers. Tracing paper or clear acetate for the grids is ideal. No lab equipment. Optional: one screen for the FireSat page and the Satellite Explorer.',
   h_steps='How it works', h_dl='Download the activity', pdf='Teacher guide and worksheets (PDF)', docx='Editable version (Word .docx)',
   h_more='Go further', more='See the real mission on the <a href="FireSat.html">FireSat page</a>, explore orbits in the <a href="Satellite_Explorer.html">Satellite Explorer</a>, or build a full lesson in the <a href="Lesson_Builder.html">Lesson Plan Builder</a>.',
   cap1='Coarse pixels can miss a small fire that fine (about 5 m) pixels detect.', cap2='The six steps of the activity, for teachers.',
   alt1='Diagram comparing a coarse pixel grid that misses a small fire with a fine 5-meter grid that detects it', alt2='Flow diagram of the six classroom steps of the Spot the Fire activity',
   credit='Written in the <a href="https://astroedu.iau.org/" target="_blank" rel="noopener">astroEDU</a> activity format (IAU Office of Astronomy for Education). Shared under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>: you may copy, adapt and share it with credit to Saving Planets. FireSat facts: Earth Fire Alliance public releases (Jul 7 and Sep 16, 2026).',
   link='Classroom activity: Spot the Fire from Space (How big is a pixel?)', linkp='A free, printable astroEDU-format lesson on satellite pixels and wildfire detection.'),
 'fr': dict(title='Repérer un feu depuis l’espace : quelle est la taille d’un pixel ?', kicker='Activité gratuite en classe · 10–14 ans · environ 60 minutes',
   desc='Une activité gratuite au format astroEDU : les élèves superposent une grille grossière et une grille fine sur un paysage imprimé pour comprendre pourquoi la taille des pixels compte pour repérer les incendies, puis comparent avec l’échelle réelle de FireSat (5×5 m).',
   intro='Un satellite peut-il rater un incendie parce que ses « pixels » sont trop grands ? Les élèves posent une grille grossière puis une grille fine sur un paysage imprimé où se cachent trois « feux », et testent lesquels chaque grille détecte. Ils convertissent ensuite la grille fine en mètres et la comparent à FireSat, qui peut détecter des feux de 5×5 mètres, soit environ deux places de parking (Earth Fire Alliance, 16 sept. 2026).',
   h_learn='Ce que les élèves apprennent', learn=['Ce qu’est un pixel dans une image satellite, et pourquoi sa taille limite ce que l’on peut détecter.', 'Appliquer une règle claire : un feu est détecté s’il remplit environ la moitié d’une case ou plus.', 'L’échelle de détection de FireSat (5×5 m) et sa comparaison avec la grille fine.', 'Pourquoi la finesse des détails et des passages fréquents aident à lutter contre les incendies.'],
   h_need='Matériel', need='Fiches imprimées (paysage, grille grossière, grille fine, ticket de sortie), crayons et règles. Idéalement, papier calque ou transparents pour les grilles. Aucun matériel de laboratoire. En option : un écran pour la page FireSat et l’explorateur de satellites.',
   h_steps='Déroulement', h_dl='Télécharger l’activité', pdf='Guide de l’enseignant et fiches (PDF, en anglais)', docx='Version modifiable (Word .docx, en anglais)',
   h_more='Pour aller plus loin', more='Découvrez la vraie mission sur la <a href="FireSat.html">page FireSat</a>, explorez les orbites avec l’<a href="Satellite_Explorer.html">explorateur de satellites</a> ou créez une leçon complète avec le <a href="Lesson_Builder.html">générateur de plans de cours</a>.',
   cap1='Des pixels grossiers peuvent rater un petit feu que des pixels fins (environ 5 m) détectent.', cap2='Les six étapes de l’activité, pour l’enseignant.',
   alt1='Schéma comparant une grille de pixels grossière qui rate un petit feu et une grille fine de 5 mètres qui le détecte', alt2='Schéma des six étapes de l’activité en classe',
   credit='Rédigée au format d’activité <a href="https://astroedu.iau.org/" target="_blank" rel="noopener">astroEDU</a> (Bureau de l’UAI pour l’enseignement de l’astronomie). Partagée sous licence <a href="https://creativecommons.org/licenses/by/4.0/deed.fr" target="_blank" rel="noopener">CC BY 4.0</a> : vous pouvez la copier, l’adapter et la partager en citant Saving Planets. Faits sur FireSat : communiqués d’Earth Fire Alliance (7 juil. et 16 sept. 2026).',
   link='Activité en classe : repérer un feu depuis l’espace (quelle est la taille d’un pixel ?)', linkp='Une leçon gratuite à imprimer, au format astroEDU, sur les pixels satellites et la détection des incendies.'),
 'es': dict(title='Detecta el fuego desde el espacio: ¿qué tamaño tiene un píxel?', kicker='Actividad gratuita para el aula · 10–14 años · unos 60 minutos',
   desc='Una actividad gratuita en formato astroEDU: el alumnado superpone una cuadrícula gruesa y otra fina sobre un paisaje impreso para entender por qué el tamaño del píxel importa al detectar incendios, y luego compara con la escala real de FireSat (5×5 m).',
   intro='¿Puede un satélite pasar por alto un incendio porque sus «píxeles» son demasiado grandes? El alumnado coloca una cuadrícula gruesa y otra fina sobre un paisaje impreso con tres «fuegos» ocultos y comprueba cuáles detecta cada una. Después pasa la cuadrícula fina a metros y la compara con FireSat, que detecta fuegos de apenas 5×5 metros, unas dos plazas de aparcamiento (Earth Fire Alliance, 16 sept. 2026).',
   h_learn='Qué aprende el alumnado', learn=['Qué es un píxel en una imagen de satélite y por qué su tamaño limita lo que se puede detectar.', 'Aplicar una regla clara: un fuego se detecta si ocupa aproximadamente la mitad de una casilla o más.', 'La escala de detección de FireSat (5×5 m) comparada con la cuadrícula fina.', 'Por qué el detalle fino y las visitas frecuentes ayudan a combatir los incendios.'],
   h_need='Materiales', need='Fichas impresas (paisaje, cuadrícula gruesa, cuadrícula fina, ticket de salida), lápices y reglas. Lo ideal es papel vegetal o acetato transparente para las cuadrículas. Sin material de laboratorio. Opcional: una pantalla para la página de FireSat y el explorador de satélites.',
   h_steps='Cómo funciona', h_dl='Descarga la actividad', pdf='Guía docente y fichas (PDF, en inglés)', docx='Versión editable (Word .docx, en inglés)',
   h_more='Para ir más allá', more='Conoce la misión real en la <a href="FireSat.html">página de FireSat</a>, explora órbitas en el <a href="Satellite_Explorer.html">explorador de satélites</a> o crea una clase completa con el <a href="Lesson_Builder.html">generador de planes de clase</a>.',
   cap1='Los píxeles gruesos pueden pasar por alto un fuego pequeño que los píxeles finos (unos 5 m) detectan.', cap2='Los seis pasos de la actividad, para docentes.',
   alt1='Diagrama que compara una cuadrícula de píxeles gruesa que no ve un fuego pequeño con una cuadrícula fina de 5 metros que sí lo detecta', alt2='Diagrama de los seis pasos de la actividad en el aula',
   credit='Escrita en el formato de actividades <a href="https://astroedu.iau.org/" target="_blank" rel="noopener">astroEDU</a> (Oficina de Educación en Astronomía de la UAI). Compartida con licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es" target="_blank" rel="noopener">CC BY 4.0</a>: puedes copiarla, adaptarla y compartirla citando a Saving Planets. Datos de FireSat: comunicados de Earth Fire Alliance (7 jul. y 16 sept. 2026).',
   link='Actividad para el aula: detecta el fuego desde el espacio (¿qué tamaño tiene un píxel?)', linkp='Una clase gratuita e imprimible en formato astroEDU sobre píxeles de satélite y detección de incendios.'),
 'ar': dict(title='اكتشف الحريق من الفضاء: ما حجم البكسل؟', kicker='نشاط صفي مجاني · من 10 إلى 14 سنة · نحو 60 دقيقة',
   desc='نشاط صفي مجاني بصيغة astroEDU: يضع الطلاب شبكة كبيرة المربعات وأخرى دقيقة فوق منظر طبيعي مطبوع ليفهموا لماذا يهم حجم البكسل في رصد حرائق الغابات، ثم يقارنون النتائج بمقياس FireSat الحقيقي (5×5 أمتار).',
   intro='هل يمكن أن يفوت القمر الصناعي حريقًا لأن «البكسلات» كبيرة جدًا؟ يضع الطلاب شبكة كبيرة المربعات ثم شبكة دقيقة فوق منظر طبيعي مطبوع يخفي ثلاثة «حرائق»، ويختبرون أيها تكشفه كل شبكة. بعد ذلك يحوّلون الشبكة الدقيقة إلى أمتار ويقارنونها بـ FireSat الذي يرصد حرائق لا تتجاوز 5×5 أمتار، أي بحجم موقفين للسيارات تقريبًا (Earth Fire Alliance، 16 سبتمبر 2026).',
   h_learn='ماذا يتعلم الطلاب', learn=['ما البكسل في صورة القمر الصناعي، ولماذا يحدّ حجمه مما يمكن رصده.', 'تطبيق قاعدة واضحة: يُعدّ الحريق مرصودًا إذا ملأ نصف المربع تقريبًا أو أكثر.', 'مقياس الرصد في FireSat (5×5 أمتار) ومقارنته بالشبكة الدقيقة.', 'لماذا تساعد دقة التفاصيل وتكرار المرور على مواجهة الحرائق.'],
   h_need='المواد اللازمة', need='أوراق مطبوعة (المنظر الطبيعي، الشبكة الكبيرة، الشبكة الدقيقة، بطاقة الخروج)، وأقلام ومساطر. يُفضَّل ورق شفاف للشبكات. لا حاجة إلى معدات مختبر. اختياري: شاشة لعرض صفحة FireSat ومستكشف الأقمار الصناعية.',
   h_steps='خطوات النشاط', h_dl='تنزيل النشاط', pdf='دليل المعلم وأوراق العمل (PDF، بالإنجليزية)', docx='نسخة قابلة للتعديل (Word .docx، بالإنجليزية)',
   h_more='للمزيد', more='تعرّف على المهمة الحقيقية في <a href="FireSat.html">صفحة FireSat</a>، واستكشف المدارات في <a href="Satellite_Explorer.html">مستكشف الأقمار الصناعية</a>، أو أنشئ درسًا كاملًا في <a href="Lesson_Builder.html">منشئ خطط الدروس</a>.',
   cap1='قد تفوت البكسلات الكبيرة حريقًا صغيرًا ترصده البكسلات الدقيقة (نحو 5 أمتار).', cap2='الخطوات الست للنشاط، للمعلمين.',
   alt1='رسم يقارن شبكة بكسلات كبيرة تفوت حريقًا صغيرًا بشبكة دقيقة بحجم 5 أمتار ترصده', alt2='رسم تخطيطي للخطوات الست للنشاط الصفي',
   credit='مكتوب بصيغة أنشطة <a href="https://astroedu.iau.org/" target="_blank" rel="noopener">astroEDU</a> (مكتب الاتحاد الفلكي الدولي لتعليم الفلك). منشور بترخيص <a href="https://creativecommons.org/licenses/by/4.0/deed.ar" target="_blank" rel="noopener">CC BY 4.0</a>: يمكنك نسخه وتعديله ومشاركته مع ذكر Saving Planets. معلومات FireSat: بيانات Earth Fire Alliance (7 يوليو و16 سبتمبر 2026).',
   link='نشاط صفي: اكتشف الحريق من الفضاء (ما حجم البكسل؟)', linkp='درس مجاني قابل للطباعة بصيغة astroEDU عن بكسلات الأقمار الصناعية ورصد الحرائق.'),
 'it': dict(title='Avvista l’incendio dallo spazio: quanto è grande un pixel?', kicker='Attività gratuita per la classe · 10–14 anni · circa 60 minuti',
   desc='Un’attività gratuita in formato astroEDU: gli studenti sovrappongono una griglia larga e una fitta a un paesaggio stampato per capire perché la dimensione dei pixel conta nell’avvistare gli incendi, poi confrontano i risultati con la scala reale di FireSat (5×5 m).',
   intro='Un satellite può non accorgersi di un incendio perché i suoi «pixel» sono troppo grandi? Gli studenti appoggiano una griglia larga e poi una griglia fitta su un paesaggio stampato con tre «incendi» nascosti e verificano quali vengono rilevati da ciascuna. Poi convertono la griglia fitta in metri e la confrontano con FireSat, che rileva incendi grandi appena 5×5 metri, più o meno due posti auto (Earth Fire Alliance, 16 set. 2026).',
   h_learn='Che cosa imparano gli studenti', learn=['Che cos’è un pixel in un’immagine satellitare e perché la sua dimensione limita ciò che si può rilevare.', 'Come applicare una regola chiara: un incendio è rilevato solo se occupa circa metà di un quadrato o più.', 'La scala di rilevamento di FireSat (5×5 m) a confronto con la griglia fitta.', 'Perché dettagli fini e passaggi frequenti aiutano a contrastare gli incendi.'],
   h_need='Materiale', need='Schede stampate (paesaggio, griglia larga, griglia fitta, biglietto d’uscita), matite e righelli. L’ideale è carta da lucido o acetato trasparente per le griglie. Nessuna attrezzatura di laboratorio. Facoltativo: uno schermo per la pagina di FireSat e l’esploratore di satelliti.',
   h_steps='Come funziona', h_dl='Scarica l’attività', pdf='Guida per l’insegnante e schede (PDF, in inglese)', docx='Versione modificabile (Word .docx, in inglese)',
   h_more='Per approfondire', more='Scopri la missione reale nella <a href="FireSat.html">pagina di FireSat</a>, esplora le orbite con l’<a href="Satellite_Explorer.html">esploratore di satelliti</a> o prepara una lezione completa con il <a href="Lesson_Builder.html">generatore di piani di lezione</a>.',
   cap1='I pixel larghi possono non vedere un piccolo incendio che i pixel fitti (circa 5 m) rilevano.', cap2='Le sei fasi dell’attività, per l’insegnante.',
   alt1='Schema che confronta una griglia di pixel larga, che non vede un piccolo incendio, con una griglia fitta da 5 metri che lo rileva', alt2='Schema delle sei fasi dell’attività in classe',
   credit='Scritta nel formato delle attività <a href="https://astroedu.iau.org/" target="_blank" rel="noopener">astroEDU</a> (Ufficio IAU per la didattica dell’astronomia). Condivisa con licenza <a href="https://creativecommons.org/licenses/by/4.0/deed.it" target="_blank" rel="noopener">CC BY 4.0</a>: puoi copiarla, adattarla e condividerla citando Saving Planets. Dati su FireSat: comunicati di Earth Fire Alliance (7 lug. e 16 set. 2026).',
   link='Attività in classe: avvista l’incendio dallo spazio (quanto è grande un pixel?)', linkp='Una lezione gratuita e stampabile in formato astroEDU sui pixel satellitari e sul rilevamento degli incendi.'),
}

def href(l, page):  # language page if it exists, else English
    return page if l == 'en' or os.path.exists(d(l) + page) else '../' + page

def fix_links(l, s):
    for p in ('FireSat.html', 'Satellite_Explorer.html', 'Lesson_Builder.html'):
        s = s.replace(f'href="{p}"', f'href="{href(l, p)}"')
    return s

def fig(l, pre, img, w, h, alt, cap):
    return (f'<figure class="sf-fig"><img src="{pre}assets/astroedu/{img}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(cap)} <span class="si-credit">{esc(SI[l])}</span></figcaption></figure>')

def page_html(l):
    t = T[l]; shell = rd(d(l) + 'Kids_Map.html'); pre = '' if l == 'en' else '../'
    head = shell[:shell.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(t["title"])} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(t['desc']) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(t['title']) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?edu\.css[^"]*">', '', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('Kids_Map.html', PAGE)
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}{PAGE}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{PAGE}">'
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": t['title'], "description": t['desc'], "url": f"{SITE}{d(l)}{PAGE}", "inLanguage": l,
          "learningResourceType": "Classroom activity", "educationalLevel": "Ages 10-14", "timeRequired": "PT60M", "isAccessibleForFree": True,
          "license": "https://creativecommons.org/licenses/by/4.0/", "author": {"@type": "Organization", "name": "Saving Planets", "url": SITE},
          "encoding": [{"@type": "MediaObject", "contentUrl": f"{SITE}assets/docs/Spot_the_Fire_astroEDU.pdf", "encodingFormat": "application/pdf"},
                       {"@type": "MediaObject", "contentUrl": f"{SITE}assets/docs/Spot_the_Fire_astroEDU.docx", "encodingFormat": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}]}
    head += (f'<style>.sf-wrap{{max-width:900px;margin:0 auto;padding:1rem}}.sf-fig{{margin:1.2rem 0}}.sf-fig img{{width:100%;height:auto;border-radius:8px;background:#fff}}'
             f'.sf-fig figcaption{{font-size:.9rem;margin-top:.4rem}}.si-credit{{display:block;font-size:.8rem;opacity:.85;font-style:italic}}.sf-dl{{display:flex;flex-wrap:wrap;gap:.6rem}}.sf-credit{{font-size:.9rem}}</style>\n'
             f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    body_open = re.sub(r'class="[^"]*"', 'class="toc-sub spot-fire-page"', re.search(r'<body[^>]*>', shell).group(0), count=1)
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Kids_Map.html', PAGE), nav, flags=re.S)
    foot = shell[shell.index('</main>'):]
    foot = re.sub(r'<script src="(?:\.\./)?(?:edu|edu-extras)\.js[^"]*"[^>]*></script>', '', foot)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', foot)
    main = f'''<main id="main">
<section class="page-hero hero-kids"><div class="page-hero-content"><h1>{esc(t["title"])}</h1><p>{esc(t["kicker"])}</p></div></section>
<div class="sf-wrap">
<p class="edu-lead">{esc(t["intro"])}</p>
{fig(l, pre, "spot-fire-pixels.webp", 1200, 758, t["alt1"], t["cap1"])}
<h2>{esc(t["h_learn"])}</h2><ul>{"".join(f"<li>{esc(x)}</li>" for x in t["learn"])}</ul>
<h2>{esc(t["h_need"])}</h2><p>{esc(t["need"])}</p>
<h2>{esc(t["h_steps"])}</h2>
{fig(l, pre, "spot-fire-steps.webp", 1200, 812, t["alt2"], t["cap2"])}
<h2 id="download">{esc(t["h_dl"])}</h2>
<p class="sf-dl"><a class="btn" href="{pre}assets/docs/Spot_the_Fire_astroEDU.pdf" download>📄 {esc(t["pdf"])}</a> <a class="btn" href="{pre}assets/docs/Spot_the_Fire_astroEDU.docx" download>📝 {esc(t["docx"])}</a></p>
<h2>{esc(t["h_more"])}</h2><p>{fix_links(l, t["more"])}</p>
<p class="sf-credit">{t["credit"]}</p>
</div>
'''
    return head + '</head>\n' + body_open + nav + main + foot

def link_in(l):
    t = T[l]; n = 0
    blk = (f'<!-- SPOTFIRE-LINK:START --><section class="spotfire-link" aria-label="{esc(t["link"])}"><p><a class="btn" href="{PAGE}">🔥 {esc(t["link"])}</a></p>'
           f'<p>{esc(t["linkp"])}</p></section><!-- SPOTFIRE-LINK:END -->')
    for page in ('Teachers.html', 'Kids_Map.html', 'FireSat.html', 'Lesson_Builder.html'):
        p = d(l) + page
        if not os.path.exists(p): continue
        s = rd(p)
        if 'SPOTFIRE-LINK:START' in s: s2 = re.sub(r'<!-- SPOTFIRE-LINK:START -->.*?<!-- SPOTFIRE-LINK:END -->', lambda m: blk, s, flags=re.S)
        elif '</main>' in s: s2 = s.replace('</main>', blk + '</main>', 1)
        else: s2 = s
        n += wr(p, s2)
    return n

def sitemap():
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        loc = f'{SITE}{d(l)}{PAGE}'
        if f'<loc>{loc}</loc>' not in s:
            s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    wr('sitemap.xml', s)

if __name__ == '__main__':
    ch = 0
    for l in LANGS:
        ch += wr(d(l) + PAGE, page_html(l)); ch += link_in(l)
    sitemap()
    print(f'build-spotfire: langs={",".join(LANGS)} writes={ch}')
