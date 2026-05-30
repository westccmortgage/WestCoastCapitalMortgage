# West Coast Capital Mortgage Inc. — website

Static, trilingual (EN/ES/RU) corporate mortgage site. No build step, no dependencies.

## Repository layout
- **`wccm-corporate/`** — the deployable static site. **This is the Netlify publish directory.**
  - `index.html`, `rates.html`, loan pages, `404.html`, `_redirects`, `assets/`, `styles.css`, `script.js`, `i18n.js`
  - `rate-tools.html` — internal, unlinked tool: converts the lender rate sheet (`.xlsx`) to `assets/rates.json` in the browser.
  - `assets/rates.json` — the small file that powers the public "Today's Rates" board.
- **`tools/build_site.py`** — one‑time generator that produces everything in `wccm-corporate/`.
  Run: `python3 tools/build_site.py` (writes into `../wccm-corporate`). It does **not** touch `assets/rates.json` or `rate-tools.html`.

## Netlify settings (Git deploy)
- Production branch: `main`
- Build command: *(none)*
- Publish directory: `wccm-corporate`

## Updating today's rates
1. Open `/rate-tools.html`, drop the lender `.xlsx`, set comp points, **Download `rates.json`**.
2. Upload it to `wccm-corporate/assets/rates.json` (replace) and commit to `main`.
3. Netlify auto‑deploys; `/rates` and the homepage snapshot update.

West Coast Capital Mortgage Inc. · NMLS #2817729 · Equal Housing Opportunity.
