#!/usr/bin/env python3
"""Render standalone blog figures. Python 3.10+, standard library only."""

import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
FIZIKO_REVISION = "54a63dba8e6700a5e70d3508838edebcbf0f45fe"
FIZIKO_SHA256 = "55c7b8053e62516e5091713b31d4cc21707901f9ffa5e456afbf6fef2b39e2b5"
FIZIKO_DIR = ROOT / ".cache" / "fiziko" / FIZIKO_REVISION
TOOLS = ("lualatex", "kpsewhich", "pdftocairo", "rsvg-convert", "pdfinfo")
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


class FigureError(Exception):
    pass


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise FigureError(f"Cannot read {path}: {exc}") from exc


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_metadata(directory):
    meta = read_json(directory / "figure.json")
    if not isinstance(meta, dict):
        raise FigureError("figure.json must be a JSON object")
    for key in ("id", "title", "alt", "caption", "data_kind", "data_source"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise FigureError(f"figure.json requires a nonempty string: {key}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["id"]):
        raise FigureError("id must be a lowercase slug, such as learning-curve")
    if meta["data_kind"] not in ("illustrative", "measured", "diagram"):
        raise FigureError("data_kind must be illustrative, measured, or diagram")
    meta.setdefault("width", 680)
    meta.setdefault("seed", 1729)
    meta.setdefault("font", "TeX Gyre Pagella")
    meta.setdefault("requires", [])
    if type(meta["width"]) is not int or not 240 <= meta["width"] <= 1360:
        raise FigureError("width must be an integer between 240 and 1360 CSS pixels")
    if type(meta["seed"]) is not int or not 0 <= meta["seed"] < 4096:
        raise FigureError("seed must be an integer from 0 through 4095")
    if not isinstance(meta["font"], str) or not re.fullmatch(r"[A-Za-z0-9 -]+", meta["font"]):
        raise FigureError("font must be a font family name using letters, numbers, spaces, or hyphens")
    if not isinstance(meta["requires"], list) or any(x != "fiziko" for x in meta["requires"]):
        raise FigureError('requires may contain only "fiziko"')
    if not (directory / "figure.tex").is_file():
        raise FigureError(f"Missing {directory / 'figure.tex'}")
    return meta


def require_tools():
    missing = [name for name in TOOLS if not shutil.which(name)]
    if missing:
        raise FigureError(f"Missing tools: {', '.join(missing)}. See USAGE.md for installation.")


def fiziko_path():
    path = FIZIKO_DIR / "fiziko.mp"
    if not path.is_file() or sha256(path) != FIZIKO_SHA256:
        raise FigureError("Pinned fiziko is missing or changed. Run: python3 fig-generator/figure.py install-fiziko")
    return path


def run(command, directory, log, env, timeout):
    with log.open("w", encoding="utf-8") as stream:
        try:
            result = subprocess.run(command, cwd=directory, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            raise FigureError(f"{command[0]} exceeded {timeout}s. Log: {log}") from exc
    if result.returncode:
        tail = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-20:])
        raise FigureError(f"{command[0]} failed ({result.returncode}). Log: {log}\n{tail}")


def version(name):
    result = subprocess.run([name, "-v" if name in ("pdfinfo", "pdftocairo") else "--version"],
                            capture_output=True, text=True, timeout=15, check=False)
    lines = (result.stdout + result.stderr).splitlines()
    return lines[0] if lines else "unknown"


def decorate_svg(path, meta):
    tree = ET.parse(path)
    root = tree.getroot()
    if root.tag != f"{{{SVG_NS}}}svg":
        raise FigureError("Converter did not produce an SVG document")
    try:
        box = [float(value) for value in root.attrib["viewBox"].replace(",", " ").split()]
        valid = len(box) == 4 and all(math.isfinite(value) for value in box) and min(box[2:]) > 0
    except (KeyError, ValueError):
        valid = False
    if not valid:
        raise FigureError("SVG has no usable viewBox")
    drawable = {f"{{{SVG_NS}}}{name}" for name in ("path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "use", "image")}
    if not any(element.tag in drawable for element in root.iter()):
        raise FigureError("SVG is empty: the source did not produce any drawing")
    # Do not require the reader's browser to have the TeX fonts installed.
    if root.find(f".//{{{SVG_NS}}}text") is not None:
        raise FigureError("SVG still contains font-dependent text after outlining")
    root.set("width", str(meta["width"]))
    root.set("height", f"{meta['width'] * box[3] / box[2]:.2f}")
    root.set("role", "img")
    root.set("aria-labelledby", "figure-title figure-description")
    title = ET.Element(f"{{{SVG_NS}}}title", {"id": "figure-title"})
    title.text = meta["title"]
    description = ET.Element(f"{{{SVG_NS}}}desc", {"id": "figure-description"})
    description.text = meta["alt"]
    root.insert(0, title)
    root.insert(1, description)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return box


def embed(meta):
    # Entity-encoded values survive Liquid's quoted argument parsing and HTML output.
    def attribute(value):
        return html.escape(value, quote=True).replace("{", "&#123;").replace("}", "&#125;").replace("\n", " ")
    return ("{% include figure.html "
            f'src="/assets/images/figures/{meta["id"]}/{meta["id"]}.svg" '
            f'alt="{attribute(meta["alt"])}" '
            f'caption="{attribute(meta["caption"])}" width="{meta["width"]}px" %}}')


def preview_page(meta):
    title, alt, caption = (html.escape(meta[key], quote=True) for key in ("title", "alt", "caption"))
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — figure review</title>
<style>
body {{ background:#FFFDFA; color:#2A2620; font:16px/1.6 Georgia,serif; margin:24px; }}
section {{ max-width:{meta['width']}px; margin:32px 0; }}
figure {{ margin:0; }} img {{ display:block; width:100%; height:auto; }}
figcaption {{ color:#5A5F7A; font-style:italic; margin-top:12px; }}
.mobile {{ max-width:340px; }} a {{ color:#B5563A; }}
</style>
<h1>{title}</h1>
<p>Review the SVG at both sizes. Check labels, clipping, meaning, and data against the source.</p>
<section><h2>Article width</h2><figure><img src="{meta['id']}.svg" alt="{alt}"><figcaption>{caption}</figcaption></figure></section>
<section class="mobile"><h2>Mobile width</h2><figure><img src="{meta['id']}.svg" alt="{alt}"><figcaption>{caption}</figcaption></figure></section>
<p><a href="{meta['id']}.pdf">PDF</a> · <a href="{meta['id']}.png">PNG</a> · <a href="render.json">Build record</a></p>
</html>
"""


def render(args):
    source = args.source.resolve()
    meta = validate_metadata(source)
    require_tools()
    dependency = fiziko_path() if "fiziko" in meta["requires"] else None
    output = (args.output or ROOT / ".build" / meta["id"]).resolve()
    if output.parent == Path(output.anchor):
        raise FigureError(
            f"Output points directly under the filesystem root: {output}. "
            "A shell variable in --output may be unset. "
            "Use an explicit path such as --output fig-generator/.build/plot-test."
        )
    if output == source or source in output.parents or output in source.parents:
        raise FigureError("Output and source directories must be separate, without nesting")
    if output.exists():
        raise FigureError(f"Output already exists: {output}. Choose a fresh --output directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    # A failed build keeps its logs but never looks like a completed output directory.
    work = Path(tempfile.mkdtemp(prefix=f".{meta['id']}-", dir=output.parent))
    try:
        inputs = work / "source"
        shutil.copytree(source, inputs)
        shutil.copytree(ROOT / "theme", work / "theme")
        (work / "settings.tex").write_text(
            f"\\newcommand{{\\FigureFont}}{{{meta['font']}}}\n"
            f"\\newcommand{{\\FigureSeed}}{{{meta['seed']}}}\n", encoding="utf-8")
        env = os.environ.copy()
        cache = ROOT / ".cache" / "tex"
        cache.mkdir(parents=True, exist_ok=True)
        env["TEXMFVAR"] = str(cache)
        env["TEXMFCACHE"] = str(cache)
        env["TEXINPUTS"] = os.pathsep.join((str(work / "theme"), str(work), ""))
        env["MPINPUTS"] = os.pathsep.join((str(dependency.parent), "")) if dependency else os.pathsep
        env["SOURCE_DATE_EPOCH"] = "946684800"
        env["FORCE_SOURCE_DATE"] = "1"
        env["TZ"] = "UTC"
        env["LC_ALL"] = "C"
        for pass_number in (1, 2):
            run(["lualatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", f"-jobname={meta['id']}", f"-output-directory={work}", "figure.tex"],
                inputs, work / f"latex-{pass_number}.log", env, args.timeout)
        pdf = work / f"{meta['id']}.pdf"
        run(["pdfinfo", str(pdf)], work, work / "pdfinfo.log", env, args.timeout)
        if not re.search(r"^Pages:\s+1\s*$", (work / "pdfinfo.log").read_text(), re.MULTILINE):
            raise FigureError("Expected exactly one cropped PDF page")
        svg = work / f"{meta['id']}.svg"
        run(["pdftocairo", "-svg", str(pdf), str(svg)],
            work, work / "svg.log", env, args.timeout)
        box = decorate_svg(svg, meta)
        for suffix, width in (("", meta["width"] * 2), ("-mobile", min(meta["width"], 340))):
            run(["rsvg-convert", "--width", str(width), "--keep-aspect-ratio",
                 "--background-color", "#FFFDFA", "--output", str(work / f"{meta['id']}{suffix}.png"), str(svg)],
                work, work / f"png{suffix}.log", env, args.timeout)
        tex_log = (work / f"{meta['id']}.log").read_text(encoding="utf-8", errors="replace")
        if "Missing character:" in tex_log:
            raise FigureError("The selected font is missing a character. Check the TeX log.")
        warnings = [line for line in tex_log.splitlines() if re.search(r"Overfull|Missing character:|LaTeX Warning:", line)]
        if svg.stat().st_size > 1_000_000:
            warnings.append("SVG exceeds 1 MB; consider simplifying hatching or using the PNG.")
        record = {
            "metadata": meta,
            "tools": {name: version(name) for name in TOOLS if name != "kpsewhich"},
            "fiziko": {"revision": FIZIKO_REVISION, "sha256": FIZIKO_SHA256} if dependency else None,
            "inputs": {str(path.relative_to(work)): sha256(path)
                       for folder in (inputs, work / "theme") for path in sorted(folder.rglob("*")) if path.is_file()},
            "renderer_sha256": sha256(Path(__file__)),
            "viewBox": box,
            "warnings": warnings,
            "include": embed(meta),
            "outputs": {name: sha256(work / name) for name in (
                f"{meta['id']}.svg", f"{meta['id']}.pdf", f"{meta['id']}.png", f"{meta['id']}-mobile.png")},
        }
        write_json(work / "render.json", record)
        (work / "embed.liquid").write_text(record["include"] + "\n", encoding="utf-8")
        (work / "preview.html").write_text(preview_page(meta), encoding="utf-8")
        work.rename(output)
    except (FigureError, OSError, ET.ParseError, subprocess.TimeoutExpired) as exc:
        raise FigureError(f"{exc}\nIncomplete build retained at: {work}") from exc
    return {"output": str(output), "preview": str(output / "preview.html"),
            "include": record["include"], "warnings": warnings}


def new(args):
    destination = args.destination.resolve()
    if destination.exists():
        raise FigureError(f"Destination already exists: {destination}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", destination.name):
        raise FigureError("Destination folder name must be a lowercase slug")
    shutil.copytree(TEMPLATES / args.recipe, destination)
    meta = read_json(destination / "figure.json")
    meta["id"] = destination.name
    write_json(destination / "figure.json", meta)
    return {"source": str(destination), "next": "Edit figure.json, figure.tex, and any data files; then render."}


def install_fiziko(args):
    FIZIKO_DIR.mkdir(parents=True, exist_ok=True)
    base = f"https://raw.githubusercontent.com/jemmybutton/fiziko/{FIZIKO_REVISION}/"
    for name in ("fiziko.mp", "LICENSE.md"):
        with urllib.request.urlopen(base + name, timeout=30) as response:
            content = response.read()
        if name == "fiziko.mp" and hashlib.sha256(content).hexdigest() != FIZIKO_SHA256:
            raise FigureError("Downloaded fiziko does not match the pinned checksum")
        (FIZIKO_DIR / name).write_bytes(content)
    return {"fiziko": str(fiziko_path()), "revision": FIZIKO_REVISION}


def doctor(args):
    paths = {name: shutil.which(name) for name in TOOLS}
    packages = {}
    if paths["kpsewhich"]:
        for name in ("standalone.cls", "fontspec.sty", "unicode-math.sty", "tikz.sty", "pgfplots.sty",
                     "texgyrepagella-regular.otf", "texgyrepagella-math.otf"):
            result = subprocess.run(["kpsewhich", name], capture_output=True, text=True, timeout=15, check=False)
            packages[name] = result.stdout.strip() or None
    try:
        fiziko = str(fiziko_path())
    except FigureError:
        fiziko = None
    luamplib = None
    if paths["kpsewhich"]:
        luamplib = subprocess.run(["kpsewhich", "luamplib.sty"], capture_output=True,
                                 text=True, timeout=15, check=False).stdout.strip() or None
    ready = all(paths.values()) and all(packages.values())
    print(json.dumps({"ready": ready, "tools": paths, "tex_packages": packages,
                      "pinned_fiziko": fiziko, "luamplib": luamplib,
                      "engraved_ready": ready and fiziko is not None and luamplib is not None}, indent=2))
    return 0 if ready else 1


def publish(args):
    build = args.build.resolve()
    record = read_json(build / "render.json")
    meta = record["metadata"]
    # Revalidate before using metadata as a filesystem or Liquid path.
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["id"]):
        raise FigureError("Invalid figure id in build record")
    names = [f"{meta['id']}{extension}" for extension in (".svg", ".pdf", ".png")]
    for name in names:
        if sha256(build / name) != record["outputs"].get(name):
            raise FigureError(f"Artifact changed since rendering: {name}. Render again before publishing.")
    destination = ROOT.parent / "assets" / "images" / "figures" / meta["id"]
    if destination.exists():
        raise FigureError(f"Published destination already exists: {destination}. Use a new id or update the assets explicitly.")
    destination.mkdir(parents=True)
    for name in names:
        shutil.copy2(build / name, destination / name)
    return {"assets": str(destination), "include": embed(meta)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check the local toolchain; JSON output, nonzero if incomplete")
    sub.add_parser("list", help="List starter recipes")
    sub.add_parser("install-fiziko", help="Download the pinned optional fiziko source and license")
    create = sub.add_parser("new", help="Copy a starter recipe into a new source directory")
    create.add_argument("recipe", choices=sorted(path.name for path in TEMPLATES.iterdir() if path.is_dir()))
    create.add_argument("destination", type=Path)
    build = sub.add_parser("render", help="Render a source folder into a fresh build directory")
    build.add_argument("source", type=Path)
    build.add_argument("--output", type=Path, help="Default: fig-generator/.build/<id>; must not exist")
    build.add_argument("--timeout", type=int, default=180, help="Seconds per renderer invocation (default: 180)")
    export = sub.add_parser("publish", help="Copy reviewed SVG/PDF/PNG into this blog's assets; does not deploy")
    export.add_argument("build", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            return doctor(args)
        if args.command == "list":
            result = {path.name: read_json(path / "figure.json")["title"]
                      for path in sorted(TEMPLATES.iterdir()) if path.is_dir()}
        else:
            if args.command == "render" and args.timeout <= 0:
                raise FigureError("--timeout must be positive")
            result = {"new": new, "render": render, "install-fiziko": install_fiziko, "publish": publish}[args.command](args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (FigureError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"figure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
