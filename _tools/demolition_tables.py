"""Tables for content/Wardogs_DemolitionAssets_v1.md: the Wardogs/Content/Demolition folder, rebuilt from data/.

Reads every BHDemolitionDataAsset (DA_Demolition_*), component settings, remnant-mesh assets and ruleset
(BH_Demolition_RS_*). Rulesets are resolved recursively (Or / Ruleset-reference rules) into an effective rule set.
Blocks sit between

    <!-- demolition_tables MODE -->  ...  <!-- /demolition_tables -->

    python _tools/demolition_tables.py --write      # refresh every block in place
    python _tools/demolition_tables.py --check      # exit 1 when a block is stale
    python _tools/demolition_tables.py MODE         # print one block (counts, assets, meshes, remnants, settings,
                                                    #   rules, ruleuse, crosstalk, vfx)
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "content/Wardogs_DemolitionAssets_v1.md"
BLOCK = re.compile(r"<!-- demolition_tables (\w+) -->\r?\n.*?<!-- /demolition_tables -->", re.S)
IDENT = {"Rotation": {"X": 0.0, "Y": 0.0, "Z": 0.0, "W": 1.0}, "Translation": {"X": 0.0, "Y": 0.0, "Z": 0.0},
         "Scale3D": {"X": 1.0, "Y": 1.0, "Z": 1.0}}


def short(path):
    """Asset name from an object path, AssetPathName or quoted ObjectName."""
    s = str(path)
    m = re.search(r"'([^']+)'", s)
    if m:
        s = m.group(1)
    return s.split("/")[-1].split(".")[0]


def objref(o):
    if not o:
        return None
    return short(o.get("ObjectName") or o.get("ObjectPath") or o.get("AssetPathName"))


def load():
    d = {"assets": {}, "settings": {}, "remnants": {}, "rulesets": {}, "tagrefs": collections.defaultdict(set)}
    for f in sorted(glob.glob(os.path.join(DATA, "Wardogs", "Content", "Demolition", "**", "*.json"), recursive=True)):
        rel = ct.rel_of(f)
        ex = ct.exports(f)
        top = next((e for e in ex if e["Type"] == "BHDemolitionRuleset"), ex[0])
        name = top["Name"]
        if top["Type"] == "BHDemolitionDataAsset":
            d["assets"][name] = {"rel": rel, "p": top["Properties"]}
        elif top["Type"] == "BHDemolitionComponentSettings":
            d["settings"][name] = {"rel": rel, "p": top["Properties"]}
        elif top["Type"] == "BHDemolitionRemnantMeshesAsset":
            d["remnants"][name] = {"rel": rel, "p": top["Properties"]}
        elif top["Type"] == "BHDemolitionRuleset":
            d["rulesets"][name] = {"rel": rel, "list": ex, "top": top}
    pat = os.path.join(DATA, "Wardogs", "Content", "Audio", "Events", "Prop", "PropDemolition", "*.json")
    for f in glob.glob(pat):
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        for t in set(re.findall(r"Audio\.Event\.Prop\.Demolition\.\w+", text)):
            d["tagrefs"][t].add(ct.rel_of(f))
    return d


def sub_ref(rs, r):
    """Export a rule reference points at: the ObjectPath suffix .N is the export's index in the file."""
    return rs["list"][int(r["ObjectPath"].rsplit(".", 1)[1])]


def resolve(d, name):
    """Effective rule set of a ruleset: explosions {tag: mindist}, vehicles list, buildable flag, direct children."""
    rs = d["rulesets"][name]
    out = {"expl": {}, "veh": [], "build": False, "overlap": set(), "block": set(), "kids": []}

    def walk(e):
        t = e["Type"]
        p = e.get("Properties", {})
        if t == "BHDemolitionRuleset":
            r = p.get("Rule")
            if r:
                walk(sub_ref(rs, r))
        elif t == "BHDemolitionRule_Or":
            for r in p.get("Rules", []):
                walk(sub_ref(rs, r))
        elif t == "BHDemolitionRule_Ruleset":
            child = objref(p["Ruleset"])
            out["kids"].append(child)
            sub = resolve(d, child)
            for k, v in sub["expl"].items():
                out["expl"][k] = min(v, out["expl"].get(k, v))
            for v in sub["veh"]:
                if v not in out["veh"]:
                    out["veh"].append(v)
            out["build"] |= sub["build"]
            out["overlap"] |= sub["overlap"]
            out["block"] |= sub["block"]
        elif t == "WDDemolitionRule_Explosion":
            md = p.get("MinimumDistanceFromExplosionSource")
            for tg in p["PermittedDamageSources"]["TagDictionary"]:
                out["expl"][tg["TagName"]] = md
        elif t == "BHDemolitionRule_Vehicle":
            for v in p["PermittedVehicles"]:
                if v not in out["veh"]:
                    out["veh"].append(v)
            out["overlap"].add(p.get("bPermitOverlaps"))
            out["block"].add(p.get("bPermitBlockingHits"))
        elif t == "WDDemolitionRule_Buildable":
            out["build"] = True
    walk(rs["top"])
    return out


