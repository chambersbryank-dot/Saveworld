#!/usr/bin/env python3
"""Real first-commit date (HST) of each solution page -> assets/data/solution-added.json. Used for the auto-expiring 'New' badge."""
import json,subprocess,os,datetime
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
pages=[p['url'] for p in json.load(open('assets/data/solutions.json'))['pages'] if p.get('type')=='solution']
log=subprocess.run(['git','log','--diff-filter=A','--format=@%cI','--name-only','--','*.html'],capture_output=True,text=True).stdout
first={};cur=None
for ln in log.splitlines():
    if ln.startswith('@'): cur=ln[1:]
    elif ln.strip() and '/' not in ln: first[ln.strip()]=cur  # older commits overwrite -> earliest add
out={}
for p in pages:
    if p in first:
        t=datetime.datetime.fromisoformat(first[p]).astimezone(datetime.timezone(datetime.timedelta(hours=-10)))
        out[p]=t.date().isoformat()
json.dump(out,open('assets/data/solution-added.json','w'),separators=(',',':'),sort_keys=True)
print(len(out),'of',len(pages))
