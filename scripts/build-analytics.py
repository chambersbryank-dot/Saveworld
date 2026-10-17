#!/usr/bin/env python3
"""Oct 16 2026: Google Analytics removed site-wide (COPPA); Cloudflare Web Analytics instead (cookie-free, no local
storage, no cross-site profile). Replaces the old add-gtag.py. Idempotent; run after all page generators.
- strips the GA4 block (<!-- Google tag (gtag.js) --> ... <!-- /Google tag -->) and the consent.js include from every page
- adds the Cloudflare beacon before </body> between CF-WA markers (site token is public by design: it ships in HTML)
- updates the Privacy page analytics / children / browser-storage text in en, fr, es, ar, it
The consent banner (consent.js) is gone: with no cookies or identifiers there is nothing to consent to (logged in NOTES.md)."""
import pathlib, re, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"googlea5d3cc0c785fec04.html"}
CF_TOKEN = '9d4cc1c099e74c1e8b66eb937aa58186'  # Cloudflare Web Analytics site for savingplanets.com (created in the dashboard Oct 8)
BEACON = ("<!-- CF-WA:START --><script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
          "data-cf-beacon='{\"token\": \"%s\"}'></script><!-- CF-WA:END -->" % CF_TOKEN)
GA = re.compile(r"\n?<!-- Google tag \(gtag\.js\) -->.*?<!-- /Google tag -->", re.S)
CONSENT = re.compile(r'<script[^>]*src="(?:\.\./)?consent\.js[^"]*"[^>]*></script>\n?')
CFW = re.compile(r'<!-- CF-WA:START -->.*?<!-- CF-WA:END -->', re.S)
E = lambda s: html.escape(s, quote=False)
PRIV = {
 'en': dict(h='Analytics (Cloudflare Web Analytics)', p=[
   'We count visits with Cloudflare Web Analytics. It sets no cookies, uses no local storage and does not build a profile of you or follow you across sites. We see only totals such as page views, referring sites, countries and browser types.',
   'We stopped using Google Analytics on October 16, 2026, so there is no consent banner: nothing on this site sets a tracking cookie.'],
   kid='Analytics on every page, including kids pages, is cookie-free and counts totals only. Lesson plans are built in your browser and are not sent to us.',
   st='We save small settings, such as badges and progress in a learning tool, in your browser’s local storage. It stays on your device.',
   up='Last updated: October 16, 2026'),
 'fr': dict(h='Statistiques (Cloudflare Web Analytics)', p=[
   'Nous comptons les visites avec Cloudflare Web Analytics. Cet outil ne dépose aucun cookie, n’utilise pas le stockage local et ne crée pas de profil de vous ni ne vous suit d’un site à l’autre. Nous ne voyons que des totaux : pages vues, sites d’origine, pays et types de navigateur.',
   'Nous n’utilisons plus Google Analytics depuis le 16 octobre 2026 ; il n’y a donc plus de bandeau de consentement : rien sur ce site ne dépose de cookie de suivi.'],
   kid='Sur toutes les pages, y compris celles pour les enfants, les statistiques sont sans cookie et ne comptent que des totaux. Les plans de cours sont créés dans votre navigateur et ne nous sont pas envoyés.',
   st='Nous enregistrons de petits réglages, comme les badges et la progression dans un outil d’apprentissage, dans le stockage local de votre navigateur. Ils restent sur votre appareil.',
   up='Dernière mise à jour : 16 octobre 2026'),
 'es': dict(h='Analítica (Cloudflare Web Analytics)', p=[
   'Contamos las visitas con Cloudflare Web Analytics. No usa cookies ni almacenamiento local, y no crea un perfil tuyo ni te sigue de un sitio a otro. Solo vemos totales como páginas vistas, sitios de procedencia, países y tipos de navegador.',
   'Dejamos de usar Google Analytics el 16 de octubre de 2026, así que no hay banner de consentimiento: nada en este sitio instala una cookie de seguimiento.'],
   kid='En todas las páginas, incluidas las infantiles, la analítica no usa cookies y solo cuenta totales. Los planes de clase se crean en tu navegador y no se nos envían.',
   st='Guardamos pequeños ajustes, como insignias y tu progreso en una herramienta educativa, en el almacenamiento local del navegador. Se quedan en tu dispositivo.',
   up='Última actualización: 16 de octubre de 2026'),
 'ar': dict(h='التحليلات (Cloudflare Web Analytics)', p=[
   'نحسب الزيارات باستخدام Cloudflare Web Analytics، وهي لا تضع ملفات تعريف ارتباط ولا تستخدم التخزين المحلي، ولا تنشئ ملفًا شخصيًا عنك ولا تتبعك عبر المواقع. لا نرى إلا الأعداد الإجمالية مثل مشاهدات الصفحات والمواقع المُحيلة والبلدان وأنواع المتصفحات.',
   'توقفنا عن استخدام Google Analytics في 16 أكتوبر 2026، لذلك لا يوجد شريط موافقة: لا شيء في هذا الموقع يضع ملف تعريف ارتباط للتتبع.'],
   kid='التحليلات في كل الصفحات، بما فيها صفحات الأطفال، بلا ملفات تعريف ارتباط وتحسب الأعداد الإجمالية فقط. تُنشأ خطط الدروس في متصفحك ولا تُرسل إلينا.',
   st='نحفظ إعدادات صغيرة، مثل الشارات والتقدّم في أداة تعليمية، في التخزين المحلي لمتصفحك، وتبقى على جهازك.',
   up='آخر تحديث: 16 أكتوبر 2026'),
 'it': dict(h='Statistiche (Cloudflare Web Analytics)', p=[
   'Contiamo le visite con Cloudflare Web Analytics. Non usa cookie né archiviazione locale, e non crea un tuo profilo né ti segue da un sito all’altro. Vediamo solo totali come pagine viste, siti di provenienza, paesi e tipi di browser.',
   'Abbiamo smesso di usare Google Analytics il 16 ottobre 2026, quindi non c’è un banner di consenso: niente su questo sito imposta cookie di tracciamento.'],
   kid='Su tutte le pagine, comprese quelle per bambini, le statistiche sono senza cookie e contano solo totali. I piani di lezione vengono creati nel tuo browser e non ci vengono inviati.',
   st='Salviamo piccole impostazioni, come badge e progressi in uno strumento didattico, nell’archiviazione locale del browser. Restano sul tuo dispositivo.',
   up='Ultimo aggiornamento: 16 ottobre 2026'),
}
EXTRA = {}  # lang -> extra <p> appended to the analytics section (filled by build-events text, Oct 16)
try:
    import sys; sys.path.insert(0, str(ROOT / 'scripts')); import events_text as _EV; EXTRA = _EV.PRIV_P
