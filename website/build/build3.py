#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from chrome import (head, header, footer, chat, page_hero, cta_band,
                    PHONE, PHONE_TEL, NMLS, PROGRAMS)
OUT = "/sessions/keen-eloquent-planck/mnt/outputs/site"
def write(name, html):
    open(os.path.join(OUT, name),"w",encoding="utf-8").write(html); print("wrote",name)

def sidebar(active):
    links="".join(
        f'<a href="{u}" style="display:block;padding:10px 14px;border-radius:8px;{ "background:var(--gold-soft);color:var(--gold-2);font-weight:600" if u==active else "color:var(--text)"}">{e} {n}</a>'
        for u,n,e in PROGRAMS)
    return f"""<aside style="position:sticky;top:90px">
      <div class="card" style="padding:16px">
        <h4 style="text-transform:uppercase;font-size:.78rem;letter-spacing:.12em;color:var(--muted);margin-bottom:10px">Loan Programs</h4>
        {links}
      </div>
      <div class="card" style="margin-top:18px;background:var(--navy);color:#fff;text-align:center">
        <h3 style="color:#fff">Ready to start?</h3>
        <p style="color:#c2cedd;font-size:.92rem">Get pre-approved in minutes.</p>
        <a class="btn btn-gold" href="apply.html" style="width:100%;justify-content:center">Apply Now</a>
        <p style="margin-top:12px;font-size:.9rem"><a href="tel:{PHONE_TEL}" style="color:var(--gold)">📞 {PHONE}</a></p>
      </div>
    </aside>"""

def loan_page(slug, name, emoji, hero_sub, intro, sections, faqs, highlights):
    h = head(f"{name} in California", hero_sub, "programs")
    h += header("programs")
    h += page_hero(f'<a href="conventional.html">Loan Programs</a> / {name}', name, hero_sub)
    # highlight strip
    hl="".join(f'<div class="card fade" style="text-align:center;padding:20px"><div class="ico" style="margin:0 auto 12px">{e}</div><b style="display:block;color:var(--navy)">{t}</b><span class="muted" style="font-size:.88rem">{d}</span></div>' for e,t,d in highlights)
    body=f'<p class="lead">{intro}</p>'
    for title, paras in sections:
        body+=f'<h2>{title}</h2>'
        for p in paras:
            if isinstance(p,list):
                body+='<ul>'+''.join(f'<li>{i}</li>' for i in p)+'</ul>'
            else:
                body+=f'<p>{p}</p>'
    if faqs:
        body+='<h2>Frequently asked questions</h2>'
        for q,ans in faqs:
            body+=f'<details class="faq"><summary>{q}</summary><div class="a">{ans}</div></details>'
    h += f"""
<section class="section tight"><div class="container">
  <div class="grid grid-4 fade">{hl}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
  <div style="display:grid;grid-template-columns:1fr 300px;gap:40px;align-items:start">
    <article class="article" style="max-width:none">{body}</article>
    {sidebar(slug+'.html')}
  </div>
</div></section>
"""
    h += cta_band() + footer() + chat()
    write(slug+".html", h)

