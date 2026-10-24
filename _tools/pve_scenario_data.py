"""Build assets/data/pve-scenarios.json from the round-36 extractor dumps.

    python -I _tools/pve_scenario_data.py [<round36_ai dir>]

Reads, under the round-36 output directory (default E:/Reverse_Engineer/wardogs_analysis/round36_ai):
  dump/        WdExtract dump of Wardogs/Plugins/GameFeatures/{PvE,AI}/ packages
  cells/       WdExtract dump of the World Partition cell levels (.umap) of each scenario
  cells_<Scenario>.txt   the cell package paths of one scenario (from `rawfiles <Scenario>/Content/EDL`)
and writes, per scenario, the starting cash, player faction, map, placed AI spawners by config,
spawn mode and forced goal, the hack duration, and the VIP loot rows. Idempotent: same input, same file.
Exits 0 with a message if the input directory is absent.
"""
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "pve-scenarios.json")
SCEN = ["HunterKiller_01", "StrikeDisarm_01", "VIPEscort_01"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def short(o):
    return o["ObjectName"].split("'")[1] if isinstance(o, dict) and "'" in o.get("ObjectName", "") else None


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r"E:/Reverse_Engineer/wardogs_analysis/round36_ai"
    if not os.path.isdir(os.path.join(base, "dump")):
        print(f"input not found ({base}); skipping")
        return 0
    result = {"source": "round 36 cooked-data read (docs/evidence/round36-ai.md)", "scenarios": {}}
    for s in SCEN:
        gfd = load(os.path.join(base, "dump", s + ".json"))
        sd = {}
        for x in gfd:
            if x["Type"] == "WDGameFeatureAction_AddScenarioState":
                sd = x["Properties"]["ScenarioData"]
        entry = {
            "map": "Kavkazi",
            "startingCash": sd.get("ScenarioStartingCash"),
            "playerFaction": (sd.get("PlayerFactionTag") or {}).get("TagName"),
            "spawners": collections.Counter(),
            "hackingDurationSeconds": None,
        }
        counts = collections.Counter()
        for line in open(os.path.join(base, "cells_%s.txt" % s), encoding="utf-8").read().split("\n"):
            line = line.strip()
            if not line:
                continue
            for x in load(os.path.join(base, "cells", line.split("/")[-1] + ".json")):
                p = x.get("Properties", {})
                if x["Type"] == "BP_WDPvEAISpawner_C":
                    mode = "triggered" if "SpawnTriggerType" in p else "automatic"
                    goal = short(p["ForcedGoal"]) if "ForcedGoal" in p else "default"
                    counts["%s|%s|%s" % (short(p["SpawnConfig"]), mode, goal)] += 1
                elif x["Type"] == "B_StrikeDisarm_LaptopObjective_C":
                    entry["hackingDurationSeconds"] = p.get("HackingDurationSeconds")
        entry["spawners"] = [
            {"config": k.split("|")[0], "spawn": k.split("|")[1], "goal": k.split("|")[2], "count": v}
            for k, v in sorted(counts.items())
        ]
        entry["spawnerTotal"] = sum(counts.values())
        result["scenarios"][s] = entry
    loot = load(os.path.join(base, "dump", "DT_LootableDataTable_VIPEscort_01.json"))[0]["Rows"]
    result["vipEscortLoot"] = {
        name: {
            "item": r["LootableData"]["ItemsToSpawn"][0]["ItemTag"]["TagName"],
            "subItems": [s["SubItemTag"]["TagName"] for s in r["LootableData"]["ItemsToSpawn"][0]["SubItemsSpawnData"]],
            "amount": r["LootableData"]["ItemsToSpawn"][0]["ItemAmount"],
            "chance": r["LootableData"]["SpawnChance"],
            "spawnByPoints": r["LootableData"]["bSpawnByPoints"],
            "initialSpawnPoints": r["LootableData"]["InitialSpawnPoints"],
            "canRespawn": r["LootableData"]["bCanRespawn"],
            "respawnTime": r["LootableData"]["RespawnTime"],
        }
        for name, r in loot.items()
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
