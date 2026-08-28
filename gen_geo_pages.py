#!/usr/bin/env python3
"""
gen_geo_pages.py — geography pages for westcoastcapitalmortgage.com (wccm-corporate).

Replaces the 466 city x program pages (jumbo/dscr x 233 cities) with a
consolidated set that passes the "is the answer actually different?" test:

  * 28 county jumbo pages  -> the conforming limit is a COUNTY property, so the
    county is the correct granularity. Each carries the full city table
    (typical value + whether jumbo usually applies) plus every city-specific
    market note, so no research from the old pages is lost.
  *  8 DSCR metro pages    -> rental markets are metro-level, not city-level.
  * 10 flagship city pages per program, kept because they carry real search
    demand of their own.

Everything else 301s to its county/metro page (see build_redirects) — 301 and
not 410, because the content is being MERGED, not deleted.

Data (CITY_DATA / COUNTY_LIMITS) still lives in gen_city_pages.py, which is now
the data store only; do not run its main().
"""
import os
import re
import collections

from gen_city_pages import (
    CITY_DATA, COUNTY_LIMITS, BASELINE_LIMIT, HIGH_COST_CEILING,
    NMLS, PHONE, is_high_cost,
)
import flagship_detail as fd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wccm-corporate")
LASTMOD = "2026-07-30"
FLAGSHIP_LASTMOD = "2026-08-03"   # flagship pages deepened with verified local data
BASE = "https://westcoastcapitalmortgage.com"

# Cities kept as standalone pages: real standalone search demand.
FLAGSHIP = [
    "los-angeles", "san-diego", "san-francisco", "san-jose", "beverly-hills",
    "santa-monica", "irvine", "newport-beach", "pasadena", "long-beach",
]

# DSCR is a rental-market product; rental markets are metro-level.
METROS = [
    ("los-angeles-metro", "Los Angeles County", ["Los Angeles County"]),
    ("orange-county", "Orange County", ["Orange County"]),
    ("san-diego-metro", "San Diego & Imperial", ["San Diego County", "Imperial County"]),
    ("inland-empire", "the Inland Empire", ["Riverside County", "San Bernardino County"]),
    ("bay-area", "the San Francisco Bay Area", [
        "San Francisco County", "San Mateo County", "Santa Clara County",
        "Alameda County", "Contra Costa County", "Marin County"]),
    ("north-bay", "the North Bay & Wine Country", [
        "Sonoma County", "Napa County", "Solano County"]),
    ("central-coast", "the Central Coast", [
        "Ventura County", "Santa Barbara County", "Santa Cruz County",
        "San Benito County", "Monterey County"]),
    ("sacramento-central-valley", "Sacramento & the Central Valley", [
        "Sacramento County", "Placer County", "El Dorado County", "Yolo County",
        "San Joaquin County", "Stanislaus County", "Merced County", "Kern County"]),
]

PROGRAMS = {
    "jumbo": {"name": "Jumbo Loans", "hub": "/jumbo-loans",
              "fp_name": "Jumbo Mortgage Loans", "sibling": "dscr"},
    "dscr": {"name": "DSCR Loans", "hub": "/dscr-loans",
             "fp_name": "DSCR Investment Property Loans", "sibling": "jumbo"},
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def county_slug(county):
    """'Los Angeles County' -> 'los-angeles-county'"""
    return county.lower().replace(" ", "-").replace(".", "")


def money_to_float(s):
    """'$1,249,125' or 'approximately $5.5M as of mid-2026' -> float dollars."""
    m = re.search(r"\$([\d,.]+)\s*([MK])?", s)
    if not m:
        return None
    val = float(m.group(1).replace(",", ""))
    suffix = m.group(2)
    if suffix == "M":
        val *= 1_000_000
    elif suffix == "K":
        val *= 1_000
    return val


def jumbo_likelihood(median_str, limit_str):
    """How often a purchase in this city actually crosses the conforming line."""
    med, lim = money_to_float(median_str), money_to_float(limit_str)
    if not med or not lim:
        return "Depends on the home"
    r = med / lim
    if r >= 2.0:
        return "Almost always"
    if r >= 1.15:
        return "Usually"
    if r >= 0.90:
        return "Often &mdash; depends on the home"
    if r >= 0.60:
        return "Higher-end homes only"
    return "Rarely"


def median_short(median_str):
    """'approximately $3.69M as of June 2026 (Zillow ZHVI)' -> '$3.69M'

    A handful of places (unincorporated areas such as West Los Angeles and
    Pebble Beach) have no Zillow series at all; they carry a sentinel string
    instead of a figure, and must not be shown as a number.
    """
    m = re.search(r"\$[\d,.]+\s*[MK]?", median_str)
    return m.group(0) if m else "Not tracked separately"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def jd(obj):
    import json
    return json.dumps(obj, indent=2, ensure_ascii=False)


CITIES_BY_COUNTY = collections.OrderedDict()
for _c in CITY_DATA:
    CITIES_BY_COUNTY.setdefault(_c["county"], []).append(_c)
for _k in CITIES_BY_COUNTY:
    CITIES_BY_COUNTY[_k].sort(key=lambda x: x["city"])

CITY_BY_SLUG = {c["slug"]: c for c in CITY_DATA}
COUNTY_OF_METRO = {}
for _slug, _name, _counties in METROS:
    for _cty in _counties:
        COUNTY_OF_METRO[_cty] = _slug


# --------------------------------------------------------------------------
# page shell — placeholders are @@NAME@@ so CSS/JS braces need no escaping
# --------------------------------------------------------------------------
SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">

<link rel="canonical" href="@@URL@@">
<meta name="robots" content="index, follow">
<meta name="author" content="West Coast Capital Mortgage Inc.">
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="@@PLACE@@, California">
<meta property="og:type" content="website">
<meta property="og:site_name" content="West Coast Capital Mortgage Inc.">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESC@@">
<meta property="og:url" content="@@URL@@">
<meta property="og:image" content="https://westcoastcapitalmortgage.com/assets/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESC@@">
<meta name="twitter:image" content="https://westcoastcapitalmortgage.com/assets/og-image.jpg">
@@JSONLD@@
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "wzzlo9s35g");
</script>
</head>
<body>
<div class="topbar">
  <div class="wrap topbar-inner">
    <nav class="topbar-left" aria-label="Utility">
      <a href="/loans.html">Mortgage</a>
      <a href="/buy.html">Home Search</a>
    </nav>
    <div class="topbar-right">
      <div class="lang-switch" role="group" aria-label="Language">
        <button type="button" data-lang="en">EN</button>
        <button type="button" data-lang="es">ES</button>
        <button type="button" data-lang="ru">RU</button>
      </div>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/index.html" aria-label="West Coast Capital Mortgage Inc. home">
      <span class="l1">WEST COAST CAPITAL</span>
      <span class="l2">MORTGAGE INC.</span>
    </a>
    <div class="nav-collapse" id="navc">
      <nav class="mainnav" aria-label="Primary"><a href="/buy.html">Buy a Home</a><a href="/refinance.html">Refinance</a><a href="/rates.html">Today's Rates</a><a href="/loans.html" class="active">Loans</a><a href="/resources.html">Resources</a><a href="/about.html">About Us</a></nav>
      <div class="header-cta">
        <a class="btn btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Apply Now</a>
      </div>
    </div>
    <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navc">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<section class="page-hero">
  <div class="hero-wallpaper" aria-hidden="true">
    <div class="wallpaper-line" style="top:18%">WEST COAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w2" style="top:58%">WEST COAST CAPITAL MORTGAGE</div>
  </div>
  <div class="wrap page-hero-inner">
    <div class="crumbs"><a href="/index.html">Home</a> &nbsp;/&nbsp; <a href="/loans.html">Loans</a> &nbsp;/&nbsp; <a href="@@HUB@@">@@PROGNAME@@</a> &nbsp;/&nbsp; @@PLACE@@</div>
    <h1>@@H1@@</h1>
    <p class="lead">@@LEAD@@</p>
  </div>
