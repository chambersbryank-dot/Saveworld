# Save The Planet — Project Notes

**Repo:** chambersbryank-dot/Saveworld
**Live site:** https://www.saveplanetminusthedoom.com (GitHub Pages via CNAME)
**Last updated:** 2026-10-07

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

---

## Design System (locked)

- **Palette:** Primary blue #0066cc, accent teal #00b894, dark navy #003366 (footer/impact), page background #f0f7ff, card white.
- **Fonts:** 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif. Body line-height 1.7, color #222.
- **Cards:** Border-radius 18px, box-shadow 0 10px 35px rgba(0,0,0,0.08), hover translateY(-8px). Image containers: radius 12px, image height 245px, object-fit cover, hover scale 1.12.
- **Buttons:** Primary fill, white text, padding 13px 30px, border-radius 50px, font-weight 600.
- **Spacing:** Max content width 1250px, section padding 1.5rem sides, generous vertical rhythm (h2 margin 5rem 0 3rem).
- **Nav:** Sticky, translucent white background, z-index 1000, 85px height. Dropdown: absolute, white, radius 10px, shadow, z-index 1001; open on hover or click toggle.
- **Mobile:** Breakpoint 768px. Reduce h1 to 2.4rem, nav gap to 1.2rem, page-hero to 40vh. Keep grids auto-fit so cards stack.
- **iPhone readiness:** Viewport meta tag on every page (width=device-width, initial-scale=1.0). Test key flows on iPhone Safari before calling a page done.

---

## File Map

- **index.html** — Homepage (splash): sticky nav with Solutions dropdown (Oceans, Space), hero, solutions grid. Oceans card (id oceans-card) links to Ocean_Cleanup.html; Space card (id space-card) links to Space.html. Reforestation card, The Ocean Cleanup card. Footer, dropdown script.
- **Ocean_Cleanup.html** — Ocean Cleanup splash page: page hero, five W's grid, impact statement, donate card linking to theoceancleanup.com/donate. Nav, footer, dropdown script.
- **Space.html** — Space splash page: page hero, five W's grid, impact statement, go-deeper link card (Starcloud, Google Project Suncatcher). Nav, footer, dropdown script. Created 2026-10-07.
- **Oceans.html** — Older Oceans template page (five W's + impact + link to Ocean_Cleanup.html). Kept as alternate template; may be consolidated later.
- **styles.css** — Shared design system: nav, dropdown, hero, page-hero, grids, cards, impact, cleanup-link, footer, mobile breakpoint, under-construction animation. No CSS changes this round.
- **assets/** — SavePlanetLogo.jpg, OceanBeach.JPG, theoceancleanup.jpg, LightthrForest.JPG, CutTreePlantThree.JPG, BargCleaning.JPG, StreamLog.JPG, streamlog2.JPG.
- **.github/workflows/static.yml** — GitHub Pages deploy on push to main.
- **CNAME** — www.saveplanetminusthedoom.com.
- **NOTES.md** — This file: standing rules, template rule, design system, file map, open items, content queue, session log.

---

## Open Items (prioritized)

1. Build missing homepage sections: Actions, Amazing Facts, Community, Join. Nav links currently point to sections that don't exist.
2. Remove or keep "Under Construction" text as appropriate once sections are built.
3. ~~Draft the space section/page using research logged 2026-10-06.~~ DONE 2026-10-07.
4. iPhone/Safari pass: verify nav dropdown, cards, heroes, and links render correctly on iPhone.
5. Cloudflare DNS/custom domain managed separately — not accessible from this session.
6. Decide whether to consolidate Oceans.html into Ocean_Cleanup.html or keep both.
7. Implement Solutions dropdown items for future solution pages as they are created. (Oceans ✓, Space ✓)
8. Source a dedicated space-themed image for the Space card (currently reusing LightthrForest.JPG).

---

## Content Queue (drafted, awaiting user review)

- Five W's + impact statement for Ocean_Cleanup.html (sourced from theoceancleanup.com, 2026-10-07). Published.
- Donate link: https://theoceancleanup.com/donate (sourced 2026-10-07).
- Space section research: data center water use figures and space-based data center developments (sourced 2026-10-06, refreshed 2026-10-07). Published in Space.html.
- Space.html five W's, impact statement, and go-deeper links (Starcloud, Google Project Suncatcher) drafted 2026-10-07.

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
