#!/usr/bin/env python3
"""Teachers page home (Nov 11). Collapses the 11 hubs and the course list, and
builds the path strip, starter kits, and card catalog from the pages already
on the site. Counts come from those lists and from assets/data/standards.json.

Run from the repo root:
  python3 scripts/build-teachers-home.py --tags-only
  python3 scripts/build-standards.py
  python3 scripts/build-teachers-home.py

Does not edit footer-v2, the Cloudflare beacon, or solution pages (build-standards
writes the standards block on a sheet when --tags-only has updated the JSON).
"""
import html, json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = lambda s: html.escape(s if s is not None else '', quote=True)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
BANDS = ['K-2', '3-5', '6-8', '9-12']
SUBJ_ORDER = ['earth', 'life', 'space', 'literacy']
ASSET = '20261111e'

# Codes already defined in standards.json. Nothing new is invented here.
RI = 'CCSS.ELA-LITERACY.RI.5.9'
RST = 'CCSS.ELA-LITERACY.RST.6-8.1'
FULL = ['K-ESS3-3', '5-ESS3-1', 'MS-ESS3-3', 'MS-LS2-5', 'HS-ESS3-4', RI, RST]
CARB = ['K-ESS3-3', '5-ESS3-1', 'MS-ESS3-3', 'HS-ESS3-4', RI, RST]
PERMA = ['4-ESS3-2', '5-ESS3-1', 'MS-ESS3-2', 'MS-ESS3-3', 'HS-ESS3-4', RI, RST]
SMART = ['4-ESS3-2', '5-ESS3-1', 'MS-ESS3-2', 'MS-ESS3-3', RI, RST]
SAT = ['5-ESS3-1', 'MS-ESS3-3', RI, RST]
WEATHER = ['4-ESS3-2', 'MS-ESS3-2', 'MS-ESS3-3', RI, RST]
MONITOR = ['MS-ESS3-3', RST]
ADVICE = ['5-ESS3-1', 'MS-ESS3-3', RI, RST]
CENSUS = ['5-ESS3-1', 'MS-ESS3-3', RI, RST]
SEED = ['MS-LS2-5', RST]
READ = [RST]
# Reading-only: the sheet does not clearly support a science expectation in this set.
PARTIAL = {
    'Beyond_EPICA_Oldest_Ice.html': 'Ice-core research on past climate cycles. None of the science expectations in standards.json match that work.',
    'SOOS.html': 'A Southern Ocean data network. The sheet does not describe a solution a science expectation covers.',
    'Inuit_Circumpolar_Council.html': 'Advocacy for Inuit rights. The sheet does not describe a science solution.',
    'Arctic_Basecamp.html': 'Science communication with leaders. The sheet does not describe a student design solution covered by the coded expectations.',
    'Ice_Memory_Sanctuary.html': 'An ice-core archive in a cave. It is not on the Teachers list. No science expectation in this set matches storing cores for later study.',
}
PAGE_TAGS = {}
for p in ['ASOC_Antarctic_Coalition.html', 'CAFF_Arctic_Biodiversity.html', 'CCAMLR.html', 'Gough_Island_Restoration.html',
          'IAATO.html', 'Iceland_Land_Restoration.html', 'PAME_Arctic_Council.html', 'Polar_Bears_International.html',
          'Ross_Sea_MPA.html', 'South_Georgia_Habitat_Restoration.html', 'Tallurutiup_Imanga_NMCA.html', 'WWF_Arctic_Programme.html']:
    PAGE_TAGS[p] = FULL
PAGE_TAGS['Carbfix.html'] = CARB
PAGE_TAGS['Permafrost_Pathways.html'] = PERMA
PAGE_TAGS['SmartICE.html'] = SMART
for p in ['CIMR.html', 'CRISTAL.html', 'CryoSat.html', 'ICESat-2.html', 'PREFIRE.html', 'GCOM-W_SHIZUKU.html',
          'PROMICE_GC-Net.html', 'SOCCOM.html', 'SCISAT.html']:
    PAGE_TAGS[p] = SAT
PAGE_TAGS['Arctic_Weather_Satellite.html'] = WEATHER
PAGE_TAGS['Thwaites_Glacier_Collaboration.html'] = MONITOR
PAGE_TAGS['MOSAiC_Expedition.html'] = MONITOR
PAGE_TAGS['SCAR_Antarctic_Research.html'] = ADVICE
PAGE_TAGS['Oceanites_Penguin_Census.html'] = CENSUS
PAGE_TAGS['Penguin_Watch.html'] = CENSUS
PAGE_TAGS['Svalbard_Global_Seed_Vault.html'] = SEED
for p in PARTIAL:
    PAGE_TAGS[p] = READ