except Exception: pass

def privacy(p, l):
    s = p.read_text(encoding='utf-8'); t = PRIV[l]
    paras = ''.join(f'<p>{E(x)}</p>' for x in t['p'] + ([EXTRA[l]] if l in EXTRA else []))
    s = re.sub(r'(<section class="five-ws" id="s2">).*?(</section>)', lambda m: f'{m.group(1)}<h2>{E(t["h"])}</h2>{paras}{m.group(2)}', s, count=1, flags=re.S)
    def kid(m):
        sec = m.group(0); i = sec.rfind('<p>')
        return sec[:i] + f'<p>{E(t["kid"])}</p></section>' if i > 0 else sec
    s = re.sub(r'<section class="five-ws" id="s4">.*?</section>', kid, s, count=1, flags=re.S)
    s = re.sub(r'(<section class="five-ws" id="s5"><h2>[^<]*</h2>).*?(</section>)', lambda m: f'{m.group(1)}<p>{E(t["st"])}</p>{m.group(2)}', s, count=1, flags=re.S)
    try: rp = _EV.REPORT_P[l]
    except Exception: rp = ''
    s = re.sub(r'<p class="rf-priv">.*?</p>', '', s, flags=re.S)
    if rp: s = re.sub(r'(<section class="five-ws" id="s6">.*?)(</section>)', lambda m: m.group(1) + f'<p class="rf-priv">{E(rp)}</p>' + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<p class="trust-updated">[^<]*</p>', f'<p class="trust-updated">{E(t["up"])}</p>', s, count=1)
    return s

ABOUT = {'en': 'We count visits with Cloudflare Web Analytics, which sets no cookies and keeps no personal profile. There is no consent banner because nothing needs one. Details: Privacy.',
 'fr': 'Nous comptons les visites avec Cloudflare Web Analytics, qui ne dépose aucun cookie et ne garde aucun profil personnel. Il n’y a pas de bandeau de consentement, car rien n’en a besoin. Détails : Confidentialité.',
 'es': 'Contamos las visitas con Cloudflare Web Analytics, que no usa cookies ni guarda perfiles personales. No hay aviso de consentimiento porque nada lo necesita. Detalles: Privacidad.',
 'ar': 'نحسب الزيارات باستخدام Cloudflare Web Analytics، وهي لا تضع ملفات تعريف ارتباط ولا تحتفظ بملف شخصي. لا يوجد شريط موافقة لأنه لا حاجة إليه. التفاصيل: الخصوصية.',
 'it': 'Contiamo le visite con Cloudflare Web Analytics, che non usa cookie e non conserva profili personali. Non c’è un banner di consenso perché non serve. Dettagli: Privacy.'}
GA_P = re.compile(r'<p>(?:(?!</p>).)*Google Analytics(?:(?!</p>).)*</p>', re.S)
n = 0
for p in ROOT.rglob('*.html'):
    rel = p.relative_to(ROOT).parts
    if '.git' in rel or 'pagefind' in rel or 'node_modules' in rel or p.name in SKIP: continue
    s = p.read_text(encoding='utf-8'); t = GA.sub('', s); t = CONSENT.sub('', t); t = CFW.sub('', t)
    t = re.sub(r'search-ui\.js\?v=[\w.-]+', 'search-ui.js?v=20261016g', t)  # Oct 16: GA search events removed
    if '</body>' in t: t = t.replace('</body>', BEACON + '</body>', 1)
    if p.name == 'About.html':
        la = rel[0] if len(rel) == 2 else 'en'
        if la in ABOUT: t = GA_P.sub(lambda m: '<p>' + E(ABOUT[la]) + '</p>', t, count=1)
    if p.name == 'Privacy.html':
        l = rel[0] if len(rel) == 2 and rel[0] in ('fr', 'es', 'ar', 'it') else 'en' if len(rel) == 1 else None
        if l:
            p.write_text(t, encoding='utf-8'); t = privacy(p, l)
    if t != s: p.write_text(t, encoding='utf-8'); n += 1
print(f'build-analytics: {n} pages updated')
