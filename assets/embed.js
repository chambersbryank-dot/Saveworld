/* Oct 16 2026: Embed bar (build-embed.py). Shows the prefilled iframe snippet and copies it. One privacy-safe event
   (share/embed/<page kind>) via spTrack, which is a no-op under Do Not Track / GPC. No cookies, no third parties. */
(function(){document.querySelectorAll('.emb-bar').forEach(function(bar){var out=bar.querySelector('.dt-out'),ta=out.querySelector('textarea'),
 show=bar.querySelector('[data-emb="show"]'),cp=bar.querySelector('[data-emb="copy"]'),st=bar.querySelector('.emb-st');
 show.addEventListener('click',function(){out.hidden=!out.hidden;show.setAttribute('aria-expanded',String(!out.hidden));if(!out.hidden){ta.focus();ta.select()}});
 cp.addEventListener('click',function(){var done=function(){st.textContent=cp.dataset.ok;if(window.spTrack)window.spTrack('share',{kind:'embed',page:bar.dataset.page})};
  (navigator.clipboard?navigator.clipboard.writeText(ta.value):Promise.reject()).then(done,function(){ta.select();try{document.execCommand('copy')}catch(e){}done()})})})})();
