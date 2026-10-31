#!/usr/bin/env python3
"""New observation scenes for Hesna's memory drills. L1–L4 stay in the base file."""
from __future__ import annotations

import random

ORD_EN = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]
ORD_AR = ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع"]

# Filled from the base vocab at build time if present; these match the existing page.
C = {
    "red": ["Red", "أحمر"], "gray": ["Gray", "رمادي"], "blue": ["Blue", "أزرق"],
    "green": ["Green", "أخضر"], "black": ["Black", "أسود"], "white": ["White", "أبيض"],
    "yellow": ["Yellow", "أصفر"], "purple": ["Purple", "بنفسجي"], "pink": ["Pink", "وردي"],
    "orange": ["Orange", "برتقالي"], "brown": ["Brown", "بني"], "blonde": ["Blonde", "أشقر"],
}
I = {
    "bag": ["a bag", "حقيبة"], "umbrella": ["an umbrella", "مظلة"], "phone": ["a phone", "هاتف"],
    "balloon": ["a balloon", "بالون"], "box": ["a box", "صندوق"], "cup": ["a cup", "كوب"],
}
V = {
    "car": ["Car", "سيارة"], "van": ["Van", "شاحنة صغيرة"], "pickup": ["Pickup truck", "بيك أب"],
    "taxi": ["Taxi", "سيارة أجرة"],
}
STREETS = ["King St", "Beretania St", "Kalakaua Ave", "Kuhio Ave", "Kapahulu Ave", "Keeaumoku St", "Piikoi St", "Punchbowl St", "Ward Ave", "Auahi St", "Hotel St", "Young St"]


def q(en, ar, oe, oa, ans):
    if len(oe) < 2 or len(oe) != len(oa):
        raise SystemExit("bad options " + en)
    if len(set(oe)) != len(oe):
        raise SystemExit("dup " + en + str(oe))
    if not (0 <= ans < len(oe)):
        raise SystemExit("ans " + en)
    return [en, ar, oe, oa, ans]


def pick(rng, pool, correct, n=3):
    rest = [x for x in pool if x != correct]
    rng.shuffle(rest)
    if len(rest) < n:
        raise SystemExit("pool")
    return rest[:n]


