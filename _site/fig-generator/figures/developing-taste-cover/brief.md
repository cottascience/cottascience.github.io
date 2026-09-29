# Developing taste

## Intent

Cover image for a future post on developing taste. Mood: good taste, abstract
art meets dark punk techies. Product is a single PNG, not an inline figure.

## Content and evidence

Abstract, no data. A 14x12 grid of one primitive, a round-capped bar. Left to
right, seeded tilt and length fall to zero, so bars shorten and align until they
collapse into identical dots, then one large chosen circle. Taste as pruning
noise. (v2 mixed lines/squares/arcs/crosses; read as sloppy, replaced in v3.)

## Figure-specific choices

Schematic recipe, inverted palette (paper on ink) as a deliberate cover
exception. No text. Post-processed with ImageMagick per USAGE.md photo effects
(grain, scanlines, glitch slices) to 1280x832, matching the noise.jpg cover.

## Review and handoff

Build: `fig-generator/.build/developing-taste-cover-v3` (width 1280, PNG 2560x1664).
Grit pass, from the repo root:

```sh
B=fig-generator/.build/developing-taste-cover-v3
magick $B/developing-taste-cover.png -resize 1280x832 -colorspace Gray \
 \( +clone -crop 1280x18+0+300 +repage -roll +46+0 \) -geometry +0+300 -composite \
 \( +clone -crop 1280x6+0+352 +repage -roll -22+0 \) -geometry +0+352 -composite \
 \( +clone -crop 1280x34+0+548 +repage -roll +90+0 \) -geometry +0+548 -composite +geometry \
 -blur 0x0.6 -attenuate 0.45 +noise Gaussian -colorspace Gray \
 \( -size 1x4 xc:white -fill '#555555' -draw 'point 0,3' -write mpr:dark +delete \) \
 \( +clone -tile mpr:dark -draw 'color 0,0 reset' \) -compose multiply -composite \
 \( -size 1x4 xc:'#1A1A1A' -fill black -draw 'point 0,3' -write mpr:lift +delete \) \
 \( +clone -tile mpr:lift -draw 'color 0,0 reset' \) -compose screen -composite -compose over \
 -background black -vignette 0x90-120-80 +level-colors '#111111','#FFFFFF' -strip $B/cover.png
```

Reviewed at 1280, 640 and 340px: bars-to-dots reads at all sizes, scanlines
visible across whites and the black field. SVG >1 MB warning ignored, since
only the PNG ships. Copied to `assets/images/developing-taste.png`; not in any post.
