#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a curated set of high-value California local mortgage pages.

These are intentionally NOT mass city x product doorway pages. Each local page
combines the mortgage situations that are genuinely relevant to that market
(jumbo, move-up/bridge, self-employed, equity, condo/project review, rebuild,
second-look, or investor financing) and is written as a standalone local guide.

Wave 1 receives stronger growth-sitemap priority. Wave 2 is published at the
same time so internal links are complete, but receives a lower crawl priority.
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"
OUT = ROOT / "mortgage"
BASE = "https://westcoastcapitalmortgage.com"
TODAY = "2026-08-25"
COMPANY = "West Coast Capital Mortgage Inc."
PHONE = "(310) 654-1577"
PHONE_HREF = "+13106541577"
NMLS = "2817729"
CA_DRE = "02440065"
LO_NMLS = "2775380"
LO_DRE = "01385024"
LA_LIMIT = "$1,249,125"
VENTURA_LIMIT = "$1,035,000"

PATHS = {
    "jumbo": ("Jumbo Purchase", "/jumbo-loans", "Structure a high-value purchase above the conforming ceiling."),
    "bridge": ("Buy Before You Sell", "https://californiamtg.com/buy-before-you-sell-california", "Use existing-home equity and timing strategy when the next purchase cannot wait."),
    "self": ("Self-Employed / Complex Income", "/self-employed-borrowers", "Review tax returns, bank statements, 1099 income, business cash flow, or other eligible documentation paths."),
    "equity": ("Home Equity / Second Lien", "https://californiamtg.com/home-equity-review-california", "Compare a HELOC, fixed second lien, or cash-out structure without assuming the first mortgage should be replaced."),
    "condo": ("Condo Project Pre-Screen", "https://californiamtg.com/condo-project-prescreen", "Check HOA and project eligibility before a project issue jeopardizes a transaction."),
    "secondlook": ("Mortgage Second Look", "https://californiamtg.com/second-look", "Re-review a declined or difficult file before accepting the first lender's answer as final."),
    "dscr": ("Investor / DSCR", "/dscr-loans", "For eligible business-purpose rental-property scenarios, review qualification based on property cash flow."),
    "rebuild": ("Pacific Palisades Rebuild", "https://californiamtg.com/guides/pacific-palisades-rebuild-financing-2026/", "Organize insurance proceeds, lot ownership, construction budget, and rebuild financing options."),
}

