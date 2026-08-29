#!/usr/bin/env python3
"""Install the WCCM Google Tag Manager container on every published HTML page.

This runs during the Netlify build so generated pages cannot lose tracking on a
future rebuild. The operation is idempotent: existing correct snippets are kept
and missing head/body snippets are added exactly once.
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


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    # Protect against accidentally running two different GTM containers on WCCM.
    if "googletagmanager.com/gtm.js" in text or "googletagmanager.com/ns.html" in text:
        ids = {m.upper() for m in GTM_ID_RE.findall(text)}
        if ids and ids != {GTM_ID}:
            raise SystemExit(f"Conflicting GTM container(s) in {path}: {sorted(ids)}")

    changed = False

    if "googletagmanager.com/gtm.js" not in text:
        match = HEAD_TAG_RE.search(text)
        if not match:
            raise SystemExit(f"Missing <head> in published HTML: {path}")
        text = text[: match.end()] + "\n" + HEAD_SNIPPET + text[match.end() :]
        changed = True

    if "googletagmanager.com/ns.html" not in text:
        match = BODY_TAG_RE.search(text)
        if not match:
            raise SystemExit(f"Missing <body> in published HTML: {path}")
        text = text[: match.end()] + "\n" + BODY_SNIPPET + text[match.end() :]
        changed = True

    if GTM_ID not in text or "googletagmanager.com/gtm.js" not in text or "googletagmanager.com/ns.html" not in text:
        raise SystemExit(f"GTM verification failed for {path}")

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    publish = repo / "wccm-corporate"
    pages = sorted(publish.rglob("*.html"))
    if not pages:
        raise SystemExit(f"No HTML pages found under {publish}")

    changed = 0
    for page in pages:
        if inject(page):
            changed += 1

    print(f"GTM {GTM_ID} verified on {len(pages)} WCCM HTML pages; changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
