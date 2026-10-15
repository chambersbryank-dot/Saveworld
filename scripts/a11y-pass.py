#!/usr/bin/env python3
"""Accessibility pass (Oct 14, 2026). Idempotent. Data: assets/data/a11y.json.
  python3 scripts/a11y-pass.py            English pages, run BEFORE i18n-build:
      - generic '<Name> image' alts -> '<Name>: <specific description of that picture>'
      - wrong alts fixed (alt_fix), translation memory (i18n/<lang>.json) filled for every new alt
      - every <video>: <track kind="captions"> (assets/captions/<video>.<lang>.vtt) + Transcript <details> below its figure
      - writes the WebVTT files for en/fr/es/ar
  python3 scripts/a11y-pass.py --translated   fr/es/ar pages, run AFTER i18n-build: point tracks at the page language,
      and re-apply alt fixes if translation memory was missing."""
import json, re, os, sys, glob, html, collections
D = json.load(open('assets/data/a11y.json', encoding='utf8'))
# Oct 15: solution counts in video captions/transcripts follow the live count (assets/data/solutions.json, written by build-stats.js)
try: _N = json.load(open('assets/data/solutions.json', encoding='utf8'))['site']['solutions']
except Exception: _N = None
if _N:
    _NUM = re.compile(r'\b\d{2,4}(?=\s*(?:real solutions|solutions réelles|soluciones reales|soluzioni reali|حلاً))')
    for _v in D['videos'].values():
        for _cue in _v['cues']:
            for _l in _cue[2]: _cue[2][_l] = _NUM.sub(str(_N), _cue[2][_l])
    # live-count variants in translation memory, so translated captions/figcaptions never fall back to a stale count
    if '--translated' not in sys.argv:
        for _lg in ['fr', 'es', 'ar', 'it']:
            _f = f'i18n/{_lg}.json'
            if not os.path.exists(_f): continue
            _m = json.load(open(_f, encoding='utf8')); _ch = 0
            for _k in list(_m):
                if re.search(r'\b\d{2,4} real solutions', _k):
                    _nk = _NUM.sub(str(_N), _k)
                    if _nk != _k and _nk not in _m: _m[_nk] = _NUM.sub(str(_N), _m[_k]); _ch = 1
            if _ch: json.dump(_m, open(_f, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
LANGS = ['fr', 'es', 'ar', 'it']
LABEL = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية', 'it': 'Italiano'}
UI = {'All facts': {'fr': 'Tous les faits', 'es': 'Todos los datos', 'ar': 'كل الحقائق', 'it': 'Tutti i fatti'}, 'Transcript': {'fr': 'Transcription', 'es': 'Transcripción', 'ar': 'النص المكتوب', 'it': 'Trascrizione'},
      'What you see:': {'fr': 'Ce que vous voyez :', 'es': 'Lo que se ve:', 'ar': 'ما تراه:', 'it': 'Cosa vedi:'},
      'What you hear:': {'fr': 'Ce que vous entendez :', 'es': 'Lo que se oye:', 'ar': 'ما تسمعه:', 'it': 'Cosa senti:'}}
WEAK = re.compile(r'^(.+?) image$')
SKIP = re.compile(r'^(Learn more|Donate|Support|$)')
rd = lambda f: open(f, encoding='utf8').read()
def wr(f, s):
    if rd(f) != s: open(f, 'w', encoding='utf8').write(s); return 1
    return 0
def key(src): return re.sub(r'^(\.\./)+', '', src.split('?')[0])
def esc(s): return html.escape(s, quote=True)

def best_desc(pages):
    c = collections.defaultdict(collections.Counter)
    for f in pages:
        for t in re.findall(r'<img\b[^>]*>', rd(f)):
            s = re.search(r'src="([^"]+)"', t); a = re.search(r'alt="([^"]*)"', t)
            if s and a:
                v = html.unescape(a.group(1))
                if not SKIP.match(v) and not WEAK.match(v) and len(v) > 25: c[key(s.group(1))][v] += 1
    out = {k: max(v, key=lambda x: (v[x], len(x))) for k, v in c.items()}
    for k, v in D['alt_desc'].items(): out[k] = v['en']
    return out

def vtt(cues, l):
    t = lambda x: f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}'
    return 'WEBVTT\n\n' + ''.join(f'{i+1}\n{t(a)} --> {t(b)}\n{c[l]}\n\n' for i, (a, b, c) in enumerate(cues))

def transcript(v, l):
    x = D['videos'][v]; T = lambda s: s if l == 'en' else UI[s][l]
    return (f'<!-- TRANSCRIPT:START --><details class="video-transcript"><summary>{T("Transcript")}</summary>'
            f'<p><strong>{T("What you see:")}</strong> {esc(x["visual"][l])}</p><p><strong>{T("What you hear:")}</strong></p>'
            + ''.join(f'<p>{esc(c[l])}</p>' for _, _, c in x['cues']) + '</details><!-- TRANSCRIPT:END -->')

def videos(s, l, prefix):
    def tr(m):
        blk = m.group(0); v = re.search(r'assets/videos/([\w-]+)\.mp4', blk)
        if not v or v.group(1) not in D['videos']: return blk
        v = v.group(1); blk = re.sub(r'<track kind="captions"[^>]*>', '', blk)
        if 'hero-video' in blk: return blk  # silent decorative loop: no visible captions
        tag = f'<track kind="captions" src="{prefix}assets/captions/{v}.{l}.vtt" srclang="{l}" label="{LABEL[l]}" default>'
        return blk.replace('</video>', tag + '</video>')
    s = re.sub(r'<video\b.*?</video>', tr, s, flags=re.S)
    s = re.sub(r'<!-- TRANSCRIPT:START -->.*?<!-- TRANSCRIPT:END -->', '', s, flags=re.S)
    def add(m):
        v = re.search(r'assets/videos/([\w-]+)\.mp4', m.group(0))
        if not v or 'hero-video' in m.group(0) or v.group(1) not in D['videos']: return m.group(0)
        return m.group(0) + transcript(v.group(1), l)
    return re.sub(r'<figure class="sp-video-fig">.*?</figure>', add, s, flags=re.S)

def alts(s, desc, l, mem):
    n = 0
    def fix(m):
        nonlocal n
        t = m.group(0); s_ = re.search(r'src="([^"]+)"', t); a = re.search(r'alt="([^"]*)"', t)
        if not s_ or not a: return t
        k = key(s_.group(1)); old = html.unescape(a.group(1)); new = None
        fx = D['alt_fix'].get(f'{k}|{old}')
        if fx: new = fx[l]
        elif l == 'en':
            w = WEAK.match(old)
            if w and k in desc: new = f'{w.group(1)}: {desc[k]}'
        if new is None or new == old: return t
        n += 1; return t.replace(a.group(0), f'alt="{esc(new)}"')
    return re.sub(r'<img\b[^>]*>', fix, s), n

def main():
    en = [f for f in sorted(glob.glob('*.html')) if not f.startswith('google')]
    if '--translated' in sys.argv:
        n = 0
        for l in LANGS:
            for f in glob.glob(f'{l}/*.html'):
                s = rd(f); s, _ = alts(s, {}, l, None)
                s = re.sub(r'<track\b[^>]*kind="captions"[^>]*>', lambda m: m.group(0).replace('.en.vtt', f'.{l}.vtt').replace('srclang="en"', f'srclang="{l}"').replace('label="English"', f'label="{LABEL[l]}"'), s)
                n += wr(f, s)
        print(f'a11y-pass --translated: {n} pages updated'); return
    desc = best_desc(en)
    mems = {l: json.load(open(f'i18n/{l}.json', encoding='utf8')) for l in LANGS}
    tot = 0; newalts = set()
    for f in en:
        s0 = rd(f); s, k = alts(s0, desc, 'en', None); tot += k
        s = videos(s, 'en', '')
        if f == 'Amazing_Facts.html' and 'id="facts-h"' not in s:   # heading order: h1 -> fact h3s skipped a level
            s = s.replace('<section class="five-ws" id="solution"><div class="ws-grid">', '<section class="five-ws" id="solution" aria-labelledby="facts-h"><h2 id="facts-h" class="visually-hidden">All facts</h2><div class="ws-grid">', 1)
        for a in re.findall(r'<img\b[^>]*alt="([^"]*)"', s): newalts.add(html.unescape(a))
        wr(f, s)
    # translation memory for composed alts, transcripts
    for l, m in mems.items():
        n0 = len(m)
        for a in newalts:
            if a in m: continue
            mm = re.match(r'^(.+?): (.+)$', a)
            if mm:
                tr = None
                for k2, v2 in D['alt_desc'].items():
                    if v2['en'] == mm.group(2): tr = v2[l]
                tr = tr or m.get(mm.group(2))
                if tr: m[a] = f'{mm.group(1)}{" :" if l == "fr" else ":"} {tr[0].lower() + tr[1:] if l == "fr" and False else tr}'
        for fx in D['alt_fix'].values():
            if isinstance(fx, dict): m.setdefault(fx['en'], fx[l])
        for v in D['videos'].values():
            m.setdefault(v['visual']['en'], v['visual'][l])
            for _, _, c in v['cues']: m.setdefault(c['en'], c[l])
        for k2, v2 in UI.items(): m.setdefault(k2, v2[l])
        if len(m) != n0: json.dump(m, open(f'i18n/{l}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    os.makedirs('assets/captions', exist_ok=True)
    for v, x in D['videos'].items():
        for l in ['en'] + LANGS: open(f'assets/captions/{v}.{l}.vtt', 'w', encoding='utf8').write(vtt(x['cues'], l))
    print(f'a11y-pass: {tot} alts rewritten on English pages; captions for {len(D["videos"])} videos x {1+len(LANGS)} languages')

if __name__ == '__main__':
    main()
