#!/usr/bin/env python3
"""MIT OCW-style section bar on each live course: Syllabus, Calendar, Units, Labs, Problem Sets, Exams.

Nov 2 2026 (Bryan-approved). The bar jumps to those parts of the page. Nothing is hidden, so it
works without JavaScript, in print, and in RTL. Problem sets stay inside each unit; this adds an
index. Idempotent. Called at the end of build-courses.py after the teacher-guide splice.
"""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
E = lambda s: html.escape(s, quote=True)
VOLD, VNEW = '20261024h', '20261102a'

T = {
 'en': {'nav': 'Course sections', 'syl': 'Syllabus', 'cal': 'Calendar', 'units': 'Units', 'labs': 'Labs', 'psets': 'Problem Sets', 'exams': 'Exams',
        'pintro': 'These practice problems live inside each unit. Work on paper first, then open the answer.',
        'n': '{n} problems'},
 'fr': {'nav': 'Parties du cours', 'syl': 'Programme', 'cal': 'Calendrier', 'units': 'Unités', 'labs': 'Travaux pratiques', 'psets': 'Exercices', 'exams': 'Examens',
        'pintro': 'Ces exercices sont dans chaque unité. Faites-les sur papier, puis ouvrez la réponse.',
        'n': '{n} exercices'},
 'es': {'nav': 'Partes del curso', 'syl': 'Programa', 'cal': 'Calendario', 'units': 'Unidades', 'labs': 'Laboratorios', 'psets': 'Problemas', 'exams': 'Exámenes',
        'pintro': 'Estos problemas están dentro de cada unidad. Hazlos en papel y luego abre la respuesta.',
        'n': '{n} problemas'},
 'ar': {'nav': 'أقسام المقرر', 'syl': 'المنهج', 'cal': 'التقويم', 'units': 'الوحدات', 'labs': 'المختبرات', 'psets': 'مجموعات المسائل', 'exams': 'الامتحانات',
        'pintro': 'هذه التمارين داخل كل وحدة. حلّها على الورق أولًا، ثم افتح الإجابة.',
        'n': '{n} مسائل'},
 'it': {'nav': 'Parti del corso', 'syl': 'Programma', 'cal': 'Calendario', 'units': 'Unità', 'labs': 'Laboratori', 'psets': 'Esercizi', 'exams': 'Esami',
        'pintro': 'Questi esercizi stanno dentro ogni unità. Falli su carta, poi apri la risposta.',
        'n': '{n} esercizi'},
 'he': {'nav': 'חלקי הקורס', 'syl': 'סילבוס', 'cal': 'לוח שנה', 'units': 'יחידות', 'labs': 'מעבדות', 'psets': 'תרגילים', 'exams': 'מבחנים',
        'pintro': 'התרגילים האלה נמצאים בתוך כל יחידה. פתרו על הנייר, ואז פתחו את התשובה.',
        'n': '{n} תרגילים'},
}

def course_files():
    found = []
    for lang in LANGS:
        base = '.' if lang == 'en' else lang
        for name in os.listdir(base):
            if not name.endswith('.html'): continue
            f = name if lang == 'en' else f'{lang}/{name}'
            with open(f, encoding='utf-8') as fh:
                if 'data-course="' in fh.read(): found.append((lang, f))
    return found

def problems(s):
    items = []
    for part in re.split(r'(?=<section class="crs-unit")', s)[1:]:
        unit = part.split('</section>', 1)[0]
        idm = re.match(r'<section class="crs-unit" id="([^"]+)"', unit)
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', unit)
        prac = re.search(r'<ol class="crs-prac">(.*)</ol>', unit, re.S)
        if not (idm and hm and prac): continue
        items.append((idm.group(1), hm.group(1), prac.group(1).count('<li>')))
    return items

def nav(lang):
    t = T[lang]
    links = [('#syllabus', t['syl']), ('#schedule', t['cal']), ('#units', t['units']),
             ('#lab', t['labs']), ('#problem-sets', t['psets']), ('#exam', t['exams'])]
    a = ''.join(f'<a href="{h}">{E(lab)}</a>' for h, lab in links)
    return f'<!-- OCW:START --><nav class="crs-ocw" aria-label="{E(t["nav"])}">{a}</nav><!-- OCW:END -->'

def pset(lang, items):
    t = T[lang]
    lis = ''.join(f'<li><a href="#{i}">{title}</a> <span class="t-codes">{E(t["n"].replace("{n}", str(n)))}</span></li>' for i, title, n in items)
    return (f'<!-- OCW-PSET:START --><section class="crs-pset" id="problem-sets"><h2>{E(t["psets"])}</h2>'
            f'<p>{E(t["pintro"])}</p><ol>{lis}</ol></section><!-- OCW-PSET:END -->')

def apply_one(lang, f):
    s = open(f, encoding='utf-8').read()
    if '<section id="about">' not in s or '<section class="crs-unit"' not in s: return False
    orig = s
    s = re.sub(r'<!-- OCW:START -->.*?<!-- OCW:END -->', '', s, flags=re.S)
    s = re.sub(r'<!-- OCW-PSET:START -->.*?<!-- OCW-PSET:END -->', '', s, flags=re.S)
    s = s.replace('<!-- OCW-SYL:START --><div id="syllabus" class="crs-ocw-sec" tabindex="-1">', '')
    s = s.replace('</div><!-- OCW-SYL:END -->', '')
    s = s.replace(f'<!-- OCW-U:START --><div id="units" class="crs-ocw-sec" tabindex="-1"><h2 class="crs-ocw-h">{E(T[lang]["units"])}</h2>', '')
    s = s.replace('</div><!-- OCW-U:END -->', '')
    if '<p class="crs-tools"' not in s or '<section id="schedule">' not in s or '<section id="lab">' not in s:
        raise SystemExit(f'OCW anchors missing in {f}')
    s = s.replace('<p class="crs-tools"', nav(lang) + '<p class="crs-tools"', 1)
    s = s.replace('<section id="about">', '<!-- OCW-SYL:START --><div id="syllabus" class="crs-ocw-sec" tabindex="-1"><section id="about">', 1)
    s = s.replace('<section id="schedule">', '</div><!-- OCW-SYL:END --><section id="schedule">', 1)
    s = s.replace('<section class="crs-unit"', f'<!-- OCW-U:START --><div id="units" class="crs-ocw-sec" tabindex="-1"><h2 class="crs-ocw-h">{E(T[lang]["units"])}</h2><section class="crs-unit"', 1)
    s = s.replace('<section id="lab">', '</div><!-- OCW-U:END -->' + pset(lang, problems(s)) + '<section id="lab">', 1)
    s = s.replace(f'courses.css?v={VOLD}', f'courses.css?v={VNEW}').replace(f'courses.js?v={VOLD}', f'courses.js?v={VNEW}')
    if s.count('id="syllabus"') != 1 or s.count('id="units"') != 1 or s.count('id="problem-sets"') != 1:
        raise SystemExit(f'OCW wrap failed on {f}')
    if s != orig: open(f, 'w', encoding='utf-8').write(s)
    return True

def apply():
    n = 0
    for lang, f in course_files():
        if apply_one(lang, f): n += 1
    print(f'course ocw: {n} pages')

if __name__ == '__main__':
    apply()
