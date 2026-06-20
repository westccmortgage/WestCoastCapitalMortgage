-- ============================================================
-- California Mortgage / WCCM / Suncoast — add per-brand "site" tag
-- Run this ONCE in the Supabase SQL editor (safe to re-run).
-- Lets one project hold all three brands, filterable by site:
--   californiamtg.com | westccmortgage.com | suncoastcapitalmortgage.com
-- ============================================================
alter table public.visitors       add column if not exists site text;
alter table public.visitor_events add column if not exists site text;
alter table public.leads          add column if not exists site text;

create index if not exists visitors_site_idx       on public.visitors (site);
create index if not exists visitor_events_site_idx on public.visitor_events (site);
create index if not exists leads_site_idx          on public.leads (site);
