# Community Wall (archived Oct 14, 2026)
Paused until traffic grows. Saved copies: branch `archive/community-wall`, folder `_archive/community/{en,fr,es,ar}/Community.html` (kept off main because main publishes the whole repo).
Restore:
1. Set `COMMUNITY_ENABLED = True` in scripts/build-batch4.py and scripts/disable-community.py.
2. Add `Community.html` back to i18n/pages.txt; remove it from SKIP in scripts/build-search.mjs.
3. Delete the redirect stubs (Community.html, fr/, es/, ar/) or copy these archived files back over them.
4. Run scripts/weekly-sync.sh (rebuilds the page, nav/footer links, sitemap, translations).
Data: assets/data/community.json (kept in place).
