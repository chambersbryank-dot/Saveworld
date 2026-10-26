/* Oct 26 2026: Learn hubs (scripts/build-learn-hubs.py). Calculator widget: subject tabs + calculator tabs (WAI-ARIA tabs, arrow keys,
   Home/End), auto-primed from the hub topic or #calc-<id>; iframes the existing calculator pages in ?embed=1 mode.
   Roadmap: progress in localStorage (key sp-aero-roadmap), up next = unfinished courses whose prerequisites are done. No network calls. */
(function(){
var w=document.querySelector('.lhc');
if(w){var data=[].slice.call(w.querySelectorAll('.lhc-data li')),st=w.querySelectorAll('.lhc-tabs')[0],kt=w.querySelectorAll('.lhc-tabs')[1],
 fr=w.querySelector('#lhp iframe'),full=w.querySelector('.lhc-full'),panel=w.querySelector('#lhp');
 function keys(list){list.addEventListener('keydown',function(e){var b=[].slice.call(list.querySelectorAll('[role=tab]')),i=b.indexOf(document.activeElement);if(i<0)return;
  var rtl=getComputedStyle(list).direction==='rtl',n=null;if(e.key==='ArrowRight')n=rtl?i-1:i+1;else if(e.key==='ArrowLeft')n=rtl?i+1:i-1;else if(e.key==='Home')n=0;else if(e.key==='End')n=b.length-1;
  if(n===null)return;e.preventDefault();n=(n+b.length)%b.length;b[n].focus();b[n].click()})}
 function sel(list,btn){[].forEach.call(list.querySelectorAll('[role=tab]'),function(x){var on=x===btn;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1})}
 function pickCalc(c){var it=data.filter(function(x){return x.dataset.calc===c})[0];if(!it)return;var b=kt.querySelector('[data-calc="'+c+'"]');sel(kt,b);
  fr.src=it.dataset.src;fr.title=it.textContent;full.href=it.dataset.full;panel.setAttribute('aria-labelledby',b.id)}
 function pickSubj(s,c){var b=st.querySelector('[data-subj="'+s+'"]');sel(st,b);kt.innerHTML='';
  data.filter(function(x){return x.dataset.subj===s}).forEach(function(x){var t=document.createElement('button');t.type='button';t.setAttribute('role','tab');t.id='lhk-'+x.dataset.calc;
   t.setAttribute('aria-controls','lhp');t.dataset.calc=x.dataset.calc;t.textContent=x.textContent;t.addEventListener('click',function(){pickCalc(x.dataset.calc)});kt.appendChild(t)});
  pickCalc(c||kt.querySelector('[role=tab]').dataset.calc)}
 [].forEach.call(st.querySelectorAll('[role=tab]'),function(b){b.addEventListener('click',function(){pickSubj(b.dataset.subj)})});keys(st);keys(kt);
 function fromHash(){var m=/^#calc-(\w+)$/.exec(location.hash);if(m){var it=data.filter(function(x){return x.dataset.calc===m[1]})[0];if(it){pickSubj(it.dataset.subj,m[1]);w.scrollIntoView();return true}}return false}
 if(!fromHash())pickSubj(w.dataset.default);window.addEventListener('hashchange',fromHash)}
var r=document.querySelector('.lhr');if(!r)return;var K='sp-aero-roadmap',done={};try{done=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){}
var items=[].slice.call(document.querySelectorAll('.lhs li[data-id]'));
function save(){try{localStorage.setItem(K,JSON.stringify(done))}catch(e){}}
function li(a,t){var l=document.createElement('li'),x=document.createElement('a');x.href=a;x.textContent=t;l.appendChild(x);return l}
function draw(){var n=0;items.forEach(function(it){var on=!!done[it.dataset.id];it.classList.toggle('is-done',on);it.querySelector('input').checked=on;if(on)n++});
 r.querySelector('.lhp-t').textContent=r.dataset.of.replace('{a}',n).replace('{b}',items.length);var bar=r.querySelector('[role=progressbar]');bar.setAttribute('aria-valuenow',n);bar.firstChild.style.width=(100*n/items.length)+'%';
 var nx=items.filter(function(it){return !done[it.dataset.id]&&(it.dataset.pre||'').split(' ').filter(Boolean).every(function(p){return done[p]})}).slice(0,3),
  ul=r.querySelector('.lh-next'),ex=r.querySelector('.lh-exams');ul.innerHTML='';ex.innerHTML='';
 if(!nx.length){ul.appendChild(document.createElement('li')).textContent=r.dataset.done}
 nx.forEach(function(it){var nm=it.querySelector('a').textContent,h=it.dataset.href;ul.appendChild(li(h,nm));ex.appendChild(li(h+'#u1',nm+': '+r.dataset.units));ex.appendChild(li(h+'#exam',nm+': '+r.dataset.exam))})}
items.forEach(function(it){it.querySelector('input').addEventListener('change',function(e){if(e.target.checked)done[it.dataset.id]=1;else delete done[it.dataset.id];save();draw()})});
r.querySelector('.lh-reset').addEventListener('click',function(){done={};save();draw()});draw()})();
