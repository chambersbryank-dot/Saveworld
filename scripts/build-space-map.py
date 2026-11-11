#!/usr/bin/env python3
"""Draft Space Map data, spacecraft images, and Space_Map.html.

Not part of weekly-sync. Does not touch the nav, sitemap, or homepage.
Rerun after editing SATS below. Images are small WebP files under assets/space-map/.
"""
import html, json, re, time, urllib.parse, urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UA = 'SavingPlanets-SpaceMap/1.0 (https://www.savingplanets.com/; educational draft)'
TODAY = '2026-11-09'
COLOR = {'leo': '#3DDC97', 'sso': '#4CC3FF', 'meo': '#FFD166', 'geo': '#FF7A59', 'l1': '#C9A0FF', 'l2': '#C9A0FF', 'l5': '#C9A0FF'}
REGIME = {
    'leo': 'Low Earth orbit', 'sso': 'Sun-synchronous orbit', 'meo': 'Medium Earth orbit',
    'geo': 'Geostationary orbit', 'l1': 'Sun–Earth L1', 'l2': 'Sun–Earth L2', 'l5': 'Sun–Earth L5',
}

# One marker per solution page. norad None = approximate placement (no usable Earth TLE).
SATS = [
    dict(id='landsat9', page='Landsat_9.html', label='Landsat 9', regime='sso', norad=49260, expect='LANDSAT 9', q='Landsat 9 spacecraft'),
    dict(id='s2c', page='Sentinel-2C.html', label='Sentinel-2C', regime='sso', norad=60989, expect='SENTINEL-2C', q='Sentinel-2 satellite ESA'),
    dict(id='s1c', page='Sentinel-1.html', label='Sentinel-1C', regime='sso', norad=62261, expect='SENTINEL-1C', q='Sentinel-1 satellite ESA',
         extra='Sentinel-1C stands in for the Sentinel-1 constellation on that solution page.'),
    dict(id='s3b', page='Sentinel-3.html', label='Sentinel-3B', regime='sso', norad=43437, expect='SENTINEL-3B', q='Sentinel-3 satellite ESA',
         extra='Sentinel-3B stands in for the Sentinel-3 pair on that solution page.'),
    dict(id='s5p', page='Sentinel-5P.html', label='Sentinel-5P', regime='sso', norad=42969, expect='SENTINEL-5P', q='Sentinel-5P satellite Tropomi'),
    dict(id='s6b', page='Sentinel-6B.html', label='Sentinel-6B', regime='leo', norad=66514, expect='SENTINEL-6B', q='Sentinel-6 satellite ESA NASA',
         extra='Sentinel-6B flies a non-sun-synchronous orbit, inclined about 66°, near 1,300 km.'),
    dict(id='oco2', page='OCO-2.html', label='OCO-2', regime='sso', norad=40059, expect='OCO 2', q='OCO-2 Orbiting Carbon Observatory spacecraft'),
    dict(id='smap', page='SMAP.html', label='SMAP', regime='sso', norad=40376, expect='SMAP', q='SMAP spacecraft NASA'),
    dict(id='pace', page='PACE.html', label='PACE', regime='sso', norad=58928, expect='PACE', q='PACE spacecraft NASA plankton'),
    dict(id='swot', page='SWOT.html', label='SWOT', regime='leo', norad=54754, expect='SWOT', q='SWOT satellite spacecraft NASA'),
    dict(id='icesat2', page='ICESat-2.html', label='ICESat-2', regime='leo', norad=43613, expect='ICESAT-2', q='ICESat-2 spacecraft NASA'),
    dict(id='gracefo', page='GRACE-FO.html', label='GRACE-FO', regime='leo', norad=43476, expect='GRACE-FO', q='GRACE-FO spacecraft NASA',
         extra='GRACE-FO 1 stands in for the twin pair. Both fly this orbit.'),
    dict(id='nisar', page='NISAR.html', label='NISAR', regime='sso', norad=65053, expect='NISAR', q='NISAR satellite NASA ISRO'),
    dict(id='earthcare', page='EarthCARE.html', label='EarthCARE', regime='sso', norad=59908, expect='EARTHCARE', q='EarthCARE satellite ESA JAXA'),
    dict(id='noaa21', page='JPSS.html', label='NOAA-21', regime='sso', norad=54234, expect='NOAA 21', q='NOAA-21 JPSS satellite',
         extra='NOAA-21 stands in for the Joint Polar Satellite System on that solution page.'),
    dict(id='gcomc', page='GCOM-C.html', label='GCOM-C', regime='sso', norad=43065, expect='SHIKISAI', q='GCOM-C SHIKISAI satellite JAXA'),
    dict(id='gcomw', page='GCOM-W_SHIZUKU.html', label='GCOM-W', regime='sso', norad=38337, expect='SHIZUKU', q='GCOM-W SHIZUKU satellite JAXA'),
    dict(id='gosatgw', page='GOSAT-GW.html', label='GOSAT-GW', regime='sso', norad=64694, expect='GOSAT-GW', q='GOSAT-GW IBUKI satellite JAXA'),
    dict(id='eos06', page='EOS-06.html', label='EOS-06', regime='sso', norad=54361, expect='OCEANSAT-3', q='Oceansat-3 EOS-06 satellite ISRO'),
    dict(id='alos4', page='ALOS-4.html', label='ALOS-4', regime='sso', norad=60182, expect='ALOS-4', q='ALOS-4 DAICHI-4 satellite JAXA'),
    dict(id='biomass', page='Biomass.html', label='Biomass', regime='sso', norad=63772, expect='BIOMASS', q='Biomass satellite ESA'),
    dict(id='tanager', page='Tanager-1.html', label='Tanager-1', regime='sso', norad=60507, expect='TANAGER', q='Tanager-1 satellite Planet Carbon Mapper'),
    dict(id='cryosat', page='CryoSat.html', label='CryoSat-2', regime='leo', norad=36508, expect='CRYOSAT', q='CryoSat-2 satellite ESA'),
    dict(id='aws', page='Arctic_Weather_Satellite.html', label='Arctic Weather Satellite', regime='sso', norad=60543, expect='ARCTIC WEATHER', q='Arctic Weather Satellite ESA'),
    dict(id='rcm', page='RCM.html', label='RADARSAT RCM-1', regime='sso', norad=44322, expect='RCM-1', q='RADARSAT Constellation Mission satellite',
         extra='RCM-1 stands in for the three-satellite RADARSAT Constellation.'),
    dict(id='neossat', page='NEOSSat.html', label='NEOSSat', regime='sso', norad=39089, expect='NEOSSAT', q='NEOSSat satellite Canada'),
    dict(id='scisat', page='SCISAT.html', label='SCISAT', regime='leo', norad=27858, expect='SCISAT', q='SCISAT satellite Canadian Space Agency'),
    dict(id='prefire', page='PREFIRE.html', label='PREFIRE-1', regime='sso', norad=59965, expect='PREFIRE-1', q='PREFIRE cubesat NASA',
         extra='PREFIRE-1 stands in for the two PREFIRE CubeSats.'),
    dict(id='adras', page='Astroscale.html', label='ADRAS-J', regime='sso', norad=58992, expect='ADRAS-J', q='ADRAS-J Astroscale spacecraft'),
    dict(id='punch', page='PUNCH.html', label='PUNCH', regime='sso', norad=63178, expect='PUNCH', q='PUNCH satellite NASA',
         extra='The PUNCH narrow-field imager stands in for the four PUNCH satellites, which share this orbit.'),
    dict(id='tracers', page='TRACERS.html', label='TRACERS 1', regime='sso', norad=64870, expect='TRACERS', q='TRACERS satellites NASA',
         extra='TRACERS 1 stands in for the twin TRACERS satellites.'),
    dict(id='hydro', page='HydroGNSS.html', label='HydroGNSS-1', regime='sso', norad=66762, expect='HYDROGNSS', q='HydroGNSS satellite ESA',
         extra='HydroGNSS-1 stands in for the two HydroGNSS satellites.'),
    dict(id='firesat', page='FireSat.html', label='FireSat 1', regime='sso', norad=69886, expect='FIRESAT', q='FireSat satellite Earth Fire Alliance',
         extra='FireSat 1 stands in for the FireSat constellation on that solution page.'),
    dict(id='gedi', page='GEDI.html', label='GEDI on the ISS', regime='leo', norad=25544, expect='ISS', q='GEDI instrument International Space Station',
         nudge=-18, extra='GEDI is an instrument on the International Space Station, so this marker follows the station (NORAD 25544).'),
    dict(id='emit', page='EMIT.html', label='EMIT on the ISS', regime='leo', norad=25544, expect='ISS', q='EMIT instrument International Space Station',
         nudge=18, extra='EMIT is an instrument on the International Space Station, so this marker follows the station (NORAD 25544).'),
    dict(id='galileo', page='Galileo.html', label='Galileo 23', regime='meo', norad=43566, expect='GALILEO', q='Galileo satellite ESA navigation',
         extra='Galileo 23 (GSAT0219) stands in for the Galileo constellation.'),
    dict(id='goes19', page='GOES-19.html', label='GOES-19', regime='geo', norad=60133, expect='GOES 19', q='GOES-19 GOES-U satellite NOAA'),
    dict(id='insat', page='INSAT-3DS.html', label='INSAT-3DS', regime='geo', norad=58990, expect='INSAT-3DS', q='INSAT-3DS satellite ISRO'),
    dict(id='mtgi', page='Meteosat_Third_Generation.html', label='MTG-I1', regime='geo', norad=54743, expect='MTG-I1', q='Meteosat Third Generation MTG-I1 satellite'),
    dict(id='mtgs', page='Sentinel-4.html', label='Sentinel-4 on MTG-S1', regime='geo', norad=64723, expect='MTG-S1', q='MTG-S1 Sentinel-4 satellite',
         extra='Sentinel-4 is an instrument on the geostationary MTG-S1 weather satellite (NORAD 64723).'),
    dict(id='tempo', page='TEMPO.html', label='TEMPO on Intelsat 40e', regime='geo', norad=56174, expect='INTELSAT 40E', q='TEMPO instrument Intelsat 40e',
         extra='TEMPO is a NASA instrument on the geostationary satellite Intelsat 40e (NORAD 56174).'),
    dict(id='mev', page='SpaceLogistics.html', label='MEV-2', regime='geo', norad=46113, expect='MEV-2', q='Mission Extension Vehicle MEV-2 Northrop Grumman',
         extra='MEV-2 stands in for Northrop Grumman SpaceLogistics life-extension vehicles in geostationary orbit.'),
    dict(id='metop', page='MetOp-SG-A1_Sentinel-5A.html', label='MetOp-SG-A1', regime='sso', norad=65159, expect='METOP-SGA1', q='MetOp-SG satellite ESA EUMETSAT'),
    dict(id='aeolus', page='Aeolus.html', label='Aeolus', regime='sso', q='Aeolus wind satellite ESA',
         approx=dict(altKm=320, inc=97, periodMin=90.7, raan=40, phase=0.4),
         source='Approximate sun-synchronous orbit near 320 km. Aeolus reentered on 28 July 2023, so there is no current TLE. The solution page describes the assisted reentry.'),
    dict(id='dscovr', page='DSCOVR_EPIC.html', label='DSCOVR', regime='l1', q='DSCOVR spacecraft NASA NOAA',
         approx=dict(kind='l1'),
         source='Approximate. DSCOVR sits in a halo orbit around Sun–Earth L1, about 1.5 million km toward the Sun (NASA/NOAA). It is drawn much closer so Earth stays visible. A standard Earth TLE is not used.'),
    dict(id='aditya', page='Aditya_L1.html', label='Aditya-L1', regime='l1', q='Aditya-L1 satellite ISRO',
         approx=dict(kind='l1'),
         source='Approximate. Aditya-L1 studies the Sun from a halo orbit around Sun–Earth L1, about 1.5 million km from Earth (solution page). Drawn closer than the real distance.'),
    dict(id='soho', page='SOHO.html', label='SOHO', regime='l1', q='SOHO spacecraft ESA NASA',
         approx=dict(kind='l1'),
         source='Approximate. SOHO has watched the Sun from Sun–Earth L1 since 1995 (solution page). Drawn closer than the real distance. A standard Earth TLE is not used.'),
    dict(id='imap', page='IMAP.html', label='IMAP', regime='l1', q='IMAP spacecraft NASA',
         approx=dict(kind='l1'),
         source='Approximate. IMAP watches the Sun from about a million miles sunward, around Sun–Earth L1 (solution page). No standard Earth TLE named IMAP was found on 9 November 2026. Drawn closer than the real distance.'),
    dict(id='carruthers', page='Carruthers.html', label='Carruthers', regime='l1', q='Carruthers Geocorona Observatory spacecraft NASA',
         approx=dict(kind='l1'),
         source='Approximate. The solution page says Carruthers watches Earth’s exosphere from about a million miles sunward (Sun–Earth L1). Drawn closer than the real distance.'),
    dict(id='webb', page='Webb_2024_YR4.html', label='James Webb', regime='l2', q='James Webb Space Telescope spacecraft',
         approx=dict(kind='l2'),
         source='Approximate. The James Webb Space Telescope operates around Sun–Earth L2 (NASA). This solution page is about Webb’s look at asteroid 2024 YR4. Drawn closer than the real distance.'),
    dict(id='neosurveyor', page='NEO_Surveyor.html', label='NEO Surveyor', regime='l1', q='NEO Surveyor spacecraft NASA',
         approx=dict(kind='l1'),
         source='Approximate. NEO Surveyor is planned for a halo orbit around Sun–Earth L1 and has not launched (solution page). Drawn closer than the real distance.'),
    dict(id='vigil', page='Vigil.html', label='Vigil', regime='l5', q='ESA Vigil space weather satellite L5',
         approx=dict(kind='l5'),
         source='Approximate. Vigil is planned for Sun–Earth L5, with launch planned for 2031 (solution page). Drawn closer than the real distance.'),
    dict(id='co2m', page='CO2M.html', label='CO2M', regime='sso', q='CO2M satellite Copernicus ESA',
         approx=dict(altKm=735, inc=98.0, periodMin=99.5, raan=12, phase=2.1),
         source='Approximate sun-synchronous orbit. CO2M is still being built and is not in orbit yet (solution page).'),
    dict(id='geoxo', page='GeoXO.html', label='GeoXO', regime='geo', q='GeoXO satellite NOAA NASA',
         approx=dict(altKm=35786, inc=0, periodMin=1436, fixed=True, lon=-105),
         source='Approximate geostationary orbit. GeoXO is a future NOAA/NASA series and is not in orbit yet (solution page). The longitude is a placeholder.'),
    dict(id='forum', page='FORUM.html', label='FORUM', regime='sso', q='FORUM satellite ESA far-infrared',
         approx=dict(altKm=830, inc=98.2, periodMin=101, raan=200, phase=3.4),
         source='Approximate sun-synchronous orbit. FORUM is a future ESA mission and is not in orbit yet (solution page).'),
    dict(id='libera', page='Libera.html', label='Libera', regime='sso', q='Libera Earth energy instrument NASA',
         approx=dict(altKm=824, inc=98.7, periodMin=101, raan=80, phase=4.2),
         source='Approximate sun-synchronous orbit. Libera is a future instrument planned to fly on a JPSS satellite, not its own spacecraft yet (solution page).'),
    dict(id='clearspace', page='ClearSpace.html', label='ClearSpace-1', regime='leo', q='ClearSpace-1 debris removal spacecraft ESA',
         approx=dict(altKm=700, inc=98, periodMin=98.5, raan=150, phase=1.7),
         source='Approximate low Earth orbit. ClearSpace-1 is a future debris-removal mission and is not in orbit yet (solution page).'),
    dict(id='lignosat', page='LignoSat.html', label='LignoSat', regime='leo', q='LignoSat wooden satellite JAXA',
         approx=dict(altKm=420, inc=51.6, periodMin=93, raan=10, phase=5.1),
         source='Approximate. LignoSat was deployed from the International Space Station into low Earth orbit (NASA, cited on the solution page). No current TLE named LignoSat was found on 9 November 2026, so it is drawn near the station’s orbit.'),
    dict(id='otter', page='Starfish_Otter.html', label='Starfish Otter', regime='leo', q='Starfish Space Otter spacecraft SSPICY',
         approx=dict(altKm=520, inc=97.4, periodMin=95, raan=260, phase=2.8),
         source='Approximate low Earth orbit. The solution page says the first Otter launched on 1 October 2026 on Transporter-18 to inspect objects in low Earth orbit. No CelesTrak entry named Starfish or SSPICY was found on 9 November 2026. The picture is Starfish’s Otter Pup, an earlier vehicle in the same Otter design.'),
    dict(id='usdv', page='US_Deorbit_Vehicle.html', label='U.S. Deorbit Vehicle', regime='leo', q='U.S. Deorbit Vehicle NASA SpaceX',
         approx=dict(altKm=410, inc=51.6, periodMin=92.7, raan=90, phase=0.9),
         source='Approximate low Earth orbit near the space station. The U.S. Deorbit Vehicle is a future spacecraft and is not in orbit yet (solution page).'),
]

