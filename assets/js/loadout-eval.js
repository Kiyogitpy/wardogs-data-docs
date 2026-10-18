/* Weapon loadout evaluator: the browser twin of `python -I _tools/weapon_attributes.py --weapon ...`.
   Pure logic, no DOM, no dependencies. UMD: a browser global `window.WDLoadout`, or
   `require("./assets/js/loadout-eval.js")` in node. Data: assets/data/weapon-loadouts.json
   (python -I _tools/weapon_attributes.py --json). `python -I _tools/weapon_attributes.py --check`
   runs the same loadouts through this file and through the Python and requires 0 mismatches.

   Rules (Wardogs_WeaponAttributes_v1.md "Rules"; Effects §7.1, §4.2, §4.4): base = the weapon's
   DefaultAttributes as f32; one application per equipped attachment's AppliedEffects, the selected
   sight's effects, the bipod's unfolded or mounted lists, and the stance preset (with its stacks);
   stack scaling m' = (m - I) * n + I (not for Override); the first Override wins, otherwise
   ((Base + ΣAdd) * (1 + Σ(Mul - 1)) / D) * ΠMulCompound + ΣAddFinal. Sums are CPython 3.12+ sum()
   (Neumaier-compensated), magnitudes are Math.fround'ed like the Python's f32(). Character-side
   lists are listed, never evaluated.

   ----------------------------------------------------------------------------------- API
   Strings that come from the game data (display names, tags, ids, effect names, notes) are data:
   set them as text, never as HTML. Notes use `backticks` around ids, as the Python prints them.

   WDLoadout.model(json) -> model
       Prepares the parsed weapon-loadouts.json. The model is read-only; keep one per page.
       model.meta                  the JSON's meta (data tree id, generator, doc anchors, notes)
       model.weapons               [{id, display, archetype}] in the Python's order (archetype, name)
       model.items[id]             {id, itemId, display, attachmentType, archetype, isWeapon,
                                    isAttachment, hasSights, isBipod, sights: [name]}
                                   id = asset name, e.g. "ID_WEPN_037" (also every `itemId` below)
       model.stances               ["Stand", "Crouch", "Prone"]
       model.bipodStates           ["folded", "unfolded", "mounted"]
       model.defaultSight          "S_Aim01"

   A loadout is a plain object (JSON-safe, fine for a permalink):
       {weapon: id, items: {<slot key>: itemId|null}, sight: name|null,
        stance: "Stand"|"Crouch"|"Prone", bipod: "folded"|"unfolded"|"mounted"}
       - slot key: the sub-slot's label path from the weapon down, joined by "/", e.g. "Barrel",
         "Barrel/Muzzle", "Handguard/Underbarrel" (label = tag without "Item.Attachment.").
       - a key missing from `items` means the slot's default item; null means empty. Keys of slots
         that are not open are ignored. Choosing "none" never adds a slot's missing-default note
         back or drops it: only placing an item drops it (as in the Python).
       - sight null means the default: every sight-bearing attachment uses `S_Aim01`, or no sight
         effects if it has no `S_Aim01`. A name applies to every attachment that has that entry;
         the others fall back to `S_Aim01` with a note (the Python's --sight).

   WDLoadout.defaultLoadout(model, weaponId) -> loadout
       The weapon's default loadout with every open slot written out explicitly (DefaultContainerItems,
       or DefaultItems only when that is empty), sight null, Stand, folded.

   WDLoadout.slots(model, loadout) -> [slot]
       The open sub-slots in walk order (each slot followed by the sub-slots its item brings):
       {key, tag, label, parent: key|null, depth (0 = on the weapon), owner: itemId (weapon or the
        attachment that brings the slot), accepts: [itemId] (attachments the filter admits, in data
        order), default: itemId|null, choice: itemId|null (what the loadout puts there),
        isDefault: bool, flag: string|null (missing default item note)}
       Slots that accept no attachment (chamber, magazine ammo) are included with accepts [].

   WDLoadout.setItem(model, loadout, key, itemId|null) -> new loadout
       Puts the item into the slot (it must be in that slot's `accepts`, or null), drops the keys of
       the slot's old sub-slots and writes out the defaults of the sub-slots the new item brings.

   WDLoadout.normalize(model, loadout) -> {loadout, dropped: [string]}
       For a loadout from a permalink: drops an unknown weapon (falls back to the first weapon),
       keys of slots that are not open, items the slot does not accept, an unknown stance or bipod
       state, and a sight no equipped item has; `dropped` says what went.

   WDLoadout.sights(model, loadout) -> [{name, items: [itemId], isDefault}]
       The SightsData entries of the equipped attachments, in walk order then data order, deduped by
       name. isDefault marks `S_Aim01`. Empty when nothing equipped has sights.

   WDLoadout.hasBipod(model, loadout) -> bool
       True when an equipped item carries the bipod lists (enable the bipod control only then).
       Evaluating a loadout with bipod unfolded/mounted and no bipod gives a note, no error.

   WDLoadout.evaluate(model, loadout) -> result
       {weapon: [{tag, label, base: number|null,
                  steps: [{source, effect, op, symbol, kind, stacks, magnitude: number|null,
                           backing: tag|null, flag: string|null}],
                  final: number|null, notes: [string]}],
        character: [{effect, source, modifiers: [modifier]|null}],
        applications: [{effect, stacks, source}],       weapon-side, in Override order
        attachments: [{key, tag, item}],                 equipped items in walk order
        hasBipod: bool,
        notes: [string]}                                  loadout flags, application notes, eval flags
       `weapon` lists every attribute the weapon has a base for (data order), then any other
       attribute a weapon-side modifier reaches. magnitude = the stack-scaled value the formula used,
       null when it was not evaluated (flag says why). `op` is the EBHAttributeModOp name, `symbol`
       its sign (+ × ÷ ×c +f =). `source` is the attachment id, "<id> sight <name>",
       "<id> bipod unfolded|mounted" or "stance <Stance>". Throws on an unknown weapon or an item a
       slot does not accept (normalize() first for untrusted input).

   WDLoadout.cli(model, loadout) -> {args, exact, reason}
       The weapon_attributes.py arguments for the loadout, e.g.
       "--weapon ID_WEPN_037 --with ID_FGRP_006 ID_SGHT_009 --sight S_Aim02 --stance Prone --mounted".
       exact = true when those arguments give exactly this loadout (checked by replaying the
       --with placement); otherwise false with a plain-text reason (e.g. the CLI cannot empty a slot
       that has a default item, or its first-free-slot rule would put an item elsewhere).

   WDLoadout.withItems(model, weaponId, ids, opts?) -> loadout
       The CLI's --with placement: each item goes into the first free sub-slot (walk order, sub-slots
       opened by earlier items included) that accepts it, replacing the default there. opts may give
       sight, stance, bipod. Throws when no free sub-slot accepts an item (the CLI's error).

   WDLoadout.effect(model, name) -> [modifier]|null
       An effect's modifiers: {attribute, op, symbol, kind, value?, backing?, mode?, channel?,
       curve?, indexing?, fallback?}.
   WDLoadout.attrLabel(tag) -> tag without "Attribute.Gameplay.Weapon." (or "Attribute.Gameplay.")
   WDLoadout.slotLabel(tag) -> tag without "Item.Attachment."
   WDLoadout.OPS             {Add: "+", Multiply: "×", Divide: "÷", MultiplyCompound: "×c",
                              AddFinal: "+f", Override: "="}
   WDLoadout.fmt(x, digits=6) -> Python f"{x:.{digits}g}" ("—" for null): the tables' rounding.
   ------------------------------------------------------------------------------------------ */
(function (root, factory) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.WDLoadout = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  // API header only; the implementation follows in the next commit.
  var api = {};
  ["model", "defaultLoadout", "slots", "setItem", "normalize", "sights", "hasBipod", "evaluate", "cli",
   "withItems", "effect", "attrLabel", "slotLabel", "fmt"].forEach(function (n) {
    api[n] = function () { throw new Error("WDLoadout." + n + ": not implemented yet"); };
  });
  return api;
});
