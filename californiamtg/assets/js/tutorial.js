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
      demo: { sel: "#hs-q", value: "90210", silent: true },
      avatarText: "Your Financial Navigator — a quick intro to how this tool works.",
      videoSrc: "/assets/video/avatar/intro.mp4", audioSrc: null
    },
    {
      target: "county-limit",
      title: "Understand County Loan Limits",
      body: "Every county has a cut-off loan amount. Stay under it and your loan is a regular “conforming” loan. Go over it and it becomes a bigger “jumbo” loan. This bar shows where your loan sits versus that line.",
      videoSrc: "/assets/video/avatar/step-county.mp4", audioSrc: null,
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "property-value",
      title: "Purchase Price vs. Loan Amount",
      body: "Drag this to the home's price (for a purchase) or its current value (for a refinance). Most other numbers update from this one.",
      demo: { sel: "#hs-value", value: "1600000" },
      videoSrc: "/assets/video/avatar/step-value.mp4", audioSrc: null,
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "loan-purpose",
      title: "What you're trying to do",
      body: "Buying a home, refinancing, pulling cash out, or financing a rental? Pick the goal and the tool shows only the fields that matter for it.",
      videoSrc: "/assets/video/avatar/step-purpose.mp4", audioSrc: null,
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "down-payment",
      title: "Down Payment Strategy",
      body: "This is the cash you put in up front. Putting down 20% or more usually removes monthly mortgage insurance (PMI), which lowers your payment.",
      demo: { sel: "#hs-down", value: "20" },
      videoSrc: "/assets/video/avatar/step-down.mp4", audioSrc: null,
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "fico",
      title: "Credit Score Impact",
      body: "A higher score usually means a lower interest rate. Slide it and watch the assumed rate and payment change. 740 and up is already strong.",
      demo: { sel: "#hs-score", value: "760" },
      videoSrc: "/assets/video/avatar/step-fico.mp4", audioSrc: null,
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "income-type",
      title: "How your income is evaluated",
      body: "Not all income is reviewed the same way. W-2, self-employed, 1099, and business owners may each need different documentation and calculations. Identifying the right category is key to an accurate strategy — the goal is understanding how your income may be evaluated for qualification, not just how much you earn.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "income",
      title: "Qualifying income vs. gross income",
      body: "Gross income and qualifying income aren't always the same. Lenders apply underwriting guidelines — business expenses, deductions, rental income, self-employment history, and documentation can all change the final number. The more accurately we evaluate income, the more accurate your financing strategy becomes.",
      demo: { sel: "#hs-income", value: "180000" },
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "result",
      title: "Conforming vs. jumbo result",
      body: "Bringing it all together — location, loan amount, down payment, credit, and income — some scenarios fit conforming or high-balance conforming, others require jumbo. Neither is automatically better. The goal isn't simply to get a loan, it's to identify the most efficient financing structure for your situation.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "payment-strategy",
      title: "Payment strategy",
      body: "Monthly payment is a major factor, but it's part of a broader picture. Rates, terms, down payment, and loan structure all shape the final obligation. The lowest payment isn't always best, and the highest isn't always necessary — the aim is a payment that supports both qualification and your long-term goals.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "buydown",
      title: "Buydowns & points",
      body: "Paying points at closing can lower your rate, and temporary buydowns can reduce payments in the early years. Every buydown has a cost, so we compare the upfront investment against the long-term benefit. Sometimes it creates meaningful savings; sometimes keeping those funds available is the better move.",
      avatarText: "Avatar explanation will appear here"
    },
    {
      target: "interest-only",
      title: "Interest-only financing",
      body: "Interest-only payments cover interest without reducing principal for a set period, creating lower payments and improved cash flow. That flexibility is valuable for some, but it isn't right for everyone. Used appropriately it's an effective planning tool; misunderstood it can create unrealistic expectations — so we compare all options before deciding.",
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
  // Shared still image for the avatar when a step has no video clip.
  // Drop a file here to use it; if it is missing a neutral placeholder shows.
  var AVATAR_IMG = "/assets/video/avatar/navigator.jpg";
  var MOBILE = function () { return window.matchMedia("(max-width: 760px)").matches; };

  /* Are we running inside the homepage iframe embed? If so, the parent
     page owns the scrollbar, so we drive it through a postMessage bridge
     (see the matching handler in the homepage). When standalone, we use
     normal in-page scrolling. */
  var EMBEDDED = (function () { try { return window.top !== window.self; } catch (e) { return true; } })();
  var viewport = { iframeTop: 0, parentH: 640 }; // updated by the parent while embedded

  /* ----------------------------------------------------------
     2. State + element refs (built lazily)
     ---------------------------------------------------------- */
  var state = { idx: 0, order: [], open: false, prevFocus: null };
  var els = {};
  var brokenImg = {}; // remembers avatar image srcs that failed to load

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
    if (EMBEDDED) root.classList.add("cmtut--embed");

    root.innerHTML =
      '<div class="cmtut__spot" data-tut-spot></div>' +
      '<div class="cmtut__card" data-tut-card>' +
        // LEFT — avatar / video
        '<div class="cmtut__media" data-tut-media>' +
          '<div class="cmtut__media-ph" data-tut-ph aria-hidden="true">' +
            '<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true">' +
              '<circle cx="32" cy="24" r="12" fill="rgba(255,255,255,.85)"/>' +
              '<path d="M12 58c0-12 9-19 20-19s20 7 20 19Z" fill="rgba(255,255,255,.85)"/>' +
            '</svg>' +
          '</div>' +
          '<img class="cmtut__img" data-tut-img alt="" />' +
          '<video class="cmtut__video" data-tut-video playsinline preload="metadata"></video>' +
          '<span class="cmtut__badge"><i></i>Financial Navigator</span>' +
          '<button type="button" class="cmtut__mute" data-tut-mute aria-label="Unmute" hidden>&#128263;</button>' +
          '<div class="cmtut__media-foot">Your Financial Navigator</div>' +
        '</div>' +
        // RIGHT — text + controls
        '<div class="cmtut__panel">' +
          '<button type="button" class="cmtut__close" data-tut-skip aria-label="Close tutorial">&#215;</button>' +
          '<p class="cmtut__step" data-tut-count>Step 1 of 1</p>' +
          '<h3 class="cmtut__title" data-tut-title></h3>' +
          '<span class="cmtut__rule" aria-hidden="true"></span>' +
          '<p class="cmtut__body" data-tut-body></p>' +
          '<div class="cmtut__nav">' +
            '<button type="button" class="cmtut__btn cmtut__btn--skip" data-tut-skip>Skip</button>' +
            '<div class="cmtut__nav-right">' +
              '<button type="button" class="cmtut__btn cmtut__btn--back" data-tut-back>Back</button>' +
              '<button type="button" class="cmtut__btn cmtut__btn--next" data-tut-next>' +
                '<span data-tut-nextlabel>Next</span>' +
                '<svg class="cmtut__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5.5 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';

    document.body.appendChild(root);

    els.root = root;
    els.spot = root.querySelector("[data-tut-spot]");
    els.card = root.querySelector("[data-tut-card]");
    els.media = root.querySelector("[data-tut-media]");
    els.ph = root.querySelector("[data-tut-ph]");
    els.img = root.querySelector("[data-tut-img]");
    els.video = root.querySelector("[data-tut-video]");
    els.mute = root.querySelector("[data-tut-mute]");
    els.count = root.querySelector("[data-tut-count]");
    els.title = root.querySelector("[data-tut-title]");
    els.body = root.querySelector("[data-tut-body]");
    els.back = root.querySelector("[data-tut-back]");
    els.next = root.querySelector("[data-tut-next]");
    els.nextLabel = root.querySelector("[data-tut-nextlabel]");

    // Buttons
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-skip]"), function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); finish(true); });
    });
    els.back.addEventListener("click", function (e) { e.preventDefault(); go(-1); });
    els.next.addEventListener("click", function (e) { e.preventDefault(); advance(); });

    // Mute / unmute toggle (only relevant for clips with sound).
    els.mute.addEventListener("click", function (e) {
      e.preventDefault();
      els.video.muted = !els.video.muted;
      els.mute.innerHTML = els.video.muted ? "&#128263;" : "&#128266;";
      els.mute.setAttribute("aria-label", els.video.muted ? "Unmute" : "Mute");
      if (!els.video.muted) { try { els.video.play(); } catch (e2) {} }
    });
    // If the clip is wrong/missing, fall back to the avatar image silently.
    els.video.addEventListener("error", function () { showLayer("img"); els.mute.hidden = true; });
    // If the image is also missing, remember it and show the placeholder
    // (caching avoids re-requesting a 404 on every step).
    els.img.addEventListener("error", function () {
      if (els.img.getAttribute("src")) brokenImg[els.img.getAttribute("src")] = true;
      showLayer("ph");
    });

    // Reposition on resize/scroll while open.
    window.addEventListener("resize", onReflow, { passive: true });
    window.addEventListener("scroll", onReflow, { passive: true });

    // Embed bridge: the parent feeds us its visible viewport, and (when the
    // card is hosted on the page) relays Next/Back/Skip clicks back to us.
    window.addEventListener("message", function (e) {
      var d = e && e.data; if (!d) return;
      if (d.cmTut === "viewport") {
        viewport.iframeTop = typeof d.iframeTop === "number" ? d.iframeTop : viewport.iframeTop;
        viewport.parentH = d.parentH || viewport.parentH;
        if (state.open) positionFor(currentTarget());
      } else if (d.cmTut === "nav") {
        if (!state.open) return;
        if (d.dir === "next") advance();
        else if (d.dir === "back") go(-1);
        else if (d.dir === "skip") finish(true);
      }
    });
  }

  function onReflow() { if (state.open) positionFor(currentTarget()); }

  /* ----------------------------------------------------------
     4. Per-step rendering
     ---------------------------------------------------------- */
  function currentStep() { return STEPS[state.order[state.idx]]; }
  function currentTarget() { return qTarget(currentStep().target); }

  function applyDemo(step) {
    // Optional sample value — sets the field and (unless silent) fires the
    // events the calculator listens for so it recomputes. The ZIP field is
    // set "silent": firing input there would collapse the example scenario
    // (the engine hides everything below ZIP until a county is confirmed).
    if (step.demo && step.demo.sel) {
      try {
        var el = document.querySelector(step.demo.sel);
        if (el && el.value !== step.demo.value) {
          el.value = step.demo.value;
          if (!step.demo.silent) {
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
          }
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

    var last = state.idx === state.order.length - 1;

    if (EMBEDDED) {
      // Card is hosted on the page (off the calculator frame); send it data.
      postStep(step, last);
    } else {
      els.count.textContent = "Step " + (state.idx + 1) + " of " + state.order.length;
      els.title.textContent = step.title;
      els.body.textContent = step.body;
      loadStepMedia(step);                 // video → image → placeholder
      els.back.disabled = state.idx === 0;
      els.nextLabel.textContent = last ? "Done" : "Next";
      els.next.classList.toggle("is-done", last);
    }

    applyDemo(step);

    // Scroll the field into a spot that leaves it visible next to the card.
    var r = target.getBoundingClientRect();
    var place = EMBEDDED ? "host" : sideFor(r, els.card.offsetWidth || 560, window.innerWidth);
    var frac = MOBILE() ? 0.3 : (place === "host" ? 0.42 : (place === "stack" ? 0.28 : 0.5));
    scrollTargetTo(r, frac);
    positionFor(target);
    // Re-measure after the smooth scroll settles.
    window.setTimeout(function () { positionFor(currentTarget()); }, 280);
  }

  // Tell the page-hosted card which step to show (embedded mode only).
  function postStep(step, last) {
    try {
      window.parent.postMessage({
        cmTut: "step",
        idx: state.idx, total: state.order.length,
        title: step.title, body: step.body,
        videoSrc: step.videoSrc || null,
        imageSrc: step.imageSrc || AVATAR_IMG || null,
        first: state.idx === 0, last: !!last
      }, "*");
    } catch (e) {}
  }

  /* Where does the card fit relative to the field without covering it? */
  function sideFor(r, cw, vw) {
    if (MOBILE()) return "stack";
    if (r.right + 22 + cw <= vw) return "right";
    if (r.left - 22 - cw >= 0) return "left";
    return "stack";
  }

  /* Scroll so the field's center sits at `frac` of the visible height. */
  function scrollTargetTo(r, frac) {
    if (EMBEDDED) {
      try { window.parent.postMessage({ cmTut: "scrollTo", y: r.top + r.height / 2, frac: frac }, "*"); } catch (e) {}
    } else {
      try {
        var delta = (r.top + r.height / 2) - window.innerHeight * frac;
        window.scrollBy({ top: delta, behavior: "smooth" });
      } catch (e) { try { r && null; } catch (e2) {} }
    }
  }

  /* The vertical band (in the SAME coordinate space as getBoundingClientRect
     and our fixed-positioned overlay) that the user can currently see.
       • Standalone: the whole window viewport.
       • Embedded: the slice of the studio visible inside the parent page. */
  function getBand() {
    if (!EMBEDDED) return { top: 0, bottom: window.innerHeight };
    var top = Math.max(0, -viewport.iframeTop);
    var bottom = viewport.parentH - viewport.iframeTop;
    var contentH = document.documentElement.scrollHeight;
    if (bottom > contentH) bottom = contentH;
    if (bottom - top < 160) {                 // viewport not ready / tiny sliver
      var h = Math.min(viewport.parentH || 640, 640);
      return { top: top, bottom: top + h };
    }
    return { top: top, bottom: bottom };
  }

  /* ---- Avatar media (video → image → placeholder) ----
     Each step may set videoSrc and/or imageSrc; otherwise the shared
     AVATAR_IMG still is used, and if that is missing too a neutral
     placeholder shows. Nothing here can throw or stall the tour. */
  function showLayer(which) {
    if (els.video) els.video.style.display = which === "video" ? "block" : "none";
    if (els.img) els.img.style.display = which === "img" ? "block" : "none";
    if (els.ph) els.ph.style.display = which === "ph" ? "flex" : "none";
  }

  function loadStepMedia(step) {
    var v = els.video, img = els.img;
    try { if (v) v.pause(); } catch (e) {}
    if (els.mute) els.mute.hidden = true;

    var imgSrc = step.imageSrc || AVATAR_IMG;

    function tryImage() {
      if (!img || !imgSrc || brokenImg[imgSrc]) { showLayer("ph"); return; }
      if (img.getAttribute("src") !== imgSrc) img.setAttribute("src", imgSrc);
      // 'load' shows img; 'error' (wired in buildOverlay) falls to placeholder.
      if (img.complete && img.naturalWidth > 0) showLayer("img");
      else { showLayer("ph"); img.onload = function () { showLayer("img"); }; }
    }

    if (step.videoSrc && v) {
      if (v.getAttribute("src") !== step.videoSrc) {
        v.setAttribute("src", step.videoSrc);
        try { v.load(); } catch (e) {}
      }
      if (imgSrc && img) v.setAttribute("poster", imgSrc);
      v.muted = true;
      if (els.mute) {
        els.mute.hidden = false;
        els.mute.innerHTML = "&#128263;";
        els.mute.setAttribute("aria-label", "Unmute");
      }
      showLayer("video");
      var p = v.play();
      if (p && typeof p.catch === "function") p.catch(function () {/* autoplay blocked: poster stays */});
    } else {
      if (v) { v.removeAttribute("src"); try { v.load(); } catch (e) {} }
      tryImage();
    }
  }

  /* Glow the target and center the wide card over the calculator, nudging
     it to the band half opposite the target so the field stays peeking. */
  function positionFor(target) {
    if (!target) return;
    var r = target.getBoundingClientRect();
    var pad = 7;

    // Subtle gold glow ring around the active field.
    var s = els.spot.style;
    s.top = (r.top - pad) + "px";
    s.left = (r.left - pad) + "px";
    s.width = (r.width + pad * 2) + "px";
    s.height = (r.height + pad * 2) + "px";

    // Embedded: the card lives on the page, so we only place the glow here.
    if (EMBEDDED) return;

    var card = els.card;
    var band = getBand();
    var bandH = band.bottom - band.top;
    var ch = card.offsetHeight || 320;
    var cw = card.offsetWidth || 560;
    var vw = window.innerWidth;
    var gap = 18;

    card.style.position = "fixed";
    card.style.right = "auto";
    card.style.bottom = "auto";

    if (MOBILE()) {
      // Card docks to the bottom; the field is scrolled high above it.
      card.style.left = "10px";
      card.style.right = "10px";
      card.style.width = "auto";
      card.style.top = Math.round(Math.max(band.top + 8, band.bottom - ch - 10)) + "px";
      return;
    }
    card.style.width = "";

    var place = sideFor(r, cw, vw);
    var left, top;

    if (place === "right" || place === "left") {
      // Beside the field — horizontal separation means it never covers it.
      left = (place === "right") ? r.right + gap : r.left - gap - cw;
      top = clamp(r.top + r.height / 2 - ch / 2, band.top + 12, Math.max(band.top + 12, band.bottom - ch - 12));
    } else {
      // Stacked — sit fully below the field (or above if no room below).
      left = clamp(Math.round((vw - cw) / 2), 12, Math.max(12, vw - cw - 12));
      if (r.bottom + gap + ch <= band.bottom - 8) {
        top = r.bottom + gap;                         // below, field visible above
      } else if (r.top - gap - ch >= band.top + 8) {
        top = r.top - gap - ch;                       // above, field visible below
      } else {
        top = clamp(band.bottom - ch - 12, band.top + 12, Math.max(band.top + 12, band.bottom - ch - 12));
      }
    }

    card.style.left = Math.round(clamp(left, 12, Math.max(12, vw - cw - 12))) + "px";
    card.style.top = Math.round(top) + "px";
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
    if (EMBEDDED) {
      try { window.parent.postMessage({ cmTut: "open" }, "*"); } catch (e) {}
      try { window.parent.postMessage({ cmTut: "needViewport" }, "*"); } catch (e) {}
    }
    render();
    // Trigger the fade/slide-in on the next frame.
    requestAnimationFrame(function () { els.root.classList.add("cmtut--in"); });
    window.setTimeout(function () { try { els.next.focus(); } catch (e) {} }, 80);
  }

  function finish(completed) {
    state.open = false;
    if (els.video) { try { els.video.pause(); } catch (e) {} }
    if (els.root) {
      els.root.classList.remove("cmtut--in");
      // Hide after the exit transition so it fades out gracefully.
      window.setTimeout(function () { if (!state.open && els.root) els.root.hidden = true; }, 260);
    }
    document.body.classList.remove("cmtut-lock");
    document.removeEventListener("keydown", onKey, true);
    if (EMBEDDED) { try { window.parent.postMessage({ cmTut: "close" }, "*"); } catch (e) {} }
    try { if (completed) localStorage.setItem(STORAGE_KEY, "1"); } catch (e) {}
    try { if (state.prevFocus && state.prevFocus.focus) state.prevFocus.focus(); } catch (e) {}
  }

  function onKey(e) {
    if (!state.open) return;
    if (e.key === "Escape") { e.preventDefault(); finish(true); }
    else if (e.key === "ArrowRight") { e.preventDefault(); advance(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    else if (e.key === "Tab") { trapFocus(e); }   // keep focus inside the modal
  }

  // Simple focus trap across the modal's focusable controls.
  function trapFocus(e) {
    if (!els.card) return;
    var f = els.card.querySelectorAll(
      'button:not([disabled]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1], a = document.activeElement;
    if (e.shiftKey && (a === first || !els.card.contains(a))) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && a === last) { e.preventDefault(); first.focus(); }
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
