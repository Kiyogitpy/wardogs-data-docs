"""Prevent model assumptions and range markers becoming current native claims."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


weapons = load("wiki_weapons")


class S3WeaponClaims(unittest.TestCase):
    def test_range_marker_does_not_define_damage_falloff(self):
        text = "\n".join(weapons.wiki_ttk.section_lines("M4"))
        self.assertIn("not a damage cutoff", text)
        self.assertNotIn("where damage falls with distance", text)
        self.assertIn("separate", weapons.comparison_page())

    def test_current_recoil_inputs_and_historical_native_spread_are_scoped(self):
        wid = next(iter(weapons.SPRAY_BY_ITEM.keys() & weapons.SPREAD_BY_ITEM.keys()))
        text = weapons.recoil_section(wid, "Test")
        self.assertIn("S3-input recoil model", text)
        self.assertIn("current native equivalence is unverified", text)
        self.assertIn("retains Season 1/2 data", text)
        self.assertIn("does not establish their absence from S3", text)
        self.assertNotIn("There is no per-shot bloom", text)

    def test_omitted_rpm_is_labelled_at_the_display(self):
        wid = next(w for w in weapons.loadouts["weapons"] if weapons.code_for(w) in weapons.wdamage)
        code = weapons.code_for(wid)
        assumed = {**weapons.wdamage[code], "rpm_source": "class_default_native"}
        with patch.dict(weapons.wdamage, {code: assumed}):
            self.assertIn("historical default assumption", weapons.stats(wid)["rpm"])
        with patch.dict(weapons.wdamage, {code: {**assumed, "rpm_source": "asset"}}):
            self.assertNotIn("historical default assumption", weapons.stats(wid)["rpm"])

    def test_ghillie_reference_is_distinct_from_missing_definition(self):
        locations = load("weapon_damage_locations")
        text = " ".join(locations.build()["meta"]["assumptions"])
        self.assertIn("include AppliedEffects references", text)
        self.assertIn("referenced effect definitions are absent", text)
        self.assertIn("not verified S3 protection", text)

    def test_comparison_marks_assumed_rpm_and_dependent_times(self):
        row = next(l for l in weapons.comparison_page().splitlines() if '[GGX 17]' in l and l.startswith('|'))
        self.assertIn('600†', row)
        self.assertEqual(row.count('†'), 3)  # RPM and two TTK cells, not the hit counts.
        self.assertIn('historical 600 RPM default', weapons.comparison_page())

    def test_fallback_range_is_not_called_stored(self):
        text = '\n'.join(weapons.wiki_ttk.section_lines('WEPN_027'))
        self.assertIn('may use a historical default when omitted', text)
        self.assertNotIn('stored effective-range', text)

    def test_bow_hub_follows_both_saved_speed_fields(self):
        fixture = {'Properties': {'WeaponStats': {'InitialBulletSpeed': 31000, 'TypicalSpeed': 21000,
                                                  'bOverrideTypicalSpeed': True}}}
        with patch.object(weapons, 'read', return_value='--- export: test ---\n' + json.dumps(fixture)):
            row = weapons.bow_row()
        self.assertIn('310 m/s initial setting', row)
        self.assertIn('210 m/s typical override', row)
        self.assertIn('release unverified', row)

    def _bow_row(self, stats, item_exports, bow_item):
        """bow_row() over fixture exports: the stats file and the item file each get their own text."""
        def fake_read(rel):
            if rel.endswith('DA_CombatBow_Stats.json'):
                return '--- export: stats ---\n' + json.dumps(stats)
            return ''.join(f'--- export: item {i} ---\n' + (x if isinstance(x, str) else json.dumps(x)) + '\n'
                           for i, x in enumerate(item_exports))
        with patch.object(weapons, 'read', side_effect=fake_read), patch.object(weapons, 'BOW_ITEM', bow_item):
            return weapons.bow_row()

    STATS = {'Properties': {'WeaponStats': {'InitialBulletSpeed': 24000}}}

    def test_bow_hub_reads_draw_time_and_price(self):
        row = self._bow_row(self.STATS, [{'Properties': {}}, {'Properties': {'FullDrawTime': 1.25}}],
                            {'price': 900, 'priceHidden': False})
        self.assertIn('| 1.25 s setting | 900 |', row)

    def test_bow_hub_labels_omitted_draw_and_hidden_or_missing_price(self):
        row = self._bow_row(self.STATS, [{'Properties': {}}], {'price': 900, 'priceHidden': True})
        self.assertIn('| omitted in export | not yet known |', row)
        row = self._bow_row(self.STATS, [{'Properties': {}}], {})
        self.assertIn('| omitted in export | not yet known |', row)

    def test_bow_hub_skips_an_unparseable_export(self):
        row = self._bow_row(self.STATS, ['{"Properties": {"FullDraw', {'Properties': {'FullDrawTime': 1.4}}],
                            {'price': 1350})
        self.assertIn('| 1.4 s setting | 1350 |', row)

    def test_ammo_summary_preserves_deagle_and_50cal_exceptions(self):
        def damage(code, aid, armor):
            return next(a for a in weapons.wdamage[code]['ammo'] if a['id'] == aid)['damage_raw']['torso_armor'][armor]
        self.assertGreater(damage('WEPN_027', 'ArmorPiercing', 'Medium'), damage('WEPN_027', 'FMJ', 'Medium'))
        for armor in weapons.ARMOR_NAME:
            self.assertLessEqual(damage('SR_04', 'ArmorPiercing', armor), damage('SR_04', 'FMJ', armor))
        self.assertIn('Deagle', weapons.ammo_page())
        self.assertIn('AP never beats FMJ', weapons.ammo_page())

    def test_tcx_recoil_reads_current_authored_pattern_not_the_archive(self):
        current = weapons.current_recoil_by_item()['ID_WEPN_037']
        path = Path(weapons.ROOT) / current['sourceNote'].split(';', 1)[0]
        raw = json.loads(path.read_text(encoding='utf-8').split('\n', 1)[1])['Properties']['WeaponStats']
        expected = [{'x': p['X'], 'y': p['Y']} for p in raw['RecoilPattern']]
        self.assertEqual(current['pattern'], expected)
        self.assertNotEqual(current['pattern'], weapons.SPRAY_BY_ITEM['ID_WEPN_037']['seasons']['s2']['pattern'])
        self.assertAlmostEqual(weapons._path(current, 10)[1], sum(p['Y'] for p in raw['RecoilPattern'][:10]))

    def test_stored_role_levels_are_separate_from_vendor_fields(self):
        self.assertIn('Recon 41', weapons.unlock_levels('SR_04'))
        self.assertIn('Support 8', weapons.unlock_levels('Launcher_04'))
        fixture = [{'tree': 'Meta.Role.Recon', 'node': 'Id.Item.SR_04', 'minLevel': 57}]
        with patch.object(weapons, 'ROLE_UNLOCK_NODES', fixture):
            self.assertEqual(weapons.unlock_levels('SR_04'), 'Recon 57')
            self.assertIn('Not resolved', weapons.unlock_levels('M4'))


if __name__ == "__main__":
    unittest.main()
