"""Tables for game-features/Wardogs_Medical_v1.md, rebuilt from data/ and assets/data/ge-values.json.

Reads the item definitions of every medical item (appliable extension data, medkit extension data, durability,
stack size, container data, animation set), the GameplayEffects they apply (ge-values.json), the Medic skill rows
and curves (DT_MedicSkills, CT_MedicSkills), and the Medic skill-tree node texts (DT_CharacterSkillNodes_Data).
Native values (bleed-out, revive health, vitality defaults) are constants below with the RVA they were read at.
Each table sits between

    <!-- medical_tables MODE -->  ...  <!-- /medical_tables -->

Rerun after a data update (idempotent):

    python _tools/medical_tables.py --write      # refresh every block in place
    python _tools/medical_tables.py MODE         # print one block (counts, use, container, effect, medkit, effects,
                                                 #   states, skills, example)

Joins: item file -> WDItemExtensionData_Appliable / _MedKit / _Battery (Data); applied effect class name ->
ge-values.json entry (Data); skill row -> GE class and CT_MedicSkills curve (Data); item anim set -> montage name
(montage length is not exported, so use time in seconds is not traced). Worked example numbers are Derived.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT = ct.ROOT
DATA = ct.DATA
PAGE = "game-features/Wardogs_Medical_v1.md"
BLOCK = re.compile(r"<!-- medical_tables (\w+) -->\r?\n.*?<!-- /medical_tables -->", re.S)
link, cell, n, tag, objname, exports = ct.link, ct.cell, ct.n, ct.tag, ct.objname, ct.exports

W = "Wardogs/"
P = W + "Plugins/GameFeatures/Items/"
ITEMS = [
    W + "Content/Items/Consumables/Bandage/ID_Bandage.json",
    W + "Content/Items/Consumables/Bandage/ID_SuperBandage.json",
    P + "MedKit/Content/Data/ID_MedKit_Standard.json",
    P + "Enox/Content/Data/ID_Enox_Standard.json",
    P + "StimPen/Content/Data/ID_StimPen.json",
    P + "Defibrillator/Content/Data/ID_Defibrillator_Standard.json",
    P + "Enox/Content/Data/ResuscitatorTest/ID_Resuscitator.json",
    P + "Enox/Content/Data/ResuscitatorTest/ID_Resuscitator_Standard.json",
]
SKILL_TABLE = W + "Content/Meta/CharacterSkills/DT_MedicSkills.json"
CURVE_TABLE = W + "Content/Meta/CharacterSkills/CT_MedicSkills.json"
NODE_TABLE = W + "Content/UI/Data/DT_CharacterSkillNodes_Data.json"
TUTORIAL = W + "Content/UI/Features/Frontend/LearnToPlay/Data/ContentSceneData/TabData/Introduction/ContentTabData/DA_Tutorials_Health.json"
MAX_HEALTH = 100.0  # Native: UWDVitalityComponent constructor 0x6B81720 (BaseHealth = MaxHealth = 100). Blueprint may override.

# Native constants (decompile corpus CL-516586, image base 0x140000000; class defaults, the blueprint may override).
NATIVE = [
    ("Base bleed-out time", "300 s", "`AWDMoverCharacter` constructor `0x6E67160` writes `BaseBleedOutTime` (+0x980) = 300.0; the timer start `0x6E75540` copies it into total (+0x814) and remaining (+0x828)"),
    ("Minimum bleed-out time after a revive", "60 s", "constructor `0x6E67160` writes `MinBleedOutTime` (+0x984) = 60.0; `0x6E75540` uses `max(MinBleedOutTime, remaining)` when the revive counter byte (+0xA70) is nonzero, so a character that was revived once and goes down again restarts from at least 60 s, not 300 s"),
    ("Bleed-out drain", "dt x rate; kill at 0", "tick `0x6E780D0` subtracts `dt * rate` from the remaining time (floored at 0) and, with role byte 3, calls the kill path `0x6E71400` when it reaches 0. The rate it reads in the normal state is the float at +0x990 (SDK name `HoldOnBleedOutRate`, native default 0.1); in give-up state (byte +0x820 = 2) it reads +0x994 (`GiveUpBleedOutRate`, default 6.0). `DefaultBleedOutRate` (+0x98C, default 1.0) has no native reader, so the blueprint presumably sets +0x990 per state: the effective rate in each state is not traced"),
    ("Damage while critical", "none", "the bleed tick never calls the damage or health path; `UWDCharacterVitalityComponent` (`0x6B17760`) returns 0 and writes no health when the character lacks `State.Player.Vitality.Alive`. There is no damage-over-time bleeding"),
    ("Revive health (component default)", "25", "`UWDCharacterVitalityComponent` constructor `0x6B16790` writes `DefaultHealthToReviveTo` (+0x160) = 25.0. The revive handler (`AWDMoverCharacter` vtable slot 323, `0x6E75620`) sets the Alive tag, bumps the revive counter, restarts the bleed timer and calls `ResetHealth` (`0x6B16E80`); which function applies the 25 (or the Medical Bag's 50) is not traced, the revive call `RevivePlayer(..., float, ...)` is blueprint-implemented"),
    ("Max health", "100", "`UWDVitalityComponent` constructor `0x6B81720` writes `BaseHealth` = `MaxHealth` = 100.0 (the player blueprint may override; the cooked player blueprint is not in `data/`)"),
    ("Regeneration delay", "10 s", "same constructor: `RegenDelay` (+0x138) = 10.0. The damage path (`0x6B82520`) only broadcasts the `RegenTimer` delegate with this delay; no native tick that adds health to infantry was found. The only regeneration component in the data is `WDHealthRegenComponent`, added by the Deathmatch game feature (`OnRegenTimerStarted` `0x84965F0` is a ProcessEvent stub, so its logic and values are blueprint: not traced)"),
    ("Overheal pool", "max 0", "`MaxOverhealHealth` (+0x164) defaults to 0 in the constructor `0x6B16790`; the character clamp is `[0, MaxHealth + MaxOverhealHealth + MaxDecayHealth]` (`0x6B17D20`)"),
    ("Decay pool (Enox)", "max 0; DecayRate 5, DecayMagnitude 5", "constructor `0x6B16790`: `MaxDecayHealth` (+0x168) = 0, `DecayRate` (+0x16C) = 5.0, `DecayMagnitude` (+0x170) = 5.0. `Auth_CharacterHeal` (`0x6B168B0`) with a decay amount > 0 caps the heal at `MaxHealth + MaxDecay - health`, writes the decay pool (+0x17C) and starts a timer with period `DecayRate` whose callback `0x6B16EC0` subtracts a delta from health and the pool. That delta is not visible in the decompile (assumed `DecayMagnitude`, not confirmed). With `MaxDecayHealth` 0 the pool cannot hold anything, so the Enox only works if the blueprint raises it: not traced"),
    ("Damage reduces the decay pool", "by the damage", "`0x6B17760`, server role only: damage lowers the pool at +0x17C by the damage taken, at most to 0"),
]


def load():
    d = {"ge": {}, "items": [], "skills": {}, "curves": {}, "nodes": {}, "tut": {}}
    with open(os.path.join(ROOT, "assets", "data", "ge-values.json"), encoding="utf-8") as f:
        for e in json.load(f)["effects"]:
            d["ge"][e["name"]] = e
    for rel in ITEMS:
        path = os.path.join(DATA, rel)
        ex = exports(path)
        by = {}
        for e in ex:
            by.setdefault(e["Type"], []).append(e)
        item = {"rel": rel, "dir": os.path.dirname(path)}
        defn = by["BHInventoryItemDefinition"][0]["Properties"]
        item["id"] = tag(defn["ItemId"])
        item["name"] = (defn.get("DisplayName") or {}).get("SourceString") or item["id"]
        item["app"] = (by.get("WDItemExtensionData_Appliable") or [{}])[0].get("Properties")
        item["med"] = (by.get("WDItemExtensionData_MedKit") or [{}])[0].get("Properties")
        item["bat"] = (by.get("WDItemExtensionData_Battery") or [{}])[0].get("Properties")
        item["watts"] = next((e["Properties"] for t, v in by.items() if "WattsExtensionData" in t for e in v), None)
        item["cont"] = (item["app"] or {}).get("ContainerData")
        item["action_ge"] = []
        for e in by.get("WDActionDefinition", []):
            item["action_ge"] += [ge_name(v) for v in (e["Properties"].get("ActionEffects") or {}).values()] if isinstance(e["Properties"].get("ActionEffects"), dict) else []
        dur = (by.get("WDInventoryFragment_Durability") or [{}])[0].get("Properties")
        item["dur"] = dur["ReplicatedData"]["Durability"] if dur else None
        stk = (by.get("BHInventoryFragment_Stackable") or [{}])[0].get("Properties")
        item["stack"] = stk.get("MaxStackSize") if stk else None
        item["stackable"] = stk is not None
        if "Defibrillator" in rel:
            for e in exports(os.path.join(DATA, P + "Defibrillator/Content/Data/Actions/DA_Action_Defibrillator.json")):
                for kv in (e.get("Properties") or {}).get("ActionEffects", []) or []:
                    item["action_ge"].append(ge_name(kv["Value"]))
        item["anim"] = {}
        for e in by.get("WDItemExtensionData_Animation", []):
            setname = objname(e["Properties"].get("AnimationSet"))
            ap = os.path.join(item["dir"], setname + ".json") if setname else None
            if ap and os.path.exists(ap):
                for a in exports(ap)[0]["Properties"].get("Animations", []):
                    base = a["Value"]["BaseAsset"]
                    fp = objname(base.get("FirstPersonPlayerAnimation"))
                    item["anim"][tag(a["Key"])] = (fp, base.get("bOverrideLength"), base.get("OverrideLength"))
        d["items"].append(item)
    for e in exports(os.path.join(DATA, SKILL_TABLE)):
        if "Rows" in e:
            d["skills"] = e["Rows"]
    for e in exports(os.path.join(DATA, CURVE_TABLE)):
        if "Rows" in e:
            d["curves"] = {k: [(x["Time"], x["Value"]) for x in v["Keys"]] for k, v in e["Rows"].items()}
    for e in exports(os.path.join(DATA, NODE_TABLE)):
        if "Rows" in e:
            for k, v in e["Rows"].items():
                if k.startswith("Meta.Role.Medic."):
                    d["nodes"][k] = (v["FriendlyName"].get("CultureInvariantString") or "-",
                                     v["Description"].get("CultureInvariantString") or "-")
    return d


def short(t):
    return t.replace("State.Player.", "").replace("Attribute.Gameplay.", "") if t else t


def states(lst):
    return ", ".join(f"`{short(s)}`" for s in lst) or "-"


def ge_name(obj):
    nm = objname(obj) or ""
    return re.sub(r"_C$", "", nm)


def actions(item):
    """[(action tag, data)] from the appliable or medkit extension, medkit prefers its own."""
    src = item["med"] or item["app"] or {}
    return [(tag(a["Key"]), a["Value"]) for a in src.get("AppliableActionData", [])]


def method(a):
    return a["InteractionTimeMethod"].split("::")[-1]


def who(act):
    if "Secondary" in act or "SecondaryUse" in act:
        return "self"
    return "other player"


def use(d):
    out = ["| Item | Use | Time method | Animation (first-person montage) | Consumed per use | Stack or charges | Owner must be | Target must be |",
           "|---|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        for act, a in actions(it):
            anim = it["anim"].get(tag(a["AnimationTag"]))
            m = "-"
            if anim and anim[0]:
                m = f"`{anim[0]}`" + (f" (length overridden to {n(anim[2])} s)" if anim[1] else "")
            notifier = a.get("Notifier")
            tm = f"`{method(a)}`" + (f", notifier `{notifier}`" if notifier not in (None, "None") else "")
            if it["med"]:
                consumed = "durability (see medkit table)"
            elif it["bat"] is not None or it["app"] and it["app"].get("bContainerAppliable"):
                consumed = f"{n(a['AmountConsumedOnUse'])} (container unit)"
            else:
                consumed = n(a["AmountConsumedOnUse"])
            stack = []
            if it["stack"]:
                stack.append(f"stack of {it['stack']}")
            elif it["stackable"]:
                stack.append("stackable, size not set in the item (not traced)")
            if it["dur"]:
                stack.append(f"durability {n(it['dur'])}")
            out.append("| " + " | ".join([
                f"{it['name']} (`{it['id']}`)", f"`{act}` ({who(act)})", tm, m, consumed,
                cell("; ".join(stack) or "single item"), states(a["RequiredOwnerStates"]),
                states(a["RequiredTargetStates"])]) + " |")
    return "\n".join(out)


def effect_of(it, d):
    """(heal now, heal over time, revive, cures, side effects, stacking) strings for one item."""
    app, med = it["app"] or {}, it["med"]
    ges = []
    for _, a in actions(it):
        for e in (a.get("EffectsToApply") or {}).get("Effects", []):
            ges.append(ge_name(e["Effect"]))
    for e in (app.get("AppliedEffects") or []) + ((med or {}).get("AppliedEffects") or []):
        ges.append(ge_name(e))
    ges += it["action_ge"]
    ges = list(dict.fromkeys(ges))
    ge_txt = ", ".join(f"`{g}`" for g in ges) or "-"
    nm = it["id"]
    if med:
        heal = (f"self {n(med['HealSelfAmount'])} over {n(med['HealSelfDuration'])} s; other {n(med['HealOtherAmount'])} "
                f"over {n(med['HealOtherDuration'])} s")
        hot = (f"self {n(med['HealSelfAmount'] / med['HealSelfDuration'])} HP/s; other "
               f"{n(med['HealOtherAmount'] / med['HealOtherDuration'])} HP/s (Derived: amount / duration)")
        rev = f"{n(med['ReviveOtherHealthAmount'])} health (durability {n(med['ReviveOtherDurabilityCost'])})"
    elif nm.startswith("Id.Item.Resus") or nm.startswith("Id.Item.Defib"):
        heal, hot = "-", "-"
        rev = "instant revive; revive health not traced"
        if nm.startswith("Id.Item.Resus"):
            rev = "revive; health after revive not traced"
    elif app.get("AttributeValue") and tag(app.get("Attribute")) == "Attribute.Gameplay.Health":
        heal = f"+{n(app['AttributeValue'])} health ({'delta' if app.get('bApplyAsDelta') else 'set'})"
        hot = "no per-tick value in data; one `AttributeValue` per use (when it is applied within the animation: not traced)"
        rev = "-"
        if "Enox" in nm:
            heal = "+40 as decaying health (`DecayHealAmount` 40)"
            hot = "decays after use; pool size and decay delta not traced (see states)"
    else:
        heal, hot, rev = "-", "-", "-"
    return heal, hot, rev, ge_txt


def effect(d):
    out = ["| Item | Heal now | Heal over time | Revive | Cures or removes | Applied effects | Side effects | Stacking and cooldown |",
           "|---|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        heal, hot, rev, ge_txt = effect_of(it, d)
        nm = it["id"]
        side = []
        if "GE_UseAppliable" in ge_txt:
            side.append("movement speed x0.5 while using (`GE_UseAppliable`, no duration set; removal by the action, not traced)")
        if "StimPen" in nm:
            side.append("60 s: tac sprint stamina use x0, focus energy use x0; tags `Stimulant.UnlimitedTacSprint`, `InhibitWeight.StepDown` (equipment weight class one step lower); camera FOV x1.05 (ignored while Critical)")
        if "Defib" in nm:
            side.append("`GE_Defib` (from the action) grants tag `Reviving.Friendly` (no modifiers)")
            if it["watts"]:
                side.append(f"watts extension `Damage` {n(it['watts']['Damage'])} (what it applies to is not traced)")
        stack = []
        if it["stack"]:
            stack.append(f"carry up to {it['stack']}")
        elif it["stackable"]:
            stack.append("stackable, size not set (not traced)")
        if "Bandage" in nm:
            stack.append("the primary and secondary bandage use block each other (response rules in Item Actions §4.1)")
        if "StimPen" in nm:
            stack.append("effect `Stacks` 1; `max_stacks` and refresh policy are not set in data (native default not traced); the two stim uses block each other")
        if "Defib" in nm:
            stack.append("cannot be used while the user is Critical")
        if "Resus" in nm:
            stack.append("single use per purchase (shop text)")
        if "MedKit" in nm:
            stack.append("no cooldown in data; durability 150 is the limit")
        if "Enox" in nm:
            stack.append("requires Injured; no cooldown in data")
        out.append("| " + " | ".join([
            f"{it['name']} (`{nm}`)", cell(heal), cell(hot), cell(rev),
            "no cure or removal tags in data (no bleed, splint or poison state exists to cure)", ge_txt,
            cell("; ".join(s for s in side if s) or "-"), cell("; ".join(stack) or "-")]) + " |")
    return "\n".join(out)


def mult_steps(d):
    keys = d["curves"].get("ReduceUsage_Medkit", [])
    return keys


def medkit(d):
    it = next(i for i in d["items"] if i["med"])
    m = it["med"]
    mults = mult_steps(d)
    out = ["| Action | Amount | Duration | Rate (Derived) | Durability cost | Uses from 150 durability (Derived) |", "|---|---|---|---|---|---|"]
    rows = [("Heal self", m["HealSelfAmount"], m["HealSelfDuration"], m["HealSelfDurabilityCost"]),
            ("Heal other", m["HealOtherAmount"], m["HealOtherDuration"], m["HealOtherDurabilityCost"]),
            ("Revive other (health after revive)", m["ReviveOtherHealthAmount"], None, m["ReviveOtherDurabilityCost"])]
    for name, amt, dur_s, cost in rows:
        rate = f"{n(amt / dur_s)} HP/s" if dur_s else "-"
        uses = n(it["dur"] / cost)
        out.append(f"| {name} | {n(amt)} | {n(dur_s) + ' s' if dur_s else '-'} | {rate} | {n(cost)} | {uses} |")
    out.append("")
    out.append("`ReduceUsage_Medkit` skill curve (multiplies `Attribute.Gameplay.Item.UsageRateMultiplier`, which the item lists as default 1; "
               "**Data**): " + ", ".join(f"key {n(t)}: {n(v)}" for t, v in mults) + " (the curve is evaluated at the skill level, which the Progression page describes).")
    out.append("")
    out.append("| Skill curve value | Durability cost per self heal | per other heal | per revive | Self heals per kit | Other heals per kit | Revives per kit |")
    out.append("|---|---|---|---|---|---|---|")
    for t, v in mults:
        cs, co, cr = (m["HealSelfDurabilityCost"] * v, m["HealOtherDurabilityCost"] * v, m["ReviveOtherDurabilityCost"] * v)
        out.append(f"| key {n(t)}: {n(v)} | {n(cs)} | {n(co)} | {n(cr)} | {n(it['dur'] / cs)} | {n(it['dur'] / co)} | {n(it['dur'] / cr)} |")
    return "\n".join(out)


def fmt_mod(m):
    a = short(m["attribute"])
    k = m["kind"]
    if k == "Scalar":
        return f"{a} {m['op']} {n(m['value'])}"
    if k == "SetByCaller":
        fb = f", fallback {n(m['fallback_value'])}" if m.get("allow_fallback") else ", no fallback"
        return f"{a} {m['op']} set-by-caller `{short(m['set_by_caller_tag'])}` (x{n(m['coefficient']['value'])}{fb})"
    return f"{a} {m['op']} {k}"


def ge_list(d):
    names = []
    for it in d["items"]:
        for _, a in actions(it):
            for e in (a.get("EffectsToApply") or {}).get("Effects", []):
                names.append(ge_name(e["Effect"]))
        for e in (it["app"] or {}).get("AppliedEffects", []) or []:
            names.append(ge_name(e))
        for e in (it["med"] or {}).get("AppliedEffects", []) or []:
            names.append(ge_name(e))
    for row in d["skills"].values():
        for se in row["SkillEffects"]:
            for eff in se["Value"]["SkillEffects"]:
                names.append(ge_name(eff["Effect"]))
    names += ["GE_Defib", "GE_Player_RessedByEnemy"]
    return list(dict.fromkeys(names))


def effects(d):
    out = ["| GameplayEffect | Modifiers | Duration | Granted tags | Magnitude source |", "|---|---|---|---|---|"]
    for nm in ge_list(d):
        e = d["ge"].get(nm)
        if not e:
            out.append(f"| `{nm}` | not in ge-values.json | - | - | - |")
            continue
        mods = "<br>".join(fmt_mod(m) for m in e["modifiers"]) or "none"
        dur = f"{n(e['duration'])} s" if e["duration"] is not None else "not set (native default)"
        tags = ", ".join(f"`{short(t)}`" for t in e["granted_tags"]) or "-"
        src = []
        if any(m["kind"] == "SetByCaller" for m in e["modifiers"]):
            src.append("set by the caller (skill curve or native code)")
        if not e["modifiers"]:
            src.append("tag only")
        if nm == "GE_Item_UsageRateMultiplier":
            src = ["skill `ReduceUsage_Medkit` supplies the value (Data)"]
        if nm == "GE_Weapon_EquipSpeedMultiplier":
            src = ["skill `MedicalItemSwapSpeed` supplies the value (Data)"]
        if nm == "GE_Player_SprintSpeedMultiplier_Temp":
            src = ["skills `ReviveSpeedBoost.*` supply both values (Data)"]
        if nm == "GE_Player_RessedByEnemy":
            src = ["tag only; what applies it is not traced"]
        out.append(f"| `{nm}` | {cell(mods)} | {dur} | {tags} | {cell('; '.join(src) or 'fixed in the effect')} |")
    return "\n".join(out)


def states_block(d):
    out = ["| Mechanic | Value | Source (**Native**) |", "|---|---|---|"]
    for a, b, c in NATIVE:
        out.append(f"| {cell(a)} | {cell(b)} | {cell(c)} |")
    return "\n".join(out)


def tutorial_lines(d):
    lines = []
    for e in exports(os.path.join(DATA, TUTORIAL)):
        txt = json.dumps(e.get("Properties", {}))
        for m in re.finditer(r'"SourceString": "([^"]+)"', txt):
            lines.append(m.group(1))
    return list(dict.fromkeys(lines))


def skills(d):
    out = ["| Skill | Skill-tree text | Resolved in data | Effect on medical numbers |", "|---|---|---|---|"]
    for key in sorted(d["nodes"]):
        fn, desc = d["nodes"][key]
        row = d["skills"].get(key)
        res, eff = "no data row (not traced)", "-"
        if row:
            parts = []
            for se in row["SkillEffects"]:
                for eff_ in se["Value"]["SkillEffects"]:
                    g = d["ge"].get(ge_name(eff_["Effect"]), {})
                    dur = f", {n(g['duration'])} s" if g.get("duration") is not None else ""
                    for cm in eff_["CustomMagnitudes"]:
                        crow = cm["Value"]["Curve"]["RowName"]
                        curve = ", ".join(f"{n(t)}: {n(v)}" for t, v in d["curves"].get(crow, []))
                        parts.append(f"`{short(tag(cm['Key']))}` from `{crow}` ({curve}){dur}")
            res = "yes (`DT_MedicSkills`)"
            eff = "<br>".join(parts)
        out.append(f"| `{key.replace('Meta.Role.Medic.', '')}` | {cell(fn)}: {cell(desc)} | {res} | {cell(eff)} |")
    return "\n".join(out)


def container(d):
    out = ["| Item | Attribute and amount | Container start / max | Update time | Update amount | Derived reading |", "|---|---|---|---|---|---|"]
    for it in d["items"]:
        c = it["cont"]
        if not c:
            continue
        app = it["app"]
        read = "-"
        if "Defib" in it["id"]:
            read = (f"if a full charge is the {n(app['AttributeValue'])} amount: {n(app['AttributeValue'] / c['UpdateAmount'] * c['UpdateTime'])} s "
                    "to charge (the threshold is not confirmed); `ChargesPerSecondConsumption` is 0, battery cost per charge not traced")
        else:
            read = (f"{n(c['StartingAmount'])} units emptied at {n(c['UpdateAmount'])} per {n(c['UpdateTime'])} s = "
                    f"{n(c['StartingAmount'] / c['UpdateAmount'] * c['UpdateTime'])} s to empty; whether a revive needs all {n(c['StartingAmount'])} units is not traced")
        out.append("| " + " | ".join([
            f"{it['name']} (`{it['id']}`)", f"`{short(tag(app['Attribute']))}` {n(app['AttributeValue'])}"
            + (" (delta)" if app.get("bApplyAsDelta") else ""),
            f"{n(c['StartingAmount'])} / {n(c['MaxAmount'])}" if "StartingAmount" in c else "-",
            f"{n(c['UpdateTime'])} s", n(c["UpdateAmount"]), cell(read)]) + " |")
    out += ["", "Batteries that feed the defibrillator (**Data**, `Plugins/GameFeatures/Items/Battery`): `Id.Item.Battery` holds up to 100 `Id.Item.BatteryCharge`, `Id.Item.LargeBattery` up to 250 (`MaxSlotAmountStackSize` of the charge container). "
            "The defibrillator takes a battery as its magazine (`Item.Attachment.Magazine.Battery`) and starts with one `Id.Item.Battery`."]
    return "\n".join(out)


def counts(d):
    nodes = d["nodes"]
    res = sum(1 for k in nodes if k in d["skills"])
    return "\n".join([
        "| Measure | Count |", "|---|---|",
        f"| Medical item definitions read | {len(d['items'])} |",
        f"| Medic skill-tree nodes | {len(nodes)} |",
        f"| Medic skills resolved to a GameplayEffect and curve | {res} |",
        f"| Medic skills with no data row | {len(nodes) - res} |",
        f"| GameplayEffects resolved | {sum(1 for g in ge_list(d) if g in d['ge'])} of {len(ge_list(d))} |"])


def example(d, start=20.0):
    it = next(i for i in d["items"] if i["med"])
    m = it["med"]
    mults = d["curves"]["ReduceUsage_Medkit"]
    need = MAX_HEALTH - start
    bandage = next(i for i in d["items"] if i["id"] == "Id.Item.Bandage")["app"]["AttributeValue"]
    out = [f"Start at {n(start)} health, goal {n(MAX_HEALTH)} (assumed max health, **Native** default; need {n(need)}). "
           "All figures are **Derived** from the item data above.", "",
           "| Method | Uses needed | Time | Items or durability spent | Notes |", "|---|---|---|---|---|"]
    k = math.ceil(need / bandage)
    out.append(f"| Bandage (self) | {k} | {k} x one bandage animation (seconds not traced) | {k} of a stack of 5 | +{n(bandage)} each; the last one is clamped at max health |")
    out.append(f"| Individual First Aid Kit (self) | 1 | 1 x one use (seconds not traced) | 1 kit | +100 clamps at max health |")
    t = need / (m["HealSelfAmount"] / m["HealSelfDuration"])
    dcost = need * m["HealSelfDurabilityCost"] / m["HealSelfAmount"]
    out.append(f"| Medical Bag (self) | continuous | {n(t)} s | {n(dcost)} durability ({n(dcost / it['dur'] * 100)} % of 150) | assumes the 35 HP is spread evenly over 5 s and durability is spent in proportion; if cost is charged per full {n(m['HealSelfDuration'])} s step instead it is {n(math.ceil(need / m['HealSelfAmount']) * m['HealSelfDurabilityCost'])} |")
    for tt, v in mults[1:]:
        out.append(f"| Medical Bag (self), skill curve value {n(v)} | continuous | {n(t)} s | {n(dcost * v)} durability | assumes `UsageRateMultiplier` scales the cost (not traced) |")
    t2 = need / (m["HealOtherAmount"] / m["HealOtherDuration"])
    d2 = need * m["HealOtherDurabilityCost"] / m["HealOtherAmount"]
    out.append(f"| Medical Bag (teammate) | continuous | {n(t2)} s | {n(d2)} durability | 10 HP/s, cheap per HP; heals stop if the user moves away (tutorial text) |")
    out.append("| Enox | 1 | one use (seconds not traced) | 1 | gives 40 health as decaying health, not permanent; pool limits not traced |")
    out.append("| Natural regeneration | - | - | - | no infantry regen tick traced outside Deathmatch |")
    return "\n".join(out)


MODES = {"counts": counts, "container": container, "use": use, "effect": effect, "medkit": medkit, "effects": effects,
         "states": states_block, "skills": skills, "example": example}


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
        return nl.join([f"<!-- medical_tables {m.group(1)} -->"] + body + ["<!-- /medical_tables -->"])
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
