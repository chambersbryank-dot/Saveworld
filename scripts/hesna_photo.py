#!/usr/bin/env python3
"""Picture quizzes for Hesna's DELPOE visual section.

Same picture, three 45-question passes, each finer than the last.
Then a new picture with the same 3×45 pattern.
Official shape: statements are true/false; later items are presence.
Study time is always 2 minutes. Original practice, not exam items.
"""
from __future__ import annotations

TF_EN = ["A. The statement is true.", "B. The statement is false."]
TF_AR = ["A. العبارة صحيحة.", "B. العبارة خطأ."]
PR_EN = ["A. Yes, it was in the picture.", "B. No, it was not in the picture."]
PR_AR = ["A. نعم، كان في الصورة.", "B. لا، لم يكن في الصورة."]


def tf(en, ar, yes):
    return [en, ar, TF_EN, TF_AR, 0 if yes else 1]


def pr(en, ar, yes):
    return [en, ar, PR_EN, PR_AR, 0 if yes else 1]


def quiz(qid, scene, band, img, alt, title, blurb, rows):
    if len(rows) != 45:
        raise SystemExit(f"{qid}: {len(rows)} questions, need 45")
    stems = [r[0] for r in rows]
    if len(set(stems)) != 45:
        raise SystemExit(f"{qid}: duplicate stem")
    trues = sum(1 for r in rows if r[4] == 0)
    if trues < 16 or trues > 30:
        raise SystemExit(f"{qid}: true-count {trues} is lopsided")
    return {
        "id": qid,
        "pic": 1,
        "scene": scene,
        "band": band,
        "secs": 120,
        "img": img,
        "alt": alt,
        "title": title,
        "blurb": blurb,
        "q": rows,
    }


