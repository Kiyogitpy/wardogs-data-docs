"""Tables for game-features/Wardogs_AttachmentsPlatforms_v1.md, rebuilt from data/ and assets/data/ge-values.json.

Reads every `ID_*` item that carries a `WDInventoryFragment_Attachment` (the attachments), every
ranged weapon (the platforms), the 12 slot archetypes under Content/Items/Attachments/Archetypes and
the effect modifiers of assets/data/ge-values.json. Item loading, sub-slot filters and the default
loadout reuse _tools/weapon_attributes.py, so the two pages agree. Each table sits between

    <!-- attachment_tables MODE -->  ...  <!-- /attachment_tables -->

on the page. Rerun after a data update (idempotent):

    python _tools/attachment_tables.py --write      # refresh every block in place
    python _tools/attachment_tables.py --check      # exit 1 when a block on the page is stale
    python _tools/attachment_tables.py MODE         # print one block (counts, archetypes, platforms,
                                                    #   slots, items, effects, bipods, noeffect, attributes)
"""
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raw_source_links import source_link, link_generated  # noqa: E402
import weapon_attributes as wa  # noqa: E402
from ge_values import OPS, num, short  # noqa: E402

ROOT = wa.ROOT
PAGE = "game-features/Wardogs_AttachmentsPlatforms_v1.md"
BLOCK = re.compile(r"<!-- attachment_tables (\w+) -->\r?\n.*?<!-- /attachment_tables -->", re.S)
ARCH_DIR = "data/Wardogs/Content/Items/Attachments/Archetypes"
HIDE_CTX = {"item.context.equippable"}


# --- loading ------------------------------------------------------------------------------------

def raw(item):
    """The item's export objects, by Type."""
    with open(os.path.join(ROOT, item.path), encoding="utf-8") as f:
        objs = [json.loads(p) for p in wa.EXPORT.split(f.read()) if p.strip()]
    out = collections.defaultdict(list)
    for o in objs:
        out[o["Type"]].append(o.get("Properties") or {})
    return out


def first(by_type, typ):
    return (by_type.get(typ) or [{}])[0]


class Extra:
    """Fields of an item that weapon_attributes.Item does not keep."""

    def __init__(self, item):
        t = raw(item)
        self.weight = first(t, "BHInventoryFragment_Weight").get("Weight")
        dim = first(t, "BHInventoryFragment_CustomShape").get("Dimensions")
        self.grid = f"{dim['X']}x{dim['Y']}" if dim else None
        ad = (first(t, "WDInventoryFragment_Attachment").get("AttachmentData")) or {}
        self.ad = ad
        self.removable = ad.get("bCanBeRemovedInGame")
        self.discard = ad.get("bDiscardWhenEmptyOnReload")
        self.clearable = first(t, "WDInventoryFragment_Gunsmith").get("ClearableAttachmentSlots", [])
        self.gunsmith_type = first(t, "WDInventoryFragment_Gunsmith").get("ItemType", "").split("::")[-1]


def load():
    d = wa.Data()
    d.extra = {it.key: Extra(it) for it in list(d.attachments) + list(d.weapons)}
    d.archetypes = []
    for path in sorted(glob.glob(os.path.join(ROOT, ARCH_DIR, "DA_*.json"))):
        with open(path, encoding="utf-8") as f:
            for p in wa.EXPORT.split(f.read()):
                if p.strip():
                    o = json.loads(p)
                    pr = o.get("Properties") or {}
                    d.archetypes.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), o["Name"], pr.get("AttachmentId", {}).get("TagName", ""),
                                         pr.get("AttachBoneName", ""), str(pr.get("AttachmentType", "")).split("::")[-1]))
    d.fits = fits(d)
    return d


def wname(w):
    return w.display or w.asset.replace("ID_", "")


def fits(d):
    """attachment key -> {slot label: set of weapon names}; same 3-level reach as weapon_attributes.reachable_containers."""
    res = collections.defaultdict(lambda: collections.defaultdict(set))
    for w in d.weapons:
        frontier = [(wa.short_slot(c["ContainerIdentifier"]["TagName"]), c) for c in w.containers]
        for _ in range(3):
            nxt, seen = [], set()
            for label, c in frontier:
                for a in d.attachments:
                    if wa.accepts(c, a):
                        res[a.key][label].add(wname(w))
                        for sc in a.containers:
                            lab = f"{label}>{wa.short_slot(sc['ContainerIdentifier']['TagName'])}"
                            key = (lab, json.dumps(sc.get("Filter", {}), sort_keys=True))
                            if key not in seen:
                                seen.add(key)
                                nxt.append((lab, sc))
            frontier = nxt
    return res


