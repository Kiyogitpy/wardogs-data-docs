"""Round 40 medical, armour and movement values: assets/data/medical-status-r40.json and the page blocks that quote them.

    python -I _tools/round40_medical_movement.py            # print what would change
    python -I _tools/round40_medical_movement.py --write    # rewrite the JSON and the page blocks in place (idempotent)

Armour numbers (durability, stages, weights) are read from data/ (ID_*Armor / ID_*Helmet in Items/Armor). Native values (the
UWDPlayerVitalityState_Critical constructor, UBHMoverSwimmingDataAsset constructor, WDPingComponent constructor, the
Weight fragment constructor, the ground-mode speed pipeline) and Blueprint values (Halligan DurabilityCost, pawn CDO) are
constants below with the RVA or asset they were read at; they come from docs/evidence/round40-medical-movement.md.
Blocks sit between

    <!-- r40_med NAME -->  ...  <!-- /r40_med -->

If a page has no such block yet, the section that holds it is inserted once (before the anchor named in SECTIONS).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "Wardogs")
OUT = os.path.join(ROOT, "assets", "data", "medical-status-r40.json")
ARMOR_DIR = os.path.join(D, "Plugins", "GameFeatures", "Items", "Armor", "Content", "Data")
EV = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md"


def load(path):
    text = open(path, encoding="utf-8-sig").read()
    parts = re.split(r"^--- export:[^\n]*---\s*$", text, flags=re.M)
    return [json.loads(p) for p in parts if p.strip()]


def armor():
    """Per armour piece: durability, the four stage rows, covered locations, weight."""
    rows = []
    for f in sorted(glob.glob(os.path.join(ARMOR_DIR, "ID_*.json"))):
        name = os.path.basename(f)[:-5]
        row = {"item": name, "weight": None, "durability": None, "stages": [], "covered": [], "context_tag": None}
        for e in load(f):
            pr = e.get("Properties") or {}
            if e.get("Type") == "BHInventoryFragment_Weight":
                row["weight"] = pr.get("Weight", "default")
            if e.get("Type") == "WDInventoryFragment_Armor":
                row["context_tag"] = (pr.get("DamageContextTag") or {}).get("TagName")
                row["durability"] = (pr.get("ReplicatedData") or {}).get("Durability")
                row["covered"] = [c.split(".")[-1] for c in pr.get("CoveredHitLocations", [])]
                row["stages"] = [[s.get("DamagePercentageReduction"), s.get("Thickness"), s.get("Density")]
                                 for s in pr.get("DurabilityStagesSetupData", [])]
        rows.append(row)
    return rows


def ge_ghillie():
    d = json.load(open(os.path.join(ROOT, "assets", "data", "ge-values.json"), encoding="utf8"))
    for x in d["effects"]:
        if x["name"] == "GE_Player_GhilliEffects":
            return {"requires": (x.get("application_requirements") or {}).get("require"),
                    "modifiers": [[m["attribute"].replace("Attribute.Gameplay.", ""), m["op"], m["value"]] for m in x["modifiers"]]}
    return {}


# Native and Blueprint constants (evidence page has the reading path of each).
NATIVE = {
    "critical_state": {
        "ctor": "0x6E9B030 (UWDPlayerVitalityState_Critical)",
        "vitality_tag_source": "ctor stores global tag qword_14D36B800 at +0x28 (VitalityTag); the Critical state object carries "
                               "State.Player.Vitality.Critical and the character applies a state's VitalityTag when it enters it",
        "InputMappingContextPriority": 2, "bIsPlayerAbleToGiveUp": True, "CallForHelpCooldownTime": 5.0,
        "pawn_states": ["WDPlayerVitalityState_Alive", "B_WDPlayerVitalityState_Critical_C", "WDPlayerVitalityState_Dead"],
        "pawn_values": {"GiveUpBleedOutRate": 240.0, "OutOfBoundsTimeLimit": 20.0, "CriticalReviveHoldThreshold": 10.0,
                        "core_pawn_CriticalReviveHoldThreshold": 20.0, "BaseBleedOutTime": 360.0, "MinBleedOutTime": 30.0,
                        "BleedOutRevivePenaltyOffset": 100.00002, "HoldOnBleedOutRate": 0.5},
        "camera": {"asset": "DA_CharacterModifierState_Critical", "Priority": 0, "PitchLockAngle": 40.0,
                   "DefaultState": "Character transform, bone head, world offset (0, -200, 0), transition 0 s",
                   "DraggedState": "Character transform, bone pelvis, relative offset (3, 20, 0), rotation (0, 110, -90)",
                   "character_modifier": "B_CharacterModifier_IgnoreLookInput",
                   "condition": "State.Player.Vitality.Critical and none of the vehicle roles (driver, gunner, active or passive passenger)"}},
    "halligan": {"item": "ID_Crowbar", "durability": 7000.0, "cost_per_use": -1000.0, "uses": 7,
                 "actions": ["B_Action_ForceOpenDoor", "B_Action_ForceUnlockVehicle"],
                 "call": "WDDurabilityHelpers::UpdateDurability(owner, WDItemExtension_Inventory, DurabilityCost, 0.0, 100000.0); "
                         "ConsumeItem() when the returned durability is <= 0",
                 "source": "ID_Crowbar WDInventoryFragment_Durability (data); DurabilityCost -1000 in the CDO of both action Blueprints"},
    "armor_durability_write": {"queue": "WDPlayerInventoryComponent.QueuedArmorDamageEvents (+0xA60), 20-byte events {slot tag, fragment, Amount}",
                               "producer": "0x6B53280 (called from the slot-5 hook 0x6E74970 and 0x6B676DD)",
                               "consumer": "tick 0x6B64EC0 loops 0x6B59000, which does Durability -= Amount on the replicated armour "
                                           "entry, updates the stage index and sends WDEvent_ArmorDamage"},
    "weight_default": {"ctor": "0x67793A0 (UBHInventoryFragment_Weight)", "value": 1.0,
                       "note": "stores 0x3F800000 at +0x38; fragments that omit Weight (Level 1 Helmet, Tank, Pilot, Ghillie headwear) take it"},
    "enox_decay": {"callback": "0x6B16EC0", "per_tick": "min(DecayMagnitude (+0x170), decay pool (+0x17C))",
                   "application": "applied to the Health attribute through 0x52311D0 (negated), the pool then drops by |applied|",
                   "DecayRate": 5.0, "DecayMagnitude": 5.0},
    "deathmatch_regen": {"component": "UWDHealthRegenComponent", "tick": "0x8496170 (vtable slot 131)",
                         "HealthToRegenerate": 5.0, "TickInterval_field": 1.0,
                         "gate": "stored regen deadline byte (+0xF0, set by OnRegenTimerStarted 0x84965F0 as world time + RegenDelay) "
                                 "reached, then if CurrentHealth < MaxHealth a heal event of HealthToRegenerate (movss at 0x849627C) "
                                 "is sent through the vitality component vtable +0x518",
                         "open": "TickInterval (+0xEC) has no reader; whether it feeds the component tick rate was not shown"},
    "swimming_defaults": {
        "ctor": "0x52B3270 (UBHMoverSwimmingDataAsset)",
        "values": {"MaxInputSpeed": 250.0, "InputAcceleration": 500.0, "InputDeceleration": 800.0, "FastSwimMultiplier": 2.0,
                   "FastSwimStaminaUsagePerSecond": 20.0, "bFastSwimConsumesStamina": True, "WaterAcceleration": 1000.0,
                   "MaxStepHeight": 40.0, "IdealImmersionDepth": 156.0, "IdealImmersionDepthTolerance": 7.5,
                   "ImmersionDepthToStartSwimming": 170.0, "ImmersionDepthToStopSwimming": 120.0, "MaxBuoyancyForce": 3800.0,
                   "BuoyancyFrictionUp": 3.0, "BuoyancyExpDragUp": 0.05, "BuoyancyFrictionDownSubmerged": 7.5,
                   "BuoyancyExpDragDownSubmerged": 0.1, "BuoyancyFrictionDown": 5.0, "BuoyancyExpDragDown": 0.05},
        "overridden_in_DA_SwimmingMovement": {"WaterAcceleration": 4000.0, "InputDeceleration": 500.0}},
    "ping_component": {"ctor": "0x6B472C0 (UWDPingComponent)", "Cooldown": 0.1,
                       "DoublePingThreshold": 0.25, "PingTraceAngle": 5.0, "TraceChannel": 26,
                       "note": "unit of the first three presumed seconds, seconds, degrees; no Blueprint override was found"},
    "pawn": {"asset": "B_WDMoverPlayerCharacter CDO", "ProneHeldThreshold": 0.25, "CloseAnimationDistance": 3500.0,
             "WalkGunBobRotation": "CRV_LandGunBob", "first_person_fov": 106.0,
             "PlayerInteractionData_ServerBoxExtent": [50.0, 50.0, 50.0],
             "TacSprintFOV": "parent: keys (0,0) (0.25,5) (0.5,0), hold 0.25; WDCore pawn: delta 10, fade 0.25 in/out, hold 1.0",
             "PlayerKillFOV": "parent: keys (0,0) (0.05,-2.5) (0.25,-2.5) (0.3,0) (1,0), chromatic aberration x2.0; WDCore pawn: "
                              "duration 0.25, delta 11, chromatic aberration x3.5"},
    "death_effect_close_eyes": {
        "asset": "B_CharacterDeathStateEffectComponent",
        "blink": {"BlinkCycleDuration": 5.0, "BlinkCycleRandomness": 0.35, "BlinkCooldownDuration": 0.65, "MinimumBlinkOpenness": 0.35,
                  "OpenHoldDuration": 3.75, "OpenHoldDurationRandomness": 0.35, "BlinkSpeedScaleFactor": 0.85, "TwitchDuration": 0.5,
                  "TwitchMagnitude": 0.3, "MinBlurValue": 1.0, "EaseInOutExponent": 0.65},
        "linear": [["Eye_Mask_Visibility", None, None, 0.965, 0.94], ["Exposure", 1.0, 0.0, None, None],
                   ["Eye_Strain_Visibility", None, None, 0.7, 0.65], ["Blur_Strength", 1.0, 3.0, 0.9, 0.2],
                   ["Distortion_Amp", 0.0035, 0.005, 0.85, 0.15], ["Distortion_Pulse_Speed", 0.03, 0.05, 0.85, 0.15]],
        "pulse": [["Exposure", 0.9, 1.0, 1.5, 2.0, 0.6], ["Eye_Mask_Strain_Strength", 0.75, 2.0, 1.75, 1.5, 0.7]],
        "unit_of_conditions": "fraction of the bleed-out time left (BleedoutStart/EndCondition)"},
    "speed_pipeline": {
        "mode_slots": {"142 (+0x470)": "0x5291720 BH / 0x6DC1000 WD: walk speed", "144 (+0x480)": "0x5291A90 / 0x6DC1050: sprint scale",
                       "145 (+0x488)": "0x5291FD0 / 0x6DC10F0: tactical sprint scale", "147 (+0x498)": "0x5290900 / 0x6DC0E70: friction"},
        "lambda": "0x52820C0 runs the thunk 0x5288D80, which calls slot 142 of the mode",
        "formula": "stance speed = MaxSpeedModifier.ModifyValue(MaxSpeed) of the current stance, or MaxSpeed (+0x4C) when the stance has no "
                   "modifier; while a stance change is running it is blended: prev + (cur - prev) x alpha; only when Stand (enum 2) and "
                   "sprinting is it multiplied by the sprint scale (data +0x130) or the tactical sprint scale (+0x134), otherwise by a mode "
                   "float (+168, writer not found); the WD mode then multiplies by an attribute evaluator (+272 for speed, +304 sprint, "
                   "+320 tactical sprint, +352 friction)"},
}

LOOK = {"user_settings": ["UserSettings.Controls.Gamepad.LookAcceleration", ".Curve", ".MagnitudeThreshold", ".PitchWeight",
                          ".MaxMultiplier"], "curve_types": ["Standard", "Linear", "Aggressive"],
        "exe_strings": "0xB41F490 bGamepadLookAccelerationEnabled; 0xB41F4B0 LookAccelerationCurveType; 0xB420980 "
                       "EWDLookAccelerationCurveType; 0xB424678 UserSettings.Controls.Gamepad.LookAcceleration*"}

MODE_IMC = [["Falling", "IMC_Player_Falling", "IA_Player_DeployParachute", "SpaceBar / Gamepad_FaceButton_Bottom"],
            ["Ladder", "IMC_LadderClimbing", "IA_Player_SlideDownLadder_Toggle", "LeftShift / Gamepad_LeftThumbstick"],
            ["Ladder", "IMC_LadderClimbing", "IA_Player_JumpOffLadder", "SpaceBar / Gamepad_FaceButton_Bottom"],
            ["Swimming", "IMC_Player_Swimming", "IA_Player_FastSwim_Toggle", "LeftShift / Gamepad_LeftThumbstick"],
            ["Body dragging", "IMC_Player_BodyDrag", "IA_Player_BodyDrag", "G / Gamepad_RightShoulder"],
            ["No clip", "IMC_Player_NoClipping", "IA_Player_NoClipDown / NoClipUp / NoClipSuperSpeed", "LeftControl / SpaceBar / LeftShift"]]

ACTION_RESPONSE = ["None", "Block", "BlockingStates", "Interrupt", "InterruptAndBuffer", "InterruptOnComplete", "Reactivate", "Buffer",
                   "BlockCategories", "InterruptCategories", "InterruptBuffered", "RequiredStates"]


def build():
    return {"meta": {"source": "docs/evidence/round40-medical-movement.md; written by _tools/round40_medical_movement.py"},
            "armor": armor(), "ghillie_set_effect": ge_ghillie(), "native_and_blueprint": NATIVE, "gamepad_look_acceleration": LOOK,
            "mode_input_contexts": MODE_IMC, "action_response_types": ACTION_RESPONSE,
            "query_token_stream": {"format": "UE FGameplayTagQuery: [version 0][has root 1][root expr 5 = AllExprMatch][2 sub-expressions]"
                                              "[1 = AnyTagsMatch, 1 tag, index 0][3 = NoTagsMatch, 4 tags, indexes 1 2 3 4]",
                                   "example": "DA_CharacterModifierState_Critical: [0,1,5,2,1,1,0,3,4,1,2,3,4] = ALL(ANY(Critical), "
                                              "NONE(ActivePassenger, Driver, Gunner, PassivePassenger))",
                                   "expr_types": {"1": "AnyTagsMatch", "2": "AllTagsMatch", "3": "NoTagsMatch", "4": "AnyExprMatch",
                                                  "5": "AllExprMatch", "6": "NoExprMatch"}},
            "pose_search": {"databases": 20, "schemas": ["PSS_TPCharacter", "PSS_TPCharacter_Traversal", "PSS_TPCharacter_Turns"],
                            "animation_counts": {"PSD_Launcher_Loco": 27, "PSD_Pistol_Loco": 21, "PSD_Unarmed_Loco": 24,
                                                 "PSD_Rifle_Idle": 16, "PSD_Rifle_Walking_*": 8, "PSD_Rifle_Running_*": 8,
                                                 "PSD_Rifle_Standing_Turns": 6, "PSD_Rifle_Mantle_*": "3 to 4", "PSD_Rifle_Vault_*": 3,
                                                 "PSD_Rifle_Climb_On/Off": 1}}}


def n(v):
    return f"{v:g}" if isinstance(v, (int, float)) else str(v)


def armor_block(d):
    lines = ["| Piece | Context tag | Durability | Stage rows (reduction %, thickness, density) | Covered locations | Weight |",
             "|---|---|---:|---|---|---:|"]
    for r in d["armor"]:
        st = "; ".join(f"{n(a)} / {n(b)} / {n(c)}" for a, b, c in r["stages"]) or "none"
        wt = r["weight"] if r["weight"] != "default" else "1 (class default, omitted)"
        lines.append(f"| `{r['item']}` | `{r['context_tag']}` | {n(r['durability']) if r['durability'] else '-'} | {st} | "
                     f"{', '.join(dict.fromkeys(r['covered'])) or '-'} | {n(wt) if not isinstance(wt, str) else wt} |")
    return "\n".join(lines)


def swim_block(d):
    v = NATIVE["swimming_defaults"]["values"]
    return "\n".join(["| Swimming property | Native default | `DA_SwimmingMovement` |", "|---|---:|---|"] +
                     [f"| {k} | {n(x)} | {NATIVE['swimming_defaults']['overridden_in_DA_SwimmingMovement'].get(k, 'omitted (default)')} |"
                      for k, x in v.items()])


def imc_block(d):
    return "\n".join(["| Mover mode | Context asset (set in the mode's data asset) | Action | Keys |", "|---|---|---|---|"] +
                     [f"| {a} | `{b}` | `{c}` | {e} |" for a, b, c, e in d["mode_input_contexts"]])


def death_block(d):
    c = NATIVE["death_effect_close_eyes"]
    b = ", ".join(f"{k} {n(v)}" for k, v in c["blink"].items())
    lines = [f"Blink and twitch settings: {b}.", "",
             "| Parameter | Start value | End value | Bleed-out fraction where it starts | where it ends |", "|---|---:|---:|---:|---:|"]
    for p, s, e, bs, be in c["linear"]:
        lines.append(f"| `{p}` (linear) | {n(s) if s is not None else '-'} | {n(e) if e is not None else '-'} | "
                     f"{n(bs) if bs is not None else '-'} | {n(be) if be is not None else '-'} |")
    for p, lo, hi, dur, sc, bs in c["pulse"]:
        lines.append(f"| `{p}` (pulse {n(lo)} to {n(hi)}, {n(dur)} s, intensity factor {n(sc)}) | - | - | {n(bs)} | - |")
    return "\n".join(lines)


def crit_block(d):
    c = NATIVE["critical_state"]
    p = c["pawn_values"]
    cam = c["camera"]
    rows = [
        ("Where the Critical tag is set", "The vitality state object `UWDPlayerVitalityState_Critical` carries `VitalityTag`; its constructor `0x6E9B030` stores the global tag `State.Player.Vitality.Critical` (`qword_14D36B800`) at +0x28. The pawn lists three state classes (Alive, `B_WDPlayerVitalityState_Critical_C`, Dead); the character applies a state's tag when it enters the state (**Native**, constructor read; the enter call itself was not traced)"),
        ("Critical state defaults", f"`bIsPlayerAbleToGiveUp` {c['bIsPlayerAbleToGiveUp']}, `CallForHelpCooldownTime` {n(c['CallForHelpCooldownTime'])} s, `InputMappingContextPriority` {c['InputMappingContextPriority']} (**Native** constructor; the Blueprint only sets the call-for-help cue and the input context)"),
        ("Critical camera", f"`{cam['asset']}`, priority {cam['Priority']}, pitch lock {n(cam['PitchLockAngle'])} degrees. Default state: {cam['DefaultState']}. Dragged state: {cam['DraggedState']}. Character modifier `{cam['character_modifier']}` (look input ignored). Applies while: {cam['condition']} (**Data**)"),
        ("Pawn bleed-out values", f"`BaseBleedOutTime` {n(p['BaseBleedOutTime'])}, `MinBleedOutTime` {n(p['MinBleedOutTime'])}, `HoldOnBleedOutRate` {n(p['HoldOnBleedOutRate'])}, `GiveUpBleedOutRate` {n(p['GiveUpBleedOutRate'])}, `OutOfBoundsTimeLimit` {n(p['OutOfBoundsTimeLimit'])} (**Data**, pawn CDO; the WDCore pawn holds `CriticalReviveHoldThreshold` {n(p['core_pawn_CriticalReviveHoldThreshold'])}, its parent {n(p['CriticalReviveHoldThreshold'])})"),
    ]
    return "\n".join(["| Item | Value |", "|---|---|"] + [f"| {a} | {b} |" for a, b in rows])


def med_native_block(d):
    h = NATIVE["halligan"]
    e = NATIVE["enox_decay"]
    r = NATIVE["deathmatch_regen"]
    w = NATIVE["weight_default"]
    a = NATIVE["armor_durability_write"]
    rows = [
        ("Armour durability when hit", f"Each armour or helmet piece that takes a hit gets an armour event whose `Amount` comes from `DT_GlobalDamage_ArmorData` (ordinary bullet: 0.4 x the incoming amount). Events queue in `QueuedArmorDamageEvents`; the inventory tick `0x6B64EC0` runs `0x6B59000`, which does `Durability -= Amount`, updates the stage and fires `WDEvent_ArmorDamage` ({a['producer']}). The piece breaks when durability reaches 0 (**Native**). The stage tables above all give a flat reduction, so the number only drives the break and the durability bar"),
        ("Halligan durability", f"`ID_Crowbar` durability {n(h['durability'])}; opening a door (`B_Action_ForceOpenDoor`) or unlocking a vehicle (`B_Action_ForceUnlockVehicle`) each add `DurabilityCost` {n(h['cost_per_use'])}; the item is consumed when the result is 0 or less, so {h['uses']} uses (**Data** and **bytecode read**)"),
        ("Enox decay per tick", f"{e['per_tick']}, applied to Health through `0x52311D0`; with `DecayRate` {n(e['DecayRate'])} s and `DecayMagnitude` {n(e['DecayMagnitude'])} that is 5 health every 5 s until the pool ({'+0x17C'}) is empty (**Native**; the `movss xmm0,[rcx+0x170]` read at `0x6B16EE7` is the reader earlier searches missed)"),
        ("Armour weight default", f"{n(w['value'])} (constructor {w['ctor']}); {w['note']} (**Native**)"),
        ("Deathmatch regeneration tick", f"{r['component']} tick `{r['tick']}`: {r['gate']}. Amount {n(r['HealthToRegenerate'])} per tick (**Native**). {r['open']}, so \"5 per second\" stays derived"),
    ]
    return "\n".join(["| Item | Reading |", "|---|---|"] + [f"| {x} | {y} |" for x, y in rows])


def mov_formula_block(d):
    s = NATIVE["speed_pipeline"]
    rows = [("Walk speed (mode vtable slot 142)", s["formula"]),
            ("Where it is called", s["lambda"]),
            ("Other slots read", "; ".join(f"{k}: {v}" for k, v in s["mode_slots"].items())),
            ("Result for the numbers on this page", "Stand walk 428.8, sprint 608.9 and tactical sprint 664.6 stay as derived in 1b (Stand 0.8 x 536, x 1.42, x 1.55). Crouch (0.5) and Prone (0.15) have no sprint multiplier in this code path, so they cannot sprint at those scales (**Native**, static reading)"),
            ("Pawn defaults (CDO)", f"First-person FOV 106; `ProneHeldThreshold` {n(NATIVE['pawn']['ProneHeldThreshold'])}; `CloseAnimationDistance` {n(NATIVE['pawn']['CloseAnimationDistance'])}; interaction server box {NATIVE['pawn']['PlayerInteractionData_ServerBoxExtent']}; `WalkGunBobRotation` = `CRV_LandGunBob`. Tactical sprint FOV: {NATIVE['pawn']['TacSprintFOV']}. Kill FOV: {NATIVE['pawn']['PlayerKillFOV']}"),
            ("Gamepad look acceleration", "A user setting, not a map asset: `UserSettings.Controls.Gamepad.LookAcceleration` with `.Curve` (Standard, Linear or Aggressive = the three `CRV_LookAcceleration*` curves), `.MagnitudeThreshold`, `.PitchWeight`, `.MaxMultiplier` (exe strings). No exported asset references the curves"),
            ("Ping component", f"`UWDPingComponent` constructor {NATIVE['ping_component']['ctor']}: cooldown {n(NATIVE['ping_component']['Cooldown'])}, double-ping threshold {n(NATIVE['ping_component']['DoublePingThreshold'])}, trace angle {n(NATIVE['ping_component']['PingTraceAngle'])}, trace channel {NATIVE['ping_component']['TraceChannel']} (**Native**; units presumed)")]
    return "\n".join(["| Item | Reading |", "|---|---|"] + [f"| {a} | {b} |" for a, b in rows])


def action_block(d):
    return ", ".join(f"`{x}`" for x in d["action_response_types"])


SECTIONS = {
    "game-features/Wardogs_Medical_v1.md": {
        "anchor": None,  # append at end
        "text": """
