#!/usr/bin/env python3
"""Study this: a compact course block beside For Teachers.

Data: assets/data/study.json. Each solution hub has default disciplines, a course
now, a course next, go-further links and a career. A page override replaces any
of those fields. A coming-soon course has no page and is never linked.

Writes <!-- STUDY --> into the pilot pages only (all six languages, where the
page exists), the same way scripts/build-standards.py writes STANDARDS.
`--all` is the later rollout: every solution page whose merged record has a
sourced fact, a live course and a career. Idempotent. Run after i18n-build.
"""
import html, json, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
STYLEV = '20261122a'
D = json.load(open('assets/data/study.json', encoding='utf8'))
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
def lang_of(obj, lang):
    if lang not in obj: raise SystemExit(f'missing {lang} translation')
    return obj[lang]
def primary_hubs():
    s = rd('Solutions.html'); out = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        h = re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)
        for u in re.findall(r'data-url="([^"#]+)"', m.group(2)): out.setdefault(u, h)
    return out
PH = primary_hubs()
def merged(page):
    hub = PH.get(page, '')
    base = dict(D['hubs'].get(hub, {}))
    over = D['pages'].get(page, {})
    for k, v in over.items():
        if v is not None: base[k] = v
    base['_hub'] = hub
    return base
def ready(rec):
    return bool(rec.get('disciplines') and rec.get('why') and rec.get('course_now') and rec.get('further') and rec.get('career'))
def course_file(lang, course):
    c = D['courses'][course]
    if c['status'] != 'live' or not c.get('page'): return None
    return ('' if lang == 'en' else lang + '/') + c['page']
def money(n):
    return f'<bdi dir="ltr">${n:,}</bdi>'
def ext(url, text):
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(text)}</a>'
def block(lang, page):
    u = D['ui']; rec = merged(page)
    if not ready(rec): return ''
    discs = ''.join(f'<li>{esc(lang_of(D["disciplines"][i], lang))}</li>' for i in rec['disciplines'])
    fact = D['facts'][rec['why']]
    why = (f'<p>{esc(lang_of(fact["text"], lang))}</p>'
           f'<p class="std-note">{esc(lang_of(u["source"], lang))} {ext(fact["url"], lang_of(fact["source"], lang))}</p>')
    now_id = rec['course_now']
    path = course_file(lang, now_id)
    if not path or not os.path.exists(path):
        raise SystemExit(f'{page} ({lang}): course page missing: {path}')
    now = D['courses'][now_id]
    now_html = f'<p class="help-btns"><a class="btn help-btn" href="{esc(now["page"])}">{esc(lang_of(now["title"], lang))}</a></p>'
    fields = [
        (u['learn'], f'<ul class="std-list">{discs}</ul>', False),
        (u['why'], why, False),
        (u['now'], now_html, False),
    ]
    nxt = rec.get('course_next')
    if nxt:
        c = D['courses'][nxt]
        if c['status'] != 'soon' or c.get('page'):
            live = course_file(lang, nxt)
            if not live or not os.path.exists(live):
                raise SystemExit(f'{page}: next course {nxt} is not a live page and is not marked soon')
            fields.append((u['next'], f'<p class="help-btns"><a class="btn help-btn" href="{esc(c["page"])}">{esc(lang_of(c["title"], lang))}</a></p>', False))
        else:
            fields.append((u['next'], f'<p>{esc(lang_of(c["title"], lang))} <span class="study-soon">{esc(lang_of(u["soon"], lang))}</span></p>', False))
    lis = ''.join(f'<li>{ext(D["resources"][i]["url"], lang_of(D["resources"][i]["title"], lang))}</li>' for i in rec['further'])
    fields.append((u['further'], f'<ul class="std-list">{lis}</ul>', True))
    car = D['careers'][rec['career']]
    when = f'{esc(lang_of(car["as_of"], lang))} <bdi dir="ltr">{car["year"]}</bdi>'
    career = (f'<p class="study-career">{ext(car["url"], lang_of(car["title"], lang))}</p>'
              f'<p class="std-note">{esc(lang_of(u["median"], lang))} {money(car["pay"])} {esc(lang_of(u["per_year"], lang))}. '
              f'{esc(lang_of(u["source"], lang))} {ext(car["url"], lang_of(u["handbook"], lang))}, {when}.</p>')
    fields.append((u['career'], career, True))
    body = ''.join(f'<div class="study-field{" study-span" if span else ""}"><h3>{esc(lang_of(h, lang))}</h3>{inner}</div>' for h, inner, span in fields)
    return (f'<!-- STUDY:START --><section class="study-box" id="study-this" aria-labelledby="study-h">'
            f'<h2 id="study-h">{esc(lang_of(u["title"], lang))}</h2><div class="study-grid">{body}</div></section><!-- STUDY:END -->')
MARK = re.compile(r'<!-- STUDY:START -->.*?<!-- STUDY:END -->', re.S)
def put(s, new):
    s = MARK.sub('', s)
    if not new: return s
    i = s.find('<!-- TEACHER:START -->')
    if i < 0: return s
    s = s[:i] + new + s[i:]
    return re.sub(r'(styles\.css\?v=)[\w.-]+', r'\g<1>' + STYLEV, s)
