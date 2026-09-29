# sampler-composition

## Intent

See the "Figure brief: sampler-composition" comment in `_posts/2026-09-27-noise.md`.

## Content and evidence

Conceptual diagram of Z = g(f(X,U),V). Conventions shared with text-vs-diffusion: square-cornered ink boxes are deterministic; accent arrows from above are noise.

## Figure-specific choices

Schematic recipe.

## Review and handoff

Final build: `fig-generator/.build/sampler-composition-v1`. Desktop and 340px PNGs inspected; labels legible, no overlaps, no warnings. Published to `assets/images/figures/sampler-composition/`.

## Restyle (2026-09-27, newsprint)

Black-and-white newsprint theme: FIG. 6 masthead and foot rule, JetBrains Mono
labels, dashed ink H box. Noise (U, V) now marked by `figure emph arrow` (heavy)
instead of accent color; shared convention with text-vs-diffusion. Final build:
`.build/sampler-composition-news3`; desktop and 340px PNGs inspected, no warnings.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/sampler-composition-min2`, inspected.
