#!/usr/bin/env python3
"""Nov 23, 2026 batch A: Inouye, Mālama Maunalua, Mauna Loa, Kaʻena Point, Cabo Pulmo.

Clones the Hawaiian Monk Seal page shell and hand-wires listings.
Does not run the full weekly sync. Created by the Founder and SI.
"""
import html, json, os, re, sys, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
E = lambda s: html.escape(s, quote=True)
TODAY = '2026-11-23'
UNTIL = '2026-12-23'
OLD_TOTAL = 292
TOTAL = 297
BADGE = 'background:linear-gradient(135deg,#0077b0,#005f8f);color:#fff;border:1px solid rgba(160,225,255,.6);font-weight:800'
LANGS = ['fr', 'es', 'ar', 'it', 'he']
UI = {
    'en': dict(active='Active', new='✨ New solution', image='Image:'),
    'fr': dict(active='Actif', new='✨ Nouvelle solution', image='Image :'),
    'es': dict(active='Activo', new='✨ Nueva solución', image='Imagen:'),
    'ar': dict(active='نشط', new='✨ حل جديد', image='الصورة:'),
    'it': dict(active='Attiva', new='✨ Nuova soluzione', image='Immagine:'),
    'he': dict(active='פעיל', new='✨ פתרון חדש', image='תמונה:'),
}
HUBNAME = {
    'space-weather': {'en': 'Space Weather', 'fr': 'Météo spatiale', 'es': 'Meteorología espacial', 'ar': 'طقس الفضاء', 'it': 'Meteorologia spaziale', 'he': 'מזג אוויר בחלל'},
    'ocean': {'en': 'Ocean', 'fr': 'Océan', 'es': 'Océano', 'ar': 'المحيط', 'it': 'Oceano', 'he': 'אוקיינוס'},
    'earth-observation': {'en': 'Earth Observation', 'fr': 'Observation de la Terre', 'es': 'Observación de la Tierra', 'ar': 'رصد الأرض', 'it': 'Osservazione della Terra', 'he': 'תצפית על כדור הארץ'},
    'forests': {'en': 'Forests', 'fr': 'Forêts', 'es': 'Bosques', 'ar': 'الغابات', 'it': 'Foreste', 'he': 'יערות'},
}
EMOJI = {'space-weather': '☀️', 'ocean': '🌊', 'earth-observation': '🌍', 'forests': '🌳'}
HUB_FILE = {
    'space-weather': 'Space_Weather.html',
    'ocean': 'Oceans.html',
    'earth-observation': 'Earth_Observation.html',
    'forests': 'Deforestation.html',
}
HUB_ID = {h: 'hub-' + h for h in HUB_FILE}
VOL_ID = {h: 'vol-hub-' + h for h in HUB_FILE}
NEW_COUNTS = {'space-weather': 14, 'ocean': 52, 'earth-observation': 50, 'forests': 43}
TR = {}

NSO_OVER = 'https://nso.edu/telescopes/dkist/fact-sheets/dkist-overview/'
NSO_HOME = 'https://nso.edu/telescopes/inouye-solar-telescope/'
NSO_BLOG = 'https://nso.edu/blog/tiny-explosions-big-discoveries-the-inouye-solar-telescope-uncovers-hidden-sparkles-on-the-sun/'
NSO_SW = 'https://nso.edu/telescopes/dkist/fact-sheets/dkist-space-weather/'
NOAA_GRID = 'https://www.spaceweather.gov/impacts/electric-power-transmission'
MM_NEAR = 'https://malamamaunalua.org/nearshore/'
MM_PDF = 'https://malamamaunalua.org/wp-content/uploads/2025-Malama-Maunalua-Annual-Report.pdf'
MM_CN = 'https://www.charitynavigator.org/ein/364671116'
MM_GIVE = 'https://www.paypal.com/donate/?hosted_button_id=2FSFWCXMK3RGS'
MM_VOL = 'https://malamamaunalua.org/volunteer/'
MLO = 'https://gml.noaa.gov/obop/mlo/'
TRENDS = 'https://gml.noaa.gov/ccgg/trends/'
AGGI = 'https://gml.noaa.gov/aggi/aggi.html'
EPA_O3 = 'https://www.epa.gov/ozone-layer-protection/health-and-environmental-effects-ozone-layer-depletion'
DLNR = 'https://dlnr.hawaii.gov/blog/2019/02/05/nr19-024/'
GOV = 'https://governor.hawaii.gov/newsroom/dlnr-news-release-albatross-thriving-at-40-year-old-kaena-point-natural-area-reserve/'
YOUNG = 'https://pacificrimconservation.org/wp-content/uploads/2024/11/Young-et-al-2024-albatrosses-on-Oahu.pdf'
PLOS = 'https://doi.org/10.1371/journal.pone.0023601'
UNESCO = 'https://whc.unesco.org/en/list/1182/'
NOAA_SEAL = 'https://www.fisheries.noaa.gov/species/hawaiian-monk-seal'

def src(name, url):
    return f'<p class="fact-source">Source: <a href="{E(url)}" target="_blank" rel="noopener">{E(name)}</a></p>'

