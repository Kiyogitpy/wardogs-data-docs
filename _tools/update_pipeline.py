"""Patch-update pipeline: turn a new Wardogs build into refreshed site data.

    python -I _tools/update_pipeline.py snapshot [--label L]        manifest of the installed paks -> <root>/L/manifest.json
    python -I _tools/update_pipeline.py status   [--against L]      is a new build installed? (compares with the last manifest)
    python -I _tools/update_pipeline.py extract  --label L [--assets]   CueDump + WdExtract passes -> <root>/L/{data,wdextract}
    python -I _tools/update_pipeline.py diff     --old A --new B    patch-diff.md / patch-diff.json in <root>/B
    python -I _tools/update_pipeline.py regen    --data DIR         run every generator against DIR, then the checks, then report
    python -I _tools/update_pipeline.py run      --label L          snapshot -> extract -> diff -> regen in a dedicated worktree
    python -I _tools/update_pipeline.py audit                       every _tools script is classified in pipeline_registry.json

Standard library only. The game is never run and nothing is downloaded. The AES key is read from its file by the
extractor and is never printed or copied. The pipeline cannot make a usmap: when the extraction shows the usmap is stale
it stops and tells you to regenerate it with Dumper-7 (docs/UPDATE_PIPELINE.md). `regen` and `run` refuse to work in the
main checkout: they swap the worktree's data/ junction, which must never happen there.
"""
import argparse
import collections
import concurrent.futures
import datetime
import fnmatch
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REGISTRY = os.path.join(HERE, "pipeline_registry.json")
HEADER = re.compile(r"^--- export: (.*?) ---\r?\n", re.M)
HASHED = re.compile(r"_[a-p]{21}")
NOISE_LINES = ("\"source_data_tree\":",)           # lines a regen rewrites without meaning (git tree id of an untracked data/)
SUSPECT = ("not yet known", "not decoded", "not traced", "unresolved", "Not yet known")
EOL = "\n"


# ------------------------------------------------------------------------------------------------ helpers
def load_registry():
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def config(args=None):
    """Environment: registry defaults < WD_PIPELINE_<KEY> environment variables < --config JSON file."""
    reg = load_registry()
    env = dict(reg["environment"])
    for k in env:
        v = os.environ.get("WD_PIPELINE_" + k.upper())
        if v:
            env[k] = v
    path = getattr(args, "config", None) if args else None
    if path:
        with open(path, encoding="utf-8") as f:
            env.update(json.load(f))
    return env


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def say(msg=""):
    print(msg, flush=True)


def sha256_file(path, limit=None, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        left = limit
        while True:
            n = chunk if left is None else min(chunk, left)
            if n <= 0:
                break
            b = f.read(n)
            if not b:
                break
            h.update(b)
            if left is not None:
                left -= len(b)
    return h.hexdigest()


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, sort_keys=False)
        f.write("\n")


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def run_cmd(cmd, cwd=None, log=None, timeout=None, env=None, echo=False):
    """Run a command, capture combined output (to `log` if given). Returns (rc, seconds, tail)."""
    t = time.time()
    e = dict(os.environ)
    if env:
        e.update(env)
    try:
        p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, timeout=timeout)
        out = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
        rc = p.returncode
    except subprocess.TimeoutExpired as ex:
        out = ((ex.stdout or b"").decode("utf-8", "replace") if ex.stdout else "") + "\nTIMEOUT after %ss" % timeout
        rc = 124
    except FileNotFoundError as ex:
        out, rc = "not found: %s" % ex, 127
    if log:
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "a", encoding="utf-8", newline="\n") as f:
            f.write("$ %s\n%s\n" % (" ".join(map(str, cmd)), out))
    if echo:
        say(out.rstrip()[-2000:])
    return rc, round(time.time() - t, 1), out[-1500:]


def git(*a, cwd=None, check=False):
    p = subprocess.run(["git"] + list(a), cwd=cwd or REPO, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    if check and p.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(a), p.stderr.decode("utf-8", "replace")))
    return p.returncode, out


def is_main_checkout(repo):
    """True when `repo` is the main working tree (not a linked worktree)."""
    _, gd = git("rev-parse", "--absolute-git-dir", cwd=repo)
    _, cd = git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=repo)
    return os.path.normcase(os.path.normpath(gd.strip())) == os.path.normcase(os.path.normpath(cd.strip()))


def is_link(p):
    return os.path.islink(p) or (hasattr(os.path, "isjunction") and os.path.isjunction(p))


def link_target(p):
    try:
        return os.path.realpath(p)
    except OSError:
        return None


def remove_link(p):
    """Remove a junction/symlink WITHOUT touching its target. Refuses anything that is a real directory."""
    if not (os.path.lexists(p) and is_link(p)):
        raise SystemExit("refusing to remove %s: not a link" % p)
    try:
        os.rmdir(p)           # a junction or directory symlink: removes the link only
    except OSError:
        os.unlink(p)


def make_link(p, target):
    target = os.path.normpath(target)
    if os.name == "nt":
        rc = subprocess.run(["cmd", "/c", "mklink", "/J", os.path.normpath(p), target], capture_output=True)
        if rc.returncode:
            raise SystemExit("mklink failed: %s" % rc.stdout.decode("utf-8", "replace"))
    else:
        os.symlink(target, p, target_is_directory=True)


