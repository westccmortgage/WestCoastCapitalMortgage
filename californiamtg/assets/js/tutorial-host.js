/* ============================================================
   California Mortgage — Tutorial host (parent page)
   ------------------------------------------------------------
   When the Strategy Studio is embedded in an iframe on the homepage,
   the tutorial card is rendered HERE, on the page, as a floating
   "Financial Navigator" panel pinned to a corner — fully separate
   from the calculator frame. The iframe keeps only the gold glow on
   the active field and drives the flow via postMessage:

     iframe → page : { cmTut:"open" } / { cmTut:"step", ... } / { cmTut:"close" }
     page → iframe : { cmTut:"nav", dir:"next"|"back"|"skip" }

   Safe: does nothing until it receives a tutorial message; never throws.
   ============================================================ */
(function () {
  "use strict";

  var host = null, els = {}, brokenImg = {}, prefMuted = false; // sound ON by default

  function frameWin() {
    var f = document.getElementById("studioFrame");
    return f && f.contentWindow ? f.contentWindow : null;
  }
  function nav(dir) { var w = frameWin(); if (w) try { w.postMessage({ cmTut: "nav", dir: dir }, "*"); } catch (e) {} }

  function build() {
    if (host) return;
    host = document.createElement("div");
    host.className = "cmtut-host";
    host.setAttribute("role", "dialog");
    host.setAttribute("aria-modal", "false");
    host.setAttribute("aria-label", "Guided tour — Financial Navigator");
    host.hidden = true;
    host.innerHTML =
      '<div class="cmtut__card">' +
        '<div class="cmtut__media">' +
          '<div class="cmtut__media-ph" aria-hidden="true">' +
            '<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true">' +
              '<circle cx="32" cy="24" r="12" fill="rgba(255,255,255,.85)"/>' +
              '<path d="M12 58c0-12 9-19 20-19s20 7 20 19Z" fill="rgba(255,255,255,.85)"/>' +
            '</svg>' +
          '</div>' +
          '<img class="cmtut__img" alt="" />' +
          '<video class="cmtut__video" playsinline preload="metadata"></video>' +
          '<span class="cmtut__badge"><i></i>Financial Navigator</span>' +
          '<button type="button" class="cmtut__mute" aria-label="Unmute" hidden>&#128263;</button>' +
          '<div class="cmtut__media-foot">Your Financial Navigator</div>' +
        '</div>' +
        '<div class="cmtut__panel">' +
          '<button type="button" class="cmtut__close" data-act="skip" aria-label="Close tutorial">&#215;</button>' +
          '<p class="cmtut__step"></p>' +
          '<h3 class="cmtut__title"></h3>' +
          '<span class="cmtut__rule" aria-hidden="true"></span>' +
          '<p class="cmtut__body"></p>' +
          '<div class="cmtut__nav">' +
            '<button type="button" class="cmtut__btn cmtut__btn--skip" data-act="skip">Skip</button>' +
            '<div class="cmtut__nav-right">' +
              '<button type="button" class="cmtut__btn cmtut__btn--back" data-act="back">Back</button>' +
              '<button type="button" class="cmtut__btn cmtut__btn--next" data-act="next">' +
                '<span class="cmtut__nextlabel">Next</span>' +
                '<svg class="cmtut__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5.5 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(host);

    els.media = host.querySelector(".cmtut__media");
    els.ph = host.querySelector(".cmtut__media-ph");
    els.img = host.querySelector(".cmtut__img");
    els.video = host.querySelector(".cmtut__video");
    els.mute = host.querySelector(".cmtut__mute");
    els.step = host.querySelector(".cmtut__step");
    els.title = host.querySelector(".cmtut__title");
    els.body = host.querySelector(".cmtut__body");
    els.back = host.querySelector(".cmtut__btn--back");
    els.next = host.querySelector(".cmtut__btn--next");
    els.nextLabel = host.querySelector(".cmtut__nextlabel");

    host.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]"); if (!b) return;
      e.preventDefault(); nav(b.getAttribute("data-act"));
    });
    els.mute.addEventListener("click", function (e) {
      e.preventDefault();
      els.video.muted = !els.video.muted;
      prefMuted = els.video.muted;            // remember the choice across steps
      setMuteIcon();
      if (!els.video.muted) { try { els.video.play(); } catch (e2) {} }
    });
    els.video.addEventListener("error", function () { showLayer("img"); els.mute.hidden = true; });
    els.img.addEventListener("error", function () {
      if (els.img.getAttribute("src")) brokenImg[els.img.getAttribute("src")] = true;
      showLayer("ph");
    });
  }

  function showLayer(which) {
    if (els.video) els.video.style.display = which === "video" ? "block" : "none";
    if (els.img) els.img.style.display = which === "img" ? "block" : "none";
    if (els.ph) els.ph.style.display = which === "ph" ? "flex" : "none";
  }

  function setMuteIcon() {
    if (!els.mute || !els.video) return;
    if (els.video.muted) { els.mute.innerHTML = "&#128263;"; els.mute.setAttribute("aria-label", "Unmute"); }
    else { els.mute.innerHTML = "&#128266;"; els.mute.setAttribute("aria-label", "Mute"); }
  }

  function loadMedia(d) {
    var v = els.video, img = els.img;
    try { if (v) v.pause(); } catch (e) {}
    if (els.mute) els.mute.hidden = true;
    var imgSrc = d.imageSrc || null;

    function tryImage() {
      if (!img || !imgSrc || brokenImg[imgSrc]) { showLayer("ph"); return; }
      if (img.getAttribute("src") !== imgSrc) img.setAttribute("src", imgSrc);
      if (img.complete && img.naturalWidth > 0) showLayer("img");
      else { showLayer("ph"); img.onload = function () { showLayer("img"); }; }
    }

    if (d.videoSrc && v) {
      if (v.getAttribute("src") !== d.videoSrc) { v.setAttribute("src", d.videoSrc); try { v.load(); } catch (e) {} }
      if (imgSrc) v.setAttribute("poster", imgSrc);
      els.mute.hidden = false;
      // Sound ON by default (unless the user muted earlier). If the browser
      // blocks autoplay-with-sound, fall back to muted so it still plays, and
      // leave the unmute button so they can enable it.
      v.muted = prefMuted;
      setMuteIcon();
      showLayer("video");
      var p = v.play();
      if (p && p.catch) p.catch(function () {
        if (!prefMuted) {
          v.muted = true; setMuteIcon();
          try { var p2 = v.play(); if (p2 && p2.catch) p2.catch(function () {}); } catch (e) {}
        }
      });
    } else {
      if (v) { v.removeAttribute("src"); try { v.load(); } catch (e) {} }
      tryImage();
    }
  }

  function renderStep(d) {
    build();
    els.step.textContent = "Step " + (d.idx + 1) + " of " + d.total;
    els.title.textContent = d.title || "";
    els.body.textContent = d.body || "";
    els.back.disabled = !!d.first;
    els.nextLabel.textContent = d.last ? "Done" : "Next";
    els.next.classList.toggle("is-done", !!d.last);
    loadMedia(d);
  }

  function open() {
    build();
    host.hidden = false;
    requestAnimationFrame(function () { host.classList.add("is-in"); });
    document.addEventListener("keydown", onKey, true);
  }
  function close() {
    if (!host) return;
    if (els.video) { try { els.video.pause(); } catch (e) {} }
    host.classList.remove("is-in");
    document.removeEventListener("keydown", onKey, true);
    window.setTimeout(function () { if (host && !host.classList.contains("is-in")) host.hidden = true; }, 280);
  }
  function onKey(e) {
    if (!host || host.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); nav("skip"); }
    else if (e.key === "ArrowRight") { e.preventDefault(); nav("next"); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); nav("back"); }
  }

  window.addEventListener("message", function (e) {
    var d = e && e.data; if (!d || !d.cmTut) return;
    if (d.cmTut === "open") open();
    else if (d.cmTut === "step") renderStep(d);
    else if (d.cmTut === "close") close();
  });
})();
