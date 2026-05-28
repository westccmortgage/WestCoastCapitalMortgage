#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from chrome import (head, header, footer, chat, page_hero, cta_band,
                    PHONE, PHONE_TEL, NMLS)
OUT = "/sessions/keen-eloquent-planck/mnt/outputs/site"
def write(name, html):
    open(os.path.join(OUT, name),"w",encoding="utf-8").write(html); print("wrote",name)

def field(lbl, id_, val, typ="text", opts=None):
    if opts:
        o="".join(f'<option value="{v}"{" selected" if v==val else ""}>{t}</option>' for v,t in opts)
        return f'<div class="field"><label>{lbl}</label><select id="{id_}">{o}</select></div>'
    return f'<div class="field"><label>{lbl}</label><input id="{id_}" type="{typ}" value="{val}"></div>'

# ---------------- CALCULATORS ----------------
c = head("Mortgage Calculators","Estimate your monthly mortgage payment, refinance savings, home affordability, and compare renting vs buying with West Coast Capital Mortgage's free calculators.","calc")
c += header("calc")
c += page_hero("Calculators","Mortgage Calculators","Estimate payments, test a refinance, check affordability, and weigh renting against buying — all updated live as you type.")
c += f"""
<section class="section"><div class="container">
  <div class="calc-tabs">
    <button class="calc-tab active" data-calc="purchase">🧮 Payment</button>
    <button class="calc-tab" data-calc="refi">🔁 Refinance</button>
    <button class="calc-tab" data-calc="afford">🏡 Affordability</button>
    <button class="calc-tab" data-calc="rentbuy">⚖️ Rent vs Buy</button>
  </div>

  <div id="panel-purchase" class="calc-panel">
    <div class="calc">
      <div>
        <h3>Purchase payment</h3>
        <div class="wiz-grid">
          {field("Home price ($)","p-price","750000")}
          {field("Down payment (%)","p-down","20")}
          {field("Interest rate (%)","p-rate","6.49")}
          {field("Loan term","p-term","30",opts=[("30","30 years"),("20","20 years"),("15","15 years"),("10","10 years")])}
          {field("Property tax (%/yr)","p-tax","1.1")}
          {field("Home insurance ($/yr)","p-ins","1800")}
          {field("HOA ($/mo)","p-hoa","0")}
        </div>
      </div>
      <div class="calc-result">
        <span class="sub">Estimated monthly payment</span>
        <span class="big" id="p-out-total">$0</span>
        <div class="breakdown">
          <div class="br"><span>Principal &amp; interest</span><b id="p-out-pi">$0</b></div>
          <div class="br"><span>Property tax</span><b id="p-out-tax">$0</b></div>
          <div class="br"><span>Insurance + PMI</span><b id="p-out-ins">$0</b></div>
          <div class="br"><span>Loan amount</span><b id="p-out-loan">$0</b></div>
          <div class="br"><span>Down payment</span><b id="p-out-down">$0</b></div>
        </div>
        <a class="btn btn-gold" style="margin-top:18px" href="apply.html">Get my real rate →</a>
      </div>
    </div>
  </div>

  <div id="panel-refi" class="calc-panel hide">
    <div class="calc">
      <div>
        <h3>Refinance savings</h3>
        <div class="wiz-grid">
          {field("Current balance ($)","r-balance","500000")}
          {field("Current rate (%)","r-oldrate","7.25")}
          {field("New rate (%)","r-newrate","6.25")}
          {field("New term","r-term","30",opts=[("30","30 years"),("20","20 years"),("15","15 years")])}
          {field("Closing costs ($)","r-costs","6000")}
        </div>
      </div>
      <div class="calc-result">
        <span class="sub">New monthly payment</span>
        <span class="big" id="r-out-new">$0</span>
        <div class="breakdown">
          <div class="br"><span>Monthly savings</span><b id="r-out-save">$0</b></div>
          <div class="br"><span>Annual savings</span><b id="r-out-year">$0</b></div>
          <div class="br"><span>Break-even</span><b id="r-out-break">—</b></div>
        </div>
        <a class="btn btn-gold" style="margin-top:18px" href="refinance.html">Start refinancing →</a>
      </div>
    </div>
  </div>

  <div id="panel-afford" class="calc-panel hide">
    <div class="calc">
      <div>
        <h3>How much can I afford?</h3>
        <div class="wiz-grid">
          {field("Gross annual income ($)","a-income","140000")}
          {field("Monthly debts ($)","a-debts","700")}
          {field("Down payment ($)","a-down","100000")}
          {field("Interest rate (%)","a-rate","6.49")}
          {field("Loan term","a-term","30",opts=[("30","30 years"),("15","15 years")])}
        </div>
      </div>
      <div class="calc-result">
        <span class="sub">Estimated home price you can afford</span>
        <span class="big" id="a-out-price">$0</span>
        <div class="breakdown">
          <div class="br"><span>Max monthly payment</span><b id="a-out-pmt">$0</b></div>
          <div class="br"><span>Estimated loan amount</span><b id="a-out-loan">$0</b></div>
          <div class="br"><span>Based on 43% DTI</span><b>guideline</b></div>
        </div>
        <a class="btn btn-gold" style="margin-top:18px" href="apply.html">Get pre-approved →</a>
      </div>
    </div>
  </div>

  <div id="panel-rentbuy" class="calc-panel hide">
    <div class="calc">
      <div>
        <h3>Rent vs Buy</h3>
        <div class="wiz-grid">
          {field("Current monthly rent ($)","v-rent","3500")}
          {field("Home price ($)","v-price","750000")}
          {field("Down payment (%)","v-down","20")}
          {field("Interest rate (%)","v-rate","6.49")}
          {field("Years staying","v-years","7")}
          {field("Annual appreciation (%)","v-appr","4")}
        </div>
      </div>
      <div class="calc-result">
        <span class="sub">Verdict over your time horizon</span>
        <span class="big" id="v-out-verdict">—</span>
        <div class="breakdown">
          <div class="br"><span>Total cost of renting</span><b id="v-out-rent">$0</b></div>
          <div class="br"><span>Net cost of owning</span><b id="v-out-own">$0</b></div>
          <div class="br"><span>Est. home equity built</span><b id="v-out-equity">$0</b></div>
        </div>
        <a class="btn btn-gold" style="margin-top:18px" href="apply.html">Talk to an advisor →</a>
      </div>
    </div>
  </div>

  <p class="muted center" style="margin-top:24px;font-size:.85rem">Estimates only and not an offer to lend. Actual figures depend on your full financial profile. Contact us at <a href="tel:{PHONE_TEL}">{PHONE}</a> for a precise quote.</p>
</div></section>
"""
c += cta_band() + footer() + chat()
write("calculators.html", c)

