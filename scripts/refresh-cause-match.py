#!/usr/bin/env python3
"""Refresh Match from the solution pages, and add the Find-your-cause lines.

Donate counts on Ways to Help are counted from each page's donation cards.
The takes-donations flag is the official donation URL in ways-to-help.json,
which is the same set the English Ways to Help page lists.
Does not change donate_click tracking or stylesheet preload pairs.
"""
import html, json, os, re
from datetime import date

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
E = lambda s: html.escape(s if s is not None else '', quote=True)
TODAY = date.today().isoformat()
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
FOLDER = {'en': '', 'fr': 'fr/', 'es': 'es/', 'ar': 'ar/', 'it': 'it/', 'he': 'he/'}
DONATE_LABEL = {
    'en': 'Donate', 'fr': 'Faire un don', 'es': 'Donar',
    'ar': 'تبرّع', 'it': 'Dona', 'he': 'תרומה',
}
# Counted sentence. {n} is the number of donation cards on that language's Ways to Help page.
COPY = {
    'en': dict(
        line='Not sure this is your cause? See if your interest lies with one of our other {n} hand-selected groups.',
        btn='Find your cause',
        causes=[
            ('earth-observation', 'Earth Observation'), ('forests', 'Forests'), ('lakes', 'Lakes'),
            ('ocean', 'Ocean'), ('planetary-defense', 'Planetary Defense'), ('polar', 'Polar'),
            ('project-rawane', 'Project Rawane'), ('rivers', 'Rivers'), ('space', 'Space'),
            ('space-disposal', 'Space Disposal'), ('space-weather', 'Space Weather'),
        ],
        nodonate='{names} solutions don\'t take donations yet. Here are other ways to help.',
        nodonate_short='{names} solutions don\'t take donations yet.',
        join_and=' and ',
        counts='{n} solutions on this site. {d} take donations.',
    ),
    'fr': dict(
        line='Ce n\'est pas votre cause ? Voyez si votre intérêt rejoint l\'un de nos {n} autres groupes choisis à la main.',
        btn='Trouvez votre cause',
        causes=[
            ('earth-observation', 'Observation de la Terre'), ('forests', 'Forêts'), ('lakes', 'Lacs'),
            ('ocean', 'Océan'), ('planetary-defense', 'Défense planétaire'), ('polar', 'Pôles'),
            ('project-rawane', 'Projet Rawane'), ('rivers', 'Rivières'), ('space', 'Espace'),
            ('space-disposal', 'Élimination spatiale'), ('space-weather', 'Météo spatiale'),
        ],
        nodonate='Les solutions {names} n\'acceptent pas encore de dons. Voici d\'autres façons d\'aider.',
        nodonate_short='Les solutions {names} n\'acceptent pas encore de dons.',
        join_and=' et ',
        counts='{n} solutions sur ce site. {d} acceptent des dons.',
    ),
    'es': dict(
        line='¿No es esta tu causa? Mira si tu interés encaja con uno de nuestros otros {n} grupos elegidos a mano.',
        btn='Encuentra tu causa',
        causes=[
            ('earth-observation', 'Observación de la Tierra'), ('forests', 'Bosques'), ('lakes', 'Lagos'),
            ('ocean', 'Océano'), ('planetary-defense', 'Defensa planetaria'), ('polar', 'Polos'),
            ('project-rawane', 'Proyecto Rawane'), ('rivers', 'Ríos'), ('space', 'Espacio'),
            ('space-disposal', 'Eliminación espacial'), ('space-weather', 'Clima espacial'),
        ],
        nodonate='Las soluciones de {names} todavía no aceptan donaciones. Estas son otras formas de ayudar.',
        nodonate_short='Las soluciones de {names} todavía no aceptan donaciones.',
        join_and=' y ',
        counts='{n} soluciones en este sitio. {d} aceptan donaciones.',
    ),
    'ar': dict(
        line='أليست هذه قضيتك؟ انظر إن كان اهتمامك يوافق إحدى مجموعاتنا الأخرى المختارة يدويًا، وعددها {n}.',
        btn='اعثر على قضيتك',
        causes=[
            ('earth-observation', 'رصد الأرض'), ('forests', 'الغابات'), ('lakes', 'البحيرات'),
            ('ocean', 'المحيط'), ('planetary-defense', 'الدفاع الكوكبي'), ('polar', 'القطبان'),
            ('project-rawane', 'مشروع Rawane'), ('rivers', 'الأنهار'), ('space', 'الفضاء'),
            ('space-disposal', 'التخلص من الحطام الفضائي'), ('space-weather', 'طقس الفضاء'),
        ],
        nodonate='حلول {names} لا تقبل التبرعات بعد. هذه طرق أخرى للمساعدة.',
        nodonate_short='حلول {names} لا تقبل التبرعات بعد.',
        join_and=' و',
        counts='في هذا الموقع {n} حلول، منها {d} تقبل التبرعات.',
    ),
    'it': dict(
        line='Non è questa la tua causa? Guarda se il tuo interesse è per uno degli altri {n} gruppi che abbiamo scelto a mano.',
        btn='Trova la tua causa',
        causes=[
            ('earth-observation', 'Osservazione della Terra'), ('forests', 'Foreste'), ('lakes', 'Laghi'),
            ('ocean', 'Oceano'), ('planetary-defense', 'Difesa planetaria'), ('polar', 'Poli'),
            ('project-rawane', 'Progetto Rawane'), ('rivers', 'Fiumi'), ('space', 'Spazio'),
            ('space-disposal', 'Smaltimento dei detriti spaziali'), ('space-weather', 'Meteo spaziale'),
        ],
        nodonate='Le soluzioni di {names} non accettano ancora donazioni. Ecco altri modi per aiutare.',
        nodonate_short='Le soluzioni di {names} non accettano ancora donazioni.',
        join_and=' e ',
        counts='{n} soluzioni su questo sito. {d} accettano donazioni.',
    ),
    'he': dict(
        line='זו לא המטרה שלך? בדקו אם העניין שלכם הוא באחת מ-{n} הקבוצות האחרות שבחרנו בקפידה.',
        btn='מצאו את המטרה',
        causes=[
            ('earth-observation', 'תצפית על כדור הארץ'), ('forests', 'יערות'), ('lakes', 'אגמים'),
            ('ocean', 'אוקיינוס'), ('planetary-defense', 'הגנה פלנטרית'), ('polar', 'הקטבים'),
            ('project-rawane', 'Project Rawane'), ('rivers', 'נהרות'), ('space', 'חלל'),
            ('space-disposal', 'סילוק פסולת חלל'), ('space-weather', 'מזג אוויר בחלל'),
        ],
        nodonate='הפתרונות בנושא {names} עדיין לא מקבלים תרומות. הנה דרכים אחרות לעזור.',
        nodonate_short='הפתרונות בנושא {names} עדיין לא מקבלים תרומות.',
        join_and=' ו',
        counts='באתר {n} פתרונות. {d} מהם מקבלים תרומות.',
    ),
}
HUB_SLUG = {
    'Earth_Observation.html': 'earth-observation',
    'Deforestation.html': 'forests',
    'Lakes.html': 'lakes',
    'Oceans.html': 'ocean',
    'Planetary_Defense.html': 'planetary-defense',
    'Polar.html': 'polar',
    'Project-Rawane.html': 'project-rawane',
    'Rivers.html': 'rivers',
    'Space.html': 'space',
    'Space_Disposal.html': 'space-disposal',
    'Space_Weather.html': 'space-weather',
}
FIND_CSS = (
    '.wh-find{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.7rem 1rem;'
    'max-width:46rem;margin:.85rem auto 0;padding:.8rem 1rem;text-align:center;'
    'border:1px solid rgba(160,225,255,.45);border-radius:16px;'
    'background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.05)),rgba(10,79,120,.35);'
    'box-shadow:inset 0 1px 0 rgba(255,255,255,.28)}'
    '.wh-find-copy{flex:1 1 16rem;margin:0;line-height:1.45}'
    '.wh-find .btn{flex:none;margin:0}'
)


