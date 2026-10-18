# Legacy one-shot scripts

These ran once, in order, to turn the captured Uber homepage into the RESET homepage. Their output is now
committed in `public/`, and they are kept only as a record of how it was made. They are not part of the build
and should not be re-run: their inputs (the original capture) are no longer in this repo.

- `brand_css.py`: Uber's stylesheet recoloured to the RESET monochrome ramp, fonts swapped -> `public/assets/css/base.css`
- `rewrite_copy.py`: first copy and image pass over `index.html`
- `copy_v2.py`: second copy pass (Uber-style voice)
- `motion_markup.py`: hooks for `assets/js/motion.js`
