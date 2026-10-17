#!/usr/bin/env python3
"""Oct 16 2026: Embed buttons + ?embed=1 minimal-chrome mode (5 languages).
- EMBED block (after the page's main content): dt-bar style "Embed" button with a prefilled, responsive iframe snippet that
  carries attribution + the CC BY-NC 4.0 note; Copy fires one privacy-safe event (share/embed). assets/embed.js.
- EMBEDMODE block (in <head> + end of <body>): with ?embed=1 the page hides nav, footer, share/newsletter/help chrome, opens
  links in a new tab, and shows a small attribution bar. &only=<id> keeps just one section (Artemis_II.html#launches).
  GitHub Pages sends no X-Frame-Options or CSP frame-ancestors, so any site may frame these pages.
Pages: the 11 calculators, Orbit/Aero/Physics labs, Artemis_II launch tracker. Run after build-calcs.py / build-learn.py. Idempotent."""
import re, os, glob, html, sys
sys.path.insert(0, 'scripts')
import calc_text as CT
SITE = 'https://www.savingplanets.com/'; LANGS = ['en', 'fr', 'es', 'ar', 'it']; V = '20261016e'
E = lambda x: html.escape(x, quote=True)
U = {'en': dict(h='Embed', b='Embed this', copy='Copy code', ok='Code copied', note='Free for non-commercial use (CC BY-NC 4.0). Keep the attribution line under the frame.', by='by Saving Planets', open='Open full page', lic='CC BY-NC 4.0'),
     'fr': dict(h='Intégrer', b='Intégrer cet outil', copy='Copier le code', ok='Code copié', note='Libre pour un usage non commercial (CC BY-NC 4.0). Gardez la ligne d’attribution sous le cadre.', by='par Saving Planets', open='Ouvrir la page complète', lic='CC BY-NC 4.0'),
     'es': dict(h='Insertar', b='Insertar esta herramienta', copy='Copiar código', ok='Código copiado', note='Libre para uso no comercial (CC BY-NC 4.0). Mantén la línea de atribución bajo el marco.', by='por Saving Planets', open='Abrir la página completa', lic='CC BY-NC 4.0'),
     'ar': dict(h='تضمين', b='تضمين هذه الأداة', copy='نسخ الرمز', ok='تم نسخ الرمز', note='مجاني للاستخدام غير التجاري (CC BY-NC 4.0). أبقِ سطر الإسناد أسفل الإطار.', by='من Saving Planets', open='افتح الصفحة كاملة', lic='CC BY-NC 4.0'),
     'it': dict(h='Incorpora', b='Incorpora questo strumento', copy='Copia codice', ok='Codice copiato', note='Libero per uso non commerciale (CC BY-NC 4.0). Mantieni la riga di attribuzione sotto il riquadro.', by='di Saving Planets', open='Apri la pagina completa', lic='CC BY-NC 4.0')}
PAGES = {c['page']: ('calc', None, 760) for c in CT.C}
PAGES.update({'Orbit_Lab.html': ('lab', None, 900), 'Aero_Lab.html': ('lab', None, 900), 'Physics_Lab.html': ('lab', None, 900), 'Artemis_II.html': ('launches', 'launches', 720)})
MODE_HEAD = ('<!-- EMBEDMODE:START --><script>(function(){var q=location.search;if(!/[?&]embed=1(&|$)/.test(q))return;var d=document.documentElement;d.classList.add("sp-embed");'
             'var o=(q.match(/[?&]only=([A-Za-z0-9_-]{1,40})/)||[])[1];var b=document.createElement("base");b.target="_blank";document.head.appendChild(b);'
             'document.addEventListener("DOMContentLoaded",function(){var a=document.querySelector(".emb-attr");if(a)a.hidden=false;if(!o)return;var e=document.getElementById(o);if(!e)return;'
             'for(var n=e;n&&n.parentElement&&n.tagName!=="BODY";n=n.parentElement){[].forEach.call(n.parentElement.children,function(s){if(s!==n&&s.tagName!=="SCRIPT"&&s.tagName!=="STYLE"&&!s.classList.contains("emb-attr"))s.style.display="none"})}})})();</script>'
             '<style>.sp-embed #topnav,.sp-embed .skip-link,.sp-embed footer,.sp-embed .shr,.sp-embed .share-bar,.sp-embed .nl-call,.sp-embed .emb-bar,.sp-embed .dt-bar,.sp-embed .sticky-help,.sp-embed .gu-link,.sp-embed .lw-toc,.sp-embed [data-sp-newsletter]{display:none!important}'
             '.sp-embed body{padding-top:0!important;margin-top:0!important}html.sp-embed body[class] .page-hero.page-hero[class],html.sp-embed body .page-hero .page-hero-content{min-height:0!important;height:auto!important;padding:.6rem 1rem!important;margin:0!important}html.sp-embed body[class] .page-hero.page-hero[class]{background:#0b1620!important}.sp-embed .page-hero video,.sp-embed .page-hero img,.sp-embed .page-hero::before,.sp-embed .page-hero::after{display:none!important}.sp-embed .page-hero h1{font-size:1.5rem!important}'
             '.emb-attr{position:sticky;bottom:0;z-index:50;margin:0;padding:6px 12px;font:600 13px/1.6 system-ui,sans-serif;background:#0b1620;color:#e8eef5;border-top:1px solid #2b4a5e;text-align:center}.emb-attr a{color:#8fd3ff}</style><!-- EMBEDMODE:END -->')
