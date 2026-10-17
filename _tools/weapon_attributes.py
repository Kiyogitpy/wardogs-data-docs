"""Final Attribute.Gameplay.Weapon.* values for a weapon and an attachment set.

Applies the rules of Wardogs_GameplayEffectsPipeline_v1.md §7.1 (what applies to a
weapon) with the stack scaling of §4.2 and the current-value formula of §4.4, to the
item data in data/ and the effect modifiers in assets/data/ge-values.json.

    python _tools/weapon_attributes.py --weapon ID_WEPN_037 [--with ID_X ...]
        [--sight NAME] [--stance Stand|Crouch|Prone] [--bipod | --mounted]
    python _tools/weapon_attributes.py --write   # refresh the marked block in the page

Without --with the weapon carries its default loadout. Each --with attachment goes into
the first free sub-slot that accepts it, replacing the default item there. The sight
defaults to the `SightsData` entry `S_Aim01` (Effects §7.1), or the first entry when an
attachment has none. --mounted mounts the bipod (it implies unfolded): the unfolded lists are
removed and the mounted lists apply instead.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ge_values import OPS, SRC, num, short  # noqa: E402

BLOB = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "Wardogs_WeaponAttributes_v1.md")
BLOCK = re.compile(r"<!-- BEGIN weapon_attributes -->\r?\n.*?<!-- END weapon_attributes -->", re.S)
EXPORT = re.compile(r"^--- export:.*---\s*$", re.M)
SKIP = re.compile(r"BarrelTest")  # vehicle barrel test items, as in recoil_table.py
# FWDBipodAttachmentData +0x138 (unfolded, on the weapon) and +0x148 (unfolded, on the
# character); the cooked names are obfuscated, the SDK gives the order. +0x158 / +0x168 are
# the mounted lists, applied by the Blueprint action B_Action_MountBipod (Effects §7.1).
BIPOD_WEAPON = "_aaabgocclgplfdmmfjefm_$E22B6FB53CC5945C$_$22$"
BIPOD_CHARACTER = "_aaabpgfgnkcdbhhlgdhmb_$656DA23177B637C1$_$31$"
MOUNTED_WEAPON = "MountedAppliedEffects"
MOUNTED_CHARACTER = "MountedAppliedCharacterEffects"
# The sight name the weapon starts with and returns to on every attachment change
# (0x6C90DE0, 0x6C9DC7B; Effects §7.1).
DEFAULT_SIGHT = "S_Aim01"
STANCES = ("Stand", "Crouch", "Prone")
EPS = 1e-8


def f32(x):
    """The value as the float the asset stores, widened to a double (§4.4)."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


def fmt(x, digits=6):
    return "—" if x is None else f"{x:.{digits}g}"


def ge_name(ref):
    if not ref:
        return None
    name = ref["ObjectName"].split("'")[1]
    return name[:-2] if name.endswith("_C") else name


# --------------------------------------------------------------------------- data


