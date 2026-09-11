#!/usr/bin/env python3
"""Reject missing or damaged Clarity bootstraps on WCCM campaign pages."""
from pathlib import Path
import re

PROJECT_ID = "wzzlo9s35g"
REQUIRED_PAGES = {
    "bank-statement-loans.html", "self-employed-borrowers.html",
    "dscr-loans.html", "jumbo-loans.html", "florida-condo-financing.html",
    "foreign-national-loans.html", "investment-property-loans.html",
    "non-qm-loans.html",
}
SCRIPT_RE = re.compile(r"<script\b[^>]*>(.*?)</script\s*>", re.I | re.S)
EXPECTED = '''(function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "wzzlo9s35g");'''


def verify(publish: Path) -> int:
    errors = []
    verified = 0
    for name in sorted(REQUIRED_PAGES):
        if not (publish / name).is_file():
            errors.append(f"{name}: required page missing")
    for path in sorted(publish.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        blocks = [code for code in SCRIPT_RE.findall(text) if "clarity.ms/tag/" in code]
        required = path.relative_to(publish).as_posix() in REQUIRED_PAGES
        if not blocks and not required:
            continue
        if len(blocks) != 1 or re.sub(r"\s+", "", blocks[0]) != re.sub(r"\s+", "", EXPECTED):
            errors.append(f"{path.relative_to(publish)}: missing, duplicate or modified Clarity bootstrap")
        else:
            verified += 1
    if errors:
        raise SystemExit("Clarity verification failed:\n" + "\n".join(errors))
    print(f"Clarity {PROJECT_ID}: {verified} bootstraps verified; {len(REQUIRED_PAGES)} required pages")
    return verified


if __name__ == "__main__":
    verify(Path(__file__).resolve().parents[1] / "wccm-corporate")