SKIPPED = [
    {'group': 'Ground telescopes and night-sky projects', 'why': 'They are not satellites.',
     'pages': ['ATLAS.html', 'Catalina_Sky_Survey.html', 'Pan-STARRS.html', 'Globe_at_Night.html', 'ESA_NEOCC.html']},
    {'group': 'Radars and data services', 'why': 'They use satellite data, or watch satellites from the ground, but they are not one spacecraft in orbit.',
     'pages': ['LeoLabs.html', 'CAMS.html', 'Copernicus_EMS.html', 'Copernicus_Marine.html', 'Digital_Earth_Africa.html', 'FIRMS.html', 'OpenET.html', 'UNEP_MARS.html', 'Coral_Reef_Watch.html', 'EFFIS.html', 'International_Charter.html', 'GSMaP.html', 'GLOBE_Program.html', 'Tsunami_Early_Warning.html', 'SARSAT.html', 'Argos.html']},
    {'group': 'Concepts, charters, and natural worlds', 'why': 'No spacecraft to place.',
     'pages': ['Atmospheric_Drag.html', 'Three_Shields.html', 'Moon_Steadies_Earth.html', 'Jupiter.html', 'Enceladus.html', 'Titan.html', 'Orbital_Data_Centers.html', 'Zero_Debris_Charter.html']},
    {'group': 'Crew vehicles and station systems', 'why': 'Not Earth-observing or debris satellites. GEDI and EMIT, which ride on the station, are included.',
     'pages': ['Artemis_II.html', 'Gaganyaan.html', 'ISS_Water_Recovery.html', 'Veggie_Space_Garden.html']},
    {'group': 'Probes sent away from Earth', 'why': 'They do not stay in Earth orbit or at Sun–Earth L1, L2, or L5.',
     'pages': ['BepiColombo.html', 'Juice.html', 'Europa_Clipper.html', 'Lucy.html', 'Psyche.html', 'Hera.html', 'OSIRIS-APEX.html', 'Dragonfly.html', 'EnVision.html', 'ExoMars_Rosalind_Franklin.html', 'Hope_Mars_Mission.html', 'ESCAPADE.html', 'Emirates_Mission_Asteroid_Belt.html', 'Chandrayaan-5_LUPEX.html', 'Danuri_ShadowCam.html', 'MMX.html', 'Parker_Solar_Probe.html', 'Solar_Orbiter.html', 'Comet_Interceptor.html', 'Hayabusa2_Torifune.html', 'Ramses.html', 'Ariel.html', 'Plato.html', 'SPHEREx.html', 'Nancy_Grace_Roman.html', 'Voyager.html']},
    {'group': 'Future Earth missions left for the next pass', 'why': 'Not in orbit yet. The Coming Soon draft stays readable; add them in scripts/build-space-map.py when this map grows.',
     'pages': ['CHIME.html', 'CIMR.html', 'CRISTAL.html', 'FLEX.html', 'PRELUDE.html']},
]

