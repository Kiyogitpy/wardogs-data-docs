"""Tables for content/Wardogs_PlayerMovement_v1.md, rebuilt from data/ plus the native class defaults.

Reads the `GameMechanics/Player` folder (137 files) and the MoverTesting movement settings. Each table
sits between

    <!-- movement_tables MODE -->  ...  <!-- /movement_tables -->

on the page. Rerun after a data update (idempotent):

    python _tools/movement_tables.py --write       # refresh every block in place
    python _tools/movement_tables.py MODE          # print one block (counts, ground, stances, modes,
                                                   #   curves, ladder, audio, components, files)
    python _tools/movement_tables.py --check-native  # compare the NATIVE table with the constructor in the exe

An exported asset omits every property equal to the class default, so `MaxSpeed` is missing from
`DA_GroundMovement` because it equals the constructor value. The defaults in NATIVE were read from the
`UBHGroundMovementData` constructor in the restored exe: vtable store at RVA 0x528352D, the default stores
run from RVA 0x5283574 to 0x52837EF as `mov [r14+off], imm`; `r14` is the object, offsets match
`BHMover_classes.hpp`.
"""
import glob
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "content/Wardogs_PlayerMovement_v1.md"
PLAYER = "Wardogs/Content/GameMechanics/Player/"
SETTINGS = "Wardogs/Content/MoverTesting/Settings/"
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
BLOCK = re.compile(r"<!-- movement_tables (\w+) -->\r?\n.*?<!-- /movement_tables -->", re.S)
sys.stdout.reconfigure(encoding="utf-8")

# offset in UBHGroundMovementData -> (property, dword written by the constructor)
NATIVE = {
    0x48: ("Acceleration", 0x40E00000), 0x4C: ("MaxSpeed", 0x44060000), 0x50: ("MinSpeed", 0x42F00000),
    0x54: ("MaxStopSpeed", 0x42C80000), 0x58: ("Friction", 0x41000000), 0x5C: ("MaxStepHeight", 0x42200000),
    0x60: ("BlockedMovePct", 0x3F000000), 0x64: ("BackAccelerationScale", 0x3F800000),
    0x68: ("BackMaxSpeedScale", 0x3F800000), 0x6C: ("StrafeAccelerationScale", 0x3F800000),
    0x70: ("StrafeMaxSpeedScale", 0x3F800000), 0x74: ("ForwardStrafeScale", 0x3F59999A),
    0x78: ("BackwardStrafeScale", 0x3F59999A), 0x7C: ("InertiaMax", 0x42480000),
    0x90: ("JumpVelocity", 0x43FA0000), 0x94: ("MaxJumpStamina", 0x42C80000), 0x98: ("JumpStaminaCost", 0x41A00000),
    0x9C: ("JumpStaminaRegenPerSecond", 0x40A00000), 0xA0: ("JumpCooldown", 0x3F000000),
    0xC8: ("PostVaultFrictionScale", 0x3F99999A), 0xCC: ("PostVaultFrictionTime", 0x3F800000),
    0x128: ("SprintAccelerationScale", 0x3F800000), 0x12C: ("TacSprintAccelerationScale", 0x3F800000),
    0x130: ("SprintMaxSpeedScale", 0x3FB5C28F), 0x134: ("TacSprintMaxSpeedScale", 0x3FC66666),
    0x138: ("ForwardStrafeScaleSprinting", 0x3F2AC083), 0x13C: ("ForwardStrafeScaleTacSprinting", 0x3ECCCCCD),
    0x140: ("BlockSprintTime", 0x3F800000), 0x144: ("BlockTacSprintTime", 0x3F800000),
    0x148: ("TacSprintStaminaUsagePerSecond", 0x41A00000), 0x14C: ("MinStartTacSprintPercentage", 0x3E99999A),
    0x154: ("LeanLeftAngle", 0x41F00000), 0x158: ("LeanRightAngle", 0x420C0000), 0x15C: ("PivotOffset", 0x42700000),
    0x180: ("LeanTime", 0x3F000000), 0x184: ("UnleanTime", 0x3F000000), 0x188: ("SwapLeanTime", 0x3E4CCCCD),
    0x18C: ("UnleanInterpolationSpeedCollided", 0x41200000), 0x190: ("LeanTraceRadius", 0x40A00000),
    0x194: ("StanceCooldown", 0x3F000000), 0x198: ("MaxStanceStamina", 0x42C80000),
    0x19C: ("StanceStaminaRegenPerSecond", 0x41F00000), 0x1A0: ("StanceStaminaRegenDelay", 0x3F800000),
    0x1C4: ("ProneSweepDistance", 0x43020000),
}
CTOR_FIRST, CTOR_LAST = 0x5283574, 0x52837F0

