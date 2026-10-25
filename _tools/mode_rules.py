"""Game-mode rules for round 39, rebuilt into assets/data/mode-rules.json.

Collects the mode, lobby and match-flow values that the wiki listed as "not yet known". Two kinds of source:

  config   plain config files read from the paks (data/Wardogs/Config/*.ini, Config/Experiences/*.json and three
           plugin ini files). They are parsed here, so the JSON follows the files.
  native   constructor defaults of native classes. They are not in any cooked asset; they were read from the
           decompiled constructors of the restored exe (docs/evidence/round39-modes-ai-other.md gives each RVA
           and the store). Each entry keeps the raw 32-bit store value and the decoded number; this script
           checks that the decode is right. A value a config file overrides is marked, the default stays.

Also checked against data/: DT_CurrenciesDefinitions (Cash InitialBalance, Gold Bars InitialBalance).

Rerun after a data update (idempotent, stdlib only):

    python -I _tools/mode_rules.py            # rewrite assets/data/mode-rules.json
    python -I _tools/mode_rules.py --check    # exit 1 if the file is stale or a check fails
"""
import glob
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "data", "Wardogs", "Config")
GF = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures")
OUT = os.path.join(ROOT, "assets", "data", "mode-rules.json")
EXPORT = re.compile(r"^--- export: .* ---\s*$", re.M)


def f32(raw):
    return struct.unpack("<f", struct.pack("<I", raw))[0]


# Native constructor stores. raw is the immediate written by the constructor (u32); kind says how to read it.
# Class, constructor RVA, field offset (class layout from sdk/raw), raw store value, kind, decoded value.
NATIVE = [
    # WDMatchState_Playing_KOTH (ControlZoneRuntime), ctor 0x77560C0. +0x50 and +0x54 are one 8-byte store (10).
    ("WDMatchState_Playing_KOTH", "0x77560C0", "ScoreLimit", 0x50, 10, "int", 10),
    ("WDMatchState_Playing_KOTH", "0x77560C0", "ScorePeriod", 0x54, 0, "float", 0.0),
    ("WDMatchState_Playing_KOTH", "0x77560C0", "MinScorePeriod", 0x58, 0x41900000, "float", 18.0),
    ("WDMatchState_Playing_KOTH", "0x77560C0", "MaxScorePeriod", 0x5C, 0x41F00000, "float", 30.0),
    ("WDMatchState_Playing_KOTH", "0x77560C0", "InactivityTimeoutSeconds", 0x60, 0, "float", 0.0),
    ("WDMatchState_Playing_KOTH", "0x77560C0", "MatchHardCapSeconds", 0x64, 0, "float", 0.0),
    # WDMatchState_Playing_Deathmatch (DeathmatchRuntime), ctor 0x848B6F0.
    ("WDMatchState_Playing_Deathmatch", "0x848B6F0", "ScoreLimit", 0x60, 75, "int", 75),
    # WDMatchState_Playing_SniperShowdown (SniperShowdownRuntime), ctor 0x8644A30.
    ("WDMatchState_Playing_SniperShowdown", "0x8644A30", "KillLimit", 0x50, 10, "int", 10),
    # WDHealthRegenComponent (Deathmatch), ctor 0x848B5F0.
    ("WDHealthRegenComponent", "0x848B5F0", "HealthToRegenerate", 0xE8, 0x40A00000, "float", 5.0),
    ("WDHealthRegenComponent", "0x848B5F0", "TickInterval", 0xEC, 0x3F800000, "float", 1.0),
    # WDSniperShowdownStillnessSpottingComponent, ctor 0x8645410 (the Blueprint subclass overrides nothing).
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "UpdateInterval", 0xE0, 0x3F800000, "float", 1.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "unnamed_E4", 0xE4, 0x40A00000, "float", 5.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "DistanceThreshold", 0xE8, 0x459C4000, "float", 5000.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "unnamed_EC", 0xEC, 0x41700000, "float", 15.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "unnamed_F0", 0xF0, 0x42B40000, "float", 90.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "GracePeriod", 0xF4, 0x41700000, "float", 15.0),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "unnamed_F8", 0xF8, 3, "int", 3),
    ("WDSniperShowdownStillnessSpottingComponent", "0x8645410", "unnamed_FC", 0xFC, 0x43480000, "float", 200.0),
    # WDServerSeedingPreLobbyComponent (pre-match lobby award), ctor 0x863D6A0.
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_E0 (first pending award)", 0xE0, 150, "int", 150),
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_E4 (pending award cap)", 0xE4, 5000, "int", 5000),
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_E8 (periodic timer, seconds)", 0xE8, 0x42700000, "float", 60.0),
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_EC (periodic award)", 0xEC, 250, "int", 250),
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_F0 (seconds added to a game-state value)", 0xF0, 0x41700000, "float", 15.0),
    ("WDServerSeedingPreLobbyComponent", "0x863D6A0", "unnamed_F4 (stop threshold, compared with a player-state value)", 0xF4, 60, "int", 60),
    # WDHotPotatoComponent, ctor 0x8636FE0; WDItemExtensionData_HotPotato, ctor 0x8637170.
    ("WDHotPotatoComponent", "0x8636FE0", "unnamed_100", 0x100, 0x40200000, "float", 2.5),
    ("WDItemExtensionData_HotPotato", "0x8637170", "unnamed_48", 0x48, 0x41000000, "float", 8.0),
    ("WDItemExtensionData_HotPotato", "0x8637170", "unnamed_4C", 0x4C, 0x41700000, "float", 15.0),
    ("WDItemExtensionData_HotPotato", "0x8637170", "unnamed_50", 0x50, 0x3F59999A, "float", 0.85),
]

