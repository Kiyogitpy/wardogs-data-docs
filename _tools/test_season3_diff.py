"""Synthetic regression fixtures for the literal saved-export comparator."""
import contextlib
import copy
from decimal import Decimal
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import season3_diff as d


class LiteralDiffTests(unittest.TestCase):
    def changes(self, before, after):
        out = []
        d.diff_value(d.load_json(before), d.load_json(after), [], ["header", 1], out)
        return out

    def test_exact_numeric_types_and_precision(self):
        for before, after in (("1", "1.0"), ("1", "true"),
                              ("1.00000000000000000001", "1.00000000000000000002"),
                              ("9007199254740992", "9007199254740993"),
                              ("-0.0", "0.0")):
            with self.subTest(before=before, after=after):
                self.assertEqual(len(self.changes(before, after)), 1)
        self.assertFalse(self.changes("1.0", "1e0"))
        self.assertIs(type(d.load_json(d.dumps(Decimal("1e0")))), Decimal)
        self.assertEqual(d.load_json(d.dumps(Decimal("1.00000000000000000001"))),
                         Decimal("1.00000000000000000001"))

    def test_missing_null_and_unambiguous_paths(self):
        changes = self.changes('{"a/b~":null}', '{"x":null}')
        self.assertEqual([c["op"] for c in changes], ["removed", "added"])
        self.assertEqual(changes[0]["pointer"], "/a~1b~0")
        self.assertEqual(changes[0]["after_type"], "missing")
        self.assertNotIn("after", changes[0])
        self.assertIsNone(changes[1]["after"])

    def test_arrays_keep_indexes_and_do_not_infer_ids(self):
        changes = self.changes('[{"Id":"A","v":1},{"Id":"B","v":2}]',
                               '[{"Id":"B","v":2},{"Id":"A","v":1}]')
        self.assertEqual(len(changes), 4)
        self.assertEqual(changes[0]["tokens"], [0, "Id"])
        self.assertEqual(self.changes('[1,2]', '[0,1,2]')[-1]["tokens"], [2])

    def test_no_rename_swap_or_reference_index_suppression(self):
        self.assertEqual(len(self.changes('{"A":1}', '{"B":1}')), 2)
        self.assertEqual(len(self.changes('{"A":1,"B":2}', '{"A":2,"B":1}')), 2)
        self.assertEqual(len(self.changes('{"ObjectName":"A","ObjectPath":"x.1"}',
                                          '{"ObjectName":"A","ObjectPath":"x.2"}')), 1)

    def test_strict_complete_parser(self):
        for text in ('{"x":1,"x":2}', '{"a":{"x":1,"x":2}}',
                     '{"x":', '{} garbage', '{} {}', 'NaN',
                     '--- export: Class / A ---\n{}\n--- export: Class / B ---\n',
                     'prefix\n--- export: Class / A ---\n{}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                d.parse_exports(text)
        self.assertEqual(d.parse_exports('{"plain":true}')[0][0], "$document")
        parsed = d.parse_exports('--- export: Class / A ---\r\n{}\r\n--- export: Class / A ---\r\n{"v":2}\r\n')
        self.assertEqual(list(d.export_map(parsed)), [("Class / A", 1), ("Class / A", 2)])


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.s2, self.s3, self.out = [self.root / name for name in ("s2", "s3", "out")]
        for path in (self.s2, self.s3):
            path.mkdir()
            (path / "a.json").write_text('--- export: Class / A ---\n{"n":1}', encoding="utf-8")
            (path / "config.ini").write_text("config", encoding="utf-8")

    def manifests(self):
        return [{"source": {"revision": "synthetic-" + path.name, "schema": "synthetic"},
                 "files": d.inventory(path)} for path in (self.s2, self.s3)]

    def render(self):
        return d.render(self.s2, self.s3, *self.manifests())

    def test_identity_is_full_header_and_occurrence_not_name_or_type(self):
        (self.s3 / "a.json").write_text('--- export: OtherClass / A ---\n{"n":1}')
        files, index = self.render()
        self.assertEqual(index["totals"]["property_changes"], 2)
        assets = d.load_json(files["engine-tooling-data.json"])["assets"]
        self.assertEqual({c["op"] for c in assets[0]["changes"]}, {"added", "removed"})
        (self.s3 / "a.json").rename(self.s3 / "b.json")
        _, index = self.render()
        self.assertEqual(index["totals"]["assets_moved"], 0)
        self.assertEqual(index["totals"]["assets_added"], 1)
        self.assertEqual(index["totals"]["assets_removed"], 1)

    def test_path_case_is_preserved_without_implicit_pairing(self):
        (self.s3 / "a.json").rename(self.s3 / "A.json")
        _, index = self.render()
        self.assertEqual(index["totals"]["assets_added"], 1)
        self.assertEqual(index["totals"]["assets_removed"], 1)
        self.assertEqual(index["accounting"]["json_paired"], 0)

    def test_export_order_and_determinism(self):
        first, second = '--- export: C / A ---\n{}\n', '--- export: C / B ---\n{}\n'
        (self.s2 / "a.json").write_text(first + second)
        (self.s3 / "a.json").write_text(second + first)
        files, index = self.render()
        asset = d.load_json(files["engine-tooling-data.json"])["assets"][0]
        self.assertTrue(asset["export_order_changed"])
        self.assertEqual(asset["changes"], [])
        self.assertEqual((files, index), self.render())
        self.assertEqual(index["accounting"]["non_json_unchanged"], 1)

    def test_configs_are_compared_and_only_side_values_count_separately(self):
        for root, value in ((self.s2, 1), (self.s3, 2)):
            config = root / "Wardogs/Config/Experiences/plain.json"
            config.parent.mkdir(parents=True)
            config.write_text('{"value":' + str(value) + '}')
        (self.s3 / "a.json").write_text('--- export: Class / A ---\n{"n":2}')
        (self.s2 / "old.json").write_text('{"saved":null}')
        (self.s3 / "new.json").write_text('{"saved":null}')
        files, index = self.render()
        self.assertEqual(index["totals"]["property_changes"], 2)
        self.assertEqual(index["totals"]["added_values"], 1)
        self.assertEqual(index["totals"]["removed_values"], 1)
        accounted = d.load_json(files["files.json"])["files"]
        self.assertEqual(len(accounted), 5)
        config = next(row for row in accounted if row["path"].startswith("Wardogs/Config/"))
        self.assertEqual(config["exports_before"], [["$document", 1]])
        self.assertEqual(config["literal_changes"], 1)

    def test_large_values_reference_exact_sources_and_small_scalars_stay_inline(self):
        (self.s2 / "a.json").write_text(d.dumps({"large": [1] * 1000, "number": 1,
                                               "precise": Decimal("1.00000000000000000001"), "zero": Decimal("-0.0")}))
        (self.s3 / "a.json").write_text(d.dumps({"large": "x" * 2000, "number": Decimal("1.0"),
                                               "precise": Decimal("1.00000000000000000002"), "zero": Decimal("0.0")}))
        manifests = self.manifests()
        files, _ = d.render(self.s2, self.s3, *manifests)
        asset = d.load_json(files["engine-tooling-data.json"])["assets"][0]
        self.assertEqual(asset["change_exports"], [["$document", 1]])
        rows = {c["path"]: c for c in asset["changes"]}
        large = rows["0::/large"]
        self.assertEqual(d.resolve_reference(large["before"], self.s2, manifests[0]), [1] * 1000)
        self.assertEqual(d.resolve_reference(large["after"], self.s3, manifests[1]), "x" * 2000)
        number = rows["0::/number"]
        self.assertEqual(number["before_type"], "integer")
        self.assertEqual(number["after_type"], "decimal")
        self.assertIs(type(number["after"]), Decimal)
        self.assertNotIn("before_literal", number)
        self.assertEqual(rows["0::/precise"]["before_literal"], "1.00000000000000000001")
        self.assertEqual(rows["0::/zero"]["before_literal"], "-0.0")
        for field, value in (("content_sha256", "0" * 64), ("file_sha256", "0" * 64),
                             ("pointer", "/number"), ("count", 999),
                             ("export", ["wrong-header", 1]), ("file", "missing.json")):
            with self.subTest(field=field):
                bad = copy.deepcopy(large["before"])
                bad["$saved_export"][field] = value
                with self.assertRaises((ValueError, KeyError, TypeError)):
                    d.resolve_reference(bad, self.s2, manifests[0])
        (self.s2 / "a.json").write_text("{}")
        with self.assertRaises(ValueError):
            d.resolve_reference(large["before"], self.s2, manifests[0])

    def test_nested_exact_literals_survive_browser_number_limits(self):
        value = d.load_json('{"zero":-0.0,"nested":[9007199254740993,1.00000000000000000001]}')
        changes = []
        d.diff_value(d.MISSING, value, [], ["example", 1], changes)
        _, rows = d.compact_changes({"path": "a.json", "before_sha256": None,
                                    "after_sha256": "0" * 64, "changes": changes})
        self.assertEqual(rows[0]["after_literal"], d.dumps(value))
        self.assertIn('"zero":-0.0', rows[0]["after_literal"])
        self.assertIn('9007199254740993', rows[0]["after_literal"])
        self.assertIn('1.00000000000000000001', rows[0]["after_literal"])
        self.assertTrue(d.browser_safe({"normal": [1, Decimal("0.5")]}))

    def test_manifest_missing_extra_changed_duplicate_and_private_labels(self):
        for mutation in ("missing", "extra", "changed", "duplicate", "private"):
            with self.subTest(mutation=mutation):
                manifests = self.manifests()
                if mutation == "missing":
                    manifests[0]["files"].append({"path": "missing.json", "bytes": 2, "sha256": d.sha(b"{}")})
                elif mutation == "extra":
                    manifests[0]["files"].pop()
                elif mutation == "changed":
                    manifests[0]["files"][0]["sha256"] = "0" * 64
                elif mutation == "duplicate":
                    manifests[0]["files"].append(manifests[0]["files"][0])
                else:
                    manifests[0]["source"]["revision"] = "E:/private/checkout"
                with self.assertRaises(ValueError):
                    d.render(self.s2, self.s3, *manifests)
        with self.assertRaises(ValueError):
            d.inventory(self.root / "missing")

    def test_manifest_order_is_posix_case_sensitive_on_windows(self):
        (self.s2 / "Z.json").write_text("{}")
        (self.s2 / "aA.json").write_text("{}")
        rows = d.inventory(self.s2)
        self.assertEqual([r["path"] for r in rows], sorted(r["path"] for r in rows))
        manifest = {"source": {"revision": "synthetic"}, "files": list(reversed(rows))}
        self.assertEqual(d.validate_manifest(self.s2, manifest), rows)

    def cli(self, mode):
        manifests = self.manifests()
        args = ["--s2", str(self.s2), "--s3", str(self.s3), "--out", str(self.out), mode]
        for name, manifest in zip(("s2", "s3"), manifests):
            path = self.root / (name + "-manifest.json")
            path.write_text(d.dumps(manifest), encoding="utf-8")
            args += ["--" + name + "-manifest", str(path)]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return d.main(args)

    def test_malformed_input_never_writes(self):
        (self.s3 / "a.json").write_text('{"a":1,"a":2}')
        self.assertEqual(self.cli("--write"), 1)
        self.assertFalse(self.out.exists())
        (self.s3 / "a.json").write_text('{"a":')
        self.assertEqual(self.cli("--write"), 1)
        self.assertFalse(self.out.exists())

    def test_write_check_stats_and_output_mutation(self):
        self.assertEqual(self.cli("--stats"), 0)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.cli("--write"), 0)
        self.assertEqual(self.cli("--check"), 0)
        (self.out / "index.json").write_text("{}")
        self.assertEqual(self.cli("--check"), 1)
        (self.out / "unowned.json").write_text("{}")
        self.assertEqual(self.cli("--write"), 1)
        self.assertEqual((self.out / "unowned.json").read_text(), "{}")


if __name__ == "__main__":
    unittest.main()
