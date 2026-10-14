#!/usr/bin/env python3
"""Batch A (Oct 12): share bar, "Last reviewed" + source count, Related Solutions, "What makes us different" strip.
English pages only; i18n-build.py regenerates /fr/ /es/ /ar/ (this script also writes the dynamic i18n keys it needs).
All blocks live between <!-- NAME:START --> / <!-- NAME:END --> markers, so re-running is idempotent.
Related Solutions = cosine similarity of page vectors (mean of each page's bge-small-en-v1.5 chunk vectors + its title/description chunk) from the
committed search/semantic-index.json + semantic-vectors.bin (built by build-search.mjs, which strips these blocks).
Last reviewed = date of the last change to the page's substantive text (hero, Five W's, impact, mission status),
kept in assets/data/reviewed.json (bootstrapped from git history; later changes stamped with the run date, HST).
Run from repo root (weekly-sync.sh runs it before i18n-build): python3 scripts/build-batch-a.py"""
import re, os, json, html, hashlib, datetime, subprocess, importlib.util, struct
SITE = 'https://www.savingplanets.com/'
CSSV, JSV = '20261012a', '20261012a'
rd = lambda f: open(f, encoding='utf8').read()
spec = importlib.util.spec_from_file_location('sol', 'scripts/build-solutions-index.py'); sol = importlib.util.module_from_spec(spec); spec.loader.exec_module(sol)

HL = sol.hubs()
NAME, HUB = {}, {}
for f, hub, items in HL:
    for h, n in items:
        if h not in NAME: NAME[h] = n; HUB[h] = hub
SOLS = sorted(NAME)
HUBPAGES = [f for f, _ in sol.HUBS if os.path.exists(f)]
SHARE_PAGES = SOLS + HUBPAGES + ['Amazing_Facts.html', 'Myth_vs_Fact.html']

def put(s, name, inner, anchor_re, before=False):
    b = f'<!-- {name}:START -->{inner}<!-- {name}:END -->'
    pat = re.compile(rf'<!-- {name}:START -->.*?<!-- {name}:END -->\n?', re.S)
    if pat.search(s): return pat.sub(lambda m: b + '\n', s, count=1)
    m = re.search(anchor_re, s, re.S)
    if not m: raise SystemExit(f'anchor not found for {name}: {anchor_re}')
    i = m.start() if before else m.end()
    return s[:i] + ('' if before else '\n') + b + ('\n' if before else '') + s[i:]

def assets(s):
    if 'batch-a.css' not in s: s = s.replace('</head>', f'<link rel="stylesheet" href="batch-a.css?v={CSSV}">\n</head>', 1)
    if 'share.js' not in s and '<!-- SHARE:START -->' in s: s = s.replace('</body>', f'<script src="share.js?v={JSV}" defer></script>\n</body>', 1)
    return s

# ---------- 1) share bar ----------
def share_bar(page, s):
    url = SITE + page
    title = html.unescape(sol.m1(r'<title>([^<]*)</title>', s))
    q = lambda x: __import__('urllib.parse').parse.quote(x, safe='')
    return ('<section class="share-bar" aria-label="Share this page" data-pagefind-ignore><p class="share-title">Share this page</p><div class="share-btns">'
        '<button type="button" class="share-btn share-native" hidden>Share</button>'
        f'<a class="share-btn share-x" href="https://twitter.com/intent/tweet?url={q(url)}&amp;text={q(title)}" target="_blank" rel="noopener" aria-label="Share on X">X</a>'
        f'<a class="share-btn share-fb" href="https://www.facebook.com/sharer/sharer.php?u={q(url)}" target="_blank" rel="noopener" aria-label="Share on Facebook">Facebook</a>'
        f'<a class="share-btn share-li" href="https://www.linkedin.com/sharing/share-offsite/?url={q(url)}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">LinkedIn</a>'
        f'<a class="share-btn share-mail" href="mailto:?subject={q(title)}&amp;body={q(url)}" aria-label="Share by email">Email</a>'
        '<button type="button" class="share-btn share-copy">Copy link</button><span class="share-ok" role="status" hidden>Link copied</span></div></section>')

# ---------- 2) last reviewed + sources ----------
def substance(s):
    parts = re.findall(r'<section class="(?:page-hero[^"]*|five-ws|impact|mission-widget)"[^>]*>.*?</section>', s, re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(parts)))).strip()