# ---------------- APPLY ----------------
def choice(group, emoji, label):
    return f'<div class="choice" data-group="{group}"><div class="e">{emoji}</div><div>{label}</div></div>'

a = head("Apply Now — Online Mortgage Application","Start your secure online mortgage application with West Coast Capital Mortgage. Get pre-approved in minutes for purchase or refinance loans in CA, FL & WA.","apply")
a += header("apply")
a += page_hero("Apply Now","Apply Online in Minutes","A quick, secure application to get you pre-approved. No obligation — and a licensed loan officer reviews every submission personally.")
a += f"""
<section class="section"><div class="container">
  <form id="wizard" class="wizard" name="application" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="application">
    <p class="hide"><label>Don't fill this out: <input name="bot-field"></label></p>
    <div class="wiz-bar">
      <div class="wb active"><span class="num">1</span><br>Goal</div>
      <div class="wb"><span class="num">2</span><br>Property</div>
      <div class="wb"><span class="num">3</span><br>About you</div>
      <div class="wb"><span class="num">4</span><br>Contact</div>
      <div class="wb"><span class="num">✓</span><br>Done</div>
    </div>

    <div class="wiz-step active">
      <h3>What would you like to do?</h3>
      <div class="choice-grid" style="margin-top:16px">
        {choice("goal","🏠","Buy a home")}
        {choice("goal","🔁","Refinance")}
        {choice("goal","💵","Cash-out refinance")}
        {choice("goal","🏗️","Renovation / 203(k)")}
      </div>
      <div class="field" style="margin-top:20px"><label>Which loan type interests you?</label>
        <select name="loan_type"><option>Not sure yet</option><option>Conventional</option><option>FHA</option><option>VA</option><option>USDA</option><option>Jumbo</option><option>Reverse</option></select>
      </div>
    </div>

    <div class="wiz-step">
      <h3>Tell us about the property</h3>
      <div class="wiz-grid" style="margin-top:16px">
        <div class="field"><label>Property state</label><select name="state"><option>California</option><option>Florida</option><option>Washington</option></select></div>
        <div class="field"><label>Property type</label><select name="property_type"><option>Single-family</option><option>Condo</option><option>Townhome</option><option>Multi-unit</option><option>Investment</option></select></div>
        <div class="field"><label>Estimated price / value ($)</label><input name="price" type="text" placeholder="750,000"></div>
        <div class="field"><label>Down payment / equity ($)</label><input name="down" type="text" placeholder="150,000"></div>
      </div>
    </div>

    <div class="wiz-step">
      <h3>A little about you</h3>
      <div class="wiz-grid" style="margin-top:16px">
        <div class="field"><label>Credit profile</label><select name="credit"><option>Excellent (740+)</option><option>Good (680–739)</option><option>Fair (620–679)</option><option>Below 620</option><option>Not sure</option></select></div>
        <div class="field"><label>Annual household income ($)</label><input name="income" type="text" placeholder="140,000"></div>
        <div class="field"><label>Employment</label><select name="employment"><option>W-2 employee</option><option>Self-employed</option><option>Retired</option><option>Other</option></select></div>
        <div class="field"><label>First-time buyer?</label><select name="firsttime"><option>Yes</option><option>No</option></select></div>
      </div>
    </div>

    <div class="wiz-step">
      <h3>Where can we reach you?</h3>
      <div class="wiz-grid" style="margin-top:16px">
        <div class="field"><label>Full name</label><input name="name" type="text" required placeholder="Jane Doe"></div>
        <div class="field"><label>Phone</label><input name="phone" type="tel" required placeholder="(310) 555-1234"></div>
        <div class="field"><label>Email</label><input name="email" type="email" required placeholder="you@email.com"></div>
        <div class="field"><label>Best time to call</label><select name="besttime"><option>Anytime</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div>
      </div>
      <div class="field"><label>Anything else we should know? (optional)</label><textarea name="notes" rows="3" style="width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;font-family:inherit"></textarea></div>
      <p class="muted" style="font-size:.8rem">By submitting, you certify the information is complete and correct for the purpose of obtaining mortgage services. We respect your privacy and never sell your data.</p>
    </div>

    <div class="wiz-step">
      <div class="success-box">
        <div class="check">✓</div>
        <h3>Application received!</h3>
        <p class="muted">Thank you. A licensed loan officer from West Coast Capital Mortgage will review your information and reach out shortly. Need to talk now? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
        <a class="btn btn-gold" href="index.html">Back to home</a>
      </div>
    </div>

    <div class="wiz-nav">
      <button type="button" class="btn btn-outline" id="wiz-back">← Back</button>
      <button type="button" class="btn btn-gold" id="wiz-next">Continue</button>
    </div>
  </form>
  <p class="center muted" style="margin-top:20px;font-size:.85rem">🔒 Your information is encrypted and secure. {NMLS} · Equal Housing Lender.</p>
</div></section>
"""
a += footer() + chat()
write("apply.html", a)