def plain(fragment):
    t = re.sub(r'<[^>]+>', ' ', fragment or '')
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def page_donate(path, lang):
    """Official Donate URL from that solution page's own Donate button."""
    if not path or not os.path.exists(path):
        return ''
    src = open(path, encoding='utf8').read()
    label = DONATE_LABEL[lang]
    for sec in re.findall(r'<section[^>]*\bid="support"[^>]*>(.*?)</section>', src, re.S):
        for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', sec, re.S):
            attrs, inner = m.group(1), m.group(2)
            if 'help-btn' not in attrs:
                continue
            text = plain(inner)
            if 'data-sp-donate' not in attrs and text != label:
                continue
            href = re.search(r'\bhref="([^"]+)"', attrs)
            if not href:
                continue
            url = html.unescape(href.group(1))
            if url.startswith('https://') and 'savingplanets.com' not in url.lower():
                return url
    return ''


def help_kind(url):
    u = url or ''
    if re.search(r'career|/(jobs|employ)(/|$|\.)|recruiting/jobs', u, re.I):
        return 'careers'
    if re.search(r'/(contact|inquiries|enquiry)(/|$|\.)|contact\.html|contact-us|contact-2', u, re.I):
        return 'contact'
    return 'volunteer' if u else 'none'


def donate_cards(path):
    src = open(path, encoding='utf8').read()
    m = re.search(r'id="donations".*?</section>', src, re.S)
    if not m:
        raise SystemExit('no donations section in ' + path)
    return re.findall(r'<li class="wh-card">.*?</li>', m.group(0), re.S)


