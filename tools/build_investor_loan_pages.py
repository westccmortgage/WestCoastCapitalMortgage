#!/usr/bin/env python3
"""Generate the WCCM real-estate-investor loan section.

Writes six pages into wccm-corporate/:
  investor-loans.html (hub), fix-and-flip-loans.html, ground-up-construction-loans.html,
  bridge-loans.html, rental-portfolio-loans.html, multifamily-bridge-loans.html

This file is the content source of truth for those pages: edit the text and
numbers here and re-run `python tools/build_investor_loan_pages.py`.

Every program figure comes from the capital partner's current product manuals
(November 2026; summary in "D:/wcc Mortgage/ROC/Программы Roc — хайлайты и условия.md").
Do not add rates, speed or approval promises that are not in those documents.
Voice: private lending for investors. Loans close with WCCM (white-label platform,
our private lender). Never write "direct lender", "our own money" or "in-house
underwriting/funding": the capital and underwriting belong to the capital partner.

Shared site chrome (top bar, header, footer) is copied from loans.html, the
Investors nav link is added the same way tools/install_investor_links.py adds it
everywhere else, and production tracking plus the hidden Netlify form schemas
are installed with the same tools the build uses.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import install_investor_links as links  # noqa: E402
import install_wccm_ads_readiness as readiness  # noqa: E402
import install_wccm_gtm as gtm  # noqa: E402

PUBLISH = TOOLS.parent / "wccm-corporate"
SITE = "https://westcoastcapitalmortgage.com"
ORG_ID = f"{SITE}/#organization"
PERSON_ID = f"{SITE}/loan-officer#anatoliy-kanevsky"
UPDATED_ISO = "2026-11-05"
MODIFIED_ISO = "2026-11-06"
UPDATED_TEXT = "November 5, 2026"
UPDATED_SHORT = "Nov 5, 2026"
PHONE_HREF = "tel:+13106541577"
PHONE_TEXT = "310-654-1577"
# Anatoliy's direct line is already published on /loan-officer.
DIRECT_HREF = "tel:+13106865053"
DIRECT_TEXT = "310-686-5053"
PHOTO = "assets/anatoliy-kanevsky-portrait.webp"
AVATAR = "assets/anatoliy-kanevsky-avatar.webp"
FORM_ID = "investor-review"
# White-label borrower portal (Roc Capital platform), live since 2026-11-09.
PORTAL_APPLY = "https://portal.westcoastcapitalmortgage.com/apply-for-a-loan"
PORTAL_LOGIN = "https://portal.westcoastcapitalmortgage.com/login"
STATES = ["California", "Florida", "Texas"]

# ---------------------------------------------------------------------------
# Small HTML helpers
# ---------------------------------------------------------------------------

def plain(fragment: str) -> str:
    """HTML fragment -> plain text for JSON-LD (FAQ answers must match visible text)."""
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def table(head: list[str], rows: list[list[str]], caption: str = "", first_col_header: bool = True, ledger: bool = False) -> str:
    cap = f'<caption class="inv-caption">{caption}</caption>' if caption else ""
    ths = "".join(f'<th scope="col">{h}</th>' for h in head)
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            if i == 0 and first_col_header:
                cells.append(f'<th scope="row">{cell}</th>')
            else:
                cells.append(f"<td>{cell}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    cls = "inv-table wide" if len(head) >= 4 else "inv-table"
    wrap_cls = "inv-table-wrap inv-ledger" if ledger else "inv-table-wrap"
    return (f'<div class="{wrap_cls}" role="region" aria-label="{plain(caption) or plain(head[0])}" tabindex="0">'
            f'<table class="{cls}">{cap}<thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def term_sheet(title: str, rows: list[tuple[str, str]], note: str) -> str:
    """Program maximums laid out like the term sheet a borrower actually receives."""
    items = "".join(f'<div class="ts-row"><dt>{label}</dt><dd>{value}</dd></div>' for label, value in rows)
    return f"""<section class="inv-terms-sec"><div class="wrap">
  <div class="inv-terms">
    <div class="inv-terms-head"><h2>{title}</h2></div>
    <dl class="inv-terms-list">{items}</dl>
  </div>
</div></section>"""


def answer(h2: str, body: str, bg: bool = False, extra: str = "", anchor: str = "") -> str:
    cls = ' class="bg-light"' if bg else ""
    sid = f' id="{anchor}"' if anchor else ""
    return f"""<section{cls}{sid}><div class="wrap inv-answer">
  <h2>{h2}</h2>
  {body}{extra}
</div></section>"""


def feature_list(items: list[str], cls: str = "feature-list") -> str:
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def split_lists(left_title: str, left: list[str], right_title: str, right: list[str], h2: str) -> str:
    """Only the checklist side is shown: what the borrower needs to bring."""
    return f"""<section><div class="wrap">
  <div class="inv-checklist-box inv-checklist-solo"><h2 class="inv-h2">{right_title}</h2>{feature_list(right, "inv-checklist")}</div>
</div></section>"""


def faq_section(faqs: list[tuple[str, str]], title: str) -> str:
    items = "".join(f'<details class="acc"><summary>{q}</summary><div class="acc-body">{a}</div></details>' for q, a in faqs)
    return f"""<section class="bg-light" id="faq"><div class="wrap inv-faq">
  <h2 class="inv-h2">{title}</h2>
  {items}
</div></section>"""


def face(size: str = "") -> str:
    """Anatoliy's head-and-shoulders photo, so visitors see who they will talk to."""
    cls = f"inv-face {size}".strip()
    return f'<img class="{cls}" src="{AVATAR}" alt="Anatoliy Kanevsky" width="360" height="360" decoding="async">'


def cta_band(h2: str, p: str) -> str:
    return f"""<section><div class="wrap"><div class="cta-band inv-cta">
  <h2>{h2}</h2><p>{p}</p>
  <div class="btn-row"><a class="btn btn-lg btn-blue" href="#{FORM_ID}">Tell Me Your Scenario</a><a class="btn btn-lg btn-outline-light" href="{PHONE_HREF}">Call {PHONE_TEXT}</a></div>
  <p class="inv-cta-who">{face("sm")}<span>Anatoliy Kanevsky reviews investor deals himself. Direct line <a href="{DIRECT_HREF}">{DIRECT_TEXT}</a></span></p>
</div></div></section>"""


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------

SOFT_PULL_TEXT = ("Credit is checked with a soft pull that doesn&rsquo;t touch your score. Then we order the appraisal "
                  "and line up title, insurance and your entity documents.")


def how_it_works(close_text: str, close_title: str = "Close in your LLC", terms_text: str = SOFT_PULL_TEXT) -> str:
    steps = [
        ("We look at the numbers",
         "Address, price, budget, what it will sell or rent for, and your track record. By form or by phone. No application and no credit check yet."),
        ("You get a straight answer",
         "Which program fits and roughly how much leverage to expect, before you pay for an appraisal. If the deal doesn&rsquo;t work, we say so."),
        ("Written terms", terms_text),
        (close_title, close_text),
    ]
    lis = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in steps)
    return f"""<section class="bg-light"><div class="wrap">
  <div class="inv-two">
    <div><h2 class="inv-h2">What happens after you send a deal</h2><p class="lead">Same person from the first call to the payoff.</p></div>
    <ol class="steps">{lis}</ol>
  </div>
</div></section>"""


# The note is written in Anatoliy's voice from facts in his public bio (about.html):
# mortgage and real estate professional, CA real estate broker, residential
# development background. Have him approve the wording before it goes live.
NOTE_FULL = (
    "<p>I work in mortgage lending and real estate, and I&rsquo;ve been on the developer&rsquo;s side of a project too. "
    "So when you send me a deal, I read it the way you do: what you&rsquo;re paying, what the work will really cost, "
    "what it sells or rents for when it&rsquo;s done, and how much cash you need to get there.</p>"
    "<p>If the numbers work, I&rsquo;ll tell you which program fits and about how much leverage to expect before you spend money on an appraisal. "
    "If they don&rsquo;t, I&rsquo;ll tell you that too. When it&rsquo;s time to sell or rent it out, our sister brokerage "
    "<a href=\"https://westcoastcapitalrealty.com\">West Coast Capital Realty</a> can help, and once it&rsquo;s rented we can move you into a long-term "
    "<a href=\"dscr-loans.html\">DSCR loan</a>.</p>"
)


def numbers_band() -> str:
    """Real numbers only: program maximums, loan sizes, years in business, Google rating."""
    items = [("Up to 90%", "of the price, plus 100% of the rehab"),
             ("$50K&ndash;$5M", "loan sizes across our investor programs"),
             ("3 states", "California, Florida and Texas"),
             ("5.0 &#9733;", '<a href="reviews.html">rating on Google</a>')]
    cells = "".join(f'<div class="inv-num"><b>{v}</b><span>{l}</span></div>' for v, l in items)
    return f'<section class="inv-numbers" aria-label="By the numbers"><div class="wrap"><div class="inv-num-grid">{cells}</div></div></section>'


def trust_strip(items: list[str]) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<section class="inv-strip" aria-label="At a glance"><div class="wrap"><ul>{lis}</ul></div></section>'


STRIP_DEFAULT = ["Soft credit pull for terms", "No personal income verification",
                 "Up to 100% of rehab financed", "Closes in your LLC"]


