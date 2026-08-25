#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"

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

print("Normalized local flagship output and WCCM contact data")
