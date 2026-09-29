# From seed to sample

## Intent

Connect the finite PRNG back to the opening interval: seed → state → 16-point grid → sampling function → output; a boundary at 0.10 realizes 0.125.

## Content and evidence

Toy generator (5s+1) mod 16 from post; thumbnails are simplified callbacks to die-interval-sampler and box-muller-map. Source: figure brief in `_posts/2026-09-27-noise.md`.

## Figure-specific choices

Schematic pipeline with magnified inset over [0, 4/16]; accent only on boundary, points below it, and the 0.125 annotation.

## Review and handoff

Final build: `fig-generator/.build/seed-to-sample-v2`. Desktop and 340px mobile PNGs inspected: labels readable, no overlaps, values match brief. Mobile text is small but legible. Published to `assets/images/figures/seed-to-sample/`.

## Restyle (newsprint)

Restyled 2026-09-27 to the black-and-white newsprint look (STYLE.md): masthead + foot rule, mono labels, no spot color. Emphasis moved from accent color to texture/weight (crosshatch success regions and solid highlight plates in coupling; halftone band, solid dots, solid annotation plate in seed-to-sample). Final build: `fig-generator/.build/seed-to-sample-news2`; desktop and 340px PNGs inspected, no warnings. Math parentheses still come from Pagella Math (theme maps only digits and letters to mono).

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/seed-to-sample-min2`, inspected.
