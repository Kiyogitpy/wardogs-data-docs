"""Item and player action tables, rebuilt from data/ (BHActionDefinition / WDActionDefinition assets).

Sources, all read from the exported JSON:
  - every `BHActionDefinition` and `WDActionDefinition` export under data/ (155 assets);
  - the item side: `WDItemInputBehavior_*` exports (which item binds which action tag to which input tag) and
    `WDItemExtensionData_Appliable` (use time method, consumption, owner/target states);
  - assets/data/ge-values.json for the GameplayEffects named in `ActionEffects`.

    python _tools/action_tables.py                      # summary (family counts)
    python _tools/action_tables.py --family medical     # definitions + response rules for one family
    python _tools/action_tables.py --appliables         # per-item use data of WDItemExtensionData_Appliable
    python _tools/action_tables.py --effects            # ActionEffects resolved against ge-values.json
    python _tools/action_tables.py --montages           # use, throw and place montage seconds (assets/data/bp-defaults.json)
    python _tools/action_tables.py --fields             # property / flag census
    python _tools/action_tables.py --write              # refresh <!-- action_tables MODE --> blocks

Page: content/Wardogs_ItemActions_v1.md. Markers look like `<!-- action_tables family medical -->`.
"""
import collections
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bp_defaults as bpd  # noqa: E402

DATA = os.path.join(ROOT, "data")
GE_JSON = os.path.join(ROOT, "assets", "data", "ge-values.json")
PAGE = "content/Wardogs_ItemActions_v1.md"
GE_PAGE = "../pipelines/Wardogs_GameplayEffect_Values_v1.md"
DEF_TYPES = ("BHActionDefinition", "WDActionDefinition")
EXPORT = re.compile(r"^--- export:.*---\s*$", re.M)

FAMILIES = collections.OrderedDict([
    ("medical", "Medical and revive"),
    ("throwables", "Throwables, explosives and placeables"),
    ("tools", "Tools and utilities"),
    ("buildables", "Buildables and build tool"),
    ("weapons", "Weapons, melee and bow"),
    ("vehicles", "Vehicle actions"),
    ("movement", "Movement and stance"),
    ("emotes", "Emotes"),
    ("ui", "UI, vendors and pings"),
    ("world", "World interaction and AI"),
])


