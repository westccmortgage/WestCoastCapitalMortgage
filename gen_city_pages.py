# -*- coding: utf-8 -*-
"""
gen_city_pages.py — Generate program x city local SEO landing pages.

Programs: Jumbo, DSCR. Cities: 14 across Los Angeles County and Orange County.
Outputs root-relative, subfolder-served pages:
  loans/jumbo/{slug}.html  -> /loans/jumbo/{slug}
  loans/dscr/{slug}.html   -> /loans/dscr/{slug}

Re-runnable / idempotent: overwrites the 28 target files each run.

2026 loan-limit ground truth (FIXED, verified vs. FHFA/2026 CA county tables):
  baseline conforming (1-unit): $832,750
  high-cost ceiling (1-unit):   $1,249,125
  Per-county 2026 one-unit conforming limit (the jumbo threshold) lives in COUNTY_LIMITS.
  A jumbo loan in a given city = a 1-unit loan ABOVE that city's COUNTY limit.
"""
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

# 2026 one-unit conforming loan limit by county (the jumbo threshold).
# Verified against 2026 FHFA / California county conforming-limit tables.
COUNTY_LIMITS = {
    "Los Angeles County": "$1,249,125",
    "Orange County": "$1,249,125",
    "San Diego County": "$1,104,000",
    "Ventura County": "$1,035,000",
    "Santa Barbara County": "$941,850",
    "Kern County": "$832,750",
    "San Bernardino County": "$832,750",
    "Riverside County": "$832,750",
    # ---- Wave 2: San Diego radius ----
    "Imperial County": "$832,750",
    # ---- Wave 2: San Francisco radius ----
    "San Francisco County": "$1,249,125",
    "San Mateo County": "$1,249,125",
    "Santa Clara County": "$1,249,125",
    "Alameda County": "$1,249,125",
    "Contra Costa County": "$1,249,125",
    "Marin County": "$1,249,125",
    "Santa Cruz County": "$1,249,125",
    "San Benito County": "$1,249,125",
    "Napa County": "$1,017,750",
    "Monterey County": "$994,750",
    "Sonoma County": "$897,000",
    "Solano County": "$832,750",
    "Sacramento County": "$832,750",
    "San Joaquin County": "$832,750",
    "Stanislaus County": "$832,750",
    "Merced County": "$832,750",
    "Placer County": "$832,750",
    "El Dorado County": "$832,750",
    "Yolo County": "$832,750",
}
HIGH_COST_CEILING = "$1,249,125"
BASELINE_LIMIT = "$832,750"
LASTMOD = "2026-06-09"
PHONE = "+1-310-654-1577"
NMLS = "2817729"


def limit_for(c):
    """Return the 2026 one-unit conforming limit string for a city's county."""
    return COUNTY_LIMITS[c["county"]]


def is_high_cost(county):
    """True when the county limit is above the national baseline."""
    return COUNTY_LIMITS[county] != BASELINE_LIMIT

