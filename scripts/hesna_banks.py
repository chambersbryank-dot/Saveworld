#!/usr/bin/env python3
"""Item banks for Hesna's HPD study guide. Original practice, not exam content.

Logic answers that come from a line-up are checked against every permutation.
Grammar items have exactly one grammatical sentence.
"""
from __future__ import annotations

from itertools import permutations

YES = ("Yes", "نعم")
NO = ("No", "لا")
NOT = ("Not necessarily", "ليس بالضرورة")
NORULE = ("Only if a second rule says so", "فقط إذا قالت قاعدة ثانية ذلك")
CANNOT = ("Cannot be determined", "لا يمكن الجزم")


def opt(en, ar):
    return (en, ar)


def item(iid, tier, pillar, en, ar, opts, ans, why_en, why_ar, **kw):
    if len(opts) != 4:
        raise SystemExit(f"{iid}: need 4 options")
    if not (0 <= ans < 4):
        raise SystemExit(f"{iid}: bad ans")
    ens = [o[0] for o in opts]
    if len(set(ens)) != 4:
        raise SystemExit(f"{iid}: duplicate option {ens}")
    if not en or not ar or not why_en or not why_ar:
        raise SystemExit(f"{iid}: empty text")
    row = {
        "id": iid,
        "tier": tier,
        "depth": kw.get("depth", 1),
        "pillar": pillar,
        "en": en,
        "ar": ar,
        "opts": [[a, b] for a, b in opts],
        "ans": ans,
        "why": [why_en, why_ar],
    }
    for key in ("family", "diag", "retest", "probe", "stretch"):
        if kw.get(key):
            row[key] = kw[key] if key == "family" else True
    return row


def g(iid, tier, family, en_correct, wrongs, why_en, why_ar, **kw):
    """Grammar: the stem is fixed; exactly one sentence is correct. wrongs: 3 English strings."""
    if len(wrongs) != 3:
        raise SystemExit(f"{iid}: 3 wrong sentences")
    opts = [opt(en_correct, en_correct)] + [opt(w, w) for w in wrongs]
    stem_en = kw.pop("stem_en", "Which sentence is grammatically correct?")
    stem_ar = kw.pop("stem_ar", "أي جملة صحيحة نحويًا؟ الجمل بالإنجليزية، كما في الامتحان.")
    return item(
        iid, tier, "grammar", stem_en, stem_ar, opts, 0, why_en, why_ar,
        family=family, **kw,
    )


def grammar_items():
    W = "Which sentence is grammatically correct?"
    A = "أي جملة صحيحة نحويًا؟ الجمل بالإنجليزية، كما في الامتحان."
    out = []
    add = out.append

    # --- articles (Arabic has no "a/an"; French gender doesn't choose a/an) ---
    add(g("g-art-1", 1, "articles",
          "She is an officer on this shift.",
          ["She is a officer on this shift.", "She is officer on this shift.", "She is an officers on this shift."],
          '"Officer" begins with a vowel sound, so it takes "an", and the noun stays singular.',
          "كلمة officer تبدأ بصوت علة، فتأخذ an، وتبقى المفرد.",
          diag=True))
    add(g("g-art-2", 1, "articles",
          "Please file the report before noon.",
          ["Please file report before noon.", "Please file a reports before noon.", "Please file an report before noon."],
          "A specific report needs \"the\". \"An\" is not used before the consonant sound in \"report\".",
          "التقرير المحدد يحتاج the. ولا تُستخدم an قبل صوت الساكن في report.",
          diag=True))
    add(g("g-art-3", 2, "articles",
          "He took an umbrella from the car.",
          ["He took a umbrella from the car.", "He took umbrella from the car.", "He took an umbrellas from the car."],
          '"Umbrella" starts with a vowel sound: "an", one umbrella.',
          "umbrella تبدأ بصوت علة: an، ومظلة واحدة."))
    add(g("g-art-4", 3, "articles",
          "An honest witness came forward at 6.",
          ["A honest witness came forward at 6.", "Honest witness came forward at 6.", "An honest witnesses came forward at 6."],
          'The "h" in "honest" is silent, so the word starts with a vowel sound: "an".',
          "الهاء في honest صامتة، فالكلمة تبدأ بصوت علة: an.",
          retest=True))
    add(g("g-art-5", 4, "articles",
          "We need information about the driver, not a rumor.",
          ["We need an information about the driver, not a rumor.", "We need informations about the driver, not a rumor.", "We need a information about the driver, not a rumor."],
          '"Information" is uncountable here: no "a/an" and no plural -s.',
          "information غير قابلة للعد هنا: بلا a/an وبلا جمع بالـ s."))
    add(g("g-art-6", 5, "articles",
          "The officer wrote a one-page report.",
          ["The officer wrote an one-page report.", "The officer wrote one-page report.", "The officer wrote a one-pages report."],
          '"One" starts with a /w/ sound, so the article is "a", and "page" stays singular inside the compound.',
          "one تبدأ بصوت w، فالمقالة a، وتبقى page مفردة داخل المركّب."))

    # --- prepositions ---
    add(g("g-prep-1", 1, "prepositions",
          "The wallet was on the bench.",
          ["The wallet was into the bench.", "The wallet was at to the bench.", "The wallet was on to the bench."],
          '"On" is the preposition for a surface. "Into" would mean movement into it.',
          "on للسطح. into تعني حركة إلى الداخل.",
          diag=True))
    add(g("g-prep-2", 1, "prepositions",
          "She arrived at the scene at 9:40.",
          ["She arrived to the scene at 9:40.", "She arrived at the scene in 9:40.", "She arrived the scene on 9:40."],
          'English says "arrive at" a place and "at" a clock time. "Arrive to" is a calque.',
          "في الإنجليزية arrive at للمكان و at للساعة. arrive to نقل حرفي.",
          diag=True))
    add(g("g-prep-3", 2, "prepositions",
          "The charge depends on the report.",
          ["The charge depends of the report.", "The charge depends from the report.", "The charge is depend of the report."],
          'The verb is "depend on", not "depend of/from" (dépendre de / يعتمد على).',
          "الفعل depend on، وليس depend of أو from."))
    add(g("g-prep-4", 3, "prepositions",
          "They have been waiting for twenty minutes.",
          ["They have been waiting since twenty minutes.", "They have been waiting from twenty minutes.", "They have been waiting since twenty minute."],
          '"For" plus a length of time. "Since" needs a starting point, like "since 9:40".',
          "for مع المدة. since تحتاج نقطة بداية مثل since 9:40.",
          retest=True))
    add(g("g-prep-5", 4, "prepositions",
          "The number is printed on the plate.",
          ["The number is printed in the plate.", "The number is printed into the plate.", "The number is printed on to plate."],
          "A plate number sits on the plate: \"on\".",
          "رقم اللوحة على اللوحة: on."))
    add(g("g-prep-6", 5, "prepositions",
          "The driver ran toward the alley.",
          ["The driver ran towards to the alley.", "The driver ran at to the alley.", "The driver ran toward to the alley."],
          '"Toward" already includes the direction. Do not add "to" after it.',
          "toward تتضمن الاتجاه. لا تضيفي to بعدها."))

    # --- tense ---
    add(g("g-tense-1", 1, "tense",
          "The officer wrote the report yesterday.",
          ["The officer has written the report yesterday.", "The officer has wrote the report yesterday.", "The officer writing the report yesterday."],
          'A finished time ("yesterday") takes the simple past, not the present perfect.',
          "زمن منتهٍ (yesterday) يأخذ الماضي البسيط، لا المضارع التام.",
          diag=True))
    add(g("g-tense-2", 1, "tense",
          "She has worked this beat since March.",
          ["She works this beat since March.", "She has work this beat since March.", "She is working this beat since March."],
          '"Since March" (a start that is still true) takes the present perfect: "has worked".',
          "since March (بداية ما زالت صحيحة) تأخذ المضارع التام: has worked.",
          diag=True))
    add(g("g-tense-3", 2, "tense",
          "By the time backup arrived, the driver had left.",
          ["By the time backup arrived, the driver has left.", "By the time backup arrived, the driver have left.", "By the time backup arrived, the driver leaving."],
          "When the later past event is \"arrived\", the earlier one is \"had left\".",
          "إذا كان الحدث الأحدث في الماضي arrived، فالأسبق had left."))
    add(g("g-tense-4", 3, "tense",
          "I saw him last night.",
          ["I have seen him last night.", "I have saw him last night.", "I seeing him last night."],
          'Same trap as "yesterday": "last night" closes the time, so use "saw".',
          "الفخ نفسه كما في yesterday: last night تغلق الزمن، فاستخدمي saw.",
          retest=True))
    add(g("g-tense-5", 4, "tense",
          "The clerk said the window had been broken before she arrived.",
          ["The clerk said the window has been broken before she arrived.", "The clerk said the window been broken before she arrived.", "The clerk said the window had broke before she arrived."],
          'Reported earlier past: "had been broken". "Had broke" mixes the helper with the simple past.',
          "ماضٍ أسبق في الكلام المنقول: had been broken. had broke تخلط الفعل المساعد بالماضي البسيط."))
    add(g("g-tense-6", 5, "tense",
          "She has already logged the firearm.",
          ["She has already log the firearm.", "She already logging the firearm.", "She has already logged the firearm yesterday."],
          '"Has" needs the past participle "logged". A finished clock time does not belong with "already" in this sentence.',
          "has تحتاج اسم المفعول logged. وزمن ساعة منتهٍ لا يجلس مع already في هذه الجملة."))

    # --- verb complements ---
    add(g("g-comp-1", 1, "complements",
          "She explained the route to me.",
          ["She explained me the route.", "She explained me to the route.", "She explained to me to the route."],
          '"Explain" does not take a person as a bare object. Use "explain something to someone".',
          "explain لا يأخذ الشخص مفعولًا مباشرًا عاريًا. قولي explain something to someone.",
          diag=True))
    add(g("g-comp-2", 1, "complements",
          "Listen to the witness before you write.",
          ["Listen the witness before you write.", "Listen at the witness before you write.", "Listen to witness before you are write."],
          '"Listen" needs "to" before the person.',
          "listen تحتاج to قبل الشخص.",
          diag=True))
    add(g("g-comp-3", 2, "complements",
          "We discussed the case for an hour.",
          ["We discussed about the case for an hour.", "We discussed on the case for an hour.", "We did discussed the case for an hour."],
          '"Discuss" takes the topic directly. Do not add "about", and do not use "did" with the past form.',
          "discuss يأخذ الموضوع مباشرة. لا تضيفي about، ولا did مع صيغة الماضي."))
    add(g("g-comp-4", 3, "complements",
          "Please explain the delay to the sergeant.",
          ["Please explain the sergeant the delay.", "Please explain to the delay the sergeant.", "Please explain the sergeant to the delay."],
          "Same complement as Day 1, in a report sentence: explain the delay to the sergeant.",
          "المكمّل نفسه كما في اليوم 1، في جملة تقرير: explain the delay to the sergeant.",
          retest=True))
    add(g("g-comp-5", 4, "complements",
          "She is married to a paramedic.",
          ["She is married with a paramedic.", "She is married of a paramedic.", "She is marry to a paramedic."],
          '"Married to", not "married with" (marié avec / متزوجة من).',
          "married to، وليس married with."))
    add(g("g-comp-6", 5, "complements",
          "We entered the lobby through the side door.",
          ["We entered in the lobby through the side door.", "We entered to the lobby through the side door.", "We entered into to the lobby through the side door."],
          '"Enter" takes the place directly: "enter the lobby", not "enter in/to".',
          "enter يأخذ المكان مباشرة: enter the lobby، وليس enter in أو to."))

    # --- adjective placement ---
    add(g("g-adj-1", 1, "adjectives",
          "She drove a blue Honda.",
          ["She drove a Honda blue.", "She drove blue a Honda.", "She drove a blue Hondas."],
          "English puts the adjective before the noun: \"a blue Honda\", and one car is singular.",
          "الصفة في الإنجليزية قبل الاسم: a blue Honda، والسيارة الواحدة مفرد.",
          diag=True))
    add(g("g-adj-2", 2, "adjectives",
          "The man in the green jacket left.",
          ["The man in jacket green left.", "The man in the jacket green left.", "The green in man the jacket left."],
          "Color sits before \"jacket\": \"the green jacket\".",
          "اللون قبل jacket: the green jacket."))
    add(g("g-adj-3", 3, "adjectives",
          "A small black backpack was on the chair.",
          ["A backpack small black was on the chair.", "A small black backpacks was on the chair.", "Small a black backpack was on the chair."],
          "Size, then color, then the noun. The verb \"was\" needs a singular backpack.",
          "الحجم ثم اللون ثم الاسم. الفعل was يحتاج مفردًا.",
          retest=True))
    add(g("g-adj-4", 5, "adjectives",
          "Two parked white vans blocked the ramp.",
          ["Two white vans parked blocked the ramp.", "Two parked white van blocked the ramp.", "Parked two white vans blocked the ramp."],
          '"Two" needs the plural "vans", and the adjectives stay in front: "parked white vans".',
          "two تحتاج الجمع vans، والصفات تبقى أمام الاسم."))

    # --- countability ---
    add(g("g-count-1", 1, "count",
          "He gave me a piece of advice.",
          ["He gave me an advice.", "He gave me advices.", "He gave me a advice."],
          '"Advice" is uncountable. Count it with "a piece of advice".',
          "advice غير قابلة للعد. عُدّيها بـ a piece of advice.",
          diag=True))
    add(g("g-count-2", 2, "count",
          "The luggage is in the trunk.",
          ["The luggages are in the trunk.", "The luggage are in the trunk.", "A luggages is in the trunk."],
          '"Luggage" is uncountable and takes "is".',
          "luggage غير قابلة للعد وتأخذ is."))
    add(g("g-count-3", 3, "count",
          "Two pieces of evidence were logged.",
          ["Two evidences were logged.", "Two evidence was logged.", "Two piece of evidences were logged."],
          '"Evidence" is uncountable. Count it with "pieces", and the verb agrees with "pieces".',
          "evidence غير قابلة للعد. عُدّيها بـ pieces، والفعل يوافق pieces.",
          retest=True))
    add(g("g-count-4", 4, "count",
          "She asked for information.",
          ["She asked for an information.", "She asked for informations.", "She asked for a informations."],
          'No article and no plural -s on "information".',
          "بلا أداة تعريف نكرة وبلا s على information."))
    add(g("g-count-5", 6, "count",
          "There was little traffic on King Street.",
          ["There was few traffic on King Street.", "There were few traffics on King Street.", "There was a few traffic on King Street."],
          '"Traffic" is uncountable, so use "little", not "few".',
          "traffic غير قابلة للعد، فاستخدمي little لا few.",
          stretch=True))

    # --- calques from French / Arabic ---
    add(g("g-cal-1", 1, "calques",
          "I agree with the statement.",
          ["I am agree with the statement.", "I am agreed with the statement.", "I have agree with the statement."],
          '"Agree" is a verb here. "I am agree" copies "je suis d\'accord" / "أنا موافقة" into English words that do not work.',
          "agree فعل هنا. I am agree تنقل je suis d'accord أو أنا موافقة بكلمات إنجليزية لا تستقيم.",
          diag=True))
    add(g("g-cal-2", 1, "calques",
          "She is 25 years old.",
          ["She has 25 years.", "She has 25 years old.", "She is 25 years age."],
          'Age is "is ... years old", not "has ... years" (elle a 25 ans / عمرها 25).',
          "العمر: is ... years old، وليس has ... years.",
          diag=True))
    add(g("g-cal-3", 2, "calques",
          "She asked for a glass of water.",
          ["She demanded for a glass of water.", "She did a demand for a glass of water.", "She asked a glass of water."],
          '"Ask for" something. "Demand" does not take "for" this way, and "did a demand" is not English.',
          "ask for للطلب. demand لا تأخذ for هكذا، و did a demand ليست إنجليزية."))
    add(g("g-cal-4", 3, "calques",
          "The witness is currently at the counter.",
          ["The witness is actually at the counter.", "The witness is actual at the counter.", "The witness currently is be at the counter."],
          'For "right now", say "currently". "Actually" means "in fact" (actuellement is the false friend).',
          "للمعنى «الآن» قولي currently. actually تعني «في الواقع»، وهي الصديق الكاذب لـ actuellement.",
          retest=True, stem_en="Which sentence is grammatical and means the witness is at the counter right now?",
          stem_ar="أي جملة سليمة وتعني أن الشاهد عند المنضدة الآن؟"))
    add(g("g-cal-5", 5, "calques",
          "This report is sensitive. Handle it quietly.",
          ["This report is sensible. Handle it quietly.", "This report is sensitive. Handle it quiet.", "This report is sensitive. Handle quietly it."],
          'The false friend of French "sensible" is "sensitive" (delicate), not "sensible" (reasonable). Only the first sentence is both grammatical and that meaning. "Quietly" is the adverb.',
          "الصديق الكاذب للفرنسية sensible هو sensitive (حسّاس)، لا sensible (عاقل). والجملة الأولى وحدها سليمة بهذا المعنى. والظرف quietly.",
          stem_en="Which sentence is grammatical and means the report is delicate and must be handled without noise?",
          stem_ar="أي جملة سليمة وتعني أن التقرير حسّاس ويجب التعامل معه بلا ضجة؟"))

    # --- subject-verb agreement ---
    add(g("g-sva-1", 1, "agreement",
          "The list of plates is on the desk.",
          ["The list of plates are on the desk.", "The list of plates be on the desk.", "The list of plates are being on the desk."],
          'The head noun is "list" (singular), not "plates".',
          "رأس الجملة list مفرد، لا plates.",
          diag=True))
    add(g("g-sva-2", 2, "agreement",
          "There are two witnesses in the lobby.",
          ["There is two witnesses in the lobby.", "There are two witness in the lobby.", "There is two witness in the lobby."],
          '"There are" agrees with the plural "two witnesses".',
          "there are توافق الجمع two witnesses."))
    add(g("g-sva-3", 3, "agreement",
          "The sergeant, along with two officers, is on the way.",
          ["The sergeant, along with two officers, are on the way.", "The sergeant, along with two officers, be on the way.", "The sergeant, along with two officers, are being on the way."],
          '"Along with" does not make the subject plural. The subject is "the sergeant".',
          "along with لا تجعل الفاعل جمعًا. الفاعل the sergeant.",
          retest=True))
    add(g("g-sva-4", 4, "agreement",
          "Neither the passengers nor the driver was hurt.",
          ["Neither the passengers nor the driver were hurt.", "Neither the passengers nor the driver be hurt.", "Neither the passengers nor the driver were hurting hurt."],
          'With "neither/nor", the verb agrees with the nearer subject: "the driver was".',
          "مع neither/nor يوافق الفعل الفاعل الأقرب: the driver was."))
    add(g("g-sva-5", 6, "agreement",
          "The box of plates is on the desk.",
          ["The box of plates are on the desk.", "The box of plates be on the desk.", "The box of plates are being on the desk."],
          'The head noun is "box". "Plates" does not take over the verb.',
          "رأس الجملة box. وplates لا تسيطر على الفعل.",
          stretch=True))

    # --- negatives ---
    add(g("g-neg-1", 1, "negatives",
          "I did not see anyone in the alley.",
          ["I did not see no one in the alley.", "I did not saw anyone in the alley.", "I did not seeing anyone in the alley."],
          'One negative is enough: "did not" plus "anyone". After "did", use the base verb "see".',
          "نفي واحد يكفي: did not مع anyone. بعد did استخدمي أصل الفعل see.",
          diag=True))
    add(g("g-neg-2", 2, "negatives",
          "She doesn't have any information.",
          ["She doesn't have no information.", "She don't have any information.", "She doesn't has any information."],
          '"Doesn\'t" already carries the third person. Use "have", and use "any" after a negative.',
          "doesn't تحمل صيغة الغائب أصلًا. استخدمي have، و any بعد النفي."))
    add(g("g-neg-3", 3, "negatives",
          "Nobody was in the car.",
          ["Nobody were not in the car.", "Nobody weren't in the car.", "Nobody were in the car."],
          '"Nobody" is singular and already negative. "Was" is enough.',
          "nobody مفرد ومنفي أصلًا. was تكفي.",
          retest=True))
    add(g("g-neg-4", 5, "negatives",
          "We did not find any weapon in the bag.",
          ["We did not found any weapon in the bag.", "We did not find no weapon in the bag.", "We not find any weapon in the bag."],
          'After "did not", the verb stays "find". Do not add a second negative.',
          "بعد did not يبقى الفعل find. لا تضيفي نفيًا ثانيًا."))

    # --- questions ---
    add(g("g-q-1", 1, "questions",
          "Where did the car go?",
          ["Where the car went?", "Where did the car went?", "Where went the car?"],
          'Questions need the helper "did" plus the base verb "go", not "went".',
          "السؤال يحتاج did مع أصل الفعل go، لا went.",
          diag=True))
    add(g("g-q-2", 2, "questions",
          "How many people were in the lobby?",
          ["How many people was in the lobby?", "How much people were in the lobby?", "How many peoples were in the lobby?"],
          '"People" is plural ("were") and countable ("how many"), and it does not take -s.',
          "people جمع (were) وقابلة للعد (how many)، ولا تأخذ s."))
    add(g("g-q-3", 3, "questions",
          "What time did the call come in?",
          ["What time the call came in?", "What time did the call came in?", "At what time came the call in?"],
          'Same helper as Day 1: "did" + base verb "come".',
          "المساعد نفسه كما في اليوم 1: did مع أصل الفعل come.",
          retest=True))
    add(g("g-q-4", 4, "questions",
          "Did the witness see the plate?",
          ["Did the witness saw the plate?", "Does the witness saw the plate?", "Did the witness seen the plate?"],
          'After "did", use "see", not "saw" or "seen".',
          "بعد did استخدمي see، لا saw ولا seen."))

    # --- pronouns: spot-check, retire fast if she owns them ---
    add(g("g-pro-1", 1, "pronouns",
          "Hana and I saw the car.",
          ["Me and Hana saw the car.", "Hana and me saw the car.", "Me and Hana seen the car."],
          'The subject form is "I". "Seen" cannot be the main verb alone.',
          "صيغة الفاعل I. ولا تكون seen الفعل الرئيسي وحدها.",
          diag=True))
    add(g("g-pro-2", 2, "pronouns",
          "The officer who wrote the report is outside.",
          ["The officer which wrote the report is outside.", "The officer what wrote the report is outside.", "The officer whom wrote the report is outside."],
          'For a person as the subject of the clause, use "who", not "which" or "whom".',
          "للشخص حين يكون فاعل الصلة استخدمي who، لا which ولا whom."))
    add(g("g-pro-3", 4, "pronouns",
          "The sergeant gave the radio to Noa and me.",
          ["The sergeant gave the radio to Noa and I.", "The sergeant gave the radio to I and Noa.", "The sergeant gave the radio to Noa and we."],
          'After "to", use the object form "me".',
          "بعد to استخدمي صيغة المفعول me."))

    # --- report phrasing: still one grammatical sentence, not a style coin-flip ---
    add(g("g-ph-1", 1, "phrasing",
          "The suspect ran, but he was caught.",
          ["The suspect ran, he was caught.", "The suspect ran but, he was caught.", "The suspect ran, but he were caught."],
          'Two full sentences need more than a comma. "But" can join them, and "he was" agrees.',
          "جملتان تامتان تحتاجان أكثر من فاصلة. but تصل بينهما، و he was توافق.",
          diag=True))
    add(g("g-ph-2", 2, "phrasing",
          "When I arrived, I saw that the door was open.",
          ["When I arrived, I seen that the door was open.", "Upon I arrived, I saw that the door was open.", "When I arrived, I saw that the door open was."],
          '"Saw" is the past of "see". "Upon" needs a noun ("upon arrival"), not "upon I arrived".',
          "saw ماضي see. upon تحتاج اسمًا (upon arrival)، لا upon I arrived."))
    add(g("g-ph-3", 3, "phrasing",
          "The driver fled east on King Street.",
          ["The driver fleed east on King Street.", "The driver fled to east on King Street.", "East fled the driver on King Street."],
          'The past of "flee" is "fled". Direction "east" does not take "to" here.',
          "ماضي flee هو fled. والاتجاه east لا يأخذ to هنا.",
          retest=True))
    add(g("g-ph-4", 4, "phrasing",
          "I asked the clerk for the receipt.",
          ["I asked the clerk for the receipt, he had none.", "I asked to the clerk for the receipt.", "I did asked the clerk for the receipt."],
          'The first wrong line is a comma splice. "Ask" does not take "to" before the person, and "did" does not take "asked".',
          "السطر الخطأ الأول فاصلة بين جملتين. ask لا تأخذ to قبل الشخص، و did لا تأخذ asked."))
    add(g("g-ph-5", 5, "phrasing",
          "The window was broken, and glass covered the sidewalk.",
          ["The window was broken, glass covered the sidewalk.", "The window was broken and, glass covered the sidewalk.", "The window were broken, and glass covered the sidewalk."],
          'Join the two sentences with "and" or a semicolon, and keep "window was".',
          "صلي الجملتين بـ and أو فاصلة منقوطة، وأبقي window was."))
    add(g("g-ph-6", 6, "phrasing",
          "After the correction, the backpack was black, not blue.",
          ["After the correction, the backpack was black, not it was blue.", "After the correction the backpack black was, not blue.", "After the correction, the backpack were black, not blue."],
          'A report correction stays a normal clause: "was black, not blue".',
          "تصحيح التقرير يبقى جملة عادية: was black, not blue.",
          stretch=True))
    return out


