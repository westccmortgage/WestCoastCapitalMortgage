// ============================================================
// Supabase Edge Function: lead-email
// Emails a notification whenever a new row is inserted into public.leads.
// Trigger: a Supabase Database Webhook on leads INSERT (see SETUP below).
// Secret required: RESEND_API_KEY  (Resend is already verified for californiamtg.com)
// ------------------------------------------------------------
// SETUP (all in the Supabase dashboard — no CLI needed):
//   1) Resend -> API Keys -> create a key (re_...). Copy it.
//   2) Supabase -> Edge Functions -> Create a function named "lead-email",
//      paste this file, Deploy.
//   3) Supabase -> Edge Functions -> Secrets (Manage secrets) ->
//      add RESEND_API_KEY = <your re_... key>.
//   4) Supabase -> Database -> Webhooks -> Create a webhook:
//        Table: leads | Events: INSERT
//        Type: "Supabase Edge Functions" -> select "lead-email"
//      (Supabase signs the request with a valid key, so leave Verify JWT on.
//       If you hit a 401, turn Verify JWT OFF for this function.)
// ============================================================
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") ?? "";
const TO = ["info@californiamtg.com"];                       // where leads are received
const FROM = "California Mortgage <leads@californiamtg.com>"; // any address on the verified domain

const esc = (v: unknown) =>
  String(v ?? "").replace(/[<&>]/g, (c) => ({ "<": "&lt;", "&": "&amp;", ">": "&gt;" }[c]!));

serve(async (req) => {
  if (!RESEND_API_KEY) return new Response("Missing RESEND_API_KEY secret", { status: 500 });
  try {
    const payload = await req.json();
    const r = payload.record ?? payload; // DB webhook sends { type, table, record, ... }

    const fields: [string, unknown][] = [
      ["Name", r.full_name], ["Phone", r.phone], ["Email", r.email],
      ["Preferred contact", r.preferred_contact_method],
      ["Lead category", r.lead_category], ["Scenario", r.scenario_type],
      ["User type", r.user_type], ["State", r.property_state], ["Timeline", r.timeline],
      ["Est. price/value", r.estimated_price_or_value], ["Message", r.message],
      ["Site", r.site], ["Source", r.lead_source],
      ["UTM source", r.utm_source], ["UTM campaign", r.utm_campaign],
      ["Referrer", r.referrer], ["Landing page", r.landing_page],
    ];
    const rows = fields
      .filter(([, v]) => v)
      .map(([k, v]) =>
        `<tr><td style="padding:4px 12px;color:#6f675b">${k}</td>` +
        `<td style="padding:4px 12px;color:#2b2825"><b>${esc(v)}</b></td></tr>`)
      .join("");
    const answers = r.answers
      ? `<p style="color:#6f675b;margin:14px 0 4px">Answers</p><pre style="background:#f6f2ea;padding:12px;border-radius:8px;white-space:pre-wrap;color:#2b2825">${esc(JSON.stringify(r.answers, null, 2))}</pre>`
      : "";
    const html =
      `<div style="font-family:Inter,Arial,sans-serif;max-width:640px">` +
      `<h2 style="color:#2b2825">New lead — ${esc(r.lead_category || "California Mortgage")}</h2>` +
      `<table style="border-collapse:collapse">${rows}</table>${answers}` +
      `<p style="color:#9a917f;font-size:12px;margin-top:16px">California Mortgage · ${esc(r.created_at || "")} · crm_status: ${esc(r.crm_status || "not_connected")}</p>` +
      `</div>`;

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: FROM,
        to: TO,
        reply_to: r.email || undefined,
        subject: `New lead: ${r.full_name || "Unknown"} — ${r.lead_category || "scenario"} (${r.site || ""})`,
        html,
      }),
    });
    if (!res.ok) return new Response("Resend error: " + (await res.text()), { status: 502 });
    return new Response("ok", { status: 200 });
  } catch (e) {
    return new Response("error: " + (e instanceof Error ? e.message : String(e)), { status: 500 });
  }
});
