#!/usr/bin/env python3
"""Write data/voyages.json from the NASA/JPL Horizons API.

Each command below is the spacecraft line from Horizons COMMAND='*'.
Kilometers are that response's AU figure times the au= km value in the same
response. A failed query is stored ok:false. Nothing is invented.
"""
import datetime, json, os, re, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'voyages.json')
# destCenter is the Horizons body the range is measured from. None means Earth only.
MISSIONS = [
    {'slug': 'europa-clipper', 'command': '-159', 'destCenter': '500@502', 'destName': 'Europa'},
    {'slug': 'juice', 'command': '-28', 'destCenter': '500@503', 'destName': 'Ganymede'},
    {'slug': 'juno', 'command': '-61', 'destCenter': '500@599', 'destName': 'Jupiter'},
    {'slug': 'psyche', 'command': '-255', 'destCenter': '500@2000016', 'destName': 'Psyche'},
    {'slug': 'lucy', 'command': '-49', 'destCenter': None, 'destName': ''},
    {'slug': 'bepicolombo', 'command': '-121', 'destCenter': '500@199', 'destName': 'Mercury'},
    {'slug': 'hera', 'command': '-91', 'destCenter': '500@20065803', 'destName': 'Didymos'},
    {'slug': 'parker-solar-probe', 'command': '-96', 'destCenter': '500@10', 'destName': 'Sun'},
    {'slug': 'solar-orbiter', 'command': '-144', 'destCenter': '500@10', 'destName': 'Sun'},
    {'slug': 'new-horizons', 'command': '-98', 'destCenter': '500@10', 'destName': 'Sun'},
    {'slug': 'voyager-1', 'command': '-31', 'destCenter': '500@10', 'destName': 'Sun'},
    {'slug': 'voyager-2', 'command': '-32', 'destCenter': '500@10', 'destName': 'Sun'},
]


def day_span():
    start = datetime.datetime.now(datetime.timezone.utc).date()
    stop = start + datetime.timedelta(days=1)
    return start.isoformat(), stop.isoformat()


def fetch(command, center, start, stop):
    q = urllib.parse.urlencode({
        'format': 'text', 'COMMAND': f"'{command}'", 'MAKE_EPHEM': 'YES',
        'EPHEM_TYPE': 'OBSERVER', 'CENTER': f"'{center}'",
        'START_TIME': start, 'STOP_TIME': stop, 'STEP_SIZE': '1 d', 'QUANTITIES': '20',
    })
    req = urllib.request.Request(
        'https://ssd.jpl.nasa.gov/api/horizons.api?' + q,
        headers={'User-Agent': 'SavingPlanets-voyages'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode('utf-8', 'replace')


def au_km(text):
    m = re.search(r'1 au=\s*([0-9.]+)\s*km', text, re.I)
    if not m:
        raise ValueError('Horizons did not state the AU length')
    return float(m.group(1))


def first_delta(text):
    if 'No ephemeris' in text or '$$SOE' not in text:
        raise ValueError('no ephemeris row')
    # Target name must be the spacecraft, not a different body Horizons substituted.
    name = re.search(r'Target body name:\s*([^\n{]+)', text)
    m = re.search(r'\$\$SOE\s+\S+\s+\S+\s+([0-9]+(?:\.[0-9]+)?)', text)
    if not m:
        raise ValueError('no ephemeris row')
    return float(m.group(1)), (name.group(1).strip() if name else '')


def one(m, start, stop):
    row = {'slug': m['slug'], 'horizonsId': m['command'], 'destName': m['destName'],
           'ok': False, 'asOf': start + 'T00:00:00Z'}
    try:
        earth = fetch(m['command'], '500@399', start, stop)
        scale = au_km(earth)
        eau, ename = first_delta(earth)
        row.update(ok=True, auKm=scale, earthAu=eau, earthKm=int(round(eau * scale)), target=ename)
        if m['destCenter']:
            try:
                dest = fetch(m['command'], m['destCenter'], start, stop)
                dau, _ = first_delta(dest)
                row.update(destAu=dau, destKm=int(round(dau * scale)))
            except Exception as e:
                row['destError'] = str(e)[:180]
    except Exception as e:
        row['ok'] = False
        row['error'] = str(e)[:180]
    return row


def main():
    start, stop = day_span()
    missions = {}
    for m in MISSIONS:
        row = one(m, start, stop)
        missions[m['slug']] = row
        print(m['slug'], 'ok' if row['ok'] else 'NO', row.get('target', ''), row.get('earthKm'), row.get('destKm'), row.get('error', ''))
    doc = {'source': 'NASA/JPL Horizons API', 'generated': start + 'T00:00:00Z', 'missions': missions}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
