#!/usr/bin/env python3
"""Teacher guide template, a For instructors block on each course, and a Courses section on Teachers.

Nov 2 2026 (Bryan-approved). Writes Teacher_Guide.html in en/fr/es/ar/it/he, splices
<!-- INSTRUCT --> into each live course page, and <!-- TEACHCRS --> onto Teachers.html.
Translations live in this file (first draft; native review still needed). Idempotent.
Does not touch the Saturn hero or add analytics. Wired from build-courses.py so the
weekly sync keeps the blocks after a course rebuild.
"""
import os, re, sys, glob, html, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
PAGE = 'Teacher_Guide.html'
E = lambda s: html.escape(s, quote=True)

# ELI10 copy. Keys are shared. {units} {labs} {code} filled per course.
INS = {
 'en': {
  'h': 'For instructors',
  'lead': 'You can teach this course, or let a student work through it alone. It is free. Saving Planets does not give a grade or school credit.',
  'time': 'Plan on 15 weeks, about 6 to 9 hours a week, including the lab weeks.',
  'counts': 'This page is the whole course: {units} units and {labs} labs ({code}).',
  'how': 'Follow the 15-week schedule. Read the unit, do the practice on paper, then open the answer. In a lab week, do the lab or the home version.',
  'check': 'A check is one number or code result on the page that a script recomputes before we publish. The number you see and the recomputed number have to match.',
  'print': 'Use Print this page, or download the PDF study guide. The formula sheet is near the end.',
  'discuss': 'Ask: how does this unit help people and the planet? Each unit has a green box with a sourced fact.',
  'copy': 'Copy the teacher guide template and write in your class name, the time you have, and the questions you will ask.',
  'link': 'Open the teacher guide template',
  'toc': 'For instructors',
 },
 'fr': {
  'h': 'Pour les enseignants',
  'lead': 'Vous pouvez enseigner ce cours, ou laisser un élève le faire seul. Il est gratuit. Saving Planets ne donne ni note ni crédit scolaire.',
  'time': 'Prévoyez 15 semaines, environ 6 à 9 heures par semaine, y compris les semaines de travaux pratiques.',
  'counts': 'Cette page est le cours entier : {units} unités et {labs} travaux pratiques ({code}).',
  'how': 'Suivez le calendrier de 15 semaines. Lisez l’unité, faites les exercices sur papier, puis ouvrez la réponse. La semaine d’un TP, faites le TP ou la version à la maison.',
  'check': 'Un contrôle est un nombre ou un résultat de code sur la page qu’un script recalcule avant publication. Le nombre affiché et le nombre recalculé doivent correspondre.',
  'print': 'Utilisez Imprimer cette page, ou téléchargez le guide d’étude PDF. La feuille de formules est vers la fin.',
  'discuss': 'Demandez : en quoi cette unité aide-t-elle les gens et la planète ? Chaque unité a un encadré vert avec un fait sourcé.',
  'copy': 'Copiez le modèle de guide enseignant et écrivez le nom de votre classe, le temps dont vous disposez et les questions que vous poserez.',
  'link': 'Ouvrir le modèle de guide enseignant',
  'toc': 'Pour les enseignants',
 },
 'es': {
  'h': 'Para docentes',
  'lead': 'Puedes enseñar este curso o dejar que un estudiante lo haga solo. Es gratis. Saving Planets no pone nota ni da crédito escolar.',
  'time': 'Calcula 15 semanas, unas 6 a 9 horas por semana, incluidas las semanas de laboratorio.',
  'counts': 'Esta página es el curso completo: {units} unidades y {labs} laboratorios ({code}).',
  'how': 'Sigue el calendario de 15 semanas. Lee la unidad, haz la práctica en papel y luego abre la respuesta. En una semana de laboratorio, haz el laboratorio o la versión en casa.',
  'check': 'Una comprobación es un número o un resultado de código en la página que un script vuelve a calcular antes de publicar. El número que ves y el recalculado tienen que coincidir.',
  'print': 'Usa Imprimir esta página, o descarga la guía de estudio en PDF. La hoja de fórmulas está cerca del final.',
  'discuss': 'Pregunta: ¿cómo ayuda esta unidad a las personas y al planeta? Cada unidad tiene un recuadro verde con un dato y su fuente.',
  'copy': 'Copia la plantilla de guía docente y escribe el nombre de tu clase, el tiempo que tienes y las preguntas que harás.',
  'link': 'Abrir la plantilla de guía docente',
  'toc': 'Para docentes',
 },
 'ar': {
  'h': 'للمعلمين',
  'lead': 'يمكنك تدريس هذا المقرر، أو أن يتابعه الطالب وحده. إنه مجاني. Saving Planets لا تمنح درجة ولا ساعات معتمدة.',
  'time': 'خطّط لخمسة عشر أسبوعًا، نحو 6 إلى 9 ساعات في الأسبوع، بما في ذلك أسابيع المختبر.',
  'counts': 'هذه الصفحة هي المقرر كاملًا: {units} وحدات و{labs} مختبرات ({code}).',
  'how': 'اتبع جدول الخمسة عشر أسبوعًا. اقرأ الوحدة، حلّ التمارين على الورق، ثم افتح الإجابة. في أسبوع المختبر، نفّذ المختبر أو نسخته المنزلية.',
  'check': 'التحقق هو رقم أو نتيجة برمجية في الصفحة يعيد سكربت حسابها قبل النشر. يجب أن يطابق الرقم الظاهر الرقم المعاد حسابه.',
  'print': 'استخدم طباعة هذه الصفحة، أو نزّل دليل الدراسة PDF. ورقة القوانين قرب النهاية.',
  'discuss': 'اسأل: كيف تساعد هذه الوحدة الناس والكوكب؟ في كل وحدة مربع أخضر فيه حقيقة مع مصدرها.',
  'copy': 'انسخ نموذج دليل المعلم واكتب اسم صفك والوقت المتاح والأسئلة التي ستطرحها.',
  'link': 'افتح نموذج دليل المعلم',
  'toc': 'للمعلمين',
 },
 'it': {
  'h': 'Per gli insegnanti',
  'lead': 'Puoi insegnare questo corso, oppure lasciare che uno studente lo faccia da solo. È gratis. Saving Planets non dà un voto né crediti scolastici.',
  'time': 'Prevedi 15 settimane, circa 6–9 ore a settimana, comprese le settimane di laboratorio.',
  'counts': 'Questa pagina è l’intero corso: {units} unità e {labs} laboratori ({code}).',
  'how': 'Segui il calendario di 15 settimane. Leggi l’unità, fai la pratica su carta, poi apri la risposta. Nella settimana di laboratorio, fai il laboratorio o la versione a casa.',
  'check': 'Un controllo è un numero o un risultato di codice nella pagina che uno script ricalcola prima della pubblicazione. Il numero che vedi e quello ricalcolato devono coincidere.',
  'print': 'Usa Stampa questa pagina, oppure scarica la guida di studio PDF. Il formulario è verso la fine.',
  'discuss': 'Chiedi: in che modo questa unità aiuta le persone e il pianeta? Ogni unità ha un riquadro verde con un fatto e la sua fonte.',
  'copy': 'Copia il modello di guida per insegnanti e scrivi il nome della classe, il tempo che hai e le domande che farai.',
  'link': 'Apri il modello di guida per insegnanti',
  'toc': 'Per gli insegnanti',
 },
 'he': {
  'h': 'למורים',
  'lead': 'אפשר ללמד את הקורס הזה, או לתת לתלמיד לעבור אותו לבד. הוא חינם. Saving Planets לא נותנת ציון ולא נקודות זכות.',
  'time': 'תכננו 15 שבועות, בערך 6 עד 9 שעות בשבוע, כולל שבועות המעבדה.',
  'counts': 'העמוד הזה הוא כל הקורס: {units} יחידות ו-{labs} מעבדות ({code}).',
  'how': 'עקבו אחרי לוח 15 השבועות. קראו את היחידה, פתרו על הנייר, ואז פתחו את התשובה. בשבוע מעבדה עשו את המעבדה או את הגרסה הביתית.',
  'check': 'בדיקה היא מספר או תוצאת קוד בעמוד שסקריפט מחשב מחדש לפני הפרסום. המספר שרואים והמספר שחושב מחדש חייבים להתאים.',
  'print': 'השתמשו בהדפסת העמוד, או הורידו את מדריך הלימוד ב-PDF. דף הנוסחאות נמצא לקראת הסוף.',
  'discuss': 'שאלו: איך היחידה הזו עוזרת לאנשים ולכוכב? בכל יחידה יש תיבה ירוקה עם עובדה ומקור.',
  'copy': 'העתיקו את תבנית המדריך למורה וכתבו את שם הכיתה, הזמן שיש לכם, והשאלות שתשאלו.',
  'link': 'פתיחת תבנית המדריך למורה',
  'toc': 'למורים',
 },
}
HUB = {
 'en': ('Courses', 'Free courses you can teach. Each one has a For instructors section. Copy the teacher guide template for your class.', 'Teacher guide template'),
 'fr': ('Cours', 'Cours gratuits à enseigner. Chacun a une section Pour les enseignants. Copiez le modèle de guide pour votre classe.', 'Modèle de guide enseignant'),
 'es': ('Cursos', 'Cursos gratuitos para enseñar. Cada uno tiene una sección Para docentes. Copia la plantilla de guía para tu clase.', 'Plantilla de guía docente'),
 'ar': ('المقررات', 'مقررات مجانية يمكن تدريسها. لكل مقرر قسم للمعلمين. انسخ نموذج الدليل لصفك.', 'نموذج دليل المعلم'),
 'it': ('Corsi', 'Corsi gratuiti da insegnare. Ognuno ha una sezione Per gli insegnanti. Copia il modello di guida per la tua classe.', 'Modello di guida per insegnanti'),
 'he': ('קורסים', 'קורסים חינמיים שאפשר ללמד. לכל קורס יש מקטע למורים. העתיקו את תבנית המדריך לכיתה שלכם.', 'תבנית מדריך למורה'),
}
NOTE = {
 'fr': 'Traduction rédigée par machine, à relire.',
 'es': 'Traducción hecha por máquina, pendiente de revisión.',
 'ar': 'ترجمة آلية بانتظار المراجعة.',
 'it': 'Traduzione automatica, da rivedere.',
 'he': 'תרגום מכונה, ממתין לבדיקה.',
}
TPL = {
 'en': {
  'title': 'Teacher Guide Template',
  'desc': 'A one-page guide teachers can copy for any Saving Planets course: goal, time, materials, steps, questions, and how you will know they learned it.',
  'kicker': 'Copy this page. Write on it. You do not need an account, and you do not pay.',
  'rows': [
   ('Course', 'Write the course name and the code, like CHEM 110.'),
   ('Who it is for', 'Write the age or grade, and what they should already know.'),
   ('Time', 'Write how many weeks and how many minutes you have.'),
   ('Goal', 'Write one sentence a 10-year-old could say back to you.'),
   ('Materials', 'Write what you need: a computer, paper, and anything for the lab or its home version.'),
   ('Steps', 'Hook, teach, practice, check. Use the course’s 15-week schedule.'),
   ('Questions', 'Write three questions. One should ask how the work helps people and the planet.'),
   ('How you will know', 'Look at the practice, the lab, and the quiz. There is no grade from us.'),
   ('Planet', 'Copy one sourced fact from a green box on the course page.'),
   ('Sources', 'Keep the source links next to the fact. Do not drop them.'),
  ],
 },
 'fr': {
  'title': 'Modèle de guide enseignant',
  'desc': 'Un guide d’une page à copier pour n’importe quel cours Saving Planets : objectif, temps, matériel, étapes, questions, et comment savoir que c’est appris.',
  'kicker': 'Copiez cette page. Écrivez dessus. Pas de compte, et rien à payer.',
  'rows': [
   ('Cours', 'Écrivez le nom du cours et le code, par exemple CHEM 110.'),
   ('Pour qui', 'Écrivez l’âge ou le niveau, et ce qu’ils doivent déjà savoir.'),
   ('Temps', 'Écrivez le nombre de semaines et de minutes dont vous disposez.'),
   ('Objectif', 'Écrivez une phrase qu’un enfant de 10 ans pourrait répéter.'),
   ('Matériel', 'Écrivez ce qu’il faut : un ordinateur, du papier, et le nécessaire pour le TP ou sa version à la maison.'),
   ('Étapes', 'Accroche, cours, pratique, vérification. Utilisez le calendrier de 15 semaines du cours.'),
   ('Questions', 'Écrivez trois questions. L’une doit demander en quoi le travail aide les gens et la planète.'),
   ('Comment savoir', 'Regardez la pratique, le TP et le quiz. Nous ne mettons pas de note.'),
   ('Planète', 'Copiez un fait sourcé d’un encadré vert de la page du cours.'),
   ('Sources', 'Gardez les liens des sources à côté du fait. Ne les enlevez pas.'),
  ],
 },
 'es': {
  'title': 'Plantilla de guía docente',
  'desc': 'Una guía de una página para copiar en cualquier curso de Saving Planets: meta, tiempo, materiales, pasos, preguntas y cómo sabrás que lo aprendieron.',
  'kicker': 'Copia esta página. Escribe en ella. No hace falta una cuenta y no se paga.',
  'rows': [
   ('Curso', 'Escribe el nombre del curso y el código, por ejemplo CHEM 110.'),
   ('Para quién', 'Escribe la edad o el grado, y lo que ya deben saber.'),
   ('Tiempo', 'Escribe cuántas semanas y cuántos minutos tienes.'),
   ('Meta', 'Escribe una frase que un niño de 10 años podría repetir.'),
   ('Materiales', 'Escribe lo que hace falta: un ordenador, papel y lo del laboratorio o su versión en casa.'),
   ('Pasos', 'Enganche, explicación, práctica, comprobación. Usa el calendario de 15 semanas del curso.'),
   ('Preguntas', 'Escribe tres preguntas. Una debe preguntar cómo el trabajo ayuda a las personas y al planeta.'),
   ('Cómo sabrás', 'Mira la práctica, el laboratorio y el cuestionario. Nosotros no ponemos nota.'),
   ('Planeta', 'Copia un dato con su fuente de un recuadro verde de la página del curso.'),
   ('Fuentes', 'Deja los enlaces de las fuentes junto al dato. No los quites.'),
  ],
 },
 'ar': {
  'title': 'نموذج دليل المعلم',
  'desc': 'دليل من صفحة واحدة يمكن نسخه لأي مقرر في Saving Planets: الهدف والوقت والمواد والخطوات والأسئلة وكيف تعرف أن الطلاب تعلموا.',
  'kicker': 'انسخ هذه الصفحة. اكتب عليها. لا حساب مطلوب ولا دفع.',
  'rows': [
   ('المقرر', 'اكتب اسم المقرر والرمز، مثل CHEM 110.'),
   ('لمن', 'اكتب العمر أو الصف، وما الذي ينبغي أن يعرفوه مسبقًا.'),
   ('الوقت', 'اكتب عدد الأسابيع والدقائق المتاحة لك.'),
   ('الهدف', 'اكتب جملة يستطيع طفل في العاشرة أن يعيدها.'),
   ('المواد', 'اكتب ما يلزم: حاسوب وورقة وما يحتاجه المختبر أو نسخته المنزلية.'),
   ('الخطوات', 'تمهيد، شرح، تدريب، تحقق. استخدم جدول الخمسة عشر أسبوعًا في المقرر.'),
   ('الأسئلة', 'اكتب ثلاثة أسئلة. واحد منها يسأل كيف يساعد هذا العمل الناس والكوكب.'),
   ('كيف تعرف', 'انظر إلى التمارين والمختبر والاختبار القصير. نحن لا نضع درجة.'),
   ('الكوكب', 'انسخ حقيقة مع مصدرها من مربع أخضر في صفحة المقرر.'),
   ('المصادر', 'أبقِ روابط المصادر بجانب الحقيقة. لا تحذفها.'),
  ],
 },
 'it': {
  'title': 'Modello di guida per insegnanti',
  'desc': 'Una guida di una pagina da copiare per qualsiasi corso di Saving Planets: obiettivo, tempo, materiali, passi, domande e come saprai che hanno imparato.',
  'kicker': 'Copia questa pagina. Scrivici sopra. Non serve un account e non si paga.',
  'rows': [
   ('Corso', 'Scrivi il nome del corso e il codice, per esempio CHEM 110.'),
   ('Per chi', 'Scrivi l’età o la classe, e che cosa devono già sapere.'),
   ('Tempo', 'Scrivi quante settimane e quanti minuti hai.'),
   ('Obiettivo', 'Scrivi una frase che un bambino di 10 anni potrebbe ripetere.'),
   ('Materiali', 'Scrivi che cosa serve: un computer, carta, e il necessario per il laboratorio o la versione a casa.'),
   ('Passi', 'Gancio, spiegazione, pratica, verifica. Usa il calendario di 15 settimane del corso.'),
   ('Domande', 'Scrivi tre domande. Una deve chiedere in che modo il lavoro aiuta le persone e il pianeta.'),
   ('Come saprai', 'Guarda la pratica, il laboratorio e il quiz. Noi non diamo un voto.'),
   ('Pianeta', 'Copia un fatto con la fonte da un riquadro verde della pagina del corso.'),
   ('Fonti', 'Tieni i link delle fonti accanto al fatto. Non toglierli.'),
  ],
 },
 'he': {
  'title': 'תבנית מדריך למורה',
  'desc': 'מדריך של עמוד אחד שאפשר להעתיק לכל קורס ב-Saving Planets: מטרה, זמן, חומרים, צעדים, שאלות, ואיך תדעו שהתלמידים למדו.',
  'kicker': 'העתיקו את העמוד. כתבו עליו. לא צריך חשבון, ולא משלמים.',
  'rows': [
   ('קורס', 'כתבו את שם הקורס ואת הקוד, למשל CHEM 110.'),
   ('למי', 'כתבו גיל או כיתה, ומה הם כבר צריכים לדעת.'),
   ('זמן', 'כתבו כמה שבועות וכמה דקות יש לכם.'),
   ('מטרה', 'כתבו משפט שילד בן 10 יכול לחזור עליו.'),
   ('חומרים', 'כתבו מה צריך: מחשב, נייר, ומה שצריך למעבדה או לגרסה הביתית.'),
   ('צעדים', 'פתיח, הסבר, תרגול, בדיקה. השתמשו בלוח 15 השבועות של הקורס.'),
   ('שאלות', 'כתבו שלוש שאלות. אחת צריכה לשאול איך העבודה עוזרת לאנשים ולכוכב.'),
   ('איך תדעו', 'הסתכלו על התרגול, המעבדה והבוחן. אנחנו לא נותנים ציון.'),
   ('כוכב', 'העתיקו עובדה עם מקור מתיבה ירוקה בעמוד הקורס.'),
   ('מקורות', 'השאירו את קישורי המקור ליד העובדה. אל תמחקו אותם.'),
  ],
 },
}

