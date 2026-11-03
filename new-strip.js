/* Turns the "New this week" link list into icon cards + carousel. Same links, no extra requests. */
(function(){
var M=[[/penguin|oceanites/i,'🐧'],[/polar_bear/i,'🐻‍❄️'],[/soccom|float/i,'🤖'],[/epica|ice|smartice/i,'🧊'],[/gough|island/i,'🏝️'],[/iaato|touris/i,'🚢'],[/inuit|council_?$|pathways|permafrost/i,'🏔️'],[/ccamlr|pame|marine|nmca|soos|ocean/i,'🌊'],[/mosaic|expedition|basecamp/i,'⛺'],[/scar|research|caff|biodiv/i,'🔬'],[/wwf|asoc|coalition/i,'🌍']];
var L={en:['new','Swipe or use the arrows','Previous','Next','Read'],fr:['nouv.','Faites défiler ou utilisez les flèches','Précédent','Suivant','Lire'],es:['nuevas','Desliza o usa las flechas','Anterior','Siguiente','Leer'],it:['nuove','Scorri o usa le frecce','Precedente','Successivo','Leggi'],ar:['جديد','اسحب أو استخدم الأسهم','السابق','التالي','اقرأ'],he:['חדש','החליקו או השתמשו בחצים','הקודם','הבא','לקריאה']};
var lang=(document.documentElement.lang||'en').slice(0,2),T=L[lang]||L.en,rtl=document.documentElement.dir==='rtl';
document.querySelectorAll('section.new-strip').forEach(function(s,k){
 var ul=s.querySelector('.ns-list');if(!ul||s.classList.contains('nsx'))return;
 s.classList.add('nsx');var items=ul.querySelectorAll('li');
 var h=s.querySelector('h2'),sum=s.querySelector('.ns-sum'),head=document.createElement('div');head.className='nsx-head';
 var b=document.createElement('span');b.className='nsx-badge';b.setAttribute('aria-hidden','true');b.innerHTML='<b>'+items.length+'</b><small>'+T[0]+'</small>';
 var box=document.createElement('div');h.parentNode.insertBefore(head,h);head.appendChild(b);head.appendChild(box);box.appendChild(h);if(sum)box.appendChild(sum);
 var nav=document.createElement('div');nav.className='nsx-nav';
 ul.id=ul.id||('nsx-list-'+k);ul.setAttribute('tabindex','0');ul.setAttribute('aria-label',h.textContent.replace(/^\W+/,'')+' — '+T[1]);
 [[T[2],rtl?'→':'←',-1],[T[3],rtl?'←':'→',1]].forEach(function(d){var x=document.createElement('button');x.type='button';x.textContent=d[1];x.setAttribute('aria-label',d[0]);x.setAttribute('aria-controls',ul.id);
  x.onclick=function(){var r=matchMedia('(prefers-reduced-motion: reduce)').matches;ul.scrollBy({left:d[2]*(rtl?-1:1)*ul.clientWidth*.85,behavior:r?'auto':'smooth'})};nav.appendChild(x)});
 head.appendChild(nav);
 items.forEach(function(li){var a=li.querySelector('a');if(!a)return;var hr=a.getAttribute('href')||'',ic='🧭';
  for(var i=0;i<M.length;i++)if(M[i][0].test(hr)){ic=M[i][1];break}
  var t=document.createElement('span');t.className='nsx-t';while(a.firstChild)t.appendChild(a.firstChild);
  var e=document.createElement('span');e.className='nsx-ic';e.setAttribute('aria-hidden','true');e.textContent=ic;
  var g=document.createElement('span');g.className='nsx-go';g.setAttribute('aria-hidden','true');g.textContent=T[4]+(rtl?' ←':' →');
  a.appendChild(e);a.appendChild(t);a.appendChild(g);});
});
})();
