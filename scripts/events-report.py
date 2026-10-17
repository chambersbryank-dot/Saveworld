#!/usr/bin/env python3
"""Oct 16 2026: private weekly summary of the aggregate events (Workers Analytics Engine dataset sp_events).
Runs on the box only (needs /home/box/.cloudflare_token with Account Analytics read). Nothing is published.
Usage: python3 scripts/events-report.py [days=7] [--out FILE]   (default output: ~/reports/events-YYYY-MM-DD.md)
Columns: blob1=event, blob2=language, blob3..5=event fields (see workers/si-helper/src/index.js EV). Counts use _sample_interval."""
import sys, os, json, urllib.request, urllib.error, datetime
days = int(next((a for a in sys.argv[1:] if a.isdigit()), '7'))
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.expanduser(f'~/reports/events-{datetime.date.today()}.md')
T = open('/home/box/.cloudflare_token').read().strip(); A = open('/home/box/.cloudflare_account_id').read().strip()
def q(sql):
    r = urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{A}/analytics_engine/sql', data=sql.encode(), method='POST', headers={'Authorization': 'Bearer ' + T})
    try: return json.loads(urllib.request.urlopen(r, timeout=60).read())['data']
    except urllib.error.HTTPError as e: sys.exit(f'Analytics Engine SQL API error {e.code}: {e.read()[:300].decode(errors="replace")}')
W = f"timestamp > NOW() - INTERVAL '{days}' DAY"
SECTIONS = [
 ('Lab tool usage (sessions that used a lab)', "SELECT blob3 AS tool, blob2 AS lang, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='lab' AND {w} GROUP BY tool, lang ORDER BY n DESC"),
 ('Learn page views', "SELECT blob3 AS track, blob4 AS kind, blob2 AS lang, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='learn' AND {w} GROUP BY track, kind, lang ORDER BY n DESC"),
 ('Practice problems (attempts / correct)', "SELECT blob3 AS track, blob5 AS topic, blob4 AS result, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='practice' AND {w} GROUP BY track, topic, result ORDER BY track, topic, result"),
 ('SI Helper questions by outcome', "SELECT blob3 AS outcome, blob2 AS lang, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='si' AND {w} GROUP BY outcome, lang ORDER BY n DESC"),
 ('Newsletter sign-ups (successful submits)', "SELECT blob2 AS lang, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='newsletter' AND {w} GROUP BY lang ORDER BY n DESC"),
 ('Share buttons (Learn and Teachers pages)', "SELECT blob3 AS kind, blob4 AS page, blob2 AS lang, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='share' AND {w} GROUP BY kind, page, lang ORDER BY n DESC"),
 ('Ways to Help: outbound partner clicks', "SELECT blob3 AS partner, blob4 AS kind, SUM(_sample_interval) AS n FROM sp_events WHERE blob1='partner' AND {w} GROUP BY partner, kind ORDER BY n DESC LIMIT 50"),
]
lines = [f'# Saving Planets events: last {days} days (generated {datetime.datetime.now():%Y-%m-%d %H:%M} HST)', '',
         'Aggregate counts only (no visitors, no IPs, no text). SI outcomes: ok = answered, none = no answer found, unsafe/pii = refused, busy/bot/error = not answered.', '']
for title, sql in SECTIONS:
    rows = q(sql.format(w=W)); lines += [f'## {title}', '']
    if not rows: lines += ['(none)', '']; continue
    cols = list(rows[0].keys()); lines += ['| ' + ' | '.join(cols) + ' |', '|' + '---|' * len(cols)]
    lines += ['| ' + ' | '.join(str(r[c]) for c in cols) + ' |' for r in rows] + ['']
try:  # Oct 16: Cloudflare R2 media usage vs free tier (scripts/r2_usage.py)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import r2_usage; lines += ['', r2_usage.section()]
except Exception as e: lines += ['', f'## Cloudflare R2 usage', '', f'(unavailable: {e})', '']
os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write('\n'.join(lines)); print(out)