MARKETS = [
    {
        "wave": 1, "city": "Manhattan Beach", "slug": "manhattan-beach", "place_type": "City",
        "zips": "90266", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$3.32M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Move-Up",
        "lead": "High-value South Bay purchase planning for buyers who need more than a generic rate quote.",
        "market": "Manhattan Beach is one of the South Bay's highest-value owner-occupied markets. With a June 2026 Zillow ZHVI around $3.32M, many purchases naturally sit above the Los Angeles County conforming ceiling, making jumbo structure, reserves, liquidity, and timing central to the financing plan.",
        "local_angle": "A meaningful share of local buyers are also existing homeowners with substantial equity. When the next property appears before the current home is sold, the financing problem is often timing rather than qualification. That makes buy-before-you-sell, bridge, or equity planning especially relevant here.",
        "property_note": "Attached homes and smaller condo projects can add a separate layer of project review. For a condo or townhome, the borrower can qualify while the HOA or project creates the financing issue, so an early pre-screen can save time.",
        "areas": ["Sand Section", "Tree Section", "Hill Section", "East Manhattan Beach"],
        "paths": ["jumbo", "bridge", "self", "equity", "condo", "secondlook"],
        "special_q": "Why start financing before writing an offer in Manhattan Beach?",
        "special_a": "Because high-value transactions often involve larger reserves, complex income, sale-of-current-home timing, or property-specific questions. A financing review before the offer can identify the correct lender and documentation path earlier."
    },
    {
        "wave": 1, "city": "Palos Verdes Estates", "slug": "palos-verdes-estates", "place_type": "City",
        "zips": "90274", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$2.79M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Equity",
        "lead": "Jumbo, move-up, equity, and complex-income planning for Palos Verdes Estates homeowners and buyers.",
        "market": "Palos Verdes Estates is a high-equity coastal market where the June 2026 Zillow ZHVI was about $2.79M. The typical value is well above the Los Angeles County one-unit conforming ceiling, so jumbo financing is a normal part of purchase planning rather than an exception.",
        "local_angle": "Many transactions involve owners moving within the Peninsula, downsizing, or buying before a current residence is sold. That creates a practical need to compare sale-contingent financing with bridge, second-lien, or other liquidity strategies instead of looking only at a single first-mortgage quote.",
        "property_note": "Custom homes, views, lot characteristics, and significant remodeling can make appraisal and property analysis important. The correct strategy should be selected around the actual property and borrower profile, not simply the ZIP code.",
        "areas": ["Lunada Bay", "Malaga Cove", "Montemalaga", "Valmonte"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "Can a Palos Verdes Estates owner use home equity without refinancing the first mortgage?",
        "special_a": "Potentially. Depending on equity, lien position, credit, occupancy, and program availability, a HELOC or fixed second lien may be worth comparing with a cash-out refinance."
    },
    {
        "wave": 1, "city": "Rancho Palos Verdes", "slug": "rancho-palos-verdes", "place_type": "City",
        "zips": "90275", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.83M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Property Review",
        "lead": "Property-aware mortgage planning for Rancho Palos Verdes purchases, move-up buyers, and difficult files.",
        "market": "Rancho Palos Verdes had a June 2026 Zillow ZHVI around $1.83M, above the Los Angeles County conforming ceiling. Many detached-home purchases therefore require jumbo financing, although the exact loan category depends on the loan amount after down payment.",
        "local_angle": "The Peninsula includes a wide range of property types and hillside conditions. In some locations, property condition, access, insurance, appraisal, or geotechnical questions can matter as much as borrower income. Those issues should be identified early rather than after a lender has already been selected.",
        "property_note": "A property-specific concern does not automatically mean there is no financing path. It means the property, insurance, appraisal, and lender guidelines need to be organized before the transaction becomes time-sensitive.",
        "areas": ["Miraleste", "Peninsula Center area", "Eastview", "Portuguese Bend area"],
        "paths": ["jumbo", "bridge", "equity", "self", "secondlook", "condo"],
        "special_q": "Can a Rancho Palos Verdes property issue affect financing even when the borrower qualifies?",
        "special_a": "Yes. Property, insurance, appraisal, access, condition, or project eligibility can be separate underwriting issues. A strong borrower does not eliminate the need for a property-specific review."
    },
    {
        "wave": 1, "city": "Rolling Hills", "slug": "rolling-hills", "place_type": "City",
        "zips": "90274", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": None, "median_note": None, "property_card": "Estate / acreage", "focus": "Jumbo + Custom Property",
        "lead": "Mortgage strategy for custom estates, large lots, and high-net-worth purchase scenarios in Rolling Hills.",
        "market": "Rolling Hills is a private gated estate community where custom homes, larger lots, and non-cookie-cutter property characteristics are common. Financing therefore needs to account for both the borrower and the property's appraisal and eligibility profile.",
        "local_angle": "For a high-net-worth buyer, liquidity can be more important than income alone. A jumbo first mortgage, bridge structure, securities or business income documentation, or a second-lien strategy may each solve a different part of the transaction.",
        "property_note": "Custom estates should be matched with lenders that are comfortable with the actual property characteristics. Early appraisal and property review is preferable to discovering an overlay late in escrow.",
        "areas": ["Rolling Hills gated community", "Large-lot estates", "Equestrian-oriented properties", "Custom hillside homes"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "Why can a custom Rolling Hills property need a different lender strategy?",
        "special_a": "Custom construction, large lots, unique improvements, and appraisal comparables can affect lender eligibility. The best lender for a standard tract home is not always the best lender for a unique estate."
    },
    {
        "wave": 1, "city": "Calabasas", "slug": "calabasas", "place_type": "City",
        "zips": "91302", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.73M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Move-Up",
        "lead": "Jumbo and move-up mortgage planning for Calabasas buyers, business owners, and existing homeowners.",
        "market": "Calabasas had a June 2026 Zillow ZHVI around $1.73M, above the Los Angeles County conforming ceiling. A large portion of detached-home purchases therefore require jumbo financing, with reserves and income structure becoming more important as loan size increases.",
        "local_angle": "Calabasas transactions frequently involve owners moving between high-value homes or borrowers with business, 1099, bonus, commission, or investment income. The financing plan should test documentation and liquidity before the borrower is committed to a specific lender.",
        "property_note": "Gated communities, HOA documentation, and property-specific appraisal considerations can also affect timing. The goal is to identify those requirements before they become closing surprises.",
        "areas": ["The Oaks", "Calabasas Park", "Mulholland Heights", "Greater 91302"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "Can self-employed borrowers qualify for a Calabasas jumbo purchase?",
        "special_a": "Potentially. Depending on the program, qualification may use traditional tax-return analysis or an eligible alternative-documentation approach. The correct path depends on the borrower, loan amount, occupancy, and lender guidelines."
    },
    {
        "wave": 1, "city": "Encino", "slug": "encino", "place_type": "Neighborhood",
        "zips": "91316, 91436", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.44M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Complex Income",
        "lead": "Jumbo and complex-income mortgage planning for Encino buyers, homeowners, and business owners.",
        "market": "Encino had a June 2026 Zillow ZHVI around $1.44M, placing the typical value above the Los Angeles County conforming ceiling. Larger south-of-the-boulevard and estate properties can move well beyond that threshold.",
        "local_angle": "For business owners, professionals, and borrowers with variable or multiple income streams, the central question is often not whether income exists, but how a particular lender is allowed to document it. A pre-offer income review can prevent avoidable lender changes later.",
        "property_note": "Existing homeowners may also have substantial equity that can be used strategically for a move-up purchase, reserves, renovation, or other eligible purposes without automatically replacing a favorable first mortgage.",
        "areas": ["Royal Oaks", "Amestoy Estates", "Encino Village", "Encino Hills"],
        "paths": ["jumbo", "self", "bridge", "equity", "secondlook", "dscr"],
        "special_q": "What should an Encino self-employed buyer review before making an offer?",
        "special_a": "Review the income-documentation path, liquidity and reserves, expected loan amount, property type, and timing. Different jumbo and Non-QM lenders can calculate the same business-owner profile differently."
    },
    {
        "wave": 1, "city": "Sherman Oaks", "slug": "sherman-oaks", "place_type": "Neighborhood",
        "zips": "91401, 91403, 91411, 91423", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.35M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Move-Up",
        "lead": "Local mortgage strategy for Sherman Oaks detached homes, hillside properties, condos, and move-up buyers.",
        "market": "Sherman Oaks had a June 2026 Zillow ZHVI around $1.35M, close enough to the Los Angeles County conforming ceiling that financing can change from high-balance conforming to jumbo based on the specific home and down payment.",
        "local_angle": "That threshold effect makes scenario planning valuable: a modest change in down payment can change the loan category, while a buyer selling another home may need to compare liquidity and timing before deciding how much cash to deploy at closing.",
        "property_note": "Sherman Oaks also has meaningful condo and townhome inventory. In those transactions, the HOA and project can become a second underwriting file, so project review should start early when there is litigation, insurance, reserve, maintenance, or questionnaire uncertainty.",
        "areas": ["South of Ventura", "Chandler Estates", "Fashion Square area", "Hillside neighborhoods"],
        "paths": ["jumbo", "bridge", "self", "condo", "equity", "secondlook"],
        "special_q": "Why can the same Sherman Oaks purchase be conforming with one down payment and jumbo with another?",
        "special_a": "Because the conforming limit applies to the loan amount, not the purchase price. A different down payment can move the requested loan above or below the Los Angeles County one-unit limit."
    },

    # ------------------------------- Wave 2 -------------------------------
    {
        "wave": 2, "city": "Pacific Palisades", "slug": "pacific-palisades", "place_type": "Neighborhood",
        "zips": "90272", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": None, "median_note": None, "property_card": "Rebuild + high-value", "focus": "Rebuild + Jumbo",
        "lead": "Rebuild, jumbo, equity, and move-up financing strategy for Pacific Palisades homeowners and buyers.",
        "market": "Pacific Palisades requires a different local mortgage conversation in 2026 because ordinary high-value purchase financing now sits alongside wildfire rebuild, insurance-proceeds, lot-ownership, construction-budget, and replacement-home decisions.",
        "local_angle": "A homeowner who already owns the lot may need a construction or rebuild structure, while another household may choose to purchase elsewhere before the original property is rebuilt or sold. Those are different financing problems and should not be pushed through one generic application path.",
        "property_note": "Insurance proceeds, existing liens, construction contracts, permits, completed value, and borrower liquidity can all affect the structure. Rebuild financing availability is lender- and program-specific.",
        "areas": ["Alphabet Streets", "Huntington Palisades", "Marquez area", "Palisades Highlands"],
        "paths": ["rebuild", "jumbo", "bridge", "equity", "self", "secondlook"],
        "special_q": "Can a homeowner finance a Pacific Palisades rebuild if the lot is already owned?",
        "special_a": "Potentially. The available structure depends on existing liens, insurance proceeds, construction budget, completed value, borrower qualification, and the lender's construction or rebuild guidelines."
    },
    {
        "wave": 2, "city": "Westlake Village", "slug": "westlake-village", "place_type": "City / postal area",
        "zips": "91361, 91362", "limit_display": "$1.249M / $1.035M", "limit_label": "LA / Ventura 2026 1-unit limits",
        "median": "$1.61M", "median_note": "Zillow ZHVI, June 2026", "focus": "County Check + Jumbo",
        "lead": "A county-aware mortgage review for Westlake Village and nearby Westlake postal addresses.",
        "market": "Westlake Village is a useful example of why the exact property address matters. The incorporated City of Westlake Village is in Los Angeles County, while nearby Westlake-area properties using the same general place name can be in Ventura County.",
        "local_angle": "That county distinction matters because the 2026 one-unit conforming limit is $1,249,125 in Los Angeles County and $1,035,000 in Ventura County. The same purchase price can therefore fall into a different loan category depending on the actual parcel location and requested loan amount.",
        "property_note": "Before comparing rates, verify county, occupancy, property type, loan amount, and whether a current home must sell first. That sequence prevents a borrower from solving the wrong financing problem.",
        "areas": ["Westlake Village", "North Ranch area", "Westlake Lake area", "Nearby Thousand Oaks / Westlake postal area"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "Why can two Westlake Village mailing addresses have different conforming limits?",
        "special_a": "Because conforming limits are county-based. A property in Los Angeles County uses the Los Angeles County limit, while a property in Ventura County uses the Ventura County limit. The parcel location, not the marketing name, controls."
    },
    {
        "wave": 2, "city": "Marina del Rey", "slug": "marina-del-rey", "place_type": "Community",
        "zips": "90292", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.34M", "median_note": "Zillow ZHVI, June 2026", "focus": "Condo + Jumbo",
        "lead": "Condo-project and jumbo mortgage planning for Marina del Rey buyers, owners, and investors.",
        "market": "Marina del Rey had a June 2026 Zillow ZHVI around $1.34M, close to the Los Angeles County conforming ceiling, but the more important local distinction is the heavy concentration of condos, attached homes, and waterfront projects.",
        "local_angle": "A borrower may qualify cleanly while the project creates the financing problem. Master insurance, litigation, reserves, deferred maintenance, commercial characteristics, short-term rental activity, or other project factors can change the available lender set.",
        "property_note": "For that reason, a project pre-screen can be more valuable than another borrower application when the property is inside an HOA or condominium project.",
        "areas": ["Marina Peninsula", "Silver Strand area", "Waterfront condo communities", "Harbor-adjacent residences"],
        "paths": ["condo", "jumbo", "bridge", "self", "secondlook", "dscr"],
        "special_q": "Can a Marina del Rey condo be declined even if the borrower is fully qualified?",
        "special_a": "Yes. Condo project eligibility is separate from borrower qualification. Insurance, litigation, reserves, repairs, ownership concentration, or other project factors can affect lender eligibility."
    },
    {
        "wave": 2, "city": "Torrance", "slug": "torrance", "place_type": "City",
        "zips": "90501, 90503, 90504, 90505", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.12M", "median_note": "Zillow ZHVI, June 2026", "focus": "Conforming / Jumbo Line",
        "lead": "Mortgage planning around the conforming-to-jumbo threshold for Torrance buyers and homeowners.",
        "market": "Torrance had a June 2026 Zillow ZHVI around $1.12M, which places many transactions near the Los Angeles County conforming ceiling rather than far above it. That makes loan amount and down payment especially important to program selection.",
        "local_angle": "A buyer can sometimes remain in a conforming or high-balance structure with one down payment and move into jumbo with another. Existing homeowners may also compare whether to use equity for the next purchase instead of selling first.",
        "property_note": "The city includes detached homes, townhomes, and condo inventory, so property and project review should be matched to the actual address rather than assumed from the city name.",
        "areas": ["South Torrance", "West Torrance", "North Torrance", "Old Torrance"],
        "paths": ["jumbo", "bridge", "self", "equity", "condo", "secondlook"],
        "special_q": "Is every Torrance purchase a jumbo loan?",
        "special_a": "No. Torrance values often sit around the conforming threshold. Whether the loan is conforming or jumbo depends on the requested loan amount after down payment, not the purchase price alone."
    },
    {
        "wave": 2, "city": "Hermosa Beach", "slug": "hermosa-beach", "place_type": "City",
        "zips": "90254", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$2.30M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Move-Up",
        "lead": "High-value beach-city purchase, move-up, and equity planning for Hermosa Beach.",
        "market": "Hermosa Beach had a June 2026 Zillow ZHVI around $2.30M, well above the Los Angeles County one-unit conforming ceiling. Jumbo financing is therefore common for standard detached-home purchases.",
        "local_angle": "The compact, high-equity market also creates frequent timing questions for owners moving from one coastal property to another. Bridge and home-equity options can be worth reviewing before accepting a sale contingency as the only path.",
        "property_note": "Condos and attached properties should still be reviewed for project eligibility when applicable, especially when there are insurance, repair, reserve, or HOA-document concerns.",
        "areas": ["Sand Section", "Hermosa Valley", "North Hermosa", "East Hermosa"],
        "paths": ["jumbo", "bridge", "self", "equity", "condo", "secondlook"],
        "special_q": "Can a Hermosa Beach seller buy the next home before the current home closes?",
        "special_a": "Potentially. Depending on equity, debt-to-income, liquidity, and program availability, a bridge or equity-based structure may allow the next purchase to be evaluated without waiting for the current sale to close."
    },
    {
        "wave": 2, "city": "Redondo Beach", "slug": "redondo-beach", "place_type": "City",
        "zips": "90277, 90278", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.50M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Condo",
        "lead": "Jumbo, condo-project, and move-up financing for North and South Redondo Beach.",
        "market": "Redondo Beach had a June 2026 Zillow ZHVI around $1.50M, above the Los Angeles County conforming ceiling. Many detached-home and townhome transactions therefore require jumbo or careful high-balance planning.",
        "local_angle": "The market also has a meaningful attached-home and condominium component. When an HOA or project is involved, a lender must evaluate more than the borrower, making early project review especially valuable in a short escrow.",
        "property_note": "For existing homeowners, home equity can also be part of a move-up plan, a renovation plan, or a way to avoid replacing a favorable first mortgage when another eligible second-lien structure fits better.",
        "areas": ["South Redondo", "North Redondo", "Riviera Village area", "Golden Hills"],
        "paths": ["jumbo", "condo", "bridge", "self", "equity", "secondlook"],
        "special_q": "What should a Redondo Beach condo buyer check before appraisal?",
        "special_a": "Review the project early for master insurance, litigation, reserves, repairs, ownership concentration, and any known questionnaire issues. Borrower approval alone does not approve the condo project."
    },
    {
        "wave": 2, "city": "Culver City", "slug": "culver-city", "place_type": "City",
        "zips": "90230, 90232", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.31M", "median_note": "Zillow ZHVI, June 2026", "focus": "Threshold + Complex Income",
        "lead": "Conforming-versus-jumbo and complex-income planning for Culver City buyers and homeowners.",
        "market": "Culver City had a June 2026 Zillow ZHVI around $1.31M, very close to the Los Angeles County conforming ceiling. That makes this a market where down payment and exact loan amount can materially change program selection.",
        "local_angle": "Borrowers working in media, technology, professional services, or self-employment may also have bonus, stock, commission, 1099, or business income that different lenders analyze differently. Documentation strategy should be tested before escrow becomes tight.",
        "property_note": "Culver City includes detached homes, condos, and townhomes. When the property is attached or in an HOA, project eligibility may need to be checked separately from borrower qualification.",
        "areas": ["Culver Crest", "Carlson Park", "Blair Hills", "Downtown Culver City"],
        "paths": ["jumbo", "bridge", "self", "condo", "equity", "secondlook"],
        "special_q": "Why is down payment strategy especially important in Culver City?",
        "special_a": "Because many purchase prices sit close to the county's conforming threshold. The requested loan amount after down payment determines whether the file is conforming or jumbo."
    },
    {
        "wave": 2, "city": "Studio City", "slug": "studio-city", "place_type": "Neighborhood",
        "zips": "91604", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.58M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + Self-Employed",
        "lead": "Jumbo and complex-income mortgage planning for Studio City buyers and entertainment-industry households.",
        "market": "Studio City had a June 2026 Zillow ZHVI around $1.58M, above the Los Angeles County conforming ceiling. Prime hillside and detached-home purchases commonly require jumbo financing.",
        "local_angle": "Variable compensation, project-based income, business income, bonuses, and multiple entities can make income documentation more important than the headline rate. The lender should be chosen after the income is organized, not before.",
        "property_note": "Condos and attached homes add project eligibility to the analysis, while hillside or highly renovated properties can create appraisal questions that should be identified early.",
        "areas": ["Colfax Meadows", "Fryman Canyon", "Studio City Hills", "Tujunga Village area"],
        "paths": ["jumbo", "self", "bridge", "equity", "condo", "secondlook"],
        "special_q": "Can project-based or variable income be used for a Studio City mortgage?",
        "special_a": "Potentially. The answer depends on income history, continuity, documentation, loan program, and lender rules. Different lenders may analyze the same income stream differently."
    },
    {
        "wave": 2, "city": "Woodland Hills", "slug": "woodland-hills", "place_type": "Neighborhood",
        "zips": "91364, 91367", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$1.21M", "median_note": "Zillow ZHVI, June 2026", "focus": "Threshold + Move-Up",
        "lead": "Move-up, jumbo-threshold, and equity planning for Woodland Hills buyers and homeowners.",
        "market": "Woodland Hills had a June 2026 Zillow ZHVI around $1.21M, very close to the Los Angeles County conforming ceiling. Some purchases remain conforming while larger, hillside, or more highly improved homes move into jumbo territory.",
        "local_angle": "That makes it useful to compare loan categories before committing cash. A buyer selling another Valley property may have several viable structures depending on equity, reserves, and timing.",
        "property_note": "The area also includes condos and townhomes around major corridors and Warner Center, so project eligibility can become relevant on attached-property purchases.",
        "areas": ["South of Ventura", "Walnut Acres", "Warner Center", "Western Woodland Hills"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "Does a Woodland Hills purchase automatically require jumbo financing?",
        "special_a": "No. The typical value is close to the conforming ceiling. The requested loan amount after down payment determines whether the loan is conforming or jumbo."
    },
    {
        "wave": 2, "city": "Brentwood", "slug": "brentwood", "place_type": "Neighborhood",
        "zips": "90049", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": "$2.88M", "median_note": "Zillow ZHVI, June 2026", "focus": "Jumbo + High Net Worth",
        "lead": "High-value mortgage strategy for Brentwood purchases, business owners, and existing homeowners with significant equity.",
        "market": "Brentwood had a June 2026 Zillow ZHVI around $2.88M, well above the Los Angeles County conforming ceiling. Jumbo financing is therefore the normal starting point for many detached-home transactions.",
        "local_angle": "High-value borrowers may have substantial assets but income that is spread across businesses, partnerships, bonuses, investments, or other sources. The underwriting strategy should reflect the full financial profile rather than forcing every borrower into one documentation model.",
        "property_note": "For homeowners with a low-rate first mortgage, an equity or second-lien review can also be more relevant than immediately replacing the first mortgage through cash-out refinance.",
        "areas": ["Brentwood Park", "Brentwood Glen", "Mandeville Canyon", "Kenter Canyon area"],
        "paths": ["jumbo", "bridge", "self", "equity", "secondlook", "dscr"],
        "special_q": "What matters most in a Brentwood jumbo file besides credit score?",
        "special_a": "Loan amount, liquidity, reserves, income documentation, property type, occupancy, and the lender's specific jumbo guidelines can all materially affect the available structure."
    },
    {
        "wave": 2, "city": "West Los Angeles", "slug": "west-los-angeles", "place_type": "Neighborhood",
        "zips": "90025, 90064", "limit_display": LA_LIMIT, "limit_label": "2026 Los Angeles County 1-unit limit",
        "median": None, "median_note": None, "property_card": "Condos + detached", "focus": "Condo + Jumbo",
        "lead": "Property-specific mortgage planning for West Los Angeles condos, detached homes, and move-up buyers.",
        "market": "West Los Angeles is not tracked by Zillow as one single standalone ZHVI geography, which is a useful reminder that the financing strategy should be built around the actual address rather than an artificial citywide average.",
        "local_angle": "The area mixes condos, townhomes, and high-value detached homes. Some transactions fit conforming or high-balance programs; others require jumbo. The requested loan amount, not a neighborhood label, determines the category.",
        "property_note": "Because attached housing is common, HOA insurance, reserves, litigation, deferred maintenance, and project-review findings can become decisive. A condo pre-screen can therefore be more useful than repeatedly changing lenders after a project issue is discovered.",
        "areas": ["West LA", "Sawtelle", "Rancho Park", "Cheviot Hills-adjacent 90064"],
        "paths": ["condo", "jumbo", "bridge", "self", "equity", "secondlook"],
        "special_q": "Why does West Los Angeles need an address-specific mortgage review?",
        "special_a": "Because the area contains a wide range of property types and price points. Loan category and project eligibility can change materially from one property to another even within the same ZIP code."
    },
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def tracked_url(url: str, slug: str) -> str:
    if not url.startswith("http"):
        return url
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}utm_source=westccmortgage&utm_medium=local_market&utm_campaign={slug}"


def schema_blocks(m: dict) -> str:
    url = f"{BASE}/mortgage/{m['slug']}"
    service = {
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Mortgage Financing in {m['city']}", "url": url,
        "provider": {
            "@type": "Organization", "name": COMPANY, "url": BASE,
            "telephone": "+1-310-654-1577",
            "identifier": {"@type": "PropertyValue", "name": "NMLS", "value": NMLS},
        },
        "areaServed": {"@type": m.get("place_type", "Place").split(" /")[0], "name": m["city"]},
        "serviceType": "Residential mortgage brokerage and mortgage scenario review",
    }
    crumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "California Local Markets", "item": BASE + "/california-mortgage-locations"},
            {"@type": "ListItem", "position": 3, "name": m["city"], "item": url},
        ],
    }
    faqs = faq_items(m)
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
    ]}
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False) for o in (service, crumb, faq))


