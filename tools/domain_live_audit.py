#!/usr/bin/env python3
import csv
import hashlib
import json
import re
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests

DOMAINS = ['ananasikpsy.com', 'beforejumboloan.com', 'beforejumboloans.com', 'belairfinancing.com', 'boutiquemtg.com', 'browardcountymortgage.com', 'caboutiquemortgage.com', 'caboutiquemtg.com', 'cadeed.com', 'californiaboutiquemtg.com', 'californiamtg.com', 'californiardp.com', 'calirdp.com', 'cawccmortgage.com', 'cawccmtg.com', 'cawestccmortgage.com', 'cawestmortgage.com', 'floridasunmortgage.com', 'grcrm.com', 'kwestloans.com', 'kwestmortgages.com', 'kwmtg.com', 'lenderscapitalmortgage.com', 'lunadabayhome.com', 'lunadabayloan.com', 'lunadabaymortgage.com', 'lunadabayrealestate.com', 'markevita.com', 'miamidadecountymortgage.com', 'miamidademortgage.com', 'monroecountymortgage.com', 'mortgagesouthbay.com', 'mtgcn.com', 'orangesmortgages.com', 'ourmtg.com', 'pacificpalisadestownhomes.com', 'palmbeachcountymortgage.com', 'pegascn.com', 'pegascnet.com', 'pegasuscapital.network', 'pegasuscapitalnetwork.com', 'pegasuscnet.com', 'pegasuscng.com', 'pegasusprivatenetwork.com', 'pornhubcrm.com', 'privatedeedcapital.com', 'privatenotecapital.com', 'sccmotgage.com', 'seattlemtg.com', 'southbayloans.com', 'southbaymtg.com', 'sunccmortgage.com', 'suncoastcapitalmortgage.com', 'walletwccm.com', 'washingtonmtg.com', 'wawccm.com', 'wawestccmortgage.com', 'wawestccmtg.com', 'wawestmortgage.com', 'wcci.online', 'westccmortgage.com', 'westccmtg.com', 'westcoastcapitalinvestment.com', 'westcoastcapitalmortgage.com', 'wwccm.ai', 'wwccm.com', 'cawccm.com', 'vistadelmartownhomes.com', 'pegasuslendersgroup.com', 'pegasuscapitalmortgage.com', 'pegasuslenders.com', 'sunstatecapitalmortgage.com', '90210estate.com', 'measureddecisionai.com', 'measureddecision.com', 'southbayestate.com', 'westccrealty.com', 'westcoastcapitalrealty.com']
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WCCM-Domain-Audit/1.2)"}
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
PARK = (
    "domain for sale",
    "buy this domain",
    "afternic",
    "sedo",
    "godaddy.com/forsale",
    "domain expired",
    "coming soon",
)

class CanonicalParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.href = ""

    def handle_starttag(self, tag, attrs):
        if self.href or tag.lower() != "link":
            return
        data = {str(k).lower(): (v or "") for k, v in attrs}
        rel_tokens = data.get("rel", "").lower().split()
        if "canonical" in rel_tokens and data.get("href"):
            self.href = data["href"].strip()

def clean_html(value):
    return WS_RE.sub(" ", TAG_RE.sub(" ", value or "")).strip()

def canonical_from(text, base):
    parser = CanonicalParser()
    try:
        parser.feed(text or "")
    except Exception:
        return ""
    return urljoin(base, parser.href)[:500] if parser.href else ""

