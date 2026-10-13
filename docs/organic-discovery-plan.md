# Organic Discovery Plan - Oct 13, 2026

Goal: maximize free, organic discovery of www.savingplanets.com (en/fr/es/ar) in Spain, UK, Australia, French- and Arabic-speaking countries before any ad spend.
Status checked by web research on Oct 13, 2026 unless marked "(not re-verified)".

## Current technical SEO: is it enough?
In place: titles/meta descriptions, OG/Twitter, canonical, hreflang en/fr/es/ar + x-default (pages and sitemap), robots.txt with Sitemap line, schema.org JSON-LD (Article/CollectionPage/LearningResource/Organization), GA4.
That covers every crawler-based engine below. What's missing is platform-specific, not markup:
- Ownership verification (Google, Bing, Yandex, Naver). Use a meta tag in index.html, or a DNS TXT record in Cloudflare. Both work with GitHub Pages + Cloudflare. Bing can also import from Search Console.
- IndexNow key file + ping on deploy (not set up yet).
- Cloudflare Crawler Hints (dashboard toggle). It sends IndexNow automatically for cached changes; it's a lighter alternative or complement to a script.
- Make sure Cloudflare Bot Fight Mode / "Block AI bots" doesn't block Googlebot/Bingbot/YandexBot/Mojeek/Brave crawlers. Check under Security > Bots.

## Platform table
| Platform | Index | Sitemap/robots | Multilingual | Submission / cost | Priority |
|---|---|---|---|---|---|
| Google Search Console | Own | Yes | hreflang fully supported | Free; verify (meta/DNS) and submit sitemap | P1 |
| Bing Webmaster Tools | Own; powers Yahoo, DuckDuckGo (mostly), parts of Ecosia/Qwant, plus ChatGPT/Copilot search grounding | Yes | hreflang used as a hint; also reads content-language | Free; import from GSC or meta/DNS; IndexNow | P1 |
| IndexNow (Bing, Yandex, Naver, Seznam, Yep, Amazon) | Shared protocol | Key file at root | n/a | Free; one POST to api.indexnow.org reaches all | P1 (in-repo) |
| Yahoo / DuckDuckGo | Bing results | via Bing | via Bing | Nothing separate | covered by Bing |
| Ecosia / Qwant (EUSP index, Paris) | Own EUSP index live in France since Aug 2025 and in Germany since Jul 30, 2026; otherwise Bing/Google mix | Crawls normally; no webmaster portal | FR strong | No submission; Bing + crawlability | P2 (matters for FR) |
| Brave Search | Own independent index | Yes | Yes | Free URL submission at search.brave.com/submit-url (no webmaster tools) | P2 |
| Yandex Webmaster | Own | Yes; supports hreflang | Yes | Free; verify by meta/DNS/file; IndexNow | P3 (low use in target regions) |
| Mojeek (UK) | Own | Yes | Mostly EN | No manual submission; discovered via links | P3 (passive) |
| Startpage | Google results | via Google | via Google | Nothing separate | covered by Google |
| Seznam (CZ) / Naver (KR) / Yahoo Japan (Google results) | Own / own / Google | Yes | Not target languages | IndexNow covers Seznam/Naver | Skip (P4) |
| Baidu | Own | Yes | Chinese-first; needs fast China access | Free webmaster tools; slow for non-.cn sites (not re-verified) | Skip |
| Google Scholar / BASE / CORE / Semantic Scholar | Scholarly | BASE/CORE need OAI-PMH repository; Scholar needs scholarly papers with citation_* meta | n/a | Free but eligibility fails | Not applicable: site is educational, not peer-reviewed research. Be honest about this. |
| OER Commons | Education library | n/a | Multilingual | Free account; "Submit from Web"; librarian review in 24-48h | P1 education |
| MERLOT | Higher-ed OER | n/a | Mostly EN | Free member submission, peer review optional (not re-verified) | P2 |
| Common Sense Education | Editorial reviews | n/a | EN | Editorial pick only; can pitch, no guaranteed listing (not re-verified) | P3 |
| PBS LearningMedia | Partner content only | n/a | EN/ES | Not open to submissions (not re-verified) | Skip |
| Scootle (AU) | Teacher portal, Education Services Australia | n/a | EN | Teacher-login portal of curated resources; no public submission route; reach AU teachers via contacts (Scootle Community) | P3 |
| UK: Oak National Academy, TES resources, STEM Learning (stem.org.uk), Scoilnet (IE) | Teacher platforms | n/a | EN | TES free upload of teacher sheets; STEM Learning resource suggestions (not re-verified) | P2 (TES upload of teacher sheets) |
| Eduscol / Éduthèque (FR) | Ministry-curated | n/a | FR | Institutional partners only (not re-verified) | P4 |
| Procomún / INTEF (ES) | OER repository | n/a | ES | Free registered upload of open resources (not re-verified) | P2 for Spain |
| Edraak (Arabic MOOCs) / TelmidTICE (MA ministry) | Curated platforms | n/a | AR/FR | Partnership only (not re-verified) | P4; outreach later |
| Curlie (DMOZ successor) | Human directory | n/a | Has French/Spanish/Arabic "World" branches | Free; submit once to one specific category; volunteer review, highly selective, no express option | P2 (submit EN + World/Français etc.) |
| NASA/ESA/NOAA education partner lists | Curated | n/a | | Usually for partner orgs; link requests to featured agencies' outreach pages are possible (not re-verified) | P3 |
| UN SDG platforms (SDG Actions Platform), Idealist, Earthday.org partners, Candid/GuideStar | Org directories | n/a | Multilingual | Need a registered org (nonprofit or similar) for most | Later, once a legal entity exists |
| Wikipedia / Wikidata | Encyclopedia | n/a | All languages | Wikipedia needs independent coverage (notability); don't self-write. A Wikidata item is also on hold until there's independent sourcing | Later |
| Google Business, Apple/Google News, podcasts | n/a | | | Not relevant (no storefront, not a news publisher) | Skip |

