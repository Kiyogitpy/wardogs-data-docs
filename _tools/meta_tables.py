"""Tables for game-features/Wardogs_Progression_v1.md, rebuilt from data/.

Reads the skill tables (WDMetaSkillEffectsTaggedTableRow), their level curves (CT_*Skills), the UI skill
node names (DT_CharacterSkillNodes_Data), the live curve tables (WDLiveCurveTableRow) with their CRV assets,
the currency table (WDCurrencyDefinition) and every cosmetic table (WDCosmeticData). Each table sits between

    <!-- meta_tables MODE -->  ...  <!-- /meta_tables -->

Rerun after a data update (idempotent):

    python _tools/meta_tables.py --write      # refresh every block in place
    python _tools/meta_tables.py MODE         # print one block (counts, skills, skillcurves, livecurves,
                                              #   currencies, cosmetics, coverage)

Joins: skill row -> GameplayEffect class (path in the row) -> modifiers in assets/data/ge-values.json;
skill magnitude -> CT_* curve row (named in the row); live curve row -> CRV asset (path in the row);
reward formula variable -> live curve (ScalingValueCurveTag equals the row tag, Data); live curve -> challenge
tree through the reward tag the tree names (Derived, uses challenge_tables).
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT = ct.ROOT
DATA = ct.DATA
PAGE = "game-features/Wardogs_Progression_v1.md"
BLOCK = re.compile(r"<!-- meta_tables (\w+) -->\r?\n.*?<!-- /meta_tables -->", re.S)
link, cell, n, tag, objname, exports, rel_of = ct.link, ct.cell, ct.n, ct.tag, ct.objname, ct.exports, ct.rel_of
ROLE_ORDER = ["Driver", "Infantry", "Medic", "Pilot", "Recon", "Support"]


def tables_by_struct(struct):
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, "**", "DT_*.json"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            head = f.read(1200)
        if f"Class'{struct}'" not in head:
            continue
        for e in exports(path):
            if e.get("Type") == "DataTable" and objname(e["Properties"].get("RowStruct")) == struct:
                out.append((rel_of(path), e["Name"], e["Rows"]))
    return out


def curve_keys(keys):
    return [(k["Time"], k["Value"], k["InterpMode"].replace("RCIM_", "")) for k in keys]


def fmt_keys(keys):
    return ", ".join(f"{n(t)}: {n(v)}" for t, v, _ in curve_keys(keys))


def interp(keys):
    return "/".join(sorted({k[2] for k in curve_keys(keys)}))


def load():
    d = {}
    ge = json.load(open(os.path.join(ROOT, "assets", "data", "ge-values.json"), encoding="utf-8"))
    d["ge"] = {e["name"]: e for e in ge["effects"]}
    d["ui"] = {}
    for rel, name, rows in tables_by_struct("WDMetaTreeNodeData_UI"):
        for k, r in rows.items():
            d["ui"][k] = ((r.get("FriendlyName") or {}).get("CultureInvariantString"),
                          (r.get("Description") or {}).get("CultureInvariantString"))
    d["skilltabs"] = tables_by_struct("WDMetaSkillEffectsTaggedTableRow")
    d["ctcurves"] = {}
    for path in glob.glob(os.path.join(DATA, "Wardogs", "Content", "Meta", "CharacterSkills", "CT_*.json")):
        for e in exports(path):
            d["ctcurves"][e["Name"]] = (rel_of(path), e["Rows"])
    d["livetabs"] = tables_by_struct("WDLiveCurveTableRow")
    d["crv"] = {}
    for path in glob.glob(os.path.join(DATA, "**", "CRV_*.json"), recursive=True):
        for e in exports(path):
            d["crv"][e["Name"]] = (rel_of(path), e)
    d["currtabs"] = tables_by_struct("WDCurrencyDefinition")
    d["costabs"] = tables_by_struct("WDCosmeticData")
    d["ch"] = ct.load()
    d["formulas"] = {}
    for path in sorted(glob.glob(os.path.join(DATA, "**", "DT_ChallengeRewards_*.json"), recursive=True)):
        for e in exports(path):
            if e.get("Type") == "DataTable":
                for key, row in e["Rows"].items():
                    d["formulas"][key] = (rel_of(path), e["Name"], row)
    d["gold"] = {}
    for rel, name, rows in tables_by_struct("WDGoldMarketItemTableRow"):
        for k, r in rows.items():
            d["gold"][k] = (name, r)
    d["slot"] = {}
    for rel, name, rows in tables_by_struct("WDVehicleSlotPartRow"):
        for k, r in rows.items():
            d["slot"][k] = (name, r)
    return d


def skill_rows(d):
    out = []
    for rel, tname, rows in d["skilltabs"]:
        for key, row in rows.items():
            for e in row["SkillEffects"]:
                for se in e["Value"]["SkillEffects"]:
                    eff = objname(se["Effect"])
                    eff = eff[:-2] if eff and eff.endswith("_C") else eff
                    mags = []
                    for m in se["CustomMagnitudes"]:
                        c = m["Value"]["Curve"]
                        mags.append((tag(m["Key"]), m["Value"]["Value"], (objname(c.get("CurveTable")) or "").replace("CurveTable'", "").rstrip("'") or None, c["RowName"]))
                    req = []
                    for a in se["AdditionalData"]:
                        for rk, rv in a.items():
                            if rk in ("ItemApplicationRequirements", "VehicleApplicationRequirements"):
                                parts = []
                                if rv.get("RequireTags"):
                                    parts.append("require " + ", ".join(f"`{t}`" for t in rv["RequireTags"]))
                                if rv.get("IgnoreTags"):
                                    parts.append("ignore " + ", ".join(f"`{t}`" for t in rv["IgnoreTags"]))
                                if rv.get("TagQuery", {}).get("AutoDescription"):
                                    parts.append("query " + rv["TagQuery"]["AutoDescription"].strip())
                                req.append(("Item" if rk[0] == "I" else "Vehicle") + ": " + ("; ".join(parts) or "any"))
                            elif rk == "DefaultAttributes":
                                req.append("Default " + ", ".join(f"`{tag(x['Key'])}` = {n(x['Value'])}" for x in rv))
                    out.append(dict(table=tname, rel=rel, row=key, key=tag(e["Key"]), effect=eff, mags=mags, req=req))
    return out


def role_of(row):
    m = re.match(r"Meta\.Role\.(\w+)\.", row)
    return m.group(1) if m else "?"


def ge_text(d, eff):
    g = d["ge"].get(eff)
    if not g:
        return "not in ge-values.json"
    mods = []
    for m in g["modifiers"]:
        s = f"{m['op']} `{m['attribute']}`"
        if m["kind"] == "SetByCaller":
            s += " by the skill value"
        elif m.get("value") is not None:
            s += f" {n(m['value'])}"
        mods.append(s)
    extra = []
    if g.get("duration"):
        extra.append(f"duration {g['duration']}")
    if g.get("granted_tags"):
        extra.append("grants " + ", ".join(f"`{t}`" for t in g["granted_tags"]))
    return ("; ".join(mods) or "no modifiers") + (" (" + ", ".join(extra) + ")" if extra else "")


def counts(d):
    sk = skill_rows(d)
    nkeys = sum(len(v["Keys"]) for _, rows in d["ctcurves"].values() for v in rows.values())
    live_rows = sum(len(r) for _, _, r in d["livetabs"])
    cos_rows = sum(len(r) for _, _, r in d["costabs"])
    cur_rows = sum(len(r) for _, _, r in d["currtabs"])
    effs = {s["effect"] for s in sk}
    resolved = sum(1 for e in effs if e in d["ge"])
    return "\n".join([
        f"- Skill tables: **{len(d['skilltabs'])}** (`WDMetaSkillEffectsTaggedTableRow`), **{len(sk)}** skill rows, **{len(effs)}** distinct GameplayEffects (**{resolved}** found in `ge-values.json`).",
        f"- Skill level curves: **{len(d['ctcurves'])}** `CT_*Skills` tables, **{sum(len(r) for _, r in d['ctcurves'].values())}** curve rows, **{nkeys}** keys.",
        f"- Live curve tables: **{len(d['livetabs'])}** (`WDLiveCurveTableRow`), **{live_rows}** rows, **{len(d['crv'])}** `CRV_*` curve assets in the export.",
        f"- Currency tables: **{len(d['currtabs'])}**, **{cur_rows}** currencies.",
        f"- Cosmetic tables: **{len(d['costabs'])}** (`WDCosmeticData`), **{cos_rows}** rows.",
    ])


def skills(d):
    sk = skill_rows(d)
    out = []
    for role in ROLE_ORDER:
        rows = [s for s in sk if role_of(s["row"]) == role]
        if not rows:
            continue
        out += [f"### {role} ({len(rows)} skills)", "",
                "| Skill tag | Display name | Table | Applies via | GameplayEffect | What the effect does | Skill value curve | Applies to |",
                "|---|---|---|---|---|---|---|---|"]
        for s in sorted(rows, key=lambda x: x["row"]):
            nm, desc = d["ui"].get(s["row"], (None, None))
            curve = "<br>".join((f"`{m[2]}` / `{m[3]}`: {fmt_keys(d['ctcurves'][m[2]][1][m[3]]['Keys'])}" if m[2] in d["ctcurves"] and m[3] in d["ctcurves"][m[2]][1] else (f"`{m[2]}` / `{m[3]}`" if m[2] else "no curve table")) + (f" (base {n(m[1])})" if m[1] != 1.0 else "") for m in s["mags"]) or "-"
            out.append("| " + " | ".join([
                f"`{s['row']}`", cell(nm or "-") + (f"<br>{cell(desc)}" if desc else ""), link(s["rel"], s["table"]),
                f"`{s['key']}`", f"`{s['effect']}`", cell(ge_text(d, s["effect"])), curve,
                cell("<br>".join(s["req"]) or "-")]) + " |")
        out.append("")
    return "\n".join(out).rstrip()


def skillcurves(d):
    used = {}
    for s in skill_rows(d):
        for m in s["mags"]:
            used.setdefault((m[2], m[3]), []).append(s["row"])
    out = ["| Curve table | Row | Keys (level: value) | Interpolation | Used by skill |", "|---|---|---|---|---|"]
    for tname in sorted(d["ctcurves"]):
        rel, rows = d["ctcurves"][tname]
        for rn, row in rows.items():
            u = used.get((tname, rn), [])
            out.append(f"| {link(rel, tname)} | `{rn}` | {fmt_keys(row['Keys'])} | {interp(row['Keys'])} | "
                       + (", ".join(f"`{x}`" for x in u) if u else "none found") + " |")
    return "\n".join(out)


def formula_users(d):
    """curve tag -> [(formula row tag, variable name)]; Data: ScalingValueCurveTag equals the curve row tag."""
    users = {}
    for rtag, (rel, tname, row) in d["formulas"].items():
        stack = [row]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                if "Key" in o and isinstance(o.get("Value"), dict) and "ScalingValueCurveTag" in o["Value"]:
                    t = tag(o["Value"]["ScalingValueCurveTag"])
                    if t:
                        users.setdefault(t, []).append((rtag, o["Key"]))
                stack.extend(o.values())
            elif isinstance(o, list):
                stack.extend(o)
    return users


def trees_for_reward(d, rtags):
    out = set()
    for nm, (rel, p) in d["ch"]["trees"].items():
        calc, _ = ct.reward_nodes(p)
        if any(c[0] in rtags for c in calc):
            out.add(nm)
    return sorted(out)


def short(items, k):
    items = list(items)
    return f"{len(items)}: " + ", ".join(f"`{x}`" for x in items[:k]) + (f", ... (+{len(items) - k})" if len(items) > k else "")


def livecurves(d):
    users = formula_users(d)
    out = ["| Table | Curve row tag | Curve asset | Keys (input: value) | Interpolation | Reward formula rows using it | State trees naming those reward tags |",
           "|---|---|---|---|---|---|---|"]
    for rel, tname, rows in d["livetabs"]:
        for rtag, row in rows.items():
            asset = (objname(row["CurveAsset"]) or "").replace("CurveFloat'", "").rstrip("'")
            crv = d["crv"].get(asset)
            keys = crv[1]["Properties"]["FloatCurve"]["Keys"] if crv else []
            fr = sorted({x[0] for x in users.get(tag(row["Tag"]) or rtag, [])})
            trees = trees_for_reward(d, set(fr)) if fr else []
            out.append("| " + " | ".join([
                link(rel, tname), f"`{rtag}`", link(crv[0], asset) if crv else f"`{asset}` (not exported)",
                fmt_keys(keys) if keys else "-", interp(keys) if keys else "-",
                short(fr, 6) if fr else "none", short(trees, 4) if trees else "-"]) + " |")
    return "\n".join(out)


def currencies(d):
    out = ["| Table | Currency tag | Display name | Localization key | Initial balance |", "|---|---|---|---|---|"]
    for rel, tname, rows in d["currtabs"]:
        for k, r in rows.items():
            dn = r["DisplayName"]
            out.append(f"| {link(rel, tname)} | `{k}` | {dn.get('SourceString')} | `{dn.get('Key')}` | {n(r['InitialBalance'])} |")
    return "\n".join(out)


def base(p):
    return (p or "").rsplit("/", 1)[-1].split(".")[0]


def cosmetics(d):
    out = ["| Table | Cosmetic tag | Entity (item or vehicle) | Category | Archetype | Name | Skin definition | Icon assets | Slot / vehicle filter | Gold market |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for rel, tname, rows in d["costabs"]:
        if not rows:
            out.append(f"| {link(rel, tname)} | (no rows) | - | - | - | - | - | - | - | - |")
        for k, r in rows.items():
            nm = r.get("NameOverride") or {}
            name = nm.get("CultureInvariantString") or nm.get("SourceString") or (f"key `{nm['Key']}`" if nm.get("Key") else "-")
            icons = [base((r["UITextures"]["FallbackIcon"] or {}).get("AssetPathName"))] + \
                    [base(v.get("AssetPathName")) for kk, v in r.items() if kk.startswith("_") and isinstance(v, dict)]
            icons = [i for i in icons if i]
            t = tag(r["Tag"]) or k
            sp = d["slot"].get(t)
            slot = "-"
            if sp:
                vf = ", ".join(f"`{x}`" for x in sp[1]["VehicleFilter"]) or "none"
                slot = f"{sp[1]['TargetSlot']}; vehicle filter {vf}"
            g = d["gold"].get(t)
            gold = f"{n(g[1]['GoldBarCost'])} Gold Bars" if g else "-"
            out.append("| " + " | ".join([
                link(rel, tname), f"`{t}`", f"`{tag(r['EntityId'])}`", f"`{tag(r['Category'])}`",
                f"`{tag(r['Archetype'])}`" if tag(r["Archetype"]) else "-", cell(name),
                f"`{base(r['SkinDefinition'].get('AssetPathName'))}`" if r["SkinDefinition"].get("AssetPathName") else "-",
                cell(", ".join(f"`{i}`" for i in icons) or "-"), cell(slot), gold]) + " |")
    return "\n".join(out)


def coverage(d):
    out = ["| Row struct | Table | Rows | Section |", "|---|---|---|---|"]

    def add(struct, tabs, where):
        for rel, tname, rows in tabs:
            out.append(f"| `{struct}` | {link(rel, tname)} | {len(rows)} | {where} |")
    add("WDMetaSkillEffectsTaggedTableRow", d["skilltabs"], "2")
    add("WDLiveCurveTableRow", d["livetabs"], "4")
    add("WDCurrencyDefinition", d["currtabs"], "5")
    add("WDCosmeticData", d["costabs"], "6")
    return "\n".join(out)


MODES = {"counts": counts, "skills": skills, "skillcurves": skillcurves, "livecurves": livecurves,
         "currencies": currencies, "cosmetics": cosmetics, "coverage": coverage}


def write(d):
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, nothing written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = MODES[m.group(1)](d).split("\n")
        return nl.join([f"<!-- meta_tables {m.group(1)} -->"] + body + ["<!-- /meta_tables -->"])
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
        print(MODES[next((a for a in args if a in MODES), "counts")](d))


if __name__ == "__main__":
    main()
