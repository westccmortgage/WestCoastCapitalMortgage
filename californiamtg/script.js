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

  /* ---- Hero video: only attempt playback once sources exist ----
     The <video> ships with its <source> tags commented out, so until a real
     file is added the poster/gradient shows. When sources are added, this
     ensures muted autoplay resumes cleanly on browsers that pause it. */
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo && heroVideo.querySelector("source")) {
    heroVideo.load();
    var tryPlay = heroVideo.play();
    if (tryPlay && typeof tryPlay.catch === "function") {
      tryPlay.catch(function () { /* autoplay blocked — poster remains */ });
    }
  }
})();
