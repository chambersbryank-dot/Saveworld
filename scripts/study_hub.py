# -*- coding: utf-8 -*-
"""Study: Aerospace Engineering hub body for Courses.html.
Splices into the existing page so the header, footer, and preload styles stay."""
import html, json, os, re
from study_aero_text import T, IDS
from courses import roadmap as RM

SRC = {
 'en': ('Embry-Riddle aerospace engineering degree', 'Daytona Beach catalog (PDF)'),
 'fr': ('Diplôme Embry-Riddle en génie aérospatial', 'Catalogue de Daytona Beach (PDF)'),
 'es': ('Grado Embry-Riddle de ingeniería aeroespacial', 'Catálogo de Daytona Beach (PDF)'),
 'ar': ('درجة إمبري-ريدل في هندسة الطيران والفضاء', 'فهرس دايتونا بيتش (PDF)'),
 'it': ('Titolo Embry-Riddle in ingegneria aerospaziale', 'Catalogo di Daytona Beach (PDF)'),
 'he': ('התואר של אמברי-רידל בהנדסת אווירונאוטיקה וחלל', 'קטלוג דייטונה ביץ׳ (PDF)'),
}
SRC_URL = (
 'https://erau.edu/degrees/bachelor/aerospace-engineering',
 'https://catalog.erau.edu/programs/undergraduate/bachelors/aerospace-engineering/aerospace-engineering_daytonabeachtext.pdf',
)

