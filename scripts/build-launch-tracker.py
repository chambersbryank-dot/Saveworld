#!/usr/bin/env python3
"""Upgrade the Live Launch Tracker on Upcoming_Launches.html (all langs).

After PR #132 the Live Launch Tracker list (<ul class="lw-list" id="lw-list">)
lives on Upcoming_Launches.html, not Artemis_II.html. Idempotent: refreshes the
English chrome note and assets/launch-tracker.js tag. Translations come from
i18n/<lang>.json via scripts/i18n-build.py.

Artemis_II.html keeps only a handoff link (no #lw-list); this script skips it
and any other page that no longer hosts the list.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
V = "20261026d"  # bump with launch-tracker.js
HUB = "Upcoming_Launches.html"
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
# i18n-build sometimes rewrites attribute order on translated pages
EXT_RE_ALT = re.compile(
    r'<script defer="" src="(?:\.\./)?assets/launch-tracker\.js\?v=[^"]*"></script>',
)


def has_tracker_list(html: str) -> bool:
    return 'id="lw-list"' in html and 'class="lw-list"' in html


def patch_en_box(html: str) -> str:
    """Insert / refresh the blurb explainer note before lw-more (English source)."""
    def repl(m):
        return (
            m.group(1)
            + '<p class="lw-note">Note: Launches shift left and right all the time - stay updated.</p>'
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
    if EXT_RE_ALT.search(html):
        return EXT_RE_ALT.sub(tag, html, count=1)
    # Fallback: insert before launch-actions if present
    if "launch-actions.js" in html:
        m = re.search(
            rf'<script[^>]*src="{re.escape(pre)}assets/launch-actions\.js[^"]*"[^>]*></script>',
            html,
        )
        if not m:
            m = re.search(
                r'<script[^>]*src="(?:\.\./)?assets/launch-actions\.js[^"]*"[^>]*></script>',
                html,
            )
        if m:
            return html[: m.start()] + tag + "\n" + html[m.start() :]
    if "</body>" in html:
        return html.replace("</body>", tag + "\n</body>", 1)
    raise SystemExit("could not place launch-tracker.js")


def hub_path(lang: str) -> pathlib.Path:
    return ROOT / HUB if not lang else ROOT / lang / HUB


n = 0

# Artemis_II no longer hosts the list (PR #132). Skip quietly if the list is gone.
for lg in LANGS:
    art = ROOT / "Artemis_II.html" if not lg else ROOT / lg / "Artemis_II.html"
    if art.exists():
        raw = art.read_text(encoding="utf-8")
        if has_tracker_list(raw):
            print(
                "warn: Artemis_II still has #lw-list;",
                art.relative_to(ROOT),
                "(not patched; hub is canonical)",
            )
        else:
            print("skip", art.relative_to(ROOT), "(no #lw-list; handoff only)")

# Canonical host: Upcoming_Launches.html in all six languages
for lg in LANGS:
    p = hub_path(lg)
    if not p.exists():
        print("skip missing", p.relative_to(ROOT))
        continue
    s = p.read_text(encoding="utf-8")
    if not has_tracker_list(s):
        print("skip", p.relative_to(ROOT), "(no #lw-list)")
        continue
    pre = "" if not lg else "../"
    s2 = s
    if not lg:
        s2 = patch_en_box(s2)
    s2 = patch_script(s2, pre)
    # Ensure blurb-note exists after translation (English note may still be present until i18n-build)
    if lg and 'class="lw-blurb-note"' not in s2 and 'class="lw-note"' in s2:
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
    else:
        print("unchanged", p.relative_to(ROOT))

print(n, "pages touched; script v=", V)
