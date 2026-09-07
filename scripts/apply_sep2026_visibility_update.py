from pathlib import Path
import re, json, html, sys

ROOT=Path('.')
DATE='2026-09-07'
changed=[]
notes=[]

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s):
    Path(p).write_text(s,encoding='utf-8'); changed.append(str(p))

def inject_before_conversion(path, marker, block):
    p=Path(path); s=read(p)
    if marker in s: return
    anchors=['<section><div class="wrap"><div class="wcci-cta">','<section><div class="wrap"><div class="cta-band">','<footer class="site-footer">','</body>']
    for a in anchors:
        if a in s:
            s=s.replace(a, block+'\n'+a,1); write(p,s); return
    raise RuntimeError(f'No insertion anchor in {path}')

def add_schema(path, marker, schema):
    p=Path(path); s=read(p)
    if marker in s: return
    block=f'\n<!-- {marker} -->\n<script type="application/ld+json">{json.dumps(schema,separators=(",",":"))}</script>\n'
    if '</head>' not in s: raise RuntimeError(f'No head in {path}')
    s=s.replace('</head>',block+'</head>',1); write(p,s)

def set_description(path, desc):
    p=Path(path); s=read(p)
    ns=re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc,quote=True)}">', s, count=1)
    ns=re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc,quote=True)}">', ns, count=1)
    ns=re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{html.escape(desc,quote=True)}">', ns, count=1)
    if ns!=s: write(p,ns)

def faq_schema(url, faqs):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}

W='wccm-corporate'; S='suncoast-corporate'

# ---------- Shared content blocks ----------
investor_faqs=[
('Can short-term rental income be used to qualify?','Potentially, in eligible scenarios. Conventional Agency, DSCR and Non-QM programs evaluate short-term-rental income differently. Eligibility depends on the borrower, property, legal rental use, documentation and current Agency or lender guidelines.'),
('When can conventional financing work for a rental property?','Conventional financing may work when the borrower, property, occupancy, rental-income history and required documentation satisfy current Agency and lender requirements. A rental-property analysis should compare the conventional path before assuming DSCR is required.'),
('When may DSCR be a better option?','DSCR may be worth comparing when property cash flow is stronger than the borrower’s traditional qualifying income, or when an investor prefers a property-income-focused underwriting approach. Program terms and documentation vary.'),
('What documentation may be required for rental income?','Documentation varies by scenario and may include leases, tax returns or Schedule E history, appraisal market-rent analysis, evidence of current housing payments, proof of legal short-term-rental use, asset and reserve documentation, or other items required by the applicable program.')]

w_invest=f'''<!-- SEP2026-AEO:investor-comparison -->
<section class="bg-light"><div class="wrap">
  <span class="eyebrow">Updated September 2026</span>
  <h2>Conventional vs. DSCR: Which Works Better for Your Rental Property?</h2>
  <p><strong>Direct answer:</strong> A rental property does not automatically require a DSCR or Non-QM loan. Some investors may have a conventional Agency option, while DSCR or another Non-QM structure may be more appropriate in other scenarios. The right comparison depends on the borrower, property, rental history, documentation and current Agency and lender guidelines.</p>
  <div class="grid grid-3">
    <div class="card"><h3>Conventional</h3><p>May use Agency rental-income rules together with the borrower’s overall income, credit, assets and property eligibility. Documentation requirements vary by scenario.</p></div>
    <div class="card"><h3>DSCR</h3><p>Designed for investment-property scenarios where qualifying focuses primarily on property cash flow rather than the borrower’s traditional employment income.</p></div>
    <div class="card"><h3>Non-QM</h3><p>May provide alternative documentation or property structures when an Agency loan is not the best fit. Terms and eligibility vary by program.</p></div>
  </div>
  <h2 style="margin-top:38px">Short-Term Rental / Airbnb-Type Property Questions</h2>
  <details class="acc"><summary>Can short-term rental income be used to qualify?</summary><div class="acc-body">Potentially, in eligible scenarios. Conventional Agency, DSCR and Non-QM programs evaluate short-term-rental income differently. Eligibility depends on the borrower, property, legal rental use, documentation and current Agency or lender guidelines.</div></details>
  <details class="acc"><summary>When can conventional financing work?</summary><div class="acc-body">It may work when the borrower, property, occupancy, rental-income history and required documentation satisfy current Agency and lender requirements. We compare the conventional path before assuming DSCR is required.</div></details>
  <details class="acc"><summary>When may DSCR be a better option?</summary><div class="acc-body">DSCR may be worth comparing when property cash flow is stronger than the borrower’s traditional qualifying income, or when an investor prefers a property-income-focused approach. Program terms and documentation vary.</div></details>
  <details class="acc"><summary>What documentation may be required?</summary><div class="acc-body">Depending on the scenario, documentation may include leases, tax returns or Schedule E history, appraisal market-rent analysis, evidence of current housing payments, proof of legal short-term-rental use, assets/reserves, or other program-specific items.</div></details>
  <p style="margin-top:24px"><strong>Have a rental property or short-term rental? We can compare Conventional, DSCR and Non-QM options before you choose a loan.</strong></p>
  <div class="btn-row"><a class="btn btn-blue" href="conventional-loans.html">Conventional Loans</a><a class="btn btn-outline" href="dscr-loans.html">DSCR Loans</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM Loans</a></div>
</div></section>'''
inject_before_conversion(f'{W}/investment-property-loans.html','SEP2026-AEO:investor-comparison',w_invest)
add_schema(f'{W}/investment-property-loans.html','SEP2026-SCHEMA:investor-faq',faq_schema('https://westcoastcapitalmortgage.com/investment-property-loans',investor_faqs))

