#!/usr/bin/env python3
"""Nov 20 2026: where the free materials are officially published.

Two verified listings only (do not add platforms here):
  TES member page, 32 free resources, Nov 16 2026
  OER Commons, Introduction to Aerospace Engineering (AERO 101), Nov 19 2026

Writes, in all six languages:
  index.html                         <!-- PUBLISHED --> crystal-water strip (existing .hv-chip)
  About.html                         <!-- MILESTONES --> dated list, one li per entry
  Intro_to_Aerospace_Engineering.html <!-- OERPUB --> small link in the license line

Idempotent. Run from the repo root. i18n-build ignores PUBLISHED and MILESTONES, so this
script fills those blocks in each language after translation. The AERO 101 sentence also
lives in i18n/courses/aero101.json for scripts/build-courses.py.
"""
import json, os, re, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
TES = 'https://www.tes.com/member/savingplanets'
OER = 'https://oercommons.org/courses/introduction-to-aerospace-engineering-aero-101'

def bdi(name):
    return f'<bdi>{name}</bdi>'

# Platform names and the course code stay untranslated. Teacher Sheets uses each
# language's existing name for that page. The figure 32 is the verified count.
HOME = {
 'en': {'h': 'Our free materials are published on',
        'tes': f'{bdi("TES")} — 32 free Teacher Sheets and handouts',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: Introduction to Aerospace Engineering'},
 'fr': {'h': 'Nos ressources gratuites sont publiées sur',
        'tes': f'{bdi("TES")} — 32 fiches enseignants et documents à distribuer gratuits',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: Introduction à l’ingénierie aérospatiale'},
 'es': {'h': 'Nuestros materiales gratuitos están publicados en',
        'tes': f'{bdi("TES")} — 32 fichas docentes y materiales de apoyo gratuitos',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: Introducción a la ingeniería aeroespacial'},
 'it': {'h': 'I nostri materiali gratuiti sono pubblicati su',
        'tes': f'{bdi("TES")} — 32 schede per insegnanti e dispense gratuite',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: Introduzione all’ingegneria aerospaziale'},
 'ar': {'h': 'موادنا المجانية منشورة على',
        'tes': f'{bdi("TES")} — {bdi("32")} من أوراق المعلمين والنشرات المجانية',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: مقدمة في هندسة الطيران والفضاء'},
 'he': {'h': 'החומרים החינמיים שלנו מתפרסמים באתרים אלה',
        'tes': f'{bdi("TES")} — {bdi("32")} דפי מורים ודפי חלוקה חינמיים',
        'oer': f'{bdi("OER Commons")} — {bdi("AERO 101")}: מבוא להנדסת אווירונאוטיקה וחלל'},
}
# Whole clause is the link so the accessible name says what was published and where.
MS = {
 'en': {'h': 'Milestones', 'items': [
     ('2026-11-16', 'Nov 16, 2026', TES, f'32 free Teacher Sheets and handouts published on {bdi("TES")}'),
     ('2026-11-19', 'Nov 19, 2026', OER, f'Introduction to Aerospace Engineering ({bdi("AERO 101")}) published on {bdi("OER Commons")}')]},
 'fr': {'h': 'Jalons', 'items': [
     ('2026-11-16', '16 nov. 2026', TES, f'32 fiches enseignants et documents à distribuer gratuits publiés sur {bdi("TES")}'),
     ('2026-11-19', '19 nov. 2026', OER, f'Introduction à l’ingénierie aérospatiale ({bdi("AERO 101")}) publiée sur {bdi("OER Commons")}')]},
 'es': {'h': 'Hitos', 'items': [
     ('2026-11-16', '16 nov. 2026', TES, f'32 fichas docentes y materiales de apoyo gratuitos publicados en {bdi("TES")}'),
     ('2026-11-19', '19 nov. 2026', OER, f'Introducción a la ingeniería aeroespacial ({bdi("AERO 101")}) publicada en {bdi("OER Commons")}')]},
 'it': {'h': 'Tappe', 'items': [
     ('2026-11-16', '16 nov. 2026', TES, f'32 schede per insegnanti e dispense gratuite pubblicate su {bdi("TES")}'),
     ('2026-11-19', '19 nov. 2026', OER, f'Introduzione all’ingegneria aerospaziale ({bdi("AERO 101")}) pubblicata su {bdi("OER Commons")}')]},
 'ar': {'h': 'معالم', 'items': [
     ('2026-11-16', f'{bdi("16")} نوفمبر {bdi("2026")}', TES, f'نُشرت {bdi("32")} من أوراق المعلمين والنشرات المجانية على {bdi("TES")}'),
     ('2026-11-19', f'{bdi("19")} نوفمبر {bdi("2026")}', OER, f'نُشرت مقدمة في هندسة الطيران والفضاء ({bdi("AERO 101")}) على {bdi("OER Commons")}')]},
 'he': {'h': 'אבני דרך', 'items': [
     ('2026-11-16', f'{bdi("16")} בנובמבר {bdi("2026")}', TES, f'{bdi("32")} דפי מורים ודפי חלוקה חינמיים פורסמו ב-{bdi("TES")}'),
     ('2026-11-19', f'{bdi("19")} בנובמבר {bdi("2026")}', OER, f'מבוא להנדסת אווירונאוטיקה וחלל ({bdi("AERO 101")}) פורסם ב-{bdi("OER Commons")}')]},
}
# Must match i18n/courses/aero101.json (build-courses.py translates this sentence).
OER_LINE = {
 'en': 'Also published on OER Commons',
 'fr': 'Également publié sur OER Commons',
 'es': 'También publicado en OER Commons',
 'it': 'Pubblicato anche su OER Commons',
 'ar': 'منشور أيضًا على OER Commons',
 'he': 'פורסם גם ב-OER Commons',
}

def chip(href, inner):
    # One span: .hv-chip is inline-flex, so bare <bdi> children become separate items and wrap apart.
    return f'<a class="hv-chip" href="{href}" target="_blank" rel="noopener"><span>{inner}</span></a>'

def home_block(lang):
    t = HOME[lang]
    # Wrap only. Color, glass, and focus come from the existing .hv-chip rule on this page.
    css = ('<style>#published .hv-chip{max-width:100%;min-width:0}'
           '#published .hv-chip span{display:block;min-width:0;max-width:100%;white-space:normal;text-align:center;line-height:1.35}</style>')
    return ('<!-- PUBLISHED:START -->' + css
            + '<section class="home-vision" id="published" aria-labelledby="pub-h">'
            + f'<h2 id="pub-h">{t["h"]}</h2><p class="hv-chips">{chip(TES, t["tes"])}{chip(OER, t["oer"])}</p>'
            + '</section><!-- PUBLISHED:END -->')

def ms_block(lang):
    t = MS[lang]
    # Link blue already used on dark cards (#8fd3ff). Cards are the shared .w-card.
    css = ('<style>.ms-tl{list-style:none;margin:0;padding:0}'
           '.ms-tl a{color:#8fd3ff;font-weight:700;text-decoration:underline;text-underline-offset:2px}'
           '.ms-tl a:focus-visible{outline:3px solid #ffd54a;outline-offset:3px}</style>')
    items = ''.join(
        f'<li class="w-card"><p><time datetime="{iso}">{date}</time> — <a href="{href}" target="_blank" rel="noopener">{body}</a></p></li>'
        for iso, date, href, body in t['items'])
    return ('<!-- MILESTONES:START -->' + css
            + '<section class="five-ws" id="milestones" aria-labelledby="ms-h">'
            + f'<h2 id="ms-h">{t["h"]}</h2>'
            + '<!-- Add the next milestone as another li.w-card, oldest first. -->'
            + f'<ol class="ws-grid ms-tl">{items}</ol></section><!-- MILESTONES:END -->')

def oer_block(lang):
    # A small link in the license line. The platform name stays in Latin.
    return ('<!-- OERPUB:START --><a class="crs-oer" href="' + OER
            + '" target="_blank" rel="noopener">' + bdi('OER Commons') + '</a><!-- OERPUB:END -->')

def put(path, rx, block, anchor):
    s = open(path, encoding='utf-8').read()
    o = s
    if rx.search(s):
        s = rx.sub(lambda m: block, s, count=1)
    else:
        if anchor not in s:
            raise SystemExit(f'{path}: missing anchor {anchor!r}')
        s = s.replace(anchor, block + anchor, 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
    return s != o

def check_json():
    p = 'i18n/courses/aero101.json'
    d = json.load(open(p, encoding='utf-8'))
    key = OER_LINE['en']
    got = d.get(key)
    if not got:
        raise SystemExit(f'{p}: missing {key!r} (build-courses would drop translated AERO 101 pages)')
    for lang in LANGS[1:]:
        if got.get(lang) != OER_LINE[lang]:
            raise SystemExit(f'{p}: {lang} is {got.get(lang)!r}, expected {OER_LINE[lang]!r}')

def main():
    check_json()
    n = 0
    hr = re.compile(r'<!-- PUBLISHED:START -->.*?<!-- PUBLISHED:END -->', re.S)
    mr = re.compile(r'<!-- MILESTONES:START -->.*?<!-- MILESTONES:END -->', re.S)
    cr = re.compile(r'<!-- OERPUB:START -->.*?<!-- OERPUB:END -->', re.S)
    for lang in LANGS:
        pre = '' if lang == 'en' else lang + '/'
        n += put(pre + 'index.html', hr, home_block(lang), '<!-- HOMENUM:START -->')
        n += put(pre + 'About.html', mr, ms_block(lang), '<!-- SOURCES:START -->')
        n += put(pre + 'Intro_to_Aerospace_Engineering.html', cr, oer_block(lang), '</p><!-- LICENSE:END -->')
    print(f'build-published: {n} file(s) updated')

if __name__ == '__main__':
    sys.exit(main())