def load(path):
    """All exports of one file (CUE4Parse writes several `--- export:` blocks)."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    out = []
    for part in EXPORT.split(text):
        part = part.strip()
        if not part:
            continue
        try:
            obj = json.loads(part)
        except ValueError:
            continue
        out += obj if isinstance(obj, list) else [obj]
    return out


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def short(tag, prefix="Action."):
    return tag[len(prefix):] if tag and tag.startswith(prefix) else tag


def obj_name(o):
    """`BlueprintGeneratedClass'B_Action_X_C'` -> `B_Action_X_C` (object name only, never a path)."""
    if not o:
        return ""
    n = o.get("ObjectName", "")
    m = re.search(r"'([^']+)'", n)
    return m.group(1) if m else n


# --- loading ---------------------------------------------------------------------------------------

_cache = {}


def actions():
    """name -> record for every action definition under data/."""
    if "actions" in _cache:
        return _cache["actions"]
    res = {}
    for p in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8", errors="ignore") as f:
            head = f.read()
        if "ActionDefinition\"" not in head:
            continue
        for e in load(p):
            if e.get("Type") in DEF_TYPES:
                pr = e.get("Properties", {})
                res[e["Name"]] = {
                    "name": e["Name"], "type": e["Type"], "file": rel(p), "p": pr,
                    "tag": pr.get("ActionTag", {}).get("TagName", ""),
                }
    _cache["actions"] = res
    return res


def family(a):
    tag, f = a["tag"], a["file"]
    if "/Emote" in tag or tag.startswith("Action.Player.Emote") or "Action.Context.Emote" in a["p"].get("ActionContext", []):
        return "emotes"
    if re.search(r"Buildable|BuildTool|FOBPlacement|BuildBuildable", tag + f):
        return "buildables"
    if re.search(r"FuelCan|VehicleRepairTool|Crowbar|Keycard|Binocular|RangeFinder|ForceOpenDoor|ForceUnlockVehicle", tag + f):
        return "tools"
    if re.search(r"Appliable|MedKit|StimPen|Defibrillator|Resuscitator|Revive|Enox", tag + f):
        return "medical"
    if re.search(r"Throw|C4|IED|Trigger\.Primary|PlaceItem|Placeable", tag + f):
        return "throwables"
    if tag.startswith("Action.Vehicle") or "Actions/Vehicle" in f:
        return "vehicles"
    if "Access" in tag and "/Actions/UI/" in f:
        return "ui"
    if re.search(r"Action\.Weapon|Melee|Action\.Item\.Inspect|Equipment|Player\.Lean|Player\.Focus|Action\.Player\.Equip|DropWeapon", tag + f):
        return "weapons"
    if "/Actions/Weapons/" in f or "/Actions/Melee/" in f:
        return "weapons"
    if "/Movement/" in f:
        return "movement"
    if "/UI/" in f or re.search(r"Access|Ping|QuickSlot|ToggleHands|Radial", tag):
        return "ui"
    return "world"


def ge_index():
    if "ge" not in _cache:
        with open(GE_JSON, encoding="utf-8") as f:
            _cache["ge"] = {e["name"]: e for e in json.load(f)["effects"]}
    return _cache["ge"]


def bindings():
    """action tag -> {'activate': set(items), 'complete': set(items)}, from item input behaviours."""
    if "bind" in _cache:
        return _cache["bind"]
    res = collections.defaultdict(lambda: {"activate": set(), "complete": set(), "inputs": set()})
    for p in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8", errors="ignore") as f:
            if "WDItemInputBehavior" not in f.read():
                continue
        ex = load(p)
        item = os.path.splitext(os.path.basename(p))[0]
        by_name = {}
        for e in ex:
            t = e.get("Type", "")
            if t.startswith("WDItemInputBehavior"):
                pr = e.get("Properties", {})
                tag = (pr.get("ActionToActivate") or pr.get("ActionToComplete") or {}).get("TagName")
                if tag:
                    by_name[e["Name"]] = (t, tag)
        for e in ex:
            if e.get("Type") != "WDItemExtensionData_Input":
                continue
            for b in e.get("Properties", {}).get("InputBehaviors", []):
                m = re.search(r"\.(WDItemInputBehavior\w+)'$", b["Value"].get("ObjectName", ""))
                nm = m.group(1) if m else b["Value"].get("ObjectName", "").split(".")[-1].rstrip("'")
                if nm in by_name:
                    t, tag = by_name[nm]
                    kind = "complete" if t.endswith("CompleteAction") else "activate"
                    res[tag][kind].add(item)
                    if kind == "activate":
                        res[tag]["inputs"].add(short(b["Key"]["TagName"], "Input.NamedActions."))
    _cache["bind"] = res
    return res


# --- formatting ------------------------------------------------------------------------------------

def code(x):
    return f"`{x}`"


def tags(lst, prefix="Action."):
    return ", ".join(code(short(t, prefix)) for t in lst)


def rules(a):
    """One line per non-empty response group."""
    out = []
    for r in a["p"].get("ActionResponseData", []):
        v = r["Value"]
        key = r["Key"].split("::")[1]
        if v.get("ActionResponses"):
            out.append(f"{key}: {tags(v['ActionResponses'])}")
        if v.get("BlockingStates"):
            out.append(f"{key}: {tags(v['BlockingStates'], 'State.Player.')}")
        if v.get("RequiredStates"):
            out.append(f"{key}: {tags(v['RequiredStates'], 'State.Player.')}")
        if v.get("BlockedCategories"):
            out.append(f"{key}: {tags(v['BlockedCategories'], 'Action.Context.')}")
        if v.get("InterruptedCategories"):
            out.append(f"{key}: {tags(v['InterruptedCategories'], 'Action.Context.')}")
        for b in v.get("BufferedResponses", []):
            out.append(f"{key}: {code(short(b['ActionTag']['TagName']))} "
                       f"({b['BufferType'].split('::')[1]}, {b['BufferTime']:g} s)")
        if not any(v.get(k) for k in ("ActionResponses", "BlockingStates", "RequiredStates",
                                      "BlockedCategories", "InterruptedCategories", "BufferedResponses")):
            out.append(f"{key}: (empty)")
    return out


def flags(a):
    p = a["p"]
    f = []
    for k in ("bInstantAction", "bConsumeAxisInputOnCompletion", "bRebufferAction"):
        if p.get(k):
            f.append(k)
    for k in ("_aaabhcpaaifhekodaalnj", "_aaacbmicphngedjgincpn"):
        if p.get(k):
            f.append(f"unnamed `{k}`")
    return ", ".join(f)


def effects_of(a):
    return [(e["Key"], re.sub(r"_C$", "", obj_name(e["Value"]))) for e in a["p"].get("ActionEffects", [])]


def ctx_flags(a):
    return ", ".join(short(t, "Action.Context.") for t in a["p"].get("ActionContext", []))


def bound(a):
    b = bindings().get(a["tag"])
    if not b or not b["activate"]:
        return "—" if not (b and b["complete"]) else "release only"
    items = sorted(b["activate"])
    s = ", ".join(code(i) for i in items[:5])
    return s + (f" +{len(items) - 5}" if len(items) > 5 else "")


def group_rows(rows, sig):
    """Merge rows that are identical apart from their names (the 26 emotes, the stance twins)."""
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault(sig(r), []).append(r)
    return list(groups.values())


def asset_names(rs):
    return ", ".join(code(r["name"]) for r in rs)


def family_table(fam):
    rows = sorted((a for a in actions().values() if family(a) == fam), key=lambda a: (a["tag"], a["name"]))
    out = [f"**{FAMILIES[fam]}: {len(rows)} action definitions**", "",
           "| Action asset | Action tag | Type | Context flags | Action class | Context struct | Flags | Effects | Bound by items |",
           "|---|---|---|---|---|---|---|---|---|"]
    def dsig(a):
        return (a["type"], ctx_flags(a), obj_name(a["p"].get("ActionClass")), obj_name(a["p"].get("ActivationContextType")),
                flags(a), tuple(effects_of(a)))
    for g in group_rows(rows, dsig):
        a = g[0]
        if len(g) > 1:
            tg = ", ".join(code(short(r["tag"])) for r in g)
            nm = f"{len(g)} assets: " + asset_names(g)
            bd = "—"
        else:
            tg, nm, bd = code(short(a["tag"])), code(a["name"]), bound(a)
        eff = ", ".join(code(e[1]) for e in effects_of(a)) or "—"
        out.append(f"| {nm} | {tg} | {a['type'].replace('ActionDefinition', '')} | {ctx_flags(a) or '—'} | "
                   f"{code(re.sub(r'_C$', '', obj_name(a['p'].get('ActionClass')))) if a['p'].get('ActionClass') else '—'} | "
                   f"{code(obj_name(a['p'].get('ActivationContextType'))) if a['p'].get('ActivationContextType') else '—'} | "
                   f"{flags(a) or '—'} | {eff} | {bd} |")
    out += ["", f"*{FAMILIES[fam]}: response rules*", "",
            "| Action asset | Response rules (Key: tags) |", "|---|---|"]
    for g in group_rows(rows, lambda a: tuple(rules(a))):
        a = g[0]
        nm = (f"{len(g)} assets: " + asset_names(g)) if len(g) > 1 else code(a["name"])
        out.append(f"| {nm} | {'<br>'.join(rules(a)) or '— (no ActionResponseData)'} |")
    return "\n".join(out)


def summary_table():
    acts = actions().values()
    out = ["| Family | BHActionDefinition | WDActionDefinition | Total |", "|---|---:|---:|---:|"]
    tot = collections.Counter()
    for fam, label in FAMILIES.items():
        c = collections.Counter(a["type"] for a in acts if family(a) == fam)
        out.append(f"| {label} | {c['BHActionDefinition']} | {c['WDActionDefinition']} | {sum(c.values())} |")
        tot.update(c)
    out.append(f"| **All** | **{tot['BHActionDefinition']}** | **{tot['WDActionDefinition']}** | **{sum(tot.values())}** |")
    return "\n".join(out)


def fields_table():
    acts = list(actions().values())
    keys = collections.Counter()
    for a in acts:
        for k in a["p"]:
            keys[(a["type"], k)] += 1
    nb = sum(a["type"] == "BHActionDefinition" for a in acts)
    nw = len(acts) - nb
    out = ["| Property | In BH (of %d) | In WD (of %d) |" % (nb, nw), "|---|---:|---:|"]
    for k in sorted({k for _, k in keys}, key=lambda k: (-(keys[("BHActionDefinition", k)] + keys[("WDActionDefinition", k)]), k)):
        out.append(f"| `{k}` | {keys[('BHActionDefinition', k)]} | {keys[('WDActionDefinition', k)]} |")
    rt = collections.Counter()
    for a in acts:
        for r in a["p"].get("ActionResponseData", []):
            rt[r["Key"].split("::")[1]] += 1
    out += ["", "| Response type | Entries |", "|---|---:|"]
    out += [f"| `{k}` | {v} |" for k, v in rt.most_common()]
    ct = collections.Counter(obj_name(a["p"].get("ActivationContextType")) or "(none)" for a in acts)
    out += ["", "| Activation context struct | Actions |", "|---|---:|"]
    out += [f"| `{k}` | {v} |" for k, v in ct.most_common()]
    return "\n".join(out)


def num(x):
    return f"{x:g}"


def ge_modifier(m):
    sys.path.insert(0, os.path.join(ROOT, "_tools"))
    import ge_values
    return ge_values.modifier(m)


def effects_table():
    ge = ge_index()
    users = collections.defaultdict(list)
    for a in actions().values():
        for _, g in effects_of(a):
            users[g].append(a["name"])
    out = ["| Effect | Used by actions | Duration (s) | Modifiers | Granted tags |", "|---|---|---:|---|---|"]
    for g in sorted(users):
        r = ge.get(g)
        names = ", ".join(code(n) for n in sorted(users[g]))
        if not r:
            out.append(f"| `{g}` | {names} | not in ge-values.json | | |")
            continue
        mods = "<br>".join(ge_modifier(m) for m in r["modifiers"]) or "—"
        dur = num(r["duration"]) if r.get("duration") is not None else "native default"
        gt = "<br>".join(code(t) for t in r.get("granted_tags") or []) or "—"
        out.append(f"| `{g}` | {names} | {dur} | {mods} | {gt} |")
    return "\n".join(out)


def appliable_rows():
    rows = []
    for p in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8", errors="ignore") as f:
            if "WDItemExtensionData_Appliable\"" not in f.read():
                continue
        item = os.path.splitext(os.path.basename(p))[0]
        for e in load(p):
            if e.get("Type") != "WDItemExtensionData_Appliable":
                continue
            pr = e["Properties"]
            rows.append((item, rel(p), pr))
    return rows


def appliables_table():
    out = ["| Item | Heal / attribute | Applied effects | Continuous | Container | Action entry | Owner states required | Time method | Animation tag | Consumed per use | Target states required | World interaction |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for item, _, pr in sorted(appliable_rows()):
        attr = short(pr.get("Attribute", {}).get("TagName", ""), "Attribute.Gameplay.")
        if "AttributeValue" in pr:
            attr += f" {pr['AttributeValue']:+g}" + (" (delta)" if pr.get("bApplyAsDelta") else " (delta flag not set)")
        eff = ", ".join(code(re.sub(r"_C$", "", obj_name(x))) for x in pr.get("AppliedEffects", [])) or "—"
        cont = "yes" if pr.get("bContinuousUse") else "—"
        cd = "yes" if pr.get("bContainerAppliable") else "—"
        ents = pr.get("AppliableActionData", [])
        if not ents:
            out.append(f"| {code(item)} | {attr or '—'} | {eff} | {cont} | {cd} | (none) | | | | | | |")
        for en in sorted(ents, key=lambda x: x["Key"]["TagName"]):
            v = en["Value"]
            wi = obj_name(v.get("WorldInteractionContextClass")) or ("world interactable" if v.get("bWorldInteractableUse") else "—")
            out.append(
                f"| {code(item)} | {attr or '—'} | {eff} | {cont} | {cd} | {code(short(en['Key']['TagName']))} | "
                f"{tags(v.get('RequiredOwnerStates', []), 'State.Player.') or '—'} | "
                f"{v.get('InteractionTimeMethod', '').split('::')[-1] or '—'} | "
                f"{code(short(v.get('AnimationTag', {}).get('TagName', ''), 'Animation.Asset.')) if v.get('AnimationTag', {}).get('TagName', 'None') != 'None' else '—'} | "
                f"{v.get('AmountConsumedOnUse', '—')} | "
                f"{tags(v.get('RequiredTargetStates', []), 'State.Player.') or '—'} | {wi} |")
    return "\n".join(out)


def bindings_table():
    out = ["| Action tag | Activated by (items) | Input tags | Released by (items) |", "|---|---|---|---|"]
    known = {a["tag"] for a in actions().values()}
    for tag, b in sorted(bindings().items()):
        if tag not in known:
            continue
        it = sorted(b["activate"])
        s = ", ".join(code(i) for i in it[:6]) + (f" +{len(it) - 6}" if len(it) > 6 else "")
        c = sorted(b["complete"])
        sc = ", ".join(code(i) for i in c[:4]) + (f" +{len(c) - 4}" if len(c) > 4 else "")
        out.append(f"| {code(short(tag))} | {s or '—'} | {', '.join(code(i) for i in sorted(b['inputs'])) or '—'} | {sc or '—'} |")
    return "\n".join(out)


def unbound_table():
    b = bindings()
    out = ["| Action asset | Action tag |", "|---|---|"]
    for a in sorted(actions().values(), key=lambda a: a["name"]):
        if a["tag"] not in b:
            out.append(f"| {code(a['name'])} | {code(short(a['tag']))} |")
    return "\n".join(out)


# --- blocks ----------------------------------------------------------------------------------------

BLOCK = re.compile(r"<!-- action_tables (.+?) -->\r?\n.*?<!-- /action_tables -->", re.S)


MONTAGE_GROUPS = [
    ("Use (medical)", [
        ("Bandage, self", "AM_FP_Bandage_Self_Heal"), ("Bandage, teammate", "AM_FP_Bandage_Teammate_Heal"),
        ("Individual First Aid Kit, self", "AM_FP_IFAK_Self_Heal"), ("Individual First Aid Kit, teammate", "AM_FP_IFAK_Teammate_Heal"),
        ("Medical Bag, other", "AM_FP_Medkit_Use"), ("Medical Bag, self", "AM_FP_Medkit_Use_Self"),
        ("Enox, self", "AM_FP_Enox_Use"), ("Stim Pen, self", "AM_FP_StimPen_Use"), ("Stim Pen, teammate", "AM_FP_StimPen_Use_Teammate"),
        ("Resuscitator", "AM_Resuscitator_Use"), ("Defibrillator", "AM_FP_Defib_Use"), ("Base revive (bare hands)", "AM_FP_Revive")]),
    ("Throw", [
        ("M67 frag, primary (overhand)", "AM_FP_Grenade_Throw_Overhand"), ("M67 frag, secondary (underhand)", "AM_FP_Grenade_Throw_Underhand"),
        ("M67 frag, throw back", "AM_FP_Grenade_Throw_It_Back"), ("Smoke, primary", "AM_FP_SmokeGrenade_Throw_Overarm"),
        ("Smoke, secondary", "AM_FP_SmokeGrenade_Throw_Underarm"), ("Molotov, primary", "AM_FP_Molotov_Throw_Overarm"),
        ("Molotov, secondary", "AM_FP_Molotov_Throw_Underarm"), ("C4 charge", "AM_FP_C4_Throw")]),
    ("Place", [
        ("AT mine", "AM_FP_AT_Mine_Place"), ("Claymore", "AM_FP_Claymore_Deploy"), ("IED (place)", "AM_FP_IED_Plant"),
        ("IED trigger (dial and ring)", "AM_FP_IED_Dial_and_Ring"), ("C4 detonator", "AM_FP_C4_Use")]),
]


def montage_points(asset):
    pts = []
    for e in bpd.topic_entries("item_actions"):
        if e["asset"] == asset and e["property"].startswith(("Notify:", "Section:")):
            pts.append((e["value"], e["property"].split(":", 1)[1] if e["property"].startswith("Notify:") else "section " + e["property"].split(":", 1)[1]))
    pts.sort(key=lambda x: (x[0], x[1]))
    return ", ".join("%s %s" % (n, bpd.fmt(round(t, 2))) for t, n in pts) or "-"


def montages_table():
    out = ["| Group | Action | First-person montage | Length (s) | Play rate | Timed points (s) |", "|---|---|---|---:|---:|---|"]
    for grp, rows in MONTAGE_GROUPS:
        for label, m in rows:
            ln = bpd.get("item_actions", m, "SequenceLength")
            rt = bpd.get("item_actions", m, "RateScale")
            if ln is None:
                continue
            out.append("| %s | %s | `%s` | %s | %s | %s |" % (grp, label, m, bpd.fmt(round(ln["value"], 2)), bpd.fmt(rt["value"]) if rt else "-", montage_points(m)))
    return "\n".join(out)


def render(mode):
    args = mode.split()
    if args[:1] == ["family"]:
        return family_table(args[1])
    return {"summary": summary_table, "fields": fields_table, "effects": effects_table,
            "appliables": appliables_table, "bindings": bindings_table, "unbound": unbound_table,
            "montages": montages_table}[args[0]]()


def write_docs():
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, no tables written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        mode = m.group(1)
        res = render(mode).strip()
        return nl.join([f"<!-- action_tables {mode} -->"] + res.split("\n") + ["<!-- /action_tables -->"])

    new, n = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{PAGE}: {n} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args:
        write_docs()
    elif "--family" in args:
        print(family_table(args[args.index("--family") + 1]))
    elif args and args[0].startswith("--"):
        print(render(args[0][2:]))
    else:
        print(summary_table())


if __name__ == "__main__":
    main()
