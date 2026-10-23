"""Tables for game-features/Wardogs_VehicleAssets_v1.md: per-vehicle plugin assets no other page names, rebuilt from data/.

Scope: every export file under Plugins/GameFeatures/Vehicles/* whose file name (without .json) does not appear as a whole
identifier on any other published page (same rule as _tools/doc_coverage.py, with this page left out). Skipped on purpose:
audio (WDAudioData, CrosstalkAudioEvent, REVModelAsset engine-sound models, AEB_* audio event behaviours) and UI radial-wheel slot types. Rows are grouped by the
export's engine type. Each row flattens the export's properties to path=value: tags as their name, object references as
the referenced asset name, curve key lists as time->value points, null/empty values dropped. A cell is cut at CAP characters
and says how many values were left out; files over BIG bytes (tire-model lookup grids, interaction-context tables,
building stages) show only the top-level properties with their leaf-value counts. Blocks sit between

    <!-- vehicle_asset_tables MODE -->  ...  <!-- /vehicle_asset_tables -->

    python _tools/vehicle_asset_tables.py --write      # refresh every block in place
    python _tools/vehicle_asset_tables.py --check      # exit 1 when a block is stale
    python _tools/vehicle_asset_tables.py MODE         # print one block (counts, then one per type section: s0, s1, ...)
    python _tools/vehicle_asset_tables.py sections     # print the section skeleton for a new page
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402
import doc_coverage as dc  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "game-features/Wardogs_VehicleAssets_v1.md"
BLOCK = re.compile(r"<!-- vehicle_asset_tables (\w+) -->\r?\n.*?<!-- /vehicle_asset_tables -->", re.S)
SKIP_TYPES = {"WDAudioData", "WDUIRadialWheelSlotTypeDataAsset", "CrosstalkAudioEvent", "REVModelAsset"}
SKIP_PREFIX = ("AEB_",)  # audio event behaviours
CAP, BIG = 1400, 60000
SECTIONS = [  # (type, title, note)
    ("ModularVehicleVariant", "Vehicle variants (VV_*)", "Spawn bounds, variant tag and the platform each variant assembles."),
    ("WDVehicleWeaponExtensionDataAsset", "Weapon extensions (WE_*)", "Weapon slot, ammo, reload and stats asset for each vehicle weapon."),
    ("WDVehicleInteractionsDataAsset", "Seat and interaction tables", ""),
    ("WDVehicleInteractionContextsData", "Interaction contexts", ""),
    ("WDVehicleGameplayComponentsDataAsset", "Gameplay components", ""),
    ("BHBaseVehicleConfigDataAsset", "Vehicle config", ""),
    ("MTrackedVehicleDynamicsData", "Tracked vehicle dynamics", ""),
    ("MTrackedVehicleSuspensionData", "Tracked vehicle suspension", ""),
    ("MTrackedInputControlsDataAsset", "Tracked input controls", ""),
    ("MLandInputControlsDataAsset", "Wheeled input controls", ""),
    ("MWheeledVehicleCharacteristicsDataAsset", "Wheeled characteristics", ""),
    ("MWheeledVehicleArcadeDataAsset", "Wheeled arcade controls", ""),
    ("MWheeledVehicleWheelDataAsset", "Wheeled axle wheels", ""),
    ("MWheeledVehicleTireModelSimpleDataAsset", "Wheeled simple tire models", ""),
    ("BHSeatSettingsDataAsset", "Seat settings", ""),
    ("BHHelicopterEngineDataAsset", "Helicopter engines", ""),
    ("BHRotaryVehicleBodyDataAsset", "Helicopter bodies", ""),
    ("BHRotaryVehicleSensorsDataAsset", "Helicopter sensors", ""),
    ("MRotaryInputControlsDataAsset", "Helicopter input controls", ""),
    ("MVehicleSensorsDataAsset", "Vehicle sensors", ""),
    ("MVehicleSpringArmDataAsset", "Camera spring arms (tracked, spawner)", ""),
    ("MLandVehicleSpringArmDataAsset", "Camera spring arms (stationary)", ""),
    ("MRotaryVehicleSpringArmDataAsset", "Camera spring arms (helicopter)", ""),
    ("CurveFloat", "Curves (camera, yaw drag, rotor RPM)", ""),
    ("WDAttributeEffectsTrigger_VehicleHealth", "Vehicle health attribute triggers", ""),
    ("PDA_CBM_Map_C", "Control bus mix maps", "Maps vehicle state to control-bus names; the bus mixes themselves are audio and are not documented."),
    ("BHInventoryFragment_SubSlotSupport", "Vehicle inventories (sub-slots)", ""),
    ("BHInventoryFragment_CustomShape", "Inventory custom shapes", ""),
    ("BHInventoryItemDefinition", "Inventory item definitions", ""),
    ("B_SupplyCrate_Free_C", "Supply crate blueprint", ""),
    ("BuildingStagesDefinition", "Buildable stage definitions (stationary vehicles)", "Large files: only top-level properties with leaf counts."),
    ("WDDeploymentBoardVehicleConfigExtension", "Deployment board extension", ""),
]


def short(o):
    on = str(o.get("ObjectName", ""))
    return on.split("'")[-2] if "'" in on else str(o.get("ObjectPath", "")).rsplit("/", 1)[-1].split(".")[0]


def leaves(o, path, out):
    if o is None or o == "" or o == [] or o == {}:
        return
    if isinstance(o, dict):
        if "TagName" in o and len(o) == 1:
            out.append((path, str(o["TagName"])))
        elif "ObjectPath" in o and "ObjectName" in o:
            out.append((path, short(o)))
        elif isinstance(o.get("Keys"), list) and o["Keys"] and all(isinstance(k, dict) and "Time" in k for k in o["Keys"]):
            pts = ", ".join(f"{ct.n(k['Time'])}->{ct.n(k.get('Value', 0))}" for k in o["Keys"][:16])
            out.append((path + ".Keys", f"{len(o['Keys'])} pts: {pts}" + (" ..." if len(o["Keys"]) > 16 else "")))
        else:
            for k, v in o.items():
                leaves(v, f"{path}.{k}" if path else k, out)
    elif isinstance(o, list):
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in o):
            out.append((path, "[" + ", ".join(ct.n(v) for v in o) + "]"))
        else:
            for i, v in enumerate(o):
                leaves(v, f"{path}[{i}]", out)
    elif isinstance(o, bool):
        out.append((path, str(o).lower()))
    elif isinstance(o, (int, float)):
        out.append((path, ct.n(o)))
    else:
        s = str(o)
        out.append((path, s.split("::")[-1] if "::" in s else s))


def summarize(props):
    rows = []
    for k, v in props.items():
        lv = []
        leaves(v, k, lv)
        if lv:
            rows.append(f"`{k}` {len(lv)}")
    return "top-level properties (leaf values): " + ", ".join(rows)


def render(exports, size):
    cells = []
    for e in exports:
        props = e.get("Properties") or {}
        if size > BIG:
            cells.append(summarize(props))
            continue
        lv = []
        leaves(props, "", lv)
        out, used = [], 0
        for p, v in lv:
            piece = f"`{p}`={v}"
            if used + len(piece) > CAP and out:
                break
            out.append(piece)
            used += len(piece) + 2
        left = len(lv) - len(out)
        cells.append(("`" + e["Name"] + "` " if len(exports) > 1 else "") + "; ".join(out) + (f" (+{left} more values)" if left else ""))
    return cells[0] if len(cells) == 1 else " / ".join(cells[:3]) + (f" / (+{len(cells) - 3} more exports)" if len(cells) > 3 else "")


def others_tokens():
    toks = set()
    me = os.path.abspath(os.path.join(ROOT, PAGE))
    for base, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(base, ROOT).replace("\\", "/")
        if rel == ".":
            dirs[:] = [d for d in dirs if d not in dc.EXCLUDE and not d.startswith(".")]
        for f in files:
            full = os.path.join(base, f)
            if f.endswith(".md") and (rel != "." or f not in dc.EXCLUDE_FILES) and os.path.abspath(full) != me:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    toks.update(dc.TOKEN.findall(fh.read()))
    return toks


def folder(rel):
    parts = rel.split("/")
    return parts[parts.index("Vehicles") + 1]


def load():
    toks = others_tokens()
    groups = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(DATA, "Wardogs", "Plugins", "GameFeatures", "Vehicles", "**", "*.json"), recursive=True)):
        if os.path.basename(f)[:-5] in toks:
            continue
        es = ct.exports(f)
        if es[0]["Type"] in SKIP_TYPES or es[0]["Type"].startswith(SKIP_PREFIX):
            continue
        groups[es[0]["Type"]].append((ct.rel_of(f), es, os.path.getsize(f)))
    return groups


def section_types(d):
    known = [t for t, _, _ in SECTIONS if t in d]
    return known + sorted(t for t in d if t not in known)


def title_of(t):
    for tt, title, note in SECTIONS:
        if tt == t:
            return title, note
    return t, "Type not in the section list; grouped by its engine class name."


def table(d, t):
    out = ["| Asset | Vehicle folder | Values |", "|---|---|---|"]
    for rel, es, size in sorted(d[t], key=lambda r: (folder(r[0]), r[0])):
        out.append(f"| {ct.link(rel)} | `{folder(rel)}` | {ct.cell(render(es, size))} |")
    return "\n".join(out)


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def counts(d):
    out = ["| Section | Engine type | Assets |", "|---|---|---|"]
    for i, t in enumerate(section_types(d)):
        out.append(f"| {i + 2}. {title_of(t)[0]} | `{t}` | {len(d[t])} |")
    out.append(f"| **Total** | | **{sum(len(v) for v in d.values())}** |")
    return "\n".join(out)


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"
    types = section_types(d)

    def regen(m):
        mode = m.group(1)
        if mode == "counts":
            body = counts(d)
        else:
            i = int(mode[1:])
            body = table(d, types[i]) if i < len(types) else "| (none) |"
        return nl.join([f"<!-- vehicle_asset_tables {mode} -->"] + body.split("\n") + ["<!-- /vehicle_asset_tables -->"])
    return BLOCK.subn(regen, text)


def sections_md(d):
    out = []
    for i, t in enumerate(section_types(d)):
        title, note = title_of(t)
        out += [f"## {i + 2}. {title}", "", f"Engine type `{t}`. {note}".strip(), "", f"<!-- vehicle_asset_tables s{i} -->", "<!-- /vehicle_asset_tables -->", ""]
    return "\n".join(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    d = load()
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(d, text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    if "sections" in args:
        print(sections_md(d))
        return 0
    mode = next((a for a in args if re.fullmatch(r"counts|s\d+", a)), "counts")
    print(counts(d) if mode == "counts" else table(d, section_types(d)[int(mode[1:])]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
