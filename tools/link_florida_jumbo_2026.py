#!/usr/bin/env python3
"""Keep the Florida hub pointed at the state-specific jumbo guide.

This is intentionally narrow and idempotent. It updates only the Florida jumbo
card and the existing Florida specialty-guide ItemList. It does not alter rates,
program terms, licensing, or any other state content.
"""
from pathlib import Path

PAGE = Path("wccm-corporate/florida.html")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Expected {label} marker not found in {PAGE}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    old_card = (
        '<a class="card" href="jumbo-loans.html"><span class="label">Higher loan amounts</span>'
        '<h3>Jumbo Loans</h3><p>Financing designed for higher-priced Florida properties and larger loan amounts.</p>'
        '<span class="more">Learn more &rarr;</span></a>'
    )
    new_card = (
        '<a class="card" href="florida-jumbo-loans.html"><span class="label">Higher loan amounts</span>'
        '<h3>Florida Jumbo Loans</h3><p>2026 state-specific jumbo guidance, including Florida county conforming thresholds and the Monroe County exception.</p>'
        '<span class="more">Florida jumbo guide &rarr;</span></a>'
    )
    text = replace_once(text, old_card, new_card, "Florida jumbo card")

    old_schema_tail = (
        '{"@type":"ListItem","position":4,"name":"Foreign National Loans for Florida Buyers",'
        '"url":"https://westcoastcapitalmortgage.com/foreign-national-loans"}]}</script>'
    )
    new_schema_tail = (
        '{"@type":"ListItem","position":4,"name":"Foreign National Loans for Florida Buyers",'
        '"url":"https://westcoastcapitalmortgage.com/foreign-national-loans"},'
        '{"@type":"ListItem","position":5,"name":"Florida Jumbo Loans 2026",'
        '"url":"https://westcoastcapitalmortgage.com/florida-jumbo-loans"}]}</script>'
    )
    text = replace_once(text, old_schema_tail, new_schema_tail, "Florida specialty-guide schema")

    PAGE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