def anatoliy_note(text: str, title: str = "A note before you send a deal") -> str:
    return f"""<section class="inv-person-sec"><div class="wrap">
  <div class="inv-person">
    <img class="inv-person-photo" src="{PHOTO}" alt="Anatoliy Kanevsky, founder of West Coast Capital Mortgage" width="720" height="810" loading="lazy" decoding="async">
    <div class="inv-person-note">
      <h2 class="inv-h2">{title}</h2>
      {text}
      <div class="inv-sign">
        <span class="inv-sign-name" aria-hidden="true">Anatoliy Kanevsky</span>
        <span class="inv-sign-meta"><a href="/loan-officer">Anatoliy Kanevsky</a>, founder &middot; NMLS #2775380 &middot; CA DRE #01385024</span>
        <span class="inv-sign-meta">Direct line <a href="{DIRECT_HREF}">{DIRECT_TEXT}</a> &middot; Burbank office</span>
      </div>
    </div>
  </div>
</div></section>"""

DISCLOSURE = f"""<section class="inv-disclosure"><div class="wrap">
  <p><strong>Business-purpose loans only.</strong> The programs on this page finance non-owner-occupied investment property purchased or refinanced by an LLC or corporation. They are not available for personal, family or household purposes or for a home you live in. Owners typically sign a personal guarantee. Loans are made or arranged by West Coast Capital Mortgage (NMLS #2817729, CA DRE Corporation License #02440065) and funded by our private lender. Figures are program maximums under current program guidelines as of {UPDATED_TEXT}. Actual leverage, loan amount, rate, term and eligibility depend on experience, credit, liquidity, the property, the market and underwriting. Some markets receive lower leverage or are not eligible, and programs change without notice. Nothing on this page is an offer of credit, a rate quote or a commitment to lend.</p>
</div></section>"""

PROGRAMS = {
    "investor-loans": ("All programs", "Investment Property Loans", "Compare every program side by side."),
    "fix-and-flip-loans": ("Fix &amp; Flip", "Fix and Flip Loans", "Up to 90% of purchase and 100% of rehab."),
    "ground-up-construction-loans": ("New construction", "Ground-Up Construction Loans", "Land plus 100% of the construction budget."),
    "bridge-loans": ("Bridge", "Investor Bridge Loans", "Finished properties listed for sale or leasing up."),
    "rental-portfolio-loans": ("Portfolio", "Rental Portfolio Loans", "Two to ten rentals in one 30-year loan."),
    "multifamily-bridge-loans": ("5+ units", "Multifamily Bridge Loans", "$2M&ndash;$5M value-add loans in California."),
    "dscr-loans": ("Long-term rental", "DSCR Loans", "Qualify a single rental on its rent."),
    "hard-money-loans": ("California", "Hard Money Loans in California", "Private money to buy, fix, build or bridge."),
    "hard-money-loans-los-angeles": ("Los Angeles", "Hard Money Loans in Los Angeles", "Los Angeles office, loans across LA County and the Valley."),
}


def related(current: str) -> str:
    links_html = []
    for slug, (_label, name, text) in PROGRAMS.items():
        if slug == current:
            continue
        links_html.append(f'<li><a href="{slug}.html">{name}</a><span>{text}</span></li>')
    return f"""<section class="inv-also"><div class="wrap">
  <h2 class="inv-h2">Not quite this deal?</h2>
  <ul class="inv-also-list">{"".join(links_html)}</ul>
</div></section>"""


DRAW_FAQ = ("How do I get the rehab or construction money?",
    "The budget is held back at closing and released in draws as the work is done: you request a draw online, an inspection confirms the progress and the funds go out.")
LLC_FAQ = ("Do I need an LLC or corporation?",
    "Yes, the loan closes in your LLC or corporation. No entity yet? Set one up before closing.")
SPEED_FAQ = ("How fast can you close?",
    "As fast as the appraisal and title allow. We order both right after the pre-screen.")
CREDIT_PULL_FAQ = ("Will checking my terms affect my credit score?",
    "No. It is a soft pull that does not affect your score.")
REFI_TO_RENTAL_FAQ = ("Can I keep the property as a rental when the work is done?",
    "Yes. Once it is rented, refinance into a 30-year <a href=\"dscr-loans.html\">DSCR</a> or <a href=\"rental-portfolio-loans.html\">portfolio loan</a>, qualified on the rent.")
MARKETS_FAQ = ("Which states do you lend in?",
    "California, Florida and Texas. Terms can vary by market, and we confirm what applies to your property on the first call.")


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_hub() -> dict:
    # Investors describe the situation, not the product name, so the chooser starts there.
    situations = [
        ("fix-and-flip-loans", "I&rsquo;m buying a house that needs work", "Fix and flip loan",
         "Up to 90% of the price + 100% of the rehab"),
        ("ground-up-construction-loans", "I&rsquo;m building on a lot or a teardown", "Ground-up construction loan",
         "75% of the land + 100% of construction"),
        ("bridge-loans", "The work is done. It&rsquo;s listed or leasing up", "Bridge loan",
         "Up to 70% of value, no prepayment penalty"),
        ("dscr-loans", "I&rsquo;m keeping one rental long term", "DSCR loan",
         "Qualify on the rent, not your W-2"),
        ("rental-portfolio-loans", "I want 2 to 10 rentals under one loan", "Rental portfolio loan",
         "Up to 80% LTV, one payment"),
        ("multifamily-bridge-loans", "I&rsquo;m buying a 5+ unit building in California", "Multifamily bridge loan",
         "$2M to $5M, 100% of the renovation"),
    ]
    rows = "".join(
        f'<li><a href="{slug}.html"><span class="pick-q">{q}</span>'
        f'<span class="pick-a"><b>{name}</b><small>{fig}</small></span><span class="pick-go" aria-hidden="true">&rarr;</span></a></li>'
        for slug, q, name, fig in situations)
    programs = f"""<section><div class="wrap">
  <h2 class="inv-h2">What are you working on?</h2>
  <p class="lead inv-lead">Pick the closest one. Each page has the full terms, a worked example and the paperwork you&rsquo;ll need.</p>
  <ul class="inv-pick">{rows}</ul>
</div></section>"""

    compare = table(
        ["Program", "Best for", "Maximum leverage", "Loan size", "Term", "Credit from", "Experience"],
        [
            ['<a href="fix-and-flip-loans.html">Fix &amp; flip</a>', "Buy, renovate, then sell or rent", "90% of purchase + 100% of rehab", "$50K&ndash;$3M", "12 months, interest only", "660 (680 for newer investors)", "Not required"],
            ['<a href="ground-up-construction-loans.html">Ground-up construction</a>', "New homes", "75% of land + 100% of construction", "$50K&ndash;$3M", "12 months (18&ndash;24 available)", "660 (680 for newer builders)", "Completed ground-up projects"],
            ['<a href="bridge-loans.html">Bridge</a>', "Finished property being sold or leased", "70% of value", "$50K&ndash;$3M", "12 months, interest only", "660 (680 for newer investors)", "Not required for renovated homes"],
            ['<a href="rental-portfolio-loans.html">Rental portfolio</a>', "2&ndash;10 leased rentals", "80% LTV purchase or rate-and-term, 75% cash-out", "Up to $2M", "30 years, fixed or ARM", "660 (700 for 80% LTV)", "Not required"],
            ['<a href="multifamily-bridge-loans.html">Multifamily bridge</a>', "5+ unit value-add in California", "75% of purchase + 100% of renovation", "$2M&ndash;$5M", "18&ndash;24 months + extensions", "725", "Multifamily in the same submarket"],
        ],
        caption="Investor loan programs compared",
    )
    compare_section = answer(
        "Investor loan programs compared",
        f"""<p>Use a fix and flip loan to buy and renovate, a ground-up construction loan to build, a bridge loan to hold a finished property while it sells or leases, and a DSCR or rental portfolio loan to keep rentals long term. The table shows each program&rsquo;s maximums.</p>{compare}
  <p class="inv-note">Single-rental DSCR terms are on the <a href="dscr-loans.html">DSCR page</a>.</p>""",
        bg=True, anchor="compare")

    cycle = f"""<section><div class="wrap">
  <h2 class="inv-h2">One deal, usually two loans</h2>
  <p class="lead inv-lead">A short-term loan to buy and fix or build, then a sale or a long-term loan to keep it. We can do both, and our sister brokerage can help on the buying and selling side.</p>
  <ol class="inv-cycle">
    <li><b>Buy</b><span>Bring your own deal or find one with <a href="https://westcoastcapitalrealty.com">West Coast Capital Realty</a>.</span></li>
    <li><b>Fix or build</b><span>Use a <a href="fix-and-flip-loans.html">fix and flip</a> or <a href="ground-up-construction-loans.html">ground-up</a> loan. The budget comes out in draws as the work gets done.</span></li>
    <li><b>Sell or lease</b><span>List it with our Realty team. If the sale takes longer than planned, a <a href="bridge-loans.html">bridge loan</a> on the finished property can buy time.</span></li>
    <li><b>Keep it</b><span>Once it&rsquo;s rented, refinance into a <a href="dscr-loans.html">DSCR</a> or <a href="rental-portfolio-loans.html">portfolio</a> loan.</span></li>
  </ol>
</div></section>"""

    faqs = [
        ("What investor loans do you offer?",
         "Fix and flip, ground-up construction, bridge, DSCR, rental portfolio and multifamily bridge loans for investors in California, Florida and Texas, closed in your LLC or corporation."),
        ("Are you a lender or a broker?",
         "Your loan closes with West Coast Capital Mortgage, funded by our private lender. We issue your term sheet and stay your contact from the first call to the payoff. NMLS #2817729 &middot; CA DRE #02440065."),
        ("How much can I borrow?",
         "Up to 90% of the price plus 100% of the rehab on a fix and flip, 75% of the land plus 100% of construction on a new build, up to 80% LTV on rentals, and $2M to $5M on apartment buildings."),
        ("Will you finance my first flip?",
         "Yes. First-time investors can get up to 90% of the price plus 100% of the rehab, depending on credit and the project."),
        ("Do you verify my personal income?",
         "No. Rental loans qualify on the rent, and short-term loans are sized on the property, your credit and your experience."),
        DRAW_FAQ,
        ("Is there a prepayment penalty?",
         "Not on fix and flip, construction or bridge loans. On rental loans you choose, including no penalty."),
        REFI_TO_RENTAL_FAQ,
        ("Are these hard money loans?",
         "They do the same job: short-term, interest-only loans based on the property and the deal. More on <a href=\"hard-money-loans.html\">hard money loans in California</a>."),
        CREDIT_PULL_FAQ,
        MARKETS_FAQ,
    ]
    what_you_get = f"""<section class="bg-light"><div class="wrap">
  <div class="inv-two">
    <div><h2 class="inv-h2">Your loan closes with us</h2><p class="lead">You deal with one company from the first call to the payoff, and the capital is there when the deal is.</p></div>
    <ul class="inv-checklist inv-get">
      <li><b>A term sheet in our name</b> before you pay for an appraisal, with the rate, leverage and costs in writing.</li>
      <li><b>Your own borrower portal</b> to apply, upload documents and request draws, extensions and payoffs online.</li>
      <li><b>One team to the payoff</b>, and on to your long-term rental loan when you keep the property.</li>
      <li><b>Our private lender behind every loan</b>, published guidelines and no prepayment penalty on fix and flip, construction and bridge loans.</li>
    </ul>
  </div>
</div></section>"""
    sections = [numbers_band(), programs, what_you_get, anatoliy_note(NOTE_FULL), compare_section, cycle,
                faq_section(faqs, "Questions investors ask us"),
                cta_band("Have a deal? Send it over.", "The address, the price and your budget are enough to start. You&rsquo;ll hear which program fits and how much leverage to expect before you spend money on an appraisal."),
                DISCLOSURE]
    return dict(
        slug="investor-loans",
        title="Investment Property Loans | West Coast Capital Mortgage",
        description="Investment property loans for investors and developers in CA, FL and TX: fix & flip, ground-up construction, bridge, rental portfolio and multifamily loans.",
        h1="Financing for Real Estate Investors &amp; Developers", crumb="Investment Property Loans", programs_line="Fix &amp; Flip &middot; Ground-Up Construction &middot; Bridge Loans",
        lead="Fix and flip, construction, bridge and rental loans in California, Florida and Texas. Your loan closes with West Coast Capital Mortgage: our term sheet, our team and our borrower portal, with our private lender behind every loan.",
        sections=sections, faqs=faqs, product=None,
        catalog=[(PROGRAMS[s][1], s) for s in PROGRAMS if s != "investor-loans"],
    )


