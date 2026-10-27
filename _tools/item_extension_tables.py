"""Item extension fields that no other generator prints (round 91, items V5-02, V5-03, V5-05).

Sources (exported JSON under data/Wardogs/): the `ID_*` item definitions (`WDInventoryFragment_Armor`,
`WDItemExtensionData_Throwable / _RangedWeapon / _RangedBow_C / _Appliable / _Keycard / _Placeable /
_BuildableDismantle / _CriticalHitSpotManager / _MedKit`, `BHInventoryFragment_Droppable`,
`BH_FuelCan_ExtensionData_C`, `BH_VehicleRepairToolExtensionData_C`, `BH_SpottingExtensionData_C`) and the
`DT_GlobalDamage_*Data` rule tables (for the armour piece to damage row link).

    python -I _tools/item_extension_tables.py            # summary counts
    python -I _tools/item_extension_tables.py --write    # refresh <!-- item_ext NAME --> blocks
    python -I _tools/item_extension_tables.py --check    # exit 1 when a block is stale

Blocks live in game-features/Wardogs_ItemShop_v1.md, Wardogs_FireAndUtility_v1.md, Wardogs_Buildables_v1.md,
Wardogs_GameFeatures_Spotting_v2.md and Wardogs_Medical_v1.md.
"""
import collections
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_vendor_tables as wv  # noqa: E402
import item_shop_tables as ist  # noqa: E402

ROOT = wv.ROOT
DATA = os.path.join(ROOT, "data", "Wardogs")
GF = os.path.join(ROOT, "game-features")
P_SHOP = os.path.join(GF, "Wardogs_ItemShop_v1.md")
P_FIRE = os.path.join(GF, "Wardogs_FireAndUtility_v1.md")
P_BUILD = os.path.join(GF, "Wardogs_Buildables_v1.md")
P_SPOT = os.path.join(GF, "Wardogs_GameFeatures_Spotting_v2.md")
P_MED = os.path.join(GF, "Wardogs_Medical_v1.md")
P_DMGP = os.path.join(ROOT, "pipelines", "Wardogs_DamagePipeline_v2.md")
DMG = os.path.join(DATA, "Content", "GameMechanics", "DamageSystem", "DamageDataTables")

cell = wv.cell
num = wv.num


def short(t):
    return t.replace("Meta.Damage.", "")


class Items:
    """Every ID_* export, grouped by extension type, with a display name per item."""

    def __init__(self):
        c = ist.Ctx()
        self.names = {}
        for it in c.items:
            self.names[it["key"]] = c.name(it)
        for key, rows in c.entity.items():
            if key not in self.names or self.names[key] in ("-", ""):
                for _, row, _ in rows:
                    s = c.text(row.get("FriendlyName"))
                    if s:
                        self.names[key] = s
                        break
        self.by_type = collections.defaultdict(list)  # type -> [(file, item id, props)]
        for p in sorted(glob.glob(os.path.join(DATA, "**", "ID_*.json"), recursive=True)):
            ex = wv.exports(p)
            iid = ""
            for o in ex:
                if o.get("Type") == "BHInventoryItemDefinition":
                    iid = ((o.get("Properties") or {}).get("ItemId") or {}).get("TagName", "")
            f = os.path.basename(p)[:-5]
            for o in ex:
                self.by_type[o.get("Type", "")].append((f, iid, o.get("Properties") or {}))

    def name(self, f, iid):
        n = self.names.get(iid.lower())
        if n and n != "-":
            return n
        return f[3:].replace("_", " ")

    def rows(self, typ):
        return self.by_type.get(typ, [])


