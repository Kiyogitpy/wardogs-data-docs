---
title: "Combat Data Flow"
parent: "Pipelines"
nav_order: 4
redirect_from: ["/Wardogs_CombatDataFlow_v1.html", "/Wardogs_CombatDataFlow_v1"]
---

# Wardogs — Combat Data Flow Integration

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

End-to-end view of how the three pipeline docs integrate. Reads a
single trigger event (a weapon fire) and follows it through all three
pipelines until the target's health changes.

Companion to:
- [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) — infantry damage modifier chain
- [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) — vehicle damage rule tables
- [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) — BH-GAS effect application

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7

---

## The combat data flow at a glance

```
┌──────────────────────────────────────────────────────────────────┐
│  INPUT: player presses Fire                                      │
└───────────────────────────┬──────────────────────────────────────┘
                            │
            ┌───────────────▼───────────────┐
            │ WEAPON STATE                  │
            │ DA_<Weapon>_Stats JSON        │─────────────────────┐
            │   SupportedCaliber            │                     │
            │   InitialBulletSpeed          │                     │
            │   EffectiveRange              │                     │
            │   RecoilPattern               │                     │
            │   SupportedFireModes          │                     │
            │   Base damage (per caliber)   │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ ATTACHMENTS (GAS)             │                     │
            │ UBHGameplayEffectComponent    │                     │
            │ holds active effects:         │                     │
            │   - GE_MAGZ_* (magazine)      │                     │
            │   - GE_FGRP_* (foregrip)      │                     │
            │   - GE_MUZL_* (muzzle)        │                     │
            │   - GE_SGHT_* (sight)         │                     │
            │ Each modifies weapon          │                     │
            │ attributes (ADSTime,          │                     │
            │ VerticalRecoilMultiplier,     │                     │
            │ ...) via TMap<Tag, float>.    │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ FIRE EVENT                    │                     │
            │ Projectile spawn with:        │                     │
            │   Caliber tag                 │                     │
            │   Weapon archetype tag        │                     │
            │   Initial velocity            │                     │
            │   Instigator (player)         │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ DAMAGE EVENT                  │                     │
            │ The calling system builds     │                     │
            │ FWDDamageEventData: amount S, │                     │
            │ instigator/target/source tags │                     │
            │ and context, hit location     │                     │
            │ (hit-validation edge not      │                     │
            │  traced)                      │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ UWDDamageSubsystem::          │                     │
            │   ModifyDamage                │                     │
            │ Walk target tag → parents;    │                     │
            │ each level's registry row     │                     │
            │ contributes matching entries  │                     │
            │ (infantry, vehicle and armor  │                     │
            │  rule tables)                 │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ EVALUATE  (C starts at S)     │                     │
            │ order: tag level, then        │                     │
            │        category index         │                     │
            │ non-custom %: C ×= 1 + a/100  │                     │
            │ custom op:    C += delta      │                     │
            │   (bone, calibre, ammo, seat, │                     │
            │    armor durability)          │                     │
            │ once at end:  C = max(C, 0)   │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ APPLY                         │                     │
            │ Unreal damage event (type     │                     │
            │ from damage-type tag) →       │                     │
            │ target TakeDamage, or the     │                     │
            │ WDDamageable path             │                     │
            │ Characters: ReceiveDamage →   │                     │
            │ vitality → base value of      │                     │
            │ Attribute.Gameplay.Health     │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ GRANTED TAGS + GEs            │                     │
            │ On zero health:               │                     │
            │   Downed/Dead tag granted     │                     │
            │   GE_PlayerDowned applied     │                     │
            │   GameplayCue triggers        │                     │
            │     (VFX, audio, animation)   │                     │
            └───────────────────────────────┘                     │
                                                                  │
            Weapon state continues firing  ←──────────────────────┘
            (RecoilPattern walked, next
            shot's start conditions update
            via GE_Weapon_StanceRecoil_* etc.)
```

## Component responsibilities

