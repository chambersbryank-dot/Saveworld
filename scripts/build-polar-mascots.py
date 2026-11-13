#!/usr/bin/env python3
"""Oct 28 (founder): polar mascots on World_Map.html + Kids_Map.html, all 6 langs (run after build-map/build-map-he/i18n).
A polar bear walks down from the north and points up ('look up here'); a penguin waddles up from the south and points down.
World map: buttons pan the map to each pole (polar-mascots.js). Kids map: links to Polar.html#north-pole / #south-pole.
prefers-reduced-motion: static. Idempotent (PMASCOT markers)."""
import os, re
from html import escape as E
V = "20261028pm3"
T = {
 'en': ('Look up here for cooler solutions!', 'Arctic solutions, North Pole', 'Antarctic solutions are down this way!', 'South Pole, Antarctica'),
 'fr': ('Regarde par ici, des solutions encore plus fraîches !', "Solutions de l'Arctique, pôle Nord", "Les solutions de l'Antarctique, c'est par là !", 'Pôle Sud, Antarctique'),
 'es': ('¡Mira aquí arriba: soluciones más frescas!', 'Soluciones del Ártico, Polo Norte', '¡Las soluciones de la Antártida están por aquí abajo!', 'Polo Sur, Antártida'),
 'ar': ('انظر إلى هنا في الأعلى: حلول أكثر برودة!', 'حلول القطب الشمالي', 'حلول القارة القطبية الجنوبية من هنا في الأسفل!', 'القطب الجنوبي، أنتاركتيكا'),
 'it': ('Guarda quassù: soluzioni ancora più fresche!', "Soluzioni dell'Artico, Polo Nord", "Le soluzioni dell'Antartide sono quaggiù!", 'Polo Sud, Antartide'),
 'he': ('הביטו כאן למעלה: פתרונות קרירים יותר!', 'פתרונות באזור הארקטי, הקוטב הצפוני', 'הפתרונות של אנטארקטיקה כאן למטה!', 'הקוטב הדרומי, אנטארקטיקה'),
}
def block(l, kids):
    a, b, c, d = T[l]
    def one(cls, pole, ch, hand, say, sub):
        inner = (f'<span class="pm-ch" aria-hidden="true">{ch}</span><span class="pm-hand" aria-hidden="true">{hand}</span>'
                 f'<span class="pm-say"><b>{E(say)}</b><small>{E(sub)}</small></span>')
        if kids:
            return f'<a class="pm {cls}" href="Polar.html#{"north-pole" if pole=="n" else "south-pole"}">{inner}</a>'
        return f'<button type="button" class="pm {cls}" data-pole="{pole}">{inner}</button>'
    return ('<div class="pm-wrap" role="group">' + one('pm-n', 'n', '🐻‍❄️', '☝️', a, b) + one('pm-s', 's', '🐧', '👇', c, d) + '</div>')
def main():
    n = 0
    for l in T:
        dd = '' if l == 'en' else l + '/'
        pre = '' if l == 'en' else '../'
        p = dd + 'World_Map.html'
        if not os.path.exists(p): continue
        t = open(p, encoding='utf8').read()
        t = re.sub(r'<!-- PMASCOT:START -->.*?<!-- PMASCOT:END -->\n?', '', t, flags=re.S)
        t = re.sub(r'<!-- PMASCOTH:START -->.*?<!-- PMASCOTH:END -->', '', t, flags=re.S)
        open(p, 'w', encoding='utf8').write(t); n += 1
    print(f'polar mascots: {n} pages')
if __name__ == '__main__': main()
