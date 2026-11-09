(function(){
  var form=document.getElementById('match-form');
  if(!form)return;
  var lang=(document.documentElement.lang||'en').slice(0,2);
  var pre=location.pathname.indexOf('/'+lang+'/')>-1?'../':'';
  var T=window.SP9MATCH||{};
  fetch(pre+'assets/data/match.'+lang+'.json').then(function(r){return r.json()}).then(function(data){
    var all=data.solutions||[];
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var fd=new FormData(form);
      var cause=fd.get('cause'), help=fd.get('help'), where=fd.get('where'), who=fd.get('who');
      function ok(s, place){
        if(s.theme!==cause)return false;
        if(who==='kid'&&!s.kid)return false;
        if(help==='money'&&!s.give)return false;
        if(help==='time'&&!s.time)return false;
        if(!place)return true;
        if(where==='near')return !!(s.local||s.where==='local');
        if(help==='money')return true;
        if(help==='learn')return true;
        if(s.where==='remote')return true;
        if(s.where==='local')return false;
        return !!s.remote;
      }
      var exact=all.filter(function(s){return ok(s,true)});
      exact.sort(function(a,b){return a.title.localeCompare(b.title)});
      var note=T.exact, list=exact.slice(0,3), mode='exact';
      if(who==='kid'&&exact.length===0){
        note=T.kid_empty; list=[];
      } else if(list.length<3){
        var wide=all.filter(function(s){return ok(s,false)});
        wide.sort(function(a,b){return a.title.localeCompare(b.title)});
        if(wide.length>list.length){list=wide.slice(0,3); note=T.relaxed; mode='relaxed';}
        else {note=list.length?T.short:T.none;}
      }
      var out=document.getElementById('match-out');
      out.hidden=false;
      document.getElementById('match-note').textContent=note;
      var ol=document.getElementById('match-list');
      ol.textContent='';
      list.forEach(function(s){
        var li=document.createElement('li');
        var h=document.createElement('a'); h.href=s.url; h.textContent=s.title; li.appendChild(h);
        if(s.blurb){var p=document.createElement('p'); p.textContent=s.blurb; li.appendChild(p);}
        var href=s.url, label=T.learn||'Learn';
        if(help==='money'&&s.donate){href=s.donate; label=T.don||'Donate';}
        else if(help==='time'&&s.volunteer){href=s.volunteer; label=T.vol||'Volunteer';}
        var a=document.createElement('a'); a.className='btn'; a.href=href; a.textContent=label;
        if(/^https?:/.test(href)){a.target='_blank'; a.rel='noopener';}
        var why=document.createElement('p');
        why.textContent=(s.local?T.why_near:T.why_remote)||'';
        li.appendChild(a); li.appendChild(why); ol.appendChild(li);
      });
      out.focus&&out.setAttribute('tabindex','-1'); out.focus();
    });
  });
})();
