#!/usr/bin/env bash
# Weekly (or daily; idempotent) translation sync. Hook for the daily translation sync routine:
# refreshes Solution of the Week (rotation flips Sundays, HST) + batch-2 blocks, rebuilds /fr/ /es/ /ar/ /it/, sitemap, checks.
# Exit non-zero if a check fails. Commit + push only if `git status --porcelain` shows changes.
# Roman: build-roman.py refreshes assets/data/roman.json (JPL Horizons distance + newest NASA image) before the builds.
# Batch 4: build-batch4.py renders Do One Thing Today from assets/data/daily-actions.json (edit there), Community + Find a Cleanup pages, nav/footer links.
# GA4: add-gtag.py injects the G-M5L2259Z68 tag after <head> on every page (idempotent, Consent Mode).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build-roman.py || echo "build-roman failed (kept previous data)"
python3 scripts/build-home-extras.py
python3 scripts/build-batch2.py
python3 scripts/build-batch3.py
python3 scripts/build-batch4.py
python3 scripts/build-solutions-index.py   # Solutions.html directory + plain Solutions nav link (Oct 12)
node scripts/newsletter-updates-sync.js || true  # Oct 14: 'feat(Page.html): ...' commits and NOTES.md '## Newsletter' bullets -> scripts/newsletter-updates.json (What's New)
node build-stats.js --data-only          # Oct 14: live solution/hub counts (assets/data/solutions.json) from Solutions.html
python3 scripts/build-trust.py             # Oct 14: Privacy, Editorial_Policy, Corrections, Topics A-Z (+ i18n strings)
python3 scripts/build-batch-b.py           # ELI10 / teacher / cite boxes, Glossary + Teachers pages, homepage audience row (Oct 12)
python3 scripts/build-site-extras.py        # footer site map, Sitemap.html, <main> landmark, video labels, extras.css (Oct 13)
python3 scripts/build-batch-a.py   # Batch A (Oct 12): share bar, Last reviewed + sources, Related Solutions (from last semantic index), difference strip
python3 scripts/build-edu.py               # Oct 14: Kids Map, Lesson Builder, Satellite Explorer + edu.<lang>.json + links
python3 scripts/a11y-pass.py              # Oct 14: specific img alts, video captions (WebVTT) + transcripts, i18n memory
python3 scripts/add-gtag.py
python3 scripts/dept-contacts.py         # Oct 14: EN department blocks before translation
python3 scripts/disable-community.py
python3 scripts/build-fivews.py          # Oct 15: sourced Five W's for Roman + tsunami horizon tools (EN + i18n strings)
python3 scripts/i18n-build.py
# Translation freshness is checked right after i18n-build stamps hashes: later all-language post-processors
# (heroes, mailto, dept-contacts, a11y, video schema...) edit English too and would always read as stale.
node scripts/i18n-check.js | tail -3
python3 scripts/a11y-pass.py --translated # point caption tracks at fr/es/ar/it
python3 scripts/add-gtag.py
python3 scripts/apply-heroes.py           # Oct 14: themed page heroes (all langs)
python3 scripts/optimize-images.py        # Oct 14: WebP srcset for homepage cards (all langs)
python3 scripts/add-video-schema.py       # Oct 14: VideoObject JSON-LD (all langs)
python3 scripts/link-errors.py           # Oct 14: errors@ mailto for error/bug reports (all langs)
python3 scripts/dept-contacts.py         # Oct 14: department inboxes (all langs)
python3 scripts/mailto-subjects.py        # Oct 14: purpose subject on every mailto (all langs)
python3 scripts/disable-community.py     # Oct 14: Community Wall paused (archived; flag inside)
python3 scripts/i18n-sitemap.py
node build-stats.js --data-only          # Oct 15: re-run after the sitemap lists every English page, so new solutions land in solutions.json (one entry per page)
python3 scripts/build-edu.py --translated   # satellite part names in fr/es/ar/it
python3 scripts/build-batch-b.py --glossary  # tap/hover glossary definitions in en/fr/es/ar/it (after translation)
python3 scripts/build-map.py           # Oct 15: World Map (assets/data/map-locations.json pins + Launch Library 2 rocket sites, RU/CN/KP excluded) -> map.<lang>.json + World_Map.html (all langs)
python3 scripts/build-ux.py            # Oct 15: grouped nav, homepage domains/news, Solutions filters, auto counts, About video 720p-first
python3 scripts/build-spotfire.py       # Oct 15: astroEDU "Spot the Fire from Space" page (all langs) + links from Teachers/Kids_Map/FireSat/Lesson_Builder + sitemap
python3 scripts/si-credits.py           # Oct 15: visible SI credit caption next to every SI-generated image (all langs)
python3 scripts/seo-audit.py | tail -3
# Search (Oct 12): rebuild the committed Pagefind + semantic indexes from the final HTML (both layers in one step).
[ -d node_modules ] || npm ci --no-audit --no-fund >/dev/null
node scripts/build-search.mjs
# IndexNow (Oct 14): pages are not live yet at this point. After committing + pushing, run
#   bash scripts/post-deploy.sh   (waits for the live key file, pings changed URLs, never fails the sync)
# With WEEKLY_SYNC_POST_DEPLOY=1 the caller has already pushed, so ping now.
if [ "${WEEKLY_SYNC_POST_DEPLOY:-0}" = 1 ]; then bash scripts/post-deploy.sh || true; fi
