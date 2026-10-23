#!/usr/bin/env python3
"""Oct 22 (founder): Contact 'Get in Touch' card order, all languages:
Teachers & Schools, Send a Solution, Help Translate, Partnerships & Sponsorships, General Questions, then the rest in
their existing order, Found an Error / Bug last. Cards are matched by their mailto address (language-independent).
dept-contacts.py refills <!-- DEPT:contact --> in place each sync, so the markers are kept (empty) after the list and
duplicate cards are dropped here. Idempotent; run after the last dept-contacts.py."""
import os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
ORDER = ['teachers@', 'ideas@', 'translate@', 'partners@', 'hello@']
LAST = 'errors@'
SEC = re.compile(r'(<h2>[^<]*</h2><div class="ws-grid">)(.*?)(</div></section>)', re.S)
CARD = re.compile(r'<div class="w-card"[^>]*>(?:(?!<div).)*?</div>', re.S)
def key(c):
    m = re.search(r'mailto:([\w.-]+@)', c); return m.group(1) if m else 'other:' + c[:80]
n = 0
for d in ('', 'fr/', 'es/', 'ar/', 'it/', 'he/'):
    f = d + 'Contact.html'
    if not os.path.exists(f): continue
    s = open(f, encoding='utf8').read()
    for m in SEC.finditer(s):
        body = m.group(2)
        if 'mailto:errors@' not in body or 'mailto:teachers@' not in body: continue
        cards, seen = [], set()
        for c in CARD.findall(body):
            k = key(c)
            if k not in seen: seen.add(k); cards.append((k, c))
        rank = lambda kc: (ORDER.index(kc[0]) if kc[0] in ORDER else (99 if kc[0] == LAST else 50))
        cards.sort(key=rank)  # stable: the rest keep their order
        new = ''.join(c for _, c in cards) + '<!-- DEPT:contact --><!-- /DEPT:contact -->'
        s2 = s[:m.start(2)] + new + s[m.end(2):]
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
        break
print('contact-order:', n, 'pages updated')
