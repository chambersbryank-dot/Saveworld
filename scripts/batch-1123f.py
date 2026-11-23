#!/usr/bin/env python3
"""Nov 23, 2026 batch B: Lake Apopka, CEWH, Working for Water, ESA Space Debris Office, SDO.

Listing 297 -> 302. Created by the Founder and SI.
"""
import importlib.util, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('e', 'scripts/batch-1123e.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)

SJ = 'https://www.sjrwmd.com/projects/lake-apopka-project/'
SJ24 = 'https://www.sjrwmd.com/2024/08/continued-success-in-native-planting-efforts-enhances-lake-apopkas-health/'
CEWH = 'https://www.dcceew.gov.au/cewh/resources-media/news/cewh/20000-gigalitres-counting'
GOVZA = 'https://www.gov.za/news/media-statements/environmental-affairs-working-water-programme-29-oct-2015'
CBD = 'https://www.cbd.int/ecorestoration/doc/casestudy-south-africa-en.pdf'
ESA26 = 'https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2026'
ESA25 = 'https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2025'
AEOLUS = 'https://www.esa.int/Space_Safety/ESA_spacecraft_dodges_large_constellation'
SDO_SC = 'https://sdo.gsfc.nasa.gov/mission/spacecraft.php'
SDO_IN = 'https://sdo.gsfc.nasa.gov/mission/instruments.php'
SDO_MS = 'https://science.nasa.gov/mission/sdo/'
NOAA_GRID = 'https://www.spaceweather.gov/impacts/electric-power-transmission'

e.OLD_TOTAL = 297
e.TOTAL = 302
e.NEW_COUNTS = {'lakes': 20, 'rivers': 29, 'space-disposal': 15, 'space-weather': 15}
e.HUB_FILE.update({
    'lakes': 'Lakes.html', 'rivers': 'Rivers.html', 'space-disposal': 'Space_Disposal.html',
})
e.HUB_ID.update({h: 'hub-' + h for h in ('lakes', 'rivers', 'space-disposal')})
e.VOL_ID.update({h: 'vol-hub-' + h for h in ('lakes', 'rivers', 'space-disposal')})
e.EMOJI.update({'lakes': '🏞️', 'rivers': '💧', 'space-disposal': '🚀'})
e.HUBNAME.update({
    'lakes': {'en': 'Lakes', 'fr': 'Lacs', 'es': 'Lagos', 'ar': 'البحيرات', 'it': 'Laghi', 'he': 'אגמים'},
    'rivers': {'en': 'Rivers', 'fr': 'Rivières', 'es': 'Ríos', 'ar': 'الأنهار', 'it': 'Fiumi', 'he': 'נהרות'},
    'space-disposal': {'en': 'Space Disposal', 'fr': 'Élimination spatiale', 'es': 'Eliminación espacial', 'ar': 'التخلص الفضائي', 'it': 'Smaltimento spaziale', 'he': 'סילוק בחלל'},
})

def _card_href(html, anchor_file):
    """The href that sits inside a card, not a nav or footer link."""
    start = 0
    while True:
        i = html.find(f'href="{anchor_file}"', start)
        if i < 0:
            raise SystemExit('anchor missing ' + anchor_file)
        j = html.rfind('<article', 0, i)
        if j >= 0 and i - j < 4000:
            return i, j
        start = i + 1

def insert_before(html, anchor_file, snippet, marker):
    if f'href="{marker}"' in html or f'data-url="{marker}"' in html:
        return html
    i, j = _card_href(html, anchor_file)
    if marker == 'Working_for_Water.html':
        end = html.find('</article>', i)
        return html[:end + len('</article>')] + snippet + html[end + len('</article>'):]
    return html[:j] + snippet + html[j:]
e.insert_before = insert_before

e.PAGES = [
 dict(
    file='Lake_Apopka_Restoration.html', title='Lake Apopka Restoration', hub='lakes',
    hub_file='Lakes.html', anchor='Lake_Biwa_Soap_Movement.html', hub_anchor='Lake_Biwa_Soap_Movement.html',
    region='americas', glass='water', tint='lakes', klass='agency',
    img='assets/Lake_Apopka.jpg', w=1600, h=1200,
    alt='Lake Apopka in Florida, seen from the air',
    credit='Photo: Michael Adams / Wikimedia Commons, CC BY-SA 3.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Lakeapopka_01212012.jpg',
    blurb="Lake Apopka's restorers cut its phosphorus 66% and brought native underwater plants back to about 95% of its shoreline.",
    label='Agency solution · active',
    eli=["Lake Apopka is a big lake in Florida that got sick from too much phosphorus.",
         "Since the late 1980s, phosphorus is down 66 percent and the water is 52 percent clearer.",
         "Native underwater plants were gone in 1994. By 2024 they lined about 95 percent of the shore."],
    who=dict(text=["The St. Johns River Water Management District runs the restoration. It is a public water district, and the work is a four-decade effort of about 200 million dollars on Florida's fourth-largest lake."],
             sources=[('St. Johns River Water Management District, Lake Apopka project', SJ), ('St. Johns River Water Management District, August 2024', SJ24)]),
    what=dict(text=["About 750,000 pounds of gizzard shad are harvested each year. Since 1993 that harvest has removed more than 274,000 pounds of phosphorus. The 760-acre Marsh Flow-Way filters about 30 percent of the lake's volume each year."],
              sources=[('St. Johns River Water Management District, Lake Apopka project', SJ)]),
    when=dict(text=["As of March 2026, phosphorus is down 66 percent and water clarity is up 52 percent since the late 1980s. In 2022 the annual average phosphorus fell below the target for the first time. Since 2003 the flow-way has removed more than 77,500 tons of suspended solids, 1,500 tons of nitrogen, and 38.9 tons of phosphorus."],
              sources=[('St. Johns River Water Management District, Lake Apopka project', SJ)]),
    where=dict(text=["The lake is in Central Florida. Native underwater plants were absent in 1994. By the 2024 survey they lined about 95 percent of the shoreline."],
               sources=[('St. Johns River Water Management District, Lake Apopka project', SJ)]),
    why=dict(text=["Removing phosphorus starves the algae, and clearer water lets sunlight reach the bottom. The plants that return take up still more phosphorus. Those plants were the habitat behind the lake's once world-class bass fishery."],
             sources=[('St. Johns River Water Management District, Lake Apopka project', SJ), ('St. Johns River Water Management District, August 2024', SJ24)]),
    impact="Phosphorus in Lake Apopka is down 66 percent and native underwater plants now line about 95 percent of the shoreline.",
    impact_src=[('St. Johns River Water Management District, Lake Apopka project', SJ)],
    people="Clearer water and the returning plants rebuild the habitat of a fishery people used, and the recreation that went with it.",
    people_src=('St. Johns River Water Management District, August 2024', SJ24),
    nature="Less phosphorus means less algae. Sunlight reaches the bottom again, and native underwater plants take up still more phosphorus.",
    nature_src=('St. Johns River Water Management District, Lake Apopka project', SJ),
    official=SJ, button='Read the district page',
    ways="Lake Apopka's restorers cut phosphorus 66 percent and brought plants back to about 95 percent of the shore.",
    help='The St. Johns River Water Management District runs this public restoration.',
    next=[('Lake Washington Cleanup (Seattle)', 'Lake_Washington_Cleanup.html'), ('Kissimmee River Restoration (Florida)', 'Kissimmee_River_Restoration.html'), ('Lake Geneva Phosphorus Cleanup', 'Lake_Geneva_CIPEL.html')],
    sources=[('St. Johns River Water Management District, Lake Apopka project', SJ), ('St. Johns River Water Management District, August 2024', SJ24)],
 ),
 dict(
    file='Commonwealth_Environmental_Water_Holder.html', title='Commonwealth Environmental Water Holder', hub='rivers',
    hub_file='Rivers.html', anchor='Cuyahoga_River_Cleanup.html', hub_anchor='Cuyahoga_River_Cleanup.html',
    region='eurafrica', glass='water', tint='rivers', klass='agency',
    img='assets/Murray_River_Boundary_Bend.jpg', w=1600, h=1200,
    alt='The Murray River at Boundary Bend',
    credit='Photo: Scott Davis / Wikimedia Commons, CC BY 2.5.',
    credit_url='https://commons.wikimedia.org/wiki/File:Murray_River_at_Boundary_Bend.jpg',
    blurb="Australia's Commonwealth Environmental Water Holder has returned more than 20,000 gigalitres of water to the Murray–Darling's rivers and wetlands since 2009.",
    label='Agency solution · active',
    eli=["Australia holds some river water just for nature, then lets it flow when rivers and wetlands need it.",
         "Since 2009 that office has delivered 20,099 gigalitres. That is about 20 trillion litres.",
         "The water has reached native fish, 11 Ramsar wetlands, and flushed 4.3 million tonnes of salt."],
    who=dict(text=["The Commonwealth Environmental Water Holder is an Australian Government statutory body. It delivers water to rivers and wetlands in the Murray–Darling Basin."],
             sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)]),
    what=dict(text=["It has delivered 20,099 gigalitres since 2009, about 20 trillion litres, or 8 million Olympic pools. Of that, 15,500 gigalitres supported native fish spawning, migration, and survival."],
              sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)]),
    when=dict(text=["From 2014 to June 2025, flows reached more than 28,500 kilometres of waterways, and more than 470,000 hectares of wetlands, lakes, and floodplains were watered. The count was published on October 23, 2026."],
              sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)]),
    where=dict(text=["The water goes to the Murray–Darling Basin. It has helped 11 Ramsar wetlands and threatened species such as the southern bell frog and the Murray hardyhead. Environmental water made up 90 percent of Barwon–Darling flows in 2017–18."],
               sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)]),
    why=dict(text=["Water held for nature is released to reconnect rivers and floodplains. That triggers native fish spawning and migration and has flushed 4.3 million tonnes of salt. Healthier waterways then support water quality, regional communities, tourism, and the industries that depend on the river."],
             sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)]),
    impact="Since 2009 the office has delivered 20,099 gigalitres of water to the Murray–Darling's rivers and wetlands.",
    impact_src=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)],
    people="DCCEEW says the healthier waterways improve water quality and support regional communities, tourism, and the industries that depend on the river.",
    people_src=('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH),
    nature="The water has supported native fish, 11 Ramsar wetlands, and species such as the southern bell frog, and it has flushed 4.3 million tonnes of salt.",
    nature_src=('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH),
    official=CEWH, button='Read the DCCEEW page',
    ways='The Commonwealth Environmental Water Holder has returned more than 20,000 gigalitres to the Murray–Darling since 2009.',
    help='This is an Australian Government statutory body.',
    next=[('Room for the River (Netherlands)', 'Room_for_the_River.html'), ('Okavango Delta: The River That Ends in a Desert', 'Okavango_Delta.html'), ('Cuyahoga River Cleanup (Ohio)', 'Cuyahoga_River_Cleanup.html')],
    sources=[('DCCEEW, 20,000 gigalitres and counting, October 23, 2026', CEWH)],
 ),
 dict(
    file='Working_for_Water.html', title='Working for Water', hub='rivers',
    hub_file='Rivers.html', anchor='Waterkeeper_Alliance.html', hub_anchor='Waterkeeper_Alliance.html',
    region='eurafrica', glass='water', tint='rivers', klass='agency',
    img='assets/Acacia_mearnsii.jpg', w=1600, h=1067,
    alt='Black wattle, Acacia mearnsii, one of the invasive trees Working for Water clears',
    credit='Photo: SAplants / Wikimedia Commons, CC BY-SA 4.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Acacia_mearnsii_1DS-II_2-0158.jpg',
    blurb='South Africa\'s Working for Water teams cleared over 2.1 million hectares of thirsty invasive plants from 1995 to 2011, adding an estimated 48–56 million cubic meters of water a year.',
    label='Agency solution · active',
    eli=["Working for Water is a South African program that hires people to cut invasive plants that drink up river water.",
         "From 1995 to 2011 the teams cleared over 2.1 million hectares. That is estimated to add 48 to 56 million cubic meters of water a year.",
         "The newest official national totals are from 2015. They are not later guesses."],
    who=dict(text=["Working for Water is a national public-works program of South Africa's Department of Forestry, Fisheries and the Environment. It started on October 16, 1995, with a budget of 25 million rand."],
             sources=[('South African Government, October 29, 2015', GOVZA)]),
    what=dict(text=["About 2.8 million hectares of invasive plants had been treated as of 2015. Working for Water and its sister programs had created more than 227,100 person-years of work, with more than 55,000 job opportunities in the 2014/15 financial year."],
              sources=[('South African Government, October 29, 2015', GOVZA)]),
    when=dict(text=["From 1995 to 2011, teams cleared over 2.1 million hectares. That clearing is estimated to add 48 to 56 million cubic meters of water every year. The 2015 government statement is the newest official national total used here."],
              sources=[('UN Convention on Biological Diversity, Working for Water case study', CBD), ('South African Government, October 29, 2015', GOVZA)]),
    where=dict(text=["The work is across South Africa. The country is semi-arid and water-scarce, and invasive plants reduce stream flow and water yield."],
               sources=[('UN Convention on Biological Diversity, Working for Water case study', CBD)]),
    why=dict(text=["Removing invasive trees that drink up stream flow puts water back into rivers. Hiring jobless people to do the clearing also gives tens of thousands of families an income each year."],
             sources=[('UN Convention on Biological Diversity, Working for Water case study', CBD), ('South African Government, October 29, 2015', GOVZA)]),
    impact="From 1995 to 2011, Working for Water cleared over 2.1 million hectares of invasive plants, estimated to add 48 to 56 million cubic meters of water a year.",
    impact_src=[('UN Convention on Biological Diversity, Working for Water case study', CBD)],
    people="By 2015 the program and its sister programs had created more than 227,100 person-years of work, including more than 55,000 job opportunities in 2014/15.",
    people_src=('South African Government, October 29, 2015', GOVZA),
    nature="Invasive plants reduce stream flow in a water-scarce country. Clearing them is how the program puts water back into rivers.",
    nature_src=('UN Convention on Biological Diversity, Working for Water case study', CBD),
    official=GOVZA, button='Read the 2015 government statement',
    ways='Working for Water cleared over 2.1 million hectares of invasive plants from 1995 to 2011.',
    help='This is a South African government program. The figures stop at the 2015 official statement and the earlier case study.',
    next=[('Room for the River (Netherlands)', 'Room_for_the_River.html'), ('Okavango Delta: The River That Ends in a Desert', 'Okavango_Delta.html'), ('Great Green Wall (African Union / UNCCD)', 'Great_Green_Wall.html')],
    sources=[('South African Government, October 29, 2015', GOVZA), ('UN Convention on Biological Diversity, Working for Water case study', CBD)],
 ),
 dict(
    file='ESA_Space_Debris_Office.html', title='ESA Space Debris Office', hub='space-disposal',
    hub_file='Space_Disposal.html', anchor='Europa_Clipper.html', hub_anchor='Zero_Debris_Charter.html',
    region='eurafrica', glass='space', tint='orbit', klass='agency',
    img='assets/ESA_Optical_Ground_Station.jpg', w=1600, h=1340,
    alt='Operators at ESA’s Optical Ground Station, which observes space debris',
    credit='Photo: ESA, CC BY-SA 3.0 IGO.',
    credit_url='https://commons.wikimedia.org/wiki/File:ESA_Optical_Ground_Station_ESA237927.jpg',
    blurb="ESA's Space Debris Office tracks the crowding of Earth's orbits: in 2025, ten objects launched every day while just over three re-entered.",
    label='Agency solution · active',
    eli=["The Space Debris Office is ESA's team that tracks junk in orbit and says when a satellite should move.",
         "In 2025, about ten objects launched every day, and just over three intact objects re-entered every day.",
         "Its yearly report is one way to see whether the rules, including the Zero Debris Charter, are working."],
    who=dict(text=["ESA's Space Debris Office sits at ESOC in Darmstadt, Germany. It tracks debris, runs collision-risk analysis, and has published a Space Environment Report every year since 2017."],
             sources=[('ESA, Space Environment Report 2026', ESA26)]),
    what=dict(text=["In 2025 there were more than 300 launches and over 4,000 new payloads. About ten objects are launched each day, while more than three intact objects re-enter each day. The 2025 report estimated over 1.2 million debris objects larger than 1 centimetre, each big enough to cause catastrophic damage."],
              sources=[('ESA, Space Environment Report 2026', ESA26), ('ESA, Space Environment Report 2025', ESA25)]),
    when=dict(text=["On September 2, 2019, the office's collision-risk numbers led ESA's first avoidance manoeuvre against a large-constellation satellite. Aeolus raised its orbit by 350 metres when the risk reached about 1 in 1,000, ten times ESA's threshold."],
              sources=[('ESA, Aeolus dodges a large constellation', AEOLUS)]),
    where=dict(text=["The office is in Darmstadt. The telescopes it uses include ESA's Optical Ground Station. Even with no new launches, the debris population would keep growing, because fragmentations create debris faster than it naturally re-enters."],
               sources=[('ESA, Space Environment Report 2026', ESA26)]),
    why=dict(text=["The collision-risk numbers tell ESA when to move a satellite. In 2019 that kept the Aeolus wind-mapping satellite from a possible crash and returned it to normal science operations. The yearly report shows which rules are working, such as 90 percent of rocket bodies in low orbit now leaving under the 25-year rule. That work sits beside the Zero Debris Charter."],
             sources=[('ESA, Aeolus dodges a large constellation', AEOLUS), ('ESA, Space Environment Report 2025', ESA25)]),
    impact="In 2025 about ten objects launched every day while just over three intact objects re-entered. The office is the team that counts that gap.",
    impact_src=[('ESA, Space Environment Report 2026', ESA26)],
    people="Keeping orbits usable protects the weather, navigation, and Earth-watching satellites people rely on. In 2019 the office's warning moved Aeolus out of a possible crash.",
    people_src=('ESA, Aeolus dodges a large constellation', AEOLUS),
    nature="Space debris keeps growing even if launches stop, because fragments appear faster than they fall back. The yearly report is the public check on that, and on the Zero Debris Charter.",
    nature_src=('ESA, Space Environment Report 2026', ESA26),
    official=ESA26, button='Read the 2026 report',
    ways="ESA's Space Debris Office counted about ten objects launched a day in 2025, and just over three re-entering.",
    help='The office is part of ESA, an intergovernmental agency. Its page links to the Zero Debris Charter.',
    next=[('Zero Debris Charter (ESA)', 'Zero_Debris_Charter.html'), ('Aeolus Assisted Reentry (ESA)', 'Aeolus.html'), ('ClearSpace', 'ClearSpace.html')],
    sources=[('ESA, Space Environment Report 2026', ESA26), ('ESA, Space Environment Report 2025', ESA25), ('ESA, Aeolus dodges a large constellation', AEOLUS)],
 ),
 dict(
    file='Solar_Dynamics_Observatory.html', title='Solar Dynamics Observatory', hub='space-weather',
    hub_file='Space_Weather.html', anchor='Solar_Orbiter.html', hub_anchor='Solar_Orbiter.html',
    region='americas', glass='space', tint='sun', klass='agency',
    img='assets/SDO_Sun_PIA26681.jpg', w=1600, h=1600,
    alt='The Sun photographed by NASA’s Solar Dynamics Observatory',
    credit='Photo: NASA/GSFC/Solar Dynamics Observatory, public domain.',
    credit_url='https://commons.wikimedia.org/wiki/File:Image_of_Sun_From_NASA%E2%80%99s_Solar_Dynamics_Observatory_(PIA26681).jpg',
    blurb="NASA's Solar Dynamics Observatory has photographed the Sun in 10 wavelengths every 10 seconds since 2010 to learn what drives space weather.",
    label='Agency solution · active',
    eli=["The Solar Dynamics Observatory is a NASA satellite that watches the Sun almost all the time.",
         "Since 2010 it has photographed the Sun in 10 wavelengths every 10 seconds.",
         "Those pictures show how flares and eruptions build. That is what drives space weather."],
    who=dict(text=["NASA's Solar Dynamics Observatory is the first mission of the Living With a Star program. It studies how solar activity is created and how it drives space weather, by watching the Sun's interior, atmosphere, magnetic field, and energy output."],
             sources=[('NASA, Solar Dynamics Observatory', SDO_MS)]),
    what=dict(text=["The spacecraft weighs 3,100 kilograms and sends a continuous science downlink of 130 megabits per second. Its Atmospheric Imaging Assembly photographs the Sun in 10 wavelengths every 10 seconds."],
              sources=[('NASA, SDO spacecraft', SDO_SC), ('NASA, SDO instruments', SDO_IN)]),
    when=dict(text=["It launched on February 11, 2010, on an Atlas V from Cape Canaveral."],
              sources=[('NASA, SDO spacecraft', SDO_SC)]),
    where=dict(text=["SDO watches the Sun from Earth orbit, almost without a break."],
               sources=[('NASA, SDO spacecraft', SDO_SC)]),
    why=dict(text=["Its nonstop images show how flares and eruptions build, which is what drives space weather. Storms from the Sun can disrupt the power grid. NOAA cites a nine-hour blackout in Canada in March 1989 and a Swedish blackout in 2003. No official source used here says NOAA forecasters use these images every day, so this page stops at what the mission measures."],
             sources=[('NASA, Solar Dynamics Observatory', SDO_MS), ('NOAA, electric power transmission', NOAA_GRID)]),
    impact="Since 2010, SDO has photographed the Sun in 10 wavelengths every 10 seconds to learn what drives space weather.",
    impact_src=[('NASA, SDO instruments', SDO_IN), ('NASA, Solar Dynamics Observatory', SDO_MS)],
    people="The measurements show how flares and eruptions build. Storms of that kind have caused a nine-hour blackout in Canada in 1989 and a blackout in Sweden in 2003.",
    people_src=('NOAA, electric power transmission', NOAA_GRID),
    nature="SDO watches the Sun's interior, atmosphere, magnetic field, and energy output, which is the chain that drives space weather around Earth.",
    nature_src=('NASA, Solar Dynamics Observatory', SDO_MS),
    official=SDO_MS, button='Read the NASA page',
    ways='Since 2010, the Solar Dynamics Observatory has photographed the Sun in 10 wavelengths every 10 seconds.',
    help='NASA runs this public satellite.',
    next=[('Inouye Solar Telescope', 'Inouye_Solar_Telescope.html'), ('Solar Orbiter (ESA / NASA)', 'Solar_Orbiter.html'), ('SOHO Solar and Heliospheric Observatory (ESA / NASA)', 'SOHO.html')],
    sources=[('NASA, Solar Dynamics Observatory', SDO_MS), ('NASA, SDO spacecraft', SDO_SC), ('NASA, SDO instruments', SDO_IN), ('NOAA, electric power transmission', NOAA_GRID)],
 ),
]
for p in e.PAGES:
    p['every'] = e.EVERY
    p['showcase'] = e.SHOW
    p['nodeonate'] = e.NODON

