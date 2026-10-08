# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution against these before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on organizations that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

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

## Solutions Criteria (authoritative — check every new solution against these before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on organizations that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

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
  - **Terraformation:** CONFIRMED — 5.4M native trees planted in 2025 (up from 2.3M in 2024), 447 species, 2,155 hectares restored; 4.7M+ trees all-time, 68 projects in 18 countries. Donate path confirmed at terraformation.org.
  - **Life Terra:** CONFIRMED — 36M+ trees planted 2020-2025 across 32 countries, 563,000 tonnes CO2, 76% average survival rate on monitored plots. Donate path confirmed at lifeterra.eu/en/support-us.
- All ten still pass all four criteria. No removals needed.

## Session Log — 2026-10-08 (page number updates + Oceans hub link fix)

- Updated Great_Lakes_Plastic_Cleanup.html: When card now reads 277,000+ pieces (was 244,000).
- Updated Life_Terra.html: When card now reads 36 million trees and 563,000 tonnes CO2 (was 35M / 3.5M tonnes).
- Fixed Oceans.html hub: the 4ocean card link previously pointed to Oceans.html itself (self-refresh). Now points to Ocean_Cleanup.html — the dedicated page that exists in the repo. Note: there is no 4ocean.html file; 4ocean is covered on the Ocean Cleanup page.
- Verified all three updated files on main after push.

## Session Log — 2026-10-08 (page verification dates in footers)

- Added "Page verified October 2026" to the footers of seven solution pages: Plastic_Bank.html, Clean_Up_the_Lake.html, Sungai_Watch.html, Great_Bubble_Barrier.html, Astroscale.html, ClearSpace.html, Terraformation.html.
- Life_Terra.html and Great_Lakes_Plastic_Cleanup.html already carried the same footer text from the earlier number-update push, so all ten new solution pages now show a verification date.
- Also re-pushed Oceans.html in this batch to correct the 4ocean card link to Ocean_Cleanup.html (the previous push had pointed it at the nonexistent 4ocean.html).
- Going forward, when a solution's numbers are re-verified, update the footer date on that page and log it here.

### Still open
1. Rename assets/IMG_0060.jpeg to Saturn.jpg
8. Confirm ideas@savingplanets.com mailbox receives mail
13. Subpage navs still use the older bar — match them to this nav if the homepage look is approved
14. Review and finalize Solutions Criteria on About.html
15. Decide whether Astroscale and ClearSpace stay given partial donate paths
