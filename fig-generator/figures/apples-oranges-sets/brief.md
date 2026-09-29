# Apples and oranges as disjoint sets

## Intent

A 1970s science-magazine-cover take on "apples and oranges": two large sets of
fruit that share no element, A ∩ O = ∅.

## Content and evidence

Conceptual diagram. Set A holds apples, set O holds oranges; the circles do not
overlap. Fruit counts, sizes, and positions are decorative (seeded jitter), not data.

## Figure-specific choices

`engraved` recipe: the look is the point. Apples use fiziko line-hatched spheres
with stem and hatched leaf; oranges use stippled spheres so the two sets differ by
texture, not color. A heavy/thin masthead rule and headline give the newspaper
cover feel, an intentional exception to STYLE.md's no-decorative-frame rule, made
at the user's request.

## Review and handoff

Final build: `fig-generator/.build/apples-oranges-sets-v3`. Desktop and 340px PNGs
inspected: fruit stays inside both set boundaries, labels clear the circles,
headline and set labels legible on mobile (kicker text small but decorative).
v1 was too sparse; v2 fixed density and back-to-front overlap. Warning kept: SVG is
8.5 MB from the stipple/hatch strokes; prefer the PNG in the post.
Published locally to `assets/images/figures/apples-oranges-sets/`.
