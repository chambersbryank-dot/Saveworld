#!/usr/bin/env python3
"""Nov 3 (founder): Ways to Help redesign. Turns the generated per-hub tables (build-ways-to-help.py + i18n) into
two sections, 'Donations' and 'Roll up your sleeves', each grouped by hub (chips + collapsible hub groups) with
compact cards: org name, ONE sentence (first sentence of our own solution page's meta description in that language),
and the org's official button. Links/vetting unchanged: Donations only lists rows the data already marks give=1.
Run after i18n (weekly-sync). Idempotent: skips a page whose tables are already converted."""
import re, html, os
from bs4 import BeautifulSoup
LANGS = ['', 'es/', 'fr/', 'ar/', 'he/', 'it/']
EMOJI = {'earth-observation':'🛰️','forests':'🌳','lakes':'🏞️','ocean':'🌊','planetary-defense':'☄️','polar':'🧊',
         'project-rawane':'🚀','rivers':'🏞','space':'🪐','space-disposal':'♻️','space-weather':'☀️'}
T = {
 '': dict(h='Ways to Help', intro='Two ways to help: give to an organization, or roll up your sleeves. Every button opens the organization’s own official page. Saving Planets never receives the money.',
   don='Donations', don_s='Official donation pages, grouped by hub.', vol='Roll up your sleeves', vol_s='Volunteer, citizen science and hands-on work, grouped by hub.',
   search='Search organizations or solutions', all='All hubs', b_don='Donate', b_vol='Volunteer', b_con='Contact', orgs='organizations', none='Nothing matches. Try another word or hub.',
   sol='Solution page', how='How this works', jump='Jump to'),
 'es/': dict(h='Formas de ayudar', intro='Dos formas de ayudar: donar a una organización o arremangarse. Cada botón abre la página oficial de la organización. Saving Planets nunca recibe el dinero.',
   don='Donaciones', don_s='Páginas oficiales de donación, por tema.', vol='Manos a la obra', vol_s='Voluntariado, ciencia ciudadana y trabajo práctico, por tema.',
   search='Busca organizaciones o soluciones', all='Todos los temas', b_don='Donar', b_vol='Voluntariado', b_con='Contacto', orgs='organizaciones', none='No hay resultados. Prueba otra palabra u otro tema.',
   sol='Página de la solución', how='Cómo funciona', jump='Ir a'),
 'fr/': dict(h='Comment aider', intro='Deux façons d’aider : donner à une organisation ou retrousser ses manches. Chaque bouton ouvre la page officielle de l’organisation. Saving Planets ne reçoit jamais l’argent.',
   don='Dons', don_s='Pages de dons officielles, par thème.', vol='Retroussez vos manches', vol_s='Bénévolat, science participative et travail de terrain, par thème.',
   search='Rechercher une organisation ou une solution', all='Tous les thèmes', b_don='Faire un don', b_vol='Bénévolat', b_con='Contact', orgs='organisations', none='Aucun résultat. Essayez un autre mot ou thème.',
   sol='Page de la solution', how='Comment ça marche', jump='Aller à'),
 'ar/': dict(h='طرق المساعدة', intro='طريقتان للمساعدة: التبرع لمنظمة، أو المشاركة بنفسك. كل زر يفتح الصفحة الرسمية للمنظمة. لا تتلقى Saving Planets أي أموال.',
   don='التبرعات', don_s='صفحات التبرع الرسمية، حسب المحور.', vol='شارك بنفسك', vol_s='التطوع وعلوم المواطن والعمل الميداني، حسب المحور.',
   search='ابحث عن منظمة أو حل', all='كل المحاور', b_don='تبرّع', b_vol='تطوّع', b_con='تواصل', orgs='منظمة', none='لا نتائج. جرّب كلمة أو محورًا آخر.',
   sol='صفحة الحل', how='كيف يعمل هذا', jump='انتقل إلى'),
 'he/': dict(h='דרכים לעזור', intro='שתי דרכים לעזור: לתרום לארגון, או להפשיל שרוולים. כל כפתור פותח את העמוד הרשמי של הארגון. Saving Planets אינו מקבל את הכסף.',
   don='תרומות', don_s='עמודי תרומה רשמיים, לפי נושא.', vol='מפשילים שרוולים', vol_s='התנדבות, מדע אזרחי ועבודה בשטח, לפי נושא.',
   search='חיפוש ארגון או פתרון', all='כל הנושאים', b_don='לתרומה', b_vol='להתנדבות', b_con='יצירת קשר', orgs='ארגונים', none='אין תוצאות. נסו מילה או נושא אחרים.',
   sol='עמוד הפתרון', how='איך זה עובד', jump='מעבר אל'),
 'it/': dict(h='Come aiutare', intro='Due modi per aiutare: donare a un’organizzazione o rimboccarsi le maniche. Ogni pulsante apre la pagina ufficiale dell’organizzazione. Saving Planets non riceve mai il denaro.',
   don='Donazioni', don_s='Pagine ufficiali per donare, per tema.', vol='Rimbocchiamoci le maniche', vol_s='Volontariato, citizen science e lavoro sul campo, per tema.',
   search='Cerca organizzazioni o soluzioni', all='Tutti i temi', b_don='Dona', b_vol='Volontariato', b_con='Contatti', orgs='organizzazioni', none='Nessun risultato. Prova un’altra parola o un altro tema.',
   sol='Pagina della soluzione', how='Come funziona', jump='Vai a'),
}
E = lambda s: html.escape(s, quote=True)
EXT = ' target="_blank" rel="noopener"'
CSS = ('<style>.wh{max-width:1100px;margin:0 auto;padding:0 1.25rem}.wh-intro{font-size:1.1rem;max-width:46rem}.wh-jump{display:flex;gap:.6rem;flex-wrap:wrap;margin:1rem 0 1.5rem}'
 '.wh-jump a{display:inline-flex;align-items:center;gap:.4rem;min-height:44px;padding:.4rem 1rem;border-radius:999px;font-weight:700;text-decoration:none;background:#1b6e4b;color:#fff}.wh-jump a.v{background:#0b5c8a}'
 '.wh-sec{scroll-margin-top:90px;margin:2rem 0}.wh-sec>h2{display:flex;align-items:center;gap:.5rem;margin:0 0 .2rem}.wh-sub{margin:0 0 .8rem;opacity:.85}'
 '.wh-bar{position:sticky;top:var(--spn-h,64px);z-index:5;background:rgba(7,16,24,.96);padding:.6rem 0;margin:0 0 .6rem}html:not(.dark) .wh-bar{background:rgba(255,255,255,.97)}'
 '.wh-q{width:100%;box-sizing:border-box;font:inherit;padding:.6rem .9rem;min-height:44px;border-radius:10px;border:1px solid rgba(127,127,127,.5);background:transparent;color:inherit}'
 '.wh-chips{display:flex;gap:.4rem;overflow-x:auto;padding:.5rem 0 .2rem;scrollbar-width:thin}.wh-chip{flex:none;font:inherit;font-size:.9rem;min-height:40px;padding:.3rem .8rem;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer;white-space:nowrap}'
 '.wh-chip[aria-pressed=true]{background:#1b6e4b;border-color:#1b6e4b;color:#fff}.wh-sec.v .wh-chip[aria-pressed=true]{background:#0b5c8a;border-color:#0b5c8a}'
 '.wh-hub{border:1px solid rgba(127,127,127,.3);border-radius:12px;margin:.5rem 0;scroll-margin-top:150px}.wh-hub>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:.6rem;padding:.8rem 1rem;min-height:44px;font-weight:700;font-size:1.05rem}'
 '.wh-hub>summary::-webkit-details-marker{display:none}.wh-hub>summary::after{content:"+";margin-inline-start:auto;font-size:1.4rem;line-height:1}.wh-hub[open]>summary::after{content:"\\2212"}.wh-n{font-weight:400;opacity:.75;font-size:.9rem}'
 '.wh-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.7rem;padding:0 1rem 1rem;margin:0;list-style:none}'
 '.wh-card{display:flex;flex-direction:column;gap:.35rem;border-radius:10px;padding:.8rem .9rem;background:rgba(127,127,127,.09)}.wh-card h3{font-size:1rem;margin:0}.wh-card p{margin:0;font-size:.92rem;line-height:1.4}'
 '.wh-card .wh-s{font-size:.82rem;opacity:.8}.wh-card .btn{margin-top:auto;align-self:flex-start;min-height:40px;display:inline-flex;align-items:center}.wh-card .wh-c{background:transparent;border:1px solid currentColor;color:inherit}'
 '.wh-none{padding:1rem;opacity:.85}.wh [hidden]{display:none!important}.wh-chip:focus-visible,.wh-q:focus-visible,.wh-hub>summary:focus-visible,.wh-jump a:focus-visible{outline:3px solid #f5b400;outline-offset:2px}'
 '.wh-how{margin:2rem 0}.wh-how summary{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center}'
 '@media (prefers-reduced-motion:no-preference){.wh-hub[open] .wh-grid{animation:whf .2s ease}}@keyframes whf{from{opacity:0}to{opacity:1}}</style>')
