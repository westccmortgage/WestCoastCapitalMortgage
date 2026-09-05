/* K West Mortgage — consent-gated Google Ads + first-party attribution */
(function () {
  "use strict";

  var ADS_ID = "AW-18417657219";
  var LEAD_DESTINATION = "AW-18417657219/LiA7CPWd4eocEIPLnM5E";
  var ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid"];
  var PREFIX = "kwest_attr_";
  var PENDING_KEY = "kwest_pending_lead";

  function hasConsent() {
    try { return localStorage.getItem("kw_consent") === "granted"; } catch (_) { return false; }
  }
  function safeGet(key) { try { return localStorage.getItem(key) || ""; } catch (_) { return ""; } }
  function safeSet(key, value) { try { localStorage.setItem(key, value); } catch (_) {} }
  function sessionGet(key) { try { return sessionStorage.getItem(key) || ""; } catch (_) { return ""; } }
  function sessionSet(key, value) { try { sessionStorage.setItem(key, value); } catch (_) {} }
  function sessionRemove(key) { try { sessionStorage.removeItem(key); } catch (_) {} }
  function uid() { return "kwest_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 10); }

  function captureAttribution() {
    if (!hasConsent()) return;
    var qs = new URLSearchParams(window.location.search);
    ATTR_KEYS.forEach(function (key) {
      var value = qs.get(key);
      if (value) safeSet(PREFIX + key, value);
    });
    if (!safeGet(PREFIX + "landing_page")) safeSet(PREFIX + "landing_page", window.location.href);
  }

  function syncAttribution(form) {
    if (!form || !hasConsent()) return;
    captureAttribution();
    var values = {};
    ATTR_KEYS.forEach(function (key) { values[key] = safeGet(PREFIX + key); });
    values.landing_page = safeGet(PREFIX + "landing_page") || window.location.href;
    values.submission_page = window.location.href;
    Object.keys(values).forEach(function (key) {
      var input = form.querySelector('input[name="' + key + '"]');
      if (!input) {
        input = document.createElement("input");
        input.type = "hidden";
        input.name = key;
        form.appendChild(input);
      }
      input.value = values[key] || "";
    });
  }

  function initAds() {
    if (!hasConsent()) return;
    captureAttribution();
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    if (!window.__kwestAdsConfigured) {
      window.__kwestAdsConfigured = true;
      window.gtag("js", new Date());
      window.gtag("config", ADS_ID);
    }
    if (!document.querySelector("script[data-kwest-google-ads]")) {
      var script = document.createElement("script");
      script.async = true;
      script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ADS_ID);
      script.setAttribute("data-kwest-google-ads", "");
      document.head.appendChild(script);
    }
  }

  function isLeadForm(form) {
    if (!form || !form.matches || !form.matches('form')) return false;
    var name = form.getAttribute("name") || "";
    return /(?:key-west|kwest|monroe).*(?:scenario|review|lead|contact|mortgage)|(?:scenario|review).*(?:key-west|kwest|monroe)/i.test(name);
  }

  function markPending(form) {
    if (!isLeadForm(form)) return;
    syncAttribution(form);
    if (!hasConsent()) return;
    sessionSet(PENDING_KEY, JSON.stringify({
      id: uid(),
      ts: Date.now(),
      form_name: form.getAttribute("name") || "kwest-lead"
    }));
  }

  function fireConfirmedLead() {
    if (!/^\/thank-you(?:\.html)?\/?$/.test(window.location.pathname)) return;
    if (!hasConsent()) return;
    var raw = sessionGet(PENDING_KEY);
    if (!raw) return;
    var item;
    try { item = JSON.parse(raw); } catch (_) { sessionRemove(PENDING_KEY); return; }
    if (!item || !item.id || !item.ts || Date.now() - item.ts > 30 * 60 * 1000) {
      sessionRemove(PENDING_KEY);
      return;
    }
    sessionRemove(PENDING_KEY);
    initAds();
    window.dataLayer.push({
      event: "kwest_lead_submit",
      form_name: item.form_name,
      lead_event_id: item.id,
      page_location: window.location.href
    });
    window.gtag("event", "conversion", {
      send_to: LEAD_DESTINATION,
      value: 1.0,
      currency: "USD",
      transaction_id: item.id
    });
  }

  /* Capture phase runs before the site's existing submit listener builds FormData. */
  document.addEventListener("submit", async function (event) {
    var form = event.target;
    if (!isLeadForm(form)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (form.dataset.kwestSending === "true") return;
    form.dataset.kwestSending = "true";
    syncAttribution(form);
    sessionRemove(PENDING_KEY);
    var button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    try {
      var body = new URLSearchParams(new FormData(form));
      if (!body.has("form-name")) body.set("form-name", form.getAttribute("name"));
      var response = await fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body.toString() });
      if (!response.ok) throw new Error("Submission failed");
      markPending(form);
      window.location.assign(form.getAttribute("action") || "/thank-you.html");
    } catch (_) {
      form.dataset.kwestSending = "false";
      if (button) button.disabled = false;
      var notice = form.querySelector("[data-kwest-submit-error]");
      if (!notice) { notice = document.createElement("p"); notice.setAttribute("data-kwest-submit-error", ""); notice.setAttribute("role", "alert"); form.appendChild(notice); }
      notice.textContent = "Your request could not be sent. Please try again.";
    }
  }, true);

  document.addEventListener("click", function (event) {
    var button = event.target && event.target.closest ? event.target.closest("[data-consent-accept]") : null;
    if (!button) return;
    window.setTimeout(function () { initAds(); }, 0);
  }, true);

  if (hasConsent()) initAds();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fireConfirmedLead, { once: true });
  } else {
    fireConfirmedLead();
  }
})();
