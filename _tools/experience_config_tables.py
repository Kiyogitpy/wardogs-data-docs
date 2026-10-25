"""Tables for game-features/Wardogs_ExperienceConfigs_v1.md: the experience definitions, legacy match-state ini and
example server config under data/Wardogs/Config, rebuilt from data/.

Reads Config/Experiences/**/*.json (34 definitions), Config/DefaultMatchState.ini and
Config/ServerConfigs/ExampleStandaloneServerConfig.ini. The server file's password, banner URL and player-id lines
are never printed (whitelisted keys only). Blocks sit between

    <!-- experience_config_tables MODE -->  ...  <!-- /experience_config_tables -->

    python -I _tools/experience_config_tables.py --write   # refresh every block in place
    python -I _tools/experience_config_tables.py --check   # exit 1 when a block is stale
    python -I _tools/experience_config_tables.py MODE      # print one block (counts, experiences, infantry, matchstate,
                                                           #   server, rotation)

Stdlib only; idempotent.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "data", "Wardogs", "Config")
PAGE = "game-features/Wardogs_ExperienceConfigs_v1.md"
BLOCK = re.compile(r"<!-- experience_config_tables (\w+) -->\r?\n.*?<!-- /experience_config_tables -->", re.S)
SERVER_KEYS = {"ServerName", "ServerMinPlayerCash", "ServerMaxPlayerCash", "ServerMinPlayerLevel", "ServerMaxPlayerLevel",
               "MaxReservedSlots", "MinimumRequiredPlayers", "ScorePeriod", "bLockOverpopulatedTeamsConfig",
               "OverpopulatedTeamThresholdConfig", "RestartTimeUtc", "bEnabled", "RotationMode", "MaxAveragePingMilliseconds",
               "bSoftBanKickedPlayers", "WarmupSeconds", "StallSeconds", "MaximumWarmupSeconds", "MeasurementSeconds",
               "SampleIntervalSeconds", "MinimumSampleIntervalSeconds", "ServerHitchSeconds", "MinimumServerFramesPerSecond",
               "DiscardHighestSampleFraction", "PendingSampleLifetimeSeconds", "Port", "bEventFeedEnabled"}
VEHICLE_NAMES = {
    "TNK_01": "Heavy, artillery and anti-air tank bodies (L2A6, SPH-2, Flakpanzer Gepard)",
    "ROT_02": "Havoc attack helicopter",
    "ROT_03_WeaponVariants": "Armed AH-6 variants (AH-6M [Miniguns], AH-6R [Rockets])",
    "WHL_05_Minigun": "Humvee [Minigun]",
    "STN_01": "Talon 9K SAM",
    "STN_02": "Vanguard CIWS",
    "STN_05": "Stingray",
    "TNK_04": "T-72B3",
    "ROT_04_MachineGun": "Z20 Lakota [Miniguns]",
    "WHL_02_RingTurret": "Kodiak [M249]",
    "WHL_05_RingTurret": "Humvee [M249]",
    "WHL_07_ArmouredBattle": "Ural Defender [M249]",
    "WHL_08_RingTurret": "Wolf-110 [M2 Browning]",
}


def experiences():
    out = []
    for p in sorted(glob.glob(os.path.join(CFG, "Experiences", "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8-sig") as f:
            out.append((os.path.relpath(p, os.path.join(CFG, "Experiences")).replace("\\", "/")[:-5], json.load(f)))
    return out


def lst(v, limit=None):
    if not v:
        return ""
    if limit and len(v) > limit:
        return f"{len(v)} entries"
    return ", ".join(f"`{x}`" for x in v)


def counts():
    ex = experiences()
    legacy = [x for x in ex if x[0].startswith("Legacy")]
    return "\n".join(["| Item | Count |", "|---|---|", f"| Experience definitions | {len(ex)} |",
                      f"| Without `EditorVisible` | {sum(1 for _, d in ex if not d.get('EditorVisible'))} |",
                      f"| Legacy and AI scenario definitions | {len(legacy)} |",
                      f"| With rule flags (`FeatureFlags`) | {sum(1 for _, d in ex if d.get('FeatureFlags'))} |"])


def experiences_tab():
    rows = ["| Definition | Alias | Includes | Enables features | Disables features | Rule flags | Disallowed flags | Data layers | Other |",
            "|---|---|---|---|---|---|---|---|---|"]
    for name, d in experiences():
        other = []
        if d.get("PawnData"):
            other.append("pawn data " + d["PawnData"].split(":")[-1])
        if "ReturnToSpawnLockTime" in d:
            other.append(f"ReturnToSpawnLockTime {d['ReturnToSpawnLockTime']}")
        if d.get("PresenceStatus"):
            other.append("presence status set")
        if "EditorVisible" not in d:
            other.append("not editor visible")
        layers = ""
        if d.get("EnabledDataLayers"):
            layers = f"{len(d['EnabledDataLayers'])} enabled"
        if d.get("DisabledDataLayers"):
            layers = "disables " + lst(d["DisabledDataLayers"])
        rows.append(f"| `{name}` | {lst(d.get('Aliases'))} | {lst(d.get('Includes'))} | {lst(d.get('EnabledGameFeatures'), 8)} | "
                    f"{lst(d.get('DisabledGameFeatures'), 14)} | {lst(d.get('FeatureFlags'))} | {lst(d.get('DisallowedFeatureFlags'))} | {layers} | {'; '.join(other)} |")
    return "\n".join(rows)


def infantry():
    d = dict(experiences())["KOTH_InfantryOnly"]
    rows = ["| Disabled feature pack | Vehicle or emplacement it holds |", "|---|---|"]
    for g in d["DisabledGameFeatures"]:
        rows.append(f"| `{g}` | {VEHICLE_NAMES.get(g, '')} |")
    return "\n".join(rows)


def ini(path):
    out, sec = [], None
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"\[(.+)\]$", line)
            if m:
                sec = m.group(1)
            elif "=" in line and sec:
                k, v = line.split("=", 1)
                out.append((sec, k.lstrip("+"), v))
    return out


def matchstate():
    rows = ["| Section | Key | Value |", "|---|---|---|"]
    for s, k, v in ini(os.path.join(CFG, "DefaultMatchState.ini")):
        rows.append(f"| `{s.split('.')[-1]}` | `{k}` | {v} |")
    return "\n".join(rows)


def server():
    rows = ["| Section | Key | Example value |", "|---|---|---|"]
    for s, k, v in ini(os.path.join(CFG, "ServerConfigs", "ExampleStandaloneServerConfig.ini")):
        if k in SERVER_KEYS:
            rows.append(f"| `{s.split('/')[-1]}` | `{k}` | {v if v else '(empty)'} |")
    return "\n".join(rows)


def rotation():
    ents = []
    for s, k, v in ini(os.path.join(CFG, "ServerConfigs", "ExampleStandaloneServerConfig.ini")):
        if k == "RotationEntries":
            ents.append(dict(re.findall(r'(\w+)="([^"]*)"', v)))
    pair = collections.Counter((e["Map"], e["Experience"]) for e in ents)
    light = collections.Counter(e["Lighting"] for e in ents)
    zone = collections.Counter(e["ZoneAlternator"] for e in ents)
    rows = [f"{len(ents)} rotation entries.", "", "| Map | Experience | Entries |", "|---|---|---|"]
    rows += [f"| {m} | `{x}` | {c} |" for (m, x), c in sorted(pair.items())]
    rows += ["", "| Lighting preset | Entries |", "|---|---|"] + [f"| `{k}` | {c} |" for k, c in sorted(light.items())]
    rows += ["", "| Zone alternator | Entries |", "|---|---|"] + [f"| `{k}` | {c} |" for k, c in sorted(zone.items())]
    return "\n".join(rows)


MODES = {"counts": counts, "experiences": experiences_tab, "infantry": infantry, "matchstate": matchstate,
         "server": server, "rotation": rotation}


def regenerate(text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        return nl.join([f"<!-- experience_config_tables {m.group(1)} -->"] + MODES[m.group(1)]().split("\n")
                       + ["<!-- /experience_config_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "counts")]())
    return 0


if __name__ == "__main__":
    sys.exit(main())
