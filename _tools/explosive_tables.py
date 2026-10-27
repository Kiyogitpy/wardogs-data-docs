"""Explosives reference for game-features/Wardogs_Explosives_v1.md, rebuilt from data/ with the pipeline's own rules.

Every blast-bearing source is one row: each projectile asset with ExplosiveRadius > 0 (caliber assets and the
drone, arrow, 70mm and TV-guided assets that infantry_tables.projectile_assets() also reads) and the six reviewed
thrown/placed actors in assets/data/explosive-actors.json. Nothing is re-derived: the data comes from
infantry_tables.PROJ / sources() and damage_tables (rule rows, section routing, hits_to_destroy). Blocks:

    <!-- explosive_tables MODE -->  ...  <!-- /explosive_tables -->

    python _tools/explosive_tables.py --write   # refresh every block in place (idempotent)
    python _tools/explosive_tables.py MODE      # print one block: main, direct, falloff, infantry, vehicles

Radial amount (Damage Pipeline section 1.1, native 0x6F06540 / 0x6F03720): BaseDamage out to the inner radius E
(EffectiveExplosiveRadius), then linear toward BaseDamage x (1 - ExplosiveDamageFallOff) just inside the outer
radius R (ExplosiveRadius), 0 at or beyond R, floored at MinimumExplosiveDamage. Ring = Inner within E, else Outer.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402
import infantry_tables as it  # noqa: E402
import bp_defaults as bpd  # noqa: E402

ROOT = dt.ROOT
PAGE = "game-features/Wardogs_Explosives_v1.md"
BLOCK = re.compile(r"<!-- explosive_tables (\w+) -->\r?\n.*?<!-- /explosive_tables -->", re.S)
EXPLOSIVE, INNER, OUTER = "Meta.Damage.DamageType.Explosive", it.INNER, it.OUTER
TORSO = it.ZONES.index(dt.HIT + "Torso.Upper")
DISTANCES_M = [0, 2.5, 5, 7.5, 10, 12, 15, 20]
VEHICLES = [("Little Bird", "ROT_03_Default"), ("Humvee", "WHL_05_Humvee_Default"),
            ("T-72 (TNK_04)", "TNK_04"), ("Leopard spawn", "SPW_01")]

# Item names as the shop pages show them (WeaponShop launcher rows, ItemShop section 4).
WEAPON_NAMES = {"CGM4": "MAAWS", "Launcher_04": "9K333 Verba", "MMGL": "MGL-40", "RPG7": "RPG-7"}
ACTOR_ITEMS = {"M67 frag grenade": "M67 frag grenade", "C4": "C4 Charge (`Id.Item.C4Explosive`)",
               "AT mine": "AT mine", "Claymore": "Claymore", "IED": "Improvised Explosive Device (`Id.Item.IED.Trigger`)",
               "Molotov": "Molotov (initial burst only)"}
NO_ITEM = {"Item.Caliber.70mm": "no weapon item lists it (vehicle rocket pods not traced)",
           "Item.Caliber.84mm.TVGuided": "no weapon item lists it (TV-guided missile asset)",
           "Item.Caliber.122mm.Havoc": "no weapon item lists it (Havoc rocket asset)",
           "Item.Caliber.155mm.Expensive.Sandbox": "no weapon item (sandbox copy)",
           "Item.Caliber.155mm.Standard.Sandbox": "no weapon item (sandbox copy)",
           "Item.Caliber.Arrow.Explosive": "Rambo Explosive Arrow (`Id.Item.Arrow.Explosive`), combat bow"}


def fmt(x, nd=1):
    if x is None:
        return "-"
    s = f"{x:.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def m(cm):
    return None if cm is None else cm / 100


def amount(d_cm, v):
    """Radial amount at distance d (cm): (amount, ring name)."""
    base, e, r = v["base"], v["E"], v["R"]
    mn, f = v["min"] or 0.0, v["falloff"]
    if d_cm >= r:
        return 0.0, "none"
    if d_cm <= e:
        return max(base, mn), "Inner"
    end = base * (1 - f)
    return max(base + (end - base) * (d_cm - e) / (r - e), mn), "Outer"


def item_names():
    """ProjectileId -> item/weapon labels, from the same source list the infantry viewer uses."""
    out = {}
    for s in it.sources():
        cal = s["values"].get("caliber") if s["category"] == "explosives" else None
        if not cal or s["group"] == "Back-blast":
            continue
        name = re.sub(r"\s*\([^)]*\)\s*(\+\d+ more)?$", "", s["label"]).replace("  ", " ")
        name = WEAPON_NAMES.get(name, name)
        if s["group"] in ("Vehicle", "Cannon") and not name.startswith("GrenadeLauncher"):
            name += " (vehicle weapon)"
        out.setdefault(cal, [])
        if name not in out[cal]:
            out[cal].append(name)
    return out


def collect():
    items = item_names()
    sources = {s["label"]: s for s in it.sources() if s["group"] == "Thrown and placed"}
    by_cal = {}
    for s in it.sources():
        c = s["values"].get("caliber")
        if c and s["category"] == "explosives" and s["values"].get("radial"):
            by_cal.setdefault(c, s["values"]["radial"]["source_context"])
    rows = []
    for pid, p in sorted(it.PROJ.items(), key=lambda kv: (kv[1]["source_tag"] or "", kv[0])):
        v = p["values"]
        if not v.get("ExplosiveRadius", 0) > 0:
            continue
        raw = next(o for o in dt.exports(os.path.join(ROOT, p["path"])) if o.get("Properties", {}).get("ProjectileStats"))
        dv = raw["Properties"]["ProjectileStats"]["DamageValues"]
        ctx = by_cal.get(pid) or p["context"] + [pid, EXPLOSIVE]
        rows.append({
            "id": pid.replace("Item.Caliber.", ""), "kind": "projectile", "by": ", ".join(items.get(pid, [])) or NO_ITEM.get(pid, "no item mapped"),
            "tag": p["source_tag"], "ctx": ctx, "base": v["BaseDamage"], "E": v.get("EffectiveExplosiveRadius", 0.0),
            "R": v["ExplosiveRadius"], "falloff": v.get("ExplosiveDamageFallOff", 0.0), "min": v.get("MinimumExplosiveDamage"),
            "upward": dv.get("bPreferUpwardsTrace"), "arming": p["arming_delay"] if p["has_arming_delay"] else None,
            "unarmed_delay": None if p["has_arming_delay"] else p["arming_delay"],
            "blunt": v.get("ExplosiveBluntDamage"), "path": p["path"], "swapped": v.get("EffectiveExplosiveRadius", 0) > v["ExplosiveRadius"],
        })
    for label, s in sources.items():
        a = s["values"]["damage_values"]
        rows.append({
            "id": label, "kind": "actor", "by": ACTOR_ITEMS[label], "tag": s["values"]["tag"], "ctx": s["values"]["source_context"],
            "base": a["BaseDamage"], "E": a["EffectiveExplosiveRadius"], "R": a["ExplosiveRadius"],
            "falloff": a["ExplosiveDamageFallOff"], "min": a["MinimumExplosiveDamage"], "upward": a["bPreferUpwardsTrace"],
            "arming": None, "unarmed_delay": None, "blunt": None, "path": s["values"]["reviewed_defaults_src"],
            "swapped": False, "sustained": s["values"].get("sustained_fire"),
        })
    return rows


def ring_factors(r):
    """(Inner factor, Outer factor) at the unarmored Torso.Upper for a source's root tag and appended context."""
    out = []
    for ring in (INNER, OUTER):
        enc, zm, *_ = it.encode_zones(r["tag"], r["ctx"] + [ring], all_armor_locations=True)
        out.append(it.decode(enc, zm, dt.BONE)[TORSO])
    return out