def page_fix_flip() -> dict:
    terms = [
        ("Purchase price financed", "Up to 90%"),
        ("Rehab budget financed", "100%, released in draws"),
        ("Loan vs. after-repair value", "70&ndash;75% max"),
        ("Loan amount", "$50K &ndash; $3M"),
        ("Term", "12 months, interest only <small>18&ndash;24 months for additions and ADUs</small>"),
        ("Prepayment penalty", "None"),
        ("Credit score", "From 660 <small>680 for first-time investors</small>"),
        ("First flip", "Yes, with 680+ credit"),
    ]
    example = table(
        ["Example deal", "Amount"],
        [
            ["Purchase price", "$500,000"],
            ["Rehab budget", "$100,000"],
            ["After-repair value (ARV)", "$800,000"],
            ["90% of the purchase, funded at closing", "$450,000"],
            ["100% of the rehab, released in draws", "$100,000"],
            ["<strong>Total loan</strong>", "<strong>$550,000</strong>"],
            ["ARV check: 70% of $800,000", "$560,000 &mdash; the loan fits"],
            ["Your cash to close", "$50,000 + closing costs and one month of interest reserve"],
        ],
        caption="Fix and flip loan sizing example", ledger=True,
    )
    tiers = table(
        ["Projects in the last 3 years", "Credit from", "Light / moderate rehab", "Heavy rehab", "Additions, ADUs, expansion", "Rehab budget up to"],
        [
            ["None (first flip)", "680", "75%&ndash;90% of purchase", "&mdash;", "&mdash;", "$100,000"],
            ["1&ndash;2", "680", "80%&ndash;90% of purchase", "75%", "&mdash;", "2&times; your largest project, max $500K"],
            ["3&ndash;4", "660", "85%&ndash;90% of purchase", "80%&ndash;85%", "80%, no ADUs (680+ credit)", "2&times; your largest project, max $500K"],
            ["5&ndash;9", "660", "90%", "85%", "85% (680+ credit)", "2&times; your largest project, max $500K"],
            ["10+", "660", "90%", "90%", "85% (680+ credit)", "2&times; your largest project, max $500K"],
        ],
        caption="Fix and flip leverage by experience (initial loan as a share of the purchase price)",
    )
    faqs = [
        ("Can I get a loan for my first flip?",
         "Yes. First-time investors can get up to 90% of the price plus 100% of a light or moderate rehab, depending on credit. Licensed agents and contractors start with experience credit."),
        ("How much do I need to put down?",
         "Usually 10% to 25% of the price, plus closing costs. The rehab is financed at 100%."),
        ("What credit score do I need?",
         "From 660, or 680 for first-time investors."),
        ("Do I pay interest on the whole loan?",
         "No. On loans of $100,000 or more you pay interest only on the money drawn."),
        DRAW_FAQ,
        ("Is there a prepayment penalty?",
         "No. Pay it off whenever you sell or refinance."),
        ("Can I refinance a flip that is already underway?",
         "Yes, for experienced investors with a project that is at least half done."),
        ("Can I finance a wholesale deal?",
         "Yes, with an assignment fee of up to 20% of the price."),
        ("What properties can I flip with this loan?",
         "Single-family homes, townhomes and small multi-unit properties, from cosmetic updates to full gut renovations, plus additions and ADUs for experienced investors."),
        REFI_TO_RENTAL_FAQ,
        LLC_FAQ,
        MARKETS_FAQ,
    ]
    sections = [
        term_sheet("Fix and flip terms", terms,
                   "Program maximums for 1&ndash;4 unit residential investment property. Leverage depends on experience, credit, rehab scope and market. In Florida and Travis, Harris and Bexar counties, TX, these loans need three or more completed projects and 680+ credit and are capped at 65% of ARV. Not a commitment to lend."),
        answer("What is a fix and flip loan?",
               """<p>A fix and flip loan is a short-term, interest-only loan that finances the purchase and renovation of an investment property. Part of the purchase price is funded at closing, the renovation budget is held back and released in draws as work is completed, and the loan is repaid when the property is sold or refinanced, typically within 12 months.</p>"""),
        answer("How much can I borrow on a fix and flip?",
               f"""<p>Up to 90% of the purchase price plus 100% of the rehab budget, as long as the total loan stays within 70% of the after-repair value (75% for qualifying experienced investors). Here is the math on a typical deal:</p>{example}
  <p class="inv-note">Illustration only; your terms depend on experience, credit and the project.</p>""",
               bg=True, anchor="example"),
        answer("Fix and flip leverage by experience",
               f"""<p>The more projects you have completed in the last three years, the more of the purchase price is financed and the heavier the renovation can be.</p>{tiers}
  """,
               anchor="leverage"),
        split_lists("What we finance", [
            "Single-family homes, 2&ndash;4 unit properties and townhomes; condos outside Florida",
            "Cosmetic updates through full gut renovations; additions and expansions for experienced investors (ADUs from five completed projects)",
            "Purchases and delayed purchases; refinances, including mid-project, for investors with three or more completed projects",
            "Wholesale and assignment deals within program limits",
        ], "What you will need", [
            "An LLC or corporation as the borrower; owners sign a personal guarantee",
            "The purchase contract (and the full assignment chain if a wholesaler is involved)",
            "A scope of work and rehab budget, plus your track record of past projects",
            "Entity documents: articles, EIN letter, operating agreement and certificate of good standing",
            "Funds for the down payment, closing costs and at least one month of interest reserve",
        ], "What we finance and what you need"),
        how_it_works("The rehab budget is released through draws you request online as work is completed."),
        anatoliy_note("<p>Send me the address, what you&rsquo;re paying, the rehab budget and what it will sell for. I&rsquo;ll tell you how much of that the loan covers and how much cash you need to bring, before you pay for an appraisal.</p>",
                      "Send me the flip first"),
        faq_section(faqs, "Questions about fix and flip loans"),
        related("fix-and-flip-loans"),
        cta_band("Have a flip under contract?", "Send the address, purchase price, rehab budget and ARV. You&rsquo;ll hear how much leverage to expect before you pay for an appraisal."),
        DISCLOSURE,
    ]
    return dict(
        slug="fix-and-flip-loans",
        terms=terms,
        strip=["Up to 90% of the price + 100% of the rehab", "Interest only on funds drawn", "No prepayment penalty", "Soft credit pull for terms"],
        title="Fix & Flip Loans in CA, FL, TX | West Coast Capital Mortgage",
        description="Fix and flip loans up to 90% of purchase and 100% of rehab, $50K–$3M, 12-month interest-only with no prepayment penalty. First-time flippers considered.",
        h1="Fix and Flip Loans", crumb="Fix and Flip Loans",
        lead="Up to 90% of the purchase price and 100% of the rehab budget. Short-term, interest-only money to buy and renovate homes you plan to sell or rent.",
        sections=sections, faqs=faqs,
        product=dict(name="Fix and Flip Loan", loanType="Fix and flip (rehab) loan", min=50000, max=3000000, term=12, termUnit="MON",
                     collateral="Non-owner-occupied 1–4 unit residential investment property",
                     description="Short-term, interest-only loan for the purchase and renovation of 1–4 unit investment property: up to 90% of purchase and 100% of rehab, within 70–75% of after-repair value."),
    )


