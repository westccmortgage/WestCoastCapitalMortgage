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
     Any element with [data-start] scrolls to the builder and (re)starts it.
     An optional [data-goal] preselects the entry scenario (e.g. Investors,
     Self-Employed, Rates "Check My Scenario"). */
  function startBuilder(goal) {
    var target = document.getElementById("builder");
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    if (window.CMScenario && typeof window.CMScenario.start === "function") {
      window.CMScenario.start(goal || null);
    }
  }
  document.querySelectorAll("[data-start]").forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      closeNav && nav && nav.classList.contains("open") && closeNav();
      startBuilder(link.getAttribute("data-goal"));
    });
  });

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
