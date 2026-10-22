---
title: Round 17 native constructor defaults
nav_exclude: true
---

# Round 17 native constructor defaults

Cooked Blueprints store only values that differ from their parent. When nothing overrides a property, the value is the native C++ constructor default. This page lists 176 such defaults (171 from round 17, 5 added in round 18) read from the constructors in the restored executable (CL-516586, image base `0x140000000`). All addresses are RVAs. Source: [`assets/data/native-defaults.json`](../../assets/data/native-defaults.json). Verifier: `python _tools/native_defaults_check.py` re-disassembles all 18 constructors and asserts every value.

## Method

1. Find the class vtable alias in the decompile corpus (`<Class>_VFT`), then the function that loads it with `lea` near its start: that is the constructor.
2. Disassemble the constructor and replay every store of an immediate (or a constant loaded from `.rdata`) into a byte map keyed by `[reg+disp]`. Qword and dword stores are split into bytes, so one `mov [rdi+0x2e4], 0x101` sets two adjacent bools.
3. Name each offset from the SDK dump (`CppSDK/SDK`). Many property names in this build are obfuscated (`_aaab...`); they are kept as they appear and flagged `obfuscated` in the JSON.

Labels: **Native** means read from the constructor store; **Derived** means a role inferred from how code uses the field. Values are single-precision floats unless the type says otherwise. Zero rows are real stores (the constructor sets 0 explicitly), not omissions.

## Mines and explosives

**Native.** `AWDLandmine` (ctor `0x6CAF780`) and `AWDC4` (ctor `0x6CA6A80`) are thin subclasses: their constructors store only `FGameplayTag` pairs at `+0x480`, `+0x488` and `+0x4B8` (the tag values are FNames, not decoded here) and no numeric defaults. Their numeric defaults come from the shared base `AWDExplosive` (ctor `0x6CA7800`), so C4 and the landmine inherit `StartingHealth` 50, `bExplodeOnHealthDepleted` true and `PostExplodeLifespan` 2 s unless a Blueprint overrides them. `AWDGrenade` (ctor `0x6CADC90`) confirms the round 16 fuse: `BaseFuseTime` 5.0 s at `+0x620`. The placeable `AWDLandminePlaceable` (ctor `0x7721230`) sets `bExplodeOnDamageTaken` true with a threshold of 50.

The mine and C4 tunables named on the pages (`ArmingDelay`, `TraceCheckTime`, `DetectFriendlyVehicles`, `PerVehicleSpeedListDetection`, `ActivationDelayTimer`, `DelayTillExplosion`, `MaxDetonationDistance`) are not fields of the native actors. The SDK declares them on `BH_AT_MineExtensionData`, `BH_ClaymoreExtensionData` and `BH_C4_Data` (offsets `+0x70`, `+0x50`, `+0x58`, `+0x60`, `+0x50`, `+0x48`, `+0x50`), and the corpus has no vtable alias for those classes, so there is no native constructor to read. Treat them as Blueprint/data-side values from the Blueprint export.

24 values.

