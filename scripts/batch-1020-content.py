#!/usr/bin/env python3
"""Oct 20 2026 Alaska batch (owner approved Oct 20): Gulf of Alaska Keeper (with its Montague Island volunteer partner, the
Prince William Sound Stewardship Foundation, folded into the same page), Alaska kelp and seaweed farming (Alaska Mariculture
Alliance + Alaska Sea Grant), Bristol Bay salmon habitat protection (EPA CWA 404(c); court ruling pending, stated neutrally),
Alaska SeaLife Center. Same writer as batch-1019-content.py (Surfrider skeleton, BLUF hook + sourced wow fact, Five W's,
widgets, Connected Solutions, hub cards, eli10, map pins). Every fact is from the cited page (fetched 2026-10-20);
org figures are labeled as theirs. Figures we could not verify were left out (e.g. SeaLife Center rescue/release totals).
Re-runnable: overwrites only these pages, their hub cards (added once) and the XLINK1020 blocks."""
import json, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('b19', os.path.join(ROOT, 'scripts/batch-1019-content.py'))
b19 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b19)
b18, W, see_block, E = b19.b18, b19.W, b19.see_block, b19.E
ADDED = '2026-10-20'
SHIP = ['Gulf_of_Alaska_Keeper', 'Alaska_Kelp_Farming', 'Bristol_Bay_Salmon', 'Alaska_SeaLife_Center']

GOAKH = ('https://goak.org/', 'Gulf of Alaska Keeper')
GOAK = ('https://goak.org/about/', 'Gulf of Alaska Keeper, About')
GOAKDON = 'https://goak.org/short-code/'
NOAAM = ('https://marinedebris.noaa.gov/removal/removing-large-scale-marine-debris-montague-island-northern-gulf-alaska', 'NOAA Marine Debris Program, Removing large-scale marine debris from Montague Island (updated March 25, 2026)')
KTUU = ('https://www.alaskasnewssource.com/2025/08/30/gulf-alaska-keeper-moving-make-montague-island-pristine-once-again/', "Alaska's News Source (KTUU), Gulf of Alaska Keeper moving to make Montague Island pristine once again (Aug. 29, 2025)")
AMK = ('https://mariculturealaska.org/kelp/', 'Alaska Mariculture Alliance, Kelp')
MRG = ('https://alaskamariculturecluster.org/wp-content/uploads/2026/07/Spring-2026-Alaska-mariculture-update-7.30.26.pdf', 'McKinley Research Group for the Alaska Mariculture Cluster, Alaska Mariculture Industry Update, Spring 2026')
ASG = ('https://alaskaseagrant.org/our-work/aquaculture/', 'Alaska Sea Grant, Aquaculture in Alaska')
EPAF = ('https://www.epa.gov/bristolbay/final-determination-pebble-deposit-area', 'U.S. EPA, Final Determination for Pebble Deposit Area')
EPAPDF = ('https://www.epa.gov/system/files/documents/2023-01/Pebble-Deposit-Area-404c-FD-Jan2023.pdf', 'U.S. EPA, Final Determination, Pebble Deposit Area (January 2023)')
FR23 = ('https://www.federalregister.gov/documents/2023/02/03/2023-02287/final-determination-to-prohibit-the-specification-of-and-restrict-the-use-for-specification-of', 'Federal Register, Final Determination, Pebble Deposit Area (Feb. 3, 2023)')
ADFG = ('https://www.adfg.alaska.gov/FedAidPDFs/FMR26-08.pdf', 'Alaska Department of Fish and Game, 2025 Bristol Bay Area Annual Management Report (May 2026)')
KDLG = ('https://www.kdlg.org/2026-06-26/federal-judge-hears-oral-arguments-in-pebble-mine-case-decision-pending', 'KDLG, Federal judge hears oral arguments in Pebble mine case, decision pending (June 26, 2026)')
ANEWS = ('https://alaskanews.com/c/alaska-news/the-fate-of-the-epa-veto-blocking-pebble-mine-is-now-in-a-federal-judges-hands', "Alaska News, The fate of the EPA veto blocking Pebble Mine is now in a federal judge's hands (August 2026)")
ASLC = ('https://www.alaskasealife.org/uploads/pdfs/annual_reports/2024_annual_report.pdf', 'Alaska SeaLife Center, 2024 Annual Report')
ASLCR = 'https://www.alaskasealife.org/annual_and_financial_reports'
ASLCDON = 'https://www.alaskasealife.org/donate'

