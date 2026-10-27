#!/usr/bin/env python3
"""Oct 16 2026: standards tags on Learn guides, math pages, labs and calculators (6 languages).
Chips under the page hero + schema.org educationalAlignment (AlignmentObject) in the page's LearningResource JSON-LD, and a
filter-by-standard block on Learn.html. Alignments are our editorial judgement and are listed only where the page genuinely
practises the performance expectation / standard / unit; AP and IB codes only where the official course description lists the
topic (see paths_text2.py). Not reviewed or endorsed by NGSS Lead States, CCSSO/NGA, the College Board or the IBO. Idempotent."""
import re, os, json, html, sys
sys.path.insert(0, 'scripts')
import calc_text as CT
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']; E = lambda x: html.escape(x, quote=True)
NGSS_URL = 'https://www.nextgenscience.org/'
AP1 = 'https://apcentral.collegeboard.org/media/pdf/ap-physics-1-course-and-exam-description.pdf'
AP2 = 'https://apcentral.collegeboard.org/media/pdf/ap-physics-2-course-at-a-glance.pdf'
IB = 'https://ibo.org/globalassets/new-structure/recognition/pdfs/dp_sciences_physics_subject-brief_jan_2022_e.pdf'
def fw(code):
    if code.startswith(('HS-', 'MS-')): return 'NGSS', NGSS_URL
    if code.startswith('CCSS.'): c = code[5:]; return 'Common Core State Standards for Mathematics', 'https://www.thecorestandards.org/Math/Content/' + c.replace('-', '/').replace('.', '/') + '/'
    if code.startswith('AP1 '): return 'AP Physics 1', AP1
    if code.startswith('AP2 '): return 'AP Physics 2', AP2
    if code.startswith('IB '): return 'IB Diploma Programme Physics', IB
STD = {
 'Orbits_Guide.html': ['HS-ESS1-4', 'HS-PS2-4', 'MS-PS2-4'],
 'Orbit_Math.html': ['HS-ESS1-4', 'HS-PS2-4', 'HS-PS2-2', 'CCSS.HSF-LE.A.4', 'AP1 Unit 2', 'AP1 Unit 4', 'IB D.1', 'IB A.2'],
 'Orbit_Lab.html': ['HS-ESS1-4', 'HS-PS2-4'],
 'Aero_Guide.html': ['HS-PS2-1', 'MS-PS2-2'],
 'Aero_Math.html': ['HS-PS2-1', 'CCSS.HSA-CED.A.4', 'AP1 Unit 8', 'AP2 Unit 14'],
 'Aero_Lab.html': ['HS-PS2-1', 'MS-PS2-2'],
 'Physics_Guide.html': ['HS-PS2-1', 'MS-PS2-2', 'HS-PS3-1'],
 'Physics_Math.html': ['HS-PS2-1', 'HS-PS3-1', 'CCSS.HSG-SRT.C.8', 'AP1 Unit 1', 'AP1 Unit 3', 'AP1 Unit 7', 'IB A.1', 'IB A.3', 'IB C.1'],
 'Physics_Lab.html': ['HS-PS2-1', 'MS-PS2-2'],
}
CALC = {'dv': ['HS-PS2-2', 'CCSS.HSF-LE.A.4', 'AP1 Unit 4', 'IB A.2'], 'hohmann': ['HS-ESS1-4', 'AP1 Unit 2', 'IB D.1'], 'period': ['HS-ESS1-4', 'AP1 Unit 2', 'IB D.1'],
        'vel': ['HS-ESS1-4', 'HS-PS2-4', 'IB D.1'], 'stall': ['HS-PS2-1', 'CCSS.HSA-CED.A.4', 'AP1 Unit 8'], 'lift': ['HS-PS2-1', 'CCSS.HSA-CED.A.4', 'AP1 Unit 8'],
        'mach': ['AP2 Unit 14', 'CCSS.HSN-Q.A.1'], 'tw': ['HS-PS2-1', 'AP1 Unit 2', 'IB A.2'], 'rotor': ['HS-PS3-1', 'AP1 Unit 3', 'IB A.3'],
        'proj': ['HS-PS2-1', 'CCSS.HSG-SRT.C.8', 'AP1 Unit 1', 'IB A.1'], 'pend': ['AP1 Unit 7', 'IB C.1', 'CCSS.HSA-CED.A.4']}
