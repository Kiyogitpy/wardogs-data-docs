"""Build assets/data/r41-misc.json: small round-41 findings read from cooked data.

    python -I _tools/r41_misc_data.py [--check] [<round41_modes dir>]

Reads, under the scratch directory (default E:/Reverse_Engineer/wardogs_analysis/round41_modes):
  o1/B_FactionSetup_Create{Two,Three}Teams.json   teams a mode creates
  o2/PDA_SmokeGrenade.json, o2/B_MovingTarget.json, o2/DT_ServerTestingProfiles.json
  o3/raw/Wardogs/Content/Localization/Game/<culture>/Game.locres   (UE LocRes v3)
and writes the class defaults of the smoke VFX data asset, the Gym moving target, the empty automation
profile table, and per-culture string counts of the shipped translations. Idempotent. --check exits 1 on
difference. Exits 0 with a message if the input is absent. Nothing from the locres files is copied except counts.
"""
import collections
import glob
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "r41-misc.json")
MAGIC = bytes([0x0E, 0x14, 0x74, 0x75, 0x67, 0x4A, 0x03, 0xFC, 0x4A, 0x15, 0x90, 0x9D, 0xC3, 0x37, 0x7F, 0x1B])


def rstr(b, o):
    n = struct.unpack_from("<i", b, o)[0]
    o += 4
    if n == 0:
        return "", o
    if n < 0:
        n = -n
        return b[o:o + 2 * n - 2].decode("utf-16le"), o + 2 * n
    return b[o:o + n - 1].decode("utf-8", "replace"), o + n


def locres(path):
    b = open(path, "rb").read()
    if b[:16] != MAGIC or b[16] != 3:
        raise ValueError("unsupported locres " + path)
    off = struct.unpack_from("<q", b, 17)[0]
    p = off
    n = struct.unpack_from("<i", b, p)[0]
    p += 4
    arr = []
    for _ in range(n):
        s, p = rstr(b, p)
        p += 4
        arr.append(s)
    o = 17 + 8 + 4
    nn = struct.unpack_from("<i", b, o)[0]
    o += 4
    out = {}
    for _ in range(nn):
        o += 4
        ns, o = rstr(b, o)
        nk = struct.unpack_from("<i", b, o)[0]
        o += 4
        for _ in range(nk):
            o += 4
            k, o = rstr(b, o)
            o += 4
            idx = struct.unpack_from("<i", b, o)[0]
            o += 4
            out[(ns, k)] = arr[idx]
    return out


def props(path, typ_prefix=None, name_prefix=None):
    for o in json.load(open(path, encoding="utf-8")):
        if name_prefix and o["Name"].startswith(name_prefix) and "Properties" in o:
            return o["Properties"]
    return {}


def main():
    check = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else r"E:/Reverse_Engineer/wardogs_analysis/round41_modes"
    if not os.path.isdir(os.path.join(base, "o2")):
        print(f"input not found ({base}); skipping")
        return 0
    out = {"source": "round 41 cooked-data read (docs/evidence/round41-modes-ai-other.md)"}
    teams = {}
    for n in ("CreateTwoTeams", "CreateThreeTeams"):
        d = props(os.path.join(base, "o1", f"B_FactionSetup_{n}.json"), name_prefix="Default__")
        teams[n] = [x["ObjectName"].split("'")[1].replace("Meta_Alignment_Faction_", "") for x in d["FactionsToCreate"]]
    out["factionSetup"] = teams
    out["smokeGrenadeClassDefaults"] = props(os.path.join(base, "o2", "PDA_SmokeGrenade.json"), name_prefix="Default__")
    mt = props(os.path.join(base, "o2", "B_MovingTarget.json"), name_prefix="Default__")
    out["movingTarget"] = {k: mt[k] for k in ("Health", "DamageIncrease", "TimeToReachTargetRange") if k in mt}
    out["movingTarget"]["fallTimelineSeconds"] = 0.5
    out["movingTarget"]["moveLocationOffsetY"] = 150.0
    tbl = json.load(open(os.path.join(base, "o2", "DT_ServerTestingProfiles.json"), encoding="utf-8"))[0]
    rows = tbl.get("Rows", {}) or {}
    out["serverTestingProfiles"] = {
        "rowStruct": "WDAutomatedTestServerProfile",
        "rows": {k: {"totalClients": v["TotalClients"], "orchestrator": v["TestOrchestrator"]["AssetPathName"].rsplit(".", 1)[-1]} for k, v in rows.items()},
    }
    loc = {}
    cultures = {}
    en = None
    for p in sorted(glob.glob(os.path.join(base, "o3", "raw", "Wardogs", "Content", "Localization", "Game", "*", "Game.locres"))):
        c = os.path.basename(os.path.dirname(p))
        cultures[c] = locres(p)
        if c == "en":
            en = cultures[c]
    ns = collections.Counter(k[0] for k in en)
    out["localization"] = {
        "archive": "Game.locres (UE LocRes version 3)",
        "cultures": {c: {"entries": len(v), "sameAsEnglish": sum(1 for k, x in v.items() if en.get(k) == x)} for c, v in sorted(cultures.items())},
        "namespaces": len(ns),
        "largestNamespaces": [[k or "(empty)", n] for k, n in ns.most_common(8)],
    }
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if check:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("ok" if cur == text else "DIFFERS")
        return 0 if cur == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
