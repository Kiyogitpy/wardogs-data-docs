"""Parameter table for the AI environment queries (EQS), for game-features/Wardogs_GameFeatures_AI_v2.md section 9.1.

Reads assets/data/ai-eqs.json (built by _tools/ai_eqs.py) and prints one Markdown table row per query option:
the generator with its radii, ring count, spacing and arc, and each test with filter, limits, scoring equation and
factor. Values the data takes from a provider (AI config radius, weapon range, volume size, goal distance) are
shown as the provider field, with the stored default when there is one. Unit: Unreal units (centimetres). The block
sits between

    <!-- ai_eqs_table params -->  ...  <!-- /ai_eqs_table -->

    python -I _tools/ai_eqs_table.py --write   # refresh the block in place
    python -I _tools/ai_eqs_table.py --check   # exit 1 when the block is stale
    python -I _tools/ai_eqs_table.py           # print the block

Stdlib only; idempotent.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "data", "ai-eqs.json")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_GameFeatures_AI_v2.md")
BLOCK = re.compile(r"<!-- ai_eqs_table params -->\r?\n.*?<!-- /ai_eqs_table -->", re.S)

GEN_KEYS = ["CenterContext", "Center", "Radius", "InnerRadius", "OuterRadius", "NumberOfRings", "DistanceBetweenPoints",
            "ArcAngle", "OnlyFreeCovers", "IncludeReservedByMe", "SenseToUse"]
TEST_KEYS = ["TestPurpose", "FilterType", "TestMode", "DistanceTo", "FloatValueMin", "FloatValueMax", "ScoringEquation",
             "ScoringFactor", "BoolValue"]


def short(s):
    s = str(s)
    for p in ("EnvQueryContext_", "EQS_Context_", "BP_EnvQueryContext_", "TestPurpose.", "TestFilterType.",
              "TestScoreEquation.", "TestDot.", "TestPathfinding.", "TestDistance.", "EAIConfigDataField.",
              "EAIWeaponDataField.", "ESDAIGoalDataProviderTargetType."):
        s = s.replace(p, "")
    return s[:-2] if s.endswith("_C") else s


def val(v):
    if isinstance(v, dict):
        frm = v.get("from")
        d = v.get("default")
        dtxt = " (default %g)" % d if isinstance(d, (int, float)) else ""
        if isinstance(frm, dict):
            prov = short(frm.get("provider", "provider")).replace("WDAIDataProvider_", "").replace(
                "SDAIGoalDataProvider_", "Goal")
            args = []
            for k, x in frm.items():
                if k == "provider":
                    continue
                args.append("composite" if isinstance(x, (dict, list)) else short(x))
            return "%s(%s)%s" % (prov, ", ".join(args), dtxt)
        return "provider%s" % dtxt
    if isinstance(v, float) and v == int(v):
        return "%d" % int(v)
    return short(v)


def gen_text(g):
    out = [short(g["type"]).replace("SDEnvQueryGenerator_", "").replace("EnvQueryGenerator_", "")]
    for k in GEN_KEYS:
        if k in g:
            out.append("%s %s" % (k, val(g[k])))
    return ", ".join(out)


def test_text(t):
    out = [short(t["type"]).replace("EnvQueryTest_", "").replace("WDEnvQueryTest_", "WD")]
    for k in TEST_KEYS:
        if k in t:
            n = {"TestPurpose": "", "FilterType": "", "TestMode": "", "DistanceTo": "to ", "FloatValueMin": "min ",
                 "FloatValueMax": "max ", "ScoringEquation": "", "ScoringFactor": "x", "BoolValue": "bool "}[k]
            out.append(n + val(t[k]))
    return " ".join(out)


def block():
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    rows = ["| Query | Option | Generator (Unreal units) | Tests (in listed order) |", "|---|---|---|---|"]
    qs = d["queries"]
    items = sorted(qs.items()) if isinstance(qs, dict) else sorted(qs)
    for name, opts in items:
        for i, o in enumerate(opts, 1):
            tests = "; ".join(test_text(t) for t in o["tests"]) or "-"
            rows.append("| `%s` | %d | %s | %s |" % (name, i, gen_text(o["generator"]).replace("|", "/"),
                                                    tests.replace("|", "/")))
    return "<!-- ai_eqs_table params -->\n" + "\n".join(rows) + "\n<!-- /ai_eqs_table -->"


def main():
    new = block()
    if "--write" in sys.argv or "--check" in sys.argv:
        with open(PAGE, encoding="utf-8", newline="") as f:
            t = f.read()
        if not BLOCK.search(t):
            print("marker block missing in", PAGE)
            return 1
        nt = BLOCK.sub(lambda m: new.replace("\n", "\r\n") if "\r\n" in t else new, t, count=1)
        if "--check" in sys.argv:
            if nt != t:
                print("stale: run python -I _tools/ai_eqs_table.py --write")
                return 1
            print("ok")
            return 0
        with open(PAGE, "w", encoding="utf-8", newline="") as f:
            f.write(nt)
        print("written")
        return 0
    print(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
