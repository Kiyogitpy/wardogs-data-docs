"""Focused saved-export compatibility and fail-closed economy controls (stdlib only)."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("economy_tables", Path(__file__).with_name("economy_tables.py"))
econ = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(econ)
S2_REVISION = "8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b"


class EconomyHotfixTests(unittest.TestCase):
    def test_current_achievements(self):
        errors = []
        rows = econ.achievements(errors)
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 14)
        self.assertTrue(all(r["criteria"] for r in rows))
        self.assertEqual([r["threshold"] for r in rows if r["parameter"]], [100000, 100000, 3600.0, 95000.0])
        slot = next(r for r in rows if r["tag"].endswith("SlotMachine"))
        self.assertIn("NumCodeDigits >= 4", slot["criteria"])
        self.assertIn("integer 2", rows[-1]["criteria"])

    def test_historical_achievements(self):
        def old_exports(path):
            rel = Path(path).resolve().relative_to(Path(econ.ROOT)).as_posix()
            raw = subprocess.check_output(["git", "show", S2_REVISION + ":" + rel], cwd=econ.ROOT).decode()
            return [json.loads(x) for x in econ.EXPORT.split(raw)[1:]]
        with patch.object(econ, "exports", side_effect=old_exports), patch.object(econ.os.path, "exists", return_value=False):
            errors = []
            rows = econ.achievements(errors)
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(r["criteria"] for r in rows))
        self.assertTrue(all(r["thresholdEvidence"]["status"] == "historical_report" for r in rows if r["parameter"]))

    def test_historical_wagers(self):
        def old_table(rel):
            raw = subprocess.check_output(["git", "show", S2_REVISION + ":data/Wardogs/Content/" + rel], cwd=econ.ROOT).decode()
            return json.loads(econ.EXPORT.split(raw)[1])["Rows"]
        with patch.object(econ, "table", side_effect=old_table):
            errors = []
            wagers = econ.wagers(errors)
        self.assertEqual(errors, [])
        self.assertTrue(all(r["category"] for r in wagers["conditions"]))
        self.assertTrue(any(r["requiresAnyAction"] for r in wagers["conditions"]))

    def test_parameter_metadata_mutations(self):
        tag = "Achievement.Economy.LoadoutSpend"
        original = econ.table(econ.SHARED_CHALLENGES)[tag]["StateTreeReference"]
        self.assertTrue(econ.parameter_matches(original, econ.BYTE_VALUES[tag]))
        variants = []
        for field, value in [("Name", "Unknown"), ("ID", "wrong"), ("ValueType", "EPropertyBagPropertyType::Float"),
                             ("ContainerType", "EPropertyBagContainerType::Array")]:
            sr = copy.deepcopy(original)
            sr["Parameters"]["PropertyDescs"][0][field] = value
            variants.append(sr)
        for descs in [[], original["Parameters"]["PropertyDescs"] * 2]:
            sr = copy.deepcopy(original)
            sr["Parameters"]["PropertyDescs"] = descs
            variants.append(sr)
        for field, value in [("SerialSize", 5), ("SerialSize", 7)]:
            sr = copy.deepcopy(original)
            sr["Parameters"][field] = value
            variants.append(sr)
        sr = copy.deepcopy(original)
        sr["PropertyOverrides"] *= 2
        variants.append(sr)
        for sr in variants:
            with self.subTest(sr=sr):
                self.assertFalse(econ.parameter_matches(sr, econ.BYTE_VALUES[tag]))

    def test_changed_source_suppresses_thresholds(self):
        original = econ.exports
        def changed(path):
            data = original(path)
            if str(path).endswith("DT_Challenges_SessionEvents_Shared.json"):
                row = data[0]["Rows"]["Achievement.Economy.LoadoutSpend"]
                row["StateTreeReference"]["Parameters"]["SerialSize"] = 5
            return data
        with patch.object(econ, "exports", side_effect=changed):
            errors = []
            rows = econ.achievements(errors)
        self.assertTrue(errors)
        self.assertTrue(all(r["threshold"] is None for r in rows))

    def test_missing_and_duplicate_challenges(self):
        original = econ.table
        target = "Achievement.Economy.LoadoutSpend"
        for duplicate in (False, True):
            def changed(rel):
                data = copy.deepcopy(original(rel))
                if duplicate and rel == econ.SHOOTING_CHALLENGES:
                    data[target] = original(econ.SHARED_CHALLENGES)[target]
                if not duplicate and rel == econ.SHARED_CHALLENGES:
                    del data[target]
                return data
            with patch.object(econ, "table", side_effect=changed):
                errors = []
                rows = econ.achievements(errors)
            self.assertTrue(errors)
            row = next(r for r in rows if r["tag"] == target)
            self.assertIsNone(row["threshold"])
            self.assertIsNone(row["criteria"])

    def test_changed_tree_suppresses_prose(self):
        original = econ.exports
        for change in ("binding", "duplicate", "truncated"):
            def changed(path):
                data = original(path)
                if str(path).endswith("ST_Achievement_HesBehindYou.json"):
                    if change == "binding":
                        data[0]["Properties"]["Nodes"]["Structs"][5]["bInvert"] = True
                    elif change == "duplicate":
                        data.append(copy.deepcopy(data[0]))
                    else:
                        data = []
                return data
            with patch.object(econ, "exports", side_effect=changed):
                errors = []
                rows = econ.achievements(errors)
            self.assertTrue(errors)
            self.assertIsNone(next(r for r in rows if r["tag"].endswith("HesBehindYou"))["criteria"])

    def test_unknown_achievement_is_explicit(self):
        original = econ.table
        def changed(rel):
            data = copy.deepcopy(original(rel))
            if rel == "Meta/Achievements/DT_Achievements.json":
                data["Achievement.Unknown"] = {"DisplayName": "Unknown", "SteamAchievementID": "Unknown"}
            return data
        with patch.object(econ, "table", side_effect=changed):
            errors = []
            rows = econ.achievements(errors)
        self.assertIsNone(rows[-1]["criteria"])
        self.assertIn("Achievement.Unknown", errors[-1])

    def test_tag_containers(self):
        self.assertEqual(econ.action_tags({"GameplayTags": [{"TagName": "Wager.Action.Kills"}]}), ["Wager.Action.Kills"])
        self.assertEqual(econ.action_tags(["Wager.Action.Kills"]), ["Wager.Action.Kills"])
        self.assertEqual(econ.action_tags([]), [])
        for bad in (None, "Wager.Action.Kills", {}, {"Other": []}, [1], [{"Other": "x"}]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                econ.action_tags(bad)

    def test_wagers_keep_current_actions_and_unknown_categories(self):
        errors = []
        wagers = econ.wagers(errors)
        self.assertEqual(len(errors), 90)
        self.assertTrue(all("Category" in e for e in errors))
        row = next(r for r in wagers["conditions"] if r["tag"] == "Wager.Condition.NoResupply")
        self.assertIsNone(row["category"])
        self.assertEqual(row["requiresAnyAction"], ["Wager.Action.Kills"])

    def test_raw_unknown_truncated_and_duplicate_rejected(self):
        shared = econ.exports(Path(econ.DATA) / econ.SHARED_CHALLENGES)
        for raw in (b"", b"\x00\x03", bytes.fromhex("0003a0860100") * 2):
            with patch("builtins.open", return_value=io.BytesIO(raw)), patch.object(econ, "exports", return_value=shared):
                errors = []
                econ.verify_bytes("unused", errors)
            self.assertTrue(errors)
        with patch("builtins.open", side_effect=FileNotFoundError("missing")):
            errors = []
            econ.verify_bytes("unused", errors)
        self.assertTrue(errors)

    def test_cli_check_and_write_contract(self):
        doc = {"achievements": [], "wagers": {"actions": [], "conditions": [], "objectiveCatalog": []}, "roleUnlocks": {"nodes": []}}
        rendered = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
        for check, stale, expected in [(True, False, 0), (True, True, 1), (False, False, 0)]:
            stream = io.StringIO("stale" if stale else rendered)
            stream.close = lambda: None
            with patch.object(econ, "build", return_value=doc), patch.object(econ.os.path, "exists", return_value=True), \
                    patch.object(econ.os, "makedirs"), patch("builtins.open", return_value=stream) as opened, patch("sys.stdout", new=io.StringIO()):
                self.assertEqual(econ.main(["--check"] if check else []), expected)
            self.assertEqual(opened.call_args.args[1:] if len(opened.call_args.args) > 1 else (), () if check else ("w",))


if __name__ == "__main__":
    unittest.main()