# ----- Loan data (real copy adapted from existing site) -----
loan_page("conventional","Conventional Mortgage","🏠",
  "Flexible terms and competitive rates with as little as 3% down for qualified buyers in California, Florida and Washington.",
  "A conventional mortgage is one that's not guaranteed or insured by the federal government. Instead, these loans are available through private lenders such as banks, credit unions, and mortgage companies — and they remain the most popular financing choice for well-qualified buyers.",
  [("What is a conventional mortgage?",
    ["Because they aren't government-backed, conventional loans follow guidelines set by Fannie Mae and Freddie Mac. They offer flexible terms, competitive rates, and can be used for primary homes, second homes, and investment properties.",
     "Down payments can start as low as 3% for qualifying first-time buyers, though putting 20% down lets you avoid private mortgage insurance (PMI) entirely."]),
   ("Conventional mortgage requirements",
    [["A credit score of at least 620 (higher scores earn better rates)",
      "A down payment of 3%–20% depending on the program",
      "A debt-to-income ratio generally at or below 43%",
      "Steady, verifiable income and employment history",
      "Sufficient reserves for some loan amounts"]]),
   ("Private mortgage insurance (PMI)",
    ["If your down payment is below 20%, lenders typically require PMI to protect against default. The good news: PMI can be cancelled once you reach 20% equity, lowering your monthly payment over time."]),
   ("Advantages of a conventional loan",
    [["Available for primary, secondary, and investment properties",
      "No upfront mortgage insurance fee like FHA loans",
      "PMI can be removed at 20% equity",
      "Competitive rates for strong credit profiles",
      "Higher loan limits than FHA in most areas"]])],
  [("How much do I need to put down?","As little as 3% for qualified first-time buyers, but 20% avoids PMI. We'll help you find the sweet spot for your budget."),
   ("What credit score do I need?","Generally 620 or higher. Stronger scores unlock lower rates — we can review your profile for free.")],
  [("💰","From 3% Down","Low down-payment options"),("📊","No Upfront MI","Unlike FHA loans"),("🏘️","Any Property","Primary, second, investment"),("✂️","Cancel PMI","Once you hit 20% equity")])

loan_page("fha","FHA Home Loan","🔑",
  "Just 3.5% down and flexible credit requirements — a favorite among first-time homebuyers in Los Angeles and beyond.",
  "FHA home loans are insured by the Federal Housing Administration and provided by FHA-approved lenders. With low down payments and forgiving credit guidelines, they're one of the most accessible paths to homeownership — especially for first-time buyers.",
  [("What is an FHA home loan?",
    ["FHA loans come with fixed terms of 15 or 30 years and are a popular choice among first-time homebuyers as well as buyers with less-than-perfect credit. Because the government insures the loan, lenders can offer more flexible qualification standards."]),
   ("Mortgage insurance premiums (MIP)",
    ["FHA loans require both an upfront mortgage insurance premium and an annual premium paid monthly. This insurance is what allows the low down payment and flexible credit — factor it into your monthly cost when comparing to conventional financing."]),
   ("How to qualify for an FHA loan",
    [["A credit score as low as 580 with 3.5% down (or 500–579 with 10% down)",
      "A debt-to-income ratio typically up to 43% (sometimes higher with compensating factors)",
      "Steady employment and verifiable income",
      "The home must be your primary residence",
      "The property must meet FHA minimum standards"]]),
   ("Advantages of FHA loans",
    [["Down payments as low as 3.5%",
      "Flexible credit requirements",
      "Gift funds allowed for the down payment",
      "Assumable by a future buyer",
      "Great for first-time buyers"]])],
  [("Can I use gift money for my down payment?","Yes — FHA allows your entire down payment to come from an eligible gift, such as from family."),
   ("Is FHA only for first-time buyers?","No. While popular with first-timers, FHA loans are available to any qualified buyer purchasing a primary residence.")],
  [("🔑","3.5% Down","Low entry point"),("📉","580 Score","Flexible credit"),("🎁","Gift Funds OK","For down payment"),("👨‍👩‍👧","First-Timers","Most popular choice")])