def page_main(p):
    ws = []
    for key, label in [('who', 'Who'), ('what', 'What'), ('when', 'When'), ('where', 'Where'), ('why', 'Why')]:
        bits = ''.join(f'<p>{E(t)}</p>' for t in p[key]['text']) + ''.join(src(n, u) for n, u in p[key]['sources'])
        ws.append(f'<div class="w-card"><h3>{label}</h3>{bits}</div>')
    eli = ''.join(f'<li>{E(t)}</li>' for t in p['eli'])
    sources = ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in p['sources'])
    nsrc = f'{len(p["sources"])} source cited' if len(p["sources"]) == 1 else f'{len(p["sources"])} sources cited'
    credit = f'<p class="photo-credit">{E(p["credit"])} <a href="{E(p["credit_url"])}" target="_blank" rel="noopener">Source</a>.</p>'
    if p.get('donate'):
        reviewed = ('<!-- REVIEWED:START --><div class="review-row"><p class="page-reviewed" aria-label="Page review and sources" data-pagefind-ignore>'
                    f'<span class="rv-label">Last reviewed:</span> <time datetime="2026-11">November 2026</time><span aria-hidden="true"> · </span><a href="#sources">{nsrc}</a></p>'
                    '<a class="btn help-btn return-wth" href="Ways_to_Help.html#donate">Return to Ways to Help</a></div><!-- REVIEWED:END -->')
        support = (f'<section class="five-ws help-cta" id="support"><h2>Support {E(p["title"])}</h2><div class="help-btns">'
                   f'<a class="btn help-btn" data-sp-donate="1" href="{E(p["donate"])}" target="_blank" rel="noopener">Donate</a>'
                   f'<a class="btn help-btn" href="{E(p["volunteer"])}" target="_blank" rel="noopener">Volunteer</a>'
                   f'<a class="btn help-btn" href="Ways_to_Help.html#roll-up-your-sleeves">Roll up your sleeves</a></div>'
                   f'<p>{E(p["donate_why"])} {E(p["showcase"])}</p></section>')
        helpb = (f'<section class="help-actions" id="help" aria-label="Ways to help"><h2>Help This Work</h2><p>{E(p["help"])} {E(p["showcase"])}</p><div class="help-btns">'
                 f'<a class="btn help-btn" data-sp-donate="1" href="{E(p["donate"])}" target="_blank" rel="noopener">Donate</a>'
                 f'<a class="btn help-btn" href="{E(p["volunteer"])}" target="_blank" rel="noopener">Volunteer</a>'
                 f'<a class="btn help-btn" href="Ways_to_Help.html#roll-up-your-sleeves">Roll up your sleeves</a></div>'
                 f'<p class="help-more"><a href="Ways_to_Help.html">See all ways to help</a></p></section>')
    else:
        reviewed = ('<!-- REVIEWED:START --><p class="page-reviewed" aria-label="Page review and sources" data-pagefind-ignore>'
                    f'<span class="rv-label">Last reviewed:</span> <time datetime="2026-11">November 2026</time><span aria-hidden="true"> · </span><a href="#sources">{nsrc}</a></p><!-- REVIEWED:END -->')
        support = (f'<section class="five-ws help-cta" id="support"><h2>Learn About {E(p["title"])}</h2><div class="help-btns">'
                   f'<a class="btn help-btn" href="{E(p["official"])}" target="_blank" rel="noopener">{E(p["button"])}</a></div>'
                   f'<p>{E(p["nodeonate"])} {E(p["showcase"])}</p></section>')
        helpb = (f'<section class="help-actions" id="help" aria-label="Ways to help"><h2>Help This Work</h2><p>{E(p["help"])} {E(p["showcase"])}</p><div class="help-btns">'
                 f'<a class="btn help-btn" href="{E(p["official"])}" target="_blank" rel="noopener">{E(p["button"])}</a>'
                 f'<a class="btn help-btn" href="Ways_to_Help.html#roll-up-your-sleeves">Roll up your sleeves</a></div>'
                 f'<p class="help-more"><a href="Ways_to_Help.html">See all ways to help</a></p></section>')
    return f'''<section class="page-hero space-hero" style="background-image:linear-gradient(rgba(0,20,40,.35),rgba(0,20,40,.62)),url('{p["img"]}');background-size:cover;background-position:center 42%"><div class="page-hero-content"><h1>{E(p["title"])}</h1><p>{E(p["blurb"])}</p></div></section>
{credit}
<nav aria-label="Breadcrumb" class="breadcrumb" hidden><ol><li><a href="index.html">Home</a></li><li><a href="{p["hub_file"]}">{E(HUBNAME[p["hub"]]["en"])}</a></li><li><span aria-current="page">{E(p["title"])}</span></li></ol></nav>
{reviewed}
<!-- ELI10:START --><section class="eli10" id="eli10" aria-labelledby="eli10-h"><h2 id="eli10-h"><span class="eli10-icon" aria-hidden="true">💡</span> Explain Like I'm 10</h2><ul>{eli}</ul></section><!-- ELI10:END -->
<section class="five-ws" id="solution"><h2>The Five W's of {E(p["title"])}</h2><div class="ws-grid">{''.join(ws)}</div></section>
<style>details.src-fold{{max-width:1100px;margin:.4rem auto 0;padding:0 1.5rem}}details.src-fold>summary{{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center;font-size:1.25rem}}details.src-fold ul{{margin:.2rem 0 1rem;padding-inline-start:1.2rem;line-height:1.55}}details.src-fold a{{text-decoration:underline;text-underline-offset:.12em}}details.src-fold>summary:focus-visible{{outline:3px solid #f5b400;outline-offset:3px}}</style>
<details class="src-fold" id="sources"><summary>Sources</summary><p>{E(p["every"])}</p><ul>{sources}</ul></details>
<section class="impact" id="impact"><h2>Impact Statement</h2><div class="impact-box"><p class="hub-label">{E(p["label"])}</p><p>{E(p["impact"])}</p>{''.join(src(n, u) for n, u in p["impact_src"])}</div></section>
<section class="impact saves-planets" id="saves"><h2>How This Saves People &amp; the Planet</h2><div class="impact-box"><h3 class="mission-title">For People</h3><p>{E(p["people"])}</p>{src(*p["people_src"])}<h3 class="mission-title">For Nature</h3><p>{E(p["nature"])}</p>{src(*p["nature_src"])}</div></section>
{support}
<section class="next-solutions" aria-label="Explore another solution"><h2>Next: Explore Another Solution</h2><ul>{''.join(f'<li><a href="{E(h)}">{E(n)}</a></li>' for n, h in p["next"])}</ul></section>
{helpb}
'''

SHOW = 'Saving Planets is showcasing this work, not partnering with it.'
EVERY = 'Every fact on this page comes from one of these public pages.'
NODON = 'There is no donate button, because this is a public agency or public body.'