# Point the translation loader at this batch.
_merge = e.merge_i18n
def merge_i18n():
    src = open('scripts/batch-1123e.py', encoding='utf8').read()
    # loader path is hardcoded; swap for this call by loading f-tr into e.TR first
    import importlib.util as iu
    spec = iu.spec_from_file_location('trf', 'scripts/batch-1123f-tr.py')
    mod = iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # temporarily make e's merge see these strings by writing them over the e loader
    # Call the original after stuffing EXTRA into a stand-in module name.
    real = open('scripts/batch-1123e-tr.py', encoding='utf8').read()
    try:
        open('scripts/batch-1123e-tr.py', 'w', encoding='utf8').write(open('scripts/batch-1123f-tr.py', encoding='utf8').read())
        _merge()
    finally:
        open('scripts/batch-1123e-tr.py', 'w', encoding='utf8').write(real)
e.merge_i18n = merge_i18n

def wire_home():
    for lang in [None] + e.LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        pre = '' if lang is None else '../'
        path = pref + 'index.html'
        s = open(path, encoding='utf8').read()
        s = s.replace('class="imp-num">297<', 'class="imp-num">302<')
        s = re.sub(r'(?<![\d,])297(?!\d)', '302', s)
        i = s.find('<!-- NEW-STRIP:START -->')
        j = s.find('<!-- NEW-STRIP:END -->')
        block = s[i:j]
        block = block.replace('>10 new ', '>15 new ').replace('>10 nouvelles ', '>15 nouvelles ').replace('>10 soluciones ', '>15 soluciones ')
        block = block.replace('أُضيفت 10 حلول', 'أُضيفت 15 حلول').replace('>10 nuove ', '>15 nuove ').replace('>10 פתרונות', '>15 פתרונות')
        m = re.search(r'<time datetime="2026-11-23">([^<]+)</time>', block)
        date = m.group(1)
        def title(p):
            return p['title'] if code == 'en' else e.TR.get(p['title'], {}).get(code, p['title'])
        extra = ''.join(f'<li><time datetime="2026-11-23">{date}</time> <a href="{pre}{p["file"]}">{e.E(title(p))}</a></li>' for p in e.PAGES)
        if e.PAGES[0]['file'] not in block:
            block = block.replace('</ul>', extra + '</ul>', 1)
        s = s[:i] + block + s[j:]
        open(path, 'w', encoding='utf8').write(s)
        cpath = pref + 'Changelog.html'
        c = open(cpath, encoding='utf8').read()
        if f'href="{pre}{e.PAGES[0]["file"]}"' not in c:
            c = c.replace(' (10)</h3>', ' (15)</h3>', 1)
            k = c.find('datetime="2026-11-23">')
            ul = c.find('<ul>', k)
            lis = ''.join(f'<li><a href="{pre}{p["file"]}">{e.E(title(p))}</a></li>' for p in e.PAGES)
            c = c[:ul + 4] + lis + c[ul + 4:]
            open(cpath, 'w', encoding='utf8').write(c)