# --- helpers ------------------------------------------------------------------------------------

def link(item, label=None):
    return source_link(item.path, label or item.asset)


def tname(d, tag):
    it = d.items.get(tag.lower())
    return it.asset if it else tag


def n(x):
    return "-" if x is None else num(x)


def esc(s):
    return str(s).replace("|", "\\|")


def type_label(it):
    return it.att_type.replace("Item.Attachment.", "") or "(none)"


def groups(d):
    g = collections.OrderedDict()
    for it in sorted(d.attachments, key=lambda i: (type_label(i).lower(), i.asset.lower())):
        g.setdefault(type_label(it), []).append(it)
    return g


def mods(d, effect):
    """An effect's modifiers as `Attr op value` strings."""
    return wa.compact(d, [effect])


def eff_text(d, effects, empty="-"):
    if not effects:
        return empty
    parts = []
    for e in effects:
        m = mods(d, e)
        parts.append(f"`{e}`: " + ("; ".join(m) if m else "no modifiers"))
    return "<br>".join(parts)


def filt(d, c):
    f = c.get("Filter", {})
    method = f.get("SupportFilter", "").split("::")[-1]
    parts = []
    for key, label in (("AllowedSubSlotItems", "allow items"), ("AllowedSubSlotContext", "allow ctx"),
                       ("BlockedSubSlotItems", "block items"), ("BlockedSubSlotContext", "block ctx")):
        v = f.get(key) or []
        if v:
            parts.append(f"{label}: " + ", ".join(f"`{tname(d, x).replace('ID_', '') if 'items' in label else x}`" for x in v))
    return method, "; ".join(parts) or "-"


def fits_text(d, it):
    by = d.fits.get(it.key)
    if not by:
        return "none"
    inv = collections.defaultdict(list)
    for label, ws in by.items():
        for w in ws:
            inv[w].append(label)
    byset = collections.defaultdict(list)
    for w, labs in inv.items():
        byset[tuple(sorted(labs))].append(w)
    return "<br>".join(f"{', '.join(labs)}: {', '.join(sorted(ws))}" for labs, ws in sorted(byset.items(), key=lambda kv: -len(kv[1])))


def weapon_slots(d, w):
    return [wa.short_slot(c["ContainerIdentifier"]["TagName"]) for c in w.containers]


# --- tables -------------------------------------------------------------------------------------

def counts(d):
    side = lambda it: it.applied or any(it.sights.values()) or it.bipod_weapon or it.mounted_weapon  # noqa: E731
    noeff = [it for it in d.attachments if not (side(it) or it.character or it.bipod_character or it.mounted_character)]
    nofit = [it for it in d.attachments if it.key not in d.fits]
    attrs = sorted({m["attribute"] for e in d.effects.values() for m in e["modifiers"]})
    return "\n".join([
        f"- Attachment items (`WDInventoryFragment_Attachment` with attachment data): **{len(d.attachments)}**, in {len(groups(d))} attachment types.",
        f"- Items with an attachment fragment whose `AttachmentData` is null: **{len(null_frag(d))}** (listed under section 7).",
        f"- Slot archetype assets: **{len(d.archetypes)}**.",
        f"- Weapon platforms (ranged weapons with base attributes): **{len(d.weapons)}**.",
        f"- Attachments that change nothing in data (no weapon or character effect): **{len(noeff)}**.",
        f"- Attachments no weapon sub-slot accepts, to three nesting levels: **{len(nofit)}**.",
        f"- Gameplay effects in `ge-values.json` reached by an attachment: **{len(used_effects(d))}**.",
    ])


def null_frag(d):
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "**", "ID_*.json"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "WDInventoryFragment_Attachment" not in text:
            continue
        objs = [json.loads(p) for p in wa.EXPORT.split(text) if p.strip()]
        if any(o.get("Type") == "WDInventoryFragment_Attachment" and not o.get("Properties") for o in objs) or \
                any(o.get("Type") == "WDInventoryFragment_Attachment" and not (o.get("Properties") or {}).get("AttachmentData") for o in objs):
            name = next((o["Name"] for o in objs if o.get("Type") == "BHInventoryItemDefinition"), None)
            if name:
                out.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), name))
    return out


