#!/usr/bin/env python3
"""Oct 16 2026 (user-approved): grow the Weekly Brief list and teacher sharing, COPPA-safe.
- CLSHARE block after the <h1> on Learn hub, guides, math, labs and Teachers (5 langs): Google Classroom share (plain link to
  classroom.google.com/share, no Google script) + Copy link button; clicks counted via site.js spTrack('share') -> /e.
- NLCALL block before </main> on adult/teen pages only (Learn hub, *_Math, Teachers): Weekly Brief callout "for teachers,
  parents and students 13+", reusing the MailerLite double opt-in form rendered by site.js into [data-sp-newsletter]
  (when such a host exists, site.js does not add the footer form, so there is one form per page).
- Kids-directed pages (audit list + guides and labs, which are written for kids/teens): body gets data-no-newsletter (site.js
  skips the footer signup) and GROWNUPS block at the top of the footer: "Grown-ups: get the Weekly Brief" -> Teachers#weekly-brief.
Idempotent. Run in weekly-sync.sh after build-learn.py and the footer generators."""
import re, glob, os, html, urllib.parse
SITE = 'https://www.savingplanets.com/'; V = '20261016s'
TRACKS = ['Orbits', 'Orbit', 'Aero', 'Physics']
def kind(b):
    if b == 'Learn.html': return 'learn'
    if b == 'Teachers.html': return 'teachers'
    m = re.match(r'(Orbits?|Aero|Physics)_(Guide|Math|Lab)\.html$', b)
    return m.group(2).lower() if m else None
KIDS = {'Kids_Map.html', 'Amazing_Facts.html', 'Satellite_Explorer.html', 'Spot_the_Fire.html', 'Myth_vs_Fact.html', 'Play_and_Learn.html', 'Glossary.html'}
T = {
 'en': dict(grp='Share this page', cr='Share to Google Classroom', cp='Copy link', ok='Link copied', aud='For teachers, parents and students 13+',
            gu='Grown-ups: get the Weekly Brief', newtab='(opens in a new tab)'),
 'fr': dict(grp='Partager cette page', cr='Partager sur Google Classroom', cp='Copier le lien', ok='Lien copié', aud='Pour les enseignants, les parents et les élèves de 13 ans et plus',
            gu='Adultes : recevez le Brief hebdomadaire', newtab='(s’ouvre dans un nouvel onglet)'),
 'es': dict(grp='Compartir esta página', cr='Compartir en Google Classroom', cp='Copiar enlace', ok='Enlace copiado', aud='Para docentes, familias y estudiantes de 13 años o más',
            gu='Adultos: reciban el Resumen semanal', newtab='(se abre en una pestaña nueva)'),
 'ar': dict(grp='شارك هذه الصفحة', cr='المشاركة في Google Classroom', cp='نسخ الرابط', ok='نُسخ الرابط', aud='للمعلمين وأولياء الأمور والطلاب من سن 13 عامًا فأكثر',
            gu='للبالغين: احصلوا على النشرة الأسبوعية', newtab='(يُفتح في علامة تبويب جديدة)'),
 'it': dict(grp='Condividi questa pagina', cr='Condividi su Google Classroom', cp='Copia link', ok='Link copiato', aud='Per insegnanti, genitori e studenti dai 13 anni in su',
            gu='Adulti: ricevete il Brief settimanale', newtab='(si apre in una nuova scheda)'),
}
CSS = ('<style>.shr{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:.6rem 0 1.2rem}.shr a.shr-cr,.shr button.shr-copy{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px;'
       'border-radius:999px;font:600 .95rem Montserrat,system-ui,sans-serif;text-decoration:none;cursor:pointer;box-sizing:border-box;border:1px solid rgba(0,156,222,.6);background:rgba(0,156,222,.12);color:inherit}'
       '.shr a.shr-cr:hover,.shr button.shr-copy:hover{background:rgba(0,156,222,.25)}.shr a.shr-cr:focus-visible,.shr button.shr-copy:focus-visible{outline:2px solid #8fd3ff;outline-offset:2px}'
       '.shr svg{width:20px;height:20px;flex:none}.shr .shr-copy.is-done{border-color:#5fe0b5}.shr-st{font-weight:600;font-size:.9rem}'
       '.nl-call{max-width:720px;margin:2.4rem auto 1rem;padding:0 1rem}.nl-call .nl-aud{text-align:center;font-weight:700;font-size:.85rem;letter-spacing:.04em;text-transform:uppercase;margin:0 0 -1.6rem;position:relative;z-index:1}'
       '.nl-call .nl-aud span{display:inline-block;background:#009cde;color:#fff;border-radius:999px;padding:4px 12px}.gu-link{text-align:center;margin:1rem 0}.gu-link a{display:inline-block;min-height:44px;line-height:44px;padding:0 16px;font-weight:700}</style>')
