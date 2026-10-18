#!/usr/bin/env python3
"""Oct 17 2026 batch: six approved solutions (A Parker Solar Probe, B SOHO, C MTG, D CryoSat, E SMAP, F GCOM-C,
G International Coastal Cleanup, H The SeaCleaners, I Tideway, J Penobscot, K Kissimmee, N WeForest).
Writes the English source pages from the shared solution template (Surfrider_Foundation.html
at 29b1c1fa skeleton) + eli10.json + map-locations.json entries + apply-heroes is edited by hand.
Every fact below is from the cited page (fetched 2026-10-17). Re-runnable: overwrites only these six pages."""
import json, html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

def src(url, name):
    return f'<p class="fact-source">Source: <a href="{url}" target="_blank" rel="noreferrer">{E(name)}</a></p>'

NASA_PSP = ('https://science.nasa.gov/mission/parker-solar-probe/', 'NASA, Parker Solar Probe')
NASA_SOHO = ('https://science.nasa.gov/mission/soho/', 'NASA, SOHO')
ESA_SOHO = ('https://www.esa.int/Science_Exploration/Space_Science/SOHO_overview2', 'ESA, SOHO overview')
ESA_CS = ('https://www.esa.int/Applications/Observing_the_Earth/FutureEO/CryoSat', 'ESA, CryoSat')
ESA_CSF = ('https://www.esa.int/Applications/Observing_the_Earth/FutureEO/CryoSat/Facts_and_figures', 'ESA, CryoSat facts and figures')
ESA_CSL = ('https://www.esa.int/Applications/Observing_the_Earth/FutureEO/CryoSat/85_new_subglacial_lakes_detected_below_Antarctica', 'ESA, 85 new subglacial lakes detected below Antarctica')
OC_ICC = ('https://oceanconservancy.org/trash-free-seas/international-coastal-cleanup/', 'Ocean Conservancy, International Coastal Cleanup')
TSC = ('https://www.theseacleaners.org/', 'The SeaCleaners')
WEF = ('https://www.weforest.org/about-us/', 'WeForest, About us')

