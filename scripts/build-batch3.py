#!/usr/bin/env python3
"""Batch 3: Myth_vs_Fact.html, Rawanes_Mission_Log.html (from the Press.html template),
5-question hub quizzes (QUIZ marker block), footer + Amazing Facts links. Idempotent.
Content lives in scripts/batch3-content.py (QUIZZES, MYTHS, LOG). To add a Mission Log entry,
append to LOG (newest first is rendered automatically) and rerun, then weekly-sync.sh."""
import re, html, json, os, sys, importlib.util
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
spec = importlib.util.spec_from_file_location('c', 'scripts/batch3-content.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
E = html.escape
TPL = open('Press.html', encoding='utf8').read()
FOOT = TPL[TPL.index('<footer>'):]

def page(slug, title, h1, sub, desc, body):
    head = TPL[:TPL.index('<section class="page-hero')]
    head = head.replace('Press and media kit for Saving Planets: logo downloads, mission, boilerplate, contact and fact sheets. Everything you need to write about Saving Planets.', E(desc, quote=True))
    head = head.replace('Press and Media | Saving Planets', E(title)).replace('"Press and Media"', json.dumps(h1)).replace('Press.html', slug + '.html')
    head = head.replace('"Press and Media"', json.dumps(h1))
    head = re.sub(r'"name": "Press and Media"', '"name": ' + json.dumps(h1), head)
    crumbs = f'<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">Home</a></li><li><span aria-current="page">{E(h1)}</span></li></ol></nav>'
    hero = f'<section class="page-hero"><div class="page-hero-content"><h1>{E(h1)}</h1><p>{E(sub)}</p></div></section>\n'
    mid = hero + crumbs + '\n' + body + '\n'
    f = slug + '.html'
    if os.path.exists(f):  # keep the existing (seo-fixed) head and footer; only refresh the body
        cur = open(f, encoding='utf8').read(); a = cur.index('<section class="page-hero'); b = cur.index('<footer>')
        if cur[a:b] == mid: print('unchanged', slug); return
        open(f, 'w', encoding='utf8').write(cur[:a] + mid + cur[b:]); print('updated', slug); return
    open(f, 'w', encoding='utf8').write(head + mid + FOOT)
    print('wrote', slug)

# ---- Myth vs Fact
cards = []
for i, m in enumerate(C.MYTHS, 1):
    rel = ''.join(f'<li><a href="{p}">{E(t)}</a></li>' for p, t in m['related'])
    cards.append(f'<article class="myth-card" id="myth-{i}"><p class="myth-tag myth-tag-myth">Myth</p><h2>{E(m["myth"])}</h2>'
                 f'<p class="myth-tag myth-tag-fact">Fact</p><p>{E(m["fact"])}</p><p class="myth-honest">{E(m["honest"])}</p>'
                 f'<p class="myth-source">Source: <a href="{m["url"]}" target="_blank" rel="noopener">{E(m["src"])}</a></p>'
                 f'<div class="myth-related"><p>On Saving Planets:</p><ul>{rel}</ul></div></article>')
body = ('<section class="impact" id="intro"><h2>Why This Page Exists</h2><div class="impact-box"><p>' + E(C.MYTH_INTRO) + '</p></div></section>\n'
        '<section class="myths" aria-label="Myths and facts">' + ''.join(cards) + '</section>\n'
        '<section class="help-actions" id="more"><h2>More Sourced Good News</h2><p>' + E(C.MYTH_MORE) + '</p><p><a class="btn" href="Amazing_Facts.html">Amazing Facts</a> <a class="btn help-btn" href="Rawanes_Mission_Log.html">Rawane&#x27;s Mission Log</a></p></section>')
page('Myth_vs_Fact', 'Myth vs Fact: Doom Myths, Busted | Saving Planets', 'Myth vs Fact', 'Common doom myths, checked against NASA, NOAA and ESA.', C.MYTH_DESC, body)

# ---- Mission Log
ents = []
for e in C.LOG:  # newest first
    paras = ''.join(f'<p>{p}</p>' for p in e['paras'])
    facts = ''.join(f'<li>{E(t)} <a href="{u}" target="_blank" rel="noopener">{E(s)}</a></li>' for t, s, u in e['facts'])
    rel = ''.join(f'<li><a href="{p}">{E(t)}</a></li>' for p, t in e['related'])
    ents.append(f'<article class="log-entry" id="{e["id"]}"><p class="log-meta"><span>{E(e["num"])}</span> · <time datetime="{e["date"]}">{E(e["date_label"])}</time></p><h2>{E(e["title"])}</h2>{paras}'
                f'<div class="log-facts"><h3>Fact Check</h3><ul>{facts}</ul></div><div class="myth-related"><p>On Saving Planets:</p><ul>{rel}</ul></div></article>')
body = ('<section class="impact" id="intro"><h2>Who Is Rawane?</h2><div class="impact-box"><p>' + E(C.LOG_INTRO) + '</p><p>' + E(C.LOG_RULE) + '</p><p>Her home base: <a href="Project-Rawane.html">Project Rawane</a></p></div></section>\n'
        '<aside class="new-callout" aria-label="New"><a href="Nancy_Grace_Roman.html"><span class="new-badge">New</span><span class="new-text">Rawane is tracking NASA\'s new Roman Space Telescope on its trip to L2.</span><span class="new-cta">See Roman <span aria-hidden="true">→</span></span></a></aside>\n'
        '<!-- LOG: entries are generated from scripts/batch3-content.py (LOG list, newest first) -->\n<section class="mission-log" aria-label="Log entries">' + ''.join(ents) + '</section>')
page('Rawanes_Mission_Log', "Rawane's Mission Log | Saving Planets", "Rawane's Mission Log", 'Weekly field notes from our astronaut mascot. The story is made up; the facts are real.', C.LOG_DESC, body)

# ---- Quizzes
def quiz(hub, qs, name):
    out = [f'<section class="quiz" id="quiz" aria-labelledby="quiz-h"><h2 id="quiz-h">Quick Quiz: {E(name)}</h2><p class="quiz-intro">Five questions from this hub. Pick an answer to see if you got it, with a link to the source page. Nothing is tracked.</p>']
    for i, q in enumerate(qs, 1):
        opts = ''.join(f'<li><button type="button" class="quiz-opt" data-i="{j}">{E(o)}</button></li>' for j, o in enumerate(q['opts']))
        out.append(f'<fieldset class="quiz-q" data-answer="{q["a"]}"><legend><span class="quiz-num">{i}.</span> {E(q["q"])}</legend><ul class="quiz-opts" role="list">{opts}</ul>'
                   f'<div class="quiz-fb" role="status" aria-live="polite" hidden><p><strong class="quiz-ok" hidden>Correct.</strong><strong class="quiz-no" hidden>Not quite.</strong> {E(q["why"])}</p>'
                   f'<p><a href="{q["page"]}">Read the source page</a></p></div></fieldset>')
    out.append('<div class="quiz-result" hidden><p class="quiz-score" role="status" aria-live="polite"></p><p class="quiz-actions"><button type="button" class="btn quiz-share">Share my score</button> <button type="button" class="btn help-btn quiz-reset">Try again</button></p><p class="quiz-copied" role="status" aria-live="polite" hidden>Copied to your clipboard.</p></div>')
    out.append(f'<p class="quiz-tpl" hidden>I scored {{n}} out of 5 on the {E(name)} quiz at Saving Planets.</p><p class="quiz-tpl-score" hidden>You scored {{n}} out of 5.</p></section>')
    return ''.join(out)

for hub, (name, qs) in C.QUIZZES.items():
    f = hub + '.html'; s = open(f, encoding='utf8').read()
    block = '<!-- QUIZ:START -->' + quiz(hub, qs, name) + '<!-- QUIZ:END -->'
    s = re.sub(r'<!-- QUIZ:START -->.*?<!-- QUIZ:END -->\n?', '', s, flags=re.S)
    i = s.index('<section class="donate-banner bottom-link"') if '<section class="donate-banner bottom-link"' in s else s.index('<section class="next-solutions"')
    s = s[:i] + block + '\n' + s[i:]
    open(f, 'w', encoding='utf8').write(s); print('quiz:', f, len(qs))

# ---- Footer links + Amazing Facts cross-link (English pages; translations regenerate)
OLD = '<p class="footer-links"><a href="Press.html">Press &amp; media</a></p>'
NEW = '<p class="footer-links"><a href="Press.html">Press &amp; media</a><span aria-hidden="true"> · </span><a href="Myth_vs_Fact.html">Myth vs Fact</a><span aria-hidden="true"> · </span><a href="Rawanes_Mission_Log.html">Rawane&#x27;s Mission Log</a></p>'
n = 0
for f in sorted(os.listdir('.')):
    if f.endswith('.html'):
        s = open(f, encoding='utf8').read()
        if OLD in s: open(f, 'w', encoding='utf8').write(s.replace(OLD, NEW)); n += 1
print('footers:', n)
f = 'Amazing_Facts.html'; s = open(f, encoding='utf8').read()
XL = '<!-- MYTH-LINK:START --><section class="help-actions myth-xlink"><h2>Heard a Doom Headline?</h2><p>We check common doom myths against NASA, NOAA and ESA.</p><p><a class="btn" href="Myth_vs_Fact.html">Myth vs Fact</a></p></section><!-- MYTH-LINK:END -->'
s = re.sub(r'<!-- MYTH-LINK:START -->.*?<!-- MYTH-LINK:END -->\n?', '', s, flags=re.S)
s = s.replace('<footer>', XL + '\n<footer>', 1); open(f, 'w', encoding='utf8').write(s)