# ---------------------------------------------------------------------------
# CITY_DATA — per-city unique content.
#   median: rounded, "approximate as of mid-2026" labeling applied in copy.
#   market: city-specific market angle (jumbo + dscr variants).
#   faqs: list of {q, a} dicts — city-specific (built per program below).
# ---------------------------------------------------------------------------
CITY_DATA = [
    {
        "city": "Beverly Hills", "slug": "beverly-hills", "county": "Los Angeles County",
        "median": "approximately $3.69M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "In Beverly Hills the typical home value sits far above the 2026 high-cost conforming ceiling, so the overwhelming majority of Beverly Hills purchases and refinances are financed as jumbo loans rather than conforming loans.",
        "dscr_market": "Beverly Hills commands some of the highest rents in Southern California, and demand from long-term and luxury short-term tenants gives investors a strong rental-income basis for a DSCR loan — though at these price points cash flow is rarely the only consideration.",
    },
    {
        "city": "Santa Monica", "slug": "santa-monica", "county": "Los Angeles County",
        "median": "approximately $1.7M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "With the typical Santa Monica home priced well above the 2026 conforming ceiling, most single-family and many condo purchases here require jumbo financing to reach the full purchase price.",
        "dscr_market": "Santa Monica's coastal location, walkability, and tech-and-entertainment employment base keep rental demand high year-round, making it a popular market for DSCR-financed long-term rentals.",
    },
    {
        "city": "Culver City", "slug": "culver-city", "county": "Los Angeles County",
        "median": "approximately $1.31M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Culver City's typical home value runs above the 2026 conforming ceiling, so a substantial share of detached-home purchases here cross into jumbo territory even though entry-level condos may still fit conforming limits.",
        "dscr_market": "Culver City's transformation into a media-and-tech hub (anchored by major studio and streaming campuses) has driven steady rental demand, supporting DSCR loans for investors targeting professional tenants.",
    },
    {
        "city": "Manhattan Beach", "slug": "manhattan-beach", "county": "Los Angeles County",
        "median": "approximately $3.32M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Manhattan Beach is one of the South Bay's priciest markets, with typical values several times the 2026 conforming ceiling — virtually every standard purchase here is financed as a jumbo loan.",
        "dscr_market": "Manhattan Beach's beach-town premium translates into high rents for both long-term and vacation rentals, giving DSCR investors a strong income basis even as high purchase prices keep coverage ratios in focus.",
    },
    {
        "city": "Torrance", "slug": "torrance", "county": "Los Angeles County",
        "median": "approximately $1.12M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Torrance sits right around the 2026 conforming ceiling, so whether a purchase needs a jumbo loan often comes down to the specific home and down payment — larger detached homes here frequently push the loan amount above the limit.",
        "dscr_market": "Torrance's stable, employment-rich South Bay economy and family-oriented neighborhoods produce reliable long-term rental demand, a profile many DSCR investors favor for predictable cash flow.",
    },
    {
        "city": "West Los Angeles", "slug": "west-los-angeles", "county": "Los Angeles County",
        "median": "not tracked separately by Zillow",
        "jumbo_market": "Typical West Los Angeles home values run above the 2026 conforming ceiling, so a large share of single-family purchases on the Westside are financed with jumbo loans rather than conforming loans.",
        "dscr_market": "West Los Angeles's dense mix of professionals, students, and proximity to major job centers keeps rental occupancy high, making it a frequent target for DSCR-financed rental acquisitions.",
    },
    {
        "city": "Los Angeles", "slug": "los-angeles", "county": "Los Angeles County",
        "median": "approximately $950K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Citywide, the typical Los Angeles home value sits near the 2026 conforming ceiling, but in the city's higher-priced neighborhoods purchase prices routinely exceed it — and those buyers turn to jumbo financing.",
        "dscr_market": "As one of the nation's largest rental markets, Los Angeles offers deep, diverse tenant demand across neighborhoods, giving DSCR investors a wide range of cash-flowing rental opportunities.",
    },
    {
        "city": "Long Beach", "slug": "long-beach", "county": "Los Angeles County",
        "median": "approximately $860K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Long Beach purchases fall below the 2026 conforming ceiling, so jumbo loans here typically come into play for higher-end coastal and waterfront homes rather than the typical single-family purchase.",
        "dscr_market": "Long Beach's relatively accessible prices combined with strong rental demand near the port, downtown, and the universities make it one of the more cash-flow-friendly DSCR markets in Los Angeles County.",
    },
    {
        "city": "Glendale", "slug": "glendale", "county": "Los Angeles County",
        "median": "approximately $1.2M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Glendale's typical home value runs at or slightly above the 2026 conforming ceiling, so many detached-home purchases here — especially in the hillside neighborhoods — require jumbo financing.",
        "dscr_market": "Glendale's central location, strong schools, and large multifamily inventory support consistent rental demand, making it a practical market for DSCR investors building a local portfolio.",
    },
    {
        "city": "Pasadena", "slug": "pasadena", "county": "Los Angeles County",
        "median": "approximately $1.21M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Pasadena's typical home value sits around the 2026 conforming ceiling, and its larger historic and estate homes regularly carry prices well above it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "Pasadena's universities, hospitals, and employment base anchor steady rental demand, and its mix of condos and single-family homes gives DSCR investors flexible options across price points.",
    },
    {
        "city": "Burbank", "slug": "burbank", "county": "Los Angeles County",
        "median": "approximately $1.19M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Burbank's typical home value sits near the 2026 conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger or updated properties frequently push past the limit.",
        "dscr_market": "Home to major studios, Burbank draws a steady stream of entertainment-industry renters, supporting reliable occupancy for DSCR-financed long-term rentals.",
    },
    {
        "city": "Irvine", "slug": "irvine", "county": "Orange County",
        "median": "approximately $1.54M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Irvine's typical home value runs above the 2026 Orange County conforming ceiling, so the majority of single-family purchases in this master-planned city are financed with jumbo loans.",
        "dscr_market": "Irvine's top-rated schools, large university population, and corporate employment base produce some of Orange County's most consistent rental demand, a profile DSCR investors prize for stability.",
    },
    {
        "city": "Newport Beach", "slug": "newport-beach", "county": "Orange County",
        "median": "approximately $3.73M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Newport Beach is among Orange County's most expensive markets, with typical values far above the 2026 conforming ceiling — nearly every standard purchase here is financed as a jumbo loan.",
        "dscr_market": "Newport Beach's coastal premium drives high rents across long-term and vacation rentals, giving DSCR investors a strong income basis even as elevated purchase prices keep coverage ratios in focus.",
    },
    {
        "city": "Anaheim", "slug": "anaheim", "county": "Orange County",
        "median": "approximately $950K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Anaheim purchases fall below the 2026 Orange County conforming ceiling, so jumbo loans here typically apply to larger homes and the higher-priced Anaheim Hills neighborhoods rather than the typical purchase.",
        "dscr_market": "Anaheim's tourism economy, major employers, and proximity to the resort district create strong, year-round rental demand, making it one of Orange County's more approachable DSCR markets on price.",
    },

    # ===================== Los Angeles County (added) =====================
    {
        "city": "Malibu", "slug": "malibu", "county": "Los Angeles County",
        "median": "approximately $3.21M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Malibu is one of the most expensive coastal markets in the country, with typical values many times the 2026 Los Angeles County conforming ceiling — virtually every standard Malibu purchase is financed as a jumbo loan.",
        "dscr_market": "Malibu's oceanfront cachet supports premium long-term and luxury vacation rents, giving DSCR investors a high income basis, though elevated entry prices keep coverage ratios firmly in focus.",
    },
    {
        "city": "Marina del Rey", "slug": "marina-del-rey", "county": "Los Angeles County",
        "median": "approximately $1.34M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Marina del Rey's waterfront condos and homes typically price above the 2026 Los Angeles County conforming ceiling, so a large share of purchases in this harbor community require jumbo financing.",
        "dscr_market": "Marina del Rey's marina lifestyle and Westside job access keep rental demand strong, making it a popular DSCR target for investors focused on professional and waterfront-seeking tenants.",
    },
    {
        "city": "Venice", "slug": "venice", "county": "Los Angeles County",
        "median": "approximately $1.82M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Venice home values run well above the 2026 Los Angeles County conforming ceiling, so most single-family and many remodeled bungalow purchases in this beachside neighborhood are financed as jumbo loans.",
        "dscr_market": "Venice's creative-and-tech 'Silicon Beach' employment base and walkable beach culture drive consistently high rents, a profile DSCR investors favor for both long-term and short-term strategies.",
    },
    {
        "city": "Brentwood", "slug": "brentwood", "county": "Los Angeles County",
        "median": "approximately $2.88M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Brentwood is a premier Westside enclave where typical values sit far above the 2026 Los Angeles County conforming ceiling — nearly all standard purchases here are financed with jumbo loans.",
        "dscr_market": "Brentwood's affluent, school-driven demand and proximity to major job centers support steady high-end rental occupancy, giving DSCR investors a stable, premium-rent income basis.",
    },
    {
        "city": "Westwood", "slug": "westwood", "county": "Los Angeles County",
        "median": "approximately $1.35M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Westwood's typical home value runs above the 2026 Los Angeles County conforming ceiling, so most single-family purchases near UCLA and the village are financed as jumbo loans.",
        "dscr_market": "Westwood's large UCLA student-and-faculty population anchors deep, year-round rental demand, making it one of the Westside's most reliable DSCR markets for occupancy.",
    },
    {
        "city": "Encino", "slug": "encino", "county": "Los Angeles County",
        "median": "approximately $1.44M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Encino's typical home value runs above the 2026 Los Angeles County conforming ceiling, and its larger gated and hillside estates push well past it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "Encino's established San Fernando Valley neighborhoods and strong schools support dependable family-rental demand, a profile many DSCR investors value for predictable cash flow.",
    },
    {
        "city": "Sherman Oaks", "slug": "sherman-oaks", "county": "Los Angeles County",
        "median": "approximately $1.35M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Sherman Oaks home values typically run above the 2026 Los Angeles County conforming ceiling, so a large share of detached-home purchases south of the boulevard require jumbo financing.",
        "dscr_market": "Sherman Oaks' central Valley location, walkable corridors, and entertainment-industry tenants produce steady rental demand that DSCR investors find attractive for long-term holds.",
    },
    {
        "city": "Studio City", "slug": "studio-city", "county": "Los Angeles County",
        "median": "approximately $1.58M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Studio City's typical home value sits above the 2026 Los Angeles County conforming ceiling, so most hillside and prime-flats purchases here are financed as jumbo loans.",
        "dscr_market": "Studio City's proximity to major studios draws a steady stream of entertainment-industry renters, supporting reliable occupancy for DSCR-financed long-term rentals.",
    },
    {
        "city": "Woodland Hills", "slug": "woodland-hills", "county": "Los Angeles County",
        "median": "approximately $1.21M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Woodland Hills sits near the 2026 Los Angeles County conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger or hillside Warner Center-area properties frequently push past the limit.",
        "dscr_market": "Woodland Hills' growing Warner Center employment hub and family neighborhoods generate stable rental demand, a balanced profile for DSCR investors seeking Valley cash flow.",
    },
    {
        "city": "Calabasas", "slug": "calabasas", "county": "Los Angeles County",
        "median": "approximately $1.73M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Calabasas is an affluent gated-community market where typical values run well above the 2026 Los Angeles County conforming ceiling — the majority of purchases here are financed as jumbo loans.",
        "dscr_market": "Calabasas' top schools and luxury-suburban appeal support strong, high-end rental demand, giving DSCR investors a premium income basis in a sought-after Valley submarket.",
    },
    {
        "city": "West Hollywood", "slug": "west-hollywood", "county": "Los Angeles County",
        "median": "approximately $1000K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "West Hollywood's detached homes typically price above the 2026 Los Angeles County conforming ceiling, so single-family purchases here often require jumbo financing even where entry-level condos still fit conforming limits.",
        "dscr_market": "West Hollywood's dense, walkable nightlife-and-design district keeps rental occupancy high among professionals and creatives, a strong profile for DSCR-financed rentals.",
    },
    {
        "city": "Hermosa Beach", "slug": "hermosa-beach", "county": "Los Angeles County",
        "median": "approximately $2.3M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Hermosa Beach is a premium South Bay beach town where typical values run far above the 2026 Los Angeles County conforming ceiling — nearly every standard purchase is financed as a jumbo loan.",
        "dscr_market": "Hermosa Beach's beach-town premium drives high long-term and vacation rents, giving DSCR investors a strong income basis even as elevated prices keep coverage ratios in focus.",
    },
    {
        "city": "Redondo Beach", "slug": "redondo-beach", "county": "Los Angeles County",
        "median": "approximately $1.5M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Redondo Beach home values typically run above the 2026 Los Angeles County conforming ceiling, so most single-family and townhome purchases in this South Bay beach city require jumbo financing.",
        "dscr_market": "Redondo Beach's beach proximity, employment access, and family neighborhoods sustain steady rental demand, making it a dependable South Bay DSCR market.",
    },
    {
        "city": "El Segundo", "slug": "el-segundo", "county": "Los Angeles County",
        "median": "approximately $1.75M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "El Segundo's typical home value runs above the 2026 Los Angeles County conforming ceiling, so a large share of purchases in this compact beach-and-tech city are financed as jumbo loans.",
        "dscr_market": "El Segundo's concentration of aerospace and tech employers ('Silicon Beach South') anchors strong professional rental demand, an appealing profile for DSCR investors.",
    },
    {
        "city": "Rancho Palos Verdes", "slug": "rancho-palos-verdes", "county": "Los Angeles County",
        "median": "approximately $1.83M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Rancho Palos Verdes is a hillside coastal community where typical values run well above the 2026 Los Angeles County conforming ceiling — most ocean-view purchases here are financed as jumbo loans.",
        "dscr_market": "Rancho Palos Verdes' view properties and top schools support premium long-term rents, giving DSCR investors a high income basis on the Palos Verdes Peninsula.",
    },
    {
        "city": "Palos Verdes Estates", "slug": "palos-verdes-estates", "county": "Los Angeles County",
        "median": "approximately $2.79M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Palos Verdes Estates is among the peninsula's most exclusive markets, with typical values far above the 2026 Los Angeles County conforming ceiling — virtually all standard purchases are jumbo loans.",
        "dscr_market": "Palos Verdes Estates' coastal estates and acclaimed schools sustain strong high-end rental demand, a premium profile DSCR investors target for stable upscale tenants.",
    },
    {
        "city": "Inglewood", "slug": "inglewood", "county": "Los Angeles County",
        "median": "approximately $760K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Inglewood purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo loans here typically apply to larger or newly redeveloped homes rather than the typical purchase.",
        "dscr_market": "Inglewood's redevelopment around its sports-and-entertainment district has sharpened rental demand and investor interest, making it one of the area's more cash-flow-oriented DSCR markets.",
    },
    {
        "city": "Hawthorne", "slug": "hawthorne", "county": "Los Angeles County",
        "median": "approximately $880K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Hawthorne purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo loans here generally come into play for larger homes rather than the typical purchase.",
        "dscr_market": "Hawthorne's South Bay location near aerospace and tech employers supports steady, workforce-driven rental demand, a practical profile for DSCR cash-flow investors.",
    },
    {
        "city": "Gardena", "slug": "gardena", "county": "Los Angeles County",
        "median": "approximately $790K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Gardena purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo financing here is generally reserved for larger or higher-end homes.",
        "dscr_market": "Gardena's central South Bay position and accessible prices relative to coastal cities make it one of the more cash-flow-friendly DSCR markets in the area.",
    },
    {
        "city": "Carson", "slug": "carson", "county": "Los Angeles County",
        "median": "approximately $800K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Carson purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo loans here typically apply to larger homes rather than the typical purchase.",
        "dscr_market": "Carson's proximity to the ports, universities, and major freeways supports steady rental demand, giving DSCR investors a workforce-housing angle with relatively approachable prices.",
    },
    {
        "city": "Downey", "slug": "downey", "county": "Los Angeles County",
        "median": "approximately $890K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Downey purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo financing here generally applies to larger or premium homes rather than the typical purchase.",
        "dscr_market": "Downey's established Southeast LA neighborhoods and central location sustain reliable family-rental demand, a steady profile for DSCR investors.",
    },
    {
        "city": "Whittier", "slug": "whittier", "county": "Los Angeles County",
        "median": "approximately $830K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Whittier purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo loans here typically apply to larger hillside or historic homes rather than the typical purchase.",
        "dscr_market": "Whittier's college presence, walkable Uptown, and family neighborhoods produce steady rental demand, a balanced profile for DSCR cash flow.",
    },
    {
        "city": "Arcadia", "slug": "arcadia", "county": "Los Angeles County",
        "median": "approximately $1.41M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Arcadia's typical home value runs above the 2026 Los Angeles County conforming ceiling, and its large rebuilt estates push well past it — the majority of purchases here are financed as jumbo loans.",
        "dscr_market": "Arcadia's acclaimed schools and strong buyer demand support premium rents, giving DSCR investors a high income basis in this San Gabriel Valley submarket.",
    },
    {
        "city": "San Marino", "slug": "san-marino", "county": "Los Angeles County",
        "median": "approximately $2.84M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Marino is one of the San Gabriel Valley's most exclusive markets, with typical values far above the 2026 Los Angeles County conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "San Marino's top-rated schools and estate homes sustain strong high-end rental demand, a premium profile DSCR investors target for upscale, stable tenancy.",
    },
    {
        "city": "La Cañada Flintridge", "slug": "la-canada-flintridge", "county": "Los Angeles County",
        "median": "approximately $2.48M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "La Cañada Flintridge home values run well above the 2026 Los Angeles County conforming ceiling — nearly all standard purchases in this foothill community are financed as jumbo loans.",
        "dscr_market": "La Cañada Flintridge's highly regarded schools and foothill estates support premium rents, giving DSCR investors a strong, upscale income basis.",
    },
    {
        "city": "Santa Clarita", "slug": "santa-clarita", "county": "Los Angeles County",
        "median": "approximately $800K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Santa Clarita purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo loans here typically apply to larger estate and luxury-tract homes rather than the typical purchase.",
        "dscr_market": "Santa Clarita's master-planned communities, strong schools, and family demand make it one of northern LA County's most dependable long-term DSCR rental markets.",
    },
    {
        "city": "Lancaster", "slug": "lancaster", "county": "Los Angeles County",
        "median": "approximately $470K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Lancaster purchases fall well below the 2026 Los Angeles County conforming ceiling, so jumbo financing is rarely needed here and applies only to unusually large or custom Antelope Valley homes.",
        "dscr_market": "Lancaster's affordable prices and steady Antelope Valley rental demand make it one of LA County's stronger markets for DSCR cash flow and rent-to-price ratios.",
    },
    {
        "city": "Palmdale", "slug": "palmdale", "county": "Los Angeles County",
        "median": "approximately $510K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Palmdale purchases fall well below the 2026 Los Angeles County conforming ceiling, so jumbo loans are seldom required here outside of unusually large custom homes.",
        "dscr_market": "Palmdale's low entry prices and consistent Antelope Valley rental demand give DSCR investors some of the most favorable cash-flow math in Los Angeles County.",
    },
    {
        "city": "Pomona", "slug": "pomona", "county": "Los Angeles County",
        "median": "approximately $690K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Pomona purchases fall below the 2026 Los Angeles County conforming ceiling, so jumbo financing here is generally limited to larger or higher-end homes.",
        "dscr_market": "Pomona's universities and central Inland-edge location support steady rental demand at accessible prices, a favorable profile for DSCR cash-flow investors.",
    },

    # ===================== Orange County (added) =====================
    {
        "city": "Costa Mesa", "slug": "costa-mesa", "county": "Orange County",
        "median": "approximately $1.43M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Costa Mesa's typical home value runs above the 2026 Orange County conforming ceiling, so a large share of single-family purchases in this central OC city are financed as jumbo loans.",
        "dscr_market": "Costa Mesa's arts district, retail hubs, and young professional base keep rental demand strong, making it a popular DSCR market for long-term holds.",
    },
    {
        "city": "Huntington Beach", "slug": "huntington-beach", "county": "Orange County",
        "median": "approximately $1.37M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Huntington Beach home values typically run above the 2026 Orange County conforming ceiling, so most single-family purchases in 'Surf City' require jumbo financing.",
        "dscr_market": "Huntington Beach's beach lifestyle and tourism draw sustain strong long-term and vacation rental demand, giving DSCR investors a solid coastal income basis.",
    },
    {
        "city": "Tustin", "slug": "tustin", "county": "Orange County",
        "median": "approximately $1.18M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Tustin sits around the 2026 Orange County conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger or newer Tustin Legacy homes frequently push past the limit.",
        "dscr_market": "Tustin's central OC location, strong schools, and new master-planned housing support steady rental demand, a balanced DSCR profile.",
    },
    {
        "city": "Mission Viejo", "slug": "mission-viejo", "county": "Orange County",
        "median": "approximately $1.22M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Mission Viejo sits near the 2026 Orange County conforming ceiling, so jumbo financing often hinges on the specific home — larger lake-adjacent and view homes commonly exceed the limit.",
        "dscr_market": "Mission Viejo's master-planned community, top schools, and family demand make it one of south OC's most reliable long-term DSCR rental markets.",
    },
    {
        "city": "Fullerton", "slug": "fullerton", "county": "Orange County",
        "median": "approximately $1.05M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Fullerton purchases fall below the 2026 Orange County conforming ceiling, so jumbo loans here typically apply to larger or historic-district homes rather than the typical purchase.",
        "dscr_market": "Fullerton's universities and downtown anchor steady, student-and-professional rental demand, a dependable DSCR profile at relatively accessible OC prices.",
    },
    {
        "city": "Orange", "slug": "orange", "county": "Orange County",
        "median": "approximately $1.14M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard purchases in the City of Orange fall near or below the 2026 Orange County conforming ceiling, so jumbo financing here often depends on the specific home — larger Old Towne and hillside properties can exceed it.",
        "dscr_market": "The City of Orange's historic Old Towne charm, university presence, and central location support steady rental demand for DSCR investors.",
    },
    {
        "city": "Santa Ana", "slug": "santa-ana", "county": "Orange County",
        "median": "approximately $870K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Santa Ana purchases fall below the 2026 Orange County conforming ceiling, so jumbo loans here generally apply to larger or historic homes rather than the typical purchase.",
        "dscr_market": "Santa Ana's dense population, county-seat employment, and downtown revitalization sustain strong rental demand, making it one of OC's more cash-flow-oriented DSCR markets.",
    },
    {
        "city": "Garden Grove", "slug": "garden-grove", "county": "Orange County",
        "median": "approximately $1.02M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Garden Grove purchases fall below the 2026 Orange County conforming ceiling, so jumbo financing here is generally limited to larger homes.",
        "dscr_market": "Garden Grove's central OC location and steady workforce demand support reliable rental occupancy, a practical profile for DSCR investors on price.",
    },
    {
        "city": "Laguna Beach", "slug": "laguna-beach", "county": "Orange County",
        "median": "approximately $3.03M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Laguna Beach is among OC's priciest coastal markets, with typical values far above the 2026 Orange County conforming ceiling — virtually every standard purchase is financed as a jumbo loan.",
        "dscr_market": "Laguna Beach's art-colony tourism and ocean views drive premium long-term and vacation rents, giving DSCR investors a high income basis at elevated entry prices.",
    },
    {
        "city": "Laguna Niguel", "slug": "laguna-niguel", "county": "Orange County",
        "median": "approximately $1.5M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Laguna Niguel home values typically run above the 2026 Orange County conforming ceiling, so most single-family purchases in this south OC hillside city are financed as jumbo loans.",
        "dscr_market": "Laguna Niguel's master-planned neighborhoods and strong schools support steady upscale rental demand, a stable DSCR profile in south Orange County.",
    },
    {
        "city": "Aliso Viejo", "slug": "aliso-viejo", "county": "Orange County",
        "median": "approximately $1.01M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Aliso Viejo sits near the 2026 Orange County conforming ceiling, so jumbo financing often depends on the specific home — larger detached properties commonly exceed the limit while many condos fit conforming loans.",
        "dscr_market": "Aliso Viejo's young professional base and business parks generate steady rental demand, a balanced DSCR profile for south OC investors.",
    },
    {
        "city": "San Clemente", "slug": "san-clemente", "county": "Orange County",
        "median": "approximately $1.75M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Clemente home values typically run above the 2026 Orange County conforming ceiling, so most single-family purchases in this Spanish-village beach town require jumbo financing.",
        "dscr_market": "San Clemente's surf-town appeal and coastal tourism support strong long-term and vacation rents, giving DSCR investors a solid south-OC coastal income basis.",
    },
    {
        "city": "Dana Point", "slug": "dana-point", "county": "Orange County",
        "median": "approximately $1.76M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Dana Point home values typically run above the 2026 Orange County conforming ceiling, so most single-family purchases in this harbor town are financed as jumbo loans.",
        "dscr_market": "Dana Point's harbor, resorts, and beaches drive premium vacation and long-term rental demand, an attractive coastal DSCR market.",
    },
    {
        "city": "Yorba Linda", "slug": "yorba-linda", "county": "Orange County",
        "median": "approximately $1.42M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Yorba Linda's typical home value runs above the 2026 Orange County conforming ceiling, so most single-family purchases in this affluent north OC city are financed as jumbo loans.",
        "dscr_market": "Yorba Linda's top schools and spacious neighborhoods support steady upscale family-rental demand, a stable profile for DSCR investors.",
    },
    {
        "city": "Brea", "slug": "brea", "county": "Orange County",
        "median": "approximately $1.14M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Brea sits near the 2026 Orange County conforming ceiling, so jumbo financing often depends on the specific home — larger hillside properties commonly exceed the limit.",
        "dscr_market": "Brea's downtown, retail employment, and family neighborhoods sustain reliable rental demand, a practical DSCR profile in north Orange County.",
    },
    {
        "city": "Fountain Valley", "slug": "fountain-valley", "county": "Orange County",
        "median": "approximately $1.4M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Fountain Valley sits near the 2026 Orange County conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home and down payment.",
        "dscr_market": "Fountain Valley's central location and family-oriented neighborhoods produce steady rental demand, a dependable DSCR profile.",
    },
    {
        "city": "Westminster", "slug": "westminster", "county": "Orange County",
        "median": "approximately $1.1M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Westminster purchases fall near or below the 2026 Orange County conforming ceiling, so jumbo financing here generally applies to larger homes.",
        "dscr_market": "Westminster's Little Saigon commercial hub and central OC location support steady rental demand at relatively accessible prices for DSCR investors.",
    },
    {
        "city": "Lake Forest", "slug": "lake-forest", "county": "Orange County",
        "median": "approximately $1.2M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Lake Forest sits near the 2026 Orange County conforming ceiling, so jumbo financing often depends on the specific home — larger and newer master-planned homes frequently exceed the limit.",
        "dscr_market": "Lake Forest's family neighborhoods, schools, and central south-OC location support steady rental demand, a balanced DSCR profile.",
    },
    {
        "city": "Rancho Santa Margarita", "slug": "rancho-santa-margarita", "county": "Orange County",
        "median": "approximately $1.02M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Rancho Santa Margarita sits near the 2026 Orange County conforming ceiling, so jumbo financing often hinges on the specific home — larger detached properties commonly exceed the limit.",
        "dscr_market": "Rancho Santa Margarita's master-planned community and family demand support reliable long-term rental occupancy, a steady DSCR profile.",
    },

    # ===================== Ventura County (added) =====================
    {
        "city": "Oxnard", "slug": "oxnard", "county": "Ventura County",
        "median": "approximately $770K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Oxnard purchases fall below the 2026 Ventura County conforming ceiling, so jumbo loans here typically apply to larger or coastal Harbor-area homes rather than the typical purchase.",
        "dscr_market": "Oxnard's agricultural and port economy, plus relatively accessible prices, support steady workforce rental demand, a favorable DSCR cash-flow profile for Ventura County.",
    },
    {
        "city": "Ventura", "slug": "ventura", "county": "Ventura County",
        "median": "approximately $900K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Ventura purchases fall below the 2026 Ventura County conforming ceiling, so jumbo financing here generally applies to larger hillside or beachfront homes rather than the typical purchase.",
        "dscr_market": "The City of San Buenaventura's beach-town appeal and steady coastal rental demand make it a balanced DSCR market with both long-term and seasonal tenants.",
    },
    {
        "city": "Thousand Oaks", "slug": "thousand-oaks", "county": "Ventura County",
        "median": "approximately $1.05M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Thousand Oaks home values run above the 2026 Ventura County conforming ceiling, so a large share of single-family purchases in this affluent Conejo Valley city are financed as jumbo loans.",
        "dscr_market": "Thousand Oaks' top schools, corporate employers, and safe-suburb reputation support strong, stable rental demand, an attractive DSCR profile.",
    },
    {
        "city": "Simi Valley", "slug": "simi-valley", "county": "Ventura County",
        "median": "approximately $840K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Simi Valley purchases fall below the 2026 Ventura County conforming ceiling, so jumbo loans here typically apply to larger or newer homes rather than the typical purchase.",
        "dscr_market": "Simi Valley's family neighborhoods, low crime, and commuter access to the Valley sustain reliable rental demand, a dependable DSCR profile.",
    },
    {
        "city": "Camarillo", "slug": "camarillo", "county": "Ventura County",
        "median": "approximately $920K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Camarillo purchases fall below the 2026 Ventura County conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Camarillo's mild climate, business parks, and family neighborhoods support steady rental demand, a balanced DSCR profile in Ventura County.",
    },
    {
        "city": "Westlake Village", "slug": "westlake-village", "county": "Ventura County",
        "median": "approximately $1.61M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Westlake Village home values run above the 2026 Ventura County conforming ceiling, so most single-family purchases in this affluent lakeside community are financed as jumbo loans.",
        "dscr_market": "Westlake Village's upscale neighborhoods, top schools, and corporate base support premium rental demand, a strong income basis for DSCR investors.",
    },
    {
        "city": "Moorpark", "slug": "moorpark", "county": "Ventura County",
        "median": "approximately $940K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Moorpark purchases fall below the 2026 Ventura County conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Moorpark's family-oriented suburbs and strong schools support steady long-term rental demand, a dependable DSCR profile.",
    },
    {
        "city": "Ojai", "slug": "ojai", "county": "Ventura County",
        "median": "approximately $1.17M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Ojai home values run above the 2026 Ventura County conforming ceiling, so a large share of single-family purchases in this scenic valley town are financed as jumbo loans.",
        "dscr_market": "Ojai's wellness-and-arts tourism and limited housing supply support premium long-term and vacation rents, an attractive DSCR niche market.",
    },

    # ===================== Santa Barbara County (added) =====================
    {
        "city": "Santa Barbara", "slug": "santa-barbara", "county": "Santa Barbara County",
        "median": "approximately $1.83M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Santa Barbara home values run well above the 2026 Santa Barbara County conforming ceiling, so most single-family purchases in this coastal city are financed as jumbo loans.",
        "dscr_market": "Santa Barbara's tourism, university, and limited coastal supply drive strong long-term and vacation rental demand, a premium DSCR income basis.",
    },
    {
        "city": "Santa Maria", "slug": "santa-maria", "county": "Santa Barbara County",
        "median": "approximately $670K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Santa Maria purchases fall well below the 2026 Santa Barbara County conforming ceiling, so jumbo financing is rarely needed here outside of unusually large homes.",
        "dscr_market": "Santa Maria's agricultural and wine-country economy and affordable prices support steady workforce rental demand, one of the county's stronger DSCR cash-flow markets.",
    },
    {
        "city": "Goleta", "slug": "goleta", "county": "Santa Barbara County",
        "median": "approximately $1.37M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Goleta home values run above the 2026 Santa Barbara County conforming ceiling, so most single-family purchases near UCSB and the tech corridor are financed as jumbo loans.",
        "dscr_market": "Goleta's university population and tech employers anchor deep, year-round rental demand, a reliable DSCR profile on the South Coast.",
    },
    {
        "city": "Montecito", "slug": "montecito", "county": "Santa Barbara County",
        "median": "approximately $5.62M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Montecito is one of California's most exclusive markets, with typical values many times the 2026 Santa Barbara County conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Montecito's celebrity-tier estates command premium long-term and luxury seasonal rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Carpinteria", "slug": "carpinteria", "county": "Santa Barbara County",
        "median": "approximately $1.53M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Carpinteria home values run above the 2026 Santa Barbara County conforming ceiling, so most single-family purchases in this small beach town are financed as jumbo loans.",
        "dscr_market": "Carpinteria's beach-town appeal and limited supply support strong long-term and vacation rents, an attractive South Coast DSCR niche.",
    },

    # ===================== Kern County (added) =====================
    {
        "city": "Bakersfield", "slug": "bakersfield", "county": "Kern County",
        "median": "approximately $390K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Bakersfield purchases fall far below the 2026 Kern County conforming ceiling, so jumbo financing is rarely needed here and applies only to unusually large or custom homes.",
        "dscr_market": "Bakersfield's low prices and steady energy-and-agriculture employment produce some of California's most favorable rent-to-price ratios, a top market for DSCR cash flow.",
    },
    {
        "city": "Tehachapi", "slug": "tehachapi", "county": "Kern County",
        "median": "approximately $430K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Tehachapi purchases fall well below the 2026 Kern County conforming ceiling, so jumbo loans are seldom required here outside of larger mountain or ranch properties.",
        "dscr_market": "Tehachapi's mountain-town appeal and affordable prices support steady rental demand, a favorable DSCR cash-flow profile in eastern Kern County.",
    },

    # ===================== San Bernardino County (added) =====================
    {
        "city": "San Bernardino", "slug": "san-bernardino", "county": "San Bernardino County",
        "median": "approximately $500K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard San Bernardino purchases fall far below the 2026 San Bernardino County conforming ceiling, so jumbo financing is rarely needed here outside of unusually large homes.",
        "dscr_market": "San Bernardino's affordable prices and Inland Empire logistics-driven employment support strong workforce rental demand, a top DSCR cash-flow market.",
    },
    {
        "city": "Rancho Cucamonga", "slug": "rancho-cucamonga", "county": "San Bernardino County",
        "median": "approximately $790K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Rancho Cucamonga purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo loans here typically apply to larger or north-end foothill homes rather than the typical purchase.",
        "dscr_market": "Rancho Cucamonga's strong schools, retail hubs, and family neighborhoods sustain reliable rental demand, a dependable Inland Empire DSCR profile.",
    },
    {
        "city": "Ontario", "slug": "ontario", "county": "San Bernardino County",
        "median": "approximately $670K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Ontario purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo financing here generally applies to larger or new Ontario Ranch homes.",
        "dscr_market": "Ontario's airport, logistics economy, and new housing growth drive steady rental demand, a favorable Inland Empire DSCR cash-flow market.",
    },
    {
        "city": "Fontana", "slug": "fontana", "county": "San Bernardino County",
        "median": "approximately $640K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Fontana purchases fall well below the 2026 San Bernardino County conforming ceiling, so jumbo loans are seldom needed here outside of larger custom homes.",
        "dscr_market": "Fontana's logistics-and-warehouse employment base and affordable family housing support strong workforce rental demand, a solid DSCR cash-flow profile.",
    },
    {
        "city": "Rialto", "slug": "rialto", "county": "San Bernardino County",
        "median": "approximately $590K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Rialto purchases fall far below the 2026 San Bernardino County conforming ceiling, so jumbo financing is rarely needed here.",
        "dscr_market": "Rialto's central Inland Empire location and logistics jobs support steady, affordable workforce rental demand, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Redlands", "slug": "redlands", "county": "San Bernardino County",
        "median": "approximately $640K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Redlands purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo loans here typically apply to larger historic or hillside homes.",
        "dscr_market": "Redlands' university, historic downtown, and family neighborhoods support steady rental demand, a balanced Inland Empire DSCR profile.",
    },
    {
        "city": "Chino", "slug": "chino", "county": "San Bernardino County",
        "median": "approximately $760K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Chino purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo financing here generally applies to larger or new Preserve-area homes.",
        "dscr_market": "Chino's new master-planned housing and logistics employment support steady rental demand, a growing Inland Empire DSCR market.",
    },
    {
        "city": "Chino Hills", "slug": "chino-hills", "county": "San Bernardino County",
        "median": "approximately $990K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Chino Hills purchases fall below the 2026 San Bernardino County conforming ceiling, but its larger hillside homes frequently push past it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "Chino Hills' top schools and affluent suburban neighborhoods support strong, stable rental demand, a premium Inland Empire DSCR profile.",
    },
    {
        "city": "Upland", "slug": "upland", "county": "San Bernardino County",
        "median": "approximately $820K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Upland purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo loans here typically apply to larger north-end foothill homes.",
        "dscr_market": "Upland's established neighborhoods and foothill location support steady rental demand, a dependable Inland Empire DSCR profile.",
    },
    {
        "city": "Victorville", "slug": "victorville", "county": "San Bernardino County",
        "median": "approximately $440K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Victorville purchases fall far below the 2026 San Bernardino County conforming ceiling, so jumbo financing is rarely needed in this High Desert city.",
        "dscr_market": "Victorville's low High Desert prices and steady rental demand give DSCR investors some of the most favorable cash-flow math in the Inland Empire.",
    },
    {
        "city": "Hesperia", "slug": "hesperia", "county": "San Bernardino County",
        "median": "approximately $460K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Hesperia purchases fall far below the 2026 San Bernardino County conforming ceiling, so jumbo loans are seldom required in this High Desert city.",
        "dscr_market": "Hesperia's affordable High Desert housing and consistent rental demand support strong rent-to-price ratios, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Yucaipa", "slug": "yucaipa", "county": "San Bernardino County",
        "median": "approximately $570K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Yucaipa purchases fall below the 2026 San Bernardino County conforming ceiling, so jumbo financing here generally applies to larger foothill homes.",
        "dscr_market": "Yucaipa's small-town appeal and foothill setting support steady rental demand at accessible prices, a balanced DSCR profile.",
    },

    # ===================== Riverside County (added) =====================
    {
        "city": "Riverside", "slug": "riverside", "county": "Riverside County",
        "median": "approximately $650K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Riverside purchases fall below the 2026 Riverside County conforming ceiling, so jumbo financing here generally applies to larger or historic-district homes rather than the typical purchase.",
        "dscr_market": "Riverside's university, county-seat employment, and Inland Empire logistics base support steady rental demand, a dependable DSCR cash-flow market.",
    },
    {
        "city": "Corona", "slug": "corona", "county": "Riverside County",
        "median": "approximately $760K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Corona purchases fall below the 2026 Riverside County conforming ceiling, so jumbo loans here typically apply to larger or hillside homes.",
        "dscr_market": "Corona's commuter access to OC and family neighborhoods support steady rental demand, a balanced Inland Empire DSCR profile.",
    },
    {
        "city": "Moreno Valley", "slug": "moreno-valley", "county": "Riverside County",
        "median": "approximately $550K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Moreno Valley purchases fall far below the 2026 Riverside County conforming ceiling, so jumbo financing is rarely needed here.",
        "dscr_market": "Moreno Valley's logistics-driven employment and affordable housing support strong workforce rental demand, one of the Inland Empire's stronger DSCR cash-flow markets.",
    },
    {
        "city": "Temecula", "slug": "temecula", "county": "Riverside County",
        "median": "approximately $770K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Temecula purchases fall below the 2026 Riverside County conforming ceiling, so jumbo loans here typically apply to larger wine-country and custom estate homes.",
        "dscr_market": "Temecula's wine-country tourism, strong schools, and family growth support both long-term and vacation rental demand, an appealing south Riverside DSCR market.",
    },
    {
        "city": "Murrieta", "slug": "murrieta", "county": "Riverside County",
        "median": "approximately $690K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Murrieta purchases fall below the 2026 Riverside County conforming ceiling, so jumbo financing here generally applies to larger or custom homes.",
        "dscr_market": "Murrieta's family-oriented master-planned neighborhoods and strong schools support steady long-term rental demand, a dependable south Riverside DSCR profile.",
    },
    {
        "city": "Menifee", "slug": "menifee", "county": "Riverside County",
        "median": "approximately $590K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Menifee purchases fall well below the 2026 Riverside County conforming ceiling, so jumbo loans are seldom needed in this fast-growing city.",
        "dscr_market": "Menifee's rapid new-home growth and affordable prices support steady rental demand, a favorable DSCR cash-flow profile in south Riverside County.",
    },
    {
        "city": "Hemet", "slug": "hemet", "county": "Riverside County",
        "median": "approximately $450K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Hemet purchases fall far below the 2026 Riverside County conforming ceiling, so jumbo financing is rarely needed in this affordable San Jacinto Valley city.",
        "dscr_market": "Hemet's low prices and consistent rental demand give DSCR investors some of the most favorable rent-to-price math in Riverside County.",
    },
    {
        "city": "Eastvale", "slug": "eastvale", "county": "Riverside County",
        "median": "approximately $950K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Eastvale sits near the 2026 Riverside County conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger newer homes frequently exceed the limit.",
        "dscr_market": "Eastvale's newer master-planned housing, strong schools, and OC-commuter appeal support steady family-rental demand, a stable Inland Empire DSCR profile.",
    },
    {
        "city": "Jurupa Valley", "slug": "jurupa-valley", "county": "Riverside County",
        "median": "approximately $680K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Jurupa Valley purchases fall below the 2026 Riverside County conforming ceiling, so jumbo financing here generally applies to larger homes.",
        "dscr_market": "Jurupa Valley's central Inland Empire location and affordable housing support steady workforce rental demand, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Palm Springs", "slug": "palm-springs", "county": "Riverside County",
        "median": "approximately $620K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Palm Springs purchases fall below the 2026 Riverside County conforming ceiling, so jumbo loans here typically apply to larger mid-century and luxury desert estates.",
        "dscr_market": "Palm Springs' resort tourism and strong vacation-rental market give DSCR investors a distinctive short-term-rental income angle, subject to local rules.",
    },
    {
        "city": "Palm Desert", "slug": "palm-desert", "county": "Riverside County",
        "median": "approximately $550K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Palm Desert purchases fall below the 2026 Riverside County conforming ceiling, so jumbo financing here generally applies to larger or gated luxury desert homes.",
        "dscr_market": "Palm Desert's resort, retail, and seasonal-resident economy supports both long-term and vacation rental demand, a flexible Coachella Valley DSCR market.",
    },
    {
        "city": "La Quinta", "slug": "la-quinta", "county": "Riverside County",
        "median": "approximately $740K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard La Quinta purchases fall below the 2026 Riverside County conforming ceiling, but its larger golf-resort and gated estates frequently push past it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "La Quinta's golf-resort communities and seasonal tourism support premium vacation and long-term rents, an attractive Coachella Valley DSCR market.",
    },
    {
        "city": "Rancho Mirage", "slug": "rancho-mirage", "county": "Riverside County",
        "median": "approximately $840K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Many Rancho Mirage purchases push toward or above the 2026 Riverside County conforming ceiling, and its gated country-club estates frequently exceed it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "Rancho Mirage's upscale resort and country-club communities support premium long-term and seasonal rents, a high-end Coachella Valley DSCR market.",
    },
    {
        "city": "Indio", "slug": "indio", "county": "Riverside County",
        "median": "approximately $510K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Indio purchases fall well below the 2026 Riverside County conforming ceiling, so jumbo financing is seldom needed in this Coachella Valley city.",
        "dscr_market": "Indio's affordable prices and festival-driven tourism support both long-term and seasonal rental demand, a favorable Coachella Valley DSCR cash-flow market.",
    },

    # ===================== San Diego County (added) =====================
    {
        "city": "San Diego", "slug": "san-diego", "county": "San Diego County",
        "median": "approximately $1.0M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Diego's typical home value sits near the 2026 San Diego County conforming ceiling, and in its higher-priced coastal and central neighborhoods purchases routinely exceed it — those buyers turn to jumbo financing.",
        "dscr_market": "As a major coastal metro with military, biotech, and tourism employment, San Diego offers deep, diverse tenant demand, a broad and reliable DSCR market.",
    },
    {
        "city": "Oceanside", "slug": "oceanside", "county": "San Diego County",
        "median": "approximately $880K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Oceanside purchases fall below the 2026 San Diego County conforming ceiling, so jumbo loans here typically apply to larger or beachfront homes rather than the typical purchase.",
        "dscr_market": "Oceanside's beach lifestyle, military presence, and North County growth support strong long-term and vacation rental demand, an attractive coastal DSCR market.",
    },
    {
        "city": "Carlsbad", "slug": "carlsbad", "county": "San Diego County",
        "median": "approximately $1.39M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Carlsbad home values run above the 2026 San Diego County conforming ceiling, so most single-family purchases in this North County coastal city are financed as jumbo loans.",
        "dscr_market": "Carlsbad's beaches, biotech-and-resort employment, and top schools support premium rental demand, a strong North County DSCR income basis.",
    },
    {
        "city": "Vista", "slug": "vista", "county": "San Diego County",
        "median": "approximately $880K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Vista purchases fall below the 2026 San Diego County conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Vista's affordable-by-North-County prices and steady employment support reliable rental demand, a balanced San Diego County DSCR profile.",
    },
    {
        "city": "San Marcos", "slug": "san-marcos", "county": "San Diego County",
        "median": "approximately $960K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard San Marcos purchases fall below the 2026 San Diego County conforming ceiling, so jumbo loans here typically apply to larger or newer master-planned homes.",
        "dscr_market": "San Marcos' university presence and growing North County housing support steady, student-and-family rental demand, a dependable DSCR profile.",
    },
    {
        "city": "Escondido", "slug": "escondido", "county": "San Diego County",
        "median": "approximately $800K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Escondido purchases fall below the 2026 San Diego County conforming ceiling, so jumbo financing here generally applies to larger or hillside homes.",
        "dscr_market": "Escondido's inland-North-County affordability and steady demand support favorable rent-to-price ratios, a solid San Diego County DSCR cash-flow market.",
    },
    {
        "city": "Encinitas", "slug": "encinitas", "county": "San Diego County",
        "median": "approximately $1.94M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Encinitas home values run well above the 2026 San Diego County conforming ceiling, so most single-family purchases in this coastal North County city are financed as jumbo loans.",
        "dscr_market": "Encinitas' surf-town appeal, beaches, and limited supply support premium long-term and vacation rents, a high-end coastal DSCR market.",
    },
    {
        "city": "Del Mar", "slug": "del-mar", "county": "San Diego County",
        "median": "approximately $3.83M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Del Mar is among San Diego County's most expensive coastal markets, with typical values far above the 2026 conforming ceiling — virtually every standard purchase is financed as a jumbo loan.",
        "dscr_market": "Del Mar's oceanfront cachet and racetrack-season tourism command premium long-term and seasonal rents, giving DSCR investors a high coastal income basis.",
    },

    # =====================================================================
    # ============================ WAVE 2 =================================
    # =====================================================================

    # ===================== San Diego County (wave 2) =====================
    {
        "city": "Chula Vista", "slug": "chula-vista", "county": "San Diego County",
        "median": "approximately $850K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Chula Vista purchases fall below the 2026 San Diego County conforming ceiling, so jumbo loans here typically apply to larger or newer eastern master-planned homes rather than the typical purchase.",
        "dscr_market": "Chula Vista's fast-growing South Bay neighborhoods, family demand, and proximity to the border economy support steady rental demand, a dependable San Diego County DSCR profile.",
    },
    {
        "city": "El Cajon", "slug": "el-cajon", "county": "San Diego County",
        "median": "approximately $820K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard El Cajon purchases fall below the 2026 San Diego County conforming ceiling, so jumbo financing here generally applies to larger or hillside homes rather than the typical purchase.",
        "dscr_market": "El Cajon's inland-East-County affordability and steady demand support favorable rent-to-price ratios, a solid San Diego County DSCR cash-flow market.",
    },
    {
        "city": "La Mesa", "slug": "la-mesa", "county": "San Diego County",
        "median": "approximately $900K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard La Mesa purchases fall below the 2026 San Diego County conforming ceiling, so jumbo loans here typically apply to larger or view homes rather than the typical purchase.",
        "dscr_market": "La Mesa's walkable village, central East-County location, and steady demand support reliable rental occupancy, a balanced San Diego County DSCR profile.",
    },
    {
        "city": "Santee", "slug": "santee", "county": "San Diego County",
        "median": "approximately $800K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Santee purchases fall below the 2026 San Diego County conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Santee's family neighborhoods and relatively accessible East-County prices support steady rental demand, a practical San Diego County DSCR profile.",
    },
    {
        "city": "Poway", "slug": "poway", "county": "San Diego County",
        "median": "approximately $1.23M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Poway home values run above the 2026 San Diego County conforming ceiling, so most single-family purchases in this inland-North-County city are financed as jumbo loans.",
        "dscr_market": "Poway's top-rated schools and spacious neighborhoods support strong family-rental demand, a stable San Diego County DSCR profile.",
    },
    {
        "city": "National City", "slug": "national-city", "county": "San Diego County",
        "median": "approximately $690K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard National City purchases fall below the 2026 San Diego County conforming ceiling, so jumbo financing is rarely needed in this compact South Bay city.",
        "dscr_market": "National City's central South Bay location, port-adjacent employment, and accessible prices support steady workforce rental demand, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Coronado", "slug": "coronado", "county": "San Diego County",
        "median": "approximately $2.59M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Coronado is among San Diego County's most expensive markets, with typical values far above the 2026 conforming ceiling — virtually every standard purchase here is financed as a jumbo loan.",
        "dscr_market": "Coronado's island setting, resort tourism, and military presence drive premium long-term and seasonal rents, giving DSCR investors a high coastal income basis.",
    },
    {
        "city": "Imperial Beach", "slug": "imperial-beach", "county": "San Diego County",
        "median": "approximately $860K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Imperial Beach purchases fall below the 2026 San Diego County conforming ceiling, so jumbo loans here typically apply to larger or beachfront homes rather than the typical purchase.",
        "dscr_market": "Imperial Beach's relaxed beach-town appeal and southernmost-coastal location support steady long-term and vacation rental demand, an approachable coastal DSCR market.",
    },
    {
        "city": "Rancho Santa Fe", "slug": "rancho-santa-fe", "county": "San Diego County",
        "median": "approximately $4.44M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Rancho Santa Fe is one of California's most exclusive markets, with typical values many times the 2026 San Diego County conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Rancho Santa Fe's gated estates and acreage command premium long-term rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Solana Beach", "slug": "solana-beach", "county": "San Diego County",
        "median": "approximately $2.26M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Solana Beach home values run well above the 2026 San Diego County conforming ceiling, so nearly every standard purchase in this coastal North County city is financed as a jumbo loan.",
        "dscr_market": "Solana Beach's beaches, train access, and affluent coastal demand support premium long-term and vacation rents, a high-end North County DSCR market.",
    },

    # ===================== Imperial County (wave 2) =====================
    {
        "city": "El Centro", "slug": "el-centro", "county": "Imperial County",
        "median": "approximately $390K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard El Centro purchases fall far below the 2026 Imperial County conforming ceiling, so jumbo financing is rarely needed in this affordable border-region city.",
        "dscr_market": "El Centro's low prices and steady agricultural-and-government employment produce some of California's most favorable rent-to-price ratios, a strong DSCR cash-flow market.",
    },
    {
        "city": "Calexico", "slug": "calexico", "county": "Imperial County",
        "median": "approximately $390K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Calexico purchases fall far below the 2026 Imperial County conforming ceiling, so jumbo loans are seldom required in this affordable border city.",
        "dscr_market": "Calexico's cross-border commerce and low housing costs support steady workforce rental demand, a favorable DSCR cash-flow profile in Imperial County.",
    },
    {
        "city": "Brawley", "slug": "brawley", "county": "Imperial County",
        "median": "approximately $360K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Brawley purchases fall far below the 2026 Imperial County conforming ceiling, so jumbo financing is rarely needed in this agricultural valley city.",
        "dscr_market": "Brawley's agricultural economy and affordable housing support consistent rental demand, giving DSCR investors strong rent-to-price math in Imperial County.",
    },
    {
        "city": "Imperial", "slug": "imperial", "county": "Imperial County",
        "median": "approximately $440K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard purchases in the City of Imperial fall far below the 2026 Imperial County conforming ceiling, so jumbo loans are seldom needed outside of unusually large custom homes.",
        "dscr_market": "The City of Imperial's newer housing and affordable prices support steady rental demand, a favorable DSCR cash-flow profile in the Imperial Valley.",
    },

    # ===================== San Francisco County (wave 2) =====================
    {
        "city": "San Francisco", "slug": "san-francisco", "county": "San Francisco County",
        "median": "approximately $1.4M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Francisco home values run above the 2026 high-cost conforming ceiling, so the large majority of single-family and many condo purchases in the city are financed as jumbo loans.",
        "dscr_market": "As a dense, high-rent global tech hub, San Francisco offers deep tenant demand, giving DSCR investors a strong income basis even as elevated purchase prices keep coverage ratios in focus.",
    },

    # ===================== San Mateo County (wave 2) =====================
    {
        "city": "San Mateo", "slug": "san-mateo", "county": "San Mateo County",
        "median": "approximately $1.68M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Mateo home values run well above the 2026 high-cost conforming ceiling, so nearly every standard single-family purchase on the mid-Peninsula is financed as a jumbo loan.",
        "dscr_market": "San Mateo's central Peninsula location and tech-and-biotech employment keep rental demand strong, a reliable Bay Area DSCR market.",
    },
    {
        "city": "Redwood City", "slug": "redwood-city", "county": "San Mateo County",
        "median": "approximately $1.88M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Redwood City home values run well above the 2026 high-cost conforming ceiling, so virtually all standard single-family purchases here are financed as jumbo loans.",
        "dscr_market": "Redwood City's downtown growth and tech-employer base drive consistent rental demand, a strong Peninsula DSCR income basis.",
    },
    {
        "city": "Daly City", "slug": "daly-city", "county": "San Mateo County",
        "median": "approximately $1.13M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Daly City home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this San Francisco-adjacent city are financed as jumbo loans.",
        "dscr_market": "Daly City's proximity to San Francisco and dense housing support steady rental demand, an accessible-by-Peninsula-standards DSCR market.",
    },
    {
        "city": "South San Francisco", "slug": "south-san-francisco", "county": "San Mateo County",
        "median": "approximately $1.23M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "South San Francisco home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in 'The Industrial City' are financed as jumbo loans.",
        "dscr_market": "South San Francisco's biotech employment hub and airport-adjacent location anchor strong professional rental demand, a dependable Peninsula DSCR profile.",
    },
    {
        "city": "Burlingame", "slug": "burlingame", "county": "San Mateo County",
        "median": "approximately $2.82M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Burlingame is an affluent Peninsula market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Burlingame's tree-lined neighborhoods, top schools, and central Peninsula location support premium rental demand, a strong DSCR income basis.",
    },
    {
        "city": "Menlo Park", "slug": "menlo-park", "county": "San Mateo County",
        "median": "approximately $2.88M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Menlo Park is a premier Peninsula market where typical values run far above the 2026 high-cost conforming ceiling — nearly all standard purchases are financed as jumbo loans.",
        "dscr_market": "Menlo Park's headquarters-tech employment and acclaimed schools sustain premium, high-end rental demand, a top-tier Peninsula DSCR income basis.",
    },
    {
        "city": "Foster City", "slug": "foster-city", "county": "San Mateo County",
        "median": "approximately $1.88M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Foster City home values run well above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this waterfront planned community is a jumbo loan.",
        "dscr_market": "Foster City's lagoon lifestyle, top schools, and biotech employers support strong rental demand, a stable Peninsula DSCR profile.",
    },
    {
        "city": "San Carlos", "slug": "san-carlos", "county": "San Mateo County",
        "median": "approximately $2.45M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Carlos is an affluent Peninsula market where typical values run far above the 2026 high-cost conforming ceiling — nearly every standard purchase is a jumbo loan.",
        "dscr_market": "San Carlos' 'City of Good Living' reputation, top schools, and central Peninsula location support premium rental demand, a strong DSCR income basis.",
    },
    {
        "city": "Belmont", "slug": "belmont", "county": "San Mateo County",
        "median": "approximately $2.29M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Belmont home values run far above the 2026 high-cost conforming ceiling, so virtually every standard hillside purchase here is financed as a jumbo loan.",
        "dscr_market": "Belmont's wooded hillsides, top schools, and mid-Peninsula tech access support strong rental demand, a stable DSCR profile.",
    },
    {
        "city": "Millbrae", "slug": "millbrae", "county": "San Mateo County",
        "median": "approximately $2.07M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Millbrae home values run well above the 2026 high-cost conforming ceiling, so nearly every standard purchase in this transit-hub city is a jumbo loan.",
        "dscr_market": "Millbrae's BART-and-Caltrain transit hub and airport proximity support steady rental demand, a well-connected Peninsula DSCR market.",
    },
    {
        "city": "Pacifica", "slug": "pacifica", "county": "San Mateo County",
        "median": "approximately $1.27M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Pacifica home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this coastal city are financed as jumbo loans.",
        "dscr_market": "Pacifica's coastal setting and San Francisco commuter access support steady long-term rental demand, a scenic Peninsula DSCR market.",
    },
    {
        "city": "Half Moon Bay", "slug": "half-moon-bay", "county": "San Mateo County",
        "median": "approximately $1.56M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Half Moon Bay home values run well above the 2026 high-cost conforming ceiling, so most single-family purchases in this coastal town are financed as jumbo loans.",
        "dscr_market": "Half Moon Bay's coastal tourism and limited supply support premium long-term and vacation rents, an attractive coastal DSCR niche.",
    },

    # ===================== Santa Clara County (wave 2) =====================
    {
        "city": "San Jose", "slug": "san-jose", "county": "Santa Clara County",
        "median": "approximately $1.41M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Jose home values run above the 2026 high-cost conforming ceiling, so the majority of single-family purchases in the Bay Area's largest city are financed as jumbo loans.",
        "dscr_market": "As the capital of Silicon Valley, San Jose offers deep, high-rent tenant demand across neighborhoods, a broad and reliable DSCR market.",
    },
    {
        "city": "Santa Clara", "slug": "santa-clara", "county": "Santa Clara County",
        "median": "approximately $1.71M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Santa Clara home values run well above the 2026 high-cost conforming ceiling, so nearly every standard single-family purchase here is financed as a jumbo loan.",
        "dscr_market": "Santa Clara's concentration of major tech employers and the university anchor strong, year-round rental demand, a dependable Silicon Valley DSCR profile.",
    },
    {
        "city": "Sunnyvale", "slug": "sunnyvale", "county": "Santa Clara County",
        "median": "approximately $2.08M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Sunnyvale home values run far above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this Silicon Valley city is a jumbo loan.",
        "dscr_market": "Sunnyvale's dense tech-employer base and top schools sustain premium rental demand, a strong Silicon Valley DSCR income basis.",
    },
    {
        "city": "Mountain View", "slug": "mountain-view", "county": "Santa Clara County",
        "median": "approximately $1.97M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Mountain View home values run far above the 2026 high-cost conforming ceiling, so nearly every standard single-family purchase here is financed as a jumbo loan.",
        "dscr_market": "Mountain View's headquarters-tech employment and walkable downtown drive strong rental demand, a premium Silicon Valley DSCR market.",
    },
    {
        "city": "Palo Alto", "slug": "palo-alto", "county": "Santa Clara County",
        "median": "approximately $3.6M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Palo Alto is one of the priciest markets in the country, with typical values many times the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Palo Alto's university and venture-tech economy command premium rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Cupertino", "slug": "cupertino", "county": "Santa Clara County",
        "median": "approximately $3.07M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Cupertino home values run far above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this top-schools tech city is a jumbo loan.",
        "dscr_market": "Cupertino's flagship-tech employment and acclaimed schools sustain premium rental demand, a top-tier Silicon Valley DSCR income basis.",
    },
    {
        "city": "Milpitas", "slug": "milpitas", "county": "Santa Clara County",
        "median": "approximately $1.45M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Milpitas home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this northern Silicon Valley city are financed as jumbo loans.",
        "dscr_market": "Milpitas' tech-and-logistics employment and transit access support steady rental demand, a dependable Silicon Valley DSCR profile.",
    },
    {
        "city": "Campbell", "slug": "campbell", "county": "Santa Clara County",
        "median": "approximately $1.9M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Campbell home values run well above the 2026 high-cost conforming ceiling, so nearly every standard single-family purchase in this central-valley city is a jumbo loan.",
        "dscr_market": "Campbell's lively downtown and central Silicon Valley location support strong rental demand, a desirable DSCR market.",
    },
    {
        "city": "Los Gatos", "slug": "los-gatos", "county": "Santa Clara County",
        "median": "approximately $2.66M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Los Gatos is an affluent foothill market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Los Gatos' top schools, charming downtown, and tech-executive demand sustain premium rents, a high-end Silicon Valley DSCR income basis.",
    },
    {
        "city": "Saratoga", "slug": "saratoga", "county": "Santa Clara County",
        "median": "approximately $4.09M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Saratoga is one of Silicon Valley's most exclusive markets, with typical values many times the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Saratoga's acclaimed schools and hillside estates command premium rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Los Altos", "slug": "los-altos", "county": "Santa Clara County",
        "median": "approximately $4.62M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Los Altos is among the priciest markets in the country, with typical values many times the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Los Altos' top schools and venture-tech wealth command premium rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Gilroy", "slug": "gilroy", "county": "Santa Clara County",
        "median": "approximately $1.07M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Gilroy sits near the 2026 high-cost conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger or newer homes frequently push past the limit.",
        "dscr_market": "Gilroy's relatively accessible south-county prices and agricultural-and-commuter economy support steady rental demand, a favorable Santa Clara County DSCR cash-flow market.",
    },
    {
        "city": "Morgan Hill", "slug": "morgan-hill", "county": "Santa Clara County",
        "median": "approximately $1.34M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Morgan Hill home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this south-county city are financed as jumbo loans.",
        "dscr_market": "Morgan Hill's family neighborhoods and growing south-Silicon-Valley demand support steady rental occupancy, a balanced DSCR profile.",
    },

    # ===================== Alameda County (wave 2) =====================
    {
        "city": "Oakland", "slug": "oakland", "county": "Alameda County",
        "median": "approximately $720K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Citywide, the typical Oakland home value sits below the 2026 high-cost conforming ceiling, but in its higher-priced hills neighborhoods purchases routinely exceed it — those buyers turn to jumbo financing.",
        "dscr_market": "As a major East Bay metro with diverse neighborhoods and transit access, Oakland offers deep tenant demand, a broad and active DSCR market.",
    },
    {
        "city": "Fremont", "slug": "fremont", "county": "Alameda County",
        "median": "approximately $1.5M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Fremont home values run above the 2026 high-cost conforming ceiling, so the majority of single-family purchases in this large East Bay city are financed as jumbo loans.",
        "dscr_market": "Fremont's tech-and-manufacturing employment and top schools sustain strong rental demand, a dependable East Bay DSCR profile.",
    },
    {
        "city": "Hayward", "slug": "hayward", "county": "Alameda County",
        "median": "approximately $840K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Hayward purchases fall below the 2026 high-cost conforming ceiling, so jumbo loans here typically apply to larger or hillside homes rather than the typical purchase.",
        "dscr_market": "Hayward's central East Bay location, university, and transit access support steady rental demand at relatively accessible prices, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Berkeley", "slug": "berkeley", "county": "Alameda County",
        "median": "approximately $1.48M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Berkeley home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this university city are financed as jumbo loans.",
        "dscr_market": "Berkeley's large university population anchors deep, year-round rental demand, one of the East Bay's most reliable DSCR markets for occupancy.",
    },
    {
        "city": "Alameda", "slug": "alameda", "county": "Alameda County",
        "median": "approximately $1.16M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Alameda home values run above the 2026 high-cost conforming ceiling, so most single-family purchases on 'the Island' are financed as jumbo loans.",
        "dscr_market": "Alameda's island setting, historic homes, and ferry access to San Francisco support steady rental demand, a desirable East Bay DSCR market.",
    },
    {
        "city": "San Leandro", "slug": "san-leandro", "county": "Alameda County",
        "median": "approximately $820K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard San Leandro purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "San Leandro's central East Bay location, transit access, and accessible prices support steady rental demand, a practical DSCR cash-flow market.",
    },
    {
        "city": "Pleasanton", "slug": "pleasanton", "county": "Alameda County",
        "median": "approximately $1.56M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Pleasanton home values run well above the 2026 high-cost conforming ceiling, so nearly every standard single-family purchase in this affluent Tri-Valley city is a jumbo loan.",
        "dscr_market": "Pleasanton's top schools, corporate employers, and family neighborhoods sustain premium rental demand, a strong Tri-Valley DSCR profile.",
    },
    {
        "city": "Dublin", "slug": "dublin", "county": "Alameda County",
        "median": "approximately $1.27M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Dublin home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this fast-growing Tri-Valley city are financed as jumbo loans.",
        "dscr_market": "Dublin's new master-planned housing, top schools, and BART access support strong family-rental demand, a growing Tri-Valley DSCR market.",
    },
    {
        "city": "Livermore", "slug": "livermore", "county": "Alameda County",
        "median": "approximately $1.11M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Livermore sits near the 2026 high-cost conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger or newer homes frequently push past the limit.",
        "dscr_market": "Livermore's wine-country setting, lab employment, and family neighborhoods support steady rental demand, a balanced Tri-Valley DSCR profile.",
    },
    {
        "city": "Union City", "slug": "union-city", "county": "Alameda County",
        "median": "approximately $1.25M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Union City sits near the 2026 high-cost conforming ceiling, so jumbo financing often depends on the specific home — larger detached properties commonly exceed the limit.",
        "dscr_market": "Union City's central East Bay location and transit access support steady rental demand, a dependable DSCR profile.",
    },
    {
        "city": "Newark", "slug": "newark", "county": "Alameda County",
        "median": "approximately $1.23M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Newark sits near the 2026 high-cost conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home and down payment.",
        "dscr_market": "Newark's southern East Bay location and new housing growth support steady rental demand, a practical DSCR profile.",
    },
    {
        "city": "Castro Valley", "slug": "castro-valley", "county": "Alameda County",
        "median": "approximately $1.12M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Castro Valley sits near the 2026 high-cost conforming ceiling, so jumbo financing often depends on the specific home — larger hillside properties commonly exceed the limit.",
        "dscr_market": "Castro Valley's family neighborhoods, strong schools, and central East Bay location support steady rental demand, a balanced DSCR profile.",
    },

    # ===================== Contra Costa County (wave 2) =====================
    # NOTE: Contra Costa "Brentwood" intentionally OMITTED — slug collision with LA County Brentwood.
    {
        "city": "Concord", "slug": "concord", "county": "Contra Costa County",
        "median": "approximately $740K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Concord purchases fall below the 2026 high-cost conforming ceiling, so jumbo loans here typically apply to larger homes rather than the typical purchase.",
        "dscr_market": "Concord's central Contra Costa location, BART access, and accessible prices support steady rental demand, a favorable East Bay DSCR cash-flow market.",
    },
    {
        "city": "Richmond", "slug": "richmond", "county": "Contra Costa County",
        "median": "approximately $610K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Richmond purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing here generally applies to larger or waterfront homes.",
        "dscr_market": "Richmond's waterfront location, transit access, and relatively accessible prices support steady rental demand, a favorable West-County DSCR cash-flow market.",
    },
    {
        "city": "Walnut Creek", "slug": "walnut-creek", "county": "Contra Costa County",
        "median": "approximately $1.04M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Walnut Creek home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this central Contra Costa hub are financed as jumbo loans.",
        "dscr_market": "Walnut Creek's downtown, retail, and BART access sustain strong rental demand, a desirable East Bay DSCR market.",
    },
    {
        "city": "Antioch", "slug": "antioch", "county": "Contra Costa County",
        "median": "approximately $600K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Antioch purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing is rarely needed in this East-County city.",
        "dscr_market": "Antioch's affordable East-County prices and steady demand produce favorable rent-to-price ratios, a strong DSCR cash-flow market.",
    },
    {
        "city": "San Ramon", "slug": "san-ramon", "county": "Contra Costa County",
        "median": "approximately $1.5M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Ramon home values run well above the 2026 high-cost conforming ceiling, so nearly every standard purchase in this affluent Tri-Valley city is a jumbo loan.",
        "dscr_market": "San Ramon's corporate campuses, top schools, and master-planned neighborhoods sustain premium rental demand, a strong Tri-Valley DSCR profile.",
    },
    {
        "city": "Danville", "slug": "danville", "county": "Contra Costa County",
        "median": "approximately $1.88M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Danville is an affluent Tri-Valley market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Danville's top schools and upscale neighborhoods support premium rental demand, a high-end Tri-Valley DSCR income basis.",
    },
    {
        "city": "Pittsburg", "slug": "pittsburg", "county": "Contra Costa County",
        "median": "approximately $570K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Pittsburg purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing is rarely needed in this East-County city.",
        "dscr_market": "Pittsburg's waterfront, BART extension, and affordable prices support steady rental demand, a favorable East-County DSCR cash-flow market.",
    },
    {
        "city": "Martinez", "slug": "martinez", "county": "Contra Costa County",
        "median": "approximately $770K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Martinez purchases fall below the 2026 high-cost conforming ceiling, so jumbo loans here typically apply to larger or hillside homes.",
        "dscr_market": "Martinez's county-seat employment, historic downtown, and waterfront support steady rental demand, a balanced Contra Costa DSCR profile.",
    },
    {
        "city": "Pleasant Hill", "slug": "pleasant-hill", "county": "Contra Costa County",
        "median": "approximately $1.0M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Pleasant Hill sits near the 2026 high-cost conforming ceiling, so jumbo financing often depends on the specific home — larger properties commonly exceed the limit.",
        "dscr_market": "Pleasant Hill's central location, retail hubs, and family neighborhoods support steady rental demand, a dependable East Bay DSCR profile.",
    },
    {
        "city": "Lafayette", "slug": "lafayette", "county": "Contra Costa County",
        "median": "approximately $1.96M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Lafayette is an affluent Lamorinda market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Lafayette's top schools, semi-rural charm, and BART access sustain premium rental demand, a high-end East Bay DSCR income basis.",
    },
    {
        "city": "Orinda", "slug": "orinda", "county": "Contra Costa County",
        "median": "approximately $1.99M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Orinda is an affluent Lamorinda market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Orinda's acclaimed schools and wooded estates support premium rental demand, a high-end East Bay DSCR income basis.",
    },

    # ===================== Marin County (wave 2) =====================
    {
        "city": "San Rafael", "slug": "san-rafael", "county": "Marin County",
        "median": "approximately $1.34M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "San Rafael home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in Marin's county seat are financed as jumbo loans.",
        "dscr_market": "San Rafael's central Marin location, downtown, and transit access support steady rental demand, a dependable North Bay DSCR market.",
    },
    {
        "city": "Novato", "slug": "novato", "county": "Marin County",
        "median": "approximately $1.08M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Novato sits near the 2026 high-cost conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger homes frequently push past the limit.",
        "dscr_market": "Novato's relatively accessible North Marin prices and family neighborhoods support steady rental demand, a balanced Marin DSCR profile.",
    },
    {
        "city": "Mill Valley", "slug": "mill-valley", "county": "Marin County",
        "median": "approximately $2.17M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Mill Valley is an affluent Marin market where typical values run far above the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Mill Valley's wooded hillsides, top schools, and San Francisco proximity support premium rental demand, a high-end Marin DSCR income basis.",
    },
    {
        "city": "Sausalito", "slug": "sausalito", "county": "Marin County",
        "median": "approximately $1.56M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Sausalito home values run far above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this waterfront town is a jumbo loan.",
        "dscr_market": "Sausalito's bayfront views, tourism, and ferry access to San Francisco support premium long-term and vacation rents, a high-end Marin DSCR market.",
    },
    {
        "city": "Tiburon", "slug": "tiburon", "county": "Marin County",
        "median": "approximately $3.09M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Tiburon is one of Marin's most exclusive markets, with typical values many times the 2026 high-cost conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Tiburon's waterfront estates and bay views command premium rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },
    {
        "city": "Larkspur", "slug": "larkspur", "county": "Marin County",
        "median": "approximately $2.2M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Larkspur home values run far above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this central Marin town is a jumbo loan.",
        "dscr_market": "Larkspur's ferry terminal, downtown, and desirable neighborhoods support premium rental demand, a strong Marin DSCR income basis.",
    },
    {
        "city": "Corte Madera", "slug": "corte-madera", "county": "Marin County",
        "median": "approximately $1.87M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Corte Madera home values run far above the 2026 high-cost conforming ceiling, so virtually every standard purchase in this central Marin town is a jumbo loan.",
        "dscr_market": "Corte Madera's retail hubs, top schools, and central Marin location support premium rental demand, a stable Marin DSCR profile.",
    },

    # ===================== Sonoma County (wave 2) =====================
    {
        "city": "Santa Rosa", "slug": "santa-rosa", "county": "Sonoma County",
        "median": "approximately $720K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Santa Rosa purchases fall below the 2026 Sonoma County conforming ceiling, so jumbo loans here typically apply to larger or eastside homes rather than the typical purchase.",
        "dscr_market": "Santa Rosa's wine-country economy, county-seat employment, and steady demand support reliable rental occupancy, a balanced Sonoma County DSCR profile.",
    },
    {
        "city": "Petaluma", "slug": "petaluma", "county": "Sonoma County",
        "median": "approximately $910K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Petaluma purchases fall below the 2026 Sonoma County conforming ceiling, so jumbo financing here generally applies to larger or historic homes.",
        "dscr_market": "Petaluma's historic downtown, North Bay commuter appeal, and steady demand support reliable rental occupancy, a dependable Sonoma County DSCR profile.",
    },
    {
        "city": "Rohnert Park", "slug": "rohnert-park", "county": "Sonoma County",
        "median": "approximately $720K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Rohnert Park purchases fall below the 2026 Sonoma County conforming ceiling, so jumbo financing is rarely needed in this planned city.",
        "dscr_market": "Rohnert Park's university presence and relatively accessible prices support steady rental demand, a favorable Sonoma County DSCR cash-flow market.",
    },
    {
        "city": "Sonoma", "slug": "sonoma", "county": "Sonoma County",
        "median": "approximately $960K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "The City of Sonoma sits near the 2026 Sonoma County conforming ceiling, so whether a purchase needs a jumbo loan often depends on the specific home — larger wine-country homes frequently push past the limit.",
        "dscr_market": "The City of Sonoma's wine-country tourism and historic plaza support both long-term and vacation rental demand, an attractive North Bay DSCR market.",
    },
    {
        "city": "Healdsburg", "slug": "healdsburg", "county": "Sonoma County",
        "median": "approximately $1.12M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Healdsburg home values run above the 2026 Sonoma County conforming ceiling, so most single-family purchases in this wine-country town are financed as jumbo loans.",
        "dscr_market": "Healdsburg's premium wine-country tourism and limited supply support strong vacation and long-term rents, a high-end Sonoma County DSCR market.",
    },
    {
        "city": "Windsor", "slug": "windsor", "county": "Sonoma County",
        "median": "approximately $810K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Windsor purchases fall below the 2026 Sonoma County conforming ceiling, so jumbo financing is rarely needed in this town.",
        "dscr_market": "Windsor's family neighborhoods and wine-country setting support steady rental demand at accessible prices, a favorable Sonoma County DSCR profile.",
    },

    # ===================== Napa County (wave 2) =====================
    {
        "city": "Napa", "slug": "napa", "county": "Napa County",
        "median": "approximately $880K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Napa purchases fall below the 2026 Napa County conforming ceiling, so jumbo loans here typically apply to larger or wine-country estate homes rather than the typical purchase.",
        "dscr_market": "The City of Napa's world-renowned wine tourism supports strong vacation and long-term rental demand, a distinctive North Bay DSCR market.",
    },
    {
        "city": "American Canyon", "slug": "american-canyon", "county": "Napa County",
        "median": "approximately $740K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard American Canyon purchases fall below the 2026 Napa County conforming ceiling, so jumbo financing is rarely needed in this commuter-friendly city.",
        "dscr_market": "American Canyon's accessible prices and North Bay commuter appeal support steady rental demand, a favorable Napa County DSCR cash-flow market.",
    },
    {
        "city": "St. Helena", "slug": "st-helena", "county": "Napa County",
        "median": "approximately $1.68M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "St. Helena home values run well above the 2026 Napa County conforming ceiling, so virtually every standard purchase in this upvalley wine town is a jumbo loan.",
        "dscr_market": "St. Helena's premium wine-country tourism and limited supply support strong vacation and long-term rents, a high-end Napa County DSCR market.",
    },
    {
        "city": "Yountville", "slug": "yountville", "county": "Napa County",
        "median": "approximately $1.32M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Yountville home values run above the 2026 Napa County conforming ceiling, so most single-family purchases in this small wine-country town are financed as jumbo loans.",
        "dscr_market": "Yountville's culinary-tourism draw and limited supply support premium vacation and long-term rents, an attractive Napa County DSCR niche.",
    },

    # ===================== Solano County (wave 2) =====================
    {
        "city": "Vallejo", "slug": "vallejo", "county": "Solano County",
        "median": "approximately $530K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Vallejo purchases fall far below the 2026 Solano County conforming ceiling, so jumbo financing is rarely needed in this waterfront city.",
        "dscr_market": "Vallejo's affordable prices, ferry access to San Francisco, and steady demand produce favorable rent-to-price ratios, a strong North Bay DSCR cash-flow market.",
    },
    {
        "city": "Fairfield", "slug": "fairfield", "county": "Solano County",
        "median": "approximately $610K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Fairfield purchases fall well below the 2026 Solano County conforming ceiling, so jumbo loans are seldom needed in this midway-commuter city.",
        "dscr_market": "Fairfield's central Solano location between San Francisco and Sacramento supports steady rental demand at accessible prices, a favorable DSCR cash-flow market.",
    },
    {
        "city": "Vacaville", "slug": "vacaville", "county": "Solano County",
        "median": "approximately $610K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Vacaville purchases fall well below the 2026 Solano County conforming ceiling, so jumbo financing is rarely needed in this city.",
        "dscr_market": "Vacaville's family neighborhoods and midway-commuter location support steady rental demand, a dependable Solano County DSCR profile.",
    },
    {
        "city": "Benicia", "slug": "benicia", "county": "Solano County",
        "median": "approximately $800K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Benicia purchases fall below the 2026 Solano County conforming ceiling, so jumbo loans here typically apply to larger or waterfront homes.",
        "dscr_market": "Benicia's historic waterfront downtown and small-town appeal support steady rental demand, a balanced Solano County DSCR profile.",
    },
    {
        "city": "Suisun City", "slug": "suisun-city", "county": "Solano County",
        "median": "approximately $530K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Suisun City purchases fall far below the 2026 Solano County conforming ceiling, so jumbo financing is rarely needed in this waterfront city.",
        "dscr_market": "Suisun City's affordable prices and waterfront marina district support steady rental demand, a favorable Solano County DSCR cash-flow market.",
    },
    {
        "city": "Dixon", "slug": "dixon", "county": "Solano County",
        "median": "approximately $610K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Dixon purchases fall well below the 2026 Solano County conforming ceiling, so jumbo loans are seldom needed in this small agricultural city.",
        "dscr_market": "Dixon's agricultural roots, small-town appeal, and accessible prices support steady rental demand, a favorable Solano County DSCR cash-flow profile.",
    },

    # ===================== Santa Cruz County (wave 2) =====================
    {
        "city": "Santa Cruz", "slug": "santa-cruz", "county": "Santa Cruz County",
        "median": "approximately $1.37M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Santa Cruz home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this coastal university city are financed as jumbo loans.",
        "dscr_market": "Santa Cruz's beaches, university population, and tourism drive strong long-term and vacation rental demand, a premium Central Coast DSCR market.",
    },
    {
        "city": "Watsonville", "slug": "watsonville", "county": "Santa Cruz County",
        "median": "approximately $830K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Watsonville purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Watsonville's agricultural economy and relatively accessible prices support steady workforce rental demand, a favorable Santa Cruz County DSCR cash-flow market.",
    },
    {
        "city": "Scotts Valley", "slug": "scotts-valley", "county": "Santa Cruz County",
        "median": "approximately $1.27M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Scotts Valley home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this mountain-gateway city are financed as jumbo loans.",
        "dscr_market": "Scotts Valley's top schools and Silicon Valley commuter access support steady rental demand, a dependable Santa Cruz County DSCR profile.",
    },
    {
        "city": "Capitola", "slug": "capitola", "county": "Santa Cruz County",
        "median": "approximately $1.26M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Capitola home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this seaside village are financed as jumbo loans.",
        "dscr_market": "Capitola's beach-village charm and tourism support strong long-term and vacation rents, an attractive Central Coast DSCR niche.",
    },
    {
        "city": "Aptos", "slug": "aptos", "county": "Santa Cruz County",
        "median": "approximately $1.35M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Aptos home values run above the 2026 high-cost conforming ceiling, so most single-family purchases in this coastal community are financed as jumbo loans.",
        "dscr_market": "Aptos' beaches, redwoods, and desirable neighborhoods support steady long-term and vacation rental demand, a premium Santa Cruz County DSCR market.",
    },

    # ===================== San Benito County (wave 2) =====================
    {
        "city": "Hollister", "slug": "hollister", "county": "San Benito County",
        "median": "approximately $760K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Hollister purchases fall below the 2026 high-cost conforming ceiling, so jumbo financing here generally applies to larger homes rather than the typical purchase.",
        "dscr_market": "Hollister's relatively accessible prices and growing Silicon Valley commuter demand support steady rental occupancy, a favorable San Benito County DSCR cash-flow market.",
    },

    # ===================== Monterey County (wave 2) =====================
    {
        "city": "Monterey", "slug": "monterey", "county": "Monterey County",
        "median": "approximately $1.18M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Monterey home values run above the 2026 Monterey County conforming ceiling, so most single-family purchases in this coastal city are financed as jumbo loans.",
        "dscr_market": "The City of Monterey's tourism, aquarium, and coastal appeal drive strong long-term and vacation rental demand, a premium Central Coast DSCR market.",
    },
    {
        "city": "Salinas", "slug": "salinas", "county": "Monterey County",
        "median": "approximately $750K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Salinas purchases fall below the 2026 Monterey County conforming ceiling, so jumbo financing is rarely needed in this agricultural-valley city.",
        "dscr_market": "Salinas' 'Salad Bowl' agricultural economy and accessible prices support steady workforce rental demand, a favorable Monterey County DSCR cash-flow market.",
    },
    {
        "city": "Carmel-by-the-Sea", "slug": "carmel-by-the-sea", "county": "Monterey County",
        "median": "approximately $2.46M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Carmel-by-the-Sea is one of California's most exclusive coastal markets, with typical values many times the 2026 Monterey County conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Carmel-by-the-Sea's storybook charm and premium tourism command high vacation and long-term rents, giving DSCR investors a strong coastal income basis.",
    },
    {
        "city": "Pacific Grove", "slug": "pacific-grove", "county": "Monterey County",
        "median": "approximately $1.4M as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Pacific Grove home values run above the 2026 Monterey County conforming ceiling, so most single-family purchases in this coastal town are financed as jumbo loans.",
        "dscr_market": "Pacific Grove's Victorian charm and coastal tourism support strong long-term and vacation rents, an attractive Monterey Peninsula DSCR market.",
    },
    {
        "city": "Seaside", "slug": "seaside", "county": "Monterey County",
        "median": "approximately $810K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Seaside purchases fall below the 2026 Monterey County conforming ceiling, so jumbo financing here generally applies to larger or view homes rather than the typical purchase.",
        "dscr_market": "Seaside's relatively accessible Monterey Peninsula prices and university presence support steady rental demand, a favorable Monterey County DSCR cash-flow market.",
    },
    {
        "city": "Marina", "slug": "marina", "county": "Monterey County",
        "median": "approximately $870K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Marina purchases fall below the 2026 Monterey County conforming ceiling, so jumbo financing here generally applies to larger or newer homes rather than the typical purchase.",
        "dscr_market": "Marina's coastal location, new housing growth, and university presence support steady rental demand, a balanced Monterey County DSCR profile.",
    },
    {
        "city": "Pebble Beach", "slug": "pebble-beach", "county": "Monterey County",
        "median": "not tracked separately by Zillow",
        "jumbo_market": "Pebble Beach is one of California's most exclusive markets, with typical values many times the 2026 Monterey County conforming ceiling — virtually every standard purchase is a jumbo loan.",
        "dscr_market": "Pebble Beach's world-famous golf resorts and gated estates command premium rents, giving DSCR investors a high income basis at very elevated entry prices.",
    },

    # ===================== Sacramento County (wave 2) =====================
    {
        "city": "Sacramento", "slug": "sacramento", "county": "Sacramento County",
        "median": "approximately $480K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Sacramento purchases fall below the 2026 Sacramento County conforming ceiling, so jumbo financing here generally applies to larger or premium central-city homes rather than the typical purchase.",
        "dscr_market": "As the state capital with deep government, healthcare, and university employment, Sacramento offers broad tenant demand and favorable rent-to-price ratios, a strong DSCR market.",
    },
    {
        "city": "Elk Grove", "slug": "elk-grove", "county": "Sacramento County",
        "median": "approximately $640K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Elk Grove purchases fall below the 2026 Sacramento County conforming ceiling, so jumbo financing is rarely needed in this fast-growing suburb.",
        "dscr_market": "Elk Grove's family neighborhoods, strong schools, and new housing growth support steady rental demand, a dependable Sacramento-area DSCR profile.",
    },
    {
        "city": "Folsom", "slug": "folsom", "county": "Sacramento County",
        "median": "approximately $770K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Folsom purchases fall below the 2026 Sacramento County conforming ceiling, so jumbo loans here typically apply to larger or newer master-planned homes.",
        "dscr_market": "Folsom's top schools, tech employers, and lakeside appeal support steady upscale rental demand, a stable Sacramento-area DSCR profile.",
    },
    {
        "city": "Citrus Heights", "slug": "citrus-heights", "county": "Sacramento County",
        "median": "approximately $480K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Citrus Heights purchases fall far below the 2026 Sacramento County conforming ceiling, so jumbo financing is rarely needed in this suburb.",
        "dscr_market": "Citrus Heights' affordable suburban prices and steady demand produce favorable rent-to-price ratios, a strong Sacramento-area DSCR cash-flow market.",
    },
    {
        "city": "Rancho Cordova", "slug": "rancho-cordova", "county": "Sacramento County",
        "median": "approximately $540K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Rancho Cordova purchases fall below the 2026 Sacramento County conforming ceiling, so jumbo financing is rarely needed in this employment-rich suburb.",
        "dscr_market": "Rancho Cordova's business parks, new housing, and accessible prices support steady rental demand, a favorable Sacramento-area DSCR cash-flow market.",
    },

    # ===================== Placer County (wave 2) =====================
    {
        "city": "Roseville", "slug": "roseville", "county": "Placer County",
        "median": "approximately $650K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Roseville purchases fall below the 2026 Placer County conforming ceiling, so jumbo financing here generally applies to larger or newer master-planned homes.",
        "dscr_market": "Roseville's strong schools, retail hubs, and family neighborhoods support steady rental demand, a dependable Placer County DSCR profile.",
    },
    {
        "city": "Rocklin", "slug": "rocklin", "county": "Placer County",
        "median": "approximately $700K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Rocklin purchases fall below the 2026 Placer County conforming ceiling, so jumbo loans here typically apply to larger or newer homes.",
        "dscr_market": "Rocklin's top schools and family-oriented neighborhoods support steady rental demand, a stable Placer County DSCR profile.",
    },
    {
        "city": "Lincoln", "slug": "lincoln", "county": "Placer County",
        "median": "approximately $650K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Lincoln purchases fall below the 2026 Placer County conforming ceiling, so jumbo financing is rarely needed in this fast-growing city.",
        "dscr_market": "Lincoln's new master-planned and active-adult communities support steady rental demand, a favorable Placer County DSCR cash-flow market.",
    },
    {
        "city": "Auburn", "slug": "auburn", "county": "Placer County",
        "median": "approximately $640K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Auburn purchases fall below the 2026 Placer County conforming ceiling, so jumbo financing here generally applies to larger foothill homes.",
        "dscr_market": "Auburn's historic Gold Country charm and foothill setting support steady rental demand, a balanced Placer County DSCR profile.",
    },

    # ===================== El Dorado County (wave 2) =====================
    {
        "city": "El Dorado Hills", "slug": "el-dorado-hills", "county": "El Dorado County",
        "median": "approximately $920K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard El Dorado Hills purchases fall below the 2026 El Dorado County conforming ceiling, but its larger gated and view homes frequently push past it — those purchases are commonly financed as jumbo loans.",
        "dscr_market": "El Dorado Hills' top schools and affluent master-planned neighborhoods support strong upscale rental demand, a premium Sacramento-area DSCR profile.",
    },
    {
        "city": "Placerville", "slug": "placerville", "county": "El Dorado County",
        "median": "approximately $540K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Placerville purchases fall far below the 2026 El Dorado County conforming ceiling, so jumbo financing is rarely needed in this Gold Country town.",
        "dscr_market": "Placerville's historic Gold Country appeal and foothill setting support steady rental demand at accessible prices, a favorable El Dorado County DSCR cash-flow market.",
    },

    # ===================== Yolo County (wave 2) =====================
    {
        "city": "Davis", "slug": "davis", "county": "Yolo County",
        "median": "approximately $850K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Davis purchases fall below the 2026 Yolo County conforming ceiling, so jumbo loans here typically apply to larger homes rather than the typical purchase.",
        "dscr_market": "Davis' large university population anchors deep, year-round rental demand, one of the Sacramento region's most reliable DSCR markets for occupancy.",
    },
    {
        "city": "Woodland", "slug": "woodland", "county": "Yolo County",
        "median": "approximately $560K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Woodland purchases fall far below the 2026 Yolo County conforming ceiling, so jumbo financing is rarely needed in this agricultural county-seat city.",
        "dscr_market": "Woodland's agricultural economy, historic downtown, and accessible prices support steady rental demand, a favorable Yolo County DSCR cash-flow market.",
    },
    {
        "city": "West Sacramento", "slug": "west-sacramento", "county": "Yolo County",
        "median": "approximately $530K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard West Sacramento purchases fall far below the 2026 Yolo County conforming ceiling, so jumbo financing is rarely needed in this riverfront city.",
        "dscr_market": "West Sacramento's riverfront redevelopment and proximity to downtown Sacramento support steady rental demand, a favorable Yolo County DSCR cash-flow market.",
    },

    # ===================== San Joaquin County (wave 2) =====================
    {
        "city": "Stockton", "slug": "stockton", "county": "San Joaquin County",
        "median": "approximately $430K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Stockton purchases fall far below the 2026 San Joaquin County conforming ceiling, so jumbo financing is rarely needed in this Central Valley city.",
        "dscr_market": "Stockton's low prices, port economy, and Bay Area commuter demand produce some of Northern California's most favorable rent-to-price ratios, a strong DSCR cash-flow market.",
    },
    {
        "city": "Lodi", "slug": "lodi", "county": "San Joaquin County",
        "median": "approximately $520K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Lodi purchases fall far below the 2026 San Joaquin County conforming ceiling, so jumbo financing is rarely needed in this wine-country town.",
        "dscr_market": "Lodi's wine-country economy and small-city appeal support steady rental demand at accessible prices, a favorable San Joaquin County DSCR cash-flow market.",
    },
    {
        "city": "Tracy", "slug": "tracy", "county": "San Joaquin County",
        "median": "approximately $690K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Most standard Tracy purchases fall below the 2026 San Joaquin County conforming ceiling, so jumbo financing here generally applies to larger or newer homes.",
        "dscr_market": "Tracy's Bay Area commuter appeal and new housing growth support steady rental demand, a favorable San Joaquin County DSCR cash-flow market.",
    },
    {
        "city": "Manteca", "slug": "manteca", "county": "San Joaquin County",
        "median": "approximately $590K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Manteca purchases fall below the 2026 San Joaquin County conforming ceiling, so jumbo financing is rarely needed in this fast-growing city.",
        "dscr_market": "Manteca's new housing growth and Central Valley commuter appeal support steady rental demand, a favorable San Joaquin County DSCR cash-flow market.",
    },

    # ===================== Stanislaus County (wave 2) =====================
    {
        "city": "Modesto", "slug": "modesto", "county": "Stanislaus County",
        "median": "approximately $450K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Modesto purchases fall far below the 2026 Stanislaus County conforming ceiling, so jumbo financing is rarely needed in this Central Valley city.",
        "dscr_market": "Modesto's agricultural economy and affordable prices produce favorable rent-to-price ratios, a strong Central Valley DSCR cash-flow market.",
    },
    {
        "city": "Turlock", "slug": "turlock", "county": "Stanislaus County",
        "median": "approximately $490K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Turlock purchases fall far below the 2026 Stanislaus County conforming ceiling, so jumbo financing is rarely needed in this university-and-agriculture city.",
        "dscr_market": "Turlock's university presence and agricultural economy support steady rental demand at accessible prices, a favorable Stanislaus County DSCR cash-flow market.",
    },
    {
        "city": "Ceres", "slug": "ceres", "county": "Stanislaus County",
        "median": "approximately $460K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Ceres purchases fall far below the 2026 Stanislaus County conforming ceiling, so jumbo financing is rarely needed in this Central Valley city.",
        "dscr_market": "Ceres' affordable prices and agricultural-valley demand produce strong rent-to-price ratios, a favorable Stanislaus County DSCR cash-flow market.",
    },

    # ===================== Merced County (wave 2) =====================
    {
        "city": "Merced", "slug": "merced", "county": "Merced County",
        "median": "approximately $400K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Merced purchases fall far below the 2026 Merced County conforming ceiling, so jumbo financing is rarely needed in this Central Valley university city.",
        "dscr_market": "Merced's growing UC campus anchors year-round rental demand at low prices, producing some of California's most favorable rent-to-price ratios for DSCR investors.",
    },
    {
        "city": "Los Banos", "slug": "los-banos", "county": "Merced County",
        "median": "approximately $460K as of June 2026 (Zillow ZHVI)",
        "jumbo_market": "Standard Los Banos purchases fall far below the 2026 Merced County conforming ceiling, so jumbo financing is rarely needed in this affordable valley city.",
        "dscr_market": "Los Banos' low prices and Bay Area commuter growth support steady rental demand, a favorable Merced County DSCR cash-flow market.",
    },
]

# ---------------------------------------------------------------------------
# PROGRAM config
# ---------------------------------------------------------------------------
PROGRAMS = {
    "jumbo": {
        "name": "Jumbo Loans",
        "fp_name": "Jumbo Mortgage Loans",
        "fp_desc": "High-balance mortgage loans for properties exceeding conforming loan limits.",
        "hub": "/jumbo-loans",
        "sibling_dir": "dscr",
        "sibling_label": "DSCR loans",
    },
    "dscr": {
        "name": "DSCR Loans",
        "fp_name": "DSCR Investment Property Loans",
        "fp_desc": "Debt service coverage ratio loans for investment properties qualifying on rental income.",
        "hub": "/dscr-loans",
        "sibling_dir": "jumbo",
        "sibling_label": "Jumbo loans",
    },
}


def build_faqs(prog, c):
    """Return a list of {q,a} dicts — city + program specific."""
    city = c["city"]
    county = c["county"]
    median = c["median"]
    county_limit = limit_for(c)
    area_phrase = "a high-cost area" if is_high_cost(county) else "where the national baseline limit applies"
    if prog == "jumbo":
        return [
            {
                "q": "What counts as a jumbo loan in %s?" % city,
                "a": "%s is in %s, %s, where the 2026 one-unit conforming limit is %s (per FHFA/HUD 2026 loan limits). A jumbo loan in %s is simply any one-unit loan amount above %s." % (city, county, area_phrase, county_limit, city, county_limit),
            },
            {
                "q": "How much are homes in %s, and does that mean I need a jumbo loan?" % city,
                "a": "The typical %s home value is %s. %s" % (city, median, c["jumbo_market"]),
            },
            {
                "q": "How much down payment do jumbo borrowers usually need in %s?" % city,
                "a": "Jumbo programs commonly look for a larger down payment — often 10 to 20 percent or more — along with strong credit and cash reserves. The exact figure depends on the loan amount, property, and your overall profile; we will review what may fit your %s purchase." % city,
            },
            {
                "q": "Can I use a jumbo loan for a second home in %s?" % city,
                "a": "Yes. Jumbo financing is available for primary residences, second homes, and many investment properties in %s, with terms that vary by occupancy and program." % city,
            },
        ]
    else:  # dscr
        return [
            {
                "q": "Do I need to verify my income for a DSCR loan in %s?" % city,
                "a": "No. A DSCR loan qualifies the %s property on whether its rental income covers the mortgage payment, rather than on your personal income documentation. A DSCR of 1.0 means rent equals the payment." % city,
            },
            {
                "q": "How does the 2026 loan limit affect a DSCR loan in %s?" % city,
                "a": "%s is in %s, where the 2026 one-unit conforming limit is %s (per FHFA/HUD 2026 loan limits). DSCR loans are non-conforming investor loans, so they are not capped by that limit — but it is a useful local benchmark, since the typical %s home value is %s." % (city, county, county_limit, city, median),
            },
            {
                "q": "What rental market should investors expect in %s?" % city,
                "a": c["dscr_market"],
            },
            {
                "q": "Can I use a DSCR loan for short-term rentals in %s?" % city,
                "a": "Often yes. Some DSCR programs will consider short-term or vacation rental income for %s properties, though guidelines and documentation requirements vary by program." % city,
            },
        ]


def faq_html(faqs):
    parts = []
    for f in faqs:
        parts.append(
            '  <details class="acc"><summary>%s</summary><div class="acc-body">%s</div></details>'
            % (f["q"], f["a"])
        )
    return "\n".join(parts)


def faqpage_jsonld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in faqs
        ],
    }