def street_questions(scene, vocab, seed):
    rng = random.Random(seed)
    C_, I_, V_ = vocab["C"], vocab["I"], vocab["V"]
    cols = list(C_.keys())
    out = []

    def add(en, ar, oe, oa, ans):
        out.append(q(en, ar, oe, oa, ans))

    def col_opts(correct):
        wrong = pick(rng, cols, correct)
        oe = [C_[correct][0]] + [C_[w][0] for w in wrong]
        oa = [C_[correct][1]] + [C_[w][1] for w in wrong]
        return oe, oa

    # Clock and signs.
    tm = scene["tm"]
    parts = tm.replace(":", " ").split()
    hh, mm, ap = parts[0], parts[1], parts[2]
    alts = [f"{hh}:{mm[::-1]} {ap}" if mm[::-1] != mm else f"{hh}:{int(mm)+3:02d} {ap}",
            f"{int(hh)+1}:{mm} {ap}", f"{hh}:{mm} {('PM' if ap=='AM' else 'AM')}"]
    alts = [a for a in alts if a != tm][:3]
    while len(alts) < 3:
        alts.append(f"{hh}:{int(mm)+7:02d} {ap}")
    oe = alts[:2] + [tm] + alts[2:3]
    # put answer at index 2 to mirror the original page's habit, but any index is fine
    add("What time did the clock show?", "ما الوقت الذي أظهرته الساعة؟", [alts[0], alts[1], tm, alts[2]],
        [alts[0], alts[1], tm, alts[2]], 2)

    st, cr = scene["st"], scene["cr"]
    others = [s for s in STREETS if s not in (st, cr)]
    rng.shuffle(others)
    add("Which street name was on the top sign?", "ما اسم الشارع على اللافتة العليا؟",
        [others[0], others[1], cr, st], [others[0], others[1], cr, st], 3)
    add("Which cross street was on the lower sign?", "ما اسم الشارع على اللافتة السفلى؟",
        [others[2], others[3], cr, others[4]], [others[2], others[3], cr, others[4]], 2)

    people = scene["p"]
    for i, p in enumerate(people):
        n, na = ORD_EN[i], ORD_AR[i]
        oe, oa = col_opts(p["s"])
        add(f"What color shirt was the {n} person from the left wearing?",
            f"ما لون قميص الشخص {na} من اليسار؟", oe, oa, 0)
        oe, oa = col_opts(p["p"])
        add(f"What color pants was the {n} person wearing?",
            f"ما لون بنطال الشخص {na}؟", oe, oa, 0)
        oe, oa = col_opts(p["h"])
        add(f"What hair color did the {n} person have?",
            f"ما لون شعر الشخص {na}؟", oe, oa, 0)
        wrong_i = pick(rng, list(I_.keys()), p["i"])
        add(f"What was the {n} person carrying?",
            f"ماذا كان يحمل الشخص {na}؟",
            [I_[p["i"]][0]] + [I_[w][0] for w in wrong_i],
            [I_[p["i"]][1]] + [I_[w][1] for w in wrong_i], 0)
        oe, oa = col_opts(p["ic"])
        add(f"What color was the item the {n} person carried?",
            f"ما لون الغرض الذي حمله الشخص {na}؟", oe, oa, 0)
        yes = ["Yes", "نعم"]
        no = ["No", "لا"]
        if p["hat"]:
            add(f"Was the {n} person wearing a hat?", f"هل كان الشخص {na} يرتدي قبعة؟",
                ["Yes", "No"], ["نعم", "لا"], 0)
            oe, oa = col_opts(p["hat"])
            add(f"What color hat was the {n} person wearing?",
                f"ما لون قبعة الشخص {na}؟", oe, oa, 0)
        else:
            add(f"Was the {n} person wearing a hat?", f"هل كان الشخص {na} يرتدي قبعة؟",
                ["No", "Yes"], ["لا", "نعم"], 0)

    for i, v in enumerate(scene["v"], start=1):
        wrong_t = pick(rng, list(V_.keys()), v["t"])
        add(f"What type was vehicle {i} from the left?",
            f"ما نوع المركبة رقم {i} من اليسار؟",
            [V_[v["t"]][0]] + [V_[w][0] for w in wrong_t],
            [V_[v["t"]][1]] + [V_[w][1] for w in wrong_t], 0)
        oe, oa = col_opts(v["c"])
        add(f"What color was vehicle {i}?", f"ما لون المركبة رقم {i}؟", oe, oa, 0)
        plates = [x["pl"] for x in scene["v"]]
        alts = []
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
        k = 0
        while len(alts) < 3 and k < 30:
            k += 1
            s = list(v["pl"])
            j = rng.randrange(len(s))
            s[j] = chars[rng.randrange(len(chars))]
            alt = "".join(s)
            if alt != v["pl"] and alt not in plates and alt not in alts:
                alts.append(alt)
        add(f"What was the plate of vehicle {i}?", f"ما لوحة المركبة رقم {i}؟",
            alts[:2] + [v["pl"]] + alts[2:], alts[:2] + [v["pl"]] + alts[2:], 2)
        if v["d"] == "E":
            add(f"Which way was vehicle {i} heading?", f"في أي اتجاه كانت المركبة رقم {i} تسير؟",
                ["East (right)", "West (left)"], ["شرقًا (يمينًا)", "غربًا (يسارًا)"], 0)
        else:
            add(f"Which way was vehicle {i} heading?", f"في أي اتجاه كانت المركبة رقم {i} تسير؟",
                ["West (left)", "East (right)"], ["غربًا (يسارًا)", "شرقًا (يمينًا)"], 0)
        owners = [j for j, x in enumerate(scene["v"]) if x["pl"] == v["pl"]]
        if len(owners) == 1:
            labels_en = [f"Vehicle {j+1}" for j in range(len(scene["v"]))]
            labels_ar = [f"المركبة {j+1}" for j in range(len(scene["v"]))]
            # 3 options when there are many vehicles: correct, one other, none
            other = (owners[0] + 1) % len(scene["v"])
            add(f"Which vehicle had plate {v['pl']}?", f"أي مركبة كانت لوحتها {v['pl']}؟",
                [f"Vehicle {owners[0]+1}", f"Vehicle {other+1}", "None of them"],
                [f"المركبة {owners[0]+1}", f"المركبة {other+1}", "ولا واحدة"], 0)

    blds = scene["b"]
    for i, b in enumerate(blds):
        names = [x["n"] for x in blds]
        pool = [names[(i + k) % len(names)] for k in range(1, len(names))]
        extra = ["PALI PIZZA", "KONA BANK", "MAKANA BOOKS", "ISLAND GROCERY"]
        for e in extra:
            if e not in names and e not in pool:
                pool.append(e)
        wrong = pool[:3]
        add(f"What was the name of building {i+1} from the left?",
            f"ما اسم المبنى رقم {i+1} من اليسار؟",
            [b["n"]] + wrong, [b["n"]] + wrong, 0)
        # number distractors
        num = b["no"]
        nd = []
        for delta in (10, -10, 100, 1, -1, 11):
            alt = str(int(num) + delta)
            if alt != num and alt not in nd and alt not in [x["no"] for x in blds]:
                nd.append(alt)
        add(f"What number was on {b['n']}?", f"ما الرقم على {b['n']}؟",
            [num, nd[0], nd[1], nd[2]], [num, nd[0], nd[1], nd[2]], 0)
        oe, oa = col_opts(b["c"])
        add(f"What color was {b['n']}?", f"ما لون {b['n']}؟", oe, oa, 0)

    def count_q(stem_en, stem_ar, n, cap):
        opts = [n]
        for d in (1, -1, 2, -2, 3):
            if 0 < n + d <= cap and (n + d) not in opts:
                opts.append(n + d)
            if len(opts) == 4:
                break
        oe = [str(x) for x in opts]
        add(stem_en, stem_ar, oe, oe[:], 0)

    count_q("How many people were in the scene?", "كم شخصًا كان في المشهد؟", len(people), 12)
    count_q("How many vehicles were in the scene?", "كم مركبة كانت في المشهد؟", len(scene["v"]), 8)
    count_q("How many buildings were in the scene?", "كم مبنى كان في المشهد؟", len(blds), 6)
    hats = sum(1 for p in people if p["hat"])
    count_q("How many people were wearing a hat?", "كم شخصًا كان يرتدي قبعة؟", hats, 10)
    east = sum(1 for v in scene["v"] if v["d"] == "E")
    count_q("How many vehicles were heading east?", "كم مركبة كانت تتجه شرقًا؟", east, 8)

    # Who carried a unique item, and the shirt of that person.
    from collections import Counter
    cnt = Counter(p["i"] for p in people)
    for kind, n in cnt.items():
        if n != 1:
            continue
        idx = next(i for i, p in enumerate(people) if p["i"] == kind)
        labels = list(range(len(people)))
        wrong = pick(rng, labels, idx)
        add(f"Who was carrying {I_[kind][0]}?", f"من كان يحمل {I_[kind][1]}؟",
            [f"The {ORD_EN[idx]} person"] + [f"The {ORD_EN[w]} person" for w in wrong],
            [f"الشخص {ORD_AR[idx]}"] + [f"الشخص {ORD_AR[w]}" for w in wrong], 0)
        oe, oa = col_opts(people[idx]["s"])
        add(f"What color shirt was the person carrying {I_[kind][0]} wearing?",
            f"ما لون قميص الشخص الذي كان يحمل {I_[kind][1]}؟", oe, oa, 0)

    # Highest building number, if unique.
    nums = [int(b["no"]) for b in blds]
    if len(set(nums)) == len(nums):
        top = max(range(len(blds)), key=lambda i: nums[i])
        wrong = pick(rng, list(range(len(blds))), top)
        add("Which building had the highest street number?", "أي مبنى كان رقمه هو الأعلى؟",
            [blds[top]["n"]] + [blds[w]["n"] for w in wrong],
            [blds[top]["n"]] + [blds[w]["n"] for w in wrong], 0)

    # Always keep the clock, the signs, and the counts. Then the comparison
    # questions. Fill the rest without repeating a stem.
    must_prefix = (
        "What time did the clock",
        "Which street name",
        "Which cross street",
        "How many people were in",
        "How many vehicles were in",
        "How many buildings",
        "How many people were wearing",
        "How many vehicles were heading",
        "Which building had the highest",
    )
    must, hard, rest = [], [], []
    for item in out:
        if item[0].startswith(must_prefix):
            must.append(item)
        elif item[0].startswith(("Who was carrying", "What color shirt was the person carrying")):
            hard.append(item)
        else:
            rest.append(item)
    rng.shuffle(rest)
    chosen, seen = [], set()
    for item in must + hard + rest:
        if item[0] in seen:
            continue
        seen.add(item[0])
        chosen.append(item)
        if len(chosen) == 45:
            break
    if len(chosen) < 45:
        raise SystemExit(f"{scene['id']}: only {len(chosen)} questions")
    return chosen


def _person(s, p, h, hat, i, ic):
    return {"s": s, "p": p, "h": h, "hat": hat, "i": i, "ic": ic}


def _veh(t, c, pl, d):
    return {"t": t, "c": c, "pl": pl, "d": d}


def _b(n, no, c):
    return {"n": n, "no": no, "c": c}


