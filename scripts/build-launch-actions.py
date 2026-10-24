#!/usr/bin/env python3
"""Adds the launch tracker action buttons (assets/launch-actions.js) to every page
with the Launch Library widget (#lw-next), in all languages. Idempotent; bump V to bust caches."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
V = "20261024a"
LANGS = ["", "fr", "es", "ar", "it", "he"]
n = 0
for lg in LANGS:
    d = ROOT / lg if lg else ROOT
    for p in sorted(d.glob("*.html")):
        s = p.read_text(encoding="utf-8")
        if 'id="lw-next"' not in s:
            continue
        pre = "../" if lg else ""
        tag = f'<script src="{pre}assets/launch-actions.js?v={V}" defer></script>'
        s2 = re.sub(r'<script src="(?:\.\./)?assets/launch-actions\.js\?v=[^"]*" defer></script>', tag, s)
        if tag not in s2:
            s2 = s2.replace("</body>", tag + "\n</body>", 1)
        if s2 != s:
            p.write_text(s2, encoding="utf-8"); n += 1
            print("updated", p.relative_to(ROOT))
print(n, "pages updated")