def financialproduct_jsonld(prog_cfg, url, city, prog_name):
    return {
        "@context": "https://schema.org",
        "@type": "FinancialProduct",
        "name": "%s in %s" % (prog_cfg["fp_name"], city),
        "url": url,
        "description": prog_cfg["fp_desc"],
        "provider": {
            "@type": "Organization",
            "name": "West Coast Capital Mortgage Inc.",
            "url": "https://westccmortgage.com",
            "telephone": PHONE,
        },
    }


def breadcrumb_jsonld(prog_cfg, prog_name, city, url):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://westccmortgage.com/"},
            {"@type": "ListItem", "position": 2, "name": "Loans", "item": "https://westccmortgage.com/loans"},
            {"@type": "ListItem", "position": 3, "name": prog_name, "item": "https://westccmortgage.com" + prog_cfg["hub"]},
            {"@type": "ListItem", "position": 4, "name": city, "item": url},
        ],
    }


def jd(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)


def render_page(prog, prog_cfg, c):
    city = c["city"]
    slug = c["slug"]
    county = c["county"]
    median = c["median"]
    county_limit = limit_for(c)
    prog_name = prog_cfg["name"]
    url = "https://westccmortgage.com/loans/%s/%s" % (prog, slug)

    title = "%s in %s, CA | West Coast Capital Mortgage" % (prog_name, city)
    if prog == "jumbo":
        desc = ("Jumbo loans in %s, %s. With a 2026 one-unit conforming limit of %s, "
                "a jumbo loan finances %s homes above that ceiling. NMLS #%s.") % (
                    city, county, county_limit, city, NMLS)
        lead = ("Financing %s homes above the 2026 %s conforming limit of %s. %s") % (
            city, county, county_limit, c["jumbo_market"])
        market = c["jumbo_market"]
    else:
        desc = ("DSCR investment property loans in %s, %s. Qualify on rental income, not personal income. "
                "Local 2026 conforming limit context: %s. NMLS #%s.") % (
                    city, county, county_limit, NMLS)
        lead = ("DSCR investment property loans in %s — qualify on the property's rental cash flow rather than "
                "personal income. %s") % (city, c["dscr_market"])
        market = c["dscr_market"]

    faqs = build_faqs(prog, c)

    fp = financialproduct_jsonld(prog_cfg, url, city, prog_name)
    bc = breadcrumb_jsonld(prog_cfg, prog_name, city, url)
    fq = faqpage_jsonld(faqs)

    sibling = PROGRAMS[prog_cfg["sibling_dir"]]
    sibling_url = "/loans/%s/%s" % (prog_cfg["sibling_dir"], slug)

    if is_high_cost(county):
        limit_paragraph = ("Across %s, the 2026 one-unit conforming loan limit is %s (per FHFA/HUD 2026 loan limits), "
                           "set above the %s national baseline because %s is a designated high-cost area.") % (
                               county, county_limit, BASELINE_LIMIT, county)
    else:
        limit_paragraph = ("Across %s, the 2026 one-unit conforming loan limit is the %s national baseline "
                           "(per FHFA/HUD 2026 loan limits); %s is not designated a high-cost area, so the standard "
                           "conforming ceiling applies.") % (county, BASELINE_LIMIT, county)

    # Stat cards differ by program
    if prog == "jumbo":
        cards = ('<div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">%s</h3>'
                 '<p style="margin:0">2026 %s 1-unit limit</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">Above</h3>'
                 '<p style="margin:0">the conforming ceiling</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">700+</h3>'
                 '<p style="margin:0">Typical credit score</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">10&ndash;20%%+</h3>'
                 '<p style="margin:0">Typical down payment</p></div></div>') % (county_limit, county)
        overview_h = "What a jumbo loan means in %s" % city
        area_clause = ("a high-cost area with a 2026 one-unit conforming limit of %s" % county_limit
                       if is_high_cost(county)
                       else "where the 2026 one-unit conforming limit is the national baseline of %s" % county_limit)
        overview_p = ("A jumbo loan exceeds the conforming limit set by the Federal Housing Finance Agency. "
                      "Because %s is in %s — %s "
                      "(per FHFA/HUD 2026 loan limits) — a jumbo loan in %s is any one-unit loan above %s. "
                      "%s") % (city, county, area_clause, city, county_limit, market)
        overview_p2 = ("For strong borrowers, jumbo pricing is often very competitive with conforming loans. "
                       "The typical %s home value is %s, which is why jumbo financing is so common here.") % (city, median)
        req_list = ('<ul class="feature-list"><li>A strong credit score, generally 700 or higher</li>'
                    '<li>A larger down payment (often 10&ndash;20%+)</li>'
                    '<li>Significant cash reserves</li>'
                    '<li>Full documentation of income and assets</li></ul>')
        ben_list = ('<ul class="feature-list">'
                    '<li>Finance high-value %s properties in a single loan</li>'
                    '<li>Competitive rates for strong borrowers</li>'
                    '<li>Fixed and adjustable options</li>'
                    '<li>Available for primary, second, and investment homes</li></ul>') % city
    else:
        cards = ('<div class="grid grid-4"><div class="card center"><h3 style="color:var(--blue)">DSCR</h3>'
                 '<p style="margin:0">Income = property</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">No DTI</h3>'
                 '<p style="margin:0">Personal income optional</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">%s</h3>'
                 '<p style="margin:0">2026 %s 1-unit limit</p></div>'
                 '<div class="card center"><h3 style="color:var(--blue)">Scale</h3>'
                 '<p style="margin:0">Grow your holdings</p></div></div>') % (county_limit, county)
        overview_h = "What a DSCR loan means in %s" % city
        overview_p = ("DSCR stands for Debt-Service Coverage Ratio. A DSCR loan qualifies a %s investment property "
                      "based on whether its rental income covers the mortgage payment, rather than on your personal "
                      "income. A DSCR of 1.0 means rent equals the payment; higher ratios indicate stronger cash flow. "
                      "%s") % (city, market)
        overview_p2 = ("DSCR loans are non-conforming investor loans, so they are not capped by the conforming limit. "
                       "Still, the 2026 one-unit conforming limit in %s is %s (per FHFA/HUD 2026 loan limits), and the "
                       "typical %s home value is %s — useful benchmarks when you size a purchase.") % (county, county_limit, city, median)
        req_list = ('<ul class="feature-list"><li>An investment (non-owner-occupied) %s property</li>'
                    '<li>Rental income that supports the debt-service coverage ratio</li>'
                    '<li>A down payment consistent with investor programs</li>'
                    '<li>A solid credit profile and reserves</li></ul>') % city
        ben_list = ('<ul class="feature-list">'
                    '<li>Qualify on %s property cash flow, not personal income</li>'
                    '<li>Streamlined documentation for investors</li>'
                    '<li>Finance multiple properties over time</li>'
                    '<li>Available for short- and long-term rentals</li></ul>') % city

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">

