#!/usr/bin/env python3
"""Index NGSS/CCSS codes already printed on each English page -> standards-index.json (for Teachers filter)."""
import re,glob,json,os
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
pat=re.compile(r'>\s*((?:K|[1-5]|MS|HS)-(?:ESS|LS|PS|ETS)\d-\d|CCSS\.[A-Z-]+\.[A-Za-z0-9.-]*[A-Za-z0-9])\s*<')
out={}
for f in sorted(glob.glob('*.html')):
    s=open(f,encoding='utf-8',errors='ignore').read()
    c=sorted(set(pat.findall(s)))
    if c: out[f]=c
json.dump(out,open('standards-index.json','w'),separators=(',',':'),sort_keys=True)
print(len(out),'pages')