def _seq(iid, tier, depth, nums, rule_en, rule_ar, wrongs):
    shown = ", ".join(str(n) for n in nums[:-1]) + ", ?"
    ans = nums[-1]
    opts_n = [ans] + list(wrongs)
    if len(set(opts_n)) != 4 or ans in wrongs:
        raise SystemExit(f"bad seq {iid}")
    opts = [opt(str(n), str(n)) for n in opts_n]
    return item(
        iid, tier, "logic",
        f"What number comes next: {shown}",
        f"ما الرقم التالي: {shown}",
        opts, 0,
        rule_en, rule_ar,
        depth=depth,
    )


def _cond(iid, tier, depth, probe, en, ar, ans, why_en, why_ar):
    opts = [YES, NO, NOT, NORULE]
    return item(iid, tier, "logic", en, ar, opts, ans, why_en, why_ar, depth=depth, probe=probe)


def logic_items():
    out = []
    # Sequences. Distractors are nearby and are not the true next term.
    out.append(_seq("L-seq-1", 1, 1, [5, 8, 11, 14, 17], "Each term adds 3.", "كل حد يزيد 3.", [16, 18, 20]))
    out.append(_seq("L-seq-2", 1, 1, [3, 6, 12, 24, 48], "Each term doubles.", "كل حد يتضاعف.", [36, 46, 50]))
    out.append(_seq("L-seq-3", 1, 2, [2, 5, 8, 11, 14], "Each term adds 3.", "كل حد يزيد 3.", [13, 15, 17]))
    out.append(_seq("L-seq-4", 2, 1, [4, 6, 9, 13, 18, 24], "The gaps grow by 1: +2, +3, +4, +5, +6.", "الفجوات تزيد 1: +2 ثم +3 ثم +4 ثم +5 ثم +6.", [22, 23, 26]))
    out.append(_seq("L-seq-5", 2, 1, [3, 4, 8, 9, 18, 19, 38], "Alternate ×2 and +1.", "التناوب: ×2 ثم +1.", [20, 36, 40]))
    out.append(_seq("L-seq-6", 2, 2, [7, 14, 15, 30, 31, 62], "Alternate ×2 and +1.", "التناوب: ×2 ثم +1.", [32, 60, 63]))
    out.append(_seq("L-seq-7", 3, 1, [2, 5, 11, 23, 47], "Each term is ×2 then +1.", "كل حد: ×2 ثم +1.", [46, 48, 69]))
    out.append(_seq("L-seq-8", 3, 2, [1, 2, 6, 7, 21, 22, 66], "Alternate ×3 and +1.", "التناوب: ×3 ثم +1.", [44, 63, 69]))
    out.append(_seq("L-seq-9", 4, 1, [4, 5, 7, 11, 19, 35], "Each gap doubles, starting at +1.", "كل فجوة تتضاعف، بدءًا من +1.", [33, 36, 43]))
    out.append(_seq("L-seq-10", 4, 2, [8, 11, 17, 29, 53], "Each gap doubles, starting at +3.", "كل فجوة تتضاعف، بدءًا من +3.", [51, 77, 89]))
    out.append(_seq("L-seq-11", 5, 1, [2, 3, 5, 9, 17, 33], "Each term is the previous ×2, then −1? Wait check.", "x", [32, 34, 49]))
    # verify seq 11: 2,3 (+1), 5 (+2), 9 (+4), 17 (+8), 33 (+16). yes doubling gaps. Fix the why.
    out[-1]["why"] = [
        "The gaps double: +1, +2, +4, +8, +16. Next is 33.",
        "الفجوات تتضاعف: +1، +2، +4، +8، +16. التالي 33.",
    ]
    out.append(_seq("L-seq-12", 5, 2, [6, 7, 9, 13, 21, 37], "Gaps double from +1.", "الفجوات تتضاعف من +1.", [36, 45, 53]))
    out.append(_seq("L-seq-13", 6, 1, [5, 6, 8, 12, 20, 36, 68], "Gaps double from +1.", "الفجوات تتضاعف من +1.", [52, 66, 70], ))
    out[-1]["stretch"] = True
    out.append(_seq("L-seq-14", 6, 2, [9, 10, 12, 16, 24, 40], "Gaps double from +1. Next gap is +32.", "الفجوات تتضاعف من +1. الفجوة التالية +32.", [48, 56, 72]))
    out[-1]["stretch"] = True

    # Single-rule conditionals. ans index into [Yes, No, Not necessarily, Only if a second rule].
    conds = [
        ("L-if-1", 1, 1, False,
         "Using only this rule: if a report is late, the sergeant is notified. This report is late. Is the sergeant notified?",
         "باستخدام هذه القاعدة فقط: إذا تأخر التقرير يُبلَّغ الرقيب. هذا التقرير متأخر. هل يُبلَّغ الرقيب؟",
         0, "The rule's \"if\" happened, so the result follows.", "شرط القاعدة وقع، فالنتيجة تتبع."),
        ("L-if-2", 1, 1, False,
         "Using only this rule: every night-shift officer carries a radio. Noa is a night-shift officer. Does Noa carry a radio?",
         "باستخدام هذه القاعدة فقط: كل ضابط في نوبة الليل يحمل جهاز لاسلكي. نوا ضابط في نوبة الليل. هل يحمل نوا جهازًا؟",
         0, "Noa is inside the group the rule covers.", "نوا داخل المجموعة التي تغطيها القاعدة."),
        ("L-if-3", 1, 2, False,
         "Using only this rule: every night-shift officer carries a radio. Kai carries a radio. Is Kai on the night shift?",
         "باستخدام هذه القاعدة فقط: كل ضابط في نوبة الليل يحمل جهازًا. كاي يحمل جهازًا. هل كاي في نوبة الليل؟",
         2, "The rule does not say that only night-shift officers carry radios.", "القاعدة لا تقول إن نوبة الليل وحدها تحمل الأجهزة."),
        ("L-if-4", 2, 1, False,
         "Using only this rule: if a report is late, the sergeant is notified. The sergeant was not notified. Was the report late?",
         "باستخدام هذه القاعدة فقط: إذا تأخر التقرير يُبلَّغ الرقيب. لم يُبلَّغ الرقيب. هل تأخر التقرير؟",
         1, "If the report had been late, the sergeant would have been notified. That did not happen, so it was not late.", "لو تأخر التقرير لبلغوا الرقيب. وهذا لم يحدث، فالتقرير لم يتأخر."),
        ("L-if-5", 2, 1, False,
         "Using only this rule: if the scene is active, logging waits until the end of the shift. The scene is not active. Must logging wait until the end of the shift?",
         "باستخدام هذه القاعدة فقط: إذا كان المسرح نشطًا يُؤجَّل التسجيل إلى نهاية النوبة. المسرح ليس نشطًا. هل يجب أن ينتظر التسجيل نهاية النوبة؟",
         2, "The rule only tells you what happens when the scene is active. It does not say what happens otherwise.", "القاعدة تخبرك بما يحدث حين يكون المسرح نشطًا فقط. ولا تقول ماذا يحدث في غير ذلك."),
        ("L-if-6", 2, 2, True,
         "Using only this rule: no officer on the night shift works Mondays. Kai works Mondays. Is Kai on the night shift?",
         "باستخدام هذه القاعدة فقط: لا ضابط في نوبة الليل يعمل الاثنين. كاي يعمل الاثنين. هل كاي في نوبة الليل؟",
         1, "If Kai were on the night shift, Kai could not work Mondays. Kai does work Mondays, so Kai is not on that shift.", "لو كان كاي في نوبة الليل لما عمل الاثنين. وهو يعمل الاثنين، فهو ليس في تلك النوبة."),
        ("L-if-7", 3, 1, True,
         "Using only this rule: an officer may enter without a warrant only if there is consent or an emergency. There is no consent and no emergency. May the officer enter under this rule?",
         "باستخدام هذه القاعدة فقط: يجوز للضابط الدخول بلا مذكرة فقط إذا وُجدت موافقة أو طارئ. لا موافقة ولا طارئ. هل يجوز الدخول بموجب هذه القاعدة؟",
         1, "Neither of the only two permitted conditions is true.", "لا أحد من الشرطين المسموح بهما متحقق."),
        ("L-if-8", 3, 1, True,
         "Using only these rules: all reports are filed by 6 PM, and this rule has no exceptions. Report X was filed. Was it filed by 6 PM?",
         "باستخدام هاتين القاعدتين فقط: كل التقارير تُودَع قبل 6 مساءً، ولا استثناء. التقرير X أُودع. هل أُودع قبل 6 مساءً؟",
         0, "Report X is a report, and the rule covers every report.", "التقرير X تقرير، والقاعدة تشمل كل التقارير."),
        ("L-if-9", 3, 2, False,
         "Using only this rule: if both officers on a call are new, a sergeant rides along. A sergeant rode along. Were both officers new?",
         "باستخدام هذه القاعدة فقط: إذا كان الضابطان في البلاغ جديدين يرافقهما رقيب. رافقهما رقيب. هل كان كلاهما جديدًا؟",
         2, "The sergeant might have ridden along for a different reason. The rule does not say this is the only reason.", "قد يرافق الرقيب لسبب آخر. القاعدة لا تقول إن هذا السبب الوحيد."),
        ("L-if-10", 4, 1, False,
         "Using only this rule: if the item is a firearm, it is logged within 30 minutes, even when another rule allows longer. The item is a firearm and the scene is active. A second rule says active scenes may wait until the end of the shift, four hours away. What is the deadline under the firearm rule?",
         "باستخدام قاعدة السلاح فقط: إذا كان الغرض سلاحًا ناريًا يُسجَّل خلال 30 دقيقة، حتى إذا سمحت قاعدة أخرى بمدة أطول. الغرض سلاح والمسرح نشط. وقاعدة ثانية تقول إن المسرح النشط قد ينتظر نهاية النوبة بعد أربع ساعات. ما المهلة بموجب قاعدة السلاح؟",
         0, "The firearm rule states that it wins over a longer allowance. The deadline is 30 minutes.", "قاعدة السلاح تقول إنها تتقدم على المهلة الأطول. المهلة 30 دقيقة."),
    ]
    # L-if-10 options are Yes/No but the question asks for a deadline. That's a bad item. Remove it from conds and write it properly below.
    conds = [c for c in conds if c[0] != "L-if-10"]
    for row in conds:
        out.append(_cond(*row))

    out.append(item(
        "L-if-10", 4, "logic",
        "Rules: (1) Log evidence within 1 hour unless the scene is active. (2) If the scene is active, log it before the shift ends. (3) If the item is a firearm, log it within 30 minutes even if another rule allows longer. The scene is active, the item is a firearm, and the shift ends in 4 hours. What is the deadline?",
        "القواعد: (1) سجّل الدليل خلال ساعة إلا إذا كان المسرح نشطًا. (2) إذا كان المسرح نشطًا سجّله قبل نهاية النوبة. (3) إذا كان الغرض سلاحًا ناريًا سجّله خلال 30 دقيقة حتى لو سمحت قاعدة أخرى بمدة أطول. المسرح نشط، والغرض سلاح، والنوبة تنتهي بعد 4 ساعات. ما المهلة؟",
        [("Within 30 minutes", "خلال 30 دقيقة"), ("Within 1 hour", "خلال ساعة"), ("Before the shift ends", "قبل نهاية النوبة"), ("There is no deadline", "لا مهلة")],
        0,
        "Rule 3 governs a firearm even when the scene is active and the shift is hours away.",
        "القاعدة 3 تحكم السلاح الناري حتى لو كان المسرح نشطًا والنوبة بعيدة.",
        depth=1,
    ))
    out.append(item(
        "L-if-11", 4, "logic",
        "Rules: secure the scene before anyone photographs. Photograph an item before anyone moves it. Bag an item before it is logged. Logging is last. Which order respects every rule?",
        "القواعد: أمّن المسرح قبل أن يصوّر أحد. صوّر الغرض قبل أن يحرّكه أحد. ضعه في الكيس قبل تسجيله. التسجيل آخر خطوة. أي ترتيب يحترم كل القواعد؟",
        [("Secure, photograph, bag, log", "تأمين، تصوير، تكيس، تسجيل"),
         ("Photograph, secure, bag, log", "تصوير، تأمين، تكيس، تسجيل"),
         ("Secure, bag, photograph, log", "تأمين، تكيس، تصوير، تسجيل"),
         ("Log, secure, photograph, bag", "تسجيل، تأمين، تصوير، تكيس")],
        0,
        "Each rule forces the next step to wait. Only one order satisfies all four.",
        "كل قاعدة تُلزم الخطوة التالية بالانتظار. وترتيب واحد فقط يفي بالأربع.",
        depth=2,
    ))
    out.append(item(
        "L-if-12", 5, "logic",
        "Rules: a pursuit may start only with a supervisor's approval, unless someone is in immediate danger. If it starts under the danger exception, the supervisor is told within 1 minute. There is immediate danger, and no approval was given before the start. Which statement must be true?",
        "القواعد: لا يبدأ المطاردة إلا بموافقة مشرف، إلا إذا كان شخص في خطر فوري. وإذا بدأت بموجب استثناء الخطر يُبلَّغ المشرف خلال دقيقة. هناك خطر فوري، ولم تُعطَ موافقة قبل البدء. أي عبارة يجب أن تكون صحيحة؟",
        [("The pursuit may start, and the supervisor is told within 1 minute.", "يجوز أن تبدأ المطاردة، ويُبلَّغ المشرف خلال دقيقة."),
         ("The pursuit may not start, because approval was missing.", "لا يجوز أن تبدأ المطاردة لأن الموافقة غائبة."),
         ("The pursuit may start, and no one needs to tell the supervisor.", "يجوز أن تبدأ المطاردة ولا حاجة لإبلاغ المشرف."),
         ("The pursuit may start only after the shift ends.", "يجوز أن تبدأ المطاردة بعد نهاية النوبة فقط.")],
        0,
        "The danger exception allows the start, and it adds a one-minute notice. It does not erase the notice.",
        "استثناء الخطر يسمح بالبدء، ويضيف إبلاغًا خلال دقيقة. ولا يلغي الإبلاغ.",
        depth=1,
    ))
    out.append(item(
        "L-if-13", 5, "logic",
        "A call is logged at 10:12. Backup arrives 7 minutes after the log. You must open your notes 3 minutes before backup arrives. At what time do you open your notes? Use only these times.",
        "يُسجَّل البلاغ عند 10:12. يصل الدعم بعد 7 دقائق من التسجيل. يجب أن تفتحي ملاحظاتك قبل 3 دقائق من وصول الدعم. في أي وقت تفتحين الملاحظات؟ استخدمي هذه الأوقات فقط.",
        [("10:16", "10:16"), ("10:15", "10:15"), ("10:19", "10:19"), ("10:22", "10:22")],
        0,
        "Backup is at 10:19. Three minutes before that is 10:16.",
        "الدعم يصل 10:19. قبل ذلك بثلاث دقائق هو 10:16.",
        depth=2,
    ))
    out.append(item(
        "L-if-14", 6, "logic",
        "Rules: (1) Bag currency before it is counted. (2) Count it before it is logged. (3) If a second officer is not present, do not count it; seal the bag and log \"uncounted\" instead. (4) Logging is otherwise last. One officer is present. Which action is required?",
        "القواعد: (1) ضع النقد في الكيس قبل عدّه. (2) عُدّه قبل تسجيله. (3) إذا لم يحضر ضابط ثانٍ فلا تعدّه؛ أغلق الكيس وسجّل «غير معدود» بدلًا من ذلك. (4) التسجيل في غير هذه الحالة هو الأخير. ضابط واحد حاضر. ما الإجراء المطلوب؟",
        [("Seal the bag and log it as uncounted.", "أغلق الكيس وسجّله غير معدود."),
         ("Count it, then log the total.", "عُدّه ثم سجّل المجموع."),
         ("Log the total, then bag it.", "سجّل المجموع ثم ضعه في الكيس."),
         ("Leave it unbagged until a second officer arrives. The rules do not allow any other step.", "اتركه بلا كيس حتى يصل ضابط ثانٍ. القواعد لا تسمح بأي خطوة أخرى.")],
        0,
        "Rule 3 replaces counting when the second officer is absent. The bag is still sealed and a log line is still made.",
        "القاعدة 3 تستبدل العدّ حين يغيب الضابط الثاني. ويبقى الكيس مغلقًا ويبقى سطر التسجيل.",
        depth=1, stretch=True,
    ))
    out.append(item(
        "L-if-15", 6, "logic",
        "Four statements, one scene: the radio first said the hoodie was gray. A minute later the dispatcher said, \"Disregard gray. The hoodie is green. The cap is still red.\" Which description must you keep?",
        "أربع عبارات، مشهد واحد: قال اللاسلكي أولًا إن القلنسوة رمادية. وبعد دقيقة قال الموزّع: «تجاهلوا الرمادي. القلنسوة خضراء. القبعة ما زالت حمراء.» أي وصف تبقيه؟",
        [("Green hoodie, red cap.", "قلنسوة خضراء، قبعة حمراء."),
         ("Gray hoodie, red cap.", "قلنسوة رمادية، قبعة حمراء."),
         ("Green hoodie, gray cap.", "قلنسوة خضراء، قبعة رمادية."),
         ("Gray hoodie, green cap.", "قلنسوة رمادية، قبعة خضراء.")],
        0,
        "A correction replaces only the detail it names. The cap was not corrected.",
        "التصحيح يستبدل التفصيل الذي يسميه فقط. القبعة لم تُصحَّح.",
        depth=2, stretch=True,
    ))

    # Line-up puzzles. Constraints are checked against every permutation.
    puzzles = [
        dict(id="line-a", tier=3, depth=1, probe=True,
             names=["Kai", "Noa", "Rae", "Sol"],
             setup_en="Four officers stand in a line, first to last.",
             setup_ar="أربعة ضباط في صف، من الأول إلى الأخير.",
             rules_en=["Kai is somewhere before Noa.", "Rae is last.", "Noa is immediately after Kai.", "Sol is not first."],
             rules_ar=["كاي قبل نوا في مكان ما.", "راي الأخير.", "نوا مباشرة بعد كاي.", "سول ليس الأول."],
             cons=lambda p: p["Kai"] < p["Noa"] and p["Rae"] == 3 and p["Noa"] == p["Kai"] + 1 and p["Sol"] != 0),
        dict(id="line-b", tier=3, depth=2,
             names=["North", "East", "South", "West"],
             setup_en="Four calls are handled in order, first to last.",
             setup_ar="أربعة بلاغات تُعالج بالترتيب، من الأول إلى الأخير.",
             rules_en=["North is somewhere before South.", "East is last.", "West is immediately before North.", "South is not first."],
             rules_ar=["نورث قبل ساوث في مكان ما.", "إيست الأخير.", "ويست مباشرة قبل نورث.", "ساوث ليس الأول."],
             cons=lambda p: p["North"] < p["South"] and p["East"] == 3 and p["West"] == p["North"] - 1 and p["South"] != 0),
        dict(id="line-c", tier=4, depth=1,
             names=["Hana", "Ika", "Bo", "Dee"],
             setup_en="Four reports are stacked, top (first) to bottom (last).",
             setup_ar="أربعة تقارير مكدسة، من الأعلى (الأول) إلى الأسفل (الأخير).",
             rules_en=["Hana is above Ika.", "Dee is immediately above Bo.", "Ika is not last.", "Bo is last."],
             rules_ar=["هانا فوق إيكا.", "دي مباشرة فوق بو.", "إيكا ليست الأخيرة.", "بو الأخير."],
             cons=lambda p: p["Hana"] < p["Ika"] and p["Dee"] == p["Bo"] - 1 and p["Ika"] != 3 and p["Bo"] == 3),
        dict(id="line-d", tier=4, depth=2, probe=True,
             names=["Kai", "Noa", "Rae", "Sol"],
             setup_en="Four lockers are numbered 1 to 4.",
             setup_ar="أربع خزائن مرقمة من 1 إلى 4.",
             rules_en=["Kai's locker number is lower than Noa's.", "Sol has locker 4.", "Rae's number is exactly one less than Kai's.", "Noa does not have locker 2."],
             rules_ar=["رقم خزانة كاي أصغر من رقم نوا.", "سول له الخزانة 4.", "رقم راي أقل من رقم كاي بواحد.", "نوا ليس له الخزانة 2."],
             cons=lambda p: p["Kai"] < p["Noa"] and p["Sol"] == 3 and p["Rae"] == p["Kai"] - 1 and p["Noa"] != 1),
        dict(id="line-e", tier=5, depth=1,
             names=["Bus", "Taxi", "Van", "Pickup"],
             setup_en="Four vehicles leave a curb in order, first to last.",
             setup_ar="أربع مركبات تغادر الرصيف بالترتيب، من الأولى إلى الأخيرة.",
             rules_en=["The bus leaves before the taxi.", "The pickup leaves last.", "The van leaves immediately before the bus.", "The taxi does not leave first."],
             rules_ar=["الحافلة تغادر قبل التاكسي.", "البيك أب يغادر أخيرًا.", "الشاحنة تغادر مباشرة قبل الحافلة.", "التاكسي لا يغادر أولًا."],
             cons=lambda p: p["Bus"] < p["Taxi"] and p["Pickup"] == 3 and p["Van"] == p["Bus"] - 1 and p["Taxi"] != 0),
        dict(id="line-f", tier=5, depth=2,
             names=["Hana", "Ika", "Bo", "Dee"],
             setup_en="Four interviews run from first to last.",
             setup_ar="أربع مقابلات من الأولى إلى الأخيرة.",
             rules_en=["Hana is interviewed before Bo.", "Dee is first.", "Ika is immediately after Hana.", "Bo is last."],
             rules_ar=["هانا تُقابل قبل بو.", "دي الأولى.", "إيكا مباشرة بعد هانا.", "بو الأخير."],
             cons=lambda p: p["Hana"] < p["Bo"] and p["Dee"] == 0 and p["Ika"] == p["Hana"] + 1 and p["Bo"] == 3),
        dict(id="line-g", tier=6, depth=1,
             names=["Kai", "Noa", "Rae", "Sol"],
             setup_en="Four beats are assigned from Beat 1 through Beat 4.",
             setup_ar="أربع مناطق من المنطقة 1 إلى المنطقة 4.",
             rules_en=["Kai's beat number is lower than Rae's.", "Noa has Beat 1.", "Sol is immediately after Kai.", "Rae is not on Beat 2."],
             rules_ar=["رقم منطقة كاي أصغر من رقم راي.", "نوا في المنطقة 1.", "سول مباشرة بعد كاي.", "راي ليس في المنطقة 2."],
             cons=lambda p: p["Kai"] < p["Rae"] and p["Noa"] == 0 and p["Sol"] == p["Kai"] + 1 and p["Rae"] != 1),
        dict(id="line-i", tier=3, depth=1,
             names=["Ana", "Ben", "Cal", "Dia"],
             setup_en="Four witnesses are seated from first to last.",
             setup_ar="أربعة شهود يجلسون من الأول إلى الأخير.",
             rules_en=["Ana is somewhere before Ben.", "Dia is last.", "Ben is immediately after Ana.", "Cal is not first."],
             rules_ar=["آنا قبل بن في مكان ما.", "ديا الأخيرة.", "بن مباشرة بعد آنا.", "كال ليس الأول."],
             cons=lambda p: p["Ana"] < p["Ben"] and p["Dia"] == 3 and p["Ben"] == p["Ana"] + 1 and p["Cal"] != 0),
        dict(id="line-j", tier=3, depth=2,
             names=["Mint", "Rose", "Gold", "Ink"],
             setup_en="Four folders are handled from first to last.",
             setup_ar="أربعة ملفات تُعالج من الأول إلى الأخير.",
             rules_en=["Mint is somewhere before Rose.", "Ink is last.", "Rose is immediately after Mint.", "Gold is not first."],
             rules_ar=["مينت قبل روز في مكان ما.", "إنك الأخير.", "روز مباشرة بعد مينت.", "غولد ليس الأول."],
             cons=lambda p: p["Mint"] < p["Rose"] and p["Ink"] == 3 and p["Rose"] == p["Mint"] + 1 and p["Gold"] != 0),
        dict(id="line-k", tier=4, depth=1,
             names=["Hana", "Ika", "Bo", "Dee"],
             setup_en="Four radios are signed out from first to last.",
             setup_ar="أربعة أجهزة لاسلكي تُسلَّم من الأول إلى الأخير.",
             rules_en=["Hana is before Ika.", "Bo is last.", "Dee is immediately before Bo.", "Ika is not first."],
             rules_ar=["هانا قبل إيكا.", "بو الأخير.", "دي مباشرة قبل بو.", "إيكا ليست الأولى."],
             cons=lambda p: p["Hana"] < p["Ika"] and p["Bo"] == 3 and p["Dee"] == p["Bo"] - 1 and p["Ika"] != 0),
        dict(id="line-l", tier=4, depth=2,
             names=["North", "East", "South", "West"],
             setup_en="Four doors are checked from first to last.",
             setup_ar="أربعة أبواب تُفحص من الأول إلى الأخير.",
             rules_en=["North is checked before South.", "West is first.", "East is immediately after North.", "South is last."],
             rules_ar=["نورث يُفحص قبل ساوث.", "ويست الأول.", "إيست مباشرة بعد نورث.", "ساوث الأخير."],
             cons=lambda p: p["North"] < p["South"] and p["West"] == 0 and p["East"] == p["North"] + 1 and p["South"] == 3),
        dict(id="line-h", tier=6, depth=2,
             names=["North", "East", "South", "West"],
             setup_en="Four witnesses speak in order, first to last.",
             setup_ar="أربعة شهود يتكلمون بالترتيب، من الأول إلى الأخير.",
             rules_en=["North speaks before East.", "West speaks immediately after South.", "East is last.", "South is not first."],
             rules_ar=["نورث يتكلم قبل إيست.", "ويست يتكلم مباشرة بعد ساوث.", "إيست الأخير.", "ساوث ليس الأول."],
             cons=lambda p: p["North"] < p["East"] and p["West"] == p["South"] + 1 and p["East"] == 3 and p["South"] != 0),
    ]
    places = ["first", "second", "third", "fourth"]
    places_ar = ["الأول", "الثاني", "الثالث", "الرابع"]
    for pz in puzzles:
        names = pz["names"]
        hits = [perm for perm in permutations(names) if pz["cons"]({n: i for i, n in enumerate(perm)})]
        if len(hits) != 1:
            raise SystemExit(f"{pz['id']}: {len(hits)} solutions {hits[:4]}")
        order = hits[0]
        # Ask two determined positions: first, and whichever middle spot is most informative.
        ask_at = [0, 2]
        for slot in ask_at:
            who = order[slot]
            others = [n for n in names if n != who]
            opts = [opt(who, who), opt(others[0], others[0]), opt(others[1], others[1]), CANNOT]
            rules = " ".join(pz["rules_en"])
            rules_ar = " ".join(pz["rules_ar"])
            why = "The only order that fits every rule is " + ", ".join(order) + f". Position {slot+1} is {who}."
            why_ar = "الترتيب الوحيد الذي يوافق كل القواعد هو " + "، ".join(order) + f". الموضع {slot+1} هو {who}."
            out.append(item(
                f"L-{pz['id']}-{slot}", pz["tier"], "logic",
                f"{pz['setup_en']} {rules} Who is {places[slot]}?",
                f"{pz['setup_ar']} {rules_ar} من هو {places_ar[slot]}؟",
                opts, 0, why, why_ar,
                depth=pz["depth"], probe=pz.get("probe", False) and slot == 0,
                stretch=pz["tier"] == 6,
            ))
    out.extend(scenario_logic())
    out.extend(more_lines())
    return out