class Item:
    def __init__(self, path, objs):
        by_type = collections.defaultdict(list)
        for o in objs:
            by_type[o["Type"]].append(o)
        d = by_type["BHInventoryItemDefinition"][0]
        p = d.get("Properties", {})
        self.path = os.path.relpath(path, ROOT).replace(os.sep, "/")
        self.asset = d["Name"]
        self.item_id = p["ItemId"]["TagName"]
        self.key = self.item_id.lower()
        self.display = (p.get("DisplayName") or {}).get("LocalizedString") or (p.get("DisplayName") or {}).get("SourceString") or ""
        self.context_tags = list(p.get("ItemContext", []))
        self.context = [t.lower() for t in self.context_tags]
        self.archetype = next((t.split(".", 2)[2] for t in p.get("ItemContext", []) if t.startswith("Item.Archetype.")), "Other")
        ss = by_type.get("BHInventoryFragment_SubSlotSupport")
        self.containers = (ss[0].get("Properties", {}).get("Containers", []) if ss else [])
        ge = [o for o in by_type.get("WDItemExtensionData_GameplayEffects", []) if o.get("Properties", {}).get("DefaultAttributes")]
        pairs = [(kv["Key"]["TagName"], kv["Value"]) for kv in (ge[0]["Properties"]["DefaultAttributes"] if ge else [])]
        self.base = collections.OrderedDict(pairs)  # a repeated key keeps its last value
        seen = collections.defaultdict(list)
        for k, v in pairs:
            seen[k].append(v)
        self.repeated = {k: v for k, v in seen.items() if len(v) > 1}
        rw = by_type.get("WDItemExtensionData_RangedWeapon")
        self.ranged = bool(rw)
        self.stance = {}
        for e in (rw[0].get("Properties", {}).get("StanceGameplayEffects", []) if rw else []):
            self.stance[e["Key"].split("::")[-1]] = [(ge_name(x.get("Effect")), x.get("Stacks", 1), x.get("CustomMagnitudes") or [])
                                                     for x in e["Value"].get("Effects", [])]
        att = [o for o in by_type.get("WDInventoryFragment_Attachment", []) if o.get("Properties", {}).get("AttachmentData")]
        ad = att[0]["Properties"]["AttachmentData"] if att else None
        self.attachment = ad is not None
        ad = ad or {}
        self.att_type = (ad.get("AttachmentType") or {}).get("TagName", "")
        self.null_refs = sum(1 for k in ("AppliedEffects", "AppliedCharacterEffects", BIPOD_WEAPON, BIPOD_CHARACTER,
                                       MOUNTED_WEAPON, MOUNTED_CHARACTER)
                             for r in ad.get(k, []) if not r)
        self.applied = [ge_name(r) for r in ad.get("AppliedEffects", []) if r]
        self.character = [ge_name(r) for r in ad.get("AppliedCharacterEffects", []) if r]
        self.sights = collections.OrderedDict(
            (s["Key"], [ge_name(r) for r in s["Value"].get("AppliedEffects", []) if r]) for s in ad.get("SightsData", []))
        self.is_bipod = BIPOD_WEAPON in ad
        self.bipod_weapon = [ge_name(r) for r in ad.get(BIPOD_WEAPON, []) if r]
        self.bipod_character = [ge_name(r) for r in ad.get(BIPOD_CHARACTER, []) if r]
        self.mounted_weapon = [ge_name(r) for r in ad.get(MOUNTED_WEAPON, []) if r]
        self.mounted_character = [ge_name(r) for r in ad.get(MOUNTED_CHARACTER, []) if r]

    def default_sight(self):
        """`S_Aim01` if the attachment has it, otherwise its first `SightsData` entry."""
        return DEFAULT_SIGHT if DEFAULT_SIGHT in self.sights else next(iter(self.sights))

    def label(self):
        return f"{self.display} (`{self.asset}`)" if self.display else f"`{self.asset}`"


class Data:
    def __init__(self):
        with open(SRC, encoding="utf-8") as f:
            self.effects = {e["name"]: e for e in json.load(f)["effects"]}
        self.items = {}
        for path in sorted(glob.glob(os.path.join(ROOT, "data", "**", "ID_*.json"), recursive=True)):
            with open(path, encoding="utf-8") as f:
                objs = [json.loads(p) for p in EXPORT.split(f.read()) if p.strip()]
            if any(o.get("Type") == "BHInventoryItemDefinition" for o in objs):
                it = Item(path, objs)
                self.items[it.key] = it
        self.by_asset = {it.asset.lower(): it for it in self.items.values()}
        self.weapons = sorted((it for it in self.items.values() if it.ranged and it.base and not SKIP.search(it.path)),
                              key=lambda it: (it.archetype, it.display.lower(), it.asset))
        self.attachments = sorted((it for it in self.items.values() if it.attachment), key=lambda it: it.asset.lower())

    def find(self, name):
        it = self.by_asset.get(name.lower()) or self.items.get(name.lower())
        if not it:
            raise SystemExit(f"error: no item named {name!r} (use the asset name, e.g. ID_FGRP_006, or the ItemId)")
        return it


# ------------------------------------------------------------------- sub-slots


def tag_match(tag, wanted):
    """Gameplay-tag match: the tag itself or a child of it (case-insensitive)."""
    wanted = wanted.lower()
    return tag == wanted or tag.startswith(wanted + ".")


