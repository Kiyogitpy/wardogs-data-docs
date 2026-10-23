"""Per-weapon spread, recoil, camera-kick, sway and movement-accuracy table, rebuilt from data/.

Writes content/Wardogs_WeaponSpreadRecoilData_v1.md (everything between the generated markers) and
assets/data/weapon-spread-recoil.json (row-level, curve keys included).

    python -I _tools/spread_recoil_tables.py          # print the doc body
    python -I _tools/spread_recoil_tables.py --write  # refresh the doc and the JSON

Sources, all under data/:
  * every WDWeaponStatsData asset (DA_*_Stats), exported by CUE4Parse; an exported asset omits every
    property that still has its class-default value;
  * the WDItemExtensionData_RangedWeapon object of the weapon's item (SpreadValues, stance recoil effects,
    default attributes, ADS transition, trace radius, fire-animation blend curve);
  * the curve table Content/Items/Weapons/Curves/CT_Weapon_Spread;
  * sight attachments (WDInventoryFragment_Attachment SightsData: sway-distance and stabilisation overrides).

Native defaults. The omitted fields take their value from the FWDWeaponStats constructor (RVA 0x699E6C0
in the reference image, the same method as _tools/native_defaults_check.py and weapon_stats_defaults.py).
The script disassembles it with capstone, applies every store to a byte map, follows the three helper calls
(memset 0x98F8026, float-curve ctor 0x3DFB270, vector-curve ctor 0x699DD90), and reads each omitted field at
its offset. Field names and offsets come from sdk/raw/WDGame_structs.hpp. When the exe or the disassembler
is missing, the defaults saved in the JSON by the last run are used.
"""
import glob
import hashlib
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = "content/Wardogs_WeaponSpreadRecoilData_v1.md"
JSON_OUT = "assets/data/weapon-spread-recoil.json"
EXE = r"E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
CTOR = 0x699E6C0
MEMSET, FCURVE_CTOR, VCURVE_CTOR = 0x98F8026, 0x3DFB270, 0x699DD90
STRUCTS = os.path.join(ROOT, "sdk", "raw", "WDGame_structs.hpp")
BEGIN, END = "<!-- spread_recoil_tables -->", "<!-- /spread_recoil_tables -->"
BLOB = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
NON_INFANTRY = re.compile(r"Vehicles|VehicleWeaponry|Stationary|Gunsmith|BarrelTest|BuildTool|Fists")

ENUMS = {
    "EWDWeaponAccuracyType": {0: "MinutesOfAngle", 1: "Milliradians"},
    "EWDWeaponFOVShiftingType": {0: "Constant", 1: "Curve", 2: "None"},
    "EWDFiringAnimationOffsetType": {0: "None", 1: "Procedural", 2: "FollowRecoilPattern"},
}


# --------------------------------------------------------------------------- struct layout from the SDK
def parse_structs():
    text = open(STRUCTS, encoding="utf-8", errors="replace").read()
    out = {}
    for m in re.finditer(r"\nstruct (F\w+) final\b.*?\n};", text, re.S):
        fields = []
        for line in m.group(0).split("\n"):
            f = re.match(r"\s+(\S.*?)\s+(\w+);\s*//\s*0x([0-9A-Fa-f]+)\(0x([0-9A-Fa-f]+)\)", line)
            if f and not f.group(2).startswith("Pad_"):
                fields.append((int(f.group(3), 16), int(f.group(4), 16), f.group(1).strip(), f.group(2)))
        out[m.group(1)] = fields
    return out


ALIAS = {  # SDK dump name -> key the cooked asset uses (the stabilisation-sway vector curves, +0x1F0 and +0x388)
    "_aaacclfeejhodkalcagid": "WeaponTranslationStabilizationSway",
    "_aaabpoakjgapligblioee": "WeaponRotationStabilizationSway",
}


def leaves(structs, name="FWDWeaponStats", base=0, prefix=""):
    """Flatten a struct into (path, absolute offset, kind) leaves. Kinds: f32 f64 u8 i32 enum:X curve vcurve
    vec2 interval array."""
    for off, size, typ, fname in structs[name]:
        path = prefix + ALIAS.get(fname, fname)
        t = typ.replace("struct ", "").strip()
        if t == "float":
            yield path, base + off, "f32"
        elif t == "bool":
            yield path, base + off, "bool"
        elif t == "uint8":
            yield path, base + off, "u8"
        elif t == "int32":
            yield path, base + off, "i32"
        elif t in ENUMS or t in ("EWDWeaponFOVShiftingType", "EWDFiringAnimationOffsetType", "EWDWeaponAccuracyType"):
            yield path, base + off, "enum:" + t
        elif t == "FRuntimeFloatCurve":
            yield path, base + off, "curve"
        elif t == "FRuntimeVectorCurve":
            yield path, base + off, "vcurve"
        elif t == "FVector2D":
            yield path, base + off, "vec2"
        elif t == "FFloatInterval":
            yield path, base + off, "interval"
        elif t.startswith("TArray"):
            yield path, base + off, "array"
        elif t in structs and t not in ("FWDWeaponAIData",):
            yield from leaves(structs, t, base + off, path + ".")


