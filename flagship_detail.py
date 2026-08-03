#!/usr/bin/env python3
"""
flagship_detail.py — verified local content for the 10 flagship city pages.

Every figure here is sourced. Nothing is estimated by the author:
  * Transfer taxes  — county recorder / city finance pages (fetched 2026-08-03):
      LA County DTT list (lavote.gov), LA Office of Finance Measure ULA FAQ
      (thresholds effective July 1, 2026), santamonica.gov (Measure GS tiers),
      sf.gov/transfer-tax (full schedule), San Jose Measure E (sanjoseca.gov +
      Santa Clara County Clerk-Recorder), OC Clerk-Recorder, SD ARCC.
  * STR ordinances  — each city's official page, checked 2026-08-03.
  * Home values / rents — Zillow ZHVI + ZORI, June 2026 (flagship_data.json).
  * Property-tax mechanics — CA Prop 13 / supplemental assessment (state law).

If a fact could not be verified against an official source it was left out.
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(_HERE, "flagship_data.json"), encoding="utf-8") as _f:
        _DATA = json.load(_f)
except OSError:
    _DATA = {"zori": {}, "hoods": {}, "asof": ""}

ZORI = _DATA.get("zori", {})
HOODS = _DATA.get("hoods", {})
DATA_ASOF = "June 2026"

SLUG_TO_CITY = {
    "los-angeles": "Los Angeles", "san-diego": "San Diego",
    "san-francisco": "San Francisco", "san-jose": "San Jose",
    "beverly-hills": "Beverly Hills", "santa-monica": "Santa Monica",
    "irvine": "Irvine", "newport-beach": "Newport Beach",
    "pasadena": "Pasadena", "long-beach": "Long Beach",
}


def _money(v):
    if v >= 1e6:
        s = ("%.2f" % (v / 1e6)).rstrip("0").rstrip(".")
        return "$%sM" % s
    return "$%dK" % round(v / 1e3)


def _src(links):
    items = " &middot; ".join(
        '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (u, t)
        for t, u in links)
    return items


PROP13 = (
    "California property tax follows Proposition 13: a 1%% base levy on assessed value, plus "
    "voter-approved local additions that vary by tax rate area. When you buy, the assessed value "
    "resets to your purchase price, and one or two supplemental tax bills arrive after closing to "
    "cover the gap between the seller's old assessed value and yours — a real cash-flow item in "
    "your first year that buyers in %s often don't budget for.")


# ---------------------------------------------------------------------------
# per-city verified detail
# ---------------------------------------------------------------------------
DETAIL = {
    "los-angeles": {
        "transfer_html": (
            "<p>Base documentary transfer tax in the city of Los Angeles is <b>$5.60 per $1,000</b> "
            "of price — $1.10 county plus $4.50 city (0.56%% combined). On top of that, <b>Measure ULA</b> "
            "adds <b>4%% on transfers over $5.4M</b> and <b>5.5%% over $10.9M</b> (thresholds effective "
            "July 1, 2026; adjusted each year for inflation). ULA is owed when the property transfers and "
            "is customarily borne by the seller, but on high-end deals it is actively negotiated and "
            "priced into offers — a buyer of an $6M home should expect the seller's ~$240K ULA bill to "
            "shape the negotiation.</p>"
            "<p>" + PROP13 % "Los Angeles" + "</p>"),
        "transfer_sources": [
            ("LA County Registrar-Recorder — Documentary Transfer Tax",
             "https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info"),
            ("LA Office of Finance — Measure ULA FAQ", "https://finance.lacity.gov/faq/measure-ula"),
        ],
        "faqs_jumbo": [
            {"q": "Does the LA mansion tax (Measure ULA) affect jumbo purchases?",
             "a": "Only above its thresholds. As of July 1, 2026 Measure ULA applies 4% to transfers over "
                  "$5.4M and 5.5% over $10.9M in the city of Los Angeles, on top of the $5.60 per $1,000 "
                  "base transfer tax. It is customarily a seller-side cost, but on high-end deals it gets "
                  "negotiated into pricing. Neighboring incorporated cities such as Beverly Hills and "
                  "Santa Monica are outside the city of LA and are not subject to ULA."},
            {"q": "Which Los Angeles neighborhoods usually need jumbo financing?",
             "a": "The spread is enormous. Zillow's June 2026 neighborhood values run from roughly $603K in "
                  "Southeast Los Angeles to well over $2.8M in Brentwood — against a $1,249,125 conforming "
                  "limit. Westside neighborhoods (Brentwood, Pacific Palisades, Westwood) are mostly jumbo "
                  "territory; large parts of South LA and the East Valley still price within conforming "
                  "range. The table above shows where each major neighborhood sits."},
        ],
        "str_html": (
            "<p>The city of Los Angeles allows short-term rentals only under its <b>Home-Sharing "
            "Ordinance</b>: the unit must be the host's <b>primary residence</b>, city registration is "
            "required, and rentals are capped at <b>120 days per year</b> unless the host qualifies for "
            "extended home-sharing approval. A pure investor property cannot legally operate as a "
            "short-term rental in the city of LA — so DSCR underwriting here should assume "
            "<b>long-term rental income</b>, not Airbnb projections.</p>"),
        "str_sources": [
            ("LA City Planning — Home-Sharing Ordinance (PDF)",
             "https://planning.lacity.gov/odocument/d0270730-ad61-4c4d-90c3-7bef3812a369/HS_Ordinance.pdf"),
        ],
        "faqs_dscr": [
            {"q": "Can I run a short-term rental on a DSCR loan in Los Angeles?",
             "a": "Generally no. LA's Home-Sharing Ordinance limits short-term rentals to a registered "
                  "host's primary residence with a 120-day annual cap — which an investor property is not. "
                  "DSCR loans in the city of LA should be underwritten on long-term market rent."},
        ],
    },

    "santa-monica": {
        "transfer_html": (
            "<p>Santa Monica layers a city transfer tax on top of the $1.10 county rate, and it is "
            "steeply tiered: <b>$3.00 per $1,000 under $5M</b>, <b>$6.00 per $1,000 from $5M to "
            "$7,999,999</b>, and — since Measure GS took effect March 1, 2023 — <b>$56.00 per $1,000 "
            "(5.6%%) at $8M and above</b>. An $8M transfer owes roughly $448K city tax plus $8,800 "
            "county. For jumbo buyers near those break points, a small change in price crosses a very "
            "large tax cliff.</p>"
            "<p>" + PROP13 % "Santa Monica" + "</p>"),
        "transfer_sources": [
            ("City of Santa Monica — Documentary Transfer Tax",
             "https://www.santamonica.gov/documentary-transfer-tax-real-property-transfer-tax"),
        ],
        "faqs_jumbo": [
            {"q": "How big is Santa Monica's transfer tax on a high-end purchase?",
             "a": "Santa Monica's city transfer tax is tiered: $3.00 per $1,000 under $5M, $6.00 per "
                  "$1,000 from $5M to just under $8M, and $56.00 per $1,000 (5.6%) at $8M or more under "
                  "Measure GS — plus the $1.10 county rate. The jump at $8M is a genuine cliff: pricing a "
                  "sale at $7.95M versus $8.05M changes the city tax by hundreds of thousands of dollars."},
        ],
        "str_html": (
            "<p>Santa Monica <b>prohibits vacation rentals outright</b> — renting an entire unit for "
            "under 30 days is illegal. Only licensed <b>hosted home-sharing</b> is allowed: the resident "
            "host must live on-site during the stay. For DSCR purposes an investor property in Santa "
            "Monica is a <b>long-term rental, full stop</b>.</p>"),
        "str_sources": [
            ("City of Santa Monica — Home-Sharing Ordinance", "https://www.smgov.net/homeshare"),
        ],
        "faqs_dscr": [
            {"q": "Are Airbnb-style rentals allowed in Santa Monica?",
             "a": "No. Santa Monica prohibits renting an entire unit for less than 30 days; only hosted "
                  "home-sharing in the host's own primary residence is licensed. DSCR loans here are "
                  "underwritten on long-term rent."},
        ],
    },

    "beverly-hills": {
        "transfer_html": (
            "<p>Beverly Hills has <b>no city transfer tax</b> — transfers pay only the LA County rate of "
            "<b>$1.10 per $1,000</b> (0.11%%). Because Beverly Hills is its own incorporated city, it is "
            "also <b>outside Measure ULA</b>: the 4–5.5%% City-of-LA mansion tax stops at the city line. "
            "On an $8M sale, the transfer-tax difference between Beverly Hills ($8,800) and the city of "
            "Los Angeles (roughly $364,800 including ULA at 2026 thresholds) is material enough to shape "
            "where high-end buyers and sellers transact.</p>"
            "<p>" + PROP13 % "Beverly Hills" + "</p>"),
        "transfer_sources": [
            ("LA County Registrar-Recorder — Documentary Transfer Tax",
             "https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info"),
            ("LA Office of Finance — Measure ULA FAQ", "https://finance.lacity.gov/faq/measure-ula"),
        ],
        "faqs_jumbo": [
            {"q": "Does the LA mansion tax apply in Beverly Hills?",
             "a": "No. Measure ULA applies only inside the city of Los Angeles. Beverly Hills is a "
                  "separate incorporated city with no city transfer tax at all — transfers pay only the "
                  "$1.10 per $1,000 county rate. On multi-million-dollar sales that difference runs into "
                  "the hundreds of thousands."},
            {"q": "Is any Beverly Hills purchase realistically conforming?",
             "a": "Rarely. Zillow's June 2026 typical value for Beverly Hills is about $3.69M, and even "
                  "the least expensive tracked neighborhoods sit near $1.8M against the $1,249,125 "
                  "conforming limit. Nearly every standard purchase here is jumbo financing."},
        ],
        "str_html": (
            "<p>Beverly Hills <b>bans short-term rentals citywide</b>. Current rules require a minimum "
            "initial lease of <b>12 months</b> for single-family and multi-family rentals, with fines up "
            "to $5,000 per day for violations. Investor underwriting in Beverly Hills means "
            "<b>long-term leases only</b>.</p>"),
        "str_sources": [
            ("City of Beverly Hills — Short-Term Rentals", "https://www.beverlyhills.org/278/Short-Term-Rentals"),
        ],
        "faqs_dscr": [
            {"q": "Can I use short-term rental income for a DSCR loan in Beverly Hills?",
             "a": "No. Beverly Hills prohibits short-term rentals citywide and currently requires a "
                  "12-month minimum initial lease, with steep daily fines. DSCR qualification here rests "
                  "on long-term market rent."},
        ],
    },

    "pasadena": {
        "transfer_html": (
            "<p>Pasadena has <b>no city transfer tax</b> — only the LA County <b>$1.10 per $1,000</b> "
            "applies (Pasadena is not one of the five LA County cities that levy their own). It is also "
            "outside Measure ULA. Transfer costs here are among the lowest of any flagship market we "
            "cover.</p>"
            "<p>" + PROP13 % "Pasadena" + "</p>"),
        "transfer_sources": [
            ("LA County Registrar-Recorder — Documentary Transfer Tax",
             "https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info"),
        ],
        "faqs_jumbo": [
            {"q": "Which Pasadena purchases need a jumbo loan?",
             "a": "It genuinely depends on the neighborhood. Zillow's June 2026 values run from the high "
                  "$700Ks in West Central Pasadena to well above the $1,249,125 conforming limit in "
                  "southern and northeastern neighborhoods. Mid-city condos often still fit conforming "
                  "financing; larger single-family homes usually do not."},
        ],
        "str_html": (
            "<p>Pasadena permits short-term rentals <b>only in the host's primary residence</b> (lived in "
            "at least 9 months a year, one permit per person, TOT collected). Hosted stays have no annual "
            "cap; <b>un-hosted stays are limited to 90 days per year</b>. Non-primary vacation rentals "
            "are prohibited — so investor DSCR deals in Pasadena are long-term-rent deals.</p>"),
        "str_sources": [
            ("City of Pasadena — Short-Term Rental Regulations",
             "https://www.cityofpasadena.net/planning/short-term-rental-regulations/"),
        ],
        "faqs_dscr": [
            {"q": "Can an investor run an Airbnb in Pasadena?",
             "a": "Not on a pure investment property. Pasadena limits short-term rentals to a permitted "
                  "host's primary residence, with un-hosted stays capped at 90 days a year; non-primary "
                  "vacation rentals are prohibited. Underwrite Pasadena DSCR loans on long-term rent."},
        ],
    },

    "long-beach": {
        "transfer_html": (
            "<p>Long Beach has <b>no city transfer tax</b> — transfers pay only the LA County "
            "<b>$1.10 per $1,000</b>, and the city is outside Measure ULA. Combined with the lowest "
            "typical values among our flagship LA-area markets, entry costs here are comparatively "
            "light.</p>"
            "<p>" + PROP13 % "Long Beach" + "</p>"),
        "transfer_sources": [
            ("LA County Registrar-Recorder — Documentary Transfer Tax",
             "https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info"),
        ],
        "faqs_jumbo": [
            {"q": "Is jumbo financing common in Long Beach?",
             "a": "Less than in most coastal LA markets. The typical Long Beach value (Zillow, June "
                  "2026) sits well under the $1,249,125 conforming limit, and most tracked neighborhoods "
                  "price in the $600Ks-$900Ks. Jumbo loans concentrate in the higher-end coastal "
                  "pockets — the table above shows exactly where each neighborhood sits."},
        ],
        "str_html": (
            "<p>Long Beach is one of the few LA-County flagship markets where a <b>non-primary-residence "
            "short-term rental is legal</b>: the city registers them, but caps non-primary registrations "
            "at <b>800 citywide</b>, allocated by lottery when demand exceeds supply (roughly 695 were in "
            "use at the city's last published count). Un-hosted activity on a valid non-primary "
            "registration is not day-capped. STR-based DSCR underwriting is possible here — subject to "
            "actually holding a registration.</p>"),
        "str_sources": [
            ("City of Long Beach — Short-Term Rentals", "https://www.longbeach.gov/lbcd/enforcement/strs/"),
        ],
        "faqs_dscr": [
            {"q": "Does Long Beach allow investor short-term rentals?",
             "a": "Yes, with a registration — and that is the catch. Non-primary-residence STR "
                  "registrations are capped at 800 citywide and allocated by lottery when full. If you "
                  "hold one, un-hosted days are not capped. Some DSCR programs will consider documented "
                  "short-term rental income; without a registration, underwrite on long-term rent."},
        ],
    },

    "irvine": {
        "transfer_html": (
            "<p>Irvine transfers pay only the Orange County rate of <b>$1.10 per $1,000</b> — no city "
            "transfer tax exists anywhere in Orange County. The bigger recurring line item is "
            "<b>Mello-Roos</b>: many newer Irvine villages (including Great Park neighborhoods) sit in "
            "Community Facilities Districts whose special taxes are billed on top of the Prop 13 base. "
            "Always request the CFD disclosures early — two similar Irvine homes can carry very "
            "different annual tax bills.</p>"
            "<p>" + PROP13 % "Irvine" + "</p>"),
        "transfer_sources": [
            ("OC Clerk-Recorder — Documentary Transfer Tax",
             "https://ocrecorder.zendesk.com/hc/en-us/articles/21191850544027-What-is-Documentary-Transfer-Tax-and-how-do-I-calculate-it"),
        ],
        "faqs_jumbo": [
            {"q": "Do Irvine's Mello-Roos taxes affect jumbo qualification?",
             "a": "They affect the payment your lender qualifies you against. Mello-Roos special taxes in "
                  "newer Irvine villages are part of the property-tax bill underwriters use for your "
                  "debt-to-income math, so a home in a Community Facilities District qualifies "
                  "differently than an older-village home at the same price. Ask for the CFD disclosure "
                  "before you write the offer."},
        ],
        "str_html": (
            "<p>Irvine <b>prohibits short-term rentals (under 31 days) in all residential zones</b> — "
            "the ban, in Zoning Code Chapter 3-25, extends to advertising a listing at all. There is no "
            "permit path. Every DSCR loan in Irvine is a <b>long-term rental</b> loan.</p>"),
        "str_sources": [
            ("City of Irvine — Short-Term Rentals", "https://www.cityofirvine.org/code-enforcement/short-term-rentals"),
        ],
        "faqs_dscr": [
            {"q": "Can I buy an Irvine condo as a short-term rental with a DSCR loan?",
             "a": "No. Irvine bans rentals under 31 days in all residential zones, including advertising "
                  "them. DSCR deals in Irvine are underwritten on long-term leases — where demand from "
                  "the tech and university employment base is strong."},
        ],
    },

    "newport-beach": {
        "transfer_html": (
            "<p>Newport Beach transfers pay only the Orange County <b>$1.10 per $1,000</b> — no city "
            "transfer tax. At Newport values that is still real money on closing day, but it is an order "
            "of magnitude below what the same sale would owe inside the city of LA or Santa Monica.</p>"
            "<p>" + PROP13 % "Newport Beach" + "</p>"),
        "transfer_sources": [
            ("OC Clerk-Recorder — Documentary Transfer Tax",
             "https://ocrecorder.zendesk.com/hc/en-us/articles/21191850544027-What-is-Documentary-Transfer-Tax-and-how-do-I-calculate-it"),
        ],
        "faqs_jumbo": [
            {"q": "Is anything in Newport Beach conforming?",
             "a": "Very little. Zillow's June 2026 typical values run about $4.24M in Corona del Mar and "
                  "$5.6M in Newport Coast — multiples of the $1,249,125 Orange County conforming limit. "
                  "Assume jumbo financing, larger reserves, and full documentation for essentially any "
                  "standard purchase here."},
        ],
        "str_html": (
            "<p>Newport Beach allows short-term lodging <b>with a city permit</b>, and caps active "
            "permits at <b>1,550 citywide</b> — when the cap is full, new applicants join a waitlist. "
            "Buying a home does not automatically convey STR rights. For DSCR purposes, short-term "
            "income is only underwritable on a property that actually holds (or can obtain) a permit; "
            "otherwise qualify on long-term rent.</p>"),
        "str_sources": [
            ("City of Newport Beach — Short Term Lodging",
             "https://www.newportbeachca.gov/government/departments/community-development/short-term-rentals"),
        ],
        "faqs_dscr": [
            {"q": "Do Newport Beach short-term rental permits transfer with the property?",
             "a": "Permits are limited (1,550 active citywide) and administered by the city — verify the "
                  "specific property's permit status and transferability with the city before "
                  "underwriting any short-term income. Waitlists apply when the cap is reached."},
        ],
    },

    "san-diego": {
        "transfer_html": (
            "<p>San Diego transfers pay the standard <b>$1.10 per $1,000</b> county documentary transfer "
            "tax with <b>no city addition</b> — among big California cities this is the cheapest "
            "transfer regime.</p>"
            "<p>" + PROP13 % "San Diego" + "</p>"),
        "transfer_sources": [
            ("San Diego County ARCC — Recorder Fee Schedule",
             "https://www.sdarcc.gov/content/dam/arcc/recorder-county-clerk/forms/Recorder%20County%20Clerk%20Fee%20Schedule.pdf"),
        ],
        "faqs_jumbo": [
            {"q": "Where does the jumbo line fall across San Diego?",
             "a": "San Diego County's 2026 one-unit conforming limit is $1,104,000 — lower than LA/OC — "
                  "so jumbo territory starts sooner. Zillow's June 2026 neighborhood values run from "
                  "about $1.0M in Mira Mesa to $1.94M in Carmel Valley, putting much of the northern and "
                  "coastal city firmly in jumbo range while parts of the south and east remain "
                  "conforming."},
        ],
        "str_html": (
            "<p>San Diego licenses short-term rentals through its <b>STRO tier system</b>. Whole-home "
            "rentals (Tier 3) are capped at <b>1%% of the city's housing stock</b>, and Mission Beach "
            "(Tier 4) at 30%% of its units; part-time (&le;20 days) and home-share tiers are uncapped. "
            "Licenses are limited and allocated when available — an investor cannot assume a whole-home "
            "license comes with a purchase. DSCR loans without a license in hand should be underwritten "
            "on long-term rent.</p>"),
        "str_sources": [
            ("City of San Diego — Short-Term Residential Occupancy",
             "https://www.sandiego.gov/treasurer/short-term-residential-occupancy"),
        ],
        "faqs_dscr": [
            {"q": "Can I get a whole-home short-term rental license in San Diego?",
             "a": "Only within the citywide cap — Tier 3 whole-home licenses are limited to 1% of San "
                  "Diego's housing stock (Mission Beach has its own 30% cap), and availability varies. "
                  "Verify license status before underwriting STR income; otherwise qualify on long-term "
                  "rent."},
        ],
    },

    "san-francisco": {
        "transfer_html": (
            "<p>San Francisco's transfer tax is <b>tiered on the full price</b> (city and county "
            "combined): 0.50%% up to $250K, <b>0.68%%</b> to $1M, <b>0.75%%</b> from $1M to $5M, "
            "<b>2.25%%</b> from $5M to $10M, <b>5.5%%</b> from $10M to $25M, and 6%% above $25M. The "
            "steps at $5M and $10M are cliffs — the higher rate applies to the entire price, not just "
            "the amount above the threshold, so a $5.05M sale owes roughly triple the transfer tax of a "
            "$4.95M sale.</p>"
            "<p>" + PROP13 % "San Francisco" + "</p>"),
        "transfer_sources": [
            ("SF Treasurer &amp; Tax Collector — Transfer Tax", "https://www.sf.gov/transfer-tax"),
        ],
        "faqs_jumbo": [
            {"q": "How does San Francisco's transfer tax hit jumbo price points?",
             "a": "Most SF jumbo purchases land in the 0.75% tier ($1M-$5M, applied to the full price). "
                  "The jump to 2.25% at $5M — again on the whole price — is a genuine cliff: crossing it "
                  "adds roughly $75K of tax on a $5M sale, which experienced buyers and sellers "
                  "negotiate around."},
        ],
        "str_html": (
            "<p>San Francisco allows short-term rentals only in a registered host's <b>primary "
            "residence</b> (occupied at least 275 nights a year), with <b>un-hosted stays capped at 90 "
            "days per year</b> and dual registration (Office of Short-Term Rentals + Treasurer). An "
            "investor property cannot legally run as a short-term rental — DSCR deals in SF are "
            "<b>long-term rental</b> deals.</p>"),
        "str_sources": [
            ("SF Planning — Office of Short-Term Rentals", "https://sfplanning.org/office-short-term-rentals"),
        ],
        "faqs_dscr": [
            {"q": "Is Airbnb income usable for a DSCR loan in San Francisco?",
             "a": "Not on an investment property. SF limits short-term rentals to a registered host's "
                  "primary residence with a 90-day un-hosted cap. DSCR qualification in San Francisco "
                  "rests on long-term market rent."},
        ],
    },

    "san-jose": {
        "transfer_html": (
            "<p>San Jose stacks three layers: the county <b>$1.10 per $1,000</b>, the city conveyance "
            "tax of <b>$3.30 per $1,000</b>, and — on transfers above <b>$2.3M</b> (threshold effective "
            "July 1, 2025, adjusted every five years) — <b>Measure E</b> at $7.50 per $1,000 up to $5M, "
            "$10 per $1,000 from $5M to $10M, and $15 per $1,000 above $10M, applied to the full value. "
            "A $3M sale owes roughly $13,200 base plus $22,500 Measure E. At Zillow's June 2026 typical "
            "San Jose value of about $1.5M most standard purchases stay under the Measure E line, but "
            "West San Jose and higher-end pockets cross it routinely.</p>"
            "<p>" + PROP13 % "San Jose" + "</p>"),
        "transfer_sources": [
            ("City of San Jos&eacute; — Measure E Real Property Transfer Tax",
             "https://www.sanjoseca.gov/your-government/departments-offices/housing/resource-library/housing-investment-plans-and-policy/measure-e-real-property-transfer-tax"),
            ("Santa Clara County Clerk-Recorder — Measure E",
             "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate/measure-e"),
        ],
        "faqs_jumbo": [
            {"q": "When does San Jose's Measure E transfer tax apply?",
             "a": "On transfers above $2.3M (threshold effective July 1, 2025; reviewed every five "
                  "years): $7.50 per $1,000 to $5M, $10 to $10M, $15 above — on the full value, in "
                  "addition to the $4.40 per $1,000 combined county-plus-city base. With Zillow's June "
                  "2026 typical value near $1.5M, most standard purchases stay under the line, but "
                  "higher-end neighborhoods like West San Jose (about $2.1M typical) cross it "
                  "regularly."},
        ],
        "str_html": (
            "<p>San Jose permits short-term rentals only in the host's <b>primary residence</b> "
            "(occupied at least 60 consecutive days a year). Hosted stays are uncapped; <b>un-hosted "
            "stays are limited to 180 days per year</b> (Municipal Code &sect;20.80). A pure investor "
            "STR is not permitted — DSCR underwriting in San Jose should assume long-term rent, where "
            "tech-employment demand keeps the market deep.</p>"),
        "str_sources": [],
        "faqs_dscr": [
            {"q": "Can a DSCR investment property run as a short-term rental in San Jose?",
             "a": "No — San Jose's rules (Municipal Code §20.80) allow short-term rentals only in a "
                  "host's primary residence, with un-hosted stays capped at 180 days a year. Underwrite "
                  "San Jose DSCR loans on long-term market rent."},
        ],
    },
}


# ---------------------------------------------------------------------------
# builders used by gen_geo_pages.render_flagship()
# ---------------------------------------------------------------------------
def _jumbo_likelihood(zhvi, limit_val):
    r = zhvi / limit_val
    if r >= 2.0:
        return "Almost always"
    if r >= 1.15:
        return "Usually"
    if r >= 0.90:
        return "Often &mdash; depends on the home"
    if r >= 0.60:
        return "Higher-end homes only"
    return "Rarely"


def hood_table_html(slug, limit_str, for_program="jumbo", max_rows=14):
    """Real Zillow neighborhood table. Returns '' when no data exists."""
    city = SLUG_TO_CITY.get(slug)
    hoods = HOODS.get(city or "", [])
    if not hoods:
        return ""
    limit_val = float(re.sub(r"[^\d.]", "", limit_str))
    rows = list(hoods[:max_rows])
    # make sure the extremes are represented
    for extreme in (min(hoods, key=lambda h: h["zhvi"]), max(hoods, key=lambda h: h["zhvi"])):
        if extreme not in rows:
            rows.append(extreme)
    rows.sort(key=lambda h: -h["zhvi"])
    if for_program == "jumbo":
        head = ("<thead><tr><th>Neighborhood</th><th>Typical value<br>"
                "<span style=\"font-weight:400;font-size:.85em\">Zillow ZHVI, %s</span></th>"
                "<th>Usually jumbo at %s?</th></tr></thead>" % (DATA_ASOF, limit_str))
        body = "\n".join(
            "<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>"
            % (h["name"], _money(h["zhvi"]), _jumbo_likelihood(h["zhvi"], limit_val))
            for h in rows)
    else:
        head = ("<thead><tr><th>Neighborhood</th><th>Typical value<br>"
                "<span style=\"font-weight:400;font-size:.85em\">Zillow ZHVI, %s</span></th></tr></thead>"
                % DATA_ASOF)
        body = "\n".join(
            "<tr><td><b>%s</b></td><td>%s</td></tr>" % (h["name"], _money(h["zhvi"]))
            for h in rows)
    note = ("<p class=\"muted\" style=\"font-size:.9rem\">Neighborhood values are Zillow Home Value "
            "Index (ZHVI) figures for %s, rounded — the typical value for homes in the 35th–65th "
            "percentile of each neighborhood. %d of %d tracked neighborhoods shown (largest by size, "
            "plus the highest- and lowest-priced). Not an appraisal of any specific property.</p>"
            % (DATA_ASOF, len(rows), len(hoods)))
    return ("<div style=\"overflow-x:auto\">\n<table class=\"rate-table\" "
            "style=\"width:100%%;min-width:520px\">\n%s\n<tbody>\n%s\n</tbody></table>\n</div>\n%s"
            % (head, body, note))


def rent_reality_html(slug, city, median_str):
    """ZORI rent + arithmetic gross yield. Returns '' when either input is missing."""
    rent = ZORI.get(city)
    m = re.search(r"\$([\d.]+)([MK])", median_str or "")
    if not rent or not m:
        return ""
    val = float(m.group(1)) * (1e6 if m.group(2) == "M" else 1e3)
    gross = rent * 12 / val * 100
    return (
        "<p>Zillow's typical asking rent for %s is <b>$%s/month</b> (ZORI, %s), against a typical home "
        "value of about %s — a <b>gross rent-to-value ratio of roughly %.1f%%</b> before taxes, "
        "insurance, and expenses. That arithmetic (annual asking rent &divide; typical value, both "
        "city-level Zillow figures) is a screening number, not a quote: the DSCR your lender actually "
        "underwrites uses the specific property's documented rent against its specific payment.</p>"
        % (city, format(rent, ","), DATA_ASOF, _money(val), gross))


def sources_html(slug, program):
    d = DETAIL.get(slug, {})
    links = [("FHFA / HUD 2026 conforming loan limits", "https://www.fhfa.gov/data/conforming-loan-limit-cll-values")]
    links += d.get("transfer_sources", []) if program == "jumbo" else d.get("str_sources", [])
    zl = ("Zillow Research — ZHVI home values%s, %s"
          % (" and ZORI asking rents" if program == "dscr" else "", DATA_ASOF),
          "https://www.zillow.com/research/data/")
    links.append(zl)
    return (
        "<section style=\"padding-top:0\"><div class=\"wrap\">"
        "<p class=\"muted\" style=\"font-size:.85rem\"><b>Sources &amp; data notes:</b> %s. "
        "Tax rules and rental ordinances change; figures above were checked against the linked official "
        "sources in August 2026 and are provided for education, not tax or legal advice.</p>"
        "</div></section>" % _src(links))
