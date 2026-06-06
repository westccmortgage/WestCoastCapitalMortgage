California Mortgage — hero poster / fallback image
==================================================

Add a cinematic California still here (recommended):

  california_mortgage_poster.jpg   (1920x1080, optimized JPG/WebP, < 300 KB)

The hero <video> in ../../index.html already points its poster at this path:

  poster="public/images/california_mortgage_poster.jpg"

This image is shown:
  - before the background video starts,
  - on mobile devices (where the video is intentionally not loaded),
  - on data-saver / slow connections and with reduced-motion,
  - if the video file is missing.

Until this file is added, the hero falls back to a premium warm CSS background
(sandy / stone gradient with soft bronze ambient lighting) — so there is never
empty space.
