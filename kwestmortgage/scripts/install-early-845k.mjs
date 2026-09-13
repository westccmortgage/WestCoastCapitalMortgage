import fs from 'node:fs';

const file = 'high-balance-conforming.html';
let html = fs.readFileSync(file, 'utf8');
const marker = '<h2>Who it may fit in Key West</h2>';
const id = 'early-845k-reference';

if (!html.includes(id)) {
  if (!html.includes(marker)) throw new Error('KWest high-balance insertion marker not found');
  const block = `
<div id="${id}" class="note-strip" style="margin:24px 0;padding:22px">
  <strong>September 2026 update:</strong> select lenders are offering an early national conforming limit up to <strong>$845,000</strong>, while the official 2026 baseline remains <strong>$832,750</strong>. For Key West, do not replace the county line with $845,000: Monroe County's official 2026 one-unit conforming limit is <strong>$990,150</strong>.
  <div style="margin-top:14px"><a class="btn btn--ghost" href="/early-conforming-loan-limit-845000">See what the $845K update means for Key West →</a></div>
</div>
`;
  html = html.replace(marker, block + marker);
  fs.writeFileSync(file, html);
  console.log('Installed KWest early-$845K reference');
} else {
  console.log('KWest early-$845K reference already installed');
}
