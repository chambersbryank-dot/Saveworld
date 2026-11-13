#!/usr/bin/env python3
"""Same top nav on every page: the homepage bar.

Nov 2 2026 (Bryan-approved) started this on the homepage. Nov 13: every page
uses that bar. Items, in order: Solutions, Courses, Earth & Space Map,
Teachers, About, then the crystal-water Donate / Help button. The utility row
is the language switch plus Newsletter. The map link still goes to
World_Map.html. Satellite Launch Tracker stays in that menu: the Nov 12 utility
link (build-nav.py UTIL) was dropped when this short bar replaced the utility
row with only the language switch and Newsletter. Do not remove
Upcoming_Launches.html from MENUS. Language links stay pointed at the current
page. Idempotent.
Run after build-nav.py (wired there) so a full nav rebuild does not put the
long dropdown menu back.
"""
import os, re, html, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
E = lambda s: html.escape(s, quote=False)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
LBL = {
 'en': dict(main='Main menu', util='Site links', sol='Solutions', courses='Courses', map='Earth & Space Map', teach='Teachers', about='About', news='Newsletter', donate='Donate / Help'),
 'fr': dict(main='Menu principal', util='Liens du site', sol='Solutions', courses='Cours', map='Carte de la Terre et de l’espace', teach='Enseignants', about='À propos', news='Infolettre', donate='Faire un don / Aider'),
 'es': dict(main='Menú principal', util='Enlaces del sitio', sol='Soluciones', courses='Cursos', map='Mapa de la Tierra y el espacio', teach='Docentes', about='Acerca de', news='Boletín', donate='Donar / Ayudar'),
 'ar': dict(main='القائمة الرئيسية', util='روابط الموقع', sol='الحلول', courses='المقررات', map='خريطة الأرض والفضاء', teach='المعلمون', about='من نحن', news='النشرة', donate='تبرّع / ساعد'),
 'it': dict(main='Menu principale', util='Link del sito', sol='Soluzioni', courses='Corsi', map='Mappa della Terra e dello spazio', teach='Insegnanti', about='Chi siamo', news='Newsletter', donate='Dona / Aiuta'),
 'he': dict(main='תפריט ראשי', util='קישורי האתר', sol='פתרונות', courses='קורסים', map='מפת כדור הארץ והחלל', teach='מורים', about='אודות', news='ניוזלטר', donate='תרומה / עזרה'),
}
# Each menu: the top label links to the first page, and that page is listed first.
# Only pages that exist in the repo. Earth & Space Map includes the satellite map and Voyages.
MENUS = [
 ('sol', [
  ('Solutions.html', 'all'), ('Oceans.html', 'oceans'), ('Rivers.html', 'rivers'),
  ('Earth_Observation.html', 'observe'), ('Space.html', 'space'), ('Topics.html', 'topics'),
 ]),
 ('courses', [
  ('Courses.html', 'courses'), ('Learn.html', 'learn'), ('Orbits_Guide.html', 'orbits'), ('Orbit_Lab.html', 'olab'),
 ]),
 ('map', [
  ('World_Map.html', 'map'), ('Space.html#satmap', 'sats'), ('Voyages.html', 'voyages'),
  ('Upcoming_Launches.html', 'launches'),
 ]),
 ('teach', [
  ('Teachers.html', 'teach'), ('Lesson_Builder.html', 'lessons'), ('GLOBE_Program.html', 'globe'),
 ]),
 ('ab', [
  ('About.html', 'about'), ('Editorial_Policy.html', 'editorial'), ('Privacy.html', 'privacy'),
  ('Contact.html', 'contact'), ('Corrections.html', 'corrections'),
 ]),
]
SUB = {
 'en': dict(all='All Solutions', oceans='Oceans', rivers='Rivers', observe='Earth Observation', space='Space', topics='Topics A to Z',
            learn='Learn', orbits='Orbits guide', olab='Orbit Lab', sats='Satellite map', voyages='Voyages Beyond Earth',
            launches='Satellite Launch Tracker', lessons='Lesson Plan Builder', globe='GLOBE',
            editorial='Editorial Policy', privacy='Privacy', contact='Contact', corrections='Corrections'),
 'fr': dict(all='Toutes les solutions', oceans='Océan', rivers='Rivières', observe='Observation de la Terre', space='Espace', topics='Sujets de A à Z',
            learn='Apprendre', orbits='Guide des orbites', olab='Laboratoire d’orbites', sats='Carte des satellites', voyages='Voyages au-delà de la Terre',
            launches='Suivi des lancements de satellites', lessons='Générateur de plans de cours', globe='GLOBE',
            editorial='Politique éditoriale', privacy='Confidentialité', contact='Contact', corrections='Corrections'),
 'es': dict(all='Todas las soluciones', oceans='Océano', rivers='Ríos', observe='Observación de la Tierra', space='Espacio', topics='Temas de la A a la Z',
            learn='Aprender', orbits='Guía de órbitas', olab='Laboratorio de órbitas', sats='Mapa de satélites', voyages='Viajes más allá de la Tierra',
            launches='Rastreador de lanzamientos de satélites', lessons='Creador de planes de clase', globe='GLOBE',
            editorial='Política editorial', privacy='Privacidad', contact='Contacto', corrections='Correcciones'),
 'ar': dict(all='كل الحلول', oceans='المحيط', rivers='الأنهار', observe='رصد الأرض', space='الفضاء', topics='المواضيع من الألف إلى الياء',
            learn='تعلّم', orbits='دليل المدارات', olab='مختبر المدارات', sats='خريطة الأقمار الصناعية', voyages='رحلات ما وراء الأرض',
            launches='متتبع إطلاق الأقمار الصناعية', lessons='منشئ خطط الدروس', globe='GLOBE',
            editorial='السياسة التحريرية', privacy='الخصوصية', contact='اتصل بنا', corrections='التصحيحات'),
 'it': dict(all='Tutte le soluzioni', oceans='Oceano', rivers='Fiumi', observe='Osservazione della Terra', space='Spazio', topics='Argomenti dalla A alla Z',
            learn='Impara', orbits='Guida alle orbite', olab='Laboratorio di orbite', sats='Mappa dei satelliti', voyages='Viaggi oltre la Terra',
            launches='Tracker dei lanci satellitari', lessons='Generatore di piani di lezione', globe='GLOBE',
            editorial='Politica editoriale', privacy='Privacy', contact='Contatti', corrections='Correzioni'),
 'he': dict(all='כל הפתרונות', oceans='אוקיינוס', rivers='נהרות', observe='תצפית על כדור הארץ', space='חלל', topics='נושאים מא׳ עד ת׳',
            learn='למידה', orbits='מדריך מסלולים', olab='מעבדת מסלולים', sats='מפת הלוויינים', voyages='מסעות מעבר לכדור הארץ',
            launches='מעקב שיגורי לוויינים', lessons='בונה מערכי שיעור', globe='GLOBE',
            editorial='מדיניות המערכת', privacy='פרטיות', contact='יצירת קשר', corrections='תיקונים'),
}

