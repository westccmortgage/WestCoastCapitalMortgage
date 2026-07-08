# westcoastcapitalmortgage.com — alias deploy

Standalone Netlify site for the alias domain **westcoastcapitalmortgage.com**, which
301-redirects to the primary site **westccmortgage.com**. No build step, no dependencies.

## Files
- `sitemap.xml` — index/homepage sitemap for `https://westcoastcapitalmortgage.com/`.
- `robots.txt` — points crawlers at `https://westcoastcapitalmortgage.com/sitemap.xml`.
- `_redirects` — serves `sitemap.xml` and `robots.txt` directly (200); 301-redirects
  every other path to `https://westccmortgage.com/:splat`.
- `index.html` — meta-refresh fallback to the primary site.

## Netlify settings
- Publish directory: `westcoastcapitalmortgage` (or drag-and-drop this folder's contents).
