Avatar / "Financial Navigator" tutorial videos
==============================================

Drop clip files here. They are served from the site root, e.g.:
  /assets/video/avatar/intro.mp4

Naming used by the tutorial (assets/js/tutorial.js -> STEPS):
  intro.mp4            step 1  (ZIP / welcome — "first script / ознакомление")
  step-county.mp4      step 2  (county loan limit)
  step-value.mp4       step 3  (home price / value)
  step-purpose.mp4     step 4  (loan purpose)
  step-down.mp4        step 5  (down payment)
  step-fico.mp4        step 6  (credit score)
  step-income-type.mp4 step 7  (income type)
  step-income.mp4      step 8  (yearly income)
  step-result.mp4      step 9  (conforming vs jumbo)
  step-payment.mp4     step 10 (payment strategy)
  step-buydown.mp4     step 11 (buydown / points)
  step-io.mp4          step 12 (interest only)
  step-final.mp4       step 13 (final review)

Recommended:
  - Format: .mp4 (H.264 + AAC). Optionally add a matching .webm.
  - Width ~480-640px (the avatar box is small).
  - Autoplays muted; a mute/unmute button appears if the clip has sound.

To attach a clip to a step, set "videoSrc" on that step in
assets/js/tutorial.js, for example:
  videoSrc: "/assets/video/avatar/intro.mp4"
