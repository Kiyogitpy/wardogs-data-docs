"""Tables for game-features/Wardogs_Buildables_v1.md, rebuilt from data/.

Reads the Buildables item plugin (data/Wardogs/Plugins/GameFeatures/Items/Buildables), the
three cash reward tables under Content/GameMechanics/.../CashRewardsDataTable/Buildable and
the destroyed-cash table next to them. Each table sits between

    <!-- buildable_tables MODE -->  ...  <!-- /buildable_tables -->

on the page. Rerun after a data update (idempotent):

    python _tools/buildable_tables.py --write       # refresh every block in place
    python _tools/buildable_tables.py MODE          # print one block (inventory, placement,
                                                    #   stages, damage, rewards, economy,
                                                    #   special, names, files, stationary, counts)
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raw_source_links import source_link, link_generated  # noqa: E402
import bp_defaults as bpd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "game-features/Wardogs_Buildables_v1.md"
PLUGIN = "Wardogs/Plugins/GameFeatures/Items/Buildables/Content/"
DATA = PLUGIN + "Data/"
CASH = "Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/"
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
BLOCK = re.compile(r"<!-- buildable_tables (\w+) -->\r?\n.*?<!-- /buildable_tables -->", re.S)


def exports(rel):
    with open(os.path.join(ROOT, "data", rel), encoding="utf-8") as f:
        return [json.loads(part) for part in EXPORT.split(f.read())[1:]]


def table(rel):
    return next(e for e in exports(rel) if e.get("Type") == "DataTable")["Rows"]


def n(x):
    return f"{x:,.0f}" if float(x) == int(x) else f"{x:,.2f}".rstrip("0").rstrip(".")


def link(rel, label=None):
    return source_link("data/" + rel, label or os.path.basename(rel)[:-5])


def cls(obj):
    """Short class name of an ObjectName like Class'WDFobPlacementCondition'."""
    name = obj["ObjectName"] if isinstance(obj, dict) else obj
    name = name.split("'")[1] if "'" in name else name
    name = re.sub(r"^B_", "", name)
    return re.sub(r"_C$", "", name)


# --- load ---------------------------------------------------------------------------------------

def load():
    d = {"assets": [], "stages": {}}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", DATA, "Buildables", "**", "DA_*.json"), recursive=True)):
        rel = os.path.relpath(path, os.path.join(ROOT, "data")).replace("\\", "/")
        for e in exports(rel):
            if e["Type"].startswith("WDBuildable") and e["Type"] != "WDBuildablePlacementDataAsset" and "EntityTag" in e["Properties"]:
                d["assets"].append((rel, e["Name"], e["Type"], e["Properties"]))
            elif e["Type"] == "BuildingStagesDefinition":
                d["stages"][e["Name"]] = (rel, e["Properties"])
    d["entity"] = {k.lower(): v for k, v in table(DATA + "DT_EntityData_UI_Buildables.json").items()}
    d["entity_rows"] = table(DATA + "DT_EntityData_UI_Buildables.json")
    d["vendor"] = table(DATA + "DT_VendorData_Ext_Buildables.json")
    d["damage"] = table(DATA + "DT_GlobalDamage_BuildableData.json")
    d["hammer"] = {h: [k.lower() for k in table(DATA + f"{h}Hammer/DT_Buildables_{h}Hammer.json")]
                   for h in ("Small", "Medium", "Large")}
    d["fob_rules"] = next(e for e in exports(DATA + "Buildables/ForwardOperatingBase/DA_FOB_Ruleset.json")
                          if e["Type"] == "WDFOBRulesetData")["Properties"]
    return d


def tag_of(p):
    return p["EntityTag"]["TagName"]


def short(tag):
    return tag.split("Id.Buildable.")[-1]


def display_name(d, p):
    dn = p.get("DisplayName", {})
    name = dn.get("SourceString") or dn.get("LocalizedString")
    if name:
        return name
    row = d["entity"].get(tag_of(p).lower())
    return row["FriendlyName"].get("SourceString") if row else None


def hammers(d, tag):
    t = tag.lower()
    return "".join(h[0] for h in ("Small", "Medium", "Large") if t in d["hammer"][h]) or "-"


def stage_list(d, p):
    ref = p.get("BuildingStagesDefinition")
    if ref:
        name = ref["ObjectName"].split("'")[1]
        if name in d["stages"]:
            return d["stages"][name][1]["Stages"]
    return p.get("BuildingStages") or []


def progress(stage):
    return stage.get("RequiredBuildingProgress")


# --- tables -------------------------------------------------------------------------------------

def inventory(d):
    out = ["| Asset | Tag | Name (UI text) | Supply cost | Max health | Repair multiplier | Stages | Hammers | Part of |",
           "|---|---|---|---|---|---|---|---|---|"]
    for rel, name, typ, p in d["assets"]:
        tag = tag_of(p)
        dn = display_name(d, p)
        parts = [t for t in (short(tag).split(".")) if t]
        part_of = ""
        if len(parts) > 1:
            part_of = parts[0]
        if name.startswith("DA_Buildable_Door_"):
            part_of = "Door"
        if name.startswith("DA_Buildable_Gate_"):
            part_of = "Gate"
        sl = stage_list(d, p)
        stages = str(len(sl)) if sl else "-"
        rep = n(p["RepairSpeedMultiplier"]) if "RepairSpeedMultiplier" in p else "-"
        out.append(f"| {link(rel, name)} | `{tag}` | {dn or '(blank in export)'} | {n(p.get('Cost', 0))} | {n(p.get('MaxHealth', 0))} | "
                   f"{rep} | {stages} | {hammers(d, tag) if not part_of else 'with ' + part_of} | {part_of or '-'} |")
    return "\n".join(out)


def counts(d):
    kinds = {}
    for _, _, typ, _ in d["assets"]:
        kinds[typ] = kinds.get(typ, 0) + 1
    files = glob.glob(os.path.join(ROOT, "data", PLUGIN, "**", "*.json"), recursive=True)
    return "\n".join([
        f"- Files under the Buildables plugin: **{len(files)}**.",
        f"- Buildable data assets: **{len(d['assets'])}** (" + ", ".join(f"{v} `{k}`" for k, v in sorted(kinds.items())) + ").",
        f"- Build-stage definitions: **{len(d['stages'])}**.",
        f"- Rows in the entity name table: **{len(d['entity_rows'])}**; in the vendor table: **{len(d['vendor'])}**; "
        f"in the damage table: **{len(d['damage'])}**.",
        f"- Hammer lists: " + ", ".join(f"{h} {len(v)}" for h, v in d["hammer"].items()) + ".",
    ])


def placement(d):
    out = ["| Asset | Placement conditions | Max stack | Pivot up / side | Max under terrain | Block buffer (free / snapped) | Max surface angle | Registers with FOB | FOB limit |",
           "|---|---|---|---|---|---|---|---|---|"]
    limits = {x["Key"]["TagName"]: x["Value"] for x in d["fob_rules"]["LimitFOBBuildables"]}
    for rel, name, typ, p in d["assets"]:
        conds = ", ".join(f"`{cls(c)}`" for c in p.get("PlacementConditions", [])) or "-"
        pv = p.get("PlacePivotVerticalOffset")
        ph = p.get("PlacePivotHorizontalOffset")
        pivot = (n(pv) if pv is not None else "-") + " / " + (n(ph) if ph is not None else "-")
        buf = "-"
        if "PlacementBlockedPenetrationBuffer" in p:
            buf = f"{n(p['PlacementBlockedPenetrationBuffer'])} / {n(p.get('SnappedPlacementBlockedPenetrationBuffer', 0))}"
        out.append(f"| {link(rel, name)} | {conds} | {p['MaxStack'] if 'MaxStack' in p else '-'} | {pivot} | "
                   f"{n(p['MaxDepthUnderTerrain']) if 'MaxDepthUnderTerrain' in p else '-'} | {buf} | "
                   f"{n(p['MaximumValidSurfaceAngle']) if 'MaximumValidSurfaceAngle' in p else '-'} | "
                   f"{'yes' if p.get('bRegisterWithFOB') else '-'} | {limits.get(tag_of(p), '-')} |")
    return "\n".join(out)


def stages(d):
    out = ["| Stage definition | Stages | Progress thresholds | Meshes per stage | Critical-hit spots per stage |",
           "|---|---|---|---|---|"]
    for name, (rel, p) in sorted(d["stages"].items()):
        st = p["Stages"]
        out.append(f"| {link(rel, name)} | {len(st)} | " + ", ".join(n(progress(s)) for s in st) + " | "
                   + ", ".join(str(len(s.get("MeshToPlacements", []))) for s in st) + " | "
                   + ", ".join(str(len(s.get("CriticalHitSpots", []))) for s in st) + " |")
    inline = [(rel, name, p) for rel, name, typ, p in d["assets"] if p.get("BuildingStages")]
    if inline:
        out.append("")
        out.append("Parts that carry one inline stage in the asset itself (no separate stage file):")
        out.append("")
        out.append("| Asset | Stages | Progress |")
        out.append("|---|---|---|")
        for rel, name, p in inline:
            out.append(f"| {link(rel, name)} | {len(p['BuildingStages'])} | " + ", ".join(n(progress(s)) for s in p["BuildingStages"]) + " |")
    return "\n".join(out)


DAMAGE_COLS = [("Melee", "Meta.Damage.DamageType.Melee"), ("Bullet", "Meta.Damage.Bullet"),
               ("Grenade", "Meta.Damage.Explosive.Grenade"), ("Rocket", "Meta.Damage.Explosive.Rocket"),
               ("C4", "Meta.Damage.Explosive.Utility.C4"), ("IED", "Meta.Damage.Explosive.Utility.IED")]


def single(row, tag):
    for e in row["DamageModificationEntries"]:
        if e["SourceRequirements"] == [tag] and not e["InstigatorRequirements"] and not e["TargetRequirements"] and not e["PossibleHitLocations"]:
            m = e["OutModification"]
            return f"{m['Amount']:+g}%" if m["Operation"].endswith("Percentage_Ongoing") else "none"
    return "-"


def damage(d):
    out = ["| Asset | Max health | Damage row | Entries | " + " | ".join(c for c, _ in DAMAGE_COLS) + " |",
           "|---|---|---|---|" + "---|" * len(DAMAGE_COLS)]
    seen = set()
    for rel, name, typ, p in d["assets"]:
        tag = p.get("DamageEntityData", {}).get("Tag", {}).get("TagName")
        row = d["damage"].get(tag) if tag else None
        cells = [single(row, t) for _, t in DAMAGE_COLS] if row else ["-"] * len(DAMAGE_COLS)
        out.append(f"| {link(rel, name)} | {n(p.get('MaxHealth', 0))} | `{tag or 'none'}`{'' if row else ' (no row)'} | "
                   f"{len(row['DamageModificationEntries']) if row else '-'} | " + " | ".join(cells) + " |")
        seen.add(tag)
    unused = sorted(set(d["damage"]) - seen)
    out.append("")
    out.append("Damage rows that no buildable asset points at: " + (", ".join(f"`{u}`" for u in unused) or "none") + ".")
    return "\n".join(out)


def rewards(d):
    def rows(rel):
        return {k: v for k, v in table(rel).items() if k.startswith("Id.Buildable.")}
    built = rows(CASH + "Buildable/DT_Reward_Cash_BuildableBuilt.json")
    placed = rows(CASH + "Buildable/DT_Reward_Cash_BuildablePlaced.json")
    fob = rows(CASH + "Buildable/DT_Reward_Cash_BuildablePlacedInFOB.json")
    dest = rows(CASH + "Deployable/DT_Reward_Cash_DeployableDestroyed.json")
    tags = sorted(set(built) | set(placed) | set(fob) | set(dest), key=lambda t: t.lower())
    out = ["| Buildable | Built | Placed | Placed in FOB | Destroyed (enemy build) |", "|---|---|---|---|---|"]

    def cell(t, src):
        return n(src[t]["base"]) if t in src else "-"
    for t in tags:
        out.append(f"| `{t}` | {cell(t, built)} | {cell(t, placed)} | {cell(t, fob)} | {cell(t, dest)} |")
    out.append("")
    owner = lambda src: sorted({src[t]["OwnerModifier"] for t in src})
    out.append(f"Friendly modifier on every row above: placed {sorted({placed[t]['FriendlyModifier'] for t in placed})}, "
               f"destroyed {sorted({dest[t]['FriendlyModifier'] for t in dest})}. Owner modifier: built {owner(built)}, "
               f"placed {owner(placed)}, placed in FOB {owner(fob)}, destroyed {owner(dest)}.")
    return "\n".join(out)


def economy(d):
    out = ["| Vendor row | Variation | Price | Amount per purchase | Level to unlock | Lifetime buy limit |", "|---|---|---|---|---|---|"]
    for k, r in d["vendor"].items():
        for v in r["VendorItemVariations"]:
            out.append(f"| `{k}` | `{v['VariationTag']['TagName']}` | {n(v['Price'])} | {v['Amount']} | {v['LevelToUnlock']} | "
                       f"{v['LifeTimeBuyLimit'] or 'none'} |")
    return "\n".join(out)


def special(d):
    out = []
    for rel, name, typ, p in d["assets"]:
        if typ == "WDBuildableHotZoneMagnetDataAsset":
            out.append("| Setting (`" + name + "`) | Value |")
            out.append("|---|---|")
            for k in ("InitialDelayDuration", "HotZoneMagnetRechargeDuration", "HotZoneMagnetMinimumFuel",
                      "HotZoneMagnetDurationPerFuel", "MaxFuel"):
                out.append(f"| `{k}` | {n(p[k])} |")
            out.append(f"| `FuelSuppliesResourceItemTag` | `{p['FuelSuppliesResourceItemTag']['TagName']}` |")
    return "\n".join(out)


def names(d):
    out = ["| Entity tag | UI name | Description (as shown in game) |", "|---|---|---|"]
    for k, r in d["entity_rows"].items():
        desc = (r["Description"].get("SourceString") or "").replace("\r\n", " / ").replace("\n", " / ")
        out.append(f"| `{k}` | {r['FriendlyName'].get('SourceString') or r['FriendlyName'].get('LocalizedString') or 'blank in export'} | {desc or '-'} |")
    return "\n".join(out)


def stationary(d):
    """Stationary weapons (Vehicles/STN_*): the buildable data tables, the registries they are added to, and the
    buildable data asset each row points to."""
    veh = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles")
    data = os.path.join(ROOT, "data")

    def rel(p):
        return os.path.relpath(p, data).replace(os.sep, "/")

    def find(pdir, name):
        return next(iter(glob.glob(os.path.join(pdir, "**", name + ".json"), recursive=True)), None)
    out = ["| Plugin | Table | Added to registries | Row tag | Data asset | Name | Cost | Max health | Repair multiplier | Max stack | Stages | Vehicle tag | Placement conditions |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for pdir in sorted(glob.glob(os.path.join(veh, "STN_*"))):
        plug = os.path.basename(pdir)
        feature = next(e for e in exports(f"Wardogs/Plugins/GameFeatures/Vehicles/{plug}/Content/{plug}.json")
                       if e["Type"] == "GameFeatureAction_DataRegistrySource")
        by_table = {}
        for src in feature["Properties"]["SourcesToAdd"]:
            if src["RegistryToAddTo"].startswith("Buildables_"):
                tname = src["DataTableToAdd"]["AssetPathName"].rsplit("/", 1)[-1].split(".")[0]
                by_table.setdefault(tname, []).append(src["RegistryToAddTo"])
        for tname, regs in by_table.items():
            trel = rel(find(pdir, tname))
            for tag, row in table(trel).items():
                dname = row["BuildableData"]["ObjectName"].split("'")[1]
                drel = rel(find(pdir, dname))
                ex = exports(drel)
                da = next(e for e in ex if e["Type"] == "WDBuildableDataAsset")["Properties"]
                sp = next((e for e in ex if e["Type"] == "WDVehicleBuildSpawner"), None)
                vtag = sp["Properties"]["VehicleTag"]["TagName"] if sp else "-"
                stages = "-"
                if da.get("BuildingStagesDefinition"):
                    spath = find(pdir, da["BuildingStagesDefinition"]["ObjectName"].split("'")[1])
                    if spath:
                        sl = next(e for e in exports(rel(spath)) if e["Type"] == "BuildingStagesDefinition")["Properties"]
                        stages = str(len(sl.get("Stages", [])))
                conds = ", ".join(f"`{cls(c)}`" for c in da.get("PlacementConditions", [])) or "-"
                dn = da.get("DisplayName", {})
                out.append(f"| `{plug}` | {link(trel)} | {', '.join('`' + r + '`' for r in regs)} | `{tag}` | {link(drel, dname)} | "
                           f"{dn.get('SourceString') or dn.get('LocalizedString') or '-'} | {n(da.get('Cost', 0))} | {n(da.get('MaxHealth', 0))} | "
                           f"{n(da['RepairSpeedMultiplier']) if 'RepairSpeedMultiplier' in da else '-'} | {n(da['MaxStack']) if 'MaxStack' in da else '-'} | "
                           f"{stages} | `{vtag}` | {conds} |")
    return "\n".join(out)


def kind(rel):
    base = os.path.basename(rel)[:-5]
    low = rel.lower()
    if "/audio/" in low or base.startswith("AE_") or base.startswith("DA_Item_") and "Audio" in base:
        return "audio"
    if base.startswith("DA_Buildable_") and base.endswith("_Stages") or base.endswith("_Stages"):
        return "build stages"
    if base.startswith("DA_RadialWheelSlotType"):
        return "radial wheel slot"
    if base.startswith("DA_Buildable_") or base == "DA_WoodBase_Stages":
        return "buildable"
    if base.startswith(("ID_", "AnimSet_")) or "/Data/UI/" in rel.replace("\\", "/") or "UI" in base.split("_")[:2]:
        return "item or UI"
    if base.startswith("DT_"):
        return "table"
    if base.startswith("DA_Action") or base.startswith("IMC_"):
        return "action or input"
    return "other"


ROLES = {
    "Data/Actions": "build-tool actions (construct, place, dismantle, rotate, snap, secondary use)",
    "Data/BuildTool": "build tool HUD, radial wheel data, camera FOV curves, hit sound",
    "Data/BuildToolSupply": "Build Supplies item and its audio",
    "Data/Buildables": "shared damage tint curve and global placement settings",
    "Data/Buildables/Audio": "default buildable sound events (placed, constructed, damaged, destroyed)",
    "Data/Buildables/ForwardOperatingBase": "FOB buildable asset, ruleset, interactions, FOB sound events",
    "Data/Buildables/FloorBoard": "radial wheel slot only; no buildable asset in this export",
    "Data/Buildables/Ramp": "radial wheel slot only; no buildable asset in this export",
    "Data/Buildables/WindowBoard": "radial wheel slot only; no buildable asset in this export",
    "Data/Buildables/BarrierDoor": "door buildable, its two parts, stages and destruction definition",
    "Data/Buildables/HBlock_Gate_6x2": "gate buildable, left, right and ramp parts, stages, door destruction definitions",
    "Data/ForwardOperatingBase": "FOB item, animation set, placement texts, interaction and post-process data",
    "Data/FuelSupplies": "Fuel Supplies item and audio",
    "Data/LargeHammer": "Large Hammer item, animations, audio and its placeable list",
    "Data/MediumHammer": "Medium Hammer item, animations, audio and its placeable list",
    "Data/SmallHammer": "Small Hammer item, animations, audio and its placeable list",
    "Data/MunitionsSupplies": "Ammo Supplies item and audio",
    "Data/SparePartsSupplies": "Mechanical Supplies item and audio",
    "Data/UI": "FOB inventory and tooltip, map and spatial trackers, material trackers, refuel and repair scene",
    "root": "feature root, entity names, global damage, vendor table, input mappings",
}


def files(d):
    base = os.path.join(ROOT, "data", PLUGIN)
    groups = {}
    for path in sorted(glob.glob(os.path.join(base, "**", "*.json"), recursive=True)):
        rel = os.path.relpath(path, base).replace("\\", "/")
        parts = rel.split("/")
        if parts[:2] == ["Data", "Buildables"] and len(parts) > 3:
            key = "Data/Buildables/" + parts[2]
        elif len(parts) > 2:
            key = "/".join(parts[:2])
        else:
            key = "root"
        groups.setdefault(key, []).append((rel, parts[-1][:-5]))
    out = ["| Folder | Files | What is in it | File names |", "|---|---|---|---|"]
    for key in sorted(groups):
        items = groups[key]
        role = ROLES.get(key) or ("buildable, stage definition, radial wheel slot and sounds" if key.startswith("Data/Buildables/") else "")
        out.append(f"| `{key}` | {len(items)} | {role} | " + ", ".join(f"`{nm}`" for _, nm in items) + " |")
    out.append("")
    out.append(f"Total: {sum(len(v) for v in groups.values())} files.")
    return "\n".join(out)


def hammer_speed(d):
    """Hammer swing montage times and build amounts per hit (assets/data/bp-defaults.json, round 17)."""
    out = ["| Hammer | Shop text | Build amount per hit | Critical-spot hit amount | Use montage | Montage (s) | Hit notify (s) | Swing loop (s) | Dismantle per hit |",
           "|---|---|---:|---:|---|---:|---:|---:|---:|"]
    rows = (("Large", "ID_LargeHammer", "AM_FP_Large_Hammer_Use", "Fast Build Speed"),
            ("Medium", "ID_MediumHammer", "AM_FP_BuildTool_Use", "Moderate Build Speed"),
            ("Small", "ID_SmallHammer", "AM_FP_Small_Hammer_Use", "Slow Build Speed"))
    g = lambda a, p: bpd.get("buildables", a, p)  # noqa: E731
    for name, idn, mon, text in rows:
        ba, bc, ln, hit = g(idn, "BuildAmount"), g(idn, "BuildAmountWhenTargetIsHit"), g(mon, "SequenceLength"), g(mon, "Notify:Hit")
        ls, le, dis = g(mon, "Section:LoopStart"), g(mon, "Section:LoopEnd"), g(idn, "DismantleRatePerHit")
        if not (ba and ln):
            continue
        loop = round(le["value"] - ls["value"], 3) if ls and le else None
        out.append("| %s (`%s`) | %s | %s | %s | `%s` | %s | %s | %s | %s |" % (
            name, idn, text, bpd.fmt(ba["value"]), bpd.fmt(bc["value"]) if bc else "-", mon, bpd.fmt(round(ln["value"], 2)),
            bpd.fmt(round(hit["value"], 2)) if hit else "-", bpd.fmt(loop) if loop else "-", bpd.fmt(dis["value"]) if dis else "-"))
    return "\n".join(out)


MODES = {"hammer_speed": hammer_speed, "inventory": inventory, "counts": counts, "placement": placement, "stages": stages, "damage": damage,
         "rewards": rewards, "economy": economy, "special": special, "names": names, "files": files, "stationary": stationary}


def write(d):
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, nothing written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = link_generated(MODES[m.group(1)](d)).split("\n")
        return nl.join([f"<!-- buildable_tables {m.group(1)} -->"] + body + ["<!-- /buildable_tables -->"])
    new, count = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = load()
    args = sys.argv[1:]
    if "--write" in args:
        write(d)
    else:
        print(link_generated(MODES[next((a for a in args if a in MODES), "inventory")](d)))


if __name__ == "__main__":
    main()