def street_specs():
    return [
        {
            "id": "L5-1", "lv": 5, "secs": 90,
            "tm": "7:15 AM", "st": "Kalakaua Ave", "cr": "Seaside Ave",
            "b": [_b("REEF SURF", "2190", "blue"), _b("PALM BOOKS", "2196", "yellow"),
                  _b("HONU CAFE", "2204", "green"), _b("TIDE HOTEL", "2212", "pink")],
            "p": [
                _person("orange", "gray", "black", None, "phone", "gray"),
                _person("yellow", "black", "blonde", "green", "box", "green"),
                _person("blue", "brown", "brown", None, "bag", "red"),
                _person("white", "blue", "black", "red", "cup", "white"),
                _person("green", "gray", "brown", None, "umbrella", "purple"),
                _person("pink", "black", "blonde", "yellow", "balloon", "red"),
                _person("purple", "brown", "black", None, "bag", "blue"),
                _person("red", "white", "gray", "black", "phone", "black"),
            ],
            "v": [_veh("taxi", "yellow", "CAB 18", "E"), _veh("car", "white", "HNL 441", "W"),
                  _veh("van", "blue", "KLM 220", "E"), _veh("pickup", "red", "TUV 087", "W"),
                  _veh("car", "black", "NRP 663", "E")],
        },
        {
            "id": "L5-2", "lv": 5, "secs": 90,
            "tm": "6:40 PM", "st": "Ward Ave", "cr": "Auahi St",
            "b": [_b("LANI FISH", "450", "orange"), _b("KOA BANK", "460", "white"),
                  _b("MILO GIFTS", "472", "pink"), _b("NALU GYM", "488", "green")],
            "p": [
                _person("black", "blue", "brown", "white", "box", "brown"),
                _person("yellow", "gray", "black", None, "phone", "white"),
                _person("orange", "black", "blonde", "blue", "cup", "green"),
                _person("blue", "brown", "red", None, "umbrella", "black"),
                _person("white", "green", "black", "orange", "bag", "yellow"),
                _person("green", "gray", "brown", None, "balloon", "pink"),
                _person("red", "black", "blonde", None, "phone", "gray"),
                _person("purple", "blue", "black", "green", "box", "white"),
            ],
            "v": [_veh("pickup", "green", "PLM 190", "W"), _veh("car", "red", "HCX 552", "E"),
                  _veh("taxi", "yellow", "CAB 77", "E"), _veh("van", "white", "JKR 314", "W"),
                  _veh("car", "blue", "LPL 808", "E")],
        },
        {
            "id": "L5-3", "lv": 5, "secs": 90,
            "tm": "11:05 AM", "st": "King St", "cr": "Punchbowl St",
            "b": [_b("ALOHA BAKE", "1018", "yellow"), _b("HALE BOOKS", "1026", "blue"),
                  _b("PONO CAFE", "1034", "white"), _b("KIHEI RX", "1042", "orange")],
            "p": [
                _person("green", "black", "black", None, "bag", "brown"),
                _person("white", "blue", "brown", "red", "phone", "black"),
                _person("yellow", "gray", "blonde", None, "cup", "white"),
                _person("blue", "brown", "black", "yellow", "umbrella", "green"),
                _person("orange", "black", "red", None, "box", "orange"),
                _person("pink", "gray", "brown", None, "balloon", "purple"),
                _person("black", "blue", "blonde", "white", "bag", "black"),
                _person("red", "brown", "black", None, "phone", "blue"),
            ],
            "v": [_veh("car", "gray", "MKA 219", "E"), _veh("van", "green", "KTB 104", "W"),
                  _veh("pickup", "blue", "SDF 773", "E"), _veh("car", "white", "HNL 905", "W"),
                  _veh("taxi", "yellow", "CAB 12", "E")],
        },
    ]


def _fq(en, ar, correct, wrongs, *more):
    if more:
        wrongs = [wrongs, *more]
    oe = [correct[0]] + [w[0] for w in wrongs]
    oa = [correct[1]] + [w[1] for w in wrongs]
    return q(en, ar, oe, oa, 0)


