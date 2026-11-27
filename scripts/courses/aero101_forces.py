"""AERO 101 four-forces diagram and the free course textbook.

Facts follow NASA Glenn, Beginner's Guide to Aeronautics, "Four Forces on an Airplane"
(https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/four-forces-on-an-airplane/):
weight toward Earth's center through the center of gravity; lift perpendicular to the
flight direction, mostly from the wings, through the center of pressure; thrust forward
along the body from the engines; drag along and opposed to the flight direction.
The Leishman citation was checked on the book's own pages on 2026-11-27.
SI drafts. Say SI, never AI.
"""
import html

BOOK = 'https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/'
BOOK_LICENSE = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
NASA = 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/four-forces-on-an-airplane/'

# label, short card back
FORCES = {
    'en': {
        'lift': ('Lift', 'Most lift comes from the wings. It is perpendicular to the flight direction and acts through the center of pressure.'),
        'weight': ('Weight', 'Weight is directed toward the center of the Earth and acts through the center of gravity.'),
        'thrust': ('Thrust', 'Thrust from the engines acts forward along the body. Exhaust goes aft; the force on the airplane is forward.'),
        'drag': ('Drag', 'Drag is air resisting the motion. It points along and against the flight direction.'),
        'lic': 'License:',
        'src': 'Source:',
        'nasa': 'NASA Glenn Beginner’s Guide to Aeronautics',
        'credit': 'Made with SI',
        'cap': 'Lift goes up from the wings through the center of pressure. Weight goes down through the center of gravity. Thrust goes forward from the engines. Drag goes back along the airframe, opposite the flight direction.',
        'book_h': 'Course textbook',
        'free': 'Free open textbook.',
        'opt': 'Optional, if you have access:',
        'and': 'and',
        'sources': 'Sources for each unit are listed in that unit. Listing a source is not an endorsement.',
    },
    'fr': {
        'lift': ('Portance', 'L’essentiel de la portance vient des ailes. Elle est perpendiculaire au sens du vol et agit au centre de pression.'),
        'weight': ('Poids', 'Le poids est dirigé vers le centre de la Terre et agit au centre de gravité.'),
        'thrust': ('Poussée', 'La poussée des moteurs agit vers l’avant, le long du fuselage. Les gaz sortent vers l’arrière ; la force sur l’avion va vers l’avant.'),
        'drag': ('Traînée', 'La traînée est la résistance de l’air. Elle est dirigée dans le sens du vol, et à l’opposé.'),
        'lic': 'Licence :',
        'src': 'Source :',
        'nasa': 'Beginner’s Guide to Aeronautics de NASA Glenn',
        'credit': 'Réalisé avec SI',
        'cap': 'La portance monte depuis les ailes, au centre de pression. Le poids descend au centre de gravité. La poussée va vers l’avant depuis les moteurs. La traînée va vers l’arrière le long de la cellule, à l’opposé du sens du vol.',
        'book_h': 'Manuel du cours',
        'free': 'Manuel ouvert et gratuit.',
        'opt': 'Facultatif, si vous y avez accès :',
        'and': 'et',
        'sources': 'Les sources de chaque unité sont indiquées dans l’unité. Citer une source n’est pas une approbation.',
    },
    'es': {
        'lift': ('Sustentación', 'La mayor parte de la sustentación sale de las alas. Es perpendicular al sentido del vuelo y actúa en el centro de presión.'),
        'weight': ('Peso', 'El peso se dirige hacia el centro de la Tierra y actúa en el centro de gravedad.'),
        'thrust': ('Empuje', 'El empuje de los motores actúa hacia adelante, a lo largo del fuselaje. Los gases salen hacia atrás; la fuerza sobre el avión va hacia adelante.'),
        'drag': ('Resistencia', 'La resistencia es el aire que se opone al movimiento. Apunta en la dirección del vuelo y en contra de ella.'),
        'lic': 'Licencia:',
        'src': 'Fuente:',
        'nasa': 'Beginner’s Guide to Aeronautics de NASA Glenn',
        'credit': 'Hecho con SI',
        'cap': 'La sustentación sube desde las alas, en el centro de presión. El peso baja en el centro de gravedad. El empuje va hacia adelante desde los motores. La resistencia va hacia atrás a lo largo del avión, en contra del sentido del vuelo.',
        'book_h': 'Libro del curso',
        'free': 'Libro abierto y gratuito.',
        'opt': 'Opcional, si tienes acceso:',
        'and': 'y',
        'sources': 'Las fuentes de cada unidad están en esa unidad. Citar una fuente no es un aval.',
    },
    'ar': {
        'lift': ('الرفع', 'معظم الرفع يأتي من الجناحين. وهو عمودي على اتجاه الطيران ويمر بمركز الضغط.'),
        'weight': ('الوزن', 'الوزن موجّه نحو مركز الأرض ويمر بمركز الثقل.'),
        'thrust': ('الدفع', 'دفع المحركات يعمل إلى الأمام على امتداد الجسم. العادم يخرج إلى الخلف، والقوة على الطائرة إلى الأمام.'),
        'drag': ('السحب', 'السحب هو مقاومة الهواء للحركة. وهو في اتجاه الطيران وعكسه.'),
        'lic': 'الترخيص:',
        'src': 'المصدر:',
        'nasa': 'دليل ناسا غلين للمبتدئين في علم الطيران',
        'credit': 'صُنع بمساعدة SI',
        'cap': 'الرفع إلى الأعلى من الجناحين عند مركز الضغط. الوزن إلى الأسفل عند مركز الثقل. الدفع إلى الأمام من المحركات. السحب إلى الخلف على هيكل الطائرة، عكس اتجاه الطيران.',
        'book_h': 'الكتاب المقرر',
        'free': 'كتاب مفتوح مجاني.',
        'opt': 'اختياري، إن كان لديك وصول:',
        'and': 'و',
        'sources': 'مصادر كل وحدة مذكورة داخل الوحدة. ذكر المصدر ليس تزكية.',
    },
    'it': {
        'lift': ('Portanza', 'La maggior parte della portanza viene dalle ali. È perpendicolare al senso del volo e agisce nel centro di pressione.'),
        'weight': ('Peso', 'Il peso è diretto verso il centro della Terra e agisce nel baricentro.'),
        'thrust': ('Spinta', 'La spinta dei motori agisce in avanti, lungo la fusoliera. I gas escono indietro; la forza sull’aereo è in avanti.'),
        'drag': ('Resistenza', 'La resistenza è l’aria che si oppone al moto. È diretta lungo il volo e contro di esso.'),
        'lic': 'Licenza:',
        'src': 'Fonte:',
        'nasa': 'Beginner’s Guide to Aeronautics della NASA Glenn',
        'credit': 'Realizzato con SI',
        'cap': 'La portanza sale dalle ali, nel centro di pressione. Il peso scende nel baricentro. La spinta va in avanti dai motori. La resistenza va indietro lungo la cellula, opposta al senso del volo.',
        'book_h': 'Libro del corso',
        'free': 'Libro aperto e gratuito.',
        'opt': 'Facoltativo, se hai accesso:',
        'and': 'e',
        'sources': 'Le fonti di ogni unità sono indicate nell’unità. Citare una fonte non è un’approvazione.',
    },
    'he': {
        'lift': ('עילוי', 'רוב העילוי בא מהכנפיים. הוא ניצב לכיוון הטיסה ופועל דרך מרכז הלחץ.'),
        'weight': ('משקל', 'המשקל מכוון אל מרכז כדור הארץ ופועל דרך מרכז הכובד.'),
        'thrust': ('דחף', 'הדחף מהמנועים פועל קדימה לאורך הגוף. הפליטה יוצאת לאחור; הכוח על המטוס הוא קדימה.'),
        'drag': ('גרר', 'הגרר הוא התנגדות האוויר לתנועה. הוא לאורך כיוון הטיסה ונגדו.'),
        'lic': 'רישיון:',
        'src': 'מקור:',
        'nasa': 'המדריך למתחילים באווירונאוטיקה של נאס״א גלן',
        'credit': 'נוצר עם SI',
        'cap': 'העילוי עולה מהכנפיים במרכז הלחץ. המשקל יורד במרכז הכובד. הדחף קדימה מהמנועים. הגרר לאחור לאורך גוף המטוס, נגד כיוון הטיסה.',
        'book_h': 'ספר הלימוד',
        'free': 'ספר פתוח וחינמי.',
        'opt': 'אופציונלי, אם יש לכם גישה:',
        'and': 'ו',
        'sources': 'המקורות של כל יחידה רשומים בתוך היחידה. ציון מקור אינו הסכמה.',
    },
}

