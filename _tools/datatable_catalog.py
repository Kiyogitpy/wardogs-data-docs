"""Catalog of every DataTable export under data/, rebuilt from the JSON.

Pages: content/Wardogs_DataTables_v1.md (index) and the child pages content/Wardogs_DataTables_<Group>_v1.md.
Each generated block sits between

    <!-- datatable_catalog MODE -->  ...  <!-- /datatable_catalog -->

MODE is "index" or "struct <RowStruct>". Rerun after a data update (idempotent):

    python _tools/datatable_catalog.py --write          # refresh every block on every catalog page
    python _tools/datatable_catalog.py index            # print the index
    python _tools/datatable_catalog.py struct NAME      # print one expanded struct
    python _tools/datatable_catalog.py stats            # counts

Expansion is generic: one markdown row per data-table row. Nested structs become dotted keys, gameplay
tags are printed as tag names, object references as asset names, arrays are joined with ", ". Columns
that are empty in every row of the struct are dropped. Output is sorted by table name, then by the row
order stored in the export.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
BLOCK = re.compile(r"<!-- datatable_catalog ([^>]+?) -->\r?\n.*?<!-- /datatable_catalog -->", re.S)
INDEX_PAGE = "content/Wardogs_DataTables_v1.md"
PAGE_GLOB = "content/Wardogs_DataTables*_v1.md"

# --- dispositions ---------------------------------------------------------------------------------
AUDIO = {"WDImpulseResonanceEntry", "WDMusicState", "WDRainSpotEntry", "WDVoxBase", "WDUIActionSoundTableRow"}
UI_WIDGET = {
    "RichTextStyleRow", "RichImageRow", "WDPostProcessEffect", "WDUIVehicleCrosshairDataTableRow",
    "WDUITrackerDataTableRow", "WDUITaggedIconRow", "WDUIRadialWheelSlotTypeTableRow", "WDUIRadialWheelTableRow",
    "WDUIIndicatorTableRow", "SDUINotificationDataRow", "WDUIPingAction", "WDUIInteractionContextDataTableRow",
    "WDUIInteractionContextStateDataTableRow", "WDUIInteractableComponentStateDataTableRow",
    "WDUIMaterialTrackerDataTableRow", "WDUITaggedWidgetParamsRow", "WDUIPopupTypeDataTableRow",
    "WDUIPopupOptionDataTableRow", "WDUIPopupButtonDataTableRow", "WDUIScopeReticleType", "WDReticleAssetInfo",
    "FToolFont", "WDUIFlairBasicPaintType", "WDFlairMaskInfo", "GrassLayerInfo", "WDUITooltipDataTableRow",
    "WDPlacementUiTextRecord", "WDUIInputActionDataTableRow", "WDUIVendorType",
}
OWNED = {  # expanded by another page this round, index only
    "WDMetaSkillEffectsTaggedTableRow": "teammate B", "WDLiveCurveTableRow": "teammate B",
    "WDCurrencyDefinition": "teammate B", "WDCosmeticData": "teammate B",
    "WDVendorData": "teammate C", "BHEntityData_UI": "teammate C", "WDBuildableDataTableRow": "teammate C",
    "WDVehicleSeatNameOverrideRow": "teammate C", "WDDamageableEntityTableRow": "teammate C",
    "WDUIGameplayTagToTextTableRow": "teammate D",
}
COVERED = {  # already expanded by a dedicated generator: struct -> (label, page)
    "BHUserSettingDataTableRow": ("Settings and Inputs", "content/Wardogs_SettingsAndInputs_v1.md"),
    "WDChallengeDefinition": ("Challenges", "game-features/Wardogs_Challenges_v1.md"),
    "WDChallengeRewardDefinition": ("Challenges", "game-features/Wardogs_Challenges_v1.md"),
    "WDVariantRewardLookupRow": ("Reward Lookup (Session Events)", "content/Wardogs_RewardLookup_SessionEvents_v1.md"),
    "WDCustomRewardTableRow": ("Buildables", "game-features/Wardogs_Buildables_v1.md"),
    "WDVehicleSlotPartRow": ("Vehicle Handling", "game-features/Wardogs_VehicleHandling_v1.md"),
    "WDBoneDamageModifierData": ("All Vehicles Stats and Damage", "content/Wardogs_AllVehicles_Stats_Damage_v1.md"),
    "WDArchetypeCaliberDamageModifierData": ("All Vehicles Stats and Damage", "content/Wardogs_AllVehicles_Stats_Damage_v1.md"),
    "WDAmmoTypeEffectivenessData": ("All Vehicles Stats and Damage", "content/Wardogs_AllVehicles_Stats_Damage_v1.md"),
}

# group name -> (page suffix, title, structs); anything not listed falls in "Other"
GROUPS = [
    ("Economy", "Economy and Rewards", ["WDRewardTableRow", "WDResourceRewardTableRow", "WDAssistResourceRewardTableRow",
        "WDResourceRewardModifierTableRow", "WDRewardFeedActionDataTableRow", "WDEventFeedActionDataTableRow",
        "WDRewardDefinition", "WDGoldMarketItemTableRow", "WDExchangeDefinitionTableRow", "WDMockInvestmentItemTableRow",
        "WDFactoryRecipe", "WDWagerConditionDefinition", "WDWagerActionDefinition", "WDWagerObjectiveCatalogDefinition",
        "WDWagerPricingDefinition", "WDLootableDataTable", "WDControlZoneContributionModifierTableRow",
        "WDMissionDefinition", "WDAchievementDefinition"]),
    ("Meta", "Meta Progression and Cosmetics", ["WDMetaTreeNodeData_UI", "WDMetaTreeTableRow", "WDMetaMasteryDefinitionTableRow",
        "WDMetaSeasonDefinitionTableRow", "WDCosmeticSetData", "WDEmoteData", "WDPlayerIdentityRow", "WDFactionDataTableRow"]),
    ("Combat", "Combat, Vehicles and Scene Data", ["WDVehicleSeatDamageReductionData", "FVehiclePropEntry",
        "WDAmmoModifierTableRow", "WDDeathmatchWeaponData", "WDSceneDataTableRow", "BHGameplayEffectTaggedTableRow", "WDAssistanceRequestData",
        "WDPingTypeData", "WDVoxBase"]),
    ("Frontend", "Frontend, Server and Test Data", ["WDLoadingScreenTips", "WDExperienceServerBrowserTagRow",
        "WDServerBrowserRegionData", "WDUIServerBrowserMapTextureTableRow", "WDUIUserSettingDisplayDataTableRow",
        "WDUIScoreboardStatTableRow", "WDUILevelTableRow", "WDUISquadIntentTableRow", "WDUIDeploymentBoardRejectionTableRow",
        "WDDevMenuMapsDataTableRow", "WDClientHotConfigTableRow", "WDAutomatedTestServerProfile", "WDAutomatedTestClientProfile"]),
]
CELL_MAX = 110
LIST_MAX = 6
COLS_PER_TABLE = 7


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def load_tables():
    tabs = []
    for p in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8") as f:
            t = f.read()
        if '"Type": "DataTable"' not in t and '"Type": "CompositeDataTable"' not in t:
            continue
        for part in EXPORT.split(t)[1:]:
            try:
                d = json.loads(part)
            except ValueError:
                continue
            if d.get("Type") not in ("DataTable", "CompositeDataTable"):
                continue
            rs = (d.get("Properties") or {}).get("RowStruct") or {}
            name = rs.get("ObjectName", "")
            struct = name.split("'")[-2] if "'" in name else (name or "(none)")
            tabs.append({"name": d["Name"], "struct": struct, "path": rel(p), "rows": d.get("Rows") or {}})
    tabs.sort(key=lambda t: (t["struct"], t["name"], t["path"]))
    return tabs


_TABS = None


def tables():
    global _TABS
    if _TABS is None:
        _TABS = load_tables()
    return _TABS


def md_files():
    out = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        r = rel(p)
        if r.startswith(("data/", "graphify-out/", "node_modules/", "_site/", "vendor/")):
            continue
        if re.match(r"content/Wardogs_DataTables.*_v1\.md$", r):
            continue
        out.append(r)
    return sorted(out)


_MENT = None


def mentions():
    global _MENT
    if _MENT is None:
        texts = {}
        for r in md_files():
            with open(os.path.join(ROOT, r), encoding="utf-8", errors="replace") as f:
                texts[r] = f.read()
        # collect candidate tokens once, then intersect
        tok = re.compile(r"[A-Za-z0-9_]+")
        sets = {r: set(tok.findall(t)) for r, t in texts.items()}
        _MENT = {}
        for t in tables():
            _MENT[t["name"]] = [r for r in sorted(sets) if t["name"] in sets[r]]
    return _MENT


# --- flattening -----------------------------------------------------------------------------------

def asset_name(s):
    base = s.rsplit("/", 1)[-1]
    if "." in base:
        a, b = base.rsplit(".", 1)
        base = b if a == b else base
    return base


def num(x):
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        s = f"{x:.5f}".rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    return str(x)


def scalar_text(v):
    if isinstance(v, str):
        if "::" in v and " " not in v:
            return v.split("::")[-1]
        m = re.match(r"^(?:Class|BlueprintGeneratedClass|Package)'(.+?)'$", v)
        return m.group(1) if m else v
    return num(v)


def flat(v, key, out):
    """Flatten v into out[key] = text. Dicts become dotted keys; leaves become short text."""
    if isinstance(v, dict):
        if "TagName" in v and len(v) == 1:
            out[key] = "" if v["TagName"] == "None" else v["TagName"]
        elif "AssetPathName" in v:
            p = v["AssetPathName"]
            out[key] = "" if p in ("", "None") else asset_name(p)
        elif "ObjectName" in v:
            on = v["ObjectName"]
            m = re.match(r"^\w+'(.+)'$", on)
            out[key] = asset_name(m.group(1)) if m else asset_name(on)
        elif {"SourceString", "Key"} & set(v) and "LocalizedString" not in v and all(
                k in ("TableId", "Key", "SourceString", "LocalizedString", "CultureInvariantString", "Namespace", "Flags") for k in v):
            out[key] = v.get("SourceString") or v.get("LocalizedString") or v.get("CultureInvariantString") or v.get("Key", "")
        elif "LocalizedString" in v or "CultureInvariantString" in v:
            out[key] = v.get("LocalizedString") or v.get("CultureInvariantString") or ""
        elif not v:
            out[key] = ""
        else:
            for k, x in v.items():
                flat(x, f"{key}.{k}" if key else k, out)
    elif isinstance(v, list):
        parts = []
        for x in v[:LIST_MAX]:
            sub = {}
            flat(x, "", sub)
            if len(sub) == 1 and "" in sub:
                parts.append(sub[""])
            else:
                parts.append("{" + "; ".join(f"{k}={t}" for k, t in sub.items() if t != "") + "}")
        s = ", ".join(p for p in parts if p != "")
        if len(v) > LIST_MAX:
            s += f" (+{len(v) - LIST_MAX} more)"
        out[key] = s
    elif v is None:
        out[key] = ""
    else:
        out[key] = scalar_text(v)


def clip(s):
    s = s.replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return s if len(s) <= CELL_MAX else s[:CELL_MAX - 1] + "…"


def expand(struct):
    """Return (columns, rows) with rows = [(table, rowname, {col: text})]; empty columns dropped."""
    rows, cols = [], []
    for t in tables():
        if t["struct"] != struct:
            continue
        for rn, rv in t["rows"].items():
            out = {}
            flat(rv, "", out)
            for k in out:
                if k not in cols:
                    cols.append(k)
            rows.append((t["name"], rn, out))
    cols = [c for c in cols if any(r[2].get(c, "") != "" for r in rows)]
    return cols, rows


def block_struct(struct):
    cols, rows = expand(struct)
    ntab = len({r[0] for r in rows})
    if not rows:
        return f"*No rows ({sum(1 for t in tables() if t['struct'] == struct)} empty tables).*"
    lines = [f"*{ntab} table(s), {len(rows)} rows, {len(cols)} non-empty columns. Source: the `Rows` of each table export (**Data**).*", ""]
    chunks = [cols[i:i + COLS_PER_TABLE] for i in range(0, len(cols), COLS_PER_TABLE)] or [[]]
    for ci, ch in enumerate(chunks):
        if len(chunks) > 1:
            lines += [f"Columns {ci * COLS_PER_TABLE + 1}-{ci * COLS_PER_TABLE + len(ch)} of {len(cols)}:", ""]
        multi = ntab > 1
        head = (["Table"] if multi else []) + ["Row"] + [f"`{c}`" if c else "value" for c in ch]
        lines.append("| " + " | ".join(head) + " |")
        lines.append("|" + "---|" * len(head))
        for tn, rn, out in rows:
            cells = ([f"`{tn}`"] if multi else []) + [f"`{clip(rn)}`"] + [clip(out.get(c, "")) for c in ch]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines).rstrip()


# --- index ----------------------------------------------------------------------------------------

def page_of_struct(struct):
    for suffix, title, structs in GROUPS:
        if struct in structs:
            return f"content/Wardogs_DataTables_{suffix}_v1.md", title
    return None, None


def anchor(struct):
    return struct.lower()


def disposition(struct):
    if struct in AUDIO:
        return "Audio table, skipped"
    if struct in UI_WIDGET:
        return "UI widget table, not expanded"
    if struct in OWNED:
        return "Index only (expanded on another page)"
    if struct in COVERED:
        label, page = COVERED[struct]
        return f"Expanded on [{label}](../{page})"
    page, title = page_of_struct(struct)
    if page:
        return f"Expanded in [{title}]({os.path.basename(page)}#{anchor(struct)})"
    return "Not expanded"


def block_index():
    ment = mentions()
    by = {}
    for t in tables():
        by.setdefault(t["struct"], []).append(t)
    lines = []
    for s in sorted(by, key=lambda s: (-sum(len(t["rows"]) for t in by[s]), s)):
        ts = by[s]
        nrows = sum(len(t["rows"]) for t in ts)
        undoc = sum(1 for t in ts if not ment[t["name"]])
        lines += [f"#### {s}", "",
                  f"{len(ts)} table(s), {nrows} rows, {len(ts) - undoc} named in docs. {disposition(s)}.", ""]
        lines += ["| Table | Rows | Folder | Documented in |", "|---|---|---|---|"]
        for t in ts:
            link = f"`{t['name']}`"
            pages = ment[t["name"]]
            shown = ", ".join(f"[{os.path.basename(p)[:-3]}](../{p})" for p in pages[:3])
            if len(pages) > 3:
                shown += f" (+{len(pages) - 3})"
            folder = os.path.dirname(t["path"]).replace("data/Wardogs/", "")
            folder = folder.replace("Plugins/GameFeatures/", "GF/").replace("Content/", "")
            lines.append(f"| {link} | {len(t['rows'])} | `{folder}` | {shown or 'not named'} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def stats():
    ment = mentions()
    tabs = tables()
    by = {}
    for t in tabs:
        by.setdefault(t["struct"], []).append(t)
    exp_structs = [s for s in by if disposition(s).startswith("Expanded in")]
    rows = sum(len(t["rows"]) for s in exp_structs for t in by[s])
    named = sum(1 for t in tabs if ment[t["name"]])
    return (f"{len(tabs)} tables, {len(by)} row structs; expanded here: {len(exp_structs)} structs, "
            f"{sum(len(by[s]) for s in exp_structs)} tables, {rows} rows; "
            f"named in docs: {named} of {len(tabs)} (without catalog pages)")


def render(mode):
    if mode == "index":
        return block_index()
    if mode.startswith("struct "):
        return block_struct(mode[7:].strip())
    raise SystemExit(f"unknown mode {mode}")


def write_all():
    total = 0
    for p in sorted(glob.glob(os.path.join(ROOT, PAGE_GLOB))):
        with open(p, encoding="utf-8", newline="") as f:
            text = f.read()
        n = [0]

        def sub(m):
            n[0] += 1
            return f"<!-- datatable_catalog {m.group(1)} -->\n{render(m.group(1))}\n<!-- /datatable_catalog -->"
        new = BLOCK.sub(sub, text)
        if new != text:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        total += n[0]
        print(f"{rel(p)}: {n[0]} blocks")
    print(f"{total} blocks refreshed")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--write":
        write_all()
    elif a[0] == "stats":
        print(stats())
    elif a[0] == "index":
        print(block_index())
    elif a[0] == "struct" and len(a) > 1:
        print(block_struct(a[1]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
