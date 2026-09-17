#!/usr/bin/env python3
"""Make the WCCM publish tree safe to send paid search traffic to.

Two jobs, both idempotent and both re-applied on every build so generated pages
cannot silently lose them:

1. Link the privacy policy and terms from the footer. Both pages existed but
   nothing on the site linked to them, and Google Ads requires the policy to be
   reachable from the landing page.
2. Declare hidden schema twins for the lead forms that script.js injects. The
   Netlify deploy parser never sees a JS-injected form, and Netlify stores only
   the fields of a registered form, so an undeclared field is dropped silently.
   Field lists here must stay in step with PROGRAM_LEAD_FORMS in script.js.
"""
from __future__ import annotations

import re
from pathlib import Path

PUBLISH_DIR = Path(__file__).resolve().parent.parent / "wccm-corporate"

LEGAL_NAV_RE = re.compile(r'(<nav aria-label="Legal">)(.*?)(</nav>)', re.IGNORECASE | re.DOTALL)
LICENSING_LINK_RE = re.compile(r'<a href="(/?)about\.html"[^>]*>Licensing and Disclosures</a>', re.IGNORECASE)
SCRIPT_ANCHOR = '<script src="i18n.js">'
SCRIPT_ANCHOR_ROOTED = '<script src="/i18n.js">'

ATTRIBUTION_FIELDS = (
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "gbraid", "wbraid", "landing_page", "conversion_page", "source_path",
    "referrer",
)

# Reliable-delivery id (see wccm-corporate/script.js). Declared for every lead
# form the same way ATTRIBUTION_FIELDS is, so Netlify does not drop it.
SUBMISSION_ID_FIELDS = ("submission_id",)

# Partial-lead capture (abandoned-form recovery). A visitor who typed a
# plausible email or phone and then left the page without submitting gets
# recorded here by script.js via sendBeacon/fetch. Never used for SMS.
PARTIAL_LEAD_CONTENT_FIELDS = (
    "source_form", "page_path", "state_context", "name", "first_name", "last_name",
    "email", "phone", "program_interest", "details", "submission_id", "partial_reason",
    "status", "sms_consent",
)
PARTIAL_LEAD_ATTRIBUTION_FIELDS = (
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "gbraid", "wbraid", "landing_page", "referrer",
)

FORM_SCHEMAS = {
    "bank-statement-lead": (
        "goal", "property_area", "loan_amount", "statements_available", "self_employed_years",
        "full_name", "email", "phone", "message",
    ),
    "mortgage-lead": (
        "goal", "property_area", "loan_amount", "timeline",
        "full_name", "email", "phone", "message",
    ),
    "jumbo-lead": (
        "goal", "property_area", "purchase_price", "loan_amount", "income_documentation",
        "full_name", "email", "phone", "message",
    ),
    "dscr-lead": (
        "goal", "property_area", "property_type", "monthly_rent", "loan_amount", "vesting",
        "full_name", "email", "phone", "message",
    ),
    "self-employed-lead": (
        "goal", "property_area", "loan_amount", "income_documentation", "self_employed_years",
        "full_name", "email", "phone", "message",
    ),
    # Optional step 2 of the hero quick form (QUICK_LEAD_FORMS in script.js):
    # one shared form for every landing page, linked to the step-1 lead by
    # lead_submission_id. Union of every page's step-2 fields.
    "lead-details": (
        "lead_submission_id", "source_form", "full_name", "phone", "goal",
        "property_type", "income_documentation", "statements_available", "occupancy",
        "property_area", "purchase_price", "loan_amount", "monthly_rent",
        "self_employed_years", "country_of_residence", "email",
    ),
}

PAGE_FORMS = {
    "bank-statement-loans.html": "bank-statement-lead",
    "index.html": "mortgage-lead",
    "jumbo-loans.html": "jumbo-lead",
    "dscr-loans.html": "dscr-lead",
    "self-employed-borrowers.html": "self-employed-lead",
    "florida-condo-financing.html": "mortgage-lead",
    "foreign-national-loans.html": "mortgage-lead",
    "loans/jumbo/los-angeles-county.html": "jumbo-lead",
    "loans/dscr/los-angeles-metro.html": "dscr-lead",
}

