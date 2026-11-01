"""Focused tests for hashed_names_check. Run: python -I -W ignore -m unittest discover -s _tools -p test_hashed_names_check.py -v"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent / "hashed_names_check.py"
FOUND = "_" + "abcdefghijklmnopabcde"
SUFFIXED = "_" + "ponmlkjihgfedcbaponml"
MISSING = "_" + "gfedcba" * 3


class HashedNamesCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.tools = self.root / "tools"
        self.data = self.root / "data" / "Engine"
        self.tools.mkdir()
        self.data.mkdir(parents=True)
        # Line 2 is a comment: not a literal, so MISSING there must not count.
        (self.tools / "alpha.py").write_text(
            f'FOUND = "{FOUND}"\n'
            f"# {MISSING} in a comment\n"
            f'SUFFIXED = "{SUFFIXED}_$x$_$22$"\n'
            f'GONE = "{MISSING}"\n', encoding="utf-8")
        # Test files are skipped even when they hold a missing literal.
        (self.tools / "test_skip.py").write_text(f'X = "{"_" + "p" * 21}"\n', encoding="utf-8")
        (self.data / "a.json").write_text(json.dumps({"k": FOUND}), encoding="utf-8")
        (self.data / "b.json").write_text(json.dumps({"k": SUFFIXED + "_$y$_$22$"}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, *extra):
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--tools", str(self.tools), "--data", str(self.data), *extra],
            capture_output=True, text=True, encoding="utf-8")

    def test_found_and_suffixed_pass_and_missing_is_reported_with_line(self):
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(r.stdout.splitlines(), [
            f"alpha.py:4 {MISSING}",
            f"hashed names: 3 hard-coded, 1 missing from {self.data}",
        ])

    def test_exit_zero_when_nothing_missing(self):
        (self.data / "c.json").write_text(json.dumps({"k": MISSING}), encoding="utf-8")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("hashed names: 3 hard-coded, 0 missing", r.stdout)

    def test_json_output(self):
        out = self.root / "out" / "report.json"
        r = self.run_check("--json", str(out))
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")), {
            "hardcoded": 3,
            "missing": [{"script": "alpha.py", "line": 4, "name": MISSING}],
        })

    def test_missing_data_folder_is_usage_error(self):
        r = subprocess.run([sys.executable, "-I", str(SCRIPT), "--tools", str(self.tools),
                            "--data", str(self.root / "nope")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("--data is not a folder", r.stderr)


if __name__ == "__main__":
    unittest.main()
