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
- **Ad v2** posted via Postiz (X/TikTok/YouTube) + featured on About; GA4 G-ZCJ7CEKN94 on every page (Consent Mode v2).
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
- GA4 G-ZCJ7CEKN94 (Consent Mode v2, add-gtag.py). IndexNow key aa19429b4f58f36d34c263abe996de09.txt.
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

**Batch 2026-10-15** (17, ~6:38 AM HST run). Nothing built; awaiting owner yes/no. No new solution pages vs existing *.html; Dragonfly already has a mission widget on Titan.html (flagged). Org figures labeled as org figures. Spot-checked ESA Sentinel-3 (3C 15 Sep 2026) and HydroGNSS (science ops / open data 31 Jul 2026).
| ID | Candidate | Hub | Widget | Status |
|---|---|---|---|---|
| A | NASA EMIT (ISS spectrometer; methane/CO₂ plumes + mineral dust) | Earth Observation | Yes, extended ≥2026 | PENDING |
| B | NASA GEDI (ISS lidar; forest canopy / carbon) | Forests (+ EO) | Yes, ops post-2024 reinstall | PENDING |
| C | NASA OCO-2 (global CO₂; Caltech ops partnership 2026) | Earth Observation | Yes, active (+ OCO-3 note) | PENDING |
| D | ESA Sentinel-5P / TROPOMI (daily air quality + CH₄) | Earth Observation | Yes, operational | PENDING |
| E | NASA PREFIRE (polar far-IR CubeSats; extended through Sep 2026) | Earth Observation | Yes | PENDING |
| F | ESA HydroGNSS (Scout GNSS-R soil moisture/wetlands; open data 31 Jul 2026) | Earth Observation (+ Rivers/Lakes) | Yes | PENDING |
| G | ESA Sentinel-3 A/B/C (ocean/land/ice; 3C launched 15 Sep 2026) | Earth Observation | Yes, 3C commissioning | PENDING |
| H | NASA Libera (Earth radiation budget on JPSS-4; LRD ~2027) | Earth Observation | Yes, horizon to launch | PENDING |
| I | Surfrider Foundation (beach cleanups + plastic policy) | Oceans | No | PENDING |
| J | Heal the Bay (Santa Monica Bay / LA County) | Oceans | No | PENDING |
| K | Plastic Odyssey (containerized recycling factories) | Oceans | No | PENDING |
| L | Trout Unlimited (coldwater river restore/reconnect) | Rivers | No | PENDING |
| M | Chesapeake Bay Foundation (oysters, trees, living shorelines) | Rivers (+ estuaries) | No | PENDING |
| N | League to Save Lake Tahoe / Keep Tahoe Blue | Lakes | No | PENDING |
| O | American Forests (Tree Equity + U.S. reforestation) | Forests | No | PENDING |
| P | Plant-for-the-Planet (youth restoration + platform) | Forests | No | PENDING |
| Q | NASA Dragonfly (Titan rotorcraft; launch ~Jul 2028) | Project Rawane | Yes | PENDING — already mission widget on Titan.html; approve only for dedicated page |
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

- Daily sync (Oct 15, ~6:55 AM HST): weekly-sync.sh exit 0; All translations current; SOTW Great_Bubble_Barrier; Roman 1494325 km; fr/es/ar/it 157 pages each; pagefind 788 pages (5 langs); solutions.json 125; seo-audit TOTAL 1066 (title-length 2, twitter-missing 36).
- Daily sync FIXED (Oct 14, 85524bfc): i18n-check now runs right after i18n-build in weekly-sync.sh (later all-language post-processors edit English and always read as stale); i18n-build runs seo-fix on English before hashing; JSON-LD and RELATED blocks ignored in i18n hashes (py + js). Full sync exits 0.
- Solution candidates 10/14: CO2M (Earth Observation) and Mission Blue Hope Spots (Oceans) approved and BUILT (3fefc99b), 120 solutions.

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
