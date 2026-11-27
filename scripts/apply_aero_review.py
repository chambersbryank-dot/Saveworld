#!/usr/bin/env python3
"""Splice the authorship, review, alignment and study-guide link into the live pages.
Does not rebuild the course pages."""
import json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, 'scripts')
from courses import aero101_review as AR
import study_hub
import importlib.util
spec = importlib.util.spec_from_file_location('tc', 'scripts/trust-content.py')
TC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(TC)
spec = importlib.util.spec_from_file_location('bc', 'scripts/build-courses.py')
BC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BC)

HE = {
 'sub': 'איך אנחנו בוחרים פתרונות וקורסים, בודקים עובדות ומשתמשים ב-SI.',
 'date': 'עודכן לאחרונה: 27 בנובמבר 2026',
 'rev': 'כל עמוד קורס מציג תאריך «נבדק לאחרונה», שנקבע כשהמייסדים מאשרים את העמוד.',
 'h': 'קורסים',
 'body': 'עמוד קורס הוא לימוד עצמי חינמי. הוא אינו קורס אוניברסיטאי, אינו מעניק נקודות זכות אקדמיות, אף מוסד לימודים אינו מעורב בו, ואף ארגון המוזכר בעמוד אינו ממליץ עליו. המייסד והמייסדת השותפה קובעים את הכיוון, בוחרים את הנושאים ואת ההיקף, בודקים את גישת ההוראה ומאשרים כל דף. SI חוקר, מנסח, מתרגם ובודק מקורות. עובדות, דוגמאות פתורות וקישורים נבדקים מול המקורות הנקובים בעמוד. בדיקה היא מספר או תוצאת קוד בעמוד קורס שסקריפט מחשב מחדש לפני הפרסום. המספר המודפס והמספר שחושב מחדש חייבים להתאים. כל עמוד קורס מציין את המייסד ואת המייסדת השותפה, מקשר למדיניות הזו, ומציג תאריך של בדיקה אחרונה.',
}
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
IDX = {'en': 0, 'fr': 1, 'es': 2, 'ar': 3, 'it': 4}

def pol(lang):
    if lang == 'he':
        return HE
    i = IDX[lang]
    page = TC.PAGES['Editorial_Policy']
    sub = page['sub'][i]
    date = TC.UPDATED[i]
    rev = page['sections'][2][1][1][i]  # second paragraph of Reviews
    course = page['sections'][3]
    return {'sub': sub, 'date': date, 'rev': rev, 'h': course[0][i], 'body': course[1][0][i]}

def course_pages():
    for lang in LANGS:
        rel = 'Intro_to_Aerospace_Engineering.html' if lang == 'en' else f'{lang}/Intro_to_Aerospace_Engineering.html'
        t = open(rel, encoding='utf8').read()
        if 'id="aero101-lock"' not in t:
            raise SystemExit('no lock ' + rel)
        if '.crs-review{' not in t[t.find('id="aero101-lock"'):t.find('</style>', t.find('id="aero101-lock"'))]:
            j = t.find('</style>', t.find('id="aero101-lock"'))
            t = t[:j] + AR.CSS + t[j:]
        if 'id="authorship"' not in t:
            needle = '</p><!-- OCW:START -->'
            if t.count(needle) != 1:
                raise SystemExit('glance ' + rel)
            t = t.replace(needle, '</p>' + AR.box(lang, quality=True) + '<!-- OCW:START -->', 1)
        if 'class="crs-std"' not in t:
            i = t.find('id="outcomes"')
            j = t.find('</section>', i)
            if i < 0 or j < 0:
                raise SystemExit('outcomes ' + rel)
            t = t[:j] + AR.alignment(lang) + t[j:]
        if '.docx' not in t:
            marker = 'Study_Guide'
            i = t.find(marker)
            j = t.find('</a>', i)
            if i < 0 or j < 0:
                raise SystemExit('pdf ' + rel)
            t = t[:j + 4] + AR.guide_link(lang) + t[j + 4:]
        policy = BC.AERO_POLICY[lang]
        if policy not in t:
            raise SystemExit('policy missing ' + rel)
        if AR.T[lang]['disclose'] not in t and 'crs-disclose' not in t:
            # The disclosure is escaped in disclose(); the page stores the escaped form.
            disc = AR.disclose(lang)
            if disc in t:
                pass
            else:
                i = t.find(policy)
                start = t.rfind('<p class="lic-foot">', 0, i)
                if start < 0:
                    raise SystemExit('lic ' + rel)
                t = t[:start] + '<p class="lic-foot">' + disc + ' ' + t[i:]
        open(rel, 'w', encoding='utf8').write(t)
        print('course', lang)

