import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const attributionFields = [
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
  'gclid', 'gbraid', 'wbraid', 'landing_page', 'submission_page',
]

function htmlFiles(dir) {
  const out = []
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) out.push(...htmlFiles(full))
    else if (entry.isFile() && entry.name.endsWith('.html')) out.push(full)
  }
  return out
}

for (const file of htmlFiles(root)) {
  let html = fs.readFileSync(file, 'utf8')
  let changed = false
  let cursor = 0

  // Register attribution fields on existing CaliforniaMTG contact forms.
  while (true) {
    const start = html.indexOf('<form', cursor)
    if (start < 0) break
    const tagEnd = html.indexOf('>', start)
    if (tagEnd < 0) break
    const close = html.indexOf('</form>', tagEnd)
    if (close < 0) break
    const openTag = html.slice(start, tagEnd + 1)
    const body = html.slice(tagEnd + 1, close)
    const isContact = /class\s*=\s*["'][^"']*\bcm-form\b[^"']*["']/i.test(openTag)
    const isNetlify = /data-netlify/i.test(openTag)
    if (isContact && isNetlify) {
      const missing = attributionFields.filter((name) => !new RegExp(`name=["']${name}["']`, 'i').test(body))
      if (missing.length) {
        const hidden = missing.map((name) => `<input type="hidden" name="${name}" value="" />`).join('')
        html = html.slice(0, tagEnd + 1) + hidden + html.slice(tagEnd + 1)
        cursor = close + hidden.length + 7
        changed = true
        continue
      }
    }
    cursor = close + 7
  }

  // Register one hidden fallback form for mobile Scenario Builder leads.
  if (path.basename(file) === 'index.html' && !html.includes('name="californiamtg-scenario-lead"')) {
    const form = `\n<form name="californiamtg-scenario-lead" data-netlify="true" hidden>\n` +
      `  <input type="hidden" name="form-name" value="californiamtg-scenario-lead" />\n` +
      `  <input name="full_name" /><input name="phone" /><input name="email" />\n` +
      `  <input name="lead_category" /><input name="scenario_type" /><input name="timeline" />\n` +
      `  <textarea name="message"></textarea><input name="landing_page" />\n` +
      `  <input name="utm_source" /><input name="utm_medium" /><input name="utm_campaign" />\n` +
      `  <textarea name="lead_json"></textarea>\n` +
      `</form>\n`
    html = html.replace('</body>', form + '</body>')
    changed = true
  }

  if (changed) fs.writeFileSync(file, html)
}

console.log('CaliforniaMTG Netlify fallback forms registered in build output.')