| Component | Owns | Documented in |
|---|---|---|
| **Weapon stats** (`DA_<Weapon>_Stats` JSON) | Fire mode, projectile physics, recoil pattern, caliber/archetype tags | [`Wardogs_InfantryWeapons_Stats_v1.md`](../content/Wardogs_InfantryWeapons_Stats_v1.md) + [`Wardogs_Weapons_v2.md`](../content/Wardogs_Weapons_v2.md) |
| **Attachments GAS layer** (`GE_<Attachment>` applied via `UBHGameplayEffectComponent`) | Per-attachment modifiers to weapon attributes (ADS, recoil, mag capacity, etc.) | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) |
| **Hit validation** (`BHHitValidationWorldSubsystem`) | Declared in the SDK; its edge into the damage event is not traced | — |
| **Damage modification** (`UWDDamageSubsystem::ModifyDamage`) | Rule selection, ordering and arithmetic; five custom operations (bone, calibre, ammo type, seat, armor durability) | [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) §1–7 |
| **Damage hand-off** | Unreal damage event and `TakeDamage` on the target | [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) §1.1 |
| **Vehicle damage** (same rule pipeline, per-vehicle rows) | 21 vehicle tables (23 rows, 581 selectable entries) through the same evaluator, then the section health model | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) |
| **Attribute application** (`UBHGameplayEffectComponent`) | Attribute storage and replication. Character damage writes the `Attribute.Gameplay.Health` base value directly (DamagePipeline §10) | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §4 |
| **GameplayCue dispatch** | VFX, audio and animation cues through `UWDGameplayCueComponent`, separate from effects | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §6 |

## Example — AK74M bullet to infantry torso

How far the pipelines get for one hit, and where the numbers stop.

### Inputs

| Input | Value | Source |
|---|---|---|
| Weapon stats | `DA_AK74M_Stats.json` | Fire data |
| Caliber tag | `Item.Caliber.545mm` | `SupportedCaliber[0]` |
| Weapon archetype tag | `Meta.Damage.Weapon.AR` | Classification |
| Initial bullet speed | `89000.0` cm/s (= 890 m/s) | `InitialBulletSpeed` |
| Effective range | `1000.0` m | `EffectiveRange` |
| Base damage | (lookup by caliber) | Caliber damage table |
| Target | Enemy player, 100 HP | Game state |
| Hit location | `Meta.Damage.HitLocation.Infantry.Torso.Upper` | Damage event |
| Ammo type | Standard (not AP/HP/Tracer) | Weapon mag content |

### Pipeline execution

```
S = 26        // DA_545mm_ProjectileData BaseDamage; source tag
              // Meta.Damage.Bullet.545mm, source context Arms.Medium +
              // Weapon.AR.AK47M + Item.Caliber.545mm + DamageType.Projectile

Step 1 — Attachments: GEs modify weapon attributes such as recoil, not
         the damage amount in the event.

Step 2 — ModifyDamage collects every infantry-row entry whose
         requirements match this event (DamagePipeline §4) and sorts
         them by category: Calibre, AmmoModifier, Bone, ...

Step 3 — Evaluate, C = S (every step is a factor, so order is irrelevant):
  Non-custom percentage entries   C ×= (1 + a/100) each
  B_ArchetypeCaliberModifiers     C ×= AR row [5.45mm]          = 1.00
  B_BoneDamageModifiers           C ×= Universal × AR row
                                       [Torso.Upper] = 1.10 × 0.885 = 0.9735
  Armor on the torso (bullets):   C ×= 1 − DPR × AAS / 100
                                       e.g. heavy armor, FMJ  = 0.50
  No non-custom entry with a factor other than 1 matches this hit.
  C = max(C, 0)  →  26 × 0.9735 = 25.3 unarmored, 12.7 with heavy armor

Step 4 — Hand-off: the target is WDDamageable, so IWDDamageable::ReceiveDamage
         → character vitality component (0x6B17760 → 0x6B82520).

Step 5 — Health write: Attribute.Gameplay.Health base value −= C via
         SetAttributeBaseValue; death when the current value reaches 0.
         Downed characters take no health write (DamagePipeline §10).
```

