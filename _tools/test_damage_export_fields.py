"""Synthetic old/current field controls plus read-only cooked-export integration."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from damage_export_fields import armor_damage_context, caliber_modifiers


class FieldAssociations(unittest.TestCase):
    def test_caliber_uses_current_payload_without_historical_substitution(self):
        old = [{"Key": {"TagName": "Meta.Damage.Bullet.308Win"}, "Value": 1.0}]
        current = [{"Key": {"TagName": "Meta.Damage.Bullet.308Win"}, "Value": 0.91}]
        self.assertIs(caliber_modifiers({"_aaabapbnbhiopifeenjml": old}), old)
        self.assertIs(caliber_modifiers({"CaliberModifiers": current}), current)

    def test_armor_old_and_current_context(self):
        value = {"TagName": "Meta.Damage.Armor.Light"}
        for name in ("DamageContextTag", "_aaabapigngpcfjdppejoi"):
            self.assertIs(armor_damage_context({name: value}), value)

    def test_missing_and_ambiguous_fields_fail(self):
        for fn, names in (
            (caliber_modifiers, ("CaliberModifiers", "_aaabapbnbhiopifeenjml")),
            (armor_damage_context, ("DamageContextTag", "_aaabapigngpcfjdppejoi")),
        ):
            for properties in ({}, {"Unrelated": []}, {name: [] for name in names}):
                with self.subTest(function=fn.__name__, properties=properties):
                    with self.assertRaises(ValueError):
                        fn(properties)

    def test_prefix_lookalike_is_not_an_alias(self):
        with self.assertRaises(ValueError):
            caliber_modifiers({"_aaabapbnbhiopifeenjml_unknown": []})

    def test_empty_payload_is_preserved(self):
        self.assertEqual(caliber_modifiers({"CaliberModifiers": []}), [])

    def test_shared_damage_loader_reads_exported_values(self):
        import damage_tables as dt
        table = dt.rows("DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json")
        self.assertEqual(set(dt.CALIBER), set(table))
        for key, row in table.items():
            self.assertEqual(dt.CALIBER[key], dt.tag_map(caliber_modifiers(row)))
        import infantry_tables
        items = infantry_tables.armor_items()
        self.assertTrue(items)
        self.assertTrue(all(item["tag"] for item in items))
        self.assertNotIn(None, dt.ARMOR)

    def test_drill_known_old_and_current_paths(self):
        import buildable_semantics as bs
        fields = ("InitialDelayDuration", "HotZoneMagnetRechargeDuration", "HotZoneMagnetMinimumFuel",
                  "HotZoneMagnetDurationPerFuel", "MaxFuel", "Cost", "MaxHealth")
        synthetic = dict.fromkeys(fields, 1)
        for segment in ("Buildables/Content/Data/Buildables/Hotzone_Magnet",
                        "Buildables_HotZoneMagnet/Content/Data"):
            with patch.object(bs.os.path, "isfile", side_effect=lambda p: segment in p.replace("\\", "/")), \
                 patch.object(bs, "first", return_value=synthetic) as read:
                self.assertEqual(bs.drill(), synthetic)
                self.assertIn(segment, read.call_args.args[0].replace("\\", "/"))

    def test_empty_generic_vehicle_table_has_no_stored_rules(self):
        import damage_tables as dt
        with patch.object(dt, "rows", return_value={}), patch.object(dt.glob, "glob", return_value=[]):
            self.assertEqual(dt.vehicle_tables(), ([], {}))

    def test_present_generic_vehicle_row_keeps_rules_and_unknown_row_rejects(self):
        import damage_tables as dt
        rules = [{"Amount": -85.0}]
        with patch.object(dt.glob, "glob", return_value=[]):
            with patch.object(dt, "rows", return_value={"Meta.Damage.Vehicle": {"DamageModificationEntries": rules}}):
                self.assertIs(dt.vehicle_tables()[0], rules)
            with patch.object(dt, "rows", return_value={"UnrecognizedRow": {}}):
                with self.assertRaises(KeyError):
                    dt.vehicle_tables()

    def test_drill_missing_and_ambiguous_paths_fail(self):
        import buildable_semantics as bs
        for exists in (False, True):
            with patch.object(bs.os.path, "isfile", return_value=exists), \
                 patch.object(bs, "first") as read:
                with self.assertRaises(ValueError):
                    bs.drill()
                read.assert_not_called()


if __name__ == "__main__":
    unittest.main()
