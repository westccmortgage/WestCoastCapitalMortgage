import fs from 'node:fs';

const file = 'high-balance-conforming.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Who it\'s for</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('CaliforniaMTG high-balance insertion marker not found');
  const block = `
    <div id="${id}" class="card" style="margin:28px 0;border-left:4px solid #b08a4c">
      <p class="eyebrow gold">September 2026 update</p>
      <h2 style="margin-top:.35rem">Select lenders: early conforming limit up to $845,000</h2>
      <p>The official 2026 national one-unit baseline remains <strong>$832,750</strong>. Select lenders are now offering an early conforming limit up to <strong>$845,000</strong> ahead of FHFA's official 2027 announcement. California high-cost county limits remain separate and may already be higher than $845,000.</p>
      <p><strong>Keep the official county table unchanged:</strong> $845,000 is a lender-specific early limit, not a replacement FHFA county limit.</p>
      <div class="btn-row"><a class="btn btn-primary" href="/early-conforming-loan-limit-845000">See the $845K update</a></div>
    </div>
`;
  html = html.replace(marker, block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed CaliforniaMTG early-$845K reference');
} else {
  console.log('CaliforniaMTG early-$845K reference already installed');
}