PAGES = [
 dict(
    file='Inouye_Solar_Telescope.html', title='Inouye Solar Telescope', hub='space-weather',
    hub_file='Space_Weather.html', anchor='INSAT-3DS.html', hub_anchor='Solar_Orbiter.html',
    region='americas', glass='space', tint='sun', klass='agency',
    img='assets/Inouye_DKIST_Haleakala.jpg', w=1600, h=1067,
    alt='The Daniel K. Inouye Solar Telescope near the summit of Haleakalā on Maui',
    credit='Photo: NSF/NSO/AURA, CC BY 4.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:DKIST_near_the_summit_of_Haleakal%C4%81.jpg',
    blurb="From atop Haleakalā, the Inouye Solar Telescope's 4-meter mirror gathers 7 times more sunlight than any other solar telescope to map the magnetic fields that drive space weather.",
    label='Agency solution · active',
    eli=["The Inouye Solar Telescope is a giant telescope on a mountain in Hawaiʻi that looks at the Sun.",
         "Its 4-meter mirror gathers 7 times more sunlight than any other solar telescope.",
         "It watches the magnetic changes that drive space weather, so forecasts can get better."],
    who=dict(text=["The National Science Foundation's Daniel K. Inouye Solar Telescope is built and run by the National Solar Observatory. This telescope is a public observatory."],
             sources=[('NSO, DKIST overview', NSO_OVER)]),
    what=dict(text=["The mirror is 4 meters (13 feet) across, the largest of any solar telescope. It sees features three times smaller than anything seen on the Sun before, and it can do that several times a second."],
              sources=[('NSO, DKIST overview', NSO_OVER), ('NSO, Inouye Solar Telescope', NSO_HOME)]),
    when=dict(text=["Construction began in 2010, and the first images came in late 2019. It is expected to run at least 44 years, through four solar cycles, into the 2060s. On November 20, 2026, scientists reported 14 tiny Ellerman bomb explosions powered by magnetic reconnection."],
              sources=[('NSO, DKIST overview', NSO_OVER), ('NSO, tiny explosions on the Sun, November 20, 2026', NSO_BLOG)]),
    where=dict(text=["It sits at 10,000 feet on Haleakalā, Maui. The base facility is in Pukalani, and the data center is at the National Solar Observatory in Boulder."],
               sources=[('NSO, DKIST overview', NSO_OVER)]),
    why=dict(text=["The telescope measures the Sun's smallest magnetic changes. Scientists can then compare space-weather models with real observations at the same scale and refine the forecasts."],
             sources=[('NSO, DKIST and space weather', NSO_SW)]),
    impact="A 4-meter telescope on Haleakalā gathers 7 times more sunlight than any other solar telescope and watches the magnetic fields that drive space weather.",
    impact_src=[('NSO, DKIST overview', NSO_OVER)],
    people="Better forecasts help protect power grids, satellites, and the GPS that first responders, pilots, and farmers rely on. NOAA records a nine-hour blackout in Canada, with a transformer loss, in March 1989.",
    people_src=('NOAA, electric power transmission', NOAA_GRID),
    nature="The telescope measures the Sun's smallest magnetic changes, so models of space weather can be checked against the real Sun.",
    nature_src=('NSO, DKIST and space weather', NSO_SW),
    official=NSO_HOME, button='Read the NSO page',
    ways="The Inouye Solar Telescope's 4-meter mirror gathers 7 times more sunlight than any other solar telescope.",
    help='The National Solar Observatory runs this public telescope.',
    next=[('Solar Orbiter (ESA / NASA)', 'Solar_Orbiter.html'), ('SOHO Solar and Heliospheric Observatory (ESA / NASA)', 'SOHO.html'), ('SOLAR-1 (NOAA)', 'SOLAR_1.html')],
    sources=[('NSO, DKIST overview', NSO_OVER), ('NSO, Inouye Solar Telescope', NSO_HOME),
             ('NSO, tiny explosions on the Sun, November 20, 2026', NSO_BLOG), ('NSO, DKIST and space weather', NSO_SW),
             ('NOAA, electric power transmission', NOAA_GRID)],
 ),
 dict(
    file='Malama_Maunalua.html', title='Mālama Maunalua', hub='ocean',
    hub_file='Oceans.html', anchor='Mesoamerican_Reef_Insurance.html', hub_anchor='Hawaii_Wildlife_Fund.html',
    region='americas', glass='ocean', tint='water', klass='nonprofit',
    img='assets/Maunalua_Bay_NASA.jpg', w=1600, h=1065,
    alt='Maunalua Bay on Oʻahu, photographed from the International Space Station',
    credit='Photo: NASA/Tim Kopra, public domain.',
    credit_url='https://commons.wikimedia.org/wiki/File:Maunalua_Bay.jpg',
    blurb="Mālama Maunalua volunteers have pulled more than 4 million pounds of invasive algae from Oʻahu's Maunalua Bay and turned it into soil for local farms.",
    label='Nonprofit solution · active',
    eli=["Mālama Maunalua is a community group on Oʻahu that pulls invasive algae out of Maunalua Bay.",
         "Volunteers have pulled more than 4 million pounds, and the algae is recycled as soil for local farms.",
         "Clearing the algae gives native seagrass, algae, and coral room to grow back."],
    who=dict(text=["Mālama Maunalua is a community nonprofit, EIN 36-4671116, working to restore Maunalua Bay on Oʻahu."],
             sources=[('Mālama Maunalua, nearshore restoration', MM_NEAR), ('Charity Navigator, EIN 36-4671116', MM_CN)]),
    what=dict(text=["More than 4 million pounds of invasive alien algae have been pulled from the bay. The algae is recycled as soil amendment at local farms. About 3,000 volunteers, including 1,000 students, join more than 30 community work days every year. The work focuses on the 28 or more acres of Paikō beach."],
              sources=[('Mālama Maunalua, nearshore restoration', MM_NEAR)]),
    when=dict(text=["In 2025 the group removed 65,154 pounds of invasive limu, created 3,102 coral fragments, restored 18,000 square meters, and counted 3,971 volunteers."],
              sources=[('Mālama Maunalua, 2025 annual report', MM_PDF)]),
    where=dict(text=["The bay is on Oʻahu, Hawaiʻi. Over 90 percent of the coastal land around Maunalua is paved or roofed, which feeds the runoff that fuels the algae. That is why the group also works from ridge to reef."],
               sources=[('Mālama Maunalua, 2025 annual report', MM_PDF)]),
    why=dict(text=["Invasive algae grows over and smothers coral reefs and native algae. Pulling it clears space for native seagrass, algae, and coral. The pulled algae then becomes soil for local farms."],
             sources=[('Mālama Maunalua, nearshore restoration', MM_NEAR)]),
    impact="Volunteers have pulled more than 4 million pounds of invasive algae from Maunalua Bay and recycled it as soil for local farms.",
    impact_src=[('Mālama Maunalua, nearshore restoration', MM_NEAR)],
    people="About 3,000 volunteers a year, including 1,000 students, do the pulling. The algae they remove becomes soil amendment at local farms.",
    people_src=('Mālama Maunalua, nearshore restoration', MM_NEAR),
    nature="Pulling the algae clears space for native seagrass, algae, and coral to come back.",
    nature_src=('Mālama Maunalua, nearshore restoration', MM_NEAR),
    official='https://malamamaunalua.org/', button='Read the Mālama Maunalua page',
    donate=MM_GIVE, volunteer=MM_VOL,
    donate_why='Charity Navigator rates Mālama Maunalua Four-Star. It is a 501(c)(3), EIN 36-4671116, and its 2024 Form 990 reports financial statements audited by an independent accountant.',
    ways='Volunteers have pulled more than 4 million pounds of invasive algae from Maunalua Bay.',
    help='Donations go to Mālama Maunalua through the PayPal button on its own site. Saving Planets does not receive the money.',
    next=[('Hawaiʻi Wildlife Fund', 'Hawaii_Wildlife_Fund.html'), ('Hawaiian Monk Seal Recovery', 'Hawaiian_Monk_Seal_Recovery.html'), ('Papahānaumokuākea National Marine Sanctuary', 'Papahanaumokuakea.html')],
    sources=[('Mālama Maunalua, nearshore restoration', MM_NEAR), ('Mālama Maunalua, 2025 annual report', MM_PDF), ('Charity Navigator, EIN 36-4671116', MM_CN)],
 ),
 dict(
    file='Mauna_Loa_Observatory.html', title='NOAA Mauna Loa Observatory', hub='earth-observation',
    hub_file='Earth_Observation.html', anchor='Meteosat_Third_Generation.html', hub_anchor='OCO-2.html',
    region='americas', glass='earth', tint='air', klass='agency',
    img='assets/Mauna_Loa_Observatory_NOAA.jpg', w=1600, h=877,
    alt='NOAA Mauna Loa Observatory on the north flank of Mauna Loa',
    credit='Photo: Christine Smith/NOAA, public domain.',
    credit_url='https://commons.wikimedia.org/wiki/File:NOAA_Mauna_Loa_Observatory.png',
    blurb="Since 1958, Hawaiʻi's Mauna Loa Observatory has kept the world's longest direct record of carbon dioxide in the air; it read 426.69 ppm in October 2026.",
    label='Agency solution · active',
    eli=["Mauna Loa Observatory is a NOAA station high on a volcano in Hawaiʻi that measures the air.",
         "It has the world's longest direct record of carbon dioxide, started in 1958.",
         "In October 2026 the monthly average was 426.69 ppm. The same network also shows that ozone-harming gases fell after the world agreed to control them."],
    who=dict(text=["NOAA's Global Monitoring Laboratory runs the observatory. A staff of 8, based in Hilo, works there. It also hosts the World Dobson Ozone Calibration Centre."],
             sources=[('NOAA, Mauna Loa Observatory', MLO)]),
    what=dict(text=["NOAA calls it the premier long-term atmospheric monitoring facility on Earth. Carbon dioxide measurements began in March 1958 with C. David Keeling of Scripps. They are the longest record of direct carbon dioxide measurements in the atmosphere."],
              sources=[('NOAA, Mauna Loa Observatory', MLO), ('NOAA, trends in atmospheric carbon dioxide', TRENDS)]),
    when=dict(text=["The monthly average carbon dioxide was 426.69 ppm in October 2026, up from 424.87 ppm in October 2025. NOAA last updated that trends page on November 19, 2026. A temporary access road was completed on March 26, 2026, after the 2022 eruption cut the old road."],
              sources=[('NOAA, trends in atmospheric carbon dioxide', TRENDS), ('NOAA, Mauna Loa Observatory', MLO)]),
    where=dict(text=["The observatory sits at 3,397 meters (11,135 feet) on the north flank of Mauna Loa, on Hawaiʻi Island."],
               sources=[('NOAA, Mauna Loa Observatory', MLO)]),
    why=dict(text=["The same network tracks ozone-depleting gases. It shows that CFC and HCFC emissions fell sharply after global controls under the Montreal Protocol. A healing ozone layer means less UVB. EPA links extra UVB to melanoma, other skin cancers, and cataracts."],
             sources=[('NOAA, Annual Greenhouse Gas Index', AGGI), ('EPA, health effects of ozone layer depletion', EPA_O3)]),
    impact="Since 1958, Mauna Loa Observatory has kept the longest direct record of carbon dioxide in the air. The October 2026 average was 426.69 ppm.",
    impact_src=[('NOAA, trends in atmospheric carbon dioxide', TRENDS)],
    people="A healing ozone layer means less UVB. EPA links extra UVB to melanoma, other skin cancers, and cataracts.",
    people_src=('EPA, health effects of ozone layer depletion', EPA_O3),
    nature="NOAA's record shows that CFC and HCFC emissions fell sharply after the Montreal Protocol. That is measured proof the ozone treaty is working.",
    nature_src=('NOAA, Annual Greenhouse Gas Index', AGGI),
    official=MLO, button='Read the NOAA page',
    ways='Mauna Loa Observatory has measured carbon dioxide in the air since 1958. The October 2026 average was 426.69 ppm.',
    help='NOAA runs this public observatory.',
    next=[('OCO-2 Orbiting Carbon Observatory (NASA)', 'OCO-2.html'), ('MicroCarb', 'MicroCarb.html'), ('SMOS: Soil Moisture and Ocean Salinity (ESA)', 'SMOS.html')],
    sources=[('NOAA, Mauna Loa Observatory', MLO), ('NOAA, trends in atmospheric carbon dioxide', TRENDS),
             ('NOAA, Annual Greenhouse Gas Index', AGGI), ('EPA, health effects of ozone layer depletion', EPA_O3)],
 ),
 dict(
    file='Kaena_Point_Fence.html', title='Kaʻena Point Predator-Proof Fence', hub='forests',
    hub_file='Deforestation.html', anchor='Kakapo_Recovery.html', hub_anchor='Kakapo_Recovery.html',
    region='americas', glass='forest', tint='green', klass='agency',
    img='assets/Kaena_Point_Albatross.jpg', w=1200, h=675,
    alt='A Laysan albatross beside dark lava rock at Kaʻena Point',
    credit='Photo: H20story / Wikimedia Commons, CC BY-SA 4.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Laysan_Albatross_Ka%CA%BBena_Point_State_Park.jpg',
    blurb="A 59-acre predator-proof fence at Oʻahu's Kaʻena Point helped albatross reach a record 106 breeding pairs and more than tripled shearwater chicks.",
    label='Agency solution · active',
    eli=["Kaʻena Point is a wild corner of Oʻahu with a fence that keeps out cats, rats, and mongoose.",
         "Inside the 59 acres, albatross reached a record 106 breeding pairs, and shearwater chicks more than tripled.",
         "More chicks survive, and keeping cats out also lowers a disease risk for endangered monk seals."],
    who=dict(text=["Hawaiʻi's Department of Land and Natural Resources runs Kaʻena Point Natural Area Reserve. The fence, finished in 2011, was the first landscape-scale predator-proof fence of its kind in the United States."],
             sources=[('Hawaiʻi DLNR, February 5, 2019', DLNR)]),
    what=dict(text=["The fence encloses 59 acres. Before it, dogs, cats, mongoose, rats, and mice preyed on seabirds and native plants. Cats also spread toxoplasmosis, which can kill monk seals."],
              sources=[('Hawaiʻi DLNR, February 5, 2019', DLNR)]),
    when=dict(text=["In the 2018 season, 106 albatross pairs tried to breed, a record, and wedge-tailed shearwater chicks more than tripled in seven years. In the 2023 season there were 98 albatross nests, the second-highest ever."],
              sources=[('Hawaiʻi DLNR, February 5, 2019', DLNR), ('Hawaiʻi DLNR, via the Governor’s newsroom', GOV)]),
    where=dict(text=["The reserve is at Kaʻena Point on Oʻahu. A peer-reviewed study says the new colonies sit high on the island and can serve as refuges as the sea rises."],
               sources=[('Young and others, Pacific Science, 2024', YOUNG)]),
    why=dict(text=["Fencing at Kaʻena in 2011 and at Kuaokalā in 2021 raised albatross chick fledging success from 0.60 to 0.80. That is an estimated 69 extra chicks. Oʻahu had 875 adult Laysan albatross in 2023. Keeping cats out also cuts the toxoplasmosis risk to endangered monk seals that rest on the point."],
             sources=[('Young and others, Pacific Science, 2024', YOUNG), ('Hawaiʻi DLNR, February 5, 2019', DLNR), ('NOAA Fisheries, Hawaiian monk seal', NOAA_SEAL)]),
    impact="A 59-acre predator-proof fence helped albatross at Kaʻena Point reach a record 106 breeding pairs, and shearwater chicks more than tripled.",
    impact_src=[('Hawaiʻi DLNR, February 5, 2019', DLNR)],
    people="Cats at the point spread toxoplasmosis, which can kill monk seals. The fence keeps those cats out.",
    people_src=('Hawaiʻi DLNR, February 5, 2019', DLNR),
    nature="Fledging success for albatross chicks rose from 0.60 to 0.80 after the fences at Kaʻena and Kuaokalā. The colonies sit high on Oʻahu, where they can serve as refuges as the sea rises.",
    nature_src=('Young and others, Pacific Science, 2024', YOUNG),
    official=DLNR, button='Read the DLNR page',
    ways='A 59-acre fence at Kaʻena Point helped albatross reach 106 breeding pairs.',
    help="Hawaiʻi's Department of Land and Natural Resources runs this public reserve.",
    next=[('Kākāpō Recovery (New Zealand)', 'Kakapo_Recovery.html'), ('Redonda Island Restoration', 'Redonda_Restoration.html'), ('Hawaiian Monk Seal Recovery', 'Hawaiian_Monk_Seal_Recovery.html')],
    sources=[('Hawaiʻi DLNR, February 5, 2019', DLNR), ('Hawaiʻi DLNR, via the Governor’s newsroom', GOV),
             ('Young and others, Pacific Science, 2024', YOUNG), ('NOAA Fisheries, Hawaiian monk seal', NOAA_SEAL)],
 ),
 dict(
    file='Cabo_Pulmo.html', title='Cabo Pulmo National Park', hub='ocean',
    hub_file='Oceans.html', anchor='Copernicus_Marine.html', hub_anchor='Papahanaumokuakea.html',
    region='americas', glass='ocean', tint='water', klass='agency',
    img='assets/Cabo_Pulmo_Angelfish.jpg', w=1600, h=1067,
    alt='A king angelfish on the reef at Cabo Pulmo, Baja California Sur',
    credit='Photo: Diego Delso, delso.photo, CC BY-SA 4.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Pez_%C3%A1ngel_real_(Holacanthus_passer),_Cabo_Pulmo,_Baja_California,_M%C3%A9xico,_2024-12-19,_DD_25.jpg',
    blurb='After fishing stopped at Mexico\'s Cabo Pulmo, fish biomass grew 463% in ten years (1999–2009).',
    label='Agency solution · active',
    eli=["Cabo Pulmo is a national park in Mexico where the community stopped fishing inside the reef.",
         "From 1999 to 2009, the weight of fish there grew by 463 percent.",
         "Top predators increased 11-fold. Families who used to fish now earn a living from visitors who come to see a living reef."],
    who=dict(text=["Cabo Pulmo National Park was created in 1995. A peer-reviewed study calls it the only well-enforced no-take area in the Gulf of California, largely thanks to local community support."],
             sources=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS)]),
    what=dict(text=["Fish biomass rose from 0.75 to 4.24 tonnes per hectare between 1999 and 2009, an increase of 463 percent. Top predators increased 11-fold and carnivores 4-fold over the same decade."],
              sources=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS)]),
    when=dict(text=["The park dates from 1995. The published biomass comparison covers 1999 to 2009. Locally owned small-scale tourism earned 538,800 U.S. dollars in 2006, as cited in that study."],
              sources=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS)]),
    where=dict(text=["The park is in Baja California Sur, Mexico. It is part of the Islands and Protected Areas of the Gulf of California, a UNESCO World Heritage site of 244 islands, islets, and coastal areas, with 891 fish species, 90 of them endemic. UNESCO has listed that wider site as World Heritage in Danger since 2019."],
               sources=[('UNESCO, Islands and Protected Areas of the Gulf of California', UNESCO)]),
    why=dict(text=["No-take protection let the fish rebuild. A full reef became the draw for locally owned dive and snorkel tourism. Former fishing families earn a living from a living reef instead of an emptied one."],
             sources=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS)]),
    impact='Fish biomass at Cabo Pulmo grew 463 percent in ten years after the no-take park was enforced, from 0.75 to 4.24 tonnes per hectare.',
    impact_src=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS)],
    people='Locally owned small-scale tourism earned 538,800 U.S. dollars in 2006. The study ties that income to the recovered reef.',
    people_src=('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS),
    nature='Top predators increased 11-fold and carnivores 4-fold from 1999 to 2009 inside this no-take area.',
    nature_src=('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS),
    official=UNESCO, button='Read the UNESCO listing',
    ways='Fish biomass at Cabo Pulmo grew 463 percent in the ten years after fishing stopped.',
    help='Cabo Pulmo is a Mexican national park.',
    next=[('Papahānaumokuākea National Marine Sanctuary', 'Papahanaumokuakea.html'), ('Tubbataha Reefs Natural Park', 'Tubbataha_Reefs.html'), ('Palau National Marine Sanctuary', 'Palau_National_Marine_Sanctuary.html')],
    sources=[('Aburto-Oropeza and others, PLoS ONE, 2011', PLOS), ('UNESCO, Islands and Protected Areas of the Gulf of California', UNESCO)],
 ),
]

