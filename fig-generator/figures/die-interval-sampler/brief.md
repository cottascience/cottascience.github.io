# Sampling a loaded die from a uniform draw

## Intent

Probability of a face equals the length of its piece of [0,1); a uniform draw at 0.42 lands in piece 4.

## Content and evidence

Conceptual diagram from _posts/2026-09-27-noise.md (figure brief `die-interval-sampler`). Die
probabilities (0.05, 0.10, 0.15, 0.20, 0.20, 0.30) and, for x1, their reversal.
Segment widths are exact cumulative sums on a 13cm interval.

## Figure-specific choices

Schematic recipe. Segments alternate paper / light grid hatch; same styling and
x-scale shared between die-interval-sampler and context-moves-partition. Accent
reserved for the draw u = 0.42 and its output.

## Review and handoff

Final build: `fig-generator/.build/die-interval-sampler-v2`. Desktop and mobile PNGs
inspected: labels do not collide; values match the post. Mobile tick labels are
small but legible. Published to `assets/images/figures/die-interval-sampler/`.

### Newsprint restyle (2026-09-27)

Restyled to the black-and-white newspaper plate look: masthead "FIG. 1 / THE
LOADED DIE", halftone for alternate segments, heavy rule at u = 0.42, solid-black
output box, foot rule, mono math. Final build `.build/die-interval-sampler-news6`;
desktop and 340px PNGs inspected, label "4" nudged left of the draw line.
Republished over the previous assets at the same id.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/die-interval-sampler-min2`, inspected.
