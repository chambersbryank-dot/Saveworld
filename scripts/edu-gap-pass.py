#!/usr/bin/env python3
"""November 18, 2026 pass for the education-comparison gaps that live in generated HTML:
neutral source line, honest footer note, non-blocking stylesheets, Classroom script,
hero-image fallback, and a production-only analytics beacon.
Does not edit Before Saving Planets pages. Run from the repo root after the course and
teacher generators."""
import glob, os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
KIDS = {'Kids.html', 'Play_and_Learn.html', 'Kids_Map.html', 'Kids_World.html', 'Amazing_Facts.html', 'Space_Passport.html', 'Boarding_Pass.html', 'Myth_or_Fact_Arcade.html'}
PHRASES = [
    ('Page verified October 2026', 'Sources are listed on the page'),
    ('Page vérifiée en octobre 2026', 'Les sources sont indiquées sur la page'),
    ('Página verificada en octubre de 2026', 'Las fuentes están indicadas en la página'),
    ('تم التحقق من الصفحة في أكتوبر 2026', 'المصادر مذكورة في الصفحة'),
    ('Pagina verificata a ottobre 2026', 'Le fonti sono indicate nella pagina'),
    ('Pagina verificata ottobre 2026', 'Le fonti sono indicate nella pagina'),
    ('הדף אומת באוקטובר 2026', 'המקורות מצוינים בעמוד'),
]
OLD_TRUST = 'Why trust it: every page is cross-checked against NASA, Yale, Harvard, MIT, and other leading universities and scholars.'
HERO_CRIT = (
    '<style id="lcp-crit">body{margin:0;background:#071018;color:#e8eef5;font-family:Montserrat,"Segoe UI",sans-serif}'
    '.hero{position:relative;height:100vh;min-height:640px;display:flex;align-items:flex-start;justify-content:center;background:#071018}'
    '.hero-content{width:min(46rem,92vw);margin:0 auto;text-align:center;padding:calc(22vh + 3.4rem) 1.25rem 2rem}'
    '.hero-welcome{font-size:clamp(2.4rem,5vw,4.4rem);line-height:1.05;margin:0 0 1rem;color:#fff;text-align:center}'
    '.page-hero{min-height:320px;background:#071018;color:#fff}'
    '.page-hero h1{color:#fff;font-size:clamp(2rem,5vw,3.2rem);margin:0}</style>'
)
BEACON = re.compile(r'<script defer src="https://static\.cloudflareinsights\.com/beacon\.min\.js" data-cf-beacon=\'(\{[^\']*\})\'></script>')
BEACON_JS = (
    '<script>(function(){var h=location.hostname;if(!/(^|\\.)savingplanets\\.com$/.test(h))return;'
    'if(/\\/(Kids|Play_and_Learn|Kids_Map|Kids_World|Amazing_Facts|Space_Passport|Boarding_Pass|Myth_or_Fact_Arcade)\\.html$/.test(location.pathname))return;'
    'var s=document.createElement("script");s.defer=true;s.src="https://static.cloudflareinsights.com/beacon.min.js";'
    's.setAttribute("data-cf-beacon",%r);document.body.appendChild(s)})();</script>'
)

def pages():
    out = []
    for p in glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html'):
        if 'Before' in p or os.path.basename(p).startswith('Before'): continue
        out.append(p)
    return out

def defer_css(head):
    """Turn render-blocking stylesheet links that sit outside noscript into the preload pattern."""
    parts = re.split(r'(<noscript\b.*?</noscript>)', head, flags=re.S)
    for i, part in enumerate(parts):
        if part.startswith('<noscript'): continue
        def repl(m):
            tag, href = m.group(0), m.group(1)
            if 'media=' in tag or 'onload=' in tag: return tag
            if f'rel="preload" as="style" href="{href}"' in head: return ''
            return (f'<link rel="preload" as="style" href="{href}" onload="this.onload=null;this.rel=\'stylesheet\'">'
                    f'<noscript class="crit-ns"><link rel="stylesheet" href="{href}"></noscript>')
        parts[i] = re.sub(r'<link rel="stylesheet" href="([^"]+\.css[^"]*)">', repl, part)
    return ''.join(parts)

