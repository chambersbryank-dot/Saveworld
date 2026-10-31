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
    ["logic", "grammar", "reading", "comp", "listen", "obs"].forEach(function (p) {
      var r = state.pillar[p];
      if (!r || !r.n) return;
      pillar += '<li>' + esc(p) + ': ' + Math.round(100 * r.ok / r.n) + '% (' + r.ok + '/' + r.n + ')</li>';
    });
    board.innerHTML = '<h2>' + bi("Scoreboard", "لوحة النتائج") + '</h2>'
      + '<p>' + bi("Day 1 is the photograph. The latest column is who you are on these items now. A family at 95% over 4 or more items is retired.",
        "اليوم 1 هو الصورة. العمود الأخير هو مستواكِ على هذه البنود الآن. العائلة التي تبلغ 95% في 4 بنود أو أكثر تُوقف.") + '</p>'
      + (last ? '<p>' + bi("Latest sitting: Day " + lastN + " · " + last.pct + "% overall · core " + (last.corePct == null ? "—" : last.corePct + "%") + " · tier " + last.tier + " · " + Math.round((last.sec || 0) / 60) + " min.",
        "آخر جلسة: اليوم " + lastN + " · " + last.pct + "% إجمالًا · الجوهر " + (last.corePct == null ? "—" : last.corePct + "%") + " · المستوى " + last.tier + " · " + Math.round((last.sec || 0) / 60) + " د.") + '</p>'
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
      "You are already on the top tier. The stretch bank is the raise: tighter corrections, no victory lap.",
      "أنتِ أصلًا في أعلى مستوى. بنك التمدد هو رفع المستوى: تصحيحات أدق، بلا جولة نصر.");
    return "";
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
    var memLv = day.n <= 2 ? 1 : day.n <= 3 ? 2 : day.n <= 4 ? 3 : day.n <= 6 ? 4 : day.n <= 8 ? 5 : 6;
    var memNote = session.nQ < 12
      ? bi("Only " + session.nQ + " written items are left at this tier, because earlier sittings cleared the bank. Also do Memory Level " + memLv + " (45 questions). That scene is what keeps today from being a snack.",
        "لم يبقَ إلا " + session.nQ + " بندًا مكتوبًا في هذا المستوى، لأن الجلسات السابقة أفرغت البنك. اعملي أيضًا مستوى الذاكرة " + memLv + " (45 سؤالًا). ذلك المشهد هو ما يمنع اليوم من أن يكون وجبة خفيفة.")
      : bi("When this sitting is done, Memory Level " + memLv + " is the scene for today if you have not already cleared it at 95%.",
        "بعد هذه الجلسة، مستوى الذاكرة " + memLv + " هو مشهد اليوم إذا لم تكوني قد أنجزتيه بنسبة 95%.");
    app.innerHTML = '<h2>' + bi(day.title_en, day.title_ar) + '</h2>'
      + (b ? '<p class="hs-banner">' + b + '</p>' : '')
      + '<p>' + bi("Tier " + session.tier + " · " + session.nQ + " questions · budget " + day.budgetMin + " min. Too easy: core 95%+, or core 90%+ in under " + day.tooFastMin + " min. Grammar misses do not freeze the tier. Grammar mastery does not get more drills.",
        "المستوى " + session.tier + " · " + session.nQ + " سؤالًا · الميزانية " + day.budgetMin + " د. سهل أكثر من اللازم: جوهر 95% أو أكثر، أو جوهر 90% أو أكثر في أقل من " + day.tooFastMin + " د. أخطاء القواعد لا تجمّد المستوى. وإتقان القواعد لا يجلب تمارين إضافية.") + '</p>'
      + '<p>' + memNote + '</p>'
      + (day.n > 1 && !(state.day1 && state.day1.fam) ? '<p class="hs-banner">' + bi("Day 1 has not been scored in this browser. The grammar baseline is not in yet, so this sitting cannot aim extra drills at your weak families. Start Day 1 first if you have not.", "اليوم 1 لم يُسجَّل في هذا المتصفح. خط أساس القواعد غير موجود بعد، فلا تستطيع هذه الجلسة توجيه تمارين إضافية إلى عائلاتكِ الضعيفة. ابدئي باليوم 1 إذا لم تفعلي.") + '</p>' : '')
      + '<button type="button" class="sp-btn" id="hs-begin">' + bi("Begin", "ابدئي") + '</button>';
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
    app.innerHTML = '<p class="md-timer" id="hs-script-t"></p><p class="hs-script">' + esc(step.set.en) + '</p>'
      + '<p class="sp-ph">' + bi(step.kind === "obs" ? "Observation. Read once. It will hide." : "Radio call. Read once. It will hide.",
        step.kind === "obs" ? "ملاحظة. اقرئي مرة واحدة. سيختفي." : "نداء لاسلكي. اقرئي مرة واحدة. سيختفي.") + '</p>'
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
      passage = '<div class="hs-passage"><p>' + esc(step.passage.en) + '</p><p class="sp-ph">' + esc(step.passage.ar) + '</p></div>';
    }
    var opts = "";
    item.opts.forEach(function (o, i) {
      opts += '<button type="button" class="hs-opt" data-i="' + i + '">' + optLabel(item, i) + '</button>';
    });
    app.innerHTML = '<p class="sp-ph">' + bi("Question " + sofar + " of " + nQ, "السؤال " + sofar + " من " + nQ) + ' · <span id="hs-clock"></span></p>'
      + passage
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
    A.applyGrade(state, session.day, session, g, sec);
    save();
    var row = state.days[String(session.day.n)];
    var fast = row.tooFastSec && sec < row.tooFastSec;
    var raised = A.hot(row);
    var html = '<h2>' + bi("Day " + session.day.n + ": " + g.pct + "%", "اليوم " + session.day.n + ": " + g.pct + "%") + '</h2>'
      + '<p>' + bi("Core (logic, reading, listening, comprehension, observation): " + (g.corePct == null ? "—" : g.corePct + "%") + ". Grammar is tracked by family and does not hold the tier.",
        "الجوهر (منطق، قراءة، استماع، فهم، ملاحظة): " + (g.corePct == null ? "—" : g.corePct + "%") + ". القواعد تُتابَع حسب العائلة ولا تحبس المستوى.") + '</p>'
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
    html += '<button type="button" class="sp-btn" id="hs-home">' + bi("Back to the plan", "العودة إلى الخطة") + '</button>';
    app.innerHTML = html;
    var extraBtn = document.getElementById("hs-extra");
    if (extraBtn) extraBtn.onclick = startExtra;
    document.getElementById("hs-home").onclick = function () { renderBoard(); app.innerHTML = ""; window.scrollTo(0, 0); };
    renderBoard();
    window.scrollTo(0, 0);
  }

  function startExtra() {
    var row = state.days[String(session.day.n)] || {};
    var tier = A.extraTier(session);
    if (row.probeN >= 3 && row.probePct >= 75) tier = Math.min(6, Math.max(tier, 3));
    var items = (D.items || []).filter(function (it) {
      return it.pillar === "logic" && !it.probe && it.tier >= tier && !state.seen[it.id];
    }).slice(0, 8);
    if (!items.length) {
      A.noteExtra(state, session.day.n, 80);
      save();
      app.querySelector(".hs-banner").insertAdjacentHTML("afterend", '<p>' + bi("No unseen items sit above this tier. Tomorrow still starts higher.",
        "لا بنود غير محلولة فوق هذا المستوى. وغدًا يبدأ أعلى رغم ذلك.") + '</p>');
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
        ? bi("That stuck. The next day jumps an extra tier.", "ثبت. اليوم التالي يقفز مستوى إضافيًا.")
        : bi("The raise did not stick yet. Tomorrow goes up one tier, not two.", "الرفع لم يثبت بعد. غدًا يصعد مستوى واحدًا لا اثنين.")) + '</p>'
      + review(session.extraBlocks, g.answers)
      + '<button type="button" class="sp-btn" id="hs-home">' + bi("Back to the plan", "العودة إلى الخطة") + '</button>';
    document.getElementById("hs-home").onclick = function () { renderBoard(); app.innerHTML = ""; };
    renderBoard();
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

  function startDay(n) {
    var day = D.days.filter(function (d) { return d.n === n; })[0];
    if (!day) return;
    load();
    session = A.planSession(day, D, state);
    session.day = day;
    if (!session.nQ) {
      app.innerHTML = '<p>' + bi("Nothing new is left at this tier. Reset the saved progress if you want the photograph again, or go to the next day.",
        "لم يبقَ جديد في هذا المستوى. أعيدي التقدّم المحفوظ إذا أردتِ الصورة من جديد، أو انتقلي إلى اليوم التالي.") + '</p>';
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
    renderBoard();
    document.body.addEventListener("click", function (e) {
      var b = e.target.closest("[data-day]");
      if (!b) return;
      startDay(+b.getAttribute("data-day"));
    });
    var reset = document.getElementById("hs-reset");
    if (reset) reset.onclick = function () {
      if (!confirm(document.documentElement.lang === "ar"
        ? "مسح تقدّم الخطة في هذا المتصفح؟"
        : "Clear this plan's saved progress in this browser?")) return;
      state = { seen: {}, fam: {}, pillar: {}, days: {} };
      save();
      renderBoard();
      app.innerHTML = "";
    };
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
