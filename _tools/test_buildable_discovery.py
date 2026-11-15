"""The relocated definition remains visible; ambiguous definitions reject."""
from pathlib import Path
import copy
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buildable_tables as tables


class BuildableDiscovery(unittest.TestCase):
    def test_current_definitions_have_item_or_stationary_coverage(self):
        expected, stationary = set(), set()
        for path in (Path(tables.ROOT) / "data").rglob("*.json"):
            rel = path.relative_to(Path(tables.ROOT) / "data").as_posix()
            for obj in tables.exports(rel):
                if (obj["Type"].startswith("WDBuildable") and obj["Type"] != "WDBuildablePlacementDataAsset"
                        and "EntityTag" in obj.get("Properties", {})):
                    if rel.startswith("Wardogs/Plugins/GameFeatures/Items/"):
                        expected.add((rel, obj["Name"]))
                    else:
                        self.assertTrue(rel.startswith("Wardogs/Plugins/GameFeatures/Vehicles/STN_"), rel)
                        stationary.add(rel)
        data = tables.load()
        self.assertEqual({(rel, name) for rel, name, _, _ in data["assets"]}, expected)
        rendered = tables.stationary(data)
        for path in stationary:
            self.assertIn(path, rendered)

    def test_current_relocated_drill_is_present_once(self):
        data = tables.load()
        rows = [row for row in data["assets"] if row[1] == "DA_Buildable_HotzoneMagnet"]
        self.assertEqual(len(rows), 1)
        self.assertIn("Buildables_HotZoneMagnet/Content/Data/", rows[0][0])
        self.assertEqual(len(data["damage"]["Meta.Damage.Buildable.BuildableHotzoneMagnet"]["DamageModificationEntries"]), 22)
        self.assertIn("id.buildable.hotzonemagnet", data["hammer"]["Large"])
        import structure_hits
        self.assertIn("HotzoneMagnet", structure_hits.buildables())

    def test_duplicate_definition_is_not_silently_combined(self):
        obj = {"Type": "WDBuildableDataAsset", "Name": "DA_Example", "Properties": {"EntityTag": {"TagName": "Test"}}}
        with patch.object(tables.glob, "glob", side_effect=[["a.json"], ["b.json"]]), \
                patch.object(tables, "exports", return_value=[obj]):
            with self.assertRaisesRegex(ValueError, "Duplicate buildable"):
                tables.load()

    def test_unproven_registry_bindings_reject(self):
        original = tables.exports(tables.HOTZONE + "Buildables_HotZoneMagnet.json")
        for mutation in ("unreferenced", "duplicate", "wrong_table", "disabled", "string_flag", "bool_priority"):
            objects = copy.deepcopy(original)
            feature = next(o for o in objects if o["Type"] == "GameFeatureData")
            action = next(o for o in objects if o["Type"] == "GameFeatureAction_DataRegistrySource")
            source = next(s for s in action["Properties"]["SourcesToAdd"] if s["RegistryToAddTo"] == "GlobalDamageData")
            if mutation == "unreferenced":
                feature["Properties"]["Actions"] = []
            elif mutation == "duplicate":
                action["Properties"]["SourcesToAdd"].append(copy.deepcopy(source))
            elif mutation == "wrong_table":
                source["DataTableToAdd"]["AssetPathName"] = "/Other.Table"
            elif mutation == "disabled":
                source["bServerSource"] = False
            elif mutation == "string_flag":
                source["bServerSource"] = "false"
            else:
                source["AssetPriority"] = False
            with patch.object(tables, "exports", return_value=objects):
                with self.assertRaises(ValueError):
                    tables.hotzone_rows("GlobalDamageData", "DT_GlobalDamage_BuildableData_HotZoneMagnet")

    def test_present_table_without_feature_source_rejects(self):
        with patch.object(tables.os.path, "isfile", side_effect=[False, True]):
            with self.assertRaises(ValueError):
                tables.hotzone_rows("GlobalDamageData", "DT_GlobalDamage_BuildableData_HotZoneMagnet")

    def test_conflicting_contribution_cannot_replace_root_rows(self):
        tag = next(iter(tables.table(tables.DATA + "DT_GlobalDamage_BuildableData.json")))
        with patch.object(tables, "hotzone_rows", return_value={tag: {}}):
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                tables.load()


if __name__ == "__main__":
    unittest.main()
