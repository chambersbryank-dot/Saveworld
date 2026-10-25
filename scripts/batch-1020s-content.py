#!/usr/bin/env python3
"""Oct 20 2026 batch (owner approved all 19, A-S, Oct 20): South Georgia Habitat Restoration, Arctic Weather Satellite +
EPS-Sterna, GCOM-W SHIZUKU, SCISAT, Chilika Lake, Tonle Sap, Lake Biwa Soap Movement, Lake Constance, Room for the River,
Tubbataha Reefs, Sargassum Watch, Redonda, Iberian lynx, Trees for Life, Nepal tigers, Altyn Dala saiga, Gorongosa, NEOSSat,
Chandrayaan-5/LUPEX. Same writer as batch-1019-content.py (Surfrider_Foundation.html skeleton via batch-1018/1017, BLUF box,
Five W's, widgets after the Five W's, Connected Solutions, XLINK1020S blocks on existing pages). Every fact was re-opened at
build time (2026-10-20); org/agency figures are labeled as theirs. No invented donate partners: where none is verified the
page links a learn/support page. Re-runnable: overwrites only these pages, their hub cards (added once) and XLINK1020S blocks."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b19', os.path.join(ROOT, 'scripts/batch-1019-content.py'))
b19 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b19)
W, see_block, body = b19.W, b19.see_block, b19.body
ADDED = '2026-10-20'

SGH = ('https://sght.org/habitat-restoration-project/', 'South Georgia Heritage Trust, Habitat Restoration Project')
SGHD = 'https://sght.org/donate/'
FOSGI = 'https://www.fosgi.org/donate'
AWSF = ('https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/Arctic_Weather_Satellite/Facts_and_figures', 'ESA, Arctic Weather Satellite facts and figures')
AWSC = ('https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/Arctic_Weather_Satellite/Arctic_Weather_Satellite_paves_way_for_constellation', 'ESA, Arctic Weather Satellite paves way for constellation')
EUM = ('https://www.eumetsat.int/europe-backs-transformative-polar-satellite-constellation-2026', 'EUMETSAT, Europe backs transformative polar satellite constellation')
GCW = ('https://global.jaxa.jp/projects/sat/gcom_w/', 'JAXA, GCOM-W "SHIZUKU"')
GCW12 = ('https://global.jaxa.jp/press/2012/08/20120825_arctic_sea_e.html', 'JAXA, Arctic sea ice extent smallest in observation history (Aug. 2012)')
SCI = ('https://www.asc-csa.gc.ca/eng/satellites/scisat/about.asp', 'Canadian Space Agency, About SCISAT')
SCIDP = ('https://www.asc-csa.gc.ca/eng/publications/dp-2026-2027.asp', 'Canadian Space Agency, 2026-27 Departmental Plan')
CHE = ('https://www.chilika.com/eco-restoration.php', 'Chilika Development Authority, Eco-restoration')
CHD = ('https://www.newindianexpress.com/states/odisha/2025/Mar/13/census-puts-dolphin-number-in-odisha-at-710-rajnagar-tops-list', 'The New Indian Express, Odisha dolphin census 2024-25 (March 2025)')
TSM = ('https://www.unesco.org/en/mab/tonle-sap', 'UNESCO Man and the Biosphere Programme, Tonle Sap')
BIW = ('https://www.pref.shiga.lg.jp/biwakatsu/handbook_en/106515.html', 'Shiga Prefecture, Think about life by seeing Lake Biwa')
IGP = ('https://www.igkb.org/medien/faktenblaetter/phosphor-im-bodensee-oktober-2018', 'IGKB, Phosphor im Bodensee (fact sheet)')
IGW = ('https://www.igkb.org/medien/faktenblaetter/wasserentnahme-aus-dem-bodensee', 'IGKB, Wasserentnahme aus dem Bodensee (fact sheet)')
RFR = ('https://www.rijkswaterstaat.nl/en/projects/iconic-structures/room-for-the-river', 'Rijkswaterstaat, Room for the River')
TUB = ('https://whc.unesco.org/en/list/653/', 'UNESCO World Heritage Centre, Tubbataha Reefs Natural Park')
TUBO = ('https://worldheritageoutlook.iucn.org/node/1062', 'IUCN World Heritage Outlook, Tubbataha Reefs Natural Park')
SAWS = ('https://optics.marine.usf.edu/projects/saws.html', 'USF Optical Oceanography Lab, Sargassum Watch System')
SAWN = ('https://www.usf.edu/marine-science/news/2019/scientists-discover-the-biggest-seaweed-bloom-in-the-world.aspx', 'USF College of Marine Science, Scientists discover the biggest seaweed bloom in the world (2019)')
RED = ('https://www.fauna-flora.org/news/to-the-moonscape-and-back-rejuvenated-redonda-granted-protected-area-status/', 'Fauna & Flora, Rejuvenated Redonda granted protected area status (Sept. 2023)')
EAGD = 'https://4agc.com/donation_pages/c68ec3bb-41da-4d34-8211-53f90f59fd83'  # Oct 24: eagantigua.org now serves an unrelated casino site; EAG moved to eagantigua.net, whose Donate button goes to this BirdsCaribbean-processed page
LYN = ('https://www.miteco.gob.es/es/prensa/ultimas-noticias/2026/junio/la-poblacion-de-lince-iberico-alcanzo-los-2-663-ejemplares-en-20.html', 'MITECO, Iberian lynx population reached 2,663 in 2025 (June 2026)')
TFL = ('https://treesforlife.org.uk/about-us/annual-review-2023-24/', 'Trees for Life, Annual Review 2023-24')
TFLD = 'https://treesforlife.org.uk/support/donate/'
NTN = ('https://ntnc.org.np/news/historical-day-tiger-conservation-nepal-first-country-double-its-tiger-population', 'NTNC, Nepal is the first country to double its tiger population (July 2022)')
SAI = ('https://altyndala.org/results-from-the-2024-saiga-aerial-census-in-kazakhstan-are-in/', 'Altyn Dala Conservation Initiative, 2024 saiga aerial census results')
SAIP = ('https://altyndala.org/partnership/', 'Altyn Dala Conservation Initiative, Our partnership')
GOR = ('https://gorongosa.org/wp-content/uploads/2024/11/GorongosaAerialWildlifeCount-October-2024.pdf', 'Stalmans & Peel, Aerial wildlife count of Gorongosa National Park, October 2024')
GORD = 'https://gorongosa.org/donate/'
GORH = ('https://gorongosa.org/wp-content/uploads/2025/04/04-24-2025-SMALL-ENG-GORONGOSA-HIGHLIGHTS-copy.pdf', 'Gorongosa Restoration Project, 2024 annual highlights')
NEO = ('https://www.asc-csa.gc.ca/eng/satellites/neossat/', 'Canadian Space Agency, NEOSSat')
LPX = ('https://www.exploration.jaxa.jp/e/program/lunarpolar/', 'JAXA, Lunar Polar Exploration Mission (LUPEX)')
CH3 = ('https://www.isro.gov.in/Chandrayaan3.html', 'ISRO, Chandrayaan-3')
CITSCI = 'https://science.nasa.gov/citizen-science/'

def pin(lat, lng, label, strip=None):
    d = {'status': 'active', 'pins': [{'lat': lat, 'lng': lng, 'label': label, 'basis': 'page'}]}
    if strip: d['strip'] = strip
    return d

PAGES = [
 dict(slug='South_Georgia_Habitat_Restoration', title='South Georgia Habitat Restoration', short='the Habitat Restoration Project', cat='polar',
  hub=('Polar.html', 'Polar'), cls='nonprofit', status='active', glass='earth', label='Nonprofit solution · completed, now guarding the island',
  img=('South_Georgia_ISS071_E_581850.jpg', 1920, 1280, 'Snow-covered South Georgia Island in the South Atlantic, photographed from the International Space Station'),
  credit='NASA (ISS071-E-581850, astronaut photograph of South Georgia Island, Sept. 1, 2024)',
  hook="The world's biggest rat hunt gave a whole island back to its seabirds.",
  wow=("The project covered 108,723 hectares, more than eight times larger than any rodent eradication area tackled before (SGHT).", SGH),
  lead='Two charities raised £10 million to clear rats and mice from South Georgia, and on 8 May 2018 the island was declared rodent-free (SGHT).',
  eli=['Long ago, ships brought rats and mice to South Georgia, an island near Antarctica.',
       'The rats ate the eggs and chicks of birds that nest on the ground.',
       'A team spread bait across the whole island, and in 2018 it was declared free of rats and mice.'],
  ws=[('Who', 'The South Georgia Heritage Trust, a Scottish charity, and its US partner, Friends of South Georgia Island.', SGH),
      ('What', 'The Habitat Restoration Project: removing invasive rats and mice from the entire island so native birds can nest again.', SGH),
      ('When', 'Baiting in 2011, 2013 and 2015, a full survey in 2017-18, and the rodent-free declaration on 8 May 2018.', SGH),
      ('Where', 'South Georgia, a UK Overseas Territory in the South Atlantic Ocean.', SGH),
      ('Why', 'Rats had devastated the island\'s bird populations for two centuries, and retreating glaciers were opening paths to the last rat-free areas.', SGH)],
  impact=('South Georgia was declared free of rodents for the first time since humans arrived over 200 years ago (SGHT).', SGH),
  fact=('Dogs on Patrol', 'Three rodent detection dogs covered 2,420 km searching for any sign of rats and mice (SGHT).', SGH),
  people=('SGHT supports the island government with biosecurity measures, so ships and visitors do not bring rodents back (SGHT).', SGH),
  nature=('Storm petrels, prions, diving petrels and the endemic South Georgia pipit can breed on the main island again (SGHT).', SGH),
  support_h='Support South Georgia',
  btns=[('Donate to SGHT', SGHD), ('Donate to Friends of South Georgia Island', FOSGI)],
  bottom=('The South Georgia Heritage Trust keeps working to protect the island\'s wildlife.', SGHD, 'Donate'),
  widget=None, see=[('Predator_Free_2050.html', 'Predator Free 2050', 'New Zealand\'s plan to remove introduced predators.')],
  pin=pin(-54.28, -36.51, 'South Georgia Island, South Atlantic Ocean')),
 dict(slug='Arctic_Weather_Satellite', title='Arctic Weather Satellite and EPS-Sterna (ESA/EUMETSAT)', short='the Arctic Weather Satellite', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · active, constellation from 2029',
  img=('Arctic_Weather_Satellite_ESA.jpg', 1920, 1080, "Artist's view of ESA's Arctic Weather Satellite in orbit above Earth"),
  credit='ESA (Arctic Weather Satellite, CC BY-SA 3.0 IGO)',
  hook="A small satellite built in just three years proved Europe could watch Arctic weather far more often.",
  wow=("The Arctic Weather Satellite was conceived and deployed in just three years, on a tightly constrained budget (ESA).", AWSC),
  lead="ESA's small Arctic Weather Satellite, launched in August 2024, paved the way for EPS-Sterna, a fleet of 20 satellites from 2029 (ESA, EUMETSAT).",
  eli=['Weather forecasts need measurements of the air: how warm, how wet, how cloudy.',
       'The Arctic has few weather stations, so satellites do much of the measuring there.',
       'A small test satellite worked so well that Europe is building a whole fleet of them.'],
  ws=[('Who', 'The European Space Agency (ESA) built the prototype; EUMETSAT will run the EPS-Sterna constellation.', AWSC),
      ('What', 'A 125 kg satellite with a 19-channel microwave radiometer that measures temperature and humidity in the atmosphere.', AWSF),
      ('When', 'Launched on 16 August 2024. EUMETSAT aims to launch the first EPS-Sterna satellites in 2029.', AWSF),
      ('Where', 'A 600 km sun-synchronous orbit, controlled from Tromsø and Svalbard in Norway.', AWSF),
      ('Why', 'More frequent measurements over the Arctic and the whole globe mean better short-range forecasts.', EUM)],
  impact=('EUMETSAT projects EPS-Sterna data to provide at least €30 billion in economic value to Europe over the programme\'s lifetime (EUMETSAT figure).', EUM),
  fact=('Near-Global in Under Five Hours', 'Each EPS-Sterna satellite will carry identical microwave sounders in different orbital planes, giving near-global coverage in less than five hours (EUMETSAT).', EUM),
  people=('Better forecasts of storms and severe weather help people prepare, in the Arctic and well beyond it (EUMETSAT).', EUM),
  nature=('Watching temperature, humidity and clouds over the poles helps scientists follow how the Arctic is changing (ESA).', AWSC),
  support_h='Learn More About the Arctic Weather Satellite',
  btns=[('ESA Facts and Figures', AWSF[0]), ('EPS-Sterna (EUMETSAT)', EUM[0])],
  bottom=('Want to go deeper? ESA has the full mission story.', AWSC[0], 'For Further Information'),
  widget=W('EPS-Sterna', 'The Arctic Weather Satellite launched on 16 Aug. 2024. EUMETSAT aims to launch the first EPS-Sterna satellites in 2029 (exact date not yet set).', EUM, 'EUMETSAT',
           launch='2024-08-16T00:00:00Z', arrival='2029-01-01T00:00:00Z', arrival_label='first EPS-Sterna launches, 2029 (target year)',
           milestones=[('2024-08-16', 'Arctic Weather Satellite launches'), ('2029-01-01', 'First EPS-Sterna satellites (target year)')]),
  see=[('GCOM-W_SHIZUKU.html', 'GCOM-W "SHIZUKU" (JAXA)', 'Watches Arctic sea ice with the largest antenna on any Earth observation satellite.')],
  pin=pin(69.65, 18.96, 'Tromsø, Norway, one of the Arctic Weather Satellite mission control sites', 'orbit')),
 dict(slug='GCOM-W_SHIZUKU', title='GCOM-W "SHIZUKU" Sea-Ice Watch (JAXA)', short='SHIZUKU', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('Greenland_Sea_Ice_GSFC.jpg', 1472, 1920, 'Sea ice breaking up and swirling in the Greenland Sea, seen by NASA\'s Aqua satellite'),
  credit='NASA Goddard Space Flight Center (MODIS on Aqua, sea ice in the Greenland Sea)',
  hook="A spinning 2-metre antenna has watched the Arctic sea ice for more than a decade.",
  wow=("SHIZUKU's AMSR2 sensor can observe over 99% of Earth's area in just two days (JAXA).", GCW),
  lead="JAXA's SHIZUKU satellite, launched in 2012, measures sea ice, rain, snow and sea temperature through clouds, day and night (JAXA).",
  eli=['Sea ice is frozen ocean water that floats around the North and South Poles.',
       'SHIZUKU is a Japanese satellite with a big spinning antenna that "hears" faint microwaves from Earth.',
       'Those signals show where the ice is, even through clouds and in the dark polar winter.'],
  ws=[('Who', 'The Japan Aerospace Exploration Agency (JAXA).', GCW),
      ('What', 'A satellite carrying AMSR2, a microwave radiometer that measures precipitation, water vapour, sea temperature, snow depth and sea ice.', GCW),
      ('When', 'Launched on 18 May 2012 on an H-IIA rocket from Tanegashima Space Center.', GCW),
      ('Where', 'In orbit, covering the whole planet, including both polar regions.', GCW),
      ('Why', 'Long, steady records of sea ice and water show how the climate is changing.', GCW)],
  impact=('In August 2012, SHIZUKU recorded Arctic sea ice at 4.21 million km², below the previous record low of 4.25 million km² set in 2007 (JAXA).', GCW12),
  fact=('The Biggest Eye', 'AMSR2\'s antenna is about 2 metres across, the world\'s largest observation sensor on a satellite (JAXA).', GCW),
  people=('SHIZUKU data on rain, water vapour and sea temperature support weather and water information people use (JAXA).', GCW),
  nature=('Tracking sea ice shows how the Arctic Ocean\'s frozen cover is changing from year to year (JAXA).', GCW12),
  support_h='Learn More About SHIZUKU',
  btns=[('JAXA: GCOM-W', GCW[0])],
  bottom=('Want to go deeper? JAXA has the full mission story.', GCW[0], 'For Further Information'),
  widget=None, see=[('GOSAT-GW.html', 'GOSAT-GW (JAXA)', 'Carries the next AMSR sensor alongside greenhouse gas instruments.')],
  pin=pin(30.40, 130.97, 'Tanegashima Space Center, Japan, where SHIZUKU launched in 2012', 'orbit')),
 dict(slug='SCISAT', title='SCISAT Ozone Watch (Canadian Space Agency)', short='SCISAT', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('Ozone_Hole_2024_SVS14711.jpg', 1920, 1080, 'Global view of the ozone layer from NASA\'s 2024 ozone hole visualization'),
  credit='NASA Scientific Visualization Studio (2024 Ozone Hole Update, SVS 14711)',
  hook="Built to last two years, a tiny Canadian satellite is still watching the ozone layer more than 20 years later.",
  wow=("SCISAT measures 70 different trace gases in the atmosphere (CSA).", SCI),
  lead="Canada's 150 kg SCISAT has measured the chemistry of the ozone layer since 2003, with a special focus on Canada and the Arctic (CSA).",
  eli=['High in the sky, a layer of ozone gas blocks most of the Sun\'s harmful ultraviolet rays.',
       'Some human-made chemicals were eating holes in that layer.',
       'SCISAT watches sunlight shine through the air at sunrise and sunset to find out which gases are there.'],
  ws=[('Who', 'The Canadian Space Agency, with a science team led from the University of Waterloo.', SCI),
      ('What', 'A small satellite with two instruments, ACE-FTS and MAESTRO, that measure gases and particles that affect ozone.', SCI),
      ('When', 'Launched on 12 August 2003. In its 2026-27 plan, CSA says SCISAT is entering its 22nd year in orbit.', SCIDP),
      ('Where', 'A 650 km high-inclination orbit that passes over the polar regions as well as the tropics.', SCI),
      ('Why', 'Ozone protects us from the Sun\'s ultraviolet radiation, and Arctic spring ozone has seen severe declines.', SCI)],
  impact=('SCISAT data make an important contribution to policies that protect the ozone layer, such as the Montreal Protocol (CSA).', SCI),
  fact=('Tracking Volcano Water', 'After the 2022 Hunga Tonga eruption, SCISAT helped estimate how much water vapour reached the stratosphere (CSA).', SCI),
  people=('A healthy ozone layer prevents most of the Sun\'s ultraviolet radiation from reaching people on the ground (CSA).', SCI),
  nature=('SCISAT also tracks pollution and wildfire smoke, and helped explain ozone loss after the 2019-20 Australian bushfires (CSA).', SCI),
  support_h='Learn More About SCISAT',
  btns=[('CSA: About SCISAT', SCI[0])],
  bottom=('Want to go deeper? The Canadian Space Agency has the full mission story.', SCI[0], 'For Further Information'),
  widget=None, see=[('Sentinel-5P.html', 'Sentinel-5P', 'Maps ozone and air pollution across the globe every day.')],
  pin=pin(43.47, -80.54, 'University of Waterloo, Ontario, home of the SCISAT science team', 'orbit')),
 dict(slug='Chilika_Lake', title='Chilika Lake Restoration', short='Chilika', cat='lakes',
  hub=('Lakes.html', 'Lakes'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Chilika_Lake_Mouth.jpg', 1920, 1280, 'The mouth of Chilika Lake, where the lagoon meets the Bay of Bengal in Odisha, India'),
  credit='Phadke09 via Wikimedia Commons (Mouth of Chilika Lake, CC BY-SA 4.0)',
  hook="Opening one new mouth to the sea brought a dying lagoon, and its fishers, back to life.",
  wow=("In the seven months after the new mouth opened, the fish landing was 3,718 tonnes, against an earlier average of about 1,600 tonnes a year (Chilika Development Authority).", CHE),
  lead='In 2000, the Chilika Development Authority opened a new mouth between India\'s Chilika Lake and the sea, and the lagoon and its fisheries recovered (CDA).',
  eli=['Chilika is a huge lagoon in India where river water and seawater mix.',
       'Mud was choking its link to the sea, so fish and the people who catch them were struggling.',
       'Engineers dug a new opening to the sea, and the fish came back.'],
  ws=[('Who', 'The Chilika Development Authority (CDA), a body of the Government of Odisha, India.', CHE),
      ('What', 'A new mouth to the sea and desilting of the lead channel, which shortened the outflow channel by 18 km.', CHE),
      ('When', 'The new mouth opened on 23 September 2000.', CHE),
      ('Where', 'Chilika Lake, a brackish lagoon on the Bay of Bengal in Odisha, India.', CHE),
      ('Why', 'Silt, a shrinking water area, falling salinity and invasive freshwater weeds were degrading the lagoon.', CHE)],
  impact=('The CDA reports that average annual family income for fishers rose by more than Rs 50,000 after the restoration (CDA figure).', CHE),
  fact=('Dolphins of the Lagoon', 'The 2025 state census counted 159 Irrawaddy dolphins in Chilika, the highest of any area in Odisha (state wildlife wing, via The New Indian Express).', CHD),
  people=('The restored lagoon immensely benefited the fisher families who depend on it (CDA).', CHE),
  nature=('The new mouth improved salinity and rejuvenated the lagoon ecosystem (CDA).', CHE),
  support_h='Learn More About Chilika',
  btns=[('Chilika Eco-Restoration (CDA)', CHE[0])],
  bottom=('Want to go deeper? The Chilika Development Authority explains the restoration.', CHE[0], 'For Further Information'),
  widget=None, see=[],
  pin=pin(19.72, 85.32, 'Chilika Lake, Odisha, India')),
 dict(slug='Tonle_Sap', title='Tonle Sap: The Lake That Reverses a River', short='Tonle Sap', cat='lakes',
  hub=('Lakes.html', 'Lakes'), cls='natural', status='active', glass='earth', label='Natural solution · UNESCO biosphere reserve',
  img=('Tonle_Sap_Floating_Village.jpg', 1920, 1358, 'A floating village of houses on the water of the Tonle Sap lake in Cambodia'),
  credit='Christophe95 via Wikimedia Commons (Floating village on the Tonlé Sap, CC BY-SA 4.0)',
  hook="Every rainy season, the Mekong pushes water backwards into a lake that can grow up to five times larger.",
  wow=("During the rains the Mekong overflows and can expand Tonle Sap Lake by up to five times (UNESCO).", TSM),
  lead='Tonle Sap, the largest freshwater lake in Southeast Asia, is a UNESCO biosphere reserve whose flooded forests shelter villages and fish (UNESCO).',
  eli=['Tonle Sap is a giant lake in Cambodia joined to the Mekong River.',
       'In the rainy season the river gets so full that water flows backwards into the lake.',
       'The lake swells up, flooding forests where fish grow, and many families live in floating villages.'],
  ws=[('Who', 'A natural system, protected as a UNESCO biosphere reserve in Cambodia.', TSM),
      ('What', 'A seasonal flood pulse: the lake, its flooded forests and swamps, and rice fields around them.', TSM),
      ('When', 'Named a UNESCO biosphere reserve in 1997; the flooding returns every rainy season.', TSM),
      ('Where', 'Tonle Sap Lake, at the centre of the Tonle Sap Basin in Cambodia.', TSM),
      ('Why', 'The floods create habitats for many species and support the people who live around the lake.', TSM)],
  impact=('The biosphere reserve covers about 1.48 million hectares and is home to about 1.38 million people (UNESCO).', TSM),
  fact=('Nature\'s Flood Wall', 'Flooded forests around the lake act as a natural barrier, protecting villages from inundation and soil erosion (UNESCO).', TSM),
  people=('Flooded forests protect villages against floods and erosion (UNESCO).', TSM),
  nature=('Fish are the reserve\'s most species-rich animal group, and about 225 bird species live there (UNESCO).', TSM),
  support_h='Learn More About Tonle Sap',
  btns=[('UNESCO: Tonle Sap Biosphere Reserve', TSM[0])],
  bottom=('Want to go deeper? UNESCO describes the biosphere reserve.', TSM[0], 'For Further Information'),
  widget=None, see=[],
  pin=pin(12.81, 104.05, 'Tonle Sap Biosphere Reserve, Cambodia')),
 dict(slug='Lake_Biwa_Soap_Movement', title='Lake Biwa and the Soap Movement', short='the Soap Movement', cat='lakes',
  hub=('Lakes.html', 'Lakes'), cls='government', status='active', glass='earth', label='Community and government solution · active',
  img=('Lake_Biwa_Shiga_NASA.jpg', 1920, 1271, 'Lake Biwa, the largest lake in Japan, surrounded by Shiga Prefecture, seen from the International Space Station'),
  credit='NASA (ISS007-E-17620, astronaut photograph of Lake Biwa and Shiga Prefecture)',
  hook="Families swapping their detergent for soap helped change the law for Japan's biggest lake.",
  wow=("Around Lake Biwa Day each July, more than 100,000 people join cleanups around the lake (Shiga Prefecture).", BIW),
  lead='After a red tide in 1977, Shiga residents switched to soap, and in 1980 the prefecture limited phosphorus to protect Lake Biwa (Shiga Prefecture).',
  eli=['Lake Biwa is the biggest lake in Japan.',
       'Phosphorus from washing detergent fed tiny algae until the water turned red in 1977.',
       'People switched to natural soap, and new rules cut the phosphorus going into the lake.'],
  ws=[('Who', 'The people of Shiga, whose citizen movement led Shiga Prefecture to act.', BIW),
      ('What', 'The Soap Movement, then the Ordinance for the Prevention of Eutrophication of Lake Biwa.', BIW),
      ('When', 'A large freshwater red tide in 1977; the ordinance took effect on 1 July 1980, now Lake Biwa Day.', BIW),
      ('Where', 'Lake Biwa, Shiga Prefecture, Japan.', BIW),
      ('Why', 'Phosphorus from detergents was feeding excessive growth of phytoplankton in the lake.', BIW)],
  impact=('The citizen movement led directly to a prefecture law limiting phosphorus, and every 1 July is now Lake Biwa Day (Shiga Prefecture).', BIW),
  fact=('Sharing the Lesson', 'Shiga shares what it learned at Lake Biwa with places facing similar lake problems around the world (Shiga Prefecture).', BIW),
  people=('Residents meet every year to exchange ideas and cheer on efforts for the lake (Shiga Prefecture).', BIW),
  nature=('Ongoing work also removes invasive alien species that threaten native species in and around the lake (Shiga Prefecture).', BIW),
  support_h='Learn More About Lake Biwa',
  btns=[('Shiga Prefecture: Lake Biwa', BIW[0])],
  bottom=('Want to go deeper? Shiga Prefecture tells the story.', BIW[0], 'For Further Information'),
  widget=None, see=[('Lake_Constance.html', 'Lake Constance Phosphorus Recovery', 'Another lake saved by cutting phosphorus.')],
  pin=pin(35.25, 136.08, 'Lake Biwa, Shiga Prefecture, Japan')),
 dict(slug='Lake_Constance', title='Lake Constance Phosphorus Recovery', short='Lake Constance', cat='lakes',
  hub=('Lakes.html', 'Lakes'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Lake_Constance_ISS030_E_161620.jpg', 1920, 1275, 'Lake Constance between Germany, Austria and Switzerland, seen from the International Space Station'),
  credit='NASA (ISS030-E-161620, astronaut photograph of Lake Constance, 2012)',
  hook="Three countries cleaned up a lake that gives drinking water to about five million people.",
  wow=("Phosphorus in Lake Constance fell from a peak of 84 µg/l in the late 1970s to 6-8 µg/l since 2006 (IGKB).", IGP),
  lead='Treatment plants that remove phosphorus brought Lake Constance back to the clear state typical of Alpine lakes (International Commission for the Protection of Lake Constance).',
  eli=['Lake Constance sits between Germany, Austria and Switzerland.',
       'Too much phosphorus from wastewater made algae grow, which is bad for the lake.',
       'The countries built treatment plants that take out phosphorus, and the lake recovered.'],
  ws=[('Who', 'The International Commission for the Protection of Lake Constance (IGKB), with Germany, Austria, Switzerland and Liechtenstein.', IGP),
      ('What', 'Wastewater treatment plants with phosphorus removal around the lake.', IGP),
      ('When', 'Phosphorus peaked in the late 1970s; since 2006 it has stayed at 6-8 µg/l.', IGP),
      ('Where', 'Lake Constance (Bodensee), on the Rhine between Germany, Austria and Switzerland.', IGP),
      ('Why', 'Rising phosphorus was feeding algae and changing the lake.', IGP)],
  impact=('With less phosphorus, the lake\'s phytoplankton has shifted back toward the natural state for this type of lake (IGKB).', IGP),
  fact=('A Drinking Water Giant', 'Lake Constance supplies drinking water to around five million people (IGKB).', IGW),
  people=('About five million people get drinking water from the lake (IGKB).', IGW),
  nature=('The lake is back in the low-nutrient range typical of Alpine lakes (IGKB).', IGP),
  support_h='Learn More About Lake Constance',
  btns=[('IGKB: Phosphorus in Lake Constance', IGP[0])],
  bottom=('Want to go deeper? The IGKB publishes the lake\'s data.', IGP[0], 'For Further Information'),
  widget=None, see=[('Lake_Biwa_Soap_Movement.html', 'Lake Biwa and the Soap Movement', 'Japan\'s largest lake, saved by cutting phosphorus.')],
  pin=pin(47.63, 9.37, 'Lake Constance (Bodensee), Germany, Austria and Switzerland')),
 dict(slug='Room_for_the_River', title='Room for the River (Netherlands)', short='Room for the River', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='government', status='active', glass='earth', label='Government solution · completed 2019',
  img=('Netherlands_Rivers_ISS063_E_002730.jpg', 1920, 1280, 'The Rhine, Meuse and Scheldt river delta in the Netherlands, seen from the International Space Station'),
  credit='NASA (ISS063-E-002730, astronaut photograph of the Rhine-Meuse-Scheldt delta, April 23, 2020)',
  hook="Instead of building higher walls, the Netherlands gave its rivers more space.",
  wow=("Room for the River made around 4 million people in the Netherlands safer from floods (Rijkswaterstaat).", RFR),
  lead='At 34 locations, the Netherlands widened floodplains and dug side channels so rivers can safely carry more water (Rijkswaterstaat).',
  eli=['When rivers get very full, they can flood towns.',
       'The Netherlands moved dikes back and dug extra channels so the water has more room.',
       'Now high water can spread out safely, and the riverside landscape is better too.'],
  ws=[('Who', 'Rijkswaterstaat and regional authorities, working closely with local residents.', RFR),
      ('What', 'Measures at 34 locations: more room for rivers to carry high water safely.', RFR),
      ('When', 'From 2006; officially completed with the opening of the Reevediep flood channel in early 2019.', RFR),
      ('Where', 'Along the IJssel, Waal, Lower Rhine and Lek rivers in the Netherlands.', RFR),
      ('Why', 'To improve flood safety while also improving the riverside landscape.', RFR)],
  impact=('The programme cost €2.3 billion and improved safety, spatial quality and quality of life for around 4 million people (Rijkswaterstaat figures).', RFR),
  fact=('Room, Not Walls', 'The programme made space for high water at 34 locations rather than only raising dikes (Rijkswaterstaat).', RFR),
  people=('Around 4 million people are safer from river floods (Rijkswaterstaat).', RFR),
  nature=('The work also improved the spatial quality of the river landscape (Rijkswaterstaat).', RFR),
  support_h='Learn More About Room for the River',
  btns=[('Rijkswaterstaat: Room for the River', RFR[0])],
  bottom=('Want to go deeper? Rijkswaterstaat explains the programme.', RFR[0], 'For Further Information'),
  widget=None, see=[],
  pin=pin(52.25, 6.16, 'Deventer, on the IJssel, one of the Room for the River sites')),
 dict(slug='Tubbataha_Reefs', title='Tubbataha Reefs Natural Park', short='Tubbataha', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Tubbataha_Reefs_UNESCO.jpg', 1920, 1262, 'Coral atoll of Tubbataha Reefs Natural Park in the Sulu Sea, Philippines'),
  credit='Ron Van Oers / UNESCO via Wikimedia Commons (CC BY-SA 3.0 IGO)',
  hook="A no-fishing reef in the middle of the Sulu Sea holds far more fish than a typical healthy reef.",
  wow=("In 2023, Tubbataha's average fish biomass was 76-100 tonnes per km², against 21-40 for healthy reefs elsewhere in the Philippines (IUCN).", TUBO),
  lead='Tubbataha, a no-take marine park of 96,828 hectares in the Philippines, protects pristine coral atolls and the sea life that seeds the Sulu Sea (UNESCO).',
  eli=['Tubbataha is a group of coral reefs far out in the sea in the Philippines.',
       'Nobody is allowed to fish there, so the fish can grow big and have lots of babies.',
       'Baby fish drift out from the reef and help fill fishing grounds around it.'],
  ws=[('Who', 'The Philippine government, which protects the park; it is a UNESCO World Heritage Site.', TUB),
      ('What', 'A no-take marine park that protects coral atolls, reef walls and deep sea.', TUB),
      ('When', 'Inscribed as World Heritage in 1993; yearly reef monitoring since 1997 (IUCN).', TUBO),
      ('Where', 'In the centre of the Sulu Sea, Philippines, covering North and South Atolls and Jessie Beazley Reef.', TUB),
      ('Why', 'Low fishing pressure keeps the reef healthy and lets it help supply fisheries beyond its boundaries.', TUB)],
  impact=('The reefs support over 360 species of coral and almost 700 species of fish (UNESCO).', TUB),
  fact=('Shark Central', 'Tubbataha has recorded some of the largest densities of grey and whitetip reef sharks in the world (IUCN).', TUBO),
  people=('The park helps support fisheries outside its boundaries across the Sulu Sea (UNESCO).', TUB),
  nature=('Whales, dolphins, sharks, turtles and nesting seabirds find a refuge there (UNESCO).', TUB),
  support_h='Learn More About Tubbataha',
  btns=[('UNESCO: Tubbataha Reefs', TUB[0]), ('IUCN World Heritage Outlook', TUBO[0])],
  bottom=('Want to go deeper? UNESCO describes the park.', TUB[0], 'For Further Information'),
  widget=None, see=[('Palau_National_Marine_Sanctuary.html', 'Palau National Marine Sanctuary', 'A Pacific nation that made most of its sea a no-fishing zone.')],
  pin=pin(8.95, 119.92, 'Tubbataha Reefs Natural Park, Sulu Sea, Philippines')),
 dict(slug='Sargassum_Watch', title='Sargassum Watch System (USF)', short='Sargassum Watch', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='agency', status='active', glass='earth', label='University service · active',
  img=('Sargassum_Bloom_Atlantic_Sentinel.jpg', 1920, 1218, 'Long brown lines of sargassum seaweed floating off Martinique in the Caribbean, seen by a Copernicus Sentinel-2 satellite'),
  credit='Contains modified Copernicus Sentinel-2 data, processed by ESA (sargassum off Martinique)',
  hook="Satellites spotted a seaweed belt stretching from Africa to the Gulf of Mexico.",
  wow=("In 2018, more than 20 million tons of sargassum floated in the tropical Atlantic, heavier than 200 fully loaded aircraft carriers (USF).", SAWN),
  lead='The University of South Florida uses NASA satellite data to track the Great Atlantic Sargassum Belt and warn coasts about seaweed blooms (USF).',
  eli=['Sargassum is a brown seaweed that floats in big mats on the ocean.',
       'Some years so much of it washes onto beaches that it piles up on the shore.',
       'Scientists use satellites to see where it is, so coastal towns can get ready.'],
  ws=[('Who', 'The Optical Oceanography Lab at the University of South Florida College of Marine Science.', SAWS),
      ('What', 'The Sargassum Watch System, which uses satellite images to track floating sargassum.', SAWS),
      ('When', 'USF scientists reported the Great Atlantic Sargassum Belt in Science in 2019; it began in 2011.', SAWN),
      ('Where', 'The tropical Atlantic, Caribbean Sea and Gulf of Mexico.', SAWN),
      ('Why', 'Huge blooms can wreak havoc on shorelines across the Caribbean, Gulf of Mexico and Florida.', SAWN)],
  impact=('Scientists used NASA\'s MODIS sensors on the Terra and Aqua satellites to discover the belt (USF).', SAWN),
  fact=('Shaped by Currents', 'Simulations confirmed the belt forms its shape in response to ocean currents (USF).', SAWN),
  people=('Tracking the seaweed helps coastal communities and tourism prepare for blooms (USF).', SAWN),
  nature=('In the open ocean, sargassum is habitat for marine life; on beaches, large piles cause problems (USF).', SAWN),
  support_h='Learn More About Sargassum Watch',
  btns=[('USF Sargassum Watch System', SAWS[0])],
  bottom=('Want to go deeper? USF explains the discovery.', SAWN[0], 'For Further Information'),
  widget=None, see=[('PACE.html', 'PACE (NASA)', 'Sees ocean colour in more detail than ever before.')],
  pin=pin(27.76, -82.64, 'USF College of Marine Science, St. Petersburg, Florida')),
 dict(slug='Redonda_Restoration', title='Redonda Island Restoration', short='Redonda', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='earth', label='Nonprofit and government solution · active',
  img=('Redonda_By_Sea_2023.jpg', 1920, 1280, 'The steep green island of Redonda in Antigua and Barbuda, seen from the sea in 2023'),
  credit='Addshore via Wikimedia Commons (Redonda by sea, 2023, CC BY-SA 4.0)',
  hook="A bare rock island turned green again in just a few years.",
  wow=("After invasive rats and feral goats were removed in 2017, Redonda's total vegetation biomass rose by more than 2,000% (Fauna & Flora).", RED),
  lead='Redonda went from a dusty moonscape to a wildlife haven and is now one of the largest protected areas in the Caribbean (Fauna & Flora).',
  eli=['Redonda is a small island in the Caribbean Sea.',
       'Goats and rats had eaten almost everything, so it was bare rock.',
       'People removed them, and plants and birds came back fast.'],
  ws=[('Who', 'Antigua and Barbuda\'s Department of Environment with the Environmental Awareness Group, Fauna & Flora and Re:wild.', RED),
      ('What', 'Removing invasive rats and feral goats, then protecting the island, its reef and sea.', RED),
      ('When', 'The restoration programme launched in 2016; the protected area was announced in 2023.', RED),
      ('Where', 'Redonda, part of Antigua and Barbuda, in the Caribbean.', RED),
      ('Why', 'Invasive animals had stripped the island bare.', RED)],
  impact=('The Redonda Ecosystem Reserve covers almost 30,000 hectares of land and sea, including an 18,000-hectare coral reef (Fauna & Flora).', RED),
  fact=('Hidden Treasure', 'The new reserve is believed to hold at least 30 globally threatened and near-threatened species (Fauna & Flora).', RED),
  people=('The reserve protects seagrass and reef around the island that sea life and fisheries depend on (Fauna & Flora).', RED),
  nature=('Globally important seabird colonies nest on the island (Fauna & Flora).', RED),
  support_h='Support Redonda',
  btns=[('Donate to the Environmental Awareness Group', EAGD), ('Read the Redonda Story', RED[0])],
  bottom=('The Environmental Awareness Group works for Antigua and Barbuda\'s nature.', EAGD, 'Donate'),
  donate_alt='Donate to the Environmental Awareness Group',
  widget=None, see=[('Oceans.html', 'Ocean hub', 'Redonda\'s new reserve includes an 18,000-hectare coral reef.'), ('South_Georgia_Habitat_Restoration.html', 'South Georgia Habitat Restoration', 'The world\'s largest island rodent eradication.')],
  pin=pin(16.94, -62.35, 'Redonda, Antigua and Barbuda')),
 dict(slug='Iberian_Lynx', title='The Iberian Lynx Comeback', short='the lynx recovery', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Iberian_Lynx_Almuradiel_2021.jpg', 1920, 1920, 'A wild female Iberian lynx in Almuradiel, Ciudad Real, Spain'),
  credit='Diego Delso via Wikimedia Commons (Iberian lynx, Almuradiel, 2021, CC BY-SA 4.0)',
  hook="From fewer than 100 cats to more than 2,600 in about 25 years.",
  wow=("The Iberian lynx went from fewer than 100 counted in 2002 to 2,663 in 2025 (MITECO census).", LYN),
  lead='Spain and Portugal brought the Iberian lynx back from the edge: the 2025 census counted 2,663, almost double 2021 (MITECO).',
  eli=['The Iberian lynx is a wild cat that lives only in Spain and Portugal.',
       'By 2002 there were fewer than 100 left.',
       'Breeding, releases and protection helped, and now there are more than 2,600.'],
  ws=[('Who', 'Spain\'s Ministry for the Ecological Transition (MITECO), the Spanish regions and Portugal\'s ICNF.', LYN),
      ('What', 'Coordinated conservation and yearly census of the lynx in Spain and Portugal.', LYN),
      ('When', 'About 25 years of coordinated programmes; the 2025 census was published in June 2026.', LYN),
      ('Where', '26 areas in Spain and Portugal, led by Castilla-La Mancha with 1,051 lynx and Andalusia with 885.', LYN),
      ('Why', 'The species, found only on the Iberian Peninsula, had nearly disappeared.', LYN)],
  impact=('The 2025 count of 2,663 was up 10.9% on 2024 and about 95% on 2021 (MITECO figures).', LYN),
  fact=('952 Kittens', 'In 2025, 952 lynx kittens were born, from 542 breeding or territorial females (MITECO).', LYN),
  people=('Lynx are returning to new regions, including Castilla y León with a reintroduction project (MITECO).', LYN),
  nature=('Breeding females are getting closer to 750, the milestone for a favourable conservation status (MITECO).', LYN),
  support_h='Learn More About the Iberian Lynx',
  btns=[('MITECO: 2025 Lynx Census', LYN[0])],
  bottom=('Want to go deeper? MITECO publishes the census.', LYN[0], 'For Further Information'),
  widget=None, see=[('Rewilding_Europe.html', 'Rewilding Europe', 'Bringing wild nature back across Europe.')],
  pin=pin(38.48, -3.47, 'Almuradiel, Ciudad Real, Spain, in lynx country')),
 dict(slug='Trees_for_Life', title='Trees for Life: Restoring the Caledonian Forest', short='Trees for Life', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='earth', label='Nonprofit solution · active',
  img=('Glen_Affric_Scots_Pine.jpg', 1440, 1920, 'Native Scots pine woodland in Glen Affric, Scotland'),
  credit='Chris via Wikimedia Commons (Glen Affric Scots Pine, CC BY-SA 2.0)',
  hook="Volunteers have helped grow more than two million trees in Scotland's wild forest.",
  wow=("Since 1993, more than 5,000 volunteers have helped Trees for Life grow more than two million trees (Trees for Life).", TFL),
  lead='Trees for Life is rewilding the Scottish Highlands, bringing back the Caledonian forest, of which less than 2% survives (Trees for Life).',
  eli=['The Caledonian forest of pine trees once covered much of the Scottish Highlands.',
       'Today only small pieces are left.',
       'Volunteers plant trees and protect young ones, so the wild forest can grow back.'],
  ws=[('Who', 'Trees for Life, a Scottish rewilding charity, with thousands of volunteers.', TFL),
      ('What', 'Growing and planting native trees, protecting ancient pinewoods and returning wildlife such as red squirrels.', TFL),
      ('When', 'Restoring the Caledonian forest since 1993.', TFL),
      ('Where', 'The Scottish Highlands, including the Dundreggan estate near Loch Ness and Glen Affric.', TFL),
      ('Why', 'Less than 2% of the Caledonian forest survives, and most remaining pinewoods are under threat.', TFL)],
  impact=('More than two million trees grown, plus natural regeneration of many more (Trees for Life figures).', TFL),
  fact=('A World First', 'Its Dundreggan Rewilding Centre, opened in April 2023, welcomed over 20,000 visitors in its first year (Trees for Life).', TFL),
  people=('The charity creates nature-rich landscapes that include and support people, with volunteering and jobs (Trees for Life).', TFL),
  nature=('Red squirrels have been reintroduced to parts of their former range since 2016 (Trees for Life).', TFL),
  support_h='Support Trees for Life',
  btns=[('Donate to Trees for Life', TFLD), ('Read the Annual Review', TFL[0])],
  bottom=('Trees for Life takes donations to grow the wild forest.', TFLD, 'Donate'),
  widget=None, see=[],
  pin=pin(57.18, -4.77, 'Dundreggan Rewilding Centre, Glenmoriston, Scotland')),
 dict(slug='Nepal_Tigers', title='Nepal Doubles Its Tigers', short='Nepal\'s tiger recovery', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Bengal_Tiger_Bardia_Nepal.jpg', 1920, 1280, 'A wild Bengal tiger in tall grass in Bardia National Park, Nepal'),
  credit='Ambish Kazi via Wikimedia Commons (Royal Bengal Tiger, Bardia, Nepal, CC BY-SA 4.0)',
  hook="Nepal became the first country to double its wild tigers.",
  wow=("Nepal's tigers rose from 121 in 2009 to 355 in 2022 (Nepal's national tiger survey, via NTNC).", NTN),
  lead='With rangers, wildlife corridors and over 450 community anti-poaching units, Nepal nearly tripled its wild tigers in 13 years (NTNC).',
  eli=['Tigers were disappearing from Asia because of hunting and lost forests.',
       'Nepal promised to double its tigers, and protected forests and paths between them.',
       'Local communities helped stop poachers, and now Nepal has about three times as many tigers.'],
  ws=[('Who', 'Nepal\'s Department of National Parks and Wildlife Conservation and Department of Forests and Soil Conservation, with NTNC and communities.', NTN),
      ('What', 'Protected habitat, restored corridors, anti-poaching units and a national tiger survey every four years.', NTN),
      ('When', 'Surveys in 2009, 2013, 2018 and 2022 counted 121, 198, 235 and 355 tigers.', NTN),
      ('Where', 'Nepal\'s lowland parks, including Banke and Parsa National Parks, and corridors to India.', NTN),
      ('Why', 'Wild tigers had fallen by 97% in a century, to about 3,200 by 2010.', NTN)],
  impact=('Nepal is officially the first country to double its tiger population, meeting the 2010 pledge (NTNC).', NTN),
  fact=('Community Guardians', 'More than 450 community-based anti-poaching units have been formed in Nepal (NTNC).', NTN),
  people=('Communities take part in stewardship, and managing human-tiger conflict is a key next step (NTNC).', NTN),
  nature=('As apex predators, tigers are linked to the health of forests and ecosystems (NTNC).', NTN),
  support_h='Learn More About Nepal\'s Tigers',
  btns=[('NTNC: Nepal Doubles Its Tigers', NTN[0])],
  bottom=('Want to go deeper? NTNC tells the story of the survey.', NTN[0], 'For Further Information'),
  widget=None, see=[],
  pin=pin(28.39, 81.27, 'Bardia National Park, Nepal')),
 dict(slug='Altyn_Dala_Saiga', title='Saiga Recovery on the Kazakh Steppe (Altyn Dala)', short='Altyn Dala', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='earth', label='Nonprofit and government solution · active',
  img=('Saiga_West_Kazakhstan.jpg', 1920, 1280, 'Saiga antelope on the steppe of West Kazakhstan'),
  credit='Yakov Fedorov via Wikimedia Commons (Saiga in West Kazakhstan, CC BY-SA 4.0)',
  hook="An antelope that once ran alongside Neanderthals is back on the steppe in the millions.",
  wow=("Kazakhstan's 2024 aerial census counted 2,833,600 adult saiga, a 48% rise in one year (Altyn Dala).", SAI),
  lead='The Altyn Dala Conservation Initiative, led by ACBK, is restoring Kazakhstan\'s steppe, with the saiga antelope as its flagship (Altyn Dala).',
  eli=['The saiga is an antelope with a big, bendy nose that lives on the grassy steppe.',
       'Not long ago, there were very few left in Kazakhstan.',
       'Kazakhstan and its partners protected the steppe, and now there are millions again.'],
  ws=[('Who', 'The Association for the Conservation of Biodiversity of Kazakhstan (ACBK), with Fauna & Flora, Frankfurt Zoological Society, RSPB and the Government of Kazakhstan.', SAIP),
      ('What', 'Restoring steppe, wetland and desert ecosystems, stopping illegal wildlife trade and counting saiga every year.', SAIP),
      ('When', 'Co-founded in 2005; the 2024 census flew from 14 April to 1 May.', SAI),
      ('Where', 'The steppe of Kazakhstan: the Ural, Ustyurt and Betpak Dala saiga populations.', SAI),
      ('Why', 'An RSPB leader recalls seeing no more than seven saiga in a week in 2006 (Altyn Dala).', SAIP)],
  impact=('In 2022 the partnership helped establish a new 780,000-hectare protected area in west Kazakhstan, home to the world\'s largest saiga population (Altyn Dala).', SAIP),
  fact=('Counting From the Air', 'The 2024 census teams flew 215 hours over 151,226 km² to count the saiga (Altyn Dala).', SAI),
  people=('The work aims to build careers and generate jobs in rural communities (Altyn Dala).', SAIP),
  nature=('Healthy steppe also helps species like the steppe tortoise and saker falcon (Altyn Dala).', SAIP),
  support_h='Support Altyn Dala',
  btns=[('Altyn Dala: Our Partnership', SAIP[0]), ('2024 Census Results', SAI[0])],
  bottom=('Altyn Dala invites supporters to get in touch through its partnership page.', SAIP[0], 'For Further Information'),
  widget=None, see=[('African_Parks.html', 'African Parks', 'Managing protected areas for wildlife and people across Africa.')],
  pin=pin(50.0, 64.0, 'The Kazakh steppe, Altyn Dala landscape, Kazakhstan')),
 dict(slug='Gorongosa', title='Gorongosa National Park Restoration', short='Gorongosa', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='earth', label='Nonprofit and government solution · active',
  img=('Mount_Gorongosa_Mozambique.jpg', 1920, 1265, 'Mount Gorongosa rising above the forest in Gorongosa National Park, Mozambique'),
  credit='Judy Gallagher via Wikimedia Commons (Mount Gorongosa, CC BY 2.0)',
  hook="A restored park in Mozambique now holds more large animals than it did in the 1970s.",
  wow=("The October 2024 aerial count found 110,513 large animals in Gorongosa, the highest ever recorded (Gorongosa count report).", GOR),
  lead='The Mozambique government and the Gorongosa Project are restoring Gorongosa National Park as "a park for the people" (Gorongosa).',
  eli=['Gorongosa is a big wildlife park in Mozambique, in Africa.',
       'Rangers, scientists and local people work together to protect it.',
       'The latest count found more big animals there than ever recorded.'],
  ws=[('Who', 'The Government of Mozambique and the Gorongosa Restoration Project.', GOR),
      ('What', 'Restoring wildlife and habitat while supporting human development and farming around the park.', GOR),
      ('When', 'The latest aerial count was flown from 8 to 22 October 2024.', GOR),
      ('Where', 'Gorongosa National Park in central Mozambique.', GOR),
      ('Why', 'To bring back a wild ecosystem and make it benefit the communities around it.', GOR)],
  impact=('The 2024 total of 110,513 large animals exceeds the wildlife levels documented in the 1970s (Gorongosa 2024 highlights).', GORH),
  fact=('Waterbuck Wonderland', 'The 2024 count recorded 65,332 waterbuck, more than half of all large animals counted (Gorongosa count report).', GOR),
  people=('Community conservation areas next to the park were also surveyed, part of a park built with its neighbours (Gorongosa count report).', GOR),
  nature=('Only 61% of the park was counted, so 110,513 is the absolute minimum number of large animals there (Gorongosa count report).', GOR),
  support_h='Support Gorongosa',
  btns=[('Donate to Gorongosa', GORD), ('Read the 2024 Wildlife Count', GOR[0])],
  bottom=('The Gorongosa Project takes donations for the park and its people.', GORD, 'Donate'),
  widget=None, see=[('African_Parks.html', 'African Parks', 'Managing protected areas for wildlife and people across Africa.')],
  pin=pin(-18.97, 34.35, 'Gorongosa National Park, Mozambique')),
 dict(slug='NEOSSat', title='NEOSSat Asteroid and Debris Telescope (Canada)', short='NEOSSat', cat='planetary-defense',
  hub=('Planetary_Defense.html', 'Planetary Defense'), cls='agency', status='active', glass='space', label='Agency solution · active',
  img=('Comet_NEOWISE_ISS_NHQ202007180001.jpg', 1920, 1280, 'The International Space Station streaking across the sky above comet NEOWISE in July 2020'),
  credit='NASA/Bill Ingalls (NHQ202007180001, comet NEOWISE and the ISS, July 18, 2020)',
  hook="A suitcase-sized satellite was the world's first space telescope built to hunt asteroids and space debris.",
  wow=("NEOSSat is the world's first space telescope dedicated to detecting and tracking asteroids, comets, satellites and space debris (CSA).", NEO),
  lead="Canada's NEOSSat circles Earth every 100 minutes, scanning near the Sun for asteroids and comets and tracking satellites and debris (CSA).",
  eli=['Some space rocks, called asteroids, pass close to Earth.',
       'NEOSSat is a small Canadian telescope in space that looks for them, even near the Sun.',
       'It also watches satellites and space junk to help avoid crashes in orbit.'],
  ws=[('Who', 'The Canadian Space Agency (CSA) and Defence Research and Development Canada (DRDC).', NEO),
      ('What', 'A microsatellite telescope that tracks asteroids, comets, satellites and debris, and helps confirm exoplanets.', NEO),
      ('When', 'Launched on 25 February 2013; status active.', NEO),
      ('Where', 'About 800 km above Earth.', NEO),
      ('Why', 'Above the weather and the day-night cycle, it can work 24/7 and spot objects hard to see from the ground.', NEO)],
  impact=('NEOSSat adds to the international effort to catalogue near-Earth asteroids and comets, and its astronomy data are open (CSA).', NEO),
  fact=('It Saw NEOWISE', 'NEOSSat imaged comet C/2020 F3 (NEOWISE) on 23 July 2020 (CSA).', NEO),
  people=('Tracking space objects helps keep Canadian and international satellites, which people rely on, safe (CSA).', NEO),
  nature=('Knowing where asteroids are is the first step in protecting Earth and all life on it from an impact (CSA).', NEO),
  support_h='Learn More About NEOSSat',
  btns=[('CSA: NEOSSat', NEO[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? The Canadian Space Agency has the full mission story.', NEO[0], 'For Further Information'),
  widget=None, see=[('NEO_Surveyor.html', 'NEO Surveyor (NASA)', 'An infrared telescope to find hazardous asteroids.')],
  pin=pin(45.52, -73.39, 'Canadian Space Agency headquarters, Longueuil, Quebec', 'orbit')),
 dict(slug='Chandrayaan-5_LUPEX', title='Chandrayaan-5 / LUPEX Moon Ice Rover (ISRO-JAXA)', short='LUPEX', cat='space',
  hub=('Space.html', 'Space'), cls='agency', status='active', glass='space', label='Agency solution · in development',
  img=('Lunar_South_Pole_PIA13523.jpg', 1521, 1521, "The Moon's south pole region, mapped by NASA's Lunar Reconnaissance Orbiter"),
  credit='NASA/GSFC/Arizona State University (PIA13523, the lunar south pole)',
  hook="India and Japan are sending a rover to look for ice at the Moon's south pole.",
  wow=("LUPEX's payload, including a rover, will weigh more than 350 kg, and the mission will operate for more than 3 months (JAXA).", LPX),
  lead='JAXA and ISRO are building LUPEX, also called Chandrayaan-5, to study water at the lunar south pole; launch is no earlier than 2028 on an H3 rocket (JAXA).',
  eli=['Scientists think there may be frozen water hiding near the Moon\'s south pole.',
       'Japan and India are building a rover to drive there and check.',
       'Knowing where the water is will help plan future human trips to the Moon.'],
  ws=[('Who', 'JAXA (Japan) and ISRO (India), with instruments from partners.', LPX),
      ('What', 'A lunar lander and rover to look for water and study how it is held in the Moon\'s polar regions.', LPX),
      ('When', 'Launch no earlier than 2028 on Japan\'s H3 rocket.', LPX),
      ('Where', 'The south pole region of the Moon.', LPX),
      ('Why', 'Understanding water on the Moon matters for future human exploration beyond Earth (JAXA).', LPX)],
  impact=('It builds on India\'s Chandrayaan-3, which soft-landed on the Moon on 23 August 2023 (ISRO).', CH3),
  fact=('Six Tons to the Moon', 'The spacecraft will have a launch mass of around 6 tons or more (JAXA).', LPX),
  people=('Water on the Moon could one day support human explorers (JAXA).', LPX),
  nature=('Studying lunar water helps us understand how planetary bodies keep water, including our own (JAXA).', LPX),
  support_h='Learn More About LUPEX',
  btns=[('JAXA: LUPEX', LPX[0]), ('ISRO: Chandrayaan-3', CH3[0])],
  bottom=('Want to go deeper? JAXA has the full mission plan.', LPX[0], 'For Further Information'),
  widget=W('Chandrayaan-5 / LUPEX', 'In development. JAXA lists launch as no earlier than 2028 on an H3 rocket; no exact date is set.', LPX, 'JAXA / ISRO',
           arrival='2028-01-01T00:00:00Z', arrival_label='launch, no earlier than 2028',
           milestones=[('2023-08-23', 'Chandrayaan-3 lands on the Moon'), ('2028-01-01', 'LUPEX launch, no earlier than 2028')]),
  see=[('Artemis_II.html', 'Artemis II', 'NASA\'s crewed flight around the Moon.')],
  pin=pin(30.40, 130.97, 'Tanegashima Space Center, Japan, the planned H3 launch site', 'orbit')),
]
SHIP = [p['slug'] for p in PAGES]

XBACK = {
 'Predator_Free_2050.html': [('South_Georgia_Habitat_Restoration.html', 'South Georgia Habitat Restoration', 'The world\'s largest island rodent eradication, declared a success in 2018.'),
                             ('Redonda_Restoration.html', 'Redonda Island Restoration', 'A Caribbean island that turned green after rats and goats were removed.')],
 'Oceans.html': [],
 'GOSAT-GW.html': [('GCOM-W_SHIZUKU.html', 'GCOM-W "SHIZUKU" (JAXA)', 'The AMSR2 sea-ice watcher that came before GOSAT-GW.')],
}

ICON = {'Polar.html': '🧊', 'Earth_Observation.html': '🌍', 'Oceans.html': '🌊', 'Deforestation.html': '🌳', 'Rivers.html': '💧', 'Space.html': '🛰️',
        'Lakes.html': '🏞️', 'Planetary_Defense.html': '☄️'}

def main():
    pages = [p for p in PAGES if p['slug'] in SHIP]
    tpl = open(os.path.join(ROOT, 'Surfrider_Foundation.html'), encoding='utf8').read()
    eli = json.load(open(os.path.join(ROOT, 'assets/data/eli10.json'), encoding='utf8'))
    ml = json.load(open(os.path.join(ROOT, 'assets/data/map-locations.json'), encoding='utf8'))
    for p in pages:
        s = p['slug']; im = p['img'][0]
        out = tpl.replace('Surfrider_Foundation', s)
        b, srcs = body(p)
        out = re.sub(r'<main id="main">.*?</main>', lambda m: b, out, count=1, flags=re.S)
        desc = E(p['lead'], quote=True)
        out = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + desc, out)
        out = re.sub(r'<title>[^<]*</title>', f'<title>{E(p["title"])} | Saving Planets</title>', out)
        out = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*', lambda m: m.group(1) + E(p['title']) + ' | Saving Planets', out)
        out = re.sub(r'(<meta (?:property|name)="(?:og:image|twitter:image)" content=")[^"]*', lambda m: m.group(1) + 'https://www.savingplanets.com/assets/' + im, out)
        for k in ('category', 'classification', 'status', 'added'):
            v = {'category': p['cat'], 'classification': p['cls'], 'status': p['status'], 'added': ADDED}[k]
            out = re.sub(r'(sp:' + k + r'" content=")[^"]*', lambda m, v=v: m.group(1) + v, out)
        sl = s.lower().replace('_', '-')
        out = re.sub(r'<body[^>]*>', f'<body data-glass="{p["glass"]}" class="hp-{sl} toc-sub {sl}-page">', out, count=1)
        out = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', out, flags=re.S)
        out = re.sub(r'<!-- (TEACHER|CITE|SHARE):START -->.*?<!-- \1:END -->\n?', '', out, flags=re.S)
        out = out.replace('Surfrider Foundation', p['title']).replace('Surfrider', p['short'])
        open(os.path.join(ROOT, s + '.html'), 'w', encoding='utf8').write(out)
        eli[s + '.html'] = p['eli']
        ml['solutions'][s + '.html'] = p['pin']
    for p in pages:
        hf, hn = p['hub']; s = p['slug']; im, w, h, alt = p['img']
        fp = os.path.join(ROOT, hf); t = open(fp, encoding='utf8').read()
        if f'class="photo-link" href="{s}.html"' in t: continue
        stl = 'Completed' if p['status'] == 'completed' else 'Active'
        card = (f'<article class="card"><div class="image-container"><a class="photo-link" href="{s}.html"><img src="assets/{im}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a></div>'
                f'<p class="sol-badges"><span class="status-badge status-{stl.lower()}">{stl}</span><span class="hub-tag"><span aria-hidden="true">{ICON[hf]}</span> {hn}</span></p>'
                f'<h3><a href="{s}.html">{E(p["title"])}</a></h3><p class="card-blurb">{E(p["lead"])}</p></article>')
        i = t.find('id="missions"'); j = t.find('</div></section>', i)
        k = t.rfind('</article>', i, j) + len('</article>')
        t = t[:k] + card + t[k:]
        open(fp, 'w', encoding='utf8').write(t)
    for f, items in XBACK.items():
        items = [x for x in items if x[0][:-5] in SHIP]
        if not items: continue
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = '<!-- XLINK1020S:START -->' + see_block(items, 'connected-1020s') + '<!-- XLINK1020S:END -->'
        if '<!-- XLINK1020S:START -->' in t:
            t = re.sub(r'<!-- XLINK1020S:START -->.*?<!-- XLINK1020S:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    json.dump(eli, open(os.path.join(ROOT, 'assets/data/eli10.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump(ml, open(os.path.join(ROOT, 'assets/data/map-locations.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    ab_p = os.path.join(ROOT, 'assets/data/anim-banners.json'); ab = json.load(open(ab_p, encoding='utf8'))
    for pg in pages:  # photo banner from the untouched R2 master, page credit (apply-anim-banners.py)
        a = 'assets/' + pg['img'][0]
        ab['images'][a] = {'credit': pg['credit'], 'pos': '50% 50%', 'r2': 'images/' + pg['img'][0]}
        ab['pages'][pg['slug'] + '.html'] = a
    json.dump(ab, open(ab_p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('wrote', len(pages), 'pages')

if __name__ == '__main__':
    main()
