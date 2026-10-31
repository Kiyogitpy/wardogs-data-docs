"""Restore Markdown source links to tracked raw JSON assets on GitHub.

Run after regenerating pages:
    python _tools/link_sources.py --write
    python _tools/link_sources.py --check
    python _tools/link_sources.py --verify

Only Git-tracked data/**/*.json files are eligible. Ambiguous asset names
are left unchanged. Existing Markdown links and code blocks are preserved.
No option publishes files or changes the Git index.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = 'https://github.com/Kiyogitpy/wardogs-data-docs'
EXPORT = re.compile(r'^--- export: [^/\r\n]+/ (.*?) ---\s*$', re.MULTILINE)
# Match protected inline constructs across line boundaries before code spans.
# Bracketed labels are conservative: even a truncated link is left unchanged.
TOKEN = re.compile(
    r'(?P<escape>\\[\s\S])'
    r'|(?P<comment><!--[\s\S]*?(?:-->|$))'
    r'|(?P<anchor><a\b[^>]*>[\s\S]*?</a>)'
    r'|(?P<tag><[^>\n]+>)'
    r'|(?P<link>!?\[(?:[^\[\]]|\[[^\]]*\])*\](?:\([^)]*\)|\[[^\]]*\])?)'
    r'|(?P<incomplete>\[[^\]\n]*(?:\n|$))'
    r'|(?P<code>(?<!`)(?P<ticks>`+)(?P<body>[\s\S]*?)(?P=ticks)(?!`))',
    re.IGNORECASE,
)
FENCE = re.compile(r'^(?: {0,3}>[ \t]?)* {0,3}(`{3,}|~{3,})')
HREF = re.compile(r'\]\((https://github\.com/Kiyogitpy/wardogs-data-docs/(?:blob|tree)/main/data/[^\s)]+)\)')


def tracked_paths(root):
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                            capture_output=True, check=True)
    return [p.decode('utf-8') for p in result.stdout.split(b'\0') if p]


class SourceIndex:
    """Unambiguous aliases and path suffixes for the published JSON tree."""
    def __init__(self, root, paths):
        self.root = Path(root)
        self.paths = {str(p).replace('\\', '/') for p in paths
                      if str(p).replace('\\', '/').startswith('data/')
                      and str(p).lower().endswith('.json')}
        self.names = defaultdict(set)
        self.suffixes = defaultdict(set)
        self.folders = defaultdict(set)
        self.directory_paths = set()
        self.cache = {}
        for path in sorted(self.paths):
            relative = path[5:]
            pure = PurePosixPath(relative)
            self.names[pure.name].add(path)
            self.names[pure.stem].add(path)
            for alias in EXPORT.findall((self.root / path).read_text(encoding='utf-8-sig')):
                self.names[alias].add(path)
            parts = pure.parts
            for start in range(len(parts)):
                suffix = '/'.join(parts[start:])
                self.suffixes[suffix].add(path)
                self.suffixes[suffix[:-5]].add(path)
            for parent in pure.parents:
                folder = parent.as_posix()
                if folder == '.':
                    continue
                full = 'data/' + folder
                self.directory_paths.add(full)
                for start in range(len(parent.parts)):
                    self.folders['/'.join(parent.parts[start:])].add(full)

    @classmethod
    def from_repo(cls, root=ROOT):
        return cls(root, tracked_paths(root))

    def target(self, text):
        if text not in self.cache:
            self.cache[text] = self._resolve(text)
        return self.cache[text]

    def _resolve(self, text):
        text = text.strip().replace('\\', '/')
        if not text or any(c in text for c in '*?{}\n\r'):
            return None
        if '/' not in text:
            choices = self.names.get(text, set())
            if len(choices) == 1:
                return self.url('blob', next(iter(choices)))
            return None
        tail = text.strip('/')
        if tail.startswith('./'):
            tail = tail[2:]
        if tail.startswith('data/'):
            tail = tail[5:]
        exact = 'data/' + tail
        if exact in self.paths:
            return self.url('blob', exact)
        if tail.endswith('.uasset'):
            tail = tail[:-7] + '.json'
        if tail.startswith('Game/'):
            tail = 'Content/' + tail[5:]
        # Only slash-containing suffixes are accepted here, so an arbitrary
        # absolute path cannot fall back to its basename and link by accident.
        choices = self.suffixes.get(tail, set())
        folders = self.folders.get(tail, set())
        if len(choices) == 1 and not folders:
            return self.url('blob', next(iter(choices)))
        if len(folders) == 1 and not choices:
            return self.url('tree', next(iter(folders)))
        return None

    @staticmethod
    def url(kind, path):
        return REPO_URL + '/' + kind + '/main/' + quote(path, safe='/')


def link_markdown(text, index):
    """Link inline source names while preserving block and multiline syntax."""
    protected = []
    offset = 0
    fence = None
    front_matter = False
    for number, line in enumerate(text.splitlines(keepends=True)):
        end = offset + len(line)
        marker = FENCE.match(line)
        if number == 0 and line.lstrip('\ufeff').strip() == '---':
            front_matter = True
            protected.append((offset, end))
        elif front_matter:
            protected.append((offset, end))
            if line.strip() in ('---', '...'):
                front_matter = False
        elif fence:
            protected.append((offset, end))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not line[marker.end():].strip():
                fence = None
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            protected.append((offset, end))
        elif line.startswith(('    ', '\t')) or re.match(r'^ {0,3}\[[^\]]+\]:', line):
            protected.append((offset, end))
        offset = end

    count = 0
    block = 0

    def replace(match):
        nonlocal count, block
        while block < len(protected) and protected[block][1] <= match.start():
            block += 1
        in_block = block < len(protected) and protected[block][0] < match.end()
        body = match['body']
        if in_block or body is None or match['ticks'] != '`' or '\n' in body or '\r' in body:
            return match[0]
        target = index.target(body)
        if target is None:
            return match[0]
        count += 1
        return '[' + match[0] + '](' + target + ')'

    return TOKEN.sub(replace, text), count


_DEFAULT_INDEX = None
SOURCE_CODE_LINK = re.compile(
    r'\[(`[^`\n]+`)\]\(https://github\.com/Kiyogitpy/wardogs-data-docs/'
    r'(?:blob|tree)/main/data/[^\s)]+\)'
)


def strip_source_links(text):
    """Keep code labels for parsers; remove only our raw-data link wrappers."""
    return SOURCE_CODE_LINK.sub(lambda match: match[1], text)


def link_source_output(text, index=None):
    """Give generator write/check paths the same source-linked representation."""
    global _DEFAULT_INDEX
    if index is None:
        if _DEFAULT_INDEX is None:
            _DEFAULT_INDEX = SourceIndex.from_repo()
        index = _DEFAULT_INDEX
    return link_markdown(text, index)[0]


def verify_links(text, index):
    """Return existing source URLs whose decoded paths are not published."""
    invalid = []
    for url in HREF.findall(text):
        parsed = urlsplit(url)
        prefix = '/Kiyogitpy/wardogs-data-docs/'
        tail = unquote(parsed.path[len(prefix):])
        kind, branch, path = tail.split('/', 2)
        valid = path in (index.paths if kind == 'blob' else index.directory_paths)
        if not valid:
            invalid.append(url)
    return invalid


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='rewrite tracked Markdown pages')
    mode.add_argument('--check', action='store_true', help='fail if source links need restoration')
    mode.add_argument('--verify', action='store_true', help='verify existing source URLs only')
    mode.add_argument('--dry-run', action='store_true', help='report without writing (default)')
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--exclude', action='append', default=[])
    parser.add_argument('--report', type=Path)
    args = parser.parse_args(argv)
    paths = tracked_paths(args.root)
    index = SourceIndex(args.root, paths)
    if not index.paths:
        parser.error('no tracked raw JSON exports under data/')
    pages = sorted(p for p in paths if p.endswith('.md') and p not in args.exclude)
    changes, invalid = {}, {}
    for page in pages:
        path = args.root / page
        with path.open(encoding='utf-8', newline='') as handle:
            text = handle.read()
        new, count = (text, 0) if args.verify else link_markdown(text, index)
        bad = verify_links(new, index)
        if bad:
            invalid[page] = bad
        if count:
            changes[page] = count
            if args.write:
                with path.open('w', encoding='utf-8', newline='') as handle:
                    handle.write(new)
    report = {'tracked_json_exports': len(index.paths), 'pages_scanned': len(pages),
              'pages_changed': len(changes), 'links_added': sum(changes.values()),
              'changes': changes, 'invalid_links': invalid}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'changes'}, indent=2))
    return 1 if invalid or (args.check and changes) else 0


if __name__ == '__main__':
    raise SystemExit(main())
