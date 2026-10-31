---
title: Round 8 weapon context provenance
nav_exclude: true
---

# Round 8: vehicle, ancillary and caliber provenance

Static research, 2026-10-18; CL-516586 read-only corpus and restored
executable. Important native statements below were checked against
instructions. No game, service or runtime session was used. New bounded
Blueprint exports/listings remain outside the checkout at
`E:/Reverse_Engineer/wardogs_analysis/round8_weapon_context_20261018`.

## Vehicle projectile weapon tag: resolved

The projectile source-context weapon tag comes from the owning weapon's
**damage entity component root tag**, initialized from
`UWDVehicleWeaponExtensionDataAsset.DamageEntityData.Tag`.
It is not selected from the stats `WeaponId`, `WeaponExtensionTag`,
`WeaponItemId` or item-slot tag.

| Stage | Exact native anchor |
|---|---|
| Vehicle extension implements `IWDWeaponOwner` | Constructor `0x7642580`, instructions `0x76425A5`/`0x76425B1`, writes table `0xB63E858` at actor `+0x2B8` |
| Interface `GetDamageEntityComponent`, slot `+0x70` | Table entry points to `0x18F0650`; `mov rax,[rcx+0xB8]; ret` returns actor `+0x370`, matching SDK `DamageEntityComponent` |
| Copy configured entity data | `0x76478D0` (`OnOwningWeaponInitialized`), `0x7647B30`–`0x7647B42`: component actor `+0x370`, source `WeaponExtensionDataAsset` actor `+0x358`, source struct `+0x48`, call `0x6B18E30` |
| Component field copy | `0x6B18E40` writes root at `+0xE0`; `0x6B18E55` copies context at `+0xE8`; `0x6B18E63` writes cause tag at `+0x108` |
| Initialize corresponding weapon stats | `0x7647B5D`–`0x7647B72`, actor weapon component `+0x368`, extension data `WeaponStatsData +0x80`, virtual init slot `+0x558` |
| Build projectile slot record | `0x6B74440` initializes a record and calls `0x6B72030`; `0x6B75270` refreshes an existing record through the same writer |
| Actual record tag writer | `0x6B720C4`/`0x6B720CB` dispatch `IWDWeaponOwner +0x70` with weapon component; `0x6B720DF` calls getter `0x1C36300` (component `+0xE0`); `0x6B720E7` writes its tag to record `+0x10` |
| Use record in damage source | `0x6B725B0` resolves it with `0x6B74E30`; `0x6B7283F`–`0x6B72848` loads record `+0x10` and adds it to the source context |

The initialization follows validity checks and the owning weapon's
authority branch (`0x76478D0`); records also retain actor/cause identity.
`0x6B74E30` first tries the weapon byte id and then its composite id with
the proxy identifier. `0x763A890` transfers/refreshes records when a
vehicle operator changes, using `0x6B75270` and `0x6B74440`.
Thus switching proxy ownership does not require inventing a different tag.

For example, the exported
`/ROT_02/Weapons/122mm/WE_ROT_02_Weapon_122mm` configures
`Meta.Damage.Weapon.Vehicle.HelicopterRocket`, while its extension identity
is `Id.Vehicle.WeaponExtension.ROT_02.122mm`. The former is the projectile
context tag through this path. Each vehicle weapon still needs its own
configured `DamageEntityData.Tag`; a vehicle or caliber-wide replacement
would erase that distinction.

## Underbarrel launcher: actual writer still untraced

