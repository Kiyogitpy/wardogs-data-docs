# Wardogs — Combat Data Flow Integration (v1)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

End-to-end view of how the three pipeline docs integrate. Reads a
single trigger event (a weapon fire) and follows it through all three
pipelines until the target's health changes.

Companion to:
- [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) — infantry damage modifier chain
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
            │ HIT DETECTION                 │                     │
            │ BHHitValidationWorldSubsystem │                     │
            │ (server-side)                 │                     │
            │   Resolves hit location tag   │                     │
            │   Resolves target entity      │                     │
            │   Builds FWDModifyDamageData  │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
                   ┌────────▼────────┐                            │
                   │  TARGET TYPE?   │                            │
                   └────┬──────┬─────┘                            │
                        │      │                                  │
            ┌───────────▼─┐  ┌─▼──────────────────┐               │
            │ INFANTRY    │  │ VEHICLE             │               │
            │             │  │                     │               │
            │ 5-modifier  │  │ Per-vehicle rule    │               │
            │ chain:      │  │ table lookup:       │               │
            │  AmmoType   │  │  Match on Source,   │               │
            │  Caliber    │  │  Target, Instigator │               │
            │  Bone(loc)  │  │  requirements       │               │
            │  SeatRed    │  │                     │               │
            │  ArmorDur   │  │ Each matched entry  │               │
            │             │  │ applies Percentage  │               │
            │ Each is     │  │ Ongoing mod         │               │
            │ Percentage_ │  │ (-95% = reduce 95%, │               │
            │ Ongoing     │  │  +400% = x5)        │               │
            └──────┬──────┘  └────────┬────────────┘               │
                   │                  │                            │
                   └────────┬─────────┘                            │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ MULTIPLICATIVE STACK          │                     │
            │ finalAmount = baseDamage      │                     │
            │   × (1 + mod1/100)            │                     │
            │   × (1 + mod2/100)            │                     │
            │   × ...                       │                     │
            │                               │                     │
            │ (Resolution order unverified; │                     │
            │  §7.1 of DamagePipeline docs) │                     │
            └───────────────┬───────────────┘                     │
                            │                                     │
            ┌───────────────▼───────────────┐                     │
            │ ATTRIBUTE APPLICATION         │                     │
            │ UBHGameplayEffectComponent    │                     │
            │ ::SetAttributeBaseValue       │                     │
            │   Attribute = Health.Current  │                     │
            │   newbase = base - finalDmg   │                     │
            │                               │                     │
            │ Server-authoritative;         │                     │
            │ triggers replication          │                     │
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
| **Weapon stats** (`DA_<Weapon>_Stats` JSON) | Fire mode, projectile physics, recoil pattern, caliber/archetype tags | [`Wardogs_InfantryWeapons_Stats_v1.md`](Wardogs_InfantryWeapons_Stats_v1.md) + [`Wardogs_Weapons_v2.md`](Wardogs_Weapons_v2.md) |
| **Attachments GAS layer** (`GE_<Attachment>` applied via `UBHGameplayEffectComponent`) | Per-attachment modifiers to weapon attributes (ADS, recoil, mag capacity, etc.) | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) |
| **Hit validation** (`BHHitValidationWorldSubsystem`) | Server-side hit confirmation, hit-location resolution, `FWDModifyDamageData` construction | [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) §2 |
| **Infantry damage** (5-modifier chain) | Caliber effectiveness, bone multipliers, ammo type, seat reduction, armor durability | [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) |
| **Vehicle damage** (per-vehicle rule tables) | Per-vehicle class filter+percentage rules; 22 vehicles with 16-66 rules each | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) |
| **Attribute application** (`UBHGameplayEffectComponent::SetAttributeBaseValue`) | Health/Stamina/Shield deductions, replication, respect for `bAllowClientPredicted*` flags | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §4 |
| **GameplayCue dispatch** | VFX, audio, animation playback on hit/damage events via `DA_CharacterEffectPresets` tag mapping | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §3 |

## Example — AK74M bullet to infantry torso

Fully worked example tying the three pipelines together.

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
| Hit location | `Meta.Damage.HitLocation.Infantry.Torso.Upper` | `BHHitValidationWorldSubsystem` |
| Ammo type | Standard (not AP/HP/Tracer) | Weapon mag content |

### Pipeline execution

