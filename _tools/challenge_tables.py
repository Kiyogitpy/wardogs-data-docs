"""Tables for game-features/Wardogs_Challenges_v1.md, rebuilt from data/.

Reads every challenge definition table (WDChallengeDefinition rows), every StateTree asset
(ST_*.json), the session-event reward formula tables (DT_ChallengeRewards_SessionEvents_*) and the
reward lookup tables (DT_RewardLookup_SessionEvent_*). Each table sits between

    <!-- challenge_tables MODE -->  ...  <!-- /challenge_tables -->

on the page. Rerun after a data update (idempotent):

    python _tools/challenge_tables.py --write       # refresh every block in place
    python _tools/challenge_tables.py MODE          # print one block (counts, definitions, events,
                                                    #   rewards, lookups, conditions, trees,
                                                    #   kothfiles, orphans)

How a tree is read (Derived from the StateTree export, no engine code needed):
  States    -> Name, Parent, TasksBegin/TasksNum, TransitionsBegin/Num, RequiredEventToEnter.
  Nodes     -> one flat list; a node with an "Operand" key is a condition, every other node is a
               task or evaluator (the export drops the class name, only the display Name is kept).
  Instances -> DefaultInstanceData / SharedInstanceData hold the per-node settings: reward tag,
               calculator inputs, lookup registry name, cooldown, delay, stat updates, XP tags.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PAGE = "game-features/Wardogs_Challenges_v1.md"
REPO = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/"
KOTH = "Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/"
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
BLOCK = re.compile(r"<!-- challenge_tables (\w+) -->\r?\n.*?<!-- /challenge_tables -->", re.S)


def exports(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(part) for part in EXPORT.split(f.read())[1:]]


def rel_of(path):
    return os.path.relpath(path, DATA).replace("\\", "/")


def link(rel, label=None):
    return f"[`{label or os.path.basename(rel)[:-5]}`]({REPO}{rel})"


def n(x):
    x = float(x)
    return f"{x:,.0f}" if x == int(x) else f"{x:,.2f}".rstrip("0").rstrip(".")


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def tag(obj):
    if isinstance(obj, dict):
        t = obj.get("TagName")
        return t if t and t != "None" else None
    return None


def objname(obj):
    if not isinstance(obj, dict) or not obj.get("ObjectName"):
        return None
    name = obj["ObjectName"]
    return name.split("'")[1] if "'" in name else name


def tags_in(o):
    """Every non-None TagName string under o, in file order."""
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "TagName" and isinstance(v, str) and v != "None":
                out.append(v)
            else:
                out += tags_in(v)
    elif isinstance(o, list):
        for v in o:
            out += tags_in(v)
    return out


def uniq(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


# --- load ---------------------------------------------------------------------------------------

def load():
    d = {"trees": {}, "defs": [], "formula": {}, "lookup": {}}
    for root, _, files in os.walk(DATA):
        for fn in sorted(files):
            if fn.startswith("ST_") and fn.endswith(".json"):
                path = os.path.join(root, fn)
                for e in exports(path):
                    if e["Type"] == "StateTree":
                        d["trees"][e["Name"]] = (rel_of(path), e["Properties"])
    # challenge definition tables: every DataTable whose row struct is WDChallengeDefinition
    for path in sorted(glob.glob(os.path.join(DATA, "**", "DT_*.json"), recursive=True)):
        base = os.path.basename(path)
        if not (base.startswith("DT_Challenges_") or base.startswith("DT_Passive") or base.startswith("DT_Wager")):
            continue
        for e in exports(path):
            if e.get("Type") == "DataTable" and objname(e["Properties"].get("RowStruct")) == "WDChallengeDefinition":
                for key, row in e["Rows"].items():
                    d["defs"].append((rel_of(path), e["Name"], key, row))
    for path in glob.glob(os.path.join(DATA, "**", "DT_ChallengeRewards_SessionEvents_*.json"), recursive=True):
        for e in exports(path):
            if e.get("Type") == "DataTable":
                for key, row in e["Rows"].items():
                    d["formula"][key] = (rel_of(path), e["Name"], row)
    for path in glob.glob(os.path.join(DATA, "**", "DT_RewardLookup_SessionEvent_*.json"), recursive=True):
        for e in exports(path):
            if e.get("Type") == "DataTable":
                d["lookup"][e["Name"]] = (rel_of(path), e["Rows"])
    d["tree_to_def"] = {}
    for rel, tname, key, row in d["defs"]:
        ref = (row.get("StateTreeReference") or {}).get("StateTree")
        if ref:
            d["tree_to_def"].setdefault(objname(ref), []).append((rel, tname, key, row))
    return d


# --- reading one tree ---------------------------------------------------------------------------

def nodes_of(p):
    return p["Nodes"]["Structs"]


def is_condition(node):
    return "Operand" in node


def instance_structs(p):
    out = []
    for blk in ("DefaultInstanceData", "SharedInstanceData"):
        if blk in p:
            out += p[blk]["Data"]["InstanceStructs"]["Structs"]
    return out


def listens(p):
    """Events the tree reacts to: (tag, payload class), from listen tasks, state gates and transitions."""
    found = []
    for node in nodes_of(p):
        if "EventType" in node:
            found.append((tag(node.get("StateTreeEventTag")), objname(node["EventType"])))
    for st in p["States"]:
        r = st.get("RequiredEventToEnter") or {}
        if tag(r.get("Tag")):
            found.append((tag(r["Tag"]), objname(r.get("PayloadStruct"))))
    for tr in p["Transitions"]:
        r = tr.get("RequiredEvent") or {}
        if tag(r.get("Tag")):
            found.append((tag(r["Tag"]), objname(r.get("PayloadStruct"))))
    best = {}
    for t, pl in found:
        if t and (t not in best or (pl and not best[t])):
            best[t] = pl
    return list(best.items())


def branches(p):
    """Names of states that read 'On ...' (recipient or sub-event branches), minus the event gate itself."""
    return uniq([s["Name"] for s in p["States"] if s["Name"].startswith("On ") and not s["Name"].endswith("Event")])


def reward_nodes(p):
    """Calculate / grant tasks as (reward tag, kind, input names); lookup tasks as (registry, filters, fallback)."""
    calc, lookups = [], []
    for s in instance_structs(p):
        if "RegistryName" in s:
            lookups.append((s["RegistryName"], tuple(s.get("FilterTags", [])), tag(s.get("FallbackRewardTag"))))
        elif tag(s.get("TipTag")):
            calc.append((tag(s["TipTag"]), "tip", []))
        elif "RewardTag" in s and "Challenge" in s:
            t = tag(s["RewardTag"])
            if not t:
                continue
            kind = "calculate" if "Inputs" in s else "grant"
            calc.append((t, kind, [i["VariableName"] for i in s.get("Inputs", [])]))
    return calc, lookups


def settings(p):
    out = []
    for s in instance_structs(p):
        if isinstance(s.get("Cooldown"), (int, float)):
            out.append(f"repeat cooldown {n(s['Cooldown'])} s")
        if "Duration" in s and "RandomDeviation" in s:
            out.append(f"delay {n(s['Duration'])} s" + (" (runs forever)" if s.get("bRunForever") else ""))
        if tag(s.get("MatchStatTag")):
            out.append(f"match stat `{tag(s['MatchStatTag'])}` {s['DeltaChange']:+g}")
        if "Modifier" in s and "Operation" in s:
            out.append(f"progress counter {s['Operation'].split('::')[-1].lower()} {n(s['Modifier'])}")
        for k in ("FallbackRoleXPTag", "FallbackPlatformXPTag"):
            if tag(s.get(k)):
                out.append(f"fallback XP `{tag(s[k])}`")
        if s.get("AcceptedValues"):
            out.append("team-attitude filter " + "/".join(v.split("::")[-1] for v in s["AcceptedValues"]))
        if s.get("AcceptedVehicles"):
            out.append(f"{len(s['AcceptedVehicles'])} accepted vehicle tags")
    return uniq(out)


def condition_names(p):
    names = [x["Name"] for x in nodes_of(p) if is_condition(x)]
    return {k: names.count(k) for k in uniq(names)}


def task_names(p):
    names = [x["Name"] for x in nodes_of(p) if not is_condition(x)]
    return {k: names.count(k) for k in uniq(names)}


def code(items, empty="-", sep=", "):
    return sep.join(f"`{i}`" for i in items) if items else empty


# --- tables -------------------------------------------------------------------------------------

def counts(d):
    t = d["trees"]
    sess = [k for k in t if k.startswith("ST_Challenges_SessionEvents_")]
    koth = [k for k, v in t.items() if v[0].startswith(KOTH)]
    kfiles = glob.glob(os.path.join(DATA, KOTH, "**", "*.json"), recursive=True)
    nstates = sum(len(v[1]["States"]) for v in t.values())
    nnodes = sum(len(nodes_of(v[1])) for v in t.values())
    ncond = sum(1 for v in t.values() for x in nodes_of(v[1]) if is_condition(x))
    tables = sorted({(r, tn) for r, tn, _, _ in d["defs"]})
    reward_trees = sum(1 for v in t.values() if reward_nodes(v[1])[0] or reward_nodes(v[1])[1])
    with_tree = sum(1 for x in d["defs"] if (x[3].get("StateTreeReference") or {}).get("StateTree"))
    return "\n".join([
        f"- StateTree assets: **{len(t)}** (**{len(koth)}** under `Challenges_KOTH`, **{len(sess)}** named `ST_Challenges_SessionEvents_*`).",
        f"- Files under the `Challenges_KOTH` plugin content: **{len(kfiles)}** ({len(koth)} trees, "
        f"{sum(1 for k in kfiles if 'DT_RewardLookup' in k)} reward lookup tables, "
        f"{sum(1 for k in kfiles if os.path.basename(k).startswith('DT_Challenges'))} challenge table, "
        f"{sum(1 for k in kfiles if os.path.basename(k) == 'Challenges_KOTH.json')} feature file).",
        f"- Challenge definitions: **{len(d['defs'])}** rows in **{len(tables)}** tables; **{with_tree}** point at a StateTree.",
        f"- Trees that name a reward tag or a lookup registry: **{reward_trees}**.",
        f"- Across all trees: **{nstates}** states, **{nnodes}** nodes (**{ncond}** conditions, **{nnodes - ncond}** tasks and evaluators).",
        f"- Reward formula rows available to join: **{len(d['formula'])}** (in {len({v[1] for v in d['formula'].values()})} tables); "
        f"reward lookup tables: **{len(d['lookup'])}**.",
    ])


def definitions(d):
    out = ["| Challenge tag | UI name | Table | Auto-activates | Prerequisite | State tree | Tree parameters | Objective target | Direct reward |",
           "|---|---|---|---|---|---|---|---|---|"]
    for rel, tname, key, row in d["defs"]:
        ref = row.get("StateTreeReference") or {}
        tree = objname(ref.get("StateTree"))
        params = [x["Name"] for x in (ref.get("Parameters") or {}).get("PropertyDescs", [])]
        pre = ((row.get("Prerequisites") or {}).get("QueryDefinition") or {}).get("SharedDefinition") or {}
        prereq = []
        for s in (pre.get("Conditions") or {}).get("Structs", []):
            c = tag(s.get("ChallengeId"))
            if c:
                prereq.append(("not " if s.get("bInvert") else "") + "done: " + c)
        obj = ", ".join(f"`{tag(o['Key'])}` = {n(o['Value'])}" for o in row.get("Objectives", [])) or "-"
        rew = ", ".join(f"{n(r['Quantity'])} `{tag(r['RewardTag'])}`" for r in row.get("Rewards", [])) or "-"
        dn = row.get("DisplayName") or {}
        name = dn.get("SourceString") or dn.get("LocalizedString") or "(blank)"
        out.append(f"| `{key}` | {cell(name)} | {link(rel, tname)} | {'yes' if row.get('bAutoActivate') else 'no'} | "
                   f"{cell('; '.join(prereq)) or '-'} | {code([tree]) if tree else '-'} | {code(params)} | {obj} | {rew} |")
    return "\n".join(out)


def events(d):
    out = ["| State tree | Challenge | Listens for (event tag, payload) | Branches (states named `On ...`) | Settings in the tree |",
           "|---|---|---|---|---|"]
    for name, (rel, p) in sorted(d["trees"].items()):
        ev = "; ".join(f"`{t}`" + (f" ({pl})" if pl else "") for t, pl in listens(p)) or "none"
        rows_ = d["tree_to_def"].get(name, [])
        if len(rows_) <= 2:
            ch = ", ".join(f"`{x[2]}`" for x in rows_)
        else:
            groups = {}
            for x in rows_:
                groups[x[2].rsplit(".", 1)[0]] = groups.get(x[2].rsplit(".", 1)[0], 0) + 1
            ch = f"{len(rows_)} rows: " + ", ".join(f"`{g}.1` to `.{c}`" for g, c in groups.items())
        ch = ch or "none"
        out.append(f"| `{name}` | {ch} | {ev} | {code(branches(p))} | {cell('; '.join(settings(p))) or '-'} |")
    return "\n".join(out)


def literals(row, res_tag):
    for res in row["Resources"]:
        if tag(res["Key"]) == res_tag:
            return [(kv["Key"], kv["Value"]["LiteralValue"]) for kv in res["Value"]["Variables"]
                    if kv["Value"]["VariableType"].endswith("Literal")
                    and re.match(r"(Base|Default|Assist|Owner|Friendly)\w*(Reward|Value)$", kv["Key"])]
    return []


def rewards(d):
    out = ["| State tree | Step | Reward tag | Formula row in | Cash literals | Role XP literals | Calculator inputs |",
           "|---|---|---|---|---|---|---|"]
    missing = []
    for name, (rel, p) in sorted(d["trees"].items()):
        calc, _ = reward_nodes(p)
        merged = {}
        for t, kind, inputs in calc:
            m = merged.setdefault(t, [set(), []])
            m[0].add(kind)
            m[1].extend(inputs)
        for t, (kinds, inputs) in merged.items():
            f = d["formula"].get(t)
            if f:
                cash = literals(f[2], "Attribute.Meta.Currency.Cash")
                xp = literals(f[2], "Attribute.Meta.XP.Role")
                where = link(f[0], f[1])
                cashs = ", ".join(f"{k} {n(v)}" for k, v in cash) or "-"
                xps = ", ".join(f"{k} {n(v)}" for k, v in xp) or "-"
            else:
                where, cashs, xps = "(no row)", "-", "-"
                missing.append((name, t))
            out.append(f"| `{name}` | {'/'.join(sorted(kinds))} | `{t}` | {where} | {cell(cashs)} | {cell(xps)} | {code(uniq(inputs))} |")
    out.append("")
    base = sorted({t for _, t in missing if t.startswith("Challenges.")})
    ms = sorted({t for _, t in missing if not t.startswith("Challenges.")})
    out.append(f"Reward tags a tree names that have no row in any of the five formula tables ({len(missing)} tree and tag pairs): "
               f"{len(base)} `Challenges.Rewards.*` tags ({code(base)}) and {len(ms)} other tags ({code(ms)}). "
               "Several `Challenges.Rewards.*` ones are the parent tag of a family (the lookup tables supply variant tags); "
               "others (e.g. `ZoneEntry.SpawnVehicle`, `TeamOffence.*`) have no formula row at all. "
               "Whether the game pays anything for a tag without a row is not traced.")
    none_ = sorted(nm for nm, (rel, p) in d["trees"].items() if not reward_nodes(p)[0] and not reward_nodes(p)[1])
    out.append("")
    out.append(f"Trees with no reward tag and no lookup set in their instance data ({len(none_)}): {code(none_)}. "
               "For the event trees among them (e.g. `ST_Challenges_SessionEvents_KOTH_PlayerKill`) the reward tag is not a literal in the export, "
               "so it is bound at run time; not traced. The achievement, mission and wager trees do not pay through this path.")
    return "\n".join(out)


ALIASES = {"DestroyedBuildable": "BuildableDestroyed"}


def lookup_name(d, reg):
    """Lookup table for a registry name (Derived from the names: the export has no link between them)."""
    parts = reg.split(".")
    for cand in (ALIASES.get(parts[-1], parts[-1]), "_".join(parts[-2:])):
        if "DT_RewardLookup_SessionEvent_" + cand in d["lookup"]:
            return "DT_RewardLookup_SessionEvent_" + cand
    return "DT_RewardLookup_SessionEvent_" + parts[-1]


def lookups(d):
    out = ["| State tree | Registry name | Filter tags | Fallback reward tag | Lookup table | Rows | Rows whose reward tag has a formula row |",
           "|---|---|---|---|---|---|---|"]
    used = set()
    for name, (rel, p) in sorted(d["trees"].items()):
        _, lk = reward_nodes(p)
        for reg, filt, fb in uniq(lk):
            tn = lookup_name(d, reg)
            hit = d["lookup"].get(tn)
            if hit:
                used.add(tn)
                tags_ = [r["RewardTag"]["TagName"] for r in hit[1].values()]
                ok = sum(1 for t in tags_ if t in d["formula"])
                tbl, rows_, okc = link(hit[0], tn), str(len(tags_)), f"{ok} of {len(tags_)}"
            else:
                tbl, rows_, okc = "(no table with that name)", "-", "-"
            fbs = (f"`{fb}`" + ("" if fb in d["formula"] else " (no formula row)")) if fb else "-"
            out.append(f"| `{name}` | `{reg}` | {code(filt)} | {fbs} | {tbl} | {rows_} | {okc} |")
    unused = sorted(set(d["lookup"]) - used)
    out.append("")
    out.append("Lookup tables that no tree in this export points at by registry name: " +
               (", ".join(link(d["lookup"][u][0], u) for u in unused) if unused else "none") + ".")
    return "\n".join(out)


def conditions(d):
    out = ["| State tree | Conditions (name x count) | Context tags (`Challenges.Context.*`) | Other tags tested |",
           "|---|---|---|---|"]
    for name, (rel, p) in sorted(d["trees"].items()):
        cn = condition_names(p)
        alltags = uniq(tags_in(p))
        ctx = [t for t in alltags if t.startswith("Challenges.Context.")]
        other = [t for t in alltags if t.startswith(("State.", "Meta.Damage.", "ID.", "Id.", "Vehicle.", "Meta.Progression.Context."))]
        cs = ", ".join(f"`{k}` x{v}" if v > 1 else f"`{k}`" for k, v in cn.items()) or "none"
        out.append(f"| `{name}` | {cs} | {code(ctx)} | {code(other)} |")
    return "\n".join(out)


def trees(d):
    out = ["| State tree | Folder | States | Transitions | Conditions | Tasks and evaluators | Task names (x count) | Resource and event tags |",
           "|---|---|---|---|---|---|---|---|"]
    for name, (rel, p) in sorted(d["trees"].items()):
        folder = os.path.dirname(rel).replace("Wardogs/Plugins/GameFeatures/", "").replace("Wardogs/Content/", "").replace("/Content", "")
        tn = task_names(p)
        nc = sum(1 for x in nodes_of(p) if is_condition(x))
        res = [t for t in uniq(tags_in(p)) if t.startswith(("Attribute.", "Meta.Progression.Resources", "Event.StateTree.", "Analytics."))]
        out.append(f"| {link(rel, name)} | `{folder}` | {len(p['States'])} | {len(p['Transitions'])} | {nc} | {len(nodes_of(p)) - nc} | "
                   f"{cell(', '.join(f'{k} x{v}' if v > 1 else k for k, v in tn.items()))} | {code(res)} |")
    return "\n".join(out)


def kothfiles(d):
    base = os.path.join(DATA, KOTH)
    rows = {}
    for path in sorted(glob.glob(os.path.join(base, "**", "*.json"), recursive=True)):
        nm = os.path.basename(path)[:-5]
        if nm.startswith("ST_"):
            kind = "state tree"
        elif nm.startswith("DT_RewardLookup"):
            kind = "reward lookup table"
        elif nm.startswith("DT_Challenges"):
            kind = "challenge definition table"
        else:
            kind = "feature file (registers the lookup data registries)"
        rows.setdefault(kind, []).append(nm)
    out = ["| Kind | Files | Names |", "|---|---|---|"]
    for kind in ("feature file (registers the lookup data registries)", "challenge definition table", "reward lookup table", "state tree"):
        items = rows.get(kind, [])
        out.append(f"| {kind} | {len(items)} | " + ", ".join(f"`{nm}`" for nm in items) + " |")
    out.append("")
    out.append(f"Total: {sum(len(v) for v in rows.values())} files.")
    return "\n".join(out)


def orphans(d):
    out = []
    no_def = sorted(k for k in d["trees"] if k not in d["tree_to_def"])
    out.append("State trees that no challenge definition row points at: " +
               (", ".join(link(d["trees"][k][0], k) for k in no_def) if no_def else "none") + ".")
    out.append("")
    multi = {k: v for k, v in d["tree_to_def"].items() if len(v) > 1}
    out.append("State trees used by more than one challenge row: " +
               (", ".join(f"`{k}` ({len(v)} rows)" for k, v in sorted(multi.items())) if multi else "none") + ".")
    out.append("")
    missing = sorted(set(d["tree_to_def"]) - set(d["trees"]))
    out.append("Trees named by a challenge row but absent from the export: " + (code(missing) if missing else "none") + ".")
    return "\n".join(out)


MODES = {"counts": counts, "definitions": definitions, "events": events, "rewards": rewards, "lookups": lookups,
         "conditions": conditions, "trees": trees, "kothfiles": kothfiles, "orphans": orphans}


def write(d):
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, nothing written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = MODES[m.group(1)](d).split("\n")
        return nl.join([f"<!-- challenge_tables {m.group(1)} -->"] + body + ["<!-- /challenge_tables -->"])
    new, count = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = load()
    args = sys.argv[1:]
    if "--write" in args:
        write(d)
    else:
        print(MODES[next((a for a in args if a in MODES), "counts")](d))


if __name__ == "__main__":
    main()