def faq_items(m: dict):
    if m["slug"] == "westlake-village":
        q1 = "What is the 2026 conforming loan limit around Westlake Village?"
        a1 = "The limit depends on the actual county. Los Angeles County's 2026 one-unit limit is $1,249,125, while Ventura County's is $1,035,000. Verify the parcel county before choosing the loan category."
    else:
        q1 = f"What is the 2026 conforming loan limit in {m['city']}?"
        a1 = f"For a one-unit property in Los Angeles County, the 2026 conforming limit is {LA_LIMIT}. A loan amount above that ceiling is jumbo. The loan amount after down payment, not the purchase price alone, controls."
    if m.get("median"):
        q2 = f"Does a typical {m['city']} purchase automatically require a jumbo loan?"
        a2 = f"Not automatically. The local June 2026 Zillow ZHVI reference is about {m['median']}, but jumbo status is determined by the requested loan amount after down payment."
    else:
        q2 = f"Does every {m['city']} property use the same mortgage program?"
        a2 = "No. The correct program depends on the exact address, requested loan amount, occupancy, borrower profile, property type, and lender guidelines."
    q3 = f"Can I buy in {m['city']} before selling my current home?"
    a3 = "Potentially. Depending on equity, current liens, debt-to-income, liquidity, and program availability, a bridge, second-lien, or other move-up structure may be worth comparing with a sale-contingent purchase."
    return [(q1, a1), (q2, a2), (q3, a3), (m["special_q"], m["special_a"])]


