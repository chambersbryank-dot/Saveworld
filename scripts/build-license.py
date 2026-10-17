#!/usr/bin/env python3
"""Oct 16 2026 (user-approved): license original site content under CC BY-NC 4.0.
- Footer line on every page (5 languages) with rel="license" link (LICENSE block, just before </footer>).
- <link rel="license"> in <head> of every page.
- JSON-LD: "license" added to page-level objects (WebPage-type, Article, LearningResource, Course, Dataset, WebSite).
  Not added to ImageObject/VideoObject/MediaObject: third-party media keep their own licences.
- About page: 'Use & licence' section (#licence) before the Privacy section (LICABOUT block).
Idempotent. Runs last-ish in weekly-sync.sh (after footer/schema generators). i18n hashes ignore these blocks."""
import re, glob, json, html
LIC = 'https://creativecommons.org/licenses/by-nc/4.0/'
DEED = {'en': 'deed.en', 'fr': 'deed.fr', 'es': 'deed.es', 'ar': 'deed.ar', 'it': 'deed.it'}
FOOT = {
 'en': ('Original text, lessons and labs: © Saving Planets, licensed {cc}. Images and media keep their own credits and licences.', 'Use &amp; licence'),
 'fr': ('Textes, leçons et labos originaux : © Saving Planets, sous licence {cc}. Les images et médias conservent leurs propres crédits et licences.', 'Utilisation et licence'),
 'es': ('Textos, lecciones y laboratorios originales: © Saving Planets, con licencia {cc}. Las imágenes y medios conservan sus propios créditos y licencias.', 'Uso y licencia'),
 'ar': ('النصوص والدروس والمختبرات الأصلية: © Saving Planets، مرخّصة بموجب {cc}. تحتفظ الصور والوسائط بنسبها وتراخيصها الخاصة.', 'الاستخدام والترخيص'),
 'it': ('Testi, lezioni e laboratori originali: © Saving Planets, con licenza {cc}. Immagini e media mantengono i propri crediti e licenze.', 'Uso e licenza'),
}
ABOUT = {
 'en': ('Use &amp; Licence', [
   'Original Saving Planets text, lessons and labs are licensed under {cc}. You may copy, share and adapt them for non-commercial purposes, such as classrooms, clubs and homeschooling, as long as you credit “Saving Planets (savingplanets.com)”, link to the licence and say if you made changes.',
   'Third-party images and media (for example from NASA, ESA or Pexels) are not covered by this licence. They keep their own credits and licences, shown next to each item; please follow those terms.',
   'Images and videos made with SI keep the credit “Created by SI and Biological SI Partner”.',
   'For commercial use, write to <a href="mailto:media@savingplanets.com?subject=Media%20inquiry">media@savingplanets.com</a>.']),
 'fr': ('Utilisation et licence', [
   'Les textes, leçons et labos originaux de Saving Planets sont sous licence {cc}. Vous pouvez les copier, les partager et les adapter à des fins non commerciales, par exemple en classe, en club ou à la maison, à condition de créditer « Saving Planets (savingplanets.com) », d’indiquer un lien vers la licence et de signaler vos modifications.',
   'Les images et médias de tiers (par exemple de la NASA, de l’ESA ou de Pexels) ne sont pas couverts par cette licence. Ils conservent leurs propres crédits et licences, indiqués à côté de chaque élément ; merci d’en respecter les conditions.',
   'Les images et vidéos créées avec la SI conservent le crédit « Created by SI and Biological SI Partner ».',
   'Pour un usage commercial, écrivez à <a href="mailto:media@savingplanets.com?subject=Media%20inquiry">media@savingplanets.com</a>.']),
 'es': ('Uso y licencia', [
   'Los textos, lecciones y laboratorios originales de Saving Planets tienen licencia {cc}. Puedes copiarlos, compartirlos y adaptarlos con fines no comerciales, como en clase, clubes o educación en casa, siempre que cites «Saving Planets (savingplanets.com)», enlaces la licencia e indiques si hiciste cambios.',
   'Las imágenes y medios de terceros (por ejemplo de la NASA, la ESA o Pexels) no están cubiertos por esta licencia. Conservan sus propios créditos y licencias, indicados junto a cada elemento; respeta esas condiciones.',
   'Las imágenes y videos hechos con SI conservan el crédito «Created by SI and Biological SI Partner».',
   'Para uso comercial, escribe a <a href="mailto:media@savingplanets.com?subject=Media%20inquiry">media@savingplanets.com</a>.']),
 'ar': ('الاستخدام والترخيص', [
   'النصوص والدروس والمختبرات الأصلية في Saving Planets مرخّصة بموجب {cc}. يمكنك نسخها ومشاركتها وتعديلها لأغراض غير تجارية، مثل الفصول الدراسية والنوادي والتعليم المنزلي، بشرط نسبتها إلى «Saving Planets (savingplanets.com)» ووضع رابط للترخيص وذكر أي تغييرات أجريتها.',
   'لا يشمل هذا الترخيص الصور والوسائط التابعة لجهات أخرى (مثل NASA أو ESA أو Pexels)، فهي تحتفظ بنسبها وتراخيصها الخاصة المذكورة بجانب كل عنصر؛ يُرجى الالتزام بشروطها.',
   'تحتفظ الصور ومقاطع الفيديو المصنوعة بمساعدة SI بعبارة النسب «Created by SI and Biological SI Partner».',
   'للاستخدام التجاري، راسلنا على <a href="mailto:media@savingplanets.com?subject=Media%20inquiry">media@savingplanets.com</a>.']),
 'it': ('Uso e licenza', [
   'I testi, le lezioni e i laboratori originali di Saving Planets sono distribuiti con licenza {cc}. Puoi copiarli, condividerli e adattarli per scopi non commerciali, ad esempio in classe, nei club o nell’istruzione parentale, citando «Saving Planets (savingplanets.com)», inserendo un link alla licenza e indicando eventuali modifiche.',
   'Immagini e media di terzi (ad esempio NASA, ESA o Pexels) non sono coperti da questa licenza. Mantengono i propri crediti e licenze, indicati accanto a ciascun elemento; rispetta quelle condizioni.',
   'Immagini e video realizzati con la SI mantengono il credito «Created by SI and Biological SI Partner».',
   'Per usi commerciali scrivi a <a href="mailto:media@savingplanets.com?subject=Media%20inquiry">media@savingplanets.com</a>.']),
}
PAGE_TYPES = {'WebPage', 'AboutPage', 'CollectionPage', 'ContactPage', 'FAQPage', 'ItemPage', 'Article', 'NewsArticle', 'BlogPosting',
              'TechArticle', 'LearningResource', 'Course', 'Quiz', 'Dataset', 'WebSite', 'HowTo'}