def radial_secs(secs, flags):
    """Sections with the routes a radial event skips removed (the sections' own radial-skip flags)."""
    out = {}
    for k, (hp, hit, pre, post, simul) in secs.items():
        sp, so, ss = flags.get(k, (False, False, False))
        out[k] = (hp, hit, [] if sp else pre, [] if so else post, [] if ss else simul)
    return out


def vehicle_state():
    generic, vrows = dt.vehicle_tables()
    out = []
    by_name = {os.path.basename(p)[3:-5]: p for p in dt.variants()}
    for label, name in VEHICLES:
        modules, _, _ = dt.assemble(by_name[name])
        secs, dtag = dt.sections(modules), dt.damage_tag(modules)
        out.append((label, name, radial_secs(secs, dt.section_radial_flags(modules)),
                    dt.row_entries(dtag, vrows) + generic, secs[dt.MAIN][0]))
    return out


def t_main(rows):
    out = ["| Source | Fired or placed by | Kind | Source tag | Base | Inner radius E (m) | Outer radius R (m) | Fall-off | Minimum | Trace |",
           "|---|---|---|---|---:|---:|---:|---:|---:|---|"]
    for r in rows:
        trace = "upwards-preferred" if r["upward"] else "not upwards-preferred"
        swap = " (E > R, see note)" if r["swapped"] else ""
        out.append(f"| `{r['id']}` | {r['by']} | {r['kind']} | `{r['tag'].replace('Meta.Damage.', '')}` | {fmt(r['base'])} | "
                   f"{fmt(m(r['E']))}{swap} | {fmt(m(r['R']))} | {fmt(r['falloff'], 2)} | {fmt(r['min'])} | {trace} |")
    return "\n".join(out)