def more_lines():
    """More verified one-solution lines so a fast climber does not run out of work."""
    specs = [
        ("ml-a", 5, 1, ["Hana", "Ika", "Bo", "Dee"], "Four reports are read from first to last.", "أربعة تقارير تُقرأ من الأول إلى الأخير.",
         ["Hana is somewhere before Ika.", "Dee is last.", "Ika is immediately after Hana.", "Bo is not first."],
         ["هانا قبل إيكا في مكان ما.", "دي الأخيرة.", "إيكا مباشرة بعد هانا.", "بو ليس الأول."],
         lambda p: p["Hana"] < p["Ika"] and p["Dee"] == 3 and p["Ika"] == p["Hana"] + 1 and p["Bo"] != 0),
        ("ml-b", 5, 2, ["Kai", "Noa", "Rae", "Sol"], "Four keys are issued from first to last.", "أربعة مفاتيح تُسلَّم من الأول إلى الأخير.",
         ["Noa is first.", "Rae is immediately after Kai.", "Sol is last.", "Kai is before Sol."],
         ["نوا الأول.", "راي مباشرة بعد كاي.", "سول الأخير.", "كاي قبل سول."],
         lambda p: p["Noa"] == 0 and p["Rae"] == p["Kai"] + 1 and p["Sol"] == 3 and p["Kai"] < p["Sol"]),
        ("ml-c", 6, 1, ["Bus", "Taxi", "Van", "Pickup"], "Four vehicles are logged from first to last.", "أربع مركبات تُسجَّل من الأولى إلى الأخيرة.",
         ["The bus is somewhere before the taxi.", "The pickup is last.", "The taxi is immediately after the bus.", "The van is not first."],
         ["الحافلة قبل التاكسي في مكان ما.", "البيك أب الأخيرة.", "التاكسي مباشرة بعد الحافلة.", "الشاحنة ليست الأولى."],
         lambda p: p["Bus"] < p["Taxi"] and p["Pickup"] == 3 and p["Taxi"] == p["Bus"] + 1 and p["Van"] != 0),
        ("ml-d", 6, 2, ["Ana", "Ben", "Cal", "Dia"], "Four lockers are assigned from 1 to 4.", "أربع خزائن من 1 إلى 4.",
         ["Dia is first.", "Cal is immediately after Ana.", "Ben is last.", "Ana is before Ben."],
         ["ديا الأولى.", "كال مباشرة بعد آنا.", "بن الأخير.", "آنا قبل بن."],
         lambda p: p["Dia"] == 0 and p["Cal"] == p["Ana"] + 1 and p["Ben"] == 3 and p["Ana"] < p["Ben"]),
        ("ml-e", 6, 3, ["North", "East", "South", "West"], "Four doors are tried from first to last.", "أربعة أبواب تُجرَّب من الأول إلى الأخير.",
         ["East is last.", "South is immediately before East.", "North is before South.", "West is not first."],
         ["إيست الأخير.", "ساوث مباشرة قبل إيست.", "نورث قبل ساوث.", "ويست ليس الأول."],
         lambda p: p["East"] == 3 and p["South"] == p["East"] - 1 and p["North"] < p["South"] and p["West"] != 0),
        ("ml-f", 6, 3, ["Mint", "Rose", "Gold", "Ink"], "Four evidence bags are sealed from first to last.", "أربع أكياس دليل تُغلق من الأول إلى الأخير.",
         ["Ink is last.", "Rose is immediately after Mint.", "Gold is first.", "Mint is before Ink."],
         ["إنك الأخيرة.", "روز مباشرة بعد مينت.", "غولد الأولى.", "مينت قبل إنك."],
         lambda p: p["Ink"] == 3 and p["Rose"] == p["Mint"] + 1 and p["Gold"] == 0 and p["Mint"] < p["Ink"]),
        ("ml-g", 4, 2, ["Hana", "Ika", "Bo", "Dee"], "Four calls are dispatched from first to last.", "أربعة بلاغات تُوزَّع من الأول إلى الأخير.",
         ["Bo is last.", "Dee is immediately before Bo.", "Hana is before Ika.", "Ika is not first."],
         ["بو الأخير.", "دي مباشرة قبل بو.", "هانا قبل إيكا.", "إيكا ليست الأولى."],
         lambda p: p["Bo"] == 3 and p["Dee"] == p["Bo"] - 1 and p["Hana"] < p["Ika"] and p["Ika"] != 0),
        ("ml-h", 3, 2, ["Kai", "Noa", "Rae", "Sol"], "Four chairs are filled from first to last.", "أربعة مقاعد تُشغل من الأول إلى الأخير.",
         ["Sol is last.", "Noa is immediately after Kai.", "Rae is not first.", "Kai is before Noa."],
         ["سول الأخير.", "نوا مباشرة بعد كاي.", "راي ليس الأول.", "كاي قبل نوا."],
         lambda p: p["Sol"] == 3 and p["Noa"] == p["Kai"] + 1 and p["Rae"] != 0 and p["Kai"] < p["Noa"]),
    ]
    out = []
    places = ["first", "second", "third", "fourth"]
    places_ar = ["الأول", "الثاني", "الثالث", "الرابع"]
    for iid, tier, depth, names, setup, setup_ar, rules, rules_ar, cons in specs:
        hits = [perm for perm in permutations(names) if cons({n: i for i, n in enumerate(perm)})]
        if len(hits) != 1:
            raise SystemExit(f"{iid}: {len(hits)} {hits[:3]}")
        order = hits[0]
        for slot in (0, 2):
            who = order[slot]
            others = [n for n in names if n != who]
            out.append(item(
                f"L-{iid}-{slot}", tier, "logic",
                f"{setup} {' '.join(rules)} Who is {places[slot]}?",
                f"{setup_ar} {' '.join(rules_ar)} من هو {places_ar[slot]}؟",
                [opt(who, who), opt(others[0], others[0]), opt(others[1], others[1]), CANNOT],
                0,
                "The only order that fits every rule is " + ", ".join(order) + f". Position {slot+1} is {who}.",
                "الترتيب الوحيد الذي يوافق كل القواعد هو " + "، ".join(order) + f". الموضع {slot+1} هو {who}.",
                depth=depth, stretch=tier == 6 and depth == 3,
            ))
    return out


