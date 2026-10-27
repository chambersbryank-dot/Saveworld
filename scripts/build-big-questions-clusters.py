#!/usr/bin/env python3
"""Oct 26 2026: Expand Big_Questions.html with cluster sections from question-bank.csv.
Each cluster shows up to 5 questions with short answers + link to the answering page.
Idempotent (SP-BQ-CLUSTERS markers). Keeps existing core FAQ cards. Run after build-question-bank.
"""
import csv, html, json, os, re
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BANK = ROOT / 'assets/data/question-bank.csv'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
# Display order and labels
CLUSTERS = [
    ('myth', {'en':'Myth vs Fact','fr':'Mythe ou réalité','es':'Mito o realidad','ar':'خرافة أم حقيقة','it':'Mito o realtà','he':'מיתוס מול עובדה'}),
    ('learning', {'en':'Learning & courses','fr':'Apprentissage et cours','es':'Aprendizaje y cursos','ar':'التعلّم والدورات','it':'Apprendimento e corsi','he':'למידה וקורסים'}),
    ('teachers', {'en':'Teachers','fr':'Enseignants','es':'Docentes','ar':'المعلمون','it':'Insegnanti','he':'מורים'}),
    ('kids', {'en':'Kids','fr':'Enfants','es':'Niños','ar':'الأطفال','it':'Bambini','he':'ילדים'}),
    ('oceans', {'en':'Oceans','fr':'Océans','es':'Océanos','ar':'المحيطات','it':'Oceani','he':'אוקיינוסים'}),
    ('rivers', {'en':'Rivers','fr':'Rivières','es':'Ríos','ar':'الأنهار','it':'Fiumi','he':'נהרות'}),
    ('lakes', {'en':'Lakes','fr':'Lacs','es':'Lagos','ar':'البحيرات','it':'Laghi','he':'אגמים'}),
    ('forests', {'en':'Forests','fr':'Forêts','es':'Bosques','ar':'الغابات','it':'Foreste','he':'יערות'}),
    ('space', {'en':'Space','fr':'Espace','es':'Espacio','ar':'الفضاء','it':'Spazio','he':'חלל'}),
    ('earth-observation', {'en':'Earth Observation','fr':'Observation de la Terre','es':'Observación de la Tierra','ar':'رصد الأرض','it':'Osservazione della Terra','he':'תצפית כדור הארץ'}),
    ('planetary-defense', {'en':'Planetary Defense','fr':'Défense planétaire','es':'Defensa planetaria','ar':'الدفاع الكوكبي','it':'Difesa planetaria','he':'הגנה פלנטרית'}),
    ('ways-to-help', {'en':'Ways to Help','fr':'Comment aider','es':'Formas de ayudar','ar':'طرق المساعدة','it':'Come aiutare','he':'דרכים לעזור'}),
    ('launches', {'en':'Launches','fr':'Lancements','es':'Lanzamientos','ar':'عمليات الإطلاق','it':'Lanci','he':'שיגורים'}),
    ('solutions', {'en':'Solutions','fr':'Solutions','es':'Soluciones','ar':'الحلول','it':'Soluzioni','he':'פתרונות'}),
]
INTRO = {
    'en': 'Questions from across Saving Planets — each answer is taken from our pages and their cited sources.',
    'fr': 'Des questions à travers Saving Planets — chaque réponse vient de nos pages et de leurs sources citées.',
    'es': 'Preguntas de todo Saving Planets: cada respuesta sale de nuestras páginas y sus fuentes citadas.',
    'ar': 'أسئلة من أنحاء Saving Planets — كل إجابة مأخوذة من صفحاتنا ومصادرها المذكورة.',
    'it': 'Domande da tutto Saving Planets: ogni risposta viene dalle nostre pagine e dalle fonti citate.',
    'he': 'שאלות מכל Saving Planets — כל תשובה לקוחה מהדפים שלנו ומהמקורות המצוטטים.',
}
READ = {
    'en': 'Read on Saving Planets', 'fr': 'Lire sur Saving Planets', 'es': 'Leer en Saving Planets',
    'ar': 'اقرأ على Saving Planets', 'it': 'Leggi su Saving Planets', 'he': 'קראו ב-Saving Planets',
}
SRC = {'en':'Source','fr':'Source','es':'Fuente','ar':'المصدر','it':'Fonte','he':'מקור'}
LIMIT = 5

