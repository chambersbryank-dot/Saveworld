"""Oct 24 2026 (owner-approved, Solutions page polish): the 'Explore all solutions' page banner and back-to-top links.
- banner(): the title banner, now a code-drawn flowing animation (no photo or video): streams of light ("solutions") flow across
  the band and change colour with where they are, space violet -> ocean cyan -> land gold -> forest green, over a starfield.
  Canvas 2D, one requestAnimationFrame loop, DPR capped (2 desktop, 1.5 phones), particle count scaled to the band's area, paused
  off-screen / in a hidden tab, pause button (WCAG 2.2.2). prefers-reduced-motion: one still frame, no loop, no pause button.
  RTL pages flow right-to-left. Title centring = the hub-page standard (.sp-anim-banner + solutions.css .sol-banner: flex-centred,
  text-align:center). The section keeps class sp-anim-banner (scripts/apply-anim-banners.py must never strip it).
- toplink(): a small 'Back to top' link closing each hub section; smooth scroll, instant under reduced motion; focus moves to the
  page title so keyboard users land at the top. Text and aria-label are translated through i18n/<lang>.json (TOP_TM below).
CSS lives in solutions.css between /* SOL-FLOW:START */ markers (write_css()), scoped to .sol-flow / .sol-top."""
import re

TOP_TEXT, TOP_ARIA = 'Back to top', 'Back to the top of the page'
TOP_TM = {
    'fr': {TOP_TEXT: 'Haut de page', TOP_ARIA: 'Revenir en haut de la page'},
    'es': {TOP_TEXT: 'Volver arriba', TOP_ARIA: 'Volver al principio de la página'},
    'ar': {TOP_TEXT: 'العودة إلى الأعلى', TOP_ARIA: 'العودة إلى أعلى الصفحة'},
    'it': {TOP_TEXT: 'Torna su', TOP_ARIA: "Torna all'inizio della pagina"},
    'he': {TOP_TEXT: 'חזרה למעלה', TOP_ARIA: 'חזרה לראש העמוד'},
}
PAUSE = '<button type="button" class="spb-pause sf-pause" aria-pressed="false" aria-label="Pause banner animation">&#10074;&#10074;</button>'

JS = r"""<script>(function(){var b=document.querySelector('.sol-flow');if(!b)return;var cv=b.querySelector('canvas'),cx=cv.getContext&&cv.getContext('2d');if(!cx)return;
var mq=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)'),rtl=document.documentElement.dir==='rtl',btn=b.querySelector('.sf-pause'),
W=0,H=0,D=1,P=[],S=[],bg=null,run=false,held=false,vis=true,raf=0,t=0;
var C=[[0,[167,139,250]],[.3,[125,211,252]],[.5,[34,211,238]],[.68,[251,191,36]],[.84,[74,222,128]],[1,[52,211,153]]];
function col(y,a){var f=Math.max(0,Math.min(1,y/H)),i=1;while(i<C.length-1&&C[i][0]<f)i++;var p=C[i-1],q=C[i],k=(f-p[0])/((q[0]-p[0])||1);
return'rgba('+[0,1,2].map(function(j){return Math.round(p[1][j]+(q[1][j]-p[1][j])*k)}).join(',')+','+a+')'}
function mk(r){return{x:Math.random()*W,y:Math.random()*H,v:(.5+Math.random()*1.1)*D,s:(.7+Math.random()*1.5)*D,ph:Math.random()*6.283,big:Math.random()<.05}}
function size(){var r=b.getBoundingClientRect();D=Math.min(window.devicePixelRatio||1,innerWidth<=760?1.5:2);W=cv.width=Math.max(1,Math.round(r.width*D));H=cv.height=Math.max(1,Math.round(r.height*D));
bg=document.createElement('canvas');bg.width=W;bg.height=H;var g=bg.getContext('2d'),l=g.createLinearGradient(0,0,0,H);
l.addColorStop(0,'#040616');l.addColorStop(.32,'#071a33');l.addColorStop(.55,'#052a3a');l.addColorStop(.75,'#14261c');l.addColorStop(1,'#06140d');g.fillStyle=l;g.fillRect(0,0,W,H);
for(var i=0;i<Math.round(W*H/(5200*D*D));i++){var y=Math.pow(Math.random(),1.8)*H*.6;g.fillStyle='rgba(255,255,255,'+(.25+Math.random()*.6)*(1-y/(H*.6))+')';g.fillRect(Math.random()*W,y,D*(Math.random()<.1?1.6:.9),D*(Math.random()<.1?1.6:.9))}
var n=Math.min(innerWidth<=760?220:520,Math.round(r.width*r.height/1700));P=[];for(i=0;i<n;i++)P.push(mk());cx.globalAlpha=1;cx.drawImage(bg,0,0)}
function step(fade){cx.globalCompositeOperation='source-over';cx.globalAlpha=fade;cx.drawImage(bg,0,0);cx.globalAlpha=1;cx.globalCompositeOperation='lighter';
for(var i=0;i<P.length;i++){var p=P[i],ox=p.x,oy=p.y,a=Math.sin(p.x/(W*.18)+t*.6+p.ph*.3)*1.1+Math.sin(p.y/(H*.22)-t*.4)*.6;
p.x+=(rtl?-1:1)*p.v*(1.4+Math.cos(a)*.5);p.y+=Math.sin(a)*p.v*.85;
if(p.x>W+20||p.x<-20||p.y<-20||p.y>H+20){var q=mk();q.x=rtl?W+10:-10;P[i]=q;continue}
cx.strokeStyle=col(p.y,p.big?.95:.55);cx.lineWidth=p.s*(p.big?1.6:1);cx.lineCap='round';cx.beginPath();cx.moveTo(ox,oy);cx.lineTo(p.x,p.y);cx.stroke();
if(p.big){cx.fillStyle=col(p.y,.18);cx.beginPath();cx.arc(p.x,p.y,p.s*5,0,6.283);cx.fill()}}t+=.016}
function loop(){raf=0;if(!run)return;step(.16);raf=requestAnimationFrame(loop)}
function still(){for(var i=0;i<90;i++)step(.12)}
function upd(){var go=!held&&vis&&!document.hidden&&!(mq&&mq.matches);if(go&&!run){run=true;b.classList.add('is-playing');if(!raf)raf=requestAnimationFrame(loop)}else if(!go&&run){run=false}}
size();if(mq&&mq.matches){still()}else{still();upd()}
btn&&btn.addEventListener('click',function(){held=btn.getAttribute('aria-pressed')!=='true';btn.setAttribute('aria-pressed',held);btn.innerHTML=held?'&#9654;':'&#10074;&#10074;';upd()});
if('IntersectionObserver'in window)new IntersectionObserver(function(e){vis=e[0].isIntersecting;upd()}).observe(b);
document.addEventListener('visibilitychange',upd);mq&&mq.addEventListener&&mq.addEventListener('change',function(){if(mq.matches){run=false;b.classList.remove('is-playing');still()}upd()});
var rz;window.addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(function(){var w=Math.round(b.getBoundingClientRect().width*D);if(Math.abs(w-W)>2){size();still()}},200)});
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.sol-top-a');if(!a)return;e.preventDefault();
window.scrollTo({top:0,behavior:mq&&mq.matches?'auto':'smooth'});var h=document.getElementById('sol-h');if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}
if(history.replaceState)history.replaceState(null,'',location.pathname+location.search)})})();</script>"""

