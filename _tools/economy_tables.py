"""Build economy.json from saved exports, with source-qualified achievement evidence.

    python -I _tools/economy_tables.py             # rewrite output, exit 1 on unresolved obligations
    python -I _tools/economy_tables.py --check     # no writes; also fail on stale output
    python -I _tools/economy_tables.py --bytes DIR # verify DIR/sessionshared.bin

CL533731 thresholds were decoded independently from its raw challenge package.
Exact export/tree fingerprints bound the recorded interpretations to reviewed snapshots.
JSON fingerprints cannot prove the value bytes of a future package with identical JSON;
--bytes checks the actual package identity. Saved configuration is not effective gameplay.
"""
import glob
import hashlib
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs", "Content")
OUT = os.path.join(ROOT, "assets", "data", "economy.json")
EXPORT = re.compile(r"^--- export: .* ---\s*$", re.M)

# Parameter values independently read in both the historical report and CL533731 raw capture.
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


# Canonical JSON SHA-256 pins: current CL533731 and historical HEAD tree snapshots.
# These protect the prose from silently surviving a changed tree or binding.
TREE_SOURCES = {'Achievement.Tutorial.Completed': ('Content/Meta/Achievements/StateTrees/ST_Achievement_TutorialCompleted.json',
                                    'bf00f3e6c9cf30dc3ee9eb89b3e37b5494ecaf77e3e8ff2b6e2784355d67ceba',
                                    'bf00f3e6c9cf30dc3ee9eb89b3e37b5494ecaf77e3e8ff2b6e2784355d67ceba'),
 'Achievement.Tutorial.PunchKristopher': ('Content/Meta/Achievements/StateTrees/ST_Achievement_PunchKristopher.json',
                                          'c08bd4dcf33a49998a6ac4ae36a251637e05f370c2aedd567bc87baeae439e58',
                                          '6bfeec6749e6e9ffd7f41aea28e8769602198bc202387f2432a19f7b14325b05'),
 'Achievement.Economy.TopCashEarner': ('Content/Meta/Achievements/StateTrees/ST_Achievement_TopCashEarner.json',
                                       '1763ba99fbfc6ef4988e77454d00af06dec7a46594cd7b9d894afdc04e5924fe',
                                       'ceb78c369ce1e98e02b3fa3c22996e8c702018d670c648a61756daec79401b78'),
 'Achievement.Economy.SingleLifeProfit': ('Content/Meta/Achievements/StateTrees/ST_Achievement_SingleLifeProfit.json',
                                          '91b84ae81bb86f72ffc36e16b657934b7a37abf76eb1eec66f51ef40acfc4707',
                                          'b945a8ad6b76439e1ef397df7f95bdc81cbeda2a11e10e515762d84e64880e15'),
 'Achievement.Economy.LoadoutSpend': ('Content/Meta/Achievements/StateTrees/ST_Achievement_LoadoutSpend.json',
                                      '71fc96f7e99366c31e9b3f30ee5ad63eab8c36a48c62212881a705401cccb320',
                                      'e816e3f535dd3c7f5e02924b49bfe7e27c6b5b460467b8bdc2fcd29572d87c2f'),
 'Achievement.Survival.ControlZoneSurvivor': ('Content/Meta/Achievements/StateTrees/ST_Achievement_ControlZoneSurvivor.json',
                                              '5410a5a8763a4be92665700e887a878ed7fdb95be32ae97ae5b3cdaf92a9892b',
                                              '5410a5a8763a4be92665700e887a878ed7fdb95be32ae97ae5b3cdaf92a9892b'),
 'Achievement.Combat.LongShot': ('Content/Meta/Achievements/StateTrees/ST_Achievement_LongShot.json',
                                 '37b57dd807791f8f08a3ffcfdd57a9d7bdae91bb2741e585b9cf7fb6591cdbdf',
                                 'f422b87d27c2dcd89490187494e6a1dc9697fd8c286290a9ac293daf51a25774'),
 'Achievement.Match.CleanSweep': ('Content/Meta/Achievements/StateTrees/ST_Achievement_CleanSweep.json',
                                  'fc7a0a8d24728d662140eab0f722e40cc371121e35d043b56ac223b1f32bc219',
                                  '942674f59627b9b002240fc0bf3c42b42e3e57632bb3b9195aaa633acb7ae624'),
 'Achievement.Combat.RicochetKill': ('Content/Meta/Achievements/StateTrees/ST_Achievement_RicochetKill.json',
                                     'b7608667f5fa0eb931b2d326edb56e62b9b7a5bce9088ad16f5fa892c2ede378',
                                     'b7608667f5fa0eb931b2d326edb56e62b9b7a5bce9088ad16f5fa892c2ede378'),
 'Achievement.Combat.DefibrillatorKill': ('Content/Meta/Achievements/StateTrees/ST_Achievement_DefibrillatorKill.json',
                                          '925b1b67fa78777f266ea10eceb2696a5db727e26208598bad65b4b57ebd4825',
                                          '925b1b67fa78777f266ea10eceb2696a5db727e26208598bad65b4b57ebd4825'),
 'Achievement.Combat.HesBehindYou': ('Content/Meta/Achievements/StateTrees/ST_Achievement_HesBehindYou.json',
                                     '5a5113e51bac131813289accbc17c88c2a9caffb4ff258878c9238d8731c25e6',
                                     None),
 'Achievement.Logistics.CarJacker': ('Content/Meta/Achievements/StateTrees/ST_Achievement_CarJacker.json',
                                     '2f11f280103090de07d70b3c3dc9867c1820a7aeaeca1428b5a92e08840cc8e5',
                                     None),
 'Achievement.HotZone.SlotMachine': ('Content/Meta/Achievements/StateTrees/ST_Achievement_SlotMachine.json',
                                     'd7ccad05a98df0445a29bc5d31746ce052b337a73c9472350f634af71d5a51e9',
                                     None),
 'Achievement.ShootingRange.SoundTheHorn': ('Plugins/GameFeatures/ShootingRange/Content/Data/Challenges/ST_Achievement_SoundTheHorn.json',
                                            '008ea896b3f7d4c206167031d5e3c91148be63ec9a6bb44184f04560780da034',
                                            None)}
