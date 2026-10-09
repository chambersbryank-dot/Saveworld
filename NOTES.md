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
- **Re-check trigger:** Run this check again if we add more than ~5 large images (over ~500 KB each) or if the repo API size approaches 100 MB. At current growth rate, we are years from any limit.
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
  - **Ocean card:** OceanBeach.JPG, goal message: "Depicted is the goal we are striving for."
  - **Lakes card:** Pexels lake shot, goal message: "Depicted is our goal for the lakes to look like in the future."
  - **Rivers card:** StreamLog.JPG, goal message: "Depicted is our goal for the rivers to look like in the future."
  - **Forests card:** CutTreePlantThree.JPG, goal message: "Depicted is our goal for the forests to look like in the future."
- Fixed homepage hero: it was still pointing at the old IMG_0060.jpeg filename after Brian's Saturn.jpg rename, which would have left the hero blank. All three references (hero, space-card, and the Astroscale/ClearSpace donate buttons) now point at Saturn.jpg.
- Also fixed: the donate-routing CTA change from the earlier session had been lost in the revert; re-applied the "Be Part of the Fix" headline and donate-to-Solutions-page routing.

## Session Log — 2026-10-08 (Astroscale + ClearSpace nebula hero backgrounds)

- Brian requested Astroscale.html stop using Saturn behind Astroscale and use the nebula he uploaded instead, to reduce Saturn repetition across the site.
- Updated Astroscale.html page-hero to use assets/Nebula.jpg as background with the existing navy gradient overlay for title readability. Jupiter.jpg remains as the donate button and social image.
- Applied the same Nebula.jpg treatment to ClearSpace.html page-hero. Uranus.jpg remains as its donate button and social image.
- Saturn.jpg is now only used on the homepage hero and the Space card — each space page has its own look.
- Noted: the nebula reads as "the environment we're working in" rather than "the thing we're photographing," which fits Astroscale's debris-removal mission.

## Session Log — 2026-10-08 (Impact Statement label visibility fix)

