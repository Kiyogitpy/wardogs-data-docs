# IDA claim exposure to the protection layer

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page lists which native-address citations in these docs sit on code pages that the executable's protection layer may have virtualized. **Classification means "the page contains a stub", not "the claim is wrong".** Nothing here has been retracted. Round 19 re-verified two stub-in-body functions (`0x6bb8970`, `0x6b8ac90`): both unaffected, supported by the reference image only (see rows). The page only says where a re-check would be most useful. Refreshed 2026-10-23 (round 24) for the round 23 citations: 2,965 cited addresses (was 2,527), 323 non-clean entries (was 252); the nine stub-bodied functions are listed below, and the newly listed rows are marked "not yet reverified".

## Method

Every `0x` token of at least `0x100000` in `docs/`, `pipelines/`, `content/` and `game-features/` (excluding this page) was collected with `_tools/ida_claim_exposure.py`, which reuses the extractor in `_tools/rva_status.py`. Each token was resolved to the decompilation-corpus function that contains it, and every 4 KiB code page that function spans was looked up in a page table built by comparing the static-analysis image with the older reference image. In that image 37,878 protected `.text` pages were recovered. Of these, 31,659 are byte-identical to the reference and 6,219 differ. Of the differing pages, 6,081 contain a differing indirect dispatch stub (a `mov reg,[rip+x]` followed by `jmp [reg+disp]` through the protection layer's global table), and 138 differ without a recognised stub; eleven of those 138 are separately captured pages. Full devirtualization has not been done, so a decompiled function on such a page may be incomplete. A citation takes the worst category among its function's pages (exceptional, then stub, then differs without stub, then clean). Tokens outside the protected pages are "unknown". Only the function's own pages are checked, so a clean function that calls into a stub is not flagged. Many tokens in the docs are data addresses or sizes rather than code, which is why "unknown" is large. A token with no corpus function row is classified by the page of the address alone.

## Counts

2965 distinct addresses, by the worst page category across the containing function:

| Category | Distinct addresses | Notes |
|---|---:|---|
| Clean | 2043 | every spanned page is byte-identical to the reference |
| Page with a dispatch stub | 585 | 256 functions plus 65 addresses with no function row; 9 functions contain a stub inside their own byte range |
| Differs, no stub recognised | 8 | 2 functions |
| Exceptional (the eleven separately captured pages) | 0 | no citation lands on those pages |
| Unknown | 329 | 271 outside `.text` (data addresses), 52 in a function that spans unprotected text pages, 6 with no function row on an unprotected page |

By the page of the cited address alone (ignoring the rest of its function): clean 2136, stub 495, differs 12, exceptional 0, unknown 322.

## Reading the table

A function listed below is not necessarily virtualized. The strongest signal is the column "Stub in body". `yes` means a dispatch stub instruction pair lies inside the function's own byte range, so that decompilation should be re-read first. `no` means only another part of a spanned page holds a stub. `-` means the address has no function row, so it is classified by its own page.

## Claims in non-clean pages

323 entries (256 stub functions, 65 stub addresses without a function row, 2 differs-without-stub functions), citing 593 addresses. Citation lists show at most four lines per file.

Round 24 refresh: 71 entries are new (56 functions and 15 addresses), none vanished. New functions: `0x1563050`, `0x15b8f80`, `0x165ed30`, `0x16706ee`, `0x1670b80`, `0x1670caf`, `0x16793db`, `0x3c95ab0`, `0x3c9b230`, `0x3c9b290`, `0x3c9b420`, `0x3cb6400`, `0x4232fd0`, `0x4416ff0`, `0x48aa82f`, `0x5225c60`, `0x5293150`, `0x675be60`, `0x675cdb0`, `0x675ceb0`, `0x69e8ff0`, `0x69e93df`, `0x6b54ae0`, `0x6b73500`, `0x6b73810`, `0x6b73940`, `0x6b73a60`, `0x6b73b30`, `0x6b73de0`, `0x6b74770`, `0x6b959e0`, `0x6b98f80`, `0x6b99160`, `0x6b99270`, `0x6b99300`, `0x6b99530`, `0x6b996d0`, `0x6bbab70`, `0x6bbb7d0`, `0x6c2a4e0`, `0x6c974e0`, `0x6c97710`, `0x6c97dd0`, `0x6c987a0`, `0x6c9fee0`, `0x6ca1660`, `0x6ca167f`, `0x6ca1fb0`, `0x6dae470`, `0x6f29130`, `0x6f342b0`, `0x6f344c5`, `0x6f34fe0`, `0x6f380a0`, `0x6f38360`, `0x76db350`; new addresses without a function row: `0x3cab0a0`, `0x42d9770`, `0x5296290`, `0x675ce10`, `0x6b86240`, `0x6b95630`, `0x6b956b0`, `0x6bbd3d0`, `0x6bbd420`, `0x6bbd500`, `0x6bbd5d0`, `0x6daeaa0`, `0x6e6e260`, `0x6e6ee40`, `0x6f78270`. Three of the new functions (`0x4232fd0`, `0x4416ff0`, `0x6b99300`) were already in the byte-level table below but were missing from this list.

| Function range or address | Category | Stub in body | Cited at |
|---|---|---|---|
| `0x395be30`–`0x395beb9` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `content/Wardogs_WeaponAttributes_v1.md` L80,84; `docs/evidence/round8-ancillary-sights.md` L211,274; `docs/evidence/round8-weapon-context.md` L157,165,167,360 |
| `0x5230be0`–`0x5230c39` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `docs/ROUND11_STATUS.md` L1183,1185 |
| `0x6b74e30`–`0x6b74f79` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `docs/evidence/round8-weapon-context.md` L31,35,362 |
| `0x6b8ac90`–`0x6b8acaf` | stub | yes (reverified r19: unaffected; whole body is the stub, original leaf in reference image matches `+0x41C` claim) | `content/Wardogs_Weapons_v2.md` L332,334; `docs/evidence/weapons.md` L43,138 |
| `0x6bb8970`–`0x6bb89a3` | stub | yes (reverified r19: unaffected; whole body is the stub, original lookup in reference image matches first-match-index / -1 claim) | `docs/ROUND11_STATUS.md` L980,988; `docs/evidence/damage.md` L546; `pipelines/Wardogs_DamagePipeline_v2.md` L81,470,475 |
| `0x1563050`–`0x1563053` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L338,582 |
| `0x157c320`–`0x157c468` | stub | no | `docs/evidence/round8-loadout-rebuy.md` L110 |
| `0x1587900`–`0x15879ea` | stub | no | `docs/evidence/damage.md` L259,496; `pipelines/Wardogs_DamagePipeline_v2.md` L1177 |
| `0x15b83b0`–`0x15b83b4` | stub | no | `docs/evidence/damage.md` L311,645,651 |
| `0x15b8f80`–`0x15b8f8d` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L112 |
| `0x15fecf0`–`0x15ff3aa` | stub | no | `docs/evidence/round8-propertybag-types.md` L25 |
| `0x165ed30`–`0x165ee07` | stub; not yet reverified | no | `pipelines/Wardogs_ProjectileFlight_v1.md` L342,541 |
| `0x16706ee`–`0x167089f` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L219 |
| `0x1670b80`–`0x1670cad` | stub; not yet reverified | yes | `pipelines/Wardogs_WeaponSpread_v1.md` L34,387 |
| `0x1670caf`–`0x1670d90` | stub; not yet reverified | no | `pipelines/Wardogs_ProjectileFlight_v1.md` L406 |
| `0x16793db`–`0x167949a` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L239,389 |
| `0x1812a60`–`0x1812a65` | stub | no | `docs/evidence/round8-backblast.md` L22 |
| `0x188c980`–`0x188ca5b` | stub | no | `docs/evidence/round8-radial-points-components.md` L84 |
| `0x18f0650`–`0x18f0658` | stub | no | `docs/evidence/round8-weapon-context.md` L25 |
| `0x19a4a50`–`0x19a4a59` | stub | no | `content/Wardogs_Weapons_v2.md` L338; `docs/evidence/weapons.md` L50,113 |
| `0x1c36300`–`0x1c36308` | stub | no | `docs/evidence/round8-backblast.md` L20; `docs/evidence/round8-weapon-context.md` L30 |
| `0x1cc7300`–`0x1cc7308` | stub | no | `docs/evidence/round8-loadout-restore.md` L41 |
| `0x1d2c340`–`0x1d2c348` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L202,217 |
| `0x21a6160`–`0x21a623e` | stub | no | `docs/evidence/round8-tapered-query.md` L30 |
| `0x21e1b20`–`0x21e1cc8` | stub | no | `docs/ROUND11_STATUS.md` L275 |
| `0x246f660`–`0x246f68e` | stub | no | `docs/ROUND11_STATUS.md` L833; `docs/evidence/round8-gepard-collision-inputs.md` L83,84 |
| `0x2470790`–`0x2470884` | stub | no | `docs/evidence/round8-tapered-query.md` L55 |
| `0x250b310`–`0x250b4cb` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L73 |
| `0x2835b24`–`0x2835d7f` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L21 |
| `0x2f691e0`–`0x2f691e8` | stub | no | `docs/evidence/round8-ancillary-sights.md` L202 |
| `0x3955370`–`0x39554ca` | stub | no | `docs/evidence/round8-radial.md` L133 |
| `0x395ade0`–`0x395b048` | stub | no | `docs/evidence/damage.md` L497,498; `pipelines/Wardogs_DamagePipeline_v2.md` L1178 |
| `0x3a39990`–`0x3a39a3e` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L19; `docs/evidence/round8-radial.md` L84 |
| `0x3a93090`–`0x3a932ff` | stub | no | `docs/evidence/damage.md` L320,499; `docs/evidence/round8-loadout.md` L397; `pipelines/Wardogs_DamagePipeline_v2.md` L1179 |
| `0x3a9b050`–`0x3a9b0da` | stub | no | `docs/evidence/weapons.md` L206,261 |
| `0x3c70f50`–`0x3c71154` | stub | no | `docs/ROUND11_STATUS.md` L489 |
| `0x3c95950`–`0x3c95aab` | stub | no | `docs/ROUND11_STATUS.md` L163,488 |
| `0x3c95ab0`–`0x3c95c23` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L267 |
| `0x3c9b230`–`0x3c9b28d` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L244 |
| `0x3c9b290`–`0x3c9b328` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L246 |
| `0x3c9b420`–`0x3c9b494` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L248 |
| `0x3ca21b0`–`0x3ca2230` | stub | no | `docs/evidence/round8-vehicle-sweep.md` L12,20 |
| `0x3ca2b40`–`0x3ca2dca` | stub | no | `docs/ROUND11_STATUS.md` L548 |
| `0x3ca8f70`–`0x3ca8fd0` | stub | no | `docs/evidence/round8-loadout-initialization.md` L40 |
| `0x3cab090`–`0x3cab098` | stub | no | `docs/evidence/round8-loadout-initialization.md` L23 |
| `0x3cab670`–`0x3cab6e9` | stub | no | `docs/ROUND11_STATUS.md` L159; `docs/evidence/round8-explosive-viewer-audit.md` L204; `docs/evidence/vehicles.md` L226; `pipelines/Wardogs_HitRegistration_v1.md` L100,128,141,718 |
| `0x3cad6d0`–`0x3cad71c` | stub | no | `docs/evidence/round8-radial.md` L81 |
| `0x3cb3030`–`0x3cb334a` | stub | no | `docs/ROUND11_STATUS.md` L375; `docs/evidence/round8-vehicle-sweep.md` L22 |
| `0x3cb6400`–`0x3cb648e` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L165 |
| `0x3d6be50`–`0x3d6be6d` | stub | no | `docs/ROUND11_STATUS.md` L92,682 |
| `0x3d6e180`–`0x3d6e1f1` | stub | no | `docs/ROUND11_STATUS.md` L639 |
| `0x3d70090`–`0x3d7028f` | stub | no | `docs/evidence/round8-impact.md` L95,104 |
| `0x3d83130`–`0x3d83138` | stub | no | `docs/evidence/round8-helmet.md` L56 |
| `0x3e0df10`–`0x3e0df7c` | stub | no | `docs/evidence/weapons.md` L168,260 |
| `0x3eaf060`–`0x3eaf1b5` | stub | no | `docs/evidence/round8-backblast.md` L94; `docs/evidence/round8-radial.md` L52; `docs/evidence/vehicles.md` L130; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L566 |
| `0x3ec25f0`–`0x3ec2624` | stub | no | `docs/ROUND11_STATUS.md` L574 |
| `0x3f5af30`–`0x3f5b0f6` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L21 |
| `0x3f5b100`–`0x3f5b391` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L21 |
| `0x3f6dbc0`–`0x3f6e049` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L21 |
| `0x40bfd40`–`0x40c03e3` | stub | no | `docs/evidence/round8-helmet.md` L34 |
| `0x41e1b20`–`0x41e1f9b` | stub | no | `docs/evidence/round8-gepard-collision-inputs.md` L92,93,95 |
| `0x4232fd0`–`0x4233054` | stub; not yet reverified | yes | `docs/evidence/round8-tapered-query.md` L87 |
| `0x42bbf10`–`0x42bbf1a` | stub | no | `docs/evidence/round8-loadout-restore.md` L98 |
| `0x42c83d0`–`0x42c8413` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L28 |
| `0x42c8580`–`0x42c85c3` | stub | no | `docs/evidence/round8-loadout.md` L391 |
| `0x42d9ef0`–`0x42da02d` | stub | no | `docs/evidence/vehicles.md` L131; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L578 |
| `0x42e4930`–`0x42e4bad` | stub | no | `docs/ROUND11_STATUS.md` L832; `docs/evidence/round8-gepard-collision-inputs.md` L85 |
| `0x4416ff0`–`0x4417060` | stub; not yet reverified | yes | `docs/ROUND11_STATUS.md` L665 |
| `0x44be3f0`–`0x44be61c` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L167 |
| `0x44cc530`–`0x44ccb3e` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L167 |
| `0x46e9680`–`0x46e96d1` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L157,169,171 |
| `0x48aa82f`–`0x48aa8ff` | stub; not yet reverified | no | `pipelines/Wardogs_ProjectileFlight_v1.md` L232,259,540; `pipelines/Wardogs_WeaponSpread_v1.md` L177,394 |
| `0x4bd0d20`–`0x4bd0d28` | stub | no | `docs/evidence/round9-underbarrel.md` L62; `pipelines/Wardogs_WeaponSpread_v1.md` L169 |
| `0x4d672b0`–`0x4d672cb` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L121 |
| `0x4dd62a0`–`0x4dd62bf` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L80 |
| `0x4e75170`–`0x4e7524b` | stub | no | `docs/evidence/round8-helmet.md` L56 |
| `0x50e010f`–`0x50e0480` | stub | no | `docs/ROUND11_STATUS.md` L96; `docs/evidence/round8-stn06-attachments.md` L13,20,21,24… |
| `0x50e09b0`–`0x50e0a4a` | stub | no | `docs/ROUND11_STATUS.md` L90; `docs/evidence/round9-vehicle-sampling.md` L45 |
| `0x50e0ad0`–`0x50e0b36` | stub | no | `docs/ROUND11_STATUS.md` L103; `docs/evidence/vehicles.md` L139,153; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L250 |
| `0x50e0b90`–`0x50e0c93` | stub | no | `docs/evidence/round9-vehicle-sampling.md` L47 |
| `0x50ee770`–`0x50ee9a9` | stub | no | `docs/ROUND11_STATUS.md` L91; `docs/evidence/vehicles.md` L143; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L271 |
| `0x50eee90`–`0x50ef04f` | stub | no | `docs/evidence/vehicles.md` L144; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L240 |
| `0x51fac40`–`0x51fc815` | stub | no | `docs/evidence/round8-impact.md` L153,161,163,170… |
| `0x5203d10`–`0x520441e` | stub | no | `docs/evidence/round8-impact.md` L149,151,152,153… |
| `0x5225c60`–`0x5225de1` | stub; not yet reverified | no | `docs/evidence/round17-blueprint-defaults.md` L60,61,62,63; `docs/evidence/round17-native-defaults.md` L180,181,182,183; `game-features/Wardogs_FireAndUtility_v1.md` L87 |
| `0x5230770`–`0x5230817` | stub | no | `docs/evidence/effects.md` L32,238 |
| `0x52382e0`–`0x5238375` | stub | no | `docs/evidence/damage.md` L617; `docs/evidence/effects.md` L136,190,193,194…; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L239 |
| `0x5238840`–`0x5238a0c` | stub | no | `docs/evidence/effects.md` L60,135,137,226; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L222,380 |
| `0x5238a10`–`0x5238b67` | stub | no | `docs/evidence/effects.md` L60,138,226; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L222,381 |
| `0x527b020`–`0x527b0ce` | stub | no | `docs/evidence/round8-impact.md` L71 |
| `0x527b100`–`0x527b1ae` | stub | no | `docs/ROUND11_STATUS.md` L1409; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1100 |
| `0x5293150`–`0x52931b3` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L173,396 |
| `0x5296540`–`0x5296553` | stub | no | `docs/evidence/round8-impact.md` L103 |
| `0x52aa1f0`–`0x52aa21d` | stub | no | `content/Wardogs_PlayerMovement_v1.md` L27 |
| `0x5307ed0`–`0x5307f07` | stub | no | `docs/evidence/vehicles.md` L154; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L715 |
| `0x53288b0`–`0x5328af9` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L148; `docs/evidence/vehicles.md` L163; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L713 |
| `0x532d4c0`–`0x532d57b` | stub | no | `docs/evidence/vehicles.md` L165; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L223 |
| `0x532dcb0`–`0x532dce3` | stub | no | `docs/evidence/round8-rotor-toggle.md` L53 |
| `0x532dd70`–`0x532ddb8` | stub | no | `docs/evidence/damage.md` L557; `docs/evidence/vehicles.md` L166,212; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1008 |
| `0x5339dd0`–`0x533a196` | stub | no | `docs/ROUND11_STATUS.md` L921; `docs/evidence/round8-explosive-viewer-audit.md` L174,177; `docs/evidence/vehicles.md` L171; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L727 |
| `0x533a750`–`0x533a7a7` | stub | no | `docs/ROUND11_STATUS.md` L923; `docs/evidence/effects.md` L142,198; `docs/evidence/vehicles.md` L172,252; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L254; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L931,1031 |
| `0x5345e9f`–`0x5346008` | stub | no | `docs/evidence/vehicles.md` L177,257,258,259…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L199 |
| `0x5356b00`–`0x5356f69` | stub | no | `docs/evidence/vehicles.md` L178; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L646,657 |
| `0x5365660`–`0x5365723` | stub | no | `docs/evidence/vehicles.md` L179; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L608 |
| `0x538abd0`–`0x538af47` | stub | no | `docs/evidence/vehicles.md` L60,117,185; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L219 |
| `0x53999b0`–`0x5399cb2` | stub | no | `docs/evidence/vehicles.md` L187,188; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L611,612,1010 |
| `0x53a00c0`–`0x53a01d0` | stub | no | `docs/evidence/vehicles.md` L191,302; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L517 |
| `0x53b6190`–`0x53b6251` | stub | no | `docs/evidence/vehicles.md` L192; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L924 |
| `0x53b9ff0`–`0x53ba37b` | stub | no | `docs/evidence/round8-stn06-attachments.md` L28,30 |
| `0x53cab60`–`0x53cac0e` | stub | no | `docs/ROUND11_STATUS.md` L1408; `docs/evidence/round8-exploding-gate.md` L68; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1099 |
| `0x5f7ed10`–`0x5f7ed19` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L202,208,210 |
| `0x6699d70`–`0x6699fce` | stub | no | `docs/evidence/round8-helmet.md` L18; `pipelines/infantry-viewer.md` L367 |
| `0x66bad60`–`0x66bc426` | stub | no | `docs/evidence/round8-helmet.md` L30,48; `pipelines/infantry-viewer.md` L367 |
| `0x675be60`–`0x675c0e3` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212 |
| `0x675cdb0`–`0x675ce08` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212; `pipelines/Wardogs_WeaponSpread_v1.md` L168 |
| `0x675ceb0`–`0x675cedf` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212 |
| `0x6772790`–`0x677283e` | stub | no | `docs/evidence/round8-loadout-initialization.md` L50 |
| `0x677f6e0`–`0x677fc53` | stub | no | `docs/evidence/round8-loadout-initialization.md` L111,113 |
| `0x6790750`–`0x679084c` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L43 |
| `0x6790af0`–`0x6790b4f` | stub | no | `docs/evidence/round8-ancillary-sights.md` L178 |
| `0x6791030`–`0x6791099` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L39 |
| `0x6795480`–`0x6795a95` | stub | no | `docs/evidence/round8-loadout.md` L256 |
| `0x6795b80`–`0x6796448` | stub | no | `docs/evidence/round8-loadout-initialization.md` L23,25,137,140… |
| `0x69a0f80`–`0x69a0fb7` | stub | no | `docs/evidence/round8-ancillary-sights.md` L130 |
| `0x69a18d0`–`0x69a191c` | stub | no | `docs/evidence/round9-underbarrel.md` L92 |
| `0x69c5e40`–`0x69c5e77` | stub | no | `docs/evidence/round8-loadout-buffer-layout.md` L36 |
| `0x69e8ff0`–`0x69e906e` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L248 |
| `0x69e93df`–`0x69e96ae` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L676,740 |
| `0x6a7f06a`–`0x6a7f25c` | stub | no | `content/Wardogs_Weapons_v2.md` L330; `docs/evidence/weapons.md` L111,117,222,230 |
| `0x6a7f870`–`0x6a7fc0a` | stub | no | `content/Wardogs_Weapons_v2.md` L330; `docs/evidence/weapons.md` L118 |
| `0x6b18c80`–`0x6b18d06` | stub | no | `docs/evidence/round8-radial.md` L133 |
| `0x6b18e30`–`0x6b18e70` | stub | no | `docs/evidence/round8-backblast.md` L22; `docs/evidence/round8-melee.md` L107; `docs/evidence/round8-weapon-context.md` L26,27 |
| `0x6b29fe0`–`0x6b2a299` | stub | no | `docs/evidence/round8-loadout-buffer-layout.md` L42 |
| `0x6b2a300`–`0x6b2a32a` | stub | no | `docs/evidence/round8-loadout.md` L187 |
| `0x6b53e20`–`0x6b543ef` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L75; `docs/evidence/round8-loadout-initialization.md` L16,18,19,103 |
| `0x6b54ae0`–`0x6b54e6c` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L326 |
| `0x6b5d150`–`0x6b5d1b9` | stub | no | `docs/evidence/round8-loadout-initialization.md` L184 |
| `0x6b725b0`–`0x6b73474` | stub | no | `docs/evidence/damage.md` L345,509,510,511…; `docs/evidence/round25-falloff.md` L91; `docs/evidence/round25-ricochet-penetration.md` L47,68; `docs/evidence/round8-armor.md` L40; `docs/evidence/round8-explosive-viewer-audit.md` L23; `docs/evidence/round8-physical-material-downstream.md` L178,179; `docs/evidence/round8-radial.md` L64,65,66,67; `docs/evidence/round8-weapon-context.md` L31; `docs/evidence/vehicles.md` L197,198; `docs/gap_resolution/RESEARCH_REGISTER.md` L52; `pipelines/Wardogs_DamagePipeline_v2.md` L21,113,129,187…; `pipelines/Wardogs_HitRegistration_v1.md` L38,115,568,658…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L54,1005; `pipelines/infantry-viewer.md` L349,353,360 |
| `0x6b73500`–`0x6b7373b` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L114,531,568,589… |
| `0x6b73810`–`0x6b73939` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L245,739 |
| `0x6b73940`–`0x6b739b2` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L248,739 |
| `0x6b73a60`–`0x6b73b2d` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L739 |
| `0x6b73b30`–`0x6b73c13` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L739 |
| `0x6b73de0`–`0x6b73e90` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L567,739 |
| `0x6b73e90`–`0x6b74394` | stub | no | `docs/evidence/round8-radial.md` L96; `pipelines/Wardogs_DamagePipeline_v2.md` L113; `pipelines/Wardogs_HitRegistration_v1.md` L37,110,112,552… |
| `0x6b74440`–`0x6b74625` | stub | no | `docs/evidence/round8-weapon-context.md` L29,37 |
| `0x6b74770`–`0x6b74781` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L675,740 |
| `0x6b75270`–`0x6b754e1` | stub | no | `docs/evidence/round8-weapon-context.md` L29,37 |
| `0x6b81720`–`0x6b81909` | stub | no | `docs/evidence/round17-native-defaults.md` L106,147,148,149; `game-features/Wardogs_Medical_v1.md` L138 |
| `0x6b81ce0`–`0x6b81fe2` | stub | no | `docs/evidence/damage.md` L513; `docs/evidence/effects.md` L144; `pipelines/Wardogs_DamagePipeline_v2.md` L1125,1130; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L256 |
| `0x6b82520`–`0x6b83265` | stub | no | `docs/evidence/damage.md` L514; `docs/evidence/effects.md` L145; `game-features/Wardogs_Medical_v1.md` L139; `pipelines/Wardogs_CombatDataFlow_v1.md` L179; `pipelines/Wardogs_DamagePipeline_v2.md` L1121,1124,1136,1146; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L270 |
| `0x6b83270`–`0x6b83284` | stub | no | `docs/evidence/damage.md` L477,515,679; `docs/evidence/effects.md` L146,207; `pipelines/Wardogs_DamagePipeline_v2.md` L1135; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L259 |
| `0x6b83360`–`0x6b834c2` | stub | no | `docs/evidence/effects.md` L147; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L271 |
| `0x6b83560`–`0x6b8358c` | stub | no | `docs/evidence/effects.md` L148; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L272 |
| `0x6b84e80`–`0x6b852ff` | stub | no | `content/Wardogs_Weapons_v2.md` L305; `docs/evidence/weapons.md` L100,121,211 |
| `0x6b85d30`–`0x6b860ca` | stub | no | `content/Wardogs_Weapons_v2.md` L245; `docs/evidence/weapons.md` L122,180; `docs/gap_resolution/RESEARCH_REGISTER.md` L51 |
| `0x6b86480`–`0x6b8685e` | stub | no | `docs/evidence/weapons.md` L161,162,239,260… |
| `0x6b86860`–`0x6b8699a` | stub | no | `content/Wardogs_Weapons_v2.md` L305; `docs/evidence/weapons.md` L124 |
| `0x6b89bb0`–`0x6b8a2ee` | stub | no | `content/Wardogs_Weapons_v2.md` L249,250; `docs/evidence/weapons.md` L134,135; `docs/gap_resolution/RESEARCH_REGISTER.md` L51 |
| `0x6b8a2f0`–`0x6b8a6f8` | stub | no | `content/Wardogs_Weapons_v2.md` L332; `docs/evidence/weapons.md` L136 |
| `0x6b8a700`–`0x6b8a8cf` | stub | no | `content/Wardogs_Weapons_v2.md` L324; `docs/evidence/weapons.md` L137 |
| `0x6b94700`–`0x6b95149` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L202; `pipelines/Wardogs_WeaponSpread_v1.md` L53,107,112,121… |
| `0x6b959e0`–`0x6b95a0b` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L239,373 |
| `0x6b95c50`–`0x6b95e4f` | stub | no | `content/Wardogs_Weapons_v2.md` L240,338; `docs/evidence/weapons.md` L52,53,141,142; `docs/gap_resolution/RESEARCH_REGISTER.md` L51; `pipelines/Wardogs_WeaponSpread_v1.md` L248,256 |
| `0x6b98f80`–`0x6b99002` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212 |
| `0x6b99160`–`0x6b99184` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L216 |
| `0x6b99270`–`0x6b992f9` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212,215 |
| `0x6b99300`–`0x6b99320` | stub; not yet reverified | yes | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L210 |
| `0x6b99530`–`0x6b996c9` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L249,392 |
| `0x6b996d0`–`0x6b99869` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L249,392 |
| `0x6b99ab0`–`0x6b99aed` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L202 |
| `0x6bb7e10`–`0x6bb80ce` | stub | no | `docs/evidence/damage.md` L318,545,592; `pipelines/Wardogs_DamagePipeline_v2.md` L718,1175 |
| `0x6bb8d00`–`0x6bb8d3c` | stub | no | `content/Wardogs_GameMechanics_v2.md` L74; `docs/WHAT_IS_LEFT.md` L69; `docs/evidence/round8-armor.md` L178; `pipelines/infantry-viewer.md` L81,345 |
| `0x6bb8d40`–`0x6bb8d86` | stub | no | `content/Wardogs_GameMechanics_v2.md` L93; `pipelines/infantry-viewer.md` L81,346 |
| `0x6bb97b0`–`0x6bb9850` | stub | no | `docs/evidence/round10-vehicle-blast-audit.md` L43 |
| `0x6bbab70`–`0x6bbb04b` | stub; not yet reverified | no | `docs/evidence/round25-falloff.md` L88; `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212; `pipelines/Wardogs_ProjectileFlight_v1.md` L99,538 |
| `0x6bbb7d0`–`0x6bbb81a` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L216 |
| `0x6c168f0`–`0x6c16981` | stub | no | `docs/evidence/round8-ancillary-sights.md` L192,259 |
| `0x6c2a4e0`–`0x6c2a58e` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L581 |
| `0x6c2a5f0`–`0x6c2a790` | stub | no | `docs/ROUND11_STATUS.md` L1202; `docs/evidence/damage.md` L549; `docs/evidence/vehicles.md` L208; `pipelines/Wardogs_DamagePipeline_v2.md` L257,1104; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L58 |
| `0x6c2a790`–`0x6c2aa47` | stub | no | `docs/ROUND11_STATUS.md` L1300; `docs/evidence/damage.md` L550,556,681; `docs/evidence/round10-native-vehicle-sampling.md` L25,63; `docs/evidence/round8-radial.md` L87; `docs/evidence/vehicles.md` L209; `pipelines/Wardogs_DamagePipeline_v2.md` L124; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L676 |
| `0x6c2b390`–`0x6c2b43e` | stub | no | `docs/evidence/round8-weaponowner-imports.md` L125; `docs/evidence/weapons.md` L142 |
| `0x6c41d20`–`0x6c41d9d` | stub | no | `docs/evidence/round9-underbarrel.md` L89,95 |
| `0x6c41da0`–`0x6c41e4e` | stub | no | `docs/evidence/round8-ancillary-sights.md` L180 |
| `0x6c61040`–`0x6c610f1` | stub | no | `docs/evidence/round8-ancillary-sights.md` L73 |
| `0x6c613b0`–`0x6c614fc` | stub | no | `docs/evidence/round8-ancillary-sights.md` L73 |
| `0x6c66540`–`0x6c6666f` | stub | no | `docs/evidence/effects.md` L149; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L273 |
| `0x6c67d40`–`0x6c67e65` | stub | no | `docs/evidence/round8-melee.md` L106,107,108 |
| `0x6c745f0`–`0x6c7472d` | stub | no | `docs/evidence/round9-underbarrel.md` L64 |
| `0x6c74730`–`0x6c74815` | stub | no | `docs/evidence/round9-underbarrel.md` L62 |
| `0x6c96fb0`–`0x6c97041` | stub | no | `docs/evidence/round8-ancillary-sights.md` L195,259 |
| `0x6c974e0`–`0x6c975ef` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L145,382 |
| `0x6c97710`–`0x6c97764` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L178,385 |
| `0x6c977b0`–`0x6c9783d` | stub | no | `content/Wardogs_Weapons_v2.md` L342; `docs/evidence/round8-ancillary-sights.md` L188,189,190,233… |
| `0x6c97840`–`0x6c978f2` | stub | no | `docs/evidence/round8-ancillary-sights.md` L129 |
| `0x6c979a0`–`0x6c979ef` | stub | no | `content/Wardogs_Weapons_v2.md` L243; `docs/evidence/weapons.md` L145 |
| `0x6c97dd0`–`0x6c98161` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L111 |
| `0x6c98290`–`0x6c986f4` | stub | no | `docs/evidence/damage.md` L418,551,552,680…; `docs/evidence/round24-ammo-availability.md` L7; `docs/evidence/round8-weapon-context.md` L90,91,191,260…; `docs/evidence/vehicles.md` L210; `pipelines/Wardogs_DamagePipeline_v2.md` L956,961,1242; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1005; `pipelines/Wardogs_WeaponSpread_v1.md` L384; `pipelines/infantry-viewer.md` L368 |
| `0x6c987a0`–`0x6c988e4` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L111,260,383,405 |
| `0x6c989a0`–`0x6c989ef` | stub | no | `content/Wardogs_Weapons_v2.md` L243; `docs/evidence/weapons.md` L146 |
| `0x6c9fee0`–`0x6ca0279` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L68,166,170,175… |
| `0x6ca1660`–`0x6ca167a` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L213 |
| `0x6ca167f`–`0x6ca170f` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L215 |
| `0x6ca1ae0`–`0x6ca1b74` | stub | no | `docs/evidence/effects.md` L56,160,219; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L367 |
| `0x6ca1fb0`–`0x6ca20e6` | stub; not yet reverified | no | `pipelines/Wardogs_WeaponSpread_v1.md` L186 |
| `0x6ca7800`–`0x6ca7e2f` | stub | no | `docs/evidence/round17-native-defaults.md` L20,28,29,30…; `docs/evidence/round8-explosive-actors.md` L47,49; `docs/evidence/round8-impact.md` L32,33; `docs/evidence/round8-radial.md` L129 |
| `0x6cf5370`–`0x6cf541e` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L90; `docs/evidence/round8-loadout.md` L393 |
| `0x6d58a10`–`0x6d58d73` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L85,131 |
| `0x6d6b260`–`0x6d6b30e` | stub | no | `docs/evidence/round8-loadout.md` L294 |
| `0x6d6b890`–`0x6d6b9cd` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L81 |
| `0x6d6bb00`–`0x6d6bc06` | stub | no | `docs/evidence/round8-loadout.md` L211,219,220 |
| `0x6d6bf70`–`0x6d6c101` | stub | no | `docs/evidence/round8-loadout.md` L211 |
| `0x6dae470`–`0x6dae491` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L600,741 |
| `0x6e6d580`–`0x6e6d8b6` | stub | no | `docs/evidence/round8-impact.md` L89,98 |
| `0x6e6dcc0`–`0x6e6dd8b` | stub | no | `docs/evidence/damage.md` L556,681; `docs/evidence/round8-radial.md` L87; `pipelines/Wardogs_DamagePipeline_v2.md` L122,124; `pipelines/infantry-viewer.md` L348,366 |
| `0x6e6e170`–`0x6e6e252` | stub | no | `docs/evidence/round8-armor.md` L30,31,49 |
| `0x6e7e530`–`0x6e7ed8b` | stub | no | `docs/evidence/round8-radial-mutable-topology.md` L18 |
| `0x6e7f0b0`–`0x6e7f1b6` | stub | no | `docs/evidence/damage.md` L561; `pipelines/Wardogs_DamagePipeline_v2.md` L1116 |
| `0x6e7f420`–`0x6e7f562` | stub | no | `docs/evidence/damage.md` L562; `pipelines/Wardogs_DamagePipeline_v2.md` L1118 |
| `0x6e7fa00`–`0x6e802a6` | stub | no | `docs/evidence/round8-radial-mutable-topology.md` L22; `docs/evidence/round8-radial-points-components.md` L88,98 |
| `0x6ef2f70`–`0x6ef30b7` | stub | no | `docs/evidence/round8-armor.md` L166,168; `pipelines/Wardogs_DamagePipeline_v2.md` L810 |
| `0x6ef30bd`–`0x6ef324e` | stub | no | `docs/evidence/damage.md` L379; `docs/evidence/round8-armor.md` L166,167,168; `pipelines/Wardogs_DamagePipeline_v2.md` L811 |
| `0x6f1ffa0`–`0x6f200da` | stub | no | `docs/evidence/round8-exploding-gate.md` L16; `pipelines/Wardogs_ProjectileFlight_v1.md` L166 |
| `0x6f29130`–`0x6f291b9` | stub; not yet reverified | no | `pipelines/Wardogs_ProjectileFlight_v1.md` L253 |
| `0x6f34110`–`0x6f341af` | stub | no | `docs/evidence/round8-exploding-gate.md` L18 |
| `0x6f342b0`–`0x6f343f3` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L111,329,734; `pipelines/Wardogs_ProjectileFlight_v1.md` L170 |
| `0x6f344c5`–`0x6f34a00` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L557,689,690,733; `pipelines/Wardogs_ProjectileFlight_v1.md` L489,503 |
| `0x6f34fe0`–`0x6f34fff` | stub; not yet reverified | no | `pipelines/Wardogs_ProjectileFlight_v1.md` L383 |
| `0x6f37c00`–`0x6f38092` | stub | no | `docs/evidence/round8-physical-material-downstream.md` L135; `pipelines/Wardogs_ProjectileFlight_v1.md` L164 |
| `0x6f380a0`–`0x6f3835c` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L111,329,374,689… |
| `0x6f38360`–`0x6f3864f` | stub; not yet reverified | no | `pipelines/Wardogs_HitRegistration_v1.md` L546 |
| `0x6fa5970`–`0x6fa59c8` | stub | no | `docs/evidence/round8-loadout-frontend.md` L20 |
| `0x756e790`–`0x756eabb` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L75,76 |
| `0x76384e0`–`0x763877a` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L82 |
| `0x76423a0`–`0x764244e` | stub | no | `docs/evidence/round8-weaponowner-imports.md` L130 |
| `0x7642580`–`0x7642956` | stub | no | `docs/evidence/round8-weapon-context.md` L24 |
| `0x76448d0`–`0x76449b3` | stub | no | `docs/evidence/round8-weapon-context.md` L285,287 |
| `0x7645a30`–`0x76460c0` | stub | no | `docs/evidence/round8-weapon-context.md` L190,270,273,274…; `pipelines/infantry-viewer.md` L368 |
| `0x7646710`–`0x764686e` | stub | no | `docs/evidence/round8-weapon-context.md` L290 |
| `0x7647680`–`0x764785d` | stub | no | `docs/evidence/round8-weapon-context.md` L286 |
| `0x76478d0`–`0x7647e89` | stub | no | `docs/evidence/round8-weapon-context.md` L26,28,34; `game-features/Wardogs_GameFeatures_Weapons_v2.md` L206,215; `pipelines/infantry-viewer.md` L360 |
| `0x767b9b0`–`0x767bc33` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L168 |
| `0x767bc40`–`0x767cdc4` | stub | no | `docs/ROUND11_STATUS.md` L1445; `docs/evidence/vehicles.md` L231,289; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L71,1136 |
| `0x76a18f0`–`0x76a1aff` | stub | no | `docs/evidence/round17-native-defaults.md` L58,82,83,84… |
| `0x76a36b0`–`0x76a3993` | stub | no | `docs/evidence/round8-rotor-toggle.md` L48 |
| `0x76a8510`–`0x76a8868` | stub | no | `docs/evidence/round8-weapon-context.md` L283 |
| `0x76c3eb0`–`0x76c3ffb` | stub | no | `docs/evidence/round8-backblast.md` L59,61,73; `pipelines/Wardogs_DamagePipeline_v2.md` L324; `pipelines/infantry-viewer.md` L359 |
| `0x76cab80`–`0x76cb132` | stub | no | `docs/evidence/round8-exploding-gate.md` L69,73,75,78 |
| `0x76cfeb0`–`0x76d04f6` | stub | no | `docs/evidence/round8-exploding-gate.md` L22,25,26,40…; `pipelines/infantry-viewer.md` L364 |
| `0x76db350`–`0x76db39a` | stub; not yet reverified | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L216 |
| `0x7741ab0`–`0x7741cab` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L81 |
| `0x8584cc0`–`0x8585019` | stub | no | `docs/evidence/round17-native-defaults.md` L190,196,197,198… |
| `0x863b270`–`0x863b54a` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L84 |
| `0x869bf50`–`0x869bfcb` | stub | no | `docs/evidence/round17-native-defaults.md` L55 |
| `0x869bff0`–`0x869c1f9` | stub | no | `docs/evidence/round17-native-defaults.md` L59,65 |
| `0x977e560`–`0x977ef14` | stub | no | `docs/evidence/damage.md` L46,653 |
| `0x42333f0`–`0x42336d6` | differs; reverified r19 (a) unaffected: function bytes identical, page difference is the previous function's tail | no | `docs/evidence/round8-tapered-query.md` L53,69,70,87; `pipelines/infantry-viewer.md` L362 |
| `0x44176d0`–`0x441772e` | differs; reverified r19 (a) unaffected: function bytes identical, page difference is the previous function's tail | no | `docs/ROUND11_STATUS.md` L655,665 |
| `0x1921820` | stub | - | `docs/evidence/weapons.md` L142; `pipelines/Wardogs_WeaponSpread_v1.md` L108 |
| `0x1c051c0` | stub | - | `docs/evidence/effects.md` L166 |
| `0x246f800` | stub | - | `docs/ROUND11_STATUS.md` L312 |
| `0x2470310` | stub | - | `docs/ROUND11_STATUS.md` L837 |
| `0x395baf0` | stub | - | `docs/evidence/round8-ancillary-sights.md` L260 |
| `0x3c95c30` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L20; `docs/evidence/vehicles.md` L203; `pipelines/Wardogs_HitRegistration_v1.md` L51,164,168,721 |
| `0x3c95c61` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L20 |
| `0x3ca8630` | stub | - | `docs/evidence/effects.md` L90,100,184,195; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L316 |
| `0x3cab0a0` | stub; not yet reverified | - | `pipelines/Wardogs_HitRegistration_v1.md` L565; `pipelines/Wardogs_WeaponSpread_v1.md` L249 |
| `0x3cadbd0` | stub | - | `docs/ROUND11_STATUS.md` L164 |
| `0x3d6e200` | stub | - | `docs/ROUND11_STATUS.md` L639 |
| `0x41e0ea0` | stub | - | `docs/evidence/round8-tapered-query.md` L54 |
| `0x4244430` | stub | - | `docs/evidence/round8-tapered-query.md` L24 |
| `0x42d9770` | stub; not yet reverified | - | `pipelines/Wardogs_HitRegistration_v1.md` L52,166,723 |
| `0x44c2ba0` | stub | - | `docs/evidence/round10-native-vehicle-sampling.md` L20; `docs/evidence/round8-gepard-collision-inputs.md` L38,39 |
| `0x44c2bd0` | stub | - | `docs/evidence/round8-gepard-collision-inputs.md` L39 |
| `0x46dbb20` | stub | - | `docs/evidence/round8-loadout-rebuy.md` L123 |
| `0x50bf500` | stub | - | `docs/ROUND11_STATUS.md` L119,579; `docs/evidence/vehicles.md` L136,301; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L545 |
| `0x50bf880` | stub | - | `docs/evidence/vehicles.md` L136,137,138,262…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L203,516,635,1037 |
| `0x50bf9fd` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L18; `docs/evidence/vehicles.md` L138; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L580 |
| `0x50e08c0` | stub | - | `docs/ROUND11_STATUS.md` L95; `docs/evidence/round8-stn06-attachments.md` L21,22 |
| `0x50e08c5` | stub | - | `docs/evidence/round8-stn06-attachments.md` L23; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L276 |
| `0x52301f0` | stub | - | `docs/ROUND11_STATUS.md` L922; `docs/evidence/weapons.md` L148 |
| `0x5230c80` | stub | - | `docs/evidence/effects.md` L60,120,233; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L229 |
| `0x5296290` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L171,396 |
| `0x532d120` | stub | - | `docs/evidence/round8-rotor-toggle.md` L69,70 |
| `0x532d17a` | stub | - | `docs/evidence/round8-rotor-toggle.md` L70 |
| `0x532d180` | stub | - | `docs/evidence/round8-rotor-toggle.md` L49,58 |
| `0x532d1b0` | stub | - | `docs/evidence/round8-rotor-toggle.md` L49 |
| `0x53cae20` | stub | - | `docs/evidence/round8-loadout-buffer-layout.md` L28; `docs/evidence/round8-loadout-deathmatch.md` L31; `docs/evidence/round8-loadout-restore.md` L75; `docs/evidence/round8-weapon-context.md` L113 |
| `0x675ce10` | stub; not yet reverified | - | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L212,213 |
| `0x67912b0` | stub | - | `docs/evidence/round8-loadout.md` L189 |
| `0x6b18e70` | stub | - | `docs/evidence/round8-radial.md` L133; `docs/evidence/vehicles.md` L196,286; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L72 |
| `0x6b86240` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L170,395 |
| `0x6b86470` | stub | - | `content/Wardogs_Weapons_v2.md` L305; `docs/evidence/weapons.md` L123,236,237 |
| `0x6b95630` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L146,372 |
| `0x6b956b0` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L34,124,135,371 |
| `0x6bb9850` | stub | - | `docs/evidence/round10-vehicle-blast-audit.md` L47; `docs/evidence/round8-explosive-actors.md` L48; `docs/evidence/round8-radial.md` L129 |
| `0x6bb9858` | stub | - | `docs/evidence/round8-explosive-actors.md` L51 |
| `0x6bb9883` | stub | - | `docs/evidence/round8-explosive-actors.md` L51 |
| `0x6bb9888` | stub | - | `docs/evidence/round10-vehicle-blast-audit.md` L48; `docs/evidence/round8-explosive-actors.md` L52 |
| `0x6bbd3d0` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L85,144,375 |
| `0x6bbd420` | stub; not yet reverified | - | `pipelines/Wardogs_ProjectileFlight_v1.md` L92,473,536; `pipelines/Wardogs_WeaponSpread_v1.md` L377 |
| `0x6bbd500` | stub; not yet reverified | - | `pipelines/Wardogs_ProjectileFlight_v1.md` L89,535; `pipelines/Wardogs_WeaponSpread_v1.md` L88,239,377 |
| `0x6bbd5b0` | stub | - | `docs/evidence/weapons.md` L179,261 |
| `0x6bbd5d0` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L266,377 |
| `0x6bbd5e0` | stub | - | `docs/evidence/weapons.md` L191,263 |
| `0x6bbd650` | stub | - | `docs/evidence/round8-weapon-context.md` L77 |
| `0x6bbd780` | stub | - | `docs/evidence/round8-weapon-context.md` L81,99,130,141 |
| `0x6bbd7da` | stub | - | `docs/evidence/round8-weapon-context.md` L81 |
| `0x6bd35e0` | stub | - | `docs/evidence/round8-loadout-rebuy.md` L140 |
| `0x6c41d9d` | stub | - | `docs/evidence/round9-underbarrel.md` L95 |
| `0x6c41f80` | stub | - | `docs/evidence/round8-ancillary-sights.md` L60 |
| `0x6ce86a0` | stub | - | `docs/evidence/round8-loadout-rebuy.md` L120 |
| `0x6ce9110` | stub | - | `docs/evidence/round8-loadout-rebuy.md` L267 |
| `0x6ce9cf0` | stub | - | `docs/evidence/round8-loadout.md` L187 |
| `0x6d334a0` | stub | - | `docs/evidence/round8-loadout.md` L127 |
| `0x6daeaa0` | stub; not yet reverified | - | `pipelines/Wardogs_HitRegistration_v1.md` L556 |
| `0x6e6e260` | stub; not yet reverified | - | `pipelines/Wardogs_WeaponSpread_v1.md` L170,395 |
| `0x6e6eba0` | stub | - | `docs/evidence/damage.md` L517,557,681; `docs/evidence/vehicles.md` L204,212; `pipelines/Wardogs_DamagePipeline_v2.md` L225,1098; `pipelines/Wardogs_HitRegistration_v1.md` L256; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1008 |
| `0x6e6ee40` | stub; not yet reverified | - | `pipelines/Wardogs_HitRegistration_v1.md` L247 |
| `0x6f78270` | stub; not yet reverified | - | `pipelines/Wardogs_ProjectileFlight_v1.md` L39,356,527 |
| `0x74f72e0` | stub | - | `docs/evidence/round8-exploding-gate.md` L28 |
| `0x76449c0` | stub | - | `docs/evidence/round8-weapon-context.md` L110 |
| `0x76ab5f0` | stub | - | `docs/WHAT_IS_LEFT.md` L122; `docs/evidence/vehicles.md` L66,236,314; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L615 |

## Byte-level comparison

The own bytes of each cited function that has a corpus row in `.text` were compared between the analysis image and the reference image (file offsets from each image's `.text` section). For the functions in the 'stub' and 'differs' categories the immediately preceding corpus function was compared the same way.

| Measure | Count |
|---|---:|
| Cited functions in `.text` (distinct corpus rows) | 1027 |
| Cited addresses with no function row (not compared) | 544 |
| Own bytes identical | 1018 |
| Own bytes differ (any category) | 9 |
| Not comparable (range outside the reference `.text`) | 0 |
| Own bytes differ, category 'unknown' (page not in the recovered table) | 0 |
| Category clean | 739 |
| Category stub or differs | 258 |
| &nbsp;&nbsp;of which own bytes differ | 9 |
| &nbsp;&nbsp;of which own bytes identical | 249 |
| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in a corpus row whose own bytes differ | 136 |
| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in no corpus row | 113 |
| &nbsp;&nbsp;&nbsp;&nbsp;other | 0 |
| &nbsp;&nbsp;&nbsp;&nbsp;(immediately preceding row has differing own bytes, for reference) | 7 |

Cited functions whose own bytes differ between the images (9 rows, by start address; at most 60 shown). 'Preceding' is the corpus function immediately below the cited start, with its own-bytes status.

| Function | Category | Stub in body | Differing own bytes (first rva) | Preceding function | Preceding own bytes | Cited at |
|---|---|---|---|---|---|---|
| `0x1670b80`–`0x1670cad` | stub | yes | 297 (`0x1670b81`) | `0x1670a4d`–`0x1670b7e` | differs | `pipelines/Wardogs_WeaponSpread_v1.md:34`; `pipelines/Wardogs_WeaponSpread_v1.md:387` |
| `0x395be30`–`0x395beb9` | stub | yes | 132 (`0x395be31`) | `0x395bd50`–`0x395be2a` | same | `content/Wardogs_WeaponAttributes_v1.md:80`; `content/Wardogs_WeaponAttributes_v1.md:84` +6 |
| `0x4232fd0`–`0x4233054` | stub | yes | 130 (`0x4232fd1`) | `0x4232700`–`0x4232fc4` | same | `docs/evidence/round8-tapered-query.md:87` |
| `0x4416ff0`–`0x4417060` | stub | yes | 109 (`0x4416ff0`) | `0x4416f50`–`0x4416fe9` | same | `docs/ROUND11_STATUS.md:665` |
| `0x5230be0`–`0x5230c39` | stub | yes | 85 (`0x5230be2`) | `0x5230b80`–`0x5230bd9` | differs | `docs/ROUND11_STATUS.md:1183`; `docs/ROUND11_STATUS.md:1185` |
| `0x6b74e30`–`0x6b74f79` | stub | yes | 319 (`0x6b74e30`) | `0x6b747f0`–`0x6b74e28` | same | `docs/evidence/round8-weapon-context.md:31`; `docs/evidence/round8-weapon-context.md:35` +1 |
| `0x6b8ac90`–`0x6b8acaf` | stub | yes | 26 (`0x6b8ac92`) | `0x6b8ac60`–`0x6b8ac81` | differs | `content/Wardogs_Weapons_v2.md:332`; `content/Wardogs_Weapons_v2.md:334` +2 |
| `0x6b99300`–`0x6b99320` | stub | yes | 29 (`0x6b99302`) | `0x6b99270`–`0x6b992f9` | same | `game-features/Wardogs_GameFeatures_Weapons_v2.md:210` |
| `0x6bb8970`–`0x6bb89a3` | stub | yes | 47 (`0x6bb8972`) | `0x6bb8900`–`0x6bb8969` | same | `docs/ROUND11_STATUS.md:980`; `docs/ROUND11_STATUS.md:988` +4 |

Reading the section. The nine rows with differing own bytes are all stub-bodied functions, so the difference is the dispatch stub that replaces the body in the analysis image. Every cited function whose category is clean or unknown has identical own bytes.

Of the 249 stub or differs functions whose own bytes are identical, 136 have differing bytes outside their range inside a corpus row whose own bytes differ. This covers the two round 19 cases: `0x42333f0` and `0x44176d0` differ only in the tail of the stub functions `0x4232fd0` and `0x4416ff0`, which share their page. Only seven of them have a differing immediately preceding row (`0x157c320`, `0x15b83b0`, `0x1670caf`, `0x2f691e0`, `0x538abd0`, `0x6b73a60`, `0x6b99160`). For the other 113, the differing bytes lie in no corpus row, so this check does not attribute them. They are an open question about the protection layer's byte layout, not evidence that a claim is wrong.

Method: `_tools/ida_claim_bytes.py` (sibling of `_tools/ida_claim_exposure.py`, which supplies the page classes and the citation list). Run `python -I _tools/ida_claim_bytes.py` for this section, or add `--tsv` for one line per cited function.
