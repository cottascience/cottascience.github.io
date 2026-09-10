# Figure style

Figures should read as part of the article: clear geometry, restrained color,
serif labels, and enough space to understand the relationship being shown.
Vintage engraving is an optional illustration technique.

## Shared visual language

The defaults come from this blog's `assets/main.scss`:

| Role | Value | Use |
| --- | --- | --- |
| Paper | `#FFFDFA` | Plot interiors and label masks |
| Ink | `#2A2620` | Text, outlines, primary structure |
| Muted | `#5A5F7A` | Secondary notes and supporting marks |
| Accent | `#B5563A` | A highlighted series or result |
| Grid | `#DED8CF` | Quiet reference lines |

Keep the outer background transparent to blend with the page. PNG previews use
the page's paper color. Avoid simulating aged paper inside each figure: the blog
already supplies its background treatment.

Default labels use TeX Gyre Pagella with TeX Gyre Pagella Math. These are distributed
with TeX and provide a consistent serif companion to the site's Lora body text and
Fraunces headings. To match body labels more closely, set `font` to `Lora` when
that font is installed. Missing fonts should fail rather than silently substitute.
Math continues to use TeX Gyre Pagella Math. Font files are not bundled here.

Use the shared styles instead of repeating hard-coded values in each source:

- `blogfigure`: `figure box`, `figure arrow`, `figure note`, `figure hatch`.
- `blogplot`: `blog axis`, `blog primary`, `blog secondary`.
- `blogengraving`: fiziko setup, consistent light, ink, and seeded textures.

## Sizing and layout

The normal article width is 680 CSS pixels. Start with a drawing roughly 13–15cm
wide. The shared theme uses 16pt labels and 14pt notes/ticks; check the rendered
result, since cropping changes the scale.
Use larger labels or fewer panels when mobile text becomes difficult to read.
The 340px preview represents the figure space inside a narrow phone viewport.
Changing `width` scales the entire figure; it does not reflow the TeX layout.

Keep captions and explanatory paragraphs in HTML. Use `standalone` with an 8–10pt
border to crop to the figure while leaving room for labels and arrowheads. Avoid
page titles, page numbers, large paper margins, and decorative frames. Do not hide
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