CURRENT_CRITERIA = {'Achievement.Tutorial.Completed': 'On Event.StateTree.TutorialCompleted, transition to the unlock task.',
 'Achievement.Tutorial.PunchKristopher': 'On Event.StateTree.CharacterDamaged: target matches Id.Character.Kristopher, '
                                         'CauseEntityTag equals Id.Item.Fists, and Instigator equals the context PlayerState.',
 'Achievement.Economy.TopCashEarner': 'No event transition: Analytics.Player.Cash.Earned placement equals 1 and its value is '
                                      'greater than 0.',
 'Achievement.Economy.SingleLifeProfit': 'On Event.StateTree.ProfitChanged: the Get Match Stat Difference output for '
                                         'current-life cash earned/spent is compared with CashThreshold using GreaterOrEqual.',
 'Achievement.Economy.LoadoutSpend': 'On Event.StateTree.LoadoutPurchased: ActionTag equals '
                                     'Meta.Progression.Resources.MatchScore.Purchased.Loadout, and the cash '
                                     'ResourceChangedAmount output is compared with CashThreshold using GreaterOrEqual. The '
                                     'native sign/consumer behavior is unverified.',
 'Achievement.Survival.ControlZoneSurvivor': 'The control-zone tag listener leads to a pawn-alive check and a delay bound to '
                                             'RequiredSeconds. Tag removal or respawn returns to waiting; a vitality event '
                                             'targeting the context PlayerState also returns to waiting. Timer-state completion '
                                             'leads to unlock. Effective event filtering/completion behavior is unverified.',
 'Achievement.Combat.LongShot': 'On Event.StateTree.LongShotVitalityChanged: InstigatorPlayerState equals the context '
                                'PlayerState, ActionTag equals KillScore, target/instigator hostility accepts Hostile, and '
                                'Distance >= DistanceThreshold. An inverted Has Tags condition tests CauseTags against '
                                'Id.Vehicle, ID.Item.ATMine and Id.Item.Claymore.',
 'Achievement.Match.CleanSweep': 'No event transition: Get Final Faction Scores outputs OwnScore > 0 and HighestOpposingScore == '
                                 '0 for the context player faction.',
 'Achievement.Combat.RicochetKill': 'On Event.StateTree.RicochetVitalityChanged: InstigatorPlayerState equals the context '
                                    'PlayerState, ActionTag equals KillScore, hostility accepts Hostile, and ContextTags has '
                                    'Meta.Progression.Context.Player.KillContext.Ricochet.',
 'Achievement.Combat.DefibrillatorKill': 'On Event.StateTree.DefibrillatorVitalityChanged: InstigatorPlayerState equals the '
                                         'context PlayerState, ActionTag equals KillScore, hostility accepts Hostile, and Has '
                                         'Tags tests CauseTags against Id.Item.Defibrillator.',
 'Achievement.Combat.HesBehindYou': 'On Event.StateTree.HesBehindYouVitalityChanged: InstigatorPlayerState equals the context '
                                    'PlayerState, ActionTag equals KillScore, hostility accepts Hostile, ContextTags has '
                                    'Meta.Progression.Context.Player.KillContext.Backblast, and the context pawn has '
                                    'State.Location.Objective.ControlZone.',
 'Achievement.Logistics.CarJacker': 'On Event.StateTree.CarJackerResourceChanged: PlayerState equals the context PlayerState, '
                                    'ActionTag matches Challenges.Rewards.DeploySupplyCrate, and Has Tags tests ContextTags '
                                    'against Challenges.Context.SupplyPallet.Stolen.',
 'Achievement.HotZone.SlotMachine': 'On Event.StateTree.SlotMachineHotZoneActivated: Instigator equals the context pawn, '
                                    'NumCodeDigitsGuessed >= 3 and NumCodeDigits >= 4. The last binding is NumCodeDigits, '
                                    'despite the node label referring to drill towers.',
 'Achievement.ShootingRange.SoundTheHorn': 'On Event.StateTree.SoundTheHornInteraction: Interactor equals the context pawn, '
                                           'InteractionMessageType equals integer 2, and Interactable passes the '
                                           'B_ShootingRange_Lever_PlayAudio_C class condition. Completion of '
                                           'B_WaitForSoundDuration_C (Sound = SFX_Prop_ShootingRange_Horn) leads to unlock; '
                                           'task/native behavior is unverified.'}
