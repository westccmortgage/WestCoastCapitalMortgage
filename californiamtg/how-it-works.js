/* ============================================================
   California Mortgage — "How It Works" guided explainer
   5 live mini-demos with an illustrated guide + speech bubble + optional voice.
   Educational only; simple transparent formulas (we disclaim exactness).
   ============================================================ */
(function () {
  "use strict";
  var root = document.getElementById("hiw");
  if (!root) return;

  var $ = function (s) { return root.querySelector(s); };
  function fmt(v) { return "$" + Math.round(v).toLocaleString("en-US"); }
  function pmt(L, ratePct, n) { var i = ratePct / 100 / 12; if (i <= 0) return L / n; return L * i * Math.pow(1 + i, n) / (Math.pow(1 + i, n) - 1); }
  function rateForScore(s) {
    var add = s >= 740 ? 0 : s >= 720 ? 0.25 : s >= 700 ? 0.5 : s >= 680 ? 0.875 : s >= 660 ? 1.25 : s >= 640 ? 1.75 : 2.5;
    return 6.5 + add;
  }
  function set(sel, txt) { var e = $(sel); if (e) e.textContent = txt; }
  function on(sel, fn) { var e = $(sel); if (e) { e.addEventListener("input", fn); fn(); } }

  /* ---- step bubbles ---- */
  var BUBBLES = [
    "Hi, I’m your Financial Navigator — here to help you understand your options, no pressure. Let’s start with the county limit: lenders draw a line, and below it your loan is “conforming,” above it you go “jumbo.” Drag the price and watch where the line is crossed.",
    "Put 20% down and monthly mortgage insurance (PMI) goes away. Slide the down payment and watch PMI appear or disappear.",
    "Your credit score moves your rate. Lower the score and both the rate and the monthly payment climb.",
    "More income usually means you can support a larger loan — but taxes rise too. Slide your income to see both move.",
    "Interest-only lowers the early payment; points (a buydown) can lower the rate for a cost. Compare them here."
  ];
  var TOTAL = 5;
  var step = 1, voiceOn = false;

  /* ---- per-demo wiring (runs once) ---- */
  // 1) Jumbo line
  var BASELINE = 806500, CEILING = 1209750;
  function calc1() {
    var price = +$("#hiw1-price").value, dp = +$("#hiw1-down").value;
    var loan = Math.max(0, price * (1 - dp / 100));
    set("#hiw1-priceout", fmt(price)); set("#hiw1-downout", dp + "%");
    set("#hiw1-loan", fmt(loan));
    var zone = loan <= BASELINE ? "Conforming" : loan <= CEILING ? "High-Balance Conforming" : "Jumbo";
    var z = $("#hiw1-zone"); if (z) { z.textContent = zone + " Review"; z.setAttribute("data-zone", zone.split(" ")[0].toLowerCase()); }
  }
  on("#hiw1-price", calc1); on("#hiw1-down", calc1);

  // 2) PMI
  function calc2() {
    var dp = +$("#hiw2-down").value, price = 1000000, loan = price * (1 - dp / 100), ltv = 100 - dp;
    set("#hiw2-downout", dp + "%"); set("#hiw2-ltv", ltv + "%");
    var pmi = dp < 20 ? loan * 0.006 / 12 : 0;
    set("#hiw2-pmi", pmi > 0 ? fmt(pmi) + "/mo" : "No PMI — 20%+ down");
    var p = $("#hiw2-pmi"); if (p) p.setAttribute("data-on", pmi > 0 ? "yes" : "no");
  }
  on("#hiw2-down", calc2);

  // 3) Score -> rate
  function calc3() {
    var s = +$("#hiw3-score").value, rate = rateForScore(s), pi = pmt(800000, rate, 360);
    set("#hiw3-scoreout", String(s)); set("#hiw3-rate", rate.toFixed(3).replace(/0+$/, "").replace(/\.$/, "") + "%");
    set("#hiw3-pi", fmt(pi) + "/mo");
  }
  on("#hiw3-score", calc3);

  // 4) Income -> loan + taxes
  function calc4() {
    var inc = +$("#hiw4-income").value;
    set("#hiw4-incomeout", fmt(inc));
    var budget = inc / 12 * 0.43, rate = 6.84, i = rate / 100 / 12, n = 360;
    var loan = budget > 0 ? budget * (Math.pow(1 + i, n) - 1) / (i * Math.pow(1 + i, n)) : 0;
    set("#hiw4-loan", fmt(loan) + " · at 43% DTI");
    set("#hiw4-tax", fmt(inc * 0.22) + "/yr · ~22% effective");
  }
  on("#hiw4-income", calc4);

  // 5) P&I vs IO + buydown
  var mode5 = "pi";
  function calc5() {
    var L = 800000, base = 6.84, pts = +$("#hiw5-pts").value, eff = base - 0.25 * pts;
    set("#hiw5-ptsout", pts + (pts === 1 ? " point" : " points"));
    var pi = pmt(L, eff, 360), io = L * (eff / 100) / 12;
    var sel = mode5 === "io" ? io : pi;
    set("#hiw5-pay", fmt(sel) + "/mo");
    set("#hiw5-rate", eff.toFixed(2) + "%" + (pts > 0 ? " (after buydown)" : ""));
    set("#hiw5-diff", "Interest-only is " + fmt(pi - io) + "/mo lower than amortizing");
  }
  root.querySelectorAll("[data-hiw-mode]").forEach(function (b) {
    b.addEventListener("click", function () {
      mode5 = b.getAttribute("data-hiw-mode");
      root.querySelectorAll("[data-hiw-mode]").forEach(function (x) { x.classList.toggle("is-sel", x === b); });
      calc5();
    });
  });
  on("#hiw5-pts", calc5);

  /* ---- voice: real Financial Navigator clips (same takes as the guided tour),
     one per step, instead of the robotic Web-Speech synthesizer ---- */
  var CLIPS = [
    "/assets/video/avatar/step-county.mp4",  // 1 — where the jumbo line is
    "/assets/video/avatar/step-down.mp4",    // 2 — down payment & PMI
    "/assets/video/avatar/step-fico.mp4",    // 3 — credit score → rate
    "/assets/video/avatar/step-income.mp4",  // 4 — income → buying power & taxes
    "/assets/video/avatar/step-io.mp4"       // 5 — payment type & buydown
  ];
  // Hidden media element: we only need the avatar's audio track here.
  var voiceEl = document.createElement("video");
  voiceEl.setAttribute("playsinline", "");
  voiceEl.preload = "none";
  voiceEl.style.cssText = "position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none";
  document.body.appendChild(voiceEl);

  function speak() {
    if (!voiceOn) return;
    var src = CLIPS[step - 1] || CLIPS[0];
    try {
      if (voiceEl.getAttribute("src") !== src) { voiceEl.setAttribute("src", src); voiceEl.load(); }
      voiceEl.currentTime = 0;
      voiceEl.muted = false;
      var p = voiceEl.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) { /* ignore */ }
  }
  function stopVoice() { try { voiceEl.pause(); } catch (e) {} }

  var voiceBtn = $("#hiwVoice");
  if (voiceBtn) {
    voiceBtn.addEventListener("click", function () {
      voiceOn = !voiceOn;
      voiceBtn.setAttribute("aria-pressed", String(voiceOn));
      voiceBtn.classList.toggle("is-on", voiceOn);
      voiceBtn.textContent = voiceOn ? "🔊 Voice on" : "🔊 Listen";
      if (voiceOn) speak(); else stopVoice();
    });
  }

  /* ---- step navigation ---- */
  function render() {
    root.querySelectorAll(".hiw-step").forEach(function (p) {
      p.classList.toggle("is-active", +p.getAttribute("data-step") === step);
    });
    set("#hiwCur", String(step));
    var bar = $("#hiwBar"); if (bar) bar.style.width = Math.round(step / TOTAL * 100) + "%";
    var bubble = $("#hiwBubble"); if (bubble) bubble.textContent = BUBBLES[step - 1];
    var back = $("#hiwBack"), next = $("#hiwNext");
    if (back) back.disabled = step === 1;
    if (next) next.textContent = step === TOTAL ? "Done ✓" : "Next →";
    speak();
  }
  var nextBtn = $("#hiwNext"), backBtn = $("#hiwBack");
  if (nextBtn) nextBtn.addEventListener("click", function () {
    if (step < TOTAL) { step++; render(); root.scrollIntoView({ behavior: "smooth", block: "start" }); }
    else { var cta = $("#hiwCta"); if (cta) cta.scrollIntoView({ behavior: "smooth", block: "center" }); }
  });
  if (backBtn) backBtn.addEventListener("click", function () { if (step > 1) { step--; render(); } });

  render();
})();