def table(head, rows):
    out = ["| " + " | ".join(head[0]) + " |", "|" + "|".join(head[1]) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def tags(c):
    return [t["TagName"] if isinstance(t, dict) else t for t in c]


# -- armour piece -> damage rows ------------------------------------------------------------------
def damage_rows_by_tag():
    """Context tag -> list of 'table #index: source, operation amount' for every rule that names it."""
    out = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(DMG, "DT_GlobalDamage_*Data.json"))):
        tname = os.path.basename(p)[len("DT_GlobalDamage_"):-len("Data.json")]
        for o in wv.exports(p):
            if o.get("Type") != "DataTable":
                continue
            for r in o["Rows"].values():
                for i, e in enumerate(r["DamageModificationEntries"]):
                    t = tags(e["TargetRequirements"])
                    s = tags(e["SourceRequirements"])
                    m = e["OutModification"]
                    for tg in t:
                        if re.match(r"Meta\.Damage\.(Armor|Helmet)\.", tg):
                            op = m["Operation"].split("::")[1].replace("Percentage_", "") + (" %" if "Percentage" in m["Operation"] else "")
                            out[tg].append((tname, i, [short(x) for x in s], op, m["Amount"]))
    return out


def blk_armor(it):
    rows_by_tag = damage_rows_by_tag()
    rows = []
    for f, iid, pr in it.rows("WDInventoryFragment_Armor"):
        tg = (pr.get("DamageContextTag") or {}).get("TagName", "")
        cov = ", ".join(short(x).replace("HitLocation.Infantry.", "") for x in pr.get("CoveredHitLocations", [])) or "-"
        dur = (pr.get("ReplicatedData") or {}).get("Durability")
        refs = rows_by_tag.get(tg, [])
        links = "; ".join(f"{t} #{i}: {'+'.join(s) or 'any source'}, {op} {num(a)}" for t, i, s, op, a in refs) or "none"
        rows.append((it.name(f, iid), f"`{iid}`", f"`{tg}`", cov, num(dur), links))
    head = (["Item", "Item id", "Damage context tag", "Covered hit locations", "Durability", "Damage rule rows that name the tag (table #entry: source, operation, amount)"],
            ["---", "---", "---", "---", "---:", "---"])
    return table(head, rows)


def blk_throwable(it):
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_Throwable"):
        drop = pr.get("bDropOnInterrupt")
        cons = (pr.get("ItemToConsume") or {}).get("TagName", "")
        rows.append((it.name(f, iid), f"`{iid}`", "not set" if drop is None else ("yes" if drop else "no"),
                     f"`{cons}`" if cons else "-"))
    head = (["Item", "Item id", "Drops when interrupted (`bDropOnInterrupt`)", "Item consumed on throw (`ItemToConsume`)"],
            ["---", "---", "---", "---"])
    return table(head, rows)


def curve_keys(c):
    keys = (((c or {}).get("EditorCurveData") or {}).get("Keys")) or []
    return ", ".join(f"{num(k['Time'])}: {num(k['Value'])}" for k in keys)


def blk_ranged_misc(it):
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_RangedWeapon"):
        if "bDropAfterUse" in pr or "FireChargeTime" in pr:
            rows.append((it.name(f, iid), f"`{iid}`", "yes" if pr.get("bDropAfterUse") else "no",
                         num(pr.get("FireChargeTime"))))
    head = (["Item", "Item id", "Dropped after use (`bDropAfterUse`)", "Fire charge time (`FireChargeTime`, s)"],
            ["---", "---", "---", "---:"])
    a = table(head, rows)
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_RangedBow_C"):
        fov = pr.get("BowDrawFovShift") or {}
        rows.append((it.name(f, iid), f"`{iid}`", num(pr.get("FullDrawTime")), num(pr.get("TimeToWaitBeforeCompletion")),
                     fov.get("Type", "-").split("::")[-1], curve_keys(fov.get("ActiveFOVDeltaCurve")) or "-"))
    head = (["Item", "Item id", "Full draw time (s)", "Wait before completion (s)", "Draw FOV shift type", "FOV delta curve (time: value)"],
            ["---", "---", "---:", "---:", "---", "---"])
    return a + "\n\n" + table(head, rows)


def blk_appliable(it):
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_Appliable"):
        if not any(k in pr for k in ("ConsumeAnimationTag", "bPlayAnimationBeforeConsume", "ExtraData")):
            continue
        anim = (pr.get("ConsumeAnimationTag") or {}).get("TagName", "-")
        extra = ", ".join(f"`{k}` {num(v)}" for k, v in (pr.get("ExtraData") or {}).items()) or "-"
        pre = pr.get("bPlayAnimationBeforeConsume")
        rows.append((it.name(f, iid), f"`{iid}`", f"`{anim}`", "-" if pre is None else ("yes" if pre else "no"), extra))
    head = (["Item", "Item id", "Consume animation tag", "Animation plays before consume", "Extra data"],
            ["---", "---", "---", "---", "---"])
    return table(head, rows)


