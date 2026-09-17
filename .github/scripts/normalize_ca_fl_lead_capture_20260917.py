from pathlib import Path

path = Path('wccm-corporate/script.js')
s = path.read_text(encoding='utf-8')
old = s

replacements = [
    (
        "function stateContext(){return param('state').toUpperCase()==='FL'?'FL':'CA';}",
        "function stateContext(){\n"
        "    var explicit=param('state').toUpperCase();\n"
        "    if(explicit==='FL'||explicit==='CA')return explicit;\n"
        "    var path=(window.location.pathname||'').replace(/\\.html$/,'').replace(/\\/$/,'');\n"
        "    if(path==='/florida'||path==='/florida-bank-statement-loans'||path==='/florida-dscr-loans'||path==='/florida-condo-financing'||path==='/boca-raton-mortgage-loans'||path==='/miami-dscr-foreign-national-loans')return 'FL';\n"
        "    return 'CA';\n"
        "  }"
    ),
    (
        'See whether a bank-statement path fits your California scenario',
        'See whether a bank-statement path fits your scenario'
    ),
    (
        '<div class=\"field\"><label for=\"bs-area\">California city / county</label><input id=\"bs-area\" name=\"property_area\" autocomplete=\"address-level2\" data-error-required=\"Enter a California city or county.\" required></div>',
        '<div class=\"field\"><label for=\"bs-area\">Property city / county</label><input id=\"bs-area\" name=\"property_area\" autocomplete=\"address-level2\" data-error-required=\"Enter the property city or county.\" required></div>'
    ),
    (
        "var CITY_FIELD={name:'property_area',label:'California city / county',required:'Enter a California city or county.',autocomplete:'address-level2'};",
        "var CITY_FIELD={name:'property_area',label:'Property city / county',required:'Enter the property city or county.',autocomplete:'address-level2'};"
    ),
    (
        "eyebrow:'Mortgage Review',heading:'Talk with a licensed California mortgage broker',",
        "eyebrow:'Mortgage Review',heading:'Talk with a mortgage professional',"
    ),
    (
        "eyebrow:'Jumbo Review',heading:'See whether a jumbo loan fits your California purchase or refinance',",
        "eyebrow:'Jumbo Review',heading:'See whether a jumbo loan fits your purchase or refinance',"
    ),
    (
        "eyebrow:'Self-Employed Review',heading:'See which self-employed path fits your California scenario',",
        "eyebrow:'Self-Employed Review',heading:'See which self-employed mortgage path fits your scenario',"
    ),
    (
        "points:['Qualify on the property’s rent, not your W-2','Close in your personal name or an LLC','Licensed California broker, many DSCR lenders'],",
        "points:['Qualify on the property’s rent, not your W-2','Close in your personal name or an LLC','Multiple DSCR lender options reviewed'],"
    ),
    (
        "points:['Financing above conforming loan limits','Purchase, refinance, or cash-out','Licensed California broker, many jumbo lenders'],",
        "points:['Financing above conforming loan limits','Purchase, refinance, or cash-out','Multiple jumbo lender options reviewed'],"
    ),
    (
        "points:['Qualify using bank deposits, not tax returns','Personal or business statements','Licensed California broker, many non-QM lenders'],",
        "points:['Alternative income documentation may use bank deposits','Personal or business statements may be reviewed','Multiple Non-QM lender options reviewed'],"
    ),
    (
        "points:['Options beyond tax returns','Bank statements, P&L, or 1099s may work','Licensed California broker, many lenders'],",
        "points:['Options beyond traditional tax-return income','Bank statements, P&L, or 1099s may be considered','Multiple lender options reviewed'],"
    ),
]

for a, b in replacements:
    if a not in s:
        raise SystemExit(f'Expected source text not found: {a[:120]}')
    s = s.replace(a, b)

if s == old:
    raise SystemExit('No changes made')

path.write_text(s, encoding='utf-8')

# Guardrails: root and generic high-intent forms must no longer present a CA-only lead gate.
check = path.read_text(encoding='utf-8')
for forbidden in [
    'Talk with a licensed California mortgage broker',
    'California city / county',
    'Enter a California city or county.',
    'See whether a bank-statement path fits your California scenario',
    'See whether a jumbo loan fits your California purchase or refinance',
    'See which self-employed path fits your California scenario',
    'Licensed California broker, many DSCR lenders',
    'Licensed California broker, many jumbo lenders',
    'Licensed California broker, many non-QM lenders',
    'Licensed California broker, many lenders',
]:
    if forbidden in check:
        raise SystemExit(f'CA-only lead text remains: {forbidden}')

for required in [
    "heading:'Talk with a mortgage professional'",
    "label:'Property city / county'",
    "path==='/florida-bank-statement-loans'",
    "path==='/florida-dscr-loans'",
    'Multiple Non-QM lender options reviewed',
]:
    if required not in check:
        raise SystemExit(f'Required normalized text missing: {required}')

print('Normalized CA/FL lead capture and Florida partial-lead state detection.')