def ul_span(html_s, class_name):
    for m in re.finditer(r'<ul\b[^>]*>', html_s):
        if not re.search(rf'class="[^"]*\b{class_name}\b', m.group(0)): continue
        i, j, depth = m.start(), m.end(), 1
        while j < len(html_s) and depth:
            if html_s.startswith('<ul', j):
                depth += 1; j = html_s.find('>', j) + 1
            elif html_s.startswith('</ul>', j):
                depth -= 1; j += len('</ul>')
            else:
                j += 1
        return i, j
    return None

def replace_ul(html_s, class_name, new_ul):
    span = ul_span(html_s, class_name)
    if not span: raise SystemExit(f'no ul.{class_name}')
    i, j = span
    return html_s[:i] + new_ul + html_s[j:]

def language_switch(lang, page, s):
    sw = re.search(r'<li class="lang-switch">.*?</li>', s, re.S)
    if sw: return sw.group(0)
    src = page if os.path.exists(page) else 'Courses.html'
    en = open(src, encoding='utf-8').read()
    sw = re.search(r'<li class="lang-switch">.*?</li>', en, re.S)
    if not sw: return None
    block = sw.group(0).replace('Courses.html', page) if src != page else sw.group(0)
    block = re.sub(r'href="(?!https?:|\.\./)([^"]+)"', r'href="../\1"', block)
    block = re.sub(r' aria-current="true"', '', block)
    def mark(m):
        tag = re.sub(r'aria-checked="(?:true|false)"', 'aria-checked="false"', m.group(0))
        if f'data-lang="{lang}"' not in tag: return tag
        tag = tag.replace('aria-checked="false"', 'aria-checked="true"', 1)
        if 'aria-current=' not in tag: tag = tag[:-1] + ' aria-current="true">'
        return tag
    return re.sub(r'<a\b[^>]*>', mark, block)

