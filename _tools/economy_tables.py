"""Economy tables for round 36, rebuilt from data/ into assets/data/economy.json.

Collects, in one file, the progression and economy values that the wiki listed as "not yet known":

  achievements      DT_Achievements + the achievement rows of DT_Challenges_SessionEvents_Shared (the Steam id,
                    the StateTree, its parameter, the trigger event) and the parameter VALUES. The values are
                    not in data/: CUE4Parse keeps a StateTree parameter bag's descriptors and drops its value
                    bytes (only SerialSize survives). They were read from the cooked package bytes
                    (docs/evidence/round36-econ.md, "How the bytes were read") and are listed in BYTE_VALUES
                    below with the GUID and raw bytes. This script checks every one against data/ (same
                    descriptor GUID, same SerialSize) and, with --bytes <dir>, against the raw package dump.
  wagers            DT_WagerPricing, DT_WagerActions, DT_WagerConditions, DT_WagerObjectiveCatalog
  roleUnlocks       DT_MetaTree_Roles: every unlock node with the role level it needs and its cash cost,
                    plus DT_RoleMasteryDefinitions (101 levels per role, no rewards listed)
  platformMastery   DA_UI_PlatformMastery_SceneData: the platforms (weapons, vehicles) shown per mastery type
  currencies        DT_CurrenciesDefinitions, DT_ExchangeDefinitions, the passive-mission Intel rewards

Rerun after a data update (idempotent, stdlib only):

    python -I _tools/economy_tables.py            # rewrite assets/data/economy.json
    python -I _tools/economy_tables.py --check    # exit 1 if the file is stale or a byte value fails its check
    python -I _tools/economy_tables.py --bytes DIR  # also verify BYTE_VALUES against DIR/sessionshared.bin
"""
import glob
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs", "Content")
OUT = os.path.join(ROOT, "assets", "data", "economy.json")
EXPORT = re.compile(r"^--- export: .* ---\s*$", re.M)

# Parameter values read from the cooked bytes of Meta/Challenges/DT_Challenges_SessionEvents_Shared.
# Layout in the package: descriptor GUID (4 x uint32 LE) | FName | value type | ... | int32 SerialSize | value block.
# The value block is UE unversioned property data: a 2-byte fragment header, then the value (Int32 / Float).
# type: Int32 or Float; raw: the block bytes after SerialSize; the same decoding gives RequiredAmount = 5000
# for the passive mission EarnCash.1, which equals that row's objective value (the check of the method).
BYTE_VALUES = {
    "Achievement.Economy.LoadoutSpend": {"param": "CashThreshold", "guid": "97936D73-48650C40-A7C8D388-5CD18B2E", "type": "Int32", "raw": "0003a0860100", "value": 100000},
    "Achievement.Economy.SingleLifeProfit": {"param": "CashThreshold", "guid": "2660206F-4EDC0274-D0750083-A7B2CF63", "type": "Int32", "raw": "0003a0860100", "value": 100000},
    "Achievement.Survival.ControlZoneSurvivor": {"param": "RequiredSeconds", "guid": "691AF475-414BD91D-3C40CFB2-EC5B88B0", "type": "Float", "raw": "000300006145", "value": 3600.0},
    "Achievement.Combat.LongShot": {"param": "DistanceThreshold", "guid": "BD1E3E64-4EBD1C97-B2AED692-82AF3F75", "type": "Float", "raw": "0003008cb947", "value": 95000.0},
}