TIME_PHRASE = {
    'en': 'Plan on 15 weeks, about 6 to 9 hours a week',
    'fr': 'Prévoyez 15 semaines, environ 6 à 9 heures par semaine',
    'es': 'Calcula 15 semanas, unas 6 a 9 horas por semana',
    'ar': 'خطّط لخمسة عشر أسبوعًا، نحو 6 إلى 9 ساعات في الأسبوع',
    'it': 'Prevedi 15 settimane, circa 6–9 ore a settimana',
    'he': 'תכננו 15 שבועות, בערך 6 עד 9 שעות בשבוע',
}
WHAT = {
    'en': ['What'], 'fr': ['Quoi'], 'es': ['Qué'], 'ar': ['ماذا'], 'it': ['Cosa'], 'he': ['מה'],
}
UI = {
 'en': dict(
    pick='Pick a path', pick_lead='Choose how much time you have. Each door opens a real page.',
    quick='Quick class segment', quick_d='Start from a grade band: a few sheets, one hands-on, and every sheet for that grade.',
    lesson='Full lesson', lesson_d='Build a printable plan from the pages you pick.',
    course='A course', course_d='Teach a free course. Each one has a For instructors section.',
    also='Also on this page', more='More doors',
    try_h='Try these first', try_lead='A short row of standout pages. Open any of them, or browse every teacher sheet below.',
    kits='Grade-band starter kits', kits_lead='Four bands. Each kit uses pages already on this site.',
    sheets='Sheets in this kit', hands='Hands-on', see='See all {n} sheets for this grade',
    opens='Opens Lesson Builder on {band}.',
    nopreset='Lesson Builder has no 3–5 setting, so this opens it for you to choose the grade.',
    topics='Topics', topics_lead='{n} hubs. Open one to see its sheets, or browse them all.',
    all_btn='Browse all {n} teacher sheets',
    live='{n} sheets', partial='Showing {shown} of {n}', more_n='Show {n} more',
    one='1 sheet', many='{n} sheets',
    sheet='Sheet', lesson_b='Lesson', course_b='Course', lab='Lab', activity='Activity', map='Map',
    standard='Standard', all_std='All standards'),
 'fr': dict(
    pick='Choisissez un parcours', pick_lead='Choisissez le temps dont vous disposez. Chaque porte ouvre une vraie page.',
    quick='Un court moment de cours', quick_d='Partez d’un niveau : quelques fiches, une activité pratique, et toutes les fiches de ce niveau.',
    lesson='Une leçon complète', lesson_d='Construisez un plan imprimable à partir des pages que vous choisissez.',
    course='Un cours', course_d='Enseignez un cours gratuit. Chacun a une section Pour les enseignants.',
    also='Aussi sur cette page', more='Autres portes',
    try_h='À essayer d’abord', try_lead='Une courte rangée de pages phares. Ouvrez-en une, ou parcourez toutes les fiches plus bas.',
    kits='Kits de départ par niveau', kits_lead='Quatre niveaux. Chaque kit n’utilise que des pages déjà sur ce site.',
    sheets='Fiches de ce kit', hands='Activité pratique', see='Voir les {n} fiches de ce niveau',
    opens='Le générateur de leçons s’ouvre sur {band}.',
    nopreset='Le générateur n’a pas de réglage 3–5 : ce lien l’ouvre pour que vous choisissiez le niveau.',
    topics='Sujets', topics_lead='{n} pôles. Ouvrez-en un pour voir ses fiches, ou parcourez-les toutes.',
    all_btn='Parcourir les {n} fiches enseignants',
    live='{n} fiches', partial='{shown} sur {n}', more_n='Afficher {n} de plus',
    one='1 fiche', many='{n} fiches',
    sheet='Fiche', lesson_b='Leçon', course_b='Cours', lab='Laboratoire', activity='Activité', map='Carte',
    standard='Norme', all_std='Toutes les normes'),
 'es': dict(
    pick='Elige un camino', pick_lead='Elige cuánto tiempo tienes. Cada puerta abre una página real.',
    quick='Un tramo corto de clase', quick_d='Empieza por un grado: unas fichas, una actividad práctica y todas las fichas de ese grado.',
    lesson='Una lección completa', lesson_d='Arma un plan imprimible con las páginas que elijas.',
    course='Un curso', course_d='Enseña un curso gratuito. Cada uno tiene una sección Para docentes.',
    also='También en esta página', more='Otras puertas',
    try_h='Prueba estas primero', try_lead='Una fila corta de páginas destacadas. Abre una, o recorre todas las fichas más abajo.',
    kits='Kits de inicio por grado', kits_lead='Cuatro grados. Cada kit usa solo páginas que ya están en este sitio.',
    sheets='Fichas de este kit', hands='Actividad práctica', see='Ver las {n} fichas de este grado',
    opens='El creador de lecciones se abre en {band}.',
    nopreset='El creador no tiene un ajuste 3–5: este enlace lo abre para que elijas el grado.',
    topics='Temas', topics_lead='{n} centros. Abre uno para ver sus fichas, o recórrelas todas.',
    all_btn='Ver las {n} fichas docentes',
    live='{n} fichas', partial='{shown} de {n}', more_n='Mostrar {n} más',
    one='1 ficha', many='{n} fichas',
    sheet='Ficha', lesson_b='Lección', course_b='Curso', lab='Laboratorio', activity='Actividad', map='Mapa',
    standard='Estándar', all_std='Todos los estándares'),
 'ar': dict(
    pick='اختر مسارًا', pick_lead='اختر الوقت المتاح لك. كل باب يفتح صفحة حقيقية.',
    quick='جزء قصير من الحصة', quick_d='ابدأ من فئة صفية: بضع أوراق، ونشاط عملي واحد، وكل أوراق هذا الصف.',
    lesson='درس كامل', lesson_d='ابنِ خطة قابلة للطباعة من الصفحات التي تختارها.',
    course='مقرر', course_d='درّس مقررًا مجانيًا. لكل مقرر قسم للمعلمين.',
    also='أيضًا في هذه الصفحة', more='أبواب أخرى',
    try_h='جرّب هذه أولًا', try_lead='صف قصير من الصفحات البارزة. افتح أي صفحة، أو تصفح كل أوراق المعلمين في الأسفل.',
    kits='حزم البداية حسب الصف', kits_lead='أربع فئات. كل حزمة تستخدم صفحات موجودة فعلًا في هذا الموقع.',
    sheets='أوراق هذه الحزمة', hands='نشاط عملي', see='عرض كل أوراق هذا الصف ({n})',
    opens='يفتح منشئ الدروس على {band}.',
    nopreset='منشئ الدروس ليس فيه إعداد 3–5، لذا يفتح هذا الرابط المنشئ لتختار الصف.',
    topics='الموضوعات', topics_lead='{n} مراكز. افتح واحدًا لترى أوراقه، أو تصفحها كلها.',
    all_btn='تصفح كل أوراق المعلمين ({n})',
    live='{n} ورقة', partial='{shown} من {n}', more_n='أظهر {n} إضافية',
    one='ورقة واحدة', many='{n} ورقة',
    sheet='ورقة', lesson_b='درس', course_b='مقرر', lab='مختبر', activity='نشاط', map='خريطة',
    standard='المعيار', all_std='كل المعايير'),
 'it': dict(
    pick='Scegli un percorso', pick_lead='Scegli quanto tempo hai. Ogni porta apre una pagina vera.',
    quick='Un breve tratto di lezione', quick_d='Parti da una fascia: alcune schede, un’attività pratica e tutte le schede di quella fascia.',
    lesson='Una lezione intera', lesson_d='Costruisci un piano stampabile dalle pagine che scegli.',
    course='Un corso', course_d='Insegna un corso gratuito. Ognuno ha una sezione Per gli insegnanti.',
    also='Anche in questa pagina', more='Altre porte',
    try_h='Prova queste per prime', try_lead='Una breve fila di pagine di punta. Aprine una, oppure sfoglia tutte le schede più sotto.',
    kits='Kit di partenza per fascia', kits_lead='Quattro fasce. Ogni kit usa solo pagine già presenti su questo sito.',
    sheets='Schede di questo kit', hands='Attività pratica', see='Vedi tutte le {n} schede per questa fascia',
    opens='Il generatore di lezioni si apre su {band}.',
    nopreset='Il generatore non ha un’impostazione 3–5: questo link lo apre perché tu scelga la fascia.',
    topics='Argomenti', topics_lead='{n} hub. Aprine uno per vedere le sue schede, oppure sfogliale tutte.',
    all_btn='Sfoglia tutte le {n} schede per insegnanti',
    live='{n} schede', partial='{shown} di {n}', more_n='Mostra altre {n}',
    one='1 scheda', many='{n} schede',
    sheet='Scheda', lesson_b='Lezione', course_b='Corso', lab='Laboratorio', activity='Attività', map='Mappa',
    standard='Standard', all_std='Tutti gli standard'),
 'he': dict(
    pick='בחרו מסלול', pick_lead='בחרו כמה זמן יש לכם. כל דלת פותחת עמוד אמיתי.',
    quick='קטע קצר בשיעור', quick_d='התחילו מרצועת כיתה: כמה דפים, פעילות מעשית אחת, וכל הדפים לכיתה הזו.',
    lesson='שיעור מלא', lesson_d='בנו תוכנית להדפסה מהעמודים שתבחרו.',
    course='קורס', course_d='לַמדו קורס חינם. לכל קורס יש חלק למורים.',
    also='גם בעמוד הזה', more='דלתות נוספות',
    try_h='נסו את אלה קודם', try_lead='שורה קצרה של עמודים בולטים. פתחו אחד, או עיינו בכל דפי המורים למטה.',
    kits='ערכות פתיחה לפי כיתה', kits_lead='ארבע רצועות. כל ערכה משתמשת רק בעמודים שכבר קיימים באתר.',
    sheets='דפים בערכה הזו', hands='פעילות מעשית', see='כל {n} הדפים לכיתה הזו',
    opens='בונה השיעורים נפתח על {band}.',
    nopreset='לבונה השיעורים אין הגדרה של 3–5, אז הקישור הזה פותח אותו כדי שתבחרו.',
    topics='נושאים', topics_lead='{n} מרכזים. פתחו אחד כדי לראות את הדפים שלו, או עיינו בכולם.',
    all_btn='עיון בכל {n} דפי המורים',
    live='{n} דפים', partial='{shown} מתוך {n}', more_n='הצג עוד {n}',
    one='דף אחד', many='{n} דפים',
    sheet='דף', lesson_b='שיעור', course_b='קורס', lab='מעבדה', activity='פעילות', map='מפה',
    standard='תקן', all_std='כל התקנים'),
}
# Arabic and Hebrew counts: a simple plural that matches how this site writes numbers.
def n_sheets(lang, n):
    u = UI[lang]
    if lang == 'ar':
        if n == 1: return u['one']
        if n == 2: return 'ورقتان'
        if 3 <= n <= 10: return f'{n} أوراق'
        return u['many'].format(n=n)
    if lang == 'he':
        return u['one'] if n == 1 else u['many'].format(n=n)
    return (u['one'] if n == 1 else u['many']).format(n=n) if '{n}' in (u['one'] if n == 1 else u['many']) else (u['one'] if n == 1 else u['many'].format(n=n))