LOCAL = {
    'pace': ('assets/PACE_Spacecraft_KSC.jpg', 'Photo: NASA/Kennedy Space Center.', 'photo', 'https://www.nasa.gov/', 'The PACE spacecraft in a clean room'),
    'aws': ('assets/Arctic_Weather_Satellite_ESA.jpg', 'Rendering: ESA, Arctic Weather Satellite (CC BY-SA 3.0 IGO).', 'render', 'https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/Arctic_Weather_Satellite', 'ESA rendering of the Arctic Weather Satellite above Earth'),
    'imap': ('assets/IMAP_Spacecraft_KSC.jpg', 'Photo: NASA/Kennedy Space Center.', 'photo', 'https://www.nasa.gov/', 'The IMAP spacecraft'),
    'alos4': ('assets/ALOS-4_Model_Tsukuba.jpg', 'Photo: Syced, via Wikimedia Commons (CC0). A 1/50 scale model of ALOS-4 at JAXA Tsukuba Space Center.', 'photo', 'https://commons.wikimedia.org/wiki/File:Artefacts_at_Tsukuba_Space_Center_exhibition_hall_55.jpg', 'Scale model of ALOS-4 with its radar antenna'),
    'adras': ('assets/Astroscale_ADRAS-J_H-IIA_Stage.jpg', 'Illustration: Astroscale, via Wikimedia Commons (CC BY-SA 4.0).', 'render', 'https://commons.wikimedia.org/wiki/File:ADRAS-J_Phase_I.png', 'Illustration of ADRAS-J approaching a spent rocket stage'),
}

