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
- **No guilt, no politics.** The message is: get educated, understand how we can make a difference, and make the change — so we can have crystal clear water. Don't make Democrats or Republicans feel guilty. Just stop, make the change.

### Technology & AI as the bridge

- If we have the technology to build colossal ships, oil rigs, and petroleum/lubrication infrastructure, we have the intellect to do the opposite: increase forestation (redwoods, pines), beautify landscapes, and deploy barges across the Pacific, Atlantic, and beyond — including the Antarctic — to remove plastic and crud from the seas.
- **AI can help bridge this gap** — the same engineering capability that built the industrial world can be redirected toward restoration.
- This is a core belief of the user's and should inform messaging: the tools already exist; the will and coordination are what's missing.

### Space as the next frontier (incorporate sooner than later)

- **Space can help save Earth.** The idea: move AI's massive data centers — the petabyte farms currently scattered across the world — up into space. This frees up land and resources down here.
- Example framing: instead of destroying 50 acres on Earth to build a data center, build that petabyte of capacity in space. That's another educational angle for the site.
- Benefits to highlight: saves energy, lowers the water bill (data centers are huge water consumers for cooling), and reduces land use.
- This is a strong example of the user's core philosophy — using advanced technology (space infrastructure) to make a positive change on Earth, without guilt or anti-progress messaging. It fits the "meet in the middle" vision perfectly.
- **Action item:** incorporate this into the site sooner than later — could become its own section or page (e.g., "Space & Earth" or under Solutions/Facts).

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
6. **NEW:** Space-based AI infrastructure content not yet incorporated — user wants this sooner than later.

## Decisions Made

- Positive, hopeful tone (no doom, no guilt, no politics). Three pillars: clean oceans/lakes/rivers, plant three trees per one cut, remove plastic from beaches and highways.
- Design: blue/teal palette, card-based layout, photo-driven.
- Deployment: GitHub Pages (not Cloudflare Pages) with custom domain.
- Mission check: every page's narrative must stay on track with the vision — educate, don't guilt.

## Session Log

### 2026-10-06
- User asked if site is latest/greatest; confirmed Grok 4.7 context.
- Located repo via GitHub (Saveworld), reviewed index.html, styles.css, Ocean_Cleanup, CNAME, workflow.
- Discussed NOTES.md as persistent memory between sessions; created this file.
- User plans to resume work in 2–3 weeks depending on work/home schedule.
- Next session: read this file first, then pick up open items.
- User requested a standing reminder in NOTES.md: when proprietary or sensitive material enters the project, flag the user and recommend locking the repo down (making it private).
- User shared his core vision: honest approach to saving the world without the doom; planet care starts with water (streams, rivers, lakes, oceans) and forests, but population growth, energy, and infrastructure can't be negated; the answer is a meet-in-the-middle where saving the world means both — not saving the world by killing people, and not killing people to save the world.
- User added technology philosophy: if we can build colossal ships and oil rigs, we have the intellect to scale forestation, beautification, and ocean cleanup barges worldwide including Antarctica; AI can help bridge this.
- User added tone rule: no guilt, no politics — educate people on how they can make a difference; the goal is crystal clear water. Every page's narrative must stay on mission.
- User added space topic: moving AI petabyte data centers into space to save land, energy, and water on Earth (e.g., avoid destroying 50 acres for a data center by building capacity in orbit). Wants this incorporated sooner than later — could be its own section or page. Fits the "technology as bridge" philosophy.

## Next Steps (when resuming)

1. Read this NOTES.md at session start.
2. Rename Ocean_Cleanup → Ocean_Cleanup.html.
3. Build missing sections: Actions, Amazing Facts, Community, Join.
4. Update nav links accordingly.
5. Remove or keep "Under Construction" text as appropriate.
6. **Incorporate space-based AI infrastructure content** (data centers in orbit, land/energy/water savings) — sooner than later, per user.