def blk_keycard(it):
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_Keycard"):
        al = (pr.get("KeycardAlignment") or {}).get("TagName", "")
        rows.append((it.name(f, iid), f"`{iid}`", f"`{al}`", al.split(".")[-1], num(pr.get("KeycardNumber"))))
    head = (["Item", "Item id", "Alignment tag", "Faction", "Card number"], ["---", "---", "---", "---", "---:"])
    return table(head, rows)


def blk_droppable(it):
    ext = collections.defaultdict(list)
    force = []
    for f, iid, pr in it.rows("BHInventoryFragment_Droppable"):
        if pr.get("bOverrideDroppedBoxExtent"):
            b = pr.get("OverridedBoxExtent") or {}
            ext[(b.get("X"), b.get("Y"), b.get("Z"))].append(it.name(f, iid))
        if "ThrowingForce" in pr:
            force.append((it.name(f, iid), f"`{iid}`", num(pr["ThrowingForce"])))
    rows = [(num(k[0]), num(k[1]), num(k[2]), len(v), ", ".join(sorted(set(v)))) for k, v in sorted(ext.items(), key=lambda kv: -len(kv[1]))]
    head = (["Box X", "Box Y", "Box Z", "Items", "Item names"], ["---:", "---:", "---:", "---:", "---"])
    out = table(head, rows)
    if force:
        out += "\n\n" + table((["Item", "Item id", "Throwing force when dropped (`ThrowingForce`)"], ["---", "---", "---:"]), force)
    return out


# -- V5-03: placeables, reach constants -----------------------------------------------------------
def vec(v):
    return "not serialized" if not v else f"{num(v['X'])}, {num(v['Y'])}, {num(v['Z'])}"