`/UnderbarrelGrenadeLauncher/Data/GrenadeLauncher` is the attachment item
`Id.Item.TestGrenadeLauncher`. Its attachment data is the ancillary weapon
shape (`FWDAncillaryAttachedWeaponData`, SDK struct `WeaponStats +0x50`):
stats reference [`DA_GrenadeLauncher_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Stats.json), caliber `Item.Caliber.40mm`,
required item `Id.Item.40mm`, one resource per use, ancillary-ammo resource
type and search limited to the item. This data structure has no damage
entity field or explicit source weapon tag.

The ordinary ranged extension's `IWDWeaponOwner` getter returns its shared
`DamageEntityComponent +0x130`; its initialization copies ranged extension
data `DamageEntityData +0x1E0` (`0x6C9B588`–`0x6C9B596`). The projectile
record writer above would therefore use that root **if the ancillary
weapon component actually has this extension as its owner**. That owner
provenance and the ancillary component's creation/registration were not
found here. The stats reference alone does not establish them. Neither
the attachment item id nor the host weapon tag is verified as the actual
underbarrel projectile context. Keep `underbarrel-weapon-tag` open.

Fresh `B_Action_WeaponFire` and `B_Action_Reload` exports were inspected;
the normal fire action reads `WDItemExtensionData_RangedWeapon.WeaponStats`
(ubergraph offset 4919). These do not establish a live ancillary path for
the test attachment. Raw Blueprint dumps are not published.

## SupportedCaliber: helper direction verified, eligibility still open

SDK `FWDWeaponStats.SupportedCaliber` is a `FGameplayTagContainer` at
struct `+0xD20`. A small omitted corpus function is verified directly in
the executable: `0x6BBD650` returns `stats +0xD20`. Its indexed callers
include assistance requests (`0x6AF5720`, `0x6AF8A00`, `0x6AF93E0`),
weapon trajectory preparation (`0x6B96820`) and a UI query (`0x736A170`).

Another executable helper, `0x6BBD780`–`0x6BBD7DA`, tests a nonempty query
tag against the supported container. It compares exact tag identities
first with the explicit array (`+0xD20`, count `+0xD28`) and then with its
cached parent array (`+0xD30`, count `+0xD38`). Therefore this helper's
direction is: a supported **child** tag also answers true to a query for
its **parent**. It does not manufacture children of a configured parent.
The indexed call edges omitted two actual call sites, now traced below.
The helper's direction alone is not proof of the actual ammo admission rule.

The ordinary ranged owner's projectile getter `0x6C98290` instead resolves
the loaded item and its projectile fragment. `0x6C9845A` loads the fragment
projectile pointer at `+0x38`, returned by this function; it constructs the
ammo-modifier context separately. No `SupportedCaliber` gate occurs in
this getter. This proves provenance once an ammo item is loaded, not
which child-caliber items inventory/reload rules permit loading.

### Newly located SupportedCaliber caller: vehicle-seat compatibility state

Both raw `call 0x6BBD780` instructions, at `0x7436D77` and `0x7436DB8`,
are inside one exception-directory function range `0x7436B60–0x7436DD8`.
This range was absent from the decompilation function table; the executable
instructions, unwind entry and SDK offsets establish the following path.
It is called from `0x7436DE0` at `0x7436F20`; the latter is reached by a
list/update worker `0x7403830`, which invokes it for each candidate and
writes a state byte through `0x53EE970` (`0x7436F25–0x7436F33`). That is
a compatibility-state calculation, not an observed inventory-add or reload
write. The caller enters this SupportedCaliber branch only when
`0x7690210` returns null (`0x7436EC2–0x7436F20`). Its other branch compares
the candidate tag with a weapon extension's configured `AmmoTag` at data
asset `+0x15C` (`0x76449C0`; SDK).

The candidate input is an `ABHBaseVehiclePawn`: `0x7436B8E` calls
`0x53CAE20`, which returns pawn `VehicleSeatComponent +0x758` (SDK
`Mechanized_classes.hpp`).
The query resolves an inventory item definition through that seat and a
ranged-weapon extension. The extension is validated against
`WDItemExtensionData_RangedWeapon` (`0x7436C3F–0x7436CAB`), and its
`WeaponStats +0x98` data asset is loaded at `0x7436CB1`. Call `0x17E78D0`
returns asset `+0x38`, exactly the embedded `FWDWeaponStats` that owns
`SupportedCaliber` (SDK,
extension layout).

If the item definition has a valid `BHInventoryFragment_SubSlotSupport`,
the function walks its `Containers +0x48` as 0x110-byte
`FBHContainerSetup` records (`0x7436D3D–0x7436D8E`). Only a record whose
`ContainerIdentifier` is `Item.Ammo` is considered: the compared tag global
at RVA `0xD36C2E0` is initialized from literal `"Item.Ammo"` by
`0x129DC90`. At `0x7436D60–0x7436D7E`, the function iterates the
**explicit** entries of that container's `Filter.AllowedSubSlotContext`
(record `+0x30`, count `+0x38`) and asks `0x6BBD780(stats, &tag)` for each.
Any true result yields true for this state query. The 0x110-byte record
and nested filter offsets match
`FBHContainerSetup` and
`FBHSupportFilter`.

Only when the subslot-support fragment is absent/invalid does the function
fall back at `0x7436DA3–0x7436DC3` to the item definition's **explicit**
`ItemContext +0x38` tags (SDK),
testing each through the same helper. A valid fragment whose `Item.Ammo`
container yields no match returns false; it does not enter the fallback.
Because `0x6BBD780` searches configured SupportedCaliber tags and their
cached parents, this caller asks whether the configured supported caliber
contains a candidate context tag or a child of it. It does not admit every
child ammo item from a parent caliber, and this state calculation has not
been traced to the authoritative inventory/reload gate. The generic slot
filter below remains the verified direction for the named item contexts.

### Actual inventory filter direction and concrete ammo links

A further trace resolves the relevant generic inventory match direction,
which is separate from `SupportedCaliber`.

`FBHSupportFilter` contains method `+0`, allowed item ids `+0x8`, allowed
item contexts `+0x28`, blocked ids `+0x48` and blocked contexts `+0x68`.
The SDK enum identifies `AllowList=0`. Native filter evaluator
`0x67A2B40`'s AllowList branch compares item ids exactly, ORs that result
with `0x395BE30(item.ItemContext, filter.AllowedSubSlotContext)`, and returns
it. Machine instructions `0x67A2D00`–`0x67A2D11` form the filter `+0x28`
pointer, make that call and OR the result. Slot-item support caller
`0x67A0E20` passes the actual definition's `ItemId +0x30` and
`ItemContext +0x38` (`0x67A0E60`–`0x67A0E76`). It also applies outer-inventory
and parent/storage rules; passing this filter alone is not the whole
inventory operation.

`0x395BE30` iterates the **filter's explicit** tags and searches each in
the **item context's explicit and cached parent** arrays. Instructions
`0x395BE70`–`0x395BE9E` corroborate both searches. Thus an ammo item's child
context matches a slot's parent context filter. This direction is
verified and differs from querying the SupportedCaliber container itself.

| Named case | Reviewed cooked data and implication |
|---|---|
| Combat bow / explosive arrow | [`ID_CombatBow_MagInternal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/ID_CombatBow_MagInternal.json) allows context `Item.Caliber.Arrow`; [`ID_Arrow_Explosive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/Arrow/ID_Arrow_Explosive.json) has context `Item.Caliber.Arrow.Explosive` and directly references [`DA_Arrow_Explosive_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/Arrow/DA_Arrow_Explosive_ProjectileData.json). Its child context passes this generic filter. The normal arrow has the parent context and its own direct projectile reference. |
| M500 / MP43 rifled slug | `WEPN_011/Data/ID_M500` and `MP43/Data/ID_MP43_Mag_Internal` allow context `Item.Caliber.12g`. [`/Game/Items/Resources/Ammo/12Guage/Slug/ID_12g_RifledSlug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/12Guage/Slug/ID_12g_RifledSlug.json) explicitly has that **parent** context and directly references [`DA_12g_RifledSlug_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/7mm_Buckshot/DA_12g_RifledSlug_ProjectileData.json). The child projectile id does not require child-caliber matching at the slot filter. |
| STN_03 main barrel | `/STN_03/Weapons/ID_STN_03_MainBarrel` allows `Item.Caliber.120x800mm`. [`/Game/Items/Resources/Ammo/120x800mm/ID_120x800mm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/120x800mm/ID_120x800mm.json) has that parent context and directly references [`DA_120x800mm_Standard_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/120x800mm/DA_120x800mm_Standard_ProjectileData.json). Again the item context and projectile id differ. |
| TNK_01 artillery | [`/Game/Items/Vehicles/Weapons/TNK_01/ID_VehicleTurretArtillery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_01/ID_VehicleTurretArtillery.json) allows context `Item.Caliber.155mm`; [`ID_155mm_Standard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/155mm/ID_155mm_Standard.json) and [`ID_155mm_Expensive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/155mm/ID_155mm_Expensive.json) have the corresponding child contexts and direct references to their named projectile assets. [`WE_TNK_01_Artillery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/Weapons/WeaponExtensions/Artillery/WE_TNK_01_Artillery.json) explicitly configures starting inventory `ID.Item.155mm.Expensive=10` and `ID.Item.155mm.Standard=0`. Both child contexts pass the generic parent filter. |
| CGM4 / TV-guided candidate | `WEPN_013/Data/ID_CGM4`'s chamber allows **exact item id** `Id.Item.84mm`, with an empty allowed-context list. [`/Game/Items/Resources/Ammo/84mm/ID_84mm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/84mm/ID_84mm.json) directly references basic [`DA_84mm_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/84mm/DA_84mm_ProjectileData.json). [`DA_TVGuidedMissile_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/DA_TVGuidedMissile_Data.json) has projectile id `Item.Caliber.84mm.TVGuided`, but this prefix alone establishes neither a compatible item nor an actual CGM4 selection path. |

