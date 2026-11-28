# -*- coding: utf-8 -*-
"""Build AERO 101 quiz JSON from the facts already printed on each unit page.

Nothing here is a new number. Worked examples, practice answers, myths,
concepts and the four existing questions are copied out of the six language
pages. Run from the repo root:

    python3 scripts/courses/build_aero_check.py
"""
import html
import os
import re
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from courses import aero101_bank as B

ROOT = B.ROOT
LANGS = B.LANGS
OUT = os.path.join(ROOT, 'assets', 'courses', 'aero101')

# (kind, index, value, tolerance, unit). kind is w (worked) or p (practice).
# The value is the number the page already prints.
NUM = {
    'u1': [('w', 0, 10791, 50, 'N'), ('w', 2, 3, 0.05, 'm/s'),
           ('p', 0, 686700, 500, 'N'), ('p', 1, 30, 0.5, 'kN')],
    'u2': [('w', 2, 0.78, 0.02, ''), ('p', 0, 0.366, 0.015, 'kg/m³'),
           ('p', 1, 5.3, 0.2, '°C'), ('p', 2, 680, 5, 'm/s'),
           ('p', 3, 1.227, 0.015, 'kg/m³')],
    'u3': [('w', 0, 0.36, 0.02, ''), ('w', 1, 26.1, 0.4, 'm/s'),
           ('w', 2, 5.7, 0.2, 'million'), ('p', 1, 9680, 80, 'Pa'),
           ('p', 2, 962, 20, 'N'), ('p', 3, 7.6, 0.4, '%')],
    'u4': [('w', 0, 0.548, 0.02, ''), ('p', 0, 7.5, 0.15, ''),
           ('p', 1, 4.6, 0.2, '°'), ('p', 2, 0.0319, 0.001, ''),
           ('p', 3, 19.4, 0.4, '')],
    'u5': [('w', 0, 20, 0.5, 'km'), ('w', 1, 5235, 60, 'km'),
           ('w', 2, 52.6, 1, 'kW'), ('p', 0, 10, 0.2, 'm'),
           ('p', 1, 2.8, 0.2, 'm/s'), ('p', 2, 6159, 50, 'km'),
           ('p', 3, 20.6, 0.4, 'km')],
    'u6': [('w', 0, 0.15, 0.02, ''), ('w', 1, 11.25, 0.05, 'cm'),
           ('w', 2, 0.22, 0.02, ''), ('p', 2, 15, 0.2, 'g')],
    'u7': [('w', 0, 35, 0.5, 'kN'), ('w', 2, 4079, 40, 's'),
           ('p', 0, 20, 0.3, 'kN')],
    'u8': [('w', 0, 7102, 50, 'm/s'), ('w', 2, 8157, 50, 'm/s'),
           ('p', 0, 3351, 30, 'm/s'), ('p', 1, 1.53, 0.04, ''),
           ('p', 2, 441, 5, 's')],
    'u9': [('w', 0, 7.67, 0.05, 'km/s'), ('w', 1, 42164, 80, 'km'),
           ('w', 2, 3.90, 0.05, 'km/s'), ('p', 0, 7546, 30, 'm/s')],
    'u10': [('w', 0, 3.16, 0.03, ''), ('w', 1, 1959, 30, 'million t'),
            ('p', 0, 15800, 150, 'kg')],
}

UNIT_WORD = B.S('million', 'million', 'millón', 'مليون', 'milione', 'מיליון')
HINT = B.S(
    ' Give your answer in {u}.',
    ' Donnez la réponse en {u}.',
    ' Da la respuesta en {u}.',
    ' أعطِ الإجابة بـ{u}.',
    ' Dai la risposta in {u}.',
    ' כתבו את התשובה ב-{u}.')
WHY_TRUE = B.S(
    'This is stated in the unit.',
    'C’est écrit dans l’unité.',
    'Esto está escrito en la unidad.',
    'هذا مذكور في الوحدة.',
    'È scritto nell’unità.',
    'זה כתוב ביחידה.')
OBJ_Q = B.S(
    'This unit asks you to: {x}',
    'Cette unité vous demande de : {x}',
    'Esta unidad te pide: {x}',
    'تطلب منك هذه الوحدة: {x}',
    'Questa unità ti chiede di: {x}',
    'היחידה הזו מבקשת מכם: {x}')


