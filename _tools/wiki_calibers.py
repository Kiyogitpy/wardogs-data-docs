"""Generate one wiki article per caliber: _wiki/ammunition/<slug>.md (the Ammunition section).

Names, slugs, armor and damage helpers come from _tools/wiki_weapons.py, so every caliber
name matches the weapon articles. Numbers come from assets/data/weapon-damage.json,
weapon-damage-falloff.json and ammo-availability.json, plus the Season 2 changes page.

Run from the repo root:  python _tools/wiki_calibers.py
(run _tools/wiki_weapons.py after this if the caliber links in the weapon pages changed)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wiki_icons  # noqa: E402
import wiki_weapons as W  # noqa: E402

AMMO = W.jload("assets/data/ammo-availability.json")
TIERS = ["None", "Light", "Medium", "Heavy", "SuperHeavy"]
BASE_ORDER = ["FMJ", "HollowPoint", "ArmorPiercing", "Buckshot", "Slug"]
SHORT = {"FMJ": "Standard (FMJ)", "HollowPoint": "Flesh Damage (HP)", "ArmorPiercing": "Armor Piercing (AP)",
         "Buckshot": "Buckshot", "Slug": "Rifled slug"}


def weapon_codes():
    for wid in W.loadouts["weapons"]:
        code = W.code_for(wid)
        if code in W.SKIP or code not in W.wdamage:
            continue
        yield wid, code


def caliber_keys():
    return sorted({W.wdamage[c]["caliber"] for _, c in weapon_codes() if W.wdamage[c]["caliber"]})


def weapons_for(key):
    ws = [(wid, code) for wid, code in weapon_codes() if W.wdamage[code]["caliber"] == key]
    ws.sort(key=lambda p: (W.CLASS_ORDER.index(W.loadouts["items"][p[0]]["archetype"]), W.page_title(p[0])))
    return ws


def ammo_by_id(code):
    return {a["id"]: a for a in W.wdamage[code]["ammo"]}


def tier_name(t):
    return W.ARMOR_NAME[t].lower()


def cross_text(subj, base, sub, bas, pellets_note=""):
    """Plain sentence about where one ammo type beats another across armor classes."""
    signs = [sub[t] >= bas[t] - 1e-9 for t in TIERS]
    if all(signs):
        return f"{subj} does more damage than {base} at every armor class{pellets_note}."
    if not any(signs):
        return f"{subj} does less damage than {base} at every armor class{pellets_note}."
    flips = [i for i in range(1, len(TIERS)) if signs[i] != signs[i - 1]]
    if len(flips) != 1:
        return f"{subj} and {base} trade places more than once across armor classes; see the table above."
    k = flips[0]
    before = "with no armor" if k == 1 else f"up to {tier_name(TIERS[k - 1])} armor"
    after = f"from {tier_name(TIERS[k])} armor up"
    verb = "more" if signs[k] else "less"
    other = "less" if signs[k] else "more"
    return (f"{subj} does {other} damage than {base} {before} and {verb} damage {after}"
            f"{pellets_note}.")


def price_text(key, typ):
    cal = AMMO["calibers"].get(key)
    if not cal:
        return "not yet known"
    for a in cal.get("ammo", []):
        if a.get("type") != typ:
            continue
        v = a.get("vendor") or {}
        if v.get("price") is None:
            return "not yet known"
        txt = f"{W.fmt_int(v['price'])} cash"
        if v.get("amount") and v["amount"] != 1:
            txt += f" (vendor lot of {v['amount']})"
        if v.get("showInVendor") is False:
            txt += ", not shown in the vendor list"
        return txt
    return "not yet known"


def build(key):
    ws = weapons_for(key)
    title = W.caliber_display(key)
    codes = [c for _, c in ws]
    ids = set()
    for c in codes:
        ids |= set(ammo_by_id(c))
    base_ids = [b for b in BASE_ORDER if b in ids]
    has_tracer = any("Tracer" in i for i in ids)
    is_shell = "Buckshot" in ids
    types_txt = ", ".join(SHORT[b] for b in base_ids)
    if has_tracer and all(any(i == b or i == b + ".Tracer" or (b == "FMJ" and i == "Tracer") for i in ids)
                          for b in base_ids):
        types_txt += " (each with a tracer version)"

    classes = []
    for wid, _ in ws:
        cls = W.CLASS_NAME[W.loadouts["items"][wid]["archetype"]]
        if cls not in classes:
            classes.append(cls)
    speeds = []
    for wid, code in ws:
        fo = W.falloff.get(code)
        if fo and fo.get("initial_bullet_speed_cm_s"):
            speeds.append(fo["initial_bullet_speed_cm_s"] / 100)
    if not speeds:
        speed_txt = "not yet known"
    elif min(speeds) == max(speeds):
        speed_txt = f"{min(speeds):.0f} m/s"
    else:
        speed_txt = f"{min(speeds):.0f} to {max(speeds):.0f} m/s"

    n = len(ws)
    noun = "shells" if is_shell else "rounds"
    lead = (f"The {title} caliber is used by {n} weapon{'s' if n != 1 else ''}, "
            f"across the {', '.join(classes[:-1]) + ' and ' + classes[-1] if len(classes) > 1 else classes[0]} "
            f"class{'es' if len(classes) > 1 else ''}. "
            f"Its {noun} are {', '.join(SHORT[b] for b in base_ids)}. "
            "The tables below show how each type does against armor.")

    infobox = [f"| {title} | |", "|---|---|",
               "| **General** | |",
               f"| Bullet types | {types_txt} |",
               f"| Weapons | {n} |",
               f"| Classes | {', '.join(classes)} |",
               "| **Ballistics** | |",
               f"| Muzzle velocity | {speed_txt} |",
               "| **Availability** | |"]
    for b in base_ids:
        infobox.append(f"| {SHORT[b]} price | {price_text(key, b)} |")
    infobox += [f"| Internal name | {key} |", "{: .wiki-infobox }"]

    out = [f"# {title}", ""] + infobox + ["", lead, ""]

    # Weapons that use it
    out += ["## Weapons that use it", "",
            "| Weapon | Class | Fire rate | Upper torso, no armor, point blank |", "|---|---|---:|---:|"]
    for wid, code in ws:
        s = W.stats(wid)
        ad = ammo_by_id(code)
        base = ad.get("FMJ") or ad.get("Buckshot") or next(iter(ad.values()))
        tor = base["damage"]["location"]["Torso.Upper"]
        pell = base.get("pellets")
        dmg_txt = f"{tor:.1f}" + (f" per pellet ({pell} pellets)" if pell else "")
        out.append(f"| [{W.page_title(wid)}]({W.slugify(W.page_title(wid))}.md) | {s['cls']} | "
                   f"{s['rpm']} | {dmg_txt} |")
    out.append("")
    out += ["Point-blank figures use standard rounds (buckshot for shotguns, per pellet), per hit, without falloff. "
            "See [Ammunition](../ammunition.md) for the bullet types.", ""]

    # Ammunition types, for one representative weapon
    rep_wid, rep_code = ws[0]
    rep_name = W.page_title(rep_wid)
    ad = ammo_by_id(rep_code)
    pellets = (ad.get("Buckshot") or {}).get("pellets")
    out += ["## Ammunition types", "",
            f"Upper torso hits from the {rep_name} at point blank range, per hit, without falloff. "
            "Armor changes these numbers a lot, so every armor class is shown.", "",
            "| Ammo | No armor | Light | Medium | Heavy | Super heavy |", "|---|---|---|---|---|---|"]
    tracer_note = []
    rows = []
    for b in BASE_ORDER:
        if b in ad:
            rows.append((b, ad[b]))
    for tid in ["Tracer", "HollowPoint.Tracer", "ArmorPiercing.Tracer"]:
        if tid not in ad:
            continue
        base_id = "FMJ" if tid == "Tracer" else tid.split(".")[0]
        same = ad[tid]["damage"]["torso_armor"] == ad[base_id]["damage"]["torso_armor"]
        if tid == "Tracer" or not same:
            rows.append((tid, ad[tid]))
        if same and tid != "Tracer":
            tracer_note.append(W.AMMO_NAME[tid])
    for aid, a in rows:
        label = W.AMMO_NAME[aid]
        if aid == "Buckshot" and pellets:
            label += " (per pellet)"
        t = a["damage"]["torso_armor"]
        out.append(f"| {label} | " + " | ".join(f"{t[x]:.1f}" for x in TIERS) + " |")
    out.append("")
    notes = []
    if pellets:
        notes.append(f"A buckshot shot has {pellets} pellets, so multiply the per-pellet figure by {pellets} "
                     "for a full hit.")
    if tracer_note:
        notes.append(f"{', '.join(tracer_note)} match their base type in the data.")
    elif any(a == "Tracer" for a, _ in rows) and any("Tracer" in x for x in ad):
        notes.append("Tracer rounds do the same damage as their base type in the data.")
    if notes:
        out += [" ".join(notes), ""]

    # Against armor
    out += ["## Against armor", ""]
    take = []
    if "FMJ" in ad and "ArmorPiercing" in ad:
        take.append(cross_text("Armor Piercing", "standard rounds", ad["ArmorPiercing"]["damage"]["torso_armor"],
                               ad["FMJ"]["damage"]["torso_armor"]))
    if "FMJ" in ad and "HollowPoint" in ad:
        f = ad["FMJ"]["damage"]["torso_armor"]
        h = ad["HollowPoint"]["damage"]["torso_armor"]
        r0 = h["None"] / f["None"]
        r4 = h["SuperHeavy"] / f["SuperHeavy"]
        line = (f"Flesh Damage does {r0:.1f} times the standard damage with no armor and "
                f"{r4:.1f} times against super heavy armor.")
        if h["None"] == max(a["damage"]["torso_armor"]["None"] for a in ad.values()):
            line += " It is the strongest type against unarmored targets."
        if h["SuperHeavy"] == min(a["damage"]["torso_armor"]["SuperHeavy"] for a in ad.values()):
            line += " It is the weakest type against super heavy armor."
        take.append(line)
    if "Buckshot" in ad and "Slug" in ad and pellets:
        bk = ad["Buckshot"]["damage"]["torso_armor"]
        sl = ad["Slug"]["damage"]["torso_armor"]
        full = {t: bk[t] * pellets for t in TIERS}
        take.append(cross_text("A rifled slug", "a full buckshot shot", sl, full,
                               pellets_note=f" if all {pellets} pellets hit"))
    if not take:
        take.append("The data gives no armor comparison between bullet types for this caliber.")
    out += [f"- {t}" for t in take]
    out += ["", "The numbers come from the upper torso column of the table above. Head hits follow the same "
            "pattern at higher values; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).", ""]

    # Season 2 changes
    out += ["## Season 2 changes", ""]
    s2 = []
    pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(key) + r"(?![A-Za-z0-9])")
    hits = [l for l in W.S2.splitlines() if pat.search(l)]
    magazines = [l for l in hits if re.match(r"\| \[?ID_MAGZ", l)]
    if magazines:
        s2.append(f"- The Season 2 changes page adds {len(magazines)} magazine "
                  f"{'item' if len(magazines) == 1 else 'items'} for this caliber's tracer rounds.")
    changed = [(wid, code) for wid, code in ws if W.s2_for(code)]
    if changed:
        names = ", ".join(f"[{W.page_title(wid)}]({W.slugify(W.page_title(wid))}.md)" for wid, _ in changed)
        s2.append(f"- Weapons in this caliber with Season 2 changes: {names}. Each article lists its changes.")
    if not s2:
        s2.append("The Season 2 changes page lists no changes to this caliber or to the weapons that use it.")
    out += s2 + [""]

    # See also and sources
    out += ["## See also", "",
            "- [Ammunition](../ammunition.md), the bullet types and which weapons use each caliber",
            "- [Choosing Ammo](../guides/choosing-ammo.md), which round to load against each armor level",
            "- [Armor](../game-mechanics/armor.md)",
            "- [Ballistics](../game-mechanics/ballistics.md)",
            "- [Weapons](../weapons.md)", "",
            "## Sources", "",
            "- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part and armor numbers",
            "- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)",
            "- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber names",
            f"- [weapon-damage.json]({W.GH}assets/data/weapon-damage.json): ammo types and damage by armor class",
            f"- [weapon-damage-falloff.json]({W.GH}assets/data/weapon-damage-falloff.json): muzzle velocity",
            f"- [ammo-availability.json]({W.GH}assets/data/ammo-availability.json): ammo prices",
            ""]

    desc = (f"The {title} caliber: the weapons that fire it, its bullet types, how they do against armor "
            "and what the ammunition costs.")
    return title, desc, "\n".join(out)


def main():
    out_dir = os.path.join(W.WIKI, "ammunition")
    os.makedirs(out_dir, exist_ok=True)
    keys = caliber_keys()
    for key in keys:
        title, desc, body = build(key)
        slug = W.caliber_slug(key)
        legacy = W.slugify(W.CAL.get(key, key))  # slug the page had under _wiki/weapons/caliber-*
        fm = (f"---\ntitle: \"{title}\"\nparent: \"Ammunition\"\n"
              f"redirect_from: [\"/wiki/weapons/caliber-{legacy}/\"]\ndescription: \"{desc}\"\n---\n\n")
        path = os.path.join(out_dir, slug + ".md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(wiki_icons.inject(fm + W.rebase_links(body, "weapons", "ammunition"), path)[0])  # ammo box icon
    print(f"wrote {len(keys)} caliber articles")


if __name__ == "__main__":
    main()
