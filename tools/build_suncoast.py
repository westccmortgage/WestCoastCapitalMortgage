#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sister generator for the Suncoast Capital Mortgage (Florida-facing) brand.

Suncoast is NOT a separate codebase. It REUSES West Coast Capital Mortgage's
page bodies, content builders, and JavaScript from build_site.py — editing a loan
page (or any inner page) in build_site.py updates BOTH brands. This file only
overrides the brand chrome (head / header / footer), the homepage, the About
page, and the color palette.

Run: python3 tools/build_suncoast.py   ->  writes ../suncoast-corporate (Netlify-ready)
"""

import os
import re
import shutil
import build_site as wc  # West Coast generator: shared bodies, builders, JS

# ---- shared facts (identical operating company — Suncoast is operated through WCCM) ----
APPLY_URL = wc.APPLY_URL          # https://2817729.my1003app.com/2775380/register
WCCI_URL = wc.WCCI_URL            # https://wcci.online
NMLS = wc.NMLS                    # 2817729
card = wc.card
card_ext = wc.card_ext

# Florida / Suncoast contact line (added to the shared West Coast contact block, Suncoast only).
FL_PHONE = "(561) 925-9444"
FL_TEL = "5619259444"


def contact_block(office_label="Office / Loan Officer Questions"):
    return (wc.contact_block(office_label) +
            f'<br><b>Florida / Suncoast Contact:</b> <a href="tel:{FL_TEL}">{FL_PHONE}</a>')

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "suncoast-corporate"))
SRC_ASSETS = os.path.join(os.path.dirname(wc.OUT), "wccm-corporate", "assets")

COMPLIANCE_BAR = ("Licensed &amp; operated under West Coast Capital Mortgage Inc. "
                  "&middot; NMLS #2817729 &middot; Equal Housing Lender &middot; Licensed in FL &amp; CA")
FOOTER_LEGAL = ("Suncoast Capital Mortgage is a Florida-facing mortgage brand experience operated through "
                "West Coast Capital Mortgage Inc. NMLS #2817729. Equal Housing Lender. Licensed in FL &amp; CA. "
                "Information is provided for educational purposes only and is not a commitment to lend. All loans "
                "are subject to credit, income, property, and underwriting approval.")

# ----------------------------------------------------------------------------
# Palette: remap West Coast's CSS variables to the Suncoast (navy + gold) system.
# Because the shared stylesheet is written entirely against CSS variables, swapping
# :root turns the whole site navy/professional. Gold (--sun) is then used only as a
# deliberate accent (hero CTA, hero glow, card top-borders) — never sitewide.
# ----------------------------------------------------------------------------
SUN_ROOT = """:root{
  --black:#1f2933;
  --charcoal:#0f2d4d;
  --white:#ffffff;
  --light:#f6f7f8;
  --gray:#667085;
  --border:#d9dee7;
  --blue:#16395f;
  --blue-dark:#0f2d4d;
  --navy:#16395f;
  --navy-dark:#0f2d4d;
  --sun:#f5a623;
  --sun-dark:#cf8410;
  --sun-soft:#fff4df;
  --sand:#f3e4c8;
  --cream:#fffaf1;
  --text:#1f2933;
  --muted:#667085;
  --max:1180px;
}"""

SUN_EXTRA = r"""
/* ===================== Suncoast brand layer ===================== */
.btn-sun{background:var(--sun);color:#1f2933;border-color:var(--sun)}
.btn-sun:hover{background:var(--sun-dark);border-color:var(--sun-dark);color:#fff}
.eyebrow.gold{color:var(--sun-dark)}
.bg-cream{background:var(--cream)}
.bg-sand{background:linear-gradient(180deg,var(--sun-soft),#fff)}

/* Compliance top bar (replaces utility links + language switch) */
.topbar.compliance .topbar-inner{justify-content:center;height:auto;min-height:40px;padding:7px 0;flex-wrap:wrap}
.compliance-text{font-size:.78rem;letter-spacing:.02em;color:#cdd8e6;text-align:center;line-height:1.5}

/* Brand logo with elegant sun mark */
.logo.brand{flex-direction:row;align-items:center;gap:12px}
.brand .sun{width:30px;height:30px;border-radius:50%;flex:none;
  background:radial-gradient(circle at 34% 30%,#ffd884,var(--sun) 68%);box-shadow:0 0 0 4px rgba(245,166,35,.16)}
.brand .brand-text{display:flex;flex-direction:column;line-height:1.04}
.logo .l2{color:var(--sun-dark)}
.footer-brand .l2{color:var(--sun)}

/* Warmer Florida hero */
.hero-sun{position:relative;overflow:hidden;color:#fff;padding:92px 0;
  background:linear-gradient(160deg,#16395f 0%,#0f2d4d 58%,#0c2542 100%)}
.hero-sun::before{content:"";position:absolute;top:-32%;right:-8%;width:660px;height:660px;border-radius:50%;
  background:radial-gradient(circle,rgba(245,166,35,.34),rgba(245,166,35,0) 62%);pointer-events:none}
.hero-sun .hero-wallpaper .wallpaper-line{color:rgba(255,255,255,.05)}
.hero-sun h1{color:#fff}
.hero-sun .lead{color:#d7e0ea;max-width:54ch}
.hero-sun .eyebrow{color:var(--sun)}
.hero-grid{position:relative;z-index:1;display:grid;grid-template-columns:1.08fr .92fr;gap:48px;align-items:center}
.hero-note{margin-top:22px;font-size:.82rem;color:#aab8c7;max-width:54ch;line-height:1.6}

/* Lead card */
.lead-card{background:#fff;color:var(--text);border-radius:16px;padding:30px 30px 26px;
  box-shadow:0 28px 64px rgba(0,0,0,.30);border-top:4px solid var(--sun)}
.lead-card h3{margin:0 0 4px;color:var(--navy)}
.lead-card .sub{color:var(--gray);font-size:.92rem;margin:0 0 18px}
.lead-card .field{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.lead-card label{font-size:.76rem;font-weight:600;color:var(--gray)}
.lead-card input,.lead-card select{width:100%;padding:11px 13px;border:1px solid var(--border);border-radius:8px;
  font:inherit;font-size:.95rem;background:#fff;color:var(--text)}
.lead-card input:focus,.lead-card select:focus{outline:2px solid var(--sun);border-color:var(--sun)}
.lead-card .btn{width:100%;margin-top:6px}
.lead-card .fineprint{font-size:.72rem;color:var(--gray);margin:12px 0 0;text-align:center;line-height:1.5}

/* Informational (non-link) cards keep the card look without hover-lift */
.card.info{cursor:default}
.card.info:hover{transform:none;box-shadow:none}
.card.info .label{color:var(--sun-dark)}

.footer-grid.suncoast{grid-template-columns:1.5fr 1fr 1.25fr 1fr 1.3fr}
@media(max-width:1040px){.footer-grid.suncoast{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.footer-grid.suncoast{grid-template-columns:1fr 1fr}}
@media(max-width:920px){.hero-grid{grid-template-columns:1fr;gap:34px}}
"""

CSS = re.sub(r":root\{.*?\}", SUN_ROOT, wc.CSS, count=1, flags=re.S) + SUN_EXTRA

# ----------------------------------------------------------------------------
# Brand chrome
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("index.html", "Home", "home"),
    ("buy.html", "Buy a Home", "buy"),
    ("refinance.html", "Refinance", "refinance"),
    ("loans.html", "Loans", "loans"),
    ("resources.html", "Resources", "resources"),
    ("about.html", "About", "about"),
    ("apply.html", "Apply", "apply"),
]

# Map each generated file to the nav key it should highlight.
ACTIVE = {"index.html": "home", "apply.html": "apply", "buy.html": "buy",
          "refinance.html": "refinance", "loans.html": "loans", "about.html": "about"}


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Suncoast Capital Mortgage</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>"""


def header(active):
    def navlink(href, label, key):
        cls = ' class="active"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    links = "".join(navlink(h, l, k) for h, l, k in NAV_ITEMS)
    return f"""
<div class="topbar compliance">
  <div class="wrap topbar-inner">
    <span class="compliance-text">{COMPLIANCE_BAR}</span>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo brand" href="index.html" aria-label="Suncoast Capital Mortgage home">
      <span class="sun" aria-hidden="true"></span>
      <span class="brand-text">
        <span class="l1">SUNCOAST CAPITAL</span>
        <span class="l2">MORTGAGE</span>
      </span>
    </a>
    <div class="nav-collapse" id="navc">
      <nav class="mainnav" aria-label="Primary">{links}</nav>
      <div class="header-cta">
        <a class="btn btn-sun" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Now</a>
      </div>
    </div>
    <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navc">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>"""


def footer():
    def col(title, items):
        def fl(t, h):
            if h.startswith("http"):
                return f'<a href="{h}" target="_blank" rel="noopener noreferrer">{t}</a>'
            return f'<a href="{h}">{t}</a>'
        return f'<div><h4>{title}</h4>{"".join(fl(t, h) for t, h in items)}</div>'
    cols = "".join([
        f'<div class="footer-brand"><div class="l1">SUNCOAST CAPITAL</div><div class="l2">MORTGAGE</div>'
        f'<p style="color:#aab2bd;font-size:.9rem">A Florida-facing mortgage experience, operated through '
        f'West Coast Capital Mortgage Inc.</p>'
        f'<p class="footer-contact">{contact_block()}</p></div>',
        col("Explore", [("Buy a Home", "buy.html"), ("Refinance", "refinance.html"), ("Loans", "loans.html")]),
        col("Resources", [("Resources", "resources.html"), ("Calculators", "calculators.html"),
            ("Mortgage Articles", "mortgage-articles.html"), ("Mortgage Glossary", "glossary.html"),
            ("FAQ", "faq.html")]),
        col("Company", [("About", "about.html"), ("Contact", "contact.html"), ("Apply Now", APPLY_URL)]),
        col("Mortgage Review", [("WCCI.Online AI Mortgage Review", WCCI_URL)]),
    ])
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid suncoast">{cols}</div>
    <div class="footer-bottom">
      <div class="row">
        <span class="eho">&#8962; Equal Housing Lender</span>
        <a href="https://www.nmlsconsumeraccess.org/" target="_blank" rel="noopener noreferrer" style="display:inline">NMLS Consumer Access</a>
      </div>
      <p>{FOOTER_LEGAL}</p>
      <p>&copy; 2026 Suncoast Capital Mortgage. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="script.js"></script>
</body>
</html>"""


def page(title, desc, active, body):
    return head(title, desc) + header(active) + body + footer()


# ----------------------------------------------------------------------------
# Suncoast homepage
# ----------------------------------------------------------------------------
def info_card(label, h, body):
    return (f'<div class="card info"><span class="label">{label}</span>'
            f'<h3>{h}</h3><p>{body}</p></div>')


def _home():
    powered = "".join([
        info_card("Florida-Focused", "Florida-Focused Mortgage Support",
                  "Guidance for Florida buyers, homeowners, investors, and self-employed borrowers."),
        info_card("The Platform", "West Coast Capital Mortgage Platform",
                  "Applications, tools, resources, and mortgage workflows are powered through West Coast Capital Mortgage Inc."),
        info_card("Licensed Review", "Licensed Mortgage Review",
                  "Mortgage options are subject to borrower qualification, documentation, property review, and underwriting approval."),
    ])
    options = "".join([
        card("Purchase", "Primary Residence Purchase", "Financing to buy your Florida primary residence with confidence.", "Learn more", "buy.html"),
        card("Refinance", "Refinance", "Lower your rate, shorten your term, or access equity.", "Learn more", "refinance.html"),
        card("Jumbo", "Jumbo Loans", "Financing above conforming limits for higher-priced Florida homes.", "Learn more", "jumbo-loans.html"),
        card("FHA / VA", "FHA / VA Loans", "Low-down-payment and $0-down options for eligible borrowers.", "Learn more", "fha-loans.html"),
        card("Self-Employed", "Self-Employed Borrowers", "Programs built around how business owners actually earn.", "Learn more", "self-employed-borrowers.html"),
        card("Bank Statement", "Bank Statement Loans", "Qualify using bank deposits instead of tax-return income.", "Learn more", "bank-statement-loans.html"),
        card("DSCR", "DSCR Investor Loans", "Qualify investment properties on rental cash flow.", "Learn more", "dscr-loans.html"),
        card("Investors", "Investment Property Loans", "Financing built for rentals, second homes, and portfolios.", "Learn more", "investment-property-loans.html"),
    ])
    return f"""
<section class="hero-sun">
  <div class="hero-wallpaper" aria-hidden="true">
    <div class="wallpaper-line" style="top:6%">SUNCOAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w2" style="top:40%">SUNCOAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w3" style="top:74%">SUNCOAST CAPITAL MORTGAGE</div>
  </div>
  <div class="wrap hero-inner">
    <span class="eyebrow">Florida Mortgage Guidance</span>
    <h1>Your Florida Home Loan Starts Here</h1>
    <p class="lead">Suncoast Capital Mortgage helps Florida buyers, homeowners, investors, and self-employed borrowers explore mortgage options through West Coast Capital Mortgage Inc.</p>
    <div class="btn-row">
      <a class="btn btn-lg btn-sun" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Online</a>
      <a class="btn btn-lg btn-outline-light" href="calculators.html">View Mortgage Tools</a>
      <a class="btn btn-lg btn-outline-light" href="{WCCI_URL}" target="_blank" rel="noopener noreferrer">Talk to AI</a>
    </div>
    <p class="hero-note">Applications are processed through West Coast Capital Mortgage Inc. AI review opens WCCI.Online in a separate secure experience.</p>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow gold">Powered by West Coast</span>
  <h2>Florida-focused guidance, backed by West Coast Capital Mortgage.</h2>
  <p class="lead">Suncoast Capital Mortgage gives Florida borrowers a warmer local entry point while using the same mortgage platform, application process, educational resources, and licensed review structure operated through West Coast Capital Mortgage Inc.</p></div>
  <div class="grid grid-3">{powered}</div>
</div></section>

<section class="bg-sand"><div class="wrap">
  <div class="section-head"><span class="eyebrow gold">Programs</span><h2>Mortgage options for Florida borrowers</h2>
  <p class="lead">From first-time buyers to seasoned investors and self-employed borrowers &mdash; find the program built around your situation.</p></div>
  <div class="grid grid-4">{options}</div>
</div></section>

<section><div class="wrap">
  <div class="founder-grid founder-preview">
    <div class="founder-photo"><img src="assets/anatoliy-kanevsky.png" alt="Anatoliy Kanevsky" loading="lazy"></div>
    <div>
      <span class="eyebrow gold">Our founder</span>
      <h2>Mortgage guidance with real estate experience.</h2>
      <p class="lead">Suncoast Capital Mortgage is connected to the broader West Coast Capital Mortgage platform led by Anatoliy Kanevsky, a mortgage and real estate professional with experience across lending, brokerage, luxury residential development, and complex borrower scenarios.</p>
      <a class="btn btn-sun" href="about.html#anatoliy">Meet Anatoliy</a>
    </div>
  </div>
</div></section>

<section class="bg-cream"><div class="wrap center">
  <span class="eyebrow gold">Talk to us</span>
  <h2>Speak with Suncoast Capital Mortgage</h2>
  <p class="contact-lines" style="font-size:1.05rem">{contact_block("Office")}</p>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <span class="eyebrow" style="color:var(--sun)">Florida Mortgage Guidance</span>
  <h2>Ready to start your Florida mortgage?</h2>
  <p>Apply online in minutes, or review your scenario first &mdash; both are handled through West Coast Capital Mortgage Inc. and related secure platforms.</p>
  <div class="btn-row">
    <a class="btn btn-lg btn-sun" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Online</a>
    <a class="btn btn-lg btn-outline-light" href="{WCCI_URL}" target="_blank" rel="noopener noreferrer">Review My Scenario</a>
  </div>
</div></div></section>
"""


# ----------------------------------------------------------------------------
# Suncoast About page
# ----------------------------------------------------------------------------
def _about():
    return wc.page_hero("About Suncoast Capital Mortgage",
        "A Florida-facing mortgage experience for borrowers who want clear guidance, modern tools, and professional mortgage support &mdash; connected to West Coast Capital Mortgage Inc.",
        "About") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow gold">Who we are</span>
    <h2>Florida guidance, West Coast platform</h2>
    <p class="lead">Suncoast Capital Mortgage was created as a Florida-facing mortgage experience for borrowers who want clear guidance, modern tools, and professional mortgage support. The platform is connected to West Coast Capital Mortgage Inc., allowing clients to access the same application process, mortgage resources, and licensed review structure.</p>
    <p class="muted">Serving borrowers where properly licensed. Equal Housing Lender. Licensed in FL &amp; CA.</p>
  </div>
  <ul class="feature-list">
    <li><b>Florida-focused</b><span>A warmer, local entry point for Florida borrowers.</span></li>
    <li><b>One platform</b><span>The same applications, tools, and resources as West Coast.</span></li>
    <li><b>Licensed review</b><span>Options subject to qualification and underwriting approval.</span></li>
    <li><b>Borrower-first</b><span>Clear answers, no pressure, modern tools.</span></li>
  </ul>
</div></section>
<section id="anatoliy"><div class="wrap">
  <div class="section-head"><span class="eyebrow gold">Founder &amp; Mortgage Professional</span><h2>Meet Anatoliy Kanevsky</h2></div>
  <div class="founder-grid">
    <div class="founder-photo"><img src="assets/anatoliy-kanevsky.png" alt="Anatoliy Kanevsky" loading="lazy"></div>
    <div>
      <p>Suncoast Capital Mortgage is connected to the broader West Coast Capital Mortgage platform led by Anatoliy Kanevsky, a mortgage and real estate professional with experience across lending, brokerage, luxury residential development, and complex borrower scenarios.</p>
      <p>His background combines mortgage lending, real estate brokerage, luxury residential development, and real-world deal analysis. That perspective allows Suncoast borrowers to access both lending discipline and practical real estate experience &mdash; all operated through West Coast Capital Mortgage Inc.</p>
      <p>Whether a Florida client is buying a primary residence, refinancing, purchasing a luxury property, financing an investment property, or exploring self-employed, Non-QM, jumbo, FHA, VA, or DSCR options, the focus is simple: clear guidance, smart structure, and a mortgage strategy that fits the client&rsquo;s actual situation.</p>
      <ul class="founder-cred">
        <li>California Real Estate Broker</li>
        <li>Mortgage professional since 2001</li>
        <li>Luxury real estate and development experience</li>
        <li>Purchase, refinance, jumbo, Non-QM, DSCR, and self-employed borrower strategy</li>
        <li>Founder, West Coast Capital Mortgage Inc.</li>
      </ul>
      <p class="founder-contact"><b>Anatoliy Direct:</b> <a href="tel:{wc.DIRECT_TEL}">{wc.DIRECT_PHONE}</a><br><b>Email:</b> <a href="mailto:{wc.EMAIL}">{wc.EMAIL}</a></p>
      <div class="btn-row" style="margin-top:18px"><a class="btn btn-sun" href="contact.html">Contact Anatoliy</a><a class="btn btn-outline" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Online</a></div>
    </div>
  </div>
</div></section>
<section class="bg-cream"><div class="wrap">
  <div class="section-head center"><span class="eyebrow gold">Why Suncoast</span><h2>Why Florida borrowers choose us</h2></div>
  <div class="grid grid-3">
    {card("","Mortgage solutions","Conventional, FHA, VA, jumbo, Non-QM, DSCR, and more.","See programs","loans.html")}
    {card("","Modern tools","Calculators and a short application to move quickly.","Try our tools","calculators.html")}
    {card("","Human guidance","Licensed professionals who explain every step.","Talk to us","contact.html")}
  </div>
  <p class="form-note center" style="margin-top:30px">Suncoast Capital Mortgage is a Florida-facing mortgage brand experience operated through West Coast Capital Mortgage Inc. NMLS #{NMLS}. Equal Housing Lender. Licensed in FL &amp; CA. This is not a commitment to lend. All loans are subject to credit, income, property, and underwriting approval.</p>
</div></div></section>
"""


def _notfound():
    return f"""
<section class="page-hero"><div class="wrap page-hero-inner center" style="margin:0 auto">
  <span class="eyebrow gold">404</span>
  <h1>Page not found</h1>
  <p class="lead" style="margin-left:auto;margin-right:auto">The page you are looking for may have moved or may no longer be available.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-lg btn-sun" href="index.html">Return Home</a>
    <a class="btn btn-lg btn-outline" href="resources.html">View Mortgage Resources</a>
    <a class="btn btn-lg btn-outline" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Online</a>
  </div>
</div></section>
"""


# ----------------------------------------------------------------------------
# Assemble: reuse every West Coast page body, override index + about, swap chrome.
# ----------------------------------------------------------------------------
def build_pages():
    pages = {}
    for name, p in wc.PAGES.items():
        # Suncoast has no "Find a Loan Officer" page (not in nav or footer per spec).
        # Repoint the shared West Coast CTA links to the contact page instead, and skip the page.
        if name == "loan-officer.html":
            continue
        body = p["body"].replace('href="loan-officer.html"', 'href="contact.html"')
        # Rebrand only the decorative all-caps wallpaper text (page_hero); mixed-case
        # "West Coast Capital Mortgage" prose stays — Suncoast is operated through WCCM.
        body = body.replace("WEST COAST CAPITAL MORTGAGE", "SUNCOAST CAPITAL MORTGAGE")
        # Add the Florida / Suncoast contact line wherever the shared contact block is rendered.
        body = body.replace(wc.contact_block(), contact_block())
        pages[name] = dict(title=p["title"], desc=p["desc"], nav=p.get("nav", ""), body=body)
    # Brand-specific overrides
    pages["index.html"] = dict(
        title="Florida Home Loans, Refinance & Mortgage Guidance",
        desc="Suncoast Capital Mortgage — a Florida-facing mortgage experience operated through West Coast Capital Mortgage Inc. Explore purchase, refinance, jumbo, FHA/VA, self-employed, bank statement, DSCR, and investment property options.",
        nav="home", body=_home())
    pages["404.html"] = dict(
        title="Page not found",
        desc="The page you are looking for may have moved or may no longer be available.",
        nav="", body=_notfound())
    pages["about.html"] = dict(
        title="About Suncoast Capital Mortgage",
        desc="Suncoast Capital Mortgage is a Florida-facing mortgage brand experience operated through West Coast Capital Mortgage Inc. NMLS #2817729. Equal Housing Lender. Licensed in FL & CA.",
        nav="about", body=_about().replace("WEST COAST CAPITAL MORTGAGE", "SUNCOAST CAPITAL MORTGAGE"))
    return pages


def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "styles.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(OUT, "script.js"), "w", encoding="utf-8") as f:
        f.write(wc.JS)  # shared, brand-neutral JS
    with open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8") as f:
        f.write("/*    /404.html    404\n")

    # Suncoast favicon: deep navy tile with a warm gold sun arc
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<rect width="64" height="64" rx="12" fill="#16395f"/>'
           '<circle cx="32" cy="34" r="11" fill="#f5a623"/>'
           '<g stroke="#f5a623" stroke-width="3" stroke-linecap="round">'
           '<line x1="32" y1="11" x2="32" y2="17"/><line x1="14" y1="34" x2="20" y2="34"/>'
           '<line x1="44" y1="34" x2="50" y2="34"/><line x1="19" y1="21" x2="23" y2="25"/>'
           '<line x1="45" y1="21" x2="41" y2="25"/></g></svg>')
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(fav)
    logo = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 64">'
            '<circle cx="20" cy="30" r="13" fill="#f5a623"/>'
            '<text x="44" y="26" font-family="Inter,Arial" font-size="19" font-weight="800" fill="#16395f">SUNCOAST CAPITAL</text>'
            '<text x="44" y="48" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="6" fill="#cf8410">MORTGAGE</text></svg>')
    with open(os.path.join(OUT, "assets", "logo.svg"), "w", encoding="utf-8") as f:
        f.write(logo)

    # Shared assets carried over from West Coast (founder photo, sample rates)
    for fn in ("anatoliy-kanevsky.png", "rates.json"):
        src = os.path.join(SRC_ASSETS, fn)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(OUT, "assets", fn))

    pages = build_pages()
    for name, p in pages.items():
        active = ACTIVE.get(name, p.get("nav", ""))
        html = page(p["title"], p["desc"], active, p["body"])
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Wrote {len(pages)} pages + styles.css + script.js + assets/ into {OUT}")


if __name__ == "__main__":
    main()
