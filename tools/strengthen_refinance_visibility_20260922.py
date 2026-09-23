#!/usr/bin/env python3
"""Strengthen qualified refinance discovery for WCCM in California and Florida.

This build-time patch is intentionally narrow and idempotent. It updates only
wccm-corporate/refinance.html plus that URL's sitemap lastmod. It does not alter
rates, pricing, underwriting rules, advertising spend, or licensing claims.
"""
from pathlib import Path

PAGE = Path("wccm-corporate/refinance.html")
SITEMAP = Path("wccm-corporate/sitemap.xml")
STAMP = "2026-09-22"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Expected {label} marker not found in {PAGE}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    replacements = [
        (
            "<title>Refinance Your Mortgage | West Coast Capital Mortgage</title>",
            "<title>Mortgage Refinance California &amp; Florida | West Coast Capital Mortgage</title>",
            "title",
        ),
        (
            '<meta name="description" content="Lower your rate or access equity with a mortgage refinance. West Coast Capital Mortgage — cash-out, rate-term & streamline options. NMLS #2817729.">',
            '<meta name="description" content="Explore rate-and-term, cash-out, self-employed, investor and second-opinion refinance paths in California and Florida with West Coast Capital Mortgage Inc. NMLS #2817729.">',
            "meta description",
        ),
        (
            '<meta name="author" content="West Coast Capital Mortgage">',
            '<meta name="author" content="West Coast Capital Mortgage Inc.">',
            "author",
        ),
        (
            '<meta property="og:title" content="Refinance Your Mortgage | West Coast Capital Mortgage">',
            '<meta property="og:title" content="Mortgage Refinance California &amp; Florida | West Coast Capital Mortgage">',
            "Open Graph title",
        ),
        (
            '<meta property="og:description" content="Lower your rate or access equity with a mortgage refinance. West Coast Capital Mortgage — cash-out, rate-term & streamline options. NMLS #2817729.">',
            '<meta property="og:description" content="Rate-and-term, cash-out, self-employed, investor and second-opinion refinance guidance for California and Florida borrowers. NMLS #2817729.">',
            "Open Graph description",
        ),
        (
            '<meta name="twitter:title" content="Refinance Your Mortgage | West Coast Capital Mortgage">',
            '<meta name="twitter:title" content="Mortgage Refinance California &amp; Florida | West Coast Capital Mortgage">',
            "Twitter title",
        ),
        (
            '<meta name="twitter:description" content="Lower your rate or access equity with a mortgage refinance. West Coast Capital Mortgage — cash-out, rate-term & streamline options. NMLS #2817729.">',
            '<meta name="twitter:description" content="Rate-and-term, cash-out, self-employed, investor and second-opinion refinance guidance for California and Florida borrowers. NMLS #2817729.">',
            "Twitter description",
        ),
        (
            '{"@context":"https://schema.org","@type":"WebPage","name":"Refinance","url":"https://westcoastcapitalmortgage.com/refinance","isPartOf":{"@type":"WebSite","name":"West Coast Capital Mortgage","url":"https://westcoastcapitalmortgage.com/"},"publisher":{"@type":"Organization","name":"West Coast Capital Mortgage","identifier":"NMLS #2817729"}}',
            '{"@context":"https://schema.org","@type":"WebPage","name":"Mortgage Refinance in California and Florida","url":"https://westcoastcapitalmortgage.com/refinance","isPartOf":{"@type":"WebSite","name":"West Coast Capital Mortgage","url":"https://westcoastcapitalmortgage.com/"},"publisher":{"@type":"Organization","name":"West Coast Capital Mortgage Inc.","identifier":"NMLS #2817729"},"about":["mortgage refinance","cash-out refinance","rate-and-term refinance","self-employed refinance","investor refinance","mortgage second opinion"]}',
            "WebPage schema",
        ),
        (
            "<h1>Refinance</h1>\n    <p class=\"lead\">Lower your rate, shorten your term, or access equity by replacing your current loan with a better-fitting one.</p>",
            "<h1>Mortgage Refinance in California &amp; Florida</h1>\n    <p class=\"lead\">Compare rate-and-term, cash-out, self-employed, investor, and second-opinion refinance paths based on your goals and file.</p>",
            "hero",
        ),
        (
            '<li><b>Refinance checklist</b><span>Recent pay stubs and W-2s or tax returns.</span></li>',
            '<li><b>Refinance checklist</b><span>Income documentation varies by program and may include pay stubs and W-2s, tax returns, bank statements, or rental-property documentation.</span></li>',
            "refinance checklist",
        ),
        (
            '<details class="acc"><summary>How long does a refinance take?</summary><div class="acc-body">Many refinances close in roughly 30 days. Streamlined options for certain FHA and VA loans can move faster.</div></details>',
            '<details class="acc"><summary>How long does a refinance take?</summary><div class="acc-body">Timing varies with the loan type, documentation, appraisal or property review, title work, lender conditions, and underwriting. A file-specific review is the best way to estimate the timeline.</div></details>',
            "timeline FAQ",
        ),
        (
            '<a href="rates.html">Today\'s Rates</a>',
            '<a href="rates.html">Sample Rates</a>',
            "rates navigation label",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    geo_block = '<meta name="geo.region" content="US-CA">\n<meta name="geo.placename" content="California">\n'
    if geo_block in text:
        text = text.replace(geo_block, "", 1)

    if "<!-- WCCM refinance AI visibility 2026-09-22 -->" not in text:
        structured = '''<!-- WCCM refinance AI visibility 2026-09-22 -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"Mortgage Refinance Review","serviceType":["Rate-and-term refinance","Cash-out refinance","Self-employed refinance","Investor refinance","Mortgage second opinion"],"provider":{"@type":"Organization","name":"West Coast Capital Mortgage Inc.","identifier":"NMLS #2817729","url":"https://westcoastcapitalmortgage.com/"},"areaServed":[{"@type":"State","name":"California"},{"@type":"State","name":"Florida"}],"url":"https://westcoastcapitalmortgage.com/refinance"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How do I know if refinancing is worth it?","acceptedAnswer":{"@type":"Answer","text":"Compare the expected payment or term change with closing costs and the time you expect to keep the new loan. A break-even analysis can help determine whether the refinance fits your goals."}},{"@type":"Question","name":"What is a cash-out refinance?","acceptedAnswer":{"@type":"Answer","text":"A cash-out refinance replaces an existing mortgage with a larger new loan and, when eligible, returns part of the difference as cash from available home equity."}},{"@type":"Question","name":"Can self-employed homeowners refinance with bank statements?","acceptedAnswer":{"@type":"Answer","text":"Some Non-QM programs may evaluate eligible self-employed borrowers using bank statements or other permitted documentation instead of relying solely on traditional tax returns. Requirements vary by lender and file."}},{"@type":"Question","name":"What if another lender declined my refinance?","acceptedAnswer":{"@type":"Answer","text":"A decline can reflect one lender's guidelines, documentation, property review, or program fit. A second-opinion review can identify whether another documented path is worth evaluating, but it does not guarantee approval."}},{"@type":"Question","name":"How long does a refinance take?","acceptedAnswer":{"@type":"Answer","text":"Timing varies with the loan type, documentation, appraisal or property review, title work, lender conditions, and underwriting. A file-specific review is the best way to estimate the timeline."}}]}
</script>
'''
        text = text.replace("</head>", structured + "</head>", 1)

    if 'id="complex-refinance"' not in text:
        marker = '<section class="bg-light"><div class="wrap split">'
        if marker not in text:
            raise SystemExit(f"Expected complex-refinance insertion marker not found in {PAGE}")
        section = '''<section id="complex-refinance"><div class="wrap">
  <div class="section-head"><span class="eyebrow">California &amp; Florida</span><h2>Refinance paths for straightforward and complex files</h2>
  <p class="lead">West Coast Capital Mortgage Inc. reviews refinance scenarios in California and Florida, including files where traditional income documentation, investment-property cash flow, or a prior lender decision needs a closer look.</p></div>
  <div class="grid grid-3">
    <a class="card" href="self-employed-borrowers.html"><span class="label">Self-Employed</span><h3>Bank-statement and Non-QM review</h3><p>Eligible programs may evaluate alternative documentation when traditional tax-return income does not tell the full story.</p><span class="more">Review self-employed options &rarr;</span></a>
    <a class="card" href="dscr-loans.html"><span class="label">Investors</span><h3>DSCR and rental-property refinance</h3><p>For eligible investment properties, DSCR programs may evaluate property cash flow rather than relying only on personal income.</p><span class="more">Review investor options &rarr;</span></a>
    <a class="card" href="mortgage-second-opinion.html"><span class="label">Second Opinion</span><h3>Declined or hard-to-place refinance</h3><p>If another lender said no, review the documentation, property, and program fit before assuming the refinance has no path forward.</p><span class="more">Request a second opinion &rarr;</span></a>
  </div>
</div></section>
'''
        text = text.replace(marker, section + marker, 1)

    if "Can self-employed homeowners refinance with bank statements?" not in text.split('<script type="application/ld+json">')[-1]:
        pass

    visible_faq_anchor = '<details class="acc"><summary>How long does a refinance take?</summary><div class="acc-body">Timing varies with the loan type, documentation, appraisal or property review, title work, lender conditions, and underwriting. A file-specific review is the best way to estimate the timeline.</div></details>'
    visible_faq_extra = visible_faq_anchor + '<details class="acc"><summary>Can self-employed homeowners refinance with bank statements?</summary><div class="acc-body">Some Non-QM programs may evaluate eligible self-employed borrowers using bank statements or other permitted documentation instead of relying solely on traditional tax returns. Requirements vary by lender and file.</div></details><details class="acc"><summary>What if another lender declined my refinance?</summary><div class="acc-body">A decline can reflect one lender&rsquo;s guidelines, documentation, property review, or program fit. A second-opinion review can identify whether another documented path is worth evaluating, but it does not guarantee approval. <a href="mortgage-second-opinion.html">Request a mortgage second opinion</a>.</div></details>'
    if "Can self-employed homeowners refinance with bank statements?</summary>" not in text:
        text = replace_once(text, visible_faq_anchor, visible_faq_extra, "expanded visible FAQ")

    text = text.replace("West Coast Capital Mortgage. NMLS #2817729.", "West Coast Capital Mortgage Inc. NMLS #2817729.")
    PAGE.write_text(text, encoding="utf-8")

    sitemap = SITEMAP.read_text(encoding="utf-8")
    old_entry = '<loc>https://westcoastcapitalmortgage.com/refinance</loc>\n    <lastmod>2026-06-01</lastmod>'
    new_entry = f'<loc>https://westcoastcapitalmortgage.com/refinance</loc>\n    <lastmod>{STAMP}</lastmod>'
    if new_entry not in sitemap:
        if old_entry not in sitemap:
            raise SystemExit(f"Expected refinance sitemap marker not found in {SITEMAP}")
        sitemap = sitemap.replace(old_entry, new_entry, 1)
        SITEMAP.write_text(sitemap, encoding="utf-8")


if __name__ == "__main__":
    main()
