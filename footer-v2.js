/* Footer v2 (founder Nov 3: "mitigate long series of text"): five groups set by the founder
   (Contact, About, Policy, Media Relations, Partnerships) as accordions on mobile, a language switcher, X, and a short credit line.
   Other footer links live on the Site Map (linked under About). Long paragraphs fold into one "Credits & licence" panel.
   Without JS the original footer shows. */
(function(){
var f=document.querySelector('footer');if(!f||f.classList.contains('fv2'))return;
var H=document.documentElement,lang=(H.lang||'en').slice(0,2);
var S={en:['Contact','About','Policy','Media Relations','Partnerships','Credits & licence','Language','Created by the Founder and SI','Site map'],
fr:['Contact','À propos','Politiques','Relations médias','Partenariats','Crédits et licence','Langue','Créé par le fondateur et SI','Plan du site'],
es:['Contacto','Acerca de','Políticas','Relaciones con medios','Alianzas','Créditos y licencia','Idioma','Creado por el fundador y SI','Mapa del sitio'],
it:['Contatti','Chi siamo','Policy','Relazioni con i media','Partnership','Crediti e licenza','Lingua','Creato dal fondatore e da SI','Mappa del sito'],
ar:['اتصل بنا','من نحن','السياسات','العلاقات الإعلامية','الشراكات','الاعتمادات والترخيص','اللغة','من إنشاء المؤسس وSI','خريطة الموقع'],
he:['צור קשר','אודות','מדיניות','קשרי מדיה','שותפויות','קרדיטים ורישיון','שפה','נוצר על ידי המייסד ו-SI','מפת האתר']}[lang];
if(!S)return;
var G=[['contact',/^Contact\.html|^mailto:(hello|ideas|info)/],
['partner',/About\.html#partner|^Ways_to_Help\.html|^mailto:partner/],
['media',/^(Press|Media_Provenance)\.html|^mailto:(media|press)/],
['policy',/^(Privacy|Terms|Accessibility|Corrections|Cookies?)\.html|About\.html#licen/],
['about',/^(About|Editorial_Policy|Changelog)\.html$|^About\.html#criteria/]];
var cols={contact:[],about:[],policy:[],media:[],partner:[]},seen={};
var fm=f.querySelector('.footer-map');if(fm)fm.remove();
f.querySelectorAll('a').forEach(function(a){var h=a.getAttribute('href')||'',k=h.replace(/^(\.\.\/)+/,'');
 var key=k.replace(/[?].*$/,'');if(!h||seen[key])return;var t=a.textContent.trim();if(!t)return;
 for(var i=0;i<G.length;i++)if(G[i][1].test(k)){seen[key]=1;var n=a.cloneNode(true);n.removeAttribute('style');n.removeAttribute('class');
  if(/^mailto:/.test(h)&&!/@/.test(t))n.textContent=h.slice(7).split('?')[0];cols[G[i][0]].push(n);break}});
var pre=location.pathname.match(/^\/(fr|es|it|ar|he)\//)?'../':'';
if(!seen['Contact.html']){var c=document.createElement('a');c.href='Contact.html';c.textContent=S[0];cols.contact.unshift(c)}
if(!cols.partner.some(function(a){return /partner-relations/.test(a.href)})){var pm=document.createElement('a');pm.href='mailto:partner-relations@savingplanets.com';pm.textContent='partner-relations@savingplanets.com';cols.partner.push(pm)}
var sm=document.createElement('a');sm.href='Sitemap.html';sm.textContent=S[8];cols.about.push(sm);
var wrap=document.createElement('div');wrap.className='fv2-cols';var desk=matchMedia('(min-width:760px)');
function col(title,list){if(!list.length)return;var d=document.createElement('details');d.className='fv2-col';d.open=desk.matches;
 var s=document.createElement('summary');s.textContent=title;d.appendChild(s);var ul=document.createElement('ul');
 list.forEach(function(a){var li=document.createElement('li');li.appendChild(a);ul.appendChild(li)});d.appendChild(ul);wrap.appendChild(d)}
col(S[0],cols.contact);col(S[1],cols.about);col(S[2],cols.policy);col(S[3],cols.media);col(S[4],cols.partner);
if(desk.addEventListener)desk.addEventListener('change',function(e){wrap.querySelectorAll('details').forEach(function(d){d.open=e.matches})});
var old=document.createElement('details');old.className='fv2-old';var os=document.createElement('summary');os.textContent=S[5];old.appendChild(os);
while(f.firstChild)old.appendChild(f.firstChild);
var bar=document.createElement('div');bar.className='fv2-bar';
var L=[['en','EN'],['fr','FR'],['es','ES'],['it','IT'],['ar','عربي'],['he','עב']],p=location.pathname.replace(/^\/(fr|es|it|ar|he)\//,'/');
var ln=document.createElement('div');ln.className='fv2-lang';ln.setAttribute('role','navigation');ln.setAttribute('aria-label',S[6]);
L.forEach(function(x){var a=document.createElement('a');a.href=(x[0]==='en'?'':'/'+x[0])+p;a.textContent=x[1];a.hreflang=x[0];a.lang=x[0];if(x[0]===lang)a.setAttribute('aria-current','true');ln.appendChild(a)});
var so=document.createElement('p');so.className='fv2-soc';so.innerHTML='<a href="https://x.com/SISavingPlanets" rel="noopener me" target="_blank"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M18.2 2H21l-6.5 7.4L22 22h-6l-4.7-6.1L5.8 22H3l7-8L2 2h6.1l4.2 5.6zm-1 18h1.6L7 3.9H5.3z"/></svg> @SISavingPlanets</a>';
var cr=document.createElement('p');cr.className='fv2-credit';cr.textContent='© '+new Date().getFullYear()+' Saving Planets · '+S[7];
bar.appendChild(ln);bar.appendChild(so);bar.appendChild(cr);
f.classList.add('fv2');f.appendChild(wrap);f.appendChild(bar);f.appendChild(old);
})();