<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="author" content="West Coast Capital Mortgage Inc.">
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="{city}, California">
<meta property="og:type" content="website">
<meta property="og:site_name" content="West Coast Capital Mortgage Inc.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://westccmortgage.com/assets/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://westccmortgage.com/assets/og-image.jpg">
<script type="application/ld+json">
{fp}
</script>
<script type="application/ld+json">
{bc}
</script>
<script type="application/ld+json">
{fq}
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "wzzlo9s35g");
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
    <!-- Replace with <img src="/assets/logo.png" alt="West Coast Capital Mortgage Inc."> when ready -->
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
    <div class="crumbs"><a href="/index.html">Home</a> &nbsp;/&nbsp; <a href="/loans.html">Loans</a> &nbsp;/&nbsp; <a href="{hub}">{prog_name}</a> &nbsp;/&nbsp; {city}</div>
    <h1>{prog_name} in {city}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
<section><div class="wrap">
  {cards}
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <div>
    <span class="eyebrow">Overview</span>
    <h2>{overview_h}</h2>
    <p>{overview_p}</p><p>{overview_p2}</p>
    <div class="btn-row"><a class="btn btn-blue" href="/apply.html">Get Preapproved</a><a class="btn btn-outline" href="{hub}">All about {prog_name}</a></div>
  </div>
  <div>
    <h3>Typical requirements</h3>
    {req_list}
    <h3 style="margin-top:30px">Potential benefits</h3>
    {ben_list}
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <span class="eyebrow">{city} market</span>
  <h2>{prog_name} and the {city} market</h2>
  <p>The typical {city} home value is {median}. {market}</p>
  <p>{limit_paragraph} We can walk you through exactly how that limit applies to your {city} scenario.</p>
  <p class="muted" style="font-size:.9rem">Home-value figure is an approximate market reference for {city} as of mid-2026, rounded and provided for general education only; it is not an appraisal or valuation of any specific property.</p>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>{prog_name} in {city} &mdash; common questions</h2></div>
{faq_html}
</div></section>

