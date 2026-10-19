#!/usr/bin/env python3
"""Oct 18 2026 batch: all 16 approved candidates A-P (owner, Oct 18): Voyager, FORUM, CIMR, CRISTAL, CHIME, GeoXO,
INSAT-3DS, Galileo, Ariel, Forest elephants, Yellowstone wolves, Coral Vita, Arbor Day Foundation, Namami Gange,
Clean Lakes Alliance, Sea Turtle Conservancy. Same writer as batch-1017-content.py (Surfrider_Foundation.html skeleton)
plus: mission-status widgets (site.js [data-mission]) where the batch marked Yes, a "Connected Solutions" list on the
new pages, and an idempotent XLINK1018 block on the existing pages they cross-link with (SARSAT, CryoSat, GOES-19,
the four coral pages). Every fact is from the cited page (fetched 2026-10-18). Org/company/government figures are
labeled as theirs. Re-runnable: overwrites only these 16 pages and the XLINK1018 blocks."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b17', os.path.join(ROOT, 'scripts/batch-1017-content.py'))
b17 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b17)
src = b17.src
ADDED = '2026-10-18'

NASA_VW = ('https://science.nasa.gov/mission/voyager/where-are-voyager-1-and-voyager-2-now/', 'NASA, Where are Voyager 1 and Voyager 2 now?')
NASA_VO = ('https://science.nasa.gov/mission/voyager/mission-overview/', 'NASA, Voyager mission overview')
ESA_FORUM = ('https://www.esa.int/Applications/Observing_the_Earth/FutureEO/FORUM', 'ESA, FORUM')
ESA_CIMR = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CIMR', 'ESA, CIMR')
ESA_CIMRF = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CIMR/CIMR_facts_and_figures', 'ESA, CIMR facts and figures')
ESA_CRS = ('https://sup.apex.esa.int/en/missions/cristal', 'ESA Sentinel Users Preparation, CRISTAL')
ESA_CRP = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CRISTAL_prepares_to_sparkle', 'ESA, CRISTAL prepares to sparkle')
ESA_CRC = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Plans_underway_for_new_polar_ice_and_snow_topography_mission', 'ESA, Plans underway for new polar ice and snow topography mission')
ESA_CHS = ('https://sup.apex.esa.int/en/missions/chime', 'ESA Sentinel Users Preparation, CHIME')
ESA_CHT = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CHIME_given_the_shakes', 'ESA, CHIME given the shakes')
NOAA_GX = ('https://www.nesdis.noaa.gov/our-satellites/future-programs/geostationary-extended-observations-geoxo', 'NOAA NESDIS, GeoXO')
NOAA_GXT = ('https://www.nesdis.noaa.gov/our-satellites/future-programs/geoxo/geoxo-timeline', 'NOAA NESDIS, GeoXO timeline')
OIG_GX = ('https://www.oversight.gov/reports/evaluation-noaas-progress-implementing-geoxo-satellite-program', "U.S. Department of Commerce OIG, Evaluation of NOAA's Progress Implementing the GeoXO Satellite Program (OIG-26-009-I)")
ISRO_3DS = ('https://www.isro.gov.in/GSLV-F14_INSAT-3DS_mission.html', 'ISRO, GSLV-F14/INSAT-3DS mission')
ISRO_3DSI = ('https://www.isro.gov.in/INSAT-3DS_imaging_Earth.html', 'ISRO, INSAT-3DS imaging Earth')
PIB_3DS = ('https://pib.gov.in/PressReleasePage.aspx?PRID=2006794', 'Press Information Bureau (Ministry of Earth Sciences), INSAT-3DS launch')
ESA_GAL = ('https://www.esa.int/Applications/Satellite_navigation/Two_new_Galileo_satellites_enter_service', 'ESA, Two new Galileo satellites enter service')
ESA_GALS = ('https://www.esa.int/Applications/Satellite_navigation/Galileo/Galileo_satellites', 'ESA, Galileo satellites')
ESA_ARIEL = ('https://www.esa.int/Science_Exploration/Space_Science/Ariel', 'ESA, Ariel')
NGEO = ('https://www.nature.com/articles/s41561-019-0395-6', 'Berzaghi et al., Nature Geoscience (2019)')
WCS_FE = ('https://congo.wcs.org/Wildlife/Forest-Elephant.aspx', 'WCS Congo, Forest Elephant')
NPS_W = ('https://www.nps.gov/yell/learn/management/wolf.htm', 'National Park Service, Wolf management in Yellowstone')
YF = ('https://www.yellowstone.org/projects/', 'Yellowstone Forever, Projects')
CV = ('https://www.coralvita.co/', 'Coral Vita')
CVA = ('https://coralvita.co/adopt-a-coral-program/', 'Coral Vita, Adopt a Coral')
ADF = ('https://www.arborday.org/our-impact', 'Arbor Day Foundation, Our impact')
PIB_NG = ('https://pib.gov.in/PressReleasePage.aspx?PRID=2280512', 'Press Information Bureau (Ministry of Jal Shakti), 19th Empowered Task Force on River Ganga, 2 July 2026')
NMCG = ('https://nmcg.nic.in/', 'National Mission for Clean Ganga')
CLA = ('https://www.cleanlakesalliance.org/about/', 'Clean Lakes Alliance, About')
CLAR = ('https://www.cleanlakesalliance.org/wp-content/uploads/2020/05/2024-Impact-Report-compressed.pdf', 'Clean Lakes Alliance, 2024 Impact Report')
STC = ('https://conserveturtles.org/', 'Sea Turtle Conservancy')
CITSCI = 'https://science.nasa.gov/citizen-science/'

def W(mission, status, source, agency, launch=None, arrival=None, arrival_label=None, milestones=None, news=None):
    a = [f'data-mission="{E(mission)}"', f'data-agency="{E(agency)}"']
    if launch: a.append(f'data-launch="{launch}"')
    if arrival: a.append(f'data-arrival="{arrival}"')
    if arrival_label: a.append(f'data-arrival-label="{E(arrival_label)}"')
    a.append(f'data-status="{E(status)}"')
    if milestones: a.append('data-milestones="' + E(';'.join(f'{d}|{l}' for d, l in milestones)) + '"')
    if news: a.append(f'data-news="{E(news)}"')
    a += [f'data-source="{source[0]}"', f'data-source-label="{E(source[1])}"']
    return f'<section class="mission-widget" aria-live="polite" {" ".join(a)}></section>'

PAGES = [
 dict(slug='Voyager', title='Voyager 1 and 2 (NASA)', short='Voyager', cat='project-r',
  hub=('Project-Rawane.html', 'Project Rawane'), cls='agency', status='active', glass='space', label='Agency solution · active',
  img=('Voyager_Heliosphere_PIA22835.jpg', 1920, 1080, "Illustration of NASA's Voyager 1 and Voyager 2 outside the heliosphere, the Sun's protective bubble"), credit='NASA/JPL-Caltech (PIA22835)',
  lead='Launched in 1977, the twin Voyagers are in interstellar space, and on Nov. 18, 2026, Voyager 1 will be one light-day from Earth (NASA).',
  eli=['Voyager 1 and Voyager 2 are two spacecraft that left Earth in 1977.',
       'They flew past the giant planets and are now outside the bubble the Sun makes around itself.',
       'On Nov. 18, 2026, Voyager 1 will be so far away that its radio signal takes a whole day to reach us.'],
  ws=[('Who', 'NASA. Five science investigation teams use the spacecraft, which still have four operating instruments between them.', NASA_VO),
      ('What', 'Twin robotic spacecraft. Their main mission explored Jupiter and Saturn; Voyager 2 then went on to Uranus and Neptune.', NASA_VO),
      ('When', 'Voyager 2 launched on Aug. 20, 1977, and Voyager 1 on Sept. 5, 1977, both from Cape Canaveral, Florida.', NASA_VO),
      ('Where', 'In interstellar space, the region between stars. Voyager 1 crossed into it in August 2012 and Voyager 2 on Nov. 5, 2018.', NASA_VO),
      ('Why', 'The Voyager Interstellar Mission extends exploration to the outer limits of the Sun\'s sphere of influence, and possibly beyond.', NASA_VO)],
  impact=('On Nov. 18, 2026, at 2:16:07 a.m. PST, Voyager 1 will be 16.094 billion miles (25.902 billion km) from Earth, the distance light travels in 24 hours (NASA).', NASA_VW),
  fact=('Saving Power, One Instrument at a Time', 'To stretch their power, engineers have switched off instruments one by one; Voyager 1\'s cameras have been off since 1990 (NASA).', NASA_VW),
  people=('Voyager\'s discoveries, from active volcanoes on Jupiter\'s moon Io to details of Saturn\'s rings, are shared knowledge for everyone (NASA).', NASA_VO),
  nature=('Voyager studies the heliosphere, the bubble the Sun blows around our solar system, which surrounds Earth and all life on it (NASA).', NASA_VO),
  support_h='Get Involved With Voyager',
  btns=[('Where Are the Voyagers Now?', NASA_VW[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? NASA has the full Voyager story.', NASA_VO[0], 'For Further Information'),
  widget=W('Voyager 1', 'Both Voyagers are in interstellar space. Voyager 1 reaches one light-day from Earth on Nov. 18, 2026, at 2:16:07 a.m. PST.', NASA_VW, 'NASA',
           arrival='2026-11-18T10:16:07Z', arrival_label='one light-day from Earth, Nov. 18, 2026',
           milestones=[('1977-08-20', 'Voyager 2 launches'), ('1977-09-05', 'Voyager 1 launches'), ('2018-11-05', 'Voyager 2 enters interstellar space'), ('2026-11-18', 'Voyager 1 is one light-day from Earth')], news='Voyager'),
  see=[], pin={'status': 'active', 'pins': [{'lat': 28.392, 'lng': -80.605, 'label': 'Cape Canaveral, Florida, where both Voyagers launched in 1977', 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='FORUM', title='FORUM Far-Infrared Mission (ESA)', short='FORUM', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Agency solution · in development',
  img=('Clouds_Limb_ISS.jpg', 1200, 819, "Clouds and the thin blue layer of Earth's atmosphere seen from orbit"), credit='NASA',
  lead="ESA's FORUM will measure Earth's outgoing far-infrared radiation, never measured from space before, filling a missing piece of the climate jigsaw (ESA).",
  eli=['Earth gives off heat into space as invisible infrared light.',
       'Part of that light, called far-infrared, has never been measured from space.',
       'FORUM will measure it, helping scientists understand how Earth keeps its heat balance.'],
  ws=[('Who', 'The European Space Agency (ESA). FORUM is an Earth Explorer mission.', ESA_FORUM),
      ('What', 'A satellite carrying a Fourier transform spectrometer to measure Earth\'s outgoing radiation in the far-infrared.', ESA_FORUM),
      ('When', 'Launch is planned for 2028 on a Vega-C rocket.', ESA_FORUM),
      ('Where', 'In orbit around Earth, launching from Europe\'s Spaceport in Kourou, French Guiana.', ESA_FORUM),
      ('Why', 'FORUM data will give unique insight into Earth\'s radiation budget and how it is controlled.', ESA_FORUM)],
  impact=('FORUM will measure a part of Earth\'s outgoing radiation that has never been measured from space before (ESA).', ESA_FORUM),
  fact=('A Missing Piece', 'ESA calls the far-infrared a missing piece of the climate jigsaw that FORUM will fill in (ESA).', ESA_FORUM),
  people=('Better knowledge of Earth\'s radiation budget helps improve the climate understanding people rely on to plan ahead (ESA).', ESA_FORUM),
  nature=('FORUM looks at how Earth sheds heat to space, a basic control on the climate all ecosystems live in (ESA).', ESA_FORUM),
  support_h='Learn More About FORUM',
  btns=[('Learn About FORUM', ESA_FORUM[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has the full FORUM story.', ESA_FORUM[0], 'For Further Information'),
  widget=W('FORUM', 'In development. Launch planned for 2028 on Vega-C from Kourou, French Guiana.', ESA_FORUM, 'ESA'),
  see=[], pin={'status': 'active', 'pins': [{'lat': 5.236, 'lng': -52.769, 'label': "Europe's Spaceport, Kourou, French Guiana (planned launch site)", 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='CIMR', title='CIMR Copernicus Imaging Microwave Radiometer (ESA)', short='CIMR', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · in development',
  img=('North_Atlantic_Bloom_MODIS.jpg', 1536, 1920, 'Swirls of a phytoplankton bloom in the deep blue central North Atlantic Ocean, seen by satellite'), credit='NASA/GSFC/Jeff Schmaltz/MODIS Land Rapid Response Team',
  lead='Two Copernicus satellites will measure sea ice, sea-surface temperature and salinity over 95% of the globe every day, with sub-daily polar views (ESA).',
  eli=['CIMR will be two satellites that measure the ocean and polar sea ice.',
       'They use a huge round antenna to sense tiny amounts of natural microwave energy.',
       'They will cover almost the whole Earth every day, even through clouds.'],
  ws=[('Who', 'The European Space Agency (ESA), for Europe\'s Copernicus programme. Thales Alenia Space Italy is prime contractor for the satellite.', ESA_CIMRF),
      ('What', 'Two satellites, each with a wide-swath, conically scanning microwave radiometer and an 8.5 m reflector.', ESA_CIMRF),
      ('When', 'CIMR-A is planned to launch in 2029 and CIMR-B in 2035, giving at least 15 years of continuous measurements.', ESA_CIMRF),
      ('Where', 'A dawn-dusk sun-synchronous orbit at 817 km. Science data are downlinked to Svalbard, Norway.', ESA_CIMRF),
      ('Why', 'CIMR places the Arctic in a global context, to support solutions for this fragile region and combat climate change worldwide.', ESA_CIMR)],
  impact=('CIMR will measure 95% of the globe every day, with sub-daily coverage of the polar regions (ESA).', ESA_CIMRF),
  fact=('An 8.5-Metre Dish', 'CIMR\'s 8.5 m reflector sits on an 8 m boom that spins at 7.8 turns per minute (ESA).', ESA_CIMRF),
  people=('Daily sea-ice and ocean data support safer work and travel in polar seas and better climate information for everyone (ESA).', ESA_CIMR),
  nature=('CIMR will track sea ice, sea-surface temperature and salinity in the fragile Arctic, a region hit hard by climate change (ESA).', ESA_CIMR),
  support_h='Learn More About CIMR',
  btns=[('Learn About CIMR', ESA_CIMR[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has the full CIMR story.', ESA_CIMR[0], 'For Further Information'),
  widget=W('CIMR', 'In development. CIMR-A is planned for 2029 and CIMR-B for 2035, both from Kourou, French Guiana.', ESA_CIMRF, 'ESA'),
  see=[('CryoSat.html', 'CryoSat Ice Mission (ESA)', 'Measures the thickness of polar sea ice with radar.'),
       ('CRISTAL.html', 'CRISTAL Polar Ice and Snow Altimeter (ESA)', 'Will measure sea-ice thickness and the snow on top.')],
  pin={'status': 'active', 'pins': [{'lat': 52.218, 'lng': 4.42, 'label': 'ESA ESTEC, Noordwijk, Netherlands (project management)', 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='CRISTAL', title='CRISTAL Polar Ice and Snow Altimeter (ESA)', short='CRISTAL', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · in development',
  img=('Labrador_Sea_Ice_ISS.jpg', 1920, 1280, 'Sea ice in the Labrador Sea seen from the International Space Station'), credit='NASA (ISS070-E-086805, Feb. 3, 2024)',
  lead="CRISTAL will carry the first dual-frequency radar altimeter to measure polar sea-ice thickness and the snow on top, following ESA's CryoSat (ESA).",
  eli=['CRISTAL is a satellite that will measure how thick the polar sea ice is.',
       'It will also measure how deep the snow is on top of the ice.',
       'It carries on the work of the CryoSat satellite.'],
  ws=[('Who', 'The European Space Agency (ESA), for Copernicus. Airbus builds the satellite; Thales Alenia Space builds the IRIS altimeter; NASA JPL provides the radiometer.', ESA_CRP),
      ('What', 'Two identical satellites with a Ku- and Ka-band radar altimeter and a microwave radiometer. CRISTAL-B will replace CRISTAL-A.', ESA_CRP),
      ('When', "ESA's Sentinel Users Preparation site says launch is scheduled for 2028. An earlier ESA update said CRISTAL-A would be ready to launch in the second half of 2027.", ESA_CRS),
      ('Where', 'Over the polar regions, also measuring ice sheets, glaciers, oceans, rivers and lakes worldwide.', ESA_CRS),
      ('Why', 'It continues the radar record of ice height after CryoSat and fills observation gaps in the polar regions.', ESA_CRS)],
  impact=('CRISTAL will monitor sea-ice thickness and overlying snow depth, and changes in the height of ice sheets and glaciers worldwide (ESA).', ESA_CRS),
  fact=('A Double Radar', 'CRISTAL will be the first polar mission to carry a dual-frequency radar altimeter (ESA).', ESA_CRC),
  people=('CRISTAL supports maritime operations and safety in the rapidly changing polar seas (ESA).', ESA_CRS),
  nature=('Its data help quantify how ice responds to climate change, where effects are most pronounced (ESA).', ESA_CRS),
  support_h='Learn More About CRISTAL',
  btns=[('Learn About CRISTAL', ESA_CRS[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has the full CRISTAL story.', ESA_CRP[0], 'For Further Information'),
  widget=W('CRISTAL', 'In development. Launch scheduled for 2028 (ESA Sentinel Users Preparation); an earlier ESA update said the second half of 2027.', ESA_CRS, 'ESA'),
  see=[('CryoSat.html', 'CryoSat Ice Mission (ESA)', "CRISTAL's predecessor, in orbit since 2010."),
       ('CIMR.html', 'CIMR Copernicus Imaging Microwave Radiometer (ESA)', 'Will map sea ice and ocean temperature every day.')],
  pin={'status': 'active', 'pins': [{'lat': 47.661, 'lng': 9.48, 'label': 'Airbus, Friedrichshafen, Germany, where CRISTAL-A is being assembled', 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='CHIME', title='CHIME Hyperspectral Imaging Mission (ESA)', short='CHIME', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Agency solution · in development',
  img=('Garden_City_Kansas_Landsat.jpg', 1600, 1600, 'Circular crop fields around Garden City, Kansas, seen by Landsat'), credit='NASA/GSFC/Landsat (Sept. 25, 2000)',
  lead='CHIME will image Earth in more than 200 colours of light to support sustainable farming, food security and biodiversity (ESA).',
  eli=['CHIME will be two satellites that see far more colours than our eyes can.',
       'Those colours show how healthy crops and soils are.',
       'Farmers and scientists can use this to grow food and protect nature.'],
  ws=[('Who', 'The European Space Agency (ESA), for Europe\'s Copernicus programme.', ESA_CHS),
      ('What', 'Two identical satellites, CHIME-A and CHIME-B, each carrying a hyperspectral imager with more than 200 spectral bands.', ESA_CHS),
      ('When', 'In development: an instrument model passed launch-stress tests. ESA has not published a launch date on the pages we read.', ESA_CHT),
      ('Where', 'In a sun-synchronous orbit about 600 km up, with a 128 km swath that complements Sentinel-2.', ESA_CHS),
      ('Why', 'A rising population and climate change are intensifying threats to food security (ESA).', ESA_CHT)],
  impact=('CHIME will acquire hyperspectral imagery in more than 200 bands from 400 to 2500 nm, describing vegetation, soils and surface materials (ESA).', ESA_CHS),
  fact=('Shaken, Not Stirred', 'A model of the CHIME instrument was put in a vacuum chamber and on a shaker to prove it can survive launch (ESA).', ESA_CHT),
  people=('CHIME will provide key information on crops and soils to support agriculture and food security (ESA).', ESA_CHS),
  nature=('CHIME will support biodiversity and ecosystem monitoring and inland and coastal water quality (ESA).', ESA_CHS),
  support_h='Learn More About CHIME',
  btns=[('Learn About CHIME', ESA_CHS[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has more about CHIME.', ESA_CHT[0], 'For Further Information'),
  widget=W('CHIME', 'In development. Launch date TBA: no launch date is given on the ESA pages we read.', ESA_CHS, 'ESA'),
  see=[], pin={'status': 'active', 'pins': [{'lat': 48.849, 'lng': 2.303, 'label': 'ESA headquarters, Paris, France', 'basis': 'hq'}], 'strip': 'orbit'}),
 dict(slug='GeoXO', title='GeoXO Geostationary Extended Observations (NOAA / NASA)', short='GeoXO', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Agency solution · in development',
  img=('Lightning_Storm_ISS.jpg', 1600, 1067, 'Lightning lights up storm clouds off North Carolina, seen from the International Space Station'), credit='NASA (iss073e0080625, May 15, 2025)',
  lead="NOAA's next generation of geostationary weather satellites, planned from 2032, will improve warnings of severe weather and hazards (NOAA).",
  eli=['GeoXO will be new weather satellites that stay over the same spot above Earth.',
       'They will watch storms, wildfires, smoke and floods as they happen.',
       'This helps forecasters warn people sooner.'],
  ws=[('Who', 'NOAA and NASA. NASA manages development and launches the satellites; NOAA operates them and delivers the data.', NOAA_GX),
      ('What', 'Satellites carrying visible and infrared imagers and a new hyperspectral infrared sounder for better forecasts.', NOAA_GX),
      ('When', 'The first launch is planned for 2032; further launches are planned for 2034, 2039 and 2043.', NOAA_GXT),
      ('Where', 'In geostationary orbit, watching over the Western Hemisphere. It will replace the current GOES-R Series.', NOAA_GX),
      ('Why', "In March 2026 the Commerce Department's Inspector General found GeoXO had made adequate progress, and noted a possible gap in data if older GOES satellites end before GeoXO is operating.", OIG_GX)],
  impact=('GeoXO will detect and monitor wildfires, smoke, dust, volcanic ash, drought and flooding, improving lead times for public alerts (NOAA).', NOAA_GX),
  fact=('Six Recommendations', "The Inspector General made six recommendations to reduce the risk of a gap in geostationary weather data and improve risk management (OIG).", OIG_GX),
  people=('Better short-term forecasts and severe storm warnings protect people across the Western Hemisphere (NOAA).', NOAA_GX),
  nature=('GeoXO will watch the weather, oceans and environment, including wildfires and drought (NOAA).', NOAA_GX),
  support_h='Learn More About GeoXO',
  btns=[('Learn About GeoXO', NOAA_GX[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? NOAA has the full GeoXO story.', NOAA_GX[0], 'For Further Information'),
  widget=W('GeoXO', 'In development. First launch planned for 2032; further launches planned for 2034, 2039 and 2043.', NOAA_GXT, 'NOAA'),
  see=[('GOES-19.html', 'GOES-19', 'Today\'s GOES-R Series satellite that GeoXO will follow.')],
  pin={'status': 'active', 'pins': [{'lat': 38.992, 'lng': -77.031, 'label': 'NOAA NESDIS, Silver Spring, Maryland', 'basis': 'hq'}], 'strip': 'orbit'}),
 dict(slug='INSAT-3DS', title='INSAT-3DS Weather Satellite (ISRO)', short='INSAT-3DS', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('ISS_Over_Ganges_STS102.jpg', 1920, 1267, 'The International Space Station above the Ganges River in India, photographed from the Space Shuttle'), credit='NASA (STS102-357-031, March 18, 2001)',
  lead="India's INSAT-3DS watches weather, land and oceans from geostationary orbit and carries a search-and-rescue transponder (ISRO).",
  eli=['INSAT-3DS is an Indian weather satellite that stays over the same place above Earth.',
       'It takes pictures of clouds, rain, fog and fires.',
       'It also passes on distress calls so rescuers can find people in trouble.'],
  ws=[('Who', 'ISRO built and launched it; India\'s Ministry of Earth Sciences fully funded it. IMD and other institutes use the data.', ISRO_3DS),
      ('What', 'A weather satellite with a 6-channel Imager and a 19-channel Sounder, plus data relay and satellite-aided search and rescue.', ISRO_3DSI),
      ('When', 'Launched on Feb. 17, 2024, on GSLV-F14 from Sriharikota. Its first images came on March 7, 2024.', ISRO_3DSI),
      ('Where', 'In geostationary orbit, alongside India\'s INSAT-3D and INSAT-3DR satellites.', PIB_3DS),
      ('Why', 'It is designed for weather forecasting and disaster warning by monitoring land and ocean surfaces.', ISRO_3DS)],
  impact=('INSAT-3DS payloads generate more than 40 geophysical data products, including rainfall, sea-surface temperature, fog, fire and smoke (ISRO).', ISRO_3DSI),
  fact=('2,275 Kilograms', 'INSAT-3DS had a lift-off mass of 2,275 kg and is built on ISRO\'s I-2k bus (Ministry of Earth Sciences).', PIB_3DS),
  people=('INSAT-3DS supports weather forecasts, disaster warnings and satellite-aided search and rescue (ISRO).', ISRO_3DS),
  nature=('Its data track ocean temperature, rainfall, vegetation health, fires and smoke (ISRO).', ISRO_3DSI),
  support_h='Learn More About INSAT-3DS',
  btns=[('Learn About INSAT-3DS', ISRO_3DS[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ISRO has the full INSAT-3DS story.', ISRO_3DS[0], 'For Further Information'),
  widget=W('INSAT-3DS', 'Operational in geostationary orbit since 2024.', ISRO_3DSI, 'ISRO',
           milestones=[('2024-02-17', 'Launch on GSLV-F14 from Sriharikota'), ('2024-02-28', 'Reaches its geostationary slot for in-orbit testing'), ('2024-03-07', 'First images from the Imager and Sounder')]),
  see=[('SARSAT.html', 'SARSAT', 'How satellites relay distress-beacon alerts to rescuers.')],
  pin={'status': 'active', 'pins': [{'lat': 13.72, 'lng': 80.23, 'label': 'Satish Dhawan Space Centre, Sriharikota, India (launch site)', 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='Galileo', title='Galileo Satellite Navigation (EU / ESA)', short='Galileo', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('Romania_City_Lights_ISS.jpg', 1200, 800, 'City lights at night seen from the International Space Station'), credit='NASA (iss074e0149572, city lights trace river valleys in Romania)',
  lead="Europe's Galileo is the world's most precise satellite navigation system, serving over five billion smartphone users and helping rescues (ESA).",
  eli=['Galileo is a group of satellites that tells your phone exactly where it is.',
       'Each satellite has very accurate atomic clocks.',
       'Galileo satellites can also hear emergency beacons and pass the alert to rescuers.'],
  ws=[('Who', 'The European Union owns and funds Galileo through the European Commission. ESA designs and builds it, and EUSPA runs the service.', ESA_GAL),
      ('What', 'A constellation designed for 30 satellites, 3 of them spares. Each carries atomic clocks and a search-and-rescue antenna.', ESA_GALS),
      ('When', 'Open Service began in 2016. Satellites SAT 33 and SAT 34 entered service in 2026, and four first-generation satellites remain to launch.', ESA_GAL),
      ('Where', 'In medium Earth orbit, at 23,222 km.', ESA_GAL),
      ('Why', "Precise positioning and timing matter for rail, shipping, farming, finance and rescue operations (ESA).", ESA_GAL)],
  impact=('Galileo serves over five billion smartphone users around the globe, and all smartphones sold in the EU single market are guaranteed Galileo-enabled (ESA).', ESA_GAL),
  fact=('0.45 Nanoseconds', "Each Galileo satellite's hydrogen maser clock keeps time to within 0.45 billionths of a second over 12 hours (ESA).", ESA_GALS),
  people=("Galileo's search-and-rescue antenna picks up distress signals from beacons and sends them on to local rescue services (ESA).", ESA_GALS),
  nature=('Precise positioning supports farming, one of the fields where ESA says Galileo is making a difference (ESA).', ESA_GAL),
  support_h='Learn More About Galileo',
  btns=[('Learn About Galileo', ESA_GAL[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has the full Galileo story.', ESA_GALS[0], 'For Further Information'),
  widget=W('Galileo', 'In service. SAT 33 and SAT 34 joined in 2026; four first-generation satellites remain, with the next pair planned for the end of the year.', ESA_GAL, 'ESA',
           milestones=[('2026-07-23', 'SAT 34 enters service, completing the L14 pair')]),
  see=[('SARSAT.html', 'SARSAT', 'The international distress-beacon system that Galileo\'s rescue antennas feed into.')],
  pin={'status': 'active', 'pins': [{'lat': 48.083, 'lng': 11.281, 'label': 'Galileo Control Centre, Oberpfaffenhofen, Germany', 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='Ariel', title='Ariel Exoplanet Mission (ESA)', short='Ariel', cat='project-r',
  hub=('Project-Rawane.html', 'Project Rawane'), cls='agency', status='active', glass='space', label='Agency solution · in development',
  img=('Webb_Infrared.jpg', 1600, 895, 'Infrared space telescopes shown over a colorful nebula'), credit='NASA/Sydney Rohde',
  lead="ESA's Ariel will study the atmospheres of a thousand planets orbiting other stars, revealing what they are made of (ESA).",
  eli=['Ariel is a space telescope that will look at planets around other stars.',
       'When a planet passes in front of its star, starlight shines through its air.',
       'Ariel reads that light to find out what the planet\'s air is made of.'],
  ws=[('Who', 'The European Space Agency (ESA).', ESA_ARIEL),
      ('What', 'Ariel, the Atmospheric Remote-sensing Infrared Exoplanet Large-survey, a telescope that will inspect exoplanet atmospheres.', ESA_ARIEL),
      ('When', 'Launch is planned for 2031 on an Ariane 6 rocket.', ESA_ARIEL),
      ('Where', 'In a halo orbit around the Sun-Earth Lagrange point L2, launching from Europe\'s Spaceport in French Guiana.', ESA_ARIEL),
      ('Why', 'Ariel will reveal the ingredients of exoplanet atmospheres and the presence of clouds.', ESA_ARIEL)],
  impact=('Ariel will inspect the atmospheres of a thousand planets in our galaxy orbiting stars other than the Sun (ESA).', ESA_ARIEL),
  fact=('1,400 Kilograms', 'Ariel will weigh about 1,400 kg at launch (ESA).', ESA_ARIEL),
  people=('Learning how other planets\' atmospheres work helps everyone understand what makes a world like Earth special (ESA).', ESA_ARIEL),
  nature=('Comparing a thousand alien atmospheres puts Earth\'s own life-supporting air in context (ESA).', ESA_ARIEL),
  support_h='Learn More About Ariel',
  btns=[('Learn About Ariel', ESA_ARIEL[0]), ('Join NASA Citizen Science', CITSCI)],
  bottom=('Want to go deeper? ESA has the full Ariel story.', ESA_ARIEL[0], 'For Further Information'),
  widget=W('Ariel', 'In development. Launch planned for 2031 on Ariane 6 from French Guiana.', ESA_ARIEL, 'ESA'),
  see=[('Plato.html', 'Plato', 'ESA\'s planet-hunting telescope, which looks for Earth-like worlds.')],
  pin={'status': 'active', 'pins': [{'lat': 5.236, 'lng': -52.769, 'label': "Europe's Spaceport, Kourou, French Guiana (planned launch site)", 'basis': 'page'}], 'strip': 'orbit'}),
 dict(slug='Forest_Elephants', title='Forest Elephants, Carbon Gardeners', short='Forest Elephants', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='natural', status='active', glass='forests', label='Natural solution · active',
  img=('Congo_River_ISS.jpg', 1920, 1271, 'The Congo River between Brazzaville and Kinshasa seen from the International Space Station'), credit='NASA (ISS007-E-06305, June 6, 2003)',
  lead="By thinning small trees, forest elephants help central Africa's rainforests store more carbon: 26 to 60 more tonnes of biomass per hectare (Nature Geoscience).",
  eli=['Forest elephants live in the rainforests of central and West Africa.',
       'As they walk and eat, they push over and munch small trees.',
       'That leaves room for big, heavy trees that store more carbon.'],
  ws=[('Who', 'The African forest elephant (Loxodonta cyclotis), classified as Critically Endangered since 2021 (WCS).', WCS_FE),
      ('What', 'By reducing the number of stems, elephants favour fewer, larger trees with denser wood (Nature Geoscience).', NGEO),
      ('When', 'A 2019 study modelled the effect and confirmed it with forest inventory data.', NGEO),
      ('Where', 'Tropical rainforests of West Africa and the Congo Basin (WCS).', WCS_FE),
      ('Why', 'The main threat to elephants is poaching for ivory: some 100,000 elephants were poached across Africa between 2007 and 2016 (WCS).', WCS_FE)],
  impact=('At 0.5 to 1 elephant per square km, elephant disturbance raises aboveground biomass by 26 to 60 tonnes per hectare (Nature Geoscience, 2019).', NGEO),
  fact=('Losing Elephants Means Losing Carbon', 'The extinction of forest elephants would cut aboveground biomass in central African rainforests by 7% (Nature Geoscience).', NGEO),
  people=('Forests that store more carbon help slow climate change for everyone (Nature Geoscience).', NGEO),
  nature=('Elephants are engineers of the forest: they create trails, spread seeds of high carbon-density trees and dig for minerals other species need (WCS).', WCS_FE),
  support_h='Learn More About Forest Elephants',
  btns=[('WCS Congo: Forest Elephant Program', WCS_FE[0]), ('Read the Study', NGEO[0])],
  bottom=('Want to go deeper? WCS Congo explains its forest elephant work.', WCS_FE[0], 'For Further Information'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': -4.27, 'lng': 15.28, 'label': 'Brazzaville, Republic of Congo (WCS Congo, forest elephant program)', 'basis': 'page'}]}),
 dict(slug='Yellowstone_Wolves', title='Yellowstone Wolves', short='Yellowstone Wolves', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='natural', status='active', glass='forests', label='Natural solution · active',
  img=('Yellowstone_ISS.jpg', 1920, 1251, 'Snow-covered Yellowstone National Park, Wyoming, seen from the International Space Station'), credit='NASA (ISS023-E-007925, March 21, 2010)',
  lead='Gray wolves returned to Yellowstone in 1995 after nearly 70 years; in January 2026 at least 84 lived in the park, in eight packs (NPS).',
  eli=['Wolves disappeared from Yellowstone National Park for almost 70 years.',
       'In 1995, people brought wolves back.',
       'Scientists now study how wolves, elk and other animals live together again.'],
  ws=[('Who', 'The National Park Service (NPS) manages and studies the park\'s wolves.', NPS_W),
      ('What', 'Bringing back a top predator. Researchers track wolves with radio collars, cameras, howl recorders and DNA.', NPS_W),
      ('When', 'Wolves were reintroduced in 1995, and the Winter Study has run every year since then.', NPS_W),
      ('Where', 'Yellowstone National Park, at the core of a wolf population connected across the Greater Yellowstone Ecosystem.', NPS_W),
      ('Why', 'Monitoring shows how wolves affect other wildlife, prey and the wider food web.', NPS_W)],
  impact=('As of January 2026, at least 84 wolves in eight packs lived in Yellowstone National Park (NPS).', NPS_W),
  fact=('Listening for Howls', 'Recorders placed around the park capture wolf howls, helping estimate wolf numbers in remote areas (NPS).', NPS_W),
  people=('Yellowstone is one of the best places in the world to see wild wolves, and rangers teach visitors to watch them safely (NPS).', NPS_W),
  nature=('Wolves are apex predators, and NPS research looks at their effects on prey and the food web (NPS).', NPS_W),
  support_h='Support Yellowstone',
  btns=[('Donate to Yellowstone Forever', 'https://www.yellowstone.org/ways-to-give/'), ('Learn About the Wolves', NPS_W[0])],
  bottom=('Yellowstone Forever is the park\'s official nonprofit partner.', 'https://www.yellowstone.org/ways-to-give/', 'Donate'), donate_alt='Donate to Yellowstone Forever',
  widget=None, see=[('Beavers_River_Engineers.html', 'Beavers, River Engineers', 'Another animal that reshapes its home landscape.')],
  pin={'status': 'active', 'pins': [{'lat': 44.6, 'lng': -110.5, 'label': 'Yellowstone National Park, Wyoming', 'basis': 'page'}]}),
 dict(slug='Coral_Vita', title='Coral Vita Land-Based Coral Farms', short='Coral Vita', cat='ocean',
  hub=('Oceans.html', 'Oceans'), cls='corporate', status='active', glass='ocean', label='Company solution · active',
  img=('Bahama_Bank_PIA11019.jpg', 1920, 1277, 'Shallow Bahama Bank waters meeting the deep Tongue of the Ocean, seen from space'), credit='NASA (PIA11019)',
  lead='Coral Vita grows reef-building corals on land up to 50 times faster than in nature, and says it has grown over 100,000 corals (company figures).',
  eli=['Coral reefs are dying in many places around the world.',
       'Coral Vita grows baby corals in tanks on land, where they grow very fast.',
       'Then divers plant them back on damaged reefs.'],
  ws=[('Who', 'Coral Vita, a company that runs land-based coral farms.', CV),
      ('What', 'Growing corals in tanks on land using microfragmentation, then planting them onto damaged reefs.', CVA),
      ('When', 'Coral Vita says it has grown over 100,000 corals so far (company figure).', CV),
      ('Where', 'Grand Bahama, where it grows nearly 20 native species; it has also worked in Dubai and Saudi Arabia (company).', CVA),
      ('Why', 'Coral reefs support 25% of all marine species while covering less than 1% of the ocean floor (Coral Vita).', CVA)],
  impact=('Coral Vita says it has grown over 100,000 corals across 52 species, with doubled fish populations at restoration sites (company figures).', CV),
  fact=('Coral Cookies', 'Coral Vita fuses seven tiny coral fragments on a "coral cookie", so they grow together into one colony (company).', CVA),
  people=('Reefs protect coastlines and support tourism that many island communities depend on (Coral Vita).', CVA),
  nature=('Restored reefs give fish and other marine creatures habitat to return to (Coral Vita).', CVA),
  support_h='Support Coral Vita',
  btns=[('Adopt a Coral', CVA[0]), ('Learn About Coral Vita', CV[0])],
  bottom=('Support reef restoration by adopting a coral.', CVA[0], 'Donate'), donate_alt='Adopt a Coral',
  widget=None,
  see=[('Coral_Gardeners.html', 'Coral Gardeners', 'Reef restoration in French Polynesia.'),
       ('Coral_Restoration_Foundation.html', 'Coral Restoration Foundation', 'Coral nurseries in the Florida Keys.'),
       ('Coral_IVF.html', 'Coral IVF', 'Helping corals reproduce.'),
       ('Coral_Reef_Watch.html', 'Coral Reef Watch', 'Satellite warnings of coral bleaching.')],
  pin={'status': 'active', 'pins': [{'lat': 26.53, 'lng': -78.7, 'label': 'Grand Bahama, The Bahamas (Coral Vita coral farm)', 'basis': 'page'}]}),
 dict(slug='Arbor_Day_Foundation', title='Arbor Day Foundation', short='the Arbor Day Foundation', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='forests', label='Nonprofit solution · active',
  img=('Amazon_Clouds_ISS.jpg', 1600, 1067, 'Clouds rising over the Amazon rainforest seen from the International Space Station'), credit='NASA (ISS013-E-74843)',
  lead='Since 1972, the Arbor Day Foundation says it has planted more than half a billion trees, working in more than 60 countries (nonprofit figures).',
  eli=['The Arbor Day Foundation is a group that plants trees.',
       'It has helped plant more than 500 million trees.',
       'Trees clean the air, give animals homes and help cool the planet.'],
  ws=[('Who', 'The Arbor Day Foundation, a nonprofit, with more than 5,400 local planting partners (Arbor Day Foundation).', ADF),
      ('What', 'Planting, nurturing and celebrating trees at scale.', ADF),
      ('When', 'Planting since 1972, more than 50 years (Arbor Day Foundation).', ADF),
      ('Where', 'In more than 60 countries around the globe (Arbor Day Foundation).', ADF),
      ('Why', 'Trees absorb carbon from the atmosphere, and planted at scale they are a key tool against climate change (Arbor Day Foundation).', ADF)],
  impact=('The Arbor Day Foundation says it has planted more than half a billion trees since 1972 (nonprofit figure).', ADF),
  fact=('5,400 Partners', 'The Foundation works with more than 5,400 planting partners who work locally (Arbor Day Foundation).', ADF),
  people=('Trees planted with local partners shape a more hopeful future for communities (Arbor Day Foundation).', ADF),
  nature=('Trees absorb carbon from the atmosphere (Arbor Day Foundation).', ADF),
  support_h='Support the Arbor Day Foundation',
  btns=[('Donate', 'https://www.arborday.org/donate'), ('See Their Impact', ADF[0])],
  bottom=('Support the Arbor Day Foundation directly.', 'https://www.arborday.org/donate', 'Donate'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 40.813, 'lng': -96.702, 'label': 'Arbor Day Foundation, Lincoln, Nebraska', 'basis': 'hq'}]}),
 dict(slug='Namami_Gange', title='Namami Gange (India)', short='Namami Gange', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='government', status='active', glass='rivers', label='Government solution · active',
  img=('Sundarbans_Ganges_Delta_ISS.jpg', 1920, 1280, 'The Ganges delta and the Sundarbans mangrove forest on the India-Bangladesh border, seen from the International Space Station'), credit='NASA (iss070e005997, Oct. 19, 2023)',
  lead="India's Namami Gange programme has created or rehabilitated 4,263 million litres a day of sewage treatment for the River Ganga (government figures).",
  eli=['The Ganga is a huge, holy river in India.',
       'Too much dirty water from towns was flowing into it.',
       'India is building treatment plants to clean that water before it reaches the river.'],
  ws=[('Who', "India's Ministry of Jal Shakti, through the National Mission for Clean Ganga (NMCG), with state governments.", PIB_NG),
      ('What', 'Sewage treatment plants and sewer networks, reuse of treated wastewater, and biodiversity work.', PIB_NG),
      ('When', 'Reviewed at the 19th Empowered Task Force meeting on 2 July 2026; 538 MLD was added in financial year 2025-26.', PIB_NG),
      ('Where', 'Along the River Ganga, including Agra, Prayagraj and Varanasi.', PIB_NG),
      ('Why', 'To stop untreated wastewater from entering the river and rejuvenate the Ganga.', PIB_NG)],
  impact=('145 completed sewerage projects have created and rehabilitated 4,263 MLD of treatment capacity and over 4,611 km of sewers (government figures).', PIB_NG),
  fact=('524 Projects', 'Namami Gange has sanctioned 524 projects, of which 363 are complete (government figures).', PIB_NG),
  people=('Treated wastewater plans for Agra, Prayagraj and Varanasi look at reuse for power plants, railways, landscaping and irrigation (government).', PIB_NG),
  nature=('Projects include river ranching to restore native fish and the rescue of a stranded Gangetic dolphin (government).', PIB_NG),
  support_h='Support the Clean Ganga Fund',
  btns=[('Contribute to the Clean Ganga Fund', 'https://nmcg.nic.in/donation_form.aspx'), ('Learn About NMCG', NMCG[0])],
  bottom=('Contribute through the Clean Ganga Fund.', 'https://nmcg.nic.in/donation_form.aspx', 'Donate'), donate_alt='Contribute to the Clean Ganga Fund',
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 25.317, 'lng': 83.006, 'label': 'Varanasi, on the River Ganga, India', 'basis': 'page'}]}),
 dict(slug='Clean_Lakes_Alliance', title='Clean Lakes Alliance (Madison, Wisconsin)', short='Clean Lakes Alliance', cat='lakes',
  hub=('Lakes.html', 'Lakes'), cls='nonprofit', status='active', glass='lakes', label='Nonprofit solution · active',
  img=('Great_Lakes_MODIS.jpg', 1200, 1013, 'The Great Lakes region of North America seen by satellite'), credit='NASA GSFC MODIS Land Rapid Response Team',
  lead="Clean Lakes Alliance works to improve water quality in Madison's Yahara lakes; it reports 81 monitoring stations and over $1.4 million in grants (its figures).",
  eli=['Madison, Wisconsin, has five lakes connected by the Yahara River.',
       'Too much phosphorus washes in and feeds smelly algae blooms.',
       'Volunteers check the lakes and the group helps pay for projects to keep them clean.'],
  ws=[('Who', 'Clean Lakes Alliance, a nonprofit formed in 2010, working with government agencies, lake groups and community nonprofits.', CLA),
      ('What', 'Reducing phosphorus pollution, the top priority, plus volunteer lake monitoring, grants and education.', CLA),
      ('When', 'Since 2010. Its 2024 Impact Report marks the 14th State of the Lakes report card.', CLA),
      ('Where', 'The five Yahara lakes and their watershed in Greater Madison, Wisconsin.', CLA),
      ('Why', 'Phosphorus, mostly from stormwater runoff, is the leading cause of poor clarity, cyanobacteria blooms and beach closures (Clean Lakes Alliance).', CLA)],
  impact=('In 2024, Clean Lakes Alliance reports 81 monitoring stations, and more than $1.4 million in Clean Lakes Grants awarded since 2010 (its figures).', CLAR),
  fact=('An Early Warning App', 'Volunteer monitors post lake conditions to the LakeForecast app, warning when potentially toxic algae blooms form (Clean Lakes Alliance).', CLAR),
  people=('LakeForecast shows the public which beaches are open and where the water is best each day (Clean Lakes Alliance).', CLAR),
  nature=('Grants helped complete a 160-acre prairie at Pheasant Branch Conservancy and native shoreline plantings (Clean Lakes Alliance).', CLAR),
  support_h='Support Clean Lakes Alliance',
  btns=[('Donate', 'https://www.cleanlakesalliance.org/donate/'), ('Read the 2024 Impact Report', CLAR[0])],
  bottom=('Support Clean Lakes Alliance directly.', 'https://www.cleanlakesalliance.org/donate/', 'Donate'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 43.074, 'lng': -89.384, 'label': 'Madison, Wisconsin (Yahara lakes)', 'basis': 'page'}]}),
 dict(slug='Sea_Turtle_Conservancy', title='Sea Turtle Conservancy', short='Sea Turtle Conservancy', cat='ocean',
  hub=('Oceans.html', 'Oceans'), cls='nonprofit', status='active', glass='ocean', label='Nonprofit solution · active',
  img=('Loggerhead_Release_MINWR.jpg', 1920, 1277, 'A rescued loggerhead sea turtle being released at Merritt Island National Wildlife Refuge in Florida'), credit='NASA (2010-5237)',
  lead='Sea Turtle Conservancy works in 8 countries, has tagged and monitored more than 550 turtles and trained over 1,200 researchers (nonprofit figures).',
  eli=['Sea turtles are ancient animals that swim across whole oceans.',
       'Sea Turtle Conservancy protects the beaches where they lay their eggs.',
       'It also tracks turtles with satellites to learn where they go.'],
  ws=[('Who', 'Sea Turtle Conservancy, a nonprofit linked to the pioneering sea turtle scientist Dr. Archie Carr.', STC),
      ('What', 'Research, education, training, advocacy and protection of the habitats sea turtles depend on.', STC),
      ('When', 'Ongoing, with satellite tracking of turtles in the open ocean (Sea Turtle Conservancy).', STC),
      ('Where', 'Field sites around the Caribbean and in North, Central and South America, including Tortuguero, Costa Rica.', STC),
      ('Why', 'Its mission is to ensure the survival of sea turtles in the Caribbean, Atlantic and Pacific (Sea Turtle Conservancy).', STC)],
  impact=('Sea Turtle Conservancy says it has tagged and monitored more than 550 turtles and trained over 1,200 researchers, in 8 countries (nonprofit figures).', STC),
  fact=('Turtles by Satellite', 'Satellite telemetry lets researchers follow sea turtles across the open ocean (Sea Turtle Conservancy).', STC),
  people=('Training more than 1,200 researchers builds local skills to protect sea turtles around the globe (Sea Turtle Conservancy).', STC),
  nature=('Protecting nesting beaches and habitats helps sea turtles survive (Sea Turtle Conservancy).', STC),
  support_h='Support Sea Turtle Conservancy',
  btns=[('Donate', 'https://conserveturtles.org/donate/'), ('Learn About Sea Turtle Conservancy', STC[0])],
  bottom=('Support Sea Turtle Conservancy directly.', 'https://conserveturtles.org/donate/', 'Donate'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 10.54, 'lng': -83.5, 'label': 'Tortuguero, Costa Rica', 'basis': 'page'}]}),
]

# Existing pages that link back (idempotent XLINK1018 block, placed before the page-stats section)
XBACK = {
 'SARSAT.html': [('Galileo.html', 'Galileo Satellite Navigation (EU / ESA)', 'Europe\'s navigation satellites also carry search-and-rescue antennas.'),
                 ('INSAT-3DS.html', 'INSAT-3DS Weather Satellite (ISRO)', 'India\'s weather satellite carries a search-and-rescue transponder.')],
 'CryoSat.html': [('CRISTAL.html', 'CRISTAL Polar Ice and Snow Altimeter (ESA)', 'Will continue CryoSat\'s ice record with a dual-frequency radar.'),
                  ('CIMR.html', 'CIMR Copernicus Imaging Microwave Radiometer (ESA)', 'Will map sea ice and ocean temperature every day.')],
 'GOES-19.html': [('GeoXO.html', 'GeoXO Geostationary Extended Observations (NOAA / NASA)', 'The next generation that will follow the GOES-R Series.')],
 'Coral_Gardeners.html': [('Coral_Vita.html', 'Coral Vita Land-Based Coral Farms', 'Grows corals in tanks on land, then plants them on reefs.')],
 'Coral_Restoration_Foundation.html': [('Coral_Vita.html', 'Coral Vita Land-Based Coral Farms', 'Grows corals in tanks on land, then plants them on reefs.')],
 'Coral_IVF.html': [('Coral_Vita.html', 'Coral Vita Land-Based Coral Farms', 'Grows corals in tanks on land, then plants them on reefs.')],
 'Coral_Reef_Watch.html': [('Coral_Vita.html', 'Coral Vita Land-Based Coral Farms', 'Grows corals in tanks on land, then plants them on reefs.')],
}

def see_block(items, sid='connected'):
    lis = ''.join(f'<li><a href="{u}">{E(t)}</a> <span class="see-why">{E(w)}</span></li>' for u, t, w in items)
    return f'<section class="five-ws see-also" id="{sid}"><h2>Connected Solutions</h2><ul class="see-also-list">{lis}</ul></section>'

def body(p):
    q = dict(p)
    q['impact'] = (p['label'], p['impact'][0], p['impact'][1])
    b, srcs = b17.body(q)
    if p.get('donate_alt'):  # the bottom button goes to a partner fund, not to the page subject
        b = b.replace(f'alt="{E("Donate to " + p["short"])}"', f'alt="{E(p["donate_alt"])}"')
    extra = (p.get('widget') or '') + (see_block(p['see']) if p.get('see') else '')
    if extra:  # after the Five W's, like Titan/PRELUDE
        b = b.replace('</div></section>\n<section class="impact" id="impact">', '</div></section>\n' + extra + '\n<section class="impact" id="impact">', 1)
    return b, srcs

def main():
    tpl = open(os.path.join(ROOT, 'Surfrider_Foundation.html'), encoding='utf8').read()
    eli = json.load(open(os.path.join(ROOT, 'assets/data/eli10.json'), encoding='utf8'))
    ml = json.load(open(os.path.join(ROOT, 'assets/data/map-locations.json'), encoding='utf8'))
    for p in PAGES:
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
    ICON = {'Polar.html': '🧊', 'Earth_Observation.html': '🌍', 'Oceans.html': '🌊', 'Deforestation.html': '🌳', 'Rivers.html': '💧', 'Lakes.html': '🏞️', 'Project-Rawane.html': '🚀'}
    ANCHOR = {'Project-Rawane.html': 'id="group-voyages-outward"'}
    for p in PAGES:
        hf, hn = p['hub']; s = p['slug']; im, w, h, alt = p['img']
        fp = os.path.join(ROOT, hf); t = open(fp, encoding='utf8').read()
        if f'class="photo-link" href="{s}.html"' in t: continue
        card = (f'<article class="card"><div class="image-container"><a class="photo-link" href="{s}.html"><img src="assets/{im}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a></div>'
                f'<p class="sol-badges"><span class="status-badge status-active">Active</span><span class="hub-tag"><span aria-hidden="true">{ICON[hf]}</span> {hn}</span></p>'
                f'<h3><a href="{s}.html">{E(p["title"])}</a></h3><p class="card-blurb">{E(p["lead"])}</p></article>')
        i = t.find(ANCHOR.get(hf, 'id="missions"')); j = t.find('</div></section>', i)
        k = t.rfind('</article>', i, j) + len('</article>')
        t = t[:k] + card + t[k:]
        open(fp, 'w', encoding='utf8').write(t)
    for f, items in XBACK.items():
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = '<!-- XLINK1018:START -->' + see_block(items, 'connected-1018') + '<!-- XLINK1018:END -->'
        if '<!-- XLINK1018:START -->' in t:
            t = re.sub(r'<!-- XLINK1018:START -->.*?<!-- XLINK1018:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    json.dump(eli, open(os.path.join(ROOT, 'assets/data/eli10.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump(ml, open(os.path.join(ROOT, 'assets/data/map-locations.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('wrote', len(PAGES), 'pages;', len(XBACK), 'cross-link blocks')

if __name__ == '__main__':
    main()
