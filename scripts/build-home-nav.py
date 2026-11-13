#!/usr/bin/env python3
"""Same top nav on every page: the homepage bar.

Nov 2 2026 (Bryan-approved) started this on the homepage. Nov 13: every page
uses that bar. Items, in order: Solutions, Courses, Earth & Space Map,
Teachers, About, then the crystal-water Donate / Help button. The utility row
is the language switch plus Newsletter. The map link still goes to
World_Map.html. Language links stay pointed at the current page. Idempotent.
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
LINKS = [('Solutions.html', 'sol'), ('Courses.html', 'courses'), ('World_Map.html', 'map'), ('Teachers.html', 'teach'), ('About.html', 'about')]

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

def simplify(lang, s, page):
    t = LBL[lang]
    pre = '' if lang == 'en' else '../'
    def item(href, key):
        cur = ' aria-current="page"' if page == href else ''
        return f'<li><a class="spn-trig spn-trig-link" href="{pre}{href}"{cur}>{E(t[key])}</a></li>'
    items = ''.join(item(href, key) for href, key in LINKS)
    donate_cur = ' aria-current="page"' if page == 'Ways_to_Help.html' else ''
    main = (f'<ul class="spn-main" aria-label="{E(t["main"])}">{items}'
            f'<li class="spn-cta nav-help"><a href="{pre}Ways_to_Help.html#donate"{donate_cur}>{E(t["donate"])}</a></li></ul>')
    s = replace_ul(s, 'spn-main', main)
    sw = language_switch(lang, page, s)
    if not sw: return None
    util = (f'<ul class="spn-util" aria-label="{E(t["util"])}">{sw}'
            f'<li><a href="{pre}index.html#newsletter">{E(t["news"])}</a></li></ul>')
    s = replace_ul(s, 'spn-util', util)
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
    print(f'home nav: {n} pages, skipped {skip}, donate anchor on Ways to Help')

if __name__ == '__main__':
    apply()
