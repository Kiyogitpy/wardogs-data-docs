---
title: Round 8 weapon-owner import scan
nav_exclude: true
---

# Blueprint `IWDWeaponOwner` implementers: IoStore import scan

## Result

The full local CL516586 cooked-package scan found **no Blueprint class whose
`UClass.Interfaces` array directly names `/Script/WDGame.WDWeaponOwner`**.
This is a bounded negative result; it does not identify a concrete implementer
or close the carryover by claiming universal absence.

## Method and coverage

A task-local CUE4Parse probe mounted the installed Wardogs IoStore content with
the repository's `5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.export.usmap`.
It enumerated all `.uasset` and `.umap` entries and loaded each package. For every
`IoPackage`, it resolved `ImportMap` entries using CUE4Parse's global script
object metadata, matched the resulting path against
`/Script/WDGame.WDWeaponOwner`, then checked each exported `UClass.Interfaces`
entry in every matching package against that exact path. It also counted
resolved references to `/Script/WDGame.WDAncillaryAttachedWeaponData`.

Coverage was 107,181 package entries loaded, all 107,181 as `IoPackage`; 2,596,068
import slots and 1,230,571 script-import slots were scanned. All 1,230,571 script
imports resolved to paths. There were zero package-load or parse failures.
Fifteen packages referenced `WDWeaponOwner`; their fifteen exported classes
were `BlueprintGeneratedClass` objects, and all fifteen had an empty
`Interfaces` array. None was a direct implementer. One package referenced
`WDAncillaryAttachedWeaponData`; it was the grenade launcher data asset and had
no class export to inspect.

The 15 `WDWeaponOwner` importers are eight audio behaviors, three weapon action
Blueprints, two weapon gameplay cues, and projectile Blueprints
`BP_120x800mm` and `BP_155mm_Expensive`. Their imports establish interface use
in those assets, not interface implementation.

## Boundary

This resolves the limitation of the earlier `findname Wardogs WDWeaponOwner`
search: that search only checked local package name maps, whereas this scan
resolved IoStore script imports through global metadata. The scan is exhaustive
for package imports and direct `UClass.Interfaces` references in the mounted
cooked package set. It does not prove that no implementer exists outside this
installed build, nor cover indirect native implementation, runtime-generated
classes, or an implementation encoded in a form that does not place the
interface in a Blueprint class's `Interfaces` array. Keep the
`Blueprint IWDWeaponOwner implementers` carryover open pending a concrete
implementation path or broader evidence.

Raw package-scan output and the probe source/build are outside the repository
under `E:/Reverse_Engineer/wardogs_analysis/round8_weaponowner_importscan_20261019/`.
No raw Blueprint dumps or AES key contents are included here.

## Inheritance audit of the two known native owners

A second task-local probe enumerated the export maps of all 107,181 cooked
packages and selected exports whose class path contains
`BlueprintGeneratedClass`. It inspected 3,866 such Blueprint-generated class
exports and followed each decoded `UStruct.SuperStruct` chain through Blueprint
parents, looking for the two known native owners from the weapon-context trace:
`/Script/WDGame.WDItemExtension_RangedWeapon` and
`/Script/WDGame.WDVehicleWeaponExtension`. **No Blueprint-generated class chain
reached either owner** (0 ranged-extension descendants, 0 vehicle-extension
descendants). There were zero package or class parse failures. Accordingly,
there were no descendant `Interfaces` arrays or getter `FuncMap` entries to
report; counts for those checks are zero by absence of descendants. This audit
is limited to descendants of these two named native classes; it does not
enumerate every possible native `IWDWeaponOwner` implementation.

The SDK's reflected comments for the interface functions show these flags:

| Interface function | SDK flags |
|---|---|
| `GetWeaponTag` | `Native, Public, BlueprintCallable, BlueprintPure, Const` |
| `GetDamageEntityComponent` | `Native, Public, BlueprintCallable, BlueprintPure, Const` |
| `GetProjectileData` | `Native, Public, HasOutParams, BlueprintCallable` |