CHALLENGE_SOURCES = {
    "cecaad746f277ae52a0936b17e9584c1d5e19e96bb8dc2c64525b41ef2106521": "CL533731",
    "036037feaffb2b8af11c7186bdeb3ab204086909601c68d6263e7880ebc48ff4": "CL516586",
}
CURRENT_RAW_SHA256 = "f29e751a98f8e8a760d5b5e3712890d5ee72d51534f6a56c9aff146e75db30ea"
CURRENT_VALUE_OFFSETS = {
    "Achievement.Economy.LoadoutSpend": 2783,
    "Achievement.Economy.SingleLifeProfit": 4099,
    "Achievement.Survival.ControlZoneSurvivor": 3816,
    "Achievement.Combat.LongShot": 4373,
}
SHARED_CHALLENGES = "Meta/Challenges/DT_Challenges_SessionEvents_Shared.json"
SHOOTING_CHALLENGES = "../Plugins/GameFeatures/ShootingRange/Content/Data/Challenges/DT_Challenges_SessionEvents_ShootingRange.json"


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def parameter_matches(sr, bv):
    descs = sr["Parameters"]["PropertyDescs"]
    if len(descs) != 1:
        return False
    d = descs[0]
    return (d.get("Name") == bv["param"] and d.get("ID") == bv["guid"]
            and d.get("ValueType") == "EPropertyBagPropertyType::" + bv["type"]
            and d.get("ValueTypeObject") is None
            and d.get("ContainerType") == "EPropertyBagContainerType::None"
            and d.get("ContainerTypes", {"Types": []}) == {"Types": []}
            and sr["Parameters"]["SerialSize"] == 6
            and sr["PropertyOverrides"] == [bv["guid"]])