w_dscr='''<!-- SEP2026-AEO:dscr-conventional -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Updated September 2026</span>
<h2>Do I Need a DSCR Loan for Every Rental Property?</h2>
<p><strong>Direct answer:</strong> No. Some rental-property borrowers may have a conventional Agency option, while others may be better served by DSCR or another Non-QM structure. We compare the borrower, property, rental-income documentation and current program rules rather than assuming one loan type.</p>
<div class="grid grid-3"><div class="card"><h3>Conventional</h3><p>Potential fit when Agency borrower, property and rental-income documentation requirements can be met.</p></div><div class="card"><h3>DSCR</h3><p>Potential fit when investment-property cash flow is the primary qualification path.</p></div><div class="card"><h3>Other Non-QM</h3><p>Potential fit for alternative income documentation or scenarios outside standard Agency guidelines.</p></div></div>
<h3 style="margin-top:28px">Can a short-term rental use conventional financing?</h3><p>In some eligible scenarios, short-term-rental income may be considered under current Agency guidance. Property eligibility, legal short-term-rental use, rental history, appraisal/rent documentation and lender requirements all matter. This is a scenario analysis, not a qualification promise.</p>
<div class="btn-row"><a class="btn btn-blue" href="investment-property-loans.html">Compare Investor Options</a><a class="btn btn-outline" href="conventional-loans.html">Conventional</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed</a></div>
</div></section>'''
inject_before_conversion(f'{W}/dscr-loans.html','SEP2026-AEO:dscr-conventional',w_dscr)
add_schema(f'{W}/dscr-loans.html','SEP2026-SCHEMA:dscr-conventional',faq_schema('https://westcoastcapitalmortgage.com/dscr-loans',[
('Do I need a DSCR loan for every rental property?','No. Some investors may have a conventional Agency option. The appropriate path depends on borrower, property, rental-income documentation and current program requirements.'),
('Can a short-term rental use conventional financing?','In some eligible scenarios, short-term-rental income may be considered under current Agency guidance, subject to property eligibility, legal use, rental history, documentation and lender requirements.')]))

self_faqs=[
('Can I get a mortgage if my tax returns show low income?','Possibly. Tax-return income is only one potential qualification path. Depending on the borrower and property, traditional Agency analysis, bank statements, asset-based or asset-utilization programs, or DSCR for an investment property may be worth comparing.'),
('Can bank statements be used instead of tax returns?','Some non-QM bank-statement programs can evaluate qualifying income from eligible business or personal bank deposits rather than relying solely on tax-return income. Documentation, expense treatment and eligibility vary by program.'),
('Can assets be used to qualify for a mortgage?','Some mortgage programs may use eligible assets or an asset-utilization calculation as part of qualification. The treatment of assets, reserves and required documentation varies by program.'),
('What mortgage options exist for a self-employed real estate investor?','A self-employed investor may be able to compare traditional Agency documentation, bank-statement programs, asset-based or asset-utilization programs, DSCR and other Non-QM structures, depending on the borrower, property and transaction.')]
w_self='''<!-- SEP2026-AEO:self-employed-comparison -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Qualification paths</span><h2>Which Mortgage Qualification Method Can Work for a Self-Employed Borrower?</h2>
<p><strong>Direct answer:</strong> Self-employed does not automatically mean Non-QM. We first compare the qualification methods that may fit the borrower and property, then evaluate documentation, pricing and structure under current program guidelines.</p>
<div class="grid grid-4"><div class="card"><h3>Traditional Income Documentation</h3><p>Agency or other traditional underwriting may work when tax returns and applicable income analysis support the loan.</p></div><div class="card"><h3>Bank Statement</h3><p>Some Non-QM programs analyze eligible deposits and business-expense factors rather than relying solely on taxable net income.</p></div><div class="card"><h3>Asset-Based / Asset Utilization</h3><p>Some programs can evaluate eligible liquid or other qualifying assets using program-specific calculations and reserve rules.</p></div><div class="card"><h3>DSCR for Investment Property</h3><p>For eligible investment properties, DSCR programs may focus primarily on property cash flow rather than employment income.</p></div></div>
<h2 style="margin-top:36px">Self-Employed Mortgage Questions</h2>
<details class="acc"><summary>Can I get a mortgage if my tax returns show low income?</summary><div class="acc-body">Possibly. Tax-return income is one path, not the only path. Depending on the borrower and property, traditional Agency analysis, bank statements, asset-based or asset-utilization programs, or DSCR for an investment property may be worth comparing.</div></details>
<details class="acc"><summary>Can bank statements be used instead of tax returns?</summary><div class="acc-body">Some Non-QM bank-statement programs can evaluate qualifying income from eligible deposits rather than relying solely on tax-return income. Documentation and expense treatment vary.</div></details>
<details class="acc"><summary>Can assets be used to qualify for a mortgage?</summary><div class="acc-body">Some programs may use eligible assets or an asset-utilization calculation. Asset treatment, reserves and documentation vary by program.</div></details>
<details class="acc"><summary>What mortgage options exist for a self-employed real estate investor?</summary><div class="acc-body">Potential paths can include traditional Agency documentation, bank-statement programs, asset-based or asset-utilization programs, DSCR and other Non-QM structures.</div></details>
<div class="btn-row"><a class="btn btn-blue" href="bank-statement-loans.html">Bank Statement</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a><a class="btn btn-outline" href="investment-property-loans.html">Investor Loans</a></div>
</div></section>'''
inject_before_conversion(f'{W}/self-employed-borrowers.html','SEP2026-AEO:self-employed-comparison',w_self)
add_schema(f'{W}/self-employed-borrowers.html','SEP2026-SCHEMA:self-employed',faq_schema('https://westcoastcapitalmortgage.com/self-employed-borrowers',self_faqs))
set_description(f'{W}/self-employed-borrowers.html','Compare mortgage qualification paths for self-employed borrowers, including traditional income documentation, bank statements, asset-based options and DSCR for investment property. West Coast Capital Mortgage Inc. NMLS #2817729.')

