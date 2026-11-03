#!/usr/bin/env python3
"""Nov 2 2026 (Bryan): cross-site promotion. Ways_to_Help (all 6 langs) gets a block after WTH-ALL:END with the combined
donate/volunteer count across savingplanets.com + beforesavingplanets.com, and links to the BSP find pages whose museums
have vetted Support links. BSP data: BeforeSavingPlanets scripts/support.py (/workspace/beforesavingplanets/support-links.csv).
Donate counted only where audited finances / recognized charity rating / public body. Idempotent; run after i18n-build."""
import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BSP_DONATE, BSP_VOL = 4, 3
BSP = [("Smilodon","La Brea Tar Pits (NHMLAC)"),("Triceratops","Ulster Museum (National Museums NI)"),
       ("Borealopelta","Royal Tyrrell Museum"),("Stegosaurus","American Museum of Natural History")]
T = {"en":("Fossil sites and museums on Before Saving Planets","Across Saving Planets and Before Saving Planets: {d} donation pages and {v} volunteer programs.","Each find page below has a Support their work box linking the museum that cares for it."),
 "fr":("Sites fossiles et musées sur Before Saving Planets","Sur Saving Planets et Before Saving Planets : {d} pages de dons et {v} programmes de bénévolat.","Chaque page ci-dessous a un encadré « Soutenir leur travail » vers le musée qui conserve la découverte."),
 "es":("Sitios fósiles y museos en Before Saving Planets","Entre Saving Planets y Before Saving Planets: {d} páginas de donación y {v} programas de voluntariado.","Cada página de abajo tiene un recuadro «Apoya su trabajo» con el museo que cuida el hallazgo."),
 "it":("Siti fossili e musei su Before Saving Planets","Tra Saving Planets e Before Saving Planets: {d} pagine di donazione e {v} programmi di volontariato.","Ogni pagina qui sotto ha un riquadro «Sostieni il loro lavoro» con il museo che custodisce il reperto."),
 "ar":("مواقع الأحافير والمتاحف على Before Saving Planets","عبر Saving Planets وBefore Saving Planets: {d} صفحة تبرع و{v} برنامج تطوع.","كل صفحة أدناه فيها مربع «ادعم عملهم» يربط بالمتحف الذي يعتني بالاكتشاف."),
 "he":("אתרי מאובנים ומוזיאונים ב-Before Saving Planets","ב-Saving Planets וב-Before Saving Planets יחד: {d} דפי תרומה ו-{v} תוכניות התנדבות.","בכל דף למטה יש תיבת «תמכו בעבודתם» עם קישור למוזיאון ששומר על הממצא.")}
for lang in T:
    f = 'Ways_to_Help.html' if lang=='en' else f'{lang}/Ways_to_Help.html'
    s = open(f, encoding='utf8').read(); o = s
    d = len(re.findall(r'class="btn help-btn"[^>]*>[^<]*', s)) and None
    sec = s[s.index('<!-- WTH-ALL:START -->'):s.index('<!-- WTH-ALL:END -->')]
    sums = re.findall(r'<ul class="wth-sum"><li><b>\d+</b>.*?<li><b>(\d+)</b>.*?<li><b>(\d+)</b>', sec)
    sd = sum(int(a) for a,_ in sums); sv = sum(int(b) for _,b in sums)
    h, tot, p = T[lang]; base = "https://www.beforesavingplanets.com/" + ("" if lang=="en" else lang+"/")
    lis = "".join(f'<li><a href="{base}{sl}.html#support" target="_blank" rel="noopener">{sl}</a> <span lang="en">({n})</span></li>' for sl,n in BSP)
    blk = (f'<!-- BSP-XSITE:START --><section class="five-ws" id="before-saving-planets"><h2>{h}</h2><ul class="wth-sum"><li><b>{sd+BSP_DONATE}</b> <span>Donate</span></li><li><b>{sv+BSP_VOL}</b> <span>Volunteer</span></li></ul>'
           f'<p>{tot.format(d=sd+BSP_DONATE, v=sv+BSP_VOL)}</p><p>{p}</p><ul>{lis}</ul></section><!-- BSP-XSITE:END -->')
    s = re.sub(r'<!-- BSP-XSITE:START -->.*?<!-- BSP-XSITE:END -->', '', s, flags=re.S)
    s = s.replace('<!-- WTH-ALL:END -->', '<!-- WTH-ALL:END -->' + blk, 1)
    if s != o: open(f, 'w', encoding='utf8').write(s)
    print(lang, sd, sv, '->', sd+BSP_DONATE, sv+BSP_VOL)