The item-to-projectile references and filter behavior support these named
ordinary ammo associations more strongly than a projectile-id prefix
enumeration. A universal statement that SupportedCaliber authorizes every
child projectile is still unproved; keep that narrower claim open. In
particular, retain a limitation for CGM4's TV-guided candidate and for
ancillary ownership. Runtime loading, resource availability, chamber
state and special vehicle/bow implementations still have their own checks.

### Exact remaining leads

The vehicle owner's `GetProjectileData` interface slot `+0x90` points to
`0x7645A30` (table `0xB63E858`); its body was not yet reviewed. The normal
handheld getter `0x6C98290` is reviewed above. The ancillary attachment's
live component creation/owner and fire action remain unlocated. Neither
the normal fire action nor the attachment's stats is sufficient evidence
of that path. Further work should follow those concrete interfaces and
item/projectile references rather than treating every matching caliber
prefix as ammunition that the weapon can fire.

## Follow-up: normal reload and named projectile associations

This follow-up resolves the original generator's named `caliber-parent-match`
question through the actual inventory/reload and loaded-item paths. It also
finds a material limit missed by looking only at the bow's internal magazine:
**the actual CombatBow chamber accepts the normal arrow's exact item id**.
There is no need to prove admission of every hypothetical descendant of
every SupportedCaliber tag in order to answer these named cases.