KITS = [
    ('K-2', 'k3', 'Kids_Map.html', 'map', ['Life_Terra.html', 'Ocean_Cleanup.html', 'One_Tree_Planted.html', 'Mangroves.html', 'Plant-for-the-Planet.html']),
    ('3-5', None, 'Satellite_Explorer.html', 'activity', ['GLOBE_Program.html', 'Mangroves.html', 'Life_Terra.html', 'Global_Forest_Watch.html', 'Ocean_Cleanup.html']),
    ('6-8', 'g68', 'Spot_the_Fire.html', 'lesson', ['GLOBE_Program.html', 'ICESat-2.html', 'FIRMS.html', 'Tsunami_Early_Warning.html', 'SmartICE.html']),
    ('9-12', 'g912', 'Orbit_Lab.html', 'lab', ['Carbfix.html', 'ClearSpace.html', 'Astroscale.html', 'Ocean_Cleanup.html']),
]
# Planet science first (ocean, earth, climate, biology), then chemistry, physics, and a map.
FEATURED = [
    ('Ocean_Cleanup.html', 'sheet', '#teachers'),
    ('GLOBE_Program.html', 'sheet', '#teachers'),
    ('Spot_the_Fire.html', 'lesson', ''),
    ('Mangroves.html', 'sheet', '#teachers'),
    ('General_Chemistry_I.html', 'course', '#instructors'),
    ('Physics_I.html', 'course', '#instructors'),
    ('Kids_Map.html', 'map', ''),
]
SURFACE = ['GLOBE_Program.html', 'Myth_vs_Fact.html', 'Spot_the_Fire.html', 'Search.html']
# Nov 11, Bryan: JROTC (Cadets.html) and Careers are out of scope on Teachers.
# AP & IB Physics stays: it is a physics door, not a careers or cadet path.
SECONDARY_LABELS = {
 'en': [('AP_IB_Physics.html', '📘 AP & IB Physics')],
 'fr': [('AP_IB_Physics.html', '📘 Physique AP et IB')],
 'es': [('AP_IB_Physics.html', '📘 Física AP e IB')],
 'ar': [('AP_IB_Physics.html', '📘 فيزياء AP وIB')],
 'it': [('AP_IB_Physics.html', '📘 Fisica AP e IB')],
 'he': [('AP_IB_Physics.html', '📘 פיזיקה AP ו-IB')],
}
# Planet science first, then physics-adjacent space hubs. Counts are still taken from the lists.
HUB_LEAD = ['Oceans.html', 'Rivers.html', 'Lakes.html', 'Deforestation.html', 'Polar.html', 'Earth_Observation.html',
            'Planetary_Defense.html', 'Space_Weather.html', 'Space.html', 'Space_Disposal.html', 'Project-Rawane.html']