def page_ground_up() -> dict:
    terms = [
        ("Land or purchase price", "Up to 75% <small>with approved permits</small>"),
        ("Construction budget", "100%, released in draws"),
        ("Total project cost", "Up to 85% <small>90% with financed interest</small>"),
        ("Loan vs. completed value", "70% max"),
        ("Loan amount", "$50K &ndash; $3M"),
        ("Term", "12 months, interest only <small>18&ndash;24 months available</small>"),
        ("Credit score", "From 660 <small>680 for newer builders</small>"),
    ]
    example = table(
        ["Example build", "Amount"],
        [
            ["Land price (permits approved)", "$350,000"],
            ["Construction budget", "$450,000"],
            ["Total project cost", "$800,000"],
            ["Completed value (ARV)", "$1,200,000"],
            ["75% of the land + 100% of construction", "$262,500 + $450,000 = $712,500"],
            ["Total-cost cap: 85% of $800,000", "$680,000"],
            ["ARV cap: 70% of $1,200,000", "$840,000"],
            ["<strong>Maximum loan (the lowest of the three)</strong>", "<strong>$680,000</strong>"],
            ["Funded at closing for the land", "$230,000 (the cap trims the land advance)"],
            ["Released in draws for construction", "$450,000"],
            ["Your cash at closing", "$120,000 + closing costs and one month of interest reserve"],
        ],
        caption="Ground-up construction loan sizing example", ledger=True,
    )
    tiers = table(
        ["Completed ground-up projects", "Leverage", "Exit test", "Building in a new market"],
        [
            ["1&ndash;2", "75% of land / 100% of construction / 85% of cost", "Projected ROI of at least 20%", "Not available"],
            ["3&ndash;4", "Same", "Projected ROI of at least 10%", "With a GC contract and 5% less leverage"],
            ["5+", "Same", "Projected ROI of at least 10%", "With a GC contract and 5% less leverage"],
        ],
        caption="Ground-up construction requirements by experience",
    )
    faqs = [
        ("Can I get a construction loan before permits are approved?",
         "Yes. We fund 60% of the land now and bring it to 75% once permits are issued."),
        ("How much cash do I need to build?",
         "Usually from 15% of the total project cost, or 10% when interest is financed, plus closing costs."),
        ("Can I include interest in the loan?",
         "Yes, up to six months of interest can be built into the loan."),
        ("How long is the term?",
         "12 months, interest only, with 18 to 24 months available and extensions if the build runs long."),
        ("Do you finance lot splits and more than one home?",
         "Yes. A loan can cover two homes, including a lot split, and experienced builders can finance larger developments."),
        ("Can I refinance land I already own?",
         "Yes, in many cases, including land you bought before getting permits."),
        DRAW_FAQ,
        ("What can I build with a ground-up loan?",
         "New single-family homes, townhomes, small multi-unit buildings and condo projects on infill lots, including teardowns and lot splits."),
        REFI_TO_RENTAL_FAQ,
        LLC_FAQ,
        MARKETS_FAQ,
    ]
    sections = [
        term_sheet("Ground-up construction terms", terms,
                   "Program maximums for new 1&ndash;4 unit residential construction. Leverage is the same for every eligible builder, except in a new market (700+ credit, a GC agreement and 5% less of the land) and in Florida and Travis, Harris and Bexar counties, TX (700+ credit, 5% less of total cost, loan capped at 65% of completed value). Not a commitment to lend."),
        answer("What is a ground-up construction loan?",
               """<p>A ground-up construction loan is a short-term, interest-only loan that finances the land (or a teardown) and the full construction budget to build new homes. The land portion is funded at closing, construction money is released in draws as each stage is inspected, and the loan is repaid when the homes are sold or refinanced.</p>"""),
        answer("How much can I borrow to build?",
               f"""<p>Up to 75% of the land price plus 100% of the construction budget, limited to 85% of the total project cost (90% when interest is financed) and 70% of the completed value. The loan is the lowest of those three numbers:</p>{example}
  <p class="inv-note">Illustration only; your terms depend on experience and the project.</p>""",
               bg=True, anchor="example"),
        answer("Who qualifies for a ground-up construction loan?",
               f"""<p>Builders with completed ground-up projects. Leverage is the same at every experience level; experience changes the return the finished project must show and where you can build.</p>{tiers}
  """,
               anchor="leverage"),
        split_lists("What we finance", [
            "New single-family homes, 2&ndash;4 unit buildings and condo projects up to four units",
            "Teardowns and rebuilds on infill lots in cities and suburbs",
            "Lot splits, with a completed value for each home",
            "Purchases and delayed purchases, up to two properties per loan",
        ], "What you will need", [
            "Building plans, elevations and a site plan",
            "Approved permits, or an architect letter while permits are pending",
            "A line-item construction budget and the general contractor agreement",
            "A track record of completed ground-up projects",
            "Entity documents and funds for equity, closing costs and interest reserve",
        ], "What we finance and what you need"),
        how_it_works("Construction funds are released through draws as each stage is inspected."),
        anatoliy_note("<p>I come from luxury residential development, so I read a build the way a builder does: whether the budget matches the plans, how long permits and construction will really take, what the finished homes will sell for and how much cash you need until they do.</p>"
                      "<p>Send me the lot, where the permits stand, the budget and the completed value, and I&rsquo;ll size the loan before you pay for an appraisal.</p>",
                      "I&rsquo;ve been on the builder&rsquo;s side"),
        faq_section(faqs, "Questions about construction loans"),
        related("ground-up-construction-loans"),
        cta_band("Planning a build?", "Send the lot, the plans or permit status, the budget and the completed value. You&rsquo;ll get the loan sized before you pay for an appraisal."),
        DISCLOSURE,
    ]
    return dict(
        slug="ground-up-construction-loans",
        terms=terms,
        strip=["100% of construction financed", "Up to 6 months of interest built in", "Draws requested online", "Soft credit pull for terms"],
        title="Ground-Up Construction Loans | West Coast Capital Mortgage",
        description="Ground-up construction loans for new homes: up to 75% of land and 100% of construction, up to 85% of total cost, $50K–$3M, interest reserve financing.",
        h1="Ground-Up Construction Loans", crumb="Ground-Up Construction Loans",
        lead="Land plus 100% of the construction budget for builders putting up new homes, with up to six months of interest built into the loan.",
        sections=sections, faqs=faqs,
        product=dict(name="Ground-Up Construction Loan", loanType="Residential construction loan", min=50000, max=3000000, term=12, termUnit="MON",
                     collateral="Land and new 1–4 unit residential construction (non-owner-occupied)",
                     description="Short-term, interest-only loan for land and new 1–4 unit construction: up to 75% of land and 100% of construction, within 85% of total cost and 70% of completed value."),
    )


