/* ============================================================
   California Mortgage — Guided Tool Tutorial (modular overlay)
   ------------------------------------------------------------
   A self-contained, data-driven walkthrough of the Strategy
   Console. It does NOT touch the calculator's logic — it only
   reads/sets a few sample values and highlights sections.

   Safe by design:
     • If a step's target is missing, the step is skipped.
     • Every action runs in try/catch so it can never break the
       calculator or throw console errors.
     • Nothing here runs until the user clicks "How This Works".

   -----------------------------------------------------------
   WHERE TO EDIT TUTORIAL TEXT:  the STEPS array below.
   WHERE TO ADD FUTURE AVATAR VIDEO/AUDIO:  set "videoSrc" /
     "audioSrc" / "avatarText" on any step in STEPS.
   ============================================================ */
(function () {
  "use strict";

  /* ----------------------------------------------------------
     1. TUTORIAL STEPS (data-driven — edit text here)
     Each step supports:
       target     – value of the data-tutorial="..." attribute
       title      – short heading
       body       – plain-English explanation (consumer friendly)
       demo       – optional { sel, value } sample value to type in
       action     – optional function(api) for custom behavior
       avatarText – placeholder text for the future avatar/video
       videoSrc   – optional path to a future video clip
       audioSrc   – optional path to a future audio clip
     ---------------------------------------------------------- */
  var STEPS = [
    {
      target: "zip",
      title: "Start with the property ZIP code",
      body: "Type the ZIP code where the home is located. We use it to find the county, because each county has its own loan size limits.",
      demo: { sel: "#hs-q", value: "90210" },
      avatarText: "Avatar explanation will appear here",
      videoSrc: null, audioSrc: null
    },
    {
      target: "county-limit",
      title: "Your county's loan limit",
      body: "Every county has a cut-off loan amount. Stay under it and your loan is a regular “conforming” loan. Go over it and it becomes a bigger “jumbo” loan. This bar shows where your loan sits versus that line.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "property-value",
      title: "Home price or value",
      body: "Drag this to the home's price (for a purchase) or its current value (for a refinance). Most other numbers update from this one.",
      demo: { sel: "#hs-value", value: "1600000" },
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "loan-purpose",
      title: "What you're trying to do",
      body: "Buying a home, refinancing, pulling cash out, or financing a rental? Pick the goal and the tool shows only the fields that matter for it.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "down-payment",
      title: "Your down payment",
      body: "This is the cash you put in up front. Putting down 20% or more usually removes monthly mortgage insurance (PMI), which lowers your payment.",
      demo: { sel: "#hs-down", value: "20" },
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "fico",
      title: "Your credit score (FICO)",
      body: "A higher score usually means a lower interest rate. Slide it and watch the assumed rate and payment change. 740 and up is already strong.",
      demo: { sel: "#hs-score", value: "760" },
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "income-type",
      title: "How you earn your income",
      body: "A regular paycheck (W-2) is the simplest to document. If you're self-employed or paid on 1099, lenders look at different paperwork, which can affect your rate.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "income",
      title: "Your yearly income",
      body: "We use this to estimate how large a loan your income could comfortably support. It's a rough guide, not an approval.",
      demo: { sel: "#hs-income", value: "180000" },
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "result",
      title: "Conforming vs. jumbo result",
      body: "This is the headline answer: whether your loan stays under the county line (conforming) or goes over it (jumbo). Jumbo loans have their own rules and rates.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "payment-strategy",
      title: "How you want to pay",
      body: "“Principal & Interest” slowly pays the loan off. “Interest Only” keeps the early payment lower but doesn't reduce what you owe. Tap to compare.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "buydown",
      title: "Buying down your rate (points)",
      body: "You can pay a little extra up front to lower your interest rate. This shows the cost, the monthly savings, and how long until it pays for itself.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "interest-only",
      title: "Interest-only preview",
      body: "Here's the estimated payment if you only paid the interest each month. Lower now, but the balance doesn't go down — useful to compare, not always the goal.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "final-review",
      title: "Your strategy review",
      body: "When you're ready, this is where you can continue to a secure application or talk to a licensed mortgage professional. Everything above is educational — no credit pull, nothing sent anywhere.",
      avatarText: "Avatar explanation will appear here"
    }
  ];

  var STORAGE_KEY = "cm_tutorial_done_v1";
  var MOBILE = function () { return window.matchMedia("(max-width: 760px)").matches; };

  /* ----------------------------------------------------------
     2. State + element refs (built lazily)
     ---------------------------------------------------------- */
  var state = { idx: 0, order: [], open: false, prevFocus: null };
  var els = {};

  function qTarget(key) {
    if (!key) return null;
    try { return document.querySelector('[data-tutorial="' + key + '"]'); }
    catch (e) { return null; }
  }

  /* Build the list of steps whose target currently exists. Missing
     targets are simply left out, so navigation never lands on one. */
  function buildOrder() {
    state.order = [];
    for (var i = 0; i < STEPS.length; i++) {
      if (qTarget(STEPS[i].target)) state.order.push(i);
    }
  }

  /* ----------------------------------------------------------
     3. Overlay DOM (created once, on first launch)
     ---------------------------------------------------------- */
  function buildOverlay() {
    if (els.root) return;

    var root = document.createElement("div");
    root.className = "cmtut";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "How this tool works");
    root.hidden = true;

    root.innerHTML =
      '<div class="cmtut__spot" data-tut-spot></div>' +
      '<div class="cmtut__card" data-tut-card>' +
        '<button type="button" class="cmtut__close" data-tut-skip aria-label="Close tutorial">×</button>' +
        '<div class="cmtut__avatar" data-tut-avatar>' +
          '<span class="cmtut__avatar-tag">Guide</span>' +
          '<p class="cmtut__avatar-text" data-tut-avatartext>Avatar explanation will appear here</p>' +
        '</div>' +
        '<p class="cmtut__step" data-tut-count>Step 1 of 1</p>' +
        '<h3 class="cmtut__title" data-tut-title></h3>' +
        '<p class="cmtut__body" data-tut-body></p>' +
        '<div class="cmtut__nav">' +
          '<button type="button" class="cmtut__btn cmtut__btn--ghost" data-tut-skip>Skip</button>' +
          '<div class="cmtut__nav-right">' +
            '<button type="button" class="cmtut__btn cmtut__btn--ghost" data-tut-back>Back</button>' +
            '<button type="button" class="cmtut__btn cmtut__btn--primary" data-tut-next>Next</button>' +
          '</div>' +
        '</div>' +
      '</div>';

    document.body.appendChild(root);

    els.root = root;
    els.spot = root.querySelector("[data-tut-spot]");
    els.card = root.querySelector("[data-tut-card]");
    els.avatar = root.querySelector("[data-tut-avatar]");
    els.avatarText = root.querySelector("[data-tut-avatartext]");
    els.count = root.querySelector("[data-tut-count]");
    els.title = root.querySelector("[data-tut-title]");
    els.body = root.querySelector("[data-tut-body]");
    els.back = root.querySelector("[data-tut-back]");
    els.next = root.querySelector("[data-tut-next]");

    // Buttons
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-skip]"), function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); finish(true); });
    });
    els.back.addEventListener("click", function (e) { e.preventDefault(); go(-1); });
    els.next.addEventListener("click", function (e) { e.preventDefault(); advance(); });

    // Clicking the dimmed backdrop (not the card) advances.
    root.addEventListener("click", function (e) {
      if (e.target === root || e.target === els.spot) advance();
    });

    // Reposition on resize/scroll while open.
    window.addEventListener("resize", onReflow, { passive: true });
    window.addEventListener("scroll", onReflow, { passive: true });
  }

  function onReflow() { if (state.open) positionFor(currentTarget()); }

  /* ----------------------------------------------------------
     4. Per-step rendering
     ---------------------------------------------------------- */
  function currentStep() { return STEPS[state.order[state.idx]]; }
  function currentTarget() { return qTarget(currentStep().target); }

  function applyDemo(step) {
    // Optional sample value — sets the field and fires the events the
    // calculator already listens for, so its own logic recomputes.
    if (step.demo && step.demo.sel) {
      try {
        var el = document.querySelector(step.demo.sel);
        if (el && el.value !== step.demo.value) {
          el.value = step.demo.value;
          el.dispatchEvent(new Event("input", { bubbles: true }));
          el.dispatchEvent(new Event("change", { bubbles: true }));
        }
      } catch (e) { /* never break the tool */ }
    }
    // Optional custom action.
    if (typeof step.action === "function") {
      try { step.action({ qTarget: qTarget, document: document }); }
      catch (e) { /* swallow */ }
    }
  }

  function render() {
    var step = currentStep();
    var target = currentTarget();

    // Defensive: if the target vanished, rebuild and bail gracefully.
    if (!target) { buildOrder(); if (!state.order.length) { finish(false); return; } }

    els.count.textContent = "Step " + (state.idx + 1) + " of " + state.order.length;
    els.title.textContent = step.title;
    els.body.textContent = step.body;
    els.avatarText.textContent = step.avatarText || "Avatar explanation will appear here";

    // Future avatar media hook — structure only, no real files required.
    els.avatar.setAttribute("data-has-video", step.videoSrc ? "true" : "false");
    els.avatar.setAttribute("data-has-audio", step.audioSrc ? "true" : "false");

    els.back.disabled = state.idx === 0;
    els.next.textContent = (state.idx === state.order.length - 1) ? "Done" : "Next";

    applyDemo(step);

    // Scroll the target into view, then spotlight it.
    try { target.scrollIntoView({ behavior: "smooth", block: "center" }); } catch (e) {}
    // Wait a tick for smooth-scroll to settle before measuring.
    window.setTimeout(function () { positionFor(currentTarget()); }, 220);
    positionFor(target);
  }

  /* Place the spotlight over the target and the card beside/below it. */
  function positionFor(target) {
    if (!target) return;
    var r = target.getBoundingClientRect();
    var pad = 8;

    // Spotlight box (the dim is a big box-shadow around this rect).
    var s = els.spot.style;
    s.top = (r.top - pad) + "px";
    s.left = (r.left - pad) + "px";
    s.width = (r.width + pad * 2) + "px";
    s.height = (r.height + pad * 2) + "px";

    var card = els.card;
    if (MOBILE()) {
      // Mobile: card docks to the bottom (CSS handles layout).
      card.removeAttribute("style");
      return;
    }

    // Desktop: try right of target, then left, then below.
    var cw = card.offsetWidth || 340;
    var ch = card.offsetHeight || 240;
    var vw = window.innerWidth, vh = window.innerHeight;
    var gap = 18, top, left;

    if (r.right + gap + cw <= vw) {            // right
      left = r.right + gap;
      top = clamp(r.top, 12, vh - ch - 12);
    } else if (r.left - gap - cw >= 0) {       // left
      left = r.left - gap - cw;
      top = clamp(r.top, 12, vh - ch - 12);
    } else if (r.bottom + gap + ch <= vh) {    // below
      top = r.bottom + gap;
      left = clamp(r.left, 12, vw - cw - 12);
    } else {                                   // above
      top = clamp(r.top - gap - ch, 12, vh - ch - 12);
      left = clamp(r.left, 12, vw - cw - 12);
    }

    card.style.position = "fixed";
    card.style.top = Math.round(top) + "px";
    card.style.left = Math.round(left) + "px";
    card.style.right = "auto";
    card.style.bottom = "auto";
  }

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  /* ----------------------------------------------------------
     5. Navigation
     ---------------------------------------------------------- */
  function go(dir) {
    var next = state.idx + dir;
    if (next < 0) return;
    if (next >= state.order.length) { finish(true); return; }
    state.idx = next;
    render();
  }
  function advance() { go(1); }

  function open() {
    buildOverlay();
    buildOrder();
    if (!state.order.length) return;            // nothing to show — stay safe
    state.idx = 0;
    state.open = true;
    state.prevFocus = document.activeElement;
    els.root.hidden = false;
    document.body.classList.add("cmtut-lock");
    document.addEventListener("keydown", onKey, true);
    render();
    window.setTimeout(function () { els.next.focus(); }, 60);
  }

  function finish(completed) {
    state.open = false;
    if (els.root) els.root.hidden = true;
    document.body.classList.remove("cmtut-lock");
    document.removeEventListener("keydown", onKey, true);
    try { if (completed) localStorage.setItem(STORAGE_KEY, "1"); } catch (e) {}
    try { if (state.prevFocus && state.prevFocus.focus) state.prevFocus.focus(); } catch (e) {}
  }

  function onKey(e) {
    if (!state.open) return;
    if (e.key === "Escape") { e.preventDefault(); finish(true); }
    else if (e.key === "ArrowRight") { e.preventDefault(); advance(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
  }

  /* ----------------------------------------------------------
     6. Wire the launch button(s). The button is always available
        so visitors can replay the tour any time.
     ---------------------------------------------------------- */
  function wireLaunchers() {
    var done = false;
    try { done = localStorage.getItem(STORAGE_KEY) === "1"; } catch (e) {}
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-tutorial-launch]"),
      function (btn) {
        if (!done) btn.classList.add("tut-launch--new"); // gentle nudge first time
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          btn.classList.remove("tut-launch--new");
          open();
        });
      }
    );
  }

  // Expose a tiny API for future hooks (e.g. auto-start, deep links).
  window.CMTutorial = { open: open, close: function () { finish(false); }, steps: STEPS };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireLaunchers);
  } else {
    wireLaunchers();
  }
})();
