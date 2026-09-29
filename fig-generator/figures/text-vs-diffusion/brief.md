# Text and diffusion share one skeleton

## Intent

Autoregressive text and diffusion are the same construction (deterministic steps plus independent noise) updating different states.

## Content and evidence

Token example from post ("sofa"); noise grids illustrative, seeded TikZ rnd blended with a Gaussian blob. Source: figure brief in `_posts/2026-09-27-noise.md`.

## Figure-specific choices

Schematic; square deterministic boxes and accent noise arrows from above, matching sampler-composition. Two steps per chain; dashed ε arrow notes DDIM.

## Review and handoff

Final build: `fig-generator/.build/text-vs-diffusion-v3`. Desktop and 340px mobile PNGs inspected: labels readable, no overlaps, values match brief. Mobile text is small but legible. Published to `assets/images/figures/text-vs-diffusion/`.

## Restyle (2026-09-27, newsprint)

Black-and-white newsprint theme: FIG. 7 masthead and foot rule, square state
boxes widened to 40mm for mono text, "sofa" bold instead of accent. Noise arrows
heavy (`figure emph arrow`), DDIM-optional ε arrow heavy dashed. Noise grids are
halftone dots (area ∝ density, seeded rnd), no gray levels. Final build:
`.build/text-vs-diffusion-news2`; desktop and 340px PNGs inspected, no warnings.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/text-vs-diffusion-min2`, inspected.