</section>
@@BODY@@
<section><div class="wrap"><div class="wcci-cta">
  <span class="eyebrow" style="color:var(--blue)">WCCI.Online Mortgage Intelligence</span>
  <h2>Not sure which loan program fits?</h2>
  <p>Start with a WCCI AI Mortgage Review to organize your income, property, credit, and loan goals before speaking with a licensed mortgage professional.</p>
  <div class="btn-row"><a class="btn btn-lg btn-blue" href="/ai-mortgage-review.html">Start AI Review</a>
    <a class="btn btn-lg btn-outline" href="/loan-officer.html">Talk to a Loan Officer</a></div>
  <p class="wcci-note">WCCI.Online provides preliminary educational mortgage guidance only and is not a loan approval, rate quote, rate lock, or commitment to lend.</p>
</div></div></section>

<section><div class="wrap"><div class="cta-band">
  <h2>Ready to take the next step?</h2><p>Start with a short mortgage intake and we will help you understand your options.</p>
  <div class="btn-row"><a class="btn btn-lg btn-blue" href="/apply.html">Start Short Application</a><a class="btn btn-lg btn-outline-light" href="/loan-officer.html">Contact a Loan Officer</a></div>
</div></div></section>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid"><div class="footer-brand"><div class="l1">WEST COAST CAPITAL</div><div class="l2">MORTGAGE INC.</div><p style="color:#aab2bd;font-size:.9rem">Modern mortgage guidance for buying, refinancing, and building equity.</p><p class="footer-contact"><b>Office / Loan Officer Questions:</b> <a href="tel:3106541577">310-654-1577</a><br><b>Anatoliy Direct:</b> <a href="tel:3106865053">310-686-5053</a><br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a></p></div><div><h4>Buy A Home</h4><a href="/homebuying-guide.html">Homebuying Guide</a><a href="/apply.html">Mortgage Pre-Approval</a><a href="/first-time-homebuyer.html">First-Time Homebuyers</a><a href="/buy.html">Down Payment Assistance</a><a href="/loans.html">Home Purchase Loans</a></div><div><h4>Refinance</h4><a href="/refinancing-guide.html">Refinancing Guide</a><a href="/rates.html">Refinance Mortgage Rates</a><a href="/refinance.html">Cash-Out Refinance</a><a href="/refinance.html">Rate-and-Term Refinance</a></div><div><h4>Loans</h4><a href="/conventional-loans.html">Conventional Loans</a><a href="/fha-loans.html">FHA Loans</a><a href="/va-loans.html">VA Loans</a><a href="/jumbo-loans.html">Jumbo Loans</a><a href="/non-qm-loans.html">Non-QM Loans</a><a href="/bank-statement-loans.html">Bank Statement Loans</a><a href="/dscr-loans.html">DSCR Loans</a><a href="/investment-property-loans.html">Investment Property Loans</a></div><div><h4>Resources</h4><a href="https://wcci.online" target="_blank" rel="noopener noreferrer">WCCI.Online AI Mortgage Review</a><a href="/calculators.html">Mortgage Calculators</a><a href="/mortgage-articles.html">Mortgage Articles</a><a href="/glossary.html">Mortgage Glossary</a><a href="/faq.html">Mortgage FAQ</a><a href="/resources.html">Mortgage Videos</a><a href="/rates.html">Rate Watch</a></div><div><h4>About Us</h4><a href="/about.html">About West Coast Capital Mortgage</a><a href="/contact.html">Contact Us</a><a href="https://2817729.myagentloans.com/register" target="_blank" rel="noopener noreferrer">Find a Loan Officer</a><a href="/about.html">Licensing &amp; Disclosures</a></div></div>
    <div class="footer-bottom">
      <div class="row">
        <nav aria-label="Legal">
          <a href="/about.html" style="display:inline;margin-right:18px">Licensing and Disclosures</a>
          <a href="https://www.nmlsconsumeraccess.org/" target="_blank" rel="noopener noreferrer" style="display:inline">NMLS Consumer Access</a>
        </nav>
        <span class="eho"><img src="/assets/equal-housing.svg" alt="Equal Housing Opportunity" style="height:32px;vertical-align:middle;margin-right:7px;opacity:.92"> Equal Housing Opportunity</span>
      </div>
      <p>West Coast Capital Mortgage Inc. NMLS #@@NMLS@@. Equal Housing Opportunity. Information is provided for
      educational purposes only and is not a commitment to lend. All loans are subject to credit, income, property,
      and underwriting approval.</p>
      <p>&copy; <span class="year"></span> West Coast Capital Mortgage Inc. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="/i18n.js"></script>
