/* Oct 24 2026: Courses (scripts/build-courses.py). Quizzes with instant feedback, flashcards, progress in localStorage (this browser only). */
(function(){var root=document.querySelector('.crs[data-course]');if(!root)return;root.classList.add('crs-js');
var KEY='sp-course:'+root.dataset.course,S;try{S=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){S={}}S.done=S.done||{};S.quiz=S.quiz||{};
function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}prog()}
var boxes=root.querySelectorAll('[data-done]');
function prog(){var n=boxes.length,d=0;boxes.forEach(function(b){if(S.done[b.dataset.done])d++});var p=root.querySelector('.crs-prog');if(!p)return;
 var q=Object.keys(S.quiz).map(function(k){return k+' '+S.quiz[k]}).join(', ');p.querySelector('progress').value=n?Math.round(100*d/n):0;
 p.querySelector('.crs-prog-t').textContent=d+' of '+n+' units and labs done ('+(n?Math.round(100*d/n):0)+'%).'+(q?' Best quiz scores: '+q+'.':'')}
boxes.forEach(function(b){b.checked=!!S.done[b.dataset.done];b.addEventListener('change',function(){S.done[b.dataset.done]=b.checked;save()})});
root.querySelectorAll('.crs-quiz').forEach(function(f){var id=f.dataset.quiz,fs=f.querySelectorAll('fieldset'),sc=f.querySelector('.crs-qs');
 function score(){var r=0,a=0;fs.forEach(function(x){if(x.dataset.ans!=null){a++;if(x.dataset.ans===x.dataset.ok)r++}});
  sc.textContent=a?('Score: '+r+' of '+fs.length+(a<fs.length?' (answered '+a+')':'')):'';if(a===fs.length){var t=r+'/'+fs.length,old=S.quiz[id];
  if(!old||parseInt(old)<r)S.quiz[id]=t;save()}}
 fs.forEach(function(x){x.addEventListener('change',function(e){var v=e.target.value,fb=x.querySelector('.crs-fb'),why=x.querySelector('.crs-why').textContent;
  x.dataset.ans=v;var ok=v===x.dataset.ok;fb.className='crs-fb '+(ok?'ok':'no');
  fb.textContent=(ok?'Correct. ':'Not quite. The answer is: '+x.querySelectorAll('label')[+x.dataset.ok].textContent.trim()+'. ')+why;score()})});
 var r=document.createElement('button');r.type='button';r.className='crs-btn';r.textContent='Try this quiz again';
 r.addEventListener('click',function(){fs.forEach(function(x){delete x.dataset.ans;x.querySelectorAll('input').forEach(function(i){i.checked=false});var fb=x.querySelector('.crs-fb');fb.textContent='';fb.className='crs-fb'});sc.textContent=''});f.appendChild(r)});
root.querySelectorAll('.crs-fc').forEach(function(w){var items=[].map.call(w.querySelectorAll('li'),function(li){return[li.querySelector('.crs-fc-f').textContent,li.querySelector('.crs-fc-b').textContent]});
 var i=0,back=false,list=w.querySelector('.crs-fc-list');list.hidden=true;
 var card=document.createElement('button');card.type='button';card.className='crs-fc-one';card.setAttribute('aria-live','polite');
 var bar=document.createElement('div');bar.className='crs-fc-bar';
 function b(t,fn){var x=document.createElement('button');x.type='button';x.className='crs-btn';x.textContent=t;x.addEventListener('click',fn);bar.appendChild(x);return x}
 var pos=document.createElement('span');
 function show(){card.textContent=items[i][back?1:0];card.classList.toggle('back',back);card.setAttribute('aria-label',(back?'Answer: ':'Card '+(i+1)+' of '+items.length+': ')+items[i][back?1:0]+'. Activate to flip.');pos.textContent=(i+1)+' / '+items.length}
 card.addEventListener('click',function(){back=!back;show()});
 b('Previous',function(){i=(i-1+items.length)%items.length;back=false;show()});b('Flip',function(){back=!back;show()});b('Next',function(){i=(i+1)%items.length;back=false;show()});
 b('Shuffle',function(){for(var k=items.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1)),t=items[k];items[k]=items[j];items[j]=t}i=0;back=false;show()});
 var all=b('Show all',function(){list.hidden=!list.hidden;all.setAttribute('aria-pressed',String(!list.hidden))});all.setAttribute('aria-pressed','false');
 bar.appendChild(pos);w.insertBefore(card,list);w.insertBefore(bar,list);show()});
var rs=root.querySelector('[data-reset]');if(rs)rs.addEventListener('click',function(){if(!confirm('Clear your saved progress and quiz scores for this course?'))return;S={done:{},quiz:{}};boxes.forEach(function(b){b.checked=false});save()});
var pr=root.querySelector('[data-print]');if(pr)pr.addEventListener('click',function(){window.print()});
var opened=[];window.addEventListener('beforeprint',function(){root.querySelectorAll('details:not([open])').forEach(function(d){d.open=true;opened.push(d)})});
window.addEventListener('afterprint',function(){opened.forEach(function(d){d.open=false});opened=[]});prog()})();
