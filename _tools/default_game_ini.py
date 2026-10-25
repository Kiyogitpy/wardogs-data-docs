"""Round 40: gameplay-relevant sections of Wardogs/Config/DefaultGame.ini, rebuilt into assets/data/default-game-ini.json.

DefaultGame.ini is the project config staged in the paks. Round 39 copied it but did not read it; it overrides several
native constructor defaults (match score limits, time limits, lobby minimums) and holds the economy price modifiers.
The full file also holds backend URLs and a bearer token, so it is NOT committed. Only the sections below are kept, in
data/Wardogs/Config/DefaultGame.excerpt.ini (whitelisted by this script; large cosmetic lists such as the phonetic
alphabet and sanitised player names are summarised by count only).

    python -I _tools/default_game_ini.py --extract <path to DefaultGame.ini>   # one-off: rewrite the excerpt
    python -I _tools/default_game_ini.py                                       # rewrite assets/data/default-game-ini.json
    python -I _tools/default_game_ini.py --check                               # exit 1 if stale

Stdlib only; idempotent.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCERPT = os.path.join(ROOT, "data", "Wardogs", "Config", "DefaultGame.excerpt.ini")
OUT = os.path.join(ROOT, "assets", "data", "default-game-ini.json")

WHOLE = [  # sections copied whole
    "/Script/WDGame.WDGameModeSession", "/Script/WDGame.WDGameStateSession", "/Script/WDGame.WDGameSession",
    "MatchState.PreMatch.WaitingForPlayers.ReadyUpKOTH", "MatchState.PreMatch.WaitingForPlayers.PlayerCount",
    "MatchState.Playing.KOTH", "MatchState.Playing.Deathmatch", "MatchState.Playing.SniperShowdown",
    "MatchState.PostMatch", "/Script/WDGame.WDAISubsystem", "/Script/WDGame.WDEconomyConfig",
]
KEYS = {  # sections copied only for these keys
    "/Script/WDGame.WDGameSettings": ["MaxSquadMembers", "SquadLimit", "PlayerHitDetectionBoundsPadding",
        "PronePlayerHitDetectionBoundsPadding", "DownedPlayerHitDetectionBoundsPadding", "MaxShooterDistanceOffset",
        "ProximityChatMaxDist", "TeamLocalChatMaxDist", "MaxChatHistory", "GlobalInteractionTapTime",
        "PlanarSurfaceThicknessScale", "MaxSquadNameLength"],
    "/Script/BHUserSettings.BHUserSettingsConfig": ["RebindExistingKeyMode", "+KeybindingSources", "MinimumAllowedResolution"],
    "/Script/BHEnhancedInput.BHInputSettings": ["+InputContextsToRegister", "+NeverIgnoreInputActions", "ControllerBindPresetOverlayPriority"],
}
COUNTED = ("PhoneticAlphabet", "SanitizedPlayerNames")


def sections(text):
    cur, out = None, {}
    for line in text.replace("﻿", "").splitlines():
        m = re.match(r"^\[(.+)\]\s*$", line)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
        elif cur is not None and line.strip():
            out[cur].append(line.rstrip())
    return out


def extract(src):
    sec = sections(open(src, encoding="utf-8-sig").read())
    out = ["; Excerpt of Wardogs/Config/DefaultGame.ini (round 40). Backend URLs and tokens in the full file are omitted on purpose.",
           "; Rebuild: python -I _tools/default_game_ini.py --extract <DefaultGame.ini>", ""]
    for name in WHOLE:
        out.append("[%s]" % name)
        for ln in sec[name]:
            out.append(ln if len(ln) < 600 else ln[:600] + " ...(line cut)")
        out.append("")
    for name, keys in KEYS.items():
        out.append("[%s]" % name)
        for ln in sec[name]:
            if ln.split("=", 1)[0].strip() in keys:
                out.append(ln)
        out.append("")
    gs = sec["/Script/WDGame.WDGameSettings"]
    counts = {k: sum(1 for ln in gs if ln.lstrip("+").startswith(k + "=")) for k in COUNTED}
    out.append("; counts of omitted lists in [/Script/WDGame.WDGameSettings]: " + json.dumps(counts))
    open(EXCERPT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")


def kv(lines):
    d = {}
    for ln in lines:
        if "=" in ln:
            k, v = ln.split("=", 1)
            k, v = k.strip(), v.strip()
            if k.startswith("+"):
                d.setdefault(k[1:], []).append(v)
            else:
                d[k] = v
    return d


def num(v):
    try:
        f = float(v.rstrip("f"))
        return int(f) if "." not in v else f
    except ValueError:
        return v


def build():
    sec = sections(open(EXCERPT, encoding="utf-8").read())
    r = {"_source": "Wardogs/Config/DefaultGame.ini in the paks (excerpt: data/Wardogs/Config/DefaultGame.excerpt.ini)"}
    r["matchStates"] = {n: {k: num(v) for k, v in kv(sec[n]).items() if not isinstance(v, list)}
                        for n in sec if n.startswith("MatchState.")}
    gm = kv(sec["/Script/WDGame.WDGameModeSession"])
    r["gameModeSession"] = {"bAutoAssignFactions": gm["bAutoAssignFactions"] == "True",
                            "OverrideStartingCash": num(gm["OverrideStartingCash"]),
                            "bSkipDownedState": gm["bSkipDownedState"] == "True"}
    gs = kv(sec["/Script/WDGame.WDGameStateSession"])
    r["gameStateSession"] = {"OverpopulatedTeamThresholdConfig": num(gs["OverpopulatedTeamThresholdConfig"]),
                             "bLockOverpopulatedTeamsConfig": gs["bLockOverpopulatedTeamsConfig"].lower() == "true"}
    se = kv(sec["/Script/WDGame.WDGameSession"])
    r["gameSession"] = {k: num(se[k]) for k in ("LowestAllowedMaxPlayers", "HighestAllowedMaxPlayers", "ServerNameMaxLength")}
    ai = kv(sec["/Script/WDGame.WDAISubsystem"])
    r["aiSubsystem"] = {"NumInitialBots": num(ai["NumInitialBots"]), "BotNames": [b.strip() for b in ai["BotNames"]]}
    eco = sec["/Script/WDGame.WDEconomyConfig"]
    mods = []
    for ln in eco:
        m = re.match(r"^\+PriceModifiers=/Script/WDGame\.WDEntityPriceModifier_(\w+)\((.*)\)$", ln)
        if not m:
            continue
        body = m.group(2)
        ent = {"kind": m.group(1), "multiplier": float(re.search(r"\bMultiplier=([\d.]+)$", body).group(1)),
               "target": re.search(r"EntityTarget=(\w+)", body).group(1)}
        for key, pat in (("faction", r'Faction=\(TagName="([^"]+)"'), ("item", r'Entities=\(GameplayTags=\(\(TagName="([^"]+)"'),
                         ("requiredTag", r'RequiredTag=\(TagName="([^"]+)"'), ("scoreDifference", r"ScoreDifference=(\d+)"),
                         ("levelType", r"LevelType=(\w+)"), ("levelRequirement", r"LevelRequirement=(\w+)"),
                         ("level", r"\bLevel=(\d+)")):
            mm = re.search(pat, body)
            if mm:
                ent[key] = int(mm.group(1)) if key in ("scoreDifference", "level") else mm.group(1)
        mods.append(ent)
    ek = kv(eco)
    r["economy"] = {"priceModifiers": mods, "refundModifier": float(ek["RefundModifier"]),
                    "validRefundActions": re.findall(r'TagName="([^"]+)"', ek["ValidRefundActionTags"]),
                    "refundBlockedContext": re.findall(r'TagName="([^"]+)"', ek["RefundFilter"])}
    g = kv(sec["/Script/WDGame.WDGameSettings"])

    def vec(s):
        return {a: float(b) for a, b in re.findall(r"([XYZ])=([-\d.]+)", s)}
    r["gameSettings"] = {
        "ProximityChatMaxDist": num(g["ProximityChatMaxDist"]), "TeamLocalChatMaxDist": num(g["TeamLocalChatMaxDist"]),
        "MaxChatHistory": num(g["MaxChatHistory"]), "MaxShooterDistanceOffset": num(g["MaxShooterDistanceOffset"]),
        "GlobalInteractionTapTime": num(g["GlobalInteractionTapTime"]),
        "PlayerHitDetectionBoundsPadding": vec(g["PlayerHitDetectionBoundsPadding"]),
        "PronePlayerHitDetectionBoundsPadding": vec(g["PronePlayerHitDetectionBoundsPadding"]),
        "DownedPlayerHitDetectionBoundsPadding": vec(g["DownedPlayerHitDetectionBoundsPadding"]),
        "MaxSquadMembers": num(g["MaxSquadMembers"]), "SquadLimit": num(g["SquadLimit"])}
    inp = kv(sec["/Script/BHEnhancedInput.BHInputSettings"])
    r["input"] = {"mappingContexts": [re.search(r"/(IMC_\w+)\.", c).group(1) for c in inp["InputContextsToRegister"]],
                  "neverIgnore": [re.search(r'TagName="([^"]+)"', c).group(1) for c in inp["NeverIgnoreInputActions"]],
                  "rebindExistingKeyMode": kv(sec["/Script/BHUserSettings.BHUserSettingsConfig"])["RebindExistingKeyMode"]}
    return r


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--extract":
        extract(sys.argv[2])
        return 0
    data = json.dumps(build(), indent=1, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != data:
            print("stale: run python -I _tools/default_game_ini.py")
            return 1
        print("ok")
        return 0
    open(OUT, "w", encoding="utf-8", newline="\n").write(data)
    print("wrote", os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