# --------------------------------------------------------------------------- native constructor simulation
def sim_ctor():
    """Return (bytes map offset -> int, set of curve offsets) from the FWDWeaponStats constructor, or None."""
    if not os.path.exists(EXE):
        return None
    try:
        import pefile
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
    except ImportError:
        return None
    pe = pefile.PE(EXE, fast_load=True)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def rd(rva, n):
        return pe.__data__[pe.get_offset_from_rva(rva):][:n]

    def canon(i, reg):
        n = i.reg_name(reg)
        for pat, c in ((r"^(rax|eax|ax|al)$", "a"), (r"^(rcx|ecx|cx|cl)$", "c"), (r"^(rdx|edx|dx|dl)$", "d"),
                       (r"^(rbx|ebx|bx|bl)$", "b"), (r"^(rsi|esi|si|sil)$", "si"), (r"^(rdi|edi|di|dil)$", "di"),
                       (r"^(r8|r8d|r8w|r8b)$", "r8"), (r"^(rsp|esp|sp|spl)$", "sp")):
            if re.match(pat, n):
                return c
        return n

    mem, curves, regs = {}, set(), {"c": ("p", 0)}
    xmm = {}
    for i in md.disasm(rd(CTOR, 0x1400), CTOR):
        m, ops = i.mnemonic, i.operands
        if m == "ret":
            break
        if m == "call":
            tgt = ops[0].imm if ops[0].type == X86_OP_IMM else None
            c, d, r8 = regs.get("c"), regs.get("d"), regs.get("r8")
            if tgt == MEMSET and c and c[0] == "p" and r8 and r8[0] == "v":
                for k in range(r8[1]):
                    mem[c[1] + k] = 0
            elif tgt in (FCURVE_CTOR, VCURVE_CTOR) and c and c[0] == "p":
                curves.add(c[1])
            for r in ("a", "c", "d", "r8"):
                regs.pop(r, None)
            xmm.clear()
            continue
        if len(ops) != 2:
            continue
        a, b = ops

        def val(op):
            if op.type == X86_OP_IMM:
                return ("v", op.imm & 0xFFFFFFFFFFFFFFFF)
            if op.type == X86_OP_REG:
                return regs.get(canon(i, op.reg))
            return None

        if m == "lea" and b.type == X86_OP_MEM and b.mem.base:
            base = regs.get(canon(i, b.mem.base))
            if base and base[0] == "p":
                regs[canon(i, a.reg)] = ("p", base[1] + b.mem.disp)
            else:
                regs.pop(canon(i, a.reg), None)
        elif m == "add" and a.type == X86_OP_REG and b.type == X86_OP_IMM:
            r = regs.get(canon(i, a.reg))
            if r and r[0] == "p":
                regs[canon(i, a.reg)] = ("p", r[1] + b.imm)
        elif m in ("xor", "xorps") and a.type == X86_OP_REG and b.type == X86_OP_REG and a.reg == b.reg:
            if m == "xorps":
                xmm[canon(i, a.reg)] = b"\0" * 16
            else:
                regs[canon(i, a.reg)] = ("v", 0)
        elif m in ("mov", "movabs") and a.type == X86_OP_REG:
            if b.type == X86_OP_MEM and b.mem.base == X86_REG_RIP:
                regs.pop(canon(i, a.reg), None)
            else:
                v = val(b)
                if v is not None:
                    regs[canon(i, a.reg)] = v
                else:
                    regs.pop(canon(i, a.reg), None)
        elif m in ("mov", "movabs") and a.type == X86_OP_MEM and a.mem.base:
            base = regs.get(canon(i, a.mem.base))
            v = val(b)
            if base and base[0] == "p" and v and v[0] == "v":
                for k in range(a.size):
                    mem[base[1] + a.mem.disp + k] = (v[1] >> (8 * k)) & 0xFF
        elif m == "movups" and a.type == X86_OP_REG and b.type == X86_OP_MEM and b.mem.base == X86_REG_RIP:
            xmm[canon(i, a.reg)] = rd(i.address + i.size + b.mem.disp, 16)
        elif m == "movups" and a.type == X86_OP_MEM and a.mem.base and b.type == X86_OP_REG:
            base = regs.get(canon(i, a.mem.base))
            data = xmm.get(canon(i, b.reg))
            if base and base[0] == "p" and data:
                for k in range(16):
                    mem[base[1] + a.mem.disp + k] = data[k]
    return mem, curves


def decode(kind, off, mem, curves):
    """Native default of one leaf: (value, ok)."""
    def raw(n):
        if not all(off + k in mem for k in range(n)):
            return None
        return int.from_bytes(bytes(mem[off + k] for k in range(n)), "little")

    def f32(o):
        return float(f"{struct.unpack('<f', struct.pack('<I', o))[0]:.7g}")

    def f64(o):
        return float(f"{struct.unpack('<d', struct.pack('<Q', o))[0]:.9g}")

    if kind in ("curve", "vcurve"):
        return ("empty curve (no keys)" if off in curves else None), off in curves
    if kind == "array":
        return [], raw(8) == 0
    if kind == "f32":
        r = raw(4)
        return (f32(r) if r is not None else None), r is not None
    if kind == "i32":
        r = raw(4)
        return ((r - (1 << 32) if r >> 31 else r) if r is not None else None), r is not None
    if kind == "bool":
        r = raw(1)
        return (bool(r) if r is not None else None), r is not None
    if kind == "u8":
        r = raw(1)
        return (r if r is not None else None), r is not None
    if kind.startswith("enum:"):
        r = raw(1)
        return (ENUMS[kind[5:]].get(r, r) if r is not None else None), r is not None
    if kind == "vec2":
        x, y = raw(8), None
        if x is None:
            return None, False
        off2 = off
        off = off + 8
        y = raw(8)
        off = off2
        return ({"X": f64(x), "Y": f64(y)} if y is not None else None), y is not None
    if kind == "interval":
        lo = raw(4)
        off += 4
        hi = raw(4)
        return ({"Min": f32(lo), "Max": f32(hi)} if lo is not None and hi is not None else None), lo is not None and hi is not None
    return None, False


