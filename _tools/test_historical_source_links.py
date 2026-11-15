"""Historical links must resolve to the claimed Git object kind."""
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from link_sources import SourceIndex, strip_source_links, verify_links


class HistoricalSources(unittest.TestCase):
    def test_missing_and_wrong_kind_history_reject(self):
        revision = "a" * 40
        url = f"https://github.com/Kiyogitpy/wardogs-data-docs/blob/{revision}/data/old.json"
        for code, kind in ((1, b""), (0, b"tree\n"), (0, b"blob\n")):
            index = SourceIndex(Path("."), [])
            with patch("link_sources.subprocess.run", return_value=subprocess.CompletedProcess([], code, kind)) as call:
                self.assertEqual(verify_links(f"[old]({url})", index), [] if kind == b"blob\n" else [url])
                self.assertEqual(call.call_args.args[0][-1], revision + ":data/old.json")

    def test_current_and_historical_sources_are_separate(self):
        index = SourceIndex(Path("."), [])
        url = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/old.json"
        self.assertEqual(verify_links(f"[old]({url})", index), [url])

    def test_historical_code_label_remains_readable_to_generators(self):
        url = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/" + "a" * 40 + "/data/old.json"
        self.assertEqual(strip_source_links(f"[`old`]({url})"), "`old`")


if __name__ == "__main__":
    unittest.main()