PRINT_LABEL = {'en': 'Print', 'fr': 'Imprimer', 'es': 'Imprimir', 'ar': 'اطبع', 'it': 'Stampa', 'he': 'הדפסה'}
# Homepage Earth / beach / forest loop. Same file the live homepage and Match page already play.
HERO_VIDEO = 'https://media.savingplanets.com/videos/hero-loop.97191e628115.mp4'
HERO_CREDIT = {
 'en': 'Created by the Founder and SI',
 'fr': 'Créé par le fondateur et SI',
 'es': 'Creado por el fundador y SI',
 'ar': 'من إعداد المؤسس وSI',
 'it': 'Creato dal fondatore e da SI',
 'he': 'נוצר על ידי המייסד ו-SI',
}
def dress_hero(s, lang):
    poster = ('../' if lang != 'en' else '') + 'assets/videos/hero-loop.jpg'
    media = (
        f'<div class="t-hero-media" aria-hidden="true"><img class="t-hero-still" src="{poster}" alt="" width="1280" height="546">'
        f'<video class="t-hero-video" muted loop playsinline autoplay preload="none" poster="{poster}" width="1280" height="546">'
        f'<source data-src="{HERO_VIDEO}" type="video/mp4"></video><div class="t-hero-shade"></div></div>'
    )
    script = (
        '<script>(function(){var v=document.querySelector(".t-hero-video");if(!v)return;'
        'var mq=window.matchMedia("(prefers-reduced-motion: reduce)");'
        'function arm(){if(mq.matches){v.pause();v.removeAttribute("autoplay");v.preload="none";return;}'
        'var s=v.querySelector("source");if(s&&!s.getAttribute("src")){s.src=s.getAttribute("data-src");v.load();}'
        'var p=v.play&&v.play();if(p&&p.catch)p.catch(function(){});}'
        'arm();if(mq.addEventListener)mq.addEventListener("change",arm);})();</script>'
    )
    def repl(m):
        content = re.search(r'<div class="page-hero-content">.*?</div>', m.group(0), re.S)
        if not content:
            return m.group(0)
        return (f'<section class="page-hero hero-teach has-video">{media}{content.group(0)}'
                f'<span class="hero-credit">{E(HERO_CREDIT[lang])}</span></section>{script}')
    s2, n = re.subn(
        r'<section class="page-hero hero-teach[^"]*">.*?</section>(?:<script>\(function\(\)\{var v=document\.querySelector\("\.t-hero-video"\).*?</script>)?',
        repl, s, count=1, flags=re.S)
    if n != 1 or 't-hero-video' not in s2:
        raise SystemExit(f'{lang}: could not place the title video')
    s2 = s2.replace('data-glass-tint="site"', 'data-glass-tint="water"', 1)
    return s2
TYPE_KEY = {'sheet': 'sheet', 'lesson': 'lesson_b', 'course': 'course_b', 'lab': 'lab', 'activity': 'activity', 'map': 'map'}
# The course block was left in English on every translated Teachers page. These strings
# are the ones build-teacher-guide.py already uses for each language.
COURSE_COPY = {
 'en': ('Courses', 'Free courses you can teach. Each one has a For instructors section. Copy the teacher guide template for your class.', 'Teacher guide template'),
 'fr': ('Cours', 'Cours gratuits à enseigner. Chacun a une section Pour les enseignants. Copiez le modèle de guide pour votre classe.', 'Modèle de guide enseignant'),
 'es': ('Cursos', 'Cursos gratuitos para enseñar. Cada uno tiene una sección Para docentes. Copia la plantilla de guía para tu clase.', 'Plantilla de guía docente'),
 'ar': ('المقررات', 'مقررات مجانية يمكن تدريسها. لكل مقرر قسم للمعلمين. انسخ نموذج الدليل لصفك.', 'نموذج دليل المعلم'),
 'it': ('Corsi', 'Corsi gratuiti da insegnare. Ognuno ha una sezione Per gli insegnanti. Copia il modello di guida per la tua classe.', 'Modello di guida per insegnanti'),
 'he': ('קורסים', 'קורסים חינמיים שאפשר ללמד. לכל קורס יש מקטע למורים. העתיקו את תבנית המדריך לכיתה שלכם.', 'תבנית מדריך למורה'),
}
def localize_courses(lang, data):
    c = data['course']
    title, lead, guide = COURSE_COPY[lang]
    c['title'], c['lead'], c['guide'] = title, lead, guide
    c['guide_href'] = 'Teacher_Guide.html'
    heads = re.findall(r'<section id="y\d"[^>]*>\s*<h2>(.*?)</h2>', read(folder(lang) + 'Courses.html'), re.S)
    years = []
    for i, (head, rows) in enumerate(c['years']):
        use = plain(heads[i]) if i < len(heads) else head
        fixed = []
        for href, _title, code in rows:
            href = href.replace('../', '')
            page = href.split('#')[0]
            href = page + '#instructors'
            name = h1_of(lang, page) if os.path.exists(folder(lang) + page) else _title
            fixed.append((href, name, code))
        years.append((use, fixed))
    c['years'] = years

def folder(lang):
    return '' if lang == 'en' else lang + '/'
def asset(lang, name):
    return ('../' if lang != 'en' else '') + name
def read(path):
    return open(path, encoding='utf-8').read()
def plain(fragment):
    t = re.sub(r'<span class="gl-pop".*?</span></span>', ' ', fragment or '', flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()
def clip(text, n=150):
    text = re.sub(r'\s+', ' ', text or '').strip()
    if len(text) <= n: return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip('.,;:،')
    return (cut or text[:n].rstrip()) + '…'
def short(code):
    return code.replace('CCSS.ELA-LITERACY.', 'CCSS ')

def update_standards():
    path = 'assets/data/standards.json'
    raw = read(path)
    D = json.loads(raw)
    missing = [c for cs in PAGE_TAGS.values() for c in cs if c not in D['codes']]
    if missing: raise SystemExit('unknown standards: ' + ', '.join(sorted(set(missing))))
    if set(PAGE_TAGS) - set(PARTIAL) != set(PAGE_TAGS) - set(PARTIAL):
        pass
    changed = False
    for page, codes in PAGE_TAGS.items():
        if D['pages'].get(page) != codes:
            D['pages'][page] = codes
            changed = True
    if changed:
        # Keep the file's existing layout if a full dump would rewrite every line.
        blob = json.dumps(D, ensure_ascii=False, indent=2) + '\n'
        if blob != raw:
            open(path, 'w', encoding='utf-8').write(blob)
    return D

def primary_hubs():
    s = read('Solutions.html'); out = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        h = re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)
        for u in re.findall(r'data-url="([^"#]+)"', m.group(2)):
            out.setdefault(u, h)
    return out