def donate_count(path):
    n = 0
    for card in donate_cards(path):
        if re.search(r'<a class="btn help-btn', card):
            n += 1
    return n


def read(path):
    return open(path, encoding='utf8').read()


def write(path, text):
    if not os.path.exists(path) or read(path) != text:
        open(path, 'w', encoding='utf8').write(text)
        return True
    return False


def patch_ways(lang, n):
    path = FOLDER[lang] + 'Ways_to_Help.html'
    src = read(path)
    c = COPY[lang]
    sentence = E(c['line'].replace('{n}', str(n)))
    block = ('<p class="wh-find"><span class="wh-find-copy">' + sentence + '</span> '
             '<a class="btn help-btn" href="Match.html?help=money">' + E(c['btn']) + '</a></p>')
    src2 = re.sub(r'<p class="wh-find">.*?</p>', block, src, count=1, flags=re.S)
    if src2 == src:
        src2 = src.replace('</p><p class="wh-jump">', '</p>' + block + '<p class="wh-jump">', 1)
        # intro closes, then jump. The replace above needs the intro's </p>.
        if src2 == src:
            src2 = re.sub(r'(<p class="wh-intro">.*?</p>)', r'\1' + block, src, count=1, flags=re.S)
    if '.wh-find{' not in src2:
        src2 = src2.replace('.wh-intro{', FIND_CSS + '.wh-intro{', 1)
    if not write(path, src2):
        print('ways unchanged', path)
    else:
        print('ways', path, n)


def is_donate_section(sec, lang):
    if 'data-sp-donate="1"' in sec:
        return True
    label = DONATE_LABEL[lang]
    for m in re.finditer(r'<a\b[^>]*class="[^"]*help-btn[^"]*"[^>]*>(.*?)</a>', sec, re.S):
        if plain(m.group(1)) == label:
            return True
    return False


def patch_solutions(lang, n):
    c = COPY[lang]
    sentence = c['line'].replace('{n}', str(n))
    line = ('<p class="cause-alt" style="margin:.65rem auto 0;max-width:40rem;font-size:.92rem;line-height:1.45;text-align:center">'
            '<a href="Ways_to_Help.html" style="text-decoration:underline;text-underline-offset:2px">' + E(sentence) + '</a></p>')
    folder = FOLDER[lang]
    changed = 0
    for name in os.listdir(folder or '.'):
        if not name.endswith('.html'):
            continue
        path = folder + name
        src = read(path)
        if 'id="support"' not in src:
            continue

        def repl(m):
            sec = m.group(0)
            if 'cause-alt' in sec or not is_donate_section(sec, lang):
                return sec
            dm = re.search(r'<div class="help-btns">.*?</div>', sec, re.S)
            if not dm:
                return sec
            return sec[:dm.end()] + line + sec[dm.end():]

        src2 = re.sub(r'<section\b[^>]*\bid="support"[^>]*>.*?</section>', repl, src, count=1, flags=re.S)
        if src2 != src:
            write(path, src2)
            changed += 1
    print('solution lines', lang, changed)