# --------------------------------------------------------------------------- categories
CATS = [  # (category, path regex)
    ("Spread and accuracy", r"^(WeaponAccuracy\.|RandomDeviationDegree$|ShotgunData\.|bSpawnProjectileFromCameraWhenAds$)"),
    ("Recoil", r"^(RecoilPattern|PostPattern|FiringAnimationOffset|MinimumRandomFiring|MaximumRandomFiring|FocusData\.|"
               r"FocusEnergyReductionPerShot$|RecoilReductionWhenFocussing$|_aaabimbpohdlmnphjbidm$)"),
    ("Camera kick", r"^(ViewKick|RecoveryKickCurve$|FOVShift|AdsCameraCurve$|FovInterpSpeed$|IronSights)"),
    ("Movement accuracy", r"^(AimSwayData\.CurveData\.(Horizontal|Vertical)AimSwayMovementCurve$|"
                          r"AimSwayData\.PlayerSpeedStabilizationMultiplierCurve$|AimSwayData\.ADSStabilizationMovementSpeedRate|"
                          r"AimSwayData\.AdsStabilizationData\.AdsStabilize(CooldownRateMovingMultiplier|MovementProgressPenalty)$)"),
    ("Sway", r"^(AnimationSwayData\.|bAnimationSwayEnabled$|AimSwayData\.)"),
]


def category(path):
    for name, pat in CATS:
        if re.search(pat, path):
            return name
    return None


