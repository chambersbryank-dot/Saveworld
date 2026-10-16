# GitHub automation (Oct 15, 2026)

| File | What it does | Blocking? |
|---|---|---|
| `.github/workflows/static.yml` | Deploys Pages on every push to main (unchanged). | n/a |
| `.github/workflows/weekly-build.yml` | Runs `scripts/weekly-sync.sh`, commits changes as chambersbryank-dot, deploys Pages, runs post-deploy (IndexNow). | Schedule is OFF until repo variable `WEEKLY_BUILD_ENABLED=true`. Manual run always available. |
| `.github/workflows/quality.yml` | Weekly lychee links, Lighthouse (10 pages, all 5 languages), pa11y-ci/axe, html-validate. Updates ONE issue labelled `quality-report`. | Never blocks. |
| `.github/workflows/codeql.yml` | CodeQL for JavaScript and Python. | Reports to Security tab. |
| `.github/workflows/release.yml` | 1st of each month: tag `vYYYY.MM` + release notes from Changelog.html (`scripts/release-notes.py`). | n/a |
| `.github/dependabot.yml` | Weekly updates for GitHub Actions versions. | PRs only. |
| `.github/ISSUE_TEMPLATE/` | "Report a correction" and "Suggest a solution" forms; footer link on every page (`scripts/build-report-link.py`). | n/a |

## Switching the weekly build on
1. Actions > "Weekly build and deploy" > Run workflow (manual test). Check the commit it makes and the live site.
2. Settings > Secrets and variables > Actions > Variables > New variable `WEEKLY_BUILD_ENABLED` = `true`.
3. Stop any other machine/agent running `weekly-sync.sh` on a schedule, so two builders don't race.

## Share cards (OG images) and repository size
Today the 875 cards in `assets/og/` are committed (about 63 MB, one time). `build-og.py` keeps a manifest, so a card is only
re-rendered (and re-committed) when its photo or title changes; week-to-week growth is small.
To stop committing them entirely:
1. Set repo variable `OG_AT_BUILD=true` (cards are then rendered inside the Pages artifact by weekly-build.yml).
2. Make `static.yml` also run `pip install pillow && python3 scripts/build-og.py` before upload, otherwise a normal push would deploy without cards.
3. Then `git rm -r --cached assets/og` and add `assets/og/` to `.gitignore`.
Do all three together, or share images will 404. Old history keeps the existing 63 MB unless rewritten (not recommended).

## Secrets
None are needed. The MailerLite key stays outside the repo (`~/.mailerlite_key`, read by `scripts/newsletter-draft.js`); newsletter drafting is NOT part of these workflows.