CSS = """/* STUDY:START */
/* Same shell as .teacher-box, same inner card as .std-box, same crystal button as a.help-btn. */
body.toc-sub .study-box{max-width:1100px;margin:2rem auto;padding:1.2rem 1.4rem;border-radius:14px;border:1px solid rgba(127,127,127,.35);background:rgba(21,32,51,.55)}
body.toc-sub .study-box h2{margin-top:0}
.study-grid{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}
.study-field{margin:0;padding:.9rem 1rem;border-radius:14px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.05)}
body.toc-sub .study-field h3{margin:.1rem 0 .35rem;font-size:1.05rem}
.study-span{grid-column:1 / -1}
.study-box .std-list{margin:0;padding-inline-start:1.1rem}
.study-box .std-list li{margin:.35rem 0}
.study-box .std-note{font-size:.85rem;opacity:.85;margin:.35rem 0 0}
.study-box .std-list a,.study-box .std-note a,.study-box .study-career a{text-decoration:underline;text-underline-offset:.12em}
.study-box .help-btns{justify-content:flex-start;margin:0}
.study-box .help-btns .btn{margin-top:0}
.study-soon{display:inline-block;margin-inline-start:.45rem;padding:.12rem .6rem;border-radius:999px;background:rgba(143,211,255,.18);font-size:.8rem;font-weight:800;letter-spacing:.02em}
@media (max-width:720px){.study-grid{grid-template-columns:1fr}}
@media (max-width:1150px){body.toc-sub .study-box{margin-left:1rem;margin-right:1rem}}
@media print{.study-box{display:none !important}}
[dir=rtl] .study-box .help-btns{justify-content:flex-start}
/* STUDY:END */"""
def check_catalog():
    hubs = set(re.findall(r'data-hub="([^"]+)"', rd('Solutions.html')))
    missing = hubs - set(D['hubs'])
    if missing: raise SystemExit('study.json is missing hubs: ' + ', '.join(sorted(missing)))
    langs = set(LANGS)
    for key, obj in D['ui'].items():
        if set(obj) != langs: raise SystemExit(f'ui.{key} languages')
    for cid, c in D['courses'].items():
        if c['status'] == 'soon':
            if c.get('page'): raise SystemExit(f'{cid} is soon but has a page')
        elif c['status'] == 'live':
            for lang in LANGS:
                p = course_file(lang, cid)
                if not os.path.exists(p): raise SystemExit(f'missing {p}')
        else:
            raise SystemExit(f'{cid} status')
        if set(c['title']) != langs: raise SystemExit(f'{cid} title languages')
    for rid, r in D['resources'].items():
        if not r['url'].startswith('https://'): raise SystemExit(rid)
        if set(r['title']) != langs: raise SystemExit(f'{rid} title languages')
    for cid, c in D['careers'].items():
        if not isinstance(c['pay'], int) or c['pay'] < 1000: raise SystemExit(f'{cid} pay')
        if not c['url'].startswith('https://www.bls.gov/ooh/'): raise SystemExit(cid)
    for fid, f in D['facts'].items():
        if not f['url'].startswith('https://'): raise SystemExit(fid)
        if set(f['text']) != langs or set(f['source']) != langs: raise SystemExit(fid)
    for name, rec in list(D['hubs'].items()) + list(D['pages'].items()):
        for i in rec.get('disciplines') or []:
            if i not in D['disciplines']: raise SystemExit(f'{name} discipline {i}')
        for i in rec.get('further') or []:
            if i not in D['resources']: raise SystemExit(f'{name} link {i}')
        for key in ('course_now', 'course_next'):
            if rec.get(key) and rec[key] not in D['courses']: raise SystemExit(f'{name} {key}')
        if rec.get('career') and rec['career'] not in D['careers']: raise SystemExit(f'{name} career')
        if rec.get('why') and rec['why'] not in D['facts']: raise SystemExit(f'{name} why')
def check_block(lang, page, html_block):
    if re.search(r'(?<![A-Za-z])AI(?![A-Za-z])', html_block) or re.search(r'\bpoles\b', html_block, re.I):
        raise SystemExit(f'{page} {lang}: forbidden wording')
    now = D['courses'][merged(page)['course_now']]['page']
    if f'href="{now}"' not in html_block:
        raise SystemExit(f'{page} {lang}: missing the live course link')
    nxt = merged(page).get('course_next')
    if nxt and D['courses'][nxt]['status'] == 'soon':
        field = re.search(r'<div class="study-field"><h3>[^<]*</h3><p>[^<]*<span class="study-soon">.*?</div>', html_block)
        if not field or '<a ' in field.group(0):
            raise SystemExit(f'{page} {lang}: coming-soon course must be text, with no link')
        if D['courses'][nxt].get('page'):
            raise SystemExit(f'{page} {lang}: soon course has a page')
def targets(all_pages):
    if all_pages:
        pages = [p for p in PH if ready(merged(p))]
    else:
        pages = list(D['pilot'])
    return pages
def main():
    check_catalog()
    pages = targets('--all' in sys.argv)
    n = 0; written = []
    for page in pages:
        if not ready(merged(page)): raise SystemExit(f'{page} is not ready to publish')
        for lang in LANGS:
            path = ('' if lang == 'en' else lang + '/') + page
            if not os.path.exists(path): continue
            b = block(lang, page)
            check_block(lang, page, b)
            s = put(rd(path), b)
            if '<!-- TEACHER:START -->' not in rd(path): raise SystemExit(f'{path} has no For Teachers block')
            if b not in s: raise SystemExit(f'{path}: block was not inserted')
            n += wr(path, s); written.append(f'{lang}:{page}')
    css = rd('styles.css'); pat = re.compile(r'/\* STUDY:START \*/.*?/\* STUDY:END \*/', re.S)
    block_css = CSS.strip('\n')
    css2 = pat.sub(lambda m: block_css, css, count=1) if pat.search(css) else css.rstrip('\n') + '\n' + CSS + '\n'
    if css2 != css: open('styles.css', 'w', encoding='utf8').write(css2); n += 1
    print(f'build-study: {n} writes; pages: {", ".join(written)}')
if __name__ == '__main__': main()