def burglary():
    img = "hesna-7426-recall.jpg"
    alt = "Daytime burglary at a house numbered 7426"
    q1 = [
        tf("Two people are at the front of the house: one at the broken window and one carrying a television from the garage.", "شخصان عند واجهة البيت: واحد عند النافذة المكسورة وواحد يحمل تلفازًا من المرآب.", True),
        tf("One person is climbing through a broken front window.", "شخص يتسلق عبر نافذة أمامية مكسورة.", True),
        tf("One person is carrying a large flat television out of the garage.", "شخص يحمل تلفازًا مسطحًا كبيرًا خارج المرآب.", True),
        tf("The garage door is open.", "باب المرآب مفتوح.", True),
        tf("The front door is open.", "الباب الأمامي مفتوح.", True),
        tf("The number on the mailbox is 7426.", "الرقم على صندوق البريد هو 7426.", True),
        tf("A dark SUV is in the driveway with its rear hatch open.", "دفع رباعي داكن في الممر وبابه الخلفي مفتوح.", True),
        tf("A gray sedan is partly visible at the curb in the foreground.", "سيدان رمادية ظاهرة جزئيًا عند الرصيف في المقدمة.", True),
        tf("The picture was taken in daylight.", "أُخذت الصورة في وضح النهار.", True),
        tf("There is a swimming pool behind the house.", "يوجد مسبح خلف البيت.", True),
        tf("A dog is in the picture.", "يوجد كلب في الصورة.", True),
        tf("Broken glass is on the ground by the broken window.", "زجاج مكسور على الأرض بجانب النافذة المكسورة.", True),
        tf("The person at the window is wearing a backpack.", "الشخص عند النافذة يلبس حقيبة ظهر.", True),
        tf("Bags are visible in the open cargo area of the SUV.", "حقائب ظاهرة في صندوق الدفع الرباعي المفتوح.", True),
        tf("A wooden fence runs along the backyard.", "سياج خشبي يمتد في الفناء الخلفي.", True),
        tf("The front lawn is green.", "العشب الأمامي أخضر.", True),
        tf("A green trash cart is at the lower right, by the street.", "حاوية نفايات خضراء في أسفل اليمين قرب الشارع.", True),
        tf("Three people are carrying items out of the house.", "ثلاثة أشخاص يحملون أغراضًا خارج البيت.", False),
        tf("The garage door is closed.", "باب المرآب مغلق.", False),
        tf("The mailbox number is 7462.", "رقم صندوق البريد 7462.", False),
        tf("The SUV's rear hatch is shut.", "الباب الخلفي للدفع الرباعي مغلق.", False),
        tf("This is a night scene with no daylight.", "هذا مشهد ليلي بلا ضوء نهار.", False),
        tf("There is no swimming pool.", "لا يوجد مسبح.", False),
        tf("A marked police car is parked in the driveway.", "سيارة شرطة معلّمة متوقفة في الممر.", False),
        tf("The person at the window is the one carrying the television.", "الشخص عند النافذة هو الذي يحمل التلفاز.", False),
        tf("The gray sedan is parked inside the garage.", "السيدان الرمادية متوقفة داخل المرآب.", False),
        tf("The dog is swimming in the pool.", "الكلب يسبح في المسبح.", False),
        tf("The front window is intact, with no broken glass.", "النافذة الأمامية سليمة بلا زجاج مكسور.", False),
        tf("The trash cart is red.", "حاوية النفايات حمراء.", False),
        tf("The house number on the mailbox is 7246.", "رقم البيت على صندوق البريد 7246.", False),
        pr("A mailbox", "صندوق بريد", True),
        pr("A swimming pool", "مسبح", True),
        pr("A dog", "كلب", True),
        pr("A bicycle", "دراجة", True),
        pr("A flat television", "تلفاز مسطح", True),
        pr("A backpack", "حقيبة ظهر", True),
        pr("A green trash cart", "حاوية نفايات خضراء", True),
        pr("A wooden fence", "سياج خشبي", True),
        pr("An open patio umbrella", "مظلة فناء مفتوحة", True),
        pr("A red tool chest", "صندوق عدة أحمر", True),
        pr("A fire truck", "سيارة إطفاء", False),
        pr("A uniformed police officer", "ضابط شرطة بزي رسمي", False),
        pr("A school bus", "حافلة مدرسية", False),
        pr("A cat", "قطة", False),
        pr("A stop sign", "إشارة قف", False),
    ]
    q2 = [
        tf("The person at the window wears a black backpack.", "الشخص عند النافذة يلبس حقيبة ظهر سوداء.", True),
        tf("The person at the window wears a black beanie, not a baseball cap.", "الشخص عند النافذة يلبس قلنسوة سوداء لا قبعة بيسبول.", True),
        tf("The person at the window wears dark pants and light gray sneakers.", "الشخص عند النافذة يلبس بنطالًا داكنًا وحذاءً رياضيًا رماديًا فاتحًا.", True),
        tf("The person carrying the television wears a dark hoodie.", "الشخص الذي يحمل التلفاز يلبس قلنسوة داكنة.", True),
        tf("The person carrying the television wears a black baseball cap.", "الشخص الذي يحمل التلفاز يلبس قبعة بيسبول سوداء.", True),
        tf("The television being carried is black.", "التلفاز المحمول أسود.", True),
        tf("The rolling tool chest inside the garage is red.", "صندوق العدة المتحرك داخل المرآب أحمر.", True),
        tf("The bicycle inside the garage is dark green.", "الدراجة داخل المرآب خضراء داكنة.", True),
        tf("A blue bag lies on the driveway in front of the garage.", "حقيبة زرقاء على الممر أمام المرآب.", True),
        tf("A black case lies on the driveway near that blue bag.", "صندوق أسود على الممر قرب تلك الحقيبة الزرقاء.", True),
        tf("The pool water looks blue.", "ماء المسبح يبدو أزرق.", True),
        tf("The dog's coat is golden brown.", "فرو الكلب بني ذهبي.", True),
        tf("The dog is on the near side of the fence, not in the water.", "الكلب في الجهة القريبة من السياج، لا في الماء.", True),
        tf("One patio umbrella is open and light colored.", "إحدى مظلات الفناء مفتوحة وفاتحة اللون.", True),
        tf("One patio umbrella is closed and dark, not striped.", "إحدى مظلات الفناء مغلقة وداكنة، لا مخططة.", True),
        tf("Lounge chairs by the pool are blue and white striped.", "كراسي الاستلقاء عند المسبح مخططة بالأزرق والأبيض.", True),
        tf("The mailbox is black and its post is white.", "صندوق البريد أسود وعموده أبيض.", True),
        tf("The person with the television is moving toward the SUV.", "الشخص الذي معه التلفاز يتحرك نحو الدفع الرباعي.", True),
        tf("The window climber wears a bright red jacket.", "المتسلق عند النافذة يلبس سترة حمراء زاهية.", False),
        tf("The television carrier is bareheaded.", "حامل التلفاز مكشوف الرأس.", False),
        tf("The bicycle in the garage is red.", "الدراجة في المرآب حمراء.", False),
        tf("The tool chest is white.", "صندوق العدة أبيض.", False),
        tf("The dog is black.", "الكلب أسود.", False),
        tf("Both patio umbrellas are closed.", "مظلتا الفناء مغلقتان.", False),
        tf("The pool has no water.", "المسبح بلا ماء.", False),
        tf("The mailbox is red.", "صندوق البريد أحمر.", False),
        tf("The SUV cargo area is empty.", "صندوق الدفع الرباعي فارغ.", False),
        tf("The window climber wears a baseball cap and no backpack.", "المتسلق عند النافذة يلبس قبعة بيسبول بلا حقيبة ظهر.", False),
        tf("The television carrier wears a yellow shirt.", "حامل التلفاز يلبس قميصًا أصفر.", False),
        tf("The sedan's visible rear lamp is green.", "مصباح السيدان الخلفي الظاهر أخضر.", False),
        pr("A red tool chest", "صندوق عدة أحمر", True),
        pr("A dark green bicycle", "دراجة خضراء داكنة", True),
        pr("A blue hard-shell suitcase in the SUV", "حقيبة صلبة زرقاء في الدفع الرباعي", True),
        pr("A green bag in the SUV", "حقيبة خضراء في الدفع الرباعي", True),
        pr("A striped lounge chair", "كرسي استلقاء مخطط", True),
        pr("An open light-colored umbrella", "مظلة فاتحة مفتوحة", True),
        pr("A closed dark umbrella", "مظلة داكنة مغلقة", True),
        pr("A black baseball cap on the television carrier", "قبعة بيسبول سوداء على حامل التلفاز", True),
        pr("A beanie on the window climber", "قلنسوة على المتسلق عند النافذة", True),
        pr("A blue bag on the driveway", "حقيبة زرقاء على الممر", True),
        pr("A fire hydrant", "صنبور حريق", False),
        pr("A baby stroller", "عربة أطفال", False),
        pr("A motorcycle", "دراجة نارية", False),
        pr("A yellow taxi", "سيارة أجرة صفراء", False),
        pr("A person in the pool", "شخص في المسبح", False),
    ]
    q3 = [
        tf("The mailbox digits are 7, then 4, then 2, then 6.", "أرقام صندوق البريد هي 7 ثم 4 ثم 2 ثم 6.", True),
        tf("The gray sedan shows a Toyota emblem.", "السيدان الرمادية عليها شعار تويوتا.", True),
        tf("The sedan's trunk badge reads SE.", "شارة صندوق السيدان تُقرأ SE.", True),
        tf("The sedan plate is a Hawaii plate with a palm tree.", "لوحة السيدان لوحة هاواي فيها نخلة.", True),
        tf("The digits 318 appear on the sedan plate.", "الأرقام 318 ظاهرة على لوحة السيدان.", True),
        tf("The SUV cargo area holds one blue hard-shell suitcase, not two.", "صندوق الدفع الرباعي فيه حقيبة صلبة زرقاء واحدة، لا اثنتان.", True),
        tf("The SUV cargo area holds a tan bag and a darker green bag.", "صندوق الدفع الرباعي فيه حقيبة بنية فاتحة وحقيبة خضراء أغمق.", True),
        tf("A yellow strap lies in the SUV cargo area.", "حزام أصفر في صندوق الدفع الرباعي.", True),
        tf("The blue duffel is on the driveway, not inside the SUV.", "الحقيبة الزرقاء القماشية على الممر، لا داخل الدفع الرباعي.", True),
        tf("The window climber's pants are black.", "بنطال المتسلق عند النافذة أسود.", True),
        tf("The television carrier's shoes are black with white soles.", "حذاء حامل التلفاز أسود بنعل أبيض.", True),
        tf("Shelves of stored items are visible inside the garage.", "رفوف بأغراض مخزّنة ظاهرة داخل المرآب.", True),
        tf("A blue storage bin is inside the garage.", "صندوق تخزين أزرق داخل المرآب.", True),
        tf("A screen or monitor is visible inside the garage.", "شاشة ظاهرة داخل المرآب.", True),
        tf("A neighbor's house is visible beyond the backyard fence.", "بيت جارٍ ظاهر وراء سياج الفناء.", True),
        tf("Nobody is in the pool.", "لا أحد في المسبح.", True),
        tf("Blinds are visible in the broken window.", "ستائر ظاهرة في النافذة المكسورة.", True),
        tf("The SUV has roof rails.", "للدفع الرباعي قضبان على السقف.", True),
        tf("A lit lantern is mounted on the wall by the garage.", "فانوس مضاء مثبّت على الجدار بجانب المرآب.", True),
        tf("The front door is dark and standing open.", "الباب الأمامي داكن ومفتوح.", True),
        tf("The mailbox number is 7246.", "رقم صندوق البريد 7246.", False),
        tf("The visible number on the sedan plate is 813.", "الرقم الظاهر على لوحة السيدان هو 813.", False),
        tf("The gray sedan shows a Honda emblem.", "السيدان الرمادية عليها شعار هوندا.", False),
        tf("Three blue suitcases are in the SUV.", "ثلاث حقائب زرقاء في الدفع الرباعي.", False),
        tf("The yellow strap is tied to the mailbox.", "الحزام الأصفر مربوط بصندوق البريد.", False),
        tf("The dog is inside the pool fence, in the water.", "الكلب داخل سياج المسبح، في الماء.", False),
        tf("A large street clock reading 10:10 is the center of the picture.", "ساعة شارع كبيرة تشير إلى 10:10 هي مركز الصورة.", False),
        tf("The green trash cart is at the lower left, in front of the sedan.", "حاوية النفايات الخضراء في أسفل اليسار أمام السيدان.", False),
        tf("The bicycle is inside the SUV.", "الدراجة داخل الدفع الرباعي.", False),
        tf("The sedan plate is a plain white plate with no palm tree.", "لوحة السيدان بيضاء بسيطة بلا نخلة.", False),
        pr("A Hawaii license plate", "لوحة هاواي", True),
        pr("A Toyota emblem", "شعار تويوتا", True),
        pr("Roof rails on the SUV", "قضبان سقف على الدفع الرباعي", True),
        pr("A yellow strap in the cargo area", "حزام أصفر في الصندوق", True),
        pr("Pale broken glass by the window", "زجاج مكسور فاتح بجانب النافذة", True),
        pr("A stone column by the garage", "عمود حجري بجانب المرآب", True),
        pr("A palm-like plant by the garage", "نبتة تشبه النخيل بجانب المرآب", True),
        pr("Two blue hard-shell suitcases", "حقيبتان صلبتان زرقاوان", False),
        pr("A tan bag in the SUV", "حقيبة بنية فاتحة في الدفع الرباعي", True),
        pr("A monitor inside the garage", "شاشة داخل المرآب", True),
        pr("An ambulance", "سيارة إسعاف", False),
        pr("A second dog", "كلب ثانٍ", False),
        pr("A person swimming", "شخص يسبح", False),
        pr("A red trash cart", "حاوية نفايات حمراء", False),
        pr("A surfboard", "لوح ركوب أمواج", False),
    ]
    title = [
        ["7426 burglary · quiz 1 of 3 · broad", "سطو 7426 · الاختبار 1 من 3 · الصورة الكبيرة"],
        ["7426 burglary · quiz 2 of 3 · attributes", "سطو 7426 · الاختبار 2 من 3 · الصفات"],
        ["7426 burglary · quiz 3 of 3 · fine detail", "سطو 7426 · الاختبار 3 من 3 · التفاصيل الدقيقة"],
    ]
    blurb = [
        ["Same picture. Who, what, and the large objects. Zig-zag once, then name people, vehicles, and the house.",
         "الصورة نفسها. من، وماذا، والأغراض الكبيرة. مسح متعرج مرة، ثم سمّي الأشخاص والمركبات والبيت."],
        ["Same picture, closer. Clothing, colors, and where each thing sits.",
         "الصورة نفسها، أقرب. الملابس والألوان ومكان كل شيء."],
        ["Same picture, the small print: digits, badges, counts, and what is absent.",
         "الصورة نفسها، الحرف الصغير: الأرقام والشارات والعدد وما هو غائب."],
    ]
    out = []
    for band, rows, t, b in zip((1, 2, 3), (q1, q2, q3), title, blurb):
        out.append(quiz(f"b7426-{band}", "b7426", band, img, alt, t, b, rows))
    return out


