# Generate a blog figure from a short brief

This is the entry point for an agent creating or revising a figure. The user's
paragraph supplies the subject, intended takeaway, references, and any exceptions.
Use the workflow and defaults here for everything else. Carry out the work through
rendering, visual review, and the handoff below.

Example invocation:

> Use `fig-generator/SCAFFOLD.md` to draw protein sequence → frozen encoder →
> embedding → trainable prediction head. Emphasize that only the head is trained.

The paragraph is an instruction to the agent, not input that `figure.py` parses.
The agent turns it into drawing source and metadata, then calls the renderer.

## Read the shared context

Follow the enclosing agent instructions, then read:

- [STYLE.md](STYLE.md): visual defaults and scientific presentation.
- [USAGE.md](USAGE.md): setup, exact commands, metadata, and output conventions.
- [ATTRIBUTION.md](ATTRIBUTION.md) when adapting external drawings or code.
- Any post draft, data, or reference the user points to.

Keep shared decisions in those documents. A figure's brief should contain only
its specific intent, evidence, and departures from the defaults. Explicit user
instructions override this scaffold.

## Interpret the paragraph

Identify the one relationship, mechanism, or comparison the reader should learn.
Use the supplied post to resolve terminology, audience, and context. If no post is
provided, make the figure understandable on its own to a technical blog reader.

Choose the recipe and slug yourself. Use `schematic` for relationships and
pipelines, `plot` for numerical comparisons, and `engraved` when shaded objects
help explain the subject. Start with the corresponding source in `templates/`.
Adapt its drawing freely to the task; the example's content is not a requirement.

Infer routine presentation choices such as layout, short labels, and caption
wording. Do not require the user to fill out a form or approve a routine plan.
If a missing fact or dataset would change the scientific meaning, ask a focused
question and continue any independent preparation. Never substitute synthetic
values for requested measurements. Use illustrative values only when the brief
allows them, and identify them in the figure and caption.

## Defaults

| Decision | Default |
| --- | --- |
| Visual style | Shared theme in `theme/`, as specified by STYLE.md |
| Layout | One clear figure; split panels only when the comparison needs them |
| Size | 680px article width, reviewed at 340px mobile width |
| Source | `fig-generator/figures/<descriptive-slug>/` |
| Description | Agent-authored title, alt text, caption, and data provenance |
| Output | SVG, PDF, PNG, mobile PNG, and HTML preview |
| Local handoff | Reviewed blog assets and a ready-to-paste Jekyll include |
| Draft-only request | Keep the build for review; omit the asset copy |

The user can change any default in the same paragraph, for example “preview only,”
“use measured data from this CSV,” or “use engraving.”

## Build and refine

1. Check the toolchain using the commands in USAGE.md. If setup is needed, use
   `install.sh` within the user's permissions. Use the pinned fiziko installation
   for an engraved figure.
2. For a new figure, run `figure.py new` with the selected recipe and source path.
   For a revision, first read the existing source, metadata, and brief. Preserve
   author edits and follow the requested revision scope.
3. Write `brief.md` in the source directory using [BRIEF.md](BRIEF.md) as its
   structure. Fill it yourself from the paragraph and supplied context; keep it
   concise. Update it as figure-specific decisions become settled.
4. Implement the drawing and data inputs. Update every field in `figure.json`
   that describes the starter illustration. Keep the drawing, metadata, and
   brief consistent. Captions belong in HTML rather than inside the drawing.
5. Render with `figure.py render`. Use an explicit, fresh output path such as
   `fig-generator/.build/<slug>-v1`, then `-v2` for another iteration. Substitute
   concrete names; do not rely on shell variables from a previous terminal.
6. Inspect the actual rendered figure with the available image/browser tools.
   Review the SVG in `preview.html` when browser access is available and inspect
   the desktop and mobile PNGs. Check both meaning and presentation against
   STYLE.md. Fix issues in the source and render again.
7. Once reviewed, use `figure.py publish` to copy the finished assets into the
   blog's local asset directory, unless the user requested a draft only. This
   local copy is part of the default figure task. If that destination already
   exists, follow the revision guidance in USAGE.md and preserve existing assets;
   a new versioned figure id is suitable when replacement wasn't requested.

Keep a record of the final build path and actual review results in `brief.md`.
The renderer snapshots its inputs at build time; the live brief can record the
review afterwards without changing the rendered artifacts.

This workflow produces local files. Editing a post, committing, or deploying is
performed only when included in the user's task.

## Completion and handoff

A successful compilation is the start of review. Check that the figure conveys
the intended takeaway, its labels and values agree with the inputs, and it is
readable at both sizes. Resolve warnings or explain any that remain. If visual
inspection is unavailable, report that limitation, leave the build for review,
and do not describe it as visually verified or copy it as reviewed assets.

Return a concise handoff containing:

- A link to the final preview and editable source directory.
- The ready-to-paste Jekyll include and, when useful, the PDF link.
- Any assumption, unresolved issue, or review limitation that affects use.

For a draft-only handoff, label the include as intended for a later asset copy.
Do not repeat the scaffold or routine build logs in the final response.