loan_page("va","VA Home Loan","🎖️",
  "$0 down and no PMI for eligible veterans, active-duty service members, and their families.",
  "VA home loans are guaranteed by the U.S. Department of Veterans Affairs. Created in 1944, the program has helped more than 24 million veterans, active-duty members, and their families purchase or refinance a home — often with no down payment at all.",
  [("What is a VA home loan?",
    ["VA loans are among the most powerful benefits available to those who served. The VA guarantees a portion of the loan, allowing approved lenders to offer $0 down financing with no private mortgage insurance and competitive rates."]),
   ("How to qualify for a VA loan",
    [["A valid Certificate of Eligibility (COE) based on your service",
      "Sufficient income to cover the mortgage and living expenses",
      "A satisfactory credit profile (no strict VA minimum, though lenders set their own)",
      "The home must be your primary residence"]]),
   ("Types of VA loans",
    [["VA purchase loans for buying a primary home",
      "VA Interest Rate Reduction Refinance Loans (IRRRL / streamline)",
      "VA cash-out refinances to tap equity",
      "Loans for energy-efficient improvements"]]),
   ("Benefits of a VA loan",
    [["$0 down payment for eligible borrowers",
      "No private mortgage insurance",
      "Competitive interest rates",
      "Limited closing costs",
      "No prepayment penalty"]])],
  [("Do I need a down payment?","Most eligible borrowers can finance 100% of the purchase price with $0 down."),
   ("How do I get my Certificate of Eligibility?","We help you request your COE as part of the application — it confirms your VA loan entitlement based on your service.")],
  [("🎖️","$0 Down","For eligible vets"),("🚫","No PMI","Ever"),("💲","Low Costs","Limited closing costs"),("🔁","Streamline Refi","Easy IRRRL option")])

loan_page("usda","USDA Home Loan","🌾",
  "$0 down financing for eligible rural and suburban homebuyers, backed by the U.S. Department of Agriculture.",
  "USDA loans make purchasing a home more affordable for buyers in eligible rural and many suburban areas. The U.S. Department of Agriculture backs these loans much like the VA backs loans for veterans — meaning $0 down and lower costs for those who qualify.",
  [("What is a USDA home mortgage?",
    ["With government backing, USDA loans offer 100% financing and reduced mortgage insurance compared to other low-down-payment options. Eligibility is based on the property's location and your household income."]),
   ("How to qualify for a USDA loan",
    [["The property must be in a USDA-eligible area",
      "Household income must fall within local limits",
      "The home must be your primary residence",
      "A credit score around 640 is typically preferred"]]),
   ("Types of USDA programs",
    [["Guaranteed Loans for moderate-income buyers through approved lenders",
      "Direct Loans for low- and very-low-income applicants",
      "Home Improvement Loans and grants for eligible repairs"]]),
   ("Benefits of a USDA loan",
    [["$0 down payment",
      "Lower mortgage insurance than FHA",
      "Competitive fixed rates",
      "Flexible credit guidelines"]])],
  [("How do I know if a home qualifies?","Eligibility is location-based — we can check any address against USDA maps for you in seconds."),
   ("Are there income limits?","Yes, limits vary by county and household size. We'll confirm whether you qualify.")],
  [("🌾","$0 Down","100% financing"),("📍","Location-Based","Rural & suburban"),("📉","Low MI","Cheaper than FHA"),("💵","Income Limits","Built for affordability")])

loan_page("jumbo","Jumbo Mortgage","💎",
  "Financing above conforming loan limits — ideal for higher-priced homes across California, Florida and Washington.",
  "A jumbo home loan is financing that exceeds the limits set by the Federal Housing Finance Agency. Although they're non-conforming, jumbo loans still follow Consumer Financial Protection Bureau guidelines and are essential for purchasing higher-priced properties.",
  [("What is a jumbo mortgage?",
    ["When a home's price exceeds the conforming loan limit for your county, a jumbo loan bridges the gap. These loans let qualified buyers finance luxury and high-cost-area homes that conventional limits won't cover."]),
   ("Jumbo vs conforming loan limits",
    ["Conforming limits are set annually and vary by county. Loans above that threshold are 'jumbo.' In high-cost California markets, jumbo financing is common for primary homes — not just luxury estates."]),
   ("How to qualify for a jumbo mortgage",
    [["A strong credit score, generally 700 or higher",
      "A larger down payment (often 10–20%+)",
      "Significant cash reserves",
      "A low debt-to-income ratio",
      "Full documentation of income and assets"]]),
   ("Benefits of a jumbo mortgage",
    [["Finance high-value properties in a single loan",
      "Competitive rates for strong borrowers",
      "Fixed and adjustable options",
      "Available for primary, second, and investment homes"]])],
  [("How much can I borrow?","Jumbo loan amounts can run well into the millions depending on your profile. Let's review what you'd qualify for."),
   ("Are jumbo rates higher?","Not necessarily — for strong borrowers, jumbo rates are often very competitive with conforming loans.")],
  [("💎","High Limits","Above conforming"),("🏛️","Luxury Homes","High-cost areas"),("📈","Fixed or ARM","Flexible structures"),("🤝","Competitive","Great rates for strong files")])

