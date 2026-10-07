# Save The Planet — Project Notes

**Repo:** chambersbryank-dot/Saveworld
**Live site:** https://www.saveplanetminusthedoom.com (GitHub Pages via CNAME)
**Last updated:** 2026-10-06

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

## Next Steps (when resuming)

1. Read this NOTES.md at session start.
2. Rename Ocean_Cleanup → Ocean_Cleanup.html.
3. Build missing sections: Actions, Amazing Facts, Community, Join.
4. Update nav links accordingly.
5. Remove or keep "Under Construction" text as appropriate.