w_bank='''<!-- SEP2026-AEO:bank-statement-comparison -->
<section class="bg-light"><div class="wrap"><h2>Do Self-Employed Borrowers Always Need a Bank-Statement Loan?</h2><p><strong>Direct answer:</strong> No. A bank-statement program is one possible path. A self-employed borrower should also compare traditional Agency income analysis, asset-based or asset-utilization options, and DSCR when the property is an investment property.</p><div class="btn-row"><a class="btn btn-blue" href="self-employed-borrowers.html">Compare Self-Employed Options</a><a class="btn btn-outline" href="conventional-loans.html">Conventional</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a><a class="btn btn-outline" href="non-qm-loans.html">Non-QM</a></div></div></section>'''
inject_before_conversion(f'{W}/bank-statement-loans.html','SEP2026-AEO:bank-statement-comparison',w_bank)
add_schema(f'{W}/bank-statement-loans.html','SEP2026-SCHEMA:bank-statement',faq_schema('https://westcoastcapitalmortgage.com/bank-statement-loans',[('Do self-employed borrowers always need a bank-statement loan?','No. Bank-statement financing is one possible path. Traditional Agency income analysis, asset-based or asset-utilization options, and DSCR for investment property may also be worth comparing depending on the scenario.')]))

w_nonqm='''<!-- SEP2026-AEO:nonqm-agency-first -->
<section class="bg-light"><div class="wrap"><h2>When Should a Borrower Compare Conventional Before Non-QM?</h2><p><strong>Direct answer:</strong> When the borrower and property may satisfy Agency requirements, it is worth comparing a conventional structure before assuming Non-QM is required. Non-QM can remain valuable for alternative income documentation, investment-property cash flow, asset-based qualification or other scenarios outside standard Agency guidelines.</p><div class="btn-row"><a class="btn btn-blue" href="conventional-loans.html">Conventional</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed</a><a class="btn btn-outline" href="bank-statement-loans.html">Bank Statement</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a><a class="btn btn-outline" href="investment-property-loans.html">Investor Loans</a></div></div></section>'''
inject_before_conversion(f'{W}/non-qm-loans.html','SEP2026-AEO:nonqm-agency-first',w_nonqm)
add_schema(f'{W}/non-qm-loans.html','SEP2026-SCHEMA:nonqm-agency',faq_schema('https://westcoastcapitalmortgage.com/non-qm-loans',[('When should a borrower compare Conventional before Non-QM?','When borrower and property eligibility may satisfy Agency requirements, a conventional structure is worth comparing. Non-QM may be appropriate for alternative documentation or scenarios outside standard Agency guidelines.')]))

