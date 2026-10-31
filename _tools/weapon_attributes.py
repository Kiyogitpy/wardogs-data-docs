"""Final Attribute.Gameplay.Weapon.* values for a weapon and an attachment set.

Applies the rules of pipelines/Wardogs_GameplayEffectsPipeline_v1.md §7.1 (what applies to a
weapon) with the stack scaling of §4.2 and the current-value formula of §4.4, to the
item data in data/ and the effect modifiers in assets/data/ge-values.json.

    python _tools/weapon_attributes.py --weapon ID_WEPN_037 [--with ID_X ...]
        [--sight NAME] [--stance Stand|Crouch|Prone] [--bipod | --mounted]
    python _tools/weapon_attributes.py --write   # refresh the marked block in the page

Without --with the weapon carries its default loadout. Each --with attachment goes into
the first free sub-slot that accepts it, replacing the default item there. The sight
defaults to the `SightsData` entry `S_Aim01` (Effects §7.1). An attachment without that
entry gets no sight effects: natively there is no first-entry fallback (0x6C9E190). --mounted
mounts the bipod (it implies unfolded): the unfolded lists are removed and the mounted lists
apply instead.
"""
import argparse
import collections
import glob
import hashlib
import json
import math
import os
import random
import re
import shlex
import shutil
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raw_source_links import source_link, link_generated  # noqa: E402
from ge_values import OPS, SRC, num, short  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "content/Wardogs_WeaponAttributes_v1.md")
BLOCK = re.compile(r"<!-- BEGIN weapon_attributes -->\r?\n.*?<!-- END weapon_attributes -->", re.S)
EXPORT = re.compile(r"^--- export:.*---\s*$", re.M)
SKIP = re.compile(r"BarrelTest")  # vehicle barrel test items, as in recoil_table.py
# FWDBipodAttachmentData +0x138 (unfolded, on the weapon) and +0x148 (unfolded, on the
# character); the cooked names are obfuscated, the SDK gives the order. +0x158 / +0x168 are
# the mounted lists, applied by the Blueprint action B_Action_MountBipod (Effects §7.1).
# The bipod struct is detected by its named MountedAppliedEffects key, so a usmap rename of
# the two hashed keys stops the tool (Item.__init__) instead of silently emptying the lists.
BIPOD_WEAPON = "_aaabgkhkknepnbcppjkao"  # v2 usmap; _aaabgocclgplfdmmfjefm_$E22B6FB53CC5945C$_$22$ before
BIPOD_CHARACTER = "_aaabpbaanpfnnepnbpekp"  # v2 usmap; _aaabpgfgnkcdbhhlgdhmb_$656DA23177B637C1$_$31$ before
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