## Prioritized actions
### I can do these in the repo (proposals; not implemented yet)
1. Add an IndexNow key file (`<key>.txt` at root) plus `scripts/indexnow-ping.py`, run from weekly-sync.sh: POST changed URLs from sitemap lastmod to api.indexnow.org. Low risk.
2. Add placeholders for verification meta tags in the seo-fix.py head template (google-site-verification, msvalidate.01, yandex-verification). Fill them in once the user provides codes.
3. Check that robots.txt allows Bingbot, YandexBot, MojeekBot and Brave's crawler, and that sitemap lastmod is accurate. Both were done by the parallel SEO job; re-check after it lands.
4. Draft descriptions for submissions (Curlie EN/FR/ES/AR, OER Commons metadata, TES teacher-sheet listings).
5. Track referrers in GA4 for bing, duckduckgo, ecosia, qwant, brave, startpage, chatgpt, perplexity.

### User actions (need sign-in)
1. Google Search Console: add a Domain property via DNS TXT in Cloudflare, then submit sitemap.xml.
2. Bing Webmaster Tools: import from GSC and submit the sitemap. This also covers Yahoo, DDG and much of Ecosia/Qwant.
3. Cloudflare: turn on Crawler Hints, and check that bot settings don't block search crawlers.
4. Submit the homepage at search.brave.com/submit-url.
5. OER Commons: free account, then "Submit from Web" for the Solutions page and Teachers page.
6. Curlie: suggest the site once in the most specific category (e.g. Science/Environment, or Kids & Teens), plus World/Français etc.
7. TES (UK/AU) and Procomún (ES): upload teacher sheets.
8. Yandex Webmaster (optional, 10 minutes).

## Sources
- IndexNow FAQ / participants: https://www.indexnow.org/faq , https://www.indexnow.org/searchengines
- Bing IndexNow + Cloudflare Crawler Hints: https://www.bing.com/indexnow/getstarted
- EUSP Germany rollout: https://blog.ecosia.org/eusp-germany-rollout/ ; https://www.heise.de/en/news/Ecosia-and-Qwant-launch-German-web-index-11385019.html
- Alt-engine landscape 2026: https://searchenginewatch.com/best-google-alternative-search-engines/
- Brave submit URL: https://community.brave.app/t/does-brave-have-its-own-webmaster-tools-yet/652675
- Mojeek no submissions: https://blog.mojeek.com/2020/12/frequently-asked-questions-about-mojeek-search-engines-technology-stack.html
- BASE requirements: https://base.ub.uni-bielefeld.de/about/en/index.php
- OER Commons submit: https://help.oercommons.org/support/solutions/articles/42000046849-submit-oer
- Scootle access: https://scootle.edu.au/ec/p/accessing_scootle
- Curlie submit FAQ: https://curlie.org/docs/en/help/submit.html