w_jumbo='''<!-- SEP2026-AEO:jumbo-highbalance -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Updated September 2026</span><h2>High-Balance vs. Jumbo Loan Comparison</h2><p><strong>Direct answer:</strong> A high-balance conforming loan and a jumbo loan are different executions. A borrower whose loan amount falls within a high-cost conforming limit may still benefit from comparing current jumbo structures. The better fit depends on current pricing, credit, reserves, income documentation, property type and the overall transaction.</p><div class="grid grid-2"><div class="card"><h3>High-Balance Conforming</h3><p>Follows applicable Agency high-cost loan limits and underwriting requirements. Availability depends on county, property and borrower eligibility.</p></div><div class="card"><h3>Jumbo</h3><p>Non-conforming financing with lender-specific underwriting, reserve and documentation requirements. In some scenarios its current execution may be competitive with high-balance financing.</p></div></div><p><strong>Before choosing a high-balance loan, compare it with current jumbo options.</strong></p><div class="btn-row"><a class="btn btn-blue" href="apply.html">Request a Financing Comparison</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed Options</a><a class="btn btn-outline" href="bank-statement-loans.html">Bank Statement</a></div></div></section>'''
inject_before_conversion(f'{W}/jumbo-loans.html','SEP2026-AEO:jumbo-highbalance',w_jumbo)
add_schema(f'{W}/jumbo-loans.html','SEP2026-SCHEMA:jumbo-highbalance',faq_schema('https://westcoastcapitalmortgage.com/jumbo-loans',[('Should I choose a high-balance conforming loan or a jumbo loan?','Compare both when available. The better fit depends on current pricing, loan amount, county limits, credit, reserves, income documentation, property type and lender or Agency requirements.')]))

# Major California high-cost county jumbo pages: discover by canonical URL, preserving current paths.
counties=['los-angeles-county','orange-county','san-diego-county','santa-clara-county','san-mateo-county','alameda-county','marin-county','contra-costa-county']
for county in counties:
    target=None
    needle=f'https://westcoastcapitalmortgage.com/loans/jumbo/{county}'
    for p in Path(W).rglob('*.html'):
        try: txt=read(p)
        except: continue
        if needle in txt: target=p; break
    if not target:
        notes.append(f'County page not resolved: {county}'); continue
    label=county.replace('-county','').replace('-',' ').title()+' County'
    block=f'''<!-- SEP2026-AEO:county-highbalance-{county} -->\n<section class="bg-light"><div class="wrap"><h2>{label}: High-Balance vs. Jumbo</h2><p><strong>Direct answer:</strong> Buyers in {label} should not assume that a loan inside the applicable high-cost conforming limit is automatically the best execution. Depending on current pricing, loan amount, credit, reserves, documentation and property type, a jumbo structure may also be worth comparing. High-balance financing follows Agency requirements; jumbo underwriting is lender-specific. West Coast Capital Mortgage compares available structures before a borrower selects a loan.</p><p><a href="/jumbo-loans">See the full High-Balance vs. Jumbo comparison</a> or <a href="/self-employed-borrowers">compare self-employed qualification paths</a>.</p></div></section>'''
    inject_before_conversion(target,f'SEP2026-AEO:county-highbalance-{county}',block)

# California purchase
w_buy='''<!-- SEP2026-AEO:california-seller-credits -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Updated September 2026</span><h2>Can Seller Credits Help Reduce Your California Home-Buying Costs?</h2><p><strong>Direct answer:</strong> Sometimes. A negotiated seller credit may help cover eligible buyer closing costs or, when allowed, contribute toward an interest-rate buydown. The amount and permitted use depend on the loan program, transaction structure and current underwriting rules; a seller is not required to offer a concession.</p><h3>Temporary vs. permanent rate buydowns</h3><p>A temporary buydown reduces the borrower’s payment for an initial period while the mortgage note retains its permanent terms. A permanent buydown generally uses discount points to reduce the note rate. Each structure should be compared with the purchase price, seller credit, expected ownership period and available loan options.</p><p>California conditions vary materially by metro and submarket, so we do not treat the state as one uniform buyer’s market. A pre-approval and financing comparison can show whether a seller credit, high-balance loan, jumbo structure or another purchase option is appropriate for a specific offer.</p><div class="btn-row"><a class="btn btn-blue" href="apply.html">Start Pre-Approval</a><a class="btn btn-outline" href="jumbo-loans.html">Compare Jumbo / High-Balance</a></div></div></section>'''
inject_before_conversion(f'{W}/buy.html','SEP2026-AEO:california-seller-credits',w_buy)
add_schema(f'{W}/buy.html','SEP2026-SCHEMA:ca-seller-credits',faq_schema('https://westcoastcapitalmortgage.com/buy',[('Can seller credits help reduce California home-buying costs?','Sometimes. Negotiated seller credits may cover eligible closing costs or permitted buydown costs, subject to loan-program and transaction limits. Sellers are not required to provide concessions, and local market conditions vary.')]))

