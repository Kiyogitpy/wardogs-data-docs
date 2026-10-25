"""Launch speed, effective range, fire rate source and loaded-round capacity for every infantry weapon item.

Reads data/ only (cooked export). For each weapon item under Plugins/GameFeatures/Weapons that points at a
WDWeaponStatsData asset it writes: fire rate (asset value, or the native struct default 600 where the asset
omits it, FWDWeaponStats ctor RVA 0x699E6C0), InitialBulletSpeed (cm/s, also m/s), EffectiveRange (m; null where
omitted), and the capacity of the chamber and the default magazine. Capacity is the container's
MaxSlotAmountStackSize (Items v2 section 2a). A weapon with no magazine container (the RPG-7, the 9K333 chamber
is the only store) holds what its chamber container holds.

    python -I _tools/weapon_capacity_tables.py          # print the table
    python -I _tools/weapon_capacity_tables.py --json   # write assets/data/weapon-capacity.json
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = dt.ROOT
OUT = os.path.join(ROOT, "assets", "data", "weapon-capacity.json")
RPM_DEFAULT = 600.0


def containers(path):
    out = []
    for o in dt.exports(path):
        if o.get("Type") == "BHInventoryFragment_SubSlotSupport":
            out += o["Properties"].get("Containers", [])
    return out


def item_id(path):
    for o in dt.exports(path):
        if o.get("Type") == "BHInventoryItemDefinition":
            return dt.tag(o["Properties"].get("ItemId")), o["Properties"]
    return None, {}


def cinfo(c):
    f = c.get("Filter", {})
    return {"container": dt.tag(c["ContainerIdentifier"]), "stack": c.get("MaxSlotAmountStackSize"),
            "allowed_items": [dt.tag(t) for t in f.get("AllowedSubSlotItems", [])],
            "allowed_context": [dt.tag(t) for t in f.get("AllowedSubSlotContext", [])],
            "default": [dt.tag(d["Item"]) for d in c.get("DefaultContainerItems", [])] or
                       [dt.tag(t) for t in c.get("DefaultItems", [])]}


def build():
    base = os.path.join(dt.DATA, "Wardogs")
    by_tag = {}
    rx = re.compile(r'"ItemId": \{\s*"TagName": "([^"]+)"')
    for p in glob.glob(os.path.join(base, "**/ID_*.json"), recursive=True):
        m = rx.search(open(p, encoding="utf-8").read())
        if m:
            by_tag.setdefault(m.group(1), p)
    stats = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(dt.DATA, "**/DA_*_Stats.json"), recursive=True)}
    rows = []
    for t, p in sorted(by_tag.items()):
        if "/Plugins/GameFeatures/Weapons/" not in p.replace("\\", "/"):
            continue
        text = open(p, encoding="utf-8").read()
        ref = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", text)
        if not ref or ref.group(1) not in stats:
            continue
        tg, props = item_id(p)
        disp = props.get("DisplayName", {})
        st = [o for o in dt.exports(stats[ref.group(1)]) if o.get("Type") == "WDWeaponStatsData"][0]["Properties"]["WeaponStats"]
        cs = [cinfo(c) for c in containers(p)]
        chamber = next((c for c in cs if c["container"] == "Item.Attachment.Chamber"), None)
        mag_c = next((c for c in cs if c["container"] == "Item.Attachment.Magazine"), None)
        mag = None
        if mag_c:
            mt = mag_c["default"][0] if mag_c["default"] else None
            mp = by_tag.get(mt)
            mcs = [cinfo(c) for c in containers(mp)] if mp else []
            ammo = next((c for c in mcs if c["container"] == "Item.Ammo"), None)
            mag = {"item": mt, "capacity": ammo["stack"] if ammo else None,
                   "allowed_context": ammo["allowed_context"] if ammo else None,
                   "allowed_items": ammo["allowed_items"] if ammo else None}
        rpm = st.get("RoundsPerMinute")
        spd = st.get("InitialBulletSpeed")
        rows.append({"id": tg, "name": disp.get("LocalizedString") or disp.get("SourceString"), "stats_asset": ref.group(1),
                     "rpm": rpm if rpm is not None else RPM_DEFAULT,
                     "rpm_source": "asset" if rpm is not None else "class_default_native",
                     "muzzle_cm_s": spd if spd is not None else 100000.0,
                     "muzzle_m_s": (spd if spd is not None else 100000.0) / 100,
                     "muzzle_source": "asset" if spd is not None else "class_default_native",
                     "typical_speed_cm_s": st.get("TypicalSpeed") if st.get("bOverrideTypicalSpeed") else None,
                     "effective_range_m": st.get("EffectiveRange") if st.get("EffectiveRange") is not None else 100.0,
                     "effective_range_source": "asset" if st.get("EffectiveRange") is not None else "class_default_native",
                     "rounds_held": (mag["capacity"] if mag else (chamber["stack"] if chamber else None)),
                     "rounds_held_from": "default magazine container" if mag else "chamber container (no magazine container)",
                     "calibers": [dt.tag(c) for c in st.get("SupportedCaliber", [])],
                     "chamber": chamber, "magazine": mag})
    return rows


def main():
    rows = build()
    if "--json" in sys.argv:
        doc = {"meta": {"generator": "_tools/weapon_capacity_tables.py", "source": "data/ cooked export (CL516586)",
                        "units": "muzzle speed cm/s (also m/s), effective range metres, rpm rounds per minute",
                        "notes": ["rpm is the asset value, or 600 (native struct default) where the asset omits it",
                                  "muzzle speed and effective range likewise fall back to the struct ctor defaults 100000 cm/s and 100 m (RVA 0x699E6C0) where the asset omits them",
                                  "capacity = MaxSlotAmountStackSize of the container (inferred meaning, Items v2 section 2a)"]},
               "weapons": rows}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(rows)} weapons")
        return
    for r in rows:
        ch, mg = r["chamber"], r["magazine"]
        print(f"{r['id']:28} {r['rpm']:6g} {r['rpm_source'][:5]:5} {str(r['muzzle_m_s']):>8} m/s  range {r['effective_range_m']}  "
              f"chamber {ch and (ch['stack'], ch['allowed_items'] or ch['allowed_context'])}  mag {mg and (mg['item'], mg['capacity'])}")


if __name__ == "__main__":
    main()
