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
  var lastStep = false; // is the current step the final episode? (gates auto-advance)

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
          '<button type="button" class="cmtut__playbig" data-bigplay aria-label="Play video" hidden>' +
            '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>' +
          '</button>' +
          '<span class="cmtut__badge"><i></i>Financial Navigator</span>' +
          '<button type="button" class="cmtut__mute" aria-label="Unmute" hidden>&#128263;</button>' +
          '<div class="cmtut__media-foot">Your Financial Navigator</div>' +
          '<div class="cmtut__controls" data-controls hidden>' +
            '<button type="button" class="cmtut__ctrlbtn" data-pp aria-label="Pause">&#9208;</button>' +
            '<button type="button" class="cmtut__ctrlbtn" data-replay aria-label="Replay this video">&#8635;</button>' +
          '</div>' +
          '<div class="cmtut__progress" data-progress hidden><span class="cmtut__progress-fill" data-fill></span></div>' +
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
    els.bigplay = host.querySelector("[data-bigplay]");
    els.controls = host.querySelector("[data-controls]");
    els.pp = host.querySelector("[data-pp]");
    els.replay = host.querySelector("[data-replay]");
    els.progress = host.querySelector("[data-progress]");
    els.fill = host.querySelector("[data-fill]");

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

    // Big centered Play overlay — shown whenever the clip is paused (e.g.
    // when mobile blocks autoplay). A tap is a user gesture, so play WITH
    // sound and remember that choice for the rest of the tour.
    els.bigplay.addEventListener("click", function (e) {
      e.preventDefault();
      els.video.muted = false; prefMuted = false; setMuteIcon();
      try { var p = els.video.play(); if (p && p.catch) p.catch(function () {}); } catch (e2) {}
    });

    // Playback controls — pause/resume, replay, seek; auto-advance on end.
    els.pp.addEventListener("click", function (e) {
      e.preventDefault();
      if (els.video.paused) { try { els.video.play(); } catch (e2) {} }
      else els.video.pause();
    });
    els.replay.addEventListener("click", function (e) {
      e.preventDefault();
      try { els.video.currentTime = 0; els.video.play(); } catch (e2) {}
    });
    els.video.addEventListener("play", setPPIcon);
    els.video.addEventListener("pause", setPPIcon);
    els.video.addEventListener("timeupdate", function () {
      if (!els.fill || !els.video.duration) return;
      els.fill.style.width = (els.video.currentTime / els.video.duration * 100) + "%";
    });
    els.video.addEventListener("ended", function () {
      // Continuous training: roll into the next episode automatically.
      if (!lastStep) nav("next");
    });
    els.progress.addEventListener("click", function (e) {
      if (!els.video.duration) return;
      var rect = els.progress.getBoundingClientRect();
      var ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      try { els.video.currentTime = ratio * els.video.duration; } catch (e2) {}
    });

    els.video.addEventListener("error", function () { showLayer("img"); els.mute.hidden = true; });
    els.img.addEventListener("error", function () {
      if (els.img.getAttribute("src")) brokenImg[els.img.getAttribute("src")] = true;
      showLayer("ph");
    });
  }

  function setPPIcon() {
    if (!els.pp || !els.video) return;
    if (els.video.paused) { els.pp.innerHTML = "&#9654;"; els.pp.setAttribute("aria-label", "Play"); }
    else { els.pp.innerHTML = "&#9208;"; els.pp.setAttribute("aria-label", "Pause"); }
    // Big overlay Play button: visible only while a clip is loaded but paused.
    if (els.bigplay) {
      var videoShown = els.video.style.display === "block";
      els.bigplay.hidden = !(videoShown && els.video.paused);
    }
  }

  function showLayer(which) {
    var vid = which === "video";
    if (els.video) els.video.style.display = vid ? "block" : "none";
    if (els.img) els.img.style.display = which === "img" ? "block" : "none";
    if (els.ph) els.ph.style.display = which === "ph" ? "flex" : "none";
    if (els.controls) els.controls.hidden = !vid;
    if (els.progress) els.progress.hidden = !vid;
    if (els.fill && !vid) els.fill.style.width = "0";
    if (els.bigplay && !vid) els.bigplay.hidden = true;
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
    lastStep = !!d.last;
    els.step.textContent = "Step " + (d.idx + 1) + " of " + d.total;
    els.title.textContent = d.title || "";
    els.body.textContent = d.body || "";
    els.back.disabled = !!d.first;
    els.nextLabel.textContent = d.last ? "Done" : "Next";
    els.next.classList.toggle("is-done", !!d.last);
    loadMedia(d);
    setPPIcon();
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
