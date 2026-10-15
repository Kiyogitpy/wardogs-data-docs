"""Link asset names and folder paths in the docs to their source JSON under data/.

Every inline-code span in a Wardogs_*.md doc whose text is a dump file's name (with or
without .json), the name of an object exported inside one, or a dump folder path
becomes a link to that file or folder on GitHub. Names found in more than one file
are left alone. Re-running is safe: spans already linked are skipped.

    python _tools/link_sources.py            # rewrite the docs
    python _tools/link_sources.py --dry-run  # only count what would be linked
"""
import argparse
import collections
import glob
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPO_URL = "https://github.com/Kiyogitpy/wardogs-data-docs"
EXPORT = re.compile(r"^--- export: [^/\n]+/ (\S+) ---", re.M)
# `x` not already the text of a [..](..) link
CODE = re.compile(r"(?<!\[)`([^`\n]+)`(?!\]\()")


def index(data):
    """{name: set of data-relative paths} for files and their exports, and the folder paths."""
    names = collections.defaultdict(set)
    folders = set()
    for dirpath, _, files in os.walk(data):
        rel_dir = os.path.relpath(dirpath, data).replace(os.sep, "/")
        if rel_dir != ".":
            folders.add(rel_dir)
        for f in files:
            rel = f"{rel_dir}/{f}" if rel_dir != "." else f
            stem = os.path.splitext(f)[0]
            names[stem].add(rel)
            names[f].add(rel)
            with open(os.path.join(dirpath, f), encoding="utf-8", errors="replace") as fh:
                for name in EXPORT.findall(fh.read()):
                    names[name].add(rel)
    return names, folders


def url(kind, rel):
    return f"{REPO_URL}/{kind}/main/data/{urllib.parse.quote(rel)}"


def by_suffix(text, names, folders):
    """A partial path (`Content/Data/X.json`, `/Game/Items/X`): the one file or folder it ends."""
    tail = text.strip("/")
    if tail.startswith("Game/"):
        tail = "Content/" + tail[len("Game/"):]
    tail = "/" + (tail[:-len(".json")] if tail.endswith(".json") else tail)
    files = {p for ps in names.values() for p in ps if ("/" + p[:-len(".json")]).endswith(tail)}
    dirs = {d for d in folders if ("/" + d).endswith(tail)}
    if len(files) == 1 and not dirs:
        return url("blob", files.pop())
    if len(dirs) == 1 and not files:
        return url("tree", dirs.pop())
    return None


def target(text, names, folders):
    paths = names.get(text)
    if paths and len(paths) == 1:
        return url("blob", next(iter(paths)))
    folder = text.strip("/")
    if folder in folders:
        return url("tree", folder)
    if "/" in text and " " not in text:
        return by_suffix(text, names, folders)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(DATA):
        raise SystemExit(f"no {DATA}: copy the dump's Wardogs/ and Engine/ folders there first")
    names, folders = index(DATA)
    total = 0
    for doc in sorted(glob.glob(os.path.join(ROOT, "Wardogs_*.md"))):
        with open(doc, encoding="utf-8", newline="") as fh:
            text = fh.read()
        count = 0

        def link(m):
            nonlocal count
            href = target(m.group(1), names, folders)
            if not href:
                return m.group(0)
            count += 1
            return f"[`{m.group(1)}`]({href})"

        new = CODE.sub(link, text)
        total += count
        print(f"{count:5d}  {os.path.basename(doc)}")
        if count and not args.dry_run:
            with open(doc, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
    print(f"{total} links{' (dry run)' if args.dry_run else ''}")


if __name__ == "__main__":
    main()