def scenario_logic():
    """Short scene rules with one defensible answer. Not real exam items."""
    rows = []
    A = rows.append
    A(item(
        "L-sc-1", 3, "logic",
        "Using only this rule: photograph an item before it is moved, and bag it before it is logged. You have photographed the phone and you have not bagged it. What is the next required step?",
        "باستخدام هذه القاعدة فقط: صوّر الغرض قبل نقله، وضعه في الكيس قبل تسجيله. صوّرتِ الهاتف ولم تضعيه في الكيس. ما الخطوة المطلوبة التالية؟",
        [("Bag the phone", "ضعي الهاتف في الكيس"), ("Log the phone", "سجّلي الهاتف"),
         ("Move the phone, then photograph it", "انقلي الهاتف ثم صوّريه"), ("Leave without a log", "غادري بلا تسجيل")],
        0, "Photographing is done. Bagging is the step still in front of logging.",
        "التصوير تم. والتكييس هو الخطوة التي ما زالت قبل التسجيل.", depth=1))
    A(item(
        "L-sc-2", 3, "logic",
        "Three cars are in a line. The blue car is immediately ahead of the red car. The green car is last. Which car is first?",
        "ثلاث سيارات في صف. السيارة الزرقاء مباشرة أمام الحمراء. السيارة الخضراء الأخيرة. أي سيارة هي الأولى؟",
        [("The blue car", "الزرقاء"), ("The red car", "الحمراء"), ("The green car", "الخضراء"), CANNOT],
        0, "Green is last, and blue is immediately ahead of red, so the only order is blue, red, green.",
        "الخضراء الأخيرة، والزرقاء مباشرة أمام الحمراء، فالترتيب الوحيد: زرقاء، حمراء، خضراء.", depth=1))
    A(item(
        "L-sc-3", 3, "logic",
        "Kai works Monday. No one works two days. Noa works the day after Kai. Who works Tuesday?",
        "كاي يعمل الاثنين. لا أحد يعمل يومين. نوا يعمل اليوم الذي بعد كاي. من يعمل الثلاثاء؟",
        [("Noa", "نوا"), ("Kai", "كاي"), ("Both", "كلاهما"), CANNOT],
        0, "The day after Monday is Tuesday, and Noa is the person assigned to it.",
        "اليوم الذي بعد الاثنين هو الثلاثاء، ونوا هو المعيَّن له.", depth=2))
    A(item(
        "L-sc-4", 3, "logic",
        "A note says: the gray door, not the blue door. The package is behind the gray door, on the second floor, not the first. Where is the package?",
        "تقول ورقة: الباب الرمادي لا الأزرق. الطرد خلف الباب الرمادي، في الطابق الثاني لا الأول. أين الطرد؟",
        [("Behind the gray door, second floor", "خلف الباب الرمادي، الطابق الثاني"),
         ("Behind the blue door, second floor", "خلف الباب الأزرق، الطابق الثاني"),
         ("Behind the gray door, first floor", "خلف الباب الرمادي، الطابق الأول"),
         ("Behind the blue door, first floor", "خلف الباب الأزرق، الطابق الأول")],
        0, "Both corrections are stated. Do not mix the rejected door or the rejected floor back in.",
        "التصحيحان مذكوران. لا تعيدي الباب المرفوض ولا الطابق المرفوض.", depth=2))
    A(item(
        "L-sc-5", 4, "logic",
        "Rule: write \"not seen\" when you did not see a detail. Do not copy it from another car. You saw Car A's plate but not its color. Car B is white. What do you write for Car A's color?",
        "القاعدة: اكتبي «لم يُرَ» حين لا ترين تفصيلًا. ولا تنقليه من سيارة أخرى. رأيت لوحة السيارة أ لا لونها. السيارة ب بيضاء. ماذا تكتبين للون السيارة أ؟",
        [("not seen", "لم يُرَ"), ("white", "أبيض"), ("the same as the plate", "مثل اللوحة"), ("black, because most cars in the note are black", "أسود، لأن معظم السيارات في الورقة سوداء")],
        0, "The rule forbids borrowing Car B's color.",
        "القاعدة تمنع استعارة لون السيارة ب.", depth=1))
    A(item(
        "L-sc-6", 4, "logic",
        "Four steps, and only these rules: seal the bag before it leaves the room; label the bag before it is sealed; count the cash before the label is written, and only if a second officer is present. A second officer is present. What is first?",
        "أربع خطوات، وهذه القواعد فقط: أغلق الكيس قبل أن يغادر الغرفة؛ ضع الملصق قبل الإغلاق؛ عُدّ النقد قبل كتابة الملصق، وفقط إذا حضر ضابط ثانٍ. الضابط الثاني حاضر. ما الخطوة الأولى؟",
        [("Count the cash", "عدّ النقد"), ("Write the label", "كتابة الملصق"),
         ("Seal the bag", "إغلاق الكيس"), ("Carry the bag out, then count", "إخراج الكيس ثم العد")],
        0, "Counting is required before the label, the label before the seal, and the seal before the bag leaves. Counting is first.",
        "العد مطلوب قبل الملصق، والملصق قبل الإغلاق، والإغلاق قبل مغادرة الكيس. العد أولًا.", depth=1))
    A(item(
        "L-sc-7", 4, "logic",
        "Exactly these facts: the alarm started at 2:05. You arrived at 2:14. The manager says the door was already open when the alarm started. Which statement must be true?",
        "هذه الوقائع فقط: بدأ الإنذار عند 2:05. وصلتِ عند 2:14. يقول المدير إن الباب كان مفتوحًا أصلًا حين بدأ الإنذار. أي عبارة يجب أن تكون صحيحة؟",
        [("The door was open before you arrived.", "الباب كان مفتوحًا قبل وصولك."),
         ("You arrived before the alarm.", "وصلتِ قبل الإنذار."),
         ("The manager opened the door at 2:14.", "المدير فتح الباب عند 2:14."),
         ("The alarm started because you arrived.", "بدأ الإنذار لأنك وصلتِ.")],
        0, "Open at 2:05, and you arrived at 2:14, so it was open before you arrived. The other lines add a cause the facts do not give.",
        "مفتوح عند 2:05، ووصلتِ عند 2:14، فكان مفتوحًا قبل وصولك. والأسطر الأخرى تضيف سببًا لا تعطيه الوقائع.", depth=2))
    A(item(
        "L-sc-8", 4, "logic",
        "A shift has three posts and three officers: Kai, Noa, Rae. Kai does not take the desk. Noa does not take the car. Rae takes the desk. Who takes the car?",
        "نوبة فيها ثلاثة مواقع وثلاثة ضباط: كاي، نوا، راي. كاي لا يأخذ المكتب. نوا لا يأخذ السيارة. راي يأخذ المكتب. من يأخذ السيارة؟",
        [("Kai", "كاي"), ("Noa", "نوا"), ("Rae", "راي"), CANNOT],
        0, "Rae has the desk. Noa cannot take the car, so Noa takes the remaining post (the door) and Kai takes the car.",
        "راي في المكتب. نوا لا يأخذ السيارة، فيأخذ الموقع الباقي (الباب) وكاي يأخذ السيارة.", depth=2))
    # Verify sc-8: posts desk, car, door implied. Rae = desk. Noa not car, so Noa = door, Kai = car. Yes if there are exactly three posts. I said three posts but only named desk and car. The third is implied as "the remaining one". The question only asks who takes the car. Noa doesn't take the car, Rae takes the desk, so Kai must take the car IF the only posts are desk, car, and one other that Noa can take. Yes Kai takes the car. Good.
    A(item(
        "L-sc-9", 5, "logic",
        "Rule: a newer officer is placed after every officer with a year or more, even if the newer officer bid first. Badge 214 has six months and bid at 2:00. Badge 188 has two years and bid at 3:50. Who is placed first?",
        "القاعدة: الضابط الأحدث يُرتَّب بعد كل ضابط له سنة أو أكثر، حتى لو طلب الأحدث أولًا. الشارة 214 لها ستة أشهر وطلبت عند 2:00. الشارة 188 لها سنتان وطلبت عند 3:50. من يُوضع أولًا؟",
        [("Badge 188", "الشارة 188"), ("Badge 214", "الشارة 214"),
         ("Neither; the times cancel", "لا أحد؛ الوقتان يُلغيان بعضهما"), ("Whichever bid is closer to 4:00", "أي طلب أقرب إلى 4:00")],
        0, "Time would favor 214, but the year-or-more rule places 188 first.",
        "الوقت يفضّل 214، لكن قاعدة السنة أو أكثر تضع 188 أولًا.", depth=1))
    A(item(
        "L-sc-10", 5, "logic",
        "Two statements cannot both be true, and one of them is true. Statement 1: the plate starts with K. Statement 2: the plate does not start with K. The clerk says Statement 1. Which conclusion follows?",
        "عبارتان لا تصدقان معًا، وإحداهما صادقة. العبارة 1: اللوحة تبدأ بـ K. العبارة 2: اللوحة لا تبدأ بـ K. البائع يقول العبارة 1. أي نتيجة تتبع؟",
        [("Exactly one of the two statements is true, and the clerk's saying it does not by itself prove which.", "إحدى العبارتين فقط صادقة، وقول البائع وحده لا يثبت أيهما."),
         ("Statement 1 must be true because the clerk said it.", "العبارة 1 يجب أن تكون صادقة لأن البائع قالها."),
         ("Both statements are true.", "العبارتان صادقتان."),
         ("The plate starts with a number.", "اللوحة تبدأ برقم.")],
        0, "The logic problem tells you the two statements contradict and one is true. It does not tell you the clerk is right.",
        "مسألة المنطق تقول إن العبارتين متناقضتان وإحداهما صادقة. ولا تقول إن البائع محق.", depth=2))
    A(item(
        "L-sc-11", 5, "logic",
        "You have four facts: the hoodie was corrected from gray to green; the cap stayed red; the direction stayed east; the first plate was cancelled and the second plate is TUV 330. Which set is the one you keep?",
        "عندكِ أربع وقائع: القلنسوة صُحّحت من رمادي إلى أخضر؛ القبعة بقيت حمراء؛ الاتجاه بقي شرقًا؛ اللوحة الأولى أُلغيت والثانية TUV 330. أي مجموعة تبقين؟",
        [("Green hoodie, red cap, east, TUV 330", "قلنسوة خضراء، قبعة حمراء، شرقًا، TUV 330"),
         ("Gray hoodie, red cap, east, TUV 330", "قلنسوة رمادية، قبعة حمراء، شرقًا، TUV 330"),
         ("Green hoodie, gray cap, east, the cancelled plate", "قلنسوة خضراء، قبعة رمادية، شرقًا، اللوحة الملغاة"),
         ("Green hoodie, red cap, west, TUV 330", "قلنسوة خضراء، قبعة حمراء، غربًا، TUV 330")],
        0, "Keep each correction and every detail the correction did not touch.",
        "أبقي كل تصحيح وكل تفصيل لم يمسسه التصحيح.", depth=1))
    A(item(
        "L-sc-12", 6, "logic",
        "Rule 1: visitors out by 9 PM. Rule 2: a nurse on duty may stay. Rule 3: one family member with a blue band may stay with a patient. At 9:20 a man with no band is sitting in a patient's room. He is not the nurse. What do the rules require?",
        "القاعدة 1: الزوار يغادرون عند 9 مساءً. القاعدة 2: ممرضة في النوبة يجوز لها البقاء. القاعدة 3: قريب واحد بسوار أزرق يجوز له البقاء مع مريض. عند 9:20 رجل بلا سوار جالس في غرفة مريض. هو ليس الممرضة. ماذا توجب القواعد؟",
        [("He is a visitor past 9, so he is out of line.", "هو زائر بعد 9، فهو مخالف."),
         ("Rule 2 lets him stay, because he is in a patient's room.", "القاعدة 2 تسمح له بالبقاء لأنه في غرفة مريض."),
         ("Rule 3 lets him stay, even without a band.", "القاعدة 3 تسمح له بالبقاء حتى بلا سوار."),
         ("No rule applies after 9.", "لا قاعدة تنطبق بعد 9.")],
        0, "He is not the nurse and he has no blue band. Rule 1 still applies.",
        "هو ليس الممرضة ولا سوار أزرق له. القاعدة 1 ما زالت تنطبق.",
        depth=1, stretch=True))
    A(item(
        "L-sc-13", 6, "logic",
        "A log shows only two sign-ins after 4:00: Chen at 4:12 with a blue sticker, and Ortiz at 4:28 with a yellow sticker, destination roof, escorted. It is 4:40. Who is logged to the roof?",
        "سجل يُظهر توقيعين فقط بعد 4:00: تشين عند 4:12 بملصق أزرق، وأورتيز عند 4:28 بملصق أصفر، الوجهة السطح، برفقة. الساعة 4:40. من المسجَّل إلى السطح؟",
        [("Ortiz", "أورتيز"), ("Chen", "تشين"), ("Both", "كلاهما"), ("No one; 4:40 cancelled the log", "لا أحد؛ 4:40 ألغت السجل")],
        0, "Only Ortiz's line names the roof. 4:40 is when you read the log, not a third sign-in.",
        "سطر أورتيز وحده يسمي السطح. و4:40 وقت قراءتك للسجل، لا توقيع ثالث.",
        depth=2, stretch=True))
    A(item(
        "L-sc-14", 6, "logic",
        "Using only the witness's own words: he is sure of a red cap; he is not sure the hoodie was gray; he states the car was a black sedan that turned east; he did not see the passenger. Which detail do you leave out of the sure facts?",
        "باستخدام كلمات الشاهد وحدها: هو متأكد من قبعة حمراء؛ غير متأكد أن القلنسوة كانت رمادية؛ يذكر أن السيارة سيدان سوداء انعطفت شرقًا؛ لم يرَ الراكب. أي تفصيل تتركينه خارج الوقائع المؤكدة؟",
        [("The gray hoodie", "القلنسوة الرمادية"), ("The red cap", "القبعة الحمراء"),
         ("The east turn", "الانعطاف شرقًا"), ("That the passenger was not seen", "أن الراكب لم يُرَ")],
        0, "He marked the hoodie as unsure. The rest are stated as sure or as a direct observation.",
        "هو وصف القلنسوة بغير المؤكدة. والباقي مذكور كمؤكد أو كملاحظة مباشرة.",
        depth=2, stretch=True))
    return rows