loan_page("fixed-rate","Fixed-Rate Mortgage","📈",
  "Predictable payments that never change — the most popular financing for buyers who value stability.",
  "A fixed-rate mortgage has an interest rate that stays the same for the entire life of the loan. Your principal-and-interest payment never changes, which is exactly why it's the most popular type of home financing — it offers predictability you can plan your life around.",
  [("What is a fixed-rate mortgage?",
    ["With a fixed rate, market swings don't touch your monthly principal and interest. Whether rates rise or fall, your payment is locked, making budgeting simple for the long haul."]),
   ("Types of fixed-rate mortgages",
    [["30-year fixed — the lowest monthly payment, most popular",
      "20-year fixed — a middle ground on term and interest",
      "15-year fixed — higher payment, far less interest paid overall",
      "10-year fixed — fastest payoff for aggressive savers"]]),
   ("Advantages of a fixed-rate mortgage",
    [["Payment stability for the life of the loan",
      "Protection from rising interest rates",
      "Easy, predictable budgeting",
      "Simple to understand"]]),
   ("Drawbacks to consider",
    ["Fixed rates can start slightly higher than the initial rate on an adjustable-rate mortgage. If you plan to move or refinance within a few years, an ARM may save money short-term — we'll help you weigh it."])],
  [("Which term is right for me?","If you want the lowest payment, go 30-year. If you want to pay less interest and own sooner, consider 15-year. We'll model both."),
   ("Can I pay it off early?","Yes — our fixed-rate loans have no prepayment penalty, so extra payments shorten your loan and save interest.")],
  [("📈","Locked Rate","Never changes"),("🛡️","Rate Protection","Beat future hikes"),("🗓️","Easy Budgeting","Same payment"),("⏱️","10–30 Yrs","Choose your term")])

loan_page("refinance","Mortgage Refinancing","🔁",
  "Lower your rate, shorten your term, or tap your home's equity by replacing your current loan with a better one.",
  "When you refinance, you replace your current home loan with a new one. Like your original mortgage, refinancing requires an application, underwriting, and closing — but the payoff can be a lower rate, a shorter term, or cash from your equity.",
  [("The refinancing process",
    ["You file an application, go through underwriting, and close on the new loan — which pays off and replaces the old one. We make each step clear and handle the heavy lifting so it's far simpler than your first mortgage felt."]),
   ("Reasons to refinance",
    [["Lower your interest rate and monthly payment",
      "Shorten your loan term to pay off faster",
      "Switch from an adjustable to a fixed rate",
      "Take cash out for renovations or debt consolidation",
      "Remove mortgage insurance once you have equity"]]),
   ("Types of refinancing",
    [["Rate-and-term refinance — change your rate, term, or both",
      "Cash-out refinance — borrow against your equity",
      "Streamline refinance — simplified process for FHA and VA loans"]]),
   ("Is it worth it?",
    ["The key is your break-even point — when monthly savings cover your closing costs. Use our refinance calculator to see your number, then let us confirm it with a real quote."])],
  [("When should I refinance?","Often when rates drop at least 0.5–1% below your current rate, or when your goals change. We'll run the math with you for free."),
   ("How long does it take?","Most refinances close in roughly 30 days. Streamline options for FHA/VA can be faster.")],
  [("📉","Lower Rate","Cut your payment"),("⏱️","Shorter Term","Pay off sooner"),("💵","Cash Out","Use your equity"),("🔄","FHA/VA Streamline","Fast & simple")])

