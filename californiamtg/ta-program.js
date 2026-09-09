/* Keeps the TA-Next "American Dream" program links in sync with the site
   language. The i18n engine translates text nodes but not href attributes, so
   this rewrites the ?lang= param on any <a data-ta-program> to match the
   language stored by i18n.js (localStorage "cmLang"). Runs on load and whenever
   a language button is pressed. Self-contained; no dependency on i18n internals. */
(function () {
  "use strict";
  var LANGS = { en: "en", es: "es", ru: "ru", zh: "zh" };
  function current() {
    var l = null;
    try { l = localStorage.getItem("cmLang"); } catch (e) {}
    return LANGS[l] ? l : "en";
  }
  function apply() {
    var lang = LANGS[current()] || "en";
    var links = document.querySelectorAll("a[data-ta-program]");
    for (var i = 0; i < links.length; i++) {
      try {
        var u = new URL(links[i].href, location.origin);
        u.searchParams.set("lang", lang);
        links[i].href = u.toString();
      } catch (e) {}
    }
  }
  function init() {
    apply();
    var btns = document.querySelectorAll("[data-lang]");
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function () { setTimeout(apply, 0); });
    }
  }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
