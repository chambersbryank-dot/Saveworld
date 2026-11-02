#!/usr/bin/env python3
"""Homepage nav only: 5 links, a newsletter signup jump, and a Donate button.

Nov 2 2026 (Bryan-approved). Other pages keep the full menu. Donate goes to
Ways_to_Help.html#donate (the existing donate showcase). Newsletter jumps to the
signup already on the homepage (#newsletter). Language switch stays so all 6
languages remain reachable. Does not touch the Saturn hero. Idempotent.
Run after build-nav.py (wired there) so a full nav rebuild does not put the
long menu back on the homepage.
"""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
E = lambda s: html.escape(s, quote=False)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
LBL = {
 'en': dict(main='Main menu', util='Site links', sol='Solutions', courses='Courses', map='World Map', teach='Teachers', about='About', news='Newsletter', donate='Donate'),
 'fr': dict(main='Menu principal', util='Liens du site', sol='Solutions', courses='Cours', map='Carte du monde', teach='Enseignants', about='À propos', news='Infolettre', donate='Faire un don'),
 'es': dict(main='Menú principal', util='Enlaces del sitio', sol='Soluciones', courses='Cursos', map='Mapa del mundo', teach='Docentes', about='Acerca de', news='Boletín', donate='Donar'),
 'ar': dict(main='القائمة الرئيسية', util='روابط الموقع', sol='الحلول', courses='المقررات', map='خريطة العالم', teach='المعلمون', about='من نحن', news='النشرة', donate='تبرع'),
 'it': dict(main='Menu principale', util='Link del sito', sol='Soluzioni', courses='Corsi', map='Mappa del mondo', teach='Insegnanti', about='Chi siamo', news='Newsletter', donate='Dona'),
 'he': dict(main='תפריט ראשי', util='קישורי האתר', sol='פתרונות', courses='קורסים', map='מפת העולם', teach='מורים', about='אודות', news='ניוזלטר', donate='תרומה'),
}
LINKS = [('Solutions.html', 'sol'), ('Courses.html', 'courses'), ('World_Map.html', 'map'), ('Teachers.html', 'teach'), ('About.html', 'about')]

def replace_ul(html_s, class_name, new_ul):
    m = re.search(rf'<ul class="{class_name}"[^>]*>', html_s)
    if not m: raise SystemExit(f'no ul.{class_name}')
    i, j, depth = m.start(), m.end(), 1
    while j < len(html_s) and depth:
        if html_s.startswith('<ul', j):
            depth += 1; j = html_s.find('>', j) + 1
        elif html_s.startswith('</ul>', j):
            depth -= 1; j += len('</ul>')
        else:
            j += 1
    return html_s[:i] + new_ul + html_s[j:]

def simplify(lang, s):
    t = LBL[lang]
    pre = '' if lang == 'en' else '../'
    items = ''.join(f'<li><a class="spn-trig spn-trig-link" href="{pre}{href}">{E(t[key])}</a></li>' for href, key in LINKS)
    main = (f'<ul class="spn-main" aria-label="{E(t["main"])}">{items}'
            f'<li class="spn-cta nav-help"><a href="{pre}Ways_to_Help.html#donate">{E(t["donate"])}</a></li></ul>')
    s = replace_ul(s, 'spn-main', main)
    sw = re.search(r'<li class="lang-switch">.*?</li>', s, re.S)
    if not sw: raise SystemExit(f'no language switch on {lang} home')
    util = (f'<ul class="spn-util" aria-label="{E(t["util"])}">{sw.group(0)}'
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

def apply():
    for lang in LANGS:
        f = 'index.html' if lang == 'en' else f'{lang}/index.html'
        s = open(f, encoding='utf-8').read()
        s2 = simplify(lang, s)
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2)
        donate_anchor(lang)
    print('home nav: 6 homepages, donate anchor on Ways to Help')

if __name__ == '__main__':
    apply()
