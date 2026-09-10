"""Exercise installer planning and failure paths without installing system packages."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "install.sh"


class InstallerContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.env = {**os.environ, "PATH": f"{self.bin}:/usr/bin:/bin"}
        self.stub("uname", "printf 'Linux\\n'")
        self.stub("python3", "exit 1")
        for command in ("lualatex", "kpsewhich"):
            self.stub(command, "exit 1")

    def stub(self, name, body):
        path = self.bin / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def run_installer(self, *arguments):
        return subprocess.run(["/bin/bash", str(INSTALLER), *arguments], cwd=self.root,
                              env=self.env, capture_output=True, text=True, timeout=10)

    def test_dry_run_plans_linux_install_without_executing_package_manager(self):
        self.stub("apt-get", "exit 99")
        result = self.run_installer("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("apt-get install", result.stdout)
        self.assertIn("texlive-metapost", result.stdout)
        self.assertIn("install-fiziko", result.stdout)

    def test_no_fiziko_omits_optional_installations(self):
        self.stub("apt-get", "exit 99")
        result = self.run_installer("--dry-run", "--no-fiziko")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("texlive-metapost", result.stdout)
        self.assertNotIn("install-fiziko", result.stdout)

    def test_check_does_not_try_to_install_missing_dependencies(self):
        self.stub("apt-get", "exit 99")
        result = self.run_installer("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Python 3.10+", result.stderr)
        self.assertNotIn("apt-get", result.stdout)

    def test_package_manager_failure_stops_installation(self):
        self.stub("id", "printf '0\\n'")
        self.stub("apt-get", "exit 99")
        result = self.run_installer()
        self.assertEqual(result.returncode, 99, result.stderr)
        self.assertNotIn("toolchain ready", result.stdout)
        self.assertNotIn("install-fiziko", result.stdout)

    def test_unsupported_platform_has_actionable_error(self):
        self.stub("uname", "printf 'MINGW64_NT\\n'")
        result = self.run_installer("--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("WSL", result.stderr)

    def test_unknown_option_and_conflicting_modes_fail(self):
        for arguments in (("--unknown",), ("--check", "--dry-run")):
            with self.subTest(arguments=arguments):
                self.assertNotEqual(self.run_installer(*arguments).returncode, 0)


if __name__ == "__main__":
    unittest.main()
