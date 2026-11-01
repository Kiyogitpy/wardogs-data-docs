"""review_pages.py regressions on a synthetic repo. Run: python -I -m unittest discover -s _tools -p test_review_pages.py -v"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import review_pages  # noqa: E402

AK = "Wardogs/Content/Weapons/Rifles/BP_Rifle_AK.json"
FRAG = "Wardogs/Content/Items/Throwables/BP_Throw_Frag.json"
MINE = "Wardogs/Content/Items/Placed/BP_OldMine.json"
CLAY = "Wardogs/Content/Items/Placed/Claymore.json"
PRICE = "Wardogs/Content/Items/Shop/DT_Prices.json"


def export(name, props):
    return "--- export: UObject / %s ---\n%s\n" % (name, json.dumps({"Type": "T", "Name": name, "Properties": props}, indent=2))


def put(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build(tmp):
    """-> (repo, diff_path). Old/new data trees with 2 changed assets, 1 removed, 1 bare-name asset, 1 unreferenced."""
    repo, od, nd = (os.path.join(tmp, d) for d in ("repo", "old/data", "new/data"))
    extra = export("AK_Alias", {}) + export("Shared_Sub_0", {})       # another export name (link_sources alias) and a numbered sub-object
    put(od, AK, export("BP_Rifle_AK_C_0", {"MuzzleVelocity": 2000, "Damage": 30, "Tag": "Rifle.AK"}) + extra)
    put(nd, AK, export("BP_Rifle_AK_C_0", {"MuzzleVelocity": 2200, "Damage": 32, "Tag": "Rifle.AK"}) + extra)
    put(od, FRAG, export("BP_Throw_Frag_C_0", {"ThrowSpeed": 1500, "Fuse": 3.5, "Radius": 7.25}))
    put(nd, FRAG, export("BP_Throw_Frag_C_0", {"ThrowSpeed": 1700, "Fuse": 3.5, "Radius": 7.5}))
    put(od, MINE, export("BP_OldMine_C_0", {"Damage": 300}))
    put(od, CLAY, export("Claymore_C_0", {"Angle": 60}))
    put(nd, CLAY, export("Claymore_C_0", {"Angle": 55}))
    put(od, PRICE, export("DT_Prices", {"A": 1}))
    put(nd, PRICE, export("DT_Prices", {"A": 2}))
    # hand-written wiki article that names the asset
    put(repo, "_wiki/weapons/ak.md", "---\ntitle: AK Rifle\n---\n\n# AK Rifle\n\nMuzzle velocity is 2,000 cm/s.\nSource asset: `BP_Rifle_AK`.\nDamage is 30 per hit.\n")
    # wiki article that never names the asset: cites a reference page that does
    put(repo, "_wiki/equipment/frag-grenade.md", "---\ntitle: Frag Grenade\n---\n\n# Frag Grenade\n\nThrown at 1500 cm/s. Blast radius 7.25 m.\n\n## Sources\n\n- [Throwables](../../game-features/Throwables.md)\n")
    # same, but the reference line does not carry the article title (weaker)
    # title differs from the reference page wording, but its Internal name tag is on the reference line
    put(repo, "_wiki/equipment/frag-alt.md", "---\ntitle: Pineapple\n---\n\n| Internal name | `Id.Item.Frag` |\n\n- [Throwables](../../game-features/Throwables.md)\n")
    # cites only the Season 2 change log, which names the frag asset: not a reason to review it
    put(repo, "_wiki/equipment/hist-only.md", "---\ntitle: Hist\n---\n- [S2](../../season-2-changes/items.md)\n")
    put(repo, "_wiki/equipment/smoke.md", "---\ntitle: Smoke\n---\n\nSmoke lasts a while.\n\n- [Throwables](../../game-features/Throwables.md)\n")
    # wiki article linking only to a data folder
    put(repo, "_wiki/equipment/folder.md", "---\ntitle: Placed\n---\n\nSee [folder](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Placed).\n")
    # reference page: prose + generated block + bare word in prose
    put(repo, "game-features/Throwables.md", "# Throwables\n\n| Frag Grenade | `BP_Throw_Frag` | 1500 | Id.Item.Frag |\n\n<!-- test_tables rows -->\n| BP_Rifle_AK | 2000 |\n<!-- /test_tables -->\n\nThe claymore is a Claymore mine, see BP_OldMine.\n" + "\n" * 10 + "Thrown at 1500 elsewhere.\n")
    # only in a generated block -> generated
    put(repo, "content/Generated.md", "# G\n\n<!-- test_tables a -->\n| BP_Throw_Frag | 1500 |\n<!-- /test_tables -->\n")
    put(repo, "assets/data/frag.json", json.dumps({"asset": "BP_Throw_Frag"}))
    # historical log
    put(repo, "season-2-changes/items.md", "Changed `BP_Throw_Frag` from 1200.\n")
    # a bare word in prose only must not hit; the same word in backticks must
    put(repo, "content/Folder.md", "[x](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Claymore/Other.json)\n")
    put(repo, "content/Alias.md", "The AK_Alias export, but not Shared_Sub_0.\n")
    put(repo, "content/Prose.md", "A Claymore is a mine.\n")
    put(repo, "content/Ticks.md", "The `Claymore` asset angle is 60.\n")
    diff = {"old": od, "new": nd, "added": ["Wardogs/New.json"], "removed": [MINE],
            "changed": [{"file": f, "area": "x", "nchanges": 2, "top_fields": [], "examples": ["/Properties/MuzzleVelocity: 2000 -> 2200"]} for f in (AK, FRAG, CLAY, PRICE)]}
    dp = os.path.join(tmp, "new", "patch-diff.json")
    put(os.path.dirname(dp), "patch-diff.json", json.dumps(diff))
    return repo, dp


class ReviewPages(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.repo, self.diff = build(self.tmp)
        self.summary, self.out = review_pages.run(self.diff, self.repo)
        with open(os.path.join(self.out, "review-pages.json"), encoding="utf-8") as f:
            self.js = json.load(f)
        with open(os.path.join(self.out, "review-pages.md"), encoding="utf-8") as f:
            self.md = f.read()
        self.pages = {p["page"]: p for p in self.js["pages"]}

    def test_outputs_sit_next_to_the_diff(self):
        self.assertEqual(self.out, os.path.dirname(self.diff))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "review-pages.md")))

    def test_hand_written_direct_hit_shows_values_and_lines(self):
        p = self.pages["_wiki/weapons/ak.md"]
        self.assertEqual((p["class"], p["relation"], p["kind"]), ("hand-written", "direct", "wiki"))
        a = p["assets"][0]
        self.assertEqual(a["file"], AK)
        why = {l["n"]: l["why"] for l in a["lines"]}
        self.assertIn("names `BP_Rifle_AK`", why[8])            # the backticked mention
        self.assertIn("old value 2,000 (Properties.MuzzleVelocity)", why[7])   # page says 2,000, data went 2000 -> 2200
        self.assertNotIn(9, why)                                     # "30" is too common a number to search for
        self.assertIn("MuzzleVelocity: 2000 -> 2200", self.md.replace("`", "").replace("/Properties/", "").replace("Properties/", ""))

    def test_wiki_comes_before_other_hand_written_and_generated_last(self):
        hand = [p["page"] for p in self.js["pages"] if p["class"] == "hand-written" and p["relation"] == "direct" and not p["historical"]]
        self.assertEqual(hand, ["_wiki/weapons/ak.md", "content/Alias.md", "content/Ticks.md", "game-features/Throwables.md"])
        classes = [p["class"] for p in self.js["pages"]]
        self.assertEqual(classes, sorted(classes, key=lambda c: c != "hand-written"))

    def test_generated_block_hits_do_not_count_as_hand_written(self):
        g = self.pages["content/Generated.md"]
        self.assertEqual(g["class"], "generated")
        self.assertEqual(self.pages["assets/data/frag.json"]["class"], "generated")
        ref = self.pages["game-features/Throwables.md"]
        self.assertEqual([a["file"] for a in ref["assets"]], [MINE, FRAG])      # BP_Rifle_AK is only inside the generated block
        self.assertEqual(ref["generated_block_assets"], [AK])

    def test_bare_name_needs_backticks_or_a_path(self):
        self.assertNotIn("content/Prose.md", self.pages)
        self.assertIn("content/Ticks.md", self.pages)
        self.assertEqual([a["file"] for a in self.pages["game-features/Throwables.md"]["assets"]].count(CLAY), 0)

    def test_removed_asset_is_flagged(self):
        a = next(x for x in self.pages["game-features/Throwables.md"]["assets"] if x["file"] == MINE)
        self.assertEqual(a["status"], "removed")
        self.assertIn("REMOVED", self.md)

    def test_indirect_wiki_hit_through_cited_reference_page(self):
        p = self.pages["_wiki/equipment/frag-grenade.md"]
        self.assertEqual((p["class"], p["relation"]), ("hand-written", "indirect"))
        self.assertEqual(p["via"][0]["cites"], "game-features/Throwables.md")
        self.assertEqual(p["via"][0]["assets"], [FRAG])             # not the mine or rifle the same page also names
        self.assertEqual([a["file"] for a in p["assets"]], [FRAG])
        self.assertEqual(len(self.pages["_wiki/equipment/smoke.md"]["assets"]), 3)   # no title match: every asset the cited page names
        self.assertTrue(p["title_match"])                          # reference line holds "Frag Grenade"
        self.assertTrue(any("1500" in l["text"] for l in p["lines"]))   # page quotes the old 1500 throw speed
        self.assertFalse(self.pages["_wiki/equipment/smoke.md"]["title_match"])
        order = [r["page"] for r in self.js["pages"] if r["relation"] == "indirect"]
        self.assertLess(order.index("_wiki/equipment/frag-grenade.md"), order.index("_wiki/equipment/smoke.md"))

    def test_internal_name_tag_also_makes_an_indirect_hit_likely(self):
        p = self.pages["_wiki/equipment/frag-alt.md"]
        self.assertTrue(p["title_match"])
        self.assertEqual([a["file"] for a in p["assets"]], [FRAG])

    def test_export_name_alias_hits_but_numbered_sub_objects_do_not(self):
        a = next(x for x in self.js["assets"] if x["file"] == AK)
        self.assertEqual(a["aliases"], ["AK_Alias"])
        self.assertEqual([x["file"] for x in self.pages["content/Alias.md"]["assets"]], [AK])

    def test_folder_in_another_pages_path_is_not_a_mention(self):
        # Claymore.json exists, but `.../Items/Claymore/Other.json` only passes through a folder of that name
        self.assertNotIn("content/Folder.md", self.pages)

    def test_value_far_from_any_mention_is_not_shown_for_a_direct_hit(self):
        shown = [l["text"] for a in self.pages["game-features/Throwables.md"]["assets"] for l in a["lines"]]
        self.assertNotIn("Thrown at 1500 elsewhere.", shown)       # more than NEAR lines from any line naming the asset

    def test_indirect_hit_through_data_folder_link(self):
        p = self.pages["_wiki/equipment/folder.md"]
        self.assertEqual(p["relation"], "indirect")
        self.assertEqual(sorted(p["via"][0]["assets"]), [MINE, CLAY])

    def test_direct_hit_is_not_repeated_as_indirect(self):
        self.assertEqual([p["relation"] for p in self.js["pages"] if p["page"] == "_wiki/weapons/ak.md"], ["direct"])

    def test_citing_only_a_change_log_is_not_an_indirect_hit(self):
        self.assertNotIn("_wiki/equipment/hist-only.md", self.pages)

    def test_historical_pages_are_set_apart(self):
        h = self.pages["season-2-changes/items.md"]
        self.assertTrue(h["historical"])
        self.assertIn("## 3. Historical", self.md)
        self.assertEqual(self.summary["historical"], 1)

    def test_unreferenced_asset_is_counted_but_not_listed_under_pages(self):
        row = next(a for a in self.js["assets"] if a["file"] == PRICE)
        self.assertEqual(row["pages"], [])
        self.assertEqual(self.summary["assets_without_pages"], 1)

    def test_summary_counts_and_added_assets(self):
        s = self.summary
        self.assertEqual((s["changed"], s["removed"], s["added_not_scanned"]), (4, 1, 1))
        self.assertEqual(s["hand_written_direct_wiki"], 1)
        self.assertEqual(s["hand_written_indirect_wiki"], 4)       # frag-grenade, frag-alt, smoke, folder
        self.assertEqual(s["hand_written_indirect_wiki_likely"], 2)
        self.assertIn("| Removed assets | 1 |", self.md)

    def test_falls_back_to_diff_examples_when_old_data_is_gone(self):
        import shutil
        shutil.rmtree(os.path.join(self.tmp, "old"))
        review_pages.run(self.diff, self.repo, os.path.join(self.tmp, "again"))
        with open(os.path.join(self.tmp, "again", "review-pages.json"), encoding="utf-8") as f:
            js = json.load(f)
        a = next(x for x in js["assets"] if x["file"] == AK)
        self.assertEqual(a["value_source"], "examples")
        self.assertEqual((a["fields"][0]["old"], a["fields"][0]["new"]), (2000.0, 2200.0))

    def test_output_is_deterministic(self):
        review_pages.run(self.diff, self.repo, os.path.join(self.tmp, "again"))
        for n in ("review-pages.md", "review-pages.json"):
            with open(os.path.join(self.out, n), "rb") as a, open(os.path.join(self.tmp, "again", n), "rb") as b:
                self.assertEqual(a.read(), b.read())

    def test_generated_line_detection(self):
        lines = ["a", "<!-- x mode -->", "b", "<!-- /x -->", "<!-- TODO fix -->", "c", "<!-- y s1 -->", "<!-- /y -->"]
        self.assertEqual(review_pages.generated_lines(lines), {1, 2, 3, 6, 7})

    def test_value_needles_skip_common_numbers(self):
        self.assertEqual(review_pages.needle_forms(2000), ["2000", "2,000"])
        self.assertEqual(review_pages.needle_forms(5), [])
        self.assertEqual(review_pages.needle_forms(0.25), ["0.25"])
        self.assertEqual(review_pages.needle_forms(1.5), [])

    def test_non_finite_values_are_not_needles(self):
        # a diffed value of "nan" or "inf" used to crash the whole run (int(nan) / int(inf))
        for v in (float("nan"), float("inf"), float("-inf"), "nan", "inf", "-inf"):
            self.assertEqual(review_pages.needle_forms(v), [], v)


if __name__ == "__main__":
    unittest.main()