CSS = r"""/* STUDY-TRACKS */
@font-face{font-family:"SP Hub Fallback";src:local("Liberation Sans"),local("Arial");size-adjust:113.7%;ascent-override:90%;descent-override:22%;line-gap-override:0%}
html:not([dir="rtl"]) body.toc-sub.learn-page:has(#bs-aero){font-family:Montserrat,"SP Hub Fallback","Segoe UI",sans-serif}
.page-hero.hero-learn:has(.crs-program) h1{line-height:1.23}
.page-hero.hero-learn:has(.crs-program) .page-hero-content p{line-height:1.2}
.page-hero .crs-program{margin:0 0 .35rem;font-weight:800;font-size:.95rem}
body.toc-sub.learn-page .page-hero.hero-learn:has(.crs-program){min-height:0!important;padding:calc(var(--nav-height,88px) + .5rem) 1.1rem .75rem!important}
.cite-foot{overflow-wrap:anywhere}
#track-sentinel{height:1px}
#track-prompt{margin:.15rem 0 .4rem}
.crs-week{margin:.15rem 0 .35rem}
.crs-hook{display:grid;gap:.45rem 1rem;align-items:center;margin:0 0 .45rem}
.crs-hook .crs-week{margin:0}
.crs-film{margin:0}
.crs-watch-frame{position:relative;aspect-ratio:16/9;margin:0;border-radius:12px;overflow:hidden;background:#071422}
.crs-watch-play{appearance:none;border:0;padding:0;margin:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.65rem;cursor:pointer;color:#fff;background:linear-gradient(160deg,#12304d,#071422 70%);font:inherit}
.crs-watch-play:focus-visible{outline:3px solid #ffd54a;outline-offset:-6px}
.crs-watch-tri{display:block;width:0;height:0;border-style:solid;border-width:16px 0 16px 28px;border-color:transparent transparent transparent #fff}
.crs-watch-cap{max-width:34rem;text-align:center;font-weight:700;padding:0 .8rem;line-height:1.35}
.crs-watch-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.crs-film figcaption{display:flex;flex-direction:column;gap:.12rem;margin-top:.35rem;font-size:.9rem;line-height:1.35}
.crs-film-title{font-weight:800}
@media (min-width:800px){.crs-hook{grid-template-columns:minmax(0,1fr) minmax(260px,420px)}}
@media (max-width:700px){#track-prompt,.crs-week{padding-inline-end:11rem}}
.crs:has(#bs-aero){max-width:1180px;padding:.65rem 1rem 1.15rem}
.crs-sticky{position:sticky;top:var(--nav-height,88px);z-index:30;display:flex;flex-wrap:wrap;gap:.4rem .6rem;align-items:flex-start;justify-content:space-between;margin:.15rem 0 .45rem;padding:.4rem .5rem;background:rgba(7,16,24,.94);border:1px solid rgba(143,211,255,.4);border-radius:16px;box-shadow:0 8px 22px rgba(0,0,0,.28)}
.crs-tracks{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:.4rem;flex:1 1 280px;margin:0}
@media (min-width:900px){.crs-sticky{flex-direction:column;align-items:stretch}.crs-tracks{grid-template-columns:repeat(4,minmax(0,1fr));flex:none}}
.crs-track{min-height:44px;text-align:start;border-radius:14px;padding:.4rem .7rem;cursor:pointer;color:#fff;font:inherit;border:1px solid rgba(255,255,255,.4);background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),rgba(12,28,56,.72);box-shadow:inset 0 1px 0 rgba(255,255,255,.5),0 6px 16px rgba(0,0,0,.25)}
.crs-track-n{display:block;font-weight:800}
.crs-track-d{display:block;font-size:.82rem;font-weight:500;line-height:1.35}
.crs-track[aria-pressed="true"]{border:2px solid #ffd54a;font-weight:700}
.crs-track:focus-visible,.crs-jumps a:focus-visible,.crs-totop:focus-visible,.crs-foldbar button:focus-visible,.crs-tip>summary:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}
.crs-tip{margin:.15rem 0 0}
.crs-tip>summary{cursor:pointer;display:inline-flex;align-items:center;min-height:44px;padding:0 .15rem;list-style:none;font-size:.85rem;font-weight:800;text-decoration:underline;text-underline-offset:.15em}
.crs-tip>summary::-webkit-details-marker{display:none}
.crs-tip>p{margin:.15rem 0 .35rem;max-width:36rem;font-size:.9rem;line-height:1.45}
.crs-sticky.is-stuck{padding:.35rem .5rem}
.crs-sticky.is-stuck .crs-track-d{display:none}
.crs-jumps{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center}
body.toc-sub .crs-jumps{position:static;top:auto;right:auto;left:auto;width:auto;z-index:auto}
.crs-jumps a{min-height:44px;display:inline-flex;align-items:center;padding:0 .8rem;border-radius:999px;text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,.4);background:rgba(255,255,255,.06)}
.crs-tag{display:inline-block;margin:0 .35rem .15rem 0;font-size:.75rem;font-weight:700;padding:.08rem .45rem;border-radius:999px;border:1px solid rgba(143,211,255,.45);background:rgba(143,211,255,.1);vertical-align:middle}
html[dir="rtl"] .crs-tag{margin:0 0 .15rem .35rem}
html.crs-js .crs-tag{display:none}
.crs-soon{display:inline-block;margin:0 0 .15rem;font-size:.75rem;font-weight:650;letter-spacing:.01em;opacity:.72}
.crs-source{font-size:.98rem}
html.crs-js .crs-c.is-track{display:none}
html.crs-js .crs-c.is-track.is-on{display:block}
html.crs-js .crs-cmp{display:none}
html.crs-js .crs-cmp.is-on{display:block}
.crs-cmp{margin:.55rem 0;padding:.1rem 0}
.crs-cmp h3{margin-bottom:.3rem}
#bs-aero h2{margin:.65rem 0 .2rem}
#bs-aero .crs-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));list-style:none;padding:0;align-items:start;margin:.15rem 0 0;gap:.55rem}
#bs-aero .crs-c{padding:.55rem .7rem;border:1px solid rgba(255,255,255,.2);border-radius:16px;box-sizing:border-box}
#bs-aero .crs-c h3{margin:.15rem 0 .05rem;font-size:1.25rem;line-height:1.65}
#bs-aero .crs-kicker{font-size:.85rem;line-height:1.65;letter-spacing:.04em;text-transform:uppercase}
#bs-aero .crs-c>p{margin:.15rem 0}
#bs-aero .crs-top{margin:.25rem 0 0}
#bs-aero .crs-top a{min-height:44px;display:inline-flex;align-items:center}
.crs-totop{position:fixed;z-index:1100;inset-inline-start:16px;bottom:16px;min-height:44px;min-width:44px;display:inline-flex;align-items:center;justify-content:center;padding:0 1rem;border-radius:999px;text-decoration:none;font-weight:800;color:#fff;background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),rgba(11,58,91,.9);border:1px solid rgba(255,255,255,.45);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 6px 18px rgba(0,0,0,.3)}
.crs-totop[hidden]{display:none!important}
.crs-fold{margin:.35rem 0 1rem;border-bottom:1px solid rgba(255,255,255,.16)}
.crs-fold>summary{cursor:pointer;min-height:44px;display:flex;align-items:center;gap:.65rem;list-style:none}
.crs-fold>summary::-webkit-details-marker{display:none}
.crs-fold>summary::before{content:"▸";flex:none;font-size:1rem;line-height:1}
.crs-fold[open]>summary::before{content:"▾"}
html[dir="rtl"] .crs-fold>summary::before{content:"◂"}
html[dir="rtl"] .crs-fold[open]>summary::before{content:"▾"}
.crs-fold>summary h2{margin:0;flex:1;font-size:1.15rem}
.crs-foldbar{display:flex;flex-wrap:wrap;gap:.45rem;margin:.4rem 0 1rem}
@media (prefers-reduced-motion:reduce){.crs-sticky,.crs-track,.crs-totop,.crs-fold{transition:none!important}}
@media print{.crs-sticky,.crs-totop,.crs-foldbar{display:none!important}html.crs-js .crs-c.is-track,html.crs-js .crs-cmp{display:block!important}html.crs-js .crs-tag{display:inline-block!important}.crs-fold,.crs-fold>*{display:block!important}}
#y1,#y2,#y3,#y4,.crs-fold{scroll-margin-top:11rem}
.crs section[id],.crs h2[id]{scroll-margin-top:13rem}
"""

