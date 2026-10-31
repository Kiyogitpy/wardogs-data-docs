---
title: Round 17 Blueprint class defaults
nav_exclude: true
---

# Round 17 Blueprint class defaults

A cooked Blueprint stores only the values that differ from its parent. To settle open numbers on the Medical, Fire and Utility, Explosives, Item Actions and Buildables pages, round 17 exported the relevant Blueprint classes and montages with the offline extractor and resolved each value up the chain. The result is [`assets/data/bp-defaults.json`](../../assets/data/bp-defaults.json) (281 entries, values only), written by [`_tools/bp_defaults.py`](../../_tools/bp_defaults.py). The native constructor half of the chain is on [round 17 native constructor defaults](round17-native-defaults.md).

## Method

1. List and dump packages with `tools/cue4parse_extractor` (`list`, then `dump <files.txt>`), reading the game's own paks. Nothing was run or contacted. The dumps (174 packages, grouped below) stay outside the repository.
2. For each wanted value, read the class default object (`Default__X_C`) or the item instance export. If the property is absent, follow the Blueprint parent (`Super` of the generated class) until a Blueprint sets it. Item instances fall back to the class Blueprint behind them (for example [`ID_AT_Mine`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/AT_mine/Content/Data/ID_AT_Mine.json) to `BH_AT_MineExtensionData`).
3. If no Blueprint sets it, there are two cases. A variable the Blueprint declares itself (listed in its `ChildProperties`) takes its type default (0, false, empty). A property that belongs to a native class takes the constructor default from `assets/data/native-defaults.json`, joined by class and SDK offset.
4. Montage values (length, notify times, section starts) are read from the cooked `AnimMontage` exports. A missing `RateScale` is the engine default 1.0.
5. Blueprint bytecode was listed with `tools/cue4parse_extractor/kismet_listing.py` to check how each value is used (for example how the appliable base action turns an animation into a use time).

Each JSON entry has: `topic` (page), `asset`, `class` (the export read), `property`, `value`, `unit`, `resolved_from`, `from_asset` (where it was found), `native_class` and `sdk_offset` when a native class owns the property, `native_default` and `native_ctor_rva` for that native value, `package` and a short `note`.

## What was dumped

