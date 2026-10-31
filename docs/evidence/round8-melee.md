---
title: Round 8 melee event construction
nav_exclude: true
---

# Round 8: melee event construction

Static research, 2026-10-18. The actual melee damage logic is Blueprint,
not the native `UWDItemExtension_CharacterMelee` initializer. Three cooked
Blueprints were exported successfully with the existing offline
`WdExtract` tool into the new local directory
`E:/Reverse_Engineer/wardogs_analysis/round8_melee_20261018`. The extractor
consumed the authorized key-file path without exposing its contents.
No game execution, attachment, IDA database access or service access was
used. Raw Blueprint dumps remain local.

## Confirmed behavior

| Character damage path | Starting amount | Source tag | Source context |
|---|---|---|---|
| `/Game/GameMechanics/Actions/Melee/B_Action_Melee`, `DamagePlayer` | Selected `MeleeAction.Damage` | Held item's `ItemId`, for example `Id.Item.Fists` | Singleton `Meta.Damage.DamageType.Melee` |
| `/Game/GameMechanics/Actions/Weapons/B_Action_MeleeBash`, `DamagePlayer` | `Weapon Stats.MeleeDamage` | Held item's `ItemId` | Singleton `Meta.Damage.DamageType.Melee` |
| `/Game/GameMechanics/ExtensionComponents/B_WDItemExtension_ItemMelee`, `DamagePlayer` | Selected `MeleeAction.Damage` | Held item's `WDItemExtensionData_CharacterMelee.DamageEntityData.Tag`, e.g. `Meta.Damage.Utility.Crowbar` | Singleton valid `DamageTypeTagOverride`, otherwise singleton `Meta.Damage.DamageType.Melee` |

All three call the inventory armor operation with an explicit
`Meta.Damage.HitLocation.Infantry.Torso` and bone name `None`, then call
`ModifyDamage(EventData, false)`, then put its result into
`FWDDamageContext.CurrentDamage` and call `BP_DamageActor`. The point
damage event uses damage type Melee, or the extension's valid override.
The source context is assigned, not appended to the extension's original
context. The extension stores the override in `ActivateMeleeDamage` at
bytecode offset 5; the false/true cases of its `DamagePlayer` switch at
1380 explicitly select the Melee/default or override singleton.

**The armor operation's returned event is ignored.** Consequently, the
explicit Torso tag controls the separately queued armor events, but is
not transferred to the health event. The health event keeps its original
empty `HitLocationTag` and default hit result with bone `None`; its
target entity is initially empty and is discovered by the converter.
There is no lookup of the actual melee trace's bone for this character
health event. This is verified static behavior, not a gameplay test.

### Why the ignored return matters

The cooked call is an assignment to
`CallFunc_BP_TryDamageArmorSimple_ReturnValue`. That local has no later
read in any of the three `DamagePlayer` functions. They subsequently
evaluate the original `EventData` variable.

The reflected native entry `0x6B67870` confirms that the operation does
not alter the caller's event through its const-reference parameter:

| Instruction | Meaning |
|---|---|
| `0x6B6797C`–`0x6B6798F` | Obtain the input event address |
| `0x6B679AC`: call `0x6B4D540` | Deep-copy input event into a separate local event |
| `0x6B679B1`: `lea r9,[rbp+0xF0]` | Pass the local copy to the general armor implementation |
| `0x6B679C1`: call `0x6B53580` | Process armor coverage and queue armor events on that copy |
| `0x6B679D0`: call `0x6B4F730` | Move the processed copy into the reflected return value |

The copy constructor duplicates the entity context containers and event
arrays (`0x6B4D540`, corpus body and exe). The implementation can still
queue armor damage on the inventory component, so ignoring the return
does not suppress those side effects. It does suppress reuse of the
filtered target context and Torso hit-location field in the health
evaluation. See [the armor report](round8-armor.md) for the general hook
and converter branches (`0x6EF90B9`, `0x6EF91B3`, `0x6EF9299`).

Thus the character's complete recovered armor/helmet context reaches
health-rule matching. Do not model this as projectile-style selection
of one piece by the trace bone. The native custom armor-reduction
operation still chooses the first armor-or-helmet tag in context order,
as described in DamagePipeline §7.5; this pass does not establish that
runtime context order for every equipment combination.

## Exact Blueprint anchors

Offsets below are Kismet statement offsets within the named function,
not native RVAs. Both the formatted statements and their original JSON
expression trees were reviewed; particularly the override switch and the
unused return were checked in the original trees.