def cc(l, rel=True):
    r = 'rel="license" ' if rel else ''
    return f'<a {r}href="{LIC}{DEED[l]}" lang="en" dir="ltr">CC BY-NC 4.0</a>'
def add_lic(o):
    ch = False
    if isinstance(o, list):
        for x in o: ch |= add_lic(x)
    elif isinstance(o, dict):
        t = o.get('@type'); ts = set(t if isinstance(t, list) else [t])
        if ts & PAGE_TYPES and o.get('license') != LIC: o['license'] = LIC; ch = True
        if '@graph' in o: ch |= add_lic(o['@graph'])
    return ch
def ld(s):
    def fix(m):
        try: obj = json.loads(m.group(2))
        except Exception: return m.group(0)
        return m.group(1) + json.dumps(obj, ensure_ascii=False) + m.group(3) if add_lic(obj) else m.group(0)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, s, flags=re.S)
def main():
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in FOOT: continue
        s = open(f, encoding='utf8').read(); s2 = s; pre = '' if l == 'en' else '../'
        if '</head>' in s2 and 'rel="license" href="' + LIC + '"' not in s2.split('</head>')[0]:
            s2 = s2.replace('</head>', f'<link rel="license" href="{LIC}">\n</head>', 1)
        s2 = re.sub(r'<!-- LICENSE:START -->.*?<!-- LICENSE:END -->', '', s2, flags=re.S)
        if '</footer>' in s2:
            t, more = FOOT[l]
            blk = f'<!-- LICENSE:START --><style>footer .lic-foot{{font-size:.85rem;opacity:.9}}footer .lic-foot a{{display:inline!important;margin:0!important;padding:0!important;min-height:0!important;width:auto!important}}</style><p class="lic-foot">{t.format(cc=cc(l))} <a href="{pre}About.html#licence">{more}</a></p><!-- LICENSE:END -->'
            s2 = s2.replace('</footer>', blk + '</footer>', 1)
        s2 = ld(s2)
        if f.endswith('About.html'):
            h, ps = ABOUT[l]
            s2 = re.sub(r'<!-- LICABOUT:START -->.*?<!-- LICABOUT:END -->', '', s2, flags=re.S)
            sec = (f'<!-- LICABOUT:START --><section class="five-ws" id="licence"><h2>{h}</h2>' +
                   ''.join(f'<p>{p.format(cc=cc(l, False))}</p>' for p in ps) + '</section><!-- LICABOUT:END -->')
            assert '<section class="five-ws" id="privacy">' in s2, f
            s2 = s2.replace('<section class="five-ws" id="privacy">', sec + '<section class="five-ws" id="privacy">', 1)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-license: {n} pages')
if __name__ == '__main__': main()