# --------------------------------------------------------------------------- data loading
def split_exports(text):
    for part in re.split(r"^--- export:.*---\s*$", text, flags=re.M):
        part = part.strip()
        if part:
            try:
                obj = json.loads(part)
            except ValueError:
                continue
            yield from (obj if isinstance(obj, list) else [obj])


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def get(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def keys_of(curve):
    return [{k: v for k, v in key.items()
             if k in ("Time", "Value", "InterpMode", "ArriveTangent", "LeaveTangent", "TangentMode")}
            for key in ((curve or {}).get("EditorCurveData") or {}).get("Keys", [])]


def vector_curve_keys(curve):
    """Keys of an external CurveVector asset (X, Y, Z), read from its own data file."""
    ext = (curve or {}).get("ExternalCurve") or {}
    m = re.match(r"/Game/(.+)\.\d+$", ext.get("ObjectPath", ""))
    if not m:
        return None
    path = os.path.join(ROOT, "data", "Wardogs", "Content", m.group(1) + ".json")
    if not os.path.exists(path):
        return None
    for o in split_exports(open(path, encoding="utf-8").read()):
        if o.get("Type") == "CurveVector":
            fc = o["Properties"].get("FloatCurves")
            fc = fc if isinstance(fc, list) else [fc]
            return {a: keys_of({"EditorCurveData": c}) for a, c in zip("XYZ", fc) if c}
    return None


def curve_ref(curve):
    ext = (curve or {}).get("ExternalCurve") or {}
    on = ext.get("ObjectName") or ""
    m = re.search(r"'([^']+)'", on)
    return m.group(1) if m else None


def load_all():
    stats, items, sights, ct = {}, {}, [], {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if not re.search(r"WDWeaponStatsData|WDItemExtensionData_RangedWeapon|SightsData|CurveTable", text):
            continue
        objs = list(split_exports(text))
        defattrs = max((o["Properties"]["DefaultAttributes"] for o in objs
                        if o.get("Type") == "WDItemExtensionData_GameplayEffects" and o.get("Properties", {}).get("DefaultAttributes")),
                       key=len, default=None)
        for o in objs:
            t = o.get("Type")
            if t == "WDWeaponStatsData":
                stats[o["Name"]] = (rel(p), o)
            elif t == "WDItemExtensionData_RangedWeapon":
                m = re.search(r"'(DA_\w+)'", (o["Properties"].get("WeaponStats") or {}).get("ObjectName", ""))
                if m:
                    props = dict(o["Properties"])
                    if defattrs and len(defattrs) > len(props.get("DefaultAttributes", [])):
                        props["DefaultAttributes"] = defattrs
                    items[m.group(1)] = (os.path.basename(p)[:-5], rel(p), props)
            elif t == "CurveTable" and o.get("Name") == "CT_Weapon_Spread":
                ct = o["Rows"]
            elif t == "WDInventoryFragment_Attachment":
                for s in (o["Properties"].get("AttachmentData") or {}).get("SightsData", []) or []:
                    v = s.get("Value", {})
                    if v.get("bOverrideSightSwayDistanceOffset") or v.get("bOverrideWeaponSwayStabilizationData") \
                            or v.get("bOverrideSightCameraOffset"):
                        sights.append((os.path.basename(p)[:-5], rel(p), s["Key"], v))
    return stats, items, sights, ct


# --------------------------------------------------------------------------- build
def build():
    structs = parse_structs()
    spec = [(p, off, kind) for p, off, kind in leaves(structs) if category(p)]
    spec.sort(key=lambda s: [c[0] for c in CATS].index(category(s[0])) * 100000 + s[1])
    sim = sim_ctor()
    prev = None
    jp = os.path.join(ROOT, JSON_OUT)
    if os.path.exists(jp):
        prev = json.load(open(jp, encoding="utf-8")).get("nativeDefaults")
    defaults = {}
    for path, off, kind in spec:
        if sim:
            val, ok = decode(kind, off, *sim)
            defaults[path] = {"offset": hex(off), "kind": kind, "default": val if ok else None, "resolved": ok}
        elif prev and path in prev:
            defaults[path] = prev[path]
        else:
            defaults[path] = {"offset": hex(off), "kind": kind, "default": None, "resolved": False}

    stats, items, sights, ct = load_all()
    weapons = []
    unmapped = set()
    for name, (path, o) in sorted(stats.items()):
        ws = o["Properties"].get("WeaponStats", {})
        tag = ((o["Properties"].get("WeaponId") or {}).get("TagName") or "").rsplit(".", 1)[-1]
        label = name[3:-6]
        cls = "Infantry" if not NON_INFANTRY.search(path) else (
            "Vehicle" if re.search(r"Vehicle", path) else "Stationary" if "Stationary" in path else "Other")
        w = {"asset": name, "label": label, "weaponId": tag, "path": path, "class": cls, "fields": {}, "curves": {}}
        for p_, off, kind in spec:
            raw = get(ws, p_)
            d = defaults[p_]
            if kind in ("curve", "vcurve"):
                node = get(ws, p_)
                if node is None:
                    w["curves"][p_] = {"source": "native default", "ref": None, "keys": []}
                else:
                    ext = node.get("ExternalCurve") if isinstance(node, dict) else None
                    if kind == "vcurve":
                        w["curves"][p_] = {"source": "data", "ref": curve_ref(node), "keys": vector_curve_keys(node) or []}
                    else:
                        w["curves"][p_] = {"source": "data", "ref": curve_ref(node), "keys": keys_of(node)}
            elif raw is not None:
                w["fields"][p_] = {"value": raw, "source": "data"}
            else:
                w["fields"][p_] = {"value": d["default"], "source": "native default" if d["resolved"] else "unresolved"}
        # unmapped keys: cooked keys of interest that the SDK layout does not know
        def walk(dd, pre=""):
            for k, v in dd.items():
                if isinstance(v, dict) and not (k.endswith("Curve") or k in ("ExternalCurve", "EditorCurveData")) \
                        and not any(re.search(pat, pre + k) for _, pat in CATS):
                    walk(v, pre + k + ".")
                elif category(pre + k) and (pre + k) not in {s[0] for s in spec}:
                    if isinstance(v, dict) and any(s[0].startswith(pre + k + ".") for s in spec):
                        continue
                    unmapped.add(pre + k)
        walk(ws)
        it = items.get(name)
        if it:
            _, ipath, ip = it
            w["item"] = {
                "id": it[0], "path": ipath,
                "spreadValues": {k["Key"].split("::")[-1]: {
                    "value": k["Value"].get("Value"),
                    "row": (k["Value"].get("Curve") or {}).get("RowName")} for k in ip.get("SpreadValues", [])},
                "stanceEffects": {k["Key"].split("::")[-1]: [
                    re.search(r"GE_\w+?(?=_C')", e["Effect"]["ObjectName"]).group(0) for e in k["Value"].get("Effects", [])]
                    for k in ip.get("StanceGameplayEffects", [])},
                "attributes": {a["Key"]["TagName"].replace("Attribute.Gameplay.Weapon.", ""): a["Value"]
                               for a in ip.get("DefaultAttributes", [])},
                "weaponTraceRadius": ip.get("WeaponTraceRadius"),
                "adsTransition": ip.get("AdsTransitionData"),
                "sightPositionOffset": ip.get("SightPositionOffset"),
                "ironSightCameraOffset": ip.get("IronSightCameraOffset"),
                "fireAnimBlendTimeCurve": keys_of(ip.get("FireAnimBlendTimeCurve")) if ip.get("FireAnimBlendTimeCurve") else None,
                "fireAnimBlendTargets": ip.get("FireAnimBlendTargets"),
                "bufferedFireAnimBlendTime": ip.get("BufferedFireAnimBlendTime"),
            }
        weapons.append(w)
    spread_rows = {r: [(k["Time"], k["Value"]) for k in v["Keys"]] for r, v in ct.items()}
    sight_rows = []
    for fname, p, key, v in sights:
        sight_rows.append({
            "item": fname, "path": p, "sight": key,
            "swayDistance": {"override": bool(v.get("bOverrideSightSwayDistanceOffset")),
                             "value": v.get("SightSwayDistanceOffset"),
                             "perWeapon": {e["Key"]["TagName"]: e["Value"] for e in v.get("SightSwayDistanceOffsetOverridePerWeapon", [])}},
            "stabilisation": {"override": bool(v.get("bOverrideWeaponSwayStabilizationData")),
                              "perArchetype": {e["Key"]["TagName"]: e["Value"] for e in v.get("SightStabilizationOverrideMultipliers", [])}},
            "cameraOffset": {"override": bool(v.get("bOverrideSightCameraOffset")),
                             "value": v.get("SightCameraOffsetOverride"),
                             "perWeapon": {e["Key"]["TagName"]: e["Value"] for e in v.get("SightCameraOffsetOverridePerWeapon", [])}},
        })
    return spec, defaults, weapons, spread_rows, sight_rows, unmapped, bool(sim)


# --------------------------------------------------------------------------- rendering
def num(x):
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:.6g}"
    return str(x)


def val_str(v):
    if isinstance(v, dict):
        return " … ".join(num(x) for x in v.values())
    if isinstance(v, list):
        return ", ".join(str(x).split("::")[-1] for x in v) if v else "none"
    if isinstance(v, str):
        return v.split("::")[-1]
    if v is None:
        return "?"
    return num(v)


def cell(w, path):
    f = w["fields"].get(path)
    if f is None:
        return "—"
    s = val_str(f["value"])
    return s + ("†" if f["source"] != "data" else "")


def triple(w, base):
    return " / ".join(cell(w, f"{base}.{k}Multiplier") for k in ("Stand", "Crouch", "Prone"))


def curve_sig(c):
    return json.dumps([(k["Time"], k["Value"], k["InterpMode"].split("_")[-1]) for k in c["keys"]]) \
        if isinstance(c["keys"], list) else str(c["keys"])


def fmt_keys(keys):
    if isinstance(keys, dict):
        return " / ".join(f"{a}: {fmt_keys(v)}" for a, v in keys.items())
    if not isinstance(keys, list):
        return str(keys)
    if not keys:
        return "no keys"
    tag = {"Linear": "L", "Cubic": "C", "Constant": "K"}
    out = []
    for k in keys:
        m = tag.get(k.get("InterpMode", "").split("_")[-1], "?")
        out.append(f"{num(k['Time'])}:{num(k['Value'])}{m}")
    return " ".join(out)


def link(w):
    return f"[`{w['label']}`]({BLOB}{w['path']})"


def table(head, rows, align=None):
    align = align or ["---"] * len(head)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "|".join(align) + "|"] + ["| " + " | ".join(r) + " |" for r in rows])


