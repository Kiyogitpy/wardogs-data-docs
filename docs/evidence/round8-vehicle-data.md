# Round-8 vehicle data checks

Offline export and viewer-data check for the rotor hubs and STN_06 partial
attachment flag. This closes serialized-data questions only; it does not infer
native defaults or runtime behavior from an omitted export field.

## Rotor hubs, blades, and sections

**Native follow-up:** [group registration and health toggling](round8-rotor-toggle.md)
now establish the association left open by this serialized-data pass.

All three rotary platforms explicitly put the hub/base mesh and the blade mesh
in their rotor destructible group. In each platform export, follow
`UObject / MVF_DestructibleMeshes_0.Properties.DestructibleMeshesData`:

| Asset | Group | Entry | mesh | complex surface registration |
|---|---|---|---|---|
| [`VP_ROT_02.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Platforms/VP_ROT_02.json) | `[0]` Main | `[0]` `...Rotor.Main.Base` | `SM_ROT_02_Main_Rotor_Hub` | true, `ComplexSurface.Group.Default` |
| same | `[0]` Main | `[1]` `...Rotor.Main.Blades` | `SM_ROT_02_Main_Rotor_Blades` | true, `ComplexSurface.Group.Default` |
| same | `[1]` Tail | `[0]` `...Rotor.Tail.Base` | `SM_ROT_02_Rear_Rotor` | true, `ComplexSurface.Group.Default` |
| same | `[1]` Tail | `[1]` `...Rotor.Tail.Blades` | `SM_ROT_02_Rear_Rotor_Blades` | true, `ComplexSurface.Group.Default` |
| [`VP_ROT_03.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Platform/VP_ROT_03.json) | `[0]` Main | `[0]` Base; `[1]` Blades | `SM_ROT_03_MainRotor`; `SM_ROT_03_MainRotorBlades` | both true, Default |
| same | `[1]` Tail | `[0]` Base; `[1]` Blades | `SM_ROT_03_RearRotor`; `SM_ROT_03_RearRotor_Blades` | both true, Default |
| [`VP_ROT_04.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Platforms/VP_ROT_04.json) | `[0]` Main | `[2]` Base; `[0]` Blades | `SM_ROT_04_MainRotor`; `SM_ROT_04_RotorBlades` | both true, Default |
| same | `[1]` Tail | `[2]` Base; `[0]` Blades | `SM_ROT_04_RearRotor_`; `SM_ROT_04_RearRotor_Blades` | both true, Default |

Each `MeshTag` is under the stated `DestructibleMeshGroupTag` (`Vehicle.DestructibleMesh.Rotor.Main` or `.Tail`). Hub/base entries use `MVCT_QueryProxy`; blade entries use `WDRotorCollision`. The `*.Spin` entries are separate: `SM_RotorSpeedmesh`, `bRegisterComplexSurface: false`, `SurfaceGroup: None`, and `NoCollision`. Do not describe those spin meshes as blades.

The collision viewer models corroborate the part distinction by mesh names:
`air-rotary-havoc.glb` has `CC_ROT_02_Main_Rotor` and
`CC_ROT_02_Main_Rotor_Blades` (likewise rear rotor and rear blades);
`air-rotary-littlebird.glb` has `CC_ROT_03_MainRotor` and
`CC_ROT_03_RotorBlades` (likewise rear); `air-rotary-rot-04.glb` has
`CC_ROT_04_MainRotor` and `CC_ROT_04_RotorBlades` (likewise rear). These are
viewer mesh names; the hit slot is the collision mesh material slot, as
described in [Vehicle Damage Pipeline §3.2](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md#32-from-a-hit-triangle-to-a-section).
The generated [`vehicle-hitboxes.json`](../../assets/data/vehicle-hitboxes.json)
maps `CC_MainRotor` in `ComplexSurface.Group.Default` to
`Attribute.Gameplay.Health.Rotor.Main` (400), and `CC_TailRotor` in Default to
`Attribute.Gameplay.Health.Rotor.Tail` (300), for Havoc, Little Bird, and ROT_04.
Together with the collision-mesh slot evidence already documented in Vehicle
Damage Pipeline §3.1, the hub and blade entries share the same section mapping.

This closes serialized destructible-group membership and Default surface
registration for hub and blade meshes. It does **not** establish whether the
runtime damage-model group's hide/collision toggle associates a hub with a
health section; keep that native association as an open question if that is
what “hub group membership” means. The exports also use no `AttachQuery` for
these rotor entries. For ordinary attachment records, the serialized key is
`AttachQuery.SourceId` (capital I, lower-case d), not `SourceID`; for example
the STN_06 turret export below. Do not infer a rotor parent from a casing
variant or from a render-model slot.

## STN_06 partial attachment

**Follow-up resolved the static default:** the native constructor explicitly
sets the flag false, and the stationary chain/platform have no override.
See [the constructor trace](round8-stn06-attachments.md). The discussion below
records the earlier serialization/gate boundary; it is not a remaining
default-value blocker. Later runtime mutation remains untraced.

No `bEnablePartialAttachments` field appears in the exported STN_06 vehicle
data tree ([`data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06)). In
[`VP_STN_06_Turret.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Parts/VP_STN_06_Turret.json),
the skeletal component export `UObject / MVF_SkeletalMesh_0.Properties.ComponentSettings`
has `AttachQuery: {SourceId: "Chassis", SocketName: "S_GunMount"}` and tag
`TurretSkeleton`; the gun-proxy static mesh export
`UObject / MVF_StaticMesh_3.Properties.ComponentSettings.AttachQuery` asks
for `{SourceId: "TurretSkeleton", SocketName: "receiver_J"}`. The adjacent
`Properties.StaticMesh.AssetPathName` is
`/MWSY_001/Meshes/ComplexCollisions/ComplexProxy/Browning_Gun_Proxy.Browning_Gun_Proxy`.
This is explicit serialized attachment data; it does not serialize the
vehicle-level allow-partial flag.

Absence of the property proves only that the export does not override or
serialize it. It does **not** prove the effective value is false (or true):
class defaults, inherited defaults, and constructor code remain unverified.
The owner and native gate are resolved below; the remaining next step is to
obtain the inherited native default or constructor write. Until then, retain the existing conditional wording: the proxy
attaches at the skeleton origin only if partial attachments are enabled;
actual STN_06 attachment remains unknown.

### Native owner and attachment gate follow-up

The SDK resolves the property owner and inheritance chain. In
`sdk/raw/ModularVehicles_structs.hpp`,
`FModularVehicleAttachManager::bEnablePartialAttachments` is at struct offset
`0x08`. `sdk/raw/ModularVehicles_classes.hpp`
places `AModularVehicle::AttachManager` at `0x4A8`. The native class path is
`AWDStationaryVehicle : AMStationaryVehicle : ABHBaseVehiclePawn :
AModularVehicle` (`WDGame_classes.hpp`, `Mechanized_classes.hpp`); the STN_06
platform's `ImplementationClass` is `/Script/WDGame.WDStationaryVehicle`.
Thus the owner is the inherited `AModularVehicle` attach-manager struct, not a
platform fragment field.

The corpus body for `0x50EF920` reads the option at `a3 + 8`. It obtains an
attachment result from `0x50EBDE0`, then accepts result `2` (full attach) in
either mode; when the flag is enabled it also accepts result `1` (partial
match). SDK `EModularVehicleAttachState` names these values `Attached = 2`
and `Detached = 1`. The accepting branch calls `0x50E5F30`; rejected results
clear the output state. This separates the missing `receiver_J` match from
the option: the absent bone yields a partial result, while the flag decides
whether that partial result is accepted. It does not establish whether the
STN_06 instance's flag is enabled.

The reviewed SDK declaration does not encode a default initializer, and the
platform export names a native class rather than a vehicle Blueprint whose
CDO could provide a serialized override. The allowed corpus lookup provides
the checker's body, but did not identify a constructor/default write for this
field. Therefore the effective STN_06 value remains unresolved. Close it only
by inspecting the native `AModularVehicle`/`AWDStationaryVehicle` class
default or constructor initialization in the restored executable (including
any inherited/default override); specifically verify the byte at
`AttachManager + 0x08` before `0x50EF920` reads it. A generic zero-initialization
assumption is not evidence.

## Suggested handoff edits

- Replace the broad rotor “hub group membership” open item with the closed
  serialized result above, while retaining the narrower native hide/collision
  association as unresolved.
- Keep STN_06's flag and attachment runtime value open; say the export omits
  the field and avoid equating omission with the class default.
- Keep viewer part labels distinct for hub/base, blades, and spin meshes.
