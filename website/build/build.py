#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from chrome import (head, header, footer, chat, page_hero, cta_band,
                    PHONE, PHONE_TEL, NMLS, COMPANY, PROGRAMS)

OUT = "/sessions/keen-eloquent-planck/mnt/outputs/site"

def write(name, html):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", name)

# ---------------- HOME ----------------
RATES = [("30-Year Fixed","6.49%","6.61%"),("15-Year Fixed","5.74%","5.92%"),
         ("FHA 30-Year","6.13%","6.95%"),("VA 30-Year","6.05%","6.28%"),
         ("Jumbo 30-Year","6.55%","6.63%")]
rate_rows = "".join(
    f'<div class="rate-row"><span class="name">{n}</span><span><span class="val">{r}</span><span class="apr">{a} APR</span></span></div>'
    for n,r,a in RATES)

PROGRAM_CARDS = [
    ("conventional.html","🏠","Conventional","Flexible terms and competitive rates with as little as 3% down for qualified buyers."),
    ("fha.html","🔑","FHA Loans","Just 3.5% down and flexible credit — a favorite for first-time buyers."),
    ("va.html","🎖️","VA Loans","$0 down and no PMI for eligible veterans and active-duty service members."),
    ("usda.html","🌾","USDA Loans","$0 down financing for eligible rural and suburban homebuyers."),
    ("jumbo.html","💎","Jumbo Loans","Financing above conforming limits for higher-priced California homes."),
    ("refinance.html","🔁","Refinance","Lower your rate, shorten your term, or tap into your home's equity."),
]
program_cards = "".join(
    f'<a class="card fade" href="{u}"><div class="ico">{e}</div><h3>{t}</h3><p>{d}</p><span class="more">Explore {t} →</span></a>'
    for u,e,t,d in PROGRAM_CARDS)

REVIEWS = [
    ("Helpful service made the whole loan process a positive experience. The loan was amazing for my investment property — I will definitely come back again.","Google Reviewer","Investment Property, Los Angeles","★★★★★"),
    ("Anatoliy and his team made our first home purchase painless. They explained every step in plain English and got us a great rate.","Maria & Daniel R.","First-Time Buyers, FHA","★★★★★"),
    ("Refinanced and cut my monthly payment significantly. Honest advice and no surprises at closing.","James T.","Refinance, Conventional","★★★★★"),
]
review_cards = "".join(
    f'<div class="review fade"><div class="stars">{s}</div><p>"{q}"</p><div class="who"><div class="av">{n[0]}</div><div><b>{n}</b><span>{role}</span></div></div></div>'
    for q,n,role,s in REVIEWS)

home = head("Los Angeles Home Loans & Mortgage Refinancing",
    "West Coast Capital Mortgage — your trusted local lender for home loans and refinancing across CA, FL & WA. Apply online, get a free instant rate quote, or use our calculators.","home")