def live_courses():
    from courses import roadmap as RM
    mods = {}
    for f in sorted(glob.glob('scripts/courses/*.py')):
        name = os.path.basename(f)[:-3]
        if name in ('roadmap', '__init__'): continue
        spec = importlib.util.spec_from_file_location('crs_' + name, f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if getattr(m, 'STATUS', '') == 'live': mods[m.ID] = m
    rows = []
    for yi, (_year, cs) in enumerate(RM.YEARS):
        for cid, _title, _d in cs:
            if cid in mods: rows.append((yi, mods[cid]))
    return rows

def path(lang, page):
    return page if lang == 'en' else f'{lang}/{page}'

def pre(lang):
    return '' if lang == 'en' else '../'

def h1_of(lang, page):
    s = open(path(lang, page), encoding='utf-8').read()
    m = re.search(r'<h1>(.*?)</h1>', s, re.S)
    return m.group(1) if m else E(page)

def year_heads(lang):
    s = open(path(lang, 'Courses.html'), encoding='utf-8').read()
    hs = re.findall(r'<section id="y\d"[^>]*>\s*<h2>(.*?)</h2>', s)
    if len(hs) != 4: raise SystemExit(f'year headings missing on {lang} Courses.html ({len(hs)})')
    return hs

def instruct_html(lang, mod):
    t = INS[lang]
    counts = t['counts'].replace('{units}', str(len(mod.UNITS))).replace('{labs}', str(len(mod.LABS))).replace('{code}', mod.CODE)
    href = pre(lang) + PAGE
    bits = [f'<section class="crs-card" id="instructors" aria-labelledby="instructors-h">',
            f'<h2 id="instructors-h">{E(t["h"])}</h2>',
            f'<p>{E(t["lead"])}</p>',
            '<ul>',
            f'<li>{E(counts)}</li>',
            f'<li>{E(t["time"])}</li>',
            f'<li>{E(t["how"])}</li>',
            f'<li>{E(t["check"])}</li>',
            f'<li>{E(t["print"])}</li>',
            f'<li>{E(t["discuss"])}</li>',
            f'<li>{E(t["copy"])} <a href="{E(href)}">{E(t["link"])}</a></li>',
            '</ul></section>']
    return '<!-- INSTRUCT:START -->' + ''.join(bits) + '<!-- INSTRUCT:END -->'

def splice_course(lang, mod):
    p = path(lang, mod.PAGE)
    if not os.path.exists(p): return False
    s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'<!-- INSTRUCT:START -->.*?<!-- INSTRUCT:END -->', '', s, flags=re.S)
    blk = instruct_html(lang, mod)
    if '<section id="start">' not in s2: raise SystemExit(f'no #start in {p}')
    s2 = s2.replace('<section id="start">', blk + '<section id="start">', 1)
    toc = f'<li><a href="#instructors">{E(INS[lang]["toc"])}</a></li>'
    if 'href="#instructors"' not in s2:
        s2 = re.sub(r'(<a href="#about">.*?</a></li>)', r'\1' + toc, s2, count=1)
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2)
    return True

