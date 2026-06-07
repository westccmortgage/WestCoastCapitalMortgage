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
   Works with no backend configured (graceful fallback).
   ============================================================ */
import { getSupabase, isConfigured } from "./lib/supabaseClient.js";
import { sendLeadToCRM } from "./lib/crmWebhook.js";
import { track, initAutoTracking } from "./lib/tracking.js";
import {
  getVisitorId, getConsentStatus, hasConsentDecision, setConsentStatus,
  resetConsent, bumpVisit, buildVisitorRecord, getUTM
} from "./lib/consent.js";

const VISITOR_SAVED = "cm_visitor_saved";

/* ---------- visitor row (insert once; RLS is insert-only) ---------- */
async function saveVisitorOnce() {
  try {
    if (window.localStorage.getItem(VISITOR_SAVED) === "1") return;
  } catch (e) { /* ignore */ }
  const supabase = await getSupabase();
  if (!supabase) return;
  try {
    await supabase.from("visitors").insert(buildVisitorRecord());
    window.localStorage.setItem(VISITOR_SAVED, "1");
  } catch (e) {
    // unique visitor_id (already inserted) or RLS — safe to ignore
    try { window.localStorage.setItem(VISITOR_SAVED, "1"); } catch (_) {}
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
      if (choice === "accepted") initAutoTracking();
    });
  });
}

/* ---------- lead mapping + save ---------- */
function leadRowFromScenario(lead) {
  const c = lead.contact || {};
  const s = lead.source || {};
  return {
    visitor_id: getVisitorId(),
    lead_source: "californiamtg.com",
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
    answers: lead.answers || {},
    utm_source: s.utm_source || "",
    utm_medium: s.utm_medium || "",
    utm_campaign: s.utm_campaign || "",
    referrer: s.referrer || "",
    crm_status: "new"
  };
}

function leadRowFromContactForm(form) {
  const f = new FormData(form);
  const utm = getUTM();
  const get = function (k) { return (f.get(k) || "").toString().trim(); };
  return {
    visitor_id: getVisitorId(),
    lead_source: "californiamtg.com",
    lead_category: get("helpWith") || "Contact",
    full_name: get("fullName"),
    phone: get("phone"),
    email: get("email"),
    preferred_contact_method: get("contactMethod"),
    user_type: get("iAmA"),
    scenario_type: get("helpWith"),
    property_state: "",
    timeline: "",
    estimated_price_or_value: "",
    message: get("message"),
    answers: { iAmA: get("iAmA"), helpWith: get("helpWith"), via: "contact_form" },
    utm_source: utm.utm_source || "",
    utm_medium: utm.utm_medium || "",
    utm_campaign: utm.utm_campaign || "",
    referrer: document.referrer || "",
    crm_status: "new"
  };
}

// Save a lead: Supabase first, then CRM webhook. Always resolves (never breaks UX).
async function saveLead(row, eventName) {
  // Always keep a local copy so a lead is never lost before integration.
  try { window.localStorage.setItem("cm_last_lead", JSON.stringify(row)); } catch (e) {}

  const supabase = await getSupabase();
  if (supabase) {
    try {
      await supabase.from("leads").insert(row);                  // 1) save first
    } catch (e) {
      console.warn("[California Mortgage] lead insert failed:", e);
    }
    try { await track(eventName, { lead_category: row.lead_category }); } catch (e) {}

    // 2) attempt CRM; lead already stored. Status reconciliation (sent/pending)
    //    is intended to run server-side, since the browser anon role is insert-only.
    try {
      const res = await sendLeadToCRM(row);
      if (!res.ok && !res.skipped) console.warn("[California Mortgage] CRM webhook failed; lead remains in Supabase (crm_status=new/pending).");
    } catch (e) { /* ignore */ }
    return { stored: "supabase" };
  }

  // No Supabase configured -> Netlify Forms fallback (contact form only carries the form),
  // plus CRM attempt and the localStorage copy above.
  try { await sendLeadToCRM(row); } catch (e) {}
  return { stored: "local" };
}

/* ---------- public API ---------- */
window.CMTrack = function (eventName, data) { track(eventName, data); };

window.CMLeads = {
  isSupabaseConfigured: isConfigured,
  saveScenarioLead: function (lead) { return saveLead(leadRowFromScenario(lead), "scenario_completed"); },
  saveContactForm: function (form) {
    const row = leadRowFromContactForm(form);
    const p = saveLead(row, "contact_form_submitted");
    // If Supabase isn't configured, also POST to Netlify Forms so the lead is captured on deploy.
    if (!isConfigured()) {
      try {
        const body = new URLSearchParams(new FormData(form)).toString();
        fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body }).catch(function () {});
      } catch (e) { /* ignore */ }
    }
    return p;
  }
};

window.CMConsent = {
  status: getConsentStatus,
  getVisitorId: getVisitorId,
  reset: function () { resetConsent(); try { window.localStorage.removeItem(VISITOR_SAVED); } catch (e) {} renderBanner(); }
};

/* ---------- init ---------- */
getVisitorId(); // ensure an id exists
if (hasConsentDecision()) {
  if (getConsentStatus() === "accepted") { bumpVisit(); saveVisitorOnce(); initAutoTracking(); }
  else { saveVisitorOnce(); } // essential -> minimal functional record only
} else {
  renderBanner();
}

// "Manage cookie preferences" button (e.g. on the Privacy Policy page)
var manageBtn = document.getElementById("manageConsent");
if (manageBtn) manageBtn.addEventListener("click", function (e) { e.preventDefault(); window.CMConsent.reset(); });
