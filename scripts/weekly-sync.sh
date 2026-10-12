#!/usr/bin/env bash
# Weekly (or daily; idempotent) translation sync. Hook for the daily translation sync routine:
# refreshes Solution of the Week (rotation flips Sundays, HST) + batch-2 blocks, rebuilds /fr/ /es/ /ar/, sitemap, checks.
# Exit non-zero if a check fails. Commit + push only if `git status --porcelain` shows changes.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build-home-extras.py
python3 scripts/build-batch2.py
python3 scripts/build-batch3.py
python3 scripts/i18n-build.py
python3 scripts/i18n-sitemap.py
python3 scripts/seo-audit.py | tail -3
node scripts/i18n-check.js | tail -3
