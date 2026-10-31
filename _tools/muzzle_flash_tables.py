"""Tables for content/Wardogs_MuzzleFlashes_v1.md: every muzzle-flash data asset, rebuilt from data/.

Reads the three families under data/Wardogs/Content/VFX/Weapons/MuzzleFlashes:
  AmmoMuzzleFlashData        (PDA_MuzzleFlashAmmuniton_C)  per-ammo flash colour and spark overrides
  AttachmentMuzzleFlashData  (PDA_MuzzleFlashAttachement_C) per-muzzle-device multipliers
  MuzzleFlashData/**         (PDA_MuzzleFlash_C)            per-weapon / per-vehicle-gun recipes
Blocks sit between

    <!-- muzzle_flash_tables MODE -->  ...  <!-- /muzzle_flash_tables -->

    python -I _tools/muzzle_flash_tables.py --write      # refresh every block in place
    python -I _tools/muzzle_flash_tables.py --check      # exit 1 when a block is stale
    python -I _tools/muzzle_flash_tables.py MODE         # print one block (counts, ammo, attach, weapons, vehicles)

Stdlib only; idempotent.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_sources import link_source_output  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "Wardogs", "Content", "VFX", "Weapons", "MuzzleFlashes")
PAGE = "content/Wardogs_MuzzleFlashes_v1.md"
BLOCK = re.compile(r"<!-- muzzle_flash_tables (\w+) -->\r?\n.*?<!-- /muzzle_flash_tables -->", re.S)
VEH = ("ROT_", "STN", "TNK_", "WHL_")


def props(path):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    return json.loads(t[t.index("{"):]).get("Properties", {})


def n(v, d=2):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        s = f"{v:.{d}f}".rstrip("0").rstrip(".")
        return s or "0"
    return str(v)


def rgb(c):
    return "" if not c else f"{n(c['R'], 1)} / {n(c['G'], 1)} / {n(c['B'], 1)}"


def xy(c):
    return "" if not c else f"{n(c['X'], 1)} to {n(c['Y'], 1)}"


def objname(o):
    m = re.search(r"'([^']+)'", (o or {}).get("ObjectName", ""))
    return m.group(1) if m else ""


def files(sub):
    out = []
    for p in sorted(glob.glob(os.path.join(BASE, sub, "**", "*.json"), recursive=True)):
        out.append((os.path.relpath(p, os.path.join(BASE, sub)).replace("\\", "/"), props(p)))
    return out


def counts():
    a, b, w = files("AmmoMuzzleFlashData"), files("AttachmentMuzzleFlashData"), files("MuzzleFlashData")
    veh = [x for x in w if any(s in x[0] for s in VEH)]
    return "\n".join(["| Family | Assets |", "|---|---|",
                      f"| Ammo overrides | {len(a)} |", f"| Muzzle device multipliers | {len(b)} |",
                      f"| Weapon recipes (infantry) | {len(w) - len(veh)} |", f"| Vehicle gun recipes | {len(veh)} |",
                      f"| **Total** | {len(a) + len(b) + len(w)} |"])


def ammo():
    rows = ["| Asset | Overrides flash | Flash colour (R / G / B) | Overrides sparks | Spark colour (R / G / B) | Spark count |", "|---|---|---|---|---|---|"]
    for name, p in files("AmmoMuzzleFlashData"):
        rows.append(f"| `{name[:-5]}` | {n(p.get('Override Flash')) or 'not set'} | {rgb(p.get('Flash Color'))} | "
                    f"{n(p.get('Override Sparks')) or 'not set'} | {rgb(p.get('Spark Color'))} | {xy(p.get('Spark Amount'))} |")
    return "\n".join(rows)


def attach():
    rows = ["| Asset | Mesh | Flash size 1P | Flash size 3P | Light | Distant flash | Gas size | Sparks | Pattern size 1P | Offset X |", "|---|---|---|---|---|---|---|---|---|---|"]
    for name, p in files("AttachmentMuzzleFlashData"):
        off = p.get("Offset")
        rows.append(f"| `{name[:-5]}` | {objname(p.get('Mesh'))} | {n(p.get('Flash Size Multiplyer 1P'))} | {n(p.get('Flash Size Multiplyer 3P'))} | "
                    f"{n(p.get('Light Intensity Multiplyer'))} | {n(p.get('Distant Flash Multiplyer'))} | {n(p.get('Gas Size Multiplyer'))} | "
                    f"{xy(p.get('Spark Amount'))} | {n(p.get('Flash Pattern Size 1P'))} | {n(off['X'], 1) if off else ''} |")
    return "\n".join(rows)


def recipes(vehicle):
    rows = ["| Folder | Asset | Flash 1P | Flash 3P | Lifetime (s) | Distant | Distant max | Default muzzle | Other fields |", "|---|---|---|---|---|---|---|---|---|"]
    for rel, p in files("MuzzleFlashData"):
        if any(s in rel for s in VEH) != vehicle:
            continue
        folder, _, name = rel.rpartition("/")
        other = [k for k in p if k not in ("Flash Size 1P", "Flash Size 3P", "Flash Lifetime", "Distant Flash Size", "Distant Flash Max Size", "DefaultMuzzle", "NativeClass", "Flash Color")]
        rows.append(f"| {folder or '(root)'} | `{name[:-5]}` | {n(p.get('Flash Size 1P'))} | {n(p.get('Flash Size 3P'))} | {n(p.get('Flash Lifetime'))} | "
                    f"{n(p.get('Distant Flash Size'))} | {n(p.get('Distant Flash Max Size'))} | `{objname(p.get('DefaultMuzzle')).replace('PDA_MuzzleFlashAttachement_C', '')}` | {', '.join(other)} |")
    return "\n".join(rows)


MODES = {"counts": counts, "ammo": ammo, "attach": attach, "weapons": lambda: recipes(False), "vehicles": lambda: recipes(True)}


def regenerate(text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        return nl.join([f"<!-- muzzle_flash_tables {m.group(1)} -->"] + MODES[m.group(1)]().split("\n") + ["<!-- /muzzle_flash_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(text)
        new = link_source_output(new)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "counts")]())
    return 0


if __name__ == "__main__":
    sys.exit(main())