GROUND_ROWS = [
    ("Movement", ["MaxSpeed", "MinSpeed", "MaxStopSpeed", "Acceleration", "Friction", "MaxStepHeight", "BlockedMovePct"]),
    ("Direction scales", ["BackMaxSpeedScale", "BackAccelerationScale", "StrafeMaxSpeedScale", "StrafeAccelerationScale",
                          "ForwardStrafeScale", "BackwardStrafeScale", "InertiaMax"]),
    ("Sprint", ["SprintMaxSpeedScale", "SprintAccelerationScale", "TacSprintMaxSpeedScale", "TacSprintAccelerationScale",
                "ForwardStrafeScaleSprinting", "ForwardStrafeScaleTacSprinting", "BlockSprintTime", "BlockTacSprintTime",
                "TacSprintStaminaUsagePerSecond", "MinStartTacSprintPercentage"]),
    ("Jump", ["JumpVelocity", "MaxJumpStamina", "JumpStaminaCost", "JumpStaminaRegenPerSecond", "JumpCooldown",
              "PostVaultFrictionScale", "PostVaultFrictionTime"]),
    ("Lean", ["LeanLeftAngle", "LeanRightAngle", "PivotOffset", "LeanTime", "UnleanTime", "SwapLeanTime",
              "UnleanInterpolationSpeedCollided", "LeanTraceRadius"]),
    ("Stance stamina", ["StanceCooldown", "MaxStanceStamina", "StanceStaminaRegenPerSecond", "StanceStaminaRegenDelay",
                        "ProneSweepDistance"]),
]


# --- helpers ------------------------------------------------------------------------------------

def exports(rel):
    with open(os.path.join(ROOT, "data", rel), encoding="utf-8") as f:
        return [json.loads(part) for part in EXPORT.split(f.read())[1:]]


def link(rel, label=None):
    return f"`{label or os.path.basename(rel)[:-5]}`"


def n(x, nd=4):
    x = float(x)
    if abs(x) < 1e-5:
        x = 0.0
    if x == int(x):
        return f"{int(x):,}"
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s


def f32(dword):
    return struct.unpack("<f", struct.pack("<I", dword))[0]


def native_value(prop):
    for _off, (name, dw) in NATIVE.items():
        if name == prop:
            return round(f32(dw), 4)
    return None


def asset(rel, typ):
    return next(e for e in exports(rel) if e["Type"] == typ)["Properties"]


def keys_of(curve):
    return [(k["Time"], k["Value"]) for k in curve.get("Keys", [])]


def ktxt(ks):
    return "; ".join(f"{n(t, 3)} → {n(v, 3)}" for t, v in ks)


def curve_channels(props):
    """Channels of a float or vector curve as {index: keys}."""
    if "FloatCurve" in props:
        return {0: keys_of(props["FloatCurve"])}
    out = {}
    for name, v in props.items():
        m = re.fullmatch(r"FloatCurves(?:\[(\d+)\])?", name)
        if m:
            out[int(m.group(1) or 0)] = keys_of(v)
    return out


# --- blocks -------------------------------------------------------------------------------------

def player_files():
    base = os.path.join(ROOT, "data", PLAYER)
    return sorted(os.path.relpath(p, os.path.join(ROOT, "data")).replace("\\", "/")
                  for p in glob.glob(os.path.join(base, "**", "*.json"), recursive=True))


def ground_data():
    return {nm: asset(SETTINGS + f"{nm}.json", "BHGroundMovementData") for nm in ("DA_GroundMovement", "DA_BodyDragging_GroundMovement")}