def page_bridge() -> dict:
    terms = [
        ("Loan vs. as-is value", "Up to 70%"),
        ("Loan vs. your cost", "Up to 90% <small>homes bought in the last 6 months</small>"),
        ("Loan amount", "$50K &ndash; $3M"),
        ("Term", "12 months, interest only <small>extension up to 6 months for a fee</small>"),
        ("Cash-flow test", "None on renovated homes"),
        ("Prepayment penalty", "None"),
        ("Credit score", "From 660 <small>680 for newer investors</small>"),
    ]
    options = table(
        ["", "Renovated", "Not fully updated"],
        [
            ["Typical use", "Finished flip or new build that is listed for sale or for rent", "Livable property with no deferred maintenance, leasing up before a long-term loan"],
            ["Cash-flow test", "None", "1.10 DSCR at exit"],
            ["Experience", "Not required (680+ credit)", "At least one completed project in the last 3 years"],
        ],
        caption="Two kinds of bridge loan, by property condition",
    )
    tiers = table(
        ["Projects in the last 3 years", "Credit from", "Renovated (C1&ndash;C2), owned 180 days or less", "C3&ndash;C4, owned 180 days or less", "Owned more than 180 days"],
        [
            ["None", "680", "80% of cost, within 70% of value", "Not eligible", "70% of value (C1&ndash;C2 only)"],
            ["1&ndash;2", "680", "80% of cost, within 70% of value", "75% of cost, within 70% of value, 1.10 DSCR", "70% of value; 1.10 DSCR in C3&ndash;C4"],
            ["3 or more", "660", "90% of cost, within 70% of value", "85% of cost, within 70% of value, 1.10 DSCR", "70% of value; 1.10 DSCR in C3&ndash;C4"],
        ],
        caption="Bridge loan leverage by experience and condition (loans up to $1M)",
    )
    faqs = [
        ("When does a bridge loan make sense?",
         "When a finished flip or new build is listed but not sold, a rehab loan is coming due, or a rental is leasing up before its long-term loan."),
        ("Can a bridge loan pay off my current hard money loan?",
         "Yes, when the project is finished."),
        ("How is the loan sized for a property that is listed for sale?",
         "On the lower of the list price and the appraised value, or on your cost if you bought it in the last six months."),
        ("Is a DSCR required?",
         "Not for renovated homes. Other properties need a 1.10 DSCR."),
        ("Do I need experience?",
         "Not for renovated homes."),
        ("What credit score do I need?",
         "From 660, or 680 for newer investors."),
        ("What happens after the bridge loan?",
         "Sell the property, or refinance into a long-term <a href=\"dscr-loans.html\">DSCR</a> or <a href=\"rental-portfolio-loans.html\">portfolio loan</a> once it is rented. There is no prepayment penalty."),
        LLC_FAQ,
        SPEED_FAQ,
        MARKETS_FAQ,
    ]
    sections = [
        term_sheet("Bridge loan terms", terms,
                   "Program maximums for finished 1&ndash;4 unit residential investment property. Leverage depends on experience, credit, condition, hold time and market. Not a commitment to lend."),
        answer("What is an investor bridge loan?",
               """<p>An investor bridge loan is a short-term, interest-only loan on a finished or nearly finished investment property that is listed for sale or being leased up but is not yet ready for long-term financing. It pays off a maturing rehab or construction loan, or buys a stabilized property quickly, and is repaid when the property sells or is refinanced.</p>""",
               extra=options),
        answer("How much can I borrow on a bridge loan?",
               f"""<p>Up to 70% of the appraised value. For a property you bought in the last six months, the loan is also sized on your total cost: up to 80% for newer investors and up to 90% for experienced investors on renovated homes.</p>
  """,
               bg=True, anchor="leverage"),
        split_lists("Good fits", [
            "A finished flip or new build that is listed but not sold yet",
            "A rehab or construction loan coming due before the property sells",
            "A finished property you want to buy and close quickly",
            "A rental leasing up before it qualifies for a long-term loan",
        ], "What you will need", [
            "An LLC or corporation as the borrower; owners sign a personal guarantee",
            "The listing or leases, plus the purchase settlement statement and renovation receipts",
            "Payoff statement for any existing loan",
            "Entity documents: articles, EIN letter, operating agreement and certificate of good standing",
        ], "When a bridge loan fits"),
        how_it_works("Payments, extensions and the payoff are handled online in the borrower portal."),
        anatoliy_note("<p>Send me the address, what you have into it, the list price or the rent, and the payoff on the current loan. I&rsquo;ll tell you what the property supports and what it takes to close.</p>",
                      "Send me the property first"),
        faq_section(faqs, "Questions about bridge loans"),
        related("bridge-loans"),
        cta_band("Need to bridge a finished property?", "Send the address, your cost, the list price or rent and the payoff. You&rsquo;ll hear how much the property supports and what it takes to close."),
        DISCLOSURE,
    ]
    return dict(
        slug="bridge-loans",
        terms=terms,
        strip=["Up to 70% of value", "No DSCR test on renovated homes", "No prepayment penalty", "Soft credit pull for terms"],
        title="Investor Bridge Loans | West Coast Capital Mortgage",
        description="Bridge loans for finished 1–4 unit investment properties listed for sale or leasing up: up to 70% of value, 12 months interest-only, no prepayment penalty.",
        h1="Investor Bridge Loans", crumb="Bridge Loans",
        lead="For a finished property that&rsquo;s listed for sale or leasing up. Pay off a rehab loan that&rsquo;s coming due, or buy a finished home quickly.",
        sections=sections, faqs=faqs,
        product=dict(name="Investor Bridge Loan", loanType="Short-term bridge loan", min=50000, max=3000000, term=12, termUnit="MON",
                     collateral="Finished non-owner-occupied 1–4 unit residential investment property",
                     description="Short-term, interest-only loan on finished 1–4 unit investment property listed for sale or leasing up: up to 70% of value and, on properties owned under six months, no more than 80% of cost (90% for experienced investors)."),
    )


def page_portfolio() -> dict:
    terms = [
        ("Properties", "2&ndash;10 in one blanket loan"),
        ("Loan amount", "Up to $2M total"),
        ("Purchase or rate-and-term", "Up to 80% LTV"),
        ("Cash-out refinance", "Up to 75% LTV"),
        ("DSCR minimum", "1.05 <small>gross rent divided by the monthly payment</small>"),
        ("Term", "30 years <small>fixed, ARM or interest-only</small>"),
        ("Income documents", "None <small>no tax returns, W-2s or pay stubs</small>"),
        ("Credit score", "From 660 <small>700+ for 80% LTV</small>"),
    ]
    ltv = table(
        ["Credit score", "Purchase", "Rate-and-term refinance", "Cash-out refinance"],
        [
            ["700 and above", "80%", "80%", "75%"],
            ["680&ndash;699", "75%", "75%", "70%"],
            ["660&ndash;679", "65%", "65%", "60%"],
        ],
        caption="Maximum loan-to-value by credit score",
    )
    dscr = table(
        ["Example portfolio of five rentals", "Monthly"],
        [
            ["Gross rent (lower of leases and the appraiser&rsquo;s market rent)", "$12,000"],
            ["Principal, interest, taxes, insurance and HOA (PITIA)", "$10,500"],
            ["<strong>DSCR = $12,000 &divide; $10,500</strong>", "<strong>1.14 &mdash; above the 1.05 minimum</strong>"],
        ],
        caption="How the debt-service coverage ratio is calculated", ledger=True,
    )
    faqs = [
        ("Can I mix property types in one portfolio loan?",
         "Yes. Single-family homes, 2&ndash;4 unit properties, townhomes, PUDs and condos can be combined in one loan."),
        ("Can I sell one property later?",
         "Yes. Pay 120% of the loan amount allocated to that property and it is released."),
        ("Is there a prepayment penalty?",
         "You choose: five, four, three or one year, or no penalty."),
        ("What credit score do I need?",
         "From 660, or 700 for 80% LTV."),
        ("Do the rentals need to be leased?",
         "Yes. At least 90% of the units should be leased, on 12- to 36-month leases."),
        ("How much cash do I need in reserve?",
         "Closing costs plus three months of payments for a purchase, or six months for a refinance."),
        ("When can I do a cash-out refinance?",
         "After 90 days of ownership."),
        ("Can foreign nationals get a portfolio loan?",
         "Yes, up to 65% LTV."),
        ("I only have one rental. Which loan fits?",
         "A single-property <a href=\"dscr-loans.html\">DSCR loan</a>. Portfolio loans start at two properties."),
        LLC_FAQ,
        MARKETS_FAQ,
    ]
    sections = [
        term_sheet("Rental portfolio loan terms", terms,
                   "Program maximums for leased 1&ndash;4 unit rentals held in an LLC or corporation. If a quarter or more of the properties are valued under $100,000, the maximum is 70% LTV. Not a commitment to lend."),
        answer("What is a rental portfolio loan?",
               """<p>A rental portfolio loan, also called a blanket loan, is one long-term loan secured by several rental properties at once, here two to ten. It replaces separate mortgages with one closing and one payment, and it qualifies on the properties&rsquo; rent rather than your personal income.</p>"""),
        answer("How is a portfolio loan qualified?",
               f"""<p>On the debt-service coverage ratio: the portfolio&rsquo;s monthly gross rent divided by its monthly principal, interest, taxes, insurance and HOA. The minimum is 1.05, and leverage depends on credit.</p>{dscr}{ltv}""",
               bg=True, anchor="leverage"),
        split_lists("Eligible properties", [
            "Single-family homes, 2&ndash;4 unit properties, townhomes and PUDs",
            "Warrantable condos",
            "Properties in C1&ndash;C4 condition with no deferred maintenance; single-family at least 700 square feet",
            "At least 90% of units leased",
        ], "What you will need", [
            "An LLC or corporation as the borrower; owners with 20% or more guarantee",
            "Current leases and a rent roll for every property",
            "Two consecutive statements showing closing costs and reserves",
            "Entity documents: articles, EIN letter, operating agreement and certificate of good standing",
        ], "What qualifies"),
        how_it_works("One payment for the whole portfolio, with escrow for taxes and insurance."),
        anatoliy_note("<p>Send me the addresses, the rents, rough values and what you owe on each one. I&rsquo;ll run the DSCR and tell you how much the portfolio supports.</p>",
                      "Send me the rent roll first"),
        faq_section(faqs, "Questions about portfolio loans"),
        related("rental-portfolio-loans"),
        cta_band("Ready to put your rentals under one loan?", "Send the addresses, rents, values and current payoffs. You&rsquo;ll hear the DSCR and how much the portfolio supports."),
        DISCLOSURE,
    ]
    return dict(
        slug="rental-portfolio-loans",
        terms=terms,
        strip=["Qualify on rent", "No tax returns or W-2s", "2 to 10 rentals, one payment", "30-year terms"],
        title="Rental Portfolio Loans | West Coast Capital Mortgage",
        description="One 30-year blanket loan for 2–10 rentals, qualified on rent with DSCR from 1.05: up to 80% LTV on purchases and rate-and-term, 75% cash-out.",
        h1="Rental Portfolio Loans", crumb="Rental Portfolio Loans",
        lead="Two to ten rentals under one 30-year loan. One closing, one payment, qualified on the rent instead of your personal income.",
        sections=sections, faqs=faqs,
        product=dict(name="Rental Portfolio (Blanket) Loan", loanType="DSCR blanket loan", min=100000, max=2000000, term=30, termUnit="ANN",
                     collateral="Two to ten leased 1–4 unit residential rental properties",
                     description="Long-term blanket loan for 2–10 rentals qualified on rent (DSCR from 1.05): up to 80% LTV on purchases and rate-and-term refinances, 75% on cash-out."),
    )


