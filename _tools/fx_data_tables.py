"""Tables for content/Wardogs_FX_Field_Tables_v1.md: every field of the explosion, impact, vehicle-prop and muzzle-flash data assets.

Reads, from data/Wardogs/Content:
  VFX/Explosions/*.json                  PDA_Explosion_C (35 assets; the 14 PDA_ExplosionTimingData_C sequences are on the VFX page)
  VFX/Weapons/Impacts/*.json             PDA_PhysicalMaterialResponse_C (9)
  Environment/Blueprints/VehiclePropTooling/DA_*.json   PDA_VehicleProp_C (34)
  VFX/Weapons/MuzzleFlashes/MuzzleFlashData/**          PDA_MuzzleFlash_C (48)
  VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/  PDA_MuzzleFlashAttachement_C (47)
Blocks sit between

    <!-- fx_data_tables MODE -->  ...  <!-- /fx_data_tables -->

    python -I _tools/fx_data_tables.py --write     # refresh every block in place
    python -I _tools/fx_data_tables.py --check     # exit 1 when a block is stale
    python -I _tools/fx_data_tables.py MODE        # print one block

Blank cell = the asset does not set the field (the class default applies; the export does not give it). Stdlib only; idempotent.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "data", "Wardogs", "Content")
PAGE = os.path.join(ROOT, "content", "Wardogs_FX_Field_Tables_v1.md")
BLOCK = re.compile(r"<!-- fx_data_tables (\w+) -->\r?\n.*?<!-- /fx_data_tables -->", re.S)
NL = chr(10)


def props(path):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    return json.loads(t[t.index("{"):]).get("Properties", {})


def folder(sub, recursive=False, prefix=""):
    pat = os.path.join(CONTENT, sub, "**" if recursive else "", prefix + "*.json")
    out = []
    for p in sorted(glob.glob(pat, recursive=recursive)):
        if os.path.basename(p).startswith("DT_"):
            continue
        out.append((os.path.relpath(p, os.path.join(CONTENT, sub)).replace(os.sep, "/")[:-5], props(p)))
    return out


def short(path):
    """Last name of an object or asset path."""
    m = re.search(r"'([^']+)'", path)
    return m.group(1) if m else path.split("/")[-1].split(".")[0]


def num(v, d=4):
    s = f"{v:.{d}g}" if abs(v) < 100000 else f"{v:,.0f}"
    if "e" in s:
        s = f"{v:.{d}f}".rstrip("0").rstrip(".")
    return s


def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)):
        return num(v)
    if isinstance(v, str):
        return f"`{v}`"
    if isinstance(v, list):
        return "; ".join(x for x in (cell(i) for i in v) if x)
    if isinstance(v, dict):
        if "AssetPathName" in v:
            return f"`{short(v['AssetPathName'])}`" if v["AssetPathName"] and v["AssetPathName"] != "None" else ""
        if "ObjectName" in v:
            return f"`{short(v['ObjectName'])}`"
        if {"R", "G", "B"} <= set(v):
            return f"{num(v['R'], 3)} / {num(v['G'], 3)} / {num(v['B'], 3)}"
        if {"X", "Y", "Z"} <= set(v):
            return f"{num(v['X'])}, {num(v['Y'])}, {num(v['Z'])}"
        if {"X", "Y"} <= set(v):
            return f"{num(v['X'])} to {num(v['Y'])}"
    return str(v)


def table(rows, cols, first="Asset"):
    """cols: [(header, key)]; rows: [(name, props)]."""
    out = ["| " + " | ".join([first] + [h for h, _ in cols]) + " |", "|" + "---|" * (len(cols) + 1)]
    for name, p in rows:
        out.append("| " + " | ".join([f"`{name}`"] + [cell(p.get(k)) for _, k in cols]) + " |")
    return NL.join(out)


def explosions_a():
    cols = [("Fireball", "Fireball"), ("Fireball size", "FireballSize"), ("Fireball life (s)", "FireballLifetime"),
            ("Fireball distance", "FireBallDistance"), ("Origin distance", "OriginDistance"), ("Core size", "CoreSize"),
            ("Core amount", "CoreAmount"), ("Small core size", "SmallCoreSize"), ("Small core amount", "CoreAmountSmall"),
            ("Size multiplier", "SizeMultiplyer"), ("Heat", "HeatIntensity"), ("Hanging smoke", "HangingSmoke"),
            ("Remains smoking", "RemainsSmoking"), ("Remains flames", "RemainsFlames")]
    return table(folder("VFX/Explosions"), cols)


def explosions_b():
    cols = [("Streaks", "StreaksAmount"), ("Streak size", "StreakSize"), ("Small streaks", "StreaksAmountSmall"),
            ("Small streak size", "SmallStreakSize"), ("Embers", "Embers"), ("Sparks", "SparksAmount"),
            ("Debris", "DebrisAmount"), ("Debris scale", "DebrisScale"), ("Shockwave", "Shockwave"),
            ("Shockwave size", "ShockWaveSize"), ("Camera shake", "CameraShake"), ("Shake range", "CameraShakeRange")]
    return table(folder("VFX/Explosions"), cols)


def impacts():
    cols = [("Bullet impact effect", "BulletImpactEffect"), ("Bullet decal", "BulletDecal"),
            ("Explosion effects (by size)", "ExplosionEffect"), ("Explosion decal", "ExplosionDecal"),
            ("Explosion decal size", "ExplosionDecalSize"), ("Small caliber", "SmallCaliberSIze"),
            ("Medium caliber", "MediumCaliberSIze"), ("Large caliber", "LargeCaliberSIze"),
            ("Size random min", "SizeRandomMin"), ("Size random max", "SizeRandomMax")]
    return table(folder("VFX/Weapons/Impacts"), cols)


def vehicle_props():
    rows = folder("Environment/Blueprints/VehiclePropTooling", prefix="DA_")
    mesh = [("Base mesh", "BaseMesh"), ("Base scale", "BaseMeshScale"), ("Glass mesh", "BaseGlassMesh"),
            ("Glass scale", "BaseGlassMeshScale"), ("Cabin mesh", "CabinMesh"), ("Cabin scale", "CabinScale"),
            ("Load mesh", "LoadMesh"), ("Load scale", "LoadScale"), ("Roof mesh", "RoofMesh"), ("Roof scale", "RoofMeshScale"),
            ("Wheel mesh", "WheelMeshPrimary"), ("Wheel scale", "Wheel Uniform Scale"),
            ("Material override", "BaseMaterialOverride")]
    return table(rows, mesh)


def vehicle_colors():
    rows = folder("Environment/Blueprints/VehiclePropTooling", prefix="DA_")
    out = ["| Asset | Base colors | Cabin colors | Load colors | Wheel colors |", "|---|---|---|---|---|"]

    def hexes(v):
        return " ".join(f"`{c['Hex']}`" for c in (v or []))
    for name, p in rows:
        out.append(f"| `{name}` | {hexes(p.get('BaseColor'))} | {hexes(p.get('CabinColor'))} | {hexes(p.get('LoadColor'))} | {hexes(p.get('WheelColor'))} |")
    return NL.join(out)


def flash_recipes(vehicle):
    rows = [(n, p) for n, p in folder("VFX/Weapons/MuzzleFlashes/MuzzleFlashData", recursive=True)
            if any(s in n for s in ("ROT_", "STN", "TNK_", "WHL_")) == vehicle]
    if vehicle:
        cols = [("Niagara system", "NiagaraSystem"), ("Distant system", "DistantMuzzleFlash"), ("Material", "Material"),
                ("Flash color (RGB, HDR)", "Flash Color"), ("Flash 1P", "Flash Size 1P"), ("Flash 3P", "Flash Size 3P"),
                ("Lifetime (s)", "Flash Lifetime"), ("Frequency", "Flash Frequency"), ("Distant size", "Distant Flash Size"),
                ("Distant max", "Distant Flash Max Size"), ("Distant chance", "Distant Flash Probability"),
                ("Light intensity", "Light Intensity"), ("Light radius", "Light Radius"), ("Light color", "Light Color"),
                ("Gas size", "GasSize"), ("Gas amount", "GasAmount"), ("Gas lifetime (s)", "GasLifetime"), ("Gas spread", "GasSpread"),
                ("Spark amount", "Spark Amount"), ("Spark color", "Spark Color"), ("Spark spread", "Spark Spread"),
                ("Socket", "OverrideSocketName"), ("Spawn offset", "RelativeSpawnOffset"), ("Pooling", "UseManualPooling"),
                ("Default muzzle", "DefaultMuzzle")]
    else:
        cols = [("Flash color (RGB, HDR)", "Flash Color"), ("Flash 1P", "Flash Size 1P"), ("Flash 3P", "Flash Size 3P"),
                ("Lifetime (s)", "Flash Lifetime"), ("Frequency", "Flash Frequency"), ("Distant size", "Distant Flash Size"),
                ("Distant max", "Distant Flash Max Size"), ("Distant chance", "Distant Flash Probability"),
                ("Light intensity", "Light Intensity"), ("Light color", "Light Color"), ("Gas size", "GasSize"),
                ("Gas amount", "GasAmount"), ("Gas lifetime (s)", "GasLifetime"), ("Gas spread", "GasSpread"),
                ("Spark amount", "Spark Amount"), ("Spark color", "Spark Color"), ("Spark spread", "Spark Spread"),
                ("Default muzzle", "DefaultMuzzle")]
    return table(rows, cols, "Recipe")


def flash_devices():
    cols = [("Mesh", "Mesh"), ("Offset", "Offset"), ("Flash material", "Flash Material"), ("Flash 1P x", "Flash Size Multiplyer 1P"),
            ("Flash 3P x", "Flash Size Multiplyer 3P"), ("Head-on x", "Flash Head On Size Multiplyer"),
            ("Distant x", "Distant Flash Multiplyer"), ("Light x", "Light Intensity Multiplyer"),
            ("Gas size x", "Gas Size Multiplyer"), ("Gas side scale", "Gas Side Scale"), ("Spark amount", "Spark Amount"),
            ("Pattern", "Flash Pattern"), ("Pattern count", "Flash Pattern Count"), ("Pattern 1P", "Flash Pattern Size 1P"),
            ("Pattern 3P", "Flash Pattern Size 3P"), ("Pattern offset", "Flash Pattern Offset"), ("Pattern tilt", "Flash Pattern Tilt"),
            ("Distant chance", "Distant Flash Probability")]
    rows = folder("VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData")
    return table(rows, cols, "Muzzle device")


def counts():
    n = {"explosions": len(folder("VFX/Explosions")), "impacts": len(folder("VFX/Weapons/Impacts")),
         "props": len(folder("Environment/Blueprints/VehiclePropTooling", prefix="DA_")),
         "recipes": len(folder("VFX/Weapons/MuzzleFlashes/MuzzleFlashData", recursive=True)),
         "devices": len(folder("VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData"))}
    return NL.join(["| Asset class | Assets | Section |", "|---|---:|---|",
                    f"| `PDA_Explosion_C` | {n['explosions']} | 1 |", f"| `PDA_PhysicalMaterialResponse_C` | {n['impacts']} | 2 |",
                    f"| `PDA_VehicleProp_C` | {n['props']} | 3 |", f"| `PDA_MuzzleFlash_C` | {n['recipes']} | 4 |",
                    f"| `PDA_MuzzleFlashAttachement_C` | {n['devices']} | 4 |"])


BLOCKS = {"counts": counts, "explosions_a": explosions_a, "explosions_b": explosions_b, "impacts": impacts,
          "props": vehicle_props, "prop_colors": vehicle_colors,
          "flash_weapons": lambda: flash_recipes(False), "flash_vehicles": lambda: flash_recipes(True),
          "flash_devices": flash_devices}


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace(chr(13) + NL, NL)


def render(text):
    return BLOCK.sub(lambda m: f"<!-- fx_data_tables {m.group(1)} -->{NL}{BLOCKS[m.group(1)]()}{NL}<!-- /fx_data_tables -->", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if args and args[0] in BLOCKS:
        print(BLOCKS[args[0]]())
        return 0
    page = read(PAGE)
    new = render(page)
    if "--write" in args:
        if new != page:
            with open(PAGE, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            print("wrote", os.path.relpath(PAGE, ROOT))
        return 0
    if "--check" in args:
        if new != page:
            print("stale:", os.path.relpath(PAGE, ROOT))
            return 1
        print("fx_data_tables: up to date")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