def sig(s): return hashlib.sha1(substance(s).encode('utf8')).hexdigest()[:12]

def git_date(page, cur):
    """Most recent commit date at which the page's substantive text changed (walk history newest -> oldest)."""
    try: log = subprocess.run(['git', 'log', '--format=%H %cs', '--', page], capture_output=True, text=True, check=True).stdout.split('\n')
    except Exception: return None
    log = [l.split() for l in log if l.strip()]
    if not log: return None
    prev_date = log[0][1]
    for h, d in log:
        try: old = subprocess.run(['git', 'show', f'{h}:{page}'], capture_output=True, text=True, check=True).stdout
        except Exception: break
        if sig(old) != cur: return prev_date
        prev_date = d
    return prev_date  # unchanged since first commit

def sources(s):
    b = s.split('<body', 1)[-1]
    b = re.sub(r'<nav id="topnav">.*?</nav>|<footer>.*?</footer>|<section class="help-actions".*?</section>|<!-- (SHARE|RELATED|REVIEWED):START -->.*?<!-- \1:END -->', ' ', b, flags=re.S)
    urls = set(re.findall(r'href="(https?://[^"]+)"', b)) | set(re.findall(r'data-source="(https?://[^"]+)"', b))
    urls = {u.split('#')[0].rstrip('/') for u in urls if not re.search(r'twitter\.com/intent|facebook\.com/sharer|linkedin\.com/sharing|donate', u)}
    return len(urls)

MONTHS = {'en': 'January February March April May June July August September October November December'.split(),
          'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
          'es': 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split(),
          'ar': 'يناير فبراير مارس أبريل مايو يونيو يوليو أغسطس سبتمبر أكتوبر نوفمبر ديسمبر'.split()}
SRC_T = {'fr': ('{n} sources citées', '1 source citée'), 'es': ('{n} fuentes citadas', '1 fuente citada'), 'ar': ('{n} مصادر مذكورة', 'مصدر واحد مذكور')}

# ---------- 3) related ----------
def related():
    idx = json.load(open('search/semantic-index.json')); dim = idx['dim']
    raw = open('search/semantic-vectors.bin', 'rb').read()
    import array
    v = array.array('b'); v.frombytes(raw)
    n = len(idx['chunkPage']); acc, first = {}, {}
    for c in range(n):  # page vector = normalized mean of all chunks + normalized title/description chunk
        p = idx['chunkPage'][c]; a = acc.setdefault(p, [0.0] * dim); base = c * dim
        if p not in first: first[p] = [float(v[base + d]) for d in range(dim)]
        for d in range(dim): a[d] += v[base + d]
    nz = lambda a: (lambda n: [x / n for x in a])(sum(x * x for x in a) ** .5 or 1)
    for p in acc: acc[p] = [x + y for x, y in zip(nz(acc[p]), nz(first[p]))]
    url2p = {pg['url'].lstrip('/'): i for i, pg in enumerate(idx['pages'])}
    vec = {}
    for f in SOLS:
        if f in url2p and url2p[f] in acc:
            a = acc[url2p[f]]; norm = sum(x * x for x in a) ** .5 or 1; vec[f] = [x / norm for x in a]
    out = {}
    for f in vec:
        sc = sorted(((sum(x * y for x, y in zip(vec[f], vec[g])), g) for g in vec if g != f), reverse=True)
        out[f] = [g for _, g in sc[:4]]
    return out

# Manual overrides (assets/data/related-overrides.json: {"Page.html": ["A.html", ...]}) win over the similarity picks,
# so hand-chosen cards survive the weekly sync. Targets may be solution pages or hub pages.
OVR_F = 'assets/data/related-overrides.json'
HUBNAME = dict(sol.HUBS)
def apply_overrides(rel):
    if not os.path.exists(OVR_F): return rel
    for page, picks in json.load(open(OVR_F)).items():
        if page.startswith('_'): continue
        picks = [g for g in picks if os.path.exists(g) and g != page][:4]
        if picks: rel[page] = picks
    return rel