loan_page("renovation-203k","Renovation Mortgage 203(k)","🔨",
  "Buy or refinance a home that needs work and roll the renovation costs into a single FHA-insured loan.",
  "With a 203(k) loan, you can buy or refinance a home that needs repairs and fold the renovation costs right into your mortgage. Because these loans are insured by the Federal Housing Administration, they often come with more lenient qualification requirements than other renovation financing.",
  [("What is a 203(k) renovation mortgage?",
    ["Instead of juggling a purchase loan plus a separate construction loan, the 203(k) combines the home price and the renovation budget into one FHA-insured mortgage with one monthly payment."]),
   ("Limited vs standard 203(k)",
    [["Limited 203(k) — for smaller projects up to a set cost cap; ideal for cosmetic updates and minor repairs",
      "Standard 203(k) — for major renovations, structural work, and larger budgets, with a HUD consultant involved"]]),
   ("How to qualify for a 203(k)",
    [["Meet FHA credit and down-payment guidelines (as low as 3.5% down)",
      "The home must be your primary residence",
      "Renovation plans and contractor bids are required",
      "The property must meet FHA standards after the work"]]),
   ("The 203(k) process",
    ["You get approved based on the home's projected after-renovation value, choose licensed contractors, and the renovation funds are held in escrow and released as work is completed. We coordinate the moving parts with you."])],
  [("Can I buy a fixer-upper with this?","Yes — that's exactly what it's for. You finance the purchase and the repairs together."),
   ("How much can I borrow for renovations?","It depends on the loan type and the home's after-repair value. We'll size the right program for your project.")],
  [("🔨","Buy + Renovate","One loan"),("🏚️","Fixer-Uppers","Turn into dream homes"),("🔑","3.5% Down","FHA-backed"),("📦","Funds in Escrow","Released as you go")])

loan_page("reverse","Reverse Mortgage","🌅",
  "For homeowners 62+ — convert a portion of your home equity into cash without monthly mortgage payments.",
  "A reverse mortgage is a type of loan where a homeowner withdraws a portion of their home equity but doesn't have to repay the loan until they leave the house. It's designed to help older homeowners turn equity into usable funds while staying in their home.",
  [("What is a reverse mortgage?",
    ["With a reverse mortgage, the lender pays you — not the other way around. The loan balance is repaid when you sell the home, move out permanently, or pass away. You retain ownership and continue paying property taxes, insurance, and upkeep."]),
   ("How to qualify for a reverse mortgage",
    [["Be at least 62 years old",
      "Own the home outright or have significant equity",
      "Live in the home as your primary residence",
      "Stay current on property taxes, insurance, and maintenance",
      "Complete a required HUD counseling session"]]),
   ("Ways to receive your proceeds",
    [["A lump sum at closing",
      "Fixed monthly payments",
      "A line of credit you draw from as needed",
      "A combination of these options"]]),
   ("Benefits of a reverse mortgage",
    [["No monthly mortgage payments required",
      "Stay in your home",
      "Funds are generally tax-free (consult a tax advisor)",
      "Flexible ways to receive money"]])],
  [("Do I still own my home?","Yes. You keep title to your home. The loan is repaid when you sell, move out, or pass away."),
   ("Is counseling required?","Yes — HUD requires independent counseling to make sure a reverse mortgage is right for you. We'll point you to an approved counselor.")],
  [("🌅","Age 62+","For older homeowners"),("🚫","No Monthly Pmt","Required"),("🏠","Stay Home","Keep your title"),("💳","Flexible Payout","Lump, monthly, or LOC")])