for p in PAGES:
    p['every'] = EVERY
    p['showcase'] = SHOW
    p['nodeonate'] = NODON

def collect_strings(p):
    out = [p['title'], p['blurb'], p['alt'], p['credit'], p['impact'], p['people'], p['nature'], p['help'], p['button'], p['ways'], p['label'], p['every'], p['showcase']]
    if not p.get('donate'):
        out.append(p['nodeonate'])
    else:
        out.append(p['donate_why'])
    out += p['eli']
    for key in ('who', 'what', 'when', 'where', 'why'):
        out += p[key]['text']
        out += [n for n, u in p[key]['sources']]
    out += [n for n, u in p['sources']]
    out += [n for n, u in p['impact_src']]
    out += [n for n, h in p['next']]
    return out

def strings_needed():
    need = []
    for p in PAGES:
        for s in collect_strings(p):
            if s not in TR and s not in need:
                need.append(s)
    return need

def write_english():
    shell = open('Hawaiian_Monk_Seal_Recovery.html', encoding='utf8').read()
    a, b = shell.find('<section class="page-hero'), shell.find('</main>')
    assert a > 0 and b > a
    for p in PAGES:
        page = shell[:a] + page_main(p) + shell[b:]
        page = page.replace('Hawaiian_Monk_Seal_Recovery.html', p['file'])
        for lang in LANGS:
            page = page.replace(f'href="{lang}/index.html"', f'href="{lang}/{p["file"]}"')
        old_title = 'Hawaiian Monk Seal Recovery'
        page = page.replace(f'<title>{old_title} | Saving Planets</title>', f'<title>{E(p["title"])} | Saving Planets</title>')
        page = page.replace(f'content="{old_title} | Saving Planets"', f'content="{E(p["title"])} | Saving Planets"')
        old_desc = 'NOAA Fisheries estimates about 1,600 Hawaiian monk seals, and up to 30 percent of those alive today are alive because of direct recovery work.'
        page = page.replace(old_desc, E(p['blurb']))
        page = page.replace('content="Hawaiian, Monk, Seal, Recovery, NOAA, Fisheries, estimates, about"', f'content="{E(p["title"])}, Saving Planets"')
        page = page.replace('https://www.savingplanets.com/assets/Hawaiian_Monk_Seal_NOAA.jpg', 'https://www.savingplanets.com/' + p['img'])
        page = page.replace('content="750"', f'content="{p["w"]}"')
        page = page.replace('content="500"', f'content="{p["h"]}"')
        page = page.replace('A Hawaiian monk seal and her pup resting on a sandy beach beside the ocean', E(p['alt']))
        page = page.replace('content="ocean"', f'content="{p["hub"]}"')
        page = page.replace('content="agency"', f'content="{p["klass"]}"')
        page = page.replace('content="2026-11-09"', f'content="{TODAY}"')
        page = page.replace('hp-hawaiian-monk-seal-recovery toc-sub hawaiian-monk-seal-recovery-page', f'hp-{p["file"][:-5].lower().replace("_", "-")} toc-sub')
        page = page.replace('data-glass="ocean"', f'data-glass="{p["glass"]}"')
        page = page.replace('data-glass-tint="water"', f'data-glass-tint="{p["tint"]}"')
        page = page.replace(old_title, p['title'])
        page = page.replace('Hawaiian%20Monk%20Seal%20Recovery', urllib.parse.quote(p['title'], safe=''))
        cites = ','.join('{"@type": "CreativeWork", "url": "%s"}' % u for n, u in p['sources'])
        page = re.sub(r'"citation": \[.*?\]', '"citation": [' + cites + ']', page, count=1, flags=re.S)
        if 'hreflang="fr"' not in page:
            block = '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="https://www.savingplanets.com/{lang}/{p["file"]}">' for lang in LANGS)
            page = page.replace(
                f'<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/{p["file"]}">',
                block + '\n<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/' + p['file'] + '">')
        page = page.replace('What is ' + p['title'] + ', and what problem does it work on?', 'What is ' + p['title'] + ', and what problem does it help solve?')
        page = page.replace('Which number on this page surprised you, and which source supports it?', 'Who is behind ' + p['title'] + ', and where does the work happen?')
        page = page.replace('How does this work help people, and how does it help nature?', 'How does ' + p['title'] + ' help both people and nature? Use one fact from this page.')
        open(p['file'], 'w', encoding='utf8').write(page)
        print('wrote', p['file'], 'leftover monk', page.lower().count('monk seal'))

