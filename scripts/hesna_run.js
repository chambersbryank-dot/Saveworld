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
  function weekAr(n) { return n === 1 ? "الأول" : n === 2 ? "الثاني" : String(n); }
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
    [1, 2].forEach(function (w) {
      var st = A.packStatus(state, w);
      var p = st.perf;
      var statusEn, statusAr;
      if (st.blocked) { statusEn = "locked until the previous week is mastered"; statusAr = "مقفلة حتى يُتقن الأسبوع السابق"; }
      else if (st.cleared) { statusEn = "mastered"; statusAr = "مُتقنة"; }
      else if (st.needsRepair) { statusEn = p.masteredN + "/" + p.total + " periods mastered · weak spots still open"; statusAr = p.masteredN + "/" + p.total + " فترات مُتقنة · مواضع لينة ما زالت مفتوحة"; }
      else if (st.needsStretch) { statusEn = p.masteredN + "/" + p.total + " periods mastered · stretch still open"; statusAr = p.masteredN + "/" + p.total + " فترات مُتقنة · التمدد ما زال مفتوحًا"; }
      else { statusEn = p.masteredN + "/" + p.total + " periods mastered"; statusAr = p.masteredN + "/" + p.total + " فترات مُتقنة"; }
      var core = p.overall == null ? "—" : p.overall + "%";
      weeks += "<li>" + bi("Week " + w + " pack: " + statusEn + " · core " + core, "حزمة الأسبوع " + weekAr(w) + ": " + statusAr + " · الجوهر " + core) + "</li>";
    });
    board.innerHTML = '<h2>' + bi("Scoreboard", "لوحة النتائج") + '</h2>'
      + '<p>' + bi("Each week is one pack. A period is mastered at 80% on the core before the next period. At 95% the harder set is the one that counts. Week 2 opens only after Week 1 is mastered, and it is harder from that week's weak spots and overall score. Day 1 is still the photograph. A family at 95% over 4 or more items is retired.",
        "كل أسبوع حزمة واحدة. تُتقن الفترة عند 80% في الجوهر قبل الفترة التالية. عند 95% المجموعة الأصعب هي التي تُحسب. الأسبوع الثاني يُفتح فقط بعد إتقان الأسبوع الأول، وهو أصعب بناءً على مواضع الضعف والنتيجة الإجمالية. اليوم 1 ما زال الصورة. العائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف.") + '</p>'
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
      "You are already on the top tier. The stretch bank is the raise: tighter corrections, no victory lap. Master it before the next week opens.",
      "أنتِ أصلًا في أعلى مستوى. بنك التمدد هو رفع المستوى: تصحيحات أدق، بلا جولة نصر. أتقنيه قبل أن يُفتح الأسبوع التالي.");
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
  function nextControls(week) {
    var st = A.packStatus(state, week);
    if (st.blocked) return "";
    if (st.cleared) {
      if (week < 2) return '<p>' + bi("Week 1 is mastered. Week 2 is open, and it is harder.", "أُتقن الأسبوع الأول. الأسبوع الثاني مفتوح، وهو أصعب.") + '</p><button type="button" class="sp-btn" data-week="2">' + bi("Start the Week 2 pack", "ابدئي حزمة الأسبوع الثاني") + "</button>";
      return "<p>" + bi("Both weekly packs are mastered. The end state for these two weeks is about 98% on this kind of page.", "أُتقنت حزمتا الأسبوعين. حالة نهاية هذين الأسبوعين نحو 98% على صفحة من هذا النوع.") + "</p>";
    }
    var en = "Next period in this pack", ar = "الفترة التالية في هذه الحزمة";
    if (st.needsRepair) { en = "Repair the weak spots"; ar = "أصلحي المواضع اللينة"; }
    else if (st.needsStretch) { en = "Master the stretch"; ar = "أتقني التمدد"; }
    else if (st.need === "retry") { en = "Retry this period. It is not mastered yet."; ar = "أعيدي هذه الفترة. لم تُتقن بعد."; }
    else if (st.need === "extra") { en = "The harder set is the one that counts"; ar = "المجموعة الأصعب هي التي تُحسب"; }
    return '<button type="button" class="sp-btn" data-week="' + week + '">' + bi(en, ar) + "</button>";
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
      "Visual pack: open Memory Drills. Week 1 is the 7426 burglary, three quizzes, 2 minutes each, then the picture hides. 80% unlocks the next quiz. 95% means that quiz was too easy and the harder one is the one that counts. Week 2 is Quick Stop, then the corner crash, and the pass bar rises when Week 1 was strong. Street sketches sit inside the same weekly packs.",
      "الحزمة البصرية: افتحي تمارين الذاكرة. الأسبوع الأول سطو 7426، ثلاثة اختبارات، دقيقتان لكل منها، ثم تختفي الصورة. 80% تفتح الاختبار التالي. 95% تعني أن الاختبار كان أسهل مما ينبغي والأصعب هو الذي يُحسب. الأسبوع الثاني كويك ستوب ثم حادث الزاوية، وعتبة النجاح ترتفع إذا كان الأسبوع الأول قويًا. رسوم الشوارع داخل حزم الأسابيع نفسها.");
    var period = day.n ? ((day.n - 1) % 7) + 1 : 0;
    var where = (session.kind === "repair" || session.kind === "stretch" || session.kind === "extra")
      ? bi("Week " + session.week + " pack", "حزمة الأسبوع " + weekAr(session.week))
      : bi("Week " + session.week + " pack · period " + period + " of 7", "حزمة الأسبوع " + weekAr(session.week) + " · الفترة " + period + " من 7");
    var lesson = (day.body_en && day.body_ar) ? "<p>" + bi(day.body_en, day.body_ar) + "</p>" : "";
    app.innerHTML = '<p class="sp-ph">' + where + '</p><h2>' + bi(day.title_en, day.title_ar) + '</h2>'
      + (b ? '<p class="hs-banner">' + b + '</p>' : '')
      + detailLine()
      + lesson
      + '<p>' + bi("Tier " + session.tier + " · " + session.nQ + " questions · budget " + day.budgetMin + " min. A period is mastered at 80% on the core. Too easy: core 95%+, or core 90%+ in under " + day.tooFastMin + " min, and then the harder set is the one that counts. You do not skip ahead inside the pack. Grammar misses do not freeze the tier. Grammar mastery does not get more drills.",
        "المستوى " + session.tier + " · " + session.nQ + " سؤالًا · الميزانية " + day.budgetMin + " د. تُتقن الفترة عند 80% في الجوهر. أسهل مما ينبغي: جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في أقل من " + day.tooFastMin + " د، وعندها المجموعة الأصعب هي التي تُحسب. لا قفز داخل الحزمة. أخطاء القواعد لا تجمّد المستوى. وإتقان القواعد لا يجلب تمارين إضافية.") + '</p>'
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
    if (step.set.img) {
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
      el.innerHTML = bi("Time left: ", "الوقت المتبقي: ") + left + "s";
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
    if (!raised) html += nextControls(session.week);
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
        "لا بنود غير محلولة فوق هذا المستوى. تُحسب هذه الفترة مُتقنة، والحزمة تتابع.") + '</p>' + nextControls(session.week);
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
      + nextControls(session.week)
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
    [1, 2].forEach(function (w) {
      var note = document.getElementById("hs-pack-note-" + w);
      var btn = document.getElementById("hs-pack-btn-" + w);
      if (!note && !btn) return;
      var st = A.packStatus(state, w);
      var p = st.perf;
      var en, ar, ben, bar;
      if (st.blocked) {
        en = "Locked. Master Week " + (w - 1) + " first, including its weak spots. This pack will be harder when it opens.";
        ar = "مقفلة. أتقني الأسبوع " + weekAr(w - 1) + " أولًا، بما فيه مواضع الضعف. هذه الحزمة ستكون أصعب حين تُفتح.";
        ben = "Week " + w + " pack is locked";
        bar = "حزمة الأسبوع " + weekAr(w) + " مقفلة";
      } else if (st.cleared) {
        en = "Mastered. Core " + (p.overall == null ? "—" : p.overall + "%") + ".";
        ar = "مُتقنة. الجوهر " + (p.overall == null ? "—" : p.overall + "%") + ".";
        ben = "Review the Week " + w + " pack";
        bar = "راجعي حزمة الأسبوع " + weekAr(w);
      } else if (p.masteredN > 0 || st.needsRepair || st.needsStretch) {
        en = p.masteredN + " of " + p.total + " periods mastered" + (p.overall == null ? "" : " · core " + p.overall + "%") + (st.needsRepair ? " · weak spots still open" : "") + (st.needsStretch ? " · stretch still open" : "") + ".";
        ar = p.masteredN + " من " + p.total + " فترات مُتقنة" + (p.overall == null ? "" : " · الجوهر " + p.overall + "%") + (st.needsRepair ? " · مواضع لينة ما زالت مفتوحة" : "") + (st.needsStretch ? " · التمدد ما زال مفتوحًا" : "") + ".";
        ben = "Continue the Week " + w + " pack";
        bar = "تابعي حزمة الأسبوع " + weekAr(w);
      } else {
        en = w === 1
          ? "Opens on Day 1. Master each period before the next. Week 2 stays closed until this pack is mastered."
          : "Harder than Week 1, from that week's weak spots and overall score. Master each period before the next.";
        ar = w === 1
          ? "تُفتح على اليوم 1. أتقني كل فترة قبل التالية. الأسبوع الثاني يبقى مغلقًا حتى تُتقن هذه الحزمة."
          : "أصعب من الأسبوع الأول، من مواضع ضعفه ونتيجته الإجمالية. أتقني كل فترة قبل التالية.";
        ben = "Start the Week " + w + " pack";
        bar = "ابدئي حزمة الأسبوع " + weekAr(w);
      }
      if (note) note.innerHTML = bi(en, ar);
      if (btn) {
        btn.innerHTML = bi(ben, bar);
        if (st.blocked) btn.setAttribute("aria-disabled", "true");
        else btn.removeAttribute("aria-disabled");
      }
    });
  }

  function startWeek(week) {
    load();
    var step = A.planPackStep(week, D, state);
    save();
    refreshPackNotes();
    if (step.blocked) {
      app.innerHTML = '<p class="hs-banner">' + bi(
        "Week " + (week - 1) + " is not mastered yet. Finish that pack, including the weak spots, before this one opens. The next week is harder, and it waits.",
        "الأسبوع " + weekAr(week - 1) + " لم يُتقن بعد. أكملي تلك الحزمة، بما فيها مواضع الضعف، قبل أن تُفتح هذه. الأسبوع التالي أصعب، وهو ينتظر.") + '</p>';
      window.scrollTo(0, 0);
      return;
    }
    if (step.done) {
      app.innerHTML = '<h2>' + bi("Week " + week + " is mastered.", "أُتقن الأسبوع " + weekAr(week) + ".") + '</h2>' + nextControls(week);
      window.scrollTo(0, 0);
      return;
    }
    if (!step.session) {
      app.innerHTML = '<p>' + bi("Nothing new is left in this pack. Reset the saved progress if you want the photograph again.",
        "لم يبقَ جديد في هذه الحزمة. أعيدي التقدّم المحفوظ إذا أردتِ الصورة من جديد.") + '</p>';
      return;
    }
    session = step.session;
    session.day = step.day;
    if (step.retryExtra) {
      showIntro(step.day);
      var begin = document.getElementById("hs-begin");
      if (begin) begin.onclick = function () { startExtra(); };
      window.scrollTo(0, 0);
      return;
    }
    if (!session.nQ) {
      app.innerHTML = '<p>' + bi("Nothing new is left at this tier. Reset the saved progress if you want the photograph again, or continue the pack.",
        "لم يبقَ جديد في هذا المستوى. أعيدي التقدّم المحفوظ إذا أردتِ الصورة من جديد، أو تابعي الحزمة.") + '</p>' + nextControls(week);
      return;
    }
    steps = flatten(session.blocks);
    showIntro(step.day);
    window.scrollTo(0, 0);
  }

  function boot() {
    app = document.getElementById("hs-app");
    board = document.getElementById("hs-board");
    if (!app || !D) return;
    load();
    renderBoard();
    refreshPackNotes();
    document.body.addEventListener("click", function (e) {
      var b = e.target.closest("[data-week]");
      if (!b) return;
      startWeek(+b.getAttribute("data-week"));
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