<script src="/script.js"></script>
</body>
</html>"""


def shell(**kw):
    out = SHELL
    kw.setdefault("NMLS", NMLS)
    for k, v in kw.items():
        out = out.replace("@@%s@@" % k, v)
    return out


def jsonld_blocks(objs):
    return "\n".join('<script type="application/ld+json">\n%s\n</script>' % jd(o) for o in objs)


def faq_section(title, faqs):
    parts = []
    for f in faqs:
        parts.append(
            '  <details class="acc"><summary>%s</summary><div class="acc-body">%s</div></details>'
            % (f["q"], f["a"]))
    return ('<section class="bg-light"><div class="wrap">\n'
            '  <div class="section-head"><span class="eyebrow">FAQ</span><h2>%s</h2></div>\n%s\n'
            '</div></section>' % (title, "\n".join(parts)))


def faqpage_jsonld(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["a"])}}
                       for f in faqs],
    }


def breadcrumb_jsonld(prog, prog_name, place, url):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Loans", "item": BASE + "/loans"},
            {"@type": "ListItem", "position": 3, "name": prog_name,
             "item": BASE + PROGRAMS[prog]["hub"]},
            {"@type": "ListItem", "position": 4, "name": place, "item": url},
        ],
    }


def product_jsonld(prog, url, place, area_names):
    return {
        "@context": "https://schema.org", "@type": "FinancialProduct",
        "name": "%s in %s" % (PROGRAMS[prog]["fp_name"], place),
        "url": url,
        "provider": {
            "@type": "Organization", "name": "West Coast Capital Mortgage Inc.",
            "url": BASE, "telephone": PHONE,
            "identifier": {"@type": "PropertyValue", "name": "NMLS", "value": NMLS},
        },
        "areaServed": [{"@type": "City", "name": n} for n in area_names[:60]],
    }


# --------------------------------------------------------------------------
# county jumbo pages
# --------------------------------------------------------------------------
def render_county_jumbo(county):
    cities = CITIES_BY_COUNTY[county]
    limit = COUNTY_LIMITS[county]
    slug = county_slug(county)
    url = "%s/loans/jumbo/%s" % (BASE, slug)
    high = is_high_cost(county)
    short = county.replace(" County", "")

    title = "Jumbo Loans in %s, CA &mdash; 2026 Limit %s | West Coast Capital Mortgage" % (county, limit)
    title = title.replace("&mdash;", "—")
    desc = ("Jumbo loans in %s. The 2026 one-unit conforming limit is %s, so any one-unit loan above that "
            "is a jumbo loan. Typical values for %d %s cities inside. NMLS #%s."
            % (county, limit, len(cities), short, NMLS))

    if high:
        limit_para = ("%s is a designated high-cost area, so its 2026 one-unit conforming loan limit is %s "
                      "(per FHFA/HUD 2026 loan limits) rather than the %s national baseline. Any one-unit "
                      "loan above %s in %s is a jumbo loan."
                      % (county, limit, BASELINE_LIMIT, limit, county))
    else:
        limit_para = ("%s is not designated a high-cost area, so the 2026 one-unit conforming loan limit is "
                      "the national baseline of %s (per FHFA/HUD 2026 loan limits). Any one-unit loan above "
                      "%s in %s is a jumbo loan." % (county, BASELINE_LIMIT, limit, county))

    # the city table — the actual data asset
    rows = []
    for c in cities:
        rows.append(
            '<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>'
            % (esc(c["city"]), median_short(c["median"]), jumbo_likelihood(c["median"], limit)))
    table = (
        '<div style="overflow-x:auto">\n'
        '<table class="rate-table" style="width:100%%;min-width:520px">\n'
        '<thead><tr><th>City</th><th>Typical home value<br><span style="font-weight:400;font-size:.85em">approx., mid-2026</span></th>'
        '<th>Is a jumbo loan usually needed?</th></tr></thead>\n<tbody>\n%s\n</tbody></table>\n</div>'
        % "\n".join(rows))

    # every city-specific market note is preserved here
    notes = "\n".join(
        '  <p><b>%s.</b> %s</p>' % (esc(c["city"]), c["jumbo_market"]) for c in cities)

    # Only cities with an actual figure can anchor the range.
    priced = [c for c in cities if money_to_float(c["median"]) is not None]
    cheapest = min(priced, key=lambda c: money_to_float(c["median"]))
    priciest = max(priced, key=lambda c: money_to_float(c["median"]))
    spread = ("Values across the county run from roughly %s in %s to about %s in %s, so whether a purchase "
              "needs jumbo financing varies widely by city &mdash; the table below shows where each one sits "
              "against the %s limit."
              % (median_short(cheapest["median"]), cheapest["city"],
                 median_short(priciest["median"]), priciest["city"], limit))

    lead = ("The 2026 one-unit conforming limit in %s is %s. Any one-unit loan above that is a jumbo loan. "
            "Below: how that line falls across %d %s cities." % (county, limit, len(cities), short))

    faqs = [
        {"q": "What is the 2026 jumbo loan limit in %s?" % county,
         "a": "In %s the 2026 one-unit conforming limit is %s (per FHFA/HUD 2026 loan limits). A jumbo loan "
              "is any one-unit loan amount above %s. %s"
              % (county, limit, limit,
                 "The county carries the high-cost limit rather than the %s national baseline." % BASELINE_LIMIT
                 if high else "This is the national baseline limit; %s is not a designated high-cost area." % county)},
        {"q": "Which %s cities usually require a jumbo loan?" % short,
         "a": "It varies by city. In %s, where typical values run around %s, jumbo financing applies to most "
              "standard purchases. In %s, closer to %s, it comes into play mainly on higher-end homes. The "
              "table on this page marks where each of the %d cities we cover falls against the %s limit."
              % (priciest["city"], median_short(priciest["median"]),
                 cheapest["city"], median_short(cheapest["median"]), len(cities), limit)},
        {"q": "How much down payment do jumbo borrowers need in %s?" % short,
         "a": "Jumbo programs commonly look for 10 to 20 percent or more, along with a credit score generally "
              "at or above 700 and meaningful cash reserves. The exact figure depends on the loan amount, the "
              "property, and your overall profile."},
        {"q": "Do jumbo loans cost more than conforming loans in %s?" % short,
         "a": "Not necessarily. For strong borrowers jumbo pricing is often very competitive with conforming "
              "loans, and in some markets it prices close to or below a comparable conforming loan. Pricing "
              "depends on credit, down payment, reserves, and the specific program."},
    ]

    body = """<section><div class="wrap">
  <div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">@@LIMIT@@</h3>
  <p style="margin:0">2026 1-unit conforming limit</p></div>
  <div class="card center"><h3 style="color:var(--blue)">@@HIGHCOST@@</h3>
  <p style="margin:0">County designation</p></div>
  <div class="card center"><h3 style="color:var(--blue)">@@NCITIES@@</h3>
  <p style="margin:0">Cities covered below</p></div>
  <div class="card center"><h3 style="color:var(--blue)">700+</h3>
  <p style="margin:0">Typical credit score</p></div></div>
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <div>
    <span class="eyebrow">Overview</span>
    <h2>What counts as a jumbo loan in @@COUNTY@@</h2>
    <p>@@LIMITPARA@@</p>
    <p>@@SPREAD@@</p>
    <div class="btn-row"><a class="btn btn-blue" href="/apply.html">Get Preapproved</a><a class="btn btn-outline" href="/jumbo-loans">All about Jumbo Loans</a></div>
  </div>
  <div>
    <h3>Typical requirements</h3>
    <ul class="feature-list"><li>A strong credit score, generally 700 or higher</li>
    <li>A larger down payment (often 10&ndash;20%+)</li>
    <li>Significant cash reserves</li>
    <li>Full documentation of income and assets</li></ul>
    <h3 style="margin-top:30px">Potential benefits</h3>
    <ul class="feature-list"><li>Finance high-value @@SHORT@@ properties in a single loan</li>
    <li>Competitive rates for strong borrowers</li>
    <li>Fixed and adjustable options</li>
    <li>Available for primary, second, and investment homes</li></ul>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">City by city</span>
  <h2>Where the @@LIMIT@@ line falls across @@COUNTY@@</h2>
  <p>Typical home values are Zillow Home Value Index (ZHVI) figures for June 2026, rounded. ZHVI reflects the
  typical value for homes in the 35th to 65th percentile range, so it sits below the median sale price in
  markets with a heavy luxury tail. Provided as a market reference for general education only; not an appraisal
  or valuation of any specific property.</p>
