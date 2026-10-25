"""assets/data/r46-guidance.json: guided-projectile data (WDProjectileGuidance) of the cooked projectile assets.

Reads `data/` only (cooked JSON). A key a projectile asset does not store keeps the struct's native default,
which was not read. Nothing was run.

    python -I _tools/r46_guidance_data.py           # rewrite assets/data/r46-guidance.json
    python -I _tools/r46_guidance_data.py --check   # exit 1 when the file is stale
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "r46-guidance.json")
BASE = os.path.join(ROOT, "data", "Wardogs", "Content")
ASSETS = {
    "DA_70mm_ProjectileData": "GameMechanics/Inventory/Equipment/Caliber/70mm/DA_70mm_ProjectileData.json",
    "DA_72mm_ProjectileData": "GameMechanics/Inventory/Equipment/Caliber/72mm/DA_72mm_ProjectileData.json",
    "DA_DebugHomingRocketData": "Items/Resources/Ammo/DebugHomingRocket/DA_DebugHomingRocketData.json",
}


def load(rel):
    with open(os.path.join(BASE, rel), encoding="utf-8") as f:
        t = f.read()
    return json.loads(t[t.index("{"):])


def build():
    rows = {}
    for name, rel in ASSETS.items():
        d = load(rel)
        s = d["Properties"]["ProjectileStats"]
        rows[name] = {"GuidanceData": s.get("GuidanceData"), "TypicalSpeed": s.get("TypicalSpeed"),
                      "MaxProjectileLifetime": s.get("MaxProjectileLifetime"), "ArmingDelay": s.get("ArmingDelay")}
    return {"_note": "WDProjectileGuidance fields stored in the cooked asset; unset keys keep the native struct default (not read). "
                     "Struct layout: bGuidedProjectile, ProportionalNavigationConstant, MaxTurnAngle, LockOnTime, NearMissExtentMultiplier.",
            "projectiles": rows}


def main():
    text = json.dumps(build(), indent=2) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        sys.exit(0 if cur == text else 1)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


if __name__ == "__main__":
    main()
