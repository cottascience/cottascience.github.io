# box-muller-map

## Intent

See the "Figure brief: box-muller-map" comment in `_posts/2026-09-27-noise.md`.

## Content and evidence

Conceptual diagram with exact geometry: radii sqrt(-2 log u) for u = 3/4, 1/2, 1/4 (0.7585, 1.1774, 1.6651), 1.4 cm per unit; 45° wedges. Cells A = (0,1/8]×(3/4,1] and B = (0,1/8]×(1/4,1/2].

## Figure-specific choices

Schematic recipe.

## Review and handoff

Final build: `fig-generator/.build/box-muller-map-v3`. Desktop and 340px PNGs inspected; labels legible, no overlaps, no warnings. Published to `assets/images/figures/box-muller-map/`.

## Restyle (2026-09-27)

Newsprint B&W: FIG. 5 masthead/foot rule; cells A/B crosshatched with 1.6pt outlines and paper-masked labels (replaces accent tint); grid in muted/ink, outer region dotted. Radii unchanged (exact). Final build `.build/box-muller-map-news3`; desktop and 340px PNGs inspected, no warnings.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/box-muller-map-min4`, inspected.
