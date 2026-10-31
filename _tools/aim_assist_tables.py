"""Aim-assist curves and the settings fields not tabulated elsewhere, for content/Wardogs_AimAssistCurves_v1.md.

Reads the eight Items/Weapons/DA_AimAssistSettings_* assets and the sixteen BHAimAssist plugin curves (CurveFloat).
Blocks sit between <!-- aim_assist NAME --> and <!-- /aim_assist -->: curves (every key), classes (which curve each class
uses and the target-score, sensitivity and unnamed fields), hashed (the seven unnamed floats with offsets from the SDK).

    python -I _tools/aim_assist_tables.py --write | --check | curves | classes | hashed
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_sources import link_source_output  # noqa: E402
import challenge_tables as ct  # noqa: E402

ROOT, DATA, N = ct.ROOT, ct.DATA, ct.n
PAGE = os.path.join(ROOT, "content/Wardogs_AimAssistCurves_v1.md")
BLOCK = re.compile(r"<!-- aim_assist (\w+) -->\r?\n.*?<!-- /aim_assist -->", re.S)
CLASSES = ["AR", "LMG", "SMG", "Shotgun", "SR", "Pistol", "Melee", "RPG"]
HASHED = [("_aaablbcidfbimhkninjgh", "0x3B0"), ("_aaabohfjefmdjckeghchd", "0x3B4"), ("_aaabifkkogdgdilllniki", "0x3B8"),
          ("_aaabiopcjcdaaocfaifcm", "0x3BC"), ("_aaabgnegmcifdipjmhfdb", "0x3C0"), ("_aaabkejidmenonabgonll", "0x3C4"),
          ("_aaabfibckgemadeemoaha", "0x3C8")]


def classes():
    out = {}
    for c in CLASSES:
        out[c] = ct.exports(os.path.join(DATA, "Wardogs/Content/Items/Weapons/DA_AimAssistSettings_%s.json" % c))[0]["Properties"]
    return out


def val(p, k):
    v = p.get(k)
    if v is None:
        return "-"
    if isinstance(v, dict):
        if "Value" in v:
            return N(v["Value"])
        return "`" + str(v.get("ObjectName", "")).split("'")[1].replace("C_AimAssist", "") + "`" if "'" in str(v.get("ObjectName", "")) else "-"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)):
        return N(v)
    return str(v).split("::")[-1]


def curves_block():
    rows = ["| Curve | Keys (distance in cm, strength 0 to 1) |", "|---|---|"]
    for f in sorted(glob.glob(os.path.join(DATA, "Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_*.json"))):
        e = ct.exports(f)[0]
        keys = e["Properties"]["FloatCurve"]["Keys"]
        name = os.path.basename(f)[2:-5]
        label = "`C_%s`" % name
        pts = ", ".join("(%g, %g)" % (k["Time"], round(k["Value"], 4)) for k in keys)
        if "Edge" in name:
            pts += " (key is the position inside the reticle, 0 at the centre and 1 at the edge, not a distance)"
        elif "TargetWeight" in name:
            pts += " (key unit not named in the export)"
        rows.append("| %s | %s |" % (label, pts))
    return "\n".join(rows)


def classes_block():
    d = classes()
    fields = [("Hip pull curve", "PullStrengthDistanceCurve"), ("ADS pull curve", "PullStrengthDistanceCurveADS"),
              ("Hip slow curve", "SlowStrengthDistanceCurve"), ("ADS slow curve", "SlowStrengthDistanceCurveADS"),
              ("Reticle edge falloff", "_aaabhkcdlildobfpgdcfh"), ("Target weight curve", "TargetWeightCurve"),
              ("`SensitivityScale` (hip)", "SensitivityScale"), ("`SensitivityScaleADS`", "SensitivityScaleADS"),
              ("`StrengthScale`", "StrengthScale"), ("`TargetScore_AssistWeight`", "TargetScore_AssistWeight"),
              ("`TargetScore_ViewDot`", "TargetScore_ViewDot"), ("`TargetScore_ViewDotOffset`", "TargetScore_ViewDotOffset"),
              ("`TargetScore_ViewDistance`", "TargetScore_ViewDistance"), ("`TargetScore_RenderedRecently`", "TargetScore_RenderedRecently"),
              ("`bFOVReticleScaling`", "bFOVReticleScaling"), ("`bApplySlowing`", "bApplySlowing"), ("`bUseDynamicSlow`", "bUseDynamicSlow"),
              ("`bApplyStrafePullScale`", "bApplyStrafePullScale")]
    rows = ["| Field | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
    for label, k in fields:
        rows.append("| %s | " % label + " | ".join(val(d[c], k) for c in CLASSES) + " |")
    return "\n".join(rows)


def hashed_block():
    d = classes()
    rows = ["| Unnamed field | Settings offset | " + " | ".join(CLASSES) + " |", "|---|---|" + "---|" * len(CLASSES)]
    for k, off in HASHED:
        rows.append("| `%s` | `%s` | " % (k, off) + " | ".join(val(d[c], k) for c in CLASSES) + " |")
    return "\n".join(rows)


def blocks():
    return {"curves": curves_block(), "classes": classes_block(), "hashed": hashed_block()}


def main():
    b = blocks()
    a = sys.argv[1:]
    if a and a[0] in b:
        print(b[a[0]])
        return 0
    text = open(PAGE, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    new = BLOCK.sub(lambda m: "<!-- aim_assist %s -->\n%s\n<!-- /aim_assist -->" % (m.group(1), b[m.group(1)]), text)
    new = link_source_output(new)
    if "--check" in a:
        if new != text:
            print("stale: " + PAGE)
            return 1
        print("ok")
        return 0
    if "--write" in a:
        open(PAGE, "w", encoding="utf-8", newline="\n").write(new)
        print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
