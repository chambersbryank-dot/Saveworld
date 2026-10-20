#!/usr/bin/env python3
"""Oct 19 2026 batch (owner approved all 17, A-Q, Oct 19): Svalbard Global Seed Vault, International Thwaites Glacier
Collaboration, Carbfix, African Parks, Digital Earth Africa, Emirates Mars Mission (Hope), Abu Dhabi mangroves, Gaganyaan G1,
NEWater, Cheonggyecheon, Palau National Marine Sanctuary, Papahanaumokuakea, Predator Free 2050, Galapagos giant tortoises,
MAAP, Mesoamerican Reef insurance, Costa Rica PES. Same writer as batch-1018-content.py (Surfrider_Foundation.html skeleton,
Five W's, widgets after the Five W's, Connected Solutions, XLINK blocks on existing pages) plus a BLUF box (hook + one
sourced wow fact) right after the breadcrumb, styled by the BLUF1019 block in styles.css (written here, idempotent).
Shipped in small batches: SHIP below lists the slugs written so far (A-C, D-H, I-M, N-Q). Every fact is from the cited page
(fetched 2026-10-19); org/company/government figures are labeled as theirs. Re-runnable: overwrites only these pages,
their hub cards (added once) and the XLINK1019 blocks."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b18', os.path.join(ROOT, 'scripts/batch-1018-content.py'))
b18 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b18)
src, W, see_block = b18.b17.src, b18.W, b18.see_block
ADDED = '2026-10-19'
SHIP = ['Svalbard_Global_Seed_Vault', 'Thwaites_Glacier_Collaboration', 'Carbfix', 'African_Parks', 'Digital_Earth_Africa', 'Hope_Mars_Mission', 'Abu_Dhabi_Mangroves', 'Gaganyaan', 'NEWater', 'Cheonggyecheon', 'Palau_National_Marine_Sanctuary', 'Papahanaumokuakea', 'Predator_Free_2050', 'Galapagos_Giant_Tortoises', 'MAAP', 'Mesoamerican_Reef_Insurance', 'Costa_Rica_Forest_Payments']

SV = ('https://www.seedvault.no/', 'Svalbard Global Seed Vault')
SVD = ('https://www.seedvault.no/2026/10/14/thousands-of-seeds-deposited-in-svalbard-as-global-cooperation-safeguards-food-security/', 'Svalbard Global Seed Vault, October 2026 deposit')
CROP = 'https://donate.croptrust.org/'
TGF = ('https://thwaitesglacier.org/about/facts', 'International Thwaites Glacier Collaboration, Facts')
TGR = ('https://thwaitesglacier.org/findings', 'International Thwaites Glacier Collaboration, Findings')
BAS = ('https://www.bas.ac.uk/project/international-thwaites-glacier-collaboration/', 'British Antarctic Survey, International Thwaites Glacier Collaboration')
CF = ('https://www.carbfix.com/our-story', 'Carbfix, Our story')
SCI = ('https://www.science.org/doi/10.1126/science.aad8132', 'Matter et al., Science (2016)')

APS = ('https://www.africanparks.org/about-us/our-story', 'African Parks, Our story')
AP25 = ('https://www.africanparks.org/25-years', 'African Parks, 25 years')
DEA = ('https://www.digitalearthafrica.org/en_za/about-digital-earth-africa/', 'Digital Earth Africa, About')
DEAG = ('https://docs.digitalearthafrica.org/en/latest/data_specs/GeoMAD_specs.html', 'Digital Earth Africa, GeoMAD specifications')
WAMH = ('https://www.wam.ae/en/article/bysbi4j-uae-space-agency-announces-extension-emirates-mars', 'Emirates News Agency (WAM), UAE Space Agency extends Emirates Mars Mission until 2028, 17 Feb 2026')
EADM = ('https://www.mediaoffice.abudhabi/en/environment/environment-agency-abu-dhabi-launches-mangrove-observatory-to-advance-mangrove-restoration-efforts/', 'Abu Dhabi Media Office, EAD launches Mangrove Observatory (July 2026)')
ISROG = ('https://www.isro.gov.in/Gaganyaan.html', 'ISRO, Gaganyaan')
ISROG1 = ('https://www.isro.gov.in/LVM3_first_uncrewed_flight_Gaganyaan.html', 'ISRO, HLVM3 for the first uncrewed Gaganyaan flight')
DDG = ('https://ddnews.gov.in/en/india-targets-first-uncrewed-gaganyaan-mission-with-vyommitra-in-late-2026-human-spaceflight-programme-achieves-major-milestones/', 'DD News, India targets first uncrewed Gaganyaan mission with Vyommitra in late 2026')
CITSCI = 'https://science.nasa.gov/citizen-science/'

PUBN = ('https://www.pub.gov.sg/Public/WaterLoop/OurWaterStory/NEWater', "PUB, Singapore's National Water Agency, NEWater")
CGM = ('https://web.archive.org/web/20250930180135/https://museum.seoul.go.kr/eng/about/cheongGyeMuse.jsp', 'Seoul Museum of History, Cheonggyecheon Museum')
CGE = ('https://encykorea.aks.ac.kr/Article/E0068490', 'Encyclopedia of Korean Culture (Academy of Korean Studies), Cheonggyecheon restoration project')
PICRC = ('https://picrc.org/january-1-2020-pnms-act-enters-into-full-force-with-the-start-of-a-new-decade/', 'Palau International Coral Reef Center, PNMS Act enters into full force (Jan. 1, 2020)')
LEAP = ('https://leap.unep.org/en/countries/pw/national-legislation/palau-national-marine-sanctuary-act-rppl-no-9-49-2015', 'UNEP LEAP, Palau National Marine Sanctuary Act (RPPL No. 9-49 of 2015)')
PIT = ('https://islandtimes.org/president-whipps-outlines-progress-challenges-in-state-of-the-republic-address/', 'Island Times, President Whipps outlines progress and challenges in State of the Republic address (July 2026)')
PINA = ('https://pina.com.fj/2026/10/01/pacific-must-balance-ocean-protection-with-economic-needs-palau-president-whipps/', 'PINA, Pacific must balance ocean protection with economic needs (Oct. 1, 2026)')
PPL = ('https://palaupledge.com/', 'Palau Pledge')
NMS = ('https://sanctuaries.noaa.gov/papahanaumokuakea/', 'NOAA, Papahānaumokuākea National Marine Sanctuary')
PMA = ('https://www.papahanaumokuakea.gov/about/', 'Papahānaumokuākea Marine National Monument, About')
FWSW = ('https://www.fws.gov/story/2026-04/midway-atoll-national-wildlife-refuge-great-monument-people-who-passed-here', 'USFWS, Midway Atoll National Wildlife Refuge (April 2026)')
FOM = 'https://friendsofmidway.org/get-involved/donations/'
DOCW = ('https://www.doc.govt.nz/nature/pests-and-threats/predator-free-2050/what-is-predator-free/', 'DOC, What is Predator Free 2050')
DOCP = ('https://www.doc.govt.nz/nature/pests-and-threats/predator-free-2050/', 'DOC, Predator Free 2050')
DOC16 = ('https://www.doc.govt.nz/news/media-releases/2016/predator-free-nz-2050-to-be-a-massive-team-effort', 'DOC, Predator Free New Zealand 2050 to be a massive team effort (July 25, 2016)')
PFNZ = 'https://predatorfreenz.org/get-involved/'
GAL = ('https://www.galapagos.org/projects/rewilding-galapagos/rewilding-giant-tortoises/', 'Galápagos Conservancy, Rewilding Giant Tortoises')
GALR = ('https://www.galapagos.org/conservation/giant-tortoise-restoration/', 'Galápagos Conservancy, Giant Tortoise Restoration')
GALE = ('https://www.galapagos.org/newsroom/espanola-tortoises-return-home-following-closure-of-successful-breeding-program/', 'Galápagos Conservancy, Española tortoises return home')
GALDON = 'https://www.galapagos.org/give/'
MAAPA = ('https://www.amazonconservation.org/what-we-do/put-science-and-tech-to-work/technology-for-conservation/about-maap/', 'Amazon Conservation, About MAAP')
MAAPH = ('https://www.maapprogram.org/', 'MAAP, Monitoring of the Andes Amazon Program')
ACDON = 'https://www.amazonconservation.org/donate/'
MARL = ('https://www.marfund.org/en/hurricane-lisa-triggers-first-pay-out-of-mesoamerican-reef-insurance-programme-to-finance-immediate-reef-response-in-belize/', 'MAR Fund, Hurricane Lisa triggers first pay-out (Nov. 2022)')
MARF = ('https://www.marfund.org/en/the-mar-insurance-programme-enters-its-fifth-year-advancing-climate-resilience-across-the-mesoamerican-reef/', 'MAR Fund, The MAR Insurance Programme enters its fifth year (Sept. 2025)')
MARDON = 'https://www.marfund.org/en/donate-now'
FONA = ('https://www.fonafifo.go.cr/en/servicios/pago-de-servicios-ambientales', 'FONAFIFO, Payment of Environmental Services')

PAGES = [
 dict(slug='Svalbard_Global_Seed_Vault', title='Svalbard Global Seed Vault', short='the Seed Vault', cat='polar',
  hub=('Polar.html', 'Polar'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Svalbard_Nordaustlandet_Landsat9_2022.jpg', 1920, 2072, 'Glaciers, sea ice and dark Arctic water around Nordaustlandet, Svalbard, seen by Landsat 9'),
  credit='NASA Earth Observatory image by Joshua Stevens, using Landsat 9 data from the USGS (Nordaustlandet, Svalbard, July 29, 2022)',
  hook="Deep inside an Arctic mountain, the world keeps a spare copy of its crops.",
  wow=("The Seed Vault holds 1,417,799 seed samples of 6,587 species, sent by about 135 genebanks and institutions (Seed Vault figures).", SV),
  lead='The Svalbard Global Seed Vault stores backup copies of the world\'s crop seeds free of charge, more than 100 metres inside an Arctic mountain (Seed Vault).',
  eli=['Farmers and scientists keep seeds of thousands of crops in places called genebanks.',
       'The Seed Vault on Svalbard keeps a spare copy of those seeds deep inside a frozen mountain.',
       'If a genebank loses its seeds to war or disaster, it can take its copies back and grow them again.'],
  ws=[('Who', 'Norway, through its Ministry of Agriculture and Food, runs the vault with NordGen and the Crop Trust.', SV),
      ('What', 'A long-term backup store for duplicate seed samples from genebanks around the world, free of charge.', SV),
      ('When', 'Opened on Feb. 26, 2008. On Oct. 13, 2026, it received 16,676 samples from 21 institutions.', SVD),
      ('Where', 'More than 100 metres inside a mountain near Longyearbyen on Svalbard, Norway, in the Arctic.', SV),
      ('Why', 'Genebanks can lose seeds to war, disaster or failing equipment. The vault keeps a safe copy for them.', SV)],
  impact=('ICARDA became the first depositor to take seeds back out, to rebuild its genebank collection (Seed Vault).', SV),
  fact=('Ukraine\'s Seeds Are Safe', 'The October 2026 deposit included 773 samples from Ukraine\'s national genebank and 8,917 from CGIAR genebanks (Seed Vault).', SVD),
  people=('The vault is part of the global community\'s joint effort to ensure the world\'s future food supply (Seed Vault).', SV),
  nature=('Seeds of 6,587 species are stored there, so the diversity of the world\'s crops has a safe backup (Seed Vault figures).', SV),
  support_h='Support the Seed Vault', donate_alt='Donate to the Crop Trust',
  btns=[('Donate to the Crop Trust', CROP), ('Learn About the Seed Vault', SV[0])],
  bottom=('The Crop Trust, a partner of the vault, takes donations for crop diversity.', CROP, 'Donate'),
  widget=None, see=[('Biomass.html', 'Biomass Forest Mission (ESA)', 'Measures the forests that hold much of the planet\'s plant life.')],
  pin={'status': 'active', 'pins': [{'lat': 78.2357, 'lng': 15.4913, 'label': 'Svalbard Global Seed Vault, near Longyearbyen, Svalbard, Norway', 'basis': 'page'}]}),
 dict(slug='Thwaites_Glacier_Collaboration', title='International Thwaites Glacier Collaboration', short='the Thwaites Collaboration', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('Thwaites_Glacier_Landsat8_2019.jpg', 1920, 1467, 'The cracked ice front of Thwaites Glacier in West Antarctica meeting the sea, seen by Landsat 8'),
  credit='NASA Earth Observatory image by Lauren Dauphin, using Landsat 8 data from the USGS (Thwaites Glacier, Dec. 28, 2019)',
  hook="About 100 scientists spent years on the glacier that could change every coastline.",
  wow=("If Thwaites Glacier were lost completely, it would raise global sea level by 65 cm (ITGC).", TGF),
  lead='About 100 scientists from the UK, US, South Korea, Germany and Sweden are working out how fast Antarctica\'s Thwaites Glacier could raise sea levels (ITGC).',
  eli=['Thwaites is a giant glacier in Antarctica, the widest on Earth.',
       'It is melting and sliding into the sea, which makes the oceans rise a little.',
       'Scientists went there to find out how fast it could change, so coastal towns can plan.'],
  ws=[('Who', 'The UK\'s Natural Environment Research Council (NERC) and the US National Science Foundation (NSF), with about 100 scientists.', BAS),
      ('What', 'The largest UK-US Antarctic research collaboration in over 70 years, studying how Thwaites is changing and what could happen next.', BAS),
      ('When', 'From April 2018. The programme runs until Dec. 1, 2026 (British Antarctic Survey).', BAS),
      ('Where', 'Thwaites Glacier in West Antarctica, about 120 km wide, draining a basin of 192,000 square kilometres.', TGF),
      ('Why', 'Thwaites accounts for about 4% of global sea-level rise, a rate that has trebled since the mid-1990s (British Antarctic Survey).', BAS)],
  impact=('ITGC findings say Thwaites will keep retreating, further and faster, through the 21st and 22nd centuries; cutting emissions is the best hope of slowing it (ITGC).', TGR),
  fact=('50 Billion Tonnes a Year', 'Each year Thwaites loses about 50 billion tonnes more ice than it gains from snowfall (ITGC).', TGF),
  people=('Understanding the glacier\'s future is critical for planning and adapting to climate change, including on the world\'s coasts (British Antarctic Survey).', BAS),
  nature=('Understanding Thwaites shows how Antarctic ice, the ocean beneath it and the climate are linked (ITGC).', TGF),
  support_h='Learn More About Thwaites',
  btns=[('Read the Findings', TGR[0]), ('Thwaites Facts', TGF[0])],
  bottom=('Want to go deeper? The collaboration shares its findings in plain language.', TGR[0], 'For Further Information'),
  widget=W('International Thwaites Glacier Collaboration', 'Research programme from April 2018 to Dec. 1, 2026, funded by NERC and NSF (British Antarctic Survey).', BAS, 'British Antarctic Survey',
           arrival='2026-12-01T00:00:00Z', arrival_label='programme end, Dec. 1, 2026',
           milestones=[('2018-04-01', 'Programme begins'), ('2026-12-01', 'Programme ends')]),
  see=[('CryoSat.html', 'CryoSat Ice Mission (ESA)', 'Measures how the polar ice sheets are changing from orbit.')],
  pin={'status': 'active', 'pins': [{'lat': -75.5, 'lng': -106.75, 'label': 'Thwaites Glacier, West Antarctica', 'basis': 'page'}]}),
 dict(slug='Carbfix', title='Carbfix: Turning CO2 Into Stone', short='Carbfix', cat='polar',
  hub=('Polar.html', 'Polar'), cls='corporate', status='active', glass='earth', label='Company solution · active',
  img=('Iceland_Volcanic_Landscape_jsc2026e406058.jpg', 1920, 1144, 'Two people crossing a dark volcanic lava plain in Iceland'),
  credit='NASA/James Blair (jsc2026e406058, volcanic landscape in Iceland)',
  hook="In Iceland, carbon dioxide is being turned into rock.",
  wow=("In a 2012 test, over 95% of the injected CO2 turned to stone in less than two years (Science, 2016).", SCI),
  lead='Carbfix dissolves carbon dioxide in water and injects it into basalt rock, where it turns into stone (company).',
  eli=['Carbon dioxide is a gas that warms the planet.',
       'Carbfix mixes it with water, like fizzy water, and pumps it deep into volcanic rock.',
       'There the gas reacts with the rock and becomes solid stone that stays put.'],
  ws=[('Who', 'Carbfix, a subsidiary of Reykjavík Energy (OR) that began operating as its own company on Jan. 1, 2020. It began as a project of Reykjavík Energy, the University of Iceland, CNRS and Columbia University\'s Earth Institute.', CF),
      ('What', 'CO2 is dissolved in water and injected underground, where it reacts with basalt and turns into carbonate minerals.', CF),
      ('When', 'Started in 2006 and formalized in 2007. Injection at industrial scale at Hellisheiði has run since 2014.', CF),
      ('Where', 'At the Hellisheiði geothermal power plant in Iceland, in basalt rock.', CF),
      ('Why', 'Rock storage keeps CO2 out of the atmosphere for good. The company\'s goal is to store 1 billion tonnes of CO2.', CF)],
  impact=('In the 2012 pilot, 175 tonnes of CO2 were injected at about 500 m depth, and over 95% mineralized in less than two years (Science, 2016).', SCI),
  fact=('About $25 a Tonne', 'Carbfix puts its on-site cost at about US $24.8 per tonne of CO2 (company figure).', CF),
  people=('At Hellisheiði, CO2 and hydrogen sulphide are captured from a geothermal power plant\'s emissions and stored as rock (Carbfix).', CF),
  nature=('Carbfix copies a natural process: CO2 and rock form stable carbonate minerals, a permanent and environmentally benign store (Carbfix).', CF),
  support_h='Learn More About Carbfix',
  btns=[('Carbfix\'s Story', CF[0]), ('Read the Science Study', SCI[0])],
  bottom=('Want to go deeper? Carbfix explains how CO2 turns to stone.', CF[0], 'For Further Information'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 64.037, 'lng': -21.40, 'label': 'Hellisheiði geothermal power plant, Iceland', 'basis': 'page'}]}),
 dict(slug='African_Parks', title='African Parks', short='African Parks', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='forests', label='Nonprofit solution · active',
  img=('Lake_Kariba_ISS_2024.jpg', 1920, 1280, 'Lake Kariba on the Zambia-Zimbabwe border, with its winding shoreline and dry hills, seen from the International Space Station'),
  credit='NASA (iss071e047913, Lake Kariba between Zambia and Zimbabwe, May 2, 2024)',
  hook="One nonprofit now runs 24 of Africa's wild places with their governments and neighbours.",
  wow=("Over 25 years, African Parks has moved 11,610 animals of 37 species, 18 of which had become locally extinct (nonprofit figures).", AP25),
  lead='African Parks manages 24 protected areas in 13 countries, covering over 20 million hectares, in partnership with governments and local communities (nonprofit).',
  eli=['Some of Africa\'s national parks were losing their animals because there was not enough money or care.',
       'African Parks works with each country\'s government to run those parks well.',
       'It brings back animals that had disappeared and helps the people who live nearby.'],
  ws=[('Who', 'African Parks, a non-profit conservation organisation, working in partnership with governments and local communities.', APS),
      ('What', 'It takes on the long-term management of protected areas, run with a clear business approach.', APS),
      ('When', 'Founded in 2000, in response to the dramatic decline of protected areas from poor management and lack of funding.', APS),
      ('Where', '24 protected areas in 13 countries, from Zakouma in Chad to Matusadona in Zimbabwe.', APS),
      ('Why', 'So each park is ecologically, socially and financially sustainable for the long term. Its goal is 30 parks by 2030.', APS)],
  impact=('African Parks reports 11,610 animals of 37 species translocated over 25 years to restore how ecosystems work (nonprofit figures).', AP25),
  fact=('Back From Local Extinction', 'Of the 37 species African Parks has moved, 18 had disappeared from the area before they were brought back (nonprofit figures).', AP25),
  people=('African Parks focuses on economic development and on reducing poverty in the communities around each park (African Parks).', APS),
  nature=('Its parks cover over 20 million hectares of wild land across 13 countries (African Parks).', APS),
  support_h='Support African Parks',
  btns=[('Donate', 'https://www.africanparks.org/donate'), ('Learn About African Parks', APS[0])],
  bottom=('Support African Parks directly.', 'https://www.africanparks.org/donate', 'Donate'),
  widget=None, see=[('Forest_Elephants.html', 'Forest Elephants, Carbon Gardeners', 'Elephants that help forests store more carbon.')],
  pin={'status': 'active', 'pins': [{'lat': -16.85, 'lng': 28.55, 'label': 'Matusadona National Park, Zimbabwe', 'basis': 'page'}, {'lat': 10.9, 'lng': 19.8, 'label': 'Zakouma National Park, Chad', 'basis': 'page'}]}),
 dict(slug='Digital_Earth_Africa', title='Digital Earth Africa', short='Digital Earth Africa', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Research programme solution · active',
  img=('Okavango_Delta_ISS_2025.jpg', 1920, 1078, 'The Okavango Delta in Botswana fanning out into the Kalahari, seen from the International Space Station'),
  credit='NASA (iss073e0604445, Okavango Delta, Botswana, Aug. 30, 2025)',
  hook="Free satellite maps of an entire continent, for anyone who needs them.",
  wow=("Its Landsat-based maps of Africa reach back to 1984, so users can see four decades of change (Digital Earth Africa).", DEAG),
  lead='Digital Earth Africa turns satellite data into free and open maps of water, farmland and coasts for the whole African continent (Digital Earth Africa).',
  eli=['Satellites take pictures of Africa all the time, but the raw data is hard to use.',
       'Digital Earth Africa cleans it up and turns it into ready-made maps.',
       'Anyone can use them for free to track water, crops and coastlines.'],
  ws=[('Who', 'Digital Earth Africa, a programme of icipe, the International Centre of Insect Physiology and Ecology, built on partnerships with African institutions.', DEA),
      ('What', 'An operational service that delivers free and open satellite data and products, such as Water Observations from Space and a cropland map.', DEA),
      ('When', 'Running now as an operational service; its Landsat-based maps go back to 1984.', DEAG),
      ('Where', 'The entire African continent.', DEA),
      ('Why', 'To give planners and policy makers Earth observation information for better decisions and sustainable development.', DEA)],
  impact=('Digital Earth Africa provides free and open data and products to all its users as a public good (Digital Earth Africa).', DEA),
  fact=('Four Decades of Africa', 'Digital Earth Africa\'s Landsat-based maps of Africa start in 1984 (Digital Earth Africa).', DEAG),
  people=('Earth observation data support better decisions by governments and sectors, with benefits for individuals and communities (Digital Earth Africa).', DEA),
  nature=('Its services track water bodies, land degradation and coastal erosion across the continent (Digital Earth Africa).', DEA),
  support_h='Use Digital Earth Africa',
  btns=[('Explore the Map', 'https://maps.digitalearth.africa/'), ('About Digital Earth Africa', DEA[0])],
  bottom=('Want to go deeper? Digital Earth Africa explains its data and services.', DEA[0], 'For Further Information'),
  widget=None, see=[('Landsat_9.html', 'Landsat 9 (NASA/USGS)', 'Part of the Landsat record of Earth\'s land that began in 1972.')],
  pin={'status': 'active', 'pins': [{'lat': -1.2216, 'lng': 36.8962, 'label': 'icipe, Nairobi, Kenya (host of the programme)', 'basis': 'hq'}], 'strip': 'orbit'}),
 dict(slug='Hope_Mars_Mission', title='Emirates Mars Mission (Hope Probe)', short='the Hope Probe', cat='space',
  hub=('Space.html', 'Space'), cls='agency', status='active', glass='mars', label='Agency solution · active',
  img=('Valles_Marineris_Viking_PIA00422.jpg', 1920, 682, 'Valles Marineris, the great canyon system of Mars, in a colour mosaic from NASA\'s Viking orbiters'),
  credit='NASA/JPL/USGS (PIA00422, Valles Marineris, Viking orbiter mosaic)',
  hook="The Arab world's first interplanetary mission is still sending home Martian weather.",
  wow=("Hope set out to collect a terabyte of new data on Mars's atmosphere and has gathered ten (UAE Space Agency).", WAMH),
  lead='The UAE\'s Hope Probe has studied the Martian atmosphere from orbit since 2021, and its mission is now extended until 2028 (UAE Space Agency).',
  eli=['Hope is a spacecraft from the United Arab Emirates that circles Mars.',
       'It studies the air and weather on Mars, all around the planet.',
       'Scientists everywhere can download its data for free to learn how planets change.'],
  ws=[('Who', 'The UAE Space Agency. The Emirates Mars Mission is the first interplanetary exploration undertaken by an Arab nation.', WAMH),
      ('What', 'The Hope Probe, an orbiter that studies Mars\'s atmosphere and climate, and has also flown past the moon Deimos.', WAMH),
      ('When', 'In Mars orbit since 2021. Planned for two years, the mission is now extended until 2028.', WAMH),
      ('Where', 'In orbit around Mars. In October 2025 it also imaged the interstellar comet 3I/ATLAS.', WAMH),
      ('Why', 'To give the world unique data on the Martian atmosphere and build experience for future deep-space missions.', WAMH)],
  impact=('Hope\'s 10 terabytes of data have gone out in 16 releases to more than 200 academic and research institutions, and fed more than 35 peer-reviewed papers (UAE Space Agency).', WAMH),
  fact=('A Comet From Another Star', 'In October 2025, Hope turned away from Mars to photograph Comet 3I/ATLAS, the third known interstellar object (UAE Space Agency).', WAMH),
  people=('The UAE Space Agency says the mission helps improve understanding of climate change and has helped build the country\'s science and education ecosystem.', WAMH),
  nature=('Hope has made pioneering observations of the Martian aurora and given a new understanding of where the moon Deimos came from (UAE Space Agency).', WAMH),
  support_h='Learn More About Hope',
  btns=[('Mission Extension News', WAMH[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? The UAE Space Agency has the latest on Hope.', WAMH[0], 'For Further Information'),
  widget=W('Emirates Mars Mission (Hope)', 'Active in Mars orbit since 2021. The UAE Space Agency has extended the mission until 2028.', WAMH, 'UAE Space Agency',
           milestones=[('2025-10-03', 'Comet 3I/ATLAS passes closest to Mars, and Hope images it'), ('2026-02-17', 'Mission extended until 2028')]),
  see=[('Project-Rawane.html', 'Project Rawane', 'Our hub for missions that keep space safe and go further out.'), ('Voyager.html', 'Voyager 1 and 2 (NASA)', 'The farthest spacecraft from Earth.')],
  pin={'status': 'active', 'pins': [{'lat': 24.45, 'lng': 54.38, 'label': 'UAE Space Agency, United Arab Emirates', 'basis': 'hq'}], 'strip': 'orbit'}),
 dict(slug='Abu_Dhabi_Mangroves', title='Abu Dhabi Mangrove Restoration', short='Abu Dhabi\'s mangroves', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='government', status='active', glass='ocean', label='Government solution · active',
  img=('Abu_Dhabi_Coast_ISS_2024.jpg', 1920, 1280, 'The shallow turquoise coast and islands of Abu Dhabi, seen from the International Space Station'),
  credit='NASA (iss071e378611, Abu Dhabi, July 23, 2024)',
  hook="Abu Dhabi now tracks its mangroves by how many survive, not just how many go in the ground.",
  wow=("Across 19 active projects, more than 18.5 million mangroves have been planted, with a 46.94% average success rate (EAD figures).", EADM),
  lead='The Environment Agency – Abu Dhabi tracks more than 18.5 million mangroves planted across over 1,775 hectares with its new Mangrove Observatory (government figures).',
  eli=['Mangroves are trees that grow in salty water along the coast.',
       'Abu Dhabi is planting millions of them to bring its coastal forests back.',
       'A new website uses satellites and field checks to see how many really grow.'],
  ws=[('Who', 'The Environment Agency – Abu Dhabi (EAD), under the Abu Dhabi Mangrove Initiative. Dolphin Energy funds the observatory.', EADM),
      ('What', 'The ADMI Mangrove Observatory, a digital platform that brings together restoration data from 19 active projects.', EADM),
      ('When', 'The observatory launched in July 2026. The Abu Dhabi Mangrove Initiative began in 2022.', EADM),
      ('Where', 'Restoration sites along the coast of Abu Dhabi, United Arab Emirates.', EADM),
      ('Why', 'EAD says restoration must be measured by ecosystem recovery and long-term impact, not by trees planted alone.', EADM)],
  impact=('The observatory records a total growth count of more than 10.4 million mangroves across over 1,775 hectares of restored habitat (EAD figures).', EADM),
  fact=('Counting What Survives', 'Field surveys, satellite images and partner reports feed one system, so planners can see growth and gaps (EAD).', EADM),
  people=('Shared data help EAD and its partners coordinate restoration zones and plan using science (EAD).', EADM),
  nature=('Restored mangrove habitat supports long-term ecosystem recovery and resilience along the coast (EAD).', EADM),
  support_h='Learn More About the Observatory',
  btns=[('Visit the Mangrove Observatory', 'https://admangroveobservatory.ead.ae/'), ('Read the Launch News', EADM[0])],
  bottom=('Want to go deeper? The observatory shows the latest restoration data.', 'https://admangroveobservatory.ead.ae/', 'For Further Information'),
  widget=None, see=[('Mangroves.html', 'Mangroves', 'Why coastal mangrove forests matter, and the teams restoring them.')],
  pin={'status': 'active', 'pins': [{'lat': 24.45, 'lng': 54.43, 'label': 'Abu Dhabi coast, United Arab Emirates', 'basis': 'page'}]}),
 dict(slug='Gaganyaan', title='Gaganyaan G1 Uncrewed Flight (ISRO)', short='Gaganyaan', cat='space',
  hub=('Space.html', 'Space'), cls='agency', status='active', glass='space', label='Agency solution · in development',
  img=('South_India_Sri_Lanka_ISS_2024.jpg', 1920, 1280, 'Southern India and Sri Lanka under scattered clouds, seen from the International Space Station'),
  credit='NASA (iss071e014023, Sri Lanka and southern India, April 20, 2024)',
  hook="India is testing its first crew capsule with a robot in the seat.",
  wow=("The human-rated HLVM3 rocket stands 53 metres tall and weighs 640 tonnes, with an escape system to pull the crew module clear (ISRO).", ISROG1),
  lead='Gaganyaan G1, ISRO\'s first uncrewed Gaganyaan flight, is targeted for late 2026 on the human-rated HLVM3 rocket (ISRO).',
  eli=['India wants to send its own astronauts into space.',
       'First, it will fly the crew capsule with a robot called Vyommitra instead of people.',
       'If the test goes well, astronauts can fly on later missions.'],
  ws=[('Who', 'The Indian Space Research Organisation (ISRO).', ISROG),
      ('What', 'The first uncrewed flight of Gaganyaan, carrying the half-humanoid robot Vyommitra to test systems before crewed flights.', DDG),
      ('When', 'Targeted for the last quarter of 2026. ISRO has not announced a launch date.', DDG),
      ('Where', 'From the Satish Dhawan Space Centre (SDSC), Sriharikota, into low Earth orbit.', ISROG1),
      ('Why', 'Gaganyaan aims to fly a crew of 3 to a 400 km orbit for 3 days and bring them back safely to Earth (ISRO).', ISROG)],
  impact=('HLVM3 is a three-stage rocket that can carry about 10 tonnes to low Earth orbit, rebuilt from LVM3 to meet human safety requirements (ISRO).', ISROG1),
  fact=('Stacking Began in 2024', 'On Dec. 18, 2024, ISRO began stacking the HLVM3 rocket for the G1 mission at SDSC-SHAR (ISRO).', ISROG1),
  people=('Gaganyaan builds life support, crew escape and crew safety know-how for human spaceflight (ISRO).', ISROG),
  nature=('ISRO lists space station building and crewed missions to the Moon and Mars among the future work Gaganyaan prepares for (ISRO).', ISROG),
  support_h='Learn More About Gaganyaan',
  btns=[('ISRO Gaganyaan', ISROG[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ISRO has the full Gaganyaan story.', ISROG[0], 'For Further Information'),
  widget=W('Gaganyaan G1', 'Target: late 2026 (fourth quarter). Launch date TBA; ISRO has not set a date yet.', DDG, 'ISRO',
           milestones=[('2024-12-18', 'HLVM3 stacking begins at SDSC-SHAR')], news='Gaganyaan'),
  see=[],
  pin={'status': 'active', 'pins': [{'lat': 13.72, 'lng': 80.23, 'label': 'Satish Dhawan Space Centre, Sriharikota, India (launch site)', 'basis': 'launch'}], 'strip': 'orbit'}),
 dict(slug='NEWater', title="NEWater, Singapore's Recycled Water (PUB)", short='NEWater', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Singapore_Night_ISS_2025.jpg', 1920, 1280, 'Singapore and Johor Bahru, Malaysia, glowing at night on either side of the Johor Strait, seen from the International Space Station'),
  credit='NASA (iss073e0763866, Singapore at night, Sept. 21, 2025)',
  hook='Singapore cleans its used water until it is ultra-clean, then uses it again.',
  wow=('On Aug. 9, 2002, 60,000 people at the National Day Parade toasted the nation with bottles of NEWater (PUB).', PUBN),
  lead="NEWater is high-grade reclaimed water from PUB, Singapore's National Water Agency, made from treated used water in a three-step purification process at 4 plants (PUB).",
  eli=['Singapore is a small island without much room to store rain.',
       'So it takes water that has already been used, cleans it with special filters and ultraviolet light, and makes it ultra-clean.',
       'Factories use most of it, and in dry spells some is added to reservoirs.'],
  ws=[('Who', "PUB, Singapore's National Water Agency.", PUBN),
      ('What', 'NEWater: treated used water purified by microfiltration or ultrafiltration, reverse osmosis and ultraviolet disinfection.', PUBN),
      ('When', 'PUB set up a test team in 1998, built a demonstration plant in 2000 and launched NEWater to the public in 2002.', PUBN),
      ('Where', 'Singapore, where 4 NEWater plants are in operation today.', PUBN),
      ('Why', "To help close the water loop and strengthen Singapore's water resilience (PUB).", PUBN)],
  impact=("Experts found NEWater's quality consistently safe and well within WHO and USEPA drinking water requirements (PUB).", PUBN),
  fact=('Its Biggest Users Are Chip Makers', 'The biggest users are wafer fabrication plants, which need water quality even more stringent than drinking water (PUB).', PUBN),
  people=('In dry periods, NEWater is added to reservoirs, then treated again at waterworks before it reaches homes as tap water (PUB).', PUBN),
  nature=('By recycling treated used water, NEWater helps close the water loop (PUB).', PUBN),
  support_h='Learn More About NEWater',
  btns=[("PUB's NEWater Story", PUBN[0])],
  bottom=('Want to go deeper? PUB tells the full NEWater story.', PUBN[0], 'For Further Information'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 1.3521, 'lng': 103.8198, 'label': 'Singapore', 'basis': 'page'}]}),
 dict(slug='Cheonggyecheon', title='Cheonggyecheon Stream Restoration (Seoul)', short='Cheonggyecheon', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Seoul_Night_ISS_2025.jpg', 1920, 1280, 'Seoul at night, split by the dark curve of the Han River, seen from the International Space Station'),
  credit='NASA (iss072e757318, Seoul at night, March 5, 2025)',
  hook='Seoul tore down a motorway to let a buried stream see daylight again.',
  wow=('In the month after it reopened on Oct. 1, 2005, about 6.27 million people visited the restored stream (Encyclopedia of Korean Culture).', CGE),
  lead='Seoul removed an ageing road and elevated motorway that covered the Cheonggyecheon stream and restored it along a 5.84 km corridor through the city centre (Cheonggyecheon Museum).',
  eli=['A stream in the middle of Seoul was covered with concrete and a highway was built on top.',
       'The city took the highway down and opened the stream up again.',
       'Now people walk beside the water in the heart of the city.'],
  ws=[('Who', 'The Seoul Metropolitan Government.', CGM),
      ('What', 'The Cheonggyecheon Restoration Project, which demolished the old road and elevated motorway and brought the stream back.', CGM),
      ('When', 'From July 2003 to Oct. 1, 2005, two years and three months.', CGM),
      ('Where', 'A 5.84 km corridor through central Seoul, South Korea.', CGM),
      ('Why', 'The road and motorway were badly ageing, and many argued the stream should be restored rather than spending more on maintenance (Cheonggyecheon Museum).', CGM)],
  impact=('The museum says the project changed the face of the city forever, as ecology and heritage became goals ahead of growth and development (Cheonggyecheon Museum).', CGM),
  fact=('Down in About a Month', 'The Cheonggye elevated motorway was fully demolished by Aug. 3, 2003, about a month after work began (Encyclopedia of Korean Culture).', CGE),
  people=('Its museum, with exhibition halls and an auditorium for cultural events, tells visitors the story of the restoration (Cheonggyecheon Museum).', CGM),
  nature=('The Encyclopedia of Korean Culture describes the project as more than a stream restoration: a restoration of history, culture and life (Encyclopedia of Korean Culture).', CGE),
  support_h='Learn More About Cheonggyecheon',
  btns=[('Cheonggyecheon Museum', CGM[0])],
  bottom=('Want to go deeper? The Cheonggyecheon Museum tells the restoration story.', CGM[0], 'For Further Information'),
  widget=None, see=[('Elwha_River_Restoration.html', 'Elwha River Restoration', 'Two Elwha River dams came down between 2011 and 2014.')],
  pin={'status': 'active', 'pins': [{'lat': 37.5692, 'lng': 126.9784, 'label': 'Cheonggyecheon, Seoul, South Korea', 'basis': 'page'}]}),
 dict(slug='Palau_National_Marine_Sanctuary', title='Palau National Marine Sanctuary', short='the Palau sanctuary', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='government', status='active', glass='ocean', label='Government solution · active',
  img=('Palau_Landsat8_2014.jpg', 1920, 1280, 'The green islands of Palau ringed by turquoise reefs in a deep blue Pacific, seen by Landsat 8'),
  credit='NASA Earth Observatory/Jesse Allen, Landsat 8 data from USGS (Palau, March 21, 2014)',
  hook='A small island nation closed most of its ocean to fishing.',
  wow=("Since Jan. 1, 2020, about 500,000 km² of Palau's ocean, 80% of its exclusive economic zone, has been closed to all fishing and extraction (PICRC).", PICRC),
  lead="The Palau National Marine Sanctuary makes about 80% of Palau's exclusive economic zone a no-take area, with the other 20% kept as a Domestic Fishing Zone (Government of Palau law).",
  eli=["Palau is a country made of islands in the Pacific Ocean.",
       'It decided that most of its ocean should be a place where nobody fishes.',
       'That gives sea life room to grow back and spill over into the areas where local people fish.'],
  ws=[('Who', 'The Republic of Palau. The Palau International Coral Reef Center is the administrator of the sanctuary.', PPL),
      ('What', 'A no-take marine sanctuary covering about 80% of Palau\'s exclusive economic zone, plus a 20% Domestic Fishing Zone.', LEAP),
      ('When', 'Signed into law on Oct. 28, 2015 (RPPL No. 9-49) and in full force since Jan. 1, 2020.', PICRC),
      ('Where', 'The waters around Palau in the western Pacific Ocean.', PICRC),
      ('Why', 'To protect most of Palau\'s ocean from all exploitation while local fishing continues in the other 20% (UNEP LEAP).', LEAP)],
  impact=('PICRC says the sanctuary offers better protection to nearly 800 animal species, nine of them endangered (PICRC).', PICRC),
  fact=('Status in 2026', "No rollback has been enacted. In July 2026 President Whipps proposed \"rightsizing\" the no-take area from 80% to about 30% and sent the plan to Palau's national congress; as of October 2026 it was still under review, with critics including a former president (Island Times; PINA).", PIT),
  people=("Palau was the first nation to change its immigration laws for the environment: visitors sign the Palau Pledge on arrival (Palau Pledge).", PPL),
  nature=('PICRC says the no-take zone aims to improve marine biodiversity and nurture stronger pelagic fisheries for the people of Palau (PICRC).', PICRC),
  support_h='Help Protect Palau',
  btns=[('Learn About the Palau Pledge', PPL[0]), ('Read the PICRC Update', PICRC[0])],
  bottom=('Visiting Palau? Learn the Palau Pledge first.', PPL[0], 'Palau Pledge'),
  widget=None, see=[('Mission_Blue_Hope_Spots.html', 'Mission Blue Hope Spots', 'Special places in the ocean that people are working to protect.')],
  pin={'status': 'active', 'pins': [{'lat': 7.515, 'lng': 134.58, 'label': 'Palau', 'basis': 'page'}]}),
 dict(slug='Papahanaumokuakea', title='Papahānaumokuākea National Marine Sanctuary', short='Papahānaumokuākea', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='government', status='active', glass='ocean', label='Government solution · active',
  img=('Pearl_Hermes_Atoll_ISS_2002.jpg', 1920, 1254, 'The turquoise lagoon and reef rim of Pearl and Hermes Atoll in the Northwestern Hawaiian Islands, seen from the International Space Station'),
  credit='NASA (ISS005-E-13929, Pearl and Hermes Atoll, Sept. 12, 2002)',
  hook="One of the world's largest protected seas sits just northwest of the main Hawaiian Islands.",
  wow=("Wisdom, the Laysan albatross of Midway Atoll, is the oldest known wild bird, at an approximate age of 75 (USFWS).", FWSW),
  lead="Designated in 2025 as America's 18th national marine sanctuary, Papahānaumokuākea covers 582,570 square miles of Pacific Ocean around Hawaiʻi (NOAA).",
  eli=['Far out in the ocean past the main Hawaiian islands is a long chain of tiny islands and reefs.',
       'The United States protects the ocean all around them.',
       'Millions of seabirds nest there, and it is a sacred place for Native Hawaiians.'],
  ws=[('Who', 'Three co-trustees and seven co-managing agencies, including NOAA, which runs the sanctuary.', PMA),
      ('What', 'The largest marine protected area in the U.S. National Marine Sanctuary System, protecting nature, culture and history.', NMS),
      ('When', 'First protected as a marine national monument on June 15, 2006, and designated a national marine sanctuary in 2025.', PMA),
      ('Where', 'The Northwestern Hawaiian Islands, including Nihoa, Mokumanamana and Midway Atoll.', PMA),
      ('Why', 'To protect ecosystem health and diversity and the Native Hawaiian cultural significance of the area (Papahānaumokuākea).', PMA)],
  impact=('Its reefs are home to over 7,000 marine species, a quarter of them found only in the Hawaiian Archipelago (Papahānaumokuākea).', PMA),
  fact=('A Long Life at Sea', 'Wisdom is estimated to have produced 50 to 60 eggs and 30 chicks that fledged in her lifetime (USFWS).', FWSW),
  people=('It became the first mixed natural and cultural UNESCO World Heritage Site in the United States, on July 30, 2010 (Papahānaumokuākea).', PMA),
  nature=('About 14 million seabirds of 22 species breed and nest there, along with endangered Hawaiian monk seals (Papahānaumokuākea).', PMA),
  support_h='Support Midway Atoll',
  btns=[('Donate to Friends of Midway Atoll', FOM), ('Learn About the Sanctuary', NMS[0])],
  bottom=('Support Friends of Midway Atoll National Wildlife Refuge.', FOM, 'Donate'),
  widget=None, see=[('Mission_Blue_Hope_Spots.html', 'Mission Blue Hope Spots', 'Special places in the ocean that people are working to protect.')],
  pin={'status': 'active', 'pins': [{'lat': 28.21, 'lng': -177.37, 'label': 'Midway Atoll, Papahānaumokuākea', 'basis': 'page'}, {'lat': 23.06, 'lng': -161.92, 'label': 'Nihoa, Papahānaumokuākea', 'basis': 'page'}]}),
 dict(slug='Predator_Free_2050', title='Predator Free 2050 (New Zealand)', short='Predator Free 2050', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='government', status='active', glass='forests', label='Government solution · active',
  img=('NZ_Southern_Lakes_ISS_2024.jpg', 1920, 1280, 'Lakes Tekapo, Pukaki and Ōhau, bright blue among snowy mountains near the Southern Alps of New Zealand, seen from the International Space Station'),
  credit='NASA (iss071e073568, Lakes Tekapo, Pukaki and Ōhau, New Zealand, May 11, 2024)',
  hook='New Zealand wants to remove its most harmful introduced predators from the whole country.',
  wow=('Introduced rats, possums, feral cats and mustelids kill an estimated 25 million native birds in New Zealand each year (DOC).', DOCW),
  lead='Predator Free 2050 is a nationwide goal to eradicate rats, possums, feral cats and mustelids from all of Aotearoa New Zealand by 2050, with the Department of Conservation as lead agency (DOC).',
  eli=["New Zealand's birds grew up with no mammals that hunt them.",
       'Then people brought rats, stoats, possums and cats, which eat birds and their eggs.',
       'The country is working to remove those predators everywhere by 2050.'],
  ws=[('Who', "The New Zealand Government, with the Department of Conservation (DOC) as lead agency, and iwi, hapū, NGOs, businesses, community groups and scientists.", DOCW),
      ('What', 'A goal, a movement and a government-funded programme to eradicate the most harmful introduced predators.', DOCW),
      ('When', 'Announced on July 25, 2016, with a target of 2050.', DOC16),
      ('Where', 'All of Aotearoa New Zealand.', DOCW),
      ('Why', 'Introduced predators are one of the key threats to native species, which evolved without mammals (DOC).', DOCW)],
  impact=('DOC reports that kākā now live alongside people in Wellington and kiwi share backyards on Waiheke Island (DOC).', DOCP),
  fact=('Eradication, Not Just Control', 'The aim is to remove every last animal and stop them from coming back, which is much harder than keeping numbers down (DOC).', DOCW),
  people=('Anyone can help, from backyard traps to community projects across the country (DOC).', DOCP),
  nature=('The target species were chosen as the most harmful to native wildlife and realistic to eradicate by 2050 (DOC).', DOCW),
  support_h='Get Involved',
  btns=[('Get Involved With Predator Free NZ', PFNZ), ('Learn About Predator Free 2050', DOCW[0])],
  bottom=('Join the Predator Free movement.', PFNZ, 'Get Involved'),
  widget=None, see=[('Yellowstone_Wolves.html', 'Yellowstone Wolves', 'Gray wolves returned to Yellowstone in 1995 after nearly 70 years.')],
  pin={'status': 'active', 'pins': [{'lat': -41.29, 'lng': 174.78, 'label': 'Wellington, New Zealand', 'basis': 'page'}]}),
 dict(slug='Galapagos_Giant_Tortoises', title='Galápagos Giant Tortoise Rewilding', short='Galápagos tortoises', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='forests', label='Nonprofit solution · active',
  img=('Fernandina_Galapagos_ISS_2022.jpg', 1920, 1280, 'The cloud-wrapped peak of La Cumbre volcano on Fernandina Island in the Galápagos, seen from the International Space Station'),
  credit='NASA (iss068e025397, La Cumbre volcano, Fernandina Island, Galápagos, Nov. 28, 2022)',
  hook='Galápagos tortoises were nearly gone; a breeding programme has sent thousands home.',
  wow=('Over the last 60 years, more than 9,000 giant tortoises have been reared in captivity and released to the wild in the Galápagos (Galápagos Conservancy).', GAL),
  lead='Galápagos Conservancy and the Galápagos National Park Directorate rear giant tortoises in breeding centres and return them to their home islands (Galápagos Conservancy, nonprofit).',
  eli=['Giant tortoises once covered the Galápagos Islands, but people and animals they brought nearly wiped them out.',
       'Park rangers and scientists raise baby tortoises in safe centres until they are big enough to survive.',
       'Then they carry them back to the islands where they belong.'],
  ws=[('Who', 'Galápagos Conservancy, a nonprofit, with the Galápagos National Park Directorate.', GAL),
      ('What', 'Rearing endangered giant tortoises in breeding centres and releasing them on their home islands.', GAL),
      ('When', 'The programme launched in 1965 and has run for about 60 years.', GAL),
      ('Where', 'The Galápagos Islands, Ecuador.', GAL),
      ('Why', "Today's tortoise populations are only about 10% of their historical numbers and live in only 35% of their available habitat (Galápagos Conservancy).", GAL)],
  impact=('Española tortoises went from 15 survivors in the 1960s to more than 2,300 living and breeding on the island (Galápagos Conservancy).', GAL),
  fact=('The 15 Who Came Home', 'In June 2020 the 15 original Española adults were released back on their island, ending one of the most successful breeding programmes in the world (Galápagos Conservancy).', GALE),
  people=('As "ecosystem engineers," the tortoises have restorative effects on Galápagos land and biodiversity (Galápagos Conservancy).', GAL),
  nature=('Pinzón Island got tortoise hatchlings again after black rats were eradicated in 2012, for the first time in over 100 years (Galápagos Conservancy).', GAL),
  support_h='Support the Tortoises',
  btns=[('Donate to Galápagos Conservancy', GALDON), ('Learn About Tortoise Rewilding', GAL[0])],
  bottom=('Help rewild the Galápagos giant tortoises.', GALDON, 'Donate'),
  widget=None, see=[('Forest_Elephants.html', 'Forest Elephants, Carbon Gardeners', 'Elephants that help forests store more carbon.')],
  pin={'status': 'active', 'pins': [{'lat': -0.7, 'lng': -90.6, 'label': 'Galápagos Islands, Ecuador', 'basis': 'page'}]}),
 dict(slug='MAAP', title='MAAP, Amazon Deforestation Watch', short='MAAP', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='forests', label='Nonprofit solution · active',
  img=('Ucayali_River_ISS_2026.jpg', 1920, 1280, 'The winding Ucayali River through the lowland Amazon rainforest of central Peru, seen from the International Space Station'),
  credit='NASA/Jessica Meir (iss074e0492148, Ucayali River, Peru, April 15, 2026)',
  hook='Satellites spot new clearing in the Amazon, and MAAP reports explain what is behind it.',
  wow=('MAAP says it monitors deforestation and fires across 100% of the Amazon Basin (MAAP).', MAAPH),
  lead='MAAP, the Monitoring of the Andes Amazon Program, is an initiative of the nonprofit Amazon Conservation that uses satellite images to report on urgent deforestation and fires in the Amazon (MAAP).',
  eli=['The Amazon rainforest is huge, and it is hard to see where trees are being cut.',
       'Satellites take pictures from space, and MAAP experts compare them to find new clearings.',
       'Then they publish simple reports so governments and everyone else can act.'],
  ws=[('Who', 'Amazon Conservation, a Washington, D.C.-based nonprofit, with partners in Peru, Colombia and Ecuador.', MAAPA),
      ('What', 'Near-real-time monitoring that finds urgent deforestation, identifies its causes and publishes easy-to-read reports.', MAAPH),
      ('When', 'Launched in April 2015.', MAAPA),
      ('Where', 'It began in the Andean Amazon, with an initial emphasis on Peru, and now reports across the Amazon Basin.', MAAPA),
      ('Why', 'To give policymakers, law enforcement, researchers and the public the facts to help drive action against illegal deforestation (MAAP).', MAAPH)],
  impact=('MAAP combines satellite alerts built on Landsat, radar from Sentinel-1 and high-resolution imagery to verify forest loss and find its drivers (Amazon Conservation).', MAAPA),
  fact=('Drivers, Not Just Dots', 'MAAP has documented causes of deforestation including gold mining, oil palm, cacao, small-scale agriculture, logging roads and hydroelectric dams (Amazon Conservation).', MAAPA),
  people=('Its reports serve policymakers, law enforcement, civil society, researchers, the media and the general public (MAAP).', MAAPH),
  nature=('MAAP looks for deforestation inside protected areas and isolated indigenous communities, and in hotspots like the gold-mining zone of Madre de Dios (Amazon Conservation).', MAAPA),
  support_h='Support Amazon Conservation',
  btns=[('Donate to Amazon Conservation', ACDON), ('Read MAAP Reports', MAAPH[0])],
  bottom=('Support the team behind MAAP.', ACDON, 'Donate'),
  widget=None, see=[('Landsat_9.html', 'Landsat 9 (NASA/USGS)', 'Part of the Landsat record of Earth\'s land that began in 1972.')],
  pin={'status': 'active', 'pins': [{'lat': -10.5, 'lng': -73.5, 'label': 'Ucayali region, Peruvian Amazon', 'basis': 'page'}]}),
 dict(slug='Mesoamerican_Reef_Insurance', title='Mesoamerican Reef Insurance Programme (MAR Fund)', short='the MAR Insurance Programme', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='nonprofit', status='active', glass='ocean', label='Nonprofit solution · active',
  img=('Belize_Coast_ISS_2014.jpg', 1920, 1278, 'The Caribbean coast of Belize with its reef, cayes and turquoise shallows, seen from the International Space Station'),
  credit='NASA (ISS040-E-018752, Caribbean coast of Belize, June 24, 2014)',
  hook='A reef now has storm insurance that pays out fast, so crews can start repairs within days.',
  wow=('After Hurricane Lisa hit Belize\'s Turneffe Atoll in November 2022, the programme paid out US$175,000, and brigades stabilised nearly 200 coral fragments within 15 days (MAR Fund).', MARF),
  lead='The MAR Insurance Programme, run by the nonprofit MAR Fund, uses parametric insurance to pay for fast reef repair after hurricanes along the 1,000 km Mesoamerican Reef (MAR Fund).',
  eli=['Hurricanes can smash coral reefs, and repairs only work if they start quickly.',
       'This insurance pays out automatically when winds reach a set speed, with no long wait.',
       'Trained local teams then use the money to fix the reef.'],
  ws=[('Who', 'MAR Fund, a regional environmental fund, with insurance partners and local reef groups.', MARF),
      ('What', 'A parametric insurance programme that pays out when a hurricane\'s winds pass a trigger, funding reef response.', MARL),
      ('When', 'Launched in 2021, and entering its fifth year in 2025.', MARF),
      ('Where', '11 protected reef sites along the Mesoamerican Reef in Mexico, Belize, Guatemala and Honduras.', MARF),
      ('Why', 'Hurricanes are a leading driver of coral loss in the region, and reef response is hard to fund after extreme events (MAR Fund).', MARL)],
  impact=('The programme grew from 4 insured sites in 2021 to 11 reef sites (MAR Fund).', MARF),
  fact=('Paid Out in Two Weeks', 'The first payout was triggered on Nov. 2, 2022, when winds of 70 knots hit Turneffe Atoll, and MAR Fund received the money within two weeks (MAR Fund).', MARF),
  people=('The reef region provides over US$4.5 billion in environmental services each year and helps protect more than 5 million people living within 50 km of the coast (MAR Fund).', MARF),
  nature=('Local brigades assess and clean up reef damage, then repair it, following pre-agreed response plans (MAR Fund).', MARL),
  support_h='Support the Mesoamerican Reef',
  btns=[('Donate to MAR Fund', MARDON), ('Read About the Insurance Programme', MARF[0])],
  bottom=('Support reef rescue with MAR Fund.', MARDON, 'Donate'),
  widget=None, see=[('Coral_Reef_Watch.html', 'Coral Reef Watch (NOAA)', 'Satellites that warn when reefs are heating up.')],
  pin={'status': 'active', 'pins': [{'lat': 17.35, 'lng': -87.85, 'label': 'Turneffe Atoll, Belize', 'basis': 'page'}]}),
 dict(slug='Costa_Rica_Forest_Payments', title='Costa Rica Payments for Environmental Services (FONAFIFO)', short='Costa Rica\'s forest payments', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='government', status='active', glass='forests', label='Government solution · active',
  img=('Costa_Rica_ISS_2020.jpg', 1920, 1280, 'Central Costa Rica with the Gulf of Nicoya and green mountains, seen from the International Space Station'),
  credit='NASA (iss062e001866, Costa Rica, Feb. 8, 2020)',
  hook='Costa Rica pays people to keep their forests standing.',
  wow=("Costa Rica's programme changed 'subsidy' into 'economic recognition' for the services forests provide, including cutting emissions, protecting water and biodiversity (FONAFIFO).", FONA),
  lead="Costa Rica's FONAFIFO pays the owners of forests and forest plantations for the environmental services they provide, under Forestry Law 7575 (FONAFIFO).",
  eli=['Forests clean the air, keep water safe and give animals a home.',
       'In Costa Rica the government pays forest owners for those services.',
       'So keeping trees standing becomes worth it for the people who own the land.'],
  ws=[('Who', 'Costa Rica\'s national forestry financing fund, FONAFIFO, working with SINAC and others.', FONA),
      ('What', 'Payments to forest and plantation owners for four recognised services: reducing greenhouse gases, protecting biodiversity, protecting water and scenic beauty.', FONA),
      ('When', "The programme is set up under Forestry Law 7575, part of Costa Rica's environmental legislation of the 1990s.", FONA),
      ('Where', 'Costa Rica.', FONA),
      ('Why', 'To reduce deforestation, recover forest cover and support rural development, among other aims (FONAFIFO).', FONA)],
  impact=('FONAFIFO lists reduced deforestation, recovery of forest cover and degraded land, and rural development among the programme\'s effects (FONAFIFO).', FONA),
  fact=('Paid by the Pump', 'Funding first came from one third of the fuel consumption tax, and now 3.5% of the single fuel tax goes to the programme (FONAFIFO).', FONA),
  people=('The programme contributes to rural development and to national strategies to fight poverty (FONAFIFO).', FONA),
  nature=('It recognises forests for climate, biodiversity, water and scenic value (FONAFIFO).', FONA),
  support_h='Learn About the Programme',
  btns=[('FONAFIFO Payments for Environmental Services', FONA[0])],
  bottom=("Want to go deeper? FONAFIFO explains how Costa Rica's payments work.", FONA[0], 'For Further Information'),
  widget=None, see=[('Mangroves.html', 'Mangroves', 'Why coastal mangrove forests matter, and the teams restoring them.')],
  pin={'status': 'active', 'pins': [{'lat': 9.93, 'lng': -84.08, 'label': 'San José, Costa Rica', 'basis': 'page'}]}),
]

# Existing pages that link back (idempotent XLINK1019 block). Only entries whose new page is in SHIP are written.
XBACK = {
 'CryoSat.html': [('Thwaites_Glacier_Collaboration.html', 'International Thwaites Glacier Collaboration', 'About 100 scientists studying how fast Thwaites could raise sea levels.')],
 'Mangroves.html': [('Abu_Dhabi_Mangroves.html', 'Abu Dhabi Mangrove Restoration', 'Millions of mangroves planted along the Abu Dhabi coast, tracked by an observatory.')],
}

CSS = '''/* BLUF1019:START (generated by scripts/batch-1019-content.py) */
body.toc-sub .sol-bluf-box{margin:1rem auto .5rem;max-width:960px;padding:0 1rem}
body.toc-sub .sol-bluf-box .impact-box{max-width:880px;margin:0 auto;padding:1.1rem 1.4rem}
body.toc-sub .sol-bluf-box .impact-box p{margin:0 0 .55rem;line-height:1.5}
body.toc-sub .sol-bluf-box .bluf-hook{font-size:clamp(1.15rem,2vw,1.4rem);line-height:1.3}
body.toc-sub .sol-bluf-box .bluf-wow{font-size:1.05rem}
body.toc-sub .sol-bluf-box .impact-box p.fact-source{margin:0;font-size:.85rem}
@media (max-width:600px){body.toc-sub .sol-bluf-box .impact-box{padding:.9rem 1rem}}
/* BLUF1019:END */'''

def bluf(p):
    t, c = p['wow']
    return (f'<section class="impact sol-bluf-box" id="bluf" aria-label="The bottom line"><div class="impact-box">'
            f'<p class="bluf-hook"><strong>{E(p["hook"])}</strong></p><p class="bluf-wow">{E(t)}</p>{src(*c)}</div></section>')

def body(p):
    b, srcs = b18.body(p)
    b = b.replace('<!-- REVIEWED:START --><!-- REVIEWED:END -->', '<!-- REVIEWED:START --><!-- REVIEWED:END -->\n' + bluf(p), 1)
    return b, sorted(set(srcs) | {p['wow'][1][0]})

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
        out = re.sub(r'(sp:category" content=")[^"]*', lambda m: m.group(1) + p['cat'], out)
        out = re.sub(r'(sp:classification" content=")[^"]*', lambda m: m.group(1) + p['cls'], out)
        out = re.sub(r'(sp:status" content=")[^"]*', lambda m: m.group(1) + p['status'], out)
        out = re.sub(r'(sp:added" content=")[^"]*', lambda m: m.group(1) + ADDED, out)
        sl = s.lower().replace('_', '-')
        out = re.sub(r'<body[^>]*>', f'<body data-glass="{p["glass"]}" class="hp-{sl} toc-sub {sl}-page">', out, count=1)
        out = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', out, flags=re.S)
        out = re.sub(r'<!-- (TEACHER|CITE|SHARE):START -->.*?<!-- \1:END -->\n?', '', out, flags=re.S)
        out = out.replace('Surfrider Foundation', p['title']).replace('Surfrider', p['short'])
        open(os.path.join(ROOT, s + '.html'), 'w', encoding='utf8').write(out)
        eli[s + '.html'] = p['eli']
        pin = dict(p['pin'])
        if pin.get('strip') is None: pin.pop('strip', None)
        ml['solutions'][s + '.html'] = pin
    ICON = {'Polar.html': '🧊', 'Earth_Observation.html': '🌍', 'Oceans.html': '🌊', 'Deforestation.html': '🌳', 'Rivers.html': '💧', 'Space.html': '🛰️'}
    for p in pages:
        hf, hn = p['hub']; s = p['slug']; im, w, h, alt = p['img']
        fp = os.path.join(ROOT, hf); t = open(fp, encoding='utf8').read()
        if f'class="photo-link" href="{s}.html"' in t: continue
        card = (f'<article class="card"><div class="image-container"><a class="photo-link" href="{s}.html"><img src="assets/{im}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a></div>'
                f'<p class="sol-badges"><span class="status-badge status-active">Active</span><span class="hub-tag"><span aria-hidden="true">{ICON[hf]}</span> {hn}</span></p>'
                f'<h3><a href="{s}.html">{E(p["title"])}</a></h3><p class="card-blurb">{E(p["lead"])}</p></article>')
        i = t.find('id="missions"'); j = t.find('</div></section>', i)
        k = t.rfind('</article>', i, j) + len('</article>')
        t = t[:k] + card + t[k:]
        open(fp, 'w', encoding='utf8').write(t)
    for f, items in XBACK.items():
        items = [x for x in items if x[0][:-5] in SHIP]
        if not items: continue
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = '<!-- XLINK1019:START -->' + see_block(items, 'connected-1019') + '<!-- XLINK1019:END -->'
        if '<!-- XLINK1019:START -->' in t:
            t = re.sub(r'<!-- XLINK1019:START -->.*?<!-- XLINK1019:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    cp = os.path.join(ROOT, 'styles.css'); css = open(cp, encoding='utf8').read()
    css2 = re.sub(r'/\* BLUF1019:START.*?BLUF1019:END \*/', lambda m: CSS, css, flags=re.S) if 'BLUF1019:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
    if css2 != css: open(cp, 'w', encoding='utf8').write(css2)
    json.dump(eli, open(os.path.join(ROOT, 'assets/data/eli10.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump(ml, open(os.path.join(ROOT, 'assets/data/map-locations.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('wrote', len(pages), 'pages')

if __name__ == '__main__':
    main()