def solution_rows():
    sol = read('Solutions.html')
    hubs = [(m.start(), m.group(1)) for m in re.finditer(r'<h2[^>]*><a href="([^"]+)">', sol)]
    rows = []
    for m in re.finditer(r'<article class="card sol-card" data-url="([^"]+)"', sol):
        hub = [h for h in hubs if h[0] < m.start()][-1][1]
        if hub not in HUB_SLUG:
            raise SystemExit('unknown hub ' + hub)
        rows.append((m.group(1), HUB_SLUG[hub]))
    return rows


def first_sentence(text):
    text = (text or '').strip()
    m = re.match(r'(.+?[.!?。])(\s|$)', text)
    return ((m.group(1) if m else text)[:220])


def page_title_blurb(path, fallback_title):
    if not os.path.exists(path):
        return None
    src = read(path)
    hm = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
    title = plain(hm.group(1)) if hm else fallback_title
    dm = re.search(r'<meta name="description" content="([^"]*)"', src)
    blurb = first_sentence(html.unescape(dm.group(1))) if dm else ''
    return title or fallback_title, blurb


def card_from_article(article, lang):
    im = re.search(r'<img\b([^>]*)>', article, re.S)
    if not im:
        return None
    attrs = im.group(1)
    src_m = re.search(r'\ssrc="([^"]+)"', attrs)
    if not src_m:
        return None
    alt_m = re.search(r'\salt="([^"]*)"', attrs)
    w_m = re.search(r'\swidth="(\d+)"', attrs)
    h_m = re.search(r'\sheight="(\d+)"', attrs)
    credit_m = re.search(r'<p class="photo-credit sol-credit">(.*?)</p>', article, re.S)
    card = {'src': html.unescape(src_m.group(1)), 'alt': html.unescape(alt_m.group(1)) if alt_m else ''}
    if w_m:
        card['w'] = int(w_m.group(1))
    if h_m:
        card['h'] = int(h_m.group(1))
    if credit_m:
        card['credit'] = credit_m.group(1)
    return card


