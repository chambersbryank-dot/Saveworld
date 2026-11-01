#!/usr/bin/env python3
"""Oct 28 2026 (founder-approved text, 4:29 PM HST): 'How we feature solutions from around the world' policy on About.html
(#feature-policy, after #criteria) + a one-line link to it on every solution hub page (FEATPOL markers, before the bottom link).
Names no countries. EN source only; i18n-build translates from i18n/<lang>.json, into which this script merges the strings in
i18n/feature-policy-1028.json (hand-drafted, not native-reviewed). Idempotent; run before i18n-build (weekly-sync wired)."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
H = 'How We Feature Solutions from Around the World'
PARAS = ["Saving Planets showcases solutions from any country that genuinely help both people and nature.",
         "We judge each effort on its own record, not on the government of the country it works in.",
         "We feature efforts that are independent and transparent about how they use their funds.",
         "Featuring a project doesn't mean we're partners with it or endorse it; we share it so people can learn and find ways to help.",
         "We link Donate buttons only to organizations that publish audited finances or carry a recognized charity rating, so your gift goes to the cause and not to corruption.",
         "Every fact we share comes from a source we cite."]
HUBS = ['Earth_Observation.html', 'Deforestation.html', 'Lakes.html', 'Oceans.html', 'Planetary_Defense.html', 'Polar.html', 'Rivers.html',
        'Space.html', 'Space_Disposal.html', 'Space_Weather.html', 'Project-Rawane.html']

def put(t, tag, blk, anchor_rx):
    t = re.sub(rf'<!-- {tag}:START -->.*?<!-- {tag}:END -->\n?', '', t, flags=re.S)
    m = re.search(anchor_rx, t, re.S)
    if not m: raise SystemExit(f'{tag}: anchor not found')
    return t[:m.end()] + f'\n<!-- {tag}:START -->{blk}<!-- {tag}:END -->' + t[m.end():]

def main():
    from html import escape as E
    sec = (f'<section class="five-ws" id="feature-policy"><h2>{E(H)}</h2><div class="impact-box">'
           + ''.join(f'<p>{E(p, quote=False)}</p>' for p in PARAS) + '</div></section>')
    t = open('About.html', encoding='utf8').read()
    t2 = put(t, 'FEATPOL', sec, r'<section class="five-ws" id="criteria">.*?</section>')
    if t2 != t: open('About.html', 'w', encoding='utf8').write(t2)
    line = ('<p class="feat-policy-link"><strong>Showcase, not partnership:</strong> '
            '<a href="About.html#feature-policy">How we feature solutions from around the world</a></p>')
    n = 0
    for f in HUBS:
        if not os.path.exists(f): continue
        t = open(f, encoding='utf8').read()
        t = re.sub(r'<!-- FEATPOL:START -->.*?<!-- FEATPOL:END -->\n?', '', t, flags=re.S)
        i = t.find('<section class="donate-banner')
        if i < 0: i = t.find('<section class="next-solutions"')
        if i < 0: i = t.find('</main>')
        t = t[:i] + f'<!-- FEATPOL:START -->{line}<!-- FEATPOL:END -->\n' + t[i:]
        open(f, 'w', encoding='utf8').write(t); n += 1
    T = json.load(open('i18n/feature-policy-1028.json', encoding='utf8')); T.pop('_note', None)
    for lang in ('fr', 'es', 'ar', 'it', 'he'):
        p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf8'))
        for en, tr in T.items(): m[en] = tr[lang]
        json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(f'feature policy: About + {n} hubs')

if __name__ == '__main__':
    main()