def strip(s, k): return re.sub(rf'<!-- {k}:START -->.*?<!-- {k}:END -->', '', s, flags=re.S)
def title_of(s): m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S); return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else 'Saving Planets'
def main():
    n = 0
    for l in LANGS:
        d = '' if l == 'en' else l + '/'; u = U[l]; pre = '' if l == 'en' else '../'
        for p, (kind, only, ht) in PAGES.items():
            f = d + p
            if not os.path.exists(f): continue
            s = open(f, encoding='utf8').read(); s2 = s
            for k in ('EMBED', 'EMBEDMODE'): s2 = strip(s2, k)
            url = SITE + d + p; t = title_of(s2)
            src = url + '?embed=1' + (f'&only={only}' if only else '')
            snip = (f'<iframe src="{E(src)}" title="{E(t)}" width="100%" height="{ht}" style="border:0;max-width:100%;display:block" loading="lazy"></iframe>\n'
                    f'<p style="font-size:13px"><a href="{E(url + ("#" + only if only else ""))}">{E(t)}</a> {E(u["by"])}, <a href="https://creativecommons.org/licenses/by-nc/4.0/">{u["lic"]}</a></p>')
            bar = (f'<!-- EMBED:START --><section class="dt-bar emb-bar" data-pagefind-ignore="all" aria-label="{E(u["b"])}" data-page="{kind}"><h2>{E(u["h"])}</h2>'
                   f'<button type="button" class="dt-btn" data-emb="show" aria-expanded="false">&lt;/&gt; {E(u["b"])}</button>'
                   f'<div class="dt-out" hidden><textarea readonly dir="ltr" aria-label="{E(u["b"])}">{E(snip)}</textarea><button type="button" class="dt-btn" data-emb="copy" data-ok="{E(u["ok"])}">{E(u["copy"])}</button> <span class="emb-st" role="status" aria-live="polite"></span></div>'
                   f'<p class="dt-note">{E(u["note"])}</p></section><script src="{pre}assets/embed.js?v={V}" defer></script><!-- EMBED:END -->')
            if only:  # put the bar at the end of the launches section
                m = re.search(rf'<section[^>]*id="{only}"', s2); end = s2.find('</section>', m.end()) if m else -1
                # launch widget may contain nested sections: find matching close
                if m:
                    depth, i = 0, m.start()
                    for mm in re.finditer(r'<section\b|</section>', s2[m.start():]):
                        depth += 1 if mm.group(0) == '<section' else -1
                        if depth == 0: end = m.start() + mm.start(); break
                    s2 = s2[:end] + bar + s2[end:]
            else:
                s2 = s2.replace('</main>', bar + '</main>', 1)
            attr = (f'<!-- EMBEDMODE:START --><p class="emb-attr" hidden><a href="{E(url)}" target="_blank" rel="noopener">Saving Planets</a> · '
                    f'<a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener license">{u["lic"]}</a> · <a href="{E(url)}" target="_blank" rel="noopener">{E(u["open"])}</a></p><!-- EMBEDMODE:END -->')
            s2 = s2.replace('</head>', MODE_HEAD + '</head>', 1).replace('</body>', attr + '</body>', 1)
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-embed: {n} pages')
if __name__ == '__main__': main()
