#!/usr/bin/env python3
"""Oct 14 2026: department inboxes. Contact cards (teachers@, privacy@, translate@), grown-ups/teacher notes on Teachers,
Lesson_Builder and Kids_Map, About translate@ note, footer hello@ line, and a 'Help translate' line in fr/es/ar footers.
Writes EN blocks (marker comments) + i18n strings; run before i18n-build and again after it (fixes translated footers). Idempotent."""
import re, glob, os, json
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
S = 'mailto:%s@savingplanets.com?subject=%s'
M = {'teachers': S % ('teachers', 'Classroom%20question'), 'privacy': S % ('privacy', 'Privacy%20request'),
     'translate': S % ('translate', 'Help%20translate%20Saving%20Planets'), 'hello': S % ('hello', 'Question')}
TR = {
 'Teachers & Schools': ('Enseignants et écoles', 'Docentes y escuelas', 'المعلمون والمدارس'),
 'Classroom questions, lesson-plan requests and school partnerships.': ('Questions de classe, demandes de plans de cours et partenariats scolaires.', 'Preguntas de clase, solicitudes de planes de clase y alianzas escolares.', 'أسئلة الصف وطلبات خطط الدروس والشراكات المدرسية.'),
 'Privacy & Data Requests': ('Confidentialité et données', 'Privacidad y datos', 'الخصوصية وطلبات البيانات'),
 'Questions about your data, or a deletion request.': ('Questions sur vos données ou demande de suppression.', 'Preguntas sobre tus datos o una solicitud de borrado.', 'أسئلة عن بياناتك أو طلب حذف.'),
 'Help Translate': ('Aider à traduire', 'Ayuda a traducir', 'ساعد في الترجمة'),
 'Volunteer translators and language corrections for French, Spanish and Arabic.': ('Traducteurs bénévoles et corrections linguistiques en français, espagnol et arabe.', 'Traductores voluntarios y correcciones de idioma en francés, español y árabe.', 'المترجمون المتطوعون وتصحيحات اللغة للفرنسية والإسبانية والعربية.'),
 'For grown-ups and teachers: classroom questions, lesson-plan requests or school partnerships?': ('Pour les adultes et les enseignants : questions de classe, demandes de plans de cours ou partenariats scolaires ?', 'Para adultos y docentes: ¿preguntas de clase, solicitudes de planes de clase o alianzas escolares?', 'للكبار والمعلمين: أسئلة الصف أو طلبات خطط الدروس أو الشراكات المدرسية؟'),
 'Speak French, Spanish or Arabic? Volunteer translators and language corrections are welcome.': ('Vous parlez français, espagnol ou arabe ? Les traducteurs bénévoles et les corrections linguistiques sont les bienvenus.', '¿Hablas francés, español o árabe? Los traductores voluntarios y las correcciones de idioma son bienvenidos.', 'هل تتحدث الفرنسية أو الإسبانية أو العربية؟ نرحب بالمترجمين المتطوعين وتصحيحات اللغة.'),
 'Questions? Write to': ('Des questions ? Écrivez à', '¿Preguntas? Escribe a', 'أسئلة؟ راسل'),
}
HELP = {'fr': 'Une traduction à améliorer ? Aidez-nous :', 'es': '¿Ves una traducción que mejorar? Ayúdanos:', 'ar': 'هل ترى ترجمة تحتاج إلى تحسين؟ ساعدنا:'}
def a(k): return f'<a href="{M[k]}">{k}@savingplanets.com</a>'
def card(h, p, k): return f'<div class="w-card" id="dept-{k}"><h3>{h.replace("&", "&amp;")}</h3><p>{p}</p><p>{a(k)}</p></div>'
def put(s, name, block, before):
    blk = f'<!-- DEPT:{name} -->{block}<!-- /DEPT:{name} -->'
    if f'<!-- DEPT:{name} -->' in s: return re.sub(rf'<!-- DEPT:{name} -->.*?<!-- /DEPT:{name} -->', lambda m: blk, s, flags=re.S)
    i = s.find(before)
    return s if i < 0 else s[:i] + blk + s[i:]
for l, d in (('fr', 0), ('es', 1), ('ar', 2)):
    f = f'i18n/{l}.json'; m = json.load(open(f, encoding='utf-8')); ch = False
    for k, v in TR.items():
        if m.get(k) != v[d]: m[k] = v[d]; ch = True
    if ch: json.dump(m, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
n = 0
for lang in ('', 'fr/', 'es/', 'ar/'):
    for f in glob.glob(lang + '*.html'):
        s = open(f, encoding='utf-8').read(); o = s
        base = os.path.basename(f)
        if not lang:  # EN content blocks (i18n-build translates them for fr/es/ar)
            if base == 'Contact.html':
                s = put(s, 'contact', card('Teachers & Schools', TR['Teachers & Schools'] and 'Classroom questions, lesson-plan requests and school partnerships.', 'teachers') +
                        card('Privacy & Data Requests', 'Questions about your data, or a deletion request.', 'privacy') +
                        card('Help Translate', 'Volunteer translators and language corrections for French, Spanish and Arabic.', 'translate'), '<div class="w-card"><h3>General Questions</h3>')
            if base in ('Teachers.html', 'Lesson_Builder.html', 'Kids_Map.html'):
                s = put(s, 'teachers', '<section class="help-actions dept-note" id="grown-ups"><p>For grown-ups and teachers: classroom questions, lesson-plan requests or school partnerships?</p><p>' + a('teachers') + '</p></section>', '</main>')
            if base == 'About.html':
                s = put(s, 'translate', '<section class="help-actions dept-note" id="translate"><p>Speak French, Spanish or Arabic? Volunteer translators and language corrections are welcome.</p><p>' + a('translate') + '</p></section>', '</main>')
        if '<footer>' in s and not base.startswith('google') and base not in ('ways_to_help.html', 'ways-to-help.html'):
            ln = lang.rstrip('/')
            extra = f'<p class="dept-foot">Questions? Write to {a("hello")}</p>'
            if ln:
                q = {'fr': 'Des questions ? Écrivez à', 'es': '¿Preguntas? Escribe a', 'ar': 'أسئلة؟ راسل'}[ln]
                extra = f'<p class="dept-foot">{q} {a("hello")}</p><p class="dept-foot">{HELP[ln]} {a("translate")}</p>'
            s = put(s, 'foot', extra, '</footer>')
        if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print(f'dept-contacts: {n} pages updated')
