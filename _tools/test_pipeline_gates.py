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
        for d in ("paks", "builds", "sdk", "s1/Wardogs/Content", "s2/Wardogs/Content"):
            os.makedirs(j(*d.split("/")))
        for f, text in (("paks/a.pak", "x"), ("aes.txt", KEY_SENTINEL), ("v2.usmap", "m"), ("n.usmap", "m"), ("wd.exe", "x"), ("oo2.dll", "x"), ("c.csproj", "x")):
            with open(j(*f.split("/")), "w") as fh:
                fh.write(text)
        self.env = {"paks": j("paks"), "aes_key_file": j("aes.txt"), "usmap_cuedump": j("v2.usmap"), "usmap_wdextract": j("n.usmap"),
                    "wdextract_exe": j("wd.exe"), "oo2core": j("oo2.dll"), "cue4parse_project": j("c.csproj"), "builds_root": j("builds"),
                    "sdk_raw": j("sdk"), "season1_export": j("s1"), "season2_export": j("s2")}
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

    def test_run_needs_both_season_exports_with_wardogs_content_but_extract_does_not(self):
        shutil.rmtree(os.path.join(self.m.env["season2_export"], "Wardogs"))
        self.m.env["season1_export"] = os.path.join(self.m.tmp, "gone")
        self.assertEqual(up.missing_inputs(self.m.env, "extract"), [])
        self.assertEqual([(k, w) for k, _, w in up.missing_inputs(self.m.env, "run")],
                         [("season2_export", "no Wardogs/Content inside"), ("season1_export", "missing")])
        self.assertEqual([k for k, _, _ in up.missing_inputs(self.m.env, "regen")], ["season2_export", "season1_export"])
        self.m.write_cfg()
        rc, out = run(up.cmd_preflight, self.m.args(step="regen"))
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertIn("WD_PIPELINE_SEASON2_EXPORT", out)
        self.assertIn("WD_PIPELINE_SEASON1_EXPORT", out)

    def test_cue4parse_is_required_only_when_cuedump_must_be_rebuilt(self):
        bin_dir = up.cuedump_bin_dir(self.m.env)
        exe, stamp = up.cuedump_paths(bin_dir)
        os.makedirs(bin_dir)
        os.remove(self.m.env["cue4parse_project"])
        names = lambda: [k for k, _, _ in up.missing_inputs(self.m.env, "extract")]
        self.assertEqual(names(), ["cue4parse_project"])                  # no built exe
        with open(exe, "w") as f:
            f.write("x")
        self.assertEqual(names(), [])                                     # exe without a stored hash is accepted
        with open(stamp, "w") as f:
            f.write("0" * 64)
        self.assertEqual(names(), ["cue4parse_project"])                  # sources changed since the build
        with open(stamp, "w") as f:
            f.write(up.cuedump_source_hash())
        self.assertEqual(names(), [])
        rc, out = run(up.cmd_preflight, self.m.args(step="extract"))
        self.assertEqual(rc, 0, out)

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

    def extract(self, ok=1000, processed=10000, mounted=120, mutate=None, base_bytes=None, force=False, crash=None, write_log=True, stale_log=None):
        """crash: (rc, output, wrote_data) makes the fake CueDump fail; stale_log: text of a progress log left by an earlier run."""
        files = sorted({c["file"] for c in self.canaries})
        if stale_log:
            os.makedirs(os.path.join(self.m.env["builds_root"], "t"))
            with open(os.path.join(self.m.env["builds_root"], "t", "data_progress.log"), "w") as f:
                f.write(stale_log)

        def fake_run_cmd(cmd, cwd=None, log=None, timeout=None, env=None, echo=False):
            if cmd[0] != "fake-cuedump":
                return 0, 0.0, ""
            data = cmd[-1]
            if crash and not crash[2]:
                return crash[0], 0.1, crash[1]
            for rel in files:
                dst = os.path.join(data, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(ROOT, "data", rel), dst)
            if mutate:
                mutate(data)
            if write_log:
                with open(data + "_progress.log", "w") as f:
                    f.write("Mounted %d vfs, 70000 files\nDONE. processed=%d ok=%d skipped=0 errored=0 warnings=0\n" % (mounted, processed, ok))
            return (crash[0], 0.1, crash[1]) if crash else (0, 0.1, "")

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

    def test_cuedump_stopping_on_too_few_containers_is_a_truncated_export_not_a_stale_usmap(self):
        # tools/cuedump aborts with rc 1 before it creates data/ or writes the progress log: nothing to compare, so the output decides
        rc, out, meta = self.extract(crash=(1, "Only 5 containers mounted - wrong key or unsupported format. Aborting.", False), write_log=False)
        self.assertEqual((rc, meta["status"]), (3, "export-shrunk"))
        self.assertIn("AES KEY", out)
        self.assertIn("Only 5 containers mounted", out)
        self.assertNotIn("USMAP IS STALE", out)
        self.assertNotIn(KEY_SENTINEL, out)

    def test_cuedump_failing_before_creating_data_is_a_truncated_export(self):
        rc, out, meta = self.extract(crash=(1, "unhandled exception", False), write_log=False)
        self.assertEqual((rc, meta["status"]), (3, "export-shrunk"))

    def test_cuedump_failing_after_it_exported_stays_a_usmap_problem(self):
        rc, out, meta = self.extract(crash=(1, "System.Exception: boom", True))
        self.assertEqual((rc, meta["status"]), (3, "usmap-stale"))
        self.assertIn("CueDump exited 1", " ".join(meta["why"]))

    def test_a_progress_log_from_an_earlier_run_is_never_read(self):
        old = "Mounted 120 vfs, 70000 files\nDONE. processed=10000 ok=1000 skipped=0 errored=0 warnings=0\n"
        rc, out, meta = self.extract(write_log=False, stale_log=old)
        self.assertEqual((rc, meta["status"]), (3, "usmap-stale"))
        self.assertIn("no DONE line", " ".join(meta["why"]))
        self.assertIsNone(meta["steps"]["cuedump"]["progress"]["done"])

    def test_a_failed_extraction_is_replaced_by_the_retry_but_a_good_one_is_not(self):
        rc, out, meta = self.extract(ok=400, processed=4000, mounted=60)
        self.assertEqual(rc, 3)
        rc, out, meta = self.extract()                                   # same label, no --force: the failed data/ is replaced
        self.assertEqual((rc, meta["status"]), (0, "ok"))
        self.assertIn("holds a failed extraction", out)
        with self.assertRaises(SystemExit) as cm:                       # a verified extraction still needs --force
            self.extract()
        self.assertIn("--force", str(cm.exception))

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