def narrative_scenes():
    """Two incident scenes. The picture and the paragraph match; questions use both."""
    lobby_svg = """<svg viewBox="0 0 800 460" role="img" aria-label="Practice scene" style="width:100%;height:auto;background:#d7ecf7;border-radius:12px;font-family:sans-serif">
<rect x="30" y="40" width="500" height="280" fill="#f4efe6" stroke="#8a7355" stroke-width="3"/>
<rect x="40" y="48" width="220" height="28" fill="#0b3a5b"/><text x="150" y="68" fill="#fff" font-size="16" text-anchor="middle" font-weight="bold">1427 16th Ave</text>
<rect x="270" y="48" width="160" height="28" fill="#185"/><text x="350" y="68" fill="#fff" font-size="14" text-anchor="middle">Kilauea Ave</text>
<circle cx="620" cy="70" r="36" fill="#fff" stroke="#333" stroke-width="3"/>
<line x1="620" y1="70" x2="620" y2="48" stroke="#111" stroke-width="3"/>
<line x1="620" y1="70" x2="636" y2="80" stroke="#111" stroke-width="3"/>
<text x="620" y="122" font-size="16" text-anchor="middle" font-weight="bold">4:20 PM</text>
<rect x="60" y="100" width="70" height="90" fill="#dedede" stroke="#333"/>
<text x="95" y="125" font-size="12" text-anchor="middle">MAIL</text>
<text x="95" y="145" font-size="12" text-anchor="middle">3B</text>
<text x="95" y="165" font-size="12" text-anchor="middle">12A</text>
<rect x="160" y="110" width="80" height="120" fill="#9bb" stroke="#333"/>
<text x="200" y="160" font-size="28" text-anchor="middle" font-weight="bold">2</text>
<text x="200" y="185" font-size="12" text-anchor="middle">ELEVATOR</text>
<rect x="270" y="150" width="90" height="70" fill="#fff" stroke="#c00" stroke-dasharray="4 3"/>
<text x="315" y="180" font-size="12" text-anchor="middle">4C GONE</text>
<text x="315" y="198" font-size="11" text-anchor="middle">DO NOT BEND</text>
<rect x="400" y="120" width="70" height="150" fill="#6b4a2a"/>
<rect x="470" y="200" width="28" height="16" fill="#a33"/>
<text x="430" y="110" font-size="12" text-anchor="middle">FIRE DOOR</text>
<text x="484" y="190" font-size="11">BRICK</text>
<rect x="390" y="250" width="46" height="28" fill="#f4d03f" stroke="#333"/>
<circle cx="400" cy="282" r="8" fill="#333"/><circle cx="428" cy="282" r="8" fill="#333"/>
<text x="413" y="246" font-size="11" text-anchor="middle">BIKE</text>
<ellipse cx="250" cy="250" rx="16" ry="8" fill="#f5f5f5" stroke="#333"/>
<circle cx="266" cy="246" r="5" fill="#f5f5f5" stroke="#333"/>
<text x="250" y="270" font-size="11" text-anchor="middle">DOG</text>
<circle cx="120" cy="230" r="10" fill="#c9956b"/>
<rect x="108" y="240" width="24" height="28" fill="#f7f7f7" stroke="#333"/>
<rect x="108" y="268" width="24" height="22" fill="#222"/>
<rect x="100" y="236" width="40" height="6" fill="#d32f2f"/>
<text x="120" y="214" font-size="11" text-anchor="middle">3B</text>
<rect x="100" y="292" width="18" height="14" fill="#6d4c41"/>
<circle cx="340" cy="230" r="10" fill="#c9956b"/>
<rect x="328" y="240" width="24" height="22" fill="#2e7d32"/>
<rect x="328" y="262" width="24" height="16" fill="#c2a36b"/>
<rect x="326" y="220" width="28" height="6" fill="#fff" stroke="#333"/>
<rect x="352" y="246" width="8" height="14" fill="#444"/>
<text x="340" y="210" font-size="11" text-anchor="middle">12A</text>
<circle cx="520" cy="240" r="10" fill="#c9956b"/>
<rect x="508" y="250" width="24" height="26" fill="#9e9e9e"/>
<rect x="508" y="276" width="10" height="18" fill="#1565c0"/>
<rect x="522" y="276" width="10" height="18" fill="#1565c0"/>
<rect x="534" y="258" width="16" height="12" fill="#111"/>
<rect x="506" y="286" width="12" height="6" fill="#d32f2f"/>
<text x="560" y="250" font-size="18">→</text>
<text x="520" y="228" font-size="11" text-anchor="middle">WEST</text>
<rect x="48" y="300" width="16" height="22" fill="#1565c0"/>
<text x="70" y="316" font-size="12">NOE</text>
<rect x="30" y="340" width="740" height="110" fill="#555"/>
<g><rect x="40" y="360" width="200" height="50" rx="8" fill="#cfd8dc" stroke="#333"/>
<rect x="120" y="392" width="70" height="14" fill="#ffd"/><text x="155" y="404" font-size="12" text-anchor="middle">HNL 640</text>
<text x="140" y="384" font-size="12" text-anchor="middle">SUV driver waiting</text></g>
<g><rect x="280" y="368" width="170" height="44" rx="8" fill="#d32f2f" stroke="#333"/>
<rect x="330" y="394" width="70" height="14" fill="#ffd"/><text x="365" y="406" font-size="12" text-anchor="middle">KXM 218</text>
<text x="365" y="390" font-size="12" text-anchor="middle">empty</text></g>
</svg>"""
    lobby_desc = (
        "Tuesday, 4:20 PM, lobby of 1427 16th Avenue at Kilauea. Study the picture and this paragraph together. A resident in a white blouse, black slacks, and a red scarf (unit 3B) walks in with a brown grocery bag. A man in a green polo, khaki shorts, and a white cap (unit 12A) stands at the mailboxes on a phone. A teenager in a gray hoodie, ripped blue jeans, and red sneakers runs west with a black backpack; the hood hides the face. A package marked 4C — DO NOT BEND was by the door and is gone. Manager NOE, in a blue vest, points at the stairwell. He first says the backpack was blue, then corrects himself: black. A small white dog with no leash is by the elevator, which shows 2. A yellow bicycle is against the rail. Keys with a blue fob are on the counter. Outside: silver SUV plate HNL 640, bearded driver in sunglasses waiting; red compact plate KXM 218, empty. A brick props the fire door.",
        "الثلاثاء، 4:20 مساءً، ردهة 1427 الجادة 16 عند كيلوا. ادراسي الصورة وهذه الفقرة معًا. مقيمة ببلوزة بيضاء وبنطال أسود ووشاح أحمر (الوحدة 3B) تدخل بكيس بقالة بني. رجل بقميص أخضر وشورت كاكي وقبعة بيضاء (الوحدة 12A) عند صناديق البريد على الهاتف. مراهق بقلنسوة رمادية وجينز أزرق ممزق وحذاء أحمر يجري غربًا بحقيبة سوداء؛ القلنسوة تخفي الوجه. طرد مكتوب عليه 4C — DO NOT BEND كان عند الباب واختفى. المدير NOE بسترة زرقاء يشير إلى الدرج. قال أولًا إن الحقيبة زرقاء ثم صحّح: سوداء. كلب أبيض صغير بلا مقود عند المصعد الذي يُظهر 2. دراجة صفراء على السياج. مفاتيح بحلقة زرقاء على المنضدة. في الخارج: دفع رباعي فضي لوحة HNL 640، سائق بلحية ونظارة ينتظر؛ سيارة حمراء لوحة KXM 218 فارغة. طوبة تسند باب الحريق.",
    )
    lobby_qs = [
        _fq("What time was shown?", "ما الوقت الذي ظهر؟", ("4:20 PM", "4:20 م"), [("4:02 PM", "4:02 م"), ("2:40 PM", "2:40 م"), ("4:12 PM", "4:12 م")]),
        _fq("What was the building number?", "ما رقم المبنى؟", ("1427", "1427"), [("1247", "1247"), ("1472", "1472"), ("16", "16")]),
        _fq("Which avenue was the building on?", "في أي جادة كان المبنى؟", ("16th Ave", "الجادة 16"), [("Kilauea Ave", "كيلوا"), ("King St", "كينغ"), ("Piikoi St", "بييكوي")]),
        _fq("Which cross street was on the sign?", "ما الشارع على اللافتة الثانية؟", ("Kilauea Ave", "كيلوا"), [("16th Ave", "الجادة 16"), ("Kalakaua Ave", "كالاناوا"), ("Hotel St", "هوتيل")]),
        _fq("What color was the woman's blouse?", "ما لون بلوزة المرأة؟", ("White", "أبيض"), [("Green", "أخضر"), ("Gray", "رمادي"), ("Red", "أحمر")]),
        _fq("What color were her slacks?", "ما لون بنطالها؟", ("Black", "أسود"), [("Khaki", "كاكي"), ("Blue", "أزرق"), ("White", "أبيض")]),
        _fq("What color was her scarf?", "ما لون وشاحها؟", ("Red", "أحمر"), [("Blue", "أزرق"), ("White", "أبيض"), ("Green", "أخضر")]),
        _fq("What was her unit?", "ما وحدتها؟", ("3B", "3B"), [("12A", "12A"), ("4C", "4C"), ("2", "2")]),
        _fq("What was she carrying in her hand?", "ماذا كانت تحمل في يدها؟", ("A brown grocery bag", "كيس بقالة بني"), [("A black backpack", "حقيبة ظهر سوداء"), ("Keys", "مفاتيح"), ("A phone", "هاتف")]),
        _fq("What color was the man's polo?", "ما لون قميص الرجل؟", ("Green", "أخضر"), [("White", "أبيض"), ("Gray", "رمادي"), ("Blue", "أزرق")]),
        _fq("What color were his shorts?", "ما لون شورت الرجل؟", ("Khaki", "كاكي"), [("Blue", "أزرق"), ("Black", "أسود"), ("Red", "أحمر")]),
        _fq("What color was his cap?", "ما لون قبعته؟", ("White", "أبيض"), [("Red", "أحمر"), ("Black", "أسود"), ("Green", "أخضر")]),
        _fq("What was his unit?", "ما وحدته؟", ("12A", "12A"), [("3B", "3B"), ("4C", "4C"), ("2", "2")]),
        _fq("What was he doing?", "ماذا كان يفعل؟", ("Talking on a phone at the mailboxes", "يتحدث في الهاتف عند صناديق البريد"), [("Running west", "يجري غربًا"), ("Pointing at the stairwell", "يشير إلى الدرج"), ("Driving the SUV", "يقود الدفع الرباعي")]),
        _fq("What color was the teenager's hoodie?", "ما لون قلنسوة المراهق؟", ("Gray", "رمادي"), [("Black", "أسود"), ("Blue", "أزرق"), ("Green", "أخضر")]),
        _fq("What color were his jeans?", "ما لون جينزه؟", ("Blue", "أزرق"), [("Black", "أسود"), ("Khaki", "كاكي"), ("Gray", "رمادي")]),
        _fq("What color were his sneakers?", "ما لون حذائه؟", ("Red", "أحمر"), [("White", "أبيض"), ("Black", "أسود"), ("Blue", "أزرق")]),
        _fq("After the correction, what color was his backpack?", "بعد التصحيح، ما لون حقيبة ظهره؟", ("Black", "أسود"), [("Blue", "أزرق"), ("Gray", "رمادي"), ("Brown", "بني")]),
        _fq("What color did the manager say first?", "ما اللون الذي قاله المدير أولًا؟", ("Blue", "أزرق"), [("Black", "أسود"), ("Gray", "رمادي"), ("Red", "أحمر")]),
        _fq("Which way was the teenager running?", "في أي اتجاه كان المراهق يجري؟", ("West", "غربًا"), [("East", "شرقًا"), ("Up the elevator", "صعودًا بالمصعد"), ("Toward the SUV", "نحو الدفع الرباعي")]),
        _fq("What hid his face?", "ما الذي أخفى وجهه؟", ("The hood", "القلنسوة"), [("A mask on the counter", "قناع على المنضدة"), ("The scarf", "الوشاح"), ("Sunglasses", "نظارة شمسية")]),
        _fq("What had happened to the package?", "ماذا حدث للطرد؟", ("It was gone", "اختفى"), [("It was still by the door", "ما زال عند الباب"), ("The dog was holding it", "الكلب يمسكه"), ("It was in the SUV", "كان في الدفع الرباعي")]),
        _fq("What was written as the package unit?", "ما الوحدة المكتوبة على الطرد؟", ("4C", "4C"), [("3B", "3B"), ("12A", "12A"), ("2", "2")]),
        _fq("What else was written on the package?", "ماذا كُتب أيضًا على الطرد؟", ("DO NOT BEND", "DO NOT BEND"), [("OPEN", "OPEN"), ("FRAGILE GLASS", "زجاج قابل للكسر"), ("NOE", "NOE")]),
        _fq("What was the manager's name tag?", "ماذا على بطاقة المدير؟", ("NOE", "NOE"), [("3B", "3B"), ("HNL", "HNL"), ("KXM", "KXM")]),
        _fq("What color was his vest?", "ما لون سترته؟", ("Blue", "أزرق"), [("Green", "أخضر"), ("Gray", "رمادي"), ("Red", "أحمر")]),
        _fq("Where was he pointing?", "إلى أين كان يشير؟", ("The stairwell", "الدرج"), [("The elevator", "المصعد"), ("The SUV", "الدفع الرباعي"), ("The dog", "الكلب")]),
        _fq("What color was the dog?", "ما لون الكلب؟", ("White", "أبيض"), [("Brown", "بني"), ("Black", "أسود"), ("Yellow", "أصفر")]),
        _fq("Where was the dog?", "أين كان الكلب؟", ("By the elevator", "عند المصعد"), [("In the SUV", "في الدفع الرباعي"), ("On the bicycle", "على الدراجة"), ("In the alley", "في الزقاق")]),
        _fq("Did the dog have a leash?", "هل كان للكلب مقود؟", ("No", "لا"), [("Yes", "نعم"), ("Only a blue fob", "فقط حلقة زرقاء"), ("The paragraph did not say", "الفقرة لم تقل")]),
        _fq("What number did the elevator show?", "ما الرقم الذي أظهره المصعد؟", ("2", "2"), [("3", "3"), ("4", "4"), ("12", "12")]),
        _fq("What color was the bicycle?", "ما لون الدراجة؟", ("Yellow", "أصفر"), [("Red", "أحمر"), ("Blue", "أزرق"), ("Black", "أسود")]),
        _fq("Where was the bicycle?", "أين كانت الدراجة؟", ("Against the rail", "على السياج"), [("In the alley", "في الزقاق"), ("On the elevator", "في المصعد"), ("In the red car", "في السيارة الحمراء")]),
        _fq("Where were the keys?", "أين كانت المفاتيح؟", ("On the counter", "على المنضدة"), [("In the backpack", "في الحقيبة"), ("In the grocery bag", "في كيس البقالة"), ("Under the brick", "تحت الطوبة")]),
        _fq("What color was the key fob?", "ما لون حلقة المفاتيح؟", ("Blue", "أزرق"), [("Red", "أحمر"), ("Yellow", "أصفر"), ("White", "أبيض")]),
        _fq("What plate was on the silver SUV?", "ما لوحة الدفع الرباعي الفضي؟", ("HNL 640", "HNL 640"), [("KXM 218", "KXM 218"), ("NRP 441", "NRP 441"), ("4C", "4C")]),
        _fq("Who was with the silver SUV?", "من كان مع الدفع الرباعي الفضي؟", ("A bearded driver in sunglasses, waiting", "سائق بلحية ونظارة، ينتظر"), [("No one", "لا أحد"), ("The teenager", "المراهق"), ("Manager NOE", "المدير NOE")]),
        _fq("What plate was on the empty red car?", "ما لوحة السيارة الحمراء الفارغة؟", ("KXM 218", "KXM 218"), [("HNL 640", "HNL 640"), ("CAB 77", "CAB 77"), ("PLM 316", "PLM 316")]),
        _fq("Was anyone in the red car?", "هل كان أحد في السيارة الحمراء؟", ("No", "لا"), [("Yes, the woman from 3B", "نعم، المرأة من 3B"), ("Yes, the driver with the beard", "نعم، السائق ذو اللحية"), ("The paragraph did not say", "الفقرة لم تقل")]),
        _fq("What was propping the fire door?", "ما الذي كان يسند باب الحريق؟", ("A brick", "طوبة"), [("The bicycle", "الدراجة"), ("The package", "الطرد"), ("The dog", "الكلب")]),
        _fq("How many people were described inside, not counting the SUV driver?", "كم شخصًا وُصفوا في الداخل، دون سائق الدفع الرباعي؟", ("4", "4"), [("3", "3"), ("5", "5"), ("2", "2")]),
        _fq("Which detail was corrected?", "أي تفصيل صُحّح؟", ("The backpack color", "لون الحقيبة"), ("The time", "الوقت"), ("The woman's unit", "وحدة المرأة"), ("The SUV plate", "لوحة الدفع الرباعي")),
        _fq("What color was the grocery bag?", "ما لون كيس البقالة؟", ("Brown", "بني"), [("Black", "أسود"), ("Yellow", "أصفر"), ("Blue", "أزرق")]),
        _fq("Which person was running?", "من كان يجري؟", ("The teenager in the gray hoodie", "المراهق بالقلنسوة الرمادية"), ("The woman from 3B", "المرأة من 3B"), ("The man from 12A", "الرجل من 12A"), ("Manager NOE", "المدير NOE")),
        _fq("What day was given?", "ما اليوم المذكور؟", ("Tuesday", "الثلاثاء"), [("Wednesday", "الأربعاء"), ("Monday", "الاثنين"), ("No day was given", "لم يُذكر يوم")]),
    ]
    garage_svg = """<svg viewBox="0 0 800 460" role="img" aria-label="Practice scene" style="width:100%;height:auto;background:#cfd8dc;border-radius:12px;font-family:sans-serif">
<rect x="0" y="300" width="800" height="160" fill="#616161"/>
<rect x="80" y="40" width="36" height="250" fill="#f6e27a" stroke="#333"/>
<text x="98" y="80" font-size="22" text-anchor="middle" font-weight="bold">C</text>
<text x="98" y="160" font-size="16" text-anchor="middle">P2</text>
<text x="98" y="200" font-size="14" text-anchor="middle">18</text>
<circle cx="700" cy="60" r="28" fill="#fff" stroke="#333" stroke-width="3"/>
<line x1="700" y1="60" x2="700" y2="42" stroke="#111" stroke-width="3"/>
<line x1="700" y1="60" x2="714" y2="68" stroke="#111" stroke-width="3"/>
<text x="700" y="108" font-size="14" text-anchor="middle" font-weight="bold">11:06 AM</text>
<g><rect x="180" y="330" width="180" height="46" rx="10" fill="#222"/>
<rect x="210" y="312" width="90" height="24" rx="6" fill="#222"/>
<rect x="230" y="360" width="78" height="14" fill="#ffd"/><text x="269" y="372" font-size="12" text-anchor="middle">NRP 441</text>
<text x="300" y="324" font-size="12" fill="#fdd835">DENT</text>
<text x="360" y="300" font-size="18" fill="#fff">→</text></g>
<g><rect x="400" y="360" width="170" height="42" rx="10" fill="#222"/>
<rect x="440" y="386" width="78" height="14" fill="#ffd"/><text x="479" y="398" font-size="12" text-anchor="middle">NRP 414</text>
<text x="479" y="352" font-size="12" fill="#fff" text-anchor="middle">no dent</text></g>
<g><rect x="40" y="400" width="150" height="40" rx="6" fill="#f5f5f5" stroke="#333"/>
<text x="115" y="424" font-size="13" text-anchor="middle">PLB 902</text></g>
<text x="30" y="390" font-size="13" fill="#fff">WEST EXIT</text>
<rect x="560" y="250" width="70" height="40" fill="#ef6c00"/>
<text x="595" y="274" font-size="12" text-anchor="middle">ATTENDANT</text>
<rect x="640" y="300" width="40" height="18" fill="#111"/>
<text x="660" y="294" font-size="11" text-anchor="middle">M 28</text>
<ellipse cx="150" cy="300" rx="22" ry="8" fill="#5d4037"/>
<text x="150" y="286" font-size="11" text-anchor="middle">OIL</text>
<rect x="200" y="230" width="36" height="28" fill="#43a047"/>
<text x="218" y="222" font-size="11" text-anchor="middle">BAG</text>
<rect x="250" y="210" width="30" height="20" fill="#90caf9" stroke="#333"/>
<text x="265" y="204" font-size="11" text-anchor="middle">SEAT</text>
<rect x="430" y="250" width="54" height="22" fill="#fff" stroke="#333"/>
<text x="457" y="266" font-size="12" text-anchor="middle">10:41</text>
<circle cx="250" cy="270" r="9" fill="#c9956b"/>
<rect x="238" y="278" width="24" height="20" fill="#fdd835"/>
<text x="250" y="258" font-size="11" text-anchor="middle">BRAID</text>
<circle cx="470" cy="300" r="9" fill="#c9956b"/>
<rect x="458" y="308" width="24" height="20" fill="#1565c0"/>
<circle cx="330" cy="250" r="9" fill="#c9956b"/>
<rect x="318" y="258" width="24" height="22" fill="#757575"/>
<text x="360" y="250" font-size="16">→</text>
</svg>"""
    garage_desc = (
        "Wednesday, 11:06 AM, parking level P2, yellow pillar C, stall 18. Study the picture and this paragraph together. Black sedan A: plate NRP 441, a dent on the left rear door, driver a woman with a braid and a yellow top, engine running, pointed east. Black sedan B: plate NRP 414, no dent, a man in a blue shirt, parked, engine off. The radio says: disregard 414, the plate is 441. A green shopping bag and a child seat are in a cart by pillar C. An attendant in an orange vest is at the booth. A black motorcycle, plate M 28, is in stall 20. A white van, plate PLB 902, blocks part of the west exit; its driver is not the attendant. An oil spot is in stall 18 under sedan A. A ticket on the ground reads 10:41 AM. The reporting person, in a gray hoodie, points at sedan A.",
        "الأربعاء، 11:06 صباحًا، مستوى الموقف P2، العمود الأصفر C، الموقف 18. ادراسي الصورة وهذه الفقرة معًا. سيدان سوداء أ: لوحة NRP 441، انبعاج في الباب الخلفي الأيسر، سائقة بضفيرة وقميص أصفر، المحرك يعمل، متجهة شرقًا. سيدان سوداء ب: لوحة NRP 414، بلا انبعاج، رجل بقميص أزرق، متوقفة، المحرك مطفأ. اللاسلكي يقول: تجاهلوا 414، اللوحة 441. كيس تسوق أخضر ومقعد طفل في عربة بجانب العمود C. موظف بسترة برتقالية عند الكشك. دراجة نارية سوداء لوحة M 28 في الموقف 20. شاحنة بيضاء لوحة PLB 902 تسد جزءًا من مخرج الغرب؛ سائقها ليس الموظف. بقعة زيت في الموقف 18 تحت السيدان أ. تذكرة على الأرض 10:41 صباحًا. المبلّغ بقلنسوة رمادية يشير إلى السيدان أ.",
    )
    garage_qs = [
        _fq("What time was the scene?", "ما وقت المشهد؟", ("11:06 AM", "11:06 ص"), [("10:41 AM", "10:41 ص"), ("11:40 AM", "11:40 ص"), ("1:06 PM", "1:06 م")]),
        _fq("What time was on the ticket?", "ما الوقت على التذكرة؟", ("10:41 AM", "10:41 ص"), [("11:06 AM", "11:06 ص"), ("10:14 AM", "10:14 ص"), ("4:10 PM", "4:10 م")]),
        _fq("What parking level was it?", "ما مستوى الموقف؟", ("P2", "P2"), [("P1", "P1"), ("C", "C"), ("18", "18")]),
        _fq("What letter was on the yellow pillar?", "ما الحرف على العمود الأصفر؟", ("C", "C"), [("A", "A"), ("B", "B"), ("P", "P")]),
        _fq("What stall number was by the pillar?", "ما رقم الموقف بجانب العمود؟", ("18", "18"), [("20", "20"), ("14", "14"), ("41", "41")]),
        _fq("What color were the two sedans?", "ما لون السيدانين؟", ("Black", "أسود"), [("White", "أبيض"), ("Blue", "أزرق"), ("Yellow", "أصفر")]),
        _fq("Which plate do you keep after the radio correction?", "أي لوحة تبقين بعد تصحيح اللاسلكي؟", ("NRP 441", "NRP 441"), [("NRP 414", "NRP 414"), ("PLB 902", "PLB 902"), ("M 28", "M 28")]),
        _fq("Which plate did the radio tell you to disregard?", "أي لوحة قال اللاسلكي أن تتجاهليها؟", ("NRP 414", "NRP 414"), [("NRP 441", "NRP 441"), ("PLB 902", "PLB 902"), ("M 28", "M 28")]),
        _fq("Which sedan had the dent?", "أي سيدان كان فيها الانبعاج؟", ("Sedan A, plate 441", "السيدان أ، لوحة 441"), ("Sedan B, plate 414", "السيدان ب، لوحة 414"), ("The white van", "الشاحنة البيضاء"), ("Both sedans", "السيدانان معًا")),
        _fq("Where was the dent?", "أين كان الانبعاج؟", ("Left rear door", "الباب الخلفي الأيسر"), ("Front hood", "غطاء المحرك"), ("Right mirror", "المرآة اليمنى"), ("There was no dent", "لم يكن هناك انبعاج")),
        _fq("Who was driving sedan A?", "من كانت تقود السيدان أ؟", ("A woman with a braid", "امرأة بضفيرة"), ("A man in a blue shirt", "رجل بقميص أزرق"), ("The attendant", "الموظف"), ("No one", "لا أحد")),
        _fq("What color was her top?", "ما لون قميصها؟", ("Yellow", "أصفر"), [("Blue", "أزرق"), ("Gray", "رمادي"), ("Orange", "برتقالي")]),
        _fq("Was sedan A's engine running?", "هل كان محرك السيدان أ يعمل؟", ("Yes", "نعم"), ("No", "لا"), ("Only sedan B's engine", "محرك السيدان ب فقط"), ("The paragraph did not say", "الفقرة لم تقل")),
        _fq("Which way was sedan A pointed?", "إلى أين كانت السيدان أ متجهة؟", ("East", "شرقًا"), [("West", "غربًا"), ("Toward the booth only", "نحو الكشك فقط"), ("The paragraph did not say", "الفقرة لم تقل")]),
        _fq("Who was in sedan B?", "من كان في السيدان ب؟", ("A man in a blue shirt", "رجل بقميص أزرق"), ("A woman with a braid", "امرأة بضفيرة"), ("No one", "لا أحد"), ("The attendant", "الموظف")),
        _fq("Was sedan B's engine on?", "هل كان محرك السيدان ب يعمل؟", ("No", "لا"), ("Yes", "نعم"), ("Only if the radio said so", "فقط إذا قال اللاسلكي ذلك"), ("The paragraph did not say", "الفقرة لم تقل")),
        _fq("Did sedan B have a dent?", "هل كان في السيدان ب انبعاج؟", ("No", "لا"), ("Yes, on the left rear door", "نعم، في الباب الخلفي الأيسر"), ("Yes, on the hood", "نعم، على الغطاء"), ("Both cars were dented", "السيارتان منبعجتان")),
        _fq("What color was the shopping bag?", "ما لون كيس التسوق؟", ("Green", "أخضر"), [("Yellow", "أصفر"), ("Blue", "أزرق"), ("White", "أبيض")]),
        _fq("What else was in the cart?", "ماذا أيضًا في العربة؟", ("A child seat", "مقعد طفل"), [("The ticket", "التذكرة"), ("A motorcycle helmet", "خوذة دراجة"), ("The oil bottle", "زجاجة الزيت")]),
        _fq("Where was the cart?", "أين كانت العربة؟", ("By pillar C", "بجانب العمود C"), [("In stall 20", "في الموقف 20"), ("On the west ramp", "على منحدر الغرب"), ("Inside sedan B", "داخل السيدان ب")]),
        _fq("What color was the attendant's vest?", "ما لون سترة الموظف؟", ("Orange", "برتقالي"), [("Yellow", "أصفر"), ("Gray", "رمادي"), ("Blue", "أزرق")]),
        _fq("Where was the attendant?", "أين كان الموظف؟", ("At the booth", "عند الكشك"), [("Driving the van", "يقود الشاحنة"), ("In sedan A", "في السيدان أ"), ("On the motorcycle", "على الدراجة النارية")]),
        _fq("What plate was on the motorcycle?", "ما لوحة الدراجة النارية؟", ("M 28", "M 28"), [("NRP 441", "NRP 441"), ("PLB 902", "PLB 902"), ("NRP 414", "NRP 414")]),
        _fq("What color was the motorcycle?", "ما لون الدراجة النارية؟", ("Black", "أسود"), [("Yellow", "أصفر"), ("White", "أبيض"), ("Orange", "برتقالي")]),
        _fq("Which stall was the motorcycle in?", "في أي موقف كانت الدراجة؟", ("20", "20"), [("18", "18"), ("2", "2"), ("41", "41")]),
        _fq("What plate was on the white van?", "ما لوحة الشاحنة البيضاء؟", ("PLB 902", "PLB 902"), [("NRP 441", "NRP 441"), ("M 28", "M 28"), ("NRP 414", "NRP 414")]),
        _fq("What was the van doing?", "ماذا كانت الشاحنة تفعل؟", ("Blocking part of the west exit", "تسد جزءًا من مخرج الغرب"), [("Pointed east with a dent", "متجهة شرقًا وبانبعاج"), ("Parked in stall 20", "متوقفة في الموقف 20"), ("Driving on King Street", "تسير في شارع كينغ")]),
        _fq("Was the van's driver the attendant?", "هل كان سائق الشاحنة هو الموظف؟", ("No", "لا"), ("Yes", "نعم"), ("Yes, and he wore yellow", "نعم، وكان يلبس أصفر"), ("The paragraph did not say", "الفقرة لم تقل")),
        _fq("Where was the oil spot?", "أين كانت بقعة الزيت؟", ("Stall 18, under sedan A", "الموقف 18، تحت السيدان أ"), [("Under the van", "تحت الشاحنة"), ("On pillar C", "على العمود C"), ("In stall 20", "في الموقف 20")]),
        _fq("What color was the reporting person's hoodie?", "ما لون قلنسوة المبلّغ؟", ("Gray", "رمادي"), [("Yellow", "أصفر"), ("Blue", "أزرق"), ("Orange", "برتقالي")]),
        _fq("Whom did the reporting person point at?", "إلى من أشار المبلّغ؟", ("Sedan A", "السيدان أ"), ("Sedan B", "السيدان ب"), ("The van", "الشاحنة"), ("The attendant", "الموظف")),
        _fq("What day was given?", "ما اليوم المذكور؟", ("Wednesday", "الأربعاء"), [("Tuesday", "الثلاثاء"), ("Monday", "الاثنين"), ("No day was given", "لم يُذكر يوم")]),
        _fq("Which vehicle had the engine running?", "أي مركبة كان محركها يعمل؟", ("Sedan A", "السيدان أ"), ("Sedan B", "السيدان ب"), ("The motorcycle", "الدراجة النارية"), ("Both sedans", "السيدانان معًا")),
        _fq("How many black sedans were described?", "كم سيدان سوداء وُصفت؟", ("2", "2"), [("1", "1"), ("3", "3"), ("4", "4")]),
        _fq("Which exit did the van block?", "أي مخرج سدته الشاحنة؟", ("The west exit", "مخرج الغرب"), [("The east exit", "مخرج الشرق"), ("The elevator", "المصعد"), ("Stall 18", "الموقف 18")]),
        _fq("What color was pillar C?", "ما لون العمود C؟", ("Yellow", "أصفر"), [("Orange", "برتقالي"), ("White", "أبيض"), ("Black", "أسود")]),
        _fq("Who wore the blue shirt?", "من لبس القميص الأزرق؟", ("The man in sedan B", "الرجل في السيدان ب"), ("The woman in sedan A", "المرأة في السيدان أ"), ("The attendant", "الموظف"), ("The reporting person", "المبلّغ")),
        _fq("Which detail did the radio change?", "أي تفصيل غيّره اللاسلكي؟", ("Which plate to keep", "أي لوحة تُبقى"), ("The time on the ticket", "وقت التذكرة"), ("The pillar letter", "حرف العمود"), ("The color of the vest", "لون السترة")),
        _fq("What was under sedan A besides the car itself?", "ماذا تحت السيدان أ غير السيارة نفسها؟", ("An oil spot", "بقعة زيت"), [("The child seat", "مقعد الطفل"), ("The ticket", "التذكرة"), ("The motorcycle", "الدراجة النارية")]),
        _fq("How many plates were given in total?", "كم لوحة ذُكرت في المجموع؟", ("4", "4"), [("2", "2"), ("3", "3"), ("5", "5")]),
        _fq("Which plate is one digit away from the plate you keep?", "أي لوحة تبعد رقمًا واحدًا عن اللوحة التي تبقينها؟", ("NRP 414", "NRP 414"), [("PLB 902", "PLB 902"), ("M 28", "M 28"), ("NRP 441, it is not different", "NRP 441، لا فرق")]),
        _fq("What color was the van?", "ما لون الشاحنة؟", ("White", "أبيض"), [("Black", "أسود"), ("Yellow", "أصفر"), ("Green", "أخضر")]),
        _fq("Where was the green bag relative to the child seat?", "أين الكيس الأخضر بالنسبة إلى مقعد الطفل؟", ("Both were in the cart", "كلاهما في العربة"), [("The bag was in sedan B", "الكيس في السيدان ب"), ("The seat was on the motorcycle", "المقعد على الدراجة"), ("Neither was in the scene", "لا هذا ولا ذاك في المشهد")]),
        _fq("Who points, and at which car?", "من يشير، وإلى أي سيارة؟", ("The person in the gray hoodie, at sedan A", "صاحب القلنسوة الرمادية، إلى السيدان أ"), ("The attendant, at the van", "الموظف، إلى الشاحنة"), ("The woman, at sedan B", "المرأة، إلى السيدان ب"), ("The man in blue, at the motorcycle", "الرجل بالأزرق، إلى الدراجة")),
        _fq("Is 11:06 the time on the ticket?", "هل 11:06 هو الوقت على التذكرة؟", ("No. The ticket says 10:41 AM.", "لا. التذكرة تقول 10:41 صباحًا."), ("Yes", "نعم"), ("The ticket says 11:06 and the scene says 10:41", "التذكرة تقول 11:06 والمشهد 10:41"), ("No ticket was in the scene", "لا تذكرة في المشهد")),
    ]
    # People inside lobby: woman, man 12A, teenager, manager = 4. SUV driver is outside. Question says 4. Good.
    if len(lobby_qs) != 45:
        raise SystemExit(f"lobby {len(lobby_qs)}")
    if len(garage_qs) != 45:
        raise SystemExit(f"garage {len(garage_qs)}")
    return [
        {"id": "L6-1", "lv": 6, "secs": 120, "svg": lobby_svg, "desc": list(lobby_desc), "q": lobby_qs},
        {"id": "L6-2", "lv": 6, "secs": 120, "svg": garage_svg, "desc": list(garage_desc), "q": garage_qs},
    ]


