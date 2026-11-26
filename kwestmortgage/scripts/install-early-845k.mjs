import fs from 'node:fs';

const file = 'high-balance-conforming.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Who it may fit in Key West</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('KWest high-balance insertion marker not found');
  const block = `
<div id="${id}" class="note-strip" style="margin:24px 0;padding:22px">
  <strong>FHFA update &middot; November 24, 2026:</strong> the 2027 national one-unit conforming baseline is <strong>$855,400</strong> (up $22,650 from $832,750), with a high-cost ceiling of <strong>$1,283,100</strong>. Monroe County is a high-cost county, so check FHFA's county map for its 2027 limit; county figures shown on this site are 2026 reference figures. The early $845,000&ndash;$850,000 limits some lenders offered in September 2026 are superseded by the official 2027 baseline.
  <div style="margin-top:14px"><a class="btn btn--ghost" href="/early-conforming-loan-limit-845000">Read the 2027 limit update &rarr;</a></div>
</div>
`;
  html = html.replace(marker, () => block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed KWest 2027 limit update block');
} else {
  console.log('KWest 2027 limit update block already installed');
}
