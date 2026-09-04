import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const scriptTag = '<script src="/js/ads.js" defer></script>'
const attributionFields = [
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'gclid', 'gbraid', 'wbraid', 'landing_page', 'submission_page',
]

function htmlFiles(dir) {
  const out = []
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) out.push(...htmlFiles(full))
    else if (entry.isFile() && entry.name.endsWith('.html')) out.push(full)
  }
  return out
}

for (const file of htmlFiles(root)) {
  let html = fs.readFileSync(file, 'utf8')
  let changed = false

  if (!html.includes('/js/ads.js') && html.includes('</body>')) {
    html = html.replace('</body>', `${scriptTag}\n</body>`)
    changed = true
  }

  // Register campaign-attribution fields on every Netlify lead form while
  // keeping them invisible. This lets the existing form handler submit them.
  let cursor = 0
  while (true) {
    const formStart = html.indexOf('<form', cursor)
    if (formStart < 0) break
    const formTagEnd = html.indexOf('>', formStart)
    if (formTagEnd < 0) break
    const formClose = html.indexOf('</form>', formTagEnd)
    if (formClose < 0) break
    const openTag = html.slice(formStart, formTagEnd + 1)
    const formBody = html.slice(formTagEnd + 1, formClose)
    const isNetlify = /data-netlify(?:\s*=\s*["']true["'])?/i.test(openTag)
    const nameMatch = openTag.match(/name\s*=\s*["']([^"']+)["']/i)
    const name = nameMatch ? nameMatch[1] : ''
    const isLead = isNetlify && /(?:key-west|kwest|monroe).*(?:scenario|review|lead|contact|mortgage)|(?:scenario|review).*(?:key-west|kwest|monroe)/i.test(name)

    if (isLead) {
      const missing = attributionFields.filter((field) => !new RegExp(`name=["']${field}["']`, 'i').test(formBody))
      if (missing.length) {
        const hidden = missing.map((field) => `<input type="hidden" name="${field}" value="" />`).join('')
        html = html.slice(0, formTagEnd + 1) + hidden + html.slice(formTagEnd + 1)
        const delta = hidden.length
        cursor = formClose + delta + 7
        changed = true
        continue
      }
    }
    cursor = formClose + 7
  }

  if (changed) fs.writeFileSync(file, html)
}

console.log('K West Ads tracking installed in build output.')
