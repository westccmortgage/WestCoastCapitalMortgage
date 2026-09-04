/* ============================================================
   California Mortgage — app orchestrator (ES module, all pages)
   ------------------------------------------------------------
   - Renders the cookie/consent banner (once).
   - Generates/stores a first-party visitor_id and a visitors row.
   - Initializes event tracking (only when consent === "accepted").
   - Exposes lead helpers used by the contact form (script.js) and the
     scenario builder (scenario-builder.js):
        window.CMTrack(eventName, data)
        window.CMLeads.saveContactForm(formEl)
        window.CMLeads.saveScenarioLead(lead)
        window.CMConsent.reset()
   - A lead is counted as a Google Ads conversion only after Supabase or
     Netlify has actually accepted it.
   ============================================================ */
import { getSupabase, isConfigured } from "./lib/supabaseClient.js";
import { track, initAutoTracking } from "./lib/tracking.js";
import {
  getVisitorId, getConsentStatus, hasConsentDecision, setConsentStatus,
  resetConsent, bumpVisit, buildVisitorRecord, getUTM, getLandingPage, getReferrer
} from "./lib/consent.js";
import { initGoogleAds, fireLeadConversion } from "./lib/ads.js";
import "./lib/contactSubmit.js";

const VISITOR_SAVED = "cm_visitor_saved";
const SCENARIO_FORM_NAME = "californiamtg-scenario-lead";

/* ---------- visitor row (insert once; RLS is insert-only) ---------- */
async function saveVisitorOnce() {
  try {
    if (window.localStorage.getItem(VISITOR_SAVED) === "1") return;
  } catch (e) { /* ignore */ }
  const supabase = await getSupabase();
  if (!supabase) return;
  try {
    const result = await supabase.from("visitors").insert(buildVisitorRecord());
    if (result && result.error) {
      // A duplicate visitor_id means the row already exists and is safe to mark saved.
      if (result.error.code !== "23505") throw result.error;
    }
    try { window.localStorage.setItem(VISITOR_SAVED, "1"); } catch (_) {}
  } catch (e) {
    console.debug("[California Mortgage] visitor insert failed:", e);
  }
}

/* ---------- consent banner ---------- */
function renderBanner() {
  if (document.getElementById("cmConsent")) return;
  const el = document.createElement("div");
  el.id = "cmConsent";
  el.className = "cm-consent";
  el.setAttribute("role", "dialog");
  el.setAttribute("aria-label", "Cookie consent");
  el.innerHTML =
    '<div class="cm-consent-inner">' +
      '<div class="cm-consent-copy">' +
        '<h3>Personalized Mortgage Guidance</h3>' +
        '<p>We use cookies and analytics to remember your visit, improve your experience, and ' +
        'understand which mortgage topics are helpful. You can continue with essential cookies ' +
        'only or allow full experience tracking. ' +
        '<a href="/privacy-policy.html">Privacy Policy</a></p>' +
      '</div>' +
      '<div class="cm-consent-actions">' +
        '<button type="button" class="btn btn-outline-dark" data-consent="essential">Essential Only</button>' +
        '<button type="button" class="btn btn-primary" data-consent="accepted">Accept &amp; Continue</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(el);
  requestAnimationFrame(function () { el.classList.add("show"); });

  el.querySelectorAll("[data-consent]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const choice = btn.getAttribute("data-consent");
      setConsentStatus(choice);
      el.classList.remove("show");
      window.setTimeout(function () { el.remove(); }, 300);
      saveVisitorOnce();
      if (choice === "accepted") {
        initGoogleAds();
        initAutoTracking();
      }
    });
  });
}

/* ---------- attribution helpers ---------- */
function consentedAttribution() {
  if (getConsentStatus() !== "accepted") return {};
  const a = getUTM() || {};
  return {
    utm_source: a.utm_source || "",
    utm_medium: a.utm_medium || "",
    utm_campaign: a.utm_campaign || "",
    utm_content: a.utm_content || "",
    utm_term: a.utm_term || "",
    gclid: a.gclid || "",
    gbraid: a.gbraid || "",
    wbraid: a.wbraid || ""
  };
}

function attributionForAnswers() {
  const a = consentedAttribution();
  const out = {};
  ["utm_content", "utm_term", "gclid", "gbraid", "wbraid"].forEach(function (key) {
    if (a[key]) out[key] = a[key];
  });
  return out;
}

