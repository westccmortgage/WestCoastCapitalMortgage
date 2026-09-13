import fs from 'node:fs';

const file = 'california-jumbo-loan-limits-2026.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Key California county limits for 2026</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('BeforeJumbo limit-table insertion marker not found');
  const block = `
    <div id="${id}" class="limit-callout">
      <p class="hero__label">New lender update · September 2026</p>
      <h2 style="margin-top:.35rem">Select lenders are offering an early conforming limit up to $845,000</h2>
      <p>The official 2026 one-unit national baseline remains <strong>$832,750</strong>. The early <strong>$845,000</strong> figure is lender-specific and does <strong>not</strong> replace the official FHFA county limits in the table below.</p>
      <p>For a baseline county, a loan near $840,000 may now have an additional conforming path through an eligible lender. In a high-cost California county, the official county limit may already be above $845,000.</p>
      <p><a class="btn btn--primary" href="/early-conforming-loan-limit-845000">Read the $845K update →</a></p>
    </div>
`;
  html = html.replace(marker, block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed BeforeJumbo early-$845K reference');
} else {
  console.log('BeforeJumbo early-$845K reference already installed');
}
