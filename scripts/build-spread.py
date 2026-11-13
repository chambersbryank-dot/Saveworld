#!/usr/bin/env python3
"""Spread_the_Word.html in six languages, plus platform-sized share images.
Captions use only claims already on the Press, Ways to Help, Courses and Teacher Sheets pages.
Images: NASA Blue Marble disc already on the site, plus the existing logo. Idempotent."""
import html, os, re
from PIL import Image, ImageDraw, ImageFont
SITE = 'https://www.savingplanets.com/'
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
BG = (6, 16, 24, 255)
FONT = 'assets/fonts/og/Montserrat.ttf'
AR_FONT = 'assets/fonts/og/NotoSansArabic.ttf'

def e(s): return html.escape(s, quote=True)
def words(s): return len(re.findall(r'\S+', s))
def home(lang):
    return SITE if lang == 'en' else f'{SITE}{lang}/'
def page(lang, name):
    return (SITE if lang == 'en' else f'{SITE}{lang}/') + name

# English blurbs are counted exactly. Translations are the same text, not padded to a word count.
BLURB50 = {
 'en': 'Saving Planets (savingplanets.com) tracks practical fixes for our planet: ocean, lake and river cleanups, forest restoration, and satellites and missions that watch Earth. It is free to read in six languages. Every figure is sourced. The site takes no donations. Every Donate button goes to the organization doing the work.',
 'fr': 'Saving Planets (savingplanets.com) suit des solutions concrètes pour notre planète : nettoyages d’océans, de lacs et de rivières, restauration des forêts, et satellites qui veillent sur la Terre. La lecture est gratuite en six langues. Chaque chiffre a une source. Le site ne reçoit aucun don : chaque bouton Faire un don va directement à l’organisation qui fait le travail.',
 'es': 'Saving Planets (savingplanets.com) sigue soluciones prácticas para nuestro planeta: limpiezas de océanos, lagos y ríos, restauración de bosques y satélites que vigilan la Tierra. Se lee gratis en seis idiomas. Cada cifra tiene una fuente. El sitio no recibe donaciones: cada botón Donar va directo a la organización que hace el trabajo.',
 'ar': 'يتابع Saving Planets (savingplanets.com) حلولاً عملية لكوكبنا: تنظيف المحيطات والبحيرات والأنهار، واستعادة الغابات، والأقمار التي تراقب الأرض. القراءة مجانية بست لغات. كل رقم له مصدر. الموقع لا يتلقى تبرعات: كل زر تبرع يذهب مباشرة إلى المنظمة التي تقوم بالعمل.',
 'it': 'Saving Planets (savingplanets.com) segue soluzioni pratiche per il nostro pianeta: pulizie di oceani, laghi e fiumi, ripristino delle foreste e satelliti che sorvegliano la Terra. Si legge gratis in sei lingue. Ogni cifra ha una fonte. Il sito non riceve donazioni: ogni pulsante Dona va diretto all’organizzazione che fa il lavoro.',
 'he': 'Saving Planets (savingplanets.com) עוקב אחר פתרונות מעשיים לכוכב שלנו: ניקוי אוקיינוסים, אגמים ונהרות, שיקום יערות, ולוויינים שצופים על כדור הארץ. הקריאה חינמית בשש שפות. לכל מספר יש מקור. האתר לא מקבל תרומות: כל כפתור תרומה הולך ישר לארגון שעושה את העבודה.',
}
BLURB100 = {
 'en': 'Saving Planets (savingplanets.com) is a website that tracks practical fixes for our planet: ocean, lake and river cleanups, forest restoration, and the satellites and missions that watch over Earth and protect it from space hazards. It is free to read in six languages. Every figure is sourced to NASA, ESA, JAXA, ISRO or NOAA, or to the organization doing the work. A free four-year aerospace and STEM study track is built one course at a time. Teacher sheets are a printable page for every solution. The site takes no donations: every Donate button goes to the organization doing the work.',
 'fr': 'Saving Planets (savingplanets.com) est un site indépendant qui suit des solutions concrètes pour notre planète : nettoyages d’océans, de lacs et de rivières, restauration des forêts, et satellites et missions qui veillent sur la Terre et la protègent des dangers venus de l’espace. La lecture est gratuite en anglais, français, espagnol, arabe, italien et hébreu. Chaque chiffre est sourcé auprès de la NASA, de l’ESA, de la JAXA, de l’ISRO ou de la NOAA, ou auprès de l’organisation qui fait le travail. Un parcours gratuit de quatre ans en aérospatiale et STEM se construit un cours à la fois, et les fiches enseignants sont un guide imprimable d’une page pour chaque solution. Le site ne reçoit aucun don. Sur Ways to Help, chaque bouton Faire un don va directement à l’organisation qui fait le travail.',
 'es': 'Saving Planets (savingplanets.com) es un sitio independiente que sigue soluciones prácticas para nuestro planeta: limpiezas de océanos, lagos y ríos, restauración de bosques, y satélites y misiones que vigilan la Tierra y la protegen de peligros del espacio. Se lee gratis en inglés, francés, español, árabe, italiano y hebreo. Cada cifra está respaldada por la NASA, la ESA, la JAXA, la ISRO o la NOAA, o por la organización que hace el trabajo. Un itinerario gratuito de cuatro años de ingeniería aeroespacial y STEM se construye curso a curso, y las fichas docentes son una guía imprimible de una página para cada solución. El sitio no recibe donaciones. En Ways to Help, cada botón Donar va directo a la organización que hace el trabajo.',
 'ar': 'Saving Planets (savingplanets.com) موقع مستقل يتابع حلولاً عملية لكوكبنا: تنظيف المحيطات والبحيرات والأنهار، واستعادة الغابات، والأقمار والمهمات التي تراقب الأرض وتحميها من أخطار الفضاء. القراءة مجانية بالإنجليزية والفرنسية والإسبانية والعربية والإيطالية والعبرية. كل رقم منسوب إلى ناسا أو وكالة الفضاء الأوروبية أو جاكسا أو إيسرو أو نوا، أو إلى المنظمة التي تقوم بالعمل. مسار مجاني لأربع سنوات في الطيران والفضاء وSTEM يُبنى دورة بعد دورة، وأوراق المعلمين دليل مطبوع من صفحة واحدة لكل حل. الموقع لا يتلقى تبرعات. في صفحة طرق المساعدة، كل زر تبرع يذهب مباشرة إلى المنظمة التي تقوم بالعمل.',
 'it': 'Saving Planets (savingplanets.com) è un sito indipendente che segue soluzioni pratiche per il nostro pianeta: pulizie di oceani, laghi e fiumi, ripristino delle foreste, e satelliti e missioni che sorvegliano la Terra e la proteggono dai pericoli dello spazio. Si legge gratis in inglese, francese, spagnolo, arabo, italiano ed ebraico. Ogni cifra è attribuita a NASA, ESA, JAXA, ISRO o NOAA, o all’organizzazione che fa il lavoro. Un percorso gratuito di quattro anni in ingegneria aerospaziale e STEM si costruisce un corso alla volta, e le schede insegnanti sono una guida stampabile di una pagina per ogni soluzione. Il sito non riceve donazioni. In Ways to Help, ogni pulsante Dona va diretto all’organizzazione che fa il lavoro.',
 'he': 'Saving Planets (savingplanets.com) הוא אתר עצמאי שעוקב אחר פתרונות מעשיים לכוכב שלנו: ניקוי אוקיינוסים, אגמים ונהרות, שיקום יערות, ולוויינים ומשימות שצופים על כדור הארץ ומגנים עליו מסכנות מהחלל. הקריאה חינמית באנגלית, צרפתית, ספרדית, ערבית, איטלקית ועברית. כל מספר מיוחס לנאס״א, לסוכנות החלל האירופית, לג׳אקסה, לאיסרו או ל-NOAA, או לארגון שעושה את העבודה. מסלול חינמי של ארבע שנים בהנדסת תעופה וחלל ו-STEM נבנה קורס אחר קורס, ודפי המורים הם מדריך להדפסה בן עמוד אחד לכל פתרון. האתר לא מקבל תרומות. בעמוד דרכים לעזור, כל כפתור תרומה הולך ישר לארגון שעושה את העבודה.',
}

