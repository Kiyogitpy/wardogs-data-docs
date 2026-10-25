"""Round 44: shop price modifiers from DefaultGame.ini, with the ratio the client applies.

Reads the +PriceModifiers= lines of data/Wardogs/Config/DefaultGame.excerpt.ini (UWDEconomyConfig) and writes
assets/data/price-modifiers.json. The client divides Multiplier by 100: the base modifier slot 1 (0x6BE48D0) calls
slot 3 (0x6BE4930), which returns Multiplier * 0.01 for a Global modifier or Data[i].Multiplier * 0.01 for a Specified
one whose entity tag matches (constant 0.00999999978 at 0x9AAD9DC, default Multiplier 100.0 in the constructors).

    python -I _tools/price_modifiers.py            # rewrite assets/data/price-modifiers.json (idempotent)
    python -I _tools/price_modifiers.py --check    # exit 1 if the file is stale
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INI = os.path.join(ROOT, "data", "Wardogs", "Config", "DefaultGame.excerpt.ini")
OUT = os.path.join(ROOT, "assets", "data", "price-modifiers.json")
LINE = re.compile(r"^\+PriceModifiers=/Script/WDGame\.WDEntityPriceModifier_(\w+)\((.*)\)\s*$")


def build():
    rows = []
    for ln in open(INI, encoding="utf8", errors="ignore"):
        m = LINE.match(ln.strip())
        if not m:
            continue
        kind, body = m.groups()
        rec = {"kind": kind, "target": (re.search(r"EntityTarget=(\w+)", body) or [None, None])[1]}
        # top-level Multiplier is the last one in the line (Data=(...) holds nested Multiplier values)
        top = re.findall(r"Multiplier=([-0-9.]+)", body)
        rec["multiplier"] = float(top[-1])
        rec["ratio"] = round(rec["multiplier"] / 100.0, 6)
        data = re.search(r"Data=\(\((.*)\)\),Multiplier=", body)
        if data:
            rec["entities"] = re.findall(r'TagName="([^"]+)"', data.group(1))
            nested = re.findall(r"Multiplier=([-0-9.]+)", data.group(1))
            rec["entityMultipliers"] = [float(x) for x in nested]
            rec["entityRatios"] = [round(float(x) / 100.0, 6) for x in nested]
        for key in ("Faction", "RequiredTag"):
            f = re.search(key + r'=\(TagName="([^"]*)"\)', body)
            if f:
                rec[key[0].lower() + key[1:]] = f.group(1)
        for key in ("LevelType", "LevelRequirement"):
            f = re.search(key + r"=(\w+)", body)
            if f:
                rec[key[0].lower() + key[1:]] = f.group(1)
        for key in ("Level", "ScoreDifference"):
            f = re.search(r"\b" + key + r"=(-?\d+)", body)
            if f:
                rec[key[0].lower() + key[1:]] = int(f.group(1))
        rows.append(rec)
    return {"source": "data/Wardogs/Config/DefaultGame.excerpt.ini [UWDEconomyConfig] PriceModifiers",
            "divisor": 100, "note": "ratio = Multiplier / 100; a price is multiplied by the product of all applicable ratios",
            "modifiers": rows}


def main():
    text = json.dumps(build(), indent=2) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
        sys.exit(0 if cur == text else 1)
    with open(OUT, "w", encoding="utf8", newline="\n") as f:
        f.write(text)
    print("wrote", OUT, len(build()["modifiers"]), "modifiers")


if __name__ == "__main__":
    main()
