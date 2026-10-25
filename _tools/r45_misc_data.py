"""assets/data/r45-misc.json: round-45 findings that are small tables (idempotent snapshot plus a few joins).

Sources are static: native constructors and functions of WardogsClient-Win64-Shipping.restored.exe (RVAs inline),
cooked World Settings of the four world maps and the Sniper Showdown / Control Zone data-layer cells (dumped with
`WdExtract dump`; the dumps are large and stay outside the repository), the TeamOffence string table, and
`assets/data/vehicle-seats.json` / `data/` for the joins. Nothing was run.

    python -I _tools/r45_misc_data.py           # rewrite assets/data/r45-misc.json
    python -I _tools/r45_misc_data.py --check   # exit 1 when the file is stale
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "r45-misc.json")
SEATS = os.path.join(ROOT, "assets", "data", "vehicle-seats.json")
CURVE = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "PvE", "Scenarios", "BaseScenario",
                     "Content", "ExtractionHelicopter", "Extraction_Helicopter_Speed_Curve_Entry.json")

# WDWorldSettings of each persistent world map (units: Unreal units; WorldToMeters is not stored, so the engine
# default 100 applies and 1 unit = 1 cm).
WORLDS = {
    "Europe": {"defaultExperience": "Madrid_KOTH_01", "killZ": -150000.0,
               "playableBounds": {"min": [-1042343.4, -975825.06], "max": [-190525.48, -201000.0]},
               "worldBounds": {"min": [-1632400.0, -1632400.0, -99075.0], "max": [0.0, 0.0, 18442.0]}},
    "Kavkazi": {"defaultExperience": "Bakurani_KOTH_01", "killZ": -150000.0,
                "playableBounds": {"min": [-1400000.0, -1700000.0], "max": [-300000.0, -600000.0]},
                "worldBounds": {"min": [-1633865.9, -2040857.2, -103095.89], "max": [724.3164, -407388.78, 18638.545]}},
    "NorthAmerica": {"defaultExperience": "Detroit_KOTH_01", "killZ": -150000.0,
                     "playableBounds": {"min": [-620000.0, -600000.0], "max": [430000.0, 320000.0]},
                     "worldBounds": {"min": [-867000.0, -610000.0, -1e10], "max": [867000.0, 610000.0, 1e9]}},
    "Russia": {"defaultExperience": "KOTH", "killZ": None,
               "playableBounds": {"min": [-660000.0, -660000.0], "max": [660000.0, 660000.0]},
               "worldBounds": {"min": [-816000.0, -816000.0, 8121.4907], "max": [816000.0, 816000.0, 66003.19]}},
}

# 100 random Russia streaming cells (seed 5) of 10,746: actor/component classes by count (top rows).
RUSSIA_CELL_SAMPLE = {
    "cellsSampled": 100, "cellsTotal": 10746,
    "topClasses": {"InstancedStaticMeshComponent": 589, "StaticMeshComponent": 212, "SceneComponent": 163,
                   "BodySetup": 152, "EpSpawnedSplineMeshComponent": 111, "HLODInstancedStaticMeshComponent": 107,
                   "PCGPartitionActor": 89, "StaticMeshActor": 77, "ChildActorComponent": 69,
                   "HierarchicalInstancedStaticMeshComponent": 51, "WDDestructionAmbienceVolume": 26,
                   "B_SmashableApartmentSingleWindow_C": 17, "PropVehicle_C": 3},
    "gameplayClassesFound": ["PropVehicle_C (3, parked prop vehicles)", "B_Door_C (5)"],
    "notFound": ["PlayerStart", "spawn volumes", "control-zone actors", "FOB or buildable actors"],
}

SNIPER = {
    "factionPool": {"class": "WDSniperShowdownFactionPool", "classConstructor": "0x8644C80", "entries": 100,
                    "entryNames": "FFAFactionData_001 .. FFAFactionData_100 (display \"FFA %d\")"},
    "assignment": {"function": "0x86464B0 (called from the player-state-added callback 0x864B1D0)",
                   "rule": "each joining player goes to the non-default faction with the fewest members "
                           "(lowest count; the first one wins a tie), so with 100 or fewer players everyone is alone",
                   "factionsCreatedAt": "0x864A150 (BeginPlay hook): one faction actor spawned per pool entry"},
    "lootPointsPerMap": {"Kavkazi": {"HighValue": 87, "MiddleValue": 21, "LowValue": 42, "total": 150},
                         "NorthAmerica": {"HighValue": 69, "MiddleValue": 16, "LowValue": 65, "total": 150},
                         "Russia": {"HighValue": 79, "MiddleValue": 19, "LowValue": 52, "total": 150}},
    "lootPointNote": "WDGameFrameworkComponentReceiver actors with tags Lootable.SniperOnly.{High,Middle,Low}Value in the "
                     "Sniper Showdown data-layer cells (10 cells per map).",
}

TEAM_OFFENCE = {
    "settingsClass": "WDTeamOffenceSettings (UDeveloperSettings, Config)", "constructor": "0x8936700",
    "defaults": {"RejectRewardCooldownSeconds": 900.0, "ApprovalsPerSessionToFlag": 3, "FlaggedVoterWeight": 0.5,
                 "OffenceRelevanceSeconds": 180.0, "SelfDefenceWindowSeconds": 60.0,
                 "ConsequencePointThreshold": 15.0, "BanLengthsInSeconds": [600, 1500, 3600, 86400],
                 "ForgivenessTimeInSeconds": 604800},
    "defaultsNote": "Constructor values; DefaultGame.ini excerpt carries no TeamOffence section, so these apply.",
    "notices": {
        "Notice.TeamOffence.OffenderPunished": "You were punished for a team offence. You have {Points} of {Threshold} points before a kick vote.",
        "Notice.TeamOffence.VoterPunish": "{OffenderName} was punished.",
        "Notice.TeamOffence.VoterForgive": "{OffenderName} was forgiven.",
        "Notice.TeamOffence.VoterKick": "{OffenderName} was punished, they have been banned.",
        "Notice.TeamOffence.OffenderKicked": "Removed for repeated team offences.",
        "Notice.TeamOffence.VoterExpired": "You were removed from the vote on {OffenderName}: no decision was made within {Seconds} seconds.",
        "Notice.TeamOffence.VoterSafeZoneForgive": "You left the safe zone before deciding, so your vote on {OffenderName} was recorded as Forgive."},
    "prompt": {"title": "TEAM KILL", "forgive": "FORGIVE", "punish": "PUNISH", "killer": "KILLER",
               "text": "{OffenderName}\\nHas killed you. Forgive or punish?", "rewardFeed": "Forgave Player"},
}

WATER_HEIGHT = {
    "sampler": {"grid": "0x76C1430", "subsystem": "0x6F771B0", "subsystemGetter": "0x6F77110",
                "users": ["WDMolotovGrenade::Auth_Explode (0x86A15B0)", "0x6E6FD40"]},
    "gridLayout": {"+0x30/+0x38": "world minimum X, Y (double)", "+0x40/+0x48": "world size X, Y (double)",
                   "+0x50/+0x54": "width, height in samples (int32)", "+0x58/+0x60": "height range low, high (double)",
                   "+0x88": "pointer to uint16 samples"},
    "formula": "bilinear blend of the four nearest samples (cell centres at half-sample offsets); a sample of 65535 "
               "means no water and is left out of the blend (weights renormalised); height = low + sample / 65535 "
               "x (high - low); the subsystem returns max(height - query Z, 0), the water depth at the point",
}

HOTZONE_MAGNET = {
    "worldComponent": "WDHotZoneMagnetGameStateComponent (native constructor 0x8566570)",
    "sizeMultiplierFieldOffset": "+0xF8 (vector); speed +0xF0 (float, read only through the Blueprint getter 0x8573ED0)",
    "nativeDefaults": {"speed": 3.0, "sizeMultiplier": [0.6, 0.6, 1.0]},
    "activationHandler": "0x85674A0 (authority-side activation handler; it reads as the rig or tower activation) and client function 0x8571F80: the hot-zone cache "
                         "extents are multiplied component-wise by the world component's size multiplier and the "
                         "result is handed to the control-zone component callback 0x8571E20; the tower number, "
                         "durations and location are stored by 0x856FE50 and replicated",
    "rigDataAssetValues": {"ActivatedHotZoneMagnetSpeed": 5.0, "SizeMultiplier": [0.5, 0.5, 1.0],
                           "note": "The rig data asset carries its own pair; the two activation functions read the "
                                   "world component's pair at +0xF8 (0.6, 0.6, 1.0 by default), not the rig's."},
}


def extraction_curve():
    t = open(CURVE, encoding="utf8").read()
    keys = [(float(a), float(b)) for a, b in re.findall(r'"Time": ([-\d.e]+),\s*"Value": ([-\d.e]+)', t)]
    return {"asset": "Extraction_Helicopter_Speed_Curve_Entry (used by the entry and the exit path)", "keys": keys,
            "mover": "WDQuestNodeLatentAction_WaitForVehicleMovedAlongSpline tick 0x88A48E0: distance += "
                     "Curve(distance / splineLength) x deltaTime, clamped to the spline length "
                     "(USplineComponent length, Unreal units = cm), so the value is cm per second",
            "unit": "cm/s (3 m/s up to 70 percent of the path, then easing to 1 m/s)"}


def seat_roles():
    rows = json.load(open(SEATS, encoding="utf8"))
    c = collections.Counter(r["role"] for r in rows)
    veh = collections.defaultdict(set)
    for r in rows:
        veh[r["role"]].add(r["plugin"])
    return {"seatsByRole": dict(sorted(c.items())),
            "pluginsByRole": {k: sorted(v) for k, v in sorted(veh.items())},
            "passiveOnly": "SPW_01 (M113): seats 1 to 9",
            "rules": "All 17 gameplay-state queries and the Sprint, TacSprint and ping-request blocks that name a "
                     "vehicle role list State.Player.Vehicle.Role.ActivePassenger and .PassivePassenger together.",
            "inputContexts": "MVehicleInputControlsDataAsset has separate ActivePassenger and PassivePassenger "
                             "InputMappingContexts arrays; none of the 15 cooked input-controls assets sets either "
                             "(only DriverInputMappingContexts, and Gunner on 2)."}


def build():
    return {
        "worlds": WORLDS, "worldUnits": "WorldToMeters is not stored in any of the four WDWorldSettings, so the "
                                       "engine default 100 applies: 1 Unreal unit = 1 cm",
        "russiaCellSample": RUSSIA_CELL_SAMPLE, "sniperShowdown": SNIPER, "teamOffence": TEAM_OFFENCE,
        "waterHeight": WATER_HEIGHT, "hotZoneMagnet": HOTZONE_MAGNET, "extractionHelicopter": extraction_curve(),
        "vehicleSeatRoles": seat_roles(),
        "flareRestock": {"item": "Id.Item.Flares (FlaresIdTag of each DA_*GameplaySystems)",
                         "addHandler": "0x767E260 via OnItemAdded 0x7689D10: on the authority, when the added item tag "
                                       "equals the flare tag, CurrentFlaresAmount (+0x790) += Delta, replicate, then "
                                       "broadcast 0x7673540 (Client_FlaresRestocked)",
                         "removeHandler": "0x767E3A0 via OnItemRemoved 0x7689EE0: count -= Delta",
                         "smoke": "same handlers: the smoke block (+0x350) count at +0x7B4 follows its own item tag",
                         "vendorRow": {"table": "DT_VendorData_Ext_Flares", "price": 750.0, "amount": 1,
                                       "levelToUnlock": 1, "category": "Vendor.Category.Vehicle.CounterMeasures"}},
        "tyreStateWriter": {"function": "0x537C580", "binding": "0x5356B00 binds it to each wheel's health attribute",
                            "states": "0 intact, 1 damaged (health / max health at or below the trigger threshold, "
                                      "55 percent in the cooked triggers), 2 destroyed (health 0); byte array at +0x9B0, "
                                      "replicated (copy at +0x9D8), change handler 0x5370A40 refreshes the wheel mesh"},
        "pawnUnitSystems": {"aiPerception": "SightRadius 200000 and HearingRange 100000 are Unreal units (cm): 2,000 m and 1,000 m",
                            "vendorSpeedLabel": "STRINGS_VehicleVendor_Stats VehicleStats.Title.MaxSpeed = \"Max Speed (KM/H)\""},
    }


def main():
    text = json.dumps(build(), indent=1, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
        sys.exit(0 if cur == text else 1)
    with open(OUT, "w", encoding="utf8", newline="\n") as fh:
        fh.write(text)
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