home += header("home")
home += f"""
<section class="hero">
  <div class="container">
    <div>
      <span class="pill">Licensed in CA · FL · WA · {NMLS}</span>
      <h1 style="margin-top:16px">Home loans done <span class="hl">the honest way.</span></h1>
      <p>Whether you're buying your first home, refinancing, or investing — we deliver clear answers, competitive rates, and a team that's with you every step. Backed by 20+ years of lending experience.</p>
      <div class="hero-cta">
        <a class="btn btn-gold btn-lg" href="apply.html">Get Pre-Approved</a>
        <a class="btn btn-ghost btn-lg" href="calculators.html">Estimate My Payment</a>
      </div>
      <div class="hero-badges">
        <div><b>20+ yrs</b><span>Lending experience</span></div>
        <div><b>$0 down</b><span>VA &amp; USDA options</span></div>
        <div><b>3 states</b><span>CA · FL · WA</span></div>
      </div>
    </div>
    <div class="rate-card">
      <h3>Today's Sample Rates <span class="live">● LIVE</span></h3>
      {rate_rows}
      <p class="rate-note">Illustrative rates as of today. Your actual rate depends on credit, down payment & loan type. <a href="contact.html" style="color:var(--gold)">Get your real quote →</a></p>
    </div>
  </div>
</section>

<div class="trust"><div class="container">
  <span><b>★ 5.0</b> Google Reviews</span><span class="dot"></span>
  <span><b>Equal Housing</b> Lender</span><span class="dot"></span>
  <span><b>{NMLS}</b></span><span class="dot"></span>
  <span><b>CA Broker</b> since 2009</span>
</div></div>

<section class="section" id="programs"><div class="container">
  <div class="sec-head fade">
    <span class="eyebrow">Loan Programs</span>
    <h2>Find the loan that fits your life</h2>
    <p class="lead">Every borrower is different. We match you with the right program — and explain exactly why it works for you.</p>
  </div>
  <div class="grid grid-3">{program_cards}</div>
  <div class="center" style="margin-top:34px"><a class="btn btn-outline" href="conventional.html">View all loan programs →</a></div>
</div></section>

<section class="section bg-mist"><div class="container">
  <div class="split">
    <div class="fade">
      <span class="eyebrow">Why West Coast Capital</span>
      <h2>Experience you can rely on</h2>
      <p class="lead">Founded by Anatoliy Kanevsky, a California-licensed broker since 2009 with a career in residential lending dating back to 2004. We've guided thousands of families through one of the most important financial decisions of their lives.</p>
      <ul class="feature-list">
        <li><div><b>Straight answers, no jargon.</b> We explain your options clearly so you can decide with confidence.</div></li>
        <li><div><b>Local market expertise.</b> Deep knowledge of California, Florida & Washington housing markets.</div></li>
        <li><div><b>Full-lifecycle insight.</b> Our team understands both financing and construction — a rare advantage.</div></li>
        <li><div><b>Fast, modern process.</b> Apply online in minutes and track everything in one place.</div></li>
      </ul>
      <div style="margin-top:24px"><a class="btn btn-dark" href="about.html">Meet our founder →</a></div>
    </div>
    <div class="media-frame fade">
      <div class="steps" style="grid-template-columns:1fr">
        <div class="step"><div class="n">1</div><h3>Apply in minutes</h3><p>Complete a quick, secure online application — no paperwork pile.</p></div>
        <div class="step"><div class="n">2</div><h3>Get matched & quoted</h3><p>We compare programs and bring you a personalized rate.</p></div>
        <div class="step"><div class="n">3</div><h3>Close with confidence</h3><p>We handle the details and keep you informed to the finish line.</p></div>
      </div>
    </div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="sec-head fade"><span class="eyebrow">Tools</span><h2>Crunch the numbers in seconds</h2>
  <p class="lead">Estimate payments, test a refinance, or see how much home you can afford — instantly.</p></div>
  <div class="grid grid-4">
    <a class="card fade" href="calculators.html#purchase"><div class="ico">🧮</div><h3>Payment</h3><p>Estimate your monthly principal, interest, taxes & insurance.</p><span class="more">Open →</span></a>
    <a class="card fade" href="calculators.html#refi"><div class="ico">🔁</div><h3>Refinance</h3><p>See your potential savings and break-even point.</p><span class="more">Open →</span></a>
    <a class="card fade" href="calculators.html#afford"><div class="ico">🏡</div><h3>Affordability</h3><p>Find a comfortable price range based on your income.</p><span class="more">Open →</span></a>
    <a class="card fade" href="calculators.html#rentbuy"><div class="ico">⚖️</div><h3>Rent vs Buy</h3><p>Compare the long-term cost of renting and owning.</p><span class="more">Open →</span></a>
  </div>
</div></section>

<section class="section bg-navy"><div class="container">
  <div class="sec-head fade"><span class="eyebrow" style="color:var(--gold)">Client Reviews</span><h2>Families who trusted us</h2></div>
  <div class="grid grid-3">{review_cards}</div>
  <div class="center" style="margin-top:34px"><a class="btn btn-gold" href="reviews.html">Read all reviews →</a></div>
</div></section>
"""
home += cta_band()
home += footer() + chat()
write("index.html", home)
print("HOME done")
