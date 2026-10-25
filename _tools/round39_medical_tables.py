"""Round 39 medical, status and movement values: assets/data/medical-status-r39.json and the page blocks that quote them.

    python -I _tools/round39_medical_tables.py            # print what would change
    python -I _tools/round39_medical_tables.py --write    # rewrite the JSON and the page blocks in place (idempotent)

Data-side values are read from data/ (spotter item extension data, suppression component, post-process rows,
CT_ReconSkills, DT_MedicSkills, ID_Resuscitator_Standard, ID_Armor weights). Native and Blueprint-bytecode values
(revive health path, Resuscitator action, GE defaults) are constants below with the RVA or asset they were read at;
they come from docs/evidence/round39-medical-movement.md. Blocks sit between

    <!-- r39_med NAME -->  ...  <!-- /r39_med -->
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "Wardogs")
OUT = os.path.join(ROOT, "assets", "data", "medical-status-r39.json")
BLOCK = re.compile(r"<!-- r39_med (\w+) -->\r?\n.*?<!-- /r39_med -->", re.S)


def load(path):
    text = open(path, encoding="utf8").read()
    if text.lstrip().startswith("---"):
        parts = re.split(r"^--- export:[^\n]*---\s*$", text, flags=re.M)
        return [json.loads(p) for p in parts if p.strip()]
    d = json.loads(text)
    return d if isinstance(d, list) else [d]


def find_key(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            r = find_key(v, key)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_key(v, key)
            if r:
                return r
    return None


def tag(v):
    return v.get("TagName") if isinstance(v, dict) else v


def spotting():
    """Per-device, per-target spot timing from BH_SpottingExtensionData (spotter items)."""
    rows = []
    for f in sorted(glob.glob(os.path.join(D, "Plugins", "GameFeatures", "Items", "**", "ID_*.json"), recursive=True)):
        if "BH_SpottingExtensionData_C" not in open(f, encoding="utf8").read():
            continue
        for e in load(f):
            if e.get("Type") != "BH_SpottingExtensionData_C":
                continue
            p = e["Properties"]
            for td in p.get("TargetData", []):
                v = td["Value"]
                rows.append({"item": os.path.basename(f)[3:-5], "action": tag(p.get("ActionTag")),
                             "tracking_bounds": p.get("TrackingBoundsDiameter"),
                             "target": td["Key"].split(".")[-1].replace("_C", ""),
                             "spot_time": v.get("SpotTime"), "spot_refresh_time": v.get("SpotRefreshTime"),
                             "decay_time": v.get("DecayTime"), "persistent_spot_time": v.get("PersistentSpotTime"),
                             "owner_skill_tag": tag(v.get("RequiredOwnerSkillTag"))})
    return rows


def recon_spot_curves():
    e = load(os.path.join(D, "Content", "Meta", "CharacterSkills", "CT_ReconSkills.json"))[0]
    return {k: [[x["Time"], x["Value"]] for x in v["Keys"]] for k, v in e["Rows"].items() if "Spot" in k}


def suppression():
    # B_CharacterSuppressionComponent (WDCharacterComponents) is a Blueprint, not in data/: values read with WdExtract dump.
    out = {"component": "WDCharacterComponents/Content/Components/B_CharacterSuppressionComponent",
           "effects": [
               {"type": "Default", "class": "WDSuppressionEffect_PostProcess", "post_process_tag": "PostProcessEffect.Suppression.Default", "decay_multiplier": 0.4},
               {"type": "Concussive", "class": "WDSuppressionEffect_PostProcess", "post_process_tag": "PostProcessEffect.Suppression.Concussive", "decay_multiplier": 0.1},
               {"type": "CameraShake", "class": "WDSuppressionEffect_CameraShake", "camera_shake": "B_CameraShake_Suppression_C"},
               {"type": "BackblastCameraShake", "class": "WDSuppressionEffect_CameraShake", "camera_shake": "B_CameraShake_Suppression_Backblast_C"}]}
    pp = load(os.path.join(D, "Content", "VFX", "Postprocess", "DT_PostProcessEffects.json"))[0]["Rows"]
    out["post_process"] = {k: {"material": v["MaterialClass"].get("ObjectName") if isinstance(v["MaterialClass"], dict)
                               else v["MaterialClass"], "duration": v["Duration"]}
                           for k, v in pp.items() if "Suppression" in k}
    base = {}
    for f in sorted(glob.glob(os.path.join(D, "Content", "GameMechanics", "Inventory", "Equipment", "Caliber", "*", "*ProjectileData*.json"))):
        for e in load(f):
            s = find_key(e.get("Properties") or {}, "SuppressionData")
            if s:
                base[os.path.basename(f)[3:-5]] = {"base": s.get("BaseSuppression"),
                                                    "falloff_range": s.get("DistanceFalloffRange")}
    out["projectile_base_suppression"] = base
    return out


def resuscitator():
    for e in load(os.path.join(D, "Plugins", "GameFeatures", "Items", "Enox", "Content", "Data", "ResuscitatorTest",
                               "ID_Resuscitator_Standard.json")):
        if e.get("Type") == "WDItemExtensionData_Appliable":
            p = e["Properties"]
            return {"revive_health_AttributeValue": p["AttributeValue"], "container": p["ContainerData"],
                    "interaction_time_method": p["AppliableActionData"][0]["Value"]["InteractionTimeMethod"]}


def armor_weights():
    out = {}
    for f in sorted(glob.glob(os.path.join(D, "Plugins", "GameFeatures", "Items", "Armor", "**", "ID_*.json"), recursive=True)):
        es = load(f)
        name = [e["Properties"].get("DisplayName", {}).get("SourceString") for e in es if e["Type"] == "BHInventoryItemDefinition"]
        w = [(e.get("Properties") or {}).get("Weight") for e in es if e["Type"] == "BHInventoryFragment_Weight"]
        out[os.path.basename(f)[3:-5]] = {"name": name[0] if name else None, "weight": w[0] if w else "no fragment"}
    return out


NATIVE_AND_BP = {
    "revive_health": {
        "mechanism": "AWDMoverCharacter::RevivePlayer (0x6E75620) passes its float to ResetHealth (0x6B16E80), which sets the "
                     "Health attribute to that value, or to DefaultHealthToReviveTo (+0x160 = 25) when the value is 0",
        "base_hand_revive": {"value": 10.0, "source": "UWDReviveInteractionContext ctor 0x772C5F0, +0x240 = 0x41200000; "
                             "passed by 0x772D860 as the 4th argument of vtable slot 323"},
        "defibrillator": 35.0, "medical_bag": 50.0, "resuscitator": 10.0},
    "enox_decay": {"timer_period_source": "DecayRate (+0x16C, 5 s), SetTimer in 0x6B168B0 loop=true",
                   "callback": "0x6B16EC0 subtracts fabs(attribute-eval helper 0x52311D0) from the pool (+0x17C)",
                   "decay_magnitude_readers": 0},
    "gameplay_effect_defaults": {"ctor": "0x5225C60 (UBHGameplayEffect)", "max_stacks": 1,
                                 "stack_duration_refresh_policy": "RefreshOnSuccessfulApplication",
                                 "stack_expiration_policy": "RemoveSingleStackAndRefreshDuration", "duration": 0.0},
    "ressed_by_enemy": {"applied_by": "B_Action_Resuscitator.OnInteractionFinished",
                        "condition": "target faction differs from the reviver's faction (AreActorsOfSameFaction false)",
                        "effect": "GE_Player_RessedByEnemy, 60 s, granted tag State.Player.RessedByEnemy"},
    "critical_revive_hold_threshold": {"reader": "0x6E69D20 passes +0x970 as the hold threshold when it builds the revive "
                                       "interaction context; HealHoldThreshold (+0x974) goes to the heal context"},
    "deathmatch_regen": {"HealthToRegenerate": 5.0, "TickInterval": 1.0, "ctor": "0x848B5F0",
                         "delay": "RegenDelay 10 s (UWDVitalityComponent 0x6B81720); OnRegenTimerStarted 0x84965F0 stores the "
                                  "delay deadline"},
}


def build():
    return {"meta": {"source": "docs/evidence/round39-medical-movement.md; written by _tools/round39_medical_tables.py"},
            "spotting": spotting(), "recon_spot_skill_curves": recon_spot_curves(), "suppression": suppression(),
            "resuscitator": resuscitator(), "armor_weights": armor_weights(), "native_and_blueprint": NATIVE_AND_BP}


def spot_block(d):
    seen = {}
    for r in d["spotting"]:
        seen.setdefault((r["target"], r["spot_time"], r["spot_refresh_time"], r["decay_time"], r["persistent_spot_time"]),
                        set()).add(r["item"])
    lines = ["| Target class | Spot time (s) | Refresh time (s) | Decay time (s) | Persistent spot time (s) | Spotter items |",
             "|---|---|---|---|---|---|"]
    for (t, a, b, c, e), items in sorted(seen.items(), key=lambda kv: (kv[0][3], kv[0][0])):
        lines.append(f"| `{t}` | {a} | {b} | {c:g} | {e:g} | {', '.join(sorted(items))} |")
    return "\n".join(lines)


def replace(path, name, body, write):
    p = os.path.join(ROOT, path)
    text = open(p, encoding="utf8").read()
    pat = re.compile(r"(<!-- r39_med " + name + r" -->\r?\n).*?(<!-- /r39_med -->)", re.S)
    if not pat.search(text):
        return False
    new = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)
    if new != text and write:
        open(p, "w", encoding="utf8", newline="").write(new)
    return new != text


def main():
    write = "--write" in sys.argv
    d = build()
    js = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
    old = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
    changed = [OUT] if js != old else []
    if write and js != old:
        open(OUT, "w", encoding="utf8", newline="").write(js)
    if replace("game-features/Wardogs_GameFeatures_Spotting_v2.md", "spot_times", spot_block(d), write):
        changed.append("Spotting page")
    print(("wrote " if write else "would change ") + (", ".join(changed) if changed else "nothing (up to date)"))


if __name__ == "__main__":
    main()