def quickstop():
    img = "hesna-quickstop-recall.jpg"
    alt = "Daytime grab-and-run outside a Quick Stop store"
    q1 = [
        tf("The store sign reads QUICK STOP.", "لافتة المتجر تقول QUICK STOP.", True),
        tf("A person in a yellow jacket is running.", "شخص بسترة صفراء يجري.", True),
        tf("That runner wears a red cap.", "العدّاء يلبس قبعة حمراء.", True),
        tf("The runner carries a red bag.", "العدّاء يحمل حقيبة حمراء.", True),
        tf("A clerk in a green apron stands in the doorway.", "موظف بمئزر أخضر يقف في المدخل.", True),
        tf("The clerk wears a white shirt.", "الموظف يلبس قميصًا أبيض.", True),
        tf("A child in a green shirt stands by a shopping cart.", "طفل بقميص أخضر يقف بجانب عربة تسوق.", True),
        tf("The cart holds a pineapple and a white jug.", "العربة فيها أناناس وإبريق أبيض.", True),
        tf("A silver sedan has a door open.", "سيدان فضية وبابها مفتوح.", True),
        tf("A blue pickup is parked beside the sedan.", "بيك أب أزرق متوقف بجانب السيدان.", True),
        tf("An orange cone is on the pavement in front of the sedan.", "مخروط برتقالي على الأرض أمام السيدان.", True),
        tf("A black dog sits near that cone.", "كلب أسود جالس قرب ذلك المخروط.", True),
        tf("It is daytime, with a blue sky and clouds.", "الوقت نهار، والسماء زرقاء وفيها غيوم.", True),
        tf("The store walls are beige.", "جدران المتجر بيج.", True),
        tf("This scene is a store parking lot, not a house.", "هذا المشهد موقف متجر، لا بيت.", True),
        tf("The runner's pants are black.", "بنطال العدّاء أسود.", True),
        tf("The store sign reads HALE MART.", "لافتة المتجر تقول HALE MART.", False),
        tf("The runner's jacket is blue.", "سترة العدّاء زرقاء.", False),
        tf("The clerk wears a red apron.", "الموظف يلبس مئزرًا أحمر.", False),
        tf("The child is sitting in the driver's seat.", "الطفل جالس في مقعد السائق.", False),
        tf("The pickup is red.", "البيك أب أحمر.", False),
        tf("The dog is golden brown.", "الكلب بني ذهبي.", False),
        tf("The cone is blue.", "المخروط أزرق.", False),
        tf("It is raining at night.", "إنها تمطر ليلًا.", False),
        tf("A police car is in the lot.", "سيارة شرطة في الموقف.", False),
        tf("The shopping cart is empty.", "عربة التسوق فارغة.", False),
        tf("The runner is carrying the pineapple.", "العدّاء يحمل الأناناس.", False),
        tf("The child wears a yellow jacket.", "الطفل يلبس سترة صفراء.", False),
        tf("The silver car's doors are all shut.", "أبواب السيارة الفضية كلها مغلقة.", False),
        tf("The clerk is inside the blue pickup.", "الموظف داخل البيك أب الأزرق.", False),
        pr("A QUICK STOP sign", "لافتة QUICK STOP", True),
        pr("A green apron", "مئزر أخضر", True),
        pr("A red cap", "قبعة حمراء", True),
        pr("A pineapple", "أناناس", True),
        pr("A shopping cart", "عربة تسوق", True),
        pr("An orange cone", "مخروط برتقالي", True),
        pr("A black dog", "كلب أسود", True),
        pr("A blue pickup", "بيك أب أزرق", True),
        pr("An open car door", "باب سيارة مفتوح", True),
        pr("A red bag", "حقيبة حمراء", True),
        pr("A swimming pool", "مسبح", False),
        pr("A fire truck", "سيارة إطفاء", False),
        pr("A police officer", "ضابط شرطة", False),
        pr("A mailbox numbered 7426", "صندوق بريد رقمه 7426", False),
        pr("A bicycle", "دراجة", False),
    ]
    q2 = [
        tf("The runner is an adult in a yellow jacket, black pants, and a red cap.", "العدّاء بالغ بسترة صفراء وبنطال أسود وقبعة حمراء.", True),
        tf("The runner's shoes are black with light soles.", "حذاء العدّاء أسود بنعل فاتح.", True),
        tf("The child wears a green T-shirt, dark shorts, and dark shoes with light soles.", "الطفل يلبس قميصًا أخضر وشورتًا داكنًا وحذاءً داكنًا بنعل فاتح.", True),
        tf("The child is standing, not running.", "الطفل واقف، لا يجري.", True),
        tf("The clerk's apron is green and the shirt under it is white.", "مئزر الموظف أخضر والقميص تحته أبيض.", True),
        tf("The clerk is pointing, with an arm extended.", "الموظف يشير وذراعه ممدودة.", True),
        tf("The open door is on the silver sedan, on the side facing the camera.", "الباب المفتوح على السيدان الفضية، في الجهة المواجهة للكاميرا.", True),
        tf("The blue pickup is behind the sedan, toward the right of the picture.", "البيك أب الأزرق خلف السيدان، نحو يمين الصورة.", True),
        tf("The shopping cart is to the left of the doorway.", "عربة التسوق على يسار المدخل.", True),
        tf("The pineapple and the white jug are both in the cart.", "الأناناس والإبريق الأبيض كلاهما في العربة.", True),
        tf("The black dog is sitting, not running with the yellow jacket.", "الكلب الأسود جالس، لا يجري مع السترة الصفراء.", True),
        tf("The orange cone is closer to the sedan than to the shopping cart.", "المخروط البرتقالي أقرب إلى السيدان منه إلى عربة التسوق.", True),
        tf("The store has a glass door, and that door is open.", "للمتجر باب زجاجي، والباب مفتوح.", True),
        tf("Trees are visible beyond the parking lot.", "أشجار ظاهرة وراء الموقف.", True),
        tf("The runner is moving past the open sedan door.", "العدّاء يتحرك مارًّا بباب السيدان المفتوح.", True),
        tf("The child is looking toward the doorway, not driving the pickup.", "الطفل ينظر نحو المدخل، لا يقود البيك أب.", True),
        tf("The runner's cap is blue.", "قبعة العدّاء زرقاء.", False),
        tf("The child's shirt is red.", "قميص الطفل أحمر.", False),
        tf("The dog is running beside the person in yellow.", "الكلب يجري بجانب الشخص بالأصفر.", False),
        tf("The cone is next to the shopping cart.", "المخروط بجانب عربة التسوق.", False),
        tf("The pickup is in front of the sedan, blocking the door.", "البيك أب أمام السيدان يسد الباب.", False),
        tf("The clerk wears a yellow jacket and a red cap.", "الموظف يلبس سترة صفراء وقبعة حمراء.", False),
        tf("The white jug is in the runner's red bag.", "الإبريق الأبيض في حقيبة العدّاء الحمراء.", False),
        tf("The store walls are red brick.", "جدران المتجر آجر أحمر.", False),
        tf("The silver sedan is a pickup.", "السيدان الفضية بيك أب.", False),
        tf("Two dogs are in the lot.", "كلبان في الموقف.", False),
        tf("The child is wearing the green apron.", "الطفل يلبس المئزر الأخضر.", False),
        tf("The sky is gray and the lot is wet.", "السماء رمادية والموقف مبلل.", False),
        tf("The red bag is in the shopping cart.", "الحقيبة الحمراء في عربة التسوق.", False),
        tf("The clerk is sitting in the sedan.", "الموظف جالس في السيدان.", False),
        pr("A white jug in the cart", "إبريق أبيض في العربة", True),
        pr("Dark shoes with light soles on the child", "حذاء داكن بنعل فاتح على الطفل", True),
        pr("A red cap on the runner", "قبعة حمراء على العدّاء", True),
        pr("A glass store door", "باب متجر زجاجي", True),
        pr("Clouds", "غيوم", True),
        pr("A beige store wall", "جدار متجر بيج", True),
        pr("A silver sedan", "سيدان فضية", True),
        pr("A black dog sitting", "كلب أسود جالس", True),
        pr("An extended arm on the clerk", "ذراع ممدودة للموظف", True),
        pr("Trees beyond the lot", "أشجار وراء الموقف", True),
        pr("A swimming pool", "مسبح", False),
        pr("A golden retriever", "كلب ذهبي", False),
        pr("A red pickup", "بيك أب أحمر", False),
        pr("A uniformed officer", "ضابط بزي رسمي", False),
        pr("A house mailbox", "صندوق بريد بيت", False),
    ]
    q3 = [
        tf("The words on the storefront are QUICK STOP, not STOP QUICK.", "الكلمات على الواجهة QUICK STOP، لا STOP QUICK.", True),
        tf("A no-smoking sign is on the wall to the right of the door.", "لافتة ممنوع التدخين على الجدار يمين الباب.", True),
        tf("The no-smoking sign is a small wall sign, not the big store name.", "لافتة ممنوع التدخين لافتة جدار صغيرة، لا اسم المتجر الكبير.", True),
        tf("The silver sedan shows a Toyota emblem.", "السيدان الفضية عليها شعار تويوتا.", True),
        tf("The open door is the near-side door of the silver sedan, facing the camera.", "الباب المفتوح هو الباب القريب من السيدان الفضية، المواجه للكاميرا.", True),
        tf("The runner's hair is pulled back.", "شعر العدّاء مشدود إلى الخلف.", True),
        tf("The runner carries one red bag, not the pineapple.", "العدّاء يحمل حقيبة حمراء واحدة، لا الأناناس.", True),
        tf("The cart has one pineapple and one white jug, not a stack of boxes.", "العربة فيها أناناس واحد وإبريق أبيض واحد، لا كومة صناديق.", True),
        tf("The black dog wears a collar.", "الكلب الأسود يلبس طوقًا.", True),
        tf("The cone is orange and sits on the asphalt in front of the sedan.", "المخروط برتقالي وعلى الأسفلت أمام السيدان.", True),
        tf("The pickup is blue and is a pickup, not a van.", "البيك أب أزرق وهو بيك أب، لا فان.", True),
        tf("The child is shorter than the clerk and stands outside, by the cart.", "الطفل أقصر من الموظف ويقف خارجًا بجانب العربة.", True),
        tf("The clerk is a man in the doorway, not the person in the yellow jacket.", "الموظف رجل في المدخل، لا الشخص بالسترة الصفراء.", True),
        tf("No police vehicle is in the frame.", "لا مركبة شرطة في الإطار.", True),
        tf("The lot surface is asphalt, not grass.", "أرض الموقف أسفلت، لا عشب.", True),
        tf("The store name on the wall is HALE MART.", "اسم المتجر على الجدار HALE MART.", False),
        tf("The wall sign says NO PARKING and there is no no-smoking sign.", "لافتة الجدار تقول NO PARKING ولا توجد لافتة ممنوع تدخين.", False),
        tf("The sedan emblem is a Tesla mark.", "شعار السيدان علامة تسلا.", False),
        tf("The plate digits 318 are the large text over the door.", "أرقام اللوحة 318 هي النص الكبير فوق الباب.", False),
        tf("The runner's bag is green.", "حقيبة العدّاء خضراء.", False),
        tf("Two pineapples are in the cart.", "أناناسان في العربة.", False),
        tf("The dog is standing on the sedan's hood.", "الكلب واقف على غطاء السيدان.", False),
        tf("The cone is yellow.", "المخروط أصفر.", False),
        tf("The child's shoes are red.", "حذاء الطفل أحمر.", False),
        tf("The clerk's apron is yellow.", "مئزر الموظف أصفر.", False),
        tf("A house number 7426 is on the store.", "رقم البيت 7426 على المتجر.", False),
        tf("The pickup is white.", "البيك أب أبيض.", False),
        tf("Three people wear red caps.", "ثلاثة أشخاص يلبسون قبعات حمراء.", False),
        tf("The door under the QUICK STOP sign is closed and dark.", "الباب تحت لافتة QUICK STOP مغلق ومظلم.", False),
        tf("The runner is barefoot.", "العدّاء حافي القدمين.", False),
        pr("A no-smoking sign", "لافتة ممنوع التدخين", True),
        pr("The words QUICK STOP", "كلمتا QUICK STOP", True),
        pr("A Toyota emblem", "شعار تويوتا", True),
        pr("A collar on the black dog", "طوق على الكلب الأسود", True),
        pr("A ponytail on the runner", "ذيل حصان على العدّاء", True),
        pr("One pineapple", "أناناس واحد", True),
        pr("One white jug", "إبريق أبيض واحد", True),
        pr("Asphalt", "أسفلت", True),
        pr("A beige wall", "جدار بيج", True),
        pr("An open driver door", "باب سائق مفتوح", True),
        pr("A Hawaii plate reading 7426", "لوحة هاواي مكتوب فيها 7426", False),
        pr("A swimming pool", "مسبح", False),
        pr("A second child", "طفل ثانٍ", False),
        pr("An ambulance", "سيارة إسعاف", False),
        pr("A red tool chest", "صندوق عدة أحمر", False),
    ]
    title = [
        ["Quick Stop · quiz 1 of 3 · broad", "كويك ستوب · الاختبار 1 من 3 · الصورة الكبيرة"],
        ["Quick Stop · quiz 2 of 3 · attributes", "كويك ستوب · الاختبار 2 من 3 · الصفات"],
        ["Quick Stop · quiz 3 of 3 · fine detail", "كويك ستوب · الاختبار 3 من 3 · التفاصيل الدقيقة"],
    ]
    blurb = [
        ["New picture. Same habit: the whole scene, then people, vehicles, and the sign.",
         "صورة جديدة. العادة نفسها: المشهد كله، ثم الأشخاص والمركبات واللافتة."],
        ["Same Quick Stop picture. Colors, clothes, and which side each thing is on.",
         "صورة كويك ستوب نفسها. الألوان والملابس وأي جهة لكل شيء."],
        ["Same picture. Readable words, emblems, and the objects that are not there.",
         "الصورة نفسها. الكلمات المقروءة والشعارات والأغراض غير الموجودة."],
    ]
    out = []
    for band, rows, t, b in zip((1, 2, 3), (q1, q2, q3), title, blurb):
        out.append(quiz(f"qstop-{band}", "qstop", band, img, alt, t, b, rows))
    return out


