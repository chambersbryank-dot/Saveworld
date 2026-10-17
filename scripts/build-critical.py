#!/usr/bin/env python3
"""Oct 16 (user: fast, quality first): critical CSS per page template, inlined, with the full stylesheets loaded without
blocking render.
Template = the set of linked stylesheets + the page-hero class (e.g. styles/batch-a/batchb/extras + space-hero = solution pages).
For each template, Playwright opens sample pages (an English page and its Arabic version, RTL) at phone 412, iPad 820 and
desktop 1280 widths and keeps every rule (all media queries kept) whose selector matches an element in the first screenfuls,
plus everything for the nav and its dropdowns/mobile menu, the hero (all .page-hero/.space-hero rules, since each page has its
own image), :root/html/body, @font-face and @keyframes. The result is inlined in <head> (marker CRIT) and each
<link rel="stylesheet"> becomes <link rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'"> with a
<noscript> fallback. Document order is unchanged, so the cascade is too. Cache: scripts/critical-cache.json, keyed by template
and a hash of the CSS files, so the weekly run only re-extracts when CSS changes.
Usage: python3 scripts/build-critical.py [--only PAGE.html ...] [--revert]
Run last in weekly-sync.sh (after every generator that touches <head>)."""
import os, re, sys, json, glob, hashlib, threading, http.server, socketserver, functools
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
CACHE = 'scripts/critical-cache.json'
JSCLS = re.compile(r'(mw-|spn|topnav|sp-lb|is-|js-)')  # classes added by JS at runtime: never required to be in the HTML
EXTRACT_V = '6'  # bump when the extraction JS changes (forces re-extract). v2: bare img/svg/video rules always kept (below-fold 1200px card images overflowed in RTL before the full CSS loaded). v3: .sp-video always kept; v4: class-coverage sampling + per-page rule filter (only selectors whose classes appear in the page). v5: mission widget (+ JS-built .mw-*) always kept. v6: .horizon-note/.horizon-badge always kept
SKIP = {'index.html', 'Solutions.html'}  # homepage head is owned by the hero generator (build-batch2 / hero-themes); never rewritten here. Solutions.html: A/B Oct 16 (6 Lighthouse runs each, gzip) showed no FCP gain and +15 KB HTML, so it keeps plain stylesheets
LINK = re.compile(r'<link (?:rel="stylesheet" href="([^"]+\.css[^"]*)"|href="([^"]+\.css[^"]*)" rel="stylesheet")\s*/?>')
BLOCK = re.compile(r'<!-- CRIT:START -->.*?<!-- CRIT:END -->', re.S)
JS = r"""(fold) => {
 const keep = [], DYN = /::?(hover|focus-visible|focus-within|focus|active|visited|target|before|after|placeholder|marker|selection|first-letter|first-line|backdrop|file-selector-button|-webkit-[\w-]+|-moz-[\w-]+)(\([^)]*\))?/g;
 const ALWAYS = /topnav|spn|skip-link|sp-lb|sp-video|mission-widget|mw-|horizon-/, HERO = /page-hero|space-hero|-hero\b/, BARE = /^(img|svg|video|picture|iframe|canvas|html|body|:root|\*|html\.dark|html\.dark body|html\[dir=rtl\]|\[dir=rtl\])$/;
 const nav = document.getElementById('topnav');
 const top = el => { if (nav && nav.contains(el)) return 0; const r = el.getBoundingClientRect(); if (!r.width && !r.height) return 1e9; return r.top + scrollY; };
 const hit = sel => { if (ALWAYS.test(sel) || sel.split(',').some(x => BARE.test(x.trim().replace(DYN, '')))) return true; let s = sel.replace(DYN, '').replace(/\(\s*\)/g, '');
   s = s.split(',').map(x => x.trim() || '*').join(','); let els; try { els = document.querySelectorAll(s); } catch (e) { return true; }
   for (const el of els) { if (top(el) < fold) return true; } return false; };
 const heroes = [], wrap = []; let sheetName = '';
 const walk = (rules) => { const out = [];
   for (const r of rules) {
     if (r.type === 1) { if (HERO.test(r.selectorText)) { if (wrap.length < 2) heroes.push([sheetName, wrap[0] || '', r.selectorText, r.style.cssText]); } else if (hit(r.selectorText)) out.push(r.cssText); }
     else if (r.type === 4 || r.type === 12 || (r.cssRules && r.conditionText !== undefined)) { const w = r.type === 4 ? '@media ' + r.conditionText : r.cssText.split('{')[0].trim(); wrap.push(w); const inner = walk(r.cssRules); wrap.pop(); if (inner.length) out.push(w + '{' + inner.join('') + '}'); }
     else if (r.type === 5 || r.type === 7) out.push(r.cssText);
   } return out; };
 const res = {};
 for (const sh of document.styleSheets) { if (!sh.href) continue; const name = sh.href.split('/').pop().split('?')[0]; sheetName = name; try { res[name] = walk(sh.cssRules); } catch (e) {} }
 res.__hero__ = heroes; return res; }"""

