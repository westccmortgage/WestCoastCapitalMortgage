California Mortgage — premium landing site (californiamtg.com)
=============================================================

Powered by West Coast Capital Mortgage Inc. (NMLS #2817729 · CA DRE #01385024).

A standalone, no-build static landing page — separate brand chrome from the
West Coast / Suncoast corporate sites. Deploy as its own Netlify site.

Files
-----
  index.html        Full homepage (hero + 6 sections + footer, SEO + JSON-LD)
  styles.css        Premium dark-navy / white / gold design system
  script.js         Sticky-header scroll state, mobile nav, hero video init
  assets/           favicon.svg, equal-housing.svg, hero poster (SVG fallback)
  videos/           Place hero video here (see videos/README.txt)
  images/           Place hero poster JPG here (see images/README.txt)
  _redirects        Netlify SPA-style fallback to index.html
  robots.txt, sitemap.xml

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
  Add files to videos/ and images/ then uncomment the <source> tags in the
  hero <video>. See videos/README.txt and images/README.txt.

Compliance
----------
  No rate quotes, no "instant/guaranteed approval" claims. AI disclaimer
  appears under the AI section and in the footer. Loan options are stated as
  "subject to review and approval."
