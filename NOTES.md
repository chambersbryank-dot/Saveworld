# Save The Planet — Project Notes

## Status (as of October 8, 2026)

### Saturn Image Upload — TEMPORARY FILENAME
- **Current file on repo:** `assets/IMG_0060.jpeg` (uploaded from iPad photo library)
- **index.html space card** points to `assets/IMG_0060.jpeg` (updated Oct 8)
- **Homepage hero background** also uses `assets/IMG_0060.jpeg` (space-led hero, updated Oct 8)
- **Planned rename:** `IMG_0060.jpeg` → `Saturn.jpg` (blocked on iPad GitHub app upload flow)
- **When renamed:** revert index.html src back to `assets/Saturn.jpg` (both space card and hero background)
- **Source:** Cassini Saturn photo, public domain (Wikimedia Commons) — no attribution required

### Open Items
1. Rename `assets/IMG_0060.jpeg` to `assets/Saturn.jpg` and update index.html references (space card + hero background)
2. SEO meta-tagging standard across all pages — DONE 2026-10-08 (see session log)
3. Weekly copyright scan of all assets
4. Build missing homepage sections: Actions, Community, Join — DONE 2026-10-08
5. Homepage hero overhaul — DONE 2026-10-08 (space-led hero, impact stat bar, under-construction banner, ideas email line)
6. Hero centering fix — DONE 2026-10-08 (hero-content width 100%, h1 white with text-shadow, CTA padding)
7. Join Movement / subscription system — ON HOLD (brainstorming; Formspree or Buttondown options discussed)
8. Cloudflare Email Routing — create `ideas@saveplanetminusthedoom.com` mailbox so the hero email link works

