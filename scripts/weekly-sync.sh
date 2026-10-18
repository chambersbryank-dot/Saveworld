#!/usr/bin/env bash
# Weekly (or daily; idempotent) translation sync. Hook for the daily translation sync routine:
# refreshes Solution of the Week (rotation flips Sundays, HST) + batch-2 blocks, rebuilds /fr/ /es/ /ar/ /it/, sitemap, checks.
# Exit non-zero if a check fails. Commit + push only if `git status --porcelain` shows changes.
# Roman: build-roman.py refreshes assets/data/roman.json (JPL Horizons distance + newest NASA image) before the builds.
# Batch 4: build-batch4.py renders Do One Thing Today from assets/data/daily-actions.json (edit there), Community + Find a Cleanup pages, nav/footer links.
# Analytics: build-analytics.py (Oct 16) strips GA4/consent.js remnants and adds the cookie-free Cloudflare Web Analytics beacon + Privacy text.
set -euo pipefail
cd "$(dirname "$0")/.."
# Oct 17: install build deps first (build-learn/build-calcs need katex before build-search); was only checked right before build-search.
[ -d node_modules ] || npm ci --no-audit --no-fund >/dev/null
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
python3 scripts/build-wow.py               # Oct 17: first-screen wow rule (EN source moves + WOW CSS block)
python3 scripts/build-biosi-cc.py           # Oct 17: Cc biosipartner@ line on Contact + About #cohost
python3 scripts/i18n-build.py
python3 scripts/he-attr-i18n.py             # Oct 17: he/ UI strings in data-t JSON / data-* messages via i18n/he.json
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
python3 scripts/r2-cards.py && python3 scripts/build-ux.py   # Oct 16: card images (home + Related Solutions) get R2 WebP srcset (uploads only new ones), then re-run build-ux
python3 scripts/add-video-schema.py       # Oct 16: re-run after build-ux puts the 720p About source first (VideoObject contentUrl = first source)
python3 scripts/build-glass.py  # Oct 15 item 6: Liquid Glass only on primary buttons + nav panels; flat tinted icons; -webkit- pairing; reduced-transparency/contrast fallbacks
python3 scripts/build-spotfire.py       # Oct 15: astroEDU "Spot the Fire from Space" page (all langs) + links from Teachers/Kids_Map/FireSat/Lesson_Builder + sitemap
python3 scripts/build-play.py           # Oct 15 item 9: Kids Play & Learn hub (all langs), progress badges (site.js PLAY block), homepage Kids card
python3 scripts/build-learn.py           # Oct 16 Phase 1 education: Learn hub (3 tracks), Orbits_Guide, Orbit_Math (KaTeX at build), Orbit_Lab (all langs)
node scripts/test-orbit-lab.js >/dev/null  # Orbit Lab physics unit test (fails the sync on error)
if [ -f scripts/test-aero-lab.js ]; then node scripts/test-aero-lab.js >/dev/null; fi   # Aero Lab physics unit test (Phase 2)
python3 scripts/build-si-helper.py      # Oct 16: SI Helper pilot widget (Teachers), SI_Helper.html, Privacy section (all langs)
python3 scripts/build-student-qa.py     # Oct 16: Student_Questions.html Q&A pool from approved assets/data/student-qa.json (all langs, sitemap, search/student-qa.json; Vectorize via si-index.py)
node scripts/test-phys-lab.js >/dev/null   # Physics Lab unit test (Phase 3): JS vs phys_calc.py
python3 scripts/calc_check.py >/dev/null && node scripts/test-calcs.js >/dev/null  # Oct 16: calculator textbook checks + calc.js vs Python vectors (fails the sync on error)
python3 scripts/build-calcs.py          # Oct 16: 11 search-named calculator pages + Calculators.html (all langs, sitemap)
python3 scripts/build-paths.py          # Oct 16: Careers, Cadets (JROTC+CAP), AP_IB_Physics, Homeschool + Learn hub Start-here block (all langs, sitemap)
python3 scripts/build-new.py            # Oct 15 item 10: dated New this week strip (home x5, Solutions, World_Map) + Changelog.html from git first-publish dates
python3 scripts/build-nav.py            # Oct 16: header nav v2 (two rows, dropdowns, mobile accordion); LAST page generator so copied pages get correct nav
python3 scripts/build-events.py         # Oct 16: privacy-safe aggregate event counter block in site.js (Analytics Engine via si-helper /e)
python3 scripts/build-analytics.py      # Oct 16: again after the late generators (Cloudflare beacon on every page, no GA, Privacy/About analytics text)
python3 scripts/build-report-link.py    # Oct 16: Report a correction footer link (all langs) -> on-site form (Corrections.html#report)
python3 scripts/build-license.py       # Oct 16: CC BY-NC 4.0 footer line, rel=license, JSON-LD license, About "Use & licence" (all langs)
python3 scripts/build-share.py         # Oct 16: Classroom share + copy link (Learn/Teachers), Weekly Brief callout (13+ pages), kids pages: no signup, grown-ups link
python3 scripts/build-embed.py         # Oct 16: Embed button + ?embed=1 minimal mode (calculators, labs, Artemis_II launches)
python3 scripts/build-cohost.py         # Oct 16: About "Co-host with us" (#cohost) + homepage teaser link (all langs)
python3 scripts/fix-language-count.py   # Oct 16: translations that said four languages where English says five (i18n memory + built pages)
python3 scripts/build-learn-standards.py  # Oct 16: NGSS/CCSS/AP/IB chips + educationalAlignment on Learn pages and calculators, Learn hub filter
python3 scripts/build-search-page.py    # Oct 16: Search.html = centred search bar + floating example questions + credits only (all langs)
python3 scripts/build-langbanner.py      # Oct 16: language-suggestion banner (site.js + styles.css; localStorage only, never redirects)
python3 scripts/build-lcp.py            # Oct 16: preload the page-hero background WebP (fetchpriority=high) on shared-hero pages (all langs)
python3 scripts/r2-cards.py             # Oct 16: again after i18n-build so translated pages keep the card srcset
python3 scripts/build-af-images.py       # Oct 17: Amazing Facts responsive WebP srcset + lazy (all langs)
python3 scripts/defer-sitejs.py         # Oct 16: site.js loads with defer (skips pages whose inline scripts call window.sp*)
python3 scripts/build-critical.py       # Oct 16: critical CSS inline + async stylesheets (cached per template; run after every head-touching generator)
python3 scripts/build-hero-themes.py    # Oct 16: homepage hero weekly theme rotation (space W42 / earth video, ?hero=), all langs
python3 scripts/si-credits.py --check        # Oct 15: visible SI credit caption next to every SI-generated image (all langs)
python3 scripts/seo-fix.py               # Oct 16 SEO pass: late pass after every page generator (titles/descriptions + i18n/seo-meta.json overrides, hreflang, OG/Twitter, JSON-LD) in all 5 langs
python3 scripts/add-video-schema.py       # Oct 16: again after seo-fix, so VideoObject descriptions match the final meta descriptions
python3 scripts/build-og.py             # Oct 15 item 7: distinct 1200x630 share card per page per language (assets/og/), SI credit on the card when the photo is SI
python3 scripts/seo-jsonld.py             # Oct 16: re-sync JSON-LD image/description after build-og bumps og:image ?v=
python3 scripts/i18n-sitemap.py           # Oct 16: sitemap.xml rebuilt from the pages on disk (all langs, hreflang alternates, git lastmod)
python3 scripts/seo-lint.py --no-fail | tail -6   # gap counts (strict run at the end)
# Search (Oct 12): rebuild the committed Pagefind + semantic indexes from the final HTML (both layers in one step).
node scripts/build-search.mjs
# Oct 16: SI Helper pilot retrieval index (Workers AI bge-m3 -> Vectorize si-helper-site). Incremental; only runs on the box
# where the Cloudflare token file exists; never fails the sync.
if [ -f /home/box/.cloudflare_token ]; then python3 scripts/si-index.py || echo 'si-index: failed (non-fatal)'; fi
# IndexNow (Oct 14): pages are not live yet at this point. After committing + pushing, run
#   bash scripts/post-deploy.sh   (waits for the live key file, pings changed URLs, never fails the sync)
# With WEEKLY_SYNC_POST_DEPLOY=1 the caller has already pushed, so ping now.
if [ "${WEEKLY_SYNC_POST_DEPLOY:-0}" = 1 ]; then bash scripts/post-deploy.sh || true; fi
# Oct 16 SEO lint (strict): fails the sync on missing/duplicate titles or descriptions, broken hreflang reciprocity or invalid JSON-LD.
python3 scripts/seo-lint.py > /tmp/seo-lint.log || { tail -12 /tmp/seo-lint.log; echo 'seo-lint: ERRORS (see python3 scripts/seo-lint.py --list)'; exit 1; }
