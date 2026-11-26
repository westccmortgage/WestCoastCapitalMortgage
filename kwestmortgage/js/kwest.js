/* ============================================================
   K West Mortgage — Site behavior
   Nav, scenario rotation, scroll reveal, accordion,
   forms (webhook/email ready), cookie consent + visitor ID.
   ============================================================ */
(function () {
  "use strict";

  /* ---------------- Config ----------------
     Set FORM_ENDPOINT to your webhook / Netlify function / Zapier URL
     to start capturing leads. Until set, submissions are stored
     locally and the success message still shows.                     */
  var CONFIG = {
    FORM_ENDPOINT: "", // e.g. "/.netlify/functions/lead" or a webhook URL
    BRAND: "K West Mortgage"
  };

  /* ---------------- Helpers ---------------- */
  function $(s, ctx) { return (ctx || document).querySelector(s); }
  function $all(s, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(s)); }
  function uid() { return "kw_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 9); }

  /* ---------------- Header scroll state ---------------- */
  var header = $(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 12); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------------- Mobile nav ----------------
     Scroll lock lives on <html> only (html.menu-open); locking <body> as well
     breaks position:sticky. Closes on Esc, link click, outside tap, and when the
     viewport grows past the 1240px breakpoint. */
  var toggle = $(".nav__toggle"), menu = $(".mobile-menu");
  if (toggle && menu) {
    var root = document.documentElement;
    var LBL = { en: ["Open menu", "Close menu"], es: ["Abrir men\u00fa", "Cerrar men\u00fa"], pt: ["Abrir menu", "Fechar menu"] };
    var lblFor = function () {
      var l = (root.getAttribute("lang") || "en").toLowerCase().slice(0, 2);
      return LBL[l] || LBL.en;
    };
    var setMenu = function (open, returnFocus) {
      menu.classList.toggle("open", open);
      toggle.classList.toggle("open", open);
      root.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", lblFor()[open ? 1 : 0]);
      if (!open && returnFocus) toggle.focus();
    };
    toggle.addEventListener("click", function () { setMenu(!menu.classList.contains("open")); });
    $all("a", menu).forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if ((e.key === "Escape" || e.key === "Esc") && menu.classList.contains("open")) setMenu(false, true);
    });
    document.addEventListener("click", function (e) {
      if (!menu.classList.contains("open")) return;
      if (menu.contains(e.target) || toggle.contains(e.target)) return;
      setMenu(false);
    });
    var closeIfWide = function () { if (window.innerWidth > 1240) setMenu(false); };
    window.addEventListener("resize", closeIfWide);
    window.addEventListener("orientationchange", closeIfWide);
  }

  /* ---------------- Wide tables: "swipe" hint only while they really overflow ---------------- */
  $all(".limits-scroll, .compare-wrap, .table-wrap, [data-swipe]").forEach(function (wrap) {
    var hint = document.createElement("p");
    hint.className = "swipe-hint";
    hint.hidden = true;
    hint.setAttribute("aria-hidden", "true");
    hint.textContent = "Swipe to see more \u2192";
    wrap.parentNode.insertBefore(hint, wrap);
    var update = function () {
      var overflows = wrap.scrollWidth > wrap.clientWidth + 2;
      var atEnd = wrap.scrollLeft + wrap.clientWidth >= wrap.scrollWidth - 2;
      hint.hidden = !overflows || atEnd;
    };
    wrap.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    window.addEventListener("load", update);
    update();
  });

  /* ---------------- Scroll reveal ---------------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    $all(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $all(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------------- Rotating scenario card ---------------- */
  var stage = $("[data-scenarios]");
  if (stage) {
    var scenarios = [
      { q: "“I’m buying in Key West at $1.15M with 20% down. Do I really need jumbo?”", next: "High-Balance Review", href: "jumbo-vs-conforming.html" },
      { q: "“I’m self-employed and buying a second home in Key West.”", next: "Self-Employed / Second Home Review", href: "loan-options.html" },
      { q: "“I’m buying an investment property in the Florida Keys and want to compare DSCR vs conventional.”", next: "Investor Review", href: "loan-options.html" },
      { q: "“I’m a veteran buying in Monroe County. Can VA work in Key West?”", next: "VA Review", href: "loan-options.html" }
    ];
    var quoteEl = $(".scenario-card .quote", stage);
    var nextEl = $(".scenario-card .next span", stage);
    var nextLink = $(".scenario-card .next", stage);
    var dotsWrap = $(".scenario-dots", stage);
    var idx = 0, timer;

    scenarios.forEach(function (_, i) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("aria-label", "Scenario " + (i + 1));
      b.addEventListener("click", function () { show(i); reset(); });
      dotsWrap.appendChild(b);
    });
    var dots = $all("button", dotsWrap);

    function show(i) {
      idx = i;
      quoteEl.classList.remove("show");
      window.setTimeout(function () {
        quoteEl.textContent = scenarios[i].q;
        nextEl.textContent = scenarios[i].next;
        if (nextLink) nextLink.setAttribute("href", scenarios[i].href);
        quoteEl.classList.add("show");
      }, 180);
      dots.forEach(function (d, di) { d.classList.toggle("active", di === i); });
    }
    function advance() { show((idx + 1) % scenarios.length); }
    function reset() { window.clearInterval(timer); timer = window.setInterval(advance, 5200); }
    show(0); reset();
  }

  /* ---------------- Accordion ---------------- */
  $all(".acc-head").forEach(function (head) {
    head.addEventListener("click", function () {
      var item = head.closest(".acc-item");
      var body = $(".acc-body", item);
      var open = item.classList.toggle("open");
      body.style.maxHeight = open ? body.scrollHeight + "px" : null;
      head.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* ---------------- Visitor ID (first-party, consent-gated) ---------------- */
  function ensureVisitorId() {
    try {
      if (localStorage.getItem("kw_consent") !== "granted") return null;
      var id = localStorage.getItem("kw_visitor_id");
      if (!id) { id = uid(); localStorage.setItem("kw_visitor_id", id); }
      return id;
    } catch (e) { return null; }
  }

  /* ---------------- Microsoft Clarity (loads only after consent) ----------------
     The tag is NOT part of the page: it is injected here once kw_consent is "granted"
     (on Accept, and on later page loads when consent was already given). */
  var CLARITY_ID = "x8m07mb7jq";
  function clarityConsent(state) {
    try {
      if (typeof window.clarity === "function") window.clarity("consentv2", { ad_Storage: state, analytics_Storage: state });
    } catch (e) {}
  }
  function loadClarity() {
    try {
      if (localStorage.getItem("kw_consent") !== "granted") return;
      if (!document.querySelector('script[src*="clarity.ms/tag/"]')) {
        (function (c, l, a, r, i, t, y) {
          c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
          t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
          y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
        })(window, document, "clarity", "script", CLARITY_ID);
      }
      clarityConsent("granted");
    } catch (e) {}
  }

  /* ---------------- Cookie consent ---------------- */
  var bar = $(".cookie-bar");
  if (bar) {
    var stored;
    try { stored = localStorage.getItem("kw_consent"); } catch (e) { stored = null; }
    if (!stored) { window.setTimeout(function () { bar.classList.add("show"); }, 900); }
    var setConsent = function (val) {
      try { localStorage.setItem("kw_consent", val); } catch (e) {}
      bar.classList.remove("show");
      if (val === "granted") { ensureVisitorId(); loadClarity(); }
      else clarityConsent("denied");
    };
    var acc = $("[data-consent-accept]", bar), dec = $("[data-consent-decline]", bar);
    if (acc) acc.addEventListener("click", function () { setConsent("granted"); });
    if (dec) dec.addEventListener("click", function () { setConsent("declined"); });
  }
  ensureVisitorId();
  loadClarity();

  /* ---------------- Netlify Forms (AJAX submit) ----------------
     Forms stay as real Netlify forms in the HTML (data-netlify="true" +
     hidden form-name + honeypot) so Netlify detects them at deploy and the
     native POST still works with JS disabled. With JS on, we submit via a
     urlencoded fetch POST to "/" (the most reliable Netlify method on
     statically-hosted sites), then redirect to the thank-you page. */
  $all('form[data-netlify]').forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      // Let the browser enforce required fields and the phone pattern first.
      if (typeof form.reportValidity === "function" && !form.reportValidity()) return;
      if (form.dataset.kwestSending === "true") return; // one POST per submit
      form.dataset.kwestSending = "true";

      var btn = $("button[type=submit]", form);
      var redirect = form.getAttribute("action") || "/thank-you.html";

      // Build url-encoded body from the form (includes hidden form-name + bot-field).
      var data = new FormData(form);
      var encoded = new URLSearchParams();
      data.forEach(function (value, key) { encoded.append(key, value); });
      // Guarantee form-name is present even if the hidden field is ever missing.
      if (!encoded.has("form-name")) {
        encoded.append("form-name", form.getAttribute("name") || "key-west-scenario-review");
      }

      if (btn) { btn.dataset.label = btn.textContent; btn.disabled = true; btn.textContent = "Sending\u2026"; }

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: encoded.toString()
      }).then(function (res) {
        if (!res.ok) throw new Error("Bad status " + res.status);
        window.location.href = redirect;
      }).catch(function () {
        form.dataset.kwestSending = "false";
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Submit"; }
        var n = form.querySelector("[data-kwest-submit-error]");
        if (!n) { n = document.createElement("p"); n.setAttribute("data-kwest-submit-error", ""); n.setAttribute("role", "alert"); form.appendChild(n); }
        n.textContent = "Your request could not be sent. Please try again or call ";
        var tel = document.createElement("a"); tel.href = "tel:+13106541577"; tel.textContent = "(310) 654-1577";
        n.appendChild(tel); n.appendChild(document.createTextNode("."));
      });
    });
  });

  /* ---------------- Hero video ---------------- */
  /* Phones (<= 760px) keep the lightweight poster image and never download the
     video. On wider screens the desktop video loads after the page has loaded
     (unless Data Saver is on) and fades in over its poster. */
  var heroStarted = false;
  function startHeroVideo() {
    if (heroStarted || window.innerWidth <= 760) return;
    var conn = navigator.connection;
    if (conn && conn.saveData) return;
    heroStarted = true;
    $all("[data-hero-video][data-src]").forEach(function (v) {
      var reveal = function () { v.classList.add("is-ready"); };
      v.addEventListener("canplay", reveal, { once: true });
      v.addEventListener("loadeddata", reveal, { once: true });
      v.preload = "auto";
      v.src = v.getAttribute("data-src");
      var p = v.play && v.play();
      if (p && typeof p.catch === "function") p.catch(function () {});
    });
  }
  if ($("[data-hero-video][data-src]")) {
    if (document.readyState === "complete") startHeroVideo();
    else window.addEventListener("load", startHeroVideo, { once: true });
    window.addEventListener("resize", startHeroVideo);
  }

  /* ---------------- Hero Quick Check ---------------- */
  var qc = $("[data-quickcheck]");
  if (qc && window.KW) {
    var priceEl = $("[data-qc-price]", qc);
    var downEl = $("[data-qc-down]", qc);
    var occBtns = $all("[data-qc-occ]", qc);
    var priceOut = $("[data-qc-price-out]", qc);
    var downOut = $("[data-qc-down-out]", qc);
    var downPct = $("[data-qc-down-pct]", qc);
    var loanOut = $("[data-qc-loan]", qc);
    var pathOut = $("[data-qc-path]", qc);
    var fill = $("[data-qc-fill]", qc);
    var tick1 = $("[data-qc-tick1]", qc);
    var tick2 = $("[data-qc-tick2]", qc);
    var insight = $("[data-qc-insight]", qc);
    var cont = $("[data-qc-continue]", qc);
    var occ = "Primary";

    var renderQC = function () {
      var price = window.KW.parseNum(priceEl.value);
      var pct = window.KW.parseNum(downEl.value);
      var down = Math.round(price * pct / 100);
      var loan = Math.max(0, price - down);
      priceOut.textContent = window.KW.fmtCurrency(price);
      downOut.textContent = window.KW.fmtCurrency(down);
      downPct.textContent = pct + "%";
      loanOut.textContent = window.KW.fmtCurrency(loan);
      pathOut.textContent = window.KW.heroPath(loan, occ);
      var m = window.KW.meter(loan);
      fill.style.width = m.pct + "%";
      qc.setAttribute("data-zone", m.zone);
      if (tick1) tick1.style.left = m.tick1 + "%";
      if (tick2) tick2.style.left = m.tick2 + "%";
      if (insight) insight.textContent = window.KW.heroInsight(loan, occ);
      // Estimated P&I (program rate assumption) + mini purchase structure bar
      if (window.KW.rateFor && window.KW.monthlyPI) {
        var ra = window.KW.rateFor({ loan: loan, occupancy: occ });
        var pi = window.KW.monthlyPI(loan, ra.rate, 30);
        var piEl = $("[data-qc-pi]", qc); if (piEl) piEl.textContent = window.KW.fmtCurrency(pi) + "/mo";
        var piRate = $("[data-qc-pi-rate]", qc); if (piRate) piRate.textContent = "@ " + ra.rate + "% / 30 yr (illustrative assumption)";
        var sd = $("[data-qc-sd]", qc), sl = $("[data-qc-sl]", qc), sr = $("[data-qc-sr]", qc);
        if (sd) sd.style.width = (price > 0 ? Math.max(0, Math.min(100, down / price * 100)) : 0) + "%";
        if (sl) sl.style.width = (price > 0 ? Math.max(0, Math.min(100, loan / price * 100)) : 0) + "%";
        if (sr) { var _cc = window.KW.config.highBalanceLimit || window.KW.config.countyConformingLimitOneUnit; sr.style.left = (price > 0 ? Math.max(0, Math.min(100, _cc / price * 100)) : 0) + "%"; }
      }
      // Persist non-PII scenario for the Studio + pass via URL.
      var data = { price: price, down: down, downPct: pct, occ: occ, loan: loan };
      try { localStorage.setItem("kw_scenario", JSON.stringify(data)); } catch (e) {}
      if (cont) {
        cont.setAttribute("href", "/scenario-studio?price=" + price + "&downpct=" + pct + "&occ=" + encodeURIComponent(occ));
      }
    };

    var track = function (n) { try { (window.dataLayer = window.dataLayer || []).push({ event: n }); if (typeof window.gtag === "function") window.gtag("event", n); } catch (e) {} };
    var onInput = function () { renderQC(); track("quick_check_changed"); };
    if (priceEl) priceEl.addEventListener("input", onInput);
    if (downEl) downEl.addEventListener("input", onInput);
    occBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        occ = b.getAttribute("data-qc-occ");
        occBtns.forEach(function (x) { x.classList.toggle("is-on", x === b); x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        renderQC(); track("quick_check_changed");
      });
    });

    // Secondary action: prefill the simple form (#builder) with the current numbers.
    var sendLink = $("[data-qc-send]", qc);
    if (sendLink) sendLink.addEventListener("click", function () {
      var f = document.querySelector('form[name="key-west-scenario-review"]');
      if (f) {
        var price = window.KW.parseNum(priceEl.value), pct = window.KW.parseNum(downEl.value);
        var setv = function (n, v) { var el = f.querySelector('[name="' + n + '"]'); if (el && "value" in el) el.value = v; };
        setv("purchase_price", window.KW.fmtCurrency(price));
        setv("estimated_down_payment", window.KW.fmtCurrency(Math.round(price * pct / 100)));
        var occMap = { "Primary": "Primary residence", "Second home": "Second home", "Investment": "Investment property" };
        setv("occupancy", occMap[occ] || "");
      }
    });

    renderQC();
  }

  /* ---------------- Year stamp ---------------- */
  $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
