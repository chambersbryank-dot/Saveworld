#!/usr/bin/env python3
"""Oct 15: warm invitation link in every page footer (all 6 languages), right after the footer's Corrections link.
Oct 16: the link now opens the on-site form (Corrections.html?page=<this page>#report) instead of a GitHub issue (GitHub needs
an account and is 13+). The form (REPORTFORM block on each language's Corrections page) posts to the si-helper Worker /report,
which emails media@savingplanets.com: no name/email fields, emails/phone numbers refused, Turnstile, rate limits, nothing stored.
Adults can still use GitHub: one small line on the Corrections page only. Idempotent. Run late in weekly-sync.sh."""
import re, glob, os, urllib.parse, json, html
SITE = 'https://www.savingplanets.com/'; REPO = 'https://github.com/chambersbryank-dot/Saveworld/issues/new?template=correction.yml'
ENDPOINT = 'https://si-helper.chambersbryank.workers.dev/report'; SITEKEY = '0x4AAAAAAFY9fV0YboAn4sqm'; V = '20261027w'
L = {
 'en': 'Saving Planets would love your native-language fixes to our site!',
 'fr': 'Saving Planets serait ravi de vos corrections dans votre langue !',
 'es': '¡A Saving Planets le encantarían tus correcciones en tu idioma!',
 'ar': 'يسعد Saving Planets بتصحيحاتكم بلغتكم الأم!',
 'it': 'Saving Planets sarebbe felice delle vostre correzioni nella vostra lingua!',
 'he': 'Saving Planets ישמח לתיקונים שלכם בשפת האם!',
}
F = {
 'en': dict(h='Saving Planets would love your native-language fixes to our site!', intro='Tell us what is wrong — a translation wording or a fact — and we will fix it in every language. Any language is fine.', page='Page', what='What is wrong?', fix='Suggested fix or source (optional)',
   note='Please don’t type names, emails or phone numbers. We can’t reply, and nothing you send is stored on this site.', send='Send report', wait='Sending…',
   ok='Thank you! Your report was sent.', pii='Please remove emails or phone numbers and try again.', short='Please describe the problem in a few more words.',
   bot='Couldn’t confirm you are a person. Reload the page and try again.', busy='Too many reports right now. Please try again later.', error='Something went wrong. Please try again.', neterr='No connection. Please try again.',
   gh='Adults with a GitHub account can also open a public issue on GitHub.'),
 'fr': dict(h='Saving Planets serait ravi de vos corrections dans votre langue !', intro='Dites-nous ce qui ne va pas et nous le corrigerons dans toutes les langues. Toute langue convient.', page='Page', what='Qu’est-ce qui ne va pas ?', fix='Correction proposée ou source (facultatif)',
   note='Merci de ne saisir ni nom, ni e-mail, ni numéro de téléphone. Nous ne pouvons pas répondre et rien de ce que vous envoyez n’est conservé sur ce site.', send='Envoyer', wait='Envoi…',
   ok='Merci ! Votre signalement a été envoyé.', pii='Retirez les e-mails ou numéros de téléphone, puis réessayez.', short='Décrivez le problème en quelques mots de plus.',
   bot='Impossible de confirmer que vous êtes une personne. Rechargez la page et réessayez.', busy='Trop de signalements pour le moment. Réessayez plus tard.', error='Une erreur s’est produite. Réessayez.', neterr='Pas de connexion. Réessayez.',
   gh='Les adultes ayant un compte GitHub peuvent aussi ouvrir un ticket public sur GitHub.'),
 'es': dict(h='¡A Saving Planets le encantarían tus correcciones en tu idioma!', intro='Cuéntanos qué está mal y lo corregiremos en todos los idiomas. Cualquier idioma sirve.', page='Página', what='¿Qué está mal?', fix='Corrección sugerida o fuente (opcional)',
   note='No escribas nombres, correos ni teléfonos. No podemos responder y nada de lo que envíes se guarda en este sitio.', send='Enviar', wait='Enviando…',
   ok='¡Gracias! Tu aviso se ha enviado.', pii='Quita los correos o teléfonos e inténtalo de nuevo.', short='Describe el problema con unas palabras más.',
   bot='No se pudo confirmar que eres una persona. Recarga la página e inténtalo de nuevo.', busy='Demasiados avisos ahora mismo. Inténtalo más tarde.', error='Algo salió mal. Inténtalo de nuevo.', neterr='Sin conexión. Inténtalo de nuevo.',
   gh='Los adultos con cuenta de GitHub también pueden abrir una incidencia pública en GitHub.'),
 'ar': dict(h='يسعد Saving Planets بتصحيحاتكم بلغتكم الأم!', intro='أخبرنا بما هو خطأ وسنصححه في كل اللغات. يمكنك الكتابة بأي لغة.', page='الصفحة', what='ما الخطأ؟', fix='التصحيح المقترح أو المصدر (اختياري)',
   note='يُرجى عدم كتابة أسماء أو عناوين بريد إلكتروني أو أرقام هواتف. لا يمكننا الرد، ولا يُحفظ أي شيء ترسله على هذا الموقع.', send='إرسال البلاغ', wait='جارٍ الإرسال…',
   ok='شكرًا لك! أُرسل بلاغك.', pii='يُرجى حذف عناوين البريد أو أرقام الهواتف والمحاولة مجددًا.', short='يُرجى وصف المشكلة ببضع كلمات إضافية.',
   bot='تعذّر التأكد من أنك شخص. أعد تحميل الصفحة وحاول مجددًا.', busy='بلاغات كثيرة الآن. يُرجى المحاولة لاحقًا.', error='حدث خطأ ما. يُرجى المحاولة مجددًا.', neterr='لا يوجد اتصال. يُرجى المحاولة مجددًا.',
   gh='يمكن للبالغين الذين لديهم حساب على GitHub فتح بلاغ عام على GitHub أيضًا.'),
 'it': dict(h='Saving Planets sarebbe felice delle vostre correzioni nella vostra lingua!', intro='Dicci cosa non va e lo correggeremo in tutte le lingue. Va bene qualsiasi lingua.', page='Pagina', what='Cosa non va?', fix='Correzione suggerita o fonte (facoltativo)',
   note='Non scrivere nomi, email o numeri di telefono. Non possiamo rispondere e nulla di ciò che invii viene conservato su questo sito.', send='Invia segnalazione', wait='Invio…',
   ok='Grazie! La segnalazione è stata inviata.', pii='Togli email o numeri di telefono e riprova.', short='Descrivi il problema con qualche parola in più.',
   bot='Impossibile confermare che sei una persona. Ricarica la pagina e riprova.', busy='Troppe segnalazioni in questo momento. Riprova più tardi.', error='Qualcosa è andato storto. Riprova.', neterr='Nessuna connessione. Riprova.',
   gh='Gli adulti con un account GitHub possono anche aprire una segnalazione pubblica su GitHub.'),
 'he': dict(h='Saving Planets ישמח לתיקונים שלכם בשפת האם!', intro='ספרו לנו מה לא בסדר — ניסוח בתרגום או עובדה — ונתקן בכל השפות. כל שפה בסדר.', page='דף', what='מה לא בסדר?', fix='תיקון מוצע או מקור (רשות)',
   note='בבקשה אל תכתבו שמות, כתובות דוא״ל או מספרי טלפון. אנחנו לא יכולים להשיב, ושום דבר שתשלחו לא נשמר באתר.', send='שלחו דיווח', wait='שולחים…',
   ok='תודה! הדיווח נשלח.', pii='הסירו כתובות דוא״ל או מספרי טלפון ונסו שוב.', short='תארו את הבעיה בעוד כמה מילים.',
   bot='לא הצלחנו לוודא שאתם אדם. רעננו את הדף ונסו שוב.', busy='יותר מדי דיווחים כרגע. נסו שוב מאוחר יותר.', error='משהו השתבש. נסו שוב.', neterr='אין חיבור. נסו שוב.',
   gh='מבוגרים עם חשבון GitHub יכולים גם לפתוח דיווח ציבורי ב-GitHub.'),
}
CSS = ('<style>.rf{max-width:760px;margin:1.5rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(0,156,222,.45);border-radius:14px;background:rgba(15,27,38,.6)}'
       '.rf label{display:block;font-weight:600;margin:.8rem 0 .3rem}.rf input,.rf textarea{width:100%;box-sizing:border-box;font:inherit;font-size:1rem;padding:.6rem .7rem;border-radius:8px;border:1px solid #7aa7c2;background:#0b1620;color:#e8eef5}'
       '.rf textarea{min-height:7rem;resize:vertical}.rf .rf-note{font-size:.9rem;opacity:.9}.rf button{min-height:44px;min-width:44px;margin-top:.9rem;padding:.6rem 1.4rem;border:0;border-radius:999px;background:#009cde;color:#fff;font-weight:700;font-size:1rem;cursor:pointer}'
       '.rf button:disabled{opacity:.6}.rf input:focus-visible,.rf textarea:focus-visible,.rf button:focus-visible{outline:2px solid #8fd3ff;outline-offset:2px}.rf-out{min-height:1.4em;margin:.7rem 0 0;font-weight:600}.rf-ok{color:#7ee2a8}.rf-err{color:#ffb4a9}.rf-gh{font-size:.85rem;opacity:.85}</style>')