def links(s): return [a or b for a, b in LINK.findall(s)]
def name(h): return h.split('/')[-1].split('?')[0]
def template(s):
    hero = re.search(r'<section class="page-hero((?: [\w-]+)*)"', s)
    return '+'.join(sorted(name(h) for h in links(s))) + '|' + (hero.group(1).split()[0] if hero and hero.group(1).split() else ('page-hero' if hero else '-'))
def css_hash(key):
    h = hashlib.sha256(EXTRACT_V.encode())
    for n in key.split('|')[0].split('+'):
        if os.path.exists(n): h.update(open(n, 'rb').read())
    return h.hexdigest()[:16]

def extract(samples):
    from playwright.sync_api import sync_playwright
    class Q(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=os.getcwd(), **k)
        def log_message(self, *a): pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Q)
    threading.Thread(target=srv.serve_forever, daemon=True).start(); port = srv.server_address[1]
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for key, pages in samples.items():
            merged = {}
            for pg_path in pages:
                for w, h, fold in ((412, 900, 1500), (820, 1180, 1500), (1280, 800, 1100)):
                    pg = b.new_page(viewport={'width': w, 'height': h})
                    pg.route('**/*', lambda r: r.abort() if r.request.resource_type in ('image', 'media', 'font') or not r.request.url.startswith(f'http://127.0.0.1:{port}') else r.continue_())
                    pg.goto(f'http://127.0.0.1:{port}/{pg_path}', wait_until='load'); pg.wait_for_timeout(150)
                    for sheet, rules in pg.evaluate(JS, fold).items():
                        if sheet == '__hero__': rules = [list(x) for x in rules]
                        lst = merged.setdefault(sheet, [])
                        for r in rules:
                            if r not in lst: lst.append(r)
                    pg.close()
            out[key] = merged
        b.close()
    srv.shutdown()
    return out

def page_classes(s):
    return set(c for m in re.findall(r'class="([^"]*)"', s) for c in m.split()) | {'dark'}

def hero_css(merged, sheet, have):
    out, cur, buf = [], None, []
    def flush():
        if buf: out.append((cur + '{' + ''.join(buf) + '}') if cur else ''.join(buf))
    for sh, w, sel, decl in merged.get('__hero__', []):
        if sh != sheet: continue
        keep = [x.strip() for x in sel.split(',') if set(re.findall(r'\.([\w-]+)', x)) <= have]
        if not keep: continue
        if w != cur: flush(); buf = []; cur = w
        buf.append(','.join(keep) + '{' + decl + '}')
    flush()
    return ''.join(out)

def split_rules(css):
    out, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: out.append(css[start:i + 1]); start = i + 1
        elif ch == ';' and depth == 0: out.append(css[start:i + 1]); start = i + 1
    return [r.strip() for r in out if r.strip()]

def keep_rule(r, have):
    head = r.split('{', 1)[0].strip()
    if head.startswith('@media') or head.startswith('@supports') or head.startswith('@container') or head.startswith('@layer'):
        inner = [x for x in split_rules(r[r.index('{') + 1:r.rindex('}')]) if keep_rule(x, have)]
        return (head + '{' + ''.join(inner) + '}') if inner else None
    if head.startswith('@') or not have: return r
    sels = [x for x in head.split(',') if set(c for c in re.findall(r'\.([\w-]+)', re.sub(r':not\([^)]*\)', '', x)) if not JSCLS.match(c)) <= have]
    return (','.join(sels) + r[len(r.split('{', 1)[0]):]) if sels else None

