"""Source links for generators: only exact, tracked, present raw JSON targets."""
from functools import lru_cache
from pathlib import Path
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BLOB = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"


@lru_cache(maxsize=None)
def tracked_json(root=ROOT):
    root = Path(root)
    paths = subprocess.check_output(["git", "ls-files", "-z", "--", "data"], cwd=root)
    return frozenset(p for p in paths.decode("utf-8").split("\0")
                     if p.startswith("data/") and p.endswith(".json") and (root / p).is_file())


def source_link(path, label):
    """Repository-relative exact path; never guess from an unpublished basename."""
    text = f"`{label}`"
    if path not in tracked_json():
        return text
    # Parentheses must also be encoded: these URLs are embedded in Markdown.
    return f"[{text}]({BLOB}{quote(path, safe='/')})"


def link_generated(text):
    """Keep generator output/checks consistent with the docs' inline-code linker."""
    from link_sources import link_source_output
    return link_source_output(text)
