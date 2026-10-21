"""Generated tables for user-setting assets and input actions.

Reads the exported JSON under data/ (multi-export files are split on their
`--- export: <Class> / <Name> ---` headers, the same way the other generators do).

Settings: every BHUserSetting* data asset in
    data/Wardogs/Content/GameMechanics/Settings/        (scope "Game")
    data/Wardogs/Plugins/BHFramework/Content/Settings/   (scope "BHFramework")
Display text comes from the DT_Settings_* rows whose TypeData points at the asset.

Inputs: every BHInputAction asset under data/. Default keys come from the
DefaultKeyMappings of every InputMappingContext (IMC_*) export.

    python _tools/settings_tables.py                 # both tables to stdout
    python _tools/settings_tables.py settings        # settings table only
    python _tools/settings_tables.py inputs          # input table only
    python _tools/settings_tables.py --write         # refresh the marker blocks in the docs, in place

Blocks in the doc look like:
    <!-- settings_tables settings --> ... <!-- /settings_tables -->
    <!-- settings_tables inputs -->   ... <!-- /settings_tables -->
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOC = "content/Wardogs_SettingsAndInputs_v1.md"

SETTINGS_DIRS = [
    ("Game", "Wardogs/Content/GameMechanics/Settings"),
    ("BHFramework", "Wardogs/Plugins/BHFramework/Content/Settings"),
]
SETTING_TYPES = {"BHUserSettingNumericData": "Numeric",
                 "BHUserSettingDiscreteData": "Discrete",
                 "BHUserSettingInputFieldData": "Input field"}
DISCRETE_VALUES = {"BHUserSettingEnumDiscreteValues": "enum",
                   "BHUserSettingBoolDiscreteValues": "bool",
                   "BHUserSettingGameplayTagDiscreteValues": "gameplay tag"}

AREA_RULES = [
    ("Vehicles", "Vehicle"),
    ("PlayerController", "Player controller"),
    ("PlayerCharacter", "Infantry"),
    ("Weapons", "Weapon"),
    ("Itemsmith", "Itemsmith"),
    ("BHSpectatorCamera", "Spectator"),
    ("MoverTesting", "Mover test"),
    ("Items", "Items"),
    ("UI", "UI"),
]

EXPORT_HDR = re.compile(r"^--- export: .*?---\s*$", re.M)
REF = re.compile(r"'([^']*)'")


def exports(path):
    """Return the list of export dicts in one data file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for blk in EXPORT_HDR.split(text):
        blk = blk.strip()
        if blk.startswith("{"):
            out.append(json.loads(blk))
    return out


def ref_name(obj):
    """Asset or sub-object name from an ObjectName reference ("Class'Outer:Name'")."""
    if not isinstance(obj, dict):
        return None
    m = REF.search(obj.get("ObjectName", ""))
    if not m:
        return None
    return m.group(1).split(":")[-1]


def ref_type(obj):
    if not isinstance(obj, dict):
        return None
    return obj.get("ObjectName", "").split("'")[0] or None


def label(val):
    """Display label for one option's Value block (SourceString, then LocalizedString)."""
    if not isinstance(val, dict):
        return ""
    for k in ("SourceString", "LocalizedString"):
        if val.get(k):
            return val[k]
    return ""


def option_key(entry):
    k = entry.get("Key")
    if isinstance(k, dict):
        return k.get("TagName", "")
    return str(k)


def fmt_num(v):
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def files_under(rel):
    base = os.path.join(DATA, rel)
    return sorted(glob.glob(os.path.join(base, "**", "*.json"), recursive=True))


def settings_rows():
    rows = []
    display = {}
    for scope, rel in SETTINGS_DIRS:
        for f in files_under(rel):
            if os.path.basename(f).startswith("DT_"):
                for ex in exports(f):
                    if ex.get("Type") != "DataTable":
                        continue
                    for row in (ex.get("Rows") or {}).values():
                        ta = (row.get("TypeData") or {}).get("AssetPathName", "")
                        asset = ta.split(".")[-1] if ta else ""
                        dn = ((row.get("UIData") or {}).get("DisplayName") or {}).get("SourceString")
                        if asset and dn:
                            display[asset] = dn
    for scope, rel in SETTINGS_DIRS:
        base = os.path.join(DATA, rel)
        for f in files_under(rel):
            if os.path.basename(f).startswith("DT_"):
                continue
            exps = exports(f)
            by_name = {e.get("Name"): e for e in exps}
            top = exps[0] if exps else {}
            if top.get("Type") not in SETTING_TYPES:
                continue
            name = top.get("Name")
            folder = os.path.relpath(os.path.dirname(f), base).replace("\\", "/")
            category = folder.split("/")[0] if folder != "." else "(root)"
            p = top.get("Properties", {}) or {}
            params = p.get("Parameters") or {}
            kind = SETTING_TYPES[top["Type"]]
            row = {"name": name, "scope": scope, "category": category, "display": display.get(name, "")}
            if top["Type"] == "BHUserSettingNumericData":
                lo, hi, step = params.get("Minimum"), params.get("Maximum"), params.get("Increment")
                dlo, dhi = params.get("DisplayMinimum"), params.get("DisplayMaximum")
                rng = f"{fmt_num(lo)} to {fmt_num(hi)}" if lo is not None and hi is not None else "not in export"
                if dlo is not None and dhi is not None and (dlo, dhi) != (lo, hi):
                    rng += f" (display {fmt_num(dlo)} to {fmt_num(dhi)})"
                if step is not None:
                    rng += f", step {fmt_num(step)}"
                row.update(kind="Numeric", default=fmt_num(params["Default"]) if "Default" in params else "omitted",
                           range=rng, options="")
                if params.get("bDisplayAsPercentage"):
                    row["kind"] = "Numeric (%)"
            elif top["Type"] == "BHUserSettingDiscreteData":
                ref = params.get("DefaultValues")
                vals = by_name.get(ref_name(ref)) or {}
                vkind = DISCRETE_VALUES.get(vals.get("Type"), "")
                entries = vals.get("Properties", {}).get("NamedValues") or vals.get("Properties", {}).get("Values") or []
                opts = [label(e.get("Value")) or option_key(e) for e in entries]
                if not entries:
                    opts = None
                idx = params.get("DefaultIndex", 0)
                if opts is None:
                    dflt = f"index {idx}" + ("" if "DefaultIndex" in params else " (omitted)")
                elif "DefaultIndex" in params:
                    dflt = f"{opts[idx] if idx < len(opts) else '?'} (index {idx})"
                else:
                    dflt = f"{opts[0] if opts else '?'} (index 0, omitted)"
                dtype = (p.get("DisplayType") or {}).get("TagName", "").split(".")[-1].lower()
                kind = " ".join(x for x in (vkind, dtype) if x)
                row.update(kind=f"Discrete ({kind})" if kind else "Discrete", default=dflt, range="",
                           options=" / ".join(opts) if opts else "not in export")
            else:
                hint = (params.get("Hint") or {}).get("SourceString", "")
                row.update(kind="Input field", default="", range="", options=f"Hint: {hint}" if hint else "")
            rows.append(row)
    return sorted(rows, key=lambda r: (r["scope"] != "Game", r["category"], r["name"]))


