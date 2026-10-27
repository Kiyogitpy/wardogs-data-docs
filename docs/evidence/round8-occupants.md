# Round 8 evidence: occupant damage

Static, offline review of the restored CL-516586 executable with the provided Capstone helper, plus the decompilation corpus and `sdk/raw`. No game or service was run. The two routines are the `UWDVehicleOperatorComponent` vtable slots 160 and 161 (`0x7692B60` and `0x768ED20`); their corpus bodies are marked unreviewed.

## Findings

- **Amount:** slot 160 loads a single-precision constant from RVA `0x9AADAE8` into `xmm1` immediately before the `0x6BB4D30` event builder call at `0x7692E9B`. The restored executable stores `1000.0f` there. Slot 161 preserves its incoming `xmm1` in `xmm6` at entry and forwards it back in `xmm1` to the event builder at `0x768EF9A`; this routine has no preceding scaling of that value. Both pass the event through `UWDDamageSubsystem::ModifyDamage` afterwards, so these are starting amounts, not necessarily final applied damage.
- **Source data:** both routines build `FWDDamageEventData` through `0x6BB4D30`. They provide `SourceEntityData` from an entity-data object obtained through `sub_146B4C2B0` / `unk_141C36300`, and pass an optional source actor (falling back to the owning actor) into the `SourceActor` field. Slot 160 appends tag globals `qword_14D36A490` and `qword_14D36A800` to its local source context; slot 161 appends `qword_14D36A590` and `qword_14D36A810`. The source entity tag, context and cause tag are copied as `FWDDamageEntityData` fields. This confirms context construction, but this review did not resolve those four globals to readable tag names or assign the documented context pairs to each slot. The open-item note in [`_tools/infantry_tables.py`](../../_tools/infantry_tables.py#L423) lists the candidate tags as `Meta.Damage.Explosive.VehicleExplosion` + `DamageType.Explosive`, and `Meta.Damage.Vehicle` + `DamageType.Enviroment`.
- **Hit location:** both routines zero a full 0x100-byte local `FHitResult`, then set selected standard defaults and pass it to `0x6BB4D30`, which copies it into `FWDDamageEventData.HitResult`. Neither routine writes a bone name into that zeroed result. Both also pass the `None` gameplay tag for `FWDDamageEventData.HitLocationTag`. The synthetic hit therefore has no supplied `BoneName` or explicit hit-location tag.

SDK layout anchors: `FWDDamageEventData` places `SourceActor` at `0x58`, `SourceEntityData` at `0x60`, `HitResult` at `0x90`, and `HitLocationTag` at `0x1A0`; `FWDDamageEntityData` is `Tag`, `Context`, `CauseEntityTag` at offsets `0`, `8`, `0x28`. `sub_146BB4D30` writes the amount and these fields into the event layout. The aliases for both entrypoints are recorded in [vehicle evidence](vehicles.md#3-table).

## Suggested doc edit

The infantry generator now records slot 160's `1000.0f` starting amount and slot 161's caller-supplied float, with no bone or explicit hit-location tag. The integrating lead resolved the readable tag names below; they are no longer an open question.

## Integration verification: tag names resolved

The integrating lead independently decoded the static initializers and their
literal ASCII operands. Initializer `0x127A830` registers global `0xD36A490`
from `0xB348028`, `Meta.Damage.Explosive.VehicleExplosion`.
Initializer `0x127A150` registers `0xD36A800` as
`Meta.Damage.DamageType.Explosive` (also checked by the radial pass).
Initializer `0x127BF50` registers `0xD36A590` from `0xB348568`,
`Meta.Damage.Vehicle`. Initializer `0x127A0B0` registers `0xD36A810`
from `0xB3490D8`, `Meta.Damage.DamageType.Enviroment` (the spelling is
the shipped tag). Thus slot 160 is the explosion context pair and slot
161 the vehicle/environment pair. These are appended context tags,
not replacements for the copied source entity's root tag.

The amount and no-bone conclusions above plus this mapping close the
original occupant-damage question at these two entrypoints. They do not
establish every caller-supplied slot-161 amount or final health outcome.