def teachers_html(lang, courses):
    h, lead, link = HUB[lang]
    years = year_heads(lang)
    parts = [f'<section class="five-ws" id="courses"><h2>{E(h)}</h2><p>{E(lead)}</p>',
             f'<p><a href="{E(pre(lang) + PAGE)}">{E(link)}</a></p>']
    buckets = {i: [] for i in range(4)}
    for yi, mod in courses:
        if not os.path.exists(path(lang, mod.PAGE)): continue
        title = h1_of(lang, mod.PAGE)
        buckets[yi].append(f'<li><a href="{E(mod.PAGE)}#instructors">{title}</a> <span class="t-codes">{E(mod.CODE)}</span></li>')
    for i in range(4):
        if not buckets[i]: continue
        parts.append(f'<h3>{years[i]}</h3><ul class="t-list">' + ''.join(buckets[i]) + '</ul>')
    parts.append('</section>')
    return '<!-- TEACHCRS:START -->' + ''.join(parts) + '<!-- TEACHCRS:END -->'

def splice_teachers(lang, courses):
    p = path(lang, 'Teachers.html')
    s = open(p, encoding='utf-8').read()
    # Nov 11: build-teachers-home.py owns the collapsed course accordion inside TEACHHOME.
    if '<!-- TEACHHOME:START -->' in s:
        return
    s2 = re.sub(r'<!-- TEACHCRS:START -->.*?<!-- TEACHCRS:END -->\n?', '', s, flags=re.S)
    blk = teachers_html(lang, courses)
    anchor = '<section class="five-ws t-hub">'
    if anchor not in s2: raise SystemExit(f'no teacher hub list in {p}')
    s2 = s2.replace(anchor, blk + '\n' + anchor, 1)
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2)

