"""Reward values with no zone, a zone and a prio zone, for the sidebar's zone switch.

Writes assets/data/zone-rewards.json (read by assets/js/wd-reading.js) with two parts:

- "challenges": every DT_ChallengeRewards_SessionEvents_* row evaluated (below); the
  docs' challenge tables get a Value column from it.
- "cash": the DT_Reward_Cash_* tables' rows as base x their own ModifierCZ (zone) and
  ModifierHZ (prio zone), keyed by the label each row has in a CASH_DOCS page's table
  under a heading that links that DT_Reward_Cash_* file. The page's base figures swap.

Each row's formula is evaluated as the game's reward calculator does: every formula
variable goes through its selector (first option whose tag query matches the event's
context tags, else the default), then to that variable's literal value. The three
states differ only in context tags, with you and the target on the same footing:

    none  no zone tags
    zone  Instigator.InControlZone + Target.InControlZone
    prio  Instigator.InHotZone + Target.InHotZone (magnet not active)

Runtime game values get neutral defaults (first kill, no repeat victim, crew of one,
build finished). A row whose value scales with a runtime amount the tables don't hold
(the event's base reward, supplies deposited, cash spent, a curve) is written as a
multiple of that amount instead of a cash figure.

    python _tools/zone_rewards.py
    python _tools/zone_rewards.py --check     # assert the Team Offence values (exit 1 on mismatch)

Names are matched case-insensitively. The Team Offence table names its selector and variable keys
"basePoints", "causeMultiplier" while its expression and DefaultOption say "BasePoints",
"CauseMultiplier". The selector and variable maps are TMap<FName, ...> (sdk/raw/WDGame_structs.hpp,
FWDRewardCalculatorExpression), and an FName compares case-insensitively, so the game's lookup
treats them as the same key; the lower-casing below is that rule. The Team Offence table
(DT_ChallengeRewards_TeamOffence) is evaluated too, and its Punish.Kill points under each cause
context are written to the "teamOffence" part of the output.
"""
import ast
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = os.path.join(ROOT, "data", "**", "DT_ChallengeRewards_SessionEvents_*.json")
TEAM_OFFENCE = os.path.join(ROOT, "data", "**", "DT_ChallengeRewards_TeamOffence.json")
OUT = os.path.join(ROOT, "assets", "data", "zone-rewards.json")
CASH_TABLES = os.path.join(ROOT, "data", "**", "DT_Reward_Cash_*.json")
CASH_DOCS = ["Wardogs_Rewards_and_Progression_v2.md"]
BASE_COLUMNS = {"Base", "Base cash"}
CTX = "Challenges.Context."
STATES = {
    "none": set(),
    "zone": {CTX + "Instigator.InControlZone", CTX + "Target.InControlZone"},
    "prio": {CTX + "Instigator.InHotZone", CTX + "Target.InHotZone"},
}
# Runtime values with a natural "plain event" setting; anything else is an unknown amount.
NEUTRAL = {
    "LastVictimCount": 0, "KillStreak": 1, "CrewCount": 1, "HotZoneStreak": 0,
    "RepeatActionCount": 0, "BuildProgress": 1, "PlayersSurvivedCount": 1,
    "InteractionProgress": 1,
}
FUNCS = {"clamp": lambda x, lo, hi: min(max(x, lo), hi), "pow": math.pow, "max": max, "min": min}


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return json.loads(text[text.index("{"):])


def matches(desc, tags):
    """A tag query's AutoDescription, e.g. ' ALL( A,  NONE( B ) )', against the tags set."""
    tokens = re.findall(r"ALL\(|ANY\(|NONE\(|\)|,|[^\s(),]+", desc)
    pos = 0

    def parse():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if not tok.endswith("("):
            return tok in tags
        op, items = tok[:-1], []
        while tokens[pos] != ")":
            if tokens[pos] == ",":
                pos += 1
                continue
            items.append(parse())
        pos += 1
        return {"ALL": all, "ANY": any, "NONE": lambda xs: not any(xs)}[op](items)

    return parse() if tokens else True