PAGES = [
 dict(slug='Parker_Solar_Probe', title='Parker Solar Probe (NASA)', short='Parker Solar Probe', cat='space-weather',
  hub=('Space_Weather.html', 'Space Weather'), cls='agency', status='active', glass='space',
  img=('SDO_Sun.jpg', 1600, 900, 'The Sun seen by NASA\'s Solar Dynamics Observatory'), credit='NASA/SDO',
  lead='The first spacecraft to fly through the Sun\'s outer atmosphere, helping scientists understand the space weather that affects life and technology on Earth (NASA).',
  eli=['Parker Solar Probe is a spacecraft that flies closer to the Sun than any other.',
       'A thick heat shield keeps it safe from the Sun\'s heat.',
       'It helps scientists learn about solar storms that can affect satellites on Earth.'],
  ws=[('Who','NASA\'s Goddard Space Flight Center and the Johns Hopkins University Applied Physics Laboratory run the mission. It is named for Dr. Eugene N. Parker, who predicted the solar wind in the 1950s.',NASA_PSP),
      ('What','A spacecraft with four instrument suites that study magnetic fields, plasma and energetic particles, and take images of the solar wind.',NASA_PSP),
      ('When','It launched in 2018. In 2021 it became the first spacecraft to fly through the corona, the Sun\'s upper atmosphere.',NASA_PSP),
      ('Where','In orbit around the Sun, well inside the orbit of Mercury. At its closest it comes within about 3.9 million miles (6.2 million km) of the Sun.',NASA_PSP),
      ('Why','Space weather can change the orbits of satellites, shorten their lifetimes or interfere with their electronics. Parker\'s data are key to understanding and forecasting it.',NASA_PSP)],
  impact=('Agency solution · active','At closest approach, Parker Solar Probe moves at about 430,000 mph (700,000 km/h), fast enough to get from Philadelphia to Washington, D.C., in one second (NASA).',NASA_PSP),
  fact=('A 4.5-Inch Heat Shield','Parker\'s 4.5-inch-thick carbon-composite shield can withstand temperatures of nearly 2,500 degrees Fahrenheit (1,377 Celsius).',NASA_PSP),
  people=('Parker\'s data help forecast space weather that can disrupt the satellites people depend on (NASA).',NASA_PSP),
  nature=('We live in the Sun\'s atmosphere, and Parker helps scientists understand the Sun\'s impact on Earth (NASA).',NASA_PSP),
  support_h='Get Involved With Parker Solar Probe',
  btns=[('Learn About Parker Solar Probe',NASA_PSP[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? NASA has the full Parker Solar Probe story.',NASA_PSP[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':39.165,'lng':-76.898,'label':'Johns Hopkins Applied Physics Laboratory, Laurel, Maryland (mission partner)','basis':'hq'}],'strip':'orbit'}),
 dict(slug='SOHO', title='SOHO Solar and Heliospheric Observatory (ESA / NASA)', short='SOHO', cat='space-weather',
  hub=('Space_Weather.html', 'Space Weather'), cls='agency', status='active', glass='space',
  img=('SDO_Sun.jpg', 1600, 900, 'The Sun seen by NASA\'s Solar Dynamics Observatory'), credit='NASA/SDO',
  lead='Watching the Sun nonstop since 1995, SOHO helps experts predict solar storms and has found more than 5,000 comets (NASA).',
  eli=['SOHO is a spacecraft that has watched the Sun every day for 30 years.',
       'It sits in a special spot in space where it can always see the Sun.',
       'Its pictures help people get ready for solar storms.'],
  ws=[('Who','SOHO is a joint project of ESA and NASA. ESA leads the mission, and NASA contributed three instruments and the launch.',NASA_SOHO),
      ('What','An observatory with 12 instruments that studies the Sun from its hot interior to its stormy atmosphere and the solar wind.',ESA_SOHO),
      ('When','SOHO launched on 2 December 1995. It was meant to work until 1998, and in December 2025 it marked 30 years of operation.',NASA_SOHO),
      ('Where','About 1.5 million kilometres (932,000 miles) from Earth, orbiting the L1 point, where it has an uninterrupted view of the Sun.',ESA_SOHO),
      ('Why','Experts around the world use SOHO images and data to help predict space weather events that affect our planet.',ESA_SOHO)],
  impact=('Agency solution · active','SOHO is the most prolific discoverer of comets in history, with more than 5,000 found, over half of all known comets (NASA).',NASA_SOHO),
  fact=('Lost and Found in Space','In 1998 contact with SOHO was lost for weeks. A powerful radar signal from Earth found it, and engineers brought it back to work (ESA).',ESA_SOHO),
  people=('SOHO plays a vital role in forecasting potentially dangerous solar storms (NASA).',NASA_SOHO),
  nature=('SOHO has watched two full 11-year solar cycles, showing how our star changes over time (NASA).',NASA_SOHO),
  support_h='Get Involved With SOHO',
  btns=[('Learn About SOHO',ESA_SOHO[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? NASA has the full SOHO story.',NASA_SOHO[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':43.604,'lng':1.444,'label':'Toulouse, France, where SOHO was assembled','basis':'page'}],'strip':'orbit'}),
 dict(slug='CryoSat', title='CryoSat Ice Mission (ESA)', short='CryoSat', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth',
  img=('Labrador_Sea_Ice_ISS.jpg', 1920, 1280, 'Sea ice in the Labrador Sea seen from the International Space Station'), credit='NASA (ISS070-E-086805, Feb. 3, 2024)',
  lead='CryoSat measures polar sea ice and the great ice sheets from space, and its data revealed 85 hidden lakes under Antarctica (ESA).',
  eli=['CryoSat is a satellite that measures how thick the ice is near the North and South Poles.',
       'It uses radar to spot tiny changes in the height of the ice.',
       'Knowing how ice changes helps scientists understand sea level rise.'],
  ws=[('Who','The European Space Agency (ESA). CryoSat is an Earth Explorer mission, flown from ESA\'s operations centre in Darmstadt, Germany.',ESA_CSF),
      ('What','A satellite carrying a radar altimeter built for ice. It measures the thickness of polar sea ice and changes in the ice sheets of Greenland and Antarctica.',ESA_CS),
      ('When','CryoSat launched on 8 April 2010 and has been in orbit for more than 10 years, far beyond its minimum 3-year mission.',ESA_CSF),
      ('Where','In a polar orbit at a mean altitude of 719 km, which lets it see almost the whole of the Arctic and Antarctic.',ESA_CSF),
      ('Why','Lakes under the ice affect how fast glaciers move and so influence global sea level rise.',ESA_CSL)],
  impact=('Agency solution · active','A decade of CryoSat data revealed 85 unknown lakes under Antarctica, raising the known active subglacial lakes by more than half, to 231 (ESA).',ESA_CSL),
  fact=('First of Its Kind','CryoSat carries the first radar altimeter of its kind, designed to measure ice (ESA).',ESA_CS),
  people=('CryoSat data help improve projections of future sea level rise, which matters for coastal communities (ESA).',ESA_CSL),
  nature=('CryoSat tracks the polar sea ice and ice sheets that shape the oceans around them (ESA).',ESA_CSL),
  support_h='Get Involved With CryoSat',
  btns=[('Learn About CryoSat',ESA_CS[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? ESA has the full CryoSat story.',ESA_CS[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':49.871,'lng':8.622,'label':'ESA mission control (ESOC), Darmstadt, Germany','basis':'page'}],'strip':'orbit'}),
 dict(slug='International_Coastal_Cleanup', title='International Coastal Cleanup (Ocean Conservancy)', short='Ocean Conservancy', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='nonprofit', status='active', glass='ocean',
  img=('Bahamas_Ocean_ISS.jpg', 1000, 667, 'Turquoise ocean around the Bahamas seen from the International Space Station'), credit='NASA, International Space Station',
  lead='Since 1986, more than 19 million volunteers have collected more than 400 million pounds of trash from beaches and waterways (Ocean Conservancy).',
  eli=['Every year, people around the world clean trash off beaches and rivers on the same day.',
       'They also write down what they find.',
       'That list helps find ways to stop trash from reaching the ocean.'],
  ws=[('Who','Ocean Conservancy, working with volunteer groups and people around the globe.',OC_ICC),
      ('What','A global cleanup where volunteers remove trash from beaches and waterways and record every item they collect.',OC_ICC),
      ('When','It began in 1986 with 2,800 volunteers and has grown every year since.',OC_ICC),
      ('Where','It started on the coast of Texas and now happens on beaches and waterways around the world.',OC_ICC),
      ('Why','Recording each item builds the world\'s largest database on marine debris, used to find ways to stop ocean trash.',OC_ICC)],
  impact=('Nonprofit solution · active','More than 19 million volunteers have collected more than 400 million pounds of trash since the Cleanup began (Ocean Conservancy).',OC_ICC),
  fact=('The World\'s Biggest Trash List','Cleanup volunteers add to the world\'s largest database on marine debris (Ocean Conservancy).',OC_ICC),
  people=('Volunteers make beaches and waterways cleaner for the communities that use them (Ocean Conservancy).',OC_ICC),
  nature=('Every item picked up is trash that no longer litters the coast and waterways (Ocean Conservancy).',OC_ICC),
  support_h='Support the International Coastal Cleanup',
  btns=[('Donate','https://donate.oceanconservancy.org/page/177540/donate/1'),('Become a Partner','https://oceanconservancy.org/work/plastics/cleanups-icc/partners/'),('Find a Cleanup','Find_a_Cleanup.html')],
  bottom=('Support Ocean Conservancy directly.','https://donate.oceanconservancy.org/page/177540/donate/1','Donate'),
  pin={'status':'active','pins':[{'lat':29.3,'lng':-94.8,'label':'Texas coast, where the first Cleanup was held in 1986','basis':'page'}],'strip':'world'}),
 dict(slug='The_SeaCleaners', title='The SeaCleaners', short='The SeaCleaners', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='nonprofit', status='active', glass='ocean',
  img=('PlasticBank_Indonesia_STS66.jpg', 1200, 946, 'Islands of Indonesia seen from the Space Shuttle'), credit='NASA (STS-66)',
  lead='Mobula cleanup boats catch plastic close to where it starts, and in Malaysia one boat turned 135,000 pieces of debris into community walkways (The SeaCleaners).',
  eli=['The SeaCleaners use special boats called Mobulas to scoop plastic out of the water.',
       'They work with local people so the cleanup keeps going after they leave.',
       'Some of the plastic is recycled into useful things, like walkways.'],
  ws=[('Who','The SeaCleaners, working with local teams, partners and volunteers.',TSC),
      ('What','Three-year expeditions that use Mobula boats and floating barriers to clean up waste, support local recycling and engage communities.',TSC),
      ('When','In 2025 the Mobula 8.2 worked in Kota Kinabalu, Malaysia; in its first three months it collected more than 53,000 pieces of plastic waste.',TSC),
      ('Where','Expeditions in Kota Kinabalu, Malaysia, and in Bali and Ambon, Indonesia.',TSC),
      ('Why','Catching pollution close to its source, before it spreads at sea, delivers measurable impact.',TSC)],
  impact=('Nonprofit solution · active','In Kota Kinabalu, the Mobula 8.2 collected 2 tons of waste, trained local teams and turned 630 kg of plastic into 61 meters of walkways (The SeaCleaners).',TSC),
  fact=('Plastic Into Walkways','The SeaCleaners turned 630 kg of collected plastic into 61 meters of walkways in Malaysia.',TSC),
  people=('Each mission trains local people so they can keep the cleanup going after the expedition ends (The SeaCleaners).',TSC),
  nature=('Mobula boats remove plastic waste from coastal waters before it reaches the open ocean (The SeaCleaners).',TSC),
  support_h='Support The SeaCleaners',
  btns=[('Donate','https://www.theseacleaners.org/en/donate/'),('Volunteer','https://www.theseacleaners.org/en/news/join-the-seacleaners-wave/')],
  bottom=('Support The SeaCleaners directly.','https://www.theseacleaners.org/en/donate/','Donate'),
  pin={'status':'active','pins':[{'lat':5.98,'lng':116.073,'label':'Kota Kinabalu, Malaysia (Mobula 8.2 expedition)','basis':'page'},{'lat':-3.695,'lng':128.181,'label':'Ambon, Indonesia','basis':'page'},{'lat':-8.65,'lng':115.216,'label':'Bali, Indonesia','basis':'page'}],'strip':None}),
 dict(slug='WeForest', title='WeForest', short='WeForest', cat='forests',
  hub=('Deforestation.html', 'Forests'), cls='nonprofit', status='active', glass='forests',
  img=('Kilimanjaro_STS72.jpg', 1200, 1200, 'Mount Kilimanjaro and the surrounding forests of East Africa seen from the Space Shuttle'), credit='NASA (STS-72)',
  lead='WeForest has grown more than 118 million trees and has 100,000 hectares of forest under restoration and conservation (WeForest).',
  eli=['WeForest helps whole areas of land grow back into healthy forests.',
       'It works with local families so trees and people can both thrive.',
       'It has grown more than 118 million trees so far.'],
  ws=[('Who','WeForest, a nonprofit with more than 100 staff, mostly in its field offices in Zambia and Ethiopia, and a global team in Brussels.',WEF),
      ('What','It restores and conserves forests at the landscape level, to get the most out of trees for people, nature and climate.',WEF),
      ('When','Founded in 2009. For its first three years everyone was a volunteer and every euro went to growing trees.',WEF),
      ('Where','Mainly in Zambia and Ethiopia, with its global team in Brussels, Belgium.',WEF),
      ('Why','Its vision is a world where communities and nature sustainably thrive together.',WEF)],
  impact=('Nonprofit solution · active','WeForest has grown more than 118 million trees and has 100,000 hectares of forest under restoration and conservation (WeForest).',WEF),
  fact=('45,000 Households','WeForest has engaged 45,000 households in alternative livelihood activities.',WEF),
  people=('WeForest has engaged 45,000 households in alternative livelihood activities (WeForest).',WEF),
  nature=('100,000 hectares of forest are under restoration and conservation with WeForest (WeForest).',WEF),
  support_h='Support WeForest',
  btns=[('Donate','https://www.weforest.org/donate/'),('Partner With WeForest','https://www.weforest.org/partner-with-us/business-partnerships/')],
  bottom=('Support WeForest directly.','https://www.weforest.org/donate/','Donate'),
  pin={'status':'active','pins':[{'lat':-15.417,'lng':28.283,'label':'Zambia field office (Lusaka)','basis':'page'},{'lat':9.03,'lng':38.74,'label':'Ethiopia field office (Addis Ababa)','basis':'page'}],'strip':None}),
]