# ---------- SunCoast ----------
s_invest=w_invest.replace('SEP2026-AEO:investor-comparison','SEP2026-AEO:florida-investor-comparison').replace('Conventional vs. DSCR: Which Works Better for Your Rental Property?','Florida Investment Property Loans: Conventional vs. DSCR vs. Non-QM').replace('Have a rental property or short-term rental?','Have a Florida rental property, condo or short-term rental?')
inject_before_conversion(f'{S}/investment-property-loans.html','SEP2026-AEO:florida-investor-comparison',s_invest)
add_schema(f'{S}/investment-property-loans.html','SEP2026-SCHEMA:florida-investor',faq_schema('https://suncoastcapitalmortgage.com/investment-property-loans',investor_faqs))

s_dscr=w_dscr.replace('SEP2026-AEO:dscr-conventional','SEP2026-AEO:florida-dscr-conventional').replace('Do I Need a DSCR Loan for Every Rental Property?','Does Every Florida Rental Property Need a DSCR Loan?')
inject_before_conversion(f'{S}/dscr-loans.html','SEP2026-AEO:florida-dscr-conventional',s_dscr)
add_schema(f'{S}/dscr-loans.html','SEP2026-SCHEMA:florida-dscr',faq_schema('https://suncoastcapitalmortgage.com/dscr-loans',[('Does every Florida rental property need a DSCR loan?','No. Depending on the borrower, property and rental-income documentation, a conventional Agency or another Non-QM path may also be available.'),('Can a Florida short-term rental use conventional financing?','In some eligible scenarios, short-term-rental income may be considered under current Agency guidance, subject to property eligibility, legal use, rental history, documentation and lender requirements.')]))

s_self=w_self.replace('SEP2026-AEO:self-employed-comparison','SEP2026-AEO:florida-self-employed-comparison').replace('Which Mortgage Qualification Method Can Work for a Self-Employed Borrower?','Which Mortgage Qualification Method Can Work for a Self-Employed Florida Borrower?')
inject_before_conversion(f'{S}/self-employed-borrowers.html','SEP2026-AEO:florida-self-employed-comparison',s_self)
add_schema(f'{S}/self-employed-borrowers.html','SEP2026-SCHEMA:florida-self-employed',faq_schema('https://suncoastcapitalmortgage.com/self-employed-borrowers',self_faqs))
set_description(f'{S}/self-employed-borrowers.html','Compare Florida mortgage qualification paths for self-employed borrowers, including traditional documentation, bank statements, asset-based options and DSCR for investment property.')

s_jumbo=w_jumbo.replace('SEP2026-AEO:jumbo-highbalance','SEP2026-AEO:florida-jumbo-highbalance')+'''\n<!-- SEP2026-AEO:south-florida-jumbo -->\n<section><div class="wrap"><h2>South Florida Luxury Financing: Prepare the Structure Before the Offer</h2><p><strong>Direct answer:</strong> Luxury buyers in Miami, Palm Beach and other South Florida markets may benefit from comparing jumbo, traditional documentation, bank-statement and asset-based qualification paths before making an offer. Strong financing readiness can reduce uncertainty in a complex transaction, but pre-approval and final approval remain subject to complete underwriting and current program requirements.</p><div class="btn-row"><a class="btn btn-blue" href="self-employed-borrowers.html">Self-Employed Options</a><a class="btn btn-outline" href="bank-statement-loans.html">Bank Statement</a></div></div></section>'''
inject_before_conversion(f'{S}/jumbo-loans.html','SEP2026-AEO:florida-jumbo-highbalance',s_jumbo)
add_schema(f'{S}/jumbo-loans.html','SEP2026-SCHEMA:florida-jumbo',faq_schema('https://suncoastcapitalmortgage.com/jumbo-loans',[('Should a South Florida buyer compare jumbo with other financing structures?','Yes. Depending on loan amount and borrower profile, it can be useful to compare jumbo, applicable conforming or high-balance options, traditional documentation, bank-statement and asset-based paths before selecting a structure.')]))

s_home='''<!-- SEP2026-AEO:florida-entry-points -->
<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">Florida financing paths</span><h2>Start With the Property and the Borrower Scenario</h2><p>Florida financing is not one market or one loan type. These two paths separate luxury-home financing from investment-property analysis.</p></div><div class="grid grid-2"><div class="card"><h3>South Florida Luxury Financing</h3><p>For Miami, Palm Beach and other South Florida luxury buyers: compare jumbo financing, traditional income documentation, bank statements and asset-based qualification before choosing a structure.</p><div class="btn-row"><a class="btn btn-blue" href="jumbo-loans.html">Explore Jumbo</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed Options</a></div></div><div class="card"><h3>Florida Investment Property Financing</h3><p>For rentals, condos and eligible short-term-rental scenarios: compare Conventional, DSCR and Non-QM based on property cash flow, borrower profile and documentation.</p><div class="btn-row"><a class="btn btn-blue" href="investment-property-loans.html">Investor Loans</a><a class="btn btn-outline" href="dscr-loans.html">DSCR</a></div></div></div></div></section>'''
inject_before_conversion(f'{S}/index.html','SEP2026-AEO:florida-entry-points',s_home)

