"""Find broken cross-references between the docs.

Checks every markdown link to a local .md page: the file must exist, a #anchor must
match a heading id on that page (GitHub-style ids, which the site uses), and a "§N" or
"§N.M" written right after the link must match a numbered heading there. Exits 1 when
anything is broken.

    python _tools/check_links.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+?\.md)(#[^)\s]*)?\)(?:`?[^\S\n]*(?:—[^\S\n]*)?§\s?(\d+(?:\.\d+)?))?")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.M)
CODE = re.compile(r"```.*?```", re.S)


def slug(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text).replace("`", "").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def headings(path):
    with open(path, encoding="utf-8") as f:
        body = CODE.sub("", f.read())
    titles = HEADING.findall(body)
    numbers = {m.group(1) for t in titles if (m := re.match(r"(\d+(?:\.\d+)*)\.?\s", t))}
    return {slug(t) for t in titles}, numbers


def main():
    pages = glob.glob(os.path.join(ROOT, "*.md"))
    for d in ("game-features", "content", "pipelines", "plugins", "docs"):
        pages += glob.glob(os.path.join(ROOT, d, "**", "*.md"), recursive=True)
    cache, broken = {}, []
    for page in sorted(pages):
        with open(page, encoding="utf-8") as f:
            text = CODE.sub("", f.read())
        for m in LINK.finditer(text):
            target, anchor, section = m.group(1), m.group(2), m.group(3)
            if target.startswith(("http:", "https:")):
                continue
            path = os.path.normpath(os.path.join(os.path.dirname(page), target))
            where = f"{os.path.relpath(page, ROOT)}: {m.group(0)[:90]}"
            if not os.path.exists(path):
                broken.append(f"{where}\n    missing file {target}")
                continue
            ids, numbers = cache.setdefault(path, headings(path))
            if anchor and anchor[1:] and anchor[1:] not in ids:
                broken.append(f"{where}\n    no heading for {anchor}")
            if section and section not in numbers:
                broken.append(f"{where}\n    no section §{section} in {target}")
    print("\n".join(broken) or "no broken links")
    print(f"{len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