def shrink_picture(html):
    def repl(m):
        pic = m.group(0)
        sized = re.findall(r'https://[^"\s]+-1280\.[A-Za-z0-9]+\.webp', pic) or re.findall(r'https://[^"\s]+-800\.[A-Za-z0-9]+\.webp', pic)
        if not sized: return pic
        return re.sub(r'(<img\b[^>]*?\bsrc=")[^"]+"', lambda mm: mm.group(1) + sized[0] + '"', pic, count=1)
    return re.sub(r'<picture class="spb-media">.*?</picture>', repl, html, count=1, flags=re.S)

def preload_hero(html):
    if 'rel="preload" as="image"' in html: return html
    m = re.search(r'(https://media\.savingplanets\.com/images/[^"\s]+-800\.[A-Za-z0-9]+\.avif)', html)
    if not m: return html
    link = f'<link rel="preload" as="image" href="{m.group(1)}" fetchpriority="high">'
    return html.replace('</head>', link + '</head>', 1)

def add_classroom(html, path):
    base = os.path.basename(path)
    if base in KIDS: return html
    if 'assets/classroom.js' in html or '../assets/classroom.js' in html: return html
    want = ('class="gc-slot"' in html or 'class="teacher-box"' in html or base in ('Lesson_Builder.html', 'Myth_vs_Fact.html', 'Teachers.html', 'Lesson_Plan.html'))
    if not want: return html
    pre = '' if '/' not in path.replace('\\', '/') or path.startswith('./') and path.count('/') == 0 else ('../' if os.path.dirname(path) else '')
    # dirname of "fr/x.html" is fr
    pre = '../' if os.path.dirname(path) else ''
    tag = f'<link rel="stylesheet" href="{pre}assets/classroom.css"><script src="{pre}assets/classroom.js" defer></script>'
    if base == 'Lesson_Builder.html':
        html = html.replace(f'<script src="{pre}edu.js', tag + f'<script src="{pre}edu.js', 1)
        if 'classroom.js' in html: return html
    return html.replace('</body>', tag + '</body>', 1)

def one(path):
    s = open(path, encoding='utf8').read()
    n = s
    for a, b in PHRASES:
        n = n.replace(a, b)
    if '</head>' in n:
        head, rest = n.split('</head>', 1)
        head2 = defer_css(head)
        if 'id="lcp-crit"' not in head2 and 'id="crit"' not in head2 and ('class="hero"' in n or 'class="page-hero"' in n):
            head2 = head2.replace('</head>', HERO_CRIT) if False else head2 + HERO_CRIT
        n = head2 + '</head>' + rest
    if 'has-video' in n and 'id="crit"' in n and '.has-video .hero-media{position:absolute' not in n:
        n = n.replace('</style><!-- CRIT:END -->', '.page-hero.has-video{height:52vh;min-height:320px;max-height:560px}.page-hero.has-video .hero-media,.page-hero.has-video .hero-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}</style><!-- CRIT:END -->', 1)
    n = shrink_picture(n)
    n = preload_hero(n)
    def beacon(m):
        return BEACON_JS % (m.group(1),)
    n = BEACON.sub(beacon, n, count=1)
    n = add_classroom(n, path)
    if n != s:
        open(path, 'w', encoding='utf8').write(n)
        return 1
    return 0

def json_phrases():
    n = 0
    for p in glob.glob('i18n/*.json') + glob.glob('i18n/**/*.json', recursive=True):
        raw = open(p, encoding='utf8').read()
        nxt = raw
        for a, b in PHRASES:
            nxt = nxt.replace(a, b)
        if nxt != raw:
            open(p, 'w', encoding='utf8').write(nxt)
            n += 1
    return n

def main():
    c = sum(one(p) for p in pages())
    print('html', c, 'json', json_phrases())

if __name__ == '__main__':
    main()