| Class | Property | Offset | Type | Value | Ctor RVA | Store RVA |
|---|---|---|---|---|---|---|
| `AWDExplosive` | `ThrowInfo.ThrownServerTime` | `0x318` | float | -1 | `0x6ca7800` | `0x6ca78d5` |
| `AWDExplosive` | `ThrowInfo.InitialLocation.Z` | `0x330` | double | 0 | `0x6ca7800` | `0x6ca78f5` |
| `AWDExplosive` | `ExplosionInfo.ExplodeServerTime` | `0x340` | float | -1 | `0x6ca7800` | `0x6ca7903` |
| `AWDExplosive` | `ExplosionCueTimeoutTolerance` | `0x490` | float | 2 | `0x6ca7800` | `0x6ca79b7` |
| `AWDExplosive` | `CollisionExplodeImpactThreshold` | `0x498` | float | 0 | `0x6ca7800` | `0x6ca79c8` |
| `AWDExplosive` | `_aaabjgmikeipcelkioaip` | `0x4a0` | float | 0.25 | `0x6ca7800` | `0x6ca79d5` |
| `AWDExplosive` | `CollisionEffectImpactThreshold` | `0x4a4` | float | 3000 | `0x6ca7800` | `0x6ca79df` |
| `AWDExplosive` | `CollisionEffectMinTime` | `0x4a8` | float | 0.25 | `0x6ca7800` | `0x6ca79e9` |
| `AWDExplosive` | `PostExplodeLifespan` | `0x4b4` | float | 2 | `0x6ca7800` | `0x6ca7a04` |
| `AWDExplosive` | `bExplodeOnHealthDepleted` | `0x4e8` | bool | true | `0x6ca7800` | `0x6ca7a63` |
| `AWDExplosive` | `StartingHealth` | `0x4ec` | float | 50 | `0x6ca7800` | `0x6ca7a6a` |
| `AWDExplosive` | `ImpactDamage` | `0x550` | float | 10 | `0x6ca7800` | `0x6ca7ac4` |
| `AWDExplosive` | `AdditionalGravity` | `0x554` | float | 0 | `0x6ca7800` | `0x6ca7ac4` |
| `AWDExplosive` | `_aaabkmlienndgffldjaln` | `0x558` | float | 0.3 | `0x6ca7800` | `0x6ca7ad1` |
| `AWDGrenade` | `BaseFuseTime` | `0x620` | float | 5 | `0x6cadc90` | `0x6cadcb1` |
| `AWDGrenade` | `InteractionRange` | `0x634` | float | 250 | `0x6cadc90` | `0x6cadd38` |
| `AWDGrenade` | `InteractionAngle` | `0x638` | float | 60 | `0x6cadc90` | `0x6cadd42` |
| `AWDGrenade` | `InteractionHoldTime` | `0x63c` | float | 0.25 | `0x6cadc90` | `0x6cadd4c` |
| `AWDGrenade` | `GrenadeInteractionData.MaximumVelocity` | `0x640` | float | 250 | `0x6cadc90` | `0x6cadd6b` |
| `AWDGrenade` | `GrenadeInteractionData.MinimumLifetime` | `0x644` | float | 0.5 | `0x6cadc90` | `0x6cadd75` |
| `AWDGrenade` | `GrenadeInteractionData.SphereRadius` | `0x648` | float | 25 | `0x6cadc90` | `0x6cadd7f` |
| `AWDGrenade` | `GrenadeInteractionData.MinimumRemainingFuseTime` | `0x64c` | float | 0 | `0x6cadc90` | `0x6cadd7f` |
| `AWDLandminePlaceable` | `bExplodeOnDamageTaken` | `0x3a0` | bool | true | `0x7721230` | `0x77212df` |
| `AWDLandminePlaceable` | `DamageToExplodeThreshold` | `0x3a4` | float | 50 | `0x7721230` | `0x77212e6` |

## Smoke

**Native.** `AWDSmokeGrenade` (ctor `0x869BF50`) stores only a class pointer at `+0x660`; it adds no numeric defaults on top of `AWDGrenade` and `AWDExplosive` (fuse 5.0 s). Total duration and fade-in/fade-out come from `GetEffectiveSmokeTimings` (`0x869F010`), which is not a constructor default and is not traced here. What the constructors do fix:

- `AWDSmokeGrenadeVFXActor` (ctor `0x869C200`): the volume probe. Sphere trace radius 65, wall-hit offset 100, trace channel value 10, and two rings of rays. Ring 1 is 8 directions, 45 degree step, pitch 0, length 350. Ring 2 is 5 directions, 72 degree step, pitch 30, length 250. One float in each ring and the first `Params` fields have obfuscated SDK names, so they are shown by offset.
- `AWDSmokeTrailBlockerActor` (ctor `0x76A18F0`): `EffectDuration` 12.0 s, `SmokeSize` 750, and a `Params_0` block (`RadiusMultiplier` 0.6, `HeightOffset` 100, plus obfuscated fields).
- `AWDSmokeGrenadeAfterEffect` (ctor `0x869BFF0`): one float at `+0x2C8` set to -1.0 (a "not set" sentinel; role not traced).

38 values.