@@TABLE@@
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">Market notes</span>
  <h2>How jumbo financing plays out in each @@SHORT@@ city</h2>
@@NOTES@@
</div></section>
@@FAQ@@
<section style="padding-top:0"><div class="wrap">
  <h3>Related links</h3>
  <p>Learn more about our <a href="/jumbo-loans">Jumbo Loans</a> program, explore
  <a href="/loans/dscr/@@METRO@@">DSCR investment loans in this region</a>, or see
  <a href="/loans.html">all loan programs</a>.</p>
</div></section>"""
    body = (body
            .replace("@@LIMIT@@", limit)
            .replace("@@HIGHCOST@@", "High-cost" if high else "Baseline")
            .replace("@@NCITIES@@", str(len(cities)))
            .replace("@@COUNTY@@", county)
            .replace("@@SHORT@@", short)
            .replace("@@LIMITPARA@@", limit_para)
            .replace("@@SPREAD@@", spread)
            .replace("@@TABLE@@", table)
            .replace("@@NOTES@@", notes)
            .replace("@@METRO@@", COUNTY_OF_METRO[county])
            .replace("@@FAQ@@", faq_section("Jumbo loans in %s &mdash; common questions" % county, faqs)))

    objs = [product_jsonld("jumbo", url, county, [c["city"] for c in cities]),
            breadcrumb_jsonld("jumbo", "Jumbo Loans", county, url),
            faqpage_jsonld(faqs)]

    return shell(TITLE=esc(title), DESC=esc(desc), URL=url, PLACE=county,
                 HUB="/jumbo-loans", PROGNAME="Jumbo Loans",
                 H1="Jumbo Loans in %s" % county, LEAD=lead,
                 JSONLD=jsonld_blocks(objs), BODY=body)


# --------------------------------------------------------------------------
# DSCR metro pages
# --------------------------------------------------------------------------
def render_metro_dscr(slug, name, counties):
    cities = [c for cty in counties for c in CITIES_BY_COUNTY.get(cty, [])]
    cities.sort(key=lambda x: x["city"])
    url = "%s/loans/dscr/%s" % (BASE, slug)
    display = name[0].upper() + name[1:] if not name.startswith("the ") else name
    heading = name if name.startswith("the ") else name

    limits = sorted({COUNTY_LIMITS[c] for c in counties}, key=lambda s: -(money_to_float(s) or 0))
    limit_txt = (limits[0] if len(limits) == 1
                 else "%s to %s" % (limits[-1], limits[0]))

    title = "DSCR Loans in %s, CA | West Coast Capital Mortgage" % display.replace("the ", "")
    desc = ("DSCR investment property loans across %s — qualify on the property's rental income, not personal "
            "income. Covers %d cities in %d %s. NMLS #%s."
            % (heading, len(cities), len(counties), "county" if len(counties) == 1 else "counties", NMLS))

    rows = []
    for c in cities:
        rows.append('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (esc(c["city"]), esc(c["county"].replace(" County", "")),
                       median_short(c["median"]), COUNTY_LIMITS[c["county"]]))
    table = ('<div style="overflow-x:auto">\n<table class="rate-table" style="width:100%%;min-width:560px">\n'
             '<thead><tr><th>City</th><th>County</th><th>Typical value<br>'
             '<span style="font-weight:400;font-size:.85em">approx., mid-2026</span></th>'
             '<th>2026 conforming limit</th></tr></thead>\n<tbody>\n%s\n</tbody></table>\n</div>'
             % "\n".join(rows))

    notes = "\n".join('  <p><b>%s.</b> %s</p>' % (esc(c["city"]), c["dscr_market"]) for c in cities)

    lead = ("DSCR investment property loans across %s — qualify on the property's rental cash flow rather than "
            "your personal income. Rental conditions for %d cities below." % (heading, len(cities)))

    faqs = [
        {"q": "Do I need to verify my income for a DSCR loan in %s?" % display.replace("the ", ""),
         "a": "No. Qualification rests on the property's rental income against the mortgage payment, not on your "
              "personal income documentation — so W-2s, tax returns, and debt-to-income ratios are not the "
              "deciding factors they would be on a conventional loan."},
        {"q": "Do conforming loan limits cap a DSCR loan?",
         "a": "No. DSCR loans are non-conforming investor loans, so they are not capped by the conforming limit. "
              "The 2026 one-unit conforming limit across this region runs %s, which is still a useful benchmark "
              "when sizing a purchase." % limit_txt},
        {"q": "Which %s markets work best for DSCR investors?" % display.replace("the ", ""),
         "a": "It depends on your strategy: lower-priced cities generally produce stronger coverage ratios, while "
              "higher-priced coastal markets carry higher rents but tighter ratios. The city notes below describe "
              "the rental picture in each market we cover."},
        {"q": "Can I use a DSCR loan for short-term rentals?",
         "a": "Often yes. Some DSCR programs will consider short-term or vacation rental income, though guidelines, "
              "documentation, and local ordinances vary by program and by city."},
    ]

    body = """<section><div class="wrap">
  <div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">DSCR</h3>
  <p style="margin:0">Income = the property</p></div>
  <div class="card center"><h3 style="color:var(--blue)">No DTI</h3>
  <p style="margin:0">Personal income optional</p></div>
  <div class="card center"><h3 style="color:var(--blue)">@@NCITIES@@</h3>
  <p style="margin:0">Cities covered</p></div>
  <div class="card center"><h3 style="color:var(--blue)">Scale</h3>
  <p style="margin:0">Grow your holdings</p></div></div>
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <div>
    <span class="eyebrow">Overview</span>
    <h2>How a DSCR loan works in @@HEADING@@</h2>
    <p>DSCR stands for Debt-Service Coverage Ratio. A DSCR loan qualifies an investment property based on whether
    its rental income covers the mortgage payment, rather than on your personal income. A DSCR of 1.0 means rent
    equals the payment; higher ratios indicate stronger cash flow.</p>
    <p>DSCR loans are non-conforming investor loans and are not capped by the conforming limit. Across @@HEADING@@
    the 2026 one-unit conforming limit runs @@LIMITTXT@@ — a useful benchmark when you size a purchase, even
    though it does not bind a DSCR loan.</p>
    <div class="btn-row"><a class="btn btn-blue" href="/apply.html">Get Preapproved</a><a class="btn btn-outline" href="/dscr-loans">All about DSCR Loans</a></div>
  </div>
  <div>
    <h3>Typical requirements</h3>
    <ul class="feature-list"><li>An investment (non-owner-occupied) property</li>
    <li>Rental income that supports the debt-service coverage ratio</li>
    <li>A down payment consistent with investor programs</li>
    <li>A solid credit profile and reserves</li></ul>
    <h3 style="margin-top:30px">Potential benefits</h3>
    <ul class="feature-list"><li>Qualify on property cash flow, not personal income</li>
    <li>Streamlined documentation for investors</li>
    <li>Finance multiple properties over time</li>
    <li>Available for short- and long-term rentals</li></ul>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">City by city</span>
  <h2>Markets we cover across @@HEADING@@</h2>
  <p>Typical home values are Zillow Home Value Index (ZHVI) figures for June 2026, rounded. Provided as a market
  reference for general education only; not an appraisal or valuation of any specific property.</p>