_PLANE = (
    '<g fill="#e7eef5" stroke="#93a6b8" stroke-width="1.4" stroke-linejoin="round">'
    '<path d="M48 108c0-18 30-32 82-36h148c38-2 66 12 78 36-14 24-42 34-78 34H130c-52-4-82-18-82-34z"/>'
    '<path fill="#163e63" stroke="#163e63" d="M62 98l10-48c12-4 34 2 42 20l-10 34z"/>'
    '<path fill="#d3dee8" d="M36 108h46l12-10 12 10-12 10-12-10z"/>'
    '<path fill="#d5dee8" d="M158 98c20-10 58-12 92 8l-20 18c-28 8-58 4-74-8z"/>'
    '<path fill="#7d93a8" stroke="#6a8094" d="M186 128c0-9 16-16 44-13 12 7 14 18 4 24l-38 4c-8-2-10-8-10-15z"/>'
    '<ellipse cx="228" cy="126" rx="5" ry="8" fill="#24384a" stroke="none"/>'
    '<path fill="#163e63" stroke="none" d="M300 92h30a3 3 0 0 1 0 7h-30a3 3 0 0 1 0-7z"/>'
    '</g>'
)

def _e(s):
    return html.escape(s, quote=True)

def _arrow(kind, x1, y1, x2, y2, lx, ly, anchor, label, rtl):
    dx, dy = x2 - x1, y2 - y1
    mag = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / mag, dy / mag
    sx, sy = x2 - ux * 12, y2 - uy * 12
    direction = ' direction="rtl"' if rtl else ''
    return (
        f'<g class="crs-arrow is-{kind}">'
        f'<line x1="{x1}" y1="{y1}" x2="{sx:.1f}" y2="{sy:.1f}" />'
        f'<polygon points="{_head(x1, y1, x2, y2)}" />'
        f'<text x="{lx}" y="{ly}" text-anchor="{anchor}"{direction}>{_e(label)}</text>'
        f'</g>'
    )

