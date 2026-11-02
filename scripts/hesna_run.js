/* Browser runner for the study guide. Scoring is from the choice she taps,
   not a self-grade, so a high score really does raise the next tier. */
(function () {
  var A = window.HesnaAdapt;
  var D = window.HS;
  var K = "hesnaAdapt";
  var app, board, state, session, steps, cursor, answers, t0, timer, mode;

  function load() {
    try { state = JSON.parse(localStorage.getItem(K)) || {}; } catch (e) { state = {}; }
    state.seen = state.seen || {};
    state.fam = state.fam || {};
    state.pillar = state.pillar || {};
    state.days = state.days || {};
  }
  function save() {
    try { localStorage.setItem(K, JSON.stringify(state)); } catch (e) {}
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function bi(en, ar) {
    return '<span data-en>' + esc(en) + '</span><span data-ar>' + esc(ar) + '</span>';
  }
  function optLabel(item, i) {
    var o = item.opts[i];
    if (item.pillar === "grammar" || (item.family && D.grammarFamilies && D.grammarFamilies[item.family])) {
      return esc(o[0]);
    }
    return bi(o[0], o[1]);
  }
  function isGrammar(item) {
    return item.pillar === "grammar";
  }
  var FAM_AR = {
    articles: "أدوات التعريف", adjectives: "الصفات", agreement: "مطابقة الفعل والفاعل", tense: "الأزمنة",
    prepositions: "حروف الجر", pronouns: "الضمائر", negatives: "النفي", questions: "الأسئلة",
    count: "المعدود", complements: "المتممات", phrasing: "الصياغة", calques: "النقل الحرفي",
    "ab-agree": "مطابقة الفعل والفاعل", "ab-fragment": "الجملة الناقصة", "ab-homo": "الكلمات المتشابهة", "ab-well": "well و good"
  };
  var FAM_EN = {
    articles: "articles", adjectives: "adjectives", agreement: "subject-verb agreement", tense: "verb tense",
    prepositions: "prepositions", pronouns: "pronouns", negatives: "negatives", questions: "question form",
    count: "count and plurals", complements: "complements", phrasing: "phrasing", calques: "word-for-word transfer",
    "ab-agree": "subject-verb agreement", "ab-fragment": "sentence fragments", "ab-homo": "homophones", "ab-well": "well and good"
  };
  function memArea(en) {
    var s = String(en || "").toLowerCase();
    if (/shirt|pants|hat|hair|jacket|shoe|dress|vest|clothing|wore|wearing|backpack|umbrella|braid/.test(s)) return ["Memory: clothing details", "الذاكرة: تفاصيل الملابس"];
    if (/carried|carrying|phone|cup|bag|box/.test(s)) return ["Memory: what people carried", "الذاكرة: ما يحمله الأشخاص"];
    if (/plate|license|badge|number/.test(s)) return ["Memory: numbers and plates", "الذاكرة: الأرقام واللوحات"];
    if (/time|clock/.test(s)) return ["Memory: the time", "الذاكرة: الوقت"];
    if (/street|sign|cafe|gym/.test(s)) return ["Memory: signs and names", "الذاكرة: اللافتات والأسماء"];
    if (/car|van|truck|sedan|vehicle|bike|bicycle|bus/.test(s)) return ["Memory: vehicles", "الذاكرة: المركبات"];
    if (/color/.test(s)) return ["Memory: colors", "الذاكرة: الألوان"];
    if (/how many|count/.test(s)) return ["Memory: counts", "الذاكرة: الأعداد"];
    return ["Memory: scene details", "الذاكرة: تفاصيل المشهد"];
  }
  function areaOf(item) {
    if (!item) return ["This quiz", "هذا الاختبار"];
    if (item.pillar === "mem") return memArea(item.en);
    if (item.pillar === "written") {
      var wfam = item.family && FAM_EN[item.family];
      if (wfam) return ["Written expression: " + wfam, "التعبير الكتابي: " + (FAM_AR[item.family] || wfam)];
      return ["Written expression", "التعبير الكتابي"];
    }
    if (item.pillar === "grammar") {
      var fam = item.family && FAM_EN[item.family];
      if (fam) return ["Grammar and word usage: " + fam, "القواعد واستخدام الكلمات: " + (FAM_AR[item.family] || fam)];
      return ["Grammar and word usage", "القواعد واستخدام الكلمات"];
    }
    if (item.pillar === "logic") return ["Reasoning and judgment", "الاستدلال والحكم"];
    if (item.pillar === "reading" || item.pillar === "comp") return ["Reading: the passage", "القراءة: المقطع"];
    if (item.pillar === "listen") return ["Listening: radio calls", "الاستماع: النداءات"];
    if (item.pillar === "obs") return ["Observation: the scene", "الملاحظة: المشهد"];
    return ["This quiz", "هذا الاختبار"];
  }
  var PIL_AR = { logic: "المنطق", reading: "القراءة", comp: "الفهم", listen: "الاستماع", obs: "الملاحظة", grammar: "القواعد", written: "الكتابة" };
  var EXAM_NAME = {
    written: ["Written expression", "التعبير الكتابي"],
    grammar: ["Grammar, word usage, and vocabulary", "القواعد واستخدام الكلمات والمفردات"],
    reading: ["Reading with Understanding", "القراءة بفهم"],
    comp: ["Reading comprehension", "فهم المقروء"],
    logic: ["Reasoning and judgment", "الاستدلال والحكم"],
    listen: ["Radio call", "نداء لاسلكي"],
    obs: ["Observation scenario", "سيناريو الملاحظة"]
  };
  var AREA_META = [
    { id: "written", key: "ab", en: "Written Communication", ar: "التواصل الكتابي", note: "Official exam area. A means the sentence is correct. B means it is not.", noteAr: "قسم الامتحان الرسمي. A تعني الجملة صحيحة. B تعني أنها ليست كذلك." },
    { id: "grammar", key: "grammar", en: "Grammar: which sentence is correct", ar: "القواعد: أي جملة صحيحة", note: "Four-choice written practice from the earlier plan.", noteAr: "تدريب كتابي من أربع خيارات من الخطة السابقة." },
    { id: "reading", key: "reading", en: "Reading with Understanding", ar: "القراءة بفهم", note: "Official exam area. The passage stays. Answer only from it.", noteAr: "قسم الامتحان الرسمي. المقطع يبقى. أجيبي منه فقط." },
    { id: "comp", key: "comp", en: "Reading comprehension", ar: "فهم المقروء", note: "More reading practice. The passage stays.", noteAr: "تدريب قراءة إضافي. المقطع يبقى." },
    { id: "logic", key: "logic", en: "Logic", ar: "المنطق", note: "Extra practice kept from the earlier plan.", noteAr: "تدريب إضافي محفوظ من الخطة السابقة." },
    { id: "listen", key: "listen", en: "Radio call", ar: "نداء لاسلكي", note: "Extra practice kept from the earlier plan.", noteAr: "تدريب إضافي محفوظ من الخطة السابقة." },
    { id: "obs", key: "obs", en: "Observation scenario", ar: "سيناريو الملاحظة", note: "Extra practice kept from the earlier plan.", noteAr: "تدريب إضافي محفوظ من الخطة السابقة." }
  ];
  function weekAr(n) {
    return { 1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع" }[n] || String(n);
  }
  function listBi(enList, arMap) {
    var en = enList.join(", ");
    var ar = enList.map(function (x) { return arMap[x] || x; }).join("، ");
    return [en, ar];
  }

  function renderSummary(dayN) {
    var el = document.getElementById("hs-summary");
    if (!el) return;
    var row = state.days && state.days[String(dayN)];
    var list = (row && row.quizzes) || [];
    if (!list.length) { el.innerHTML = ""; return; }
    el.innerHTML = "<h2>" + bi("Today", "هذا اليوم") + "</h2><ul>"
      + list.map(function (q) {
        if (q.key === "bio") return "<li>" + bi(q.label_en, q.label_ar) + "</li>";
        return "<li>" + bi(q.label_en + ": " + q.pct + "% (" + q.ok + "/" + q.n + ")", q.label_ar + ": " + q.pct + "% (" + q.ok + "/" + q.n + ")") + "</li>";
      }).join("") + "</ul>";
  }
  function rememberQuiz(dayN, rec) {
    state.days = state.days || {};
    var row = state.days[String(dayN)] || {};
    var list = (row.quizzes || []).filter(function (q) { return q.key !== rec.key; });
    list.push(rec);
    row.quizzes = list;
    state.days[String(dayN)] = row;
  }
  function collectLines(blocks, ans) {
    var lines = [];
    var i = 0;
    function push(item, given) {
      lines.push({ item: item, given: given, good: given === item.ans });
    }
    (blocks || []).forEach(function (b) {
      if (b.kind === "q") { push(b.item, ans[i]); i += 1; }
      else (b.set.qs || []).forEach(function (q) {
        push(Object.assign({ pillar: b.set.pillar, family: q.family, why: q.why, opts: q.opts, ans: q.ans, en: q.en, ar: q.ar }, q), ans[i]);
        i += 1;
      });
    });
    return lines;
  }
  function resultsPanel(titleEn, titleAr, lines) {
    var ok = lines.filter(function (l) { return l.good; }).length;
    var n = lines.length;
    var pct = n ? Math.round(100 * ok / n) : 0;
    var seen = {};
    var areas = [];
    lines.forEach(function (ln) {
      if (ln.good) return;
      var area = areaOf(ln.item);
      if (seen[area[0]]) return;
      seen[area[0]] = true;
      areas.push(area);
    });
    var study = areas.length
      ? "<ul>" + areas.map(function (a) { return "<li>" + bi(a[0], a[1]) + "</li>"; }).join("") + "</ul>"
      : "<p>" + bi("Nothing to review on this quiz.", "لا شيء للمراجعة في هذا الاختبار.") + "</p>";
    var misses = lines.filter(function (l) { return !l.good; });
    var missHtml = misses.length
      ? '<ol class="md-qs">' + misses.map(function (ln) {
        return '<li class="sp-day md-bad"><p>' + bi(ln.item.en, ln.item.ar) + "</p><p>"
          + bi("Your answer: ", "إجابتك: ") + answerText(ln.item, ln.given) + "</p><p><strong>"
          + bi("Correct: ", "الصحيح: ") + answerText(ln.item, ln.item.ans) + "</strong></p>"
          + whyLine(ln.item) + "</li>";
      }).join("") + "</ol>"
      : "<p>" + bi("No misses.", "لا أخطاء.") + "</p>";
    return {
      pct: pct, ok: ok, n: n,
      html: '<section class="hs-results"><h2>' + bi(titleEn + ": " + ok + "/" + n + " (" + pct + "%)", titleAr + ": " + ok + "/" + n + " (" + pct + "%)") + "</h2>"
        + "<h3>" + bi("Study up on", "ذاكري") + "</h3>" + study
        + "<h3>" + bi("Missed", "ما فات") + "</h3>" + missHtml + "</section>"
    };
  }
  function whyLine(item) {
    var w = item && item.why;
    if (!w || !w[0]) return "";
    return "<p><strong>" + bi("Why: ", "لماذا: ") + "</strong>" + bi(w[0], w[1] || w[0]) + "</p>";
  }
  function answerText(item, idx) {
    if (idx == null || idx < 0 || !item.opts || !item.opts[idx]) return bi("(none)", "(لا شيء)");
    return optLabel(item, idx);
  }

  function bannerText(kind) {
    if (kind === "jump") return bi(
      "The last sitting was too easy. That is the plan falling behind you, so today starts one tier higher.",
      "الجلسة السابقة كانت أسهل مما ينبغي. هذه الخطة تأخّرت عنكِ، فاليوم يبدأ من مستوى أعلى.");
    if (kind === "jump2") return bi(
      "You cleared the raised set too. Today jumps two tiers, not one.",
      "أنجزتِ المجموعة المرفوعة أيضًا. اليوم يقفز مستويين لا مستوى واحدًا.");
    if (kind === "bridge") return bi(
      "The core of the last sitting was under 70%. Today still moves forward, and it opens with a short bridge so the miss does not become a wall.",
      "جوهر الجلسة السابقة كان تحت 70%. اليوم يتقدّم رغم ذلك، ويبدأ بجسر قصير حتى لا يصير التعثّر جدارًا.");
    if (kind === "repair") return bi(
      "Today is only what is still soft. Anything at 95% stays retired.",
      "اليوم لما يزال لينًا فقط. ما بلغ 95% يبقى موقوفًا.");
    if (kind === "stretch") return bi(
      "You are already on the top tier. The stretch bank is the raise: tighter corrections, no victory lap. The score is saved, and every other day stays open.",
      "أنتِ أصلًا في أعلى مستوى. بنك التمدد هو رفع المستوى: تصحيحات أدق، بلا جولة نصر. النتيجة تُحفظ، وكل يوم آخر يبقى مفتوحًا.");
    if (kind === "weekJump") return bi(
      "Week 1 was strong. This week starts one tier higher, and it aims at whatever was still soft.",
      "الأسبوع الأول كان قويًا. هذا الأسبوع يبدأ من مستوى أعلى، ويستهدف ما بقي لينًا.");
    if (kind === "weekJump2") return bi(
      "Week 1 was too easy. This week jumps two tiers, and the weak spots still come first.",
      "الأسبوع الأول كان أسهل مما ينبغي. هذا الأسبوع يقفز مستويين، ومواضع الضعف تبقى أولًا.");
    if (kind === "weekSoft") return bi(
      "Week 1 was mastered, and the core was under 85%. This week is still harder than last week. It opens with a bridge, then the new work.",
      "أُتقن الأسبوع الأول، والجوهر كان تحت 85%. هذا الأسبوع أصعب من السابق رغم ذلك. يبدأ بجسر، ثم العمل الجديد.");
    return "";
  }
  function detailLine() {
    var d = session && session.bannerDetail;
    if (!d) return "";
    var bits = [];
    if (session.week === 2 && d.overall != null) bits.push(bi("Week 1 core " + d.overall + "%.", "جوهر الأسبوع الأول " + d.overall + "%."));
    if (d.fams && d.fams.length) {
      var fam = listBi(d.fams, FAM_AR);
      bits.push(bi("Weak spots: " + fam[0] + ".", "مواضع لينة: " + fam[1] + "."));
    }
    if (d.pillars && d.pillars.length) {
      var pil = listBi(d.pillars, PIL_AR);
      bits.push(bi("Soft skills: " + pil[0] + ".", "مهارات لينة: " + pil[1] + "."));
    }
    return bits.length ? "<p>" + bits.join(" ") + "</p>" : "";
  }
  function nextControls(week, dayN) {
    var next = dayN ? dayN + 1 : week * 7 + 1;
    if (next > 28) return "";
    return '<button type="button" class="sp-btn" data-day="' + next + '">' + bi("Next day", "اليوم التالي") + "</button>";
  }

  function flatten(blocks) {
    var steps = [];
    blocks.forEach(function (b) {
      if (b.kind === "listen" || b.kind === "obs") steps.push({ type: "script", set: b.set, kind: b.kind });
      if (b.kind === "read" || b.kind === "comp") steps.push({ type: "passage", set: b.set, kind: b.kind });
      if (b.kind === "q") steps.push({ type: "q", item: b.item, passage: null });
      else if (b.set) b.set.qs.forEach(function (q) {
        steps.push({
          type: "q",
          item: Object.assign({ pillar: b.set.pillar, tier: b.set.tier }, q),
          passage: (b.kind === "read" || b.kind === "comp") ? b.set : null
        });
      });
    });
    return steps;
  }

  function clock() {
    if (!t0) return;
    var el = document.getElementById("hs-clock");
    if (!el) return;
    var s = Math.floor((Date.now() - t0) / 1000);
    el.textContent = Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
  }

  function showIntro(day) {
    clearInterval(timer);
    var b = bannerText(session.banner);
    var memNote = bi(
      "This day already started with its picture: 2 minutes, then it hid, then questions about what it shows. These next questions are the other exam sections. You can open any other day from the plan.",
      "هذا اليوم بدأ أصلًا بصورته: دقيقتان، ثم اختفت، ثم أسئلة عما تُظهره. الأسئلة التالية هي أقسام الامتحان الأخرى. يمكنك فتح أي يوم آخر من الخطة.");
    var period = day.n ? ((day.n - 1) % 7) + 1 : 0;
    var where = (session.kind === "repair" || session.kind === "stretch" || session.kind === "extra")
      ? bi("Week " + session.week + " pack", "حزمة الأسبوع " + weekAr(session.week))
      : bi("Week " + session.week + " pack · period " + period + " of 7", "حزمة الأسبوع " + weekAr(session.week) + " · الفترة " + period + " من 7");
    var lesson = (day.body_en && day.body_ar) ? "<p>" + bi(day.body_en, day.body_ar) + "</p>" : "";
    app.innerHTML = '<p class="sp-ph">' + where + '</p><h2>' + bi(day.title_en, day.title_ar) + '</h2>'
      + (b ? '<p class="hs-banner">' + b + '</p>' : '')
      + detailLine()
      + lesson
      + '<p>' + bi("Tier " + session.tier + " · " + session.nQ + " questions · budget " + day.budgetMin + " min. 80% on the core is the mastery mark. Too easy: core 95%+, or core 90%+ in under " + day.tooFastMin + " min, and then the harder set is the one the scoreboard counts. You can open any other day. Grammar misses do not freeze the tier. Grammar mastery does not get more drills.",
        "المستوى " + session.tier + " · " + session.nQ + " سؤالًا · الميزانية " + day.budgetMin + " د. 80% في الجوهر علامة الإتقان. أسهل مما ينبغي: جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في أقل من " + day.tooFastMin + " د، وعندها المجموعة الأصعب هي التي تحسبها لوحة النتائج. يمكنك فتح أي يوم آخر. أخطاء القواعد لا تجمّد المستوى. وإتقان القواعد لا يجلب تمارين إضافية.") + '</p>'
      + '<p>' + memNote + '</p>'
      + (session.week > 1 && !(state.day1 && state.day1.fam) ? '<p class="hs-banner">' + bi("Week 1 has not been scored in this browser. The grammar baseline is not in yet, so this pack cannot aim extra drills at your weak families.", "الأسبوع الأول لم يُسجَّل في هذا المتصفح. خط أساس القواعد غير موجود بعد، فلا تستطيع هذه الحزمة توجيه تمارين إضافية إلى عائلاتكِ الضعيفة.") + '</p>' : '')
      + '<button type="button" class="sp-btn" id="hs-begin">' + (session.kind === "extra"
        ? bi("Begin the harder set", "ابدئي المجموعة الأصعب")
        : bi("Begin this period", "ابدئي هذه الفترة")) + '</button>';
    document.getElementById("hs-begin").onclick = function () {
      t0 = Date.now();
      cursor = 0;
      answers = [];
      mode = "main";
      timer = setInterval(clock, 500);
      renderStep();
    };
  }

  function renderStep() {
    var step = steps[cursor];
    if (!step) { finishMain(); return; }
    if (step.type === "script") return renderScript(step);
    if (step.type === "passage") { cursor += 1; return renderStep(); }
    renderQ(step);
  }

  function renderScript(step) {
    var left = step.set.secs || 40;
    var body, note;
    if (step.set.mem && typeof hesnaScene === "function") {
      body = hesnaScene(step.set);
      note = bi("Recall of Visual Details. Two minutes. No notes.", "استرجاع التفاصيل البصرية. دقيقتان. بلا ملاحظات.");
    } else if (step.set.img) {
      body = '<figure class="hs-script"><img src="' + esc(step.set.img) + '" alt="' + esc(step.set.alt || "Practice scene") + '" style="width:100%;height:auto;border-radius:12px"><figcaption class="si-credit">'
        + bi("Created by SI and Biological SI Partner", "أُنشئ بواسطة SI وBiological SI Partner") + '</figcaption></figure><p>'
        + bi(step.set.en, step.set.ar) + '</p>';
      note = bi("Observation. Study this picture. It will hide. Every question is about this picture only.",
        "ملاحظة. ادراسي هذه الصورة. ستختفي. كل سؤال عن هذه الصورة فقط.");
    } else {
      body = '<p class="hs-script">' + esc(step.set.en) + '</p>';
      note = bi(step.kind === "obs" ? "Observation. Read once. It will hide." : "Radio call. Read once. It will hide.",
        step.kind === "obs" ? "ملاحظة. اقرئي مرة واحدة. سيختفي." : "نداء لاسلكي. اقرئي مرة واحدة. سيختفي.");
    }
    app.innerHTML = '<p class="md-timer" id="hs-script-t"></p>' + body
      + (note ? '<p class="sp-ph">' + note + '</p>' : '')
      + '<p id="hs-clock"></p>'
      + '<button type="button" class="sp-btn" id="hs-ready">' + bi("I'm ready, hide it", "أنا جاهزة، أخفيه") + '</button>';
    var el = document.getElementById("hs-script-t");
    function tick() {
      var show = Math.max(left, 0);
      var mm = Math.floor(show / 60);
      var ss = ("0" + (show % 60)).slice(-2);
      el.innerHTML = bi("Time left: ", "الوقت المتبقي: ") + mm + ":" + ss;
      if (left-- <= 0) { clearInterval(scriptTimer); cursor += 1; renderStep(); }
    }
    tick();
    var scriptTimer = setInterval(tick, 1000);
    document.getElementById("hs-ready").onclick = function () {
      clearInterval(scriptTimer);
      cursor += 1;
      renderStep();
    };
  }

  function renderQ(step) {
    var item = step.item;
    var nQ = steps.filter(function (s) { return s.type === "q"; }).length;
    var sofar = answers.length + 1;
    var passage = "";
    if (step.passage) {
      var stay = step.passage.pillar === "reading" || step.passage.pillar === "comp";
      passage = (stay
        ? '<p class="sp-ph">' + bi("Reading with Understanding. The passage stays. This is not a memory test. Answer only from it.", "القراءة بفهم. المقطع يبقى. هذا ليس اختبار ذاكرة. أجيبي منه فقط.") + '</p>'
        : '')
        + '<div class="hs-passage"><p>' + esc(step.passage.en) + '</p><p class="sp-ph">' + esc(step.passage.ar) + '</p></div>';
    }
    var visKey = "";
    if (item.pillar === "mem" && item.opts && item.opts[0]) {
      var head = String(item.opts[0][0] || "");
      visKey = head.indexOf("Yes") >= 0
        ? '<p class="hs-key">' + bi("Recall of Visual Details. A = yes, it was in the picture. B = no. If only part was shown, it was present.", "استرجاع التفاصيل البصرية. A = نعم كان في الصورة. B = لا. إذا ظهر جزء منه فهو موجود.") + '</p>'
        : '<p class="hs-key">' + bi("Recall of Visual Details. A = the statement is true. B = the statement is false.", "استرجاع التفاصيل البصرية. A = العبارة صحيحة. B = العبارة خطأ.") + '</p>';
    }
    var writtenKey = item.pillar === "written"
      ? '<p class="hs-key">' + bi("Written expression. A = grammatically correct. B = grammatically incorrect. Spelling, punctuation, and capitalization are not scored. A wrong homophone still counts.", "التعبير الكتابي. A = صحيحة نحويًا. B = غير صحيحة نحويًا. الإملاء وعلامات الترقيم وحالة الحرف لا تُحسب. والكلمة المتشابهة إذا غُلِط فيها تُحسب.") + '</p>'
      : (item.pillar === "grammar"
        ? '<p class="hs-key">' + bi("Grammar, word usage, and vocabulary. Pick the sentence that is correct. On the exam, spelling, punctuation, and capitalization are not scored. A wrong homophone still counts.", "القواعد واستخدام الكلمات والمفردات. اختاري الجملة الصحيحة. في الامتحان، الإملاء وعلامات الترقيم وحالة الحرف لا تُحسب. والكلمة المتشابهة إذا غُلِط فيها تُحسب.") + '</p>'
        : (item.pillar === "logic"
          ? '<p class="hs-key">' + bi("Reasoning and judgment. Use only what the question states.", "الاستدلال والحكم. استخدمي ما يقوله السؤال فقط.") + '</p>'
          : ''));
    var opts = "";
    item.opts.forEach(function (o, i) {
      opts += '<button type="button" class="hs-opt" data-i="' + i + '">' + optLabel(item, i) + '</button>';
    });
    app.innerHTML = '<p class="sp-ph">' + bi("Question " + sofar + " of " + nQ, "السؤال " + sofar + " من " + nQ) + ' · <span id="hs-clock"></span></p>'
      + passage
      + visKey
      + writtenKey
      + '<p class="hs-stem">' + (isGrammar(item) ? bi(item.en, item.ar) : bi(item.en, item.ar)) + '</p>'
      + opts;
    app.querySelectorAll(".hs-opt").forEach(function (btn) {
      btn.onclick = function () {
        answers.push(+btn.getAttribute("data-i"));
        cursor += 1;
        renderStep();
      };
    });
    window.scrollTo(0, 0);
  }

  function coreOf(blocks, ans) {
    var g = A.grade(blocks, ans);
    return g;
  }

  function finishMain() {
    if (session && session.kind === "mem") return finishMem();
    clearInterval(timer);
    var sec = Math.round((Date.now() - t0) / 1000);
    if (mode === "extra") return finishExtra(A.grade(session.extraBlocks, answers));
    var g = A.grade(session.blocks, answers);
    var row = null;
    if (session.kind === "repair" || session.kind === "stretch") A.applyPackGrade(state, session.week, session.kind, session.blocks, g);
    else row = A.applyGrade(state, session.day, session, g, sec);
    var lines = collectLines(session.blocks, answers);
    var examName = EXAM_NAME[session.exam] || ["Written Communication", "التواصل الكتابي"];
    var panel = resultsPanel(examName[0], examName[1], lines);
    rememberQuiz(session.day.n, {
      key: session.exam || "written",
      label_en: examName[0],
      label_ar: examName[1],
      pct: panel.pct, ok: panel.ok, n: panel.n
    });
    save();
    if (!row) row = { tooFastSec: session.tooFastSec, sec: sec };
    var raised = session.kind !== "repair" && session.kind !== "stretch" && A.hot(row);
    var html = panel.html;
    if (session.day) html += nextQuizButton(session.day, (session.quizIndex || 0) + 1);
    app.innerHTML = html;
    renderSummary(session.day.n);
    window.scrollTo(0, 0);
  }

  function startExtra() {
    var row = state.days[String(session.day.n)] || {};
    var tier = A.extraTier(session);
    if (row.probeN >= 3 && row.probePct >= 75) tier = Math.min(6, Math.max(tier, 3));
    var items = (D.items || []).filter(function (it) {
      var seen = state.seen[it.id];
      return it.pillar === "logic" && !it.probe && it.tier >= tier && (!seen || !seen.ok);
    }).slice(0, 8);
    if (!items.length) {
      A.noteExtra(state, session.day.n, 80);
      save();
      renderSummary(session.day.n);
      return;
    }
    session.extraBlocks = items.map(function (it) { return { kind: "q", item: it }; });
    steps = flatten(session.extraBlocks);
    cursor = 0;
    answers = [];
    mode = "extra";
    t0 = Date.now();
    timer = setInterval(clock, 500);
    renderStep();
  }

  function finishExtra(g) {
    clearInterval(timer);
    A.absorb(state, session.extraBlocks, g.answers, session.day.n);
    var pct = g.corePct == null ? g.pct : g.corePct;
    A.noteExtra(state, session.day.n, pct);
    var lines = collectLines(session.extraBlocks, g.answers);
    var panel = resultsPanel("Harder set", "المجموعة الأصعب", lines);
    rememberQuiz(session.day.n, {
      key: "extra",
      label_en: "Harder set",
      label_ar: "المجموعة الأصعب",
      pct: panel.pct, ok: panel.ok, n: panel.n
    });
    save();
    app.innerHTML = panel.html + nextControls(session.week, session.day && session.day.n);
    renderSummary(session.day.n);
    window.scrollTo(0, 0);
  }

  function review(blocks, ans) {
    var html = '<ol class="md-qs">';
    var i = 0;
    function line(item, given) {
      var good = given === item.ans;
      html += '<li class="sp-day ' + (good ? "md-ok" : "md-bad") + '"><p>' + bi(item.en, item.ar) + '</p><p>'
        + (good ? "✅ " : "❌ ") + bi("Your answer: ", "إجابتك: ") + optLabel(item, given < 0 ? 0 : given) + '</p>'
        + (good ? '' : '<p><strong>' + bi("Correct: ", "الصحيح: ") + optLabel(item, item.ans) + '</strong></p><p>' + bi(item.why[0], item.why[1]) + '</p>')
        + '</li>';
    }
    blocks.forEach(function (b) {
      if (b.kind === "q") { line(b.item, ans[i]); i += 1; }
      else b.set.qs.forEach(function (q) {
        line(Object.assign({ pillar: b.set.pillar, why: q.why, opts: q.opts, ans: q.ans, en: q.en, ar: q.ar }, q), ans[i]);
        i += 1;
      });
    });
    return html + '</ol>';
  }

  function refreshPackNotes() {
    [1, 2, 3, 4].forEach(function (w) {
      var note = document.getElementById("hs-pack-note-" + w);
      var btn = document.getElementById("hs-pack-btn-" + w);
      if (!note && !btn) return;
      var st = A.packStatus(state, w);
      var p = st.perf;
      var core = p.overall == null ? "—" : p.overall + "%";
      var en = "Open. " + p.masteredN + " of " + p.total + " days at the mastery mark · core " + core + ".";
      var ar = "مفتوح. " + p.masteredN + " من " + p.total + " أيام عند علامة الإتقان · الجوهر " + core + ".";
      if (note) note.innerHTML = bi(en, ar);
      if (btn) {
        btn.innerHTML = bi("Open Week " + w, "افتحي الأسبوع " + weekAr(w));
        btn.removeAttribute("disabled");
      }
    });
  }

  function beginMemory(step) {
    var drill = step.memory;
    var qs = (drill.qs || []).map(function (q) {
      return { en: q.en, ar: q.ar, opts: q.opts, ans: q.ans, why: q.why || ["It is in the picture.", "هذا في الصورة."], pillar: "mem" };
    });
    var set = {
      mem: 1,
      id: drill.id,
      pillar: "mem",
      secs: drill.secs || 120,
      img: drill.img,
      alt: drill.alt,
      overlay: drill.overlay,
      svg: drill.svg,
      tm: drill.tm,
      st: drill.st,
      cr: drill.cr,
      b: drill.b,
      p: drill.p,
      v: drill.v,
      en: drill.title_en,
      ar: drill.title_ar,
      qs: qs
    };
    session = {
      kind: "mem",
      week: step.week,
      day: step.day,
      memId: drill.id,
      memIndex: step.memIndex || 0,
      blocks: [{ kind: "obs", set: set }],
      tier: step.day.tier || 1,
      tooFastSec: (step.day.tooFastMin || 20) * 60,
      nQ: qs.length,
      banner: null
    };
    steps = flatten(session.blocks);
    cursor = 0;
    answers = [];
    mode = "mem";
    t0 = Date.now();
    clearInterval(timer);
    renderStep();
  }
  function finishMem() {
    clearInterval(timer);
    var qs = session.blocks[0].set.qs;
    var ok = 0;
    qs.forEach(function (q, i) { if (answers[i] === q.ans) ok += 1; });
    var pct = qs.length ? Math.round(100 * ok / qs.length) : 0;
    A.noteMem(state, session.day, session.memId, pct);
    var lines = qs.map(function (q, i) {
      return { item: q, given: answers[i], good: answers[i] === q.ans };
    });
    var title = (session.blocks[0].set.en || "Picture");
    var panel = resultsPanel("Recall of Visual Details", "استرجاع التفاصيل البصرية", lines);
    rememberQuiz(session.day.n, {
      key: "mem:" + session.memId,
      label_en: title,
      label_ar: session.blocks[0].set.ar || title,
      pct: panel.pct, ok: panel.ok, n: panel.n
    });
    save();
    var idx = (session.memIndex || 0) + 1;
    var ids = (session.day && session.day.mem) || [];
    var go = nextAfterMemory(session.day, idx);
    go += '<button type="button" class="sp-btn" data-day="' + session.day.n + '" data-mem="' + (session.memIndex || 0) + '">' + bi("Retry", "أعيدي") + "</button>";
    app.innerHTML = panel.html + go;
    renderSummary(session.day.n);
    window.scrollTo(0, 0);
  }
  function startReading(day) {
    var built = A.planSession(day, D, state, "reading");
    built.kind = "period";
    built.week = A.weekOf(day.n);
    session = built;
    session.day = day;
    session.exam = "reading";
    if (!session.nQ) {
      if (day.bio) startBio(day);
      return;
    }
    steps = flatten(session.blocks);
    t0 = Date.now();
    cursor = 0;
    answers = [];
    mode = "main";
    clearInterval(timer);
    timer = setInterval(clock, 500);
    renderStep();
    window.scrollTo(0, 0);
  }
  function startBio(day) {
    var items = (D.bio || []).slice(day.bioStart || 0, (day.bioStart || 0) + (day.bio || 0));
    var i = 0;
    var picks = [];
    function show() {
      if (i >= items.length) {
        rememberQuiz(day.n, {
          key: "bio",
          label_en: "Biodata: " + picks.length + " answered, not scored",
          label_ar: "البيانات الشخصية: " + picks.length + " إجابة، بلا درجة"
        });
        save();
        app.innerHTML = "<p>" + bi("Biodata saved. One choice each. Not scored right or wrong.", "حُفظت البيانات الشخصية. خيار واحد لكل سؤال. بلا صح أو خطأ.") + "</p>"
          + '<p>' + bi("Day " + day.n + " is complete. The other days stay open.", "اكتمل اليوم " + day.n + ". الأيام الأخرى تبقى مفتوحة.") + "</p>"
          + nextControls(A.weekOf(day.n), day.n);
        renderSummary(day.n);
        window.scrollTo(0, 0);
        return;
      }
      var q = items[i];
      var opts = "";
      (q.opts || []).forEach(function (o, k) {
        opts += '<button type="button" class="hs-opt" data-i="' + k + '">' + bi(o[0], o[1]) + "</button>";
      });
      app.innerHTML = '<p class="hs-key">' + bi("Biodata. Not right or wrong. Mark one choice, the closest honest fit. A blank gets no credit. Two marks get no credit.", "البيانات الشخصية. ليست صحًا أو خطأ. علّمي خيارًا واحدًا، الأقرب الصادق. الفراغ بلا رصيد. والعلامتان بلا رصيد.") + "</p>"
        + "<p class=\"sp-ph\">" + bi("Question " + (i + 1) + " of " + items.length, "السؤال " + (i + 1) + " من " + items.length) + "</p>"
        + "<p class=\"hs-stem\">" + bi(q.en, q.ar) + "</p>" + opts;
      app.querySelectorAll(".hs-opt").forEach(function (btn) {
        btn.onclick = function () {
          picks.push(+btn.getAttribute("data-i"));
          i += 1;
          show();
        };
      });
      window.scrollTo(0, 0);
    }
    show();
  }
  function findDay(n) {
    var day = null;
    (D.days || []).forEach(function (d) { if (d.n === n) day = d; });
    return day;
  }
  function byId(list) {
    var map = {};
    (list || []).forEach(function (row) { map[row.id] = row; });
    return map;
  }
  function blocksFor(area, ids) {
    if (area === "written" || area === "grammar" || area === "logic") {
      var items = byId(D.items);
      return ids.map(function (id) { return items[id] ? { kind: "q", item: items[id] } : null; }).filter(Boolean);
    }
    var src = area === "reading" ? D.reads : area === "comp" ? D.comps : area === "listen" ? D.listens : D.obs;
    var sets = byId(src);
    var kind = area === "reading" ? "read" : area === "comp" ? "comp" : area;
    return ids.map(function (id) { return sets[id] ? { kind: kind, set: sets[id] } : null; }).filter(Boolean);
  }
  function nextQuizButton(day, qi) {
    var after = day.after || [];
    if (qi < after.length) {
      var step = after[qi];
      return '<button type="button" class="sp-btn" data-day="' + day.n + '" data-quiz="' + qi + '" data-phase="quiz">'
        + bi("Next: " + step.en, "التالي: " + step.ar) + "</button>";
    }
    if (day.bio) {
      return '<button type="button" class="sp-btn" data-day="' + day.n + '" data-area="bio">'
        + bi("Next: Biodata", "التالي: البيانات الشخصية") + "</button>";
    }
    return '<p>' + bi("Day " + day.n + " is complete. The other days stay open.", "اكتمل اليوم " + day.n + ". الأيام الأخرى تبقى مفتوحة.") + "</p>"
      + nextControls(A.weekOf(day.n), day.n);
  }
  function nextAfterMemory(day, memIndex) {
    var ids = day.mem || [];
    if (memIndex < ids.length) {
      return '<button type="button" class="sp-btn" data-day="' + day.n + '" data-mem="' + memIndex + '" data-phase="mem">'
        + bi("Next: memory test " + (memIndex + 1) + " of " + ids.length, "التالي: اختبار الذاكرة " + (memIndex + 1) + " من " + ids.length)
        + "</button>";
    }
    return nextQuizButton(day, 0);
  }
  function startQuiz(n, qi) {
    load();
    var day = findDay(n);
    if (!day) return;
    var step = (day.after || [])[qi];
    if (!step) {
      if (day.bio) startBio(day);
      else {
        app.innerHTML = '<p>' + bi("Day " + day.n + " is complete. The other days stay open.", "اكتمل اليوم " + day.n + ". الأيام الأخرى تبقى مفتوحة.") + "</p>"
          + nextControls(A.weekOf(day.n), day.n);
      }
      return;
    }
    var blocks = blocksFor(step.area, step.ids || []);
    if (!blocks.length) { startQuiz(n, qi + 1); return; }
    session = {
      kind: "period",
      week: A.weekOf(day.n),
      day: day,
      exam: step.area,
      quizIndex: qi,
      blocks: blocks,
      tier: day.tier || 1,
      tooFastSec: (day.tooFastMin || 20) * 60,
      nQ: A.countQ(blocks),
      banner: null
    };
    steps = flatten(blocks);
    t0 = Date.now();
    cursor = 0;
    answers = [];
    mode = "main";
    clearInterval(timer);
    timer = setInterval(clock, 500);
    renderStep();
    window.scrollTo(0, 0);
  }
  function startDay(n, memIndex, phase) {
    load();
    var day = findDay(n);
    if (!day) {
      app.innerHTML = '<p>' + bi("That day is not on this page.", "هذا اليوم ليس في هذه الصفحة.") + '</p>';
      window.scrollTo(0, 0);
      return;
    }
    var sel = document.getElementById("hs-day");
    if (sel) sel.value = String(day.n);
    renderSummary(day.n);
    var ids = day.mem || [];
    var i = memIndex || 0;
    if (i < ids.length && D.mem && D.mem[ids[i]]) {
      beginMemory({ memory: D.mem[ids[i]], day: day, week: A.weekOf(day.n), memIndex: i });
      window.scrollTo(0, 0);
      return;
    }
    startQuiz(day.n, 0);
  }

  function paintDays() {
    var lang = document.documentElement.lang === "ar" ? "ar" : "en";
    document.querySelectorAll("#hs-day option").forEach(function (o) {
      o.textContent = o.getAttribute(lang === "ar" ? "data-ar" : "data-en") || o.value;
    });
  }
  function boot() {
    app = document.getElementById("hs-app");
    board = document.getElementById("hs-board");
    if (!app || !D) return;
    load();
    if (A.resync) A.resync(state, D);
    save();
    paintDays();
    var jump = (location.hash || "").match(/^#(?:day-(\d+)|week-(\d+))/);
    var openDay = 1;
    if (jump && jump[1]) openDay = +jump[1];
    else if (jump && jump[2]) openDay = (+jump[2] - 1) * 7 + 1;
    var sel = document.getElementById("hs-day");
    if (sel) sel.addEventListener("change", function () { startDay(+sel.value, 0, "mem"); });
    var toggle = document.getElementById("sp-toggle");
    if (toggle) toggle.addEventListener("click", function () { setTimeout(paintDays, 0); });
    startDay(openDay, 0, "mem");
    document.body.addEventListener("click", function (e) {
      var b = e.target.closest("[data-day],[data-week],[data-area]");
      if (!b) return;
      if (b.getAttribute("data-phase") === "quiz") {
        startQuiz(+b.getAttribute("data-day"), +(b.getAttribute("data-quiz") || 0));
        return;
      }
      if (b.getAttribute("data-area") === "bio") {
        var bioDay = findDay(+b.getAttribute("data-day"));
        if (bioDay) startBio(bioDay);
        return;
      }
      if (b.hasAttribute("data-day")) {
        startDay(+b.getAttribute("data-day"), +(b.getAttribute("data-mem") || 0), "mem");
        return;
      }
      startDay((+b.getAttribute("data-week") - 1) * 7 + 1, 0, "mem");
    });
    var reset = document.getElementById("hs-reset");
    if (reset) reset.onclick = function () {
      if (!confirm(document.documentElement.lang === "ar"
        ? "مسح تقدّم الخطة في هذا المتصفح؟"
        : "Clear this plan's saved progress in this browser?")) return;
      state = { seen: {}, fam: {}, pillar: {}, days: {}, weeks: {} };
      save();
      renderSummary(1);
      startDay(1, 0, "mem");
    };
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
