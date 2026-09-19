from pathlib import Path

path = Path("wccm-corporate/florida-condo-financing.html")
text = path.read_text(encoding="utf-8")

marker = "2026 AGENCY CONDO UPDATE"
if marker in text:
    print("Florida condo 2026 update already present")
    raise SystemExit(0)

old_meta = '<meta name="description" content="Florida condo financing for primary homes, second homes, and investment properties. Review warrantable and non-warrantable condo options in Miami-Dade, Broward, Palm Beach and across Florida. West Coast Capital Mortgage NMLS #2817729.">'
new_meta = '<meta name="description" content="Florida condo financing updated for the August 3, 2026 agency project-review changes. Review warrantable, non-warrantable, Full Review, reserves and specialty condo options with West Coast Capital Mortgage Inc. NMLS #2817729.">'
assert old_meta in text, "Expected Florida condo meta description not found"
text = text.replace(old_meta, new_meta, 1)

old_og = '<meta property="og:description" content="Understand warrantable and non-warrantable condo financing options for Florida buyers, investors, and international purchasers.">'
new_og = '<meta property="og:description" content="Florida condo financing guidance updated for the August 3, 2026 agency project-review changes, including Full Review, reserves and specialty financing paths.">'
assert old_og in text, "Expected Florida condo OG description not found"
text = text.replace(old_og, new_og, 1)

faq_anchor = '    {"@type":"Question","name":"Can foreign nationals finance Florida condos?","acceptedAnswer":{"@type":"Answer","text":"Some foreign-national and Non-QM programs may finance eligible Florida condos for qualified international buyers. Program terms, property eligibility and documentation vary and are subject to underwriting review."}}'
faq_insert = '''    {"@type":"Question","name":"What changed for agency condo project reviews on August 3, 2026?","acceptedAnswer":{"@type":"Answer","text":"For Fannie Mae loan applications dated on or after August 3, 2026, the Limited Review process is retired; established projects that previously qualified for Limited Review must use Full Review or, when applicable, Waiver of Project Review. Freddie Mac likewise limits Streamlined Review to applications received before August 3, 2026. The applicable review path depends on the agency, project and loan."}},
    {"@type":"Question","name":"Are Fannie Mae condo reserve requirements changing again in 2027?","acceptedAnswer":{"@type":"Answer","text":"Yes. For Fannie Mae Full Review loan applications dated on or after January 4, 2027, the minimum replacement-reserve allocation rises from 10% to 15% of the annual budgeted income assessment. Fannie Mae also updated reserve-study requirements, so the applicable reserve analysis depends on the project documentation and review path."}},
''' + faq_anchor
assert faq_anchor in text, "Expected FAQ anchor not found"
text = text.replace(faq_anchor, faq_insert, 1)

section_anchor = '</div></div></section>\n\n<section class="bg-light"><div class="wrap split"><div><span class="eyebrow">WHAT WE REVIEW</span>'
assert text.count(section_anchor) == 1, f"Expected one section anchor, found {text.count(section_anchor)}"
update_section = '''</div></div></section>

<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">2026 AGENCY CONDO UPDATE</span><h2>Condo project review changed for applications dated August 3, 2026 or later.</h2><p class="lead">For conventional agency condo financing, Fannie Mae retired Limited Review and Freddie Mac no longer permits Streamlined Review for applications received on or after August 3, 2026. The specific remaining review path depends on the agency, project and loan, which makes early project screening more important for Florida buyers.</p></div><div class="grid grid-2">
<div class="card"><span class="label">FANNIE MAE</span><h3>Limited Review is retired.</h3><p>Fannie Mae says established projects that previously qualified for Limited Review must now use Full Review or, when applicable, Waiver of Project Review for loan applications dated on or after August 3, 2026.</p></div>
<div class="card"><span class="label">FLORIDA NEW PROJECTS</span><h3>Mandatory PERS review was retired.</h3><p>Fannie Mae also retired the requirement that new or newly converted Florida condo projects with attached units be submitted through PERS. Those projects may be reviewed through the lender-delegated Full Review process, subject to applicable requirements.</p></div>
<div class="card"><span class="label">SMALL PROJECTS</span><h3>Waiver eligibility expanded to 10 units.</h3><p>Fannie Mae expanded Waiver of Project Review eligibility to certain new and established projects with ten or fewer units. Conditions still apply, including project, insurance and critical-repair requirements.</p></div>
<div class="card"><span class="label">JANUARY 4, 2027</span><h3>The Fannie Mae reserve allocation test increases.</h3><p>For Fannie Mae Full Review applications dated on or after January 4, 2027, the minimum replacement-reserve allocation increases from 10% to 15% of the annual budgeted income assessment. Reserve-study requirements can also affect the analysis.</p></div>
</div><p><b>Primary sources:</b> <a href="https://capitalmarkets.fanniemae.com/mortgage-backed-securities/single-family-mbs/fannie-mae-announces-updates-single-family-project-standards-and-property-insurance-requirements" target="_blank" rel="noopener noreferrer">Fannie Mae LL-2026-03 announcement</a> and <a href="https://sf.freddiemac.com/faqs/condominium-unit-mortgage-faq" target="_blank" rel="noopener noreferrer">Freddie Mac Condominium Unit Mortgage FAQ</a>. Agency and lender requirements can change; confirm the review path for the specific loan and project.</p></div></section>

<section class="bg-light"><div class="wrap split"><div><span class="eyebrow">WHAT WE REVIEW</span>'''
text = text.replace(section_anchor, update_section, 1)

html_faq_anchor = '<div class="card"><h3>Can investors use DSCR for a Florida condo?</h3><p>Some DSCR programs permit eligible condominium investment properties. Project type, rental use, HOA characteristics, short-term rental rules, and lender guidelines all matter.</p></div>'
html_faq_insert = '''<div class="card"><h3>What changed on August 3, 2026?</h3><p>Fannie Mae retired Limited Review for applications dated on or after August 3, 2026, and Freddie Mac limits Streamlined Review to applications received before that date. The remaining project-review path depends on the agency, project, and loan.</p></div>
<div class="card"><h3>Are condo reserve requirements changing again in 2027?</h3><p>For Fannie Mae Full Review applications dated on or after January 4, 2027, the minimum replacement-reserve allocation rises from 10% to 15% of annual budgeted income assessment, with reserve-study rules also relevant to the analysis.</p></div>
''' + html_faq_anchor
assert html_faq_anchor in text, "Expected visible FAQ anchor not found"
text = text.replace(html_faq_anchor, html_faq_insert, 1)

# Basic safety checks: preserve tracking, company identity and canonical URL.
for required in [
    'GTM-K2X3X454',
    'AW-18417657219',
    'clarity',
    'West Coast Capital Mortgage Inc.',
    'NMLS #2817729',
    'https://westcoastcapitalmortgage.com/florida-condo-financing',
    '2026 AGENCY CONDO UPDATE',
    'August 3, 2026',
    'January 4, 2027',
]:
    assert required in text, f"Required marker missing after update: {required}"

path.write_text(text, encoding="utf-8")
print("Updated Florida condo page with sourced 2026 agency review changes")
