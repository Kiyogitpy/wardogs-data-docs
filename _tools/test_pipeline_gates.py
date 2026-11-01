"""Tests for the update pipeline's gates: preflight, the shrink / mount gate and the canary values.
Run: python -I -m unittest discover -s _tools -p test_pipeline_gates.py -v   (or: python -I _tools/test_pipeline_gates.py)

Everything runs on synthetic inputs in a temp dir. `cmd_extract` is driven end to end with CueDump and WdExtract replaced by
a fake that writes a small export (copied from the repo's own data/) and a progress log, so no game, key or build is needed.
"""
import contextlib
import copy
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from argparse import Namespace
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import canary_values_check as cv  # noqa: E402
import update_pipeline as up  # noqa: E402

KEY_SENTINEL = "SECRET-KEY-SENTINEL-0123"
M4 = "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_002/Content/Data/DA_M4_Stats.json"
BASE = {"cuedump_warnings": 0, "cuedump_errored": 0, "cuedump_exported_files": 6830, "cuedump_packages": 66550,
        "cuedump_exported_bytes": 337079676, "cuedump_mounted_vfs": 120}
OK = {"exported": 6830, "candidates": 66550, "bytes": 337079676, "mounted": 120, "unmounted": None}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*a, **k)
    return rc, buf.getvalue()


class ShrinkGate(unittest.TestCase):
    def gate(self, **over):
        return up.shrink_gate(BASE, dict(OK, **over))

    def test_baseline_growth_and_small_dips_pass(self):
        self.assertEqual(self.gate(), [])
        self.assertEqual(self.gate(exported=9000, candidates=90000, bytes=500000000, mounted=130), [])
        self.assertEqual(self.gate(exported=6830 - 60, candidates=66550 - 600, bytes=int(337079676 * 0.97)), [])

    def test_exported_count_drop_fails(self):
        why = self.gate(exported=4000)
        self.assertEqual(len(why), 1)
        self.assertIn("exported files", why[0])

    def test_package_count_drop_fails(self):
        self.assertIn("packages read", self.gate(candidates=30000)[0])

    def test_byte_drop_fails_even_when_counts_hold(self):
        why = self.gate(bytes=int(337079676 * 0.8))
        self.assertEqual(len(why), 1)
        self.assertIn("exported bytes", why[0])

    def test_mounted_below_baseline_and_unmounted_fail(self):
        self.assertIn("containers mounted", self.gate(mounted=90)[0])
        self.assertIn("did not mount", self.gate(unmounted=4)[0])

    def test_unmeasured_values_and_null_baseline_are_skipped(self):
        self.assertEqual(up.shrink_gate(BASE, {"exported": None, "candidates": None, "bytes": None, "mounted": None, "unmounted": None}), [])
        self.assertEqual(up.shrink_gate(dict(BASE, cuedump_mounted_vfs=None), dict(OK, mounted=3)), [])

    def test_parse_progress_reads_mount_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "x_progress.log")
            with open(p, "w") as f:
                f.write("Mounted 120 vfs, 70000 files\nUnmounted 3 vfs\nDONE. processed=10 ok=5 skipped=4 errored=1 warnings=0\n")
            r = up.parse_progress(p)
        self.assertEqual((r["mounted"], r["unmounted"], r["done"]["ok"]), (120, 3, 5))


class Env:
    """A complete synthetic machine: every path input exists. `cfg` is the --config file."""

    def __init__(self, tmp):
        self.tmp = tmp
        j = lambda *p: os.path.join(tmp, *p)
        for d in ("paks", "builds", "sdk"):
            os.makedirs(j(d))
        for f, text in (("paks/a.pak", "x"), ("aes.txt", KEY_SENTINEL), ("v2.usmap", "m"), ("n.usmap", "m"), ("wd.exe", "x"), ("oo2.dll", "x"), ("c.csproj", "x")):
            with open(j(*f.split("/")), "w") as fh:
                fh.write(text)
        self.env = {"paks": j("paks"), "aes_key_file": j("aes.txt"), "usmap_cuedump": j("v2.usmap"), "usmap_wdextract": j("n.usmap"),
                    "wdextract_exe": j("wd.exe"), "oo2core": j("oo2.dll"), "cue4parse_project": j("c.csproj"), "builds_root": j("builds"),
                    "sdk_raw": j("sdk")}
        self.cfg = j("cfg.json")
        self.write_cfg()

    def write_cfg(self):
        with open(self.cfg, "w") as f:
            json.dump(self.env, f)

    def args(self, **k):
        d = dict(label="t", force=False, assets=False, config=self.cfg, step="run", quick=True, old=None, base="main",
                 worktree=None, full=False, passes=1, no_baseline=True)
        d.update(k)
        return Namespace(**d)