# What each state tree tests, read from the StateTree nodes and states (Derived from the export).
CRITERIA = {
    "Achievement.Tutorial.Completed": "Event.StateTree.TutorialCompleted fires (the tutorial is finished).",
    "Achievement.Tutorial.PunchKristopher": "A character-damaged event whose target is Kristopher (the tutorial NPC) and whose damage is melee.",
    "Achievement.Economy.TopCashEarner": "No event trigger. Checked on a match stat: the player's cash-earned placement equals 1 and the cash earned is above 0.",
    "Achievement.Economy.SingleLifeProfit": "Event.StateTree.ProfitChanged; a match-stat difference (profit) compared with CashThreshold using GreaterOrEqual.",
    "Achievement.Economy.LoadoutSpend": "Event.StateTree.LoadoutPurchased; the resource tag must equal cash and the resource change is compared with CashThreshold using GreaterOrEqual.",
    "Achievement.Survival.ControlZoneSurvivor": "Entering a control zone starts a timer; the achievement unlocks when RequiredSeconds pass in the zone and the pawn is still alive. Death resets the watch.",
    "Achievement.Combat.LongShot": "Event.StateTree.LongShotVitalityChanged; the target is hostile and the message Distance (float) is compared with DistanceThreshold using GreaterOrEqual.",
    "Achievement.Combat.RicochetKill": "Event.StateTree.RicochetVitalityChanged; the target is hostile and the kill carries the ricochet tag.",
    "Achievement.Combat.DefibrillatorKill": "Event.StateTree.DefibrillatorVitalityChanged; the target is hostile and the kill carries the defibrillator tag.",
    "Achievement.Match.CleanSweep": "No event trigger. Checked on the final faction scores: the player's own faction score is above 0 and the opposing faction's score is 0.",
}


def exports(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(p) for p in EXPORT.split(f.read())[1:]]


def table(rel):
    for e in exports(os.path.join(DATA, rel)):
        if e.get("Type") == "DataTable":
            return e["Rows"]
    raise SystemExit("no DataTable in " + rel)


def text(v):
    if isinstance(v, dict):
        return v.get("SourceString") or v.get("CultureInvariantString")
    return v


def tag(v):
    return v.get("TagName") if isinstance(v, dict) else v


def guid_bytes(g):
    return b"".join(struct.pack("<I", int(x, 16)) for x in g.split("-"))


def names():
    out = {}
    for f in ("Items", "Garage", "Misc", "VehicleAmmo"):
        for k, v in table(f"UI/Data/Entities/DT_EntityData_UI_{f}.json").items():
            out[k.lower()] = text(v.get("FriendlyName"))
    return out


def achievements(errors):
    base = table("Meta/Achievements/DT_Achievements.json")
    chal = table("Meta/Challenges/DT_Challenges_SessionEvents_Shared.json")
    rows = []
    for tg, v in base.items():
        c = chal.get(tg)
        sr = c["StateTreeReference"]
        descs = sr["Parameters"]["PropertyDescs"]
        row = {
            "tag": tg,
            "name": text(v["DisplayName"]),
            "steamId": v["SteamAchievementID"],
            "stateTree": sr["StateTree"]["ObjectName"].split("'")[1],
            "autoActivate": c["bAutoActivate"],
            "rewards": c["Rewards"],
            "objectives": c["Objectives"],
            "parameter": None,
            "threshold": None,
            "unit": None,
            "criteria": CRITERIA[tg],
        }
        bv = BYTE_VALUES.get(tg)
        if bv:
            d = descs[0]
            ok = d["Name"] == bv["param"] and d["ID"] == bv["guid"] and sr["Parameters"]["SerialSize"] == 6 and sr["PropertyOverrides"] == [bv["guid"]]
            if not ok:
                errors.append(f"{tg}: descriptor, GUID or SerialSize no longer matches BYTE_VALUES")
            raw = bytes.fromhex(bv["raw"])
            val = struct.unpack("<i" if bv["type"] == "Int32" else "<f", raw[2:6])[0]
            if raw[:2] != b"\x00\x03" or val != bv["value"]:
                errors.append(f"{tg}: raw bytes do not decode to {bv['value']}")
            row["parameter"] = bv["param"]
            row["threshold"] = bv["value"]
            row["unit"] = {"CashThreshold": "cash", "RequiredSeconds": "seconds", "DistanceThreshold": "Unreal units (cm); 95000 = 950 m"}[bv["param"]]
        elif descs:
            errors.append(f"{tg}: has parameters but no BYTE_VALUES entry")
        rows.append(row)
    return rows


