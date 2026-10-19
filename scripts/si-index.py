#!/usr/bin/env python3
"""Oct 16 SI Helper pilot: build the retrieval index of site pages (5 languages) for the si-helper Worker.
Extracts each page's <main> text, splits it into ~900-character chunks, embeds them with Workers AI @cf/baai/bge-m3
(1024-d, multilingual) and upserts them into the Vectorize index 'si-helper-site' (metadata: url, title, lang, text).
Only public page text is indexed. Student_Questions.html (Oct 16) is indexed one chunk per approved entry of assets/data/student-qa.json. Incremental: a manifest of chunk hashes (~/.cache/si-index-state.json on the box) means only changed
chunks are re-embedded, and removed chunks are deleted. Runs from weekly-sync.sh when the Cloudflare token exists on the box.
Usage: python3 scripts/si-index.py [--dry]"""
import os, re, sys, json, html, glob, hashlib
sys.path.insert(0, 'scripts')
SITE = 'https://www.savingplanets.com/'
LANGS = {'en': '', 'fr': 'fr/', 'es': 'es/', 'ar': 'ar/', 'it': 'it/'}
SKIP = {'404.html', 'Search.html', 'Sitemap.html', 'Changelog.html', 'SI_Helper.html', 'googlea5d3cc0c785fec04.html', 'ways-to-help.html', 'ways_to_help.html'}
STATE = os.path.expanduser('~/.cache/si-index-state.json'); INDEX = 'si-helper-site'; MAXC = 900; PER_PAGE = 10
def text_of(s):
    m = re.search(r'<main[^>]*>(.*?)</main>', s, re.S); s = m.group(1) if m else ''
    s = re.sub(r'<!-- (?:LEARNLINK|SIHELPER):START -->.*?<!-- (?:LEARNLINK|SIHELPER):END -->', ' ', s, flags=re.S)
    s = re.sub(r'<(script|style|svg|canvas|noscript|form|nav|pre|math|annotation)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<span class="katex-mathml">.*?</span>', ' ', s, flags=re.S)
    s = re.sub(r'</(p|h[1-6]|li|dt|dd|tr|section|div|summary)>', '\n', s)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    return '\n'.join(x for x in (re.sub(r'[ \t\u00a0]+', ' ', l).strip() for l in s.split('\n')) if len(x) > 2)
def chunks(t):
    out, cur = [], ''
    for para in t.split('\n'):
        if len(cur) + len(para) + 1 > MAXC and cur: out.append(cur); cur = ''
        cur = (cur + '\n' + para).strip()[:MAXC * 2]
    if len(cur) > 80: out.append(cur)
    return out[:PER_PAGE]
def collect():
    docs = []
    for l, pre in LANGS.items():
        for f in sorted(glob.glob(pre + '*.html')):
            name = os.path.basename(f)
            if name in SKIP: continue
            s = open(f, encoding='utf8').read()
            if 'noindex' in s[:3000]: continue
            title = html.unescape(re.sub(r'\s*\|\s*Saving Planets.*$', '', (re.search(r'<title>(.*?)</title>', s, re.S) or [None, name])[1])).strip()
            if name == 'Student_Questions.html':  # Oct 16: one chunk per approved Q&A entry (scripts/build-student-qa.py), linked to its anchor
                for e in [e for e in json.load(open('assets/data/student-qa.json', encoding='utf8')).get('entries', []) if e.get('approved') is True]:
                    c = (e['q'][l] + '\n' + e['a'][l] + '\nSources: ' + '; '.join(x['title'] for x in e['sources']))[:MAXC * 2]
                    cid = hashlib.sha1(f'{l}/{name}#{e["id"]}'.encode()).hexdigest()[:32]
                    docs.append(dict(id=cid, h=hashlib.sha1((title + c).encode()).hexdigest()[:16], url=SITE + pre + name + '#' + e['id'], title=(e['q'][l] + ' | ' + title)[:200], lang=l, text=c))
                continue
            for i, c in enumerate(chunks(text_of(s))):
                cid = hashlib.sha1(f'{l}/{name}#{i}'.encode()).hexdigest()[:32]
                docs.append(dict(id=cid, h=hashlib.sha1((title + c).encode()).hexdigest()[:16], url=SITE + pre + name, title=title[:200], lang=l, text=c))
    return docs
def main():
    docs = collect(); state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    todo = [d for d in docs if state.get(d['id']) != d['h']]; gone = sorted(set(state) - {d['id'] for d in docs})
    print(f'si-index: {len(docs)} chunks, {len(todo)} to embed, {len(gone)} to delete')
    if '--dry' in sys.argv: return
    if not os.path.exists('/home/box/.cloudflare_token'): print('si-index: no Cloudflare token on this machine, skipped'); return
    import si_cf
    for i in range(0, len(todo), 50):
        b = todo[i:i + 50]
        emb = si_cf.call('POST', '/accounts/{acct}/ai/run/@cf/baai/bge-m3', {'text': [d['title'] + '\n' + d['text'] for d in b]})['result']['data']
        nd = '\n'.join(json.dumps(dict(id=d['id'], values=v, metadata=dict(url=d['url'], title=d['title'], lang=d['lang'], text=d['text'])), ensure_ascii=False) for d, v in zip(b, emb))
        si_cf.call('POST', f'/accounts/{{acct}}/vectorize/v2/indexes/{INDEX}/upsert', nd.encode(), ctype='application/x-ndjson', raw=True)
        for d in b: state[d['id']] = d['h']
        if i % 1000 == 0: print(f'  {i + len(b)}/{len(todo)}'); json.dump(state, open(STATE, 'w'), sort_keys=True)
    for i in range(0, len(gone), 100):
        si_cf.call('POST', f'/accounts/{{acct}}/vectorize/v2/indexes/{INDEX}/delete_by_ids', {'ids': gone[i:i + 100]})
        for g in gone[i:i + 100]: state.pop(g, None)
    json.dump(state, open(STATE, 'w'), sort_keys=True, indent=0); print(f'si-index: done, {len(state)} chunks indexed')
if __name__ == '__main__': main()
