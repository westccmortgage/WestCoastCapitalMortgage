#!/usr/bin/env python3
import csv, hashlib, json, re, socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin
import requests

DOMAINS = [
    "ananasikpsy.com",
    "beforejumboloan.com",
    "beforejumboloans.com",
    "belairfinancing.com",
    "boutiquemtg.com",
    "browardcountymortgage.com",
    "caboutiquemortgage.com",
    "caboutiquemtg.com",
    "cadeed.com",
    "californiaboutiquemtg.com",
    "californiamtg.com",
    "californiardp.com",
    "calirdp.com",
    "cawccmortgage.com",
    "cawccmtg.com",
    "cawestccmortgage.com",
    "cawestmortgage.com",
    "floridasunmortgage.com",
    "grcrm.com",
    "kwestloans.com",
    "kwestmortgages.com",
    "kwmtg.com",
    "lenderscapitalmortgage.com",
    "lunadabayhome.com",
    "lunadabayloan.com",
    "lunadabaymortgage.com",
    "lunadabayrealestate.com",
    "markevita.com",
    "miamidadecountymortgage.com",
    "miamidademortgage.com",
    "monroecountymortgage.com",
    "mortgagesouthbay.com",
    "mtgcn.com",
    "orangesmortgages.com",
    "ourmtg.com",
    "pacificpalisadestownhomes.com",
    "palmbeachcountymortgage.com",
    "pegascn.com",
    "pegascnet.com",
    "pegasuscapital.network",
    "pegasuscapitalnetwork.com",
    "pegasuscnet.com",
    "pegasuscng.com",
    "pegasusprivatenetwork.com",
    "pornhubcrm.com",
    "privatedeedcapital.com",
    "privatenotecapital.com",
    "sccmotgage.com",
    "seattlemtg.com",
    "southbayloans.com",
    "southbaymtg.com",
    "sunccmortgage.com",
    "suncoastcapitalmortgage.com",
    "walletwccm.com",
    "washingtonmtg.com",
    "wawccm.com",
    "wawestccmortgage.com",
    "wawestccmtg.com",
    "wawestmortgage.com",
    "wcci.online",
    "westccmortgage.com",
    "westccmtg.com",
    "westcoastcapitalinvestment.com",
    "westcoastcapitalmortgage.com",
    "wwccm.ai",
    "wwccm.com",
    "cawccm.com",
    "vistadelmartownhomes.com",
    "pegasuslendersgroup.com",
    "pegasuscapitalmortgage.com",
    "pegasuslenders.com",
    "sunstatecapitalmortgage.com",
    "90210estate.com",
    "measureddecisionai.com",
    "measureddecision.com",
    "southbayestate.com",
    "westccrealty.com",
    "westcoastcapitalrealty.com"
]
HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; WCCM-Domain-Audit/1.1)"}
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I|re.S)
LINK = re.compile(r"<link\b[^>]*>", re.I)
REL = re.compile(r"\brel\s*=\s*(["'])(.*?)\1", re.I|re.S)
HREF = re.compile(r"\bhref\s*=\s*(["'])(.*?)\1", re.I|re.S)
TAG = re.compile(r"<[^>]+>")
PARK = ("domain for sale","buy this domain","afternic","sedo","godaddy.com/forsale","domain expired","coming soon")

def clean(s):
    return re.sub(r"\s+"," ",TAG.sub(" ",s or "")).strip()

def canonical_from(text, base):
    for tag in LINK.findall(text or ""):
        rm=REL.search(tag)
        if not rm or "canonical" not in rm.group(2).lower().split():
            continue
        hm=HREF.search(tag)
        if hm:
            return urljoin(base, hm.group(2).strip())[:500]
    return ""

def fetch(url, follow):
    r = requests.get(url, headers=HEADERS, timeout=(7,25), allow_redirects=follow, verify=True)
    ctype=r.headers.get("content-type","").lower()
    text = r.text[:1000000] if ("text" in ctype or "html" in ctype) else ""
    tm=TITLE.search(text)
    title=clean(tm.group(1))[:300] if tm else ""
    canon=canonical_from(text,r.url)
    visible=clean(text[:500000])
    low=visible.lower()
    return {
        "status": r.status_code, "url": r.url, "redirects": len(r.history),
        "location": r.headers.get("location","") if not follow else "",
        "chain": [{"status":x.status_code,"url":x.url,"location":x.headers.get("location","")} for x in r.history],
        "title": title, "canonical": canon, "parked": any(x in low for x in PARK),
        "content_type": r.headers.get("content-type",""), "server": r.headers.get("server",""),
        "body_sha256": hashlib.sha256(text.encode("utf-8","replace")).hexdigest() if text else "",
        "visible_chars": len(visible),
    }

def audit(domain):
    row={"domain":domain,"checked_at_utc":datetime.now(timezone.utc).isoformat()}
    try:
        row["ips"]=",".join(sorted({x[4][0] for x in socket.getaddrinfo(domain,443,type=socket.SOCK_STREAM)})[:8]); row["dns_ok"]=True
    except Exception as e:
        row.update(dns_ok=False,ips="",classification="NO_DNS",error=str(e)); return row
    errors=[]
    for label,url in [("https",f"https://{domain}/"),("www",f"https://www.{domain}/"),("http",f"http://{domain}/")]:
        try:
            initial=fetch(url,False); final=fetch(url,True)
            row.update(
                tested_url=url,initial_status=initial["status"],initial_location=initial["location"],
                final_status=final["status"],redirect_count=final["redirects"],final_url=final["url"],
                final_host=urlparse(final["url"]).hostname or "",title=final["title"],canonical=final["canonical"],
                parked=final["parked"],body_sha256=final["body_sha256"],visible_chars=final["visible_chars"],
                chain=json.dumps(final["chain"],ensure_ascii=False),content_type=final["content_type"],
                server=final["server"],error=""
            )
            if label=="https":
                if final["redirects"] and final["status"]<400:c="HTTPS_REDIRECT_OK"
                elif final["status"]==200:c="HTTPS_200_PARKED" if final["parked"] else "HTTPS_200"
                elif final["status"] in (401,403):c="HTTPS_RESTRICTED"
                else:c=f"HTTPS_{final['status']}"
            elif label=="www":c="ROOT_HTTPS_FAIL_WWW_WORKS"
            else:c="HTTP_REDIRECT_OK_HTTPS_FAIL" if final["redirects"] and final["status"]<400 else "HTTP_ONLY"
            row["classification"]=c; return row
        except Exception as e:errors.append(f"{label}: {type(e).__name__}: {e}")
    row.update(classification="HTTPS_ERROR",error=" | ".join(errors)); return row

def main():
    rows=[]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs={ex.submit(audit,d):d for d in DOMAINS}
        for f in as_completed(futs):
            r=f.result();rows.append(r);print(r["domain"],r.get("classification"),r.get("final_url",""),flush=True)
    order={d:i for i,d in enumerate(DOMAINS)};rows.sort(key=lambda r:order[r["domain"]])
    open("domain_live_audit.json","w",encoding="utf-8").write(json.dumps(rows,indent=2,ensure_ascii=False))
    fields=["domain","checked_at_utc","dns_ok","ips","classification","tested_url","initial_status","initial_location","final_status","redirect_count","final_url","final_host","title","canonical","parked","body_sha256","visible_chars","content_type","server","error","chain"]
    with open("domain_live_audit.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"") for k in fields})
    counts={}
    for r in rows:counts[r["classification"]]=counts.get(r["classification"],0)+1
    print("SUMMARY",json.dumps(counts,sort_keys=True))

if __name__=="__main__":main()