def sub_label(lang, key):
    if key in LBL[lang]: return LBL[lang][key]
    return SUB[lang][key]

def simplify(lang, s, page):
    t = LBL[lang]
    pre = '' if lang == 'en' else '../'
    items = []
    for key, links in MENUS:
        for href, _ in links:
            path = href.split('#')[0]
            folder = '' if lang == 'en' else lang + '/'
            if not os.path.exists(folder + path) and not os.path.exists(path):
                raise SystemExit(f'missing nav page {path}')
        head = links[0][0]
        top = {'ab': 'about'}.get(key, key)
        cur_top = any(href.split('#')[0] == page for href, _ in links)
        lis = []
        for href, lab in links:
            cur = ' aria-current="page"' if href.split('#')[0] == page else ''
            lis.append(f'<li><a href="{pre}{href}"{cur}>{E(sub_label(lang, lab))}</a></li>')
        items.append(
            f'<li class="spn-dd{" is-current" if cur_top else ""}">'
            f'<a class="spn-trig spn-trig-link" href="{pre}{head}" aria-expanded="false" aria-controls="spn-{key}">{E(t[top])}<span class="spn-chev" aria-hidden="true"></span></a>'
            f'<ul class="spn-sub" id="spn-{key}">{"".join(lis)}</ul></li>')
    donate_cur = ' aria-current="page"' if page == 'Ways_to_Help.html' else ''
    main = (f'<ul class="spn-main" aria-label="{E(t["main"])}">{"".join(items)}'
            f'<li class="spn-cta nav-help"><a href="{pre}Ways_to_Help.html#donate"{donate_cur}>{E(t["donate"])}</a></li></ul>')
    s = replace_ul(s, 'spn-main', main)
    sw = language_switch(lang, page, s)
    if not sw: return None
    util = (f'<ul class="spn-util" aria-label="{E(t["util"])}">{sw}'
            f'<li><a href="{pre}index.html#newsletter">{E(t["news"])}</a></li></ul>')
    s = replace_ul(s, 'spn-util', util)
    s = re.sub(r'styles\.css\?v=[^"\']+', 'styles.css?v=20261113z', s)
    s = re.sub(r'site\.js\?v=[^"\']+', 'site.js?v=20261113z', s)
    return s

def donate_anchor(lang):
    f = 'Ways_to_Help.html' if lang == 'en' else f'{lang}/Ways_to_Help.html'
    s = open(f, encoding='utf-8').read()
    if 'id="donate"' in s: return
    if 'class="wth-filters"' not in s: raise SystemExit(f'no donate showcase on {f}')
    s = s.replace('class="wth-filters"', 'id="donate" class="wth-filters"', 1)
    open(f, 'w', encoding='utf-8').write(s)

def pages():
    for lang in LANGS:
        folder = '' if lang == 'en' else lang + '/'
        for f in sorted(glob.glob(folder + '*.html')):
            yield lang, f

def apply():
    n = skip = 0
    for lang, f in pages():
        s = open(f, encoding='utf-8').read()
        if '<nav id="topnav">' not in s or ul_span(s, 'spn-main') is None: continue
        s2 = simplify(lang, s, os.path.basename(f))
        if s2 is None:
            skip += 1; print('skip, no language switch:', f); continue
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2); n += 1
        if os.path.basename(f) == 'Ways_to_Help.html': donate_anchor(lang)
    for lang in LANGS:
        home = 'index.html' if lang == 'en' else f'{lang}/index.html'
        text = open(home, encoding='utf-8').read()
        if 'Upcoming_Launches.html' not in text.split('</nav>', 1)[0]:
            raise SystemExit(f'Satellite Launch Tracker missing from {home} nav')
    print(f'home nav: {n} pages, skipped {skip}, donate anchor on Ways to Help')

if __name__ == '__main__':
    apply()