def path_cards(m: dict) -> str:
    cards = []
    for key in m["paths"]:
        title, url, desc = PATHS[key]
        url = tracked_url(url, m["slug"])
        cards.append(
            f'<a class="card" href="{esc(url)}"><span class="label">{esc(title)}</span>'
            f'<h3>{esc(title)}</h3><p>{esc(desc)}</p><span class="more">Review this path <span aria-hidden="true">&rarr;</span></span></a>'
        )
    return "".join(cards)


def page_html(m: dict) -> str:
    url = f"{BASE}/mortgage/{m['slug']}"
    title = f"{m['city']} Mortgage Financing | West Coast Capital Mortgage"
    desc = f"Mortgage financing in {m['city']}, California: {m['focus'].lower()}, self-employed, equity, condo/project and second-look strategies from West Coast Capital Mortgage. NMLS #{NMLS}."
    median_card = (
        f'<div class="card center"><h3 style="color:var(--blue)">{esc(m["median"])}</h3><p style="margin:0">Typical value · {esc(m["median_note"])}</p></div>'
        if m.get("median") else
        f'<div class="card center"><h3 style="color:var(--blue)">{esc(m.get("property_card", "Local review"))}</h3><p style="margin:0">Property-specific planning</p></div>'
    )
    areas = "".join(f'<div class="card center"><h3>{esc(a)}</h3><p style="margin:0">Local financing should be based on the exact property and borrower profile.</p></div>' for a in m["areas"])
    faq_html = "".join(f'<details class="acc"><summary>{esc(q)}</summary><div class="acc-body">{esc(a)}</div></details>' for q, a in faq_items(m))
    source_zillow = ' &middot; <a href="https://www.zillow.com/research/data/" target="_blank" rel="noopener noreferrer">Zillow Research — ZHVI home values, June 2026</a>' if m.get("median") else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<link rel="canonical" href="{esc(url)}"><meta name="robots" content="index, follow, max-image-preview:large"><meta name="author" content="{COMPANY}">
