# Context moves the partition

## Intent

Context shifts the boundaries; the same noise u=0.42 gives face 4 under x0 and face 2 under x1.

## Content and evidence

Conceptual diagram from _posts/2026-09-27-noise.md (figure brief `context-moves-partition`). Die
probabilities (0.05, 0.10, 0.15, 0.20, 0.20, 0.30) and, for x1, their reversal.
Segment widths are exact cumulative sums on a 13cm interval.

## Figure-specific choices

Schematic recipe. Segments alternate paper / light grid hatch; same styling and
x-scale shared between die-interval-sampler and context-moves-partition. Accent
reserved for the draw u = 0.42 and its output.

## Review and handoff

Final build: `fig-generator/.build/context-moves-partition-v1`. Desktop and mobile PNGs
inspected: labels do not collide; values match the post. Mobile tick labels are
small but legible. Published to `assets/images/figures/context-moves-partition/`.

## Restyle (2026-09-27)

Restyled to the black-and-white newsprint look (masthead, halftone fills, weight/solid-fill emphasis instead of accent color, mono labels). Content unchanged. Final build: `fig-generator/.build/context-moves-partition-news2`; desktop and 340px PNGs inspected, no warnings. Republished in place.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/context-moves-partition-min2`, inspected.