def meta_for(D, PH, page):
    cs = D['pages'].get(page) or D['hubs'].get(PH.get(page, ''), [])
    grades = [b for b in BANDS if any(D['codes'][c]['band'] == b for c in cs)]
    subjects = [s for s in SUBJ_ORDER if any(D['codes'][c]['subject'] == s for c in cs)]
    return cs, grades, subjects

def h1_of(lang, page):
    s = read(folder(lang) + page)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return plain(m.group(1)) if m else page
def hero_p(lang, page):
    s = read(folder(lang) + page)
    m = re.search(r'<div class="page-hero-content">.*?<p>(.*?)</p>', s, re.S)
    if m: return clip(plain(m.group(1)))
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    return clip(html.unescape(m.group(1))) if m else ''
def what_hook(lang, page, cache):
    key = (lang, page)
    if key in cache: return cache[key]
    path = folder(lang) + page
    text = ''
    if os.path.exists(path):
        s = read(path)
        for h in WHAT[lang]:
            m = re.search(r'<h3>' + re.escape(h) + r'</h3>\s*<p>(.*?)</p>', s, re.S)
            if m:
                text = plain(m.group(1)); break
        if not text:
            m = re.search(r'<meta name="description" content="([^"]*)"', s)
            if m: text = html.unescape(m.group(1)).strip()
    cache[key] = clip(text)
    return cache[key]
def band_label(lang, value):
    if not value: return None
    s = read(folder(lang) + 'Lesson_Builder.html')
    m = re.search(r'<option value="' + re.escape(value) + r'"[^>]*>([^<]+)', s)
    return html.unescape(m.group(1)).strip() if m else None
def course_time(lang, href):
    page = href.split('#')[0]
    path = folder(lang) + page
    if not os.path.exists(path): return ''
    phrase = TIME_PHRASE[lang]
    return phrase if phrase in read(path) else ''

def parse(s):
    hubs = []
    for m in re.finditer(r'<section class="five-ws t-hub"><h2><a href="([^"]+)">([^<]*)</a></h2><ul class="t-list">(.*?)</ul></section>', s, re.S):
        items = [(a, html.unescape(t)) for a, t in re.findall(r'<a href="([^"#]+)#teachers">([^<]*)</a>', m.group(3))]
        hubs.append({'href': m.group(1), 'name': html.unescape(m.group(2)), 'items': items})
    if not hubs and 'class="t-topic"' in s:
        for m in re.finditer(r'<details class="t-topic"[^>]*data-hub="([^"]+)"[^>]*>(.*?)</details>', s, re.S):
            name = re.search(r'class="t-topic-name">([^<]*)', m.group(2))
            items = [(html.unescape(a), html.unescape(t)) for a, t in re.findall(r'class="t-card-main" href="([^"#]+)#teachers">(?:(?!</a>).)*?<span class="t-card-title">([^<]*)</span>', m.group(2), re.S)]
            hubs.append({'href': html.unescape(m.group(1)), 'name': html.unescape(name.group(1)) if name else m.group(1), 'items': items})
    crs = re.search(r'<!-- TEACHCRS:START -->(.*?)<!-- TEACHCRS:END -->', s, re.S)
    course = {'title': 'Courses', 'lead': '', 'guide_href': 'Teacher_Guide.html', 'guide': '', 'years': []}
    if crs:
        body = crs.group(1)
        hm = re.search(r'<h2[^>]*>([^<]*)</h2>', body)
        if hm: course['title'] = html.unescape(hm.group(1))
        pm = re.search(r'</h2>\s*<p>(.*?)</p>', body, re.S)
        if not pm: pm = re.search(r'class="t-courses-body">\s*<p>(.*?)</p>', body, re.S)
        if pm: course['lead'] = plain(pm.group(1))
        gm = re.search(r'<a href="([^"]*Teacher_Guide\.html)">([^<]*)</a>', body)
        if gm:
            course['guide_href'], course['guide'] = gm.group(1), html.unescape(gm.group(2))
        years = re.findall(r'<h3>(.*?)</h3>\s*<ul class="t-list">(.*?)</ul>', body, re.S)
        if years:
            for head, ul in years:
                rows = [(html.unescape(h), html.unescape(t), html.unescape(c)) for h, t, c in re.findall(r'<a href="([^"]+)">([^<]*)</a>\s*<span class="t-codes">([^<]*)</span>', ul)]
                course['years'].append((html.unescape(head), rows))
        else:
            for ym in re.finditer(r'<details class="t-year">(.*?)</details>', body, re.S):
                head = plain(re.search(r'<summary[^>]*>(.*?)</summary>', ym.group(1), re.S).group(1))
                head = re.sub(r'\s+\d+\s+\S+$', '', head).strip()
                rows = []
                for cm in re.finditer(r'<a class="t-card-main" href="([^"]+)">(.*?)</a>', ym.group(1), re.S):
                    title = re.search(r'class="t-card-title">([^<]*)', cm.group(2))
                    code = re.search(r'class="t-code"[^>]*>([^<]*)', cm.group(2))
                    rows.append((html.unescape(cm.group(1)), html.unescape(title.group(1)) if title else '', html.unescape(code.group(1)) if code else ''))
                course['years'].append((head, rows))
    browse = re.search(r'<!-- T-BROWSE:START -->(.*?)<!-- T-BROWSE:END -->', s, re.S)
    bsrc = browse.group(1) if browse else s
    grades = re.findall(r'data-k="g" data-v="([^"]*)"[^>]*>([^<]*)<', bsrc)
    subjects = re.findall(r'data-k="s" data-v="([^"]*)"[^>]*>([^<]*)<', bsrc)
    note = re.search(r'class="std-note">([^<]*)', bsrc)
    none = re.search(r'class="t-none"[^>]*>([^<]*)', bsrc)
    bh = re.search(r'id="tb-h">([^<]*)', bsrc)
    legend_g = re.search(r'data-k="g"[^>]*>[\s\S]*?<legend>([^<]*)</legend>', bsrc) or re.search(r'<legend>([^<]*)</legend>\s*<button[^>]*data-k="g"', bsrc)
    # legends are before the buttons
    legends = re.findall(r'<legend>([^<]*)</legend>', bsrc)
    print_label = 'Print'
    pm = re.search(r'class="t-print"[^>]*>([^<]+)', s)
    if pm: print_label = html.unescape(pm.group(1)).strip()
    secondary = []
    search = 'Search'
    nav = re.search(r'<nav id="topnav">.*?</nav>', s, re.S)
    if nav:
        sm = re.search(r'<a[^>]*href="(?:\.\./)?Search\.html"[^>]*>(.*?)</a>', nav.group(0), re.S)
        if sm and plain(sm.group(1)): search = plain(sm.group(1))
    return dict(hubs=hubs, course=course, grades=grades, subjects=subjects, legends=legends,
                note=html.unescape(note.group(1)) if note else '', none=html.unescape(none.group(1)) if none else '',
                browse_h=html.unescape(bh.group(1)) if bh else '', print_label=print_label,
                secondary=secondary, search=search)

