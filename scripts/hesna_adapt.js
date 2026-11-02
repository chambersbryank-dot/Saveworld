/* Adaptive session builder for Hassnaa's HPD study pages.
   Four weeks, every day open. Scores are saved. Nothing is locked.
   A high score can still raise the tier inside a sitting.
   A family she already commands is not drilled again. */
(function (root, factory) {
  var api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.HesnaAdapt = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function acc(rec) {
    if (!rec || !rec.n) return null;
    return rec.ok / rec.n;
  }
  function famStat(state, family) {
    var s = (state.fam && state.fam[family]) || { ok: 0, n: 0 };
    return s;
  }
  function mastered(state, family) {
    var s = famStat(state, family);
    return s.n >= 4 && s.ok / s.n >= 0.95;
  }
  function weak(state, family) {
    var s = famStat(state, family);
    if (!s.n) return false; // unseen is not a weakness; Day 1 is the measurement
    return s.ok / s.n < 0.8;
  }
  function day1WeakFamilies(state) {
    var out = {};
    var d = (state.day1 && state.day1.fam) || {};
    Object.keys(d).forEach(function (f) {
      if (d[f].n && d[f].ok / d[f].n < 0.8) out[f] = true;
    });
    return out;
  }
  function seen(state, id) {
    return state.seen && state.seen[id];
  }
  function missed(state, id) {
    var s = seen(state, id);
    return !!(s && !s.ok);
  }
  function coreOf(prev) {
    if (!prev) return 0;
    if (prev.corePct != null) return prev.corePct;
    return prev.pct == null ? 0 : prev.pct;
  }
  function baseOf(prev) {
    if (!prev) return 0;
    if (prev.basePct != null) return prev.basePct;
    return coreOf(prev);
  }
  /** Too easy is judged on logic/reading/listening/comprehension, not on the
      grammar baseline. Missing a transfer trap on Day 1 is expected. */
  function hot(prev) {
    if (!prev || prev.pct == null) return false;
    var fast = prev.tooFastSec && prev.sec != null && prev.sec < prev.tooFastSec;
    var core = coreOf(prev);
    var base = baseOf(prev);
    if (core >= 95 || (core >= 90 && fast)) return true;
    if (prev.probeN >= 3 && prev.probePct >= 75 && base >= 85) return true;
    return false;
  }
  /** How many tiers to add because the previous day was too easy. */
  function bonus(prev) {
    if (!prev) return 0;
    if (hot(prev) && prev.extraPct != null && prev.extraPct >= 80) return 2;
    if (hot(prev)) return 1;
    return 0;
  }
  function needsBridge(prev) {
    if (!prev || prev.pct == null || hot(prev)) return false;
    return baseOf(prev) < 70;
  }
  var WEEK_DAYS = {
    1: [1, 2, 3, 4, 5, 6, 7],
    2: [8, 9, 10, 11, 12, 13, 14],
    3: [15, 16, 17, 18, 19, 20, 21],
    4: [22, 23, 24, 25, 26, 27, 28]
  };
  function weekOf(n) { return Math.min(4, Math.floor((n - 1) / 7) + 1); }
  function week1Core(state) {
    var sum = 0, n = 0;
    WEEK_DAYS[1].forEach(function (d) {
      var r = state && state.days && state.days[String(d)];
      if (!r || (r.corePct == null && r.pct == null)) return;
      var c = r.corePct != null ? r.corePct : r.pct;
      if (r.extraPct != null && c >= 95) c = r.extraPct;
      sum += c;
      n += 1;
    });
    return n ? Math.round(sum / n) : null;
  }
  /** Week 1 pictures pass at 80. Week 2 pictures are harder when Week 1 was strong. */
  function memPassBar(state, id) {
    var key = String(id || "");
    if (key.indexOf("qstop") !== 0 && key.indexOf("corner") !== 0) return 80;
    var overall = week1Core(state);
    var bar = 80;
    if (overall != null && overall >= 95) bar = 90;
    else if (overall != null && overall >= 85) bar = 85;
    ["b7426-1", "b7426-2", "b7426-3"].forEach(function (k) {
      var s = state && state.mem && state.mem[k];
      if (s != null && s < 85) bar = Math.max(bar, 85);
    });
    return Math.min(90, bar);
  }
  function memDone(state, row) {
    var ids = (row && row.memNeed) || [];
    return ids.every(function (id) {
      return ((state.mem && state.mem[id]) || 0) >= memPassBar(state, id);
    });
  }
  function markMastered(state, row) {
    if (!row) return false;
    row.mastered = judgeMastered(row) && memDone(state, row);
    return row.mastered;
  }
  /** 80% on the core masters a period. At 95% the harder set is the one that counts. */
  function judgeMastered(row) {
    if (!row || row.pct == null) return false;
    if (hot(row)) return row.extraPct != null && row.extraPct >= 80;
    if (row.corePct == null) return row.pct >= 80;
    return row.corePct >= 80;
  }
  function rowMastered(row) {
    if (!row || row.pct == null) return false;
    if (typeof row.mastered === "boolean") return row.mastered;
    return judgeMastered(row);
  }
  function weakFamilies(state) {
    var out = [];
    Object.keys((state && state.fam) || {}).forEach(function (f) {
      if (weak(state, f)) out.push(f);
    });
    return out.sort();
  }
  function weakPillars(state) {
    var out = [];
    ["logic", "reading", "comp", "listen", "obs"].forEach(function (p) {
      var r = state && state.pillar && state.pillar[p];
      if (r && r.n >= 3 && r.ok / r.n < 0.8) out.push(p);
    });
    return out;
  }
  function weekPerformance(state, week) {
    var ids = WEEK_DAYS[week] || [];
    var coreSum = 0, coreN = 0, hotN = 0, extraStuck = 0, masteredN = 0, scored = 0;
    ids.forEach(function (n) {
      var r = state && state.days && state.days[String(n)];
      if (!r || r.pct == null) return;
      scored += 1;
      var c = coreOf(r);
      if (c != null) { coreSum += c; coreN += 1; }
      if (hot(r)) hotN += 1;
      if (hot(r) && r.extraPct != null && r.extraPct >= 80) extraStuck += 1;
      if (rowMastered(r)) masteredN += 1;
    });
    return {
      n: scored,
      total: ids.length,
      overall: coreN ? Math.round(coreSum / coreN) : null,
      hotN: hotN,
      extraStuck: extraStuck,
      masteredN: masteredN,
      complete: ids.length > 0 && masteredN === ids.length
    };
  }
  /** Extra tiers for Week 2 once Week 1 is mastered. 0 still uses the higher week-2 plan. */
  function weekLift(state) {
    var p = weekPerformance(state, 1);
    if (!p.complete || p.overall == null) return 0;
    if (p.overall >= 95 || p.extraStuck >= 3) return 2;
    if (p.overall >= 85 || p.extraStuck >= 1) return 1;
    return 0;
  }
  function liveCleared(state, week) {
    var perf = weekPerformance(state, week);
    if (!perf.complete) return false;
    if (weakFamilies(state).length || weakPillars(state).length) return false;
    if (perf.overall != null && perf.overall >= 95) {
      var stretch = state.weeks && state.weeks[String(week)] && state.weeks[String(week)].stretchPct;
      if (perf.extraStuck < 1 && !(stretch >= 80)) return false;
    }
    return true;
  }
  /** Once a week is mastered, later misses do not lock it again. */
  function sealWeeks(state) {
    [1, 2, 3, 4].forEach(function (week) {
      var slot = state.weeks && state.weeks[String(week)];
      if (slot && slot.cleared) return;
      if (!liveCleared(state, week)) return;
      state.weeks = state.weeks || {};
      state.weeks[String(week)] = state.weeks[String(week)] || {};
      state.weeks[String(week)].cleared = true;
    });
  }
  function weekCleared(state, week) {
    var slot = state && state.weeks && state.weeks[String(week)];
    if (slot && slot.cleared) return true;
    return liveCleared(state, week);
  }
  function packDetail(state, week) {
    var prev = week > 1 ? weekPerformance(state, week - 1) : weekPerformance(state, week);
    return {
      overall: prev.overall,
      lift: week === 2 ? weekLift(state) : 0,
      fams: weakFamilies(state),
      pillars: weakPillars(state)
    };
  }
  function packStatus(state, week) {
    state = state || {};
    var ids = WEEK_DAYS[week] || [];
    var next = null, need = null;
    for (var i = 0; i < ids.length; i++) {
      var row = state.days && state.days[String(ids[i])];
      if (rowMastered(row)) continue;
      if (!row || row.pct == null) need = "fresh";
      else if (hot(row) && !(row.extraPct >= 80)) need = "extra";
      else if (!judgeMastered(row)) need = "retry";
      else if (!memDone(state, row)) need = "mem";
      else continue;
      next = ids[i];
      break;
    }
    var cleared = weekCleared(state, week);
    var blocked = false;
    var soft = weakFamilies(state).length || weakPillars(state).length;
    var needsRepair = next == null && !cleared && !!soft;
    var needsStretch = next == null && !cleared && !needsRepair;
    return {
      week: week,
      next: next,
      need: need,
      cleared: cleared,
      blocked: blocked,
      needsRepair: needsRepair,
      needsStretch: needsStretch,
      perf: weekPerformance(state, week),
      prev: week > 1 ? weekPerformance(state, week - 1) : null,
      lift: week === 2 ? weekLift(state) : 0,
      weakFams: weakFamilies(state),
      weakPillars: weakPillars(state)
    };
  }
  function pool(items, pred) {
    return (items || []).filter(pred);
  }
  function byTierDepth(tier, depth) {
    return function (it) {
      return it.tier === tier && (it.depth || 1) === depth;
    };
  }
  function takeFrom(items, n, state, pred) {
    var out = [];
    pool(items, function (it) {
      return !seen(state, it.id) && pred(it);
    }).forEach(function (it) {
      if (out.length < n) out.push(it);
    });
    return out;
  }
  /** Fill n items at tier/depth, then deeper bands, then the next tier. */
  function takeTier(items, n, state, tier, depth, extraPred, maxTier) {
    var out = [];
    var d, t;
    if (maxTier == null) maxTier = Math.min(6, tier + 1);
    function grab(pred) {
      if (out.length >= n) return;
      var more = takeFrom(items, n - out.length, state, function (it) {
        if (extraPred && !extraPred(it)) return false;
        return pred(it) && !out.some(function (x) { return x.id === it.id; });
      });
      out = out.concat(more);
    }
    for (t = tier; t <= maxTier && out.length < n; t++) {
      var startD = t === tier ? (depth || 1) : 1;
      for (d = startD; d <= 3 && out.length < n; d++) grab(byTierDepth(t, d));
      // Prefer the harder band, then any unseen item still in this tier.
      if (t === tier && startD > 1) {
        for (d = 1; d < startD && out.length < n; d++) grab(byTierDepth(t, d));
      }
    }
    if (out.length < n) {
      pool(items, function (it) {
        if (!missed(state, it.id)) return false;
        if (extraPred && !extraPred(it)) return false;
        return !out.some(function (x) { return x.id === it.id; });
      }).forEach(function (it) {
        if (out.length < n) out.push(it);
      });
    }
    return out;
  }
  function pickGrammar(items, day, state, tier, depth, n) {
    var gramm = pool(items, function (it) { return it.pillar === "grammar"; });
    if (day.n === 1) {
      return takeFrom(gramm, 99, state, function (it) { return !!it.diag; });
    }
    var out = [];
    var weakNow = {};
    gramm.forEach(function (it) {
      if (it.family && weak(state, it.family) && !mastered(state, it.family)) weakNow[it.family] = true;
    });
    // Day 3 rescores the families that were soft on the Day 1 baseline.
    if (day.n === 3) {
      var d1 = day1WeakFamilies(state);
      out = takeFrom(gramm, n, state, function (it) {
        return it.retest && it.family && d1[it.family] && !mastered(state, it.family);
      });
    }
    if (out.length < n) {
      var more = takeTier(gramm, n - out.length, state, tier, depth, function (it) {
        if (!it.family || mastered(state, it.family)) return false;
        if (it.diag || it.retest) return false;
        return weak(state, it.family);
      }, tier);
      // Drop ids already chosen.
      more.forEach(function (it) {
        if (out.length < n && !out.some(function (x) { return x.id === it.id; })) out.push(it);
      });
    }
    // A jumped tier must not skip the weak families. If nothing at this tier
    // is left, use the reserved retest sentences rather than drill a strength.
    if (day.n > 1 && out.length < n) {
      var rescue = takeFrom(gramm, n - out.length, state, function (it) {
        return it.retest && it.family && weak(state, it.family) && !mastered(state, it.family) && !out.some(function (x) { return x.id === it.id; });
      });
      out = out.concat(rescue);
    }
    // One spot-check of a mastered family, so retirement stays honest.
    if (day.n > 1) {
      var spot = takeFrom(gramm, 1, state, function (it) {
        return it.family && mastered(state, it.family) && !it.diag && !it.retest;
      });
      if (spot.length && out.length < n + 1) out.push(spot[0]);
    }
    return out.slice(0, n + 1);
  }
  function pickWritten(items, day, state, tier, depth, n) {
    var list = pool(items, function (it) { return it.pillar === "written"; });
    if (!n) return [];
    if (day.n === 1) return takeFrom(list, n, state, function (it) { return !!it.diag; });
    var out = [];
    if (day.n === 3) {
      var d1 = day1WeakFamilies(state);
      out = takeFrom(list, n, state, function (it) {
        return it.retest && it.family && d1[it.family] && !mastered(state, it.family);
      });
    }
    if (out.length < n) {
      var more = takeTier(list, n - out.length, state, tier, depth, function (it) {
        if (!it.family || mastered(state, it.family) || it.diag) return false;
        if (it.retest && day.n < 3) return false;
        if (day.n > 1 && it.family && !weak(state, it.family) && famStat(state, it.family).n) return false;
        return true;
      });
      more.forEach(function (it) {
        if (out.length < n && !out.some(function (x) { return x.id === it.id; })) out.push(it);
      });
    }
    if (out.length < n) {
      var fill = takeTier(list, n - out.length, state, tier, depth, function (it) {
        return it.family && !mastered(state, it.family) && !out.some(function (x) { return x.id === it.id; });
      });
      out = out.concat(fill);
    }
    return out.slice(0, n);
  }
  function pickPillar(items, pillar, n, state, tier, depth, pred) {
    var list = pool(items, function (it) {
      return it.pillar === pillar && (!pred || pred(it));
    });
    return takeTier(list, n, state, tier, depth, pred);
  }
  function pickWrapped(groups, pillar, n, state, tier, depth) {
    var g = pool(groups, function (it) { return it.pillar === pillar; });
    return takeTier(g, n, state, tier, depth);
  }
  /**
   * day: plan row. data: {items, reads, listens, comps, obs}. state: progress.
   * Returns {tier, depth, bonus, bridge, stretch, banner, blocks, tooFastSec}.
   * blocks: [{kind:'q', item} | {kind:'read'|'listen'|'comp'|'obs', set}]
   */
  function planSession(day, data, state) {
    state = state || {};
    var prev = state.days && state.days[String(day.n - 1)];
    var dayBonus = bonus(prev);
    var lift = weekOf(day.n) === 2 ? weekLift(state) : 0;
    var b = Math.max(dayBonus, lift);
    var tier = Math.min(6, day.tier + b);
    if ((state.logicTier || 0) > tier) tier = Math.min(6, state.logicTier);
    var depth = b ? 1 : day.depth;
    var stretch = tier === 6 && (b > 0 || day.depth >= 3);
    var perfPrev = weekOf(day.n) === 2 ? weekPerformance(state, 1) : null;
    var weekSoft = !!(perfPrev && perfPrev.complete && perfPrev.overall != null && perfPrev.overall < 85 && lift === 0);
    var bridge = (needsBridge(prev) && dayBonus === 0 && lift === 0) || (weekSoft && day.n === 8);
    var banner = null;
    if (weekSoft && day.n === 8) banner = "weekSoft";
    else if (lift >= 2 && lift >= dayBonus) banner = "weekJump2";
    else if (lift === 1 && lift >= dayBonus) banner = "weekJump";
    else if (dayBonus >= 2) banner = "jump2";
    else if (dayBonus === 1) banner = "jump";
    else if (bridge) banner = "bridge";
    else if (stretch && day.tier === 6) banner = "stretch";
    var blocks = [];
    if (bridge && prev) {
      var bridgeItems = pickPillar(data.items, "logic", 4, state, prev.tier, 1, function (it) {
        return !it.probe;
      });
      bridgeItems.forEach(function (it) { blocks.push({ kind: "q", item: it, bridge: true }); });
    }
    var counts = day.take || {};
    // Day 13: only soft spots, unless she is already at the end-state bar.
    if (day.mode === "repair") {
      var soft = repairBlocks(data, state);
      if (soft.length) {
        return finish(day, tier, depth, b, false, true, "repair", soft);
      }
      stretch = true;
      banner = "stretch";
      counts = day.stretchTake || counts;
    }
    if (day.mode === "capstone") {
      var prev13 = state.days && state.days["13"];
      if (prev13 && prev13.pct != null && prev13.pct < 96) {
        var again = repairBlocks(data, state);
        if (again.length) return finish(day, tier, depth, b, bridge, false, "repair", again);
      }
    }
    function pushQs(list) {
      list.forEach(function (it) { blocks.push({ kind: "q", item: it }); });
    }
    if (day.n === 1) {
      pushQs(pickGrammar(data.items, day, state, tier, depth, counts.grammar || 0));
      pushQs(pickPillar(data.items, "logic", counts.logic || 0, state, 1, 1, function (it) { return !it.probe; }));
      pushQs(pickPillar(data.items, "logic", 99, state, 3, 1, function (it) { return !!it.probe; }));
    } else {
      pushQs(pickPillar(data.items, "logic", counts.logic || 0, state, tier, depth, function (it) {
        return !it.probe && (!stretch || tier < 6 || it.stretch || it.depth >= depth);
      }));
      // If stretch filter starved the set, fill from the tier without it.
      var logicN = blocks.filter(function (x) { return x.kind === "q" && x.item.pillar === "logic" && !x.bridge; }).length;
      if ((counts.logic || 0) && logicN < counts.logic) {
        pushQs(pickPillar(data.items, "logic", counts.logic - logicN, state, tier, depth, function (it) { return !it.probe; }));
      }
      pushQs(pickGrammar(data.items, day, state, tier, depth, counts.grammar || 0));
    }
    pushQs(pickWritten(data.items, day, state, tier, depth, counts.ab || 0));
    pickWrapped(data.listens, "listen", listenCount(day, counts), state, tier, depth).forEach(function (set) {
      blocks.push({ kind: "listen", set: set });
    });
    pickWrapped(data.reads, "reading", counts.reading || 0, state, tier, depth).forEach(function (set) {
      blocks.push({ kind: "read", set: set });
    });
    pickWrapped(data.comps, "comp", counts.comp || 0, state, tier, depth).forEach(function (set) {
      blocks.push({ kind: "comp", set: set });
    });
    pickWrapped(data.obs, "obs", counts.obs || 0, state, tier, depth).forEach(function (set) {
      blocks.push({ kind: "obs", set: set });
    });
    if (weekOf(day.n) > 1) blocks = aimWeak(blocks, data, state, tier, depth);
    return finish(day, tier, depth, b, bridge, stretch, banner, blocks);
  }
  function aimWeak(blocks, data, state, tier, depth) {
    weakPillars(state).forEach(function (p) {
      var have = 0;
      blocks.forEach(function (b) {
        if (b.kind === "q" && b.item && b.item.pillar === p) have += 1;
        else if (b.set && b.set.pillar === p) have += (b.set.qs ? b.set.qs.length : 1);
      });
      if (have >= 3) return;
      if (p === "logic") {
        var list = pickPillar(data.items, "logic", 3 - have, state, tier, depth, function (it) { return !it.probe; });
        var head = [];
        list.forEach(function (it) {
          if (!blocks.some(function (b) { return b.kind === "q" && b.item && b.item.id === it.id; }) && !head.some(function (b) { return b.item.id === it.id; })) {
            head.push({ kind: "q", item: it, weak: true });
          }
        });
        blocks = head.concat(blocks);
      } else {
        var src = p === "reading" ? data.reads : p === "comp" ? data.comps : p === "listen" ? data.listens : data.obs;
        var kind = p === "reading" ? "read" : p === "comp" ? "comp" : p;
        pickWrapped(src, p, 1, state, tier, depth).forEach(function (set) {
          if (!blocks.some(function (b) { return b.set && b.set.id === set.id; })) {
            blocks.unshift({ kind: kind, set: set, weak: true });
          }
        });
      }
    });
    return blocks;
  }
  function listenCount(day, counts) {
    return counts.listen || 0;
  }
  function finish(day, tier, depth, b, bridge, stretch, banner, blocks) {
    return {
      tier: tier,
      depth: depth,
      bonus: b,
      bridge: !!bridge,
      stretch: !!stretch,
      banner: banner,
      blocks: blocks,
      tooFastSec: (day.tooFastMin || 0) * 60,
      budgetSec: (day.budgetMin || 0) * 60,
      nQ: countQ(blocks)
    };
  }
  function countQ(blocks) {
    var n = 0;
    blocks.forEach(function (b) {
      if (b.kind === "q") n += 1;
      else if (b.set && b.set.qs) n += b.set.qs.length;
    });
    return n;
  }
  /** Items and passage questions in families/pillars still under 95% after 3+ tries. */
  function repairBlocks(data, state) {
    var blocks = [];
    var gramm = pool(data.items, function (it) {
      return (it.pillar === "grammar" || it.pillar === "written") && it.family && weak(state, it.family) && !mastered(state, it.family);
    });
    gramm.sort(function (a, b) {
      return (seen(state, a.id) ? 1 : 0) - (seen(state, b.id) ? 1 : 0);
    });
    gramm.slice(0, 10).forEach(function (it) { blocks.push({ kind: "q", item: it }); });
    ["logic", "reading", "comp", "listen", "obs"].forEach(function (p) {
      var rec = (state.pillar && state.pillar[p]) || { ok: 0, n: 0 };
      if (rec.n >= 3 && rec.ok / rec.n < 0.95) {
        var src = p === "logic" ? data.items : p === "reading" ? data.reads : p === "comp" ? data.comps : p === "listen" ? data.listens : data.obs;
        var list = p === "logic"
          ? takeTier(pool(src, function (it) { return it.pillar === "logic" && !it.probe; }), 6, state, 6, 1)
          : takeTier(src, 1, state, 1, 1);
        if (p === "logic") list.forEach(function (it) { blocks.push({ kind: "q", item: it }); });
        else list.forEach(function (set) { blocks.push({ kind: p === "reading" ? "read" : p === "comp" ? "comp" : p, set: set }); });
      }
    });
    return blocks;
  }
  function grade(blocks, answers) {
    var ok = 0, n = 0, i = 0;
    var fam = {}, pillar = {};
    var core = { ok: 0, n: 0 }, base = { ok: 0, n: 0 }, probe = { ok: 0, n: 0 };
    function add(p, f, good, isProbe) {
      n += 1;
      if (good) ok += 1;
      pillar[p] = pillar[p] || { ok: 0, n: 0 };
      pillar[p].n += 1;
      if (good) pillar[p].ok += 1;
      if (f) {
        fam[f] = fam[f] || { ok: 0, n: 0 };
        fam[f].n += 1;
        if (good) fam[f].ok += 1;
      }
      if (p !== "grammar" && p !== "written") {
        core.n += 1;
        if (good) core.ok += 1;
        if (!isProbe) {
          base.n += 1;
          if (good) base.ok += 1;
        }
      }
      if (isProbe) {
        probe.n += 1;
        if (good) probe.ok += 1;
      }
    }
    blocks.forEach(function (b) {
      if (b.kind === "q") {
        add(b.item.pillar, b.item.family, answers[i] === b.item.ans, !!b.item.probe);
        i += 1;
      } else {
        b.set.qs.forEach(function (q) {
          add(b.set.pillar, q.family, answers[i] === q.ans, !!q.probe);
          i += 1;
        });
      }
    });
    function pct(x) { return x.n ? Math.round(100 * x.ok / x.n) : null; }
    return {
      ok: ok, n: n, pct: n ? Math.round(100 * ok / n) : 0,
      corePct: pct(core), basePct: pct(base), probePct: pct(probe), probeN: probe.n,
      fam: fam, pillar: pillar, answers: answers.slice()
    };
  }
  function absorb(state, blocks, answers, dayN) {
    state.seen = state.seen || {};
    state.fam = state.fam || {};
    state.pillar = state.pillar || {};
    var idx = 0;
    function mark(it, good) {
      state.seen[it.id] = { ok: good ? 1 : 0, pillar: it.pillar, family: it.family || "", tier: it.tier, day: dayN };
      if (it.family) {
        state.fam[it.family] = state.fam[it.family] || { ok: 0, n: 0 };
        state.fam[it.family].n += 1;
        if (good) state.fam[it.family].ok += 1;
      }
      if (it.pillar) {
        state.pillar[it.pillar] = state.pillar[it.pillar] || { ok: 0, n: 0 };
        state.pillar[it.pillar].n += 1;
        if (good) state.pillar[it.pillar].ok += 1;
      }
    }
    blocks.forEach(function (b) {
      if (b.kind === "q") {
        mark(b.item, answers[idx] === b.item.ans);
        idx += 1;
      } else {
        b.set.qs.forEach(function (q) {
          mark(Object.assign({ pillar: b.set.pillar, tier: b.set.tier }, q), answers[idx] === q.ans);
          idx += 1;
        });
      }
    });
  }
  function applyGrade(state, day, session, result, sec) {
    state.days = state.days || {};
    absorb(state, session.blocks, result.answers, day.n);
    if (day.n === 1 && !state.day1) {
      state.day1 = {};
      state.day1.fam = JSON.parse(JSON.stringify(state.fam));
      state.day1.pillar = JSON.parse(JSON.stringify(state.pillar));
      state.day1.pct = result.pct;
    }
    var row = {
      pct: result.pct,
      corePct: result.corePct,
      basePct: result.basePct,
      probePct: result.probePct,
      probeN: result.probeN || 0,
      sec: sec,
      tier: session.tier,
      tooFastSec: session.tooFastSec,
      n: result.n,
      at: Date.now()
    };
    row.memNeed = day.mem || row.memNeed || [];
    var prev = state.days[String(day.n)];
    if (prev && prev.quizzes) row.quizzes = prev.quizzes;
    state.days[String(day.n)] = row;
    markMastered(state, row);
    sealWeeks(state);
    return row;
  }
  function applyPackGrade(state, week, kind, blocks, result) {
    state.weeks = state.weeks || {};
    var slot = state.weeks[String(week)] || {};
    absorb(state, blocks, result.answers, week * 7);
    if (kind === "repair") slot.repairPct = result.pct;
    if (kind === "stretch") slot.stretchPct = result.corePct == null ? result.pct : result.corePct;
    slot.at = Date.now();
    state.weeks[String(week)] = slot;
    sealWeeks(state);
    return slot;
  }
  function stretchBlocks(data, state) {
    var blocks = [];
    takeTier(pool(data.items, function (it) {
      return it.pillar === "logic" && !it.probe && (it.stretch || (it.tier || 0) >= 6);
    }), 8, state, 6, 3).forEach(function (it) { blocks.push({ kind: "q", item: it }); });
    if (blocks.length < 4) {
      takeTier(pool(data.items, function (it) { return it.pillar === "logic" && !it.probe; }), 8 - blocks.length, state, 6, 1).forEach(function (it) {
        if (!blocks.some(function (b) { return b.item && b.item.id === it.id; })) blocks.push({ kind: "q", item: it });
      });
    }
    pickWrapped(data.obs, "obs", 1, state, 6, 1).forEach(function (set) { blocks.push({ kind: "obs", set: set }); });
    return blocks;
  }
  function findDay(data, n) {
    var days = (data && data.days) || [];
    for (var i = 0; i < days.length; i++) if (days[i].n === n) return days[i];
    return null;
  }
  function synthetic(week, kind) {
    var repair = kind === "repair";
    var ords = ["", "الأول", "الثاني", "الثالث", "الرابع"];
    var ord = ords[week] || String(week);
    return {
      n: week * 7,
      tier: 6,
      depth: 3,
      budgetMin: repair ? 40 : 35,
      tooFastMin: repair ? 18 : 16,
      mode: kind,
      title_en: repair ? "Week " + week + " — weak spots" : "Week " + week + " — the stretch",
      title_ar: repair ? "الأسبوع " + ord + " — المواضع اللينة" : "الأسبوع " + ord + " — التمدد",
      body_en: repair
        ? "This sitting is only what is still under 80%. The score is saved. Every other day stays open."
        : "This week was too easy. The stretch is the one that counts on the scoreboard. Every other day stays open.",
      body_ar: repair
        ? "هذه الجلسة لما يزال تحت 80% فقط. النتيجة تُحفظ. كل يوم آخر يبقى مفتوحًا."
        : "كان هذا الأسبوع أسهل مما ينبغي. التمدد هو الذي يُحسب على لوحة النتائج. كل يوم آخر يبقى مفتوحًا."
    };
  }
  function planPackStep(week, data, state) {
    state = state || {};
    var status = packStatus(state, week);
    if (status.cleared) return { done: true, status: status, week: week };
    if (status.needsStretch) {
      var stretch = stretchBlocks(data, state);
      if (!stretch.length) {
        state.weeks = state.weeks || {};
        state.weeks[String(week)] = state.weeks[String(week)] || {};
        state.weeks[String(week)].stretchPct = 80;
        return planPackStep(week, data, state);
      }
    }
    if (status.needsRepair || status.needsStretch) {
      var kind = status.needsRepair ? "repair" : "stretch";
      var synth = synthetic(week, kind);
      var blocks = kind === "repair" ? repairBlocks(data, state) : stretchBlocks(data, state);
      var session = finish(synth, 6, 3, 0, false, kind === "stretch", kind, blocks);
      session.kind = kind;
      session.week = week;
      session.bannerDetail = packDetail(state, week);
      return { session: session, day: synth, status: status, week: week };
    }
    var day = findDay(data, status.next);
    if (!day) return { empty: true, status: status, week: week };
    if (status.need === "mem") {
      var row = state.days && state.days[String(day.n)] || {};
      var ids = row.memNeed || day.mem || [];
      var id = null;
      for (var mi = 0; mi < ids.length; mi++) {
        if (((state.mem && state.mem[ids[mi]]) || 0) < memPassBar(state, ids[mi])) { id = ids[mi]; break; }
      }
      var drill = id && data.mem && data.mem[id];
      if (!drill) return { empty: true, status: status, week: week, day: day };
      return { memory: drill, day: day, status: status, week: week };
    }
    var session = planSession(day, data, state);
    session.kind = status.need === "extra" ? "extra" : "period";
    session.week = week;
    session.bannerDetail = packDetail(state, week);
    return {
      session: session,
      day: day,
      status: status,
      week: week,
      retryExtra: status.need === "extra"
    };
  }
  function extraTier(session) {
    return Math.min(6, session.tier + 1);
  }
  return {
    acc: acc,
    mastered: mastered,
    weak: weak,
    hot: hot,
    bonus: bonus,
    planSession: planSession,
    planPackStep: planPackStep,
    packStatus: packStatus,
    weekOf: weekOf,
    weekCleared: weekCleared,
    weekLift: weekLift,
    weekPerformance: weekPerformance,
    rowMastered: rowMastered,
    weakFamilies: weakFamilies,
    weakPillars: weakPillars,
    grade: grade,
    applyGrade: applyGrade,
    applyPackGrade: applyPackGrade,
    absorb: absorb,
    extraTier: extraTier,
    countQ: countQ,
    noteExtra: function (state, dayN, pct) {
      var row = state.days && state.days[String(dayN)];
      if (!row) return;
      row.extraPct = pct;
      markMastered(state, row);
      sealWeeks(state);
    },
    memPassBar: memPassBar,
    noteMem: function (state, day, id, pct) {
      state.mem = state.mem || {};
      var prev = state.mem[id] || 0;
      if (pct > prev) state.mem[id] = pct;
      var row = state.days && state.days[String(day.n)];
      if (row) {
        row.memNeed = day.mem || row.memNeed || [];
        markMastered(state, row);
      }
      sealWeeks(state);
    },
    resync: function (state, data) {
      state.mem = state.mem || {};
      ((data && data.days) || []).forEach(function (day) {
        var row = state.days && state.days[String(day.n)];
        if (!row || row.pct == null) return;
        row.memNeed = day.mem || [];
        markMastered(state, row);
      });
      sealWeeks(state);
      return state;
    }
  };
});
