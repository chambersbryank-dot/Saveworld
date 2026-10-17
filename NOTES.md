# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

> Working file for Chief of Staff + Grok only. Keep lean: last 24h, next/open, reference. Long detail goes in docs/ and gets a one-line link.
> Archives: full history to Oct 12 midday → docs/notes-archive-2026-10-12.md (restored; 8987d81 had wiped NOTES to 28 bytes). Search/IA/hero detail + test tables → docs/search-and-ia-notes.md. Discovery research → docs/organic-discovery-plan.md.

## Last 24h (Oct 12–14 HST)
- **5 solution pages** (Oct 14, owner "Add all new solutions"): Coral_Gardeners, Project_Seagrass (Ocean); FreshWater_Watch (Rivers); Rewilding_Europe (Forests); Globe_at_Night (Space; NSF NOIRLab program, citizen science only, no donate). en/fr/es/ar, ELI10 in eli10.json, hub cards, Ways_to_Help rows (Globe at Night in citizen-science table), sitemap EN entries. Count 113 -> 118. Images: NASA public domain (STS093-717-066, KSC-20230329-PH-KLS01_0304, GSFC Danube Delta, iss074e0149572); FreshWater Watch reuses Mississippi PIA23534. All figures labeled organization/program figures.
- **12 solution pages** (Oct 13, approved A–L): Klamath_River_Dam_Removal, Elwha_River_Restoration, Living_Lands_and_Waters, American_Rivers (Rivers); Lake_Erie_Algal_Bloom_Forecast, Alliance_for_the_Great_Lakes_Adopt_a_Beach (Lakes); Global_Forest_Watch, Rainforest_Connection, One_Tree_Planted (Forests); Global_Fishing_Watch (Ocean); TEMPO (EO); Zero_Debris_Charter (Space Disposal). en/fr/es/ar, ELI10 overrides in assets/data/eli10.json, +6 glossary terms, 7 orgs + TEMPO on Ways_to_Help. Generator: page data kept in commit msg/diff. Note: weekly-sync exits 1 at i18n-check (pre-existing missing strings) so build-search must be run by hand after it.
- **16 more solution pages** (Oct 13, approved A–Q; I merged): BepiColombo, Psyche, EnVision, SPHEREx, Veggie_Space_Garden (Project Rawane); Hayabusa2_Torifune, Lucy, Comet_Interceptor (Planetary Defense); Sentinel-4, SARSAT (EO); Coral_IVF, Posidonia_Meadows, Whales_Ocean_Gardeners (Ocean); Justdiggit, Great_Green_Wall (Forests); River_Cleanup (Rivers). CyAN merged into Lake_Erie_Algal_Bloom_Forecast. Ways_to_Help: +Justdiggit, River Cleanup, Great Barrier Reef Foundation; NASA citizen table +Psyche, Lucy, SPHEREx, Veggie, SARSAT. GGW: no donate, UNCCD link only (AU page 404); figure corrected ~20M → ~4M ha in zone / ~18M wider (UNCCD 2020). SARSAT: 50,000+ rescues; one neutral line on 1979 co-founders incl. Russia (then USSR). Mission widgets for A–H not built.
- **Search** (1cfa5c1 → 31aaba1): Pagefind keyword + in-browser semantic (bge-small-en) on Search.html; hero "Search Saving Planets" over ocean/Earth/nebula bg; results only on Enter, top 5 + Show more + refine hint; 12 floating best-practice questions (search/featured-questions.json — never label "popular"); `?q=` deep links; key-term retry for 0-hit long queries; newsletter block off on Search only; 2-line credits (d3c8ef3); GA4 `search` event.
- **Solutions.html** directory (7da53ce, 3e39335, 093f635, 9b57735): hubs A–Z, 84 cards, search bar filters cards, (Top) links, left-aligned hub titles + synopsis/impact/links per hub; long nav dropdown removed (plain "Solutions" link).
- **Batch B** (08273c6): ELI10 boxes, Glossary (27 terms) + tap definitions, homepage Start Here row, Cite This Page, teacher print sheets + Teachers.html.
- **Batch A** (3322291, 5f996c5): share bars (96 pages), Last reviewed + sources count, 4 Related Solutions, "what makes us different" strip (home + About), videos compressed (ad 36→17 MB, GRACE-FO 19→8 MB), removed savingplanets-ad.mp4 + channel-intro.
- **Contacts**: media@savingplanets.com (Press), partners@savingplanets.com (About#partner), new Contact cards; hello@/ideas@ kept.
- **Ad v2** posted via Postiz (X/TikTok/YouTube) + featured on About; GA4 G-M5L2259Z68 on every page (Consent Mode v2).
- **SEO** (fc2a4f5, 46117d7): JSON-LD via scripts/seo-jsonld.py (Article+citations on solutions, CollectionPage hubs, Org+WebSite SearchAction, DefinedTermSet, LearningResource; no person names); robots.txt with Sitemap + disallows.
- **Organic discovery plan** (0dffe5a): docs/organic-discovery-plan.md. Tech SEO is sufficient; missing = verification + IndexNow wiring.
- Site review: distinctive combination, not "the only one" — claim the combination, never uniqueness.
- **Video hook (Oct 13, owner voice session):** Thank-you/updates video (education features, 22 new updates) opens with "We heard your feedback, and we took action." Captions on, no text overlay, so viewers see the new education features. Recycle existing clips, no new footage. Target ~30s, tonight or this week. Chief of Staff drafts script when owner is ready.
- **Tsunami_Early_Warning** (Oct 13, ACTIVE per Oct 13 approvals): EO hub + Ocean (Also in), en/fr/es/ar. Covers what a tsunami is, DART (39-station network 2008, 15 s, ~1 cm, GOES/Iridium), SWOT Kamchatka (Science 2026 Sepúlveda; Seismic Record Ruiz-Angulo ~400 vs ~300 km; Titov quote), GUARDIAN (350+ stations, 1,200 km, ≥20 min, 30–40 min before Hawaii, 580 mph, Moore quote, Scout), DAS cable (arXiv preprint), Med buoys (Sonardyne/INGV), BMKG Aceh HF radar, USGS GNSS-A Cascadia, Sentinel-6; NOAA safety; required caveat box near top. Horizon notes: SWOT ops, GUARDIAN, cables. Corrected: GUARDIAN 8 min→20 min, 30–45→30–40 min. Dropped: GREAT v1.0 (no primary source), Med buoy "Oct 2026" date (not on Sonardyne page), current DART count. Image NASA/JPL PIA26652. Follow-up: Related Solutions are auto (SARSAT, GRACE-FO, SOLAR-1, Sentinel-1); SWOT/Sentinel-6B/DSCOVR linked in Next + Explore.
- Tsunami polish (Oct 13): intro line, 4-step warning list, detection regrouped (buoys → coast/seafloor → satellites → horizon), Five W's moved below safety/people; Related Solutions now hand-set via assets/data/related-overrides.json (build-batch-a.py honors it, survives weekly sync).

## Next / Open
**Next priorities (after current builds)**
- (a) Interactive data visualizations: embed real climate data tools (PhET / Fluid Earth style) on Amazing Facts or the Earth Observation hub.
- (b) Adaptive learning paths branching deeper by age (kids / teens / adults), beyond the Start Here row.
- (c) Eco-anxiety support content after heavy topics, with "what you can actually do" reassurance.
- (d) Choose-your-own-adventure action guide tied to Ways_to_Help, branching by role (citizen, investor, professional, consumer, role model).

**User to-dos**
- [ ] YouTube Studio: "Altered or synthetic content" = Yes on ad v2 + older SI videos (Life Terra, GRACE-FO, earlier); Postiz can't set it.
- [ ] Pin comment "Every fact and source at savingplanets.com 🌍" on YouTube + TikTok uploads.
- [ ] Awards: CSS Design Awards ($50), Awwwards ($65), Indie Hackers (free); kit /workspace/awards_kit.md.
- [ ] GA4: register `search_term` custom dimension (Admin > Custom definitions) to see search report.
- [ ] Optional: swap .github/workflows/static.yml for docs/static-with-search.yml.txt (token lacks workflow scope) → indexes build per deploy.
- [ ] Old GA ID G-M5L2259Z68: removed from site; decide whether to delete that property.
- [ ] Partner With Us: supply real, verified audience stats (none shown until then).
- [ ] Google Search Console (Cloudflare DNS TXT) + submit sitemap; Bing Webmaster (import from GSC); Cloudflare Crawler Hints; Brave submit; then OER Commons, Curlie (EN/FR/ES/AR), TES/Procomún. Rich Results Test on solution/hub/Glossary/home/an /ar/ page.
- [ ] Grok Plus 9:16 setting still yields wide video; optional Artemis video remake ("Artegs III"); 4 ad clips from /workspace/grok-ad-savingplanets.txt.
- [ ] MailerLite double-opt-in confirmation texts: manual edit in dashboard (scripts/newsletter-confirmation-texts.md).
- [ ] Human-SI collab awards (draft /workspace/awards/human-si-collaboration-writeup.md): Fast Company World Changing Ideas (early Nov 13 / final Dec 11, 2026, $345/$445); Telly (early Dec 11, unconfirmed); A' Design late Feb 28, 2027 (unconfirmed); Internationalist AI for Better Marketing (May 7, 2027, $495); Anthem (opens Spring 2027); NI Prize 2026 closed, watch 2027.

**Open decisions**
- Merge Related Solutions with "Next: Explore Another Solution" (two "more" lists now).
- Homepage "minus the doom" appears in strip and headline — shorten one.
- Rewrite ELI10 in truly simple language (assets/data/eli10.json overrides) for most-visited pages.
- Hub/solution pages lacking "How This Saves People & the Planet" section — add when touched (people+nature rule).
- Real photos for the 3 lake cleanup cards (currently site logo).
- Multilingual semantic model (e.g. multilingual-e5-small) so fr/es/ar get meaning search; also DSCOVR misses top 12 for sea-level query.
- IndexNow: key file exists; wire `node scripts/indexnow-ping.js --send` into post-deploy (proposal).

**Follow-ups**
- Newsletter "What's New with Saving Planets" section in next Monday's issue (only live features).
- Daily 6:17 AM HST solution-candidate run → owner approves yes/no before anything is built.
- Glossary: add terms as pages grow. Stash `stash@{0}` (pre-Roman, Oct 12) in shared clone still unreviewed.

## Reference
**Content rules (standing)**
- Say "SI" not "AI" in owner-facing/site copy. Credits: "Made from SI and Biological SI Partner" / "SI-generated … by Saving Planets"; owner alias = "SI Partner". **Never write the owner's real name** anywhere (repo, site, newsletter, JSON-LD — Organization author only).
- People + nature rule: every solution page ties to saving planets for BOTH people and nature: `<section class="impact saves-planets" id="saves">` "How This Saves People & the Planet" after Impact Statement, h3 "For People"/"For Nature", sourced claims + fact-source lines.
- Horizon rule: unconfirmed contract/funding ⇒ "Potential solution on the horizon" badge + note "This is a potential solution [ORG] is advancing. We expect to know more within [TIMEFRAME] and will keep you updated here." (`.horizon-note` data-org/data-timeframe/data-next-milestone; `sp:status` horizon; never summed into totals; never invent dates).
- Sourcing: only cited, checkable figures; label company/nonprofit figures as such. Amazing Facts: `p.amazing-fact` with data-source, else skipped.
- Bottom-link rule: one `section.donate-banner.bottom-link#bottom-link` per content page (Donate → Join the work → "For further information").
- Ways to Help: EN Solution column Title Case (FR/ES sentence case); nothing non-link may look underlined. Never run /workspace/build_wth.py.
- Logos: none (agency logos need permission); use wordmark badges. Partner page: no sponsor influence, "Sponsored" labels, no China/Russia-state sponsors, no audience numbers until verified.
- Translations machine-quality (Arabic = MSA, RTL); keep numbers/names/URLs exact.
- Video: 9:16 1080x1920, H.264 High yuv420p +faststart; SI-generated visuals; rising www.savingplanets.com end card; AI label on TikTok (video_made_with_ai), YouTube public/not for kids; X strips domains → end "Follow @SISavingPlanets, link in bio".
- One canonical URL https://www.savingplanets.com; fallback chambersbryank-dot.github.io/Saveworld/.

**Pipeline**
- Deploy: .github/workflows/static.yml uploads repo root to GitHub Pages (static). Search indexes are committed.
- `scripts/weekly-sync.sh` order: build-roman.py → build-home-extras.py → build-batch2/3/4.py → build-solutions-index.py → build-batch-b.py → build-batch-a.py → add-gtag.py → i18n-build.py (runs seo-fix.py → seo-jsonld.py) → add-gtag.py → i18n-sitemap.py → build-batch-b.py --glossary → seo-audit.py → i18n-check.js → npm ci (if needed) → build-search.mjs. Expect: seo-audit TOTAL 0, "All translations current", 2 known JS-template linkcheck false positives.
- Older generators: `node build-search-index.js` → build-stats.js (solutions.json, nav/menus, lang switcher in PROJECT-R-MENU) + build-facts.js (Amazing_Facts). New solution = sp: meta tags + page-stats + sitemap entry, then rerun.
- i18n: i18n/<lang>.json translation memory, i18n/pages.txt list, `i18n-build.py --missing fr|es|ar`, i18n-check.js hashes (`i18n-source` meta). Artemis data: update-artemis.js → i18n-data.py.
- Search: `npm ci && node scripts/build-search.mjs` → /pagefind/ (4 langs) + /search/semantic-index.json + semantic-vectors.bin + hubs.json. search/semantic.js is the swappable module (contract: supports/load/search). search-ui.js fuses RRF.
- Data files: assets/data/{solutions,reviewed,eli10,glossary,roman,artemis*,daily-actions,community,new-callout}.json; scripts/batch3-content.py (myths, mission log, quizzes); scripts/newsletter-corrections.json.
- Newsletter: MailerLite acct 2704021, key /home/box/.mailerlite_key; `node scripts/newsletter-draft.js [--update]` creates DRAFTS only (never send/schedule); groups EN 201062857381512972, FR …692939304, ES …966617859, AR …265462233; language_id en4 fr6 es8 ar23.
- GA4 G-M5L2259Z68 (Consent Mode v2, add-gtag.py). IndexNow key aa19429b4f58f36d34c263abe996de09.txt.
- Postiz: post via `integrationList` (X, TikTok, YouTube are connected); YouTube category + altered-content flags not exposed. IDs: X cmv4dud7z1utemq0y74sa8177, TikTok cmv4dwne61uxdmq0ykvftgylr (DIRECT_POST, video_made_with_ai true), YouTube cmv4dv4qy1urrqz0y6xnd3d4y.
- Cloudflare: www grey-cloud CNAME → chambersbryank-dot.github.io, apex A 185.199.108-111.153, HTTPS enforced (cert to 2027-01-08); saveplanetminusthedoom.com → savingplanets.com redirect (Oct 12).
- Cache-bust `?v=YYYYMMDDx` on styles.css/site.js when CSS/JS changes.

**Gotchas**
- NEVER edit via GitHub connector create_or_update_file (truncated NOTES/styles.css; decodes HTML entities). Use git clone + push, `pull --rebase`.
- `git add -u` or explicit paths, never `-A` (shared box clone has other workers' scratch files).
- Launch Library: use /2.3.0/ (2.2.0 404s). Use curl with browser UA when WebFetch times out (nasa.gov).
- Concurrent workers: on heavy generated-file conflicts, reset to origin/main and re-run generators instead of rebasing.

## Candidate Queue (append-only; older batches 10-09..10-12 in docs/notes-archive-2026-10-12.md, all built)
**Batch 2026-10-13** (17, 6:17 AM run). Nothing built; awaiting owner yes/no. No repeats vs pages, solutions.json, prior queues. Org figures labeled as org figures.
| ID | Candidate | Hub | Widget | Status |
|---|---|---|---|---|
| A | BepiColombo arrives at Mercury (ESA/JAXA; orbit 21 Nov 2026, split 9-10 Dec, science Apr 2027) | Project Rawane | Yes | BUILT |
| B | Hayabusa2# Torifune flyby (JAXA; 5 Jul 2026, ~400 m from surface, record) | Planetary Defense | Yes, Earth swing-by Dec 2027 | BUILT |
| C | Psyche (NASA; launched 13 Oct 2023, Mars flyby 15 May 2026, arrives Aug 2029) | Project Rawane | Yes | BUILT |
| D | Lucy (NASA; 11 asteroids, Eurybates 11 Aug 2027) | Project Rawane / Planetary Defense | Yes | BUILT |
| E | Comet Interceptor (ESA+JAXA; launch late 2028/early 2029) | Planetary Defense | Yes | BUILT |
| F | EnVision (ESA Venus; launch Nov 2031) | Project Rawane | Yes | BUILT |
| G | SPHEREx (NASA; launched 11 Mar 2025, all-sky ice maps) | Project Rawane | Yes, active | BUILT |
| H | Sentinel-4 on MTG-S1 (ESA/EUMETSAT, GEO hourly air quality) | Earth Observation | Yes, active | BUILT |
| I | CyAN satellite algae watch, 2,000+ US lakes (EPA/NASA/NOAA/USGS/USACE) | Lakes + Earth Observation | No | MERGED into Lake_Erie_Algal_Bloom_Forecast |
| J | SARSAT search-and-rescue satellites incl. MEOSAR (NOAA/NASA/USCG/DAF) | Earth Observation | No | BUILT (SARSAT.html; flag for integrity rules: Cospas-Sarsat co-founded 1979 by Russia/USSR with Canada, France, US; one neutral sentence; 50,000+ used) |
| K | Coral IVF, Great Barrier Reef (GBRF + RRAP) | Oceans | Spawning Oct/Nov | BUILT |
| L | Posidonia oceanica meadows (natural, Balearics/Spain; peer-reviewed) | Oceans (x-link Seagrass) | No | BUILT |
| M | Whales as ocean gardeners (natural; NOAA Fisheries) | Oceans (x-link Phytoplankton) | No | BUILT |
| N | Justdiggit (nonprofit; Kenya, Tanzania, Senegal; 525,000 ha) | Forests | No | BUILT |
| O | River Cleanup (nonprofit; 4,397,462 kg, 1,000 rivers by 2050) | Rivers | No | BUILT |
| P | Great Green Wall (African Union, UNCCD; ~20M ha restored 2007-18) | Forests | No | BUILT (Great_Green_Wall.html; no donate, UNCCD link; 20M ha softened to ~4M in zone / ~18M wider) |
| Q | Veggie space garden (NASA ISS) | Project Rawane (x-link ISS_Water_Recovery) | No | BUILT |
Dropped 10-13: JPSS/NOAA-21 (too few confirmed facts), ozone recovery (already a Myth vs Fact card), The Rivers Trust UK (no figures on impact page), Hayabusa2 1998 KY26 arrival date and Comet Interceptor L2 parking (not on pages read).
Sources: esa.int BepiColombo + Latest_updates_BepiColombo_s_arrival_at_Mercury; global.jaxa.jp/press/2026/07/20260730-1_e.html, -2_e.html, 20260706-3_e.html; hayabusa2.jaxa.jp press PDF 20260706; science.nasa.gov/mission/{psyche,lucy,spherex}/; esa.int Comet_Interceptor, EnVision, Copernicus/Sentinel-4; epa.gov/water-research/cyanobacteria-assessment-network-cyan (+ -application-cyan-app); sarsat.noaa.gov; barrierreef.org/news/explainers/what-is-coral-ivf + GBRF Year in Review 2023-24 PDF; gbrrestoration.org RRAP-MC-01 final report 2025; doi.org/10.1002/lno.10510; doi.org/10.1371/journal.pone.0030454; pubmed 33360312; fisheries.noaa.gov/feature-story/whales-and-carbon-sequestration-can-whales-store-carbon; justdiggit.org/what-we-do/impact/ + water-bunds; river-cleanup.org/en; unccd.int GGWI page + 2020 status report press release; nasa.gov growing-plants-in-space + Veggie activation (2014).

**Batch 2026-10-15** (17, ~6:38 AM HST run). Owner approved all 17 (Oct 16); all BUILT in 5 languages (EN/FR/ES/AR/IT), live; 142 solutions total. No new solution pages vs existing *.html; Dragonfly already has a mission widget on Titan.html (flagged). Org figures labeled as org figures. Spot-checked ESA Sentinel-3 (3C 15 Sep 2026) and HydroGNSS (science ops / open data 31 Jul 2026).
| ID | Candidate | Hub | Widget | Status |
|---|---|---|---|---|
| A | NASA EMIT (ISS spectrometer; methane/CO₂ plumes + mineral dust) | Earth Observation | Yes, extended ≥2026 | BUILT (29b1c1fa) |
| B | NASA GEDI (ISS lidar; forest canopy / carbon) | Forests (+ EO) | Yes, ops post-2024 reinstall | BUILT (29b1c1fa) |
| C | NASA OCO-2 (global CO₂; Caltech ops partnership 2026) | Earth Observation | Yes, active (+ OCO-3 note) | BUILT (29b1c1fa) |
| D | ESA Sentinel-5P / TROPOMI (daily air quality + CH₄) | Earth Observation | Yes, operational | BUILT (29b1c1fa) |
| E | NASA PREFIRE (polar far-IR CubeSats; extended through Sep 2026) | Earth Observation | Yes | BUILT (29b1c1fa) |
| F | ESA HydroGNSS (Scout GNSS-R soil moisture/wetlands; open data 31 Jul 2026) | Earth Observation (+ Rivers/Lakes) | Yes | BUILT (29b1c1fa) |
| G | ESA Sentinel-3 A/B/C (ocean/land/ice; 3C launched 15 Sep 2026) | Earth Observation | Yes, 3C commissioning | BUILT (29b1c1fa) |
| H | NASA Libera (Earth radiation budget on JPSS-4; LRD ~2027) | Earth Observation | Yes, horizon to launch | BUILT (29b1c1fa) |
| I | Surfrider Foundation (beach cleanups + plastic policy) | Oceans | No | BUILT (29b1c1fa) |
| J | Heal the Bay (Santa Monica Bay / LA County) | Oceans | No | BUILT (29b1c1fa) |
| K | Plastic Odyssey (containerized recycling factories) | Oceans | No | BUILT (29b1c1fa) |
| L | Trout Unlimited (coldwater river restore/reconnect) | Rivers | No | BUILT (a1531746) |
| M | Chesapeake Bay Foundation (oysters, trees, living shorelines) | Rivers (+ estuaries) | No | BUILT (29b1c1fa) |
| N | League to Save Lake Tahoe / Keep Tahoe Blue | Lakes | No | BUILT (29b1c1fa; page Keep_Tahoe_Blue.html) |
| O | American Forests (Tree Equity + U.S. reforestation) | Forests | No | BUILT (29b1c1fa) |
| P | Plant-for-the-Planet (youth restoration + platform) | Forests | No | BUILT (29b1c1fa) |
| Q | NASA Dragonfly (Titan rotorcraft; launch ~Jul 2028) | Project Rawane | Yes | BUILT (29b1c1fa; Dragonfly.html cross-linked with Titan.html widget) |
Dropped 10-15: MethaneSAT (lost 2025); Oceana / International Rivers / Blue Marine (advocacy-heavy); SECORE (overlaps Coral IVF/CRF/Gardeners); Kelp Blue (weak totals + Kelp_Forests exists); Rainforest Trust / Trillion Trees / Restor / Canopy / Wetlands International / Restore America’s Estuaries (funders/networks); FORUM / CHIME / LSTM / ROSE-L / CRISTAL (later EO); VERITAS / DAVINCI / Ariel (thin near-term Earth hook); Destiny+ (Apophis overlaps Ramses).
Sources: earthdata.nasa.gov EMIT/GEDI/OCO-3; nasa.gov OCO-2 launch + PREFIRE + Libera + Dragonfly; science.nasa.gov OCO-2 blog 2026-08-24, Libera test blog, Dragonfly; ocov2.jpl.nasa.gov; earth.jpl.nasa.gov/emit; gedi.umd.edu; esa.int Sentinel-5P, Sentinel-3, HydroGNSS (+ data-open 31 Jul 2026); dataspace.copernicus.eu Sentinel-5P; tropomi.eu methane; prefire.ssec.wisc.edu; nesdis.noaa.gov Libera; surfrider.org 2025 Beach Cleanup Report PDF + plastic initiative; healthebay.org CCD 2025/2026 wrap-ups; factories.plasticodyssey.com + plasticodyssey.org SUNU; tu.org 2024-25 Annual Report PDF; cbf.org FY26 impact report PDF + restoration; keeptahoeblue.org science-to-solutions + July 5 cleanup news + BEBOT StoryMap; americanforests.org + Tree Equity Score; plant-for-the-planet.org + trilliontreecampaign.org.

## Oct 13 approvals (owner voice session)
1. Merge Related Solutions + "Next: Explore Another Solution" into one more-list.
2. Homepage "minus the doom": keep it in only the strip or only the headline, not both.
3. Rewrite ELI10 boxes in truly simple language, starting with most-visited pages.
4. Add "How This Saves People & the Planet" to hub/solution pages lacking it, when touched.
5. Tsunami early-warning page is now ACTIVE (off hold); to be built.

## Oct 13 fixes
- scripts/build-site-extras.py (weekly-sync, after batch-b): footer site map + Sitemap.html, <main> landmark, video labels, extras.css (contrast). axe: 295 -> ~4 issues on 18 sampled pages.
- Lake pages use public-domain NASA/NPS photos; Solutions lists each solution once (primary hub = breadcrumb) with "Also in"; About sources are a plain list.
- Daily sync (Oct 13, 7:06 AM run, 5e3f2b8): first pass left 339 translations stale (English solution pages change after i18n-build hashes them, so i18n-check fails and build-search never runs). Fix: rerun i18n-build → add-gtag → i18n-sitemap → batch-b --glossary, then build-search. Proposal: add that second pass to weekly-sync.sh. seo-audit TOTAL 49 (was 113 on main): 36 English img alts on fr/es/ar, 12 missing breadcrumbs on Glossary/Sitemap/Teachers (×4 langs), ar/Sitemap description 114 chars.

- Daily sync (Oct 16, ~7:00 AM HST, 4ea31130): weekly-sync.sh exit 0; All translations current; SOTW Great_Bubble_Barrier; Roman 1496564 km; solutions.json 142 active; map 166 green / 14 blue pins, 12 no-pin; pagefind 888 pages (5 langs); seo-audit TOTAL 1219 (was 1237 on main; title-length 9, twitter-missing 36). FIX: build-og now sets og:image to assets/og/<lang>/<page>.jpg share cards, so apply-heroes' og:image fallback dropped 39 pages' photo heroes (e.g. Great_Bubble_Barrier, Coral_IVF); apply-heroes now keeps the hero already in styles.css when og:image is a share card (0 warnings).
- Daily sync (Oct 15, ~6:55 AM HST): weekly-sync.sh exit 0; All translations current; SOTW Great_Bubble_Barrier; Roman 1494325 km; fr/es/ar/it 157 pages each; pagefind 788 pages (5 langs); solutions.json 125; seo-audit TOTAL 1066 (title-length 2, twitter-missing 36).
- Daily sync FIXED (Oct 14, 85524bfc): i18n-check now runs right after i18n-build in weekly-sync.sh (later all-language post-processors edit English and always read as stale); i18n-build runs seo-fix on English before hashing; JSON-LD and RELATED blocks ignored in i18n hashes (py + js). Full sync exits 0.
- Solution candidates 10/14: CO2M (Earth Observation) and Mission Blue Hope Spots (Oceans) approved and BUILT (3fefc99b), 120 solutions.

## Oct 16 request: Education expansion + orbital mechanics + aerospace track (SCOPE ONLY, nothing built)
Owner request (11:38 AM HST, + 11:39 addition): expand education beyond kids to community college, university and graduate; teachers stay top priority.
Components: (1) plain-language orbital mechanics guide; (2) interactive delta-v / Hohmann transfer tool (real vis-viva, animated); (3) leveled math help guide
(vis-viva, Kepler, Hohmann, rocket equation, plane changes; K-12 to grad); (4) aerospace/aeronautical engineering track for college students (fighter-jet and
helicopter design aims): aerodynamics, propulsion, performance, stability & control, structures/materials, rotorcraft. Public/unclassified material only, no export-controlled details.

**Levels** (badge on every section): Kids (K-5), Teens (6-12), College (community college / first two years), University (upper division), Graduate.

**Pages (EN + fr/es/ar/it via the generators; new generator scripts/build-learn.py; equations rendered with KaTeX, MIT licence, self-hosted under assets/vendor/katex/, MathML output for screen readers)**
| File | What | Effort |
|---|---|---|
| Learn.html | "Learn" hub: pick a level, then a topic (orbits, rockets, flight, helicopters); the teacher path is first | S |
| Orbits_Guide.html | Plain-language orbital mechanics: what an orbit is, why things stay up, LEO/GEO, transfers, plane changes; ELI10 box per section, then "go deeper" per level | M |
| Orbit_Lab.html + assets/orbit-lab.js | Interactive tool: choose a body (Earth default), starting circular orbit (altitude), enter a delta-v (or a target altitude). It computes the Hohmann burns with vis-viva v^2 = mu(2/r - 1/a), shows the transfer ellipse and an animated rocket on canvas/SVG, total delta-v, transfer time (half the ellipse period), and says plainly when the delta-v is not enough or reaches escape. Static JS (no build step, no libraries except KaTeX); keyboard controls, live text readout (aria-live), table alternative to the animation, reduced-motion still frames, RTL layout for Arabic, numbers via Intl.NumberFormat. Constants from JPL SSD (mu, radii), cited on the page. Unit-tested against textbook cases (LEO 300 km to GEO, about 3.9 km/s total). | M-L (about 2-3 days) |
| Orbit_Math.html | Math guide, leveled: Kepler's 3 laws, vis-viva, circular and escape speed, Hohmann delta-v, Tsiolkovsky rocket equation, plane-change delta-v = 2v sin(di/2), with worked examples and "check your answer" boxes | M |
| Aero_Track.html | Aerospace engineering track hub, freshman to senior: course map and links | S |
| Aero_Aerodynamics.html | Lift/drag equations, Bernoulli, airfoils and thin-airfoil theory (Cl = 2*pi*alpha), compressible flow, Mach and normal/oblique shocks (textbook relations only) | M |
| Aero_Propulsion.html | Brayton cycle, thrust equation, specific fuel consumption, turbojet/turbofan/afterburner principles (public textbook level, no specific engine data) | M |
| Aero_Performance_Stability.html | Flight performance (range/Breguet, climb, turn), static stability, control-surface basics | M |
| Aero_Structures.html | Loads, stress and strain, beam bending, material families (aluminium, titanium, composites) at textbook level | S-M |
| Rotorcraft.html | Momentum theory (hover induced velocity, figure of merit), blade element theory, autorotation; FAA Helicopter Flying Handbook as the plain-language companion | M |
| Teacher kits | Each page gets a teacher box: NGSS/CCSS where they really apply (HS-PS2-4 gravitation, HS-ESS1-4 orbits already in standards.json), printable handout and Lesson Builder seeds | S each |

**Ties into existing pages**: Teachers.html (new "Orbits & Flight" browse chip + teacher kits), Lesson_Builder.html (new topics with standards and slides), Satellite_Explorer.html ("now fly it" link to Orbit_Lab), Play_and_Learn.html (Orbit Lab tile, kid mode), Glossary.html (new terms), Project-Rawane / Space pages (real missions as worked examples: Hohmann-like transfers), World_Map untouched. Nav: Kids & Teachers door gains "Learn (all levels)". standards.json gets the new pages.

**Estimate**: orbital part (Learn, Orbits_Guide, Orbit_Lab, Orbit_Math) about 5-7 working sessions incl. 5 languages; aerospace track (6 pages) about 6-8 sessions. Translation of equations is cheap (math is shared); prose follows the existing i18n flow. Feasibility of the tool as a static GitHub Pages JS page: high (vis-viva and Kepler are closed-form; no server).

**Verified free resources (checked Oct 16 2026; link out, do not copy unless the licence allows)**
- NASA Basics of Space Flight: https://science.nasa.gov/learn/basics-of-space-flight/ (US gov, public)
- MIT OCW 16.346 Astrodynamics (Battin): https://ocw.mit.edu/courses/16-346-astrodynamics-fall-2008/ (CC BY-NC-SA 4.0)
- Orbital Mechanics & Astrodynamics open textbook: https://orbital-mechanics.space/ (licence to confirm before reuse)
- PhET Gravity and Orbits: https://phet.colorado.edu/en/simulations/gravity-and-orbits ; Kepler's Laws: https://phet.colorado.edu/en/simulations/keplers-laws (PhET page links CC BY-NC 4.0 and GPL 2.0; link out, confirm per sim before embedding)
- OpenStax University Physics Vol 1, ch. 13 Gravitation: https://openstax.org/books/university-physics-volume-1/pages/13-introduction (page shows CC BY-NC-SA 4.0; confirm)
- NASA Eyes on the Solar System: https://eyes.nasa.gov/ ; NASA Space Place (kids): https://spaceplace.nasa.gov/
- JPL SSD planetary constants: https://ssd.jpl.nasa.gov/planets/phys_par.html
- Kerbal Space Program wiki, Basic Orbiting (Math): https://wiki.kerbalspaceprogram.com/wiki/Tutorial:Basic_Orbiting_(Math) (game wiki, link only)
- Bate, Mueller, White, Fundamentals of Astrodynamics (Dover, copyrighted book, cite/link only): https://store.doverpublications.com/products/9780486497044
- Curtis, Orbital Mechanics for Engineering Students (Elsevier, copyrighted; no official open notes found, cite only)
- ESA Education: https://www.esa.int/Education
- NASA Glenn Beginner's Guide to Aeronautics: https://www.grc.nasa.gov/www/k-12/airplane/ (and bga.html); Beginner's Guide to Rockets: https://www.grc.nasa.gov/www/k-12/rocket/
- MIT OCW 16.100 Aerodynamics: https://ocw.mit.edu/courses/16-100-aerodynamics-fall-2005/ ; 16.01-04 Unified Engineering: https://ocw.mit.edu/courses/16-01-unified-engineering-i-ii-iii-iv-fall-2005-spring-2006/ ; 16.50 Propulsion Systems: https://ocw.mit.edu/courses/16-50-introduction-to-propulsion-systems-spring-2012/ ; 16.333 Aircraft Stability and Control: https://ocw.mit.edu/courses/16-333-aircraft-stability-and-control-fall-2004/ ; 16.07 Dynamics: https://ocw.mit.edu/courses/16-07-dynamics-fall-2009/ (OCW: CC BY-NC-SA)
- FAA Helicopter Flying Handbook: https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/helicopter_flying_handbook ; Pilot's Handbook of Aeronautical Knowledge: https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak ; Airplane Flying Handbook: https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/airplane_handbook (US gov, public)
- NASA Technical Reports Server: https://ntrs.nasa.gov/ (public reports)
- AIAA students: https://www.aiaa.org/get-involved/students-educators (blocks automated checks, 403; verify in a browser)
- KaTeX: https://katex.org/ (MIT licence)
Not used: braeunig.us orbital mechanics page (did not respond). Fighter-jet/helicopter content stays at public textbook level (equations, principles, FAA/NASA/OCW), no specific military aircraft performance, design or export-controlled data.

**Open decisions for the owner**
1. Level names and order (Kids / Teens / College / University / Graduate)? Include community college as its own level or merge with College?
2. Build order: orbital part first (recommended), then aerospace track?
3. Orbit Lab scope v1: Earth only, circular start orbits, coplanar Hohmann + altitude raise; later: Moon/Mars, plane change, bi-elliptic?
4. Equations via self-hosted KaTeX (recommended, works offline, about 300 KB) or native MathML only (no library, less consistent on iPad Safari)?
5. Translate full grad-level prose into fr/es/ar/it, or translate K-12/college sections fully and keep grad derivations in English with translated headings?
6. Fighter-jet / helicopter framing: generic "high-performance jet" and "rotorcraft" with textbook examples (recommended), or name public aircraft (F-16, F-35) only where public sources such as NASA or the manufacturers say so?
7. Credit for any SI-made diagrams ("Created by SI and Biological SI Partner") vs only NASA/public-domain images?
8. Add a "Learn" door to the nav, or keep it under Kids & Teachers?

## Brainstorm (ideas only, NOT committed to-dos)
- Press outreach (Oct 13): intro emails to news outlets introducing savingplanets.com (features, education content, EN/FR/ES/AR). Owner framing: out-of-the-box, speed-to-scale near a tipping point. Research only, no contact: target outlets (local Hawaii, national US, France/Spain/Arabic-speaking), contact best practices, one master email + language variants? Nothing sent.
- Human-SI awards as free advertising ("SI and its Biological SI Partner" team entry): covered by /workspace/awards/human-si-collaboration-writeup.md and the User to-dos line (6342867).
- Media + university pitch research (Oct 13, BRAINSTORM ONLY, nothing sent, no forms filled). Return address: media@savingplanets.com (existing Press contact).
  - CNN: tips form https://www.cnn.com/feedback/forms/form11b.html ; tips page https://www.cnn.com/tips/ (tips@cnn.com; says "not for press releases", wants newsworthy and corroborated). No public science/climate desk address found; pitch named reporters by beat instead.
  - MSNBC is now MS NOW (official Nov 15, 2025, AP: https://apnews.com/article/msnbc-ms-now-new-company-network-tv-a3813857af61282876ba847afa1c7ef9). Contact page https://www.ms.now/information/msnow-info/contact-us-n1301857 (feedback msnowinfo@ms.now; press msnowpress@ms.now). No public tips form found.
  - Fox News: tips form https://www.foxnews.com/tips (Fox News Digital, 1 attachment ≤25 MB); "Send a story idea or news tip" ticket https://help.foxnews.com/hc/en-us/requests/new?ticket_form_id=360000067394 ; hotline per https://help.foxnews.com/hc/en-us/articles/233193788-Does-FoxNews-com-have-a-news-hotline
  - Universities/OER: MERLOT add-a-material (free account, open URL) https://info.merlot.org/merlothelp/Add_a_Material.htm ; OER Commons (submit link, staff review) https://www.oercommons.org/ ; NAGT/SERC Teach the Earth site submission https://serc.carleton.edu/teachearth/contribute_site.html and activity submission https://serc.carleton.edu/teachearth/contribute_activity.html (peer reviewed; teacher sheets fit here). Also short notes to subject librarians (asking for LibGuide inclusion) and to earth-science/sustainability dept chairs and campus sustainability offices. Start with the University of Hawaii (UH Mānoa SOEST, Sea Grant). NSTA: no public submission route found.
  - Best practices (Cision 2025 State of the Media https://www.cision.com/resources/articles/how-to-pitch-journalists-media-approved-tips/ ; Muck Rack https://muckrack.com/resources/guides/media-pitching): email, one reporter at a time on their beat; 100–300 words; subject line under ~50–100 characters, factual and not hype ("urgent" and "groundbreaking" get rejected); one follow-up only, 2–3 days later, 8 AM–noon in their time zone; embargoes only for real news, agreed in advance, with exact date, time and zone.
  - Angles: (1) Hawaii/tsunami: how the Kamchatka M8.8 wave was tracked (DART, SWOT, GUARDIAN) explained for kids, timed to Hawaii news and the Oct 2026 PTWS meeting; (2) kid-level "Explain Like I'm 10" boxes plus free teacher sheets; (3) four languages (EN/FR/ES/AR) as a secondary differentiator. Lead with it for international, Arabic-language or Spanish-language outlets and for OER/ESL use, not as the US-network hook.
  - Draft subject idea: "Kid-friendly explainer: how the 2025 Pacific tsunami was tracked". Keep the no-exact-time/place caveat in any pitch.
- Outreach drafts (Oct 13): 15 Gmail drafts created, UNSENT (CNN, MS NOW, Fox tips, MERLOT, OER Commons, SERC, UH librarian, UH SOEST, FR/ES/AR outlets, EN/FR/ES/AR master intros). Pending owner: set Reply-To media@savingplanets.com and send-as Name 'Saving Planets' in Gmail (alias currently shows real name); add verified recipients.
- Outreach framing (owner, Oct 13): pure introduction, NO donation/membership asks. Lead with the tsunami early-warning hub + differentiators (education side, news side, teaching people worldwide one-on-one about satellites, tsunami alerts, how buoys work). Target list to expand and review together before anything sends: big international list incl. Spain, France, UK, Australia, Saudi Arabia (friendly Arab country), plus universities. Pre-send blockers on the 15 drafts (8d5c65c): reply-to media@savingplanets.com; From name must not show the owner's name, ideally send from media@savingplanets.com as a Send mail as alias. Nothing sent.

## Newsletter
<!-- Weekly Brief "What's New" feed. scripts/newsletter-updates-sync.js (run by scripts/weekly-sync.sh) appends to
     scripts/newsletter-updates.json from: (1) commits titled "feat(Page.html): reader-facing sentence" (or "feat: sentence"),
     and (2) bullets in this section formatted "- YYYY-MM-DD | Page.html | reader-facing sentence".
     Auto entries are English-only; add what.fr / what.es / what.ar in the JSON for translated issues (otherwise English shows). -->

## 2026-10-16 — Friday community outreach campaign (prepared, NOT sent)
- Contacts researched/verified against official sites: /workspace/outreach-community-1016/contacts.csv (26 rows).
- 23 drafts prepared (EN 15, FR 3, IT 3, ES 2) + AR master template, in /workspace/outreach-community-1016/drafts/. All linked pages checked live (200).
- Contact-form only: CNES, Agencia Espacial Española. Unverified: Australian Space Agency (media@space.gov.au; official page unreachable).
- Skipped as duplicates: JAXA, ISRO (already thanked in outreach-142).
- Awaiting owner approval before any send.

## 2026-10-16 — Learn hub math-layer benchmark research
Full spec also at /workspace/learn-benchmark-spec.md (box). Research only; no site pages edited.

## 1. Benchmark table
| Resource | What makes it exceptional | Wow-factor | Weaknesses / gaps we can beat |
|---|---|---|---|
| MIT OCW 16.07 Dynamics, 16.346 Astrodynamics, 16.100 Aerodynamics, 8.01SC, 18.03SC (ocw.mit.edu) | Real MIT rigor, full problem sets + solutions, lecture notes; "SC" scholar courses add sequenced sessions + recitation videos | Authenticity; complete problem/solution sets | Static PDFs, little interactivity, no intuition-first layer, English only, uneven accessibility (scanned PDFs, raw LaTeX images) |
| Khan Academy (khanacademy.org/science/physics) | Mastery learning, short videos, auto-graded practice with hints, multilingual | Instant feedback + step hints | Stops ~intro college; little aero/astro; no graduate depth |
| Paul's Online Math Notes (tutorial.math.lamar.edu) | Extremely clear step-by-step worked examples, every algebra step shown; notes/practice/assignment split | "Show every step" examples; hidden solutions | Pure math only, no applications, no visuals, English only |
| NASA Glenn Beginner's Guide to Aeronautics (grc.nasa.gov/www/k-12/airplane) | Authoritative, one-concept-per-page, equation pages + FoilSim/EngineSim interactives | Interactive simulators tied to equations | Dated UI, Java-era sims partly broken, shallow math beyond algebra, weak navigation |
| NASA Basics of Space Flight (science.nasa.gov/learn/basics-of-space-flight) | Plain-language JPL mission context, real spacecraft examples | Real-mission storytelling | Almost no equations or worked problems; no practice |
| ESA Education (esa.int/Education) | Teacher kits, classroom activities, multilingual European reach | Teacher-ready packs | Mostly school level; little university math |
| OpenStax University Physics (openstax.org) | Free peer-reviewed textbook, CC BY, worked "Strategy/Solution/Significance" examples, end-of-chapter problems, accessible HTML | Strategy→Solution→Significance example format | Static; no interactive solvers; no aero/astro specialization |
| 3Blue1Brown (3blue1brown.com) | Visual intuition first; animations reveal why | Geometric "aha" visuals | No practice, no worked engineering problems |
| Brilliant (brilliant.org) | Active learning: interact before being told; bite-size, gamified | Learn-by-doing puzzles | Paywalled, shallow at grad level, no citations |
| PhET (phet.colorado.edu) | Research-based HTML5 sims, accessible (keyboard, screen-reader descriptions, sonification), 90+ languages, teacher activities | Inclusive sims + translations | Intro physics only; no orbital transfers/aircraft dynamics |
| LibreTexts (phys.libretexts.org) | Huge open library, remixable, upper-division content | Breadth to grad level | Inconsistent quality/format, cluttered |
| Stanford AA, Caltech GALCIT, Purdue AAE, Georgia Tech AE | Define the canonical curriculum sequence (statics→dynamics→aero→propulsion→controls→astro; grad: viscous flow, optimal control, perturbation theory) | Curriculum map | Not public learning resources; behind enrollment |
| Curtis, *Orbital Mechanics for Engineering Students*; Vallado, *Fundamentals of Astrodynamics and Applications* (cite only) | Gold-standard derivations + algorithms (Kepler/Newton-Raphson, Lambert, Hohmann); Vallado has public code (celestrak.org/software/vallado-sw.php) | Algorithm-level worked examples | Paid texts; no interactivity; we cite, never copy |

## 2. Synthesis — top wow-factors to adopt
1. Intuition first, then rigor (3B1B/Brilliant): every topic opens with an interactive or visual before the equations.
2. Paul's-style fully shown steps + OpenStax "Strategy → Solution → Significance" framing.
3. Live calculators tied to the worked example (NASA Glenn/PhET): change inputs, watch numbers and animation update.
4. Auto-checked practice with progressive hints and hidden full solutions (Khan).
5. PhET-grade accessibility + true 5-language support (nobody does this at grad level).

## 3. Gaps we can beat
- No free resource spans freshman → PhD in one consistent format for astro/aero.
- Rigorous sources (OCW, Curtis, Vallado) lack interactivity; interactive ones (Khan, PhET, Brilliant) lack depth.
- Almost no aero/astro math is in FR/ES/IT/AR with RTL support.
- Few show code (Python) side-by-side with math; few cite sources per equation.
- Teacher packs exist for school level only — we add college-level instructor notes.

## 4. Page template (every topic page, in order)
1. Header: title, track, **level badge** (Kids/Teens/College/Graduate/PhD), est. time, last-verified date.
2. **Learning goals** (3–5 measurable "you will be able to…").
3. **Prerequisites** with links to our own lower-level pages + external (Khan/Paul's/OpenStax).
4. **Intuition first**: short plain-language story + interactive/visual; "Explain like I'm 10" box.
5. **Derivation**: numbered steps, each with a one-line "why"; collapsible for lower levels.
6. **Worked example on a real problem** — Given / Find / Strategy / Step-by-step / Answer with units / Sanity check / Significance. Plus a Python snippet toggle.
7. **Practice problems** (3–6, graded easy→hard): numeric answer box with tolerance check, progressive hints, hidden full step-by-step solution (`<details>`).
8. **Common mistakes** (degrees vs radians, km vs m, mean vs eccentric anomaly, sign conventions, etc.).
9. **Check your understanding**: 3 conceptual multiple-choice/explain questions with feedback.
10. **Go deeper**: next level page + grad/PhD extensions.
11. **For teachers**: objectives alignment, slide-ready figure, lesson time, answer key note.
12. **Cited sources**: per-equation citations (Curtis ch./Vallado algorithm number, OCW course, NASA page).

## 5. Flagship worked examples (verify numbers in build)
- **Kepler's equation via Newton-Raphson**: M = E − e sinE; E₀ = M (or π for e>0.8); E_{n+1} = E_n − (E_n − e sinE_n − M)/(1 − e cosE_n); stop |ΔE|<1e-10. Example e=0.37255, M=3.6029 rad (Curtis Ex. 3.2 style; cite, use own numbers). Show iteration table.
- **LEO→GEO Hohmann**: μ=398600.4418 km³/s², r1=6678 km (300 km alt), r2=42164 km; Δv1≈2.43 km/s, Δv2≈1.47 km/s, total ≈3.89 km/s (excl. plane change); TOF ≈5.28 h. Extension: combined 28.5° plane change at apogee (~4.2 km/s total to GEO).
- **Short-period aircraft stability**: 2-state [α, q] linear model, characteristic eq s² − (Z_α/V + M_q + M_α̇)s + (Z_α M_q/V − M_α) = 0; compute ω_n, ζ; compare to MIL-STD-1797 / FAA handling-quality ranges (generic high-performance jet; public data only).
- **Rotor momentum theory (hover)**: T = 2ρA v_i², v_i = √(T/2ρA), P_ideal = T v_i, figure of merit FM = P_ideal/P_actual; example ~2,700 kg light helicopter, R=5.1 m (generic).
- Physics track: projectile with drag (ODE, numeric), simple harmonic oscillator → damped → eigenvalues (ties to aircraft stability), Lagrangian of a pendulum (grad).

## 6. Interactive elements
- Orbit Lab (Δv → animated orbit raise; vis-viva live readout), Kepler solver iteration stepper, Hohmann calculator, root-locus/eigenvalue plotter for short-period, rotor disk-loading slider, unit converter.
- Vanilla JS + canvas/SVG, no build step, works offline-ish on iPad; KaTeX self-hosted.
- Every interactive: keyboard operable, visible focus, `aria-live` numeric readouts, text description of the animation, pause/reduced-motion honoring `prefers-reduced-motion`.

## 7. Accessibility (WCAG 2.2 AA)
- Math as KaTeX with MathML output (screen-reader readable); never equations as images.
- Alt text for figures, long descriptions for diagrams; color-blind-safe palettes; ≥4.5:1 contrast.
- Hidden solutions via native `<details>/<summary>`; touch targets ≥44px; works at 200% zoom.

## 8. Five-language considerations (EN/FR/ES/IT/AR)
- Math notation stays LTR inside RTL Arabic (`dir="ltr"` on math spans/code); numbers use locale decimal separator in prose but `.` in code/inputs (accept both in answer boxes).
- Glossary per language for terms (eccentric anomaly, figure of merit, short-period mode) reviewed against ESA/CNES/ASI terminology.
- Units SI everywhere; imperial secondary for aero (ft, lbf) shown in parentheses.
- Translated `hreflang` + same slug pattern (/fr/, /es/, /it/, /ar/).

## 9. Sources (verified 200, 2026-10-16)
ocw.mit.edu/courses/16-07-dynamics-fall-2009 · ocw.mit.edu/courses/16-346-astrodynamics-fall-2008 · ocw.mit.edu/courses/16-100-aerodynamics-fall-2005 · ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016 · ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011 · khanacademy.org/science/physics · tutorial.math.lamar.edu · grc.nasa.gov/www/k-12/airplane · science.nasa.gov/learn/basics-of-space-flight · esa.int/Education · openstax.org/details/books/university-physics-volume-1 · 3blue1brown.com · brilliant.org · phet.colorado.edu · phys.libretexts.org · aa.stanford.edu · galcit.caltech.edu · engineering.purdue.edu/AAE · ae.gatech.edu · Curtis (Elsevier) · Vallado software (celestrak.org/software/vallado-sw.php)

## 2026-10-16 — Learn Phase 1 BUILT (Orbital Mechanics track)
- **Structure correction (owner):** NO standalone Mathematics track / Math_Track hub (none was ever built; nothing to remove). Learn.html shows THREE tracks: Orbital Mechanics (live), Aeronautical Engineering, Physics (coming). Math (calculus, vectors, linear algebra, ODEs, Newton-Raphson, RK4, root finding) is woven into each track as step-by-step worked examples.
- Pages (EN/fr/es/ar/it): Learn.html, Orbits_Guide.html (kids/teens/community college), Orbit_Math.html (undergrad→PhD, 13 sections), Orbit_Lab.html. New nav door "Learn" (build-ux GROUPS 'le', labels from learn_text.py). STYLEV 20261016L.
- Generator: scripts/build-learn.py (content: learn_orbit_math.py, learn_text.py, learn_extras.py; numbers: learn_calc.py, never typed). KaTeX 0.16 rendered at build (scripts/katex-render.cjs, htmlAndMathml), self-hosted in assets/vendor/katex (woff2 + LICENSE). assets/learn.js (auto-checked practice, hints, MCQ), assets/orbit-lab.js (+ node scripts/test-orbit-lab.js in weekly-sync).
- Follows /workspace/learn-benchmark-spec.md: track/level badges, est. time, last-verified date; goals; prerequisites linked; intuition box; numbered derivations with a "why" per step; structured worked examples (Given/Find/Strategy/Steps/Answer/Sanity/Significance + Python toggle) for Hohmann and Kepler/Newton-Raphson (iteration table); auto-checked numeric practice (dot or comma, tolerance, progressive hints, hidden solution); conceptual practice; common mistakes; Check your understanding (3 MCQ with feedback); Go deeper; For teachers; per-section citations. Math/code/inputs LTR inside Arabic.
- Verified numbers: LEO300→GEO 2.4257 + 1.4668 = 3.8926 km/s, TOF 5.275 h; + 28.5° combined at apogee = 4.256 km/s total; Kepler e=0.37255, M=3.6029 → E=3.479422 rad in 4 iterations (Curtis Ex. 3.2 gives 3.479); SSO 700 km 98.19°, 800 km 98.60°; ISS RAAN −4.95°/day; Lambert checked by RK4 (1.7e-10 km). Phase 2 check: hover 2700 kg, R=5.1 m, ρ=1.225 → v_i=11.50 m/s, P_ideal=304.5 kW.
- Open (not yet built): "Explain like I'm 10" box per topic, Kepler iteration stepper / Hohmann calculator widgets on Orbit_Math (Orbit Lab covers Hohmann), per-language glossary review vs ESA/CNES/ASI terms, SI diagrams.
- **Phase 2 (Aeronautical Engineering) plan:** atmosphere/units → lift, drag, thin-airfoil theory → finite wings (lifting-line) → compressible flow/shocks → jet propulsion (Brayton) → performance → stability & control (short-period 2-state [α,q] model, ω_n/ζ vs MIL-STD-1797 ranges, eigenvalue plotter) → rotorcraft (momentum + blade-element, disk-loading slider) → CFD basics. Generic "high-performance jet"/"rotorcraft"; SI units with imperial in parentheses.
- **Phase 3 (Physics) plan:** Newtonian mechanics & conservation → projectile with drag (numeric ODE) → oscillators (SHO→damped→eigenvalues, ties to aircraft stability) → Lagrangian/Hamiltonian (pendulum, central force, Noether) → E&M (Maxwell, plasma/space weather) → thermo & stat mech → fluids (Navier–Stokes) → relativity for orbits (GPS clocks, Mercury perihelion).

## 2026-10-16 — Learn Phase 1 gaps closed + Phase 2 Aeronautical Engineering BUILT
- Phase 1 gaps: per-topic ELI10 on all 13 Orbit_Math sections; embedded Kepler stepper (.wk) and Hohmann calculator (.wh); full Given/Find/Strategy/Steps/Answer/Sanity/Significance + Python on all topics; LEARNLINK aside on Teachers, Satellite_Explorer, Play_and_Learn (now also links Aero_Guide/Aero_Lab).
- Phase 2 pages (5 langs): Aero_Guide.html (4 forces, wings, why jets fly high, hover, stability), Aero_Math.html (9 sections: atmos, airfoil, wing, perf, compress, prop, stab, rotor, cfd; each with intuition, ELI10, derivation in KaTeX, full worked example + Python, auto-checked practice with hints/solutions, mistakes, per-section refs; 3 MCQs; teacher + deeper notes), Aero_Lab.html (ISA stall calculator, short-period eigenvalues + s-plane + MIL-STD-1797A Level 1 ζ check, rotor hover sliders).
- Content: scripts/learn_aero.py; numbers: scripts/aero_calc.py (all placeholders a_*); lab JS assets/aero-lab.js checked by scripts/test-aero-lab.js against the same values. build-learn.py math_page is now track-generic (TRACKS dict). Hub marks Aeronautical Engineering live; nav door 'le' has the 3 aero pages; STYLEV/V 20261016N.
- Verified numbers: ISA 11 km 216.65 K / 22632.04 Pa / 0.363918 kg/m³ / a 295.07 m/s (USSA 1976); c_l(5°) 0.5483; stall 26.07 m/s (50.7 kn), 28.05 at 1500 m; C_Di 0.01105; finite a 4.917/rad; (L/D)max 16.82 at C_L* 0.673; Breguet 5235 km; M2 isentropic T0/T 1.8, p0/p 7.824; normal shock M2 0.5774, p2/p1 4.5, p02/p01 0.7209 (NACA 1135); Brayton η 0.622 (π 30) / 0.482 (π 10); short period ωn 3.082, ζ 0.454, −1.4±2.746i; hover vi 11.50 m/s, P_ideal 304.5 kW, DL 324 N/m², FM 0.761; FD errors 0.0429 / 0.0009.
- Fixed: build-learn copied Kids_Map's report-a-correction URL into learn pages (fought build-report-link); now rewritten per page, pipeline converges (learn/report-link/og all 0 writes on rerun).
- Open: Phase 3 Physics track; blade-element theory not yet covered (momentum theory only).

## 2026-10-16 — Arabic readout fix, blade-element theory, Learn Phase 3 Physics BUILT
- Aero Lab: readout numbers are now DOM <bdi dir="ltr"> (put() in assets/aero-lab.js), so "-1.400 ± 2.746i" keeps its order in Arabic; same pattern in phys-lab.js.
- Aero_Math rotorcraft: added blade-element theory + combined BEMT (4 derivation steps, auto-checked C_T problem, written question on 0.75R). aero_calc.bemt(): σ 0.08, a 5.73, θ.75 8° → λ 0.04980, C_T 0.004960, C_P 0.000357, FM 0.692; at 10° C_T 0.006701, FM 0.779 (Leishman ch. 3 form). Topic retitled "momentum and blade-element theory", levels ug/grad/phd.
- Phase 3 pages (5 langs): Physics_Guide.html (pushes and crashes, pendulums, air resistance, magnets/aurora, GPS relativity), Physics_Math.html (8 topics: newton, drag, osc, lagr, em, thermo, fluids, rel — full spec template, 8 auto-checked problems, 3 MCQs, teacher/deeper, per-topic refs), Physics_Lab.html (RK4 projectile with drag vs vacuum plot; damped oscillator eigenvalues + x(t) plot; exact pendulum period via AGM).
- Content scripts/learn_phys.py; numbers scripts/phys_calc.py ({p_*}, CODATA 2018); phys_calc.checks() asserts at build time that every literal typed in the text agrees with computed values/references. assets/phys-lab.js checked by scripts/test-phys-lab.js against phys_calc (RK4 matches Python to 1e-6; zero drag reproduces vacuum). Hub: all three tracks live; nav 'le' has 10 pages; V/STYLEV 20261016P.
- Verified: elastic 2kg@3 vs 1kg → 1, 4 m/s; ball 40 m/s 35° C_D 0.35: range 93.9 m (vacuum 153.3), apex 20.2, t 4.05 s, v_t 39.3 m/s, best angle 41°; oscillator ω_n 4, ζ 0.25, −1 ± 3.873i, Q 2; pendulum 1 m 60°: 2.0064 → 2.1532 s (+7.32 %, matches K(k) tables), 2 m 90° 3.3492 s; solar-wind proton r_g 835 km, T_g 13.1 s, f_pe 20.1 kHz (n 5 cm⁻³), c from μ0ε0; N2 300 K v_rms 516.8, mean 476.2 m/s; Re cruise wing 3.2e7 (μ 1.4216e-5 = USSA), model 4.11e5; GPS +45.65 / −7.21 / net +38.44 μs/day (Ashby 2003: 45.7/−7.1/38.6), 11.5 km/day; Mercury 42.98″/cy (Will 2014), Venus 8.62″/cy.
- SEO audit total rises with page count (15 new pages × site-wide og-locale-alt/jsonld categories), same pattern as existing learn pages.

## SI Helper pilot (Oct 16, 2026, HST)
- Option A from si-helper-plan: Cloudflare Worker `si-helper` (workers/si-helper/) at https://si-helper.chambersbryank.workers.dev — workers.dev only; NO DNS/routes on savingplanets.com. The 4 pre-existing account Workers are untouched.
- Pipeline: Turnstile (invisible widget "si-helper", sitekey public in Teachers markup) -> per-IP limits (rate-limit binding 10/60s; Durable Object `Guard` 50/day by salted IP hash) -> daily spend guard (pre-charge $0.004, settle to measured neurons x $0.011/1k; hard stop when >$1.00 UTC-day) -> PII regex block -> Llama Guard 3 on question -> bge-m3 embed -> Vectorize `si-helper-site` (1024d cosine, metadata index `lang`, MIN_SCORE 0.50) -> gpt-oss-120b grounded answer with [n] citations or "I don't know" -> Llama Guard 3 on answer. CORS/origin lock to savingplanets.com (+www). Question <=400 chars.
- Nothing stored: no question text, observability off, Guard keeps only today's counters (wiped at UTC day change).
- Index: scripts/si-index.py (incremental, manifest ~/.cache/si-index-state.json, outside repo). 4936 chunks (en 928, fr 1061, es 1037, ar 883, it 1027), ~5M stored dims (<10M included). Hooked into weekly-sync.sh after build-search, only when /home/box/.cloudflare_token exists, non-fatal.
- Pages: Teachers widget (5 langs, SIHELPER markers, generator scripts/build-si-helper.py + scripts/si_helper_text.py, assets/si-helper.js ?v=20261016S), SI_Helper.html "How SI Helper works and what we don't keep" (5 langs), Privacy section #si-helper (pilot).
- Secrets live only on the box (paths: /home/box/.cloudflare_token, /home/box/.cloudflare_account_id, /home/box/.si_turnstile_secret, /home/box/.si_ip_salt) and as Worker secrets TURNSTILE_SECRET/IP_SALT. Deploy: `cd workers/si-helper && bash ../../scripts/si-wrangler.sh deploy` (private Node 22 Wrangler).
- Tested via a temporary Worker `si-helper-test` (Turnstile test keys, local origin), deleted afterwards: EN/FR/AR grounded answers with sources, off-topic -> "I don't know", unsafe -> refusal, email -> PII refusal; iPad 820x1180 widget EN/FR/AR (AR dir=rtl), no overflow, no console errors, 44px button.
- Needs owner: COPPA/legal review before promoting to students; native-speaker check of AR/IT strings; custom domain decision; Cloudflare billing alert.
- Oct 16 follow-up: live iPad-width test (headed Chromium, real Turnstile) EN/FR/AR answered with sources; off-topic -> I don't know; unsafe -> refusal. Worker now normalizes gpt-oss 【n†Lx】 citations to [n] (version b78021b1).

## Header nav v2 (Oct 16, 2026, HST)
- New generator scripts/build-nav.py (runs LAST among page generators in weekly-sync, after build-new.py). Replaces `<nav id="topnav">…</nav>` on every page in 5 languages; keeps `<nav id="topnav">` + `<li class="lang-switch">` so older generators that copy the nav still work. CSS/JS in styles.css / site.js between SPNAV markers; cache v=20261016N (build-ux STYLEV).
- Pattern (kidSAFE-style, our colours): brand left; right side two rows. Utility row: language switch · Search · Weekly Brief · Find a Cleanup · Contact. Main row (13px bold uppercase): Solutions ▾, Space ▾, Learn ▾, Kids ▾, Teachers ▾, About ▾, CTA Help / Donate (Liquid Glass .nav-help style). No social icons: the site has no social accounts.
- Dropdowns: button + aria-expanded/aria-controls; open on hover (fine pointer) AND click/tap; Esc closes and returns focus; outside click closes; last 3 dropdowns align to the end edge. Fixed header: transparent with scrim at top, solid #071018-ish + shadow and tighter padding after 24px scroll (spn-solid). <992px: brand + 44px menu button, panel slides down (utility, main items as tap accordions, full-width CTA), opaque panel, z above sticky Help.
- All previous nav links kept (Search/Weekly Brief/Contact/Find a Cleanup moved to utility row; World Map under Solutions; Project Rawane + Mission Log under Space); added About pages (Editorial Policy, Corrections, Press, Privacy) and SI Helper page under Teachers.
- i18n-build/i18n-check normalize now ignore the whole header nav (regenerated per language), so nav changes never mark translations stale.

## Google Analytics removed → Cloudflare Web Analytics (Oct 16, 2026, HST; user-approved, COPPA)
- scripts/build-analytics.py replaces add-gtag.py (deleted) in weekly-sync (runs at the old add-gtag spots + once more after build-nav). Strips the GA4 block and any consent.js include from every page (5 langs) and adds the Cloudflare Web Analytics beacon (static.cloudflareinsights.com/beacon.min.js, site token 9d4c…8186, public by design) before </body> between CF-WA markers.
- Web Analytics site: an existing site for zone savingplanets.com (site_tag d61bb4a4…, created in the dashboard Oct 8) is used. Creating a new one via API returned 403 (token can read RUM, not edit: would need Account › Account Analytics/Web Analytics Edit) — not needed. No DNS/proxy change; the site stays on GitHub Pages, beacon is the manual JS snippet.
- Consent banner removed (consent.js deleted): Cloudflare WA sets no cookies/localStorage and keeps no identifiers, so there is nothing to consent to. site.js deletes the old sp_consent key once. search-ui.js no longer sends search text anywhere (both GA search events removed); cache: site.js/styles v=20261016G, search-ui.js v=20261016g.
- Privacy (s2 analytics, s4 kids paragraph, s5 browser storage, Last updated Oct 16) and the About analytics paragraph rewritten in en/fr/es/ar/it by build-analytics.py (it owns that text; trust-content.py's GA text is overwritten later in the sync).

## Aggregate event counts (Oct 16, 2026, HST; user-approved)
- Worker: new route POST /e on si-helper (version 6f2fc04e…). Origin-locked (403 otherwise), rate limit RL_EV 60 batches/min per visitor (salted hash in memory only), ≤20 events/batch, strict allowlist per event (no free text), writes to Workers Analytics Engine dataset `sp_events`: blobs [event, lang, field1..3], double 1. No IP/UA/URL/cookie/identifier written.
- Events: lab {tool orbit|aero|phys, once per page}; learn {track, kind hub|guide|math|lab}; practice {track, result attempt|correct, topic = section id}; si {outcome ok|none|unsafe|pii|busy|bot|error} written server-side in /ask (never the question); newsletter (successful submit count); partner {host, kind donate|join|link} on Ways_to_Help.
- Client: scripts/build-events.py → SPEV block in site.js (v=20261016E). Skips entirely on Do Not Track / Global Privacy Control; batches, navigator.sendBeacon text/plain on page hide or 10 queued.
- Private report: `python3 scripts/events-report.py [days]` → ~/reports/events-YYYY-MM-DD.md via Analytics Engine SQL API (token has read access). Nothing public.
- Privacy analytics section gets the extra paragraph from scripts/events_text.py (5 langs) via build-analytics.py.

## Report-a-correction form + SI cap alert email (Oct 16, 2026, HST; user-approved)
- Email: Workers `send_email` binding MAIL (destination fixed to media@savingplanets.com) from site-forms@savingplanets.com. Email Routing was already active on the zone (MX route*.mx.cloudflare.net, cf DKIM present); NO DNS/MX/Routing change made. media@ was already a verified destination: test sends arrived (Gmail, 03:07 and 03:08 UTC Oct 17).
- Worker POST /report: origin lock, ≤6 KB, page URL must be a savingplanets.com URL, "what" ≥10 chars, refuses emails/phone numbers (same PII regex as SI), Turnstile, RL_REP 3/min + Guard 10/day per salted IP hash (in DO day counters only), one email per report, nothing stored; event count report/sent. Email footer reminds: credit fixes in the correction log to "SI Partner".
- SI cap alert: Guard sets `alerted` the first time a /check is refused for budget each UTC day → one email to media@ (tested with a temporary worker at cap 0: 1 email for 2 refusals; temp worker deleted).
- Site: build-report-link.py now links every footer (5 langs, incl. kids pages) to Corrections.html?page=<page>#report; REPORTFORM block (form, 5 langs, RTL, 44px, aria-live) on each Corrections page + assets/report-form.js (v=20261016r). GitHub issue link removed from all footers; one small "Adults with a GitHub account…" line remains on Corrections only.
- Privacy s6 gets the form paragraph (scripts/events_text.py REPORT_P via build-analytics.py).

## CC BY-NC 4.0 licence (Oct 16, 2026, HST; user-approved)
- scripts/build-license.py (weekly-sync, after build-report-link): footer line on every page in 5 langs (LICENSE block, rel="license" to the CC deed in that language), <link rel="license"> in every head, JSON-LD "license" on page-level types only (not ImageObject/VideoObject: third-party media keep own licences), About #licence "Use & licence" section (LICABOUT block): attribution "Saving Planets (savingplanets.com)", third-party media keep own credits, SI media keep "Created by SI and Biological SI Partner", commercial use → media@.
- i18n-build/check strip REPORTFORM|LICENSE|LICABOUT blocks from the source hash.

## Classroom share + Weekly Brief growth, COPPA-safe (Oct 16, 2026, HST; user-approved)
- scripts/build-share.py (weekly-sync, after build-license): CLSHARE block (named so it does not clash with the existing social SHARE block) after the <h1> on Learn, *_Guide, *_Math, *_Lab, Teachers (5 langs): "Share to Google Classroom" = plain link to https://classroom.google.com/share?url=…&title=… (no Google script; nothing sent to Google unless clicked) + Copy link (Clipboard API, fallback) — assets/share.js v=20261016s; clicks → spTrack('share',{kind:classroom|copy,page}) → /e (Worker allowlist share.kind/page). events-report.py has a Share section. Privacy events paragraph mentions share clicks + the Classroom plain-link note (5 langs).
- NLCALL Weekly Brief callout ("For teachers, parents and students 13+"), reusing site.js MailerLite double opt-in, only on Learn hub, *_Math, Teachers (#weekly-brief). Guides and Labs are written for kids/teens (audit lists labs as kids-directed) so they are treated as kids pages.
- Kids pages (Kids_Map, Amazing_Facts [its static newsletter band is removed too], Satellite_Explorer, Spot_the_Fire, Myth_vs_Fact, Play_and_Learn, Glossary, *_Guide, *_Lab): body data-no-newsletter (no footer signup) + GROWNUPS footer link "Grown-ups: get the Weekly Brief" → Teachers.html#weekly-brief.
- Kids.html redirect pages (5 langs; meta refresh + canonical + link, noindex) → Play_and_Learn.html (was 404).
- Fix: Learn "On this page" TOC (.lw nav) was position:fixed via the old body.toc-sub nav rule and covered the hero on iPad; now static (build-nav CSS). STYLEV 20261016T.

## Oct 16, 2026: Calculators, Start-here pages, Careers, standards tags, embeds
- **Calculators** (scripts/build-calcs.py; text calc_text.py; numbers calc_check.py → calc-vectors.json; widget assets/calc.js): Calculators.html + 11 search-named pages (Delta_V, Hohmann_Transfer, Orbital_Period, Orbital_Velocity, Stall_Speed, Lift_Equation, Mach_Number, Thrust_to_Weight, Rotor_Hover_Power, Projectile_Motion_Drag, Pendulum_Period `_Calculator.html`), 5 languages, KaTeX at build, worked example generated from the Python mirror, sources, Learn + lab links. Textbook checks assert at build (Hohmann LEO→GEO ≈3.89 km/s, GEO 23.934 h, ISS ≈92.6 min, NASA escape 11.186 km/s, ISA 1.225 / 216.65 K, √2 at 60° bank, a = 340.29 m/s, Leishman v_i, 2.006 s pendulum, AGM large-angle factor). weekly-sync: `calc_check.py && node scripts/test-calcs.js` (19 vectors) fails the sync on error.
- **Start here + Careers** (scripts/build-paths.py; text paths_text.py / paths_text2.py / paths_text3.py): Careers.html (BLS OOH, May 2025 median pay, 2025–35 outlook, pages modified Aug 27 2026; FAA/VA/SkillBridge; scholarship list with official links only, dates only where verified: AIAA Oct 15–Jan 31, CAP 2027 cycle Dec 15 2026–Jan 15 2027), Cadets.html (AFJROTC/NJROTC topics from Kentucky DOE 2025–26 JROTC course descriptions; CAP Aerospace Dimensions 1–6, ACE, AEX; Army/Marine not mapped; disclaimers; instructor section + printable topic map), AP_IB_Physics.html (AP1 units 1–4, 7, 8; AP C note; AP2 units 9, 14; IB A.1–A.3, C.1, D.1; College Board trademark line), Homeschool.html (ages 5–18, 12-week printable plan). Start-here block on Learn.html and Teachers.html; Learn nav dropdown gets the 5 entries (learn_text.NAV_ITEMS ← paths_text.NAV).
- **Kids/no sign-up**: Cadets + Homeschool are kid-facing (build-share NOSIGNUP: data-no-newsletter + grown-ups link). Weekly Brief callout on Calculators/calculator pages, Careers, AP_IB. build-learn shell now drops the Kids_Map template's data-no-newsletter.
- **Standards** (scripts/build-learn-standards.py; NOT the older build-standards.py): NGSS / CCSS / AP / IB chips under the hero + schema.org educationalAlignment on Learn guides, math pages, labs and calculators; filter-by-standard (STDMAP) on Learn.html. Editorial alignment, noted on the page.
- **Embeds** (scripts/build-embed.py, assets/embed.js): dt-bar Embed button with prefilled iframe + attribution + CC BY-NC 4.0 line on calculators, Orbit/Aero/Physics labs and Artemis_II launches; `?embed=1` hides nav/footer/share/newsletter/help, opens links in a new tab, shows an attribution bar; `&only=launches` keeps one section. GitHub Pages sends no X-Frame-Options/CSP, so framing is allowed.
- **Events**: Worker /e allowlist adds `calc {tool}` and share kind `embed`, pages `calc|path|launches`; site.js SPEV maps spTrack('calc'); Privacy text updated (5 langs). Marker blocks STARTHERE/EMBED/EMBEDMODE/STDTAGS/STDMAP stripped by i18n-build/check. STYLEV 20261016U.