def b_ground():
    g = ground_data()
    a, b = g["DA_GroundMovement"], g["DA_BodyDragging_GroundMovement"]
    rows = ["| Group | Property | Class default (Native) | `DA_GroundMovement` (Data) | `DA_BodyDragging_GroundMovement` (Data) | Value in use |",
            "|---|---|---|---|---|---|"]
    omitted = 0
    for grp, props in GROUND_ROWS:
        for i, p in enumerate(props):
            d = native_value(p)
            va, vb = a.get(p), b.get(p)
            use_a = va if va is not None else d
            use_b = vb if vb is not None else d
            if va is None:
                omitted += 1
            use = n(use_a) if use_a == use_b else f"{n(use_a)} / {n(use_b)}"
            rows.append(f"| {grp if i == 0 else ''} | {p} | {n(d)} | {n(va) if va is not None else 'omitted'} | "
                        f"{n(vb) if vb is not None else 'omitted'} | **{use}** |")
    rows.append("")
    rows.append(f"{len(NATIVE)} defaults decoded from the constructor; {omitted} of the listed rows are omitted from `DA_GroundMovement`, so the class default applies. "
                "The last column shows ground movement first, body dragging second when they differ.")
    return "\n".join(rows)


def stance_speeds():
    g = ground_data()["DA_GroundMovement"]
    rows = []
    mods = {e["Name"]: e["Properties"] for e in exports(SETTINGS + "DA_GroundMovement.json") if e["Type"] == "BHFloatModifier_Operation"}
    for s in g["StanceSettings"]:
        v = s["Value"]
        r = {"stance": s["Key"].split("::")[-1]}
        for k, x in v.items():
            if isinstance(x, dict) and "ObjectName" in x:
                m = mods[x["ObjectName"].split(":")[-1].rstrip("'")]
                r[k] = (m.get("Operation", "Set").split("::")[-1], m["Magnitude"])
            elif x is not None:
                r[k] = x
        rows.append(r)
    return rows


