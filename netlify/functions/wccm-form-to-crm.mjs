const CRM_ENDPOINT = 'https://grcrm.com/.netlify/functions/lead-inbound'

// The CRM keeps only name, email, phone and message on the contact, so the
// program, the visitor's answers and the ad source are folded into the message.
// Everything else stays in the CRM intake log only.
const NOTE_SKIP = new Set([
  'form-name', 'form_name', 'company', 'full_name', 'name', 'first_name', 'last_name',
  'email', 'phone', 'message', 'program_interest', 'submission_id', 'lead_submission_id',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'gclid', 'gbraid', 'wbraid', 'fbclid', 'landing_page', 'conversion_page', 'source_path',
  'page_path', 'referrer', 'ip', 'user_agent',
])

function text(value) {
  return value == null ? '' : String(value).trim()
}

function pagePath(data) {
  const raw = text(data.page_path) || text(data.conversion_page) || text(data.landing_page)
  try {
    return raw ? new URL(raw, 'https://westcoastcapitalmortgage.com').pathname : ''
  } catch {
    return ''
  }
}

function leadNote(data) {
  const answers = Object.entries(data)
    .filter(([key, value]) => !NOTE_SKIP.has(key) && text(value))
    .map(([key, value]) => `${key.replace(/_/g, ' ')}: ${text(value)}`)
  const source = ['utm_source', 'utm_medium', 'utm_campaign'].map((key) => text(data[key])).filter(Boolean)
  const page = pagePath(data)
  return [
    [text(data.program_interest), ...answers].filter(Boolean).join(' · '),
    [source.length && `Source: ${source.join(' / ')}`, page && `Page: ${page}`].filter(Boolean).join(' · '),
    text(data.message),
  ].filter(Boolean).join('\n')
}

function requireEnv(name) {
  const value = Netlify.env.get(name)
  if (!value) throw new Error(`Missing required environment variable: ${name}`)
  return value
}

export default {
  async formSubmitted(event) {
    const token = requireEnv('WCCM_CRM_LEAD_TOKEN')
    const data = event?.data

    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      throw new Error('Netlify form event did not include a valid data object')
    }

    const response = await fetch(CRM_ENDPOINT, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-lead-token': token,
      },
      body: JSON.stringify({ ...data, message: leadNote(data) }),
      redirect: 'error',
    })

    if (!response.ok) {
      throw new Error(`CRM lead intake returned HTTP ${response.status}`)
    }
  },
}