class Preflight(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.m = Env(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_complete_machine_passes(self):
        self.assertEqual(up.missing_inputs(self.m.env, "run"), [])
        rc, out = run(up.cmd_preflight, self.m.args())
        self.assertEqual(rc, 0)

    def test_every_missing_input_is_named_by_key_and_env_var(self):
        for k in ("aes_key_file", "cue4parse_project", "builds_root", "usmap_cuedump", "wdextract_exe"):
            self.m.env[k] = os.path.join(self.m.tmp, "gone", k)
        self.m.write_cfg()
        rc, out = run(up.cmd_preflight, self.m.args())
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertEqual(up.PREFLIGHT_RC, 5)
        for k in ("aes_key_file", "cue4parse_project", "builds_root", "usmap_cuedump", "wdextract_exe"):
            self.assertIn(k, out)
            self.assertIn("WD_PIPELINE_" + k.upper(), out)
        self.assertNotIn("usmap_wdextract", out)        # present, so not listed

    def test_key_file_contents_are_never_printed(self):
        self.m.env["cue4parse_project"] = os.path.join(self.m.tmp, "gone")
        self.m.write_cfg()
        rc, out = run(up.cmd_preflight, self.m.args())
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertNotIn(KEY_SENTINEL, out)

    def test_wrong_kind_counts_as_missing(self):
        self.m.env["aes_key_file"] = self.m.env["paks"]         # a directory where a file is expected
        self.assertEqual([k for k, _, _ in up.missing_inputs(self.m.env, "extract")], ["aes_key_file"])

    def test_sdk_raw_is_needed_by_run_only(self):
        self.m.env["sdk_raw"] = os.path.join(self.m.tmp, "gone")
        self.assertEqual(up.missing_inputs(self.m.env, "extract"), [])
        self.assertEqual([k for k, _, _ in up.missing_inputs(self.m.env, "run")], ["sdk_raw"])

    def test_extract_and_run_stop_before_doing_anything(self):
        self.m.env["aes_key_file"] = os.path.join(self.m.tmp, "gone")
        self.m.write_cfg()
        rc, out = run(up.cmd_extract, self.m.args())
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertEqual(os.listdir(self.m.env["builds_root"]), [])      # no label dir, no manifest
        with mock.patch.object(up, "cmd_snapshot", side_effect=AssertionError("snapshot ran")):
            rc, out = run(up.cmd_run, self.m.args())
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertIn("aes_key_file", out)


class ExtractGates(unittest.TestCase):
    """cmd_extract end to end with a fake CueDump."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.m = Env(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.canaries = cv.load_canaries()["canaries"]

    def extract(self, ok=1000, processed=10000, mounted=120, mutate=None, base_bytes=None, force=False):
        files = sorted({c["file"] for c in self.canaries})

        def fake_run_cmd(cmd, cwd=None, log=None, timeout=None, env=None, echo=False):
            if cmd[0] != "fake-cuedump":
                return 0, 0.0, ""
            data = cmd[-1]
            for rel in files:
                dst = os.path.join(data, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(ROOT, "data", rel), dst)
            if mutate:
                mutate(data)
            with open(data + "_progress.log", "w") as f:
                f.write("Mounted %d vfs, 70000 files\nDONE. processed=%d ok=%d skipped=0 errored=0 warnings=0\n" % (mounted, processed, ok))
            return 0, 0.1, ""

        reg = copy.deepcopy(up.load_registry())
        data = os.path.join(self.m.env["builds_root"], "t", "data")
        size = sum(os.path.getsize(os.path.join(ROOT, "data", rel)) for rel in files)
        reg["baseline"].update({"cuedump_exported_files": 1000, "cuedump_packages": 10000, "cuedump_exported_bytes": base_bytes or size,
                                "cuedump_mounted_vfs": 120})
        with mock.patch.object(up, "load_registry", return_value=reg), mock.patch.object(up, "ensure_cuedump", return_value="fake-cuedump"), \
                mock.patch.object(up, "run_cmd", side_effect=fake_run_cmd):
            rc, out = run(up.cmd_extract, self.m.args(force=force))
        meta = up.read_json(os.path.join(self.m.env["builds_root"], "t", "extract-meta.json"))
        return rc, out, meta

    def edit(self, rel, old, new):
        def go(data):
            p = os.path.join(data, rel)
            with open(p, encoding="utf-8", newline="") as f:
                t = f.read()
            self.assertIn(old, t)
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(t.replace(old, new))
        return go

    def test_healthy_export_and_growth_pass_and_record_the_canaries(self):
        rc, out, meta = self.extract()
        self.assertEqual((rc, meta["status"]), (0, "ok"))
        self.assertEqual(meta["canaries"]["checked"], len(self.canaries))
        self.assertEqual(meta["canaries"]["missing"] + meta["canaries"]["wrong_type"], [])
        self.assertEqual(meta["gate"]["shrunk"], [])
        rc, out, meta = self.extract(ok=1400, processed=14000, mounted=140, force=True)       # new content is fine
        self.assertEqual(rc, 0)

    def test_shrunk_export_fails_with_exit_3_and_names_the_aes_key(self):
        rc, out, meta = self.extract(ok=400, processed=4000, mounted=60)
        self.assertEqual(rc, 3)
        self.assertEqual(meta["status"], "export-shrunk")
        self.assertIn("AES KEY", out)
        self.assertIn("exported files", out)
        self.assertNotIn("USMAP IS STALE", out)
        self.assertNotIn(KEY_SENTINEL, out)

    def test_byte_drop_alone_fails(self):
        rc, out, meta = self.extract(base_bytes=2 * sum(os.path.getsize(os.path.join(ROOT, "data", c["file"])) for c in {c["file"]: c for c in self.canaries}.values()))
        self.assertEqual((rc, meta["status"]), (3, "export-shrunk"))
        self.assertIn("exported bytes", " ".join(meta["why"]))

    def test_missing_canary_fails_as_stale_usmap(self):
        rc, out, meta = self.extract(mutate=self.edit(M4, '"RoundsPerMinute"', '"_aaaaaaaaaaaaaaaaaaaaa"'))
        self.assertEqual((rc, meta["status"]), (3, "usmap-stale"))
        self.assertIn("infantry-m4-rpm", meta["canaries"]["missing"])
        self.assertIn("USMAP IS STALE", out)

    def test_wrong_type_canary_fails_as_stale_usmap(self):
        rc, out, meta = self.extract(mutate=self.edit(M4, '"RoundsPerMinute": 800.0', '"RoundsPerMinute": "800.0"'))
        self.assertEqual((rc, meta["status"]), (3, "usmap-stale"))
        self.assertEqual(meta["canaries"]["wrong_type"], ["infantry-m4-rpm"])

    def test_changed_canary_only_warns(self):
        rc, out, meta = self.extract(mutate=self.edit(M4, '"RoundsPerMinute": 800.0', '"RoundsPerMinute": 900.0'))
        self.assertEqual((rc, meta["status"]), (0, "ok"))
        self.assertEqual(meta["canaries"]["changed"], [{"id": "infantry-m4-rpm", "old": 800.0, "new": 900.0}])
        self.assertIn("canary changed, review: infantry-m4-rpm", out)


class Canaries(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.data = os.path.join(self._tmp.name, "data")
        os.makedirs(os.path.join(self.data, "d"))
        with open(os.path.join(self.data, "d", "multi.json"), "w", newline="") as f:
            f.write('--- export: UObject / A_0 ---\r\n{"Name": "A_0", "Properties": {"X": 5.0}}\r\n'
                    '--- export: UObject / B ---\r\n{"Name": "B", "Properties": {"Rows": [{"V": 1}, {"V": 2}], "Tag": "t", "On": true}}\r\n')
        with open(os.path.join(self.data, "d", "single.json"), "w") as f:
            f.write('{"Name": "S", "Properties": {"N": 7}}')
        self.spec = [
            {"id": "x", "area": "a", "file": "d/multi.json", "export": "A_0", "path": "Properties/X", "expected": 5.0},
            {"id": "row", "area": "a", "file": "d/multi.json", "export": "B", "path": "Properties/Rows/1/V", "expected": 2},
            {"id": "tag", "area": "b", "file": "d/multi.json", "export": "B", "path": "Properties/Tag", "expected": "t"},
            {"id": "single", "area": "b", "file": "d/single.json", "export": "S", "path": "Properties/N", "expected": 7},
        ]

    def status(self, spec=None):
        return {r["id"]: r["status"] for r in cv.evaluate(self.data, spec or self.spec)}

    def test_clean_data_passes(self):
        self.assertEqual(set(self.status().values()), {"ok"})
        self.assertEqual(cv.exit_code(cv.evaluate(self.data, self.spec)), 0)
        self.assertEqual(self.status([dict(self.spec[0], expected=5)]), {"x": "ok"})      # 5 == 5.0

    def test_missing_file_export_and_path(self):
        spec = [dict(self.spec[0], id="nofile", file="d/gone.json"), dict(self.spec[0], id="noexport", export="Z"),
                dict(self.spec[0], id="nopath", path="Properties/Y"), dict(self.spec[1], id="badindex", path="Properties/Rows/9/V")]
        self.assertEqual(set(self.status(spec).values()), {"missing"})

    def test_wrong_type(self):
        spec = [dict(self.spec[0], id="s", expected="5.0"), dict(self.spec[2], id="n", expected=1), dict(self.spec[0], id="b", expected=True)]
        res = cv.evaluate(self.data, spec)
        self.assertEqual([r["status"] for r in res], ["type"] * 3)
        self.assertEqual(cv.exit_code(res), 2)

    def test_changed_value(self):
        res = cv.evaluate(self.data, [dict(self.spec[0], expected=6.0), dict(self.spec[2], expected="u")])
        self.assertEqual([r["status"] for r in res], ["changed", "changed"])
        self.assertEqual(cv.exit_code(res), 1)
        self.assertEqual(cv.summarize(res)["changed"][0], {"id": "x", "old": 6.0, "new": 5.0})

    def write_canaries(self, spec):
        p = os.path.join(self._tmp.name, "canaries.json")
        with open(p, "w") as f:
            json.dump({"version": 1, "canaries": spec}, f)
        return p

    def main(self, *a):
        return run(cv.main, list(a))

    def test_check_exit_codes_and_listing(self):
        ok = self.write_canaries(self.spec)
        self.assertEqual(self.main("--check", "--data", self.data, "--canaries", ok)[0], 0)
        chg = self.write_canaries([dict(self.spec[0], expected=6.0)])
        rc, out = self.main("--check", "--data", self.data, "--canaries", chg)
        self.assertEqual(rc, 1)
        self.assertIn("changed, review", out)
        bad = self.write_canaries([dict(self.spec[0], expected=6.0), dict(self.spec[1], path="Properties/Rows/9/V"), dict(self.spec[2], expected=1)])
        rc, out = self.main("--check", "--data", self.data, "--canaries", bad)
        self.assertEqual(rc, 2)
        for needle in ("MISSING", "row", "WRONG TYPE", "tag", "changed, review", "x"):
            self.assertIn(needle, out)

    def test_accept_takes_over_reviewed_changes_only(self):
        p = self.write_canaries([dict(self.spec[0], expected=6.0), self.spec[3]])
        self.assertEqual(self.main("--accept", "--data", self.data, "--canaries", p)[0], 0)
        self.assertEqual(self.main("--check", "--data", self.data, "--canaries", p)[0], 0)
        self.assertEqual(json.loads(read(p))["canaries"][0]["expected"], 5.0)
        # a missing or mistyped canary is never accepted, and nothing is rewritten
        p = self.write_canaries([dict(self.spec[0], expected=6.0), dict(self.spec[1], path="Properties/Gone")])
        before = read(p)
        self.assertEqual(self.main("--accept", "--data", self.data, "--canaries", p)[0], 2)
        self.assertEqual(read(p), before)

    def test_shipped_canaries_cover_the_areas_and_are_present_in_the_repo_data(self):
        doc = cv.load_canaries()
        self.assertGreaterEqual(len(doc["canaries"]), 15)
        self.assertEqual(len({c["id"] for c in doc["canaries"]}), len(doc["canaries"]))
        areas = {c["area"] for c in doc["canaries"]}
        for a in ("infantry weapons", "vehicles", "artillery range table", "vendor prices", "challenge rewards", "movement"):
            self.assertIn(a, areas)
        s = cv.summarize(cv.evaluate(os.path.join(ROOT, "data"), doc["canaries"]))
        self.assertEqual((s["missing"], s["wrong_type"]), ([], []))      # changed values are a patch's business, not a misread

    def test_registry_runs_the_check_in_regen(self):
        reg = up.load_registry()
        e = next(x for x in reg["scripts"] if x["script"] == "canary_values_check.py")
        self.assertEqual((e["class"], e["tier"], e["check"]), ("checker", "core", ["--check"]))
        for k in ("cuedump_packages", "cuedump_exported_bytes", "cuedump_mounted_vfs"):
            self.assertIn(k, reg["baseline"])


if __name__ == "__main__":
    unittest.main()
