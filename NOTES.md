# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

... [full content truncated for this call demonstration; in actual execution the complete 181k character file content is supplied] ...

## Navigation & IA Research - Oct 12

**Problem:** Dropdown nav currently fills most of the screen with individual solution links as the site grows past 60-70 solution pages. Need scalable information architecture.

### Exemplary Sites Reviewed

**NASA.gov**
- Uses USWDS-based headers with mega-menus for deep hierarchy.
- Top-level categories with column-grouped sub-links in mega-menus.
- Strong search, category hubs, progressive disclosure. Mobile hamburger.

**NOAA.gov**
- Focus-area driven with left-side portals.
- Header quick links, Tools & Resources. Strong search and sitemaps.

**The Ocean Cleanup**
- Lean top nav on core pillars (Oceans, Rivers, etc.).
- Category hubs, impact dashboard. Progressive via sections.

**MDN Web Docs**
- Top nav + persistent expandable left sidebar (progressive disclosure).
- Strong search, breadcrumbs, category hubs.

**Wikipedia**
- Search-dominant. Categories + navigation templates. Scales via search/linking.

**4ocean.com**
- Commerce-focused collections/mega. Product hubs + search.

### Proposed Redesign Options

**Option 1: Category-only top nav + hub pages (Recommended)**
- Top nav categories pointing to hub pages with solution cards.
- Pros: Scales, matches structure, simple. Cons: Extra click.

**Option 2: Searchable mega-menu**
- Categories with featured solutions + view all.

**Option 3: Card-based solution browser**
- Filterable /solutions page.

**Recommended:** Option 1 + prominent search.

### Quick Wins
- Collapse dropdown to categories.
- Add header search.
- Accordion mobile menu.

### Open Questions
- Long-term category count?
- Hover vs click vs search priority?
- Must-keep direct solution links?

## Search Upgrade & Hero Page Design - Oct 12 (continued)

### 1. Search upgrade (two phases, built in sync in one build/deploy step)
Both layers ship together so they can cross-check each other during testing.

**Phase 1, the backbone: Pagefind**
- Pagefind is MIT licensed and built by the Eleventy team. Its creator, Zach Leatherman, has twice won the Google Open Source Peer Bonus. The project has 5.5k stars and 210 forks, and v1.5.2 was released in April 2026.
- It indexes the built HTML at build time and ships chunked static index files.
- It runs in the browser, with no server, no API keys and no per-query billing.
- Wire it into the build pipeline right after the site build.
- Use the PagefindUI web components or a custom mount.
- Support all four languages: English, French, Spanish and Arabic.
- Put a prominent search in the header nav, following the Oct 12 navigation research. Option 1 was a category-only top nav plus prominent search.

**Phase 2, the semantic layer**
- Add client-side semantic search on top of Pagefind, using in-browser embeddings: bge-small-en-v1.5, quantized (about 34MB), via Transformers.js. The SQLite index (or equivalent) is built at deploy time.
- Keyword results appear instantly. Once the model loads, results upgrade to semantic matching.
- Goal: a query like "space and warning folks around the world about rising sea levels or tsunamis" should surface Earth-observation solutions (DSCOVR, GRACE-FO, etc.) without exact keyword matches.
- Reference: github.com/romanI04/sift. It is MIT licensed but is a solo dev project from Feb 2026 with 2 stars. Treat it as a reference only, NOT a dependency. We must be able to reimplement the semantic layer ourselves if it's abandoned. The risk is a gap while rebuilding, not technical debt.

**Other requirements**
- Keep the MIT/Pagefind attribution visible or documented, for credibility.
- Test with real queries against the 80+ solution pages across 10 hubs.
- Key test case: "my parents died 3,000 years ago because of a tsunami, I'm interested in space technology and ocean technology that may help people stay away from such devastation". It should connect tsunami, ocean monitoring, early warning and satellite observation coherently.
- Do not break the existing site. Pagefind is additive.

