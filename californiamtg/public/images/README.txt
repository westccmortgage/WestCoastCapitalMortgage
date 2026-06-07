California Mortgage — hero poster / fallback image
==================================================

A generated on-brand poster already ships here:

  california_mortgage_poster.png   (1200x630 warm gradient + roofline mark)

Replace it with a cinematic California still (1920x1080, < 300 KB) any time —
keep the same filename. It is also used as the Open Graph / Twitter share image.

The hero <video> in ../../index.html already points its poster at this path:

  poster="public/images/california_mortgage_poster.png"

This image is shown:
  - before the background video starts,
  - on mobile devices (where the video is intentionally not loaded),
  - on data-saver / slow connections and with reduced-motion,
  - if the video file is missing.

Until this file is added, the hero falls back to a premium warm CSS background
(sandy / stone gradient with soft bronze ambient lighting) — so there is never
empty space.
