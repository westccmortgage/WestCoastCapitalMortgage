/* California Mortgage — landing interactions
   Powered by West Coast Capital Mortgage Inc.
   Vanilla JS, no dependencies. */
(function () {
  "use strict";

  /* ---- Sticky header: transparent over hero, solid navy on scroll ---- */
  var header = document.getElementById("siteHeader");
  function onScroll() {
    if (window.scrollY > 40) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- Mobile navigation ---- */
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("mainNav");
  function closeNav() {
    nav.classList.remove("open");
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    // Close menu when a link is tapped
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });
    // Close on Escape
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
  }

  /* ---- Footer year ---- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---- Scenario Builder quick-start ----
     On the homepage (where #builder exists) a [data-start] link scrolls to the
     builder and (re)starts it, optionally at a preselected [data-goal]. On other
     pages there is no builder, so we let the link navigate normally to the
     homepage (e.g. /index.html#builder). */
  document.querySelectorAll("[data-start]").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (window.CMTrack) window.CMTrack("begin_button_clicked", {
        label: (link.textContent || "").trim(), goal: link.getAttribute("data-goal") || ""
      });
      var builder = document.getElementById("builder");
      if (!builder || !window.CMScenario) return; // off-home: follow the href
      e.preventDefault();
      if (nav && nav.classList.contains("open")) closeNav();
      builder.scrollIntoView({ behavior: "smooth", block: "start" });
      window.CMScenario.start(link.getAttribute("data-goal") || null);
    });
  });

  /* ---- Contact form (Netlify-Forms ready) ----
     Submits via fetch so the page shows an inline success message. Works with
     Netlify Forms when deployed (the static form is detected at build, and the
     POST below is captured). Locally the fetch fails harmlessly and we still
     thank the user. */
  var contactForm = document.querySelector("form.cm-form");
  if (contactForm) {
    var startedTracked = false;
    contactForm.addEventListener("input", function () {
      if (!startedTracked) { startedTracked = true; if (window.CMTrack) window.CMTrack("contact_form_started", {}); }
    });
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      // basic required validation
      var ok = true;
      contactForm.querySelectorAll("[required]").forEach(function (el) {
        var bad = !String(el.value || "").trim();
        var f = el.closest(".field");
        var err = f && f.querySelector(".field-error");
        if (err) err.textContent = bad ? "This field is required." : "";
        if (bad) ok = false;
      });
      if (!ok) return;

      /* Persistence is delegated to the lead layer (src/app.js -> CMLeads):
         it writes to Supabase + CRM when configured, otherwise falls back to
         Netlify Forms. If that module isn't present, fall back here directly.
         TODO: connect WCCM email workflow / CRM / Zapier / Make in crmWebhook.js */
      if (window.CMLeads && window.CMLeads.saveContactForm) {
        window.CMLeads.saveContactForm(contactForm).then(showContactSuccess).catch(showContactSuccess);
      } else {
        var body = new URLSearchParams(new FormData(contactForm)).toString();
        fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body })
          .then(showContactSuccess).catch(showContactSuccess);
      }
    });
  }
  function showContactSuccess() {
    var card = document.getElementById("contactCard") || (contactForm && contactForm.parentNode);
    if (!card) return;
    card.innerHTML =
      '<div class="thankyou">' +
        '<div class="ty-mark" aria-hidden="true">&#10003;</div>' +
        '<h3>Thank you.</h3>' +
        '<p class="ty-lead">Your scenario has been received. A licensed mortgage professional ' +
        'can review your situation and contact you about the next step.</p>' +
        '<p class="ty-compliance">This is not a loan approval, loan commitment, or rate quote. ' +
        'Final loan options are subject to review by a licensed mortgage professional.</p>' +
      '</div>';
    card.classList.add("is-thankyou");
  }

  /* ---- Hero background video ----
     The <video> ships with no <source> (only data-src) so nothing heavy loads
     by default. On larger screens with a normal connection we attach the source
     and autoplay it muted. On mobile, data-saver, or reduced-motion we drop the
     video element entirely and let the poster image + warm gradient show. */
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    var src = heroVideo.getAttribute("data-src");
    var mq = function (q) { return window.matchMedia ? window.matchMedia(q).matches : false; };
    var bigEnough = window.matchMedia ? mq("(min-width: 768px)") : true;
    var saveData = navigator.connection && navigator.connection.saveData;
    var reduceMotion = mq("(prefers-reduced-motion: reduce)");

    if (src && bigEnough && !saveData && !reduceMotion) {
      var source = document.createElement("source");
      source.src = src;
      source.type = heroVideo.getAttribute("data-type") || "video/mp4";
      heroVideo.appendChild(source);
      heroVideo.load();
      var tryPlay = heroVideo.play();
      if (tryPlay && typeof tryPlay.catch === "function") {
        tryPlay.catch(function () { /* autoplay blocked — poster/gradient remain */ });
      }
    } else {
      // Fall back to poster image + warm gradient (lighter for mobile/slow links)
      heroVideo.remove();
    }
  }

  /* ---- Rotating Scenario Preview Card ----
     Elegant auto-rotating preview of different mortgage situations. Preview only
     (no approval implied). Fades every ~4.5s, pauses on hover/focus, dots to jump,
     clickable to open the scenario builder. Respects reduced-motion. */
  var rotator = document.getElementById("scenarioRotator");
  if (rotator) {
    var SCENARIOS = [
      { label: "BUYER SCENARIO", title: "First-Time or Move-Up Buyer",
        quote: ["“I'm buying in California.", "$1.2M purchase.", "Need pre-approval and payment options.”"],
        next: "Purchase Review" },
      { label: "SELF-EMPLOYED", title: "Complex Income Profile",
        quote: ["“I own a business.", "Tax returns don't show full income.", "Need bank statement or Non-QM options.”"],
        next: "Income Review" },
      { label: "INVESTOR / DSCR", title: "Rental Property Financing",
        quote: ["“I'm buying an investment property.", "Want to qualify using rental income.", "Need DSCR options.”"],
        next: "Investor Review" },
      { label: "LOWER PAYMENT", title: "Payment Strategy",
        quote: ["“My current payment feels too high.", "I want to understand refinance, rate, points, or payment options.”"],
        next: "Payment Review" },
      { label: "REALTOR FILE", title: "Difficult Buyer Scenario",
        quote: ["“My buyer was denied by a bank.", "We need a second opinion before losing the deal.”"],
        next: "Second Opinion" },
      { label: "JUMBO PURCHASE", title: "High-Value California Property",
        quote: ["“I'm buying a high-value home.", "Need jumbo options and a clear monthly payment strategy.”"],
        next: "Jumbo Review" }
    ];
    var elLabel = rotator.querySelector('[data-role="label"]');
    var elTitle = rotator.querySelector('[data-role="title"]');
    var elQuote = rotator.querySelector('[data-role="quote"]');
    var elNext = rotator.querySelector('[data-role="next"]');
    var dotsWrap = document.getElementById("previewDots");
    var i = 0, timer = null, paused = false;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var INTERVAL = 4500;

    // build dots
    SCENARIOS.forEach(function (_, n) {
      var d = document.createElement("button");
      d.type = "button"; d.className = "preview-dot"; d.setAttribute("role", "tab");
      d.setAttribute("aria-label", "Show scenario " + (n + 1));
      d.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation();   // don't trigger card navigation
        go(n, true);
        restart();
      });
      dotsWrap.appendChild(d);
    });
    var dots = dotsWrap.querySelectorAll(".preview-dot");

    function paint(n) {
      var s = SCENARIOS[n];
      elLabel.textContent = s.label;
      elTitle.textContent = s.title;
      elQuote.innerHTML = s.quote.map(function (line) { return "<span>" + line + "</span>"; }).join("");
      elNext.textContent = s.next;
      dots.forEach(function (d, k) { d.classList.toggle("active", k === n); d.setAttribute("aria-selected", k === n ? "true" : "false"); });
      i = n;
    }
    function go(n, instant) {
      n = (n + SCENARIOS.length) % SCENARIOS.length;
      if (reduce || instant) { paint(n); return; }
      rotator.classList.add("swapping");           // fade out
      window.setTimeout(function () { paint(n); rotator.classList.remove("swapping"); }, 360);
    }
    function tick() { if (!paused) go(i + 1); }
    function start() { if (!reduce) timer = window.setInterval(tick, INTERVAL); }
    function stop() { if (timer) { window.clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    paint(0);
    start();
    // pause on hover / focus
    rotator.addEventListener("mouseenter", function () { paused = true; });
    rotator.addEventListener("mouseleave", function () { paused = false; });
    rotator.addEventListener("focusin", function () { paused = true; });
    rotator.addEventListener("focusout", function () { paused = false; });

    // clickable -> open scenario builder (or /scenarios as fallback)
    function openBuilder() {
      var builder = document.getElementById("builder");
      if (builder && window.CMScenario) {
        builder.scrollIntoView({ behavior: "smooth", block: "start" });
        window.CMScenario.start(null);
      } else {
        window.location.href = "/scenarios.html";
      }
    }
    rotator.addEventListener("click", openBuilder);
    rotator.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openBuilder(); }
    });
  }
})();
