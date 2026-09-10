# Working on blog figures

For figure creation or revision, use [SCAFFOLD.md](SCAFFOLD.md) as the task
workflow. A short user paragraph supplies the figure-specific details; infer
routine choices from the scaffold. Write the per-figure `brief.md` yourself using
[BRIEF.md](BRIEF.md), rather than asking the user to complete it.

Read `USAGE.md` and `STYLE.md` before generating a figure. Follow the enclosing
repository's command conventions, including the RTK prefix.

1. Choose a recipe with `figure.py list`. Use `new` to create editable sources
   under `fig-generator/figures/<id>/`; keep the starter templates reusable.
2. Update the drawing, data, and all description/provenance fields together. Do
   not present the starter's synthetic values as experimental results.
3. Use the shared theme and render through `figure.py`. Do not manually fabricate
   a successful render record or publish stale assets after a failed build.
4. Inspect the SVG/HTML preview and both PNG sizes. Check the image against the
   intended scientific claim and its data. Compilation alone is not review.
5. Report unresolved warnings or readability problems and revise the source.
6. When publishing is within the requested task, use `publish` for reviewed
   assets and the returned include for the post. Rendering by itself does not
   authorize posting, committing, or deploying.

Commands return JSON on success and exit nonzero on failure. Existing sources,
build directories, and published destinations are not overwritten. Use a new
`--output` directory when iterating. Keep the final editable source with the assets.

`install.sh` and `install-fiziko` use the network; rendering is offline. Treat the
TeX input as trusted executable code; the renderer is not an isolation boundary. Do not change dependency pins
without verifying the new source, checksum, license, and rendered examples.
