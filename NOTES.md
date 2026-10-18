# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

> Working file for Chief of Staff + Grok only. Keep lean: last 24h, next/open, reference. Long detail goes in docs/ and gets a one-line link.
> Archives: full history to Oct 12 midday → docs/notes-archive-2026-10-12.md (restored; 8987d81 had wiped NOTES to 28 bytes). Search/IA/hero detail + test tables → docs/search-and-ia-notes.md. Discovery research → docs/organic-discovery-plan.md.

## Last 24h (Oct 16–17 HST)
- **Learn tracks**: Phase 1 Orbital Mechanics (Orbits_Guide, Orbit_Math, Orbit_Lab + KaTeX, practice, Orbit Lab), Phase 2 Aeronautical Engineering, Phase 3 Physics. Math woven in, not standalone. Generator build-learn.py; weekly-sync updated.
- **SI Helper pilot**: Cloudflare Worker (Turnstile, grounded answers, refusals, citation normalize), Teachers widget + SI_Helper.html + Privacy, unanswered-question KV log + Student_Questions pool (weekly routine), iPad tests. Needs COPPA/legal before student promotion.
- **Header nav v2**: build-nav.py, utility + main rows, dropdowns, mobile, 5 langs, SPNAV markers, cache 20261016N. Alphabetical subs later.
- **Analytics**: GA4 fully removed → Cloudflare Web Analytics beacon (no cookies). Aggregate event counts Worker. Report-a-correction form + SI cap alert email. Consent banner gone.
- **Licensing & growth**: CC BY-NC 4.0. Classroom share + Weekly Brief growth (COPPA-safe).
- **Calculators / start-here / careers / standards tags / embeds**. Search.html cleanup. R2 media hosting for videos. Hero themes (space Enceladus→Earthrise loop, captions, hi-res, composition). First-screen wow rule.
- **SEO**: metadata 5 langs, seo-fix/seo-lint/seo-jsonld pipeline, IndexNow ping in post-deploy, hand titles in i18n/seo-meta.json.
- **Agency solutions batch** (20 pages + merges). Translations (no English section names). Great Bubble Barrier total. AGENCY_1016 emails sent.
- **World Map**: map-first layout (centered, one-line h1, collapsed details, filters on map).
- **12 approved solutions batch** (ABDGHN + C E F I J K; L/M rejected). Count ~163.
- **Hebrew**: Phase 1-2 + completeness batches (non-solution, World_Map, calculators, etc.), noindex normalized in generators (HE_PUBLIC=False), 241 pages hidden.
- **Kids Phase 1**: Space_Passport (stamps, localStorage), Myth_or_Fact_Arcade (47 claims), Boarding_Pass (real launches), Superpowers panel (read-aloud etc.). Play & Learn audit fixes. STYLEV 20261017h.
- **Other**: About video duplicate fix, homepage hero title centered, Earthrise caption note, hero position locked, biosipartner@ Cc, SI terminology sweep, generator fixes for i18n hashes.

## Next / Open
**Next priorities**
- (a) Interactive data visualizations (PhET / Fluid Earth style) on Amazing Facts or EO hub.
- (b) Adaptive learning paths by age (kids/teens/adults).
- (c) Eco-anxiety support after heavy topics.
- (d) Choose-your-own-adventure action guide (Ways_to_Help roles).
- SI Helper: COPPA/legal review, native-speaker AR/IT check, custom domain decision, Cloudflare billing alert. Promote only after.
- Learn open: ELI10 boxes, Kepler/Hohmann widgets on Orbit_Math, per-lang glossary, SI diagrams.
- Hebrew: decision on public (currently noindex).
- First-screen wow on remaining top pages; remaining people+nature sections.

**User to-dos**
- [ ] YouTube Studio: set "Altered or synthetic content" = Yes on ad v2 + older SI videos.
- [ ] Pin comment "Every fact and source at savingplanets.com 🌍" on YouTube + TikTok.
- [ ] Awards: CSS Design Awards ($50), Awwwards ($65), Indie Hackers (free); kit /workspace/awards_kit.md.
- [ ] Optional: swap .github/workflows/static.yml for docs/static-with-search.yml.txt (token lacks workflow scope).
- [ ] Partner With Us: supply real, verified audience stats.
- [ ] Google Search Console (Cloudflare DNS TXT) + submit sitemap; Bing Webmaster (import from GSC); Cloudflare Crawler Hints; Brave; then OER Commons, Curlie (EN/FR/ES/AR), TES/Procomún. Rich Results Test.
- [ ] Grok Plus 9:16 still yields wide video; optional Artemis remake; 4 ad clips from /workspace/grok-ad-savingplanets.txt.
- [ ] MailerLite double-opt-in confirmation texts (scripts/newsletter-confirmation-texts.md).
- [ ] Human-SI collab awards (draft /workspace/awards/human-si-collaboration-writeup.md): Fast Company (early Nov 13 / final Dec 11 2026), Telly, A' Design, Internationalist, Anthem, NI Prize 2027.
- [ ] One-time: GSC Domain property TXT, Bing import, etc. (see Oct 16 SEO section).
- [ ] SI Helper: COPPA/legal, native checks, domain, billing alert.

**Open decisions**
- Merge Related Solutions with "Next: Explore Another Solution".
- Homepage "minus the doom" in strip + headline — shorten one.
- Rewrite ELI10 truly simple for top pages.
- Hub/solution pages missing "How This Saves People & the Planet" — add when touched.
- Real photos for 3 lake cleanup cards.
- Multilingual semantic model for fr/es/ar/it meaning search.
- IndexNow already wired in post-deploy; confirm live.
- Hebrew public vs keep noindex.
- Custom domain for SI Helper.

**Follow-ups**
- Newsletter "What's New" (Monday, live features only).
- Daily 6:17 AM HST candidate run → owner yes/no.
- Glossary terms as pages grow.
- Weekly unanswered-question answers routine (Wednesdays).
- Stash `stash@{0}` (pre-Roman, Oct 12) still unreviewed.

## Reference
