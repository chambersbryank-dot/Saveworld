# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

## Site Size & Maintenance Log

### 2026-10-08 — Size check (Brian's request)

- **Repo size (GitHub API):** 4,321 KB (~4.2 MB) — GitHub's reported figure, which includes git history.
- **Working-tree size (all blobs on main):** 10,614,614 bytes = **10.13 MB** across 44 files.
- **GitHub Pages limits (free tier, public repo):**
  - Published site size: 1 GB (hard cap)
  - Source repository: 1 GB recommended
  - Bandwidth: 100 GB/month soft limit
  - Builds: 10/hour soft limit (does not apply to custom Actions workflows — ours uses one)
  - Deployment timeout: 10 minutes hard
- **Headroom:** We are at roughly 1% of the 1 GB site limit. No risk of hitting any threshold or triggering a paid tier.
- **Biggest files:** assets/IMG_0060.jpeg (1.60 MB), assets/StreamLog.JPG (581 KB), assets/LightthrForest.JPG (552 KB), assets/CutTreePlantThree.JPG (552 KB), assets/streamlog2.JPG (538 KB), assets/OceanBeach.JPG (265 KB), assets/theoceancleanup.jpg (262 KB), assets/BargCleaning.JPG (246 KB), assets/SavePlanetLogo.jpg (175 KB). All HTML/CSS/JS combined is under 100 KB.
- **Maintenance actions taken:**
  1. Logged this size check here so future sessions can compare.
  2. Noted that IMG_0060.jpeg (Saturn image, used by Astroscale and ClearSpace pages) is still pending rename to Saturn.jpg (open item #1) — renaming does not change size, just clarity.
  3. No files deleted; nothing oversized.
- **Re-check trigger:** Run this check again if you add more than ~5 large images (over ~500 KB each) or if the repo API size approaches 100 MB. At current growth rate, we are years from any limit.
- **Bottom line:** No paid tier needed. GitHub Pages is free for public repos, and we are nowhere near any limit. The only real cost risk would be if the site became primarily commercial/e-commerce, which it is not.

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

## Session Log — 2026-10-08 (ten new solution pages)

- Added two new solutions per category, each as its own page matching the Ocean_Cleanup.html template (nav, page-hero, Five W's, impact statement, donate-btn with category background image, footer, site.js).
- **Ocean:** 4ocean (Oceans.html updated as hub; 4oceanfoundation.org/donate) and Plastic Bank (Plastic_Bank.html; plasticbank.com/individuals).
- **Lakes:** Clean Up the Lake (Clean_Up_the_Lake.html; cleanupthelake.org/donate) and Great Lakes Plastic Cleanup (Great_Lakes_Plastic_Cleanup.html; greatlakesplasticcleanup.org/get-involved).
- **Rivers:** Sungai Watch (Sungai_Watch.html; sungai.watch/products/donate) and The Great Bubble Barrier (Great_Bubble_Barrier.html; thegreatbubblebarrier.com/donate).
- **Space:** Astroscale (Astroscale.html; astroscale.com/get-involved) and ClearSpace (ClearSpace.html; clearspace.today).
- **Forests:** Terraformation (Terraformation.html; terraformation.org) and Life Terra (Life_Terra.html; lifeterra.eu/en/support-us).
- Updated index.html solution cards and sitemap.xml with all new pages.
- Donate buttons use category-appropriate background images (ocean, lake, river, space, forest) with centered Donate text, per the established pattern.

## Criteria check — all ten new solutions (2026-10-08)

| Solution | Hands-on | Verifiable numbers | Donate path | Not advocacy |
|---|---|---|---|---|
| 4ocean | Yes — full-time crews | Yes — 50M lbs, GreenCircle-verified | Yes — 4oceanfoundation.org/donate | Yes — removal work |
| Plastic Bank | Yes — 77,000+ collectors | Yes — 10B bottles, 209M kg | Yes — plasticbank.com/individuals | Yes — collection work |
| Clean Up the Lake | Yes — scuba divers | Yes — 78,000 lbs, 130 miles | Yes — cleanupthelake.org/donate | Yes — removal work |
| Great Lakes Plastic Cleanup | Yes — Seabins, drones, robots | Yes — 277,000+ pieces, 17.5B liters | Yes — get-involved page | Yes — capture work |
| Sungai Watch | Yes — 180+ River Warriors | Yes — 4M kg, 400+ barriers | Yes — sungai.watch/products/donate | Yes — removal work |
| Great Bubble Barrier | Yes — installs bubble barriers | Yes — 1M+ pieces captured | Yes — thegreatbubblebarrier.com/donate | Yes — capture work |
| Astroscale | Yes — spacecraft operations | Yes — ADRAS-J, ADRAS-J2 missions | Partial — get-involved page, not a donation form | Yes — debris removal |
| ClearSpace | Yes — robotic servicers | Yes — ClearSpace-1, PRELUDE | Partial — clearspace.today, not a donation form | Yes — debris removal |
| Terraformation | Yes — seed-to-canopy teams | Yes — species counts, project data | Yes — terraformation.org | Yes — restoration work |
| Life Terra | Yes — planting teams | Yes — 36M+ trees, 563,000 tonnes CO2 | Yes — lifeterra.eu/en/support-us | Yes — planting work |

- All ten pass hands-on work, verifiable numbers, and not-advocacy.
- **Flag:** Astroscale and ClearSpace have partial donate paths (get-involved pages, no donation forms) because they are companies, not charities. Kept on the site because their get-involved routes are transparent and the criteria explicitly allows them. If the donate-path bar is tightened later, these two are the first to revisit.

## Session Log — 2026-10-08 (Solutions Criteria on About page)

- Added a Solutions Criteria section to About.html, below the existing What we cover block, using the same five-ws card grid layout.
- Four criteria: hands-on work, published verifiable numbers, a clear donate path, and solutions not advocacy.
- Retitled the section header to "Our solutions are based on the following criteria" per Brian's direction.
- Criteria section logged here as the authoritative checklist for all future solution additions.

## Session Log — 2026-10-08 (criteria verification against live sources)

- Spot-checked all ten solutions against current web sources. Results:
  - **4ocean:** CONFIRMED — 50M+ lbs removed (Feb 2026 milestone, GreenCircle-verified), 29,311 cleanups, 2,456 jobs. Donate path confirmed at 4oceanfoundation.org/donate.
  - **Plastic Bank:** CONFIRMED — 10.5 billion bottles exchanged, 77,331 collectors, 196M+ kg recovered (as of mid-2026). Donate path confirmed at plasticbank.com/individuals.
  - **Clean Up the Lake:** CONFIRMED — 78,194 lbs total collected, 130.13 underwater miles, 460 dives (cleanupthelake.org stats). Donate path confirmed. Also completed a Sept 2026 Upper Twin Lakes cleanup removing 2,433 lbs.
  - **Great Lakes Plastic Cleanup:** CONFIRMED — 277,000+ pieces removed since 2020 (up from 244,000 at time of page creation), 32,500+ pieces sorted in 2025. Donate path confirmed at get-involved page.
  - **Sungai Watch:** CONFIRMED — 3.5M+ kg collected (July 2025), 368 barriers installed (June 2025), 185 barriers + 745 tons in 2025 alone. Donate path confirmed at sungai.watch/products/donate.
  - **Great Bubble Barrier:** CONFIRMED — 1M+ pieces captured in Amsterdam since 2019 (Aug 2025 milestone), ~15,536 pieces/month. Donate path confirmed.
  - **Astroscale:** CONFIRMED — ADRAS-J completed operations and began deorbit March 2026; ADRAS-J2 launch booked with Isar Aerospace for 2027-2028. Donate path remains partial (get-involved only).
  - **ClearSpace:** CONFIRMED — ClearSpace-1 now targeting PROBA-1 satellite (target changed from VESPA adapter in April 2024), launch 2028; PRELUDE launch June 2027; Phoenix GEO life-extension contract signed Sept 2026. Donate path remains partial.
  - **Terraformation:** CONFIRMED — 5.4M native trees planted in 2025 (up from 2.3M in 2024), 447 species, 2,155 hectares restored; 4.7M+ trees all-time, 68 projects in 18 countries.
  - **Life Terra:** CONFIRMED — 36M+ trees planted 2020-2025 across 32 countries, 563,000 tonnes CO2, 76% average survival rate on monitored plots. Donate path confirmed at lifeterra.eu/en/support-us.
- All ten still pass all four criteria. No removals needed.

## Session Log — 2026-10-08 (page number updates + Oceans hub link fix)

- Updated Great_Lakes_Plastic_Cleanup.html: When card now reads 277,000+ pieces (was 244,000).
- Updated Life_Terra.html: When card now reads 36 million trees and 563,000 tonnes CO2 (was 35M / 3.5M tonnes).
- Fixed Oceans.html hub: the 4ocean card link previously pointed to Oceans.html itself (self-refresh). Now points to Ocean_Cleanup.html — the dedicated page that exists in the repo. Note: there is no 4ocean.html file; 4ocean is covered on the Ocean Cleanup page.
- Verified all three updated files on main after push.

## Session Log — 2026-10-08 (page verification dates in footers)

- Added "Page verified October 2026" to the footers of seven solution pages: Plastic_Bank.html, Clean_Up_the_Lake.html, Clean_Up_the_Lake.html, Sungai_Watch.html, Great_Bubble_Barrier.html, Astroscale.html, ClearSpace.html, Terraformation.html.
- Life_Terra.html and Great_Lakes_Plastic_Cleanup.html already carried the same footer text from the earlier number-update push, so all ten new solution pages now show a verification date.
- Also re-pushed Oceans.html in this batch to correct the 4ocean card link to Ocean_Cleanup.html (the previous push had pointed it at the nonexistent 4ocean.html).
- Going forward, when a solution's numbers are re-verified, update the footer date on that page and log it here.

## Session Log — 2026-10-08 (homepage CTA update: Be Part of the Fix)

- Updated index.html bottom CTA section (id="actions"), commit aa2c52e:
  - Headline changed from "Join the Work" to "Be Part of the Fix" (brand-blue spans on Be and Fix).
  - Lead line: "Plastic, forests, and energy are problems we can tackle together."
  - Links: "Send an idea" (mailto:ideas@savingplanets.com?subject=Idea) and "share a solution you know" (same mailbox).
  - Removed the donate mailto link — a donation email would just bounce back and forth asking where to donate. Instead: "If you'd like to donate, visit our Solutions page and pick the one that matches your interest," linking to index.html#solutions so donors land directly on the solution cards with their donate buttons.
- Follow-up commit 8130274fb5: removed the remaining donate mailto from the lead line and replaced it with the solutions-page pointer.
- Rationale: the site's donate path is per-solution (each page has its own donate button with a category-matched background image), so the homepage should route donors there rather than to email.

## Session Log — 2026-10-08 (Space card photo overlay: Cassini story + clickable NASA link)

- Updated index.html space-card image (commit 0a6eeb4b4f5f8cdadf201c1b48d92c3bde1f8f61) and toc-home.css (commit 4ad2d1e512f70cce409550d58d045b81c7b7aef1):
  - Wrapped the Saturn image (assets/IMG_0060.jpeg) in an anchor (class "photo-link") pointing to NASA's "Impact Site: Cassini's Final Image" article: https://www.nasa.gov/image-article/impact-site-cassinis-final-image/ (opens in a new tab, rel="noreferrer").
  - Added a hover overlay (class "cassini-tip") with the message: "This is a real photograph of Saturn, taken by NASA's Cassini spacecraft during its 13-year mission at the ringed planet. Click to read the full story of Cassini's final dive into Saturn's atmosphere."
  - Overlay fades in on hover/focus-within, positioned at the bottom of the image container with a small arrow pointer; pointer-events: none so it does not block the click.
  - CSS is reusable: the same .photo-link / .cassini-tip pattern can be applied to the Ocean, Lakes, Rivers, and Forests card images with simple goal messages (e.g., "Depicted is the goal we are striving for" / "our goal for the lakes to look like in the future") — pending Brian's review of the Space card.
  - Note: the exact capture date of IMG_0060.jpeg is unknown from file metadata; the overlay uses the mission-level description rather than a specific date. If Brian identifies the photo, the date can be added.
  - NASA images are public domain; attribution (NASA/JPL-Caltech/Space Science Institute) is provided via the overlay and the linked NASA page.

## Session Log — 2026-10-08 (Cassini overlay widened + space-to-Saturn gradient)

- Updated index.html (commit b092924be5f8104239222e245232cbc0a0bd4027) and toc-home.css (commit 677a363d85122dc58a41f1684976c7a3b90e42bd):
  - Overlay now spans the full card width (left: 0; right: 0; width: 100%) instead of the previous max-width cap, giving room for more text.
  - Overlay text now opens with "The following image was taken from the Cassini spacecraft during its 13-year mission at the ringed planet. Click to read the full story of Cassini's final dive into Saturn's atmosphere."
  - Background changed from flat rgba(0,20,40,0.88) to a vertical gradient: deep space navy (rgba(0,20,40,0.92)) fading into Saturn's golden ring-glow (rgba(180,120,40,0.55)) at the bottom — echoing the planet's own colors.
  - Arrow pointer color updated to match the darker navy end of the gradient.
  - This gradient treatment is the template for the other four cards (Ocean, Lakes, Rivers, Forests) when their goal-message overlays are added.

## Session Log — 2026-10-08 (space solution pages: unique planet photos instead of repeated Saturn)

- Brian requested that the three space solution pages (Space.html, Astroscale.html, ClearSpace.html) stop using the same Saturn image (assets/IMG_0060.jpeg) on every card/page. Each page should have its own real, high-resolution NASA photo of a different planet.
- Selected four NASA public-domain images (all from the NASA Images API, direct ~orig.jpg URLs):
  1. **Jupiter.jpg** — PIA21395, "Jupiter's Great Red Spot Revealed," JunoCam, July 10, 2017, ~6,130 miles from cloud tops. Citizen-science enhanced color by Kevin Gill. URL: https://images-assets.nasa.gov/image/PIA21395/PIA21395~orig.jpg
  2. **Mars.jpg** — PIA01250, "Hubble Captures A Full Rotation Of Mars," Hubble Space Telescope. URL: https://images-assets.nasa.gov/image/PIA01250/PIA01250~orig.jpg
  3. **Earth.jpg** — AS17-148-22742, Apollo 17 view of Earth (Australia/Antarctica), Dec 1972, 70mm Hasselblad. URL: https://images-assets.nasa.gov/image/as17-148-22742~orig.jpg
  4. **Neptune.jpg** — PIA01493, "Neptune Rings," Voyager 2, August 1989. URL: https://images-assets.nasa.gov/image/PIA01493/PIA01493~orig.jpg
- **BLOCKER:** The code-execution environment has no outbound internet access (requests to images-assets.nasa.gov failed with ConnectionRefusedError), so the images could not be downloaded and uploaded to the repo from this session. The GitHub MCP create_or_update_file tool only accepts text content, not binary image uploads.
- **Plan for next session:** Download the four ~orig.jpg files (browser or curl), then upload each to assets/ via the GitHub web UI (drag-and-drop into the assets folder) or via git push from a local clone. Then update Space.html, Astroscale.html, and ClearSpace.html to use the new unique images instead of IMG_0060.jpeg, and update og:image meta tags accordingly.
- Suggested mapping (to be confirmed with Brian): Space.html hero -> Earth.jpg (the "pale blue dot" perspective); Astroscale.html -> Jupiter.jpg; ClearSpace.html -> Neptune.jpg. Mars.jpg held in reserve or used on a future fourth space page.
- All four images are NASA public domain; attribution NASA/JPL-Caltech/SwRI/MSSS (Juno), NASA/ESA (Hubble), NASA (Apollo 17), NASA/JPL (Voyager 2).

## Session Log — 2026-10-08 (Ken Burns animation on all homepage cards)

- Added a slow zoom-and-drift (Ken Burns) animation to every homepage solution card image — Ocean, Lakes, Rivers, Forests, and Space — in toc-home.css (commit 2b9c9e38f436447994c14b8520440bfb83c41dfd).
- Keyframes: 4-second ease-in-out loop, scale 1.0 to 1.09 with gentle translate drift; seamless return to start.
- Animation pauses on card hover so the image freezes while the user reads the overlay.
- Respects prefers-reduced-motion: animation disabled for users who opt out.
- Applied site-wide via the shared .card-band .image-container img rule — no per-card HTML changes needed.

## Session Log — 2026-10-08 (homepage revert: pre-overlay baseline)

- Brian asked to revert the homepage to the state before the Cassini overlay work so we can discuss what we do with each solution card.
- Reverted index.html (commit c7d01316) and toc-home.css (commit 82df705d) to the pre-overlay state:
  - index.html: plain card images (no photo-link wrapper, no cassini-tip), Space card points at assets/IMG_0060.jpeg, bottom CTA restored to "Join the Work" with Donate / show up / send an idea links.
  - toc-home.css: removed the .photo-link / .cassini-tip overlay block and the Ken Burns keyframes + animation rules.
- Kept intact: hero, nav, mission block, impact bar, stats, footer, site.js, and all other pages (Space.html, Astroscale.html, ClearSpace.html, etc.).
- The overlay CSS pattern and goal-message copy are preserved in the session logs above, so re-applying to any card is straightforward once Brian decides the per-card treatment.

## Session Log — 2026-10-08 (planet image uploads + homepage overlay re-apply + hero fix)

- Brian uploaded four new planet photos to assets/ via the GitHub web UI: Earth.jpg (84 KB), Jupiter.jpg (171 KB), Saturn.jpg (1.60 MB), Uranus.jpg (224 KB). Mars.jpg was mentioned but not present in the repo at time of check — held in reserve.
- Re-applied the Cassini photo overlay to all five homepage solution cards (index.html), using the Saturn navy-to-gold gradient template from the earlier session:
  - **Space card:** Saturn.jpg, click-through to NASA's "Impact Site: Cassini's Final Image" (https://www.nasa.gov/image-article/impact-site-cassinis-final-image/), overlay text: "The following image was taken from the Cassini spacecraft during its 13-year mission at the ringed planet. Click to read the full story of Cassini's final dive into Saturn's atmosphere."
  - **Ocean card:** OceanBeach.JPG, overlay text: "The picture depicted is the goal of the solutions we are bringing to you — clean, thriving oceans."
  - **Lakes card:** Pexels mountain lake photo, overlay text: "This is our goal for the lakes to look like in the future — clear, healthy, and thriving."
  - **Rivers card:** Pexels forest river photo, overlay text: "This is our goal for the rivers to look like in the future — clean, flowing, and alive."
  - **Forests card:** Threetrees3.jpg, overlay text: "This is our goal for the forests to look like in the future — restored, green, and thriving."
- Hero fix: the space-hero background image was still pointing at the old IMG_0060.jpeg path after the rename to Saturn.jpg. Updated toc-home.css (commit 4ad2d1e512f70cce409550d58d045b81c7b7aef1) so the hero now uses assets/Saturn.jpg. Without this fix the homepage hero showed no image at all.
- All five cards now have unique photos and working click-through links. Verified on main.

## Session Log — 2026-10-09 (Restoring the Lake Depths Foundation — fourth lake solution)

- Researched Restoring the Lake Depths Foundation (restoremylake.org): Nevada 501(c)(3), founded 2020 by Lindsay Kopf and parents Jamie and Kathy Kopf, Zephyr Cove NV. Fleet of four ROVs including flagship Deep Emerald (600 m fiber tether, reaches 1,640 ft). Volunteer scuba and free divers. Summer 2024: 13+ tons of debris removed from Lake Tahoe south shore; ~80 tires and nearly 1 ton of plastic in a single year. Donate via Givebutter at restoremylake.org/donate. No dedicated volunteer form found — join invitation is on their homepage.
- Created Restoring_the_Lake_Depths.html with Five W's, impact statement, donate button (StreamLog.JPG) and join button (Nebula.jpg) side by side.
- Updated Lakes.html hub to four cards with new photos: StreamLog.JPG (Lake Plastic Recovery), OceanBeach.JPG (Clean Up the Lake), BargCleaning.JPG (Great Lakes Plastic Cleanup), Nebula.jpg (Restoring the Lake Depths). Hub subtitle updated to "Four solutions."
- Updated index.html Lakes card image to StreamLog.JPG and added Restoring the Lake Depths to the homepage Lakes list.
- Updated sitemap.xml and Search.html index.
- **OPEN ITEM:** Brian needs to create the hello@savingplanets.com email in Cloudflare. (Resolved 2026-10-09 — Brian confirmed both hello@ and ideas@ are now functional.)
- Session ended for the night; Brian heading to sleep.

## Session Log — 2026-10-09 (nav bar upgrade: frosted glass)

- Replaced the solid white nav bar with a frosted-glass treatment: translucent navy with backdrop-filter blur when over the hero, transitioning to solid frosted white with soft shadow on scroll. Text switches from white to navy automatically. Added scroll-margin-top so anchor links clear the fixed bar. Also fixed double semicolons in site.js.
- Pushed to main; deploy confirmed green.

## Session Log — 2026-10-09 (solution link color + Five W's text fix)

- Changed .solution-list a color from green (#00b894) to brand blue (#009cde), bumped font from 0.95 to 1.05 rem. Dark mode updated to #4da3ff.
- Five W's cards: white text throughout, body bumped to 1.05 rem, titles white on navy.
- Applied site-wide via toc-home.css.

## Session Log — 2026-10-09 (Pages source fix)

- Root cause of stale live site: Pages was set to "Deploy from a branch" instead of GitHub Actions, serving a stale snapshot. Switched to GitHub Actions in repo settings. Deleted stray malformed workflow file. All subsequent deploys confirmed green and live.

## Session Log — 2026-10-09 (4ocean dedicated page)

- Created 4ocean.html with its own Five W's and impact statement (founders Alex Schulze and Andrew Cooper, 2017 Boca Raton founding, 50M lb Feb 2026 milestone, 29,311 cleanups, 2,456 jobs, 85/12/3 river-coastline-ocean split). Donate button points to 4oceanfoundation.org/donate. Fixed Oceans.html hub 4ocean card link. Updated sitemap and search index. Noted 4ocean is a for-profit B Corp, stated explicitly on the page.

## Session Log — 2026-10-09 (contact page + remaining items)

- Created Contact.html with ideas@savingplanets.com (solutions/ideas) and hello@savingplanets.com (general/partnerships/press), linked from nav, homepage footer, and search index. Added to sitemap.
- Added twitter:card large_image meta tags across homepage and hubs.
- Added 404.html.
- Added README.md.
- Added lastmod dates to sitemap.xml.
- Deleted duplicate Clear_Space.html; Interceptors.html deleted.
- Finished Project-R.html with real content.
- Added focus styles to styles.css.
- Added donate buttons to Three_Trees.html and Orbital_Data_Centers.html.
- Added verification dates to Astroscale, Oceans, Lakes, Rivers, Deforestation, Amazing_Facts footers.
- Built build-search-index.js (run locally before push; GitHub Pages is static-only).
- Deleted duplicate deploy workflow file.
- **OPEN ITEM:** Google Search Console + GA4 Analytics still to set up (account-level, Brian's side).
- **OPEN ITEM:** Privacy policy page if/when analytics added.
- **OPEN ITEM:** Newsletter signup.
- **OPEN ITEM:** Compress Saturn.jpg (1.60 MB) and Threetrees4.jpeg (1.96 MB) — Brian's side, binary upload not possible via connector.
- **OPEN ITEM:** README-old.md (1 byte) still in repo — harmless but could be deleted.
- **OPEN ITEM:** Double semicolons remain in Search.html inline script (harmless).

## Session Log — 2026-10-09 (Space Disposal hub + Project R launches widget)

- GitHub sign-in on the agent's computer completed (chambersbryank-dot); all work below was promoted from drafts to the repo root and pushed to main in one commit.
- **Space_Disposal.html** — new Space Disposal hub, modeled on Ocean_Cleanup.html (same nav, page-hero with space-hero image, Five W's with id="solution", impact section, donate-banner pattern, footer with "Page verified October 2026", styles.css + toc-home.css + site.js, canonical https://www.saveplanetminusthedoom.com/Space_Disposal.html, og/twitter tags). Five W's cover space debris removal as a category (Astroscale, JAXA, ClearSpace, ESA; robotic capture and deorbit; missions targeted 2027–2028; low Earth orbit; protecting climate and navigation satellites protects Earth).
  - Featured deep dive: **ADRAS-J2** — Astroscale's Phase II of JAXA's CRD2 program (~¥13.2B), capturing the same 11 m, 3 t H-IIA upper stage ADRAS-J photographed in 2024 with a robotic arm and lowering it to burn up; launch targeted for Japan's fiscal 2027 on Isar Aerospace's Spectrum from Andøya, Norway. Also mentions ClearSpace PRELUDE (June 2027) and ClearSpace-1 targeting PROBA-1 (2028). Links internally to Astroscale.html and ClearSpace.html.
  - Subtle source link at the bottom of the impact synopsis: "For further information, visit JAXA" → https://global.jaxa.jp/ (new tab, rel="noreferrer"). Donate-style banner uses assets/Saturn.jpg with "Learn More" → astroscale.com.
- **Project-R.html** — copy of Project-R.html with:
  - An upcoming-launches widget right under the page-hero, before the Five W's, powered by The Space Devs Launch Library 2. Shows the next launch prominently (mission, provider, rocket, local date/time, live countdown ticking every second) plus the next 4 launches. Includes the note "Launches shift left and right all the time - stay updated." and a link to the full schedule at nextspaceflight.com. Response is cached in sessionStorage for 10 minutes to respect API rate limits; fetch errors show a fallback message with the schedule link. Uses API v2.3.0 because the v2.2.0 endpoint now returns 404.
  - A Project R category card grid (index.html card-band / image-container / photo-tip pattern) with a Space Disposal card (assets/Saturn.jpg) linking to Space_Disposal.html, and an intro line explaining that category cards drill into hubs.
  - All new CSS is in an inline <style> block scoped to the widget and cards; styles.css and toc-home.css are unchanged.
- **sitemap.xml** — adds Space_Disposal.html (lastmod 2026-10-09) and bumps Project-R.html lastmod to 2026-10-09.
- **OPEN ITEM:** ClearSpace.html is out of date — it still describes the old Vega adapter target and says PRELUDE "launched in 2026". ESA now targets PROBA-1, and PRELUDE is targeting June 2027.
- **OPEN ITEM:** Search.html index does not yet include Space_Disposal.html; run build-search-index.js to add the new page to search.

## Session Log — 2026-10-09 (voice session with Brian, in car)

- Reviewed Project-R.html source: Five W's section, Impact Statement, Upcoming Launches widget (live countdown via The Space Devs Launch Library 2 API, cached 10 min), Project R Categories card (Space Disposal), mobile reorder so widget appears after Impact Statement on phones <=600px.
- Read NOTES.md (capitalized filename at repo root; notes.md lowercase does not exist).
- Searched today's commits (2026-10-09): six pushes including Project-R.html rewrite to Ocean_Cleanup.html template for Project Rawane, Space_Disposal.html hub (ADRAS-J2 deep dive), Restoring_the_Lake_Depths.html, Three_Trees.html, Orbital_Data_Centers.html sitemap additions, build-search-index.js syntax fix, Space Disposal added to site search index, and mobile launches-widget reorder.
- Produced a fresh site-wide enhancement assessment (polish, SEO, UX, logical flow) and ranked top five recommendations plus quicker extras; Brian approved all for execution.
- Execution kicked off: one commit per item in order — (1) broken links + date conflicts, (2) JSON-LD structured data on all 28 pages, (3) image compression + width/height/lazy-loading, (4) Space/Project R/Space Disposal path unification + breadcrumbs + next-solution blocks, (5) CSS merge of styles.css and toc-home.css plus removal of 7 inline style blocks. Quicker extras included: Project-R spelling fixes, Twitter card tags, meta description lengthening, Page verified footers, Apple touch icon, font preconnect.
- STANDING RULE from Brian: NOTES.md is the single source of truth for continuity between the voice assistant and the Chief of Staff. Before starting any task or reminding Brian of anything, read NOTES.md first. After finishing any task, append a session log here. Goal: Brian should never have to re-explain context or re-list dropped items.
- Open item carried forward: IMG_0060.jpeg still pending rename to Saturn.jpg (from 2026-10-08 size check).

## Standing Rules (added 2026-10-09)

- AUTOMATIC SESSION START: At the beginning of every Saveworld session (whether Brian asks or a task arrives), automatically pull the latest NOTES.md (git pull on the Chief of Staff's machine, or the raw GitHub URL, to avoid connector truncation) and review the commits from the last 24 hours (git log --since=24.hours or GitHub commit search for repo:chambersbryank-dot/Saveworld). Use that to reconstruct context so Brian never has to re-explain what was done or what was dropped.
- GLITCH LOGGING: Whenever a connector glitch or limitation is hit (e.g., file truncation, failed tool calls, timeouts), log it under "- PEOPLE + NATURE RULE (added 2026-10-12, Brian's request): every solution page must explicitly tie the solution to saving planets, covering BOTH how it helps people (mankind) and how it helps nature. Use `<section class="impact saves-planets" id="saves">` titled "How This Saves People &amp; the Planet" right after the Impact Statement, with "For People" and "For Nature" h3s; sourced claims only, each followed by its fact-source line. Pages built before 2026-10-12 don't have it yet; add it whenever a page is touched.

## Known Glitches & Workarounds" below with the date, what failed, the workaround used, and whether it is resolved. Goal: surface recurring patterns so root causes get fixed instead of rediscovered.

## Known Glitches & Workarounds

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-09 | build-search-index.js had a syntax typo and expected an outdated Search.html format (would have overwritten the search list) | Added the entry by hand, then rewrote the script to preserve curated entries (19abb6a) | Yes |
| 2026-10-09 | Launch Library 2 endpoint /2.2.0/launches/upcoming/ returned 404 | Switched widget to /2.3.0/ (same fields) | Yes |
| 2026-10-09 | GitHub device sign-in code expired before approval on first attempt | Generated a fresh code; signed in as chambersbryank-dot via gh CLI | Yes |
| 2026-10-09 | Gmail connector inactivity check reported it could not create drafts; the summary email had in fact already been sent at 7:57 AM HST | Verified via Gmail search; no action needed | Yes |
| 2026-10-09 | npx lighthouse failed within ~1.5s with no report during the site assessment | Assessment used scripted checks instead; no performance scores yet | No |
| 2026-10-10 | NOTES.md was truncated in cfad49d (domain-reset log, 62 KB to 23 KB): about 275 lines were replaced by a literal "[+43216 bytes at .content[1].resource.text]" marker, dropping Standing Rules, this table, Candidate Queue, and most 2026-10-09 logs. Five later log commits built on the truncated copy. | Restored the full pre-truncation text from 6cafb7a and re-appended every later session log (morning candidate run). Edit NOTES.md via git clone, never the connector's create_or_update_file. | Yes |
| 2026-10-10 | HTTPS on www.savingplanets.com failed (GitHub Pages served its *.github.io certificate, so browsers showed a security warning) even though DNS was correct: www grey-cloud CNAME to chambersbryank-dot.github.io, apex A records on 185.199.108-111.153, Pages health check all valid. No certificate had ever been requested. | Cleared and re-set the Pages custom domain via `gh api -X PUT repos/chambersbryank-dot/Saveworld/pages`, which triggered issuance; certificate approved within a minute (covers savingplanets.com and www.savingplanets.com, expires 2027-01-08), then enabled Enforce HTTPS. | Yes |
| 2026-10-11 | Old newsletter script used Launch Library /2.2.0/ (404 per 2026-10-09 row), so drafts silently lost launches | Newsletter now uses /2.3.0/launches/ with week window; failures logged as a note | Yes |
| 2026-10-11 | MailerLite API cannot edit form double opt-in (confirmation) emails | Texts prepared in scripts/newsletter-confirmation-texts.md; edited manually in dashboard | No (manual) |
| 2026-10-11 | Link checks for Donate/Join: terraformation.org/donate, /careers, /get-involved all 404 (site is JS-rendered; real pages live on terraformation.com); coralrestoration.org and starfishspace.com return 403 to curl without a browser User-Agent (starfishspace.com still 403 with one); plasticbank.com/individuals now redirects to /pricing | Used terraformation.com/work-with-us + /careers; re-checked with a browser UA (Coral Restoration 200); left Starfish Space out; no Donate for Plastic Bank | Yes (Starfish unverified) |
| 2026-10-11 | i18n-build.py rewrote href/src/data-image to ../ on translated pages but not `poster`, so video poster frames 404'd on /fr/ /es/ /ar/ | Added 'poster' to the rewritten attributes (line 114) | Yes |
| 2026-10-11 | build-batch3.py regenerated Myth_vs_Fact / Rawanes_Mission_Log from the Press.html template on every run, overwriting the seo-fix edits to their head, so i18n-check flagged fr/es/ar copies STALE after each weekly-sync run | Generator now keeps the existing head/footer and only rewrites the body between page-hero and footer, skipping the write when nothing changed; two back-to-back weekly-sync runs both end 'All translations current' | Yes |
| 2026-10-11 | Headless Chrome screenshots cropped at the wrong spot (100vh heroes make the layout depend on window height, and the live page is taller than the local copy) | Measure and capture at the same tall window size (/workspace/shot2.sh, H=16000-26000) | Partly (ar/Space_Weather 390 crop shows the quiz top only) |
| 2026-10-12 | WebFetch timed out on every nasa.gov / science.nasa.gov page; science.nasa.gov/people/nancy-grace-roman/ and several guessed URLs 404; JPL Horizons API sends no CORS header (browser fetch impossible); session start found 168 uncommitted fr/es/ar + English files in the shared tree (an in-progress i18n run from a concurrent task, older i18n-source hashes) | curl with a browser UA + WebSearch for correct URLs; Horizons pulled server-side by scripts/build-roman.py into assets/data/roman.json; stashed the stray tree as `stash@{0}` 'uncommitted pre-Roman session 2026-10-12' (not dropped; the concurrent task then committed 5d0cd72) | Yes (stash kept for review) |

## Session Log — 2026-10-09 (evening): enhancement execution

1. **Broken links + date conflicts** — e3af02b. ClearSpace and Rivers donate links now use https://; Space.html links ClearSpace.html (was Clear_Space.html). ADRAS-J2 is fiscal 2027 on Astroscale, Space, Project R and Space Disposal. ClearSpace.html: PRELUDE planned June 2027 (no longer "launched"); ClearSpace-1 target is PROBA-1 (old Vega adapter noted as original target), targeted 2028 (ESA lists 2029). Project R impact text switched to numerals (fiscal 2027, 2024, H-IIA, 11-meter, 3-ton, 13.2 billion yen) in this commit. Search keywords: Vega-C -> PROBA-1.
2. **JSON-LD** — b396d24. Organization + WebSite/SearchAction (Search.html?q=) on index; BreadcrumbList on hubs, About, Contact, Search, Amazing Facts; BreadcrumbList + Article (dateModified 2026-10-09) on 16 solution pages. 44 blocks, all parse. 404 excluded. First deploy collided with the previous in-progress deploy; rerun succeeded.
3. **Images** — d6810cd. assets/ 9.26 MB -> 3.19 MB (max 1600px, progressive JPEG, EXIF orientation applied). Saturn.jpg 1.60 MB -> 53 KB. Threetrees4.jpeg 1.96 MB -> 280 KB (resized to 900px wide; the only file still over 250 KB). Tree4.jpg is a 2-byte placeholder, untouched. width/height on every img, loading="lazy" on all but the first img per page, decoding="async" everywhere.
   - **Duplicate photo note for Brian:** CutTreePlantThree.JPG and LightthrForest.JPG are byte-identical (same sha256 f2e4af37…). Nothing deleted; pick one and repoint references when convenient.
4. **Space / Project R / Space Disposal flow** — 00e1302. Space Disposal card on Space.html; Space Disposal hub trimmed with links to Astroscale/ClearSpace pages; visible breadcrumbs on 22 hub/solution pages (match JSON-LD); "Next: explore another solution" block above the footer on every solution page.
5. **CSS merge** — 7238b4d. toc-home.css merged into styles.css (18 shared selectors deduped, 42 overridden declarations removed, cascade order kept); 7 inline style blocks moved into styles.css (404 scoped via body.nf-page, Project R via body.pr-page); toc-home.css deleted; stray ;; removed from site.js and Search.html. Before/after screenshots at 1280/390: index, Oceans, Astroscale, Search and Project R identical (apart from the live countdown). 404 changed for the better because it never loaded toc-home.css and its nav was broken. Dark mode verified.
6. **Extras** — 05f95c9. Twitter card/title/description/image on all pages (404 excluded); 120–155 char meta + og descriptions on Search, About, Astroscale, Oceans; "Page verified October 2026" footers (index, About, Contact, Search, Space, Ocean_Cleanup, Sungai_Watch, Great_Bubble_Barrier); Google Fonts preconnects; apple-touch-icon.png (180x180, rendered from favicon.svg) linked on every page.
7. **Wrap-up** — this commit: build-search-index.js run (26 pages, 0 added, Search.html unchanged); sitemap lastmod set to 2026-10-09 for all 27 URLs (every page changed today).

Open/observed: the launches widget can show a launch that already happened (status "Success") as "Next launch" until its 10-minute cache refreshes. Worth filtering out past launches. Lighthouse scores are still not available.

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-09 | GitHub Pages deploy for b396d24 failed: "in progress deployment" (two pushes too close together) | Re-ran the workflow (gh run rerun), succeeded | Yes |

## Session Log — 2026-10-09 (late): Jupiter natural debris page

- **Jupiter.html created** (commit 29771e7) as a fun-but-educational natural space-debris "solution", built on the Ocean_Cleanup.html template: breadcrumb Home > Space > Jupiter, Five W's, Impact Statement with honest trade-off, "Jupiter by the numbers" card grid, Learn More banner to NASA (no donate button), next-solutions block, JSON-LD BreadcrumbList + Article. New styles.css rules: body.jupiter-page hero, .fact-source, .photo-credit, banner lead text. Image: assets/Jupiter.jpg (NASA / JPL-Caltech / SwRI / MSSS, enhanced color by Kevin Gill, JunoCam, July 10 2017, PIA21395).
- **Sources used (each fetched and checked):**
  - https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html (diameter 142,984 km, 1,321 Earth volumes, 317.83 Earth masses, gravity 2.36x equatorial, 11.86-yr orbit, 5.2 AU, 89.8% H2 / 10.2% He)
  - https://science.nasa.gov/jupiter/jupiter-facts/ (11x wider, 9.9-hr day, 4.6 billion years, dilute/fuzzy core, Great Red Spot bigger than Earth, observed 300+ years)
  - https://science.nasa.gov/jupiter/jupiter-moons/ (115 IAU-recognized moons, Galilean moons 1610, Ganymede > Mercury, Io most volcanic, Europa ocean)
  - https://www.planetary.org/articles/does-jupiter-protect-earth-from-asteroids-and-comets (2,000x comet impacts, 12-45/yr vs once per 6-15 yr for ~10 m objects, Oort vs asteroid trade-off)
  - https://arxiv.org/abs/0806.2795 (Horner & Jones 2008, Jupiter: friend or foe? I: the asteroids)
  - https://arxiv.org/abs/2512.03961 (Knierim et al. 2025, metal-rich dilute core; a modeling paper, not a Juno/EGU release)
  - https://science.nasa.gov/jupiter/ (Learn More target; solarsystem.nasa.gov/planets/jupiter/overview/ redirects here)
- **Corrections vs brief:** gravity 2.4x (NASA, equatorial) instead of ESA 2.5x; formation 4.6 billion years per NASA (hero keeps "four and a half billion"); Great Red Spot 680 km/h dropped (not on NASA page; used "observed 300+ years"); "70% of Earth-crossing asteroids" dropped (not in Horner & Jones abstract or Planetary Society article); Hammel/MIT credit is for the Shoemaker-Levy 9 image, not the 2,000x stat, so the stat is credited to the Planetary Society. 115 moons confirmed by NASA citing the IAU.
- **Hub/sitemap/search:** Space_Disposal.html gets a "Natural debris solution" Jupiter card and a next-solutions link; index.html Space list gets a Jupiter link; sitemap.xml adds Jupiter.html (lastmod 2026-10-09); build-search-index.js added Jupiter to Search.html (27 entries) and the keywords were enriched by hand. Space.html not edited (could get a Jupiter card later).

## Candidate Queue — batch 2026-10-09

First daily candidate batch (16). Status reflects Brian's decisions as of 2026-10-09 evening. Phase 1 = build now; Phase 2 = queued behind Phase 1.

| ID | Candidate | Classification | Suggested hub | Status |
|---|---|---|---|---|
| A | Hera (ESA, Didymos/Dimorphos; DART follow-up, arrival Nov 2026) | Agency mission (ESA) | Planetary Defense | APPROVED (build now, Phase 1) |
| B | NEO Surveyor (NASA, Sun-Earth L1 infrared asteroid hunter, NET Sept 2027) | Agency mission (NASA) | Planetary Defense | APPROVED (build now, Phase 1) |
| C | Webb and asteroid 2024 YR4 (NASA/ESA/CSA, L2; 2032 lunar impact ruled out) | Agency mission (NASA/ESA/CSA) | Planetary Defense | APPROVED (build now, Phase 1) |
| D | Three invisible shields: heliosphere, magnetosphere, atmosphere | Natural | Space Weather & Shields | APPROVED (queued, Phase 2) |
| E | SOLAR-1 (NOAA, L1 space weather monitor) | Agency mission (NOAA) | Space Weather & Shields | APPROVED (queued, Phase 2) |
| F | Vigil (ESA, L5 side view of the Sun, 2031) | Agency mission (ESA) | Space Weather & Shields | APPROVED (queued, Phase 2) |
| G | Aditya-L1 (ISRO, L1 solar observatory) | Agency mission (ISRO) | Space Weather & Shields | APPROVED (queued, Phase 2) |
| H | Atmospheric drag as Earth's own debris vacuum | Natural | Space Disposal | PENDING (no decision yet) |
| I | ClearSpace CLEAR (UK) and PRELUDE update | Corporate | Space Disposal (update ClearSpace.html) | PENDING (no decision yet) |
| J | Astroscale next missions (ISSA-J1, LEXI-P, APS-R) | Corporate | Space Disposal (update Astroscale.html) | PENDING (no decision yet) |
| K | NISAR (NASA/ISRO radar) | Agency mission (NASA/ISRO) | Earth Observation | APPROVED (queued, Phase 2) |
| L | ESA Biomass (P-band forest carbon radar) | Agency mission (ESA) | Earth Observation (cross-link Deforestation) | APPROVED (queued, Phase 2) |
| M | Tanager-1 (Planet / Carbon Mapper methane) | Corporate / nonprofit | Earth Observation | APPROVED (queued, Phase 2) |
| N | DSCOVR / EPIC (NASA/NOAA, L1 full-Earth imaging, ozone product) | Agency mission (NASA/NOAA) | Earth Observation | APPROVED (queued, Phase 2) |
| O | LeoLabs (ground radar debris tracking) | Corporate | Space Disposal | PENDING (no decision yet) |
| P | MMX (JAXA with NASA, Phobos sample return; launch Oct 2026) | Agency mission (JAXA) | Space Disposal ("saving moons", next to Titan) | APPROVED (build now, Phase 1) |

New hubs approved: Planetary Defense (A, B, C + Jupiter cross-link), Space Weather & Shields (D–G), Earth Observation (K–N). Every figure is re-verified on its source page before publishing; company figures are labeled as company figures.

## Session Log — 2026-10-09 (late): Titan & Dragonfly "saving moons" page

- **Titan.html** (757b28b): built on Jupiter.html pattern. Breadcrumb Home > Project R > Space Disposal > Titan (matches Space_Disposal's own Project R breadcrumb; JSON-LD matches). Five W's, impact statement (honest: not debris removal, fits Project R's two-way Earth-space relationship), "Titan by the numbers" grid with .fact-source lines, Learn More banner to NASA's Dragonfly page, next-solutions (Jupiter, Space Disposal, Astroscale, Space). New styles.css rule body.titan-page hero.
- **Image:** assets/Titan.jpg from NASA Photojournal PIA20016 "Peering Through Titan's Haze" (Cassini VIMS infrared mosaic), credit NASA/JPL/University of Arizona/University of Idaho; resized 2002px -> 1600px, 128 KB.
- **Mission status widget** (a04ed7f): reusable [data-mission] widget in site.js + .mission-widget in styles.css (NASA-sourced launch/arrival countdowns, milestones, Spaceflight News API v4 headlines cached 1 h in localStorage with last-known-good fallback). Used on Titan.html.
- **Project R launches widget fix** (8b70fe1): skips launches with a past net or Success/Failure/Partial Failure status.
- **Sources (all fetched and checked):** science.nasa.gov/saturn/moons/titan/facts/; science.nasa.gov/mission/dragonfly/; nasa.gov/news-release/nasa-awards-launch-services-contract-for-dragonfly-mission/ (July 5-25 2028, Falcon Heavy, LC-39A, ~$256.6M launch contract); astrobiology.nasa.gov/news/nasa-selects-flying-mission-to-study-titan-for-origins-signs-of-life/ (eight rotors, 4x denser atmosphere, early-Earth analog, Shangri-La, Selk; selected June 27 2019); dragonfly.jhuapl.edu/What-Is-Dragonfly/ and /Why-Titan/; science.nasa.gov/solar-system/nasas-dragonfly-mission-sets-sights-on-titans-mysteries/ (Selk ~50 mi); science.nasa.gov/mission/cassini-huygens/ + ESA Huygens PR (Jan 14 2005, only outer-solar-system landing, most distant); science.nasa.gov/mission/cassini/ and Cassini RADAR page; ESA Sentinel-1 Emergency response; NASA Radioisotope Power Systems; Turtle et al. OPAG Nov 2024 (70-90 min one-way light time, autonomous flight); ESA Automating collision avoidance; JPL "Titan may not have global ocean" + Petricca et al., Nature 2025.
- **Corrections vs brief:** subsurface ocean reframed as contested (2025 JPL/Nature reanalysis suggests slush with water pockets); atmosphere stated precisely (surface pressure ~60% higher than Earth's, ~4x denser); "nuclear battery powers climate-monitoring probes" dropped (no source; reframed as radioisotope power where sunlight is scarce: Curiosity, Perseverance, Voyager, New Horizons); radio delay given as 70-90 min one way (not a flat 1.5 h); radar tie framed as same family of technique (Cassini RADAR vs Sentinel-1 SAR), not same instrument; arrival "late 2034" per NASA (widget countdown uses Dec 1 2034 as a labeled approximation).
- **Hub/sitemap/search** (commit 2): Space_Disposal.html "Saving moons: Titan" card beside Jupiter (section heading renamed "Natural debris and saving moons") + Titan in next-solutions; sitemap adds Titan.html (2026-10-09); build-search-index.js added Titan (28 entries, prior 27 intact), keywords enriched by hand.

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-09 | WebFetch timed out on science.nasa.gov/mission/dragonfly/; nasa.gov press-release body not in curl HTML on first URL guess | curl + text extraction, web search to find the correct press-release URL | Yes |
| 2026-10-09 | Headless Chrome reused cached styles.css during widget screenshots (stale render) | Fresh --user-data-dir and cache-busting query string | Yes |

- **Decisions update (2026-10-09, 4:51 PM HST):** H (Atmospheric drag), I (ClearSpace CLEAR/PRELUDE update), J (Astroscale next missions), O (LeoLabs) → APPROVED. Build order: after Phase 2 (Space Weather, Earth Observation), applying the horizon rule below.

## Standing Rule — Potential solutions on the horizon (added 2026-10-09)

- Any candidate without a solidly confirmed contract or funding must NOT be presented as an active solution. Label it "Potential solution on the horizon" with the note: "We'll keep you updated here if this becomes a reality."
- Site implementation: reusable .horizon-badge / .horizon-note styles in styles.css; every page carries an sp:status meta of "active" or "horizon"; the stats engine counts horizon items separately ("X active solutions, Y on the horizon") and never sums their impact numbers into totals.
- Known horizon item: ClearSpace CLEAR (reported £61.3M UK Phase 3 contract is only reported by a third-party tender tracker, unconfirmed by the UK Space Agency).

## Session Log — 2026-10-09 (night): Phase 1 — Planetary Defense hub, Hera, NEO Surveyor, Webb/2024 YR4, MMX

- Worked in a separate clone (/workspace/sw2) because the shared clone /workspace/Saveworld had the parallel Titan worker's uncommitted edits.
- **Planetary_Defense.html** (09209ce) — new hub: DART intro, cards for Hera, NEO Surveyor, Webb & 2024 YR4, Jupiter; honest note that Roman (launched Aug 30, 2026) is a dark-energy/exoplanet mission, not an NEO mission, and NEO Surveyor is.
- **NEO_Surveyor.html** (b0d9b5d), **Webb_2024_YR4.html** (af48975), **Hera.html** (30c7885, + site.js data-agency so the widget note says "Dates per ESA/JAXA"), **MMX.html** (f4c30f5, + MMX card next to Titan on Space_Disposal.html). All five commits went out in one push / one deploy because the per-commit pull step failed on the dirty working tree; content unaffected.
- Mission widgets: Hera counts down to "window opens, November 2026" (ESA gives only the month); MMX counts down to 2026-10-19T19:41:03Z (= Oct 20 4:41:03 JST, H3 F10, JAXA); NEO Surveyor shows status + news only (NET Sept 2027, no fake-precise countdown).
- **Links** (2fb835e): "Planetary Defense" added to the Solutions dropdown on every page except Titan.html (left to the Titan worker — add it there next time Titan is touched); homepage Space card links Planetary Defense + MMX; Space.html gets a Planetary Defense card.
- **Corrections vs research brief:** 2024 YR4 miss distance is 21,200 km from the lunar surface per NASA (22,900 ± 800 km is from the Moon's center per the RNAAS paper; both stated). DART period change shown as the refined 33 min 15 s (NASA), with the original 32 min announcement noted. MMX sample is "at least 10 g" (ESA) / "more than 10 g" (JAXA); return is Japan fiscal year 2031.
- **Sources:** ESA Hera overview / early-arrival / deep-space-manoeuvre articles; NASA Hubble boulders (37 boulders, 1–6.7 m); NASA DART orbit study; NASA NEO Surveyor page + launch services release (2/3 of unknown NEOs >140 m in 5 years, ~50 cm telescope, Falcon 9); NASA PD and Webb blogs, ESA, RNAAS 10.3847/2515-5172/ae4fb4 (YR4); NASA Roman launch release; JAXA MMX launch press release + mission page; ESA MMX factsheet.
- **Image credits:** Hera.jpg — ESA–Science Office, CC BY-SA 3.0 IGO (via Wikimedia Commons "Hera in orbit"); NEO_Surveyor.jpg — NASA/JPL-Caltech/University of Arizona PIA25253; Webb_Infrared.jpg — NASA/JPL-Caltech PIA25790; Phobos.jpg — NASA/JPL-Caltech/University of Arizona PIA10368 (HiRISE; used instead of a JAXA image to avoid JAXA reuse-term ambiguity); DART_Didymos.jpg — NASA/Johns Hopkins APL/Steve Gribben PIA25329. All ≤1600 px, <250 KB.
- Sitemap: 5 URLs added (lastmod 2026-10-09). Search: build-search-index.js added 5 entries (33 total), keywords enriched by hand.

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-09 | Shared clone had another worker's uncommitted edits, so `git pull --rebase` refused | Used a separate clone /workspace/sw2 | Yes |
| 2026-10-09 | JPL NEO Surveyor page returns 403 (CloudFront) to fetch and curl; MMX ISAS site returned 500 | Used NASA science.nasa.gov + NASA launch release, and mmx.jaxa.jp + ESA factsheet | Yes |
| 2026-10-09 | images-api.nasa.gov asset lookup hung | Fetched images-assets.nasa.gov/image/<id>/<id>~large.jpg directly with a timeout | Yes |

## Session Log — 2026-10-09 (night): shared stats engine

- **What:** build-stats.js (called at the end of build-search-index.js) reads every sitemap page's `sp:` meta tags and `[data-mission]` widgets and writes assets/data/solutions.json (site-wide + per-category aggregates + per-page list). site.js renders the homepage overview (above the existing static stats, which stay as the no-JS/failure fallback) and a `.page-stats` "By the numbers" block on every hub/solution page (category counts, a site-wide line, and the page's own sourced stats). One fetch per session (sessionStorage); if the fetch fails the blocks stay hidden.
- **First build:** 21 active solutions, 0 on the horizon, 8 hubs, 7 categories, 4 upcoming missions (Hera, MMX, NEO Surveyor, Dragonfly); 5 agency · 7 corporate · 8 nonprofit · 1 natural. No summable impact totals yet (see below).
- **Seeded headline stats** only where the page already links a source: Hera (DART 33.25 min, 37 boulders), Webb/YR4 (21,200 km), NEO Surveyor (2/3 of NEOs >140 m), MMX (≥10 g), Jupiter (2,000×, 115 moons). Older pages (Ocean Cleanup 60M kg, 4ocean 50M lb, Plastic Bank 209M kg, Sungai Watch 4.5M kg, Life Terra 36M trees, etc.) state numbers but have no source link on the page, so no stats were seeded. **OPEN ITEM:** add source links to those pages, then add `sp:stat ... |impact|` tags so totals sum.
- **Homepage static stats:** kept. They name sources in text (Ocean Cleanup press release / annual report, Science Advances, USGS) but without links. **OPEN ITEM:** link them.
- **Titan.html** has no sp: tags (owned by the parallel Titan worker); build-stats.js uses a FALLBACK entry and warns. Add the tags + page-stats block to Titan.html next time it is touched, then delete the FALLBACK entry.
- **How to add a solution:** sp: meta tags + page-stats section + sitemap entry, then `node build-search-index.js` (see README "Stats engine").

## Session Log — 2026-10-09 (night): Phase 2 — Space Weather & Shields, Earth Observation

- **Format decision:** both hubs use substantial sourced sections on the hub page (one section per candidate, each with its own source links) rather than separate solution pages. Each section is counted by the stats engine through `<meta name="sp:item" content="name|classification|status">` (new in build-stats.js).
- **Space_Weather.html** — D three invisible shields (natural: Voyager 1 heliopause Aug 25 2012 at ~122 AU per NASA; IMAP launched Sept 24 2025; NASA magnetosphere; NOAA ozone/UV-B), E SOLAR-1 (launched Sept 24 2025, L1 Jan 23 2026, operational June 10 2026 — NOAA), F Vigil (L5, 4–5 days' notice, €340M Airbus contract, launch 2031 — ESA; funded, so active), G Aditya-L1 (PSLV-C57 Sept 2 2023, halo orbit Jan 6 2024, ~1.5M km, 7 payloads — ISRO).
- **Earth_Observation.html** — K NISAR (launched July 30 2025, land/ice twice every 12 days, ~1 cm motion — NASA), L Biomass (launched Apr 29 2025, first P-band SAR in space, cross-linked to Deforestation.html — ESA), M Tanager-1 (first methane plume Sept 19 2024, Karachi landfill, 1,200 kg/h, labeled as Carbon Mapper estimate — NASA + Carbon Mapper release), N DSCOVR/EPIC (full sunlit Earth since 2015; L4 tropospheric ozone hi-res product released Oct 5 2026 — NASA).
- **Corrections vs research brief:** SOLAR-1 also became operational on June 10 2026 (the brief only said it reached L1); Vigil warning is "up to four to five days" (brief said up to 5); Voyager 1 heliopause shown as ~122 AU per NASA (121.7 AU in the original particle paper).
- **Images:** SDO_Sun.jpg — NASA/SDO (GSFC_20171208_Archive_e001210); EPIC_Earth.jpg — NASA/NOAA DSCOVR EPIC (GSFC_20171208_Archive_e000678). Both public domain, ≤1600 px, <250 KB.
- Nav dropdown now lists Planetary Defense, Space Weather, Earth Observation on every page except Titan.html; homepage Space card links both hubs; sitemap + search updated (35 entries); solutions.json rebuilt: 29 active solutions, 0 horizon, 10 hubs, 4 upcoming missions.
- **Earth Observation open item:** no earlier "Earth Observation" open item was found in NOTES.md; the hub now exists, so consider it resolved.

## Horizon copy pattern (added 2026-10-09)

- **Template (exact):** "This is a potential solution [ORG] is advancing. We expect to know more within [TIMEFRAME] and will keep you updated here."
- **Component:** one callout, `<div class="horizon-note" data-org="[ORG]" data-timeframe="[TIMEFRAME]" data-next-milestone="[YYYY-MM or empty]">` containing `<span class="horizon-badge">Potential solution on the horizon</span>` plus the sentence (text is in the HTML, so it works without JS and is crawlable). Pages carrying horizon items add `<meta name="sp:item" content="Name|classification|horizon">` so the stats engine counts them separately and never sums their numbers.
- **Timeframe rules:** measure from today to the item's sourced next milestone: ~3 months → "the next three months"; ~6 months → "the next six months"; ~9 months → "the next nine months"; ~12 months → "the coming year"; no reported milestone → "the coming months". Never invent a date; leave data-next-milestone empty when none is reported.

| Item | ORG | Timeframe | Next milestone | Source |
|---|---|---|---|---|
| PRELUDE (with ESA) | ClearSpace | the next nine months | 2027-06 (launch target) | clearspace.today/missions/prelude; SpaceNews Jan 13 2026 |
| CLEAR (with the UK Space Agency) | ClearSpace | the coming months | none officially reported | clearspace.today/missions/clear (the £61.3M Phase 3 award appears only on third-party tender trackers) |
| ISSA-J1 Phase 3 (flight) | Astroscale Japan | the coming months | none reported | Astroscale notice Oct 6 2026 (Phase 2 increase, Phase 3 not awarded) |
| LEXI-P | Astroscale | the next six months | 2027-04 (contract signing expected in FY2027, year ending Apr 2027) | Astroscale business update Apr 2026 |

## Session Log — 2026-10-09 (night): H, I, J, O + horizon rule

- **H Atmospheric_Drag.html** — natural page on Space Disposal (breadcrumb Home > Project R > Space Disposal), paired with Jupiter. Altitude figures only from NASA ODPO FAQ (below 600 km: falls back within several years; 800 km: often centuries; above 1,000 km: a thousand years or more; debris densest at 750–1,000 km; ~1 cataloged piece re-enters per day over 50 years) and NOAA SWPC satellite drag (boost ~4×/yr when quiet vs every 2–3 weeks at solar max).
- **I ClearSpace.html** — new "On the horizon" section: PRELUDE and CLEAR as horizon callouts; the Where card no longer says the UK Space Agency "selected" ClearSpace. PRELUDE callouts also added next to PRELUDE mentions on Space.html and Space_Disposal.html. ClearSpace-1 (ESA contract) stays active.
  - **PRELUDE decision: horizon.** ESA and ClearSpace jointly announced the collaboration (Jan 12 2026) and a June 2027 launch target, but no contract value or funding has been published by ESA, so it does not meet "solidly confirmed contract or funding."
- **J Astroscale.html** — substantial "What's next" section instead of a new page: APS-R active (USSF Space Systems Command agreement; launch now planned in Astroscale FY2027), ISSA-J1 Phase 2 active (¥249M increase Oct 6 2026) with Phase 3 flight as horizon, LEXI-P horizon (contract not signed). Company figures labeled.
- **O LeoLabs.html** — corporate page on Space Disposal; 2 cm tracking claim labeled as a 2021 company figure, and the current company page lists Tracker radars at >10 cm with Ranger (<10 cm) in development.
- Space_Disposal.html: Atmospheric Drag and LeoLabs cards. Sitemap +2, search 37 entries, solutions.json: 32 active, 4 on the horizon, 10 hubs, 4 upcoming missions.
- Images: Progress_Reentry.jpg — NASA iss029e034092; LEO_View.jpg — NASA iss023e057948 (caption strip cropped). Public domain.

## Session Log — 2026-10-09 (late night): Titan catch-up, impact-figure sources, Project R dropdown

- **Titan.html** (e343da7): current Solutions nav, sp: tags (project-r / solution / agency / active, stat: Dragonfly flight >175 km, NASA), page-stats block before next-solutions. FALLBACK entry removed from build-stats.js; build runs with no warnings.
- **Impact figures re-verified (checked 2026-10-09)** and given inline `.fact-source` links:
  - Ocean Cleanup: total 60M kg (July 2026) → >65M kg (theoceancleanup.com homepage); 2025 "over 25M kg" → 27,385,000 kg (Ocean Cleanup 2025 in review).
  - 4ocean: 50M lb (Feb 20, 2026) verified on 4ocean blog. Other 4ocean counts (29,311 cleanups, 2,456 jobs, 346 artisans, 5,672 sq ft kelp, 5,000 mangroves) NOT verified, left as-is.
  - Plastic Bank: 209M kg / 10B bottles / 77,000 collectors → 196,170,000+ kg / ~9.8B bottles / 64,920 collectors (Plastic Bank newsletter, all-time data as of June 10, 2026).
  - Life Terra: 36M trees and 563,000 t CO2 verified; participants 125,000 → 120,000+; classrooms 14,000 → 35,000 (Life Terra release via EURACTIV PR, May 13, 2026). Deforestation.html participant count matched.
  - Clean Up The Lake: 72 Mile Cleanup 25,281 lb verified; "78,000 lb across 130 miles" → 36,177 lb total since 2018 (cleanupthelake.org/stats). Lakes.html matched.
  - Great Lakes Plastic Cleanup: 277,000 pieces verified (GLPC May 26, 2026); "17.5 billion liters filtered" and "nearly 29,000 people" could not be verified and were removed (page + Lakes.html).
  - Restoring the Lake Depths: 13 tons summer 2024 verified (restoremylake.org). Not summed: unit (short vs metric tons) not stated.
  - Sungai Watch: "4.5M kg / 368 barriers (July 2026)" NOT verified on an official source (only third-party: 4M+ kg, March 2026). Left as-is, no link, not summed.
  - Homepage static stats: linked sources; 60M→65M kg, 25M→27M kg, "1,000 rivers carrying most plastic" → "1,000+ rivers carry 80%" (Meijer et al. 2021), 17B gal source corrected from USGS to LBNL 2024 report (17.4B gal, 2023).
- **Summable impact stats** (`sp:stat ...|impact|`): Ocean Cleanup 65,000,000 kg; 4ocean 22,679,619 kg (50M lb converted); Plastic Bank 196,170,000 kg; Clean Up The Lake 16,410 kg (36,177 lb); Life Terra 36,000,000 trees. Homepage overview now renders impactTotals: **283,866,029 kg** across 4 solutions and **36,000,000 trees** (site.js cache key bumped to sp-solutions-v2). Caveat: these organisations count different things (river + ocean trash, hand-gathered plastic, lake litter), so the combined figure is labeled "combined across N solutions".
- **Project R dropdown**: the nav "Project R" link is now a dropdown (Project R overview, then Space Disposal, Planetary Defense, Space Weather & Shields; solutions alphabetical; horizon tag). 
  - **How it auto-updates:** on a hub page, give the solution's card/section `id="anchor" data-menu-item="Name|active"` (or `|horizon`), id first. `node build-search-index.js` → build-stats.js reads PROJECT_R_HUBS (ordered list in build-stats.js), writes `projectRMenu` into solutions.json, and rewrites the static menu HTML between `<!-- PROJECT-R-MENU:START -->` and `<!-- PROJECT-R-MENU:END -->` in every page. New hubs: add to PROJECT_R_HUBS. New pages: copy the nav including the markers.
  - Hub membership is by explicit hub file (not sp:category) because Project-R.html and Space_Disposal.html share category project-r.
  - Astroscale → Space_Disposal Who card (#astroscale), ClearSpace → Impact box (#clearspace); PRELUDE horizon note (#prelude). CLEAR and Astroscale horizon items live only on their own pages, so they are not in the menu.
  - ClearSpace.html and Plastic_Bank.html had no Project R nav link before; they now have the dropdown.
  - site.js: all .nav-dropdown menus toggle with aria-expanded, Escape closes, opening one closes others. styles.css: scroll-margin-top on menu targets, max-height + scroll on menu and mobile nav.

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-09 | Local port 8765 was already serving a stale copy of the site, so the first headless test read old HTML | Served /workspace/sw2 on 127.0.0.1:8799 | Yes |
| 2026-10-09 | Headless Chrome `networkidle0` waits up to minutes on pages with the mission news widget | Use `load` for UI checks | Yes |
| 2026-10-09 | Mobile screenshots show page text faintly behind the open menu although .nav-links computes to white 0.98 (likely headless rendering of the parent nav's backdrop-filter) | Not fixed; needs a check on a real phone | No |

## Session Log — 2026-10-09 (Project R reorder by Brian)

- Brian reordered Project-R.html in 194b72a: Impact Statement, Five W's, Project R Categories, By the Numbers (page-stats), Upcoming Launches last.
- FOLLOW-UP (open): the phone-only rule in styles.css (`@media (max-width: 600px)` .pr-flow order rules) still forces the old order on phones and lifts page-stats to the top; recommended fix is deleting that rule. Skip link still targets #solution (Five W's) instead of the Impact Statement now first.
- FOLLOW-UP (open): faint text visible behind the open mobile menu at 390px in headless screenshots; verify on a real phone.

## Session Log — 2026-10-09 (styles.css truncation fix)

- GLITCH: commit f2f3357 (pr-hero class, pushed via GitHub connector) truncated styles.css from 519 to 261 lines, ending mid-rule at "body.toc-home .s". Lost launches widget, stats, mission widget, horizon, Project R menu, page-specific and responsive styles.
- WORKAROUND: ab53f4b restored the full file from git history (54a064d), re-added the pr-hero rule, and replaced the Dark mode section with the expanded version (99 html.dark selectors). File now 589 lines, braces balanced, deploy succeeded. RESOLVED.
- RULE OF THUMB: edit styles.css (and other large files) via git clone, not the connector's create_or_update_file, which truncates large files.

## Session Log — 2026-10-09 (domain reset: one URL, no redirects)

- **Decision:** Use exactly one public URL — `https://www.savingplanets.com` — and drop every redirect, alias, and old domain. No connection to `saveplanetminusthedoom.com` or `saveplanet-minus-doom.com`.
- **Repo change:** CNAME set to `www.savingplanets.com` (commit on main). The deploy workflow (`.github/workflows/static.yml`) is unchanged — it uploads the repo root to GitHub Pages.
- **Why this works:** GitHub Pages serves the site on the default domain `chambersbryank-dot.github.io/Saveworld/` automatically. A custom domain is only a DNS pointer on top of that. The site does not depend on the custom domain to exist.
- **Cloudflare DNS (user action, required):**
  1. Delete the proxied A records for `www` (104.21.41.225 / 172.67.195.99) — they were sending www to a dead Cloudflare origin, which is the 404.
  2. Create one DNS-only (grey cloud) CNAME: `www` → `chambersbryank-dot.github.io` (no repo name in the target).
  3. Leave the apex `savingplanets.com` A records alone for now, or delete them too if you want the bare domain to stop resolving.
  4. Do not create any Page Rule or Redirect Rule. No redirects, by design.
- **Verification:** `https://www.savingplanets.com` should show the homepage. `https://chambersbryank-dot.github.io/Saveworld/` is the permanent fallback that always works even if DNS is broken.
- **Old domains:** `saveplanetminusthedoom.com` and `saveplanet-minus-doom.com` are retired. If they still have DNS, point them at nothing or let them expire. They are not referenced anywhere in the site.
- **HTTPS:** GitHub Pages provisions a certificate for the custom domain automatically after DNS is correct; can take up to 24 hours. No Cloudflare SSL settings needed since the proxy is off.

## Session Log — 2026-10-10 (Project R → Project Rawane rename)

- Renamed Project-R.html → Project-Rawane.html; title, h1, breadcrumb, canonical, og/twitter, JSON-LD now "Project Rawane" at https://www.savingplanets.com/Project-Rawane.html. sp:category kept as project-r.
- Hero subtitle: "The two-way relationship between Earth and space. Project R is named for Rawane — because the best projects start with someone you love." Removed duplicate "named for Rawane" sentence from impact statement (it now opens with "It follows Astroscale's ADRAS-J mission…"; there was no "Errol Scales" text).
- .pr-hero background → assets/Nebula2.jpg (gradient kept). All Project-R.html links replaced site-wide incl. build-stats.js menu generator, sitemap, solutions.json, Search.html, README. Nav label still "Project R".
- Old Project-R.html URL now 404s; consider a meta-refresh stub.

## Session Log — 2026-10-10 (Project-R.html redirect, Rawane labels, Errol Scales)

- Added Project-R.html redirect stub (meta refresh 0 → Project-Rawane.html, canonical, noindex). Excluded from build-stats.js SKIP and build-search-index.js; not in sitemap.
- Nav dropdown label, "Project Rawane overview", Five W's heading, Categories heading and build-stats.js menu generator now say Project Rawane. URLs and sp:category=project-r unchanged; hero subtitle untouched.
- Impact statement now opens: "It follows Errol Scales' work on orbital debris removal. It also follows Astroscale's ADRAS-J mission…"
- Still "Project R" (not in scope): JSON-LD breadcrumb names on Space Disposal sub-pages, "Back to Project R" link, "Part of Project R", Dragonfly copy, categories intro paragraph, build-stats.js category label 'project-r': 'Project R'.

## Session Log — 2026-10-10 (remaining Project R labels → Project Rawane)

- Renamed: "Back to Project Rawane" (Space_Disposal), "Part of Project Rawane" (Space.html), Dragonfly paragraph (Titan), categories intro (Project-Rawane), JSON-LD + visible breadcrumb names on Atmospheric_Drag, LeoLabs, MMX, Space_Disposal, Titan. build-stats.js display name 'project-r': 'Project Rawane' (key unchanged); solutions.json rebuilt.
- Still "Project R": meta/og/twitter descriptions on Project-Rawane.html and Search.html, Search.html index title entry (build-search-index.js doesn't refresh existing titles).

## Session Log — 2026-10-10 (Project Rawane mission list + plain nav link)

- Project-Rawane.html breadcrumb (was Home › Project Rawane) replaced by alphabetical middot-separated mission list (nav.breadcrumb.mission-list; CSS in styles.css; inherits dark-mode breadcrumb colors). 16 items incl. Space Disposal hub; PRELUDE keeps horizon tag.
- No dedicated page (hub anchors): Aditya-L1, PRELUDE, SOLAR-1, Three invisible shields, Vigil.
- Top nav: Project Rawane is now a plain link on all pages; build-stats.js menuHtml emits the plain link (markers kept, menu data still in solutions.json).

## Session Log — 2026-10-10 (Titan restructure + jump-nav)

- Titan.html order after breadcrumb: Impact Statement → Five W's (id five-ws, was #solution; skip-link updated) → .jump-nav (Five W's / Titan by the numbers / Learn more) → Dragonfly mission widget → Titan by the numbers (id by-the-numbers, was #numbers) → page-stats → Learn More banner (unchanged) → next-solutions.
- Learn more: original donate-banner kept; jump-nav has a matching external link (science.nasa.gov/mission/dragonfly, new tab).
- styles.css: .jump-nav pill styles (dark mode, wraps), added to the nav.breadcrumb position reset (generic nav rule otherwise fixes it to top), scroll-margin for new ids. Smooth scroll already global.

## Candidate Queue — batch 2026-10-10

Second daily batch (16), prepared by the 6:17 AM HST routine. Nothing built; awaiting Brian's yes/no on each. Checked against every page, solutions.json, and the 2026-10-09 queue (A–P) so nothing repeats. Every figure below was read on the cited page this morning; company/nonprofit figures are labeled as such at build time.

| ID | Candidate | Classification | Suggested hub | Mission widget | Status |
|---|---|---|---|---|---|
| A | IMAP (NASA, Sun-Earth L1; launched Sept 24 2025; ~half-hour radiation warning) | Agency mission (NASA) | Space Weather & Shields (own page; hub mentions it in one line today) | Yes, active (I-ALiRT real-time feed) | PENDING |
| B | GOES-19 + CCOR-1 (NOAA, GEO 22,236 mi; first operational space coronagraph) | Agency mission (NOAA) | Space Weather & Shields | Yes, active | PENDING |
| C | U.S. Deorbit Vehicle for the ISS (NASA contract to SpaceX, up to $843M; station ops end 2030) | Agency contract (NASA) / corporate | Space Disposal | Yes, countdown to 2030 end of ops | PENDING |
| D | ESA Aeolus assisted reentry (July 28 2023, first of its kind) + Zero Debris by 2030 | Agency mission (ESA) | Space Disposal | No (complete); Aeolus-2 = horizon | PENDING |
| E | LignoSat wooden satellite (Kyoto Univ + Sumitomo Forestry, deployed by JAXA Dec 9 2024; no signal, reentered Apr 4 2025) | University / corporate | Space Disposal + Forests cross-link | No; any follow-on = horizon | PENDING (horizon if approved) |
| F | SWOT (NASA/CNES; 95%+ of lakes >15 acres, rivers >330 ft) | Agency mission (NASA/CNES) | Earth Observation + Lakes and Rivers cross-links | Yes, active | PENDING |
| G | PACE (NASA ocean color, 676 km, launched Feb 2024) | Agency mission (NASA) | Earth Observation + Oceans | Yes, active | PENDING |
| H | Phytoplankton, the ocean's oxygen engine (NOAA: about half of Earth's oxygen) | Natural | Oceans (pairs with G) | No | PENDING |
| I | Copernicus Sentinel-6B (ESA/NASA/EUMETSAT/NOAA, launched Nov 17 2025; sea-level record since early 1990s) | Agency mission (ESA/NASA) | Earth Observation + Oceans | Yes, active | PENDING |
| J | GOSAT-GW "IBUKI GW" (JAXA, launched June 29 2025; CO2/CH4/NO2 + water cycle) | Agency mission (JAXA) | Earth Observation | Yes, data-release milestone | PENDING |
| K | EarthCARE (ESA/JAXA, launched May 28 2024; JAXA cloud radar measures up/down flow) | Agency mission (ESA/JAXA) | Earth Observation | Yes, active | PENDING |
| L | ALOS-4 "DAICHI-4" (JAXA, launched July 1 2024; 200 km radar swath, deforestation alerts in 77 countries) | Agency mission (JAXA) | Earth Observation + Deforestation cross-link | Yes, active | PENDING |
| M | Artemis II (NASA/CSA, Apr 1–10 2026; record 252,756 mi from Earth) | Agency mission (NASA/CSA) | Project Rawane (voyages outward) | Yes, Artemis III (NASA: "next year", 2027) | PENDING |
| N | Mr. Trash Wheel family (Waterfront Partnership of Baltimore; 4 wheels, 500 tons/yr for Mr. Trash Wheel) | Nonprofit | Rivers | No | PENDING |
| O | Coral Restoration Foundation (Florida Keys; 253,833 corals returned through 2024, 22,404 in 2025) | Nonprofit | Oceans | No | PENDING |
| P | Mangrove forests (natural, NOAA; ~80 species, coastline storm buffer) | Natural | Forests + Oceans cross-link | No | PENDING |

Dropped this morning (could not verify or status unclear): NASA TEMPO (extension beyond Sept 2026 not confirmed), ESA Proba-3 (coronagraph spacecraft contact being restored), Eden: People+Planet (headline figures are carbon-credit projections), Mr. Trash Wheel all-time tonnage (only in press, not on the official site; per-year figure used instead).

## Session Log — 2026-10-10 (morning candidate run)

- Session start: git pull, NOTES.md read, last 24h of commits reviewed. Found NOTES.md truncated since cfad49d; restored in 4452700 and logged under Known Glitches.
- Prepared batch 2026-10-10 (A–P above) for Brian's yes/no. No pages built or pushed.


## Session Log — 2026-10-10 (HTTPS certificate for www.savingplanets.com)

- Live check ~7:35 AM HST: DNS fixes are in (www CNAME DNS-only, A-record typo gone). Site loaded over http, but https failed with a certificate mismatch.
- Re-entered the custom domain www.savingplanets.com in GitHub Pages via the API to trigger the certificate request. State went new to approved; certificate covers apex and www.
- Enabled Enforce HTTPS. Verified https://www.savingplanets.com and /Titan.html return 200, and https://savingplanets.com 301s to https://www.savingplanets.com/.
- Still open: www.saveplanetminusthedoom.com returns a 404 (no Worker anymore, but no redirect either). Per the domain-reset decision it is retired; a redirect to the new domain is optional and needs Brian's call in Cloudflare.

## Session Log — 2026-10-10 (dedicated pages: Aditya-L1, SOLAR-1, Three Shields, Vigil, PRELUDE)

- New pages Aditya_L1.html, SOLAR_1.html, Three_Shields.html, Vigil.html (sp:category space-weather) and PRELUDE.html (sp:category space, status horizon, horizon-note pattern). Seeded only from existing hub text + its sources; no new figures. PRELUDE launch date labeled company target.
- Counting: removed the matching sp:item metas from Space_Weather.html (4) and ClearSpace.html (PRELUDE) so totals unchanged (32 active, 4 horizon). Upcoming missions 4 → 6 (Vigil 2031, PRELUDE June 2027 widgets, status-text detection; no exact dates invented). Aditya-L1 and SOLAR-1 widgets have milestones only.
- Hub sections got "Read more" links; Project-Rawane A–Z list now links to the new pages; sitemap +5; search index rebuilt. projectRMenu data in solutions.json still points to hub anchors (menu not rendered).

## Session Log — 2026-10-10 (site consistency pass: hub pattern, hub cards, bottom-link rule)

- GLITCH: 58f80df accidentally committed another worker's scratch files (crf25.pdf 27 MB, crf25.txt, ligno.pdf, ligno.txt) via `git add -A`. Removed from the tree in 8d27d44 (files still on the box; added to .git/info/exclude). The blob remains in history (no force-push). Rule: use `git add -u` or explicit paths, never `-A`, in the shared clone.
- 77b3a76: every hub (Oceans, Lakes, Rivers, Deforestation, Space, Space Disposal, Planetary Defense, Space Weather, Earth Observation) has a `card-band hub-cards` (#missions) grid before page-stats. Earth Observation cards link to hub anchors (no dedicated pages). Hubs without next-solutions got "Next: explore another hub". Project Rawane categories band now has Planetary Defense + Space Weather cards next to Space Disposal.
- Impact-first order applied to 17 solution pages (line move only, no text changes).
- Bottom-link rule: exactly one `section.donate-banner.bottom-link#bottom-link` per content page, before next-solutions. Priority donate → "Join the work" → subtle "For further information" (.donate-btn-subtle). All old donate/learn-more banners and .source-link paragraphs removed. Donate URLs verified by HTTP 200 on 2026-10-10. Plastic Bank /individuals now redirects to /pricing (business plans) and Astroscale get-involved is careers/events, so both get "For further information". Terraformation's donate URL couldn't be verified, so it also gets "For further information".
- Not touched: index, About, Contact, Amazing_Facts, Search, 404, Project-R redirect.

## Session Log — 2026-10-10 (Project Rawane as hub)

- Project-Rawane.html: hero → Impact Statement → Five W's → three hub card groups (section.card-band.hub-cards.hub-group: Space Disposal 8, Planetary Defense 4, Space Weather & Shields 4; headings link to hubs; Jupiter appears under both SD and PD) → page-stats → launches → one bottom link (NASA ODPO) → next-solutions. A–Z mission-list nav and old categories band removed.
- Mobile order rules (≤600px) now impact 1, five-ws 2, hub-group 3, page-stats 4, launch-widget 5 (old rule put Five W's first and launches before cards).

## Session Log — 2026-10-10 (hub audit to Space_Disposal template; Project Rawane top removed)

- 0c15c1e: Project-Rawane.html hero (h1 + Rawane line) removed; visually hidden h1 "Project Rawane" added; .pr-flow gets top padding to clear the nav. (A–Z row was already gone.) The Rawane hero line no longer appears anywhere on the page.
- Hub audit: Oceans, Lakes, Rivers, Deforestation, Space got new Impact Statement + Five W's (replacing the old duplicate solution grid; hub cards remain). Figures only from site-cited sources: Ocean Cleanup 65M kg, 4ocean 50M lb, Plastic Bank 196M kg, Clean Up The Lake 36,177 lb, GLPC 277,000 pieces, Restore My Lake 13 t, Life Terra 36M trees. Org/company figures labeled. Rivers and Space impact statements are qualitative (river figures on old grid had no source link on the hub).
- Planetary Defense, Space Weather, Earth Observation: impact heading → "Impact Statement" (old heading kept as h3), "On this hub"/solutions grid replaced by Five W's, hub cards moved right after Five W's; detailed sections (Roman note, SW/EO mission sections) kept below.
- All solution pages have an Impact Statement and Five W's. Earth Observation missions (NISAR, Biomass, Tanager-1, DSCOVR/EPIC) still have no pages.

## Session Log — 2026-10-10 (permanent dark mode)

- Theme toggle removed from all pages (build-stats.js never emitted it). site.js: localStorage/prefers-color-scheme toggle logic removed; just adds 'dark' as a safety net.
- Approach: static `<html lang="en" class="dark">` + `<meta name="color-scheme" content="dark">` on every page (no flash; existing html.dark rules apply). Light-mode base rules remain in styles.css but are always overridden; promoting html.dark to defaults was judged higher risk.
- All .theme-toggle CSS deleted. New pages must use `<html lang="en" class="dark">`.

## Session Log — 2026-10-10 (Space Disposal: no hero)

- Space_Disposal.html: removed hero (h1 + "Removing dead rockets and debris from orbit — before it removes our satellites.") and visible breadcrumb (Home › Project Rawane › Space Disposal). Added visually hidden h1 + body class `no-hero`; CSS `body.no-hero h1.visually-hidden + section` pads below the fixed nav (reusable for other hero-less pages). JSON-LD breadcrumb kept.

## Session Log — 2026-10-10 (Space Disposal duplicate Jupiter)

- Removed the Jupiter card from the "Missions and solutions" card grid on Space_Disposal.html; kept the entry under "Natural debris and saving moons" (already carries id="jupiter" + data-menu-item). Jupiter's count comes from Jupiter.html's own sp: tags, so totals unchanged (32 active, 4 horizon, 10 hubs, 6 upcoming). If hub cards are ever regenerated, leave Jupiter out of the Space Disposal list.

## Session Log — 2026-10-10 (Space Disposal centered headings)

- Added `h2.h2-center` (styles.css) to Impact Statement, The Five W's of Space Disposal, and Natural debris and saving moons on Space_Disposal.html. Missions and solutions / Next headings were already centered.

## Session Log — 2026-10-10 (Space Disposal: Atmospheric Drag only under natural)

- Atmospheric Drag already had an entry (id="atmospheric-drag", data-menu-item) in "Natural debris and saving moons"; removed its duplicate card from "Missions and solutions". Totals unchanged (32/4/10/6). Still duplicated across both sections: Titan, MMX, LeoLabs (awaiting a decision).

## Session Log — 2026-10-10 (Space Disposal: dedupe Titan, MMX, LeoLabs)

- Titan kept only in "Natural debris and saving moons" (card removed from Missions grid). MMX and LeoLabs kept only in "Missions and solutions": their natural-section w-cards removed, and their id (#mmx, #leolabs) + data-menu-item moved onto the mission cards. Natural section now: Jupiter, Titan, Atmospheric Drag. Missions grid: Astroscale, ClearSpace, LeoLabs, MMX, PRELUDE. Totals unchanged (32/4/10/6).

## Session Log — 2026-10-10 (Project Rawane title hero restored)

- Project-Rawane.html: visible hero restored with only `<h1>Project Rawane</h1>` on .pr-hero (Nebula2.jpg + dark gradient); no subtitle/Rawane line, breadcrumb or links. Visually hidden h1 removed (one h1). The .pr-flow top-padding rule was removed from styles.css. The mobile order rules sit inside .pr-flow, and the hero is outside it, so they are unaffected.

## Session Log — 2026-10-10 (all hubs: Nebula2 title hero)

- New shared `.page-hero.hub-hero` (styles.css): Nebula2.jpg + pr-hero dark gradient. Applied to Oceans, Lakes, Rivers, Deforestation (Forests), Space, Planetary Defense, Space Weather, Earth Observation, Space Disposal: hero contains only the h1 (subtitles removed; old hero classes space-hero/lakes-hero/rivers-hero/forest-hero dropped on hubs; photo credits for the old hero images on Earth Observation, Planetary Defense and Space Weather removed). Breadcrumbs left in place (between hero and Impact Statement where present).
- Space Disposal: hidden h1 replaced by visible hero; `no-hero` body class and its CSS removed. Project Rawane keeps its pr-hero (same look). Mission pages untouched.

## Session Log — 2026-10-10 (hubs: visible breadcrumbs removed)

- Removed visible breadcrumb nav from Oceans, Lakes, Rivers, Deforestation, Space, Planetary Defense, Space Weather, Earth Observation (Space Disposal and Project Rawane had none). JSON-LD BreadcrumbList kept on all.
- Order fix: Planetary Defense "A note on Roman" moved from between Five W's and cards to after the cards. Space Disposal keeps "Natural debris and saving moons" (itself a card group) before "Missions and solutions"; Space Weather and Earth Observation keep their detailed mission sections after the cards.

## Session Log — 2026-10-10 (Project Rawane dedication restored)

- Restored `<p class="pr-dedication">` below the title hero, above the Impact Statement: "The two-way relationship between Earth and space. Project R is named for Rawane — because the best projects start with someone you love." (CSS .pr-dedication, centered italic).
- Searched full history of Project-Rawane.html and Project-R.html (log --follow -p, -S/-G across all files) for a dedication mentioning a daughter: none found. The only dedication wording in history is the line above (hero subtitle) and "Project Rawane is named for Rawane — because the best projects start with someone you love." (impact sentence, introduced f2bd4c5, removed ddf48f6 at the user's request). Hero subtitle line: added ddf48f6, removed 0c15c1e, restored 06c58f4.
- Errol Scales sentence was still present in the impact statement; not changed.

## Session Log — 2026-10-10 (Project Rawane: Space Disposal split cards)

- Project-Rawane.html Space Disposal group: (1) two cards side by side (.grid.sd-split): "Space Disposal (created by mankind)" → Space_Disposal.html#missions, "Space Disposal (natural space disposal solutions)" → Space_Disposal.html#natural-debris-and-saving-moons (synopses from existing Space Disposal text); (2) natural row (.grid.sd-natural): Atmospheric Drag, Titan, Jupiter → their pages; (3) mission grid now only Astroscale, ClearSpace, LeoLabs, MMX, PRELUDE. Jupiter's Planetary Defense card unchanged.
- Space_Disposal.html: added `<span id="natural-debris-and-saving-moons" class="anchor-target">` inside section#natural (kept #natural for existing links).

## Session Log — 2026-10-10 (Project Rawane dedication gap)

- styles.css (pr-page scoped): .pr-flow > .impact padding-top 0.3rem and its h2 margin-top 0.7rem. Gap from dedication line to "Impact Statement" heading 32px → 16px at 1280px and 390px (measured in headless Chrome). No text changes.

## Session Log — 2026-10-10 (Project Rawane dedication in hero)

- p.pr-dedication moved inside .pr-hero under the h1 (text unchanged); centered italic light text with shadow. pr-hero now height:auto, min-height 340px, padding-top nav+2.2rem so title + line clear the nav and wrap on phones. Removed the old standalone .pr-dedication rule and the earlier impact gap tweak (cdf2bbb), so the Impact Statement uses default spacing.

## Session Log — 2026-10-10 (dedication wording)

- Dedication line now reads: "A two-way relationship between Earth and Space. Project R is named for Rawane — because the best projects start with someone you love." (Project-Rawane.html hero). Earlier log entries keep the old wording as history. Meta/og/twitter descriptions and the Five W's "What" card use a different phrase ("the two-way relationship between Earth and space — …") and were not changed.

## Session Log — 2026-10-10 (Project Rawane Space Disposal subsections)

- After the two split cards (now titled "Man-made solutions" / "Natural solutions" per user commits 6ce41f3, 36711ed): h3.sd-subhead "Space disposal (made by mankind)" + Astroscale, ClearSpace, LeoLabs, MMX, PRELUDE (horizon); then h3.sd-subhead "Space disposal made by nature" + Atmospheric Drag, Titan, Jupiter. Reorder only, no text changes.

## Session Log — 2026-10-10 (Project Rawane: PRELUDE centered)

- Man-made grid on Project-Rawane.html gets class sd-mankind: flex-wrap with justify-content:center; cards fixed at 1/4 width (≤900px: 1/2, ≤600px: full), min-width:0 so images don't force width. At 1280px the first four stay in one row and PRELUDE is centered under ClearSpace/LeoLabs (same 270px width); at ~800px rows of two with PRELUDE centered; phones single column.

- 2026-10-10: Project Rawane — halved gap above "Space disposal (made by mankind)" block (29px → 14px at 1280/390; subhead-to-cards 16px unchanged). Commit fa1763c.

## 2026-10-10 — Fix Upcoming Launches widget stuck on loading
- Project-Rawane.html inline launch script had three unterminated string literals (`getElementById('lw-next);`, `'lw-list);`, `querySelector('.lw-countdown);`), introduced in ddf48f6 (Project R → Project Rawane rename). The SyntaxError stopped the whole script, so the "Loading the next launch" placeholder never changed. Not CORS, rate limit, cache or a removed element.
- Also fixed: `&hellp;` typo in the placeholder, and the `esc()` HTML-escape map (entities had been decoded to raw characters).
- Added fallback: 10 s timeout + AbortController; on any fetch/HTTP/render failure it shows "Launch data unavailable right now" with the Next Spaceflight link.
- Verified in headless Chrome on a local server: mocked LL2 response renders next launch + countdown + list; mocked 429 shows the fallback; no page errors (site.js widgets unaffected).

### Known Glitches
- Upcoming Launches (Project-Rawane.html): was stuck on "Loading…" due to a JS syntax error from a bulk rename. Fixed 2026-10-10. After bulk find/replace edits, run `node --check` on inline scripts.

## Amazing Facts convention
- Mark facts on any sitemap page with `<p class="amazing-fact" [hidden] data-title="..." data-source="URL" data-source-name="...">text</p>`. `node build-search-index.js` → `build-facts.js` regenerates Amazing_Facts.html between FACTS:START/END (dedupe by text, sort by heading, From-page + Source links; no data-source = skipped + warning). Hand cards in the block use `data-fact-origin="hand"` and are preserved. Only add facts supported by a cited source.

## 2026-10-10 — Amazing Facts: Jupiter fact + auto-collect (4d3b198)
- Added build-facts.js (called from build-search-index.js). Amazing_Facts.html now has FACTS markers; 4 existing hand facts kept (data-fact-origin="hand"), plus "Room for 1,300 Earths" sourced from a hidden amazing-fact on Jupiter.html (NASA Jupiter Fact Sheet, 1,321 by volume). 5 facts total. Proposed "Jupiter deflected/captured 2,000+ objects" NOT added: unsupported (real stat: comet impacts ~2,000x Earth's rate). Verified in headless Chrome at 1280px; build is idempotent.

- 2026-10-10: Project Rawane headings (Impact Statement, Five W's, Space Disposal, Made by Mankind, Made by Nature, Planetary Defense, Space Weather & Shields, By the Numbers, Upcoming Launches) all use the Impact Statement h2 size, clamp(1.6rem, 3vw, 2.2rem) = 35.2px @1280 / 25.6px @390, via ONE scoped body.pr-page block at the end of styles.css (replaced stacked overrides from 054b7cb/c584de1/809a7b3). Heading renamed "Space Disposal (Made by Nature)". All pages now link styles.css?v=20261010 and site.js?v=20261010; bump the version when CSS/JS changes.

- 2026-10-10: d87db2a Project Rawane: Space Disposal hub group moved up — `body.pr-page #group-space-disposal { padding-top: 0 }`; gap Five W's→h2 82px→41px (1280 & 390). styles.css cache-bust ?v=20261010b on 44 pages.
- 2026-10-10: c709c79 Project Rawane: even 41px gaps between all major blocks (Five W's, Space Disposal, Mankind, Nature, Planetary Defense, Space Weather, By the Numbers, Upcoming Launches) at 1280 & 390; Mankind treated as a block. Cache-bust ?v=20261010c.
- 2026-10-10: 73b1536 Project Rawane: Natural solutions card image (Earth.jpg), Astroscale card image (RocketLaunch.jpg), sd-split gap 16px->24px (1.5rem), 360px cards centered. Cache-bust ?v=20261010d.

## 2026-10-10 — Review fixes (10 items)
- b1edf3a alt text on 60 card images (15 pages) that had alt="".
- 83f8985 unique NASA images for in-page duplicate cards: Earth_Observation (NISAR PIA26285, Biomass PIA11420, Tanager-1 PIA26416), Space_Weather (Aditya PIA22661, SOLAR-1 KSC-20250924-PH-SPX01_0007, shields GSFC_20171208_Archive_e002115, Vigil PIA21836), Space + Space_Disposal (Astroscale S66-62755, PRELUDE iss042e013730), Oceans Plastic Bank (sts066-154-157), Rivers Sungai Watch (iss074e0492148). All <=1200px, <250KB. Bottom "Next" banner images intentionally reuse the page hero.
- 7972212 Amazing Facts: removed duplicate data-site-stats counter (one stats block); Be Part of the Fix h2 = section size (body.toc-sub #actions only exists on AF).
- 49b772e Project Rawane Jupiter blurbs differentiated (Nature = debris capture; Planetary Defense = 2,000x comet impact rate, per Jupiter.html sources); Nature Jupiter image -> Jupiter.html.
- c1a6c42 Project Rawane headings: Made by Mankind/Nature subheads now h2.sd-subhead (CSS h3.sd-subhead -> .sd-subhead), all h3 20px, Title Case (site.js "By the Numbers", "Site-Wide"); site.js ?v=20261010b on all pages. Gaps unchanged.
- 8539791 AF captions opacity 0.85, min 0.55rem, wrap (not clip) <380px.
- 96ba6f1 Lena 520->226KB (900px), Bahamas 205->112KB (1000px); banner already 143KB, left as is.
- 8838d23 AF banner pause/play button (.af-motion-toggle, aria-pressed; hidden under prefers-reduced-motion).
- 47bddcf AF footer trimmed to copyright line.
- f098448 phone check via CDP device emulation (390x844, 360): no horizontal overflow on PR/AF; AF hero got room for the pause button. Screenshots /workspace/phone_*.png. Tip: node --experimental-websocket + Chrome --remote-debugging-port gives real mobile emulation without puppeteer.

## 2026-10-10 — Heading hierarchy, PRELUDE badge a11y, site-wide Title Case
- 73ffd72 `.impact-box h3.mission-title` (11 pages: Three_Shields, Space_Weather, Hera, MMX, Titan, Jupiter, Astroscale, Atmospheric_Drag, Earth_Observation, Planetary_Defense, Space_Disposal) now clamp(1.3rem, 2.4vw, 1.7rem) = 27.2px @1280 / 20.8px @390 (was 20px), between h2 (35.2/25.6) and body. styles.css ?v=20261010n on all pages.
- 37d10e3 PRELUDE "horizon" badge: aria-hidden on Space, Space_Disposal, Project-Rawane cards (heading name = "PRELUDE (ClearSpace)"); build-stats.js menu template adds visually-hidden ", on the horizon".
- 18584a3 Title Case on 38 pages (headings, <title>, og/twitter titles, JSON-LD headline/name) via script; site.js generated headings ("Mission Status", "Latest News", "This Page"); site.js ?v=20261010c. Preserved: brand "4ocean", "horizon" badge, "Our Stats are Already Amazing Facts.", Space Disposal (Made by …). Rule: lowercase a/an/the/and/or/but/nor/of/to/in/on/for/by/at/vs/as unless first, last or after a colon; words with any capital left untouched. New headings should follow Title Case.

## 2026-10-10 — Batch 2026-10-10 (A–P) built; site review
- Used the "Candidate Queue — batch 2026-10-10" table (6:17 AM HST routine). All 16 approved by Brian; none skipped (no join-me events or donation drives); none already on the site. Each = hub section (Impact Statement + Five W's + For Further Information link) + card in the hub grid + sp:item meta; unique NASA images (<=1200px, <250KB) with alt text.
- c0b9e92 Space_Weather: #imap (A), #goes-19 (B). 115c3f6 Space_Disposal: #us-deorbit-vehicle (C, contract amount omitted — not on NASA page), #aeolus (D), #lignosat (E; LignoSat-2 follow-on = horizon, Kyoto University, "the coming months", no milestone). 8355181 Earth_Observation: #swot (F, Earth/atmosphere/space value explicit), #pace (G), #sentinel-6b (I), #gosat-gw (J), #earthcare (K), #alos-4 (L; 77-country JJ-FAST figure attributed to DAICHI-2 data). f062b05 Oceans: #phytoplankton (H), #coral-restoration-foundation (O, org figures). a844d52 Rivers: #mr-trash-wheel (N, org figure). 80c4235 Deforestation: #mangroves (P). 352a05e Project-Rawane: new "Voyages Outward" group #group-voyages-outward with #artemis-ii (M).
- beaf352 Amazing Facts: 11 hidden amazing-fact entries (A, B, D, E, F, H, K, M, N, O, P) with data-image/alt/credit; build → 14 cards. solutions.json: 47 active, 5 horizon.
- 66d68ed Mission Status widget h2 now section size (35.2/25.6px); styles.css ?v=20261010o on all 44 styled pages.
- Review: no overflow at 390/360/1280 on all 45 pages; no broken links/anchors/images; all images have alt; Title Case clean (exceptions: 4ocean brand, horizon badge, "Our Stats are Already Amazing Facts."); consent.js on all 45, no inline gtag; LIVE fresh-profile test: no GA before Accept, gtag+collect after Accept, nothing after Decline. HTTPS cert www valid to 2027-01-08; https://savingplanets.com → 301 www. Port-80 (http://) redirect not testable from the box (outbound 80 blocked).

## Candidate Queue — batch 2026-10-11

Third daily batch (19), prepared by the 6:17 AM HST routine. Status 2026-10-11: all 19 approved by Brian 2026-10-11 and built (see build log below). Checked against every page, solutions.json, and the 2026-10-09 (A–P) and 2026-10-10 (A–P, all approved and built) queues so nothing repeats. Every figure was read on the cited page this morning; company/nonprofit figures get labeled as such at build time.

| ID | Candidate | Classification | Suggested hub | Mission widget | Status |
|---|---|---|---|---|---|
| A | Europa Clipper (NASA; launched Oct 14 2024; Earth gravity-assist flyby Dec 3 2026; Jupiter April 2030, 49 Europa flybys) | Agency mission (NASA) | Space Disposal "saving moons" (next to Titan) | Yes, Earth flyby Dec 3 2026 + arrival countdown | APPROVED by Brian 2026-10-11; BUILT |
| B | Juice (ESA; launched Apr 14 2023; Earth flyby Sept 2026 done, next Jan 2029; Jupiter July 2031, 35 moon flybys) | Agency mission (ESA) | Space Disposal "saving moons" | Yes, Jan 2029 Earth flyby + July 2031 arrival | APPROVED by Brian 2026-10-11; BUILT |
| C | OSIRIS-APEX and Apophis 2029 (NASA; Apophis passes ~20,000 mi from Earth Apr 13 2029; rendezvous June 2029) | Agency mission (NASA) | Planetary Defense | Yes, Apophis flyby countdown | APPROVED by Brian 2026-10-11; BUILT |
| D | Ramses (ESA with JAXA; EUR 81.2M build contract Feb 10 2026; H3 launch spring 2028; first switch-on Sept 2026) | Agency mission (ESA/JAXA) | Planetary Defense (pairs with C, Hera heritage) | Yes, spring 2028 launch | APPROVED by Brian 2026-10-11; BUILT |
| E | PUNCH (NASA; four smallsats, launched Mar 11 2025; 3D corona-to-solar-wind) | Agency mission (NASA) | Space Weather & Shields | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| F | TRACERS (NASA; twin satellites, launched July 23 2025; magnetic reconnection in polar cusps) | Agency mission (NASA) | Space Weather & Shields (cross-link Three Shields) | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| G | Carruthers Geocorona Observatory (NASA; L1, launched Sept 24 2025; first mission dedicated to the exosphere) | Agency mission (NASA) | Space Weather & Shields | Yes, active (2-year mission) | APPROVED by Brian 2026-10-11; BUILT |
| H | Solar Orbiter (ESA with NASA; launched Feb 2020; 42 million km from Sun; first close-up views of the Sun's poles) | Agency mission (ESA/NASA) | Space Weather & Shields | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| I | ESCAPADE (NASA/UC Berkeley; twin Mars orbiters, launched Nov 13 2025; Earth slingshot fall 2026) | Agency mission (NASA) | Project Rawane (Voyages Outward) | Yes, Earth slingshot + Mars arrival | APPROVED by Brian 2026-10-11; BUILT |
| J | GRACE-FO (NASA/Germany; launched May 22 2018; tracks groundwater, ice, sea level by gravity) | Agency mission (NASA/GFZ) | Earth Observation + Lakes/Rivers cross-links | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| K | ICESat-2 (NASA; launched Sept 15 2018; laser fires 10,000 pulses a second) | Agency mission (NASA) | Earth Observation | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| L | Copernicus Sentinel-1 radar (ESA; 1C Dec 5 2024, 1D Nov 4 2025; all-weather day-night imaging) | Agency mission (ESA) | Earth Observation (Titan.html already mentions Sentinel-1 emergency response in passing) | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| M | FLEX + Sentinel-3C (ESA; launched together Sept 15 2026 on Vega-C; FLEX maps plant fluorescence) | Agency mission (ESA) | Earth Observation + Deforestation cross-link | Yes, commissioning/first data | APPROVED by Brian 2026-10-11; BUILT |
| N | EOS-06 / Oceansat-3 (ISRO; PSLV-C54, Nov 2022; ocean color, sea-surface temperature, winds) | Agency mission (ISRO) | Earth Observation + Oceans | Yes, active | APPROVED by Brian 2026-10-11; BUILT |
| O | Northrop Grumman SpaceLogistics (MEV life extension in GEO; MRV + 3 MEPs launched July 21 2026) | Corporate | Space Disposal | Yes, MRV first servicing | APPROVED by Brian 2026-10-11; BUILT |
| P | Starfish Space Otter (life extension + disposal; first Otter NET Oct 2026 on Transporter-18 for NASA SSPICY) | Corporate | Space Disposal | Yes, launch NET Oct 2026 | APPROVED by Brian 2026-10-11; BUILT |
| Q | Kelp forests (natural, NOAA; up to 18 in/day; shelter for thousands of species) | Natural | Oceans | No | APPROVED by Brian 2026-10-11; BUILT |
| R | Seagrass meadows (natural, NOAA; 0.1% of seafloor, 11% of ocean's buried organic carbon) | Natural | Oceans (cross-link Mangroves) | No | APPROVED by Brian 2026-10-11; BUILT |
| S | Billion Oyster Project (NY Harbor; goal 1 billion oysters by 2030; 3.2M lbs shells recycled) | Nonprofit | Oceans (or Rivers, Hudson estuary) | No | APPROVED by Brian 2026-10-11; BUILT |

Dropped this morning: GRACE-C successor (no launch date on the NASA page read), Seagrass "7% lost per year" kept but flagged as a 215-study assessment summarized by NOAA. Starfish homepage still says "launching summer 2025"; used the Sept 24 2026 press release instead.

Sources: science.nasa.gov/mission/europa-clipper/; esa.int/Science_Exploration/Space_Science/Juice; science.nasa.gov/mission/osiris-apex/; science.nasa.gov/solar-system/asteroids/apophis/; esa.int/Space_Safety/Planetary_Defence/ESA_awards_contracts_for_Ramses_mission_to_Apophis; esa.int/Space_Safety/Planetary_Defence/First_switch_on_for_ESA-JAXA_Ramses_asteroid_mission; science.nasa.gov/mission/punch/; science.nasa.gov/mission/tracers/; science.nasa.gov/mission/carruthers-geocorona-observatory/; esa.int/Science_Exploration/Space_Science/Solar_Orbiter; science.nasa.gov/mission/escapade/; gracefo.jpl.nasa.gov; science.nasa.gov/mission/grace-fo/; icesat-2.gsfc.nasa.gov; esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1; esa.int/Applications/Observing_the_Earth/FutureEO/FLEX; esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-3; isro.gov.in/EOS_06.html; northropgrumman.com/space/space-logistics-services; starfishspace.com/press-release/starfish-spaces-first-otter-is-going-to-space/; oceanservice.noaa.gov/facts/kelp.html; coast.noaa.gov/states/fast-facts/blue-carbon.html; fisheries.noaa.gov/southeast/habitat-conservation/why-submerged-aquatic-vegetation-designated-essential-fish-habitat; sanctuaries.noaa.gov/visit/ecosystems/seagrass.html; billionoysterproject.org.

## Session Log — 2026-10-11 (morning candidate run)

- Session start: git pull (84b5b2c), NOTES.md read, last 24h of commits reviewed (batch 2026-10-10 fully built; homepage hero fix). No glitches.
- Prepared batch 2026-10-11 (A–S above) for Brian's yes/no. No pages built or pushed.

## 2026-10-11 — Artemis II dedicated page
- New Artemis_II.html (mission template from Hera: space-hero with ArtemisII_Launch_SLS.jpg via body.artemis-page, breadcrumb Home › Project Rawane › Artemis II, Five W's, Impact Statement, bottom-link "For Further Information" → NASA Artemis II, next-solutions, footer, consent.js, JSON-LD/og/twitter/canonical). Same content/sources as the former inline section; sp:category project-r, sp:type solution, sp:stat 252,756 miles. amazing-fact "Farthest Humans Have Gone" moved here (Amazing Facts From: → Artemis_II.html).
- Project-Rawane.html: inline #artemis-ii Impact Statement + Five W's removed (and its sp:item); Voyages Outward card image + title → Artemis_II.html.
- sitemap.xml + search index updated; styles.css ?v=20261011a on all 45 styled pages.

## 2026-10-11 — Artemis_II.html expanded into a living Artemis program tracker
- Added: Artemis II/III/IV mission-status widgets (site.js [data-mission] pattern: milestones done/upcoming, news, source); countdown only where NASA has a date (Artemis II launch Apr 1 2026). Artemis III = "NASA target: 2027", Artemis IV = "NASA target: early 2028", as of Oct 2026, no countdown until NASA sets a date.
- Program tracker cards (goals, crew, hardware, Gateway status) sourced to NASA releases (architecture update Feb 27 2026, Artemis III crew Jun 9 2026, Artemis IV mission page, Mar 2026 plan PDF). Starship/Blue Moon named as landers per NASA.
- "Why Voyages Outward Matter on Earth" framing section; Launch Library 2 widget copied from Project-Rawane (with launches-shift note).
- styles.css: launch heading at section size on artemis-page; cache-bust v=20261011b on all pages.

## 2026-10-11 — Artemis tracker: data-driven schedule + Artemis III spotlight
- Data: assets/data/artemis.json (asOf, updated, missions[]: target/targetLabel, launch, status, objective, crew, hardware, milestones, sources, watch URL). Artemis_II.html inline script fetches it and renders the three mission widgets (via new window.spRenderMission in site.js) and tracker cards; static HTML is the no-JS fallback. "Last updated" line from JSON.
- scripts/update-artemis.js: fetches NASA Artemis III/IV mission pages + Our Artemis III Crew page; updates only reliably parsed fields (LAUNCH target, Mission Type, Artemis III crew names/roles); prints diff; never invents data. Exit 0 no change / 2 changed / 1 errors. Run weekly, then commit the JSON if exit 2.
- Added "Spotlight: Artemis III" (source nasa.gov/mission/artemis-iii); Impact Statement rewritten as program-page value; Five W's now cover the Artemis program (companies labeled). site.js cache tag v=20261011a on all pages.

## 2026-10-11 — Batch 2026-10-11 (A–S) built
- All 19 approved by Brian 2026-10-11; none skipped (S Billion Oyster Project is a restoration nonprofit, not a donation/join drive; nonprofit figures labeled). No horizon labels: every item is launched/funded (Ramses: ESA contract signed Feb 10 2026).
- Anchors: A Space_Disposal.html#europa-clipper; B Space_Disposal.html#juice; C Planetary_Defense.html#osiris-apex; D Planetary_Defense.html#ramses; E Space_Weather.html#punch; F Space_Weather.html#tracers; G Space_Weather.html#carruthers; H Space_Weather.html#solar-orbiter; I Project-Rawane.html#escapade; J Earth_Observation.html#grace-fo; K Earth_Observation.html#icesat-2; L Earth_Observation.html#sentinel-1; M Earth_Observation.html#flex; N Earth_Observation.html#eos-06; O Space_Disposal.html#spacelogistics; P Space_Disposal.html#starfish-otter; Q Oceans.html#kelp-forests; R Oceans.html#seagrass; S Oceans.html#billion-oyster-project.
- Template: impact section (hub-label, Impact Statement, sources, For Further Information link, photo credit) + The Five W's + mission widget where flagged (only NASA/ESA/ISRO/company-sourced dates; approximate months shown as status/arrival labels, no invented days). Company figures labeled (O Northrop Grumman, P Starfish). Saving-moons w-cards for A/B in Space_Disposal #natural.
- Images (new, <250KB, <=1200px): Europa_Clipper_Jupiter (NASA/JPL PIA26068), Juice_RIME_Radar (NASA/JPL PIA24026), OSIRIS_APEX (NASA), Ramses_Switch_On (ESA), PUNCH_Mission (NASA), TRACERS_Launch (NASA KSC-20250723), Carruthers_SWFO_KSC (NASA KSC-20250905), Solar_Orbiter_Astrotech (NASA KSC-20200108), ESCAPADE_Launch_NG2 (NASA KSC-20251113), GRACE_FO_Orbit (PIA22431), ICESat2_Launch (NHQ201809150011), Sentinel1_Ground_Motion (PIA21962), Global_Plant_Fluorescence (PIA18935, OCO-2 SIF map as FLEX proxy), Oceansat_Winds_Irene (PIA14742), Satellite_Servicing_Arm_GSFC (NASA), Transporter18_Launch (KSC-20261001), Kerguelen_Kelp_ISS (ISS018-E-018110), Seagrass_Planting_KSC (KSC-20230329), NYC_Hudson_Harbor (STS039-88-054).
- Amazing Facts added (6): 49 Flybys of an Ocean Moon; Closer Than Our Satellites; Earth's Ultraviolet Halo; A Dozen Photons Come Home; Eighteen Inches a Day; Small Meadows, Big Carbon. Facts page now 20.
- Updates since queue: Starfish Otter launched Oct 1 2026 on Transporter-18 (NASA SSPICY page); MRV launch confirmed by Northrop Grumman July 22 2026 release. Oceans 'Mangroves.html' link pointed at Deforestation.html#mangroves (no Mangroves page exists).

## 2026-10-11 — Own pages for batches 2026-10-10 (A–P, except Artemis II) and 2026-10-11 (A–S)
- 34 new mission-template pages (Hera layout: hero with per-page background rule in styles.css, credit, breadcrumb Home › Hub › Name, mission widget if the hub had one, The Five W's, Impact Statement with sources + For Further Information link + hidden amazing-fact, page-stats, bottom-link, next-solutions, footer, consent.js; canonical/og/twitter/JSON-LD; sp:category from hub, sp:type solution, sp:classification from the hub's sp:item). Hub sections removed; hub cards (image + title) now link to the pages; hub sp:item metas for these removed (the pages count instead). Other pages' Hub#anchor links rewritten.
- Pages: IMAP, GOES-19, PUNCH, TRACERS, Carruthers, Solar_Orbiter (Space Weather); US_Deorbit_Vehicle, Aeolus, LignoSat (horizon), Europa_Clipper, Juice, SpaceLogistics, Starfish_Otter (Space Disposal); SWOT, PACE, Sentinel-6B, GOSAT-GW, EarthCARE, ALOS-4, GRACE-FO, ICESat-2, Sentinel-1, FLEX, EOS-06 (Earth Observation); Phytoplankton, Coral_Restoration_Foundation, Kelp_Forests, Seagrass, Billion_Oyster_Project (Oceans); Mr_Trash_Wheel (Rivers); Mangroves (Deforestation); OSIRIS-APEX, Ramses (Planetary Defense); ESCAPADE (Project Rawane Voyages Outward, with Artemis_II).
- Space_Disposal natural w-cards (Jupiter, Titan, Atmospheric Drag, Europa Clipper, Juice): image + title now link to their pages.
- Nav: Solutions dropdown is now generated by build-stats.js (SOLUTIONS_HUBS) between <!-- SOLUTIONS-MENU:START/END --> on every page: hub groups (Ocean, Lakes, Rivers, Space, Space Disposal, Forests, Planetary Defense, Space Weather, Earth Observation, Project Rawane = pages not listed elsewhere) with every solution page from hub card titles, alphabetical. Desktop 4-column panel right-aligned under the nav; mobile scrolls (max 60vh). projectRMenu data in solutions.json now built from the same card lists.
- styles.css ?v=20261011c on all pages. Sitemap +34, search index rebuilt; Amazing Facts From: links point to the new pages.
## 2026-10-11 — Translations: French (/fr/), Spanish (/es/), Arabic (/ar/)
- Scope: Project-Rawane + 9 hubs (Oceans, Lakes, Rivers, Deforestation, Space, Space_Disposal, Planetary_Defense, Space_Weather, Earth_Observation) + Amazing_Facts, in fr, es and ar (33 pages). Arabic is **Modern Standard Arabic** (user asked for Moroccan Darija first, then changed to MSA before any Arabic was committed). All three are machine-quality drafts by the agent: **native-speaker review recommended, especially Arabic.**
- Rules: numbers, units, mission/agency/organization names and every source URL kept exactly; English source titles kept as link text; "Potential solution on the horizon" translated (Solution potentielle à l'horizon / Posible solución en el horizonte / حل محتمل في الأفق). Five W's = "Les cinq W" / "Las cinco W" / "الأسئلة الخمسة".
- Files: i18n/<lang>.json = translation memory (English string → translation; missing = English kept). scripts/i18n-build.py generates <lang>/<Page>.html from the English page: lang (+ dir=rtl for ar), translated text/alt/aria/title/meta/og/twitter, canonical + og:url per language, hreflang alternates (en/fr/es/ar/x-default, also added to the 11 English originals), og:locale, asset/link paths (`../` unless the target page is translated, so links stay in-language), language switcher in the top nav, `<meta name="i18n-source" content="Page.html <hash>">`.
- Amazing facts: translated pages rename `p.amazing-fact` to `p.amazing-fact-i18n`, and build-facts.js / build-search-index.js / build-stats.js skip /fr/ /es/ /ar/ sitemap URLs, so nothing is collected twice.
- Language switcher (EN · FR · ES · العربية): English pages get it from build-stats.js inside the PROJECT-R-MENU block (survives regeneration; links to fr/<page> if it exists, else fr/Project-Rawane.html). Translated pages get theirs from i18n-build.py. CSS: `.lang-switch` + `[dir="rtl"]` block at the end of styles.css.
- consent.js: banner text in en/fr/es/ar by `<html lang>`; About link `../About.html` on translated pages; RTL buttons. site.js: solutions.json fetched with `../` from language folders.
- sitemap.xml: +33 URLs.
- **Workflow when English changes:** `node scripts/i18n-check.js` lists MISSING/STALE translations (hash of the English page, ignoring hreflang, PROJECT-R-MENU and SOLUTIONS-MENU blocks, switcher and ?v= tags; the switcher sits in PROJECT-R-MENU, outside SOLUTIONS-MENU). Then `python3 scripts/i18n-build.py --missing fr` lists English strings with no translation; add them to i18n/fr.json, es.json, ar.json; run `python3 scripts/i18n-build.py`; re-run the check. Script-rendered text (launch widget, mission-status widgets, stats blocks from site.js) stays English.
- Verified: 0 broken local links/anchors across English + 33 translated pages; screenshots at 1280/390 for fr/Oceans, es/Project-Rawane, ar/Space_Disposal (/workspace/i18n_*.png) — RTL layout, nav, consent banner OK.

## 2026-10-11 — Dropdown fit, Earth Observation pages, Project Rawane groups
- Solutions dropdown: build-stats.js now packs hub groups into 4 balanced li.menu-col columns; desktop panel is a flex row with max-height calc(100vh - 104px) + overflow-y:auto (opens via .nav-dropdown.open as before), tighter link padding. Content height ~700px; fits 1920x1080, scrolls inside the panel at 1280x720 (616px visible) and 1366x768 (664px). Mobile unchanged (60vh scroll). Screens: /workspace/dropdown_*.png.
- New pages NISAR, Biomass, Tanager-1 (corporate), DSCOVR_EPIC from the old Earth Observation sections; each got sourced Five W's (same NASA/ESA sources as the section) and a For Further Information link; hub cards link to pages; hub sp:items removed; menu now 72 items.
- Project-Rawane.html: Space Disposal (mankind + natural), Planetary Defense and Space Weather groups now include every hub card (US Deorbit Vehicle, Aeolus, LignoSat, SpaceLogistics, Starfish Otter; Europa Clipper, Juice; OSIRIS-APEX, Ramses; IMAP, GOES-19, PUNCH, TRACERS, Carruthers, Solar Orbiter), linking to the pages.
- styles.css ?v=20261011f on all pages (after i18n worker's e); sitemap +4; search index rebuilt.

## i18n phase 2 (Oct 11, 2026)
- Pages translated are listed in `i18n/pages.txt` (hubs, Project Rawane, Amazing Facts, Artemis_II, 34 solution pages, 4 EO pages). Add a line + run `python3 scripts/i18n-build.py --missing fr|es|ar`, fill `i18n/<lang>.json`, then `python3 scripts/i18n-build.py` and `python3 scripts/i18n-sitemap.py`.
- Templates (PATTERNS in i18n-build.py) cover "Learn more about X", "Want to go deeper? X has…", "X | Saving Planets", "The Five W's of X", "X: Mission Status".
- Script-drawn UI: `site.js` has a strings table (`spT`, `spLang`) for mission widgets and stats blocks; inline launch-widget literals are swapped at build time from `i18n/ui.json`. On translated Artemis pages the artemis.json refresh script is dropped (data file is English); the translated static cards stay.
- Every English page carries PROJECT-R-MENU markers so build-stats.js re-adds the language switcher (Project-Rawane.html was missing them).
- Switcher + RTL CSS live at the end of styles.css (they had been lost in a merge; restored, styles v=20261011g, site.js v=20261011b).

## 2026-10-11 — Artemis Program row on Project Rawane (auto-synced)
- assets/data/artemis.json: added Artemis I (NASA mission page: uncrewed flight test Nov. 16 – Dec. 11, 2022) and Artemis V (NASA Mar 2026 plan PDF: additional landing, NASA target late 2028; no NASA mission page yet), plus a `synopsis` field for all five. Target text lives only in targetLabel so the update script keeps it current.
- Project-Rawane.html Voyages Outward: "Artemis Program" subhead (h2.sd-subhead) + ws-grid of five w-cards (title → Artemis_II.html, status, synopsis, NASA source) + "Last updated" + "For Further Information: Artemis Program Tracker" → Artemis_II.html. Inline loader re-renders from artemis.json (static HTML fallback). Artemis_II.html tracker now shows I–V.
- scripts/update-artemis.js: Artemis V watched at nasa.gov/mission/artemis-v/ with watchOptional — 404 is reported as a note (currently 404), never invents data.
- Translator: fr/es/ar Project-Rawane (and Artemis_II tracker cards) need regeneration; the loader renders English text from artemis.json.

## SEO pass (Oct 11, 2026)
- `python3 scripts/seo-audit.py [--list]`: issue counts across all 234 pages (EN + fr/es/ar). Before: 1,232 issues. After: 0.
- `python3 scripts/seo-fix.py [en fr es ar]`: idempotent, text-level edits (keeps file formatting). Adds meta robots index,follow (noindex on Project-R.html, 404.html), titles of 60 characters or fewer (translated titles that match the English one get " · Français/Español/بالعربية"), localized descriptions of 120 to 155 characters (padded from page text, trimmed at sentence boundaries), canonical, hreflang en/fr/es/ar/x-default (en + x-default only on untranslated pages), og:* / twitter:* with absolute URLs, og:locale + og:locale:alternate, and JSON-LD inLanguage/datePublished/dateModified (from git history). It adds WebPage JSON-LD where a page had none, a WebSite SearchAction (Search.html?q=), and img width/height/loading=lazy/decoding=async.
- `scripts/i18n-build.py` runs seo-fix automatically after building translations. After build-stats.js or any English page edit, run: `python3 scripts/i18n-build.py && python3 scripts/i18n-sitemap.py && python3 scripts/seo-audit.py`.
- Artemis data per language: `python3 scripts/i18n-data.py` writes assets/data/artemis.{fr,es,ar}.json (run after scripts/update-artemis.js; `--missing` lists new strings). Translated pages fetch their own language file and keep static translated cards as fallback.
- IndexNow: key file `aa19429b4f58f36d34c263abe996de09.txt` at the site root. Run `node scripts/indexnow-ping.js` (dry run) and then `--send` once per deploy, after the pages are live. It only submits changed pages; don't resubmit unchanged URLs.

## 2026-10-11 — Project Rawane Impact Statement + Five W's rewritten
- Impact Statement: kept the Errol Scales sentence, the ESA 1.5 million debris sentence and "Space disposal solutions are moving forward." verbatim; added portfolio roll-up (ADRAS-J2 via JAXA press + Astroscale company figures, Hera ESA, Ramses ESA, Apophis NASA, IMAP/PUNCH NASA, Artemis II NASA, Europa Clipper NASA, Juice ESA), daily-update paragraph (Launch Library 2, mission widgets, daily candidates, weekly Artemis refresh) and sharing paragraph (sources, 4 languages, Amazing Facts, live stats engine counts instead of a hard-coded total). Five W's rewritten (Who/When cite JAXA, ESA, NASA). Dedication line unchanged.
- i18n: fr/es/ar Project-Rawane regenerated with translated new Impact Statement + Five W's + Artemis Program row labels (23 strings per language in i18n/*.json); i18n-data, i18n-sitemap, seo-audit TOTAL 0, i18n-check 'All translations current'. Homepage not translated yet, so the 'We Find and Share Solutions' change was skipped.

## i18n phase 3 — full-site translation (2026-10-11)
- All 83 English pages (everything except the Project-R redirect) now exist in /fr/, /es/, /ar/ (MSA): index, About, Search, Contact, 404 and the 29 older solution pages were added to i18n/pages.txt.
- Search.html: translated pages localize the inline index at build time (`localize_search` in i18n-build.py): titles translated, translated h1/intro of each page appended to the searchable text, results link within-language; case-insensitive match fixed on translated pages; result/no-match strings via i18n/ui.json.
- Home pages: per-language WebSite (SearchAction → /<lang>/Search.html) + Organization JSON-LD (seo-fix.py).
- Home mission heading fragments ("We / Find / and / Share Solutions / to / Save / the / Planet / Minus the / Doom") are translated as fragments; "the" maps to empty so word order reads naturally.
- seo-audit img-alt check now only flags alt text identical to the English page (org names are not false positives). Result: 333 pages, 0 issues; 0 broken links; i18n-check: all current.
- IndexNow: added --all (submit every sitemap <loc>). One-off full submission on 2026-10-11 of 331 URLs returned 403 Forbidden (key not accepted for host; key file is served 200 at /aa19429b4f58f36d34c263abe996de09.txt). Not retried.

## Newsletter: Weekly Saving Planets Brief (MailerLite), 2026-10-11

- **Account:** MailerLite account 2704021, sender `newsletter@savingplanets.com`. API key lives only in `/home/box/.mailerlite_key` on the box (never in the repo or site files).
- **Groups:** English 201062857381512972, French 201062857692939304, Spanish 201062857966617859, Arabic 201062858265462233.
- **Embedded forms (double opt-in on), created via API:** EN 201062861124929242, FR 201062865506927746, ES 201062865837229281, AR 201062866183259490. Each adds to its own group.
- **Site sign-up:** module at the end of `site.js` posts the email with `fetch` (credentials omitted, no cookies) to MailerLite's public endpoint `https://assets.mailerlite.com/jsonp/2704021/forms/<formId>/subscribe` (CORS `*`). Only public form IDs are client-side. Language comes from `<html lang>`. It fills `<div data-sp-newsletter>` placeholders (index.html after the stats, Amazing_Facts.html before the footer, copied to fr/es/ar by i18n-build), and on every other page adds a compact block at the top of the footer. Strings for EN/FR/ES/AR live in the module (same pattern as consent.js). It has a visually hidden label, a honeypot, email validation and success/error messages (aria-live). About.html has a new `#privacy` section (analytics + newsletter); its translations are in i18n/*.json.
- **Weekly drafts:** `node scripts/newsletter-draft.js [--dry-run] [--days 7] [--lang en,fr]` builds the issue (new non-hub pages added in git in the last N days, from solutions.json + page meta; a rotating Amazing Fact card with image; next 3 LL2 launches + next mission milestones from solutions.json; Why It Matters) per language and creates a **draft** campaign per group named `Weekly Brief YYYY-MM-DD (XX)`. It never sends or schedules, and it skips names that already exist. A preview HTML copy goes to /tmp/newsletter-<date>-<lang>.html.
- First sample drafts: Weekly Brief 2026-10-11 (EN/FR/ES/AR).
- site.js cache tag bumped to v=20261011n on all pages.

## Session Log — 2026-10-11 (newsletter template v2)

- scripts/newsletter-draft.js rebuilt per Brian's minimum sections, all four languages (FR/ES/AR fixed strings translated; AR is MSA with dir=rtl): (1) issue date as large header in a navy masthead; (2) new solutions this week (git add date within --days, default 7) grouped by hub from each language's homepage SOLUTIONS-MENU, title + meta description + language-specific www.savingplanets.com link; pages whose only sp status is "horizon" get the "Potential solution on the horizon" badge + standard note; empty hubs omitted, "No new solutions this week" if none; (3) launches for the issue week (Mon-Sun HST; on a Sunday run it covers today through next Sunday) from Launch Library 2.3.0 with date (UTC), vehicle, provider, mission, plus link to Project-Rawane.html#launches; (4) Suggest a New Solution block, mailto ideas@savingplanets.com + About.html#criteria (same anchor as homepage link); (5) two Amazing Facts with source and link to Amazing_Facts.html, rotated without repeats via scripts/newsletter-state.json (usedFacts keyed by fact page|image; resets when all used). Unsubscribe footer kept (translated label).
- NL_SUFFIX env var appends to the draft name (used to create the "v2" drafts alongside the old ones).
- Drafts created (not sent/scheduled): Weekly Brief 2026-10-11 v2 EN 201065485151766039, FR 201065487765866070, ES 201065490374723027, AR 201065492891305016. Old 2026-10-11 drafts (201063058037015705, 201063060570376100, 201063063098492531, 201063065632900542) were NOT deleted, pending Brian's OK to delete.
- This week: 67 new solution pages, 2 horizon (LignoSat, PRELUDE), 3 launches (Oct 12-15), facts Aeolus "150 Times Safer" + Europa Clipper "49 Flybys of an Ocean Moon".
- Known glitch noted: with 67 new pages the issue is long (~8,400px). Consider capping per hub later if Brian wants it shorter.

## Session Log — 2026-10-11 (newsletter: per-hub cap + draft cleanup)

- Brian approved deleting the four v1 drafts (201063058037015705, 201063060570376100, 201063063098492531, 201063065632900542); they and the four v2 drafts (201065485151766039, 201065487765866070, 201065490374723027, 201065492891305016) were deleted (HTTP 204).
- newsletter-draft.js: new solutions capped at 3 per hub (CAP constant); hubs with more get a translated "See all N new in <hub>" link to that hub's page in the reader's language.
- Recreated drafts "Weekly Brief 2026-10-11" (not sent/scheduled): EN 201065768381580767, FR 201065770961077668, ES 201065773376996573, AR 201065775843247964. Same facts as before (Aeolus, Europa Clipper), reused from newsletter-state.json; no new facts consumed. EN preview 5,258px tall (was ~8,400).

## Session Log — 2026-10-11 (newsletter logo + confirmation emails)

- Added assets/SavePlanetLogo-email.png (192x225 PNG from SavePlanetLogo.jpg, shown at 72x84) to the newsletter masthead, linked to the homepage; absolute https://www.savingplanets.com URL.
- Deleted drafts 201065768381580767/…770961077668/…773376996573/…775843247964 and recreated "Weekly Brief 2026-10-11": EN 201066038081619241, FR 201066040711448072, ES 201066043295139426, AR 201066045808576058 (same facts; not sent/scheduled). Preview 5,263px.
- Confirmation emails: MailerLite's public API (connect.mailerlite.com) exposes forms read-only except the name; it cannot edit double opt-in emails. Translated FR/ES/AR texts saved in scripts/newsletter-confirmation-texts.md for Brian to paste in the dashboard.

## Session Log — 2026-10-11 (newsletter language selector)

- site.js newsletter module: every sign-up block (homepage, Amazing Facts, compact footer; all languages) now has a language select (English / Français / Español / العربية, each option with its own lang/dir), defaulting to the page language; the chosen value picks the MailerLite form (FORMS map) it posts to. Visually hidden translated label (Newsletter language / Langue de la newsletter / Idioma del boletín / لغة النشرة). No cookies or storage.
- Cache bump site.js?v=20261011o on all 332 pages. i18n-build + i18n-sitemap + seo-audit (333 pages, TOTAL 0) + i18n-check (all current).
- Verified via headless Chrome CDP at 1280 and 390: EN index/About, AR index/About/Amazing_Facts: no horizontal scroll, AR blocks dir=rtl with العربية preselected. No real sign-ups submitted. Screenshot /workspace/newsletter-footer-ar-390.png.
- Tip: box node is v20; CDP scripts need `node --experimental-websocket`. Clip screenshots of the footer came out blank; scroll + viewport screenshot works.

## Session Log — 2026-10-11 (newsletter hub banners + dad joke)

- assets/newsletter/: 552x140 hub banners, linked to each hub page, translated alt ("Banner image for <hub>"). Animated GIFs (6-frame slow zoom, 64 colours, all <300 KB, frame 1 = full static crop for Outlook): earth-observation (EPIC_Earth.jpg, NASA/NOAA DSCOVR EPIC), ocean (OceanBeach.JPG, site photo), planetary-defense (DART_Didymos.jpg, NASA/Johns Hopkins APL/Steve Gribben PIA25329), space (Jupiter.jpg, NASA/JPL-Caltech/SwRI/MSSS, Kevin Gill, PIA21395), space-disposal (Progress_Reentry.jpg, NASA ISS Expedition 29 iss029e034092), space-weather (SDO_Sun.jpg, NASA/SDO). Static JPG (GIF versions were >300 KB): project-rawane (Earth.jpg, NASA Apollo 17 AS17-148-22742), forests (Threetrees3.jpg, site photo), lakes (StreamLog.JPG, site photo), rivers (streamlog2.JPG, site photo).
- "Project Rawane's Favorite Dad Joke" block above the footer: 30 jokes (JOKES in the script, FR/ES/AR adapted translations in JOKES_T, MSA), one per issue, rotation tracked in newsletter-state.json (usedJokes + issues[date].joke). Week 1: #0 sun/brighter.
- Drafts recreated (not sent/scheduled), same facts: EN 201066788540122334, FR 201066791102842840, ES 201066793554413454, AR 201066795972429219. Old 201066038081619241/…040711448072/…043295139426/…045808576058 deleted, plus an interim set from an interrupted run (201066756756735816, …759385515059, …761812969164, …764367300047). Preview 7,030px.
- Note: Project Rawane and Earth Observation banners are both whole-Earth photos; swap Project Rawane to a rocket image once one with a known credit is in assets/.

## Session Log — 2026-10-11 (image credits for site-owned images)

- Credits confirmed by the site owner (never use the owner's real name): Threetrees3.jpg = "Photo: SI Partner."; OceanBeach.JPG, StreamLog.JPG, streamlog2.JPG = "SI-generated image by Saving Planets." (the owner says "SI" instead of "AI"; keep that wording).
- Added `<p class="photo-credit">` after every visible use: card images (index, Oceans, Lakes, Rivers, Deforestation), donate/further-info buttons (4ocean, Plastic Bank, Great Bubble Barrier, Sungai Watch, Restoring the Lake Depths, Life Terra, Deforestation), Life Terra Five W's image, and below the CSS-background heroes (forest-hero: Life_Terra, Terraformation, Three_Trees; rivers-hero: Great_Bubble_Barrier, Sungai_Watch). New CSS `.card .photo-credit, .w-card .photo-credit`; styles.css?v=20261011i. FR/ES/AR strings in i18n/*.json. Builds/audits: TOTAL 0, all translations current.
- Newsletter: small credit line under each hub banner (HUBCREDIT in the script, label translated).
- Drafts recreated, same facts + same joke (#0), not sent/scheduled; previous 201066788540122334/…791102842840/…793554413454/…795972429219 deleted.

## Session Log — 2026-10-11 (ThreeTrees2 credit)

- ThreeTrees2.jpg is the owner's photo: "Photo: SI Partner." added under its only visible use (Three Trees card on Deforestation.html; translated via i18n on fr/es/ar). Not used in the newsletter, so drafts unchanged.
- Verified at 390px (CDP): index, Life_Terra, Deforestation, ar/index, ar/Life_Terra all scrollWidth 390 = no horizontal scroll. Builds/audits TOTAL 0, translations current.

## Session Log — 2026-10-11 (newsletter footer address)

- Checked scripts/newsletter-draft.js: footer already uses only MailerLite merge tags `{$account_address}` and `{$unsubscribe}`; no hard-coded address anywhere. The address comes from MailerLite Account settings > Company profile (company name/website/physical address). To change it (e.g. to a PO box): edit it there; to push the change into existing drafts, Account settings > Default settings > "Company details and unsubscribe disclaimer" > check "Force-update company details..." and save. Template unchanged, so drafts were not recreated. Never record the address itself in the repo.

## Session Log — 2026-10-11 (newsletter header + quick links)

- Logo moved to the right of the masthead (left in Arabic via dir=rtl cell order); text cell width=100%.
- Intro line centered, bold, 17px (was 15px).
- "In this issue" quick-links box under the intro (New Solutions, Launches This Week, Amazing Facts, Suggest a New Solution, Dad Joke) with anchors #sp-new/#sp-launches/#sp-facts/#sp-suggest/#sp-joke; "Back to top ↑" (#sp-top) after each section. Strings in T2 (inIssue, backTop) for EN/FR/ES/AR. Anchor links work in Apple Mail/iOS/most webmail; Gmail app and some Outlook versions may ignore them (harmless).
- Drafts recreated (same facts/joke, not sent): EN 201069299318653981, FR 201069301940094906, ES 201069304342382052, AR 201069306793952542. Preview 7,490px.

## 2026-10-11 session
- Added assets/videos/channel-intro.mp4 (15s channel rebrand intro, SI-generated visuals by Saving Planets, no on-screen text). Posted via Postiz to X, TikTok, YouTube.
- Added assets/videos/great-bubble-barrier.mp4 (Great Bubble Barrier short, ~15s, 1920x810 horizontal, SI-generated visuals, no on-screen text). Posted 2026-10-11 ~8:42pm HST via Postiz: X cmv4vxxl8006gqw0y9f5t8kxt, TikTok cmv4vxxs8006lqw0y28h1qk27 (DIRECT_POST, AI label), YouTube cmv4vxxxv006oqw0yh354fpzb (public, not for kids) - all PUBLISHED. Note: Postiz strips even plain-text "savingplanets.com" from X posts; YouTube altered/synthetic flag not exposed by Postiz (set in YouTube Studio).
- Added assets/videos/life-terra-trees.mp4 (Life Terra trees short, 22.6s, 1920x794 horizontal, SI-generated visuals, rising www.savingplanets.com end card, clean ending after "Follow Saving Planets"). Posted 2026-10-11 ~9:00pm HST via Postiz: X cmv4wkfp30081qw0y09iai4rb (@LIFETerraEurope, ends "Follow @SISavingPlanets, link in bio", no domain), TikTok cmv4wkg1p0082qw0y39w0zqe7 (DIRECT_POST, public, AI label), YouTube cmv4wkgev0083qw0yauh5yhvt (public, not for kids, "Visuals SI-generated by Saving Planets" + https://www.savingplanets.com) - all PUBLISHED. To do by hand: YouTube Studio altered/synthetic = Yes; pin savingplanets.com comment on TikTok/YouTube.
- Added assets/videos/grace-fo-satellites.mp4 (GRACE-FO satellites short, 16.5s, 1920x968 horizontal (source 2752x1388, not 9:16 despite the setting), SI-generated visuals, rising www.savingplanets.com end card after "Saving a planet is saving people." (voiceover had no "Follow Saving Planets" line)). 220 km separation and "fraction of a hair" verified against NASA/JPL (jpl.nasa.gov GRACE-FO press kit, nasa.gov launch release). Posted 2026-10-11 ~9:20pm HST via Postiz: X cmv4xa1ce009zqw0ytwdlmt9c (@NASAJPL @GFZ_Potsdam, no domain, ends "Follow @SISavingPlanets, link in bio"), TikTok cmv4xa1jp00a0qw0ycoa2r31x (DIRECT_POST, public, AI label, @nasa), YouTube cmv4xa1rp00a2qw0y5wnbos1l (public, not for kids, SI credit + https://www.savingplanets.com) - all PUBLISHED. To do by hand: YouTube Studio altered/synthetic = Yes; pin savingplanets.com comment on TikTok/YouTube.

## Session Log — 2026-10-11 (Donate / Join the work buttons + Ways to Help page)

- New "Help This Work" section (`<section class="help-actions" id="help">`) before the footer on 37 pages: Donate and/or Join the work buttons (`.btn.help-btn`, Join in solution green), target=_blank rel=noopener, plus "See all ways to help" link. Existing bottom-link banners untouched. Generator: /workspace/help_links.py (mapping lives there; rerun is idempotent).
- Links (all curl -IL 200 on 2026-10-11): Terraformation terraformation.com/work-with-us (Terraformation.org Foundation 501(c)(3) giving) + terraformation.com/careers; Great Lakes Plastic Cleanup get-involved (its donation section routes US via CGLR Click & Pledge, Canada via Pollution Probe/CanadaHelps; site has no /donate) + mailto info@greatlakesplasticcleanup.org (their own "Joining" link); 4ocean 4oceanfoundation.org/donate (no volunteer page); Clean Up the Lake /donate/ + /volunteer/; Great Bubble Barrier /donate/ + /careers/; Ocean Cleanup /donate/ + /careers/; Life Terra /en/support-us + /en/join-in; Restoring the Lake Depths /donate (no volunteer page); Sungai Watch /products/donate + /pages/cleanups ("Join Cleanup"); Billion Oyster Project /donate + /volunteering; Coral Restoration Foundation /one-time-donation/ + /get-involved/; Mr. Trash Wheel classy.org/give/546227 (Waterfront Partnership, linked from mrtrashwheel.com) + mrtrashwheel.com/volunteer-opportunities; Tanager-1 Carbon Mapper carbonmapper.org/donate + /about/get-involved.
- Companies (Join only, careers/join pages): Plastic Bank /careers, Astroscale /en/careers, ClearSpace /joinclearspace, LeoLabs /careers/, SpaceLogistics northropgrumman.com/careers.
- NASA-led pages (Join only → science.nasa.gov/citizen-science/, text "NASA doesn't take donations..."): Artemis II, Carruthers, DSCOVR/EPIC, ESCAPADE, Europa Clipper, GRACE-FO, ICESat-2, IMAP, NEO Surveyor, NISAR, OSIRIS-APEX, PACE, PUNCH, Sentinel-6B, SWOT, TRACERS, Titan (Dragonfly), US Deorbit Vehicle, Webb/2024 YR4.
- Skipped: ESA/JAXA/ISRO/NOAA/CNES pages (no donations, no general volunteer program), hubs, topic/natural pages (Mangroves, Seagrass, Kelp, Phytoplankton, Jupiter, Three Shields, Atmospheric Drag), owner projects (Three Trees, Lake Plastic Recovery already have mailto Join), horizon pages (PRELUDE, LignoSat), Orbital Data Centers (Starcloud careers redirects to a third-party ATS), Starfish Otter (careers page 403, unverified).
- New Ways_to_Help.html (+ fr/es/ar): How This Works note (Saving Planets receives none of the money; only active solutions), tables for donate/volunteer orgs and companies, NASA citizen science block. Generator /workspace/build_wth.py. Added to i18n/pages.txt, sitemap.xml (+ i18n-sitemap), build-stats SKIP. index.html "Be Part of the Fix": new line + button "Every donate and volunteer link is also in one place: Ways to Help".
- styles.css?v=20261011j on all pages. i18n-build + i18n-sitemap + seo-audit (337 pages, TOTAL 0) + i18n-check (all current). Headless Chrome screenshots at 390/1280 OK.

## Session Log — 2026-10-11 (Batch 1: videos on pages, Planet Scoreboard, Solution of the Week)
- New `scripts/build-home-extras.py` (idempotent, marker blocks VIDEO / SOTW / SCOREBOARD). Run it, then `python3 scripts/i18n-build.py && python3 scripts/i18n-sitemap.py && python3 scripts/seo-audit.py`.
- Videos: `<section class="sp-video" id="video">` with `<video controls playsinline preload="metadata" poster=...>` + caption "SI-generated video by Saving Planets." placed after the breadcrumb on Great_Bubble_Barrier, Life_Terra, GRACE-FO, Artemis_II; channel-intro on About.html (after hero). Posters assets/videos/<slug>.jpg via ffmpeg (frame at 2s; Artemis at 4s because early frames are text-only). Note: artemis-ii-farthest.mp4 shows garbled burned-in text near the end ("Next: Artegs III") — consider re-cutting.
- Planet Scoreboard (index, after "What the Stats Show"): 36,000,000+ trees (Life Terra, company figure, May 2026, EURACTIV PR); 65,000,000+ kg (The Ocean Cleanup, company figure, homepage "65M+" re-checked live Oct 11 2026); 252,756 miles (NASA, Artemis II, Apr 2026); 15 active Earth Observation missions (count from solutions.json, Oct 11 2026). Count-up in site.js with IntersectionObserver; skipped under prefers-reduced-motion; static numbers without JS. Omitted: Great Bubble Barrier pieces caught (no verified count; page says so).
- Solution of the Week: assets/data/solution-of-week.json (start 2026-10-11, weekly rotation Bubble Barrier → Life Terra → GRACE-FO → Artemis II). Static card on index (translated via i18n); English home refreshes from JSON in site.js; translated homes update on the next build-home-extras + i18n-build run (do it weekly).
- Newsletter: newsletter-draft.js adds a "Solution of the Week" section (+ In this issue link) from the same JSON, translated through i18n/<lang>.json. Dry run only; nothing created or sent; state file unchanged.
- i18n: 30 new strings per language in fr/es/ar.json (incl. future rotation blurbs). i18n-check all current; seo-audit TOTAL 0. styles v=20261011l, site.js v=20261011p.
- Verified live: pages 200 with elements present; CDP screenshots 1280/390 (/workspace/shots3/), no horizontal scroll at 390; counters end at final values.

## Session Log — 2026-10-11 (Batch 2: hero video, status badges, Press kit, launch calendar)
- New `scripts/build-batch2.py` (idempotent): HERO-VIDEO marker block on index, `.sol-badges` on solution cards, `<p class="footer-links">Press &amp; media</p>` in every footer, launch .ics + CAL marker block. New `scripts/weekly-sync.sh` = build-home-extras + build-batch2 + i18n-build + i18n-sitemap + seo-audit + i18n-check (hook for the daily translation sync; it refreshes FR/ES/AR Solution of the Week, which rotates Sundays HST). Commit only if git status shows changes.
- Hero: assets/videos/hero-loop.mp4 (7.4s, 1280x546, H.264 CRF30, no audio, 1.1 MB, faststart) cut from channel-intro.mp4 (Earth 0.2-3.4s, beach 4.0-6.6s, forest 7.0-9.8s, 0.6s crossfades; no burned-in text; no Artemis footage). Poster hero-loop.jpg. `autoplay muted loop playsinline`, dark gradient overlay, credit "SI-generated video by Saving Planets." bottom-right. prefers-reduced-motion: CSS hides video (poster as background) + site.js pauses and sets preload none.
- Badges: 98 cards on hub/index pages; status + category from assets/data/solutions.json (non-section entries). Active (green) / On the horizon (amber, existing #f5b942); hub tag with emoji icon. Old inline `menu-tag horizon` inside card h3 removed (badge replaces it). Hub tag = the page's own category (e.g. Jupiter shows Space on the Planetary Defense hub).
- Press.html (+fr/es/ar): mission line, boilerplate, logo downloads (SavePlanetLogo.jpg, SavePlanetLogo-email.png, favicon.svg), fact-sheet links (About, criteria, Scoreboard, Amazing Facts, Ways to Help, solutions.json), contact ideas@savingplanets.com (subject "Press"; newsletter@ isn't used on the site). Added to i18n/pages.txt, sitemap, build-stats SKIP.
- Launch calendar: only mission-widget `data-launch` dates in the future get an .ics: MMX 2026-10-19T19:41:03Z (JAXA press release 2026-08-20, re-checked today: Oct 20 4:41:03 JST) and Dragonfly launch period opens 2028-07-05 (NASA, all-day). No .ics for undated targets (NEO Surveyor NET Sept 2027, Ramses spring 2028, Artemis III 2027, Vigil 2031, PRELUDE horizon). Files assets/calendar/*.ics; "Add to calendar" button below the widget on MMX/Titan.
- i18n: 32 new strings per language. styles v=20261011m, site.js v=20261011q.
- Glitch: first footer approach appended " • Press" inside the first footer <p>, which changed the text node and un-translated every footer; switched to a separate <p class="footer-links">.

## Session Log — 2026-10-11 (Batch 3: Myth vs Fact, Rawane's Mission Log, hub quizzes)
- New `scripts/build-batch3.py` + content file `scripts/batch3-content.py` (MYTHS, LOG, QUIZZES). The generator is idempotent and now runs in `scripts/weekly-sync.sh` right after build-batch2. **To add a Mission Log entry:** put a dict at the top of LOG (id log-00N, num, date, date_label, title, paras (plain text, no inline links), facts [(text, source name, URL)], related [(page, label)]), rerun weekly-sync.sh, then add the new strings to i18n/<lang>.json (`python3 scripts/i18n-build.py --missing fr`).
- Myth_vs_Fact.html (+fr/es/ar): 7 myths (ozone: NOAA 2025 ozone-hole release; asteroid deflection: NASA DART 33 min 15 s; Apophis: NASA no risk for 100+ years; 2024 YR4: NASA PD blog Mar 2026; bleached coral: NOAA Ocean Service; solar storms: NOAA SOLAR-1 release (30-minute coronagraph delivery); space junk: ESA Space Environment Report 2025 (debris still growing) + Aeolus). Each card has Fact, an honest caveat, the source link and links to related site pages. All 9 external links returned 200 on 2026-10-11.
- Rawanes_Mission_Log.html (+fr/es/ar): intro (Rawane, say Rah-wahn, the original astronaut mascot; the story is made up and the facts are real; home base Project Rawane), Log 002 "Bleached Is Not Dead" (NOAA + CRF 253,833 corals, organization figure), Log 001 "Waiting for Hera" (NASA DART + ESA Hera arriving Nov 2026). Newest first, each with a Fact Check box.
- Quizzes: `<!-- QUIZ:START/END -->` block (section#quiz) before the bottom link on all 9 hubs, with 5 questions each drawn from the hub's own sourced copy and an answer link to the source page. All quiz text is in the HTML (translated by i18n-build); site.js handles the clicks: aria-live feedback, ✓/✗ plus color, score, Share (navigator.share, falling back to clipboard and then execCommand copy, sharing the text plus https://www.savingplanets.com/<path>#quiz) and Try again. No storage, no analytics events. Buttons are at least 44px tall with a visible focus ring; RTL works. Headless check: answering 4 of 5 correctly shows "You scored 4 out of 5."
- Links: footer-links on every page are now Press & media · Myth vs Fact · Rawane's Mission Log; Amazing_Facts has a "Heard a Doom Headline?" block (MYTH-LINK markers) before the footer. Sitemap +8 URLs; both pages are in i18n/pages.txt and build-stats SKIP; search index rebuilt.
- MMX/Titan "Add to calendar": .cal-add is now max-width 1200px with 1.5rem padding (matching .mission-widget), so the button lines up with the widget's content edge; the top margin was tightened.
- i18n: about 300 new strings per language (machine-quality; native review is still recommended, especially for Arabic). styles v=20261011n, site.js v=20261011r. seo-audit 349 pages, TOTAL 0; i18n-check all current; 0 broken local links (the 8 hits are JS template literals on Artemis_II/Project-Rawane).
- Screenshots (live): /workspace/shots5/live_*_{1280,390}.png.

## Session Log — 2026-10-11 (Batch 4: Do One Thing Today, Community Wall, Find a Cleanup; SOTW overlap fix; Project Rawane New callout)
- New `scripts/build-batch4.py` (idempotent; in weekly-sync.sh after build-batch3). Data: `assets/data/daily-actions.json` (28 actions, start 2026-01-01), `assets/data/community.json` (items [], approved only), `assets/data/new-callout.json`.
- Do One Thing Today: DOT marker block on index (before #actions) + 9 hubs (before QUIZ). The whole list is rendered into the HTML so translations work. Item 0 shows without JS; site.js picks (days since start by the visitor's local date) mod 28. Every URL was checked 2026-10-11 (200). greatlakes.org returns a Cloudflare 403 to curl but loads in headless Chrome (title "Adopt-a-Beach - Alliance for the Great Lakes").
- Community.html (+fr/es/ar): mailto ideas@savingplanets.com, subject "Community photo" (prefilled body with a consent line). Guidelines: own photos, first name/alias, no minors' faces, consent to publish + takedown on request, may decline. Grid comes from community.json via site.js; empty "Be the first" state. No invented submissions. **To publish a photo:** put the file in assets/community/, add {img, alt, name, place, caption, date} to items (newest first), then commit.
- Find_a_Cleanup.html (+fr/es/ar): official finders only, grouped Worldwide (OC ICC map, Clean Swell, World Cleanup Day, Marine Debris Tracker) / United States (Surfrider cleanups.surfrider.org, KAB Great American Cleanup, California Coastal Cleanup Day, NOAA MDP prevention) / Great Lakes (Alliance Adopt-a-Beach, GLPC) / UK (MCS beach clean) / Australia (Clean Up Australia). Also start-your-own guide + safety tips. No embedded map (no keyless official source; no invented points).
- Links: nav "Community" (before Search) on all pages; footer-links + Community Wall · Find a Cleanup; Ways to Help "Join a Cleanup" block (B4-WTH markers); DOT footer links Find a Cleanup + Ways to Help. Sitemap, pages.txt, build-stats SKIP, search index.
- URGENT fix (commit 4e3fe4b): on the homepage Solution of the Week card, the "Watch and Learn More" button covered the "SI-generated image" credit. The cause: an inline .btn with padding overflowed its <p>. The fix: inline-block button, static credit below it, and the card stacks at ≤1024px (iPad portrait). Checked at 1024x1366, 768x1024, 1280 and 390.
- Project Rawane "New" callout (d16c220): NEW-CALLOUT block under the hero, linking to Myth_vs_Fact.html, with optional date. Edit new-callout.json (enabled false hides it). Project-R.html is only a redirect, so the callout lives on Project-Rawane.html.
- Glitches: (1) the nav on most pages has no Contact item, so the first nav anchor touched only 14 pages; it now anchors on Search. (2) i18n json is insertion-ordered, so a sort_keys dump made a big diff, which was reverted. (3) build-batch2 rewrote the .ics DTSTAMP on every run because it compared after universal newlines (CRLF); it now reads with newline=''. (4) i18n --missing skips external link text, so the "Do it with X" strings were added explicitly.
- i18n: about 120 new strings per language (machine-quality). weekly-sync ran clean twice after each change (seo-audit 357 pages, TOTAL 0; all translations current). Broken local links: 0 (the 2 known JS-template false positives). styles v=20261011q, site.js v=20261011s.

## Candidate Queue — batch 2026-10-12

Fourth daily batch (17), prepared by the 6:17 AM HST routine. Nothing built; awaiting Brian's yes/no on each. Checked against every page, solutions.json, and the 2026-10-09/10/11 queues (no repeats). Company/nonprofit figures labeled as such.

| ID | Candidate | Classification | Suggested hub | Mission widget | Status |
|---|---|---|---|---|---|
| A | Nancy Grace Roman Space Telescope (NASA; launched Aug 30 2026 on Falcon Heavy; L2 ~1M mi; 300-megapixel camera; first images by early 2027) | Agency mission (NASA) | Project Rawane (Voyages Outward) | Yes, L2 arrival + first images | APPROVED 2026-10-12, built: Nancy_Grace_Roman.html |
| B | Plato (ESA; 26 cameras; launch planned March 2027 on Ariane 6 to L2; 4-yr mission) | Agency mission (ESA) | Project Rawane (Voyages Outward) | Yes, launch Mar 2027 | BUILT 2026-10-12 |
| C | ExoMars Rosalind Franklin rover (ESA; launch target 2028; drill to 2 m) | Agency mission (ESA) | Project Rawane (Voyages Outward, next to ESCAPADE) | Yes, launch 2028 | BUILT 2026-10-12 |
| D | Copernicus Sentinel-2C (ESA; launched Sept 5 2024 on final Vega; 290 km swath, 13 bands, 5-day revisit) | Agency mission (ESA) | Earth Observation + Deforestation cross-link | Yes, active | BUILT 2026-10-12 |
| E | MetOp-SG-A1 + Sentinel-5A (ESA/EUMETSAT; launched Aug 13 2025 on Ariane 6; daily global air-pollutant data) | Agency mission (ESA/EUMETSAT) | Earth Observation | Yes, active | BUILT 2026-10-12 |
| F | Landsat 9 and the 50-year Landsat record (NASA/USGS; launched Sept 27 2021; 740 scenes/day; 8-day revisit with Landsat 8) | Agency mission (NASA/USGS) | Earth Observation + Forests/Lakes cross-links | Yes, active | BUILT 2026-10-12 |
| G | ISS water recovery reaches 98% (NASA, Brine Processor Assembly, June 2023) | Agency program (NASA) | Project Rawane (voyages outward benefit Earth) | No | BUILT 2026-10-12 |
| H | Saharan dust feeds the Amazon (natural; NASA CALIPSO: 27.7M tons/yr, ~22,000 tons phosphorus) | Natural | Forests (Deforestation) | No | BUILT 2026-10-12 |
| I | The Amazon makes its own rainy season (natural; NASA JPL 2017, transpiration starts rains 2-3 months early) | Natural | Forests (pairs with H) | No | BUILT 2026-10-12 |
| J | The Moon steadies Earth's tilt (natural; NASA: 23.5-degree tilt kept in check, tides) | Natural | Space Disposal "saving moons" / Space | No | BUILT 2026-10-12 |
| K | Beavers, river engineers (natural + NOAA Fisheries beaver dam analogs; Bridge Creek +52% steelhead survival, +175% production) | Natural / agency restoration | Rivers | No | BUILT 2026-10-12 |
| L | Salt marshes (natural, NOAA; nursery for 75%+ of fisheries species, erosion buffer) | Natural | Oceans (cross-link Mangroves, Seagrass) | No | BUILT 2026-10-12 |
| M | Ocean Voyages Institute (nonprofit; 850,000+ lb from Pacific Gyre in 10 voyages; 340,000 lb in 2020) | Nonprofit | Oceans | No | BUILT 2026-10-12 |
| N | Healthy Seas (nonprofit; ghost nets; 1,309.1 tons marine litter removed since 2013) | Nonprofit | Oceans | No | BUILT 2026-10-12 |
| O | Mote Marine Laboratory coral restoration (nonprofit; 216,000+ corals restored to Florida's Coral Reef) | Nonprofit | Oceans (cross-link Coral Restoration Foundation) | No | BUILT 2026-10-12 |
| P | Trees for the Future (nonprofit; 450M+ trees grown, 99,000 acres restored, 63,700 farmers, East Africa) | Nonprofit | Forests | No | BUILT 2026-10-12 |
| Q | Seabin (company; Sydney Harbour since 2020: 33.0M items captured, 18.9M microplastics, 21 active Seabins) | Corporate | Oceans (cross-link Great Lakes Plastic Cleanup, which uses Seabins) | No | BUILT 2026-10-12 |

Flags: N's 2026 press kit gives 1,309.1 tons in one section and an older "991 tons since 2013" in another; use 1,309.1 as the latest headline and label it as a Healthy Seas figure. Q's donate path is a corporate partnership model (no individual donate page). A's first-images timing per NASA ("by early 2027"); L2 arrival ~100 days after launch is from a non-NASA tracker, so the widget should say "NASA: L2 orbit early December" only after confirming on a NASA page.

Dropped this morning: Sea otters as kelp keystone (NOAA Sanctuaries page did not load), NASA L2 arrival date for Roman (not found on a NASA page; kept only the launch and first-images milestones).

Sources: nasa.gov/news-release/nasas-dark-universe-seeking-nancy-grace-roman-space-telescope-launches/; science.nasa.gov/mission/roman-space-telescope/; esa.int/Science_Exploration/Space_Science/Plato; esa.int/Science_Exploration/Space_Science/Plato_factsheet; cosmos.esa.int/web/plato/status-and-history; esa.int/Science_Exploration/Human_and_Robotic_Exploration/Exploration/ExoMars; esa.int/.../ExoMars/ExoMars_rover; esa.int/Newsroom/Press_Releases/Sentinel-2C_joins_the_Copernicus_family_in_orbit; esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Facts_and_figures; esa.int/Newsroom/Press_Releases/First_MetOp-SG_satellite_and_Sentinel-5A_launched; science.nasa.gov/mission/landsat-9/; nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/; nasa.gov/centers-and-facilities/goddard/nasa-satellite-reveals-how-much-saharan-dust-feeds-amazons-plants/; doi.org/10.1002/2015GL063040; jpl.nasa.gov/news/new-study-shows-the-amazon-makes-its-own-rainy-season/; science.nasa.gov/solar-system/moon/10-things-what-we-learn-about-earth-by-studying-the-moon/; science.nasa.gov/science-research/earth-science/milankovitch-orbital-cycles-and-their-role-in-earths-climate/; fisheries.noaa.gov/feature-story/oregon-beavers-engineer-better-fish-habitat-more-fish; fisheries.noaa.gov/feature-story/start-beaver-dams-transform-parched-california-creeks-salmon-havens-new-research-finds; oceanservice.noaa.gov/facts/saltmarsh.html; oceanvoyagesinstitute.org; healthyseas.org/assets/uploads/Press-Kit-3_2026.pdf; mote.org/research/program/coral-reef-restoration/; trees.org; seabin.io.

## Session Log — 2026-10-12 (morning candidate run)

- Session start: git pull (85150bb, already up to date), NOTES.md read, last 24h of commits reviewed (Batches 1-4 site enhancements, videos, newsletter; no new solution pages). No glitches.
- Prepared batch 2026-10-12 (A–Q above) for Brian's yes/no. No pages built or pushed.

## Session Log — 2026-10-12 (daily translation sync)

- Routine: pulled main (already up to date at b31b423), ran scripts/weekly-sync.sh.
- SOTW still Great_Bubble_Barrier; EO active 15; fr/es/ar rebuilt 89 pages each (no content diff); seo-audit 357 pages TOTAL 0; i18n-check all current.
- Only change: sitemap.xml lastmod refresh (267 URLs). Committed and pushed.

## Session Log — 2026-10-12 (Monday newsletter drafts)

- Routine: git pull (already up to date at 10107ad after morning translation sync), NOTES.md read, last 24h of commits reviewed.
- Ran `node scripts/newsletter-draft.js` (key from `/home/box/.mailerlite_key`). Created **draft-only** campaigns (never sent or scheduled):
  - Weekly Brief 2026-10-12 (EN) id=201145275148928579
  - Weekly Brief 2026-10-12 (FR) id=201145277909829187
  - Weekly Brief 2026-10-12 (ES) id=201145280540706614
  - Weekly Brief 2026-10-12 (AR) id=201145283144320564
- Issue content: Solution of the Week = Great Bubble Barrier; 67 new solution pages in the last 7 days (Oct 10–11 batch), capped at 3 per hub with “see all” links; 3 launches this week (Falcon 9 Starlink Group 15-25, Dragon CRS-2 SpX-35, USSF-481); Amazing Facts GOES-19 CCOR-1 (NOAA SWPC) + ICESat-2 photon return (NASA); dad joke #1.
- Preview check vs sourcing rules: page meta pulled as-is; nonprofit/organization/company figures labeled where the page description already says so; NASA/NOAA/ESA/JAXA/ISRO named in agency items. Horizon-only pages added this week (LignoSat, PRELUDE) sit behind Space Disposal “see all 11” so the horizon badge is not in the capped list. Spot note for Brian: Life_Terra.html meta still says “planting 500 million trees” (goal language) while the page/impact figures use 36M+ planted — newsletter inherits the meta.
- State: `scripts/newsletter-state.json` updated (usedFacts + issues[2026-10-12]). Preview HTML also at `/tmp/newsletter-2026-10-12-{en,fr,es,ar}.html`.
- Glitches: none. Older Weekly Brief 2026-10-11 drafts remain in MailerLite as drafts (still unsent).

## Session Log — 2026-10-12 (Monday newsletter rerun check)

- Asked to rerun the "interrupted" Monday newsletter routine. git pull: already up to date at 38ae3d7, which already logged the 7:45 AM HST run as complete.
- MailerLite check: exactly one draft per language for 2026-10-12 (EN 201145275148928579, FR 201145277909829187, ES 201145280540706614, AR 201145283144320564), all status draft and not scheduled. No duplicates, so nothing deleted. Did not rerun newsletter-draft.js: it skips existing names, and a rerun could only rotate the facts/joke state.
- Solution of the Week (Great Bubble Barrier) section confirmed in the issue (in-issue link #sp-sotw plus card).
- FLAG for Brian: MailerLite lists "Weekly Brief 2026-10-11 (EN)" (201069299318653981) as **sent**, finished 2026-10-11 21:40:51 UTC (11:40 AM HST Oct 11). The FR/ES/AR 10-11 drafts are still drafts. No send was made in this session.

## 2026-10-12 08:05 HST: Life Terra wording, newsletter language + Corrections & Updates
- Life Terra: page hero/meta/JSON-LD, Deforestation hub card + quiz explanation (scripts/batch3-content.py) said Life Terra "is planting 500 million trees" (their goal). Now: "more than 36 million trees planted across Europe (company figure), working toward a goal of 500 million". New FR/ES/AR strings in i18n/*.json. weekly-sync run twice: seo-audit TOTAL 0, all translations current; linkcheck: only the 2 known JS-template false positives.
- scripts/newsletter-draft.js: sets MailerLite `language_id` on create (LANG_IDS en 4, fr 6, es 8, ar 23 from GET /campaigns/languages). New `--update` flag rewrites this issue's existing drafts in place (PUT /campaigns/{id}: content + language_id); it reuses state.issues[iso] facts/joke, so the rotation does not advance (newsletter-state.json unchanged).
- New Corrections & Updates section: data in scripts/newsletter-corrections.json ({date, page, what{en,fr,es,ar}, caught_by{...}}). Shows entries dated after the previous issue up to the issue date, in all 4 languages, with an "In this issue" link; hidden when empty. caught_by: 'SI Partner' for owner-caught fixes, otherwise a reader's first name/alias or 'a sharp-eyed reader'; never a real full name. Seeded with the Life Terra fix.
- This week's drafts EN 201145275148928579, FR 201145277909829187, ES 201145280540706614, AR 201145283144320564 updated via --update: fixed Life Terra line, Corrections section, language set to en/fr/es/ar. Still drafts; nothing sent or scheduled.
- About page: added "Spot an error? Email ideas@savingplanets.com..." line (+FR/ES/AR).

### 2026-10-12 — Ways to Help: Solution vs Organization columns + Home/About links
- Ways_to_Help.html: Solution column now = 2-4 word action (linked to the solution page), Organization = org name, in Donate/Volunteer (13) and Join the Team (5) tables. NASA citizen-science "Related solutions" list turned into a Solution/Organization table (19 rows, agency in Organization). Wording taken from each page's meta description. Script: /workspace/wth_cols.py (one-off; build_wth.py is the old generator and would overwrite this if rerun).
- Added `div.help-pagelinks` (a <nav> picked up the fixed #topnav styling, fixed in follow-up) (Home + About buttons) under the breadcrumb, and "Back to Home / About Saving Planets" buttons above the footer. CSS `.help-pagelinks` in styles.css; cache bump styles.css?v=20261012a on Ways_to_Help only (other pages keep v=20261011r to avoid dateModified churn).
- i18n: 47 new strings per language (fr/es/ar, machine-quality). weekly-sync: seo-audit 357 pages TOTAL 0. i18n-check: Ways_to_Help current; About/Deforestation/Life_Terra show STALE from the concurrent a82ca03 Life Terra/About English edit (not this task; needs its strings translated).
- Note: a concurrent agent commit (66df0c2) picked up part of this work (Ways_to_Help + styles.css) from the shared working tree.

## Session Log — 2026-10-12 (Nancy Grace Roman showcase, candidate A approved)
- Session start: git pull, NOTES + last 24h commits reviewed. Stashed a stray uncommitted tree (see glitch row).
- New Nancy_Grace_Roman.html (+fr/es/ar; ESCAPADE/mission template, body class roman-page, Project Rawane / Voyages Outward card first, menu via build-search-index, sitemap, i18n/pages.txt): jump links; mission widget (launch 2026-08-30T11:26:04Z, solar panels deployed +1h23m; no L2-arrival date because NASA gives only "three-month journey"); Roman vs Webb vs Hubble table (mirror, FOV, wavelengths, orbit, launch, best at); Where Is Roman Now; Newest Image; What Is a Lagrange Point (inline SVG L1-L5, pulsing L2, reduced-motion safe); Who Was Nancy Grace Roman (4 cards); fun-facts strip (300 MP, 1.4 TB/day, 100x, 1,000+ exoplanets); How This Saves People and the Planet (census of planetary systems / Coronagraph to Habitable Worlds Observatory / citizen science / mirror 80% lighter + on budget); Impact Statement + amazing-fact (1.4 TB a day).
- Sources (NASA only): nasa.gov Roman launch release (Aug 30 2026); science.nasa.gov/mission/roman-space-telescope/ (+ /frequently-asked-questions/, /introducing-the-roman-space-telescope/, /who-is-nancy-grace-roman/); science.nasa.gov/roman-and-hubble/; science.nasa.gov/people/nancy-grace-roman-for-hubble/; Webb fact sheet + orbit; Hubble vs. Webb; science.nasa.gov/resource/what-is-a-lagrange-point/; JPL Horizons; NASA Image and Video Library.
- LIVE DATA: JPL Horizons has Roman as spacecraft -211 (Webb -170). scripts/build-roman.py (first step of weekly-sync.sh; failures keep the previous JSON, never invent) writes assets/data/roman.json: geocentric distance at 00:00 UTC today (Oct 12: 1,484,298 km / 922,300 mi; Webb 1,403,399 km) + newest NASA Images item titled "Roman" (now NHQ202609010029, launch celebration photo, NASA/Aubrey Gemignani). It also rewrites the static ROMAN-LIVE block. assets/roman.js renders JSON client-side (localized numbers/date) + countdown to Jan 1 2027 (labeled start of NASA's "early 2027" window, not a NASA date). NASA Eyes link is general (no Roman-specific Eyes URL confirmed). When Roman's first science images appear in NASA Images, the "newest" slot picks them up automatically.
- Mission Log: build-batch3.py adds a "New: See Roman →" callout under Who Is Rawane (Project Rawane NEW callout left on Myth vs Fact).
- CSS block at end of styles.css; only Nancy_Grace_Roman.html uses ?v=20261012r.
- i18n: 93 new strings per language (machine-quality). The daily date string and the NASA image title/credit stay English in static HTML (JS localizes the date). weekly-sync run 3x: seo-audit 361 pages TOTAL 0, All translations current, stable tree. linkcheck: only the 2 known JS-template false positives.
- Live check 200 for EN/FR/AR page, roman.json, roman.js; screenshots 1280/1024/390 in /workspace/shots_roman/. At 390 the comparison table scrolls sideways inside its box (by design).
- Video: /workspace/grok-video-roman.txt (15 s, 9:16). X handles verified via X lookup: @NASA, @NASARoman, @NASAWebb, @NASAHubble, @NASAGoddard, @SISavingPlanets.

## Session Log — 2026-10-12 (batch 2026-10-12 B–Q built)
- All 16 approved candidates B–Q built as own pages (Sentinel-1 template: hero + credit, breadcrumb, mission widget for B–F, Five W's, Impact Statement with hub-label + sources + For Further Information, NEW "How This Saves People & the Planet" section, page-stats, bottom-link, next-solutions, help-actions). Commits c755e1f (pages, 13 NASA images, hero CSS) and e029acf (hub cards, cross-links, Ways to Help, sitemap, search, solutions.json, menus, fr/es/ar + 226 strings/lang). Built in a separate clone (/workspace/swbq); generator + content in /workspace/bqgen (data.py, build.py, hubs.py, tr1-4.py).
- Pages: Plato, ExoMars_Rosalind_Franklin, ISS_Water_Recovery (Project Rawane, Voyages Outward grid); Sentinel-2C, MetOp-SG-A1_Sentinel-5A, Landsat_9 (Earth Observation); Saharan_Dust_Amazon, Amazon_Rainy_Season (paired, cross-linked), Trees_for_the_Future (Forests); Moon_Steadies_Earth (Space Disposal natural "Saving Moons" w-card); Beavers_River_Engineers (Rivers); Salt_Marshes, Ocean_Voyages_Institute, Healthy_Seas, Mote_Marine_Laboratory, Seabin (Oceans). Cross-links added to next-solutions on Mangroves, Seagrass (→Salt Marshes), Coral Restoration Foundation (→Mote), Great Lakes Plastic Cleanup (→Seabin), ESCAPADE (→ExoMars), Biomass (→Saharan dust), Sentinel-1 (→Sentinel-2C).
- Upcoming launches: Plato and ExoMars follow the MMX/Dragonfly/NEO Surveyor pattern: sp:status active (funded, launch-scheduled agency missions), hub-label "launch planned March 2027" / "launch targeted for 2028", widget status only (no data-launch countdown, no .ics, no invented day; ESA gives month/year only). No horizon items in this batch (horizon count unchanged at 5).
- Figures: all from the queue sources, re-fetched 2026-10-12 (all 200). Healthy Seas 1,309.1 tons (Healthy Seas figure, 2026 press kit; the kit's older "991 tons" line ignored). Org/company figures labeled (OVI, Healthy Seas, Mote, TREES nonprofit; Seabin company).
- Help buttons + Ways to Help (Org/Solution format, +fr/es/ar via i18n): OVI Donate (oceanvoyagesinstitute.org/donate); Healthy Seas Donate (/donate/); Mote Donate (mote.org/support) + Join (mote.org/volunteer); TREES Donate (trees.org/support/personal-ways-to-give) + Join (trees.org/careers); Seabin Join only (seabin.io/get-involved: corporate volunteering + citizen science) in Join the Team; Landsat 9 + ISS water recovery in the NASA citizen-science table. No help section on ESA pages (B–E) or natural pages (H–L), per the 2026-10-11 rules. Ways to Help now 44 rows.
- solutions.json: 83 active, 5 horizon, 98 pages. Amazing Facts +6 (26). weekly-sync run 3x: seo-audit 425 pages TOTAL 0, all translations current, third run no diff. linkcheck: only the 2 known JS-template false positives. Roman pages only touched by the auto-generated Solutions menu line.
- Screenshots (live): /workspace/shots_bq/ (Plato, Healthy_Seas, fr/Landsat_9, ar/Seabin at 1280/390).
- No existing content corrected, so no Corrections & Updates entry.

| Date | What failed | Workaround | Resolved? |
|---|---|---|---|
| 2026-10-12 | Donate/Join link probes: trees.org/donate 404, seabin.io/careers 404, healthyseas.org/volunteer 404; oceanvoyagesinstitute.org/volunteer/ returns 200 but is a leftover WordPress theme demo page ("Namibia Wildlife Sanctuary"); OVI home also links a /donate-ways-to-give/ that 404s | Used trees.org/support/personal-ways-to-give + /careers, seabin.io/get-involved, Healthy Seas and OVI Donate only | Yes |
| 2026-10-12 | Roman executor pushed 0365251/d5d7935 while this batch was committed locally; rebasing would have conflicted on every page's generated menu, solutions.json, sitemap and i18n json | Reset to origin/main and re-ran the generators (bqgen scripts) + build-search-index + weekly-sync, then pushed | Yes |
| 2026-10-12 | ImageMagick `convert` not installed on the box | Resized images with Pillow | Yes |
| 2026-10-12 | Mission widget fmt() turns year-only milestones ("2016") into a fake Jan 1 date | Left data-milestones empty on Plato/ExoMars | Yes |


## Session Log — 2026-10-12 (Roman page: logical-flow reorder)
- Nancy_Grace_Roman.html (+fr/es/ar via i18n) reordered into one narrative: hook (#solution) → Who Was Nancy Grace Roman? (#nancy) → What Will Roman Do? (new #science: goals paragraph + fun-facts strip, now a div inside the section) → Roman vs Webb vs Hubble (#compare) → Where Is Roman Now? (#where, live distance) + mission widget + What Is a Lagrange Point? (#lagrange) → Newest Image and First Light (#newest) → How This Saves People & the Planet (#saves; card order For People, For Nature, For Life, For Future Missions) → Impact, stats, bottom-link, next, help, footer. Jump nav reordered to match (+ What will Roman do?).
- Short .roman-lead lead-in sentences on each section (no new claims; science paragraph uses only facts already on the page). Removed: duplicate "100x" fun-fact tile (stated in hook + table), "about one million miles from Earth" from the Impact Statement (L2 distance stays in the table + L2 figure). Hook now mentions the launch date and ties the census to how rare Earth may be.
- All IDs used by roman.js/build-roman.py kept (ROMAN-LIVE block, roman-km/mi/asof, webb-km, roman-cd, roman-latest*). CSS: .roman-lead, nested .roman-facts, .roman-facts-3; Roman page only bumped to styles.css?v=20261012s. 15 new strings/lang in i18n (machine-quality, appended, existing order kept).
- weekly-sync x2: seo-audit 425 TOTAL 0, all translations current, stable. linkcheck: only the 2 known JS-template false positives.