/* ---------- lead mapping ---------- */
function leadRowFromScenario(lead) {
  const c = lead.contact || {};
  const s = lead.source || {};
  const a = consentedAttribution();
  const answers = Object.assign({}, lead.answers || {});
  const extraAttribution = attributionForAnswers();
  if (Object.keys(extraAttribution).length) answers.attribution = extraAttribution;
  return {
    visitor_id: getVisitorId(),
    lead_source: "californiamtg.com",
    site: (window.CM_CONFIG && window.CM_CONFIG.SITE) || "californiamtg.com",
    lead_category: (lead.leadCategories || []).join(", "),
    full_name: c.fullName || "",
    phone: c.phone || "",
    email: c.email || "",
    preferred_contact_method: c.contactMethod || "",
    user_type: lead.userType || "",
    scenario_type: lead.scenarioType || "",
    property_state: lead.propertyState || "",
    timeline: lead.timeline || "",
    estimated_price_or_value: lead.estimatedValue || "",
    message: c.message || "",
    answers: answers,
    landing_page: getLandingPage(),
    utm_source: s.utm_source || a.utm_source || "",
    utm_medium: s.utm_medium || a.utm_medium || "",
    utm_campaign: s.utm_campaign || a.utm_campaign || "",
    referrer: s.referrer || getReferrer(),
    crm_status: "not_connected"
  };
}

function leadRowFromContactForm(form) {
  const f = new FormData(form);
  const utm = consentedAttribution();
  const get = function (k) { return (f.get(k) || "").toString().trim(); };

  const specialtyAnswers = {
    iAmA: get("iAmA"),
    helpWith: get("helpWith"),
    via: form.getAttribute("data-intake-type") || "contact_form",
    propertyCity: get("propertyCity"),
    propertyAddress: get("propertyAddress"),
    propertyType: get("propertyType"),
    occupancy: get("occupancy"),
    purchasePrice: get("purchasePrice"),
    propertyValue: get("propertyValue"),
    loanAmount: get("loanAmount"),
    downPayment: get("downPayment"),
    creditRange: get("creditRange"),
    incomeType: get("incomeType"),
    denialReason: get("denialReason"),
    currentLender: get("currentLender"),
    closingDeadline: get("closingDeadline"),
    monthlyRent: get("monthlyRent"),
    monthlyHousingExpense: get("monthlyHousingExpense"),
    currentHomeCity: get("currentHomeCity"),
    currentMortgageBalance: get("currentMortgageBalance"),
    listingStatus: get("listingStatus"),
    nextPropertyCity: get("nextPropertyCity"),
    nextPropertyStatus: get("nextPropertyStatus"),
    availableCash: get("availableCash"),
    currentInterestRate: get("currentInterestRate"),
    useOfFunds: get("useOfFunds"),
    preferredStructure: get("preferredStructure")
  };
  const extraAttribution = attributionForAnswers();
  if (Object.keys(extraAttribution).length) specialtyAnswers.attribution = extraAttribution;
  Object.keys(specialtyAnswers).forEach(function (key) {
    if (!specialtyAnswers[key] || (typeof specialtyAnswers[key] === "object" && !Object.keys(specialtyAnswers[key]).length)) delete specialtyAnswers[key];
  });

  return {
    visitor_id: getVisitorId(),
    lead_source: form.getAttribute("data-lead-source") || "californiamtg.com",
    site: (window.CM_CONFIG && window.CM_CONFIG.SITE) || "californiamtg.com",
    lead_category: form.getAttribute("data-lead-category") || get("helpWith") || "Contact",
    full_name: get("fullName"),
    phone: get("phone"),
    email: get("email"),
    preferred_contact_method: get("contactMethod"),
    user_type: get("iAmA"),
    scenario_type: get("denialReason") || get("helpWith"),
    property_state: get("propertyState") || "",
    timeline: get("closingDeadline") || get("timeline") || "",
    estimated_price_or_value: get("purchasePrice") || get("propertyValue") || "",
    message: get("message"),
    answers: specialtyAnswers,
    landing_page: getLandingPage(),
    utm_source: utm.utm_source || "",
    utm_medium: utm.utm_medium || "",
    utm_campaign: utm.utm_campaign || "",
    referrer: getReferrer() || document.referrer || "",
    crm_status: "not_connected"
  };
}

/* ---------- backend persistence ---------- */
async function saveLeadToSupabase(row, eventName) {
  try { window.localStorage.setItem("cm_last_lead", JSON.stringify(row)); } catch (e) {}
  const supabase = await getSupabase();
  if (!supabase) throw new Error("Supabase client unavailable");
  const result = await supabase.from("leads").insert(row);
  if (result && result.error) throw result.error;
  try { await track(eventName, { lead_category: row.lead_category }); } catch (e) {}
  return { stored: "supabase" };
}

