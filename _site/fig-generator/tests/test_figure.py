"""CLI contracts that protect source files and published assets; no TeX required."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import figure


class FigureContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "my-plot"
        figure.new(SimpleNamespace(recipe="plot", destination=self.source))

    def test_new_preserves_existing_work(self):
        data = self.source / "data.csv"
        data.write_text("user's work\n")
        with self.assertRaises(figure.FigureError):
            figure.new(SimpleNamespace(recipe="plot", destination=self.source))
        self.assertEqual(data.read_text(), "user's work\n")

    def test_metadata_rejects_paths_and_mistyped_dimensions(self):
        meta = figure.read_json(self.source / "figure.json")
        for field, value in (("id", "../escape"), ("width", True), ("width", 0),
                             ("seed", 4096), ("requires", "fiziko"), ("alt", "")):
            with self.subTest(field=field, value=value):
                figure.write_json(self.source / "figure.json", {**meta, field: value})
                with self.assertRaises(figure.FigureError):
                    figure.validate_metadata(self.source)

    def test_include_escapes_html_and_liquid_delimiters(self):
        meta = figure.validate_metadata(self.source)
        meta["caption"] = 'A "quote" <script> & {% include bad %}'
        result = figure.embed(meta)
        self.assertIn("&quot;quote&quot;", result)
        self.assertNotIn("<script>", result)
        self.assertNotIn("{% include bad", result)
        self.assertIn('width="680px"', result)

    def test_missing_pinned_dependency_is_an_error(self):
        with patch.object(figure, "FIZIKO_DIR", self.root / "missing"):
            with self.assertRaisesRegex(figure.FigureError, "install-fiziko"):
                figure.fiziko_path()

    def test_empty_drawing_is_rejected_even_with_valid_dimensions(self):
        svg = self.root / "empty.svg"
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><g/></svg>')
        with self.assertRaisesRegex(figure.FigureError, "SVG is empty"):
            figure.decorate_svg(svg, figure.validate_metadata(self.source))

    def test_failed_compile_retains_logs_without_completed_output(self):
        output = self.root / "build"

        def fail_compile(command, directory, log, env, timeout):
            log.write_text("Undefined control sequence")
            raise figure.FigureError("compiler failed")

        with patch.object(figure, "require_tools"), patch.object(figure, "run", side_effect=fail_compile):
            with self.assertRaisesRegex(figure.FigureError, "Incomplete build retained"):
                figure.render(SimpleNamespace(source=self.source, output=output, timeout=10))
        self.assertFalse(output.exists())
        self.assertEqual(len(list(self.root.glob(".my-plot-*/latex-1.log"))), 1)
        self.assertTrue((self.source / "figure.tex").is_file())

    def test_existing_build_is_not_overwritten(self):
        output = self.root / "build"
        output.mkdir()
        sentinel = output / "keep.txt"
        sentinel.write_text("keep")
        with patch.object(figure, "require_tools"):
            with self.assertRaisesRegex(figure.FigureError, "already exists"):
                figure.render(SimpleNamespace(source=self.source, output=output, timeout=10))
        self.assertEqual(sentinel.read_text(), "keep")

    def test_empty_shell_variable_cannot_send_output_to_filesystem_root(self):
        with patch.object(figure, "require_tools"), patch.object(figure.tempfile, "mkdtemp") as make_temp:
            with self.assertRaisesRegex(figure.FigureError, "shell variable.*unset"):
                figure.render(SimpleNamespace(source=self.source, output=Path("/plot"), timeout=10))
        make_temp.assert_not_called()

    def test_publish_verifies_artifacts_and_refuses_overwrite(self):
        build = self.root / "build"
        build.mkdir()
        meta = figure.validate_metadata(self.source)
        names = [f"my-plot{suffix}" for suffix in (".svg", ".pdf", ".png")]
        for name in names:
            (build / name).write_text("original")
        figure.write_json(build / "render.json", {
            "metadata": meta, "outputs": {name: figure.sha256(build / name) for name in names},
        })
        (build / names[0]).write_text("tampered")
        site = self.root / "site"
        with patch.object(figure, "ROOT", site / "fig-generator"):
            with self.assertRaisesRegex(figure.FigureError, "changed since rendering"):
                figure.publish(SimpleNamespace(build=build))
            self.assertFalse((site / "assets").exists())
            (build / names[0]).write_text("original")
            result = figure.publish(SimpleNamespace(build=build))
            self.assertEqual(sorted(path.name for path in Path(result["assets"]).iterdir()), sorted(names))
            with self.assertRaisesRegex(figure.FigureError, "already exists"):
                figure.publish(SimpleNamespace(build=build))

    def test_doctor_fails_when_executables_are_missing(self):
        with patch.object(figure.shutil, "which", return_value=None), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(figure.doctor(SimpleNamespace()), 1)
        self.assertFalse(json.loads(out.getvalue())["ready"])


if __name__ == "__main__":
    unittest.main()
