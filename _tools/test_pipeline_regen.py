"""Tests for `update_pipeline.py regen` / `diff`: the data/ mirror, data/ reported on its own, the pinned Season 2 diff, the quick
diff's hashed-name handling, failure grouping and the hashed-name check wiring.
Run: python -I -W ignore -m unittest discover -s _tools -p test_pipeline_regen.py -v   (or: python -I _tools/test_pipeline_regen.py)

Everything runs on a small synthetic git repo (a main checkout plus a linked worktree) and synthetic exports in a temp dir.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import update_pipeline as up  # noqa: E402

HASHED_A = "_" + "abcdefghijklmnopabcde"          # 21 letters a-p after the underscore
HASHED_B = "_" + "ponmlkjihgfedcbaponml"
GEN = '''import os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = sorted(os.listdir(os.path.join(root, "data", "Wardogs", "Content")))
with open(os.path.join(root, "site", "out.md"), "w", newline="\\n") as f:
    f.write("files=%s\\nversion=2\\n" % ",".join(names))
'''
FAIL = '''import json
open("nowhere/Kenya_KOTH_01.json")
'''
FAIL_KEY = '''raise KeyError("Missing_Key")
'''


def export(name, obj):
    return "--- export: %s ---\n%s\n" % (name, json.dumps(obj, indent=1))


def put(root, rel, text):
    p = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def read(root, rel):
    with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


def git(cwd, *a):
    p = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"] + list(a), cwd=cwd, capture_output=True)
    if p.returncode:
        raise AssertionError("git %s: %s" % (" ".join(a), p.stderr.decode("utf-8", "replace")))
    return p.stdout.decode("utf-8", "replace")


def run(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*a, **k)
    return rc, buf.getvalue()


class Fixture:
    """tmp/main (a repo with tracked data/ JSON and a generator), tmp/wt (a linked worktree), tmp/old and tmp/new (exports)."""

    def __init__(self, tmp, gens=("gen.py",)):
        self.tmp = tmp
        self.main = os.path.join(tmp, "main")
        self.wt = os.path.join(tmp, "wt")
        self.report = os.path.join(tmp, "report")
        os.makedirs(self.main)
        git(self.main, "init", "-q", "-b", "main")
        put(self.main, ".gitignore", "/data/**\n!/data/**/\n!/data/**/*.json\n")
        put(self.main, ".gitattributes", "data/** -text\n")
        put(self.main, "data/Wardogs/Content/A.json", export("A", {"Value": 1, "Heights": [1, 2, 3]}))
        put(self.main, "data/Wardogs/Content/B.json", export("B", {"Value": 2}))
        put(self.main, "site/out.md", "files=A.json,B.json\nversion=1\n")          # the committed output lags the generator
        for g in gens:
            put(self.main, "_tools/" + g, GEN)
        git(self.main, "add", "-A")
        git(self.main, "commit", "-q", "-m", "init")
        git(self.main, "worktree", "add", "-q", "-b", "upd", self.wt)
        self.old = os.path.join(tmp, "old")                 # the previous export == the tracked data/ (+ an untracked config file)
        shutil.copytree(os.path.join(self.main, "data"), self.old)
        put(self.old, "Wardogs/Config/Tags.ini", "[a]\n")
        self.new = os.path.join(tmp, "new")                 # A changed, B removed, D added, config changed
        shutil.copytree(self.old, self.new)
        put(self.new, "Wardogs/Content/A.json", export("A", {"Value": 5, "Heights": [1, 2, 3]}))
        os.remove(os.path.join(self.new, "Wardogs", "Content", "B.json"))
        put(self.new, "Wardogs/Content/D.json", export("D", {"Value": 4}))
        put(self.new, "Wardogs/Config/Tags.ini", "[b]\n")
        self.s1, self.s2 = os.path.join(tmp, "s1"), os.path.join(tmp, "s2")      # the two pinned exports of season_diff.py
        for d in (self.s1, self.s2):
            put(d, "Wardogs/Content/X.json", export("X", {"v": 1}))
        self.extra = {}                                                          # more top-level registry keys

    def registry(self, scripts):
        return dict({"environment": {"builds_root": os.path.join(self.tmp, "builds"), "season2_export": self.s2, "season1_export": self.s1},
                     "scripts": scripts, "chains": []}, **self.extra)

    def gen(self, name="gen.py", **k):
        e = {"script": name, "class": "generator", "tier": "core", "write": [], "check": None, "inputs": []}
        e.update(k)
        return e

    def regen(self, data, scripts=None, repo=None, **k):
        args = Namespace(data=data, repo=repo or self.wt, label="t", report_dir=self.report, passes=1, only=None, skip="link_sources", no_assets=False,
                         allow_shrink=False, config=None)
        for key, v in k.items():
            setattr(args, key, v)
        with mock.patch.object(up, "load_registry", return_value=self.registry(scripts or [self.gen()])), mock.patch.object(up, "REPO", self.main):
            return run(up.cmd_regen, args)

    def report_md(self):
        return read(self.report, "regen-report.md")

    def report_json(self):
        return json.loads(read(self.report, "regen-report.json"))


class Base(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory(prefix="wd-regen-test-")
        self.addCleanup(self._t.cleanup)
        self.tmp = os.path.realpath(self._t.name)


class DataMirror(Base):
    def test_export_is_mirrored_into_the_worktree_data_and_reported_as_one_line(self):
        fx = Fixture(self.tmp)
        rc, out = fx.regen(fx.new)
        self.assertEqual(rc, 0, out)
        self.assertFalse(os.path.islink(os.path.join(fx.wt, "data")))
        self.assertIn('"Value": 5', read(fx.wt, "data/Wardogs/Content/A.json"))
        self.assertFalse(os.path.exists(os.path.join(fx.wt, "data", "Wardogs", "Content", "B.json")))     # absent from the export: deleted
        self.assertTrue(os.path.exists(os.path.join(fx.wt, "data", "Wardogs", "Content", "D.json")))
        self.assertEqual(read(fx.wt, "data/Wardogs/Config/Tags.ini"), "[b]\n")                              # non-JSON copied for the generators
        rep = fx.report_json()
        self.assertEqual(rep["data_changes"], {"added": 1, "removed": 1, "changed": 1})
        self.assertEqual(rep["real_changed"], ["site/out.md"])                    # no data/ file listed as a site change
        self.assertEqual(rep["shrunk"], [])
        self.assertEqual(rep["untracked"], [])
        md = fx.report_md()
        self.assertIn("data/: +1 -1 ~1 files", md)
        self.assertNotIn("data/Wardogs/Content/A.json", md)
        git(fx.wt, "add", "-A")
        tracked = git(fx.wt, "ls-files", "data").split()
        self.assertEqual(sorted(tracked), ["data/Wardogs/Content/A.json", "data/Wardogs/Content/D.json"])    # the ini is never tracked

    def test_a_shrunk_data_file_is_not_reported_as_lost_content(self):
        fx = Fixture(self.tmp)
        put(fx.new, "Wardogs/Content/A.json", export("A", {"Value": 1}))        # fewer values than HEAD
        rc, out = fx.regen(fx.new)
        self.assertEqual(fx.report_json()["shrunk"], [])
        self.assertEqual(fx.report_json()["suspicious"], [])
        self.assertEqual(fx.report_json()["data_changes"]["changed"], 1)

    def test_run_baseline_then_final_regen_commits_drift_then_data(self):
        fx = Fixture(self.tmp)
        rc, out = fx.regen(fx.old)                      # baseline on the old export (== tracked data/)
        self.assertEqual(rc, 0, out)
        self.assertEqual(fx.report_json()["data_changes"], {"added": 0, "removed": 0, "changed": 0})
        git(fx.wt, "add", "-A")
        git(fx.wt, "commit", "-q", "-m", "baseline")
        base = git(fx.wt, "show", "--name-only", "--format=", "HEAD").split()
        self.assertEqual(base, ["site/out.md"])        # generator drift only
        rc, out = fx.regen(fx.new)                      # final regen on the new export
        self.assertEqual(rc, 0, out)
        git(fx.wt, "add", "-A")
        git(fx.wt, "commit", "-q", "-m", "final")
        final = sorted(git(fx.wt, "show", "--name-only", "--format=", "HEAD").split())
        self.assertEqual(final, ["data/Wardogs/Content/A.json", "data/Wardogs/Content/B.json", "data/Wardogs/Content/D.json", "site/out.md"])
        self.assertEqual(read(fx.wt, "site/out.md"), "files=A.json,D.json\nversion=2\n")

    def test_regen_still_refuses_the_main_checkout(self):
        fx = Fixture(self.tmp)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc, out = fx.regen(fx.new, repo=fx.main)
        self.assertEqual(rc, up.REGEN_FATAL_RC)
        self.assertIn("main checkout", err.getvalue())
        self.assertIn('"Value": 1', read(fx.main, "data/Wardogs/Content/A.json"))

    def test_mirror_refuses_links_and_overlapping_trees(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        put(src, "a/x.json", "1")
        os.makedirs(dst)
        with self.assertRaises(SystemExit):
            up.mirror_tree(src, src)
        with self.assertRaises(SystemExit):
            up.mirror_tree(src, os.path.join(src, "a"))
        link = os.path.join(self.tmp, "lnk")
        up.make_link(link, src)
        try:
            with self.assertRaises(SystemExit):
                up.mirror_tree(src, link)
            self.assertTrue(os.path.exists(os.path.join(src, "a", "x.json")))
        finally:
            up.remove_link(link)

    def test_mirror_counts_and_removes_emptied_directories(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        put(src, "keep.json", "1")
        put(src, "chg.json", "2")
        put(src, "new/n.json", "3")
        put(dst, "keep.json", "1")
        put(dst, "chg.json", "old")
        put(dst, "gone/deep/g.json", "4")
        stat = up.mirror_tree(src, dst)
        self.assertEqual({k: stat[k] for k in ("added", "removed", "changed", "unchanged")}, {"added": 1, "removed": 1, "changed": 1, "unchanged": 1})
        self.assertFalse(os.path.exists(os.path.join(dst, "gone")))
        self.assertEqual(read(dst, "chg.json"), "2")

    def test_mirror_leaves_the_export_untouched(self):
        fx = Fixture(self.tmp)
        before = sorted(up._files(fx.new))
        fx.regen(fx.new)
        self.assertEqual(sorted(up._files(fx.new)), before)
        self.assertIn('"Value": 5', read(fx.new, "Wardogs/Content/A.json"))


class PinnedSeasonDiff(Base):
    def test_registry_pins_season_diff_to_the_season_2_export(self):
        reg = up.load_registry()
        self.assertIn("season2_export", reg["environment"])
        e = next(x for x in reg["scripts"] if x["script"] == "season_diff.py")
        for mode in ("write", "check"):
            self.assertEqual(e[mode][:2], ["--s2", "{season2_export}"])
        self.assertEqual(e["tier"], "core")
        sp = next(x for x in reg["scripts"] if x["script"] == "spray_patterns.py")
        self.assertEqual(sp["tier"], "manual")           # hard-codes data/ as Season 2: cannot be pinned, so regen does not run it

    def test_regen_hands_the_pinned_path_to_the_generator_not_data(self):
        reg = up.load_registry()
        e = next(x for x in reg["scripts"] if x["script"] == "season_diff.py")
        seen = []
        with mock.patch.object(up, "run_cmd", side_effect=lambda cmd, **k: seen.append(cmd) or (0, 0.0, "")):
            up.run_generator("R", e, "write", {}, {"season2_export": "E:/s2/data", "season1_export": "E:/s1/data"}, None)
            up.run_generator("R", e, "check", {}, {"season2_export": "E:/s2/data", "season1_export": "E:/s1/data"}, None)
        for cmd in seen:
            self.assertEqual(cmd[cmd.index("--s2") + 1], "E:/s2/data")
            self.assertEqual(cmd[cmd.index("--s1") + 1], "E:/s1/data")
        self.assertEqual([c[-1] for c in seen], ["--write", "--check"])

    def test_env_var_overrides_the_pin(self):
        with mock.patch.dict(os.environ, {"WD_PIPELINE_SEASON2_EXPORT": "X:/other"}):
            self.assertEqual(up.config()["season2_export"], "X:/other")

    def test_regen_passes_the_environment_pin_into_the_fills(self):
        fx = Fixture(self.tmp)
        seen = []
        orig = up.run_generator
        scripts = [fx.gen(write=["--s2", "{season2_export}"])]
        with mock.patch.object(up, "run_generator", side_effect=lambda repo, e, mode, ee, fills, log, **k: (seen.append(fills["season2_export"]), orig(repo, e, mode, ee, fills, log, **k))[1]):
            fx.regen(fx.old, scripts=scripts)
        self.assertEqual(seen[0], fx.s2)


class SeasonDiffGuard(Base):
    """A missing or empty export on either side must stop season_diff.py, not turn every asset of the other side into added/removed."""

    def season_diff(self, s1, s2, mode):
        out = os.path.join(self.tmp, "season-diff")
        p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "season_diff.py"), "--s1", s1, "--s2", s2, "--out", out, mode], capture_output=True)
        return p.returncode, p.stderr.decode("utf-8", "replace"), out

    def test_an_empty_or_missing_side_exits_non_zero_and_writes_nothing(self):
        full = os.path.join(self.tmp, "full")
        put(full, "Wardogs/Content/A.json", export("A", {"v": 1}))
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        for s1, s2, side in ((full, empty, "Season 2"), (full, "", "Season 2"), (empty, full, "Season 1"), (full, os.path.join(self.tmp, "gone"), "Season 2")):
            for mode in ("--write", "--check"):
                rc, err, out = self.season_diff(s1, s2, mode)
                self.assertNotEqual(rc, 0, (s1, s2, mode))
                self.assertIn(side, err)
                self.assertFalse(os.path.exists(out))

    def test_two_populated_sides_still_compare(self):
        a, b = os.path.join(self.tmp, "a"), os.path.join(self.tmp, "b")
        put(a, "Wardogs/Content/A.json", export("A", {"v": 1}))
        put(b, "Wardogs/Content/A.json", export("A", {"v": 2}))
        rc, err, out = self.season_diff(a, b, "--write")
        self.assertEqual(rc, 0, err)
        self.assertTrue(os.path.exists(os.path.join(out, "index.json")))


class RegenInputs(Base):
    def test_regen_names_a_missing_season_2_export_and_does_nothing(self):
        fx = Fixture(self.tmp)
        shutil.rmtree(fx.s2)
        rc, out = fx.regen(fx.new)
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertIn("season2_export", out)
        self.assertIn("WD_PIPELINE_SEASON2_EXPORT", out)
        self.assertIn('"Value": 1', read(fx.wt, "data/Wardogs/Content/A.json"))          # nothing was mirrored
        self.assertFalse(os.path.exists(os.path.join(fx.report, "regen-report.json")))

    def test_an_export_folder_without_wardogs_content_counts_as_missing(self):
        fx = Fixture(self.tmp)
        shutil.rmtree(os.path.join(fx.s1, "Wardogs"))
        rc, out = fx.regen(fx.new)
        self.assertEqual(rc, up.PREFLIGHT_RC)
        self.assertIn("season1_export", out)
        self.assertIn("no Wardogs/Content inside", out)
        self.assertNotIn("season2_export", out)

    def test_step_regen_and_run_require_both_exports(self):
        env = {"season2_export": os.path.join(self.tmp, "gone2"), "season1_export": os.path.join(self.tmp, "gone1")}
        self.assertEqual([k for k, _, _ in up.missing_inputs(env, "regen")], ["season2_export", "season1_export"])
        run_keys = [k for k, _, _ in up.missing_inputs(dict(env, builds_root=self.tmp), "run")]
        self.assertTrue({"season2_export", "season1_export"} <= set(run_keys))

    def test_a_regen_that_skips_season_diff_does_not_need_the_exports(self):
        fx = Fixture(self.tmp)
        shutil.rmtree(fx.s2)
        rc, out = fx.regen(fx.new, only="gen")
        self.assertEqual(rc, 0, out)


class MirrorSafety(Base):
    def test_a_source_far_smaller_than_the_destination_is_refused(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        for i in range(10):
            put(dst, "d/%d.json" % i, "1")
        os.makedirs(src)
        with self.assertRaises(SystemExit) as cm:                       # empty export
            up.mirror_tree(src, dst)
        self.assertIn("--allow-shrink", str(cm.exception))
        for i in range(8):                                              # 80%: still below 90%
            put(src, "d/%d.json" % i, "1")
        with self.assertRaises(SystemExit):
            up.mirror_tree(src, dst)
        self.assertEqual(len(up._files(dst)), 10)
        put(src, "d/8.json", "1")                                       # 90% passes
        up.mirror_tree(src, dst)
        self.assertEqual(len(up._files(dst)), 9)

    def test_allow_shrink_overrides_the_refusal(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        for i in range(10):
            put(dst, "%d.json" % i, "1")
        put(src, "0.json", "1")
        up.mirror_tree(src, dst, allow_shrink=True)
        self.assertEqual(sorted(up._files(dst)), ["0.json"])

    def test_non_json_files_do_not_count_toward_the_ratio(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        for i in range(10):
            put(dst, "%d.json" % i, "1")
        for i in range(30):
            put(src, "c/%d.ini" % i, "x")
        with self.assertRaises(SystemExit):
            up.mirror_tree(src, dst)

    def test_regen_with_an_empty_export_stops_with_the_fatal_code_and_keeps_data(self):
        fx = Fixture(self.tmp)
        empty = os.path.join(self.tmp, "emptyexport")
        os.makedirs(os.path.join(empty, "Wardogs", "Content"))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc, out = fx.regen(empty)
        self.assertEqual(rc, up.REGEN_FATAL_RC)
        self.assertIn("refusing to mirror", err.getvalue())
        self.assertTrue(os.path.exists(os.path.join(fx.wt, "data", "Wardogs", "Content", "A.json")))
        self.assertFalse(os.path.exists(os.path.join(fx.report, "regen-report.json")))
        rc, out = fx.regen(empty, allow_shrink=True)                    # the explicit override
        self.assertNotEqual(rc, up.REGEN_FATAL_RC)          # data/Wardogs/Content is gone, so gen.py itself fails: exit 1
        self.assertFalse(os.path.exists(os.path.join(fx.wt, "data", "Wardogs", "Content", "A.json")))

    def test_a_bad_data_dir_is_a_fatal_setup_error_not_a_generator_failure(self):
        fx = Fixture(self.tmp)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            rc, out = fx.regen(os.path.join(self.tmp, "nothing"))
        self.assertEqual(rc, up.REGEN_FATAL_RC)
        self.assertIn("does not look like a data export", err.getvalue())
        rc, out = fx.regen(fx.old, scripts=[fx.gen("fail.py")])        # a failing generator is still exit 1
        self.assertEqual(rc, 1)

    def test_a_worktree_of_another_repository_is_refused(self):
        fx = Fixture(self.tmp)
        other = os.path.join(self.tmp, "other")
        os.makedirs(other)
        git(other, "init", "-q", "-b", "main")
        put(other, "data/Wardogs/Content/A.json", export("A", {"Value": 1}))
        git(other, "add", "-A")
        git(other, "commit", "-q", "-m", "init")
        owt = os.path.join(self.tmp, "other-wt")
        git(other, "worktree", "add", "-q", "-b", "upd", owt)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc, out = fx.regen(fx.new, repo=owt)
        self.assertEqual(rc, up.REGEN_FATAL_RC)
        self.assertIn("not a worktree of the repository", err.getvalue())
        self.assertIn('"Value": 1', read(owt, "data/Wardogs/Content/A.json"))

    def test_mirror_never_writes_through_a_link_inside_the_destination(self):
        src, dst, outside = (os.path.join(self.tmp, n) for n in ("src", "dst", "outside"))
        put(src, "sub/x.json", "1")
        put(src, "keep.json", "1")
        put(dst, "keep.json", "1")
        os.makedirs(outside)
        up.make_link(os.path.join(dst, "sub"), outside)
        try:
            with self.assertRaises(SystemExit) as cm:
                up.mirror_tree(src, dst)
            self.assertIn("outside", str(cm.exception))
            self.assertEqual(os.listdir(outside), [])
        finally:
            up.remove_link(os.path.join(dst, "sub"))


class MirrorReporting(Base):
    def test_json_counts_are_apart_from_the_raw_copy_counts_and_case_renames_are_reported(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        put(src, "Audio/WAVs/a.json", "1")
        put(src, "Config/x.ini", "[a]")
        put(src, "Config/y.ini", "[a]")
        put(src, "k.json", "same")
        put(dst, "Audio/Wavs/a.json", "1")
        put(dst, "k.json", "same")
        m = up.mirror_tree(src, dst)
        self.assertEqual((m["json_added"], m["json_removed"], m["json_changed"], m["json_unchanged"]), (1, 1, 0, 1))
        self.assertEqual((m["added"], m["removed"], m["changed"], m["unchanged"]), (3, 1, 0, 1))
        self.assertEqual(m["case_renames"], 1)
        text = "\n".join(up.mirror_report("D", m, 1.0))
        self.assertIn("tracked JSON (what git will see): +1 -1 ~0, 1 identical", text)
        self.assertIn("raw copy", text)
        self.assertIn("+3 -1 ~0", text)
        self.assertIn("1 file(s) differ from data/ only by letter case", text)
        self.assertIn("core.ignorecase=false", text)

    def test_no_case_note_without_case_renames(self):
        src, dst = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "dst")
        put(src, "a.json", "1")
        put(dst, "b.json", "1")
        m = up.mirror_tree(src, dst, allow_shrink=True)
        self.assertEqual(m["case_renames"], 0)
        self.assertNotIn("letter case", "\n".join(up.mirror_report("D", m, 1.0)))

    def test_regen_prints_the_json_line(self):
        fx = Fixture(self.tmp)
        rc, out = fx.regen(fx.new)
        self.assertEqual(rc, 0, out)
        self.assertIn("tracked JSON (what git will see): +1 -1 ~1, 0 identical", out)
        self.assertIn("raw copy (every file", out)

    def test_new_directories_are_counted_file_by_file(self):
        fx = Fixture(self.tmp)
        for i in range(3):
            put(fx.old, "Wardogs/Content/NewDir/%d.json" % i, export("N", {"v": i}))
        rc, out = fx.regen(fx.old)
        self.assertEqual(rc, 0, out)
        self.assertEqual(fx.report_json()["data_changes"], {"added": 3, "removed": 0, "changed": 0})
        self.assertEqual(up.data_changes(fx.wt)["added"], 3)


class HashedAllowlist(Base):
    CHECKER = '''import sys
print("bp.py:12 %s")
print("bp.py:40 %s")
print("new.py:7 %s")
print("3 hashed names hard-coded in scripts are missing from the export")
sys.exit(1)
''' % (HASHED_A, HASHED_B, HASHED_A)

    def fx(self):
        fx = Fixture(self.tmp)
        put(fx.wt, "_tools/hashed_names_check.py", self.CHECKER)
        fx.extra["hashed_names_expected_missing"] = {"names": [{"script": "bp.py", "name": HASHED_A, "reason": "Blueprint dump"},
                                                                 {"script": "bp.py", "name": HASHED_B, "reason": "Blueprint dump"}]}
        return fx

    def test_only_new_misses_are_listed_and_the_allowlisted_count_is_still_shown(self):
        fx = self.fx()
        rc, out = fx.regen(fx.old)
        self.assertEqual(rc, 0, out)
        self.assertIn("hard-coded hashed names missing from this export: 1 (+2 expected, allowlisted in the registry)", out)
        self.assertEqual(fx.report_json()["hashed_names_missing"], [["new.py:7", HASHED_A]])       # same name, other script: still new
        self.assertEqual(fx.report_json()["hashed_names_expected"], [["bp.py:12", HASHED_A], ["bp.py:40", HASHED_B]])
        md = fx.report_md()
        self.assertIn("- `new.py:7` `%s`" % HASHED_A, md)
        self.assertNotIn("- `bp.py:12`", md)
        self.assertIn("Expected misses", md)
        self.assertIn("- `bp.py`: 2 (Blueprint dump)", md)

    def test_the_shipped_allowlist_covers_every_miss_of_the_season_2_export(self):
        reg = up.load_registry()
        names = reg["hashed_names_expected_missing"]["names"]
        self.assertEqual(len(names), 14)
        for x in names:
            self.assertTrue(x["reason"])
        hn = up.hashed_names_missing(ROOT, os.path.join(ROOT, "data"), self.tmp, {(x["script"], x["name"]) for x in names})
        self.assertEqual(hn["missing"], [])
        self.assertEqual(len(hn["expected"]), 14)


class QuickDiff(Base):
    def tree(self, old, new):
        o, n = os.path.join(self.tmp, "o"), os.path.join(self.tmp, "n")
        for root, files in ((o, old), (n, new)):
            for rel, text in files.items():
                put(root, rel, text)
        return o, n

    def diff(self, old, new):
        o, n = self.tree(old, new)
        added, removed, changed, areas = up.diff_trees(o, n, [])
        return {c["file"]: c for c in changed}, areas

    def test_hashed_rename_with_the_same_value_pairs_and_is_rename_only(self):
        ch, _ = self.diff({"R.json": export("R", {HASHED_A: {"x": 1.5}, "Other": 3})}, {"R.json": export("R", {"Named": {"x": 1.5}, "Other": 3})})
        self.assertEqual(ch["R.json"]["kind"], "rename_only")
        self.assertEqual(ch["R.json"]["nchanges"], 0)
        self.assertEqual(ch["R.json"]["hashed_names"], {HASHED_A})

    def test_same_value_pairing_needs_a_hashed_side_and_the_same_value(self):
        ch, _ = self.diff({"N.json": export("N", {"Old": 1})}, {"N.json": export("N", {"New": 1})})                  # named -> named: a real change
        self.assertEqual(ch["N.json"]["nchanges"], 2)
        ch, _ = self.diff({"V.json": export("V", {HASHED_A: 1})}, {"V.json": export("V", {"Named": 2})})             # different value
        self.assertEqual(ch["V.json"]["kind"], "values")
        self.assertEqual(ch["V.json"]["nchanges"], 1)                                                                # the named field is new; the hashed one is noise

    def test_rename_only_file_is_not_counted_as_changed_values(self):
        ch, areas = self.diff({"R.json": export("R", {HASHED_A: 1}), "V.json": export("V", {"v": 1})},
                              {"R.json": export("R", {"Named": 1}), "V.json": export("V", {"v": 2})})
        self.assertEqual({k: c["kind"] for k, c in ch.items()}, {"R.json": "rename_only", "V.json": "values"})
        self.assertEqual(sum(a["changed"] for a in areas.values()), 1)
        self.assertEqual(sum(a["renamed_files"] for a in areas.values()), 1)

    def test_fields_are_distinct_with_array_indices_collapsed(self):
        old = {"H.json": export("H", {"Heights": list(range(100)), "Scale": 1})}
        new = {"H.json": export("H", {"Heights": [x + 1 for x in range(100)], "Scale": 2})}
        ch, areas = self.diff(old, new)
        self.assertEqual(ch["H.json"]["nchanges"], 2)                         # not 101 leaves
        self.assertEqual(sorted(ch["H.json"]["fields"]), ["Heights", "Scale"])
        self.assertEqual(ch["H.json"]["fields"]["Heights"], 1)

    def test_assets_rank_by_distinct_fields_not_leaf_counts(self):
        old = {"Big.json": export("Big", {"Heights": list(range(500))}), "Few.json": export("Few", {"a": 1, "b": 1, "c": 1})}
        new = {"Big.json": export("Big", {"Heights": list(range(1, 501))}), "Few.json": export("Few", {"a": 2, "b": 2, "c": 2})}
        ch, _ = self.diff(old, new)
        self.assertGreater(ch["Few.json"]["nchanges"], ch["Big.json"]["nchanges"])

    def test_hashed_names_are_counted_distinct_not_per_leaf(self):
        old = {"H.json": export("H", {HASHED_A: {"a": 1, "b": 2, "c": 3}})}
        new = {"H.json": export("H", {"Other": 9, HASHED_B: [1, 2, 3, 4]})}
        ch, areas = self.diff(old, new)
        self.assertEqual(ch["H.json"]["hashed_names"], {HASHED_A, HASHED_B})
        self.assertEqual(sum(len(a["hashed_names"]) for a in areas.values()), 2)

    def test_unparseable_file_is_listed_apart_not_as_a_change(self):
        good = export("T", {"a": 1})
        ch, _ = self.diff({"T.json": good, "U.json": good}, {"T.json": good[:-12], "U.json": export("U", {"a": 1})})
        self.assertEqual(ch["T.json"]["kind"], "unparseable")
        self.assertEqual(ch["T.json"]["nchanges"], 0)
        self.assertEqual(ch["T.json"]["unparseable"], ["new: T"])
        bad = []
        up.split_exports(good[:-12], bad)
        self.assertEqual(bad, ["T"])

    def test_cmd_diff_reports_each_kind_in_its_own_place(self):
        o, n = self.tree({"R.json": export("R", {HASHED_A: 1}), "V.json": export("V", {"v": 1}), "T.json": export("T", {"a": 1})},
                         {"R.json": export("R", {"Named": 1}), "V.json": export("V", {"v": 2}), "T.json": export("T", {"a": 1})[:-6]})
        out = os.path.join(self.tmp, "out")
        args = Namespace(old=o, new=n, out=out, full=False, config=None)
        with mock.patch.object(up, "run_cmd", return_value=(0, 0.0, "")), mock.patch.object(up, "load_area_rules", return_value=[]):
            rc, stdout = run(up.cmd_diff, args)
        self.assertEqual(rc, 0)
        j = json.loads(read(out, "patch-diff.json"))
        self.assertEqual([c["file"] for c in j["changed"]], ["V.json"])
        self.assertEqual(j["rename_only_changed"], ["R.json"])
        self.assertEqual([u["file"] for u in j["unparseable"]], ["T.json"])
        self.assertEqual(j["hashed_property_names"], 1)
        md = read(out, "patch-diff.md")
        self.assertIn("| Changed values | 1 |", md)
        self.assertIn("| Renamed hashed property names only (no value changed) | 1 |", md)
        self.assertIn("## Unparseable or truncated files", md)
        self.assertIn("1 distinct hashed property names", md)


class FailureGroups(Base):
    def test_signatures(self):
        tb = "Traceback (most recent call last):\n  File \"x.py\", line 3\nFileNotFoundError: [Errno 2] No such file or directory: 'E:\\\\a\\\\b\\\\Kenya_KOTH_01.json'\n"
        self.assertEqual(up.error_signature(tb), "FileNotFoundError .../Kenya_KOTH_01.json")
        self.assertEqual(up.error_signature("KeyError: 'Foo'"), "KeyError Foo")
        self.assertEqual(up.error_signature("no exception here\nSeason 1 folder not found"), "exit: Season N folder not found")
        a, b = "content/A_v1.md: 9 tables, stale", "game-features/B_v1.md: 33 tables, stale"        # --check lines: one group per cause
        self.assertEqual(up.error_signature(a), up.error_signature(b))
        self.assertEqual(up.group_failures([("a.py", a), ("b.py", b), ("c.py", "KeyError: 'k'")]),
                         [("exit: <file>: N tables, stale", ["a.py", "b.py"]), ("KeyError k", ["c.py"])])
        self.assertEqual(up.error_signature(""), "(no output)")

    def test_failures_are_grouped_by_signature_then_listed_per_script(self):
        names = ["f1.py", "f2.py", "f3.py", "k1.py"]
        fx = Fixture(self.tmp, gens=["gen.py"])
        for n in names[:3]:
            put(fx.main, "_tools/" + n, FAIL)
        put(fx.main, "_tools/k1.py", FAIL_KEY)
        git(fx.main, "add", "-A")
        git(fx.main, "commit", "-q", "-m", "fails")
        git(fx.wt, "merge", "-q", "main")
        rc, out = fx.regen(fx.old, scripts=[fx.gen(n) for n in names + ["gen.py"]])
        self.assertEqual(rc, 1)
        md = fx.report_md()
        self.assertIn("- 3 scripts: FileNotFoundError `.../Kenya_KOTH_01.json`", md)
        self.assertIn("- 1 script: KeyError `Missing_Key`", md)
        self.assertLess(md.index("3 scripts: FileNotFoundError"), md.index("Per script:"))
        self.assertIn("- `f2.py` rc=1:", md)
        self.assertEqual(sorted(fx.report_json()["failure_groups"]["FileNotFoundError .../Kenya_KOTH_01.json"]), ["f1.py", "f2.py", "f3.py"])


class HashedNamesWiring(Base):
    CHECKER = '''import sys
print("some_script.py:12 %s")
print("other.py:7 %s")
print("2 hashed names hard-coded in scripts are missing from the export")
sys.exit(1)
''' % (HASHED_A, HASHED_B)

    def test_missing_names_are_reported_before_the_generators_and_do_not_stop_regen(self):
        fx = Fixture(self.tmp)
        put(fx.wt, "_tools/hashed_names_check.py", self.CHECKER)
        rc, out = fx.regen(fx.old)
        self.assertEqual(rc, 0, out)
        self.assertIn("hard-coded hashed names missing from this export: 2", out)
        self.assertLess(out.index("hard-coded hashed names"), out.index("--- pass 1"))
        md = fx.report_md()
        self.assertIn("hard-coded hashed names missing from this export: 2", md)
        self.assertIn("- `some_script.py:12` `%s`" % HASHED_A, md)
        self.assertEqual(fx.report_json()["hashed_names_missing"], [["some_script.py:12", HASHED_A], ["other.py:7", HASHED_B]])

    def test_checker_is_passed_the_export_and_a_json_path(self):
        fx = Fixture(self.tmp)
        put(fx.wt, "_tools/hashed_names_check.py", "import sys\nopen(sys.argv[-1] + '.args', 'w').write(' '.join(sys.argv[1:]))\n")
        fx.regen(fx.old)
        args = read(fx.report, "hashed-names.json.args").split()
        self.assertEqual(args[0:2], ["--data", fx.old])
        self.assertEqual(args[2], "--json")
        self.assertIn("hard-coded hashed names missing from this export: 0", fx.report_md())

    def test_absent_checker_is_skipped(self):
        fx = Fixture(self.tmp)
        rc, out = fx.regen(fx.old)
        self.assertEqual(rc, 0)
        self.assertNotIn("hashed names missing", out)
        self.assertIsNone(fx.report_json()["hashed_names_missing"])


if __name__ == "__main__":
    unittest.main()