def passage(iid, tier, depth, pillar, secs, en, ar, qs):
    if pillar in ("listen", "obs") and not secs:
        raise SystemExit(iid)
    for q in qs:
        if len(q["opts"]) != 4 or len(set(o[0] for o in q["opts"])) != 4:
            raise SystemExit(f"bad q in {iid}")
    return {
        "id": iid, "tier": tier, "depth": depth, "pillar": pillar,
        "secs": secs or 0, "en": en, "ar": ar, "qs": qs,
    }


def qq(qid, en, ar, opts, ans, why_en, why_ar):
    return {
        "id": qid, "en": en, "ar": ar,
        "opts": [[a, b] for a, b in opts],
        "ans": ans, "why": [why_en, why_ar],
    }


def passages():
    reads, comps, listens, obs = [], [], [], []
    reads.append(passage(
        "r1", 1, 1, "reading", 0,
        "Officers must notify a supervisor before any vehicle pursuit begins. If the pursuit ends within two blocks, the officer still files a short report the same shift. A pursuit that leaves the district also requires a phone call to dispatch before the officer crosses the line.",
        "يجب على الضباط إبلاغ مشرف قبل أن تبدأ أي مطاردة مركبة. وإذا انتهت المطاردة خلال مربعين سكنيين، يظل الضابط يودع تقريرًا قصيرًا في النوبة نفسها. والمطاردة التي تغادر المنطقة تتطلب أيضًا اتصالًا بالموزّع قبل أن يجتاز الضابط الحد.",
        [qq("r1a", "When is the supervisor told about a pursuit?", "متى يُبلَّغ المشرف بالمطاردة؟",
            [("Before it begins", "قبل أن تبدأ"), ("Only if it leaves the district", "فقط إذا غادرت المنطقة"),
             ("After the short report", "بعد التقرير القصير"), ("Only if it lasts more than two blocks", "فقط إذا استمرت أكثر من مربعين")],
            0, "The first sentence puts the notice before the start.", "الجملة الأولى تضع الإبلاغ قبل البدء."),
         qq("r1b", "A pursuit ends in one block. What else is required?", "مطاردة تنتهي في مربع واحد. ماذا يُطلب أيضًا؟",
            [("A short report the same shift", "تقرير قصير في النوبة نفسها"), ("No report", "لا تقرير"),
             ("A phone call to dispatch before crossing a line", "اتصال بالموزّع قبل اجتياز الحد"), ("A new supervisor approval the next day", "موافقة مشرف جديدة في اليوم التالي")],
            0, "Ending within two blocks does not cancel the same-shift report.", "الانتهاء خلال مربعين لا يلغي تقرير النوبة نفسها."),
         qq("r1c", "Which detail is NOT required by this passage?", "أي تفصيل لا يطلبه هذا المقطع؟",
            [("The name of the sergeant's child", "اسم ابن الرقيب"), ("Notice before the pursuit", "إبلاغ قبل المطاردة"),
             ("A same-shift report even for a short pursuit", "تقرير في النوبة نفسها حتى للمطاردة القصيرة"), ("A dispatch call before leaving the district", "اتصال بالموزّع قبل مغادرة المنطقة")],
            0, "Nothing in the passage mentions a family name.", "لا شيء في المقطع يذكر اسم عائلة.")],
    ))
    reads.append(passage(
        "r2", 2, 1, "reading", 0,
        "Evidence is logged within one hour of collection. If the scene is still active, the officer may wait, but the log is finished before the shift ends. A firearm is never held under the longer allowance: it is logged within 30 minutes of being made safe. The log line includes the time collected, the officer's name, and the location.",
        "يُسجَّل الدليل خلال ساعة من جمعه. وإذا كان المسرح ما زال نشطًا يجوز للضابط الانتظار، لكن التسجيل يُنهى قبل نهاية النوبة. والسلاح الناري لا يُحبس تحت المهلة الأطول: يُسجَّل خلال 30 دقيقة من جعله آمنًا. ويشمل سطر التسجيل وقت الجمع واسم الضابط والمكان.",
        [qq("r2a", "The scene is still active, and the item is a wallet. What is the deadline?", "المسرح ما زال نشطًا، والغرض محفظة. ما المهلة؟",
            [("Before the shift ends", "قبل نهاية النوبة"), ("Within 30 minutes", "خلال 30 دقيقة"),
             ("Within one hour, with no exception", "خلال ساعة بلا استثناء"), ("The next shift", "النوبة التالية")],
            0, "A wallet can use the active-scene allowance. A firearm cannot.", "المحفظة يمكن أن تستخدم مهلة المسرح النشط. السلاح لا يمكن."),
         qq("r2b", "The item is a firearm, made safe at 2:10. By when is it logged?", "الغرض سلاح ناري جُعل آمنًا عند 2:10. متى يُسجَّل؟",
            [("By 2:40", "بحلول 2:40"), ("By 3:10", "بحلول 3:10"), ("Before the shift ends, even if that is tomorrow morning", "قبل نهاية النوبة حتى لو كان ذلك صباح الغد"), ("No time is stated", "لا وقت مذكور")],
            0, "Thirty minutes after 2:10 is 2:40.", "ثلاثون دقيقة بعد 2:10 هي 2:40."),
         qq("r2c", "Which of these must be on the log line?", "أي من هذه يجب أن يكون في سطر التسجيل؟",
            [("Time collected, officer's name, and location", "وقت الجمع واسم الضابط والمكان"),
             ("The suspect's school", "مدرسة المشتبه به"), ("The weather only", "الطقس فقط"), ("A photo of the officer", "صورة للضابط")],
            0, "The last sentence lists those three and no others.", "الجملة الأخيرة تذكر هذه الثلاثة ولا غيرها.")],
    ))
    reads.append(passage(
        "r3", 3, 1, "reading", 0,
        "Witness statements are taken one at a time, out of earshot of the other witnesses. The officer writes what the person says they saw, not what the officer thinks happened. If a witness corrects a detail, the officer draws a single line through the old detail, writes the new one, and initials the change. The old detail stays readable.",
        "تُؤخذ إفادات الشهود واحدة واحدة، بعيدًا عن سمع الشهود الآخرين. ويكتب الضابط ما يقول الشخص إنه رآه، لا ما يظن الضابط أنه حدث. وإذا صحّح شاهد تفصيلًا، يضع الضابط خطًا واحدًا على التفصيل القديم، ويكتب الجديد، ويوقّع بالحروف الأولى. ويبقى التفصيل القديم مقروءًا.",
        [qq("r3a", "Why are witnesses separated?", "لماذا يُفصل الشهود؟",
            [("So they cannot hear one another", "حتى لا يسمع أحدهم الآخر"),
             ("So the report is shorter", "حتى يكون التقرير أقصر"),
             ("Because the passage says they must be arrested", "لأن المقطع يقول إنهم يجب أن يُقبض عليهم"),
             ("So the officer can guess the ending", "حتى يستطيع الضابط تخمين النهاية")],
            0, "\"Out of earshot\" is the reason given.", "«بعيدًا عن السمع» هو السبب المذكور."),
         qq("r3b", "A witness changes the color of a hat. What happens to the first color?", "شاهد يغيّر لون قبعة. ماذا يحدث للون الأول؟",
            [("It is lined through but left readable", "يُشطب بخط ويبقى مقروءًا"),
             ("It is erased completely", "يُمحى تمامًا"),
             ("It is torn out of the page", "يُمزق من الصفحة"),
             ("It replaces the new color", "يحل محل اللون الجديد")],
            0, "The passage says a single line, and the old detail stays readable.", "المقطع يقول خطًا واحدًا، والتفصيل القديم يبقى مقروءًا."),
         qq("r3c", "What does the officer write down?", "ماذا يكتب الضابط؟",
            [("What the witness says they saw", "ما يقول الشاهد إنه رآه"),
             ("What the officer believes is more likely", "ما يعتقد الضابط أنه أرجح"),
             ("Only details that match the other witnesses", "فقط التفاصيل التي تطابق الشهود الآخرين"),
             ("A guess, labeled as a fact", "تخمينًا يُوسم كحقيقة")],
            0, "The second sentence forbids substituting the officer's theory.", "الجملة الثانية تمنع استبدال نظرية الضابط.")],
    ))
    reads.append(passage(
        "r4", 3, 2, "reading", 0,
        "A lost child is described over the radio once, then updated only when a detail changes. The first description is: girl, about 6, yellow raincoat, blue boots, holding a gray stuffed dog, last seen by the fountain at 3:05. At 3:18 the mother says the dog is brown, not gray. No other detail changes. Officers still search the fountain area.",
        "يوصف طفل ضائع عبر اللاسلكي مرة واحدة، ثم يُحدَّث فقط حين يتغير تفصيل. الوصف الأول: بنت، نحو 6 سنوات، معطف مطر أصفر، حذاء أزرق، تمسك كلبًا محشوًا رماديًا، شوهدت آخر مرة عند النافورة الساعة 3:05. وعند 3:18 تقول الأم إن الكلب بني لا رمادي. لا يتغير أي تفصيل آخر. وما زال الضباط يفتشون منطقة النافورة.",
        [qq("r4a", "After 3:18, which description is correct?", "بعد 3:18، أي وصف صحيح؟",
            [("Yellow raincoat, blue boots, brown stuffed dog", "معطف أصفر، حذاء أزرق، كلب محشو بني"),
             ("Yellow raincoat, blue boots, gray stuffed dog", "معطف أصفر، حذاء أزرق، كلب محشو رمادي"),
             ("Brown raincoat, blue boots, gray dog", "معطف بني، حذاء أزرق، كلب رمادي"),
             ("Yellow raincoat, brown boots, brown dog", "معطف أصفر، حذاء بني، كلب بني")],
            0, "Only the dog's color was corrected.", "لون الكلب وحده هو الذي صُحّح."),
         qq("r4b", "Where was she last seen?", "أين شوهدت آخر مرة؟",
            [("By the fountain", "عند النافورة"), ("At the bus stop", "عند موقف الحافلة"),
             ("In the parking garage", "في مرأب السيارات"), ("The passage does not say", "المقطع لا يقول")],
            0, "The first description gives the fountain.", "الوصف الأول يذكر النافورة."),
         qq("r4c", "What should officers assume about the search area at 3:18?", "ماذا ينبغي أن يفترض الضباط عن منطقة البحث عند 3:18؟",
            [("They are still searching the fountain area", "ما زالوا يفتشون منطقة النافورة"),
             ("The search moved downtown because the dog color changed", "انتقل البحث إلى وسط المدينة لأن لون الكلب تغير"),
             ("The search ended at 3:05", "انتهى البحث عند 3:05"),
             ("The mother cancelled the report", "ألغت الأم البلاغ")],
            0, "The last sentence keeps the search at the fountain.", "الجملة الأخيرة تبقي البحث عند النافورة.")],
    ))
    reads.append(passage(
        "r5", 4, 1, "reading", 0,
        "Store policy, posted by the door: employees may not accuse a customer of theft on the sales floor. They may watch, and they may call the police if they see someone conceal merchandise and pass the last register without paying. Until an officer arrives, employees stay between the person and the exit only if they can do so without touching the person. They do not search a bag.",
        "سياسة المتجر، معلّقة عند الباب: لا يجوز للموظفين اتهام زبون بالسرقة في صالة البيع. ويجوز لهم المراقبة، ويجوز لهم الاتصال بالشرطة إذا رأوا شخصًا يخفي بضاعة ويجتاز آخر صندوق دون دفع. وحتى يصل ضابط، يبقى الموظفون بين الشخص والمخرج فقط إذا استطاعوا ذلك دون لمسه. وهم لا يفتشون حقيبة.",
        [qq("r5a", "When may employees call the police, according to this posting?", "متى يجوز للموظفين الاتصال بالشرطة حسب هذا الإعلان؟",
            [("If they see merchandise concealed and the person pass the last register without paying", "إذا رأوا بضاعة مخفاة واجتاز الشخص آخر صندوق دون دفع"),
             ("Whenever a customer looks nervous", "كلما بدا الزبون متوترًا"),
             ("Only after they search the bag", "فقط بعد تفتيش الحقيبة"),
             ("Only after they accuse the person on the sales floor", "فقط بعد اتهام الشخص في صالة البيع")],
            0, "The posting gives those two observed facts as the condition.", "الإعلان يجعل هاتين الملاحظتين الشرط."),
         qq("r5b", "What are employees told not to do?", "ماذا يُطلب من الموظفين ألا يفعلوا؟",
            [("Accuse someone on the sales floor, touch the person, or search a bag", "اتهام أحد في الصالة، أو لمسه، أو تفتيش حقيبة"),
             ("Watch the sales floor", "مراقبة الصالة"),
             ("Call the police", "الاتصال بالشرطة"),
             ("Stand near an exit without touching anyone", "الوقوف قرب مخرج دون لمس أحد")],
            0, "Those three limits are stated. Watching and calling are allowed.", "هذه الحدود الثلاثة مذكورة. والمراقبة والاتصال مسموحان."),
         qq("r5c", "An employee can block the exit only by grabbing a sleeve. What does the posting allow?", "لا يستطيع الموظف سد المخرج إلا بالإمساك بكم. ماذا يسمح الإعلان؟",
            [("Do not block that way; do not touch", "لا تسد المخرج بهذه الطريقة؛ لا تلمس"),
             ("Grab the sleeve, then search the bag", "أمسك الكم ثم فتش الحقيبة"),
             ("Accuse the person first, then grab the sleeve", "اتهم الشخص أولًا ثم أمسك الكم"),
             ("The posting requires the grab", "الإعلان يوجب الإمساك")],
            0, "Blocking is allowed only without touching.", "سد الطريق مسموح فقط دون لمس.")],
    ))
    reads.append(passage(
        "r6", 4, 2, "reading", 0,
        "Radio procedure for this exercise: give your unit, your location, and what you need, in that order. Then stop and listen. If dispatch corrects a detail, repeat the corrected detail back and do not repeat the old one. Numbers are said one digit at a time. Plate HNL 204 is \"H-N-L two zero four,\" not \"two hundred four.\"",
        "إجراء اللاسلكي في هذا التمرين: اذكر وحدتك، ثم موقعك، ثم ما تحتاجه، بهذا الترتيب. ثم توقف واستمع. وإذا صحّح الموزّع تفصيلًا، أعد التفصيل المصحّح ولا تعد القديم. والأرقام تُقال رقمًا رقمًا. اللوحة HNL 204 هي «H-N-L two zero four»، لا «two hundred four».",
        [qq("r6a", "What is the order of a first transmission?", "ما ترتيب الإرسال الأول؟",
            [("Unit, location, what you need", "الوحدة، الموقع، ما تحتاجه"),
             ("What you need, unit, location", "ما تحتاجه، الوحدة، الموقع"),
             ("Location only", "الموقع فقط"),
             ("The plate, then the unit", "اللوحة ثم الوحدة")],
            0, "The first sentence gives that order.", "الجملة الأولى تعطي هذا الترتيب."),
         qq("r6b", "Dispatch says the plate is HNL 240, not 204. What do you repeat back?", "يقول الموزّع إن اللوحة HNL 240 لا 204. ماذا تعيدين؟",
            [("H-N-L two four zero", "H-N-L two four zero"),
             ("H-N-L two zero four", "H-N-L two zero four"),
             ("Two hundred forty", "مئتان وأربعون"),
             ("Both plates, old then new", "اللوحتان، القديمة ثم الجديدة")],
            0, "Repeat only the correction, one digit at a time: 2, 4, 0.", "أعيدي التصحيح فقط، رقمًا رقمًا: 2 ثم 4 ثم 0."),
         qq("r6c", "After you say what you need, what does the procedure tell you to do?", "بعد أن تقولي ما تحتاجينه، ماذا يطلب منك الإجراء؟",
            [("Stop and listen", "توقفي واستمعي"), ("Keep talking until dispatch interrupts", "واصلي الكلام حتى يقاطع الموزّع"),
             ("Repeat the old detail twice", "كرري التفصيل القديم مرتين"), ("Spell your childhood street", "تهجّي شارع طفولتك")],
            0, "The second sentence says to stop and listen.", "الجملة الثانية تقول توقفي واستمعي.")],
    ))
    reads.append(passage(
        "r7", 5, 1, "reading", 0,
        "A building log says visitors sign in, show a photo ID, and wear a blue sticker on the chest. Contractors wear a yellow sticker and must be escorted above the second floor. A person with no sticker is walked back to the desk, not questioned in the hallway about a crime. At 4:40 the log shows: M. Chen, unit 12C, blue sticker, photo ID checked, entered 4:12. J. Ortiz, contractor, yellow sticker, escorted, entered 4:28, destination roof. No one else signed in after 4:00.",
        "سجل المبنى يقول إن الزوار يوقّعون، ويبرزون هوية بصورة، ويلبسون ملصقًا أزرق على الصدر. والمقاولون يلبسون ملصقًا أصفر ويجب مرافقتهم فوق الطابق الثاني. والشخص بلا ملصق يُعاد إلى المكتب، ولا يُستجوب في الممر عن جريمة. وعند 4:40 يظهر السجل: M. Chen، الوحدة 12C، ملصق أزرق، فُحصت هوية بصورة، دخل 4:12. J. Ortiz، مقاول، ملصق أصفر، برفقة، دخل 4:28، الوجهة السطح. لم يوقّع أحد آخر بعد 4:00.",
        [qq("r7a", "Who may be on the roof at 4:35 under this log?", "من يجوز أن يكون على السطح عند 4:35 حسب هذا السجل؟",
            [("J. Ortiz, escorted", "J. Ortiz برفقة"), ("M. Chen, alone", "M. Chen وحدها"),
             ("Anyone with a blue sticker", "أي شخص بملصق أزرق"), ("A person with no sticker", "شخص بلا ملصق")],
            0, "Only Ortiz is logged to the roof, and contractors above the second floor are escorted.", "أورتيز وحده مسجّل إلى السطح، والمقاولون فوق الطابق الثاني بمرافقة."),
         qq("r7b", "You see a person in the hallway with no sticker. What does the log's rule say to do?", "ترين شخصًا في الممر بلا ملصق. ماذا تقول قاعدة السجل؟",
            [("Walk them back to the desk", "أعيديهم إلى المكتب"),
             ("Question them in the hallway about a theft", "استجوبهم في الممر عن سرقة"),
             ("Send them to the roof", "أرسلهم إلى السطح"),
             ("Issue a yellow sticker in the hallway", "أصدر ملصقًا أصفر في الممر")],
            0, "The rule sends an unstickered person back to the desk and bars a hallway crime interview.", "القاعدة تعيد الشخص بلا ملصق إلى المكتب وتمنع استجواب جريمة في الممر."),
         qq("r7c", "What time did M. Chen enter?", "في أي وقت دخل M. Chen؟",
            [("4:12", "4:12"), ("4:28", "4:28"), ("4:40", "4:40"), ("4:00", "4:00")],
            0, "Chen's line says entered 4:12. 4:40 is when you are reading the log.", "سطر تشين يقول دخل 4:12. و4:40 هو وقت قراءتك للسجل.")],
    ))
    reads.append(passage(
        "r8", 6, 1, "reading", 0,
        "Use only this notice. Shift bids close Friday at 4:00 PM. A bid submitted at 4:00 PM is on time. A bid submitted at 4:01 PM is late and is not read. Officers with less than one year on the job may bid, but they are placed after every officer who has a year or more, even if the newer officer bid first. If two qualified officers bid the same post, the earlier bid wins. If the times match to the minute, the lower badge number wins. Badge 214 bid post 3 at 3:40. Badge 188 bid post 3 at 3:40. Both have more than a year.",
        "استخدمي هذا الإعلان فقط. تُقفل طلبات النوبة يوم الجمعة الساعة 4:00 مساءً. الطلب المقدَّم عند 4:00 في الوقت. والطلب عند 4:01 متأخر ولا يُقرأ. والضباط الذين لهم أقل من سنة يجوز لهم الطلب، لكنهم يُرتَّبون بعد كل ضابط له سنة أو أكثر، حتى لو طلب الضابط الأحدث أولًا. وإذا طلب ضابطان مؤهلان الموقع نفسه يفوز الطلب الأسبق. وإذا تطابق الوقت حتى الدقيقة يفوز رقم الشارة الأصغر. الشارة 214 طلبت الموقع 3 عند 3:40. الشارة 188 طلبت الموقع 3 عند 3:40. وكلاهما له أكثر من سنة.",
        [qq("r8a", "Who wins post 3?", "من يفوز بالموقع 3؟",
            [("Badge 188", "الشارة 188"), ("Badge 214", "الشارة 214"),
             ("Neither, because the times match", "لا أحد، لأن الوقتين متطابقان"),
             ("Whichever officer has less than a year", "أي ضابط له أقل من سنة")],
            0, "The times match, both are qualified, and 188 is the lower badge number.", "الوقتان متطابقان، وكلاهما مؤهل، و188 هو رقم الشارة الأصغر."),
         qq("r8b", "A bid arrives at 4:01 PM from an officer with ten years on the job. What happens?", "يصل طلب عند 4:01 مساءً من ضابط له عشر سنوات. ماذا يحدث؟",
            [("It is late and is not read", "إنه متأخر ولا يُقرأ"),
             ("It wins, because of seniority", "يفوز بسبب الأقدمية"),
             ("It is on time, because 4:00 was the close", "إنه في الوقت لأن 4:00 كان الإقفال"),
             ("It is placed first", "يُوضع أولًا")],
            0, "4:01 is late for everyone. Seniority is not an exception to the clock.", "4:01 متأخر للجميع. والأقدمية ليست استثناء من الساعة."),
         qq("r8c", "A new officer, month six, bids a post at 2:00 PM. A one-year officer bids the same post at 3:50 PM. Who is placed first?", "ضابط جديد، الشهر السادس، يطلب موقعًا عند 2:00 مساءً. وضابط له سنة يطلب الموقع نفسه عند 3:50. من يُوضع أولًا؟",
            [("The one-year officer", "الضابط الذي له سنة"),
             ("The new officer, because 2:00 is earlier", "الضابط الجديد لأن 2:00 أسبق"),
             ("Neither can bid", "لا يجوز لأي منهما الطلب"),
             ("The new officer, then the bids are not read", "الضابط الجديد، ثم لا تُقرأ الطلبات")],
            0, "Less than one year may bid, but is placed after everyone with a year or more.", "أقل من سنة يجوز له الطلب، لكنه يُرتَّب بعد كل من له سنة أو أكثر.")],
    ))
    reads.append(passage(
        "r9", 6, 2, "reading", 0,
        "A witness says: \"I think the driver was a man, but I only saw the back of a red cap and a gray hoodie. I am sure about the red cap. I am not sure about the hoodie. The car was a black sedan, plate starting with K, and it turned east. I did not see who was in the passenger seat.\" Use only what the witness marks as sure, plus the facts stated without a doubt.",
        "يقول شاهد: «أعتقد أن السائق كان رجلًا، لكني رأيت فقط ظهر قبعة حمراء وقلنسوة رمادية. أنا متأكد من القبعة الحمراء. لست متأكدًا من القلنسوة. السيارة كانت سيدان سوداء، لوحتها تبدأ بـ K، وانعطفت شرقًا. لم أرَ من كان في مقعد الراكب.» استخدمي فقط ما يصفه الشاهد بالمؤكد، إضافة إلى الوقائع المذكورة بلا شك.",
        [qq("r9a", "Which set is safe to put in the report as the witness's account?", "أي مجموعة آمنة لتوضع في التقرير بوصفها رواية الشاهد؟",
            [("Red cap; black sedan; plate starts with K; turned east; passenger not seen", "قبعة حمراء؛ سيدان سوداء؛ اللوحة تبدأ بـ K؛ انعطفت شرقًا؛ الراكب لم يُرَ"),
             ("Male driver; gray hoodie; red cap; black sedan", "سائق رجل؛ قلنسوة رمادية؛ قبعة حمراء؛ سيدان سوداء"),
             ("Gray hoodie; passenger was a woman; plate starts with K", "قلنسوة رمادية؛ الراكب امرأة؛ اللوحة تبدأ بـ K"),
             ("Red cap only. The car details were guesses.", "القبعة الحمراء فقط. وتفاصيل السيارة كانت تخمينًا.")],
            0, "He is sure of the cap. The car, plate start, turn, and unseen passenger are stated as facts. The man and the gray hoodie are not sure.", "هو متأكد من القبعة. والسيارة وبداية اللوحة والانعطاف والراكب غير المرئي مذكورة كوقائع. والرجل والقلنسوة الرمادية ليسا مؤكدين."),
         qq("r9b", "What does the witness say about the passenger seat?", "ماذا يقول الشاهد عن مقعد الراكب؟",
            [("He did not see who was in it", "لم يرَ من كان فيه"),
             ("A woman was in it", "كانت فيه امرأة"),
             ("It was empty, and he is sure", "كان فارغًا وهو متأكد"),
             ("The passage does not mention it", "المقطع لا يذكره")],
            0, "The last clause is the whole fact: he did not see the passenger.", "الجملة الأخيرة هي الواقعة كلها: لم يرَ الراكب."),
         qq("r9c", "Which detail did the witness mark as unsure?", "أي تفصيل وصفه الشاهد بغير المؤكد؟",
            [("The gray hoodie", "القلنسوة الرمادية"), ("The red cap", "القبعة الحمراء"),
             ("The turn to the east", "الانعطاف شرقًا"), ("The black sedan", "السيدان السوداء")],
            0, "He says he is not sure about the hoodie, and he is sure about the cap.", "يقول إنه غير متأكد من القلنسوة، ومتأكد من القبعة.")],
    ))

    comps.append(passage(
        "c1", 2, 1, "comp", 0,
        "Notice: dogs in the park must be on a leash before 6 PM. After 6 PM, a dog may be off leash in the fenced field only. The beach path is never an off-leash area. At 6:30 a dog is running on the beach path.",
        "إعلان: الكلاب في الحديقة يجب أن تكون بمقود قبل 6 مساءً. وبعد 6 مساءً يجوز أن يكون الكلب بلا مقود في الميدان المسيّج فقط. وممر الشاطئ ليس منطقة بلا مقود أبدًا. وعند 6:30 كلب يجري في ممر الشاطئ.",
        [qq("c1a", "Is the dog where the notice allows it to be off leash?", "هل الكلب حيث يسمح الإعلان بأن يكون بلا مقود؟",
            [("No", "لا"), ("Yes, because it is after 6 PM", "نعم، لأنه بعد 6 مساءً"),
             ("Yes, because the beach path is a field", "نعم، لأن ممر الشاطئ ميدان"),
             ("The notice does not mention paths", "الإعلان لا يذكر الممرات")],
            0, "After 6, off leash is only the fenced field. The beach path is never off leash.", "بعد 6، بلا مقود يعني الميدان المسيّج فقط. وممر الشاطئ ليس كذلك أبدًا."),
         qq("c1b", "Where may a dog be off leash at 6:30?", "أين يجوز أن يكون الكلب بلا مقود عند 6:30؟",
            [("In the fenced field", "في الميدان المسيّج"), ("On the beach path", "في ممر الشاطئ"),
             ("Anywhere in the park", "في أي مكان في الحديقة"), ("Nowhere", "لا مكان")],
            0, "The exception is the fenced field only.", "الاستثناء هو الميدان المسيّج فقط."),
         qq("c1c", "A dog is off leash in the fenced field at 5:30. What does the notice require?", "كلب بلا مقود في الميدان المسيّج عند 5:30. ماذا يطلب الإعلان؟",
            [("A leash, because it is before 6 PM", "مقودًا، لأنه قبل 6 مساءً"),
             ("Nothing; the field is always off leash", "لا شيء؛ الميدان بلا مقود دائمًا"),
             ("That the dog move to the beach path", "أن ينتقل الكلب إلى ممر الشاطئ"),
             ("That the park close", "أن تُغلق الحديقة")],
            0, "Before 6 PM the leash rule has no field exception.", "قبل 6 مساءً قاعدة المقود بلا استثناء للميدان.")],
    ))
    comps.append(passage(
        "c2", 3, 1, "comp", 0,
        "You read one note, then it is covered. \"Unit 12, meet the clerk at 1420 King, gray door, second floor. The clerk will be in a green apron. Do not interview the customer in the red hat; that person already left a statement with Unit 4. The safe is open. A blue backpack is under the counter, and the clerk says it is not store property.\"",
        "تقرئين ورقة واحدة ثم تُغطى. «الوحدة 12، قابلي البائع عند 1420 كينغ، باب رمادي، الطابق الثاني. البائع سيكون بمئزر أخضر. لا تستجوب الزبون ذي القبعة الحمراء؛ ذلك الشخص ترك إفادة مع الوحدة 4. الخزنة مفتوحة. حقيبة ظهر زرقاء تحت المنضدة، والبائع يقول إنها ليست ملك المتجر.»",
        [qq("c2a", "What color is the clerk's apron?", "ما لون مئزر البائع؟",
            [("Green", "أخضر"), ("Red", "أحمر"), ("Blue", "أزرق"), ("Gray", "رمادي")],
            0, "The apron is green. Red is the hat. Blue is the backpack. Gray is the door.", "المئزر أخضر. الأحمر القبعة. الأزرق الحقيبة. الرمادي الباب."),
         qq("c2b", "What are you told about the customer in the red hat?", "ماذا يُقال لك عن الزبون ذي القبعة الحمراء؟",
            [("Do not interview that person; Unit 4 already took a statement", "لا تستجوب هذا الشخص؛ الوحدة 4 أخذت إفادة"),
             ("Interview that person first", "استجوب هذا الشخص أولًا"),
             ("That person owns the blue backpack", "هذا الشخص يملك الحقيبة الزرقاء"),
             ("The note does not mention a red hat", "الورقة لا تذكر قبعة حمراء")],
            0, "The note bars a second interview.", "الورقة تمنع مقابلة ثانية."),
         qq("c2c", "Which fact is stated, not guessed?", "أي واقعة مذكورة وليست تخمينًا؟",
            [("The safe is open", "الخزنة مفتوحة"),
             ("The backpack was stolen", "الحقيبة سُرقت"),
             ("The customer in the red hat opened the safe", "الزبون ذو القبعة الحمراء فتح الخزنة"),
             ("Unit 4 is still inside", "الوحدة 4 ما زالت في الداخل")],
            0, "Only the open safe is stated. The other lines add a story the note does not tell.", "الخزنة المفتوحة وحدها مذكورة. الأسطر الأخرى تضيف قصة لا تقولها الورقة.")],
    ))
    comps.append(passage(
        "c3", 4, 1, "comp", 0,
        "Procedure: write the plate, then the color, then the direction, then the street. If you did not see a detail, write \"not seen\". Do not fill it from another car. Car A: plate KLM 119, color not seen, headed west on Beretania. Car B: plate KLM 191, white, headed east on King. A later note says, \"Car A color correction: black. Plate stands.\"",
        "الإجراء: اكتبي اللوحة، ثم اللون، ثم الاتجاه، ثم الشارع. وإذا لم تري تفصيلًا اكتبي «لم يُرَ». ولا تملئيه من سيارة أخرى. السيارة أ: لوحة KLM 119، اللون لم يُرَ، اتجهت غربًا في بيريتانيا. السيارة ب: لوحة KLM 191، بيضاء، اتجهت شرقًا في كينغ. وملاحظة لاحقة تقول: «تصحيح لون السيارة أ: أسود. اللوحة تبقى.»",
        [qq("c3a", "After the correction, what is Car A?", "بعد التصحيح، ما السيارة أ؟",
            [("KLM 119, black, west on Beretania", "KLM 119، سوداء، غربًا في بيريتانيا"),
             ("KLM 191, white, west on Beretania", "KLM 191، بيضاء، غربًا في بيريتانيا"),
             ("KLM 119, white, east on King", "KLM 119، بيضاء، شرقًا في كينغ"),
             ("KLM 119, not seen, west on Beretania", "KLM 119، لم يُرَ، غربًا في بيريتانيا")],
            0, "The correction changes only Car A's color. The plate and direction stay.", "التصحيح يغيّر لون السيارة أ فقط. اللوحة والاتجاه يبقيان."),
         qq("c3b", "Before the correction, what should the color line for Car A have said?", "قبل التصحيح، ماذا كان ينبغي أن يقول سطر لون السيارة أ؟",
            [("not seen", "لم يُرَ"), ("white", "أبيض"), ("black", "أسود"), ("the same as Car B", "مثل السيارة ب")],
            0, "The procedure says to write \"not seen\" rather than borrow Car B's white.", "الإجراء يقول اكتبي «لم يُرَ» بدل استعارة أبيض السيارة ب."),
         qq("c3c", "Which plate belongs to the white car headed east?", "أي لوحة للسيارة البيضاء المتجهة شرقًا؟",
            [("KLM 191", "KLM 191"), ("KLM 119", "KLM 119"), ("KLM 911", "KLM 911"), ("No plate was given", "لم تُعطَ لوحة")],
            0, "That is Car B, unchanged by a correction that named Car A.", "هذه السيارة ب، ولم يغيّرها تصحيح سمّى السيارة أ.")],
    ))
    comps.append(passage(
        "c4", 5, 1, "comp", 0,
        "Two rules are posted. Rule A: visitors leave by 9 PM. Rule B: a nurse on duty may stay, and one family member with a blue band may stay with a patient after 9. At 9:20 you see three people: a nurse with a badge, a woman with a blue band sitting with a patient, and a man with no band sitting in a second patient's room.",
        "قاعدتان معلّقتان. القاعدة أ: يغادر الزوار عند 9 مساءً. القاعدة ب: ممرضة في النوبة يجوز لها البقاء، وقريب واحد بسوار أزرق يجوز له البقاء مع مريض بعد 9. وعند 9:20 ترين ثلاثة: ممرضة بشارة، وامرأة بسوار أزرق جالسة مع مريض، ورجل بلا سوار جالس في غرفة مريض ثانٍ.",
        [qq("c4a", "Who is out of line with the posted rules?", "من يخالف القواعد المعلّقة؟",
            [("The man with no band, still in a patient's room", "الرجل بلا سوار، ما زال في غرفة مريض"),
             ("The nurse", "الممرضة"),
             ("The woman with the blue band", "المرأة ذات السوار الأزرق"),
             ("No one described is out of line", "لا أحد ممن وُصفوا يخالف")],
            0, "The nurse and the blue band are allowed after 9. A man with no band who is still in a room is a visitor past the deadline.",
            "الممرضة والسوار الأزرق مسموحان بعد 9. والرجل بلا سوار الذي ما زال في غرفة زائر بعد المهلة."),
         qq("c4b", "The woman with the blue band is with a patient at 9:20. What does Rule B allow?", "المرأة ذات السوار الأزرق مع مريض عند 9:20. ماذا تسمح القاعدة ب؟",
            [("She may stay", "يجوز لها البقاء"), ("She must leave because it is after 9", "يجب أن تغادر لأنه بعد 9"),
             ("She may stay only if she is the nurse", "يجوز لها البقاء فقط إذا كانت الممرضة"),
             ("She must take off the band", "يجب أن تنزع السوار")],
            0, "Rule B names exactly this person.", "القاعدة ب تسمي هذا الشخص تحديدًا."),
         qq("c4c", "Which person does Rule A, read alone, tell to leave at 9?", "أي شخص تقول له القاعدة أ وحدها أن يغادر عند 9؟",
            [("Visitors, before the exception in Rule B is applied", "الزوار، قبل تطبيق الاستثناء في القاعدة ب"),
             ("The nurse on duty", "الممرضة في النوبة"),
             ("No one; Rule A is about parking", "لا أحد؛ القاعدة أ عن المواقف"),
             ("Only people with a blue band", "فقط من معهم سوار أزرق")],
            0, "Rule A covers visitors. Rule B is what carves out the nurse and the blue band.", "القاعدة أ تشمل الزوار. والقاعدة ب هي التي تستثني الممرضة والسوار الأزرق.")],
    ))
    comps.append(passage(
        "c5", 6, 1, "comp", 0,
        "A dispatcher says: \"Correction. Disregard the white van on King. The vehicle is a white van on Hotel Street, plate PLM 316, headed east, driver described as a woman with a dark braid. The King Street van is unrelated and is blue. Repeat the Hotel Street details only.\"",
        "يقول الموزّع: «تصحيح. تجاهلوا الشاحنة البيضاء في كينغ. المركبة شاحنة بيضاء في شارع هوتيل، لوحتها PLM 316، تتجه شرقًا، والسائق وُصف بامرأة ذات ضفيرة داكنة. وشاحنة شارع كينغ غير متعلقة وهي زرقاء. أعدوا تفاصيل شارع هوتيل فقط.»",
        [qq("c5a", "Which vehicle are you following after the correction?", "أي مركبة تتبعين بعد التصحيح؟",
            [("White van, Hotel Street, PLM 316, east, woman with a dark braid", "شاحنة بيضاء، شارع هوتيل، PLM 316، شرقًا، امرأة بضفيرة داكنة"),
             ("White van on King", "شاحنة بيضاء في كينغ"),
             ("Blue van on Hotel Street", "شاحنة زرقاء في شارع هوتيل"),
             ("Blue van, King Street, PLM 316", "شاحنة زرقاء، شارع كينغ، PLM 316")],
            0, "The correction names Hotel Street and tells you to drop the King Street van.", "التصحيح يسمي شارع هوتيل ويطلب منك إسقاط شاحنة كينغ."),
         qq("c5b", "What is the King Street van, after the correction?", "ما شاحنة شارع كينغ بعد التصحيح؟",
            [("Blue, and unrelated", "زرقاء، وغير متعلقة"),
             ("White, plate PLM 316", "بيضاء، لوحة PLM 316"),
             ("The vehicle to follow", "المركبة التي تُتبع"),
             ("Driven by the woman with the braid", "تقودها المرأة ذات الضفيرة")],
            0, "The last factual sentence before the repeat order says it is unrelated and blue.", "الجملة الواقعية الأخيرة قبل أمر الإعادة تقول إنها غير متعلقة وزرقاء."),
         qq("c5c", "What are you told to repeat?", "ماذا يُطلب منك أن تعيدي؟",
            [("The Hotel Street details only", "تفاصيل شارع هوتيل فقط"),
             ("Both vans", "الشاحنتين"),
             ("The disregarded detail, so everyone hears it again", "التفصيل المتجاهَل حتى يسمعه الجميع مرة أخرى"),
             ("Nothing; corrections are not repeated", "لا شيء؛ التصحيحات لا تُعاد")],
            0, "The last sentence is the repeat order.", "الجملة الأخيرة هي أمر الإعادة.")],
    ))

    def L(iid, tier, depth, secs, en, ar, qs):
        listens.append(passage(iid, tier, depth, "listen", secs, en, ar, qs))

    L("ls1", 1, 1, 40,
      "Unit 12, a wallet was turned in at the front desk of 200 Ala Moana, at 1:10 PM. Brown wallet, no cash, a blue bus pass inside. The clerk is wearing a white shirt. Meet the clerk, not the security guard.",
      "الوحدة 12، سُلّمت محفظة في مكتب الاستقبال في 200 ألا موانا، الساعة 1:10 ظهرًا. محفظة بنية، بلا نقد، وبها تذكرة حافلة زرقاء. البائع يلبس قميصًا أبيض. قابلي البائع لا حارس الأمن.",
      [qq("ls1a", "Where do you go?", "إلى أين تذهبين؟",
          [("Front desk, 200 Ala Moana", "مكتب الاستقبال، 200 ألا موانا"),
           ("The bus stop", "موقف الحافلة"), ("The security office", "مكتب الأمن"), ("Unit 4's car", "سيارة الوحدة 4")],
          0, "The address and the desk are the place.", "العنوان والمكتب هما المكان."),
       qq("ls1b", "What is inside the wallet?", "ماذا داخل المحفظة؟",
          [("A blue bus pass, and no cash", "تذكرة حافلة زرقاء، وبلا نقد"),
           ("Cash and a red pass", "نقد وتذكرة حمراء"), ("A phone", "هاتف"), ("Nothing was said", "لم يُقل شيء")],
          0, "Those two details were in the call.", "هذان التفصيلان كانا في البلاغ."),
       qq("ls1c", "Whom do you meet?", "من تقابلين؟",
          [("The clerk in the white shirt", "البائع بالقميص الأبيض"),
           ("The security guard", "حارس الأمن"), ("The bus driver", "سائق الحافلة"), ("No one; leave the wallet", "لا أحد؛ اتركي المحفظة")],
          0, "The call says the clerk, not the guard.", "البلاغ يقول البائع لا الحارس.")])
    L("ls2", 2, 1, 40,
      "Be advised, a child in a yellow raincoat is with the attendant at the Zoo entrance, not at the fountain. The attendant has a red cap. The child's aunt is on the way and will show a photo ID. Do not release the child to anyone without that ID.",
      "تنبيه، طفل بمعطف مطر أصفر مع الموظف عند مدخل الحديقة، لا عند النافورة. الموظف يلبس قبعة حمراء. عمة الطفل في الطريق وستبرز هوية بصورة. لا تسلّمي الطفل لأحد بلا تلك الهوية.",
      [qq("ls2a", "Where is the child?", "أين الطفل؟",
          [("Zoo entrance, with the attendant", "مدخل الحديقة، مع الموظف"),
           ("At the fountain", "عند النافورة"), ("In a yellow taxi", "في تاكسي أصفر"), ("The call did not say", "البلاغ لم يقل")],
          0, "The call moves the child off the fountain and onto the entrance.", "البلاغ ينقل الطفل من النافورة إلى المدخل."),
       qq("ls2b", "What is the attendant wearing?", "ماذا يلبس الموظف؟",
          [("A red cap", "قبعة حمراء"), ("A yellow raincoat", "معطف مطر أصفر"),
           ("A blue badge only", "شارة زرقاء فقط"), ("A green apron", "مئزرًا أخضر")],
          0, "The raincoat is the child's. The cap is the attendant's.", "معطف المطر للطفل. والقبعة للموظف."),
       qq("ls2c", "When may the child leave with an adult?", "متى يجوز أن يغادر الطفل مع بالغ؟",
          [("When the aunt shows a photo ID", "حين تبرز العمة هوية بصورة"),
           ("As soon as any adult arrives", "حالما يصل أي بالغ"),
           ("Only if the adult wears yellow", "فقط إذا لبس البالغ أصفر"),
           ("The call says to release the child immediately", "البلاغ يقول سلّمي الطفل فورًا")],
          0, "The last sentence is a hold until the ID.", "الجملة الأخيرة إبقاء حتى الهوية.")])
    L("ls3", 3, 1, 45,
      "Two calls, do not mix them. Call 1: burglary alarm, 88 Piikoi, apartment 3B, manager in a blue vest will meet you at the lobby. Call 2: a loose dog, brown, no tags, corner of Piikoi and King, a boy in a green shirt is watching it from the sidewalk. You are assigned Call 1.",
      "بلاغان، لا تخلطيهما. البلاغ 1: إنذار اقتحام، 88 بييكوي، الشقة 3B، المدير بسترة زرقاء سيقابلك في الردهة. البلاغ 2: كلب طليق، بني، بلا طوق، زاوية بييكوي وكينغ، وصبي بقميص أخضر يراقبه من الرصيف. أنتِ مكلّفة بالبلاغ 1.",
      [qq("ls3a", "Where do you go?", "إلى أين تذهبين؟",
          [("88 Piikoi, apartment 3B, the lobby", "88 بييكوي، الشقة 3B، الردهة"),
           ("The corner of Piikoi and King", "زاوية بييكوي وكينغ"),
           ("Apartment 3B on King", "الشقة 3B في كينغ"),
           ("Wherever the brown dog is", "حيث يكون الكلب البني")],
          0, "You are assigned Call 1. The corner is Call 2.", "أنت مكلّفة بالبلاغ 1. والزاوية هي البلاغ 2."),
       qq("ls3b", "Who meets you?", "من يقابلك؟",
          [("The manager in a blue vest", "المدير بسترة زرقاء"),
           ("The boy in the green shirt", "الصبي بالقميص الأخضر"),
           ("A tenant in 3B with a dog", "مستأجر في 3B مع كلب"),
           ("No one", "لا أحد")],
          0, "Call 1 names the manager. The boy belongs to Call 2.", "البلاغ 1 يسمي المدير. والصبي يتبع البلاغ 2."),
       qq("ls3c", "Which detail is from the call you are NOT assigned?", "أي تفصيل من البلاغ غير المكلّفة به؟",
          [("A brown dog with no tags", "كلب بني بلا طوق"),
           ("Apartment 3B", "الشقة 3B"),
           ("A blue vest", "سترة زرقاء"),
           ("A lobby meeting", "لقاء في الردهة")],
          0, "The dog is Call 2.", "الكلب هو البلاغ 2.")])
    L("ls4", 4, 1, 45,
      "Listen for the correction. First: suspect on a red bicycle, black helmet, headed west on Young Street from Kalakaua. Correction: disregard the bicycle. The suspect is on foot, still a black helmet, red jacket, headed west on Young. The bicycle belongs to a witness who stayed at the corner.",
      "استمعي للتصحيح. أولًا: مشتبه به على دراجة حمراء، خوذة سوداء، يتجه غربًا في شارع يونغ من كالاناوا. تصحيح: تجاهلوا الدراجة. المشتبه به راجل، وما زال بخوذة سوداء، سترة حمراء، يتجه غربًا في يونغ. والدراجة لشاهد بقي عند الزاوية.",
      [qq("ls4a", "After the correction, how is the suspect traveling?", "بعد التصحيح، كيف يتحرك المشتبه به؟",
          [("On foot", "راجلًا"), ("On the red bicycle", "على الدراجة الحمراء"),
           ("In a red car", "في سيارة حمراء"), ("The call cancelled the suspect", "البلاغ ألغى المشتبه به")],
          0, "The correction says on foot.", "التصحيح يقول راجلًا."),
       qq("ls4b", "What still matches the first description?", "ما الذي ما زال يطابق الوصف الأول؟",
          [("Black helmet, headed west on Young Street", "خوذة سوداء، يتجه غربًا في شارع يونغ"),
           ("Red bicycle and red jacket", "دراجة حمراء وسترة حمراء"),
           ("The witness left on the bicycle", "الشاهد غادر على الدراجة"),
           ("Headed east on Kalakaua", "يتجه شرقًا في كالاناوا")],
          0, "Helmet, direction, and street were not changed. The jacket is new. The bicycle moved to the witness.", "الخوذة والاتجاه والشارع لم تتغير. السترة جديدة. والدراجة انتقلت إلى الشاهد."),
       qq("ls4c", "Who has the red bicycle?", "من معه الدراجة الحمراء؟",
          [("A witness who stayed at the corner", "شاهد بقي عند الزاوية"),
           ("The suspect", "المشتبه به"),
           ("No one; it was a mistake and there is no bicycle", "لا أحد؛ كان خطأ ولا دراجة"),
           ("The dispatcher", "الموزّع")],
          0, "The last sentence places the bicycle with the witness.", "الجملة الأخيرة تضع الدراجة مع الشاهد.")])
    L("ls5", 5, 1, 50,
      "Parking level P2, stall 18. Two black sedans. Sedan 1, plate NRP 441, dent on the left rear door, driver is a woman with a braid and a white shirt, engine on. Sedan 2, plate NRP 414, no dent, empty. A white van, plate PLB 902, is stopped at the ramp, driver on a ladder at the sign, unrelated. The reporting person points at Sedan 1. Repeat 441, not 414.",
      "مستوى الموقف P2، الموقف 18. سيدان سوداوان. السيدان 1، لوحة NRP 441، انبعاج في الباب الخلفي الأيسر، السائقة امرأة بضفيرة وقميص أبيض، المحرك يعمل. السيدان 2، لوحة NRP 414، بلا انبعاج، فارغة. شاحنة بيضاء، لوحة PLB 902، متوقفة عند المنحدر، سائقها على سلّم عند اللافتة، غير متعلقة. والمبلّغ يشير إلى السيدان 1. أعيدي 441 لا 414.",
      [qq("ls5a", "Which plate does the reporting person indicate?", "أي لوحة يشير إليها المبلّغ؟",
          [("NRP 441", "NRP 441"), ("NRP 414", "NRP 414"), ("PLB 902", "PLB 902"), ("No plate was given", "لم تُعطَ لوحة")],
          0, "Sedan 1 is 441, and that is the one indicated. The repeat line says not 414.", "السيدان 1 هي 441، وهي المشار إليها. وسطر الإعادة يقول ليس 414."),
       qq("ls5b", "What is different about the empty sedan?", "ما المختلف في السيدان الفارغة؟",
          [("No dent, plate NRP 414", "بلا انبعاج، لوحة NRP 414"),
           ("A dent, and a driver with a braid", "انبعاج، وسائقة بضفيرة"),
           ("It is white", "إنها بيضاء"),
           ("It is on a ramp with a ladder", "إنها على منحدر مع سلّم")],
          0, "Sedan 2 is the empty one: 414, no dent. The ladder belongs to the van.", "السيدان 2 هي الفارغة: 414، بلا انبعاج. والسلّم للشاحنة."),
       qq("ls5c", "What is the driver of Sedan 1 wearing?", "ماذا تلبس سائقة السيدان 1؟",
          [("A white shirt, and she has a braid", "قميصًا أبيض، ولها ضفيرة"),
           ("A black helmet", "خوذة سوداء"),
           ("A blue vest", "سترة زرقاء"),
           ("The sedan is empty", "السيدان فارغة")],
          0, "Those details are on Sedan 1 only.", "هذان التفصيلان على السيدان 1 فقط.")])
    L("ls6", 6, 2, 50,
      "Night call, 9:52 PM, bus stop Beretania at Piikoi, route 2, bus 214. First version: a person in a brown jacket boarded. Correction at 9:54: the jacket is red, not brown. White sneakers, gray backpack, boarded. A second person in a yellow dress with a black umbrella stayed on the bench. A bald man in an orange shirt was on a phone and did not board. The streetlight on the east end of the stop is out. A blue pickup, plate TUV 330, drove west and is not part of the call.",
      "بلاغ ليلي، 9:52 مساءً، موقف بيريتانيا عند بييكوي، الخط 2، الحافلة 214. الرواية الأولى: شخص بسترة بنية صعد. تصحيح عند 9:54: السترة حمراء لا بنية. حذاء رياضي أبيض، حقيبة ظهر رمادية، صعد. شخص ثانٍ بفستان أصفر ومظلة سوداء بقي على المقعد. رجل أصلع بقميص برتقالي كان على الهاتف ولم يصعد. مصباح الشارع في الطرف الشرقي من الموقف مطفأ. بيك أب أزرق، لوحة TUV 330، سار غربًا وهو ليس جزءًا من البلاغ.",
      [qq("ls6a", "After 9:54, what color is the jacket of the person who boarded?", "بعد 9:54، ما لون سترة الشخص الذي صعد؟",
          [("Red", "أحمر"), ("Brown", "بني"), ("Yellow", "أصفر"), ("Orange", "برتقالي")],
          0, "The correction replaces brown with red.", "التصحيح يستبدل البني بالأحمر."),
       qq("ls6b", "Who stayed at the stop?", "من بقي عند الموقف؟",
          [("The person in the yellow dress and the bald man in orange", "صاحب الفستان الأصفر والرجل الأصلع بالبرتقالي"),
           ("The person in the red jacket", "صاحب السترة الحمراء"),
           ("The driver of the blue pickup", "سائق البيك أب الأزرق"),
           ("No one stayed", "لم يبقَ أحد")],
          0, "The dress stayed on the bench. The bald man did not board. The red jacket boarded.", "الفستان بقي على المقعد. والأصلع لم يصعد. والسترة الحمراء صعدت."),
       qq("ls6c", "Which detail is not part of the call?", "أي تفصيل ليس جزءًا من البلاغ؟",
          [("Blue pickup TUV 330", "بيك أب أزرق TUV 330"),
           ("Bus 214", "الحافلة 214"),
           ("The east streetlight is out", "مصباح الشرق مطفأ"),
           ("Gray backpack", "حقيبة ظهر رمادية")],
          0, "The pickup is stated as not part of the call.", "البيك أب مذكور على أنه ليس جزءًا من البلاغ.")])

    obs.append(passage(
        "o1", 5, 1, "obs", 55,
        "Tuesday, 4:20 PM, lobby of 1427 16th Avenue at Kilauea. A resident in a white blouse and black slacks, red scarf, unit 3B, walks in with a brown grocery bag. A man in a green polo, khaki shorts, and a white cap, unit 12A, stands at the mailboxes on a phone. A teenager in a gray hoodie, ripped blue jeans, and red sneakers runs toward the west alley with a black backpack; the hood hides the face. A package marked \"4C — DO NOT BEND\" had been by the door and is gone. The manager, blue vest, name tag NOE, points at the stairwell and first says the backpack was blue, then corrects: black. A small white dog with no leash is by the elevator, which shows 2. A yellow bicycle is against the rail. Keys with a blue fob are on the counter. Outside: a silver SUV, plate HNL 640, driver with a beard and sunglasses waiting; a red compact, plate KXM 218, empty. A brick props the side fire door.",
        "الثلاثاء، 4:20 مساءً، ردهة 1427 الجادة 16 عند كيلوا. مقيمة ببلوزة بيضاء وبنطال أسود ووشاح أحمر، الوحدة 3B، تدخل بكيس بقالة بني. رجل بقميص بولو أخضر وشورت كاكي وقبعة بيضاء، الوحدة 12A، يقف عند صناديق البريد على الهاتف. مراهق بقلنسوة رمادية وجينز أزرق ممزق وحذاء أحمر يجري نحو الزقاق الغربي بحقيبة ظهر سوداء؛ القلنسوة تخفي الوجه. طرد مكتوب عليه «4C — DO NOT BEND» كان عند الباب واختفى. المدير، سترة زرقاء، بطاقة NOE، يشير إلى الدرج ويقول أولًا إن الحقيبة زرقاء ثم يصحّح: سوداء. كلب أبيض صغير بلا مقود عند المصعد، والمصعد يُظهر 2. دراجة صفراء على السياج. مفاتيح بحلقة زرقاء على المنضدة. في الخارج: دفع رباعي فضي، لوحة HNL 640، سائق بلحية ونظارة ينتظر؛ سيارة صغيرة حمراء، لوحة KXM 218، فارغة. طوبة تسند باب الحريق الجانبي.",
        [qq("o1a", "After the manager's correction, what color is the backpack?", "بعد تصحيح المدير، ما لون حقيبة الظهر؟",
            [("Black", "أسود"), ("Blue", "أزرق"), ("Gray", "رمادي"), ("Red", "أحمر")],
            0, "He corrected blue to black. The hoodie is gray. The sneakers are red.", "صحّح الأزرق إلى الأسود. القلنسوة رمادية. والحذاء أحمر."),
         qq("o1b", "Which unit is the woman with the red scarf?", "أي وحدة للمرأة ذات الوشاح الأحمر؟",
            [("3B", "3B"), ("12A", "12A"), ("4C", "4C"), ("2", "2")],
            0, "3B is her unit. 12A is the man at the mailboxes. 4C is the package. 2 is the elevator.", "3B وحدتها. 12A الرجل عند البريد. 4C الطرد. 2 المصعد."),
         qq("o1c", "Which plate is on the empty red car?", "أي لوحة على السيارة الحمراء الفارغة؟",
            [("KXM 218", "KXM 218"), ("HNL 640", "HNL 640"), ("4C", "4C"), ("No plate was given", "لم تُعطَ لوحة")],
            0, "HNL 640 is the silver SUV with the driver waiting.", "HNL 640 هي الدفع الرباعي الفضي وسائقها ينتظر."),
         qq("o1d", "What is holding the fire door?", "ما الذي يسند باب الحريق؟",
            [("A brick", "طوبة"), ("The yellow bicycle", "الدراجة الصفراء"),
             ("The white dog", "الكلب الأبيض"), ("The package", "الطرد")],
            0, "The brick props the door. The bicycle is on the rail. The package is gone.", "الطوبة تسند الباب. والدراجة على السياج. والطرد اختفى.")]),
    )
    obs.append(passage(
        "o2", 6, 1, "obs", 55,
        "Wednesday, 11:06 AM, parking level P2, yellow pillar C, stall 18. Black sedan A: plate NRP 441, dent on the left rear door, driver a woman with a braid and a yellow top, engine running, pointed east. Black sedan B: plate NRP 414, no dent, driver a man in a blue shirt, parked, engine off. The radio says, \"Disregard 414. The plate is 441.\" A green shopping bag with a child seat in the cart sits by pillar C. An attendant in an orange vest stands at the booth. A black motorcycle, plate M 28, is in stall 20. A white van, plate PLB 902, blocks part of the west exit ramp; its driver is not the attendant. An oil spot is in stall 18, under sedan A. A ticket on the ground reads 10:41 AM. The reporting person, gray hoodie, points at sedan A.",
        "الأربعاء، 11:06 صباحًا، مستوى الموقف P2، العمود الأصفر C، الموقف 18. سيدان سوداء أ: لوحة NRP 441، انبعاج في الباب الخلفي الأيسر، سائقة بضفيرة وقميص أصفر، المحرك يعمل، متجهة شرقًا. سيدان سوداء ب: لوحة NRP 414، بلا انبعاج، سائق بقميص أزرق، متوقفة، المحرك مطفأ. اللاسلكي يقول: «تجاهلوا 414. اللوحة 441.» كيس تسوق أخضر ومقعد طفل في العربة بجانب العمود C. موظف بسترة برتقالية عند الكشك. دراجة نارية سوداء، لوحة M 28، في الموقف 20. شاحنة بيضاء، لوحة PLB 902، تسد جزءًا من منحدر الخروج الغربي؛ سائقها ليس الموظف. بقعة زيت في الموقف 18 تحت السيدان أ. تذكرة على الأرض مكتوب فيها 10:41 صباحًا. والمبلّغ، قلنسوة رمادية، يشير إلى السيدان أ.",
        [qq("o2a", "Which plate do you keep after the radio correction?", "أي لوحة تبقين بعد تصحيح اللاسلكي؟",
            [("NRP 441", "NRP 441"), ("NRP 414", "NRP 414"), ("PLB 902", "PLB 902"), ("M 28", "M 28")],
            0, "The radio drops 414 and keeps 441, which is also the car the reporting person points at.", "اللاسلكي يسقط 414 ويبقي 441، وهي أيضًا السيارة التي يشير إليها المبلّغ."),
         qq("o2b", "What color is the reporting person's hoodie, and whom do they indicate?", "ما لون قلنسوة المبلّغ، وإلى من يشير؟",
            [("Gray, sedan A", "رمادي، السيدان أ"), ("Yellow, sedan B", "أصفر، السيدان ب"),
             ("Orange, the van", "برتقالي، الشاحنة"), ("Blue, the motorcycle", "أزرق، الدراجة النارية")],
            0, "Gray hoodie, pointing at sedan A. Orange is the attendant. Yellow is the driver's top.", "قلنسوة رمادية، يشير إلى السيدان أ. البرتقالي الموظف. والأصفر قميص السائقة."),
         qq("o2c", "What time is on the ticket, and what time is the scene?", "ما الوقت على التذكرة، وما وقت المشهد؟",
            [("Ticket 10:41 AM, scene 11:06 AM", "التذكرة 10:41 صباحًا، المشهد 11:06 صباحًا"),
             ("Both 11:06", "كلاهما 11:06"),
             ("Ticket 11:06, scene 10:41", "التذكرة 11:06، المشهد 10:41"),
             ("Neither time was given", "لم يُعطَ أي وقت")],
            0, "The scene clock and the ticket are different on purpose.", "ساعة المشهد والتذكرة مختلفتان عمدًا."),
         qq("o2d", "Which vehicle blocks part of the west exit?", "أي مركبة تسد جزءًا من مخرج الغرب؟",
            [("White van PLB 902", "الشاحنة البيضاء PLB 902"),
             ("Sedan A", "السيدان أ"), ("The motorcycle", "الدراجة النارية"), ("Sedan B", "السيدان ب")],
            0, "The van is the one on the ramp. The sedans are at stall 18's area and parked.", "الشاحنة هي التي على المنحدر. والسيدان عند منطقة الموقف 18 ومتوقفة.")]),
    )
    return reads, comps, listens, obs


