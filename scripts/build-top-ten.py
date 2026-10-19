#!/usr/bin/env python3
"""Oct 18 2026 (owner-approved): Top_Ten.html, "This Week's Saving Planets Top Ten Features", ONE stable URL for X posts
(content can rotate weekly: edit FEATURES below). Owner design: clean page = banner + ten feature cards + the standard
site header/footer, nothing else in between (no video, newsletter box, share bar, related links or long intro).
EN page is generated here from the Glossary.html shell; fr/es/ar/it (+ hidden noindex he) come from i18n-build.py.
Live numbers (solutions, hubs) come from assets/data/solutions.json (same source as the homepage counters). This script
writes its own strings into each i18n/<lang>.json with the CURRENT numbers on every run, so translations never go stale.
Card visuals: real 2x screenshots of each feature page (2880x1800 PNG masters on R2, uploaded untouched by r2-upload.py
--srcset, which also made the WebP/AVIF sizes). Banner: NASA ISS photo (R2 master + its srcset). Run before i18n-build."""
import json, re, os, html, datetime, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, 'scripts'); import sp_banner as SPB  # shared animated banner (Oct 18)
SITE = 'https://www.savingplanets.com/'; PAGE = 'Top_Ten.html'
MF = json.load(open('assets/data/media-manifest.json', encoding='utf-8'))
SITED = json.load(open('assets/data/solutions.json', encoding='utf-8'))['site']
N, H = SITED['solutions'], SITED['hubs']
LANGS = ['fr', 'es', 'ar', 'it', 'he']
SI = 'Created by SI and Biological SI Partner'
BANNER = 'images/Pacific_Clouds_Sunset_ISS.jpg'
BANNER_OG = 'assets/top-ten/banner-2560.webp'   # local copy of the R2 2560 WebP size, used only as the share-card photo (build-og.py)
BANNER_CREDIT = 'NASA (ISS074-E-0046371, Jan. 3, 2026)'
# Each string: English -> {lang: translation}. '{n}' = live solution count, '{h}' = live hub count.
S = {
 'title': ("This Week's Saving Planets Top Ten Features", {
   'fr': "Le top 10 de la semaine sur Saving Planets", 'es': "Las 10 novedades destacadas de la semana en Saving Planets",
   'ar': "أفضل 10 ميزات في Saving Planets هذا الأسبوع", 'it': "La top ten della settimana di Saving Planets",
   'he': "עשר התכונות המובילות של Saving Planets השבוע"}),
 'sub': ("Ten things worth exploring this week, each one click away.", {
   'fr': "Dix choses à explorer cette semaine, chacune à un clic.", 'es': "Diez cosas que vale la pena explorar esta semana, cada una a un clic.",
   'ar': "عشرة أشياء تستحق الاستكشاف هذا الأسبوع، كلٌّ منها على بُعد نقرة.", 'it': "Dieci cose da esplorare questa settimana, ognuna a un clic.",
   'he': "עשרה דברים ששווה לגלות השבוע, כל אחד במרחק לחיצה."}),
 'desc': ("This week's top ten on Saving Planets: {n} real solutions, Myth vs Fact, the Weekly Brief, lessons from kids to PhD, the World Map, Roman and the new Polar hub.", {
   'fr': "Le top 10 de la semaine sur Saving Planets : {n} solutions réelles, Mythe ou réalité, le bulletin, des leçons de l'école au doctorat, la carte du monde, Roman et le pôle Polaire.",
   'es': "Lo mejor de la semana en Saving Planets: {n} soluciones reales, Mito o realidad, el boletín, lecciones de primaria a doctorado, el mapa mundial, Roman y el área Polar.",
   'ar': "أفضل 10 في Saving Planets هذا الأسبوع: {n} حلاً حقيقياً، وخرافة أم حقيقة، والنشرة الأسبوعية، ودروس من الأطفال إلى الدكتوراه، وخريطة العالم، ورومان، ومحور القطبين الجديد.",
   'it': "La top ten della settimana su Saving Planets: {n} soluzioni reali, Mito o realtà, il notiziario, lezioni dai bambini al dottorato, la mappa del mondo, Roman e il nuovo hub Poli.",
   'he': "עשרת המובילים של Saving Planets השבוע: {n} פתרונות אמיתיים, מיתוס מול עובדה, העלון השבועי, שיעורים מילדים ועד דוקטורט, מפת העולם, רומן ומרכז הקטבים החדש."}),
 'shot': ("Screenshot", {'fr': "Capture d'écran", 'es': "Captura de pantalla", 'ar': "لقطة شاشة", 'it': "Schermata", 'he': "צילום מסך"}),
 'nav': ("Top Ten", {'fr': "Top 10", 'es': "Top 10", 'ar': "أفضل 10", 'it': "Top 10", 'he': "עשרת המובילים"}),
 'photo': ("Photo", {'fr': "Photo", 'es': "Foto", 'ar': "صورة", 'it': "Foto", 'he': "תמונה"}),
}
# (id, page href, screenshot, extra credit, title, synopsis, button(s))
F = [
 ('solutions', 'Solutions.html', 'top10-solutions.png', '',
  ("{n} Solutions Saving the World", {'fr': "{n} solutions qui sauvent le monde", 'es': "{n} soluciones que salvan el mundo", 'ar': "{n} حلاً تنقذ العالم", 'it': "{n} soluzioni che salvano il mondo", 'he': "{n} פתרונות שמצילים את העולם"}),
  ("Real, sourced projects from the ocean floor to orbit, each explained with the Five W's. Browse all {h} hubs in one place.", {
   'fr': "De vrais projets sourcés, du fond des océans à l'orbite, chacun expliqué avec les cinq W. Parcourez les {h} pôles au même endroit.",
   'es': "Proyectos reales y con fuentes, del fondo del mar a la órbita, cada uno explicado con las cinco W. Recorre las {h} áreas en un solo lugar.",
   'ar': "مشاريع حقيقية موثّقة المصادر من قاع المحيط إلى المدار، كلٌّ منها مشروح بالأسئلة الخمسة. تصفّح المحاور الـ{h} في مكان واحد.",
   'it': "Progetti reali e con fonti, dal fondo dell'oceano all'orbita, ognuno spiegato con le cinque W. Sfoglia tutti gli {h} hub in un unico posto.",
   'he': "פרויקטים אמיתיים ומבוססי מקורות, מקרקעית האוקיינוס ועד המסלול, כל אחד מוסבר בחמשת ה-W. עיינו בכל {h} המרכזים במקום אחד."}),
  [('Solutions.html', ("Explore the solutions", {'fr': "Explorer les solutions", 'es': "Explorar las soluciones", 'ar': "استكشف الحلول", 'it': "Esplora le soluzioni", 'he': "גלו את הפתרונות"}))]),
 ('myths', 'Myth_vs_Fact.html', 'top10-myth.png', '',
  ("Myth vs Fact", {'fr': "Mythe ou réalité", 'es': "Mito o realidad", 'ar': "خرافة أم حقيقة", 'it': "Mito o realtà", 'he': "מיתוס מול עובדה"}),
  ("Doom myths about Earth and space, each checked against a NASA, NOAA, ESA or EPA source you can read yourself.", {
   'fr': "Les mythes catastrophistes sur la Terre et l'espace, chacun vérifié auprès d'une source de la NASA, de la NOAA, de l'ESA ou de l'EPA que vous pouvez lire vous-même.",
   'es': "Mitos catastrofistas sobre la Tierra y el espacio, cada uno contrastado con una fuente de la NASA, la NOAA, la ESA o la EPA que puedes leer tú mismo.",
   'ar': "خرافات التشاؤم عن الأرض والفضاء، كلٌّ منها مدقَّق مقابل مصدر من ناسا أو NOAA أو وكالة الفضاء الأوروبية أو وكالة حماية البيئة يمكنك قراءته بنفسك.",
   'it': "Miti catastrofisti sulla Terra e sullo spazio, ognuno verificato con una fonte NASA, NOAA, ESA o EPA che puoi leggere da te.",
   'he': "מיתוסי אבדון על כדור הארץ והחלל, כל אחד נבדק מול מקור של NASA, ‏NOAA, ‏ESA או EPA שאפשר לקרוא בעצמכם."}),
  [('Myth_vs_Fact.html', ("Bust a myth", {'fr': "Démonter un mythe", 'es': "Desmentir un mito", 'ar': "افضح خرافة", 'it': "Sfata un mito", 'he': "הפריכו מיתוס"}))]),
 ('brief', 'index.html#newsletter', 'top10-newsletter.png', '',
  ("Weekly News Brief", {'fr': "Le bulletin hebdomadaire", 'es': "Boletín semanal", 'ar': "النشرة الأسبوعية", 'it': "Notiziario settimanale", 'he': "העלון השבועי"}),
  ("New solutions, one amazing fact and upcoming launches in your inbox every Monday. Free, and you can unsubscribe anytime.", {
   'fr': "Nouvelles solutions, un fait étonnant et les prochains lancements dans votre boîte chaque lundi. Gratuit, désinscription à tout moment.",
   'es': "Nuevas soluciones, un dato asombroso y los próximos lanzamientos en tu correo cada lunes. Gratis, y puedes darte de baja cuando quieras.",
   'ar': "حلول جديدة وحقيقة مذهلة وعمليات الإطلاق القادمة في بريدك كل يوم اثنين. مجاناً، ويمكنك إلغاء الاشتراك في أي وقت.",
   'it': "Nuove soluzioni, un fatto sorprendente e i prossimi lanci nella tua casella ogni lunedì. Gratis, e puoi annullare l'iscrizione quando vuoi.",
   'he': "פתרונות חדשים, עובדה מדהימה אחת ושיגורים קרובים בתיבת הדואר שלכם בכל יום שני. בחינם, ואפשר לבטל בכל עת."}),
  [('index.html#newsletter', ("Sign up free", {'fr': "S'inscrire gratuitement", 'es': "Suscríbete gratis", 'ar': "اشترك مجاناً", 'it': "Iscriviti gratis", 'he': "הירשמו בחינם"}))]),
 ('learn', 'Learn.html', 'top10-learn.png', '',
  ("Education Hub, Kids to PhD", {'fr': "Espace éducation, de l'école au doctorat", 'es': "Centro educativo, de niños a doctorado", 'ar': "مركز التعليم، من الأطفال إلى الدكتوراه", 'it': "Hub educativo, dai bambini al dottorato", 'he': "מרכז הלמידה, מילדים ועד דוקטורט"}),
  ("Three tracks (orbital mechanics, aeronautical engineering and physics) at six levels, from a child's first question to research-grade derivations.", {
   'fr': "Trois parcours (mécanique orbitale, ingénierie aéronautique et physique) sur six niveaux, de la première question d'un enfant aux démonstrations de niveau recherche.",
   'es': "Tres itinerarios (mecánica orbital, ingeniería aeronáutica y física) en seis niveles, desde la primera pregunta de un niño hasta deducciones de nivel de investigación.",
   'ar': "ثلاثة مسارات (الميكانيكا المدارية وهندسة الطيران والفيزياء) على ستة مستويات، من أول سؤال لطفل إلى اشتقاقات بمستوى البحث العلمي.",
   'it': "Tre percorsi (meccanica orbitale, ingegneria aeronautica e fisica) su sei livelli, dalla prima domanda di un bambino alle dimostrazioni da ricerca.",
   'he': "שלושה מסלולים (מכניקה מסלולית, הנדסת אווירונאוטיקה ופיזיקה) בשש רמות, מהשאלה הראשונה של ילד ועד גזירות ברמת מחקר."}),
  [('Learn.html', ("Start learning", {'fr': "Commencer à apprendre", 'es': "Empieza a aprender", 'ar': "ابدأ التعلّم", 'it': "Inizia a imparare", 'he': "התחילו ללמוד"}))]),
 ('help', 'Ways_to_Help.html', 'top10-help.png', 'NPS',
  ("Ways to Help", {'fr': "Comment aider", 'es': "Formas de ayudar", 'ar': "طرق المساعدة", 'it': "Come aiutare", 'he': "דרכים לעזור"}),
  ("Donate, partner or roll up your sleeves: every listing links to the organization's own donation or volunteer page.", {
   'fr': "Donner, devenir partenaire ou retrousser vos manches : chaque fiche renvoie vers la page de don ou de bénévolat de l'organisation elle-même.",
   'es': "Dona, colabora o arremángate: cada ficha enlaza con la página oficial de donaciones o voluntariado de la organización.",
   'ar': "تبرّع أو كن شريكاً أو شمّر عن ساعديك: كل إدراج يرتبط بصفحة التبرع أو التطوع الخاصة بالمنظمة نفسها.",
   'it': "Dona, diventa partner o rimboccati le maniche: ogni scheda porta alla pagina ufficiale per donare o fare volontariato dell'organizzazione.",
   'he': "תרמו, היו שותפים או הפשילו שרוולים: כל רשומה מקשרת לדף התרומות או ההתנדבות של הארגון עצמו."}),
  [('Ways_to_Help.html', ("Find a way to help", {'fr': "Trouver comment aider", 'es': "Encuentra cómo ayudar", 'ar': "اعثر على طريقة للمساعدة", 'it': "Trova un modo per aiutare", 'he': "מצאו דרך לעזור"}))]),
 ('languages', None, 'top10-languages.png', 'NASA/JPL-Caltech/Space Science Institute',
  ("Read in 5 Languages", {'fr': "À lire en 5 langues", 'es': "Disponible en 5 idiomas", 'ar': "اقرأ بخمس لغات", 'it': "Da leggere in 5 lingue", 'he': "קראו ב-5 שפות"}),
  ("Every page reads in English, French, Spanish, Arabic and Italian, with a one-tap language switch at the top of the page.", {
   'fr': "Chaque page se lit en anglais, français, espagnol, arabe et italien, avec un sélecteur de langue en haut de la page.",
   'es': "Cada página se lee en inglés, francés, español, árabe e italiano, con un selector de idioma en la parte superior.",
   'ar': "كل صفحة تُقرأ بالإنجليزية والفرنسية والإسبانية والعربية والإيطالية، مع مبدّل لغة بلمسة واحدة أعلى الصفحة.",
   'it': "Ogni pagina si legge in inglese, francese, spagnolo, arabo e italiano, con un selettore di lingua in cima alla pagina.",
   'he': "כל דף זמין באנגלית, צרפתית, ספרדית, ערבית ואיטלקית, עם מתג שפה בלחיצה אחת בראש הדף."}),
  'LANGS'),
 ('lessons', 'Lesson_Builder.html', 'top10-lessons.png', 'USFWS',
  ("Lesson Plan Builder and Teacher Sheets", {'fr': "Créateur de plans de cours et fiches enseignants", 'es': "Creador de planes de clase y fichas docentes", 'ar': "منشئ خطط الدروس وأوراق المعلمين", 'it': "Generatore di lezioni e schede per insegnanti", 'he': "בונה מערכי שיעור ודפי מורים"}),
  ("Free printable lesson plans from K-3 to university, plus a one-page teacher sheet for every solution.", {
   'fr': "Des plans de cours gratuits et imprimables, de la maternelle à l'université, et une fiche enseignant d'une page pour chaque solution.",
   'es': "Planes de clase gratuitos e imprimibles, desde infantil hasta la universidad, y una ficha docente de una página para cada solución.",
   'ar': "خطط دروس مجانية قابلة للطباعة من الروضة حتى الجامعة، وورقة معلّم من صفحة واحدة لكل حل.",
   'it': "Piani di lezione gratuiti e stampabili, dall'infanzia all'università, più una scheda di una pagina per ogni soluzione.",
   'he': "מערכי שיעור חינמיים להדפסה מגן הילדים ועד האוניברסיטה, ודף מורה של עמוד אחד לכל פתרון."}),
  [('Lesson_Builder.html', ("Build a lesson", {'fr': "Créer une leçon", 'es': "Crear una clase", 'ar': "أنشئ درساً", 'it': "Crea una lezione", 'he': "בנו שיעור"})),
   ('Teachers.html', ("Teacher Sheets", {'fr': "Fiches enseignants", 'es': "Fichas docentes", 'ar': "أوراق المعلمين", 'it': "Schede per insegnanti", 'he': "דפי מורים"}))]),
 ('map', 'World_Map.html', 'top10-map.png', '© OpenStreetMap',
  ("Interactive World Map", {'fr': "Carte du monde interactive", 'es': "Mapa mundial interactivo", 'ar': "خريطة العالم التفاعلية", 'it': "Mappa del mondo interattiva", 'he': "מפת העולם האינטראקטיבית"}),
  ("All {n} solutions on one map: pick a hub and watch its solutions light up around the world.", {
   'fr': "Les {n} solutions sur une seule carte : choisissez un pôle et regardez ses solutions s'allumer partout dans le monde.",
   'es': "Las {n} soluciones en un solo mapa: elige un área y mira cómo sus soluciones se iluminan por todo el mundo.",
   'ar': "كل الحلول الـ{n} على خريطة واحدة: اختر محوراً وشاهد حلوله تضيء حول العالم.",
   'it': "Tutte le {n} soluzioni su un'unica mappa: scegli un hub e guarda le sue soluzioni illuminarsi in tutto il mondo.",
   'he': "כל {n} הפתרונות במפה אחת: בחרו מרכז וצפו בפתרונות שלו נדלקים ברחבי העולם."}),
  [('World_Map.html', ("Open the map", {'fr': "Ouvrir la carte", 'es': "Abrir el mapa", 'ar': "افتح الخريطة", 'it': "Apri la mappa", 'he': "פתחו את המפה"}))]),
 ('roman', 'Nancy_Grace_Roman.html', 'top10-roman.png', 'NASA',
  ("Nancy Grace Roman Tracker", {'fr': "Suivi du télescope Nancy Grace Roman", 'es': "Seguimiento del Nancy Grace Roman", 'ar': "متتبّع تلسكوب نانسي غريس رومان", 'it': "Tracker del Nancy Grace Roman", 'he': "מעקב טלסקופ ננסי גרייס רומן"}),
  ("Follow NASA's newest space telescope, launched Aug 30, 2026, on its way to L2: live distance from Earth, its newest image and what it will do.", {
   'fr': "Suivez le plus récent télescope spatial de la NASA, lancé le 30 août 2026, en route vers L2 : sa distance de la Terre en direct, sa dernière image et sa mission.",
   'es': "Sigue el telescopio espacial más reciente de la NASA, lanzado el 30 de agosto de 2026, rumbo a L2: su distancia a la Tierra en vivo, su imagen más reciente y lo que hará.",
   'ar': "تابع أحدث تلسكوب فضائي لناسا، الذي أُطلق في 30 أغسطس 2026، في طريقه إلى L2: بُعده عن الأرض مباشرةً، وأحدث صورة له، وما سيفعله.",
   'it': "Segui il più recente telescopio spaziale della NASA, lanciato il 30 agosto 2026, in viaggio verso L2: distanza dalla Terra in diretta, l'immagine più recente e cosa farà.",
   'he': "עקבו אחר טלסקופ החלל החדש ביותר של NASA, ששוגר ב-30 באוגוסט 2026, בדרכו ל-L2: מרחק חי מכדור הארץ, התמונה החדשה ביותר שלו ומה הוא יעשה."}),
  [('Nancy_Grace_Roman.html', ("Track Roman", {'fr': "Suivre Roman", 'es': "Seguir a Roman", 'ar': "تابع رومان", 'it': "Segui Roman", 'he': "עקבו אחר רומן"}))]),
 ('polar', 'Polar.html', 'top10-polar.png', 'NASA GSFC, Operation IceBridge',
  ("New: the Polar Hub", {'fr': "Nouveau : le pôle Polaire", 'es': "Nuevo: el área Polar", 'ar': "جديد: محور القطبين", 'it': "Novità: l'hub Poli", 'he': "חדש: מרכז הקטבים"}),
  ("Our newest hub: CryoSat, CRISTAL, CIMR, ICESat-2 and PREFIRE watch ice sheets, sea ice and the polar regions from space.", {
   'fr': "Notre pôle le plus récent : CryoSat, CRISTAL, CIMR, ICESat-2 et PREFIRE observent depuis l'espace les calottes glaciaires, la banquise et les régions polaires.",
   'es': "Nuestra área más reciente: CryoSat, CRISTAL, CIMR, ICESat-2 y PREFIRE vigilan desde el espacio los mantos de hielo, el hielo marino y las regiones polares.",
   'ar': "أحدث محاورنا: CryoSat وCRISTAL وCIMR وICESat-2 وPREFIRE ترصد من الفضاء الصفائح الجليدية والجليد البحري والمناطق القطبية.",
   'it': "Il nostro hub più recente: CryoSat, CRISTAL, CIMR, ICESat-2 e PREFIRE osservano dallo spazio calotte glaciali, ghiaccio marino e regioni polari.",
   'he': "המרכז החדש ביותר שלנו: CryoSat, ‏CRISTAL, ‏CIMR, ‏ICESat-2 ו-PREFIRE עוקבים מהחלל אחר יריעות קרח, קרח ים ואזורי הקטבים."}),
  [('Polar.html', ("Explore Polar", {'fr': "Explorer le pôle Polaire", 'es': "Explorar el área Polar", 'ar': "استكشف محور القطبين", 'it': "Esplora l'hub Poli", 'he': "גלו את מרכז הקטבים"}))]),
]
LANG_LINKS = [('EN', SITE), ('FR', SITE + 'fr/'), ('ES', SITE + 'es/'), ('العربية', SITE + 'ar/'), ('IT', SITE + 'it/')]  # public languages only
ALT = "Screenshot of the {t} page on Saving Planets"
ALT_T = {'fr': "Capture d'écran de la page {t} sur Saving Planets", 'es': "Captura de pantalla de la página {t} en Saving Planets", 'ar': "لقطة شاشة لصفحة {t} على Saving Planets",
         'it': "Schermata della pagina {t} su Saving Planets", 'he': "צילום מסך של הדף {t} ב-Saving Planets"}
