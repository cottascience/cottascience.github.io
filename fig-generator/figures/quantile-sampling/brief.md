# Inverse-CDF sampling, continuous and discrete

## Intent

Show inverse-CDF sampling for a continuous law and for a discrete one, where a jump turns a band of heights into one outcome.

## Content and evidence

Post: `_posts/2026-09-27-noise.md`, section "From intervals to distributions". Left: exact $F(y)=y^2$, height 1/4 → y = 1/2, bands (1/4,1] and (1/2,1] shaded. Right: the die's staircase CDF (cumulative .05, .15, .30, .50, .70, 1), band [.30,.50) → face 4, u = 0.42 marked. Conceptual diagram with exact geometry.

## Figure-specific choices

`plot` recipe, two pgfplots axes sharing height. Closed dots at jump tops, open at bottoms. Sparse ticks.

## Review and handoff

Final build: `fig-generator/.build/quantile-sampling-v2`. Checked desktop and 340px PNGs: curve, staircase heights, open/closed dots, u=0.42 → face 4 correct; labels legible. Published to `assets/images/figures/quantile-sampling/`.

## Restyle (2026-09-27)

Restyled to the black-and-white newsprint look (masthead, halftone fills, weight/solid-fill emphasis instead of accent color, mono labels). Content unchanged. Final build: `fig-generator/.build/quantile-sampling-news2`; desktop and 340px PNGs inspected, no warnings. Republished in place.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/quantile-sampling-min2`, inspected.
