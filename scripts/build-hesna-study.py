#!/usr/bin/env python3
"""Rebuild Hassnaa's hidden HPD study guide and memory drills.

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
body{max-width:1100px;margin:0 auto;padding:1rem 1rem 3rem}
h1{font-size:1.35rem;margin:.2rem 0}
.hs-dayline{margin:.35rem 0 .6rem}
.hs-dayline select{font:inherit;color:inherit;background:#0b1622;border:1px solid rgba(255,255,255,.3);border-radius:8px;padding:.4rem .6rem;min-height:44px;max-width:100%}
.hs-results h2,.hs-results h3{margin:.35rem 0}
details.hs-ref{margin:1.5rem 0}
.sp-top{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
#sp-toggle{padding:.5rem 1.1rem;border-radius:999px;border:1px solid var(--brand-blue,#2b7bd6);background:transparent;color:inherit;font:inherit;cursor:pointer}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem}
.sp-week{border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:1rem 1rem 1.25rem;margin:1.25rem 0}
.hs-pack{margin:.5rem 0 1rem}
.hs-pack-head{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .75rem;margin:0 0 .7rem;font-size:1.45rem;line-height:1.3}
.hs-pack-cue{font-size:1rem;font-weight:600;line-height:1.4}
.hs-pack-head .hs-pack-start{margin:0 .2rem;font-size:1rem;font-weight:600;vertical-align:middle}
.hs-lesson{border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:.9rem 1rem;margin:.7rem 0;background:rgba(255,255,255,.04)}
.hs-lesson h3{margin:0 0 .4rem}
.sp-day{border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:1rem;background:rgba(255,255,255,.04)}
.sp-btn{margin-top:.5rem;padding:.45rem .9rem;border-radius:8px;border:1px solid rgba(255,255,255,.3);background:transparent;color:inherit;font:inherit;cursor:pointer;min-height:44px}
.sp-phase{margin:1.5rem 0}.sp-day h3{margin:0 0 .5rem}.sp-ph{opacity:.85;font-style:italic;margin:0}
html{scroll-behavior:auto!important}
html[lang=en] [data-ar],html[lang=ar] [data-en]{display:none}
#week-1,#week-2,#week-3,#week-4,#day-1{scroll-margin-top:4.75rem}
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
         body_en="Start with the memory drill: picture quiz 1, the 7426 burglary. Study the scene for 2 minutes. No notes. Then it hides. The questions ask only about details the picture shows. After that come the other quizzes: written A/B, correct or incorrect the way the exam asks, plus the transfer traps Arabic and French leave in English; one short reading, and the passage stays visible; logic probes; and a radio call. Logic and the radio call are extra practice, not a fifth section. This is a baseline. A miss is information, and it does not lock any other day.",
         body_ar="ابدئي بتمرين الذاكرة: الاختبار 1 لصورة السطو 7426. ادرسي المشهد دقيقتين. بلا ملاحظات. ثم يختفي. الأسئلة عن تفاصيل تُظهرها الصورة فقط. بعد ذلك الاختبارات الأخرى: كتابة A/B، صح أو خطأ كما في الامتحان، مع فخاخ النقل من العربية والفرنسية؛ وقراءة قصيرة يبقى مقطعها ظاهرًا؛ ومجسّات منطق؛ ونداء لاسلكي. المنطق والنداء تدريب إضافي، لا قسمًا خامسًا. هذا خط أساس. الخطأ معلومة، ولا يقفل أي يوم آخر."),
    dict(n=2, tier=2, depth=1, budgetMin=45, tooFastMin=22, target="72%",
         take=dict(logic=10, grammar=8, reading=1, comp=1, listen=1, ab=4),
         en="Day 2 — First raise",
         ar="اليوم 2 — الرفع الأول",
         body_en="Memory first: two Level 1 street sketches. Two minutes each, then the drawing hides. Every question is something that drawing shows. Then logic sits one tier above whatever Day 1 proved. If the probes were already easy, today starts higher: that is the plan catching up, not a compliment. Grammar returns only the families you missed. A high score is saved. It does not close the other sketches or the next day.",
         body_ar="الذاكرة أولًا: رسمان من المستوى 1. دقيقتان لكل رسم، ثم يختفي. كل سؤال عن شيء يُظهره ذلك الرسم. ثم المنطق يعلو مستوى واحدًا فوق ما أثبته اليوم 1. إذا كانت المجسّات سهلة أصلًا، فاليوم يبدأ أعلى: الخطة تلحق بكِ، وهذا ليس مجاملة. القواعد تعود فقط للعائلات التي أضعتِها. النتيجة العالية تُحفظ. وهي لا تغلق الرسوم الأخرى ولا اليوم التالي."),
    dict(n=3, tier=3, depth=1, budgetMin=55, tooFastMin=30, target="75%",
         take=dict(logic=16, grammar=8, reading=2, comp=1, listen=1, ab=4),
         en="Day 3 — The line should move",
         ar="اليوم 3 — يُفترض أن يتحرك الخط",
         body_en="Memory first: one more Level 1 sketch, then the first Level 2 corner. Two minutes each, then they hide. Questions match the drawing. Then the same grammar families as Day 1, in new sentences. The scoreboard should show those families climbing. Logic is now long: lines of people, a rule with an exception, \"must be true.\" This is the first day that should not feel quick. If it does, a harder set is offered in the same sitting. The next day stays open either way.",
         body_ar="الذاكرة أولًا: رسم آخر من المستوى 1، ثم أول زاوية من المستوى 2. دقيقتان لكل منهما، ثم يختفيان. الأسئلة تطابق الرسم. ثم عائلات القواعد نفسها كما في اليوم 1، بجمل جديدة. لوحة النتائج يُفترض أن تُظهر هذه العائلات وهي ترتفع. المنطق الآن طويل: صفوف أشخاص، وقاعدة باستثناء، و«يجب أن يكون صحيحًا». هذا أول يوم لا يُفترض أن يبدو سريعًا. إذا بدا كذلك تُعرض مجموعة أصعب في الجلسة نفسها. واليوم التالي يبقى مفتوحًا في الحالين."),
    dict(n=4, tier=4, depth=1, budgetMin=60, tooFastMin=32, target="78%",
         take=dict(logic=16, grammar=6, reading=2, comp=1, listen=1, ab=2),
         en="Day 4 — Slow on purpose",
         ar="اليوم 4 — بطيء عن قصد",
         body_en="Memory first: two Level 2 sketches, 2 minutes each, then they hide. Then a full logic block: two rules that seem to argue, an order that has only one legal sequence, a correction you must not mix back in. Grammar only where Day 3 was still soft. You are not supposed to finish this too fast. Finishing it fast at 90% or better is the plan being late, and a harder set is offered in the same sitting.",
         body_ar="الذاكرة أولًا: رسمان من المستوى 2، دقيقتان لكل منهما، ثم يختفيان. ثم كتلة منطق كاملة: قاعدتان تبدوان متعارضتين، وترتيب له تسلسل قانوني واحد، وتصحيح لا تخلطينه بالقديم. القواعد فقط حيث بقي اليوم 3 لينًا. لا يُفترض أن تنهي هذا بسرعة. إنهاؤه بسرعة عند 90% أو أفضل يعني أن الخطة تأخّرت، وتُعرض مجموعة أصعب في الجلسة نفسها."),
    dict(n=5, tier=5, depth=1, budgetMin=50, tooFastMin=28, target="82%",
         take=dict(logic=12, grammar=4, reading=1, comp=1, listen=1),
         en="Day 5 — Hold the new pace",
         ar="اليوم 5 — ثبّتي الإيقاع الجديد",
         body_en="Memory first: picture quiz 2 on the 7426 burglary. Same photo, finer questions, 2 minutes, then it hides. Every question is something the photo shows. Then a mixed set at today's tier, which is already past Day 4: logic, grammar, reading, and a radio call. The point is pace, not a new kind of puzzle for its own sake.",
         body_ar="الذاكرة أولًا: الاختبار 2 لصورة سطو 7426. الصورة نفسها، وأسئلة أدق، دقيقتان ثم تختفي. كل سؤال عن شيء تُظهره الصورة. ثم مجموعة مختلطة في مستوى اليوم، وهو أصلًا بعد اليوم 4: منطق وقواعد وقراءة ونداء لاسلكي. المقصود هو الإيقاع، لا نوعًا جديدًا من الألغاز لذاته."),
    dict(n=6, tier=5, depth=2, budgetMin=50, tooFastMin=28, target="84%",
         take=dict(logic=12, grammar=4, reading=1, comp=1),
         en="Day 6 — Judgment, and the harder band of the same tier",
         ar="اليوم 6 — الحكم، والنطاق الأصعب من المستوى نفسه",
         body_en="Memory first: two Level 3 street sketches, 2 minutes each, then they hide. Then biodata. The exam's 54 biodata items are not right-or-wrong: some credit is given for every choice, a blank gets none, and two marks get none. Use the Biodata practice section on this page. Answer honestly, one choice, the closest fit. Also gather the Personal History Statement dates. The scored block is still harder than Day 5.",
         body_ar="الذاكرة أولًا: رسمان من المستوى 3، دقيقتان لكل منهما، ثم يختفيان. ثم البيانات الشخصية. بنود الامتحان الـ 54 ليست صح أو خطأ: كل خيار يأخذ بعض الرصيد، والفراغ لا يأخذ شيئًا، والعلامتان لا تأخذان شيئًا. استخدمي قسم تدريب البيانات في هذه الصفحة. أجيبي بصدق، خيارًا واحدًا، الأقرب. واجمعي أيضًا تواريخ بيان السيرة. والكتلة المحسوبة ما زالت أصعب من اليوم 5."),
    dict(n=7, tier=5, depth=3, budgetMin=50, tooFastMin=28, target="85%",
         take=dict(logic=12, grammar=4, reading=1, listen=1, comp=1),
         en="Day 7 — Look back at Monday",
         ar="اليوم 7 — انظري إلى الاثنين",
         body_en="Memory first: the last Level 3 sketch, then the fine 7426 quiz. Same burglary picture, the small print, 2 minutes, then it hides. Questions match what the picture shows. Then one mixed sitting at this week's top band. 80% is the mastery mark on the scoreboard. At 95% the scoreboard treats the picture as easy. Neither mark closes Week 2. Then open the scoreboard: Day 1 beside today. Fitness, on your own: push-ups, sit-ups, and the 1.5-mile run. The quiz does not grade those.",
         body_ar="الذاكرة أولًا: آخر رسم من المستوى 3، ثم اختبار التفاصيل لصورة 7426. صورة السطو نفسها، الحرف الصغير، دقيقتان ثم تختفي. الأسئلة تطابق ما تُظهره الصورة. ثم جلسة مختلطة واحدة في أعلى نطاق هذا الأسبوع. 80% علامة الإتقان على لوحة النتائج. عند 95% تعامل اللوحة الصورة على أنها سهلة. لا علامة منهما تغلق الأسبوع الثاني. ثم افتحي لوحة النتائج: اليوم 1 بجانب اليوم. اللياقة، لحسابكِ: تمارين الضغط، والبطن، وجري 1.5 ميل. الاختبار لا يقيّمها."),
    dict(n=8, tier=5, depth=3, budgetMin=50, tooFastMin=26, target="87%",
         take=dict(logic=8, grammar=2, listen=1),
         en="Day 8 — Eyes",
         ar="اليوم 8 — العينان",
         body_en="Week 2 Day 1 is open now. It is harder than Week 1. Memory first: Quick Stop, quiz 1, the broad scene. 2 minutes, then it hides. Questions match the picture. Then the other work, which sits higher and aims at what was still soft. That logic is extra practice, not a fifth exam section.",
         body_ar="اليوم 1 من الأسبوع الثاني مفتوح الآن. وهو أصعب من الأسبوع الأول. الذاكرة أولًا: كويك ستوب، الاختبار 1، الصورة الكبيرة. دقيقتان ثم تختفي. الأسئلة تطابق الصورة. ثم بقية العمل، وهو أعلى ويستهدف ما بقي لينًا. وذلك المنطق تدريب إضافي، لا قسم امتحان خامس."),
    dict(n=9, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="88%",
         take=dict(logic=10, grammar=4, reading=2, comp=1),
         en="Day 9 — Read at exam pace",
         ar="اليوم 9 — اقرئي بإيقاع الامتحان",
         body_en="Memory first: Quick Stop, quiz 2, the attributes. Same picture, 2 minutes, then it hides. Then reading with understanding. The passage stays on the screen. It is not a memory test. Answer only from it. On the real exam, after the 2-minute picture study, you have 2 hours for the 169 questions, about 43 seconds each if you keep moving. Grammar only on families still under 80%.",
         body_ar="الذاكرة أولًا: كويك ستوب، الاختبار 2، الصفات. الصورة نفسها، دقيقتان ثم تختفي. ثم القراءة بفهم. المقطع يبقى على الشاشة. ليس اختبار ذاكرة. أجيبي منه فقط. في الامتحان الحقيقي، بعد دراسة الصورة لدقيقتين، لديكِ ساعتان للأسئلة الـ 169، نحو 43 ثانية لكل سؤال إذا واصلتِ التقدّم. القواعد فقط للعائلات التي ما زالت تحت 80%."),
    dict(n=10, tier=6, depth=1, budgetMin=50, tooFastMin=28, target="90%",
         take=dict(logic=8, grammar=8, reading=1, ab=4),
         en="Day 10 — A sentence a sergeant can use",
         ar="اليوم 10 — جملة يستطيع الرقيب استخدامها",
         body_en="Memory first: Quick Stop, quiz 3, the fine detail. Same picture, 2 minutes, then it hides. Then grammar and phrasing in report register: one sentence is correct, three are not. On paper, write a six-line incident (who, what, when, where, direction, correction) and read it against the sentences you just judged. Do not drill a family the scoreboard has retired.",
         body_ar="الذاكرة أولًا: كويك ستوب، الاختبار 3، التفاصيل الدقيقة. الصورة نفسها، دقيقتان ثم تختفي. ثم القواعد والصياغة في لغة التقرير: جملة واحدة صحيحة وثلاث ليست كذلك. على الورق، اكتبي حادثة من ستة أسطر (من، ماذا، متى، أين، الاتجاه، التصحيح) واقرئيها مقابل الجمل التي حكمتِ عليها. لا تدرّبي عائلة أوقفتها لوحة النتائج."),
    dict(n=11, tier=6, depth=2, budgetMin=50, tooFastMin=28, target="92%",
         take=dict(logic=14, grammar=4, comp=1, reading=1),
         en="Day 11 — Which rule wins",
         ar="اليوم 11 — أي قاعدة تفوز",
         body_en="Memory first: street sketch L4-1, 2 minutes, then it hides. Then procedures. Two rules seem to apply; one governs. Pick the next step, not the step that sounds busy. This band is harder than Day 10 even though both sit on tier 6.",
         body_ar="الذاكرة أولًا: رسم الشارع L4-1، دقيقتان ثم يختفي. ثم الإجراءات. قاعدتان تبدوان منطبقتين؛ وواحدة تحكم. اختاري الخطوة التالية، لا الخطوة التي تبدو مشغولة. هذا النطاق أصعب من اليوم 10 رغم أن كليهما في المستوى 6."),
    dict(n=12, tier=6, depth=3, budgetMin=70, tooFastMin=40, target="94%",
         take=dict(logic=12, grammar=6, reading=1, comp=1, listen=1, obs=1, ab=2),
         en="Day 12 — Dress rehearsal",
         ar="اليوم 12 — بروفة",
         body_en="Memory first: street sketch L4-2, 2 minutes, then it hides. Then all pillars, one sitting, including a new observation scenario with a correction. The scoreboard marks what is still soft. 98% with time left means the stretch bank is the one that counts, not a review of what you already command. Week 3 stays open either way.",
         body_ar="الذاكرة أولًا: رسم الشارع L4-2، دقيقتان ثم يختفي. ثم كل الأعمدة، في جلسة واحدة، ومنها مشهد ملاحظة جديد فيه تصحيح. لوحة النتائج تعلّم ما يزال لينًا. 98% مع وقت متبقٍّ تعني أن بنك التمدد هو الذي يُحسب، لا مراجعة ما تملكينه أصلًا. الأسبوع الثالث يبقى مفتوحًا في الحالين."),
    dict(n=13, tier=6, depth=3, budgetMin=45, tooFastMin=24, target="96%", mode="repair",
         take=dict(logic=8, grammar=8, listen=1, obs=1),
         stretchTake=dict(logic=8, grammar=4, listen=1, obs=1),
         en="Day 13 — Soft spots, or the stretch",
         ar="اليوم 13 — المواضع اللينة، أو التمدد",
         body_en="Memory first: street sketch L4-3, 2 minutes, then it hides. Then the soft spots, if anything is still under 95%. If nothing is, the stretch bank loads. Use the Biodata practice section again and check that the two lateness answers still agree. Fitness, on your own: agility run and the 300-meter run. Not scored here. The next day stays open either way.",
         body_ar="الذاكرة أولًا: رسم الشارع L4-3، دقيقتان ثم يختفي. ثم المواضع اللينة، إذا بقي شيء تحت 95%. إذا لم يبقَ شيء يُحمَّل بنك التمدد. استخدمي قسم تدريب البيانات مرة أخرى وتحقّقي أن جوابَي التأخر ما زالا متفقين. اللياقة، لحسابكِ: جري الرشاقة وجري 300 متر. لا يُحسبان هنا. واليوم التالي يبقى مفتوحًا في الحالين."),
    dict(n=14, tier=6, depth=3, budgetMin=35, tooFastMin=18, target="98%", mode="capstone",
         take=dict(logic=8, grammar=4, reading=1, listen=1),
         en="Day 14 — The photograph, beside today",
         ar="اليوم 14 — الصورة، بجانب اليوم",
         body_en="Memory first: street sketch L4-4, the hand-drawn corner, 2 minutes, then it hides. Every question is something that drawing shows, including the driver. Then a short sharp mix if Day 13 was high, or the weak bank if it was not. Put Day 1 beside Day 14. Weeks 3 and 4 are already open, and they are harder. The aim across the four weeks is about 98% on this kind of page, with a rested mind, before the Honolulu exam. Bring what HPD's own instructions list; this page does not guess the packing list.",
         body_ar="الذاكرة أولًا: رسم الشارع L4-4، الزاوية المرسومة يدويًا، دقيقتان ثم يختفي. كل سؤال عن شيء يُظهره ذلك الرسم، بما فيه السائق. ثم مزيج قصير حاد إذا كان اليوم 13 مرتفعًا، أو بنك الضعف إذا لم يكن. ضعي اليوم 1 بجانب اليوم 14. الأسبوعان الثالث والرابع مفتوحان أصلًا، وهما أصعب. هدف الأسابيع الأربعة نحو 98% على صفحة من هذا النوع، بعقل مرتاح، قبل امتحان هونولولو. أحضري ما تذكره تعليمات الشرطة نفسها؛ هذه الصفحة لا تخمّن قائمة الأمتعة."),
    dict(n=15, tier=6, depth=2, budgetMin=55, tooFastMin=30, target="90%",
         take=dict(logic=10, grammar=4, reading=1, listen=1, ab=4),
         en="Week 3 Day 1 — Corner, the broad scene",
         ar="الأسبوع 3 اليوم 1 — الزاوية، الصورة الكبيرة",
         body_en="Week 3 is harder than Week 2, and it is open now. Memory first: the corner crash, quiz 1, the broad scene. People, the two vehicles, and what happened. 2 minutes, then the picture hides. Questions match that picture only. Then written A/B, a short reading with the passage left visible, logic, and a radio call.",
         body_ar="الأسبوع الثالث أصعب من الثاني، وهو مفتوح الآن. الذاكرة أولًا: حادث الزاوية، الاختبار 1، الصورة الكبيرة. الأشخاص، والمركبتان، وما حدث. دقيقتان ثم تختفي الصورة. الأسئلة تطابق تلك الصورة فقط. ثم كتابة A/B، وقراءة قصيرة يبقى مقطعها ظاهرًا، ومنطق، ونداء لاسلكي."),
    dict(n=16, tier=6, depth=2, budgetMin=55, tooFastMin=30, target="91%",
         take=dict(logic=10, grammar=4, reading=1, comp=1, ab=2),
         en="Week 3 Day 2 — Corner, attributes",
         ar="الأسبوع 3 اليوم 2 — الزاوية، الصفات",
         body_en="Memory first: the same corner, quiz 2. Clothes, counts, and which person goes with which object. 2 minutes, then it hides. Then logic, grammar, a reading whose passage stays visible, and a comprehension set.",
         body_ar="الذاكرة أولًا: الزاوية نفسها، الاختبار 2. الملابس والعدد وأي شخص مع أي غرض. دقيقتان ثم تختفي. ثم منطق وقواعد وقراءة يبقى مقطعها ظاهرًا ومجموعة فهم."),
    dict(n=17, tier=6, depth=2, budgetMin=60, tooFastMin=32, target="92%",
         take=dict(logic=12, grammar=4, reading=2, ab=2, listen=1),
         en="Week 3 Day 3 — Corner, fine detail",
         ar="الأسبوع 3 اليوم 3 — الزاوية، التفاصيل الدقيقة",
         body_en="Memory first: the same corner, quiz 3. Signs, small counts, and the look-alike details from the earlier pictures. 2 minutes, then it hides. Then a longer logic block, two readings, written A/B, and a radio call.",
         body_ar="الذاكرة أولًا: الزاوية نفسها، الاختبار 3. اللافتات والأعداد الصغيرة والتفاصيل التي تشبه الصور السابقة. دقيقتان ثم تختفي. ثم كتلة منطق أطول، وقراءتان، وكتابة A/B، ونداء لاسلكي."),
    dict(n=18, tier=6, depth=3, budgetMin=60, tooFastMin=32, target="93%",
         take=dict(logic=12, grammar=6, comp=1, listen=1, ab=2),
         en="Week 3 Day 4 — Denser streets",
         ar="الأسبوع 3 اليوم 4 — شوارع أكثف",
         body_en="Memory first: street sketch L5-1. The corner is denser than Week 1. 2 minutes, then it hides. Every question is on the drawing. Then grammar, logic, comprehension, a radio call, and written A/B.",
         body_ar="الذاكرة أولًا: رسم الشارع L5-1. الزاوية أكثف من الأسبوع الأول. دقيقتان ثم يختفي. كل سؤال عن الرسم. ثم قواعد ومنطق وفهم ونداء لاسلكي وكتابة A/B."),
    dict(n=19, tier=6, depth=3, budgetMin=60, tooFastMin=32, target="94%",
         take=dict(logic=12, grammar=4, reading=2, obs=1, ab=2),
         en="Week 3 Day 5 — Denser streets, continued",
         ar="الأسبوع 3 اليوم 5 — الشوارع الأكثف، تتمة",
         body_en="Memory first: street sketch L5-2, 2 minutes, then it hides. Then two readings with the passages left visible, an observation scenario, logic, and written A/B.",
         body_ar="الذاكرة أولًا: رسم الشارع L5-2، دقيقتان ثم يختفي. ثم قراءتان يبقى مقطعاهما ظاهرين، ومشهد ملاحظة، ومنطق، وكتابة A/B."),
    dict(n=20, tier=6, depth=3, budgetMin=55, tooFastMin=30, target="94%",
         take=dict(logic=10, grammar=6, reading=1, comp=1, ab=4),
         en="Week 3 Day 6 — Denser streets, and biodata",
         ar="الأسبوع 3 اليوم 6 — الشوارع الأكثف، والبيانات",
         body_en="Memory first: street sketch L5-3, 2 minutes, then it hides. Then grammar, logic, one reading, and comprehension. Use the Biodata practice section again: one honest choice, no blank, no second mark.",
         body_ar="الذاكرة أولًا: رسم الشارع L5-3، دقيقتان ثم يختفي. ثم قواعد ومنطق وقراءة واحدة وفهم. استخدمي قسم تدريب البيانات مرة أخرى: خيار صادق واحد، بلا فراغ، وبلا علامة ثانية."),
    dict(n=21, tier=6, depth=3, budgetMin=65, tooFastMin=34, target="95%",
         take=dict(logic=14, grammar=4, reading=1, listen=1, ab=2, obs=1),
         en="Week 3 Day 7 — A correction incident",
         ar="الأسبوع 3 اليوم 7 — حادثة فيها تصحيح",
         body_en="Memory first: the lobby correction, L6-1. Study the scene for 2 minutes. The questions use only what that scene shows, including the correction you must keep and the one you must drop. Then the hardest mixed set of this week: logic, grammar, reading, a radio call, written A/B, and an observation scenario.",
         body_ar="الذاكرة أولًا: تصحيح الردهة، L6-1. ادرسي المشهد دقيقتين. الأسئلة تستخدم فقط ما يُظهره ذلك المشهد، بما فيه التصحيح الذي تبقينه والذي تسقطينه. ثم أصعب مجموعة مختلطة في هذا الأسبوع: منطق وقواعد وقراءة ونداء لاسلكي وكتابة A/B ومشهد ملاحظة."),
    dict(n=22, tier=6, depth=3, budgetMin=70, tooFastMin=36, target="96%",
         take=dict(logic=14, grammar=6, reading=2, comp=1, ab=4),
         en="Week 4 Day 1 — The second correction",
         ar="الأسبوع 4 اليوم 1 — التصحيح الثاني",
         body_en="Week 4 is the hardest week, and it is open now. Memory first: the garage correction, L6-2. 2 minutes, then it hides. Keep the detail the scene tells you to keep, and drop the one it tells you to disregard. Then two readings, comprehension, a long logic block, grammar, and written A/B.",
         body_ar="الأسبوع الرابع هو الأصعب، وهو مفتوح الآن. الذاكرة أولًا: تصحيح المرآب، L6-2. دقيقتان ثم يختفي. أبقي التفصيل الذي يقول المشهد أن تبقيه، وأسقطي الذي يقول أن تتجاهليه. ثم قراءتان وفهم وكتلة منطق طويلة وقواعد وكتابة A/B."),
    dict(n=23, tier=6, depth=3, budgetMin=65, tooFastMin=34, target="96%",
         take=dict(logic=12, grammar=8, reading=1, listen=1, obs=1, ab=2),
         en="Week 4 Day 2 — Quick Stop, fine review",
         ar="الأسبوع 4 اليوم 2 — كويك ستوب، مراجعة دقيقة",
         body_en="Memory first: Quick Stop, quiz 3, again. Same picture, same questions, 2 minutes, then it hides. The written work around it is the top tier: grammar, logic, one reading, a radio call, an observation scenario, and written A/B.",
         body_ar="الذاكرة أولًا: كويك ستوب، الاختبار 3، مرة أخرى. الصورة نفسها والأسئلة نفسها، دقيقتان ثم تختفي. والعمل الكتابي حولها في أعلى مستوى: قواعد ومنطق وقراءة واحدة ونداء لاسلكي ومشهد ملاحظة وكتابة A/B."),
    dict(n=24, tier=6, depth=3, budgetMin=65, tooFastMin=34, target="97%",
         take=dict(logic=12, grammar=6, reading=2, comp=1, ab=4),
         en="Week 4 Day 3 — Corner again, attributes",
         ar="الأسبوع 4 اليوم 3 — الزاوية مرة أخرى، الصفات",
         body_en="Memory first: the corner crash, quiz 2, again. 2 minutes, then it hides. Then two readings, comprehension, logic, grammar, and written A/B at the top tier.",
         body_ar="الذاكرة أولًا: حادث الزاوية، الاختبار 2، مرة أخرى. دقيقتان ثم يختفي. ثم قراءتان وفهم ومنطق وقواعد وكتابة A/B في أعلى مستوى."),
    dict(n=25, tier=6, depth=3, budgetMin=70, tooFastMin=36, target="97%",
         take=dict(logic=14, grammar=4, reading=1, listen=1, obs=1, ab=2),
         en="Week 4 Day 4 — Corner again, fine detail",
         ar="الأسبوع 4 اليوم 4 — الزاوية مرة أخرى، التفاصيل الدقيقة",
         body_en="Memory first: the corner crash, quiz 3, again. Signs and small counts. 2 minutes, then it hides. Then logic, a reading, a radio call, an observation scenario, grammar, and written A/B.",
         body_ar="الذاكرة أولًا: حادث الزاوية، الاختبار 3، مرة أخرى. اللافتات والأعداد الصغيرة. دقيقتان ثم يختفي. ثم منطق وقراءة ونداء لاسلكي ومشهد ملاحظة وقواعد وكتابة A/B."),
    dict(n=26, tier=6, depth=3, budgetMin=65, tooFastMin=34, target="97%",
         take=dict(logic=12, grammar=8, reading=2, comp=1, ab=4),
         en="Week 4 Day 5 — The lobby correction, again",
         ar="الأسبوع 4 اليوم 5 — تصحيح الردهة، مرة أخرى",
         body_en="Memory first: L6-1 again. Same lobby, same questions, 2 minutes, then it hides. Then the top-tier written and reading set: grammar, two readings, comprehension, logic, and written A/B.",
         body_ar="الذاكرة أولًا: L6-1 مرة أخرى. الردهة نفسها والأسئلة نفسها، دقيقتان ثم تختفي. ثم مجموعة الكتابة والقراءة في أعلى مستوى: قواعد وقراءتان وفهم ومنطق وكتابة A/B."),
    dict(n=27, tier=6, depth=3, budgetMin=60, tooFastMin=32, target="98%",
         take=dict(logic=10, grammar=6, reading=1, listen=1, ab=4, comp=1),
         en="Week 4 Day 6 — The garage correction, and biodata",
         ar="الأسبوع 4 اليوم 6 — تصحيح المرآب، والبيانات",
         body_en="Memory first: L6-2 again. 2 minutes, then it hides. Then grammar, logic, one reading, a radio call, comprehension, and written A/B. Use the Biodata practice section once more before exam week: one closest honest choice on every item.",
         body_ar="الذاكرة أولًا: L6-2 مرة أخرى. دقيقتان ثم يختفي. ثم قواعد ومنطق وقراءة واحدة ونداء لاسلكي وفهم وكتابة A/B. استخدمي قسم تدريب البيانات مرة أخيرة قبل أسبوع الامتحان: خيار صادق واحد أقرب في كل بند."),
    dict(n=28, tier=6, depth=3, budgetMin=50, tooFastMin=24, target="98%",
         take=dict(logic=8, grammar=4, reading=1, listen=1, ab=4),
         en="Week 4 Day 7 — Day 1 beside today",
         ar="الأسبوع 4 اليوم 7 — اليوم 1 بجانب اليوم",
         body_en="Memory first: the fine 7426 quiz again. Same burglary picture, 2 minutes, then it hides. Then a short top-tier mix: logic, grammar, one reading, a radio call, and written A/B. Put Day 1 beside today. The aim, walking into the Honolulu exam, is about 98% on this kind of page. Every earlier week is still open if you want it.",
         body_ar="الذاكرة أولًا: اختبار التفاصيل لصورة 7426 مرة أخرى. صورة السطو نفسها، دقيقتان ثم تختفي. ثم مزيج قصير في أعلى مستوى: منطق وقواعد وقراءة واحدة ونداء لاسلكي وكتابة A/B. ضعي اليوم 1 بجانب اليوم. الهدف، وأنتِ داخلة إلى امتحان هونولولو، نحو 98% على صفحة من هذا النوع. كل أسبوع سابق ما زال مفتوحًا إذا أردته."),
]


def delpoe_block():
    return f'''<section><h2>{bi("How the four sections are practiced", "كيف تُدرَّب الأقسام الأربعة")}</h2>
<ol>
<li>{bi("Recall of visual details — 40 scored questions. One picture, 2 minutes, no notes, then it hides. Statements are true or false. Other items ask whether something was in the picture. Every day on this page starts with that drill. Week 1 is the 7426 burglary and the first street sketches. Week 2 is Quick Stop, then the Level 4 sketches. Week 3 is the corner crash, then the denser sketches and the lobby correction. Week 4 is the garage correction and a harder pass over the same scenes. The picture shows every fact a question asks. 80% is the mastery mark on the scoreboard. 95% means it was too easy. Neither mark locks the next picture.",
"استرجاع التفاصيل البصرية — 40 سؤالًا محسوبًا. صورة واحدة، دقيقتان، بلا ملاحظات، ثم تختفي. العبارات صحيحة أو خطأ. وبنود أخرى تسأل هل كان الشيء في الصورة. كل يوم في هذه الصفحة يبدأ بهذا التمرين. الأسبوع الأول هو سطو 7426 ورسوم الشوارع الأولى. الأسبوع الثاني هو كويك ستوب ثم رسوم المستوى 4. الأسبوع الثالث هو حادث الزاوية ثم الرسوم الأكثف وتصحيح الردهة. الأسبوع الرابع هو تصحيح المرآب ومرور أصعب على المشاهد نفسها. الصورة تُظهر كل حقيقة يسأل عنها سؤال. 80% علامة الإتقان على لوحة النتائج. 95% تعني أنها كانت أسهل مما ينبغي. لا علامة منهما تقفل الصورة التالية.")}</li>
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


MEM_BY_DAY = {
    1: ["b7426-1"],
    2: ["L1-1", "L1-2"],
    3: ["L1-3", "L2-1"],
    4: ["L2-2", "L2-3"],
    5: ["b7426-2"],
    6: ["L3-1", "L3-2"],
    7: ["L3-3", "b7426-3"],
    8: ["qstop-1"],
    9: ["qstop-2"],
    10: ["qstop-3"],
    11: ["L4-1"],
    12: ["L4-2"],
    13: ["L4-3"],
    14: ["L4-4"],
    15: ["corner-1"],
    16: ["corner-2"],
    17: ["corner-3"],
    18: ["L5-1"],
    19: ["L5-2"],
    20: ["L5-3"],
    21: ["L6-1"],
    22: ["L6-2"],
    23: ["qstop-3"],
    24: ["corner-2"],
    25: ["corner-3"],
    26: ["L6-1"],
    27: ["L6-2"],
    28: ["b7426-3"],
}
MEM_TITLES = {}


def _qpack(rows):
    out = []
    for en, ar, oe, oa, ans in rows:
        out.append({
            "en": en,
            "ar": ar,
            "opts": [[a, b] for a, b in zip(oe, oa)],
            "ans": ans,
            "why": ["It is in the picture.", "هذا في الصورة."],
        })
    return out


def load_memory():
    """Every picture and street sketch, with questions that match that scene."""
    photos = {q["id"]: q for q in hesna_photo.quizzes()}
    base = json.loads((ROOT / "scripts" / "hesna_memory_base.json").read_text())
    sketches = {s["id"]: s for s in base["S"]}
    extra = {s["id"]: s for s in hesna_scenes.new_scenes({"C": base["C"], "I": base["I"], "V": base["V"]})}
    known = set(photos) | set(sketches) | set(extra)
    assigned = {mid for ids in MEM_BY_DAY.values() for mid in ids}
    missing = sorted(known - assigned)
    if missing:
        raise SystemExit("memory drills not on a day: " + ",".join(missing))
    mem = {}
    titles = {}
    for ids in MEM_BY_DAY.values():
        for mid in ids:
            if mid in mem:
                continue
            if mid in photos:
                src = photos[mid]
                titles[mid] = (src["title"][0], src["title"][1])
                mem[mid] = {
                    "id": mid,
                    "secs": src["secs"],
                    "img": src["img"],
                    "alt": src["alt"],
                    "title_en": src["title"][0],
                    "title_ar": src["title"][1],
                    "blurb_en": src["blurb"][0],
                    "blurb_ar": src["blurb"][1],
                    "qs": _qpack(src["q"]),
                }
            else:
                src = sketches.get(mid) or extra.get(mid)
                if not src:
                    raise SystemExit("missing memory drill " + mid)
                titles[mid] = (f"Street sketch {mid}", f"رسم الشارع {mid}")
                desc = src.get("desc") or [
                    "This scene, 2 minutes. Every question is something the picture shows.",
                    "هذا المشهد، دقيقتان. كل سؤال عن شيء تُظهره الصورة.",
                ]
                row = {
                    "id": mid,
                    "secs": src.get("secs", 120),
                    "title_en": titles[mid][0],
                    "title_ar": titles[mid][1],
                    "blurb_en": desc[0],
                    "blurb_ar": desc[1],
                    "qs": _qpack(src["q"]),
                }
                if src.get("svg"):
                    row["svg"] = src["svg"]
                else:
                    row.update({
                        "tm": src.get("tm"),
                        "st": src.get("st"),
                        "cr": src.get("cr"),
                        "b": src.get("b"),
                        "p": src.get("p"),
                        "v": src.get("v"),
                    })
                mem[mid] = row
            if len(mem[mid]["qs"]) != 45:
                raise SystemExit(f"{mid} has {len(mem[mid]['qs'])} questions")
            if mem[mid].get("secs") != 120:
                raise SystemExit(f"{mid} is not a 2-minute scene")
    return mem, titles


def lesson(d):
    week = (d["n"] - 1) // 7 + 1
    period = ((d["n"] - 1) % 7) + 1
    meta_en = (
        f"Week {week}, day {period} of 7. Open now. "
        f"Target {d['target']}. Budget {d['budgetMin']} min. "
        f"The scoreboard marks 80% as mastered and 95% as too easy. The score never locks another day."
    )
    meta_ar = (
        f"الأسبوع {week}، اليوم {period} من 7. مفتوح الآن. "
        f"الهدف {d['target']}. الميزانية {d['budgetMin']} د. "
        f"لوحة النتائج تعلّم 80% كإتقان و95% كأسهل مما ينبغي. النتيجة لا تقفل يومًا آخر."
    )
    drills = MEM_BY_DAY.get(d["n"], [])
    drill_en = "; ".join(MEM_TITLES[i][0] for i in drills)
    drill_ar = "؛ ".join(MEM_TITLES[i][1] for i in drills)
    drill = (
        f'<p class="sp-ph">{bi("This day starts with: " + drill_en + ". 2 minutes, then the picture hides, then questions about details that picture shows. The other quizzes come after.", "هذا اليوم يبدأ بـ: " + drill_ar + ". دقيقتان، ثم تختفي الصورة، ثم أسئلة عن تفاصيل تُظهرها تلك الصورة. الاختبارات الأخرى تأتي بعد ذلك.")}</p>'
        if drills else ""
    )
    start = (
        f'<p><button type="button" class="sp-btn" data-day="{d["n"]}">'
        f'{bi("Start this day", "ابدئي هذا اليوم")}</button></p>'
    )
    return (
        f'<article class="hs-lesson" id="day-{d["n"]}"><h3>{bi(d["en"], d["ar"])}</h3>'
        f'{start}{drill}<p>{bi(d["body_en"], d["body_ar"])}</p><p class="sp-ph">{bi(meta_en, meta_ar)}</p></article>'
    )


WEEK_NAME_AR = {1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع"}


def week_section(num, lessons, blurb_en, blurb_ar):
    name_en = f"Week {num}"
    name_ar = "الأسبوع " + WEEK_NAME_AR[num]
    btn_en = f"Open Week {num}"
    btn_ar = "افتحي الأسبوع " + WEEK_NAME_AR[num]
    cue = (
        f'<span class="hs-pack-cue">('
        f'{bi("review below or ", "راجعي أدناه أو ")}'
        f'<button type="button" class="sp-btn hs-pack-start" data-week="{num}" id="hs-pack-btn-{num}">{bi(btn_en, btn_ar)}</button>'
        f'{bi(" here", " هنا")}'
        f')</span>'
    )
    return (
        f'<section class="sp-week" id="week-{num}">'
        f'<h2 class="hs-pack-head"><span class="hs-pack-title">{bi(name_en, name_ar)}</span> {cue}</h2>'
        f'<p id="hs-pack-note-{num}" class="sp-ph"></p>'
        f'<p>{bi(blurb_en, blurb_ar)}</p>'
        f'<div class="hs-pack">{"".join(lessons)}</div>'
        f'</section>'
    )


def study_html(payload):
    weeks = []
    for num in (1, 2, 3, 4):
        lo, hi = (num - 1) * 7 + 1, num * 7
        weeks.append([lesson(d) for d in DAYS if lo <= d["n"] <= hi])
    ladder = "".join(
        f'<span>{bi("D"+str(d["n"])+" · t"+str(d["tier"]), "ي"+str(d["n"])+" · م"+str(d["tier"]))}</span>'
        for d in DAYS
    )
    rules = f'''<section><h2>{bi("How the bar moves", "كيف يتحرك المستوى")}</h2>
<p>{bi("Four weeks. Every week, every day, every drill, and every quiz is open. Nothing waits on another score. Week 1 is the baseline. Week 2 is harder. Week 3 is harder again. Week 4 is the hardest. A sitting that is too easy still raises the tier, and the score is saved.",
"أربعة أسابيع. كل أسبوع وكل يوم وكل تمرين وكل اختبار مفتوح. لا شيء ينتظر نتيجة أخرى. الأسبوع الأول خط الأساس. الثاني أصعب. الثالث أصعب مرة أخرى. الرابع هو الأصعب. والجلسة السهلة أكثر من اللازم ترفع المستوى رغم ذلك، والنتيجة تُحفظ.")}</p>
<ul>
<li>{bi("Each day starts with a memory drill: 2 minutes on one scene, then it hides, then questions about details that scene shows. Written A/B, reading, logic, and the other quizzes come after that. Biodata is the practice section on this page.", "كل يوم يبدأ بتمرين ذاكرة: دقيقتان على مشهد واحد، ثم يختفي، ثم أسئلة عن تفاصيل يُظهرها ذلك المشهد. الكتابة A/B والقراءة والمنطق وبقية الاختبارات تأتي بعد ذلك. والبيانات الشخصية هي قسم التدريب في هذه الصفحة.")}</li>
<li>{bi("80% on the core is the mastery mark on the scoreboard. Core 95% or higher, or core 90%+ finished under the too-fast time: too easy. A harder set is offered in that sitting, and it is the one the scoreboard counts. You can leave it and open any other day.", "80% في الجوهر علامة الإتقان على لوحة النتائج. جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في زمن أقصر من حد السرعة: أسهل مما ينبغي. تُعرض مجموعة أصعب في تلك الجلسة، وهي التي تحسبها لوحة النتائج. يمكنك تركها وفتح أي يوم آخر.")}</li>
<li>{bi("The official exam has four sections, below. On this page the core that moves the tier is reading, listening, comprehension, observation, and the extra logic drills. Written A/B and four-choice grammar are a separate track. Biodata is honest practice, not a key.", "للامتحان الرسمي أربعة أقسام، في الأسفل. في هذه الصفحة الجوهر الذي يحرّك المستوى هو القراءة والاستماع والفهم والملاحظة وتدريبات المنطق الإضافية. الكتابة A/B وقواعد الأربع خيارات مسار منفصل. والبيانات الشخصية تدريب صادق، لا مفتاح.")}</li>
<li>{bi("Core under 70%: the next day you open can still start with a short bridge, so a miss is not a wall. The bridge is an offer. It is not a lock.", "جوهر تحت 70%: اليوم التالي الذي تفتحينه يمكن أن يبدأ بجسر قصير، حتى لا يصير التعثّر جدارًا. الجسر عرض. وهو ليس قفلًا.")}</li>
<li>{bi("Day 1 probes: 3 of 4 harder probes right, with the ordinary core at 85%+, already counts as too easy. The grammar traps may still be soft. That is allowed. Later days still offer those families.", "مجسّات اليوم 1: ثلاثة من أربعة مجسّات أصعب صحيحة، مع جوهر عادي عند 85% أو أكثر، تُحسب أصلًا أسهل مما ينبغي. فخاخ القواعد قد تبقى لينة. وهذا مسموح. والأيام اللاحقة ما زالت تعرض تلك العائلات.")}</li>
<li>{bi("Grammar drills the families under 80%. A family at 95% across 4 or more items is retired from new drills. The Week 1 retest rescores Day 1's soft families on new sentences, so the rise is visible. A family still under 80% stays on the scoreboard. It does not close a week.", "القواعد تدرّب العائلات تحت 80%. والعائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف عن التمارين الجديدة. وإعادة القياس في الأسبوع الأول تعيد قياس عائلات اليوم 1 اللينة بجمل جديدة، فيظهر الارتفاع. والعائلة التي تبقى تحت 80% تبقى على لوحة النتائج. وهي لا تغلق أسبوعًا.")}</li>
<li>{bi("Every picture and every street sketch is inside a day, and also on the memory page. Same scenes, same questions. Week 4 repeats the hardest scenes while the written work stays at the top tier.", "كل صورة وكل رسم شارع داخل يوم، وأيضًا في صفحة الذاكرة. المشاهد نفسها والأسئلة نفسها. الأسبوع الرابع يعيد أصعب المشاهد بينما يبقى العمل الكتابي في أعلى مستوى.")}</li>
<li>{bi("End state for the four weeks: about 98% on this kind of page. Harder items, not a softer key.", "حالة نهاية الأسابيع الأربعة: نحو 98% على صفحة من هذا النوع. بنود أصعب، لا مفتاح أسهل.")}</li>
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
    draw = (ROOT / "scripts" / "hesna_draw.js").read_text()
    adapt = (ROOT / "scripts" / "hesna_adapt.js").read_text()
    run = (ROOT / "scripts" / "hesna_run.js").read_text()
    day_opts = "".join(
        f'<option value="{d["n"]}" data-en="{E(d["en"])}" data-ar="{E(d["ar"])}"></option>'
        for d in DAYS
    )
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr" class="dark">
<head>
<meta charset="UTF-8"><meta name="color-scheme" content="dark"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>Hassnaa's Four-Week HPD Study Plan | خطة حسناء الدراسية</title>
<link rel="stylesheet" href="/styles.css?v=20261026b">
{PWA}
<style>{CSS}</style>
</head>
<body>
<main data-pagefind-ignore="all">
{NAV.format(g=' aria-current="page"', m='')}
<div class="sp-top"><h1>{bi("Hassnaa's HPD Study Plan", "خطة حسناء")}</h1><button id="sp-toggle" type="button" aria-label="Switch language / تغيير اللغة"><span data-en>العربية</span><span data-ar>English</span></button></div>
<p class="hs-dayline"><select id="hs-day" aria-label="Day">{day_opts}</select></p>
<div id="hs-app"></div>
<div id="hs-summary"></div>
<details class="hs-ref"><summary>{bi("Biodata", "البيانات الشخصية")}</summary>
{biodata_block()}
</details>
<p><button type="button" class="sp-btn" id="hs-reset">{bi("Reset saved scores", "امسحي النتائج المحفوظة")}</button></p>
</main>
<script>window.HS={payload};</script>
<script>{draw}</script>
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
    scenes = photos + base["S"] + extra
    first_week = {}
    order = {}
    n = 0
    for day in range(1, 29):
        for mid in MEM_BY_DAY.get(day, []):
            if mid in first_week:
                continue
            first_week[mid] = (day - 1) // 7 + 1
            order[mid] = n
            n += 1
    for scene in scenes:
        scene["week"] = first_week.get(scene["id"], 4)
    scenes.sort(key=lambda s: (s.get("week", 4), order.get(s["id"], 999)))
    data = {
        "S": scenes,
        "C": base["C"], "I": base["I"], "V": base["V"], "BC": base["BC"],
        "BLURB": hesna_scenes.BLURBS,
    }
    raw = (ROOT / "scripts" / "hesna_memory_shell.html").read_text()
    needle = "window.MD_DATA={};"
    if needle not in raw:
        raise SystemExit("MD_DATA placeholder missing")
    raw = raw.replace(needle, "window.MD_DATA=" + js(data) + ";", 1)
    anchor = "<script>(function(){var D=window.MD_DATA"
    draw = (ROOT / "scripts" / "hesna_draw.js").read_text()
    if anchor not in raw:
        raise SystemExit("memory shell anchor missing")
    if "function hesnaScene" not in raw:
        raw = raw.replace(anchor, "<script>\n" + draw + "\n</script>\n" + anchor, 1)
    return raw


def audit_scenes():
    """Every pictured fact a Week 1 or Week 2 question asks has to be on the scene."""
    base = json.loads((ROOT / "scripts" / "hesna_memory_base.json").read_text())
    l44 = next(s for s in base["S"] if s["id"] == "L4-4")
    if l44["q"][-1][2][l44["q"][-1][4]] != "7":
        raise SystemExit("L4-4 still hides the drawn driver")
    for tok in ("WALLET", "DOG", "SKATE", "CANE", "PHONE", "HYDRANT", "UMBRELLA", "BRAID", "DRIVER"):
        if tok not in l44["svg"]:
            raise SystemExit("L4-4 scene missing " + tok)
    extra = hesna_scenes.new_scenes({"C": hesna_scenes.C, "I": hesna_scenes.I, "V": hesna_scenes.V})
    by_id = {s["id"]: s.get("svg") or "" for s in extra}
    need = {
        "L6-1": ["Tuesday", "KEYS", "blue fob", "STAIRS", "HOOD", "RAIL", "SILVER", "beard", "sunglasses", "backpack blue, then black"],
        "L6-2": ["Wednesday", "ENGINE ON", "ENGINE OFF", "LEFT REAR", "DENT", "CART by pillar C", "BOOTH", "STALL 20", "disregard 414", "keep 441", "OIL under 441"],
    }
    for sid, toks in need.items():
        for tok in toks:
            if tok not in by_id[sid]:
                raise SystemExit(f"{sid} scene missing {tok}")
    draw = (ROOT / "scripts" / "hesna_draw.js").read_text()
    if 'p.i === "cup"' not in draw or "q0 11 -7 11" not in draw:
        raise SystemExit("street cup is not drawn")


def main():
    audit_scenes()
    photo_stats = hesna_photo.check()
    stats = hesna_banks.check_banks()
    stats["photos"] = photo_stats
    reads, comps, listens, obs = hesna_banks.passages()
    items = hesna_banks.all_items()
    # Drop callables; items are plain dicts.
    if [d["n"] for d in DAYS] != list(range(1, 29)):
        raise SystemExit("the plan must be days 1 through 28")
    for d in DAYS:
        if not MEM_BY_DAY.get(d["n"]):
            raise SystemExit(f"day {d['n']} has no memory drill")
        if d["tier"] < (d["n"] - 1) // 7:
            raise SystemExit(f"day {d['n']} is easier than its week")
    days = []
    for d in DAYS:
        row = {k: d[k] for k in ("n", "tier", "depth", "budgetMin", "tooFastMin", "take") if k in d}
        row["title_en"] = d["en"]
        row["title_ar"] = d["ar"]
        row["body_en"] = d["body_en"]
        row["body_ar"] = d["body_ar"]
        if d.get("mode"):
            row["mode"] = d["mode"]
        if d.get("stretchTake"):
            row["stretchTake"] = d["stretchTake"]
        row["mem"] = list(MEM_BY_DAY.get(d["n"], []))
        days.append(row)
    mem, titles = load_memory()
    global MEM_TITLES
    MEM_TITLES = titles
    missing = [i for ids in MEM_BY_DAY.values() for i in ids if i not in mem]
    if missing:
        raise SystemExit("missing memory drills " + ",".join(missing))
    payload = js({
        "days": days,
        "items": items,
        "reads": reads,
        "comps": comps,
        "listens": listens,
        "obs": obs,
        "mem": mem,
    })
    STUDY.write_text(study_html(payload), encoding="utf-8")
    MEM.write_text(memory_html(), encoding="utf-8")
    print("wrote", STUDY, STUDY.stat().st_size)
    print("wrote", MEM, MEM.stat().st_size)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
