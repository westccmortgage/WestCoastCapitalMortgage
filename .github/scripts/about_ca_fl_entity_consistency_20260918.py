from pathlib import Path

p = Path("wccm-corporate/about.html")
s = p.read_text(encoding="utf-8")
old = s

replacements = {
    'Learn about West Coast Capital Mortgage, a California-licensed mortgage lender. NMLS #2817729. Serving CA, TX, FL, WA & more. Call 310-654-1577.':
        'Learn about West Coast Capital Mortgage Inc., a mortgage company serving borrowers in California and Florida with purchase, refinance, jumbo, Non-QM, bank-statement, DSCR, and investor financing. Company NMLS #2817729. Call 310-654-1577.',
    '<meta name="geo.region" content="US-CA">\n<meta name="geo.placename" content="California">\n': '',
    '"@type": "LocalBusiness",\n  "name": "West Coast Capital Mortgage",':
        '"@type": ["FinancialService", "LocalBusiness"],\n  "name": "West Coast Capital Mortgage Inc.",\n  "legalName": "West Coast Capital Mortgage Inc.",',
    '  "telephone": "+1-310-654-1577",\n  "email": "westccmortgage@gmail.com",':
        '  "telephone": "+1-310-654-1577",\n  "email": "westccmortgage@gmail.com",\n  "areaServed": ["California", "Florida"],\n  "serviceType": ["Home purchase mortgages", "Mortgage refinance", "Jumbo loans", "Non-QM loans", "Bank statement loans", "DSCR loans", "Investment property loans", "Condo financing", "Foreign national mortgage review", "Mortgage second opinion"],',
    'West Coast Capital Mortgage is a modern mortgage company focused on helping people buy homes, refinance, and build equity with confidence. We pair efficient technology with experienced, licensed guidance.':
        'West Coast Capital Mortgage Inc. is a modern mortgage company serving borrowers in California and Florida with purchase, refinance, jumbo, self-employed, investor, condo, and complex mortgage scenarios. We pair efficient technology with experienced, licensed guidance.',
    'Anatoliy Kanevsky is the founder of West Coast Capital Mortgage and a California real estate and mortgage professional with more than 20 years of experience helping borrowers, homeowners, Realtors, investors, and self-employed clients navigate real-world financing scenarios.':
        'Anatoliy Kanevsky is the founder of West Coast Capital Mortgage Inc. and a mortgage and real estate professional since 2004, helping borrowers, homeowners, Realtors, investors, and self-employed clients navigate real-world financing scenarios.',
    '<li>Founder, West Coast Capital Mortgage</li>': '<li>Founder, West Coast Capital Mortgage Inc.</li>',
    'West Coast Capital Mortgage. NMLS #2817729. CA DRE Corporation License #02440065.':
        'West Coast Capital Mortgage Inc. NMLS #2817729. CA DRE Corporation License #02440065.'
}

for a, b in replacements.items():
    if a not in s:
        raise SystemExit(f"Expected About-page source text not found: {a[:120]}")
    s = s.replace(a, b)

if s == old:
    raise SystemExit("No About-page changes applied")

p.write_text(s, encoding="utf-8")

check = p.read_text(encoding="utf-8")
assert 'California-licensed mortgage lender' not in check
assert 'name="geo.region"' not in check
assert 'name="geo.placename"' not in check
assert '"name": "West Coast Capital Mortgage Inc."' in check
assert '"areaServed": ["California", "Florida"]' in check
assert 'mortgage and real estate professional since 2004' in check
assert 'West Coast Capital Mortgage Inc. is a modern mortgage company serving borrowers in California and Florida' in check
print("About-page CA/FL entity consistency patch validated")
