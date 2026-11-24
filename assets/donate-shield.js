/* Icon-only donate shield. Tooltip stays off the Donate button. */
(function () {
  var hoverMQ = window.matchMedia("(hover: hover) and (pointer: fine)");
  var hoverOK = hoverMQ.matches;
  if (hoverMQ.addEventListener) {
    hoverMQ.addEventListener("change", function () { hoverOK = hoverMQ.matches; });
  }

  function donateButton(shield) {
    var wrap = shield.closest(".sp-shield-wrap") || shield;
    var node = wrap.previousElementSibling;
    var steps = 0;
    while (node && steps < 4) {
      if (node.matches && node.matches("a")) return node;
      node = node.previousElementSibling;
      steps += 1;
    }
    return null;
  }

  function pad(r, p) {
    return { left: r.left - p, top: r.top - p, right: r.right + p, bottom: r.bottom + p };
  }

  function overlapArea(a, b) {
    var w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    var h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (w <= 0 || h <= 0) return 0;
    return w * h;
  }

  function choose(shieldRect, tipW, tipH, btnRect) {
    var vw = window.visualViewport ? window.visualViewport.width : window.innerWidth;
    var vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    var margin = 8;
    var gap = 10;
    var btnLeft = false;
    var btnRight = false;
    var btnAbove = false;
    var btnBelow = false;
    if (btnRect && btnRect.width && btnRect.height) {
      var scx = (shieldRect.left + shieldRect.right) / 2;
      var bcx = (btnRect.left + btnRect.right) / 2;
      var scy = (shieldRect.top + shieldRect.bottom) / 2;
      var bcy = (btnRect.top + btnRect.bottom) / 2;
      var vOverlap = !(btnRect.bottom < shieldRect.top - 2 || btnRect.top > shieldRect.bottom + 2);
      var hOverlap = !(btnRect.right < shieldRect.left - 2 || btnRect.left > shieldRect.right + 2);
      if (vOverlap && bcx < scx) btnLeft = true;
      if (vOverlap && bcx >= scx) btnRight = true;
      if (hOverlap && bcy < scy) btnAbove = true;
      if (hOverlap && bcy >= scy) btnBelow = true;
      if (!vOverlap && !hOverlap) {
        if (bcy < scy) btnAbove = true;
        else btnBelow = true;
        if (bcx < scx) btnLeft = true;
        else btnRight = true;
      }
    }
    function box(left, top) {
      return { left: left, top: top, right: left + tipW, bottom: top + tipH };
    }
    function clamp(b) {
      var left = b.left;
      var top = b.top;
      if (left < margin) left = margin;
      if (top < margin) top = margin;
      if (left + tipW > vw - margin) left = Math.max(margin, vw - margin - tipW);
      if (top + tipH > vh - margin) top = Math.max(margin, vh - margin - tipH);
      return box(left, top);
    }
    var raw = [];
    function above() {
      if (btnRight) raw.push(box(shieldRect.right - tipW, shieldRect.top - gap - tipH));
      else raw.push(box(shieldRect.left, shieldRect.top - gap - tipH));
    }
    function below() {
      if (btnRight) raw.push(box(shieldRect.right - tipW, shieldRect.bottom + gap));
      else raw.push(box(shieldRect.left, shieldRect.bottom + gap));
    }
    function sideRight() { raw.push(box(shieldRect.right + gap, shieldRect.top + (shieldRect.height - tipH) / 2)); }
    function sideLeft() { raw.push(box(shieldRect.left - gap - tipW, shieldRect.top + (shieldRect.height - tipH) / 2)); }
    if (!btnAbove) above();
    if (!btnRight) sideRight();
    if (!btnLeft) sideLeft();
    if (!btnBelow) below();
    above();
    below();
    sideRight();
    sideLeft();

    var btnPad = btnRect ? pad(btnRect, 8) : null;
    var shieldPad = pad(shieldRect, 4);
    function inside(b) {
      return b.left >= margin - 0.5 && b.top >= margin - 0.5 && b.right <= vw - margin + 0.5 && b.bottom <= vh - margin + 0.5;
    }
    function clearOf(b, rects) {
      if (!rects) return true;
      for (var n = 0; n < rects.length; n++) {
        if (overlapArea(b, rects[n]) > 0) return false;
      }
      return true;
    }
    var best = null;
    var bestScore = Infinity;
    for (var pass = 0; pass < 2; pass++) {
      for (var i = 0; i < raw.length; i++) {
        var candidate = raw[i];
        if (!inside(candidate)) continue;
        if (btnPad && overlapArea(candidate, btnPad) > 0) continue;
        if (overlapArea(candidate, shieldPad) > 0) continue;
        if (pass === 0 && !clearOf(candidate, choose.extras)) continue;
        return candidate;
      }
    }
    for (var j = 0; j < raw.length; j++) {
      var c = clamp(raw[j]);
      var btnHit = btnPad ? overlapArea(c, btnPad) : 0;
      var shieldHit = overlapArea(c, shieldPad);
      var off = inside(c) ? 0 : 1;
      var score = btnHit * 100 + shieldHit * 10 + off * 100000 + j;
      if (score < bestScore) {
        bestScore = score;
        best = c;
      }
    }
    return best || box(margin, margin);
  }

  function labelFor(shield) {
    if (shield._label && shield._label.isConnected) return shield._label;
    var label = shield.querySelector(".sp-shield-label");
    if (label) shield._label = label;
    return label;
  }

  function place(shield) {
    var label = labelFor(shield);
    if (!label) return;
    if (label.parentNode !== document.body) document.body.appendChild(label);
    label._shield = shield;
    var shieldRect = shield.getBoundingClientRect();
    var btn = donateButton(shield);
    var btnRect = btn ? btn.getBoundingClientRect() : null;
    label.style.position = "fixed";
    label.style.left = "0px";
    label.style.top = "0px";
    label.style.right = "auto";
    label.style.bottom = "auto";
    label.style.zIndex = "10000";
    var cap = window.visualViewport ? window.visualViewport.width : window.innerWidth;
    var room = cap - 24;
    if (btnRect && btnRect.width) {
      if (btnRect.right <= shieldRect.left + 4) room = cap - shieldRect.left - 12;
      else if (btnRect.left >= shieldRect.right - 4) room = shieldRect.right - 12;
    }
    label.style.maxWidth = Math.max(96, Math.min(220, room)) + "px";
    label.style.visibility = "hidden";
    var tr = label.getBoundingClientRect();
    var extras = [];
    var row = shield.closest(".hero-title-row, .wh-card");
    if (row) {
      var heading = row.querySelector("h1, h3");
      if (heading) extras.push(pad(heading.getBoundingClientRect(), 4));
    }
    choose.extras = extras;
    var spot = choose(shieldRect, tr.width, tr.height, btn ? btn.getBoundingClientRect() : null);
    choose.extras = null;
    label.style.left = Math.round(spot.left) + "px";
    label.style.top = Math.round(spot.top) + "px";
    label.style.visibility = "";
    label.classList.add("is-floating");
    shield.classList.add("is-placed");
  }

  function unplace(shield) {
    var label = labelFor(shield);
    if (!label) return;
    label.style.position = "";
    label.style.left = "";
    label.style.top = "";
    label.style.right = "";
    label.style.bottom = "";
    label.style.zIndex = "";
    label.style.maxWidth = "";
    label.style.visibility = "";
    label.classList.remove("is-floating");
    if (label.parentNode !== shield) shield.appendChild(label);
    shield.classList.remove("is-placed");
  }

  function shieldFrom(node) {
    if (!node || !node.closest) return null;
    var direct = node.closest(".sp-shield");
    if (direct) return direct;
    var label = node.closest(".sp-shield-label");
    if (label && label._shield) return label._shield;
    return null;
  }

  function openRecord(shield) {
    if (!shield || shield.tagName !== "A" || !shield.href) return;
    if (shield.target === "_blank") window.open(shield.href, "_blank", "noopener");
    else window.location.href = shield.href;
  }

  function sync(el) {
    var focused = el === document.activeElement || el.contains(document.activeElement);
    var on = !el.classList.contains("is-dismissed") && (el.dataset.pinned === "1" || el.dataset.hover === "1" || focused);
    el.classList.toggle("is-shown", on);
    if (on) place(el);
    else unplace(el);
  }

  function closeOthers(except) {
    document.querySelectorAll(".sp-shield").forEach(function (el) {
      if (el === except) return;
      if (!el.dataset.pinned && !el.dataset.hover && !el.classList.contains("is-shown")) return;
      delete el.dataset.pinned;
      delete el.dataset.hover;
      sync(el);
    });
  }

  document.addEventListener("pointerover", function (e) {
    if (e.pointerType === "touch") return;
    var shield = shieldFrom(e.target);
    if (!shield) return;
    shield.classList.remove("is-dismissed");
    shield.dataset.hover = "1";
    sync(shield);
  }, true);

  document.addEventListener("pointerout", function (e) {
    var shield = shieldFrom(e.target);
    if (!shield) return;
    if (shieldFrom(e.relatedTarget) === shield) return;
    var to = e.relatedTarget;
    if (to && shield.contains(to)) return;
    delete shield.dataset.hover;
    sync(shield);
  }, true);

  document.addEventListener("focusin", function (e) {
    var shield = shieldFrom(e.target);
    if (!shield) return;
    shield.classList.remove("is-dismissed");
    sync(shield);
  });

  document.addEventListener("focusout", function (e) {
    var shield = shieldFrom(e.target);
    if (!shield) return;
    setTimeout(function () { sync(shield); }, 0);
  });

  var lastPointer = "mouse";
  document.addEventListener("pointerdown", function (e) {
    lastPointer = e.pointerType || "mouse";
    var shield = shieldFrom(e.target);
    closeOthers(shield || null);
    if (!shield) {
      document.querySelectorAll(".sp-shield[data-pinned]").forEach(function (el) {
        delete el.dataset.pinned;
        sync(el);
      });
    }
  }, true);

  document.addEventListener("click", function (e) {
    var shield = shieldFrom(e.target);
    if (!shield) return;
    var onLabel = e.target.closest && e.target.closest(".sp-shield-label");
    var link = shield.tagName === "A";
    if (onLabel && link) {
      e.preventDefault();
      openRecord(shield);
      return;
    }
    if (lastPointer !== "touch" && link) return;
    if (shield.dataset.pinned === "1") {
      if (link) return;
      delete shield.dataset.pinned;
      sync(shield);
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    shield.classList.remove("is-dismissed");
    shield.dataset.pinned = "1";
    sync(shield);
  }, true);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") lastPointer = "key";
    if (e.key !== "Escape") return;
    document.querySelectorAll(".sp-shield").forEach(function (el) {
      delete el.dataset.pinned;
      delete el.dataset.hover;
      el.classList.add("is-dismissed");
      sync(el);
    });
    var active = document.activeElement;
    if (active && active.classList && active.classList.contains("sp-shield")) active.blur();
  });

  var scheduled = false;
  function reposition() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      document.querySelectorAll(".sp-shield.is-shown").forEach(place);
    });
  }
  window.addEventListener("scroll", reposition, true);
  window.addEventListener("resize", reposition);
})();