def txt(fragment):
    fragment = re.sub(r'<[^>]+>', '', fragment)
    return html.unescape(re.sub(r'\s+', ' ', fragment)).strip()


def end(s, start, op, cl):
    i = start + len(op)
    depth = 1
    while depth:
        a = s.find(op, i)
        b = s.find(cl, i)
        if a != -1 and a < b:
            depth += 1
            i = a + len(op)
        else:
            depth -= 1
            i = b + len(cl)
    return i


def unit_html(page, n):
    a = page.find(f'<section class="crs-unit" id="u{n}"')
    b = page.find('<section class="crs-unit"', a + 10)
    if b < 0:
        b = page.find('<section id="psets"', a)
    return page[a:b]


def after_strong(fragment):
    if '</strong>' in fragment:
        return txt(fragment.split('</strong>', 1)[1])
    return txt(fragment)


def lis(block):
    out = []
    i = 0
    while True:
        a = block.find('<li>', i)
        if a < 0:
            break
        b = block.find('</li>', a)
        out.append(block[a:b])
        i = b + 5
    return out


def paras(block):
    return [txt(p) for p in re.findall(r'<p>(.*?)</p>', block, re.S)]


def strip_label(text):
    return re.sub(r'^[^:]{1,24}:\s*', '', text, count=1)


def cloze(text):
    if ':' in text:
        left, right = text.split(':', 1)
        if len(left.strip()) > 8 and len(right.strip()) > 8:
            return left.strip(), right.strip()
    m = re.search(r'-?\d[\d\s.,]*', text)
    if m and len(m.group(0).strip(' .,') ) >= 2:
        front = (text[:m.start()] + '____' + text[m.end():]).strip()
        if front and front != text:
            return front, text
    return None


def unit_name(unit):
    return 'million' if False else unit


def display_unit(lang, unit):
    if unit == 'million':
        return UNIT_WORD[lang]
    if unit == 'million t':
        return UNIT_WORD[lang] + ' t'
    return unit


def pack_q(lang, kind, topic, q, why, src, name, **extra):
    row = {
        'type': kind, 'topic': topic[lang], 'q': q, 'why': why,
        'src': src, 'srcName': name[lang],
    }
    row.update(extra)
    return row


