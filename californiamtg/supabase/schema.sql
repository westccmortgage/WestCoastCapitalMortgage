-- ============================================================
-- California Mortgage — Supabase schema
-- Run this in the Supabase SQL editor.
--
-- Security model: the website uses the public ANON key in the browser.
-- Row Level Security is ENABLED on every table. The anon role may only
-- INSERT into visitors, visitor_events, and leads — it can NOT read them.
-- Read access is reserved for the service role / authenticated dashboards.
-- ============================================================

-- ---------- VISITORS ----------
create table if not exists public.visitors (
  id            uuid primary key default gen_random_uuid(),
  visitor_id    text unique not null,
  first_visit_at timestamptz,
  last_visit_at  timestamptz,
  visit_count   int default 1,
  consent_status text,
  landing_page  text,
  referrer      text,
  utm_source    text,
  utm_medium    text,
  utm_campaign  text,
  utm_content   text,
  utm_term      text,
  user_agent    text,
  screen_size   text,
  created_at    timestamptz default now()
);

-- ---------- VISITOR EVENTS ----------
create table if not exists public.visitor_events (
  id          uuid primary key default gen_random_uuid(),
  visitor_id  text,
  event_name  text,
  page_path   text,
  event_data  jsonb,
  created_at  timestamptz default now()
);
create index if not exists visitor_events_visitor_idx on public.visitor_events (visitor_id);
create index if not exists visitor_events_name_idx     on public.visitor_events (event_name);

-- ---------- LEADS ----------
create table if not exists public.leads (
  id                       uuid primary key default gen_random_uuid(),
  visitor_id               text,
  lead_source              text default 'californiamtg.com',
  lead_category            text,
  full_name                text,
  phone                    text,
  email                    text,
  preferred_contact_method text,
  user_type                text,
  scenario_type            text,
  property_state           text,
  timeline                 text,
  estimated_price_or_value text,
  message                  text,
  answers                  jsonb,
  utm_source               text,
  utm_medium               text,
  utm_campaign             text,
  referrer                 text,
  crm_status               text default 'new',
  created_at               timestamptz default now()
);
create index if not exists leads_visitor_idx on public.leads (visitor_id);
create index if not exists leads_created_idx  on public.leads (created_at);

-- ============================================================
-- Row Level Security
-- ============================================================
alter table public.visitors       enable row level security;
alter table public.visitor_events enable row level security;
alter table public.leads          enable row level security;

-- Anonymous (and authenticated) clients may INSERT only. No SELECT/UPDATE/DELETE.
drop policy if exists "anon insert visitors" on public.visitors;
create policy "anon insert visitors"
  on public.visitors for insert to anon, authenticated with check (true);

drop policy if exists "anon insert visitor_events" on public.visitor_events;
create policy "anon insert visitor_events"
  on public.visitor_events for insert to anon, authenticated with check (true);

drop policy if exists "anon insert leads" on public.leads;
create policy "anon insert leads"
  on public.leads for insert to anon, authenticated with check (true);

-- NOTE: No SELECT policies are created, so the anon key cannot read any rows.
-- Use the service_role key (server-side only) or an authenticated dashboard to
-- read leads/visitors. crm_status is set to 'new' on insert; reconcile delivery
-- status (sent/pending) server-side, since the browser role is insert-only.