def card(lang, u, href, title, kind, grades, codes, hook, time, print_label, extra=''):
    pills = ''.join(f'<span class="t-pill" dir="ltr">{E(g)}</span>' for g in grades)
    code = f'<span class="t-code" dir="ltr" lang="en">{E(codes)}</span>' if isinstance(codes, str) and codes else ''
    codes = codes if isinstance(codes, list) else []
    hook_h = f'<span class="t-hook">{E(hook)}</span>' if hook else ''
    time_h = f'<span class="t-time">{E(time)}</span>' if time else ''
    badge = UI[lang][TYPE_KEY[kind]]
    data = ''
    if kind == 'sheet':
        data = f' data-grades="{" ".join(grades)}" data-subjects="{extra}" data-codes="{"|".join(short(c) for c in codes)}"'
    print_a = ''
    if kind == 'sheet' and print_label:
        print_a = f'<a class="t-print t-chip" href="{E(href.split("#")[0])}?print=1" rel="nofollow">{E(print_label)}</a>'
    return (f'<li class="t-card" data-type="{kind}"{data}><a class="t-card-main" href="{E(href)}">'
            f'<span class="t-type">{E(badge)}</span><span class="t-card-title">{E(title)}</span>{hook_h}{code}{time_h}'
            f'<span class="t-pills">{pills}</span></a>{print_a}</li>')