GOOD = ('spacecraft', 'satellite', 'clean room', 'cleanroom', 'rendering', 'artist', 'illustration', 'impression', 'observatory', 'encapsul', 'solar array', 'instrument', 'cubesat', 'fairing', 'deploy')
BAD = ('hurricane', 'wildfire', 'temperature map', 'concentration', 'anomaly', 'global map', 'false color', 'logo only', 'coat of arms', 'flag of', 'ground track', 'data visualization', 'patch')


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    err = None
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(0.8 * (i + 1))
    raise err


def txt(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def cards():
    s = (ROOT / 'Solutions.html').read_text(encoding='utf8')
    out = {}
    for c in re.findall(r'<article class="card sol-card".*?</article>', s, re.S):
        u = re.search(r'data-url="([^"]+)"', c).group(1)
        name = txt(re.search(r'<h3>(.*?)</h3>', c, re.S).group(1))
        dm = re.search(r'class="sol-desc">(.*?)</p>', c, re.S)
        st = re.search(r'data-status="([^"]+)"', c)
        out[u] = dict(name=name, desc=txt(dm.group(1)) if dm else '', status=st.group(1) if st else 'active')
    return out


def fetch_tle(norad, expect):
    raw = get(f'https://celestrak.org/NORAD/elements/gp.php?CATNR={norad}&FORMAT=tle').decode('utf8', 'replace')
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip() and not ln.strip().lower().startswith('<!')]
    if not lines or 'not found' in raw.lower()[:80]:
        raise RuntimeError(f'No TLE for {norad} ({expect})')
    name = lines[0]
    l1 = next((ln for ln in lines if ln.startswith('1 ') and len(ln) > 60), None)
    l2 = next((ln for ln in lines if ln.startswith('2 ') and len(ln) > 60), None)
    if not l1 or not l2:
        raise RuntimeError(f'Bad TLE for {norad}: {raw[:180]!r}')
    if int(l1[2:7]) != int(norad):
        raise RuntimeError(f'TLE catalog mismatch for {norad}: {l1}')
    if expect.upper() not in name.upper():
        raise RuntimeError(f'TLE name mismatch for {norad}: got {name!r}, expected {expect!r}')
    return name, l1, l2


def score_text(title, desc):
    t = f'{title} {desc}'.lower()
    s = 0
    for g in GOOD:
        if g in t:
            s += 3
    for b in BAD:
        if b in t:
            s -= 4
    return s


def relevant(title, desc, need):
    blob = f'{title} {desc}'.lower()
    if not any(n.lower() in blob for n in need):
        return False
    if any(b in blob for b in ('nitrogen dioxide', 'concentration map', 'global map', 'ground track', 'false-color', 'false color')):
        return False
    return score_text(title, desc) >= 1


def nasa_candidate(query, need):
    url = 'https://images-api.nasa.gov/search?media_type=image&q=' + urllib.parse.quote(query)
    try:
        data = json.loads(get(url, timeout=30))
    except Exception:
        return None
    best = None
    for it in (data.get('collection') or {}).get('items', [])[:14]:
        meta = (it.get('data') or [{}])[0]
        title = meta.get('title') or ''
        desc = meta.get('description') or ''
        if not relevant(title, desc, need):
            continue
        sc = score_text(title, desc)
        links = it.get('links') or []
        preview = next((l.get('href') for l in links if l.get('href')), None)
        if not preview:
            continue
        if best is None or sc > best['score']:
            best = dict(score=sc, title=title, desc=desc[:240], preview=preview, nasa_id=meta.get('nasa_id'), page=f"https://images.nasa.gov/details/{meta.get('nasa_id')}" if meta.get('nasa_id') else 'https://images.nasa.gov/')
    if not best or best['score'] < 1:
        return None
    href = best['preview']
    if best.get('nasa_id'):
        try:
            asset = json.loads(get('https://images-api.nasa.gov/asset/' + urllib.parse.quote(best['nasa_id']), timeout=30))
            files = [x.get('href') for x in (asset.get('collection') or {}).get('items', []) if x.get('href')]
            jpgs = [h for h in files if re.search(r'\.(jpg|jpeg|png)($|\?)', h, re.I)]
            medium = [h for h in jpgs if re.search(r'medium|~medium|large|~large', h, re.I) and 'orig' not in h.lower()]
            if medium:
                href = medium[0]
            elif jpgs:
                href = sorted(jpgs, key=len)[0]
        except Exception:
            pass
    best['href'] = href
    best['credit'] = f"Image: NASA ({best['title']})."
    best['kind'] = 'render' if re.search(r'render|illustrat|artist|impression|concept', best['title'], re.I) else 'photo'
    best['where'] = 'nasa'
    return best


def commons_candidate(query, need):
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': query,
        'gsrnamespace': 6, 'gsrlimit': 8, 'prop': 'imageinfo',
        'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': 900,
    })
    try:
        data = json.loads(get(api, timeout=30))
    except Exception:
        return None
    pages = (data.get('query') or {}).get('pages') or {}
    best = None
    for p in pages.values():
        info = (p.get('imageinfo') or [{}])[0]
        mime = info.get('mime') or ''
        if not mime.startswith('image/') or 'svg' in mime:
            continue
        if (info.get('width') or 0) < 400 or not info.get('thumburl'):
            continue
        meta = info.get('extmetadata') or {}
        lic = (meta.get('LicenseShortName') or {}).get('value') or ''
        lic_l = lic.lower()
        if any(x in lic_l for x in ('non-commercial', 'nc', 'all rights reserved', 'fair use', 'no restrictions unknown')):
            continue
        if not any(x in lic_l for x in ('public domain', 'cc0', 'cc by', 'attribution', 'gfdl')):
            continue
        title = p.get('title') or ''
        desc = re.sub(r'<[^>]+>', ' ', (meta.get('ImageDescription') or {}).get('value') or '')
        artist = re.sub(r'<[^>]+>', ' ', (meta.get('Artist') or {}).get('value') or '')
        artist = re.sub(r'\s+', ' ', html.unescape(artist)).strip() or 'Wikimedia Commons'
        if not relevant(title, desc, need):
            continue
        sc = score_text(title, desc)
        if best is None or sc > best['score']:
            page = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_'))
            kind = 'render' if re.search(r'render|illustrat|artist|impression|concept', title + ' ' + desc, re.I) else 'photo'
            word = 'Rendering' if kind == 'render' else 'Photo'
            best = dict(score=sc, title=title, href=info['thumburl'], page=page, where='commons', kind=kind,
                        credit=f'{word}: {artist}, via Wikimedia Commons ({lic}).')
    if not best or best['score'] < 1:
        return None
    return best


