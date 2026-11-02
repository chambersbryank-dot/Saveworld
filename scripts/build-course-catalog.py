#!/usr/bin/env python3
"""Filterable course catalog on Courses.html, plus the numbering rule and flagged outliers.

Nov 2 2026 (Bryan-approved). Filters: year (level), subject, language the course is published in.
Numbering rule: the first digit is the year (1 freshman … 4 senior), the letters are the subject,
and a lab keeps the lecture number plus L. Outliers are flagged on the card. Codes are not renamed.
Idempotent. Called at the end of build-courses.py. No hero or analytics changes.
"""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
E = lambda s: html.escape(s, quote=True)

UI = {
 'en': {'title': 'Filter the catalog', 'level': 'Level', 'subject': 'Subject', 'lang': 'Language',
        'all': 'All', 'y': ['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        'sub': {'CHEM': 'Chemistry', 'PHYS': 'Physics', 'MATH': 'Math', 'ENGR': 'Engineering', 'AERO': 'Aerospace'},
        'count': 'Showing {n}',
        'rule': 'Numbering rule: the first digit is the year (1 freshman, 2 sophomore, 3 junior, 4 senior). The letters name the subject. A lab uses the same number plus L. Cards below flag numbers that do not follow the usual step. We are not renaming codes that are already published.',
        'flags': {
            'AERO 101': 'Flag: this is the only aerospace number that is not a multiple of 10.',
            'MATH 111': 'Flag: this steps by 1 from MATH 110. Later math courses step by 10.',
            'AERO 470': 'Flag: 470 is numbered before the capstone (AERO 490) but listed after it.',
        }},
 'fr': {'title': 'Filtrer le catalogue', 'level': 'Niveau', 'subject': 'Matière', 'lang': 'Langue',
        'all': 'Tout', 'y': ['Année 1', 'Année 2', 'Année 3', 'Année 4'],
        'sub': {'CHEM': 'Chimie', 'PHYS': 'Physique', 'MATH': 'Maths', 'ENGR': 'Ingénierie', 'AERO': 'Aérospatiale'},
        'count': '{n} affichés',
        'rule': 'Règle de numérotation : le premier chiffre est l’année (1 première année, 2 deuxième, 3 troisième, 4 quatrième). Les lettres nomment la matière. Un TP garde le même numéro plus L. Les cartes ci-dessous signalent un numéro qui ne suit pas le pas habituel. Nous ne renommons pas un code déjà publié.',
        'flags': {
            'AERO 101': 'Signalé : c’est le seul numéro d’aérospatiale qui n’est pas un multiple de 10.',
            'MATH 111': 'Signalé : celui-ci avance de 1 après MATH 110. Les maths suivantes avancent de 10.',
            'AERO 470': 'Signalé : 470 est numéroté avant le projet final (AERO 490) mais listé après.',
        }},
 'es': {'title': 'Filtrar el catálogo', 'level': 'Nivel', 'subject': 'Materia', 'lang': 'Idioma',
        'all': 'Todo', 'y': ['Año 1', 'Año 2', 'Año 3', 'Año 4'],
        'sub': {'CHEM': 'Química', 'PHYS': 'Física', 'MATH': 'Matemáticas', 'ENGR': 'Ingeniería', 'AERO': 'Aeroespacial'},
        'count': 'Se muestran {n}',
        'rule': 'Regla de numeración: el primer dígito es el año (1 primer año, 2 segundo, 3 tercero, 4 cuarto). Las letras nombran la materia. Un laboratorio usa el mismo número más L. Las fichas de abajo marcan un número que no sigue el paso habitual. No cambiamos un código ya publicado.',
        'flags': {
            'AERO 101': 'Aviso: es el único número de aeroespacial que no es múltiplo de 10.',
            'MATH 111': 'Aviso: este avanza 1 desde MATH 110. Los cursos de matemáticas posteriores avanzan de 10 en 10.',
            'AERO 470': 'Aviso: 470 está numerado antes del proyecto final (AERO 490) pero aparece después.',
        }},
 'ar': {'title': 'تصفية الفهرس', 'level': 'المستوى', 'subject': 'المادة', 'lang': 'اللغة',
        'all': 'الكل', 'y': ['السنة 1', 'السنة 2', 'السنة 3', 'السنة 4'],
        'sub': {'CHEM': 'كيمياء', 'PHYS': 'فيزياء', 'MATH': 'رياضيات', 'ENGR': 'هندسة', 'AERO': 'طيران وفضاء'},
        'count': 'المعروض {n}',
        'rule': 'قاعدة الترقيم: الرقم الأول هو السنة (1 سنة أولى، 2 ثانية، 3 ثالثة، 4 رابعة). الحروف تسمي المادة. المختبر يستخدم الرقم نفسه مع حرف L. البطاقات أدناه تشير إلى رقم لا يتبع الخطوة المعتادة. لا نغيّر رمزًا نُشر بالفعل.',
        'flags': {
            'AERO 101': 'تنبيه: هذا رقم الطيران والفضاء الوحيد الذي ليس من مضاعفات 10.',
            'MATH 111': 'تنبيه: هذا يزيد 1 عن MATH 110. مقررات الرياضيات اللاحقة تزيد بمقدار 10.',
            'AERO 470': 'تنبيه: 470 مرقّم قبل مشروع التخرج (AERO 490) لكنه مذكور بعده.',
        }},
 'it': {'title': 'Filtra il catalogo', 'level': 'Livello', 'subject': 'Materia', 'lang': 'Lingua',
        'all': 'Tutti', 'y': ['Anno 1', 'Anno 2', 'Anno 3', 'Anno 4'],
        'sub': {'CHEM': 'Chimica', 'PHYS': 'Fisica', 'MATH': 'Matematica', 'ENGR': 'Ingegneria', 'AERO': 'Aerospaziale'},
        'count': 'Mostrati {n}',
        'rule': 'Regola di numerazione: la prima cifra è l’anno (1 primo anno, 2 secondo, 3 terzo, 4 quarto). Le lettere indicano la materia. Un laboratorio usa lo stesso numero più L. Le schede sotto segnalano un numero che non segue il passo abituale. Non rinominiamo un codice già pubblicato.',
        'flags': {
            'AERO 101': 'Segnalato: è l’unico numero aerospaziale che non è un multiplo di 10.',
            'MATH 111': 'Segnalato: questo avanza di 1 da MATH 110. I corsi di matematica successivi avanzano di 10.',
            'AERO 470': 'Segnalato: 470 è numerato prima del progetto finale (AERO 490) ma è elencato dopo.',
        }},
 'he': {'title': 'סינון הקטלוג', 'level': 'רמה', 'subject': 'מקצוע', 'lang': 'שפה',
        'all': 'הכל', 'y': ['שנה 1', 'שנה 2', 'שנה 3', 'שנה 4'],
        'sub': {'CHEM': 'כימיה', 'PHYS': 'פיזיקה', 'MATH': 'מתמטיקה', 'ENGR': 'הנדסה', 'AERO': 'אווירונאוטיקה'},
        'count': 'מוצגים {n}',
        'rule': 'כלל המספור: הספרה הראשונה היא השנה (1 שנה א, 2 שנה ב, 3 שנה ג, 4 שנה ד). האותיות הן המקצוע. מעבדה משתמשת באותו מספר ועוד L. הכרטיסים למטה מסמנים מספר שלא צועד כמו השאר. לא משנים קוד שכבר פורסם.',
        'flags': {
            'AERO 101': 'סימון: זה מספר האווירונאוטיקה היחיד שאינו כפולה של 10.',
            'MATH 111': 'סימון: זה עולה ב-1 מ-MATH 110. קורסי המתמטיקה שאחריו עולים ב-10.',
            'AERO 470': 'סימון: 470 ממוספר לפני פרויקט הגמר (AERO 490) אבל מופיע אחריו.',
        }},
}
LANGNAME = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية', 'it': 'Italiano', 'he': 'עברית'}
JS = r"""<script>(function(){var root=document.querySelector('.crs');if(!root)return;var bar=root.querySelector('.crs-filters');if(!bar)return;
var cards=[].slice.call(root.querySelectorAll('.crs-c')),state={level:'',subject:'',lang:''};
var out=bar.querySelector('[data-count]'),tpl=out?out.getAttribute('data-tpl'):'{n}';
function apply(){var n=0;cards.forEach(function(c){var ok=(!state.level||c.dataset.level===state.level)&&(!state.subject||c.dataset.subject===state.subject)&&(!state.lang||(c.dataset.langs||'').split(' ').indexOf(state.lang)>=0);c.hidden=!ok;if(ok)n++});
root.querySelectorAll('section[id^="y"]').forEach(function(sec){var any=false;sec.querySelectorAll('.crs-c').forEach(function(c){if(!c.hidden)any=true});sec.hidden=!any});
if(out)out.textContent=tpl.replace('{n}',n)}
bar.addEventListener('click',function(e){var b=e.target.closest('button[data-k]');if(!b)return;var k=b.dataset.k,v=b.dataset.v||'';state[k]=v;
bar.querySelectorAll('button[data-k="'+k+'"]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});apply()});
apply()})();</script>"""

def published(page):
    return [l for l in LANGS if os.path.exists(page if l == 'en' else f'{l}/{page}')]

def enrich(card, lang):
    t = UI[lang]
    kick = re.search(r'class="crs-kicker">(.*?)</p>', card)
    code = html.unescape(kick.group(1)) if kick else ''
    base = code.split(' + ')[0]
    sub = (re.match(r'([A-Z]+)', base) or [None, ''])[1] if False else (re.match(r'([A-Z]+)', base).group(1) if re.match(r'([A-Z]+)', base) else '')
    num = re.search(r'(\d)', base)
    level = num.group(1) if num else ''
    href = re.search(r'href="(?:\.\./)?([^"]+\.html)"', card)
    langs = ' '.join(published(href.group(1))) if href else ''
    card = re.sub(r'\sdata-(?:level|subject|langs)="[^"]*"', '', card)
    card = re.sub(r'<p class="crs-flag">.*?</p>', '', card)
    card = re.sub(r'class="crs-c live"[^>]*>', f'class="crs-c live" data-level="{level}" data-subject="{sub}" data-langs="{langs}">', card, count=1)
    flag = t['flags'].get(base)
    if flag: card = card.replace('</li>', f'<p class="crs-flag">{E(flag)}</p></li>', 1)
    return card

def buttons(lang, key, opts):
    t = UI[lang]
    label = t[key] if key != 'lang' else t['lang']
    btns = f'<button type="button" data-k="{key}" data-v="" aria-pressed="true">{E(t["all"])}</button>'
    for val, name in opts:
        btns += f'<button type="button" data-k="{key}" data-v="{E(val)}" aria-pressed="false">{E(name)}</button>'
    return f'<div class="crs-frow"><span class="crs-fl">{E(label)}</span>{btns}</div>'

def block(lang):
    t = UI[lang]
    levels = buttons(lang, 'level', [(str(i), t['y'][i - 1]) for i in range(1, 5)])
    subs = buttons(lang, 'subject', list(t['sub'].items()))
    langs = buttons(lang, 'lang', [(l, LANGNAME[l]) for l in LANGS])
    return ('<!-- CATALOG:START --><section class="crs-filters" aria-labelledby="catalog-h">'
            f'<h2 id="catalog-h">{E(t["title"])}</h2><p class="crs-rule">{E(t["rule"])}</p>'
            f'{levels}{subs}{langs}<p data-count data-tpl="{E(t["count"])}">{E(t["count"].replace("{n}", "30"))}</p>'
            f'</section>{JS}<!-- CATALOG:END -->')

def apply_one(lang, f):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- CATALOG:START -->.*?<!-- CATALOG:END -->', '', s, flags=re.S)
    def repl(m):
        return enrich(m.group(0), lang)
    s2, n = re.subn(r'<li class="crs-c live"[^>]*>.*?</li>', repl, s, flags=re.S)
    if n != 30: raise SystemExit(f'{f}: expected 30 live cards, found {n}')
    if '<section id="y1">' not in s2: raise SystemExit(f'no y1 in {f}')
    s2 = s2.replace('<section id="y1">', block(lang) + '<section id="y1">', 1)
    s2 = s2.replace('courses.css?v=20261024h', 'courses.css?v=20261102b').replace('courses.css?v=20261102a', 'courses.css?v=20261102b')
    if s2 != s: open(f, 'w', encoding='utf-8').write(s2)

def apply():
    for lang in LANGS:
        apply_one(lang, 'Courses.html' if lang == 'en' else f'{lang}/Courses.html')
    print('course catalog: 6 hubs')

if __name__ == '__main__':
    apply()