def criterion(tg, sr, cohort, errors):
    source = TREE_SOURCES.get(tg)
    if source:
        path, current, historical = source
        try:
            tree = exports(os.path.join(DATA, "..", path))
            trees = [e for e in tree if e.get("Type") == "StateTree"]
            reference = sr["StateTree"]
            matches = (len(trees) == 1 and reference["ObjectName"] == "StateTree'" + trees[0]["Name"] + "'"
                       and reference["ObjectPath"] == trees[0]["Package"] + "." + str(tree.index(trees[0])))
            expected = current if cohort == "CL533731" else historical if cohort == "CL516586" else None
            if matches and expected and fingerprint(tree) == expected:
                prose = CURRENT_CRITERIA[tg] if cohort == "CL533731" else CRITERIA[tg]
                return "Saved StateTree configuration: " + prose
        except (OSError, ValueError, KeyError):
            pass
    errors.append(f"{tg}: unresolved criteria; missing, changed or unreviewed StateTree/reference")
    return None


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
    shared = exports(os.path.join(DATA, SHARED_CHALLENGES))
    cohort = CHALLENGE_SOURCES.get(fingerprint(shared))
    chal = dict(table(SHARED_CHALLENGES))
    shooting = os.path.join(DATA, SHOOTING_CHALLENGES)
    if os.path.exists(shooting):
        for tg, value in table(SHOOTING_CHALLENGES).items():
            if tg in chal:
                errors.append(f"{tg}: duplicate challenge definition")
                chal[tg] = None
            else:
                chal[tg] = value
    rows = []
    for tg, v in base.items():
        c = chal.get(tg)
        row = {"tag": tg, "name": text(v["DisplayName"]), "steamId": v["SteamAchievementID"],
               "stateTree": None, "autoActivate": None, "rewards": None, "objectives": None,
               "parameter": None, "threshold": None, "unit": None, "criteria": None}
        rows.append(row)
        if c is None:
            errors.append(f"{tg}: unresolved missing or duplicate challenge definition")
            continue
        sr = c.get("StateTreeReference")
        if (not isinstance(sr, dict) or not isinstance(sr.get("StateTree"), dict)
                or not isinstance(sr.get("Parameters"), dict)
                or not isinstance(sr["Parameters"].get("PropertyDescs"), list)
                or "SerialSize" not in sr["Parameters"] or "PropertyOverrides" not in sr):
            errors.append(f"{tg}: unresolved missing StateTree reference or parameter metadata")
            continue
        descs = sr["Parameters"]["PropertyDescs"]
        row.update(stateTree=sr["StateTree"]["ObjectName"].split("'")[1], autoActivate=c["bAutoActivate"],
                   rewards=c["Rewards"], objectives=c["Objectives"], criteria=criterion(tg, sr, cohort, errors))
        bv = BYTE_VALUES.get(tg)
        if bv:
            if not cohort or not parameter_matches(sr, bv):
                errors.append(f"{tg}: unresolved parameter; source, descriptor, type, GUID, size or overrides changed")
                continue
            raw = bytes.fromhex(bv["raw"])
            val = struct.unpack("<i" if bv["type"] == "Int32" else "<f", raw[2:6])[0]
            if raw[:2] != b"\x00\x03" or val != bv["value"]:
                errors.append(f"{tg}: raw bytes do not decode to {bv['value']}")
                continue
            row.update(parameter=bv["param"], threshold=val,
                       unit={"CashThreshold": "cash", "RequiredSeconds": "seconds", "DistanceThreshold": "Unreal units (cm)"}[bv["param"]])
            row["thresholdEvidence"] = ({"status": "saved_package_bytes", "build": cohort,
                                         "rawPackageSha256": CURRENT_RAW_SHA256, "offset": CURRENT_VALUE_OFFSETS[tg],
                                         "raw": bv["raw"]} if cohort == "CL533731" else
                                        {"status": "historical_report", "build": cohort, "source": "docs/evidence/round36-econ.md"})
        elif descs or sr["PropertyOverrides"] or sr["Parameters"]["SerialSize"] not in (0, 2):
            errors.append(f"{tg}: unresolved unreviewed parameter data")
    return rows


