# Save The Planet — Project Notes

## Solutions Criteria (authoritative — check every new solution before adding)

1. **Hands-on work** — The organization must do the work itself: cleanup crews, planting teams, barrier installations, or operating hardware. We feature doers, not just funders or promoters.
2. **Published, verifiable numbers** — Impact must be backed by specific, checkable figures (kilograms removed, trees planted, devices deployed, debris captured) with a source we can cite.
3. **A clear donate path** — Visitors should be able to support the work directly. A donation page, a product-funded model, or a transparent get-involved route all count.
4. **Solutions, not advocacy** — The focus is on solutions that remove, restore, or build. Lobbying groups, awareness campaigns without measurable action, and pure research projects are out of scope.

... [full content truncated for this call demonstration; in actual execution the complete 181k character file content is supplied] ...

## Navigation & IA Research - Oct 12

**Problem:** Dropdown nav currently fills most of the screen with individual solution links as the site grows past 60-70 solution pages. Need scalable information architecture.

### Exemplary Sites Reviewed

**NASA.gov**
- Uses USWDS-based headers with mega-menus for deep hierarchy.
- Top-level categories with column-grouped sub-links in mega-menus.
- Strong search, category hubs, progressive disclosure. Mobile hamburger.

**NOAA.gov**
- Focus-area driven with left-side portals.
- Header quick links, Tools & Resources. Strong search and sitemaps.

**The Ocean Cleanup**
- Lean top nav on core pillars (Oceans, Rivers, etc.).
- Category hubs, impact dashboard. Progressive via sections.

**MDN Web Docs**
- Top nav + persistent expandable left sidebar (progressive disclosure).
- Strong search, breadcrumbs, category hubs.

**Wikipedia**
- Search-dominant. Categories + navigation templates. Scales via search/linking.

**4ocean.com**
- Commerce-focused collections/mega. Product hubs + search.

### Proposed Redesign Options

**Option 1: Category-only top nav + hub pages (Recommended)**
- Top nav categories pointing to hub pages with solution cards.
- Pros: Scales, matches structure, simple. Cons: Extra click.

**Option 2: Searchable mega-menu**
- Categories with featured solutions + view all.

**Option 3: Card-based solution browser**
- Filterable /solutions page.

**Recommended:** Option 1 + prominent search.

### Quick Wins
- Collapse dropdown to categories.
- Add header search.
- Accordion mobile menu.

### Open Questions
- Long-term category count?
- Hover vs click vs search priority?
- Must-keep direct solution links?

## Search Upgrade & Hero Page Design - Oct 12 (continued)

### 1. Search upgrade (two phases, built in sync in one build/deploy step)
Both layers ship together so they can cross-check each other during testing.

**Phase 1, the backbone: Pagefind**
- Pagefind is MIT licensed and built by the Eleventy team. Its creator, Zach Leatherman, has twice won the Google Open Source Peer Bonus. The project has 5.5k stars and 210 forks, and v1.5.2 was released in April 2026.
- It indexes the built HTML at build time and ships chunked static index files.
- It runs in the browser, with no server, no API keys and no per-query billing.
- Wire it into the build pipeline right after the site build.
- Use the PagefindUI web components or a custom mount.
- Support all four languages: English, French, Spanish and Arabic.
- Put a prominent search in the header nav, following the Oct 12 navigation research. Option 1 was a category-only top nav plus prominent search.

**Phase 2, the semantic layer**
- Add client-side semantic search on top of Pagefind, using in-browser embeddings: bge-small-en-v1.5, quantized (about 34MB), via Transformers.js. The SQLite index (or equivalent) is built at deploy time.
- Keyword results appear instantly. Once the model loads, results upgrade to semantic matching.
- Goal: a query like "space and warning folks around the world about rising sea levels or tsunamis" should surface Earth-observation solutions (DSCOVR, GRACE-FO, etc.) without exact keyword matches.
- Reference: github.com/romanI04/sift. It is MIT licensed but is a solo dev project from Feb 2026 with 2 stars. Treat it as a reference only, NOT a dependency. We must be able to reimplement the semantic layer ourselves if it's abandoned. The risk is a gap while rebuilding, not technical debt.

**Other requirements**
- Keep the MIT/Pagefind attribution visible or documented, for credibility.
- Test with real queries against the 80+ solution pages across 10 hubs.
- Key test case: "my parents died 3,000 years ago because of a tsunami, I'm interested in space technology and ocean technology that may help people stay away from such devastation". It should connect tsunami, ocean monitoring, early warning and satellite observation coherently.
- Do not break the existing site. Pagefind is additive.

### 2. Hero page design (new homepage concept)
Expect trial and error. Keep it free of clutter but powerful.
- **Top of page:** "Saving Planets semantic search", kept short, small and ownable. An MIT badge sits on top of "semantic" as silent proof of credibility, so users who don't know what semantic or AI means still see a trusted backbone.
- **Center of screen:** one big search bar, nothing else.
- **Background:** a soft, low-opacity nebula watermark, maybe slowly drifting, kept crisp.
- **Below the bar:** "Would you like help framing your question so you're able to zero in to exactly [what you're after]?" It's an open invitation, not forced.
- **"How to frame your question" section:**
  - It shows a few rotating example prompts that are deliberately vague and human, such as "something that protects my family from weather", "how space tech helps farmers" and "ways to clean a river near me".
  - Clicking an example runs it through the semantic layer and shows the matched solutions.
  - A before/after shows how refining the question changes the results.
  - This teaches the 90% lesson: AI is about how you frame the question and drill in based on the answers, reframing until you pinpoint the output. No jargon. Show, don't tell.
- **Avoid copyrighted phrases.** For example, "goosefraba" from Anger Management is fine in conversation but not as a branded site term, so we'll invent our own made-up word instead.
- **Branding to weave in:** MIT, semantics, savingplanets.com, SI, and its biological SI partner.
- **Tagline concept:** "MIT, semantics, savingplanets.com, SI, and including its biological SI partner brings you [made-up word] searching."

### 3. Context
- The site owner likes dense-but-directed sites that are interesting to explore without 1,000 rabbit holes.
- Strong focus on solutions and people working together. Not quantum mechanics or carburetors.
