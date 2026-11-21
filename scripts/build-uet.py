#!/usr/bin/env python3
"""Microsoft Advertising UET (tag ID 343288039) for ad-visit and Donate-click measurement.

Idempotent. Run after the other page generators (weekly-sync.sh calls it last).
- Public pages, all six languages: async UET base tag (https://bat.bing.com/bat.js, ti 343288039)
  plus one delegated click listener. The listener pushes
  window.uetq.push('event', 'donate_click', {event_category, event_label})
  and does not cancel or delay the click. Donate links already open in a new tab.
- Kids pages, kids maps, and kid games/quests (and localized copies) get neither the tag nor the listener.
- Privacy.html gains one plain sentence in each language, with Microsoft's privacy statement linked.
- The old "no ad tracking" / "nothing sets a tracking cookie" lines are rewritten so they stay true.
  The Cloudflare visit count is still cookie-free. The UET block is ignored by i18n-check (<!-- UET:START -->).

Donate clicks are external organization donation links only:
  a[data-sp-donate], a Donate button inside #donations, or a link whose own label is a Donate word
  (Donate, Donar, Faire un don, Dona, تبرّع, לתרומה). "For further information" uses class donate-btn
  and is not a donation link. Nav and sticky "Donate / Help" point at Ways to Help on this site.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {'.git', 'pagefind', 'node_modules'}
SKIP_NAMES = {'googlea5d3cc0c785fec04.html'}
LANGS = ('fr', 'es', 'ar', 'it', 'he')
TI = '343288039'
# Basename match, so /fr/Kids_Map.html is excluded the same way as /Kids_Map.html.
# Play and Learn hub tiles, plus Kids.html (redirect) and Spot the Fire (kid game, not always on the hub).
KIDS = {
    'Kids.html',                 # redirect to Play and Learn
    'Play_and_Learn.html',       # kids hub
    'Kids_Map.html',             # kids planet map
    'Kids_World.html',           # kids world map
    'Amazing_Facts.html',        # kids facts
    'Myth_vs_Fact.html',         # kids myth game source, on the kids hub
    'Glossary.html',             # kids-hub glossary, no sign-up
    'Satellite_Explorer.html',   # drag-and-build satellite game
    'Earth_Satellite_Explorer.html',  # kid satellite explorer
    'Spot_the_Fire.html',        # kid spotting game
    'Space_Passport.html',       # kid quest
    'Boarding_Pass.html',        # kid quest
    'Myth_or_Fact_Arcade.html',  # kid tap game
}

A = '\u2019'  # same apostrophe the privacy pages already use

# Short version: the site still shows no ads. It does measure ad visits, so "no ad tracking" was no longer true.
SHORT = {
    'en': (
        'Saving Planets has no accounts, no ads and no ad tracking. We do not sell or share personal information.',
        'Saving Planets has no accounts and shows no ads. We do not sell or share personal information.',
    ),
    'fr': (
        f'Saving Planets n{A}a ni comptes, ni publicités, ni pistage publicitaire. Nous ne vendons ni ne partageons aucune information personnelle.',
        f'Saving Planets n{A}a pas de comptes et n{A}affiche pas de publicité. Nous ne vendons ni ne partageons aucune information personnelle.',
    ),
    'es': (
        'Saving Planets no tiene cuentas, ni anuncios, ni rastreo publicitario. No vendemos ni compartimos información personal.',
        'Saving Planets no tiene cuentas y no muestra anuncios. No vendemos ni compartimos información personal.',
    ),
    'ar': (
        'لا توجد في Saving Planets حسابات ولا إعلانات ولا تتبع إعلاني. نحن لا نبيع المعلومات الشخصية ولا نشاركها.',
        'لا توجد في Saving Planets حسابات ولا إعلانات في صفحاته. نحن لا نبيع المعلومات الشخصية ولا نشاركها.',
    ),
    'it': (
        'Saving Planets non ha account, nessun annuncio e nessun tracciamento pubblicitario. Non vendiamo o condividiamo le informazioni personali.',
        'Saving Planets non ha account e non mostra annunci. Non vendiamo o condividiamo le informazioni personali.',
    ),
    'he': (
        'ל-Saving Planets אין חשבונות, אין פרסומות ואין מעקב פרסומי. איננו מוכרים או משתפים מידע אישי.',
        'ל-Saving Planets אין חשבונות והאתר אינו מציג פרסומות. איננו מוכרים או משתפים מידע אישי.',
    ),
}
# Cloudflare's count is still cookie-free. UET may set a cookie, so the old "nothing sets a tracking cookie" line was false.
GA = {
    'en': (
        'We stopped using Google Analytics on October 16, 2026, so there is no consent banner: nothing on this site sets a tracking cookie.',
        'We stopped using Google Analytics on October 16, 2026. The Cloudflare visit count does not use a tracking cookie.',
    ),
    'fr': (
        f'Nous n{A}utilisons plus Google Analytics depuis le 16 octobre 2026 ; il n{A}y a donc plus de bandeau de consentement : rien sur ce site ne dépose de cookie de suivi.',
        f'Nous n{A}utilisons plus Google Analytics depuis le 16 octobre 2026. Le comptage des visites par Cloudflare ne dépose pas de cookie de suivi.',
    ),
    'es': (
        'Dejamos de usar Google Analytics el 16 de octubre de 2026, así que no hay banner de consentimiento: nada en este sitio instala una cookie de seguimiento.',
        'Dejamos de usar Google Analytics el 16 de octubre de 2026. El recuento de visitas de Cloudflare no instala una cookie de seguimiento.',
    ),
    'ar': (
        'توقفنا عن استخدام Google Analytics في 16 أكتوبر 2026، لذلك لا يوجد شريط موافقة: لا شيء في هذا الموقع يضع ملف تعريف ارتباط للتتبع.',
        'توقفنا عن استخدام Google Analytics في 16 أكتوبر 2026. حساب الزيارات في Cloudflare لا يضع ملف تعريف ارتباط للتتبع.',
    ),
    'it': (
        f'Abbiamo smesso di usare Google Analytics il 16 ottobre 2026, quindi non c{A}è un banner di consenso: niente su questo sito imposta cookie di tracciamento.',
        f'Abbiamo smesso di usare Google Analytics il 16 ottobre 2026. Il conteggio delle visite di Cloudflare non imposta un cookie di tracciamento.',
    ),
    'he': (
        'הפסקנו להשתמש ב-Google Analytics ב-16 באוקטובר 2026, ולכן אין באנר הסכמה: שום דבר באתר הזה לא מגדיר עוגיית מעקב.',
        'הפסקנו להשתמש ב-Google Analytics ב-16 באוקטובר 2026. ספירת הביקורים של Cloudflare אינה מגדירה עוגיית מעקב.',
    ),
}
# One plain sentence. {link} is Microsoft's privacy statement.
PRIV = {
    'en': f'This site uses Microsoft Advertising{A}s tracking tag to measure ad visits and Donate clicks, it may set a cookie, it does not collect donation amounts or personal donation data, and it is not loaded on kids pages ({{link}}).',
    'fr': f'Ce site utilise la balise de suivi de Microsoft Advertising pour mesurer les visites issues des annonces et les clics sur Faire un don, elle peut déposer un cookie, elle ne collecte ni montants ni données personnelles de don, et elle n{A}est pas chargée sur les pages pour enfants ({{link}}).',
    'es': 'Este sitio usa la etiqueta de seguimiento de Microsoft Advertising para medir las visitas desde anuncios y los clics en Donar, puede instalar una cookie, no recoge importes ni datos personales de las donaciones y no se carga en las páginas infantiles ({link}).',
    'ar': 'يستخدم هذا الموقع وسم التتبع من Microsoft Advertising لقياس زيارات الإعلانات والنقرات على التبرع، وقد يضع ملف تعريف ارتباط، ولا يجمع مبالغ التبرع ولا بيانات التبرع الشخصية، ولا يُحمَّل على صفحات الأطفال ({link}).',
    'it': f'Questo sito usa il tag di monitoraggio di Microsoft Advertising per misurare le visite dagli annunci e i clic su Dona, può impostare un cookie, non raccoglie importi né dati personali delle donazioni e non viene caricato nelle pagine per bambini ({{link}}).',
    'he': 'אתר זה משתמש בתג המעקב של Microsoft Advertising כדי למדוד ביקורים ממודעות ולחיצות על תרומה, הוא עשוי להגדיר עוגייה, הוא אינו אוסף סכומי תרומה או נתוני תרומה אישיים, והתג אינו נטען בעמודי ילדים ({link}).',
}
LINK = {
    'en': f'Microsoft{A}s privacy statement',
    'fr': 'déclaration de confidentialité de Microsoft',
    'es': 'declaración de privacidad de Microsoft',
    'ar': 'بيان خصوصية Microsoft',
    'it': 'informativa sulla privacy di Microsoft',
    'he': 'הצהרת הפרטיות של Microsoft',
}

# Labels on Donate buttons. Arabic includes the form with and without the kashida.
# The listener also accepts data-sp-donate and any Donate button inside #donations.
UET_JS = r"""<!-- UET:START --><script>(function(w,d,t,r,u){w[u]=w[u]||[];if(/(^|\.)savingplanets\.com$/.test(location.hostname)){var f=function(){var o={ti:"343288039",enableAutoSpaTracking:true};o.q=w[u];w[u]=new UET(o);w[u].push("pageLoad")};var n=d.createElement(t);n.src=r;n.async=1;n.onload=n.onreadystatechange=function(){var s=this.readyState;if(s&&s!=="loaded"&&s!=="complete")return;f();n.onload=n.onreadystatechange=null};var i=d.getElementsByTagName(t)[0];i.parentNode.insertBefore(n,i)}function text(a){var s=a.cloneNode(true),nodes=s.querySelectorAll(".sr-only"),i;for(i=0;i<nodes.length;i++)nodes[i].parentNode.removeChild(nodes[i]);return (s.textContent||"").replace(/\s+/g," ").trim().replace(/^[^\w\u0590-\u05FF\u0600-\u06FF]+/,"")}function external(a){var href=a.getAttribute("href")||"";if(/^(mailto:|tel:|javascript:|#)/i.test(href))return false;var host="";try{host=(a.hostname||"").toLowerCase()}catch(e){return false}if(!host||/(^|\.)savingplanets\.com$/.test(host))return false;return /^https?:$/i.test(a.protocol||"")}function isDon(a){if(a.hasAttribute("data-sp-donate"))return true;if(a.closest&&a.closest("#donations")&&a.classList.contains("help-btn"))return true;return /^(?:donate|donar|faire un don|dona|\u062A\u0628\u0631\u0639|\u062A\u0628\u0631\u0651\u0639|\u05DC\u05EA\u05E8\u05D5\u05DE\u05D4)$/i.test(text(a))}function lab(a){var sr=a.querySelector(".sr-only");if(sr){var o=(sr.textContent||"").replace(/^[\s\u2013\u2014:\-]+/,"").trim();if(o)return o.slice(0,80)}var card=a.closest&&a.closest(".wh-card");if(card){var h=card.querySelector("h3");if(h){var x=(h.textContent||"").trim();if(x)return x.slice(0,80)}}var slug=(location.pathname.split("/").pop()||"index").replace(/\.html$/i,"");return (slug||"index").slice(0,80)}d.addEventListener("click",function(e){var a=e.target&&e.target.closest&&e.target.closest("a[href]");if(!a||!isDon(a)||!external(a))return;w.uetq=w.uetq||[];w.uetq.push("event","donate_click",{event_category:"donation",event_label:lab(a)})},true)})(window,document,"script","https://bat.bing.com/bat.js","uetq");</script><noscript><img alt="" height="0" src="https://bat.bing.com/action/0?ti=343288039&amp;Ver=2" style="display:none" width="0"></noscript><!-- UET:END -->"""

UET_RE = re.compile(r'<!-- UET:START -->.*?<!-- UET:END -->', re.S)
S2_RE = re.compile(r'(<section class="five-ws" id="s2">.*?)(</section>)', re.S)


def lang_of(path):
    parts = path.relative_to(ROOT).parts
    if len(parts) == 1:
        return 'en'
    if len(parts) == 2 and parts[0] in LANGS:
        return parts[0]
    return None


def kids_page(path):
    return path.name in KIDS


def privacy_sentence(lang):
    link = ('<a href="https://privacy.microsoft.com/privacystatement" rel="noopener noreferrer" target="_blank">%s</a>'
            % html.escape(LINK[lang]))
    return '<!-- UET:START --><p>' + PRIV[lang].format(link=link) + '</p><!-- UET:END -->'


def strip_uet(text):
    return UET_RE.sub('', text)


# Meta descriptions on the Arabic privacy page repeat only the first sentence of the short version.
FRAGMENTS = {
    'ar': (
        'لا توجد في Saving Planets حسابات ولا إعلانات ولا تتبع إعلاني.',
        'لا توجد في Saving Planets حسابات ولا إعلانات في صفحاته.',
    ),
}


def apply_copy(text, lang):
    old_s, new_s = SHORT[lang]
    text = text.replace(old_s, new_s)
    old_g, new_g = GA[lang]
    text = text.replace(old_g, new_g)
    if lang in FRAGMENTS:
        text = text.replace(FRAGMENTS[lang][0], FRAGMENTS[lang][1])
    return text


def insert_privacy(text, lang):
    block = privacy_sentence(lang)
    if 'id="s2"' not in text:
        return text
    return S2_RE.sub(lambda m: m.group(1) + block + m.group(2), text, count=1)


def pages():
    for path in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.name in SKIP_NAMES:
            continue
        yield path


def update_i18n():
    """Keep the short-version string translatable. One line in each dictionary, no reformat."""
    n = 0
    for lang in LANGS:
        path = ROOT / 'i18n' / f'{lang}.json'
        raw = path.read_text(encoding='utf-8')
        old_s, new_s = SHORT['en']
        trans = SHORT[lang][1]
        old_line_start = '"' + old_s + '":'
        new_line = '"' + new_s + '": "' + trans.replace('\\', '\\\\').replace('"', '\\"') + '"'
        if old_line_start in raw:
            raw2 = re.sub(r'^' + re.escape('"' + old_s + '"') + r': ".*",$', new_line + ',', raw, count=1, flags=re.M)
            if raw2 != raw:
                path.write_text(raw2, encoding='utf-8')
                n += 1
                raw = raw2
        if lang == 'he':
            old_g, new_g = GA['en']
            he = GA['he'][1].replace('\\', '\\\\').replace('"', '\\"')
            old_g_line = '"' + old_g + '":'
            if old_g_line in raw:
                raw2 = re.sub(r'^' + re.escape('"' + old_g + '"') + r': ".*",$',
                              '"' + new_g + '": "' + he + '",', raw, count=1, flags=re.M)
                if raw2 != raw:
                    path.write_text(raw2, encoding='utf-8')
                    n += 1
    return n


def main():
    changed = 0
    tagged = 0
    excluded = []
    for path in pages():
        lang = lang_of(path)
        original = path.read_text(encoding='utf-8')
        text = strip_uet(original)
        if lang and path.name == 'Privacy.html':
            text = apply_copy(text, lang)
            text = insert_privacy(text, lang)
        if kids_page(path):
            excluded.append(str(path.relative_to(ROOT)))
        elif '</body>' in text:
            text = text.replace('</body>', UET_JS + '</body>', 1)
            tagged += 1
        if text != original:
            path.write_text(text, encoding='utf-8')
            changed += 1
    dictionaries = update_i18n()
    print(f'build-uet: {changed} files written, {tagged} pages tagged, {len(excluded)} kids pages excluded, {dictionaries} dictionaries updated')
    for rel in sorted(excluded):
        print('  excluded', rel)
    return 0 if check(excluded) else 1


def check(excluded):
    errors = []
    def read(rel):
        return (ROOT / rel).read_text(encoding='utf-8')
    for rel in ('index.html', 'Solutions.html', 'Hawaiian_Monk_Seal_Recovery.html', 'fr/index.html', 'es/Solutions.html', 'he/About.html'):
        text = read(rel)
        if 'ti:"343288039"' not in text or 'https://bat.bing.com/bat.js' not in text:
            errors.append(rel + ' missing UET tag')
        if "uetq.push(\"event\",\"donate_click\"" not in text:
            errors.append(rel + ' missing donate_click listener')
        if text.count('<!-- UET:START -->') != 1:
            errors.append(rel + ' UET block count ' + str(text.count('<!-- UET:START -->')))
    for rel in excluded:
        text = read(rel)
        if 'bat.bing.com' in text or 'uetq' in text or '343288039' in text:
            errors.append(rel + ' still has the UET tag')
    for lang, rel in (('en', 'Privacy.html'), ('fr', 'fr/Privacy.html'), ('es', 'es/Privacy.html'),
                      ('ar', 'ar/Privacy.html'), ('it', 'it/Privacy.html'), ('he', 'he/Privacy.html')):
        text = read(rel)
        if 'https://privacy.microsoft.com/privacystatement' not in text:
            errors.append(rel + ' missing Microsoft privacy link')
        if LINK[lang] not in text:
            errors.append(rel + ' missing localized link text')
        if 'nothing on this site sets a tracking cookie' in text or 'no ad tracking' in text or 'لا تتبع إعلاني' in text:
            errors.append(rel + ' still claims there is no ad tracking')
        if text.count('<!-- UET:START -->') != 2:
            errors.append(rel + ' expected privacy sentence plus tag, got ' + str(text.count('<!-- UET:START -->')))
    # Stylesheet loader must still sit beside every noscript stylesheet on the pages we ship the tag to.
    for rel in ('index.html', 'Solutions.html', 'Hawaiian_Monk_Seal_Recovery.html', 'fr/index.html', 'Privacy.html', 'Kids_Map.html'):
        text = read(rel)
        for href in re.findall(r'<noscript class="crit-ns"><link rel="stylesheet" href="([^"]+)"></noscript>', text):
            loader = '<link rel="preload" as="style" href="%s" onload="this.onload=null;this.rel=\'stylesheet\'">' % href
            if loader + '<noscript class="crit-ns"><link rel="stylesheet" href="%s">' % href not in text:
                errors.append(rel + ' stylesheet loader missing for ' + href)
    monk = read('Hawaiian_Monk_Seal_Recovery.html')
    if re.search(r'<a\b[^>]*\bdata-sp-donate\b', monk):
        errors.append('Hawaiian_Monk_Seal_Recovery.html unexpectedly gained a donate marker')
    if monk.count('class="btn help-btn"') != 2:
        errors.append('Hawaiian monk seal help buttons changed')
    snow = read('Snow_Leopard_Trust.html')
    if snow.count('data-sp-donate="1"') != 1:
        errors.append('Snow Leopard donate button count changed')
    if '>Donate</a>' not in snow:
        errors.append('Snow Leopard Donate label changed')
    for rel in errors:
        print('ERROR', rel)
    if errors:
        print(f'build-uet: {len(errors)} checks failed')
        return False
    print('build-uet: checks ok')
    return True


if __name__ == '__main__':
    sys.exit(main())