def page_multifamily() -> dict:
    terms = [
        ("Loan amount", "$2M &ndash; $5M <small>one property per loan</small>"),
        ("Purchase price", "Up to 75%"),
        ("Renovation budget", "100%, through a holdback"),
        ("Total project cost", "Up to 80%"),
        ("Term", "18&ndash;24 months, interest only <small>plus two 6-month extensions</small>"),
        ("As-stabilized value", "70% LTV max"),
        ("Once stabilized", "1.25x DSCR and a 9% debt yield"),
        ("Credit score", "725+"),
    ]
    metrics = table(
        ["Sizing test", "Limit"],
        [
            ["Loan-to-purchase price", "75%"],
            ["Loan-to-cost (initial)", "70%"],
            ["Loan-to-total cost (with renovation)", "80%"],
            ["As-is loan-to-value", "75%"],
            ["As-stabilized loan-to-value", "70%"],
            ["Stabilized debt-service coverage", "1.25x"],
            ["Debt yield", "9% or higher"],
        ],
        caption="Multifamily bridge loan sizing tests",
    )
    faqs = [
        ("What is the exit for a multifamily bridge loan?",
         "A refinance into long-term agency financing once the property is stabilized."),
        ("How many units do I need?",
         "Five or more, in a fully residential building."),
        ("What experience do I need?",
         "Experience owning and operating apartment buildings in the same market."),
        ("What are the borrower requirements?",
         "A single-purpose LLC or corporation, 725+ credit for each member and liquidity of 10% of the loan after closing."),
        ("What renovations can be financed?",
         "Light to moderate value-add work, up to about half of the purchase price."),
        ("How does prepayment work?",
         "You can pay off at any time; a minimum of 12 months of interest is due at payoff."),
        ("Where can I use a multifamily bridge loan?",
         "Apartment buildings in California&rsquo;s primary and secondary markets."),
        ("What due diligence is required?",
         "A commercial appraisal, environmental and property condition reports, a budget review and a site visit."),
    ]
    sections = [
        term_sheet("Multifamily bridge terms", terms,
                   "Program maximums for 5+ unit residential buildings in California. Not a commitment to lend."),
        answer("What is a multifamily bridge loan?",
               """<p>A multifamily bridge loan is a short-term, interest-only loan to buy and renovate an apartment building with five or more units, lease it up and then refinance into long-term agency financing. The purchase is funded at closing and the renovation budget is released from a holdback as the work is completed.</p>"""),
        answer("How is a multifamily bridge loan sized?",
               f"""<p>Up to 75% of the purchase price plus 100% of the renovation budget, within 80% of the total cost, as long as the stabilized property supports a 1.25x DSCR, a 9% debt yield and 70% of its as-stabilized value.</p>{metrics}""",
               bg=True, anchor="leverage"),
        split_lists("Eligible properties", [
            "100% residential buildings with five or more units",
            "As-is value of at least $100,000 per unit",
            "Light to moderate renovation; no structural work, additions or ground-up",
            "California primary and secondary markets; one property per loan; no wholesale deals",
        ], "Sponsor requirements", [
            "Multifamily ownership and management experience in the same submarket",
            "Single-purpose LLC or corporation (new, or existing with no other property), up to two members",
            "725+ credit for every member; no bankruptcy or foreclosure in seven years",
            "Liquidity of 10% of the loan after closing and net worth equal to the loan",
        ], "Property and sponsor requirements"),
        how_it_works("Renovation funds are released from the holdback as work is completed.", "Close in a single-purpose entity",
                     "A full credit report is pulled on every member of the entity. Then come the commercial appraisal, "
                     "third-party reports, a site visit and a sponsor interview."),
        anatoliy_note("<p>Send me the rent roll, the price, the renovation budget and your business plan. I&rsquo;ll check it against the sizing tests before you pay for third-party reports.</p>",
                      "Send me the deal first"),
        faq_section(faqs, "Questions about multifamily bridge loans"),
        related("multifamily-bridge-loans"),
        cta_band("Underwriting an apartment deal?", "Send the rent roll, purchase price, renovation budget and business plan. You&rsquo;ll hear how it sizes before you commit to third-party reports."),
        DISCLOSURE,
    ]
    return dict(
        slug="multifamily-bridge-loans",
        terms=terms,
        strip=["$2M to $5M", "100% of the renovation", "Built for an agency refinance", "California apartment buildings"],
        title="Multifamily Bridge Loans | West Coast Capital Mortgage",
        description="Value-add bridge loans for 5+ unit apartment buildings in California: $2M–$5M, up to 75% of purchase and 100% of renovation, 18–24 months plus extensions.",
        h1="Multifamily Bridge Loans", crumb="Multifamily Bridge Loans",
        lead="Buy, renovate and stabilize a 5+ unit apartment building in California, then refinance into long-term agency financing.",
        sections=sections, faqs=faqs, states=["California"],
        product=dict(name="Multifamily Bridge Loan", loanType="Multifamily bridge (value-add) loan", min=2000000, max=5000000, term=24, termUnit="MON",
                     collateral="100% residential apartment building with five or more units",
                     description="Short-term, interest-only value-add loan for 5+ unit apartment buildings in California: $2M–$5M, up to 75% of purchase and 100% of renovation, within 80% of total cost."),
    )


def page_hard_money() -> dict:
    terms = [
        ("Programs", "Fix and flip, bridge and ground-up construction <small>plus rental refinances</small>"),
        ("Purchase price financed", "Up to 90% <small>fix and flip</small>"),
        ("Rehab or construction budget", "100%, released in draws"),
        ("Loan vs. after-repair value", "70&ndash;75% max <small>fix and flip</small>"),
        ("Loan amount", "$50K &ndash; $3M"),
        ("Term", "12 months, interest only <small>no prepayment penalty</small>"),
        ("Credit score", "From 660 <small>680 for first-time investors</small>"),
        ("Where", "Statewide in California <small>also Florida and Texas</small>"),
        ("Borrower", "LLC or corporation"),
    ]
    programs = table(
        ["Hard money program", "Use it to", "Maximum leverage", "Loan size", "Term"],
        [
            ['<a href="fix-and-flip-loans.html">Fix and flip</a>', "Buy and renovate a home", "90% of purchase + 100% of rehab", "$50K&ndash;$3M", "12 months"],
            ['<a href="ground-up-construction-loans.html">Ground-up construction</a>', "Build on a lot or a teardown", "75% of land + 100% of construction", "$50K&ndash;$3M", "12 months (18&ndash;24 available)"],
            ['<a href="bridge-loans.html">Bridge</a>', "Hold a finished property while it sells or leases", "70% of value", "$50K&ndash;$3M", "12 months"],
            ['<a href="multifamily-bridge-loans.html">Multifamily bridge</a>', "Buy and renovate 5+ units", "75% of purchase + 100% of renovation", "$2M&ndash;$5M", "18&ndash;24 months"],
            ['<a href="rental-portfolio-loans.html">Rental refinance</a>', "Keep the property long term", "80% LTV", "Up to $2M", "30 years"],
        ],
        caption="Hard money and private money programs",
    )
    faqs = [
        ("Who offers hard money loans in Los Angeles?",
         "West Coast Capital Mortgage in Los Angeles offers hard money loans across Los Angeles County and the rest of California, plus Florida and Texas: fix and flip, bridge and construction loans."),
        ("Is private money the same as hard money?",
         "In practice, yes: short-term, interest-only loans based on the property and the deal."),
        ("How much can I borrow with a hard money loan?",
         "Up to 90% of the price plus 100% of the rehab on a flip, 75% of the land plus 100% of the build on new construction, and 70% of value on a bridge loan, from $50,000 to $3 million."),
        ("Can I get a hard money loan for my first flip in California?",
         "Yes. First-time investors can get up to 90% of the price plus 100% of a light or moderate rehab, depending on credit."),
        ("What credit score do I need for a hard money loan?",
         "From 660, or 680 for first-time investors."),
        ("Do you check my income for a hard money loan?",
         "No personal income verification. The loan is sized on the property, your credit and your experience."),
        ("Are you licensed in California?",
         "Yes: California DRE Corporation License #02440065 and NMLS #2817729."),
        ("What does a hard money loan cost?",
         "A rate and origination points set per deal, plus third-party costs. You see everything in a written term sheet before you pay for an appraisal."),
        SPEED_FAQ,
        DRAW_FAQ,
        LLC_FAQ,
        MARKETS_FAQ,
    ]
    sections = [
        term_sheet("Hard money loan terms", terms,
                   "Program maximums for 1&ndash;4 unit residential investment property. Leverage depends on experience, credit, the project and market. Not a commitment to lend."),
        answer("What is a hard money loan?",
               """<p>A hard money loan is a short-term, interest-only loan secured by investment real estate and sized mainly on the property and the deal rather than your personal income. Investors use it to buy and renovate, to build, or to hold a finished property until it sells or refinances. In California the terms hard money and private money are used for the same kind of loan.</p>
  <p>Our loans do that job with our private lender behind them: published guidelines, online draw requests and no prepayment penalty on fix and flip, construction and bridge loans.</p>"""),
        answer("Hard money programs we offer", programs, bg=True, anchor="programs"),
        answer("Where we lend in California",
               """<p>Statewide: Los Angeles County and the San Fernando Valley, Orange County, the Inland Empire, Ventura, San Diego, the Bay Area, Sacramento and the Central Valley. Infill homes and lots in cities and suburbs are the best fit.</p>
  <p>We also lend in Florida and Texas.</p>
  <p><a class="more" href="hard-money-loans-los-angeles.html">Hard Money Loans in Los Angeles</a></p>"""),
        how_it_works("The rehab or construction budget is released through draws you request online as work is completed."),
        anatoliy_note("<p>Send me the address, the price, your budget and what it will sell for. I&rsquo;ll tell you which loan fits and how much cash you need to bring, before you pay for an appraisal.</p>",
                      "Send me the deal first"),
        faq_section(faqs, "Questions about hard money loans"),
        related("hard-money-loans"),
        cta_band("Have a deal in California?", "Send the address, price and budget. You&rsquo;ll hear which loan fits and how much leverage to expect before you pay for an appraisal."),
        DISCLOSURE,
    ]
    return dict(
        slug="hard-money-loans",
        terms=terms,
        strip=["Up to 90% of the price + 100% of the rehab", "Loans from $50K to $3M", "No personal income verification", "Soft credit pull for terms"],
        title="Hard Money Loans in California | West Coast Capital Mortgage",
        description="Hard money and private money loans for California real estate investors: fix and flip, bridge and construction loans, up to 90% of purchase and 100% of rehab.",
        h1="Hard Money Loans in California", crumb="Hard Money Loans",
        lead="Short-term private money for California real estate investors: buy, fix, build or bridge a property, with the loan closed in your LLC. Also available in Florida and Texas.",
        sections=sections, faqs=faqs,
        product=dict(name="Hard Money Loan", loanType="Hard money (private money) loan", min=50000, max=3000000, term=12, termUnit="MON",
                     collateral="Non-owner-occupied 1–4 unit residential investment property",
                     description="Short-term, interest-only private money loans for California real estate investors: fix and flip, bridge and ground-up construction, up to 90% of purchase and 100% of rehab."),
    )