def build_unit(pages, n):
    uid = f'u{n}'
    topic, src, name = B.OLD[uid][0]
    chunks = {lang: unit_html(pages[lang], n) for lang in LANGS}
    en = chunks['en']

    # Existing multiple choice, same order in every language.
    quiz_mc = {lang: [] for lang in LANGS}
    for lang in LANGS:
        form = re.search(r'<form class="crs-quiz" data-quiz="%s".*?</form>' % uid, chunks[lang], re.S).group(0)
        fields = re.findall(r'<fieldset data-ok="(\d+)">(.*?)</fieldset>', form, re.S)
        for i, (ok, body) in enumerate(fields):
            legend = re.search(r'<legend>(.*?)</legend>', body, re.S).group(1)
            q = re.sub(r'^\d+\.\s*', '', txt(legend))
            opts = [txt(x) for x in re.findall(r'</input>|>\s*([^<]+)</label>', body)]
            # labels are `<input ...> text</label>`
            opts = [txt(x) for x in re.findall(r'<label>(.*?)</label>', body, re.S)]
            opts = [re.sub(r'^.*?>', '', html.unescape(re.sub(r'<input[^>]*>', '', x))).strip() for x in re.findall(r'<label>(.*?)</label>', body, re.S)]
            opts = [txt(re.sub(r'<input[^>]*>', '', x)) for x in re.findall(r'<label>(.*?)</label>', body, re.S)]
            why = txt(re.search(r'class="crs-why"[^>]*>(.*?)</p>', body, re.S).group(1))
            t, s, nm = B.OLD[uid][i]
            quiz_mc[lang].append(pack_q(lang, 'mc', t, q, why, s, nm, opts=opts, ok=int(ok)))

    worked = {}
    practice = {}
    myths = {}
    concepts = {}
    cards_old = {}
    jets = {}
    planet = {}
    for lang in LANGS:
        c = chunks[lang]
        w = []
        for block in re.findall(r'<div class="crs-card crs-worked">(.*?)</div>', c, re.S):
            q = after_strong(re.search(r'class="crs-q">(.*?)</p>', block, re.S).group(1))
            a = after_strong(re.search(r'class="crs-ans">(.*?)</p>', block, re.S).group(1))
            w.append((q, a))
        worked[lang] = w
        p = []
        prac = c[c.find('class="crs-prac"'):]
        prac = prac[:prac.find('</ol>')]
        for li in lis(prac):
            ps = paras(li)
            if len(ps) >= 2:
                p.append((ps[0], ps[1]))
        practice[lang] = p
        m = []
        for li in lis(c[c.find('class="crs-mis"'):c.find('</ul>', c.find('class="crs-mis"'))]):
            ps = paras(li)
            if len(ps) >= 2:
                m.append((strip_label(ps[0]), strip_label(ps[1])))
        myths[lang] = m
        key = c[c.find('class="crs-key"'):]
        key = key[:end(key, 0, '<ul', '</ul>')]
        concepts[lang] = [txt(li) for li in lis(key)]
        fc = c[c.find('class="crs-fc"'):]
        fc = fc[:end(fc, 0, '<div', '</div>')]
        keep = []
        old = []
        for li in lis(fc):
            if 'crs-jet' in li:
                keep.append('<li>' + li.split('<li>', 1)[-1] if False else li if li.startswith('<li>') else '<li>' + li)
                # lis() returns the inner content without the <li> wrapper? 
                # Looking at lis(): it returns block[a:b] which INCLUDES <li> but not </li>.
                keep[-1] = li + '</li>'
            else:
                front = txt(re.search(r'class="crs-fc-f">(.*?)</p>', li, re.S).group(1)) if 'crs-fc-f' in li else ''
                back = txt(re.search(r'class="crs-fc-b">(.*?)</p>', li, re.S).group(1)) if 'crs-fc-b' in li else ''
                if front and back:
                    old.append((front, back))
        cards_old[lang] = old
        jets[lang] = keep
        pl = c[c.find('class="crs-planet"'):]
        pl = pl[:pl.find('class="crs-src"')]
        planet[lang] = [txt(x) for x in re.findall(r'<p>(.*?)</p>', pl, re.S)]

    # Questions: existing MC, myths (false), printed numbers, true statements, then concepts.
    questions = {lang: list(quiz_mc[lang]) for lang in LANGS}
    for i, (myth, actually) in enumerate(myths['en']):
        for lang in LANGS:
            mq, aq = myths[lang][i]
            questions[lang].append(pack_q(lang, 'tf', topic, mq, aq, src, name, ok=False))
    num_idx = {'w': set(), 'p': set()}
    for kind, idx, ok, tol, unit in NUM[uid]:
        num_idx[kind].add(idx)
        for lang in LANGS:
            pool = worked[lang] if kind == 'w' else practice[lang]
            q, why = pool[idx]
            shown = display_unit(lang, unit)
            if shown and shown not in q:
                q = q.rstrip() + HINT[lang].replace('{u}', shown)
            questions[lang].append(pack_q(
                lang, 'num', topic, q, why, src, name, ok=ok, tol=tol, unit=shown))
    for lang in LANGS:
        for i, (q, a) in enumerate(practice[lang]):
            if i in num_idx['p']:
                continue
            questions[lang].append(pack_q(lang, 'tf', topic, a, WHY_TRUE[lang] + ' ' + q, src, name, ok=True))
        for i, (q, a) in enumerate(worked[lang]):
            if i in num_idx['w']:
                continue
            questions[lang].append(pack_q(lang, 'tf', topic, a, WHY_TRUE[lang] + ' ' + q, src, name, ok=True))
        for para in planet[lang]:
            if len(questions[lang]) >= 20:
                break
            questions[lang].append(pack_q(lang, 'tf', topic, para, WHY_TRUE[lang], src, name, ok=True))
        for concept in concepts[lang]:
            if len(questions[lang]) >= 20:
                break
            questions[lang].append(pack_q(lang, 'tf', topic, concept, WHY_TRUE[lang], src, name, ok=True))
        obj = chunks[lang]
        mark = obj.find('class="crs-obj"')
        block = obj[mark:end(obj, mark, '<ul', '</ul>')]
        for item in lis(block):
            if len(questions[lang]) >= 20:
                break
            goal = txt(item)
            questions[lang].append(pack_q(
                lang, 'tf', topic, OBJ_Q[lang].replace('{x}', goal), WHY_TRUE[lang], src, name, ok=True))
        questions[lang] = questions[lang][:20]

    # Cards: existing text, myths, worked, practice, concept splits, planet sentences.
    cards = {lang: [] for lang in LANGS}
    seen = {lang: set() for lang in LANGS}

    def add(lang, front, back):
        front, back = front.strip(), back.strip()
        if len(front) < 2 or len(back) < 2:
            return
        key = front.casefold()
        if key in seen[lang]:
            return
        seen[lang].add(key)
        cards[lang].append({'f': front, 'b': back})

    for lang in LANGS:
        for f, b in cards_old[lang]:
            add(lang, f, b)
        for myth, actually in myths[lang]:
            add(lang, myth, actually)
        for q, a in worked[lang]:
            add(lang, q, a)
        for q, a in practice[lang]:
            add(lang, q, a)
        for concept in concepts[lang]:
            pair = cloze(concept)
            if pair:
                add(lang, pair[0], pair[1])
            else:
                add(lang, concept, WHY_TRUE[lang])
        for para in planet[lang]:
            pair = cloze(para)
            if pair:
                add(lang, pair[0], pair[1])
        cards[lang] = cards[lang][:24]

    for lang in LANGS:
        if len(questions[lang]) != 20:
            raise SystemExit(f'{uid} {lang} questions {len(questions[lang])}')
        if not 20 <= len(cards[lang]) <= 30:
            raise SystemExit(f'{uid} {lang} cards {len(cards[lang])}')
    return questions, cards, jets


