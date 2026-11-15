"""Config omission and nested-value controls; no native defaults inferred."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import default_game_ini
import price_modifiers


class PriceModifiers(unittest.TestCase):
    def test_omitted_multiplier_remains_unknown(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "config.ini"
            source.write_text('+PriceModifiers=/Script/WDGame.WDEntityPriceModifier_VendorDiscount(EntityTarget=Global,Data=)\n')
            with patch.object(price_modifiers, "INI", source):
                row = price_modifiers.build()["modifiers"][0]
        self.assertIsNone(row["multiplier"])
        self.assertIsNone(row["ratio"])

    def test_nested_multiplier_is_not_a_top_level_default(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "config.ini"
            source.write_text('+PriceModifiers=/Script/WDGame.WDEntityPriceModifier_Faction(EntityTarget=Specified,Data=((Entities=(GameplayTags=((TagName="Item.Test"))),Multiplier=0.0)))\n')
            with patch.object(price_modifiers, "INI", source):
                row = price_modifiers.build()["modifiers"][0]
        self.assertIsNone(row["multiplier"])

    def test_current_config_retains_zero_and_omitted_values(self):
        detailed = {row["kind"]: row for row in price_modifiers.build()["modifiers"]}
        summary = {row["kind"]: row for row in default_game_ini.build()["economy"]["priceModifiers"]}
        for rows in (detailed, summary):
            self.assertIsNone(rows["VendorDiscount"]["multiplier"])
            self.assertEqual(rows["Faction"]["multiplier"], 0.0)
            self.assertEqual(rows["FirstPurchase"]["multiplier"], 90.0)


if __name__ == "__main__":
    unittest.main()
