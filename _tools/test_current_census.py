"""Census comparison preserves types, unique keys and complete evidence."""
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_round25 import current_census_matches


def block(text):
    return '<!-- current-round25-census -->\n```json\n' + text + '\n```\n<!-- /current-round25-census -->'


class CurrentCensus(unittest.TestCase):
    expected = {"build": "CL533731", "zero": 0, "materials": {"PM_One": 2}}

    def test_complete_matches_and_omitted_evidence_rejects(self):
        self.assertTrue(current_census_matches(block(json.dumps(self.expected)), self.expected))
        self.assertFalse(current_census_matches(block('{"build":"CL533731","zero":0}'), self.expected))

    def test_boolean_zero_and_float_counts_reject(self):
        for old, new in (('"zero": 0', '"zero": false'), ('"PM_One": 2', '"PM_One": 2.0')):
            self.assertFalse(current_census_matches(block(json.dumps(self.expected).replace(old, new)), self.expected))

    def test_duplicate_keys_and_blocks_reject(self):
        text = json.dumps(self.expected)
        self.assertFalse(current_census_matches(block(text.replace('"zero": 0', '"zero": 99, "zero": 0')), self.expected))
        self.assertFalse(current_census_matches(block(text) + block(text), self.expected))


if __name__ == "__main__":
    unittest.main()
