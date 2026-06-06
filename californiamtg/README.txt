California Mortgage Concierge — scenario builder & intake portal (californiamtg.com)
===================================================================================

Powered by West Coast Capital Mortgage Inc. (NMLS #2817729 · CA DRE #01385024).

A standalone, no-build static site — a premium California mortgage concierge
intake experience. It collects useful mortgage scenario detail through a
branching, multi-step Scenario Builder, then routes the user to WCCI.online AI
review, a licensed mortgage professional, or a secure pre-approval. Separate
brand chrome from the West Coast / Suncoast corporate sites; deploy as its own
Netlify site.

Files
-----
  index.html           Homepage: hero + Scenario Builder + Rates + Why Start Here + footer
  scenario-builder.js  Branching multi-step questionnaire engine, lead logic, routing
  styles.css           Premium dark-navy / white / gold design system + builder UI
  script.js            Sticky-header scroll state, mobile nav, hero video, builder quick-starts
  assets/              favicon.svg, equal-housing.svg
  public/videos/       Place hero video here (see public/videos/README.txt)
  public/images/       Place hero poster JPG here (see public/images/README.txt)
  _redirects           Netlify SPA-style fallback to index.html
  robots.txt, sitemap.xml

Scenario Builder & lead capture
-------------------------------
  Flow:  Goal (Step 1)  ->  scenario-specific questions  ->  general questions
         ->  contact  ->  thank-you with smart next-step routing.

  Branches: Buying, Refinancing, Cash-out, Lowering payment, Understanding
  rates, Investment/DSCR, Self-employed, Realtor scenario, Denied by bank,
  Not sure. Quick-start entry points (Investors, Self-Employed, "Check My
  Scenario") preselect the branch.

  On submit, scenario-builder.js assembles a structured `lead` object
  (lead categories, user type, scenario, timeline, state, estimated value,
  contact, full answers summary, preferred next step, UTM/source) and calls
  submit().  *** Integration point: in scenario-builder.js, search for
  "TODO: connect lead submission endpoint here." *** to wire up a CRM, email
  notification, Zapier/Make webhook, Google Sheet, mortgage LOS, or the
  WCCI.online AI payload. Until then the lead is logged to the console and
  saved to localStorage (cm_last_lead) so nothing is lost.

Run locally
-----------
  cd californiamtg
  python3 -m http.server 8000
  # open http://localhost:8000

Build
-----
  None. It is plain static HTML/CSS/JS — deploy the folder as-is.

Netlify (Git deploy)
--------------------
  Create a new Netlify site for this brand.
  Build command: (none)
  Publish directory: californiamtg

Link targets (placeholders — update when real routes exist)
-----------------------------------------------------------
  Explore Loan Options : /loan-options
  Start AI Scenario    : https://wcci.online
  Talk to a Broker     : /contact
  Get Pre-Approved     : /apply
  Main Website         : https://westccmortgage.com

Hero video
----------
  Add files to public/videos/ and public/images/ then uncomment the <source>
  tags in the hero <video>. See public/videos/README.txt and
  public/images/README.txt. Until then a premium dark-navy gradient with soft
  gold ambient lighting (and gentle motion) is shown as the fallback.

Compliance
----------
  No rate quotes, no "instant/guaranteed approval" claims. AI disclaimer
  appears under the AI section and in the footer. Loan options are stated as
  "subject to review and approval."
