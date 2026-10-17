#!/usr/bin/env bash
# Run AFTER weekly-sync.sh output is committed and pushed (GitHub Pages deploy).
# Waits for the live IndexNow key file, then submits pages changed since the last successful ping. Never fails.
cd "$(dirname "$0")/.."
# Oct 16: SEO lint first (prints gap counts; errors are reported loudly but never block the IndexNow ping).
python3 scripts/seo-lint.py > /tmp/seo-lint-post.log; rc=$?; tail -8 /tmp/seo-lint-post.log
[ "$rc" = 0 ] || echo "SEO LINT FAILED: run python3 scripts/seo-lint.py --list and fix the generators (scripts/seo-fix.py, seo-jsonld.py, i18n/seo-meta.json)"
node scripts/indexnow-ping.js --send --wait || echo "IndexNow ping failed (ignored)"