print("BUILD3 loan pages done")

# ---------------- ABOUT ----------------
ab = head("About Our Founder & CEO","Meet Anatoliy Kanevsky, Founder & CEO of West Coast Capital Mortgage Inc. — a California-licensed broker with 20+ years in residential lending.","about")
ab += header("about")
ab += page_hero("About","Honest guidance. Clear answers. Strong results.","Meet the team and the founder behind West Coast Capital Mortgage Inc.")
ab += f"""
<section class="section"><div class="container">
  <div class="split">
    <div class="media-frame fade" style="text-align:center;padding:46px 30px">
      <img src="assets/img/logo.png" alt="Pegasus logo" style="height:120px;margin:0 auto 18px">
      <h3 style="color:#fff">Anatoliy Kanevsky</h3>
      <p style="color:var(--gold);font-weight:600">Founder &amp; CEO</p>
      <p style="color:#c2cedd;font-size:.95rem">California Broker License since July 16, 2009 · {NMLS}</p>
    </div>
    <div class="fade">
      <span class="eyebrow">Our Story</span>
      <h2>Two decades of lending, built on trust</h2>
      <p>Anatoliy Kanevsky is the Founder and CEO of West Coast Capital Mortgage Inc., with a career in residential lending that began in 2004 as a loan officer at Finance Connection. From day one, he learned the business from the ground up — working directly with borrowers and guiding families through one of the most important financial decisions of their lives.</p>
      <p>In 2009 he earned his California Broker License, opening the door to working independently and serving clients at the highest professional level. Over the years his network grew organically through referrals from clients who trusted his straightforward approach.</p>
      <p>Alongside his mortgage work, Anatoliy expanded into real estate development as CEO of California Residential Development Partners LLC, specializing in high-end residential construction throughout the Los Angeles area. This dual background — financing and construction — gives him a perspective few professionals possess: he understands the full lifecycle of a property, from financial structuring to the build itself.</p>
      <p>Today, under his leadership, West Coast Capital Mortgage Inc. is recognized for integrity, reliability, and a client-focused approach. The mission stays the same: <b>to help people move forward in life.</b></p>
    </div>
  </div>
</div></section>
<section class="section bg-mist"><div class="container">
  <div class="sec-head"><span class="eyebrow">What we value</span><h2>Why clients choose us</h2></div>
  <div class="grid grid-3">
    <div class="card fade"><div class="ico">🤝</div><h3>Integrity first</h3><p>Honest guidance and clear answers — we tell you what you need to know, not just what you want to hear.</p></div>
    <div class="card fade"><div class="ico">🏗️</div><h3>Unmatched insight</h3><p>Financing plus construction expertise means smarter advice for homeowners and investors alike.</p></div>
    <div class="card fade"><div class="ico">⚡</div><h3>Strong results</h3><p>Competitive rates, a modern process, and a team that's with you to the closing table.</p></div>
  </div>
</div></section>
"""
ab += cta_band() + footer() + chat()
write("about.html", ab)

# ---------------- REVIEWS ----------------
ALL_REVIEWS = [
 ("Helpful service made the whole loan process a positive experience. The loan was amazing for my investment property — I will definitely come back again.","Google Reviewer","Investment Property","★★★★★"),
 ("Anatoliy and his team made our first home purchase painless. They explained every step in plain English and got us a great rate on our FHA loan.","Maria & Daniel R.","First-Time Buyers","★★★★★"),
 ("Refinanced and cut my monthly payment significantly. Honest advice and no surprises at closing — exactly what you want.","James T.","Refinance","★★★★★"),
 ("As a veteran, the VA loan process can be confusing. They handled my Certificate of Eligibility and got me into my home with $0 down.","Robert M.","VA Loan","★★★★★"),
 ("We needed a jumbo loan for our LA home and they made a complex process feel simple. Responsive and professional throughout.","Priya & Sanjay K.","Jumbo Loan","★★★★★"),
 ("Great experience from start to finish. Quick communication, fair rate, and they actually answered the phone when I called.","Linda C.","Conventional","★★★★★"),
]
rev_cards="".join(
 f'<div class="review fade"><div class="stars">{s}</div><p>"{q}"</p><div class="who"><div class="av">{n[0]}</div><div><b>{n}</b><span>{role}</span></div></div></div>'
 for q,n,role,s in ALL_REVIEWS)
