# Usage

For generation through an agent, point to [SCAFFOLD.md](SCAFFOLD.md) with a short
paragraph describing the figure. It defines the workflow and handoff; this file
is the command reference the agent uses to carry it out.

## Dependencies

Python 3.10 or newer, a recent TeX Live/MacTeX distribution, Poppler, and librsvg.
There are no pip dependencies. `rtk proxy` in the examples follows this repo's
command convention; outside this repo, the underlying `python3` command works
without RTK.

The installer supports macOS with Homebrew, Debian 12+, and Ubuntu 22.04+ (also
under WSL). It installs missing tools, fetches and verifies the pinned fiziko
dependency, then runs `doctor`. On a machine with an existing working installation,
it reuses the tools and verified fiziko cache.

```sh
rtk proxy bash fig-generator/install.sh --dry-run
rtk proxy bash fig-generator/install.sh
rtk proxy bash fig-generator/install.sh --check
```

For plots and schematics only, use `--no-fiziko` with any of those commands. The
script locates its own directory, so it can be invoked from any working directory.
Run it as your regular user: apt uses sudo when necessary, and the MacTeX installer
may request administrator access. TeX is a substantial download on a new machine.
Homebrew itself must already be installed on macOS; see [brew.sh](https://brew.sh).
Native Windows and Linux package managers other than apt are not automated.

The installer does not replace an incomplete existing MacTeX/BasicTeX installation.
Use its package manager to add the packages reported by `doctor`: `standalone`,
`fontspec`, `unicode-math`, `pgf`, `pgfplots`, `tex-gyre`, and `tex-gyre-math`, plus
`luamplib` for engravings. Updating a TeX installation may require administrator
access. Rerun the installer after completing that setup.

For manual setup on macOS:

```sh
rtk proxy brew install --cask mactex-no-gui
rtk proxy brew install python poppler librsvg
```

Restart your shell after installing MacTeX so `/Library/TeX/texbin` is on `PATH`.
On Debian/Ubuntu:

```sh
rtk proxy sudo apt-get update
rtk proxy sudo apt-get install python3 ca-certificates texlive-luatex texlive-latex-extra texlive-pictures texlive-fonts-recommended texlive-metapost tex-gyre fonts-texgyre-math poppler-utils librsvg2-bin
```

Run `doctor` to check executable and package availability:

```sh
rtk proxy python3 fig-generator/figure.py doctor
rtk proxy python3 fig-generator/figure.py list
```

`doctor` exits nonzero if the base toolchain is incomplete. `engraved_ready` is a
separate result: plots and schematics do not need fiziko or luamplib. Availability
checks are followed by the real compatibility check when you render a recipe.

The SVG converter is Poppler's `pdftocairo`. This avoids relying on dvisvgm's
optional PDF backend: some installations require mutool or an older Ghostscript
even when the `dvisvgm` executable itself is present.

Package references: [MacTeX cask](https://formulae.brew.sh/cask/mactex-no-gui),
[librsvg](https://formulae.brew.sh/formula/librsvg), and
[Ubuntu MetaPost packages](https://packages.ubuntu.com/noble/texlive-metapost).

## Test commands

Check dependencies and run the contract tests (the latter do not require TeX):

```sh
rtk proxy bash fig-generator/install.sh --check
rtk proxy python3 -m unittest discover -s fig-generator/tests -v
```

Render all three recipes into a fresh directory so this test can be repeated:

```sh
figure_test_dir="$(rtk proxy mktemp -d /tmp/fig-generator-test.XXXXXX)"
rtk proxy python3 fig-generator/figure.py render fig-generator/templates/plot --output "${figure_test_dir:?Run the mktemp assignment first}/plot"
rtk proxy python3 fig-generator/figure.py render fig-generator/templates/schematic --output "${figure_test_dir:?Run the mktemp assignment first}/schematic"
rtk proxy python3 fig-generator/figure.py render fig-generator/templates/engraved --output "${figure_test_dir:?Run the mktemp assignment first}/engraved"
```

Each command returns its `preview.html` path. Open those files in your browser to
check desktop and mobile layouts. On macOS, for example:

```sh
rtk proxy open "${figure_test_dir:?Run the mktemp assignment first}/plot/preview.html"
```

These tests do not publish assets or change posts. The temporary render directory
is left available for inspection. If installed with `--no-fiziko`, skip the engraved
render and add `--no-fiziko` to the install check.

Run the assignment and render commands in the same terminal. If the variable is
unset or empty, `$figure_test_dir/plot` becomes `/plot`; the guarded expressions
above stop before invoking the renderer. For a single command without variables:

```sh
rtk proxy python3 fig-generator/figure.py render fig-generator/templates/plot --output fig-generator/.build/plot-test
```

Choose a different output name if `plot-test` already exists.

## Create and edit

```sh
rtk proxy python3 fig-generator/figure.py new schematic fig-generator/figures/encoder-overview
```

The destination must be new and its name must be a lowercase slug. That name
becomes the figure id. All commands accept paths relative to your current working
directory; the script finds its own templates and theme independently.

Edit the following files:

| File | Contents |
| --- | --- |
| `figure.tex` | Standalone figure source; use `blogfigure`, `blogplot`, or `blogengraving` |
| `figure.json` | Required description and data provenance; optional rendering settings |
| `data.csv` | Plot values; other local data files are also allowed |

Metadata fields:

| Field | Rule |
| --- | --- |
| `id` | Lowercase letters, digits, single separating hyphens; used in output paths |
| `title` | Nonempty plain text; SVG title and preview heading |
| `alt` | Nonempty plain text describing the content and relationship conveyed |
| `caption` | Nonempty plain text; exported into the Jekyll include |
| `data_kind` | `illustrative`, `measured`, or `diagram` |
| `data_source` | Nonempty description of the dataset, formula, or conceptual basis |
| `width` | Optional CSS-pixel width, 240–1360; default 680 |
| `seed` | Optional integer, 0–4095; default 1729 |
| `font` | Optional installed text-font family; default `TeX Gyre Pagella` |
| `requires` | Optional list; use `["fiziko"]` for engraved figures |

The starter metadata describes the starter illustration. Update it when changing
the source. Setting `data_kind` does not rewrite labels or validate scientific
claims: the author/agent must keep the data, drawing, alt text, and caption aligned.

Text and filenames in JSON are not interpreted as TeX. Put equations in the TeX
source. Metadata is plain text, HTML-escaped in the preview/include. Retain
attribution and licensing information in the caption or adjacent post text when
adapting a third-party figure.

## Render and review

```sh
rtk proxy python3 fig-generator/figure.py render fig-generator/figures/encoder-overview
```

Successful commands print JSON on stdout. Errors go to stderr with a nonzero exit
code. A render result contains `output`, `preview`, `include`, and `warnings`.

The default output is `fig-generator/.build/<id>/`. To iterate, choose a new output
directory; existing builds are preserved:

```sh
rtk proxy python3 fig-generator/figure.py render fig-generator/figures/encoder-overview --output fig-generator/.build/encoder-overview-v2
```

Each build contains:

- `<id>.svg`: web figure, with a responsive viewBox and outlined labels.
- `<id>.pdf`: cropped vector download with typeset text.
- `<id>.png`: rasterized from the SVG at twice the requested display width.
- `<id>-mobile.png`: SVG rasterized at up to 340 pixels wide.
- `preview.html`: actual SVG at article and mobile sizes, plus the caption.
- `embed.liquid`: ready-to-paste include for this blog.
- `render.json`: metadata, tool versions, dependency revision, checksums, warnings.
- `source/`, `theme/`, `settings.tex`: inputs used for this build.
- TeX and conversion logs for diagnosis.

Open `preview.html` directly in a browser. Inspect both PNGs when using an agent
with image-viewing tools. Check the plotted values and labels against the inputs.
The PDF is not a tagged accessible document; the HTML alt text and nearby prose
are the primary accessible explanation. Outlined SVG labels preserve appearance
but are not selectable text.

The timeout is 180 seconds **per external command**. Complex engravings can use
`--timeout 600`. LuaLaTeX runs twice for references. Multi-page output, missing
font characters, converter failures, and invalid metadata are errors. Overfull
boxes and large SVGs appear in the warnings. Empty SVGs are rejected; visual review
is still required to catch misplaced, invisible, or scientifically incorrect content.

Render only trusted TeX sources. Shell escape is disabled, but LuaLaTeX runs code;
this command is not a sandbox for untrusted documents.

## Optional fiziko illustrations

```sh
rtk proxy python3 fig-generator/figure.py install-fiziko
rtk proxy python3 fig-generator/figure.py new engraved fig-generator/figures/sphere-volumes
rtk proxy python3 fig-generator/figure.py render fig-generator/figures/sphere-volumes
```

Installation downloads only `fiziko.mp` and its license to `.cache/fiziko/`.
Rendering is offline. The dependency revision and source checksum are constants
in `figure.py`; installed TeX Live copies are deliberately not substituted for
the pinned version. See [ATTRIBUTION.md](ATTRIBUTION.md).

In `mplibcode`, reuse fiziko primitives and ordinary MetaPost geometry. Text
between `btex` and `etex` uses the document fonts. The shared style sets the ink,
stroke width, light direction, and seed. Avoid MetaPost variable names that shadow
built-ins such as `floor`. Inspect more complex textures at mobile size and watch
the resulting SVG file size.

## Publish reviewed assets

```sh
rtk proxy python3 fig-generator/figure.py publish fig-generator/.build/encoder-overview-v2
```

This verifies artifact checksums and copies SVG/PDF/PNG into this repository's
`assets/images/figures/<id>/`. It refuses to overwrite an existing destination.
For a revision of an already published figure, either choose a new id and update
the post's include, or explicitly replace the reviewed assets yourself.

Paste the returned include in a post. The include path is intended for the
published assets; it will not resolve on the site before that copy happens.
The `width` value is passed to the existing `figure.html` include as a CSS maximum.
To offer the PDF download, add a normal Markdown link beside the figure.

`publish` only copies local files; posting, committing, and deployment remain
separate actions. Commit the editable source folder along with the published
assets so future agents can regenerate them.
