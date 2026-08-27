#!/usr/bin/env python3
import csv, json, re, socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse
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
HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; WCCM-Domain-Audit/1.0)"}
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I|re.S)
CANON = re.compile(r'<link[^>]+(?:rel=["\']?canonical["\']?[^>]+href|href)=["\']([^"\']+)', re.I)
TAG = re.compile(r"<[^>]+>")
PARK = ("domain for sale","buy this domain","afternic","sedo","godaddy.com/forsale","domain expired","coming soon")

def clean(s):
    return re.sub(r"\s+"," ",TAG.sub(" ",s or "")).strip()

def fetch(url, follow):
    r = requests.get(url, headers=HEADERS, timeout=(7,25), allow_redirects=follow, verify=True)
    text = r.text[:1000000] if "text" in (r.headers.get("content-type","").lower()) or "html" in (r.headers.get("content-type","").lower()) else ""
    title = clean(TITLE.search(text).group(1))[:300] if TITLE.search(text) else ""
    cm = CANON.search(text)
    canon = cm.group(1).strip()[:500] if cm else ""
    low = clean(text[:250000]).lower()
    return {
        "status": r.status_code,
        "url": r.url,
        "redirects": len(r.history),
        "location": r.headers.get("location","") if not follow else "",
        "chain": [{"status":x.status_code,"url":x.url,"location":x.headers.get("location","")} for x in r.history],
        "title": title,
        "canonical": canon,
        "parked": any(x in low for x in PARK),
        "content_type": r.headers.get("content-type",""),
        "server": r.headers.get("server",""),
    }

def audit(domain):
    row = {"domain":domain,"checked_at_utc":datetime.now(timezone.utc).isoformat()}
    try:
        row["ips"] = ",".join(sorted({x[4][0] for x in socket.getaddrinfo(domain,443,type=socket.SOCK_STREAM)})[:8])
        row["dns_ok"] = True
    except Exception as e:
        row.update(dns_ok=False, ips="", classification="NO_DNS", error=str(e))
        return row
    attempts = [("https",f"https://{domain}/"),("www",f"https://www.{domain}/"),("http",f"http://{domain}/")]
    errors = []
    for label,url in attempts:
        try:
            initial = fetch(url,False)
            final = fetch(url,True)
            row.update(
                tested_url=url, initial_status=initial["status"], initial_location=initial["location"],
                final_status=final["status"], redirect_count=final["redirects"], final_url=final["url"],
                final_host=urlparse(final["url"]).hostname or "", title=final["title"],
                canonical=final["canonical"], parked=final["parked"], chain=json.dumps(final["chain"],ensure_ascii=False),
                content_type=final["content_type"], server=final["server"], error=""
            )
            if label=="https":
                if final["redirects"] and final["status"]<400: c="HTTPS_REDIRECT_OK"
                elif final["status"]==200: c="HTTPS_200_PARKED" if final["parked"] else "HTTPS_200"
                elif final["status"] in (401,403): c="HTTPS_RESTRICTED"
                else: c=f"HTTPS_{final['status']}"
            elif label=="www":
                c="ROOT_HTTPS_FAIL_WWW_WORKS"
            else:
                c="HTTP_REDIRECT_OK_HTTPS_FAIL" if final["redirects"] and final["status"]<400 else "HTTP_ONLY"
            row["classification"]=c
            return row
        except Exception as e:
            errors.append(f"{label}: {type(e).__name__}: {e}")
    row.update(classification="HTTPS_ERROR", error=" | ".join(errors))
    return row

def main():
    rows=[]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs={ex.submit(audit,d):d for d in DOMAINS}
        for f in as_completed(futs):
            r=f.result(); rows.append(r); print(r["domain"],r.get("classification"),r.get("final_url",""),flush=True)
    order={d:i for i,d in enumerate(DOMAINS)}; rows.sort(key=lambda r:order[r["domain"]])
    open("domain_live_audit.json","w",encoding="utf-8").write(json.dumps(rows,indent=2,ensure_ascii=False))
    fields=["domain","checked_at_utc","dns_ok","ips","classification","tested_url","initial_status","initial_location","final_status","redirect_count","final_url","final_host","title","canonical","parked","content_type","server","error","chain"]
    with open("domain_live_audit.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"") for k in fields})
    counts={}
    for r in rows:counts[r["classification"]]=counts.get(r["classification"],0)+1
    print("SUMMARY",json.dumps(counts,sort_keys=True))

if __name__=="__main__": main()
