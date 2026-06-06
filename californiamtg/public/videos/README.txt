California Mortgage — hero background video
===========================================

ACTIVE FILE (currently used by the hero):
  california_mortgage_hero_my_pick_24s.mp4

How it is wired
---------------
- index.html references it via the hero <video data-src="..."> attribute:
    public/videos/california_mortgage_hero_my_pick_24s.mp4
- script.js attaches the <source> and autoplays (muted, looped, playsinline,
  no controls, object-fit: cover) only on screens >= 768px with a normal
  connection and no reduced-motion preference.
- On mobile, data-saver, or prefers-reduced-motion, the video element is
  removed and the hero falls back to the poster image + warm gradient.

Poster / fallback image (add this file)
---------------------------------------
  ../images/california_mortgage_poster.jpg

Notes
-----
- Keep replacements reasonably small for performance (this clip is ~15 MB).
- To swap the video, replace the .mp4 above (keep the name) or update the
  data-src in index.html.
