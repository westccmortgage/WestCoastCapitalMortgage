#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"

LOCAL_SLUGS = [
    "manhattan-beach",
    "palos-verdes-estates",
    "rancho-palos-verdes",
    "rolling-hills",
    "calabasas",
    "encino",
    "sherman-oaks",
    "pacific-palisades",
    "westlake-village",
    "marina-del-rey",
    "torrance",
    "hermosa-beach",
    "redondo-beach",
    "culver-city",
    "studio-city",
    "woodland-hills",
    "brentwood",
    "west-los-angeles",
]

# Normalize generated JSON-LD types for neighborhood/community geographies.
for path in (ROOT / "mortgage").glob("*.html"):
    text = path.read_text(encoding="utf-8")
    text = text.replace('"areaServed": {"@type": "Neighborhood",', '"areaServed": {"@type": "Place",')
    text = text.replace('"areaServed": {"@type": "Community",', '"areaServed": {"@type": "Place",')
    path.write_text(text, encoding="utf-8")

# Small punctuation cleanup on the local-market hub.
hub = ROOT / "california-mortgage-locations.html"
text = hub.read_text(encoding="utf-8")
text = text.replace("West Coast Capital Mortgage Inc..", "West Coast Capital Mortgage Inc.")
hub.write_text(text, encoding="utf-8")

# The Loans hub is touched by this project, so remove the legacy direct phone
# from its footer and use the current standard WCCM contact/disclosure block.
loans = ROOT / "loans.html"
text = loans.read_text(encoding="utf-8")
old_contact = '<p class="footer-contact"><b>Office / Loan Officer Questions:</b> <a href="tel:3106541577">310-654-1577</a><br><b>Anatoliy Direct:</b> <a href="tel:3106865053">310-686-5053</a><br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a></p>'
new_contact = '<p class="footer-contact"><b>Phone:</b> <a href="tel:3106541577">(310) 654-1577</a><br><b>Office:</b> 150 E Olive Ave, Unit 112, Burbank, CA 91502<br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a></p>'
text = text.replace(old_contact, new_contact)
old_disclosure = 'West Coast Capital Mortgage. NMLS #2817729. CA DRE Corporation License #02440065. Anatoliy Kanevsky NMLS #2775380, CA Broker DRE #01385024. Equal Housing Opportunity.'
new_disclosure = 'West Coast Capital Mortgage Inc. Company NMLS #2817729. CA DRE Corporation License #02440065. Anatoliy Kanevsky NMLS #2775380, CA Broker DRE #01385024. Equal Housing Opportunity.'
text = text.replace(old_disclosure, new_disclosure)
loans.write_text(text, encoding="utf-8")

# Preserve the history of the retired city-level Jumbo/DSCR URLs. These rules
# intentionally sit ABOVE the broad county/metro consolidation block, so a
# visitor or crawler reaching an old high-value city URL lands on the new,
# substantive local page instead of a generic county page. The old source URL
# remains a 301 and therefore should not itself be indexed.
redirects = ROOT / "_redirects"
rtext = redirects.read_text(encoding="utf-8")
start = "# --- curated local flagship overrides 2026-08-25 ---"
end = "# --- end curated local flagship overrides ---"
lines = [start]
for slug in LOCAL_SLUGS:
    lines.append(f"/loans/jumbo/{slug}    /mortgage/{slug}    301!")
    lines.append(f"/loans/dscr/{slug}    /mortgage/{slug}    301!")
lines.append(end)
block = "\n".join(lines) + "\n\n"
rtext = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n*", "", rtext, flags=re.S)
geo_marker = "# --- geo consolidation 2026-07-30: city pages merged into county/metro pages ---"
if geo_marker in rtext:
    rtext = rtext.replace(geo_marker, block + geo_marker, 1)
else:
    rtext = block + rtext
redirects.write_text(rtext, encoding="utf-8")

print("Normalized local flagship output, WCCM contact data, and curated legacy redirects")