# Pages whose hero quick form posts step 2 as "lead-details".
QUICK_FORM_PAGES = (
    "bank-statement-loans.html",
    "jumbo-loans.html",
    "dscr-loans.html",
    "self-employed-borrowers.html",
    "florida-condo-financing.html",
    "foreign-national-loans.html",
)


def build_schema_twin(form_name: str) -> str:
    fields = FORM_SCHEMAS[form_name]
    lines = [
        f'<form name="{form_name}" netlify netlify-honeypot="company" hidden>',
        f'  <input type="hidden" name="form-name" value="{form_name}">',
        '  <input type="text" name="company">',
        '  <input type="hidden" name="program_interest">',
    ]
    for field in fields:
        if field == "message":
            lines.append('  <textarea name="message"></textarea>')
        else:
            lines.append(f'  <input name="{field}">')
    for field in ATTRIBUTION_FIELDS:
        lines.append(f'  <input name="{field}">')
    for field in SUBMISSION_ID_FIELDS:
        lines.append(f'  <input name="{field}">')
    lines.append("</form>")
    return "\n".join(lines)


def build_partial_lead_twin() -> str:
    lines = [
        '<form name="partial-lead" netlify netlify-honeypot="company" hidden>',
        '  <input type="hidden" name="form-name" value="partial-lead">',
        '  <input type="text" name="company">',
    ]
    for field in PARTIAL_LEAD_CONTENT_FIELDS:
        if field == "details":
            lines.append(f'  <textarea name="{field}"></textarea>')
        else:
            lines.append(f'  <input name="{field}">')
    for field in PARTIAL_LEAD_ATTRIBUTION_FIELDS:
        lines.append(f'  <input name="{field}">')
    lines.append("</form>")
    return "\n".join(lines)


