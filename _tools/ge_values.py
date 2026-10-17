"""Write the Gameplay Effect Values page from assets/data/ge-values.json.

The JSON is a static export of the cooked GE_* Blueprint class default objects
(see the page intro). Rerun after replacing the JSON:

    python _tools/ge_values.py
"""
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "data", "ge-values.json")
PAGE = os.path.join(ROOT, "Wardogs_GameplayEffect_Values_v1.md")
OPS = {"Add": "+", "Multiply": "×", "Divide": "÷", "MultiplyCompound": "×c", "AddFinal": "+f", "Override": "="}
PREFIXES = ["GE_MAGZ_", "GE_FGRP_", "GE_MUZL_", "GE_SGHT_", "GE_Player_", "GE_Weapon_", "GE_MAG_", "GE_FGP_",
            "GE_MZL_", "GE_AK74_", "GE_4xElcanSpectr_", "GE_Item_", "GE_GrantSkill_", "GE_Spotting_", "GE_Vehicle_"]


def short(tag):
    return tag.replace("Attribute.Gameplay.", "") if tag else "?"


def num(x):
    return f"{x:g}"


def modifier(m):
    op = OPS.get(m["op"], m["op"])
    if m["kind"] == "Scalar":
        value = num(m.get("value", 0))
        if m.get("curve"):
            value += f" × `{os.path.basename(m['curve']['table'])}[{m['curve']['row']}]`"
        if m.get("curve_indexing", "Fixed") != "Fixed":
            value += f" @{m['curve_indexing']}"
    elif m["kind"] == "SetByCaller":
        value = f"SetByCaller({short(m.get('set_by_caller_tag'))})"
        if m.get("allow_fallback"):
            value += f", fallback {num(m.get('fallback_value', 0))}"
    else:  # Attribute-backed
        value = f"{short(m.get('backing_attribute'))} ({m.get('attribute_mode', '')})"
        if m.get("curve"):
            value += f" via `{os.path.basename(m['curve']['table'])}[{m['curve']['row']}]`"
    return f"{short(m['attribute'])} {op} {value}"


def requirements(r):
    parts = []
    for key, label in (("application_requirements", "apply"), ("ongoing_requirements", "ongoing"),
                       ("removal_requirements", "remove")):
        req = r.get(key) or {}
        for k, v in req.items():
            if v:
                parts.append(f"{label} {k}: " + ", ".join(f"`{t}`" for t in (v if isinstance(v, list) else [v])))
    return "<br>".join(parts)


def main():
    with open(SRC, encoding="utf-8") as f:
        effects = json.load(f)["effects"]
    groups = collections.OrderedDict((p, []) for p in PREFIXES + ["Other"])
    for r in sorted(effects, key=lambda r: r["name"]):
        groups[next((p for p in PREFIXES if r["name"].startswith(p)), "Other")].append(r)
    mods = collections.Counter(m["kind"] for r in effects for m in r["modifiers"])
    out = [
        "---", 'title: "Gameplay Effect Values"', 'parent: "Pipelines"', "nav_order: 3.5", "---", "",
        "# Wardogs — Gameplay Effect Values", "",
        "> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs)"
        " · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)", "",
        f"What every `GE_*` gameplay effect does: {len(effects)} effects, {sum(mods.values())} modifiers "
        f"({mods['Scalar']} fixed values, {mods['SetByCaller']} set by the caller, {mods['Attribute']} backed by "
        "another attribute). How effects and attributes work is in the "
        "[Gameplay Effects Pipeline](Wardogs_GameplayEffectsPipeline_v1.md).", "",
        "**Source.** A static export of each effect's cooked class default object from the game's paks "
        "([`tools/cue4parse_extractor`](tools/cue4parse_extractor/README.md): CUE4Parse with the 5.7.4 usmap; three usmap "
        "array types were corrected so the modifiers and tag queries decode). The data is in [`assets/data/ge-values.json`](assets/data/ge-values.json); this page "
        "is generated from it by [`_tools/ge_values.py`](_tools/ge_values.py).", "",
        "**Reading the tables.** Attribute names drop `Attribute.Gameplay.`. Operations: `+` Add, `×` Multiply, "
        "`÷` Divide, `×c` MultiplyCompound, `+f` AddFinal, `=` Override. `@StackCount` and the like name the "
        "curve indexing ([pipeline §4.2](Wardogs_GameplayEffectsPipeline_v1.md#42-modifiers)). Cooked objects only "
        "store values that differ from the native default, so a blank duration or stack count means the native "
        "default, which is not in the paks. How the operations combine into an attribute's current value is not "
        "traced yet (pipeline E-1), so the tables give each modifier, not a combined result.", "",
        "Three effects ship in the paks but not in the SDK headers: `GE_GrantSkill_Lockpicking`, "
        "`GE_Meta_ResourceChange` and `GE_MolotovBurning`.", "",
    ]
    for prefix, rows in groups.items():
        if not rows:
            continue
        out += [f"## {prefix.rstrip('_') if prefix != 'Other' else 'Other effects'} ({len(rows)})", "",
                "| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |", "|---|---|---:|---:|---|---|"]
        for r in rows:
            m = "<br>".join(modifier(x) for x in r["modifiers"]) or "—"
            tags = "<br>".join(f"`{t}`" for t in (r.get("granted_tags") or []))
            dur = num(r["duration"]) if r.get("duration") is not None else ""
            stk = num(r["max_stacks"]) if r.get("max_stacks") is not None else ""
            out.append(f"| `{r['name']}` | {m} | {dur} | {stk} | {tags} | {requirements(r)} |")
        out.append("")
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print(f"wrote {os.path.relpath(PAGE, ROOT)}: {len(effects)} effects")


if __name__ == "__main__":
    main()