for c in CT.C: STD[c['page']] = CALC[c['id']]
L = {'en': dict(h='Standards', note='Our alignment; not reviewed by the standards bodies.', f='Filter by standard', all='All standards', fh='Find pages by standard'),
     'fr': dict(h='Programmes', note='Correspondance établie par nous ; non vérifiée par les organismes de normes.', f='Filtrer par norme', all='Toutes les normes', fh='Trouver des pages par norme'),
     'es': dict(h='Estándares', note='Alineación nuestra; no revisada por los organismos de estándares.', f='Filtrar por estándar', all='Todos los estándares', fh='Buscar páginas por estándar'),
     'ar': dict(h='المعايير', note='مواءمة من إعدادنا؛ لم تراجعها جهات المعايير.', f='التصفية حسب المعيار', all='كل المعايير', fh='ابحث عن الصفحات حسب المعيار'),
     'it': dict(h='Standard', note='Allineamento nostro; non verificato dagli enti degli standard.', f='Filtra per standard', all='Tutti gli standard', fh='Trova pagine per standard'),
     'he': dict(h='תקנים', note='ההתאמה שלנו; לא נבדקה על ידי גופי התקנים.', f='סינון לפי תקן', all='כל התקנים', fh='מצאו דפים לפי תקן')}
def short(code): return code[5:] if code.startswith('CCSS.') else code
def chips(l, codes):
    u = L[l]
    return (f'<!-- STDTAGS:START --><div class="lw std-wrap" data-pagefind-ignore="all" style="padding-top:.4rem"><p class="std-h" style="margin:.2rem 0;font-weight:700">{E(u["h"])}:</p><ul class="lchips std-chips" aria-label="{E(u["h"])}">'
            + ''.join(f'<li class="lchip"><bdi dir="ltr" title="{E(fw(c)[0])}">{E(("NGSS " if c[:3] in ("HS-", "MS-") else "CCSS " if c.startswith("CCSS.") else "") + short(c))}</bdi></li>' for c in codes)
            + f'</ul><p class="lnote" style="font-size:.85rem;margin:.2rem 0 0">{E(u["note"])}</p></div><!-- STDTAGS:END -->')
def align(codes): return [{'@type': 'AlignmentObject', 'alignmentType': 'teaches', 'educationalFramework': fw(c)[0], 'targetName': short(c), 'targetUrl': fw(c)[1]} for c in codes]
def strip(s, k): return re.sub(rf'<!-- {k}:START -->.*?<!-- {k}:END -->', '', s, flags=re.S)
def title_of(s): m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S); return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
def main():
    n = 0
    for l in LANGS:
        d = '' if l == 'en' else l + '/'; titles = {}
        for p, codes in STD.items():
            f = d + p
            if not os.path.exists(f): continue
            s = open(f, encoding='utf8').read(); s2 = strip(s, 'STDTAGS'); titles[p] = title_of(s2)
            m = re.search(r'<section class="page-hero[^"]*".*?</section>', s2, re.S)
            if m: s2 = s2[:m.end()] + chips(l, codes) + s2[m.end():]
            def ld(mm):
                try: j = json.loads(mm.group(1))
                except Exception: return mm.group(0)
                if not isinstance(j, dict) or j.get('@type') != 'LearningResource': return mm.group(0)
                j['educationalAlignment'] = align(codes)
                if p.endswith('_Calculator.html'): j['learningResourceType'] = 'interactive calculator'; j['interactivityType'] = 'active'
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
            s2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s2, flags=re.S)
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
        # Learn hub filter
        f = d + 'Learn.html'
        if os.path.exists(f):
            s = open(f, encoding='utf8').read(); s2 = strip(s, 'STDMAP'); u = L[l]
            allc = sorted({c for v in STD.values() for c in v}, key=lambda c: (c[:2] not in ('HS', 'MS'), c.startswith('CCSS'), c))
            opts = ''.join(f'<option value="{E(c)}">{E(short(c))}</option>' for c in allc)
            items = ''.join(f'<li data-std="{E("|".join(STD[p]))}"><a href="{E(p if os.path.exists(d + p) else "../" + p)}">{E(titles.get(p) or p)}</a> <small dir="ltr">{E(", ".join(short(c) for c in STD[p]))}</small></li>' for p in STD if p in titles)
            blk = (f'<!-- STDMAP:START --><h2 id="standards-filter">{E(u["fh"])}</h2><label style="display:flex;flex-direction:column;gap:.3rem;max-width:360px;font-weight:700">{E(u["f"])}'
                   f'<select id="std-f" style="min-height:44px;font:inherit;border-radius:10px;padding:.3rem .6rem"><option value="">{E(u["all"])}</option>{opts}</select></label>'
                   f'<ul id="std-list" aria-live="polite">{items}</ul><p class="lnote">{E(u["note"])}</p>'
                   '<script>(function(){var s=document.getElementById("std-f");if(!s)return;s.addEventListener("change",function(){var v=s.value;document.querySelectorAll("#std-list li").forEach(function(li){li.hidden=!!v&&("|"+li.dataset.std+"|").indexOf("|"+v+"|")<0})})})();</script><!-- STDMAP:END -->')
            stop = s2.find('<!-- NLCALL:START -->'); stop = stop if stop > 0 else s2.find('</main>')
            k = s2.rfind('</div>', 0, stop)  # end of the hub's .lw column
            s2 = s2[:k] + blk + s2[k:]
            if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-standards: {n} pages')
if __name__ == '__main__': main()
