#!/usr/bin/env python3
"""Normalize the public WCCM site to the current WWCCM.ai mortgage-review brand.

Several older generated county/service pages still contain the retired
WCCI.Online name and wcci.online destination. Netlify runs this script against
wccm-corporate immediately before publish so answer engines and borrowers see
one consistent AI-review brand and destination across the primary WCCM site.
"""
from pathlib import Path

PUBLISH_DIR = Path(__file__).resolve().parents[1] / "wccm-corporate"

REPLACEMENTS = (
    ("https://wcci.online", "https://wwccm.ai"),
    ("http://wcci.online", "https://wwccm.ai"),
    ("WCCI.Online", "WWCCM.ai"),
    ("WCCI AI Mortgage Review", "WWCCM.ai AI Mortgage Review"),
)


def main() -> int:
    if not PUBLISH_DIR.exists():
        raise SystemExit(f"Publish directory not found: {PUBLISH_DIR}")

    changed_files = 0
    replacements = 0

    for path in PUBLISH_DIR.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count:
                replacements += count
                text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1

    leftovers = []
    retired_markers = ("WCCI.Online", "wcci.online", "WCCI AI Mortgage Review")
    for path in PUBLISH_DIR.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if any(marker in text for marker in retired_markers):
            leftovers.append(str(path.relative_to(PUBLISH_DIR)))

    if leftovers:
        raise SystemExit(
            "Retired WCCI AI-review branding remains in published HTML: "
            + ", ".join(leftovers)
        )

    print(
        "AI review brand normalized: "
        f"replacements={replacements}; changed_files={changed_files}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