def card_sol(p, lang):
    ui = UI[lang]
    pre = '' if lang == 'en' else '../'
    def L(s):
        return s if lang == 'en' else TR.get(s, {}).get(lang, s)
    return (f'<article class="card sol-card" data-url="{p["file"]}" data-new="{TODAY}" data-status="active" data-region="{p["region"]}" data-grades="6-8">'
            f'<div class="image-container"><a class="photo-link" href="{p["file"]}"><img width="{p["w"]}" height="{p["h"]}" src="{pre}{p["img"]}" alt="{E(L(p["alt"]))}" loading="lazy" decoding="async"></a></div>'
            f'<p class="photo-credit sol-credit"><span>{ui["image"]}</span> <bdi>{E(L(p["credit"]))}</bdi></p>'
            f'<p class="sol-badges"><span class="status-badge status-new" data-new-until="{UNTIL}" style="{BADGE}">{ui["new"]}</span></p>'
            f'<h3><a href="{p["file"]}">{E(L(p["title"]))}</a></h3><p class="sol-desc"><span>{E(L(p["blurb"]))}</span></p></article>')

def card_hub(p, lang):
    ui = UI[lang]
    pre = '' if lang == 'en' else '../'
    def L(s):
        return s if lang == 'en' else TR.get(s, {}).get(lang, s)
    return (f'<article class="card"><div class="image-container"><a class="photo-link" href="{p["file"]}"><img src="{pre}{p["img"]}" alt="{E(L(p["alt"]))}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async"></a></div>'
            f'<p class="sol-badges"><span class="status-badge status-active">{ui["active"]}</span>'
            f'<span class="status-badge status-new" data-new-until="{UNTIL}" style="{BADGE}">{ui["new"]}</span>'
            f'<span class="hub-tag"><span aria-hidden="true">{EMOJI[p["hub"]]}</span> {E(HUBNAME[p["hub"]][lang])}</span></p>'
            f'<h3><a href="{p["file"]}">{E(L(p["title"]))}</a></h3><p class="card-blurb">{E(L(p["blurb"]))}</p></article>')