def page_hard_money_la() -> dict:
    """Local page for the home market. Facts only: the Burbank office, where we lend,
    the same program terms as the California pages, and how permits and draws work."""
    terms = [
        ("Programs", "Fix and flip, bridge and ground-up construction <small>plus rental refinances</small>"),
        ("Purchase price financed", "Up to 90% <small>fix and flip</small>"),
        ("Rehab or construction budget", "100%, released in draws"),
        ("Loan vs. after-repair value", "70&ndash;75% max <small>fix and flip</small>"),
        ("Loan amount", "$50K &ndash; $3M"),
        ("Term", "12 months, interest only <small>no prepayment penalty</small>"),
        ("Credit score", "From 660 <small>680 for first-time investors</small>"),
        ("Where", "Los Angeles County and the San Fernando Valley <small>statewide in California, plus Florida and Texas</small>"),
        ("Office", "150 E Olive Ave, Unit 112, Burbank"),
    ]
    deals = table(
        ["The deal", "The loan", "Maximum leverage"],
        [
            ["Buy an older house, renovate it and sell", '<a href="fix-and-flip-loans.html">Fix and flip</a>', "90% of purchase + 100% of rehab"],
            ["Build a new home on a lot or a teardown", '<a href="ground-up-construction-loans.html">Ground-up construction</a>', "75% of land + 100% of construction"],
            ["Hold a finished flip while it sells or leases", '<a href="bridge-loans.html">Bridge</a>', "70% of value"],
            ["Keep it as a rental", '<a href="dscr-loans.html">DSCR</a> or <a href="rental-portfolio-loans.html">rental portfolio</a>', "80% LTV, 30 years"],
            ["Buy and renovate a 5+ unit building", '<a href="multifamily-bridge-loans.html">Multifamily bridge</a>', "75% of purchase + 100% of renovation"],
        ],
        caption="Hard money loans for Los Angeles deals",
    )
    faqs = [
        ("Who offers hard money loans in Burbank and the San Fernando Valley?",
         "West Coast Capital Mortgage, 150 E Olive Ave, Unit 112, Burbank. We offer fix and flip, bridge and construction loans across the Valley and the rest of Los Angeles County."),
        ("Do you lend in the City of Los Angeles, Glendale and Pasadena?",
         "Yes, across Los Angeles County. Terms can vary by neighborhood, and we confirm them on the first call."),
        ("How much can I borrow on a Los Angeles flip?",
         "Up to 90% of the price plus 100% of the rehab, within 70&ndash;75% of the after-repair value, from $50,000 to $3 million."),
        ("Can I get a loan for my first flip?",
         "Yes. First-time investors can get up to 90% of the price plus 100% of a light or moderate rehab, depending on credit."),
        ("Can I build a new home on a lot or a teardown?",
         "Yes, with a ground-up construction loan: up to 75% of the land with approved permits plus 100% of the construction budget, for builders with completed projects."),
        ("My flip is finished. Can I get a bridge loan while it sells?",
         "Yes. A bridge loan covers up to 70% of value on a finished home that is listed for sale or leasing up."),
        ("Can I meet you in person?",
         "Yes. The office is at 150 E Olive Ave, Unit 112, Burbank, CA 91502. Call 310-654-1577 to set a time."),
        CREDIT_PULL_FAQ,
        LLC_FAQ,
        SPEED_FAQ,
    ]
    sections = [
        term_sheet("Hard money terms in Los Angeles", terms, ""),
        answer("Where we lend in Los Angeles",
               """<p><b>San Fernando Valley:</b> Burbank, North Hollywood, Studio City, Sherman Oaks, Encino, Van Nuys, Reseda, Northridge, Granada Hills, Tarzana and Woodland Hills.</p>
  <p><b>Glendale, Pasadena and the foothills:</b> Glendale, La Crescenta, La Ca&ntilde;ada Flintridge, Pasadena and Altadena.</p>
  <p><b>City of Los Angeles:</b> Silver Lake, Echo Park, Eagle Rock, Highland Park, Mid-City, the Westside and South Los Angeles.</p>
  <p>And the rest of Los Angeles County. Terms can vary by neighborhood; we confirm what applies to your property on the first call.</p>"""),
        answer("Which loan fits your deal", deals, bg=True, anchor="programs"),
        answer("Permits and draws",
               """<p>Rehab and construction money is held back at closing and released in draws after an inspection confirms the work. Permits come from the city the property is in: LADBS for the City of Los Angeles, including most of the Valley, or the building departments of Burbank, Glendale, Pasadena and the other cities.</p>
  <p>On a new build, the land is financed at the highest leverage once permits are approved.</p>"""),
        how_it_works("The rehab or construction budget is released through draws you request online as work is completed."),
        anatoliy_note("<p>Our Los Angeles office is on Olive Avenue in Burbank. If your property is in the Valley or anywhere in Los Angeles County, send me the address, the price, your budget and what it will sell for, or come by the office. I&rsquo;ll tell you which loan fits and how much cash you need to bring, before you pay for an appraisal.</p>"
                      "<p>When the work is done, our sister brokerage <a href=\"https://westcoastcapitalrealty.com\">West Coast Capital Realty</a> can list it, and if you keep it, we can move you into a long-term <a href=\"dscr-loans.html\">DSCR loan</a>.</p>",
                      "We&rsquo;re in Los Angeles"),
        faq_section(faqs, "Questions about hard money in Los Angeles"),
        answer("More for Los Angeles",
               """<p><a href="loans/dscr/los-angeles-metro.html">DSCR loans in Los Angeles</a></p>
  <p><a href="hard-money-loans.html">Hard money loans across California</a></p>"""),
        related("hard-money-loans-los-angeles"),
        cta_band("Have a deal in Los Angeles?", "Send the address, price and budget. You&rsquo;ll hear which loan fits and how much leverage to expect before you pay for an appraisal."),
        DISCLOSURE,
    ]
    cities = ["Burbank", "Los Angeles", "Glendale", "Pasadena", "North Hollywood", "Studio City", "Sherman Oaks",
              "Encino", "Van Nuys", "Northridge", "Woodland Hills"]
    return dict(
        slug="hard-money-loans-los-angeles",
        terms=terms,
        strip=["Office in Los Angeles", "Up to 90% of the price + 100% of the rehab", "Loans from $50K to $3M", "Soft credit pull for terms"],
        title="Hard Money Loans in Los Angeles & San Fernando Valley | West Coast Capital Mortgage",
        description="Hard money and fix and flip loans in Los Angeles County and the San Fernando Valley from our Los Angeles office: up to 90% of purchase and 100% of rehab, $50K to $3M.",
        h1="Hard Money Loans in Los Angeles and the San Fernando Valley", crumb="Hard Money Loans in Los Angeles",
        programs_line="Fix &amp; Flip &middot; Ground-Up Construction &middot; Bridge Loans",
        lead="Fix and flip, construction and bridge loans for investors in the San Fernando Valley and across Los Angeles County, from our office in Los Angeles. The loan closes in your LLC.",
        sections=sections, faqs=faqs,
        area_served=[{"@type": "AdministrativeArea", "name": "Los Angeles County, California"},
                     {"@type": "Place", "name": "San Fernando Valley, California"}]
                    + [{"@type": "City", "name": f"{c}, California"} for c in cities],
        product=dict(name="Hard Money Loan in Los Angeles", loanType="Hard money (private money) loan", min=50000, max=3000000, term=12, termUnit="MON",
                     collateral="Non-owner-occupied 1–4 unit residential investment property",
                     description="Short-term private money loans for real estate investors in Los Angeles County and the San Fernando Valley: fix and flip, bridge and ground-up construction, up to 90% of purchase and 100% of rehab."),
    )


def llms_full(pages: list[dict]) -> str:
    out = ["# West Coast Capital Mortgage: investment property loans (full text)", "",
           f"> Investment property loans for real estate investors and developers in California, Florida and Texas. Loans close with West Coast Capital Mortgage (150 E Olive Ave, Unit 112, Burbank, CA 91502; NMLS #2817729; CA DRE Corporation License #02440065) and are funded by its private lender partner. Figures are program maximums; not a commitment to lend.",
           "", "Site summary and other sections: https://westcoastcapitalmortgage.com/llms.txt", ""]
    for p in pages:
        out += [f"## {plain(p['h1'])}", f"URL: {SITE}/{p['slug']}", "", plain(p["lead"]), ""]
        if p.get("terms"):
            out.append("Key terms:")
            out += [f"- {plain(label)}: {plain(value)}" for label, value in p["terms"]]
            out.append("")
        out.append("Questions and answers:")
        for q, a in p["faqs"]:
            out += [f"Q: {plain(q)}", f"A: {plain(a)}", ""]
    out += ["Contact: Anatoliy Kanevsky, founder (NMLS #2775380) · 310-654-1577 · direct 310-686-5053 · westccmortgage@gmail.com", ""]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def site_chrome() -> tuple[str, str]:
    src = (PUBLISH / "loans.html").read_text(encoding="utf-8")
    body_open = re.search(r"<body[^>]*>", src)
    header_end = src.find("</header>")
    footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL)
    if not body_open or header_end < 0 or not footer:
        raise SystemExit("Could not read the site chrome from loans.html")
    top = src[body_open.end():header_end + len("</header>")]
    top = re.sub(r"<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->\s*", "", top, flags=re.DOTALL)
    return top.strip(), footer.group(0)