# ---------------- CONTACT ----------------
ct = head("Contact Us","Contact West Coast Capital Mortgage — call (310) 654-1577 or request a free, no-obligation rate quote online. Serving CA, FL & WA.","contact")
ct += header("contact")
ct += page_hero("Contact","Let's talk about your home loan","Questions about rates, programs, or your application? Reach out and a licensed loan officer will get back to you fast.")
ct += f"""
<section class="section"><div class="container">
  <div class="split">
    <div>
      <h2>Request a free rate quote</h2>
      <p class="muted">Fill this out and we'll follow up — usually the same day.</p>
      <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mailto style="margin-top:18px">
        <input type="hidden" name="form-name" value="contact">
        <p class="hide"><label>Don't fill this out: <input name="bot-field"></label></p>
        <div class="wiz-grid">
          <div class="field"><label>Full name</label><input name="name" type="text" required></div>
          <div class="field"><label>Phone</label><input name="phone" type="tel" required></div>
        </div>
        <div class="field"><label>Email</label><input name="email" type="email" required></div>
        <div class="field"><label>I'm interested in</label><select name="interest"><option>A purchase loan</option><option>Refinancing</option><option>A rate quote</option><option>General question</option></select></div>
        <div class="field"><label>Message</label><textarea name="message" rows="4" style="width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;font-family:inherit"></textarea></div>
        <button class="btn btn-gold btn-lg" type="submit">Send message</button>
        <div class="form-ok hide callout" style="margin-top:16px"><b>Thanks!</b> Your message has been sent. We'll be in touch shortly — or call {PHONE} for immediate help.</div>
      </form>
    </div>
    <div>
      <div class="media-frame">
        <h3 style="color:#fff">Get in touch</h3>
        <p style="color:#c2cedd">We're here to make your home financing simple and clear.</p>
        <p style="margin-top:20px;font-size:1.1rem"><b style="color:var(--gold)">📞 Phone</b><br><a href="tel:{PHONE_TEL}" style="color:#fff;font-size:1.4rem;font-weight:700">{PHONE}</a></p>
        <p style="margin-top:16px"><b style="color:var(--gold)">🏢 Office</b><br>Los Angeles, California</p>
        <p style="margin-top:16px"><b style="color:var(--gold)">🌎 Licensed in</b><br>California · Florida · Washington</p>
        <p style="margin-top:16px"><b style="color:var(--gold)">📋 Licensing</b><br>{NMLS} · CA Broker since 2009</p>
        <a class="btn btn-gold" style="margin-top:20px" href="apply.html">Start an application →</a>
      </div>
    </div>
  </div>
</div></section>
"""
ct += footer() + chat()
write("contact.html", ct)
print("BUILD2 done")