## 11. Round 40 findings

Read from the cooked data and the restored exe; the reading path of every row is in the [round 40 evidence]({ev}). Generated by `_tools/round40_medical_movement.py`.

### 11a. Armour: durability, stages, weight and what happens on a hit

<!-- r40_med armor -->
<!-- /r40_med -->

Ghillie pieces have no durability fragment, no covered locations and no stage rows, so the armour operation returns 0 for them. The Ghillie set effect (`GE_Player_GhilliEffects`) needs both the body suit tag and the headwear tag and applies: ADS time x0.8, aim sway x1.15, lean and un-lean time x1.15, max speed x0.95, jump velocity x0.95. In `DT_GlobalDamage_ArmorData` the Ghillie target rows are -100% for bullet, explosive, cannon, impact, melee and the unconditional entry (armour event amount x0), and the ordinary armour and helmet rows carry -10000% and -1000% entries that require the Ghillie context tag; so a Ghillie piece takes no armour damage and gives no reduction (the evaluator behaviour for values below -100% was not traced).

### 11b. Native readings

<!-- r40_med native -->
<!-- /r40_med -->

### 11c. Critical state

<!-- r40_med critical -->
<!-- /r40_med -->
""",
    },
    "content/Wardogs_PlayerMovement_v1.md": {
        "anchor": "## 8. Open items",
        "text": """## 7b. Round 40: speed pipeline, swimming, input contexts, death effect