def used_effects(d):
    s = set()
    for it in d.attachments:
        s.update(it.applied + it.character + it.bipod_weapon + it.bipod_character + it.mounted_weapon + it.mounted_character)
        for v in it.sights.values():
            s.update(v)
    return s


def archetypes(d):
    cnt = collections.Counter(it.att_type for it in d.attachments)
    out = ["| Archetype asset | Slot tag | Attach bone | Category | Attachment items of this type |", "|---|---|---|---|---:|"]
    for path, name, tag, bone, cat in d.archetypes:
        out.append(f"| {source_link(path, name)} | `{tag}` | `{bone}` | {cat or '(not serialized)'} | {cnt.get(tag, 0)} |")
    extra = sorted(t for t in cnt if t not in {a[2] for a in d.archetypes})
    if extra:
        out.append("")
        out.append("Attachment types with no archetype asset: " + ", ".join(f"`{t}` ({cnt[t]})" for t in extra) + ".")
    return "\n".join(out)


def caliber(w):
    for c in w.containers:
        if c["ContainerIdentifier"]["TagName"].endswith(".Chamber"):
            ctx = [x.replace("Item.Caliber.", "") for x in c.get("Filter", {}).get("AllowedSubSlotContext", []) if x.startswith("Item.Caliber")]
            return ", ".join(ctx) or "-"
    return "-"


def platforms(d):
    out = ["| Weapon | Asset | Item id | Archetype | Weight | Grid | Caliber (chamber allow ctx) | Sub-slots (data order) | Clearable in Gunsmith |",
           "|---|---|---|---|---:|---|---|---|---|"]
    for w in d.weapons:
        x = d.extra[w.key]
        out.append(f"| {esc(wname(w))} | {link(w)} | `{w.item_id}` | {w.archetype} | {n(x.weight)} | {x.grid or '-'} | {caliber(w)} | "
                   f"{', '.join(weapon_slots(d, w)) or '-'} | {', '.join(c.replace('Item.Attachment.', '') for c in x.clearable) or '-'} |")
    return "\n".join(out)


def slots(d):
    out = []
    for w in d.weapons:
        lo = wa.Loadout(d, w)
        out += [f"### {esc(wname(w))} ({w.asset})", ""]
        out += ["| Slot | Hidden | Filter | Rule | Default item | Accepts | Accepted items |", "|---|---|---|---|---|---:|---|"]
        rows = 0
        for s in lo.walk():
            c = s.container
            method, rule = filt(d, c)
            acc = sorted(a.asset.replace("ID_", "") for a in d.attachments if wa.accepts(c, a))
            hidden = "yes" if c.get("bIsHiddenContainer") else "no"
            depth = s.key.count("/")
            label = ("&nbsp;&nbsp;" * depth + "↳ " if depth else "") + f"`{s.key}`"
            default = f"`{s.item.asset}`" if s.item else ("-" if not s.flag else "(missing item)")
            lst = ", ".join(f"`{a}`" for a in acc) if acc else "-"
            out.append(f"| {label} | {hidden} | {method} | {rule} | {default} | {len(acc)} | {lst} |")
            rows += 1
        if not rows:
            out.append("| (no sub-slots) | | | | | | |")
        out.append("")
    return "\n".join(out).rstrip("\n")


