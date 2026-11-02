"""Second memory test for every scenario: the same scene, plus details.

Street sketches gain a person, a taxi, and a building, then 45 questions
are built only from that richer scene. Hand-drawn scenes gain a foreground
band (cone, sign, box, cart) and 45 questions that include those details.
"""
from __future__ import annotations

import copy

import hesna_scenes


def _seed(text):
    n = 0
    for ch in text:
        n = (n * 33 + ord(ch)) % 1000003
    return n


def richer_street(scene, vocab):
    s = copy.deepcopy(scene)
    s["id"] = scene["id"] + "-b"
    s["p"] = list(s["p"]) + [{
        "s": "pink", "p": "white", "h": "black", "hat": "orange", "i": "balloon", "ic": "red",
    }]
    s["v"] = list(s["v"]) + [{"t": "taxi", "c": "yellow", "pl": "NEW 880", "d": "E"}]
    added = [{"n": "KIHEI GYM", "no": "880", "c": "purple"}, {"n": "HANA BOOKS", "no": "910", "c": "green"}]
    s["b"] = list(s["b"]) + [added[0]]
    if len(s["b"]) < 4:
        s["b"].append(added[1])
    plates = [v["pl"] for v in scene["v"]]
    names = [b["n"] for b in scene["b"]]
    numbers = [b["no"] for b in scene["b"]]
    if "NEW 880" in plates or any(b["n"] in names or b["no"] in numbers for b in added[:2 if len(scene["b"]) < 3 else 1]):
        raise SystemExit(scene["id"] + " already has the added detail")
    s["q"] = hesna_scenes.street_questions(s, vocab, _seed(s["id"]))
    s["title_en"] = f"Street sketch {scene['id']} · test 2 of 2"
    s["title_ar"] = f"رسم الشارع {scene['id']} · الاختبار 2 من 2"
    s["secs"] = 120
    return s


def _band_svg(svg, spec):
    if 'viewBox="0 0 800 460"' not in svg:
        raise SystemExit("unexpected viewBox")
    svg = svg.replace('viewBox="0 0 800 460"', 'viewBox="0 0 800 540"', 1)
    extra = (
        '<g id="more">'
        '<rect x="0" y="460" width="800" height="80" fill="#cfcfcf"/>'
        f'<polygon points="40,528 58,478 76,528" fill="{spec["cone"]}" stroke="#222" stroke-width="2"/>'
        '<rect x="110" y="486" width="150" height="36" rx="4" fill="#fff" stroke="#222"/>'
        f'<text x="185" y="510" font-size="16" text-anchor="middle" fill="#111" font-weight="bold">{spec["sign"]}</text>'
        '<rect x="290" y="488" width="90" height="34" rx="3" fill="#1e5bd8" stroke="#222"/>'
        f'<text x="335" y="511" font-size="14" text-anchor="middle" fill="#fff" font-weight="bold">{spec["box"]}</text>'
        '<rect x="410" y="492" width="170" height="30" rx="4" fill="#f7f7f7" stroke="#222"/>'
        f'<text x="495" y="513" font-size="14" text-anchor="middle" fill="#111" font-weight="bold">{spec["plate"]}</text>'
        '<text x="680" y="512" font-size="14" text-anchor="middle" fill="#111">white cart</text>'
        '</g>'
    )
    if "</svg>" not in svg:
        raise SystemExit("svg has no close tag")
    return svg.replace("</svg>", extra + "</svg>", 1)


def _tf(en, ar, yes):
    oe = ["A. The statement is true.", "B. The statement is false."]
    oa = ["A. العبارة صحيحة.", "B. العبارة خطأ."]
    return [en, ar, oe, oa, 0 if yes else 1]


