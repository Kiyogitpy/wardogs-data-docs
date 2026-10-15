"""Readable sections 3 and 4 of Wardogs_AllVehicles_Stats_Damage_v1.md, rebuilt from data/.

Section 3: each DT_GlobalDamage_VehicleData* table as one table of its damage entries
(category, source tags, hit locations, change), numbered from 0 in file order as the
Season notes cite them. Fields that are empty or default on every entry are left out;
section 5 of the page says which. No-op entries (no source, no hit location, operation
None, amount 0) are counted instead of listed.

Section 4: one row per WDVehicleStatsDataAsset with what section 1 leaves out: the
vendor stat widgets in the order the asset lists them, and the string-table keys
behind the Weaponry and Countermeasures names.

The ### headings already on the page pick the files, so the page keeps its order and
anchors. Rerun after a data update:

    python _tools/vehicle_tables.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "Wardogs_AllVehicles_Stats_Damage_v1.md")
REPO_DATA = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/"
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
HEADING = re.compile(r"^### (.*\]\(" + re.escape(REPO_DATA) + r"(\S+?\.json)\))$", re.M)
ASSET = re.compile(r"^(?:### |\| )(\[`DA_\w+`\]\(" + re.escape(REPO_DATA) + r"(\S+?\.json)\))", re.M)


def exports(rel):
    with open(os.path.join(ROOT, "data", rel), encoding="utf-8") as f:
        return [json.loads(part) for part in EXPORT.split(f.read())[1:]]


def strip(tag, prefix):
    return tag[len(prefix):] if tag.startswith(prefix) else tag


def number(x):
    return f"{x:g}".replace("-", "−")


def change(mod):
    op = mod["Operation"].split("::")[-1]
    amount = mod["Amount"]
    if op == "Percentage_Ongoing":
        return ("+" if amount > 0 else "") + number(amount) + "%"
    if op == "Add":
        return ("+" if amount > 0 else "") + number(amount) + " flat"
    return "none" if amount == 0 else f"{number(amount)} ({op})"


def is_noop(entry):
    mod = entry["OutModification"]
    return (not entry["SourceRequirements"] and not entry["PossibleHitLocations"]
            and mod["Operation"].endswith("::None") and mod["Amount"] == 0)


def damage_table(rel):
    table = next(e for e in exports(rel) if e.get("Type") == "DataTable")
    out = []
    for key, row in table["Rows"].items():
        entries = row["DamageModificationEntries"]
        shown = [(i, e) for i, e in enumerate(entries) if not is_noop(e)]
        skipped = len(entries) - len(shown)
        note = f"{len(entries)} entries."
        if skipped:
            note += f" The {skipped} empty ones, with no source and no change, are not listed."
        out += [f"- **Row:** `{key}`, {note}", "",
                "| # | Category | Source | Hit location | Change |", "|---|---|---|---|---|"]
        for i, e in shown:
            mod = e["OutModification"]
            cat = strip(mod["PriorityCategory"]["TagName"], "Meta.Damage.Category.")
            # Plain text, not code: the site lets code break anywhere, which splits tags mid-word.
            src = " + ".join(strip(t, "Meta.Damage.") for t in e["SourceRequirements"])
            hit = " / ".join(strip(t, "Meta.Damage.HitLocation.") for t in e["PossibleHitLocations"])
            out.append(f"| {i} | {'—' if cat == 'None' else cat} | {src or '—'} | {hit or '—'} | {change(mod)} |")
        out.append("")
    return out


def section3(body):
    """Keep each ### heading and its Package line, replace the rest with the entry table."""
    blocks = re.split(r"(?=^### )", body, flags=re.M)
    out = [blocks[0].splitlines()[0], "",
           "Each table holds one row, named by its gameplay tag, with a list of damage entries. "
           "The tables below list the entries in file order, numbered from 0 as the Season notes "
           "above cite them.", "",
           "- **Category** is the entry's `PriorityCategory` (`Meta.Damage.Category.*`).",
           "- **Source** lists the damage tags in `SourceRequirements`, without the `Meta.Damage.` "
           "prefix. Several tags are joined with +.",
           "- **Hit location** lists `PossibleHitLocations`, without the `Meta.Damage.HitLocation.` "
           "prefix. Several locations are joined with /.",
           "- **Change** is the `Amount`. For `Percentage_Ongoing` entries it reads as a percentage "
           "change, as on the [GameMechanics page](Wardogs_GameMechanics_v2.html#2f-infantry-damage-modification-rules-dt_globaldamage_infantrydata-row-metadamageinfantry); "
           "`Add` entries are marked flat. Section 6 covers what the file leaves open.",
           "- The fields that are empty or default on every entry (instigator and target requirements, "
           "alignment, custom operation, priority index) are left out. Section 5 lists them.", ""]
    for block in blocks[1:]:
        m = HEADING.match(block)
        if not m:
            raise SystemExit("section 3 heading without a data link: " + block.splitlines()[0])
        package = next(l for l in block.splitlines() if l.startswith("- **Package:**"))
        out += ["### " + m.group(1), package] + damage_table(m.group(2)) + [""]
    return "\n".join(out).rstrip("\n") + "\n\n"


def stats_row(heading, rel):
    asset = next(e for e in exports(rel) if e.get("Type") == "WDVehicleStatsDataAsset")
    props = asset["Properties"]
    widgets = [re.search(r"W_VehicleVendor_Stat_(\w+?)_C'", s["ObjectName"]).group(1)
               for s in props.get("Stats", [])]
    keys = lambda name: ", ".join(f"`{strip(n['Key'], 'VehicleStats.Equipment.')}`"
                                  for n in props.get(name, [])) or "—"
    return (f"| {heading} | {', '.join(widgets) or '—'} | "
            f"{keys('VehicleWeaponryNames')} | {keys('VehicleCounterMeasuresNames')} |")


def section4(body):
    """Assets come from the ### headings of the old export, or this table's own first column on a rerun."""
    title = body.splitlines()[0]
    rows = [stats_row(m.group(1), m.group(2)) for m in ASSET.finditer(body)]
    if not rows:
        raise SystemExit("section 4: no stat assets found")
    return "\n".join([
        title, "",
        "What each of the 15 vehicle stat assets holds beyond the six values in section 1: the "
        "vendor stat rows it shows, in its own order, and the string-table keys behind its "
        "Weaponry and Countermeasures names (`STRINGS_VehicleVendor_Stats`, without the "
        "`VehicleStats.Equipment.` prefix). The stat rows are `W_VehicleVendor_Stat_*` widgets "
        "with no values of their own. Asset names link to the full export.", "",
        "| Asset | Vendor stat rows, in order | Weaponry keys | Countermeasure keys |",
        "|---|---|---|---|", *rows, "", "---", "", ""])


def main():
    with open(DOC, encoding="utf-8") as f:
        doc = f.read()
    s3 = doc.index("## 3. ")
    s4 = doc.index("## 4. ")
    s5 = doc.index("## 5. ")
    head3 = doc[s3:s4]
    head3 = head3[:head3.rindex("---")].rstrip("\n")
    doc = doc[:s3] + section3(head3) + "---\n\n" + section4(doc[s4:s5]) + doc[s5:]
    with open(DOC, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)


if __name__ == "__main__":
    main()
