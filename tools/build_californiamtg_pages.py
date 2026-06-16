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
import json

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
      <a href="/loan-options.html">Loan Options</a>
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
        <li><a href="/loan-options.html">Loan Options</a></li>
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


def page(path, title, description, body, canonical_path, head_extra=""):
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
{head_extra}</head>
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
BTN_PRO_OUTLINE = '<a class="btn btn-outline-dark btn-lg" href="/contact.html">Talk to a Mortgage Professional</a>'
BTN_CONTACT_PRO = '<a class="btn btn-outline-dark btn-lg" href="/contact.html">Contact a Mortgage Professional</a>'
BTN_RATES = '<a class="btn btn-primary btn-lg" href="/index.html?goal=rates#builder">Check My Scenario</a>'

# Shared licensed-company trust block.
TRUST_BLOCK = '''<div class="trust-block">
  <div class="trust-eho" aria-hidden="true">
    <img src="/assets/equal-housing.svg" alt="" width="40" height="44" loading="lazy">
  </div>
  <div class="trust-lines">
    <p class="trust-name">West Coast Capital Mortgage Inc.</p>
    <ul>
      <li>NMLS #2817729</li>
      <li>CA DRE #01385024</li>
      <li>Phone: <a href="tel:+13106865053">(310) 686-5053</a></li>
      <li>Equal Housing Opportunity</li>
    </ul>
  </div>
</div>'''


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
    "A premium mortgage concierge experience backed by real licensed professionals."
) + '''
<section class="section">
  <div class="container article prose">
    <p>California Mortgage is a premium educational and concierge entry point for people who want to
    explain their mortgage situation before starting a full application. The purpose is to help
    organize the scenario, create a clearer starting point, and route the visitor toward AI-assisted
    review or professional mortgage review.</p>
    <p>California Mortgage is powered by West Coast Capital Mortgage Inc., the licensed mortgage
    company behind professional review and follow-up.</p>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow gold">Real People Behind the Guidance</p>
    </div>
    <div class="person">
      <div class="person-photo">
        <div class="photo-placeholder" aria-hidden="true">Photo coming soon</div>
        <img class="person-img" alt="Anatoliy Kanevsky, founder of West Coast Capital Mortgage Inc."
             src="/images/anatoliy-kanevsky.jpg" width="520" height="600" loading="lazy" decoding="async"
             onerror="if(this.dataset.s!=='1'){this.dataset.s='1';this.src='/public/images/anatoliy-kanevsky.png';}else{this.parentNode.classList.add('show-placeholder');}">
      </div>
      <div class="person-copy prose">
        <h2>Meet Anatoliy Kanevsky</h2>
        <p>Anatoliy Kanevsky is the founder of West Coast Capital Mortgage Inc. and a California real
        estate and mortgage professional with decades of experience helping borrowers, homeowners,
        Realtors, investors, and self-employed clients navigate real-world financing scenarios.</p>
        <p>His background combines mortgage lending, real estate brokerage, luxury residential
        development, and practical deal analysis. That experience helps California Mortgage focus on
        clear guidance, smart scenario organization, and human review behind the technology.</p>
        <ul class="check-list">
          <li>Founder, West Coast Capital Mortgage Inc.</li>
          <li>California real estate broker</li>
          <li>Mortgage and real estate professional experience</li>
          <li>Luxury residential development background</li>
          <li>Experience with purchase, refinance, jumbo, DSCR, Non-QM, and self-employed borrower scenarios</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container article">
    <div class="section-head" style="text-align:left;margin-bottom:1.4rem">
      <h2>Human Review Behind the Technology</h2>
      <p class="section-sub" style="margin-left:0">Technology can help organize a scenario, but mortgage
      options require professional review. California Mortgage is designed to help people explain their
      situation first, then connect with the right next step.</p>
    </div>
    <div class="grid grid-3">
      <article class="card">
        <h3>Scenario first</h3>
        <p>Start by explaining the situation before a full application.</p>
      </article>
      <article class="card">
        <h3>Professional review available</h3>
        <p>A licensed mortgage professional can review the information and guide the next step.</p>
      </article>
      <article class="card">
        <h3>Trust and transparency</h3>
        <p>No credit check is required to start the concierge review. Full loan options are subject to professional review.</p>
      </article>
    </div>
''' + TRUST_BLOCK + cta_block(
    "Start With the Situation",
    "Organize your mortgage scenario in a few simple steps, or reach out to a licensed mortgage professional.",
    [BTN_START, BTN_CONTACT_PRO]
) + compliance() + '''
  </div>
</section>'''