def _band_questions(spec):
    cone, sign, box, plate = spec["cone_en"], spec["sign"], spec["box"], spec["plate"]
    wrong_cone = spec["cone_wrong"]
    art = "An" if cone[:1].lower() in "aeiou" else "A"
    rows = [
        _tf(f"{art} {cone} cone is in the foreground.", f"مخروط {spec['cone_ar']} في المقدمة.", True),
        _tf(f"A white sign in the foreground reads {sign}.", f"لافتة بيضاء في المقدمة مكتوب عليها {sign}.", True),
        _tf(f"A blue box in the foreground is labeled {box}.", f"صندوق أزرق في المقدمة مكتوب عليه {box}.", True),
        _tf(f"A white cart in the foreground has plate {plate}.", f"عربة بيضاء في المقدمة لوحتها {plate}.", True),
        _tf("The cone is in the foreground, not on the roof.", "المخروط في المقدمة لا على السطح.", True),
        _tf(f"The foreground sign says {sign}.", f"لافتة المقدمة تقول {sign}.", True),
        _tf("The foreground box is blue.", "صندوق المقدمة أزرق.", True),
        _tf("The foreground cart is white.", "عربة المقدمة بيضاء.", True),
        _tf(f"The cone is {wrong_cone}.", f"المخروط {spec['cone_wrong_ar']}.", False),
        _tf(f"The foreground sign reads {spec['sign_wrong']}.", f"لافتة المقدمة مكتوب عليها {spec['sign_wrong']}.", False),
        _tf(f"The blue box is labeled {spec['box_wrong']}.", f"الصندوق الأزرق مكتوب عليه {spec['box_wrong']}.", False),
        _tf(f"The cart's plate is {spec['plate_wrong']}.", f"لوحة العربة هي {spec['plate_wrong']}.", False),
        _tf("There is no cone in the foreground.", "لا مخروط في المقدمة.", False),
        _tf("The foreground cart is black.", "عربة المقدمة سوداء.", False),
        _tf("The foreground sign is blank.", "لافتة المقدمة فارغة.", False),
    ]
    if len(rows) != 15:
        raise SystemExit("band questions")
    return rows


def richer_svg(scene, spec):
    s = {
        "id": scene["id"] + "-b",
        "lv": scene.get("lv", 6),
        "secs": 120,
        "svg": _band_svg(scene["svg"], spec),
        "desc": [
            "The same scene, with a cone, a sign, a box, and a cart added in front.",
            "المشهد نفسه، مع مخروط ولافتة وصندوق وعربة أُضيفت في المقدمة.",
        ],
        "title_en": f"{scene['id']} · test 2 of 2",
        "title_ar": f"{scene['id']} · الاختبار 2 من 2",
    }
    old = [q for q in scene["q"] if not q[0].startswith("How many")]
    chosen = old[:30]
    if len(chosen) < 30:
        raise SystemExit(scene["id"] + " not enough lasting questions")
    s["q"] = chosen + _band_questions(spec)
    stems = [q[0] for q in s["q"]]
    if len(stems) != 45 or len(set(stems)) != 45:
        raise SystemExit(f"{s['id']} questions {len(stems)} unique {len(set(stems))}")
    return s


_SPECS = {
    "L4-4": {
        "cone": "#fb8c00", "cone_en": "orange", "cone_ar": "برتقالي",
        "cone_wrong": "green", "cone_wrong_ar": "أخضر",
        "sign": "LOT B", "sign_wrong": "LOT Z",
        "box": "KIT 7", "box_wrong": "KIT 1",
        "plate": "HX 440", "plate_wrong": "HX 044",
    },
    "L6-1": {
        "cone": "#fbc02d", "cone_en": "yellow", "cone_ar": "أصفر",
        "cone_wrong": "blue", "cone_wrong_ar": "أزرق",
        "sign": "GATE 2", "sign_wrong": "GATE 9",
        "box": "BAG 4", "box_wrong": "BAG 1",
        "plate": "LM 219", "plate_wrong": "LM 912",
    },
    "L6-2": {
        "cone": "#2e7d32", "cone_en": "green", "cone_ar": "أخضر",
        "cone_wrong": "red", "cone_wrong_ar": "أحمر",
        "sign": "ROW C", "sign_wrong": "ROW Q",
        "box": "BIN 8", "box_wrong": "BIN 3",
        "plate": "QD 552", "plate_wrong": "QD 255",
    },
}


def second_scenes(base_scenes, extra_scenes, vocab):
    """Every original scenario's second test, keyed by id."""
    out = {}
    for scene in base_scenes + extra_scenes:
        if scene.get("p") and scene.get("v") and scene.get("b"):
            nxt = richer_street(scene, vocab)
        elif scene.get("svg") and scene["id"] in _SPECS:
            nxt = richer_svg(scene, _SPECS[scene["id"]])
        else:
            continue
        if not nxt.get("title") and nxt.get("title_en"):
            nxt["title"] = [nxt["title_en"], nxt["title_ar"]]
        out[nxt["id"]] = nxt
    return out