def t_direct(rows):
    out = ["| Source | Arming delay (s) | Direct-impact `ExplosiveBluntDamage` | Thrown contact (`ImpactDamage`) | Trigger |",
           "|---|---:|---:|---:|---|"]
    for r in rows:
        if r["kind"] == "projectile":
            arming = fmt(r["arming"], 3) if r["arming"] is not None else "-"
            trig = "projectile impact"
            if r["arming"] is None and r["unarmed_delay"] is not None:
                trig += f" (`ArmingDelay` {r['unarmed_delay']:g} s present but `bHasArmingDelay` false)"
            out.append(f"| `{r['id']}` | {arming} | {fmt(r['blunt'])} | - | {trig} |")
        else:
            contact = "10" if r["id"] in ("M67 frag grenade", "C4", "IED", "Molotov") else "-"
            trig = {"M67 frag grenade": "thrown; 5.0 s grenade class default fuse",
                    "C4": "remote detonator, range 20,000 (`DelayedDetonate` route)",
                    "IED": "remote trigger, 3.0 s delay; inherits C4 detonation",
                    "AT mine": "placed; vehicles above 0.1 km/h", "Claymore": "placed; players in trigger box, LOS check",
                    "Molotov": "thrown; burst then sustained fire (15 player / 2 vehicle per 0.4 s loop)"}[r["id"]]
            out.append(f"| {r['id']} | - | - | {contact} | {trig} |")
    return "\n".join(out)


def t_falloff(rows):
    out = ["| Source | " + " | ".join(f"{d:g} m" for d in DISTANCES_M) + " |", "|---|" + "---:|" * len(DISTANCES_M)]
    for r in rows:
        out.append(f"| `{r['id']}` | " + " | ".join(fmt(amount(d * 100, r)[0]) for d in DISTANCES_M) + " |")
    return "\n".join(out)


def t_infantry(rows):
    out = ["| Source | Torso factor Inner | Torso factor Outer | Torso at 0 m | Mid-radius (R/2, m) | Ring at mid | Amount at mid | Torso at mid |",
           "|---|---:|---:|---:|---:|---|---:|---:|"]
    for r in rows:
        fi, fo = ring_factors(r)
        a0, _ = amount(0, r)
        mid = r["R"] / 2
        am, ring = amount(mid, r)
        f = fi if ring == "Inner" else fo
        out.append(f"| `{r['id']}` | x{fi:.3g} | x{fo:.3g} | {fmt(a0 * fi)} | {fmt(m(mid))} | {ring} | {fmt(am)} | {fmt(am * f)} |")
    return "\n".join(out)