@@TABLE@@
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">Rental market notes</span>
  <h2>What investors should expect in each market</h2>
@@NOTES@@
</div></section>
@@FAQ@@
<section style="padding-top:0"><div class="wrap">
  <h3>Related links</h3>
  <p>Learn more about our <a href="/dscr-loans">DSCR Loans</a> program, see
  <a href="/investment-property-loans.html">investment property loans</a>, or browse
  <a href="/loans.html">all loan programs</a>.</p>
</div></section>"""
    body = (body.replace("@@NCITIES@@", str(len(cities)))
            .replace("@@HEADING@@", heading)
            .replace("@@LIMITTXT@@", limit_txt)
            .replace("@@TABLE@@", table)
            .replace("@@NOTES@@", notes)
            .replace("@@FAQ@@", faq_section("DSCR loans in %s &mdash; common questions"
                                            % display.replace("the ", ""), faqs)))

    objs = [product_jsonld("dscr", url, display.replace("the ", ""), [c["city"] for c in cities]),
            breadcrumb_jsonld("dscr", "DSCR Loans", display.replace("the ", ""), url),
            faqpage_jsonld(faqs)]

    return shell(TITLE=esc(title), DESC=esc(desc), URL=url,
                 PLACE=display.replace("the ", ""), HUB="/dscr-loans", PROGNAME="DSCR Loans",
                 H1="DSCR Loans in %s" % display.replace("the ", ""), LEAD=lead,
                 JSONLD=jsonld_blocks(objs), BODY=body)


# --------------------------------------------------------------------------
# flagship city pages — same as before but the duplicate-sentence bug is fixed:
# the city market sentence now appears EXACTLY ONCE, in the market section.
# --------------------------------------------------------------------------
def render_flagship(prog, c):
    city, county, median = c["city"], c["county"], c["median"]
    limit = COUNTY_LIMITS[county]
    slug = c["slug"]
    url = "%s/loans/%s/%s" % (BASE, prog, slug)
    high = is_high_cost(county)
    pn = PROGRAMS[prog]["name"]
    county_url = "/loans/jumbo/%s" % county_slug(county)
    metro_url = "/loans/dscr/%s" % COUNTY_OF_METRO[county]

    if prog == "jumbo":
        title = "Jumbo Loans in %s, CA | West Coast Capital Mortgage" % city
        desc = ("Jumbo loans in %s, %s. With a 2026 one-unit conforming limit of %s, a jumbo loan finances %s "
                "homes above that ceiling. NMLS #%s." % (city, county, limit, city, NMLS))
        # lead no longer repeats the market sentence
        lead = ("Financing %s homes above the 2026 %s conforming limit of %s." % (city, county, limit))
        overview_h = "What a jumbo loan means in %s" % city
        area_clause = ("a high-cost area with a 2026 one-unit conforming limit of %s" % limit if high
                       else "where the 2026 one-unit conforming limit is the national baseline of %s" % limit)
        overview_p = ("A jumbo loan exceeds the conforming limit set by the Federal Housing Finance Agency. "
                      "Because %s is in %s — %s (per FHFA/HUD 2026 loan limits) — a jumbo loan in %s is any "
                      "one-unit loan above %s." % (city, county, area_clause, city, limit))
        overview_p2 = ("For strong borrowers, jumbo pricing is often very competitive with conforming loans, and "
                       "in some cases prices close to a comparable conforming loan. What moves the rate is "
                       "credit, down payment, reserves, and the specific program — not the jumbo label itself.")
        cards = ('<div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">%s</h3>'
                 '<p style="margin:0">2026 %s 1-unit limit</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">Above</h3>'
                 '<p style="margin:0">the conforming ceiling</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">700+</h3>'
                 '<p style="margin:0">Typical credit score</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">10&ndash;20%%+</h3>'
                 '<p style="margin:0">Typical down payment</p></div></div>' % (limit, county))
        req = ('<ul class="feature-list"><li>A strong credit score, generally 700 or higher</li>'
               '<li>A larger down payment (often 10&ndash;20%+)</li>'
               '<li>Significant cash reserves</li>'
               '<li>Full documentation of income and assets</li></ul>')
        ben = ('<ul class="feature-list"><li>Finance high-value %s properties in a single loan</li>'
               '<li>Competitive rates for strong borrowers</li><li>Fixed and adjustable options</li>'
               '<li>Available for primary, second, and investment homes</li></ul>' % city)
        market = c["jumbo_market"]
        # FAQ no longer repeats the market sentence either
        faqs = [
            {"q": "What counts as a jumbo loan in %s?" % city,
             "a": "%s is in %s, %s, where the 2026 one-unit conforming limit is %s (per FHFA/HUD 2026 loan "
                  "limits). A jumbo loan in %s is any one-unit loan amount above %s."
                  % (city, county, "a high-cost area" if high else "where the national baseline applies",
                     limit, city, limit)},
            {"q": "How much are homes in %s?" % city,
             "a": "The typical %s home value is %s. Whether a specific purchase needs jumbo financing depends "
                  "on the price and your down payment: the loan amount, not the purchase price, is what has to "
                  "clear %s." % (city, median, limit)},
            {"q": "How much down payment do jumbo borrowers usually need in %s?" % city,
             "a": "Jumbo programs commonly look for a larger down payment — often 10 to 20 percent or more — "
                  "along with strong credit and cash reserves. The exact figure depends on the loan amount, "
                  "property, and your overall profile."},
            {"q": "Can I use a jumbo loan for a second home in %s?" % city,
             "a": "Yes. Jumbo financing is available for primary residences, second homes, and many investment "
                  "properties in %s, with terms that vary by occupancy and program." % city},
        ]
        related = ('<p>See the full picture for <a href="%s">jumbo loans across %s</a>, learn more about our '
                   '<a href="/jumbo-loans">Jumbo Loans</a> program, or explore '
                   '<a href="%s">DSCR investment loans in this region</a>.</p>' % (county_url, county, metro_url))
        faqs += fd.DETAIL.get(slug, {}).get("faqs_jumbo", [])
    else:
        title = "DSCR Loans in %s, CA | West Coast Capital Mortgage" % city
        desc = ("DSCR investment property loans in %s, %s. Qualify on rental income, not personal income. "
                "Local 2026 conforming limit context: %s. NMLS #%s." % (city, county, limit, NMLS))
        lead = ("DSCR investment property loans in %s — qualify on the property's rental cash flow rather than "
                "personal income." % city)
        overview_h = "What a DSCR loan means in %s" % city
        overview_p = ("DSCR stands for Debt-Service Coverage Ratio. A DSCR loan qualifies a %s investment "
                      "property based on whether its rental income covers the mortgage payment, rather than on "
                      "your personal income. A DSCR of 1.0 means rent equals the payment; higher ratios "
                      "indicate stronger cash flow." % city)
        overview_p2 = ("DSCR loans are non-conforming investor loans, so they are not capped by the conforming "
                       "limit. Still, the 2026 one-unit conforming limit in %s is %s (per FHFA/HUD 2026 loan "
                       "limits), and the typical %s home value is %s — useful benchmarks when you size a "
                       "purchase." % (county, limit, city, median))
        cards = ('<div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">DSCR</h3>'
                 '<p style="margin:0">Income = property</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">No DTI</h3>'
                 '<p style="margin:0">Personal income optional</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">%s</h3>'
                 '<p style="margin:0">2026 %s 1-unit limit</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">Scale</h3>'
                 '<p style="margin:0">Grow your holdings</p></div></div>' % (limit, county))
        req = ('<ul class="feature-list"><li>An investment (non-owner-occupied) %s property</li>'
               '<li>Rental income that supports the debt-service coverage ratio</li>'
               '<li>A down payment consistent with investor programs</li>'
               '<li>A solid credit profile and reserves</li></ul>' % city)
        ben = ('<ul class="feature-list"><li>Qualify on %s property cash flow, not personal income</li>'
               '<li>Streamlined documentation for investors</li><li>Finance multiple properties over time</li>'
               '<li>Available for short- and long-term rentals</li></ul>' % city)
        market = c["dscr_market"]
        faqs = [
            {"q": "Do I need to verify my income for a DSCR loan in %s?" % city,
             "a": "No. A DSCR loan qualifies the %s property on whether its rental income covers the mortgage "
                  "payment, rather than on your personal income documentation. A DSCR of 1.0 means rent equals "
                  "the payment." % city},
            {"q": "How does the 2026 loan limit affect a DSCR loan in %s?" % city,
             "a": "%s is in %s, where the 2026 one-unit conforming limit is %s (per FHFA/HUD 2026 loan limits). "
                  "DSCR loans are non-conforming investor loans, so they are not capped by that limit — but it "
                  "is a useful local benchmark, since the typical %s home value is %s."
                  % (city, county, limit, city, median)},
            {"q": "What down payment do DSCR investors need in %s?" % city,
             "a": "Investor programs generally look for a larger down payment than owner-occupied financing, "
                  "along with reserves and a solid credit profile. The precise requirement moves with the "
                  "coverage ratio the property achieves."},
            {"q": "Can I use a DSCR loan for short-term rentals in %s?" % city,
             "a": "Often yes. Some DSCR programs will consider short-term or vacation rental income for %s "
                  "properties, though guidelines, documentation, and local ordinances vary by program." % city},
        ]
        related = ('<p>See <a href="%s">DSCR loans across this region</a>, learn more about our '
                   '<a href="/dscr-loans">DSCR Loans</a> program, or explore '
                   '<a href="%s">jumbo loans in %s</a>.</p>' % (metro_url, county_url, county))
        # the generic can-I-do-STR answer is wrong in cities that ban it —
        # swap it for the city's verified ordinance answer when we have one
        fd_faqs = fd.DETAIL.get(slug, {}).get("faqs_dscr", [])
        if fd_faqs:
            faqs = faqs[:3] + fd_faqs

    if high:
        limit_para = ("Across %s, the 2026 one-unit conforming loan limit is %s (per FHFA/HUD 2026 loan limits), "
                      "set above the %s national baseline because %s is a designated high-cost area."
                      % (county, limit, BASELINE_LIMIT, county))
    else:
        limit_para = ("Across %s, the 2026 one-unit conforming loan limit is the %s national baseline (per "
                      "FHFA/HUD 2026 loan limits); %s is not designated a high-cost area, so the standard "
                      "conforming ceiling applies." % (county, BASELINE_LIMIT, county))

    body = """<section><div class="wrap">
  @@CARDS@@
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <div>
    <span class="eyebrow">Overview</span>
    <h2>@@OVH@@</h2>
    <p>@@OVP@@</p><p>@@OVP2@@</p>
    <div class="btn-row"><a class="btn btn-blue" href="/apply.html">Get Preapproved</a><a class="btn btn-outline" href="@@HUB@@">All about @@PN@@</a></div>
  </div>
  <div>
    <h3>Typical requirements</h3>
    @@REQ@@
    <h3 style="margin-top:30px">Potential benefits</h3>
    @@BEN@@
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">@@CITY@@ market</span>
  <h2>@@PN@@ and the @@CITY@@ market</h2>
  <p>The typical @@CITY@@ home value is @@MEDIAN@@. @@MARKET@@</p>
  <p>@@LIMITPARA@@ We can walk you through exactly how that limit applies to your @@CITY@@ scenario.</p>
  <p class="muted" style="font-size:.9rem">Home-value figure is the Zillow Home Value Index (ZHVI) for @@CITY@@,
  June 2026, rounded. ZHVI reflects the typical value for homes in the 35th to 65th percentile range. Provided as
  a market reference for general education only; it is not an appraisal or valuation of any specific property.</p>
