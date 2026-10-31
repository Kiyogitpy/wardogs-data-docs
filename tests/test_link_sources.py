"""Source-link regression tests; run with python -m unittest discover -s tests."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / '_tools' / 'link_sources.py'


def load_linker():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location('link_sources', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceLinkTests(unittest.TestCase):
    def test_unique_asset_name_links_to_its_tracked_json(self):
        linker = load_linker()
        self.assertIsNotNone(linker, 'Raw JSON source linker has not been restored')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            relative = 'data/Wardogs/Content/Data/DT_Test.json'
            asset = root / relative
            asset.parent.mkdir(parents=True)
            asset.write_text('{"Rows": {}}', encoding='utf-8')
            index = linker.SourceIndex(root, [relative])
            text, count = linker.link_markdown('Source: `DT_Test`.', index)
            self.assertEqual(count, 1)
            self.assertEqual(text, 'Source: [`DT_Test`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/' + relative + ').')


    def test_html_comments_do_not_gain_source_links(self):
        linker = load_linker()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            relative = 'data/Wardogs/Content/DT_Test.json'
            asset = root / relative
            asset.parent.mkdir(parents=True)
            asset.write_text('{}', encoding='utf-8')
            index = linker.SourceIndex(root, [relative])
            original = '<!--\nHidden `DT_Test`\n-->\nVisible `DT_Test`\n'
            rewritten, count = linker.link_markdown(original, index)
            self.assertEqual(count, 1)
            self.assertIn('Hidden `DT_Test`', rewritten)


    def fixture_index(self, files):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for path, content in files.items():
            file = root / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content, encoding='utf-8')
        linker = load_linker()
        assert linker is not None
        return linker, linker.SourceIndex(root, files)

    def test_duplicate_asset_names_are_not_guessed(self):
        _, index = self.fixture_index({'data/A/Same.json': '{}', 'data/B/Same.json': '{}'})
        self.assertIsNone(index.target('Same'))
        self.assertTrue(index.target('data/A/Same.json').endswith('/data/A/Same.json'))

    def test_export_object_alias_resolves_to_containing_file(self):
        _, index = self.fixture_index({'data/A/Package.json': '--- export: UCurve / InnerCurve ---\n{}'})
        self.assertTrue(index.target('InnerCurve').endswith('/data/A/Package.json'))

    def test_game_package_path_resolves_to_json(self):
        _, index = self.fixture_index({'data/Wardogs/Content/Data/DT_Test.json': '{}'})
        self.assertTrue(index.target('/Game/Data/DT_Test').endswith('/data/Wardogs/Content/Data/DT_Test.json'))

    def test_unpublished_non_json_files_are_not_linked(self):
        _, index = self.fixture_index({'data/Config/Hidden.ini': '{}', 'data/SDK/Hidden.hpp': '{}'})
        self.assertIsNone(index.target('Hidden.ini'))
        self.assertIsNone(index.target('Hidden.hpp'))

    def test_source_url_encodes_special_characters(self):
        _, index = self.fixture_index({'data/Wardogs/Content/A+B/Curve (1).json': '{}'})
        self.assertEqual(index.target('Curve (1)'), 'https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/A%2BB/Curve%20%281%29.json')

    def test_second_pass_is_idempotent(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        once, count = linker.link_markdown('`DT_Test` and `DT_Test`', index)
        twice, second_count = linker.link_markdown(once, index)
        self.assertEqual(count, 2)
        self.assertEqual(second_count, 0)
        self.assertEqual(once, twice)

    def test_existing_links_and_images_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '[`DT_Test`](other.md) ![`DT_Test`](image.png) [`DT_Test`][ref]\n[ref]: other.md\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_frontmatter_code_fences_and_indented_code_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '---\ntitle: "`DT_Test`"\n---\n```text\n`DT_Test`\n```\n~~~\n`DT_Test`\n~~~\n    `DT_Test`\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_crlf_line_endings_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text, count = linker.link_markdown('Source: `DT_Test`\r\nNext line\r\n', index)
        self.assertEqual(count, 1)
        self.assertEqual(text.count('\r\n'), 2)

    def test_folder_links_only_point_to_published_json_ancestors(self):
        _, index = self.fixture_index({'data/Wardogs/Content/Data/DT_Test.json': '{}', 'data/Private/Hidden.ini': '{}'})
        self.assertTrue(index.target('Wardogs/Content/Data').endswith('/tree/main/data/Wardogs/Content/Data'))
        self.assertIsNone(index.target('Private/'))

    def test_verification_rejects_untracked_source_targets(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        good = '[source](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/A/DT_Test.json)'
        bad = '[source](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/A/Missing.json)'
        self.assertEqual(linker.verify_links(good, index), [])
        self.assertEqual(len(linker.verify_links(bad, index)), 1)


    def test_generator_output_is_linked_before_comparison(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        expected, _ = linker.link_markdown('Source `DT_Test`', index)
        self.assertEqual(linker.link_source_output('Source `DT_Test`', index), expected)

    def test_parser_normalization_preserves_unrelated_links(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        original = '`DT_Test` plus [`other`](other.md)'
        linked, _ = linker.link_markdown(original, index)
        self.assertEqual(linker.strip_source_links(linked), original)


    def test_shortcut_references_are_not_nested(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '[`DT_Test`]\n\n[`DT_Test`]: other.md\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_multiline_link_labels_are_not_nested(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '[Source `DT_Test`\ncontinued](other.md)\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_truncated_link_labels_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '[`DT_Test`](https://example.com/truncated\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_blockquote_code_fences_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '> ```text\n> `DT_Test`\n> ```\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_multiline_code_spans_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '``some code\n`DT_Test`\ncontinued``\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_successive_html_comments_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = '<!-- closed --> <!--\n`DT_Test`\n-->\n'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))

    def test_escaped_code_delimiters_are_preserved(self):
        linker, index = self.fixture_index({'data/A/DT_Test.json': '{}'})
        text = r'\`DT_Test\`'
        self.assertEqual(linker.link_markdown(text, index), (text, 0))


if __name__ == '__main__':
    unittest.main()