def evaluate(expr, values):
    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            return float(node.value)
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -ev(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = ev(node.left), ev(node.right)
            ops = {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b}
            if type(node.op) in ops:
                return ops[type(node.op)]
            if isinstance(node.op, ast.Div):
                return a / b if b else 0.0
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FUNCS:
            return float(FUNCS[node.func.id](*[ev(a) for a in node.args]))
        raise ValueError(f"unsupported: {ast.dump(node)}")

    return ev(ast.parse(expr, mode="eval"))


def resource_values(res, tags):
    """(value, scaled_by) for one resource in one context; scaled_by names the unknown inputs."""
    expr = res["DefaultExpression"]["ExpressionString"]
    selectors = {s["Key"].lower(): s["Value"] for s in res["Selectors"]}
    variables = {v["Key"].lower(): v["Value"] for v in res["Variables"]}
    values, unknown = {}, set()
    for name in set(re.findall(r"[A-Za-z_]\w*", expr)) - set(FUNCS):
        chosen = name
        if name.lower() in selectors:
            sel = selectors[name.lower()]
            chosen = next((o["Variable"] for o in sel["Options"]
                           if matches(o["Condition"]["AutoDescription"], tags)), sel["DefaultOption"])
        var = variables.get(chosen.lower())
        kind = var["VariableType"].split("::")[1] if var else None
        if kind == "Literal":
            values[name] = float(var["LiteralValue"])
        elif kind == "GameValue" and var["GameValue"] in NEUTRAL:
            values[name] = float(NEUTRAL[var["GameValue"]])
        else:
            values[name] = 1.0
            unknown.add(var["GameValue"] if kind == "GameValue" else
                        var["ScalingValueInput"] if kind == "ScalingValue" else chosen)
    return evaluate(expr, values), unknown


def words(text):
    return {w for w in re.split(r"[^a-z0-9]+", text.lower()) if w}


def cash_rows():
    """{table name: [(row key, base, (none, zone, prio))]} from the DT_Reward_Cash_* files."""
    out = {}
    for path in sorted(glob.glob(CASH_TABLES, recursive=True)):
        rows = []
        for key, row in load(path)["Rows"].items():
            base = float(row["base"])
            rows.append((key, base, (base, base * row["ModifierCZ"], base * row["ModifierHZ"])))
        out[os.path.splitext(os.path.basename(path))[0]] = rows
    return out


def cash_labels(tables):
    """{table: {row label as shown: [none, zone, prio]}} for the docs' base-cash tables.

    A row is matched to the data row with the same base whose key shares the most words
    with the label (DefaultReward counts for "default", "no item"); rows with no such
    match, or a tie between rows that scale differently, keep their figure. The label's
    words run together count too ("C4 Explosive" is the key's C4Explosive)."""
    out, skipped = {}, []
    for doc in CASH_DOCS:
        table = None
        lines = open(os.path.join(ROOT, doc), encoding="utf-8").read().splitlines()
        for i, line in enumerate(lines):
            if line.startswith("#"):
                m = re.search(r"(DT_Reward_Cash_\w+)(?:\.json)?", line)
                table = m.group(1) if m else None
                continue
            if not (table in tables and line.startswith("|") and i + 1 < len(lines)
                    and re.match(r"^\|[-| :]+\|$", lines[i + 1].strip())):
                continue
            head = [c.strip() for c in line.strip().strip("|").split("|")]
            col = next((j for j, h in enumerate(head) if h in BASE_COLUMNS), None)
            if col is None:
                continue
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                cells = [re.sub(r"[*`]", "", c).strip() for c in row.strip().strip("|").split("|")]
                label, shown = cells[0], cells[col].replace(",", "")
                if not re.fullmatch(r"\d+(\.\d+)?", shown):
                    continue
                want = words(label) | {"".join(sorted(words(label), key=label.lower().find))}
                if words(label) & {"default", "no"}:
                    want.add("defaultreward")
                same = [(len(want & words(k)), v) for k, b, v in tables[table] if b == float(shown)]
                best = max((s for s, _ in same), default=-1)
                picks = {v for s, v in same if s == best}
                if len(picks) != 1:
                    skipped.append(f"{table}: {label}")
                    continue
                out.setdefault(table, {})[label] = [round(x, 2) for x in picks.pop()]
    return out, skipped


TO_CTX = ["ClaymoreKill", "ExplosiveKill", "EnvironmentKill", "Headshot", "PrecisionArtilleryStrikeKill",
          "SniperKill"]


def team_offence():
    """Forgive and Punish.Kill for the plain case and each cause context (flagged = TeamkillFlagged)."""
    out = {}
    for path in sorted(glob.glob(TEAM_OFFENCE, recursive=True)):
        for row, data in load(path)["Rows"].items():
            res = data["Resources"][0]
            cases = {"plain": set()}
            if row.endswith("Punish.Kill"):
                for c in TO_CTX:
                    cases[c] = {CTX + c}
                cases["TeamkillFlagged"] = {CTX + "TeamkillFlagged"}
                cases["Headshot+TeamkillFlagged"] = {CTX + "Headshot", CTX + "TeamkillFlagged"}
            out[row] = {n: round(resource_values(res["Value"], t)[0], 4) for n, t in cases.items()}
            out[row]["resource"] = res["Key"]["TagName"]
    return out


def check():
    to = team_offence()
    want = {("Challenges.Rewards.TeamOffence.Forgive", "plain"): 500.0,
            ("Challenges.Rewards.TeamOffence.Punish.Kill", "plain"): 5.0,
            ("Challenges.Rewards.TeamOffence.Punish.Kill", "ClaymoreKill"): 1.0,
            ("Challenges.Rewards.TeamOffence.Punish.Kill", "ExplosiveKill"): 4.0,
            ("Challenges.Rewards.TeamOffence.Punish.Kill", "TeamkillFlagged"): 2.0,
            ("Challenges.Rewards.TeamOffence.Punish.Kill", "Headshot"): 5.0}
    bad = [(k, to.get(k[0], {}).get(k[1]), v) for k, v in want.items() if to.get(k[0], {}).get(k[1]) != v]
    for b in bad:
        print("MISMATCH", b)
    if bad:
        raise SystemExit(1)
    print("ok", json.dumps(to, sort_keys=True))


def main():
    if "--check" in sys.argv:
        return check()
    challenges = {}
    for path in sorted(glob.glob(TABLES, recursive=True)) + sorted(glob.glob(TEAM_OFFENCE, recursive=True)):
        for row, data in load(path)["Rows"].items():
            for res in data["Resources"]:
                key = f"{row}|{res['Key']['TagName']}"
                vals, scaled = [], set()
                for tags in STATES.values():
                    v, unknown = resource_values(res["Value"], tags)
                    vals.append(round(v, 4))
                    scaled |= unknown
                challenges[key] = {"v": vals, "per": sorted(scaled)} if scaled else {"v": vals}
    cash, skipped = cash_labels(cash_rows())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"challenges": challenges, "cash": cash, "teamOffence": team_offence()}, f, separators=(",", ":"), sort_keys=True)
    changed = sum(1 for e in challenges.values() if len(set(e["v"])) > 1)
    labels = sum(len(rows) for rows in cash.values())
    print(f"{len(challenges)} challenge rows ({changed} change with the zone), "
          f"{labels} cash rows in {len(cash)} tables, {OUT}")
    for s in skipped:
        print(f"  kept as written (no single match): {s}")


if __name__ == "__main__":
    main()