ESA_MTG2 = ('https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/meteosat_third_generation/MTG-I2_completes_Europe_s_latest_weather_trio', "ESA, MTG-I2 completes Europe's latest weather trio")
ESA_LI = ('https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/meteosat_third_generation/Lightning_Imager', 'ESA, Lightning Imager')
NASA_SMAP = ('https://science.nasa.gov/mission/smap/', 'NASA, SMAP')
JPL_SMAP = ('https://smap.jpl.nasa.gov/', 'NASA JPL, SMAP')
JAXA_GC = ('https://global.jaxa.jp/projects/sat/gcom_c/', 'JAXA, GCOM-C "SHIKISAI"')
TIDE = ('https://www.tideway.london/the-tunnel/', 'Tideway, The tunnel')
DMR = ('https://www.maine.gov/dmr/sites/maine.gov.dmr/files/inline-files/Trap%20Counts%20for%20Web%20Page%202025.pdf', 'Maine Department of Marine Resources, trap counts 2015-2025')
OUP = ('https://academic.oup.com/mcf/article/15/1/e210227/7810984', 'Marine and Coastal Fisheries, Fish assemblages in the Penobscot River a decade after dam removal')
PRT = ('https://www.penobscotriver.org/', 'Penobscot River Restoration Trust')
SFWMD = ('https://www.sfwmd.gov/our-work/kissimmee-river', 'South Florida Water Management District, Kissimmee River')