def related_block(page, rel):
    cards = []
    for g in rel:
        i = sol.info(g)  # decorative: the card's visible name is the link text
        img = f'<img src="{i["img"]}" alt="" loading="lazy" decoding="async">' if i['img'] else ''
        hub, name = (HUB[g], NAME[g]) if g in NAME else ('Hub', HUBNAME.get(g, g[:-5].replace('_', ' ')))
        cards.append(f'<li class="rel-card"><a href="{g}">{img}<span class="rel-hub">{sol.esc(hub)}</span><span class="rel-name">{sol.esc(name)}</span></a></li>')
    return ('<section class="related-solutions" aria-labelledby="rel-title" data-pagefind-ignore><h2 id="rel-title">Related Solutions</h2>'
            '<p class="rel-intro">More solutions like this one, matched by meaning.</p><ul class="rel-grid">' + ''.join(cards) + '</ul></section>')

# ---------- 4) difference strip ----------
DIFF_LEAD = 'From the ocean floor to low Earth orbit, solutions minus the doom.'
DIFF_BODY = '{n} real, sourced solutions across {h} hubs, explained the same simple way (Who, What, When, Where, Why), in English, French, Spanish and Arabic. Search by meaning, privately in your browser, powered by trusted MIT open-source tools.'
DIFF_T = {'fr': ("Du fond de l'océan à l'orbite terrestre basse, des solutions sans le catastrophisme.",
                 "{n} solutions réelles et sourcées réparties en {h} pôles, expliquées de la même façon simple (Qui, Quoi, Quand, Où, Pourquoi), en anglais, français, espagnol et arabe. Recherchez par le sens, en toute confidentialité dans votre navigateur, grâce à des outils open source MIT de confiance."),
          'es': ('Desde el fondo del océano hasta la órbita terrestre baja, soluciones sin catastrofismo.',
                 '{n} soluciones reales y con fuentes en {h} áreas, explicadas de la misma forma sencilla (Quién, Qué, Cuándo, Dónde, Por qué), en inglés, francés, español y árabe. Busca por significado, de forma privada en tu navegador, con herramientas de código abierto MIT de confianza.'),
          'ar': ('من قاع المحيط إلى المدار الأرضي المنخفض، حلول بلا تهويل.',
                 '{n} حلاً حقيقياً وموثّق المصادر في {h} محاور، مشروحة بالطريقة البسيطة نفسها (من، ماذا، متى، أين، لماذا)، بالإنجليزية والفرنسية والإسبانية والعربية. ابحث بالمعنى، بخصوصية داخل متصفحك، بأدوات مفتوحة المصدر موثوقة بترخيص MIT.')}
UI = {'fr': {'Share this page': 'Partager cette page', 'Share': 'Partager', 'Share on X': 'Partager sur X', 'Share on Facebook': 'Partager sur Facebook',
             'Share on LinkedIn': 'Partager sur LinkedIn', 'Share by email': 'Partager par e-mail', 'Email': 'E-mail', 'Copy link': 'Copier le lien',
             'Link copied': 'Lien copié', 'Last reviewed:': 'Dernière révision :', 'Related Solutions': 'Solutions similaires',
             'More solutions like this one, matched by meaning.': 'D’autres solutions proches de celle-ci, associées par le sens.',
             'What makes us different': 'Ce qui nous distingue', 'Page review and sources': 'Révision et sources de la page'},
      'es': {'Share this page': 'Comparte esta página', 'Share': 'Compartir', 'Share on X': 'Compartir en X', 'Share on Facebook': 'Compartir en Facebook',
             'Share on LinkedIn': 'Compartir en LinkedIn', 'Share by email': 'Compartir por correo', 'Email': 'Correo', 'Copy link': 'Copiar enlace',
             'Link copied': 'Enlace copiado', 'Last reviewed:': 'Última revisión:', 'Related Solutions': 'Soluciones relacionadas',
             'More solutions like this one, matched by meaning.': 'Más soluciones como esta, relacionadas por significado.',
             'What makes us different': 'Lo que nos hace diferentes', 'Page review and sources': 'Revisión y fuentes de la página'},
      'ar': {'Share this page': 'شارك هذه الصفحة', 'Share': 'مشاركة', 'Share on X': 'شارك على X', 'Share on Facebook': 'شارك على فيسبوك',
             'Share on LinkedIn': 'شارك على لينكدإن', 'Share by email': 'شارك عبر البريد الإلكتروني', 'Email': 'البريد', 'Copy link': 'نسخ الرابط',
             'Link copied': 'تم نسخ الرابط', 'Last reviewed:': 'آخر مراجعة:', 'Related Solutions': 'حلول ذات صلة',
             'More solutions like this one, matched by meaning.': 'حلول أخرى مشابهة لهذا الحل، مطابقة حسب المعنى.',
             'What makes us different': 'ما يميزنا', 'Page review and sources': 'مراجعة الصفحة ومصادرها'}}

