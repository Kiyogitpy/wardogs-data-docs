"""spray_patterns.py must refuse a Season folder that would rewrite the frozen S1/S2 archive with wrong data."""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "spray_patterns.py")
sys.path.insert(0, HERE)
import spray_patterns  # noqa: E402


def touch(path, text="{}"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class SeasonDirProblem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.data = os.path.join(self.tmp, "s2", "data")
        touch(os.path.join(self.data, "Wardogs", "Content", "x.json"))
        touch(os.path.join(self.data, "Wardogs", "Plugins", "W", "DA_Test_Stats.json"))

    def test_a_data_folder_with_stats_is_accepted(self):
        self.assertIsNone(spray_patterns.season_dir_problem(self.data))
        self.assertIsNone(spray_patterns.season_dir_problem(self.data + os.sep))

    def test_missing_folder(self):
        self.assertEqual(spray_patterns.season_dir_problem(os.path.join(self.tmp, "nope")), "not found")

    def test_export_root_instead_of_data_is_refused(self):
        self.assertIn("data/ folder", spray_patterns.season_dir_problem(os.path.join(self.tmp, "s2")))

    def test_data_folder_without_the_wardogs_tree_is_refused(self):
        empty = os.path.join(self.tmp, "empty", "data")
        os.makedirs(empty)
        self.assertIn("Wardogs/Content", spray_patterns.season_dir_problem(empty))

    def test_data_folder_without_stats_is_refused(self):
        bare = os.path.join(self.tmp, "bare", "data")
        touch(os.path.join(bare, "Wardogs", "Content", "x.json"))
        self.assertIn("DA_*_Stats.json", spray_patterns.season_dir_problem(bare))

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True,
                              encoding="utf-8")

    def test_write_with_a_wrong_s2_exits_before_touching_the_archive(self):
        before = os.path.getmtime(spray_patterns.OUT)
        r = self.run_cli("--write", "--s2", os.path.join(self.tmp, "s2"), "--s1", os.path.join(self.tmp, "none"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Season 2 folder", r.stderr)
        self.assertEqual(os.path.getmtime(spray_patterns.OUT), before)

    def test_a_present_but_wrong_s1_is_refused(self):
        r = self.run_cli("--check", "--s2", self.data, "--s1", os.path.join(self.tmp, "s2"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Season 1 folder", r.stderr)


if __name__ == "__main__":
    unittest.main()