def t_vehicles(rows):
    state = vehicle_state()
    out = ["| Source | Inner amount | " + " | ".join(f"{lab} (`{n}`, {fmt(hp, 0)} HP)" for lab, n, _, _, hp in state) + " |",
           "|---|---:|" + "---|" * len(state)]
    for r in rows:
        cells = []
        for _, _, secs, entries, _ in state:
            f = dt.source_rule_factor(entries, [r["tag"]] + r["ctx"] + ["Meta.Damage.Explosive.Radius.Inner"],
                                      secs[dt.MAIN][1])
            hits = dt.hits_to_destroy(secs, dt.MAIN, amount(0, r)[0] * f)
            cells.append(f"{'-' if hits is None else hits} (x{f:.3g})")
        out.append(f"| `{r['id']}` | {fmt(amount(0, r)[0])} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def t_fuses(rows):
    """Fuse, timer and arming values per thrown or placed item, from assets/data/bp-defaults.json (round 17)."""
    def g(asset, prop):
        return bpd.get("explosives", asset, prop)

    def val(e):
        return None if e is None or e["value"] is None else e["value"]

    def src(e):
        if e is None:
            return "not exported"
        how = {"export": "**Data (Blueprint CDO)**", "parent": "**Data (Blueprint CDO)**, inherited", "bp-default": "**Data (Blueprint CDO)**, type default",
               "native": "**Native**", "native-pending": "**Native**, see round 17 native defaults"}[e["resolved_from"]]
        if e["resolved_from"] == "native" and e.get("native_ctor_rva"):
            how += f" (ctor `{e['native_ctor_rva'].replace('0x', '0x').upper().replace('0X', '0x')}`)"
        if e["resolved_from"] in ("export", "parent"):
            how += f" `{e['from_asset']}`"
        return how
    out = ["| Item | Timer | Seconds | Source | Notes |", "|---|---|---|---|---|"]

    def row(item, asset, prop, label, note):
        e = g(asset, prop)
        v = val(e)
        txt = "-" if v is None else bpd.fmt(v)
        out.append(f"| {item} | {label} | {txt} | {src(e)} | {note} |")
    row("M67 frag grenade (`Id.Item.M67Grenade`)", "B_FragGrenade", "BaseFuseTime", "`BaseFuseTime` (fuse after the throw)",
        "cookable (`bCanBeCooked` true) and throw-back allowed (`bCanThrowBack` true); the gold variant `B_GoldFragGrenade` inherits")
    row("Smoke grenades, all 8 colours", "B_SmokeGrenade_Red", "BaseFuseTime", "`BaseFuseTime`",
        "every colour sets 3.0 (the native base is 5.0); the smoke then lasts `PostExplodeLifespan` 10 s on the grenade actor, the smoke itself 180 s by default (see Fire page)")
    row("Molotov (`Id.Item.Molotov`)", "B_Molotov", "BaseFuseTime", "`BaseFuseTime`",
        "`B_Molotov` does not set it, so the grenade base class value stands; `bCanBeCooked` is also native (`+0x624` false, store `0x6CADCBB`, round 18; "
        "the Molotov constructor `0x86A0200` runs the grenade base `0x6CADED0`, same zero at `0x6CADEEE`), so it cannot be cooked; "
        "whether the Molotov bursts on impact or on the fuse is not traced")
    row("C4 charge (`Id.Item.C4Explosive`)", "B_ThrowableC4", "TimerBeforeExplosion", "`TimerBeforeExplosion` on the charge",
        "set on the actor; `B_ThrowableIED` inherits it")
    row("C4 detonator (`Id.Item.C4Trigger`)", "ID_C4_Trigger", "DelayTillExplosion", "`DelayTillExplosion` after the trigger press",
        "the item and its Blueprint leave it unset, so it is the Blueprint variable's default 0 (immediate)")
    row("IED detonator (`Id.Item.IED.Trigger`)", "ID_IED_Trigger", "DelayTillExplosion", "`DelayTillExplosion` after the trigger press",
        "set on the item instance")
    row("AT mine (`ID.Item.ATMine`)", "ID_AT_Mine", "ArmingDelay", "`ArmingDelay` after placement",
        "from `BH_AT_MineExtensionData`; the item sets only the trigger box and `UniversalVehicleSpeed`")
    row("Claymore (`Id.Item.Claymore`)", "ID_Claymore", "ActivationDelayTimer", "`ActivationDelayTimer` after placement",
        "from `BH_ClaymoreExtensionData`; the item sets only the trigger box")
    return "\n".join(out)


MODES = {"main": t_main, "direct": t_direct, "falloff": t_falloff, "infantry": t_infantry, "vehicles": t_vehicles,
         "fuses": t_fuses,
         "counts": lambda rows: f"{len(rows)} explosive sources: {sum(r['kind'] == 'projectile' for r in rows)} projectile assets, "
                                f"{sum(r['kind'] == 'actor' for r in rows)} thrown/placed actors"}


def write(rows):
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, nothing written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(mt):
        body = MODES[mt.group(1)](rows).split("\n")
        return nl.join([f"<!-- explosive_tables {mt.group(1)} -->"] + body + ["<!-- /explosive_tables -->"])
    new, count = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = collect()
    args = sys.argv[1:]
    if "--write" in args:
        write(rows)
    else:
        print(MODES[next((a for a in args if a in MODES), "counts")](rows))


if __name__ == "__main__":
    main()