def card_ways(p, lang):
    def L(s):
        return s if lang == 'en' else TR.get(s, {}).get(lang, s)
    return (f'<li class="wh-card"><h3>{E(L(p["title"]))}</h3><p>{E(L(p["ways"]))}</p>'
            f'<a class="wh-s" href="{p["file"]}">{E(L(p["title"]))}</a>'
            f'<a class="btn help-btn wh-c" href="{E(p["official"])}" target="_blank" rel="noopener">{E(L(p["button"]))}'
            f'<span class="sr-only"> – {E(L(p["title"]))}</span></a></li>')

def card_donate(p, lang):
    def L(s):
        return s if lang == 'en' else TR.get(s, {}).get(lang, s)
    donate = 'Donate' if lang == 'en' else TR.get('Donate', {}).get(lang, 'Donate')
    how = 'How we check a Donate link' if lang == 'en' else TR.get('How we check a Donate link', {}).get(lang, 'How we check a Donate link')
    reviewed = 'Last reviewed:' if lang == 'en' else TR.get('Last reviewed:', {}).get(lang, 'Last reviewed:')
    nsrc = f'{len(p["sources"])} sources cited'
    nsrc_l = nsrc if lang == 'en' else TR.get(nsrc, {}).get(lang, nsrc)
    return (f'<li class="wh-card"><a class="wh-card-go" href="{p["file"]}"><h3>{E(L(p["title"]))}</h3><p>{E(L(p["ways"]))}</p><span class="wh-s">{E(L(p["title"]))}</span></a>'
            f'<a class="btn help-btn" data-sp-donate="1" href="{E(p["donate"])}" target="_blank" rel="noopener">{E(donate)}'
            f'<span class="sr-only"> – {E(L(p["title"]))}</span></a>'
            f'<p class="vet-line"><span class="vet-rev">{E(reviewed)} <time datetime="2026-11">November 2026</time></span> '
            f'<span aria-hidden="true">·</span> <a href="{p["file"]}#sources">{E(nsrc_l)}</a> '
            f'<span aria-hidden="true">·</span> <a class="vet-how" href="How_We_Evaluate.html#s3">{E(how)}</a></p></li>')

def insert_before(html, anchor_file, snippet, marker):
    if f'href="{marker}"' in html or f'data-url="{marker}"' in html:
        return html
    i = html.find(f'href="{anchor_file}"')
    if i < 0:
        raise SystemExit('anchor missing ' + anchor_file)
    j = html.rfind('<article', 0, i)
    if j < 0:
        raise SystemExit('article missing before ' + anchor_file)
    return html[:j] + snippet + html[j:]

def bump_sol_c(html, hub_id, new_n):
    return re.sub(r'(href="#' + hub_id + r'">[^<]*<span class="sol-c">)\d+(</span>)',
                  lambda m: m.group(1) + str(new_n) + m.group(2), html, count=1)