| Group | Packages |
|---|---|
| Actions and the appliable base | `B_Action_Appliable_Base`, `B_Action_Bandage_Use`, `B_Action_MedKit_*`, `B_Action_Enox_Use`, `B_Action_StimPen`, `B_Action_Defibrillator`, `B_Action_Resuscitator`, `B_Action_Revive`, `B_Action_RequestRevive`, `B_Action_ThrowExplosive`, `B_Action_PlaceItem`, build-tool actions |
| Items and extension data | `BH_Defibrillator_WattsExtensionData`/`Component`, `BH_AT_MineExtensionData`, `BH_ClaymoreExtensionData`, `BH_C4_Data`, the `ID_` definitions of the defibrillator, mines, C4, IED, Molotov, smoke, Medical Bag and the three hammers |
| Actors | `B_FragGrenade`, `B_GoldFragGrenade`, `B_Molotov` (+ fire field, trigger volume), `B_SmokeGrenade_*`, `B_WorldSmokeGrenade_*`, `BP_SmokeGrenadeVFX`, `PDA_SmokeGrenade`, `DA_SmokeGrenade_*`, `B_AT_Mine`, `B_Claymore`, `B_ThrowableC4`, `B_ThrowableIED`, `B_PlaceableIED`, `GE_MolotovBurning` |
| Player | `B_WDMoverPlayerCharacter`, `B_WDCore_MoverPlayerCharacter` (the player data asset [`WDCore_PlayerData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WDCore/Content/Character/WDCore_PlayerData.json) names the second as the pawn class), `B_WDPlayerVitalityState_Critical` |
| Montages | 12 medical, 8 throw, 8 place and trigger, 3 hammer use montages, plus equip and holster montages that are not used in the JSON |

## Counts

| Resolved from | Entries |
|---|---:|
| `export` (set on the named asset) | 192 |
| `parent` (set on a parent Blueprint or the class behind an item) | 25 |
| `bp-default` (Blueprint variable never set: type default) | 4 |
| `engine-default` (montage `RateScale` 1.0) | 41 |
| `native` (native constructor default joined from `native-defaults.json`) | 19 |
| `native-pending` (no Blueprint and not in `native-defaults.json`) | 0 |
| **Total** | **281** |

By page: medical 56, fire and utility 69, explosives 13, item actions 116, buildables 27 (the item-actions topic repeats the medical and throw montages so that page's generator reads one topic).

## What was settled

| Page | Settled (Data (Blueprint CDO) unless noted) |
|---|---|
| Medical | Montage seconds for every `AnimationLength` use (bandage 5.23 / 4.83 s, kit 5.23 s with `Heal` at 4.73 s, Enox 2.17, Stim Pen 2 / 1.27, Medical Bag 7.4, resuscitator 2.17, defibrillator 9.15, base revive 20.5). Defibrillator `ChargeDuration` 4 s, `BatteryChargesUsed` 25, revive health 35. Player bleed-out: base 360 s (native 300), minimum 30 s (60), `HoldOnBleedOutRate` 0.5 (0.1), `GiveUpBleedOutRate` 240 (6.0), penalty offset 100 (15), critical revive hold 20 (2), `MaxDecayHealth` 40 (0). Base revive hold time 20 s. Resuscitator container time 44 s (Derived from the base action formula). |
| Fire and utility | `ArmingDelay` 1.0, `TraceCheckTime` 0.1, `DetectFriendlyVehicles` true, `PerVehicleSpeedListDetection` empty, `ActivationDelayTimer` 2.0, `ShouldDetectVehicle` true, `DetectFriendlyTeammates` true, C4 `DelayTillExplosion` 0.0, charge `TimerBeforeExplosion` 0.2. Smoke fuse 3.0 s, post-explode life 10 s, world actor life 175 s, smoke asset defaults (180 s total, fade 20 / 10, sprite 800). Molotov patch fields (count 15 against native 12, offset scale 1.5 against 0.5, copied value 100 against 40, fire field 2000 against 250). |
| Explosives | Fuse table: frag 4.0 s (cookable, throw-back), smoke 3.0 s, Molotov 5.0 s (native, not overridden), C4 0.2 s / 0.0 s, IED 3.0 s, AT mine 1.0 s arming, Claymore 2.0 s activation. |
| Item actions | Use, throw and place montage seconds with notify and loop-section times (frag, smoke and Molotov throw, C4 throw, mine, Claymore and IED placement). |
| Buildables | Hammer `BuildAmount` per hit (1.5, 1.0, 0.5), critical-spot amount (8, 5, 3), swing montage lengths (1.43, 1.67, 1.27 s), `Hit` notify and loop sections. |

## What remains native-pending or not traced

Native-pending: none after round 18. The four items left open in round 17 were resolved in round 18 and joined from `native-defaults.json` (the effect is a class default object, but a Blueprint class takes its defaults from the native parent constructor). Evidence is the static-analysis image of the restored exe, which is decompiled, not devirtualized; decompilation is not equivalence proof.

| Asset | Property | Native class | SDK offset | Value | Constructor / store |
|---|---|---|---|---|---|
| `GE_MolotovBurning` | `Duration` | `UBHGameplayEffect` | `+0x30` | 0.0 | `0x5225C65` / `0x5225C82` |
| `GE_MolotovBurning` | `MaxStacks` | `UBHGameplayEffect` | `+0x34` | 1 | `0x5225C65` / `0x5225C74` |
| `GE_MolotovBurning` | `StackDurationRefreshPolicy` | `UBHGameplayEffect` | `+0x36` | 0 (`RefreshOnSuccessfulApplication`) | `0x5225C65` / `0x5225C74` |
| `GE_MolotovBurning` | `StackExpirationPolicy` (also added) | `UBHGameplayEffect` | `+0x37` | 1 (`RemoveSingleStackAndRefreshDuration`) | `0x5225C65` / `0x5225C74` |
| `B_Molotov` | `bCanBeCooked` | `AWDGrenade` | `+0x624` | false | `0x6CADC90` / `0x6CADCBB` (Molotov chain: `0x86A0200` calls `0x6CADED0`, store `0x6CADEEE`) |

Round 20 resolution (static-analysis image; virtualized dispatch not removed; pages read are byte-identical to the reference image and hold no dispatch stub): `Duration` 0.0 means no timed expiry. The duration pass `0x522D260` tests `Duration` against zero at `0x522D4B3` and, when equal, jumps to `0x522D700`, skipping the end-time comparison (`0x522D4DC`) and the removal call (`0x522D6F1`). The burning tag is removed with the effect when the actor leaves the patch: `B_Molotov_TriggerVolume` (`EffectsToApply` = `GE_MolotovBurning` x1) inherits the native enter handler `0x76FBE80` (vtable slot 237) that applies the effect and stores its handle, and the exit handler `0x76FC120` (slot 238) that removes the tag container and every stored handle (`0x52355F0`). `GE_MolotovBurning` has no removal or ongoing requirements. Open: the end-overlap wiring and tag release on removal were not traced, and overlapping patches with `MaxStacks` 1 (shared versus separate handle) are not decoded. See [Fire and utility, section 2.3](../../game-features/Wardogs_FireAndUtility_v1.md).

Not traced (logic, not defaults):

- What ends a resuscitator revive and the health it passes; the base revive health; the native use of `CriticalReviveHoldThreshold` and `BleedOutRevivePenaltyOffset`.
- How a hammer `BuildAmount` scales against the 0 to 1 stage progress (the Large and Medium hammers come out about equal by loop length, against the shop text).
- Which player Blueprint a given game mode spawns: the numbers above are for `B_WDCore_MoverPlayerCharacter` (named by the WDCore player data) and its parent `B_WDMoverPlayerCharacter`. A mode that spawns another pawn class was not checked.
- Throw timing on release: the montage holds in a loop section and the `Throw` notify sits at the loop end; how the game leaves the loop is not traced.

## Reproduce

```
WdExtract <Paks> <keyfile> <usmap> <dumpdir> <Paks>\oo2core_9_win64.dll dump <files.txt>
python _tools/bp_defaults.py --dump <dumpdir>
python _tools/bp_defaults.py --check
```

If the dump folder is absent `bp_defaults.py` leaves the committed JSON in place, and the page generators (`medical_tables.py`, `utility_throwable_tables.py`, `explosive_tables.py`, `action_tables.py`, `buildable_tables.py`) read that JSON.
