#!/usr/bin/env python3
"""One Share this page bar, directly above the footer, on every real page. Six languages.
Shared markup from render(), shared CSS assets/share-bar.css, shared behavior assets/share-bar.js.
Removes the older share rows (SHARE blocks and the Learn/Teachers Classroom row) so a page has one bar.
Redirect stubs and the Google verification file are left alone. Idempotent."""
import html, os, re, urllib.parse
SITE = 'https://www.savingplanets.com/'
V = '20261113d'
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
T = {
 'en': dict(h='Share this page', share='Share', shareA='Share this page',
            x='Share on X', fb='Share on Facebook', li='Share on LinkedIn',
            mail='Email', mailA='Share by email', copy='Copy link', copied='Copied',
            spread='Help spread the word'),
 'fr': dict(h='Partager cette page', share='Partager', shareA='Partager cette page',
            x='Partager sur X', fb='Partager sur Facebook', li='Partager sur LinkedIn',
            mail='E-mail', mailA='Partager par e-mail', copy='Copier le lien', copied='Copié',
            spread='Aidez à faire passer le mot'),
 'es': dict(h='Compartir esta página', share='Compartir', shareA='Compartir esta página',
            x='Compartir en X', fb='Compartir en Facebook', li='Compartir en LinkedIn',
            mail='Correo', mailA='Compartir por correo', copy='Copiar enlace', copied='Copiado',
            spread='Ayuda a correr la voz'),
 'ar': dict(h='شارك هذه الصفحة', share='مشاركة', shareA='شارك هذه الصفحة',
            x='المشاركة على X', fb='المشاركة على فيسبوك', li='المشاركة على لينكدإن',
            mail='بريد', mailA='المشاركة بالبريد', copy='نسخ الرابط', copied='تم النسخ',
            spread='ساعد في نشر الخبر'),
 'it': dict(h='Condividi questa pagina', share='Condividi', shareA='Condividi questa pagina',
            x='Condividi su X', fb='Condividi su Facebook', li='Condividi su LinkedIn',
            mail='Email', mailA='Condividi via email', copy='Copia link', copied='Copiato',
            spread='Aiuta a far girare la voce'),
 'he': dict(h='שתפו את הדף', share='שיתוף', shareA='שתפו את הדף',
            x='שיתוף ב-X', fb='שיתוף בפייסבוק', li='שיתוף בלינקדאין',
            mail='דוא״ל', mailA='שיתוף בדוא״ל', copy='העתקת הקישור', copied='הועתק',
            spread='עזרו להפיץ את הבשורה'),
}
SKIP_DIR = {'assets', 'scripts', 'node_modules', '.git', 'i18n', 'search'}
def e(s): return html.escape(s, quote=True)
def q(s): return urllib.parse.quote(s, safe='')
def render(lang, url, title, prefix):
    t = T[lang]
    mail = 'mailto:?subject=' + q(title) + '&body=' + q(title + '\n\n' + url)
    return (
        f'<!-- SHARE:START --><link rel="stylesheet" href="{prefix}assets/share-bar.css?v={V}">'
        f'<section class="share-bar" aria-label="{e(t["h"])}" data-copied="{e(t["copied"])}" data-pagefind-ignore>'
        f'<p class="share-title">{e(t["h"])}</p><div class="share-btns">'
        f'<button type="button" class="share-btn share-native" hidden aria-label="{e(t["shareA"])}">{e(t["share"])}</button>'
        f'<a class="share-btn share-x" href="https://twitter.com/intent/tweet?url={q(url)}&amp;text={q(title)}" target="_blank" rel="noopener noreferrer" aria-label="{e(t["x"])}">X</a>'
        f'<a class="share-btn share-fb" href="https://www.facebook.com/sharer/sharer.php?u={q(url)}" target="_blank" rel="noopener noreferrer" aria-label="{e(t["fb"])}">Facebook</a>'
        f'<a class="share-btn share-li" href="https://www.linkedin.com/sharing/share-offsite/?url={q(url)}" target="_blank" rel="noopener noreferrer" aria-label="{e(t["li"])}">LinkedIn</a>'
        f'<a class="share-btn share-mail" href="{e(mail)}" aria-label="{e(t["mailA"])}">{e(t["mail"])}</a>'
        f'<button type="button" class="share-btn share-copy" data-label="{e(t["copy"])}" aria-label="{e(t["copy"])}">{e(t["copy"])}</button>'
        f'<span class="share-ok" role="status" aria-live="polite"></span>'
        f'</div><p class="share-more"><a class="share-btn share-spread" href="{prefix}Spread_the_Word.html">{e(t["spread"])}</a></p>'
        f'</section><!-- SHARE:END -->')
def lang_of(rel, text):
    top = rel.split('/')[0] if '/' in rel else ''
    if top in T: return top
    m = re.search(r'<html[^>]*\blang="([a-z]{2})"', text)
    if m and m.group(1) in T: return m.group(1)
    return 'en'
def page_url(rel, text):
    m = re.search(r'<link rel="canonical" href="(https://www\.savingplanets\.com/[^"]*)"', text)
    if m: return m.group(1)
    path = '' if rel in ('index.html',) else rel
    if path.endswith('/index.html'): path = path[:-10]
    return SITE + path
def title_of(text):
    m = re.search(r'<title>(.*?)</title>', text, re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()) if m else 'Saving Planets'
def strip_old(text):
    text = re.sub(r'<!-- SHARE:START -->.*?<!-- SHARE:END -->\n?', '', text, flags=re.S)
    text = re.sub(r'<!-- CLSHARE:START -->.*?<!-- CLSHARE:END -->\n?', '', text, flags=re.S)
    text = re.sub(r'<script\b[^>]*\bsrc="(?:\.\./)*(?:assets/)?share\.js\?[^"]*"[^>]*>\s*</script>\n?', '', text)
    return text
def is_redirect(text):
    # Short alias pages that leave immediately. The 404 page also mentions location.replace, and it stays.
    if '<footer' in text: return False
    return 'http-equiv="refresh"' in text or 'location.replace(' in text
def apply_file(rel):
    text = open(rel, encoding='utf-8').read()
    if '<html' not in text.lower() or is_redirect(text): return False
    if '<footer' not in text and '</body>' not in text: return False
    lang = lang_of(rel, text)
    prefix = '../' * rel.count('/')
    bar = render(lang, page_url(rel, text), title_of(text), prefix)
    script = f'<script src="{prefix}assets/share-bar.js?v={V}" defer></script>'
    new = strip_old(text)
    if '<footer' in new:
        new = new.replace('<footer', bar + '<footer', 1)
    else:
        new = new.replace('</body>', bar + '</body>', 1)
    if 'assets/share-bar.js' not in new:
        new = new.replace('</body>', script + '</body>', 1)
    if new != text:
        open(rel, 'w', encoding='utf-8').write(new)
        return True
    return False
def main():
    n = 0; pages = 0
    for dirpath, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR and not d.startswith('.')]
        for name in files:
            if not name.endswith('.html'): continue
            rel = os.path.relpath(os.path.join(dirpath, name), '.')
            pages += 1
            if apply_file(rel): n += 1
    print(f'share bar: wrote {n} of {pages}')
if __name__ == '__main__': main()
