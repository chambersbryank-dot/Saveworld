/* Oct 28: on World_Map, the polar mascots pan the map to the Arctic or Antarctic (the default view crops the poles). */
(function(){document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('button.pm');if(!b||!window.wmMap)return;
var n=b.getAttribute('data-pole')==='n',m=window.wmMap,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var bb=n?[[58,-170],[86,175]]:[[-82,-170],[-45,175]];if(rm)m.fitBounds(bb);else m.flyToBounds(bb,{duration:1.2});
var el=document.getElementById('wm');el&&el.scrollIntoView({block:'center',behavior:rm?'auto':'smooth'});});})();
