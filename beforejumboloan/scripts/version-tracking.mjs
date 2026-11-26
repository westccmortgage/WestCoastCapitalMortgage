import fs from 'node:fs';
import path from 'node:path';
function walk(dir) {
  for (const entry of fs.readdirSync(dir,{withFileTypes:true})) {
    const p=path.join(dir,entry.name);
    if(entry.isDirectory()) {
      if(!['node_modules','.git','netlify'].includes(entry.name))walk(p);
    } else if(p.endsWith('.html')) {
      const html=fs.readFileSync(p,'utf8');
      const updated=html.replace(/(src=["'](?:[^"']*\/)?js\/[A-Za-z0-9_-]+\.js)(?:\?[^"']*)?(["'])/g,'$1?v=20261125-m$2');
      if(updated!==html)fs.writeFileSync(p,updated);
    }
  }
}
walk('.');