def L(d, kind, name):
    return ct.link(d[kind][name]["rel"], name)


def num(x):
    return "-" if x is None else ct.n(x)


def bar(s):
    return s.replace("DA_Demolition_", "")


def code(items):
    return ", ".join(f"`{i}`" for i in items)


def counts(d):
    meshes = sum(len(a["p"].get("SourceMeshes", [])) for a in d["assets"].values())
    rem = sum(len(r["p"]["RemnantMeshes"]) for r in d["remnants"].values())
    rows = [("Demolition assets (`BHDemolitionDataAsset`)", len(d["assets"])),
            ("Source-mesh entries across those assets", meshes),
            ("Component settings (`BHDemolitionComponentSettings`)", len(d["settings"])),
            ("Remnant-mesh assets (`BHDemolitionRemnantMeshesAsset`)", len(d["remnants"])),
            ("Remnant mesh entries", rem),
            ("Rulesets (`BHDemolitionRuleset`)", len(d["rulesets"]))]
    return "\n".join(["| Item | Count |", "|---|---|"] + [f"| {a} | {b} |" for a, b in rows])


def assets(d):
    out = ["| Asset | Meshes | Component settings | Ruleset | Zones | VFX | Crosstalk tag | Restitution | Remnant set(s) | Remnant actor | Far-rep collision |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in sorted(d["assets"]):
        p = d["assets"][n]["p"]
        rem = sorted({objref(m["Value"].get("RemnantMeshes")) for m in p.get("SourceMeshes", []) if m["Value"].get("RemnantMeshes")})
        fr = ", ".join(num(f.get("RestitutionImpulseMultiplier")) for f in p["DemolitionFragments"]) or "-"
        zones = ", ".join(z.rsplit(".", 1)[1] for z in p["PermittedZones"])
        vfx = code(short(v["AssetPathName"]) for v in p["DemolitionVFX"])
        actor = f"`{short(p['DemolitionRemnantActor']['AssetPathName'])}`" if p.get("DemolitionRemnantActor") else "-"
        col = p.get("bEnableCollisionWhenInFarRepresentation")
        cs = objref(p["DemolitionComponentSettings"]).replace("DA_Demolition_CS_", "").replace("DA_CS_", "")
        out.append(f"| {L(d, 'assets', n)} | {len(p.get('SourceMeshes', []))} | `{cs}` | "
                   f"`{objref(p['DemolitionRuleSet']).replace('BH_Demolition_RS_', '')}` | {zones} | {vfx} | "
                   f"`{p['CrosstalkEventTag']['TagName'].rsplit('.', 1)[1]}` | {fr} | "
                   f"{code(r.replace('DA_Demolition_', '') for r in rem) or '-'} | {actor} | {'-' if col is None else str(col).lower()} |")
    return "\n".join(out)


def xform(o):
    if not o:
        return "-"
    bits = []
    for k in ("Translation", "Scale3D"):
        v = o.get(k, {})
        if any(abs(v.get(a, 0) - IDENT[k][a]) > 1e-9 for a in "XYZ"):
            bits.append(f"{k} ({ct.n(v['X'])}, {ct.n(v['Y'])}, {ct.n(v['Z'])})")
    r = o.get("Rotation", {})
    if any(abs(r.get(a, 0) - IDENT["Rotation"][a]) > 1e-9 for a in "XYZW"):
        bits.append("Rotation set")
    return ", ".join(bits) or "identity"


def meshes(d):
    out = ["| Asset | Source mesh | Far-representation mesh | Remnant set | Remnant base colour / custom values | Far-rep offset |", "|---|---|---|---|---|---|"]
    for n in sorted(d["assets"]):
        for m in d["assets"][n]["p"].get("SourceMeshes", []):
            v = m["Value"]
            far = short(v["FarRepresentationMesh"]["AssetPathName"]) if v.get("FarRepresentationMesh") else "-"
            rem = objref(v.get("RemnantMeshes"))
            cpd = v.get("Remnant_BaseCPD") or {}
            col = cpd.get("CustomPrimitiveColor", {}).get("Hex")
            vals = ", ".join(ct.n(x) for x in cpd.get("CustomPrimitiveValue", []))
            cs = (f"`#{col}`" if col else "-") + (f" / {vals}" if vals else "")
            frd = v.get("FarRepresentationData") or {}
            out.append(f"| `{bar(n)}` | `{short(m['Key'])}` | `{far}` | {'`' + rem.replace('DA_Demolition_', '') + '`' if rem else '-'} | {cs} | {xform(frd.get('Offset'))} |")
    return "\n".join(out)


def remnants(d):
    users = collections.defaultdict(set)
    for n, a in d["assets"].items():
        for m in a["p"].get("SourceMeshes", []):
            r = objref(m["Value"].get("RemnantMeshes"))
            if r:
                users[r].add(bar(n))
    out = ["| Remnant set | Entries | Near mesh | Far mesh | Offset / override | Used by |", "|---|---|---|---|---|---|"]
    for n in sorted(d["remnants"]):
        es = d["remnants"][n]["p"]["RemnantMeshes"]
        near = code(short(e["NearMesh"]["AssetPathName"]) for e in es)
        far = "same" if all(e["NearMesh"] == e["FarMesh"] for e in es) else code(short(e["FarMesh"]["AssetPathName"]) for e in es)
        ov = "null" if all(e.get("Offset") is None and e.get("FarRepresentationData_Override") is None for e in es) else "set"
        out.append(f"| {L(d, 'remnants', n)} | {len(es)} | {near} | {far} | {ov} | {code(sorted(users[n])) or 'no asset in data/'} |")
    return "\n".join(out)


def settings(d):
    users = collections.defaultdict(list)
    for n, a in d["assets"].items():
        users[objref(a["p"]["DemolitionComponentSettings"])].append(bar(n))
    out = ["| Settings asset | Cull start / end | Other component settings | Collision profile | Used by | Assets |", "|---|---|---|---|---|---|"]
    for n in sorted(set(d["settings"]) | set(users)):
        if n in d["settings"]:
            p = d["settings"][n]["p"]
            cs = p.get("ComponentSettings", {})
            other = ", ".join(f"{k}={v}" for k, v in cs.items() if k not in ("InstanceStartCullDistance", "InstanceEndCullDistance"))
            if "bGenerateHitEvents" in p:
                other += (", " if other else "") + f"bGenerateHitEvents={p['bGenerateHitEvents']}"
            out.append(f"| {L(d, 'settings', n)} | {num(cs.get('InstanceStartCullDistance'))} / {num(cs.get('InstanceEndCullDistance'))} | {other or '-'} | `{p.get('CollisionProfileName', '-')}` | {len(users[n])} | {code(sorted(users[n])) or '-'} |")
    return "\n".join(out)


def rules(d):
    out = ["| Ruleset | Rule type(s) | Directly composed of | Effective explosion tags (min distance) | Vehicle variants | Buildables |", "|---|---|---|---|---|---|"]
    for n in sorted(d["rulesets"]):
        r = resolve(d, n)
        types = sorted({e["Type"] for e in d["rulesets"][n]["list"] if e["Type"] != "BHDemolitionRuleset"})
        ex = "; ".join(f"`{t.replace('Meta.Damage.', '')}` ({num(v)})" for t, v in sorted(r["expl"].items(), key=lambda kv: (kv[1] or 0, kv[0]))) or "-"
        out.append(f"| {L(d, 'rulesets', n)} | {code(types)} | {code(k.replace('BH_Demolition_RS_', '') for k in r['kids']) or '-'} | {ex} | {len(r['veh']) or '-'} | {'yes' if r['build'] else '-'} |")
    return "\n".join(out)


def ruleuse(d):
    users = collections.defaultdict(list)
    for n, a in d["assets"].items():
        users[objref(a["p"]["DemolitionRuleSet"])].append(bar(n))
    out = ["| Ruleset (as set on assets) | Assets using it | Assets |", "|---|---|---|"]
    for n in sorted(users, key=lambda k: (-len(users[k]), k)):
        out.append(f"| `{n.replace('BH_Demolition_RS_', '')}` | {len(users[n])} | {code(sorted(users[n]))} |")
    return "\n".join(out)


def vfx(d):
    out = ["| Facet | Value | Assets |", "|---|---|---|"]
    fx = collections.defaultdict(list)
    zones = collections.defaultdict(list)
    for n, a in d["assets"].items():
        p = a["p"]
        for v in p["DemolitionVFX"]:
            fx[v["AssetPathName"].split(".")[0].replace("/Game/VFX/Environmental/Destruction/Demolition/", "")].append(bar(n))
        zones[", ".join(z.rsplit(".", 1)[1] for z in sorted(p["PermittedZones"]))].append(bar(n))
    for title, m in (("Niagara system", fx), ("Zones", zones)):
        for k in sorted(m, key=lambda x: (-len(m[x]), x)):
            out.append(f"| {title} | `{k}` | {len(m[k])}: {code(sorted(m[k]))} |")
    return "\n".join(out)


def crosstalk(d):
    users = collections.defaultdict(list)
    for n, a in d["assets"].items():
        users[a["p"]["CrosstalkEventTag"]["TagName"]].append(bar(n))
    out = ["| Crosstalk tag | Audio event asset(s) carrying the tag | Demolition assets |", "|---|---|---|"]
    for t in sorted(users, key=lambda k: (-len(users[k]), k)):
        ae = ", ".join(ct.link(r) for r in sorted(d["tagrefs"].get(t, []))) or "none found in data/"
        out.append(f"| `{t}` | {ae} | {len(users[t])} |")
    return "\n".join(out)


MODES = {"counts": counts, "assets": assets, "meshes": meshes, "remnants": remnants, "settings": settings,
         "rules": rules, "ruleuse": ruleuse, "vfx": vfx, "crosstalk": crosstalk}


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = MODES[m.group(1)](d).split("\n")
        return nl.join([f"<!-- demolition_tables {m.group(1)} -->"] + body + ["<!-- /demolition_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    d = load()
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(d, text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "counts")](d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