def wire_data():
    added = json.load(open('assets/data/solution-added.json', encoding='utf8'))
    for p in e.PAGES:
        added[p['file']] = '2026-11-23'
    json.dump(added, open('assets/data/solution-added.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    s = open('assets/data/solutions.json', encoding='utf8').read()
    s = s.replace('"solutions": 297,', '"solutions": 302,', 1)
    s = s.replace('"taggedSolutions": 297', '"taggedSolutions": 302', 1)
    s = s.replace('"name": "Lakes",\n   "solutions": 19,', '"name": "Lakes",\n   "solutions": 20,')
    s = s.replace('"name": "Rivers",\n   "solutions": 27,', '"name": "Rivers",\n   "solutions": 29,')
    s = s.replace('"name": "Space Weather & Shields",\n   "solutions": 14,', '"name": "Space Weather & Shields",\n   "solutions": 15,')
    for p in e.PAGES:
        if '"href": "%s"' % p['file'] in s:
            continue
        if p['file'] == 'Working_for_Water.html':
            i = s.find('"href": "Waterkeeper_Alliance.html"')
            if i < 0:
                raise SystemExit('waterkeeper menu missing')
            j = s.find('\n   ]', i)
            k = s.rfind('}', i, j)
            ins = ',\n    {\n     "href": "Working_for_Water.html",\n     "name": "Working for Water"\n    }'
            s = s[:k + 1] + ins + s[k + 1:]
            continue
        needle = '    {\n     "href": "%s",' % p['anchor']
        ins = '    {\n     "href": "%s",\n     "name": "%s"\n    },\n    {\n     "href": "%s",' % (p['file'], p['title'], p['anchor'])
        if needle not in s:
            raise SystemExit('menu anchor missing ' + p['anchor'])
        s = s.replace(needle, ins, 1)
    objs = []
    for p in e.PAGES:
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
   "added": "2026-11-23"
  }''' % (p['file'], p['title'], p['hub'], p['klass']))
    if objs:
        s = s.replace('''   "added": "2026-11-23"
  }
 ]
}''', '''   "added": "2026-11-23"
  },