def corner():
    img = "hesna-corner-recall.jpg"
    alt = "Daytime fender bender between a red car and a white van"
    q1 = [
        tf("A red car and a white van have hit each other.", "سيارة حمراء وفان أبيض اصطدما.", True),
        tf("The damage is at the front of the red car.", "الضرر في مقدمة السيارة الحمراء.", True),
        tf("A woman in a purple top and white pants stands by the red car.", "امرأة بقميص بنفسجي وبنطال أبيض تقف عند السيارة الحمراء.", True),
        tf("She is holding a phone.", "هي تمسك هاتفًا.", True),
        tf("A man in an orange safety vest stands by the white van.", "رجل بسترة سلامة برتقالية يقف عند الفان الأبيض.", True),
        tf("He wears a white cap.", "هو يلبس قبعة بيضاء.", True),
        tf("A blue bicycle is beside a yellow fire hydrant.", "دراجة زرقاء بجانب صنبور حريق أصفر.", True),
        tf("The crosswalk stripes are green.", "خطوط ممر المشاة خضراء.", True),
        tf("A person in a pink hoodie has a dog on a leash.", "شخص بقلنسوة وردية معه كلب بمقود.", True),
        tf("The scene is a residential street in daylight.", "المشهد شارع سكني في وضح النهار.", True),
        tf("Houses with porches line the street.", "بيوت بشرفات على امتداد الشارع.", True),
        tf("Two cups sit on the hood of the red car.", "كوبان على غطاء السيارة الحمراء.", True),
        tf("The van is white.", "الفان أبيض.", True),
        tf("The sky is blue with clouds.", "السماء زرقاء وفيها غيوم.", True),
        tf("No ambulance is in the picture.", "لا سيارة إسعاف في الصورة.", True),
        tf("The red car is the smaller vehicle.", "السيارة الحمراء هي المركبة الأصغر.", True),
        tf("Three cars are in the crash.", "ثلاث سيارات في الحادث.", False),
        tf("The van is red and the car is white.", "الفان أحمر والسيارة بيضاء.", False),
        tf("The woman wears the orange vest.", "المرأة تلبس السترة البرتقالية.", False),
        tf("The cups are on the van's hood.", "الكوبان على غطاء الفان.", False),
        tf("The dog is black.", "الكلب أسود.", False),
        tf("The crosswalk stripes are yellow.", "خطوط ممر المشاة صفراء.", False),
        tf("It is night.", "الوقت ليل.", False),
        tf("An ambulance is parked behind the van.", "سيارة إسعاف متوقفة خلف الفان.", False),
        tf("The fire hydrant is red.", "صنبور الحريق أحمر.", False),
        tf("The bicycle is red.", "الدراجة حمراء.", False),
        tf("The man by the van is wearing a pink hoodie.", "الرجل عند الفان يلبس قلنسوة وردية.", False),
        tf("The woman is sitting inside the van.", "المرأة جالسة داخل الفان.", False),
        tf("The dog is loose in the crosswalk with no person.", "الكلب طليق في ممر المشاة بلا شخص.", False),
        tf("This is the 7426 house burglary.", "هذا سطو البيت 7426.", False),
        pr("A red car", "سيارة حمراء", True),
        pr("A white van", "فان أبيض", True),
        pr("A yellow fire hydrant", "صنبور حريق أصفر", True),
        pr("A blue bicycle", "دراجة زرقاء", True),
        pr("A phone", "هاتف", True),
        pr("An orange safety vest", "سترة سلامة برتقالية", True),
        pr("A pink hoodie", "قلنسوة وردية", True),
        pr("A dog on a leash", "كلب بمقود", True),
        pr("Green crosswalk stripes", "خطوط ممر مشاة خضراء", True),
        pr("Cups on a hood", "أكواب على غطاء", True),
        pr("An ambulance", "سيارة إسعاف", False),
        pr("A police car", "سيارة شرطة", False),
        pr("A swimming pool", "مسبح", False),
        pr("A flat television", "تلفاز مسطح", False),
        pr("A pineapple", "أناناس", False),
    ]
    q2 = [
        tf("The woman by the red car has dark hair, a purple blouse, and white pants.", "المرأة عند السيارة الحمراء شعرها داكن وقميصها بنفسجي وبنطالها أبيض.", True),
        tf("The man by the van wears khaki shorts under the orange vest.", "الرجل عند الفان يلبس شورتًا كاكي تحت السترة البرتقالية.", True),
        tf("A gray shirt shows under his vest.", "قميص رمادي ظاهر تحت سترته.", True),
        tf("His cap is white.", "قبعته بيضاء.", True),
        tf("The person with the dog wears pink and stands on the sidewalk, away from the cars.", "الشخص الذي معه الكلب يلبس ورديًا ويقف على الرصيف بعيدًا عن السيارتين.", True),
        tf("The dog with that person is brown.", "الكلب مع ذلك الشخص بني.", True),
        tf("Exactly two cups are on the red car's hood.", "كوبان بالضبط على غطاء السيارة الحمراء.", True),
        tf("The cups are light colored.", "الكوبان فاتحا اللون.", True),
        tf("The bicycle is on the sidewalk side, next to the hydrant, not in the middle of the crosswalk.", "الدراجة في جهة الرصيف بجانب الصنبور، لا في وسط ممر المشاة.", True),
        tf("The hydrant is yellow and close to the bicycle.", "الصنبور أصفر وقريب من الدراجة.", True),
        tf("A yellow pedestrian-crossing sign is on a pole.", "إشارة عبور مشاة صفراء على عمود.", True),
        tf("A green street-name sign is also on a pole.", "لافتة اسم شارع خضراء أيضًا على عمود.", True),
        tf("The front of the red car is against the white van.", "مقدمة السيارة الحمراء على الفان الأبيض.", True),
        tf("The woman is standing outside the red car, not in the driver's seat.", "المرأة واقفة خارج السيارة الحمراء، لا في مقعد السائق.", True),
        tf("Trees and front porches are behind the people.", "أشجار وشرفات أمامية خلف الأشخاص.", True),
        tf("The man is standing at the van's side door area.", "الرجل واقف عند منطقة الباب الجانبي للفان.", True),
        tf("The woman's pants are purple and her top is white.", "بنطال المرأة بنفسجي وقميصها أبيض.", False),
        tf("The man's vest is yellow and his cap is red.", "سترة الرجل صفراء وقبعته حمراء.", False),
        tf("The dog is with the man in the orange vest.", "الكلب مع الرجل بالسترة البرتقالية.", False),
        tf("One cup is on the hood.", "كوب واحد على الغطاء.", False),
        tf("The bicycle is white.", "الدراجة بيضاء.", False),
        tf("The pedestrian sign is a red stop sign.", "إشارة المشاة هي إشارة قف حمراء.", False),
        tf("The van is a blue pickup.", "الفان بيك أب أزرق.", False),
        tf("The woman in purple is holding the dog's leash.", "المرأة بالبنفسجي تمسك مقود الكلب.", False),
        tf("The hydrant is next to the pink hoodie.", "الصنبور بجانب القلنسوة الوردية.", False),
        tf("The crosswalk is behind the houses, not under the cars.", "ممر المشاة خلف البيوت، لا تحت السيارتين.", False),
        tf("The man is bareheaded.", "الرجل مكشوف الرأس.", False),
        tf("Four cups are on the hood.", "أربعة أكواب على الغطاء.", False),
        tf("The red car has no visible damage.", "السيارة الحمراء بلا ضرر ظاهر.", False),
        tf("The person in pink is standing in the van's cargo area.", "الشخص بالوردي واقف في صندوق الفان.", False),
        pr("Khaki shorts", "شورت كاكي", True),
        pr("A white cap", "قبعة بيضاء", True),
        pr("A gray shirt under a vest", "قميص رمادي تحت سترة", True),
        pr("A brown dog", "كلب بني", True),
        pr("A yellow pedestrian sign", "إشارة مشاة صفراء", True),
        pr("A green street-name sign", "لافتة اسم شارع خضراء", True),
        pr("Two cups", "كوبان", True),
        pr("Front porches", "شرفات أمامية", True),
        pr("A leash", "مقود", True),
        pr("White pants", "بنطال أبيض", True),
        pr("A black dog", "كلب أسود", False),
        pr("A red hydrant", "صنبور أحمر", False),
        pr("A shopping cart", "عربة تسوق", False),
        pr("A green apron", "مئزر أخضر", False),
        pr("An open garage full of tools", "مرآب مفتوح مليء بالعدد", False),
    ]
    q3 = [
        tf("There are two cups on the hood, not three.", "كوبان على الغطاء، لا ثلاثة.", True),
        tf("The pedestrian sign is a yellow diamond with a walking figure.", "إشارة المشاة معيّن أصفر فيه شخص يمشي.", True),
        tf("The street-name sign is green, and its letters are not needed to see that it is a street sign.", "لافتة اسم الشارع خضراء، وحروفها غير لازمة لمعرفة أنها لافتة شارع.", True),
        tf("The street sign does not clearly read King St.", "لافتة الشارع لا تُقرأ بوضوح King St.", True),
        tf("The woman holds the phone up, near her face.", "المرأة ترفع الهاتف قرب وجهها.", True),
        tf("The man's vest has reflective orange strips.", "سترة الرجل فيها شرائط برتقالية عاكسة.", True),
        tf("The bicycle is blue and is next to the hydrant in the foreground.", "الدراجة زرقاء وبجانب الصنبور في المقدمة.", True),
        tf("The hydrant is in the foreground, closer to the camera than the van is.", "الصنبور في المقدمة، أقرب إلى الكاميرا من الفان.", True),
        tf("The pink hoodie and the brown dog are on the far sidewalk, to the left of the red car.", "القلنسوة الوردية والكلب البني على الرصيف البعيد، يسار السيارة الحمراء.", True),
        tf("The red car is partly in the green crosswalk.", "السيارة الحمراء جزئيًا في ممر المشاة الأخضر.", True),
        tf("The van is a cargo van with side windows, not a pickup.", "الفان فان بضائع بنوافذ جانبية، لا بيك أب.", True),
        tf("The woman is not the person holding the leash.", "المرأة ليست الشخص الذي يمسك المقود.", True),
        tf("No officer in a dark police uniform is directing traffic.", "لا ضابط بزي شرطة داكن ينظم السير.", True),
        tf("The crash vehicles are one red car and one white van.", "مركبتا الحادث سيارة حمراء واحدة وفان أبيض واحد.", True),
        tf("Leaves and houses fill the background under a bright sky.", "أوراق وبيوت تملأ الخلفية تحت سماء مشرقة.", True),
        tf("The street sign clearly reads Kapahulu Ave.", "لافتة الشارع تُقرأ بوضوح Kapahulu Ave.", False),
        tf("The pedestrian figure is on a blue circular sign.", "شخص المشاة على إشارة دائرية زرقاء.", False),
        tf("Three cups are lined up on the van.", "ثلاثة أكواب مصفوفة على الفان.", False),
        tf("The leash is held by the man in the orange vest.", "المقود يمسكه الرجل بالسترة البرتقالية.", False),
        tf("The bicycle is lying in the center of the green crosswalk.", "الدراجة ملقاة في وسط ممر المشاة الأخضر.", False),
        tf("The hydrant is blue.", "الصنبور أزرق.", False),
        tf("The woman's phone is a red handbag.", "هاتف المرأة حقيبة يد حمراء.", False),
        tf("The van's front is crushed and the red car is untouched.", "مقدمة الفان محطمة والسيارة الحمراء سليمة.", False),
        tf("A Quick Stop sign is on the nearest porch.", "لافتة QUICK STOP على أقرب شرفة.", False),
        tf("The mailbox number 7426 is painted on the red car.", "رقم صندوق البريد 7426 مرسوم على السيارة الحمراء.", False),
        tf("The dog is a black dog sitting by an orange cone.", "الكلب كلب أسود جالس بجانب مخروط برتقالي.", False),
        tf("The man wears a red cap and a yellow jacket.", "الرجل يلبس قبعة حمراء وسترة صفراء.", False),
        tf("Four people are standing in the crosswalk.", "أربعة أشخاص واقفون في ممر المشاة.", False),
        tf("The crosswalk bars are red.", "قضبان ممر المشاة حمراء.", False),
        tf("The bicycle is teal and inside a garage.", "الدراجة فيروزية وداخل مرآب.", False),
        pr("A yellow diamond pedestrian sign", "إشارة مشاة معيّن أصفر", True),
        pr("A green street-name sign", "لافتة اسم شارع خضراء", True),
        pr("Reflective strips on a vest", "شرائط عاكسة على سترة", True),
        pr("Exactly two cups on the red hood", "كوبان بالضبط على الغطاء الأحمر", True),
        pr("A brown dog on the far sidewalk", "كلب بني على الرصيف البعيد", True),
        pr("Side windows on the white van", "نوافذ جانبية على الفان الأبيض", True),
        pr("A phone held up", "هاتف مرفوع", True),
        pr("Porch railings", "درابزين شرفات", True),
        pr("A blue bicycle in the foreground", "دراجة زرقاء في المقدمة", True),
        pr("Green crosswalk bars under the red car", "قضبان ممر خضراء تحت السيارة الحمراء", True),
        pr("A readable King St sign", "لافتة King St مقروءة", False),
        pr("An ambulance", "سيارة إسعاف", False),
        pr("A QUICK STOP storefront", "واجهة QUICK STOP", False),
        pr("A black dog by an orange cone", "كلب أسود بجانب مخروط برتقالي", False),
        pr("A red tool chest", "صندوق عدة أحمر", False),
    ]
    title = [
        ["Corner crash · quiz 1 of 3 · broad", "حادث الزاوية · الاختبار 1 من 3 · الصورة الكبيرة"],
        ["Corner crash · quiz 2 of 3 · attributes", "حادث الزاوية · الاختبار 2 من 3 · الصفات"],
        ["Corner crash · quiz 3 of 3 · fine detail", "حادث الزاوية · الاختبار 3 من 3 · التفاصيل الدقيقة"],
    ]
    blurb = [
        ["New picture. People, the two vehicles, and what happened.",
         "صورة جديدة. الأشخاص، والمركبتان، وما حدث."],
        ["Same corner. Clothes, counts, and which person goes with which object.",
         "الزاوية نفسها. الملابس والعدد وأي شخص مع أي غرض."],
        ["Same corner. Signs, small counts, and the look-alike details from the earlier pictures.",
         "الزاوية نفسها. اللافتات والأعداد الصغيرة والتفاصيل التي تشبه الصور السابقة."],
    ]
    out = []
    for band, rows, t, b in zip((1, 2, 3), (q1, q2, q3), title, blurb):
        out.append(quiz(f"corner-{band}", "corner", band, img, alt, t, b, rows))
    return out


def quizzes():
    rows = burglary() + quickstop() + corner()
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate photo quiz id")
    return rows


def check():
    rows = quizzes()
    scenes = []
    for r in rows:
        if r["scene"] not in scenes:
            scenes.append(r["scene"])
        if r["secs"] != 120 or len(r["q"]) != 45:
            raise SystemExit("bad quiz " + r["id"])
    if scenes != ["b7426", "qstop", "corner"]:
        raise SystemExit(scenes)
    return {"quizzes": len(rows), "scenes": scenes, "questions": len(rows) * 45}


if __name__ == "__main__":
    import json
    print(json.dumps(check()))
