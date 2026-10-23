# IDA claim exposure to the protection layer

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page lists which native-address citations in these docs sit on code pages that the executable's protection layer may have virtualized. **Classification means "the page contains a stub", not "the claim is wrong".** Nothing here has been retracted. Round 19 re-verified two stub-in-body functions (`0x6bb8970`, `0x6b8ac90`): both unaffected, supported by the reference image only (see rows). The page only says where a re-check would be most useful.

## Method

Every `0x` token of at least `0x100000` in `docs/`, `pipelines/`, `content/` and `game-features/` (excluding this page) was collected with `_tools/ida_claim_exposure.py`, which reuses the extractor in `_tools/rva_status.py`. Each token was resolved to the decompilation-corpus function that contains it, and every 4 KiB code page that function spans was looked up in a page table built by comparing the static-analysis image with the older reference image. In that image 37,878 protected `.text` pages were recovered. Of these, 31,659 are byte-identical to the reference and 6,219 differ. Of the differing pages, 6,081 contain a differing indirect dispatch stub (a `mov reg,[rip+x]` followed by `jmp [reg+disp]` through the protection layer's global table), and 138 differ without a recognised stub; eleven of those 138 are separately captured pages. Full devirtualization has not been done, so a decompiled function on such a page may be incomplete. A citation takes the worst category among its function's pages (exceptional, then stub, then differs without stub, then clean). Tokens outside the protected pages are "unknown". Only the function's own pages are checked, so a clean function that calls into a stub is not flagged. Many tokens in the docs are data addresses or sizes rather than code, which is why "unknown" is large. A token with no corpus function row is classified by the page of the address alone.

## Counts

2527 distinct addresses, by the worst page category across the containing function:

| Category | Distinct addresses | Notes |
|---|---:|---|
| Clean | 1795 | every spanned page is byte-identical to the reference |
| Page with a dispatch stub | 469 | 200 functions plus 50 addresses with no function row; 5 functions contain a stub inside their own byte range |
| Differs, no stub recognised | 8 | 2 functions |
| Exceptional (the eleven separately captured pages) | 0 | no citation lands on those pages |
| Unknown | 255 | 203 outside `.text` (data addresses), 47 in a function that spans unprotected text pages, 5 with no function row on an unprotected page |

By the page of the cited address alone (ignoring the rest of its function): clean 1876, stub 395, differs 8, exceptional 0, unknown 248.

## Reading the table

A function listed below is not necessarily virtualized. The strongest signal is the column "Stub in body". `yes` means a dispatch stub instruction pair lies inside the function's own byte range, so that decompilation should be re-read first. `no` means only another part of a spanned page holds a stub. `-` means the address has no function row, so it is classified by its own page.

## Claims in non-clean pages

252 entries (200 stub functions, 50 stub addresses without a function row, 2 differs-without-stub functions), citing 477 addresses. Citation lists show at most four lines per file.

| Function range or address | Category | Stub in body | Cited at |
|---|---|---|---|
| `0x395be30`–`0x395beb9` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `content/Wardogs_WeaponAttributes_v1.md` L79; `docs/evidence/round8-ancillary-sights.md` L211; `docs/evidence/round8-weapon-context.md` L157,165,167 |
| `0x5230be0`–`0x5230c39` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `docs/ROUND11_STATUS.md` L1179 |
| `0x6b74e30`–`0x6b74f79` | stub; reverified r19 (a) unaffected: entry stub only, reference body matches claims | yes | `docs/evidence/round8-weapon-context.md` L31,35 |
| `0x6b8ac90`–`0x6b8acaf` | stub | yes (reverified r19: unaffected; whole body is the stub, original leaf in reference image matches `+0x41C` claim) | `content/Wardogs_Weapons_v2.md` L330; `docs/evidence/weapons.md` L43,138 |
| `0x6bb8970`–`0x6bb89a3` | stub | yes (reverified r19: unaffected; whole body is the stub, original lookup in reference image matches first-match-index / -1 claim) | `docs/ROUND11_STATUS.md` L978; `docs/evidence/damage.md` L546; `pipelines/Wardogs_DamagePipeline_v2.md` L73,462 |
| `0x157c320`–`0x157c468` | stub | no | `docs/evidence/round8-loadout-rebuy.md` L110 |
| `0x1587900`–`0x15879ea` | stub | no | `docs/evidence/damage.md` L259,496; `pipelines/Wardogs_DamagePipeline_v2.md` L1165 |
| `0x15b83b0`–`0x15b83b4` | stub | no | `docs/evidence/damage.md` L311,645,651 |
| `0x15fecf0`–`0x15ff3aa` | stub | no | `docs/evidence/round8-propertybag-types.md` L25 |
| `0x1812a60`–`0x1812a65` | stub | no | `docs/evidence/round8-backblast.md` L22 |
| `0x188c980`–`0x188ca5b` | stub | no | `docs/evidence/round8-radial-points-components.md` L84 |
| `0x18f0650`–`0x18f0658` | stub | no | `docs/evidence/round8-weapon-context.md` L25 |
| `0x19a4a50`–`0x19a4a59` | stub | no | `content/Wardogs_Weapons_v2.md` L334; `docs/evidence/weapons.md` L50,113 |
| `0x1c36300`–`0x1c36308` | stub | no | `docs/evidence/round8-backblast.md` L20; `docs/evidence/round8-weapon-context.md` L30 |
| `0x1cc7300`–`0x1cc7308` | stub | no | `docs/evidence/round8-loadout-restore.md` L41 |
| `0x1d2c340`–`0x1d2c348` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L201 |
| `0x21a6160`–`0x21a623e` | stub | no | `docs/evidence/round8-tapered-query.md` L30 |
| `0x21e1b20`–`0x21e1cc8` | stub | no | `docs/ROUND11_STATUS.md` L275 |
| `0x246f660`–`0x246f68e` | stub | no | `docs/ROUND11_STATUS.md` L831; `docs/evidence/round8-gepard-collision-inputs.md` L83,84 |
| `0x2470790`–`0x2470884` | stub | no | `docs/evidence/round8-tapered-query.md` L55 |
| `0x250b310`–`0x250b4cb` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L73 |
| `0x2835b24`–`0x2835d7f` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L21 |
| `0x2f691e0`–`0x2f691e8` | stub | no | `docs/evidence/round8-ancillary-sights.md` L202 |
| `0x3955370`–`0x39554ca` | stub | no | `docs/evidence/round8-radial.md` L133 |
| `0x395ade0`–`0x395b048` | stub | no | `docs/evidence/damage.md` L497,498; `pipelines/Wardogs_DamagePipeline_v2.md` L1166 |
| `0x3a39990`–`0x3a39a3e` | stub | no | `docs/evidence/round10-native-vehicle-sampling.md` L19; `docs/evidence/round8-radial.md` L84 |
| `0x3a93090`–`0x3a932ff` | stub | no | `docs/evidence/damage.md` L320,499; `docs/evidence/round8-loadout.md` L397; `pipelines/Wardogs_DamagePipeline_v2.md` L1167 |
| `0x3a9b050`–`0x3a9b0da` | stub | no | `docs/evidence/weapons.md` L206,261 |
| `0x3c70f50`–`0x3c71154` | stub | no | `docs/ROUND11_STATUS.md` L489 |
| `0x3c95950`–`0x3c95aab` | stub | no | `docs/ROUND11_STATUS.md` L163,488 |
| `0x3ca21b0`–`0x3ca2230` | stub | no | `docs/evidence/round8-vehicle-sweep.md` L12,20 |
| `0x3ca2b40`–`0x3ca2dca` | stub | no | `docs/ROUND11_STATUS.md` L548 |
| `0x3ca8f70`–`0x3ca8fd0` | stub | no | `docs/evidence/round8-loadout-initialization.md` L40 |
| `0x3cab090`–`0x3cab098` | stub | no | `docs/evidence/round8-loadout-initialization.md` L23 |
| `0x3cab670`–`0x3cab6e9` | stub | no | `docs/ROUND11_STATUS.md` L159; `docs/evidence/round8-explosive-viewer-audit.md` L204; `docs/evidence/vehicles.md` L226 |
| `0x3cad6d0`–`0x3cad71c` | stub | no | `docs/evidence/round8-radial.md` L81 |
| `0x3cb3030`–`0x3cb334a` | stub | no | `docs/ROUND11_STATUS.md` L375; `docs/evidence/round8-vehicle-sweep.md` L22 |
| `0x3d6be50`–`0x3d6be6d` | stub | no | `docs/ROUND11_STATUS.md` L92,680 |
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
| `0x42bbf10`–`0x42bbf1a` | stub | no | `docs/evidence/round8-loadout-restore.md` L98 |
| `0x42c83d0`–`0x42c8413` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L28 |
| `0x42c8580`–`0x42c85c3` | stub | no | `docs/evidence/round8-loadout.md` L391 |
| `0x42d9ef0`–`0x42da02d` | stub | no | `docs/evidence/vehicles.md` L131; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L578 |
| `0x42e4930`–`0x42e4bad` | stub | no | `docs/ROUND11_STATUS.md` L830; `docs/evidence/round8-gepard-collision-inputs.md` L85 |
| `0x44be3f0`–`0x44be61c` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L167 |
| `0x44cc530`–`0x44ccb3e` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L167 |
| `0x46e9680`–`0x46e96d1` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L157,169,171 |
| `0x4bd0d20`–`0x4bd0d28` | stub | no | `docs/evidence/round9-underbarrel.md` L62 |
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
| `0x5230770`–`0x5230817` | stub | no | `docs/evidence/effects.md` L32,238 |
| `0x52382e0`–`0x5238375` | stub | no | `docs/evidence/damage.md` L617; `docs/evidence/effects.md` L136,190,193,194…; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L239 |
| `0x5238840`–`0x5238a0c` | stub | no | `docs/evidence/effects.md` L60,135,137,226; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L222,380 |
| `0x5238a10`–`0x5238b67` | stub | no | `docs/evidence/effects.md` L60,138,226; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L222,381 |
| `0x527b020`–`0x527b0ce` | stub | no | `docs/evidence/round8-impact.md` L71 |
| `0x527b100`–`0x527b1ae` | stub | no | `docs/ROUND11_STATUS.md` L1403; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1100 |
| `0x5296540`–`0x5296553` | stub | no | `docs/evidence/round8-impact.md` L103 |
| `0x52aa1f0`–`0x52aa21d` | stub | no | `content/Wardogs_PlayerMovement_v1.md` L26 |
| `0x5307ed0`–`0x5307f07` | stub | no | `docs/evidence/vehicles.md` L154; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L715 |
| `0x53288b0`–`0x5328af9` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L148; `docs/evidence/vehicles.md` L163; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L713 |
| `0x532d4c0`–`0x532d57b` | stub | no | `docs/evidence/vehicles.md` L165; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L223 |
| `0x532dcb0`–`0x532dce3` | stub | no | `docs/evidence/round8-rotor-toggle.md` L53 |
| `0x532dd70`–`0x532ddb8` | stub | no | `docs/evidence/damage.md` L557; `docs/evidence/vehicles.md` L166,212; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1008 |
| `0x5339dd0`–`0x533a196` | stub | no | `docs/ROUND11_STATUS.md` L919; `docs/evidence/round8-explosive-viewer-audit.md` L174,177; `docs/evidence/vehicles.md` L171; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L727 |
| `0x533a750`–`0x533a7a7` | stub | no | `docs/ROUND11_STATUS.md` L921; `docs/evidence/effects.md` L142,198; `docs/evidence/vehicles.md` L172,252; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L254; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L931,1031 |
| `0x5345e9f`–`0x5346008` | stub | no | `docs/evidence/vehicles.md` L177,257,258,259…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L199 |
| `0x5356b00`–`0x5356f69` | stub | no | `docs/evidence/vehicles.md` L178; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L646,657 |
| `0x5365660`–`0x5365723` | stub | no | `docs/evidence/vehicles.md` L179; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L608 |
| `0x538abd0`–`0x538af47` | stub | no | `docs/evidence/vehicles.md` L60,117,185; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L219 |
| `0x53999b0`–`0x5399cb2` | stub | no | `docs/evidence/vehicles.md` L187,188; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L611,612,1010 |
| `0x53a00c0`–`0x53a01d0` | stub | no | `docs/evidence/vehicles.md` L191,302; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L517 |
| `0x53b6190`–`0x53b6251` | stub | no | `docs/evidence/vehicles.md` L192; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L924 |
| `0x53b9ff0`–`0x53ba37b` | stub | no | `docs/evidence/round8-stn06-attachments.md` L28,30 |
| `0x53cab60`–`0x53cac0e` | stub | no | `docs/ROUND11_STATUS.md` L1402; `docs/evidence/round8-exploding-gate.md` L68; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1099 |
| `0x5f7ed10`–`0x5f7ed19` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L201 |
| `0x6699d70`–`0x6699fce` | stub | no | `docs/evidence/round8-helmet.md` L18; `pipelines/infantry-viewer.md` L367 |
| `0x66bad60`–`0x66bc426` | stub | no | `docs/evidence/round8-helmet.md` L30,48; `pipelines/infantry-viewer.md` L367 |
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
| `0x6a7f06a`–`0x6a7f25c` | stub | no | `content/Wardogs_Weapons_v2.md` L328; `docs/evidence/weapons.md` L111,117,222,230 |
| `0x6a7f870`–`0x6a7fc0a` | stub | no | `content/Wardogs_Weapons_v2.md` L328; `docs/evidence/weapons.md` L118 |
| `0x6b18c80`–`0x6b18d06` | stub | no | `docs/evidence/round8-radial.md` L133 |
| `0x6b18e30`–`0x6b18e70` | stub | no | `docs/evidence/round8-backblast.md` L22; `docs/evidence/round8-melee.md` L107; `docs/evidence/round8-weapon-context.md` L26,27 |
| `0x6b29fe0`–`0x6b2a299` | stub | no | `docs/evidence/round8-loadout-buffer-layout.md` L42 |
| `0x6b2a300`–`0x6b2a32a` | stub | no | `docs/evidence/round8-loadout.md` L187 |
| `0x6b53e20`–`0x6b543ef` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L75; `docs/evidence/round8-loadout-initialization.md` L16,18,19,103 |
| `0x6b5d150`–`0x6b5d1b9` | stub | no | `docs/evidence/round8-loadout-initialization.md` L184 |
| `0x6b725b0`–`0x6b73474` | stub | no | `docs/evidence/damage.md` L345,509,510,511…; `docs/evidence/round8-armor.md` L40; `docs/evidence/round8-explosive-viewer-audit.md` L23; `docs/evidence/round8-physical-material-downstream.md` L178,179; `docs/evidence/round8-radial.md` L64,65,66,67; `docs/evidence/round8-weapon-context.md` L31; `docs/evidence/vehicles.md` L197,198; `docs/gap_resolution/RESEARCH_REGISTER.md` L52; `pipelines/Wardogs_DamagePipeline_v2.md` L105,121,179,183…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L54,1005; `pipelines/infantry-viewer.md` L349,353,360 |
| `0x6b73e90`–`0x6b74394` | stub | no | `docs/evidence/round8-radial.md` L96 |
| `0x6b74440`–`0x6b74625` | stub | no | `docs/evidence/round8-weapon-context.md` L29,37 |
| `0x6b75270`–`0x6b754e1` | stub | no | `docs/evidence/round8-weapon-context.md` L29,37 |
| `0x6b81720`–`0x6b81909` | stub | no | `docs/evidence/round17-native-defaults.md` L106,147,148,149; `game-features/Wardogs_Medical_v1.md` L137 |
| `0x6b81ce0`–`0x6b81fe2` | stub | no | `docs/evidence/damage.md` L513; `docs/evidence/effects.md` L144; `pipelines/Wardogs_DamagePipeline_v2.md` L1113,1118; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L256 |
| `0x6b82520`–`0x6b83265` | stub | no | `docs/evidence/damage.md` L514; `docs/evidence/effects.md` L145; `game-features/Wardogs_Medical_v1.md` L138; `pipelines/Wardogs_CombatDataFlow_v1.md` L179; `pipelines/Wardogs_DamagePipeline_v2.md` L1109,1112,1124,1134; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L270 |
| `0x6b83270`–`0x6b83284` | stub | no | `docs/evidence/damage.md` L477,515,679; `docs/evidence/effects.md` L146,207; `pipelines/Wardogs_DamagePipeline_v2.md` L1123; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L259 |
| `0x6b83360`–`0x6b834c2` | stub | no | `docs/evidence/effects.md` L147; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L271 |
| `0x6b83560`–`0x6b8358c` | stub | no | `docs/evidence/effects.md` L148; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L272 |
| `0x6b84e80`–`0x6b852ff` | stub | no | `content/Wardogs_Weapons_v2.md` L303; `docs/evidence/weapons.md` L100,121,211 |
| `0x6b85d30`–`0x6b860ca` | stub | no | `content/Wardogs_Weapons_v2.md` L243; `docs/evidence/weapons.md` L122,180; `docs/gap_resolution/RESEARCH_REGISTER.md` L51 |
| `0x6b86480`–`0x6b8685e` | stub | no | `docs/evidence/weapons.md` L161,162,239,260… |
| `0x6b86860`–`0x6b8699a` | stub | no | `content/Wardogs_Weapons_v2.md` L303; `docs/evidence/weapons.md` L124 |
| `0x6b89bb0`–`0x6b8a2ee` | stub | no | `content/Wardogs_Weapons_v2.md` L247,248; `docs/evidence/weapons.md` L134,135; `docs/gap_resolution/RESEARCH_REGISTER.md` L51 |
| `0x6b8a2f0`–`0x6b8a6f8` | stub | no | `content/Wardogs_Weapons_v2.md` L330; `docs/evidence/weapons.md` L136 |
| `0x6b8a700`–`0x6b8a8cf` | stub | no | `content/Wardogs_Weapons_v2.md` L322; `docs/evidence/weapons.md` L137 |
| `0x6b94700`–`0x6b95149` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L201 |
| `0x6b95c50`–`0x6b95e4f` | stub | no | `content/Wardogs_Weapons_v2.md` L238,334; `docs/evidence/weapons.md` L52,53,141,142; `docs/gap_resolution/RESEARCH_REGISTER.md` L51 |
| `0x6b99ab0`–`0x6b99aed` | stub | no | `game-features/Wardogs_GameFeatures_Weapons_v2.md` L201 |
| `0x6bb7e10`–`0x6bb80ce` | stub | no | `docs/evidence/damage.md` L318,545,592; `pipelines/Wardogs_DamagePipeline_v2.md` L708,1163 |
| `0x6bb8d00`–`0x6bb8d3c` | stub | no | `content/Wardogs_GameMechanics_v2.md` L73; `docs/WHAT_IS_LEFT.md` L69; `docs/evidence/round8-armor.md` L178; `pipelines/infantry-viewer.md` L81,345 |
| `0x6bb8d40`–`0x6bb8d86` | stub | no | `content/Wardogs_GameMechanics_v2.md` L92; `pipelines/infantry-viewer.md` L81,346 |
| `0x6bb97b0`–`0x6bb9850` | stub | no | `docs/evidence/round10-vehicle-blast-audit.md` L43 |
| `0x6c168f0`–`0x6c16981` | stub | no | `docs/evidence/round8-ancillary-sights.md` L192,259 |
| `0x6c2a5f0`–`0x6c2a790` | stub | no | `docs/ROUND11_STATUS.md` L1196; `docs/evidence/damage.md` L549; `docs/evidence/vehicles.md` L208; `pipelines/Wardogs_DamagePipeline_v2.md` L249,1092; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L58 |
| `0x6c2a790`–`0x6c2aa47` | stub | no | `docs/ROUND11_STATUS.md` L1294; `docs/evidence/damage.md` L550,556,681; `docs/evidence/round10-native-vehicle-sampling.md` L25,63; `docs/evidence/round8-radial.md` L87; `docs/evidence/vehicles.md` L209; `pipelines/Wardogs_DamagePipeline_v2.md` L116; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L676 |
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
| `0x6c977b0`–`0x6c9783d` | stub | no | `content/Wardogs_Weapons_v2.md` L338; `docs/evidence/round8-ancillary-sights.md` L188,189,190,233… |
| `0x6c97840`–`0x6c978f2` | stub | no | `docs/evidence/round8-ancillary-sights.md` L129 |
| `0x6c979a0`–`0x6c979ef` | stub | no | `content/Wardogs_Weapons_v2.md` L241; `docs/evidence/weapons.md` L145 |
| `0x6c98290`–`0x6c986f4` | stub | no | `docs/evidence/damage.md` L418,551,552,680…; `docs/evidence/round8-weapon-context.md` L90,91,191,260…; `docs/evidence/vehicles.md` L210; `pipelines/Wardogs_DamagePipeline_v2.md` L944,949,1228; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1005; `pipelines/infantry-viewer.md` L368 |
| `0x6c989a0`–`0x6c989ef` | stub | no | `content/Wardogs_Weapons_v2.md` L241; `docs/evidence/weapons.md` L146 |
| `0x6ca1ae0`–`0x6ca1b74` | stub | no | `docs/evidence/effects.md` L56,160,219; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L367 |
| `0x6ca7800`–`0x6ca7e2f` | stub | no | `docs/evidence/round17-native-defaults.md` L20,28,29,30…; `docs/evidence/round8-explosive-actors.md` L47,49; `docs/evidence/round8-impact.md` L32,33; `docs/evidence/round8-radial.md` L129 |
| `0x6cf5370`–`0x6cf541e` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L90; `docs/evidence/round8-loadout.md` L393 |
| `0x6d58a10`–`0x6d58d73` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L85,131 |
| `0x6d6b260`–`0x6d6b30e` | stub | no | `docs/evidence/round8-loadout.md` L294 |
| `0x6d6b890`–`0x6d6b9cd` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L81 |
| `0x6d6bb00`–`0x6d6bc06` | stub | no | `docs/evidence/round8-loadout.md` L211,219,220 |
| `0x6d6bf70`–`0x6d6c101` | stub | no | `docs/evidence/round8-loadout.md` L211 |
| `0x6e6d580`–`0x6e6d8b6` | stub | no | `docs/evidence/round8-impact.md` L89,98 |
| `0x6e6dcc0`–`0x6e6dd8b` | stub | no | `docs/evidence/damage.md` L556,681; `docs/evidence/round8-radial.md` L87; `pipelines/Wardogs_DamagePipeline_v2.md` L114,116; `pipelines/infantry-viewer.md` L348,366 |
| `0x6e6e170`–`0x6e6e252` | stub | no | `docs/evidence/round8-armor.md` L30,31,49 |
| `0x6e7e530`–`0x6e7ed8b` | stub | no | `docs/evidence/round8-radial-mutable-topology.md` L18 |
| `0x6e7f0b0`–`0x6e7f1b6` | stub | no | `docs/evidence/damage.md` L561; `pipelines/Wardogs_DamagePipeline_v2.md` L1104 |
| `0x6e7f420`–`0x6e7f562` | stub | no | `docs/evidence/damage.md` L562; `pipelines/Wardogs_DamagePipeline_v2.md` L1106 |
| `0x6e7fa00`–`0x6e802a6` | stub | no | `docs/evidence/round8-radial-mutable-topology.md` L22; `docs/evidence/round8-radial-points-components.md` L88,98 |
| `0x6ef2f70`–`0x6ef30b7` | stub | no | `docs/evidence/round8-armor.md` L166,168; `pipelines/Wardogs_DamagePipeline_v2.md` L800 |
| `0x6ef30bd`–`0x6ef324e` | stub | no | `docs/evidence/damage.md` L379; `docs/evidence/round8-armor.md` L166,167,168; `pipelines/Wardogs_DamagePipeline_v2.md` L801 |
| `0x6f1ffa0`–`0x6f200da` | stub | no | `docs/evidence/round8-exploding-gate.md` L16 |
| `0x6f34110`–`0x6f341af` | stub | no | `docs/evidence/round8-exploding-gate.md` L18 |
| `0x6f37c00`–`0x6f38092` | stub | no | `docs/evidence/round8-physical-material-downstream.md` L135 |
| `0x6fa5970`–`0x6fa59c8` | stub | no | `docs/evidence/round8-loadout-frontend.md` L20 |
| `0x756e790`–`0x756eabb` | stub | no | `docs/evidence/round8-loadout-deathmatch.md` L75,76 |
| `0x76384e0`–`0x763877a` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L82 |
| `0x76423a0`–`0x764244e` | stub | no | `docs/evidence/round8-weaponowner-imports.md` L130 |
| `0x7642580`–`0x7642956` | stub | no | `docs/evidence/round8-weapon-context.md` L24 |
| `0x76448d0`–`0x76449b3` | stub | no | `docs/evidence/round8-weapon-context.md` L285,287 |
| `0x7645a30`–`0x76460c0` | stub | no | `docs/evidence/round8-weapon-context.md` L190,270,273,274…; `pipelines/infantry-viewer.md` L368 |
| `0x7646710`–`0x764686e` | stub | no | `docs/evidence/round8-weapon-context.md` L290 |
| `0x7647680`–`0x764785d` | stub | no | `docs/evidence/round8-weapon-context.md` L286 |
| `0x76478d0`–`0x7647e89` | stub | no | `docs/evidence/round8-weapon-context.md` L26,28,34; `pipelines/infantry-viewer.md` L360 |
| `0x767b9b0`–`0x767bc33` | stub | no | `docs/evidence/round8-spw-collision-inputs.md` L168 |
| `0x767bc40`–`0x767cdc4` | stub | no | `docs/ROUND11_STATUS.md` L1439; `docs/evidence/vehicles.md` L231,289; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L71,1136 |
| `0x76a18f0`–`0x76a1aff` | stub | no | `docs/evidence/round17-native-defaults.md` L58,82,83,84… |
| `0x76a36b0`–`0x76a3993` | stub | no | `docs/evidence/round8-rotor-toggle.md` L48 |
| `0x76a8510`–`0x76a8868` | stub | no | `docs/evidence/round8-weapon-context.md` L283 |
| `0x76c3eb0`–`0x76c3ffb` | stub | no | `docs/evidence/round8-backblast.md` L59,61,73; `pipelines/Wardogs_DamagePipeline_v2.md` L316; `pipelines/infantry-viewer.md` L359 |
| `0x76cab80`–`0x76cb132` | stub | no | `docs/evidence/round8-exploding-gate.md` L69,73,75,78 |
| `0x76cfeb0`–`0x76d04f6` | stub | no | `docs/evidence/round8-exploding-gate.md` L22,25,26,40…; `pipelines/infantry-viewer.md` L364 |
| `0x7741ab0`–`0x7741cab` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L81 |
| `0x8584cc0`–`0x8585019` | stub | no | `docs/evidence/round17-native-defaults.md` L178,184,185,186… |
| `0x863b270`–`0x863b54a` | stub | no | `docs/evidence/round12-spawn-provisioning.md` L84 |
| `0x869bf50`–`0x869bfcb` | stub | no | `docs/evidence/round17-native-defaults.md` L55 |
| `0x869bff0`–`0x869c1f9` | stub | no | `docs/evidence/round17-native-defaults.md` L59,65 |
| `0x977e560`–`0x977ef14` | stub | no | `docs/evidence/damage.md` L46,653 |
| `0x42333f0`–`0x42336d6` | differs; reverified r19 (a) unaffected: function bytes identical, page difference is the previous function's tail | no | `docs/evidence/round8-tapered-query.md` L53,69,70; `pipelines/infantry-viewer.md` L362 |
| `0x44176d0`–`0x441772e` | differs; reverified r19 (a) unaffected: function bytes identical, page difference is the previous function's tail | no | `docs/ROUND11_STATUS.md` L655 |
| `0x1921820` | stub | - | `docs/evidence/weapons.md` L142 |
| `0x1c051c0` | stub | - | `docs/evidence/effects.md` L166 |
| `0x246f800` | stub | - | `docs/ROUND11_STATUS.md` L312 |
| `0x2470310` | stub | - | `docs/ROUND11_STATUS.md` L835 |
| `0x395baf0` | stub | - | `docs/evidence/round8-ancillary-sights.md` L260 |
| `0x3c95c30` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L20; `docs/evidence/vehicles.md` L203 |
| `0x3c95c61` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L20 |
| `0x3ca8630` | stub | - | `docs/evidence/effects.md` L90,100,184,195; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L316 |
| `0x3cadbd0` | stub | - | `docs/ROUND11_STATUS.md` L164 |
| `0x3d6e200` | stub | - | `docs/ROUND11_STATUS.md` L639 |
| `0x41e0ea0` | stub | - | `docs/evidence/round8-tapered-query.md` L54 |
| `0x4244430` | stub | - | `docs/evidence/round8-tapered-query.md` L24 |
| `0x44c2ba0` | stub | - | `docs/evidence/round10-native-vehicle-sampling.md` L20; `docs/evidence/round8-gepard-collision-inputs.md` L38,39 |
| `0x44c2bd0` | stub | - | `docs/evidence/round8-gepard-collision-inputs.md` L39 |
| `0x46dbb20` | stub | - | `docs/evidence/round8-loadout-rebuy.md` L123 |
| `0x50bf500` | stub | - | `docs/ROUND11_STATUS.md` L119,579; `docs/evidence/vehicles.md` L136,301; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L545 |
| `0x50bf880` | stub | - | `docs/evidence/vehicles.md` L136,137,138,262…; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L203,516,635,1037 |
| `0x50bf9fd` | stub | - | `docs/evidence/round8-vehicle-sweep.md` L18; `docs/evidence/vehicles.md` L138; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L580 |
| `0x50e08c0` | stub | - | `docs/ROUND11_STATUS.md` L95; `docs/evidence/round8-stn06-attachments.md` L21,22 |
| `0x50e08c5` | stub | - | `docs/evidence/round8-stn06-attachments.md` L23; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L276 |
| `0x52301f0` | stub | - | `docs/ROUND11_STATUS.md` L920; `docs/evidence/weapons.md` L148 |
| `0x5230c80` | stub | - | `docs/evidence/effects.md` L60,120,233; `pipelines/Wardogs_GameplayEffectsPipeline_v1.md` L229 |
| `0x532d120` | stub | - | `docs/evidence/round8-rotor-toggle.md` L69,70 |
| `0x532d17a` | stub | - | `docs/evidence/round8-rotor-toggle.md` L70 |
| `0x532d180` | stub | - | `docs/evidence/round8-rotor-toggle.md` L49,58 |
| `0x532d1b0` | stub | - | `docs/evidence/round8-rotor-toggle.md` L49 |
| `0x53cae20` | stub | - | `docs/evidence/round8-loadout-buffer-layout.md` L28; `docs/evidence/round8-loadout-deathmatch.md` L31; `docs/evidence/round8-loadout-restore.md` L75; `docs/evidence/round8-weapon-context.md` L113 |
| `0x67912b0` | stub | - | `docs/evidence/round8-loadout.md` L189 |
| `0x6b18e70` | stub | - | `docs/evidence/round8-radial.md` L133; `docs/evidence/vehicles.md` L196,286; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L72 |
| `0x6b86470` | stub | - | `content/Wardogs_Weapons_v2.md` L303; `docs/evidence/weapons.md` L123,236,237 |
| `0x6bb9850` | stub | - | `docs/evidence/round10-vehicle-blast-audit.md` L47; `docs/evidence/round8-explosive-actors.md` L48; `docs/evidence/round8-radial.md` L129 |
| `0x6bb9858` | stub | - | `docs/evidence/round8-explosive-actors.md` L51 |
| `0x6bb9883` | stub | - | `docs/evidence/round8-explosive-actors.md` L51 |
| `0x6bb9888` | stub | - | `docs/evidence/round10-vehicle-blast-audit.md` L48; `docs/evidence/round8-explosive-actors.md` L52 |
| `0x6bbd5b0` | stub | - | `docs/evidence/weapons.md` L179,261 |
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
| `0x6e6eba0` | stub | - | `docs/evidence/damage.md` L517,557,681; `docs/evidence/vehicles.md` L204,212; `pipelines/Wardogs_DamagePipeline_v2.md` L217,1086; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L1008 |
| `0x74f72e0` | stub | - | `docs/evidence/round8-exploding-gate.md` L28 |
| `0x76449c0` | stub | - | `docs/evidence/round8-weapon-context.md` L110 |
| `0x76ab5f0` | stub | - | `docs/WHAT_IS_LEFT.md` L122; `docs/evidence/vehicles.md` L66,236,314; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` L615 |

## Byte-level comparison

The own bytes of each cited function that has a corpus row in `.text` were compared between the analysis image and the reference image (file offsets from each image's `.text` section). For the functions in the 'stub' and 'differs' categories the immediately preceding corpus function was compared the same way.

| Measure | Count |
|---|---:|
| Cited functions in `.text` (distinct corpus rows) | 896 |
| Cited addresses with no function row (not compared) | 441 |
| Own bytes identical | 888 |
| Own bytes differ (any category) | 8 |
| Not comparable (range outside the reference `.text`) | 0 |
| Own bytes differ, category 'unknown' (page not in the recovered table) | 0 |
| Category clean | 663 |
| Category stub or differs | 207 |
| &nbsp;&nbsp;of which own bytes differ | 8 |
| &nbsp;&nbsp;of which own bytes identical | 199 |
| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in a corpus row whose own bytes differ | 106 |
| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in no corpus row | 93 |
| &nbsp;&nbsp;&nbsp;&nbsp;other | 0 |
| &nbsp;&nbsp;&nbsp;&nbsp;(immediately preceding row has differing own bytes, for reference) | 4 |

Cited functions whose own bytes differ between the images (8 rows, by start address; at most 60 shown). 'Preceding' is the corpus function immediately below the cited start, with its own-bytes status.

| Function | Category | Stub in body | Differing own bytes (first rva) | Preceding function | Preceding own bytes | Cited at |
|---|---|---|---|---|---|---|
| `0x395be30`–`0x395beb9` | stub | yes | 132 (`0x395be31`) | `0x395bd50`–`0x395be2a` | same | `content/Wardogs_WeaponAttributes_v1.md:79`; `content/Wardogs_WeaponAttributes_v1.md:83` +6 |
| `0x4232fd0`–`0x4233054` | stub | yes | 130 (`0x4232fd1`) | `0x4232700`–`0x4232fc4` | same | `docs/evidence/round8-tapered-query.md:87` |
| `0x4416ff0`–`0x4417060` | stub | yes | 109 (`0x4416ff0`) | `0x4416f50`–`0x4416fe9` | same | `docs/ROUND11_STATUS.md:665` |
| `0x5230be0`–`0x5230c39` | stub | yes | 85 (`0x5230be2`) | `0x5230b80`–`0x5230bd9` | differs | `docs/ROUND11_STATUS.md:1183`; `docs/ROUND11_STATUS.md:1185` |
| `0x6b74e30`–`0x6b74f79` | stub | yes | 319 (`0x6b74e30`) | `0x6b747f0`–`0x6b74e28` | same | `docs/evidence/round8-weapon-context.md:31`; `docs/evidence/round8-weapon-context.md:35` +1 |
| `0x6b8ac90`–`0x6b8acaf` | stub | yes | 26 (`0x6b8ac92`) | `0x6b8ac60`–`0x6b8ac81` | differs | `content/Wardogs_Weapons_v2.md:330`; `content/Wardogs_Weapons_v2.md:332` +2 |
| `0x6b99300`–`0x6b99320` | stub | yes | 29 (`0x6b99302`) | `0x6b99270`–`0x6b992f9` | same | `game-features/Wardogs_GameFeatures_Weapons_v2.md:209` |
| `0x6bb8970`–`0x6bb89a3` | stub | yes | 47 (`0x6bb8972`) | `0x6bb8900`–`0x6bb8969` | same | `docs/ROUND11_STATUS.md:980`; `docs/ROUND11_STATUS.md:988` +4 |

Reading the section. The eight rows with differing own bytes are all stub-bodied functions, so the difference is the dispatch stub that replaces the body in the analysis image. Every cited function whose category is clean or unknown has identical own bytes.

Of the 199 stub or differs functions whose own bytes are identical, 106 have differing bytes outside their range inside a corpus row whose own bytes differ. This covers the two round 19 cases: `0x42333f0` and `0x44176d0` differ only in the tail of the stub functions `0x4232fd0` and `0x4416ff0`, which share their page. Only four of them have a differing immediately preceding row (`0x157c320`, `0x15b83b0`, `0x2f691e0`, `0x538abd0`). For the other 93, the differing bytes lie in no corpus row, so this check does not attribute them. They are an open question about the protection layer's byte layout, not evidence that a claim is wrong.

Method: `_tools/ida_claim_bytes.py` (sibling of `_tools/ida_claim_exposure.py`, which supplies the page classes and the citation list). Run `python -I _tools/ida_claim_bytes.py` for this section, or add `--tsv` for one line per cited function.
