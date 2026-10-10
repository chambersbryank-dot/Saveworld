# Saving Planets — Solutions Minus the Doom

A static website showcasing practical, verifiable solutions for oceans, lakes, rivers, forests, and space. Built with plain HTML, CSS, and JavaScript — no frameworks, no build step.

## Live site

https://www.savingplanets.com

## Structure

- `index.html` — homepage with solution cards, stats bar, and call to action
- Category hubs: `Oceans.html`, `Lakes.html`, `Rivers.html`, `Space.html`, `Deforestation.html`
- Solution pages: Five W's plus impact statement for each featured organization
- `Search.html` — live keyword search across all pages
- `About.html` — mission and the four solutions criteria
- `Amazing_Facts.html` — sourced numbers behind the work
- `Project-Rawane.html` — in-development initiative
- `404.html` — custom not-found page
- `styles.css`, `toc-home.css`, `site.js` — shared styling and behavior
- `sitemap.xml` — for search engines
- `assets/` — images

## Solutions criteria

1. Hands-on work — the organization does the work itself
2. Published, verifiable numbers with a citable source
3. A clear donate path
4. Solutions, not advocacy

## Contributing

Email ideas@savingplanets.com with a solution or idea. If it meets the criteria, it gets a page.

## License

Content and code: all rights reserved unless otherwise noted. Images credited on each page.

## Stats engine (solutions.json)

The homepage overview and the "By the numbers" block on every hub and solution page are generated from one file, `assets/data/solutions.json`. Do not edit it by hand.

To add a new solution:

1. Add these tags to the page `<head>`:
   - `<meta name="sp:category" content="ocean|lakes|rivers|forests|space|planetary-defense|space-weather|earth-observation|project-r">`
   - `<meta name="sp:type" content="hub|solution">`
   - `<meta name="sp:classification" content="natural|corporate|agency|nonprofit">` (solutions)
   - `<meta name="sp:status" content="active|horizon">` (horizon = no confirmed contract or funding yet; counted separately, never summed)
   - optional, repeatable: `<meta name="sp:stat" content="label|value|unit|kind|sourceUrl">` (kind `impact` = summable, `fact` = descriptive). Only numbers already on the page with a source.
2. Add `<section class="page-stats" data-stats-category="..." data-stats-page="Page.html" aria-label="Solution stats" hidden></section>` just before the next-solutions block (before the footer on hubs).
3. Add the page to `sitemap.xml`.
4. Run `node build-search-index.js` (updates Search.html and solutions.json; warns about pages missing sp: metadata). Commit both.

Upcoming missions are counted from `[data-mission]` widgets with a future `data-launch` / `data-arrival`.
