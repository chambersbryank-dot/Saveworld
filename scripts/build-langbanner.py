#!/usr/bin/env python3
"""Oct 17: bottom sheet (never covers the H1), dismissible; skipped when the visitor already chose this page's language (localStorage sp-lang-chosen, set by nav switches and the banner); he-ready.
Oct 16 (user, 6:34 PM): site-wide language-suggestion banner. Appends a marker block to site.js and styles.css.
Shows only when the browser's preferred language (navigator.languages; en, fr, es, ar, it, he) differs from the page language
AND the page lists a translated <link rel="alternate" hreflang>. Text is in the suggested language (Arabic RTL). Never
redirects. The choice is remembered in localStorage only (no cookies, no events). Hidden in ?embed=1 mode.
Oct 16 7:36 PM: it is now a pure overlay (fixed under the nav, transform/opacity slide-in), it no longer pads <body>, so it
causes no layout shift (CLS was ~0.059). It dispatches window 'sp-lb' on show/close so the homepage hero caption can move
out of its way (assets/hero-themes.js).
Oct 16 (t886): "View in ..." keeps ?query + #hash and goes through window.spnLang (nav language switches), so the matching
switch turns green before the page changes, exactly like using the nav."""
import os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
def rd(p): return open(p, encoding='utf8').read()
def asset(path, txt):
    s = rd(path); s = re.sub(r'\n?/\* LANGBANNER:START \*/.*?/\* LANGBANNER:END \*/\n?', '', s, flags=re.S)
    open(path, 'w', encoding='utf8').write(s.rstrip('\n') + '\n' + txt.strip('\n') + '\n')