JS = r"""<script id="study-tracks-js">(function(){
var root=document.querySelector(".crs");if(!root)return;
var bar=document.getElementById("trackbar");
var ids=["aeronautics","astronautics","jet","rocket"];
var names={};
if(bar){try{names=JSON.parse(bar.getAttribute("data-names")||"{}")}catch(e){}}
var prompt=document.getElementById("track-prompt");
var off=prompt?prompt.getAttribute("data-off"):"";
var on=prompt?prompt.getAttribute("data-on"):"";
function apply(id,push){
 root.querySelectorAll(".crs-c").forEach(function(c){
  var tracks=(c.getAttribute("data-tracks")||"core").split(/\s+/);
  if(c.classList.contains("is-track"))c.classList.toggle("is-on",!!(id&&tracks.indexOf(id)>=0));
  var el=c.querySelector(".crs-tag");if(!el)return;
  if(tracks.indexOf("core")>=0){el.textContent=el.getAttribute("data-core")||el.textContent;return}
  if(id&&tracks.indexOf(id)>=0)el.textContent=names[id]||id;
  else el.textContent=el.getAttribute("data-all")||el.textContent;
 });
 root.querySelectorAll(".crs-cmp").forEach(function(p){p.classList.toggle("is-on",p.getAttribute("data-cmp")===id)});
 if(bar)bar.querySelectorAll("button[data-track]").forEach(function(b){b.setAttribute("aria-pressed",b.getAttribute("data-track")===id?"true":"false")});
 if(prompt)prompt.textContent=(id&&names[id])?on.replace("{name}",names[id]):off;
 if(!bar)return;
 var u=new URL(location.href);
 if(id)u.searchParams.set("track",id);else u.searchParams.delete("track");
 if(ids.indexOf(u.hash.replace(/^#/,""))>=0)u.hash="";
 var next=u.pathname+u.search+u.hash, now=location.pathname+location.search+location.hash;
 if(next!==now){if(push)history.pushState({track:id},"",next);else history.replaceState({track:id},"",next)}
}
function fromUrl(){
 var q=new URLSearchParams(location.search).get("track")||"";
 if(ids.indexOf(q)>=0)return q;
 var h=(location.hash||"").replace(/^#/,"");
 return ids.indexOf(h)>=0?h:"";
}
if(bar){
 bar.addEventListener("click",function(e){var b=e.target.closest("button[data-track]");if(!b)return;var id=b.getAttribute("data-track");if(b.getAttribute("aria-pressed")==="true")id="";apply(id,true)});
 window.addEventListener("popstate",function(){apply(fromUrl(),false)});
 apply(fromUrl(),false);
 var sent=document.getElementById("track-sentinel");
 if(sent&&"IntersectionObserver" in window){new IntersectionObserver(function(es){bar.classList.toggle("is-stuck",es[0].intersectionRatio===0)},{threshold:[0],rootMargin:"-72px 0px 0px 0px"}).observe(sent)}
}
var top=document.querySelector("a.crs-totop");
if(top){function onScroll(){if(window.scrollY>480)top.removeAttribute("hidden");else top.setAttribute("hidden","")}
 window.addEventListener("scroll",onScroll,{passive:true});onScroll()}
document.addEventListener("click",function(e){
 var b=e.target.closest&&e.target.closest(".crs-watch-play");
 if(!b)return;
 var id=b.getAttribute("data-id")||"";
 if(!/^[A-Za-z0-9_-]{11}$/.test(id))return;
 var f=document.createElement("iframe");
 f.src="https://www.youtube-nocookie.com/embed/"+id+"?autoplay=1";
 f.title=b.getAttribute("data-title")||"";
 f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen";
 f.allowFullscreen=true;
 f.referrerPolicy="strict-origin-when-cross-origin";
 b.replaceWith(f);
});
})();</script>"""