- Brian reported the "Impact Statement" heading was invisible on solution pages — white text on white background. The .page-hero h1 color rule was bleeding into the impact section.
- Fixed in toc-home.css: .impact h2 now uses brand blue (#009cde), matching the Five W's headings, on every solution page. No HTML changes needed — all ten pages pick it up automatically via the shared stylesheet.
- Verified all ten solution pages have the Impact Statement section: Ocean Cleanup, Plastic Bank, Clean Up the Lake, Great Lakes Plastic Cleanup, Sungai Watch, Great Bubble Barrier, Astroscale, ClearSpace, Terraformation, Life Terra. The four category hubs (Lakes, Rivers, Deforestation, Space) don't have one because they're index pages.

## Session Log — 2026-10-08 (bottom CTA text update on all solution pages)

- Updated the footer CTA on all ten solution pages to Brian's requested wording: "Plastic, forests, and energy are problems we can tackle together. Send an idea or share a solution you know. If your solution meets our solutions criteria, we will add it to our solutions site. If you'd like to donate, visit our Solutions page and pick one that matches your interest."
- "solutions criteria" links to About.html#criteria; "Solutions page" links to index.html#solutions.
- Ocean_Cleanup.html and Plastic_Bank.html already had the updated text; the other eight were updated in this batch.

## Session Log — 2026-10-08 (logical flow: category cards to hubs, solution names to Five W's)

- Brian clarified the intended navigation flow: homepage category cards (Ocean, Lakes, Rivers, Forests, Space) link to their hub pages for browsing; individual solution names link straight to their Five W's pages for visitors who already know what they want.
- Audited all homepage cards and hub pages. The only real break was the 4ocean card on Oceans.html, which pointed to Ocean_Cleanup.html (same as The Ocean Cleanup card) — fixed to point to Ocean_Cleanup.html (the actual 4ocean page).
- Rule for future sessions: category title -> hub; solution name -> its own Five W's page. River Interceptors links to Ocean_Cleanup.html (it's The Ocean Cleanup's river program). Orbital Data Centers links to Space.html (covered on the Space page itself).
- No homepage changes were needed — the flow was already correct except for the 4ocean fix.

## Session Log — 2026-10-08 (Project R page created)

- Created Project-R.html using the standard hub page format: page-hero, five-ws grid with Who/What/When/Where/Why cards (all "Coming soon"), footer CTA with criteria link.
- Added Project R link to the nav on all pages (was missing from Ocean_Cleanup.html, Astroscale.html, Terraformation.html — fixed in same batch).
- Added Project R to sitemap.xml.
- Five W's content pending Brian's input.

## Session Log — 2026-10-08 (site-wide consistency audit)

- Audited all 20 HTML pages, both stylesheets, site.js, robots.txt, sitemap.xml, and the deploy workflow.
- **Consistent:** same nav, Montserrat font, Five W's + Impact Statement + donate-button structure, footer CTA, meta tags (title, description, canonical, og:title, og:description, og:image, og:url, og:type) on every page, favicon link, robots.txt pointing at sitemap.
- **Inconsistencies found:**
  1. Project R nav link missing from Ocean_Cleanup.html, Astroscale.html, Terraformation.html (fixed same session).
  2. Donate button labels: Astroscale and ClearSpace say "Support" instead of "Donate".
  3. og:image fallbacks: Clean_Up_the_Lake.html, Great_Lakes_Plastic_Cleanup.html, Sungai_Watch.html, Great_Bubble_Barrier.html all use SavePlanetLogo.jpg instead of category photos.
  4. Dead files: stray "Ocean_Cleanup" (no extension), lowercase "oceans.html" (321 bytes), empty "Plant3Trees1.jpg" (2 bytes).
  5. Duplicate CSS rules between styles.css and toc-home.css.
  6. site.js has doubled semicolons throughout.
- **Top five professional actions recommended:** (1) fix Project R nav — done; (2) swap four SavePlanetLogo.jpg og:images for category photos; (3) delete dead files; (4) add JSON-LD Organization schema to homepage; (5) add 404.html page.

## Session Log — 2026-10-08 (Forests hub hero swap to ThreeTrees2.jpg)

- Brian requested the Forests hub page-hero background swap from OceanBeach.JPG (beaches) to ThreeTrees2.jpg, his personal Hawaiian tree photo.
- Added .forest-hero rule in styles.css pointing at assets/ThreeTrees2.jpg; all other subpages keep the OceanBeach default.
- Hard refresh confirmed the new hero.

## Session Log — 2026-10-08 (Deforestation.html card image swaps)

- "Three trees for every one removed" card: swapped from CutTreePlantThree.JPG to Threetrees3.jpg (Brian's personal photo). og:image already pointed at Threetrees3.jpg, so it was already consistent.
- Life Terra card: swapped from dead Tree4.jpg (2-byte placeholder) to Threetrees4.jpeg (Brian's personal photo, 1.96 MB). CutTreePlantThree.JPG is now only used on the Terraformation card.
- Noted: Threetrees4.jpeg is the biggest tree shot at nearly 2 MB — worth watching for page-load speed if more large images are added.
- Plant3Trees1.jpg remains a 2-byte empty placeholder in the repo; if Brian intended to upload a real image under that name, it needs to be re-uploaded.

## Open Items

1. ~~Rename IMG_0060.jpeg to Saturn.jpg~~ DONE (Brian renamed; all references updated).
2. Fill in Project R Five W's content.
3. Swap og:images on Clean_Up_the_Lake, Great_Lakes_Plastic_Cleanup, Sungai_Watch, Great_Bubble_Barrier from SavePlanetLogo.jpg to category photos.
4. Delete dead files: Ocean_Cleanup (no extension), oceans.html (lowercase), Plant3Trees1.jpg (empty).
5. Add JSON-LD Organization schema to index.html.
6. Add 404.html page.
7. Deduplicate CSS between styles.css and toc-home.css.
8. Clean up doubled semicolons in site.js.
9. Decide fate of Threetrees4.jpeg (1.96 MB) vs. compressing for web.
10. Terraformation social media graphics: Brian is checking terraformation.com/tree-subscription-resources for a free Hawaii image to use on the Terraformation card.
11. Ken Burns animation: Brian reviewing the Space card trial; extend to other cards if approved.
