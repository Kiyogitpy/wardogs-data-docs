"""Tables for the Challenges KOTH page, built from assets/data/challenge-statetrees.json (round 86).

The JSON is written by _tools/statetree_outline.py from the compiled StateTree assets. Blocks in
game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md:

    <!-- statetree_tables MODE -->  ...  <!-- /statetree_tables -->

    python -I _tools/statetree_tables.py --write   # refresh every block in place (idempotent)
    python -I _tools/statetree_tables.py --check   # exit 1 if a block is stale
    python -I _tools/statetree_tables.py MODE      # print one block: rules, inputs, magnet

Modes: rules (which condition adds each Challenges.Context.* tag), inputs (what feeds Calculate Reward in each tree
family), magnet (the three Hot Zone Magnet trees).
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data", "challenge-statetrees.json")
PAGE = "game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md"
BLOCK = re.compile(r"<!-- statetree_tables (\w+) -->\r?\n.*?<!-- /statetree_tables -->", re.S)
PREFIX = "ST_Challenges_SessionEvents_"
# Conditions that only choose which actor is tested are shown without the actor binding.
SHOW_BINDING = {"Float Compare", "Integer Compare"}


def short(t):
    return t.replace(PREFIX, "")


def src(b):
    return b.split("<-", 1)[1].strip().replace("Parameters.", "").replace(".Output", "")


def fmt_list(v, limit=6):
    items = [str(x) for x in v]
    if len(items) > limit:
        return ", ".join(items[:limit]) + ", … (%d in all)" % len(items)
    return ", ".join(items)


def cond(c):
    name = c["name"]
    parts = []
    for k, v in (c.get("values") or {}).items():
        if k == "bInvert":
            continue
        parts.append("%s %s" % (k, fmt_list(v) if isinstance(v, list) else v))
    if c.get("operator"):
        parts.insert(0, c["operator"])
    if name in SHOW_BINDING:
        for b in c.get("bindings", []):
            parts.append("%s from %s" % (b.split("<-")[0].strip(), src(b)))
    txt = name + ("(" + "; ".join(parts) + ")" if parts else "")
    if c.get("bInvert") or (c.get("values") or {}).get("bInvert"):
        txt = "not " + txt
    return txt


def conds(cs):
    out = ""
    for i, c in enumerate(cs):
        op = c.get("op", "And")
        if i:
            out += " " + ("or" if op == "Or" else "and") + " "
        out += cond(c)
    return out


def rules(trees):
    sig = collections.defaultdict(set)
    for t, o in trees.items():
        for s in o["states"]:
            tags = [x["values"]["AddTag"] for x in s.get("tasks", []) if x["name"] == "Add Context Tags" and x.get("values", {}).get("AddTag")]
            if tags and s.get("conditions"):
                sig[(tags[0], conds(s["conditions"]))].add(t)
    rows = ["| Context tag | Added when | Trees |", "|---|---|---:|"]
    for (tag, c), ts in sorted(sig.items(), key=lambda x: (x[0][0], -len(x[1]), x[0][1])):
        rows.append("| `%s` | %s | %d |" % (tag, c.replace("|", "/"), len(ts)))
    return "\n".join(rows)


def inputs(trees):
    sig = collections.defaultdict(list)
    for t, o in trees.items():
        for s in o["states"]:
            for k in s.get("tasks", []):
                if k["name"] != "Calculate Reward" or not k.get("inputs"):
                    continue
                srcs = [src(b) for b in k.get("bindings", []) if b.startswith("Inputs.")]
                sig[(", ".join(k["inputs"]), ", ".join(srcs) or "(set by a state task, not a parameter)")].append(short(t))
    rows = ["| Inputs to `Calculate Reward` | Bound from | Trees | Examples |", "|---|---|---:|---|"]
    for (ins, bound), ts in sorted(sig.items(), key=lambda x: (-len(x[1]), x[0])):
        ex = ", ".join("`%s`" % x for x in sorted(set(ts))[:3])
        rows.append("| %s | %s | %d | %s |" % (ins, bound, len(ts), ex))
    return chr(10).join(rows)


def magnet(trees):
    rows = ["| Tree | Event it waits for | Context tags it can add | Reward formula inputs |", "|---|---|---|---|"]
    for t in sorted(trees):
        if "HotZoneMagnet" not in t:
            continue
        o = trees[t]
        ev = next((s["enter_event"] for s in o["states"] if "enter_event" in s), "")
        tags = [x["values"]["AddTag"] for s in o["states"] for x in s.get("tasks", []) if x.get("values", {}).get("AddTag")]
        ins = [i for s in o["states"] for x in s.get("tasks", []) for i in x.get("inputs", [])]
        rows.append("| `%s` | `%s` | %s | %s |" % (short(t), ev, ", ".join("`%s`" % x for x in tags), ", ".join(ins) or "none"))
    return chr(10).join(rows)


MODES = {"rules": rules, "inputs": inputs, "magnet": magnet}


def main():
    args = sys.argv[1:]
    trees = json.load(open(DATA, encoding="utf-8"))["trees"]
    path = os.path.join(ROOT, PAGE)
    text = open(path, encoding="utf-8", newline="").read()
    if args and args[0] in MODES:
        print(MODES[args[0]](trees))
        return 0

    def sub(m):
        return "<!-- statetree_tables %s -->\n%s\n<!-- /statetree_tables -->" % (m.group(1), MODES[m.group(1)](trees))
    new = BLOCK.sub(sub, text)
    if "--check" in args:
        print("up to date" if new == text else "DIFFERS")
        return 0 if new == text else 1
    if "--write" in args and new != text:
        open(path, "w", encoding="utf-8", newline="").write(new)
    print("%d blocks" % len(BLOCK.findall(new)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
