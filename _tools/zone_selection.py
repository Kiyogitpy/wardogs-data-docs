"""Round 40: how a King of the Hill match picks its zone layout and where the Hot Zone goes, as data.

Writes assets/data/zone-selection.json from the cooked ControlZone and ControlZoneRegions data assets under data/.
The selection rules themselves come from the decompiled client (docs/evidence/round40-modes-ai-other.md, section
"Zone layout and region selection"); they are recorded here as text next to the numbers they apply to, and the
fallback probabilities (weight / sum of weights) are computed from the data.

    python -I _tools/zone_selection.py            # rewrite assets/data/zone-selection.json
    python -I _tools/zone_selection.py --check    # exit 1 if stale

Stdlib only; idempotent.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GF = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures")
CZ = os.path.join(GF, "ControlZone", "Content", "ControlZone", "Config")
CZR = os.path.join(GF, "ControlZoneRegions", "Content", "Data", "Config")
OUT = os.path.join(ROOT, "assets", "data", "zone-selection.json")

RULES = {
    "layoutOrder": [
        "1. Only on the server (authority) and only if the config has bActivateAlternator.",
        "2. Launch option DisableZoneAlternator: no alternator, the config's base ZoneData is used (index -1).",
        "3. The layout tag set for the match (the server map rotation's ZoneAlternator entry): used if the config has an alternator with that exact tag. If several entries share the tag, one is picked by weight.",
        "4. Otherwise, if ControlZoneQueue (server ini list of tag suffixes, empty by default) produced valid tags: entry number (map-load counter modulo queue length).",
        "5. Otherwise a weighted random pick over AlternatorSelectionWeight; weight-0 entries are skipped, so they are never picked this way (only by step 3 or 4).",
    ],
    "regionRule": [
        "The Hot Zone is moved to a point inside one region of ControlZoneRegionsConfig.",
        "Candidates: regions that are not the previously chosen region, that have a weight slot, that have no polygon point within MinHotZoneMoveDistance of the current Hot Zone position, and that have at least one polygon point passing a placement test.",
        "Region weight = ControlZoneRegionAlternatorWeights[AlternatorIndex] if that index exists, otherwise ControlZoneRegionDefaultWeight. The weight used in the draw is a dynamic copy (below).",
        "One draw: random number in [0, sum of candidates' dynamic weights]; the first candidate whose running total reaches it is chosen. Server command Auth_SetNextSelectedIndex can force the next region instead (used once).",
        "After a region is chosen it gives away half of its dynamic weight; that half is shared among the other regions in proportion to their configured weights (total weight stays constant). So a region just used is less likely next time and the others recover.",
    ],
    "hotZoneTimer": [
        "First move after FirstMoveDelay (0 when absent), then every MoveDelay (25 s in the King of the Hill configs) multiplied by a scale read from the game-state side (1.0 when none is available). Sniper Showdown configs have both at 0.",
    ],
}


def load(path):
    t = open(path, encoding="utf-8-sig").read()
    return json.loads(t[t.index("\n") + 1:])["Properties"]


def main():
    out = {"_note": "Rules decoded from the client (static); numbers from cooked data. See docs/evidence/round40-modes-ai-other.md.",
           "rules": RULES, "layouts": {}, "regions": {}}
    for f in sorted(glob.glob(os.path.join(CZ, "*.json"))):
        p = load(f)
        name = os.path.basename(f)[:-5]
        hm = p.get("HotZoneMovementData", {})
        ent = {"activateAlternator": bool(p.get("bActivateAlternator")),
               "hotZoneMovement": {k: v for k, v in hm.items() if not isinstance(v, (dict, list))},
               "hotzoneSpeeds": hm.get("HotzoneSpeeds", []),
               "zoneShape": p.get("ZoneData", {}).get("ControlZoneData", {}).get("ZoneShape", "EWDZoneShape::Box (default, not stored)"),
               "controlZoneExtents": p.get("ZoneData", {}).get("ControlZoneData", {}).get("ZoneScaledExtents"),
               "hotZoneExtents": p.get("ZoneData", {}).get("HotZoneData", {}).get("ZoneScaledExtents"),
               "alternators": []}
        alts = p.get("AlternatorZoneData", [])
        total = sum(a.get("AlternatorSelectionWeight", 0.0) for a in alts)
        for i, a in enumerate(alts):
            w = a.get("AlternatorSelectionWeight", 0.0)
            ent["alternators"].append({"index": i, "tag": a["AlternatorTag"]["TagName"], "weight": w,
                                       "fallbackProbability": round(w / total, 4) if total else 0.0})
        out["layouts"][name] = ent
    for f in sorted(glob.glob(os.path.join(CZR, "**", "*.json"), recursive=True)):
        p = load(f)
        regs = []
        for r in p["ControlZoneRegionsData"]:
            aw = r.get("ControlZoneRegionAlternatorWeights", [])
            regs.append({"name": r["ControlZoneRegionName"], "defaultWeight": r.get("ControlZoneRegionDefaultWeight", 0.0),
                         "alternatorWeights": aw, "points": len(r.get("ControlZoneRegionPoints", []))})
        out["regions"][os.path.basename(f)[:-5]] = regs
    return json.dumps(out, indent=1, sort_keys=True) + "\n"


if __name__ == "__main__":
    data = main()
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != data:
            print("stale: run python -I _tools/zone_selection.py")
            sys.exit(1)
        print("ok")
    else:
        open(OUT, "w", encoding="utf-8", newline="\n").write(data)
        print("wrote", os.path.relpath(OUT, ROOT))
