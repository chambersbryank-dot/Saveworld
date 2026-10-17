#!/usr/bin/env python3
"""Oct 16 SI Helper pilot: (1) Ask SI widget on Teachers.html (5 languages) between <!-- SIHELPER:START/END --> markers,
(2) SI_Helper.html 'How SI Helper works and what we don't keep' (5 languages, Kids_Map shell via build-learn.shell),
(3) SI Helper section in Privacy.html (5 languages, same markers; Oct 16: + unanswered-question log line #si-unanswered). Text: scripts/si_helper_text.py. Worker: workers/si-helper.
Front-end: assets/si-helper.js. Run after build-learn.py (and after i18n/trust builds). Idempotent."""
import re, os, sys, json, datetime, importlib.util
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
import si_helper_text as X
LANGS, d, rd, wr, esc, SITE, href = BL.LANGS, BL.d, BL.rd, BL.wr, BL.esc, BL.SITE, BL.sf.href
V = '20261016V'  # Oct 16: unanswered-question log + outside sources (was 20261016S)
MARK = re.compile(r'<!-- SIHELPER:START -->.*?<!-- SIHELPER:END -->', re.S)
CSS = ('.si-help{max-width:900px;margin:1.2rem auto;padding:1.1rem 1.25rem;border-radius:18px;border:1px solid rgba(124,170,255,.5);background:rgba(124,170,255,.08)}'
       '.si-help h2{margin:.1rem 0 .4rem}.si-pilot{font-size:.78rem;font-weight:800;padding:.1rem .55rem;border-radius:999px;background:#ffd54a;color:#1a1300;vertical-align:middle}'
       '.si-form{display:grid;gap:.5rem}.si-form label{font-weight:700}.si-form textarea{font:inherit;font-size:1rem;min-height:5.5rem;padding:.6rem .7rem;border-radius:12px;width:100%;box-sizing:border-box;resize:vertical}'
       '.si-form button{justify-self:start;min-height:44px;padding:.45rem 1.3rem;border-radius:999px;font:inherit;font-weight:800;cursor:pointer;background:#ffd54a;color:#1a1300;border:0}'
       '.si-form button[disabled]{opacity:.6;cursor:wait}.si-note,.si-warn{font-size:.9rem;opacity:.9;margin:.2rem 0}.si-out{margin:.6rem 0;line-height:1.55;white-space:pre-line}'
       '.si-out:empty{display:none}.si-out .si-ans{padding:.7rem .9rem;border-radius:12px;background:rgba(0,0,0,.2)}.si-out h3{font-size:1rem;margin:.7rem 0 .3rem}'
       '.si-out ol{margin:.2rem 0;padding-inline-start:1.4rem}.si-out li{margin:.25rem 0}.si-out a{word-break:break-word}.si-help :focus-visible{outline:3px solid #ffd54a;outline-offset:2px}')
def t(k, l): return esc(X.W[k][l])
def hosts():  # Oct 16: outside hosts the widget may link to (only for 'none' replies) = hosts in assets/data/trusted-sources.json
    from urllib.parse import urlparse
    src = json.load(open('assets/data/trusted-sources.json', encoding='utf8'))['sources']
    return sorted({urlparse(u).hostname for x in src for u in [x['url'], *(x.get('urls') or {}).values()]})
def widget(l):
    pre = '' if l == 'en' else '../'
    tr = {k: X.W[k][l] for k in ('wait', 'src', 'short', 'neterr', 'ext')}
    return (f'<!-- SIHELPER:START --><style>{CSS}</style><section class="si-help" id="ask-si" aria-labelledby="si-h"><h2 id="si-h">{t("h", l)} <span class="si-pilot">SI</span></h2><p>{t("intro", l)}</p>'
            f'<form class="si-form" novalidate data-endpoint="{X.ENDPOINT}" data-sitekey="{X.SITEKEY}" data-lang="{l}" data-hosts="{' '.join(hosts())}" data-t="{esc(json.dumps(tr, ensure_ascii=False))}">'
            f'<label for="si-q">{t("label", l)}</label><textarea id="si-q" name="q" maxlength="400" rows="3" dir="auto" autocomplete="off" placeholder="{t("ph", l)}" aria-describedby="si-note"></textarea>'
            f'<p class="si-note" id="si-note">{t("nopii", l)}</p><button type="submit">{t("ask", l)}</button><div class="si-ts"></div></form>'
            f'<div class="si-out" role="status" aria-live="polite"></div>'
            f'<p class="si-warn">{t("warn", l)} <a href="{href(l, "SI_Helper.html")}">{t("how", l)}</a></p></section>'
            f'<script src="{pre}assets/si-helper.js?v={V}" defer></script><!-- SIHELPER:END -->')
def teachers(l):
    p = d(l) + 'Teachers.html'; s = MARK.sub('', rd(p))
    anchor = '<!-- EDU-LINKS:END -->'
    s = s.replace(anchor, anchor + widget(l), 1) if anchor in s else re.sub(r'(</section>\n)', lambda m: m.group(1) + widget(l), s, count=1)
    assert s.count('SIHELPER:START') == 1, p
    return wr(p, s)
def privacy(l):
    p = d(l) + 'Privacy.html'
    if not os.path.exists(p): return 0
    s = MARK.sub('', rd(p))
    blk = (f'<!-- SIHELPER:START --><section class="five-ws" id="si-helper"><h2>{esc(X.PRIV_H[l])}</h2><p>{esc(X.PRIV_P[l])} '
           f'<a href="{href(l, "SI_Helper.html")}">{t("how", l)}</a></p><p id="si-unanswered">{esc(X.UQ_P[l])}</p></section><!-- SIHELPER:END -->')
    a = '<section class="help-actions" id="more">'
    s = s.replace(a, blk + a, 1) if a in s else s.replace('</main>', blk + '</main>', 1)
    assert s.count('SIHELPER:START') == 1, p
    return wr(p, s)
def page(l):
    secs = ''.join(f'<section><h2>{esc(h[l])}</h2>' + ''.join(f'<p>{esc(x[l])}</p>' for x in ps) + '</section>' for h, ps in X.PAGE)
    main = (BL.hero(X.PAGE_TITLE[l], X.PAGE_DESC[l]) + f'<div class="lw"><p><span class="si-pilot" style="font-weight:800;background:#ffd54a;color:#1a1300;border-radius:999px;padding:.1rem .55rem">SI · pilot</span></p>{secs}'
            f'<p class="lbox ex"><a href="{href(l, "Teachers.html")}#ask-si">{t("h", l)}</a> · <a href="{href(l, "Privacy.html")}#si-helper">{esc(X.PRIV_H[l])}</a></p></div>\n')
    return BL.shell(l, 'SI_Helper.html', X.PAGE_TITLE[l], X.PAGE_DESC[l], main, ld_type='WebPage')
if __name__ == '__main__':
    ch = 0
    for l in LANGS: ch += teachers(l) + privacy(l) + wr(d(l) + 'SI_Helper.html', page(l))
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        loc = f'{SITE}{d(l)}SI_Helper.html'
        if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s); print(f'build-si-helper: writes={ch}')
