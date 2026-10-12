#!/usr/bin/env python3
"""Idempotently place the GA4 tag (G-ZCJ7CEKN94) right after <head> on every HTML page.
Consent Mode v2: analytics/ad storage default to denied; consent.js flips analytics_storage
to granted when the visitor clicks Accept. Run by weekly-sync.sh after all generators."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"googlea5d3cc0c785fec04.html"}
TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZCJ7CEKN94"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {analytics_storage: (function(){try{return localStorage.getItem('sp_consent')==='granted'?'granted':'denied'}catch(e){return 'denied'}})(), ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  gtag('js', new Date());

  gtag('config', 'G-ZCJ7CEKN94');
</script>
<!-- /Google tag -->"""
BLOCK = re.compile(r"\n?<!-- Google tag \(gtag\.js\) -->.*?<!-- /Google tag -->", re.S)
HEAD = re.compile(r"<head(\s[^>]*)?>", re.I)
n = 0
for p in ROOT.rglob("*.html"):
    if ".git" in p.parts or p.name in SKIP: continue
    s = p.read_text(encoding="utf-8")
    t = BLOCK.sub("", s)
    m = HEAD.search(t)
    if not m: continue
    t = t[:m.end()] + "\n" + TAG + t[m.end():]
    if t != s: p.write_text(t, encoding="utf-8"); n += 1
print(f"add-gtag: updated {n} pages")