def accepts(container, item):
    """Whether a sub-slot filter lets the item in (semantics assumed, see the page)."""
    fl = container.get("Filter", {})
    allowed = item.key in {x.lower() for x in fl.get("AllowedSubSlotItems", [])} or any(
        tag_match(t, a) for t in item.context for a in fl.get("AllowedSubSlotContext", []))
    blocked = item.key in {x.lower() for x in fl.get("BlockedSubSlotItems", [])} or any(
        tag_match(t, b) for t in item.context for b in fl.get("BlockedSubSlotContext", []))
    method = fl.get("SupportFilter", "EBHSupportFilterMethod::AllowList").split("::")[-1]
    if method == "AllowList":
        return allowed
    if method == "BlockList":
        return not blocked
    if method == "AllowPriority":
        return allowed or not blocked
    return allowed and not blocked  # BlockPriority


class Slot:
    def __init__(self, data, owner, container, flags):
        self.data, self.owner, self.container = data, owner, container
        self.tag = container["ContainerIdentifier"]["TagName"]
        self.user = False
        self.item = None
        self.children = []
        for d in (container.get("DefaultContainerItems") or []) + [{"Item": x} for x in container.get("DefaultItems") or []]:
            tag = (d.get("Item") or {}).get("TagName", "None")
            if tag == "None":
                continue
            it = data.items.get(tag.lower())
            if it is None:
                flags.add(f"{short_slot(self.tag)} default `{tag}` (on `{owner.asset}`) has no item definition in data/; "
                          "any effects it has are not included")
                break
            if it.attachment:
                self.place(it, flags)
            break

    def place(self, item, flags):
        self.item = item
        self.children = [Slot(self.data, item, c, flags) for c in item.containers]

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def short_slot(tag):
    return tag.replace("Item.Attachment.", "")


class Loadout:
    def __init__(self, data, weapon, extra=(), flags=None):
        self.data, self.weapon = data, weapon
        self.flags = flags if flags is not None else set()
        self.slots = [Slot(data, weapon, c, self.flags) for c in weapon.containers]
        for it in extra:
            self.add(it)

    def walk(self):
        for s in self.slots:
            yield from s.walk()

    def add(self, item):
        if not item.attachment:
            raise SystemExit(f"error: {item.asset} is not an attachment")
        for s in self.walk():
            if not s.user and accepts(s.container, item):
                s.place(item, self.flags)
                s.user = True
                return
        free = [short_slot(s.tag) for s in self.walk() if not s.user]
        raise SystemExit(f"error: {item.asset} (context {', '.join(item.context_tags) or 'none'}) is not allowed in any free "
                         f"sub-slot of {self.weapon.asset} (free: {', '.join(free) or 'none'})")

    def attachments(self):
        return [(s.tag, s.item) for s in self.walk() if s.item is not None]


def reachable_containers(data, weapon, depth=3):
    """The weapon's sub-slots plus those of any attachment that fits them, to `depth` levels."""
    out, frontier = list(weapon.containers), list(weapon.containers)
    for _ in range(depth - 1):
        nxt = []
        for it in data.attachments:
            if it.containers and any(accepts(c, it) for c in frontier):
                nxt += [c for c in it.containers if not any(c is o for o in out)]
        out += nxt
        frontier = nxt
    return out


# ----------------------------------------------------------------- evaluation


class Application:
    """One ApplyEffect call: an effect, its stack count and where it came from."""

    def __init__(self, effect, stacks, source):
        self.effect, self.stacks, self.source = effect, stacks, source


def applications(data, loadout, sight=None, stance="Stand", bipod=False, mounted=False):
    """Weapon-side applications in the order used for the Override lists, and the character-side effects."""
    weapon_side, character_side, notes = [], [], []
    for _, it in loadout.attachments():
        for e in it.applied:
            weapon_side.append(Application(e, 1, it.asset))
        if it.sights:
            name = sight if sight in it.sights else it.default_sight()
            if sight and sight not in it.sights:
                notes.append(f"`{it.asset}` has no sight `{sight}`; used `{name}`")
            elif not sight and name != DEFAULT_SIGHT:
                notes.append(f"`{it.asset}` has no `{DEFAULT_SIGHT}` sight; used its first entry `{name}`")
            for e in it.sights[name]:
                weapon_side.append(Application(e, 1, f"{it.asset} sight {name}"))
        if mounted and it.is_bipod:
            # Mounted: 0x6C9F6E0 removes the unfolded lists; B_Action_MountBipod applies these.
            for e in it.mounted_weapon:
                weapon_side.append(Application(e, 1, f"{it.asset} bipod mounted"))
            character_side += [(e, f"{it.asset} bipod mounted") for e in it.mounted_character]
        elif bipod and it.is_bipod:
            for e in it.bipod_weapon:
                weapon_side.append(Application(e, 1, f"{it.asset} bipod unfolded"))
            character_side += [(e, f"{it.asset} bipod unfolded") for e in it.bipod_character]
        character_side += [(e, it.asset) for e in it.character]
    if (bipod or mounted) and not any(it.is_bipod for _, it in loadout.attachments()):
        notes.append(f"--{'mounted' if mounted else 'bipod'} given but no bipod attachment is equipped")
    for e, stacks, custom in loadout.weapon.stance.get(stance, []):
        weapon_side.append(Application(e, stacks, f"stance {stance}"))
        if custom:
            notes.append(f"stance effect {e} has CustomMagnitudes, not evaluated")
    return weapon_side, character_side, notes


