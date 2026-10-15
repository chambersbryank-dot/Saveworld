# Community Wall (archived Oct 14, 2026)
Paused until traffic grows. Not published (Jekyll skips `_` folders).
Restore:
1. Set `COMMUNITY_ENABLED = True` in scripts/build-batch4.py and scripts/disable-community.py.
2. Add `Community.html` back to i18n/pages.txt; remove it from SKIP in scripts/build-search.mjs.
3. Delete the redirect stubs (Community.html, fr/, es/, ar/) or copy these archived files back over them.
4. Run scripts/weekly-sync.sh (rebuilds the page, nav/footer links, sitemap, translations).
Data: assets/data/community.json (kept in place).
