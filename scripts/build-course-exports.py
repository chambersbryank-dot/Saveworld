#!/usr/bin/env python3
"""Canvas (IMS Common Cartridge) and Google Classroom exports for every live course.

Nov 2 2026 (Bryan-approved). One .imscc and one Classroom zip per course per language.
The cartridge lists Syllabus, Calendar, Units, Labs, Problem Sets, and Exams and links
to those parts of the live page. Classroom gets a CSV a teacher can upload or paste.
Does not rename course codes, touch the Saturn hero, or add analytics.
"""
import os, re, html, glob, zipfile, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
SITE = 'https://www.savingplanets.com/'
E = lambda s: html.escape(s, quote=True)

T = {
 'en': {'syl': 'Syllabus', 'cal': 'Calendar', 'units': 'Units', 'labs': 'Labs', 'psets': 'Problem Sets', 'exams': 'Exams',
        'intro': 'Free Saving Planets course. No grade and no school credit. Open the live page for the full lesson.',
        'canvas': 'Download for Canvas', 'class': 'Download for Google Classroom',
        'readme': 'Upload the CSV in Google Classroom, or paste each row as a material. The link opens the free lesson on Saving Planets.'},
 'fr': {'syl': 'Programme', 'cal': 'Calendrier', 'units': 'Unités', 'labs': 'Travaux pratiques', 'psets': 'Exercices', 'exams': 'Examens',
        'intro': 'Cours gratuit Saving Planets. Pas de note ni de crédit scolaire. Ouvrez la page pour la leçon complète.',
        'canvas': 'Télécharger pour Canvas', 'class': 'Télécharger pour Google Classroom',
        'readme': 'Importez le CSV dans Google Classroom, ou collez chaque ligne comme un document. Le lien ouvre la leçon gratuite.'},
 'es': {'syl': 'Programa', 'cal': 'Calendario', 'units': 'Unidades', 'labs': 'Laboratorios', 'psets': 'Problemas', 'exams': 'Exámenes',
        'intro': 'Curso gratuito de Saving Planets. Sin nota ni crédito escolar. Abre la página para la lección completa.',
        'canvas': 'Descargar para Canvas', 'class': 'Descargar para Google Classroom',
        'readme': 'Sube el CSV a Google Classroom, o pega cada fila como material. El enlace abre la lección gratis.'},
 'ar': {'syl': 'المنهج', 'cal': 'التقويم', 'units': 'الوحدات', 'labs': 'المختبرات', 'psets': 'مجموعات المسائل', 'exams': 'الامتحانات',
        'intro': 'مقرر مجاني من Saving Planets. بلا درجة وبلا ساعات معتمدة. افتح الصفحة للدرس الكامل.',
        'canvas': 'تنزيل لـ Canvas', 'class': 'تنزيل لـ Google Classroom',
        'readme': 'ارفع ملف CSV إلى Google Classroom، أو الصق كل صف كمادة. الرابط يفتح الدرس المجاني.'},
 'it': {'syl': 'Programma', 'cal': 'Calendario', 'units': 'Unità', 'labs': 'Laboratori', 'psets': 'Esercizi', 'exams': 'Esami',
        'intro': 'Corso gratuito di Saving Planets. Nessun voto e nessun credito scolastico. Apri la pagina per la lezione intera.',
        'canvas': 'Scarica per Canvas', 'class': 'Scarica per Google Classroom',
        'readme': 'Carica il CSV su Google Classroom, oppure incolla ogni riga come materiale. Il link apre la lezione gratuita.'},
 'he': {'syl': 'סילבוס', 'cal': 'לוח שנה', 'units': 'יחידות', 'labs': 'מעבדות', 'psets': 'תרגילים', 'exams': 'מבחנים',
        'intro': 'קורס חינם של Saving Planets. בלי ציון ובלי נקודות זכות. פתחו את העמוד לשיעור המלא.',
        'canvas': 'הורדה ל-Canvas', 'class': 'הורדה ל-Google Classroom',
        'readme': 'העלו את ה-CSV ל-Google Classroom, או הדביקו כל שורה כחומר. הקישור פותח את השיעור החינמי.'},
}