# ---------- Resolve existing Washington and New York / Long Island pages ----------
def canonical(txt):
    m=re.search(r'<link rel="canonical" href="([^"]+)"',txt); return m.group(1) if m else ''

def resolve_state(termset):
    candidates=[]
    for base in [Path(W),Path(S)]:
        for p in base.rglob('*.html'):
            txt=read(p); low=(str(p)+' '+canonical(txt)+' '+re.sub('<[^>]+>',' ',txt[:12000])).lower()
            score=sum(1 for t in termset if t in low)
            if score>=2: candidates.append((score,p,canonical(txt)))
    return sorted(candidates,key=lambda x:(-x[0],len(str(x[1]))))

wa=resolve_state(['washington','washington mortgage','seattle'])
ny=resolve_state(['new york','long island','new-york','long-island'])
notes.append('Washington candidates: '+', '.join(f'{p} [{u}]' for _,p,u in wa[:5]) if wa else 'Washington candidates: NONE')
notes.append('New York/Long Island candidates: '+', '.join(f'{p} [{u}]' for _,p,u in ny[:5]) if ny else 'New York/Long Island candidates: NONE')

wa_block='''<!-- SEP2026-AEO:washington-seller-credits -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Updated September 2026</span><h2>Using Seller Credits and Rate Buydowns in Today’s Washington Market</h2><p><strong>Direct answer:</strong> In some Washington purchase transactions, a negotiated seller credit can help cover eligible closing costs or permitted rate-buydown costs. A seller is never required to provide a concession, and program limits and local negotiating conditions apply.</p><h3>What can be compared?</h3><ul class="feature-list"><li><strong>Seller-paid closing costs:</strong> eligible costs may be paid within applicable program limits.</li><li><strong>Temporary buydown:</strong> reduces the borrower’s payment for an initial period while the note retains its permanent terms.</li><li><strong>Permanent rate buydown:</strong> may use discount points to reduce the note rate.</li></ul><p>Where inventory has increased, some Washington submarkets may offer more room to negotiate, but conditions vary by city, price point and property. The financing should be modeled for the specific offer rather than assuming a concession will be available.</p><div class="btn-row"><a class="btn btn-blue" href="/apply">Start Pre-Approval</a><a class="btn btn-outline" href="/buy">Purchase Financing</a></div></div></section>'''
ny_block='''<!-- SEP2026-AEO:newyork-financing-strength -->
<section class="bg-light"><div class="wrap"><span class="eyebrow">Financing readiness</span><h2>Financing Strength Before You Make an Offer</h2><p><strong>Direct answer:</strong> New York and Long Island buyers with larger or more complex financing needs can benefit from comparing structures before an offer is submitted. A strong pre-approval can clarify the intended loan amount and documentation path, while final approval remains subject to complete underwriting and property review.</p><div class="grid grid-3"><div class="card"><h3>Jumbo Options</h3><p>Compare available jumbo structures, reserves and documentation instead of assuming one execution.</p></div><div class="card"><h3>Self-Employed / Asset-Based</h3><p>Compare traditional income analysis, bank statements and eligible asset-based or asset-utilization paths when applicable.</p></div><div class="card"><h3>Offer Readiness</h3><p>Resolve financing structure questions before the offer so the pre-approval reflects the intended transaction as closely as possible.</p></div></div><div class="btn-row"><a class="btn btn-blue" href="/jumbo-loans">Jumbo Loans</a><a class="btn btn-outline" href="/self-employed-borrowers">Self-Employed Options</a></div></div></section>'''
if wa:
    inject_before_conversion(wa[0][1],'SEP2026-AEO:washington-seller-credits',wa_block)
    notes.append(f'Washington implemented: {wa[0][1]} {wa[0][2]}')
else: notes.append('Washington implementation skipped: no suitable existing production page found; no duplicate/thin page created.')
if ny:
    inject_before_conversion(ny[0][1],'SEP2026-AEO:newyork-financing-strength',ny_block)
    notes.append(f'New York/Long Island implemented: {ny[0][1]} {ny[0][2]}')
else: notes.append('New York/Long Island implementation skipped: no suitable existing production page found; no duplicate/thin page created.')

