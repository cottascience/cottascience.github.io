# Figure style

Figures look like plates from an old black-and-white newspaper or 1970s science
magazine, typeset by someone who writes code: heavy/thin masthead rules, a
halftone and hatch fills instead of color, and engraved
texture where an object benefits from shading. It is the default look for every
recipe, not an option. `figures/apples-oranges-sets` is the reference plate.

## Shared visual language

Pure black and white, matching this blog's `assets/main.scss`:

| Role | Value | Use |
| --- | --- | --- |
| Paper | `#FFFFFF` | Fills, label masks, knocked-out text |
| Ink | `#111111` | Text, outlines, fills, emphasis |
| Muted | `#6B6B6B` | Secondary notes only |
| Grid | `#DDDDDD` | Quiet reference lines (dotted) |

There is no spot color. `accent` is an alias for ink so older sources compile.
Emphasis comes from weight and fill: `figure emph` (1.6pt stroke), `figure solid`
(black fill, white text), `figure emph arrow`. Distinguish regions by texture:
paper, `figure halftone` (dots), `figure hatch`, `figure crosshatch`, solid ink.
Never rely on gray levels alone.

Labels use JetBrains Mono (the site's code/meta face). Math uses TeX Gyre Pagella
Math. Boxes are square-cornered. Keep the outer background transparent; PNG
previews use white.

Plates are framed like newspaper figures, and minimal: `\FigureMasthead{x0}{x1}{y}{}{}`
draws the heavy/thin rule pair and `\FigureFootRule{x0}{x1}{y}` closes it. No text
in the frame: no "FIG. N", no titles or taglines. Inside the figure, keep only
labels the reader needs to decode it (variables, values, axes); no explanatory
sentences or slogans. The HTML caption and post carry the explanation.

Use the shared styles instead of repeating hard-coded values in each source:

- `blogfigure`: `figure box`, `figure arrow`, `figure emph`, `figure emph arrow`,
  `figure solid`, `figure halftone`, `figure hatch`, `figure crosshatch`,
  `figure note`, `\FigureMasthead`, `\FigureFootRule`.
- `blogplot`: `blog axis`, `blog primary` (heavy ink), `blog secondary` (dashed).
- `blogengraving`: fiziko setup, consistent light, ink, and seeded textures.

## Sizing and layout

Set `width` to about 0.95 × the PDF's width in points, so 16pt labels display near the 16px body text (drawings ~14cm wide land near 430px). Never stretch to the 680px column just because it's available. Start with a drawing roughly 13–15cm
wide. The shared theme uses 16pt labels and 14pt notes/ticks; check the rendered
result, since cropping changes the scale.
Use larger labels or fewer panels when mobile text becomes difficult to read.
The 340px preview represents the figure space inside a narrow phone viewport.
Changing `width` scales the entire figure; it does not reflow the TeX layout.

Keep captions and explanatory paragraphs in HTML. Use `standalone` with an 8–10pt
border to crop to the figure while leaving room for labels and arrowheads. Avoid
page numbers and large paper margins; the masthead and foot rules are the only frame. Do not hide
clipping or overlapping labels by simply shrinking the image.

## Plots and evidence

Use data files for measured series. Document their source and transformations in
`data_source`, with a companion file for longer notes if needed. Mark synthetic
data as illustrative in the figure and caption. Include units and explain any
normalization. Use a log axis only when justified by the comparison.

Do not smooth, perturb, or jitter measured coordinates for appearance. Represent
uncertainty only when supported by the data. Use line styles or symbols as well
as color when comparing series. Keep precise curves, ticks, and reference lines
geometrically exact; reserve hatching for illustrative surfaces.

## Engraving

Keep shading sparse enough to survive reduction. Use one consistent light source,
and set the random seed in metadata. Mask a label's background when it must cross
hatching. Do not equate a convincing drawing with a physically correct model:
verify geometry, scale, formulas, and assumptions separately.

## Before publishing

- Read all labels at article width and at 340px; enlarge or simplify as needed.
- Check arrow direction, units, clipping, contrast, and distinctions between series.
- Compare the rendered values and equations with the actual data/source.
- Write alt text conveying the relationship or trend, not just the chart title.
- Check the SVG as well as the PDF; PNG previews are generated from the SVG.
- Resolve build warnings and retain any required attribution in the post.

For dense diagrams, split the content across figures before adding more detail.
