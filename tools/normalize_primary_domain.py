#!/usr/bin/env python3
"""Normalize West Coast Capital Mortgage to its canonical production domain.

Deploy mode updates the Netlify publish directory in-place.
Source mode also updates WCCM generators/workflows so future rebuilds do not
re-introduce the retired short domain.
"""
from __future__ import annotations

import argparse
from pathlib import Path

OLD = "westccmortgage.com"
NEW = "westcoastcapitalmortgage.com"
CANONICAL = f"https://{NEW}"

DOMAIN_RULES = [
    f"https://{OLD}/* {CANONICAL}/:splat 301!",
    f"https://westccmtg.com/* {CANONICAL}/:splat 301!",
    f"https://cawccmortgage.com/* {CANONICAL}/:splat 301!",
    f"https://www.cawccmortgage.com/* {CANONICAL}/:splat 301!",
    f"https://cawccm.com/* {CANONICAL}/:splat 301!",
    f"http://cawccm.com/* {CANONICAL}/:splat 301!",
    f"https://www.cawccm.com/* {CANONICAL}/:splat 301!",
    f"http://www.cawccm.com/* {CANONICAL}/:splat 301!",
    f"https://westccmortgage.netlify.app/* {CANONICAL}/:splat 301!",
]

# Canonical clean-URL redirects that must be evaluated before the site's final
# 404 catch-all. Keep these here so build-time redirect normalization cannot
# accidentally place them after the catch-all or remove them as duplicates.
CANONICAL_PATH_RULES = [
    "/florida-dscr-loans.html /florida-dscr-loans 301!",
]

CONTACT_OLD_DESC = (
    "Contact West Coast Capital Mortgage Call 310-654-1577 or email us. "
    "Licensed mortgage lender in California. NMLS #2817729."
)
CONTACT_NEW_DESC = (
    "Contact West Coast Capital Mortgage Inc. at (310) 654-1577 for mortgage "
    "questions, scenario review, purchase, refinance, jumbo, self-employed, "
    "bank-statement, Non-QM and investor financing. Company NMLS #2817729."
)
CONTACT_OLD_SCHEMA = '''{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "West Coast Capital Mortgage",
  "url": "https://westcoastcapitalmortgage.com",
  "telephone": "+1-310-654-1577",
  "email": "westccmortgage@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressRegion": "CA",
    "addressCountry": "US"
  },
  "identifier": { "@type": "PropertyValue", "name": "NMLS", "value": "2817729" }
}'''
CONTACT_NEW_SCHEMA = '''{
  "@context": "https://schema.org",
  "@type": ["FinancialService", "LocalBusiness"],
  "name": "West Coast Capital Mortgage Inc.",
  "alternateName": "West Coast Capital Mortgage",
  "legalName": "West Coast Capital Mortgage Inc.",
  "url": "https://westcoastcapitalmortgage.com",
  "telephone": "+1-310-654-1577",
  "email": "westccmortgage@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "150 E Olive Ave, Unit 112",
    "addressLocality": "Burbank",
    "addressRegion": "CA",
    "postalCode": "91502",
    "addressCountry": "US"
  },
  "areaServed": [
    { "@type": "State", "name": "California" },
    { "@type": "State", "name": "Florida" }
  ],
  "serviceType": ["Home Purchase Loans", "Mortgage Refinance", "Jumbo Loans", "Bank Statement Loans", "Non-QM Loans", "DSCR Loans", "Investment Property Loans", "Mortgage Second Opinion"],
  "sameAs": [
    "https://www.nmlsconsumeraccess.org/EntityDetails.aspx/COMPANY/2817729",
    "https://g.page/r/CXUFd3B5e-n3EBM"
  ],
  "identifier": { "@type": "PropertyValue", "name": "NMLS", "value": "2817729" }
}'''
CONTACT_OLD_DETAILS = '<p class="contact-lines"><b>Office / Loan Officer Questions:</b> <a href="tel:3106541577">310-654-1577</a><br><b>Anatoliy Direct:</b> <a href="tel:3106865053">310-686-5053</a><br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a></p>\n    <p class="muted">Equal Housing Opportunity &middot; NMLS #2817729</p>'
CONTACT_NEW_DETAILS = '<p class="contact-lines"><b>Office / Loan Officer Questions:</b> <a href="tel:3106541577">310-654-1577</a><br><b>Anatoliy Direct:</b> <a href="tel:3106865053">310-686-5053</a><br><b>Email:</b> <a href="mailto:westccmortgage@gmail.com">westccmortgage@gmail.com</a><br><b>Office:</b> 150 E Olive Ave, Unit 112, Burbank, CA 91502</p>\n    <p class="muted">West Coast Capital Mortgage Inc. &middot; Company NMLS #2817729 &middot; Equal Housing Opportunity</p>'


def replace_domain(path: Path) -> int:
    if not path.is_file() or path.name == "_redirects":
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0
    count = text.count(OLD)
    if count:
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    return count