| Blueprint / function | Important offsets |
|---|---|
| `B_Action_Melee::ExecuteUbergraph_B_Action_Melee` | 2864 / 2982: look up extension `MeleeActions` by `this.ActionTag`; 2955: copy settings to `this.MeleeAction`; 3073: stop when map lookup fails; 3992: box trace |
| `B_Action_Melee::DamagePlayer` | 5: initialize event; 1321: amount from selected settings; 1855: causer from held `ItemId`; 2076 / 2112: source tag/context; 2564: event amount; 2672: empty target entity; 2859: default hit result; 3880: armor call; 4035: evaluate original event; 4276: apply |
| `B_Action_MeleeBash::DamagePlayer` | 175: amount from weapon stats; 709: held `ItemId`; 930 / 966: source tag/context; 1418: event amount; 1526: empty target entity; 1713: default hit result; 2734: armor call; 2889: evaluate original event; 3130: apply |
| `B_WDItemExtension_ItemMelee::GetActorsHit` | 251 / 369: `MeleeActions[ActionTag]`; 342: selected settings; 897: box trace |
| `B_WDItemExtension_ItemMelee::DamagePlayer` | 175: amount from settings; 790: melee extension lookup; 1313: source tag from extension; 1380: context switch; 1830: event amount; 1938: empty target entity; 2125: default hit result; 3228: armor call; 3353: evaluate original event; 3624: apply |

The extension's `ActivateMeleeDamage` dispatches characters to
`DamagePlayer` at offset 783 after character/LOS/vehicle checks.
Noncharacters take `Apply Simple Damage` (offset 1349 or 1375), whose
offset 123 calls `SimpleDamageActor` with the same selected damage and
Melee/override damage type. The action and bash graphs likewise use
`SimpleDamageActor` for their noncharacter branch (ubergraph offsets
2255 and 2962 respectively). The full trace-selection/LOS semantics
were not expanded in this bounded pass.

## Native and data corroboration

`WDItemExtensionData_CharacterMelee` stores `MeleeActions` at `+0x48`
and `DamageEntityData` at `+0x98`; settings store `Damage` at `+0x18`
and `TraceDistance` at `+0x1C` (`sdk/raw/WDGame_classes.hpp:39212`,
`sdk/raw/WDGame_structs.hpp:9562`). Native initialization
`0x6C67D40` copies that entity data into the extension's damage-entity
component: `lea rdx,[rbx+0x98]` at `0x6C67E4B`, call `0x6B18E30` at
`0x6C67E52`; the latter copies tag/context/cause at component
`+0xE0`/`+0xE8`/`+0x108`. It is not the damage-applying path.

The data asset
[`DA_Action_Melee_PrimaryUse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Melee/DA_Action_Melee_PrimaryUse.json)
references `B_Action_Melee`; the secondary-use definition references the
same class. The
`MeleeBash` action
references `B_Action_MeleeBash`.
[`ID_Fists`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Fists/ID_Fists.json)
stores 25 damage for each primary/secondary setting.
[`ID_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Data/ID_Crowbar.json)
stores 100 damage and explicitly selects
`B_WDItemExtension_ItemMelee`. Its utility tag therefore belongs to the
extension path, while `B_Action_Melee` uses the held item ID instead.

Native `BP_DamageActor` entry `0x6F07C10` calls apply helper
`0x6EF9840` without evaluating damage again, consistent with the explicit
Blueprint `ModifyDamage` immediately before it.

## Reproduction and limits

`WdExtract dump` exported exactly these three packages; it reported
`ok=3 fail=0`. Local JSON export SHA-256 hashes:

- `B_Action_Melee`: `a91579a7f053806807d793e74b5bb2b07c7993cd5235d6f1f0f333f5d51ef8b0`
- `B_Action_MeleeBash`: `eda2d4395806bfaea6c5498edac714be2c97a3bb54649afe1ef1df0fef393e2f`
- `B_WDItemExtension_ItemMelee`: `10cdaa313576640ed4878bf19720b6751bd4f8bfd257eb29c93731518a970d10`

`kismet_listing.py` rendered the extension
directly; the two action ubergraphs contain a persistent-frame let form
unsupported by that formatter. A task-local copy handled that statement
without changing the repository tool. Conclusions above were checked
against original JSON, not inferred from the truncated rendering of
unsupported expressions.

Melee event construction, amount provenance, source tags, armor call and
the ignored-return distinction are resolved for the three named paths.
All possible Blueprint subclasses/callers, activation timing, complete
trace selection and every override producer are outside this pass.
