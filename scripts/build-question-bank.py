#!/usr/bin/env python3
"""Oct 26 2026: Build assets/data/question-bank.csv from live site content (no invented facts).
Mines Myth vs Fact (6 langs), solution page title/description (6 langs), hub heroes, Learn/Teachers/
Play & Learn, Ways to Help, and Artemis launch-tracker intro. Every row cites answering_page + source.
Also writes /workspace/seo/question-bank.csv when that path exists.
Usage: python3 scripts/build-question-bank.py
"""
import csv, html, json, os, re, sys
from pathlib import Path
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit('need beautifulsoup4')

ROOT = Path(__file__).resolve().parent.parent
# Prefer fuller workspace tree for mining if present
MINE = Path('/workspace/Saveworld') if Path('/workspace/Saveworld/Myth_vs_Fact.html').exists() else ROOT
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
OUT = ROOT / 'assets' / 'data' / 'question-bank.csv'
OUT_WS = Path('/workspace/seo/question-bank.csv')
FIELDS = ['question', 'language', 'cluster', 'answering_page', 'answer_excerpt', 'source_label', 'source_url']

# Hub file → cluster id
HUBS = {
    'Oceans.html': 'oceans',
    'Rivers.html': 'rivers',
    'Lakes.html': 'lakes',
    'Deforestation.html': 'forests',
    'Space.html': 'space',
    'Earth_Observation.html': 'earth-observation',
    'Planetary_Defense.html': 'planetary-defense',
    'Space_Weather.html': 'space-weather',
    'Polar.html': 'polar',
    'Project-Rawane.html': 'space',
    'Space_Disposal.html': 'space',
    'Learn.html': 'learning',
    'Teachers.html': 'teachers',
    'Play_and_Learn.html': 'kids',
    'Amazing_Facts.html': 'kids',
    'Ways_to_Help.html': 'ways-to-help',
    'Artemis_II.html': 'launches',
    'Myth_vs_Fact.html': 'myth',
    'Solutions.html': 'solutions',
    'Big_Questions.html': 'big-questions',
    'Courses.html': 'learning',
}

# Native templates for solution questions (not literal word-for-word of EN)
SOL_Q = {
    'en': 'What is {name}, and how does it help the planet?',
    'fr': 'Qu’est-ce que {name}, et comment cela aide-t-il la planète ?',
    'es': '¿Qué es {name} y cómo ayuda al planeta?',
    'ar': 'ما هو {name} وكيف يساعد الكوكب؟',
    'it': 'Cos’è {name} e come aiuta il pianeta?',
    'he': 'מה זה {name} ואיך זה עוזר לכדור הארץ?',
}
MYTH_Q = {
    'en': 'Is it true that {claim}',
    'fr': 'Est-il vrai que {claim}',
    'es': '¿Es verdad que {claim}',
    'ar': 'هل صحيح أن {claim}',
    'it': 'È vero che {claim}',
    'he': 'האם נכון ש{claim}',
}

def path(lang, page):
    return MINE / page if lang == 'en' else MINE / lang / page

def read_soup(p: Path):
    if not p.exists():
        return None
    return BeautifulSoup(p.read_text(encoding='utf8'), 'lxml')

def meta_desc(soup):
    m = soup.find('meta', attrs={'name': 'description'})
    return (m.get('content') or '').strip() if m else ''

def abs_src(href):
    if not href:
        return ''
    if href.startswith('http'):
        return href
    return 'https://www.savingplanets.com/' + href.lstrip('/')

def clip(s, n=280):
    s = re.sub(r'\s+', ' ', (s or '')).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + '…'

def add(rows, question, language, cluster, answering_page, answer, source_label, source_url):
    q = clip(question, 200)
    a = clip(answer, 320)
    if not q or not a:
        return
    rows.append({
        'question': q,
        'language': language,
        'cluster': cluster,
        'answering_page': answering_page,
        'answer_excerpt': a,
        'source_label': clip(source_label or answering_page, 120),
        'source_url': source_url or abs_src(answering_page),
    })