class Contribution:
    def __init__(self, app, mod):
        self.app, self.mod = app, mod
        self.magnitude = None  # stack-scaled magnitude, or None when it cannot be evaluated
        self.flag = None

    def text(self):
        m = self.mod
        op = OPS.get(m["op"], m["op"])
        if m["kind"] == "Attribute":
            v = f"{short(m.get('backing_attribute'))} ({m.get('attribute_mode', '')})"
            if self.magnitude is not None:
                v += f" = {fmt(self.magnitude)}"
        elif self.magnitude is None:
            v = "?"
        else:
            v = fmt(self.magnitude)
        stacks = f" ×{self.app.stacks} stacks" if self.app.stacks != 1 else ""
        return f"{op} {v} `{self.app.effect}`{stacks}"


def evaluate(data, weapon, apps):
    """Each attribute's base, contributions and current value (§4.2, §4.4)."""
    contrib = collections.OrderedDict((a, []) for a in weapon.base)
    flags = []
    for app in apps:
        eff = data.effects.get(app.effect)
        if eff is None:
            flags.append(f"effect `{app.effect}` ({app.source}) is not in ge-values.json")
            continue
        for m in eff["modifiers"]:
            contrib.setdefault(m["attribute"], []).append(Contribution(app, m))
    result, busy = {}, set()

    def current(attr):
        if attr in result:
            return result[attr]["final"]
        if attr in busy:
            flags.append(f"{short(attr)}: attribute-backed cycle")
            return None
        busy.add(attr)
        base = f32(weapon.base[attr]) if attr in weapon.base else None
        notes = []
        for c in contrib.get(attr, []):
            m, n = c.mod, c.app.stacks
            if m.get("channel", "Default") != "Default":
                c.flag = f"channel {m['channel']}"
            if m["kind"] == "Scalar":
                if m.get("curve") or m.get("curve_indexing", "Fixed") != "Fixed":
                    c.flag = "curve row or non-Fixed indexing; curve not read"
                    notes.append(f"`{c.app.effect}`: {c.flag}")
                    continue
                v = f32(m.get("value", 0.0))
            elif m["kind"] == "Attribute":
                backing = m.get("backing_attribute")
                if m.get("curve"):
                    c.flag = "attribute-backed with a curve; curve not read"
                    notes.append(f"`{c.app.effect}`: {c.flag}")
                    continue
                if m.get("attribute_mode", "Current") == "Current":
                    v = current(backing)
                else:
                    v = f32(weapon.base[backing]) if backing in weapon.base else None
                c.flag = "capture timing not traced"
                notes.append(f"`{c.app.effect}` {short(attr)} {OPS[m['op']]} current {short(backing)}: "
                             "evaluated against its final value; capture timing not traced")
                if v is None:
                    continue
            else:
                c.flag = "SetByCaller; caller value not traced"
                notes.append(f"`{c.app.effect}`: {c.flag}")
                if not m.get("allow_fallback"):
                    continue
                v = f32(m.get("fallback_value", 0.0))
            if n == 0:
                continue
            if m["op"] != "Override":
                ident = 1.0 if m["op"] in ("Multiply", "Divide") else 0.0
                v = (v - ident) * n + ident
            c.magnitude = v
        live = [c for c in contrib.get(attr, []) if c.magnitude is not None and c.app.stacks != 0]
        overrides = [c for c in live if c.mod["op"] == "Override"]
        if overrides:
            final = overrides[0].magnitude
            distinct = {fmt(c.magnitude) for c in overrides}
            if len(distinct) > 1:
                notes.append(f"{len(overrides)} Overrides with different values ({', '.join(sorted(distinct))}); "
                             "the first in application order is used")
        elif base is None:
            final = None
            if live:
                notes.append(f"{short(attr)} is modified but has no base value on this weapon; not evaluated")
        else:
            s = {op: [c.magnitude for c in live if c.mod["op"] == op] for op in OPS}
            mul = 1.0 + sum(v - 1.0 for v in s["Multiply"])
            div = 1.0 + sum(v - 1.0 for v in s["Divide"])
            if abs(div) <= EPS:
                div = 1.0
            comp = 1.0
            for v in s["MultiplyCompound"]:
                comp *= v
            final = ((base + sum(s["Add"])) * mul / div) * comp + sum(s["AddFinal"])
        if any(c.magnitude is None for c in contrib.get(attr, [])) and final is not None:
            notes.append(f"{short(attr)}: some modifiers were not evaluated, so the final value is partial")
        busy.discard(attr)
        result[attr] = {"base": base, "contrib": contrib.get(attr, []), "final": final, "notes": notes}
        return final

    for attr in contrib:
        current(attr)
    return collections.OrderedDict((a, result[a]) for a in contrib), flags


