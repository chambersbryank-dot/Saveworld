#!/usr/bin/env python3
"""Oct 18 2026 (owner): every card is 'flush with the text. Tight.' Site-wide, all languages (one shared stylesheet).
- No equal-height stretching: cards are height:fit-content (stops grid/flex row stretch without shrinking widths in
  column layouts), min-height:0, inner text blocks never flex-grow, so buttons/links follow the text, not the card bottom.
- Tight padding (14-16 px), small internal gaps, no doubled bottom padding (last child has no bottom margin/padding).
- Project-Rawane (pr-page) and Artemis_II (artemis-page) are tightened by their own page-scoped CSS (other worker): skipped.
Writes one /* TIGHT-CARDS */ block at the end of styles.css (re-appended each run so it stays last). Run before build-critical."""
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
B = 'body:not(.pr-page):not(.artemis-page)'
C = ':is(.card,.sol-card,.w-card,.rel-card,.tt-card,.pw-card,.sx-card,.aud-card,.myth-card,.dom-card,.ps-card,.sp-card,.cleanup-card,.sotw-card,.bp-card,.src-card,.dot-card)[class]'
G = ':is(.grid,.ws-grid,.tt-grid,.hub-cards,.myths,.dom-grid,.sb-grid,.comm-grid,.ps-grid,.mw-grid,.roman-facts)[class]'
CSS = (f'{B} {C}{{height:-webkit-fit-content;height:fit-content;min-height:0}}'
 f'{B} {G}{{grid-auto-rows:auto}}'
 f'{B} {C}>*{{flex-grow:0}}'
 f'{B} {C} :is(.sol-desc,.tt-body,.card-blurb){{flex:none}}'
 f'{B} {C}>:last-child{{margin-bottom:0;padding-bottom:0}}'
 f'{B}.toc-sub .card[class]{{padding:14px 14px 15px}}'
 f'{B}.toc-sub .card[class] h3{{padding:10px 2px 2px;margin-bottom:4px}}'
 f'{B}.toc-sub .card[class] :is(.sol-desc,.card-blurb,.sol-more,.photo-credit){{padding-left:2px;padding-right:2px}}'
 f'{B}.toc-sub .card[class] .sol-desc{{margin-bottom:8px}}'
 f'{B}.toc-sub .card[class] .card-blurb{{padding-bottom:0}}'
 f'{B} .w-card[class]{{padding:14px 16px}}'
 f'{B} .tt-card .tt-body[class]{{padding:14px 16px 15px}}'
 f'{B} .tt-card .tt-body[class] h2{{margin:.1rem 0 .45rem}}'
 f'{B} .tt-card .tt-body[class]>p{{margin-bottom:.6rem}}'
 f'{B} .tt-card .tt-body[class]>:last-child{{margin-bottom:0}}'
 f'{B}.toc-home .card-band .card[class] .solution-list{{padding-bottom:14px}}'
 # Oct 18 site-wide scan (live, 1180 px): Learn track cards, Find a Cleanup / Community region cards, Careers + standards chips,
 # Tsunami warning steps and calculator result rows were stretched to their row (19-173 px empty below the text)
 f'{B} :is(.ltracks,.lchips,.warn-steps,.cx-out,.fc-regions,.pw-stats,.roman-facts,.sx-vids)[class]{{align-items:start;grid-auto-rows:auto}}'
 f'{B} :is(.ltracks,.lchips,.warn-steps,.cx-out,.fc-regions,.pw-stats,.roman-facts,.sx-vids)[class]>*{{height:auto;min-height:0}}')
s = open('styles.css', encoding='utf-8').read()
s2 = re.sub(r'\n?/\* TIGHT-CARDS:START \*/.*?/\* TIGHT-CARDS:END \*/\n?', '\n', s, flags=re.S).rstrip('\n') + '\n/* TIGHT-CARDS:START */\n' + CSS + '\n/* TIGHT-CARDS:END */\n'
if s2 != s: open('styles.css', 'w', encoding='utf-8').write(s2)
print(f'build-tight-cards: {"updated" if s2 != s else "unchanged"}')
