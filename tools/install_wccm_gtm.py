#!/usr/bin/env python3
"""Install WCCM tracking on production HTML documents.

The publish tree contains normal pages plus a few redirect/legacy .html stubs.
Normal documents receive GTM plus the Google Ads base tag. The Ads tag also
listens for the site's existing `wccm_lead_submit` dataLayer event and sends the
Google Ads `WCCM - Mortgage Lead` conversion only after a form was accepted.
Nonstandard stubs are skipped, while critical lead and paid-search pages are
explicitly required to contain both tracking layers.
"""
from __future__ import annotations

import re
from pathlib import Path

GTM_ID = "GTM-WDSXSS5Z"
GOOGLE_ADS_ID = "AW-18417657219"
GOOGLE_ADS_LEAD_DESTINATION = "AW-18417657219/LiA7CPWd4eocEIPLnM5E"
ADS_BLOCK_START = "<!-- Google tag (gtag.js) - Google Ads -->"
ADS_BLOCK_END = "<!-- End Google tag - Google Ads -->"

GTM_HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY_SNIPPET = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

GOOGLE_ADS_HEAD_SNIPPET = f"""{ADS_BLOCK_START}
<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_ADS_ID}"></script>
<script>
window.dataLayer=window.dataLayer||[];
window.gtag=window.gtag||function(){{window.dataLayer.push(arguments);}};

/* Direct WCCM lead conversion. Keep this conversion out of GTM unless this
   direct implementation is removed, so the same lead cannot be counted twice. */
(function(){{
  if(window.__wccmAdsLeadConversionHook)return;
  window.__wccmAdsLeadConversionHook=true;
  window.__wccmAdsLeadCursor=0;
  window.__wccmAdsLeadScanner=setInterval(function(){{
    var dl=window.dataLayer||[];
    while(window.__wccmAdsLeadCursor<dl.length){{
      var item=dl[window.__wccmAdsLeadCursor++];
      if(item&&item.event==='wccm_lead_submit'&&!item.__wccmAdsLeadSent){{
        item.__wccmAdsLeadSent=true;
        window.gtag('event','conversion',{{
          'send_to':'{GOOGLE_ADS_LEAD_DESTINATION}',
          'value':1.0,
          'currency':'USD'
        }});
      }}
    }}
  }},200);
}})();

window.gtag('js',new Date());
window.gtag('config','{GOOGLE_ADS_ID}');
</script>
{ADS_BLOCK_END}"""

HEAD_TAG_RE = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)
BODY_TAG_RE = re.compile(r"<body(?:\s[^>]*)?>", re.IGNORECASE)
GTM_ID_RE = re.compile(r"GTM-[A-Z0-9]+", re.IGNORECASE)
ADS_ID_RE = re.compile(r"AW-[0-9]+", re.IGNORECASE)

CRITICAL_PAGES = (
    "index.html",
    "bank-statement-loans.html",
    "self-employed-borrowers.html",
    "jumbo-loans.html",
    "dscr-loans.html",
    "loans/jumbo/los-angeles-county.html",
)


def replace_ads_block(text: str) -> tuple[str, bool]:
    """Install or upgrade the authoritative direct Google Ads block."""
    start = text.find(ADS_BLOCK_START)
    end = text.find(ADS_BLOCK_END)
    if start >= 0 and end >= start:
        end += len(ADS_BLOCK_END)
        existing = text[start:end]
        if existing == GOOGLE_ADS_HEAD_SNIPPET:
            return text, False
        return text[:start] + GOOGLE_ADS_HEAD_SNIPPET + text[end:], True

    marker = "<!-- End Google Tag Manager -->"
    pos = text.find(marker)
    if pos >= 0:
        pos += len(marker)
        return text[:pos] + "\n" + GOOGLE_ADS_HEAD_SNIPPET + text[pos:], True

    head = HEAD_TAG_RE.search(text)
    if not head:
        return text, False
    return text[: head.end()] + "\n" + GOOGLE_ADS_HEAD_SNIPPET + text[head.end() :], True


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

    # Never silently install alongside a different direct Google Ads tag.
    if "googletagmanager.com/gtag/js" in text:
        ads_ids = {m.upper() for m in ADS_ID_RE.findall(text)}
        if ads_ids and GOOGLE_ADS_ID not in ads_ids:
            raise SystemExit(f"Conflicting Google Ads tag(s) in {path}: {sorted(ads_ids)}")

    changed = False
    if "googletagmanager.com/gtm.js" not in text:
        head = HEAD_TAG_RE.search(text)
        text = text[: head.end()] + "\n" + GTM_HEAD_SNIPPET + text[head.end() :]
        changed = True

    text, ads_changed = replace_ads_block(text)
    changed = changed or ads_changed

    if "googletagmanager.com/ns.html" not in text:
        body = BODY_TAG_RE.search(text)
        text = text[: body.end()] + "\n" + GTM_BODY_SNIPPET + text[body.end() :]
        changed = True

    required = (
        GTM_ID,
        "googletagmanager.com/gtm.js",
        "googletagmanager.com/ns.html",
        GOOGLE_ADS_ID,
        f"gtag/js?id={GOOGLE_ADS_ID}",
        GOOGLE_ADS_LEAD_DESTINATION,
        "wccm_lead_submit",
    )
    if not all(token in text for token in required):
        raise SystemExit(f"Tracking verification failed for {path}")

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed, None


def verify_critical(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Critical WCCM page missing: {path}")
    text = path.read_text(encoding="utf-8")
    required = (
        GTM_ID,
        "googletagmanager.com/gtm.js",
        "googletagmanager.com/ns.html",
        GOOGLE_ADS_ID,
        f"gtag/js?id={GOOGLE_ADS_ID}",
        GOOGLE_ADS_LEAD_DESTINATION,
        "wccm_lead_submit",
    )
    if not all(token in text for token in required):
        raise SystemExit(f"Critical WCCM page is not fully instrumented: {path}")


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
        f"WCCM tracking GTM={GTM_ID} Ads={GOOGLE_ADS_ID}: "
        f"verified={installed_docs}, changed={changed}, "
        f"non_document_stubs={skipped_non_document}, "
        f"nonstandard_stubs={skipped_nonstandard}, "
        f"critical_pages={len(CRITICAL_PAGES)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())