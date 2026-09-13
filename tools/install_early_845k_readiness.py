#!/usr/bin/env python3
"""Build-time hardening for the early-$845K paid-search landing page.

Ensures Netlify registers attribution fields populated by script.js and makes the
new landing discoverable in the production sitemap. Idempotent and scoped.
"""
from pathlib import Path

PAGE = Path("wccm-corporate/early-conforming-loan-limit-845000.html")
SITEMAP = Path("wccm-corporate/sitemap.xml")
MARKER = '<input type="hidden" name="program_interest" value="Early Conforming Limit up to $845,000">'
ATTRIBUTION = """\
<input type="hidden" name="utm_source" value="">
<input type="hidden" name="utm_medium" value="">
<input type="hidden" name="utm_campaign" value="">
<input type="hidden" name="utm_term" value="">
<input type="hidden" name="utm_content" value="">
<input type="hidden" name="gclid" value="">
<input type="hidden" name="gbraid" value="">
<input type="hidden" name="wbraid" value="">
<input type="hidden" name="landing_page" value="">
<input type="hidden" name="conversion_page" value="">
<input type="hidden" name="source_path" value="">
<input type="hidden" name="referrer" value="">"""
SITEMAP_URL = "https://westcoastcapitalmortgage.com/early-conforming-loan-limit-845000"
SITEMAP_ENTRY = f"  <url><loc>{SITEMAP_URL}</loc><lastmod>2026-09-12</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n"

if not PAGE.exists():
    raise SystemExit(f"Missing paid landing page: {PAGE}")

text = PAGE.read_text(encoding="utf-8")
text = text.replace(
    "<title>Early Conforming Loan Limit Up to $845,000 | California Mortgage</title>",
    "<title>Early Conforming Loan Limit Up to $845,000 | West Coast Capital Mortgage</title>",
)

if 'name="gclid"' not in text:
    if MARKER not in text:
        raise SystemExit("Could not locate early-limit form marker")
    text = text.replace(MARKER, MARKER + ATTRIBUTION, 1)

PAGE.write_text(text, encoding="utf-8")

if SITEMAP.exists():
    sitemap = SITEMAP.read_text(encoding="utf-8")
    if SITEMAP_URL not in sitemap:
        sitemap = sitemap.replace("</urlset>", SITEMAP_ENTRY + "</urlset>", 1)
        SITEMAP.write_text(sitemap, encoding="utf-8")

print("Early $845K landing readiness installed")