```
baseDamage = <caliber-specific base damage for 5.45mm>  // from DT lookup
          
Step 1 — Attachments shouldn't modify damage directly (GEs modify
         weapon attributes like recoil, not projectile damage;
         projectile damage comes from caliber + weapon stat).
         
Step 2 — Infantry damage modifier chain:
  AmmoTypeEffectiveness(standard, 5.45mm) → ?        (needs DT_InfantryData_AmmoTypeEffectivenessPen table)
  ArchetypeCaliberModifiers(AR, 5.45mm)  → 1.00×     (table says AR with 5.45 = 1.00)
  BoneDamageModifiers(Torso.Upper)       → 1.10×     (table says Torso.Upper = 1.10)
  VehicleSeatDamageReduction             → 1.0× skip (target not in vehicle)
  PlayerArmorDurability                  → depends on armor state

Step 3 — Multiplicative stack:
  finalDamage = baseDamage × 1.00 × 1.10 × (armor reduction) × ammoEff
  ≈ baseDamage × 1.10 × (armor factor)

Step 4 — Apply:
  UBHGameplayEffectComponent::SetAttributeBaseValue(
    Attribute = Health.Current,
    newbase = base - finalDamage
  )
  
Step 5 — Replicate:
  AttributeReplication container pushes new value to clients
  
Step 6 — If new base <= 0:
  Grant tag Player.State.Downed
  Apply GE_PlayerDowned_C
  Trigger GameplayCue.Combat.PlayerDown (VFX/audio)
```

### Open gaps still blocking a full numeric answer

1. **Base damage per caliber** — the caliber → base damage table
   lookup is not fully extracted yet. Likely in a caliber-specific
   DataAsset.
2. **Modifier evaluation order** — §7.1 of both pipeline docs.
   Needed to confirm `×` order matches the stated multiplicative stack.
3. **PlayerArmorDurability behaviour** — the 5th C++ modifier.
   Reduces damage based on armor state; exact formula requires IDA RE.
4. **AmmoTypeEffectivenessPen table** — ammo type modifier for standard
   ammo not yet enumerated in this doc.

Resolution of these gaps lives in:
- Triage AI's `DAMAGE_IDA_TRACE.md` (not yet committed) — targets §7.1
- Future EXPORT re-dump — targets gap 1
- Future SDK pass 2 — targets gap 3
- Immediate: can read `DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json` for gap 4

## Example — rocket to tank

### Inputs

| Input | Value | Source |
|---|---|---|
| Weapon | AT-launcher firing 125mm rocket | Weapon stat |
| Damage source tags | `Meta.Damage.Explosive.Rocket.125mm`, `Meta.Damage.Explosive.Radius.Inner` | Projectile config |
| Target | TNK_01 (tank), full health | Game state |
| Hit location | Front-plate armor section | Section resolution |

### Pipeline execution

```
baseDamage = <125mm rocket base damage>

Step 1 — Vehicle damage rule lookup:
  Load DT_GlobalDamage_VehicleData_TNK_01, row Meta.Damage.Vehicle.<Tank Model>
  
Step 2 — Filter 66 rules by Source + Target + HitLocation:
  Matches on Source: "Explosive.Rocket.125mm"
  Matches on Source: "Explosive.Radius.Inner" (if inner hit)
  Matches on HitLocation: front-plate section tag
  
Step 3 — Each matched rule applies Percentage_Ongoing mod:
  Example matches:
    Rule 18: Explosive.Rocket.125mm (base 125mm handling) → +150%
    (If more rules match, stack multiplicatively)
    
  Final mod stack: baseDamage × 2.5

Step 4 — Vehicle section routing:
  Front-plate section PreDamageRouting:
    Partial damage to engine section if front-plate is depleted
    (configured via FVehicleHealthSection.PreDamageRouting map)
    
Step 5 — Apply damage to section:
  front_plate.CurrentHealth -= finalDamage
  
Step 6 — If section destroyed:
  PostDamageRouting applies overflow to connected sections
  Dispatch FMVehicleSectionDestroyedMessage
```

## Cross-section quick reference

| Question | See |
|---|---|
| What are the 5 damage modifiers? | [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) §2 |
| What's the actual bone multiplier value for a specific hit location? | [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) §4.1 |
| What's the damage profile for ROT_02 Havoc? | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) §4 |
| How many vehicles have per-class damage rules? | [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) §3 — 22 total |
| What's the GAS attribute system? | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §4 — `TMap<FGameplayTag, float>` not `UAttributeSet` |
| How many GE_* effect classes ship? | [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md) §2 — 338 total |
| What are the units on `InitialBulletSpeed`? | [`UNITS.md`](UNITS.md) §1 — cm/s |
| Where is `CT_Weapon_Spread` defined? | [`CROSS_REFERENCE.md`](CROSS_REFERENCE.md) `CT_*` section |

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — First integration view. Covers end-to-end from fire event through damage pipelines to attribute application. Two worked examples: AK74M → infantry torso, 125mm rocket → tank front-plate. Remaining 4 blocking gaps catalogued for next-pass resolution. |