def render(lang, data, D, PH, hooks):
    u = UI[lang]
    rows = [(hub, page, title) for hub in data['hubs'] for page, title in hub['items']]
    total = len(rows)
    def info(page):
        cs, grades, subjects = meta_for(D, PH, page)
        return cs, grades, subjects
    # path
    lb = 'Lesson_Builder.html'
    paths = f'''<section class="t-home" id="pick-a-path" aria-labelledby="start-here"><span id="ask-si"></span>
<h2 id="start-here">{E(u["pick"])}</h2><p class="t-lead">{E(u["pick_lead"])}</p>
<div class="t-paths">
<a class="t-path" href="#grade-kits"><span class="t-kicker">1</span><strong>{E(u["quick"])}</strong><span>{E(u["quick_d"])}</span></a>
<a class="t-path" href="{lb}"><span class="t-kicker">2</span><strong>{E(u["lesson"])}</strong><span>{E(u["lesson_d"])}</span></a>
<a class="t-path" href="Courses.html"><span class="t-kicker">3</span><strong>{E(u["course"])}</strong><span>{E(u["course_d"])}</span></a>
</div>
<h3 class="t-subh">{E(u["also"])}</h3><ul class="t-row">'''
    for page in SURFACE:
        label = data['search'] if page == 'Search.html' else h1_of(lang, page)
        paths += f'<li><a class="t-chip" href="{E(page)}">{E(label)}</a></li>'
    paths += f'</ul><h3 class="t-subh">{E(u["more"])}</h3><ul class="t-row t-secondary">'
    for href, label in data['secondary']:
        paths += f'<li><a class="t-chip" href="{E(href)}">{E(label)}</a></li>'
    paths += '</ul></section>'
    # featured
    feat = [f'<section class="t-home" aria-labelledby="try-h"><h2 id="try-h">{E(u["try_h"])}</h2><p class="t-lead">{E(u["try_lead"])}</p><ul class="t-feature">']
    for page, kind, frag in FEATURED:
        cs, grades, subjects = info(page) if kind == 'sheet' else ([], [], [])
        href = page + frag
        hook = what_hook(lang, page, hooks) if kind == 'sheet' else hero_p(lang, page)
        title = h1_of(lang, page)
        time = course_time(lang, page) if kind == 'course' else ''
        feat.append(card(lang, u, href, title, kind, grades, cs if kind == 'sheet' else [], hook, time, data['print_label'] if kind == 'sheet' else '', ' '.join(subjects)))
    feat.append(f'</ul><p class="t-all"><a class="t-chip" href="#t-topics">{E(u["all_btn"].format(n=total))}</a></p></section>')
    # kits
    by_page = {page: title for _h, page, title in rows}
    kits = [f'<section class="t-home" id="grade-kits" aria-labelledby="kits-h"><h2 id="kits-h">{E(u["kits"])}</h2><p class="t-lead">{E(u["kits_lead"])}</p><div class="t-kits">']
    for band, preset, hands, hands_kind, prefs in KITS:
        chosen = []
        for page in prefs:
            if page in by_page and band in info(page)[1] and page not in chosen:
                chosen.append(page)
            if len(chosen) == 3: break
        if len(chosen) < 3:
            for _hub, page, _title in rows:
                if page not in chosen and band in info(page)[1]:
                    chosen.append(page)
                if len(chosen) == 3: break
        if len(chosen) < 3: raise SystemExit(f'{lang} kit {band} only found {chosen}')
        n = sum(1 for _h, page, _t in rows if band in info(page)[1])
        label = band_label(lang, preset)
        if preset and not label:
            href, note = lb, ''
        elif preset and label:
            href, note = f'{lb}?band={preset}', u['opens'].format(band=label)
        else:
            href, note = lb, u['nopreset']
        bits = [f'<article class="t-kit"><h3 dir="ltr">{E(band)}</h3><h4>{E(u["sheets"])}</h4><ul class="t-kit-list">']
        for page in chosen:
            cs, grades, _sj = info(page)
            bits.append(card(lang, u, page + '#teachers', by_page[page], 'sheet', grades, cs, what_hook(lang, page, hooks), '', data['print_label']))
        hand_title = h1_of(lang, hands)
        bits.append('</ul>')
        bits.append(f'<h4>{E(u["hands"])}</h4><ul class="t-kit-list">' + card(lang, u, hands, hand_title, hands_kind, [], [], hero_p(lang, hands), '', '') + '</ul>')
        bits.append(f'<p><a class="t-chip" href="{E(href)}">{E(h1_of(lang, "Lesson_Builder.html"))}</a></p>')
        if note: bits.append(f'<p class="t-kit-note">{E(note)}</p>')
        bits.append(f'<p><a class="t-chip" href="Teachers.html?grade={E(band)}#t-topics">{E(u["see"].format(n=n))}</a></p></article>')
        kits.append(''.join(bits))
    kits.append('</div></section>')
    # topics + catalog
    g_leg = data['legends'][0] if data['legends'] else 'Grade'
    s_leg = data['legends'][1] if len(data['legends']) > 1 else 'Subject'
    chips_g = ''.join(f'<button type="button" class="t-chip" data-k="g" data-v="{E(v)}" aria-pressed="{"true" if v=="all" else "false"}">{E(lab)}</button>' for v, lab in data['grades'])
    chips_s = ''.join(f'<button type="button" class="t-chip" data-k="s" data-v="{E(v)}" aria-pressed="{"true" if v=="all" else "false"}">{E(lab)}</button>' for v, lab in data['subjects'])
    used = []
    seen = set()
    for _h, page, _t in rows:
        for c in info(page)[0]:
            if c not in seen:
                seen.add(c); used.append(c)
    # Keep the standards.json order.
    used = [c for c in D['codes'] if c in seen]
    opts = f'<option value="all">{E(u["all_std"])}</option>' + ''.join(
        f'<option value="{E(short(c))}" dir="ltr" lang="en" title="{E(D["codes"][c]["text"])}">{E(short(c))}</option>' for c in used)
    nhubs = len(data['hubs'])
    topics = [f'<section class="t-home" id="t-topics" aria-labelledby="topics-h"><h2 id="topics-h">{E(u["topics"])}</h2>'
              f'<p class="t-lead">{E(u["topics_lead"].format(n=nhubs))}</p>'
              f'<div class="t-browse t-browse-in" id="t-browse"><h3 id="tb-h">{E(data["browse_h"])}</h3>'
              f'<fieldset><legend>{E(g_leg)}</legend>{chips_g}</fieldset>'
              f'<fieldset><legend>{E(s_leg)}</legend>{chips_s}</fieldset>'
              f'<label class="t-std-label" for="t-std">{E(u["standard"])} <select id="t-std" class="t-std">{opts}</select></label>'
              f'<p class="std-note">{E(data["note"])}</p>'
              f'<p id="t-live" class="t-live" aria-live="polite" data-tpl="{E(u["live"])}" data-partial="{E(u["partial"])}"></p>'
              f'<p class="t-none" hidden>{E(data["none"])}</p></div><div class="t-topic-grid" id="t-topic-grid">']
    for hub in data['hubs']:
        slug = re.sub(r'[^A-Za-z0-9_-]', '-', hub['href'])
        n = len(hub['items'])
        topics.append(f'<details class="t-topic" id="hub-{E(slug)}" data-hub="{E(hub["href"])}"><summary aria-expanded="false">'
                      f'<span class="t-topic-name">{E(hub["name"])}</span><span class="t-topic-meta">{E(n_sheets(lang, n))}</span></summary><ul class="t-cat">')
        for page, title in hub['items']:
            cs, grades, subjects = info(page)
            topics.append(card(lang, u, page + '#teachers', title, 'sheet', grades, cs, what_hook(lang, page, hooks), '', data['print_label'], ' '.join(subjects)))
        topics.append('</ul></details>')
    topics.append('</div>')
    topics.append(f'<p class="t-all"><a class="t-chip t-browse-all" id="t-browse-all" href="#t-topic-grid" aria-expanded="false" aria-controls="t-topic-grid">{E(u["all_btn"].format(n=total))}</a> '
                  f'<button type="button" class="t-chip t-more-all" id="t-more-all" hidden data-more="{E(u["more_n"])}">{E(u["more_n"].format(n=24))}</button></p></section>')
    # courses
    c = data['course']
    ncourse = sum(len(rows_) for _h, rows_ in c['years'])
    years = ['<div class="t-years">']
    for head, items in c['years']:
        years.append(f'<details class="t-year"><summary aria-expanded="false"><span>{E(head)}</span><span class="t-topic-meta">{E(n_sheets(lang, len(items)).replace(UI[lang]["many"].split("{n}")[-1] if False else "", ""))}</span></summary><ul class="t-cat">')
        # The replace above is a mistake if it strips the noun. Build the year count with n_sheets directly.
        years[-1] = f'<details class="t-year"><summary aria-expanded="false"><span>{E(head)}</span><span class="t-topic-meta">{E(n_sheets(lang, len(items)))}</span></summary><ul class="t-cat">'
        for href, title, code in items:
            time = course_time(lang, href)
            years.append(card(lang, u, href, title, 'course', [], [], '', time, ''))
            # course code is the third field; card() puts codes only for sheets. Add code inside by a dedicated snippet.
            if code:
                years[-1] = years[-1].replace('</span></a>', f'</span><span class="t-code" dir="ltr" lang="en">{E(code)}</span></a>', 1)
        years.append('</ul></details>')
    years.append('</div>')
    courses = (f'<!-- TEACHCRS:START --><details class="t-courses" id="courses"><summary aria-expanded="false">'
               f'<span>{E(c["title"])}</span><span class="t-topic-meta">{E(n_sheets(lang, ncourse))}</span></summary>'
               f'<div class="t-courses-body"><p>{E(c["lead"])}</p><p><a href="{E(c["guide_href"])}">{E(c["guide"])}</a></p>'
               + ''.join(years) + '</div></details><!-- TEACHCRS:END -->')
    # n_sheets for courses says "sheets" which is wrong. Use the course title count as a number plus the existing course word.
    # Fix below in a cleaner courses header.
    return ('<!-- TEACHHOME:START --><div id="t-home">' + paths + ''.join(feat) + ''.join(kits) + ''.join(topics)
            + f'<section class="t-home">{courses}</section>'
            + '<noscript><style>.t-more-all{display:none}</style></noscript></div><!-- TEACHHOME:END -->', total, ncourse)