rv = head("Real Customer Reviews & Testimonials","Read real reviews from West Coast Capital Mortgage clients — first-time buyers, veterans, refinancers, and investors across CA, FL & WA.","reviews")
rv += header("reviews")
rv += page_hero("Reviews","What our clients say","Real experiences from families and investors we've helped finance their futures.")
rv += f"""
<section class="section tight"><div class="container center fade">
  <div style="font-size:3rem;color:var(--gold)">★★★★★</div>
  <h2 style="margin-top:6px">Rated 5.0 by our clients</h2>
  <p class="lead">We're proud of the relationships we've built. Here's what people say about working with us.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-3">{rev_cards}</div>
  <div class="center" style="margin-top:40px">
    <div class="card" style="max-width:520px;margin:0 auto;text-align:center">
      <h3>Worked with us?</h3>
      <p class="muted">We'd love to hear about your experience — and so would future homebuyers.</p>
      <a class="btn btn-gold" href="https://www.google.com/search?q=West+Coast+Capital+Mortgage" target="_blank" rel="noopener">Leave us a Google review →</a>
    </div>
  </div>
</div></section>
"""
rv += cta_band() + footer() + chat()
write("reviews.html", rv)

# ---------------- BLOG ----------------
POSTS = [
 ("Buying Your First Home in California: A 2026 Roadmap","First-Time Buyers","From budgeting and credit to closing day, here's a clear, step-by-step path to your first home in today's market.","🏡"),
 ("FHA vs Conventional: Which Loan Is Right for You?","Loan Programs","We break down down payments, mortgage insurance, and credit requirements so you can choose with confidence.","⚖️"),
 ("Should You Refinance? How to Find Your Break-Even Point","Refinancing","Refinancing only pays off if you stay past your break-even. Here's how to run the numbers in minutes.","🔁"),
 ("VA Loan Benefits Every Veteran Should Know","VA Loans","$0 down, no PMI, and a streamline refinance option — make sure you're using every benefit you've earned.","🎖️"),
 ("Jumbo Loans Explained for High-Cost California Markets","Jumbo Loans","When conforming limits won't cut it, here's how jumbo financing works and what it takes to qualify.","💎"),
 ("How Much House Can You Really Afford?","Home Buying","Lenders use the 43% DTI guideline — but the right payment is the one that fits your life. Here's how to find it.","🧮"),
]
post_cards="".join(
 f'<a class="card fade" href="contact.html"><div class="ico">{e}</div><span class="pill">{cat}</span><h3 style="margin-top:12px">{t}</h3><p>{d}</p><span class="more">Read more →</span></a>'
 for t,cat,d,e in POSTS)
bl = head("Mortgage Blog","Mortgage tips, loan program guides, and home-buying advice from West Coast Capital Mortgage — serving CA, FL & WA.","blog")
bl += header("blog")
bl += page_hero("Blog","The Mortgage Blog","Plain-English guides to help you make smart, confident decisions about your home loan.")
bl += f"""
<section class="section"><div class="container">
  <div class="grid grid-3">{post_cards}</div>
  <div class="callout center" style="max-width:680px;margin:40px auto 0">
    <b>Have a question we haven't covered?</b> Ask our AI assistant in the corner, or <a href="contact.html">reach out directly</a> — we're always happy to help.
  </div>
</div></section>
"""
bl += cta_band() + footer() + chat()
write("blog.html", bl)
print("ALL PAGES done")
