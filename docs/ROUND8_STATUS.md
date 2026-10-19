---
title: Round 8 status
nav_exclude: true
---

# Remaining-work register, 2026-10-18

This is the active checklist for [What is left](WHAT_IS_LEFT.md). Historical
handoff instructions are not new work. A checked item needs cited static or
data evidence and the corresponding documentation/generator update. Partial
answers stay unchecked; a blocked item records the missing input.

Baseline: checkout `38eb2443`. No live-game or service testing is used.

## Already completed before this continuation

- [x] Round-7 documentation corrections (handoff §2.1).
- [x] Round-7 tail verification (handoff §2.2).
- [x] Loadout calculator shipped (`ed5b3d39`). Rechecked locally: 1,752
  comparisons passed, zero mismatches, using the installed Node runner.
- [x] Vehicle and infantry collision viewers shipped. Infantry generator
  rechecked locally: 911 comparisons passed, zero mismatches.
- [x] Radial amount/falloff arithmetic traced and documented in
  [Damage §1.1](../pipelines/Wardogs_DamagePipeline_v2.md#11-callers-and-where-the-result-goes).
  Its propagation to the infantry viewer is tracked below.

## Original infantry-viewer queue

| Done | Item | Current boundary |
|---|---|---|
| [x] | `radial-amount` | Arithmetic propagated; Center/Disc/Points all use original-origin distance and Inner/Outer assignment. Native default is Points. [Evidence](evidence/round8-radial-points-components.md). |
| [x] | `radial-split` | Normal player setup has one eligible TP mesh; capsule/FP excluded. Mutable associates with that existing component; retained hits are per component, not per body. Arbitrary later mutations and per-blast acceptance remain conditional. [Topology](evidence/round8-radial-mutable-topology.md), [gather](evidence/round8-radial-points-components.md). |
| [x] | `radial-context` | Projectile blasts preserve weapon/caliber context and add Explosive/radius; generator corrected. Bone factors retain explicit valid-equipment/mapped-bone assumptions. [Evidence](evidence/round8-radial.md). |
| [x] | `exploding-hit` | Expression/default and concrete camera-projectile mutation traced, including candidate/acquisition/loss-grace arithmetic; independently reviewed. Exhaustive arbitrary writer coverage remains outside this scoped closure. [Evidence](evidence/round8-exploding-gate.md). |
| [x] | `explosive-actors` | Six actors' inherited defaults, source/context and detonation paths traced from fresh local exports plus exe; reviewed scalar fixture added. Molotov fire separate. Trigger timing/patch geometry remain scoped out. [Evidence](evidence/round8-explosive-actors.md). |
| [x] | `armor-hook-paths` | Projectile/general hooks and named source paths traced; melee's returned copy is ignored. [Armor](evidence/round8-armor.md), [melee](evidence/round8-melee.md). |
| [x] | `armor-data-rows` | Separate armor-target event, not additional health-event rows. Final queue consumption/durability writes remain outside this closure. [Evidence](evidence/round8-armor.md). |
| [x] | `vehicle-weapon-tag` | Extension data → damage component → owner interface → projectile record → source context traced. [Evidence](evidence/round8-weapon-context.md). |
| [ ] | `underbarrel-weapon-tag` | No firing consumer/owner found for the data-only test attachment. Generic lifecycle only handles audio/animation; full cooked script-import audit supplies no Blueprint consumer. A concrete ancillary factory or fire-action binding is required before assigning a shot tag. [Evidence](evidence/round8-ancillary-sights.md). |
| [x] | `melee-path` | Three cooked character paths traced: amount, source/context, no bone, ignored armor-event return and health application. [Evidence](evidence/round8-melee.md). |
| [x] | `impact-amount` | Four thrown actors inherit contact amount 10; actor-impact overlap/transform formula, substep-seconds input and settings multiplier traced. Rules bypassed; per-hit geometry/state supply actual numbers. [Evidence](evidence/round8-impact.md). |
| [x] | `backblast` | Normal handheld source, foot/seated formulas, overrides and seated no-bone hit traced. Reflected/secondary foot gather remains scoped out. [Evidence](evidence/round8-backblast.md). |
| [x] | `occupant-damage` | Slot 160 starts at 1000; slot 161 forwards caller amount; source tags mapped, synthetic hits have no bone/location. Generator updated. [Evidence](evidence/round8-occupants.md). |
| [x] | `helmet-merge` | Compiled helmet/faction/view selectors, native asset deduplication and one-body-per-bone merge traced. Normal CharacterMesh has a null override and resolves the assigned mesh's asset. Actual runtime parameters and later mutations remain conditional. [Evidence](evidence/round8-helmet.md). |
| [x] | `tapered-capsule-query` | Native builder makes mean-radius straight capsules and registers query-capable shapes; independently reviewed. Viewer retains authored taper with explicit approximation note. [Evidence](evidence/round8-tapered-query.md). |
| [x] | `collision-channels` | Packed CharacterMesh profile/edit responses and cooked Custom/QueryOnly inheritance resolved. Shape registration/runtime mutation remain separate. [Evidence](evidence/round8-config.md). |
| [x] | `physical-material` | Geometry/capacity → exit velocity → later-hit speed damage and history marking traced, including packed head/body settings. No extra direct SurfaceType health scalar in this bounded bullet path. [Evidence](evidence/round8-physical-material-downstream.md). |
| [x] | `caliber-parent-match` | Normal reload filters and actual loaded-item projectile getters traced. Slug, artillery and STN03 pairings retained; four prefix-only bow/CGM4/Havoc pairings removed. Universal SupportedCaliber admission is not the normal firing contract. [Evidence](evidence/round8-weapon-context.md). |

## Carryover from Round 6

- [ ] Normal spawn default-grant path, distinct from the purchase continuation at `0x6BD5860`. The player registration override calls the base hook, which reads `ContainerSetup.DefaultContainerItems` and calls `AddItemToContainer`. Native construction creates thirteen setups with empty default-item arrays; the actual player Blueprint has no serialized setup override. Later provisioning and first-spawn ordering remain open. A separate SniperShowdown BeginPlay component attempts to grant a small backpack and Glock. [Initialization](evidence/round8-loadout-initialization.md), [purchase continuation](evidence/round8-loadout.md).
- [ ] Saved-preset hypothesis: establish a concrete feature/store before
  assigning replacement-versus-defaults behavior. No observed preset UI
  has been supplied; the original handoff question is not evidence that
  such a feature exists.
  The [rejoin restore path](evidence/round8-loadout-restore.md) is now traced:
  snapshot and economy-loadout metadata are copied into a duplicate session.
  A client initialization/wait callback requests the named restore RPC, which
  rebuilds the player component's inventory map and restores metadata. Its
  source is current component state, not an
  identified custom preset. The [script-import audit](evidence/round8-loadout-imports.md)
  finds no explicit native loadout-RPC import across the mounted packages.
  The [frontend and persistence audit](evidence/round8-loadout-frontend.md)
  finds inventory UI bindings and native creation of five fieldless list
  entries, with no preset payload assignment in that loop. Available client
  SDK declarations identify no equipment-preset schema; generic Pragma
  payloads leave backend definitions unresolved. The hypothesis remains
  uncorroborated, pending a concrete UI action, store or consumer.
  The [Deathmatch callback](evidence/round8-loadout-deathmatch.md)
  now has a verified click-to-RPC tag handoff and a `DeathmatchWeaponsData`
  registry binding to `DT_DeathmatchWeaponSelect`. Component registration
  requests the scene directly outside PreMatch, or registers its opening for
  Playing.Deathmatch while PreMatch is active. Automatic item granting at
  spawn remains unproved.
  The [Rebuy Last Loadout button](evidence/round8-loadout-rebuy.md) passes
  current economy `FWDLoadout` to `Server_ApplyLoadout`, whose per-slot
  requests target controller buffer storage rather than pawn equipment. A separate
  `Server_ProcessRebuy` RPC plans purchases from current history/loadout;
  its history reset is not an inventory clear. That separate RPC's caller,
  a named-preset store remain unproved.
  [Buffer layout commit](evidence/round8-loadout-buffer-layout.md) now has
  a verified conditional buffer-to-pawn inventory state copy: no positive
  CartPending amounts and equal aggregate stack-tag quantities are required.
  This does not establish arbitrary saved-preset replacement or spawn ordering.
  A conditional native callback builds slots from buffer records and moves
  them into economy `+0x218` under result-code/authority gates. Its trigger
  is traced through `Server_PurchaseLoadout`'s discriminator-0 task and its
  separate callback. The discriminator-3 callback is not that RPC's route.
  After this capture block, it copies buffer state into pawn inventory and
  removes pending-cart metadata from both. This purchase-result copy has no
  aggregate-quantity equality gate; that gate belongs to the separate layout
  commit RPC. Result code 1 and cash availability gate this path; the code's
  named meaning and normal-spawn ordering remain unknown.
  Purchase submission removes selected controller-buffer entries; vendor
  insertion uses the request's destination component and checks for a
  placed-count shortfall. The later result callback establishes pawn state replacement.
  `Client_LoadoutQueued` broadcasts to native delegates; an identified
  vendor-panel subscriber reconciles queued requests with CartPending
  sources, without establishing an automatic purchase trigger.
  `Server_PurchaseLoadout` validates that
  its incoming Requests array is empty; the equipment destination is selected
  by the later buffer-to-pawn copy, not that parameter.
- [x] `ClassToHitLocations`: packed keys BHMoverPawn and WDTargetDummy select the player asset; inheritance branches do not compete. [Evidence](evidence/round8-config.md#classtohitlocations-entries-and-precedence).
- [x] Vehicle sweep hits: native query flags, conversion and reversed Item/MyItem traced. Ordinary mesh sweeps lack triangle-material indices; single-body cases do not select a section. Custom queries remain distinct. [Evidence](evidence/round8-vehicle-sweep.md).
- [x] Rotor-hub group membership: native registration, health selector and callback fan-out show hubs and blades toggle together in their Main/Tail groups, restoring each member's own profile. [Evidence](evidence/round8-rotor-toggle.md).
- [x] STN_06 `bEnablePartialAttachments`: native attach-manager constructor initializes false; stationary constructor chain/cooked platform do not override it. Later runtime mutations remain outside this static default. [Evidence](evidence/round8-stn06-attachments.md).
- [x] Blueprint `IWDWeaponOwner` audit: 107,181 packages loaded without failures; no direct implementation or Blueprint descendants of the three identified native owners across 3,866 generated classes. A typed positive control preserves a different K2 interface. This is a build-specific static audit. [Evidence](evidence/round8-weaponowner-imports.md).
- [x] Sight-multiplier data path (Weapons §5b): selected sight record, exact archetype lookup, fallback and stabilization gates traced. [Evidence](evidence/round8-ancillary-sights.md).

## Extraction and maintenance

- [ ] Remaining 2,698 hashed names: check available evidence before declaring
  the need for a new unobfuscated usmap or hash key. Current-source build
  reproduces base v2 and existing export fills: export remainder 2,690 hashed
  occurrences, not 2,698. [Audit](evidence/round8-mapping-gaps.md).
- [ ] Remaining 451 unknown element types: retain ambiguity rather than
  inventing SDK types. Existing export fills cover 236, leaving 215 unknown
  arrays in the established export map. Independent package-metadata passes
  now fill **162** (83 Blueprint and 79 RigVM), leaving **53** unknowns across
  36 generated property-bag owners. The verified final map preserves the
  2,690 hashed-name count; see the [mapping audit](evidence/round8-mapping-gaps.md)
  and [property-bag proof](evidence/round8-propertybag-types.md).
- [x] Generated-document line endings: `.gitattributes` pins the two named
  documents to LF. Both generators match existing normalized content and
  are idempotent on task-created copies; existing documents were not rewritten.
- [x] Reconciled stale handoff instructions and generated viewer limitations.

## Validation

**Current checkpoint:** 17/18 original research entries closed and six
Round-6 carryovers closed. Latest artifact check **962/0**; radial decoder
**42 rings / 132 armor factors**; loadout parity **1,752/0**; links **0 broken**; JS syntax and diff
whitespace checks pass. Snapshot-rendered tables are unchanged on a second
render. Ordinary multi-process regeneration remains intermittently failing
under Python 3.13.7; the chronology below records both passing and failing
ordinary runs, without claiming a runtime fix.
The [native-failure follow-up](evidence/round8-generator-native-failure.md)
also records an isolated ordinary `0xC0000409` exit after ten passes,
against forty passing CDB runs and eleven passing ProcDump target runs.
No native fault was captured under either monitor; the cause remains open.
Child stderr is now preserved on regeneration failure, with a regression
proving both diagnostics and unchanged outputs after a later child fails.
Run `python -I _tools/infantry_regen_check.py`. One ordinary `--write` after
the diagnostic fix passed with nine tables unchanged and byte-identical
page/JSON; this is not an intermittent-crash fix.
A controlled comparison with a separate clean interpreter has not been
performed. That runtime change requires user approval under the project
rules; the existing interpreter remains in use.

Baseline local checks: links 0 broken; infantry 911/0; loadout 1,752/0.
After the first integration: infantry 924/0, including blast-context
regression sentinels and dangling limitation-ID checks; links 0 broken.
After actor-fixture integration: infantry 961/0. Regular `--write` currently
has an intermittent Python 3.13.7 child-process access violation under
investigation; do not treat that passing standalone checker as a passing
regeneration/idempotence gate.
Before the final helmet/caliber integration: **969 passed, zero mismatches**. Loadout parity:
**1,752/0**; links **0 broken**; JavaScript syntax, whitespace diff check and
the scoped UI detector pass. At that stage all **65 direct-projectile records** retained
their original numeric damage, zone factors and rule/armor entries.
The page/JSON have been regenerated using one traced build snapshot with
the same Python interpreter; this establishes reviewable artifacts, not a
fix for the intermittent ordinary multi-process regeneration crash.
Two renders from that snapshot were byte-identical (nine tables unchanged
on the second pass, JSON hash unchanged).
After configuration integration, ordinary `--write` also completed twice
(second run: nine tables unchanged), with **969/0** checks and **0 broken
links**. Eight original viewer limitations remain. This successful rerun
does not identify or fix the earlier intermittent interpreter crash.
The next ordinary regeneration reproduced child exit `3221225477` in
`--explosives`. After tapered-shape integration, the artifacts were rendered
from one traced snapshot twice (second render unchanged); checks remain
**969/0**, links **0 broken**, with **seven** original viewer limitations.
Ordinary regeneration therefore remains an intermittent failing gate.
After physical-material integration, the snapshot render remains idempotent
and the original viewer queue has **six** open items. Independent review
found a radial UI decoding branch that skipped compact factors without
field provenance. It is fixed; the new offline Node regression check
passes **50 rings and 176 armor factors**, failing on the prior code.
Run it with `node _tools/infantry_viewer_check.js`.

After the final helmet/caliber integration, one original viewer limitation
remains: ancillary shot ownership. The normal helmet merge/default policy
is verified. Four unsupported weapon/projectile pairings were removed;
their standalone projectile data was retained. The reviewed loading pairs
replace prefix inference. Current checks are **962/0**, radial decoding
**42 rings / 132 armor factors**, loadout **1,752/0**, and links **0 broken**.
The reduced counts reflect the removed speculative pairings and the
corresponding bow sentinel, with positive/negative loading regressions added.
Independent comparison confirms exactly four removed projectile-source rows
and unchanged damage values, direct factors, falloff keys and radial rings
for all **61 retained rows**. Baseline pairings still use the original first-
SupportedCaliber modelling choice unless independently reviewed; that limit
is explicit in the page and generated metadata.
Two snapshot renders again leave nine generated tables unchanged on the
second pass; this does not resolve ordinary Python regeneration instability.

### Initialization follow-up, 2026-10-19

The player registration hook and native constructor were independently
reviewed against executable bytes. Construction supplies thirteen container
setups with empty default-item arrays; the fresh player Blueprint export
has no setup override. The generic authority-gated grant mechanism is
identified, but the normal first-spawn item source is still open. Economy
registration processes the current pawn immediately; its examined pawn
callback refreshes existing slots' QuickSlotTag metadata. A full cooked
grant-API import census finds only six AddItemToInventory dependencies
and no AddItemToContainer/Auth_AddItemSlot imports, with zero failures.
These bounded checks do not establish universal spawn provisioning. A fresh
SniperShowdown Blueprint export establishes a separate two-item BeginPlay
grant attempt. The expanded all-script Loadout/Preset import audit covers
107,181 packages and 1,230,571 resolved imports with zero failures; it does
not identify a custom saved-preset selector. A separate
[Deathmatch native handler](evidence/round8-loadout-deathmatch.md) attempts
to add the supplied item and four magazines selected from its default tag
data. Its click-to-RPC handoff and exact registry-to-table binding are now
verified, as is the conditional match-state-to-scene request. Automatic
item granting at spawn remains open. These are documentation-only
continuations; no generated data was changed in this follow-up.

### Independent mapping recovery, 2026-10-19

Independent package metadata now supplies **83 Blueprint** and **79 RigVM**
array-type fills (**162 total**) without the absent dump-usmap donor. The
final map has **53 unknown array types** across **36 generated property-bag
owners**; its **2,690 hashed-name** count is unchanged. Parsed-map comparison
confines changes to the 162 target types, and fresh exports of all 58 affected
packages are byte-identical before and after. Both fill orders produce the
same 3,046,707-byte map (SHA-256
`277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`). The
remaining fields appear PCG-related, but the current PCG candidate work has
not proved an exact descriptor-to-owner join. Details are in the
[mapping audit](evidence/round8-mapping-gaps.md) and
[property-bag proof](evidence/round8-propertybag-types.md).

## Next bounded leads

Continue the unchecked rows above; do not repeat the closed Round-7/loadout
work. In particular:

- Underbarrel: locate live ancillary-component creation/owner; then follow
  the already-known owner interface and projectile-record tag writer.
- Loadout: the recovered defaults-helper path requires purchase-request
  data and checks Cart/Restock tags. Normal spawn granting remains unproved;
  do not label that purchase continuation a spawn hook. The saved-preset
  hypothesis needs a concrete feature/store before its ordering can be
  investigated. Repeating the audited frontend graphs or SDK name searches
  does not supply that missing premise.
  Both `Server_ApplyLoadout` branches now connect to that continuation.
  StorageVault uses a class-filtered `UWDStorageVaultComponent` lookup,
  consumes available quantities and converts shortfalls to Cash. Post-grant
  bookkeeping dispatches `Client_ConfirmPurchase`; it does not establish
  a custom saved-preset source. The generic initialization caller is now
  [identified](evidence/round8-loadout-initialization.md): player registration
  reaches configured container-default insertion. The actual player Blueprint
  has no serialized setup override; native construction supplies thirteen
  setups with empty default-item arrays. Follow later provisioning and
  first-spawn ordering next. Keep the separate SniperShowdown BeginPlay grants
  scoped to that mode. The Deathmatch loadout handler is another concrete
  grant path. Its button callback
  `0x8494AA0`, entry construction `0x8495360`, and component RPC-delegate
  binding `0x8490B30` are now verified. The native `DeathmatchWeaponsData`
  key resolves through `DR_DeathmatchWeaponsData` to the 20-row
  `DT_DeathmatchWeaponSelect`. The registration hook requests the scene
  directly outside PreMatch or registers the request for Playing.Deathmatch
  while PreMatch is active. An automatic selection event or first-spawn
  item grant remains unproved.
- Mapping: package metadata supplies 162 verified type fills; investigate
  the remaining 53 unknowns across 36 generated property-bag owners. Their
  names match PCG settings layouts, but an exact join remains unproven.
  The full-package probe of exact `PCGGraph`/`PCGGraphInstance` exports found
  no remaining-owner matches in 294 nonempty serialized bags, with zero
  read failures; repeating those same fields is not a new lead. Native
  settings-derived candidates reproduce eight already-typed bags but none
  of these 36 owners. A separate mapped-descendant scan of
  `PCGMetadataSettingsBase.DefaultValues.PropertyBag` finds 33 nonempty
  singleton bags and no mapped-owner matches, with zero read failures.
  A different descriptor source or independently proved
  owner binding is needed. Native field-registration order is another
  unverified boundary: seven of the eight existing native hash controls
  are singleton bags, and a multi-field target registration table has not
  been recovered. No ordering mismatch or reordered fill is claimed.
  The two earlier Blueprint case-only misses are resolved. The
  absent old `new.usmap` still prevents independently recreating that
  historical donor. Hashed-name recovery remains separate; these type fills
  leave 2,690 hashed occurrences unchanged.
- Regeneration: preserve full faulthandler stderr if the Python 3.13.7
  access violation recurs. Baseline/current bounded comparisons did not
  establish its cause; no interpreter upgrade, code workaround or root-cause
  claim has been applied to the repository.

New bounded continuations: camera-projectile gate mutation in
[the gate report](evidence/round8-exploding-gate.md); Point-mode distance,
selectors and ordinary default components in
[the point-mode report](evidence/round8-radial-points-components.md);
entity-request purchase continuation into defaults in
[the loadout report](evidence/round8-loadout.md). The independently reviewed
camera gate is closed for the concrete traced path; the other continuations
retain their remaining actor-state boundaries.

The continuation is prepared for publication with links at 0 broken,
infantry checks at 962/0, loadout parity at 1,752/0 and the radial decoder
at 42 rings / 132 armor factors. Damage, recoil and weapon table renders
are unchanged. Publication is recorded in Git history; this does not close
the unchecked research rows or resolve the intermittent regeneration crash.
Pre-existing untracked `_tools/content.md` and `graphify-out/` were left untouched.
Browser and live-site checks from the previous handoff have not been rerun
in this continuation. Those historical results are not current validation.
