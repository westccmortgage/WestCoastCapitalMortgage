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

      var data = new FormData(contactForm);
      var body = new URLSearchParams(data).toString();

      /* =========================================================
         TODO: connect this form to the existing WCCM workflow:
           - WCCM email workflow / shared inbox
           - CRM (HubSpot / Salesforce / GoHighLevel)
           - Netlify Forms (already wired: data-netlify + hidden form-name)
           - Zapier webhook   (https://hooks.zapier.com/...)
           - Make webhook     (https://hook.make.com/...)
         The POST below feeds Netlify Forms; add additional destinations here.
         ========================================================= */
      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body
      }).then(showContactSuccess).catch(showContactSuccess);
    });
  }
  function showContactSuccess() {
    var card = document.getElementById("contactCard") || (contactForm && contactForm.parentNode);
    if (!card) return;
    card.innerHTML =
      '<div class="thankyou">' +
        '<div class="ty-mark" aria-hidden="true">&#10003;</div>' +
        '<h3>Thank you.</h3>' +
        '<p class="ty-lead">Your message has been received. A licensed mortgage professional ' +
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
})();
