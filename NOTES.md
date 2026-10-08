# Save The Planet — Project Notes

**Repo:** chambersbryank-dot/Saveworld
**Live site:** https://www.saveplanetminusthedoom.com (GitHub Pages via CNAME)
**Last updated:** 2026-10-08

---

## 📌 STANDING RULE (read this first, every session)

1. **At session start:** Read this NOTES.md file before doing anything else. Use the Session Log to see exactly what was done last (HTML changes, CSS changes, open items, decisions) so you can pick up right where things left off.
2. **During the session:** Execute whatever the user asks next, informed by that history.
3. **After every change:** Go back into NOTES.md and log what you did — specifically what changed in the HTML and what changed in the CSS — plus any new decisions or open items. Keep it concise: what you did, not a rewrite of prior entries.
4. This rule applies to every future session without being re-asked.
5. **NEW (2026-10-07):** This notes file is the shared working agreement between the user and Grok. Both parties use it to communicate, track decisions, and keep the buildout synchronous. Update it whenever the plan, priorities, or structure change.
6. **NEW (2026-10-07):** Save-every-sixty-seconds rule. If any HTML, CSS, or NOTES.md work runs longer than one minute, pause and commit what you have so far before continuing. This prevents losing progress if the connection drops mid-session.

---

## Template Rule