def fill(x): return x.replace('{n}', str(N)).replace('{h}', str(H))
def esc(x): return html.escape(x, quote=False).replace('"', '&quot;')
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf-8').write(s); return 1
def pic(key, alt, sizes, eager=False):
    e = MF[key]
    srcs = ''.join(f'<source type="image/{t}" srcset="{esc(e[k])}" sizes="{sizes}">' for t, k in (('avif', 'srcset_avif'), ('webp', 'srcset')) if e.get(k))
    load = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return f'<picture>{srcs}<img src="{e["url"]}" alt="{esc(alt)}" width="{e["width"]}" height="{e["height"]}"{load}></picture>'
def strings():
    """every translatable string with its translations, numbers filled in"""
    out = [S['title'], S['sub'], S['desc'], S['shot'], S['photo'], S['nav']]
    for f in F:
        out += [f[4], f[5]] + ([b[1] for b in f[6]] if f[6] != 'LANGS' else [])
        t_en = fill(f[4][0]); out.append((ALT.format(t=t_en), {l: ALT_T[l].format(t=fill(f[4][1][l])) for l in LANGS}))
    out.append((f"{S['shot'][0]}: {SI}", {l: f"{S['shot'][1][l]}: " + {'fr': 'Créé par SI et Biological SI Partner', 'es': 'Creado por SI y Biological SI Partner',
               'ar': 'أُنشئ بواسطة SI وBiological SI Partner', 'it': 'Creato da SI e Biological SI Partner', 'he': 'נוצר על ידי SI ושותף SI ביולוגי'}[l] for l in LANGS}))
    out.append((f"{S['photo'][0]}: {BANNER_CREDIT}", {l: f"{S['photo'][1][l]}: {BANNER_CREDIT}" for l in LANGS}))
    return [(fill(en), {l: fill(tr[l]) for l in LANGS}) for en, tr in out]
