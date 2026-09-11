from pathlib import Path
import re
import subprocess

p = Path("gen_geo_pages.py")
s = p.read_text(encoding="utf-8")


def replace_once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f"{label}: expected source text not found")
    s = s.replace(old, new, 1)


# Home value is useful market context, but jumbo classification is based on the
# requested conventional loan amount relative to the county conforming limit.
pattern = re.compile(r"def jumbo_likelihood\(median_str, limit_str\):\n.*?\n\ndef median_short", re.S)
replacement = '''def jumbo_likelihood(median_str, limit_str):
    """Home-price context only; jumbo status is determined by the loan amount."""
    med, lim = money_to_float(median_str), money_to_float(limit_str)
    if not med or not lim:
        return "Price context unavailable"
    r = med / lim
    if r >= 2.0:
        return "Typical value far above limit"
    if r >= 1.15:
        return "Typical value above limit"
    if r >= 0.90:
        return "Typical value near the limit"
    if r >= 0.60:
        return "Typical value below limit"
    return "Typical value well below limit"


def median_short'''
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f"jumbo_likelihood: expected one replacement, got {n}")

# FHFA publishes the conforming loan limits. Remove the misleading HUD attribution,
# including source strings that are split across adjacent Python literals.
s = s.replace("per FHFA/HUD 2026 loan limits", "per FHFA 2026 conforming loan limits")
s = s.replace("per FHFA/HUD 2026 loan ", "per FHFA 2026 conforming loan ")

replace_once(
    '''    desc = ("Jumbo loans in %s. The 2026 one-unit conforming limit is %s, so any one-unit loan above that "
            "is a jumbo loan. Typical values for %d %s cities inside. NMLS #%s."
            % (county, limit, len(cities), short, NMLS))''',
    '''    desc = ("Jumbo loans in %s. The 2026 one-unit conforming limit is %s. Conventional loan amounts above "
            "the county limit are generally jumbo financing; local home-value context for %d %s cities inside. NMLS #%s."
            % (county, limit, len(cities), short, NMLS))''',
    "county meta description",
)

replace_once(
    '''        limit_para = ("%s is a designated high-cost area, so its 2026 one-unit conforming loan limit is %s "
                      "(per FHFA 2026 conforming loan limits) rather than the %s national baseline. Any one-unit "
                      "loan above %s in %s is a jumbo loan."
                      % (county, limit, BASELINE_LIMIT, limit, county))''',
    '''        limit_para = ("%s is a designated high-cost area, so its 2026 one-unit conforming loan limit is %s "
                      "(per FHFA 2026 conforming loan limits) rather than the %s national baseline. A conventional "
                      "one-unit loan amount above %s in %s is generally considered jumbo financing."
                      % (county, limit, BASELINE_LIMIT, limit, county))''',
    "high-cost county definition",
)

replace_once(
    '''        limit_para = ("%s is not designated a high-cost area, so the 2026 one-unit conforming loan limit is "
                      "the national baseline of %s (per FHFA 2026 conforming loan limits). Any one-unit loan above "
                      "%s in %s is a jumbo loan." % (county, BASELINE_LIMIT, limit, county))''',
    '''        limit_para = ("%s is not designated a high-cost area, so the 2026 one-unit conforming loan limit is "
                      "the national baseline of %s (per FHFA 2026 conforming loan limits). A conventional one-unit "
                      "loan amount above %s in %s is generally considered jumbo financing." % (county, BASELINE_LIMIT, limit, county))''',
    "baseline county definition",
)

replace_once(
    '<th>Is a jumbo loan usually needed?</th></tr></thead>',
    '<th>Home-price context vs. conforming limit</th></tr></thead>',
    "county table header",
)

replace_once(
    '''    spread = ("Values across the county run from roughly %s in %s to about %s in %s, so whether a purchase "
              "needs jumbo financing varies widely by city &mdash; the table below shows where each one sits "
              "against the %s limit."
              % (median_short(cheapest["median"]), cheapest["city"],
                 median_short(priciest["median"]), priciest["city"], limit))''',
    '''    spread = ("Values across the county run from roughly %s in %s to about %s in %s. Home price alone does "
              "not determine whether financing is jumbo: compare the planned conventional one-unit loan amount "
              "after the down payment with the %s county conforming limit. The table below is price context only."
              % (median_short(cheapest["median"]), cheapest["city"],
                 median_short(priciest["median"]), priciest["city"], limit))''',
    "county price spread explanation",
)

replace_once(
    '''    lead = ("The 2026 one-unit conforming limit in %s is %s. Any one-unit loan above that is a jumbo loan. "
            "Below: how that line falls across %d %s cities." % (county, limit, len(cities), short))''',
    '''    lead = ("The 2026 one-unit conforming limit in %s is %s. Jumbo status depends on the requested conventional "
            "loan amount after the down payment, not on the home's purchase price by itself. Below: local price context "
            "across %d %s cities." % (county, limit, len(cities), short))''',
    "county lead explanation",
)

replace_once(
    '''        {"q": "What is the 2026 jumbo loan limit in %s?" % county,
         "a": "In %s the 2026 one-unit conforming limit is %s (per FHFA 2026 conforming loan limits). A jumbo loan "
              "is any one-unit loan amount above %s. %s"
              % (county, limit, limit,
                 "The county carries the high-cost limit rather than the %s national baseline." % BASELINE_LIMIT
                 if high else "This is the national baseline limit; %s is not a designated high-cost area." % county)},
        {"q": "Which %s cities usually require a jumbo loan?" % short,
         "a": "It varies by city. In %s, where typical values run around %s, jumbo financing applies to most "
              "standard purchases. In %s, closer to %s, it comes into play mainly on higher-end homes. The "
              "table on this page marks where each of the %d cities we cover falls against the %s limit."
              % (priciest["city"], median_short(priciest["median"]),
                 cheapest["city"], median_short(cheapest["median"]), len(cities), limit)},''',
    '''        {"q": "What is the 2026 conforming loan limit in %s?" % county,
         "a": "In %s the 2026 one-unit conforming limit is %s (per FHFA 2026 conforming loan limits). A conventional "
              "one-unit loan amount above %s is generally considered jumbo financing. %s"
              % (county, limit, limit,
                 "The county carries the high-cost limit rather than the %s national baseline." % BASELINE_LIMIT
                 if high else "This is the national baseline limit; %s is not a designated high-cost area." % county)},
        {"q": "How do home prices relate to jumbo financing in %s?" % short,
         "a": "Home price is context, but it does not determine jumbo status by itself. A higher-priced home can "
              "still use conforming financing if the requested conventional one-unit loan amount after the down "
              "payment is at or below the %s county limit. Typical values range from about %s in %s to about %s in %s; "
              "compare the planned loan amount with the county limit rather than the purchase price alone."
              % (limit, median_short(cheapest["median"]), cheapest["city"],
                 median_short(priciest["median"]), priciest["city"])},''',
    "county jumbo FAQ logic",
)

replace_once(
    '''        head = ("<h2>Jumbo loan limits by California county</h2>"
                "<p>The 2026 one-unit conforming limit is set per county. Pick a county to see its limit and "
                "how it falls across local home values.</p>")''',
    '''        head = ("<h2>Jumbo loan limits by California county</h2>"
                "<p>The 2026 one-unit conforming limit is set per county. Pick a county to see its limit and "
                "local home-value context; jumbo status depends on the requested loan amount.</p>")''',
    "jumbo hub county explanation",
)

p.write_text(s, encoding="utf-8")
subprocess.run(["python3", "gen_geo_pages.py"], check=True)
print("Corrected jumbo classification logic and regenerated geo pages.")