def mine_myths(rows):
    for lang in LANGS:
        soup = read_soup(path(lang, 'Myth_vs_Fact.html'))
        if not soup:
            continue
        for card in soup.select('article.myth-card'):
            claim_el = card.find('h2')
            paras = [p.get_text(' ', strip=True) for p in card.select('p') if 'myth-tag' not in (p.get('class') or []) and 'myth-source' not in (p.get('class') or []) and 'myth-honest' not in (p.get('class') or [])]
            # fact is first substantial p after h2; honest is .myth-honest
            fact = ''
            for p in card.find_all('p'):
                cls = p.get('class') or []
                if 'myth-tag' in cls or 'myth-source' in cls:
                    continue
                if 'myth-honest' in cls:
                    fact = (fact + ' ' + p.get_text(' ', strip=True)).strip()
                    continue
                if not fact and p.get_text(strip=True):
                    fact = p.get_text(' ', strip=True)
            honest = card.select_one('.myth-honest')
            if honest and honest.get_text(strip=True) not in fact:
                fact = (fact + ' ' + honest.get_text(' ', strip=True)).strip()
            src_a = card.select_one('.myth-source a')
            claim = claim_el.get_text(' ', strip=True) if claim_el else ''
            if not claim or not fact:
                continue
            # Prefer question-shaped claim; else wrap
            if claim.endswith('?') or claim.startswith('هل') or claim.startswith('¿') or '؟' in claim:
                q = claim
            else:
                # strip trailing period for wrapper
                c = claim[:-1] if claim.endswith('.') else claim
                # French/Spanish myth lines may already be statements
                tmpl = MYTH_Q[lang]
                # Arabic/Hebrew templates expect claim without leading particle duplication
                q = tmpl.format(claim=c)
                if not q.endswith('?') and not q.endswith('؟'):
                    q += '?' if lang not in ('ar',) else '؟'
            mid = card.get('id') or ''
            page = f'Myth_vs_Fact.html#{mid}' if mid else 'Myth_vs_Fact.html'
            add(rows, q, lang, 'myth', page, fact,
                src_a.get_text(' ', strip=True) if src_a else 'Myth vs Fact',
                src_a.get('href') if src_a else abs_src('Myth_vs_Fact.html'))

def mine_solutions(rows):
    data = json.load(open(MINE / 'assets/data/solutions.json', encoding='utf8'))
    pages = data.get('pages') or []
    cat_cluster = {
        'ocean': 'oceans', 'lakes': 'lakes', 'rivers': 'rivers', 'forests': 'forests',
        'space': 'space', 'planetary-defense': 'planetary-defense', 'polar': 'polar',
        'space-weather': 'space-weather', 'earth-observation': 'earth-observation',
        'project-r': 'space',
    }
    for rec in pages:
        url = rec.get('url') or ''
        if not url.endswith('.html'):
            continue
        page = url.split('/')[-1]
        if page in HUBS and HUBS[page] != 'solutions':
            continue  # hubs mined separately
        cluster = cat_cluster.get(rec.get('category') or '', 'solutions')
        for lang in LANGS:
            soup = read_soup(path(lang, page))
            if not soup or not soup.title:
                continue
            title = soup.title.string or rec.get('title') or page
            title = re.sub(r'\s*\|\s*Saving Planets\s*$', '', title).strip()
            # shorten name for question
            name = title.split(':')[0].strip()
            desc = meta_desc(soup)
            if not desc:
                continue
            # prefer sp:stat source URL when present
            st = soup.find('meta', attrs={'name': 'sp:stat'})
            src_url = abs_src(page)
            src_label = name
            if st and st.get('content'):
                parts = st['content'].split('|')
                if len(parts) >= 5 and parts[4].startswith('http'):
                    src_url = parts[4]
                    src_label = parts[0] or name
            # also try first fact-source link on page
            fa = soup.select_one('p.fact-source a, .fact-source a')
            if fa and fa.get('href', '').startswith('http'):
                src_url = fa['href']
                src_label = fa.get_text(' ', strip=True) or src_label
            q = SOL_Q[lang].format(name=name)
            add(rows, q, lang, cluster, page, desc, src_label, src_url)

def mine_hub_hero(rows, page, cluster, q_templates):
    """q_templates: lang -> question string using {topic} optional."""
    for lang in LANGS:
        soup = read_soup(path(lang, page))
        if not soup:
            continue
        h1 = soup.h1.get_text(' ', strip=True) if soup.h1 else page
        # hero blurb: first .page-hero p or meta description
        hero = ''
        hp = soup.select_one('.page-hero p, .page-hero-content p')
        if hp:
            hero = hp.get_text(' ', strip=True)
        if not hero:
            hero = meta_desc(soup)
        if not hero:
            continue
        q = q_templates[lang].format(topic=h1)
        add(rows, q, lang, cluster, page, hero, h1, abs_src(page))