def caps(lang):
    h, w, c, tch = home(lang), page(lang, 'Ways_to_Help.html'), page(lang, 'Courses.html'), page(lang, 'Teachers.html')
    # Facts are the Press boilerplate, the Ways to Help title, the Courses lead, and the Teacher Sheets description.
    text = {
     'en': {
        'hx': f'Saving Planets tracks practical fixes for Earth: ocean, lake and river cleanups, forest restoration, and satellites that watch Earth. Free to read, in six languages. Every figure is sourced. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) is an independent website that tracks practical fixes for our planet: ocean, lake and river cleanups, forest restoration, and the satellites and missions that watch over Earth and protect it from space hazards. It is published in English, French, Spanish, Arabic, Italian and Hebrew. Every figure is sourced to NASA, ESA, JAXA, ISRO or NOAA, or to the organization doing the work. #EarthObservation',
        'hfb': f'Saving Planets tracks practical fixes for our planet: cleanups of oceans, lakes and rivers, forest restoration, and the satellites that watch over Earth. It is free to read, in six languages, and every figure is sourced. {h}',
        'p1x': f'Saving Planets takes no donations. Every Donate button goes straight to the organization doing the work. Find ways to give or join them: {w} #EarthObservation',
        'p1li': f'Saving Planets takes no donations. Every Donate button on {w} goes straight to the organization doing the work, so you can give to or join the people cleaning oceans, lakes and rivers, restoring forests, and watching Earth from space. #EarthObservation',
        'p1fb': f'Want to help? Saving Planets does not take donations. Every Donate button goes straight to the organization doing the work. See the ways to give or join them: {w}',
        'p2x': f'A free four-year aerospace and STEM study track, built one course at a time, plus a printable teacher sheet for every solution. {c} #STEM',
        'p2li': f'Saving Planets publishes a free four-year aerospace and STEM (Science, Technology, Engineering and Mathematics) study track, built one course at a time: {c} Teacher sheets are a printable one-page guide for every solution: {tch} #STEM',
        'p2fb': f'Teachers and students can start a free four-year aerospace and STEM study track, one course at a time, and print a one-page teacher sheet for every solution. {c}',
     },
     'fr': {
        'hx': f'Saving Planets suit des solutions concrètes pour la Terre : nettoyages d’océans, de lacs et de rivières, restauration des forêts, et satellites qui veillent sur la Terre. Gratuit, en six langues. Chaque chiffre a une source. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) est un site indépendant qui suit des solutions concrètes : nettoyages d’océans, de lacs et de rivières, restauration des forêts, et satellites et missions qui veillent sur la Terre. Il est publié en six langues. Chaque chiffre est sourcé auprès de la NASA, de l’ESA, de la JAXA, de l’ISRO, de la NOAA, ou de l’organisation qui fait le travail. #EarthObservation',
        'hfb': f'Saving Planets suit des solutions concrètes pour notre planète : nettoyages, restauration des forêts, et satellites qui veillent sur la Terre. Gratuit, en six langues, et chaque chiffre a une source. {h}',
        'p1x': f'Saving Planets ne reçoit aucun don. Chaque bouton Faire un don va directement à l’organisation qui fait le travail. Voir comment donner ou participer : {w} #EarthObservation',
        'p1li': f'Saving Planets ne reçoit aucun don. Chaque bouton Faire un don sur {w} va directement à l’organisation qui fait le travail : nettoyages, forêts, et observation de la Terre depuis l’espace. #EarthObservation',
        'p1fb': f'Envie d’aider ? Saving Planets ne reçoit aucun don. Chaque bouton Faire un don va directement à l’organisation qui fait le travail. Les façons de donner ou de participer : {w}',
        'p2x': f'Un parcours gratuit de quatre ans en aérospatiale et STEM, construit un cours à la fois, plus une fiche enseignant imprimable pour chaque solution. {c} #STEM',
        'p2li': f'Saving Planets publie un parcours gratuit de quatre ans en aérospatiale et STEM (sciences, technologie, ingénierie et mathématiques), construit un cours à la fois : {c} Les fiches enseignants sont un guide imprimable d’une page pour chaque solution : {tch} #STEM',
        'p2fb': f'Enseignants et élèves peuvent commencer un parcours gratuit de quatre ans en aérospatiale et STEM, un cours à la fois, et imprimer une fiche d’une page pour chaque solution. {c}',
     },
     'es': {
        'hx': f'Saving Planets sigue soluciones prácticas para la Tierra: limpiezas de océanos, lagos y ríos, restauración de bosques y satélites que vigilan la Tierra. Gratis, en seis idiomas. Cada cifra tiene fuente. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) es un sitio independiente que sigue soluciones prácticas: limpiezas de océanos, lagos y ríos, restauración de bosques, y satélites y misiones que vigilan la Tierra. Está en seis idiomas. Cada cifra está respaldada por la NASA, la ESA, la JAXA, la ISRO, la NOAA o la organización que hace el trabajo. #EarthObservation',
        'hfb': f'Saving Planets sigue soluciones prácticas para nuestro planeta: limpiezas, restauración de bosques y satélites que vigilan la Tierra. Gratis, en seis idiomas, y cada cifra tiene fuente. {h}',
        'p1x': f'Saving Planets no recibe donaciones. Cada botón Donar va directo a la organización que hace el trabajo. Formas de dar o sumarse: {w} #EarthObservation',
        'p1li': f'Saving Planets no recibe donaciones. Cada botón Donar en {w} va directo a la organización que hace el trabajo: limpiezas, bosques y observación de la Tierra desde el espacio. #EarthObservation',
        'p1fb': f'¿Quieres ayudar? Saving Planets no recibe donaciones. Cada botón Donar va directo a la organización que hace el trabajo. Formas de dar o sumarse: {w}',
        'p2x': f'Un itinerario gratuito de cuatro años de ingeniería aeroespacial y STEM, curso a curso, más una ficha docente imprimible para cada solución. {c} #STEM',
        'p2li': f'Saving Planets publica un itinerario gratuito de cuatro años de ingeniería aeroespacial y STEM (ciencia, tecnología, ingeniería y matemáticas), construido curso a curso: {c} Las fichas docentes son una guía imprimible de una página para cada solución: {tch} #STEM',
        'p2fb': f'Docentes y estudiantes pueden empezar un itinerario gratuito de cuatro años de ingeniería aeroespacial y STEM, curso a curso, e imprimir una ficha de una página para cada solución. {c}',
     },
     'ar': {
        'hx': f'يتابع Saving Planets حلولاً عملية للأرض: تنظيف المحيطات والبحيرات والأنهار، واستعادة الغابات، وأقمار تراقب الأرض. مجاني، بست لغات. كل رقم له مصدر. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) موقع مستقل يتابع حلولاً عملية: تنظيف المحيطات والبحيرات والأنهار، واستعادة الغابات، وأقمار ومهمات تراقب الأرض. منشور بست لغات. كل رقم منسوب إلى ناسا أو وكالة الفضاء الأوروبية أو جاكسا أو إيسرو أو نوا، أو إلى المنظمة التي تقوم بالعمل. #EarthObservation',
        'hfb': f'يتابع Saving Planets حلولاً عملية لكوكبنا: التنظيف، واستعادة الغابات، والأقمار التي تراقب الأرض. مجاني بست لغات، وكل رقم له مصدر. {h}',
        'p1x': f'Saving Planets لا يتلقى تبرعات. كل زر تبرع يذهب مباشرة إلى المنظمة التي تقوم بالعمل. طرق العطاء أو المشاركة: {w} #EarthObservation',
        'p1li': f'Saving Planets لا يتلقى تبرعات. كل زر تبرع في {w} يذهب مباشرة إلى المنظمة التي تقوم بالعمل: التنظيف، والغابات، ومراقبة الأرض من الفضاء. #EarthObservation',
        'p1fb': f'تريد المساعدة؟ Saving Planets لا يتلقى تبرعات. كل زر تبرع يذهب مباشرة إلى المنظمة التي تقوم بالعمل. طرق العطاء أو المشاركة: {w}',
        'p2x': f'مسار مجاني لأربع سنوات في الطيران والفضاء وSTEM، يُبنى دورة بعد دورة، مع ورقة معلم قابلة للطباعة لكل حل. {c} #STEM',
        'p2li': f'ينشر Saving Planets مساراً مجانياً لأربع سنوات في الطيران والفضاء وSTEM (العلوم والتكنولوجيا والهندسة والرياضيات)، يُبنى دورة بعد دورة: {c} أوراق المعلمين دليل مطبوع من صفحة واحدة لكل حل: {tch} #STEM',
        'p2fb': f'يمكن للمعلمين والطلاب بدء مسار مجاني لأربع سنوات في الطيران والفضاء وSTEM، دورة بعد دورة، وطباعة ورقة من صفحة واحدة لكل حل. {c}',
     },
     'it': {
        'hx': f'Saving Planets segue soluzioni pratiche per la Terra: pulizie di oceani, laghi e fiumi, ripristino delle foreste e satelliti che sorvegliano la Terra. Gratis, in sei lingue. Ogni cifra ha una fonte. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) è un sito indipendente che segue soluzioni pratiche: pulizie di oceani, laghi e fiumi, ripristino delle foreste, e satelliti e missioni che sorvegliano la Terra. È in sei lingue. Ogni cifra è attribuita a NASA, ESA, JAXA, ISRO o NOAA, o all’organizzazione che fa il lavoro. #EarthObservation',
        'hfb': f'Saving Planets segue soluzioni pratiche per il nostro pianeta: pulizie, ripristino delle foreste e satelliti che sorvegliano la Terra. Gratis, in sei lingue, e ogni cifra ha una fonte. {h}',
        'p1x': f'Saving Planets non riceve donazioni. Ogni pulsante Dona va diretto all’organizzazione che fa il lavoro. Modi per dare o partecipare: {w} #EarthObservation',
        'p1li': f'Saving Planets non riceve donazioni. Ogni pulsante Dona su {w} va diretto all’organizzazione che fa il lavoro: pulizie, foreste e osservazione della Terra dallo spazio. #EarthObservation',
        'p1fb': f'Vuoi aiutare? Saving Planets non riceve donazioni. Ogni pulsante Dona va diretto all’organizzazione che fa il lavoro. Modi per dare o partecipare: {w}',
        'p2x': f'Un percorso gratuito di quattro anni in ingegneria aerospaziale e STEM, un corso alla volta, più una scheda insegnante stampabile per ogni soluzione. {c} #STEM',
        'p2li': f'Saving Planets pubblica un percorso gratuito di quattro anni in ingegneria aerospaziale e STEM (scienza, tecnologia, ingegneria e matematica), costruito un corso alla volta: {c} Le schede insegnanti sono una guida stampabile di una pagina per ogni soluzione: {tch} #STEM',
        'p2fb': f'Insegnanti e studenti possono iniziare un percorso gratuito di quattro anni in ingegneria aerospaziale e STEM, un corso alla volta, e stampare una scheda di una pagina per ogni soluzione. {c}',
     },
     'he': {
        'hx': f'Saving Planets עוקב אחר פתרונות מעשיים לכדור הארץ: ניקוי אוקיינוסים, אגמים ונהרות, שיקום יערות, ולוויינים שצופים על כדור הארץ. חינם, בשש שפות. לכל מספר יש מקור. {h} #EarthObservation',
        'hli': f'Saving Planets ({h}) הוא אתר עצמאי שעוקב אחר פתרונות מעשיים: ניקוי אוקיינוסים, אגמים ונהרות, שיקום יערות, ולוויינים ומשימות שצופים על כדור הארץ. הוא בשש שפות. כל מספר מיוחס לנאס״א, לסוכנות החלל האירופית, לג׳אקסה, לאיסרו או ל-NOAA, או לארגון שעושה את העבודה. #EarthObservation',
        'hfb': f'Saving Planets עוקב אחר פתרונות מעשיים לכוכב שלנו: ניקוי, שיקום יערות ולוויינים שצופים על כדור הארץ. חינם, בשש שפות, ולכל מספר יש מקור. {h}',
        'p1x': f'Saving Planets לא מקבל תרומות. כל כפתור תרומה הולך ישר לארגון שעושה את העבודה. דרכים לתת או להצטרף: {w} #EarthObservation',
        'p1li': f'Saving Planets לא מקבל תרומות. כל כפתור תרומה ב-{w} הולך ישר לארגון שעושה את העבודה: ניקוי, יערות ותצפית על כדור הארץ מהחלל. #EarthObservation',
        'p1fb': f'רוצים לעזור? Saving Planets לא מקבל תרומות. כל כפתור תרומה הולך ישר לארגון שעושה את העבודה. דרכים לתת או להצטרף: {w}',
        'p2x': f'מסלול חינמי של ארבע שנים בהנדסת תעופה וחלל ו-STEM, קורס אחר קורס, ועוד דף מורה להדפסה לכל פתרון. {c} #STEM',
        'p2li': f'Saving Planets מפרסם מסלול חינמי של ארבע שנים בהנדסת תעופה וחלל ו-STEM (מדע, טכנולוגיה, הנדסה ומתמטיקה), שנבנה קורס אחר קורס: {c} דפי המורים הם מדריך להדפסה בן עמוד אחד לכל פתרון: {tch} #STEM',
        'p2fb': f'מורים ותלמידים יכולים להתחיל מסלול חינמי של ארבע שנים בהנדסת תעופה וחלל ו-STEM, קורס אחר קורס, ולהדפיס דף של עמוד אחד לכל פתרון. {c}',
     },
    }[lang]
    for key in ('hx', 'p1x', 'p2x'):
        if len(text[key]) > 280: raise SystemExit(f'{lang} {key} is {len(text[key])} characters')
    return text