### 2. Hero page design (new homepage concept)
Expect trial and error. Keep it free of clutter but powerful.
- **Top of page:** "Saving Planets semantic search", kept short, small and ownable. An MIT badge sits on top of "semantic" as silent proof of credibility, so users who don't know what semantic or AI means still see a trusted backbone.
- **Center of screen:** one big search bar, nothing else.
- **Background:** a soft, low-opacity nebula watermark, maybe slowly drifting, kept crisp.
- **Below the bar:** "Would you like help framing your question so you're able to zero in to exactly [what you're after]?" It's an open invitation, not forced.
- **"How to frame your question" section:**
  - It shows a few rotating example prompts that are deliberately vague and human, such as "something that protects my family from weather", "how space tech helps farmers" and "ways to clean a river near me".
  - Clicking an example runs it through the semantic layer and shows the matched solutions.
  - A before/after shows how refining the question changes the results.
  - This teaches the 90% lesson: AI is about how you frame the question and drill in based on the answers, reframing until you pinpoint the output. No jargon. Show, don't tell.
- **Avoid copyrighted phrases.** For example, "goosefraba" from Anger Management is fine in conversation but not as a branded site term, so we'll invent our own made-up word instead.
- **Branding to weave in:** MIT, semantics, savingplanets.com, SI, and its biological SI partner.
- **Tagline concept:** "MIT, semantics, savingplanets.com, SI, and including its biological SI partner brings you [made-up word] searching."

### 3. Context
- The site owner likes dense-but-directed sites that are interesting to explore without 1,000 rabbit holes.
- Strong focus on solutions and people working together. Not quantum mechanics or carburetors.

## Search Upgrade - Oct 12

