from pathlib import Path
import json
import re

root = Path('wccm-corporate')
products = {
    'bank-statement-loans.html': {
        'name': 'Bank Statement Mortgage Loans',
        'section': '''<!-- AI-VISIBILITY-CA-FL:bank-statement-loans-20260910 -->
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">California &amp; Florida</span><h2>Are Bank Statement Loans Available in California and Florida?</h2></div>
  <p><strong>Direct answer:</strong> West Coast Capital Mortgage reviews bank-statement mortgage scenarios for eligible borrowers and properties in California and Florida. Program availability, statement period, deposit analysis, expense treatment, credit, down payment and reserve requirements vary by lender and file.</p>
  <h3>What should a self-employed borrower compare first?</h3>
  <p>Compare traditional self-employed underwriting with bank-statement and other Non-QM paths before assuming tax-return income is the only option. For investment property, DSCR may also be worth comparing because the qualification approach is different.</p>
  <div class="btn-row"><a class="btn btn-blue" href="florida.html">Florida Mortgage Options</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed Borrowers</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM Options</a></div>
</div></section>
'''
    },
    'dscr-loans.html': {
        'name': 'DSCR Investment Property Financing',
        'section': '''<!-- AI-VISIBILITY-CA-FL:dscr-loans-20260910 -->
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">California &amp; Florida</span><h2>Can Investors Use DSCR Financing in California and Florida?</h2></div>
  <p><strong>Direct answer:</strong> Yes. West Coast Capital Mortgage reviews eligible DSCR investment-property scenarios in California and Florida. DSCR programs generally evaluate the property's rental cash flow under lender-specific rules rather than relying primarily on the borrower's employment income.</p>
  <h3>Should an investor compare DSCR with conventional financing?</h3>
  <p>Often, yes. A conventional rental-property loan and a DSCR loan can evaluate income, reserves, property use and documentation differently. Comparing both before an offer can show which structure better fits the borrower and property.</p>
  <div class="btn-row"><a class="btn btn-blue" href="florida.html">Florida Investor Financing</a><a class="btn btn-outline" href="investment-property-loans.html">Investment Property Loans</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM Options</a></div>
</div></section>
'''
    },
    'non-qm-loans.html': {
        'name': 'Non-QM Mortgage Financing',
        'section': '''<!-- AI-VISIBILITY-CA-FL:non-qm-loans-20260910 -->
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">California &amp; Florida</span><h2>What Non-QM Mortgage Options Are Available in California and Florida?</h2></div>
  <p><strong>Direct answer:</strong> West Coast Capital Mortgage reviews Non-QM scenarios in California and Florida for borrowers whose income or property profile may not fit standard Agency underwriting. Depending on the file, possible paths can include bank-statement, asset-based or asset-utilization, DSCR/investor, and foreign-national financing.</p>
  <h3>When should a borrower compare Non-QM with a conventional loan?</h3>
  <p>Before choosing an alternative-documentation program, compare whether conventional underwriting can work with the borrower's documented income, assets and property. Non-QM can be useful when standard documentation does not accurately reflect the borrower's financial profile, but eligibility and terms vary by lender.</p>
  <div class="btn-row"><a class="btn btn-blue" href="florida.html">Florida Mortgage Options</a><a class="btn btn-outline" href="bank-statement-loans.html">Bank Statement</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a><a class="btn btn-outline" href="foreign-national-loans.html">Foreign National</a></div>
</div></section>
'''
    },
    'foreign-national-loans.html': {
        'name': 'Foreign National Mortgage Financing',
        'section': '''<!-- AI-VISIBILITY-CA-FL:foreign-national-loans-20260910 -->
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">California &amp; Florida</span><h2>Can Foreign Nationals Finance Property in Florida or California?</h2></div>
  <p><strong>Direct answer:</strong> Yes, eligible international buyers may have foreign-national mortgage options for property in Florida or California. Depending on the program, lenders may use a passport, foreign income or bank documentation, assets and reserves, and alternative credit references instead of a standard U.S. borrower profile.</p>
  <h3>What should an international buyer compare before making an offer?</h3>
  <p>Compare intended property use, down payment, reserve requirements, available documentation, currency-transfer timing and whether the property is a second home or investment. Investment-property buyers may also compare a foreign-national program with DSCR where lender guidelines permit.</p>
  <div class="btn-row"><a class="btn btn-blue" href="florida.html">Florida Mortgage Options</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM</a></div>
</div></section>
'''
    },
}