def action_tags(value):
    # Old exports use GameplayTags; current exports serialize the same named field as a list.
    if isinstance(value, dict) and set(value) == {"GameplayTags"}:
        value = value["GameplayTags"]
    if not isinstance(value, list) or any(not isinstance(t, str) and not
            (isinstance(t, dict) and set(t) == {"TagName"} and isinstance(t["TagName"], str)) for t in value):
        raise ValueError("RequiresAnyActionTags: unsupported tag container")
    return [tag(t) for t in value]


def wagers(errors):
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
        if "Category" not in v:
            errors.append(f"{k}: unresolved Category; absent from selected export (no proven alias)")
        try:
            requires = action_tags(v["RequiresAnyActionTags"])
        except ValueError as exc:
            errors.append(f"{k}: {exc}")
            requires = None
        conds.append({
            "tag": k, "name": text(v["DisplayName"]), "category": tag(v.get("Category")), "odds": v["Odds"],
            "minValue": v["MinValue"], "maxValue": v["MaxValue"], "valueStep": v["ValueStep"],
            "cooldownSeconds": v["CooldownSeconds"],
            "requiresAnyAction": requires,
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
    doc = {
        "meta": {"source": "Selected saved data/Wardogs exports; achievement thresholds are qualified per row",
                 "script": "_tools/economy_tables.py", "evidence": "Historical: docs/evidence/round36-econ.md; current: thresholdEvidence and source fingerprints",
                 "limits": "Saved asset configuration only; native field identity and effective gameplay remain conditional"},
        "achievements": achievements(errors),
        "wagers": wagers(errors),
        "roleUnlocks": role_unlocks(),
        "platformMastery": platform_mastery(),
        "currencies": currencies(),
    }
    doc["meta"]["unresolved"] = list(errors)
    return doc


def verify_bytes(dirpath, errors):
    try:
        with open(os.path.join(dirpath, "sessionshared.bin"), "rb") as f:
            b = f.read()
    except OSError as exc:
        errors.append(f"parameter bytes unavailable: {exc}")
        return
    cohort = CHALLENGE_SOURCES.get(fingerprint(exports(os.path.join(DATA, SHARED_CHALLENGES))))
    if cohort == "CL516586":
        # Preserve the historical --bytes contract only for the exact historical JSON cohort.
        # This is a local window check, not current-build package identity evidence.
        for tg, bv in BYTE_VALUES.items():
            g = guid_bytes(bv["guid"])
            payload = struct.pack("<i", 6) + bytes.fromhex(bv["raw"])
            positions = [m.start() for m in re.finditer(re.escape(g), b)]
            matches = [i for i in positions if b[i:i + 60].count(payload) == 1]
            if len(matches) != 1:
                errors.append(f"{tg}: expected one historical GUID/value window, found {len(matches)}")
        return
    if hashlib.sha256(b).hexdigest() != CURRENT_RAW_SHA256:
        errors.append("unresolved parameter bytes: package identity is not the reviewed CL533731 capture")
        return
    if cohort != "CL533731":
        errors.append("parameter bytes do not belong to the selected challenge export cohort")
        return
    for tg, bv in BYTE_VALUES.items():
        offset = CURRENT_VALUE_OFFSETS[tg]
        raw = bytes.fromhex(bv["raw"])
        if (b[offset - 4:offset] != struct.pack("<i", 6) or b[offset:offset + 6] != raw
                or b[offset + 6:offset + 26] != struct.pack("<i", 1) + guid_bytes(bv["guid"])):
            errors.append(f"{tg}: parameter block or override differs at the recorded offset")


def main(argv):
    errors = []
    doc = build(errors)
    if "--bytes" in argv:
        before = len(errors)
        verify_bytes(argv[argv.index("--bytes") + 1], errors)
        if len(errors) != before:
            for row in doc["achievements"]:
                if row["tag"] in BYTE_VALUES:
                    row.update(parameter=None, threshold=None, unit=None)
                    row.pop("thresholdEvidence", None)
            doc["meta"]["unresolved"] = list(errors)
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
