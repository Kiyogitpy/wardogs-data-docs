import subprocess
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import source_provenance


TREE = "0123456789abcdef0123456789abcdef01234567"


def result(code=0, stdout=""):
    return subprocess.CompletedProcess([], code, stdout, "")


class SourceDataTreeTests(unittest.TestCase):
    def test_clean_and_dirty_status(self):
        for status in (b"", b" M data/file", b"M  data/file", b"?? data/new"):
            with self.subTest(status=status):
                with patch.object(source_provenance.subprocess, "run", side_effect=[result(stdout=TREE), result(stdout=status)]) as run:
                    expected = TREE + ("+dirty" if status else "")
                    self.assertEqual(source_provenance.source_data_tree("repo"), expected)
                    self.assertEqual(len(run.call_args_list), 2)
                    self.assertTrue(all(call.args[0][0] == "git" for call in run.call_args_list))
                    self.assertIn("rev-parse", run.call_args_list[0].args[0])
                    self.assertIn("status", run.call_args_list[1].args[0])

    def test_missing_head_or_status_failure_returns_none(self):
        for responses in ([result(1)], [result(stdout=TREE), result(1)]):
            with patch.object(source_provenance.subprocess, "run", side_effect=responses):
                self.assertIsNone(source_provenance.source_data_tree("repo"))

    def test_git_error_returns_none_without_output_fallback(self):
        with patch.object(source_provenance.subprocess, "run", side_effect=OSError):
            self.assertIsNone(source_provenance.source_data_tree("repo"))


if __name__ == "__main__":
    unittest.main()