# Hand-checked Wikimedia files (or one NASA URL) so markers are the spacecraft, not a data map.
MANUAL = {
    's2c': 'File:Sentinel 2-IMG 5873-white (crop).jpg',
    's1c': 'File:Sentinel 1-IMG 5874-white.jpg',
    's3b': 'File:EUMETSAT – Model of Sentinel-3.jpg',
    's5p': 'File:Sentinel 5P model.jpg',
    'smap': 'File:SMAP spacecraft model.png',
    'carruthers': 'File:Carruthers Geocorona Observatory Images (SVS14830 - 24-22101-Carruthers SpaceVehicleComplete-Edited).jpg',
    'oco2': 'File:Orbiting Carbon Observatory spacecraft model.png',
    'icesat2': 'File:ICESat-2 spacecraft model.png',
    'gcomw': 'File:GCOM-W1 satellite.png',
    'gosatgw': 'File:GOSAT-GW-scalemodel02-atJAXATsukubaSpaceDome20250607.jpg',
    'eos06': 'File:PSLV-C54, EOS-6 (aka Oceansat-3) - Oceansat-3 on PSLV fourth stage.webp',
    'cryosat': 'File:CryoSat model ESA384323.jpg',
    'galileo': 'File:Galileo satellite in LEAF for acoustic testing ESA295941.jpg',
    'goes19': 'File:GOES-U Satellite EMI-EMC Testing (53187216386).jpg',
    'insat': 'File:INSAT-3DS Satellite.jpg',
    'mtgs': 'File:Sentinel-4 on MTG-S ESA24700249.jpeg',
    'metop': 'File:MetOp-SG-A satellite from below ESA511183.jpg',
    'mev': 'File:Mev render.jpg',
    'dscovr': 'File:Deep Space Climate Observatory (DSCOVR).jpg',
    'aditya': 'File:Aditya-L1 spacecraft.jpg',
    'webb': 'File:James Webb Space Telescope Mirror37.jpg',
    'otter': 'File:Starfish Space - Otter Pup.png',
}
MANUAL_URL = {
    'emit': dict(href='http://images-assets.nasa.gov/image/PIA25148/PIA25148~medium.jpg',
                 credit='Photo: NASA (PIA25148). EMIT being loaded into a Falcon 9 trunk.',
                 page='https://images.nasa.gov/details/PIA25148', kind='photo', title='EMIT loaded into a Falcon 9 trunk'),
}
# No free photo or official realistic rendering turned up. Left off instead of using a data map, logo, or the wrong vehicle.
DROP = {
    'gcomc': 'GCOM-C.html',
    'rcm': 'RCM.html',
    'neossat': 'NEOSSat.html',
    'firesat': 'FireSat.html',
    'gedi': 'GEDI.html',
    'tempo': 'TEMPO.html',
    'co2m': 'CO2M.html',
    'libera': 'Libera.html',
    'clearspace': 'ClearSpace.html',
    'vigil': 'Vigil.html',
    'forum': 'FORUM.html',
    'usdv': 'US_Deorbit_Vehicle.html',
}


def commons_file(title):
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'titles': title, 'prop': 'imageinfo',
        'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': 900,
    })
    data = json.loads(get(api, timeout=40))
    pages = (data.get('query') or {}).get('pages') or {}
    page = next(iter(pages.values()))
    info = (page.get('imageinfo') or [None])[0]
    if not info or not info.get('thumburl') and not info.get('url'):
        raise RuntimeError('missing ' + title)
    meta = info.get('extmetadata') or {}
    lic = re.sub(r'<[^>]+>', '', (meta.get('LicenseShortName') or {}).get('value') or '')
    lic_l = lic.lower()
    if any(x in lic_l for x in ('non-commercial', 'all rights reserved', 'fair use')) or re.search(r'\bnc\b', lic_l):
        raise RuntimeError('license not reusable: ' + lic)
    if not any(x in lic_l for x in ('public domain', 'cc0', 'cc by', 'attribution', 'gfdl', 'godl')):
        raise RuntimeError('unrecognized license: ' + lic + ' for ' + title)
    artist = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', (meta.get('Artist') or {}).get('value') or ''))).strip() or 'Wikimedia Commons'
    kind = 'render' if re.search(r'render|illustrat|artist|impression|concept|model', title, re.I) else 'photo'
    word = 'Rendering' if kind == 'render' else 'Photo'
    href = info.get('thumburl') or info.get('url')
    page_url = info.get('descriptionurl') or ('https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')))
    return dict(href=href, credit=f'{word}: {artist}, via Wikimedia Commons ({lic}).', kind=kind, page=page_url, title=title, score=10)


def pick_image(sat):
    if sat['id'] in MANUAL_URL:
        spec = MANUAL_URL[sat['id']]
        blob = get(spec['href'], timeout=60)
        return dict(raw=blob, credit=spec['credit'], kind=spec['kind'], page=spec['page'], alt=spec['title'], where='nasa', title=spec['title'], score=10)
    if sat['id'] in MANUAL:
        remote = commons_file(MANUAL[sat['id']])
        blob = get(remote['href'], timeout=60)
        return dict(raw=blob, credit=remote['credit'], kind=remote['kind'], page=remote['page'], alt=remote['title'].replace('File:', ''), where='commons', title=remote['title'], score=10)
    need = sat.get('need') or [sat['label']]
    remote = None
    order = (nasa_candidate, commons_candidate) if sat.get('prefer') != 'commons' else (commons_candidate, nasa_candidate)
    for q in (sat['q'], sat['label'] + ' spacecraft'):
        for finder in order:
            found = finder(q, need)
            if found and (remote is None or found['score'] > remote['score']):
                remote = found
            if remote and remote['score'] >= 6:
                break
        if remote and remote['score'] >= 6:
            break
        time.sleep(0.1)
    local = LOCAL.get(sat['id'])
    if local and (not remote or remote['score'] < 6):
        return dict(raw=(ROOT / local[0]).read_bytes(), credit=local[1], kind=local[2], page=local[3], alt=local[4], where='repo', title=local[0])
    if not remote:
        if local:
            return dict(raw=(ROOT / local[0]).read_bytes(), credit=local[1], kind=local[2], page=local[3], alt=local[4], where='repo', title=local[0])
        raise RuntimeError(f'No image for {sat["id"]}')
    blob = get(remote['href'], timeout=60)
    alt = remote['title'].replace('File:', '')
    return dict(raw=blob, credit=remote['credit'], kind=remote['kind'], page=remote['page'], alt=alt, where=remote['where'], title=remote['title'], score=remote['score'])