# Hot Potato Blueprint B_HotPotatoComponent: BroadcastHotPotatoMessage(PassMultiplier) -> Amount = 5 * (PassMultiplier * 2).
HOT_POTATO_BP = {
    "component": "B_HotPotatoComponent (WDHotPotatoComponent subclass), added to WDMoverPlayerCharacter",
    "itemtags": ["Id.Item.HotPotato.Alpha", "Id.Item.HotPotato.Charlie", "Id.Item.HotPotato.Bravo"],
    "awardFormula": "Amount = 5 * (PassMultiplier * 2) = 10 * PassMultiplier",
    "awardEvent": "WDPreGameLobbyAwardEvent {PlayerState of the owning player, Amount, ReasonTag}",
    "awardReasonTag": "UI.ServerSeeding.RewardReason.Potato",
    "awardReasonText": "Hot! Hot! Hot!",
    "itemDisplayName": "Gold Potato",
    "itemDescription": "- Don't hold it for too long...",
    "itemFlavor": "Hot. Hot. Hot.",
    "spawnComponent": "B_HotPotatoSpawnComponent (WDHotPotatoSpawnComponent subclass), added to WDGameFrameworkComponentReceiver",
    "throwable": "B_HotPotato_{Alpha,Bravo,Charlie}: WDHotPotatoThrowable, ThrowVelocity 2200 (primary, overarm) and 1400 (secondary, underarm)",
}


def lenient(path):
    """Parse a data/ export file: one JSON value, or several after '--- export:' markers."""
    s = open(path, encoding="utf-8-sig").read()
    parts = [p for p in EXPORT.split(s) if p.strip()]
    out = []
    for p in parts:
        v = json.loads(p)
        out.extend(v if isinstance(v, list) else [v])
    return out


def ini(path):
    """Minimal ini parser: {section: {key: value}} (later '+' lines of one key are kept as a list)."""
    out, sec = {}, None
    for line in open(path, encoding="utf-8-sig"):
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        m = re.match(r"^\[(.+)\]$", line)
        if m:
            sec = out.setdefault(m.group(1), {})
            continue
        if sec is None or "=" not in line:
            continue
        k, v = line.split("=", 1)
        plus = k.startswith("+")
        k = k.lstrip("+-")
        v = v.strip().strip('"')
        if plus:
            sec.setdefault(k, []).append(v)
        else:
            sec[k] = v
    return out


def num(v):
    v = v.rstrip("f")
    return float(v) if re.search(r"[.eE]", v) else int(v)