JS = ('<script>(function(){[].forEach.call(document.querySelectorAll(".wh-sec"),function(sec){var q=sec.querySelector(".wh-q"),chips=sec.querySelectorAll(".wh-chip"),hubs=[].slice.call(sec.querySelectorAll(".wh-hub")),none=sec.querySelector(".wh-none"),hub="all";'
 'function run(){var t=(q.value||"").trim().toLowerCase(),any=0;hubs.forEach(function(h){var ok=hub=="all"||h.getAttribute("data-hub")==hub,n=0;[].forEach.call(h.querySelectorAll(".wh-card"),function(c){var m=!t||c.textContent.toLowerCase().indexOf(t)>-1;c.hidden=!m;if(m)n++;});'
 'h.hidden=!ok||!n;if(ok&&n){any=1;if(t||hub!="all")h.open=true;}});none.hidden=!!any;}'
 'q.addEventListener("input",run);[].forEach.call(chips,function(c){c.addEventListener("click",function(){hub=c.getAttribute("data-hub");[].forEach.call(chips,function(x){x.setAttribute("aria-pressed",x===c?"true":"false")});if(hub=="all")hubs.forEach(function(h){h.open=false});run();});});});'
 'if(location.hash){var el=document.getElementById(location.hash.slice(1));if(el&&el.tagName=="DETAILS")el.open=true;}})();</script>')

