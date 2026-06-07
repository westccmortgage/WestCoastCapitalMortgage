/* ============================================================
   Visitor event tracking
   ------------------------------------------------------------
   Events are recorded ONLY when consent === "accepted". Under
   "essential" (or before a decision), tracking is a no-op — we keep
   only functional data (visitor_id, consent, form submissions).
   ============================================================ */
import { getSupabase } from "./supabaseClient.js";
import { getConsentStatus, getVisitorId } from "./consent.js";

export async function track(eventName, data) {
  if (getConsentStatus() !== "accepted") return;        // gated by consent
  const supabase = await getSupabase();
  if (!supabase) { console.debug("[track]", eventName, data || {}); return; }
  try {
    await supabase.from("visitor_events").insert({
      visitor_id: getVisitorId(),
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
    if (a.classList.contains("audience-card")) {
      track("education_card_clicked", { href: href, label: (a.querySelector("h3") || {}).textContent || "" });
    } else if (href.indexOf("wcci.online") !== -1) {
      track("ai_review_clicked", { href: href });
    } else if (href.indexOf("tel:") === 0) {
      track("phone_clicked", { href: href });
    } else if (href.indexOf("mailto:") === 0) {
      track("email_clicked", { href: href });
    }
  }, true);
}
