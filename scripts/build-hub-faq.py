#!/usr/bin/env python3
"""Oct 26 2026: Inject a short 'People also ask' block + FAQPage JSON-LD into hub/topic pages
from assets/data/question-bank.csv. Max 6 questions per page to keep weight down. Idempotent
(SP-HUBFAQ markers). Does not touch Artemis launch-tracker.js. Run after build-question-bank.py.
"""
import csv, html, json, os, re
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BANK = ROOT / 'assets/data/question-bank.csv'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
# Pages that get on-page FAQ (hubs + key topic pages only — not all 246 solutions)
TARGETS = {
    'Oceans.html': 'oceans',
    'Rivers.html': 'rivers',
    'Lakes.html': 'lakes',
    'Deforestation.html': 'forests',
    'Space.html': 'space',
    'Earth_Observation.html': 'earth-observation',
    'Planetary_Defense.html': 'planetary-defense',
    'Space_Weather.html': 'space-weather',
    'Polar.html': 'polar',
    'Learn.html': 'learning',
    'Teachers.html': 'teachers',
    'Play_and_Learn.html': 'kids',
    'Ways_to_Help.html': 'ways-to-help',
    'Myth_vs_Fact.html': 'myth',
    'Solutions.html': 'solutions',
    # Artemis: FAQ only; do not edit launch-tracker script
    'Artemis_II.html': 'launches',
}
HEAD = {
    'en': 'People also ask',
    'fr': 'Autres questions fréquentes',
    'es': 'Otras preguntas frecuentes',
    'ar': 'أسئلة أخرى يطرحها الزوار',
    'it': 'Altre domande frequenti',
    'he': 'שאלות נוספות שאנשים שואלים',
}
MORE = {
    'en': 'More big questions',
    'fr': 'Plus de grandes questions',
    'es': 'Más grandes preguntas',
    'ar': 'المزيد من الأسئلة الكبيرة',
    'it': 'Altre grandi domande',
    'he': 'עוד שאלות גדולות',
}
CSS = ('.sp-paa{margin:1.6rem auto 2rem;max-width:820px;padding:0 1.2rem}'
       '.sp-paa h2{font-size:1.25rem;margin:0 0 .8rem}'
       '.sp-paa details{border:1px solid rgba(124,170,255,.35);border-radius:12px;padding:.55rem .85rem;margin:.45rem 0;background:rgba(124,170,255,.06)}'
       '.sp-paa summary{cursor:pointer;font-weight:600}'
       '.sp-paa .paa-a{margin:.45rem 0 .2rem;line-height:1.5;font-size:.95rem}'
       '.sp-paa .paa-src{font-size:.85rem;opacity:.9}'
       '.sp-paa .paa-more{margin-top:.8rem}')

def esc(s): return html.escape(s or '', quote=False)
def escq(s): return html.escape(s or '', quote=True)
def d(lang): return '' if lang == 'en' else lang + '/'

def load_bank():
    by = defaultdict(list)
    with open(BANK, encoding='utf8') as f:
        for row in csv.DictReader(f):
            by[(row['language'], row['cluster'])].append(row)
    return by

def pick(rows, page, limit=6):
    """Prefer rows whose answering_page is this page (strip hash), then fill from cluster."""
    base = page
    primary, rest = [], []
    for r in rows:
        ap = (r['answering_page'] or '').split('#')[0]
        (primary if ap == base else rest).append(r)
    out, seen = [], set()
    for r in primary + rest:
        q = r['question']
        if q in seen:
            continue
        seen.add(q)
        out.append(r)
        if len(out) >= limit:
            break
    return out

def block(lang, page, items):
    if not items:
        return ''
    details = []
    ents = []
    for r in items:
        src = r['source_url']
        lab = r['source_label']
        ap = r['answering_page']
        # relative link to answering page when on-site
        href = ap if not ap.startswith('http') else ap
        details.append(
            f'<details><summary>{esc(r["question"])}</summary>'
            f'<p class="paa-a">{esc(r["answer_excerpt"])}</p>'
            f'<p class="paa-src">Source: <a href="{escq(src)}" target="_blank" rel="noopener noreferrer">{esc(lab)}</a>'
            f' · <a href="{escq(href)}">{esc(MORE[lang]) if False else "On this site"}</a></p></details>'
        )
        ents.append({
            '@type': 'Question',
            'name': r['question'],
            'acceptedAnswer': {'@type': 'Answer', 'text': r['answer_excerpt']},
        })
    # fix "On this site" label per lang
    onsite = {
        'en': 'On this site', 'fr': 'Sur ce site', 'es': 'En este sitio',
        'ar': 'على هذا الموقع', 'it': 'Su questo sito', 'he': 'באתר הזה',
    }[lang]
    html_details = ''.join(details).replace('>On this site<', f'>{onsite}<')
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang,
           'mainEntity': ents}
    bq = f'{d(lang)}Big_Questions.html'
    # Avoid duplicate FAQPage JSON-LD on pages that already ship one (Myth_vs_Fact via seo-jsonld).
    ld = ''
    if page != 'Myth_vs_Fact.html':
        ld = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
    return (
        f'<!-- SP-HUBFAQ:START --><style id="sp-paa-css">{CSS}</style>'
        f'<section class="sp-paa" aria-label="{escq(HEAD[lang])}">'
        f'<h2>{esc(HEAD[lang])}</h2>{html_details}'
        f'<p class="paa-more"><a href="{bq}">{esc(MORE[lang])}</a></p>'
        f'</section>'
        f'{ld}'
        f'<!-- SP-HUBFAQ:END -->'
    )

def apply(path: Path, lang: str, page: str, items):
    raw = path.read_text(encoding='utf8')
    raw = re.sub(r'<!-- SP-HUBFAQ:START -->.*?<!-- SP-HUBFAQ:END -->\n?', '', raw, flags=re.S)
    blk = block(lang, page, items)
    if not blk:
        return 0
    # insert before </main> or before footer
    if '</main>' in raw:
        raw = raw.replace('</main>', blk + '\n</main>', 1)
    else:
        raw = raw.replace('<footer>', blk + '\n<footer>', 1)
    path.write_text(raw, encoding='utf8')
    return 1

def main():
    if not BANK.exists():
        raise SystemExit('missing question-bank.csv — run build-question-bank.py first')
    bank = load_bank()
    n = 0
    for page, cluster in TARGETS.items():
        for lang in LANGS:
            p = ROOT / page if lang == 'en' else ROOT / lang / page
            if not p.exists():
                continue
            items = pick(bank[(lang, cluster)], page, limit=6)
            # Solutions hub: mix oceans/forests etc — use cluster solutions rows answering Solutions.html or any
            if page == 'Solutions.html':
                items = pick(bank[(lang, 'solutions')] + bank[(lang, 'oceans')][:2], page, limit=6)
            n += apply(p, lang, page, items)
    print(f'build-hub-faq: updated {n} pages')

if __name__ == '__main__':
    main()
