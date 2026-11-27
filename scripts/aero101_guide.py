#!/usr/bin/env python3
"""Editable AERO 101 study guide (.docx) in all six languages.
Original lessons stay CC BY-NC-SA 4.0, the same licence as the web page.
Third-party text is not copied into the file."""
import html, json, os, sys, zipfile
from xml.sax.saxutils import escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
from courses import aero101 as C
from courses import aero101_review as AR
import importlib.util
spec = importlib.util.spec_from_file_location('bc', 'scripts/build-courses.py')
BC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BC)

TR = {}
for f in ('i18n/courses/aero101.json', 'i18n/courses/_shared.json'):
    for k, v in json.load(open(f, encoding='utf8')).items():
        TR.setdefault(k, {}).update(v)

def tr(s, lang):
    if lang == 'en' or not isinstance(s, str):
        return s
    return TR.get(s, {}).get(lang, s)

def P(text, rtl=False, bold=False):
    rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:rtl/>' if rtl else '') + '</w:rPr>'
    ppr = '<w:pPr>' + ('<w:bidi/>' if rtl else '') + '</w:pPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'

def document(paragraphs, rtl):
    sect = '<w:sectPr>' + ('<w:bidi/>' if rtl else '') + '</w:sectPr>'
    body = ''.join(paragraphs) + sect
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{body}</w:body></w:document>')

CT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''
RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

LABEL = {
 'en': {'unit': 'Unit', 'obj': 'Objectives', 'ideas': 'Key ideas', 'eq': 'Equations', 'work': 'Worked examples',
        'prac': 'Practice', 'ans': 'Answer', 'lab': 'Labs', 'goal': 'Goal', 'steps': 'Procedure', 'safe': 'Safety',
        'exam': 'Exams', 'lic': 'Original text, lessons and labs: © Saving Planets, licensed CC BY-NC-SA 4.0.',
        'lic2': 'Images and media keep their own credits and licences.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'The web page is the source of this guide.',
        'page': 'https://www.savingplanets.com/Intro_to_Aerospace_Engineering.html'},
 'fr': {'unit': 'Unité', 'obj': 'Objectifs', 'ideas': 'Idées clés', 'eq': 'Équations', 'work': 'Exemples résolus',
        'prac': 'Entraînement', 'ans': 'Réponse', 'lab': 'Travaux pratiques', 'goal': 'But', 'steps': 'Marche à suivre', 'safe': 'Sécurité',
        'exam': 'Examens', 'lic': 'Textes, leçons et labos originaux : © Saving Planets, sous licence CC BY-NC-SA 4.0.',
        'lic2': 'Les images et les médias gardent leurs propres crédits et licences.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'La page web est la source de ce guide.',
        'page': 'https://www.savingplanets.com/fr/Intro_to_Aerospace_Engineering.html'},
 'es': {'unit': 'Unidad', 'obj': 'Objetivos', 'ideas': 'Ideas clave', 'eq': 'Ecuaciones', 'work': 'Ejemplos resueltos',
        'prac': 'Práctica', 'ans': 'Respuesta', 'lab': 'Laboratorios', 'goal': 'Meta', 'steps': 'Procedimiento', 'safe': 'Seguridad',
        'exam': 'Exámenes', 'lic': 'Textos, lecciones y laboratorios originales: © Saving Planets, con licencia CC BY-NC-SA 4.0.',
        'lic2': 'Las imágenes y los medios conservan sus propios créditos y licencias.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'La página web es la fuente de esta guía.',
        'page': 'https://www.savingplanets.com/es/Intro_to_Aerospace_Engineering.html'},
 'ar': {'unit': 'الوحدة', 'obj': 'الأهداف', 'ideas': 'الأفكار الأساسية', 'eq': 'المعادلات', 'work': 'أمثلة محلولة',
        'prac': 'تدريب', 'ans': 'الإجابة', 'lab': 'المختبرات', 'goal': 'الهدف', 'steps': 'الخطوات', 'safe': 'السلامة',
        'exam': 'الاختبارات', 'lic': 'النصوص والدروس والمختبرات الأصلية: © Saving Planets، مرخّصة بموجب CC BY-NC-SA 4.0.',
        'lic2': 'تحتفظ الصور والوسائط بنسبها وتراخيصها الخاصة.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'صفحة الويب هي مصدر هذا الدليل.',
        'page': 'https://www.savingplanets.com/ar/Intro_to_Aerospace_Engineering.html'},
 'it': {'unit': 'Unità', 'obj': 'Obiettivi', 'ideas': 'Idee chiave', 'eq': 'Equazioni', 'work': 'Esempi svolti',
        'prac': 'Esercizi', 'ans': 'Risposta', 'lab': 'Laboratori', 'goal': 'Obiettivo', 'steps': 'Procedura', 'safe': 'Sicurezza',
        'exam': 'Esami', 'lic': 'Testi, lezioni e laboratori originali: © Saving Planets, con licenza CC BY-NC-SA 4.0.',
        'lic2': 'Immagini e media mantengono i propri crediti e le proprie licenze.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'La pagina web è la fonte di questa guida.',
        'page': 'https://www.savingplanets.com/it/Intro_to_Aerospace_Engineering.html'},
 'he': {'unit': 'יחידה', 'obj': 'מטרות', 'ideas': 'רעיונות מרכזיים', 'eq': 'משוואות', 'work': 'דוגמאות פתורות',
        'prac': 'תרגול', 'ans': 'תשובה', 'lab': 'מעבדות', 'goal': 'מטרה', 'steps': 'מהלך', 'safe': 'בטיחות',
        'exam': 'מבחנים', 'lic': 'הטקסטים, השיעורים והמעבדות המקוריים: © Saving Planets, ברישיון CC BY-NC-SA 4.0.',
        'lic2': 'תמונות ומדיה שומרים על הקרדיטים והרישיונות שלהם.',
        'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
        'web': 'עמוד האינטרנט הוא המקור של המדריך הזה.',
        'page': 'https://www.savingplanets.com/he/Intro_to_Aerospace_Engineering.html'},
}