### Normal reload selects with the destination container filter

Fresh `B_Action_Reload` bytecode shows the ordinary loose-ammo/chamber path:

| Ubergraph offset | Operation |
|---:|---|
| 17526 | Read the weapon's `Item.Attachment.Chamber` container setup. |
| 17610 / 17858 | Call `Inventory.GetSlotsSupportingFilter` with that setup's Filter. |
| 17919 / 17992 | Get the destination chamber slot and choose `GetBestAmmoFromArray` from the filtered candidates. |
| 18033–18277 | Construct a `BHMoveItemOperation` from the selected candidate's SlotPath to the chamber's SlotPath. |
| 18336–18482 | Check that inventory operations may be sent, then register the move with the inventory manager. |

The magazine-ammo branch likewise reads the magazine's `Item.Ammo` setup
or the weapon chamber setup, queries the selected Filter at offsets 14030
and 14750, chooses from those results at 14855, and makes a one-item move
at 14940–15264. The existing registered move operation retains ordinary
inventory validity/storage constraints; the Blueprint does not replace
the item with a projectile chosen by caliber prefix.

`GetBestAmmoFromArray` is fully bounded in this Blueprint. It prefers an
exact item-id match to the existing destination item, or the ranged
extension's LastEquippedAmmoType when the destination is empty. If no
preferred match exists it chooses candidate index 0 (function offset
1200). If the candidate array is empty it returns an empty slot. It does
not test WeaponStats.SupportedCaliber or rebuild the candidate set.

