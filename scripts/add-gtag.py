#!/usr/bin/env python3
"""Idempotently place the GA4 tag (G-M5L2259Z68) right after <head> on every HTML page.
Consent Mode v2: analytics/ad storage default to denied; consent.js flips analytics_storage
to granted when the visitor clicks Accept. Run by weekly-sync.sh after all generators."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"googlea5d3cc0c785fec04.html", "ways_to_help.html", "ways-to-help.html"}  # redirect stubs
TAG = r"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M5L2259Z68"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {analytics_storage: (function(){try{return localStorage.getItem('sp_consent')==='granted'?'granted':'denied'}catch(e){return 'denied'}})(), ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  gtag('js', new Date());

  gtag('config', 'G-M5L2259Z68');
  /* Oct 14 2026 event plan: sent only after the visitor accepts analytics (sp_consent=granted). */
  window.spTrack=function(n,p){try{if(localStorage.getItem('sp_consent')==='granted')gtag('event',n,p||{})}catch(e){}};
  (function(){var d=document,km={};d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a,[data-hub]');if(!a)return;var h=a.getAttribute('href')||'';
  if(/^mailto:partners@/i.test(h))spTrack('partner_click',{link_url:h.split('?')[0]});
  else if(a.classList.contains('donate-btn')||/\/(donate|join|give)/i.test(h)&&/^https?:/i.test(h)&&h.indexOf(location.hostname)<0)spTrack('outbound_donate',{link_url:h.slice(0,200)});
  if(a.dataset&&a.dataset.hub&&a.closest('#km')){km[a.dataset.hub]=1;spTrack('map_bubble_open',{hub:a.dataset.hub});var t=a.closest('#km').querySelectorAll('[data-hub]').length;if(Object.keys(km).length===t&&!km._done){km._done=1;spTrack('map_complete',{bubbles:t})}}},true);
  d.addEventListener('submit',function(e){var f=e.target;if(f&&f.id==='lb'){var g=function(k){return f.elements[k]?f.elements[k].value:''};spTrack('lesson_generated',{grade_band:g('band'),topic:g('hub'),minutes:g('min')})}},true);
  d.addEventListener('sx:dock',function(e){if(e.detail&&e.detail.left===0)spTrack('explorer_complete',{level:(d.querySelector('input[name="sx-level"]:checked')||{}).value||''})},true);
  ['play','ended'].forEach(function(t){d.addEventListener(t,function(e){var v=e.target;if(!v||v.tagName!=='VIDEO'||v.classList.contains('hero-video'))return;if(t==='play'&&v._spStarted)return;v._spStarted=1;spTrack(t==='play'?'video_start':'video_complete',{video_url:(v.currentSrc||'').split('/').pop()})},true)});})();
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
