# Save The Planet — Project Notes

**Repo:** chambersbryank-dot/Saveworld
**Live site:** https://www.saveplanetminusthedoom.com (GitHub Pages via CNAME)
**Last updated:** 2026-10-06

---

## ⚠️ PRIVACY / PROPRIETY REMINDER

> **When the project starts getting serious — real content, real photos, real branding, or anything proprietary — flag it to the user and recommend locking the repo down (make it private) before going further.** This is a standing instruction from the user: don't wait to be asked. If proprietary material, personal info, or anything sensitive enters the repo or site, tell the user it's a good time to get locked down.

---

## User's Vision & Philosophy (the "why")

> **The site URL says it all: an honest approach to saving the world without the doom.**

- Taking care of the planet is absolutely important — but it starts with **streams, rivers, lakes, oceans, our seas, the forests**, and everything in between.
- At the same time, you cannot negate **population growth, energy, infrastructure, and people working** — those are real and necessary.
- There has to be a **meet in the middle** where we can literally save the world.
- Saving the world has to be **both**: you can't save the world by killing people, and you can't kill people and call it saving the world.
- The tone must stay **positive and practical** — hope and action, never doom or guilt.

This is the user's core worldview and should inform all content, tone, and messaging decisions going forward.

---

## Current State

- **index.html** — live homepage: sticky nav (logo, Solutions / Actions / Facts / Community links, Join Movement button), hero section with ocean photo background, three solution cards (Clean Beaches & Oceans, The Ocean Cleanup, Reforestation), footer. Meta description and keywords present.
- **styles.css** — design system: CSS custom properties (--primary #0066cc, --accent #00b894), sticky translucent nav, full-viewport hero with gradient overlay, card hover lift + image zoom, pulsing "Under Construction" animation, mobile breakpoint at 768px.
- **Ocean_Cleanup** — second page (no .html extension — needs renaming to Ocean_Cleanup.html), same nav/styling, industries grid (Technology & Engineering, Corporate & Philanthropy, Community & NGOs, Government & Policy).
- **assets/** — SavePlanetLogo.jpg, OceanBeach.JPG, theoceancleanup.jpg, LightthrForest.JPG, CutTreePlantThree.JPG, BargCleaning.JPG, StreamLog.JPG, streamlog2.JPG.
- **.github/workflows/static.yml** — standard Pages deploy on push to main.
- **CNAME** — www.saveplanetminusthedoom.com.

## Known Issues / Open Items

1. Nav links #actions, #facts, #community, #join point to sections that don't exist yet in index.html.
2. "See Real Solutions" button links to #solutions (works), but earlier mention of a solutions page 404 — verify.
3. Ocean_Cleanup file has no extension; rename to .html and add to nav.
4. Site still shows "Under Construction" — intentional until sections are built.
5. Cloudflare not accessible from this session — DNS/custom domain managed separately.

## Decisions Made

- Positive, hopeful tone (no doom). Three pillars: clean oceans/lakes/rivers, plant three trees per one cut, remove plastic from beaches and highways.
- Design: blue/teal palette, card-based layout, photo-driven.
- Deployment: GitHub Pages (not Cloudflare Pages) with custom domain.

## Session Log

### 2026-10-06
- User asked if site is latest/greatest; confirmed Grok 4.7 context.
- Located repo via GitHub (Saveworld), reviewed index.html, styles.css, Ocean_Cleanup, CNAME, workflow.
- Discussed NOTES.md as persistent memory between sessions; created this file.
- User plans to resume work in 2–3 weeks depending on work/home schedule.
- Next session: read this file first, then pick up open items.
- User requested a standing reminder in NOTES.md: when proprietary or sensitive material enters the project, flag the user and recommend locking the repo down (making it private).
- User shared his core vision: honest approach to saving the world without the doom; planet care starts with water (streams, rivers, lakes, oceans) and forests, but population growth, energy, and infrastructure can't be negated; the answer is a meet-in-the-middle where saving the world means both — not saving the world by killing people, and not killing people to save the world.

## Next Steps (when resuming)

1. Read this NOTES.md at session start.
2. Rename Ocean_Cleanup → Ocean_Cleanup.html.
3. Build missing sections: Actions, Amazing Facts, Community, Join.
4. Update nav links accordingly.
5. Remove or keep "Under Construction" text as appropriate.