def splice(lang, page, jets_by_unit, card_counts):
    pre = '' if lang == 'en' else '../'

    def repl(m):
        uid = m.group(1)
        h3 = m.group(2)
        deck, quiz = B.mount(lang, uid, 20, card_counts[uid])
        keep = ''
        jets = jets_by_unit.get(uid) or []
        if jets:
            keep = '<ul class="crs-force-keep">' + ''.join(jets) + '</ul>'
        return keep + deck + f'<h3>{h3}</h3>' + quiz

    pat = re.compile(
        r'<div class="crs-fc" data-fc="(u\d+)">.*?</ul></div><h3>(.*?)</h3><form class="crs-quiz" data-quiz="\1".*?</form>',
        re.S)
    page, n = pat.subn(repl, page)
    if n != 10:
        raise SystemExit(f'{lang} spliced {n}')
    lock = page.find('id="aero101-lock"')
    if lock > 0 and B.CHECK_CSS not in page:
        close = page.find('</style>', lock)
        page = page[:close] + B.CHECK_CSS + page[close:]
    tag = f'<script src="{pre}assets/courses/check.js?v=20261128c" defer></script>'
    needle = f'<script src="{pre}assets/courses/nasa-film.js?v=20261128a" defer></script>'
    if tag not in page:
        if needle not in page:
            raise SystemExit('film script missing ' + lang)
        page = page.replace(needle, needle + tag, 1)
    return page


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {}
    for lang in LANGS:
        path = os.path.join(ROOT, '' if lang == 'en' else lang, 'Intro_to_Aerospace_Engineering.html')
        pages[lang] = open(path, encoding='utf-8').read()
    jets = {lang: {} for lang in LANGS}
    card_counts = {lang: {} for lang in LANGS}
    for n in range(1, 11):
        questions, cards, jet = build_unit(pages, n)
        for lang in LANGS:
            card_counts[lang][f'u{n}'] = len(cards[lang])
        for lang in LANGS:
            jets[lang][f'u{n}'] = jet[lang]
            path = os.path.join(OUT, f'u{n}.{lang}.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'quiz': questions[lang], 'cards': cards[lang]}, f, ensure_ascii=False, indent=1)
            print(f'u{n}.{lang} q={len(questions[lang])} c={len(cards[lang])} jets={len(jet[lang])}')
    for lang in LANGS:
        path = os.path.join(ROOT, '' if lang == 'en' else lang, 'Intro_to_Aerospace_Engineering.html')
        text = splice(lang, pages[lang], jets[lang], card_counts[lang])
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    print('spliced')


if __name__ == '__main__':
    main()