def wagers():
    pr = table("Meta/Wagers/DT_WagerPricing.json")["Wager.Pricing"]
    p = pr["Pricing"]
    pricing = {
        "minStake": pr["MinStake"],
        "maxStake": pr["MaxStake"],
        "maxPayout": p["MaxPayout"],
        "foldBonusStep": p["FoldBonusStep"],
        "livesOdds": p["LivesOdds"],
        "unnamedFloats": {k: v for k, v in p.items() if k.startswith("_")},
    }
    acts = []
    for k, v in table("Meta/Wagers/DT_WagerActions.json").items():
        acts.append({
            "tag": k, "name": text(v["DisplayName"]), "shortName": text(v["ShortName"]), "description": text(v["Description"]),
            "challenge": tag(v["ChallengeId"]), "countParameter": v["_aaabcjojpnjmnbelecidg"],
            "minCount": v["MinCount"], "maxCount": v["MaxCount"], "defaultCount": v["DefaultCount"],
            "oddsByCount": v["Odds"], "rules": [text(r) for r in v["Rules"]],
            "payoutResource": tag(v["PayoutResourceTag"]), "cooldownSeconds": v["CooldownSeconds"],
        })
    conds = []
    for k, v in table("Meta/Wagers/DT_WagerConditions.json").items():
        conds.append({
            "tag": k, "name": text(v["DisplayName"]), "category": tag(v["Category"]), "odds": v["Odds"],
            "minValue": v["MinValue"], "maxValue": v["MaxValue"], "valueStep": v["ValueStep"],
            "cooldownSeconds": v["CooldownSeconds"],
            "requiresAnyAction": [tag(t) for t in (v["RequiresAnyActionTags"] or {}).get("GameplayTags", [])] if isinstance(v["RequiresAnyActionTags"], dict) else [],
        })
    cat = table("Meta/Wagers/DT_WagerObjectiveCatalog.json")["Wager.ObjectiveCatalog"]["Objectives"]
    objs = [{
        "id": o["ID"], "action": tag(o["ActionId"]), "count": o["Count"], "conditions": [tag(c["ConditionId"]) for c in o["Conditions"]],
        "odds": o["Odds"], "cooldownSeconds": o["CooldownSeconds"], "unlockNode": tag(o["UnlockNode"]), "flag": o["_aaaakgfoodihlgbfboeka"],
    } for o in cat]
    return {"pricing": pricing, "actions": acts, "conditions": conds, "objectiveCatalog": objs}


def role_unlocks():
    nm = names()
    tree = table("Meta/CharacterSkills/DT_MetaTree_Roles.json")
    out = []
    for role, row in tree.items():
        for n in row["Nodes"]:
            lv = n["LevelsData"]
            assert len(lv) == 1
            sd = lv[0]["Prerequisites"]["QueryDefinition"]["SharedDefinition"]
            structs = sd["Conditions"]["Structs"] if sd else []
            out.append({
                "tree": role, "node": n["ID"]["TagName"], "name": nm.get(n["ID"]["TagName"].lower()),
                "minLevel": structs[0]["MinLevel"] if structs else None,
                "cash": next((c["Value"] for c in lv[0]["Cost"] if c["Key"]["TagName"].endswith("Currency.Cash")), None),
                "otherCosts": [[c["Key"]["TagName"], c["Value"]] for c in lv[0]["Cost"] if not c["Key"]["TagName"].endswith("Currency.Cash")],
            })
    mast = table("Meta/Levels/Roles/DT_RoleMasteryDefinitions.json")
    levels = {}
    for role, row in mast.items():
        L = row["LevelDefinitions"]
        levels[role] = {"xpResource": tag(row["ResourceTag"]), "levels": len(L) - 1, "rewardsListed": sum(len(x["Rewards"]) for x in L),
                        "xpAtLevel": [x["XP"] for x in L]}
    return {"nodes": out, "roleMastery": levels}