### Completed Today
- Uploaded Saturn photo to assets folder (as IMG_0060.jpeg)
- Updated index.html space card to reference IMG_0060.jpeg
- Confirmed assets folder structure and file listing
- **SEO meta tagging implemented across all 5 pages** (index, Space, Ocean_Cleanup, Oceans, Amazing_Facts): title tags 50-60 chars front-loading keyword, meta descriptions 150-160 chars ending in CTA, Open Graph (og:title/description/image/url/type/site_name), Twitter Card summary_large_image, canonical absolute URLs, meta robots index,follow, JSON-LD structured data (Organization, WebPage, BreadcrumbList). Keywords meta removed per 2026 research (legacy noise). FAQPage skipped (rich results removed May 2026).
- **styles.css updated:** SEO/accessibility polish — heading font-weight 700, letter-spacing, color hierarchy (h1 navy #003366, h2/h3 primary blue, impact/page-hero headings white), link hover states (primary -> accent teal), strong/bold navy, em italic #444, .sr-only utility, img max-width 100%. Visual design system unchanged.
- **Space.html JSON-LD headline alignment:** WebPage name and BreadcrumbList item now match visible H1 "Computing Above the Clouds" (was "Space Data Centers").
- **Sticky nav Home link:** All 5 pages (index, Space, Ocean_Cleanup, Oceans, Amazing_Facts) now show logo + bold "Home" link in primary blue (#0066cc) immediately right of the logo, linking to index.html. styles.css: .logo is flex with gap, .nav-home bold 700, 1.15rem, hover accent teal.
- **Homepage overhaul (2026-10-08):** Space-led hero with Saturn image background and "Computing Above the Clouds" headline; impact stat bar (15M kg plastic removed, 3:1 tree ratio, 0 gallons water in orbit); removed under-construction text; added Actions, Community, and Join sections with email signup form (placeholder alert until backend wired). styles.css: .hero.space-hero, .impact-bar, .stat-number/-label, .btn-secondary, .actions-section, .community-section, .join-section, .join-form.
- **Hero centering fix (2026-10-08):** .hero-content width 100%, h1 forced white with text-shadow, CTA padding-top 0.5rem so buttons don't overlap text.
- **Under-construction banner restored (2026-10-08):** .under-construction back in hero below CTA buttons, orange pulse animation.
- **Hero ideas email line (2026-10-08):** Below under-construction, added "Please email ideas@saveplanetminusthedoom.com with your ideas for the page" as a clickable mailto link. styles.css: .hero-email, .hero-email a (white, bold, underline, hover accent teal).

## Session Log — 2026-10-08 (Under-construction + ideas email)

- Updated index.html: restored .under-construction paragraph in hero below .hero-cta; added .hero-email paragraph with mailto:ideas@saveplanetminusthedoom.com link inviting visitor ideas.
- Updated styles.css: added .hero-email and .hero-email a styles (white, bold, underline, hover accent).
- Updated NOTES.md: logged changes, added open items 7 and 8.

## Session Log — 2026-10-08 (Hero centering fix)

- Updated styles.css: .hero-content { width: 100%; }, .hero h1 { text-align: center; }, .hero-cta { padding-top: 0.5rem; }.
- Updated NOTES.md: logged fix.

## Session Log — 2026-10-08 (Homepage overhaul)

- Updated index.html: hero changed from generic welcome to space-led "Computing Above the Clouds" with Saturn background (IMG_0060.jpeg); added impact stat bar above solutions; removed under-construction pulsating text; added Actions (#actions), Community (#community), Join (#join) sections so all nav links resolve.
- Updated styles.css: .hero.space-hero background, .impact-bar with accent-colored stat numbers, .btn-secondary outline style, .actions-section/.community-section/.join-section layouts, .join-form email input styling. Mobile breakpoints added for hero height and stat bar.
- Updated NOTES.md: logged overhaul, closed open item 4.

## Session Log — 2026-10-08 (Sticky nav Home link)

- Updated index.html, Space.html, Ocean_Cleanup.html, Oceans.html, Amazing_Facts.html: added `<a href="index.html" class="nav-home">Home</a>` inside .logo div, immediately after the logo image link.
- Updated styles.css: .logo { display:flex; align-items:center; gap:0.9rem; }, .nav-home { color:var(--primary); font-weight:700; font-size:1.15rem; }, .nav-home:hover { color:var(--accent); }.
- Updated NOTES.md: logged nav change.

## Session Log — 2026-10-08 (Space.html JSON-LD headline alignment)

- Updated Space.html: JSON-LD WebPage name changed from "Space Data Centers" to "Computing Above the Clouds" to match visible H1; BreadcrumbList position-2 item updated to match.
- Title tag, OG, and Twitter titles left as "Space Data Centers in Orbit | Save The Planet" — those are search-optimized and don't need to match the H1.
- Updated NOTES.md: logged fix.

## Session Log — 2026-10-08 (SEO meta tagging + CSS polish)

- Updated index.html: full SEO head (title, description, OG, Twitter, canonical, robots, JSON-LD Organization/WebPage/BreadcrumbList); space card image still IMG_0060.jpeg (temporary).
- Updated Space.html: full SEO head; removed legacy keywords meta; JSON-LD WebPage name "Space Data Centers" matching visible H1 "Computing Above the Clouds" (headline must match visible H1 per standard).
- Updated Ocean_Cleanup.html: full SEO head; removed keywords meta.
- Updated Oceans.html: full SEO head; removed keywords meta.
- Updated Amazing_Facts.html: full SEO head; removed keywords meta.
- Updated styles.css: appended SEO/accessibility polish block (heading weights, color hierarchy, link hovers, sr-only, img max-width). No visual design changes — palette, cards, nav, heroes unchanged.
- Updated NOTES.md: logged SEO implementation, closed open item 2, added session log.

## Session Log — 2026-10-08 (SEO completion: Amazing_Facts + Oceans)

- Updated Amazing_Facts.html: full SEO head (title 50-60 chars front-loading keyword, description 150-160 chars ending in CTA, OG, Twitter Card summary_large_image, canonical, robots index,follow, JSON-LD Organization/WebPage/BreadcrumbList); removed legacy keywords meta; og:image set to StreamLog.JPG (page's featured image).
- Updated Oceans.html: full SEO head; removed legacy keywords meta; og:image set to OceanBeach.JPG.
- All five pages now carry the complete SEO standard. styles.css unchanged this round (polish block already in place).
- Updated NOTES.md: logged completion.