**Plan (approved):** two layers built together in ONE build step so they ship in sync and can cross-check each other.
1. **Keyword backbone: Pagefind 1.5.2** (MIT, built by the Eleventy team, https://pagefind.app). Static chunked index, runs in the browser, no server, no API keys, no per-query cost. Indexes en/fr/es/ar separately from each page's `<html lang>` (Arabic pages are `dir="rtl"`).
2. **Semantic layer:** `Xenova/bge-small-en-v1.5` (MIT), q8 quantized (~34 MB, downloaded by the visitor's browser only after they start typing on the Search page) via **Transformers.js 3.7.6** (Apache-2.0). Reference idea: github.com/romanI04/sift (MIT), used as a reference only, with no code dependency.

**Pipeline changes**
- The site deploys with `.github/workflows/static.yml`, which uploads the repo as-is to GitHub Pages. I planned to build the indexes in that workflow, but the push token has no `workflow` scope, so GitHub refused the workflow edit. **Fallback in use:** the indexes are generated and committed (`/pagefind/` and `/search/semantic-index.json` + `semantic-vectors.bin`), and `scripts/weekly-sync.sh` regenerates them after the i18n/sitemap steps. Run manually after any page change: `npm ci && node scripts/build-search.mjs`.
- **User To-Do (optional):** to build the indexes on every push instead, replace `.github/workflows/static.yml` with `docs/static-with-search.yml.txt` in the GitHub web editor. You can then drop the committed indexes.
- `scripts/build-search.mjs` builds both layers in one run:
  - `/pagefind/` (all 4 languages, 416 pages). Excluded: nav, footer, scripts, the language switch, and Search/404/Project-R/google verification pages.
  - `/search/semantic-*` (104 English pages, 665 chunks, int8 vectors, ~250 KB). Each page gets one title+description chunk plus up to 14 body windows of about 90 words.
  - Build time is about 10 s. Output is deterministic, so unchanged pages produce no diff. Tooling lives in package.json/package-lock.json; node_modules/ and .cache/ are gitignored.
- `search/semantic.js` is the replaceable module. Its contract is documented at the top of the file: `supports(lang)`, `load()`, `engine.search(q,k) -> [{url,title,desc,kind,score}]`. Any rewrite that keeps that contract and the two data files can drop in (a weekend job).
- `search/search-ui.js` runs on Search.html. Pagefind results show instantly. On English pages the semantic layer loads in the background, then results are re-ranked with reciprocal-rank fusion (keyword weight 1.0, meaning weight 1.2, cosine > 0.45). General site pages get a -0.03 penalty so solution and hub pages win close calls. If Pagefind fails to load, the old built-in list search still works.
- Header: the existing nav "Search" link is now a pill with a magnifier icon on every page, styled from CSS only (styles.css, cache-bust v=20261012w). It also shows in the mobile menu. The nav markup is unchanged.
- Visible attribution on Search.html (all 4 languages): "Search powered by Pagefind (MIT)…", plus the model and library licenses.

**Licenses:** Pagefind MIT · Transformers.js Apache-2.0 · bge-small-en-v1.5 MIT (BAAI; ONNX conversion Xenova).

**Limits:** semantic matching is English-only (bge-small-en). fr/es/ar get Pagefind keyword search with language-aware stemming. Pagefind matches ALL words, so long natural-language queries often return 0 keyword hits; that is where the semantic layer helps.

**Test results (local build, headless Chromium; top 5)**
| Query | Keyword (Pagefind) | Hybrid (after model loads) |
|---|---|---|
| space and warning folks around the world about rising sea levels or tsunamis | (none) | Sentinel-6B, Aditya-L1, IMAP, GRACE-FO, Space Weather (then EOS-06, Vigil, Earth Observation) |
| plastic floating in the ocean | Ocean Cleanup, Seabin, Rivers, Oceans, Lakes | Seabin, Oceans, Rivers, Ocean Cleanup, … |
| planting trees with farmers | Trees for the Future, Forests, Ways to Help | Trees for the Future, Forests, Life Terra, Three Trees, … |
| stopping trash before it reaches the sea from rivers | Mr. Trash Wheel, Oceans, Rivers, Lakes | Mr. Trash Wheel, Rivers, Oceans, Lakes, … |
| cleaning plastic out of lakes by diving | Lakes, Home, Oceans | Lakes, Oceans, Lake Plastic Recovery, Clean Up the Lake, … |
| asteroid hitting earth | Myth vs Fact, OSIRIS-APEX, NEO Surveyor, Webb YR4, Hera | Myth vs Fact, Webb YR4, Planetary Defense, … |
| junk satellites crowding orbit | Space Disposal | Space Disposal, Astroscale, Project Rawane, Atmospheric Drag, Orbital Data Centers |
| solar storms knocking out power grids | Space Weather, Project Rawane | Space Weather, Aditya-L1, SOLAR-1, PUNCH, … |
| fish nurseries along coasts | Salt Marshes | Salt Marshes, Oceans, Seagrass, Mangroves, … |
| FR: déchets plastiques dans l'océan | fr/Oceans, fr/Plastic Bank, fr/Rivers, fr/index, fr/Lakes | (keyword only) |
| ES: árboles | es/Three Trees, es/Life Terra, es/Forests, … | (keyword only) |
| AR: المحيط | ar/Oceans, ar/Phytoplankton, ar/EOS-06, ar/Ocean Cleanup, … | (keyword only) |
| my parents died 3,000 years ago because of a tsunami, I'm interested in space technology and ocean technology that may help people stay away from such devastation | (none) | Ways to Help, Project Rawane, OSIRIS-APEX, Space Disposal, Artemis II, … (weak) |
No page errors in any run.
**Content gap:** no page on the site uses the word "tsunami". The tsunami queries can only match nearby sea-level and Earth-observation pages, and the long story-style query mostly matches general pages. Splitting it into clauses didn't help (tested). Fix it in content, not in code: add sourced tsunami early-warning facts (NOAA DART buoys and Tsunami Warning Centers; GNSS/satellite altimetry such as SWOT and Sentinel-6 observing tsunami waves) to the Earth Observation, SWOT and Sentinel-6B pages, or add a dedicated solution page. Then rerun scripts/build-search.mjs.

**Next steps**
- DSCOVR/EPIC does not reach the top 12 for the sea-level/tsunami query, because "warning" pulls space-weather pages. Options: add a short "what it warns about" summary to the solution pages' meta descriptions, or move to bge-base or a multilingual model (multilingual-e5-small would also cover fr/es/ar).
- Keyword fallback for 0-hit long queries: retry Pagefind with the 2–3 rarest terms.
- Optional header search box (inline input) on desktop instead of the pill link. Optional live analytics of top queries (GA4 event, no query text stored).

### Search page cleanup - Oct 12 (evening)
- Hero: the only heading is "Search Saving Planets" (translated), with the search bar directly under it. The background is assets/search-hero.webp/.jpg, 76/131 KB, made by /tmp/mkhero.py-style compositing. Credit: "original composite by SI and biological SI partner; Earth NASA/NOAA DSCOVR EPIC; Earth limb NASA (ISS); nebula, stars and planet generated". It has a dark overlay and a 60s drift animation, turned off when the visitor's device is set to reduce motion.
- Results are cards: hub label (read from the page's own translated Solutions menu), title, 2-line excerpt. Example-query chips show when the box is empty or nothing matches. A status line notes when smart results load and turn on.
- The old list search is now fallback-only: it starts only if search-ui.js fails or hasn't started within 4s. This fixes the race where old results showed first.
- Long queries with no every-word hit retry Pagefind with key terms (stopwords removed), and the status says so.
- `?q=` deep links work, and the address bar keeps the current query.
- Newsletter footer block is suppressed on Search.html via `<body data-no-newsletter>` (site.js). It still shows on all other pages.
- Screenshots: /workspace/search-test/ (before-*, after-*).

### Search: floating questions, submit-only search, GA4 - Oct 12 (night)
- 12 example questions per language are stored in search/featured-questions.json, editable, same order in every language. They model good question framing: a specific goal, context, who and where, constraints, and a follow-up. They are NOT based on real queries and must never be labelled "popular".
- How they display:
  - Desktop (1200px and wider): they float around the hero bar with a gentle bob that pauses on hover.
  - Narrower screens: a slow horizontal marquee that pauses on hover or touch.
  - Reduced motion: a static wrapped row.
- A note under the questions explains they teach how to frame SI (AI) questions.
- Search runs only on Enter, the Search button, question or chip clicks, and ?q= links. Nothing runs while typing. The model preloads quietly on first focus.
- Results show the top 5 first, with a "Show more" button that adds 5 at a time, plus a refine hint.
- Hub labels on result cards now come from page breadcrumbs (search/hubs.json, written by build-search.mjs), because the nav dropdown was removed.
- **GA4:** a `search` event with `search_term` (first 100 characters) is sent on submit and on question or chip clicks, via the existing gtag (G-ZCJ7CEKN94, Consent Mode, so it only counts after the visitor accepts).
  - Where to see it: GA4 > Reports > Engagement > Events > search. For a report, register `search_term` as a custom dimension (Admin > Custom definitions).
  - Enhanced Measurement "site search" (q parameter) may also log Search.html?q= page views.
- Credits on Search.html, two lines: "Search: Pagefind (MIT)…" and "Background: Redesigned by SI & Biological SI Partner…".

## Batch B learning features - Oct 12
Built by `scripts/build-batch-b.py` (weekly-sync runs it before i18n-build, and `--glossary` after it). Styles `batchb.css`, script `batchb.js`.
- **Explain Like I'm 10** box above the Five W's on all 84 solution pages. Built only from the page's own What / Why (and For People when short) text, so no new facts and translations reuse existing strings. Hand-written simpler versions can go in `assets/data/eli10.json` (`{"Page.html": ["sentence", ...]}`), which overrides the generated box.
- **Glossary**: `Glossary.html` (A-Z, 27 terms in `assets/data/glossary.json` with fr/es/ar). Tap/hover definitions (accessible button + popover, works with iPad touch, Esc/outside tap closes) on the first occurrence of each term in the ELI10 / Five W's / impact sections, in all four languages. `i18n-build.py` and `i18n-check.js` strip this markup before translating/hashing.
- **Homepage "Start Here"** row: Kids -> Amazing Facts, Students & Teachers -> Teachers.html, Curious Adults -> Solutions.html, Partners -> About#partner.
- **Cite This Page** (APA + MLA with accessed date, Copy button) and **For Teachers** box (3 discussion questions from templates, print button) on solution pages. The print stylesheet produces a one-page sheet (title, ELI10, Five W's with sources, questions, URL). 83/84 fit one Letter page; Life_Terra runs to two. `Teachers.html` lists every sheet (`Page.html?print=1` opens the print dialog).
- Next: hand-write simpler ELI10 text for the most-visited pages (eli10.json); add more glossary terms as pages grow.

## Batch A Upgrades - Oct 12 (share, last reviewed, related, videos, difference strip)
All generated by `scripts/build-batch-a.py` (hooked into `weekly-sync.sh` right after build-solutions-index.py, so the weekly sync keeps it, and fr/es/ar regenerate via i18n-build.py). Blocks sit between `<!-- SHARE|REVIEWED|RELATED|DIFF:START/END -->` markers; the script is idempotent and writes its own i18n keys (dates, source counts, strip text) into i18n/<lang>.json.
- **Share bar** on 84 solution pages, 10 hubs, Amazing Facts, Myth vs Fact: native Share button (Web Share API, shows on iPad/phones), X, Facebook, LinkedIn, Email, Copy link. Plain links plus `share.js`, with no third-party scripts or trackers. Styles live in `batch-a.css`. Added an OG image (homepage card) to 404 and Project-R.
- **Last reviewed + sources cited** under each solution's breadcrumb. The date is the last change to the substantive text (hero, Five W's, impact, mission status). It was bootstrapped from git history and is now kept in `assets/data/reviewed.json`; later edits get stamped with the sync date (HST). The source count is the number of unique external citation links on the page (nav, footer, help and share links are excluded).
- **Related Solutions** (4 cards) before "Next: Explore Another Solution". Each page vector is the normalized mean of its bge-small-en-v1.5 chunk vectors plus its title/description chunk, read from the committed semantic index. build-search.mjs now strips these UI blocks so they don't feed back into search. Related cards use the previous build's index, which is fine because they lag by at most one sync.
- **Difference strip** under the homepage hero and at the top of About ("From the ocean floor to low Earth orbit, solutions minus the doom."). The solution and hub counts come from the hub pages, the same rule as Solutions.html, and translations are kept for all 4 languages.
- **Videos:** savingplanets-ad-v2.mp4 went from 36.2 MB to 17.2 MB and grace-fo-satellites.mp4 from 18.8 MB to 7.9 MB. Both are H.264 High, yuv420p, +faststart, SSIM about 0.98, same filenames. Removed unused files: savingplanets-ad.mp4 (no references), channel-intro.mp4 and channel-intro.jpg. build-home-extras.py no longer re-inserts the old channel intro on About; before this fix, the weekly sync would have brought it back.
- Possible follow-up: merge "Next: Explore Another Solution" (hand-picked links) into Related Solutions to avoid two "more" lists.

## Structured Data & robots.txt - Oct 13
- **JSON-LD:** `scripts/seo-jsonld.py` runs automatically at the end of `seo-fix.run()`, so weekly-sync and i18n-build keep it. It is idempotent and rewrites the existing blocks rather than duplicating them.
  - Solution pages (84 × 4 languages): Article with headline, description, inLanguage, url, mainEntityOfPage, image and datePublished. dateModified = Last reviewed (`assets/data/reviewed.json`). author and publisher = Organization "Saving Planets" (logo `assets/SavePlanetLogo.jpg`). citation[] = the page's source links. isPartOf = the hub CollectionPage; about = the solution and its hub.
  - BreadcrumbList is now localized: fr/es/ar names and item URLs point to that language's pages (they used to point to English).
  - Hubs (10): CollectionPage with hasPart listing their solutions.
  - Homepage: Organization (raster logo) + WebSite SearchAction (`/Search.html?q={search_term_string}`, localized per language).
  - Glossary: DefinedTermSet with every term. Teachers: CollectionPage with mainEntity LearningResource (teacher audience, free).
  - No person names anywhere; the Organization is the author.
  - Validation: all blocks parse as JSON, required fields are present, and inLanguage matches the folder (checker script, 0 issues). seo-audit total is unchanged.
- **robots.txt** (it already existed; extended it): Allow all, Disallow the semantic index blobs, /node_modules/, /scripts/ and /.cache/, plus the Sitemap line. The Pages deploy uploads the repo root, so robots.txt ships with it.
- **Follow-ups (owner):** submit sitemap.xml in Google Search Console and Bing Webmaster Tools. Run Google's Rich Results Test (https://search.google.com/test/rich-results) on a solution page, a hub, the Glossary and the homepage, and on one Arabic page.

## Organic Discovery Plan - Oct 13
Full research is in docs/organic-discovery-plan.md. Current technical SEO (hreflang, sitemap, JSON-LD, robots.txt) is enough for all crawler engines. What's missing is verification + IndexNow.
Next actions: (1) User: Google Search Console via Cloudflare DNS TXT + submit sitemap; (2) User: Bing Webmaster (import from GSC; covers Yahoo/DDG/most of Ecosia/Qwant); (3) Repo: IndexNow key file + ping script in weekly-sync (proposal); (4) User: Cloudflare Crawler Hints on, check bot settings; (5) User: Brave submit-url; (6) OER Commons + Curlie (EN/FR/ES/AR) + TES/Procomún teacher sheets; (7) Yandex optional.
Not applicable: Google Scholar/BASE/CORE/Semantic Scholar (non-scholarly). Later, once a registered org or press coverage exists: Wikipedia/Wikidata, UN SDG, Candid.