def blk_placeable_all(it):
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_Placeable"):
        vp = (pr.get("PlaceableInitData") or {}).get("VitalityComponentParams") or {}
        life = (pr.get("PlaceableInitData") or {}).get("Lifetime")
        cls = ((pr.get("PlaceableClass") or {}).get("ObjectName") or "").replace("BlueprintGeneratedClass'", "").rstrip("'")
        blocked = ", ".join(c["ObjectName"].replace("Class'", "").rstrip("'") for c in pr.get("BlockedActorClasses", [])) or "none"
        rows.append((it.name(f, iid), f"`{cls}`", num(vp.get("BaseHealthOverride")), num(vp.get("MaxHealthOverride")),
                     "-" if life is None else num(life), num(pr.get("MaxPlacementDistance")), num(pr.get("MaxPlacementAngle")),
                     vec(pr.get("PlacementCollisionSize")),
                     "-" if "bCanPlaceOnOtherPlaceable" not in pr else ("yes" if pr["bCanPlaceOnOtherPlaceable"] else "no"), blocked))
    head = (["Item", "Placed actor", "Start health", "Max health", "Lifetime (s)", "Max distance", "Max angle", "Collision size", "Can sit on another placeable", "Blocked by"],
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---", "---", "---"])
    return table(head, rows)


def blk_reach(it):
    rows = []
    for f, iid, pr in it.rows("BH_FuelCan_ExtensionData_C"):
        rows.append((it.name(f, iid), f"`{iid}`", "Fuel can trace distance (`Trace Distance`)", num(pr.get("Trace Distance")), "cm"))
    for f, iid, pr in it.rows("BH_VehicleRepairToolExtensionData_C"):
        rows.append((it.name(f, iid), f"`{iid}`", "Charges spent per use (`ChargesToUse`)", num(pr["ChargesToUse"]) if "ChargesToUse" in pr else "not set", "charges"))
    head = (["Item", "Item id", "Field", "Value", "Unit"], ["---", "---", "---", "---:", "---"])
    return table(head, rows)


def blk_optics(it):
    rows = []
    for f, iid, pr in it.rows("BH_SpottingExtensionData_C"):
        rows.append((it.name(f, iid), f"`{iid}`", "Tracking bounds diameter (`TrackingBoundsDiameter`)", num(pr.get("TrackingBoundsDiameter")), "cm"))
        rows.append((it.name(f, iid), f"`{iid}`", "Show distance / show hit data", f"{pr.get('bShowDistance', 'not set')} / {pr.get('bShowHitData', 'not set')}", ""))
    head = (["Item", "Item id", "Field", "Value", "Unit"], ["---", "---", "---", "---:", "---"])
    return table(head, rows)


def blk_hammer(it):
    crit = {(f, iid): pr for f, iid, pr in it.rows("WDItemExtensionData_CriticalHitSpotManager")}
    rows = []
    for f, iid, pr in it.rows("WDItemExtensionData_BuildableDismantle"):
        cr = crit.get((f, iid), {})
        mod = {k.split("::")[-1]: v for k, v in (pr.get("DismantleModifiers") or {}).items()} if isinstance(pr.get("DismantleModifiers"), dict) else {m["Key"].split("::")[-1]: m["Value"] for m in pr.get("DismantleModifiers", [])}
        rows.append((it.name(f, iid), num(pr.get("DismantleRatePerSecond")), num(pr.get("DismantleRatePerHit")),
                     num(pr.get("DismantleTraceDistance")) if "DismantleTraceDistance" in pr else "not set",
                     ", ".join(f"{k} x{num(v)}" for k, v in mod.items()),
                     num(cr.get("BuildAmountWhenTargetIsHit")), num(cr.get("CriticalHitSpotMaxDistanceAwayFromPlayerView")),
                     num(cr.get("CriticalHitSpotMaxDegreesFacingAwayFromCameraAtSpawn"))))
    head = (["Hammer", "Dismantle rate per second", "Dismantle rate per hit", "Dismantle trace distance (cm)", "Dismantle multiplier by team attitude",
             "Build amount on a critical-spot hit", "Spot max distance from view (cm)", "Spot max facing-away angle (degrees)"],
            ["---", "---:", "---:", "---:", "---", "---:", "---:", "---:"])
    return table(head, rows)


# -- V5-05: Medical Bag steps ---------------------------------------------------------------------
def medbag_data(it):
    for f, iid, pr in it.rows("WDItemExtensionData_MedKit"):
        dur = next((p.get("ReplicatedData", {}).get("Durability") for ff, ii, p in it.rows("WDInventoryFragment_Durability") if ff == f), None)
        return pr, dur
    return None, None


def blk_medbag(it):
    pr, dur = medbag_data(it)
    amt, secs, cost = pr["HealOtherAmount"], pr["HealOtherDuration"], pr["HealOtherDurabilityCost"]
    rows = []
    for miss in (15, 30, 45, 60, 100):
        n = math.ceil(miss / amt)
        rows.append((miss, n, num(n * secs), num(n * cost), f"{n * cost / dur * 100:.1f} %"))
    head = (["Health the teammate is missing", "Application steps (ceil(missing / " + num(amt) + "))", "Seconds to heal (steps x " + num(secs) + ")",
             "Durability spent (steps x " + num(cost) + ")", f"Share of the bag's {num(dur)} durability"], ["---:", "---:", "---:", "---:", "---:"])
    full = int(dur // cost)
    extra = (f"\n\nA full bag ({num(dur)} durability) pays for {full} steps, so at most {num(full * amt)} health at {num(full * secs)} s of continuous healing "
             f"(Derived; what the engine does when durability runs out mid-use was not traced).")
    return table(head, rows) + extra


# -- V5-04: Molotov fire against the documented selection ------------------------------------------
FIRE_SOURCE = "Meta.Damage.DamageType.Enviroment"


def parents(t):
    parts = t.split(".")
    return {".".join(parts[:i]) for i in range(1, len(parts) + 1)}


def blk_molotov(it):
    sp = parents(FIRE_SOURCE)
    rows = []
    vehicle_sum = [0, 0, 0, 0, 0, 0, 0]
    for p in sorted(glob.glob(os.path.join(DMG, "DT_GlobalDamage_*Data.json")) + glob.glob(os.path.join(DATA, "Plugins", "**", "DT_GlobalDamage_*.json"), recursive=True)):
        tname = os.path.basename(p)[len("DT_GlobalDamage_"):-5]
        total = skipped = nosrc = match = aligned = aligned_match = 0
        for o in wv.exports(p):
            if o.get("Type") != "DataTable":
                continue
            for r in o["Rows"].values():
                for e in r["DamageModificationEntries"]:
                    total += 1
                    i_, t_, s_ = tags(e["InstigatorRequirements"]), tags(e["TargetRequirements"]), tags(e["SourceRequirements"])
                    if not (i_ or t_ or s_ or e["PossibleHitLocations"]) and e["OutModification"]["Amount"] == 0:
                        skipped += 1
                        continue
                    al = e["AlignmentRequired"].split("::")[1]
                    if al != "None":
                        aligned += 1
                    if not s_:
                        nosrc += 1
                    if set(s_) <= sp:
                        match += 1
                        if al != "None":
                            aligned_match += 1
        if re.match(r"VehicleData_", tname):
            grp = vehicle_sum
            grp[0] += 1
            for k, v in enumerate((total, skipped, nosrc, aligned, match, aligned_match)):
                grp[k + 1] += v
            continue
        rows.append((f"`{tname}`", total, skipped, nosrc, aligned, match, aligned_match))
    if vehicle_sum[0]:
        rows.append((f"{vehicle_sum[0]} per-vehicle tables (`VehicleData_*`)",) + tuple(vehicle_sum[1:]))
    head = (["Rule table (`DT_GlobalDamage_*`)", "Entries", "Dropped by the empty-entry test", "Kept entries with no source requirement",
             "Entries with a Friendly, Hostile or Neutral requirement", "Entries whose source requirements the fire's source tag meets", "Of those, with an alignment requirement"],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:"])
    return table(head, rows)


# -- block writing ----------------------------------------------------------------------------------
BLOCKS = collections.OrderedDict([
    ("armor", (P_SHOP, blk_armor)),
    ("throwable", (P_SHOP, blk_throwable)),
    ("ranged_misc", (P_SHOP, blk_ranged_misc)),
    ("appliable", (P_SHOP, blk_appliable)),
    ("keycard", (P_SHOP, blk_keycard)),
    ("droppable", (P_SHOP, blk_droppable)),
    ("placeable_all", (P_FIRE, blk_placeable_all)),
    ("reach", (P_FIRE, blk_reach)),
    ("optics", (P_SPOT, blk_optics)),
    ("hammer", (P_BUILD, blk_hammer)),
    ("medbag", (P_MED, blk_medbag)),
    ("molotov", (P_DMGP, blk_molotov)),
])


def render():
    it = Items()
    return {k: fn(it) for k, (_, fn) in BLOCKS.items()}


def apply(text, name, body):
    end = "<!-- /item_ext %s -->" % name
    nl = chr(10)
    pat = re.compile("(<!-- item_ext %s -->%s)(.*?)(%s)" % (re.escape(name), nl, re.escape(end)), re.S)
    if not pat.search(text):
        raise SystemExit(f"marker item_ext {name} missing")
    return pat.sub(lambda m: m.group(1) + body + nl + m.group(3), text, count=1)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = render()
    if "--write" not in sys.argv and "--check" not in sys.argv:
        for k, v in out.items():
            print(f"{k}: {v.count(chr(10)) + 1} lines")
        return
    stale = []
    pages = collections.OrderedDict()
    for k, (page, _) in BLOCKS.items():
        if page not in pages:
            with open(page, encoding="utf-8", newline="") as f:
                pages[page] = f.read().replace(chr(13) + chr(10), chr(10))
        new = apply(pages[page], k, out[k])
        if new != pages[page]:
            stale.append(k)
            pages[page] = new
    if "--check" in sys.argv:
        if stale:
            print("stale blocks:", ", ".join(stale))
            sys.exit(1)
        print("item_extension_tables: up to date")
        return
    for page, text in pages.items():
        with open(page, "w", encoding="utf-8", newline="") as f:
            f.write(text.replace(chr(10), chr(13) + chr(10)))
    print("written; changed blocks:", ", ".join(stale) or "none")


if __name__ == "__main__":
    main()