def nsum(xs):
    """sum() of floats exactly as CPython 3.12+ does it (Neumaier-compensated), on any Python.

    Written out so the result does not depend on the Python version and so the page's evaluator
    (assets/js/loadout-eval.js) can reproduce it bit for bit."""
    it = iter(xs)
    for x in it:
        hi, lo = 0 + x, 0.0
        break
    else:
        return 0
    for x in it:
        t = hi + x
        if abs(hi) >= abs(x):
            lo += (hi - t) + x
        else:
            lo += (x - t) + hi
        hi = t
    return hi + lo if lo and math.isfinite(lo) else hi


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
        # A repeated key keeps its first value: the map load keeps both pairs, and OnRegister
        # (0x6C692E0) installs them in order with overwrite off (0x522F8F0).
        self.base = collections.OrderedDict()
        for k, v in pairs:
            self.base.setdefault(k, v)
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
        self.is_bipod = MOUNTED_WEAPON in ad or MOUNTED_CHARACTER in ad
        if self.is_bipod:
            known = {BIPOD_WEAPON, BIPOD_CHARACTER, MOUNTED_WEAPON, MOUNTED_CHARACTER, "AppliedEffects",
                     "AppliedCharacterEffects"}
            unknown = [k for k, v in ad.items() if k not in known and isinstance(v, list) and any(
                isinstance(r, dict) and "BlueprintGeneratedClass" in r.get("ObjectName", "") for r in v)]
            if unknown:
                raise SystemExit(f"error: {self.path}: bipod effect list under unknown key(s) {', '.join(unknown)}; "
                                 "update BIPOD_WEAPON / BIPOD_CHARACTER")
        self.bipod_weapon = [ge_name(r) for r in ad.get(BIPOD_WEAPON, []) if r]
        self.bipod_character = [ge_name(r) for r in ad.get(BIPOD_CHARACTER, []) if r]
        self.mounted_weapon = [ge_name(r) for r in ad.get(MOUNTED_WEAPON, []) if r]
        self.mounted_character = [ge_name(r) for r in ad.get(MOUNTED_CHARACTER, []) if r]

    def default_sight(self):
        """`S_Aim01` if the attachment has it, else None: no sight effects (no native first-entry fallback)."""
        return DEFAULT_SIGHT if DEFAULT_SIGHT in self.sights else None

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
    """Whether a sub-slot filter lets the item in (native 0x67A2B40, see the page)."""
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
    def __init__(self, data, owner, container, parent=None):
        self.data, self.owner, self.container = data, owner, container
        self.tag = container["ContainerIdentifier"]["TagName"]
        self.parent = parent  # the parent slot's key, None on the weapon
        # The page's slot key: the label path from the weapon down ("Barrel/Muzzle"). Sibling
        # sub-slots never share a tag in the data (export() checks it).
        self.key = f"{parent}/{short_slot(self.tag)}" if parent else short_slot(self.tag)
        self.user = False
        self.item = None
        self.children = []
        self.flag = None  # a missing default item; dropped when the slot is replaced
        # DefaultItems are used only when DefaultContainerItems is empty (0x6784010).
        dci = container.get("DefaultContainerItems") or []
        for d in dci or [{"Item": x} for x in container.get("DefaultItems") or []]:
            tag = (d.get("Item") or {}).get("TagName", "None")
            if tag == "None":
                continue
            it = data.items.get(tag.lower())
            if it is None:
                self.flag = (f"{short_slot(self.tag)} default `{tag}` (on `{owner.asset}`) has no item definition in "
                             "data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects")
                break
            if it.attachment:
                self.place(it)
            break

    def place(self, item):
        self.item = item
        self.flag = None
        self.children = [Slot(self.data, item, c, self.key) for c in item.containers]

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def short_slot(tag):
    return tag.replace("Item.Attachment.", "")


class Loadout:
    def __init__(self, data, weapon, extra=()):
        self.data, self.weapon = data, weapon
        self.slots = [Slot(data, weapon, c) for c in weapon.containers]
        for it in extra:
            self.add(it)

    @property
    def flags(self):
        return {s.flag for s in self.walk() if s.flag}

    def walk(self):
        for s in self.slots:
            yield from s.walk()

    def add(self, item):
        if not item.attachment:
            raise SystemExit(f"error: {item.asset} is not an attachment")
        for s in self.walk():
            if not s.user and accepts(s.container, item):
                s.place(item)
                s.user = True
                return
        free = [short_slot(s.tag) for s in self.walk() if not s.user]
        raise SystemExit(f"error: {item.asset} (context {', '.join(item.context_tags) or 'none'}) is not allowed in any free "
                         f"sub-slot of {self.weapon.asset} (free: {', '.join(free) or 'none'})")

    def choose(self, choices):
        """Explicit choices {slot key: item, or None for empty}, as the page makes them.

        Applied in walk order, so a choice in a sub-slot applies to the sub-slot the chosen (or
        default) parent item brings. Keys of slots that are not open are ignored. Choosing None
        empties the slot; only placing an item drops a missing-default flag (Slot.place)."""
        def visit(slots):
            for s in slots:
                if s.key in choices:
                    it = choices[s.key]
                    if it is None:
                        s.item, s.children = None, []
                    elif not it.attachment or not accepts(s.container, it):
                        raise SystemExit(f"error: {it.asset} is not allowed in sub-slot {s.key} of {self.weapon.asset}")
                    else:
                        s.place(it)
                    s.user = True
                visit(s.children)
        visit(self.slots)
        return self

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
                notes.append(f"`{it.asset}` has no sight `{sight}`; used " + (f"`{name}`" if name else "no sight effects"))
            elif name is None:
                notes.append(f"`{it.asset}` has no `{DEFAULT_SIGHT}` sight; no sight effects applied "
                             "(natively no first-entry fallback)")
            for e in it.sights.get(name, []):
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
        notes.append(f"bipod {'mounted' if mounted else 'unfolded'} but no bipod attachment is equipped")
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
                c.flag = "evaluated live (Effects §4.2)"
                notes.append(f"`{c.app.effect}` {short(attr)} {OPS[m['op']]} current {short(backing)}: "
                             "evaluated against its final value; the game re-evaluates it live (Effects §4.2)")
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
                             "the native order depends on the equip history (not determinable from data); "
                             "the tool used the first in its own order")
        elif base is None:
            final = None
            if live:
                notes.append(f"{short(attr)} is modified but has no base value on this weapon; not evaluated")
        else:
            s = {op: [c.magnitude for c in live if c.mod["op"] == op] for op in OPS}
            mul = 1.0 + nsum(v - 1.0 for v in s["Multiply"])
            div = 1.0 + nsum(v - 1.0 for v in s["Divide"])
            if abs(div) <= EPS:
                div = 1.0
            comp = 1.0
            for v in s["MultiplyCompound"]:
                comp *= v
            final = ((base + nsum(s["Add"])) * mul / div) * comp + nsum(s["AddFinal"])
        if any(c.magnitude is None for c in contrib.get(attr, [])) and final is not None:
            notes.append(f"{short(attr)}: some modifiers were not evaluated, so the final value is partial")
        busy.discard(attr)
        result[attr] = {"base": base, "contrib": contrib.get(attr, []), "final": final, "notes": notes}
        return final

    for attr in contrib:
        current(attr)
    return collections.OrderedDict((a, result[a]) for a in contrib), flags


