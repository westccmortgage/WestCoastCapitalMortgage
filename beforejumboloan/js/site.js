/* ============================================================
   BeforeJumboLoan.com — Site behavior
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
    BRAND: "BeforeJumboLoan.com"
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

  /* ---------------- Mobile nav ---------------- */
  var toggle = $(".nav__toggle"), menu = $(".mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.classList.toggle("open", open);
      document.body.style.overflow = open ? "hidden" : "";
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $all("a", menu).forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("open"); toggle.classList.remove("open"); document.body.style.overflow = "";
      });
    });
  }

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
      { q: "“I’m buying at $1.15M with 20% down in a high-cost county. Do I really need jumbo?”", next: "High-Balance Review", href: "https://westccmortgage.com/loans" },
      { q: "“I’m self-employed and buying a second home. What changes?”", next: "Self-Employed / Second Home Review", href: "https://westccmortgage.com/loans" },
      { q: "“I’m buying an investment property and want to compare DSCR vs conventional.”", next: "Investor Review", href: "https://westccmortgage.com/loans" },
      { q: "“I’m a veteran buying in a high-cost county. How does VA fit?”", next: "VA Review", href: "https://westccmortgage.com/resources" }
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

  /* ---------------- Cookie consent ---------------- */
  var bar = $(".cookie-bar");
  if (bar) {
    var stored;
    try { stored = localStorage.getItem("kw_consent"); } catch (e) { stored = null; }
    if (!stored) { window.setTimeout(function () { bar.classList.add("show"); }, 900); }
    var setConsent = function (val) {
      try { localStorage.setItem("kw_consent", val); } catch (e) {}
      bar.classList.remove("show");
      if (val === "granted") ensureVisitorId();
    };
    var acc = $("[data-consent-accept]", bar), dec = $("[data-consent-decline]", bar);
    if (acc) acc.addEventListener("click", function () { setConsent("granted"); });
    if (dec) dec.addEventListener("click", function () { setConsent("declined"); });
  }
  ensureVisitorId();

  /* ---------------- Netlify Forms (AJAX submit) ----------------
     Forms stay as real Netlify forms in the HTML (data-netlify="true" +
     hidden form-name + honeypot) so Netlify detects them at deploy and the
     native POST still works with JS disabled. With JS on, we submit via a
     urlencoded fetch POST to "/" (the most reliable Netlify method on
     statically-hosted sites), then redirect to the thank-you page. */
  $all('form[data-netlify]').forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      // Let the browser enforce required fields with its native UI first.
      if (typeof form.reportValidity === "function" && !form.reportValidity()) {
        ev.preventDefault();
        return;
      }
      ev.preventDefault();

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

      if (btn) { btn.dataset.label = btn.textContent; btn.disabled = true; btn.textContent = "Sending…"; }

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: encoded.toString()
      }).then(function (res) {
        if (!res.ok) throw new Error("Bad status " + res.status);
        window.location.href = redirect;
      }).catch(function () {
        // Network/processing fallback: let the browser do a normal native POST,
        // which Netlify also accepts and will redirect to the action page.
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Submit"; }
        form.submit();
      });
    });
  });

  /* ---------------- Hero video ---------------- */
  /* Reveal a hero video only once it can actually play; otherwise the
     animated coastal gradient remains as a graceful fallback. */
  $all("[data-hero-video]").forEach(function (v) {
    var reveal = function () { v.classList.add("is-ready"); };
    if (v.readyState >= 3) reveal();
    v.addEventListener("canplay", reveal, { once: true });
    v.addEventListener("loadeddata", reveal, { once: true });
    // Best-effort autoplay (some browsers need an explicit call)
    var p = v.play && v.play();
    if (p && typeof p.catch === "function") p.catch(function () {});
  });

  /* ---------------- Hero "Before Jumbo Quick Check" ---------------- */
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

  /* ---------------- Contact email (single source: engine FORM_CONFIG/BRAND_CONFIG) ----------------
     Only upgrade the contact link to a mailto when a REAL address is configured.
     Until then the markup default ("Send your scenario" → the Strategy Studio)
     stays in place, so no placeholder email is ever exposed on the live site. */
  var recipient = (window.BRAND_CONFIG && window.BRAND_CONFIG.recipient) || "";
  var validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient) && !/REPLACE|SET_/i.test(recipient);
  if (validEmail) {
    $all("[data-recipient-email]").forEach(function (a) {
      a.setAttribute("href", "mailto:" + recipient);
      a.textContent = recipient;
    });
  }
})();