def to_images(raw):
    im = Image.open(BytesIO(raw)).convert('RGB')
    card = im.copy()
    card.thumbnail((640, 420), Image.Resampling.LANCZOS)
    side = 160
    sc = max(side / im.width, side / im.height)
    thumb = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.Resampling.LANCZOS)
    left = max(0, (thumb.width - side) // 2)
    top = max(0, (thumb.height - side) // 2)
    thumb = thumb.crop((left, top, left + side, top + side))
    return card, thumb


def save_webp(im, path, quality):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, 'WEBP', quality=quality, method=6)


def credit_html(text, page):
    safe = html.escape(text)
    if page:
        return safe + ' <a href="' + html.escape(page, quote=True) + '" rel="noopener" target="_blank">Source</a>'
    return safe


def fallback(sat, index):
    if sat.get('approx'):
        a = dict(sat['approx'])
        a.setdefault('phase', round(index * 0.65, 3))
        a.setdefault('raan', (index * 47) % 360)
        return a
    base = {
        'sso': dict(altKm=720, inc=98.1, periodMin=99),
        'leo': dict(altKm=550, inc=70, periodMin=96),
        'meo': dict(altKm=23222, inc=56, periodMin=845),
        'geo': dict(altKm=35786, inc=0, periodMin=1436, fixed=True, lon=-40 + (index % 12) * 12),
    }[sat['regime']]
    base['phase'] = round(index * 0.55, 3)
    base['raan'] = (index * 37) % 360
    return base


def source_text(sat, tle_name):
    if sat.get('source'):
        return sat['source']
    extra = (' ' + sat['extra']) if sat.get('extra') else ''
    return (f"Orbit source: CelesTrak public two-line elements for NORAD {sat['norad']} ({tle_name}), "
            f"propagated in the browser with satellite.js. A copy saved on {TODAY} is used if CelesTrak does not answer.{extra}")


def build_page(rows):
    wm = (ROOT / 'World_Map.html').read_text(encoding='utf8')
    head, rest = wm.split('</head>', 1)
    desc = 'Coming soon: a draft 3D Earth map of satellite solutions already on Saving Planets, placed in low, sun-synchronous, medium, geostationary, and Lagrange orbits.'
    head = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex">', head)
    head = re.sub(r'<title>.*?</title>', '<title>Space Map (Coming Soon) | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc, quote=True) + '"', head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc, quote=True) + '"', head)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc, quote=True) + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', r'\1Space Map (Coming Soon) | Saving Planets"', head)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*"', r'\1Space Map (Coming Soon) | Saving Planets"', head)
    head = re.sub(r'(<meta name="keywords" content=")[^"]*"', r'\1Space Map, satellites, Earth orbit, LEO, sun-synchronous, geostationary"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://www.savingplanets.com/Space_Map.html">', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*"', r'\1https://www.savingplanets.com/Space_Map.html"', head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*"', r'\1https://www.savingplanets.com/assets/space-map/earth.webp"', head)
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1NASA Blue Marble photograph of Earth"', head)
    head = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', r'\1https://www.savingplanets.com/assets/space-map/earth.webp"', head)
    head = re.sub(r'\n?<link rel="stylesheet" href="assets/leaflet/leaflet.css[^"]*">', '', head)
    head = re.sub(r'\n?<link rel="stylesheet" href="map.css[^"]*">', '', head)
    head = re.sub(r'<!-- PMASCOTH:START -->.*?<!-- PMASCOTH:END -->', '', head, flags=re.S)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head += '\n<!-- DRAFT Space Map: noindex, not in the nav, sitemap, or homepage. -->\n<link rel="stylesheet" href="space-map.css?v=20261109b">\n'
    legend = '''<ul class="sm-legend" aria-label="Orbit types">
<li><button type="button" data-regime="leo" aria-pressed="true" class="is-on"><i class="sm-swatch" style="--c:#3DDC97" aria-hidden="true"></i><span><strong>Low Earth orbit</strong> A few hundred kilometers up. A loop around Earth takes about 90 minutes. The space station is here.</span></button></li>
<li><button type="button" data-regime="sso" aria-pressed="true" class="is-on"><i class="sm-swatch" style="--c:#4CC3FF" aria-hidden="true"></i><span><strong>Sun-synchronous</strong> A special low orbit that passes a place at the same local time each day, so pictures have matching sunlight. Most Earth-watching satellites use it.</span></button></li>
<li><button type="button" data-regime="meo" aria-pressed="true" class="is-on"><i class="sm-swatch" style="--c:#FFD166" aria-hidden="true"></i><span><strong>Medium Earth orbit</strong> Much higher. Navigation satellites such as Galileo live here and take roughly half a day to circle Earth.</span></button></li>
<li><button type="button" data-regime="geo" aria-pressed="true" class="is-on"><i class="sm-swatch" style="--c:#FF7A59" aria-hidden="true"></i><span><strong>Geostationary</strong> About 36,000 km up. The satellite matches Earth’s spin, so it stays over one spot. Weather satellites that stare at a region use it.</span></button></li>
<li><button type="button" data-regime="beyond" aria-pressed="true" class="is-on"><i class="sm-swatch" style="--c:#C9A0FF" aria-hidden="true"></i><span><strong>Beyond: L1, L2, L5</strong> Parking spots about 1.5 million km from Earth, toward the Sun, away from it, or along Earth’s path. Drawn closer than real life so you can still see Earth.</span></button></li>
</ul>'''
    main = f'''<main id="main" class="sm-main">
<div class="sm-soon" role="status"><span class="sm-soon-badge">Coming Soon</span><p>This Space Map is a draft. It shows satellite solutions already on Saving Planets. It will grow, and it is not in the main menu yet.</p></div>
<div class="sm-screen">
<h1 class="sm-title">Space Map</h1>
<p class="sm-lead">Tap a satellite to open its solution card. Low, sun-synchronous, medium, and geostationary orbits are drawn to scale with Earth. A gold ≈ means the place is approximate.</p>
<div class="sm-view" id="sm-view">
<canvas id="sm-canvas" class="sm-canvas" aria-hidden="true"></canvas>
<div id="sm-markers" class="sm-markers"></div>
<div class="sm-ctrl" role="group" aria-label="Earth view">
<button type="button" id="sm-zin" aria-label="Zoom in">+</button>
<button type="button" id="sm-zout" aria-label="Zoom out">−</button>
<button type="button" id="sm-reset">Reset</button>
</div>
<p id="sm-status" class="sm-status" aria-live="polite">Loading the globe…</p>
<p class="sm-credit">Earth image: NASA Goddard Space Flight Center, Blue Marble. Public domain. <a href="https://commons.wikimedia.org/wiki/File:Land_ocean_ice_cloud_hires.jpg">Source</a></p>
</div>
<div class="sm-still">
<img src="assets/space-map/earth.webp" width="2048" height="1024" alt="NASA Blue Marble photograph of Earth, a flat map of land, ocean, ice, and clouds">
<p>Motion is turned off. The table below lists the same satellites, with links to their solution pages.</p>
</div>
<p class="sm-hint">Drag to turn Earth. Scroll or pinch to zoom. Tap a picture to open that solution.</p>
{legend}
<p class="sm-scale">Orbits near Earth are to scale. L1, L2, and L5 are not: those spacecraft are about 1.5 million kilometers away, dozens of times farther than geostationary orbit.</p>
</div>
<section class="sm-list" id="satellite-list" aria-labelledby="sm-list-h">
<h2 id="sm-list-h">Satellites on this map</h2>
<p>The same satellites as the globe, for keyboards and screen readers. Where a page covers a whole fleet, one satellite stands in for it. The card says which one.</p>
<div class="sm-table-wrap"><table class="sm-table"><caption>Satellite solutions, the orbit they are drawn in, and how that place was chosen.</caption>
<thead><tr><th scope="col">Satellite</th><th scope="col">Orbit</th><th scope="col">How it is placed</th><th scope="col">Picture</th></tr></thead>
<tbody>
{rows}
</tbody></table></div>
</section>
<div id="sm-app" data-src="assets/data/space-map.json?v=20261109a" data-lib="assets/space-map/vendor/" hidden></div>
<dialog id="sm-dialog" aria-label="Solution card"></dialog>
</main>'''
    rest = re.sub(r'<main id="main".*?</main>', main, rest, count=1, flags=re.S)
    rest = rest.replace('world-map-page', 'space-map-page')
    rest = re.sub(r'data-glass="[^"]*"', 'data-glass="space"', rest, count=1)
    rest = rest.replace('href="World_Map.html"', 'href="Space_Map.html"')
    for lang in ('fr', 'es', 'ar', 'it', 'he'):
        rest = rest.replace(f'href="{lang}/World_Map.html"', f'href="{lang}/index.html"')
    rest = rest.replace(' aria-current="page"', '')
    rest = rest.replace(' is-current', '')
    rest = re.sub(r'<script src="polar-mascots\.js[^"]*" defer></script>', '', rest)
    rest = re.sub(r'<script src="assets/leaflet/leaflet\.js[^"]*" defer></script>', '', rest)
    rest = re.sub(r'<script src="map\.js[^"]*" defer></script>', '', rest)
    rest = rest.replace('</body>', '<script src="space-map.js?v=20261109a" defer></script></body>', 1)
    (ROOT / 'Space_Map.html').write_text(head + '</head>' + rest, encoding='utf8')


def vendor():
    dest = ROOT / 'assets/space-map/vendor'
    dest.mkdir(parents=True, exist_ok=True)
    files = {
        'three.min.js': 'https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js',
        'satellite.min.js': 'https://cdn.jsdelivr.net/npm/satellite.js@4.1.4/dist/satellite.min.js',
    }
    for name, url in files.items():
        if (dest / name).exists() and (dest / name).stat().st_size > 20000:
            print('keep', name)
            continue
        blob = get(url, timeout=60)
        if name.startswith('three') and (len(blob) < 400000 or b'THREE' not in blob[:2000] and b'WebGLRenderer' not in blob):
            raise SystemExit(f'unexpected three.js download ({len(blob)} bytes)')
        if name.startswith('satellite') and b'twoline2satrec' not in blob:
            raise SystemExit('satellite.js is missing twoline2satrec')
        (dest / name).write_bytes(blob)
        print(name, len(blob))


NEED = {
    'landsat9': ['landsat 9', 'landsat-9'],
    's2c': ['sentinel-2', 'sentinel 2'],
    's1c': ['sentinel-1', 'sentinel 1'],
    's3b': ['sentinel-3', 'sentinel 3'],
    's5p': ['sentinel-5', 'tropomi'],
    's6b': ['sentinel-6', 'sentinel 6'],
    'oco2': ['oco-2', 'oco 2', 'orbiting carbon'],
    'smap': ['smap'],
    'pace': ['pace'],
    'swot': ['swot'],
    'icesat2': ['icesat'],
    'gracefo': ['grace-fo', 'grace fo', 'grace follow'],
    'nisar': ['nisar'],
    'earthcare': ['earthcare', 'earth care'],
    'noaa21': ['noaa-21', 'noaa 21', 'jpss-2', 'jpss 2'],
    'gcomc': ['shikisai', 'gcom-c', 'gcom c'],
    'gcomw': ['shizuku', 'gcom-w', 'gcom w'],
    'gosatgw': ['gosat-gw', 'gosat gw', 'ibuki'],
    'eos06': ['oceansat', 'eos-06', 'eos-6'],
    'alos4': ['alos-4', 'alos 4', 'daichi-4', 'daichi 4'],
    'biomass': ['biomass'],
    'tanager': ['tanager'],
    'cryosat': ['cryosat'],
    'aws': ['arctic weather'],
    'rcm': ['radarsat', 'rcm'],
    'neossat': ['neossat'],
    'scisat': ['scisat'],
    'prefire': ['prefire'],
    'adras': ['adras'],
    'punch': ['punch'],
    'tracers': ['tracers'],
    'hydro': ['hydrognss', 'hydro gnss'],
    'firesat': ['firesat', 'fire sat'],
    'gedi': ['gedi'],
    'emit': ['emit'],
    'galileo': ['galileo'],
    'goes19': ['goes-19', 'goes 19', 'goes-u', 'goes u'],
    'insat': ['insat-3ds', 'insat 3ds'],
    'mtgi': ['mtg-i', 'meteosat third', 'meteosat-12'],
    'mtgs': ['mtg-s', 'sentinel-4', 'sentinel 4'],
    'tempo': ['tempo'],
    'mev': ['mev-2', 'mev 2', 'mission extension'],
    'metop': ['metop'],
    'aeolus': ['aeolus'],
    'dscovr': ['dscovr'],
    'aditya': ['aditya'],
    'soho': ['soho'],
    'imap': ['imap'],
    'carruthers': ['carruthers', 'geocorona'],
    'webb': ['webb', 'jwst'],
    'neosurveyor': ['neo surveyor', 'neosurveyor'],
    'vigil': ['vigil'],
    'co2m': ['co2m', 'carbon dioxide monitoring'],
    'geoxo': ['geoxo'],
    'forum': ['forum'],
    'libera': ['libera'],
    'clearspace': ['clearspace'],
    'lignosat': ['lignosat', 'wooden satellite'],
    'otter': ['otter', 'starfish'],
    'usdv': ['deorbit'],
}
COMMONS_FIRST = {'s2c', 's1c', 's3b', 's5p', 'earthcare', 'gcomc', 'gcomw', 'gosatgw', 'eos06', 'alos4', 'biomass', 'cryosat', 'aws', 'rcm', 'neossat', 'scisat', 'hydro', 'galileo', 'insat', 'mtgi', 'mtgs', 'metop', 'aeolus', 'aditya', 'soho', 'vigil', 'co2m', 'forum', 'clearspace', 'lignosat'}


def earth():
    path = ROOT / 'assets/space-map/earth.webp'
    if path.exists() and path.stat().st_size > 80000:
        print('keep earth', path.stat().st_size)
        return
    url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Land_ocean_ice_cloud_hires.jpg/1920px-Land_ocean_ice_cloud_hires.jpg'
    im = Image.open(BytesIO(get(url, timeout=60))).convert('RGB')
    im.thumbnail((2048, 1024), Image.Resampling.LANCZOS)
    path = ROOT / 'assets/space-map/earth.webp'
    save_webp(im, path, 76)
    print('earth', path.stat().st_size, im.size)


MATCH_URL = 'https://www.globe.gov/ground-to-satellite/connecting-globe-to-satellite-data'
MISSION_URL = 'https://www.globe.gov/ground-to-satellite/nasa-mission-connections'

def globe_note(text, links):
    bits = ' · '.join(f'<a href="{href}" rel="noopener" target="_blank">{html.escape(label)}</a>' for href, label in links)
    label = 'Sources: ' if len(links) > 1 else 'Source: '
    return 'GLOBE ground link: ' + html.escape(text) + ' ' + label + bits

# Official GLOBE wording only (satellite match page and NASA Mission Connections), checked 10 Nov 2026.
GLOBE_NOTES = {
    'pace': globe_note(
        'GLOBE Clouds observations are matched to this satellite. GLOBE volunteers can support PACE science by observing clouds when PACE is overhead.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data'), (MISSION_URL, 'NASA Mission Connections')]),
    'goes19': globe_note(
        'GLOBE Clouds observations are matched to GOES. This card is GOES-19.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data')]),
    'mtgi': globe_note(
        'GLOBE Clouds observations are matched to Meteosat. This card is MTG-I1, a Meteosat Third Generation satellite.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data')]),
    'landsat9': globe_note(
        'GLOBE Land Cover observations are matched to Landsat 8 and 9. Volunteers who submit land cover data are emailed the closest-in-time Landsat and Sentinel-2 observation.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data'), (MISSION_URL, 'NASA Mission Connections')]),
    's2c': globe_note(
        'GLOBE Land Cover observations are matched to Sentinel-2.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data')]),
    'noaa21': globe_note(
        'GLOBE matches Clouds observations to NOAA-20, part of the Joint Polar Satellite System. This card shows NOAA-21, which stands in for that system on this map.',
        [(MATCH_URL, 'Connecting GLOBE to Satellite Data'), (MISSION_URL, 'NASA Mission Connections')]),
    'nisar': globe_note(
        'GLOBE volunteers can contribute to NISAR studies of agriculture and snow through the Land Cover protocol.',
        [(MISSION_URL, 'NASA Mission Connections')]),
    'swot': globe_note(
        'GLOBE volunteers can participate in SWOT science by observing land cover and lake levels.',
        [(MISSION_URL, 'NASA Mission Connections')]),
    'emit': globe_note(
        'GLOBE volunteers can support EMIT science by documenting snow color using the Land Cover protocol. Observations of agriculture using that protocol may also be useful.',
        [(MISSION_URL, 'NASA Mission Connections')]),
}