def build_css(merged, order, have=frozenset()):
    parts = []
    for sheet in order:
        rules = [k for k in (keep_rule(r, have) for r in merged.get(sheet, [])) if k]
        parts.append(''.join(rules) + hero_css(merged, sheet, have))
    css = ''.join(parts)
    css = re.sub(r'\s*([{};:,>])\s*', r'\1', css).replace(';}', '}')
    return css

def apply(f, s, css):
    s = BLOCK.sub('', s)
    s = re.sub(r'<noscript class="crit-ns">.*?</noscript>', '', s, flags=re.S)
    s = re.sub(r'<link rel="preload" as="style" href="([^"]+)" onload="this.onload=null;this.rel=\'stylesheet\'">', r'<link rel="stylesheet" href="\1">', s)
    if css is None: return s
    hrefs = links(s)
    if not hrefs: return s
    first = LINK.search(s)
    s = s[:first.start()] + '<!-- CRIT:START --><style id="crit">' + css.replace('</', '<\\/') + '</style><!-- CRIT:END -->' + s[first.start():]
    def swap(m):
        h = m.group(1) or m.group(2)
        return f'<link rel="preload" as="style" href="{h}" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript class="crit-ns"><link rel="stylesheet" href="{h}"></noscript>'
    return LINK.sub(swap, s)

def main():
    args = sys.argv[1:]; revert = '--revert' in args
    only = set(a for a in args if a.endswith('.html'))
    files = sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html'))
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    groups = {}
    for f in files:
        en = f.split('/', 1)[1] if '/' in f else f
        if only and en not in only: continue
        if en in SKIP: continue
        s = BLOCK.sub('', open(f, encoding='utf8').read())
        if 'http-equiv="refresh"' in s or not links(s): continue
        k = template(apply(f, s, None)); groups.setdefault(k, []).append(f)
    need = {}
    for k, fs in groups.items():
        if revert: continue
        if cache.get(k, {}).get('hash') == css_hash(k): continue
        allen = [f for f in fs if '/' not in f] or fs[:1]
        # greedy: English samples (cap 40) until every class used on the template's pages is covered, so page-specific blocks near the fold (mission widgets, videos) are seen; build_css then keeps only rules whose classes the page actually uses that together cover the most distinct classes (page-specific blocks near the fold)
        cls = {f: page_classes(open(f, encoding='utf8').read()) for f in allen}; ens, seen = [], set()
        while allen and len(ens) < 40:
            best = max((f for f in allen if f not in ens), key=lambda f: len(cls[f] - seen), default=None)
            if best is None or (ens and not cls[best] - seen): break
            ens.append(best); seen |= cls[best]
        smp = list(ens)
        if os.path.exists('ar/' + ens[0]): smp.append('ar/' + ens[0])
        need[k] = smp
    if need:
        for k, merged in extract(need).items():
            order = [n for n in k.split('|')[0].split('+')]
            cache[k] = {'hash': css_hash(k), 'samples': need[k], 'merged': merged}
        json.dump(cache, open(CACHE, 'w'), ensure_ascii=False, separators=(',', ':'))
    n = 0; sizes = {}
    for k, fs in groups.items():
        for f in fs:
            s = open(f, encoding='utf8').read()
            order = [name(h) for h in links(apply(f, s, None))]
            css = None if revert else build_css(cache[k]['merged'], order, page_classes(s))
            if css is not None and '/' in f: css = re.sub(r"url\((['\"]?)(?!data:|https?:|/)", r"url(\1../", css)
            s2 = apply(f, s, css)
            if css: sizes[k] = len(css)
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print('build-critical:', n, 'pages,', len(groups), 'templates,', 'max inline', max(sizes.values()) if sizes else 0, 'bytes')
    for k, v in sorted(sizes.items(), key=lambda x: -x[1])[:6]: print('  ', v, k)

if __name__ == '__main__': main()
