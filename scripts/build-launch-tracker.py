#!/usr/bin/env python3
"""Upgrade the Live Launch Tracker on Artemis_II.html (all langs).

Replaces the inline Launch Library 2 widget script with assets/launch-tracker.js
(purpose blurbs + Saving Planets connection; sourced from LL2 only). Idempotent.
Also refreshes the English chrome note; translations come from i18n/<lang>.json
via scripts/i18n-build.py.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
V = "20261026d"  # bump with launch-tracker.js
LANGS = ["", "fr", "es", "ar", "it", "he"]

NOTE_EN = (
    "Each launch includes the mission purpose when agencies have published it, "
    "plus a short note on whether it supports a Saving Planets solution. "
    "Launches that help a solution link to that solution&#x27;s page; "
    "others link to the operator&#x27;s official page. "
    "If details are not public yet, we say so."
)

BOX_RE = re.compile(
    r'(<div class="lw-box">.*?<ul class="lw-list" id="lw-list"></ul>)'
    r'.*?(<p class="lw-more">)',
    re.S,
)

SCRIPT_RE = re.compile(
    r"<script>\s*\(function \(\) \{\s*var API = 'https://ll\.thespacedevs\.com[\s\S]*?</script>",
    re.S,
)
# Also match already-external tag (idempotent refresh)
EXT_RE = re.compile(
    r'<script src="(?:\.\./)?assets/launch-tracker\.js\?v=[^"]*" defer></script>',
)

def patch_en_box(html: str) -> str:
    """Insert / refresh the blurb explainer note before lw-more (English source)."""
    def repl(m):
        return (
            m.group(1)
            + f'<p class="lw-note">Note: Launches shift left and right all the time - stay updated.</p>'
            + f'<p class="lw-blurb-note">{NOTE_EN}</p>'
            + m.group(2)
        )
    out, n = BOX_RE.subn(repl, html, count=1)
    if n != 1:
        raise SystemExit(f"lw-box note block not found or ambiguous ({n})")
    return out

def patch_script(html: str, pre: str) -> str:
    tag = f'<script src="{pre}assets/launch-tracker.js?v={V}" defer></script>'
    if SCRIPT_RE.search(html):
        return SCRIPT_RE.sub(tag, html, count=1)
    if EXT_RE.search(html):
        return EXT_RE.sub(tag, html, count=1)
    # Fallback: insert before launch-actions if present
    if "launch-actions.js" in html:
        return html.replace(
            f'<script src="{pre}assets/launch-actions.js',
            tag + "\n" + f'<script src="{pre}assets/launch-actions.js',
            1,
        )
    if "</body>" in html:
        return html.replace("</body>", tag + "\n</body>", 1)
    raise SystemExit("could not place launch-tracker.js")

n = 0
en = ROOT / "Artemis_II.html"
html = en.read_text(encoding="utf-8")
html2 = patch_en_box(html)
html2 = patch_script(html2, "")
if html2 != html:
    en.write_text(html2, encoding="utf-8")
    print("updated Artemis_II.html (en chrome + script)")
    n += 1
else:
    print("en unchanged")

for lg in LANGS:
    if not lg:
        continue
    p = ROOT / lg / "Artemis_II.html"
    if not p.exists():
        print("skip missing", p)
        continue
    s = p.read_text(encoding="utf-8")
    s2 = patch_script(s, "../")
    # Ensure blurb-note exists after translation (English note may still be present until i18n-build)
    if 'class="lw-blurb-note"' not in s2 and 'class="lw-note"' in s2:
        s2 = s2.replace(
            '<p class="lw-note">',
            f'<p class="lw-note">',
            1,
        )
        # insert after first lw-note closing
        s2 = re.sub(
            r'(<p class="lw-note">.*?</p>)',
            r'\1<p class="lw-blurb-note">' + NOTE_EN + "</p>",
            s2,
            count=1,
            flags=re.S,
        )
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("updated", p.relative_to(ROOT))
        n += 1

print(n, "pages touched; script v=", V)