def _head(x1, y1, x2, y2):
    # A small triangle pointing from (x1,y1) toward (x2,y2), tip at the end.
    dx, dy = x2 - x1, y2 - y1
    mag = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / mag, dy / mag
    px, py = -uy, ux
    tipx, tipy = x2, y2
    bx, by = tipx - ux * 11, tipy - uy * 11
    return f'{tipx:.1f},{tipy:.1f} {bx + px * 5:.1f},{by + py * 5:.1f} {bx - px * 5:.1f},{by - py * 5:.1f}'

def plane_svg(lang, which):
    """which is 'all' or one of lift, weight, thrust, drag. Nose points right; dir stays ltr."""
    T = FORCES[lang]
    rtl = ' direction="rtl"' if lang in ('ar', 'he') else ''
    # Patch text direction via the helper by passing rtl flag through labels only.
    names = {k: T[k][0] for k in ('lift', 'weight', 'thrust', 'drag')}
    if which == 'all':
        aria = T['cap']
        klass = 'crs-plane is-all'
    else:
        aria = names[which] + '. ' + T[which][1]
        klass = f'crs-plane is-one is-{which}'
    rtl_text = lang in ('ar', 'he')
    arrows = ''.join([
        _arrow('lift', 200, 96, 200, 28, 200, 18, 'middle', names['lift'], rtl_text),
        _arrow('weight', 176, 116, 176, 184, 176, 190, 'middle', names['weight'], rtl_text),
        _arrow('thrust', 220, 138, 300, 138, 248, 158, 'middle', names['thrust'], rtl_text),
        _arrow('drag', 130, 108, 22, 108, 70, 92, 'middle', names['drag'], rtl_text),
    ])
    return (
        f'<svg class="{klass}" viewBox="0 0 360 200" role="img" aria-label="{_e(aria)}">'
        f'{_PLANE}{arrows}'
        f'<circle class="crs-cg" cx="176" cy="108" r="2.4"/>'
        f'</svg>'
    )

