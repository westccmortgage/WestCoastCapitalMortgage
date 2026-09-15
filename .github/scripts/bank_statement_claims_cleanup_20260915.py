from pathlib import Path

p = Path(__file__).resolve().parents[2] / "wccm-corporate" / "bank-statement-loans.html"
s = p.read_text(encoding="utf-8")

replacements = {
    'Bank statement mortgage loans for self-employed borrowers. No tax returns required. 12–24 month bank statements. West Coast Capital Mortgage. NMLS #2817729.':
        'Bank statement mortgage guidance for self-employed borrowers. Eligible programs may use personal or business bank statements as alternative income documentation; requirements vary by lender and file. West Coast Capital Mortgage Inc. NMLS #2817729.',
    '<li>No tax returns required for income</li>':
        '<li>Tax returns may not be required for income qualification under eligible programs; documentation varies by lender and file</li>',
    '<div class="acc-body">Most programs review 12 to 24 months of deposits to establish qualifying income.</div>':
        '<div class="acc-body">Statement periods vary by lender and program; many bank-statement programs review a recent series of personal or business statements to establish qualifying income.</div>',
}

changed = False
for old, new in replacements.items():
    if old in s:
        s = s.replace(old, new)
        changed = True

if changed:
    p.write_text(s, encoding="utf-8")

out = p.read_text(encoding="utf-8")
assert 'No tax returns required. 12–24 month bank statements.' not in out
assert '<li>No tax returns required for income</li>' not in out
assert 'requirements vary by lender and file' in out
print('Bank statement claims accuracy cleanup validated')