| Class | Property | Offset | Type | Value | Ctor RVA | Store RVA |
|---|---|---|---|---|---|---|
| `AWDSmokeGrenadeAfterEffect` | `_aaabgaoiibmakefeaoimc` | `0x2c8` | float | -1 | `0x869bff0` | `0x869c046` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae.SphereTraceRadius` | `0x2b8` | float | 65 | `0x869c200` | `0x869c239` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae.WallHitPosOffset` | `0x2bc` | float | 100 | `0x869c200` | `0x869c246` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaajfghfbinpidcccnaj` | `0x2c0` | float | 100 | `0x869c200` | `0x869c252` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae.TraceChannel` | `0x2c4` | ETraceTypeQuery | 10 | `0x869c200` | `0x869c22a` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae.bTraceComplex` | `0x2c5` | bool | false | `0x869c200` | `0x869c22a` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaakibhllghlgajlclfo.NumDirections` | `0x2c8` | int32 | 8 | `0x869c200` | `0x869c25c` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaakibhllghlgajlclfo._aaaaopihhflchnnnclokn` | `0x2cc` | float | 45 | `0x869c200` | `0x869c266` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaakibhllghlgajlclfo.PitchDegrees` | `0x2d0` | float | 0 | `0x869c200` | `0x869c266` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaakibhllghlgajlclfo.TraceLength` | `0x2d4` | float | 350 | `0x869c200` | `0x869c271` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaaklmahpdkhlndpcpkn.NumDirections` | `0x2d8` | int32 | 5 | `0x869c200` | `0x869c27b` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaaklmahpdkhlndpcpkn._aaaaopihhflchnnnclokn` | `0x2dc` | float | 72 | `0x869c200` | `0x869c285` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaaklmahpdkhlndpcpkn.PitchDegrees` | `0x2e0` | float | 30 | `0x869c200` | `0x869c28f` |
| `AWDSmokeGrenadeVFXActor` | `_aaabbkfdmfgfcphbmjfae._aaaaklmahpdkhlndpcpkn.TraceLength` | `0x2e4` | float | 250 | `0x869c200` | `0x869c299` |
| `AWDSmokeGrenadeVFXActor` | `SmokeVolume.Origin.Z` | `0x308` | double | 0 | `0x869c200` | `0x869c2f1` |
| `AWDSmokeGrenadeVFXActor` | `SmokeVolume._aaaapbknepbgjjpjmkdke` | `0x348` | float | 0 | `0x869c200` | `0x869c33c` |
| `AWDSmokeGrenadeVFXActor` | `_aaabcookbnlcfbbdpjapl` | `0x36c` | float | 0 | `0x869c200` | `0x869c367` |
| `AWDSmokeTrailBlockerActor` | `EffectDuration` | `0x2c0` | float | 12 | `0x76a18f0` | `0x76a190f` |
| `AWDSmokeTrailBlockerActor` | `_aaaanfpicenfgehmdpjgl` | `0x2c4` | float | 3.25 | `0x76a18f0` | `0x76a192a` |
| `AWDSmokeTrailBlockerActor` | `SmokeSize` | `0x2c8` | float | 750 | `0x76a18f0` | `0x76a1939` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaaaobmnhlnpmneknamcc` | `0x2cc` | float | 200 | `0x76a18f0` | `0x76a19a1` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabbbofjmidcfjegfleb` | `0x2d0` | float | 1 | `0x76a18f0` | `0x76a19ab` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabcjelaegdfkknollno` | `0x2d4` | float | 0.25 | `0x76a18f0` | `0x76a19b5` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabffpbbdkgpcglioemj` | `0x2d8` | float | 1 | `0x76a18f0` | `0x76a19bf` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabiigpgmhdjbnnaokld` | `0x2dc` | int32 | 48 | `0x76a18f0` | `0x76a19c9` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabbeagpcmlfbghcodjg` | `0x2e0` | int32 | 8 | `0x76a18f0` | `0x76a19d3` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabjbanakpiffhjlfahk` | `0x2e4` | bool | true | `0x76a18f0` | `0x76a194c` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabhjfimokddkeffkgid` | `0x2e5` | bool | true | `0x76a18f0` | `0x76a194c` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabdhcbhjdbcpllgefjc` | `0x2e8` | float | 0.5 | `0x76a18f0` | `0x76a19dd` |
| `AWDSmokeTrailBlockerActor` | `Params_0.RadiusMultiplier` | `0x2ec` | float | 0.6 | `0x76a18f0` | `0x76a19e7` |
| `AWDSmokeTrailBlockerActor` | `Params_0.RadiusOffset` | `0x2f0` | float | 0 | `0x76a18f0` | `0x76a19e7` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabfmefncepmlajldogd` | `0x2f4` | float | 225 | `0x76a18f0` | `0x76a19f2` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabjocpbnmnioepinlcp` | `0x2f8` | float | 1 | `0x76a18f0` | `0x76a19fc` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabbnnienfhdbobdggci` | `0x2fc` | bool | true | `0x76a18f0` | `0x76a1a06` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabdchljhaidbobddmnp` | `0x300` | float | 1.45 | `0x76a18f0` | `0x76a1a0d` |
| `AWDSmokeTrailBlockerActor` | `Params_0._aaabbdcpehbpkdlgginge` | `0x304` | float | 0 | `0x76a18f0` | `0x76a1a0d` |
| `AWDSmokeTrailBlockerActor` | `Params_0.LongitudinalOffset` | `0x308` | float | 0 | `0x76a18f0` | `0x76a1963` |
| `AWDSmokeTrailBlockerActor` | `Params_0.HeightOffset` | `0x30c` | float | 100 | `0x76a18f0` | `0x76a1a18` |

## Health, vitality and medical

**Native.** Bleed-out, revive hold and camera defaults live in `AWDMoverCharacter` (ctor `0x6E67160`). Health, decay and regen defaults live in `UWDVitalityComponent` (`0x6B81720`), `UWDCharacterVitalityComponent` (`0x6B16790`) and `UWDHealthRegenComponent` (`0x848B5F0`). Key values: `BaseBleedOutTime` 300 s, `MinBleedOutTime` 60 s, `BleedOutRevivePenaltyOffset` 15 s, bleed-out rates 1.0 default / 0.1 hold-on / 6.0 give-up, `DamagedBleedOutChange` 0.1, `DefaultHealthToReviveTo` 25, `MaxDecayHealth` 0, `DecayRate` 5, `DecayMagnitude` 5, `RegenDelay` 10 s, base and max health 100. `MaxDecayHealth` 0 and `MaxOverhealHealth` 0 mean decay and overheal stay off unless a Blueprint or Gameplay Effect sets them. `UWDHealthRegenComponent` regenerates 5 health per 1.0 s tick (`HealthToRegenerate`, `TickInterval`). `UWDReviveInteractionContext` stores 10.0 at `+0x240` (obfuscated name; plausibly a revive duration but not confirmed).

There is no defibrillator or resuscitator class: no such class exists in the SDK and the corpus has no such vtable alias.

40 values.

| Class | Property | Offset | Type | Value | Ctor RVA | Store RVA |
|---|---|---|---|---|---|---|
| `AWDMoverCharacter` | `bInfiniteAmmo` | `0x800` | bool | false | `0x6e67160` | `0x6e67429` |
| `AWDMoverCharacter` | `bInfiniteBuildingSupplies` | `0x801` | bool | false | `0x6e67160` | `0x6e67429` |
| `AWDMoverCharacter` | `bInstantBuildingMode` | `0x802` | bool | false | `0x6e67160` | `0x6e67429` |
| `AWDMoverCharacter` | `bInvincible` | `0x803` | bool | false | `0x6e67160` | `0x6e67429` |
| `AWDMoverCharacter` | `CurrentOutOfBoundsTime` | `0x830` | float | 0 | `0x6e67160` | `0x6e67437` |
| `AWDMoverCharacter` | `TargetData.bIsActive` | `0x860` | bool | true | `0x6e67160` | `0x6e6740c` |
| `AWDMoverCharacter` | `CloseAnimationDistance` | `0x868` | float | 0 | `0x6e67160` | `0x6e6743e` |
| `AWDMoverCharacter` | `CloseAnimationTickOption` | `0x86c` | EVisibilityBasedAnimTickOption | 1 | `0x6e67160` | `0x6e67445` |
| `AWDMoverCharacter` | `DefaultAnimationTickOption` | `0x86d` | EVisibilityBasedAnimTickOption | 4 | `0x6e67160` | `0x6e67445` |
| `AWDMoverCharacter` | `LowHealthStateLimit` | `0x8c0` | float | 0.25 | `0x6e67160` | `0x6e67481` |
| `AWDMoverCharacter` | `bAddDefaultPlayerInteractionContexts` | `0x8c4` | bool | true | `0x6e67160` | `0x6e6748c` |
| `AWDMoverCharacter` | `MaxSightDistance` | `0x8c8` | float | 200 | `0x6e67160` | `0x6e67494` |
| `AWDMoverCharacter` | `MaxEjectDistance` | `0x8cc` | float | 400 | `0x6e67160` | `0x6e6749f` |
| `AWDMoverCharacter` | `InteractionHoldTime` | `0x8d0` | float | 0.3 | `0x6e67160` | `0x6e674aa` |
| `AWDMoverCharacter` | `CriticalReviveHoldThreshold` | `0x970` | float | 2 | `0x6e67160` | `0x6e674ba` |
| `AWDMoverCharacter` | `HealHoldThreshold` | `0x974` | float | 5 | `0x6e67160` | `0x6e674c5` |
| `AWDMoverCharacter` | `BaseBleedOutTime` | `0x980` | float | 300 | `0x6e67160` | `0x6e674fa` |
| `AWDMoverCharacter` | `MinBleedOutTime` | `0x984` | float | 60 | `0x6e67160` | `0x6e67505` |
| `AWDMoverCharacter` | `BleedOutRevivePenaltyOffset` | `0x988` | float | 15 | `0x6e67160` | `0x6e67510` |
| `AWDMoverCharacter` | `DefaultBleedOutRate` | `0x98c` | float | 1 | `0x6e67160` | `0x6e6751b` |
| `AWDMoverCharacter` | `HoldOnBleedOutRate` | `0x990` | float | 0.1 | `0x6e67160` | `0x6e67526` |
| `AWDMoverCharacter` | `GiveUpBleedOutRate` | `0x994` | float | 6 | `0x6e67160` | `0x6e67531` |
| `AWDMoverCharacter` | `DamagedBleedOutChange` | `0x998` | float | 0.1 | `0x6e67160` | `0x6e6753c` |
| `AWDMoverCharacter` | `DamageEventAckWindow` | `0x9c0` | float | 1.5 | `0x6e67160` | `0x6e67547` |
| `AWDMoverCharacter` | `CriticalCameraHeight` | `0x9c4` | float | 20 | `0x6e67160` | `0x6e67552` |
| `AWDMoverCharacter` | `CriticalCameraHeightTransitionTime` | `0x9c8` | float | 0.2 | `0x6e67160` | `0x6e6755d` |
| `AWDMoverCharacter` | `CriticalYawCameraClampAngle` | `0x9cc` | float | 45 | `0x6e67160` | `0x6e67568` |
| `AWDMoverCharacter` | `OutOfBoundsTimeLimit` | `0x9d8` | float | 10 | `0x6e67160` | `0x6e67588` |
| `UWDCharacterVitalityComponent` | `DefaultHealthToReviveTo` | `0x160` | float | 25 | `0x6b16790` | `0x6b167ad` |
| `UWDCharacterVitalityComponent` | `MaxOverhealHealth` | `0x164` | float | 0 | `0x6b16790` | `0x6b167ad` |
| `UWDCharacterVitalityComponent` | `MaxDecayHealth` | `0x168` | float | 0 | `0x6b16790` | `0x6b167e1` |
| `UWDCharacterVitalityComponent` | `DecayRate` | `0x16c` | float | 5 | `0x6b16790` | `0x6b167f5` |
| `UWDCharacterVitalityComponent` | `DecayMagnitude` | `0x170` | float | 5 | `0x6b16790` | `0x6b167ff` |
| `UWDVitalityComponent` | `BaseHealth` | `0x130` | float | 100 | `0x6b81720` | `0x6b81743` |
| `UWDVitalityComponent` | `MaxHealth` | `0x134` | float | 100 | `0x6b81720` | `0x6b8174d` |
| `UWDVitalityComponent` | `RegenDelay` | `0x138` | float | 10 | `0x6b81720` | `0x6b817c1` |
| `UWDHealthRegenComponent` | `HealthToRegenerate` | `0xe8` | float | 5 | `0x848b5f0` | `0x848b64a` |
| `UWDHealthRegenComponent` | `TickInterval` | `0xec` | float | 1 | `0x848b5f0` | `0x848b656` |
| `UWDHealthRegenComponent` | `DelayTimer` | `0xf0` | uint8 | 0 | `0x848b5f0` | `0x848b663` |
| `UWDReviveInteractionContext` | `_aaabaegphpphphhikihho` | `0x240` | float | 10 | `0x772c5f0` | `0x772c606` |

## Fire (Molotov)

**Native.** `AWDMolotovGrenade` (ctor `0x86A0200`) holds six fields at `+0x670..+0x684` that the patch spawner `0x86A15B0` reads. The SDK names are obfuscated, so the roles below are **Derived** from how that function uses them: `+0x670` (250) and `+0x674` (0.5) scale the offset of each patch from the impact point, `+0x678` (12) is the patch count, `+0x680` (0.3) scales a reduced count (`count*2*0.3` and its square root both appear), `+0x684` (40) is copied into each spawned patch, and `+0x67C` (25) is not yet matched to a use. `AWDMolotovFireField` (ctor `0x86A0140`) and `AWDMolotovTriggerVolume` (ctor `0x86A0300`) add 250, 600, 150, 4 and 100 at the offsets below; their roles are not traced.

12 values.

| Class | Property | Offset | Type | Value | Ctor RVA | Store RVA |
|---|---|---|---|---|---|---|
| `AWDMolotovGrenade` | `_aaaamejojopeijafgdjkf` | `0x670` | float | 250 | `0x86a0200` | `0x86a021a` |
| `AWDMolotovGrenade` | `_aaaakffacidhmniagfchm` | `0x674` | float | 0.5 | `0x86a0200` | `0x86a0284` |
| `AWDMolotovGrenade` | `_aaaakmpdngpdcdjfoghgn` | `0x678` | int32 | 12 | `0x86a0200` | `0x86a028e` |
| `AWDMolotovGrenade` | `_aaabefnnihkojobdfojbk` | `0x67c` | float | 25 | `0x86a0200` | `0x86a0298` |
| `AWDMolotovGrenade` | `_aaaamiahcncilelhidghh` | `0x680` | float | 0.3 | `0x86a0200` | `0x86a02a2` |
| `AWDMolotovGrenade` | `_aaabclpkjcpbbjcpncgfa` | `0x684` | float | 40 | `0x86a0200` | `0x86a02ac` |
| `AWDMolotovFireField` | `_aaaalampbnfacakccbbcd` | `0x2d0` | float | 250 | `0x86a0140` | `0x86a0164` |
| `AWDMolotovFireField` | `_aaabdgioabebpkhhmcglm` | `0x2d4` | float | 600 | `0x86a0140` | `0x86a01d3` |
| `AWDMolotovFireField` | `_aaabknhhcfikfkdfeephh` | `0x2d8` | float | 150 | `0x86a0140` | `0x86a01dd` |
| `AWDMolotovFireField` | `_aaabakopnbgagdbajfflp` | `0x2dc` | int32 | 4 | `0x86a0140` | `0x86a01e7` |
| `AWDMolotovFireField` | `_aaaanpgemjngemejijhnd` | `0x310` | float | 0 | `0x86a0140` | `0x86a01b2` |

**Round 18 additions (Molotov-related).** Static-analysis image of the restored exe; decompilation is not equivalence proof and virtualized dispatch is not removed.

| Class | Field | Offset | Type | Value | Ctor | Store |
|---|---|---|---|---|---|---|
| `AWDGrenade` | `bCanBeCooked` | `0x624` | bool | false | `0x6cadc90` | `0x6cadcbb` |
| `UBHGameplayEffect` | `Duration` | `0x30` | float | 0 | `0x5225c65` | `0x5225c82` |
| `UBHGameplayEffect` | `MaxStacks` | `0x34` | uint16 | 1 | `0x5225c65` | `0x5225c74` |
| `UBHGameplayEffect` | `StackDurationRefreshPolicy` | `0x36` | uint8 | 0 (`RefreshOnSuccessfulApplication`) | `0x5225c65` | `0x5225c74` |
| `UBHGameplayEffect` | `StackExpirationPolicy` | `0x37` | uint8 | 1 (`RemoveSingleStackAndRefreshDuration`) | `0x5225c65` | `0x5225c74` |

The Molotov constructor `0x86a0200` calls the grenade base `0x6caded0`, which stores the same zero for `bCanBeCooked` at `0x6cadeee`. The `UBHGameplayEffect` constructor stores `0x220` as `0x101` (both client-prediction flags true) and ends at `+0x268`, matching the 0x270-byte class. What `Duration` 0.0 means at run time (the duration pass `0x522d260` compares it with zero at `0x522d4b3`) is inferred and open.
| `AWDMolotovTriggerVolume` | `_aaaajgnjpicpffeijmmnj` | `0x998` | float | 100 | `0x86a0300` | `0x86a031d` |

## Buildables

**Native.** Build progress per use comes from `UWDItemExtensionData_BuildBuildable` (ctor `0x85E7410`): `BuildAmount` 3.0 per hit and `BuildAmountPerSecond` 3.0, with a 200 construct trace distance. `UWDBuildableDataAsset` (ctor `0x8585020`) gives the data-asset defaults (`MaxHealth` 4000, `RepairSpeedMultiplier` 1.0, `Cost` and `PlacementCost` 1, placement geometry). `UWDBuildableComponent` (ctor `0x8584CC0`) sets `DefaultBuildingProgress` 1.0, `DestroyDelay` 0.5 and `ClearSupportDelayTime` 0.1. `UWDBuildableSettings` (ctor `0x8577F60`) sets `FirstPlacementDuration` 2.0 and `MaxUpTeleportDistance` 400. Blueprint data assets usually override most of these, so treat them as fallbacks.

57 values.

| Class | Property | Offset | Type | Value | Ctor RVA | Store RVA |
|---|---|---|---|---|---|---|
| `UWDBuildableComponent` | `bFirstPlacement` | `0x138` | bool | true | `0x8584cc0` | `0x8584d79` |
| `UWDBuildableComponent` | `DestroyDelay` | `0x13c` | float | 0.5 | `0x8584cc0` | `0x8584d87` |
| `UWDBuildableComponent` | `ClearSupportDelayTime` | `0x140` | float | 0.1 | `0x8584cc0` | `0x8584d93` |
| `UWDBuildableComponent` | `BuildingProgress.Value` | `0x144` | float | 0 | `0x8584cc0` | `0x8584d93` |
| `UWDBuildableComponent` | `DefaultBuildingProgress` | `0x150` | float | 1 | `0x8584cc0` | `0x8584dac` |
| `UWDBuildableComponent` | `CurrentSupportHeight` | `0x1e0` | float | 1000 | `0x8584cc0` | `0x8584e6c` |
| `UWDBuildableSettings` | `bDisabledStateBlocksSuppliesUsageForPlacement` | `0x40` | bool | false | `0x8577f60` | `0x8577f89` |
| `UWDBuildableSettings` | `bDisabledStateBlocksSuppliesUsageForConstruction` | `0x41` | bool | true | `0x8577f60` | `0x8577f89` |
| `UWDBuildableSettings` | `bDamagedDisabledStatePreventsSuppliesDeposition` | `0x42` | bool | false | `0x8577f60` | `0x8577f89` |
| `UWDBuildableSettings` | `bDisabledStateConsumesFuel` | `0x43` | bool | true | `0x8577f60` | `0x8577f89` |
| `UWDBuildableSettings` | `FirstPlacementDuration` | `0x70` | float | 2 | `0x8577f60` | `0x8577fd9` |
| `UWDBuildableSettings` | `PlayerBuildProgressPenetrationBuffer` | `0x74` | float | 34 | `0x8577f60` | `0x8577fe0` |
| `UWDBuildableSettings` | `bUseObstructedDetection` | `0x78` | bool | true | `0x8577f60` | `0x8577fe7` |
| `UWDBuildableSettings` | `bUseUpTeleport` | `0x79` | bool | true | `0x8577f60` | `0x8577fe7` |
| `UWDBuildableSettings` | `MaxUpTeleportDistance` | `0x7c` | float | 400 | `0x8577f60` | `0x8577fed` |
| `UWDItemExtensionData_BuildBuildable` | `Applicationtype` | `0x48` | EWDBuildApplicationType | 0 | `0x85e7410` | `0x85e7432` |
| `UWDItemExtensionData_BuildBuildable` | `BuildAmount` | `0x4c` | float | 3 | `0x85e7410` | `0x85e743a` |
| `UWDItemExtensionData_BuildBuildable` | `BuildAmountPerSecond` | `0x50` | float | 3 | `0x85e7410` | `0x85e744d` |
| `UWDItemExtensionData_BuildBuildable` | `MaxConstructTraceDistance` | `0xc8` | float | 200 | `0x85e7410` | `0x85e74f7` |
| `UWDBuildableDataAsset` | `PlacementCost` | `0x58` | int32 | 1 | `0x8585020` | `0x8585062` |
| `UWDBuildableDataAsset` | `Cost` | `0x5c` | int32 | 1 | `0x8585020` | `0x8585069` |
| `UWDBuildableDataAsset` | `_aaabkhhnlcojdebfcnjfd` | `0x60` | float | 1 | `0x8585020` | `0x8585070` |
| `UWDBuildableDataAsset` | `RepairSpeedMultiplier` | `0x64` | float | 1 | `0x8585020` | `0x8585077` |
| `UWDBuildableDataAsset` | `MaxHealth` | `0x78` | float | 4000 | `0x8585020` | `0x858508a` |
| `UWDBuildableDataAsset` | `StackCheckOffset` | `0x108` | float | 10 | `0x8585020` | `0x858509a` |
| `UWDBuildableDataAsset` | `MaxStack` | `0x10c` | int32 | 2 | `0x8585020` | `0x85850ab` |
| `UWDBuildableDataAsset` | `_aaabhmbpigcbckbdmafaf` | `0x110` | uint8 | 1 | `0x8585020` | `0x85850b7` |
| `UWDBuildableDataAsset` | `SnapHalfSize` | `0x128` | float | 300 | `0x8585020` | `0x85850cc` |
| `UWDBuildableDataAsset` | `PlacementFlags` | `0x12c` | uint8 | 11 | `0x8585020` | `0x85850d6` |
| `UWDBuildableDataAsset` | `PlacePivotVerticalOffset` | `0x170` | float | 100 | `0x8585020` | `0x8585115` |
| `UWDBuildableDataAsset` | `PlacePivotHorizontalOffset` | `0x174` | float | 0 | `0x8585020` | `0x8585115` |
| `UWDBuildableDataAsset` | `StartingPlacementRotationAngle` | `0x178` | float | 0 | `0x8585020` | `0x8585120` |
| `UWDBuildableDataAsset` | `PlacementBlockedPenetrationBuffer` | `0x17c` | float | 10 | `0x8585020` | `0x8585126` |
| `UWDBuildableDataAsset` | `SnappedPlacementBlockedPenetrationBuffer` | `0x180` | float | 15 | `0x8585020` | `0x8585130` |
| `UWDBuildableDataAsset` | `_aaabpjmmnkdmnfmiclcod` | `0x184` | float | 30 | `0x8585020` | `0x858513a` |
| `UWDBuildableDataAsset` | `bRequiresAllCornersOnSurface` | `0x188` | bool | true | `0x8585020` | `0x8585144` |
| `UWDBuildableDataAsset` | `bRotateWithSurface` | `0x189` | bool | false | `0x8585020` | `0x8585144` |
| `UWDBuildableDataAsset` | `_aaabmchoencnofdnabjpj` | `0x18c` | float | 30 | `0x8585020` | `0x8585154` |
| `UWDBuildableDataAsset` | `_aaacbdaennkckmjooalil` | `0x190` | float | 50 | `0x8585020` | `0x858515e` |
| `UWDBuildableDataAsset` | `bCanBuildFoundation` | `0x194` | bool | true | `0x8585020` | `0x8585168` |
| `UWDBuildableDataAsset` | `_aaabdoigdcdnmgpllilhf` | `0x1c0` | bool | true | `0x8585020` | `0x85851a6` |
| `UWDBuildableDataAsset` | `MaximumFoundationHeight` | `0x1c4` | float | 200 | `0x8585020` | `0x85851b4` |
| `UWDBuildableDataAsset` | `ServerSurfaceHitResultLeeway` | `0x1c8` | float | 5 | `0x8585020` | `0x85851c0` |
| `UWDBuildableDataAsset` | `FoundationBlockedPenetrationBuffer` | `0x1cc` | float | 20 | `0x8585020` | `0x85851ca` |
| `UWDBuildableDataAsset` | `_aaabmdkefddajcadddajd` | `0x1d0` | float | 80 | `0x8585020` | `0x85851d4` |
| `UWDBuildableDataAsset` | `MaximumValidSurfaceAngle` | `0x1d4` | float | 45 | `0x8585020` | `0x85851de` |
| `UWDBuildableDataAsset` | `bCheckAllCornersSurfaceAngle` | `0x1d8` | bool | true | `0x8585020` | `0x85851e8` |
| `UWDBuildableDataAsset` | `bShowFOBExtents` | `0x1d9` | bool | true | `0x8585020` | `0x85851e8` |
| `UWDBuildableDataAsset` | `SurfaceTraceOffset` | `0x1dc` | float | 5 | `0x8585020` | `0x85851f1` |
| `UWDBuildableDataAsset` | `_aaabbinolbehnojbpindb` | `0x1e0` | float | 500 | `0x8585020` | `0x85851fb` |
| `UWDBuildableDataAsset` | `MaxDepthUnderTerrain` | `0x1e4` | float | 20 | `0x8585020` | `0x8585205` |
| `UWDBuildableDataAsset` | `_aaabgadadjidpmcenmdfk` | `0x1ec` | float | 100 | `0x8585020` | `0x8585216` |
| `UWDBuildableDataAsset` | `BuildFinishedCollisionPenetrationDepthBuffer` | `0x294` | float | 25 | `0x8585020` | `0x85852c8` |
| `UWDBuildableDataAsset` | `MaterialDamageTintCPD` | `0x298` | int32 | 6 | `0x8585020` | `0x85852d5` |
| `UWDBuildableDataAsset` | `bRegisterWithFOB` | `0x310` | bool | false | `0x8585020` | `0x8585377` |
| `UWDBuildableDataAsset` | `bUsesCriticalHitSpots` | `0x311` | bool | true | `0x8585020` | `0x8585377` |
| `UWDBuildableDataAsset` | `_aaabcndcdhncpejmlldmi.Z` | `0x370` | double | 0 | `0x8585020` | `0x8585404` |

## Movement

**Not traced.** The stance modifier lambda at `0x5288D80` named in the brief is not a lambda body. That address sits in a run of virtual-call thunks (`mov rcx,[rcx]; mov rax,[rcx]; jmp [rax+0x470]`, then `+0x480`, `+0x4A0`, `+0x490`) just after `sub_145288CB0` (`0x5288CB0..0x5288D13`), and the corpus has no function starting there. The per-stance multipliers still need another route, for example the ground movement data decoded in round 14.

## Still untraced

- Mine, claymore and C4 tunables (`ArmingDelay`, `TraceCheckTime`, vehicle detection, `ActivationDelayTimer`, `DelayTillExplosion`, `MaxDetonationDistance`): Blueprint/data-side classes with no native constructor. They belong to the Blueprint export.
- Smoke total duration and fade times: produced by `GetEffectiveSmokeTimings` (`0x869F010`), not a constructor store.
- Roles of the obfuscated fields (Molotov patch fields, fire field, trigger volume, smoke trail params, revive `+0x240`) beyond the notes above.
- Interaction durations for heal and revive (`InteractionDuration` in `UWDWorldInteractionContextBase`) and the `FWDPlayerInteractionData` struct: base-class constructors were not read.
- Defibrillator and resuscitator: no native class exists.
- Only straight-line constructor stores are modelled. Values written by helper code called from a constructor are not captured. A field with no store is absent from the table, not zero.
- The movement stance lambda (above).
