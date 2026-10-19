---
title: Round 8 explosive actors
nav_exclude: true
---

# Round 8: explosive actors and Molotov fire

Static research, 2026-10-18. Successfully exported seven requested actor
Blueprints, the Molotov trigger volume and fire field, and its burning
effect with the existing offline `WdExtract` tool. New local research
directory: `E:/Reverse_Engineer/wardogs_analysis/round8_explosives_20261018`.
The authorized key-file path was consumed only by the extractor; its
contents were not inspected or printed. Raw dumps remain local. Native
claims below were checked against instructions in the restored executable
and the read-only CL-516586 corpus; no game or service was run.

## Detonation values

These are resolved class defaults, including native/Blueprint inheritance.
Distances retain the raw Unreal units, centimetres. `S` is `BaseDamage`,
`R` is `ExplosiveRadius`, `E` is `EffectiveExplosiveRadius`, `m` is
`MinimumExplosiveDamage`, and `F` is `ExplosiveDamageFallOff`.

| Actor | Source entity tag | S | R | E | m | F |
|---|---|---:|---:|---:|---:|---:|
| M67 frag (`B_FragGrenade`) | `Meta.Damage.Grenade` | 100 | 1000 | 500 | 10 | 1 |
| C4 (`B_ThrowableC4`) | `Meta.Damage.Explosive.Utility.C4` | 250 | 600 | 250 | 20 | 1 |
| AT mine (`B_AT_Mine`) | `Meta.Damage.Explosive.Utility.ATMine` | 300 | 750 | 375 | 50 | 0.5 |
| Claymore (`B_Claymore`) | `Meta.Damage.Explosive.Utility.Claymore` | 150 | 300 | 150 | 30 | 0.5 |
| IED (`B_ThrowableIED`) | `Meta.Damage.Explosive.Utility.IED` | 300 | 800 | 400 | 60 | 1 |
| Molotov initial burst (`B_Molotov`) | `Meta.Damage.Molotov` | 40 | 500 | 250 | 10 | 1 |

The placed IED is a placement proxy: its Blueprint spawns
`B_ThrowableIED`, rather than defining a separate blast. In
`B_PlaceableIED::ExecuteUbergraph_B_PlaceableIED`, offset 488 selects
that class, 946 finishes spawning it, and 1096 / 1815 initialize/release
it with `Action.Throw.Primary.IED`; 1916 transfers instigator state.

All six blast types reach the shared radial evaluator `0x6F06540`, so
the reviewed radial amount/falloff arithmetic applies. These are not
final health-loss numbers: source/target rules, radius context, LOS and
per-component evaluation still apply. See [round8-radial.md](round8-radial.md).
The Molotov also has a separate sustained-fire path below.

### Inherited values were checked in the executable

`AWDExplosive`'s constructor `0x6CA7800` initializes damage values at
actor `+0x518` through `0x6BB9850`. Instructions
`0x6CA7A79`–`0x6CA7ABF` pass `S=100`, `R=1000`, `m=30`, `E=500`,
`F=0.5`. The struct constructor writes them to offsets
`+0`, `+4`, `+8`, `+0xC`, `+0x10` (`0x6BB9858`–`0x6BB9883`).
It initializes `bCheckLOS` and `bPreferUpwardsTrace` true at `0x6BB9888`.
`AWDGrenade` calls the explosive constructor at `0x6CADCAA` and does not
replace those numeric damage values. The frag Blueprint overrides only
the minimum and falloff among the five columns, yielding its table row.

`AWDLandminePlaceable` separately initializes the same five numeric
defaults: `0x772124F`–`0x77212F0`, struct at actor `+0x3A8`.
Thus Claymore's omitted minimum is 30 and its omitted falloff is 0.5;
the AT mine inherits falloff 0.5. Omitted fields are not zero.

`B_ThrowableIED` explicitly inherits `B_ThrowableC4`; its CDO overrides
S/R/E/m and inherits C4's falloff 1. C4 supplies all five values, and
Molotov supplies all five values. The table's source tags come from the
corresponding damage-entity subobject, except frag's inherited native tag.

## Actual detonation paths and context

### Frag, C4, IED and the Molotov burst

The reflected `WDExplosive::Auth_Explode` entry `0x6CACE50` dispatches
actor virtual slot 237 (`+0x768`) at `0x6CACF81`.
For explosives/C4 this is `0x6CA80E0`, which calls blast construction
`0x6CA8D20` at `0x6CA857A`; the radial call is `0x6CA91ED`.
The helper copies the actor's damage-entity component, appends actor
`DamageTag` (`+0x4B8`, address formation `0x6CA8E10`), and passes
`ExplosionDamageValues` (`+0x518`) to the radial evaluator with LOS true.
It supplies damage type `Meta.Damage.DamageType.Explosive`, which the
radial helper adds to source context along with the Inner/Outer tag.

C4's actual `DelayedDetonate` route calls `Auth_Explode` in
`ExecuteUbergraph_B_ThrowableC4` at Kismet offset 5086.
`B_ThrowableIED::ExecuteUbergraph_B_ThrowableIED` offset 10 calls the
parent C4 `Detonate`. The extracted C4 Blueprint also contains an
externally callable `CreateExplosion` helper with a radial call at
ubergraph offset 1382, but no internal call to that helper was found.
It must not be counted as a second detonation merely because it exists.

For `AWDGrenade`, slot 237 is `0x6CAE3B0`, which finishes by tail-jumping
to the explosive implementation at `0x6CAE468`.
Molotov's slot 237 override `0x86A15B0` creates fire objects, then calls
the grenade implementation at `0x86A318D`; it therefore also gets the
native burst above.

