"""Synthetic controls for an absent versus present exported mode definition."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import experience_config_tables as tables


class ExperienceAvailability(unittest.TestCase):
    def test_absent_definition_does_not_reuse_historical_features(self):
        with patch.object(tables, "experiences", return_value=[("UI/Frontend", {})]):
            text = tables.infantry()
        self.assertIn("absent from this config export", text)
        self.assertNotIn("TNK_01", text)

    def test_present_definition_keeps_exported_features(self):
        with patch.object(tables, "experiences", return_value=[
                ("KOTH_InfantryOnly", {"DisabledGameFeatures": ["TNK_01", "FuturePack"]})]):
            text = tables.infantry()
        self.assertIn("`TNK_01`", text)
        self.assertIn("`FuturePack`", text)
        self.assertNotIn("absent from", text)


if __name__ == "__main__":
    unittest.main()