The native bridge is independently instruction-backed. The original
registration pair at `0xB085300` names GetSlotsSupportingFilter and points
to exec `0x67A7900`; its call at `0x67A7AA4` enters worker `0x6792CB0`.
Worker `0x6792F96–0x6792FA1` passes the supplied filter, candidate item id
and resolved definition's ItemContext (`definition+0x38`) to `0x67A2B40`.
That is the same exact-id OR parent-aware context evaluator established
above. The generic filter direction is therefore on the actual normal
reload candidate path, rather than merely an unrelated inventory helper.

The action's activation check calls
`WDInventoryStatics.CanPerformReloadWithContext`. Its original registration
pair at `0xB361D50` points to exec `0x6C3C930`; instruction `0x6C3C9B0`
calls real native entry `0x6C3A1F0` (corpus row starts seven bytes early,
at `0x6C3A1E9`). On the normal ranged-item context, it resolves the weapon
slot and dispatches to `0x6C39D70` or `0x6C3A060`
(`0x6C3A3C3–0x6C3A42E`). Those routines query the relevant container
filters through `0x6792CB0` and inspect existing ammo quantities and
capacity. Capacity helper `0x6C3B320` compares chamber/magazine ammo
quantities against the slot's maximum. `0x6C29460` reads the relevant
container packing flag from its subslot-support fragment. These recovered
normal checks do not add a WeaponStats.SupportedCaliber condition.
This is a statement about the reviewed path, not all unrelated actions or
external runtime modifications.

### Handheld chamber and vehicle owner return the loaded item's asset

The handheld getter's selected subslot is now explicit in the original
instructions. `0x6C98377` loads global `0xD36C2D8`;
`0x6C9839A` resolves its container index, saves that byte at `0x6C983A2`,
and supplies it in `edx` to subslot accessor `0x6793E10` at `0x6C983B0`.
The decompiler omitted that accessor argument. The global's initializer
`0x129DF10` identifies it as `Item.Attachment.Chamber`. It then resolves
the actual chamber item definition, looks up WDInventoryFragment_Projectile
at `0x6C983EA–0x6C98410`, validates the fragment, and loads its fixed
ProjectileData pointer at `0x6C9845A`.

The vehicle owner's slot is independently confirmed from original table
bytes: `qword[0xB63E858+0x90] = imageBase+0x7645A30`. The getter adjusts
the interface pointer back to the owning actor by `-0x2B8`, resolves its
vehicle inventory, then obtains the loaded/direct/reserve ammo slot. It
resolves that slot's item definition at `0x7645D1C–0x7645D2B`, requests
WDInventoryFragment_Projectile at `0x7645D4B–0x7645D77`, validates its
class at `0x7645D88–0x7645DBB`, and loads fragment `+0x38` at
`0x7645DC1`. `0x76460A7` returns that same pointer. Class getter
`0x6C46A30` names WDInventoryFragment_Projectile; SDK names `+0x38`
ProjectileData. Its ammo-modifier construction is separate from this asset
selection. No search for a child ProjectileId replaces that pointer.

Vehicle insertion modes are material here. SDK values are UsesMagazines=0,
LoadsAmmoDirectly=1, PullsAmmoFromReserve=2. The native extension-data
constructor `0x76A8510` writes **1** to data `+0x170` at `0x76A8706`.
Artillery's cooked asset omits the field and inherits LoadsAmmoDirectly.
Its direct-slot getter `0x76448D0` gets the weapon item using configured
ItemSlotTag/WeaponItemId (`0x7647680`) and selects its `Item.Ammo` subslot
at `0x7644935–0x7644968`, with a first-subslot fallback. STN_03's fresh
extension explicitly selects PullsAmmoFromReserve. When a loaded slot is
unavailable, `0x7645BDD–0x7645C03` takes its reserve path through
`0x7646710`, using configured AmmoCaliberTag at data `+0x164`; the selected
reserve item still flows into the same fragment getter.

### Named cases: confirmed mappings and unsupported prefix candidates