def fetch(url, follow):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=(7, 25),
        allow_redirects=follow,
        verify=True,
    )
    content_type = response.headers.get("content-type", "").lower()
    text = response.text[:1_000_000] if ("text" in content_type or "html" in content_type) else ""
    title_match = TITLE_RE.search(text)
    title = clean_html(title_match.group(1))[:300] if title_match else ""
    canonical = canonical_from(text, response.url)

    # Hash normalized visible text rather than raw HTML. This exposes clones
    # whose only differences are host-specific canonical/analytics markup.
    visible = clean_html(text[:500_000])
    visible_normalized = visible.lower()
    body_hash = (
        hashlib.sha256(visible_normalized.encode("utf-8", "replace")).hexdigest()
        if visible_normalized
        else ""
    )

    return {
        "status": response.status_code,
        "url": response.url,
        "redirects": len(response.history),
        "location": response.headers.get("location", "") if not follow else "",
        "chain": [
            {
                "status": item.status_code,
                "url": item.url,
                "location": item.headers.get("location", ""),
            }
            for item in response.history
        ],
        "title": title,
        "canonical": canonical,
        "parked": any(marker in visible_normalized for marker in PARK),
        "content_type": response.headers.get("content-type", ""),
        "server": response.headers.get("server", ""),
        "body_sha256": body_hash,
        "visible_chars": len(visible),
    }

def audit(domain):
    row = {
        "domain": domain,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
        }
        row["ips"] = ",".join(sorted(addresses)[:8])
        row["dns_ok"] = True
    except Exception as exc:
        row.update(
            dns_ok=False,
            ips="",
            classification="NO_DNS",
            error=str(exc),
        )
        return row

    errors = []
    attempts = [
        ("https", f"https://{domain}/"),
        ("www", f"https://www.{domain}/"),
        ("http", f"http://{domain}/"),
    ]
    for label, url in attempts:
        try:
            initial = fetch(url, False)
            final = fetch(url, True)
            row.update(
                tested_url=url,
                initial_status=initial["status"],
                initial_location=initial["location"],
                final_status=final["status"],
                redirect_count=final["redirects"],
                final_url=final["url"],
                final_host=urlparse(final["url"]).hostname or "",
                title=final["title"],
                canonical=final["canonical"],
                parked=final["parked"],
                body_sha256=final["body_sha256"],
                visible_chars=final["visible_chars"],
                chain=json.dumps(final["chain"], ensure_ascii=False),
                content_type=final["content_type"],
                server=final["server"],
                error="",
            )

            if label == "https":
                if final["redirects"] and final["status"] < 400:
                    classification = "HTTPS_REDIRECT_OK"
                elif final["status"] == 200:
                    classification = "HTTPS_200_PARKED" if final["parked"] else "HTTPS_200"
                elif final["status"] in (401, 403):
                    classification = "HTTPS_RESTRICTED"
                else:
                    classification = f"HTTPS_{final['status']}"
            elif label == "www":
                classification = "ROOT_HTTPS_FAIL_WWW_WORKS"
            else:
                classification = (
                    "HTTP_REDIRECT_OK_HTTPS_FAIL"
                    if final["redirects"] and final["status"] < 400
                    else "HTTP_ONLY"
                )
            row["classification"] = classification
            return row
        except Exception as exc:
            errors.append(f"{label}: {type(exc).__name__}: {exc}")

    row.update(
        classification="HTTPS_ERROR",
        error=" | ".join(errors),
    )
    return row

def main():
    rows = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(audit, domain): domain for domain in DOMAINS}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(
                row["domain"],
                row.get("classification"),
                row.get("final_url", ""),
                flush=True,
            )

    order = {domain: index for index, domain in enumerate(DOMAINS)}
    rows.sort(key=lambda row: order[row["domain"]])

    Path("domain_live_audit.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    fields = [
        "domain",
        "checked_at_utc",
        "dns_ok",
        "ips",
        "classification",
        "tested_url",
        "initial_status",
        "initial_location",
        "final_status",
        "redirect_count",
        "final_url",
        "final_host",
        "title",
        "canonical",
        "parked",
        "body_sha256",
        "visible_chars",
        "content_type",
        "server",
        "error",
        "chain",
    ]
    with open("domain_live_audit.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})

    counts = {}
    for row in rows:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1
    print("SUMMARY", json.dumps(counts, sort_keys=True))

if __name__ == "__main__":
    from pathlib import Path
    main()
