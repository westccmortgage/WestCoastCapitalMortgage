/* ============================================================
   CRM webhook — DISABLED PLACEHOLDER (do not enable yet)
   ------------------------------------------------------------
   Per current plan, the site is Supabase-only. Nothing is sent to any
   CRM, Zapier, Make, or email workflow. This file is intentionally NOT
   imported anywhere and performs no network calls.

   Leads are stored in Supabase with crm_status = "not_connected".

   FUTURE (do not enable now): when CRM is approved, add a webhook URL to
   config.js, import sendLeadToCRM() in src/app.js, call it AFTER the
   Supabase insert, and update crm_status server-side.
   ============================================================ */

// Hard-disabled. Returns immediately without sending anything.
export async function sendLeadToCRM(/* lead */) {
  return { ok: false, disabled: true };
}

export function isCRMConfigured() {
  return false;
}