<meta name="geo.region" content="US-CA"><meta name="geo.placename" content="{esc(m['city'])}, California">
<meta property="og:type" content="website"><meta property="og:site_name" content="{COMPANY}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(url)}"><meta property="og:image" content="{BASE}/assets/og-image.jpg"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image">
{schema_blocks(m)}
<!-- Microsoft Clarity --><script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","wzzlo9s35g");</script>
</head>
<body>
<div class="topbar"><div class="wrap topbar-inner"><nav class="topbar-left" aria-label="Utility"><a class="active-service" href="/">Mortgage</a><a href="https://westccrealty.com">Realty</a></nav><div class="topbar-right"><div class="lang-switch" role="group" aria-label="Language"><button type="button" data-lang="en">EN</button><button type="button" data-lang="es">ES</button><button type="button" data-lang="ru">RU</button><button type="button" data-lang="zh">中文</button></div></div></div></div>
<header class="site-header"><div class="wrap header-inner"><a class="logo" href="/index.html" aria-label="West Coast Capital Mortgage home"><span class="l1">WEST COAST CAPITAL</span><span class="l2">MORTGAGE</span></a><div class="nav-collapse" id="navc"><nav class="mainnav" aria-label="Primary"><a href="/buy.html">Buy a Home</a><a href="/refinance.html">Refinance</a><a href="/rates.html">Today's Rates</a><a href="/loans.html" class="active">Loans</a><a href="/resources.html">Resources</a><a href="/about.html">About Us</a></nav><div class="header-cta"><a class="btn btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Apply Now</a></div></div><button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navc"><span></span><span></span><span></span></button></div></header>
<section class="page-hero"><div class="hero-wallpaper" aria-hidden="true"><div class="wallpaper-line" style="top:18%">WEST COAST CAPITAL MORTGAGE</div><div class="wallpaper-line w2" style="top:58%">WEST COAST CAPITAL MORTGAGE</div></div><div class="wrap page-hero-inner"><div class="crumbs"><a href="/index.html">Home</a> &nbsp;/&nbsp; <a href="/california-mortgage-locations">California Markets</a> &nbsp;/&nbsp; {esc(m['city'])}</div><h1>Mortgage Financing in {esc(m['city'])}</h1><p class="lead">{esc(m['lead'])}</p></div></section>
<section><div class="wrap"><div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">{esc(m['limit_display'])}</h3><p style="margin:0">{esc(m['limit_label'])}</p></div>{median_card}<div class="card center"><h3 style="color:var(--blue)">{esc(m['zips'])}</h3><p style="margin:0">Primary local ZIP code(s)</p></div><div class="card center"><h3 style="color:var(--blue)">{esc(m['focus'])}</h3><p style="margin:0">Primary planning focus</p></div></div></div></section>
<section style="padding-top:0"><div class="wrap split"><div><span class="eyebrow">Local strategy</span><h2>Start with the financing problem, not just the rate.</h2><p>{esc(m['market'])}</p><p>{esc(m['local_angle'])}</p><div class="btn-row"><a class="btn btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Start Application</a><a class="btn btn-outline" href="tel:{PHONE_HREF}">Call {PHONE}</a></div></div><div><h3>What we review first</h3><ul class="feature-list"><li>Purchase price, requested loan amount, down payment, and reserves</li><li>Income type and the documentation path the lender will actually use</li><li>Whether a current home must sell or existing equity should be part of the plan</li><li>Property, HOA/project, appraisal, insurance, or timing issues that may change lender eligibility</li></ul><h3 style="margin-top:30px">Why this matters</h3><p>{esc(m['property_note'])}</p></div></div></section>
<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">Financing paths</span><h2>Common mortgage conversations in {esc(m['city'])}</h2><p>These are separate financing problems. The correct lender and program depend on the actual scenario.</p></div><div class="grid grid-3">{path_cards(m)}</div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Local context</span><h2>{esc(m['city'])} areas we commonly think about as distinct property contexts</h2><p>Neighborhood names do not determine approval, but they help identify property type, price range, HOA/project exposure, lot characteristics, and transaction patterns that can change the mortgage strategy.</p></div><div class="grid grid-4">{areas}</div></div></section>
<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">FAQ</span><h2>{esc(m['city'])} mortgage questions</h2></div>{faq_html}</div></section>
<section style="padding-top:0"><div class="wrap"><h3>Related local and California resources</h3><p><a href="/california-mortgage-locations">See all curated California local mortgage pages</a> &middot; <a href="/jumbo-loans">Jumbo Loans</a> &middot; <a href="/self-employed-borrowers">Self-Employed Borrowers</a> &middot; <a href="https://californiamtg.com/second-look?utm_source=westccmortgage&amp;utm_medium=local_market&amp;utm_campaign={esc(m['slug'])}">Mortgage Second Look</a></p></div></section>
<section style="padding-top:0"><div class="wrap"><p class="muted" style="font-size:.85rem"><b>Sources &amp; data notes:</b> <a href="https://www.fhfa.gov/data/conforming-loan-limit-cll-values" target="_blank" rel="noopener noreferrer">FHFA 2026 conforming loan limits</a>{source_zillow}. Market figures are rounded educational references, not appraisals. Program availability, property eligibility, loan limits, and underwriting guidelines are subject to change.</p></div></section>
<section><div class="wrap"><div class="cta-band"><h2>Have a {esc(m['city'])} mortgage scenario?</h2><p>Send the actual property, loan amount, income type, and timing. We will help organize the scenario before you commit to the wrong lender path.</p><div class="btn-row"><a class="btn btn-lg btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Start Application</a><a class="btn btn-lg btn-outline-light" href="tel:{PHONE_HREF}">Call {PHONE}</a></div></div></div></section>
<footer class="site-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><div class="l1">WEST COAST CAPITAL</div><div class="l2">MORTGAGE</div><p style="color:#aab2bd;font-size:.9rem">Modern mortgage guidance for buying, refinancing, and building equity.</p><p class="footer-contact"><b>Phone:</b> <a href="tel:{PHONE_HREF}">{PHONE}</a><br><b>Office:</b> 150 E Olive Ave, Unit 112, Burbank, CA 91502</p></div><div><h4>Local</h4><a href="/california-mortgage-locations">California Local Markets</a><a href="/loans/jumbo/los-angeles-county">Los Angeles County Jumbo</a><a href="/loans/dscr/los-angeles-metro">Los Angeles DSCR</a></div><div><h4>Loans</h4><a href="/jumbo-loans">Jumbo Loans</a><a href="/non-qm-loans">Non-QM Loans</a><a href="/bank-statement-loans">Bank Statement Loans</a><a href="/dscr-loans">DSCR Loans</a><a href="/heloc">HELOC / Home Equity</a></div><div><h4>About</h4><a href="/about">About West Coast Capital Mortgage</a><a href="/contact">Contact Us</a><a href="https://www.nmlsconsumeraccess.org/" target="_blank" rel="noopener noreferrer">NMLS Consumer Access</a></div></div><div class="footer-bottom"><div class="row"><span class="eho"><img src="/assets/equal-housing.svg" alt="Equal Housing Opportunity" style="height:32px;vertical-align:middle;margin-right:7px;opacity:.92"> Equal Housing Opportunity</span></div><p>{COMPANY}. Company NMLS #{NMLS}. CA DRE Corporation License #{CA_DRE}. Anatoliy Kanevsky NMLS #{LO_NMLS}, CA Broker DRE #{LO_DRE}. Equal Housing Opportunity. Educational information only; not a commitment to lend, approval, rate quote, or guarantee. All loans are subject to applicable underwriting and property requirements.</p><p>&copy; <span class="year"></span> {COMPANY}. All rights reserved.</p></div></div></footer>
<script src="/i18n.js"></script><script src="/script.js"></script>
</body></html>'''


def hub_html() -> str:
    def cards(wave):
        out = []
        for m in [x for x in MARKETS if x["wave"] == wave]:
            out.append(f'<a class="card" href="/mortgage/{esc(m["slug"])}"><span class="label">{esc(m["focus"])}</span><h3>{esc(m["city"])}</h3><p>{esc(m["lead"])}</p><span class="more">Open local guide <span aria-hidden="true">&rarr;</span></span></a>')
        return "".join(out)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>California Local Mortgage Markets | West Coast Capital Mortgage</title><meta name="description" content="Curated California local mortgage guides for Manhattan Beach, Palos Verdes, Calabasas, Encino, Sherman Oaks, Pacific Palisades, Westside and South Bay markets. NMLS #{NMLS}."><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/styles.css"><link rel="canonical" href="{BASE}/california-mortgage-locations"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="author" content="{COMPANY}"></head><body>
<div class="topbar"><div class="wrap topbar-inner"><nav class="topbar-left"><a class="active-service" href="/">Mortgage</a><a href="https://westccrealty.com">Realty</a></nav></div></div><header class="site-header"><div class="wrap header-inner"><a class="logo" href="/index.html"><span class="l1">WEST COAST CAPITAL</span><span class="l2">MORTGAGE</span></a><div class="nav-collapse" id="navc"><nav class="mainnav"><a href="/buy.html">Buy a Home</a><a href="/refinance.html">Refinance</a><a href="/rates.html">Today's Rates</a><a href="/loans.html" class="active">Loans</a><a href="/resources.html">Resources</a><a href="/about.html">About Us</a></nav><div class="header-cta"><a class="btn btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Apply Now</a></div></div><button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navc"><span></span><span></span><span></span></button></div></header>
<section class="page-hero"><div class="hero-wallpaper" aria-hidden="true"><div class="wallpaper-line" style="top:18%">WEST COAST CAPITAL MORTGAGE</div><div class="wallpaper-line w2" style="top:58%">WEST COAST CAPITAL MORTGAGE</div></div><div class="wrap page-hero-inner"><div class="crumbs"><a href="/">Home</a> &nbsp;/&nbsp; California Markets</div><h1>California Local Mortgage Strategy</h1><p class="lead">A curated set of local pages where the financing answer is genuinely different — not hundreds of city-name doorway pages.</p></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Priority markets</span><h2>South Bay, Palos Verdes, Calabasas and the Valley</h2><p>These pages receive the strongest growth priority because they combine high-value transactions with specific financing problems we can actually solve.</p></div><div class="grid grid-3">{cards(1)}</div></div></section>
<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">Additional local markets</span><h2>Westside, Beach Cities and supporting Valley markets</h2><p>Each page has its own property, county, condo, rebuild, move-up, or income-documentation angle.</p></div><div class="grid grid-3">{cards(2)}</div></div></section>
<section><div class="wrap"><div class="cta-band"><h2>Not sure which local page fits?</h2><p>Call us with the property address and scenario. We will start with the financing problem rather than forcing the file into a generic city page.</p><div class="btn-row"><a class="btn btn-lg btn-blue" href="tel:{PHONE_HREF}">Call {PHONE}</a><a class="btn btn-lg btn-outline-light" href="/loans.html">All Loan Programs</a></div></div></div></section>
<footer class="site-footer"><div class="wrap"><div class="footer-bottom"><div class="row"><span class="eho"><img src="/assets/equal-housing.svg" alt="Equal Housing Opportunity" style="height:32px;vertical-align:middle;margin-right:7px"> Equal Housing Opportunity</span></div><p>{COMPANY}. Company NMLS #{NMLS}. CA DRE Corporation License #{CA_DRE}. Anatoliy Kanevsky NMLS #{LO_NMLS}, CA Broker DRE #{LO_DRE}. 150 E Olive Ave, Unit 112, Burbank, CA 91502. {PHONE}.</p><p>&copy; <span class="year"></span> {COMPANY}.</p></div></div></footer><script src="/script.js"></script></body></html>'''