def form(l, pre):
    t = F[l]; e = lambda s: html.escape(s, quote=True)
    js = e(json.dumps({k: t[k] for k in ('wait', 'ok', 'pii', 'short', 'bot', 'busy', 'error', 'neterr')}, ensure_ascii=False))
    return (CSS + f'<section class="rf" id="report" aria-labelledby="rf-h"><h2 id="rf-h">{e(t["h"])}</h2><p>{e(t["intro"])}</p>'
            f'<form class="rf-form" novalidate data-endpoint="{ENDPOINT}" data-sitekey="{SITEKEY}" data-lang="{l}" data-t="{js}">'
            f'<label for="rf-page">{e(t["page"])}</label><input id="rf-page" name="page" type="url" dir="ltr" maxlength="200" inputmode="url" autocomplete="off" placeholder="https://www.savingplanets.com/…">'
            f'<label for="rf-what">{e(t["what"])}</label><textarea id="rf-what" name="what" required maxlength="1500" dir="auto" autocomplete="off" aria-describedby="rf-note"></textarea>'
            f'<label for="rf-fix">{e(t["fix"])}</label><textarea id="rf-fix" name="fix" maxlength="1500" dir="auto" autocomplete="off"></textarea>'
            f'<p class="rf-note" id="rf-note">{e(t["note"])}</p><div class="rf-ts"></div><button type="submit">{e(t["send"])}</button>'
            f'<p class="rf-out" role="status" aria-live="polite"></p></form>'
            f'<p class="rf-gh"><a href="{REPO.replace("&", "&amp;")}" rel="noopener" target="_blank">{e(t["gh"])}</a></p></section>'
            f'<script src="{pre}assets/report-form.js?v={V}" defer></script>')