ICON_CR = '<svg aria-hidden="true" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.2" fill="currentColor"/><path d="M8 15c.8-1.6 2.3-2.4 4-2.4s3.2.8 4 2.4M7 21h10" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
ICON_CP = '<svg aria-hidden="true" viewBox="0 0 24 24"><rect x="8" y="8" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
def strip(s, k): return re.sub(rf'<!-- {k}:START -->.*?<!-- {k}:END -->', '', s, flags=re.S)
def main():
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in T or f.endswith('Kids.html'): continue
        b = os.path.basename(f); k = kind(b); t = T[l]; e = lambda x: html.escape(x, quote=True); pre = '' if l == 'en' else '../'
        s = open(f, encoding='utf8').read(); s2 = s
        for blk in ('CLSHARE', 'NLCALL', 'GROWNUPS'): s2 = strip(s2, blk)
        if k:
            m = re.search(r'<h1[^>]*>.*?</h1>', s2, re.S)
            url = SITE + ('' if l == 'en' else l + '/') + b
            title = re.sub(r'<[^>]+>', '', m.group(0)).strip() if m else 'Saving Planets'
            cr = 'https://classroom.google.com/share?' + urllib.parse.urlencode({'url': url, 'title': title + ' | Saving Planets'})
            bar = (f'<!-- CLSHARE:START -->{CSS}<div class="shr" role="group" aria-label="{e(t["grp"])}" data-url="{url}" data-page="{k}">'
                   f'<a class="shr-cr" href="{e(cr)}" target="_blank" rel="noopener noreferrer">{ICON_CR}<span>{e(t["cr"])}</span><span class="sr-only visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">{e(t["newtab"])}</span></a>'
                   f'<button type="button" class="shr-copy" data-ok="{e(t["ok"])}">{ICON_CP}<span>{e(t["cp"])}</span></button>'
                   f'<span class="shr-st" role="status" aria-live="polite"></span></div><script src="{pre}assets/share.js?v={V}" defer></script><!-- CLSHARE:END -->')
            if m: s2 = s2[:m.end()] + bar + s2[m.end():]
        if k in ('learn', 'math', 'teachers') and '</main>' in s2:
            call = f'<!-- NLCALL:START --><aside class="nl-call" id="weekly-brief" aria-label="Weekly Brief"><p class="nl-aud"><span>{e(t["aud"])}</span></p><div data-sp-newsletter></div></aside><!-- NLCALL:END -->'
            s2 = s2.replace('</main>', call + '</main>', 1)
        if b in KIDS or k in ('guide', 'lab'):
            s2 = re.sub(r'<body(?![^>]*data-no-newsletter)([^>]*)>', r'<body\1 data-no-newsletter>', s2, count=1)
            s2 = s2.replace('<footer>', f'<footer><!-- GROWNUPS:START --><p class="gu-link"><a href="Teachers.html#weekly-brief">{e(t["gu"])}</a></p><!-- GROWNUPS:END -->', 1)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-share: {n} pages')

# Oct 16 add-on: /Kids.html (404 before) -> Play_and_Learn.html redirect page in all 5 languages (meta refresh + canonical + link).
RD = {'en': ('Kids', 'Go to Play and Learn'), 'fr': ('Enfants', 'Aller à Jouer et apprendre'), 'es': ('Niños', 'Ir a Jugar y aprender'),
      'ar': ('الأطفال', 'انتقل إلى العب وتعلّم'), 'it': ('Bambini', 'Vai a Gioca e impara')}
def redirects():
    for l, (title, go) in RD.items():
        d = '' if l == 'en' else l + '/'; target = SITE + d + 'Play_and_Learn.html'
        page = (f'<!DOCTYPE html>\n<html lang="{l}" dir="{"rtl" if l == "ar" else "ltr"}"><head><meta charset="utf-8"><title>{title} | Saving Planets</title>'
                f'<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, follow">'
                f'<link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0; url=Play_and_Learn.html"></head>'
                f'<body style="font-family:system-ui,sans-serif;padding:2rem;text-align:center"><p><a href="Play_and_Learn.html" style="display:inline-block;min-height:44px;line-height:44px;font-size:1.2rem">{go}</a></p></body></html>\n')
        p = d + 'Kids.html'
        if not os.path.exists(p) or open(p, encoding='utf8').read() != page: open(p, 'w', encoding='utf8').write(page)

if __name__ == '__main__': redirects(); main()
