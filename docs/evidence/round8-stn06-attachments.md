---
title: Round 8 STN_06 partial attachment default
nav_exclude: true
---

# STN_06 partial attachment default

Static CL-516586 finding, 2026-10-18. The native default of
`bEnablePartialAttachments` for STN_06 is **false**. The installed game's
shipping executable reports `++Wardogs+Live-CL-516586`; the restored analysis
executable has SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
The function at `0x50E0110` is misfiled as `nullsub_1723` in the read-only
corpus, so the constructor bytes below were independently decoded from that
restored executable with Capstone. No game or service was run.

`sdk/raw/ModularVehicles_classes.hpp:67` places `AttachManager` at
`AModularVehicle + 0x4A8`; `sdk/raw/ModularVehicles_structs.hpp:257` places
`bEnablePartialAttachments` at struct `+0x08`, or vehicle `+0x4B0`.
`AModularVehicle` constructor `0x50E0110` passes `this + 0x4A8` to
`0x50E08C0` at instruction `0x50E01F2-0x50E0200`. That attach-manager
constructor starts with `xor eax,eax` at `0x50E08C0`, then
`mov byte ptr [rcx+8],al` at `0x50E08C5`. It explicitly initializes the flag
to zero. The outer constructor later writes the owner pointer at `0x50E02FF`;
it does not replace the flag.

The inheritance chain's constructors are `ABHBaseVehiclePawn` `0x53B86F0`
(calls `0x50E0110`), `AMStationaryVehicle` `0x53B9FF0` (calls
`0x53B86F0`), and `AWDStationaryVehicle` `0x76B8F20` (calls
`0x53B9FF0`). Bounded machine-instruction inspection of those three complete
constructor bodies found no direct store to `+0x4B0` or replacement of
`AttachManager` at `+0x4A8`.
[`VP_STN_06.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Platforms/VP_STN_06.json)
selects native `/Script/WDGame.WDStationaryVehicle` as its
`ImplementationClass`. The exported STN_06 content tree has no
`bEnablePartialAttachments` override. Thus its native class default retains
the false value established above.

The existing [attachment-gate trace](round8-vehicle-data.md#native-owner-and-attachment-gate-follow-up)
shows that `0x50EF920` accepts a full attachment either way, but accepts a
partial match only when this flag is enabled. For the documented gun proxy's
missing `receiver_J` source on `SK_Browning_Mounted`, the false default means
the partial-match fallback is not admitted by that gate. This is the default
and the stated static path; it does not rule out an untraced later mutation or
prove a live attachment result.
