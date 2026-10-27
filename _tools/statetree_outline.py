"""Decode compiled StateTree assets into a readable outline (round 86).

A cooked `StateTree` keeps its states, transitions and node list as flat arrays and its parameter flow as copy
batches. Nothing is bytecode: the editor graph is lost, but every state, every transition (trigger, required event,
target, conditions), every task and condition node (editor name, instance-data values) and every property binding
(source struct and path -> target path) survives. This tool resolves those arrays into an outline and writes
assets/data/challenge-statetrees.json.

Dumps come from the extractor written OUTSIDE this repository:

    WdExtract <Paks> <keyfile> <usmap> <dumpdir> <oo2core> list ST_Challenges
    WdExtract <Paks> <keyfile> <usmap> <dumpdir> <oo2core> dump <dumpdir>/files.txt

Run (idempotent):

    python -I _tools/statetree_outline.py              # read DUMP_DIR if present, rewrite the JSON
    python -I _tools/statetree_outline.py --dump DIR   # another dump folder
    python -I _tools/statetree_outline.py --check      # exit 1 if the committed JSON differs
    python -I _tools/statetree_outline.py --text NAME  # print one tree as indented text (debug)

If the dump folder is absent the committed JSON is left untouched.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "challenge-statetrees.json")
DUMP_DIR = "E:/Reverse_Engineer/wardogs_analysis/round86_bp/dump_st"
NONE = 65535


def tag(v):
    return v.get("TagName") if isinstance(v, dict) and "TagName" in v else v


def simple(v):
    """Keep only scalar settings of an instance struct: tags, numbers, bools, strings. Drop nulls and empties."""
    out = {}
    for k, x in (v or {}).items():
        if x is None or x == [] or x == {}:
            continue
        if isinstance(x, dict):
            if "TagName" in x:
                if x["TagName"] != "None":
                    out[k] = x["TagName"]
            elif "RefAccessIndex" in x or "Parameters" in x or "Challenge" in x or "PropertyDescs" in x:
                continue
            elif len(x) <= 4 and all(not isinstance(y, (dict, list)) or "TagName" in (y or {}) for y in x.values()):
                s = simple(x)
                if s:
                    out[k] = s
        elif isinstance(x, list):
            items = [tag(y) if isinstance(y, dict) else y for y in x if (isinstance(y, dict) and "TagName" in y) or isinstance(y, (str, int, float))]
            if items:
                out[k] = items
        else:
            out[k] = x
    return out


def seg(path):
    return ".".join(s.get("Name", "?") for s in (path or {}).get("Segments", []))


class Tree:
    def __init__(self, p):
        self.p = p
        self.states = p.get("States", [])
        self.trans = p.get("Transitions", [])
        self.nodes = (p.get("Nodes") or {}).get("Structs", [])
        self.inst = self._structs(p.get("DefaultInstanceData"), True)
        self.shared = self._structs(p.get("SharedInstanceData"), True)
        self.evals = self._structs(p.get("DefaultEvaluationScopeInstanceData"), False)
        self.pb = p.get("PropertyBindings") or {"SourceStructs": [], "CopyBatches": [], "PropertyPathBindings": []}
        self.src = self.pb["SourceStructs"]
        self.src_by_handle = {}
        for s in self.src:
            h = s["DataHandle"]
            self.src_by_handle[(h["Source"], h["Index"], h["StateHandle"]["Index"])] = s["Name"]

    @staticmethod
    def _structs(v, wrapped):
        v = (v or {})
        if wrapped:
            v = v.get("Data", {})
        return v.get("InstanceStructs", {}).get("Structs", [])

    def srcname(self, h):
        k = (h["Source"], h["Index"], h["StateHandle"]["Index"])
        if k in self.src_by_handle:
            return self.src_by_handle[k]
        return h["Source"].split("::")[-1] + ("[%d]" % h["Index"] if h["Index"] != NONE else "")

    def bindings(self, batch):
        b = batch["Value"] if isinstance(batch, dict) else batch
        if b == NONE or b is None or b >= len(self.pb["CopyBatches"]):
            return []
        cb = self.pb["CopyBatches"][b]
        out = []
        for i in range(cb["BindingsBegin"]["Value"], cb["BindingsEnd"]["Value"]):
            pbind = self.pb["PropertyPathBindings"][i]
            sp = seg(pbind["SourcePropertyPath"])
            out.append("%s <- %s%s" % (seg(pbind["TargetPropertyPath"]), self.srcname(pbind["SourceDataHandle"]),
                                       "." + sp if sp else ""))
        return out

    def values(self, n, kind):
        t = n["InstanceTemplateIndex"]["Value"]
        arr = {"task": self.inst, "cond": self.shared, "eval": self.evals}[kind]
        if t == NONE or t >= len(arr):
            return {}
        return simple(arr[t])

    def node(self, i, kind):
        n = self.nodes[i]
        d = {"name": n.get("Name")}
        if n.get("EventType"):
            d["event_type"] = n["EventType"]["ObjectName"].split("'")[1]
        if n.get("StateTreeEventTag"):
            d["event"] = tag(n["StateTreeEventTag"])
        v = self.values(n, kind)
        if v:
            d["values"] = v
        if kind == "cond":
            op = n.get("Operand", "").split("::")[-1]
            if op:
                d["op"] = op
            if n.get("Operator"):
                d["operator"] = n["Operator"].split("::")[-1]
            for k in ("bInvert", "bExactMatch"):
                if n.get(k):
                    d[k] = True
        if kind == "task" and n.get("Name") == "Calculate Reward":
            t = n["InstanceTemplateIndex"]["Value"]
            ins = [i.get("VariableName") for i in (self.inst[t].get("Inputs") or [])] if t < len(self.inst) else []
            if ins:
                d["inputs"] = ins
        b = self.bindings(n.get("BindingsBatch"))
        if b:
            d["bindings"] = b
        extra = {k: x for k, x in n.items() if k.startswith("_aaa")}
        if extra:
            d["native_fields"] = extra
        return d

    def outline(self):
        states = []
        for i, s in enumerate(self.states):
            d = {"index": i, "name": s["Name"], "depth": s["Depth"], "parent": s["Parent"]["Index"]
                 if s["Parent"]["Index"] != NONE else None}
            d["select"] = s["SelectionBehavior"].split("::")[-1]
            ev = s["RequiredEventToEnter"]
            if tag(ev["Tag"]) != "None":
                d["enter_event"] = tag(ev["Tag"])
            if s["EnterConditionsNum"]:
                d["conditions"] = [self.node(j, "cond") for j in range(s["EnterConditionsBegin"], s["EnterConditionsBegin"] + s["EnterConditionsNum"])]
            if s["TasksNum"]:
                d["tasks"] = [self.node(j, "task") for j in range(s["TasksBegin"], s["TasksBegin"] + s["TasksNum"])]
            tr = []
            for j in range(s["TransitionsBegin"], s["TransitionsBegin"] + s["TransitionsNum"]):
                t = self.trans[j]
                x = {"trigger": t["Trigger"].split("::")[-1]}
                if tag(t["RequiredEvent"]["Tag"]) != "None":
                    x["event"] = tag(t["RequiredEvent"]["Tag"])
                tgt = t["State"]["Index"]
                x["to"] = self.states[tgt]["Name"] if tgt != NONE and tgt < len(self.states) else "(%d)" % tgt
                fb = t["FallBack"].split("::")[-1]
                if fb != "None":
                    x["fallback"] = fb
                if t["ConditionsNum"]:
                    x["conditions"] = [self.node(k, "cond") for k in range(t["ConditionsBegin"], t["ConditionsBegin"] + t["ConditionsNum"])]
                if t["Delay"]["Duration"]:
                    x["delay"] = t["Delay"]["Duration"]
                tr.append(x)
            if tr:
                d["transitions"] = tr
            states.append(d)
        params = []
        for pd in (self.p.get("Parameters") or {}).get("PropertyDescs", []):
            params.append(pd.get("Name"))
        evals = []
        for i, n in enumerate(self.nodes):
            if n.get("InstanceDataHandle", {}).get("Source") == "EStateTreeDataSourceType::EvaluationScopeInstanceData":
                evals.append(self.node(i, "eval"))
        out = {"states": states}
        if params:
            out["parameters"] = params
        if evals:
            out["property_functions"] = evals
        return out


def trees(dump):
    res = {}
    for f in sorted(glob.glob(os.path.join(dump, "ST_*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        st = [e for e in d if e.get("Type") == "StateTree"]
        if not st:
            continue
        name = os.path.basename(f)[:-5]
        res[name] = Tree(st[0]["Properties"]).outline()
    return res


def render(name, o):
    lines = [name]
    for s in o["states"]:
        ind = "  " * (s["depth"] + 1)
        lines.append("%s[%d] %s%s" % (ind, s["index"], s["name"], "  (on %s)" % s["enter_event"] if "enter_event" in s else ""))
        for c in s.get("conditions", []):
            lines.append("%s    if %s %s%s%s %s %s" % (ind, c.get("op", ""), "NOT " if c.get("bInvert") else "", c["name"], " " + c["operator"] if "operator" in c else "", c.get("values", ""), c.get("bindings", "")))
        for t in s.get("tasks", []):
            lines.append("%s    do %s %s %s" % (ind, t["name"], t.get("values", ""), t.get("bindings", "")))
        for t in s.get("transitions", []):
            lines.append("%s    -> %s on %s %s" % (ind, t["to"], t["trigger"], t.get("event", "")))
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    dump = args[args.index("--dump") + 1] if "--dump" in args else DUMP_DIR
    if not os.path.isdir(dump):
        print("dump folder absent (%s): keeping the committed %s" % (dump, os.path.relpath(OUT, ROOT)))
        return 0
    res = trees(dump)
    if "--text" in args:
        n = args[args.index("--text") + 1]
        for k, v in res.items():
            if n in k:
                print(render(k, v))
        return 0
    doc = {"meta": {"source": "StateTree assets (ST_Challenges_*) exported with tools/cue4parse_extractor (dump mode), "
                              "decoded by _tools/statetree_outline.py (round 86)", "count": len(res)},
           "trees": res}
    text = json.dumps(doc, separators=(",", ":"), ensure_ascii=False) + "\n"
    if "--check" in args:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("up to date" if cur == text else "DIFFERS")
        return 0 if cur == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote %d trees" % len(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
