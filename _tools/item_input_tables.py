"""Tables for content/Wardogs_MiscGameplayAssets_v1.md section "Item inputs and small settings".

Rebuilds from data/: the item input mapping contexts of the Defibrillator and the IED, the build-wheel slot assets of
the six stationary weapons, the Crowbar force-open-door character modifier state, the body-dragging settings, the
RPG aim-assist settings and the two explosion VFX recipes not listed elsewhere. Blocks sit between

    <!-- item_input_tables MODE -->  ...  <!-- /item_input_tables -->

    python -I _tools/item_input_tables.py --write   # refresh every block in place
    python -I _tools/item_input_tables.py --check   # exit 1 when a block is stale
    python -I _tools/item_input_tables.py MODE      # print one block (keys, wheel, door, drag, rpg, explosions)

Stdlib only; idempotent.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "data", "Wardogs")
GF = os.path.join(W, "Plugins", "GameFeatures")
PAGE = "content/Wardogs_MiscGameplayAssets_v1.md"
BLOCK = re.compile(r"<!-- item_input_tables (\w+) -->\r?\n.*?<!-- /item_input_tables -->", re.S)


def exports(path):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    out, dec, i = [], json.JSONDecoder(), 0
    while True:
        j = t.find("{", i)
        if j < 0:
            return out
        o, e = dec.raw_decode(t[j:])
        out.append(o)
        i = j + e


def main_export(path):
    for o in exports(path):
        if "Package" in o:
            return o.get("Properties", {})
    return exports(path)[0].get("Properties", {})


def short(o):
    m = re.search(r"'([^']+)'", (o or {}).get("ObjectName", ""))
    return m.group(1) if m else ""


def keys():
    files = [("Defibrillator", "Items/Defibrillator/Content/Data/IMC_Defibrillator.json"),
             ("Defibrillator (release context)", "Items/Defibrillator/Content/Data/IMC_DefibrillatorRelease.json"),
             ("IED", "Items/IED/Content/Data/IMC_IED.json")]
    rows = ["| Item | Action | Keys |", "|---|---|---|"]
    for label, rel in files:
        acts = {}
        for m in main_export(os.path.join(GF, rel))["DefaultKeyMappings"]["Mappings"]:
            acts.setdefault(short(m["Action"]), []).append(m["Key"]["KeyName"])
        for a, ks in acts.items():
            rows.append(f"| {label} | `{a}` | {', '.join(f'`{k}`' for k in ks)} |")
    return "\n".join(rows)


def wheel():
    rows = ["| Asset | Buildable tag | Wheel title |", "|---|---|---|"]
    for p in sorted(glob.glob(os.path.join(GF, "Vehicles", "STN_*", "Content", "BuildableData", "DA_RadialWheelSlotType_*.json"))):
        d = main_export(p)
        rows.append(f"| `{os.path.basename(p)[:-5]}` | `{d['ItemTag']['TagName']}` | {d['SlotTitle']['SourceString'].strip()} |")
    return "\n".join(rows)


def door():
    path = os.path.join(GF, "Items", "Crowbar", "Content", "Data", "DA_CharacterModifierState_ForceOpenDoor.json")
    ex = exports(path)
    state = next(o for o in ex if o.get("Type") == "WDCharacterModifierStateDefinition")["Properties"]
    cond = next(o for o in ex if o.get("Type") == "WDCharacterModifierCondition_Tags")["Properties"]["Requirements"]
    mods = [short(o) for o in state["CharacterModifiers"]]
    return "\n".join(["| Field | Value |", "|---|---|", f"| State tag | `{state['StateTag']['TagName']}` |",
                      f"| Priority | {state['Priority']} |", f"| Modifier | `{mods[0].split(':')[0]}` |",
                      f"| Active while the player has | {', '.join(f'`{t}`' for t in cond['RequireTags'])} |",
                      f"| Not active while the player has | {', '.join(f'`{t}`' for t in cond['IgnoreTags'])} |"])


def drag():
    d = main_export(os.path.join(W, "Content", "MoverTesting", "Settings", "DA_BodyDragging.json"))
    rows = ["| Field | Value |", "|---|---|"]
    for k, v in d.items():
        if not k.startswith("_"):
            rows.append(f"| `{k}` | {v} |")
    return "\n".join(rows)


def rpg():
    d = main_export(os.path.join(W, "Content", "Items", "Weapons", "DA_AimAssistSettings_RPG.json"))
    zero = sum(1 for v in d.values() if isinstance(v, dict) and v.get("Value") == 0.0)
    rows = ["| Field | Value |", "|---|---|", f"| `PullMode` | {d['PullMode'].split('::')[-1]} |",
            f"| `PullModeADS` | {d['PullModeADS'].split('::')[-1]} |", f"| `StrengthScale` | {d['StrengthScale']} |",
            f"| `MaxNumberOfTargets` | {d['MaxNumberOfTargets']} |", f"| Reticle, range and pull fields set to 0 | {zero} |"]
    return "\n".join(rows)


def explosions():
    rows = ["| Recipe | Core size | Fireball size | Shockwave size | Streaks | Sparks | Debris | Embers | Camera shake range | Heat intensity |", "|---|---|---|---|---|---|---|---|---|---|"]
    for n in ("DA_Explosion_122mm", "DA_Explosion_120x2230mm", "DA_Explosion_125x570mm"):
        d = main_export(os.path.join(W, "Content", "VFX", "Explosions", n + ".json"))
        f = lambda k: ("" if k not in d else f"{d[k]:.4g}")
        rows.append(f"| `{n}` | {f('CoreSize')} | {f('FireballSize')} | {f('ShockWaveSize')} | {f('StreaksAmount')} | {f('SparksAmount')} | "
                    f"{f('DebrisAmount')} | {f('Embers')} | {f('CameraShakeRange')} | {f('HeatIntensity')} |")
    return "\n".join(rows)


MODES = {"keys": keys, "wheel": wheel, "door": door, "drag": drag, "rpg": rpg, "explosions": explosions}


def regenerate(text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        return nl.join([f"<!-- item_input_tables {m.group(1)} -->"] + MODES[m.group(1)]().split("\n") + ["<!-- /item_input_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "keys")]())
    return 0


if __name__ == "__main__":
    sys.exit(main())