def compute(data, weapon, extra=(), sight=None, stance="Stand", bipod=False, mounted=False):
    loadout = Loadout(data, weapon, extra)
    apps, char, notes = applications(data, loadout, sight, stance, bipod or mounted, mounted)
    attrs, flags = evaluate(data, weapon, apps)
    return loadout, apps, char, attrs, sorted(loadout.flags) + notes + flags


# ------------------------------------------------------------------------ CLI


def cli(args):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    data = Data()
    weapon = data.find(args.weapon)
    if weapon not in data.weapons:
        raise SystemExit(f"error: {weapon.asset} is not a weapon with DefaultAttributes")
    extra = [data.find(n) for n in args.with_ or []]
    loadout, apps, char, attrs, flags = compute(data, weapon, extra, args.sight, args.stance, args.bipod, args.mounted)
    state = "mounted" if args.mounted else "unfolded" if args.bipod else "folded"
    print(f"{weapon.display} ({weapon.asset}), stance {args.stance}, bipod {state}")
    print("Loadout:")
    for tag, it in loadout.attachments():
        print(f"  {short_slot(tag):<12} {it.asset} ({it.display})")
    print("Applications on the weapon, in Override order:")
    for i, a in enumerate(apps, 1):
        print(f"  {i:>2}. {a.effect} x{a.stacks}  [{a.source}]")
    print("Character effects (not on the weapon): " + (", ".join(f"{e} [{s}]" for e, s in char) or "none"))
    print()
    for attr, r in attrs.items():
        print(f"{short(attr)}: base {fmt(r['base'], 10)} -> final {fmt(r['final'], 10)}")
        for c in r["contrib"]:
            print(f"    {c.text().replace('`', '')}  [{c.app.source}]" + (f"  ({c.flag})" if c.flag else ""))
        for n in r["notes"]:
            print(f"    note: {n.replace('`', '')}")
    for f in flags:
        print("flag: " + f.replace("`", ""))


# ----------------------------------------------------------------------- page


ATTR_ORDER = ["VerticalRecoilMultiplier", "HorizontalRecoilMultiplier", "SpreadMultiplier", "AccuracyMultiplier",
              "AimTime", "AdsZoomMultiplier", "MinZeroingRange", "MaxZeroingRange", "EquipSpeedMultiplier",
              "HolsterSpeedMultiplier", "Length"]
ABBR = {"VerticalRecoilMultiplier": "VRecoil", "HorizontalRecoilMultiplier": "HRecoil", "SpreadMultiplier": "Spread",
        "AccuracyMultiplier": "Accuracy", "AimTime": "AimTime", "AdsZoomMultiplier": "ADS zoom",
        "MinZeroingRange": "Zero min", "MaxZeroingRange": "Zero max", "EquipSpeedMultiplier": "Equip",
        "HolsterSpeedMultiplier": "Holster", "Length": "Length"}


