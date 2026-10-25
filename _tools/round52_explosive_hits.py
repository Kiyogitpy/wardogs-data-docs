"""Round 52: hits to destroy every vehicle with every anti-vehicle explosive (static data).

Reuses the rule evaluator and section routing of damage_tables.py and the explosive rows of explosive_tables.py.
For each vehicle variant and each explosive: the rule factor for source tag + context + Radius.Inner (or .Outer),
the amount (falloff formula, explosive_tables.amount), then hits_to_destroy on the main health section, and the
fewest hits through any single section (the blast resolves its section from the first component hit, so the true
count lies between the two for a centred blast).

    python -I _tools/round52_explosive_hits.py          # write assets/data/explosive-hits-vs-vehicles.json and print summary
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402
import explosive_tables as et  # noqa: E402

OUT = os.path.join(dt.ROOT, "assets", "data", "explosive-hits-vs-vehicles.json")
SOURCES = [  # (label, explosive row id, launcher or carrier)
    ("RPG-7", "93mm"), ("MAAWS", "84mm"), ("9K333 Verba", "72mm"), ("B-13 rocket (122 mm)", "122mm"),
    ("MGL-40 40 mm grenade", "40mm"), ("M67 frag grenade", "M67 frag grenade"), ("C4", "C4"), ("AT mine", "AT mine"),
    ("IED", "IED"), ("Claymore", "Claymore"), ("Stingray drone", "DroneProjectile"), ("Molotov burst", "Molotov"),
]
VEH = [("Havoc", "Attack_ROT_02"), ("MH-6 / AH-6", "ROT_03_Default"), ("Z20 Lakota", "ROT_04_Default"),
       ("SPH-2", "TNK_01_Artillery"), ("L2A6 / Gepard (heavy)", "TNK_01_Heavy"), ("Flakpanzer Gepard", "TNK_01_AntiAir"),
       ("T-72B3", "TNK_04"), ("M113 APC SV", "SPW_01"), ("Bobcat", "WHL_01_Default"), ("Dune Buggy", "WHL_06_DuneBuggy_Default"),
       ("Kodiak", "WHL_02_Default"), ("Humvee", "WHL_05_Humvee_Default"), ("Humvee [Minigun]", "WHL_05_Humvee_RingMinigun"),
       ("Humvee [M249]", "WHL_05_Humvee_RingTurret"), ("Ural", "WHL_07_Default"), ("Wolf-110", "WHL_08_Default"),
       ("Talon 9K SAM", "STN_01"), ("Vanguard CIWS", "STN_02"), ("L81 Mortar", "STN_03"), ("Loudspeaker", "STN_04"),
       ("Stingray", "STN_05"), ("MG Nest", "STN_06")]


def main():
    rows = {r["id"]: r for r in et.collect()}
    generic, vrows = dt.vehicle_tables()
    by_name = {os.path.basename(p)[3:-5]: p for p in dt.variants()}
    out = {"meta": {"generator": "python -I _tools/round52_explosive_hits.py",
                    "formula": "amount = Base inside E, then linear to Base x (1 - falloff) at R, floored at Minimum, 0 at R; "
                               "damage = amount x product(1 + a/100 over every matching Percentage_Ongoing rule, with the Inner or Outer ring tag); "
                               "hits = fewest applications until main health is 0 (section routing honoured, radial skip flags honoured).",
                    "assumptions": "full-health vehicle, no repair, one radial application per blast, distance within the inner radius for the headline count",
                    "sources": {}, "evidence": "docs/evidence/round52-explosives-vs-vehicles.md"}, "vehicles": []}
    for lab, rid in SOURCES:
        r = rows[rid]
        out["meta"]["sources"][lab] = {"row": rid, "tag": r["tag"], "base": r["base"], "inner_m": r["E"] / 100, "outer_m": r["R"] / 100,
                                        "falloff": r["falloff"], "min": r["min"]}
    for lab, name in VEH:
        modules, _, _ = dt.assemble(by_name[name])
        secs0, dtag = dt.sections(modules), dt.damage_tag(modules)
        secs = et.radial_secs(secs0, dt.section_radial_flags(modules))
        entries = dt.row_entries(dtag, vrows) + generic
        v = {"vehicle": lab, "variant": name, "damage_row": dtag, "main_health": secs[dt.MAIN][0], "hits": {}}
        for slab, rid in SOURCES:
            r = rows[rid]
            tags = [r["tag"]] + r["ctx"]
            cell = {}
            for ring, tag, d in (("inner", et.INNER, 0.0), ("outer_mid", et.OUTER, (r["E"] + r["R"]) / 2)):
                amt = et.amount(d, r)[0]
                f_main = dt.source_rule_factor(entries, tags + [tag], secs[dt.MAIN][1])
                best = None
                for sec, (hp, hit, *_) in secs.items():
                    if not hit:
                        continue
                    f = dt.source_rule_factor(entries, tags + [tag], hit)
                    h = dt.hits_to_destroy(secs, sec, amt * f)
                    if h is not None and (best is None or h < best[0]):
                        best = (h, sec.replace("Attribute.Gameplay.", ""))
                cell[ring] = {"amount": round(amt, 2), "factor_main": round(f_main, 4),
                              "hits_main": dt.hits_to_destroy(secs, dt.MAIN, amt * f_main), "min_hits_any_section": best[0] if best else None,
                              "min_section": best[1] if best else None}
            v["hits"][slab] = cell
        out["vehicles"].append(v)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for v in out["vehicles"]:
        print(v["vehicle"], v["main_health"], {k: (c["inner"]["hits_main"], c["inner"]["min_hits_any_section"], c["outer_mid"]["hits_main"]) for k, c in v["hits"].items()})



WIKI_ROWS = [  # (links, JSON vehicle label)
    ("[Havoc](havoc.md)", "Havoc"), ("[MH-6](mh-6.md), [AH-6M [Miniguns]](ah-6m-miniguns.md), [AH-6R [Rockets]](ah-6r-rockets.md)", "MH-6 / AH-6"),
    ("[Z20 Lakota](z20-lakota.md), [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md)", "Z20 Lakota"), ("[SPH-2](sph-2.md)", "SPH-2"),
    ("[L2A6](l2a6.md), [Flakpanzer Gepard](flakpanzer-gepard.md)", "Flakpanzer Gepard"), ("[T-72B3](t-72b3.md)", "T-72B3"),
    ("[M113 APC SV](m113-apc-sv.md)", "M113 APC SV"), ("[Bobcat](bobcat.md)", "Bobcat"), ("[Dune Buggy](dune-buggy.md)", "Dune Buggy"),
    ("[Kodiak](kodiak.md), [Kodiak [Pickup]](kodiak-pickup.md), [Kodiak [M249]](kodiak-m249.md)", "Kodiak"), ("[Humvee](humvee.md)", "Humvee"),
    ("[Humvee [Minigun]](humvee-minigun.md)", "Humvee [Minigun]"), ("[Humvee [M249]](humvee-m249.md)", "Humvee [M249]"),
    ("[Ural](ural.md), [Ural Defender](ural-defender.md), [Ural Defender [M249]](ural-defender-m249.md)", "Ural"),
    ("[Wolf-110](wolf-110.md), [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md)", "Wolf-110")]


def wiki_tables():
    data = json.load(open(OUT, encoding="utf-8"))
    by = {v["vehicle"]: v for v in data["vehicles"]}
    groups = [["RPG-7", "MAAWS", "9K333 Verba", "B-13 rocket (122 mm)", "MGL-40 40 mm grenade"],
              ["M67 frag grenade", "C4", "AT mine", "IED", "Claymore", "Stingray drone"]]
    for cols in groups:
        print("| Vehicle | Main health (HP) | " + " | ".join(c.replace(" rocket (122 mm)", " rocket").replace(" 40 mm grenade", "") for c in cols) + " |")
        print("|---|---:|" + "---:|" * len(cols))
        for links, lab in WIKI_ROWS:
            v = by[lab]
            cells = []
            for c in cols:
                i = v["hits"][c]["inner"]
                n = i["hits_main"]
                if i["min_hits_any_section"] is not None and n is not None and i["min_hits_any_section"] < n:
                    cells.append(f"{n} ({i['min_hits_any_section']} through the {i['min_section'].replace('Health.Rotor.Tail', 'tail rotor')})")
                else:
                    cells.append("-" if n is None else str(n))
            print(f"| {links} | {v['main_health']:,.0f} | " + " | ".join(cells) + " |")
        print()


if "--wiki" in sys.argv:
    wiki_tables()
else:
    main()
