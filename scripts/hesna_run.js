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
    articles: "أدوات التعريف", adjectives: "الصفات", agreement: "المطابقة", tense: "الأزمنة",
    prepositions: "حروف الجر", pronouns: "الضمائر", negatives: "النفي", questions: "الأسئلة",
    count: "المعدود", complements: "المتممات", phrasing: "الصياغة", calques: "النقل الحرفي",
    "ab-agree": "المطابقة في الجملة", "ab-fragment": "الجملة الناقصة", "ab-homo": "الكلمات المتشابهة", "ab-well": "well و good"
  };
  var PIL_AR = { logic: "المنطق", reading: "القراءة", comp: "الفهم", listen: "الاستماع", obs: "الملاحظة", grammar: "القواعد", written: "الكتابة" };
  function weekAr(n) {
    return { 1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع" }[n] || String(n);
  }
  function listBi(enList, arMap) {
    var en = enList.join(", ");
    var ar = enList.map(function (x) { return arMap[x] || x; }).join("، ");
    return [en, ar];
  }

  function renderBoard() {
    if (!board) return;
    var d1 = state.day1;
    var days = state.days || {};
    var nums = Object.keys(days).map(Number).filter(function (n) { return days[n] && days[n].pct != null; });
    var lastN = nums.length ? Math.max.apply(null, nums) : 0;
    var last = lastN ? days[String(lastN)] : null;
    var famRows = "";
    var fams = {};
    if (d1 && d1.fam) Object.keys(d1.fam).forEach(function (f) { fams[f] = true; });
    Object.keys(state.fam || {}).forEach(function (f) { fams[f] = true; });
    Object.keys(fams).sort().forEach(function (f) {
      var a = d1 && d1.fam && d1.fam[f];
      var b = state.fam[f];
      var ap = a && a.n ? Math.round(100 * a.ok / a.n) : null;
      var bp = b && b.n ? Math.round(100 * b.ok / b.n) : null;
      var retired = A.mastered(state, f);
      famRows += '<tr><td>' + esc(f) + '</td><td>' + (ap == null ? "—" : ap + "%") + '</td><td>' + (bp == null ? "—" : bp + "%") + '</td><td>' + (retired ? bi("retired", "أُوقف") : bi("in play", "ما زال")) + '</td></tr>';
    });
    var pillar = "";
    ["logic", "grammar", "written", "reading", "comp", "listen", "obs"].forEach(function (p) {
      var r = state.pillar[p];
      if (!r || !r.n) return;
      pillar += '<li>' + esc(p) + ': ' + Math.round(100 * r.ok / r.n) + '% (' + r.ok + '/' + r.n + ')</li>';
    });
    var weeks = "";
    [1, 2, 3, 4].forEach(function (w) {
      var st = A.packStatus(state, w);
      var p = st.perf;
      var statusEn, statusAr;
      if (st.cleared) { statusEn = "mastery mark reached"; statusAr = "بُلغت علامة الإتقان"; }
      else if (st.needsRepair) { statusEn = p.masteredN + "/" + p.total + " at the mastery mark · weak spots still on the board"; statusAr = p.masteredN + "/" + p.total + " عند علامة الإتقان · مواضع لينة ما زالت على اللوحة"; }
      else if (st.needsStretch) { statusEn = p.masteredN + "/" + p.total + " at the mastery mark · stretch still on the board"; statusAr = p.masteredN + "/" + p.total + " عند علامة الإتقان · التمدد ما زال على اللوحة"; }
      else { statusEn = p.masteredN + "/" + p.total + " at the mastery mark"; statusAr = p.masteredN + "/" + p.total + " عند علامة الإتقان"; }
      var core = p.overall == null ? "—" : p.overall + "%";
      weeks += "<li>" + bi("Week " + w + ": " + statusEn + " · core " + core + " · open", "الأسبوع " + weekAr(w) + ": " + statusAr + " · الجوهر " + core + " · مفتوح") + "</li>";
    });
    board.innerHTML = '<h2>' + bi("Scoreboard", "لوحة النتائج") + '</h2>'
      + '<p>' + bi("Scores are saved. 80% on the core is the mastery mark. At 95% the harder set is the one the board counts. Every week and every day can be opened. Day 1 still starts with the photograph. A family at 95% over 4 or more items is retired.",
        "النتائج تُحفظ. 80% في الجوهر علامة الإتقان. عند 95% المجموعة الأصعب هي التي تحسبها اللوحة. كل أسبوع وكل يوم يمكن فتحه. اليوم 1 ما زال يبدأ بالصورة. العائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف.") + '</p>'
      + "<ul>" + weeks + "</ul>"
      + (last ? '<p>' + bi("Latest sitting: period " + lastN + " · " + last.pct + "% overall · core " + (last.corePct == null ? "—" : last.corePct + "%") + " · tier " + last.tier + " · " + Math.round((last.sec || 0) / 60) + " min.",
        "آخر جلسة: الفترة " + lastN + " · " + last.pct + "% إجمالًا · الجوهر " + (last.corePct == null ? "—" : last.corePct + "%") + " · المستوى " + last.tier + " · " + Math.round((last.sec || 0) / 60) + " د.") + '</p>'
        : '<p class="sp-ph">' + bi("No sitting has been scored in this browser yet.", "لا جلسة مسجّلة في هذا المتصفح بعد.") + '</p>')
      + (famRows ? '<table class="hs-board-table"><thead><tr><th>' + bi("Grammar family", "عائلة القواعد") + '</th><th>' + bi("Day 1", "اليوم 1") + '</th><th>' + bi("Now", "الآن") + '</th><th></th></tr></thead><tbody>' + famRows + '</tbody></table>' : '')
      + (pillar ? '<ul>' + pillar + '</ul>' : '');
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
    var html = '<p class="sp-ph">' + bi("Every week and every day stays open. The score is saved either way.", "كل أسبوع وكل يوم يبقى مفتوحًا. النتيجة تُحفظ في الحالين.") + '</p>';
    if (next <= 28) html += '<button type="button" class="sp-btn" data-day="' + next + '">' + bi("Open day " + next, "افتحي اليوم " + next) + "</button>";
    return html;
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
      body = hesnaScene(step.set) + '<p>' + bi(step.set.en, step.set.ar) + '</p>';
      note = bi("No notes. When the time ends, the picture hides and it does not come back until you submit. Every question is answered by what the picture shows.",
        "بلا ملاحظات. حين ينتهي الوقت تختفي الصورة ولا تعود حتى تُرسلي الإجابات. كل سؤال يُجاب مما تُظهره الصورة.");
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
      + '<p class="sp-ph">' + note + '</p>'
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
        ? '<p class="sp-ph">' + bi("The passage stays on screen. This is not a memory test. Answer only from the passage.", "المقطع يبقى على الشاشة. هذا ليس اختبار ذاكرة. أجيبي من المقطع فقط.") + '</p>'
        : '')
        + '<div class="hs-passage"><p>' + esc(step.passage.en) + '</p><p class="sp-ph">' + esc(step.passage.ar) + '</p></div>';
    }
    var writtenKey = item.pillar === "written"
      ? '<p class="hs-key">' + bi("A = grammatically correct. B = grammatically incorrect. Judge sentence structure, grammar, and word usage. Ignore spelling, punctuation, and capitalization. A wrong homophone is still a word-usage error.", "A = صحيحة نحويًا. B = غير صحيحة نحويًا. احكمي على بناء الجملة والقواعد واستعمال الكلمة. تجاهلي الإملاء وعلامات الترقيم وحالة الحرف. والكلمة المتشابهة اللفظ إذا استُعملت غلطًا تبقى خطأ استعمال.") + '</p>'
      : '';
    var opts = "";
    item.opts.forEach(function (o, i) {
      opts += '<button type="button" class="hs-opt" data-i="' + i + '">' + optLabel(item, i) + '</button>';
    });
    app.innerHTML = '<p class="sp-ph">' + bi("Question " + sofar + " of " + nQ, "السؤال " + sofar + " من " + nQ) + ' · <span id="hs-clock"></span></p>'
      + passage
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
    save();
    if (!row) row = { tooFastSec: session.tooFastSec, sec: sec };
    var fast = row.tooFastSec && sec < row.tooFastSec;
    var raised = session.kind !== "repair" && session.kind !== "stretch" && A.hot(row);
    var periodN = session.day && session.day.n ? ((session.day.n - 1) % 7) + 1 : 0;
    var headEn = "Week " + session.week + " · period " + periodN + ": " + g.pct + "%";
    var headAr = "الأسبوع " + weekAr(session.week) + " · الفترة " + periodN + ": " + g.pct + "%";
    if (session.kind === "repair") { headEn = "Weak spots: " + g.pct + "%"; headAr = "المواضع اللينة: " + g.pct + "%"; }
    if (session.kind === "stretch") { headEn = "Stretch: " + g.pct + "%"; headAr = "التمدد: " + g.pct + "%"; }
    var html = '<h2>' + bi(headEn, headAr) + '</h2>'
      + '<p>' + bi("Core (reading, listening, comprehension, observation, and the extra logic drills): " + (g.corePct == null ? "—" : g.corePct + "%") + ". Written A/B and the four-choice grammar are tracked by family and do not hold the tier. Biodata, on the plan page, is not right-or-wrong.",
        "الجوهر (قراءة، استماع، فهم، ملاحظة، وتدريبات المنطق الإضافية): " + (g.corePct == null ? "—" : g.corePct + "%") + ". الكتابة A/B وقواعد الاختيار من أربع تُتابَع حسب العائلة ولا تحبس المستوى. والبيانات الشخصية في صفحة الخطة ليست صح أو خطأ.") + '</p>'
      + '<p>' + bi(Math.round(sec / 60) + " min " + (sec % 60) + " sec. Budget " + session.day.budgetMin + " min. Too-fast line: " + session.day.tooFastMin + " min.",
        Math.round(sec / 60) + " د " + (sec % 60) + " ث. الميزانية " + session.day.budgetMin + " د. حد السرعة الزائدة: " + session.day.tooFastMin + " د.") + '</p>';
    if (raised) {
      html += '<p class="hs-banner">' + bi("Too easy. A harder set opens now, before you close this sitting.",
        "أسهل مما ينبغي. مجموعة أصعب تُفتح الآن، قبل أن تغلقي هذه الجلسة.") + '</p>'
        + '<button type="button" class="sp-btn" id="hs-extra">' + bi("Raise the bar", "ارفعي المستوى") + '</button>';
    } else if (fast && (g.corePct || 0) < 90) {
      html += '<p>' + bi("That was fast, and the core was not high enough to call it too easy. Speed without the score does not jump you.",
        "كان ذلك سريعًا، والجوهر لم يبلغ حد «أسهل مما ينبغي». السرعة بلا النتيجة لا تقفز بكِ.") + '</p>';
    }
    html += review(session.blocks, answers);
    if (!raised) html += nextControls(session.week, session.day && session.day.n);
    html += '<button type="button" class="sp-btn" id="hs-home">' + bi("Back to the plan", "العودة إلى الخطة") + '</button>';
    app.innerHTML = html;
    var extraBtn = document.getElementById("hs-extra");
    if (extraBtn) extraBtn.onclick = startExtra;
    document.getElementById("hs-home").onclick = function () { renderBoard(); refreshPackNotes(); app.innerHTML = ""; window.scrollTo(0, 0); };
    renderBoard();
    refreshPackNotes();
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
      var box = app.querySelector(".hs-banner");
      var note = '<p>' + bi("No unseen items sit above this tier. This period counts as mastered, and the pack moves on.",
        "لا بنود غير محلولة فوق هذا المستوى. تُحسب هذه الفترة على لوحة النتائج، وكل يوم آخر يبقى مفتوحًا.") + '</p>' + nextControls(session.week, session.day && session.day.n);
      if (box) box.insertAdjacentHTML("afterend", note);
      else app.insertAdjacentHTML("afterbegin", note);
      refreshPackNotes();
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
    save();
    var stuck = pct >= 80;
    app.innerHTML = '<h2>' + bi("Raised set: " + pct + "%", "المجموعة المرفوعة: " + pct + "%") + '</h2>'
      + '<p>' + (stuck
        ? bi("That stuck. This period is mastered, and the next one in the pack starts higher.", "ثبت. أُتقنت هذه الفترة، والتالية في الحزمة تبدأ أعلى.")
        : bi("The raise did not stick. This period is not mastered yet. The harder set is the one that counts.", "الرفع لم يثبت. هذه الفترة لم تُتقن بعد. المجموعة الأصعب هي التي تُحسب.")) + '</p>'
      + review(session.extraBlocks, g.answers)
      + nextControls(session.week, session.day && session.day.n)
      + '<button type="button" class="sp-btn" id="hs-home">' + bi("Back to the plan", "العودة إلى الخطة") + '</button>';
    document.getElementById("hs-home").onclick = function () { renderBoard(); refreshPackNotes(); app.innerHTML = ""; };
    renderBoard();
    refreshPackNotes();
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
      svg: drill.svg,
      tm: drill.tm,
      st: drill.st,
      cr: drill.cr,
      b: drill.b,
      p: drill.p,
      v: drill.v,
      en: drill.blurb_en || drill.title_en,
      ar: drill.blurb_ar || drill.title_ar,
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
    var bar = A.memPassBar(state, session.memId);
    A.noteMem(state, session.day, session.memId, pct);
    save();
    var hot = pct >= 95;
    var head = bi("Picture quiz: " + ok + "/" + qs.length + " (" + pct + "%)", "اختبار الصورة: " + ok + "/" + qs.length + " (" + pct + "%)");
    var msg = hot
      ? bi("95% or higher. Saved. The scoreboard treats this picture as easy. You can continue, retry, or open any other day.", "95% أو أكثر. حُفظت. لوحة النتائج تعامل هذه الصورة على أنها سهلة. يمكنك المتابعة أو الإعادة أو فتح أي يوم آخر.")
      : bi("Saved. The mastery mark for this picture is " + bar + "%. You can continue, retry, or open any other day. Nothing outside the picture is required.", "حُفظت. علامة الإتقان لهذه الصورة " + bar + "%. يمكنك المتابعة أو الإعادة أو فتح أي يوم آخر. لا شيء خارج الصورة مطلوب.");
    var idx = (session.memIndex || 0) + 1;
    var ids = (session.day && session.day.mem) || [];
    var go = idx < ids.length
      ? '<button type="button" class="sp-btn" data-day="' + session.day.n + '" data-mem="' + idx + '">' + bi("Next picture in this day", "الصورة التالية في هذا اليوم") + "</button>"
      : '<button type="button" class="sp-btn" data-day="' + session.day.n + '" data-phase="quiz">' + bi("Continue to the other quizzes", "تابعي إلى الاختبارات الأخرى") + "</button>";
    go += '<button type="button" class="sp-btn" data-day="' + session.day.n + '" data-mem="' + (session.memIndex || 0) + '">' + bi("Retry this picture", "أعيدي هذه الصورة") + "</button>";
    var rv = "";
    qs.forEach(function (q, i) {
      var good = answers[i] === q.ans;
      rv += '<li class="sp-day ' + (good ? "md-ok" : "md-bad") + '"><p>' + bi(q.en, q.ar) + '</p><p>'
        + (good ? "✅ " : "❌ ") + bi("Your answer: ", "إجابتك: ") + optLabel(q, answers[i] < 0 || answers[i] == null ? 0 : answers[i]) + '</p>'
        + (good ? "" : '<p><strong>' + bi("Correct: ", "الصحيح: ") + optLabel(q, q.ans) + '</strong></p>')
        + '</li>';
    });
    app.innerHTML = '<h2>' + head + '</h2><p>' + msg + '</p>'
      + go
      + nextControls(session.week, session.day && session.day.n)
      + '<button type="button" class="sp-btn" id="hs-home">' + bi("Back to the plan", "العودة إلى الخطة") + '</button>'
      + hesnaScene(session.blocks[0].set)
      + '<ol class="md-qs">' + rv + '</ol>';
    document.getElementById("hs-home").onclick = function () { renderBoard(); refreshPackNotes(); app.innerHTML = ""; window.scrollTo(0, 0); };
    renderBoard();
    refreshPackNotes();
    window.scrollTo(0, 0);
  }
  function findDay(n) {
    var day = null;
    (D.days || []).forEach(function (d) { if (d.n === n) day = d; });
    return day;
  }
  function startDay(n, memIndex, phase) {
    load();
    var day = findDay(n);
    if (!day) {
      app.innerHTML = '<p>' + bi("That day is not on this page.", "هذا اليوم ليس في هذه الصفحة.") + '</p>';
      window.scrollTo(0, 0);
      return;
    }
    var ids = day.mem || [];
    var i = memIndex || 0;
    if (phase !== "quiz" && i < ids.length && D.mem && D.mem[ids[i]]) {
      beginMemory({ memory: D.mem[ids[i]], day: day, week: A.weekOf(day.n), memIndex: i });
      window.scrollTo(0, 0);
      return;
    }
    var built = A.planSession(day, D, state);
    built.kind = "period";
    built.week = A.weekOf(day.n);
    session = built;
    session.day = day;
    save();
    refreshPackNotes();
    if (!session.nQ) {
      app.innerHTML = '<h2>' + bi(day.title_en, day.title_ar) + '</h2><p>' + bi(
        "The question bank has no unseen items left at this tier. Scores already saved still stand. You can open any other day, or study this day's picture again.",
        "بنك الأسئلة لم يبقَ فيه بنود غير محلولة في هذا المستوى. النتائج المحفوظة تبقى. يمكنك فتح أي يوم آخر، أو دراسة صورة هذا اليوم من جديد.") + '</p>'
        + '<button type="button" class="sp-btn" data-day="' + day.n + '" data-mem="0">' + bi("Study this day's picture again", "ادرسي صورة هذا اليوم من جديد") + '</button>';
      window.scrollTo(0, 0);
      return;
    }
    steps = flatten(session.blocks);
    showIntro(day);
    window.scrollTo(0, 0);
  }

  function boot() {
    app = document.getElementById("hs-app");
    board = document.getElementById("hs-board");
    if (!app || !D) return;
    load();
    if (A.resync) A.resync(state, D);
    save();
    renderBoard();
    refreshPackNotes();
    document.body.addEventListener("click", function (e) {
      var b = e.target.closest("[data-day],[data-week]");
      if (!b) return;
      if (b.hasAttribute("data-day")) {
        startDay(+b.getAttribute("data-day"), +(b.getAttribute("data-mem") || 0), b.getAttribute("data-phase") || "");
        return;
      }
      startDay((+b.getAttribute("data-week") - 1) * 7 + 1, 0, "");
    });
    var reset = document.getElementById("hs-reset");
    if (reset) reset.onclick = function () {
      if (!confirm(document.documentElement.lang === "ar"
        ? "مسح تقدّم الخطة في هذا المتصفح؟"
        : "Clear this plan's saved progress in this browser?")) return;
      state = { seen: {}, fam: {}, pillar: {}, days: {}, weeks: {} };
      save();
      renderBoard();
      refreshPackNotes();
      app.innerHTML = "";
    };
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
