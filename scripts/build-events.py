#!/usr/bin/env python3
"""Oct 16 2026: privacy-safe aggregate event counter (client half). Appends the SPEV block to site.js (idempotent).
Events go to the si-helper Worker POST /e (Workers Analytics Engine, dataset sp_events): counts only, strict allowlist,
no free text, no identifiers, no cookies. Skipped when the browser sends Do Not Track or Global Privacy Control.
Batched; sent with navigator.sendBeacon (text/plain, no preflight) when the page is hidden or 10 events are queued.
Weekly report: python3 scripts/events-report.py (Analytics Engine SQL API; private, runs on the box)."""
import re
JS = r"""
/* SPEV:START */
(function(){
  var N=navigator,W=window,D=document;
  if(N.doNotTrack==='1'||W.doNotTrack==='1'||N.msDoNotTrack==='1'||N.globalPrivacyControl===true){W.spTrack=function(){};return}
  var URL_='https://si-helper.chambersbryank.workers.dev/e',L=(D.documentElement.getAttribute('lang')||'en').slice(0,2),Q=[],once={};
  function flush(){if(!Q.length||!N.sendBeacon)return;var b=JSON.stringify({l:L,e:Q.splice(0,20)});try{N.sendBeacon(URL_,new Blob([b],{type:'text/plain'}))}catch(e){}}
  function add(o,key){if(key){if(once[key])return;once[key]=1}Q.push(o);if(Q.length>=10)flush()}
  W.spTrack=function(n,p){if(n==='newsletter_signup')add({n:'newsletter'});if(n==='share'&&p)add({n:'share',kind:p.kind,page:p.page});if(n==='calc'&&p)add({n:'calc',tool:p.tool},'c'+p.tool)};
  D.addEventListener('visibilitychange',function(){if(D.visibilityState==='hidden')flush()});
  W.addEventListener('pagehide',flush);
  var pg=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,''),m=/^(Orbits?|Aero|Physics)_(Guide|Math|Lab)$/.exec(pg);
  var TR={Orbit:'orbit',Orbits:'orbit',Aero:'aero',Physics:'phys'};
  if(pg==='Learn')add({n:'learn',track:'all',kind:'hub'},'lv');
  if(m){var tr=TR[m[1]],kind=m[2].toLowerCase();add({n:'learn',track:tr,kind:kind},'lv');
    if(kind==='lab'){var f=function(e){if(e.target.closest&&e.target.closest('main')){add({n:'lab',tool:tr},'lab');D.removeEventListener('input',f,true);D.removeEventListener('click',f,true)}};D.addEventListener('input',f,true);D.addEventListener('click',f,true)}
    D.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.lnp-check,.lmcq button');if(!b)return;
      var box=b.closest('.lnp,.lmcq'),fb=box&&box.querySelector('.lnp-fb');if(!fb)return;
      var res=/\bis-ok\b/.test(fb.className)?'correct':/\bis-no\b/.test(fb.className)?'attempt':'';if(!res)return;
      var sec=box.closest('section[id]'),topic=sec?String(sec.id).toLowerCase().replace(/[^a-z0-9-]/g,'').slice(0,32):'page';
      add({n:'practice',track:tr,result:res,topic:topic||'page'});if(res==='correct')add({n:'practice',track:tr,result:'attempt',topic:topic||'page'})},false)}
  if(pg==='Ways_to_Help')D.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="http"]');if(!a)return;
    var h=(a.hostname||'').toLowerCase().replace(/^www\./,'');if(!h||/savingplanets\.com$/.test(h))return;
    add({n:'partner',host:h.slice(0,64),kind:/help-btn-join/.test(a.className)?'join':/help-btn/.test(a.className)?'donate':'link'});flush()},true);
})();
/* SPEV:END */
"""
p = 'site.js'; s = open(p, encoding='utf8').read()
s = re.sub(r'\n?/\* SPEV:START \*/.*?/\* SPEV:END \*/\n?', '', s, flags=re.S)
n = s.rstrip('\n') + '\n' + JS.strip('\n') + '\n'
if n != open(p, encoding='utf8').read(): open(p, 'w', encoding='utf8').write(n); print('build-events: site.js updated')
else: print('build-events: no change')