def hub_pages():
    css = study_hub.CSS
    for lang in LANGS:
        rel = 'Undergraduate_Studies.html' if lang == 'en' else f'{lang}/Undergraduate_Studies.html'
        t = open(rel, encoding='utf8').read()
        t2, n = re.subn(r'(<style id="study-tracks-css">).*?(</style>)',
                        lambda m: m.group(1) + css + m.group(2), t, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('css ' + rel)
        t = t2
        if 'id="authorship"' not in t:
            needle = '<section class="crs-degree" id="bs-aero"'
            if t.count(needle) != 1:
                raise SystemExit('degree ' + rel)
            t = t.replace(needle, AR.box(lang, disclosure=True) + needle, 1)
        if 'id="path-goals"' not in t:
            i = t.find('id="track-prompt"')
            j = t.find('</p>', i)
            if i < 0 or j < 0:
                raise SystemExit('prompt ' + rel)
            t = t[:j + 4] + AR.use_block(lang) + t[j + 4:]
        open(rel, 'w', encoding='utf8').write(t)
        print('hub', lang)

def editorial():
    keys = {lang: [] for lang in ('fr', 'es', 'ar', 'it', 'he')}
    en = pol('en')
    for lang in LANGS:
        p = pol(lang)
        rel = 'Editorial_Policy.html' if lang == 'en' else f'{lang}/Editorial_Policy.html'
        t = open(rel, encoding='utf8').read()
        t2, n = re.subn(r'<p class="trust-updated">.*?</p>', '<p class="trust-updated">' + p['date'] + '</p>', t, count=1)
        if n != 1:
            raise SystemExit('date ' + rel)
        t = t2
        # Subtitle sits in the hero and may also be the meta description.
        old = re.search(r'<section class="page-hero[\s\S]*?<p>(.*?)</p>', t)
        if not old:
            raise SystemExit('sub ' + rel)
        old_sub = old.group(1)
        if old_sub != p['sub']:
            c = t.count(old_sub)
            if c < 1:
                raise SystemExit('sub count ' + rel)
            t = t.replace(old_sub, p['sub'])
        if 'id="courses"' not in t:
            i = t.find('id="s3"')
            j = t.find('</section>', i)
            if i < 0 or j < 0:
                raise SystemExit('s3 ' + rel)
            extra = '<p>' + p['rev'] + '</p>'
            block = f'<section class="five-ws" id="courses"><h2>{p["h"]}</h2><p>{p["body"]}</p></section>'
            t = t[:j] + extra + t[j:j + 10] + block + t[j + 10:]
        open(rel, 'w', encoding='utf8').write(t)
        print('policy', lang, 'courses', t.count('id="courses"'))
        if lang != 'en':
            keys[lang] = [(en['sub'], p['sub']), (en['rev'], p['rev']), (en['h'], p['h']), (en['body'], p['body']), (en['date'], p['date'])]

    for lang, pairs in keys.items():
        path = f'i18n/{lang}.json'
        raw = open(path, encoding='utf8').read()
        data = json.loads(raw)
        new = [(k, v) for k, v in pairs if k not in data]
        if not new:
            print('i18n', lang, 'present')
            continue
        text = raw.rstrip()
        if text.endswith('\n'):
            text = text[:-1]
        if not text.endswith('}'):
            raise SystemExit('json ' + path)
        text = text[:-1].rstrip()
        if not text.endswith(','):
            text += ','
        extra = ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in new)
        open(path, 'w', encoding='utf8').write(text + '\n' + extra + '\n}\n')
        print('i18n', lang, len(new))

def stylesheet():
    c = open('assets/courses.css', encoding='utf8').read()
    i = c.index('/* STUDY-TRACKS */')
    open('assets/courses.css', 'w', encoding='utf8').write(c[:i] + study_hub.CSS)
    print('courses.css', study_hub.CSS.count('.crs-review{'))

if __name__ == '__main__':
    course_pages()
    hub_pages()
    editorial()
    stylesheet()
