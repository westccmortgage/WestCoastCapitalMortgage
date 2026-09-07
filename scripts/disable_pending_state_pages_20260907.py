from pathlib import Path
import re, sys, json, xml.etree.ElementTree as ET

ROOT=Path('wccm-corporate')
PAGES=['washington-mortgage-loans.html','new-york-long-island-mortgage-loans.html']
URLS=['https://westcoastcapitalmortgage.com/washington-mortgage-loans','https://westcoastcapitalmortgage.com/new-york-long-island-mortgage-loans']
PRODUCTS=['jumbo-loans.html','self-employed-borrowers.html','bank-statement-loans.html','non-qm-loans.html','dscr-loans.html','investment-property-loans.html']

for name in PAGES:
    p=ROOT/name
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'<meta name="robots" content="[^"]*">','<meta name="robots" content="noindex,nofollow">',s,count=1)
    notice='<section class="bg-light"><div class="wrap"><div class="card"><h2>State Licensing Status</h2><p><strong>West Coast Capital Mortgage Inc. is not currently offering mortgage financing in this state.</strong> This page is retained for future use while licensing/approval is pending. Current mortgage services are offered only where West Coast Capital Mortgage Inc. is properly licensed and authorized.</p></div></div></section>'
    if 'State Licensing Status' not in s:
        s=s.replace('<section><div class="wrap">',notice+'<section><div class="wrap">',1)
    p.write_text(s,encoding='utf-8')

# Remove state pages from sitemap.
sp=ROOT/'sitemap.xml'
s=sp.read_text(encoding='utf-8')
for u in URLS:
    s=re.sub(r'\s*<url>\s*<loc>'+re.escape(u)+r'</loc>.*?</url>','',s,flags=re.S)
sp.write_text(s,encoding='utf-8')

# Remove contextual links/blocks from product pages, regardless of wrapper wording.
for name in PRODUCTS:
    p=ROOT/name
    s=p.read_text(encoding='utf-8')
    # remove anchor tags to either state page
    for href in ['washington-mortgage-loans.html','new-york-long-island-mortgage-loans.html','/washington-mortgage-loans','/new-york-long-island-mortgage-loans']:
        s=re.sub(r'<a\b[^>]*href="'+re.escape(href)+r'"[^>]*>.*?</a>','',s,flags=re.S|re.I)
    # clean empty separators left by prior state link blocks
    s=s.replace(' ·  · ',' · ').replace('||','')
    p.write_text(s,encoding='utf-8')

# Validation
errors=[]
for name in PAGES:
    s=(ROOT/name).read_text(encoding='utf-8')
    if '<meta name="robots" content="noindex,nofollow">' not in s: errors.append(name+': noindex missing')
    if 'State Licensing Status' not in s: errors.append(name+': licensing notice missing')
for u in URLS:
    if u in sp.read_text(encoding='utf-8'): errors.append('sitemap still contains '+u)
for name in PRODUCTS:
    s=(ROOT/name).read_text(encoding='utf-8')
    if 'washington-mortgage-loans' in s or 'new-york-long-island-mortgage-loans' in s: errors.append(name+': state link remains')
try: ET.parse(sp)
except Exception as e: errors.append('sitemap XML invalid: '+str(e))
for name in PAGES:
    s=(ROOT/name).read_text(encoding='utf-8')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: json.loads(m.group(1))
        except Exception as e: errors.append(name+': JSON-LD invalid '+str(e))
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('PASS: pending WA/NY pages retained but disabled, de-indexed, de-linked, and removed from sitemap')
