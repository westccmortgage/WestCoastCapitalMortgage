import fs from 'node:fs';

const file = 'california-jumbo-loan-limits-2026.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Key California county limits for 2026</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('BeforeJumbo limit-table insertion marker not found');
  const block = `
    <div id="${id}" class="limit-callout">
      <p class="source-note"><strong>FHFA update &middot; November 24, 2026</strong></p>
      <h2 style="margin-top:.35rem">2027 conforming loan limit: $855,400</h2>
      <p>FHFA raised the 2027 one-unit baseline to <strong>$855,400</strong> (up $22,650 from $832,750), with a high-cost ceiling of <strong>$1,283,100</strong>. The county figures in the table below are the <strong>2026</strong> limits, so check your county&rsquo;s 2027 limit on <a href="https://www.fhfa.gov/data/dashboard/conforming-loan-limits" target="_blank" rel="noopener noreferrer">FHFA&rsquo;s map</a>.</p>
      <p>The early $845,000&ndash;$850,000 limits some lenders offered in September 2026 are superseded by the official 2027 baseline.</p>
      <p><a class="btn btn--primary" href="/early-conforming-loan-limit-845000">Read the 2027 limit update &rarr;</a></p>
    </div>
`;
  html = html.replace(marker, () => block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed BeforeJumbo 2027 limit update block');
} else {
  console.log('BeforeJumbo 2027 limit update block already installed');
}