FOLD_JS = r"""<script id="course-folds-js">(function(){
var root=document.querySelector(".crs");if(!root)return;
function openChain(el){
 if(!el)return;
 var d=el.closest?el.closest("details"):null;
 if(!d&&el.querySelector)d=el.querySelector("details.crs-fold");
 while(d){d.open=true;d=d.parentElement?d.parentElement.closest("details"):null}
}
function fromHash(){
 var id="";try{id=decodeURIComponent((location.hash||"").replace(/^#/,""))}catch(e){return}
 if(!id)return;var el=document.getElementById(id);if(!el)return;openChain(el);
 var target=(el.closest&&el.closest("details.crs-fold"))||el;
 if(target.scrollIntoView)target.scrollIntoView({block:"start",inline:"nearest",behavior:"instant"})
}
document.addEventListener("click",function(e){
 var a=e.target.closest&&e.target.closest("a[href*='#']");if(!a)return;
 var href=a.getAttribute("href")||"",i=href.indexOf("#");if(i<0)return;
 var id="";try{id=decodeURIComponent(href.slice(i+1))}catch(err){return}
 if(!id)return;var el=document.getElementById(id);if(!el||!root.contains(el))return;openChain(el)
},true);
root.addEventListener("click",function(e){
 var b=e.target.closest&&e.target.closest("[data-fold]");if(!b)return;
 var open=b.getAttribute("data-fold")==="all";
 root.querySelectorAll("details.crs-fold").forEach(function(d){d.open=open})
});
window.addEventListener("hashchange",fromHash);fromHash();
var top=document.querySelector("a.crs-totop");
if(top){function onScroll(){if(window.scrollY>480)top.removeAttribute("hidden");else top.setAttribute("hidden","")}
 window.addEventListener("scroll",onScroll,{passive:true});onScroll()}
})();</script>"""

def E(s):
    return html.escape(s, quote=True)

