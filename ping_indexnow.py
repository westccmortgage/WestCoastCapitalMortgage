#!/usr/bin/env python3
"""
ping_indexnow.py — submit westccmortgage.com URLs to IndexNow.

IndexNow pushes URLs into the discovery pipelines of Bing (which ChatGPT
Search leans on), Yandex, Seznam and Naver within hours instead of waiting
weeks for a recrawl. No account needed: ownership is proven by the key file
served at https://westccmortgage.com/<KEY>.txt.

Usage:
  python ping_indexnow.py            # submit every URL in the live sitemap
  python ping_indexnow.py URL [URL]  # submit specific URLs only

Run it after any deploy that adds or meaningfully changes pages.
"""
import json
import re
import sys
import urllib.request

HOST = "westccmortgage.com"
KEY = "6a526a773a4c41a5a4ded3a78dde63a9"          # served from wccm-corporate/<KEY>.txt
ENDPOINT = "https://api.indexnow.org/indexnow"


UA = "Mozilla/5.0 (compatible; wccm-indexnow-ping/1.0; +https://%s)" % HOST


def sitemap_urls():
    # Cloudflare 403s the default Python-urllib User-Agent, so send a real one.
    req = urllib.request.Request("https://%s/sitemap.xml" % HOST,
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        xml = r.read().decode("utf-8")
    return re.findall(r"<loc>(https://[^<]+)</loc>", xml)


def main():
    urls = sys.argv[1:] or sitemap_urls()
    if not urls:
        sys.exit("no URLs to submit")
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        print("submitted %d URLs -> HTTP %d %s" % (len(urls), r.status, r.reason))


if __name__ == "__main__":
    main()
