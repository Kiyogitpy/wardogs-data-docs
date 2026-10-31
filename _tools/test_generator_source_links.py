"""Focused source-link regressions. Run: python -m unittest discover -s _tools -p test_generator_source_links.py -v"""
import importlib
from pathlib import Path
import subprocess
import sys
import unittest
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[1]
BLOB = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"


class GeneratorSourceLinks(unittest.TestCase):
    def test_allowlist_excludes_untracked_nonjson_and_deleted_files(self):
        import tempfile
        from raw_source_links import tracked_json
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            for name in ("published.json", "untracked.json", "deleted.json", "config.ini"):
                path = repo / "data" / name
                path.parent.mkdir(exist_ok=True)
                path.write_text("{}")
            subprocess.run(["git", "add", "data/published.json", "data/deleted.json", "data/config.ini"], cwd=repo, check=True)
            (repo / "data/deleted.json").unlink()
            self.assertEqual(tracked_json(repo), {"data/published.json"})

    def test_data_relative_generator_links_are_published_and_encoded(self):
        paths = subprocess.check_output(
            ["git", "ls-files", "-z", "data"], cwd=ROOT
        ).decode().split("\0")
        path = next(p for p in paths if "Pistol Grips/" in p and p.endswith(".json"))
        for name in ("buildable_tables", "challenge_tables", "movement_tables"):
            module = importlib.import_module(name)
            with self.subTest(generator=name):
                self.assertEqual(module.link(path[5:], "source"),
                                 f"[`source`]({BLOB}{quote(path, safe='/')})")
                self.assertEqual(module.link("Wardogs/NotPublished.json", "source"), "`source`")
                self.assertEqual(module.link("Wardogs/Config/DefaultGame.ini", "source"), "`source`")

    def test_repo_relative_item_links(self):
        from types import SimpleNamespace
        import attachment_tables as attachments
        import spread_recoil_tables as spread
        path = "data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_001/Content/Data/ID_M4Grip.json"
        expected = f"[`source`]({BLOB}{quote(path, safe='/')})"
        self.assertEqual(attachments.link(SimpleNamespace(path=path, asset="source")), expected)
        self.assertEqual(spread.link({"path": path, "label": "source"}), expected)
        self.assertEqual(attachments.link(SimpleNamespace(path="sdk/raw/WDGame_classes.hpp", asset="source")), "`source`")
        self.assertEqual(spread.link({"path": "data/missing.json", "label": "source"}), "`source`")

    def test_generated_checks_keep_global_source_links(self):
        import contextlib
        import io
        import tempfile
        from unittest.mock import patch
        import attachment_tables as attachments
        import movement_tables as movement
        from raw_source_links import link_generated
        class Capture(io.StringIO):
            def reconfigure(self, **kwargs):
                pass

        source = "`ID_M4` and `data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_002/Content/Data/ID_M4.json`"
        self.assertIn(BLOB, link_generated(source))
        for module in (attachments, movement):
            for newline in ("\n", "\r\n"):
                with self.subTest(generator=module.__name__, newline=repr(newline)), tempfile.TemporaryDirectory() as tmp:
                    page = Path(tmp) / "page.md"
                    text = newline.join(["unchanged prefix", f"<!-- {module.__name__} fixture -->", "stale", f"<!-- /{module.__name__} -->", "unchanged suffix", ""])
                    page.write_bytes(text.encode())
                    mapping = {"fixture": (lambda d: source) if module is attachments else (lambda: source)}
                    modes = "MODES" if module is attachments else "BLOCKS"
                    with contextlib.ExitStack() as stack:
                        stack.enter_context(patch.object(module, "PAGE", str(page)))
                        stack.enter_context(patch.object(module, modes, mapping))
                        stack.enter_context(patch("sys.argv", [module.__name__, "--write"]))
                        stack.enter_context(contextlib.redirect_stdout(Capture()))
                        if module is attachments:
                            stack.enter_context(patch.object(module, "load", return_value=object()))
                        module.main()
                        generated = page.read_text(encoding="utf-8")
                        self.assertIn(link_generated(source), generated)
                        self.assertIn("unchanged prefix", generated)
                        self.assertIn("unchanged suffix", generated)
                        with patch("sys.argv", [module.__name__, "--check"]):
                            self.assertIn(module.main(), (None, 0))
                        first = page.read_bytes()
                        module.main()
                        self.assertEqual(page.read_bytes(), first)

    def test_vehicle_spawn_sources_link_published_json_only(self):
        import json
        import vehicle_spawns
        data = json.loads((ROOT / "assets/data/vehicle-spawns.json").read_text())
        page = vehicle_spawns.render_page(data)
        self.assertIn("https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Config/Experiences", page)
        self.assertNotIn("blob/main/sdk/raw/", page)
        self.assertNotIn("blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleUtility/Config/DefaultVehicleUtility.ini", page)

    def test_vehicle_sections_accept_linked_sources_and_are_idempotent(self):
        import vehicle_tables as vehicles
        doc = (ROOT / "content/Wardogs_AllVehicles_Stats_Damage_v1.md").read_text(encoding="utf-8")
        for section, next_section, render in (("3", "4", vehicles.section3), ("4", "5", vehicles.section4)):
            body = doc[doc.index(f"## {section}. "):doc.index(f"## {next_section}. ")]
            if section == "3":
                body = body[:body.rindex("---")].rstrip("\n")
            generated = render(body)
            self.assertIn(BLOB + "data/", generated)
            self.assertEqual(render(generated), generated)


if __name__ == "__main__":
    unittest.main()
