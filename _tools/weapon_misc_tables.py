"""Tables for game-features/Wardogs_WeaponMisc_v1.md: leftover weapon-platform, launcher, keycard, combat-bow and music-tape assets, rebuilt from data/.

Scope: export files under Plugins/GameFeatures/Weapons/Platforms, Weapons/Launchers, Items/Keycard, Items/CombatBow and
Items/MusicTapes whose file name (without .json) does not appear as a whole identifier on any other published page (same
rule as _tools/doc_coverage.py, with this page left out). Rows by kind: BHAnimationSet entries and condition overrides,
GameFeatureData stubs, the combat-bow input mapping context and release curve, music-tape track names. WDAudioData
files (ID_*_Audio and the sound keys of music tapes other than the track name) are listed as skipped with their sound-key
count and are not tabulated. Blocks sit between

    <!-- weapon_misc_tables MODE -->  ...  <!-- /weapon_misc_tables -->

    python _tools/weapon_misc_tables.py --write      # refresh every block in place
    python _tools/weapon_misc_tables.py --check      # exit 1 when a block is stale
    python _tools/weapon_misc_tables.py MODE         # print one block (counts, anim, over, stubs, bow, tapes, skipped)
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402
import doc_coverage as dc  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "game-features/Wardogs_WeaponMisc_v1.md"
BLOCK = re.compile(r"<!-- weapon_misc_tables (\w+) -->\r?\n.*?<!-- /weapon_misc_tables -->", re.S)
GF = os.path.join(DATA, "Wardogs", "Plugins", "GameFeatures")
AREAS = ["Weapons/Platforms", "Weapons/Launchers", "Items/Keycard", "Items/CombatBow", "Items/MusicTapes"]


def short(o):
    if not isinstance(o, dict):
        return "-"
    on = str(o.get("ObjectName", ""))
    return on.split("'")[-2] if "'" in on else str(o.get("ObjectPath", "")).rsplit("/", 1)[-1].split(".")[0]


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


def area_of(rel):
    s = rel.split("Plugins/GameFeatures/")[1].split("/")
    return "/".join(s[:2])


def load():
    toks = others_tokens()
    out = []
    for a in AREAS:
        for f in sorted(glob.glob(os.path.join(GF, *a.split("/"), "**", "*.json"), recursive=True)):
            if os.path.basename(f)[:-5] in toks:
                continue
            out.append((ct.rel_of(f), ct.exports(f)))
    return out


def tn(o):
    return (o or {}).get("TagName", "-") if isinstance(o, dict) else "-"


def by_type(d, t):
    return [(r, es) for r, es in d if es[0]["Type"] == t]


def is_skipped(es):
    t = es[0]["Type"]
    return t in ("WDAudioData", "CrosstalkAudioEvent") or t.startswith("AEB_")


def q(s):
    return "`" + s + "`" if s and s != "-" else "-"


def anim_table(d):
    out = ["| Set | Area | Animation tag | Player FP | Player TP | Item FP | Item TP | Length override | Blend out item / player | Overrides |", "|---|---|---|---|---|---|---|---|---|---|"]
    for rel, es in by_type(d, "BHAnimationSet"):
        for e in es:
            for x in e["Properties"].get("Animations", []):
                b = x["Value"].get("BaseAsset") or {}
                lo = ct.n(b.get("OverrideLength", 0)) if b.get("bOverrideLength") else "off"
                out.append(f"| {ct.link(rel, e['Name'])} | `{area_of(rel)}` | `{x['Key']['TagName']}` | {q(short(b.get('FirstPersonPlayerAnimation')))} | "
                           f"{q(short(b.get('ThirdPersonPlayerAnimation')))} | {q(short(b.get('FirstPersonItemAnimation')))} | "
                           f"{q(short(b.get('ThirdPersonItemAnimation')))} | {lo} | "
                           f"{ct.n(b.get('ItemBlendOutTime', 0))} / {ct.n(b.get('PlayerBlendOutTime', 0))} | {len(x['Value'].get('Overrides', []))} |")
    return "\n".join(out)


def over_table(d):
    out = ["| Set | Base tag | Condition schema | From mags | To mags | Invert | Override tag |", "|---|---|---|---|---|---|---|"]
    for rel, es in by_type(d, "BHAnimationSet"):
        for e in es:
            for x in e["Properties"].get("Animations", []):
                for o in x["Value"].get("Overrides", []):
                    sd = (o.get("Condition") or {}).get("SharedDefinition") or {}
                    schema = short(sd.get("SchemaClass")).replace("BHAnimationConditionSchema_", "")
                    structs = (sd.get("Conditions") or {}).get("Structs") or [{}]
                    for s in structs:
                        out.append(f"| {ct.link(rel, e['Name'])} | `{x['Key']['TagName']}` | {schema} | {ct.cell(', '.join(s.get('ApplicableFromMags', [])) or '-')} | "
                                   f"{ct.cell(', '.join(s.get('ApplicableToMags', [])) or '-')} | {str(s.get('bInvert', False)).lower()} | `{tn(o.get('KeyOverride'))}` |")
    return "\n".join(out)


def stub_table(d):
    out = ["| Asset | Engine type | Package | Properties |", "|---|---|---|---|"]
    for rel, es in by_type(d, "GameFeatureData"):
        e = es[0]
        out.append(f"| {ct.link(rel)} | `{e['Type']}` | `{e.get('Package', '')}` | {len(e.get('Properties') or {})} |")
    return "\n".join(out)


def bow_table(d):
    out = ["| Asset | Kind | Values |", "|---|---|---|"]
    for rel, es in d:
        if area_of(rel) != "Items/CombatBow":
            continue
        for e in es:
            p = e.get("Properties") or {}
            if e["Type"] == "InputMappingContext":
                for m in p["DefaultKeyMappings"]["Mappings"]:
                    mods = ", ".join(short(x) for x in m.get("Modifiers", [])) or "none"
                    out.append(f"| {ct.link(rel)} | key mapping | action `{short(m['Action'])}`; key `{m['Key']['KeyName']}`; modifiers {mods}; triggers {len(m.get('Triggers', []))} |")
            elif e["Type"] == "BHPlayerMappableKeySettings":
                out.append(f"| {ct.link(rel)} | mappable key setting `{e['Name']}` | input tag `{tn(p.get('InputTag'))}` |")
            elif e["Type"] == "WDDeadZoneInputModifier":
                out.append(f"| {ct.link(rel)} | dead-zone modifier `{e['Name']}` | type {p.get('Type', '').split('::')[-1]}; min setting `{tn(p.get('MinThresholdSettingTag'))}`; max setting `{tn(p.get('MaxThresholdSettingTag'))}` |")
            elif e["Type"] == "CurveFloat":
                ks = p["FloatCurve"]["Keys"]
                pts = ", ".join(f"{ct.n(k['Time'])}->{ct.n(k['Value'])} ({k['InterpMode'].split('_')[-1]})" for k in ks)
                out.append(f"| {ct.link(rel)} | float curve `{e['Name']}` | {len(ks)} keys: {pts} |")
    return "\n".join(out)


def tape_table(d):
    out = ["| Asset | Track sound asset (`Audio.Asset.Vehicle.Hifi`) | Other sound keys not tabulated |", "|---|---|---|"]
    for rel, es in d:
        if area_of(rel) != "Items/MusicTapes" or es[0]["Type"] != "WDAudioData":
            continue
        sa = es[0]["Properties"]["SoundAssets"]
        hifi = [short(x["Value"]) for x in sa if tn(x["Key"]) == "Audio.Asset.Vehicle.Hifi"]
        out.append(f"| {ct.link(rel)} | {q(hifi[0] if hifi else '-')} | {len(sa) - len(hifi)} |")
    return "\n".join(out)


def skipped_table(d):
    out = ["| Asset | Area | Engine type | Sound keys |", "|---|---|---|---|"]
    for rel, es in d:
        if is_skipped(es) and area_of(rel) != "Items/MusicTapes":
            sa = (es[0].get("Properties") or {}).get("SoundAssets")
            out.append(f"| {ct.link(rel)} | `{area_of(rel)}` | `{es[0]['Type']}` | {len(sa) if sa is not None else '-'} |")
    return "\n".join(out)


def counts(d):
    out = ["| Area | Files | Animation sets | Audio data | Other |", "|---|---|---|---|---|"]
    for a in AREAS:
        fs = [(r, es) for r, es in d if area_of(r) == a]
        an = sum(es[0]["Type"] == "BHAnimationSet" for _, es in fs)
        au = sum(is_skipped(es) for _, es in fs)
        out.append(f"| `{a}` | {len(fs)} | {an} | {au} | {len(fs) - an - au} |")
    out.append(f"| **Total** | **{len(d)}** | | | |")
    return "\n".join(out)


def build(d):
    return {"counts": counts(d), "anim": anim_table(d), "over": over_table(d), "stubs": stub_table(d),
            "bow": bow_table(d), "tapes": tape_table(d), "skipped": skipped_table(d)}


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"
    b = build(d)

    def regen(m):
        mode = m.group(1)
        return nl.join([f"<!-- weapon_misc_tables {mode} -->"] + b[mode].split("\n") + ["<!-- /weapon_misc_tables -->"])
    return BLOCK.subn(regen, text)


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
    mode = next((a for a in args if a in build(d)), "counts")
    print(build(d)[mode])
    return 0


if __name__ == "__main__":
    sys.exit(main())