All rows below were rechecked against fresh, bounded cooked exports.
They describe the normal configured path, conditional on ordinary ammo
availability, chamber state and inventory operation success.

| Weapon / candidate | Answer for the reviewed default path |
|---|---|
| M500 / 12g.RifledSlug | Supported association. M500's actual chamber allows context Item.Caliber.12g. The slug item's context is that parent tag and its fragment directly selects DA_12g_RifledSlug_ProjectileData. |
| MP43 / 12g.RifledSlug | Supported association. Both its actual weapon chamber and internal magazine allow Item.Caliber.12g. The same slug item selects the named asset. |
| TNK_01 artillery / 155mm.Standard and 155mm.Expensive | Supported associations. ID_VehicleTurretArtillery's Item.Ammo container allows parent Item.Caliber.155mm; both child-context item definitions pass and each directly selects its corresponding projectile. LoadsAmmoDirectly uses this weapon ammo slot. The extension starts with Expensive=10 and Standard=0, so support for Standard is not a claim that it starts loaded. |
| STN_03 / 120x800mm.Standard | Supported association. ID_120x800mm has the parent context Item.Caliber.120x800mm and directly selects DA_120x800mm_Standard_ProjectileData. Its extension uses reserve ammo and explicitly starts with this item=3. No child-projectile prefix test is needed. |
| ROT_02 and ROT_03 / 122mm.Havoc | **Not established by the reviewed normal/default item mapping.** Both extensions configure AmmoTag Id.Item.122mm and inherit LoadsAmmoDirectly. Their actual weapon items allow Item.Caliber.122mm and provide DefaultContainerItems Id.Item.122mm. That plain ammo definition directly selects DA_122mm_ProjectileData, whose ProjectileId is the parent Item.Caliber.122mm, with no variation fragment. The separate DA_122_mm_HAVOC_ProjectileData has child ProjectileId Item.Caliber.122mm.Havoc, but these default item paths do not select it. A parent context filter could accept another suitable ammo item; no such Havoc item-to-projectile mapping is demonstrated here. |
| CombatBow / Arrow.Explosive | **Not established as a compatible default-bow projectile.** The previously reviewed ID_CombatBow_MagInternal allows the parent Arrow context, but the actual ID_CombatBow root has only a Chamber container whose AllowList is exact Id.Item.Arrow, with no allowed-context entries. ID_Arrow_Explosive's distinct Id.Item.Arrow.Explosive fails that chamber filter. Its DefaultContainerItems also supplies the normal Id.Item.Arrow. The separate internal magazine's permissive filter does not override the weapon's chamber. |
| CGM4 / 84mm.TVGuided | **Not established as a compatible CGM4 projectile.** Its normal chamber allows exact Id.Item.84mm, no context alternatives. That definition has a plain WDInventoryFragment_Projectile selecting basic DA_84mm_ProjectileData. The fresh definition contains no Variations entry/fragment and no alternative ProjectileData in its fragment. The TVGuided asset's prefix supplies no normal item-to-chamber mapping. |

The bow-specific reload action was checked rather than assumed to share
normal behavior. Fresh DA_Action_BowReload selects B_Action_BowReload.
The latter's BP_CanActivate invokes B_Action_Reload.BP_CanActivate, and
its ubergraph offset 837 invokes the parent's BP_OnActivate. The child's
small functions add no ammo-id or chamber-filter replacement. Fresh
ID_CombatBow DataFragments contains no variation fragment overriding its
exact normal-arrow chamber filter. This closes the ordinary configured
path; it does not claim that no separate test/runtime script could ever
replace its chamber rules or projectile data.

For generator use, remove `caliber-parent-match` uncertainty from the
confirmed M500/MP43 slug, artillery Standard/Expensive and STN_03 Standard
associations. Bow/Explosive, CGM4/TVGuided and ROT_02/ROT_03 Havoc must not
be advertised as confirmed compatible sources merely because
child_calibers finds their ProjectileId prefixes. They are concrete
default-path exclusions/absent mappings, not evidence that the normal
reload path universally admits descendants. Preserve their standalone
projectile data. Keep ancillary owner provenance as its separate open issue.