def sentence(lang, href):
    p = os.path.normpath(os.path.join(lang, href.split('#')[0]))
    if not os.path.exists(p): return ''
    m = re.search(r'<meta name="description" content="([^"]*)"', open(p, encoding='utf8').read())
    if not m: return ''
    d = html.unescape(m.group(1)).strip()
    m2 = re.match(r'(.+?[.!?。])(\s|$)', d)
    return (m2.group(1) if m2 else d)

def build(lang):
    f = lang + 'Ways_to_Help.html'; s = open(f, encoding='utf8').read()
    a = s.find('<section class="five-ws" id="donate">'); b = s.find('<!-- WTH-ALL:END -->')
    if a < 0 or b < 0 or 'class="wth-hub"' not in s[a:b]: print('skip (already cards)', f); return
    t = T[lang]; soup = BeautifulSoup(s[a:b], 'html.parser')
    how = soup.select_one('#solution .impact-box')
    hubs = []
    for hd in soup.select('div.wth-hub'):
        hid = hd['id']; name = hd.h3.get_text(strip=True); hub_href = hd.h3.a['href'] if hd.h3.a else ''
        rows = []
        for tr in hd.select('tbody tr'):
            td = tr.find_all('td'); sa = td[0].a
            don = td[2].a; vol = td[3].a
            rows.append(dict(sol=sa.get_text(strip=True), sh=sa['href'], org=td[1].get_text(strip=True),
                give=tr.get('data-give') == '1', join=tr.get('data-join') == '1', dh=don['href'] if don else '', vh=(vol or don)['href'] if (vol or don) else ''))
        hubs.append((hid, name, hub_href, rows))
    def section(kind):
        v = kind == 'vol'; key = 'help' if v else 'donate-list'
        sid = 'roll-up-your-sleeves' if v else 'donations'
        out = [f'<section class="wh-sec{" v" if v else ""}" id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h">{"🧤" if v else "💚"} {E(t[kind])}</h2><p class="wh-sub">{E(t[kind+"_s"])}</p>',
               f'<div class="wh-bar"><input class="wh-q" type="search" aria-label="{E(t["search"])}" placeholder="{E(t["search"])}"><div class="wh-chips" role="group" aria-label="{E(t["jump"])}"><button type="button" class="wh-chip" data-hub="all" aria-pressed="true">{E(t["all"])}</button>']
        groups = []
        for hid, name, hh, rows in hubs:
            rs = [r for r in rows if (r['vh'] if v else (r['give'] and r['dh']))]
            if not rs: continue
            out.append(f'<button type="button" class="wh-chip" data-hub="{hid}" aria-pressed="false">{EMOJI.get(hid[4:],"")} {E(name)}</button>')
            cards = []
            for r in rs:
                if v: url, lab, cls = (r['vh'], t['b_vol'], '') if r['join'] else (r['vh'], t['b_con'], ' wh-c')
                else: url, lab, cls = r['dh'], t['b_don'], ''
                sen = sentence(lang, r['sh'])
                cards.append(f'<li class="wh-card"><h3>{E(r["org"])}</h3>' + (f'<p>{E(sen)}</p>' if sen else '') +
                    f'<a class="wh-s" href="{E(r["sh"])}">{E(r["sol"])}</a><a class="btn help-btn{cls}" href="{E(url)}"{EXT}>{E(lab)}<span class="sr-only"> – {E(r["org"])}</span></a>' + (f'<a class="wh-s" href="{E(r["dh"])}"{EXT}>{E(t["b_con"])}</a>' if v and r['dh'] and r['dh'] != url and not r['give'] else '') + (f'<a class="wh-s" href="{E(r["dh"])}"{EXT}>💚 {E(t["b_don"])}</a>' if v and r['give'] and r['dh'] else '') + '</li>')
            gid = (('vol-' if v else 'don-') + hid) if v or True else hid
            groups.append(f'<details class="wh-hub" id="{gid}" data-hub="{hid}"><summary>{EMOJI.get(hid[4:],"")} {E(name)} <span class="wh-n">{len(rs)} {E(t["orgs"])}</span></summary><ul class="wh-grid">{"".join(cards)}</ul></details>')
        out.append('</div></div>'); out += groups
        out.append(f'<p class="wh-none" hidden>{E(t["none"])}</p></section>')
        return ''.join(out)
    new = (CSS + f'<section class="five-ws wh" id="donate" aria-label="{E(t["h"])}"><p class="wh-intro">{E(t["intro"])}</p>'
           f'<p class="wh-jump"><a href="#donations">💚 {E(t["don"])}</a><a class="v" href="#roll-up-your-sleeves">🧤 {E(t["vol"])}</a></p>'
           + section('don') + section('vol') +
           (f'<details class="wh-how" id="solution"><summary>{E(t["how"])}</summary>{how.decode_contents()}</details>' if how else '') + JS + '</section>')
    s = s[:a] + new + s[b:]
    open(f, 'w', encoding='utf8').write(s); print('ok', f)

for L in LANGS: build(L)