CSS = r"""
/* LANGBANNER:START */
.sp-lb{position:fixed;left:0;right:0;bottom:0;top:auto;z-index:1001;padding-bottom:calc(.5rem + env(safe-area-inset-bottom,0px));display:flex;justify-content:center;padding:.5rem .75rem;pointer-events:none}
.sp-lb-in{pointer-events:auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.5rem .75rem;max-width:960px;width:100%;box-sizing:border-box;padding:.45rem .6rem .45rem 1rem;background:rgba(7,16,24,.96);color:#fff;border:1px solid rgba(143,211,255,.45);border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.4);font:500 .95rem/1.35 "Montserrat","Segoe UI",system-ui,sans-serif;animation:sp-lb-in .35s ease-out both}
.sp-lb[dir=rtl] .sp-lb-in{padding:.45rem 1rem .45rem .6rem;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,sans-serif}
.sp-lb[lang=he] .sp-lb-in{font-family:"Noto Sans Hebrew",Heebo,"Arial Hebrew",Arial,sans-serif}
.sp-lb-msg{margin:0;flex:1 1 220px}
.sp-lb-btns{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
.sp-lb a.sp-lb-go,.sp-lb button{min-height:44px;min-width:44px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;padding:0 1rem;border-radius:999px;font:700 .9rem/1 inherit;font-family:inherit;cursor:pointer;text-decoration:none}
.sp-lb a.sp-lb-go{background:#009cde;color:#fff;border:2px solid #009cde}
.sp-lb a.sp-lb-go:hover{background:#0083bb;border-color:#0083bb}
.sp-lb .sp-lb-stay{background:transparent;color:#8fd3ff;border:2px solid rgba(143,211,255,.6)}
.sp-lb .sp-lb-stay:hover{background:rgba(143,211,255,.12)}
.sp-lb .sp-lb-x{background:transparent;color:#cfe9ff;border:0;padding:0;font-size:1.4rem}
.sp-lb a:focus-visible,.sp-lb button:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}
@keyframes sp-lb-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.sp-lb-in{animation:none}}
@media print{.sp-lb{display:none}}
/* LANGBANNER:END */
"""
JS = r"""
/* LANGBANNER:START */
document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[hreflang],.spn-ls[data-lang]');if(!a)return;var c=(a.getAttribute('data-lang')||a.getAttribute('hreflang')||'').slice(0,2).toLowerCase();if(c)try{localStorage.setItem('sp-lang-chosen',c)}catch(_){}},true);
(function(){try{
var d=document.documentElement;if(/[?&]embed=1(&|$)/.test(location.search)||d.classList.contains('sp-embed'))return;
var L=['en','fr','es','ar','it','he'],cur=(d.lang||'en').slice(0,2).toLowerCase();if(L.indexOf(cur)<0)return;
var prefs=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']),tgt=null;
for(var i=0;i<prefs.length;i++){var c=String(prefs[i]).slice(0,2).toLowerCase();if(L.indexOf(c)>=0){tgt=c;break}}
if(!tgt||tgt===cur)return;
var alt=document.querySelector('link[rel="alternate"][hreflang="'+tgt+'"]');if(!alt||!alt.href)return;
var K='sp-langbanner-v1',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){}
if(st[cur+'>'+tgt]==='stay')return;
/* Oct 17: never suggest when the visitor already picked this page's language (nav switch, banner or earlier choice) */
var CH='';try{CH=localStorage.getItem('sp-lang-chosen')||''}catch(e){}if(CH===cur)return;
var N={en:{en:'English',fr:'French',es:'Spanish',ar:'Arabic',it:'Italian',he:'Hebrew'},fr:{en:'anglais',fr:'français',es:'espagnol',ar:'arabe',it:'italien',he:'hébreu'},es:{en:'inglés',fr:'francés',es:'español',ar:'árabe',it:'italiano',he:'hebreo'},it:{en:'inglese',fr:'francese',es:'spagnolo',ar:'arabo',it:'italiano',he:'ebraico'}};/* Oct 25: he was missing here, so a /he/ page showed 'Stay in undefined' */
for(var k in N)if(!N[k][cur])N[k][cur]=cur.toUpperCase();/* never 'undefined' if a new page language is added later */
var T={en:['This page is available in English.','View in English','Stay in '+N.en[cur],'Close'],
fr:['Cette page est disponible en français.','Voir en français','Rester en '+N.fr[cur],'Fermer'],
es:['Esta página está disponible en español.','Ver en español','Seguir en '+N.es[cur],'Cerrar'],
ar:['هذه الصفحة متوفرة باللغة العربية.','اعرضها بالعربية','البقاء على هذه الصفحة','إغلاق'],
it:['Questa pagina è disponibile in italiano.','Vedi in italiano','Resta in '+N.it[cur],'Chiudi'],
he:['הדף הזה זמין בעברית.','הצגה בעברית','להישאר בדף הזה','סגירה']}[tgt];
function save(v){st[cur+'>'+tgt]=v;try{localStorage.setItem(K,JSON.stringify(st));localStorage.setItem('sp-lang-chosen',v==='go'?tgt:cur)}catch(e){}}
var b=document.createElement('div');b.className='sp-lb';b.setAttribute('role','region');b.setAttribute('aria-label',T[0]);b.lang=tgt;b.dir=(tgt==='ar'||tgt==='he')?'rtl':'ltr';
b.innerHTML='<div class="sp-lb-in"><p class="sp-lb-msg"></p><div class="sp-lb-btns"><a class="sp-lb-go"></a><button type="button" class="sp-lb-stay"></button><button type="button" class="sp-lb-x"><span aria-hidden="true">×</span></button></div></div>';
b.querySelector('.sp-lb-msg').textContent=T[0];var g=b.querySelector('.sp-lb-go');g.textContent=T[1];g.href=alt.href.replace(/[?#].*$/,'')+location.search+location.hash;g.hreflang=tgt;
b.querySelector('.sp-lb-stay').textContent=T[2];b.querySelector('.sp-lb-x').setAttribute('aria-label',T[3]);
var nav=document.getElementById('topnav');
function place(){d.style.setProperty('--sp-lb-h',b.offsetHeight+'px')}
function ping(){try{window.dispatchEvent(new Event('sp-lb'))}catch(e){}}
function close(){save('stay');b.remove();d.classList.remove('sp-has-lb');d.style.removeProperty('--sp-lb-h');ping();if(nav){var f=nav.querySelector('a,button');f&&f.focus({preventScroll:true})}}
g.addEventListener('click',function(e){save('go');/* Oct 16 t886: switch the same way as the nav language switches (green toggle, keeps ?query/#hash) */if(!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.altKey&&window.spnLang&&window.spnLang(tgt))e.preventDefault()});
b.querySelector('.sp-lb-stay').addEventListener('click',close);b.querySelector('.sp-lb-x').addEventListener('click',close);
function show(){if(!document.body)return;if(nav&&nav.parentNode)nav.parentNode.insertBefore(b,nav.nextSibling);else document.body.insertBefore(b,document.body.firstChild);
d.classList.add('sp-has-lb');place();ping();if(window.ResizeObserver){var ro=new ResizeObserver(place);ro.observe(b);nav&&ro.observe(nav)}window.addEventListener('resize',place,{passive:true});window.addEventListener('scroll',place,{passive:true})}
/* Oct 16 perf: overlay, so show it when the main thread is idle after load (never blocks first paint) */
function later(){(window.requestIdleCallback||function(f){setTimeout(f,200)})(show,{timeout:2500})}
if(document.readyState==='complete')later();else window.addEventListener('load',later);
}catch(e){}})();
/* LANGBANNER:END */
"""
asset('styles.css', CSS); asset('site.js', JS)
print('build-langbanner: site.js + styles.css')