### Reproduction boundary and source hashes

Fresh JSON remains outside the repository under
`round8_caliber_reload_20261019` (12 named packages),
`round8_caliber_reload_more_20261019` (artillery item and STN_03 extension),
`round8_caliber_reload_bow_20261019` (actual bow item),
`round8_caliber_bow_actions_20261019` (bow action definition and MP43 item),
`round8_caliber_bow_reload_20261019` (bow reload Blueprint),
`round8_caliber_havoc_20261019` (both helicopter extensions and 122mm item),
`round8_caliber_havoc_items_20261019` (their weapon items), and
`round8_caliber_havoc_projectiles_20261019` (parent and Havoc projectiles), all under
`E:/Reverse_Engineer/wardogs_analysis`. CUE4Parse read installed paks
offline; the AES key was supplied only by path and its contents were not
inspected. The existing B_Action_Reload export/listing was read locally;
complete Blueprint dumps are not published here.

| Source JSON | SHA-256 |
|---|---|
| B_Action_Reload | `e5ef72679412cf9c175be74ae56518bd08a26c10d67563ae41dd58ccdd8a94ad` |
| ID_CombatBow | `e6d6fafd70f7abbc09fe0a831a36b4534862f14ffa9283542c1b1c35bd1db0c2` |
| B_Action_BowReload | `77d6b8b8c85a196bf78fe05b26d0ccab1a40244d04e55f8581c02d19f2d59b8f` |
| ID_CGM4 | `92de203131c8abc32365cb72c72c461046f601b07843c414ee25c8b9b5733949` |
| ID_84mm | `f682f9471e639609722d35a32e3da540c03c2fd57b35cac4bd4d3c82f938da25` |
| ID_MP43 | `2429a0dc2878aff0fd90ef5915070e78b820e7eda6df78047515a4da25654b08` |
| ID_VehicleTurretArtillery | `8e05ca74b7028cfd544a942bed6aa9748ada2f10848bce2edd8ca4b282c4c96f` |
| WE_STN_03_Heavy_MainBarrel | `c5012a52eef7154fbda8af6429e3a7ae6c4c133f80075fa0b61058495dbd12ee` |
| ID_122mm | `d75b7a0dcf6e3e0c35400d301367a306f92ab69b135fb4b23ae2a2af74e1aa62` |
| WE_ROT_02_Weapon_122mm | `97e6405ab40de2c91fa6ff3696da409c76fdeea0bb8ecb0986f854ebf0a3a7c3` |
| WE_ROT_03_Weapon_122mm | `fd42c1139d7e6d61daa570a4eb149776fc9a64b81b3e6a8eae9da8005d0af197` |
| ID_VehicleHelicopterRockets | `cb62f7f4ae6f11a9e3a52c92fe9d00001cd328134121335a0ebc67cb30dff2d3` |
| ID_VehicleHelicopterRockets_ROT_03 | `530c45bbf48f5d0d1e81e53611230a580e05701071a503d6fe4a6eef687abac2` |

> **Round 19 re-verification.** Evidence level: static-analysis image; virtualized dispatch not removed. Function `0x395BE30` begins with a protection-layer dispatch stub in the static-analysis image (`mov reg,[rip+x]` then `jmp [reg+disp]` through a runtime-filled global table, so its target is not statically resolvable); the older reference image holds the plain body, and it iterates the filter's explicit tags and searches each in the item context's explicit array (`+0`/`+8`) and cached parent array (`+0x10`/`+0x18`), the second loop at `0x395BE7E`–`0x395BE9E`, as claimed above. Classification: unaffected by the stub.
>
> **Round 19 re-verification.** Evidence level: static-analysis image; virtualized dispatch not removed. `0x6B74E30` likewise starts with a dispatch stub in the static-analysis image; the reference body hashes the byte id first (table lookup, `0x6B74E8E`–`0x6B74EC8`) and then a composite key `(proxy << 8) | id` (`0x6B74ED6`–`0x6B74F26`), writing the found record to the output, matching the claim. Unaffected.