def body():
    t = fill(S['title'][0])
    ban = SPB.banner(MF[BANNER], "An orbital sunset over the Pacific Ocean, seen from the International Space Station", t, fill(S["sub"][0]),
                     f'{S["photo"][0]}: {BANNER_CREDIT}', h1_id='tt-h', extra_class='tt-banner')
    cards = ''
    for i, (fid, href, shot, extra, title, syn, btns) in enumerate(F, 1):
        tt = fill(title[0]); key = 'images/top-ten/' + shot
        img = pic(key, ALT.format(t=tt), '(max-width:700px) 92vw, (max-width:1100px) 46vw, 520px')
        imgw = f'<a class="tt-img" href="{href}" tabindex="-1" aria-hidden="true">{img}</a>' if href else f'<div class="tt-img">{img}</div>'
        if btns == 'LANGS':
            bh = '<p class="tt-btns tt-langs">' + ''.join(f'<a class="tt-btn tt-lang" href="{u}" hreflang="{["en","fr","es","ar","it"][k]}" lang="{["en","fr","es","ar","it"][k]}">{esc(lab)}</a>' for k, (lab, u) in enumerate(LANG_LINKS)) + '</p>'
        else:
            bh = '<p class="tt-btns">' + ''.join(f'<a class="tt-btn{" tt-btn2" if k else ""}" href="{h}">{esc(fill(b[0]))}</a>' for k, (h, b) in enumerate(btns)) + '</p>'
        cred = f'{esc(S["shot"][0])}: {esc(SI)}' + (f' · {esc(extra)}' if extra else '')
        cards += (f'<article class="tt-card" id="{fid}"><span class="tt-num" aria-hidden="true">{i}</span>{imgw}<div class="tt-body">'
                  f'<h2>{esc(tt)}</h2><p>{esc(fill(syn[0]))}</p>{bh}<p class="tt-credit">{cred}</p></div></article>')
    return f'<!-- TOPTEN:START -->{ban}<div class="tt-grid">{cards}</div><!-- TOPTEN:END -->'
