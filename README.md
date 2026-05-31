# West Coast Capital Mortgage Inc. — website

Static corporate mortgage site (West Coast, trilingual EN/ES/RU) plus a Florida‑facing
**sister brand, Suncoast Capital Mortgage**, generated from the same source. No build
step, no dependencies.

## Repository layout
- **`wccm-corporate/`** — the deployable West Coast static site. **This is the Netlify publish directory.**
  - `index.html`, `rates.html`, loan pages, `404.html`, `_redirects`, `assets/`, `styles.css`, `script.js`, `i18n.js`
  - `rate-tools.html` — internal, unlinked tool: converts the lender rate sheet (`.xlsx`) to `assets/rates.json` in the browser.
  - `assets/rates.json` — the small file that powers the public "Today's Rates" board.
- **`suncoast-corporate/`** — the deployable **Suncoast Capital Mortgage** static site (Florida‑facing brand,
  operated through West Coast Capital Mortgage Inc.). Same page structure, navy + gold palette, Suncoast
  homepage/About. Deploy as its own Netlify site (publish directory `suncoast-corporate`).
- **`tools/build_site.py`** — one‑time generator that produces everything in `wccm-corporate/`.
  Run: `python3 tools/build_site.py`. It does **not** touch `assets/rates.json` or `rate-tools.html`.
- **`tools/build_suncoast.py`** — Suncoast sister generator. It **imports** `build_site.py` and reuses every
  inner‑page body, content builder, and the JS — only the brand chrome (header/footer), homepage, About page,
  and color palette are overridden. **One maintenance system:** editing a loan page (or any inner page) in
  `build_site.py` updates *both* brands. Run: `python3 tools/build_suncoast.py` (writes into `../suncoast-corporate`).

## Netlify settings (Git deploy)
- Production branch: `main`
- Build command: *(none)*
- Publish directory: `wccm-corporate` (West Coast). For Suncoast, create a second Netlify site with publish directory `suncoast-corporate`.

## Updating today's rates
1. Open `/rate-tools.html`, drop the lender `.xlsx`, set comp points, **Download `rates.json`**.
2. Upload it to `wccm-corporate/assets/rates.json` (replace) and commit to `main`.
3. Netlify auto‑deploys; `/rates` and the homepage snapshot update.

West Coast Capital Mortgage Inc. · NMLS #2817729 · Equal Housing Opportunity.
