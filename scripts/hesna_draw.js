/* Draw a memory scene so every quiz fact is visible: shirt, pants, hair,
   hat, the carried object (including a cup), plates, and arrows.
   Photos and hand-drawn incidents pass through. */
function hesnaScene(s) {
  function esc(v) {
    return String(v == null ? "" : v).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function bi(en, ar) {
    return '<span data-en>' + esc(en) + '</span><span data-ar>' + esc(ar) + '</span>';
  }
  function T(x, y, t, sz, f, w) {
    return '<text x="' + x + '" y="' + y + '" font-size="' + (sz || 12) + '" text-anchor="middle" fill="' + (f || "#111") + '"' + (w ? ' font-weight="bold"' : "") + ">" + esc(t) + "</text>";
  }
  var credit = '<figcaption class="si-credit">' + bi("Created by SI and Biological SI Partner", "أُنشئ بواسطة SI وBiological SI Partner") + "</figcaption>";
  if (s.img) {
    return '<figure class="md-fig"><img src="' + esc(s.img) + '" alt="' + esc(s.alt || "Practice scene") + '" style="width:100%;height:auto;border-radius:12px">' + credit + "</figure>";
  }
  if (s.svg) return s.svg + credit;
  var HX = { red: "#d32f2f", blue: "#1e5bd8", green: "#2e7d32", yellow: "#fbc02d", orange: "#fb8c00", purple: "#7b1fa2", pink: "#f48fb1", white: "#f5f5f5", black: "#222", gray: "#888", brown: "#6d4c41", blonde: "#e8c66a" };
  var BC = { yellow: "#f6e3a1", green: "#cfe8c8", blue: "#cfd8f5", pink: "#f5d0e0", white: "#f4f4f4", orange: "#f8d2a8", red: "#f3c1c1", gray: "#d9d9d9", black: "#cfcfcf", purple: "#e3d4f5", brown: "#e6d3c4" };
  var o = '<svg viewBox="0 0 800 460" role="img" aria-label="Practice scene" style="width:100%;height:auto;background:#bfe3ff;border-radius:12px;font-family:sans-serif">';
  o += '<circle cx="400" cy="34" r="22" fill="#ffd34d"/>';
  o += '<rect x="14" y="10" width="120" height="44" rx="8" fill="#fff" stroke="#333" stroke-width="2"/><circle cx="36" cy="32" r="12" fill="none" stroke="#333" stroke-width="2"/><path d="M36 32V24M36 32h6" stroke="#333" stroke-width="2"/>' + T(90, 38, s.tm, 15, "#111", 1);
  o += '<rect x="640" y="10" width="150" height="22" fill="#185"/>' + T(715, 26, s.st, 13, "#fff") + '<rect x="640" y="34" width="150" height="22" fill="#185"/>' + T(715, 50, s.cr, 13, "#fff");
  var nb = s.b.length, bw = 760 / nb;
  s.b.forEach(function (b, i) {
    var x = 20 + i * bw;
    var fill = BC[b.c] || HX[b.c] || "#ddd";
    o += '<rect x="' + (x + 6) + '" y="80" width="' + (bw - 12) + '" height="240" fill="' + fill + '" stroke="#555" stroke-width="2"/><rect x="' + (x + 14) + '" y="90" width="' + (bw - 28) + '" height="30" fill="#0b3a5b"/>' + T(x + bw / 2, 111, b.n, Math.min(16, (bw - 30) / Math.max(1, b.n.length) * 1.6), "#fff", 1) + T(x + bw / 2, 150, b.no, 22, "#111", 1) + '<rect x="' + (x + bw / 2 - 22) + '" y="230" width="44" height="90" fill="#6b4a2a"/><rect x="' + (x + 20) + '" y="170" width="' + (bw / 2 - 50) + '" height="50" fill="#9cd" stroke="#333"/>';
  });
  o += '<rect x="0" y="320" width="800" height="32" fill="#ccc"/><rect x="0" y="352" width="800" height="108" fill="#555"/><path d="M0 406H800" stroke="#fff" stroke-width="4" stroke-dasharray="30 20"/>';
  var np = s.p.length;
  s.p.forEach(function (p, i) {
    var x = 60 + i * (680 / Math.max(1, np - 1));
    var h = HX[p.h] || "#c8956b";
    var c = HX[p.ic] || "#888";
    o += '<rect x="' + (x - 8) + '" y="318" width="7" height="28" fill="' + (HX[p.p] || "#444") + '"/><rect x="' + (x + 1) + '" y="318" width="7" height="28" fill="' + (HX[p.p] || "#444") + '"/><rect x="' + (x - 12) + '" y="286" width="24" height="34" rx="4" fill="' + (HX[p.s] || "#888") + '" stroke="#333"/><circle cx="' + x + '" cy="274" r="11" fill="#c8956b"/>';
    if (p.hat) {
      o += '<rect x="' + (x - 12) + '" y="260" width="24" height="7" fill="' + (HX[p.hat] || "#333") + '" stroke="#333"/><rect x="' + (x - 8) + '" y="254" width="16" height="8" fill="' + (HX[p.hat] || "#333") + '"/>';
    } else {
      o += '<path d="M' + (x - 11) + ' 272 q11 -18 22 0" fill="' + h + '" stroke="#333" stroke-width="1.4"/>';
    }
    var ix = x + 22;
    if (p.i === "bag") o += '<rect x="' + (ix - 8) + '" y="298" width="18" height="20" rx="3" fill="' + c + '" stroke="#333"/><path d="M' + (ix - 2) + ' 298 q5 -8 10 0" fill="none" stroke="#333" stroke-width="2"/>';
    else if (p.i === "umbrella") o += '<path d="M' + (ix - 16) + ' 262 q16 -24 32 0 z" fill="' + c + '" stroke="#333"/><line x1="' + ix + '" y1="262" x2="' + ix + '" y2="304" stroke="#333" stroke-width="2"/>';
    else if (p.i === "phone") o += '<rect x="' + (ix - 5) + '" y="284" width="10" height="16" rx="2" fill="' + c + '" stroke="#333"/>';
    else if (p.i === "balloon") o += '<line x1="' + ix + '" y1="304" x2="' + ix + '" y2="250" stroke="#333"/><circle cx="' + ix + '" cy="242" r="11" fill="' + c + '" stroke="#333"/>';
    else if (p.i === "box") o += '<rect x="' + (ix - 9) + '" y="294" width="20" height="18" fill="' + c + '" stroke="#333"/><path d="M' + (ix - 9) + ' 294 l10 -6 l10 6" fill="none" stroke="#333"/>';
    else if (p.i === "cup") o += '<path d="M' + (ix - 7) + ' 292 h14 v9 q0 11 -7 11 q-7 0 -7 -11 z" fill="' + c + '" stroke="#333"/><path d="M' + (ix + 7) + ' 296 q12 4 0 14" fill="none" stroke="#333" stroke-width="2"/>';
    else o += '<rect x="' + (ix - 6) + '" y="292" width="12" height="14" fill="' + c + '" stroke="#333"/>';
  });
  var nv = s.v.length;
  s.v.forEach(function (v, i) {
    var x = 20 + i * (760 / nv), w = Math.min(170, 760 / nv - 20), y = i % 2 ? 400 : 360, c = HX[v.c] || "#888", q = "";
    if (v.t === "van") q = '<rect x="' + x + '" y="' + (y - 22) + '" width="' + w + '" height="62" rx="8" fill="' + c + '" stroke="#333"/>';
    else if (v.t === "pickup") q = '<rect x="' + x + '" y="' + (y + 6) + '" width="' + w + '" height="34" rx="6" fill="' + c + '" stroke="#333"/><rect x="' + (x + w * 0.55) + '" y="' + (y - 14) + '" width="' + (w * 0.4) + '" height="24" rx="5" fill="' + c + '" stroke="#333"/>';
    else {
      q = '<rect x="' + x + '" y="' + (y + 6) + '" width="' + w + '" height="34" rx="10" fill="' + c + '" stroke="#333"/><rect x="' + (x + w * 0.25) + '" y="' + (y - 12) + '" width="' + (w * 0.5) + '" height="22" rx="7" fill="' + c + '" stroke="#333"/>';
      if (v.t === "taxi") q += '<rect x="' + (x + w / 2 - 18) + '" y="' + (y - 24) + '" width="36" height="12" fill="#222"/>' + T(x + w / 2, y - 14, "TAXI", 9, "#fc0");
    }
    q += '<rect x="' + (x + w / 2 - 34) + '" y="' + (y + 20) + '" width="68" height="16" fill="#ffd" stroke="#333"/>' + T(x + w / 2, y + 33, v.pl, 12, "#111", 1) + '<circle cx="' + (x + 22) + '" cy="' + (y + 42) + '" r="10" fill="#222"/><circle cx="' + (x + w - 22) + '" cy="' + (y + 42) + '" r="10" fill="#222"/>' + T(v.d === "E" ? x + w + 10 : x - 10, y + 20, v.d === "E" ? "→" : "←", 22, "#fff", 1);
    o += q;
  });
  return o + "</svg>" + credit;
}
