/* ============================================================
   Consent + first-party visitor state
   ------------------------------------------------------------
   Privacy-conscious: we generate an anonymous first-party visitor_id
   (a UUID, not tied to identity) and remember the cookie choice so the
   banner is shown only once. We never claim to know who the visitor is
   before they submit contact information.

   Stored client-side (localStorage + a first-party cookie mirror):
     cookie_consent_status      "accepted" | "essential"
     cookie_consent_timestamp   ISO string
     visitor_id                 UUID
   plus functional helpers: cm_first_visit_at, cm_visit_count,
   cm_landing_page, cm_referrer, cm_utm (captured once on first visit).
   ============================================================ */

const K = {
  status: "cookie_consent_status",
  ts: "cookie_consent_timestamp",
  vid: "visitor_id",
  first: "cm_first_visit_at",
  count: "cm_visit_count",
  landing: "cm_landing_page",
  ref: "cm_referrer",
  utm: "cm_utm"
};

function ls(get, key, val) {
  try {
    if (get) return window.localStorage.getItem(key);
    window.localStorage.setItem(key, val);
  } catch (e) { /* storage blocked */ }
  return null;
}

function uuid() {
  if (window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID();
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0, v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function setCookie(name, value, days) {
  try {
    const d = new Date(); d.setTime(d.getTime() + days * 864e5);
    document.cookie = name + "=" + encodeURIComponent(value) + ";expires=" + d.toUTCString() + ";path=/;SameSite=Lax";
  } catch (e) { /* ignore */ }
}

export function getVisitorId() {
  let v = ls(true, K.vid);
  if (!v) { v = uuid(); ls(false, K.vid, v); setCookie(K.vid, v, 365); }
  return v;
}

export function getConsentStatus() { return ls(true, K.status); }
export function hasConsentDecision() { return Boolean(getConsentStatus()); }

export function setConsentStatus(status) {
  const ts = new Date().toISOString();
  ls(false, K.status, status);
  ls(false, K.ts, ts);
  setCookie(K.status, status, 365);
  return { status, timestamp: ts };
}

export function resetConsent() {
  try {
    window.localStorage.removeItem(K.status);
    window.localStorage.removeItem(K.ts);
  } catch (e) { /* ignore */ }
  setCookie(K.status, "", -1);
}

/* Capture immutable first-visit context once. */
function captureFirstVisit() {
  if (ls(true, K.first)) return;
  ls(false, K.first, new Date().toISOString());
  ls(false, K.count, "1");
  ls(false, K.landing, window.location.href);
  ls(false, K.ref, document.referrer || "");
  const p = new URLSearchParams(window.location.search);
  ls(false, K.utm, JSON.stringify({
    utm_source: p.get("utm_source") || "",
    utm_medium: p.get("utm_medium") || "",
    utm_campaign: p.get("utm_campaign") || "",
    utm_content: p.get("utm_content") || "",
    utm_term: p.get("utm_term") || ""
  }));
}

export function bumpVisit() {
  const n = parseInt(ls(true, K.count) || "1", 10) + 1;
  ls(false, K.count, String(n));
  return n;
}

export function getVisitCount() { return parseInt(ls(true, K.count) || "1", 10); }
export function getUTM() { try { return JSON.parse(ls(true, K.utm) || "{}"); } catch (e) { return {}; } }
export function getLandingPage() { return ls(true, K.landing) || ""; }
export function getReferrer() { return ls(true, K.ref) || ""; }

/* Build the visitors-table record. Minimal under "essential". */
export function buildVisitorRecord() {
  captureFirstVisit();
  const status = getConsentStatus();
  const base = {
    visitor_id: getVisitorId(),
    consent_status: status,
    first_visit_at: ls(true, K.first),
    last_visit_at: new Date().toISOString(),
    visit_count: getVisitCount()
  };
  if (status !== "accepted") return base; // essential -> minimal functional data only
  const utm = getUTM();
  return Object.assign(base, {
    landing_page: ls(true, K.landing) || "",
    referrer: ls(true, K.ref) || "",
    utm_source: utm.utm_source || "",
    utm_medium: utm.utm_medium || "",
    utm_campaign: utm.utm_campaign || "",
    utm_content: utm.utm_content || "",
    utm_term: utm.utm_term || "",
    user_agent: navigator.userAgent || "",
    screen_size: (window.screen ? window.screen.width + "x" + window.screen.height : "")
  });
}

captureFirstVisit();