def build(errors):
    # native values
    native = {}
    for cls, rva, field, off, raw, kind, val in NATIVE:
        got = f32(raw) if kind == "float" else raw
        if abs(got - val) > 1e-6:
            errors.append(f"{cls}.{field}: raw 0x{raw:X} decodes to {got}, not {val}")
        native.setdefault(cls, {"ctorRva": rva, "fields": []})
        if native[cls]["ctorRva"] != rva:
            errors.append(f"{cls}: two ctor RVAs")
        native[cls]["fields"].append({"field": field, "offset": f"0x{off:X}", "raw": f"0x{raw:08X}", "value": val})

    # config files
    ms = ini(os.path.join(CFG, "DefaultMatchState.ini"))
    match_state_ini = {sec.split(".")[-1]: {k: (num(v) if re.match(r"^-?[\d.]+f?$", v) else v) for k, v in kv.items()}
                       for sec, kv in ms.items()}
    srv = ini(os.path.join(CFG, "ServerConfigs", "ExampleStandaloneServerConfig.ini"))
    rot = srv["/Script/WDGame.WDServerMapRotationSettings"]["RotationEntries"]
    ents = [dict(re.findall(r'(\w+)="([^"]*)"', e)) for e in rot]
    tally = {}
    for e in ents:
        k = (e["Map"], e["Experience"])
        tally.setdefault(k, {})
        tally[k][e["ZoneAlternator"]] = tally[k].get(e["ZoneAlternator"], 0) + 1
    example_server = {
        "file": "data/Wardogs/Config/ServerConfigs/ExampleStandaloneServerConfig.ini",
        "MinimumRequiredPlayers": num(srv["MatchState.PreMatch.WaitingForPlayers.PlayerCount"]["MinimumRequiredPlayers"]),
        "KOTH_ScorePeriod": num(srv["MatchState.Playing.KOTH"]["ScorePeriod"]),
        "bLockOverpopulatedTeamsConfig": srv["/Script/WDGame.WDGameStateSession"]["bLockOverpopulatedTeamsConfig"],
        "OverpopulatedTeamThresholdConfig": num(srv["/Script/WDGame.WDGameStateSession"]["OverpopulatedTeamThresholdConfig"]),
        "RotationMode": srv["/Script/WDGame.WDServerMapRotationSettings"]["RotationMode"],
        "rotationEntryCount": len(ents),
        "rotationByMap": [
            {"map": m, "experience": x, "entries": sum(v.values()), "zoneAlternatorCounts": dict(sorted(v.items()))}
            for (m, x), v in sorted(tally.items())
        ],
        "lightingPresets": sorted({e["Lighting"] for e in ents}),
    }
    exp = {}
    for p in sorted(glob.glob(os.path.join(CFG, "Experiences", "**", "*.json"), recursive=True)):
        rel = os.path.relpath(p, os.path.join(CFG, "Experiences")).replace("\\", "/")
        d = json.loads(re.sub(r",\s*([\]}])", r"\1", open(p, encoding="utf-8-sig").read()))
        exp[rel[:-5]] = d
    plugin_ini = {
        "ControlZone.WDControlZoneGameStateComponent.ScorePerControlZoneTick": num(
            ini(os.path.join(GF, "ControlZone", "Config", "DefaultControlZone.ini"))["/Script/ControlZoneRuntime.WDControlZoneGameStateComponent"]["ScorePerControlZoneTick"]),
        "BaseScenario.WDScenarioStateComponent.ScenarioPostMatchTimeoutDuration": num(
            ini(os.path.join(GF, "PvE", "Scenarios", "BaseScenario", "Config", "DefaultBaseScenario.ini"))["/Script/BaseScenarioRuntime.WDScenarioStateComponent"]["ScenarioPostMatchTimeoutDuration"]),
        "BaseScenario.WDScenarioStateComponent.PvEGameEndUiDelay": num(
            ini(os.path.join(GF, "PvE", "Scenarios", "BaseScenario", "Config", "DefaultBaseScenario.ini"))["/Script/BaseScenarioRuntime.WDScenarioStateComponent"]["PvEGameEndUiDelay"]),
        "VehicleUtility.WDVehicleUtilityComponent.MaxVehiclesPerPlayer": num(
            ini(os.path.join(GF, "Vehicles", "VehicleUtility", "Config", "DefaultVehicleUtility.ini"))["/Script/VehicleUtilityRuntime.WDVehicleUtilityComponent"]["MaxVehiclesPerPlayer"]),
    }

    upl = {}
    for name in ("HotPotato", "ServerSeeding", "Deathmatch"):
        u = json.load(open(os.path.join(GF, name, name + ".uplugin"), encoding="utf-8-sig"))
        upl[name] = {"Description": u.get("Description", ""), "BuiltInInitialFeatureState": u.get("BuiltInInitialFeatureState"),
                     "EnabledByDefault": u.get("EnabledByDefault")}
    if "pre-lobby" not in upl["HotPotato"]["Description"]:
        errors.append("HotPotato.uplugin description no longer says pre-lobby")

    # currencies from data/
    cur = lenient(os.path.join(ROOT, "data", "Wardogs", "Content", "Meta", "CurrencyDefinitions", "DT_CurrenciesDefinitions.json"))
    rows = [e for e in cur if e.get("Type") == "DataTable"][0]["Rows"]
    currencies = {k.split(".")[-1]: v["InitialBalance"] for k, v in rows.items()}
    if currencies.get("Cash") != 10000 or currencies.get("GoldBars") != 0:
        errors.append(f"unexpected initial balances: {currencies}")
    if "Intel" in currencies:
        errors.append("Intel is now in DT_CurrenciesDefinitions; update the notes")

    return {
        "meta": {
            "source": "CL516586 paks (config files), restored exe constructors (native), data/ (currencies)",
            "evidence": "docs/evidence/round39-modes-ai-other.md",
            "note": "native defaults are constructor values; a server or runtime option can override them",
        },
        "initialBalances": currencies,
        "matchStateIni": match_state_ini,
        "matchStateIniNote": "DefaultMatchState.ini names WDMatchStateWaitingToStart / InProgress / Ending, classes that are not in this build's SDK; treat as unused legacy config",
        "pluginIni": plugin_ini,
        "upluginDescriptions": upl,
        "exampleServer": example_server,
        "experiences": exp,
        "native": native,
        "hotPotato": HOT_POTATO_BP,
        "teams": {
            "KOTH": "B_FactionSetup_CreateThreeTeams (Alpha, Bravo, Charlie)",
            "Deathmatch": "B_FactionSetup_CreateTwoTeams (Alpha, Bravo)",
        },
    }


def main():
    errors = []
    out = json.dumps(build(errors), indent=1, sort_keys=False) + "\n"
    check = "--check" in sys.argv
    if check:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != out:
            errors.append("assets/data/mode-rules.json is stale; run without --check")
    else:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
    for e in errors:
        print("ERROR:", e)
    print(f"mode_rules: {len(NATIVE)} native fields, {'check' if check else 'wrote ' + os.path.relpath(OUT, ROOT)}; errors {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