class LinkSwap:
    """Point `path` (a junction) at `target` for the duration of a block, then put it back."""

    def __init__(self, path, target):
        self.path, self.target = path, target
        self.old = None
        self.had = False

    def __enter__(self):
        if os.path.lexists(self.path):
            self.had = True
            if not is_link(self.path):
                raise SystemExit("%s is a real directory, not a junction; refusing to replace it" % self.path)
            self.old = link_target(self.path)
            remove_link(self.path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        make_link(self.path, self.target)
        return self

    def __exit__(self, *exc):
        if os.path.lexists(self.path) and is_link(self.path):
            remove_link(self.path)
        if self.had and self.old and os.path.isdir(self.old):
            make_link(self.path, self.old)
        return False


def exe_paths(env):
    return env["wdextract_exe"], env["paks"], env["aes_key_file"], env["usmap_wdextract"], env["oo2core"]


def wdextract(env, out, mode_args, log=None, timeout=1800):
    exe, paks, key, usmap, oo2 = exe_paths(env)
    os.makedirs(out, exist_ok=True)
    return run_cmd([exe, paks, key, usmap, out, oo2] + list(mode_args), log=log, timeout=timeout)


# ------------------------------------------------------------------------------------------------ snapshot / status
def steam_info(env):
    p = env.get("steam_manifest")
    info = {}
    if p and os.path.exists(p):
        txt = open(p, encoding="utf-8", errors="replace").read()
        for k in ("buildid", "LastUpdated", "name"):
            m = re.search(r'"%s"\s+"([^"]*)"' % k, txt)
            if m:
                info[k] = m.group(1)
    return info


def build_manifest(env, label, quick=False):
    paks = env["paks"]
    names = sorted(n for n in os.listdir(paks) if os.path.isfile(os.path.join(paks, n))
                   and os.path.splitext(n)[1].lower() in (".pak", ".sig", ".utoc", ".ucas", ".dll"))   # not the stray *_classes.txt notes
    big = (".ucas",)
    full = (".utoc", ".pak", ".sig", ".dll")

    def one(n):
        p = os.path.join(paks, n)
        st = os.stat(p)
        e = {"name": n, "size": st.st_size, "mtime": int(st.st_mtime)}
        ext = os.path.splitext(n)[1].lower()
        if quick:
            e["hash"] = None
        elif ext in big:
            # 20 GB containers: size plus the first and last 4 MiB (a patched container changes its size or its TOC ends)
            h = hashlib.sha256()
            with open(p, "rb") as f:
                h.update(f.read(4 << 20))
                if st.st_size > (8 << 20):
                    f.seek(-(4 << 20), os.SEEK_END)
                    h.update(f.read(4 << 20))
            e["hash"], e["hash_kind"] = h.hexdigest(), "sample(first+last 4MiB)"
        elif ext in full:
            e["hash"], e["hash_kind"] = sha256_file(p), "sha256"
        return e

    t = time.time()
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        files = list(ex.map(one, names))
    h = hashlib.sha256()
    for e in files:
        h.update(("%s|%d|%s\n" % (e["name"], e["size"], e.get("hash") or "")).encode())
    return {"label": label, "created": now(), "paks_dir": paks, "files": files, "fingerprint": h.hexdigest(),
            "file_count": len(files), "total_bytes": sum(e["size"] for e in files), "steam": steam_info(env),
            "usmap_cuedump": {"path": env["usmap_cuedump"], "sha256": sha256_file(env["usmap_cuedump"]) if os.path.exists(env["usmap_cuedump"]) else None},
            "seconds": round(time.time() - t, 1), "quick": quick}


def manifests(root):
    out = []
    if os.path.isdir(root):
        for d in sorted(os.listdir(root)):
            p = os.path.join(root, d, "manifest.json")
            if os.path.exists(p):
                m = read_json(p)
                out.append((m.get("created", ""), d, m))
    out.sort()
    return out


def compare_manifests(a, b):
    fa = {e["name"]: e for e in a["files"]}
    fb = {e["name"]: e for e in b["files"]}
    added = sorted(set(fb) - set(fa))
    removed = sorted(set(fa) - set(fb))
    changed = []
    for n in sorted(set(fa) & set(fb)):
        x, y = fa[n], fb[n]
        if x["size"] != y["size"] or (x.get("hash") and y.get("hash") and x["hash"] != y["hash"]):
            changed.append(n)
    return added, removed, changed


def cmd_snapshot(args):
    env = config(args)
    label = args.label or datetime.date.today().isoformat()
    m = build_manifest(env, label, quick=args.quick)
    path = os.path.join(env["builds_root"], label, "manifest.json")
    write_json(path, m)
    say("snapshot %s: %d files, %.1f GB, fingerprint %s (%.1fs)" % (label, m["file_count"], m["total_bytes"] / 1e9, m["fingerprint"][:16], m["seconds"]))
    if m["steam"]:
        say("steam: %s" % json.dumps(m["steam"]))
    say("wrote " + path)
    return 0


def cmd_status(args):
    env = config(args)
    ms = manifests(env["builds_root"])
    if args.against:
        prev = [m for _, d, m in ms if d == args.against]
        if not prev:
            raise SystemExit("no manifest for label %s under %s" % (args.against, env["builds_root"]))
        prev = prev[0]
    elif ms:
        prev = ms[-1][2]
    else:
        say("no manifest under %s yet: run `snapshot --label <name>` for the build you have analysed." % env["builds_root"])
        return 0
    cur = build_manifest(env, "current", quick=args.quick)
    added, removed, changed = compare_manifests(prev, cur)
    say("last manifest: %s (%s)   current paks: %d files" % (prev["label"], prev["created"], cur["file_count"]))
    sp, sc = prev.get("steam", {}), cur.get("steam", {})
    if sp or sc:
        say("steam buildid: %s -> %s" % (sp.get("buildid"), sc.get("buildid")))
    if not (added or removed or changed) and sp.get("buildid") == sc.get("buildid"):
        say("NO NEW BUILD: the installed paks match the manifest.")
        return 0
    say("NEW BUILD INSTALLED: %d added, %d removed, %d changed container/signature files" % (len(added), len(removed), len(changed)))
    for tag, lst in (("added", added), ("removed", removed), ("changed", changed)):
        for n in lst[:12]:
            say("  %-8s %s" % (tag, n))
        if len(lst) > 12:
            say("  ... %d more %s" % (len(lst) - 12, tag))
    say("")
    say("Next: python -I _tools/update_pipeline.py run --label <new-label>   (or: snapshot, extract, diff, regen)")
    say("The usmap is NOT refreshed by the pipeline. If extract reports a stale usmap, regenerate it with Dumper-7.")
    return 10


# ------------------------------------------------------------------------------------------------ extract
STALE_MSG = """
================================================================================
USMAP IS STALE (or the pak format changed): the extraction does not match the baseline.
  {why}
The pipeline cannot fix this and does not run the game. Do this yourself:
  1. Start the NEW game build with Dumper-7 injected ({dumper}); it writes a .usmap
     (and the SDK) under its output folder.
  2. Deobfuscate/restore names the way mappings/README.md describes (WdExtract deobfuscate ...)
     and save the result, then point the pipeline at it:
       set WD_PIPELINE_USMAP_CUEDUMP=<new export usmap>   (or edit _tools/pipeline_registry.json)
       set WD_PIPELINE_USMAP_WDEXTRACT=<new normal-order usmap>
  3. Re-run:  python -I _tools/update_pipeline.py extract --label {label}
  Update `baseline` in _tools/pipeline_registry.json once the new usmap reads cleanly.
The data written to {data} is KEPT for inspection but must not be used for the site.
================================================================================
"""


def parse_progress(log_path):
    res = {"warnings": 0, "errors": 0, "done": None, "samples": []}
    if not os.path.exists(log_path):
        return res
    with open(log_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("WARN ["):
                res["warnings"] += 1
                if len(res["samples"]) < 8:
                    res["samples"].append(line.strip()[:240])
            elif line.startswith("ERROR ["):
                res["errors"] += 1
                if len(res["samples"]) < 8:
                    res["samples"].append(line.strip()[:240])
            elif line.startswith("DONE."):
                res["done"] = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", line)}
    return res


def ensure_cuedump(env, bin_dir):
    exe = os.path.join(bin_dir, "CueDump.exe" if os.name == "nt" else "CueDump")
    src = os.path.join(REPO, "tools", "cuedump", "Program.cs")
    if os.path.exists(exe) and os.path.getmtime(exe) >= os.path.getmtime(src):
        return exe
    say("building tools/cuedump (CUE4Parse at %s) ..." % env["cue4parse_project"])
    rc, secs, out = run_cmd(["dotnet", "build", os.path.join(REPO, "tools", "cuedump"), "-c", "Release",
                             "-p:CUE4ParseProject=" + env["cue4parse_project"], "-o", bin_dir], timeout=900)
    if rc or not os.path.exists(exe):
        raise SystemExit("cuedump build failed:\n" + out)
    return exe


def hashed_tokens(data_dir):
    toks = set()
    for dp, _, fn in os.walk(data_dir):
        for f in fn:
            if f.endswith(".json"):
                with open(os.path.join(dp, f), encoding="utf-8", errors="replace") as fh:
                    toks.update(HASHED.findall(fh.read()))
    return toks


def copy_config(env, label_dir, raw_dir, data_dir, reg):
    """Copy the curated config/plugin files from the raw WdExtract copy into data/. Returns (copied, new_unlisted)."""
    keep = reg["config_keep"]
    copied, rels = [], []
    for dp, _, fn in os.walk(raw_dir):
        for f in fn:
            rels.append(os.path.relpath(os.path.join(dp, f), raw_dir).replace("\\", "/"))
    files = set(keep["files"])
    for rel in sorted(rels):
        ok = rel in files or any(rel.startswith(t) for t in keep["trees"])
        if ok and any(rel.startswith(x) for x in keep["exclude"]):
            ok = False
        if ok:
            dst = os.path.join(data_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(raw_dir, rel), dst)
            copied.append(rel)
    missing = sorted(files - set(copied))
    return copied, missing


def cmd_extract(args):
    env = config(args)
    reg = load_registry()
    label = args.label
    ldir = os.path.join(env["builds_root"], label)
    data = os.path.join(ldir, "data")
    wdx = os.path.join(ldir, "wdextract")
    log = os.path.join(ldir, "extract.log")
    meta = {"label": label, "started": now(), "steps": {}, "status": "running"}
    os.makedirs(ldir, exist_ok=True)
    if os.path.exists(data) and not args.force:
        raise SystemExit("%s exists: pass --force to overwrite (a full extraction is ~80 s)" % data)
    if os.path.exists(data):
        shutil.rmtree(data)
    if not os.path.exists(os.path.join(ldir, "manifest.json")):
        say("no manifest for %s yet: taking one" % label)
        write_json(os.path.join(ldir, "manifest.json"), build_manifest(env, label, quick=True))
    for k in ("paks", "aes_key_file", "usmap_cuedump", "usmap_wdextract", "wdextract_exe"):
        if not os.path.exists(env[k]):
            raise SystemExit("missing input %s = %s (override with WD_PIPELINE_%s or --config)" % (k, env[k], k.upper()))
    cd = ensure_cuedump(env, os.path.join(env["builds_root"], "_bin", "cuedump"))

    # 1. CueDump -> data/
    say("CueDump -> %s" % data)
    t = time.time()
    rc, secs, out = run_cmd([cd, env["paks"], env["aes_key_file"], env["usmap_cuedump"], data], log=log, timeout=7200)
    prog = parse_progress(data + "_progress.log")
    meta["steps"]["cuedump"] = {"rc": rc, "seconds": secs, "progress": prog}
    base = reg["baseline"]
    why = []
    if rc:
        why.append("CueDump exited %d: %s" % (rc, out.strip().splitlines()[-1] if out.strip() else ""))
    if prog["warnings"] > base["cuedump_warnings"]:
        why.append("%d CUE4Parse warnings (baseline %d); first: %s" % (prog["warnings"], base["cuedump_warnings"], prog["samples"][0] if prog["samples"] else ""))
    if prog["errors"] > base["cuedump_errored"]:
        why.append("%d packages errored (baseline %d)" % (prog["errors"], base["cuedump_errored"]))
    if prog["done"] is None:
        why.append("the progress log has no DONE line")
    say("CueDump: rc=%d %.0fs  %s  warnings=%d errors=%d" % (rc, secs, prog["done"], prog["warnings"], prog["errors"]))
    ntok = hashed_tokens(data) if os.path.isdir(data) else set()
    meta["hashed_tokens"] = len(ntok)
    prev = [d for _, d, m in manifests(env["builds_root"]) if d != label and os.path.isdir(os.path.join(env["builds_root"], d, "data"))]
    if prev:
        old = hashed_tokens(os.path.join(env["builds_root"], prev[-1], "data"))
        newt = len(ntok - old)
        meta["hashed_tokens_new_vs_" + prev[-1]] = newt
        say("hashed property names: %d distinct, %d not present in %s" % (len(ntok), newt, prev[-1]))
        if newt:
            say("  (new unnamed properties: new fields in the patch; names come from Dumper-7 + `WdExtract deobfuscate`)")
    if why:
        meta["status"] = "usmap-stale"
        meta["why"] = why
        write_json(os.path.join(ldir, "extract-meta.json"), meta)
        say(STALE_MSG.format(why="\n  ".join(why), dumper=env["dumper7_dir"], label=label, data=data))
        return 3

    # 2. raw config -> data/
    raw = os.path.join(wdx, "config")
    for mode in (["rawfiles", "Wardogs/Config", "--copy"], ["rawfiles", ".uplugin", "--copy"], ["rawfiles", "/Config/", "--copy"]):
        rc, secs, out = wdextract(env, raw, mode, log=log)
        meta["steps"]["rawfiles " + mode[1]] = {"rc": rc, "seconds": secs}
        if rc:
            say("WdExtract %s failed (rc=%d), see %s" % (mode[1], rc, log))
    rawroot = os.path.join(raw, "raw")
    copied, missing = copy_config(env, ldir, rawroot, data, reg)
    meta["config_copied"] = len(copied)
    meta["config_missing_in_paks"] = missing
    say("config: %d files copied into data/ (%d listed files absent from this build)" % (len(copied), len(missing)))
    for m in missing:
        say("  absent: " + m)
    gi = os.path.join(rawroot, "Wardogs", "Config", "DefaultGame.ini")
    if os.path.exists(gi):
        spec = importlib.util.spec_from_file_location("default_game_ini", os.path.join(HERE, "default_game_ini.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.EXCERPT = os.path.join(data, "Wardogs", "Config", "DefaultGame.excerpt.ini")
        os.makedirs(os.path.dirname(mod.EXCERPT), exist_ok=True)
        mod.extract(gi)
        say("config: DefaultGame.excerpt.ini rebuilt from the whitelist (the full DefaultGame.ini stays under %s, never commit it)" % raw)
    else:
        say("WARNING: no Wardogs/Config/DefaultGame.ini in the paks; excerpt not written")
    listed = set(rel for rel in
                 (os.path.relpath(os.path.join(dp, f), rawroot).replace("\\", "/") for dp, _, fn in os.walk(rawroot) for f in fn)
                 if rel.startswith("Wardogs/") and (rel.startswith("Wardogs/Config/") or "/Config/" in rel) and rel not in set(copied))
    meta["config_not_copied"] = len(listed)

    # 3. WdExtract passes
    files_txt = os.path.join(wdx, "files", "files.txt")
    for p in reg["passes"]:
        if p["tier"] != "core" and not args.assets:
            continue
        name = p["name"]
        if name == "files":
            rc, secs, _ = wdextract(env, os.path.join(wdx, "files"), p["wdextract"], log=log)
        elif name == "ge":
            gdir = os.path.join(wdx, "ge")
            rc, secs, _ = wdextract(env, gdir, p["wdextract"], log=log)
            if not rc:
                rc2, s2, _ = wdextract(env, os.path.join(gdir, "dump"), ["dump", os.path.join(gdir, "files.txt")], log=log)
                os.makedirs(os.path.join(gdir, "out"), exist_ok=True)
                rc3, s3, _ = run_cmd([sys.executable, "-I", os.path.join(REPO, p["summary"]), os.path.join(gdir, "dump"), os.path.join(gdir, "files.txt"), os.path.join(gdir, "out")], log=log)
                rc, secs = rc or rc2 or rc3, secs + s2 + s3
        elif name == "icons":
            idir = os.path.join(wdx, "icons")
            lst = os.path.join(wdx, "icons-list.txt")
            # item_icons.py list reads data/: run it with the new export swapped in (worktree-only, see regen)
            rc, secs, _ = run_item_icons_list(env, data, files_txt, lst, log)
            if not rc:
                rc2, s2, _ = wdextract(env, idir, ["textures", lst], log=log)
                rc, secs = rc2, secs + s2
        else:
            continue
        meta["steps"]["pass " + name] = {"rc": rc, "seconds": secs}
        say("pass %-6s rc=%d %.0fs" % (name, rc, secs))
    meta["status"] = "ok"
    meta["finished"] = now()
    meta["usmap_sha256"] = sha256_file(env["usmap_cuedump"])
    write_json(os.path.join(ldir, "extract-meta.json"), meta)
    say("extract %s: OK. data=%s" % (label, data))
    return 0


def run_item_icons_list(env, data, files_txt, out_list, log):
    """`item_icons.py list` reads <repo>/data. Run it in a throwaway link swap; only allowed outside the main checkout."""
    if is_main_checkout(REPO):
        return 1, 0, "icons pass needs a linked worktree (it swaps data/); run `run` or `regen` from a worktree"
    with LinkSwap(os.path.join(REPO, "data"), data):
        return run_cmd([sys.executable, "-I", os.path.join(HERE, "item_icons.py"), "list", files_txt, out_list], cwd=REPO, log=log)


# ------------------------------------------------------------------------------------------------ diff
def load_area_rules():
    try:
        spec = importlib.util.spec_from_file_location("season_diff", os.path.join(HERE, "season_diff.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        names = dict(mod.AREAS)
        return [(rx, names.get(a, a)) for rx, a in mod.AREA_RULES]
    except Exception:
        return []


def area_of(rel, rules):
    for rx, a in rules:
        if rx.search(rel):
            return a
    parts = rel.split("/")
    return "/".join(parts[:3])


def split_exports(text):
    ms = list(HEADER.finditer(text))
    out = {}
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        name = m.group(1)
        k, n = name, 2
        while k in out:
            k = "%s#%d" % (name, n)
            n += 1
        try:
            out[k] = json.loads(text[m.end():end])
        except ValueError:
            out[k] = None
    return out


def flatten(o, path="", out=None, depth=0):
    if out is None:
        out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            flatten(v, path + "/" + str(k), out, depth + 1)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flatten(v, "%s[%d]" % (path, i), out, depth + 1)
    else:
        out[path] = o
    return out


def field_key(path):
    comps = [re.sub(r"\[\d+\]", "", c) for c in path.split("/") if c]
    comps = [c for c in comps if c and not HASHED.fullmatch(c)]
    return ".".join(comps[-3:]) if comps else path


def file_digest(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def tree_index(root):
    idx = {}
    for dp, _, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            idx[os.path.relpath(p, root).replace("\\", "/").lower()] = (os.path.relpath(p, root).replace("\\", "/"), p)
    return idx


def num_changed(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) > 1e-6 * max(1.0, abs(a), abs(b))
    return a != b


def diff_trees(old, new, rules, example_limit=3):
    oi, ni = tree_index(old), tree_index(new)
    added = sorted(ni[k][0] for k in set(ni) - set(oi))
    removed = sorted(oi[k][0] for k in set(oi) - set(ni))
    changed = []
    areas = collections.defaultdict(lambda: {"added": 0, "removed": 0, "changed": 0, "fields": collections.Counter(), "hashed_renames": 0})
    for rel in added:
        areas[area_of(rel, rules)]["added"] += 1
    for rel in removed:
        areas[area_of(rel, rules)]["removed"] += 1

    def cmp(k):
        (rel, po), (_, pn) = oi[k], ni[k]
        if os.path.getsize(po) == os.path.getsize(pn) and file_digest(po) == file_digest(pn):
            return None
        res = {"file": rel, "area": area_of(rel, rules), "fields": collections.Counter(), "examples": [], "hashed_renames": 0, "nchanges": 0}
        if not rel.endswith(".json"):
            res["nchanges"] = 1
            res["fields"]["(text file)"] += 1
            return res
        try:
            eo = split_exports(open(po, encoding="utf-8", errors="replace").read())
            en = split_exports(open(pn, encoding="utf-8", errors="replace").read())
        except Exception as ex:
            res["fields"]["(unreadable: %s)" % ex] += 1
            return res
        for name in sorted(set(eo) | set(en)):
            if name not in eo or name not in en:
                res["fields"]["(export %s)" % ("added" if name in en else "removed")] += 1
                res["nchanges"] += 1
                if len(res["examples"]) < example_limit:
                    res["examples"].append("%s export %s" % ("+" if name in en else "-", name))
                continue
            fo, fn_ = flatten(eo[name]), flatten(en[name])
            for p in set(fo) | set(fn_):
                a, b = fo.get(p, "<absent>"), fn_.get(p, "<absent>")
                if not num_changed(a, b):
                    continue
                if HASHED.search(p) and ("<absent>" in (a, b)):
                    res["hashed_renames"] += 1
                    continue
                res["nchanges"] += 1
                res["fields"][field_key(p)] += 1
                if len(res["examples"]) < example_limit:
                    res["examples"].append("%s: %s -> %s" % (p.lstrip("/")[:140], str(a)[:40], str(b)[:40]))
        return res if (res["nchanges"] or res["hashed_renames"]) else {"file": rel, "area": res["area"], "fields": collections.Counter(), "examples": [], "hashed_renames": 0, "nchanges": 0, "bytes_only": True}

    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        for r in ex.map(cmp, sorted(set(oi) & set(ni))):
            if r:
                changed.append(r)
    for r in changed:
        a = areas[r["area"]]
        if r.get("bytes_only"):
            continue
        if r["nchanges"]:
            a["changed"] += 1
        a["fields"].update(r["fields"])
        a["hashed_renames"] += r["hashed_renames"]
    return added, removed, changed, areas


def cmd_diff(args):
    env = config(args)
    root = env["builds_root"]
    od = args.old if os.path.isabs(args.old) or os.path.isdir(args.old) else os.path.join(root, args.old, "data")
    nd = args.new if os.path.isabs(args.new) or os.path.isdir(args.new) else os.path.join(root, args.new, "data")
    if os.path.isdir(os.path.join(root, args.old, "data")):
        od = os.path.join(root, args.old, "data")
    if os.path.isdir(os.path.join(root, args.new, "data")):
        nd = os.path.join(root, args.new, "data")
    for d in (od, nd):
        if not os.path.isdir(d):
            raise SystemExit("no data directory: %s" % d)
    outdir = args.out or os.path.join(root, args.new if os.path.isdir(os.path.join(root, args.new)) else "diff-" + datetime.date.today().isoformat())
    t = time.time()
    rules = load_area_rules()
    added, removed, changed, areas = diff_trees(od, nd, rules)
    real = [c for c in changed if not c.get("bytes_only")]
    bytes_only = [c for c in changed if c.get("bytes_only")]
    secs = round(time.time() - t, 1)
    summary = {"old": od, "new": nd, "created": now(), "seconds": secs, "added": added, "removed": removed,
               "changed": [{"file": c["file"], "area": c["area"], "nchanges": c["nchanges"], "hashed_renames": c["hashed_renames"],
                            "top_fields": c["fields"].most_common(6), "examples": c["examples"]} for c in sorted(real, key=lambda c: -c["nchanges"])],
               "bytes_only_changed": [c["file"] for c in bytes_only],
               "areas": {a: {"added": v["added"], "removed": v["removed"], "changed": v["changed"], "hashed_renames": v["hashed_renames"],
                             "top_fields": v["fields"].most_common(12)} for a, v in sorted(areas.items())}}
    write_json(os.path.join(outdir, "patch-diff.json"), summary)
    L = ["# Patch diff: %s -> %s" % (args.old, args.new), "",
         "Generated by `_tools/update_pipeline.py diff` (%s, %.1fs). Old: `%s`; new: `%s`." % (summary["created"], secs, od, nd), "",
         "| | Files |", "|---|---:|", "| Added | %d |" % len(added), "| Removed | %d |" % len(removed),
         "| Changed values | %d |" % len(real), "| Changed bytes only (renamed/hashed property names, formatting) | %d |" % len(bytes_only), ""]
    if not (added or removed or real or bytes_only):
        L += ["No differences: the two exports are identical.", ""]
    L += ["## By area", "", "| Area | Added | Removed | Changed | Top changed fields |", "|---|---:|---:|---:|---|"]
    for a, v in sorted(areas.items(), key=lambda kv: -(kv[1]["added"] + kv[1]["removed"] + kv[1]["changed"])):
        L.append("| %s | %d | %d | %d | %s |" % (a, v["added"], v["removed"], v["changed"], ", ".join("`%s` (%d)" % kv for kv in v["fields"].most_common(5)) or "-"))
    L.append("")
    if real:
        L += ["## Most changed assets", ""]
        for c in sorted(real, key=lambda c: -c["nchanges"])[:40]:
            L.append("- `%s` (%s): %d value changes. %s" % (c["file"], c["area"], c["nchanges"], "; ".join(c["examples"][:2])))
        L.append("")
    for tag, lst in (("Added assets", added), ("Removed assets", removed)):
        if lst:
            L += ["## %s (%d)" % (tag, len(lst)), ""] + ["- `%s`" % x for x in lst[:80]] + (["- ... %d more (see patch-diff.json)" % (len(lst) - 80)] if len(lst) > 80 else []) + [""]
    hr = sum(v["hashed_renames"] for v in areas.values())
    if hr:
        L += ["## Property-name noise", "", "%d property names appear/disappear as hashed tokens (`_aaa...`): a usmap name change, not a game change. A large number after an update means new fields the usmap cannot name yet." % hr, ""]
    with open(os.path.join(outdir, "patch-diff.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    say("diff %s -> %s: +%d -%d ~%d (bytes-only %d) in %.1fs; wrote %s" % (args.old, args.new, len(added), len(removed), len(real), len(bytes_only), secs, os.path.join(outdir, "patch-diff.md")))
    if args.full:
        sdir = os.path.join(outdir, "season-diff")
        rc, s, out = run_cmd([sys.executable, "-I", os.path.join(HERE, "season_diff.py"), "--s1", od, "--s2", nd, "--out", sdir, "--write"], timeout=3600)
        say("season_diff --write -> %s (rc=%d, %.0fs); this is the input for a Season/patch Changes page (docs/UPDATE_PIPELINE.md)" % (sdir, rc, s))
    return 0


# ------------------------------------------------------------------------------------------------ audit / regen
def classify_scripts(reg):
    present = sorted(f for f in os.listdir(HERE) if f.endswith(".py") and not f.startswith("ads_"))
    by = {e["script"]: e for e in reg["scripts"]}
    return present, by, [f for f in present if f not in by], [n for n in by if n not in present]


def cmd_audit(args):
    reg = load_registry()
    present, by, unclassified, stale = classify_scripts(reg)
    cnt = collections.Counter((e["class"], e["tier"]) for e in reg["scripts"])
    say("%d python scripts in _tools (ads_* ignored), %d registry entries" % (len(present), len(by)))
    for (c, t), n in sorted(cnt.items()):
        say("  %-13s %-7s %3d" % (c, t, n))
    nocheck = [e["script"] for e in reg["scripts"] if e["class"] == "generator" and e["tier"] == "core" and e["check"] is None]
    say("core generators with no check mode (%d): %s" % (len(nocheck), ", ".join(nocheck)))
    for f in unclassified:
        say("UNCLASSIFIED: %s  (add it to `scripts` in pipeline_registry.json)" % f)
    for f in stale:
        say("STALE ENTRY (no such script): %s" % f)
    js = [f for f in os.listdir(HERE) if f.endswith(".js")]
    say("%d .js files covered by script_globs" % len(js))
    return 1 if (unclassified or stale) else 0


def git_status_paths(repo):
    _, out = git("status", "--porcelain", "-z", cwd=repo)
    items = [x for x in out.split("\0") if x]
    return [(x[:2], x[3:]) for x in items]


def real_diff(repo):
    """Return (real_changed, eol_only, noise_only, untracked) after `regen`. EOL-only and noise-only files are restored."""
    git("update-index", "-q", "--refresh", cwd=repo)
    _, names = git("diff", "--name-only", "-z", cwd=repo)
    names = [n for n in names.split("\0") if n]
    real, eol, noise = [], [], []
    for n in names:
        rc, _ = git("diff", "--ignore-cr-at-eol", "--quiet", "--", n, cwd=repo)
        if rc == 0:
            eol.append(n)
            continue
        _, d = git("diff", "--ignore-cr-at-eol", "-U0", "--", n, cwd=repo)
        body = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        if body and all(any(p in l for p in NOISE_LINES) for l in body):
            noise.append(n)
        else:
            real.append(n)
    for lst in (eol, noise):
        for i in range(0, len(lst), 50):
            git("checkout", "--", *lst[i:i + 50], cwd=repo)
    _, un = git("ls-files", "--others", "--exclude-standard", "-z", cwd=repo)
    return real, eol, noise, [u for u in un.split("\0") if u]


def suspicious(repo, files):
    """Files whose diff ADDS more 'not yet known'-style text or empty table cells than it removes."""
    out = []
    for n in files:
        _, d = git("diff", "--ignore-cr-at-eol", "-U0", "--", n, cwd=repo)
        add = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
        rem = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
        def cnt(lines):
            c = collections.Counter()
            for l in lines:
                for s in SUSPECT:
                    c[s.lower()] += l.lower().count(s.lower())
                c["empty cell"] += len(re.findall(r"\|\s*\|", l)) if n.endswith(".md") else 0
                c["null"] += l.count(": null") if n.endswith(".json") else 0
            return c
        a, r = cnt(add), cnt(rem)
        worse = {k: (r[k], a[k]) for k in a if a[k] > r[k]}
        if worse:
            out.append((n, worse))
    return out


def leaves(o):
    if isinstance(o, dict):
        return sum(leaves(v) for v in o.values())
    if isinstance(o, list):
        return sum(leaves(v) for v in o)
    return 1


def shrunk(repo, files, ratio=0.9):
    """Changed files that lost content: JSON with fewer values, Markdown with fewer table rows (a parser that matched nothing)."""
    out = []
    for n in files:
        rc, old = git("show", "HEAD:" + n, cwd=repo)
        p = os.path.join(repo, n)
        if rc or not os.path.exists(p):
            continue
        new = open(p, encoding="utf-8", errors="replace").read()
        if n.endswith(".json"):
            try:
                a, b = leaves(json.loads(old)), leaves(json.loads(new))
            except ValueError:
                continue
            what = "values"
        elif n.endswith(".md"):
            a = sum(1 for l in old.splitlines() if l.startswith("|"))
            b = sum(1 for l in new.splitlines() if l.startswith("|"))
            what = "table rows"
        else:
            continue
        if a and b < a * ratio:
            out.append((n, what, a, b))
    return out


def run_generator(repo, entry, mode, extra_env, fills, log, timeout=1800):
    args = entry["write"] if mode == "write" else entry["check"]
    if args is None:
        return None
    args = [a.format(**fills) if "{" in a else a for a in args]
    return run_cmd([sys.executable, "-I", os.path.join(repo, "_tools", entry["script"])] + args, cwd=repo, log=log, timeout=timeout, env=extra_env)


def cmd_regen(args):
    env = config(args)
    reg = load_registry()
    repo = os.path.abspath(args.repo or REPO)
    if is_main_checkout(repo):
        raise SystemExit("refusing to run in the main checkout %s: regen swaps data/ and rewrites site files. Use a linked worktree (`run` makes one)." % repo)
    data = os.path.abspath(args.data)
    if not os.path.isdir(os.path.join(data, "Wardogs", "Content")):
        raise SystemExit("%s does not look like a data export (no Wardogs/Content)" % data)
    outdir = args.report_dir or os.path.join(env["builds_root"], args.label or "regen")
    os.makedirs(outdir, exist_ok=True)
    log = os.path.join(outdir, "regen.log")
    open(log, "w").close()
    present, by, unclassified, stale = classify_scripts(reg)
    only = set(args.only.split(",")) if args.only else None
    skip = set(args.skip.split(",")) if args.skip else set()
    gens = [e for e in reg["scripts"] if e["class"] == "generator" and e["tier"] == "core" and e["script"][:-3] not in skip
            and (only is None or e["script"][:-3] in only)]
    t0 = time.time()
    extra_env = {"AMMO_AVAILABILITY": os.path.join(repo, "assets", "data", "ammo-availability.json")}
    results = collections.defaultdict(list)
    swaps = [LinkSwap(os.path.join(repo, "data"), data)]
    if env.get("sdk_raw") and os.path.isdir(env["sdk_raw"]) and not os.path.lexists(os.path.join(repo, "sdk", "raw")):
        swaps.append(LinkSwap(os.path.join(repo, "sdk", "raw"), env["sdk_raw"]))
    wd = os.path.join(os.path.dirname(data), "wdextract")
    fills = {"files": os.path.join(wd, "files", "files.txt"), "out": os.path.join(wd, "icons"), "dump": "", "png": "", "report": outdir}
    ran_assets, skipped_assets = [], []
    stacks = []
    for s in swaps:
        stacks.append(s.__enter__())
    try:
        say("regen: %d core generators against %s (%d passes)" % (len(gens), data, args.passes))
        pass_changed = []
        for p in range(1, args.passes + 1):
            say("--- pass %d" % p)
            for e in gens:
                r = run_generator(repo, e, "write", extra_env, fills, log)
                if r is None:
                    continue
                rc, secs, tail = r
                results[e["script"]].append({"pass": p, "rc": rc, "seconds": secs, "tail": tail[-300:]})
                say("  %-34s rc=%d %5.1fs%s" % (e["script"], rc, secs, "" if rc == 0 else "   <-- FAILED"))
            if p == 1:
                snap1 = real_diff_snapshot(repo)
            else:
                snap2 = real_diff_snapshot(repo)
                pass_changed = sorted(k for k in snap2 if snap2[k] != snap1.get(k)) + sorted(k for k in snap1 if k not in snap2)
        # assets-tier: only the icons pass has a recipe the pipeline can run
        icons_ok = os.path.exists(fills["files"]) and os.path.isdir(os.path.join(wd, "icons")) and os.path.exists(os.path.join(repo, "_tools", "item_icons.py"))
        for e in reg["scripts"]:
            if e["class"] == "generator" and e["tier"] == "assets" and e["script"][:-3] not in skip:
                if e["script"] == "item_icons.py" and icons_ok and not args.no_assets:
                    rc, secs, tail = run_generator(repo, e, "write", extra_env, fills, log)
                    results[e["script"]].append({"pass": 1, "rc": rc, "seconds": secs, "tail": tail[-300:]})
                    ran_assets.append(e["script"])
                    say("  %-34s rc=%d %5.1fs (assets)" % (e["script"], rc, secs))
                else:
                    skipped_assets.append(e)
        # GE values come from the WdExtract GE pass
        gj = os.path.join(wd, "ge", "out", "ge_summary.json")
        ge_state = "no GE pass output"
        if os.path.exists(gj) and not args.no_assets:
            dst = os.path.join(repo, "assets", "data", "ge-values.json")
            if open(gj, "rb").read() != open(dst, "rb").read():
                shutil.copyfile(gj, dst)
                ge_state = "ge-values.json UPDATED from the GE pass"
            else:
                ge_state = "ge-values.json identical to the GE pass output"
            # rerun the dependants that read ge-values.json
            for n in ("attachment_tables", "medical_tables", "sight_tables", "weapon_attributes", "action_tables"):
                e = by.get(n + ".py")
                if e and n not in skip:
                    run_generator(repo, e, "write", extra_env, fills, log)
        say("GE: " + ge_state)
        # checks
        say("--- checks")
        checks = []
        for e in reg["scripts"]:
            if e["tier"] != "core" or e["script"][:-3] in skip or e["check"] is None or e["class"] == "report":
                continue
            if only and e["script"][:-3] not in only and e["class"] == "generator":
                continue
            rc, secs, tail = run_generator(repo, e, "check", extra_env, fills, log)
            checks.append({"script": e["script"], "kind": e["class"], "args": e["check"], "rc": rc, "seconds": secs, "tail": tail[-400:]})
            say("  %-34s %s rc=%d" % (e["script"], " ".join(e["check"]), rc))
        for e in reg["scripts"]:
            if e["class"] == "report" and e["check"] is not None and not only:
                rc, secs, tail = run_generator(repo, e, "check", extra_env, fills, log)
                (open(os.path.join(outdir, e["script"][:-3] + ".txt"), "w", encoding="utf-8")).write(tail)
        real, eol, noise, untracked = real_diff(repo)
        stat = git("diff", "--ignore-cr-at-eol", "--stat", cwd=repo)[1]
        numstat = git("diff", "--ignore-cr-at-eol", "--numstat", cwd=repo)[1]
        sus = suspicious(repo, real)
        shr = shrunk(repo, real)
        # link check last
    finally:
        for s in reversed(stacks):
            s.__exit__(None, None, None)
    fails = [(k, v[-1]) for k, v in results.items() if v[-1]["rc"] != 0]
    known = {e["script"]: e["known_fail"] for e in reg["scripts"] if e.get("known_fail")}
    bad_checks = [c for c in checks if c["rc"] != 0 and c["script"] not in known]
    known_hit = [c for c in checks if c["rc"] != 0 and c["script"] in known]
    secs = round(time.time() - t0, 1)
    nocheck = [e["script"] for e in gens if e["check"] is None]
    parsers = [e["script"] for e in reg["scripts"] if e.get("parses_pages")]
    rep = {"data": data, "repo": repo, "seconds": secs, "generators": len(gens), "failed": [k for k, _ in fails],
           "checks_failed": [c["script"] for c in bad_checks], "real_changed": real, "eol_only_restored": len(eol), "noise_only_restored": noise,
           "untracked": untracked, "suspicious": [(n, w) for n, w in sus], "shrunk": shr, "second_pass_changes": pass_changed,
           "no_check": nocheck, "unclassified": unclassified, "skipped_assets": [e["script"] for e in skipped_assets], "ge": ge_state}
    write_json(os.path.join(outdir, "regen-report.json"), rep)
    L = ["# Regen report", "", "Data: `%s`. Worktree: `%s`. %d core generators, %d passes, %.0fs total." % (data, repo, len(gens), args.passes, secs), "",
         "## Summary", "", "| | |", "|---|---:|", "| Generator failures | %d |" % len(fails), "| Check failures | %d |" % len(bad_checks),
         "| Files with real changes | %d |" % len(real), "| New (untracked) files | %d |" % len(untracked),
         "| EOL-only rewrites restored | %d |" % len(eol), "| Noise-only rewrites restored (git tree id) | %d |" % len(noise),
         "| Files that changed again in pass 2 (order dependency) | %d |" % len(pass_changed), ""]
    if fails:
        L += ["## Generator failures", ""] + ["- `%s` rc=%d: `%s`" % (k, v["rc"], v["tail"].strip().splitlines()[-1] if v["tail"].strip() else "") for k, v in fails] + [""]
    if bad_checks:
        L += ["## Check failures", ""] + ["- `%s %s` rc=%d: `%s`" % (c["script"], " ".join(c["args"]), c["rc"], c["tail"].strip().splitlines()[-1] if c["tail"].strip() else "") for c in bad_checks] + [""]
    if known_hit:
        L += ["## Known failing checks (baseline, not counted)", ""] + ["- `%s`: %s" % (c["script"], known[c["script"]]) for c in known_hit] + [""]
    if pass_changed:
        L += ["## Changed in the second pass", "", "These files differed between pass 1 and pass 2: a generator reads another generator's output and ran too early (fix the order in `scripts`).", ""] + ["- `%s`" % x for x in pass_changed] + [""]
    L += ["## Real changes (git diff --ignore-cr-at-eol --stat)", "", "```", stat.rstrip() or "(none)", "```", ""]
    if untracked:
        L += ["## New files", ""] + ["- `%s`" % u for u in untracked[:100]] + [""]
    if sus:
        L += ["## Possible silent parser breakage", "",
              "These diffs ADD more `not yet known`-style text or empty table cells than they remove. Check that the generator still parses its input pages (the history rewrite once unlinked `[`DA_x`](...)` rows and a parser silently lost its data).", ""]
        L += ["- `%s`: %s" % (n, ", ".join("%s %d -> %d" % (k, a, b) for k, (a, b) in w.items())) for n, w in sus] + [""]
    if shr:
        L += ["## Files that lost content", "", "Fewer JSON values or Markdown table rows than HEAD: usually a parser that stopped matching its input (not a game change).", ""]
        L += ["- `%s`: %s %d -> %d" % x for x in shr] + [""]
    if parsers:
        L += ["## Generators that parse Markdown pages", "", "Their output depends on page text, not only on data/: " + ", ".join("`%s`" % p for p in parsers), ""]
    L += ["## Generators without a check mode (%d)" % len(nocheck), "", ", ".join("`%s`" % n for n in nocheck), "",
          "## Not refreshed by regen", "", "Generators that need inputs the pipeline did not produce (hand-run extraction, see docs/UPDATE_PIPELINE.md):", ""]
    L += ["- `%s` (%s)" % (e["script"], "; ".join(e["inputs"])) for e in skipped_assets] + [""]
    man = [e for e in reg["scripts"] if e["tier"] == "manual" and e["class"] in ("generator", "checker")]
    L += ["Manual-tier generators/checkers (exe analysis, Season 1 export): " + ", ".join("`%s`" % e["script"] for e in man), ""]
    if unclassified:
        L += ["## Unclassified scripts", ""] + ["- `%s`" % u for u in unclassified] + [""]
    L += ["## Review and merge", "", "```", "cd %s" % repo, "git status --short", "git diff --ignore-cr-at-eol --stat", "git add -A && git commit -m \"Update to build <label>: regenerated site data\"", "# then, from the main checkout: git merge <branch>", "```", ""]
    with open(os.path.join(outdir, "regen-report.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    say("regen done in %.0fs: %d generator failures, %d check failures, %d files changed, %d new, %d EOL-only restored. Report: %s" % (
        secs, len(fails), len(bad_checks), len(real), len(untracked), len(eol), os.path.join(outdir, "regen-report.md")))
    return 1 if fails else (2 if bad_checks else 0)


def real_diff_snapshot(repo):
    """Content hash of every file git sees as changed (EOL-insensitive), for the pass-1 vs pass-2 comparison."""
    git("update-index", "-q", "--refresh", cwd=repo)
    _, names = git("diff", "--name-only", "-z", cwd=repo)
    out = {}
    for n in [x for x in names.split("\0") if x]:
        p = os.path.join(repo, n)
        if os.path.exists(p):
            with open(p, "rb") as f:
                out[n] = hashlib.sha1(f.read().replace(b"\r\n", b"\n")).hexdigest()
    return out


# ------------------------------------------------------------------------------------------------ run
def cmd_run(args):
    env = config(args)
    label = args.label
    root = env["builds_root"]
    ldir = os.path.join(root, label)
    t0 = time.time()
    steps = []
    prior = [d for _, d, m in manifests(root) if d != label]
    say("== 1/5 snapshot")
    cmd_snapshot(argparse.Namespace(label=label, quick=args.quick, config=args.config))
    steps.append(("snapshot", round(time.time() - t0, 1)))
    if prior:
        pm = read_json(os.path.join(root, prior[-1], "manifest.json"))
        cm = read_json(os.path.join(ldir, "manifest.json"))
        a, r, c = compare_manifests(pm, cm)
        say("vs %s: %d added, %d removed, %d changed container files" % (prior[-1], len(a), len(r), len(c)))
        if not (a or r or c) and not args.force:
            say("the paks are identical to %s; nothing to update (use --force to run anyway)." % prior[-1])
            return 0
    say("== 2/5 extract")
    t = time.time()
    rc = cmd_extract(argparse.Namespace(label=label, force=args.force, assets=args.assets, config=args.config))
    steps.append(("extract", round(time.time() - t, 1)))
    if rc:
        say("stopped: extract failed (rc=%d)" % rc)
        return rc
    old = args.old or (prior[-1] if prior else None)
    if old and os.path.isdir(os.path.join(root, old, "data")):
        say("== 3/5 diff %s -> %s" % (old, label))
        t = time.time()
        cmd_diff(argparse.Namespace(old=old, new=label, out=None, full=args.full, config=args.config))
        steps.append(("diff", round(time.time() - t, 1)))
    else:
        say("== 3/5 diff skipped: no earlier extracted build under %s (pass --old DIR to diff against an export)" % root)
    say("== 4/5 worktree")
    wt = args.worktree or os.path.join(ldir, "worktree")
    branch = "update-" + re.sub(r"[^A-Za-z0-9._-]", "-", label)
    if not os.path.exists(wt):
        rc, out = git("worktree", "add", "-b", branch, wt, args.base, cwd=REPO)
        if rc:
            raise SystemExit("git worktree add failed (branch %s exists? use --worktree/--base)" % branch)
    say("worktree %s on %s" % (wt, branch))
    script = os.path.join(wt, "_tools", "update_pipeline.py")
    script = script if os.path.exists(script) else os.path.abspath(__file__)
    cfgarg = ["--config", args.config] if args.config else []
    if old and os.path.isdir(os.path.join(root, old, "data")) and not args.no_baseline:
        # Regenerating the OLD export first isolates what the patch changed: pages edited by hand after their last
        # generation, and generators that are ahead of their committed output, show up in this baseline commit instead.
        say("== 5a/5 baseline regen on the old export %s (so the final diff holds only the patch)" % old)
        t = time.time()
        subprocess.run([sys.executable, "-I", script, "regen", "--data", os.path.join(root, old, "data"), "--repo", wt, "--label", label + "-baseline",
                        "--passes", "1"] + cfgarg)
        git("add", "-A", cwd=wt)
        rc0, _ = git("commit", "-q", "-m", "Baseline: regenerate with the previous export (%s); no data change" % old, cwd=wt)
        steps.append(("baseline regen", round(time.time() - t, 1)))
        say("baseline committed on %s (empty commit = the site was already in sync with %s)" % (branch, old))
    say("== 5/5 regen")
    t = time.time()
    rc = subprocess.run([sys.executable, "-I", script, "regen", "--data", os.path.join(ldir, "data"),
                         "--repo", wt, "--label", label, "--passes", str(args.passes)] + cfgarg).returncode
    steps.append(("regen", round(time.time() - t, 1)))
    say("")
    say("== done in %.0fs: %s" % (time.time() - t0, ", ".join("%s %.0fs" % s for s in steps)))
    say("Reports: %s, %s" % (os.path.join(ldir, "patch-diff.md"), os.path.join(ldir, "regen-report.md")))
    say("Review and merge:")
    say("  cd %s" % wt)
    say("  git status --short && git diff --ignore-cr-at-eol --stat")
    say("  python -I _tools/check_links.py")
    say("  git add -A && git commit -m \"Update to build %s: regenerated site data\"" % label)
    say("  cd <main checkout> && git merge %s" % branch)
    say("Then review the report's 'Not refreshed' list: those generators need hand-run extraction (docs/UPDATE_PIPELINE.md).")
    return rc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", help="JSON file overriding registry `environment` keys")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("snapshot"); p.add_argument("--label"); p.add_argument("--quick", action="store_true", help="size and mtime only, no hashes")
    p = sub.add_parser("status"); p.add_argument("--against"); p.add_argument("--quick", action="store_true")
    p = sub.add_parser("extract"); p.add_argument("--label", required=True); p.add_argument("--force", action="store_true"); p.add_argument("--assets", action="store_true", help="also run the asset passes (icons)")
    p = sub.add_parser("diff"); p.add_argument("--old", required=True); p.add_argument("--new", required=True); p.add_argument("--out"); p.add_argument("--full", action="store_true", help="also run season_diff.py --write into <out>/season-diff")
    p = sub.add_parser("regen"); p.add_argument("--data", required=True); p.add_argument("--repo"); p.add_argument("--label"); p.add_argument("--report-dir"); p.add_argument("--passes", type=int, default=1, help="2 re-runs every generator to expose order dependencies")
    p.add_argument("--only"); p.add_argument("--skip"); p.add_argument("--no-assets", action="store_true")
    p = sub.add_parser("run"); p.add_argument("--label", required=True); p.add_argument("--old"); p.add_argument("--base", default="main"); p.add_argument("--worktree"); p.add_argument("--quick", action="store_true")
    p.add_argument("--force", action="store_true"); p.add_argument("--assets", action="store_true"); p.add_argument("--full", action="store_true"); p.add_argument("--passes", type=int, default=1); p.add_argument("--no-baseline", action="store_true", help="skip the baseline regen on the old export")
    sub.add_parser("audit")
    a = ap.parse_args(argv)
    return {"snapshot": cmd_snapshot, "status": cmd_status, "extract": cmd_extract, "diff": cmd_diff, "regen": cmd_regen, "run": cmd_run, "audit": cmd_audit}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