CSS = ('.top-ten-page main{padding:0}'
 '.tt-credit{font-size:.72rem;opacity:.75;margin:.6rem 0 0}'
 '.tt-grid{max-width:1180px;margin:2.2rem auto 3rem;padding:0 1.25rem;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6rem}'
 '.tt-card{position:relative;display:flex;flex-direction:column;background:#0f1b26;border:1px solid rgba(143,211,255,.18);border-radius:18px;overflow:hidden;box-shadow:0 10px 28px rgba(0,0,0,.4)}'
 '.tt-img{display:block;aspect-ratio:16/10;overflow:hidden;background:#061019;border-bottom:1px solid rgba(143,211,255,.15)}'
 '.tt-img img{width:100%;height:100%;object-fit:cover;object-position:50% 0;display:block;transition:transform .35s ease}a.tt-img:hover img{transform:scale(1.025)}'
 '.tt-num{position:absolute;z-index:2;top:.8rem;left:.8rem;min-width:2.4rem;height:2.4rem;padding:0 .5rem;border-radius:999px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.15rem;background:#009cde;color:#fff;box-shadow:0 4px 14px rgba(0,0,0,.45)}'
 '[dir=rtl] .tt-num{left:auto;right:.8rem}'
 '.tt-body{display:flex;flex-direction:column;flex:1;padding:1.1rem 1.25rem 1.1rem}.tt-body h2{margin:0 0 .45rem;font-size:1.35rem;line-height:1.2}.tt-body>p{margin:0 0 .9rem;line-height:1.5}'
 '.tt-btns{display:flex;flex-wrap:wrap;gap:.55rem;margin:auto 0 0 !important}'
 '.tt-btn{display:inline-flex;align-items:center;min-height:44px;padding:.55rem 1.1rem;border-radius:999px;background:#009cde;color:#fff !important;font-weight:700;text-decoration:none !important}'
 '.tt-btn::after{content:"\\2192";margin-inline-start:.45rem}[dir=rtl] .tt-btn::after{content:"\\2190"}.tt-lang::after,.tt-btn2::after{content:none}'
 '.tt-btn:hover,.tt-btn:focus-visible{background:#0b7fb5}.tt-btn2,.tt-lang{background:transparent;border:1.5px solid #8fd3ff;color:#e8eef5 !important}.tt-btn2:hover,.tt-lang:hover{background:rgba(143,211,255,.15)}'
 '@media (max-width:760px){.tt-grid{grid-template-columns:1fr}}')