def figure(lang):
    T = FORCES[lang]
    return (
        '<figure class="crs-forces"><div class="crs-forces-stage" dir="ltr">'
        + plane_svg(lang, 'all') + '</div><figcaption>'
        f'<p>{_e(T["cap"])}</p>'
        f'<p>{_e(T["credit"]).replace("SI", "<bdi>SI</bdi>")}</p>'
        f'<p>{_e(T["src"])} <a href="{NASA}" rel="noopener">{_e(T["nasa"])}</a></p>'
        '</figcaption></figure>'
    )

def _card(lang, which):
    T = FORCES[lang]
    name, back = T[which]
    src = f'{_e(T["src"])} {_e(T["nasa"])}.'
    return (
        '<li><div class="crs-fc-f"><p class="crs-fc-name">' + _e(name) + '</p>'
        '<div class="crs-forces-stage" dir="ltr">' + plane_svg(lang, which) + '</div></div>'
        f'<p class="crs-fc-b">{_e(back)} {src}</p></li>'
    )

def force_cards(lang):
    return ''.join(_card(lang, k) for k in ('lift', 'weight', 'thrust', 'drag'))

def readings_inner(lang):
    T = FORCES[lang]
    return (
        '<div class="crs-book"><h3>' + _e(T['book_h']) + '</h3>'
        f'<p><a href="{BOOK}" rel="noopener" lang="en"><bdi dir="ltr">Introduction to Aerospace Flight Vehicles</bdi></a>. '
        '<bdi dir="ltr">J. Gordon Leishman</bdi>. <bdi dir="ltr">Embry-Riddle Aeronautical University</bdi>. '
        '<bdi dir="ltr">October 2027 Release</bdi>. <bdi dir="ltr">© 2022–2026</bdi>. '
        f'{_e(T["lic"])} <a href="{BOOK_LICENSE}" rel="noopener license">CC BY-NC-ND 4.0</a>. {_e(T["free"])}</p>'
        f'<p>{_e(T["opt"])} <bdi dir="ltr">John D. Anderson Jr.</bdi> {_e(T["and"])} '
        '<bdi dir="ltr">Mary L. Bowden</bdi>, <bdi dir="ltr" lang="en">Introduction to Flight</bdi>, '
        '<bdi dir="ltr">9th edition</bdi> (<bdi dir="ltr">McGraw-Hill</bdi>, <bdi dir="ltr">2022</bdi>).</p>'
        '</div>'
    )

DEEPER = {
    'en': 'Go Deeper',
    'fr': 'Pour approfondir',
    'es': 'Para profundizar',
    'ar': 'للتعمّق',
    'it': 'Per approfondire',
    'he': 'להעמקה',
}
BOOK_ICON = ('<svg class="crs-deeper-i" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" '
             'd="M12 6.2C10.6 4.8 8.4 4 6 4H4.5v14H6c2.2 0 4.2.7 6 2 1.8-1.3 3.8-2 6-2h1.5V4H18c-2.4 0-4.6.8-6 2.2z"/>'
             '<path fill="none" stroke="currentColor" stroke-width="1.6" d="M12 6.2v13.8"/>'
             '</svg>')