def refresh_cards(lang, urls):
    path = 'assets/data/match-cards.%s.json' % lang
    cards = json.load(open(path, encoding='utf8')) if os.path.exists(path) else {}
    sol = read(FOLDER[lang] + 'Solutions.html') if os.path.exists(FOLDER[lang] + 'Solutions.html') else ''
    added = 0
    for url in urls:
        if url in cards and cards[url].get('src'):
            continue
        m = re.search(r'<article class="card sol-card" data-url="%s".*?</article>' % re.escape(url), sol, re.S)
        if not m:
            continue
        card = card_from_article(m.group(0), lang)
        if not card:
            continue
        cards[url] = card
        added += 1
    json.dump(cards, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    open(path, 'a', encoding='utf8').write('\n')
    print('cards', lang, 'added', added, 'total', len(cards))


def refresh_match():
    wth = json.load(open('assets/data/ways-to-help.json', encoding='utf8'))
    locs = json.load(open('assets/data/map-locations.json', encoding='utf8'))['solutions']
    kids_raw = open('assets/data/kids-world.en.json', encoding='utf8').read()
    kids = set(re.findall(r'"u":\s*"([^"]+\.html)"', kids_raw))
    rows = solution_rows()
    base = []
    for url, theme in rows:
        slug = url[:-5]
        org = wth['orgs'].get(wth['pages'].get(slug) or '', [None, None, None, None])
        don, hlp = (org[1] if len(org) > 1 else None), (org[2] if len(org) > 2 else None)
        kind = help_kind(hlp or '')
        loc = locs.get(url, {})
        local = any(pin.get('basis') == 'page' for pin in loc.get('pins') or [])
        remote = bool(don) or kind == 'volunteer' or loc.get('strip') in ('orbit', 'world') or not local
        meta = page_title_blurb(url, slug.replace('_', ' '))
        title, blurb = meta if meta else (slug, '')
        base.append({
            'url': url, 'title': title, 'theme': theme, 'blurb': blurb,
            'give': bool(don), 'time': kind == 'volunteer', 'local': local, 'remote': remote,
            'kid': url in kids, 'where': '', 'donate': don or '',
            'volunteer': hlp if kind == 'volunteer' else '',
        })
    urls = [r['url'] for r in base]
    for lang in LANGS:
        out = []
        folder = FOLDER[lang]
        for r in base:
            path = folder + r['url'] if lang != 'en' else r['url']
            if lang != 'en' and not os.path.exists(path):
                continue
            item = dict(r)
            if lang != 'en':
                got = page_title_blurb(path, r['title'])
                if got:
                    item['title'], item['blurb'] = got
            href = page_donate(path, lang)
            if not href and lang != 'en':
                href = page_donate(r['url'], 'en')
            item['donate'] = href
            item['give'] = bool(href)
            out.append(item)
        dest = 'assets/data/match.%s.json' % lang
        json.dump({'generated': TODAY, 'solutions': out}, open(dest, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        open(dest, 'a', encoding='utf8').write('\n')
        give = sum(1 for s in out if s['give'])
        print('match', lang, len(out), 'give', give)
        refresh_cards(lang, urls if lang == 'en' else [s['url'] for s in out])
    return base


def cause_opts(lang):
    parts = []
    for value, label in COPY[lang]['causes']:
        rid = 'cause-' + value
        parts.append(
            '<label class="sp9-opt" for="%s"><input type="checkbox" name="cause" id="%s" value="%s"> <span>%s</span></label>'
            % (rid, rid, value, E(label))
        )
    return ''.join(parts)


def patch_match(lang):
    path = FOLDER[lang] + 'Match.html'
    src = read(path)
    c = COPY[lang]
    src2 = re.sub(r'assets/match\.js\?v=[^"]+', 'assets/match.js?v=20261121a', src, count=1)
    src2 = re.sub(r'assets/match\.css\?v=[^"]+', 'assets/match.css?v=20261121a', src2, count=1)
    src2 = re.sub(
        r'(<form class="sp9-form" id="match-form"><fieldset><legend>.*?</legend>.*?<div class="sp9-opts">).*?(</div>)',
        lambda m: m.group(1) + cause_opts(lang) + m.group(2),
        src2, count=1, flags=re.S)
    if 'id="match-counts"' not in src2:
        src2 = src2.replace(
            '<form class="sp9-form" id="match-form">',
            '<form class="sp9-form" id="match-form"><p class="sp9-hint" id="match-counts" hidden></p>',
            1)
    m = re.search(r'(<script id="match-js">window\.SP9MATCH=)(\{.*?\})(;?</script>)', src2)
    if not m:
        raise SystemExit('no SP9MATCH in ' + path)
    data = json.loads(m.group(2))
    data['nodonate'] = c['nodonate']
    data['nodonate_short'] = c['nodonate_short']
    data['join_and'] = c['join_and']
    data['counts'] = c['counts']
    blob = json.dumps(data, ensure_ascii=False, separators=(', ', ': '))
    src2 = src2[:m.start()] + m.group(1) + blob + ';' + m.group(3)[1:] + src2[m.end():]
    # group 3 includes the semicolon already if the regex captured ';</script>' or ';</script>'
    if ';;</script>' in src2:
        src2 = src2.replace(';;</script>', ';</script>', 1)
    write(path, src2)
    print('match page', path)


def main():
    counts = {}
    for lang in LANGS:
        n = donate_count(FOLDER[lang] + 'Ways_to_Help.html')
        counts[lang] = n
        print('donate cards', lang, n)
    if counts['en'] != 84:
        raise SystemExit('English Ways to Help donate count is %s, expected 84' % counts['en'])
    for lang in LANGS:
        patch_ways(lang, counts[lang])
        patch_solutions(lang, counts[lang])
        patch_match(lang)
    refresh_match()


if __name__ == '__main__':
    main()