Read from the restored exe (static), the pawn Blueprint defaults and the cooked data. Generated by `_tools/round40_medical_movement.py`; reading paths in the [round 40 evidence]({ev}).

### Speed pipeline and pawn defaults

<!-- r40_med speed -->
<!-- /r40_med -->

### Swimming native defaults

`DA_SwimmingMovement` omits the speed cap, so the class default applies: **swim speed 250 cm/s, fast swim x2 (500) draining 20 stamina per second**. The asset overrides two values (water acceleration 4000, input deceleration 500).

<!-- r40_med swim -->
<!-- /r40_med -->

### Input contexts per mover mode

The shared keys in section 5 are resolved by which context is active: each mover mode asset carries its own `InputMappingContext`, added while the mode runs. Which one wins on a clash (context priority) is set natively and was not read.

<!-- r40_med imc -->
<!-- /r40_med -->

### Death-state effect (close eyes)

<!-- r40_med death -->
<!-- /r40_med -->

""",
    },
}

BLOCKS = {
    "game-features/Wardogs_Medical_v1.md": {"armor": armor_block, "native": med_native_block, "critical": crit_block},
    "content/Wardogs_PlayerMovement_v1.md": {"speed": mov_formula_block, "swim": swim_block, "imc": imc_block, "death": death_block},
}


def process(path, d, write):
    p = os.path.join(ROOT, path)
    text = open(p, encoding="utf8").read()
    orig = text
    sec = SECTIONS[path]
    if "<!-- r40_med " not in text:
        body = sec["text"].replace("{ev}", EV)
        if sec["anchor"] and sec["anchor"] in text:
            text = text.replace(sec["anchor"], body + sec["anchor"], 1)
        else:
            text = text.rstrip("\n") + "\n" + body
    for name, fn in BLOCKS[path].items():
        pat = re.compile(r"(<!-- r40_med " + name + r" -->\r?\n).*?(<!-- /r40_med -->)", re.S)
        text = pat.sub(lambda m: m.group(1) + fn(d) + "\n" + m.group(2), text)
    if text != orig and write:
        open(p, "w", encoding="utf8", newline="").write(text)
    return text != orig


def main():
    write = "--write" in sys.argv
    d = build()
    js = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
    old = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
    changed = [OUT] if js != old else []
    if write and js != old:
        open(OUT, "w", encoding="utf8", newline="").write(js)
    for path in SECTIONS:
        if process(path, d, write):
            changed.append(path)
    print(("wrote " if write else "would change ") + (", ".join(changed) if changed else "nothing (up to date)"))


if __name__ == "__main__":
    main()