def live():
    mods = {}
    for f in sorted(glob.glob('scripts/courses/*.py')):
        name = os.path.basename(f)[:-3]
        if name in ('roadmap', '__init__'): continue
        spec = importlib.util.spec_from_file_location('ex_' + name, f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if getattr(m, 'STATUS', '') == 'live': mods[m.PAGE] = m
    return mods

def page_url(lang, page, anchor):
    base = SITE + ('' if lang == 'en' else lang + '/') + page
    return base + anchor

def manifest(cid, lang, title, items):
    org = []
    res = []
    for i, (ident, label, href) in enumerate(items, 1):
        org.append(f'<item identifier="I{i}" identifierref="R{i}"><title>{E(label)}</title></item>')
        res.append(f'<resource identifier="R{i}" type="webcontent" href="{href}"><file href="{href}"/></resource>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="SP-{cid}-{lang}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"
 xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource"
 xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest">
 <metadata>
  <schema>IMS Common Cartridge</schema>
  <schemaversion>1.1.0</schemaversion>
  <lomimscc:lom><lomimscc:general><lomimscc:title><lomimscc:string language="{lang}">{E(title)}</lomimscc:string></lomimscc:title></lomimscc:general></lomimscc:lom>
 </metadata>
 <organizations><organization identifier="O1" structure="rooted"><item identifier="ROOT"><title>{E(title)}</title>{''.join(org)}</item></organization></organizations>
 <resources>{''.join(res)}</resources>
</manifest>
'''

def doc(lang, title, intro, body, rtl):
    direction = 'rtl' if rtl else 'ltr'
    return (f'<!DOCTYPE html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8"><title>{E(title)}</title></head>'
            f'<body><h1>{E(title)}</h1><p>{E(intro)}</p>{body}</body></html>')

def build_one(lang, mod, h1):
    t = T[lang]
    rtl = lang in ('ar', 'he')
    units = ''.join(f'<li><a href="{page_url(lang, mod.PAGE, "#" + u["id"])}">{E(u["title"] if lang=="en" else u["title"])}</a></li>' for u in mod.UNITS)
    # unit titles stay English in the module; the live page is translated. Link text uses the English title plus the code, which is stable.
    labs = ''.join(f'<li><a href="{page_url(lang, mod.PAGE, "#" + L["id"])}">{E(L["title"])}</a></li>' for L in mod.LABS)
    items = [
        ('syllabus', t['syl'], 'syllabus.html'),
        ('calendar', t['cal'], 'calendar.html'),
        ('units', t['units'], 'units.html'),
        ('labs', t['labs'], 'labs.html'),
        ('psets', t['psets'], 'problem-sets.html'),
        ('exams', t['exams'], 'exams.html'),
    ]
    files = {
        'syllabus.html': doc(lang, t['syl'], t['intro'], f'<p>{E(mod.CODE)}</p><p><a href="{page_url(lang, mod.PAGE, "#syllabus")}">{E(h1)}</a></p>', rtl),
        'calendar.html': doc(lang, t['cal'], t['intro'], f'<p><a href="{page_url(lang, mod.PAGE, "#schedule")}">{E(t["cal"])}</a></p>', rtl),
        'units.html': doc(lang, t['units'], t['intro'], f'<ol>{units}</ol>', rtl),
        'labs.html': doc(lang, t['labs'], t['intro'], f'<ol>{labs}</ol>', rtl),
        'problem-sets.html': doc(lang, t['psets'], t['intro'], f'<p><a href="{page_url(lang, mod.PAGE, "#problem-sets")}">{E(t["psets"])}</a></p>', rtl),
        'exams.html': doc(lang, t['exams'], t['intro'], f'<p><a href="{page_url(lang, mod.PAGE, "#exam")}">{E(t["exams"])}</a></p>', rtl),
    }
    folder = os.path.join('exports', lang)
    os.makedirs(folder, exist_ok=True)
    stem = mod.PAGE[:-5]
    imscc = os.path.join(folder, stem + '.imscc')
    classroom = os.path.join(folder, stem + '-classroom.zip')
    with zipfile.ZipFile(imscc, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('imsmanifest.xml', manifest(mod.ID, lang, h1, items))
        for name, data in files.items():
            z.writestr(name, data)
    rows = ['topic,title,description,link']
    for ident, label, href in items:
        url = page_url(lang, mod.PAGE, {'syllabus.html': '#syllabus', 'calendar.html': '#schedule', 'units.html': '#units', 'labs.html': '#lab', 'problem-sets.html': '#problem-sets', 'exams.html': '#exam'}[href])
        rows.append(','.join(csv(x) for x in (label, label, t['intro'], url)))
    with zipfile.ZipFile(classroom, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('materials.csv', '\n'.join(rows) + '\n')
        z.writestr('README.html', doc(lang, t['class'], t['readme'], '', rtl))
    return imscc, classroom

def csv(s):
    s = s.replace('"', '""')
    return f'"{s}"'

def h1_of(lang, page):
    p = page if lang == 'en' else f'{lang}/{page}'
    if not os.path.exists(p): return page
    m = re.search(r'<h1>(.*?)</h1>', open(p, encoding='utf-8').read())
    return html.unescape(re.sub('<[^>]+>', '', m.group(1))) if m else page

def splice(lang, mod, imscc, classroom):
    p = mod.PAGE if lang == 'en' else f'{lang}/{mod.PAGE}'
    if not os.path.exists(p): return
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- EXPORTS:START -->.*?<!-- EXPORTS:END -->', '', s, flags=re.S)
    pre = '' if lang == 'en' else '../'
    t = T[lang]
    blk = (f'<!-- EXPORTS:START --><p class="crs-tools"><a class="crs-btn" href="{pre}{imscc}">{E(t["canvas"])}</a> '
           f'<a class="crs-btn" href="{pre}{classroom}">{E(t["class"])}</a></p><!-- EXPORTS:END -->')
    if '<!-- INSTRUCT:END -->' in s:
        s = s.replace('<!-- INSTRUCT:END -->', '<!-- INSTRUCT:END -->' + blk, 1)
    else:
        s = s.replace('<section id="start">', blk + '<section id="start">', 1)
    open(p, 'w', encoding='utf-8').write(s)

def apply(link_pages=True):
    n = 0
    for page, mod in live().items():
        for lang in LANGS:
            if not os.path.exists(page if lang == 'en' else f'{lang}/{page}'): continue
            imscc, classroom = build_one(lang, mod, h1_of(lang, page))
            if link_pages: splice(lang, mod, imscc, classroom)
            n += 1
    print(f'course exports: {n} language copies')

if __name__ == '__main__':
    apply()