def render(spec, defaults, weapons, spread_rows, sight_rows, unmapped, native):
    out = []
    A = out.append
    n_inf = sum(1 for w in weapons if w["class"] == "Infantry")
    A(f"{len(weapons)} `WDWeaponStatsData` assets ({n_inf} infantry, {len(weapons) - n_inf} vehicle, stationary or test weapons), "
      f"{sum(1 for w in weapons if 'item' in w)} of them with a ranged-weapon item. `†` marks a value the asset omits, taken from the "
      f"`FWDWeaponStats` constructor. `—` means the object has no such field (items) or no item.")
    A("")
    # --- native defaults table
    A("### Native defaults used\n")
    rows = []
    for p, off, kind in spec:
        d = defaults[p]
        rows.append([f"`{p}`", category(p), f"`{d['offset']}`", kind.split(":")[-1], f"`{val_str(d['default'])}`" if d["resolved"] else "unresolved"])
    A(table(["Field", "Group", "Offset in `FWDWeaponStats`", "Type", "Native default"], rows))
    A("")

    def wrows(fn, only_class=None):
        return [fn(w) for w in weapons if only_class is None or w["class"] == only_class]

    # --- spread and accuracy
    A("## 1. Spread and accuracy\n")
    A("The aim cone itself is `WeaponAccuracy` (minutes of angle or milliradians) times the stance spread rows below times the "
      "`SpreadMultiplier` and `AccuracyMultiplier` attributes; how the code combines them is in the "
      "[weapon spread pipeline](../pipelines/Wardogs_WeaponSpread_v1.md). `RandomDeviationDegree` is the per-shot random cone used with the recoil "
      "pattern (see section 2). There is no field named bloom in the cooked weapon data; the in-game bloom is the spread rows.\n")
    A("### 1a. Stats-asset fields\n")
    sh = ["ShotgunData.ChokeFactor", "ShotgunData.bSeparateOuterConeHalfAngles", "ShotgunData.OuterConeHalfAngle",
          "ShotgunData.bSeparateRandomConeHalfAnglesRanges", "ShotgunData.RandomConeHalfAngleRange", "ShotgunData.InnerConeHalfAngleMultiplier"]
    cols = ["WeaponAccuracy.AccuracyType", "WeaponAccuracy.AccuracyValue", "RandomDeviationDegree", "bSpawnProjectileFromCameraWhenAds"] + sh
    A(table(["Weapon", "Class", "Accuracy type", "Accuracy value", "Random deviation (deg)", "Projectile from camera in ADS",
             "Choke", "Separate outer cone", "Outer cone half angle", "Separate random cone", "Random cone range", "Inner cone ×"],
            wrows(lambda w: [link(w), w["class"]] + [cell(w, c) for c in cols])))
    A("")
    A("### 1b. Stance spread (item `SpreadValues`)\n")
    A("Each stance names a `CT_Weapon_Spread` row and a scalar. Item attributes are the item's `DefaultAttributes` before attachments "
      "([final values with default attachments](Wardogs_WeaponAttributes_v1.md)).\n")
    rows = []
    for w in weapons:
        it = w.get("item")
        if not it:
            continue
        sv = it["spreadValues"]
        rows.append([link(w), f"`{it['id']}`"] + [f"`{sv[s]['row']}` ×{num(sv[s]['value'])}" if s in sv else "—" for s in ("Stand", "Crouch", "Prone")] +
                    [num(it["attributes"].get(a, "—")) for a in ("SpreadMultiplier", "AccuracyMultiplier")] + [num(it["weaponTraceRadius"]) if it["weaponTraceRadius"] is not None else "—"])
    A(table(["Weapon", "Item", "Stand", "Crouch", "Prone", "Spread ×", "Accuracy ×", "Trace radius"], rows))
    A("")
    A("### 1c. `CT_Weapon_Spread` rows\n")
    A(table(["Row", "Keys (time:value)"], [[f"`{r}`", " ".join(f"{num(t)}:{num(v)}" for t, v in k)] for r, k in sorted(spread_rows.items())]))
    A("")

    # --- recoil
    A("## 2. Recoil\n")
    A("The recoil pattern is the per-shot (yaw, pitch) kick list; after its last shot the random yaw and pitch ranges apply. How shots become "
      "view kick is in [Weapons §5a](Wardogs_Weapons_v2.md). The `_aaabimbpohdlmnphjbidm` column is the unnamed focus drain window (+0x98).\n")
    A("### 2a. Scalars\n")
    c2 = ["RecoilPatternPitchMax", "RecoilPatternYawMinMax", "PostPatternRandomYawRecoil", "PostPatternRandomPitchRecoil", "RecoilPatternResetTime",
          "FiringAnimationOffsetType", "MinimumRandomFiringAnimationOffset", "MaximumRandomFiringAnimationOffset", "FiringAnimationOffsetPatternMultiplier",
          "RecoilReductionWhenFocussing", "FocusEnergyReductionPerShot", "_aaabimbpohdlmnphjbidm", "FocusData.FocusEnergyUsageMultiplier",
          "FocusData.FocusEnergyRecoveryMultiplier", "FocusData.AdditionalFocusZoom"]
    A(table(["Weapon", "Pitch max", "Yaw min … max", "After pattern: yaw", "After pattern: pitch", "Reset (s)", "Anim offset type",
             "Anim offset min", "Anim offset max", "Anim offset pattern ×", "Focus recoil cut %", "Focus energy % / shot", "Focus window (s)",
             "Focus usage ×", "Focus recovery ×", "Focus extra zoom"],
            wrows(lambda w: [link(w)] + [cell(w, c) for c in c2])))
    A("")
    A("### 2b. Item recoil attributes and stance effects\n")
    rows = []
    for w in weapons:
        it = w.get("item")
        if not it:
            continue
        ge = it["stanceEffects"]
        rows.append([link(w), num(it["attributes"].get("VerticalRecoilMultiplier", "—")), num(it["attributes"].get("HorizontalRecoilMultiplier", "—"))] +
                    [", ".join(f"`{g}`" for g in ge.get(s, [])) or "—" for s in ("Stand", "Crouch", "Prone")])
    A(table(["Weapon", "Vertical recoil ×", "Horizontal recoil ×", "Stand effect", "Crouch effect", "Prone effect"], rows))
    A("")
    stance = {}
    for w in weapons:
        for s, gs in (w.get("item") or {}).get("stanceEffects", {}).items():
            for g in gs:
                stance[g] = None
    A("The stance effects multiply both recoil attributes (compound): Standing 1.0 for every archetype; Crouch 0.85 (AR, DMR, SMG, SR, Pistol, "
      "Shotgun) or 0.6 (LMG); Prone 0.7 (AR, DMR, SMG, SR, Pistol, Shotgun) or 0.35 vertical and 0.25 horizontal (LMG). Values are from "
      "[`weapon-loadouts.json`](../assets/data/weapon-loadouts.json).\n")
    A("### 2c. Recoil patterns, every shot\n")
    A("Each cell is `yaw,pitch` of that shot. Weapons without a pattern use only the after-pattern ranges.\n")
    rows = []
    for w in weapons:
        pat = w["fields"].get("RecoilPattern", {})
        if pat.get("source") != "data" or not pat["value"]:
            continue
        rows.append([link(w), str(len(pat["value"])), "; ".join(f"{num(p['X'])},{num(p['Y'])}" for p in pat["value"])])
    A(table(["Weapon", "Shots", "Pattern (yaw,pitch per shot)"], rows))
    A("")

    # --- curves helper
    curve_cats = {}
    for p, off, kind in spec:
        if kind in ("curve", "vcurve"):
            curve_cats.setdefault(category(p), []).append(p)
    cat_ids = {}

    def curve_ids(path):
        """Assign ids: external curve name when present, else a per-field numbered inline curve."""
        ids, sigs = {}, {}
        n = 0
        for w in weapons:
            c = w["curves"][path]
            if c["source"] != "data":
                ids[w["asset"]] = None
                continue
            sig = (c["ref"], curve_sig(c))
            if sig not in sigs:
                if c["ref"]:
                    sigs[sig] = c["ref"] if c["ref"] not in [s[0] for s in sigs] else f"{c['ref']} (variant {len(sigs)})"
                else:
                    n += 1
                    sigs[sig] = f"{path.split('.')[-1]}#{n}"
            ids[w["asset"]] = sigs[sig]
        return ids, sigs

    def curve_catalog(path):
        ids, sigs = curve_ids(path)
        users = {}
        for w in weapons:
            i = ids[w["asset"]]
            if i:
                users.setdefault(i, []).append(w["label"])
        rows = []
        seen = {}
        for w in weapons:
            c = w["curves"][path]
            i = ids[w["asset"]]
            if i and i not in seen:
                seen[i] = 1
                us = users[i]
                rows.append([f"`{i}`", fmt_keys(c["keys"]), f"{len(us)}", ", ".join(us) if len(us) <= 6 else ", ".join(us[:6]) + ", …"])
        return ids, rows

    def curve_section(path, title):
        ids, rows = curve_catalog(path)
        A(f"**`{path}`**\n")
        A(table(["Curve", "Keys (time:value, L linear, C cubic, K constant)", "Weapons", "Used by"], rows))
        A("")
        return ids

    # --- camera kick
    A("## 3. Camera kick\n")
    A("### 3a. Scalars\n")
    c3 = ["ViewKickMagnitudeMultiplier", "FOVShiftingType", "FOVShiftDeltaAmount", "FOVShiftDuration", "FovInterpSpeed", "IronSightsAimTime", "IronSightsFovMultiplier"]
    A(table(["Weapon", "View kick ×", "FOV shift type", "FOV shift delta", "FOV shift duration (s)", "FOV interp speed", "Iron-sights aim time (s)", "Iron-sights FOV ×"],
            wrows(lambda w: [link(w)] + [cell(w, c) for c in c3])))
    A("")
    A("### 3b. Curves per weapon\n")
    cc = curve_cats["Camera kick"]
    ids_by = {}
    for p in cc:
        ids_by[p] = curve_ids(p)[0]
    A(table(["Weapon"] + [f"`{p}`" for p in cc], wrows(lambda w: [link(w)] + [(f"`{ids_by[p][w['asset']]}`" if ids_by[p][w["asset"]] else "none†") for p in cc])))
    A("")
    A("### 3c. Curve keys\n")
    for p in cc:
        curve_section(p, "")
    A("### 3d. Item camera and animation fields\n")
    rows = []
    for w in weapons:
        it = w.get("item")
        if not it:
            continue
        ads = it["adsTransition"] or {}
        fb = it["fireAnimBlendTimeCurve"]
        rows.append([link(w), ", ".join(f"{k} {num(v)}" for k, v in ads.items()) or "—",
                     fmt_keys(fb) if fb else "—", num(it["fireAnimBlendTargets"]) if it["fireAnimBlendTargets"] is not None else "—",
                     num(it["bufferedFireAnimBlendTime"]) if it["bufferedFireAnimBlendTime"] is not None else "—",
                     val_str(it["sightPositionOffset"]) if it["sightPositionOffset"] else "—",
                     val_str(it["ironSightCameraOffset"]) if it["ironSightCameraOffset"] else "—"])
    A(table(["Weapon", "`AdsTransitionData`", "`FireAnimBlendTimeCurve`", "Blend targets", "Buffered blend time", "Sight position offset", "Iron-sight camera offset"], rows))
    A("")

    # --- sway
    A("## 4. Sway\n")
    A("### 4a. Aim sway scalars\n")
    sw1 = ["AimSwayData.bPersistentValues", "AimSwayData.TotalPatternDuration", "AimSwayData.StandOffsetMultiplier", "AimSwayData.CrouchOffsetMultiplier",
           "AimSwayData.ProneOffsetMultiplier", "AimSwayData.FocusOffsetMultiplier", "AimSwayData.NoFocusEnergySpeedMultiplier",
           "AimSwayData.CorrectionOffsetTime", "AimSwayData.PlayerCameraOffsetMultiplier", "AimSwayData.SwayScaleDecreaseCorrectionSpeed",
           "AimSwayData.SwayScaleIncreaseCorrectionSpeed", "AimSwayData.SwaySpeedDecreaseCorrectionSpeed", "AimSwayData.SwaySpeedIncreaseCorrectionSpeed"]
    heads = ["Persistent", "Pattern duration (s)", "Stand ×", "Crouch ×", "Prone ×", "Focus ×", "No-focus speed ×", "Correction offset time",
             "Camera offset ×", "Scale down speed", "Scale up speed", "Speed down speed", "Speed up speed"]
    A(table(["Weapon"] + heads, wrows(lambda w: [link(w)] + [cell(w, c) for c in sw1])))
    A("")
    A("### 4b. Aim sway deviation, idle sway, stabilisation sway\n")
    sw2 = ["AimSwayData.CurveData.HorizontalDeviationRange", "AimSwayData.CurveData.VerticalDeviationRange", "AimSwayData.WeaponRotationIdleSwayMultiplier",
           "AimSwayData.WeaponTranslationIdleSwayMultiplier", "T:AimSwayData.WeaponTranslationStabilizationSwayCurveStanceMultiplier",
           "T:AimSwayData.WeaponRotationStabilizationSwayCurveStanceMultiplier", "AimSwayData.WeaponRotationStabilizationSwayMultiplier",
           "AimSwayData.WeaponTranslationStabilizationSwayMultiplier", "AimSwayData.bUseTranslationStabilizationJitter",
           "AimSwayData.bUseRotationStabilizationJitter", "AimSwayData.SightSwayDefaultDistanceOffset", "AimSwayData.StabilizationHoldTime"]
    heads = ["Horizontal deviation min … max", "Vertical deviation min … max", "Rotation idle ×", "Translation idle ×", "Translation stab. stance ×",
             "Rotation stab. stance ×", "Rotation stab. ×", "Translation stab. ×", "Translation jitter", "Rotation jitter", "Sight sway distance", "Stabilisation hold (s)"]
    assert all(c.startswith("T:") or c in defaults for c in sw2), [c for c in sw2 if not c.startswith("T:") and c not in defaults]
    rows = wrows(lambda w: [link(w)] + [triple(w, c[2:]) if c.startswith("T:") else cell(w, c) for c in sw2])
    A(table(["Weapon"] + heads, rows))
    A("")
    A("Stance multipliers read `stand / crouch / prone`; each member has its own `†`.\n")
    A("### 4c. Jitter\n")
    jit = [f"AimSwayData.{j}.{k}" for j in ("TranslationStabilizationJitter", "RotationStabilizationJitter")
           for k in ("StabilizationNoiseResultOffset", "StabilizationNoiseJitter", "StabilizationInitialOffset", "GeneralPathJitter", "SecondaryJitter")]
    short = ["Result offset", "Noise jitter", "Initial offset", "Path jitter", "Secondary"]
    A(table(["Weapon"] + [f"Transl. {s}" for s in short] + [f"Rot. {s}" for s in short], wrows(lambda w: [link(w)] + [cell(w, c) for c in jit])))
    A("")
    A("### 4d. Persistent (non-curve) sway values\n")
    rows = []
    for w in weapons:
        if w["fields"].get("AimSwayData.bPersistentValues", {}).get("value"):
            rows.append([link(w)] + [cell(w, f"AimSwayData.PersistentData.{k}") for k in ("AimSwaySpeed", "HorizontalAimSwayMagnitude", "VerticalAimSwayMagnitude")])
    A(table(["Weapon", "Sway speed", "Horizontal magnitude", "Vertical magnitude"], rows) if rows else "No weapon sets `bPersistentValues`.")
    A("")
    A("### 4e. Animation sway\n")
    an = ["bAnimationSwayEnabled", "AnimationSwayData.StandSwayMultiplier", "AnimationSwayData.CrouchSwayMultiplier", "AnimationSwayData.ProneSwayMultiplier",
          "AnimationSwayData.bPersistentHipValues", "AnimationSwayData.HipPitchSwayMultiplier", "AnimationSwayData.HipYawSwayMultiplier",
          "AnimationSwayData.bPersistentADSValues", "AnimationSwayData.ADSPitchSwayMultiplier", "AnimationSwayData.ADSYawSwayMultiplier"]
    A(table(["Weapon", "Enabled", "Stand ×", "Crouch ×", "Prone ×", "Hip persistent", "Hip pitch ×", "Hip yaw ×", "ADS persistent", "ADS pitch ×", "ADS yaw ×"],
            wrows(lambda w: [link(w)] + [cell(w, c) for c in an])))
    A("")
    A("### 4f. Sway curves per weapon\n")
    sc = curve_cats["Sway"] + curve_cats["Movement accuracy"]
    for p in sc:
        ids_by[p] = curve_ids(p)[0]
    A(table(["Weapon"] + [f"`{p.replace('AimSwayData.', '').replace('AnimationSwayData.', 'Anim.')}`" for p in sc],
            wrows(lambda w: [link(w)] + [(f"`{ids_by[p][w['asset']]}`" if ids_by[p][w["asset"]] else "none†") for p in sc])))
    A("")
    A("### 4g. Sway curve keys\n")
    for p in sc:
        curve_section(p, "")

    # --- movement accuracy
    A("## 5. Movement accuracy\n")
    A("Movement changes accuracy through the sway system: the horizontal and vertical movement curves scale the sway magnitude with player speed, "
      "the player-speed stabilisation curve scales how fast the ADS stabilisation builds while moving, and the ADS stabilisation scalars below set "
      "the build and cooldown rates. The curves are listed with the sway curves in 4f and 4g.\n")
    mv = ["AimSwayData.ADSStabilizationMovementSpeedRateUp", "AimSwayData.ADSStabilizationMovementSpeedRateDown",
          "AimSwayData.AdsStabilizationData.AdsStabilizeTime", "AimSwayData.AdsStabilizationData.AdsStabilizeCooldownRate",
          "AimSwayData.AdsStabilizationData.AdsStabilizeExitGracePeriod", "AimSwayData.AdsStabilizationData.AdsStabilizeCooldownRateMovingMultiplier",
          "AimSwayData.AdsStabilizationData.AdsStabilizeMovementProgressPenalty", "AimSwayData.AdsStabilizationData._aaacalknjllchnkieahdj",
          "AimSwayData.AdsStabilizationData._aaablccoleojpkdkeghnk", "AimSwayData.AdsStabilizationData._aaabiaflojcopmfgdolfd"]
    A(table(["Weapon", "Stab. speed rate up", "Stab. speed rate down", "ADS stabilise time (s)", "Cooldown rate", "Exit grace period (s)",
             "Cooldown ×, moving", "Movement progress penalty", "Unnamed +0x124", "Unnamed +0x128", "Unnamed +0x12C"],
            wrows(lambda w: [link(w)] + [cell(w, c) for c in mv])))
    A("")
    A("The three unnamed values sit at `AdsStabilizationData` +0x124, +0x128 and +0x12C; Weapons §5b places +0x128 and +0x12C at the sight-sway "
      "translation and rotation length limits.\n")
    A("### 5a. ADS stabilisation curves\n")
    ac = [c for c in spec if c[0].startswith("AimSwayData.AdsStabilizationData.") and c[2] in ("curve", "vcurve")]
    for p, _, _ in ac:
        ids = curve_ids(p)[0]
        users = [w["label"] for w in weapons if ids[w["asset"]]]
        A(f"`{p}`: set by {len(users)} assets" + (": " + ", ".join(users) if users else " (every other asset takes the empty native curve)") + ".\n")
    A("### 5b. Sight attachments\n")
    A("Sights shift the sway distance and the stabilisation curve multipliers per weapon archetype, and move the camera. An omitted override flag means "
      "the weapon's own value applies. Only sights that set at least one override are listed.\n")
    rows = []
    for s in sight_rows:
        sd, st, co = s["swayDistance"], s["stabilisation"], s["cameraOffset"]
        rows.append([f"[`{s['item']}`]({BLOB}{s['path']})", f"`{s['sight']}`",
                     (num(sd["value"]) if sd["override"] else "—") + (" (per weapon: " + ", ".join(f"{k.split('.')[-1]} {num(v)}" for k, v in sd["perWeapon"].items()) + ")" if sd["perWeapon"] else ""),
                     ", ".join(f"{k.split('.')[-1]}: translation {num(v['WeaponTranslationStabilizationSwayCurveMultiplier'])}, rotation {num(v['WeaponRotationStabilizationSwayCurveMultiplier'])}"
                               for k, v in st["perArchetype"].items()) or ("override, no multipliers" if st["override"] else "—"),
                     (num(co["value"]) if co["override"] else "—") + (" (per weapon: " + ", ".join(f"{k.split('.')[-1]} {num(v)}" for k, v in co["perWeapon"].items()) + ")" if co["perWeapon"] else "")])
    A(table(["Sight item", "Sight", "Sway distance offset", "Stabilisation multipliers by archetype", "Camera offset"], rows))
    A("")
    if unmapped:
        A("Cooked keys with no field in the SDK layout (not tabulated): " + ", ".join(f"`{u}`" for u in sorted(unmapped)) + ".\n")
    return "\n".join(out)