def type_data(d, it):
    """Type-specific fields of the attachment data that are not effects."""
    ad = d.extra[it.key].ad
    p = []
    if "ReloadAnimationPlayRate" in ad and ad["ReloadAnimationPlayRate"] != 1:
        p.append(f"reload anim rate {n(ad['ReloadAnimationPlayRate'])}")
    for k in ("_aaabcedhgdocfgafjkign", "_aaabfbhbgfmafmfmaajnd"):
        if k in ad and ad[k] != 1:
            p.append(f"obfuscated field `{k}` = {n(ad[k])}")
    if "FireMuzzleFlashScaleMultiplier" in ad and ad["FireMuzzleFlashScaleMultiplier"] != 1:
        p.append(f"muzzle flash scale {n(ad['FireMuzzleFlashScaleMultiplier'])}")
    tag = (ad.get("FireAudioContextTag") or {}).get("TagName")
    if tag and tag != "None":
        p.append(f"fire context tag `{tag}`")
    if ad.get("bOverrideShotgunData"):
        p.append("overrides shotgun data (`bOverrideShotgunData`; values not tabulated)")
    if ad.get("AnimationSet"):
        p.append("animation set `" + ad["AnimationSet"]["ObjectName"].split("'")[1] + "`")
    if ad.get("bAllowsInspect") is False:
        p.append("inspect not allowed")
    ig = [x["TagName"] for x in ad.get("WeaponInspectIgnoreList", [])]
    if ig:
        p.append("inspect ignore list " + ", ".join(f"`{x}`" for x in ig))
    return "; ".join(p) or "-"


def items(d):
    out = []
    for grp, its in groups(d).items():
        out += [f"### {grp} ({len(its)})", "",
                "| Asset | Item id | Name | Weight | Grid | Removable | Discard on empty reload | Context tags | Brings sub-slots | Fits (slot: weapons) |",
                "|---|---|---|---:|---|---|---|---|---|---|"]
        for it in its:
            x = d.extra[it.key]
            tags = [t for t in it.context_tags if t.lower() not in HIDE_CTX and t != it.att_type]
            subs = ", ".join(f"{wa.short_slot(c['ContainerIdentifier']['TagName'])} ({filt(d, c)[0]})" for c in it.containers) or "-"
            yn = lambda v: "-" if v is None else ("yes" if v else "no")  # noqa: E731
            out.append(f"| {link(it)} | `{it.item_id}` | {esc(it.display) or '(blank)'} | {n(x.weight)} | {x.grid or '-'} | {yn(x.removable)} | "
                       f"{yn(x.discard)} | {', '.join(f'`{t}`' for t in tags) or '-'} | {subs} | {fits_text(d, it)} |")
        out.append("")
    return "\n".join(out).rstrip("\n")


def effects(d):
    out = []
    for grp, its in groups(d).items():
        rows = []
        for it in its:
            parts = []
            if it.applied:
                parts.append("**Weapon:** " + eff_text(d, it.applied))
            for name, effs in it.sights.items():
                parts.append(f"**Sight `{name}`:** " + eff_text(d, effs, "no effects"))
            if it.is_bipod:
                parts.append("**Bipod unfolded:** " + eff_text(d, it.bipod_weapon, "none"))
                parts.append("**Bipod mounted:** " + eff_text(d, it.mounted_weapon, "none"))
            char = [("Character", it.character), ("Bipod unfolded, character", it.bipod_character),
                    ("Bipod mounted, character", it.mounted_character)]
            cparts = [f"**{lab}:** " + eff_text(d, e) for lab, e in char if e]
            td = type_data(d, it)
            if not (parts or cparts) and td == "-":
                continue
            rows.append(f"| {link(it)} | {esc(it.display) or '(blank)'} | {'<br>'.join(parts) or '-'} | {'<br>'.join(cparts) or '-'} | {td} |")
        out += [f"### {grp} ({len(rows)} of {len(its)} have effects or type data)", "",
                "| Asset | Name | Weapon-side modifiers | Character-side modifiers | Other data |", "|---|---|---|---|---|"]
        out += rows
        out.append("")
    return "\n".join(out).rstrip("\n")


def bipods(d):
    out = ["| Bipod | Stance | Pitch lock | Yaw lock | Max yaw change | Max pitch change | Mount height | Try mount on unfold | On failure try |",
           "|---|---|---:|---:|---:|---:|---:|---|---|"]
    for it in d.attachments:
        if not it.is_bipod:
            continue
        for s in d.extra[it.key].ad.get("StanceData", []):
            v = s["Value"]
            out.append(f"| `{it.asset}` | {s['Key'].split('::')[-1]} | {n(v.get('PitchLockAngle')) if v.get('bLockPitch') else 'off'} | "
                       f"{n(v.get('YawLockAngle')) if v.get('bLockYaw') else 'off'} | {n(v.get('MaxYawChange'))} | {n(v.get('MaxPitchChange'))} | "
                       f"{n(v.get('BipodMountLocationHeight'))} | {'yes' if v.get('bTryMountOnUnfold') else 'no'} | "
                       f"{v.get('PlayerStanceToTryOnFail', '').split('::')[-1] if v.get('bTryAnotherStanceOnFail') else '-'} |")
    return "\n".join(out)