**Frag context quirk, verified in the exe.** Its native component source
tag is `Meta.Damage.Grenade`: grenade construction reads global
`0xD36A728` and sets the component tag at `0x6CADD96`; initializer
`0x127A8D0` references that exact string at `0x127A8EB`.
The actor's inherited `DamageTag`, appended by blast construction, is
`Meta.Damage.Explosive.Rocket.60mm`, not a grenade tag. Construction
loads global `0xD36A488` and stores it at `+0x4B8` at `0x6CADDA9`;
initializer `0x127A790` references the exact 60mm string at
`0x127A7AB`. The frag CDO overrides neither value. Thus source root and
context must be kept distinct when matching damage rules.

For C4, IED and Molotov the cooked `DamageTag` equals their source tag
from the table; the native helper appends that tag to context. Native
explosive damage type is identified by initializer `0x127A150`, exact
string reference `0x127A16B`, global `0xD36A800`.

### AT mine and Claymore

Both are `AWDLandminePlaceable` Blueprints, with their own live
`CreateExplosion` / `Create Explosion` control flow. They do not need
the thrown-explosive native path to obtain the listed values.

| Blueprint anchor | Evidence |
|---|---|
| `B_AT_Mine::GetDamageData` 167 / 232 | Origin is actor location plus `ExplosionTraceOffset`; CDO offset is `(0,0,50)` |
| Same function 297 / 373 | Source is `WDDamageEntity.DamageEntityData`; values are `this.ExplosionDamageValues` |
| Same function 72 / 400 | The supplied **damage-type tag is `Meta.Damage.Explosive.Utility.ATMine`**, rather than `DamageType.Explosive` |
| `B_AT_Mine::ExecuteUbergraph_B_AT_Mine` 2879 / 3248 | Mutually exclusive controller-present/absent radial calls, LOS true |
| `B_Claymore::GetDamageData` 109 / 273 / 349 | Origin is `ExplosionPoint` component location; component source data and class damage values |
| Same function 0 / 376 | Supplied damage type is `Meta.Damage.DamageType.Explosive` |
| `B_Claymore::ExecuteUbergraph_B_Claymore` 959 / 1182 | Mutually exclusive radial calls depending on controller validity, LOS true |

Both ignore self in their radial ignore array. Both source components
have the root tag shown in the values table and no serialized context
tags. The shared radial code appends their supplied damage-type tag and
radius tag. Consequently the AT mine's context differs from Claymore's
even though both roots are under `Meta.Damage.Explosive`.

## Molotov sustained fire

`B_Molotov` configures `B_Molotov_TriggerVolume` and
`B_Molotov_FireField` as its spawned classes. The native override above
contains their creation; its full patch-placement geometry was not
decoded here.

The trigger volume CDO accepts `WDMoverCharacter` and
`BHBaseVehiclePawn`, applies `GE_MolotovBurning` once per configured
effect application, and disables periodic queries. That effect's only
serialized override is granting `State.Player.Molotov.Burning`; the
damage amounts below belong to the fire field, not an assumed health
modifier inside that effect.

`B_Molotov_FireField` defaults are `FlatPlayerDamage=15` and
`FlatVehicleDamage=2`. Its `OnTriggerVolumeUpdated` maintains an actor
array and starts a looping **0.4-second timer** at bytecode offset 445
for `OnActorsArrayLoop`. Begin-play overlap discovery starts the same
timer at ubergraph offset 986. Each loop attempts character or vehicle
damage (offsets 328 / 893 in `OnActorsArrayLoop`).

- `TryDamagePlayer` checks `State.Player.Vitality.Alive` (128), then
  calls `SimpleDamageActorWithInstigatorController` with 15 and damage
  type **`Meta.Damage.DamageType.Enviroment`** at offset 621. Its hit
  result is synthetic, with bone names `None` (320). The spelling is
  the game's tag. Native reflected entry `0x6F09210` builds/evaluates
  the simple event without the general armor hook.
- `TryDamageVehicle` calls the vehicle damage-model component's
  `ApplyDamage(Attribute.Gameplay.Health, 2, ...)` at offset 507.

The configured cadence corresponds to 37.5 player damage or 5 vehicle
damage per second **before downstream handling and only while the
actor remains eligible**. These are derived rates, not measured DPS.
The fire-field and trigger-volume CDOs both have `InitialLifeSpan=45`;
this alone does not prove a fixed 45-second damaging footprint, since
native fire-patch lifetime/placement logic also runs.

## Reproduction and remaining limits

Package paths come directly from the exported item references:
`/Game/Weapons/Grenades/B_FragGrenade`,
`/C4/Data/Blueprints/B_ThrowableC4`, `/AT_mine/Data/Blueprints/B_AT_Mine`,
`/Claymore/Data/Blueprints/B_Claymore`,
`/Molotov/Data/Blueprints/B_Molotov`, and
`/IED/Blueprints/{B_ThrowableIED,B_PlaceableIED}`. Three additional
Molotov packages were followed from those actor defaults. All ten
exports succeeded. Findings use reviewed statements and original
Kismet expression trees; raw dumps and generated listings were not
added to the repository.

Detonation amount/source/provenance is resolved for the named actors,
and the separate Molotov fire-damage cadence is located. Remaining
bounded gaps: complete trigger/arming logic, exact native Molotov patch
geometry and lifetime, all external callers of C4's unused-internally
helper, and runtime gameplay outcomes. No authority or exploitability
claims are made.
