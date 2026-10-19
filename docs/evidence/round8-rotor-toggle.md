---
title: Round 8 rotor destructible-group toggle
nav_exclude: true
---

# Round-8 rotor destructible-group toggle

Static CL 516586 trace against `WardogsClient-Win64-Shipping.restored.exe`
(SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`)
and the three cooked platform exports. RVA values below are relative to the
image base `0x140000000`. This resolves the native group-membership question
left open in [the vehicle data check](round8-vehicle-data.md#rotor-hubs-blades-and-sections).

**Result.** The main and tail rotor hub/base components are members of their
respective destructible groups in the native component, alongside the blades.
The group's destroyed/visible selector acts on every registered member, so
both hub and blades are hidden and have collision disabled when their rotor
health group is destroyed. Main and tail are independent selectors. The
`.Spin` mesh is also listed in each group, but its cooked collision profile is
`NoCollision` and it is not a registered complex surface; it is not a blade or
a separate damage hit surface.

The group identity is a destructible mesh tag, **not** the collision surface
group. The cooked [ROT_02](../../data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Platforms/VP_ROT_02.json),
[ROT_03](../../data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Platform/VP_ROT_03.json), and
[ROT_04](../../data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Platforms/VP_ROT_04.json)
each give the Main group `Vehicle.DestructibleMesh.Rotor.Main` with Base,
Blades, and Spin mesh tags, and the Tail group the matching `.Tail` tags.
Each group's `AttributeUpdateRule` selects its matching
`Attribute.Gameplay.Health.Rotor.Main` or `.Tail` and sets
`RepairThreshold: 0.5` (ROT_02 lines 1099–1102 and 1891–1894;
ROT_03 lines 1092–1095 and 1898–1901; ROT_04 lines 1030–1033 and
1830–1833). [The vehicle data check](round8-vehicle-data.md#rotor-hubs-blades-and-sections)
records the individual mesh/profile and hit-section entries.

Native linkage:

1. `UMVF_DestructibleMeshes` setup at `0x539A5F0` iterates the fragment's
   groups (40-byte records) and their mesh entries (16-byte records). It copies
   each member's mesh tag and collision settings into a 112-byte
   `FBHMeshGroupReplicatedMeshData` entry, then passes the assembled group
   array to `0x5322520`. That function copies the 48-byte
   `FBHMeshGroupEntry` records into the destructible-mesh component's
   `DestructibleMeshGroups` at `+0x110`. Thus the cooked hub and blade entries
   survive as native group members, rather than merely sharing an export
   nesting level. Layouts match
   [Mechanized_structs.hpp](../../sdk/raw/Mechanized_structs.hpp#L972).
2. The attribute-update callback at `0x76A36B0` finds that exact group tag
   through `0x532D180` (machine code `0x532D180–0x532D1B0` scans the
   `+0x110` array). When selected health reaches `<= 0`, it calls
   `0x533B4C0(component, groupTag, true)`. On a later positive/rising
   update, a destroyed group is cleared only when current health reaches
   `0x532DCB0(damageModel, rule.AttributeTag) * rule.RepairThreshold`.
   `0x533B4C0` writes the group's `bIsDestroyed` byte at entry `+0x28`, marks
   replication dirty, and processes group rules via `0x5334F80`. The rule
   fields match [WDGame_structs.hpp](../../sdk/raw/WDGame_structs.hpp#L13445).
3. The destroyed-visibility binding at `0x53C1490` finds the same group tag
   (`0x53C14E2` calls `0x532D180`) and computes initial visibility as
   `!group.bIsDestroyed && !vehicle.bIsVehicleDestroyed`
   (`0x53C14F4–0x53C1505`). It calls `0x532B8B0` with that group tag and
   a callback thunk at `0x53C5830`, which jumps to `0x53BC420`.
   `0x532B8B0` walks **every** 112-byte member in the matching 48-byte group,
   resolves each `MeshTag` through the component's `TagToMesh` map, and invokes
   the callback for each resolved mesh. It does not filter for `.Blades` or
   exclude `.Base`.
4. Per member, `0x53BC420` writes visibility through `0x3D861E0`. In the
   hidden branch it calls the mesh component's collision-enabled virtual
   method (`vtable +0x780`) with zero (`NoCollision`). In the visible branch
   `0x532D120` retrieves that member's saved collision data by **group tag
   and mesh tag** (`0x532D120–0x532D17A`); `0x50E5C00` applies its stored
   collision profile. The hub therefore returns to its own query-proxy
   profile, while a blade returns to `WDRotorCollision`; showing a group does
   not assign the blade profile to its hub.

This proves the static selector and initial/bound callback path, including hub
membership. It does not assert that every possible gameplay event will execute
the rule at runtime, nor does it require the hub to carry a separate health
attribute. The attribute-to-group rule controls the group; the hit surface
mapping to health sections is a distinct part of the damage pipeline.