- **Oceans.html is the template page for all future solution pages.** Reuse its structure and styling (page hero, five W's grid, impact statement section, cleanup link card, nav, footer) when creating new solution pages. Do not reinvent the wheel.
- **Ocean_Cleanup.html is the Ocean Cleanup splash page** (five W's, impact statement, donate link). It is the destination for the Oceans card on the homepage and the Oceans dropdown item.
- **Space.html is the Space solution page** (five W's, impact statement, go-deeper link card). It is the destination for the Space card on the homepage and the Space dropdown item.
- **Amazing_Facts.html is the Amazing Facts page** (page hero, facts grid, impact statement, link card). It is the destination for the Amazing Facts card on the homepage and the Amazing Facts nav link.

---

## Design System (locked)

- **Palette:** Primary blue #0066cc, accent teal #00b894, dark navy #003366 (footer/impact), page background #f0f7ff, card white. Space accent: #1a1a2e.
- **Fonts:** 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif. Body line-height 1.7, color #222.
- **Cards:** Border-radius 18px, box-shadow 0 10px 35px rgba(0,0,0,0.08), hover translateY(-8px). Image containers: radius 12px, image height 245px, object-fit cover, hover scale 1.12.
- **Buttons:** Primary fill, white text, padding 13px 30px, border-radius 50px, font-weight 600.
- **Spacing:** Max content width 1250px, section padding 1.5rem sides, generous vertical rhythm (h2 margin 5rem 0 3rem).
- **Nav:** Sticky, translucent white background, z-index 1000, 85px height. Dropdown: absolute, white, radius 10px, shadow, z-index 1001; open on hover or click toggle.
- **Mobile:** Breakpoint 768px. Reduce h1 to 2.4rem, nav gap to 1.2rem, page-hero to 40vh. Keep grids auto-fit so cards stack.
- **iPhone readiness:** Viewport meta tag on every page (width=device-width, initial-scale=1.0). Test key flows on iPhone Safari before calling a page done.

---

## File Map

- **index.html** — Homepage (splash): sticky nav with Solutions dropdown (Oceans, Space), hero, solutions grid (Oceans, Space, Amazing Facts, The Ocean Cleanup, Reforestation), Amazing Facts card (id facts-card) linking to Amazing_Facts.html. Footer, dropdown script.
- **Ocean_Cleanup.html** — Ocean Cleanup splash page: page hero, five W's grid, impact statement, donate card linking to theoceancleanup.com/donate. Nav, footer, dropdown script.
- **Space.html** — Space splash page: page hero (space-hero variant), five W's grid, impact statement, go-deeper link card (Starcloud, Google Project Suncatcher). Nav, footer, dropdown script. Created 2026-10-07.
- **Amazing_Facts.html** — Amazing Facts page: page hero, five fact cards (Petabytes in Orbit first), impact statement, link card. Nav, footer, dropdown script. Created 2026-10-08.
- **Oceans.html** — Older Oceans template page (five W's + impact + link to Ocean_Cleanup.html). Kept as alternate template; may be consolidated later.
- **styles.css** — Shared design system: nav, dropdown, hero, page-hero, space-hero variant, grids, cards, impact, cleanup-link, footer, mobile breakpoint, under-construction animation.
- **assets/** — SavePlanetLogo.jpg, OceanBeach.JPG, theoceancleanup.jpg, LightthrForest.JPG, CutTreePlantThree.JPG, BargCleaning.JPG, StreamLog.JPG, streamlog2.JPG, Saturn.jpg (pending user upload — Cassini public domain photo opened from Wikimedia Commons 2026-10-08).
- **.github/workflows/static.yml** — GitHub Pages deploy on push to main.
- **CNAME** — www.saveplanetminusthedoom.com.
- **NOTES.md** — This file: standing rules, template rule, design system, file map, open items, content queue, session log.

---

## Open Items (prioritized)

1. Build missing homepage sections: Actions, Community, Join. Nav links currently point to sections that don't exist. (Amazing Facts section ✓ done 2026-10-08)
2. Remove or keep "Under Construction" text as appropriate once sections are built.
3. ~~Draft the space section/page using research logged 2026-10-06.~~ DONE 2026-10-07.
4. iPhone/Safari pass: verify nav dropdown, cards, heroes, and links render correctly on iPhone.
5. Cloudflare DNS/custom domain managed separately — not accessible from this session.
6. Decide whether to consolidate Oceans.html into Ocean_Cleanup.html or keep both.
7. Implement Solutions dropdown items for future solution pages as they are created. (Oceans ✓, Space ✓)
8. ~~Source a dedicated space-themed image for the Space card.~~ IN PROGRESS 2026-10-08 — Cassini Saturn photo selected (public domain, Wikimedia Commons); user downloading and will upload as assets/Saturn.jpg when home. index.html already references it.
9. Upload Saturn.jpg to assets/ folder (user action pending).
10. **NEW (2026-10-08):** SEO meta tagging standard — apply to every page as built. Research sourced 2026-10-08:
    - **Title tags:** 50–60 characters, front-load keyword, unique per page, brand suffix short. Google truncates ~600px.
    - **Meta descriptions:** 150–160 characters, keyword early, end with call-to-action ("learn more", "read now"). Not a ranking factor but drives click-through.
    - **Open Graph:** og:title, og:description, og:image (1200×630, ≤8MB, 1.91:1), og:url, og:type=website. Controls Facebook, LinkedIn, Slack, Discord, iMessage cards.
    - **Twitter Card:** twitter:card (use summary_large_image, not default small summary).
    - **Canonical:** link rel=canonical with absolute URL per page to de-dupe.
    - **Meta robots:** index,follow (default) — set explicitly.
    - **Structured data:** JSON-LD (Google's recommended format over Microdata/RDFa). Use Organization, WebPage, BreadcrumbList types. FAQPage markup no longer earns rich results (removed May 2026) — skip. Headline in schema must match visible H1. Absolute HTTPS URLs for image/url/logo. No trailing commas in JSON.
    - **Keywords meta:** legacy noise per 2026 research — not required.
    - Apply incrementally as each page is built rather than retrofitting all at once.
11. **NEW (2026-10-08):** Copyright/legal due diligence scan — recurring task, weekly cadence (user's choice; default weekly). Scan all HTML and CSS for proprietary content, unlicensed images, trademarks (e.g., SpaceX/Starship branding), and third-party assets. Not legal advice — just due diligence flagging. Log findings in session log.

---

## Content Queue (drafted, awaiting user review)

- Five W's + impact statement for Ocean_Cleanup.html (sourced from theoceancleanup.com, 2026-10-07). Published.
- Donate link: https://theoceancleanup.com/donate (sourced from theoceancleanup.com, 2026-10-07). Published.
- Space section research: data center water use figures and space-based data center developments (sourced 2026-10-06, refreshed 2026-10-07). Published in Space.html.
- Space.html five W's, impact statement, and go-deeper links (Starcloud, Google Project Suncatcher) drafted 2026-10-07.
- Amazing_Facts.html five facts drafted 2026-10-08: Petabytes in Orbit (links to Space.html), Twelve Times the Water, Fifteen Million Kilograms, One Thousand Rivers, Three Trees for One.

---

## Session Log — 2026-10-07 (Ocean Cleanup splash page)

- Created Ocean_Cleanup.html: Ocean Cleanup splash page using Oceans.html template. Page hero, five W's grid, impact statement, donate card linking to theoceancleanup.com/donate. Dropdown Oceans item points to index.html#oceans-card.
- Updated index.html: Oceans card renamed from "Clean Beaches & Oceans" to "Oceans" with id oceans-card; dropdown Oceans link now scrolls to #oceans-card; Ocean Cleanup card links to Ocean_Cleanup.html.
- Updated styles.css: no changes this round (resaved to confirm).
- Updated NOTES.md: template rule extended, file map and open items refreshed, session log added.

## Session Log — 2026-10-07 (Space splash page)

- Created Space.html: Space splash page using Oceans.html template. Page hero (Computing Above the Clouds), five W's grid (Who: Starcloud, Google Project Suncatcher, Cowboy Space; What: orbital AI compute; When: launch timeline; Where: LEO + lunar orbit; Why: water savings), impact statement with water-use figures (17.4B direct / 211B indirect gallons), go-deeper link card to starcloud.com and Google's Project Suncatcher blog.
- Updated index.html: added Space dropdown item under Solutions; added Space card (id space-card) linking to Space.html; updated meta description and keywords.
- Updated styles.css: no changes this round.
- Updated NOTES.md: added save-every-sixty-seconds rule (rule 6), extended template rule for Space.html, refreshed file map and open items, added session log.
- Research refreshed via web search 2026-10-07: LBNL direct/indirect water figures, Google 10.9B gallons 2025, Amazon 2.5B gallons 2025, Starcloud roadmap, Google Suncatcher launch Oct 1 2026, Firefly lunar contract Sep 30 2026.

## Session Log — 2026-10-08 (Amazing Facts page + Space card image)

- Created Amazing_Facts.html: Amazing Facts page using Oceans.html template. Page hero, five fact cards (Petabytes in Orbit first, linking to Space.html), impact statement, link card to Space.html and Ocean_Cleanup.html. Nav, footer, dropdown script.
- Updated index.html: added Amazing Facts card (id facts-card) in solutions grid linking to Amazing_Facts.html; nav Amazing Facts link points to #facts.
- Updated styles.css: added --space accent variable and .page-hero.space-hero variant (dark navy radial gradients) for Space.html.
- Updated NOTES.md: extended template rule for Amazing_Facts.html, refreshed file map and open items, added session log.
- Space card image: selected Cassini Saturn photo (public domain via Wikimedia Commons); direct image download blocked by 401/403/503 errors from Unsplash, Pexels, and Wikimedia CDNs. Opened Wikimedia Commons file page on car browser for user to download manually. index.html updated to reference assets/Saturn.jpg pending upload.

## Session Log — 2026-10-08 (SEO + copyright diligence standards)

- Researched 2026 SEO meta tag best practices via web search: title/description lengths, Open Graph, Twitter Card, canonical, meta robots, JSON-LD structured data (Organization, WebPage, BreadcrumbList), FAQPage rich results removed May 2026.
- Added open item 10: SEO meta tagging standard to apply incrementally as pages are built.
- Added open item 11: weekly copyright/legal due diligence scan of HTML and CSS.
- Completed items 3 and 7 removed from open list per user request.
- No HTML/CSS changes this round — standards logged for future application.
