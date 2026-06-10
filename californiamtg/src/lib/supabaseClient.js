/* ============================================================
   Supabase client (browser, no-build)
   ------------------------------------------------------------
   Loads @supabase/supabase-js from a CDN as an ES module and creates
   a singleton client from window.CM_CONFIG (see /config.js).

   Under a Vite migration you would instead read:
     import.meta.env.VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY
   and `import { createClient } from "@supabase/supabase-js"`.

   Returns null (with a console warning) when not configured, so callers
   can fall back gracefully. The anon key is publishable; security is
   enforced by Row Level Security (supabase/schema.sql).
   ============================================================ */

const cfg = (typeof window !== "undefined" && window.CM_CONFIG) || {};
const SUPABASE_URL = cfg.SUPABASE_URL || "";
const SUPABASE_ANON_KEY = cfg.SUPABASE_ANON_KEY || "";

let _client = null;
let _warned = false;

export function isConfigured() {
  return Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);
}

export async function getSupabase() {
  if (!isConfigured()) {
    if (!_warned) {
      _warned = true;
      console.warn(
        "[California Mortgage] Supabase is not configured. Set SUPABASE_URL and " +
        "SUPABASE_ANON_KEY in /config.js to enable visitor tracking and lead storage. " +
        "The site will continue to work (Netlify Forms / localStorage fallback)."
      );
    }
    return null;
  }
  if (_client) return _client;
  try {
    const { createClient } = await import("https://esm.sh/@supabase/supabase-js@2");
    _client = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
      auth: { persistSession: false }
    });
    return _client;
  } catch (err) {
    console.warn("[California Mortgage] Failed to load Supabase client:", err);
    return null;
  }
}
