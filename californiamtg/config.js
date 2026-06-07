/* ============================================================
   California Mortgage — runtime configuration
   ------------------------------------------------------------
   This is a no-build static site (no Vite bundler), so values are
   provided here at runtime instead of import.meta.env. The Supabase
   ANON key is a *publishable* key and is safe in the browser as long
   as Row Level Security is enabled (see supabase/schema.sql).

   To enable Supabase + CRM, fill these in (or inject them at deploy):
     SUPABASE_URL       -> your project URL  (maps to VITE_SUPABASE_URL)
     SUPABASE_ANON_KEY  -> publishable anon key (VITE_SUPABASE_ANON_KEY)
     CRM_WEBHOOK_URL    -> optional Zapier/Make/WCCM webhook (VITE_CRM_WEBHOOK_URL)

   Leave blank to run without a backend: the site still works — the
   contact form falls back to Netlify Forms and leads are kept in
   localStorage, with a console warning.
   ============================================================ */
window.CM_CONFIG = {
  SUPABASE_URL: "",
  SUPABASE_ANON_KEY: "",
  CRM_WEBHOOK_URL: "",
  SITE: "californiamtg.com"
};