def build(lang):
    rtl = lang in ('ar', 'he')
    L = LABEL[lang]
    t = AR.T[lang]
    ps = []
    def add(text, bold=False):
        ps.append(P(text, rtl, bold))
    add(tr(C.TITLE, lang), True)
    add(C.CODE + ' · ' + t['when'])
    add(t['who'])
    add(t['disclose'])
    add(BC.AERO_POLICY[lang])
    add(L['lic'])
    add(L['lic2'])
    add(L['url'])
    add(t['reviewed'] + ': ' + t['when'])
    add(t['sources'])
    add(L['web'] + ' ' + L['page'])
    for i, u in enumerate(C.UNITS, 1):
        add(f"{L['unit']} {i}. {tr(u['title'], lang)}", True)
        add(tr(u['summary'], lang))
        add(L['obj'], True)
        for o in u['objectives']:
            add('• ' + tr(o, lang))
        add(L['ideas'], True)
        for c in u['concepts']:
            add(tr(c, lang))
        add(L['eq'], True)
        for tex, cap in u['eqs']:
            add(tr(cap, lang) + ' — ' + BC.tex_plain(tex))
        add(L['work'], True)
        for n, w in enumerate(u['worked'], 1):
            add(f"{n}. {tr(w['q'], lang)}", True)
            for s in w['steps']:
                add(tr(s, lang))
            add(L['ans'] + ': ' + tr(w['a'], lang))
        add(L['prac'], True)
        for q, a in u['practice']:
            add(tr(q, lang))
            add(L['ans'] + ': ' + tr(a, lang))
    add(L['lab'], True)
    for lab in C.LABS:
        add(tr(lab['title'], lang), True)
        add(L['goal'] + ': ' + tr(lab['goal'], lang))
        add(L['steps'], True)
        for s in lab['steps']:
            add('• ' + tr(s, lang))
        add(L['safe'], True)
        for s in lab['safety']:
            add('• ' + tr(s, lang))
    add(L['exam'], True)
    for title, probs in C.EXAMS:
        add(tr(title, lang), True)
        for n, (q, steps, a) in enumerate(probs, 1):
            add(f"{n}. {tr(q, lang)}")
            for s in steps:
                add(tr(s, lang))
            add(L['ans'] + ': ' + tr(a, lang))
    add(t['who'])
    add(L['lic'])
    xml = document(ps, rtl)
    name = 'Intro_to_Aerospace_Engineering_Study_Guide' + ('' if lang == 'en' else '_' + lang) + '.docx'
    path = os.path.join('assets', 'courses', name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CT)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/document.xml', xml.encode('utf-8'))
    return path, os.path.getsize(path)

if __name__ == '__main__':
    for lang in ('en', 'fr', 'es', 'ar', 'it', 'he'):
        path, size = build(lang)
        print(lang, path, size)