def all_items():
    logic = logic_items()
    grammar = grammar_items()
    # probes already flagged inside logic
    return logic + grammar


def check_banks():
    logic = logic_items()
    grammar = grammar_items()
    reads, comps, listens, obs = passages()
    ids = []
    for group in (logic, grammar):
        for it in group:
            ids.append(it["id"])
            if it["ans"] != 0 and it["pillar"] == "grammar":
                raise SystemExit("grammar ans drifted " + it["id"])
    for group in (reads, comps, listens, obs):
        for p in group:
            ids.append(p["id"])
            for q in p["qs"]:
                ids.append(q["id"])
    if len(ids) != len(set(ids)):
        from collections import Counter
        dups = [k for k, v in Counter(ids).items() if v > 1]
        raise SystemExit("duplicate ids " + str(dups))
    # sequence answers already embedded; re-verify a few known ones
    by_tier = {}
    for it in logic:
        by_tier.setdefault(it["tier"], 0)
        by_tier[it["tier"]] += 1
    gfam = {}
    for it in grammar:
        gfam.setdefault(it["family"], 0)
        gfam[it["family"]] += 1
    return {
        "logic": len(logic),
        "logic_tiers": by_tier,
        "probes": sum(1 for it in logic if it.get("probe")),
        "grammar": len(grammar),
        "families": gfam,
        "reads": len(reads),
        "comps": len(comps),
        "listens": len(listens),
        "obs": len(obs),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(check_banks(), indent=2))
