#!/usr/bin/env python3
"""
Generate the California Mortgage concierge funnel sub-pages.

Hand-authored files (index.html, styles.css, script.js, scenario-builder.js)
are NOT touched. This script only (re)writes the shared-chrome content pages so
the header, footer, and compliance language stay consistent across the funnel.

Run:  python3 tools/build_californiamtg_pages.py
Output: ../californiamtg/*.html and ../californiamtg/education/*.html
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "californiamtg")

PHONE = "(310) 686-5053"
EDU_COMPLIANCE = ("This information is for educational purposes only and is not a loan approval, "
                  "loan commitment, or rate quote. Final loan options are subject to review by a "
                  "licensed mortgage professional.")

HEADER = '''<header class="site-header" id="siteHeader">
  <div class="container header-inner">
    <a class="brand" href="/index.html" aria-label="California Mortgage home">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 64 64" width="40" height="40">
          <path d="M14 36 L32 18 L50 36" fill="none" stroke="#b08a4c" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
          <path d="M20 34 L20 48 L44 48 L44 34" fill="none" stroke="#2c2722" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
          <rect x="29" y="40" width="6" height="8" rx="1" fill="#b08a4c"/>
        </svg>
      </span>
      <span class="brand-text"><span class="brand-name">California Mortgage</span></span>
    </a>
    <nav class="main-nav" id="mainNav" aria-label="Primary">
      <a href="/index.html#concierge">Concierge</a>
      <a href="/scenarios.html">Scenarios</a>
      <a href="/rates-payments.html">Rates &amp; Payments</a>
      <a href="/education/index.html">Education</a>
      <a href="/about.html">About</a>
      <a href="/contact.html">Contact</a>
    </nav>
    <div class="header-cta">
      <a class="btn btn-charcoal" href="/index.html#builder" data-start>Begin</a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mainNav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>'''

FOOTER = '''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <span class="brand-name">California Mortgage</span>
      <span class="brand-sub">Powered by West Coast Capital Mortgage Inc.</span>
      <ul class="footer-contact">
        <li><a href="tel:+13106865053">Phone: (310) 686-5053</a></li>
        <li><a href="mailto:info@californiamtg.com">Email: info@californiamtg.com</a></li>
        <li>Serving California</li>
      </ul>
      <div class="footer-eho">
        <img src="/assets/equal-housing.svg" alt="Equal Housing Opportunity" width="46" height="50" loading="lazy" decoding="async">
      </div>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <ul>
        <li><a href="/index.html#concierge">Concierge</a></li>
        <li><a href="/scenarios.html">Scenarios</a></li>
        <li><a href="/rates-payments.html">Rates &amp; Payments</a></li>
        <li><a href="/education/index.html">Education</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Concierge</h4>
      <ul>
        <li><a href="/index.html#builder" data-start>Start My Scenario</a></li>
        <li><a href="https://wcci.online">AI Review</a></li>
        <li><a href="/about-human-review.html">Human Review</a></li>
        <li><a href="https://westccmortgage.com">Main Website</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Disclosures</h4>
      <ul class="footer-disclosure">
        <li>West Coast Capital Mortgage Inc.</li>
        <li>NMLS #2817729</li>
        <li>CA DRE #01385024</li>
        <li>Equal Housing Opportunity</li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p class="footer-compliance">''' + EDU_COMPLIANCE + '''</p>
    <div class="footer-links">
      <a href="/index.html#concierge">Concierge</a>
      <a href="/scenarios.html">Scenarios</a>
      <a href="/rates-payments.html">Rates &amp; Payments</a>
      <a href="/education/index.html">Education</a>
      <a href="/about.html">About</a>
      <a href="/contact.html">Contact</a>
      <a href="/privacy-policy.html">Privacy Policy</a>
      <a href="/terms.html">Terms of Use</a>
    </div>
    <p class="copyright">&copy; <span id="year">2026</span> California Mortgage. Powered by West Coast Capital Mortgage Inc. All rights reserved.</p>
  </div>
</footer>'''


def page(path, title, description, body, canonical_path):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#2c2722">
<meta name="robots" content="index, follow">
<meta name="author" content="West Coast Capital Mortgage Inc.">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="canonical" href="https://californiamtg.com{canonical_path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="California Mortgage">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://californiamtg.com{canonical_path}">
<meta property="og:image" content="https://californiamtg.com/public/images/california_mortgage_poster.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://californiamtg.com/public/images/california_mortgage_poster.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

{HEADER}

<main>
{body}
</main>

{FOOTER}

<script src="/config.js"></script>
<script src="/script.js" defer></script>
<script type="module" src="/src/app.js"></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def hero(eyebrow, h1, lead):
    return f'''<section class="page-hero">
  <div class="container">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="page-lead">{lead}</p>
  </div>
</section>'''


def cta_block(title, text, buttons):
    btns = "".join(buttons)
    return f'''<div class="cta-block">
  <h2>{title}</h2>
  <p>{text}</p>
  <div class="cta-row">{btns}</div>
</div>'''


def compliance(text=EDU_COMPLIANCE):
    return f'<p class="compliance-box">{text}</p>'


BTN_START = '<a class="btn btn-primary btn-lg" href="/index.html#builder" data-start>Start My Scenario</a>'
BTN_SITUATION = '<a class="btn btn-primary btn-lg" href="/index.html#builder" data-start>Tell Us Your Situation</a>'
BTN_CONTACT = '<a class="btn btn-outline-dark btn-lg" href="/contact.html">Contact Us</a>'
BTN_PRO = '<a class="btn btn-primary btn-lg" href="/contact.html">Talk to a Mortgage Professional</a>'
BTN_RATES = '<a class="btn btn-primary btn-lg" href="/index.html?goal=rates#builder">Check My Scenario</a>'


# ----------------------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------------------
contact_body = hero(
    "Contact",
    "Talk to a Mortgage Professional",
    "Share your situation and a licensed mortgage professional with West Coast Capital "
    "Mortgage Inc. can review it and reach out about the next step."
) + '''
<section class="section">
  <div class="container">
    <div class="contact-layout">
      <div class="builder-card" id="contactCard">
        <form name="contact" class="cm-form" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/contact.html">
          <input type="hidden" name="form-name" value="contact">
          <p class="hidden-field" aria-hidden="true"><label>Do not fill this out: <input name="bot-field"></label></p>
          <div class="field-grid">
            <div class="field">
              <label class="field-label" for="c_name">Full Name <span class="req">*</span></label>
              <input class="field-input" id="c_name" name="fullName" type="text" placeholder="First and last name" required>
              <p class="field-error"></p>
            </div>
            <div class="field">
              <label class="field-label" for="c_phone">Phone <span class="req">*</span></label>
              <input class="field-input" id="c_phone" name="phone" type="tel" placeholder="(310) 555-0199" required>
              <p class="field-error"></p>
            </div>
            <div class="field field-full">
              <label class="field-label" for="c_email">Email <span class="req">*</span></label>
              <input class="field-input" id="c_email" name="email" type="email" placeholder="you@example.com" required>
              <p class="field-error"></p>
            </div>
            <div class="field">
              <label class="field-label" for="c_iama">I am a:</label>
              <select class="field-input" id="c_iama" name="iAmA">
                <option value="">Select...</option>
                <option>Home Buyer</option>
                <option>Homeowner</option>
                <option>Realtor</option>
                <option>Investor</option>
                <option>Self-Employed Borrower</option>
                <option>Not Sure</option>
              </select>
            </div>
            <div class="field">
              <label class="field-label" for="c_help">What do you need help with?</label>
              <select class="field-input" id="c_help" name="helpWith">
                <option value="">Select...</option>
                <option>Purchase</option>
                <option>Refinance</option>
                <option>Lower payment</option>
                <option>Rates</option>
                <option>Cash-out</option>
                <option>Investment property</option>
                <option>Self-employed loan options</option>
                <option>Second opinion</option>
                <option>Other</option>
              </select>
            </div>
            <div class="field field-full">
              <label class="field-label">Preferred contact method <span class="req">*</span></label>
              <div class="radio-row">
                <label class="radio-pill"><input type="radio" name="contactMethod" value="Call" required><span>Call</span></label>
                <label class="radio-pill"><input type="radio" name="contactMethod" value="Text"><span>Text</span></label>
                <label class="radio-pill"><input type="radio" name="contactMethod" value="Email"><span>Email</span></label>
              </div>
              <p class="field-error"></p>
            </div>
            <div class="field field-full">
              <label class="field-label" for="c_msg">Message / Scenario</label>
              <textarea class="field-input" id="c_msg" name="message" rows="4" placeholder="Tell us about your situation."></textarea>
            </div>
          </div>
          <p class="compliance-box">This is not a loan approval, loan commitment, or rate quote. Final loan options are subject to review by a licensed mortgage professional.</p>
          <div class="form-actions">
            <button class="btn btn-primary" type="submit">Send Message</button>
          </div>
        </form>
      </div>

      <aside class="contact-aside">
        <div class="info-card">
          <h3>California Mortgage</h3>
          <p>Powered by West Coast Capital Mortgage Inc.</p>
          <p><a href="tel:+13106865053">Phone: (310) 686-5053</a><br>
             <a href="mailto:info@californiamtg.com">info@californiamtg.com</a><br>
             Serving California</p>
        </div>
        <div class="info-card">
          <h3>Prefer to start with your situation?</h3>
          <p>Organize your scenario in a few simple steps before you talk to anyone.</p>
          <p><a href="/index.html#builder" data-start>Start My Scenario &rarr;</a></p>
        </div>
        <div class="info-card">
          <h3>Licensed company</h3>
          <p>West Coast Capital Mortgage Inc.<br>NMLS #2817729 &middot; CA DRE #01385024<br>Equal Housing Opportunity</p>
        </div>
      </aside>
    </div>
  </div>
</section>'''

# ----------------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------------
about_body = hero(
    "About",
    "About California Mortgage",
    "A premium mortgage concierge experience powered by licensed mortgage professionals."
) + '''
<section class="section">
  <div class="container article prose">
    <p>California Mortgage helps buyers, homeowners, Realtors, self-employed borrowers, and
    investors organize their mortgage situation before taking the next step. Instead of
    starting with a loan program or a full application, you start with your situation — and
    we help structure it for review.</p>

    <div class="edu-grid">
      <div class="info-card"><h3>Built for California real estate</h3><p>Designed around California property values, competitive markets, and lending requirements.</p></div>
      <div class="info-card"><h3>Designed for real-world situations</h3><p>Self-employed income, jumbo purchases, investor loans, lower-payment questions, and second opinions.</p></div>
      <div class="info-card"><h3>AI-assisted intake available</h3><p>Technology helps organize the scenario quickly and clearly before a human reviews it.</p></div>
      <div class="info-card"><h3>Human review available</h3><p>Final guidance and mortgage options are reviewed by licensed mortgage professionals.</p></div>
    </div>

    <h2>Powered by West Coast Capital Mortgage Inc.</h2>
    <p>California Mortgage is the premium educational and concierge entry point. West Coast
    Capital Mortgage Inc. is the licensed mortgage company behind the professional review and
    follow-up — California Mortgage is not trying to replace it.</p>

    <div class="info-card">
      <h3>West Coast Capital Mortgage Inc.</h3>
      <p>NMLS #2817729 &middot; CA DRE #01385024<br>
      Phone: <a href="tel:+13106865053">(310) 686-5053</a><br>
      Serving California &middot; Equal Housing Opportunity</p>
    </div>
''' + cta_block(
    "Start With the Situation",
    "Organize your mortgage scenario in a few simple steps, or reach out to a licensed mortgage professional.",
    [BTN_START, BTN_CONTACT]
) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# ABOUT — HUMAN REVIEW
# ----------------------------------------------------------------------------
human_review_body = hero(
    "Trust",
    "Human Review Behind the Technology",
    "California Mortgage is a premium mortgage concierge entry point — with licensed mortgage "
    "professionals behind the review."
) + '''
<section class="section">
  <div class="container article prose">
    <p>California Mortgage is a premium mortgage concierge entry point. The site may use
    technology and AI-assisted intake to organize scenarios quickly and clearly. That is where
    the technology stops and the people begin.</p>

    <ul class="check-list">
      <li>The site may use technology and AI-assisted intake to organize your scenario.</li>
      <li>Final guidance and mortgage options should be reviewed by licensed mortgage professionals.</li>
      <li>This is not just an AI website — there is a real licensed mortgage company behind it.</li>
      <li>West Coast Capital Mortgage Inc. provides the professional mortgage review.</li>
    </ul>

    <h2>The licensed company behind the review</h2>
    <div class="info-card">
      <h3>West Coast Capital Mortgage Inc.</h3>
      <p>NMLS #2817729 &middot; CA DRE #01385024<br>Equal Housing Opportunity</p>
    </div>
''' + cta_block(
    "Talk to a Real Mortgage Professional",
    "When you are ready, a licensed mortgage professional can review your scenario and guide the next step.",
    [BTN_PRO]
) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# EDUCATION INDEX
# ----------------------------------------------------------------------------
education_index_body = hero(
    "Education",
    "Mortgage Education",
    "Short, clear explanations to help you understand the process before you take the next step."
) + '''
<section class="section">
  <div class="container article">
    <div class="edu-grid">
      <a class="card audience-card" href="/education/no-credit-check-to-start.html">
        <h3>Why No Credit Check to Start?</h3>
        <p>How a soft scenario review differs from a full mortgage application.</p>
        <span class="link-arrow">Learn Why <span aria-hidden="true">&rarr;</span></span>
      </a>
      <a class="card audience-card" href="/education/which-program-fits.html">
        <h3>Not Sure Which Program Fits?</h3>
        <p>Conventional, jumbo, FHA, VA, bank statement, DSCR, Non-QM and more.</p>
        <span class="link-arrow">Explore Programs <span aria-hidden="true">&rarr;</span></span>
      </a>
      <a class="card audience-card" href="/education/complex-scenarios.html">
        <h3>Built for Complex Scenarios</h3>
        <p>Self-employed income, investors, jumbo, bank denials, and second opinions.</p>
        <span class="link-arrow">See Scenarios <span aria-hidden="true">&rarr;</span></span>
      </a>
      <a class="card audience-card" href="/rates-payments.html">
        <h3>Understanding Rates &amp; Payments</h3>
        <p>Why the lowest rate is not always the best total option.</p>
        <span class="link-arrow">Learn More <span aria-hidden="true">&rarr;</span></span>
      </a>
      <a class="card audience-card" href="/about-human-review.html">
        <h3>Human Review Behind the Technology</h3>
        <p>Licensed mortgage professionals review the scenario and next step.</p>
        <span class="link-arrow">About Human Review <span aria-hidden="true">&rarr;</span></span>
      </a>
      <a class="card audience-card" href="/scenarios.html">
        <h3>Start With the Situation</h3>
        <p>Find the situation that sounds like yours and begin there.</p>
        <span class="link-arrow">See Situations <span aria-hidden="true">&rarr;</span></span>
      </a>
    </div>
''' + cta_block("Start With the Situation", "You do not need to know the loan program. Start with the situation.", [BTN_START]) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# EDUCATION A — No credit check to start
# ----------------------------------------------------------------------------
no_credit_body = hero(
    "Education",
    "Why No Credit Check to Start?",
    "You can explain your situation first. No credit check is required to start the concierge review."
) + '''
<section class="section">
  <div class="container article prose">
    <p class="compliance-box">No credit check is required to start the concierge review. A credit
    review may be needed later for a full mortgage application, pre-approval, or loan approval.</p>

    <h2>Why we do not need a credit check to begin</h2>
    <p>The goal at the start is simple: understand your situation. Organizing your goals, property,
    income type, and timeline does not require pulling credit. You can share the picture first,
    then decide on next steps with a licensed mortgage professional.</p>

    <h2>What a credit score is used for in mortgage lending</h2>
    <p>Credit helps a lender understand repayment history and risk. It can influence program
    eligibility and pricing, but it is only one part of a much larger picture that includes income,
    down payment, property type, occupancy, reserves, and the loan program.</p>

    <h2>When credit may be reviewed later</h2>
    <p>A credit review typically happens when you move toward a full application, a pre-approval, or
    a loan approval — not when you are simply organizing a scenario.</p>

    <h2>Starting a scenario review vs. applying for a mortgage</h2>
    <ul class="check-list">
      <li>Scenario review: a soft, low-pressure conversation about your situation.</li>
      <li>Mortgage application: the formal step where documentation and credit are reviewed.</li>
    </ul>

    <h2>What affects a credit score</h2>
    <ul>
      <li>Payment history and on-time payments</li>
      <li>Amounts owed and credit utilization</li>
      <li>Length of credit history</li>
      <li>New credit and recent inquiries</li>
      <li>Mix of credit types</li>
    </ul>

    <h2>How borrowers can prepare credit before applying</h2>
    <ul>
      <li>Keep payments current</li>
      <li>Avoid large new debts before a mortgage</li>
      <li>Keep balances reasonable relative to limits</li>
      <li>Review reports for errors</li>
    </ul>

    <h2>Why credit, income, down payment, property type, and loan program all matter</h2>
    <p>No single factor decides the outcome. The right path depends on how these pieces fit together —
    which is exactly what a scenario review helps organize.</p>

    <h2>Why this is educational, not approval</h2>
    <p>This page is educational. It is not an approval or a commitment to lend.</p>
''' + cta_block("Start With the Situation", "Explain your situation first — no credit check required to begin.", [BTN_START]) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# EDUCATION B — Which program fits
# ----------------------------------------------------------------------------
which_program_body = hero(
    "Education",
    "Not Sure Which Mortgage Program Fits?",
    "You do not need to know the loan program before starting. That is what the review is for."
) + '''
<section class="section">
  <div class="container article prose">
    <p>There are many mortgage paths, and the right one depends on your full picture. Here are
    common options a licensed mortgage professional may consider.</p>

    <div class="edu-grid">
      <div class="info-card"><h3>Conventional loans</h3><p>A common path for many primary-home and second-home buyers.</p></div>
      <div class="info-card"><h3>Jumbo loans</h3><p>Higher loan amounts for California&rsquo;s premium property markets.</p></div>
      <div class="info-card"><h3>FHA loans</h3><p>Flexible qualifying for eligible borrowers.</p></div>
      <div class="info-card"><h3>VA loans</h3><p>Benefits for eligible veterans and service members.</p></div>
      <div class="info-card"><h3>Bank statement loans</h3><p>Income documented through bank deposits for self-employed borrowers.</p></div>
      <div class="info-card"><h3>DSCR investor loans</h3><p>Qualify investment properties using projected rental cash flow.</p></div>
      <div class="info-card"><h3>Non-QM loans</h3><p>Flexible programs for unique income, credit, or property scenarios.</p></div>
      <div class="info-card"><h3>Cash-out refinance</h3><p>Access home equity for renovations, investing, or consolidation.</p></div>
      <div class="info-card"><h3>Bridge / private options</h3><p>Short-term or private financing where it fits the scenario.</p></div>
    </div>

    <h2>Why one bank may say no while another program may fit</h2>
    <p>Different lenders and programs have different guidelines. A &ldquo;no&rdquo; on one program does not
    mean every path is closed — another structure may be a better match.</p>

    <h2>Why the loan program depends on your full picture</h2>
    <ul class="check-list">
      <li>Income type and documentation</li>
      <li>Credit profile</li>
      <li>Property type and occupancy</li>
      <li>Down payment and reserves</li>
      <li>Loan amount</li>
    </ul>

    <h2>Why a scenario review helps narrow the options</h2>
    <p>Organizing the details first makes it easier to identify which paths are worth reviewing with a
    licensed mortgage professional.</p>
''' + cta_block("Start With the Situation", "You do not need to know the program. Start with the situation.", [BTN_START]) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# EDUCATION C — Complex scenarios
# ----------------------------------------------------------------------------
complex_body = hero(
    "Education",
    "Built for Complex Mortgage Scenarios",
    "A complex scenario does not automatically mean the loan cannot work — it means it needs to be organized and reviewed under the right loan path."
) + '''
<section class="section">
  <div class="container article prose">
    <h2>Situations this is built for</h2>
    <div class="edu-grid">
      <div class="info-card"><h3>Self-employed &amp; 1099 income</h3><p>Business owners and contractors whose returns may not show full income.</p></div>
      <div class="info-card"><h3>High-value &amp; jumbo purchases</h3><p>Premium California properties and larger loan amounts.</p></div>
      <div class="info-card"><h3>Investor loans</h3><p>DSCR and rental-income approaches for investment property.</p></div>
      <div class="info-card"><h3>Refinance to lower payment</h3><p>Payment strategy, term changes, and rate improvement.</p></div>
      <div class="info-card"><h3>Cash-out refinance</h3><p>Using equity for renovations, investing, or consolidation.</p></div>
      <div class="info-card"><h3>Bank denial / second opinion</h3><p>A fresh look when another lender said no.</p></div>
      <div class="info-card"><h3>Rate vs. closing cost</h3><p>Points vs. no points, and the total cost over time.</p></div>
      <div class="info-card"><h3>Urgent Realtor files</h3><p>Time-sensitive purchase scenarios that need fast organization.</p></div>
    </div>

    <h2>Why complex does not mean impossible</h2>
    <p>Many strong borrowers simply do not fit a one-size-fits-all box. The work is to organize the
    situation and review it under the right loan path — that is the point of a scenario review.</p>
''' + cta_block("Tell Us Your Situation", "Self-employed, investor, jumbo, denial, or payment strategy — start by explaining the situation.", [BTN_SITUATION]) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# RATES & PAYMENTS
# ----------------------------------------------------------------------------
rates_body = hero(
    "Rates &amp; Payments",
    "Understanding Rates &amp; Payments",
    "Educational guidance on how mortgage rates and payments work — not a live rate quote."
) + '''
<section class="section">
  <div class="container article prose">
    <h2>Mortgage rates are not one-size-fits-all</h2>
    <p>Your rate may depend on many factors working together:</p>
    <ul class="check-list">
      <li>Credit score</li>
      <li>Loan amount</li>
      <li>Down payment</li>
      <li>Occupancy</li>
      <li>Property type</li>
      <li>Loan program</li>
      <li>Points</li>
      <li>Market conditions</li>
      <li>Lender guidelines</li>
    </ul>

    <h2>The lowest rate is not always the best total option</h2>
    <p>Points, closing costs, the loan term, the monthly payment, and how long you plan to keep the
    property all affect the true cost. Sometimes a slightly higher rate with lower costs is the
    better overall fit, depending on your plans.</p>

    <h2>Lowering a payment can involve more than one strategy</h2>
    <ul>
      <li>Refinancing when the numbers make sense</li>
      <li>Changing the loan term</li>
      <li>Improving the rate</li>
      <li>Consolidating higher-interest debt</li>
      <li>Other strategies based on the scenario</li>
    </ul>

    <p class="compliance-box">This page is educational only and is not a rate quote, loan approval, or commitment to lend.</p>
''' + cta_block("See How It Applies to You", "Organize your numbers and a licensed mortgage professional can review the full picture.", [BTN_RATES]) + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# SCENARIOS
# ----------------------------------------------------------------------------
scenarios = [
    ("I want to buy a home", "buying"),
    ("I want to refinance", "refinancing"),
    ("I want to lower my payment", "lowering-payment"),
    ("I want to understand rates", "rates"),
    ("I am self-employed", "self-employed"),
    ("I want to buy an investment property", "investment"),
    ("I was denied by a bank", "denied"),
    ("I am a Realtor with a difficult buyer scenario", "realtor"),
]
scenario_links = "".join(
    f'<a class="scenario-link" href="/index.html?goal={g}#builder"><span>{label}</span>'
    f'<span class="s-arrow" aria-hidden="true">&rarr;</span></a>'
    for label, g in scenarios
)
scenarios_body = hero(
    "Scenarios",
    "Start With the Situation",
    "Find the situation that sounds like yours. Each one starts a short, guided scenario review."
) + f'''
<section class="section">
  <div class="container article">
    <div class="scenario-list">
      {scenario_links}
    </div>
''' + cta_block("Not sure which fits?", "That is completely fine. Start a general scenario review and we will help organize it.", [BTN_START]) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# PRIVACY + TERMS (lightweight)
# ----------------------------------------------------------------------------
privacy_body = hero("Legal", "Privacy Policy", "How information you share with California Mortgage is collected, used, and protected.") + '''
<section class="section">
  <div class="container article prose">
    <p>California Mortgage, powered by West Coast Capital Mortgage Inc., respects your privacy.
    This policy explains, in plain English, what we collect and how it is used.</p>

    <h2>What data we collect</h2>
    <ul>
      <li><strong>Information you submit</strong> &mdash; name, phone, email, preferred contact method,
      and the scenario details you choose to share through the scenario builder or contact form.</li>
      <li><strong>Cookies &amp; a first-party visitor ID</strong> &mdash; an anonymous identifier stored on
      your device so we can remember your visit and your cookie choice.</li>
      <li><strong>Analytics (only with your consent)</strong> &mdash; pages viewed, general device and
      browser information, screen size, referrer, and UTM/source parameters.</li>
    </ul>

    <h2>Cookies and analytics</h2>
    <p>On your first visit we ask for your cookie preference. If you choose <em>Essential Only</em>,
    we store just the functional basics (your visitor ID, your consent choice, and any form you
    submit). If you choose <em>Accept &amp; Continue</em>, we also record page views and basic events
    to understand which mortgage topics are helpful. We do not claim to know who you are before you
    submit your contact information.</p>

    <h2>Scenario &amp; contact form data</h2>
    <p>When you submit the scenario builder or contact form, your details are stored so a licensed
    mortgage professional can review your situation and follow up.</p>

    <h2>How your data is used</h2>
    <p>We use your information to respond to your request, operate and improve the website, and route
    your mortgage inquiry to West Coast Capital Mortgage Inc. To do this, data <em>may</em> be processed
    by service providers and tools we use (for example, our database, analytics, CRM, automation
    webhooks, or email). We do not sell your personal information.</p>

    <h2>Your California privacy rights</h2>
    <p>California residents may have rights to know, access, or request deletion of personal
    information, and to opt out of certain uses, under California privacy law. To make a request,
    contact us using the details below.</p>

    <h2>Managing your cookie choice</h2>
    <p>You can change your cookie preference at any time.</p>
    <p><button type="button" id="manageConsent" class="btn btn-outline-dark">Manage cookie preferences</button></p>

    <h2>Contact</h2>
    <p>Questions or privacy requests? Email
    <a href="mailto:info@californiamtg.com">info@californiamtg.com</a> or call
    <a href="tel:+13106865053">(310) 686-5053</a>.</p>

    <p class="compliance-box">This page is provided for general information and is not legal advice.</p>
  </div>
</section>'''

terms_body = hero("Legal", "Terms of Use", "The terms that apply to your use of this website.") + '''
<section class="section">
  <div class="container article prose">
    <p>By using California Mortgage (powered by West Coast Capital Mortgage Inc.), you agree to these
    terms. The content on this site is provided for general, educational purposes.</p>
    <h2>No approval or commitment</h2>
    <p>Nothing on this site is a loan approval, loan commitment, or rate quote. Final loan options are
    subject to review by a licensed mortgage professional.</p>
    <h2>Accuracy</h2>
    <p>We aim to keep information accurate but make no guarantees. Programs and guidelines change.</p>
    <h2>Contact</h2>
    <p>Questions? Email <a href="mailto:info@californiamtg.com">info@californiamtg.com</a>.</p>
    <p class="compliance-box">''' + EDU_COMPLIANCE + '''</p>
  </div>
</section>'''


PAGES = [
    ("contact.html", "Contact | California Mortgage", "Contact California Mortgage — share your scenario and a licensed mortgage professional with West Coast Capital Mortgage Inc. can review it.", contact_body, "/contact"),
    ("about.html", "About | California Mortgage", "About California Mortgage — a premium mortgage concierge experience powered by West Coast Capital Mortgage Inc.", about_body, "/about"),
    ("about-human-review.html", "Human Review | California Mortgage", "Human review behind the technology — licensed mortgage professionals from West Coast Capital Mortgage Inc. review your scenario.", human_review_body, "/about-human-review"),
    ("scenarios.html", "Scenarios | California Mortgage", "Start with the situation — buying, refinancing, lowering payment, self-employed, investor, denied by a bank, or a Realtor scenario.", scenarios_body, "/scenarios"),
    ("rates-payments.html", "Rates & Payments | California Mortgage", "Understanding mortgage rates and payments — educational guidance, not a rate quote.", rates_body, "/rates-payments"),
    ("education/index.html", "Education | California Mortgage", "Mortgage education — credit, programs, complex scenarios, rates, and human review.", education_index_body, "/education"),
    ("education/no-credit-check-to-start.html", "Why No Credit Check to Start? | California Mortgage", "Why no credit check is required to start the concierge review, and how it differs from a full application.", no_credit_body, "/education/no-credit-check-to-start"),
    ("education/which-program-fits.html", "Which Mortgage Program Fits? | California Mortgage", "You do not need to know the loan program before starting. Explore conventional, jumbo, FHA, VA, bank statement, DSCR, and Non-QM paths.", which_program_body, "/education/which-program-fits"),
    ("education/complex-scenarios.html", "Built for Complex Scenarios | California Mortgage", "Self-employed income, jumbo, investor loans, bank denials, payment strategy, and second opinions.", complex_body, "/education/complex-scenarios"),
    ("privacy-policy.html", "Privacy Policy | California Mortgage", "How information you share with California Mortgage is collected, used, and protected.", privacy_body, "/privacy-policy"),
    ("terms.html", "Terms of Use | California Mortgage", "Terms that apply to your use of the California Mortgage website.", terms_body, "/terms"),
]

if __name__ == "__main__":
    for path, title, desc, body, canon in PAGES:
        page(path, title, desc, body, canon)
    print("Done:", len(PAGES), "pages.")
