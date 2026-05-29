# Shared chrome: head, header, footer, chat, imagery. Imported by build scripts.
PHONE = "(310) 654-1577"
PHONE_TEL = "+13106541577"
NMLS = "NMLS# 2775380"
COMPANY = "West Coast Capital Mortgage"

# Royalty-free imagery (Unsplash CDN, free license) — loaded in the visitor's browser.
# Each is paired in CSS with a gradient fallback so nothing ever looks broken.
def u(pid, w=1400):
    return f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w={w}&q=80"

IMG = {
    "hero":      u("photo-1600596542815-ffad4c1539a9", 1500),  # bright modern home exterior
    "interior":  u("photo-1600585154340-be6161a56a0c", 1200),  # luxe living room
    "family":    u("photo-1511895426328-dc8714191300", 1200),  # family at home
    "keys":      u("photo-1560518883-ce09059eeffa", 1200),     # house + lawn
    "la":        u("photo-1444723121867-7a241cacace9", 1400),  # city / LA
    "porch":     u("photo-1570129477492-45c003edd2be", 1200),  # suburban home
    "luxury":    u("photo-1512917774080-9991f1c4c750", 1400),  # aerial luxury home
    "couple":    u("photo-1521791136064-7986c2920216", 1200),  # advisor handshake
}
# Local founder photo (user provides the file at this path).
FOUNDER_IMG = "assets/img/photos/founder.jpg"

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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body data-page="{active}">
"""

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
    sub = "".join(f'<li><a href="{url}">{e} &nbsp;{n}</a></li>' for url,n,e in PROGRAMS)
    return f"""<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="West Coast Capital Mortgage home">
      <img class="brand-logo" src="assets/img/logo-horizontal.svg" alt="West Coast Capital Mortgage Inc. logo">
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
    prog = "".join(f'<a href="{url}">{n}</a>' for url,n,e in PROGRAMS[:6])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <b>West Coast Capital<br>Mortgage Inc.</b>
        <p style="margin-top:14px">Honest guidance. Clear answers. Strong results — for homebuyers and homeowners across California, Florida &amp; Washington.</p>
        <p><a href="tel:{PHONE_TEL}" style="color:var(--gold-light);display:inline;font-weight:600">{PHONE}</a></p>
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
      <span>Licensed in CA · FL · WA · Equal Housing Lender</span>
    </div>
    <p class="legal">West Coast Capital Mortgage Inc. ({NMLS}) is an Equal Housing Lender. This is not a commitment to lend. All loans are subject to credit approval, income verification, and property appraisal. Rates and programs are subject to change without notice and are shown for illustrative purposes only — actual rates depend on credit profile, loan amount, down payment, occupancy, and property type. Calculator results are estimates and not an offer or guarantee of a loan. Equal Housing Opportunity.</p>
  </div>
</footer>"""

def chat():
    return """<button id="chat-fab" aria-label="Open chat">💬</button>
<div id="chat-panel" aria-live="polite">
  <div class="chat-head">
    <div class="av">🏠</div>
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

def page_hero(crumb, h1, sub, bg=None):
    style = f' style="background-image:linear-gradient(120deg,rgba(15,50,81,.88),rgba(15,50,81,.5)),url(\'{bg}\')"' if bg else ""
    return f"""<section class="page-hero"{style}>
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>"""

def cta_band():
    return f"""<section class="section"><div class="container">
  <div class="cta-band">
    <span class="eyebrow center" style="color:var(--gold-light);justify-content:center">Let's begin</span>
    <h2>Ready to take the next step?</h2>
    <p>Get a free, no-obligation rate quote or start your application in minutes. A licensed loan officer will guide you the whole way.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn-gold btn-lg" href="apply.html">Apply Now</a>
      <a class="btn btn-ghost btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
</div></section>"""