def noeffect(d):
    side = lambda it: it.applied or any(it.sights.values()) or it.bipod_weapon or it.mounted_weapon  # noqa: E731
    out = ["| Attachment type | No effect in data | Of | Assets |", "|---|---:|---:|---|"]
    for grp, its in groups(d).items():
        ne = [it for it in its if not (side(it) or it.character or it.bipod_character or it.mounted_character)]
        out.append(f"| {grp} | {len(ne)} | {len(its)} | " + (", ".join(f"`{it.asset}`" for it in ne) or "-") + " |")
    out.append("")
    nf = [it for it in d.attachments if it.key not in d.fits]
    out.append("Attachments no weapon sub-slot accepts (three nesting levels): " + (", ".join(
        f"`{it.asset}` ({type_label(it)})" for it in nf) or "none") + ".")
    out.append("")
    oe = [it for it in nf if it.applied or any(it.sights.values()) or it.character]
    out.append("Of those, attachments that carry an effect (their effect never applies on any weapon in the data): " + (", ".join(
        f"`{it.asset}`" for it in oe) or "none") + ".")
    out.append("")
    nd = [it for it in d.attachments if it.sights and wa.DEFAULT_SIGHT not in it.sights]
    out.append("Sight items without a `S_Aim01` entry (the entry weapons start on): " + (", ".join(
        f"`{it.asset}` ({', '.join(it.sights)})" for it in nd) or "none") + ".")
    return "\n".join(out)


def ref_index(d, ids):
    """item id (lower) -> set of file stems under data/ that mention it."""
    pats = {i.lower(): set() for i in ids}
    for path in glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
        except OSError:
            continue
        stem = os.path.basename(path)[:-5]
        for i in pats:
            if i in text:
                pats[i].add(stem)
    return pats


def ref_kind(stem):
    if stem.startswith("DT_EntityData_UI"):
        return "UI catalog"
    if stem.startswith(("DT_WeaponMarket", "DT_VendorData")):
        return "vendor"
    if stem.startswith("DT_LootableDataTable"):
        return "loot"
    if stem.startswith(("DT_MetaTree", "DA_Weapon_UnlocksTree")):
        return "unlock tree"
    if stem.startswith(("DT_Challenge", "ST_Challenges", "DT_Reward")):
        return "challenges/rewards"
    if stem.startswith(("AE_",)):
        return "audio"
    return "item or weapon file"


def nofit_rows(d):
    """For each attachment no weapon sub-slot accepts: (item, reason text, reference kinds)."""
    nf = [it for it in d.attachments if it.key not in d.fits]
    refs = ref_index(d, [it.item_id for it in nf])
    wkeys = {w.key for w in d.weapons}
    others = [i for i in {id(i): i for i in d.items.values()}.values() if i.key not in wkeys]
    rows = []
    for it in nf:
        typ = type_label(it).split(".")[0]
        tool = set()
        for o in others:
            for c in getattr(o, "containers", None) or []:
                tag = c["ContainerIdentifier"]["TagName"]
                if tag == "None" or tag.startswith("Item.Container") or tag.startswith("Inventory.Slot"):
                    continue
                if wa.accepts(c, it):
                    tool.add(f"`{o.asset}` {wa.short_slot(tag)}")
        spec = [t for t in it.context_tags if t.startswith(f"Item.Attachment.{typ}.")]
        stem = spec[0].split(".")[-1] if spec else re.sub(r"^ID_|_(Mag|BRL|HGD|GRP|STK)\w*$", "", it.asset)
        owners = [w for w in d.weapons if stem.lower() in f"{w.asset} {w.display or ''} {w.item_id}".lower().replace(" ", "")]
        if tool:
            reason = "fits a tool or deployable slot, not a weapon: " + ", ".join(sorted(tool))
        elif owners:
            parts = []
            for w in owners:
                sl = [c for c in w.containers if wa.short_slot(c["ContainerIdentifier"]["TagName"]) == typ]
                if not sl:
                    parts.append(f"`{w.asset}` has no {typ} slot")
                else:
                    f = sl[0].get("Filter", {})
                    names = [tname(d, x).replace("ID_", "") for x in f.get("AllowedSubSlotItems", [])]
                    ctx = f.get("AllowedSubSlotContext", [])
                    allow = ", ".join([f"`{x}`" for x in names] + [f"ctx `{x}`" for x in ctx][:3]) or "no allow list (blocks decide)"
                    parts.append(f"`{w.asset}` {typ} slot is {f.get('SupportFilter', '').split('::')[-1]} and allows " + allow)
            reason = "; ".join(parts)
        else:
            reason = f"no weapon is named for it; the {typ} slots that exist accept other items"
        kinds = sorted({ref_kind(s) for s in refs[it.item_id.lower()] if s != os.path.basename(it.path)[:-5]})
        rows.append((it, reason, ", ".join(kinds) or "none"))
    return rows