def template_main(lang):
    t = TPL[lang]
    note = f'<p class="lnote" role="note"><small>🤖 {E(NOTE[lang])}</small></p>' if lang != 'en' else ''
    rows = ''.join(f'<li><h3>{E(h)}</h3><p>{E(body)}</p><p class="tg-blank" aria-hidden="true"></p></li>' for h, body in t['rows'])
    hero = (f'<section class="page-hero hero-learn"><div class="page-hero-content"><h1>{E(t["title"])}</h1>'
            f'<p>{E(t["kicker"])}</p></div></section>\n')
    return (hero + f'<div class="lw">{note}<section class="five-ws" id="template"><ol class="tg-steps">{rows}</ol>'
            f'<p><a href="Courses.html">{E(HUB[lang][0])}</a> · <a href="Teachers.html">{h1_of(lang, "Teachers.html")}</a></p>'
            f'</section></div>\n')

STYLE = ('<style>.tg-steps{padding-inline-start:1.2rem}.tg-steps h3{margin:.2rem 0}.tg-blank{display:block;min-height:2.4rem;'
         'border-bottom:1px solid rgba(127,127,127,.55);margin:.2rem 0 1rem}</style>\n')

def write_templates():
    spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py')
    BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
    he = '<link rel="alternate" hreflang="he" href="https://www.savingplanets.com/he/Teacher_Guide.html">'
    for lang in LANGS:
        t = TPL[lang]
        html_page = BL.shell(lang, PAGE, t['title'], t['desc'], template_main(lang), extra_head=STYLE, ld_type='LearningResource')
        if 'hreflang="he"' not in html_page.split('</head>', 1)[0]:
            html_page = html_page.replace('<link rel="alternate" hreflang="x-default"', he + '\n<link rel="alternate" hreflang="x-default"', 1)
        img_lang = lang if os.path.exists(f'assets/og/{lang}/Teachers.jpg') else 'en'
        img = f'https://www.savingplanets.com/assets/og/{img_lang}/Teachers.jpg'
        html_page = re.sub(r'(<meta property="og:image" content=")[^"]*"', r'\1' + img + '"', html_page, count=1)
        html_page = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', r'\1' + img + '"', html_page, count=1)
        html_page = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1' + E(t['title']) + '"', html_page, count=1)
        dest = path(lang, PAGE)
        if not os.path.exists(dest) or open(dest, encoding='utf-8').read() != html_page:
            open(dest, 'w', encoding='utf-8').write(html_page)