def main():
    keys = {l: dict(UI[l]) for l in UI}
    today = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=10)).date().isoformat()
    store_f = 'assets/data/reviewed.json'
    store = json.load(open(store_f)) if os.path.exists(store_f) else {}
    try: rel = related()
    except FileNotFoundError: rel = {}
    rel = apply_overrides(rel)
    stats = dict(share=0, reviewed=0, related=0)
    for page in SHARE_PAGES:
        s = rd(page); o = s
        if page in NAME:
            sg = sig(s); e = store.get(page)
            if not e or e['sig'] != sg:
                e = {'sig': sg, 'date': (git_date(page, sg) if not e else None) or today}; store[page] = e
            y, mth = int(e['date'][:4]), int(e['date'][5:7])
            mtxt = f'{MONTHS["en"][mth-1]} {y}'; n = sources(s)
            stxt = '1 source cited' if n == 1 else f'{n} sources cited'
            for l in UI:
                keys[l][mtxt] = f'{MONTHS[l][mth-1]} {y}'
                keys[l][stxt] = SRC_T[l][1] if n == 1 else SRC_T[l][0].replace('{n}', str(n))
            rv = (f'<p class="page-reviewed" aria-label="Page review and sources" data-pagefind-ignore><span class="rv-label">Last reviewed:</span> '
                  f'<time datetime="{e["date"][:7]}">{mtxt}</time><span aria-hidden="true"> · </span><a href="#solution">{stxt}</a></p>')
            s = put(s, 'REVIEWED', rv, r'<nav aria-label="Breadcrumb" class="breadcrumb">.*?</nav>'); stats['reviewed'] += 1
            if rel.get(page):
                anchor = r'<section class="next-solutions"' if '<section class="next-solutions"' in s else r'<section class="help-actions"' if '<section class="help-actions"' in s else r'<footer>'
                s = put(s, 'RELATED', related_block(page, rel[page]), anchor, before=True); stats['related'] += 1
        s = put(s, 'SHARE', share_bar(page, s), r'<footer>', before=True); stats['share'] += 1
        s = assets(s)
        if s != o: open(page, 'w', encoding='utf8').write(s)
    # difference strip
    total, nh = len(NAME), len(HL)
    body = DIFF_BODY.replace('{n}', str(total)).replace('{h}', str(nh))
    for l in DIFF_T:
        keys[l][DIFF_LEAD] = DIFF_T[l][0]; keys[l][body] = DIFF_T[l][1].replace('{n}', str(total)).replace('{h}', str(nh))
    strip = (f'<section class="diff-strip" aria-label="What makes us different"><p class="diff-lead">{DIFF_LEAD}</p><p class="diff-body">{html.escape(body, quote=False)}</p></section>')
    for page, anchor in (('index.html', r'<section class="hero [^"]*">.*?</section>'), ('About.html', r'<section class="page-hero[^"]*">.*?</section>(\s*<p class="photo-credit">[^<]*</p>)?(\s*<nav aria-label="Breadcrumb".*?</nav>)?')):
        s = rd(page); o = s
        s = put(s, 'DIFF', strip, anchor); s = assets(s)
        if s != o: open(page, 'w', encoding='utf8').write(s)
    # OG image for 404 + Project-R
    og = sol.m1(r'<meta property="og:image" content="([^"]+)"', rd('index.html'))
    for page in ('404.html', 'Project-R.html'):
        s = rd(page)
        if 'og:image' not in s and og:
            t = sol.m1(r'<title>([^<]*)</title>', s)
            s = s.replace('</title>', f'</title>\n<meta property="og:title" content="{t}">\n<meta property="og:image" content="{og}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{og}">', 1)
            open(page, 'w', encoding='utf8').write(s)
    json.dump(dict(sorted(store.items())), open(store_f, 'w'), indent=1)
    for l in keys:  # add/refresh only our keys; leave everything else in the file untouched
        f = f'i18n/{l}.json'; m = json.load(open(f, encoding='utf8')); ch = False
        for k, v in keys[l].items():
            if m.get(k) != v: m[k] = v; ch = True
        if ch: json.dump(m, open(f, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(f"batch-a: share {stats['share']}, reviewed {stats['reviewed']}, related {stats['related']}, solutions {total} in {nh} hubs")

if __name__ == '__main__': main()
