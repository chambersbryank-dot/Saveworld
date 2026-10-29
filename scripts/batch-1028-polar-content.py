#!/usr/bin/env python3
"""Oct 28 2026 polar batch (founder approved all 20, Oct 28): 10 North Pole (Arctic) + 10 South Pole (Antarctica) showcase pages.
Same writer as batch-1023-content.py (batch-1020s skeleton: BLUF, Five W's, Connected Solutions). Every fact was opened on the
organization's own site (or a named page) on 2026-10-28 and is labeled with its source. Showcase only: we feature these because
they help the planet; Saving Planets has no partnership with any of them (each page says so in How You Can Help).
Donate rule (founder, Oct 28): a Donate button only where the organization's own donate page exists AND it publishes audited
finances or carries a recognized charity rating (Charity Navigator Four-Star: PBI, Woodwell/Permafrost Pathways, Oceanites, ASOC;
UK Charity Commission no. 1124840: SCAR). Everyone else gets participation options only.
Images: NASA public domain (images.nasa.gov ids in each credit). Also splits Polar.html #missions into North Pole / South Pole /
Both poles groups (GROUPS below). Re-runnable: overwrites only these pages, their hub cards (added once), the Polar grouping,
XLINK1028 blocks and the ways-to-help.json entries."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b20s', os.path.join(ROOT, 'scripts/batch-1020s-content.py'))
b20s = importlib.util.module_from_spec(spec); spec.loader.exec_module(b20s)
W, see_block, pin = b20s.W, b20s.see_block, b20s.pin
ADDED = '2026-10-28'
TAG = 'XLINK1028'
HUB = ('Polar.html', 'Polar')

def help_block(org, items, donate_note):
    lis = ''.join(f'<li><a href="{E(u, quote=True)}" target="_blank" rel="noreferrer">{E(t)}</a>: {E(d)}</li>' for t, u, d in items)
    return (f'<section class="how-help" id="how-you-can-help"><h2>How You Can Help</h2><ul>{lis}</ul>'
            f'<p class="help-note">{E(donate_note)}</p>'
            f'<p class="help-note">Saving Planets features {E(org)} because its work helps the planet. This is a showcase, not a partnership: we are not partners with {E(org)} and receive nothing from it.</p></section>')

DN_YES = 'Donate links go only to organizations that publish audited finances or carry a recognized charity rating. {r}'
DN_NO = 'No Donate button here: {r} The ways to take part above are real options listed on the organization\'s own site.'

def P(**k):
    k.setdefault('cat', 'polar'); k.setdefault('hub', HUB); k.setdefault('status', 'active'); k.setdefault('glass', 'earth')
    k.setdefault('see', [])
    k['widget'] = help_block(k.pop('org'), k.pop('help'), k.pop('dnote'))
    return k

PBI = ('https://polarbearsinternational.org', 'Polar Bears International, home page')
PBID = 'https://polarbearsinternational.org/donate/'
SMI = ('https://smartice.org', 'SmartICE, home page')
PPW = ('https://permafrost.woodwellclimate.org', 'Permafrost Pathways, home page')
PPA = ('https://permafrost.woodwellclimate.org/about/', 'Permafrost Pathways, About')
PPD = 'https://permafrost.woodwellclimate.org/support/'
TIM = ('https://parks.canada.ca/amnc-nmca/cnamnc-cnnmca/tallurutiup-imanga', 'Parks Canada, Tallurutiup Imanga National Marine Conservation Area')
TIG = ('https://www.canada.ca/en/parks-canada/news/2018/07/parks-canada-announces-funding-to-qikiqtani-inuit-association-for-pilot-guardian-program-in-arctic-bay.html', 'Parks Canada, funding for a pilot Guardian program in Arctic Bay (July 18, 2018)')
PAME = ('https://pame.is', 'PAME (Protection of the Arctic Marine Environment), home page')
PAML = 'https://pame.is/ourwork/arctic-marine-litter/plastic-in-a-bottle/'
CAFF = ('https://www.caff.is', 'CAFF (Conservation of Arctic Flora and Fauna), home page')
MOS = ('https://mosaic-expedition.org', 'MOSAiC Expedition, home page')
MOSE = ('https://mosaic-expedition.org/expedition/', 'MOSAiC Expedition, The expedition')
WWFA = ('https://www.arcticwwf.org/about/about-us/', 'WWF Arctic Programme, About us')
WWFL = ('https://www.arcticwwf.org/our-priorities/last-ice-area/', 'WWF Arctic Programme, The Last Ice Area')
ICC = ('https://www.inuitcircumpolar.com', 'Inuit Circumpolar Council, home page')
ICCD = ('https://www.inuitcircumpolar.com/donate/', 'Inuit Circumpolar Council, Donate (I.C.C. Foundation)')
ABC = ('https://arcticbasecamp.org', 'Arctic Basecamp, home page')
ABJ = 'https://arcticbasecamp.org/join-us/'
ABJS = (ABJ, 'Arctic Basecamp, Join Us')
GOU = ('https://www.goughisland.com', 'Gough Island Restoration Programme (RSPB), home page update')
GOUG = ('https://www.goughisland.com/get-in-touch', 'Gough Island Restoration Programme, Help restore Gough')
PWZ = ('https://www.zooniverse.org/projects/penguintom79/penguin-watch', 'Zooniverse, Penguin Watch (project statistics)')
IAC = ('https://www.iaato.org/supporting-science/citizen-science', 'IAATO, Citizen Science')
OCE = ('https://oceanites.org', 'Oceanites, home page')
OCEG = ('https://www.oceanites.org/get-involved', 'Oceanites, Get Involved')
OCED = 'https://www.oceanites.org/donate'
SOC = ('https://soccom.princeton.edu', 'SOCCOM, home page')
GOB = ('https://www.go-bgc.org/outreach/adopt-a-float', 'GO-BGC, Adopt-A-Float')
SOCA = 'https://soccom.princeton.edu/broader-impacts/adopt-float-program'
SOOS = ('https://soos.aq', 'Southern Ocean Observing System (SOOS), home page')
SOOG = ('https://soos.aq/community/get-involved', 'SOOS, Get Involved')
SOOM = 'https://soos.aq/data/soosmap'
EPI = ('https://www.beyondepica.eu', 'Beyond EPICA – Oldest Ice, home page')
EPIP = 'https://www.beyondepica.eu/en/news-events/press-releases/'
ASOC = ('https://www.asoc.org', 'ASOC (Antarctic and Southern Ocean Coalition), home page')
ASOT = ('https://www.asoc.org/take-action/', 'ASOC, Take Action')
ASOD = 'https://www.asoc.org/give-now/'
CCA = ('https://www.ccamlr.org', 'CCAMLR, home page')
CCAS = 'https://spatial.ccamlr.org/'
CCAO = 'https://ccamlr.org/en/category/ccamlr-scheme-international-scientific-observation-siso'
SCAR = ('https://www.scar.org', 'SCAR (Scientific Committee on Antarctic Research), home page')
SCARD = ('https://scar.org/donate', 'SCAR, Donate (UK charity no. 1124840)')
SCARO = 'https://scar.org/about-us/administration/opportunities'
IAA = ('https://www.iaato.org', 'IAATO, home page')
PBCAM = 'https://polarbearsinternational.org/education/live/polar-bear-cams/'
PCV = 'https://parks.canada.ca/agence-agency/benevolat-volunteering'
CAFFD = 'https://www.caff.is/work/projects/arctic-biodiversity-data-service/'
CAFFB = 'https://www.caff.is/work/projects/arctic-migratory-birds-initiative/'
WWFY = 'https://www.arcticwwf.org/our-priorities/arctic-youth/'
IAAM = 'https://www.iaato.org/about-us/member-directory'

NORTH = [
 P(slug='Polar_Bears_International', title='Polar Bears International', short='Polar Bears International', cls='nonprofit',
  label='Nonprofit solution · active', org='Polar Bears International',
  img=('PBI_Arctic_Melt_Ponds_IceBridge.jpg', 985, 1260, 'Aquamarine melt ponds on Arctic sea ice seen from a NASA Operation IceBridge flight'),
  credit='NASA/Operation IceBridge (GSFC_20171208_Archive_e000266, Arctic sea ice melt ponds, public domain)',
  hook='The one group devoted only to polar bears and the sea ice they need.',
  wow=('Polar Bears International says it is the only organization dedicated solely to protecting the future of polar bears and the sea ice they depend on (Polar Bears International).', PBI),
  lead='Polar Bears International works through research, policy and on-the-ground conservation to protect polar bears and their sea-ice habitat (Polar Bears International).',
  eli=['Polar bears hunt seals from floating sea ice.', 'As the Arctic warms, the ice season gets shorter.', 'This group studies the bears and helps people and bears live safely side by side.'],
  ws=[('Who', 'Polar Bears International, a nonprofit dedicated to polar bears and sea ice.', PBI),
      ('What', 'Research, policy work and human-polar bear coexistence projects with partners.', PBI),
      ('When', 'Ongoing; Polar Bear Week runs November 1 to 7 each year.', PBI),
      ('Where', 'Across the Arctic, where polar bears live.', PBI),
      ('Why', 'To protect polar bears and the sea ice they depend on.', PBI)],
  impact=('Its donate page says gifts support research, policy and on-the-ground conservation, and help motivate people to care (Polar Bears International).', (PBID, 'Polar Bears International, Donate')),
  fact=('Waste and Bears', 'Trash is one of the biggest issues for people and bears living together, and it is especially hard to manage in the frozen north (Polar Bears International).', PBI),
  people=('Its coexistence work aims at a safer future for both polar bears and the people who live near them (Polar Bears International).', PBI),
  nature=('Protecting sea ice protects the platform polar bears use to hunt seals (Polar Bears International).', PBI),
  support_h='Support Polar Bears International',
  btns=[('Donate to Polar Bears International', PBID), ('Watch the live Polar Bear Cams', PBCAM)],
  bottom=('Polar Bears International accepts donations for its polar bear work.', PBID, 'Donate'),
  help=[('Watch the live Polar Bear Cams', PBCAM, 'see the bears and share what you learn'),
        ('Join Polar Bear Week (Nov 1-7)', 'https://polarbearsinternational.org/news-media/events/polar-bear-week/', 'webcasts, live cams and events'),
        ('Start a fundraiser', 'https://polarbearsinternational.org/donate/start-a-fundraiser/', 'run your own event for the bears'),
        ('Tune into free webcasts', 'https://polarbearsinternational.org/news-media/events/', 'talks with scientists, open to classrooms')],
  dnote=DN_YES.format(r='Polar Bears International is a Four-Star charity on Charity Navigator, with audited financial statements.'),
  see=[('Arctic_Weather_Satellite.html', 'Arctic Weather Satellite', 'Better forecasts over the Arctic.')],
  pin=pin(58.77, -94.17, 'Churchill, Manitoba, Canada (polar bear area; approximate)')),
 P(slug='SmartICE', title='SmartICE: Sea-Ice Safety for Northern Communities', short='SmartICE', cls='nonprofit',
  label='Social enterprise · active', org='SmartICE',
  img=('Hudson_Bay_Ice_Skylab.jpg', 1920, 1912, "Ice formations in Canada's Hudson Bay photographed from the Skylab space station"),
  credit='NASA (SL4-141-4316, Hudson Bay from Skylab 4, Jan. 20, 1974, public domain)',
  hook='Inuit knowledge plus sensors tell travellers how thick the ice really is.',
  wow=('SmartICE has trained 548 operators and monitored about 54,592 km of ice routes since 2018 (SmartICE).', SMI),
  lead='SmartICE combines Indigenous and local knowledge of ice with sensors and satellite mapping to give near real-time ice-thickness information for safe travel (SmartICE).',
  eli=['In the far north, people travel on frozen sea ice.', 'Warmer weather makes the ice harder to trust.', 'SmartICE measures the ice and makes maps so people know where it is safe.'],
  ws=[('Who', 'SmartICE, with local community members hired and trained to run its technology.', SMI),
      ('What', 'SmartQAMUTIK sleds and SmartBUOYs that measure ice thickness, plus weekly ice travel safety maps.', SMI),
      ('When', 'Operators trained since 2018; 231 weekly maps produced since 2022.', SMI),
      ('Where', 'Over 40 communities across Inuit Nunangat, the Northwest Territories, Yukon, Nunavik and Northern BC.', SMI),
      ('Why', 'For ice travel safety and climate change adaptation.', SMI)],
  impact=('More than 1,000 SmartQAMUTIK runs have measured ice along the most-travelled routes, chosen by Community Management Committees (SmartICE).', SMI),
  fact=('959 Ice Words', 'Elders and youth have documented 959 Inuktitut ice terms since 2019 (SmartICE).', SMI),
  people=('More than 100 local youth have been employed, with over 45,400 employment hours (SmartICE).', SMI),
  nature=('Its maps record how sea ice is changing, community by community (SmartICE).', SMI),
  support_h='Learn More About SmartICE', btns=[('Visit SmartICE', SMI[0])],
  bottom=('Want to go deeper? SmartICE explains its tools and its communities.', SMI[0], 'For Further Information'),
  help=[('Learn about SmartICE', SMI[0], 'watch its Impact in Action video series and share it')],
  dnote=DN_NO.format(r='we could not verify a donate page or a charity rating for SmartICE.'),
  see=[('Polar_Bears_International.html', 'Polar Bears International', 'People and polar bears living side by side.')],
  pin=pin(56.54, -61.69, 'Nain, Nunatsiavut, Canada (a SmartICE community)')),
 P(slug='Permafrost_Pathways', title='Permafrost Pathways', short='Permafrost Pathways', cls='nonprofit',
  label='Nonprofit solution · launched 2022', org='Permafrost Pathways',
  img=('Alaska_ABoVE_Flight.jpg', 1920, 1280, 'Alaskan landscape of rivers and lakes seen from a NASA research aircraft'),
  credit='NASA/Peter Griffith (GSFC_20171208_Archive_e000002, ABoVE flight over Alaska, public domain)',
  hook='When frozen ground thaws, villages sink and carbon escapes. This team works on both.',
  wow=('Permafrost thaw could release 30 to more than 150 billion tons of carbon by 2100 (Permafrost Pathways).', PPW),
  lead='Permafrost Pathways connects science, people and policy to address Arctic permafrost thaw and support affected communities (Permafrost Pathways).',
  eli=['Permafrost is ground that stays frozen all year.', 'As the Arctic warms, it thaws, the land sinks and gases escape.', 'This team measures the thaw and helps towns plan what to do.'],
  ws=[('Who', 'Woodwell Climate Research Center, the Arctic Initiative at Harvard Kennedy School and the Alaska Institute for Justice.', PPA),
      ('What', 'Adaptation and mitigation strategies for permafrost thaw, from monitoring to policy.', PPA),
      ('When', 'Launched in 2022 with funding through the TED Audacious Project.', PPA),
      ('Where', 'The Arctic, including Alaska Native communities.', PPW),
      ('Why', 'The Arctic is warming about three times faster than the global rate, and thaw emissions are largely left out of global carbon budgets.', PPW)],
  impact=('Upper estimates of thaw emissions are on par with the cumulative emissions of the entire United States at its current rate (Permafrost Pathways).', PPW),
  fact=('Three Times Faster', 'The Arctic is warming at three times the global rate (Permafrost Pathways).', PPW),
  people=('Thaw is collapsing land under homes and villages, an environmental justice crisis for Arctic residents (Permafrost Pathways).', PPW),
  nature=('Better monitoring keeps permafrost carbon in the picture for climate decisions (Permafrost Pathways).', PPW),
  support_h='Support Permafrost Pathways', btns=[('Donate to Permafrost Pathways', PPD)],
  bottom=('Permafrost Pathways accepts donations through Woodwell Climate Research Center.', PPD, 'Donate'),
  help=[('Learn and share', PPA[0], 'read how thaw affects Arctic communities and share it')],
  dnote=DN_YES.format(r='Woodwell Climate Research Center, which runs the fund, is a Four-Star charity on Charity Navigator, with audited financial statements.'),
  see=[('Carbfix.html', 'Carbfix', 'Turning carbon dioxide into stone.')],
  pin=pin(64.84, -147.72, 'Interior Alaska, United States (approximate)')),
 P(slug='Tallurutiup_Imanga_NMCA', title='Tallurutiup Imanga National Marine Conservation Area', short='Tallurutiup Imanga', cls='government',
  label='Government solution · Inuit co-managed', org='Parks Canada and the Qikiqtani Inuit Association',
  img=('Nunavut_ASTER.jpg', 1920, 1948, 'Satellite view of land and sea ice in Nunavut, northern Canada'),
  credit='NASA/GSFC/METI/ERSDAC/JAROS and U.S./Japan ASTER Science Team (PIA13963, Nunavut, public domain)',
  hook='Narwhals, seabirds and Inuit harvesting rights, protected together.',
  wow=("At about 108,000 square kilometres, Tallurutiup Imanga covers about 1.9% of Canada's goal of protecting 10% of its marine and coastal areas (Parks Canada).", TIM),
  lead='Tallurutiup Imanga, in Nunavut, protects Arctic waters where narwhals live alongside thousands of seabirds, next to Inuit communities (Parks Canada).',
  eli=['Tallurutiup Imanga is a huge stretch of Arctic sea in Canada.', 'Narwhals and many seabirds live there.', 'Inuit and the Government of Canada protect it together.'],
  ws=[('Who', 'The Government of Canada (Parks Canada) and the Qikiqtani Inuit Association.', TIM),
      ('What', 'A National Marine Conservation Area guided by Inuit traditional knowledge (Inuit Qaujimajatuqangit).', TIM),
      ('When', 'An Inuit Impact and Benefit Agreement was signed in 2019.', TIM),
      ('Where', 'Tallurutiup Imanga, Nunavut, Canada.', TIM),
      ('Why', 'It is rich in biodiversity and has been used by Inuit since time immemorial.', TIM)],
  impact=('The area protects Inuit harvesting rights under the Nunavut Land Claims Agreement while protecting species at risk (Parks Canada).', TIM),
  fact=('108,000 km²', 'Tallurutiup Imanga covers approximately 108,000 square kilometres (Parks Canada).', TIM),
  people=('Parks Canada funded a pilot Inuit Guardian program in Arctic Bay in 2018 (Parks Canada).', TIG),
  nature=('Narwhals live side by side with thousands of seabirds near fjords and glaciers (Parks Canada).', TIM),
  support_h='Learn More About Tallurutiup Imanga', btns=[('Parks Canada: Tallurutiup Imanga', TIM[0])],
  bottom=('Want to go deeper? Parks Canada explains the conservation area.', TIM[0], 'For Further Information'),
  help=[('Volunteer with Parks Canada', PCV, 'research, school programs and marine studies across Canada'),
        ('Learn about the Guardian program', TIG[0], 'how Inuit Guardians help watch over the area')],
  dnote=DN_NO.format(r='this is a government protected area, so there is no donation route.'),
  see=[('Ross_Sea_MPA.html', 'Ross Sea Region Marine Protected Area', 'A huge protected area off Antarctica.')],
  pin=pin(74.3, -84.0, 'Tallurutiup Imanga (Lancaster Sound), Nunavut, Canada (approximate)')),
 P(slug='PAME_Arctic_Council', title='PAME: Protecting the Arctic Marine Environment', short='PAME', cls='government',
  label='Intergovernmental solution · Arctic Council working group', org='PAME',
  img=('Western_Alaska_Sea_Ice_MODIS.jpg', 1920, 1500, "Sea ice off western Alaska seen by NASA's Aqua satellite"),
  credit='NASA/GSFC/Jeff Schmaltz, MODIS Land Rapid Response Team (GSFC_20171208_Archive_e000769, Feb. 4, 2014, public domain)',
  hook='Tracking ships and plastic so the Arctic Ocean stays clean.',
  wow=('Between 2013 and 2025, unique ships in the Arctic Polar Code area rose 40% and distance sailed nearly doubled, from 6.1 to 11.9 million nautical miles (PAME).', PAME),
  lead='PAME is the Arctic Council working group for the protection and sustainable use of the Arctic marine environment (PAME).',
  eli=['More ships now sail in the Arctic.', 'Ships and plastic can harm Arctic seas.', 'PAME tracks them and writes plans to keep the ocean healthy.'],
  ws=[('Who', 'PAME, a working group of the Arctic Council.', PAME),
      ('What', 'Plans, assessments and guidelines on Arctic shipping, marine litter and marine protected areas.', PAME),
      ('When', 'Ongoing; its symposium on marine plastic pollution was held 20 to 22 October 2026 in Reykjavík.', PAME),
      ('Where', 'The Arctic marine and coastal environment.', PAME),
      ('Why', 'To prevent pollution and manage marine activities as the Arctic changes.', PAME)],
  impact=('Its Plastic in a Bottle GPS capsules drift with ocean currents to show how marine litter travels in and out of Arctic waters (PAME).', PAME),
  fact=('649 Days Adrift', 'The longest Plastic in a Bottle journey so far has lasted 649 days (PAME).', PAME),
  people=('Its shipping work covers the safety and sustainability of marine activities that Arctic communities rely on (PAME).', PAME),
  nature=('Its marine litter work helps keep plastic out of Arctic waters (PAME).', PAME),
  support_h='Learn More About PAME', btns=[('PAME: Our work', PAME[0])],
  bottom=('Want to go deeper? PAME publishes its Arctic shipping and litter work.', PAME[0], 'For Further Information'),
  help=[('Follow Plastic in a Bottle', PAML, 'track the drifting capsules on the live map with your class'),
        ('Explore Arctic ship traffic data', PAME[0], 'see how shipping has changed since 2013')],
  dnote=DN_NO.format(r='PAME is an intergovernmental working group and does not take donations.'),
  see=[('CAFF_Arctic_Biodiversity.html', 'CAFF', "The Arctic Council's biodiversity working group.")],
  pin=pin(65.68, -18.09, 'Akureyri, Iceland (approximate)')),
 P(slug='CAFF_Arctic_Biodiversity', title='CAFF: Conservation of Arctic Flora and Fauna', short='CAFF', cls='government',
  label='Intergovernmental solution · Arctic Council working group', org='CAFF',
  img=('SW_Greenland_Fjord_IceBridge.jpg', 1024, 685, 'Mountains and an open-water fjord in southwest Greenland seen from a NASA IceBridge flight'),
  credit='NASA/GSFC/Michael Studinger (GSFC_20171208_Archive_e001911, April 8, 2011, public domain)',
  hook='Watching Arctic wildlife so changes are caught early.',
  wow=('CAFF runs the Circumpolar Biodiversity Monitoring Program across the Arctic (CAFF).', CAFF),
  lead='CAFF is the biodiversity working group of the Arctic Council (CAFF).',
  eli=['Many animals and plants live only in the Arctic.', 'Scientists from Arctic countries watch how they are doing.', 'CAFF collects that information and shares it.'],
  ws=[('Who', "CAFF, the Arctic Council's biodiversity working group.", CAFF),
      ('What', 'The Circumpolar Biodiversity Monitoring Program, the Arctic Migratory Birds Initiative and the Arctic Biodiversity Data Service.', CAFF),
      ('When', 'Ongoing, under a 2025-2027 work plan.', CAFF),
      ('Where', 'The circumpolar Arctic.', CAFF),
      ('Why', 'To understand climate change impacts on Arctic ecosystems and safeguard important areas.', CAFF)],
  impact=('With AMAP, CAFF announced a special issue on accelerating climate change impacts on Arctic ecosystems (CAFF).', CAFF),
  fact=('Arctic Migratory Birds', 'CAFF runs an Arctic Migratory Birds Initiative (CAFF).', CAFF),
  people=('CAFF lists improving knowledge and public awareness among its topics (CAFF).', CAFF),
  nature=('Its Arctic Biodiversity Data Service shares Arctic biodiversity data (CAFF).', CAFF),
  support_h='Learn More About CAFF', btns=[('CAFF: Arctic Biodiversity Data Service', CAFFD)],
  bottom=('Want to go deeper? CAFF shares its monitoring work.', CAFF[0], 'For Further Information'),
  help=[('Explore the Arctic Biodiversity Data Service', CAFFD, 'use Arctic data in a class project'),
        ('Learn about Arctic migratory birds', CAFFB, 'and share what you find')],
  dnote=DN_NO.format(r='CAFF is an intergovernmental working group and does not take donations.'),
  see=[('PAME_Arctic_Council.html', 'PAME', "The Arctic Council's marine working group.")],
  pin=pin(65.7, -18.1, 'Akureyri, Iceland (approximate)')),
 P(slug='MOSAiC_Expedition', title='MOSAiC Expedition: A Year Frozen in the Arctic Ice', short='MOSAiC', cls='agency',
  label='Research solution · expedition 2019-2020', org='the MOSAiC expedition',
  img=('Healy_Ice_Station_ICESCAPE.jpg', 1920, 1280, 'A research icebreaker parked in an Arctic ice floe'),
  credit='NASA/Kathryn Hansen (GSFC_20171208_Archive_e001722, ICESCAPE mission, Chukchi Sea, 2011, public domain; not the MOSAiC ship)',
  hook='A ship let itself freeze into the sea ice for a whole year to study the Arctic.',
  wow=('From September 2019 to October 2020, the icebreaker Polarstern drifted with the sea ice across the central Arctic (MOSAiC).', MOSE),
  lead='MOSAiC was the first year-round expedition into the central Arctic to study its climate system (MOSAiC).',
  eli=['Scientists let their ship get stuck in the Arctic ice on purpose.', 'It drifted with the ice for a full year, even in the dark winter.', 'They measured the air, ice and ocean to understand climate change.'],
  ws=[('Who', 'An international consortium led by the Alfred Wegener Institute (AWI); hundreds of researchers from 20 countries.', MOS),
      ('What', 'A drifting observatory on the research icebreaker Polarstern.', MOSE),
      ('When', 'September 2019 to October 2020.', MOSE),
      ('Where', 'The central Arctic Ocean, close to the North Pole.', MOS),
      ('Why', 'To take the closest look ever at the Arctic as the epicentre of global warming.', MOS)],
  impact=('Its data will be used by scientists around the globe to take climate research to a new level (MOSAiC).', MOS),
  fact=('More Than €140 Million', 'MOSAiC had a total budget exceeding €140 million (MOSAiC).', MOSE),
  people=('Its goal was insights key to better understanding global climate change, which affects everyone (MOSAiC).', MOS),
  nature=('It brought a research icebreaker close to the North Pole for the first time in polar winter (MOSAiC).', MOS),
  support_h='Learn More About MOSAiC', btns=[('MOSAiC: The expedition', MOSE[0])],
  bottom=('Want to go deeper? Explore the expedition and its science.', MOS[0], 'For Further Information'),
  help=[('Explore the expedition', MOSE[0], 'videos and stories from a year in the ice, good for classrooms')],
  dnote=DN_NO.format(r='MOSAiC was a completed research expedition and does not take donations.'),
  see=[('ICESat-2.html', 'ICESat-2', 'Measuring polar ice from space.')],
  pin=pin(88.0, 30.0, 'Central Arctic Ocean (approximate drift area)')),
 P(slug='WWF_Arctic_Programme', title='WWF Arctic Programme', short='the WWF Arctic Programme', cls='nonprofit',
  label='Nonprofit solution · active since 1992', org='the WWF Arctic Programme',
  img=('Wolstenholme_Fjord_IceBridge.jpg', 1920, 1272, 'Saunders Island and sea ice in Wolstenholme Fjord, Greenland, seen from a NASA IceBridge flight'),
  credit='NASA/Michael Studinger (GSFC_20171208_Archive_e001514, April 2013, public domain)',
  hook='Guarding the Last Ice Area, where summer sea ice should survive longest.',
  wow=("WWF's Arctic Programme works to see 30% of the Arctic Ocean designated as protected and conserved areas by 2030 (WWF Arctic).", WWFA),
  lead="Since 1992, WWF's Global Arctic Programme has worked for a well-managed, biodiverse and resilient Arctic (WWF Arctic).",
  eli=['Arctic sea ice is shrinking.', 'One area, above Canada and Greenland, should keep its ice the longest.', 'WWF works to protect that area for the animals that need ice.'],
  ws=[('Who', "WWF's Global Arctic Programme.", WWFA),
      ('What', 'Protected areas, species protection, good governance and work with Arctic communities and youth.', WWFA),
      ('When', 'Since 1992.', WWFA),
      ('Where', 'The Arctic, including the Last Ice Area above Canada and Greenland.', WWFL),
      ('Why', 'Summer sea ice will last longest in the Last Ice Area, a refuge for ice-dependent species such as polar bears.', WWFL)],
  impact=('Its vision is healthy wildlife populations that also benefit the well-being of people in the Arctic and beyond (WWF Arctic).', WWFA),
  fact=('The Last Ice Area', 'Projections show summer sea ice will last longest above Canada and Greenland (WWF Arctic).', WWFL),
  people=('Its species work focuses on animals immensely important for Arctic communities (WWF Arctic).', WWFA),
  nature=('It works to keep a last refuge for ice-dependent species as the world warms (WWF Arctic).', WWFL),
  support_h='Learn More About the WWF Arctic Programme', btns=[('WWF Arctic: About us', WWFA[0])],
  bottom=('Want to go deeper? WWF explains its Arctic priorities.', WWFA[0], 'For Further Information'),
  help=[('Learn about the Last Ice Area', WWFL[0], 'and share why it matters'),
        ('Arctic youth', WWFY, 'read what young Arctic people are asking for')],
  dnote=DN_NO.format(r="the Arctic Programme's Donate link goes to WWF International, and the charity rating we found covers WWF-US, a different office."),
  see=[('Polar_Bears_International.html', 'Polar Bears International', 'Protecting polar bears and sea ice.')],
  pin=pin(80.0, -70.0, 'Last Ice Area, between northern Canada and Greenland (approximate)')),
 P(slug='Inuit_Circumpolar_Council', title='Inuit Circumpolar Council', short='the Inuit Circumpolar Council', cls='nonprofit',
  label="Indigenous Peoples' organization · since 1977", org='the Inuit Circumpolar Council',
  img=('Cape_Farewell_Greenland_ISS.jpg', 1920, 1311, 'Cape Farewell (Nunap Isua), the southern tip of Greenland, photographed from the International Space Station'),
  credit='NASA (ISS017-E-012583, Cape Farewell, Greenland, Aug. 4, 2008, public domain)',
  hook='About 180,000 Inuit, one voice for the Arctic.',
  wow=('The Inuit Circumpolar Council represents about 180,000 Inuit across Alaska, Canada, Greenland (Kalaallit Nunaat) and Chukotka (ICC).', ICC),
  lead='Founded in 1977, the Inuit Circumpolar Council brings Inuit rights and priorities to the international level (ICC).',
  eli=['Inuit have lived in the Arctic for thousands of years.', 'They live in several countries but share one culture.', 'This council speaks for them at world meetings about nature and climate.'],
  ws=[('Who', "The Inuit Circumpolar Council (ICC), an Indigenous Peoples' Organization.", ICC),
      ('What', 'International advocacy for Inuit rights, including at the biodiversity summit CBD COP17.', ICC),
      ('When', 'Since 1977; its 15th General Assembly met in Iqaluit in 2026.', ICC),
      ('Where', 'Alaska, Canada, Greenland and Chukotka.', ICC),
      ('Why', 'To advance Inuit rights and priorities internationally.', ICC)],
  impact=("In October 2026 it published a position paper on Indigenous Peoples' rights at CBD COP17 (ICC).", ICC),
  fact=('Founded 1977', 'The Inuit Circumpolar Council was founded in 1977 (ICC).', ICC),
  people=('Its work covers Arctic policy, climate action, Inuit Knowledge, and health and wellness programming (ICC).', ICC),
  nature=('Its foundation promotes the management of Arctic and sub-Arctic wildlife and environment (ICC).', ICCD),
  support_h='Learn More About the ICC', btns=[('Inuit Circumpolar Council', ICC[0])],
  bottom=("Want to go deeper? Read the ICC's latest statements.", ICC[0], 'For Further Information'),
  help=[('Read and share ICC statements', ICC[0], 'learn Inuit views on Arctic nature and climate')],
  dnote=DN_NO.format(r='we could not verify audited finances or a charity rating for the I.C.C. Foundation, so we list learning options only.'),
  see=[('SmartICE.html', 'SmartICE', 'Inuit knowledge and sensors for safe ice travel.')],
  pin=pin(63.75, -68.52, 'Iqaluit, Nunavut, Canada (2026 ICC General Assembly)')),
 P(slug='Arctic_Basecamp', title='Arctic Basecamp', short='Arctic Basecamp', cls='nonprofit',
  label='Nonprofit solution · science communication', org='Arctic Basecamp',
  img=('Arctic_Sea_Ice_Minimum_2015.jpg', 1920, 1080, 'Visualization of Arctic sea ice near its 2015 summer minimum'),
  credit='NASA Scientific Visualization Studio (GSFC_20171208_Archive_e000613, 2015, public domain)',
  hook="Polar scientists bringing the Arctic's warning to world leaders.",
  wow=('Founded by Professor Gail Whiteman, Arctic Basecamp aims to "speak science to power" about polar climate risks (Arctic Basecamp).', ABC),
  lead='Arctic Basecamp is a registered not-for-profit that spotlights the global threats of polar climate change and communicates areas of action (Arctic Basecamp).',
  eli=['What happens in the Arctic affects weather everywhere.', 'Scientists meet world leaders where they gather.', 'They explain the risks so leaders act.'],
  ws=[('Who', 'Arctic Basecamp, founded by Professor Gail Whiteman.', ABC),
      ('What', 'Science communication and direct engagement with leaders in business, policy and civil society.', ABC),
      ('When', "Including events inside the World Economic Forum's official program from 2020 to 2024.", ABC),
      ('Where', 'Davos and online through its Global Climate Risk Platform.', ABC),
      ('Why', 'Arctic warming drives extreme weather, food insecurity and health risks worldwide.', ABJS)],
  impact=('It built a "Climate Risks Daily" tool that summarizes credible climate news from 100 languages (Arctic Basecamp).', ABC),
  fact=('Science to Power', 'Its mission is to "speak science to power" (Arctic Basecamp).', ABC),
  people=('It invites people to become youth ambassadors or climate reporters (Arctic Basecamp).', ABJS),
  nature=('It aims to inspire bold climate action on the threats posed by polar climate change (Arctic Basecamp).', ABC),
  support_h='Learn More About Arctic Basecamp', btns=[('Arctic Basecamp: Join Us', ABJ)],
  bottom=('Want to go deeper? See how Arctic Basecamp works.', ABC[0], 'For Further Information'),
  help=[('Become a youth ambassador or climate reporter', ABJ, 'listed on its Join Us page'),
        ('Share your climate story', ABJ, 'and spread the word')],
  dnote=DN_NO.format(r='its Donate button goes to a third-party fundraising site, and we could not verify audited finances or a charity rating.'),
  see=[('Permafrost_Pathways.html', 'Permafrost Pathways', 'Science and policy for thawing ground.')],
  pin=pin(46.80, 9.84, 'Davos, Switzerland (Arctic Basecamp events)')),
]

SOUTH = [
 P(slug='Gough_Island_Restoration', title='Gough Island Restoration Programme', short='the Gough Island Restoration', cls='nonprofit',
  label='Nonprofit solution · 2021 attempt, mice remain', org='the Gough Island Restoration Programme',
  img=('Tristan_da_Cunha_ASTER.jpg', 1459, 1049, 'Satellite view of Tristan da Cunha, the main island of the group that includes Gough Island'),
  credit='NASA/METI/AIST/Japan Space Systems and U.S./Japan ASTER Science Team (PIA22506, Tristan da Cunha, public domain; not Gough itself)',
  hook='An honest story: a huge effort to save seabirds from mice, and lessons for next time.',
  wow=("Over 99% of the world's Atlantic petrels breed on Gough Island, where mice took eggs and chicks (Gough Island Restoration Programme).", GOUG),
  lead='The RSPB-led Gough Island Restoration Programme tried in 2021 to remove the invasive mice that prey on seabirds; mice were found again, so the eradication did not fully succeed (RSPB).',
  eli=['Gough Island in the South Atlantic is home to rare seabirds.', 'Mice brought by people eat the chicks.', 'A team tried to remove every mouse; a few survived, and they are learning how to try again.'],
  ws=[('Who', 'The RSPB and partners.', GOU),
      ('What', 'An attempt to remove every invasive mouse from Gough Island.', GOU),
      ('When', 'The attempt was in 2021; a mouse was seen on camera again in December 2021.', GOU),
      ('Where', 'Gough Island, in the Tristan da Cunha group, South Atlantic.', GOUG),
      ('Why', 'Gough is home to four seabird species found only in the Tristan da Cunha group and two endemic land birds.', GOUG)],
  impact=('Atlantic petrel breeding success, as low as 12% before, was believed to be around 63% in the first season after the attempt (Gough Island Restoration Programme).', GOUG),
  fact=('About 5,000 Albatrosses', 'There are only around 5,000 mature Tristan albatrosses, and almost all breed on Gough (Gough Island Restoration Programme).', GOUG),
  people=('The RSPB says it will learn every lesson possible for the wider island restoration community (RSPB).', GOU),
  nature=('Even without full success, the attempt brought some respite from intense predation on the birds (RSPB).', GOU),
  support_h='Learn More About Gough Island', btns=[('Gough Island Restoration Programme', GOU[0])],
  bottom=("Want to go deeper? Read the programme's updates.", GOU[0], 'For Further Information'),
  help=[('Get in touch about supporting the programme', GOUG[0], 'contact details on its Help restore Gough page'),
        ('Listen to the Gough soundscape', GOUG[0], "a 10-minute recording of the island's birds to share in class")],
  dnote=DN_NO.format(r="the programme's own site has no donate page, only a contact for funding."),
  see=[('South_Georgia_Habitat_Restoration.html', 'South Georgia Habitat Restoration', "The world's largest island rodent eradication.")],
  pin=pin(-40.32, -9.94, 'Gough Island, South Atlantic')),
 P(slug='Penguin_Watch', title='Penguin Watch: Count Penguins from Home', short='Penguin Watch', cls='nonprofit',
  label='Citizen science · live', org='Penguin Watch',
  img=('Ross_Sea_Icebergs_MISR.jpg', 1476, 1681, "Large icebergs in the Ross Sea, Antarctica, seen by NASA's Terra satellite"),
  credit='NASA/GSFC/JPL, MISR Team (PIA02639, Ross Sea icebergs, Dec. 10, 2000, public domain)',
  hook='Click on photos, count penguins, help real science.',
  wow=('More than 102,000 volunteers have made over 859,000 classifications on Penguin Watch (Zooniverse).', PWZ),
  lead='On Penguin Watch, anyone online counts penguin adults, chicks and eggs in camera photos to help scientists understand their lives and environment (Zooniverse).',
  eli=['Cameras in Antarctica take pictures of penguins.', 'There are too many photos for scientists to check alone.', 'Volunteers like you count the penguins online.'],
  ws=[('Who', 'Volunteers on the Zooniverse citizen-science platform.', PWZ),
      ('What', 'Counting penguin adults, chicks and eggs in camera images.', PWZ),
      ('When', 'This project launched on Zooniverse in April 2018 and is live.', PWZ),
      ('Where', 'Online, with images from cameras placed throughout the Antarctic region.', IAC),
      ('Why', "Studying penguins tells scientists a lot about the health of Antarctica's ecosystem.", IAC)],
  impact=("Penguin Watch monitors penguins' annual breeding success and reproductive behaviours (IAATO).", IAC),
  fact=('About 100 Cameras', 'With 100 live cameras placed throughout the region, citizen scientists can help from anywhere (IAATO).', IAC),
  people=('Anyone can take part online, which makes it a classroom-friendly science project (Zooniverse).', PWZ),
  nature=('Breeding data help scientists track how penguin colonies are doing (IAATO).', IAC),
  support_h='Start Counting Penguins', btns=[('Count penguins on Penguin Watch', PWZ[0])],
  bottom=('Ready to help? Start counting penguins now.', PWZ[0], 'Take Part'),
  help=[('Count penguins on Penguin Watch', PWZ[0], 'free and online'),
        ('Use it in class', PWZ[0], 'students can classify images together')],
  dnote=DN_NO.format(r='Penguin Watch is a volunteer project, so the best way to help is to take part.'),
  see=[('Oceanites_Penguin_Census.html', 'Oceanites', 'Counting penguins on the ground for 30+ years.')],
  pin=pin(-64.8, -63.5, 'Antarctic Peninsula (camera region; approximate)')),
 P(slug='Oceanites_Penguin_Census', title='Oceanites: Antarctic Penguin Census', short='Oceanites', cls='nonprofit',
  label='Nonprofit solution · counting since 1994', org='Oceanites',
  img=('James_Ross_Island_AirSAR.jpg', 1920, 1268, "James Ross Island at the northern tip of the Antarctic Peninsula, seen from NASA's DC-8"),
  credit='NASA/Jim Ross (ED04-0056-137, AirSAR 2004, public domain)',
  hook='More than 3.5 million penguins counted by hand.',
  wow=('Oceanites counters have hand-counted 3,507,541 penguins (Oceanites).', OCE),
  lead='For more than 30 years, Oceanites has tracked penguin populations on the rapidly warming Antarctic Peninsula and shares the data openly (Oceanites).',
  eli=['Penguins show how healthy Antarctica is.', 'Oceanites counts them every season, on foot and with drones and satellites.', 'Anyone in the world can use the data.'],
  ws=[('Who', 'Oceanites, a nonprofit founded in the United States and supported primarily by individual donations.', OCE),
      ('What', 'Boots-on-the-ground penguin counts plus drone and satellite imagery, published as open data.', OCE),
      ('When', 'Since 1994.', OCE),
      ('Where', '250+ locations on the Antarctic Peninsula.', OCE),
      ('Why', 'Penguins are frontline sentinels of climate change and Antarctic ecosystem health.', OCE)],
  impact=('Oceanites counters have made 2,100+ site visits across 250+ Antarctic locations since 1994 (Oceanites).', OCE),
  fact=('6.1 Million Pairs', 'Its 2024 SOAP report recorded 6,102,358 breeding pairs among the two penguin species analysed (Oceanites).', OCE),
  people=('Its data are available to scientists, policymakers and the public worldwide (Oceanites).', OCE),
  nature=('Its evidence helps decision-makers safeguard the Antarctic ecosystem (Oceanites).', OCE),
  support_h='Support Oceanites', btns=[('Donate to Oceanites', OCED), ('Get involved', OCEG[0])],
  bottom=('Oceanites accepts donations for its penguin research.', OCED, 'Donate'),
  help=[('Adopt a penguin colony', OCEG[0], 'for individuals, families and classrooms; funds field gear and travel'),
        ('Explore open penguin data', OCE[0], 'use its SOAP report and MAPPPD in class')],
  dnote=DN_YES.format(r='Oceanites is a Four-Star charity on Charity Navigator.'),
  see=[('Penguin_Watch.html', 'Penguin Watch', 'Count penguins online.')],
  pin=pin(-64.1, -57.8, 'James Ross Island area, Antarctic Peninsula (approximate)')),
 P(slug='SOCCOM', title='SOCCOM: Robot Floats in the Southern Ocean', short='SOCCOM', cls='agency',
  label='Research solution · NSF-funded', org='SOCCOM',
  img=('Southern_Ocean_Eddies_VIIRS.jpg', 1920, 2683, 'Swirling ocean-colour eddies in the Southern Ocean west of the Drake Passage'),
  credit='NASA OceanColor/Suomi NPP/VIIRS (GSFC_20171208_Archive_e000750, Jan. 1, 2015, public domain)',
  hook='Robot floats measure how the Southern Ocean shapes our climate, and schools can name them.',
  wow=('The Adopt-A-Float program grew from one classroom in 2015 to more than 50 schools, and adopting a float is free (GO-BGC).', GOB),
  lead='SOCCOM is a multi-institutional program focused on the Southern Ocean and its influence on climate, using floats and models (SOCCOM).',
  eli=['The Southern Ocean around Antarctica soaks up heat and carbon.', 'Robot floats dive up and down measuring the water.', 'Classes can adopt a float, name it and follow it.'],
  ws=[('Who', 'A multi-institutional team led by Professor Lynne Talley at UCSD/Scripps; founded at Princeton.', SOC),
      ('What', 'Biogeochemical floats, open float data and Earth system modelling.', SOC),
      ('When', 'Princeton ran it for its first 10 years; it continues, funded by the U.S. National Science Foundation.', SOC),
      ('Where', 'The Southern Ocean.', SOC),
      ('Why', "To determine the Southern Ocean's influence on climate.", SOC)],
  impact=('Its biogeochemical float data are open to access (SOCCOM).', SOC),
  fact=('Floats Named by Kids', 'Adopted floats have been named after explorers, scientists and school mascots (GO-BGC).', GOB),
  people=('Students connect directly with the scientists who deploy the floats (GO-BGC).', GOB),
  nature=("Knowing the Southern Ocean's role helps improve climate models (GO-BGC).", GOB),
  support_h='Learn More About SOCCOM', btns=[('SOCCOM Adopt-A-Float', SOCA)],
  bottom=('Want to go deeper? Explore the float map and data.', SOC[0], 'For Further Information'),
  help=[('Adopt a float with your class', SOCA, 'free; name it and track it'),
        ('Explore the interactive float map', SOC[0], 'follow real floats')],
  dnote=DN_NO.format(r='SOCCOM is a government-funded research program and does not take donations.'),
  see=[('SOOS.html', 'SOOS', 'Coordinating Southern Ocean observations.')],
  pin=pin(-55.0, -80.0, 'Southern Ocean (float deployment area; approximate)')),
 P(slug='SOOS', title='SOOS: Southern Ocean Observing System', short='SOOS', cls='agency',
  label='Research network · active', org='SOOS',
  img=('Southern_Ocean_Cyclone_MISR.jpg', 1276, 1731, "A large storm system over the Southern Ocean seen by NASA's Terra satellite"),
  credit='NASA/GSFC/LaRC/JPL, MISR Team (PIA03430, Oct. 11, 2001, public domain)',
  hook='Making sure every Southern Ocean measurement can be found and used.',
  wow=('SOOS aims to maximise the discoverability, access and impact of Southern Ocean observations, no matter who collected them (SOOS).', SOOS),
  lead='SOOS facilitates and enhances global Southern Ocean observations by coordinating fieldwork and sharing data (SOOS).',
  eli=['Many ships and scientists study the Southern Ocean.', 'SOOS helps them share plans and data.', 'Then fewer trips are wasted, and everyone learns more.'],
  ws=[('Who', 'The Southern Ocean Observing System, based at IMAS, University of Tasmania.', SOOS),
      ('What', 'Data tools like SOOSmap, the DueSouth expedition planner, and working groups.', SOOS),
      ('When', 'Ongoing.', SOOS),
      ('Where', 'The Southern Ocean around Antarctica.', SOOS),
      ('Why', 'Better data connections support better science.', SOOG)],
  impact=('SOOSmap lets anyone explore and download curated Southern Ocean data on an interactive map (SOOS).', SOOS),
  fact=('5 Science Challenges', 'The Southern Ocean community has identified 5 scientific challenges to focus observing priorities (SOOS).', SOOS),
  people=('Shared logistics and resources help researchers work together (SOOS).', SOOS),
  nature=('Coordinated observations show how the Southern Ocean is changing (SOOS).', SOOS),
  support_h='Learn More About SOOS', btns=[('SOOS: Get Involved', SOOG[0])],
  bottom=('Want to go deeper? Explore SOOSmap.', SOOM, 'For Further Information'),
  help=[('Explore SOOSmap', SOOM, 'real Southern Ocean data for student projects'),
        ('Join a working group', SOOG[0], 'for people working in Southern Ocean fields')],
  dnote=DN_NO.format(r='SOOS is a scientific network and does not take donations.'),
  see=[('SOCCOM.html', 'SOCCOM', 'Robot floats in the Southern Ocean.')],
  pin=pin(-42.88, 147.33, 'Hobart, Tasmania, Australia (SOOS office at IMAS)')),
 P(slug='Beyond_EPICA_Oldest_Ice', title='Beyond EPICA – Oldest Ice', short='Beyond EPICA', cls='agency',
  label='Research solution · European project', org='Beyond EPICA – Oldest Ice',
  img=('Larsen_C_Iceberg_Landsat.jpg', 1920, 1670, "Landsat view of a giant iceberg breaking away from Antarctica's Larsen C ice shelf"),
  credit='NASA Earth Observatory image by Joshua Stevens, Landsat data from USGS (GSFC_20171208_Archive_e000021, 2017, public domain)',
  hook="Ice 1.2 million years old holds a record of Earth's past climate.",
  wow=('Beyond EPICA has collected an Antarctic ice core reaching at least 1.2 million years back (Beyond EPICA).', EPI),
  lead='The European project Beyond EPICA – Oldest Ice drills Antarctic ice to read climate and environmental history (Beyond EPICA).',
  eli=['Snow in Antarctica piles up into ice over a very long time.', 'Tiny air bubbles in the ice hold old air.', 'Scientists drill it out to learn how climate changed long ago.'],
  ws=[('Who', "A European project led by the Institute of Polar Sciences of Italy's National Research Council (CNR-ISP).", EPI),
      ('What', 'Drilling and analysing a very old Antarctic ice core.', EPI),
      ('When', 'Analysis of trace gases, water isotopes and impurities was set for winter 2025/26.', EPI),
      ('Where', 'Antarctica.', EPI),
      ('Why', 'To understand the Mid-Pleistocene Transition, when ice-age cycles changed from 40,000 to 100,000 years.', EPI)],
  impact=('It extracted the most detailed archive of climate and environmental history from an Antarctic ice core spanning 1.2 million years (Beyond EPICA).', EPI),
  fact=('1.2 Million Years', 'The new core reaches at least 1.2 million years (Beyond EPICA).', EPI),
  people=("Its data are expected to be crucial for understanding a significant phase in Earth's climate development (Beyond EPICA).", EPI),
  nature=("The record should shed new light on the causes of Earth's changing glacial rhythm (Beyond EPICA).", EPI),
  support_h='Learn More About Beyond EPICA', btns=[('Beyond EPICA', EPI[0])],
  bottom=("Want to go deeper? Read the project's press releases.", EPIP, 'For Further Information'),
  help=[('Read the press releases', EPIP, 'share the discoveries with your class')],
  dnote=DN_NO.format(r='Beyond EPICA is supported by research institutions and funding agencies and does not take public donations.'),
  see=[('Thwaites_Glacier_Collaboration.html', 'Thwaites Glacier Collaboration', "Studying Antarctica's fast-changing glacier.")],
  pin=pin(-76.0, 122.0, 'East Antarctic Plateau (approximate)')),
 P(slug='ASOC_Antarctic_Coalition', title='ASOC: Antarctic and Southern Ocean Coalition', short='ASOC', cls='nonprofit',
  label='Nonprofit coalition · since 1978', org='ASOC',
  img=('Ross_Sea_Bloom_2011.jpg', 1920, 2059, 'A green phytoplankton bloom in the Ross Sea, Antarctica, seen from space'),
  credit='NASA (GSFC_20171208_Archive_e001951, Ross Sea bloom, Jan. 22, 2011, public domain)',
  hook='Working since 1978 for protected areas in the Southern Ocean.',
  wow=('The Southern Ocean covers around 10% of the global ocean and supports thousands of species found nowhere else on Earth (ASOC).', ASOC),
  lead='ASOC, a coalition of conservation groups, has advocated for stronger protection of Antarctica and the Southern Ocean since 1978 (ASOC).',
  eli=['The sea around Antarctica is full of life found nowhere else.', 'Climate change and fishing put it at risk.', 'ASOC asks governments to protect special areas.'],
  ws=[('Who', 'The Antarctic and Southern Ocean Coalition: staff, campaigners, coalition members and supporters.', ASOC),
      ('What', 'Campaigns for marine protected areas and on the climate crisis in Antarctica.', ASOC),
      ('When', 'Since 1978.', ASOC),
      ('Where', 'Antarctica and the Southern Ocean.', ASOC),
      ('Why', 'Antarctica is changing in ways that will impact all of humanity.', ASOT)],
  impact=("It supports the Domain 1 marine protected area to protect the Antarctic Peninsula's critical feeding and breeding grounds (ASOC).", ASOC),
  fact=('Since 1978', 'ASOC has been advocating for stronger Antarctic protections since 1978 (ASOC).', ASOC),
  people=('ASOC links protecting Antarctica to a climate-safe future for humanity (ASOC).', ASOC),
  nature=('Protected areas help Antarctic wildlife stay resilient in a changing climate (ASOC).', ASOC),
  support_h='Support ASOC', btns=[('Donate to ASOC', ASOD), ('Take action', ASOT[0])],
  bottom=('ASOC accepts donations for its Antarctic work.', ASOD, 'Donate'),
  help=[('Take action for Antarctica', ASOT[0], 'cut carbon, learn, talk to friends and family, eat penguin-friendly'),
        ('World Penguin Day art contest', ASOC[0], 'a creative way for students to join in')],
  dnote=DN_YES.format(r='ASOC is a Four-Star charity on Charity Navigator.'),
  see=[('Ross_Sea_MPA.html', 'Ross Sea Region Marine Protected Area', "The world's largest marine protected area.")],
  pin=pin(38.91, -77.04, 'Washington, DC, United States (ASOC office)')),
 P(slug='CCAMLR', title='CCAMLR: Conserving Antarctic Marine Life', short='CCAMLR', cls='government',
  label='Intergovernmental solution · since 1982', org='CCAMLR',
  img=('Amundsen_Sea_Iceberg_IceBridge.jpg', 1346, 894, "An iceberg in the Amundsen Sea, West Antarctica, seen from NASA's DC-8"),
  credit='NASA/Jane Peterson (200910220009HQ, Operation IceBridge, Oct. 21, 2009, public domain)',
  hook='The treaty body that manages fishing so krill, penguins and whales still have enough.',
  wow=('CCAMLR was set up by international convention in 1982 to conserve Antarctic marine life, in response to growing commercial interest in krill (CCAMLR).', CCA),
  lead='CCAMLR manages Antarctic marine life with an ecosystem-based approach, allowing only sustainable harvesting that accounts for effects on the ecosystem (CCAMLR).',
  eli=['Krill are tiny animals that whales, seals and penguins eat.', 'People also want to catch krill.', 'CCAMLR sets rules so there is enough left for nature.'],
  ws=[('Who', 'The Commission for the Conservation of Antarctic Marine Living Resources.', CCA),
      ('What', 'Conservation measures, fisheries management, scientific observers and ecosystem monitoring.', CCA),
      ('When', 'Since 1982; CCAMLR-45 met 18 to 30 October 2026.', CCA),
      ('Where', 'The Southern Ocean around Antarctica.', CCA),
      ('Why', 'Krill are a keystone of the Antarctic ecosystem, and several Southern Ocean resources had been over-exploited.', CCA)],
  impact=('Harvesting is allowed only if it is sustainable and accounts for the effects of fishing on other parts of the ecosystem (CCAMLR).', CCA),
  fact=('Keystone Krill', 'Antarctic krill are a keystone component of the Antarctic ecosystem (CCAMLR).', CCA),
  people=('Sustainable harvesting keeps fisheries possible in the long run (CCAMLR).', CCA),
  nature=('Its ecosystem monitoring program watches the health of Antarctic marine life (CCAMLR).', CCA),
  support_h='Learn More About CCAMLR', btns=[('CCAMLR Spatial Data Viewer', CCAS)],
  bottom=('Want to go deeper? CCAMLR explains its conservation measures.', CCA[0], 'For Further Information'),
  help=[('Explore the CCAMLR Spatial Data Viewer', CCAS, 'maps of Southern Ocean management areas'),
        ('Learn about scientific observers', CCAO, 'people who collect data at sea')],
  dnote=DN_NO.format(r='CCAMLR is an intergovernmental commission and does not take donations.'),
  see=[('ASOC_Antarctic_Coalition.html', 'ASOC', 'Campaigning for Southern Ocean protection.')],
  pin=pin(-42.88, 147.33, 'Hobart, Tasmania, Australia (approximate)')),
 P(slug='SCAR_Antarctic_Research', title='SCAR: Scientific Committee on Antarctic Research', short='SCAR', cls='nonprofit',
  label='Scientific organization · since 1958', org='SCAR',
  img=('AirSAR_Scientists_Antarctica.jpg', 1920, 1268, "NASA JPL scientists planning radar survey lines aboard NASA's DC-8 over the Antarctic Peninsula"),
  credit='NASA/Jim Ross (ED04-0056-126, AirSAR 2004, public domain)',
  hook="Since 1958, Antarctic scientists working together.",
  wow=('SCAR gives objective, independent scientific advice to the Antarctic Treaty Consultative Meetings and bodies such as the UNFCCC and IPCC (SCAR).', SCAR),
  lead='SCAR initiates, develops and coordinates international scientific research in the Antarctic region, including the Southern Ocean (SCAR).',
  eli=['Scientists from many countries study Antarctica.', 'SCAR helps them work together.', 'It tells governments what the science says.'],
  ws=[('Who', 'SCAR, a thematic organisation of the International Science Council.', SCAR),
      ('What', 'Over 30 research groups and scientific advice on Antarctic science and conservation.', SCAR),
      ('When', 'Since 1958.', SCAR),
      ('Where', 'Antarctica and the Southern Ocean.', SCAR),
      ('Why', "To understand the Antarctic region's role in the Earth system.", SCAR)],
  impact=('Its advice covers issues of science and conservation affecting the management of Antarctica and the Southern Ocean (SCAR).', SCAR),
  fact=('30+ Groups', 'SCAR currently has over 30 groups addressing aspects of Antarctic research (SCAR).', SCAR),
  people=('Its fellowships and visiting professorships build research capacity (SCAR).', SCARD),
  nature=('Its science advice informs conservation of Antarctica and the Southern Ocean (SCAR).', SCAR),
  support_h='Support SCAR', btns=[('Donate to SCAR', SCARD[0])],
  bottom=('SCAR accepts donations, which support its Antarctic work, including fellowships.', SCARD[0], 'Donate'),
  help=[('Volunteer opportunities', SCARO, 'roles in SCAR groups for researchers at many career stages'),
        ('Sign up for the free newsletter', SCAR[0], 'follow Antarctic science news')],
  dnote=DN_YES.format(r='SCAR is a registered charity with the UK Charity Commission (no. 1124840).'),
  see=[('SOOS.html', 'SOOS', 'Southern Ocean observing network.')],
  pin=pin(52.2, 0.12, 'Cambridge, United Kingdom (approximate)')),
 P(slug='IAATO', title='IAATO: Responsible Antarctic Tourism', short='IAATO', cls='corporate',
  label='Industry association · since 1991', org='IAATO',
  img=('Larsen_Ice_Shelf_AirSAR.jpg', 1920, 1268, "Approaching the Larsen Ice Shelf, Antarctic Peninsula, from NASA's DC-8"),
  credit='NASA/Jim Ross (ED04-0056-110, AirSAR 2004, public domain)',
  hook='Rules that let visitors see Antarctica without harming it.',
  wow=('In 2019 IAATO set up vessel slow-down areas covering more than 20,000 km² where whales are dense, to reduce the risk of ship strikes (IAATO).', IAC),
  lead='IAATO, founded in 1991, promotes safe and environmentally responsible private-sector travel to the Antarctic (IAATO).',
  eli=['Some people visit Antarctica on ships.', 'Visitors could disturb wildlife.', 'IAATO members follow rules, and visitors help scientists too.'],
  ws=[('Who', 'IAATO, a member organisation of tour operators.', IAA),
      ('What', 'Responsible-visit practices plus citizen science on member trips.', IAC),
      ('When', 'Since 1991.', IAA),
      ('Where', 'Antarctica.', IAA),
      ('Why', 'Antarctica is one of the most perfectly preserved regions on the planet.', IAA)],
  impact=("Member operators offer guests citizen science such as Happywhale, Penguin Watch and NASA's GLOBE Clouds (IAATO).", IAC),
  fact=('100+ Nationalities', 'Visitors represent more than 100 nationalities on average per season (IAATO).', IAA),
  people=('Visitors return home as ambassadors of goodwill, guardianship and peace (IAATO).', IAA),
  nature=('Slow-down areas reduce the risk of ships striking whales (IAATO).', IAC),
  support_h='Learn More About IAATO', btns=[('IAATO: Citizen Science', IAC[0])],
  bottom=("Want to go deeper? See IAATO's citizen science projects.", IAC[0], 'For Further Information'),
  help=[('Join citizen science', IAC[0], 'Happywhale and GLOBE Clouds accept photos and observations from volunteers'),
        ('Check a tour operator', IAAM, 'if you visit, see whether the company is an IAATO member')],
  dnote=DN_NO.format(r='IAATO is an industry association and does not take donations.'),
  see=[('Penguin_Watch.html', 'Penguin Watch', 'Count penguins online.')],
  pin=pin(-64.82, -63.4, 'Antarctic Peninsula (approximate)')),
]

PAGES = NORTH + SOUTH
SHIP = [p['slug'] for p in PAGES]
NORTH_NEW = [p['slug'] for p in NORTH]; SOUTH_NEW = [p['slug'] for p in SOUTH]
GROUPS = [
 ('north-pole', 'North Pole: The Arctic', 'Sea ice, Greenland, Iceland, Svalbard and the Arctic Ocean.',
  ['Svalbard_Global_Seed_Vault', 'Carbfix', 'Iceland_Land_Restoration', 'PROMICE_GC-Net', 'Arctic_Weather_Satellite'] + NORTH_NEW),
 ('south-pole', 'South Pole: Antarctica', 'Antarctica, its ice and the Southern Ocean.',
  ['Thwaites_Glacier_Collaboration', 'Ross_Sea_MPA', 'South_Georgia_Habitat_Restoration'] + SOUTH_NEW),
 ('both-poles', 'Both Poles', 'Satellites that watch the ice at both ends of the Earth.',
  ['CryoSat', 'CRISTAL', 'CIMR', 'ICESat-2', 'PREFIRE', 'RCM', 'GCOM-W_SHIZUKU', 'SCISAT']),
]
XBACK = {
 'Ross_Sea_MPA.html': [('CCAMLR.html', 'CCAMLR', 'The treaty body that conserves Antarctic marine life.')],
 'South_Georgia_Habitat_Restoration.html': [('Gough_Island_Restoration.html', 'Gough Island Restoration', 'Another island effort against invasive rodents.')],
 'Svalbard_Global_Seed_Vault.html': [('MOSAiC_Expedition.html', 'MOSAiC Expedition', 'A year frozen into the Arctic ice.')],
}
WTH = {  # slug -> (org key, [name, donate, help, contact]); donate only where audited/rated (see docstring)
 'Polar_Bears_International': ('pbi', ['Polar Bears International', PBID, 'https://polarbearsinternational.org/news-media/events/polar-bear-week/', None]),
 'SmartICE': ('smartice', ['SmartICE', None, SMI[0], None]),
 'Permafrost_Pathways': ('permafrostpathways', ['Permafrost Pathways (Woodwell Climate)', PPD, PPA[0], None]),
 'Tallurutiup_Imanga_NMCA': ('parkscanada', ['Parks Canada', None, PCV, None]),
 'PAME_Arctic_Council': ('pame', ['PAME (Arctic Council)', None, PAML, None]),
 'CAFF_Arctic_Biodiversity': ('caff', ['CAFF (Arctic Council)', None, CAFFD, None]),
 'MOSAiC_Expedition': ('mosaic', ['MOSAiC (AWI)', None, MOSE[0], None]),
 'WWF_Arctic_Programme': ('wwfarctic', ['WWF Arctic Programme', None, WWFL[0], None]),
 'Inuit_Circumpolar_Council': ('icc', ['Inuit Circumpolar Council', None, ICC[0], None]),
 'Arctic_Basecamp': ('arcticbasecamp', ['Arctic Basecamp', None, ABJ, None]),
 'Gough_Island_Restoration': ('gough', ['Gough Island Restoration Programme (RSPB)', None, GOUG[0], None]),
 'Penguin_Watch': ('penguinwatch', ['Penguin Watch (Zooniverse)', None, PWZ[0], None]),
 'Oceanites_Penguin_Census': ('oceanites', ['Oceanites', OCED, OCEG[0], None]),
 'SOCCOM': ('soccom', ['SOCCOM', None, SOCA, None]),
 'SOOS': ('soos', ['SOOS', None, SOOG[0], None]),
 'Beyond_EPICA_Oldest_Ice': ('beyondepica', ['Beyond EPICA', None, EPIP, None]),
 'ASOC_Antarctic_Coalition': ('asoc', ['ASOC', ASOD, ASOT[0], None]),
 'CCAMLR': ('ccamlr', ['CCAMLR', None, CCAS, None]),
 'SCAR_Antarctic_Research': ('scar', ['SCAR', SCARD[0], SCARO, None]),
 'IAATO': ('iaato', ['IAATO', None, IAC[0], None]),
}
CSS = ('/* HOWHELP1028:START */.how-help{max-width:900px;margin:1.6rem auto;padding:0 1.2rem}.how-help ul{line-height:1.6}'
       '.how-help .help-note{font-size:.92rem;opacity:.92}.polar-group{margin:1.2rem 0 .4rem}.polar-group+p{margin:.2rem 0 .8rem;opacity:.9}/* HOWHELP1028:END */')
CARD_RX = r'<article class="card"><div class="image-container"><a class="photo-link" href="([^"]+)\.html">.*?</article>'

def group_polar():
    fp = os.path.join(ROOT, 'Polar.html'); t = open(fp, encoding='utf8').read()
    i = t.find('<section class="card-band hub-cards" id="missions">'); j = t.find('</section>', i) + len('</section>')
    cards = {m.group(1): m.group(0) for m in re.finditer(CARD_RX, t[i:j], re.S)}
    out, used = [], set()
    for gid, h, d, slugs in GROUPS:
        used |= set(slugs)
        out.append(f'<h3 class="polar-group" id="{gid}">{E(h)}</h3><p>{E(d)}</p><div class="grid">{"".join(cards[s] for s in slugs if s in cards)}</div>')
    rest = [c for s, c in cards.items() if s not in used]
    if rest: out.append('<div class="grid">' + ''.join(rest) + '</div>')
    jump = ' · '.join(f'<a href="#{g[0]}">{E(g[1])}</a>' for g in GROUPS)
    t = t[:i] + f'<section class="card-band hub-cards" id="missions"><h2>Missions and Solutions</h2><p class="polar-jump">{jump}</p>' + ''.join(out) + '</section>' + t[j:]
    open(fp, 'w', encoding='utf8').write(t)
    print('polar groups:', [(g[0], len([s for s in g[3] if s in cards])) for g in GROUPS], 'ungrouped:', len(rest))

def wth():
    fp = os.path.join(ROOT, 'assets/data/ways-to-help.json'); d = json.load(open(fp, encoding='utf8'))
    for s, (k, row) in WTH.items(): d['orgs'][k] = row; d['pages'][s] = k
    json.dump(d, open(fp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

def main():
    b20s.PAGES, b20s.SHIP, b20s.XBACK, b20s.ADDED = PAGES, SHIP, {}, ADDED
    b20s.main()  # pages, hub cards (into the last grid of #missions), eli10, map pins, anim-banners
    group_polar()
    for f, items in XBACK.items():
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = f'<!-- {TAG}:START -->' + see_block(items, 'connected-1028') + f'<!-- {TAG}:END -->'
        if f'<!-- {TAG}:START -->' in t:
            t = re.sub(rf'<!-- {TAG}:START -->.*?<!-- {TAG}:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    wth()
    cp = os.path.join(ROOT, 'styles.css'); css = open(cp, encoding='utf8').read()
    css2 = re.sub(r'/\* HOWHELP1028:START \*/.*?/\* HOWHELP1028:END \*/', lambda m: CSS, css, flags=re.S) if 'HOWHELP1028:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
    if css2 != css: open(cp, 'w', encoding='utf8').write(css2)

if __name__ == '__main__':
    main()
