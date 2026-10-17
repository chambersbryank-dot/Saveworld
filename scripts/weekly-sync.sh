#!/usr/bin/env bash
# Weekly (or daily; idempotent) translation sync. Hook for the daily translation sync routine:
# refreshes Solution of the Week (rotation flips Sundays, HST) + batch-2 blocks, rebuilds /fr/ /es/ /ar/ /it/, sitemap, checks.
# Exit non-zero if a check fails. Commit + push only if `git status --porcelain` shows changes.
# Roman: build-roman.py refreshes assets/data/roman.json (JPL Horizons distance + newest NASA image) before the builds.
# Batch 4: build-batch4.py renders Do One Thing Today from assets/data/daily-actions.json (edit there), Community + Find a Cleanup pages, nav/footer links.
# Analytics: build-analytics.py (Oct 16) strips GA4/consent.js remnants and adds the cookie-free Cloudflare Web Analytics beacon + Privacy text.
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
python3 scripts/build-analytics.py
python3 scripts/dept-contacts.py         # Oct 14: EN department blocks before translation
python3 scripts/disable-community.py
python3 scripts/build-fivews.py          # Oct 15: sourced Five W's for Roman + tsunami horizon tools (EN + i18n strings)
python3 scripts/i18n-build.py
# Translation freshness is checked right after i18n-build stamps hashes: later all-language post-processors
# (heroes, mailto, dept-contacts, a11y, video schema...) edit English too and would always read as stale.
node scripts/i18n-check.js | tail -3
python3 scripts/a11y-pass.py --translated # point caption tracks at fr/es/ar/it
python3 scripts/build-analytics.py
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
python3 scripts/build-data-tools.py     # Oct 15: Use this data (CSV + Cite + Embed) on Amazing Facts, Myth vs Fact, World Map, homepage Scoreboard; per-item Cite (all langs)
python3 scripts/build-standards.py      # Oct 15: NGSS/Common Core alignment (standards.json): teacher boxes, Teachers grade/subject browse, Lesson Builder table (all langs)
python3 scripts/build-sol-directory.py  # Oct 15: Solutions filters: status, region (map pins), grade (standards), name; URL state (all langs)
python3 scripts/build-ux.py            # Oct 15: grouped nav, homepage domains/news, Solutions filters, auto counts, About video 720p-first
python3 scripts/build-glass.py  # Oct 15 item 6: Liquid Glass only on primary buttons + nav panels; flat tinted icons; -webkit- pairing; reduced-transparency/contrast fallbacks
python3 scripts/build-spotfire.py       # Oct 15: astroEDU "Spot the Fire from Space" page (all langs) + links from Teachers/Kids_Map/FireSat/Lesson_Builder + sitemap
python3 scripts/build-play.py           # Oct 15 item 9: Kids Play & Learn hub (all langs), progress badges (site.js PLAY block), homepage Kids card
python3 scripts/build-learn.py           # Oct 16 Phase 1 education: Learn hub (3 tracks), Orbits_Guide, Orbit_Math (KaTeX at build), Orbit_Lab (all langs)
node scripts/test-orbit-lab.js >/dev/null  # Orbit Lab physics unit test (fails the sync on error)
if [ -f scripts/test-aero-lab.js ]; then node scripts/test-aero-lab.js >/dev/null; fi   # Aero Lab physics unit test (Phase 2)
python3 scripts/build-si-helper.py      # Oct 16: SI Helper pilot widget (Teachers), SI_Helper.html, Privacy section (all langs)
node scripts/test-phys-lab.js >/dev/null   # Physics Lab unit test (Phase 3): JS vs phys_calc.py
python3 scripts/build-new.py            # Oct 15 item 10: dated New this week strip (home x5, Solutions, World_Map) + Changelog.html from git first-publish dates
python3 scripts/build-nav.py            # Oct 16: header nav v2 (two rows, dropdowns, mobile accordion); LAST page generator so copied pages get correct nav
python3 scripts/build-analytics.py      # Oct 16: again after the late generators (Cloudflare beacon on every page, no GA, Privacy/About analytics text)
python3 scripts/build-report-link.py    # Oct 15: Report a correction footer link (all langs) -> GitHub issue form
python3 scripts/si-credits.py --check        # Oct 15: visible SI credit caption next to every SI-generated image (all langs)
python3 scripts/build-og.py             # Oct 15 item 7: distinct 1200x630 share card per page per language (assets/og/), SI credit on the card when the photo is SI
python3 scripts/seo-audit.py | tail -3
# Search (Oct 12): rebuild the committed Pagefind + semantic indexes from the final HTML (both layers in one step).
[ -d node_modules ] || npm ci --no-audit --no-fund >/dev/null
node scripts/build-search.mjs
# Oct 16: SI Helper pilot retrieval index (Workers AI bge-m3 -> Vectorize si-helper-site). Incremental; only runs on the box
# where the Cloudflare token file exists; never fails the sync.
if [ -f /home/box/.cloudflare_token ]; then python3 scripts/si-index.py || echo 'si-index: failed (non-fatal)'; fi
# IndexNow (Oct 14): pages are not live yet at this point. After committing + pushing, run
#   bash scripts/post-deploy.sh   (waits for the live key file, pings changed URLs, never fails the sync)
# With WEEKLY_SYNC_POST_DEPLOY=1 the caller has already pushed, so ping now.
if [ "${WEEKLY_SYNC_POST_DEPLOY:-0}" = 1 ]; then bash scripts/post-deploy.sh || true; fi