def compute(data, weapon, extra=(), sight=None, stance="Stand", bipod=False, mounted=False, choices=None):
    loadout = Loadout(data, weapon, extra)
    if choices:
        loadout.choose(choices)
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
        out.append(f"Item `{w.item_id}`, {source_link(w.path, os.path.basename(w.path))}.")
        out.append("")
        lo = [f"{short_slot(t)}: `{it.asset}`" for t, it in loadout.attachments()]
        out.append("- **Loadout:** " + ("; ".join(lo) if lo else "no attachments") + ".")
        sights = [(it, it.default_sight()) for _, it in loadout.attachments() if it.sights]
        if sights:
            out.append("- **Sight:** " + "; ".join(
                (f"`{it.asset}` `{name}`" if name else f"`{it.asset}` no `{DEFAULT_SIGHT}` (no sight effects)")
                + (f" (of {len(it.sights)})" if len(it.sights) > 1 else "")
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
        out.append(f"- **No `{DEFAULT_SIGHT}` sight** (natively no first-entry fallback; the tool applies no sight "
                   "effects): " + "; ".join(
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
        out.append(f"- **Attribute-backed** ({len(backed)} effects, evaluated live, Effects §4.2): " + "; ".join(
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
                       + ". The map load keeps both pairs (`FMapProperty::SerializeItem` adds each entry without a "
                       "lookup when the archetype's map is empty), and `OnRegister` (`0x6C692E0`) installs them in order "
                       "with overwrite off (`0x522F8F0`), so the first value is used"
                       + (": " + ", ".join(f"`{short(k).replace('Weapon.', '')}` {num(v[0])}"
                                           for k, v in w.repeated.items() if len(set(v)) > 1) if differ else "") + ".")
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
    body = link_generated(page(Data())).replace("\n", nl)
    new = BLOCK.sub(lambda _: f"<!-- BEGIN weapon_attributes -->{nl}{body}{nl}<!-- END weapon_attributes -->", text)
    if new != text:
        with open(PAGE, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{'wrote' if new != text else 'unchanged'} {os.path.basename(PAGE)}")


# ------------------------------------------------------------------ page data (--json)


JSON_OUT = os.path.join(ROOT, "assets", "data", "weapon-loadouts.json")
EVAL_JS = os.path.join(ROOT, "assets", "js", "loadout-eval.js")
RUNNER_JS = os.path.join(ROOT, "_tools", "loadout_check.js")
VECTORS = os.path.join(ROOT, "_tools", "loadout_vectors.json")
FILTER_KEYS = (("AllowedSubSlotItems", "allowItems"), ("AllowedSubSlotContext", "allowContext"),
               ("BlockedSubSlotItems", "blockItems"), ("BlockedSubSlotContext", "blockContext"))
DOCS = {
    "rules": "Wardogs_WeaponAttributes_v1.md#rules",
    "choices": "Wardogs_WeaponAttributes_v1.md#choices-this-page-makes",
    "tool": "Wardogs_WeaponAttributes_v1.md#using-the-tool",
    "applies": "../pipelines/Wardogs_GameplayEffectsPipeline_v1.md#71-what-applies-to-a-weapon",
    "modifiers": "../pipelines/Wardogs_GameplayEffectsPipeline_v1.md#42-modifiers",
    "current_value": "../pipelines/Wardogs_GameplayEffectsPipeline_v1.md#44-current-value",
}


def git(*args):
    try:
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def blob_id(path):
    """The git blob id of a file's content with LF line ends (what a commit stores)."""
    with open(path, "rb") as f:
        b = f.read().replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def data_tree():
    tree = git("rev-parse", "HEAD:data")
    if tree is None:   # data/ is no longer tracked: keep the id recorded by the last export that could read it
        try:
            with open(JSON_OUT, encoding="utf-8") as f:
                return json.load(f)["meta"]["source"]["data_tree"]
        except (OSError, ValueError, KeyError):
            return "unknown"
    return tree + ("+dirty" if git("status", "--porcelain", "--", "data") else "")


def export(data):
    """Everything assets/js/loadout-eval.js needs to reproduce compute() (schema in that file)."""
    filters, filter_ix, stances, stance_ix, used, attrs = [], {}, [], {}, [], {}

    def attr(tag):  # attribute tags are stored once, in "attributes"; the rest refers by index
        return attrs.setdefault(tag, len(attrs))

    def slots(owner):
        tags = [c["ContainerIdentifier"]["TagName"] for c in owner.containers]
        if len(set(tags)) != len(tags):
            raise SystemExit(f"error: {owner.asset} has two sub-slots with one tag; the slot keys need them distinct")
        out = []
        for c in owner.containers:
            fl = c.get("Filter", {})
            f = {"mode": fl.get("SupportFilter", "EBHSupportFilterMethod::AllowList").split("::")[-1]}
            f.update({j: list(fl[k]) for k, j in FILTER_KEYS if fl.get(k)})
            key = json.dumps(f, sort_keys=True)
            if key not in filter_ix:
                filter_ix[key] = len(filters)
                filters.append(f)
            s = Slot(data, owner, c)
            e = {"tag": s.tag, "filter": filter_ix[key]}
            if s.item is not None:
                e["default"] = s.item.asset
            if s.flag:
                e["flag"] = s.flag
            out.append(e)
        return out

    def effects(names):
        names = list(names)
        used.extend(names)
        return names

    items = collections.OrderedDict()
    for w in data.weapons:
        st = {k: [[e, n, 1 if custom else 0] for e, n, custom in v] for k, v in w.stance.items()}
        for v in w.stance.values():
            effects(e for e, _, _ in v)
        key = json.dumps(st, sort_keys=True)
        if key not in stance_ix:
            stance_ix[key] = len(stances)
            stances.append(st)
        e = {"itemId": w.item_id, "display": w.display, "archetype": w.archetype,
             "base": [[attr(k), f32(v)] for k, v in w.base.items()], "stance": stance_ix[key]}
        if w.containers:
            e["slots"] = slots(w)
        items[w.asset] = e
    for it in data.attachments:
        if it.asset in items:
            raise SystemExit(f"error: {it.asset} is both a weapon and an attachment; the page data keeps one entry per item")
        e = {"itemId": it.item_id, "display": it.display, "type": it.att_type}
        if it.context_tags:
            e["context"] = it.context_tags
        for k, v in (("applied", it.applied), ("character", it.character)):
            if v:
                e[k] = effects(v)
        if it.sights:
            e["sights"] = [[name, effects(v)] for name, v in it.sights.items()]
        if it.is_bipod:
            e["bipod"] = {"weapon": effects(it.bipod_weapon), "character": effects(it.bipod_character),
                          "mountedWeapon": effects(it.mounted_weapon), "mountedCharacter": effects(it.mounted_character)}
        if it.containers:
            e["slots"] = slots(it)
        items[it.asset] = e

    mods = collections.OrderedDict()
    for name in sorted(set(n for n in used if n in data.effects)):
        out = []
        for m in data.effects[name]["modifiers"]:
            x = {"attr": attr(m["attribute"]), "op": m["op"], "kind": m["kind"]}
            if m["kind"] == "Scalar":
                x["value"] = f32(m.get("value", 0.0))
            if m.get("channel", "Default") != "Default":
                x["channel"] = m["channel"]
            if m.get("curve"):
                x["curve"] = True
            if m.get("curve_indexing", "Fixed") != "Fixed":
                x["indexing"] = m["curve_indexing"]
            if m["kind"] == "Attribute":
                x["backing"] = attr(m["backing_attribute"]) if m.get("backing_attribute") else None
                if "attribute_mode" in m:
                    x["mode"] = m["attribute_mode"]
            if m["kind"] not in ("Scalar", "Attribute") and m.get("allow_fallback"):
                x["fallback"] = f32(m.get("fallback_value", 0.0))
            out.append(x)
        mods[name] = out
    meta = collections.OrderedDict([
        ("generator", "python -I _tools/weapon_attributes.py --json"),
        ("source", {"data_tree": data_tree(), "ge_values_blob": blob_id(SRC)}),
        ("docs", DOCS),
        ("counts", {"weapons": len(data.weapons), "attachments": len(data.attachments), "effects": len(mods),
                    "filters": len(filters), "stance_presets": len(stances)}),
        ("notes", [
            "Attribute tags are in attributes; base entries [attr, value] and modifiers (attr, backing) "
            "refer to them by index.",
            "Numbers are the f32 values the assets store, widened to doubles (Effects §4.4): base values and "
            "Scalar/fallback magnitudes; loadout-eval.js Math.fround()s them again, which changes nothing.",
            "Item ids are asset names (ID_WEPN_037); filters match the ItemId tag (itemId) exactly and context "
            "tags hierarchically, both case-insensitively (WeaponAttributes, Choices: sub-slot filters).",
            "A slot's default is the first real item of DefaultContainerItems, or of DefaultItems when that "
            "is empty; only attachments are placed (ammunition is left out); flag notes a missing item.",
            f"Sight null means {DEFAULT_SIGHT}; an attachment without it gets no sight effects (no first-entry "
            "fallback). Bipod lists: weapon/character = unfolded (+0x138/+0x148), mounted* = "
            "MountedAppliedEffects/MountedAppliedCharacterEffects (+0x158/+0x168), which replace the "
            "unfolded lists while mounted.",
            "Character-side lists (character, bipod character lists) are listed, never evaluated.",
            "Effects referenced by an item but missing here are not in ge-values.json; the evaluator flags them.",
        ]),
    ])
    return collections.OrderedDict([
        ("meta", meta), ("defaultSight", DEFAULT_SIGHT), ("stances", list(STANCES)), ("eps", EPS),
        ("weapons", [w.asset for w in data.weapons]), ("attachments", [it.asset for it in data.attachments]),
        ("attributes", list(attrs)), ("filters", filters), ("stancePresets", stances), ("effects", mods),
        ("items", items)])


def dump_json(obj):
    """Deterministic text: one line per filter, stance preset, effect and item; compact inside."""
    def one(v):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    parts = []
    for k, v in obj.items():
        if k in ("effects", "items", "filters", "stancePresets"):
            rows = [one(x) for x in v] if isinstance(v, list) else [f"{one(ik)}:{one(iv)}" for ik, iv in v.items()]
            o, c = ("[", "]") if isinstance(v, list) else ("{", "}")
            parts.append(f"{one(k)}:{o}\n" + ",\n".join(rows) + f"\n{c}")
        else:
            parts.append(f"{one(k)}:{one(v)}")
    text = "{\n" + ",\n".join(parts) + "\n}\n"
    assert json.loads(text) == json.loads(one(obj))
    return text


def write_if_changed(path, text):
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            old = f.read()
    if old is not None and old.replace("\r\n", "\n") == text:
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return True


def write_json():
    text = dump_json(export(Data()))
    changed = write_if_changed(JSON_OUT, text)
    print(f"{'wrote' if changed else 'unchanged'} {os.path.relpath(JSON_OUT, ROOT)} ({len(text.encode('utf-8'))} bytes)")


# --------------------------------------------------------------- parity (--check)


CHECK_SEED = 20261018
CHECK_RANDOM = 400
CHECK_WITH = 200
BIPOD_STATES = ("folded", "unfolded", "mounted")


def hexf(x):
    """A number as the hex of its double, so the comparison is bit-exact and format-free."""
    return None if x is None else struct.pack(">d", float(x)).hex()


def canonical(loadout, apps, char, attrs, flags):
    """compute()'s result in the shape of loadout-eval.js evaluate(), numbers as hexf()."""
    return {
        "weapon": [{"tag": a, "base": hexf(r["base"]), "final": hexf(r["final"]), "notes": r["notes"],
                    "steps": [{"source": c.app.source, "effect": c.app.effect, "op": c.mod["op"], "kind": c.mod["kind"],
                               "stacks": hexf(c.app.stacks), "magnitude": hexf(c.magnitude), "flag": c.flag}
                              for c in r["contrib"]]} for a, r in attrs.items()],
        "character": [{"effect": e, "source": s} for e, s in char],
        "applications": [{"effect": a.effect, "stacks": hexf(a.stacks), "source": a.source} for a in apps],
        "attachments": [{"key": s.key, "tag": s.tag, "item": s.item.asset} for s in loadout.walk() if s.item is not None],
        "hasBipod": any(it.is_bipod for _, it in loadout.attachments()),
        "notes": flags,
    }


def run_case(data, case):
    choices = {k: (data.by_asset[v.lower()] if v else None) for k, v in case["items"].items()}
    w = data.by_asset[case["weapon"].lower()]
    return canonical(*compute(data, w, (), case["sight"], case["stance"], case["bipod"] == "unfolded",
                              case["bipod"] == "mounted", choices))


def run_args(data, args):
    """The CLI path: the same parser and compute() call as `cli()`."""
    a = parser().parse_args(args)
    w = data.find(a.weapon)
    return canonical(*compute(data, w, [data.find(n) for n in a.with_ or []], a.sight, a.stance, a.bipod, a.mounted))


def check_cases(data):
    """Every weapon's default loadout, CHECK_RANDOM random valid loadouts and CHECK_WITH --with lists."""
    rng = random.Random(CHECK_SEED)
    acc_cache = {}

    def acc(c):
        if id(c) not in acc_cache:
            acc_cache[id(c)] = [it for it in data.attachments if accepts(c, it)]
        return acc_cache[id(c)]

    cases = [{"weapon": w.asset, "items": {}, "sight": None, "stance": "Stand", "bipod": "folded"} for w in data.weapons]
    for _ in range(CHECK_RANDOM):
        w = rng.choice(data.weapons)
        lo, items = Loadout(data, w), {}

        def visit(slots):
            for s in slots:
                opts, r = acc(s.container), rng.random()
                if r < 0.2:
                    pass  # keep the default (key left out)
                elif r < 0.35 or not opts:
                    items[s.key] = None
                    s.item, s.children = None, []
                else:
                    it = rng.choice(opts)
                    items[s.key] = it.asset
                    s.place(it)
                visit(s.children)
        visit(lo.slots)
        names = list(dict.fromkeys(n for _, it in lo.attachments() for n in it.sights))
        cases.append({"weapon": w.asset, "items": items, "sight": rng.choice([None] + names),
                      "stance": rng.choice(STANCES), "bipod": rng.choice(BIPOD_STATES)})
    withs = []
    for _ in range(CHECK_WITH):
        w = rng.choice(data.weapons)
        pool = sorted({it.asset for c in reachable_containers(data, w) for it in acc(c)})
        withs.append({"weapon": w.asset, "ids": rng.sample(pool, min(len(pool), rng.randint(1, 4))) if pool else []})
    return cases, withs


def py_with(data, case):
    try:
        lo = Loadout(data, data.by_asset[case["weapon"].lower()], [data.by_asset[i.lower()] for i in case["ids"]])
    except SystemExit:
        return "error"
    return {s.key: (s.item.asset if s.item else None) for s in lo.walk()}


def py_accepts(data):
    return {f"{o.asset}#{i}": [it.asset for it in data.attachments if accepts(c, it)]
            for o in data.weapons + data.attachments for i, c in enumerate(o.containers)}


def py_defaults(data):
    return {w.asset: {s.key: (s.item.asset if s.item else None) for s in Loadout(data, w).walk()} for w in data.weapons}


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def first_diff(a, b, path=""):
    if type(a) is not type(b):
        return f"{path}: {a!r} != {b!r}"
    if isinstance(a, dict):
        for k in list(a) + [k for k in b if k not in a]:
            if k not in a or k not in b:
                return f"{path}.{k}: only on one side"
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d:
                return d
    elif isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        if len(a) != len(b):
            return f"{path}: length {len(a)} != {len(b)}"
    elif a != b:
        return f"{path}: {a!r} != {b!r}"
    return None


def check():
    """Python vs loadout-eval.js, bit for bit; node runs the JS, else the committed vectors stand in."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    data = Data()
    ok = bad = shown = 0

    def tally(label, good, n_bad, extra=""):
        nonlocal ok, bad
        ok += good
        bad += n_bad
        print(f"{label}: ok={good} mismatched={n_bad}{extra}")

    def show(msg):
        nonlocal shown
        if shown < 10:
            print("  mismatch " + msg)
        shown += 1

    fresh = dump_json(export(data))
    on_disk = None
    if os.path.exists(JSON_OUT):
        with open(JSON_OUT, encoding="utf-8") as f:
            on_disk = f.read().replace("\r\n", "\n")
    stale = on_disk != fresh
    tally("weapon-loadouts.json matches --json", 0 if stale else 1, 1 if stale else 0, " (run --json)" if stale else "")

    cases, withs = check_cases(data)
    py = [run_case(data, c) for c in cases]
    py_w = [py_with(data, c) for c in withs]
    pa, pd = py_accepts(data), py_defaults(data)
    cases_sha = sha([cases, withs])
    node = shutil.which("node")
    if node:
        print(f"mode: node ({node}) runs {os.path.relpath(RUNNER_JS, ROOT)}")
        proc = subprocess.run([node, RUNNER_JS], input=json.dumps({"json": JSON_OUT, "cases": cases, "with": withs}),
                              capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        if proc.returncode:
            raise SystemExit(f"error: node runner failed:\n{proc.stderr}")
        js = json.loads(proc.stdout)
        res, clis, jw, ja, jd, kept = js["results"], js["cli"], js["with"], js["accepts"], js["defaults"], js["normalized"]
        vectors = {"meta": {"note": "loadout-eval.js outputs for --check where node is missing; "
                                    "rewritten by --check where node is installed",
                            "cases_sha256": cases_sha, "json_blob": blob_id(JSON_OUT), "js_blob": blob_id(EVAL_JS),
                            "runner_blob": blob_id(RUNNER_JS)},
                   "results": [sha(r) for r in res], "cli": [[c["args"], c["exact"]] for c in clis],
                   "with": [sha(x) for x in jw], "accepts": sha(ja), "defaults": sha(jd), "normalized": kept}
        wrote = write_if_changed(VECTORS, json.dumps(vectors, indent=1) + "\n")
        print(f"{'wrote' if wrote else 'unchanged'} {os.path.relpath(VECTORS, ROOT)}")
        diff = lambda i: first_diff(py[i], res[i])  # noqa: E731
        w_diff = lambda i: first_diff(py_w[i], jw[i])  # noqa: E731
        a_diff, d_diff = first_diff(pa, ja), first_diff(pd, jd)
    else:
        print(f"mode: vectors ({os.path.relpath(VECTORS, ROOT)}; node not found)")
        with open(VECTORS, encoding="utf-8") as f:
            vec = json.load(f)
        m = vec["meta"]
        for what, want, have in (("the cases", m["cases_sha256"], cases_sha),
                                 ("weapon-loadouts.json", m["json_blob"], blob_id(JSON_OUT)),
                                 ("loadout-eval.js", m["js_blob"], blob_id(EVAL_JS))):
            if want != have:
                raise SystemExit(f"error: the vectors are stale ({what} changed); rerun --check where node is installed")
        clis = [{"args": a, "exact": e} for a, e in vec["cli"]]
        kept = vec["normalized"]
        diff = lambda i: None if sha(py[i]) == vec["results"][i] else "result hash differs"  # noqa: E731
        w_diff = lambda i: None if sha(py_w[i]) == vec["with"][i] else "placement hash differs"  # noqa: E731
        a_diff = None if sha(pa) == vec["accepts"] else "accept lists hash differs"
        d_diff = None if sha(pd) == vec["defaults"] else "default trees hash differs"

    n_def = len(data.weapons)
    diffs = [diff(i) for i in range(len(cases))]
    for i, d in enumerate(diffs):
        if d:
            show(f"loadout {i} {json.dumps(cases[i])}: {d}")
    n_bipod = sum(1 for r in py if r["hasBipod"])
    tally(f"default loadouts ({n_def})", sum(1 for d in diffs[:n_def] if not d), sum(1 for d in diffs[:n_def] if d))
    tally(f"random loadouts ({len(cases) - n_def}, seed {CHECK_SEED}; {n_bipod} with a bipod)",
          sum(1 for d in diffs[n_def:] if not d), sum(1 for d in diffs[n_def:] if d))
    tally(f"normalize() keeps the valid loadouts ({len(cases)})", sum(1 for k in kept if k), sum(1 for k in kept if not k))
    w_diffs = [w_diff(i) for i in range(len(withs))]
    for i, d in enumerate(w_diffs):
        if d:
            show(f"--with placement {json.dumps(withs[i])}: {d}")
    tally(f"--with placements ({len(withs)}; {sum(1 for x in py_w if x == 'error')} rejected by both)",
          sum(1 for d in w_diffs if not d), sum(1 for d in w_diffs if d))
    if a_diff:
        show(f"accept lists: {a_diff}")
    tally(f"sub-slot accept lists ({len(pa)})", 0 if a_diff else len(pa), len(pa) if a_diff else 0)
    if d_diff:
        show(f"default slot trees: {d_diff}")
    tally(f"default slot trees ({len(pd)})", 0 if d_diff else len(pd), len(pd) if d_diff else 0)
    good = n_bad = inexact = 0
    for i, c in enumerate(clis):
        if not c["exact"]:
            inexact += 1
            continue
        d = first_diff(py[i], run_args(data, shlex.split(c["args"])))
        if d:
            n_bad += 1
            show(f"cli {c['args']!r} vs loadout {i}: {d}")
        else:
            good += 1
    tally(f"cli() args round-trip through compute() ({good + n_bad} exact, {inexact} not expressible)", good, n_bad)
    print(f"checks ok={ok} mismatched={bad}")
    if bad:
        raise SystemExit(1)


def parser():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--weapon", help="weapon asset name (ID_WEPN_037) or ItemId")
    ap.add_argument("--with", dest="with_", nargs="+", metavar="ID", help="attachments to equip, in order")
    ap.add_argument("--sight", help=f"SightsData entry to select (default: {DEFAULT_SIGHT}; without it, no sight effects)")
    ap.add_argument("--stance", choices=STANCES, default="Stand")
    ap.add_argument("--bipod", action="store_true", help="bipod unfolded (default folded)")
    ap.add_argument("--mounted", action="store_true",
                    help="bipod mounted (implies unfolded): the mounted lists replace the unfolded ones")
    ap.add_argument("--write", action="store_true", help=f"refresh the marked block in {os.path.basename(PAGE)}")
    ap.add_argument("--json", action="store_true",
                    help=f"write {os.path.relpath(JSON_OUT, ROOT)} for the loadout calculator")
    ap.add_argument("--check", action="store_true",
                    help=f"compare this tool with {os.path.relpath(EVAL_JS, ROOT)} on every default loadout and "
                         "seeded random loadouts (node if installed, else the committed vectors)")
    return ap


def main():
    ap = parser()
    args = ap.parse_args()
    if args.write or args.json or args.check:
        if args.write:
            write()
        if args.json:
            write_json()
        if args.check:
            check()
    elif args.weapon:
        cli(args)
    else:
        ap.error("give --weapon, --write, --json or --check")


if __name__ == "__main__":
    main()
