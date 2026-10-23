#!/usr/bin/env python3
"""Oct 22 (founder): on solution pages the Impact Statement box is a couple of sentences (source lines are fine).
Everything past the first two sentences moves, word for word and in order, into <div class="impact-detail"> right
below the box, still inside the Impact Statement section: nothing is deleted or reworded. Only the
<section class="impact"><h2>...</h2><div class="impact-box"> block of solution pages (hub/index pages skipped).
English source pages; translations follow via i18n-build. Idempotent: an existing impact-detail is merged back
first, so a generator that rewrites the box never leaves duplicates. -v lists changed pages."""
import os, re, glob, sys
from html.parser import HTMLParser
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
KEEP = 2
HUBS = {'index', 'Solutions', 'Oceans', 'Rivers', 'Lakes', 'Polar', 'Deforestation', 'Earth_Observation', 'Space',
        'Space_Weather', 'Space_Disposal', 'Planetary_Defense', 'Project-Rawane', 'Topics', 'World_Map'}
ABBR = r'(?<!\bU\.S)(?<!\bU\.K)(?<!\bSt)(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bvs)(?<!\bNo)(?<!\bInc)(?<!\bCo)(?<!\bLtd)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bca)(?<!\bJr)(?<!\bMt)'
SPLIT = re.compile(ABBR + r'(?<=[^\s.][.!?])(?:["”’)]?)(?=\s+["“(]?[A-Z0-9])(?![^<]*>)')
HEAD = re.compile(r'<section class="impact"(?: id="impact")?><h2>Impact Statement</h2><div class="impact-box">')
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'wbr'}

class Top(HTMLParser):
    """Top-level children of a fragment as (start, end, tag, attrs-string) offsets; stops at the unmatched </div>."""
    def __init__(s, txt):
        super().__init__(convert_charrefs=False); s.txt = txt; s.depth = 0; s.kids = []; s.end = None; s.cur = None
        s.lines = [0]
        for l in txt.splitlines(True): s.lines.append(s.lines[-1] + len(l))
    def off(s):
        l, c = s.getpos(); return s.lines[l - 1] + c
    def handle_starttag(s, tag, attrs):
        if s.end is not None: return
        if s.depth == 0: s.cur = [s.off(), None, tag, s.get_starttag_text()]
        if tag not in VOID: s.depth += 1
        elif s.depth == 0: s.cur[1] = s.off() + len(s.get_starttag_text()); s.kids.append(s.cur)
    def handle_endtag(s, tag):
        if s.end is not None or tag in VOID: return
        if s.depth == 0:
            if tag == 'div': s.end = s.off()
            return
        s.depth -= 1
        if s.depth == 0:
            e = s.txt.index('>', s.off()) + 1; s.cur[1] = e; s.kids.append(s.cur)

MASK = re.compile(r'<span class="gl">.*?</span></span>|<(a|abbr|button|sup)\b[^>]*>.*?</\1>', re.S)
def split_sentences(h):
    """Glossary tooltips, links etc. are masked so their inner text never counts as a sentence end."""
    saved = []
    def hide(m): saved.append(m.group(0)); return f'\x00{len(saved) - 1}\x00'
    t = MASK.sub(hide, h)
    out, last = [], 0
    for m in SPLIT.finditer(t): out.append(t[last:m.end()]); last = m.end()
    out.append(t[last:])
    back = lambda x: re.sub('\x00(\\d+)\x00', lambda m: saved[int(m.group(1))], x)
    return [back(x).strip() for x in out if x.strip()]

def rebuild(inner, split=True):
    p = Top(inner); p.feed(inner)
    if p.end is None: return None
    kids = [(inner[a:b], tag, st) for a, b, tag, st in p.kids]
    if re.sub(r'\s+', '', ''.join(inner[a:b] for a, b, _, _ in p.kids)) != re.sub(r'\s+', '', inner[:p.end]): return None  # stray text: leave
    is_meta = lambda h, t, st: t == 'p' and ('fact-source' in st or 'hub-label' in st or re.fullmatch(r'<p[^>]*>\s*<a [^>]*>[^<]*</a>\s*</p>', h))
    keep, rest, count, done = [], [], 0, False
    for h, t, st in kids:
        if done and not rest and is_meta(h, t, st) and 'hub-label' not in st: keep.append(h); continue  # source line right after the kept sentences
        if done: rest.append(h); continue
        if is_meta(h, t, st): keep.append(h); continue
        if t != 'p': done = True; rest.append(h); continue
        body = h[len(st):-4]
        ss = split_sentences(body)
        if not split: ss = [' '.join(ss)] if len(ss) <= KEEP - count or not keep else ss  # whole paragraphs only
        if not split and len(ss) > 1: done = True; rest.append(h); continue
        take = ss[:KEEP - count]; count += len(take) if split else len(split_sentences(body))
        keep.append(st + ' '.join(take) + '</p>')
        if ss[len(take):]: rest.append(st + ' '.join(ss[len(take):]) + '</p>')
        if count >= KEEP: done = True
    # source lines that belong to moved text travel with it: only sources before the first moved item stay in the box
    return ''.join(keep), ''.join(rest), p.end