def _sitemap_files():
    """sitemap.xml is a <sitemapindex> of per-language sitemaps since PR #206;
    fall back to the legacy single urlset if that is what is on disk."""
    sm = open('sitemap.xml', encoding='utf-8').read()
    if '<sitemapindex' in sm:
        files = [os.path.basename(u) for u in re.findall(r'<loc>https://www\.savingplanets\.com/(sitemap-[a-z]{2}\.xml)</loc>', sm)]
        if not files: raise SystemExit('sitemap index lists no per-language sitemaps')
        return files, True
    return ['sitemap.xml'], False

def sitemap():
    files, indexed = _sitemap_files()
    total_teachers = total_guide = 0
    for fn in files:
        if not os.path.exists(fn): raise SystemExit(f'sitemap missing: {fn}')
        sm = open(fn, encoding='utf-8').read()
        pat = r'  <url><loc>https://www\.savingplanets\.com/(?:[a-z]{2}/)?Teachers\.html</loc>.*?</url>\n'
        n_t = len(re.findall(pat, sm))
        total_teachers += n_t
        if PAGE in sm:
            total_guide += sm.count(f'{PAGE}</loc>')
            continue
        def repl(m):
            block = m.group(0)
            return block + block.replace('Teachers.html', PAGE)
        sm2, n = re.subn(pat, repl, sm)
        if n == 0: raise SystemExit(f'{fn} Teachers.html entries: 0')
        total_guide += sm2.count(f'{PAGE}</loc>')
        open(fn, 'w', encoding='utf-8').write(sm2)
    if total_teachers < 6: raise SystemExit(f'sitemap Teachers.html entries: {total_teachers} across {len(files)} file(s)')
    if total_guide < 6: raise SystemExit(f'sitemap {PAGE} entries: {total_guide} across {len(files)} file(s)')

def apply():
    courses = live_courses()
    n = 0
    for lang in LANGS:
        for _yi, mod in courses:
            if splice_course(lang, mod): n += 1
        splice_teachers(lang, courses)
    write_templates()
    sitemap()
    print(f'teacher guide: {n} course pages, Teachers.html × {len(LANGS)}, {PAGE} × {len(LANGS)}')

if __name__ == '__main__':
    apply()