UI = {
 'en': dict(title='Spread the Word', lead='Ready-to-post words and pictures for the homepage, for planet-health solutions, and for the free STEM courses.',
            note='These lines use only what the Press, Ways to Help, Courses and Teacher Sheets pages already say. No new figures. SI, never AI.',
            pics='Share images', picsNote='Created by the Founder and SI. SI, never AI. Earth photograph: NASA Visible Earth / Blue Marble. Logo: created by the Founder and SI. Please keep both credits if you post a picture.',
            x='X', li='LinkedIn', fb='Facebook', copy='Copy', copied='Copied',
            home='Homepage', p1='Priority 1: planet-health solutions', p2='Priority 2: free STEM courses and teacher sheets',
            logos='Logo downloads', logosNote='Same files as on the Press page. Use the logo as provided, without changing its colors or proportions.',
            jpg='Logo, JPG (full size)', png='Logo, PNG (web size)', svg='Icon, SVG',
            blurbs='Newsletter and school-site text', w50='50 words', w100='100 words',
            badge='Link and badge', badgeNote='Paste this on a school site or newsletter. It loads no script.',
            dl='Download', src='These claims are already published on', press='Press', help='Ways to Help', courses='STEM Courses', teachers='Teacher Sheets'),
 'fr': dict(title='Faire passer le mot', lead='Textes et images prêts à publier pour la page d’accueil, les solutions pour la santé de la planète, et les cours STEM gratuits.',
            note='Ces lignes reprennent seulement ce que disent déjà les pages Presse, Ways to Help, Cours STEM et Fiches enseignants. Aucun chiffre nouveau. SI, jamais une IA.',
            pics='Images à partager', picsNote='Créées par le fondateur et SI. SI, jamais une IA. Photo de la Terre : NASA Visible Earth / Blue Marble. Logo : créé par le fondateur et SI. Gardez les deux crédits si vous publiez une image.',
            x='X', li='LinkedIn', fb='Facebook', copy='Copier', copied='Copié',
            home='Page d’accueil', p1='Priorité 1 : solutions pour la santé de la planète', p2='Priorité 2 : cours STEM gratuits et fiches enseignants',
            logos='Téléchargement du logo', logosNote='Les mêmes fichiers que sur la page Presse. Utilisez le logo tel quel, sans changer ses couleurs ni ses proportions.',
            jpg='Logo, JPG (taille originale)', png='Logo, PNG (taille web)', svg='Icône, SVG',
            blurbs='Texte pour une infolettre ou un site d’école', w50='50 mots', w100='100 mots',
            badge='Lien et badge', badgeNote='Collez ceci sur un site d’école ou dans une infolettre. Aucun script n’est chargé.',
            dl='Télécharger', src='Ces faits sont déjà publiés sur', press='Presse', help='Ways to Help', courses='Cours STEM', teachers='Fiches enseignants'),
 'es': dict(title='Correr la voz', lead='Textos e imágenes listos para publicar: la portada, las soluciones para la salud del planeta y los cursos STEM gratuitos.',
            note='Estas líneas usan solo lo que ya dicen las páginas de Prensa, Ways to Help, Cursos STEM y Fichas docentes. Ninguna cifra nueva. SI, nunca una IA.',
            pics='Imágenes para compartir', picsNote='Creadas por el fundador y SI. SI, nunca una IA. Fotografía de la Tierra: NASA Visible Earth / Blue Marble. Logo: creado por el fundador y SI. Conserve ambos créditos si publica una imagen.',
            x='X', li='LinkedIn', fb='Facebook', copy='Copiar', copied='Copiado',
            home='Portada', p1='Prioridad 1: soluciones para la salud del planeta', p2='Prioridad 2: cursos STEM gratuitos y fichas docentes',
            logos='Descargas del logo', logosNote='Los mismos archivos que en la página de Prensa. Use el logo tal cual, sin cambiar colores ni proporciones.',
            jpg='Logo, JPG (tamaño completo)', png='Logo, PNG (tamaño web)', svg='Icono, SVG',
            blurbs='Texto para un boletín o un sitio escolar', w50='50 palabras', w100='100 palabras',
            badge='Enlace e insignia', badgeNote='Péguelo en un sitio escolar o un boletín. No carga ningún script.',
            dl='Descargar', src='Estos datos ya están publicados en', press='Prensa', help='Ways to Help', courses='Cursos STEM', teachers='Fichas docentes'),
 'ar': dict(title='انشر الخبر', lead='نصوص وصور جاهزة للنشر: للصفحة الرئيسية، ولحلول صحة الكوكب، ولدورات STEM المجانية.',
            note='هذه السطور تستخدم فقط ما تقوله صفحات الصحافة وطرق المساعدة ودورات STEM وأوراق المعلمين. لا أرقام جديدة. SI، وليس الذكاء الاصطناعي.',
            pics='صور للمشاركة', picsNote='أنشأها المؤسس وSI. SI، وليس الذكاء الاصطناعي. صورة الأرض: NASA Visible Earth / Blue Marble. الشعار: أنشأه المؤسس وSI. أبقِ كلا الإسنادين إذا نشرت صورة.',
            x='X', li='LinkedIn', fb='Facebook', copy='نسخ', copied='تم النسخ',
            home='الصفحة الرئيسية', p1='الأولوية 1: حلول صحة الكوكب', p2='الأولوية 2: دورات STEM المجانية وأوراق المعلمين',
            logos='تنزيل الشعار', logosNote='الملفات نفسها الموجودة في صفحة الصحافة. استخدم الشعار كما هو، دون تغيير ألوانه أو نسبه.',
            jpg='الشعار، JPG (الحجم الكامل)', png='الشعار، PNG (حجم الويب)', svg='الأيقونة، SVG',
            blurbs='نص لنشرة أو لموقع مدرسة', w50='50 كلمة', w100='100 كلمة',
            badge='رابط وشارة', badgeNote='الصق هذا في موقع مدرسة أو نشرة. لا يُحمَّل أي سكربت.',
            dl='تنزيل', src='هذه الوقائع منشورة بالفعل في', press='الصحافة', help='طرق المساعدة', courses='دورات STEM', teachers='أوراق المعلمين'),
 'it': dict(title='Far girare la voce', lead='Testi e immagini pronti da pubblicare per la pagina iniziale, le soluzioni per la salute del pianeta e i corsi STEM gratuiti.',
            note='Queste righe usano solo ciò che dicono già le pagine Stampa, Ways to Help, Corsi STEM e Schede insegnanti. Nessuna cifra nuova. SI, mai un’IA.',
            pics='Immagini da condividere', picsNote='Create dal fondatore e da SI. SI, mai un’IA. Fotografia della Terra: NASA Visible Earth / Blue Marble. Logo: creato dal fondatore e da SI. Tieni entrambi i crediti se pubblichi un’immagine.',
            x='X', li='LinkedIn', fb='Facebook', copy='Copia', copied='Copiato',
            home='Pagina iniziale', p1='Priorità 1: soluzioni per la salute del pianeta', p2='Priorità 2: corsi STEM gratuiti e schede insegnanti',
            logos='Download del logo', logosNote='Gli stessi file della pagina Stampa. Usa il logo così com’è, senza cambiarne colori o proporzioni.',
            jpg='Logo, JPG (dimensione intera)', png='Logo, PNG (dimensione web)', svg='Icona, SVG',
            blurbs='Testo per una newsletter o un sito scolastico', w50='50 parole', w100='100 parole',
            badge='Link e badge', badgeNote='Incollalo in un sito scolastico o in una newsletter. Non carica alcuno script.',
            dl='Scarica', src='Questi fatti sono già pubblicati su', press='Stampa', help='Ways to Help', courses='Corsi STEM', teachers='Schede insegnanti'),
 'he': dict(title='להפיץ את הבשורה', lead='טקסטים ותמונות מוכנים לפרסום: לעמוד הבית, לפתרונות לבריאות כוכב הלכת, ולקורסי STEM החינמיים.',
            note='השורות האלה משתמשות רק במה שכבר כתוב בעמודי העיתונות, דרכים לעזור, קורסי STEM ודפי המורים. אין מספרים חדשים. SI, אף פעם לא בינה מלאכותית.',
            pics='תמונות לשיתוף', picsNote='נוצרו על ידי המייסד ו-SI. SI, אף פעם לא בינה מלאכותית. תצלום כדור הארץ: NASA Visible Earth / Blue Marble. הלוגו: נוצר על ידי המייסד ו-SI. שמרו על שני הקרדיטים אם מפרסמים תמונה.',
            x='X', li='LinkedIn', fb='Facebook', copy='העתקה', copied='הועתק',
            home='עמוד הבית', p1='עדיפות 1: פתרונות לבריאות כוכב הלכת', p2='עדיפות 2: קורסי STEM חינמיים ודפי מורים',
            logos='הורדת הלוגו', logosNote='אותם קבצים כמו בעמוד העיתונות. השתמשו בלוגו כפי שהוא, בלי לשנות צבעים או פרופורציות.',
            jpg='לוגו, JPG (גודל מלא)', png='לוגו, PNG (גודל לרשת)', svg='אייקון, SVG',
            blurbs='טקסט לניוזלטר או לאתר בית ספר', w50='50 מילים', w100='100 מילים',
            badge='קישור ותג', badgeNote='הדביקו את זה באתר בית ספר או בניוזלטר. לא נטען שום סקריפט.',
            dl='הורדה', src='העובדות האלה כבר מפורסמות ב', press='עיתונות', help='דרכים לעזור', courses='קורסי STEM', teachers='דפי מורים'),
}