PAGES += [
 dict(slug='Meteosat_Third_Generation', title='Meteosat Third Generation (ESA / EUMETSAT)', short='Meteosat Third Generation', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth',
  img=('Lightning_Storm_ISS.jpg', 1600, 1067, 'Lightning lights up storm clouds off North Carolina, seen from the International Space Station'), credit='NASA (iss073e0080625, May 15, 2025)',
  lead='Three weather satellites now watch Europe and Africa from 36,000 km up, with new images every 2.5 minutes and a camera that catches lightning day and night (ESA).',
  eli=['Meteosat Third Generation is a team of weather satellites that watch Europe and Africa.',
       'One camera takes a new picture of the weather every 2.5 minutes.',
       'Another camera spots lightning, which helps warn people about dangerous storms.'],
  ws=[('Who','ESA developed the satellites and EUMETSAT operates them, sharing the data. Thales Alenia Space led the European industry team that built them.',ESA_MTG2),
      ('What','Imager and Sounder satellites. The Imagers carry a Flexible Combined Imager and a Lightning Imager that sees lightning by day and night.',ESA_MTG2),
      ('When','The first Imager launched in 2022 and the Sounder followed. MTG-I2 launched on 27 August 2026 on Ariane 6, completing the three-satellite system.',ESA_MTG2),
      ('Where','In geostationary orbit about 36,000 km up, watching the same part of Earth over Europe and Africa as it turns.',ESA_MTG2),
      ('Why','Lightning is a clear sign of turbulence linked to extreme weather, so spotting it early allows early warnings and storm tracking.',ESA_LI)],
  impact=('Agency solution · active','MTG-I2 will deliver new images over Europe every 2.5 minutes, supporting early warnings and the tracking of wildfires and air pollution (ESA).',ESA_MTG2),
  fact=('Three Million Flashes a Day','Around the world there are over three million lightning flashes every day (ESA).',ESA_LI),
  people=('MTG data support early warnings and will substantially improve weather forecasts for all European countries (ESA).',ESA_MTG2),
  nature=('The satellites also provide key data for monitoring water, farming and the environment (ESA).',ESA_MTG2),
  support_h='Get Involved With Meteosat Third Generation',
  btns=[('Learn About Meteosat Third Generation',ESA_MTG2[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? ESA has the full MTG story.',ESA_MTG2[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':5.24,'lng':-52.77,'label':"MTG-I2 launched from Europe's Spaceport, French Guiana",'basis':'launch'}],'strip':'orbit'}),
 dict(slug='SMAP', title='SMAP Soil Moisture Active Passive (NASA)', short='SMAP', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth',
  img=('Mississippi_River_PIA23534.jpg', 892, 1280, 'The Mississippi River seen from space'), credit='NASA/JPL (PIA23534)',
  lead='SMAP maps the water in Earth\'s soil from space, helping improve predictions of weather, floods and droughts (NASA).',
  eli=['SMAP is a satellite that measures how wet or dry the ground is.',
       'It can also tell if the soil is frozen or thawed.',
       'This helps farmers and scientists get ready for floods and droughts.'],
  ws=[('Who','NASA. The mission is run from NASA\'s Jet Propulsion Laboratory in Pasadena, California.',JPL_SMAP),
      ('What','A satellite with a radar, a radiometer and the largest rotating mesh antenna ever deployed in space, 20 feet (6 meters) wide.',JPL_SMAP),
      ('When','SMAP launched on 31 January 2015 and is an active NASA mission.',NASA_SMAP),
      ('Where','It launched on a Delta II rocket from Vandenberg Air Force Base, California, and orbits Earth mapping soils worldwide.',JPL_SMAP),
      ('Why','Soil moisture links Earth\'s water, energy and carbon cycles, so mapping it improves predictions of weather, climate, floods and droughts.',NASA_SMAP)],
  impact=('Agency solution · active','SMAP maps soil moisture and whether soils are frozen or thawed across the globe (NASA).',NASA_SMAP),
  fact=('A Golden Lasso in Space','SMAP\'s 20-foot (6-meter) "golden lasso" antenna is the largest rotating mesh antenna ever deployed in space (NASA JPL).',JPL_SMAP),
  people=('Better forecasts of floods and droughts help communities and farmers prepare (NASA).',NASA_SMAP),
  nature=('Soil moisture connects the water, energy and carbon cycles that all life depends on (NASA).',NASA_SMAP),
  support_h='Get Involved With SMAP',
  btns=[('Learn About SMAP',NASA_SMAP[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? NASA has the full SMAP story.',NASA_SMAP[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':34.2,'lng':-118.17,'label':'NASA Jet Propulsion Laboratory, Pasadena, California','basis':'page'}],'strip':'orbit'}),
 dict(slug='GCOM-C', title='GCOM-C "SHIKISAI" (JAXA)', short='GCOM-C', cat='earth-observation',
  hub=('Earth_Observation.html', 'Earth Observation'), cls='agency', status='active', glass='earth',
  img=('Pacific_Clouds_Sunset_ISS.jpg', 1920, 1280, 'Clouds over the Pacific Ocean at sunset seen from the International Space Station'), credit='NASA (ISS074-E-0046371, Jan. 3, 2026)',
  lead='Japan\'s SHIKISAI satellite checks the health of Earth from space every 2 or 3 days, tracking clouds, aerosols, ocean color, plants, snow and ice (JAXA).',
  eli=['GCOM-C, also called SHIKISAI, is a Japanese satellite that looks at the whole Earth.',
       'It sees clouds, tiny particles in the air, plants, ocean color, snow and ice.',
       'This helps scientists understand climate change.'],
  ws=[('Who','JAXA, the Japan Aerospace Exploration Agency, as part of its Global Change Observation Mission (GCOM).',JAXA_GC),
      ('What','A satellite carrying SGLI, an optical sensor that sees from near-ultraviolet to thermal infrared light at 250 m to 1 km detail.',JAXA_GC),
      ('When','GCOM-C launched on 23 December 2017 on an H-IIA rocket and is in operation.',JAXA_GC),
      ('Where','In orbit about 798 km above Earth, covering the whole globe every 2 or 3 days.',JAXA_GC),
      ('Why','Long-term views of aerosols, clouds, plants and temperatures help explain climate change and improve climate models.',JAXA_GC)],
  impact=('Agency solution · active','SGLI collects global data once every 2 or 3 days on clouds, aerosols, ocean color, vegetation, snow and ice (JAXA).',JAXA_GC),
  fact=('From Ultraviolet to Heat','SGLI observes light from near-ultraviolet to thermal infrared, from 380 nanometres to 12 micrometres (JAXA).',JAXA_GC),
  people=('GCOM-C data help improve the accuracy of predictions of future environmental change (JAXA).',JAXA_GC),
  nature=('SGLI maps phytoplankton in the ocean and the health of vegetation on land (JAXA).',JAXA_GC),
  support_h='Get Involved With GCOM-C',
  btns=[('Learn About GCOM-C',JAXA_GC[0]),('Join NASA Citizen Science','https://science.nasa.gov/citizen-science/')],
  bottom=('Want to go deeper? JAXA has the full GCOM-C story.',JAXA_GC[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':35.683,'lng':139.56,'label':'JAXA headquarters, Tokyo, Japan','basis':'hq'}],'strip':'orbit'}),
 dict(slug='London_Tideway_Tunnel', title='London Tideway Tunnel (Super Sewer)', short='the Tideway Tunnel', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='corporate', status='active', glass='rivers',
  img=('London_Thames_Night_ISS.jpg', 1600, 1067, 'London at night, split by the dark curve of the River Thames, seen from the International Space Station'), credit='NASA (iss074e0381351, March 13, 2026)',
  lead='London\'s new super sewer catches sewage that used to spill into the River Thames in storms, with room for 1.6 million cubic metres (Tideway).',
  eli=['When it rains hard in London, old sewers used to overflow into the River Thames.',
       'A giant new tunnel under the river now catches that dirty water.',
       'The water is sent away to be cleaned, so the river stays healthier.'],
  ws=[('Who','Tideway, the company that built the London Tideway Tunnel.',TIDE),
      ('What','A "super sewer" tunnel 7.2 metres wide that intercepts, stores and transfers sewage away from the River Thames.',TIDE),
      ('When','In May 2024 the super sewer was connected to the Lee Tunnel, working since 2016, completing the full network.',TIDE),
      ('Where','Under London, from Acton in the west, 31 metres deep, falling to 66 metres at Abbey Mills Pumping Station in the east.',TIDE),
      ('Why','During heavy storms, rain and sewage used to spill into the Thames at overflow points. The tunnel now captures it to be treated.',TIDE)],
  impact=('Company solution · active','The London Tideway Tunnel network can store 1.6 million cubic metres of sewage, about 600 Olympic-size swimming pools, to protect the tidal Thames (Tideway).',TIDE),
  fact=('600 Swimming Pools','The super sewer can hold about 600 Olympic-size swimming pools of sewage (Tideway).',TIDE),
  people=('The tunnel protects the river that runs through the heart of London from polluting sewage spills (Tideway).',TIDE),
  nature=('Sewage is now captured and sent for treatment, protecting the river and its wildlife (Tideway).',TIDE),
  support_h='Learn More About the Tideway Tunnel',
  btns=[('Learn About the Tunnel',TIDE[0]),('Find a Cleanup','Find_a_Cleanup.html')],
  bottom=('Want to go deeper? Tideway has the full story of the tunnel.',TIDE[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':51.531,'lng':-0.002,'label':'Abbey Mills Pumping Station, East London','basis':'page'},{'lat':51.508,'lng':-0.27,'label':'Acton, West London (tunnel start)','basis':'page'}]}),
 dict(slug='Penobscot_River_Restoration', title='Penobscot River Restoration (Maine)', short='the Penobscot River Restoration', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='nonprofit', status='active', glass='rivers',
  img=('New_England_Coast_ISS.jpg', 1600, 1067, 'The New England coast from Massachusetts to Maine seen from the International Space Station'), credit='NASA (iss072e394484, Dec. 18, 2024)',
  lead='After two dams came out of Maine\'s Penobscot River, nearly 5.93 million river herring climbed the Milford fish lift in 2025, up from about 590,000 in 2015 (Maine DMR).',
  eli=['Dams on the Penobscot River blocked fish from swimming up to lay their eggs.',
       'People took out two dams and built new ways for fish to get past others.',
       'Now millions of fish swim up the river again each year.'],
  ws=[('Who','The Penobscot River Restoration Trust, a nonprofit, with the Penobscot Indian Nation, the State of Maine, federal agencies, conservation groups and a hydropower company.',PRT),
      ('What','Removing the Great Works and Veazie dams, adding a fish lift at Milford Dam and a fish bypass around Howland Dam, while keeping hydropower.',OUP),
      ('When','Great Works Dam came out in 2012, Veazie Dam in 2013, and the Howland bypass was built in 2016.',OUP),
      ('Where','The Penobscot River, Maine\'s largest river, which drains about a quarter of the state into Penobscot Bay.',PRT),
      ('Why','For centuries, dams blocked sea-run fish from their spawning grounds. The project improves access to nearly 1,000 miles of habitat for 11 native sea-run fish species.',PRT)],
  impact=('Nonprofit solution · active','River herring counted at the Milford fish lift rose from 589,645 in 2015 to 5,927,002 in 2025 (Maine Department of Marine Resources).',DMR),
  fact=('From 556 to Millions','Before restoration, an average of just 556 river herring returned each year (1978-2012). By 2018 the count passed 2.3 million.',OUP),
  people=('Reconnecting the river rejoins the Penobscot Indian Nation\'s homeland with the Atlantic Ocean and revives fishing and paddling traditions (Penobscot River Restoration Trust).',PRT),
  nature=('Eight of the 12 sea-run fish species native to the Penobscot have used the new Milford fish lift to swim upriver (Marine and Coastal Fisheries).',OUP),
  support_h='Learn More About the Penobscot River',
  btns=[('Learn About the Project',PRT[0]),('Find a Cleanup','Find_a_Cleanup.html')],
  bottom=('Want to go deeper? The Penobscot River Restoration Trust has the full story.',PRT[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':44.94,'lng':-68.65,'label':'Milford Dam fish lift, Penobscot River, Maine','basis':'page'}]}),
 dict(slug='Kissimmee_River_Restoration', title='Kissimmee River Restoration (Florida)', short='the Kissimmee River Restoration', cat='rivers',
  hub=('Rivers.html', 'Rivers'), cls='government', status='active', glass='rivers',
  img=('Florida_Keys_PIA03890.jpg', 1200, 691, 'The Florida Keys seen from space'), credit='NASA/JPL (PIA03890)',
  lead='Once straightened into a canal, Florida\'s Kissimmee River is winding again: 44 miles of river and 20,000 acres of wetlands restored (SFWMD).',
  eli=['Long ago, people dug a straight canal through the curvy Kissimmee River.',
       'That stopped floods but hurt the wetlands, birds and fish.',
       'Now workers have filled parts of the canal so the river can curve and flood its wetlands again.'],
  ws=[('Who','The South Florida Water Management District and the U.S. Army Corps of Engineers, working together.',SFWMD),
      ('What','Filling in part of the C-38 canal so water flows again through the river\'s old curves and floods its wetlands with the seasons.',SFWMD),
      ('When','Congress authorized it in 1992, construction began in 1999, and the finish of construction was celebrated in July 2021.',SFWMD),
      ('Where','Central Florida, between Lake Kissimmee and Lake Okeechobee. The basin is the headwaters of Lake Okeechobee and the Everglades.',SFWMD),
      ('Why','In the 1960s the river was dredged into a straight canal. It gave flood protection but destroyed much of the floodplain ecosystem.',SFWMD)],
  impact=('Government solution · active','The project restores more than 40 square miles of river floodplain, 20,000 acres of wetlands and 44 miles of meandering river (SFWMD).',SFWMD),
  fact=('103 Miles of Bends','The Kissimmee River once meandered for 103 miles through central Florida (SFWMD).',SFWMD),
  people=('The project kept flood protection in place while restoring the river (SFWMD).',SFWMD),
  nature=('Seasonal rains and flows now flood the restored floodplain again, where native wetland plants, wading birds and fish once thrived (SFWMD).',SFWMD),
  support_h='Learn More About the Kissimmee River',
  btns=[('Learn About the Project',SFWMD[0]),('Find a Cleanup','Find_a_Cleanup.html')],
  bottom=('Want to go deeper? The South Florida Water Management District has the full story.',SFWMD[0],'For Further Information'),
  pin={'status':'active','pins':[{'lat':27.5,'lng':-81.05,'label':'Kissimmee River, central Florida','basis':'page'}]}),
]

def body(p):
    s = p['slug']; im, w, h, alt = p['img']
    ws = ''.join(f'<div class="w-card"><h3>{k}</h3><p>{E(t)}</p>{src(*c)}</div>' for k, t, c in p['ws'])
    lab, it, ic = p['impact']; ft, fx, fc = p['fact']
    btns = ''.join(f'<a class="btn help-btn" href="{u}"' + ('' if u.endswith('.html') else ' target="_blank" rel="noopener"') + f'>{E(l)}</a>' for l, u in p['btns'])
    bt, bu, bl = p['bottom']; subtle = '' if bl == 'Donate' else ' donate-btn-subtle'
    balt = (f'Donate to {p["short"]}' if bl == 'Donate' else f'Learn more about {p["title"]}')
    srcs = {c[0] for _, _, c in p['ws']} | {ic[0], p['people'][1][0], p['nature'][1][0]}
    return f'''<main id="main">
<section class="page-hero space-hero"><div class="page-hero-content"><h1>{E(p['title'])}</h1><p>{E(p['lead'])}</p></div></section>
<p class="photo-credit">Image: {E(p['credit'])}.</p>
<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">Home</a></li><li><a href="{p['hub'][0]}">{p['hub'][1]}</a></li><li><span aria-current="page">{E(p['title'])}</span></li></ol></nav>
<!-- REVIEWED:START --><!-- REVIEWED:END -->
<!-- ELI10:START --><!-- ELI10:END -->
<section class="five-ws" id="solution"><h2>The Five W&#x27;s of {E(p['short'])}</h2><div class="ws-grid">{ws}</div></section>
<section class="impact" id="impact"><h2>Impact Statement</h2><div class="impact-box"><p class="hub-label">{E(lab)}</p><p>{E(it)}</p>{src(*ic)}<p><a class="inline-link" href="{ic[0]}" target="_blank" rel="noreferrer">For Further Information: {E(ic[1])}</a></p><p class="amazing-fact" hidden data-title="{E(ft)}" data-source="{fc[0]}" data-source-name="{E(fc[1])}" data-image="assets/{im}" data-image-alt="{E(alt)}" data-image-credit="{E(p['credit'])}">{E(fx)}</p></div></section>
<section class="impact saves-planets" id="saves"><h2>How This Saves People &amp; the Planet</h2><div class="impact-box"><h3 class="mission-title">For People</h3><p>{E(p['people'][0])}</p>{src(*p['people'][1])}<h3 class="mission-title">For Nature</h3><p>{E(p['nature'][0])}</p>{src(*p['nature'][1])}</div></section>
<section class="page-stats" data-stats-category="{p['cat']}" data-stats-page="{s}.html" aria-label="Solution stats" hidden></section>
<section class="five-ws help-cta" id="support"><h2>{E(p['support_h'])}</h2><div class="help-btns">{btns}</div></section>
<section class="donate-banner bottom-link" id="bottom-link"><p>{E(bt)}</p><a href="{bu}" target="_blank" rel="noreferrer" class="donate-btn{subtle}"><img src="assets/{im}" alt="{E(balt)}" width="{w}" height="{h}" loading="lazy" decoding="async"><span>{bl}</span></a></section>
<!-- RELATED:START --><!-- RELATED:END -->
<section class="help-actions" id="help" aria-label="Ways to help"><h2>Help This Work</h2><p>Links go straight to the organization. Saving Planets doesn&#x27;t receive any of the money.</p><div class="help-btns">{btns}</div><p class="help-more"><a href="Ways_to_Help.html">See all ways to help</a></p></section>
</main>''', sorted(srcs)

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
        # Oct 18 (daily numbers check): the Surfrider template carries sp:added 2026-10-15; this batch was released 2026-10-17
        out = re.sub(r'(sp:added" content=")[^"]*', lambda m: m.group(1) + '2026-10-17', out)
        out = re.sub(r'<body[^>]*>', f'<body data-glass="{p["glass"]}" class="hp-{s.lower().replace("_","-")} toc-sub {s.lower().replace("_","-")}-page">', out, count=1)
        # strip old JSON-LD so seo-fix/seo-jsonld rebuild it from this page
        out = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', out, flags=re.S)
        out = re.sub(r'<!-- (TEACHER|CITE|SHARE):START -->.*?<!-- \1:END -->\n?', '', out, flags=re.S)
        out = out.replace('Surfrider Foundation', p['title']).replace('Surfrider', p['short'])
        open(os.path.join(ROOT, s + '.html'), 'w', encoding='utf8').write(out)
        eli[s + '.html'] = p['eli']
        pin = dict(p['pin'])
        if pin.get('strip') is None: pin.pop('strip', None)
        ml['solutions'][s + '.html'] = pin
    ICON = {'Space_Weather.html': '☀️', 'Earth_Observation.html': '🌍', 'Oceans.html': '🌊', 'Deforestation.html': '🌳', 'Rivers.html': '💧'}
    for p in PAGES:
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
    json.dump(eli, open(os.path.join(ROOT, 'assets/data/eli10.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump(ml, open(os.path.join(ROOT, 'assets/data/map-locations.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('wrote', len(PAGES), 'pages')

if __name__ == '__main__':
    main()
