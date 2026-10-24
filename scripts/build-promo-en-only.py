#!/usr/bin/env python3
"""Oct 21 (founder): promo videos are English-only until traffic grows.
On fr/es/ar/it/he every promo video section (homepage + About) becomes one 4K-class
NASA photo from R2 (Bahamas from the ISS, 8256x5504) with alt text in that language.
English is untouched. Idempotent; runs after i18n-build and before build-critical."""
import glob, html, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import media as MEDIA
IMG = MEDIA.M['images/Bahamas_Atlantic_ISS071_449837.jpg']
URL, W, H = IMG['url'], IMG['width'], IMG['height']
T = {
 'fr': ("Les eaux turquoise des Bahamas et l'Atlantique vus depuis la Station spatiale internationale", "Une seule planète, des solutions réelles : océans, lacs, rivières, forêts et espace.", "Photo : NASA"),
 'es': ("Las aguas turquesa de las Bahamas y el Atlántico vistos desde la Estación Espacial Internacional", "Un solo planeta, soluciones reales: océanos, lagos, ríos, bosques y espacio.", "Foto: NASA"),
 'ar': ("مياه جزر البهاما الفيروزية والمحيط الأطلسي كما تُرى من محطة الفضاء الدولية", "كوكب واحد وحلول حقيقية: المحيطات والبحيرات والأنهار والغابات والفضاء.", "الصورة: ناسا"),
 'it': ("Le acque turchesi delle Bahamas e l'Atlantico visti dalla Stazione Spaziale Internazionale", "Un solo pianeta, soluzioni reali: oceani, laghi, fiumi, foreste e spazio.", "Foto: NASA"),
 'he': ("המים הטורקיז של איי בהאמה והאוקיינוס האטלנטי כפי שנראים מתחנת החלל הבינלאומית", "כוכב לכת אחד, פתרונות אמיתיים: אוקיינוסים, אגמים, נהרות, יערות וחלל.", "צילום: נאס\"א"),
}
SEC = re.compile(r'<section[^>]*class="[^"]*\bsp-promo\b[^"]*"[^>]*>.*?</section>', re.S)
LD = re.compile(r'<script type="application/ld\+json" id="sp-video-ld">[^<]*savingplanets-promo[^<]*</script>\s*')
n = 0
for lang, (alt, cap, cred) in T.items():
    d = 'rtl' if lang in ('ar', 'he') else 'ltr'
    for f in glob.glob(f'{lang}/*.html'):
        s = open(f, encoding='utf-8').read()
        if 'sp-promo' not in s and 'savingplanets-promo' not in s: continue
        def rep(m):
            about = 'sp-promo-about' in m.group(0)
            return (f'<section class="sp-promo-still{" sp-promo-about" if about else ""}" dir="{d}" aria-label="{html.escape(cap)}">'
                    f'<figure><img src="{URL}" width="{W}" height="{H}" alt="{html.escape(alt)}" loading="lazy" decoding="async">'
                    f'<figcaption>{html.escape(cap, quote=False)} <span class="photo-credit">{html.escape(cred, quote=False)}</span></figcaption></figure></section>')
        s2 = LD.sub('', SEC.sub(rep, s))
        if 'savingplanets-promo' not in s2 and '<video' not in s2.split('<!-- VIDEO:START -->')[-1].split('<!-- VIDEO:END -->')[0]:
            s2 = re.sub(r'<!-- VIDEO:(?:START|END) -->\n?', '', s2)  # Oct 23: the still is not a video; orphan markers made seo-lint expect a VideoObject
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); n += 1
print(f'build-promo-en-only: {n} translated pages now use the still image (English keeps the video)')
