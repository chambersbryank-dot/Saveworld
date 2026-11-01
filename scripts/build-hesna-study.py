#!/usr/bin/env python3
"""Rebuild Hesna's hidden HPD study guide and memory drills.

Not wired into weekly-sync. The pages stay out of nav, sitemap, and search.

    python3 scripts/build-hesna-study.py
"""
from __future__ import annotations

import json
from pathlib import Path

import hesna_banks
import hesna_photo
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
.hs-key{border-inline-start:4px solid #2b7bd6;padding:.5rem .7rem;margin:.4rem 0}
.si-credit{display:block;font-size:.75rem;line-height:1.3;opacity:.85;font-style:italic;margin:.25rem 0 0}
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
         take=dict(logic=6, grammar=24, reading=1, listen=1, ab=8),
         en="Day 1 — The photograph",
         ar="اليوم 1 — الصورة",
         body_en="This is a baseline, not a warm-up trophy. Written A/B: correct or incorrect, the way the exam asks, plus the transfer traps Arabic and French leave in English. One short reading, and the passage stays visible. Then picture quiz 1, the 7426 burglary: 2 minutes, then it hides. Logic probes and the radio call are extra practice, not a fifth section. Missing a trap today is the photograph, not a verdict.",
         body_ar="هذا خط أساس، لا كأس إحماء. كتابة A/B: صح أو خطأ، كما في الامتحان، مع فخاخ النقل من العربية والفرنسية. قراءة قصيرة يبقى مقطعها ظاهرًا. ثم الاختبار 1 لصورة السطو 7426: دقيقتان ثم تختفي. المنطق والنداء اللاسلكي تدريب إضافي، لا قسمًا خامسًا. إضاعة فخ اليوم هو الصورة، لا حكم."),
    dict(n=2, tier=2, depth=1, budgetMin=45, tooFastMin=22, target="72%",
         take=dict(logic=10, grammar=8, reading=1, comp=1, listen=1, ab=4),
         en="Day 2 — First raise",
         ar="اليوم 2 — الرفع الأول",
         body_en="Logic sits one tier above whatever Day 1 proved. If the probes were already easy, today starts higher: that is the plan catching up, not a compliment. Grammar returns only the families you missed. Memory: 80% unlocks Level 2; 95% means leave the rest of Level 1 and start Level 2 now.",
         body_ar="المنطق يعلو مستوى واحدًا فوق ما أثبته اليوم 1. إذا كانت المجسّات سهلة أصلًا، فاليوم يبدأ أعلى: الخطة تلحق بكِ، وهذا ليس مجاملة. القواعد تعود فقط للعائلات التي أضعتِها. الذاكرة: 80% تفتح المستوى 2؛ و95% تعني اتركي بقية المستوى 1 وابدئي المستوى 2 الآن."),
    dict(n=3, tier=3, depth=1, budgetMin=55, tooFastMin=30, target="75%",
         take=dict(logic=16, grammar=8, reading=2, comp=1, listen=1, ab=4),
         en="Day 3 — The line should move",
         ar="اليوم 3 — يُفترض أن يتحرك الخط",
         body_en="Same grammar families as Day 1, new sentences. The scoreboard should show those families climbing. Logic is now long: lines of people, a rule with an exception, \"must be true.\" This is the first day that should not feel quick. If it does, the system failed, and a harder set opens before you stand up.",
         body_ar="عائلات القواعد نفسها كما في اليوم 1، بجمل جديدة. لوحة النتائج يُفترض أن تُظهر هذه العائلات وهي ترتفع. المنطق الآن طويل: صفوف أشخاص، وقاعدة باستثناء، و«يجب أن يكون صحيحًا». هذا أول يوم لا يُفترض أن يبدو سريعًا. إذا بدا كذلك فقد فشلت المنظومة، وتُفتح مجموعة أصعب قبل أن تقفي."),
    dict(n=4, tier=4, depth=1, budgetMin=60, tooFastMin=32, target="78%",
         take=dict(logic=16, grammar=6, reading=2, comp=1, listen=1, ab=2),
         en="Day 4 — Slow on purpose",
         ar="اليوم 4 — بطيء عن قصد",
         body_en="A full logic block: two rules that seem to argue, an order that has only one legal sequence, a correction you must not mix back in. Grammar only where Day 3 was still soft. You are not supposed to finish this too fast. Finishing it fast at 90% or better is the plan being late, and the bar moves in the same sitting.",
         body_ar="كتلة منطق كاملة: قاعدتان تبدوان متعارضتين، وترتيب له تسلسل قانوني واحد، وتصحيح لا تخلطينه بالقديم. القواعد فقط حيث بقي اليوم 3 لينًا. لا يُفترض أن تنهي هذا بسرعة. إنهاؤه بسرعة عند 90% أو أفضل يعني أن الخطة تأخّرت، والمستوى يتحرك في الجلسة نفسها."),
    dict(n=5, tier=5, depth=1, budgetMin=50, tooFastMin=28, target="82%",
         take=dict(logic=12, grammar=4, reading=1, comp=1, listen=1),
         en="Day 5 — Hold the new pace",
         ar="اليوم 5 — ثبّتي الإيقاع الجديد",
         body_en="Mixed set at today's tier, which is already past Day 4. Visual work is picture quiz 2 on the 7426 burglary: same photo, finer questions, 2 minutes then it hides. The point is pace, not a new kind of puzzle for its own sake.",
         body_ar="مجموعة مختلطة في مستوى اليوم، وهو أصلًا بعد اليوم 4. العمل البصري هو الاختبار 2 لصورة سطو 7426: الصورة نفسها، وأسئلة أدق، دقيقتان ثم تختفي. المقصود هو الإيقاع، لا نوعًا جديدًا من الألغاز لذاته."),
    dict(n=6, tier=5, depth=2, budgetMin=50, tooFastMin=28, target="84%",
         take=dict(logic=12, grammar=4, reading=1, comp=1),
         en="Day 6 — Judgment, and the harder band of the same tier",
         ar="اليوم 6 — الحكم، والنطاق الأصعب من المستوى نفسه",
         body_en="Biodata day. The exam's 54 biodata items are not right-or-wrong: some credit is given for every choice, a blank gets none, and two marks get none. Use the biodata practice on this page. Answer honestly, one choice, the closest fit. Also gather the Personal History Statement dates. The scored block is still harder than Day 5.",
         body_ar="يوم البيانات الشخصية. بنود الامتحان الـ 54 ليست صح أو خطأ: كل خيار يأخذ بعض الرصيد، والفراغ لا يأخذ شيئًا، والعلامتان لا تأخذان شيئًا. استخدمي تدريب البيانات في هذه الصفحة. أجيبي بصدق، خيارًا واحدًا، الأقرب. واجمعي أيضًا تواريخ بيان السيرة. والكتلة المحسوبة ما زالت أصعب من اليوم 5."),
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
         body_en="Visual section, fine pass: quiz 3 on the same 7426 picture. Still 2 minutes, then it hides. The detail is denser. The clock is not shorter. 95% opens the next picture. A short logic hold sits beside it so memory does not crowd the other skills. That logic is extra practice, not a fifth exam section.",
         body_ar="القسم البصري، الجولة الدقيقة: الاختبار 3 على صورة 7426 نفسها. ما زالت دقيقتين ثم تختفي. التفاصيل أكثف. الساعة ليست أقصر. 95% تفتح الصورة التالية. إمساك قصير بالمنطق بجانبه حتى لا تزاحم الذاكرة المهارات الأخرى. وذلك المنطق تدريب إضافي، لا قسم امتحان خامس."),
    dict(n=9, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="88%",
         take=dict(logic=10, grammar=4, reading=2, comp=1),
         en="Day 9 — Read at exam pace",
         ar="اليوم 9 — اقرئي بإيقاع الامتحان",
         body_en="Reading with understanding. The passage stays on the screen. It is not a memory test. Answer only from it. After the 2-minute picture study, the exam gives 2 hours for the 169 questions, about 43 seconds each if you keep moving. Grammar only on families still under 80%.",
         body_ar="القراءة بفهم. المقطع يبقى على الشاشة. ليس اختبار ذاكرة. أجيبي منه فقط. بعد دراسة الصورة لدقيقتين، يعطي الامتحان ساعتين للأسئلة الـ 169، نحو 43 ثانية لكل سؤال إذا واصلتِ التقدّم. القواعد فقط للعائلات التي ما زالت تحت 80%."),
    dict(n=10, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="90%",
         take=dict(logic=8, grammar=8, reading=1, ab=4),
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
         take=dict(logic=12, grammar=6, reading=1, comp=1, listen=1, obs=1, ab=2),
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


def delpoe_block():
    return f'''<section><h2>{bi("How the four sections are practiced", "كيف تُدرَّب الأقسام الأربعة")}</h2>
<ol>
<li>{bi("Recall of visual details — 40 scored questions. One picture, 2 minutes, no notes, then it hides. Statements are true or false. Other items ask whether something was in the picture. On the memory page: three 45-question quizzes on the 7426 burglary, broad then attributes then fine detail. 80% unlocks the next. 95% raises the bar. Then Quick Stop, then the corner crash, each with the same three quizzes.",
"استرجاع التفاصيل البصرية — 40 سؤالًا محسوبًا. صورة واحدة، دقيقتان، بلا ملاحظات، ثم تختفي. العبارات صحيحة أو خطأ. وبنود أخرى تسأل هل كان الشيء في الصورة. في صفحة الذاكرة: ثلاثة اختبارات من 45 على سطو 7426، من الصورة الكبيرة إلى الصفات إلى التفاصيل الدقيقة. 80% تفتح التالي. 95% ترفع المستوى. ثم كويك ستوب، ثم حادث الزاوية، كل منها بالاختبارات الثلاثة نفسها.")}</li>
<li>{bi("Written communication — 40 scored questions. A means the sentence is grammatically correct. B means it is not. Judge structure, grammar, and word usage. Ignore spelling, punctuation, and capitalization. A wrong homophone still counts. The four-choice “which sentence is correct” drills stay, beside the A/B key.",
"التواصل الكتابي — 40 سؤالًا محسوبًا. A تعني أن الجملة صحيحة نحويًا. B تعني أنها ليست كذلك. احكمي على البناء والقواعد واستعمال الكلمة. تجاهلي الإملاء وعلامات الترقيم وحالة الحرف. والكلمة المتشابهة اللفظ إذا غُلِط فيها تُحسب. تمارين «أي جملة صحيحة» من أربعة خيارات تبقى، بجانب مفتاح A/B.")}</li>
<li>{bi("Reading with understanding — 35 scored questions. The passage stays visible. Answer only from it. Do not import outside knowledge. Radio calls on this page hide on purpose. They are extra practice, not this section.",
"القراءة بفهم — 35 سؤالًا محسوبًا. المقطع يبقى ظاهرًا. أجيبي منه فقط. لا تُدخلي معرفة من خارجه. نداءات اللاسلكي في هذه الصفحة تختفي عن قصد. هي تدريب إضافي، لا هذا القسم.")}</li>
<li>{bi("Biodata — 54 questions about you. Some credit is given for every choice. No credit for a blank, and no credit for two marks. There is no single correct life. Answer honestly, and if nothing fits perfectly, pick the closest.",
"البيانات الشخصية — 54 سؤالًا عنكِ. كل خيار يأخذ بعض الرصيد. لا رصيد للفراغ، ولا رصيد لعلامتين. لا حياة واحدة صحيحة. أجيبي بصدق، وإذا لم ينطبق شيء تمامًا فاختاري الأقرب.")}</li>
</ol>
<p>{bi("While you study a picture: look at the whole, then zig-zag for details, then again for words you can read, then the whole once more. Sort people, structures, vehicles, readable items, and what is happening. Tie a name or a plate to a picture you will not forget.",
"حين تدرسين صورة: انظري إلى الكل، ثم مسح متعرج للتفاصيل، ثم مرة للكلمات المقروءة، ثم الكل مرة أخرى. صنّفي الأشخاص والمباني والمركبات والمقروء وما يحدث. اربطي اسمًا أو لوحة بصورة لن تنسيها.")}</p>
</section>'''


def biodata_block():
    qs = [
        ("In the past year, how often were you late to something you had agreed to do?",
         "في السنة الماضية، كم مرة تأخرتِ عن شيء وافقتِ على فعله؟",
         ["Never", "Once or twice", "Several times", "Often"],
         ["أبدًا", "مرة أو مرتين", "عدة مرات", "غالبًا"]),
        ("When a group task went badly, what did you usually do first?",
         "حين ساء عمل جماعي، ماذا كنتِ تفعلين أولًا عادة؟",
         ["Say what I saw", "Wait to be asked", "Quietly redo my part", "Leave it"],
         ["أقول ما رأيت", "أنتظر أن أُسأل", "أعيد جزئي بهدوء", "أتركه"]),
        ("How do you keep dates you must not miss?",
         "كيف تحفظين المواعيد التي لا يجوز أن تفوتيها؟",
         ["A written list I check", "A reminder on my phone", "I remember them", "Someone usually reminds me"],
         ["قائمة مكتوبة أراجعها", "تذكير في هاتفي", "أتذكرها", "عادة يذكّرني أحد"]),
        ("A supervisor corrects a sentence in your report. What is closest?",
         "مشرف يصحّح جملة في تقريركِ. ما الأقرب؟",
         ["I change it and ask if I still missed the point", "I change it and move on", "I argue if I think I was right", "I leave the original"],
         ["أغيّرها وأسأل إن كنت ما زلت أخطأت المقصود", "أغيّرها وأكمل", "أجادل إذا ظننت أني محقة", "أترك الأصل"]),
        ("Which is closest to that same year of lateness?",
         "ما الأقرب لتلك السنة نفسها في التأخر؟",
         ["I was almost never late", "I was late a few times", "Someone mentioned my lateness", "I was often late"],
         ["لم أتأخر تقريبًا", "تأخرت بضع مرات", "أحد ذكر تأخري", "كنت أتأخر غالبًا"]),
        ("How many jobs or regular commitments have you left without notice?",
         "كم عملًا أو التزامًا منتظمًا تركته بلا إشعار؟",
         ["None", "One", "Two", "More than two"],
         ["لا شيء", "واحد", "اثنان", "أكثر من اثنين"]),
        ("A written rule conflicts with what you expected. What do you do?",
         "قاعدة مكتوبة تعارض ما توقعتِ. ماذا تفعلين؟",
         ["Follow the written rule", "Follow what I expected", "Ask, then follow the answer", "Skip that part"],
         ["أتبع القاعدة المكتوبة", "أتبع ما توقعت", "أسأل ثم أتبع الجواب", "أتجاوز ذلك الجزء"]),
        ("Which is closest to how you answer questions about yourself?",
         "ما الأقرب لطريقة إجابتكِ عن أسئلة عن نفسكِ؟",
         ["The closest honest choice", "What sounds impressive", "I leave hard ones blank", "I mark two if both fit"],
         ["الخيار الصادق الأقرب", "ما يبدو مبهرًا", "أترك الصعب فارغًا", "أعلّم اثنين إذا انطبقا"]),
    ]
    blocks = []
    for i, (en, ar, oe, oa) in enumerate(qs, 1):
        opts = "".join(
            f'<label class="md-opt"><input type="radio" name="bio{i}" value="{k}"> {bi(oe[k], oa[k])}</label>'
            for k in range(4)
        )
        blocks.append(f'<li class="sp-day"><p>{bi(en, ar)}</p>{opts}</li>')
    return f'''<section id="biodata"><h2>{bi("Biodata practice", "تدريب البيانات الشخصية")}</h2>
<p>{bi("Eight original items, not exam questions. They are not scored right or wrong, and they do not move the tier. On the real section, answer every item, mark only one choice, and pick the closest honest fit.",
"ثمانية بنود من إعدادنا، ليست أسئلة الامتحان. لا تُحسب صحًا أو خطأ، ولا تحرّك المستوى. في القسم الحقيقي، أجيبي عن كل بند، وعلّمي خيارًا واحدًا، واختاري الأقرب الصادق.")}</p>
<ol class="md-qs">{''.join(blocks)}</ol>
<button type="button" class="sp-btn" id="hs-bio-save">{bi("Save these answers", "احفظي هذه الإجابات")}</button>
<p id="hs-bio-note"></p>
<script>
(function(){{
  var note=document.getElementById('hs-bio-note');
  var key='hesnaBio';
  function bi(e,a){{return '<span data-en>'+e+'</span><span data-ar>'+a+'</span>'}}
  try{{
    var saved=JSON.parse(localStorage.getItem(key)||'null');
    if(saved){{for(var i=1;i<=8;i++){{var el=document.querySelector('input[name=bio'+i+'][value="'+saved[i-1]+'"]'); if(el)el.checked=true;}}}}
  }}catch(err){{}}
  document.getElementById('hs-bio-save').addEventListener('click', function(){{
    var vals=[];
    for(var i=1;i<=8;i++){{var c=document.querySelector('input[name=bio'+i+']:checked'); if(!c){{note.innerHTML=bi('Every item needs one answer. A blank gets no credit on the exam.','كل بند يحتاج جوابًا واحدًا. الفراغ لا يأخذ رصيدًا في الامتحان.'); return;}} vals.push(c.value);}}
    try{{localStorage.setItem(key, JSON.stringify(vals));}}catch(err){{}}
    var msg=bi('Saved in this browser. This does not change the tier.','حُفظ في هذا المتصفح. هذا لا يغيّر المستوى.');
    if((vals[0]==='0'&&vals[4]==='3')||(vals[0]==='3'&&vals[4]==='0')) msg+=' '+bi('The two lateness answers disagree. On the exam, inconsistency is yours to notice.','جوابا التأخر لا يتفقان. في الامتحان، عدم الاتساق لكِ أن تلاحظيه.');
    if(vals[7]!=='0') msg+=' '+bi('The last item is the instruction: one honest closest choice, not a blank and not two marks.','البند الأخير هو التعليمات: خيار صادق واحد أقرب، لا فراغ ولا علامتان.');
    note.innerHTML=msg;
  }});
}})();
</script>
</section>'''


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
<li>{bi("The official exam has four sections, below. On this page the core that moves the tier is reading, listening, comprehension, observation, and the extra logic drills. Written A/B and four-choice grammar are a separate track. Biodata is honest practice, not a key.", "للامتحان الرسمي أربعة أقسام، في الأسفل. في هذه الصفحة الجوهر الذي يحرّك المستوى هو القراءة والاستماع والفهم والملاحظة وتدريبات المنطق الإضافية. الكتابة A/B وقواعد الأربع خيارات مسار منفصل. والبيانات الشخصية تدريب صادق، لا مفتاح.")}</li>
<li>{bi("Core under 70%: the next day still changes the work, and it opens with a short bridge so a miss is not a wall.", "جوهر تحت 70%: اليوم التالي يغيّر العمل رغم ذلك، ويبدأ بجسر قصير حتى لا يصير التعثّر جدارًا.")}</li>
<li>{bi("Core 70–94%: you are on the day's pace. Tomorrow is already a higher demand, even when today felt fair.", "جوهر 70–94%: أنتِ على إيقاع اليوم. وغدًا أصلًا طلب أعلى، حتى لو بدا اليوم عادلًا.")}</li>
<li>{bi("Core 95% or higher, or core 90%+ finished under the too-fast time: too easy. A harder set opens in this sitting. If that set sticks (80%+), tomorrow jumps an extra tier.", "جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في زمن أقصر من حد السرعة: أسهل مما ينبغي. تُفتح مجموعة أصعب في هذه الجلسة. إذا ثبتت (80% أو أكثر) فغدًا يقفز مستوى إضافيًا.")}</li>
<li>{bi("Day 1 probes: 3 of 4 harder probes right, with the ordinary core at 85%+, already counts as too easy. The grammar traps may still be soft. That is allowed.", "مجسّات اليوم 1: ثلاثة من أربعة مجسّات أصعب صحيحة، مع جوهر عادي عند 85% أو أكثر، تُحسب أصلًا أسهل مما ينبغي. فخاخ القواعد قد تبقى لينة. وهذا مسموح.")}</li>
<li>{bi("Grammar drills the families under 80%. A family at 95% across 4 or more items is retired. Day 3 rescores Day 1's soft families on new sentences, so the rise is visible.", "القواعد تدرّب العائلات تحت 80%. والعائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف. واليوم 3 يعيد قياس عائلات اليوم 1 اللينة بجمل جديدة، فيظهر الارتفاع.")}</li>
<li>{bi("Pictures: 80% unlocks the next quiz on that picture, then the next picture. 95% means that quiz was too easy and the harder one is the one that counts.", "الصور: 80% تفتح الاختبار التالي على تلك الصورة، ثم الصورة التالية. و95% تعني أن الاختبار كان أسهل مما ينبغي والأصعب هو الذي يُحسب.")}</li>
<li>{bi("End state for the two weeks: about 98% on this kind of page. Harder items, not a softer key.", "حالة نهاية الأسبوعين: نحو 98% على صفحة من هذا النوع. بنود أصعب، لا مفتاح أسهل.")}</li>
</ul></section>'''
    about = f'''<section><h2>{bi("The exam this plan follows", "الامتحان الذي تتبعه هذه الخطة")}</h2>
<p>{bi("Honolulu's entry exam is the Darany Entry Level Police Officer Examination, the DELPOE. It has four sections and 169 questions. You study one full-page picture for 2 minutes, with no notes. Then the picture is gone. After that study period you have 2 hours for the questions. Passing score on the city process: 70. Below 70, you may re-apply after 6 months. Math is not a section.",
"امتحان الدخول في هونولولو هو امتحان داراني لضابط الشرطة المبتدئ، DELPOE. فيه أربعة أقسام و169 سؤالًا. تدرسين صورة بصفحة كاملة لدقيقتين، بلا ملاحظات. ثم تختفي الصورة. بعد فترة الدراسة تلك لديكِ ساعتان للأسئلة. درجة النجاح في إجراءات المدينة: 70. أقل من 70، يمكنك إعادة التقديم بعد 6 أشهر. الرياضيات ليست قسمًا.")}</p>
<p>{bi("Nothing on this page is an official item. Read Darany's own study guide first. HPD has not published points per section or how the 70 is calculated.",
"لا شيء في هذه الصفحة سؤال رسمي. اقرئي دليل داراني نفسه أولًا. والشرطة لم تنشر درجات كل قسم ولا طريقة حساب الـ 70.")}</p>
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
<li>{bi("Four DELPOE sections, 169 questions: visual details 40, written communication 40, reading 35, biodata 54.", "أربعة أقسام في DELPOE، 169 سؤالًا: تفاصيل بصرية 40، تواصل كتابي 40، قراءة 35، بيانات شخصية 54.")}</li>
<li>{bi("2 minutes to study the picture, no notes, then it is gone. Then 2 hours for the questions, about 43 seconds each.", "دقيقتان لدراسة الصورة، بلا ملاحظات، ثم تختفي. ثم ساعتان للأسئلة، نحو 43 ثانية لكل سؤال.")}</li>
<li>{bi("Passing score 70. Below 70: re-apply after 6 months.", "درجة النجاح 70. أقل من 70: إعادة التقديم بعد 6 أشهر.")}</li>
<li>{bi("PRA, on-island: agility 21.6 s; 300 m in 82.8 s; 24 push-ups; 24 sit-ups in 1 min; 1.5 miles in 21 min.", "الجاهزية البدنية داخل الجزيرة: رشاقة 21.6 ث؛ 300 م في 82.8 ث؛ 24 ضغط؛ 24 بطن في دقيقة؛ 1.5 ميل في 21 د.")}</li>
</ul></section>'''
    sources = '''<section><h2><span data-en>Sources</span><span data-ar>المصادر</span></h2><ul>
<li><a href="https://www.joinhonolulupd.org/uploads/1/4/2/3/142306085/written_entry_exam_study_guide_1.pdf" rel="noopener nofollow">Darany: DELPOE study guide (HPD entrance exam PDF)</a></li>
<li><a href="https://www.joinhonolulupd.org/application-process.html" rel="noopener nofollow">JOIN HPD: Application Process</a></li>
<li><a href="https://www.joinhonolulupd.org/pra-instructions.html" rel="noopener nofollow">JOIN HPD: PRA Instructions</a></li>
<li><a href="https://www.governmentjobs.com/careers/honolulupd/jobs/3347241/metropolitan-police-recruit-on-island" rel="noopener nofollow">HPD job posting: Metropolitan Police Recruit (GovernmentJobs)</a></li>
<li><a href="https://a856-exams.nyc.gov/OASysWeb/noe/20277311000.pdf" rel="noopener nofollow">NYC DCAS: Police Officer Notice of Examination</a></li>
<li><a href="https://post.ca.gov/LE-entry-level-test-battery-agency-faqs-2026" rel="noopener nofollow">California POST: PELLETB FAQs</a></li>
<li><a href="https://www.joinlapd.com/step-2-multiple-choice-test" rel="noopener nofollow">LAPD: Step 2 Multiple Choice Test</a></li>
</ul><p class="sp-ph"><span data-en>DELPOE structure checked against Darany's guide on Nov 1, 2026. City passing score and the PRA checked Oct 28, 2026. Always confirm details with HPD before the exam.</span><span data-ar>بُنية DELPOE رُوجعت على دليل داراني في 1 نوفمبر 2026. ودرجة النجاح المدينة والجاهزية البدنية رُوجعتا في 28 أكتوبر 2026. تأكّدي دائمًا من التفاصيل مع الشرطة قبل الامتحان.</span></p></section>'''
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
<p><a class="sp-btn" href="hesna-6abec5-memory.html">{bi("Visual drills: 2 minutes, then the picture hides. Start with the 7426 burglary.", "تمارين بصرية: دقيقتان ثم تختفي الصورة. ابدئي بسطو 7426.")}</a></p>
{delpoe_block()}
{biodata_block()}
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
    photos = hesna_photo.quizzes()
    data = {
        "S": photos + base["S"] + extra,
        "C": base["C"], "I": base["I"], "V": base["V"], "BC": base["BC"],
        "BLURB": hesna_scenes.BLURBS,
    }
    raw = (ROOT / "scripts" / "hesna_memory_shell.html").read_text()
    needle = "window.MD_DATA={};"
    if needle not in raw:
        raise SystemExit("MD_DATA placeholder missing")
    return raw.replace(needle, "window.MD_DATA=" + js(data) + ";", 1)


def main():
    photo_stats = hesna_photo.check()
    stats = hesna_banks.check_banks()
    stats["photos"] = photo_stats
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