def compact(data, effects):
    """An effect list's modifiers as `Attr op value` items."""
    out = []
    for e in effects:
        eff = data.effects.get(e)
        if eff is None:
            out.append(f"`{e}` (not exported)")
            continue
        for m in eff["modifiers"]:
            op = OPS.get(m["op"], m["op"])
            if m["kind"] == "Attribute":
                v = f"current {short(m.get('backing_attribute')).replace('Weapon.', '')}"
            elif m["kind"] == "SetByCaller":
                v = "SetByCaller"
            else:
                v = num(m.get("value", 0))
            out.append(f"{short(m['attribute']).replace('Weapon.', '')} {op} {v}")
    return out


def page(data):
    weapons = data.weapons
    results = {w.key: compute(data, w) for w in weapons}
    all_attrs = []
    for w in weapons:
        for a in w.base:
            s = a.replace("Attribute.Gameplay.Weapon.", "")
            if s not in all_attrs:
                all_attrs.append(s)
    cols = [a for a in ATTR_ORDER if a in all_attrs] + sorted(a for a in all_attrs if a not in ATTR_ORDER)
    flagged = []
    out = [f"Generated by [`_tools/weapon_attributes.py`](_tools/weapon_attributes.py) from `data/` and "
           f"[`assets/data/ge-values.json`](assets/data/ge-values.json): {len(weapons)} weapons, "
           f"{len(data.attachments)} attachment items, {len(cols)} weapon attributes.", ""]

    # 1. Summary
    out += ["## 1. Final values", "",
            "Default loadout, Stand stance, bipod folded. A cell shows `base → final` where the two differ. "
            "Attributes a weapon has no base value for are blank.", "",
            "| Weapon | " + " | ".join(ABBR.get(c, c) for c in cols) + " |",
            "|---|" + "---:|" * len(cols)]
    for w in weapons:
        attrs = results[w.key][3]
        cells = []
        for c in cols:
            r = attrs.get("Attribute.Gameplay.Weapon." + c)
            if not r or r["base"] is None:
                cells.append("")
            elif r["final"] is None:
                cells.append(f"{fmt(r['base'])} → ?")
            elif fmt(r["final"]) == fmt(r["base"]):
                cells.append(fmt(r["base"]))
            else:
                cells.append(f"{fmt(r['base'])} → **{fmt(r['final'])}**")
        out.append(f"| [{w.display or w.asset}](#{anchor(w)}) | " + " | ".join(cells) + " |")
    out.append("")

    # 2. Per weapon
    out += ["## 2. Weapons", "",
            "Each weapon's default loadout (sub-slot: item), the effects applied to it in the order this page "
            "uses for Override lists, and per attribute the base, the modifiers that reach it and the final value. "
            "Modifier magnitudes are the stack-scaled values.", ""]
    archetype = None
    for w in weapons:
        if w.archetype != archetype:
            archetype = w.archetype
            out += [f"### {archetype}", ""]
        loadout, apps, char, attrs, flags = results[w.key]
        out += [f"#### {heading(w)}", ""]
        out.append(f"Item `{w.item_id}`, [`{os.path.basename(w.path)}`]({BLOB}{quote(w.path)}).")
        out.append("")
        lo = [f"{short_slot(t)}: `{it.asset}`" for t, it in loadout.attachments()]
        out.append("- **Loadout:** " + ("; ".join(lo) if lo else "no attachments") + ".")
        sights = [(it, it.default_sight()) for _, it in loadout.attachments() if it.sights]
        if sights:
            out.append("- **Sight:** " + "; ".join(
                f"`{it.asset}` `{name}`" + (f" (of {len(it.sights)})" if len(it.sights) > 1 else "")
                + ("" if name == DEFAULT_SIGHT else f" (no `{DEFAULT_SIGHT}`; first entry)")
                for it, name in sights) + ".")
        st = w.stance.get("Stand")
        out.append("- **Stance (Stand):** " + (", ".join(f"`{e}`" + (f" ×{n}" if n != 1 else "") for e, n, _ in st)
                                              if st else "no stance effect") + ".")
        out.append("- **Character effects:** " + (", ".join(f"`{e}`" for e, _ in char) if char else "none") + ".")
        out += ["", "| Attribute | Base | Modifiers | Final |", "|---|---:|---|---:|"]
        for attr, r in attrs.items():
            mods = "<br>".join(c.text() for c in r["contrib"]) or "—"
            mark = " †" if r["notes"] else ""
            out.append(f"| {short(attr).replace('Weapon.', '')} | {fmt(r['base'])} | {mods} | {fmt(r['final'])}{mark} |")
        out.append("")
        notes = [n for r in attrs.values() for n in r["notes"]] + flags
        if notes:
            out += ["† " + "; ".join(dict.fromkeys(notes)) + ".", ""]
            flagged += [f"{w.label()}: {n}" for n in dict.fromkeys(notes)]

    # 3. Attachments
    accepts_by = collections.defaultdict(list)
    for w in weapons:
        conts = reachable_containers(data, w)
        for it in data.attachments:
            if any(accepts(c, it) for c in conts):
                accepts_by[it.key].append(w)
    groups = collections.OrderedDict()
    orphans = []
    for it in sorted(data.attachments, key=lambda it: (it.att_type.lower(), it.asset.lower())):
        side = it.applied or it.sights or it.bipod_weapon or it.mounted_weapon
        if not accepts_by[it.key]:
            if side or it.character:
                orphans.append(it)
            continue
        groups.setdefault(it.att_type.replace("Item.Attachment.", "") or "(none)", []).append(it)
    listed = sum(len(v) for v in groups.values())
    out += ["## 3. Attachments", "",
            f"The {listed} attachment items at least one weapon accepts, grouped by `AttachmentType`. "
            "**On the weapon** lists the modifiers of `AppliedEffects`; **Sight** those of each "
            "`SightsData` entry in data order; **Bipod unfolded** those of the unfolded list (`+0x138`); "
            "**Bipod mounted** those of `MountedAppliedEffects` (`+0x158`), which replace the unfolded lists "
            "while mounted. **Character** names the effects that go to the character instead "
            "(`AppliedCharacterEffects`, the bipod's unfolded `+0x148` list and its mounted "
            "`MountedAppliedCharacterEffects`, `+0x168`). **Accepted by** lists the weapons with a sub-slot that accepts the item, "
            "on the weapon itself or on an attachment it accepts (a muzzle on a barrel, an underbarrel on a "
            "handguard).", ""]
    for grp, items in groups.items():
        out += [f"### {grp} ({len(items)})", "",
                "| Attachment | Weapon-side modifiers | Character | Accepted by |", "|---|---|---|---|"]
        for it in items:
            parts = []
            if it.applied:
                parts.append("**On the weapon:** " + ", ".join(compact(data, it.applied)))
            for name, effs in it.sights.items():
                parts.append(f"**Sight `{name}`:** " + (", ".join(compact(data, effs)) or "no effects"))
            if it.is_bipod:
                parts.append("**Bipod unfolded:** " + (", ".join(compact(data, it.bipod_weapon)) or "no effects"))
                parts.append("**Bipod mounted:** " + (", ".join(compact(data, it.mounted_weapon)) or "no effects"))
            char = it.character + it.bipod_character + it.mounted_character
            ws = ", ".join(sorted(w.asset.replace("ID_", "") for w in accepts_by[it.key]))
            out.append(f"| {it.label()} | {'<br>'.join(parts) or '—'} | "
                       f"{', '.join(f'`{e}`' for e in char) or '—'} | {ws} |")
        out.append("")

    # 4. Flags
    out += ["## 4. Flagged cases", "",
            "Results above that rest on something not traced or on an odd piece of data.", ""]
    multi = [it for it in data.attachments if len(it.sights) > 1]
    if multi:
        out.append("- **Several sights.** " + "; ".join(f"`{it.asset}` ({', '.join(it.sights)})" for it in multi)
                   + f". §1 and §2 use `{DEFAULT_SIGHT}`, per Effects §7.1; §3 lists each.")
    no_default = [it for it in data.attachments if it.sights and DEFAULT_SIGHT not in it.sights]
    if no_default:
        out.append(f"- **No `{DEFAULT_SIGHT}` sight** (the tool falls back to the first entry): " + "; ".join(
            f"`{it.asset}` ({', '.join(it.sights)})" for it in no_default) + ".")
    if orphans:
        out.append("- **No weapon accepts these attachments** that carry effects: "
                   + ", ".join(f"`{it.asset}`" for it in orphans) + ".")
    dup = [it for it in data.attachments if set(it.applied) & set(it.character)]
    if dup:
        out.append("- **Same effect on the weapon and the character:** " + "; ".join(
            f"`{it.asset}` lists `{', '.join(sorted(set(it.applied) & set(it.character)))}` in both "
            "`AppliedEffects` and `AppliedCharacterEffects`" for it in dup) + ".")
    backed = collections.defaultdict(set)
    for it in data.attachments:
        for e in it.applied + [e for effs in it.sights.values() for e in effs] + it.bipod_weapon + it.mounted_weapon:
            if any(m["kind"] == "Attribute" for m in data.effects.get(e, {}).get("modifiers", [])):
                backed[e].add(it.asset)
    in_default = sorted({w.asset for w in weapons for _, it in results[w.key][0].attachments()
                         if any(it.asset in v for v in backed.values())})
    if backed:
        out.append(f"- **Attribute-backed** ({len(backed)} effects, capture timing not traced): " + "; ".join(
            f"`{e}` on {', '.join(f'`{a}`' for a in sorted(backed[e]))}" for e in sorted(backed))
            + ". Each overrides `MaxZeroingRange` with the current `MinZeroingRange`; the tool uses the final "
            "`MinZeroingRange`. " + (f"In a default loadout on: {', '.join(in_default)}." if in_default
                                     else "None is in a default loadout."))
    for w in weapons:
        if w.repeated:
            differ = [f"`{short(k).replace('Weapon.', '')}` {' then '.join(num(x) for x in v)}"
                      for k, v in w.repeated.items() if len(set(v)) > 1]
            out.append(f"- **Repeated `DefaultAttributes` keys** on {w.label()}: {len(w.repeated)} keys appear twice"
                       + (f", with different values for {', '.join(differ)}" if differ else "")
                       + ". **Assumption:** the last value is used, as a map load that adds each pair in turn keeps it.")
    nulls = [it for it in data.attachments if it.null_refs]
    if nulls:
        out.append("- **Empty effect references** (skipped): " + ", ".join(f"`{it.asset}`" for it in nulls) + ".")
    for w in weapons:
        odd = [f"{s} → `{e}`" for s in STANCES for e, _, _ in w.stance.get(s, [])
               if not e.endswith({"Stand": "_Standing", "Crouch": "_Crouch", "Prone": "_Prone"}[s])]
        if odd:
            out.append(f"- **Stance map** of {w.label()}: " + ", ".join(odd) + " (taken as in data).")
    for f in flagged:
        out.append(f"- {f}.")
    out.append("")
    return "\n".join(out).rstrip("\n")