def course_count_word(lang, n):
    # Courses are not sheets. Use the page's own course heading word with the number.
    word = {'en': 'courses', 'fr': 'cours', 'es': 'cursos', 'ar': 'مقررات', 'it': 'corsi', 'he': 'קורסים'}[lang]
    one = {'en': 'course', 'fr': 'cours', 'es': 'curso', 'ar': 'مقرر', 'it': 'corso', 'he': 'קורס'}[lang]
    if lang == 'ar':
        if n == 1: return 'مقرر واحد'
        if n == 2: return 'مقرران'
        if 3 <= n <= 10: return f'{n} مقررات'
        return f'{n} مقررًا'
    if n == 1: return f'1 {one}'
    return f'{n} {word}'

def fix_course_counts(block, lang, data):
    """Replace the sheet-count phrase on the course accordion with a course count."""
    c = data['course']
    ncourse = sum(len(rows) for _h, rows in c['years'])
    # The summary we emitted used n_sheets. Swap the course-details summary meta only.
    def swap(html_block, count, phrase):
        return html_block
    block = re.sub(
        r'(<details class="t-courses" id="courses"><summary aria-expanded="false"><span>[^<]*</span><span class="t-topic-meta">)[^<]*(</span>)',
        lambda m: m.group(1) + E(course_count_word(lang, ncourse)) + m.group(2),
        block, count=1)
    # Year bands were also given a sheet phrase. Replace each t-year meta by its item count, in order.
    counts = [len(rows) for _h, rows in c['years']]
    idx = {'i': 0}
    def year_sub(m):
        i = idx['i']; idx['i'] += 1
        phrase = course_count_word(lang, counts[i]) if i < len(counts) else m.group(2)
        return m.group(1) + E(phrase) + m.group(3)
    block = re.sub(r'(<details class="t-year"><summary aria-expanded="false"><span>[^<]*</span><span class="t-topic-meta">)([^<]*)(</span>)', year_sub, block)
    return block

def grab(s, name):
    m = re.search(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), s, re.S)
    return m.group(0) if m else ''

def apply_lang(lang, D, PH):
    path = folder(lang) + 'Teachers.html'
    s = read(path)
    def foot(text):
        a = text.find('<footer')
        b = text.find('</footer>', a)
        return text[a:b + len('</footer>')]
    footer = foot(s)
    cf = re.search(r'<!-- CF-WA:START -->.*?<!-- CF-WA:END -->', s, re.S)
    data = parse(s)
    data['secondary'] = list(SECONDARY_LABELS[lang])
    data['print_label'] = PRINT_LABEL[lang]
    order = {h: i for i, h in enumerate(HUB_LEAD)}
    data['hubs'].sort(key=lambda h: order.get(h['href'], 50))
    if len(data['hubs']) != 11:
        raise SystemExit(f'{path}: expected 11 hubs, found {len(data["hubs"])}')
    if not data['grades'] or not data['subjects']:
        raise SystemExit(f'{path}: missing grade/subject chips')
    hooks = {}
    localize_courses(lang, data)
    home, total, ncourse = render(lang, data, D, PH, hooks)
    home = fix_course_counts(home, lang, data)
    edu, sat = grab(s, 'EDU-LINKS'), grab(s, 'SATEXPL')
    s2 = re.sub(r'<!-- SIHELPER:START -->.*?<!-- SIHELPER:END -->', '', s, flags=re.S)
    if '<!-- TEACHHOME:START -->' in s2:
        s2 = re.sub(r'<!-- TEACHHOME:START -->.*?<!-- TEACHHOME:END -->', lambda m: home, s2, count=1, flags=re.S)
    else:
        start = s2.find('<!-- STARTHERE:START -->')
        hubs = list(re.finditer(r'<section class="five-ws t-hub">.*?</ul></section>', s2, re.S))
        if start < 0 or not hubs:
            raise SystemExit(f'{path}: no start-here/hub region to replace')
        s2 = s2[:start] + home + s2[hubs[-1].end():]
    if edu and '<!-- EDU-LINKS:START -->' not in s2:
        s2 = s2.replace('<!-- TEACHHOME:END -->', '<!-- TEACHHOME:END -->' + edu + (sat or ''), 1)
    elif sat and '<!-- SATEXPL:START -->' not in s2:
        s2 = s2.replace('<!-- TEACHHOME:END -->', '<!-- TEACHHOME:END -->' + sat, 1)
    css = f'{asset(lang, "teachers-home.css")}?v={ASSET}'
    js = f'{asset(lang, "teachers-home.js")}?v={ASSET}'
    if 'teachers-home.css' not in s2:
        s2 = s2.replace('</head>', f'<link rel="stylesheet" href="{css}">\n</head>', 1)
    if 'teachers-home.js' not in s2:
        s2 = s2.replace('</body>', f'<script src="{js}" defer></script>\n</body>', 1)
    s2 = re.sub(r'teachers-home\.(css|js)\?v=[0-9a-z]+', lambda m: f'teachers-home.{m.group(1)}?v={ASSET}', s2)
    s2 = dress_hero(s2, lang)
    footer2 = foot(s2)
    if footer2 != footer:
        raise SystemExit(f'{path}: footer changed')
    cf2 = re.search(r'<!-- CF-WA:START -->.*?<!-- CF-WA:END -->', s2, re.S)
    if (cf and cf.group(0)) != (cf2 and cf2.group(0)):
        raise SystemExit(f'{path}: cloudflare beacon changed')
    if 'SIHELPER' in s2 or 'class="t-codes"' in s2.split('<!-- TEACHHOME:START -->', 1)[-1].split('<!-- TEACHHOME:END -->', 1)[0]:
        raise SystemExit(f'{path}: SI Helper or repeated standards codes still in the new home')
    open(path, 'w', encoding='utf-8').write(s2)
    empty_hooks = sum(1 for hub in data['hubs'] for page, _t in hub['items'] if not what_hook(lang, page, hooks))
    return total, ncourse, empty_hooks

def main():
    D = update_standards()
    if '--tags-only' in sys.argv:
        print(f'tags: {len(PAGE_TAGS)} page overrides, {len(PARTIAL)} reading-only')
        for page, why in PARTIAL.items():
            print(f'  partial {page}: {why}')
        return
    PH = primary_hubs()
    for lang in LANGS:
        total, ncourse, empty_hooks = apply_lang(lang, D, PH)
        print(f'{lang}: {total} sheet rows, {ncourse} courses, empty hooks {empty_hooks}')

if __name__ == '__main__':
    main()
