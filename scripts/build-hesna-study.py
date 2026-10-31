#!/usr/bin/env python3
"""Rebuild Hesna's hidden HPD study guide and memory drills.

Not wired into weekly-sync. The pages stay out of nav, sitemap, and search.

    python3 scripts/build-hesna-study.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import hesna_banks
import hesna_scenes

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study" / "hesna-6abec5.html"
MEM = ROOT / "study" / "hesna-6abec5-memory.html"

BEACON = '<!-- CF-WA:START --><script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "9d4cc1c099e74c1e8b66eb937aa58186"}\'></script><!-- CF-WA:END -->'

PWA = '''<!-- PWA:START --><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#0b3a5b"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Saving Planets"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><!-- PWA:END -->'''

CSS = r'''
body{max-width:1100px;margin:0 auto;padding:1.5rem 1rem 3rem}
.sp-top{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
#sp-toggle{padding:.5rem 1.1rem;border-radius:999px;border:1px solid var(--brand-blue,#2b7bd6);background:transparent;color:inherit;font:inherit;cursor:pointer}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem}
.sp-day{border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:1rem;background:rgba(255,255,255,.04)}
.sp-btn{margin-top:.5rem;padding:.45rem .9rem;border-radius:8px;border:1px solid rgba(255,255,255,.3);background:transparent;color:inherit;font:inherit;cursor:pointer;min-height:44px}
.sp-phase{margin:1.5rem 0}.sp-day h3{margin:0 0 .5rem}.sp-ph{opacity:.85;font-style:italic;margin:0}
html[lang=en] [data-ar],html[lang=ar] [data-en]{display:none}
.sp-nav{position:sticky;top:0;z-index:50;display:flex;gap:.5rem;flex-wrap:wrap;padding:.6rem 0;margin-bottom:.5rem;background:#0b1622;border-bottom:1px solid rgba(255,255,255,.15)}.sp-nav a{padding:.45rem 1rem;border-radius:999px;border:1px solid var(--brand-blue,#2b7bd6);color:inherit;text-decoration:none;font-weight:600}.sp-nav a[aria-current]{background:var(--brand-blue,#2b7bd6);color:#fff}
.hs-ladder{display:flex;flex-wrap:wrap;gap:.35rem;margin:1rem 0}
.hs-ladder span{border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:.2rem .55rem;font-size:.85rem}
.hs-banner{border-inline-start:4px solid #f6c445;padding:.6rem .8rem;background:rgba(246,196,69,.08)}
.hs-opt{display:block;width:100%;text-align:start;margin:.4rem 0;padding:.55rem .7rem;border-radius:8px;border:1px solid rgba(255,255,255,.3);background:transparent;color:inherit;font:inherit;cursor:pointer;min-height:44px}
.hs-stem{font-size:1.05rem}
.hs-passage,.hs-script{border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:.8rem 1rem;background:rgba(255,255,255,.04)}
.hs-board-table{width:100%;border-collapse:collapse;margin:1rem 0}
.hs-board-table th,.hs-board-table td{border-bottom:1px solid rgba(255,255,255,.15);padding:.35rem .4rem;text-align:start}
.md-qs{padding-inline-start:1.2rem}.md-qs li{margin:.6rem 0}.md-ok{border-color:#2e7d32}.md-bad{border-color:#d32f2f}
.md-timer{font-size:1.4rem;font-weight:bold}
'''

LANG = r'''
(function(){var K='hesnaStudyLang',h=document.documentElement;
function set(l){h.lang=l;h.dir=l==='ar'?'rtl':'ltr';try{localStorage.setItem(K,l)}catch(e){}}
var s=null;try{s=localStorage.getItem(K)}catch(e){}set(s==='ar'?'ar':'en');
document.getElementById('sp-toggle').addEventListener('click',function(){set(h.lang==='ar'?'en':'ar')});})();
'''

NAV = '''<nav class="sp-nav" aria-label="Study pages / صفحات الدراسة"><a href="hesna-6abec5.html"{g}><span data-en>📘 Study Guide</span><span data-ar>📘 دليل الدراسة</span></a><a href="hesna-6abec5-memory.html"{m}><span data-en>🧠 Memory Drills</span><span data-ar>🧠 تمارين الذاكرة</span></a></nav>'''


def E(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def bi(en, ar):
    return f'<span data-en>{E(en)}</span><span data-ar>{E(ar)}</span>'


def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


DAYS = [
    dict(n=1, tier=1, depth=1, budgetMin=45, tooFastMin=20, target="measure",
         take=dict(logic=6, grammar=24, reading=1, listen=1),
         en="Day 1 — The photograph",
         ar="اليوم 1 — الصورة",
         body_en="This is a baseline, not a warm-up trophy. Grammar: the traps Arabic and French leave in English, plus a few sentences you may already own. Logic: ordinary items, then four harder probes that find your ceiling. One short reading. One short radio call. Then Memory Level 1. Missing a grammar trap today is the photograph, not a verdict.",
         body_ar="هذا خط أساس، لا كأس إحماء. القواعد: الفخاخ التي تتركها العربية والفرنسية في الإنجليزية، مع جمل قد تملكينها أصلًا. المنطق: بنود عادية، ثم أربعة مجسّات أصعب تكشف سقفكِ. قراءة قصيرة. نداء لاسلكي قصير. ثم المستوى 1 في الذاكرة. إضاعة فخ قواعد اليوم هو الصورة، لا حكم."),
    dict(n=2, tier=2, depth=1, budgetMin=45, tooFastMin=22, target="72%",
         take=dict(logic=10, grammar=8, reading=1, comp=1, listen=1),
         en="Day 2 — First raise",
         ar="اليوم 2 — الرفع الأول",
         body_en="Logic sits one tier above whatever Day 1 proved. If the probes were already easy, today starts higher: that is the plan catching up, not a compliment. Grammar returns only the families you missed. Memory: 80% unlocks Level 2; 95% means leave the rest of Level 1 and start Level 2 now.",
         body_ar="المنطق يعلو مستوى واحدًا فوق ما أثبته اليوم 1. إذا كانت المجسّات سهلة أصلًا، فاليوم يبدأ أعلى: الخطة تلحق بكِ، وهذا ليس مجاملة. القواعد تعود فقط للعائلات التي أضعتِها. الذاكرة: 80% تفتح المستوى 2؛ و95% تعني اتركي بقية المستوى 1 وابدئي المستوى 2 الآن."),
    dict(n=3, tier=3, depth=1, budgetMin=55, tooFastMin=30, target="75%",
         take=dict(logic=16, grammar=8, reading=2, comp=1, listen=1),
         en="Day 3 — The line should move",
         ar="اليوم 3 — يُفترض أن يتحرك الخط",
         body_en="Same grammar families as Day 1, new sentences. The scoreboard should show those families climbing. Logic is now long: lines of people, a rule with an exception, \"must be true.\" This is the first day that should not feel quick. If it does, the system failed, and a harder set opens before you stand up.",
         body_ar="عائلات القواعد نفسها كما في اليوم 1، بجمل جديدة. لوحة النتائج يُفترض أن تُظهر هذه العائلات وهي ترتفع. المنطق الآن طويل: صفوف أشخاص، وقاعدة باستثناء، و«يجب أن يكون صحيحًا». هذا أول يوم لا يُفترض أن يبدو سريعًا. إذا بدا كذلك فقد فشلت المنظومة، وتُفتح مجموعة أصعب قبل أن تقفي."),
    dict(n=4, tier=4, depth=1, budgetMin=60, tooFastMin=32, target="78%",
         take=dict(logic=16, grammar=6, reading=2, comp=1, listen=1),
         en="Day 4 — Slow on purpose",
         ar="اليوم 4 — بطيء عن قصد",
         body_en="A full logic block: two rules that seem to argue, an order that has only one legal sequence, a correction you must not mix back in. Grammar only where Day 3 was still soft. You are not supposed to finish this too fast. Finishing it fast at 90% or better is the plan being late, and the bar moves in the same sitting.",
         body_ar="كتلة منطق كاملة: قاعدتان تبدوان متعارضتين، وترتيب له تسلسل قانوني واحد، وتصحيح لا تخلطينه بالقديم. القواعد فقط حيث بقي اليوم 3 لينًا. لا يُفترض أن تنهي هذا بسرعة. إنهاؤه بسرعة عند 90% أو أفضل يعني أن الخطة تأخّرت، والمستوى يتحرك في الجلسة نفسها."),
    dict(n=5, tier=5, depth=1, budgetMin=50, tooFastMin=28, target="82%",
         take=dict(logic=12, grammar=4, reading=1, comp=1, listen=1),
         en="Day 5 — Hold the new pace",
         ar="اليوم 5 — ثبّتي الإيقاع الجديد",
         body_en="Mixed set at today's tier, which is already past Day 4. Memory Level 3 if you are there; Level 4 if Level 3 was 95% or higher. The point is pace, not a new kind of puzzle for its own sake.",
         body_ar="مجموعة مختلطة في مستوى اليوم، وهو أصلًا بعد اليوم 4. ذاكرة المستوى 3 إذا كنتِ هناك؛ والمستوى 4 إذا كان المستوى 3 بنسبة 95% أو أكثر. المقصود هو الإيقاع، لا نوعًا جديدًا من الألغاز لذاته."),
    dict(n=6, tier=5, depth=2, budgetMin=50, tooFastMin=28, target="84%",
         take=dict(logic=12, grammar=4, reading=1, comp=1),
         en="Day 6 — Judgment, and the harder band of the same tier",
         ar="اليوم 6 — الحكم، والنطاق الأصعب من المستوى نفسه",
         body_en="Bio-data is not a trick. Answer the real form honestly and consistently, and gather the Personal History Statement dates. The scored block is still harder than Day 5: the next band of this tier, not a repeat.",
         body_ar="البيانات الشخصية ليست فخًا. أجيبي عن النموذج الحقيقي بصدق واتساق، واجمعي تواريخ بيان السيرة. والكتلة المحسوبة ما زالت أصعب من اليوم 5: النطاق التالي من هذا المستوى، لا تكرارًا."),
    dict(n=7, tier=5, depth=3, budgetMin=50, tooFastMin=28, target="85%",
         take=dict(logic=12, grammar=4, reading=1, listen=1, comp=1),
         en="Day 7 — Look back at Monday",
         ar="اليوم 7 — انظري إلى الاثنين",
         body_en="One mixed sitting at this week's top band. Then open the scoreboard: Day 1 beside today. That gap is the first half of the change. Fitness, on your own: push-ups, sit-ups, and the 1.5-mile run. The quiz does not grade those.",
         body_ar="جلسة مختلطة واحدة في أعلى نطاق هذا الأسبوع. ثم افتحي لوحة النتائج: اليوم 1 بجانب اليوم. هذه الفجوة هي النصف الأول من التغيّر. اللياقة، لحسابكِ: تمارين الضغط، والبطن، وجري 1.5 ميل. الاختبار لا يقيّمها."),
    dict(n=8, tier=5, depth=3, budgetMin=50, tooFastMin=26, target="87%",
         take=dict(logic=8, grammar=2, listen=1, obs=1),
         en="Day 8 — Eyes",
         ar="اليوم 8 — العينان",
         body_en="New observation scenes: Memory Level 5 is 90 seconds, four storefronts, eight people. This page adds a covered incident of its own. A short logic hold so memory does not crowd the other skills out. 95% on a Level 5 scene means Level 6 is next, not another easy corner.",
         body_ar="مشاهد ملاحظة جديدة: المستوى 5 في الذاكرة 90 ثانية، أربع واجهات، ثمانية أشخاص. وهذه الصفحة تضيف حادثة تُغطى. إمساك قصير بالمنطق حتى لا تزاحم الذاكرة المهارات الأخرى. 95% في مشهد من المستوى 5 تعني أن المستوى 6 هو التالي، لا زاوية سهلة أخرى."),
    dict(n=9, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="88%",
         take=dict(logic=10, grammar=4, reading=2, comp=1),
         en="Day 9 — Read at exam pace",
         ar="اليوم 9 — اقرئي بإيقاع الامتحان",
         body_en="Passages. Once you are answering, about 40 seconds a question is the exam's average (169 questions in 120 minutes is about 43 seconds). Ask what the passage states, and what it does not. Grammar only on families still under 80%.",
         body_ar="مقاطع. حين تجيبين، نحو 40 ثانية للسؤال هو متوسط الامتحان (169 سؤالًا في 120 دقيقة يعني نحو 43 ثانية). اسألي ماذا يذكر المقطع، وماذا لا يذكر. القواعد فقط للعائلات التي ما زالت تحت 80%."),
    dict(n=10, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="90%",
         take=dict(logic=8, grammar=8, reading=1),
         en="Day 10 — A sentence a sergeant can use",
         ar="اليوم 10 — جملة يستطيع الرقيب استخدامها",
         body_en="Grammar and phrasing in report register: one sentence is correct, three are not. On paper, write a six-line incident (who, what, when, where, direction, correction) and read it against the sentences you just judged. Do not drill a family the scoreboard has retired.",
         body_ar="القواعد والصياغة في لغة التقرير: جملة واحدة صحيحة وثلاث ليست كذلك. على الورق، اكتبي حادثة من ستة أسطر (من، ماذا، متى، أين، الاتجاه، التصحيح) واقرئيها مقابل الجمل التي حكمتِ عليها. لا تدرّبي عائلة أوقفتها لوحة النتائج."),
    dict(n=11, tier=6, depth=2, budgetMin=50, tooFastMin=28, target="92%",
         take=dict(logic=14, grammar=4, comp=1, reading=1),
         en="Day 11 — Which rule wins",
         ar="اليوم 11 — أي قاعدة تفوز",
         body_en="Procedures. Two rules seem to apply; one governs. Pick the next step, not the step that sounds busy. This band is harder than Day 10 even though both sit on tier 6.",
         body_ar="إجراءات. قاعدتان تبدوان منطبقتين؛ وواحدة تحكم. اختاري الخطوة التالية، لا الخطوة التي تبدو مشغولة. هذا النطاق أصعب من اليوم 10 رغم أن كليهما في المستوى 6."),
    dict(n=12, tier=6, depth=3, budgetMin=70, tooFastMin=40, target="94%",
         take=dict(logic=12, grammar=6, reading=1, comp=1, listen=1, obs=1),
         en="Day 12 — Dress rehearsal",
         ar="اليوم 12 — بروفة",
         body_en="All pillars, one sitting, including a new observation scenario with a correction. Mark only what is still soft. 98% with time left means Day 13 is the stretch bank, not a review of what you already command.",
         body_ar="كل الأعمدة، في جلسة واحدة، ومنها مشهد ملاحظة جديد فيه تصحيح. علّمي فقط ما يزال لينًا. 98% مع وقت متبقٍّ تعني أن اليوم 13 هو بنك التمدد، لا مراجعة ما تملكينه أصلًا."),
    dict(n=13, tier=6, depth=3, budgetMin=45, tooFastMin=24, target="96%", mode="repair",
         take=dict(logic=8, grammar=8, listen=1, obs=1),
         stretchTake=dict(logic=8, grammar=4, listen=1, obs=1),
         en="Day 13 — Soft spots, or the stretch",
         ar="اليوم 13 — المواضع اللينة، أو التمدد",
         body_en="If anything is under 95%, today is only that. If nothing is, the system failed by being too easy: the stretch bank loads. Fitness, on your own: agility run and the 300-meter run. Not scored here.",
         body_ar="إذا بقي شيء تحت 95% فاليوم له فقط. إذا لم يبقَ شيء فقد فشلت المنظومة لأنها كانت سهلة: يُحمَّل بنك التمدد. اللياقة، لحسابكِ: جري الرشاقة وجري 300 متر. لا يُحسبان هنا."),
    dict(n=14, tier=6, depth=3, budgetMin=35, tooFastMin=18, target="98%", mode="capstone",
         take=dict(logic=8, grammar=4, reading=1, listen=1),
         en="Day 14 — The photograph, beside today",
         ar="اليوم 14 — الصورة، بجانب اليوم",
         body_en="If Day 13 cleared, today is short and sharp, then you stop. Put Day 1 beside Day 14. The aim of these two weeks is about 98% on this kind of page, with a rested mind, before the Honolulu exam. If Day 13 did not clear, today is the weak bank, not a day off. Bring what HPD's own instructions list; this page does not guess the packing list.",
         body_ar="إذا اجتزتِ اليوم 13 فاليوم قصير وحاد، ثم تتوقفين. ضعي اليوم 1 بجانب اليوم 14. هدف هذين الأسبوعين نحو 98% على صفحة من هذا النوع، بعقل مرتاح، قبل امتحان هونولولو. إذا لم يُجتز اليوم 13 فاليوم هو بنك الضعف، لا يوم راحة. أحضري ما تذكره تعليمات الشرطة نفسها؛ هذه الصفحة لا تخمّن قائمة الأمتعة."),
]


def study_html(payload):
    w1, w2 = [], []
    for d in DAYS:
        jump = bi(
            f"If too easy → jump tier. Target {d['target']}. Budget {d['budgetMin']} min. Too fast: under {d['tooFastMin']} min with a high core score.",
            f"إذا كان أسهل مما ينبغي → اقفزي مستوى. الهدف {d['target']}. الميزانية {d['budgetMin']} د. سريع أكثر من اللازم: أقل من {d['tooFastMin']} د مع جوهر مرتفع.",
        )
        c = (
            f'<article class="sp-day" id="day-{d["n"]}"><h3>{bi(d["en"], d["ar"])}</h3>'
            f'<p>{bi(d["body_en"], d["body_ar"])}</p><p class="sp-ph">{jump}</p>'
            f'<button type="button" class="sp-btn" data-day="{d["n"]}">{bi("Start this day", "ابدئي هذا اليوم")}</button></article>'
        )
        (w1 if d["n"] <= 7 else w2).append(c)
    ladder = "".join(
        f'<span>{bi("D"+str(d["n"])+" · t"+str(d["tier"]), "ي"+str(d["n"])+" · م"+str(d["tier"]))}</span>'
        for d in DAYS
    )
    rules = f'''<section><h2>{bi("How the bar moves", "كيف يتحرك المستوى")}</h2>
<p>{bi("Overachievement is a failure of this plan. The next demand is always past today's, and a sitting that is too easy raises the tier before you close the laptop.",
"التفوّق الزائد فشل لهذه الخطة. الطلب التالي يتجاوز اليوم دائمًا، والجلسة السهلة أكثر من اللازم ترفع المستوى قبل أن تغلقي الحاسوب.")}</p>
<ul>
<li>{bi("The core is logic, reading, listening, comprehension, and observation. Grammar is a separate track.", "الجوهر هو المنطق والقراءة والاستماع والفهم والملاحظة. والقواعد مسار منفصل.")}</li>
<li>{bi("Core under 70%: the next day still changes the work, and it opens with a short bridge so a miss is not a wall.", "جوهر تحت 70%: اليوم التالي يغيّر العمل رغم ذلك، ويبدأ بجسر قصير حتى لا يصير التعثّر جدارًا.")}</li>
<li>{bi("Core 70–94%: you are on the day's pace. Tomorrow is already a higher demand, even when today felt fair.", "جوهر 70–94%: أنتِ على إيقاع اليوم. وغدًا أصلًا طلب أعلى، حتى لو بدا اليوم عادلًا.")}</li>
<li>{bi("Core 95% or higher, or core 90%+ finished under the too-fast time: too easy. A harder set opens in this sitting. If that set sticks (80%+), tomorrow jumps an extra tier.", "جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في زمن أقصر من حد السرعة: أسهل مما ينبغي. تُفتح مجموعة أصعب في هذه الجلسة. إذا ثبتت (80% أو أكثر) فغدًا يقفز مستوى إضافيًا.")}</li>
<li>{bi("Day 1 probes: 3 of 4 harder probes right, with the ordinary core at 85%+, already counts as too easy. The grammar traps may still be soft. That is allowed.", "مجسّات اليوم 1: ثلاثة من أربعة مجسّات أصعب صحيحة، مع جوهر عادي عند 85% أو أكثر، تُحسب أصلًا أسهل مما ينبغي. فخاخ القواعد قد تبقى لينة. وهذا مسموح.")}</li>
<li>{bi("Grammar drills the families under 80%. A family at 95% across 4 or more items is retired. Day 3 rescores Day 1's soft families on new sentences, so the rise is visible.", "القواعد تدرّب العائلات تحت 80%. والعائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف. واليوم 3 يعيد قياس عائلات اليوم 1 اللينة بجمل جديدة، فيظهر الارتفاع.")}</li>
<li>{bi("Memory: 80% unlocks the next level. 95% means the rest of that level is optional review and the next level is the one that counts.", "الذاكرة: 80% تفتح المستوى التالي. و95% تعني أن بقية ذلك المستوى مراجعة اختيارية، والمستوى التالي هو الذي يُحسب.")}</li>
<li>{bi("End state for the two weeks: about 98% on this kind of page. Harder items, not a softer key.", "حالة نهاية الأسبوعين: نحو 98% على صفحة من هذا النوع. بنود أصعب، لا مفتاح أسهل.")}</li>
</ul></section>'''
    about = f'''<section><h2>{bi("About the HPD exam", "عن امتحان شرطة هونولولو")}</h2>
<p>{bi("HPD's Metropolitan Police Recruit entrance exam: 169 multiple-choice questions in 2 hours. Sections: Observation and Memory, Written Communication, Reading/Understanding, Reasoning/Analytical Ability, and Bio-Data. Passing score: 70. If you score below 70 you may re-apply and retake it after 6 months. Math is not listed as a section.",
"امتحان القبول لمجنّد شرطة هونولولو: 169 سؤالًا من نوع الاختيار من متعدد خلال ساعتين. الأقسام: الملاحظة والذاكرة، والتواصل الكتابي، والقراءة والفهم، والاستدلال والقدرة التحليلية، والبيانات الشخصية (Bio-Data). درجة النجاح: 70. من يحصل على أقل من 70 يمكنه إعادة التقديم والامتحان بعد 6 أشهر. الرياضيات ليست قسمًا مذكورًا.")}</p>
<p>{bi("Not published by HPD: points per section, how the 70 is calculated, or real sample questions. HPD links its own Entrance Exam study guide from the Application Process page. Read it first. Nothing on this page is an official item.",
"غير منشور من الشرطة: درجات كل قسم، أو طريقة حساب الـ 70، أو أسئلة نموذجية حقيقية. الشرطة تربط دليلها للدراسة من صفحة إجراءات التقديم. اقرئيه أولًا. لا شيء في هذه الصفحة سؤال رسمي.")}</p>
<p>{bi("Physical Readiness Assessment (on-island recruits), all events must be passed: Agility Run 21.6 s · 300-meter run 82.8 s · 24 push-ups · 24 sit-ups in 1 minute · 1.5-mile run in 21 minutes. Academy graduation standards are higher.",
"تقييم الجاهزية البدنية (للمجنّدين داخل الجزيرة)، يجب اجتياز كل الاختبارات: جري الرشاقة 21.6 ث · جري 300 متر 82.8 ث · 24 تمرين ضغط · 24 تمرين بطن في دقيقة · جري 1.5 ميل في 21 دقيقة. معايير التخرج من الأكاديمية أعلى.")}</p>
<p>{bi("After the PRA: Personal History Statement, background investigation, clarification interview, psychological exam/interview, polygraph, and medical exam.",
"بعد تقييم الجاهزية: بيان السيرة الشخصية، والتحقيق في الخلفية، ومقابلة التوضيح، والاختبار/المقابلة النفسية، وجهاز كشف الكذب، والفحص الطبي.")}</p>
<p>{bi("How other departments test: NYPD uses a 70% pass mark and tests memorization, written comprehension and expression, deductive and inductive reasoning, information ordering, problem sensitivity, and spatial skills. California's PELLETB (accepted by LAPD at a T-score of 42+) tests reading and writing. Shared best practice: timed practice, reading carefully, and clear, correct sentences.",
"كيف تختبر إدارات أخرى: شرطة نيويورك تعتمد 70% وتختبر الحفظ، والفهم والتعبير الكتابي، والاستدلال الاستنباطي والاستقرائي، وترتيب المعلومات، وحساسية المشكلة، والمهارات المكانية. واختبار كاليفورنيا PELLETB (تقبله شرطة لوس أنجلوس عند درجة T قدرها 42 أو أكثر) يختبر القراءة والكتابة. الممارسة المشتركة: تدريب موقوت، وقراءة دقيقة، وجمل واضحة صحيحة.")}</p>
<p>{bi("English is your third language. Arabic and French already gave you two full grammars. This page does not reteach English from zero. It finds the transfer habits that still show up in a report sentence, and it leaves alone what you already command.",
"الإنجليزية لغتكِ الثالثة. العربية والفرنسية أعطتاكِ نحوين كاملين أصلًا. هذه الصفحة لا تعيد تعليم الإنجليزية من الصفر. إنها تجد عادات النقل التي ما زالت تظهر في جملة تقرير، وتترك ما تملكينه.")}</p>
</section>'''
    facts = f'''<section><h2>{bi("Know these cold", "احفظي هذه")}</h2>
<p class="sp-ph">{bi("These are public facts about the process, not scored by the adaptive bar. Confirm them with HPD before exam day.",
"هذه وقائع علنية عن الإجراءات، ولا يحسبها شريط الصعوبة. أكّديها مع الشرطة قبل يوم الامتحان.")}</p>
<ul>
<li>{bi("169 multiple-choice questions, 2 hours, about 43 seconds each.", "169 سؤال اختيار من متعدد، ساعتان، نحو 43 ثانية لكل سؤال.")}</li>
<li>{bi("Five sections: Observation and Memory; Written Communication; Reading/Understanding; Reasoning/Analytical Ability; Bio-Data.", "خمسة أقسام: الملاحظة والذاكرة؛ التواصل الكتابي؛ القراءة والفهم؛ الاستدلال والقدرة التحليلية؛ البيانات الشخصية.")}</li>
<li>{bi("Passing score 70. Below 70: re-apply after 6 months.", "درجة النجاح 70. أقل من 70: إعادة التقديم بعد 6 أشهر.")}</li>
<li>{bi("PRA, on-island: agility 21.6 s; 300 m in 82.8 s; 24 push-ups; 24 sit-ups in 1 min; 1.5 miles in 21 min.", "الجاهزية البدنية داخل الجزيرة: رشاقة 21.6 ث؛ 300 م في 82.8 ث؛ 24 ضغط؛ 24 بطن في دقيقة؛ 1.5 ميل في 21 د.")}</li>
</ul></section>'''
    sources = '''<section><h2><span data-en>Sources</span><span data-ar>المصادر</span></h2><ul>
<li><a href="https://www.joinhonolulupd.org/application-process.html" rel="noopener nofollow">JOIN HPD: Application Process</a></li>
<li><a href="https://www.joinhonolulupd.org/pra-instructions.html" rel="noopener nofollow">JOIN HPD: PRA Instructions</a></li>
<li><a href="https://www.governmentjobs.com/careers/honolulupd/jobs/3347241/metropolitan-police-recruit-on-island" rel="noopener nofollow">HPD job posting: Metropolitan Police Recruit (GovernmentJobs)</a></li>
<li><a href="https://a856-exams.nyc.gov/OASysWeb/noe/20277311000.pdf" rel="noopener nofollow">NYC DCAS: Police Officer Notice of Examination</a></li>
<li><a href="https://post.ca.gov/LE-entry-level-test-battery-agency-faqs-2026" rel="noopener nofollow">California POST: PELLETB FAQs</a></li>
<li><a href="https://www.joinlapd.com/step-2-multiple-choice-test" rel="noopener nofollow">LAPD: Step 2 Multiple Choice Test</a></li>
</ul><p class="sp-ph"><span data-en>Exam facts checked Oct 28, 2026. Practice added Oct 31, 2026. Always confirm details with HPD before the exam.</span><span data-ar>وقائع الامتحان رُوجعت في 28 أكتوبر 2026. والتدريب أُضيف في 31 أكتوبر 2026. تأكّدي دائمًا من التفاصيل مع الشرطة قبل الامتحان.</span></p></section>'''
    adapt = (ROOT / "scripts" / "hesna_adapt.js").read_text()
    run = (ROOT / "scripts" / "hesna_run.js").read_text()
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr" class="dark">
<head>
<meta charset="UTF-8"><meta name="color-scheme" content="dark"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>Study Plan | خطة الدراسة</title>
<link rel="stylesheet" href="/styles.css?v=20261026b">
{PWA}
<style>{CSS}</style>
</head>
<body>
<main data-pagefind-ignore="all">
{NAV.format(g=' aria-current="page"', m='')}
<div class="sp-top"><h1>{bi("Hesna's Two-Week HPD Study Plan", "خطة حسنة الدراسية لامتحان شرطة هونولولو (أسبوعان)")}</h1><button id="sp-toggle" type="button" aria-label="Switch language / تغيير اللغة"><span data-en>العربية</span><span data-ar>English</span></button></div>
<p class="sp-ph">{bi("Private study page. Practice questions are original and are not real exam items.", "صفحة دراسة خاصة. أسئلة التدريب من إعدادنا وليست أسئلة امتحان حقيقية.")}</p>
<p>{bi("Day 1 is a photograph of how you reason, and of where English sits beside Arabic and French. Day 14 should make that photograph look like a different test-taker. The work gets harder every day on purpose, and it gets harder again the moment a day is too easy. The aim, walking into the Honolulu exam, is about 98% on this kind of page.",
"اليوم 1 صورة لطريقة استدلالكِ، ولموقع الإنجليزية بجانب العربية والفرنسية. واليوم 14 يُفترض أن يجعل تلك الصورة تبدو لشخص آخر يدخل الاختبار. العمل يصعب كل يوم عن قصد، ويصعب مرة أخرى لحظة يكون اليوم أسهل مما ينبغي. الهدف، وأنتِ داخلة إلى امتحان هونولولو، نحو 98% على صفحة من هذا النوع.")}</p>
<div class="hs-ladder" aria-hidden="true">{ladder}</div>
{rules}
{about}
<section class="sp-week"><h2>{bi("Week 1", "الأسبوع الأول")}</h2><div class="sp-grid">{''.join(w1)}</div></section>
<section class="sp-week"><h2>{bi("Week 2", "الأسبوع الثاني")}</h2><div class="sp-grid">{''.join(w2)}</div></section>
<p><a class="sp-btn" href="hesna-6abec5-memory.html">{bi("Observation & Memory drills (scenes, including new Level 5 and Level 6 incidents)", "تمارين الملاحظة والذاكرة (مشاهد، ومنها حوادث جديدة في المستويين 5 و6)")}</a></p>
<div id="hs-board"></div>
<div id="hs-app"></div>
<p><button type="button" class="sp-btn" id="hs-reset">{bi("Reset saved plan progress", "امسحي تقدّم الخطة المحفوظ")}</button></p>
{facts}
{sources}
</main>
<script>window.HS={payload};</script>
<script>{adapt}</script>
<script>{run}</script>
<script>{LANG}</script>
{BEACON}
</body>
</html>
'''


def memory_html():
    base = json.loads((ROOT / "scripts" / "hesna_memory_base.json").read_text())
    vocab = {"C": base["C"], "I": base["I"], "V": base["V"]}
    extra = hesna_scenes.new_scenes(vocab)
    data = {
        "S": base["S"] + extra,
        "C": base["C"], "I": base["I"], "V": base["V"], "BC": base["BC"],
        "BLURB": hesna_scenes.BLURBS,
    }
    raw = (ROOT / "scripts" / "hesna_memory_shell.html").read_text()
    raw = re.sub(
        r"window\.MD_DATA=\{.*?\};\s*</script>",
        lambda m: "window.MD_DATA=" + js(data) + ";</script>",
        raw, count=1, flags=re.S,
    )
    old_intro = re.search(r'<p class="sp-ph">.*?</p>', raw, flags=re.S)
    if not old_intro:
        raise SystemExit("intro missing")
    new_intro = '<p class="sp-ph">' + bi(
        "Original practice scenes, not real HPD exam items. Levels 1–4 are the streets you already have. Level 5 is new: four storefronts, eight people, five vehicles, 90 seconds. Level 6 is new: an incident with a correction, picture and paragraph together. Study the scene, then it hides. Score 80% to unlock the next level. Score 95% or higher and that level is done: what remains on it is optional review, and the next level is the one that counts. Progress stays in this browser.",
        "مشاهد تدريب من إعدادنا، وليست من امتحان شرطة هونولولو. المستويات 1–4 هي الشوارع التي عندكِ. المستوى 5 جديد: أربع واجهات، ثمانية أشخاص، خمس مركبات، 90 ثانية. والمستوى 6 جديد: حادثة فيها تصحيح، صورة وفقرة معًا. ادراسي المشهد ثم يختفي. 80% تفتح المستوى التالي. 95% أو أكثر تعني أن المستوى انتهى: ما يبقى فيه مراجعة اختيارية، والمستوى التالي هو الذي يُحسب. التقدّم يبقى في هذا المتصفح.",
    ) + '</p>'
    raw = raw[:old_intro.start()] + new_intro + raw[old_intro.end():]
    old = "bi('45 questions · 2-minute view','45 سؤالًا · مشاهدة لمدة دقيقتين')"
    new = "bi(s.q.length+' questions · ',' '+s.q.length+' سؤالًا · ')+mins(s)"
    if old not in raw:
        raise SystemExit("card line missing")
    raw = raw.replace(old, new, 1)
    helper = """function mins(s){if(s.secs%60===0){var m=s.secs/60;return bi(m===1?'1-minute view':m+'-minute view', m===2?'مشاهدة لمدة دقيقتين':'مشاهدة لمدة '+m+' دقائق');}return bi(s.secs+'-second view','مشاهدة لمدة '+s.secs+' ثانية');}