def heading(w):
    return f"{w.display} ({w.asset})" if w.display else w.asset


def anchor(w):
    text = heading(w).lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def write():
    with open(PAGE, encoding="utf-8", newline="") as f:
        text = f.read()
    if not BLOCK.search(text):
        raise SystemExit(f"error: no BEGIN/END weapon_attributes markers in {os.path.basename(PAGE)}")
    nl = "\r\n" if "\r\n" in text else "\n"
    body = page(Data()).replace("\n", nl)
    new = BLOCK.sub(lambda _: f"<!-- BEGIN weapon_attributes -->{nl}{body}{nl}<!-- END weapon_attributes -->", text)
    if new != text:
        with open(PAGE, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{'wrote' if new != text else 'unchanged'} {os.path.basename(PAGE)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--weapon", help="weapon asset name (ID_WEPN_037) or ItemId")
    ap.add_argument("--with", dest="with_", nargs="+", metavar="ID", help="attachments to equip, in order")
    ap.add_argument("--sight", help=f"SightsData entry to select (default: {DEFAULT_SIGHT}, else the first entry)")
    ap.add_argument("--stance", choices=STANCES, default="Stand")
    ap.add_argument("--bipod", action="store_true", help="bipod unfolded (default folded)")
    ap.add_argument("--mounted", action="store_true",
                    help="bipod mounted (implies unfolded): the mounted lists replace the unfolded ones")
    ap.add_argument("--write", action="store_true", help=f"refresh the marked block in {os.path.basename(PAGE)}")
    args = ap.parse_args()
    if args.write:
        write()
    elif args.weapon:
        cli(args)
    else:
        ap.error("give --weapon or --write")


if __name__ == "__main__":
    main()