def fragment(lang, esc, live_for):
    """live_for(cid, title, desc) -> <li>…</li> for a roadmap course."""
    S = T[lang]
    parts = [f'<section class="page-hero hero-learn" id="top"><div class="page-hero-content">'
             f'<p class="crs-program">{E(S["title"])}</p><h1 id="bs-aero-title">{E(S["program"])}</h1>'
             f'<p>{E(S["note"])}</p></div></section>\n']
    rtl = ' dir="rtl"' if lang in ('ar', 'he') else ''
    parts.append(f'<div class="crs"{rtl}>')
    parts.append('<section class="crs-degree" id="bs-aero" aria-labelledby="bs-aero-title">')
    parts.append(f'<noscript><p>{E(S["noscript"])}</p></noscript>')
    parts.append(week_html(lang))
    parts.append(f'<p id="track-prompt" data-off="{E(S["prompt"])}" data-on="{E(S["prompt_on"])}">{E(S["prompt"])}</p>')
    names = E(json.dumps(S['tname'], ensure_ascii=False))
    buttons = ''.join(
        f'<button type="button" class="crs-track" data-track="{tid}" aria-pressed="false">'
        f'<span class="crs-track-n">{E(S["tname"][tid])}</span>'
        f'<span class="crs-track-d">{E(S["tdesc"][tid])}</span></button>' for tid in IDS)
    jumps = []
    for i, (y, _cs) in enumerate(RM.YEARS, 1):
        label = esc(y).split(' · ')[0]
        jumps.append(f'<a href="#y{i}">{label}</a>')
    parts.append(f'<div id="track-sentinel"></div><div class="crs-sticky" id="trackbar" data-names="{names}">'
                 f'<div class="crs-tracks" role="group" aria-label="{E(S["group"])}">{buttons}</div>'
                 f'<nav class="crs-jumps" aria-label="{E(S["years"])}">{"".join(jumps)}</nav></div>')
    top = f'<p class="crs-top"><a href="#top"><span aria-hidden="true">&#8593;</span> {esc("Back to top")}</a></p>'
    planned = {}
    for pid, year, tracks, model in RM.PLANNED:
        planned.setdefault(year, []).append((pid, tracks, model))
    for i, (y, cs) in enumerate(RM.YEARS, 1):
        parts.append(f'<section id="y{i}"><h2>{esc(y)}</h2><ul class="crs-grid">')
        for cid, title, desc in cs:
            parts.append(live_for(cid, title, desc))
        for pid, tracks, model in planned.get(i, []):
            parts.append(planned_card(lang, pid, tracks, model))
        parts.append('</ul>' + top + '</section>')
    parts.append(compare_html(lang, top))
    parts.append('</section><!-- PROGRAMS: add the next program as another section.crs-degree sibling. -->')
    parts.append('</div>')
    return ''.join(parts)

FILM_ID = 'c0EXAuWkMqA'
FILM_TITLE = 'Materials Science—A Building Block for the Future of Aerospace Technologies'
NASA_MEDIA = 'https://www.nasa.gov/nasa-brand-center/images-and-media/'

def week_html(lang):
    S = T[lang]
    before, after = S['week'].split('{course}')
    link = f'<a href="Intro_to_Aerospace_Engineering.html#u1">{E(S["week_course"])}</a>'
    sentence = f'<p class="crs-week">{E(before)}{link}{E(after)}</p>'
    title = E(FILM_TITLE)
    cred_before, cred_after = S['film_credit'].split('{name}')
    return (
        f'<div class="crs-hook">{sentence}'
        f'<figure class="crs-film"><div class="crs-watch-frame">'
        f'<button type="button" class="crs-watch-play" data-id="{FILM_ID}" data-title="{title}" '
        f'aria-label="{E(S["play"])}: {title}">'
        f'<span class="crs-watch-poster" aria-hidden="true"><span class="crs-watch-tri"></span></span>'
        f'<span class="crs-watch-cap"><span lang="en">{title}</span></span></button></div>'
        f'<figcaption><span class="crs-film-title" lang="en" dir="ltr">{title}</span>'
        f'<span class="crs-film-meta"><bdi lang="en" dir="ltr">NASA Glenn Research Center</bdi> · '
        f'<bdi dir="ltr">5:56</bdi> · {E(S["film_caps"])}</span>'
        f'<span class="crs-film-credit">{E(cred_before)}'
        f'<a href="{NASA_MEDIA}" rel="noopener license">{E(S["film_name"])}</a>{E(cred_after)}</span>'
        f'</figcaption></figure></div>'
    )

