#!/usr/bin/env python3
"""Install the WCCM Google Tag Manager container on production HTML documents.

The publish tree contains normal pages plus a few redirect/legacy .html stubs.
Normal documents receive both GTM snippets. Nonstandard stubs are skipped, while
critical lead and paid-search pages are explicitly required to contain GTM.
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


def inject(path: Path) -> tuple[bool, str | None]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()

    # Some legacy .html files are redirect/fragment stubs rather than documents.
    if "<html" not in lower and "<!doctype html" not in lower:
        return False, "non-document"

    head = HEAD_TAG_RE.search(text)
    body = BODY_TAG_RE.search(text)
    if not head or not body:
        return False, "nonstandard-document"

    # Never silently install alongside a different GTM container.
    if "googletagmanager.com/gtm.js" in text or "googletagmanager.com/ns.html" in text:
        ids = {m.upper() for m in GTM_ID_RE.findall(text)}
        if ids and ids != {GTM_ID}:
            raise SystemExit(f"Conflicting GTM container(s) in {path}: {sorted(ids)}")

    changed = False
    if "googletagmanager.com/gtm.js" not in text:
        text = text[: head.end()] + "\n" + HEAD_SNIPPET + text[head.end() :]
        changed = True

    if "googletagmanager.com/ns.html" not in text:
        body = BODY_TAG_RE.search(text)
        text = text[: body.end()] + "\n" + BODY_SNIPPET + text[body.end() :]
        changed = True

    required = (GTM_ID, "googletagmanager.com/gtm.js", "googletagmanager.com/ns.html")
    if not all(token in text for token in required):
        raise SystemExit(f"GTM verification failed for {path}")

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed, None


def verify_critical(path: Path) -> None:
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
    installed_docs = 0
    skipped_non_document = 0
    skipped_nonstandard = 0

    for page in pages:
        page_changed, skip_reason = inject(page)
        if skip_reason == "non-document":
            skipped_non_document += 1
            continue
        if skip_reason == "nonstandard-document":
            skipped_nonstandard += 1
            continue
        installed_docs += 1
        changed += int(page_changed)

    for rel in CRITICAL_PAGES:
        verify_critical(publish / rel)

    print(
        f"GTM {GTM_ID}: verified={installed_docs}, changed={changed}, "
        f"non_document_stubs={skipped_non_document}, "
        f"nonstandard_stubs={skipped_nonstandard}, "
        f"critical_pages={len(CRITICAL_PAGES)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