# ----------------------------------------------------------------------------
# ABOUT — HUMAN REVIEW
# ----------------------------------------------------------------------------
human_review_body = hero(
    "Human Review",
    "Human Guidance Behind the Technology",
    "AI can help organize the scenario. Real mortgage professionals help review the next step."
) + '''
<section class="section">
  <div class="container">
    <div class="person">
      <div class="person-photo">
        <img src="/public/images/anatoliy-kanevsky.png"
             alt="Anatoliy Kanevsky, founder of West Coast Capital Mortgage Inc."
             width="520" height="600" loading="lazy" decoding="async">
      </div>
      <div class="person-copy prose">
        <h2>Reviewed by Experience, Not Just Automation</h2>
        <p>California Mortgage is a premium educational and concierge entry point. Behind the
        experience is West Coast Capital Mortgage Inc., a licensed mortgage company helping buyers,
        homeowners, Realtors, self-employed borrowers, and investors review real mortgage scenarios.</p>
        <p>Anatoliy Kanevsky brings decades of real estate, mortgage, and luxury residential
        development experience to help clients understand their financing path before starting a
        full application.</p>
        <ul class="check-list">
          <li>California real estate broker</li>
          <li>Mortgage professional experience</li>
          <li>Luxury residential development background</li>
          <li>Purchase, refinance, jumbo, DSCR, Non-QM, and self-employed borrower scenarios</li>
          <li>Founder, West Coast Capital Mortgage Inc.</li>
        </ul>
      </div>
    </div>
''' + TRUST_BLOCK + '''
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow gold">Why It Matters</p>
      <h2>Why Human Review Matters</h2>
    </div>
    <div class="grid grid-3">
      <article class="card">
        <h3>Real review, not just automation</h3>
        <p>Technology can organize the situation, but mortgage options require professional review.</p>
      </article>
      <article class="card">
        <h3>Built for complex scenarios</h3>
        <p>Self-employed income, jumbo purchases, investor loans, DSCR, refinance, and second opinions.</p>
      </article>
      <article class="card">
        <h3>Clear next step</h3>
        <p>The goal is not to push a full application. The goal is to understand the situation first.</p>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container article">
''' + cta_block(
    "Start With the Situation",
    "Organize your scenario in a few simple steps, or speak with a licensed mortgage professional.",
    [BTN_START, BTN_PRO_OUTLINE]
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


# ============================================================
# LOAN PROGRAM LANDING PAGES (SEO + lead capture)
# Each becomes /<slug> with FAQ schema, internal links, and CTAs into the
# scenario builder + contact. California-focused, compliance-safe.
# ============================================================
LOANS = [
    {
        "slug": "jumbo-loans", "nav_label": "Jumbo Loans",
        "card": "Financing above conforming limits for California's higher‑value homes.",
        "title": "Jumbo Loans in California | California Mortgage",
        "desc": "Jumbo home loans for higher‑value California properties — purchase and refinance options above conforming and high‑balance limits. Powered by West Coast Capital Mortgage Inc.",
        "eyebrow": "Loan Program", "h1": "Jumbo Loans in California",
        "lead": "Financing for California homes priced above the conforming and high‑balance limits — for primary residences, second homes, and investment properties.",
        "intro": [
            "A jumbo loan is a mortgage that exceeds the conforming (and high‑balance) loan limits set for a county. In California's higher‑cost markets, many homes fall into jumbo territory, so jumbo financing is a common path for buyers and homeowners of premium properties.",
            "Jumbo guidelines vary by lender and program. We help organize your scenario first, then a licensed mortgage professional can review the options that fit."],
        "who": ["Buyers purchasing above the county's conforming/high‑balance limit",
                "Homeowners refinancing a higher‑value California property",
                "Self‑employed borrowers needing alternative income documentation",
                "Second‑home and investment‑property buyers in premium markets"],
        "how_title": "What's typically reviewed",
        "how": ["Credit profile and history", "Down payment or available equity",
                "Income documentation (full‑doc or alternative options for self‑employed)",
                "Reserves (post‑closing assets)", "Property type and occupancy"],
        "benefits": ["Finance higher‑value California homes beyond conforming limits",
                     "Options for primary, second home, and investment properties",
                     "Full‑doc and alternative‑documentation paths for complex income",
                     "Structured guidance before a full application"],
        "faqs": [
            ("What is the jumbo loan limit in California?",
             "Jumbo applies above the conforming and high‑balance limits, which vary by county. A licensed mortgage professional can confirm the current limit for your county and whether your scenario is jumbo or high‑balance conforming."),
            ("Can self‑employed borrowers get a jumbo loan?",
             "Yes — there are jumbo options that use alternative income documentation, such as bank statements, for self‑employed borrowers. The right path depends on your full picture and is subject to review."),
            ("How much down payment is needed for a jumbo loan?",
             "Down payment requirements vary by program, credit, and property type. We help organize your numbers first so a licensed professional can review realistic options.")],
    },
    {
        "slug": "high-balance-conforming", "nav_label": "High‑Balance Conforming",
        "card": "Above the baseline limit but within your county's high‑cost ceiling.",
        "title": "High‑Balance Conforming Loans in California | California Mortgage",
        "desc": "High‑balance conforming loans for California high‑cost counties — above the baseline conforming limit but within the county ceiling, using conventional guidelines.",
        "eyebrow": "Loan Program", "h1": "High‑Balance Conforming Loans in California",
        "lead": "For California's higher‑cost counties: loan amounts above the baseline conforming limit but within the county's high‑cost ceiling — under conventional guidelines.",
        "intro": [
            "High‑balance conforming loans sit between the standard conforming limit and a full jumbo loan. In designated high‑cost California counties, the conforming ceiling is raised, so some higher loan amounts can still follow conventional guidelines instead of jumbo guidelines.",
            "Whether your scenario is high‑balance conforming or jumbo depends on your county's limit and your loan amount — something a licensed mortgage professional can confirm."],
        "who": ["Buyers in high‑cost California counties above the baseline limit",
                "Homeowners refinancing within the county high‑cost ceiling",
                "Borrowers who prefer conventional guidelines over jumbo"],
        "how_title": "What's typically reviewed",
        "how": ["Your county's current high‑cost conforming ceiling", "Credit and income documentation",
                "Down payment or equity", "Occupancy and property type"],
        "benefits": ["Conventional guidelines on higher loan amounts in high‑cost counties",
                     "Potential alternative to a full jumbo loan", "Options for low‑down‑payment scenarios where eligible"],
        "faqs": [
            ("How is high‑balance conforming different from jumbo?",
             "High‑balance conforming stays within the county's raised conforming ceiling and follows conventional guidelines; jumbo exceeds that ceiling and uses jumbo guidelines. Limits vary by county."),
            ("Do California loan limits change?",
             "Yes — conforming and high‑cost limits are set annually and vary by county. A licensed mortgage professional can confirm the current figure for your area."),
            ("Is mortgage insurance required?",
             "It depends on your down payment and program. We help organize the scenario so the options can be reviewed.")],
    },
    {
        "slug": "fha-loans", "nav_label": "FHA Loans",
        "card": "Government‑backed financing with flexible qualifying and a low down payment.",
        "title": "FHA Loans in California | California Mortgage",
        "desc": "FHA home loans in California — flexible credit guidelines and low down payment options for eligible buyers. Educational guidance, not a rate quote.",
        "eyebrow": "Loan Program", "h1": "FHA Loans in California",
        "lead": "Government‑backed financing with flexible qualifying and a low down payment — a common path for first‑time and credit‑building buyers.",
        "intro": [
            "FHA loans are insured by the Federal Housing Administration and are known for flexible qualifying and lower down‑payment options. They can be a strong fit for first‑time buyers or borrowers rebuilding credit.",
            "FHA has mortgage insurance and county loan limits. We help organize your situation, then a licensed professional can review whether FHA or another program fits best."],
        "who": ["First‑time homebuyers in California", "Borrowers with limited down payment",
                "Buyers building or rebuilding credit"],
        "how_title": "What's typically reviewed",
        "how": ["Credit profile", "Down payment source", "Income and debt‑to‑income",
                "Occupancy (primary residence)", "FHA county loan limit"],
        "benefits": ["Low down‑payment options for eligible buyers", "Flexible credit guidelines",
                     "A common path for first‑time buyers"],
        "faqs": [
            ("How much down payment does FHA require?",
             "FHA allows a low down payment for eligible borrowers; the exact amount depends on credit and program guidelines and is subject to review."),
            ("Does FHA have mortgage insurance?",
             "Yes, FHA loans include mortgage insurance. A licensed professional can explain how it works for your scenario."),
            ("Is there an FHA loan limit in California?",
             "Yes — FHA limits vary by county. We can confirm the current limit for your area.")],
    },
    {
        "slug": "va-loans", "nav_label": "VA Loans",
        "card": "$0‑down options and no monthly mortgage insurance for eligible veterans.",
        "title": "VA Loans in California | California Mortgage",
        "desc": "VA home loans in California for eligible veterans, service members, and surviving spouses — $0 down options and no monthly mortgage insurance.",
        "eyebrow": "Loan Program", "h1": "VA Loans in California",
        "lead": "A benefit earned through service: $0‑down options and no monthly mortgage insurance for eligible veterans, service members, and surviving spouses.",
        "intro": [
            "VA loans are guaranteed by the U.S. Department of Veterans Affairs and offer some of the most borrower‑friendly terms available, including no‑down‑payment options and no monthly mortgage insurance for those who qualify.",
            "Eligibility is based on service and a Certificate of Eligibility (COE). We help organize the details so a licensed professional can guide the next step."],
        "who": ["Eligible veterans and active‑duty service members",
                "National Guard and Reserve members who qualify", "Eligible surviving spouses"],
        "how_title": "What's typically reviewed",
        "how": ["Certificate of Eligibility (COE)", "Residual income and credit",
                "Occupancy (primary residence)", "VA funding fee (and exemptions)"],
        "benefits": ["$0 down payment options for eligible borrowers", "No monthly mortgage insurance",
                     "Competitive, service‑earned terms", "Reusable benefit for eligible borrowers"],
        "faqs": [
            ("Do VA loans really require no down payment?",
             "Many eligible borrowers can purchase with no down payment. Eligibility and terms are subject to VA guidelines and review."),
            ("Is there mortgage insurance on a VA loan?",
             "VA loans do not have monthly mortgage insurance. There is typically a one‑time VA funding fee, which some borrowers are exempt from."),
            ("Can the VA benefit be used more than once?",
             "Yes — the VA benefit can often be reused. A licensed professional can review your entitlement.")],
    },
    {
        "slug": "dscr-loans", "nav_label": "DSCR Investor Loans",
        "card": "Qualify an investment property using rental cash flow — not personal income.",
        "title": "DSCR Investor Loans in California | California Mortgage",
        "desc": "DSCR loans for California real estate investors — qualify rental property using projected rental income instead of personal income. LLC ownership options.",
        "eyebrow": "Investor Program", "h1": "DSCR Investor Loans in California",
        "lead": "Qualify an investment property using its rental cash flow — not your personal income. Built for real estate investors and portfolio growth.",
        "intro": [
            "A DSCR (Debt‑Service Coverage Ratio) loan qualifies an investment property based on whether its rental income covers the mortgage payment, rather than on the borrower's personal income documents. It's a popular tool for real estate investors.",
            "DSCR programs often allow ownership in an LLC and can scale across multiple properties. We help organize the scenario so a licensed professional can review the fit."],
        "who": ["Real estate investors buying or refinancing rentals",
                "Borrowers who prefer to qualify on property cash flow",
                "Investors holding property in an LLC", "Long‑term and short‑term rental owners"],
        "how_title": "What's typically reviewed",
        "how": ["Property value or purchase price", "Estimated rental income vs. payment (the DSCR)",
                "Down payment and reserves", "Property type and rental strategy", "Personal vs. LLC ownership"],
        "benefits": ["Qualify on rental income, not personal income documents",
                     "LLC ownership options", "Scalable for multiple investment properties",
                     "Long‑term or short‑term rental scenarios"],
        "faqs": [
            ("What is DSCR?",
             "DSCR is the ratio of a property's rental income to its mortgage payment. Lenders use it to gauge whether the property can support the loan. Required ratios vary by program."),
            ("Do I need tax returns for a DSCR loan?",
             "DSCR loans focus on property cash flow rather than personal income documents, though requirements vary and are subject to review."),
            ("Can I close in an LLC?",
             "Many DSCR programs allow ownership through an LLC. A licensed professional can confirm options for your scenario.")],
    },
    {
        "slug": "bank-statement-loans", "nav_label": "Bank Statement Loans",
        "card": "Use bank deposits to document income — built for self‑employed borrowers.",
        "title": "Bank Statement Loans in California | California Mortgage",
        "desc": "Bank statement loans for self‑employed California borrowers — qualify using business or personal bank deposits instead of tax returns.",
        "eyebrow": "Self‑Employed Program", "h1": "Bank Statement Loans in California",
        "lead": "For self‑employed borrowers whose tax returns don't show their full income — qualify using bank deposits instead.",
        "intro": [
            "Bank statement loans let self‑employed borrowers document income through business or personal bank deposits, typically over 12–24 months, rather than tax returns. They're designed for owners whose write‑offs reduce their taxable income.",
            "These are Non‑QM programs with their own guidelines. We help organize your statements and scenario so a licensed professional can review the options."],
        "who": ["Self‑employed borrowers and business owners",
                "1099 and contractor income earners", "Owners whose tax returns understate cash flow"],
        "how_title": "What's typically reviewed",
        "how": ["12–24 months of business or personal bank statements", "Credit profile",
                "Down payment or equity", "Business ownership and time self‑employed"],
        "benefits": ["Qualify without tax returns", "Income based on real deposit activity",
                     "Purchase or refinance options", "A fit for complex self‑employed income"],
        "faqs": [
            ("How many months of statements are needed?",
             "Programs commonly use 12 or 24 months of bank statements. The exact requirement depends on the program and is subject to review."),
            ("Whose statements can be used — business or personal?",
             "Depending on the program, business statements, personal statements, or both may be used. A licensed professional can review which fits."),
            ("Is a bank statement loan more expensive?",
             "Terms vary by program and scenario. We organize the details first so the options can be reviewed without rate promises.")],
    },
    {
        "slug": "self-employed-mortgage", "nav_label": "Self‑Employed Mortgage",
        "card": "Bank statement, 1099, P&L, and Non‑QM paths for complex income.",
        "title": "Self‑Employed Mortgage Options in California | California Mortgage",
        "desc": "Mortgage options for self‑employed California borrowers — bank statement, 1099, P&L, and Non‑QM paths for business owners and contractors.",
        "eyebrow": "Self‑Employed", "h1": "Self‑Employed Mortgage Options in California",
        "lead": "Business owners, 1099 earners, and contractors don't fit a one‑size‑fits‑all box. Several paths exist to document income the right way.",
        "intro": [
            "Self‑employed borrowers often have strong cash flow that tax returns don't fully reflect. Beyond conventional loans, options like bank statement, 1099, profit‑and‑loss, and other Non‑QM programs are designed for exactly these situations.",
            "The best path depends on how your income is structured. We help organize it, then a licensed professional can review which program fits."],
        "who": ["Business owners and the self‑employed", "1099 and contract earners",
                "Borrowers with mixed or complex income", "Owners whose returns show reduced income"],
        "how_title": "Paths we can review",
        "how": ["Bank statement loans (12–24 months of deposits)", "1099‑based income programs",
                "Profit‑and‑loss (P&L) options", "Conventional/jumbo where tax returns support it",
                "Other Non‑QM options"],
        "benefits": ["Multiple ways to document self‑employed income", "Purchase, refinance, and cash‑out scenarios",
                     "Options for complex or mixed income", "Guidance before a full application"],
        "faqs": [
            ("Can I get a mortgage if my tax returns show low income?",
             "Often yes — programs like bank statement and other Non‑QM options are designed for self‑employed borrowers whose returns understate cash flow, subject to review."),
            ("How long do I need to be self‑employed?",
             "Many programs look for a track record, but requirements vary. A licensed professional can review your situation."),
            ("Which program is best for me?",
             "It depends on your income structure and goals. Start with your situation and a licensed professional can help narrow it down.")],
    },
    {
        "slug": "conventional-loans", "nav_label": "Conventional Loans",
        "card": "A common path for primary homes, second homes, and investment properties.",
        "title": "Conventional Loans in California | California Mortgage",
        "desc": "Conventional home loans in California — a flexible, common path for primary residences, second homes, and investment properties.",
        "eyebrow": "Loan Program", "h1": "Conventional Loans in California",
        "lead": "A flexible, widely used path for many California buyers and homeowners — for primary residences, second homes, and investment properties.",
        "intro": [
            "Conventional loans follow guidelines set by Fannie Mae and Freddie Mac and are among the most common mortgages. They offer a range of down‑payment and term options and can include high‑balance amounts in high‑cost counties.",
            "We help organize your scenario so a licensed professional can review whether conventional or another program is the best fit."],
        "who": ["Buyers with established credit and income", "Homeowners refinancing to change rate or term",
                "Second‑home and investment‑property buyers"],
        "how_title": "What's typically reviewed",
        "how": ["Credit profile", "Down payment or equity", "Income and debt‑to‑income",
                "Occupancy and property type", "Mortgage insurance (if applicable)"],
        "benefits": ["Flexible down‑payment and term options", "Primary, second‑home, and investment options",
                     "Mortgage‑insurance can often be removed as equity grows", "High‑balance options in high‑cost counties"],
        "faqs": [
            ("How much down payment do I need for a conventional loan?",
             "Down payment options vary by program, occupancy, and credit. We help organize your numbers so realistic options can be reviewed."),
            ("Can I avoid mortgage insurance?",
             "Mortgage insurance depends on your down payment and program; it can often be removed later as equity grows. A licensed professional can explain the options."),
            ("Can I use a conventional loan for a rental property?",
             "Yes, conventional financing can be used for investment properties, subject to guidelines and review.")],
    },
    {
        "slug": "cash-out-refinance", "nav_label": "Cash‑Out Refinance",
        "card": "Access home equity for renovations, investing, or consolidation.",
        "title": "Cash‑Out Refinance in California | California Mortgage",
        "desc": "Cash‑out refinance options in California — access home equity for renovations, investing, debt consolidation, or other goals. Subject to review and approval.",
        "eyebrow": "Refinance", "h1": "Cash‑Out Refinance in California",
        "lead": "Turn a portion of your California home equity into funds for renovations, investing, debt consolidation, or other goals.",
        "intro": [
            "A cash‑out refinance replaces your current mortgage with a new, larger loan and returns the difference to you in cash, based on your available equity. Homeowners use it for renovations, investment, consolidating higher‑interest debt, and more.",
            "Whether a cash‑out refinance makes sense depends on your equity, goals, and the overall numbers. We help organize the scenario for review."],
        "who": ["Homeowners with built‑up equity", "Owners planning renovations or investments",
                "Borrowers consolidating higher‑interest debt"],
        "how_title": "What's typically reviewed",
        "how": ["Current home value and equity", "Existing loan balance",
                "Credit and income", "Goals for the funds and how long you'll keep the property"],
        "benefits": ["Access equity for flexible goals", "Potentially consolidate higher‑interest debt",
                     "Available on primary, second‑home, and investment properties (where eligible)"],
        "faqs": [
            ("How much equity can I access?",
             "The amount depends on your home value, loan balance, program limits, and review. We help organize the numbers first."),
            ("Is a cash‑out refinance a good idea?",
             "It depends on your goals, your rate, closing costs, and how long you'll keep the property. A licensed professional can review the full picture."),
            ("Can I do a cash‑out refinance on a rental?",
             "Yes, cash‑out options exist for investment properties, subject to guidelines and review.")],
    },
    {
        "slug": "non-qm-loans", "nav_label": "Non‑QM Loans",
        "card": "Flexible programs for unique income, credit, or property scenarios.",
        "title": "Non‑QM Loans in California | California Mortgage",
        "desc": "Non‑QM loans in California — flexible mortgage programs for self‑employed income, investors, and unique credit or property scenarios.",
        "eyebrow": "Loan Program", "h1": "Non‑QM Loans in California",
        "lead": "Flexible programs for borrowers who don't fit standard guidelines — self‑employed income, investors, and unique credit or property situations.",
        "intro": [
            "Non‑QM (non‑qualified mortgage) programs use alternative ways to document income and evaluate a borrower, beyond standard conventional or government guidelines. They include bank statement, DSCR, asset‑based, and other options.",
            "Non‑QM is broad — the right path depends entirely on your scenario. We help organize it for a licensed professional to review."],
        "who": ["Self‑employed and business‑owner borrowers", "Real estate investors",
                "Borrowers with recent credit events or unique situations", "Foreign‑national and asset‑based scenarios (where eligible)"],
        "how_title": "Common Non‑QM paths",
        "how": ["Bank statement loans", "DSCR investor loans", "Asset‑based qualification",
                "1099 and P&L options", "Other alternative‑documentation programs"],
        "benefits": ["Flexible documentation and qualifying", "Solutions for complex or non‑traditional income",
                     "Purchase, refinance, and investment scenarios", "A second look when a bank says no"],
        "faqs": [
            ("What does Non‑QM mean?",
             "Non‑QM means a loan that doesn't meet the standard 'qualified mortgage' guidelines, using alternative documentation or qualifying methods instead. Terms vary widely by program."),
            ("Are Non‑QM loans safe?",
             "Non‑QM loans are legitimate mortgage programs offered by licensed lenders; they simply use alternative qualifying. All options are subject to review and approval."),
            ("Who should consider Non‑QM?",
             "Self‑employed borrowers, investors, and those with unique credit or property scenarios often benefit. Start with your situation for a professional review.")],
    },
    {
        "slug": "second-home-financing", "nav_label": "Second Home Financing",
        "card": "Vacation and second‑home options across California.",
        "title": "Second Home Financing in California | California Mortgage",
        "desc": "Second home and vacation home financing in California — options for buyers purchasing a getaway or part‑time residence.",
        "eyebrow": "Loan Program", "h1": "Second Home Financing in California",
        "lead": "Buying a vacation place or part‑time residence in California? Second‑home financing has its own guidelines, separate from primary and investment loans.",
        "intro": [
            "Second‑home (vacation home) financing is for a property you'll use part of the year, not as a rental business. It typically follows different occupancy and down‑payment guidelines than primary or investment loans.",
            "We help organize your scenario so a licensed professional can review whether a second‑home or investment structure fits your plans."],
        "who": ["Buyers purchasing a California vacation or getaway home",
                "Owners refinancing an existing second home", "Borrowers splitting time between residences"],
        "how_title": "What's typically reviewed",
        "how": ["Intended use and occupancy", "Down payment or equity", "Credit and income",
                "Property type and location"],
        "benefits": ["Financing tailored to part‑time residences", "Conventional and jumbo options where eligible",
                     "Guidance on second‑home vs. investment structure"],
        "faqs": [
            ("What's the difference between a second home and an investment property?",
             "A second home is for personal part‑time use; an investment property is held to generate rental income. They follow different guidelines, which a licensed professional can explain."),
            ("How much down payment for a second home?",
             "It varies by program and credit. We help organize the numbers so options can be reviewed."),
            ("Can I rent out my second home?",
             "Occupancy rules differ by program; significant rental use may make it an investment property. A licensed professional can review your plans.")],
    },
    {
        "slug": "condo-financing", "nav_label": "Condo Financing",
        "card": "Condo‑specific guidelines for California condominium purchases and refinances.",
        "title": "Condo Financing in California | California Mortgage",
        "desc": "Condo financing in California — condominium‑specific mortgage guidelines for purchases and refinances, including warrantable and non‑warrantable scenarios.",
        "eyebrow": "Loan Program", "h1": "Condo Financing in California",
        "lead": "Condominiums have their own financing guidelines. We help organize condo scenarios — including warrantable and non‑warrantable situations — for review.",
        "intro": [
            "Financing a condo involves reviewing both you as the borrower and the condo project itself (HOA, budget, occupancy mix, and more). Projects are often classified as 'warrantable' or 'non‑warrantable,' which affects available programs.",
            "If a condo has been difficult to finance elsewhere, there may still be a path. We help organize the details for a licensed professional to review."],
        "who": ["Buyers purchasing a California condominium", "Owners refinancing a condo",
                "Borrowers facing non‑warrantable condo challenges"],
        "how_title": "What's typically reviewed",
        "how": ["Borrower credit, income, and down payment", "Condo project status (warrantable vs. non‑warrantable)",
                "HOA and project details", "Occupancy and property type"],
        "benefits": ["Guidance on warrantable and non‑warrantable condos", "Conventional, government, and Non‑QM options where eligible",
                     "A second look when a condo was declined elsewhere"],
        "faqs": [
            ("What is a non‑warrantable condo?",
             "A non‑warrantable condo is a project that doesn't meet standard agency guidelines (due to occupancy mix, litigation, budget, or other factors). Specialized programs may still finance it, subject to review."),
            ("Why was my condo loan denied?",
             "Condo denials often relate to the project rather than the borrower. A licensed professional can review the project details and possible options."),
            ("Are condo loans different from house loans?",
             "Yes — condo financing adds a review of the project and HOA in addition to the borrower, which can affect the program and terms.")],
    },
]

def _ul(items):
    return '<ul class="check-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def faq_jsonld(faqs):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>\n'

def loan_cards(exclude=None):
    cards = ""
    for d in LOANS:
        if d["slug"] == exclude:
            continue
        cards += (f'<a class="card audience-card" href="/{d["slug"]}.html">'
                  f'<h3>{d["nav_label"]}</h3><p>{d["card"]}</p>'
                  f'<span class="link-arrow">Learn more <span aria-hidden="true">&rarr;</span></span></a>')
    return cards

def loan_body(d):
    intro = "".join(f"<p>{p}</p>" for p in d["intro"])
    faqs = "".join(f'<div class="info-card"><h3>{q}</h3><p>{a}</p></div>' for q, a in d["faqs"])
    return hero(d["eyebrow"], d["h1"], d["lead"]) + f'''
<section class="section">
  <div class="container article prose">
    {intro}
    <h2>Who it's for</h2>
    {_ul(d["who"])}
    <h2>{d["how_title"]}</h2>
    {_ul(d["how"])}
    <h2>Why borrowers choose it</h2>
    {_ul(d["benefits"])}
  </div>
</section>

<section class="section section-tint">
  <div class="container article">
    <div class="section-head" style="text-align:left;margin-bottom:1.2rem">
      <p class="eyebrow gold">FAQ</p>
      <h2>{d["nav_label"]} &mdash; common questions</h2>
    </div>
    <div class="edu-grid">{faqs}</div>
  </div>
</section>

<section class="section">
  <div class="container article">
    <h2>Explore other California loan programs</h2>
    <div class="edu-grid">{loan_cards(exclude=d["slug"])}</div>
''' + cta_block(
        "See Which Program Fits Your Scenario",
        "Start with your situation &mdash; a few simple questions, then a licensed mortgage professional can review the right path.",
        [BTN_START, BTN_CONTACT_PRO]) + compliance(
        "This information is for educational purposes only and is not a loan approval, loan commitment, or rate quote. "
        "Program availability, terms, and eligibility are subject to review and approval by a licensed mortgage professional.") + '''
  </div>
</section>'''

loan_options_body = hero(
    "Loan Options",
    "California Mortgage Loan Programs",
    "Explore the loan programs we work with across California &mdash; purchase, refinance, jumbo, government, self-employed, and investor options. Not sure which fits? Start with your situation."
) + '''
<section class="section">
  <div class="container article">
    <div class="edu-grid">''' + loan_cards() + '''</div>
''' + cta_block(
    "Not Sure Which Program Fits?",
    "You do not need to know the program. Start with your situation and a licensed mortgage professional can help narrow it down.",
    [BTN_START, BTN_CONTACT_PRO]) + compliance() + '''
  </div>
</section>'''

LOAN_ENTRIES = [
    ("loan-options.html", "Loan Options | California Mortgage Programs",
     "Explore California mortgage loan programs — jumbo, high-balance conforming, FHA, VA, DSCR, bank statement, self-employed, conventional, cash-out refinance, Non-QM, second home, and condo financing.",
     loan_options_body, "/loan-options"),
]
for _d in LOANS:
    LOAN_ENTRIES.append((f'{_d["slug"]}.html', _d["title"], _d["desc"], loan_body(_d),
                         f'/{_d["slug"]}', faq_jsonld(_d["faqs"])))


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

ALL_PAGES = PAGES + LOAN_ENTRIES

if __name__ == "__main__":
    for entry in ALL_PAGES:
        path, title, desc, body, canon = entry[:5]
        head_extra = entry[5] if len(entry) > 5 else ""
        page(path, title, desc, body, canon, head_extra)
    print("Done:", len(ALL_PAGES), "pages.")