def chrome_for(top: str) -> str:
    top = re.sub(r'(<nav class="mainnav"[^>]*>.*?</nav>)',
                 lambda m: m.group(1).replace(' class="active"', ""), top, flags=re.DOTALL)
    top, _ = links.add_nav_link(top, active=True)
    # The residential /apply application does not fit LLC business-purpose loans:
    # investor pages send borrowers to our white-label loan portal (Roc), and the
    # on-page "Tell Me Your Scenario" form keeps feeding leads to the CRM.
    top = top.replace('<a class="btn btn-blue" href="/apply" data-cta="preapproval">Get Preapproved</a>',
                      f'<a class="header-login" href="{PORTAL_LOGIN}" rel="noopener" data-cta="portal-login">Borrower Login</a>'
                      f'<a class="btn btn-blue" href="{PORTAL_APPLY}" rel="noopener" data-cta="portal-apply">Apply Online</a>', 1)
    # Desktop: the login link sits in the top bar next to the language switch (the main
    # header row has no room for it); the header-cta copy above shows only in the phone menu.
    top = re.sub(r'(<div class="topbar-right">\s*)',
                 lambda m: m.group(1) + f'<a class="topbar-login" href="{PORTAL_LOGIN}" rel="noopener" '
                                        f'data-cta="portal-login-top">Borrower Login</a>', top, count=1)
    if 'investor-loans.html" class="active"' not in top:
        top = re.sub(r'<a href="([^"]*investor-loans(?:\.html)?)">Investment Property Loans</a>',
                     r'<a href="\1" class="active">Investment Property Loans</a>', top, count=1)
    return top


_HOME_ORG: dict | None = None


def org_node() -> dict:
    """The homepage's #organization node (so every page describes one company), plus
    the states and loan types search engines and AI assistants should link to it."""
    global _HOME_ORG
    if _HOME_ORG is None:
        src = (PUBLISH / "index.html").read_text(encoding="utf-8")
        found = None
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
            for node in nodes:
                if isinstance(node, dict) and node.get("@id") == ORG_ID:
                    found = node
        if found is None:
            raise SystemExit("Homepage #organization node not found in index.html")
        keep = ("@type", "@id", "name", "legalName", "alternateName", "description", "url", "logo", "image", "telephone",
                "email", "address", "geo", "sameAs", "priceRange", "openingHoursSpecification")
        _HOME_ORG = {k: found[k] for k in keep if k in found}
    node = dict(_HOME_ORG)
    node.setdefault("areaServed", [{"@type": "State", "name": st} for st in STATES])
    node["knowsAbout"] = ["Fix and flip loans", "Hard money loans", "Private money loans", "Ground-up construction loans",
                          "Bridge loans", "DSCR loans", "Rental portfolio loans", "Multifamily bridge loans",
                          "Jumbo loans", "Non-QM loans", "Bank statement loans"]
    return node


def json_ld(page: dict) -> str:
    url = f"{SITE}/{page['slug']}"
    crumbs = [("Home", f"{SITE}/"), ("Loans", f"{SITE}/loans")]
    if page["slug"] != "investor-loans":
        crumbs.append(("Investment Property Loans", f"{SITE}/investor-loans"))
    crumbs.append((page["crumb"], url))
    states = page.get("area_served") or [{"@type": "State", "name": s} for s in page.get("states", STATES)]
    graph: list[dict] = [
        org_node(),
        {
            "@type": "Person", "@id": PERSON_ID, "name": "Anatoliy Kanevsky",
            "jobTitle": "Founder", "identifier": "NMLS #2775380", "worksFor": {"@id": ORG_ID},
            "image": f"{SITE}/{AVATAR}",
            "sameAs": ["https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/2775380"],
            "knowsAbout": ["Real estate investor financing", "Residential development", "Mortgage lending"],
        },
        {
            "@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": page["title"],
            "description": page["description"], "inLanguage": "en-US",
            "datePublished": UPDATED_ISO, "dateModified": MODIFIED_ISO,
            "publisher": {"@id": ORG_ID}, "reviewedBy": {"@id": PERSON_ID},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList", "@id": f"{url}#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(crumbs)],
        },
        {
            "@type": "FAQPage", "@id": f"{url}#faq",
            "mainEntity": [{"@type": "Question", "name": plain(q),
                            "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in page["faqs"]],
        },
    ]
    product = page.get("product")
    if product:
        graph[2]["about"] = {"@id": f"{url}#loan"}
        graph.append({
            "@type": "LoanOrCredit", "@id": f"{url}#loan", "name": product["name"], "url": url,
            "description": product["description"], "loanType": product["loanType"],
            "category": "Business-purpose real estate investor loan",
            "amount": {"@type": "MonetaryAmount", "currency": "USD", "minValue": product["min"], "maxValue": product["max"]},
            "loanTerm": {"@type": "QuantitativeValue", "value": product["term"], "unitCode": product["termUnit"]},
            "requiredCollateral": product["collateral"], "areaServed": states,
            "provider": {"@id": ORG_ID},
        })
    else:
        graph.append({
            "@type": "Service", "@id": f"{url}#service", "name": "Real estate investor loans",
            "serviceType": "Business-purpose real estate investor financing", "url": url,
            "provider": {"@id": ORG_ID}, "areaServed": states,
            "hasOfferCatalog": {
                "@type": "OfferCatalog", "name": "Investor loan programs",
                "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "LoanOrCredit", "name": name, "url": f"{SITE}/{slug}"}}
                                    for name, slug in page["catalog"]],
            },
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def render(page: dict, top: str, footer: str) -> str:
    url = f"{SITE}/{page['slug']}"
    title = html.escape(page["title"], quote=True)
    desc = html.escape(page["description"], quote=True)
    crumbs = '<a href="index.html">Home</a> &nbsp;/&nbsp; <a href="loans.html">Loans</a> &nbsp;/&nbsp; '
    if page["slug"] != "investor-loans":
        crumbs += '<a href="investor-loans.html">Investment Property Loans</a> &nbsp;/&nbsp; '
    crumbs += page["crumb"]
    programs_line = f'<p class="inv-programs-line">{page["programs_line"]}</p>\n    ' if page.get("programs_line") else ""
    hero = f"""<section class="page-hero inv-hero">
  <div class="hero-wallpaper" aria-hidden="true">
    <div class="wallpaper-line" style="top:18%">WEST COAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w2" style="top:58%">WEST COAST CAPITAL MORTGAGE</div>
  </div>
  <div class="wrap page-hero-inner">
    <div class="crumbs">{crumbs}</div>
    <h1>{page['h1']}</h1>
    {programs_line}<p class="lead">{page['lead']}</p>
    <div class="inv-updated">{face()}<span><b><a href="/loan-officer">Anatoliy Kanevsky</a></b><em>Founder &middot; NMLS #2775380</em></span></div>
    <div class="btn-row inv-hero-actions"><a class="btn btn-blue" href="#{FORM_ID}">Request a Call</a><a class="btn btn-outline" href="{PHONE_HREF}">Call {PHONE_TEXT}</a></div>
  </div>
</section>"""
    body = trust_strip(page.get("strip", STRIP_DEFAULT)) + "\n" + "\n".join(page["sections"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Caveat:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={gtm.ASSET_VERSION}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="West Coast Capital Mortgage">
<meta property="og:type" content="website">
<meta property="og:site_name" content="West Coast Capital Mortgage">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<script type="application/ld+json">
{json_ld(page)}
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "wzzlo9s35g");
</script>
</head>
<body class="investor-page">
{chrome_for(top)}
{hero}
{body}
{footer}
<script src="i18n-investor.js?v={gtm.ASSET_VERSION}"></script>
<script src="i18n.js?v={gtm.ASSET_VERSION}"></script>
<script src="script.js?v={gtm.ASSET_VERSION}"></script>
</body>
</html>
"""


PAGE_BUILDERS = (page_hub, page_fix_flip, page_ground_up, page_bridge, page_portfolio, page_multifamily, page_hard_money,
                 page_hard_money_la)
PAGE_FILES = tuple(f"{b()['slug']}.html" for b in PAGE_BUILDERS)


def main(publish: Path = PUBLISH) -> int:
    top, footer = site_chrome()
    written = []
    for builder in PAGE_BUILDERS:
        page = builder()
        path = publish / f"{page['slug']}.html"
        path.write_text(render(page, top, footer), encoding="utf-8")
        # Same production layers the Netlify build installs, so the committed
        # page is already what ships.
        gtm.inject(path)
        readiness.install_schema_twin(path, "investor-lead")
        readiness.install_schema_twin(path, "lead-details")
        readiness.install_partial_lead_twin(path)
        written.append(path.name)
    (publish / "llms-full.txt").write_text(llms_full([b() for b in PAGE_BUILDERS]), encoding="utf-8")
    print("Investor pages written: " + ", ".join(written) + "; llms-full.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