class CueDumpBuild(unittest.TestCase):
    """ensure_cuedump rebuilds when the sources' hash differs from the one stored next to the exe, never because of file times."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.bin = os.path.join(self._tmp.name, "bin")
        os.makedirs(self.bin)
        self.exe, self.stamp = up.cuedump_paths(self.bin)
        self.env = {"cue4parse_project": "C4P"}
        self.builds = []

    def fake_build(self, cmd, **kw):
        self.builds.append(cmd)
        with open(self.exe, "w") as f:
            f.write("built")
        return 0, 0.0, ""

    def ensure(self):
        with mock.patch.object(up, "run_cmd", side_effect=self.fake_build):
            rc, out = run(up.ensure_cuedump, self.env, self.bin)
        return rc, out

    def test_no_exe_builds_and_stores_the_hash(self):
        exe, out = self.ensure()
        self.assertEqual(len(self.builds), 1)
        self.assertEqual(read(self.stamp).strip(), up.cuedump_source_hash())

    def test_a_fresh_checkout_with_a_current_hash_does_not_rebuild_whatever_the_file_times(self):
        self.ensure()
        os.utime(self.exe, (0, 0))                  # older than every source file, as after a fresh clone or worktree
        self.builds.clear()
        self.ensure()
        self.assertEqual(self.builds, [])

    def test_changed_sources_rebuild(self):
        self.ensure()
        with open(self.stamp, "w") as f:
            f.write("0" * 64)
        self.builds.clear()
        self.ensure()
        self.assertEqual(len(self.builds), 1)
        self.assertEqual(read(self.stamp).strip(), up.cuedump_source_hash())

    def test_an_existing_exe_without_a_hash_is_accepted_stamped_and_announced(self):
        with open(self.exe, "w") as f:
            f.write("built elsewhere")
        exe, out = self.ensure()
        self.assertEqual(self.builds, [])
        self.assertEqual(read(self.stamp).strip(), up.cuedump_source_hash())
        self.assertIn("no source hash was stored", out)

    def test_the_hash_ignores_line_endings_but_not_content(self):
        def with_sources(program, csproj):
            d = tempfile.mkdtemp(dir=self._tmp.name)
            os.makedirs(os.path.join(d, "tools", "cuedump"))
            for n, b in (("Program.cs", program), ("CueDump.csproj", csproj)):
                with open(os.path.join(d, "tools", "cuedump", n), "wb") as f:
                    f.write(b)
            with mock.patch.object(up, "REPO", d):
                return up.cuedump_source_hash()
        lf = with_sources(b"a\nb\n", b"<P/>\n")
        self.assertEqual(lf, with_sources(b"a\r\nb\r\n", b"<P/>\r\n"))
        self.assertNotEqual(lf, with_sources(b"a\nc\n", b"<P/>\n"))
        self.assertNotEqual(lf, with_sources(b"a\nb\n", b"<Q/>\n"))


class LabelSelection(unittest.TestCase):
    """Only labels whose extraction passed (extract-meta.json status ok) count as the previous build."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.m = Env(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.root = self.m.env["builds_root"]
        self.cur = up.build_manifest(self.m.env, "cur", quick=True)
        # good: an older build (one more pak than is installed now); bad: the installed paks, but their extraction failed
        self.label("good", "2026-01-01T00:00:00+00:00", "ok", extra=True)
        self.label("bad", "2026-02-01T00:00:00+00:00", "export-shrunk")

    def label(self, name, created, status, extra=False, data=True):
        m = dict(self.cur, label=name, created=created)
        if extra:
            m["files"] = m["files"] + [{"name": "old.pak", "size": 1, "mtime": 0, "hash": None}]
        up.write_json(os.path.join(self.root, name, "manifest.json"), m)
        if status:
            up.write_json(os.path.join(self.root, name, "extract-meta.json"), {"status": status})
        if data:
            os.makedirs(os.path.join(self.root, name, "data"))

    def test_a_failed_extraction_does_not_hide_the_next_detection(self):
        rc, out = run(up.cmd_status, self.m.args(against=None))
        self.assertEqual(rc, 10, out)
        self.assertIn("last manifest: good", out)

    def test_manifests_skip_failed_labels_only_on_request_and_keep_snapshot_only_labels(self):
        self.label("snap", "2026-03-01T00:00:00+00:00", None, data=False)
        names = lambda **k: [d for _, d, _ in up.manifests(self.root, **k)]
        self.assertEqual(names(), ["good", "bad", "snap"])
        self.assertEqual(names(skip_failed=True), ["good", "snap"])

    def test_extract_ok_needs_the_ok_status_and_a_data_dir(self):
        self.label("nodata", "2026-04-01T00:00:00+00:00", "ok", data=False)
        self.assertEqual([d for d in ("good", "bad", "nodata", "missing") if up.extract_ok(self.root, d)], ["good"])

    def run_run(self, **k):
        diffs = []
        wt = os.path.join(self.m.tmp, "wt")
        os.makedirs(wt)
        with mock.patch.object(up, "cmd_extract", return_value=0), mock.patch.object(up, "cmd_diff", side_effect=lambda a: diffs.append(a) or 0), \
                mock.patch.object(up.subprocess, "run", return_value=Namespace(returncode=0)):
            rc, out = run(up.cmd_run, self.m.args(label="new", force=True, worktree=wt, **k))
        return rc, out, diffs

    def test_run_diffs_against_the_last_good_extraction_not_a_failed_one(self):
        rc, out, diffs = self.run_run()
        self.assertEqual(rc, 0, out)
        self.assertEqual([a.old for a in diffs], ["good"])
        self.assertIn("vs good:", out)

    def baseline(self, rcb, report, stale=False):
        rep = os.path.join(self.root, "new-baseline", "regen-report.json")
        if stale:
            up.write_json(rep, {"from": "an earlier run"})
        git_calls = []

        def fake(cmd, **kw):
            if "new-baseline" in cmd:
                if report:
                    up.write_json(rep, {})
                return Namespace(returncode=rcb)
            return Namespace(returncode=0)
        wt = os.path.join(self.m.tmp, "wt")
        os.makedirs(wt, exist_ok=True)
        with mock.patch.object(up, "cmd_extract", return_value=0), mock.patch.object(up, "cmd_diff", return_value=0), \
                mock.patch.object(up.subprocess, "run", side_effect=fake), \
                mock.patch.object(up, "git", side_effect=lambda *a, **k: (git_calls.append(a), (0, ""))[1]):
            try:
                rc, out = run(up.cmd_run, self.m.args(label="new", force=True, worktree=wt, no_baseline=False))
            except SystemExit as e:
                return str(e.code), git_calls
        return rc, git_calls

    def test_the_baseline_is_committed_only_with_a_report_from_this_pass(self):
        res, calls = self.baseline(1, report=True)                       # generators failed, but regen ran and reported
        self.assertEqual(res, 0)
        self.assertIn(("commit", "-q", "-m", "Baseline: regenerate with the previous export (good); no data change"), calls)
        for rcb, stale in ((1, False), (1, True), (6, True), (5, False)):  # regen never started; a stale report must not stand in
            res, calls = self.baseline(rcb, report=False, stale=stale)
            self.assertIn("baseline regen could not run", res, (rcb, stale))
            self.assertFalse([c for c in calls if c[0] == "commit"], (rcb, stale))


class JenkinsfileBranches(unittest.TestCase):
    def test_exit_3_reads_the_status_and_exit_5_has_its_own_branch(self):
        text = read(os.path.join(ROOT, "jenkins", "patch-watch.Jenkinsfile"))
        self.assertIn("extract-meta.json", text.split("rc == 3")[1].split("rc == 5")[0])
        for needle in ("'export-shrunk'", "'usmap-stale'", "truncated export", "stale usmap", "rc == 5", "preflight", "def metaStatus"):
            self.assertIn(needle, text)
        self.assertLess(text.index("rc == 3"), text.index("rc == 5"))
        self.assertLess(text.index("rc == 5"), text.index("rc in [1, 4]"))


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