</div></section>
@@EXTRA@@
@@FAQ@@
<section style="padding-top:0"><div class="wrap">
  <h3>Related links</h3>
  @@RELATED@@
</div></section>
@@SOURCES@@"""
    # verified local sections (neighborhood tables, tax stack, STR rules)
    detail = fd.DETAIL.get(slug, {})
    extra_parts = []
    if prog == "jumbo":
        hood = fd.hood_table_html(slug, limit, "jumbo")
        if hood:
            extra_parts.append(
                '<section style="padding-top:0"><div class="wrap">\n'
                '  <span class="eyebrow">Neighborhood by neighborhood</span>\n'
                '  <h2>Where the jumbo line falls across %s</h2>\n%s\n</div></section>' % (city, hood))
        if detail.get("transfer_html"):
            extra_parts.append(
                '<section style="padding-top:0"><div class="wrap">\n'
                '  <span class="eyebrow">Beyond the mortgage</span>\n'
                '  <h2>Transfer taxes and property taxes in %s</h2>\n%s\n</div></section>'
                % (city, detail["transfer_html"]))
    else:
        rent = fd.rent_reality_html(slug, city, median)
        hood = fd.hood_table_html(slug, limit, "dscr")
        if rent or hood:
            extra_parts.append(
                '<section style="padding-top:0"><div class="wrap">\n'
                '  <span class="eyebrow">Rent reality</span>\n'
                '  <h2>What %s rents actually support</h2>\n%s\n%s\n</div></section>'
                % (city, rent, hood))
        if detail.get("str_html"):
            extra_parts.append(
                '<section style="padding-top:0"><div class="wrap">\n'
                '  <span class="eyebrow">Short-term rental rules</span>\n'
                '  <h2>Short-term rental rules in %s (as of August 2026)</h2>\n%s\n</div></section>'
                % (city, detail["str_html"]))
    sources = fd.sources_html(slug, prog) if detail else ""

    body = (body.replace("@@CARDS@@", cards).replace("@@OVH@@", overview_h)
            .replace("@@OVP2@@", overview_p2).replace("@@OVP@@", overview_p)
            .replace("@@REQ@@", req).replace("@@BEN@@", ben)
            .replace("@@MEDIAN@@", median).replace("@@MARKET@@", market)
            .replace("@@LIMITPARA@@", limit_para).replace("@@RELATED@@", related)
            .replace("@@EXTRA@@", "\n".join(extra_parts))
            .replace("@@SOURCES@@", sources)
            .replace("@@HUB@@", PROGRAMS[prog]["hub"]).replace("@@PN@@", pn)
            .replace("@@CITY@@", city)
            .replace("@@FAQ@@", faq_section("%s in %s &mdash; common questions" % (pn, city), faqs)))

    objs = [product_jsonld(prog, url, city, [city]),
            breadcrumb_jsonld(prog, pn, city, url), faqpage_jsonld(faqs)]

    return shell(TITLE=esc(title), DESC=esc(desc), URL=url, PLACE=city,
                 HUB=PROGRAMS[prog]["hub"], PROGNAME=pn,
                 H1="%s in %s" % (pn, city), LEAD=lead,
                 JSONLD=jsonld_blocks(objs), BODY=body)


# --------------------------------------------------------------------------
# redirects / sitemap / hubs
# --------------------------------------------------------------------------
def build_redirects():
    """301 every retired city page onto the page that now covers it."""
    lines = ["# --- geo consolidation 2026-07-30: city pages merged into county/metro pages ---"]
    n = 0
    for c in sorted(CITY_DATA, key=lambda x: x["slug"]):
        if c["slug"] in FLAGSHIP:
            continue
        lines.append("/loans/jumbo/%s    /loans/jumbo/%s    301!"
                     % (c["slug"], county_slug(c["county"])))
        lines.append("/loans/dscr/%s    /loans/dscr/%s    301!"
                     % (c["slug"], COUNTY_OF_METRO[c["county"]]))
        n += 2
    lines.append("# --- end geo consolidation ---")
    return "\n".join(lines) + "\n", n


def write_redirects():
    path = os.path.join(ROOT, "_redirects")
    existing = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            existing = f.read()
    # strip a previous run's block so this stays idempotent
    existing = re.sub(r"# --- geo consolidation .*?# --- end geo consolidation ---\n",
                      "", existing, flags=re.S)
    block, n = build_redirects()
    # 301s MUST precede the /* catch-all — Netlify takes the first match
    catchall = "/*    /404.html    404"
    if catchall in existing:
        existing = existing.replace(catchall, block + "\n" + catchall)
    else:
        existing = block + "\n" + existing
    with open(path, "w", encoding="utf-8") as f:
        f.write(existing)
    return n


def all_geo_urls():
    urls = []
    for county in CITIES_BY_COUNTY:
        urls.append(("/loans/jumbo/%s" % county_slug(county), "0.8", LASTMOD))
    for slug, _n, _c in METROS:
        urls.append(("/loans/dscr/%s" % slug, "0.8", LASTMOD))
    for s in FLAGSHIP:
        urls.append(("/loans/jumbo/%s" % s, "0.7", FLAGSHIP_LASTMOD))
        urls.append(("/loans/dscr/%s" % s, "0.7", FLAGSHIP_LASTMOD))
    return urls


def update_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        xml = f.read()
    start, end = "  <!-- city-pages:start -->", "  <!-- city-pages:end -->"
    entries = [start]
    for loc, pri, lastmod in all_geo_urls():
        entries.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
                       "    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
                       % (BASE, loc, lastmod, pri))
    entries.append(end)
    block = "\n".join(entries)
    # Drop every previously generated block first. The markers are matched
    # whitespace-tolerantly: the original sitemap wrote them unindented, and
    # an exact-string match silently appended a duplicate block on each run.
    xml, n = re.subn(r"[ \t]*<!-- city-pages:start -->.*?<!-- city-pages:end -->\n?",
                     "", xml, flags=re.S)
    xml = xml.replace("</urlset>", block + "\n</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    return len(all_geo_urls())


def hub_links_section(prog):
    if prog == "jumbo":
        items = "".join(
            '<a href="/loans/jumbo/%s">%s <span class="muted">(%s)</span></a>'
            % (county_slug(c), c, COUNTY_LIMITS[c]) for c in CITIES_BY_COUNTY)
        head = ("<h2>Jumbo loan limits by California county</h2>"
                "<p>The 2026 one-unit conforming limit is set per county. Pick a county to see its limit and "
                "how it falls across local home values.</p>")
    else:
        items = "".join('<a href="/loans/dscr/%s">%s</a>' % (slug, name.replace("the ", ""))
                        for slug, name, _ in METROS)
        head = ("<h2>DSCR loans by California region</h2>"
                "<p>Rental markets vary by metro. Pick a region for local rental conditions and the cities we "
                "cover there.</p>")
    return ('<section style="padding-top:0"><div class="wrap">%s<div class="city-links">%s</div></div></section>'
            % (head, items))


def update_hub(prog):
    fname = "jumbo-loans.html" if prog == "jumbo" else "dscr-loans.html"
    path = os.path.join(ROOT, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m0, m1 = "<!-- CITY-LINKS:%s -->" % prog, "<!-- /CITY-LINKS:%s -->" % prog
    section = m0 + hub_links_section(prog) + m1
    if m0 in html and m1 in html:
        s, e = html.index(m0), html.index(m1) + len(m1)
        html = html[:s] + section + html[e:]
    else:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def prune_old_pages():
    """Delete the city HTML files that are no longer generated."""
    keep = set()
    for county in CITIES_BY_COUNTY:
        keep.add(("jumbo", county_slug(county)))
    for slug, _n, _c in METROS:
        keep.add(("dscr", slug))
    for s in FLAGSHIP:
        keep.add(("jumbo", s))
        keep.add(("dscr", s))
    removed = 0
    for prog in ("jumbo", "dscr"):
        d = os.path.join(ROOT, "loans", prog)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".html"):
                continue
            if (prog, fn[:-5]) not in keep:
                os.remove(os.path.join(d, fn))
                removed += 1
    return removed


def main():
    written = []
    for prog in ("jumbo", "dscr"):
        os.makedirs(os.path.join(ROOT, "loans", prog), exist_ok=True)

    for county in CITIES_BY_COUNTY:
        p = os.path.join(ROOT, "loans", "jumbo", county_slug(county) + ".html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(render_county_jumbo(county))
        written.append(p)

    for slug, name, counties in METROS:
        p = os.path.join(ROOT, "loans", "dscr", slug + ".html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(render_metro_dscr(slug, name, counties))
        written.append(p)

    for s in FLAGSHIP:
        c = CITY_BY_SLUG[s]
        for prog in ("jumbo", "dscr"):
            p = os.path.join(ROOT, "loans", prog, s + ".html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(render_flagship(prog, c))
            written.append(p)

    removed = prune_old_pages()
    nredir = write_redirects()
    nsitemap = update_sitemap()
    h1, h2 = update_hub("jumbo"), update_hub("dscr")

    print("wrote %d pages (%d county jumbo + %d dscr metro + %d flagship)"
          % (len(written), len(CITIES_BY_COUNTY), len(METROS), len(FLAGSHIP) * 2))
    print("removed %d retired city pages" % removed)
    print("wrote %d 301 redirects into _redirects" % nredir)
    print("sitemap now lists %d geo URLs" % nsitemap)
    print("hubs updated: jumbo=%s dscr=%s" % (h1, h2))


if __name__ == "__main__":
    main()