def deeper(lang, items):
    """Collapsed extra reading for one unit. items is the inner HTML of the list."""
    label = html.escape(DEEPER[lang])
    return (f'<details class="crs-deeper"><summary>{BOOK_ICON}<h3>{label}</h3></summary>'
            f'<ul class="crs-res">{items}</ul></details>')

CSS = (
    '.crs-ocw{display:flex;flex-wrap:wrap;gap:.45rem;margin:.15rem 0 .85rem}'
    '.crs-ocw a{min-height:44px;display:inline-flex;align-items:center;padding:0 .95rem;border-radius:999px;text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,.38);background:linear-gradient(180deg,rgba(255,255,255,.16),rgba(255,255,255,.04));box-shadow:inset 0 1px 0 rgba(255,255,255,.35)}'
    '.crs-units{margin:.35rem 0 1.15rem;border:1px solid rgba(255,255,255,.3);border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.13),rgba(255,255,255,.04));box-shadow:inset 0 1px 0 rgba(255,255,255,.4),0 10px 26px rgba(0,0,0,.22)}'
    '.crs-units>summary{cursor:pointer;min-height:48px;display:flex;align-items:center;gap:.7rem;padding:.35rem 1rem;list-style:none}'
    '.crs-units>summary::-webkit-details-marker{display:none}'
    '.crs-units>summary::after{content:"";width:.5rem;height:.5rem;margin-inline-start:auto;border-inline-end:2px solid currentColor;border-block-end:2px solid currentColor;transform:translateY(-.12rem) rotate(45deg)}'
    '.crs-units[open]>summary::after{transform:translateY(.12rem) rotate(225deg)}'
    '.crs-units>summary h2{margin:0;font-size:1.15rem}'
    '.crs-units .crs-tw{padding:0 .7rem .8rem}'
    '.crs-units table{width:100%;border-collapse:collapse}'
    '.crs-units th,.crs-units td{text-align:start;padding:.55rem .65rem;border-bottom:1px solid rgba(255,255,255,.12);vertical-align:top}'
    '.crs-units th{font-size:.75rem;letter-spacing:.04em;text-transform:uppercase}'
    '.crs-units td:first-child{font-weight:800;white-space:nowrap;width:4.2rem}'
    '.crs-book{margin:0 0 .9rem;padding:.8rem 1rem;border:1px solid rgba(255,255,255,.28);border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04));box-shadow:inset 0 1px 0 rgba(255,255,255,.35)}'
    '.crs-book h3{margin:0 0 .35rem;font-size:1.05rem}'
    '.crs-forces{margin:.8rem 0 1rem}.crs-forces-stage{border-radius:16px;overflow:hidden;background:linear-gradient(180deg,#10283f,#071422);border:1px solid rgba(255,255,255,.2)}'
    '.crs-forces svg,.crs-fc-f svg{display:block;width:100%;height:auto}'
    '.crs-forces figcaption{margin-top:.4rem;font-size:.9rem}'
    '.crs-fc-name{margin:0 0 .3rem;font-weight:800}'
    '.crs-arrow{opacity:0;animation:crs-force 6s ease-in-out infinite}'
    '.crs-arrow line{stroke:#d7e6f2;stroke-width:2.2}'
    '.crs-arrow polygon{fill:#d7e6f2}'
    '.crs-arrow text{fill:#f4f8fb;font-size:13px;font-weight:700;font-family:Montserrat,"Noto Sans Arabic","Noto Sans Hebrew",sans-serif}'
    '.is-lift line,.is-lift polygon{stroke:#8ee0b0;fill:#8ee0b0}'
    '.is-weight line,.is-weight polygon{stroke:#f3d56a;fill:#f3d56a}'
    '.is-thrust line,.is-thrust polygon{stroke:#8ecfff;fill:#8ecfff}'
    '.is-drag line,.is-drag polygon{stroke:#f0b0b0;fill:#f0b0b0}'
    '.crs-cg{fill:#f3d56a;stroke:none}'
    '.crs-plane.is-all .is-lift{animation-delay:0s}.crs-plane.is-all .is-weight{animation-delay:1.5s}'
    '.crs-plane.is-all .is-thrust{animation-delay:3s}.crs-plane.is-all .is-drag{animation-delay:4.5s}'
    '.crs-plane.is-one .crs-arrow{animation:none;opacity:.28}'
    '.crs-plane.is-lift .is-lift,.crs-plane.is-weight .is-weight,.crs-plane.is-thrust .is-thrust,.crs-plane.is-drag .is-drag{opacity:1}'
    '@keyframes crs-force{0%{opacity:0}15%{opacity:1}55%{opacity:1}100%{opacity:.25}}'
    '@media (prefers-reduced-motion:reduce){.crs-plane.is-all .crs-arrow{animation:none;opacity:1}.crs-plane.is-one .crs-arrow{animation:none}}'
    '@media (max-width:640px){.crs-units thead,.crs-units thead tr,.crs-units thead th{display:block;position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);clip-path:inset(50%);white-space:nowrap;border:0}'
    '.crs-units tr{display:block;padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,.14)}'
    '.crs-units td,.crs-units td:first-child{display:block;border:0;padding:.15rem .4rem;white-space:normal;width:auto;overflow-wrap:anywhere}'
    '.crs-units td::before{content:attr(data-label);display:block;font-size:.7rem;letter-spacing:.04em;text-transform:uppercase;opacity:.72}}'
    '.crs-deeper{margin:.85rem 0 .15rem;border:1px solid rgba(255,255,255,.24);border-radius:14px;background:rgba(255,255,255,.05)}'
    '.crs-deeper>summary{cursor:pointer;min-height:44px;display:flex;align-items:center;gap:.5rem;padding:.15rem .85rem;list-style:none}'
    '.crs-deeper>summary::-webkit-details-marker{display:none}'
    '.crs-deeper>summary::after{content:"";width:.45rem;height:.45rem;margin-inline-start:auto;flex:none;border-inline-end:2px solid currentColor;border-block-end:2px solid currentColor;transform:translateY(-.08rem) rotate(45deg)}'
    '.crs-deeper[open]>summary::after{transform:translateY(.08rem) rotate(225deg)}'
    '.crs-deeper>summary h3{margin:0;flex:1;font-size:.92rem;font-weight:750;line-height:1.25}'
    '.crs-deeper-i{width:1.15rem;height:1.15rem;flex:none;color:#d7ecff}'
    '.crs-deeper .crs-res{margin:.05rem .95rem .8rem;font-size:.92rem}'
    '.crs-units{position:relative;overflow:clip;max-width:100%}'
    '.crs-units>summary h2,.crs-deeper>summary h3{min-width:0;overflow-wrap:anywhere}'
    '.crs-tools{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}'
    '.crs-btn{display:inline-flex;align-items:center;justify-content:center;max-width:100%;box-sizing:border-box;text-align:center;line-height:1.25;white-space:normal}'
    '.crs-tw{max-width:100%;overflow-x:auto}'
    '.crs-src,.crs-res{overflow-wrap:anywhere}'
    '.katex-display,.crs-eq{max-width:100%;overflow-x:auto}'
    '@media (max-width:640px){.crs{padding-bottom:5.5rem}}'
)

DESC = {
    'en': 'Description', 'fr': 'Description', 'es': 'Descripción',
    'ar': 'الوصف', 'it': 'Descrizione', 'he': 'תיאור',
}
