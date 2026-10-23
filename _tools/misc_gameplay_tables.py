"""Tables for content/Wardogs_MiscGameplayAssets_v1.md: three small asset groups no other page names, rebuilt from data/.

Scope (export files whose name does not appear as a whole identifier on any other published page, same rule as
_tools/doc_coverage.py, with this page left out):
  Wardogs/Content/MoverTesting/CharacterModifierStates
  Wardogs/Content/GameMechanics/Settings/Controls   (gamepad dead-zone presets, axis config, controller button/axis presets)
  Wardogs/Content/GameMechanics/WorldInteractable/Objects   (door destruction definitions and swing/breach curves)
Skipped on purpose: audio, VFX and UI-widget assets (none of these folders hold any). Blocks sit between

    <!-- misc_gameplay_tables MODE -->  ...  <!-- /misc_gameplay_tables -->

    python _tools/misc_gameplay_tables.py --write      # refresh every block in place
    python _tools/misc_gameplay_tables.py --check      # exit 1 when a block is stale
    python _tools/misc_gameplay_tables.py MODE         # print one block (counts, states, presets, axis, binds, doors)
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402
import doc_coverage as dc  # noqa: E402
import vehicle_asset_tables as vt  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "content/Wardogs_MiscGameplayAssets_v1.md"
BLOCK = re.compile(r"<!-- misc_gameplay_tables (\w+) -->\r?\n.*?<!-- /misc_gameplay_tables -->", re.S)
C = os.path.join(DATA, "Wardogs", "Content")
STATES = os.path.join(C, "MoverTesting", "CharacterModifierStates")
CTRL = os.path.join(C, "GameMechanics", "Settings", "Controls")
OBJS = os.path.join(C, "GameMechanics", "WorldInteractable", "Objects")
CAP = 1800


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


def files_in(folder, toks):
    return [f for f in sorted(glob.glob(os.path.join(folder, "**", "*.json"), recursive=True)) if os.path.basename(f)[:-5] not in toks]


def flat(props, cap=CAP):
    lv = []
    vt.leaves(props, "", lv)
    out, used = [], 0
    for p, v in lv:
        piece = f"`{p}`={v}"
        if used + len(piece) > cap and out:
            break
        out.append(piece)
        used += len(piece) + 2
    left = len(lv) - len(out)
    return "; ".join(out) + (f" (+{left} more values)" if left else "")


def sub_name(o):
    """Name of the export inside the same file that an object reference points to."""
    on = str(o.get("ObjectName", "")) if isinstance(o, dict) else ""
    m = re.search(r":([^:']+)'$", on)
    return m.group(1) if m else None


def asset_cell(path):
    return ct.link(ct.rel_of(path))


def is_binds(f):
    return "ControllerConfigs" in f.replace("\\", "/")


def load():
    toks = others_tokens()
    return {"states": files_in(STATES, toks), "ctrl": files_in(CTRL, toks), "doors": files_in(OBJS, toks)}


def counts(d):
    ctrl = d["ctrl"]
    presets = [f for f in ctrl if "DeadZonePreset" in f]
    axis = [f for f in ctrl if "InputAxisConfig" in f]
    binds = [f for f in ctrl if is_binds(f)]
    rest = len(ctrl) - len(presets) - len(axis) - len(binds)
    out = ["| Folder | Section | Assets |", "|---|---|---|",
           f"| MoverTesting/CharacterModifierStates | 2. Character modifier states | {len(d['states'])} |",
           f"| Settings/Controls | 3. Dead-zone presets | {len(presets)} |",
           f"| Settings/Controls | 4. Axis config | {len(axis)} |",
           f"| Settings/Controls | 5. Controller binding presets | {len(binds)} |"]
    if rest:
        out.append(f"| Settings/Controls | (not in a section) | {rest} |")
    out += [f"| WorldInteractable/Objects | 6. Doors | {len(d['doors'])} |",
            f"| **Total** | | **{len(d['states']) + len(ctrl) + len(d['doors'])}** |"]
    return "\n".join(out)


def states(d):
    out = ["| Asset | State tag | Priority | Modifiers (exports in the file) | Conditions |", "|---|---|---|---|---|"]
    for f in d["states"]:
        es = ct.exports(f)
        byname = {e["Name"]: e for e in es}
        defn = next((e for e in es if e["Type"] == "WDCharacterModifierStateDefinition"), None)
        if not defn:
            out.append(f"| {asset_cell(f)} | (no state definition) | | | |")
            continue
        p = defn.get("Properties") or {}

        def one(ref):
            e = byname.get(sub_name(ref))
            if not e:
                return f"`{vt.short(ref)}`"
            vals = flat(e.get("Properties") or {}, 700)
            return f"`{e['Type']}`" + (f" {vals}" if vals else " (no values exported)")
        mods = "<br>".join(one(r) for r in p.get("CharacterModifiers", [])) or "-"
        conds = "<br>".join(one(r) for r in p.get("Conditions", [])) or "-"
        other = {k: v for k, v in p.items() if k not in ("StateTag", "CharacterModifiers", "Conditions", "Priority")}
        if other:
            mods += "<br>other: " + flat(other, 300)
        tag = (p.get("StateTag") or {}).get("TagName", "-")
        out.append(f"| {asset_cell(f)} | `{tag}` | {ct.n(p['Priority']) if 'Priority' in p else 'omitted'} | {ct.cell(mods)} | {ct.cell(conds)} |")
    return "\n".join(out)


def presets(d):
    out = ["| Asset | Named values | Preset slots (setting tag = value) |", "|---|---|---|"]
    for f in [x for x in d["ctrl"] if "DeadZonePreset" in x]:
        named, slots = [], []
        for e in ct.exports(f):
            p = e.get("Properties") or {}
            named += [str(nv["Key"]).split("::")[-1] for nv in p.get("NamedValues", [])]
            for i, sp in enumerate(p.get("SettingPresets", [])):
                kv = "; ".join(f"`{x['Key']['TagName'].replace('UserSettings.Controls.Gamepad.DeadZone.', '')}`={ct.n(x['Value'])}" for x in sp.get("SettingPreset", []))
                slots.append(f"slot {i}: {kv}")
        out.append(f"| {asset_cell(f)} | {', '.join(named) or '-'} | {ct.cell('<br>'.join(slots) or '-')} |")
    return "\n".join(out)


def axis(d):
    out = ["| Asset | Scope | Required tag groups | Axis | Gamepad | Modifier type | Setting property |", "|---|---|---|---|---|---|---|"]
    for f in [x for x in d["ctrl"] if "InputAxisConfig" in x]:
        for e in ct.exports(f):
            p = e.get("Properties") or {}
            scopes = [("default", "-", p.get("DefaultAxisConfig") or {})]
            for i, s in enumerate(p.get("StateAxisConfigs", [])):
                tags = " AND ".join("(" + " OR ".join(f"`{t}`" for t in grp) + ")" for grp in s.get("RequiredTags", []))
                scopes.append((f"state {i}", tags or "-", s.get("AxisConfigProperties") or {}))
            for name, tags, cfg in scopes:
                for m in cfg.get("AxisSettingModifiers", []):
                    out.append(f"| {asset_cell(f)} | {name} | {tags} | {str(m.get('Axis')).split('::')[-1]} | {str(m.get('bGamepad')).lower()} | {str(m.get('ModifierType')).split('::')[-1]} | `{m.get('PropertyName')}` |")
                extra = {k: v for k, v in cfg.items() if k != "AxisSettingModifiers"}
                if extra:
                    out.append(f"| {asset_cell(f)} | {name} | {tags} | other properties | | | {ct.cell(flat(extra, 600))} |")
    return "\n".join(out)


def binds(d):
    out = ["| Preset | Action tag | Action asset | Key | Triggers | Modifiers |", "|---|---|---|---|---|---|"]
    ctx = ["| Preset | Mapping contexts (obfuscated property; inference) | Binding rows |", "|---|---|---|"]
    for f in [x for x in d["ctrl"] if is_binds(x)]:
        es = ct.exports(f)
        byname = {e["Name"]: e for e in es}
        main = next(e for e in es if e["Type"] == "BHEnhancedInputPlayerBindsPresetData")
        p = main.get("Properties") or {}
        rows, contexts = [], []
        for v in p.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "Key" in v[0]:
                rows = v
            elif isinstance(v, list):
                contexts += [str(x.get("AssetPathName", x)).split(".")[-1] for x in v]

        def res(refs):
            parts = []
            for r in refs:
                if not r:
                    parts.append("(null)")
                    continue
                e = byname.get(sub_name(r))
                if e:
                    vals = flat(e.get("Properties") or {}, 400)
                    parts.append(e["Type"] + (f" ({vals})" if vals else ""))
                else:
                    parts.append(vt.short(r))
            return "<br>".join(parts) or "-"
        for r in rows:
            a = r.get("Action") or {}
            out.append(f"| {asset_cell(f)} | `{(r.get('ActionTag') or {}).get('TagName', '-')}` | `{vt.short(a) if a else '-'}` | `{(r.get('Key') or {}).get('KeyName', '-')}` | {ct.cell(res(r.get('Triggers', [])))} | {ct.cell(res(r.get('Modifiers', [])))} |")
        ctx.append(f"| {asset_cell(f)} | {', '.join(f'`{c}`' for c in contexts) or ('none (export has no properties)' if not p else '-')} | {len(rows)} |")
    return "\n".join(ctx) + "\n\nBinding rows:\n\n" + "\n".join(out)


def doors(d):
    out = ["| Asset | Engine type | Values |", "|---|---|---|"]
    for f in d["doors"]:
        e = ct.exports(f)[0]
        out.append(f"| {asset_cell(f)} | `{e['Type']}` | {ct.cell(flat(e.get('Properties') or {}))} |")
    return "\n".join(out)


MODES = {"counts": counts, "states": states, "presets": presets, "axis": axis, "binds": binds, "doors": doors}


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        mode = m.group(1)
        body = MODES[mode](d) if mode in MODES else "| (unknown block) |"
        return nl.join([f"<!-- misc_gameplay_tables {mode} -->"] + body.split("\n") + ["<!-- /misc_gameplay_tables -->"])
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
    mode = next((a for a in args if a in MODES), "counts")
    print(MODES[mode](d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
