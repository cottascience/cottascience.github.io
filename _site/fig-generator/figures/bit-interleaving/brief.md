# Splitting one uniform into two

## Intent

Show one ideal uniform splitting into two independent uniforms by dealing out its binary digits.

## Content and evidence

Post: `_posts/2026-09-27-noise.md`, section "How far does this go?". Top row U = 0.b1…b10…, odd boxes accent, even muted; arrows to U1 = 0.b1 b3 b5 … and U2 = 0.b2 b4 b6 …. Conceptual diagram, abstract digit labels.

## Figure-specific choices

`schematic` recipe. Ellipses on every row: the source is never a finite word.

## Review and handoff

Final build: `fig-generator/.build/bit-interleaving-v2`. Layout changed to columns kept in place (odd bits drop one row, even two) so no arrows cross. Checked desktop and 340px PNGs; subscripts small but legible at mobile. Published to `assets/images/figures/bit-interleaving/`.

## Restyle (2026-09-27)

Newsprint B&W: FIG. 4 masthead/foot rule; odd bits solid ink with white digit and heavy arrows, even bits paper with dashed arrows (replaces accent/muted). Final build `.build/bit-interleaving-news2`; desktop and 340px PNGs inspected, readable, no warnings.

### Minimal pass (2026-09-27)

Masthead text and prose notes removed; width set to 0.95 px/pt of the drawing so labels match body text. Final build `.build/bit-interleaving-min2`, inspected.