The earlier `baseDamage × 1.10` result assumed the Universal bone row and
a plain multiplicative chain. Neither is established, so it is withdrawn.

### What is still open

1. **Speed after drag.** Damage also scales with impact speed below the
   reference speed; how fast each round slows is not modelled.

Ammo types against armor are tabled in DamagePipeline §7.9.

The base damage, the event tags, armor coverage (only the piece covering
the hit counts, so the 12.7 applies to the torso, not a headshot),
evaluation order, every modifier and the distance falloff are
established: see DamagePipeline §5–7, with per-weapon numbers in §7.7–7.8.
Armor durability only applies to explosive-blunt and melee hits; bullets
on armor go through the ammo-type Blueprint.

## Example — rocket to tank

### Inputs

| Input | Value | Source |
|---|---|---|
| Weapon | Launcher firing a 125mm rocket | Weapon stat |
| Damage source tags | `Meta.Damage.Explosive.Rocket.125mm`, `Meta.Damage.Explosive.Radius.Inner` | Projectile config |
| Target | TNK_01 Heavy, full health | Game state |
| Hit section | `Body.StrongArea` | Section resolution |

### Pipeline execution

```
S = <125mm rocket damage>

Step 1 — Rules (same evaluator as infantry):
  Target tag = VehicleDamageTag = Meta.Damage.Vehicle.Land.Tracked.TNK_01.Heavy
  Walk: TNK_01.Heavy row → parent rows → generic Meta.Damage.Vehicle row

Step 2 — Matching entries (TNK_01.Heavy):
  Explosive.Rocket.125mm               +31.5   → ×1.315
  Explosive.Rocket + Radius.Inner      +17.5   → ×1.175
  #12 Rocket, HitLocation.Vehicle        0     → ×1
  Generic row: nothing for a non-HollowPoint rocket
  C = S × 1.545   (AntiAir row ×1.645, Artillery ×1.351)

Step 3 — Section application (VP_TNK_01_Heavy):
  Body.StrongArea PreDamageRouting: 0.4 × C to main Health
  The section takes the rest
  Section-damaged handling: message if depleted (main Health depleted
    → vehicle destroyed, no post routing)
  PostDamageRouting once depleted: overflow ×1.0 to main Health
```

The earlier "Rule 18 +150 % → ×2.5" came from ROT_02's 120 mm entry, not
TNK_01. See VehicleDamagePipeline §4–5 for the section order and routing
rules.

## Cross-section quick reference

| Question | See |
|---|---|
| What are the 5 damage modifiers? | [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) §3.1, §7 |
| What's the actual bone multiplier value for a specific hit location? | [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) §8.1 |
| What's the damage profile for ROT_02 Havoc? | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) §5.1 |
| How many vehicles have per-class damage rules? | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) §2.1 — 21 tables, 23 rows |
| What's the GAS attribute system? | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §4 — tag-keyed records with double base/current values, no `UAttributeSet` |
| How many GE_* effect classes ship? | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §2 — 338 total |
| What are the units on `InitialBulletSpeed`? | [`UNITS.md`](../docs/UNITS.md) §1 — cm/s |
| Where is `CT_Weapon_Spread` defined? | [`CROSS_REFERENCE.md`](../docs/CROSS_REFERENCE.md) `CT_*` section |

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — First integration view. Covers end-to-end from fire event through damage pipelines to attribute application. Two worked examples: AK74M → infantry torso, 125mm rocket → tank front-plate. Remaining 4 blocking gaps catalogued for next-pass resolution. |
| 2026-10-17 | Infantry path corrected against the damage pipeline: removed the "server-side" hit-validation claim and the untraced `SetAttributeBaseValue` write; replaced the multiplicative chain with the evaluator's arithmetic and the `TakeDamage` hand-off; withdrew the `× 1.10` example. Vehicle example unchanged pending the vehicle pass. |
| 2026-10-17 | Rocket-to-tank example rewritten from the vehicle audit: same rule evaluator, real TNK_01 Heavy matches (×1.545), real section routing. |