def area_of(path):
    rel = os.path.relpath(path, DATA).replace("\\", "/")
    for key, label_ in AREA_RULES:
        if key in rel:
            return label_
    return "/".join(rel.split("/")[-3:-1])


def input_rows():
    actions = {}
    for f in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            head = fh.read()
        if '"BHInputAction"' not in head:
            continue
        for ex in exports(f):
            if ex.get("Type") != "BHInputAction":
                continue
            p = ex.get("Properties", {}) or {}
            name = ex.get("Name")
            if name in actions:
                continue
            vt = (p.get("ValueType") or "").split("::")[-1]
            actions[name] = {
                "name": name,
                "area": area_of(f),
                "folder": os.path.relpath(os.path.dirname(f), DATA).replace("\\", "/"),
                "value": {"Axis1D": "Axis 1D", "Axis2D": "Axis 2D", "Axis3D": "Axis 3D"}.get(vt, "Bool (omitted)" if not vt else vt),
                "tag": (p.get("InputTag") or {}).get("TagName", ""),
                "triggers": ", ".join(ref_type(t) or "?" for t in p.get("Triggers") or []),
                "modifiers": ", ".join(ref_type(m) or "?" for m in p.get("Modifiers") or []),
                "display": ((p.get("ActionDescription") or {}).get("SourceString") or ""),
                "keys": [],
            }
    for f in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            head = fh.read()
        if "DefaultKeyMappings" not in head:
            continue
        for ex in exports(f):
            dkm = (ex.get("Properties") or {}).get("DefaultKeyMappings") or {}
            for m in dkm.get("Mappings") or []:
                act = ref_name(m.get("Action"))
                key = (m.get("Key") or {}).get("KeyName")
                if act in actions and key and key not in actions[act]["keys"]:
                    actions[act]["keys"].append(key)
    return sorted(actions.values(), key=lambda r: (r["area"], r["name"]))


def settings_table():
    rows = settings_rows()
    out = ["| Setting | Scope | Category | Type | Display text | Default | Range / step | Options |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| `{r['name']}` | {r['scope']} | {md(r['category'])} | {r['kind']} | {md(r['display']) or '—'} | "
                   f"{md(r['default']) or '—'} | {md(r['range']) or '—'} | {md(r['options']) or '—'} |")
    return out, len(rows)


def inputs_table():
    rows = input_rows()
    out = ["| Input action | Area | Value | Input tag | Triggers | Modifiers | Display name | Default key(s) |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| `{r['name']}` | {r['area']} | {r['value']} | `{r['tag'] or '—'}` | {md(r['triggers']) or '—'} | "
                   f"{md(r['modifiers']) or '—'} | {md(r['display']) or '—'} | {md(', '.join(r['keys'])) or '—'} |")
    return out, len(rows)


def render(mode):
    if mode == "settings":
        lines, n = settings_table()
    elif mode == "inputs":
        lines, n = inputs_table()
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return lines, n


BLOCK = re.compile(r"<!-- settings_tables (\w+) -->\r?\n.*?<!-- /settings_tables -->", re.S)


def write_doc():
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    cache = {}

    def regen(m):
        mode = m.group(1)
        if mode not in cache:
            cache[mode] = render(mode)
        lines, n = cache[mode]
        print(f"{mode}: {n} rows")
        return nl.join([f"<!-- settings_tables {mode} -->"] + lines + ["<!-- /settings_tables -->"])

    new, n = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
    print(f"{DOC}: {n} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args:
        write_doc()
        return
    modes = args or ["settings", "inputs"]
    for mode in modes:
        lines, n = render(mode)
        print("\n".join(lines))
        print(f"\n{n} rows", file=sys.stderr)


if __name__ == "__main__":
    main()
