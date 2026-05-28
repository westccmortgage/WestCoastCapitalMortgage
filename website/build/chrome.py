# Shared chrome: head, header, footer, chat. Imported by build.py
PHONE = "(310) 654-1577"
PHONE_TEL = "+13106541577"
NMLS = "NMLS# 2775380"
COMPANY = "West Coast Capital Mortgage"

def head(title, desc, active=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {COMPANY}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body data-page="{active}">
"""

NAV_LINKS = [
    ("index.html", "Home", "home"),
    ("#programs", "Loan Programs", "programs"),  # dropdown
    ("calculators.html", "Calculators", "calc"),
    ("about.html", "About", "about"),
    ("reviews.html", "Reviews", "reviews"),
    ("blog.html", "Blog", "blog"),
    ("contact.html", "Contact", "contact"),
]

PROGRAMS = [
    ("conventional.html", "Conventional", "🏠"),
    ("fha.html", "FHA Loans", "🔑"),
    ("va.html", "VA Loans", "🎖️"),
    ("usda.html", "USDA Loans", "🌾"),
    ("jumbo.html", "Jumbo Loans", "💎"),
    ("fixed-rate.html", "Fixed-Rate", "📈"),
    ("refinance.html", "Refinance", "🔁"),
    ("renovation-203k.html", "Renovation 203(k)", "🔨"),
    ("reverse.html", "Reverse Mortgage", "🌅"),
]

def header(active=""):
    sub = "".join(f'<li><a href="{u}">{e} &nbsp;{n}</a></li>' for u,n,e in PROGRAMS)
    return f"""<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html">
      <img src="assets/img/logo.png" alt="West Coast Capital Mortgage logo">
      <span class="bt"><b>West Coast Capital</b><span>Mortgage Inc.</span></span>
    </a>
    <nav>
      <ul class="menu" id="menu">
        <li><a href="index.html">Home</a></li>
        <li class="has-sub"><a href="conventional.html">Loan Programs</a>
          <ul class="submenu">{sub}</ul>
        </li>
        <li><a href="calculators.html">Calculators</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="reviews.html">Reviews</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:{PHONE_TEL}">📞 <span>{PHONE}</span></a>
      <a class="btn btn-gold" href="apply.html">Apply Now</a>
      <button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>"""

def footer():
    prog = "".join(f'<a href="{u}">{n}</a>' for u,n,e in PROGRAMS[:6])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/img/logo.png" alt="West Coast Capital Mortgage">
        <b>West Coast Capital Mortgage Inc.</b>
        <p style="margin-top:10px">Honest guidance. Clear answers. Strong results — for homebuyers and homeowners across California, Florida & Washington.</p>
        <p><a href="tel:{PHONE_TEL}" style="color:var(--gold);display:inline;font-weight:700">{PHONE}</a></p>
      </div>
      <div>
        <h4>Loan Programs</h4>
        {prog}
      </div>
      <div>
        <h4>Company</h4>
        <a href="about.html">About the CEO</a>
        <a href="reviews.html">Client Reviews</a>
        <a href="blog.html">Mortgage Blog</a>
        <a href="calculators.html">Calculators</a>
        <a href="contact.html">Contact Us</a>
      </div>
      <div>
        <h4>Get Started</h4>
        <a href="apply.html">Apply Online</a>
        <a href="contact.html">Free Rate Quote</a>
        <a href="calculators.html">Estimate Payment</a>
        <a href="tel:{PHONE_TEL}">Call {PHONE}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span class="year"></span> West Coast Capital Mortgage Inc. · {NMLS}</span>
      <span>Licensed in CA · FL · WA</span>
    </div>
    <p class="legal">West Coast Capital Mortgage Inc. ({NMLS}) is an Equal Housing Lender. This is not a commitment to lend. All loans are subject to credit approval, income verification, and property appraisal. Rates and programs are subject to change without notice and are shown for illustrative purposes only — actual rates depend on credit profile, loan amount, down payment, occupancy, and property type. Calculator results are estimates and not an offer or guarantee of a loan. Equal Housing Opportunity.</p>
  </div>
</footer>"""

def chat():
    return """<button id="chat-fab" aria-label="Open chat">💬</button>
<div id="chat-panel" aria-live="polite">
  <div class="chat-head">
    <div class="av">🐎</div>
    <div><b>Mortgage Assistant</b><span>● Online now</span></div>
    <button class="x" id="chat-close" aria-label="Close">×</button>
  </div>
  <div class="chat-body" id="chat-body"></div>
  <div class="chat-quick">
    <button>Today's rates</button>
    <button>FHA loans</button>
    <button>How much can I afford?</button>
    <button>Get pre-approved</button>
  </div>
  <div class="chat-input">
    <input id="chat-text" type="text" placeholder="Ask about rates, programs…" autocomplete="off">
    <button id="chat-send" aria-label="Send">➤</button>
  </div>
</div>
<script src="assets/js/main.js"></script>
</body>
</html>"""

def page_hero(crumb, h1, sub):
    return f"""<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>"""

def cta_band():
    return f"""<section class="section"><div class="container">
  <div class="cta-band">
    <h2>Ready to take the next step?</h2>
    <p>Get a free, no-obligation rate quote or start your application in minutes. A licensed loan officer will guide you the whole way.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn-dark btn-lg" href="apply.html">Apply Now</a>
      <a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}" style="background:rgba(255,255,255,.7)">Call {PHONE}</a>
    </div>
  </div>
</div></section>"""
