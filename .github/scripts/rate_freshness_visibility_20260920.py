from pathlib import Path


def replace_required(path: Path, old: str, new: str, expected: int = 1) -> None:
    text = path.read_text(encoding="utf-8")
    found = text.count(old)
    if found != expected:
        raise SystemExit(f"{path}: expected {expected} occurrence(s), found {found}: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_optional(path: Path, old: str, new: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    path.write_text(text.replace(old, new), encoding="utf-8")
    return True


index = Path("wccm-corporate/index.html")
rates = Path("wccm-corporate/rates.html")

# Homepage: do not imply an older dated sample is literally today's pricing.
replace_required(
    index,
    '<span class="eyebrow" style="color:var(--blue)">Today&rsquo;s Rates</span>',
    '<span class="eyebrow" style="color:var(--blue)">Sample Rates</span>',
)

# Dedicated rates page: keep the personalized quote language current, but remove
# false freshness claims from the cached/sample rate content and metadata.
replacements = [
    (
        "<title>Today's Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage</title>",
        "<title>Sample Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage Inc.</title>",
    ),
    (
        '<meta name="description" content="Today\'s mortgage rates from West Coast Capital Mortgage View current FHA, VA, Conventional & Jumbo rates. Updated daily. NMLS #2817729.">',
        '<meta name="description" content="Sample mortgage rates from West Coast Capital Mortgage Inc. View dated FHA, VA, Conventional and Jumbo pricing examples and request a personalized quote. NMLS #2817729.">',
    ),
    (
        '<meta property="og:title" content="Today\'s Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage">',
        '<meta property="og:title" content="Sample Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage Inc.">',
    ),
    (
        '<meta property="og:description" content="Today\'s mortgage rates from West Coast Capital Mortgage View current FHA, VA, Conventional & Jumbo rates. Updated daily. NMLS #2817729.">',
        '<meta property="og:description" content="Sample mortgage rates from West Coast Capital Mortgage Inc. View dated FHA, VA, Conventional and Jumbo pricing examples and request a personalized quote. NMLS #2817729.">',
    ),
    (
        '<meta name="twitter:title" content="Today\'s Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage">',
        '<meta name="twitter:title" content="Sample Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage Inc.">',
    ),
    (
        '<meta name="twitter:description" content="Today\'s mortgage rates from West Coast Capital Mortgage View current FHA, VA, Conventional & Jumbo rates. Updated daily. NMLS #2817729.">',
        '<meta name="twitter:description" content="Sample mortgage rates from West Coast Capital Mortgage Inc. View dated FHA, VA, Conventional and Jumbo pricing examples and request a personalized quote. NMLS #2817729.">',
    ),
    (
        '<meta name="geo.region" content="US-CA">\n<meta name="geo.placename" content="California">\n',
        "",
    ),
    (
        '{"@context":"https://schema.org","@type":"WebPage","name":"Today\'s Rates","url":"https://westcoastcapitalmortgage.com/rates","isPartOf":{"@type":"WebSite","name":"West Coast Capital Mortgage","url":"https://westcoastcapitalmortgage.com/"},"publisher":{"@type":"Organization","name":"West Coast Capital Mortgage","identifier":"NMLS #2817729"}}',
        '{"@context":"https://schema.org","@type":"WebPage","name":"Sample Mortgage Rates","url":"https://westcoastcapitalmortgage.com/rates","about":{"@type":"Service","name":"Mortgage rate review","areaServed":[{"@type":"State","name":"California"},{"@type":"State","name":"Florida"}]},"isPartOf":{"@type":"WebSite","name":"West Coast Capital Mortgage Inc.","url":"https://westcoastcapitalmortgage.com/"},"publisher":{"@type":"Organization","name":"West Coast Capital Mortgage Inc.","identifier":{"@type":"PropertyValue","name":"NMLS","value":"2817729"}}}',
    ),
    (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://westcoastcapitalmortgage.com/"},{"@type":"ListItem","position":2,"name":"Today\'s Rates","item":"https://westcoastcapitalmortgage.com/rates"}]}',
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://westcoastcapitalmortgage.com/"},{"@type":"ListItem","position":2,"name":"Sample Mortgage Rates","item":"https://westcoastcapitalmortgage.com/rates"}]}',
    ),
    (
        '<a href="rates.html" class="active">Today\'s Rates</a>',
        '<a href="rates.html" class="active">Mortgage Rates</a>',
    ),
    (
        '<div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Today&rsquo;s Rates</div>\n    <h1>Today&rsquo;s Rates</h1>',
        '<div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Sample Mortgage Rates</div>\n    <h1>Sample Mortgage Rates</h1>',
    ),
    (
        '<div class="section-head"><span class="eyebrow" style="color:var(--blue)">Today&rsquo;s Sample Rates</span><h2>Sample rates</h2>',
        '<div class="section-head"><span class="eyebrow" style="color:var(--blue)">Dated Pricing Examples</span><h2>Sample rates</h2>',
    ),
]

for old, new in replacements:
    replace_required(rates, old, new)

# Keep the generator aligned so a future rebuild does not restore stale "today"
# claims. These are optional because production has received manual visibility
# refinements since the original generator was created.
generator = Path("tools/build_site.py")
for old, new in [
    ("Today&rsquo;s Rates", "Sample Mortgage Rates"),
    ("Today's Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage", "Sample Mortgage Rates — FHA, VA, Conventional | West Coast Capital Mortgage Inc."),
    ("Today's mortgage rates from West Coast Capital Mortgage View current FHA, VA, Conventional & Jumbo rates. Updated daily. NMLS #2817729.", "Sample mortgage rates from West Coast Capital Mortgage Inc. View dated FHA, VA, Conventional and Jumbo pricing examples and request a personalized quote. NMLS #2817729."),
]:
    replace_optional(generator, old, new)

print("Rate freshness visibility patch applied successfully")