def main():
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in L: continue
        s = open(f, encoding='utf8').read(); s2 = s
        if '<footer' in s:
            s2 = re.sub(r'<li class="fm-report">.*?</li>', '', s2)
            url = SITE + ('' if l == 'en' else l + '/') + os.path.basename(f)
            li = f'<li class="fm-report"><a href="Corrections.html?page={urllib.parse.quote(url, safe="")}#report">{L[l]}</a></li>'
            m = re.search(r'<li><a href="(?:\.\./)?Corrections\.html">[^<]*</a></li>', s2)
            if m: s2 = s2[:m.end()] + li + s2[m.end():]
            elif '<!-- FOOTER-MAP:END -->' in s2: s2 = s2.replace('</ul></div></div><!-- FOOTER-MAP:END -->', li + '</ul></div></div><!-- FOOTER-MAP:END -->', 1)
        if os.path.basename(f) == 'Corrections.html':
            blk = '<!-- REPORTFORM:START -->' + form(l, '' if l == 'en' else '../') + '<!-- REPORTFORM:END -->'
            s2 = re.sub(r'<!-- REPORTFORM:START -->.*?<!-- REPORTFORM:END -->', '', s2, flags=re.S)
            s2 = s2.replace('<section class="five-ws" id="s2">', blk + '<section class="five-ws" id="s2">', 1)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-report-link: {n} pages')
if __name__ == '__main__': main()