def esc(s): return html.escape(s or '', quote=False)
def escq(s): return html.escape(s or '', quote=True)

def load():
    by = defaultdict(list)
    with open(BANK, encoding='utf8') as f:
        for row in csv.DictReader(f):
            by[(row['language'], row['cluster'])].append(row)
    return by

def pick(rows, limit=LIMIT):
    out, seen = [], set()
    # prefer hub-level answering pages first (shorter paths without many solution dupes)
    hubby = [r for r in rows if r['answering_page'].split('#')[0] in {
        'Myth_vs_Fact.html','Oceans.html','Rivers.html','Lakes.html','Deforestation.html','Space.html',
        'Learn.html','Teachers.html','Play_and_Learn.html','Ways_to_Help.html','Artemis_II.html',
        'Earth_Observation.html','Planetary_Defense.html','Solutions.html','Amazing_Facts.html'}]
    for r in hubby + rows:
        if r['question'] in seen: continue
        seen.add(r['question']); out.append(r)
        if len(out) >= limit: break
    return out

def section_html(lang, bank):
    parts = [f'<section class="bq-clusters" id="clusters"><h2 class="bq-clusters-h">{esc(INTRO[lang])}</h2>']
    ents = []
    for cid, labels in CLUSTERS:
        items = pick(bank[(lang, cid)])
        if not items: continue
        parts.append(f'<section class="bq-cluster" id="cluster-{cid}"><h3>{esc(labels[lang])}</h3>')
        for r in items:
            href = r['answering_page']
            parts.append(
                f'<article class="bq-card bq-cluster-card"><h4>{esc(r["question"])}</h4>'
                f'<p>{esc(r["answer_excerpt"])}</p>'
                f'<p class="bq-src"><strong>{esc(SRC[lang])}:</strong> '
                f'<a href="{escq(r["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(r["source_label"])}</a></p>'
                f'<p class="bq-more"><a href="{escq(href)}">{esc(READ[lang])}</a></p></article>')
            ents.append({'@type':'Question','name':r['question'],
                         'acceptedAnswer':{'@type':'Answer','text':r['answer_excerpt']}})
        parts.append('</section>')
    parts.append('</section>')
    # Additional FAQPage graph for cluster Qs (Google allows multiple FAQ blocks carefully — we merge into one script)
    faq = {'@context':'https://schema.org','@type':'FAQPage','inLanguage':lang,'mainEntity':ents[:50]}  # cap schema size
    css = ('.bq-clusters{max-width:820px;margin:2rem auto;padding:0 1.2rem}'
           '.bq-clusters-h{font-size:1.15rem;font-weight:600;margin:0 0 1rem;opacity:.95}'
           '.bq-cluster{margin:1.6rem 0}'
           '.bq-cluster h3{font-size:1.2rem;margin:0 0 .6rem;color:#8fd3ff}'
           '.bq-cluster-card h4{font-size:1.05rem;margin:.1rem 0 .4rem}')
    return (
        '<!-- SP-BQ-CLUSTERS:START -->'
        f'<style id="bq-clusters-css">{css}</style>'
        + ''.join(parts) +
        f'<script type="application/ld+json" id="bq-clusters-ld">{json.dumps(faq, ensure_ascii=False)}</script>'
        '<!-- SP-BQ-CLUSTERS:END -->'
    )

def apply(lang, bank):
    p = ROOT / 'Big_Questions.html' if lang == 'en' else ROOT / lang / 'Big_Questions.html'
    if not p.exists():
        return 0
    raw = p.read_text(encoding='utf8')
    raw = re.sub(r'<!-- SP-BQ-CLUSTERS:START -->.*?<!-- SP-BQ-CLUSTERS:END -->\n?', '', raw, flags=re.S)
    blk = section_html(lang, bank)
    # insert before closing bq-wrap / before bq-meta
    if '<p class="bq-meta">' in raw:
        raw = raw.replace('<p class="bq-meta">', blk + '\n<p class="bq-meta">', 1)
    elif '</div></main>' in raw:
        raw = raw.replace('</div></main>', blk + '\n</div></main>', 1)
    else:
        raw = raw.replace('</main>', blk + '\n</main>', 1)
    p.write_text(raw, encoding='utf8')
    return 1

def main():
    bank = load()
    n = sum(apply(l, bank) for l in LANGS)
    print(f'build-big-questions-clusters: {n} pages')

if __name__ == '__main__':
    main()
