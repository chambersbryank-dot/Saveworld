# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

> Working file for Chief of Staff + Grok only. Keep lean: last 24h, next/open, reference. Long detail goes in docs/ and gets a one-line link.
> Archives: full history to Oct 12 midday → docs/notes-archive-2026-10-12.md (restored; 8987d81 had wiped NOTES to 28 bytes). Search/IA/hero detail + test tables → docs/search-and-ia-notes.md. Discovery research → docs/organic-discovery-plan.md.

## Last 24h (Oct 12–13 HST)
- **Search** (1cfa5c1 → 31aaba1): Pagefind keyword + in-browser semantic (bge-small-en) on Search.html; hero "Search Saving Planets" over ocean/Earth/nebula bg; results only on Enter, top 5 + Show more + refine hint; 12 floating best-practice questions (search/featured-questions.json — never label "popular"); `?q=` deep links; key-term retry for 0-hit long queries; newsletter block off on Search only; 2-line credits (d3c8ef3); GA4 `search` event.
- **Solutions.html** directory (7da53ce, 3e39335, 093f635, 9b57735): hubs A–Z, 84 cards, search bar filters cards, (Top) links, left-aligned hub titles + synopsis/impact/links per hub; long nav dropdown removed (plain "Solutions" link).
- **Batch B** (08273c6): ELI10 boxes, Glossary (27 terms) + tap definitions, homepage Start Here row, Cite This Page, teacher print sheets + Teachers.html.
- **Batch A** (3322291, 5f996c5): share bars (96 pages), Last reviewed + sources count, 4 Related Solutions, "what makes us different" strip (home + About), videos compressed (ad 36→17 MB, GRACE-FO 19→8 MB), removed savingplanets-ad.mp4 + channel-intro.
- **Contacts**: media@savingplanets.com (Press), partners@savingplanets.com (About#partner), new Contact cards; hello@/ideas@ kept.
- **Ad v2** posted via Postiz (X/TikTok/YouTube) + featured on About; GA4 G-ZCJ7CEKN94 on every page (Consent Mode v2).
- **SEO** (fc2a4f5, 46117d7): JSON-LD via scripts/seo-jsonld.py (Article+citations on solutions, CollectionPage hubs, Org+WebSite SearchAction, DefinedTermSet, LearningResource; no person names); robots.txt with Sitemap + disallows.
- **Organic discovery plan** (0dffe5a): docs/organic-discovery-plan.md. Tech SEO is sufficient; missing = verification + IndexNow wiring.
- Site review: distinctive combination, not "the only one" — claim the combination, never uniqueness.

## Next / Open
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

**Open decisions**
- Merge Related Solutions with "Next: Explore Another Solution" (two "more" lists now).
- Homepage "minus the doom" appears in strip and headline — shorten one.
- Rewrite ELI10 in truly simple language (assets/data/eli10.json overrides) for most-visited pages.
- Hub/solution pages lacking "How This Saves People & the Planet" section — add when touched (people+nature rule).
- Tsunami early-warning page: ON HOLD (no page mentions "tsunami"; would fix tsunami queries; NOAA DART, SWOT, Sentinel-6).
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
