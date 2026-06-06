California Mortgage — hero background video
===========================================

Drop your cinematic California footage here:

  california-mortgage-hero.mp4    (H.264/MP4, ~6–12s loop, 1920x1080, muted)
  california-mortgage-hero.webm   (VP9/WebM, same loop — better compression)

Then open ../index.html and uncomment the two <source> lines inside the
<video class="hero-video"> tag in the HERO section:

  <source src="videos/california-mortgage-hero.webm" type="video/webm">
  <source src="videos/california-mortgage-hero.mp4"  type="video/mp4">

Notes
-----
- The video already has: autoplay muted loop playsinline preload="none".
- Poster / fallback: ../images/california-mortgage-poster.jpg
  (until that exists, assets/california-mortgage-poster.svg gradient is used).
- Keep files small (aim < 4–6 MB) for performance on mobile/slow connections.
- On mobile and slow connections the poster image is shown instead of the video.