/* Production lead tracking: only confirmed backend submissions, with cookie consent. */
(function () {
  "use strict";
  var ID="AW-18417657219", DEST=ID+"/LiA7CPWd4eocEIPLnM5E";
  var KEYS=["gclid","gbraid","wbraid","utm_source","utm_medium","utm_campaign","utm_term","utm_content"];
  function get(k){try{return localStorage.getItem(k)||"";}catch(e){return "";}}
  function set(k,v){try{localStorage.setItem(k,v);}catch(e){}}
  function consent(){return get("kw_consent")==="granted";}
  function capture(){
    if(!consent())return;
    var p=new URLSearchParams(location.search);
    KEYS.forEach(function(k){if(p.get(k))set("bjl_attr_"+k,p.get(k));});
    if(!get("bjl_attr_landing_page"))set("bjl_attr_landing_page",location.href);
  }
  function init(){
    if(!consent())return;
    capture();
    window.dataLayer=window.dataLayer||[];
    window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
    if(!document.querySelector("script[data-bjl-ads]")){
      window.gtag("js",new Date());window.gtag("config",ID);
      var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+ID;
      s.setAttribute("data-bjl-ads","");document.head.appendChild(s);
    }
  }
  function attribution(){
    capture();var a={};
    KEYS.forEach(function(k){a[k]=consent()?get("bjl_attr_"+k):"";});
    a.landing_page=consent()?get("bjl_attr_landing_page"):"";
    a.submission_page=location.href;
    a.lead_event_id="bjl_"+Date.now().toString(36)+"_"+Math.random().toString(36).slice(2,10);
    return a;
  }
  var sent={};
  function confirmed(id,done){
    if(!consent()||sent[id]){if(done)done();return;}
    sent[id]=true;init();
    var finished=false;
    function finish(){if(finished)return;finished=true;if(done)done();}
    window.dataLayer.push({event:"bjl_lead_submit",lead_event_id:id,page_location:location.href});
    window.gtag("event","conversion",{send_to:DEST,value:1,currency:"USD",transaction_id:id,event_callback:finish,event_timeout:1500});
    if(done)setTimeout(finish,1800);
  }
  window.BJLAds={attribution:attribution,confirmed:confirmed};
  function ready(){
    init();
    document.querySelectorAll("[data-consent-accept]").forEach(function(b){b.addEventListener("click",function(){setTimeout(init,0);});});
    var form=document.querySelector('form[name="contact"]');
    if(!form)return;
    var sending=false;
    form.addEventListener("submit",function(e){
      e.preventDefault();e.stopImmediatePropagation();
      if(sending||!form.reportValidity())return;
      sending=true;
      var a=attribution(),body=new URLSearchParams(new FormData(form));
      Object.keys(a).forEach(function(k){body.set(k,a[k]);});
      body.set("form-name","contact");
      var b=form.querySelector('button[type="submit"]');if(b)b.disabled=true;
      fetch("/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:body.toString()})
      .then(function(r){
        if(!r.ok)throw new Error("Submission failed");
        confirmed(a.lead_event_id,function(){location.assign(form.getAttribute("action")||"/thank-you.html");});
      }).catch(function(){
        sending=false;if(b)b.disabled=false;
        var n=form.querySelector("[data-bjl-error]");
        if(!n){n=document.createElement("p");n.setAttribute("data-bjl-error","");n.setAttribute("role","alert");form.appendChild(n);}
        n.textContent="Your request could not be sent. Please try again.";
      });
    },true);
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ready);else ready();
})();