CSS = ('html body.sol-page .sp-anim-banner.sol-flow{background:#040616}'
 'html body.sol-page .sol-flow .sf-cv{position:absolute;inset:0;width:100%;height:100%;z-index:0;display:block}'
 # text sits on a soft dark halo, so the white title keeps WCAG AA contrast wherever the streams pass
 'html body.sol-page .sol-banner.sol-flow::after{background:radial-gradient(60% 55% at 50% 50%,rgba(2,6,12,.62),rgba(2,6,12,.25) 70%,rgba(2,6,12,0)),linear-gradient(180deg,rgba(2,6,12,.55) 0%,rgba(2,6,12,0) 30%,rgba(2,6,12,0) 80%,rgba(2,6,12,.35) 100%)}'
 'html body.sol-page .sol-flow .spb-text{width:100%;margin-inline:auto;text-align:center}'
 'html body.sol-page .sol-flow .spb-pause{display:block}'
 'html body.sol-page .sol-top{margin:1.2rem 0 0;text-align:end}'
 'html body.sol-page .sol-top a{display:inline-flex;align-items:center;gap:.35rem;min-height:44px;padding:.3rem .85rem;border-radius:999px;border:1px solid rgba(127,211,255,.45);color:#7fd3ff;font-size:.9rem;font-weight:600;text-decoration:none}'
 'html body.sol-page .sol-top a:hover{background:rgba(127,211,255,.12)}'
 'html body.sol-page .sol-top a:focus-visible{outline:3px solid #4da3ff;outline-offset:2px}'
 'html body.sol-page #sol-h:focus{outline:none}'
 '@media (prefers-reduced-motion:reduce){html body.sol-page .sol-flow .spb-pause{display:none!important}}')

def banner(h1_html, sub, credit, pause_label=None):
    btn = PAUSE if not pause_label else PAUSE.replace('Pause banner animation', pause_label)
    return ('<section class="sp-anim-banner sol-banner sol-flow" id="top" aria-labelledby="sol-h">'
            '<canvas class="sf-cv" aria-hidden="true"></canvas>'
            f'<div class="spb-text"><h1 id="sol-h">{h1_html}</h1><p>{sub}</p></div>'
            f'<span class="spb-credit"><span>{credit}</span></span>{btn}</section>')

def toplink(text=TOP_TEXT, aria=TOP_ARIA):
    return f'<p class="sol-top"><a class="sol-top-a" href="#top" aria-label="{aria}"><span aria-hidden="true">&#8593;</span> {text}</a></p>'

def write_css(path='solutions.css'):
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(r'\n?/\* SOL-FLOW:START \*/.*?/\* SOL-FLOW:END \*/\n?', '\n', s, flags=re.S).rstrip('\n') + '\n/* SOL-FLOW:START */\n' + CSS + '\n/* SOL-FLOW:END */\n'
    if s2 != s: open(path, 'w', encoding='utf-8').write(s2); return 1
    return 0

def write_tm():
    import json, os
    ch = 0
    for l, tr in TOP_TM.items():
        p = f'i18n/{l}.json'
        if not os.path.exists(p): continue
        raw = open(p, encoding='utf8').read(); T = json.loads(raw)
        if all(T.get(k) == v for k, v in tr.items()): continue
        T.update(tr); json.dump(T, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0); ch += 1
    return ch