def with_globe(entry, sat_id):
    note = GLOBE_NOTES.get(sat_id)
    if not note:
        return entry
    entry = dict(entry)
    entry['globeHtml'] = note
    return entry

def main():
    global SATS
    dropped_pages = sorted(DROP.values())
    SATS = [s for s in SATS if s['id'] not in DROP]
    SKIPPED.append({'group': 'No usable free spacecraft image in this pass',
                    'why': 'Left off the draft rather than show a data map, a logo, or a picture of a different vehicle. Add one in MANUAL when a free official photo or realistic rendering is found.',
                    'pages': dropped_pages})
    os_cards = cards()
    missing = [s['page'] for s in SATS if s['page'] not in os_cards]
    if missing:
        raise SystemExit('Missing solution cards: ' + ', '.join(missing))
    vendor()
    earth()
    out_dir = ROOT / 'assets/space-map/sats'
    cache_path = ROOT / 'assets/data/space-map-build-cache.json'
    cache = json.loads(cache_path.read_text(encoding='utf8')) if cache_path.exists() else {}
    sats_json = []
    sheet = []
    failed = []
    for i, sat in enumerate(SATS):
        print('---', sat['id'], flush=True)
        if sat['id'] in cache and (out_dir / f"{sat['id']}-thumb.webp").exists():
            sats_json.append(with_globe(cache[sat['id']], sat['id']))
            sheet.append((Image.open(out_dir / f"{sat['id']}-thumb.webp"), sat['id']))
            print(' cached')
            continue
        try:
            sat = dict(sat)
            sat['need'] = NEED[sat['id']]
            if sat['id'] in COMMONS_FIRST:
                sat['prefer'] = 'commons'
            tle_name, tle = None, None
            if sat.get('norad'):
                tle_name, l1, l2 = fetch_tle(sat['norad'], sat['expect'])
                tle = [l1, l2]
                time.sleep(0.15)
                print(' tle', tle_name)
            img = pick_image(sat)
            card, thumb = to_images(img['raw'])
            save_webp(card, out_dir / f"{sat['id']}.webp", 72)
            save_webp(thumb, out_dir / f"{sat['id']}-thumb.webp", 70)
            card_meta = os_cards[sat['page']]
            kind_word = 'Rendering' if img['kind'] == 'render' else 'Photo'
            alt = f"{sat['label']} — {kind_word.lower()} of the spacecraft. {img['alt']}"
            entry = dict(
                id=sat['id'], label=sat['label'], page=sat['page'], pageName=card_meta['name'], desc=card_meta['desc'],
                status=card_meta['status'], regime=sat['regime'], regimeName=REGIME[sat['regime']], color=COLOR[sat['regime']],
                norad=sat.get('norad'), object=tle_name, tle=tle, approx=not sat.get('norad'),
                fallback=fallback(sat, i), nudge=sat.get('nudge', 0),
                source=source_text(sat, tle_name),
                img=f"assets/space-map/sats/{sat['id']}.webp",
                thumb=f"assets/space-map/sats/{sat['id']}-thumb.webp",
                alt=alt, credit=img['credit'], creditHtml=credit_html(img['credit'], img.get('page')),
                imageKind=img['kind'], imagePage=img.get('page'), imageTitle=img.get('title'),
            )
            entry = with_globe(entry, sat['id'])
            cache[sat['id']] = entry
            cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf8')
            sats_json.append(entry)
            sheet.append((thumb, sat['id']))
            print(' img', img['where'], str(img.get('title', ''))[:80], 'score', img.get('score'), flush=True)
        except Exception as e:
            failed.append((sat['id'], str(e)))
            print(' FAIL', sat['id'], e, flush=True)
    data = dict(
        generated=TODAY,
        earth=dict(src='assets/space-map/earth.webp', credit='NASA Goddard Space Flight Center, Blue Marble. Public domain.',
                   source='https://commons.wikimedia.org/wiki/File:Land_ocean_ice_cloud_hires.jpg'),
        note='Draft Space Map. Extend SATS in scripts/build-space-map.py. Not in the nav, sitemap, or homepage.',
        sats=sats_json, skipped=SKIPPED,
    )
    path = ROOT / 'assets/data/space-map.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf8')
    rows = []
    for s in sats_json:
        how = f"CelesTrak TLE, NORAD {s['norad']}" if s['norad'] else 'Approximate — see the card'
        pic = 'Official rendering' if s['imageKind'] == 'render' else 'Photo'
        rows.append(
            '<tr><th scope="row"><a href="{page}">{label}</a></th><td>{regime}</td><td>{how}</td>'
            '<td>{pic}. <button type="button" data-sm-open="{id}">Show card</button></td></tr>'.format(
                page=html.escape(s['page']), label=html.escape(s['label']), regime=html.escape(s['regimeName']),
                how=html.escape(how), pic=pic, id=html.escape(s['id'])))
    build_page('\n'.join(rows))
    if not sheet:
        print('FAILED', failed)
        raise SystemExit(1)
    # contact sheet for review
    cols = 8
    cell, cap = 150, 28
    rows_n = (len(sheet) + cols - 1) // cols
    board = Image.new('RGB', (cols * cell, rows_n * (cell + cap)), (10, 16, 28))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(board)
    for n, (im, name) in enumerate(sheet):
        r, c = divmod(n, cols)
        small = im.resize((cell - 8, cell - 8))
        board.paste(small, (c * cell + 4, r * (cell + cap) + 2))
        draw.text((c * cell + 4, r * (cell + cap) + cell - 6), name[:18], fill=(255, 255, 255))
    if sheet:
        board.save('/tmp/space-map-sheet.jpg', quality=80)
    print('sats', len(sats_json), 'json', path.stat().st_size)
    if failed:
        print('FAILED', failed)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
