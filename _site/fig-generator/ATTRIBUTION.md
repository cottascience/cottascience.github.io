# Attribution and dependencies

The initial design was informed by [Foadsf/vintage-latex](https://github.com/Foadsf/vintage-latex)
at revision `559011918849a3da819912a7c26493071d542df5`: standalone scientific
illustrations, controlled typography, fixed texture seeds, and a compilation
workflow. The CLI, shared theme, and starter drawings in this folder were written
for this blog; no upstream example or build script is vendored here.

Vintage-latex licenses its source, prose, and generated examples under
[CC BY-SA 4.0](https://github.com/Foadsf/vintage-latex/blob/559011918849a3da819912a7c26493071d542df5/LICENSE).
If you later copy or adapt those examples, preserve the required attribution,
license link, change notice, and share-alike terms for the adaptation. A mention
of upstream inspiration does not substitute for those requirements.

The optional engraved recipe calls [fiziko](https://github.com/jemmybutton/fiziko),
Sergey Slyusarev's MetaPost illustration library. It is fetched separately:

- Revision: `54a63dba8e6700a5e70d3508838edebcbf0f45fe`.
- SHA-256 of `fiziko.mp`: `55c7b8053e62516e5091713b31d4cc21707901f9ffa5e456afbf6fef2b39e2b5`.
- Upstream license: GPL-3.0-or-later, as declared in its source header.
- The install command downloads the upstream `LICENSE.md` alongside the library.

Fiziko stays in the ignored local cache. Render records identify its revision and
checksum. If redistributing library code or adapting third-party illustrations,
retain the applicable license materials and credit the source of the drawing.

LuaLaTeX, TikZ/pgfplots, luamplib, Poppler, librsvg, and fonts are external tools
under their respective licenses. No font files or external binaries are included.
