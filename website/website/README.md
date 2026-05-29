# West Coast Capital Mortgage — Website

A fast, modern, fully static website for West Coast Capital Mortgage Inc. (NMLS# 2775380).
No build step required — just static HTML, CSS, and JavaScript. Perfect for GitHub + Netlify.

## What's inside

| Page | File |
|------|------|
| Home | `index.html` |
| Calculators (payment / refinance / affordability / rent-vs-buy) | `calculators.html` |
| Apply online (multi-step wizard) | `apply.html` |
| Contact / rate quote | `contact.html` |
| About the founder | `about.html` |
| Reviews | `reviews.html` |
| Blog | `blog.html` |
| Loan programs | `conventional.html`, `fha.html`, `va.html`, `usda.html`, `jumbo.html`, `fixed-rate.html`, `refinance.html`, `renovation-203k.html`, `reverse.html` |

Shared assets live in `/assets` (CSS, JS, logo, favicon). An AI chat assistant appears on every page.

## Deploy to GitHub + Netlify

### 1. Push to GitHub
```bash
cd "this folder"
git init
git add .
git commit -m "Launch West Coast Capital Mortgage website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/west-coast-capital-mortgage.git
git push -u origin main
```

### 2. Connect to Netlify
1. Log in at https://app.netlify.com → **Add new site → Import an existing project**.
2. Choose **GitHub** and pick the repo you just pushed.
3. Build settings: leave **Build command empty**, set **Publish directory** to `.` (already configured in `netlify.toml`).
4. Click **Deploy**. Your site goes live at `https://YOUR-SITE.netlify.app`.

### 3. Forms work automatically
The Apply and Contact forms use **Netlify Forms** (`data-netlify="true"`). Submissions show up under
**Netlify dashboard → Forms**. Add a notification email under **Forms → Settings → Form notifications**
to get every lead in your inbox.

### 4. Custom domain (optional)
Netlify → **Domain settings → Add a domain** (e.g. `westcoastcapitalmortgage.com`), then point your DNS
to Netlify. HTTPS is provisioned automatically and free.

## Editing content
- **Rates:** edit the `RATES` list in `build/build.py` (or directly in `index.html` / `calculators.html`).
- **Reviews / blog posts:** edit `ALL_REVIEWS` and `POSTS` in `build/build3.py`, or the HTML directly.
- **Phone / NMLS / company info:** centralized in `build/chrome.py`.
- The `build/` scripts regenerate every page; you can also just hand-edit the `.html` files.

## Logo (done) & founder photo (1 file to add)

- **Logo:** already built as crisp, scalable SVG — `assets/img/logo-horizontal.svg` (used in the header), plus `logo-mark.svg` (icon only) and `logo.svg` (stacked lockup). The favicon is generated to match. No action needed.

- **Founder photo (the desk portrait):** drop your photo into
  `assets/img/photos/`
  named `founder` — **any image format works** (`founder.jpg`, `founder.png`, `founder.jpeg`, or `founder.webp`). The site auto-detects whichever you add and shows it on the homepage "Meet our founder" section and the About page. Until then, a soft blue gradient placeholder shows — nothing looks broken.

After adding the photo, re-deploy (push to GitHub, or drag the `website` folder into Netlify).

## Notes
- All rate figures are illustrative placeholders — replace with your real, current rates before launch,
  or wire the rate card to a live feed.
- Calculator results are estimates, not loan offers (disclaimer included in the footer).
- Replace `YOUR-SITE.netlify.app` in `robots.txt` and `sitemap.xml` with your real domain after launch.
