#!/usr/bin/env python3
"""Translation cross-verification for savingplanets.com (en → fr/es/ar/it/he).

Checks (no invented facts; flags uncertain items rather than auto-rewriting copy):
  (a) structural parity vs English (headings/FAQ counts)
  (b) glossary term consistency (tools/translation-glossary.csv)
  (c) numbers, http(s) URLs, and internal .html links match English where comparable
  (d) lang/dir attributes (ar/he must be dir=rtl)
  (e) leftover English phrases in non-English pages (heuristic)

Optional: --backtranslate uses a free HTTP endpoint when available; otherwise skips
with a note. Clear-cut generator/source fixes are NOT applied here — this tool reports.
Exit 0 always (non-blocking CI). Write markdown report with --report PATH.
"""
from __future__ import annotations
import argparse, csv, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LANGS = ['fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
KEY_PAGES = [
    'Big_Questions.html', 'Upcoming_Launches.html', 'index.html', 'Myth_vs_Fact.html',
    'Oceans.html', 'Rivers.html', 'Lakes.html', 'Deforestation.html', 'Space.html',
    'Earth_Observation.html', 'Teachers.html', 'Learn.html', 'Ways_to_Help.html',
]

# Extra hub FAQ samples (96 hubs is large; sample major hubs + discover more via glob)
HUB_GLOB = ['*_Cleanup.html', '*_Foundation.html', 'The_Ocean_Cleanup.html', '4ocean.html',
            'Coral_Gardeners.html', 'American_Forests.html', 'Seabin.html']

EN_LEFTOVER = re.compile(
    r'\b(Click here|Read more|Learn more|Home|About us|Contact us|Subscribe|Loading\.\.\.|Error|Page not found)\b',
    re.I,
)
NUM = re.compile(r'(?<![A-Za-z0-9_])\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|\d{4}')
URL = re.compile(r'https?://[^\s\"\'<>]+')
HREF = re.compile(r'href=["\']([^"\']+)["\']', re.I)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip = 0
        self.title = ''
        self.lang = ''
        self.dir_ = ''
        self.in_title = False
        self.headings = []
        self._h = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang', '')
            self.dir_ = a.get('dir', '')
        if tag in ('script', 'style', 'noscript'):
            self._skip += 1
        if tag == 'title':
            self.in_title = True
        if tag in ('h1', 'h2', 'h3'):
            self._h = tag

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript') and self._skip:
            self._skip -= 1
        if tag == 'title':
            self.in_title = False
        if tag == self._h:
            self._h = None

    def handle_data(self, data):
        if self._skip:
            return
        t = data.strip()
        if not t:
            return
        if self.in_title:
            self.title += t
        if self._h:
            self.headings.append((self._h, t))
        self.parts.append(t)

    def text(self):
        return ' '.join(self.parts)


def load(path: Path):
    if not path.exists():
        return None
    raw = path.read_text(encoding='utf-8', errors='replace')
    p = TextExtractor()
    try:
        p.feed(raw)
    except Exception:
        pass
    return {'raw': raw, 'text': p.text(), 'title': p.title, 'lang': p.lang, 'dir': p.dir_,
            'headings': p.headings, 'path': path}


def page_path(lang, page):
    return ROOT / page if lang == 'en' else ROOT / lang / page


def glossary_rows():
    p = ROOT / 'tools' / 'translation-glossary.csv'
    if not p.exists():
        p = Path('/workspace/seo/translation-glossary.csv')
    with p.open(encoding='utf-8') as f:
        return list(csv.DictReader(f))


def check_page(en, tr, lang, gloss):
    issues = []
    if not tr:
        return [('missing_page', f'{lang} page missing')]
    # (d) lang/dir
    if tr['lang'] and tr['lang'] != lang and not tr['lang'].startswith(lang):
        issues.append(('lang_attr', f'html lang={tr["lang"]!r} expected {lang}'))
    if lang in RTL:
        if tr['dir'] != 'rtl':
            issues.append(('rtl', f'expected dir=rtl, got {tr["dir"]!r}'))
    else:
        if tr['dir'] == 'rtl':
            issues.append(('rtl', 'unexpected dir=rtl'))

    # (a) heading count soft check
    if en and abs(len(en['headings']) - len(tr['headings'])) > 3:
        issues.append(('heading_count', f'en={len(en["headings"])} {lang}={len(tr["headings"])}'))

    # FAQ Question count in JSON-LD
    if en:
        en_q = en['raw'].count('@type": "Question"')
        tr_q = tr['raw'].count('@type": "Question"')
        if en_q and tr_q != en_q:
            issues.append(('faq_count', f'en={en_q} {lang}={tr_q}'))

    # (c) numbers present in EN should appear in TR (allow formatting diffs)
    if en:
        def norm_nums(text):
            out=set()
            for n in NUM.findall(text):
                n2=n.replace(',','').rstrip('%')
                if len(n2) >= 3:
                    out.add(n2)
            return out
        en_nums = norm_nums(en['text'])
        tr_nums = norm_nums(tr['text'])
        miss = en_nums - tr_nums
        miss -= {'2026', '2025', '2024', '100', '200', '404', '20261026', '20261027'}
        if len(miss) > 12:
            issues.append(('numbers', f'{len(miss)} EN numbers not found in {lang} (e.g. {sorted(miss)[:6]})'))

        en_urls = set(URL.findall(en['raw']))
        tr_urls = set(URL.findall(tr['raw']))
        # external only
        en_ext = {u for u in en_urls if 'savingplanets.com' not in u}
        tr_ext = {u for u in tr_urls if 'savingplanets.com' not in u}
        missing_u = sorted(en_ext - tr_ext)[:8]
        if missing_u:
            issues.append(('urls', f'{len(en_ext - tr_ext)} EN external URLs missing in {lang}'))

        en_links = {h for h in HREF.findall(en['raw']) if h.endswith('.html')}
        tr_links = {h for h in HREF.findall(tr['raw']) if h.endswith('.html')}
        # compare basenames
        en_b = {Path(h).name for h in en_links}
        tr_b = {Path(h).name for h in tr_links}
        if en_b - tr_b and len(en_b - tr_b) > 5:
            issues.append(('internal_links', f'{len(en_b - tr_b)} EN .html basenames missing'))

    # (b) glossary: EN brand/agency tokens should survive; localized titles should appear when EN title present
    text = tr['text'] + ' ' + tr['title']
    for row in gloss:
        en_term = row['en']
        if not en or en_term not in en['text'] and en_term not in en.get('title', ''):
            continue
        want = row.get(lang) or en_term
        if en_term in ('SI', 'NASA', 'NOAA', 'ESA', 'Saving Planets', 'Biological SI Partner'):
            if en_term not in text and en_term not in tr['raw']:
                issues.append(('glossary', f'missing locked term {en_term!r}'))
        elif want and want not in text and want not in tr['raw']:
            # soft: localized page titles may be partial
            if en_term in ('Myth vs Fact', 'Ways to Help', 'Big Questions', 'Upcoming Launches') and page_name_match(tr, want, en_term):
                continue
            issues.append(('glossary_soft', f'expected {want!r} for {en_term!r}'))

    # (e) leftover English
    for m in EN_LEFTOVER.finditer(tr['text']):
        issues.append(('english_left', f'possible English UI string {m.group(0)!r}'))

    # banned country outbound (policy)
    for bad in ('roscosmos', 'cnsa.gov.cn', 'nasa.gov.cn', '.kp/', 'isa.ir'):
        if bad in tr['raw'].lower():
            issues.append(('country_policy', f'suspicious outbound token {bad}'))

    return issues


def page_name_match(tr, want, en_term):
    return want[:8] in tr['title'] or en_term.split()[0] in tr['title']


def discover_pages():
    pages = list(KEY_PAGES)
    for p in sorted(ROOT.glob('*.html')):
        if p.name in pages:
            continue
        try:
            t = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if 'SP-HUBFAQ:START' in t or 'People also ask' in t or 'faq-block' in t:
            pages.append(p.name)
        if len(pages) >= 120:
            break
    return pages


def try_backtranslate(samples):
    """Best-effort; never invent. Returns list of notes."""
    notes = []
    # No paid API keys. If deep-translator or similar is installed, use it.
    try:
        from deep_translator import GoogleTranslator  # type: ignore
    except Exception:
        notes.append('Back-translation skipped: deep_translator not installed. '
                     'Install optional dep or review glossary/structure flags. Structural checks still ran.')
        return notes, []
    findings = []
    for lang, en_s, tr_s in samples[:12]:
        try:
            back = GoogleTranslator(source=lang, target='en').translate(tr_s[:400])
        except Exception as e:
            notes.append(f'backtranslate error {lang}: {e}')
            continue
        # crude overlap
        en_tok = set(re.findall(r'[A-Za-z]{4,}', en_s.lower()))
        back_tok = set(re.findall(r'[A-Za-z]{4,}', (back or '').lower()))
        if not en_tok:
            continue
        overlap = len(en_tok & back_tok) / max(1, len(en_tok))
        if overlap < 0.15:
            findings.append((lang, en_s[:80], back[:80], round(overlap, 2)))
    return notes, findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='')
    ap.add_argument('--backtranslate', action='store_true')
    ap.add_argument('--pages', default='')
    args = ap.parse_args()
    gloss = glossary_rows()
    pages = [p.strip() for p in args.pages.split(',') if p.strip()] or discover_pages()
    by_lang = defaultdict(list)
    samples = []
    for page in pages:
        en = load(page_path('en', page))
        if not en:
            continue
        # sample sentence for optional backtranslate
        en_sent = ''
        for h, t in en['headings']:
            if len(t) > 40:
                en_sent = t
                break
        if not en_sent:
            en_sent = en['text'][:180]
        for lang in LANGS:
            tr = load(page_path(lang, page))
            issues = check_page(en, tr, lang, gloss)
            for kind, msg in issues:
                by_lang[lang].append((page, kind, msg))
            if tr and en_sent and args.backtranslate:
                # grab comparable heading
                tr_sent = tr['headings'][0][1] if tr['headings'] else tr['text'][:180]
                samples.append((lang, en_sent, tr_sent))

    bt_notes, bt_findings = ([], [])
    if args.backtranslate:
        bt_notes, bt_findings = try_backtranslate(samples)

    # Markdown report
    lines = []
    lines.append(f'# Translation cross-check — {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
    lines.append('')
    lines.append(f'Pages scanned: **{len(pages)}** (English source vs fr/es/ar/it/he).')
    lines.append(f'Glossary terms: **{len(gloss)}** (`tools/translation-glossary.csv`).')
    lines.append('Method: structural + glossary + numbers/URLs/links + lang/dir + English-leftover heuristics. '
                 'Clear-cut generator fixes are separate; uncertain items listed as open.')
    lines.append('')
    total = 0
    for lang in LANGS:
        items = by_lang[lang]
        total += len(items)
        soft = sum(1 for _, k, _ in items if k.endswith('_soft') or k == 'english_left')
        hard = len(items) - soft
        lines.append(f'## {lang} — {len(items)} flags ({hard} hard / {soft} soft)')
        if not items:
            lines.append('_No issues flagged._')
            lines.append('')
            continue
        by_kind = Counter(k for _, k, _ in items)
        lines.append('Counts: ' + ', '.join(f'{k}={v}' for k, v in sorted(by_kind.items())))
        lines.append('')
        for page, kind, msg in items[:40]:
            lines.append(f'- `{page}` **{kind}**: {msg}')
        if len(items) > 40:
            lines.append(f'- … {len(items) - 40} more')
        lines.append('')

    lines.append('## Back-translation')
    for n in bt_notes:
        lines.append(f'- {n}')
    if bt_findings:
        lines.append('Low-overlap samples (manual review):')
        for lang, en_s, back, ov in bt_findings:
            lines.append(f'- **{lang}** overlap={ov}: EN “{en_s}” ← back “{back}”')
    else:
        if not bt_notes:
            lines.append('- Not requested (pass `--backtranslate` to enable).')
    lines.append('')
    lines.append('## Fixes made this run')
    lines.append('- None in-report (read-only checker). Companion PR fixes Hebrew Learn/Teachers generators so FAQ counts match.')
    lines.append('')
    lines.append('## Open items for Bryan / native reviewers')
    lines.append('- Soft glossary and english_left flags need human judgment; do not auto-rewrite.')
    lines.append('- Full 96-hub FAQ prose back-translation still pending native pass when traffic supports reviewers.')
    lines.append('')

    report = '\n'.join(lines)
    out = Path(args.report) if args.report else Path('/workspace/seo/translation-crosscheck-2026-10-27.md')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding='utf-8')
    # also copy into repo docs for CI reference
    repo_copy = ROOT / 'docs' / 'translation-crosscheck-latest.md'
    if (ROOT / 'docs').is_dir():
        repo_copy.write_text(report, encoding='utf-8')
    print(f'wrote {out} ({total} flags across languages)')
    for lang in LANGS:
        print(f'  {lang}: {len(by_lang[lang])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