PAGES = [
 dict(slug='Gulf_of_Alaska_Keeper', title='Gulf of Alaska Keeper: Marine Debris Cleanup', short='Gulf of Alaska Keeper', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='nonprofit', status='active', glass='ocean', label='Nonprofit solution · active',
  img=('Gulf_of_Alaska_Bloom_2017.jpg', 1920, 1748, 'The Gulf of Alaska and Prince William Sound with a green spring plankton bloom offshore and snow-covered mountains, seen from orbit'),
  credit='NASA/Goddard/NPP (GSFC_20171208_Archive_e000038, Gulf of Alaska spring bloom, April 12, 2017)',
  hook="On some of North America's wildest beaches, crews fly the ocean's trash out by helicopter.",
  wow=('Since 2006, Gulf of Alaska Keeper has removed more than 5 million pounds of plastic from 1,500 miles of remote coastline (nonprofit figures).', GOAKH),
  lead='Gulf of Alaska Keeper (GoAK) is a nonprofit that removes marine debris from the remote shores of Prince William Sound and the northern Gulf of Alaska (GoAK).',
  eli=['Ocean currents carry nets, ropes and plastic to faraway Alaska beaches where nobody lives.',
       'Gulf of Alaska Keeper crews and volunteers pick it up and pack it into giant bags.',
       'Helicopters lift the bags to a barge, and the trash goes to Anchorage to be recycled or thrown away safely.'],
  ws=[('Who', 'Gulf of Alaska Keeper, a nonprofit headquartered in Anchorage and Whittier, Alaska.', GOAK),
      ('What', 'Large-scale marine debris removal and coastal restoration: derelict fishing nets, ropes, buoys, hazmat containers and creosote-treated wood.', KTUU),
      ('When', 'Since 2006. Its NOAA-supported Montague Island project runs from October 2024 to September 2026.', NOAAM),
      ('Where', 'Prince William Sound and the northern Gulf of Alaska, from Kayak Island west to the Barren Islands.', GOAK),
      ('Why', 'Debris on these shores is an ingestion and entanglement hazard for commercially and culturally important animals and habitat (NOAA).', NOAAM)],
  impact=('In 2025, GoAK gathered and consolidated more than 500 tons of marine debris on Montague Island, where more than 60 volunteers gave more than 5,000 hours (GoAK, reported by KTUU).', KTUU),
  fact=('Partner: Prince William Sound Stewardship Foundation', 'On Montague Island, the Prince William Sound Stewardship Foundation and the Center for Alaskan Coastal Studies recruit and manage all the volunteers and lead community outreach (NOAA).', NOAAM),
  people=('Many Alaskans depend on this coast for food, and volunteers from across the region join the cleanups (KTUU).', KTUU),
  nature=('Debris is recycled where possible, and plastics that cannot be recycled are processed into construction materials (NOAA).', NOAAM),
  support_h='Support Gulf of Alaska Keeper',
  btns=[('Donate', GOAKDON), ('About Gulf of Alaska Keeper', GOAK[0])],
  bottom=('Support Gulf of Alaska Keeper directly.', GOAKDON, 'Donate'),
  widget=None, see=[('Ocean_Voyages_Institute.html', 'Ocean Voyages Institute', 'Sails out to pull ghost nets and plastic from the open Pacific.'),
                    ('Alaska_SeaLife_Center.html', 'Alaska SeaLife Center', "Rescues stranded seals and sea otters on Alaska's coast.")],
  pin={'status': 'active', 'pins': [{'lat': 59.95, 'lng': -147.45, 'label': 'Montague Island, Prince William Sound, Alaska', 'basis': 'page'}]}),
 dict(slug='Alaska_Kelp_Farming', title='Alaska Kelp and Seaweed Farming', short='Alaska kelp farming', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='corporate', status='active', glass='ocean', label='Industry solution · active',
  img=('Alaska_Clear_View_Terra_2013.jpg', 1920, 2520, 'A rare, nearly cloud-free view of Alaska, its mountains, forests and long southern coast, seen by the Terra satellite'),
  credit='NASA (GSFC_20171208_Archive_e001460, Terra/MODIS, Alaska, June 17, 2013)',
  hook="Alaska's youngest farm crop grows underwater.",
  wow=('Alaska seaweed farmers harvested 344,166 pounds in 2025, and the 2026 harvest is estimated at 650,000 to 850,000 pounds (McKinley Research Group).', MRG),
  lead="More than 20 kelp farms grow ribbon, giant, bull and sugar kelp in Alaska's cold, nutrient-rich waters (Alaska Mariculture Alliance).",
  eli=['Kelp is a big seaweed that grows fast in cold ocean water.',
       'Alaska farmers grow it on lines in the sea and harvest it each spring and early summer.',
       'It becomes food, farm and beauty products, and it takes up carbon and extra nutrients from the water.'],
  ws=[('Who', "Alaska's kelp farmers, supported by the Alaska Mariculture Alliance and by Alaska Sea Grant, which trains seaweed and shellfish farmers.", ASG),
      ('What', 'Ocean farms that grow kelp. Under Alaska law, aquatic farming is limited to shellfish and seaweeds.', ASG),
      ('When', "Alaska's first commercial kelp harvest was in 2017. Harvesting takes place each spring and early summer.", AMK),
      ('Where', 'Coastal Alaska. Of the 13 new aquatic farm lease applications in 2026, 10 are kelp farms in Southeast Alaska.', MRG),
      ('Why', 'Kelp farming supports coastal communities and contributes to ocean health by absorbing carbon and excess nutrients (Alaska Mariculture Alliance).', AMK)],
  impact=('Alaska hatcheries sold or transferred 353,930 feet of seeded line in 2025, the most on record (McKinley Research Group).', MRG),
  fact=('A Record 872,288 Pounds', "Alaska's seaweed harvest grew from 19,590 pounds in 2017 to a record 872,288 pounds in 2022 (McKinley Research Group).", MRG),
  people=('Alaska Sea Grant gives farmers training, workshops and help with permits and business plans, supporting coastal community resilience (Alaska Sea Grant).', ASG),
  nature=('As it grows, kelp absorbs carbon and excess nutrients from the water (Alaska Mariculture Alliance).', AMK),
  support_h='Find Alaska Kelp',
  btns=[('Alaska Kelp Farms Directory', AMK[0]), ('Alaska Sea Grant Mariculture', ASG[0])],
  bottom=('Want to go deeper? Alaska Sea Grant explains how mariculture works in Alaska.', ASG[0], 'For Further Information'),
  widget=None, see=[('Kelp_Forests.html', 'Kelp Forests', 'Why wild kelp forests matter, and the teams restoring them.')],
  pin={'status': 'active', 'pins': [{'lat': 57.79, 'lng': -152.41, 'label': 'Kodiak, Alaska (Alaska Sea Grant mariculture specialists)', 'basis': 'page'}, {'lat': 55.54, 'lng': -132.40, 'label': 'Kasaan Bay, Southeast Alaska (new kelp farm leases)', 'basis': 'page'}]}),
 dict(slug='Bristol_Bay_Salmon', title='Bristol Bay Salmon Habitat Protection (EPA)', short='the Bristol Bay protection', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='government', status='active', glass='ocean', label='Government solution · active',
  img=('Bristol_Bay_Terra_2017.jpg', 1920, 2329, 'Bristol Bay and the Alaska Peninsula in southwest Alaska, with brown spring tundra and wave clouds over the sea, seen by the Terra satellite'),
  credit='NASA Earth Observatory image by Joshua Stevens, using MODIS data from LANCE/EOSDIS Rapid Response (Bristol Bay, May 14, 2017)',
  hook="The world's largest sockeye salmon fishery starts in these headwater streams.",
  wow=('In 2025, about 56.8 million sockeye salmon returned to Bristol Bay, 14% above the preseason forecast (ADF&G).', ADFG),
  lead='In January 2023, the U.S. EPA used Clean Water Act section 404(c) to limit mine waste disposal in Bristol Bay headwaters near the Pebble deposit. The decision is being challenged in federal court (EPA).',
  eli=['Bristol Bay in Alaska has rivers full of wild salmon.',
       'A large copper and gold mine was proposed near streams where many of those salmon start life.',
       'The U.S. government limited where mine waste could go, and a judge is now deciding whether that decision stands.'],
  ws=[('Who', 'The U.S. Environmental Protection Agency (EPA), using its authority under Clean Water Act section 404(c).', EPAF),
      ('What', 'A Final Determination that prohibits and restricts the use of certain waters in the South Fork Koktuli, North Fork Koktuli and Upper Talarik Creek watersheds as disposal sites for dredged or fill material tied to a mine at the Pebble deposit.', FR23),
      ('When', 'Issued Jan. 30, 2023.', EPAF),
      ('Where', 'Headwaters of the Bristol Bay watershed in southwest Alaska, around the Pebble copper, gold and molybdenum deposit.', FR23),
      ('Why', 'EPA found the 2020 mine plan would permanently remove about 8.5 miles of salmon streams, 91 miles of streams that support them and 2,108 acres of wetlands and other waters.', EPAF)],
  impact=('In 2025, sockeye escapement goals were met or exceeded in every system with a goal, and the commercial sockeye harvest of 41.2 million fish was the 6th largest since records began in 1893 (ADF&G).', ADFG),
  fact=('Legal Status: Ruling Pending', 'Northern Dynasty Minerals and the Pebble Limited Partnership, the State of Alaska and two Alaska Native village corporations sued in 2024, arguing EPA exceeded its authority. The U.S. Department of Justice defends the decision, joined by intervenors including Bristol Bay Native Corporation, tribes, fishing groups and conservation groups. Judge Sharon Gleason heard arguments on June 25, 2026, and had not ruled as of Oct. 20, 2026.', ANEWS),
  people=("The 2025 commercial salmon catch was worth about $201.3 million, and subsistence harvests averaged 105,749 salmon a year from 2014 to 2023 (ADF&G).", ADFG),
  nature=("Bristol Bay's salmon are entirely wild: no hatchery fish are raised or released in the watershed (EPA).", EPAPDF),
  support_h='Learn More About Bristol Bay',
  btns=[('EPA Final Determination', EPAF[0]), ('Bristol Bay Salmon Report (ADF&G)', ADFG[0])],
  bottom=('Want to go deeper? EPA explains its Final Determination.', EPAF[0], 'For Further Information'),
  widget=W('Pebble deposit case (Clean Water Act 404(c))', 'Ruling pending in the U.S. District Court for the District of Alaska. Arguments were heard on June 25, 2026; no ruling as of Oct. 20, 2026.', KDLG, 'U.S. District Court, District of Alaska',
           milestones=[('2023-01-30', 'EPA Final Determination'), ('2024-03-01', 'Lawsuits filed'), ('2026-06-25', 'Oral arguments')]),
  see=[('Klamath_River_Dam_Removal.html', 'Klamath River Dam Removal', 'Reopening hundreds of miles of river to salmon.')],
  pin={'status': 'active', 'pins': [{'lat': 59.90, 'lng': -155.30, 'label': 'Pebble deposit area, Bristol Bay watershed, Alaska', 'basis': 'page'}, {'lat': 58.70, 'lng': -158.20, 'label': 'Bristol Bay, Alaska', 'basis': 'page'}]}),
 dict(slug='Alaska_SeaLife_Center', title='Alaska SeaLife Center: Marine Wildlife Rescue', short='the Alaska SeaLife Center', cat='ocean',
  hub=('Oceans.html', 'Ocean'), cls='nonprofit', status='active', glass='ocean', label='Nonprofit solution · active',
  img=('Gulf_of_Alaska_Aurora_ISS_2025.jpg', 1920, 1280, 'Clouds swirling over the Gulf of Alaska under a green aurora, seen at night from the International Space Station'),
  credit='NASA (iss072e820937, Gulf of Alaska and aurora, March 12, 2025)',
  hook='Alaska has one permanent place to rescue stranded seals, sea otters and walruses, and it is in Seward.',
  wow=("It runs Alaska's only permanent marine mammal rescue and rehabilitation center, for a coastline of more than 33,900 miles (Alaska SeaLife Center).", ASLC),
  lead="The Alaska SeaLife Center in Seward is a nonprofit aquarium and research center that rescues stranded marine animals, studies Alaska's marine ecosystems and teaches ocean science (Alaska SeaLife Center).",
  eli=['Sometimes baby seals and sea otters lose their mothers or get hurt.',
       'The Alaska SeaLife Center brings them to Seward and cares for them day and night.',
       'Its scientists also study sea lions and seabirds to learn how the ocean is changing.'],
  ws=[('Who', 'The Alaska SeaLife Center, a 501(c)(3) nonprofit. Its rehabilitation work is authorized by USFWS and NMFS.', ASLC),
      ('What', 'Marine wildlife rescue and rehabilitation, research and ocean education.', ASLC),
      ('When', 'Open since 1998; 2024 marked 26 years of its Wildlife Response Program.', ASLC),
      ('Where', 'Seward, Alaska, the gateway to Kenai Fjords National Park.', ASLC),
      ('Why', "Its mission is to generate and share scientific knowledge to promote understanding and stewardship of Alaska's marine ecosystems.", ASLC)],
  impact=('In 2024, its education programs reached more than 94,000 people on site and 181,000 off site, and its distance learning has reached classrooms in all 50 U.S. states and 10 countries (Alaska SeaLife Center).', ASLC),
  fact=('Meet Uki the Walrus Calf', 'In July 2024, the center led intensive care for a rare orphaned Pacific walrus calf rescued from Utqiagvik. Her name, Ukiaq, means "autumn" in Iñupiaq (Alaska SeaLife Center).', ASLC),
  people=('The center reports that it is the main reason 28,700 people visit Seward each year, with a $46.5 million direct positive impact on the local economy (Alaska SeaLife Center).', ASLC),
  nature=("Its long-term studies include 27 years of Steller sea lion video monitoring on Chiswell Island and Alaska's only year-round marine bird survey, in Resurrection Bay since 2011 (Alaska SeaLife Center).", ASLC),
  support_h='Support the Alaska SeaLife Center',
  btns=[('Donate', ASLCDON), ('Annual Reports', ASLCR)],
  bottom=('Support the Alaska SeaLife Center directly.', ASLCDON, 'Donate'),
  widget=None, see=[('Gulf_of_Alaska_Keeper.html', 'Gulf of Alaska Keeper', "Clears tons of debris from Alaska's remote beaches.")],
  pin={'status': 'active', 'pins': [{'lat': 60.0995, 'lng': -149.4417, 'label': 'Alaska SeaLife Center, Seward, Alaska', 'basis': 'page'}]}),
]

XBACK = {
 'Ocean_Voyages_Institute.html': [('Gulf_of_Alaska_Keeper.html', 'Gulf of Alaska Keeper', "Clears tons of debris from Alaska's remote beaches.")],
 'Kelp_Forests.html': [('Alaska_Kelp_Farming.html', 'Alaska Kelp and Seaweed Farming', "Alaska's fast-growing ocean farm crop.")],
}

def main():
    b19.PAGES, b19.SHIP, b19.XBACK, b19.ADDED = PAGES, SHIP, {}, ADDED
    b19.main()
    for f, items in XBACK.items():
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = '<!-- XLINK1020:START -->' + see_block(items, 'connected-1020') + '<!-- XLINK1020:END -->'
        if '<!-- XLINK1020:START -->' in t:
            t = re.sub(r'<!-- XLINK1020:START -->.*?<!-- XLINK1020:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)

if __name__ == '__main__':
    main()