def payload(spec, defaults, weapons, spread_rows, sight_rows):
    return {
        "meta": {"generator": "python -I _tools/spread_recoil_tables.py --write",
                 "native_ctor": "FWDWeaponStats ctor RVA 0x699E6C0 (reference image)",
                 "note": "fields/curves hold the exported value, or the native default when the asset omits it (source says which)"},
        "nativeDefaults": defaults,
        "spreadCurveTable": spread_rows,
        "weapons": weapons,
        "sights": sight_rows,
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec, defaults, weapons, spread_rows, sight_rows, unmapped, native = build()
    body = render(spec, defaults, weapons, spread_rows, sight_rows, unmapped, native)
    if "--write" not in sys.argv:
        print(body)
        return
    unresolved = [p for p, d in defaults.items() if not d["resolved"]]
    if unresolved:
        print("unresolved native defaults:", ", ".join(unresolved))
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    block = BEGIN + "\n" + body + "\n" + END
    new, n = re.subn(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: block, text, flags=re.S)
    if not n:
        sys.exit(f"no {BEGIN} block in {DOC}")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    with open(os.path.join(ROOT, JSON_OUT), "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload(spec, defaults, weapons, spread_rows, sight_rows), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{DOC} and {JSON_OUT} written ({len(weapons)} weapons, {len(sight_rows)} sights, native={'ctor' if native else 'cached'})")


if __name__ == "__main__":
    main()
