# Blog figure generator

Create reproducible, editable scientific figures for this Jekyll blog using a small
Python CLI and standalone LuaLaTeX recipes. The CLI uses only Python's standard
library; TeX and image conversion run as local command-line tools.

The three starter recipes are:

| Recipe | Use | Source |
| --- | --- | --- |
| `plot` | Data-driven curves with axes and annotations | pgfplots + CSV |
| `schematic` | Labeled components, equations, and information flow | TikZ |
| `engraved` | Shaded physical objects and scientific illustrations | fiziko through luamplib |

Read [USAGE.md](USAGE.md) for setup and commands, [STYLE.md](STYLE.md) for visual
and scientific conventions, and [ATTRIBUTION.md](ATTRIBUTION.md) for provenance.
Agents should also read [AGENTS.md](AGENTS.md).

## Ask an agent

Point the agent to [SCAFFOLD.md](SCAFFOLD.md) and write only the figure-specific
content. For example:

> Use `fig-generator/SCAFFOLD.md` to draw protein sequence → frozen encoder →
> embedding → trainable prediction head. Emphasize that only the head is trained.

The scaffold supplies recipe selection, shared style, source organization,
metadata, rendering, visual review, and the local asset handoff. Add a post or
data path when relevant, or an exception such as “preview only.” The agent writes
a short `brief.md` alongside the source using [BRIEF.md](BRIEF.md); you do not
need to repeat the workflow or fill out that template.

## Quick start

Run from the blog repository root:

```sh
rtk proxy bash fig-generator/install.sh
rtk proxy python3 fig-generator/figure.py doctor
rtk proxy python3 fig-generator/figure.py new plot fig-generator/figures/learning-curve
# Edit the new folder's figure.json, figure.tex, and data.csv.
rtk proxy python3 fig-generator/figure.py render fig-generator/figures/learning-curve
```

Open the `preview.html` path returned by the renderer. It displays the actual SVG
at article and mobile widths. After reviewing the figure:

```sh
rtk proxy python3 fig-generator/figure.py publish fig-generator/.build/learning-curve
```

`publish` copies the SVG, PDF, and PNG to `assets/images/figures/learning-curve/`
and returns an include for the blog's existing `figure.html`. It does not edit a
post, commit, or deploy the site. Rendering alone writes only build/cache files.

## How it works

```text
figure.tex + data + figure.json + shared theme
                     |
                 LuaLaTeX
                     |
              one cropped PDF
                     |
                 pdftocairo
                     |
            SVG with outlined labels
                     |
                rsvg-convert
                     |
       full-resolution and mobile PNGs
```

Each completed build includes the source and theme snapshots, renderer/tool
fingerprints, output checksums, diagnostics, HTML preview, and Jekyll include.
Failed builds retain logs in a separate temporary directory and exit nonzero.
The renderer never silently skips a requested recipe.

Fiziko is optional, fetched explicitly, and verified against a pinned checksum.
The TeX distribution and fonts are supplied by your machine; their versions and
the requested font are recorded, but the environment is not a locked container.
Fixed seeds and dates reduce rebuild variation; bit-for-bit identity across TeX
or font versions is not promised.

## Repository integration

Keep editable sources under `fig-generator/figures/<id>/`. Commit those sources,
the shared theme, and reviewed assets. `.build/` and `.cache/` are ignored by Git.
There is no new dependency in the Jekyll deployment workflow.

Jekyll copies ordinary directories by default. If you want to serve only the
published assets, add `fig-generator/` to the root `_config.yml` `exclude` list.
This tool does not change that configuration automatically.

Run the CLI contract tests with:

```sh
rtk proxy python3 -m unittest discover -s fig-generator/tests -v
```
