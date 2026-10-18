"""Daily Roman data (run from weekly-sync.sh). Writes assets/data/roman.json:
- distance from Earth: JPL Horizons (NASA/JPL), spacecraft -211, geocentric range 'delta' at 00:00 UTC today. Webb (-170) for comparison.
- newest NASA image: NASA Image and Video Library search 'Roman Space Telescope' (newest date_created).
Also refreshes the static fallback between <!-- ROMAN-LIVE:START/END --> in Nancy_Grace_Roman.html.
Oct 18: the newest image is saved as assets/roman-latest.jpg (NASA public domain thumb, saved byte-for-byte) and written into the page
between <!-- ROMAN-IMG:START/END --> with loading=eager, so the box never shows blank while waiting on images-assets.nasa.gov or roman.js.
Network failure: keeps the previous JSON (never invents a value)."""
import json, os, re, urllib.request, urllib.parse, datetime
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/data/roman.json'; PAGE = 'Nancy_Grace_Roman.html'; AU = 149597870.7
old = json.load(open(OUT)) if os.path.exists(OUT) else {}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'savingplanets-sync'}), timeout=40).read().decode()
def horizons(cmd, day):
    nxt = (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()
    q = urllib.parse.urlencode({'format': 'json', 'COMMAND': f"'{cmd}'", 'EPHEM_TYPE': 'OBSERVER', 'CENTER': "'500@399'",
        'START_TIME': f"'{day}'", 'STOP_TIME': f"'{nxt}'", 'STEP_SIZE': "'1d'", 'QUANTITIES': "'20'"})
    r = json.loads(get('https://ssd.jpl.nasa.gov/api/horizons.api?' + q))['result']
    m = re.search(r'\$\$SOE\s*\n\s*(\S+ \S+)\s+([\d.]+)', r)
    if not m: raise ValueError('no ephemeris')
    return float(m.group(2)) * AU
day = datetime.datetime.now(datetime.timezone.utc).date().isoformat(); d = dict(old)
try:
    km = horizons('-211', day); d['distance'] = {'date': day, 'km': round(km), 'mi': round(km / 1.609344),
        'source': 'NASA/JPL Horizons (spacecraft -211)', 'url': 'https://ssd.jpl.nasa.gov/horizons/app.html'}
    try: d['webb_km'] = round(horizons('-170', day))
    except Exception: pass
except Exception as e: print('roman: Horizons failed, kept previous:', e)
try:
    items = json.loads(get('https://images-api.nasa.gov/search?' + urllib.parse.urlencode({'q': 'Roman Space Telescope', 'media_type': 'image'})))['collection']['items']
    items = [i for i in items if 'Roman' in i['data'][0].get('title', '')]
    i = max(items, key=lambda i: (i['data'][0].get('date_created', ''), i['data'][0]['nasa_id']))
    x = i['data'][0]; thumb = next((l['href'] for l in i.get('links', []) if l.get('rel') == 'preview'), '')
    d['image'] = {'nasa_id': x['nasa_id'], 'title': x['title'].strip(), 'date': x['date_created'][:10],
        'credit': (x.get('photographer') or x.get('secondary_creator') or 'NASA').strip(), 'thumb': thumb.replace('http://', 'https://'),
        'url': 'https://images.nasa.gov/details/' + x['nasa_id']}
except Exception as e: print('roman: NASA Images failed, kept previous:', e)
IMG = 'assets/roman-latest.jpg'
if d.get('image', {}).get('thumb') and (d['image'].get('local_id') != d['image']['nasa_id'] or not os.path.exists(IMG)):
    try:
        b = urllib.request.urlopen(urllib.request.Request(d['image']['thumb'], headers={'User-Agent': 'Mozilla/5.0 (savingplanets-sync)'}), timeout=40).read()
        if b[:3] == b'\xff\xd8\xff': open(IMG, 'wb').write(b); d['image']['local_id'] = d['image']['nasa_id']
    except Exception as e: print('roman: image download failed, kept previous:', e)
d['updated'] = day
if d != old:
    json.dump(d, open(OUT, 'w'), indent=1, ensure_ascii=False); open(OUT, 'a').write('\n')
if os.path.exists(PAGE) and 'distance' in d:
    s = open(PAGE, encoding='utf8').read(); dist = d['distance']
    dt = datetime.date.fromisoformat(dist['date']); lab = dt.strftime('%B ') + str(dt.day) + dt.strftime(', %Y')
    blk = (f'<!-- ROMAN-LIVE:START --><p class="roman-big"><span id="roman-km">{dist["km"]:,}</span> km</p>'
           f'<p class="roman-sub">about <span id="roman-mi">{dist["mi"]:,}</span> miles from Earth, as of <span id="roman-asof">{lab}</span> (00:00 UTC)</p><!-- ROMAN-LIVE:END -->')
    n = re.sub(r'<!-- ROMAN-LIVE:START -->.*?<!-- ROMAN-LIVE:END -->', blk, s, flags=re.S)
    im = d.get('image') or {}
    if im.get('local_id') and os.path.exists(IMG):
        from html import escape as E
        fig = (f'<!-- ROMAN-IMG:START --><figure id="roman-latest"><a href="{E(im["url"])}" target="_blank" rel="noreferrer">'
               f'<img id="roman-latest-img" src="{IMG}?v={E(im["local_id"])}" data-id="{E(im["local_id"])}" alt="Newest Roman photo in NASA\'s image library" width="640" height="427" loading="eager" decoding="async"></a>'
               f'<figcaption>Newest Roman photo in NASA\'s image library: <span id="roman-latest-title">{E(im["title"])}</span> (<span id="roman-latest-date">{E(im["date"])}</span>). '
               f'Credit: <span id="roman-latest-credit">{E(im["credit"])}</span>.</figcaption></figure><!-- ROMAN-IMG:END -->')
        n = re.sub(r'<!-- ROMAN-IMG:START -->.*?<!-- ROMAN-IMG:END -->', lambda _: fig, n, flags=re.S)
    if n != s: open(PAGE, 'w', encoding='utf8').write(n)
print('roman:', d.get('distance', {}).get('km'), 'km;', d.get('image', {}).get('nasa_id'))