<section style="padding-top:0"><div class="wrap">
  <h3>Related links</h3>
  <p>Learn more about our <a href="{hub}">{prog_name}</a> program, explore <a href="{sibling_url}">{sibling_label} in {city}</a>, or see <a href="/loans.html">all loan programs</a>.</p>
</div></section>

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
    <div class="footer-grid"><div class="footer-brand"><div class="l1">WEST COAST CAPITAL</div><div class="l2">MORTGAGE INC.</div><p style="color:#aab2bd;font-size:.9rem">Modern mortgage guidance for buying, refinancing, and building equity.</p><p class="footer-contact"><b>Office / Loan Officer Questions:</b> <a href="tel:3106541577">310-654-1577</a><br><b>Anatoliy Direct:</b> <a href="tel:3106865053">310-686-5053</a><br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a></p></div><div><h4>Buy A Home</h4><a href="/homebuying-guide.html">Homebuying Guide</a><a href="/apply.html">Mortgage Pre-Approval</a><a href="/first-time-homebuyer.html">First-Time Homebuyers</a><a href="/buy.html">Down Payment Assistance</a><a href="/loans.html">Home Purchase Loans</a></div><div><h4>Refinance</h4><a href="/refinancing-guide.html">Refinancing Guide</a><a href="/rates.html">Refinance Mortgage Rates</a><a href="/refinance.html">Cash-Out Refinance</a><a href="/refinance.html">Rate-and-Term Refinance</a></div><div><h4>Loans</h4><a href="/conventional-loans.html">Conventional Loans</a><a href="/fha-loans.html">FHA Loans</a><a href="/va-loans.html">VA Loans</a><a href="/jumbo-loans.html">Jumbo Loans</a><a href="/non-qm-loans.html">Non-QM Loans</a><a href="/bank-statement-loans.html">Bank Statement Loans</a><a href="/dscr-loans.html">DSCR Loans</a><a href="/investment-property-loans.html">Investment Property Loans</a></div><div><h4>Resources</h4><a href="https://wcci.online" target="_blank" rel="noopener noreferrer">WCCI.Online AI Mortgage Review</a><a href="/calculators.html">Mortgage Calculators</a><a href="/mortgage-articles.html">Mortgage Articles</a><a href="/glossary.html">Mortgage Glossary</a><a href="/faq.html">Mortgage FAQ</a><a href="/resources.html">Mortgage Videos</a><a href="/rates.html">Rate Watch</a></div><div><h4>About Us</h4><a href="/about.html">About West Coast Capital Mortgage</a><a href="/contact.html">Contact Us</a><a href="https://2817729.myagentloans.com/register" target="_blank" rel="noopener noreferrer">Find a Loan Officer</a><a href="/about.html">Licensing & Disclosures</a></div></div>
    <div class="footer-bottom">
      <div class="row">
        <nav aria-label="Legal">
          <a href="/about.html" style="display:inline;margin-right:18px">Licensing and Disclosures</a>
          <a href="https://www.nmlsconsumeraccess.org/" target="_blank" rel="noopener noreferrer" style="display:inline">NMLS Consumer Access</a>
        </nav>
        <span class="eho"><img src="/assets/equal-housing.svg" alt="Equal Housing Opportunity" style="height:32px;vertical-align:middle;margin-right:7px;opacity:.92"> Equal Housing Opportunity</span>
      </div>
      <p>West Coast Capital Mortgage Inc. NMLS #{nmls}. Equal Housing Opportunity. Information is provided for
      educational purposes only and is not a commitment to lend. All loans are subject to credit, income, property,
      and underwriting approval.</p>
      <p>&copy; <span class="year"></span> West Coast Capital Mortgage Inc. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="/i18n.js"></script>