def make_images():
    os.makedirs('assets/share', exist_ok=True)
    disc = Image.open('assets/earth/blue-marble-disc-lg.webp').convert('RGBA')
    logo = Image.open('assets/SavePlanetLogo-email.png').convert('RGBA')
    font = ImageFont.truetype(FONT, 54)
    font_s = ImageFont.truetype(FONT, 28)
    font_c = ImageFont.truetype(FONT, 18)
    sizes = {'x': (1200, 675), 'li': (1200, 627), 'fb': (1200, 630), 'portrait': (1080, 1350)}
    for key, (w, h) in sizes.items():
        canvas = Image.new('RGBA', (w, h), BG)
        if key == 'portrait':
            d = int(min(w, h) * 0.72)
            globe = disc.resize((d, d), Image.Resampling.LANCZOS)
            canvas.alpha_composite(globe, ((w - d) // 2, 80))
            mark = logo.resize((120, 120), Image.Resampling.LANCZOS)
            canvas.alpha_composite(mark, ((w - 120) // 2, 80 + d + 36))
            draw = ImageDraw.Draw(canvas)
            draw.text((w / 2, 80 + d + 180), 'Saving Planets', font=font, fill=(255, 255, 255, 255), anchor='ma')
            draw.text((w / 2, 80 + d + 250), 'savingplanets.com', font=font_s, fill=(210, 230, 245, 255), anchor='ma')
            credit = 'Created by the Founder and SI. SI, never AI.'
            draw.text((w / 2, h - 70), credit, font=font_c, fill=(190, 210, 225, 255), anchor='ma')
            draw.text((w / 2, h - 42), 'Earth: NASA Visible Earth / Blue Marble', font=font_c, fill=(190, 210, 225, 255), anchor='ma')
        else:
            d = int(h * 0.86)
            globe = disc.resize((d, d), Image.Resampling.LANCZOS)
            canvas.alpha_composite(globe, (36, (h - d) // 2))
            mark = logo.resize((84, 84), Image.Resampling.LANCZOS)
            tx = 36 + d + 28
            canvas.alpha_composite(mark, (tx, 70))
            draw = ImageDraw.Draw(canvas)
            draw.text((tx, 170), 'Saving Planets', font=font, fill=(255, 255, 255, 255))
            draw.text((tx, 240), 'savingplanets.com', font=font_s, fill=(210, 230, 245, 255))
            draw.text((tx, h - 78), 'Created by the Founder and SI.', font=font_c, fill=(190, 210, 225, 255))
            draw.text((tx, h - 52), 'SI, never AI.', font=font_c, fill=(190, 210, 225, 255))
            draw.text((tx, h - 28), 'Earth: NASA Visible Earth / Blue Marble', font=font_c, fill=(190, 210, 225, 255))
        out = canvas.convert('RGB')
        path = f'assets/share/spread-{key}.jpg'
        out.save(path, 'JPEG', quality=88, optimize=True)
        check = Image.open(path)
        if check.size != (w, h): raise SystemExit(path)
    print('share images ok')

def block(lang, cid, text, ui):
    return (f'<p class="stw-cap" id="{cid}">{e(text)}</p>'
            f'<div class="stw-row"><button type="button" class="share-btn" data-copy="{cid}" data-label="{e(ui["copy"])}" data-copied="{e(ui["copied"])}" aria-label="{e(ui["copy"])}">{e(ui["copy"])}</button>'
            f'<span class="share-ok" role="status" aria-live="polite"></span></div>')

def main_html(lang, pre):
    ui = UI[lang]
    c = caps(lang)
    h, w, courses, teachers = home(lang), page(lang, 'Ways_to_Help.html'), page(lang, 'Courses.html'), page(lang, 'Teachers.html')
    groups = [('home', ui['home']), ('p1', ui['p1']), ('p2', ui['p2'])]
    posts = ''
    for gid, label in groups:
        posts += f'<h3>{e(label)}</h3>'
        for net, nk in (('x', 'x'), ('li', 'li'), ('fb', 'fb')):
            key = {'home': 'h', 'p1': 'p1', 'p2': 'p2'}[gid] + net
            posts += f'<h4>{e(ui[net])}</h4>' + block(lang, f'{gid}-{net}', c[key], ui)
    imgs = ''
    files = [('x', '1200×675', 'X'), ('li', '1200×627', 'LinkedIn'), ('fb', '1200×630', 'Facebook'), ('portrait', '1080×1350', 'portrait')]
    for key, size, name in files:
        src = f'{pre}assets/share/spread-{key}.jpg'
        imgs += (f'<figure><img src="{src}" alt="{e(ui["pics"])}, {e(name)}, {size}" width="{size.split("×")[0]}" height="{size.split("×")[1]}" loading="lazy" decoding="async">'
                 f'<figcaption><a class="share-btn" href="{src}" download>{e(ui["dl"])}: {e(name)} ({size})</a></figcaption></figure>')
    badge = (f'<a href="{h}"><img alt="Saving Planets" src="https://www.savingplanets.com/assets/SavePlanetLogo-email.png" width="64" height="64"> Saving Planets</a>')
    text_link = f'<a href="{h}">Saving Planets</a>'
    return f'''<nav aria-label="Breadcrumb" class="breadcrumb" hidden><ol><li><a href="{pre}index.html">{e(ui["home"] if lang != "en" else "Home")}</a></li><li><span aria-current="page">{e(ui["title"])}</span></li></ol></nav>
<div class="stw">
<p class="stw-note">{e(ui["note"])}</p>
<p class="stw-note">{e(ui["src"])}: <a href="{pre}Press.html">{e(ui["press"])}</a>, <a href="{pre}Ways_to_Help.html">{e(ui["help"])}</a>, <a href="{pre}Courses.html">{e(ui["courses"])}</a>, <a href="{pre}Teachers.html">{e(ui["teachers"])}</a>.</p>
{posts}
<h2>{e(ui["pics"])}</h2>
<p class="stw-note">{e(ui["picsNote"])}</p>
{imgs}
<h2>{e(ui["logos"])}</h2>
<p class="stw-note">{e(ui["logosNote"])}</p>
<div class="press-logos"><figure class="press-logo"><img src="{pre}assets/SavePlanetLogo.jpg" alt="Saving Planets logo" width="1024" height="1024" loading="lazy" decoding="async"><figcaption><a href="{pre}assets/SavePlanetLogo.jpg" download>{e(ui["jpg"])}</a></figcaption></figure><figure class="press-logo"><img src="{pre}assets/SavePlanetLogo-email.png" alt="Saving Planets logo, web version" width="512" height="512" loading="lazy" decoding="async"><figcaption><a href="{pre}assets/SavePlanetLogo-email.png" download>{e(ui["png"])}</a></figcaption></figure><figure class="press-logo"><img src="{pre}favicon.svg" alt="Saving Planets icon" width="160" height="160" loading="lazy" decoding="async"><figcaption><a href="{pre}favicon.svg" download>{e(ui["svg"])}</a></figcaption></figure></div>
<h2>{e(ui["blurbs"])}</h2>
<h3>{e(ui["w50"])}</h3>
{block(lang, "b50", BLURB50[lang], ui)}
<h3>{e(ui["w100"])}</h3>
{block(lang, "b100", BLURB100[lang], ui)}
<h2>{e(ui["badge"])}</h2>
<p class="stw-note">{e(ui["badgeNote"])}</p>
{block(lang, "badge", badge, ui)}
{block(lang, "textlink", text_link, ui)}
</div></main>'''

def build_pages():
    assert words(BLURB50['en']) == 50, words(BLURB50['en'])
    assert words(BLURB100['en']) == 100, words(BLURB100['en'])
    for lang in LANGS:
        src = 'Press.html' if lang == 'en' else f'{lang}/Press.html'
        s = open(src, encoding='utf-8').read()
        s = s.replace('Press.html', 'Spread_the_Word.html')
        ui = UI[lang]
        desc = ui['lead']
        s = re.sub(r'<title>.*?</title>', f'<title>{e(ui["title"])} | Saving Planets</title>', s, count=1, flags=re.S)
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            s = re.sub(rf'(<meta {attr} content=")[^"]*"', rf'\1{e(desc)}"', s)
        for attr in ('property="og:title"', 'name="twitter:title"'):
            s = re.sub(rf'(<meta {attr} content=")[^"]*"', rf'\1{e(ui["title"])} | Saving Planets"', s)
        s = re.sub(r'("@type": "WebPage", "name": ")[^"]*"', rf'\1{ui["title"]}"', s)
        s = re.sub(r'(<div class="page-hero-content"><h1>)[^<]*(</h1>)<p>[^<]*</p>', rf'\1{e(ui["title"])}\2<p>{e(ui["lead"])}</p>', s, count=1)
        pre = '' if lang == 'en' else '../'
        body = main_html(lang, pre)
        s2, n = re.subn(r'<nav aria-label="[^"]*" class="breadcrumb".*?</main>', body, s, count=1, flags=re.S)
        if n != 1: raise SystemExit(f'breadcrumb replace failed {lang}')
        dest = 'Spread_the_Word.html' if lang == 'en' else f'{lang}/Spread_the_Word.html'
        open(dest, 'w', encoding='utf-8').write(s2)
        if 'dir="rtl"' not in s2[:400] and lang in ('ar', 'he'): raise SystemExit('rtl missing ' + lang)
        if 'noindex' in s2.lower(): raise SystemExit('noindex ' + lang)
    print('spread pages ok', words(BLURB50['en']), words(BLURB100['en']))

def sitemaps():
    import sys
    sys.path.insert(0, 'scripts')
    import sitemap_pages
    n = 0
    for lang in LANGS:
        loc = page(lang, 'Spread_the_Word.html') if lang != 'en' else SITE + 'Spread_the_Word.html'
        # page() for en uses SITE+name which is correct
        loc = SITE + 'Spread_the_Word.html' if lang == 'en' else f'{SITE}{lang}/Spread_the_Word.html'
        n += sitemap_pages.ensure_url(loc, '2026-11-13', 'monthly', '0.6')
    print('sitemap inserts', n)

if __name__ == '__main__':
    make_images()
    build_pages()
    sitemaps()