def platform_mastery():
    path = os.path.join(DATA, "UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_SceneData.json")
    sc = [e for e in exports(path) if e["Type"] == "WDUIPlatformMasterySceneData"][0]
    nm = names()
    out = {}
    for e in sc["Properties"]["SceneTypesData"]:
        for td in e["Value"]["TypesData"]:
            out.setdefault(tag(e["Key"]), {})[td["Key"].split("::")[-1]] = [
                {"id": i, "name": nm.get(i.lower())} for i in td["Value"]["PlatformIds"]]
    # PlatformXPTag on every entity row
    n = nonnone = 0
    for path in sorted(glob.glob(os.path.join(DATA, "..", "**", "DT_EntityData_*.json"), recursive=True)):
        for e in exports(path):
            if e.get("Type") != "DataTable":
                continue
            for v in e["Rows"].values():
                if "PlatformXPTag" in v:
                    n += 1
                    nonnone += tag(v["PlatformXPTag"]) != "None"
    return {"types": out, "entityRowsWithPlatformXPTag": n, "entityRowsWithPlatformXPTagSet": nonnone}


def currencies():
    cur = {k: {"initialBalance": v["InitialBalance"], "name": text(v["DisplayName"])} for k, v in table("Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json").items()}
    exch = {k: {"exchangeRates": v["ExchangeRates"]} for k, v in table("Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json").items()}
    intel = []
    for k, v in table("Meta/Missions/DT_PassiveMissionChallenges.json").items():
        for r in v["Rewards"]:
            intel.append({"challenge": k, "reward": tag(r["RewardTag"]), "quantity": r["Quantity"],
                          "objective": [[tag(o["Key"]), o["Value"]] for o in v["Objectives"]]})
    gm = table("Meta/Collection/DT_GoldMarket.json")
    expiring = [{"tag": k, "goldBars": v["GoldBarCost"], "expirationType": v["ExpirationType"].split("::")[-1], "ticks": v["ExpirationTime"]["Ticks"]}
                for k, v in gm.items() if not v["ExpirationType"].endswith("NO_EXPIRATION")]
    return {"definitions": cur, "exchangeDefinitions": exch, "intelRewards": intel, "goldMarketExpiring": expiring}


def build(errors):
    return {
        "meta": {"source": "data/Wardogs/Content (CL516586 cooked export) plus package bytes for achievement parameter values",
                 "script": "_tools/economy_tables.py", "evidence": "docs/evidence/round36-econ.md"},
        "achievements": achievements(errors),
        "wagers": wagers(),
        "roleUnlocks": role_unlocks(),
        "platformMastery": platform_mastery(),
        "currencies": currencies(),
    }


def verify_bytes(dirpath, errors):
    b = open(os.path.join(dirpath, "sessionshared.bin"), "rb").read()
    for tg, bv in BYTE_VALUES.items():
        g = guid_bytes(bv["guid"])
        raw = bytes.fromhex(bv["raw"])
        i = b.find(g)
        found = False
        while i >= 0:
            window = b[i:i + 60]
            if struct.pack("<i", 6) + raw in window:
                found = True
                break
            i = b.find(g, i + 1)
        if not found:
            errors.append(f"{tg}: SerialSize 6 + raw bytes not found after the descriptor GUID in the package")


def main(argv):
    errors = []
    doc = build(errors)
    if "--bytes" in argv:
        verify_bytes(argv[argv.index("--bytes") + 1], errors)
    text_out = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if "--check" in argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != text_out:
            errors.append("assets/data/economy.json is stale")
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(text_out)
    for e in errors:
        print("ERROR:", e)
    a = doc["achievements"]
    print(f"achievements {len(a)}, wager actions {len(doc['wagers']['actions'])}, conditions {len(doc['wagers']['conditions'])}, "
          f"objectives {len(doc['wagers']['objectiveCatalog'])}, unlock nodes {len(doc['roleUnlocks']['nodes'])}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
