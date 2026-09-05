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
}

PAGE_FORMS = {
    "bank-statement-loans.html": "bank-statement-lead",
    "index.html": "mortgage-lead",
    "jumbo-loans.html": "jumbo-lead",
    "dscr-loans.html": "dscr-lead",
    "self-employed-borrowers.html": "self-employed-lead",
    "loans/jumbo/los-angeles-county.html": "jumbo-lead",
    "loans/dscr/los-angeles-metro.html": "dscr-lead",
}


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
    wanted = list(FORM_SCHEMAS[form_name]) + list(ATTRIBUTION_FIELDS)
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


def main() -> None:
    if not PUBLISH_DIR.is_dir():
        raise SystemExit(f"Publish directory not found: {PUBLISH_DIR}")

    # Bust previously cached handlers on every page, including nested pages.
    for page in PUBLISH_DIR.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        updated = re.sub(r'(src=["\'](?:[^"\']*/)?script\\.js)(?:\\?[^"\']*)?(["\'])',
                         r'\1?v=20260904-validation\2', html)
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
    for relative, form_name in PAGE_FORMS.items():
        page = PUBLISH_DIR / relative
        if not page.is_file():
            raise SystemExit(f"Paid-search landing page is missing: {relative}")
        if install_schema_twin(page, form_name):
            twins_changed += 1

    missing = [name for name in FORM_SCHEMAS if not any(
        f'name="{name}"' in (PUBLISH_DIR / rel).read_text(encoding="utf-8")
        for rel in PAGE_FORMS
    )]
    if missing:
        raise SystemExit("Lead form schema was not declared for: " + ", ".join(missing))

    print(
        f"Ads readiness: legal links {legal_changed} added of {legal_seen} footers; "
        f"lead form schemas {twins_changed} written or upgraded of {len(PAGE_FORMS)} pages."
    )


if __name__ == "__main__":
    main()