<script src="/script.js"></script>
</body>
</html>""".format(
        title=title, desc=desc, url=url, city=city, hub=prog_cfg["hub"], prog_name=prog_name,
        prog_name_lower=prog_name.lower(), lead=lead, cards=cards, overview_h=overview_h,
        overview_p=overview_p, overview_p2=overview_p2, req_list=req_list, ben_list=ben_list,
        median=median, market=market, county=county, county_limit=county_limit, baseline=BASELINE_LIMIT,
        limit_paragraph=limit_paragraph,
        faq_html=faq_html(faqs), sibling_url=sibling_url, sibling_label=sibling["name"],
        nmls=NMLS, fp=jd(fp), bc=jd(bc), fq=jd(fq),
    )
    return html


# County display order for grouped hub link sections.
COUNTY_ORDER = [
    "Los Angeles County", "Orange County", "Ventura County", "Santa Barbara County",
    "San Diego County", "San Bernardino County", "Riverside County", "Kern County",
    # ---- Wave 2: San Diego radius ----
    "Imperial County",
    # ---- Wave 2: San Francisco Bay Area ----
    "San Francisco County", "San Mateo County", "Santa Clara County", "Alameda County",
    "Contra Costa County", "Marin County",
    # ---- Wave 2: North Bay / Wine Country ----
    "Sonoma County", "Napa County", "Solano County",
    # ---- Wave 2: Central Coast ----
    "Santa Cruz County", "San Benito County", "Monterey County",
    # ---- Wave 2: Sacramento region ----
    "Sacramento County", "Placer County", "El Dorado County", "Yolo County",
    # ---- Wave 2: Central Valley ----
    "San Joaquin County", "Stanislaus County", "Merced County",
]


def city_links_section(prog):
    """Build the 'X loans by city' section, grouped by county, for the hub pages."""
    label = PROGRAMS[prog]["name"]
    # group cities by county
    by_county = {}
    for c in CITY_DATA:
        by_county.setdefault(c["county"], []).append(c)
    ordered = COUNTY_ORDER + [k for k in by_county if k not in COUNTY_ORDER]
    blocks = []
    for county in ordered:
        cities = by_county.get(county)
        if not cities:
            continue
        cities = sorted(cities, key=lambda x: x["city"])
        links = "".join(
            '<a href="/loans/%s/%s">%s, CA</a>' % (prog, c["slug"], c["city"]) for c in cities
        )
        blocks.append(
            '  <h3 style="margin-top:22px">%s &mdash; 2026 limit %s</h3>\n'
            '  <div class="city-links">%s</div>' % (county, COUNTY_LIMITS[county], links)
        )
    inner = "\n".join(blocks)
    return (
        '\n<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="section-head"><span class="eyebrow">By city</span><h2>%s by city</h2></div>\n'
        '%s\n'
        '</div></section>\n' % (label, inner)
    )


def insert_city_links(hub_path, prog):
    with open(hub_path, "r", encoding="utf-8") as f:
        html = f.read()
    marker = "<!-- CITY-LINKS:%s -->" % prog
    section = marker + city_links_section(prog) + ("<!-- /CITY-LINKS:%s -->" % prog)
    if marker in html:
        # idempotent replace between markers
        start = html.index(marker)
        end = html.index("<!-- /CITY-LINKS:%s -->" % prog) + len("<!-- /CITY-LINKS:%s -->" % prog)
        html = html[:start] + section + html[end:]
    else:
        # insert before the WCCI AI CTA band (first wcci-cta section)
        anchor = '<section><div class="wrap"><div class="wcci-cta">'
        idx = html.index(anchor)
        html = html[:idx] + section + "\n" + html[idx:]
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(html)


def update_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        xml = f.read()
    # Remove any previously generated city block (idempotent)
    start_marker = "  <!-- city-pages:start -->"
    end_marker = "  <!-- city-pages:end -->"
    if start_marker in xml and end_marker in xml:
        s = xml.index(start_marker)
        e = xml.index(end_marker) + len(end_marker)
        xml = xml[:s] + xml[e:]
        # tidy any leftover blank line
        xml = xml.replace("\n\n</urlset>", "\n</urlset>")
    entries = [start_marker]
    for prog in ("jumbo", "dscr"):
        for c in CITY_DATA:
            loc = "https://westccmortgage.com/loans/%s/%s" % (prog, c["slug"])
            entries.append(
                "  <url>\n"
                "    <loc>%s</loc>\n"
                "    <lastmod>%s</lastmod>\n"
                "    <changefreq>monthly</changefreq>\n"
                "    <priority>0.7</priority>\n"
                "  </url>" % (loc, LASTMOD)
            )
    entries.append(end_marker)
    block = "\n".join(entries) + "\n"
    xml = xml.replace("</urlset>", block + "</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    created = []
    for prog, prog_cfg in PROGRAMS.items():
        outdir = os.path.join(ROOT, "loans", prog)
        os.makedirs(outdir, exist_ok=True)
        for c in CITY_DATA:
            html = render_page(prog, prog_cfg, c)
            outpath = os.path.join(outdir, c["slug"] + ".html")
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(html)
            created.append(outpath)

    insert_city_links(os.path.join(ROOT, "jumbo-loans.html"), "jumbo")
    insert_city_links(os.path.join(ROOT, "dscr-loans.html"), "dscr")
    update_sitemap()

    print("Created %d city pages:" % len(created))
    for p in created:
        print("  " + p)
    print("Updated hubs: jumbo-loans.html, dscr-loans.html")
    print("Updated sitemap.xml (%d city URLs = %d cities x 2 programs)" % (len(CITY_DATA) * 2, len(CITY_DATA)))


if __name__ == "__main__":
    main()
