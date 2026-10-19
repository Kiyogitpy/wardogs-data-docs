"""Regression check: a failed table child reports stderr and preserves generated files."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import infantry_tables as tables


class RegenerationFailure(unittest.TestCase):
    def test_later_child_failure_reports_stderr_without_partial_write(self):
        original = ("<!-- infantry_tables --zones -->\nold zones\n<!-- /infantry_tables -->\n"
                    "<!-- infantry_tables --actor-explosives -->\nold actors\n<!-- /infantry_tables -->\n")
        error = subprocess.CalledProcessError(
            1, [sys.executable, "--actor-explosives"], stderr="child diagnostic sentinel\n")
        with tempfile.TemporaryDirectory(prefix="wardogs-regen-check-") as folder:
            page = Path(folder, "page.md")
            page.write_bytes(original.encode())
            data = Path(folder, "data.json")
            data.write_bytes(b'{"sentinel": true}\n')
            diagnostics = io.StringIO()
            with patch.object(tables, "ROOT", folder), patch.object(tables, "PAGE", "page.md"), \
                    patch.object(tables, "JSON_OUT", str(data)), \
                    patch.object(tables.subprocess, "run", side_effect=[
                        subprocess.CompletedProcess([], 0, "replacement zones\n", ""), error]), \
                    contextlib.redirect_stderr(diagnostics):
                with self.assertRaises(subprocess.CalledProcessError):
                    tables.write_docs()
            self.assertIn("child diagnostic sentinel", diagnostics.getvalue())
            self.assertEqual(page.read_bytes(), original.encode())
            self.assertEqual(data.read_bytes(), b'{"sentinel": true}\n')


if __name__ == "__main__":
    unittest.main()