function firstOf(lv){for(var i=0;i<D.S.length;i++)if(D.S[i].lv===lv)return i;return -1;}
function hotLevel(lv){return D.S.some(function(s){return s.lv==lv&&(st[s.id]||0)>=95});}
"""
    raw = raw.replace("function home(){", helper + "function home(){", 1)
    old_h = "o+='<section class=\"sp-phase\"><h2>'+bi('Level '+lv,'المستوى '+lv)+'</h2>'+"
    new_h = (
        "var bl=D.BLURB&&D.BLURB[String(lv)];"
        "o+='<section class=\"sp-phase\"><h2>'+bi('Level '+lv,'المستوى '+lv)+'</h2>'+"
        "(bl?'<p>'+bi(bl[0],bl[1])+'</p>':'')+"
        "(hotLevel(lv)?'<p class=\"sp-ph\">'+bi('95% or higher on this level: the rest is optional review. The next level is the one that counts.','95% أو أكثر في هذا المستوى: الباقي مراجعة اختيارية. المستوى التالي هو الذي يُحسب.')+'</p>':'')+"
    )
    if old_h not in raw:
        raise SystemExit("level header missing")
    raw = raw.replace(old_h, new_h, 1)
    old_msg = "(p>=80?bi('Passed! The next level is unlocked if there is one.','نجحتِ! يُفتح المستوى التالي إن وُجد.'):bi('Not yet 80%. Review below and try again.','لم تصلي إلى 80% بعد. راجعي الإجابات أدناه وحاولي مرة أخرى.'))"
    new_msg = "(p>=95?bi('95% or higher: this tier was too easy. The next level is the one that counts. Same-level repeats are optional review.','95% أو أكثر: هذا المستوى كان أسهل مما ينبغي. المستوى التالي هو الذي يُحسب. تكرار المستوى نفسه مراجعة اختيارية.'):(p>=80?bi('Passed. The next level is unlocked if there is one.','نجحتِ. يُفتح المستوى التالي إن وُجد.'):bi('Not yet 80%. Review below and try again.','لم تصلي إلى 80% بعد. راجعي الإجابات أدناه وحاولي مرة أخرى.')))"
    if old_msg not in raw:
        raise SystemExit("result message missing")
    raw = raw.replace(old_msg, new_msg, 1)
    # jump button after the first back button
    old_btn = "'</p><button type=\"button\" class=\"sp-btn\" data-home=\"1\">'+bi('Back to levels','العودة إلى المستويات')+'</button><div>'+scene(s)"
    new_btn = "'</p>'+(p>=95&&firstOf(s.lv+1)>=0?'<button type=\"button\" class=\"sp-btn\" data-go=\"'+firstOf(s.lv+1)+'\">'+bi('Start the next level','ابدئي المستوى التالي')+'</button>':'')+'<button type=\"button\" class=\"sp-btn\" data-home=\"1\">'+bi('Back to levels','العودة إلى المستويات')+'</button><div>'+scene(s)"
    if old_btn not in raw:
        raise SystemExit("result button missing")
    raw = raw.replace(old_btn, new_btn, 1)
    return raw


def main():
    stats = hesna_banks.check_banks()
    reads, comps, listens, obs = hesna_banks.passages()
    items = hesna_banks.all_items()
    # Drop callables; items are plain dicts.
    days = []
    for d in DAYS:
        row = {k: d[k] for k in ("n", "tier", "depth", "budgetMin", "tooFastMin", "take") if k in d}
        if d.get("mode"):
            row["mode"] = d["mode"]
        if d.get("stretchTake"):
            row["stretchTake"] = d["stretchTake"]
        days.append(row)
    payload = js({
        "days": days,
        "items": items,
        "reads": reads,
        "comps": comps,
        "listens": listens,
        "obs": obs,
    })
    STUDY.write_text(study_html(payload), encoding="utf-8")
    MEM.write_text(memory_html(), encoding="utf-8")
    print("wrote", STUDY, STUDY.stat().st_size)
    print("wrote", MEM, MEM.stat().st_size)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