for filename, cfg in products.items():
    p = root / filename
    text = p.read_text()
    text = text.replace('<meta name="geo.region" content="US-CA">\n', '')
    text = text.replace('<meta name="geo.placename" content="California">\n', '')

    marker = f'AI-VISIBILITY-CA-FL:{filename.split(".")[0]}-20260910'
    if marker not in text:
        anchor = '<section><div class="wrap"><div class="wcci-cta">'
        if anchor in text:
            text = text.replace(anchor, cfg['section'] + '\n' + anchor, 1)
        elif '<footer class="site-footer">' in text:
            text = text.replace('<footer class="site-footer">', cfg['section'] + '\n<footer class="site-footer">', 1)
        else:
            raise RuntimeError(f'No safe section insertion anchor in {filename}')

    schema_marker = f'AI-VISIBILITY-CA-FL-SCHEMA:{filename.split(".")[0]}-20260910'
    if schema_marker not in text:
        url = 'https://westcoastcapitalmortgage.com/' + filename.replace('.html', '')
        data = {
            '@context': 'https://schema.org',
            '@type': 'Service',
            'name': cfg['name'],
            'serviceType': cfg['name'],
            'url': url,
            'areaServed': [
                {'@type': 'State', 'name': 'California'},
                {'@type': 'State', 'name': 'Florida'}
            ],
            'provider': {
                '@type': 'Organization',
                'name': 'West Coast Capital Mortgage Inc.',
                'url': 'https://westcoastcapitalmortgage.com/',
                'identifier': 'NMLS #2817729',
                'telephone': '+1-310-654-1577'
            }
        }
        block = f'\n<!-- {schema_marker} -->\n<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'
        text = text.replace('</head>', block + '</head>', 1)

    p.write_text(text)

p = root / 'florida.html'
text = p.read_text()
condo_marker = 'AI-VISIBILITY-FL-CONDO-20260910'
condo_section = '''<!-- AI-VISIBILITY-FL-CONDO-20260910 -->
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Florida condo financing</span><h2>How Does Condo Financing Differ in Florida?</h2></div>
  <p><strong>Direct answer:</strong> Condo financing can require both borrower underwriting and a separate review of the condominium project. Depending on the loan program and project, lenders may review project eligibility, insurance, association financials and reserves, litigation or critical-repair issues, and other condominium documentation before a loan can be completed.</p>
  <h3>What should a Florida condo buyer review before making an offer?</h3>
  <p>Ask early whether the project and unit are likely to fit the intended loan program, especially for attached, coastal or high-rise properties. A strong borrower can still face a financing issue if the condominium project does not meet the selected program's requirements.</p>
  <h3>Can self-employed or foreign-national buyers finance Florida condos?</h3>
  <p><strong>Direct answer:</strong> Potentially, yes. Depending on borrower and project eligibility, possible paths may include conventional or jumbo financing, bank-statement or other Non-QM programs, and foreign-national options. Project requirements vary by lender and program.</p>
  <div class="btn-row"><a class="btn btn-blue" href="jumbo-loans.html">Jumbo Loans</a><a class="btn btn-outline" href="bank-statement-loans.html">Bank Statement</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM</a><a class="btn btn-outline" href="foreign-national-loans.html">Foreign National</a></div>
</div></section>
'''
if condo_marker not in text:
    anchor = '<section class="bg-light"><div class="wrap">\n  <div class="founder-grid founder-preview">'
    if anchor not in text:
        raise RuntimeError('Florida condo insertion anchor not found')
    text = text.replace(anchor, condo_section + '\n' + anchor, 1)

faq_marker = 'AI-VISIBILITY-FL-CONDO-SCHEMA-20260910'
if faq_marker not in text:
    faq = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': 'How does condo financing differ in Florida?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Condo financing can require both borrower underwriting and a separate review of the condominium project. Depending on the program and project, lenders may review project eligibility, insurance, association financials and reserves, litigation or critical-repair issues, and other condominium documentation.'}},
            {'@type': 'Question', 'name': 'Can self-employed or foreign-national buyers finance Florida condos?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Potentially, yes. Depending on borrower and project eligibility, possible paths may include conventional or jumbo financing, bank-statement or other Non-QM programs, and foreign-national options. Project requirements vary by lender and program.'}}
        ]
    }
    block = f'\n<!-- {faq_marker} -->\n<script type="application/ld+json">{json.dumps(faq, separators=(",", ":"))}</script>\n'
    text = text.replace('</head>', block + '</head>', 1)
p.write_text(text)

for p in [root / x for x in list(products) + ['florida.html']]:
    t = p.read_text()
    if t.count('<link rel="canonical"') != 1:
        raise RuntimeError(f'Canonical count failure: {p}')
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S):
        json.loads(raw)
    if 'washington-mortgage-loans' in t or 'new-york-long-island-mortgage-loans' in t:
        raise RuntimeError(f'Pending-state link reintroduced: {p}')

for name in products:
    t = (root / name).read_text()
    if '<meta name="geo.region" content="US-CA">' in t:
        raise RuntimeError(f'Single-state geo meta remains: {name}')
    if '"name":"California"' not in t or '"name":"Florida"' not in t:
        raise RuntimeError(f'CA/FL schema missing: {name}')

if 'How Does Condo Financing Differ in Florida?' not in (root / 'florida.html').read_text():
    raise RuntimeError('Florida condo AEO section missing')

print('AI visibility validation passed')