def _track_tag(S, label):
    return (f'<span class="crs-tag" data-core="{E(S["core"])}" data-all="{E(label)}">{E(label)}</span>')

def planned_card(lang, pid, tracks, model):
    S = T[lang]
    title, desc = S['card'][pid]
    if tracks == 'core':
        attr, extra, tag = 'core', '', ''
    else:
        attr = ' '.join(tracks)
        extra = ' is-track'
        tag = _track_tag(S, ' · '.join(S['tname'][t] for t in tracks))
    return (f'<li class="crs-c{extra}" data-tracks="{attr}">'
            f'<span class="crs-soon">{E(S["soon"])}</span>{tag}'
            f'<h3>{E(title)}</h3><p>{E(desc)}</p>'
            f'<p class="crs-kicker">{E(S["model"])} <bdi dir="ltr">{E(model)}</bdi></p>'
            f'<details class="crs-tip"><summary>{E(S["tip"])}</summary><p>{E(S["tip_body"])}</p></details></li>')

def compare_html(lang, top):
    S = T[lang]
    a, b = SRC[lang]
    body = ''.join(f'<p>{E(p)}</p>' for p in S['cmp'])
    panels = ''.join(f'<div class="crs-cmp" data-cmp="{tid}"><h3>{E(S["tname"][tid])}</h3><p>{E(S["track_cmp"][tid])}</p></div>' for tid in IDS)
    return (f'<section id="compare"><h2>{E(S["cmp_h"])}</h2><div class="crs-disc">{body}</div>{panels}'
            f'<p class="crs-src"><a href="{SRC_URL[0]}" rel="noopener">{E(a)}</a> · '
            f'<a href="{SRC_URL[1]}" rel="noopener">{E(b)}</a></p>{top}</section>')

def live_card(lang, cid, title, desc, esc, mod, href, english):
    S = T[lang]
    role = RM.ROLE[cid]
    if role == 'core':
        tracks, extra, tag = 'core', '', ''
    else:
        tracks, extra = ' '.join(role), ' is-track'
        tag = _track_tag(S, ' · '.join(S['tname'][t] for t in role))
    note = ' <span lang="en">(English)</span>' if english else ''
    blurb = esc(desc)
    return (f'<li class="crs-c live{extra}" data-tracks="{tracks}">{tag}'
            f'<h3><a href="{href}">{esc(title)}</a>{note}</h3><p>{blurb}</p>'
            f'<p class="crs-kicker">{esc(mod.CODE)}</p></li>')

def _upsert(s, start, end, block, anchor):
    if start in s:
        return re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _m: block, s, count=1, flags=re.S)
    return s.replace(anchor, block + '\n' + anchor, 1)

def install(path, lang, main_inner, back, title, desc):
    if not os.path.exists(path):
        raise SystemExit(f'missing {path}')
    s = open(path, encoding='utf-8').read()
    new_main = '<main id="main">\n' + main_inner + '</main>'
    s, n = re.subn(r'<main id="main">.*?</main>', new_main, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'main splice failed {path}')
    full = title + ' | Saving Planets'
    s = re.sub(r'<title>.*?</title>', f'<title>{E(full)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"',
               lambda m: m.group(1) + E(desc) + '"', s)
    s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"',
               lambda m: m.group(1) + E(full) + '"', s)
    s = re.sub(r'("name"\s*:\s*")([^"\\]*)(")', lambda m: m.group(1) + title.replace('\\', '\\\\').replace('"', '\\"') + m.group(3), s, count=1)
    s = re.sub(r'("description"\s*:\s*")([^"\\]*)(")', lambda m: m.group(1) + desc.replace('\\', '\\\\').replace('"', '\\"') + m.group(3), s, count=1)
    style = '<!-- STUDYCSS:START --><style id="study-tracks-css">' + CSS + '</style><!-- STUDYCSS:END -->'
    boot = '<!-- STUDYBOOT:START --><script>document.documentElement.classList.add("crs-js")</script><!-- STUDYBOOT:END -->'
    s = _upsert(s, '<!-- STUDYCSS:START -->', '<!-- STUDYCSS:END -->', style, '</head>')
    s = _upsert(s, '<!-- STUDYBOOT:START -->', '<!-- STUDYBOOT:END -->', boot, '</head>')
    s = _upsert(s, '<script id="study-tracks-js">', '</script>', JS, '</body>')
    # The upsert end token </script> is too broad if the block was missing and we inserted before </body>.
    # When the script is new, _upsert inserts the whole <script>…</script> before </body>. Good.
    # When it exists, the regex from <script id= to the first </script> replaces it. Good.
    btn = f'<a class="crs-totop" href="#top" hidden><span aria-hidden="true">&#8593;</span> {E(back)}</a>'
    if 'class="crs-totop"' in s:
        s = re.sub(r'<a class="crs-totop"[^>]*>.*?</a>', btn, s, count=1, flags=re.S)
    elif '<a class="sticky-help"' in s:
        s = s.replace('<a class="sticky-help"', btn + '<a class="sticky-help"', 1)
    else:
        s = s.replace('</main>', '</main>' + btn, 1)
    for old in ('20261024h', '20261102a', '20261102b'):
        s = s.replace(f'courses.css?v={old}', 'courses.css?v=20261124a')
    open(path, 'w', encoding='utf-8').write(s)

