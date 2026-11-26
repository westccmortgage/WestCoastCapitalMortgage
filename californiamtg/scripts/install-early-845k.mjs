import fs from 'node:fs';

const file = 'high-balance-conforming.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Who it\'s for</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('CaliforniaMTG high-balance insertion marker not found');
  const block = `
    <div id="${id}" class="card" style="margin:28px 0;border-left:4px solid #b08a4c">
      <p class="eyebrow gold">November 2026 update</p>
      <h2 style="margin-top:.35rem">2027 conforming loan limit: $855,400</h2>
      <p>FHFA announced the 2027 limits on November 24, 2026: the one-unit baseline rises to <strong>$855,400</strong> from $832,750, and the high-cost ceiling is <strong>$1,283,100</strong>. California county limits differ, so check the property&rsquo;s county.</p>
      <div class="btn-row"><a class="btn btn-primary" href="/early-conforming-loan-limit-845000">See the 2027 limits</a></div>
    </div>
`;
  html = html.replace(marker, block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed CaliforniaMTG early-$845K reference');
} else {
  console.log('CaliforniaMTG early-$845K reference already installed');
}