def b_stances():
    g = ground_data()["DA_GroundMovement"]
    base = g.get("MaxSpeed", native_value("MaxSpeed"))
    spr = g.get("SprintMaxSpeedScale", native_value("SprintMaxSpeedScale"))
    tac = g.get("TacSprintMaxSpeedScale", native_value("TacSprintMaxSpeedScale"))
    out = ["| Stance | Capsule half-height / radius | Eye height | Stance stamina cost | Acceleration | MaxSpeed modifier | Walk speed (derived) | Sprint (derived) | Tac sprint (derived) | Max walkable slope |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in stance_speeds():
        op, mag = r["MaxSpeedModifier"]
        walk = base * mag if op == "Multiply" else mag
        acc_op, acc = r["AccelerationModifier"]
        slope = r.get("MaxWalkableSlopeAngleModifier")
        out.append(f"| {r['stance']} | {n(r['CapsuleHalfHeight'])} / {n(r['CapsuleRadius'])} | {n(r['EyeHeight'])} | "
                   f"{n(r['StanceStaminaCost'])} | {acc_op} {n(acc)} | {op} {n(mag)} | **{n(walk, 1)}** | "
                   f"{n(walk * spr, 1) if r['stance'] == 'Stand' else '-'} | {n(walk * tac, 1) if r['stance'] == 'Stand' else '-'} | "
                   f"{n(slope[1]) + ' deg' if slope else 'not set'} |")
    out.append("")
    out.append(f"Walk speed = MaxSpeed {n(base)} (class default) x the stance multiplier. Sprint and tac sprint multiply that by "
               f"SprintMaxSpeedScale {n(spr)} and TacSprintMaxSpeedScale {n(tac)} (class defaults). "
               "Sprint columns are given for Stand only; whether Crouch or Prone can sprint is not traced. "
               "`DA_BodyDragging_GroundMovement` has the same stance table except Crouch, which sets a 45 degree walkable slope.")
    return "\n".join(out)


def b_modes():
    g = ground_data()["DA_GroundMovement"]
    fall = asset(SETTINGS + "DA_FallingMovement.json", "WDFallingData")
    lad = asset(SETTINGS + "DA_LadderClimbingMovement.json", "BHLadderClimbingData")
    swim = asset(SETTINGS + "DA_SwimmingMovement.json", "BHMoverSwimmingDataAsset")
    slow = {k.split("::")[-1]: v for k, v in ((e["Key"], e["Value"]) for e in g["SlowWalkSpeedSettings"])}
    base = g.get("MaxSpeed", native_value("MaxSpeed"))
    rows = ["| Mode | Number | Value | Source |", "|---|---|---|---|"]

    def add(mode, num, val, src):
        rows.append(f"| {mode} | {num} | {val} | {src} |")
    add("Ground, standing", "MaxSpeed (cm/s)", n(base), "Native default; stance multiplier in the stance table")
    add("Ground", "Slow walk scale (Slow / Moderate / Fast)", " / ".join(n(slow[k]) for k in ("Slow", "Moderate", "Fast")), "Data: `SlowWalkSpeedSettings`; what it multiplies is not traced")
    add("Ground", "Jump velocity (cm/s)", n(g["JumpVelocity"]), "Data")
    add("Falling", "Acceleration / MaxSpeed / MaxStopSpeed", f"{n(fall['Acceleration'])} / {n(fall['MaxSpeed'])} / {n(fall['MaxStopSpeed'])}", "Data: `DA_FallingMovement`")
    add("Falling", "AirFriction / AirControlPercentage", f"{n(fall['AirFriction'])} / {n(fall['AirControlPercentage'])}", "Data")
    add("Falling", "Terminal speed, vertical / horizontal", f"{n(fall['VerticalTerminalSpeed'])} / {n(fall['HorizontalTerminalSpeed'])}", "Data")
    for k in sorted(lad):
        if "Speed" in k or "Acceleration" in k:
            add("Ladder", k, n(lad[k]) if isinstance(lad[k], (int, float)) else str(lad[k]), "Data: `DA_LadderClimbingMovement`")
    add("Swimming", "WaterAcceleration / InputDeceleration", f"{n(swim['WaterAcceleration'])} / {n(swim['InputDeceleration'])}", "Data: `DA_SwimmingMovement`; no swim speed cap is exported")
    return "\n".join(rows)


CURVE_USE = {
    "CRV_DamageIndicator_IntensityResponse": "Damage-indicator intensity (UI response); time 0 to 1",
    "CRV_ExitVehiclePunishment_Damage": "Damage on leaving a vehicle; input unit not exported (the 40 to 75 range suggests a speed in m/s, not traced)",
    "CRV_LandingPunishment_Damage": "Fall damage by impact speed (input unit not exported, cm/s presumed); `DA_FallingMovement.DamageLookup`",
    "CRV_ParachutePunishment_Damage": "Landing damage under parachute by impact speed (unit as above); referenced by the parachute settings",
    "CRV_SlopeGroundSpeedContribution": "Ground speed scale by slope; used by `DA_GroundMovement.SlopeMovementContributionCurve`",
    "CRV_LookAcceleration": "Look-input acceleration ramp (default)",
    "CRV_LookAcceleration_Aggressive": "Look-input acceleration ramp, faster",
    "CRV_LookAcceleration_Linear": "Look-input acceleration ramp, linear",
    "CRV_LandGunBob": "Vector curve; only the Z channel has keys: weapon dip after landing",
}


def b_curves():
    rows = ["| Curve | Type | Keys (time → value) | Reading |", "|---|---|---|---|"]
    for rel in player_files():
        if "/Curves/" not in rel or "MovementFeatures" in rel or "ResponseCurves" in rel:
            continue
        e = exports(rel)[0]
        nm = e["Name"]
        ch = curve_channels(e["Properties"])
        ks = " / ".join(f"Z: {ktxt(v)}" if (e["Type"] == "CurveVector" and i == 2) else ktxt(v) for i, v in sorted(ch.items()) if v)
        rows.append(f"| {link(rel)} | {e['Type']} | {ks} | {CURVE_USE.get(nm, '')} |")
    rows.append("")
    rows.append("Interpolation: damage and slope curves are linear between keys; look-acceleration and gun-bob curves use cubic tangents "
                "(the file `InterpMode` per key). Landing damage: 0 at impact speed 670, 100 at 875, 200 at 1080; the parachute curve reaches 100 at 1700.")
    return "\n".join(rows)


def b_response():
    rows = ["| Curve | Keys (input → output) |", "|---|---|"]
    for rel in player_files():
        if "ResponseCurves" in rel:
            e = exports(rel)[0]
            rows.append(f"| {link(rel)} | {ktxt(curve_channels(e['Properties'])[0])} |")
    return "\n".join(rows)


def b_ladder():
    rows = ["| Curve | Channel | Keys | Time range | Value range |", "|---|---|---|---|---|"]
    for rel in player_files():
        if "MovementFeatures" in rel:
            e = exports(rel)[0]
            for i, ks in sorted(curve_channels(e["Properties"]).items()):
                if ks:
                    ts, vs = [k[0] for k in ks], [k[1] for k in ks]
                    rows.append(f"| {link(rel)} | {'XYZ'[i]} | {len(ks)} | {n(min(ts), 3)} to {n(max(ts), 3)} | {n(min(vs), 3)} to {n(max(vs), 3)} |")
                else:
                    rows.append(f"| {link(rel)} | {'XYZ'[i]} | 0 | - | - |")
    return "\n".join(rows)


def b_audio():
    rel = PLAYER + "PlayerCharacter/Audio/DA_DefaultPlayerMovementAudioConfiguration.json"
    p = exports(rel)[0]["Properties"]
    out = ["**Footstep trigger distance** (cm of travel per step cue; `TriggerDistance`)", "",
           "| Stance or mode | State | Distance | Cue |", "|---|---|---|---|"]
    for s in p["Stances"]:
        st = s["Key"]["TagName"].split(".")[-1]
        d = s["Value"]["DefaultState"]
        out.append(f"| {st} | default | {n(d['TriggerDistance'])} | `{d['EffectGameplayCue']['TagName']}` |")
        for a in s["Value"].get("AdditionalStates", []):
            v = a["Value"]
            out.append(f"| {st} | {a['Key']['TagName'].split('.')[-1]} | {n(v['TriggerDistance'])} | `{v['EffectGameplayCue']['TagName']}` |")
    for m in p["MovementModeEffects"]:
        d = m["Value"]["Default"]
        if d["TriggerDistance"]:
            out.append(f"| {m['Key']['TagName'].split('.')[-1]} (mode) | default | {n(d['TriggerDistance'])} | `{d['EffectGameplayCue']['TagName']}` |")
    out += ["", f"Jump cue `{p['JumpGameplayCueTag']['TagName']}`. Landing cues: " +
            "; ".join(f"`{x['Key']['TagName']}` → `{x['Value']['GameplayCueTag']['TagName']}`" for x in p["LandingGameplayCueTags"]) +
            f". Movement modes with an effect entry: {len(p['MovementModeEffects'])}; mode variants are not expanded here. "
            "Stance transition cues: " + ", ".join(f"`{v['TagName'].split('.')[-1]}`" for v in p["StanceTransitionEffects"].values()) + "."]
    return "\n".join(out)


def b_components():
    rel = PLAYER + "PlayerCharacter/DA_PlayerCharacterComponents.json"
    es = exports(rel)
    top = next(e for e in es if e["Type"] == "BHPerspectiveData")["Properties"]["Templates"]
    byname = {e["Name"]: e for e in es}
    rows = ["| Template key | Component | Anim class | Mesh | Relative location (X, Y, Z) | Other |", "|---|---|---|---|---|---|"]
    for t in top:
        comp = t["Value"]["ObjectName"]
        cls, nm = comp.split("'")[0], comp.split(":")[-1].rstrip("'")
        p = byname.get(nm, {}).get("Properties", {})
        short = lambda o: o["ObjectName"].split("'")[1] if o else "-"
        loc = p.get("RelativeLocation")
        other = []
        if "FieldOfView" in p:
            other.append(f"FOV {n(p['FieldOfView'])}")
        if p.get("BHFovShadowMode"):
            other.append(p["BHFovShadowMode"].split("::")[-1])
        rows.append(f"| {t['Key']} | {cls} | {short(p.get('AnimClass'))} | {short(p.get('SkeletalMesh'))} | "
                    f"{', '.join(n(loc[k], 2) for k in 'XYZ') if loc else '-'} | {', '.join(other) or '-'} |")
    return "\n".join(rows)


def file_summary(rel):
    es = exports(rel)
    e = es[0]
    t, p = e["Type"], e.get("Properties", {})
    if t == "BHInputAction":
        vt = p.get("ValueType", "Boolean (omitted)").split("::")[-1]
        trig = ", ".join(sorted({x["Type"].replace("InputTrigger", "") for x in es[1:]})) or "none"
        return t, f"`{p['InputTag']['TagName']}`; {vt}; triggers {trig}"
    if t == "InputMappingContext" or any(x["Type"] == "InputMappingContext" for x in es):
        m = next(x for x in es if x["Type"] == "InputMappingContext")
        maps = m["Properties"].get("DefaultKeyMappings", {}).get("Mappings", [])
        acts = sorted({x["Action"]["ObjectName"].split("'")[1] for x in maps if x.get("Action")})
        return "InputMappingContext", f"{len(maps)} default mappings, {len(acts)} actions"
    if t == "PlayerMappableInputConfig":
        return t, f"{len(p['Contexts'])} contexts"
    if t in ("CurveFloat", "CurveVector"):
        ch = curve_channels(p)
        return t, "keys " + "/".join(str(len(v)) for _i, v in sorted(ch.items()))
    if t == "WDCharacterMovementEffectsComponentConfigurationDataAsset":
        return t, "footstep, jump, landing and stance cues (see audio section)"
    if t == "BHPerspectiveData":
        return t, f"{len(p['Templates'])} component templates"
    return t, ""


def b_files():
    groups = {}
    for rel in player_files():
        sub = rel[len(PLAYER) + len("PlayerCharacter/"):]
        fam = sub.split("/")[0] if "/" in sub else "(root)"
        if fam == "Inputs" and sub.count("/") > 1:
            fam = "Inputs/" + sub.split("/")[1]
        groups.setdefault(fam, []).append(rel)
    out = []
    for fam in sorted(groups):
        rels = groups[fam]
        out += [f"**{fam}** ({len(rels)} files)", "", "| File | Type | Content |", "|---|---|---|"]
        for rel in rels:
            t, s = file_summary(rel)
            out.append(f"| {link(rel)} | {t} | {s} |")
        out.append("")
    return "\n".join(out).rstrip()


def b_counts():
    files = player_files()
    fam = {}
    for rel in files:
        k = rel[len(PLAYER) + len("PlayerCharacter/"):].split("/")[0]
        fam[k] = fam.get(k, 0) + 1
    return (f"{len(files)} files under `GameMechanics/Player`: " +
            ", ".join(f"{k if k.endswith('.json') is False else 'root file'} {v}" for k, v in sorted(fam.items())) + ".")


BLOCKS = {"counts": b_counts, "ground": b_ground, "stances": b_stances, "modes": b_modes, "curves": b_curves,
          "response": b_response, "ladder": b_ladder, "audio": b_audio, "components": b_components, "files": b_files}


# --- native check -------------------------------------------------------------------------------

def check_native():
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_OP_IMM
    exe = r"E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
    pe = pefile.PE(exe, fast_load=True)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    start = 0x5283501
    code = pe.__data__[pe.get_offset_from_rva(start):][:CTOR_LAST - start + 16]
    found = {}
    for i in md.disasm(code, start):
        if i.mnemonic == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_MEM and i.operands[1].type == X86_OP_IMM \
                and i.operands[0].size in (4, 8) and i.operands[0].mem.base != 0 and CTOR_FIRST <= i.address <= CTOR_LAST \
                and i.reg_name(i.operands[0].mem.base) == "r14":
            found[i.operands[0].mem.disp] = i.operands[1].imm & 0xFFFFFFFF  # qword stores: low dword
    bad = [(hex(o), p, hex(d), hex(found.get(o, 0))) for o, (p, d) in NATIVE.items() if found.get(o) != d]
    print(f"{len(NATIVE)} defaults checked, {len(bad)} mismatches")
    for b in bad:
        print("  mismatch", *b)
    return 1 if bad else 0


# --- write --------------------------------------------------------------------------------------

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--check-native":
        sys.exit(check_native())
    if arg == "--write":
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        count = [0]

        def sub(m):
            count[0] += 1
            return f"<!-- movement_tables {m.group(1)} -->\n{BLOCKS[m.group(1)]()}\n<!-- /movement_tables -->"
        new = BLOCK.sub(sub, text)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        print(f"{count[0]} blocks refreshed in {PAGE}")
        return
    if arg in BLOCKS:
        print(BLOCKS[arg]())
        return
    print(__doc__)


if __name__ == "__main__":
    main()