# ---- translation memory: a paragraph split in two makes two new English strings; derive their translations from the
# existing translation of the whole string by sentence count (only when the sentence counts match; else English shows
# until the next translation pass, and the page is listed).
import json
from bs4 import BeautifulSoup
MEM_LANGS = ('fr', 'es', 'ar', 'it', 'he')
MEM = {l: json.load(open(f'i18n/{l}.json', encoding='utf8')) for l in MEM_LANGS if os.path.exists(f'i18n/{l}.json')}
MEM_DIRTY = set(); MEM_MISS = []
TSPLIT = re.compile(r'(?<=[.!?؟。])["”»’)]?\s+')
def texts(h):
    sp = BeautifulSoup(h, 'html.parser')
    for x in sp.select('span.gl-pop'): x.decompose()
    return [t.strip() for t in sp.find_all(string=True) if t.strip()]
def sents(t): return [x for x in TSPLIT.split(t) if x.strip()]
WHOLE = []
def remember(page, old_h, new_h, dry=False):
    old = texts(old_h); new = texts(new_h); olds = set(old)
    fresh = [t for t in new if t not in olds]
    for i, t in enumerate(fresh):
        src = next((o for o in old if o.startswith(t) or o.endswith(t)), None)
        if not src: continue
        es = sents(src); k = len(sents(t)); head = src.startswith(t)
        for l, m in MEM.items():
            if t in m or src not in m: continue
            ts = sents(m[src])
            if len(ts) != len(es):
                if dry: return False
                MEM_MISS.append((page, l)); continue
            if not dry: m[t] = ' '.join(ts[:k] if head else ts[len(ts) - k:]); MEM_DIRTY.add(l)
    return True

n = 0; changed = []
for f in sorted(glob.glob('*.html')):
    if f[:-5] in HUBS: continue
    s = open(f, encoding='utf8').read()
    m = HEAD.search(s)
    if not m: continue
    i = m.end()
    p0 = Top(s[i:]); p0.feed(s[i:])
    if p0.end is None: continue
    box_end = i + p0.end + len('</div>')
    inner = s[i:i + p0.end]
    det = re.match(r'<div class="impact-detail">', s[box_end:])
    det_end = box_end
    if det:
        j = box_end + det.end(); p1 = Top(s[j:]); p1.feed(s[j:])
        if p1.end is None: continue
        inner += s[j:j + p1.end]; det_end = j + p1.end + len('</div>')
    for split in (True, False):
        r = rebuild(inner + '</div>', split)
        if not r: break
        keep, rest, _ = r
        new = keep + '</div>' + (f'<div class="impact-detail">{rest}</div>' if rest else '')
        if split and not remember(f, s[i:det_end], new, dry=True): continue  # a translation can't be split cleanly: whole paragraphs only
        break
    if not r or (not rest and not det): continue
    s2 = s[:i] + new + s[det_end:]
    if s2 != s:
        remember(f, s[i:det_end], new); open(f, 'w', encoding='utf8').write(s2); n += 1; changed.append(f)
        if not split: WHOLE.append(f)
for l in MEM_DIRTY: json.dump(MEM[l], open(f'i18n/{l}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('trim-impact:', n, 'pages updated; translation memory split for', sorted(MEM_DIRTY))
if WHOLE: print('trim-impact: kept whole paragraphs (translations split differently):', len(WHOLE), ' '.join(WHOLE))
if MEM_MISS: print('trim-impact: sentence counts differ, English shown until retranslated:', len(MEM_MISS), sorted(set(MEM_MISS))[:20])
if '-v' in sys.argv: print(' '.join(changed))