''' + ',\n'.join(objs) + '''
 ]
}''', 1)
    json.loads(s)
    open('assets/data/solutions.json', 'w', encoding='utf8').write(s)
    for fn in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(fn, encoding='utf8').read().splitlines()
        for p in e.PAGES:
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
        for p in e.PAGES:
            loc = f'https://www.savingplanets.com/{prefix}{p["file"]}'
            if f'<loc>{loc}</loc>' in sm:
                continue
            entry = sample.replace('Lake_Washington_Cleanup.html', p['file'])
            entry = re.sub(r'<lastmod>[^<]+</lastmod>', '<lastmod>2026-11-23</lastmod>', entry, count=1)
            if lang != 'en':
                entry = entry.replace(f'<loc>https://www.savingplanets.com/{p["file"]}</loc>', f'<loc>{loc}</loc>', 1)
            sm = sm.replace('</urlset>', '  ' + entry + '\n</urlset>')
        open(path, 'w', encoding='utf8').write(sm)

def main():
    if '--strings' in sys.argv:
        for s in e.strings_needed():
            print(s)
        return
    e.merge_i18n()
    e.write_english()
    e.translate()
    e.wire_listings()
    wire_home()
    wire_data()
    e.tooltips()
    print('done', e.TOTAL)

if __name__ == '__main__':
    main()
