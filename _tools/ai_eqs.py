"""Build assets/data/ai-eqs.json: every AI Environment Query (EQS) asset, resolved.

    python -I _tools/ai_eqs.py [--check] [<round36_ai dir>]

Reads <dir>/dump/EQS_*.json and the BP_EnvQueryContext_* assets (WdExtract dump of the
WDAIPvEAICore / AI game feature plugins, round 36). For each query lists its options; for each
option the generator and the tests (type, purpose, filter, scoring equation, values), with data
providers (weapon range, AI config radius, distance, composite) resolved to their field name.
Idempotent. With --check, exits 1 if the committed file differs. Exits 0 if input is absent.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "ai-eqs.json")
SKIP = {"VerNum", "VersionNum", "bUpdatedToUseQuery"}


def objname(v):
    m = re.search(r"'([^']*)'", v.get("ObjectName", ""))
    n = m.group(1) if m else v.get("ObjectName", "")
    return n.split(":")[-1].split(".")[-1]


def main():
    check = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else r"E:/Reverse_Engineer/wardogs_analysis/round36_ai"
    d = os.path.join(base, "dump")
    if not os.path.isdir(d):
        print(f"input not found ({base}); skipping")
        return 0

    def simplify(v, objs):
        if isinstance(v, dict):
            if "ObjectName" in v and "ObjectPath" in v:
                n = objname(v)
                o = objs.get(n)
                if o is not None and ("Provider" in o["Type"] or "SDComposite" in o["Type"]):
                    return {"provider": o["Type"], **{k: simplify(x, objs) for k, x in o.get("Properties", {}).items() if k not in SKIP}}
                return n
            if "AssetPathName" in v:
                return v["AssetPathName"]
            if "DataBinding" in v:
                b = v.get("DataBinding")
                r = {}
                if "DefaultValue" in v:
                    r["default"] = v["DefaultValue"]
                if b:
                    n = objname(b)
                    o = objs.get(n)
                    r["from"] = simplify(b, objs) if o is None else {"provider": o["Type"], **{k: simplify(x, objs) for k, x in o.get("Properties", {}).items() if k not in SKIP}}
                    r["field"] = v.get("DataField")
                return r
            if "DefaultValue" in v and len(v) <= 2:
                return v["DefaultValue"]
            return {k: simplify(x, objs) for k, x in v.items() if k not in SKIP}
        if isinstance(v, list):
            return [simplify(x, objs) for x in v]
        if isinstance(v, str):
            return v.replace("EEnv", "").replace("::", ".")
        return v

    queries = {}
    for f in sorted(glob.glob(os.path.join(d, "EQS_*.json"))):
        doc = json.load(open(f, encoding="utf-8"))
        objs = {o["Name"]: o for o in doc}
        q = next((o for o in doc if o["Type"] == "EnvQuery"), None)
        if q is None:
            continue
        opts = []
        for ref in q["Properties"].get("Options", []):
            op = objs.get(objname(ref))
            if not op:
                continue
            gen = objs.get(objname(op["Properties"]["Generator"])) if "Generator" in op["Properties"] else None
            entry = {}
            if gen:
                entry["generator"] = {"type": gen["Type"], **{k: simplify(x, objs) for k, x in gen.get("Properties", {}).items() if k not in SKIP}}
            tests = []
            for t in op["Properties"].get("Tests", []):
                to = objs.get(objname(t))
                if to:
                    tests.append({"type": to["Type"], **{k: simplify(x, objs) for k, x in to.get("Properties", {}).items() if k not in SKIP}})
            entry["tests"] = tests
            opts.append(entry)
        queries[q["Name"]] = opts
    contexts = {}
    for f in sorted(glob.glob(os.path.join(d, "BP_EnvQueryContext_*.json")) + glob.glob(os.path.join(d, "EQS_Context_*.json"))):
        doc = json.load(open(f, encoding="utf-8"))
        for o in doc:
            if o["Name"].startswith("Default__"):
                contexts[o["Name"][9:-2]] = {k: simplify(x, {}) for k, x in o.get("Properties", {}).items()}
    out = {"source": "round 41 cooked-data read of round36_ai/dump (EQS_* and EQS context assets)", "queries": queries, "contexts": contexts}
    text = json.dumps(out, indent=1, sort_keys=True) + "\n"
    if check:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("ok" if cur == text else "DIFFERS")
        return 0 if cur == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {OUT}: {len(queries)} queries, {len(contexts)} contexts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