def new_scenes(vocab):
    scenes = []
    for spec in street_specs():
        row = dict(spec)
        row["q"] = street_questions(spec, vocab, seed=spec["id"])
        scenes.append(row)
    scenes.extend(narrative_scenes())
    return scenes


BLURBS = {
    "1": ["Baseline streets. Two storefronts, a few people. Learn the habit of looking.",
          "شوارع الأساس. واجهتان وبضعة أشخاص. هنا تتعلّمين عادة النظر."],
    "2": ["More people and a third vehicle. Same two minutes.",
          "أشخاص أكثر ومركبة ثالثة. الدقيقتان نفسيهما."],
    "3": ["Three storefronts and six people. The page is getting crowded on purpose.",
          "ثلاث واجهات وستة أشخاص. الازدحام مقصود."],
    "4": ["A full curb, then one incident you read and see together.",
          "رصيف ممتلئ، ثم حادثة تقرئينها وترينها معًا."],
    "5": ["New corners. Four storefronts, eight people, five vehicles, and only 90 seconds. Count, compare, and do not linger on what you already know how to see.",
          "زوايا جديدة. أربع واجهات، ثمانية أشخاص، خمس مركبات، و90 ثانية فقط. عُدّي وقارني، ولا تتأخري عند ما صرتِ ترينه بسهولة."],
    "6": ["Incidents with a correction. A detail that was said first is not the detail you keep. This is the observation bar for the last days.",
          "حوادث فيها تصحيح. التفصيل الذي قيل أولًا ليس التفصيل الذي تبقينه. هذا مستوى الملاحظة في الأيام الأخيرة."],
}


if __name__ == "__main__":
    vocab = {"C": C, "I": I, "V": V}
    scenes = new_scenes(vocab)
    for s in scenes:
        print(s["id"], "qs", len(s["q"]), "secs", s["secs"], "svg", "svg" in s)
