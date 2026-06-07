/* ============================================================
   CRM webhook (placeholder, opt-in)
   ------------------------------------------------------------
   Forwards a saved lead to an external workflow when a webhook URL is
   configured (window.CM_CONFIG.CRM_WEBHOOK_URL / VITE_CRM_WEBHOOK_URL).
   No-op when not configured — leads still live in Supabase.

   Flow expected by the caller (src/app.js):
     1. Save lead to Supabase first.
     2. Then call sendLeadToCRM(lead).
     3. If this fails, the lead stays in Supabase with crm_status = 'pending'.
   ============================================================ */

const cfg = (typeof window !== "undefined" && window.CM_CONFIG) || {};
const CRM_WEBHOOK_URL = cfg.CRM_WEBHOOK_URL || "";

/**
 * Attempt to deliver a lead to the configured CRM/automation webhook.
 * @returns {Promise<{ok:boolean, skipped?:boolean, error?:any}>}
 */
export async function sendLeadToCRM(lead) {
  // TODO: connect WCCM CRM endpoint
  // TODO: connect Zapier / Make webhook
  // TODO: connect email notification workflow
  if (!CRM_WEBHOOK_URL) {
    return { ok: false, skipped: true };
  }
  try {
    const res = await fetch(CRM_WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lead)
    });
    return { ok: res.ok };
  } catch (error) {
    return { ok: false, error };
  }
}

export function isCRMConfigured() {
  return Boolean(CRM_WEBHOOK_URL);
}
