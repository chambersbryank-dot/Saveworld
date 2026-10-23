#!/usr/bin/env python3
"""Oct 23 2026 batch (our founder approved Oct 23): Cool Earth basic income pilot (Forests), Andfjorden Marine Protected Area
(Oceans) and Atoll Rewilding (Oceans). Same writer as batch-1021-content.py / batch-1020s-content.py (Surfrider_Foundation.html
skeleton, BLUF box, Five W's, Connected Solutions, XLINK1023 blocks on existing pages). Every fact was re-opened at build time
(2026-10-23) and is labeled with its source. Cool Earth is the only one with a verified donate page; the other two link
learn pages. Ocean cards go right after Palau / Papahanaumokuakea on the Oceans hub. Also: the Amazing Facts hand card on
gasoline-only car sales (FACT1023 markers, kept by build-facts.js as data-fact-origin="hand").
Re-runnable: overwrites only these pages, their hub cards (added once), XLINK1023 blocks and the FACT1023 card."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b20s', os.path.join(ROOT, 'scripts/batch-1020s-content.py'))
b20s = importlib.util.module_from_spec(spec); spec.loader.exec_module(b20s)
W, see_block, body, pin = b20s.W, b20s.see_block, b20s.body, b20s.pin
ADDED = '2026-10-23'
TAG = 'XLINK1023'

BATH = ('https://www.bath.ac.uk/announcements/world-first-basic-income-trial-boosts-indigenous-livelihoods-and-amazon-rainforest-protection/', 'University of Bath, World-first basic income trial boosts Indigenous livelihoods and Amazon rainforest protection (20 Oct. 2026)')
BATH0 = ('https://www.bath.ac.uk/announcements/can-a-basic-income-keep-rainforests-standing-university-of-bath-researchers-are-finding-out/', 'University of Bath, Can a basic income keep rainforests standing?')
BATHR = ('https://researchportal.bath.ac.uk/en/publications/fighting-the-climate-crisis-with-reciprocity-towards-indigenous-a/', 'University of Bath, Fighting the climate crisis with reciprocity: Towards Indigenous autonomy (report, 14 Oct. 2026)')
GUAR = ('https://www.theguardian.com/environment/2026/oct/20/unconditional-basic-income-amazon-rainforest-peru-study', 'The Guardian, Giving £2 a day to people in the Amazon helps protect rainforest, pilot project finds (20 Oct. 2026)')
COOLN = 'https://www.coolearth.org/news/world-first-basic-income-trial-boosts-indigenous-livelihoods-and-amazon-rainforest-protection/'
COOLD = 'https://www.coolearth.org/donate/'
AND = ('https://www.regjeringen.no/en/whats-new/andfjorden-blir-noregs-storste-marine-verneomrade/id3173076/', "Norwegian Ministry of Climate and Environment, Andfjorden becomes Norway's largest marine protected area (18 Sept. 2026)")
GRA = ('https://doi.org/10.1126/sciadv.aei1145', 'Graham, Benkwitt et al., Seabirds and native vegetation drive ecosystem processes that support atoll island resilience, Science Advances (14 Oct. 2026)')
ENG = ('https://doi.org/10.1126/sciadv.aem6116', 'Rewilding the atoll engine, Science Advances (Oct. 2026)')
LAN = ('https://www.lancaster.ac.uk/news/culling-rats-and-restoring-native-vegetation-how-rewilding-tropical-atolls-could-help-them-keep-pace-with-rising-sea-levels', 'Lancaster University, How rewilding tropical atolls could help them keep pace with rising sea levels (14 Oct. 2026)')

PAGES = [
 dict(slug='Cool_Earth_Basic_Income', title='Cool Earth Basic Income Pilot (Peruvian Amazon)', short='the basic income pilot', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='earth', label='Nonprofit solution · pilot completed, rollout planned',
  img=('Puerto_Bermudez_Peru_Rainforest.jpg', 1920, 1080, "A brown river lined with rainforest at Puerto Bermúdez, in Peru's central Amazon"),
  credit='Heiner Amado Cadillo via Wikimedia Commons (Puerto Bermúdez, Peru, 2016, CC BY-SA 3.0)',
  hook="No-strings cash for Indigenous families in the Amazon, and the forest gains too.",
  wow=("Close to 90% of participants adopted forest-friendly practices, such as native reforestation, less forest burning and restoring water springs (University of Bath).", BATH),
  lead="Cool Earth gave 211 Indigenous people in three communities in Peru's central Amazon an unconditional basic income for two years (University of Bath).",
  eli=['Some families in the Amazon rainforest have very little money.',
       'A charity gave each person a small amount of money every few months, to spend however they wanted.',
       'Families ate better, stayed home instead of leaving for work, and planted and protected more forest.'],
  ws=[('Who', 'The charity Cool Earth, co-designed with two Indigenous women-led groups, ONAMIAP and OMIAASEC; evaluated by the University of Bath.', BATH),
      ('What', 'A "Cash Plus" pilot: cash transfers of 1,032 soles, about £2 a day, plus community-led training.', BATH),
      ('When', 'Two years; the first transfer was made in November 2023, and results came out in October 2026.', BATH0),
      ('Where', "Three Indigenous communities in Peru's Asháninka region, in the central Peruvian Amazon.", BATH),
      ('Why', 'To test direct cash as a fairer alternative to top-down conservation and, in the long run, to stop deforestation.', BATH)],
  impact=('Households unable to afford nutritious food fell from 73% to 26%. The study had no control group and did not measure forest cover or soil, so its effect on deforestation is not yet proven (The Guardian).', GUAR),
  fact=('About £2 a Day', 'Each person received 1,032 Peruvian soles per transfer, roughly £2 a day, to spend as they liked (University of Bath).', BATH),
  people=('The share of people forced to leave home for outside work fell from 43% to 18%, and 70% of households could save money, up from 49% (University of Bath).', BATH),
  nature=('Participants joined native reforestation, cut forest burning and restored water springs (University of Bath).', BATH),
  support_h='Support Cool Earth',
  btns=[('Donate to Cool Earth', COOLD), ('Read the University of Bath report', BATHR[0])],
  bottom=('Cool Earth accepts donations for its rainforest work.', COOLD, 'Donate'),
  donate_alt='Donate to Cool Earth',
  widget=None, see=[('Costa_Rica_Forest_Payments.html', 'Costa Rica Payments for Environmental Services (FONAFIFO)', 'Costa Rica pays landowners to keep forests standing.'),
                    ('MAAP.html', 'MAAP, Amazon Deforestation Watch', 'Satellite alerts that track Amazon deforestation.')],
  pin=pin(-10.3, -74.9, 'Central Peruvian Amazon, Peru (approximate area of the pilot communities)')),
 dict(slug='Andfjorden_MPA', title='Andfjorden Marine Protected Area (Norway)', short='the Andfjorden MPA', cat='ocean',
  hub=('Oceans.html', 'Oceans'), cls='government', status='active', glass='earth', label='Government solution · protected since September 2026',
  img=('Andfjorden_Andoy_2023.jpg', 1920, 1278, 'Calm water of Andfjorden seen from the rocky shore at Andøy, Norway, with distant mountains'),
  credit='Ryan Hodnett via Wikimedia Commons (Andfjorden, Andøy, Norway, 2023, CC BY-SA 4.0)',
  hook="Norway's largest marine protected area guards coral reefs and kelp forests in the far north.",
  wow=("Andfjorden covers about 1,848.5 km² (about 714 square miles), almost 260,000 football pitches, making it Norway's largest marine protected area (Norwegian government).", AND),
  lead="On 18 September 2026, Norway's government created the Andfjorden Marine Protected Area across Andøy, Harstad and Senja (Norwegian government).",
  eli=['Andfjorden is a big, cold stretch of sea in the far north of Norway.',
       'Under the water there are coral reefs, kelp forests and lots of fish, whales and seabirds.',
       'Norway made it a protected area, with extra-strict rules in the most fragile spots.'],
  ws=[('Who', "Norway's Ministry of Climate and Environment; a board of the municipalities, county authorities and the Sámi Parliament will manage it.", AND),
      ('What', 'A marine protected area with stricter zones for the most valuable, vulnerable wildlife, and one set of rules for fishing, space and defence work.', AND),
      ('When', "Established on 18 September 2026; it was one of 36 areas in Norway's 2004 Marine Protection Plan.", AND),
      ('Where', 'Waters in the far north of Nordland and the south of Troms, in the municipalities of Andøy, Harstad and Senja.', AND),
      ('Why', 'It holds coral reefs, coral gardens, sponge and sea-pen communities, kelp forests and maerl beds.', AND)],
  impact=("With this one decision, the protected share of mainland Norway's territorial waters rises from about 4.8% to 6%. It makes 24 of the 36 areas in the 2004 Marine Protection Plan protected (Norwegian government).", AND),
  fact=('260,000 Football Pitches', 'The Andfjorden protected area is about the size of 260,000 football pitches (Norwegian government).', AND),
  people=('Local municipalities, the two counties and the Sámi Parliament share the board that runs the area (Norwegian government).', AND),
  nature=('Kelp forests, shell-sand seabeds and maerl beds are spawning, nursery and feeding grounds for many fish (Norwegian government).', AND),
  support_h='Learn More About Andfjorden',
  btns=[('Norwegian government: Andfjorden MPA', AND[0])],
  bottom=("Want to go deeper? Norway's government explains the decision.", AND[0], 'For Further Information'),
  widget=None, see=[('Palau_National_Marine_Sanctuary.html', 'Palau National Marine Sanctuary', 'About 80% of Palau\'s waters are a no-take area.'),
                    ('Ross_Sea_MPA.html', 'Ross Sea Region Marine Protected Area', 'The world\'s largest marine protected area, off Antarctica.')],
  pin=pin(69.25, 16.5, 'Andfjorden, between Andøya and Senja, Norway')),
 dict(slug='Atoll_Rewilding', title='Atoll Rewilding: Seabirds Against Sea-Level Rise', short='atoll rewilding', cat='ocean',
  hub=('Oceans.html', 'Oceans'), cls='natural', status='active', glass='earth', label='Nature-based solution · new research, 2026',
  img=('Tetiaroa_Atoll_ISS018.jpg', 1920, 1280, 'Tetiaroa atoll in French Polynesia seen from the International Space Station, a ring of islets around a turquoise lagoon'),
  credit='NASA Johnson Space Center, ISS crew photo ISS018-E-024351 (Tetiaroa, French Polynesia, 27 Jan. 2009, public domain)',
  hook="Bring back the seabirds, and their droppings help reefs grow fast enough to keep up with rising seas.",
  wow=("Lagoon reefs beside rat-free, seabird-rich islands grew about 1.8 times faster, about 5.9 mm a year, enough to closely track projected sea-level rise to 2100 under 2°C of warming (Science Advances).", GRA),
  lead='A 2026 study of 28 atoll islands found that removing rats and restoring native plants boosts the seabirds, reefs and sand that help atolls keep up with rising seas (Lancaster University).',
  eli=['Atolls are rings of tiny, low islands made by coral.',
       'Seabirds catch fish at sea and leave droppings full of nutrients on the islands, which wash onto the reef.',
       'Where rats are gone, birds come back, reefs grow faster and the islands get more sand to stay above the waves.'],
  ws=[('Who', 'An international team led by Lancaster University (lead author Nick Graham), with The Nature Conservancy, the University of the Seychelles and others.', LAN),
      ('What', 'Measuring how seabird nutrients and native plants drive reef growth, sand production and soil stability, and what rat removal could add.', LAN),
      ('When', 'Published in Science Advances on 14 October 2026.', GRA),
      ('Where', '28 atoll islands in the Seychelles and the Chagos Archipelago (Indian Ocean) and Tetiaroa, French Polynesia (Pacific).', LAN),
      ('Why', 'Invasive rats wiped out many island seabird colonies, and coconut plantations now cover about 60% of Pacific atoll forests.', LAN)],
  impact=('Rat-free, seabird-rich islands had 2.3 to 2.8 times more sand-making on their reefs, and native plants meant 4.6 times more fine roots holding the soil. Restoration helps atolls adapt, but it is no substitute for cutting emissions (Science Advances).', ENG),
  fact=('170 Cubic Metres of Sand', 'Around a small island of about 14 hectares, seabird-fed reefs could make about 170 cubic metres more sediment every year (Lancaster University).', LAN),
  people=('Where sea walls and other engineering are too costly or impractical, as on remote atolls, restoration offers another way to adapt (Lancaster University).', LAN),
  nature=('Rats have already been removed from about 1,000 islands worldwide, at a growing rate (Science Advances).', GRA),
  support_h='Learn More About Atoll Rewilding',
  btns=[('Lancaster University: the study explained', LAN[0]), ('Read the paper (Science Advances)', GRA[0])],
  bottom=('Want to go deeper? Read the study in Science Advances.', GRA[0], 'For Further Information'),
  widget=None, see=[('South_Georgia_Habitat_Restoration.html', 'South Georgia Habitat Restoration', 'The world\'s largest island rodent eradication, declared a success in 2018.'),
                    ('Redonda_Restoration.html', 'Redonda Island Restoration', 'A Caribbean island that turned green after rats and goats were removed.')],
  pin=pin(-17.01, -149.56, 'Tetiaroa atoll, French Polynesia, one of the study sites')),
]
SHIP = [p['slug'] for p in PAGES]
AFTER = {'Andfjorden_MPA': 'Papahanaumokuakea', 'Atoll_Rewilding': 'Andfjorden_MPA'}  # Oceans: next to Palau / Papahānaumokuākea

XBACK = {
 'South_Georgia_Habitat_Restoration.html': [('Atoll_Rewilding.html', 'Atoll Rewilding', 'Rat-free atolls get seabirds back, and faster-growing reefs.')],
 'Redonda_Restoration.html': [('Atoll_Rewilding.html', 'Atoll Rewilding', 'Rat-free atolls get seabirds back, and faster-growing reefs.')],
 'Ross_Sea_MPA.html': [('Andfjorden_MPA.html', 'Andfjorden Marine Protected Area', "Norway's largest marine protected area, created in 2026.")],
 'Palau_National_Marine_Sanctuary.html': [('Andfjorden_MPA.html', 'Andfjorden Marine Protected Area', "Norway's largest marine protected area, created in 2026.")],
 'Costa_Rica_Forest_Payments.html': [('Cool_Earth_Basic_Income.html', 'Cool Earth Basic Income Pilot', 'No-strings cash for Indigenous families in the Peruvian Amazon.')],
}

MOB = ('https://electrek.co/2026/10/05/gas-cars-fall-below-50-percent-global-new-car-sales/', 'Electrek, Gas cars fall below 50% of global new car sales for the first time (5 Oct. 2026; Mobility Global data via Nikkei)')
FACT = (f'<!-- FACT1023:START --><div class="w-card" id="fact-under-half-gasoline-only" data-fact-origin="hand"><h3>Under Half Gasoline-Only</h3>'
        '<p>Cars that run only on gasoline fell to 49% of global new-car sales in the first half of 2026, the first time below half (Mobility Global data via Nikkei).</p>'
        '<p>Caveat: hybrids still burn fuel, so about 83% of new cars still have an engine, and this is a six-month figure during an oil price spike.</p>'
        f'<p class="fact-source">Source: <a href="{MOB[0]}" target="_blank" rel="noreferrer">{E(MOB[1])}</a></p></div><!-- FACT1023:END -->')

def place_cards():
    fp = os.path.join(ROOT, 'Oceans.html'); t = open(fp, encoding='utf8').read()
    for s, after in AFTER.items():
        m = re.search(r'<article class="card"><div class="image-container"><a class="photo-link" href="' + s + r'\.html">.*?</article>', t, re.S)
        if not m: continue
        card = m.group(0); t = t[:m.start()] + t[m.end():]
        a = re.search(r'<article class="card"><div class="image-container"><a class="photo-link" href="' + after + r'\.html">.*?</article>', t, re.S)
        t = t[:a.end()] + card + t[a.end():]
    open(fp, 'w', encoding='utf8').write(t)

def fact():
    fp = os.path.join(ROOT, 'Amazing_Facts.html'); t = open(fp, encoding='utf8').read()
    t = re.sub(r'<!-- FACT1023:START -->.*?<!-- FACT1023:END -->\n?', '', t, flags=re.S)
    i = t.find('<!-- FACTS:START -->'); j = t.find('<!-- FACTS:END -->')
    # alphabetical by heading, like build-facts.js
    for m in re.finditer(r'<div class="w-card"[^>]*><h3>(.*?)</h3>', t[i:j]):
        if m.group(1).lower() > 'under half gasoline-only':
            k = i + m.start(); break
    else: k = j
    t = t[:k] + FACT + '\n' + t[k:]
    open(fp, 'w', encoding='utf8').write(t)

def main():
    b20s.PAGES, b20s.SHIP, b20s.XBACK, b20s.ADDED = PAGES, SHIP, {}, ADDED
    b20s.main()  # pages, hub cards, eli10, map pins, anim-banners
    place_cards()
    for f, items in XBACK.items():
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = f'<!-- {TAG}:START -->' + see_block(items, 'connected-1023') + f'<!-- {TAG}:END -->'
        if f'<!-- {TAG}:START -->' in t:
            t = re.sub(rf'<!-- {TAG}:START -->.*?<!-- {TAG}:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    fact()

if __name__ == '__main__':
    main()