def install_legal_links(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    match = LEGAL_NAV_RE.search(text)
    if not match:
        return False
    body = match.group(2)
    if "privacy-policy" in body and 'href="/terms.html"' in body or "privacy-policy" in body and 'href="terms.html"' in body:
        return False

    licensing = LICENSING_LINK_RE.search(body)
    if not licensing:
        return False
    prefix = licensing.group(1)  # "/" on pages that live in a subdirectory

    additions = (
        f'\n          <a href="{prefix}privacy-policy.html" style="display:inline;margin-right:18px">Privacy Policy</a>'
        f'\n          <a href="{prefix}terms.html" style="display:inline;margin-right:18px">Terms of Use</a>'
    )
    new_body = body[: licensing.end()] + additions + body[licensing.end():]
    updated = text[: match.start(2)] + new_body + text[match.end(2):]
    path.write_text(updated, encoding="utf-8")
    return True


TWIN_RE_TEMPLATE = r'(<form name="{name}"[^>]*hidden>)(.*?)(</form>)'


def upgrade_schema_twin(path: Path, form_name: str) -> bool:
    """Add fields the injected form now sends but the schema never declared.

    Netlify drops undeclared fields without warning, so a schema that drifts
    behind script.js silently loses data. Adding is safe; nothing is removed.
    """
    text = path.read_text(encoding="utf-8")
    match = re.search(
        TWIN_RE_TEMPLATE.format(name=re.escape(form_name)), text, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return False
    body = match.group(2)
    wanted = list(FORM_SCHEMAS[form_name]) + list(ATTRIBUTION_FIELDS) + list(SUBMISSION_ID_FIELDS)
    missing = [f for f in wanted if f'name="{f}"' not in body]
    if not missing:
        return False
    additions = "".join(
        f'  <textarea name="{f}"></textarea>\n' if f == "message" else f'  <input name="{f}">\n'
        for f in missing
    )
    updated = text[: match.start(3)] + additions + text[match.start(3):]
    path.write_text(updated, encoding="utf-8")
    return True


def install_schema_twin(path: Path, form_name: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if f'name="{form_name}"' in text:
        return upgrade_schema_twin(path, form_name)
    twin = build_schema_twin(form_name)
    for anchor in (SCRIPT_ANCHOR, SCRIPT_ANCHOR_ROOTED):
        pos = text.find(anchor)
        if pos >= 0:
            path.write_text(text[:pos] + twin + "\n" + text[pos:], encoding="utf-8")
            return True
    pos = text.lower().rfind("</body>")
    if pos < 0:
        return False
    path.write_text(text[:pos] + twin + "\n" + text[pos:], encoding="utf-8")
    return True


def upgrade_partial_lead_twin(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        TWIN_RE_TEMPLATE.format(name=re.escape("partial-lead")), text, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return False
    body = match.group(2)
    wanted = list(PARTIAL_LEAD_CONTENT_FIELDS) + list(PARTIAL_LEAD_ATTRIBUTION_FIELDS)
    missing = [f for f in wanted if f'name="{f}"' not in body]
    if not missing:
        return False
    additions = "".join(
        f'  <textarea name="{f}"></textarea>\n' if f == "details" else f'  <input name="{f}">\n'
        for f in missing
    )
    updated = text[: match.start(3)] + additions + text[match.start(3):]
    path.write_text(updated, encoding="utf-8")
    return True


def install_partial_lead_twin(path: Path) -> bool:
    """Register the partial-lead (abandoned-form) Netlify form.

    Netlify unions a form's schema across every page that declares it, so one
    static hidden twin per paid-search landing page is enough for the whole
    site to submit to "partial-lead" from any page — but every lead-form page
    carries its own twin here for redundancy rather than relying on a single
    page.
    """
    text = path.read_text(encoding="utf-8")
    if 'name="partial-lead"' in text:
        return upgrade_partial_lead_twin(path)
    twin = build_partial_lead_twin()
    for anchor in (SCRIPT_ANCHOR, SCRIPT_ANCHOR_ROOTED):
        pos = text.find(anchor)
        if pos >= 0:
            path.write_text(text[:pos] + twin + "\n" + text[pos:], encoding="utf-8")
            return True
    pos = text.lower().rfind("</body>")
    if pos < 0:
        return False
    path.write_text(text[:pos] + twin + "\n" + text[pos:], encoding="utf-8")
    return True


def main() -> None:
    if not PUBLISH_DIR.is_dir():
        raise SystemExit(f"Publish directory not found: {PUBLISH_DIR}")

    # Bust previously cached handlers on every page, including nested pages.
    # This runs after tools/install_wccm_gtm.py in the build command and
    # touches every page unconditionally, so this literal is the version that
    # actually ships — keep it in step with ASSET_VERSION in that script.
    for page in PUBLISH_DIR.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        updated = re.sub(r'(src=["\'](?:[^"\']*/)?script\\.js)(?:\\?[^"\']*)?(["\'])',
                         r'\1?v=20260917-dscr-highlights\2', html)
        if updated != html:
            page.write_text(updated, encoding="utf-8")

    legal_changed = 0
    legal_seen = 0
    for path in sorted(PUBLISH_DIR.rglob("*.html")):
        if 'aria-label="Legal"' not in path.read_text(encoding="utf-8"):
            continue
        legal_seen += 1
        if install_legal_links(path):
            legal_changed += 1

    twins_changed = 0
    partial_twins_changed = 0
    for relative, form_name in PAGE_FORMS.items():
        page = PUBLISH_DIR / relative
        if not page.is_file():
            raise SystemExit(f"Paid-search landing page is missing: {relative}")
        if install_schema_twin(page, form_name):
            twins_changed += 1
        if install_partial_lead_twin(page):
            partial_twins_changed += 1
    for relative in QUICK_FORM_PAGES:
        if install_schema_twin(PUBLISH_DIR / relative, "lead-details"):
            twins_changed += 1

    missing = [name for name in list(FORM_SCHEMAS) + ["partial-lead"] if not any(
        f'name="{name}"' in (PUBLISH_DIR / rel).read_text(encoding="utf-8")
        for rel in PAGE_FORMS
    )]
    if missing:
        raise SystemExit("Lead form schema was not declared for: " + ", ".join(missing))

    print(
        f"Ads readiness: legal links {legal_changed} added of {legal_seen} footers; "
        f"lead form schemas {twins_changed} written or upgraded of {len(PAGE_FORMS)} pages; "
        f"partial-lead schemas {partial_twins_changed} written or upgraded of {len(PAGE_FORMS)} pages."
    )


if __name__ == "__main__":
    main()