PAGE = 'Undergraduate_Studies.html'
REDIRECT = 'Courses.html'
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')

def hub_path(lang, name):
    return name if lang == 'en' else f'{lang}/{name}'

def prepare_shell(lang):
    """Copy the full Courses.html shell once. Later builds edit Undergraduate_Studies.html in place."""
    import shutil
    dest, src = hub_path(lang, PAGE), hub_path(lang, REDIRECT)
    if os.path.exists(dest):
        head = open(dest, encoding='utf-8').read(2500)
        if 'http-equiv="refresh"' not in head and '<main id="main">' in open(dest, encoding='utf-8').read():
            return dest
    if not os.path.exists(src):
        raise SystemExit(f'missing shell {src}')
    shutil.copyfile(src, dest)
    return dest

def retarget_page(path):
    s = open(path, encoding='utf-8').read()
    s = s.replace(REDIRECT, PAGE)
    open(path, 'w', encoding='utf-8').write(s)

def write_redirect(lang):
    """Old Courses.html URL. Meta refresh plus a script that keeps ?track and #hash."""
    title = T[lang]['title'] + ' | Saving Planets'
    canonical = 'https://www.savingplanets.com/' + ('' if lang == 'en' else lang + '/') + PAGE
    rtl = ' dir="rtl"' if lang in ('ar', 'he') else ''
    page = PAGE
    doc = (
        '<!DOCTYPE html>\n'
        f'<html lang="{lang}"{rtl}>\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex">\n'
        f'<title>{E(title)}</title>\n'
        f'<link rel="canonical" href="{canonical}">\n'
        f'<meta http-equiv="refresh" content="0; url={page}">\n'
        '<script>(function(){var u=' + json.dumps(page) + '+location.search+location.hash;'
        'var m=document.querySelector(\'meta[http-equiv="refresh"]\');'
        'if(m)m.setAttribute("content","0; url="+u);location.replace(u);})();</script>\n'
        '<link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">\n'
        '</head>\n<body>\n'
        f'<p><a href="{page}">{E(T[lang]["title"])}</a></p>\n'
        '</body>\n</html>\n'
    )
    open(hub_path(lang, REDIRECT), 'w', encoding='utf-8').write(doc)

def write_redirects():
    for lang in LANGS:
        write_redirect(lang)

def ensure_courses_css():
    p = 'assets/courses.css'
    s = open(p, encoding='utf-8').read()
    if '/* STUDY-TRACKS */' in s:
        s = re.sub(r'/\* STUDY-TRACKS \*/.*\Z', CSS, s, flags=re.S)
    else:
        if not s.endswith('\n'):
            s += '\n'
        s += '\n' + CSS
    open(p, 'w', encoding='utf-8').write(s)