def mine_list_headings(rows, page, cluster, prefix_templates, limit=8):
    """Turn h2/h3 topic headings into questions when a following paragraph exists."""
    for lang in LANGS:
        soup = read_soup(path(lang, page))
        if not soup:
            continue
        n = 0
        for h in soup.select('main h2, main h3'):
            if n >= limit:
                break
            title = h.get_text(' ', strip=True)
            if not title or len(title) < 3:
                continue
            # skip nav chrome
            if title.lower() in ('hubs', 'explore', 'explore another solution'):
                continue
            nxt = h.find_next_sibling(['p', 'div'])
            ans = ''
            if nxt:
                if nxt.name == 'p':
                    ans = nxt.get_text(' ', strip=True)
                else:
                    p = nxt.find('p')
                    ans = p.get_text(' ', strip=True) if p else nxt.get_text(' ', strip=True)[:300]
            if not ans or len(ans) < 40:
                continue
            q = prefix_templates[lang].format(topic=title)
            add(rows, q, lang, cluster, page, ans, title, abs_src(page))
            n += 1

def main():
    rows = []
    mine_myths(rows)

    # Hub heroes — native questions
    mine_hub_hero(rows, 'Oceans.html', 'oceans', {
        'en': 'What is Saving Planets doing about the oceans?',
        'fr': 'Que fait Saving Planets pour les océans ?',
        'es': '¿Qué hace Saving Planets por los océanos?',
        'ar': 'ماذا يفعل Saving Planets من أجل المحيطات؟',
        'it': 'Cosa fa Saving Planets per gli oceani?',
        'he': 'מה Saving Planets עושה למען האוקיינוסים?',
    })
    mine_hub_hero(rows, 'Rivers.html', 'rivers', {
        'en': 'How can rivers be restored and protected?',
        'fr': 'Comment restaurer et protéger les rivières ?',
        'es': '¿Cómo se pueden restaurar y proteger los ríos?',
        'ar': 'كيف يمكن استعادة الأنهار وحمايتها؟',
        'it': 'Come si possono restaurare e proteggere i fiumi?',
        'he': 'איך אפשר לשקם ולהגן על נהרות?',
    })
    mine_hub_hero(rows, 'Lakes.html', 'lakes', {
        'en': 'What solutions help protect lakes?',
        'fr': 'Quelles solutions aident à protéger les lacs ?',
        'es': '¿Qué soluciones ayudan a proteger los lagos?',
        'ar': 'ما الحلول التي تساعد في حماية البحيرات؟',
        'it': 'Quali soluzioni aiutano a proteggere i laghi?',
        'he': 'אילו פתרונות עוזרים להגן על אגמים?',
    })
    mine_hub_hero(rows, 'Deforestation.html', 'forests', {
        'en': 'What is being done to protect and restore forests?',
        'fr': 'Que fait-on pour protéger et restaurer les forêts ?',
        'es': '¿Qué se hace para proteger y restaurar los bosques?',
        'ar': 'ما الذي يُفعل لحماية الغابات واستعادتها؟',
        'it': 'Cosa si fa per proteggere e restaurare le foreste?',
        'he': 'מה עושים כדי להגן על יערות ולשקם אותם?',
    })
    mine_hub_hero(rows, 'Space.html', 'space', {
        'en': 'How does space science help save Earth?',
        'fr': 'Comment la science spatiale aide-t-elle à sauver la Terre ?',
        'es': '¿Cómo ayuda la ciencia espacial a salvar la Tierra?',
        'ar': 'كيف يساعد علم الفضاء في إنقاذ الأرض؟',
        'it': 'Come la scienza spaziale aiuta a salvare la Terra?',
        'he': 'איך מדע החלל עוזר להציל את כדור הארץ?',
    })
    mine_hub_hero(rows, 'Earth_Observation.html', 'earth-observation', {
        'en': 'How do Earth-observing satellites help people and nature?',
        'fr': 'Comment les satellites d’observation de la Terre aident-ils les gens et la nature ?',
        'es': '¿Cómo ayudan los satélites de observación de la Tierra a las personas y a la naturaleza?',
        'ar': 'كيف تساعد أقمار رصد الأرض الناس والطبيعة؟',
        'it': 'Come i satelliti di osservazione della Terra aiutano le persone e la natura?',
        'he': 'איך לווייני תצפית כדור הארץ עוזרים לאנשים ולטבע?',
    })
    mine_hub_hero(rows, 'Planetary_Defense.html', 'planetary-defense', {
        'en': 'What is planetary defense, and does it work?',
        'fr': 'Qu’est-ce que la défense planétaire, et est-ce que ça marche ?',
        'es': '¿Qué es la defensa planetaria y funciona?',
        'ar': 'ما الدفاع الكوكبي وهل ينجح؟',
        'it': 'Cos’è la difesa planetaria e funziona?',
        'he': 'מהי הגנה פלנטרית והאם זה עובד?',
    })
    mine_hub_hero(rows, 'Ways_to_Help.html', 'ways-to-help', {
        'en': 'How can I donate or volunteer through Saving Planets?',
        'fr': 'Comment puis-je donner ou faire du bénévolat via Saving Planets ?',
        'es': '¿Cómo puedo donar o ser voluntario a través de Saving Planets?',
        'ar': 'كيف يمكنني التبرع أو التطوع عبر Saving Planets؟',
        'it': 'Come posso donare o fare volontariato tramite Saving Planets?',
        'he': 'איך אפשר לתרום או להתנדב דרך Saving Planets?',
    })
    mine_hub_hero(rows, 'Learn.html', 'learning', {
        'en': 'What can I learn for free on Saving Planets?',
        'fr': 'Que puis-je apprendre gratuitement sur Saving Planets ?',
        'es': '¿Qué puedo aprender gratis en Saving Planets?',
        'ar': 'ماذا يمكنني أن أتعلم مجانًا على Saving Planets؟',
        'it': 'Cosa posso imparare gratis su Saving Planets?',
        'he': 'מה אפשר ללמוד בחינם ב-Saving Planets?',
    })
    mine_hub_hero(rows, 'Teachers.html', 'teachers', {
        'en': 'What free materials does Saving Planets offer teachers?',
        'fr': 'Quels supports gratuits Saving Planets propose-t-il aux enseignants ?',
        'es': '¿Qué materiales gratuitos ofrece Saving Planets a los docentes?',
        'ar': 'ما المواد المجانية التي يقدّمها Saving Planets للمعلمين؟',
        'it': 'Quali materiali gratuiti offre Saving Planets agli insegnanti?',
        'he': 'אילו חומרים חינמיים Saving Planets מציע למורים?',
    })
    mine_hub_hero(rows, 'Play_and_Learn.html', 'kids', {
        'en': 'What can kids explore on Saving Planets?',
        'fr': 'Que peuvent explorer les enfants sur Saving Planets ?',
        'es': '¿Qué pueden explorar los niños en Saving Planets?',
        'ar': 'ماذا يمكن للأطفال استكشافه على Saving Planets؟',
        'it': 'Cosa possono esplorare i bambini su Saving Planets?',
        'he': 'מה ילדים יכולים לגלות ב-Saving Planets?',
    })
    mine_hub_hero(rows, 'Artemis_II.html', 'launches', {
        'en': 'Where can I follow upcoming launches and how they relate to Saving Planets solutions?',
        'fr': 'Où suivre les prochains lancements et leur lien avec les solutions Saving Planets ?',
        'es': '¿Dónde seguir los próximos lanzamientos y su relación con las soluciones de Saving Planets?',
        'ar': 'أين أتابع عمليات الإطلاق القادمة وعلاقتها بحلول Saving Planets؟',
        'it': 'Dove seguire i prossimi lanci e il legame con le soluzioni Saving Planets?',
        'he': 'איפה לעקוב אחרי שיגורים קרובים וקשרם לפתרונות Saving Planets?',
    })

    mine_list_headings(rows, 'Teachers.html', 'teachers', {
        'en': 'What teacher resources cover {topic}?',
        'fr': 'Quelles ressources enseignants couvrent {topic} ?',
        'es': '¿Qué recursos para docentes cubren {topic}?',
        'ar': 'ما موارد المعلمين التي تغطي {topic}؟',
        'it': 'Quali risorse per insegnanti coprono {topic}?',
        'he': 'אילו משאבים למורים מכסים את {topic}?',
    }, limit=10)

    mine_list_headings(rows, 'Learn.html', 'learning', {
        'en': 'What is in the {topic} learning path?',
        'fr': 'Que contient le parcours {topic} ?',
        'es': '¿Qué incluye la ruta de aprendizaje {topic}?',
        'ar': 'ماذا يوجد في مسار التعلّم {topic}؟',
        'it': 'Cosa c’è nel percorso {topic}?',
        'he': 'מה כולל מסלול הלמידה {topic}?',
    }, limit=8)

    mine_solutions(rows)

    # Dedupe by (language, question lower)
    seen = set()
    uniq = []
    for r in rows:
        k = (r['language'], r['question'].lower())
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'w', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(uniq)
    try:
        OUT_WS.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_WS, 'w', encoding='utf8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(uniq)
    except Exception as e:
        print('workspace copy skip:', e)

    # summary
    from collections import Counter
    by_c = Counter(r['cluster'] for r in uniq)
    by_l = Counter(r['language'] for r in uniq)
    print(f'question-bank: {len(uniq)} rows')
    print('by cluster:', dict(sorted(by_c.items())))
    print('by language:', dict(sorted(by_l.items())))

if __name__ == '__main__':
    main()