def add_ways(html, hub_id, snippet, add_n, marker):
    i = html.find(f'id="{hub_id}"')
    if i < 0:
        raise SystemExit('ways hub missing ' + hub_id)
    window = html[i:i + 120000]
    if f'href="{marker}"' in window:
        return html
    j = html.find('<ul class="wh-grid">', i)
    chunk = html[i:j]
    chunk2, n = re.subn(r'(<span class="wh-n">)(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + add_n), chunk, count=1)
    if n != 1:
        raise SystemExit('wh-n missing ' + hub_id)
    html = html[:i] + chunk2 + html[j:]
    j = html.find('<ul class="wh-grid">', i)
    k = j + len('<ul class="wh-grid">')
    return html[:k] + snippet + html[k:]

def wire_listings():
    by_hub = {}
    for p in PAGES:
        by_hub.setdefault(p['hub'], []).append(p)
    for lang in [None] + LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        path = pref + 'Solutions.html'
        s = open(path, encoding='utf8').read()
        for p in PAGES:
            s = insert_before(s, p['anchor'], card_sol(p, code), p['file'])
        for hub, n in NEW_COUNTS.items():
            s = bump_sol_c(s, HUB_ID[hub], n)
        s = re.sub(r'(?<![\d,])' + str(OLD_TOTAL) + r'(?!\d)', str(TOTAL), s)
        open(path, 'w', encoding='utf8').write(s)
        for hub, items in by_hub.items():
            path = pref + HUB_FILE[hub]
            s = open(path, encoding='utf8').read()
            for p in items:
                s = insert_before(s, p['hub_anchor'], card_hub(p, code), p['file'])
            open(path, 'w', encoding='utf8').write(s)
        path = pref + 'Ways_to_Help.html'
        s = open(path, encoding='utf8').read()
        for hub, items in by_hub.items():
            snip = ''.join(card_ways(p, code) for p in items)
            s = add_ways(s, VOL_ID[hub], snip, len(items), items[0]['file'])
        donors = [p for p in PAGES if p.get('donate')]
        if donors:
            s = add_ways(s, 'don-hub-ocean', ''.join(card_donate(p, code) for p in donors), len(donors), donors[0]['file'])
        open(path, 'w', encoding='utf8').write(s)
        print('wired', code)

def wire_counts_and_home():
    for lang in [None] + LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        pre = '' if lang is None else '../'
        path = pref + 'index.html'
        s = open(path, encoding='utf8').read()
        s = s.replace(f'class="imp-num">{OLD_TOTAL}<', f'class="imp-num">{TOTAL}<')
        s = re.sub(r'(?<![\d,])' + str(OLD_TOTAL) + r'(?!\d)', str(TOTAL), s)
        i = s.find('<!-- NEW-STRIP:START -->')
        j = s.find('<!-- NEW-STRIP:END -->')
        if i < 0 or j < 0:
            raise SystemExit('strip missing ' + path)
        block = s[i:j]
        block = block.replace('>5 new ', '>10 new ').replace('>5 nouvelles ', '>10 nouvelles ').replace('>5 soluciones ', '>10 soluciones ')
        block = block.replace('أُضيفت 5 حلول', 'أُضيفت 10 حلول').replace('>5 nuove ', '>10 nuove ').replace('>5 פתרונות', '>10 פתרונות')
        items = ''.join(
            f'<li><time datetime="{TODAY}">{""}</time> '
            for p in [])  # placeholder to keep the editor quiet
        def title(p):
            return p['title'] if code == 'en' else TR.get(p['title'], {}).get(code, p['title'])
        # reuse the date text already in the strip
        m = re.search(r'<time datetime="2026-11-23">([^<]+)</time>', block)
        date = m.group(1) if m else TODAY
        extra = ''.join(f'<li><time datetime="{TODAY}">{date}</time> <a href="{pre}{p["file"]}">{E(title(p))}</a></li>' for p in PAGES)
        block = block.replace('</ul>', extra + '</ul>', 1)
        s = s[:i] + block + s[j:]
        open(path, 'w', encoding='utf8').write(s)
        cpath = pref + 'Changelog.html'
        c = open(cpath, encoding='utf8').read()
        c = c.replace(' (5)</h3>', ' (10)</h3>', 1)
        lis = ''.join(f'<li><a href="{pre}{p["file"]}">{E(title(p))}</a></li>' for p in PAGES)
        mark = f'datetime="{TODAY}">'
        k = c.find(mark)
        ul = c.find('<ul>', k)
        if p_file_present(c, PAGES[0]['file']):
            pass
        else:
            c = c[:ul + 4] + lis + c[ul + 4:]
        open(cpath, 'w', encoding='utf8').write(c)

def p_file_present(text, filename):
    return f'href="{filename}"' in text or f'href="../{filename}"' in text

def wire_data():
    added = json.load(open('assets/data/solution-added.json', encoding='utf8'))
    for p in PAGES:
        added[p['file']] = TODAY
    json.dump(added, open('assets/data/solution-added.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    s = open('assets/data/solutions.json', encoding='utf8').read()
    s = s.replace(f'"solutions": {OLD_TOTAL},', f'"solutions": {TOTAL},', 1)
    s = s.replace(f'"taggedSolutions": {OLD_TOTAL}', f'"taggedSolutions": {TOTAL}', 1)
    s = s.replace('"name": "Space Weather & Shields",\n   "solutions": 13,', '"name": "Space Weather & Shields",\n   "solutions": 14,')
    s = s.replace('"name": "Earth Observation",\n   "solutions": 49,', '"name": "Earth Observation",\n   "solutions": 50,')
    s = s.replace('"name": "Forests",\n   "solutions": 42,', '"name": "Forests",\n   "solutions": 43,')
    s = s.replace('"name": "Ocean",\n   "solutions": 50,', '"name": "Ocean",\n   "solutions": 52,')
    for p in PAGES:
        if '"href": "%s"' % p['file'] in s:
            continue
        needle = '    {\n     "href": "%s",' % p['anchor']
        ins = '    {\n     "href": "%s",\n     "name": "%s"\n    },\n    {\n     "href": "%s",' % (p['file'], p['title'].replace('"', ''), p['anchor'])
        if needle not in s:
            raise SystemExit('menu anchor missing ' + p['anchor'])
        s = s.replace(needle, ins)
    objs = []
    for p in PAGES:
        if '"url": "%s"' % p['file'] in s:
            continue
        objs.append('''  {
   "url": "%s",
   "title": "%s",
   "category": "%s",
   "type": "solution",
   "classification": "%s",
   "status": "active",
   "stats": [],
   "missions": [],
   "added": "%s"
  }''' % (p['file'], p['title'], p['hub'], p['klass'], TODAY))
    if objs:
        s = s.replace('''   "added": "2026-11-23"
  }
 ]
}''', '''   "added": "2026-11-23"
  },
''' + ',\n'.join(objs) + '''
 ]
}''')
    json.loads(s)
    open('assets/data/solutions.json', 'w', encoding='utf8').write(s)
    for fn in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(fn, encoding='utf8').read().splitlines()
        for p in PAGES:
            if p['file'] not in lines:
                lines.append(p['file'])
        open(fn, 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    block_src = open('sitemap-en.xml', encoding='utf8').read()
    i = block_src.find('<url><loc>https://www.savingplanets.com/Lake_Washington_Cleanup.html</loc>')
    j = block_src.find('</url>', i) + len('</url>')
    sample = block_src[i:j]
    for lang, prefix in [('en', ''), ('fr', 'fr/'), ('es', 'es/'), ('ar', 'ar/'), ('it', 'it/'), ('he', 'he/')]:
        path = f'sitemap-{lang}.xml'
        sm = open(path, encoding='utf8').read()
        for p in PAGES:
            if f'/{prefix}{p["file"]}' in sm or (lang == 'en' and f'/{p["file"]}' in sm and f'/fr/{p["file"]}' not in sm[sm.find(p['file'])-4:sm.find(p['file'])+2]):
                # still add if this language loc is absent
                loc = f'https://www.savingplanets.com/{prefix}{p["file"]}'
                if f'<loc>{loc}</loc>' in sm:
                    continue
            entry = sample.replace('Lake_Washington_Cleanup.html', p['file'])
            entry = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', entry, count=1)
            if lang != 'en':
                entry = entry.replace(f'<loc>https://www.savingplanets.com/{p["file"]}</loc>', f'<loc>https://www.savingplanets.com/{prefix}{p["file"]}</loc>', 1)
            sm = sm.replace('</urlset>', '  ' + entry + '\n</urlset>')
        open(path, 'w', encoding='utf8').write(sm)
    g = json.load(open('assets/data/glossary.json', encoding='utf8'))
    for t in g['terms']:
        if t['id'] == 'carbon-dioxide' and 'anidride carbonica' not in t['it']['match']:
            t['it']['match'].append('anidride carbonica')
    if not any(t['id'] == 'no-take' for t in g['terms']):
        g['terms'].append({
            'id': 'no-take',
            'en': {'term': 'No-take area', 'match': ['no-take area', 'no-take park'], 'def': 'A protected place where fishing and taking marine life are not allowed.'},
            'fr': {'term': 'Zone sans prélèvement', 'match': ['zone sans prélèvement'], 'def': 'Un lieu protégé où la pêche et le prélèvement d’êtres marins sont interdits.'},
            'es': {'term': 'Zona de no extracción', 'match': ['zona de no extracción'], 'def': 'Un lugar protegido donde no se permite pescar ni extraer vida marina.'},
            'ar': {'term': 'منطقة ممنوع فيها الأخذ', 'match': ['منطقة ممنوع فيها الأخذ'], 'def': 'مكان محمي لا يُسمح فيه بالصيد ولا بأخذ الكائنات البحرية.'},
            'it': {'term': 'Area no-take', 'match': ['area no-take'], 'def': 'Un luogo protetto dove non è permesso pescare né prelevare vita marina.'},
            'he': {'term': 'אזור ללא דיג', 'match': ['אזור ללא דיג'], 'def': 'מקום מוגן שבו אסור לדוג או לקחת יצורים מהים.'},
            'source': PLOS,
        })
    json.dump(g, open('assets/data/glossary.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)

def merge_i18n():
    import importlib.util
    existing = {lang: json.load(open(f'i18n/{lang}.json', encoding='utf8')) for lang in LANGS}
    shared = ['Donate', 'How we check a Donate link', 'Last reviewed:', 'November 2026',
              '2 sources cited', '3 sources cited', '4 sources cited', '5 sources cited']
    for s in list(strings_needed()) + shared:
        if s not in TR and all(existing[lang].get(s) for lang in LANGS):
            TR[s] = {lang: existing[lang][s] for lang in LANGS}
    spec = importlib.util.spec_from_file_location('tr1123e', 'scripts/batch-1123e-tr.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for en, tr in mod.EXTRA.items():
        TR.setdefault(en, {}).update(tr)
    missing = strings_needed()
    if missing:
        json.dump(missing, open('/tmp/batch-1123e-missing.json', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
        print('MISSING', len(missing))
        for s in missing:
            print(' -', s[:140])
        raise SystemExit(1)
    for lang in LANGS:
        path = f'i18n/{lang}.json'
        data = json.load(open(path, encoding='utf8'))
        n = 0
        for en, tr in TR.items():
            if lang in tr and tr[lang] and data.get(en) != tr[lang]:
                data[en] = tr[lang]
                n += 1
        for p in PAGES:
            title = TR.get(p['title'], {}).get(lang, p['title'])
            en_apa = f'Saving Planets. (2026). {p["title"]}. https://www.savingplanets.com/{p["file"]}'
            data[en_apa] = f'Saving Planets. (2026). {title}. https://www.savingplanets.com/{lang}/{p["file"]}'
            en_mla = f'"{p["title"]}." Saving Planets, https://www.savingplanets.com/{p["file"]}.'
            q = f'« {title} »' if lang == 'fr' else f'"{title}"'
            data[en_mla] = f'{q}. Saving Planets{"،" if lang == "ar" else ","} https://www.savingplanets.com/{lang}/{p["file"]}.'
            nsrc = f'{len(p["sources"])} sources cited'
            # leave pattern translator to handle "{n} sources cited" if the exact key is absent
        text = json.dumps(data, ensure_ascii=False, indent=0) + '\n'
        open(path, 'w', encoding='utf8').write(text)
        print(lang, 'updated', n)

def translate():
    import importlib.util
    spec = importlib.util.spec_from_file_location('i18n_build', 'scripts/i18n-build.py')
    i18n_build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(i18n_build)
    i18n_build.PAGES = [l.strip() for l in open('i18n/pages.txt', encoding='utf8') if l.strip() and not l.startswith('#')]
    files = [p['file'] for p in PAGES]
    for lang in LANGS:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        i18n_build.CUR_PAGES = i18n_build.L10N.pages_for(lang, i18n_build.PAGES)
        for f in files:
            i18n_build.build(f, lang, m)
        print('built', lang)

def tooltips():
    import importlib.util
    spec = importlib.util.spec_from_file_location('bb', 'scripts/build-batch-b.py')
    bb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bb)
    bb.GLOSS_LABEL['he'] = 'מילון'
    g = json.load(open('assets/data/glossary.json', encoding='utf8'))
    for lang in [None] + LANGS:
        code = 'en' if lang is None else lang
        bb.GL = [t for t in g['terms'] if code in t and 'match' in t[code]]
        pref = '' if lang is None else lang + '/'
        for p in PAGES:
            path = pref + p['file']
            s = open(path, encoding='utf8').read()
            s2, n = bb.tooltipify(s, code)
            if s2 != s:
                open(path, 'w', encoding='utf8').write(s2)
                print(' ', path, n)
        gpath = pref + 'Glossary.html'
        page = open(gpath, encoding='utf8').read()
        a = page.find('<!-- GLOSSARY-LIST:START -->')
        b = page.find('<!-- GLOSSARY-LIST:END -->')
        if a > 0 and b > a:
            inner = bb.gl_list(bb.GL, code)
            old_n = page[a:b].count('<dt ')
            new_n = inner.count('<dt ')
            if new_n >= old_n:
                page = page[:a + len('<!-- GLOSSARY-LIST:START -->')] + inner + page[b:]
                open(gpath, 'w', encoding='utf8').write(page)
            else:
                print('skip glossary shrink', code, old_n, new_n)
        print('tips', code)

def main():
    if '--strings' in sys.argv:
        for s in strings_needed():
            print(s)
        return
    merge_i18n()
    write_english()
    translate()
    wire_listings()
    wire_counts_and_home()
    wire_data()
    tooltips()
    print('done', TOTAL)

if __name__ == '__main__':
    main()
