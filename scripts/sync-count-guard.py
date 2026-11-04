#!/usr/bin/env python3
"""Abort the sync before commit if page, category, or question-bank counts drop sharply versus main.

A sharp drop is a new count under 80% of the copy on main (278 -> 0 pages, 10 -> 0
categories, ~1855 -> 259 question-bank rows). Small daily edits still pass.
"""
import csv, json, subprocess, sys

PATHS = {
    'pages': 'assets/data/solutions.json',
    'question-bank': 'assets/data/question-bank.csv',
}

def git_show(path):
    for ref in ('main', 'HEAD'):
        r = subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True)
        if r.returncode == 0:
            return r.stdout.decode('utf-8')
    sys.exit(f'sync-count-guard: cannot read {path} from main or HEAD')

def solution_counts(text):
    data = json.loads(text)
    return len(data.get('pages') or []), len(data.get('categories') or {})

def question_rows(text):
    return sum(1 for _ in csv.DictReader(text.splitlines()))

def sharp(old, new):
    return old > 0 and new * 5 < old * 4

def main():
    base_pages, base_cats = solution_counts(git_show(PATHS['pages']))
    now = json.load(open(PATHS['pages'], encoding='utf-8'))
    pages, cats = len(now.get('pages') or []), len(now.get('categories') or {})
    base_q = question_rows(git_show(PATHS['question-bank']))
    q = question_rows(open(PATHS['question-bank'], encoding='utf-8').read())
    print(f'sync-count-guard: pages {base_pages} -> {pages}')
    print(f'sync-count-guard: categories {base_cats} -> {cats}')
    print(f'sync-count-guard: question-bank {base_q} -> {q}')
    bad = []
    if sharp(base_pages, pages):
        bad.append(f'pages {base_pages} -> {pages}')
    if sharp(base_cats, cats):
        bad.append(f'categories {base_cats} -> {cats}')
    if sharp(base_q, q):
        bad.append(f'question-bank {base_q} -> {q}')
    if bad:
        sys.exit('sync-count-guard: aborting before commit; sharp drop versus main: ' + '; '.join(bad))

if __name__ == '__main__':
    main()