def normalize_contact_entity(path: Path) -> int:
    """Keep the Contact page state-neutral while preserving canonical WCCM identity."""
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace(CONTACT_OLD_DESC, CONTACT_NEW_DESC)
    text = text.replace('<meta name="geo.region" content="US-CA">\n', '')
    text = text.replace('<meta name="geo.placename" content="California">\n', '')
    text = text.replace(CONTACT_OLD_SCHEMA, CONTACT_NEW_SCHEMA)
    text = text.replace(CONTACT_OLD_DETAILS, CONTACT_NEW_DETAILS)

    # Idempotent guards: after the first source repair, every later deploy must
    # still carry the correct entity signals and must not reintroduce CA-only copy.
    required = [
        CONTACT_NEW_DESC,
        CONTACT_NEW_SCHEMA,
        "150 E Olive Ave, Unit 112, Burbank, CA 91502",
        "Company NMLS #2817729",
    ]
    missing = [item[:80] for item in required if item not in text]
    if missing:
        raise SystemExit("Contact entity normalization guard failed: " + " | ".join(missing))
    if "Licensed mortgage lender in California" in text:
        raise SystemExit("CA-only Contact licensing copy remains")
    if 'meta name="geo.region"' in text or 'meta name="geo.placename"' in text:
        raise SystemExit("CA-only Contact geo metadata remains")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def clean_redirects(path: Path) -> tuple[int, int]:
    """Keep first-match semantics, remove unreachable duplicates, and put host rules first."""
    if not path.exists():
        raise FileNotFoundError(path)

    original = path.read_text(encoding="utf-8").splitlines()
    unique_rules: list[str] = []
    seen_sources: set[str] = {rule.split()[0] for rule in CANONICAL_PATH_RULES}
    duplicate_count = 0

    alternate_hosts = {
        OLD,
        f"www.{OLD}",
        "westccmtg.com",
        "www.westccmtg.com",
        "cawccmortgage.com",
        "www.cawccmortgage.com",
        "cawccm.com",
        "www.cawccm.com",
        "westccmortgage.netlify.app",
    }

    for raw in original:
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        if len(parts) < 3:
            continue
        source, target, status = parts[0], parts[1], parts[2]

        # Catch-all is rebuilt once, at the bottom.
        if status == "404" or source == "/*" and target == "/404.html":
            continue

        # Host-level rules are rebuilt once, at the top.
        if source.startswith("http://") or source.startswith("https://"):
            host = source.split("://", 1)[1].split("/", 1)[0].lower()
            if host in alternate_hosts:
                continue

        if source in seen_sources:
            duplicate_count += 1
            continue
        seen_sources.add(source)
        unique_rules.append(" ".join(parts[:3]))

    out = [
        "# West Coast Capital Mortgage — Netlify redirects",
        f"# Canonical host: {CANONICAL}",
        "",
        "# Alternate hosts -> canonical host",
        *DOMAIN_RULES,
        "",
        "# Canonical path redirects",
        *CANONICAL_PATH_RULES,
        "",
        "# Retired URLs -> current consolidated pages (first-match order preserved)",
        *unique_rules,
        "",
        "# Catch-all must remain last",
        "/* /404.html 404",
        "",
    ]
    path.write_text("\n".join(out), encoding="utf-8")
    return len(unique_rules), duplicate_count


def text_files_under(root: Path):
    if not root.exists():
        return
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        action="store_true",
        help="also normalize WCCM generator/workflow sources in the repository",
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="normalize only the Netlify publish directory (default behavior)",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    publish = repo / "wccm-corporate"
    if not publish.exists():
        raise SystemExit(f"Publish directory not found: {publish}")

    replacement_count = 0
    changed_files = 0

    for p in text_files_under(publish):
        n = replace_domain(p)
        if n:
            replacement_count += n
            changed_files += 1

    contact_changed = normalize_contact_entity(publish / "contact.html")
    if contact_changed:
        changed_files += contact_changed

    if args.source:
        candidates = [
            repo / "gen_city_pages.py",
            repo / "gen_geo_pages.py",
            repo / "flagship_detail.py",
            repo / "flagship_data.json",
            repo / "ping_indexnow.py",
        ]
        candidates.extend((repo / "tools").glob("*.py"))
        candidates.extend((repo / ".github" / "workflows").glob("*.yml"))
        candidates.extend((repo / ".github" / "workflows").glob("*.yaml"))
        for p in candidates:
            if p.resolve() == Path(__file__).resolve():
                continue
            n = replace_domain(p)
            if n:
                replacement_count += n
                changed_files += 1

    rule_count, duplicate_count = clean_redirects(publish / "_redirects")

    # Hard guard: no retired short-domain SEO references may remain in the
    # published site except the intentional source host in _redirects.
    leftovers = []
    for p in text_files_under(publish):
        if p.name == "_redirects":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD in text:
            leftovers.append(str(p.relative_to(repo)))
    if leftovers:
        raise SystemExit("Old canonical domain remains in: " + ", ".join(leftovers))

    print(
        f"Canonical domain normalized: {replacement_count} domain replacements; "
        f"changed_files={changed_files}; contact={contact_changed}; "
        f"redirects={rule_count}; duplicates_removed={duplicate_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
