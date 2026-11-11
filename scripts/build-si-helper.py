#!/usr/bin/env python3
"""SI Helper retirement. The Teachers-page pilot is no longer offered on the public site.

Strips the Ask SI widget (<!-- SIHELPER -->) from Teachers.html, replaces the Privacy
section with a short past-tense note, and turns SI_Helper.html into a noindex redirect
to the matching Teachers page (meta refresh + location.replace, the same pattern as
Kids.html and Community.html). Drops SI_Helper.html from the language sitemaps.

Does not delete workers/si-helper, assets/si-helper.js, Vectorize, Turnstile, or keys.
Idempotent. Kept in weekly-sync.sh so a later sync cannot put the pilot back.
"""
import os, re, sys
sys.path.insert(0, 'scripts')
import sitemap_pages

LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
MARK = re.compile(r'<!-- SIHELPER:START -->.*?<!-- SIHELPER:END -->', re.S)
SITE = 'https://www.savingplanets.com/'
BEACON = ('<!-- CF-WA:START --><script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
          "data-cf-beacon='{\"token\": \"9d4cc1c099e74c1e8b66eb937aa58186\"}'></script><!-- CF-WA:END -->")

# Heading, one-sentence note. No new data practices. The public name stays SI.
NOTE = {
 'en': ('SI Helper (Teachers page)',
        'The Teachers-page SI Helper pilot has been retired and is no longer offered.'),
 'fr': ('SI Helper (page Enseignants)',
        'Le pilote SI Helper de la page Enseignants a \u00e9t\u00e9 retir\u00e9 et n\u2019est plus propos\u00e9.'),
 'es': ('SI Helper (p\u00e1gina para docentes)',
        'El piloto SI Helper de la p\u00e1gina para docentes se ha retirado y ya no se ofrece.'),
 'ar': ('SI Helper (\u0635\u0641\u062d\u0629 \u0627\u0644\u0645\u0639\u0644\u0645\u064a\u0646)',
        '\u0623\u064f\u0648\u0642\u0641 \u0627\u0644\u0625\u0635\u062f\u0627\u0631 \u0627\u0644\u062a\u062c\u0631\u064a\u0628\u064a \u0645\u0646 SI Helper \u0641\u064a \u0635\u0641\u062d\u0629 \u0627\u0644\u0645\u0639\u0644\u0645\u064a\u0646 \u0648\u0644\u0645 \u064a\u0639\u062f \u0645\u062a\u0627\u062d\u064b\u0627.'),
 'it': ('SI Helper (pagina Insegnanti)',
        'Il pilota SI Helper della pagina Insegnanti \u00e8 stato ritirato e non \u00e8 pi\u00f9 offerto.'),
 'he': ('SI Helper (\u05d3\u05e3 \u05d4\u05de\u05d5\u05e8\u05d9\u05dd)',
        '\u05e4\u05d9\u05d9\u05dc\u05d5\u05d8 SI Helper \u05d1\u05d3\u05e3 \u05d4\u05de\u05d5\u05e8\u05d9\u05dd \u05d4\u05d5\u05e6\u05d0 \u05de\u05e9\u05d9\u05de\u05d5\u05e9 \u05d5\u05d0\u05d9\u05e0\u05d5 \u05de\u05d5\u05e6\u05e2 \u05e2\u05d5\u05d3.'),
}
LINK = {
 'en': 'Continue to Teachers',
 'fr': 'Continuer vers la page Enseignants',
 'es': 'Seguir a la p\u00e1gina para docentes',
 'ar': '\u0627\u0644\u0645\u062a\u0627\u0628\u0639\u0629 \u0625\u0644\u0649 \u0635\u0641\u062d\u0629 \u0627\u0644\u0645\u0639\u0644\u0645\u064a\u0646',
 'it': 'Continua alla pagina Insegnanti',
 'he': '\u05d4\u05de\u05e9\u05da \u05dc\u05d3\u05e3 \u05d4\u05de\u05d5\u05e8\u05d9\u05dd',
}

def d(l):
    return '' if l == 'en' else l + '/'

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def wr(path, text):
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
    if text != old:
        open(path, 'w', encoding='utf-8').write(text)
        return 1
    return 0

def privacy_block(l):
    h, p = NOTE[l]
    return (f'<!-- SIHELPER:START --><section class="five-ws" id="si-helper"><h2>{esc(h)}</h2>'
            f'<p>{esc(p)}</p></section><!-- SIHELPER:END -->')

def teachers(l):
    p = d(l) + 'Teachers.html'
    if not os.path.exists(p):
        return 0
    s = open(p, encoding='utf-8').read()
    return wr(p, MARK.sub('', s))

def privacy(l):
    p = d(l) + 'Privacy.html'
    if not os.path.exists(p):
        return 0
    s = open(p, encoding='utf-8').read()
    blk = privacy_block(l)
    if MARK.search(s):
        s2 = MARK.sub(lambda m: blk, s, count=1)
    else:
        anchor = '<section class="help-actions" id="more">'
        s2 = s.replace(anchor, blk + anchor, 1) if anchor in s else s.replace('</main>', blk + '</main>', 1)
    return wr(p, s2)

def stub(l):
    h, ptxt = NOTE[l]
    rtl = ' dir="rtl"' if l in RTL else ''
    canon = f'{SITE}{d(l)}Teachers.html'
    title = esc(h) + ' | Saving Planets'
    body = f'{esc(ptxt)} <a href="Teachers.html">{esc(LINK[l])}</a>'
    return (
        '<!DOCTYPE html>\n'
        f'<html lang="{l}"{rtl}><head><meta charset="utf-8">'
        f'<title>{title}</title><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<meta name="robots" content="noindex, follow"><link rel="canonical" href="{canon}">'
        '<meta http-equiv="refresh" content="0; url=Teachers.html">'
        '<script>location.replace("Teachers.html")</script></head>'
        '<body style="font-family:system-ui,sans-serif;padding:2rem;text-align:center">'
        f'<p style="font-size:1.05rem;line-height:1.5">{body}</p>'
        f'{BEACON}</body></html>\n'
    )

if __name__ == '__main__':
    ch = 0
    for l in LANGS:
        ch += teachers(l) + privacy(l) + wr(d(l) + 'SI_Helper.html', stub(l))
    ch += sitemap_pages.strip_page('SI_Helper.html')
    print(f'build-si-helper: retired public SI Helper, writes={ch}')
