/* Adaptive session builder for Hesna's HPD study pages.
   Overachievement raises the tier immediately. A family she already
   commands is not drilled again. Day N+1 is a higher demand than day N
   unless a bridge is required after a score under 70. */
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
    var b = bonus(prev);
    var tier = Math.min(6, day.tier + b);
    if ((state.logicTier || 0) > tier) tier = Math.min(6, state.logicTier);
    var depth = b ? 1 : day.depth;
    var stretch = tier === 6 && (b > 0 || day.depth >= 3);
    var bridge = needsBridge(prev) && b === 0;
    var banner = null;
    if (b >= 2) banner = "jump2";
    else if (b === 1) banner = "jump";
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
    return finish(day, tier, depth, b, bridge, stretch, banner, blocks);
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
      return it.pillar === "grammar" && it.family && !seen(state, it.id) && !mastered(state, it.family) && weak(state, it.family) && famStat(state, it.family).n > 0;
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
      if (p !== "grammar") {
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
    state.days[String(day.n)] = row;
    return row;
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
    grade: grade,
    applyGrade: applyGrade,
    absorb: absorb,
    extraTier: extraTier,
    countQ: countQ,
    noteExtra: function (state, dayN, pct) {
      if (state.days && state.days[String(dayN)]) state.days[String(dayN)].extraPct = pct;
    }
  };
});
