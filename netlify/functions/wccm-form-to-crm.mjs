const CRM_ENDPOINT = 'https://grcrm.com/.netlify/functions/lead-inbound'

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
      body: JSON.stringify(data),
      redirect: 'error',
    })

    if (!response.ok) {
      throw new Error(`CRM lead intake returned HTTP ${response.status}`)
    }
  },
}