def replace_marker_block(text: str, start: str, end: str, block: str, before: str | None = None) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    wrapped = start + "\n" + block.rstrip() + "\n" + end
    if pattern.search(text):
        return pattern.sub(wrapped, text)
    if before and before in text:
        return text.replace(before, wrapped + "\n" + before, 1)
    return text.replace("</urlset>", wrapped + "\n</urlset>") if "</urlset>" in text else text + "\n" + wrapped + "\n"


def sitemap_entries(markets, growth=False) -> str:
    rows = []
    if not growth:
        rows.append(f'  <url><loc>{BASE}/california-mortgage-locations</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>')
    else:
        rows.append(f'  <url><loc>{BASE}/california-mortgage-locations</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>')
    for m in markets:
        priority = "0.9" if m["wave"] == 1 else ("0.8" if growth else "0.8")
        freq = "weekly" if growth and m["wave"] == 1 else "monthly"
        rows.append(f'  <url><loc>{BASE}/mortgage/{m["slug"]}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>')
    return "\n".join(rows)


def loans_block() -> str:
    priority = [m for m in MARKETS if m["wave"] == 1]
    cards = "".join(f'<a class="card" href="/mortgage/{m["slug"]}"><span class="label">{esc(m["focus"])}</span><h3>{esc(m["city"])}</h3><p>{esc(m["lead"])}</p><span class="more">Local mortgage guide <span aria-hidden="true">&rarr;</span></span></a>' for m in priority)
    return f'''<section class="bg-light"><div class="wrap"><div class="section-head"><span class="eyebrow">California local strategy</span><h2>Featured local mortgage markets</h2><p>We consolidated hundreds of repetitive city pages. These flagship markets are different: each has a real local financing angle and a specific path to a mortgage conversation.</p></div><div class="grid grid-3">{cards}</div><div class="btn-row" style="margin-top:28px"><a class="btn btn-blue" href="/california-mortgage-locations">See all curated local markets</a></div></div></section>'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for m in MARKETS:
        (OUT / f"{m['slug']}.html").write_text(page_html(m), encoding="utf-8")
    (ROOT / "california-mortgage-locations.html").write_text(hub_html(), encoding="utf-8")

    sitemap = ROOT / "sitemap.xml"
    xml = sitemap.read_text(encoding="utf-8")
    xml = replace_marker_block(xml, "<!-- local-market-pages:start -->", "<!-- local-market-pages:end -->", sitemap_entries(MARKETS), before="</urlset>")
    sitemap.write_text(xml, encoding="utf-8")

    growth = ROOT / "growth-sitemap.xml"
    gxml = growth.read_text(encoding="utf-8")
    gxml = replace_marker_block(gxml, "<!-- local-market-pages:start -->", "<!-- local-market-pages:end -->", sitemap_entries(MARKETS, growth=True), before="</urlset>")
    growth.write_text(gxml, encoding="utf-8")

    loans = ROOT / "loans.html"
    lhtml = loans.read_text(encoding="utf-8")
    start, end = "<!-- LOCAL-MARKETS:start -->", "<!-- LOCAL-MARKETS:end -->"
    before = '<section><div class="wrap"><div class="cta-band">'
    lhtml = replace_marker_block(lhtml, start, end, loans_block(), before=before)
    loans.write_text(lhtml, encoding="utf-8")

    print(f"Built {len(MARKETS)} curated local mortgage pages + hub")
    print("Wave 1:", ", ".join(m["city"] for m in MARKETS if m["wave"] == 1))
    print("Wave 2:", ", ".join(m["city"] for m in MARKETS if m["wave"] == 2))


if __name__ == "__main__":
    main()
