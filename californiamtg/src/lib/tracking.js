/* ============================================================
   Visitor event tracking
   ------------------------------------------------------------
   Events are recorded ONLY when consent === "accepted". Under
   "essential" (or before a decision), tracking is a no-op — we keep
   only functional data (visitor_id, consent, form submissions).
   ============================================================ */
import { getSupabase } from "./supabaseClient.js";
import { getConsentStatus, getVisitorId } from "./consent.js";

function pushDataLayer(eventName, data) {
  // Google Tag Manager / Google Ads readiness: if a Google dataLayer is
  // present, expose the same consent-gated first-party events there. This is
  // intentionally a no-op until a Google tag is installed.
  if (!window.dataLayer || typeof window.dataLayer.push !== "function") return;
  try {
    window.dataLayer.push(Object.assign({ event: "cm_" + eventName }, data || {}));
  } catch (e) {
    console.debug("[dataLayer] push failed:", e);
  }
}

export async function track(eventName, data) {
  if (getConsentStatus() !== "accepted") return;        // gated by consent
  pushDataLayer(eventName, data);
  const supabase = await getSupabase();
  if (!supabase) { console.debug("[track]", eventName, data || {}); return; }
  try {
    await supabase.from("visitor_events").insert({
      visitor_id: getVisitorId(),
      site: (window.CM_CONFIG && window.CM_CONFIG.SITE) || "",
      event_name: eventName,
      page_path: window.location.pathname,
      event_data: data || {}
    });
  } catch (e) {
    console.debug("[track] insert failed:", e);
  }
}

/* Auto-wire common interactions (accepted consent only). */
export function initAutoTracking() {
  if (getConsentStatus() !== "accepted") return;

  track("page_view", {
    page: window.location.pathname,
    referrer: document.referrer || "",
    screen_size: window.screen ? window.screen.width + "x" + window.screen.height : ""
  });

  document.addEventListener("click", function (e) {
    const a = e.target.closest && e.target.closest("a");
    if (!a) return;
    const href = a.getAttribute("href") || "";
    const label = (a.textContent || "").trim().replace(/\s+/g, " ").slice(0, 120);

    if (a.classList.contains("audience-card")) {
      track("education_card_clicked", { href: href, label: (a.querySelector("h3") || {}).textContent || "" });
    } else if (href.indexOf("my1003app.com") !== -1) {
      track("full_application_clicked", { href: href, label: label });
    } else if (href.indexOf("/home-equity-review-california") !== -1) {
      track("home_equity_review_clicked", { href: href, label: label });
    } else if (href.indexOf("/buy-before-you-sell-california") !== -1) {
      track("buy_before_sell_clicked", { href: href, label: label });
    } else if (href.indexOf("/condo-project-prescreen") !== -1) {
      track("condo_prescreen_clicked", { href: href, label: label });
    } else if (href.indexOf("/second-look") !== -1) {
      track("second_look_clicked", { href: href, label: label });
    } else if (href.indexOf("/guides/pacific-palisades-rebuild-financing-2026") !== -1) {
      track("palisades_rebuild_clicked", { href: href, label: label });
    } else if (href.indexOf("/guides/") !== -1) {
      track("guide_clicked", { href: href, label: label });
    } else if (href.indexOf("wcci.online") !== -1) {
      track("ai_review_clicked", { href: href, label: label });
    } else if (href.indexOf("tel:") === 0) {
      track("phone_clicked", { href: href, label: label });
    } else if (href.indexOf("mailto:") === 0) {
      track("email_clicked", { href: href, label: label });
    }
  }, true);
}