async function postContactToNetlify(form, row) {
  const data = new FormData(form);
  const formName = data.get("form-name") || form.getAttribute("name") || "californiamtg-contact";
  if (!data.get("form-name")) data.set("form-name", formName);
  const a = consentedAttribution();
  Object.keys(a).forEach(function (key) { if (a[key]) data.set(key, a[key]); });
  data.set("landing_page", getLandingPage() || window.location.href);
  data.set("submission_page", window.location.href);

  const body = new URLSearchParams();
  data.forEach(function (value, key) { body.append(key, String(value)); });
  const response = await fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString()
  });
  if (!response.ok) throw new Error("Netlify contact form HTTP " + response.status);
  try { await track("contact_form_submitted", { lead_category: row.lead_category }); } catch (e) {}
  return { stored: "netlify" };
}

async function postScenarioToNetlify(row) {
  const data = new URLSearchParams();
  data.set("form-name", SCENARIO_FORM_NAME);
  data.set("full_name", row.full_name || "");
  data.set("phone", row.phone || "");
  data.set("email", row.email || "");
  data.set("lead_category", row.lead_category || "");
  data.set("scenario_type", row.scenario_type || "");
  data.set("timeline", row.timeline || "");
  data.set("message", row.message || "");
  data.set("landing_page", row.landing_page || window.location.href);
  data.set("utm_source", row.utm_source || "");
  data.set("utm_medium", row.utm_medium || "");
  data.set("utm_campaign", row.utm_campaign || "");
  data.set("lead_json", JSON.stringify(row));
  const response = await fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: data.toString()
  });
  if (!response.ok) throw new Error("Netlify scenario form HTTP " + response.status);
  try { await track("scenario_completed", { lead_category: row.lead_category }); } catch (e) {}
  return { stored: "netlify" };
}

function countConfirmedLead(row, eventName, result) {
  const id = fireLeadConversion({
    lead_type: eventName,
    lead_category: row.lead_category || "",
    stored: result.stored
  });
  return Object.assign({}, result, { conversion_event_id: id || "" });
}

async function saveContactForm(form) {
  const row = leadRowFromContactForm(form);
  try { window.localStorage.setItem("cm_last_lead", JSON.stringify(row)); } catch (e) {}

  let result;
  if (isConfigured()) {
    try {
      result = await saveLeadToSupabase(row, "contact_form_submitted");
    } catch (err) {
      console.warn("[California Mortgage] Supabase contact insert failed; trying Netlify:", err);
      result = await postContactToNetlify(form, row);
    }
  } else {
    result = await postContactToNetlify(form, row);
  }
  return countConfirmedLead(row, "contact_form_submitted", result);
}

async function saveScenarioLead(lead) {
  const row = leadRowFromScenario(lead);
  try { window.localStorage.setItem("cm_last_lead", JSON.stringify(row)); } catch (e) {}

  try {
    let result;
    if (isConfigured()) {
      try {
        result = await saveLeadToSupabase(row, "scenario_completed");
      } catch (err) {
        console.warn("[California Mortgage] Supabase scenario insert failed; trying Netlify:", err);
        result = await postScenarioToNetlify(row);
      }
    } else {
      result = await postScenarioToNetlify(row);
    }
    return countConfirmedLead(row, "scenario_completed", result);
  } catch (err) {
    // The scenario builder currently thanks immediately. Keep a local copy but
    // never report a Google conversion unless a backend actually accepted it.
    console.warn("[California Mortgage] scenario lead could not reach a backend:", err);
    return { stored: "local", error: true };
  }
}

/* ---------- public API ---------- */
window.CMTrack = function (eventName, data) { track(eventName, data); };

window.CMLeads = {
  isSupabaseConfigured: isConfigured,
  saveScenarioLead: saveScenarioLead,
  saveContactForm: saveContactForm
};

window.CMConsent = {
  status: getConsentStatus,
  getVisitorId: getVisitorId,
  reset: function () {
    resetConsent();
    try { window.localStorage.removeItem(VISITOR_SAVED); } catch (e) {}
    renderBanner();
  }
};

/* ---------- init ---------- */
getVisitorId();
if (hasConsentDecision()) {
  if (getConsentStatus() === "accepted") {
    bumpVisit();
    saveVisitorOnce();
    initGoogleAds();
    initAutoTracking();
  } else {
    saveVisitorOnce();
  }
} else {
  renderBanner();
}

var manageBtn = document.getElementById("manageConsent");
if (manageBtn) manageBtn.addEventListener("click", function (e) {
  e.preventDefault();
  window.CMConsent.reset();
});
