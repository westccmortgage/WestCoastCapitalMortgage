exports.handler = async function () {
  const sourceUrl = 'https://deploy-preview-15--chipper-maamoul-a2b9d5.netlify.app/__statecourse_private_export_8f3c1a7d/california-source.json';
  try {
    const response = await fetch(sourceUrl);
    const body = await response.text();
    return {
      statusCode: response.status,
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'content-disposition': 'attachment; filename="california-source.json"',
        'cache-control': 'no-store, max-age=0'
      },
      body
    };
  } catch (error) {
    return {
      statusCode: 502,
      headers: { 'content-type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ error: 'Temporary export proxy failed', detail: String(error) })
    };
  }
};
