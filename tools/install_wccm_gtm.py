#!/usr/bin/env python3
"""Install the WCCM Google Tag Manager container on every full HTML document.

The WCCM publish tree also contains a few .html redirect/fragment stubs that are
not complete HTML documents. Those are intentionally skipped. Every full HTML
document must receive both GTM snippets, and critical paid-search pages are
verified explicitly so tracking cannot silently disappear.
"""
from __future__ import annotations

import re
from pathlib import Path

GTM_ID = "GTM-WDSXSS5Z"

HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

BODY_SNIPPET = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

HEAD_TAG_RE = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)
BODY_TAG_RE = re.compile(r"<body(?:\s[^>]*)?>", re.IGNORECASE)
GTM_ID_RE = re.compile(r"GTM-[A-Z0-9]+", re.IGNORECASE)

CRITICAL_PAGES = (
    "index.html",
    "bank-statement-loans.html",
    "self-employed-borrowers.html",
    "jumbo-loans.html",
    "dscr-loans.html",
    "loans/jumbo/los-angeles-county.html",
)


def is_full_html_document(text: str) -> bool:
    lower = text.lower()
    return "<html" in lower or "<!doctype html" in lower


def inject(path: Path) -> tuple[bool, bool]:
    text = path.read_text(encoding="utf-8")
    if not is_full_html_document(text):
        return False, True

    # Protect against accidentally running two different GTM containers on WCCM.
    if "googletagmanager.com/gtm.js" in text or "googletagmanager.com/ns.html" in text:
        ids = {m.upper() for m in GTM_ID_RE.findall(text)}
        if ids and ids != {GTM_ID}:
            raise SystemExit(f"Conflicting GTM container(s) in {path}: {sorted(ids)}")

    head = HEAD_TAG_RE.search(text)
    body = BODY_TAG_RE.search(text)
    if not head or not body:
        raise SystemExit(f"Malformed full HTML document (missing head/body): {path}")

    changed = False
    if "googletagmanager.com/gtm.js" not in text:
        text = text[: head.end()] + "\n" + HEAD_SNIPPET + text[head.end() :]
        changed = True

    if "googletagmanager.com/ns.html" not in text:
        body = BODY_TAG_RE.search(text)
        text = text[: body.end()] + "\n" + BODY_SNIPPET + text[body.end() :]
        changed = True

    if GTM_ID not in text or "googletagmanager.com/gtm.js" not in text or "googletagmanager.com/ns.html" not in text:
        raise SystemExit(f"GTM verification failed for {path}")

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed, False


def verify_page(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Critical WCCM page missing: {path}")
    text = path.read_text(encoding="utf-8")
    required = (GTM_ID, "googletagmanager.com/gtm.js", "googletagmanager.com/ns.html")
    if not all(token in text for token in required):
        raise SystemExit(f"Critical WCCM page is not GTM-instrumented: {path}")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    publish = repo / "wccm-corporate"
    pages = sorted(publish.rglob("*.html"))
    if not pages:
        raise SystemExit(f"No HTML pages found under {publish}")

    changed = 0
    skipped_stubs = 0
    full_docs = 0
    for page in pages:
        page_changed, skipped = inject(page)
        if skipped:
            skipped_stubs += 1
            continue
        full_docs += 1
        if page_changed:
            changed += 1

    for rel in CRITICAL_PAGES:
        verify_page(publish / rel)

    print(
        f"GTM {GTM_ID} verified on {full_docs} full WCCM HTML documents; "
        f"changed={changed}; non-document stubs skipped={skipped_stubs}; "
        f"critical_pages={len(CRITICAL_PAGES)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
