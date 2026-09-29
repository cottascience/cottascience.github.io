# Same marginals, different couplings

## Intent

Show two samplers with identical marginals but opposite couplings: nested successes versus disjoint ones.

## Content and evidence

Exact intervals from the post (f nested, g disjoint); joint laws computed from interval overlaps. Conceptual diagram. Source: figure brief in `_posts/2026-09-27-noise.md`.

## Figure-specific choices

Schematic 2×2 strip grid on a common x-scale; accent = success, hatch = failure; tick labels only on bottom row to save space; joint tables at label size.

## Review and handoff

Final build: `fig-generator/.build/coupling-f-vs-g-v2`. Desktop and 340px mobile PNGs inspected: labels readable, no overlaps, values match brief. Mobile text is small but legible. Published to `assets/images/figures/coupling-f-vs-g/`.

## Restyle (newsprint)

Restyled 2026-09-27 to the black-and-white newsprint look (STYLE.md): masthead + foot rule, mono labels, no spot color. Emphasis moved from accent color to texture/weight (crosshatch success regions and solid highlight plates in coupling; halftone band, solid dots, solid annotation plate in seed-to-sample). Final build: `fig-generator/.build/coupling-f-vs-g-news2`; desktop and 340px PNGs inspected, no warnings. Math parentheses still come from Pagella Math (theme maps only digits and letters to mono).

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/coupling-f-vs-g-min2`, inspected.