def nofit(d):
    out = ["| Asset | Type | Why no weapon accepts it | Referenced elsewhere in data/ |", "|---|---|---|---|"]
    for it, reason, kinds in sorted(nofit_rows(d), key=lambda r: (type_label(r[0]).lower(), r[0].asset.lower())):
        out.append(f"| {link(it)} | {type_label(it)} | {reason} | {kinds} |")
    return "\n".join(out)


def nullfrag(d):
    rows = null_frag(d)
    out = ["| Asset | Item id | Name | Context tags |", "|---|---|---|---|"]
    for rel, name in rows:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            objs = [json.loads(p) for p in wa.EXPORT.split(f.read()) if p.strip()]
        p = next(o for o in objs if o.get("Type") == "BHInventoryItemDefinition")["Properties"]
        dn = (p.get("DisplayName") or {}).get("LocalizedString") or ""
        out.append(f"| {source_link(rel, name)} | `{p['ItemId']['TagName']}` | {esc(dn) or '(blank)'} | "
                   + ", ".join(f"`{t}`" for t in p.get("ItemContext", []) if t.lower() not in HIDE_CTX) + " |")
    return "\n".join(out)


def attributes(d):
    """Per attribute: how many attachments modify it, by side and operation."""
    rows = collections.defaultdict(lambda: {"weapon": set(), "char": set(), "ops": collections.Counter(), "vals": []})

    def add(it, effs, side):
        for e in effs:
            for m in d.effects.get(e, {}).get("modifiers", []):
                r = rows[m["attribute"]]
                r[side].add(it.asset)
                r["ops"][OPS.get(m["op"], m["op"])] += 1
                if m["kind"] == "Scalar" and "value" in m:
                    r["vals"].append((m["op"], m["value"]))
    for it in d.attachments:
        add(it, it.applied + it.bipod_weapon + it.mounted_weapon + [e for v in it.sights.values() for e in v], "weapon")
        add(it, it.character + it.bipod_character + it.mounted_character, "char")
    out = ["| Attribute | Attachments (weapon side) | Attachments (character side) | Modifiers by operation | Scalar value range per operation |",
           "|---|---:|---:|---|---|"]
    for a in sorted(rows, key=lambda a: (not a.startswith("Attribute.Gameplay.Weapon"), a)):
        r = rows[a]
        rng = []
        for op in OPS:
            v = [x for o, x in r["vals"] if o == op]
            if v:
                rng.append(f"{OPS[op]} {num(min(v))} to {num(max(v))}" if min(v) != max(v) else f"{OPS[op]} {num(v[0])}")
        out.append(f"| `{short(a)}` | {len(r['weapon'])} | {len(r['char'])} | " + ", ".join(f"{k} x{v}" for k, v in sorted(r["ops"].items())) +
                   " | " + ("; ".join(rng) or "-") + " |")
    return "\n".join(out)


MODES = {"counts": counts, "archetypes": archetypes, "platforms": platforms, "slots": slots, "items": items,
         "effects": effects, "bipods": bipods, "noeffect": noeffect, "nofit": nofit, "nullfrag": nullfrag, "attributes": attributes}


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = link_generated(MODES[m.group(1)](d)).split("\n")
        return nl.join([f"<!-- attachment_tables {m.group(1)} -->"] + body + ["<!-- /attachment_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    d = load()
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        if not os.path.exists(path):
            print(f"{PAGE}: not found")
            return 1
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(d, text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(link_generated(MODES[next((a for a in args if a in MODES), "counts")](d)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