# ---------- September 2026 authority article ----------
article=Path(W)/'september-2026-mortgage-update-investors-self-employed-jumbo.html'
if not article.exists():
    t=read(Path(W)/'investment-property-loans.html')
    prefix=t.split('<section class="page-hero">',1)[0]
    tail_anchor='<section><div class="wrap"><div class="wcci-cta">'
    tail=(tail_anchor+t.split(tail_anchor,1)[1]) if tail_anchor in t else t[t.index('<footer class="site-footer">'):]
    title='September 2026 Mortgage Update: Investors, Self-Employed & Jumbo Buyers | West Coast Capital Mortgage'
    desc='September 2026 mortgage update on Fannie Mae rental-income guidance, short-term rentals, Conventional vs. DSCR, self-employed qualification, high-balance vs. jumbo, and seller credits or buydowns.'
    prefix=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',prefix,1,flags=re.S)
    prefix=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',prefix,1)
    prefix=re.sub(r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="https://westcoastcapitalmortgage.com/september-2026-mortgage-update-investors-self-employed-jumbo">',prefix,1)
    prefix=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{title}">',prefix,1)
    prefix=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{desc}">',prefix,1)
    prefix=re.sub(r'<meta property="og:url" content="[^"]+">','<meta property="og:url" content="https://westcoastcapitalmortgage.com/september-2026-mortgage-update-investors-self-employed-jumbo">',prefix,1)
    # remove inherited JSON-LD; add article + FAQ
    prefix=re.sub(r'<script type="application/ld\+json">.*?</script>','',prefix,flags=re.S)
    art_schema={'@context':'https://schema.org','@type':'Article','headline':'September 2026 Mortgage Update: What Investors, Self-Employed Borrowers and Jumbo Buyers Should Know','datePublished':'2026-09-07','dateModified':'2026-09-07','mainEntityOfPage':'https://westcoastcapitalmortgage.com/september-2026-mortgage-update-investors-self-employed-jumbo','author':{'@type':'Organization','name':'West Coast Capital Mortgage Inc.'},'publisher':{'@type':'Organization','name':'West Coast Capital Mortgage Inc.','identifier':'NMLS #2817729'}}
    prefix=prefix.replace('</head>',f'<script type="application/ld+json">{json.dumps(art_schema,separators=(",",":"))}</script></head>',1)
    body='''<section class="page-hero"><div class="wrap page-hero-inner"><div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="mortgage-articles.html">Articles</a> &nbsp;/&nbsp; September 2026 Update</div><h1>September 2026 Mortgage Update: What Investors, Self-Employed Borrowers and Jumbo Buyers Should Know</h1><p class="lead">Updated September 2026 · A practical financing-structure update from West Coast Capital Mortgage Inc.</p></div></section>
<section><div class="wrap"><p><strong>Direct answer:</strong> The September 2026 underwriting environment creates more reasons to compare structures before selecting a mortgage. New Fannie Mae rental-income guidance adds defined treatment for certain recently acquired investment properties and short-term-rental scenarios, while self-employed and jumbo borrowers still benefit from comparing traditional and alternative qualification paths.</p>
<h2>What Changed With Fannie Mae Rental-Income Guidance?</h2><p><strong>Direct answer:</strong> On September 2, 2026, Fannie Mae published specific Selling Guide requirements for rental income from non-subject investment properties purchased within 45 days of the subject-property application date. The guidance addresses eligible one- to four-unit investment properties and documentation used to determine market rent and qualifying rental income. It does not mean every investor or rental automatically qualifies.</p>
<p>For the exact Agency requirements, see Fannie Mae Selling Guide <a href="https://selling-guide.fanniemae.com/sel/b3-3.8-06/rental-income-non-subject-property-investment-properties-purchased-within-45-days-subject-property" rel="noopener">B3-3.8-06</a>. Short-term-rental treatment is scenario-specific and should be reviewed under the current rental-income sections of the Selling Guide.</p>
<h2>Can Short-Term Rental Income Be Used to Qualify?</h2><p><strong>Direct answer:</strong> Potentially, in eligible scenarios. Conventional Agency, DSCR and Non-QM programs evaluate short-term-rental income differently. Property eligibility, legal short-term-rental use, rental history, appraisal or rent analysis, borrower documentation and current lender overlays can all affect the result.</p><p><a href="investment-property-loans.html">Compare investment-property loan options</a> and <a href="dscr-loans.html">review DSCR financing</a>.</p>
<h2>Conventional vs. DSCR: Which Should an Investor Check First?</h2><p><strong>Direct answer:</strong> Check both when the scenario supports it. Some investors who assume they need DSCR may have an Agency conventional path; others may prefer or need DSCR or another Non-QM structure because of cash flow, documentation or property considerations. The useful question is not “Which product is best in general?” but “Which structures fit this borrower and this property today?”</p>
<h2>What Should a Self-Employed Borrower Compare?</h2><p><strong>Direct answer:</strong> Self-employed borrowers should not automatically assume they need Non-QM. Depending on the file, compare traditional tax-return/Agency analysis, <a href="bank-statement-loans.html">bank-statement financing</a>, asset-based or asset-utilization approaches, and <a href="dscr-loans.html">DSCR</a> for an eligible investment property. See our <a href="self-employed-borrowers.html">self-employed mortgage comparison</a>.</p>
<h2>High-Balance vs. Jumbo: Why Compare Both?</h2><p><strong>Direct answer:</strong> A loan amount that fits within an applicable high-cost conforming limit does not automatically make high-balance execution preferable to jumbo. Current pricing, credit, reserves, income documentation, property type and underwriting can change the comparison. See <a href="jumbo-loans.html">High-Balance vs. Jumbo</a>.</p>
<h2>Can Seller Credits or Rate Buydowns Help a Purchase?</h2><p><strong>Direct answer:</strong> Sometimes. Fannie Mae permits eligible interested-party contributions within program limits and has specific rules for temporary interest-rate buydowns. A temporary buydown does not change the permanent note terms. Seller participation is negotiated, never guaranteed, and the economics should be compared with price and other financing choices.</p><p>Primary references: <a href="https://selling-guide.fanniemae.com/sel/b3-4.1-02/interested-party-contributions-ipcs" rel="noopener">Fannie Mae B3-4.1-02, Interested Party Contributions</a> and <a href="https://selling-guide.fanniemae.com/sel/b2-1.4-04/temporary-interest-rate-buydowns" rel="noopener">B2-1.4-04, Temporary Interest Rate Buydowns</a>.</p>
<div class="card" style="margin-top:30px"><h3>Compare the structure before choosing the product</h3><p>A borrower arriving with one assumed solution may have other potentially appropriate financing structures. Eligibility and terms depend on complete borrower, property and transaction information and current Agency/lender guidelines.</p><div class="btn-row"><a class="btn btn-blue" href="apply.html">Request a Financing Review</a><a class="btn btn-outline" href="investment-property-loans.html">Investor Loans</a><a class="btn btn-outline" href="self-employed-borrowers.html">Self-Employed</a><a class="btn btn-outline" href="jumbo-loans.html">Jumbo</a></div></div>
</div></section>'''
    write(article,prefix+body+tail)

# ---------- Sitemap freshness ----------
def url_from_file(p):
    txt=read(p); return canonical(txt)
urls=set()
for f in changed:
    p=Path(f)
    if p.suffix=='.html' and p.exists():
        u=url_from_file(p)
        if u: urls.add(u)
article_url='https://westcoastcapitalmortgage.com/september-2026-mortgage-update-investors-self-employed-jumbo'
urls.add(article_url)

def touch_sitemap(p):
    s=read(p); orig=s
    for u in sorted(urls):
        if u in s:
            pat=r'(<loc>'+re.escape(u)+r'</loc>\s*)(?:<lastmod>[^<]+</lastmod>)?'
            def repl(m): return m.group(1)+f'<lastmod>{DATE}</lastmod>'
            s=re.sub(pat,repl,s,count=1)
    if article_url not in s and 'westcoastcapitalmortgage.com' in s and '</urlset>' in s:
        s=s.replace('</urlset>',f'  <url><loc>{article_url}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>',1)
    if s!=orig: write(p,s)
for base in [Path(W),Path(S)]:
    for sm in base.glob('sitemap*.xml'): touch_sitemap(sm)

# ---------- Tests ----------
prohibited=['guaranteed approval','guaranteed savings','lowest rate','fannie now finances airbnb']
errors=[]
for f in sorted(set(changed)):
    p=Path(f)
    if p.suffix=='.html':
        txt=read(p); low=txt.lower()
        for bad in prohibited:
            if bad in low: errors.append(f'{f}: prohibited phrase {bad}')
        if txt.count('<link rel="canonical"')!=1: errors.append(f'{f}: canonical count {txt.count("<link rel=\"canonical\"")}')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',txt,re.S):
            try: json.loads(m.group(1))
            except Exception as e: errors.append(f'{f}: JSON-LD invalid: {e}')
    elif p.suffix=='.xml':
        import xml.etree.ElementTree as ET
        try: ET.parse(p)
        except Exception as e: errors.append(f'{f}: XML invalid: {e}')

required=[f'{W}/investment-property-loans.html',f'{W}/dscr-loans.html',f'{W}/self-employed-borrowers.html',f'{W}/bank-statement-loans.html',f'{W}/non-qm-loans.html',f'{W}/jumbo-loans.html',f'{W}/buy.html',f'{S}/investment-property-loans.html',f'{S}/dscr-loans.html',f'{S}/self-employed-borrowers.html',f'{S}/jumbo-loans.html',f'{S}/index.html',str(article)]
for r in required:
    if not Path(r).exists(): errors.append(f'Missing required file {r}')

report='SEP 2026 VISIBILITY UPDATE\n\nCHANGED FILES\n'+'\n'.join(sorted(set(changed)))+'\n\nRESOLUTION NOTES\n'+'\n'.join(notes)+'\n\nTESTS\n'+('PASS' if not errors else 'FAIL\n'+'\n'.join(errors))+'\n'
Path('sep2026_visibility_implementation_report.txt').write_text(report,encoding='utf-8')
changed.append('sep2026_visibility_implementation_report.txt')
print(report)
if errors: sys.exit(1)
