"""Evaluate every challenge-reward row with no zone, a zone and a prio zone.

Reads the four DT_ChallengeRewards_SessionEvents_* tables under data/ and writes
assets/data/zone-rewards.json, which the sidebar's zone toggle (assets/js/wd-reading.js)
uses to fill a value column in the docs' challenge-reward tables.

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
"""
import ast
import glob
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = os.path.join(ROOT, "data", "**", "DT_ChallengeRewards_SessionEvents_*.json")
OUT = os.path.join(ROOT, "assets", "data", "zone-rewards.json")
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
    selectors = {s["Key"]: s["Value"] for s in res["Selectors"]}
    variables = {v["Key"]: v["Value"] for v in res["Variables"]}
    values, unknown = {}, set()
    for name in set(re.findall(r"[A-Za-z_]\w*", expr)) - set(FUNCS):
        chosen = name
        if name in selectors:
            sel = selectors[name]
            chosen = next((o["Variable"] for o in sel["Options"]
                           if matches(o["Condition"]["AutoDescription"], tags)), sel["DefaultOption"])
        var = variables.get(chosen)
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


def main():
    out = {}
    for path in sorted(glob.glob(TABLES, recursive=True)):
        for row, data in load(path)["Rows"].items():
            for res in data["Resources"]:
                key = f"{row}|{res['Key']['TagName']}"
                vals, scaled = [], set()
                for tags in STATES.values():
                    v, unknown = resource_values(res["Value"], tags)
                    vals.append(round(v, 4))
                    scaled |= unknown
                out[key] = {"v": vals, "per": sorted(scaled)} if scaled else {"v": vals}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    changed = sum(1 for e in out.values() if len(set(e["v"])) > 1)
    print(f"{len(out)} rows written, {changed} change with the zone, {OUT}")


if __name__ == "__main__":
    main()
