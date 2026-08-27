#!/usr/bin/env python3
"""Submit WCCM ecosystem growth URLs to IndexNow.

This is discovery acceleration for IndexNow-participating search engines. It does
not guarantee indexing or ranking. Each host has its own verification key file
at the site root. The script only submits URLs that are present in the live
sitemaps, so a repository change that has not deployed yet is skipped naturally.

Usage:
    python3 tools/ping_growth_indexnow.py
"""

import json
import re
import urllib.error
import urllib.request

ENDPOINT = "https://api.indexnow.org/indexnow"
UA = "Mozilla/5.0 (compatible; wccm-growth-indexnow/1.0; +https://westcoastcapitalmortgage.com)"

SITES = [
    {
        "host": "westcoastcapitalmortgage.com",
        "key": "6a526a773a4c41a5a4ded3a78dde63a9",
        "sitemaps": ["/growth-sitemap.xml"],
    },
    {
        "host": "californiamtg.com",
        "key": "feb7620d3421324937ae28c5a7a57f32",
        "sitemaps": ["/growth-sitemap.xml"],
    },
    {
        "host": "beforejumboloan.com",
        "key": "24a5c2bcdd3ab101ec9237ce4a595e10",
        "sitemaps": ["/sitemap.xml"],
    },
]


def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8"), response.status


def live_key(host, key):
    url = f"https://{host}/{key}.txt"
    try:
        text, status = get_text(url)
        return status == 200 and text.strip() == key
    except Exception as exc:
        print(f"SKIP {host}: verification key not live ({exc})")
        return False


def sitemap_urls(host, sitemap_paths):
    urls = []
    for path in sitemap_paths:
        url = f"https://{host}{path}"
        try:
            xml, _ = get_text(url)
            urls.extend(re.findall(r"<loc>\s*(https://[^<]+?)\s*</loc>", xml))
        except Exception as exc:
            print(f"SKIP sitemap {url}: {exc}")
    # only this exact host; preserve order, remove duplicates
    seen = set()
    clean = []
    prefix = f"https://{host}/"
    for url in urls:
        if not (url == f"https://{host}" or url.startswith(prefix)):
            continue
        if url not in seen:
            seen.add(url)
            clean.append(url)
    return clean


def submit(site):
    host = site["host"]
    key = site["key"]
    if not live_key(host, key):
        return

    urls = sitemap_urls(host, site["sitemaps"])
    if not urls:
        print(f"SKIP {host}: no live sitemap URLs found")
        return

    payload = json.dumps(
        {
            "host": host,
            "key": key,
            "keyLocation": f"https://{host}/{key}.txt",
            "urlList": urls,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"{host}: submitted {len(urls)} URLs -> HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        print(f"{host}: IndexNow HTTP {exc.code}: {exc.reason}")
    except Exception as exc:
        print(f"{host}: IndexNow submission failed: {exc}")


def main():
    for site in SITES:
        submit(site)


if __name__ == "__main__":
    main()