def main():
    shell = rd('Glossary.html')
    head = shell[:shell.index('</head>')]
    t = fill(S['title'][0]); dsc = fill(S['desc'][0])
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(t)}</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(dsc) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(t) + '"', head)
    head = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*"', lambda m: m.group(1) + SITE + BANNER_OG + '"', head)
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', lambda m: m.group(1) + esc(t) + '"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('Glossary.html', PAGE)
    b = re.search(r'<body[^>]*>', shell).group(0)
    b = re.sub(r'class="[^"]*"', 'class="toc-sub top-ten-page"', b, count=1)
    if 'data-no-newsletter' not in b: b = b.replace('<body', '<body data-no-newsletter', 1)  # owner: no newsletter box on this page
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Glossary.html', PAGE), nav, flags=re.S)
    foot = shell[shell.index('</main>'):]
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', foot)
    page = head + '</head>\n' + b + nav + '<main id="main">\n' + body() + '\n' + foot
    ch = wr(PAGE, page)
    # translation memories: this page's strings with the current numbers
    for l in LANGS:
        p = f'i18n/{l}.json'; T = json.load(open(p, encoding='utf8')); n0 = dict(T)
        for en, tr in strings(): T[en] = tr[l]
        if T != n0: json.dump(T, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0); ch += 1
    css = rd('styles.css'); css2 = re.sub(r'\n?/\* TOPTEN:START \*/.*?/\* TOPTEN:END \*/\n?', '\n', css, flags=re.S).rstrip('\n') + '\n/* TOPTEN:START */\n' + CSS + '\n/* TOPTEN:END */\n'
    ch += wr('styles.css', css2)
    ch += SPB.write_css('styles.css')
    s = rd('sitemap.xml'); today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-10))).date().isoformat()
    for l in ['', 'fr/', 'es/', 'ar/', 'it/']:
        loc = f'{SITE}{l}{PAGE}'
        if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-top-ten: {N} solutions / {H} hubs, writes={ch}')
def links():
    """After i18n-build: card links to pages that exist in this language folder but are made by their own generators
    (Learn, World_Map: not in i18n/pages.txt) stay in the language (i18n-build pointed them at ../ English)."""
    ch = 0
    for l in LANGS:
        p = f'{l}/{PAGE}'
        if not os.path.exists(p): continue
        s = rd(p)
        def blk(m):
            return re.sub(r'href="\.\./([A-Za-z0-9_\-]+\.html)(#[^"]*)?"', lambda mm: f'href="{mm.group(1)}{mm.group(2) or ""}"' if os.path.exists(f'{l}/{mm.group(1)}') else mm.group(0), m.group(0))
        ch += wr(p, re.sub(r'<!-- TOPTEN:START -->.*?<!-- TOPTEN:END -->', blk, s, flags=re.S))
    print(f'build-top-ten --links: {ch} pages updated')
if __name__ == '__main__':
    import sys
    links() if '--links' in sys.argv else main()
