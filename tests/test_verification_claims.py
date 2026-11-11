"""Narrow regression guards for retracted documentation interpretations.

These check prose consistency, not the truth of native/gameplay behavior.
Run: python -m unittest discover -s tests -p test_verification_claims.py -v
"""
from pathlib import Path
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VerificationClaimTests(unittest.TestCase):
    def test_status_effects_does_not_assign_walk_bob_duration_to_landing(self):
        text = (ROOT / "_wiki/game-mechanics/status-effects.md").read_text(encoding="utf-8")
        section = text.split("## Falling and landing\n", 1)[1].split("\n## ", 1)[0]
        self.assertNotRegex(section, r"(?i)landing[^\n.]*dips the weapon")
        self.assertRegex(section, r"(?i)walk gun-bob")
        self.assertIn("Wardogs_PlayerMovement_v1.md#3-fall-landing-and-vehicle-exit-damage", section)

    def test_vehicle_inactivity_legacy_seconds_key_is_explicitly_unverified(self):
        spec = importlib.util.spec_from_file_location(
            "vehicle_round85_tables", ROOT / "_tools/vehicle_round85_tables.py"
        )
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        data = generator.settings_data()
        key = "inactivity_lifetime_out_of_safe_zone_s"
        metadata = data.get("field_metadata", {}).get(key, {})
        self.assertIn("unit", metadata)
        self.assertIsNone(metadata["unit"])
        self.assertEqual(metadata.get("verification"), "unverified")
        self.assertTrue(metadata.get("legacy_key"))
        self.assertEqual(data["gameplay_systems"]["DA_GameplaySystems_ROT_02"][key], 90)

    def test_vehicle_inactivity_rendering_does_not_invent_seconds_or_server_ownership(self):
        spec = importlib.util.spec_from_file_location(
            "vehicle_round85_tables", ROOT / "_tools/vehicle_round85_tables.py"
        )
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        section = generator.settings_section()
        self.assertNotIn("Inactivity lifetime outside a safe zone (s)", section)
        self.assertNotIn("about 8.3 hours", section)
        self.assertNotIn("so the timer runs on the server", section)
        self.assertIn("unit unverified", section)
        self.assertIn("round92-modes-economy.md", section)

    def test_safe_zone_wiki_does_not_claim_an_untraced_vehicle_cleanup_timer(self):
        text = (ROOT / "_wiki/game-modes-and-maps/boundaries-and-safe-zones.md").read_text(encoding="utf-8")
        section = text.split("## Spawn safe zones\n", 1)[1]
        paragraph = next(line for line in section.splitlines() if line.startswith("- **Vehicles.**"))
        self.assertNotIn("before it is cleaned up", paragraph)
        self.assertIn("stored inactivity values", paragraph)
        self.assertIn("not established", paragraph)

    def test_buildable_assist_registry_selects_the_destruction_lookup_table(self):
        path = ROOT / "data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/DR_SessionEvent_BuildableDestroyed.json"
        self.assertTrue(path.is_file(), "The referenced buildable destruction registry export is missing")
        exports = json.loads(path.read_text(encoding="utf-8-sig"))
        registry = next(e for e in exports if e["Type"] == "DataRegistry")
        source = next(e for e in exports if e["Type"] == "DataRegistrySource_DataTable")
        self.assertEqual(registry["Properties"]["RegistryType"], "Challenges.SessionEvents.DestroyedBuildable")
        self.assertEqual(registry["Properties"]["ItemStruct"]["ObjectName"], "Class'WDVariantRewardLookupRow'")
        package = "/BuildableRewards/Rewards/LookupRegistries/DR_SessionEvent_BuildableDestroyed"
        self.assertEqual(registry["Properties"]["DataSources"][0]["ObjectPath"], package + ".1")
        self.assertEqual(source["Outer"]["ObjectPath"], package + ".0")
        self.assertEqual(source["Properties"]["SourceTable"]["AssetPathName"],
                         "/BuildableRewards/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.DT_RewardLookup_SessionEvent_BuildableDestroyed")

    def test_drill_rig_docs_use_the_rig_specific_activation_defaults(self):
        wiki = (ROOT / "_wiki/building/drill-rig.md").read_text(encoding="utf-8")
        self.assertIn("25%", wiki)
        self.assertIn("5 m/s", wiki)
        self.assertNotIn("code reads the world default", wiki)
        self.assertNotIn("whether that replaces the 3 m/s", wiki)
        technical = (ROOT / "game-features/Wardogs_Buildables_v1.md").read_text(encoding="utf-8")
        self.assertIn("0x85EB820", technical)
        self.assertIn("0x85EBAE2", technical)
        spec = importlib.util.spec_from_file_location("r45_misc_data", ROOT / "_tools/r45_misc_data.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIn("0x85EB820", module.HOTZONE_MAGNET["rigDataAssetValues"]["note"])
        self.assertNotIn("not the rig's", module.HOTZONE_MAGNET["rigDataAssetValues"]["note"])

    def test_ammo_duration_unit_is_traced_without_claiming_measured_latency(self):
        wiki = (ROOT / "_wiki/ammunition/ammo-packing.md").read_text(encoding="utf-8")
        technical = (ROOT / "game-features/Wardogs_AmmoPacking_v1.md").read_text(encoding="utf-8")
        self.assertIn("Seconds (native timer clock)", wiki)
        self.assertIn("Loose rounds use a separate combine-loose curve", wiki)
        self.assertNotIn("Combining loose rounds adds two of these times", wiki)
        self.assertIn("0x455CDB0", technical)
        self.assertNotIn("no unit is recovered", technical)
        self.assertNotIn("sum being seconds stays inferred", technical)
        self.assertIn("wall-clock", technical)

    def test_mouse_calibration_does_not_reuse_an_unselected_axis_scale(self):
        text = (ROOT / "_wiki/game-mechanics/controls-and-settings.md").read_text(encoding="utf-8")
        section = text.split("#### Mouse sensitivity formula\n", 1)[1].split("### Field of view", 1)[0]
        self.assertNotIn("degrees per mouse count = 0.07", section)
        self.assertNotIn("cm per 360 at 800 DPI", section)
        self.assertIn("0x4CE4053", section)
        self.assertIn("quantization", section)
        self.assertIn("0.398421", section)
        self.assertIn("calibration remains open", section)

    def test_buildable_assist_docs_match_the_recovered_producer_and_registry(self):
        text = (ROOT / "game-features/Wardogs_GameFeatures_Rewards_v2.md").read_text(encoding="utf-8")
        self.assertNotIn("The assist path is inferred", text)
        self.assertNotIn("The input is not named in these files", text)
        self.assertIn("retained assister damage", text)
        self.assertIn("0x858F646", text)
        self.assertIn("DR_SessionEvent_BuildableDestroyed", text)
        self.assertIn("| 11 | `WDChallengeDefinition` |", text)
        self.assertIn("role XP", text)

    def test_vehicle_noise_docs_and_generated_metadata_use_the_recovered_event_path(self):
        wiki = (ROOT / "_wiki/game-modes-and-maps/ai-enemies.md").read_text(encoding="utf-8")
        paragraph = next(line for line in wiki.splitlines() if line.startswith("- **Vehicle noise.**"))
        self.assertNotIn("Which game events make these noises count for the AI is not confirmed", paragraph)
        self.assertIn("repeating emissions", paragraph)
        self.assertIn("not guaranteed detection radii", paragraph)
        self.assertIn("damage attribution", paragraph)
        spec = importlib.util.spec_from_file_location("r42_modes_data", ROOT / "_tools/r42_modes_data.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        metadata = module.STATIC["vehicle_noise_defaults"]
        self.assertEqual(metadata.get("verification"), "verified-static-conditional")
        contract = metadata.get("emitter_contract", {})
        self.assertEqual(contract.get("reader"), "0x8869A80")
        self.assertEqual(contract.get("engine"), "0x8873CB0 -> 0x887EC80; cached range +0xF0")
        self.assertEqual(contract.get("horn"), "0x8873F80 -> 0x887EC80; cached range +0xF4")
        self.assertEqual(contract.get("destruction"), "0x8875970; cached range +0xF8")
        generated = json.loads((ROOT / "assets/data/r42-modes.json").read_text(encoding="utf-8"))
        self.assertEqual(generated["static"]["vehicle_noise_defaults"], metadata)

    def test_role_xp_assist_docs_preserve_ordered_context_alternatives(self):
        sources = [
            ("game-features/Wardogs_GameFeatures_Rewards_v2.md", "For assist context,"),
            ("docs/evidence/round93-registry-binding.md", "5. Those cash definitions"),
        ]
        for path, prefix in sources:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                paragraph = next(line for line in text.splitlines() if line.startswith(prefix))
                self.assertNotIn("instead select `AssistReward`", paragraph)
                self.assertIn("`BaseReward` selector", paragraph)
                self.assertIn("`AssistReward` alternative", paragraph)
                self.assertIn("context-dependent alternatives", paragraph)

    def test_hearing_consumer_docs_do_not_invent_a_local_expiration_comparison(self):
        text = (ROOT / "docs/evidence/round93-ai-rewards.md").read_text(encoding="utf-8")
        paragraph = next(line for line in text.splitlines() if line.startswith("4. **`UWDAIPerceptionComponent`**"))
        self.assertNotIn("non-expired", paragraph)
        self.assertIn("valid-sense-ID", paragraph)
        self.assertIn("positive-strength", paragraph)
        self.assertIn("non-invalid-age", paragraph)

    def test_ai_rewards_top_dispositions_name_the_current_static_scope(self):
        text = (ROOT / "docs/evidence/round93-ai-rewards.md").read_text(encoding="utf-8")
        section = text.split("## Disposition\n", 1)[1].split("## Sources and identity", 1)[0]
        for prefix in ("| **G5:", "| **G6:"):
            row = next(line for line in section.splitlines() if line.startswith(prefix))
            self.assertIn("**closed-static**", row)
            self.assertNotIn("**open**", row)
        self.assertIn("round93-registry-binding.md", section)
        self.assertIn("round93-ai-controller-config.md", section)
        self.assertIn("Historical discovery", section)

    def test_ammo_generator_preserves_source_links_and_native_seconds_prose(self):
        spec = importlib.util.spec_from_file_location("ammo_packing_tables", ROOT / "_tools/ammo_packing_tables.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with open(ROOT / module.PAGE, encoding="utf-8", newline="") as source:
            text = source.read()
        regenerated, count = module.regenerate(module.curves(), text)
        self.assertEqual(count, 9)
        self.assertEqual(regenerated, text, "Generator must not strip restored raw-source links or change the native-clock prose")

    def test_ai_controller_hearing_config_has_exact_component_and_sense_binding(self):
        path = ROOT / "data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BP_CoreAIController.json"
        self.assertTrue(path.is_file(), "The referenced AI controller's perception defaults are missing")
        exports = json.loads(path.read_text(encoding="utf-8-sig"))
        package = "/WDAIPvEAICore/BP_CoreAIController"
        cdo = next(e for e in exports if e["Name"] == "Default__BP_CoreAIController_C")
        perception = next(e for e in exports if e["Type"] == "WDAIPerceptionComponent")
        hearing = next(e for e in exports if e["Type"] == "AISenseConfig_Hearing")
        perception_path = package + "." + str(exports.index(perception))
        hearing_path = package + "." + str(exports.index(hearing))
        self.assertEqual(cdo["Properties"]["PerceptionComponent"]["ObjectPath"], perception_path)
        self.assertEqual(hearing["Outer"]["ObjectPath"], perception_path)
        self.assertIn(hearing_path, [r["ObjectPath"] for r in perception["Properties"]["SensesConfig"]])
        self.assertEqual(perception["Properties"]["HearingSense"]["ObjectName"], "Class'AISense_Hearing'")
        self.assertEqual(hearing["Properties"]["HearingRange"], 100000.0)
        self.assertEqual(hearing["Properties"]["MaxAge"], 30.0)
        preset_path = path.with_name("DefaultAIPreset.json")
        text = preset_path.read_text(encoding="utf-8")
        preset, _ = json.JSONDecoder().raw_decode(text[text.index("{"):])
        self.assertEqual(preset["Properties"]["AIControllerClass"]["AssetPathName"],
                         package + ".BP_CoreAIController_C")


if __name__ == "__main__":
    unittest.main()