None of the three comments lists `BlueprintEvent`. The flags establish that
these functions are exposed as Blueprint-callable functions; the SDK evidence
does not identify them as Blueprint-overridable events. The generated SDK
wrappers dispatch through `ProcessEvent`, which by itself does not establish
Blueprint override capability. This reduces the likelihood that the missing
Blueprint subclasses of the two native owners hide the implementation path,
but does not establish that all native interface implementations have been
found. The reflected flag comments are in
[`WDGame_functions.cpp`](../../sdk/raw/WDGame_functions.cpp) at the
`WDWeaponOwner.GetWeaponTag`, `GetDamageEntityComponent`, and `GetProjectileData`
wrappers.

The inheritance probe and its output are outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_weaponowner_importscan_20261019/inheritance/`.

## Third native owner and metadata positive control

The inheritance scan was extended to the native class `AWDMountedWeapon`
(SDK name `WDMountedWeapon`). It still inspected all 3,866
`BlueprintGeneratedClass` exports from the 107,181 loaded packages. No class
chain reached any of the three named native owners:
`UWDItemExtension_RangedWeapon`, `AWDVehicleWeaponExtension`, or
`AWDMountedWeapon`. Counts are 0 descendants for each, 0 relevant getter
`FuncMap` entries, 0 direct `WDWeaponOwner` interfaces among descendants, and 0
package/class parse failures. This remains scoped to those named native owners.

A fresh typed CUE4Parse load of
`Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget` provides a positive
control for the `UClass.Interfaces` parser: its exported
`B_MovingTarget_C` class resolves the superclass
`/Script/WDGame.WDMovingTarget` and one interface,
`/Script/WDGame.WDDamageable`, with `bImplementedByK2=true`. The decoded array
is therefore populated for a cooked Blueprint class under this mapping and
probe setup; the earlier empty arrays are not explained by a parser that
always returns empty interfaces.

### Bounded native registration inventory

The native registration evidence was checked against the generated class and
interface names in `sdk/raw/WDGame_classes.hpp` and against the executable's
read-only registration data. Each listed class getter RVA matches the class
function pointer at the start of its `FClassParams` record. At `FClassParams
+0x30`, the interface-array pointer resolves to a `.data` record whose first
`FImplementedInterfaceParams` tuple is the `WDWeaponOwner` getter pointer
`0x6C2B390`, followed by the interface pointer offset and `bImplementedByK2`:

| Native class | Class getter RVA | `FClassParams` RVA | Interface-array field RVA | `.data` tuple RVA | Interface offset | K2 |
|---|---:|---:|---:|---:|---:|---|
| `UWDItemExtension_RangedWeapon` | `0x6C8E430` | `0xB3868F0` | `0xB386920` | `0xCEC1518` | `0xF0` | false |
| `AWDVehicleWeaponExtension` | `0x76423A0` | `0xB63DF40` | `0xB63DF70` | `0xCEE5CD8` | `0x2B8` | false |
| `AWDMountedWeapon` (`WDMountedWeapon`) | `0x76D1E40` | `0xB673C00` | `0xB673C30` | `0xCEEADE8` | `0x2B8` | false |

The tuple byte layout is an 8-byte class getter pointer, a 32-bit offset at
`+8`, and the K2 boolean at `+12`, padded to a 16-byte element stride. This
matches the `FImplementedInterfaceParams` field ordering in UE's
`UObjectGlobals.h` registration definition (the cited source lines are
4143–4170). The SDK supplies the reflected names: its `IWDWeaponOwner`
`StaticClass` uses `WDWeaponOwner`, and the three class declarations use
`WDItemExtension_RangedWeapon`, `WDVehicleWeaponExtension`, and
`WDMountedWeapon` through `STATIC_CLASS_IMPL`.

For a bounded cross-check, aligned QWORD positions in readable, nonwritable,
nonexecutable sections of the restored executable were scanned for the three
`.data` interface-array VAs. The scan covered `.rdata`, `.pdata`, `.rodata`,
`_RDATA`, `.rsrc`, and `.reloc`; each VA had exactly one match, at its listed
`FClassParams +0x30` field. This validates those three table references only.
It does not claim all computed references or every native implementation in
the binary were enumerated.

The third-owner scan, positive control, and pointer verification scripts and
outputs are outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_weaponowner_importscan_20261019/`.

The typed package probe also shows that `BP_120x800mm_C` directly inherits
`/Script/WDGame.WDCameraProjectile`, not `WDMountedWeapon`; the same is true of
`BP_155mm_Expensive_C`. This accounts for why those projectile Blueprints do
not appear among the three audited native-owner descendants.
