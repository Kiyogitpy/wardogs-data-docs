---
title: "Data Tables & Tags changes"
parent: "Season 2 Changes"
nav_order: 6
description: "Data table and tag changes from Season 1 to Season 2: 12 assets added, 51 modified with real changes, 325 property changes, including attachment and gear market prices."
---

# Data Tables & Tags changes

{{ page.description }}

Counts come from `assets/data/season-diff/index.json` and `data-tables-tags.json`. Values are copied as stored. Signed deltas and percentages are calculated from the stored values. Noise-only assets are skipped.

| Measure | Count |
|---|---|
| Assets added | 12 |
| Assets removed | 0 |
| Assets modified with real changes | 51 |
| Assets modified, noise only (skipped) | 21 |
| Assets moved | 0 |
| Property changes (index.json) | 325 |

The change list holds 325 records. The index figure equals that total minus `removed_values` (0).

## Headline changes

### Prices and numeric values

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_Setting_Controls_LookAccelMaxMultiplier | Parameters.Minimum | 0.5 | 1.2 | +0.7 (+140.0%) |
| DA_Setting_Controls_LookAccelMaxMultiplier | Parameters.Maximum | 10.0 | 5.0 | −5.0 (−50.0%) |
| DA_Setting_Controls_LookAccelMaxMultiplier | Parameters.Default | 1.6 | 1.5 | −0.1 (−6.3%) |
| DA_Setting_Controls_LookAccelMaxMultiplier | Parameters.DisplayMinimum | 1.0 | 1.2 | +0.2 (+20.0%) |
| DA_Setting_Controls_LookAccelMaxMultiplier | Parameters.DisplayMaximum | 3.0 | 5.0 | +2.0 (+66.7%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_04.VendorItemVariations[Id.Item.MZL_04].Price | 1800.0 | 1450.0 | −350.0 (−19.4%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_07.VendorItemVariations[Id.Item.MZL_07].Price | 1350.0 | 1200.0 | −150.0 (−11.1%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_05.VendorItemVariations[Id.Item.MZL_05].Price | 1220.0 | 1090.0 | −130.0 (−10.7%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_06.VendorItemVariations[Id.Item.MZL_06].Price | 1040.0 | 1170.0 | +130.0 (+12.5%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_08.VendorItemVariations[Id.Item.MZL_08].Price | 1210.0 | 1180.0 | −30.0 (−2.5%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_09.VendorItemVariations[Id.Item.MZL_09].Price | 1300.0 | 1260.0 | −40.0 (−3.1%) |
| DT_AttachmentMarket | Rows.Id.Item.MZL_10.VendorItemVariations[Id.Item.MZL_10].Price | 1190.0 | 1160.0 | −30.0 (−2.5%) |
| DT_AttachmentMarket | Rows.Id.Item.FGP_02.VendorItemVariations[Id.Item.FGP_02].Price | 1000.0 | 820.0 | −180.0 (−18.0%) |
| DT_AttachmentMarket | Rows.Id.Item.FGP_03.VendorItemVariations[Id.Item.FGP_03].Price | 820.0 | 800.0 | −20.0 (−2.4%) |
| DT_GearMarket | …LargeBackpack.VendorItemVariations[Id.Item.LargeBackpack].Price | 2400.0 | 1600.0 | −800.0 (−33.3%) |
| DT_GearMarket | …LargeSlingBackpack.VendorItemVariations[Id.Item.LargeSlingBackpack].Price | 3500.0 | 2400.0 | −1100.0 (−31.4%) |
| DT_GearMarket | …ExtraLargeSlingBackpack.VendorItemVariations[Id.Item.ExtraLargeSlingBackpack].Price | 5000.0 | 4000.0 | −1000.0 (−20.0%) |

Attachment market `MZL_04` price: 1800.0 → 1450.0 (−350.0, −19.4%). Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=data-tables-tags&q=DT_AttachmentMarket

### Changed records by table

Non-numeric records (tags, text keys, flags and asset paths) for the largest tables. A row with "added" or "removed" has no value on the other side.

#### DT_WeaponMarket (50 records, 50 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_WeaponMarket | Rows.Id.Item.STANAGMagazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.ID.Item.A91Mag.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.M4Magazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.ID.Item.TAR21Mag.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.AK74MMagazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.AK74MExtendedMagazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.AK74MMagazine75rnd.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.M249Magazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.RFBMagazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.Glock17Magazine.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.LeapordBarrel.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | …762mm.VendorItemVariations[Id.Item.762mm.Tracer].bIsPreviewOnly | false | true | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.762mm.Tracer].VendorSlotTag.TagName | None | Inventory.Slot.Attachment.Ammo | changed |
| DT_WeaponMarket | …762mm.VendorItemVariations[Id.Item.762mm.HollowPoint.Tracer].bIsPreviewOnly | false | true | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.762mm.HollowPoint.Tracer].VendorSlotTag.TagName | None | Inventory.Slot.Attachment.Ammo | changed |
| DT_WeaponMarket | …762mm.VendorItemVariations[Id.Item.762mm.ArmorPiercing.Tracer].bIsPreviewOnly | false | true | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.762mm.ArmorPiercing.Tracer].VendorSlotTag.TagName | None | Inventory.Slot.Attachment.Ammo | changed |
| DT_WeaponMarket | Rows.Id.Item.762mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.762x54mm.Categories[2] | — | Vendor.Category.Vehicle.Ammo | added |
| DT_WeaponMarket | …762x54mm.VendorItemVariations[Id.Item.762x54mm.Tracer].Categories[1] | — | Vendor.Category.Vehicle.Ammo | added |
| DT_WeaponMarket | Rows.Id.Item.762x54mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.45Colt.Tracer].OverwrittenIcon.AssetPathName | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/T_UI_Icon_ammobox_45-COLT_FMJ.T_UI_Icon_ammobox… | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/Tracer/T_UI_Icon_ammobox_45COLT_FMJ.T_UI_Icon_a… | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.45Colt.HollowPoint.Tracer].OverwrittenIcon.AssetPathName | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/T_UI_Icon_ammobox_45-COLT_HP.T_UI_Icon_ammobox_… | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/Tracer/T_UI_Icon_ammobox_45COLT_HP.T_UI_Icon_am… | changed |
| DT_WeaponMarket | …VendorItemVariations[Id.Item.45Colt.ArmorPiercing.Tracer].OverwrittenIcon.AssetPathName | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/T_UI_Icon_ammobox_45-COLT_AP.T_UI_Icon_ammobox_… | /Game/UI/Shared/Icons/Equipment/AmmoBoxes/Tracer/T_UI_Icon_ammobox_45COLT_AP.T_UI_Icon_am… | changed |
| DT_WeaponMarket | Rows.Id.Item.45Colt.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.12g.7mmBuck.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.12g.RifledSlug.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.556mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.545mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.9mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.40mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.84mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.45ACP.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.93mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.ID.Item.120x570mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.308Win.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.50Cal.Categories[2] | — | Vendor.Category.Vehicle.Ammo | added |
| DT_WeaponMarket | …50Cal.VendorItemVariations[Id.Item.50Cal.Tracer].Categories[2] | — | Vendor.Category.Vehicle.Ammo | added |
| DT_WeaponMarket | Rows.Id.Item.50Cal.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_WeaponMarket | Rows.Id.Item.762x51mm.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |

Showing 40 of 50. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=data-tables-tags&q=DT_WeaponMarket

#### DT_GameplayTagToText_Categories (30 records, 30 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.TableId | — | /Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor | added |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.Key | 4426A44C42D70B2F7D257B97EB4DC123 | Category.Weapon.MachineGun | changed |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.Heavy].Value.TableId | — | /Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags | added |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.Heavy].Value.Key | 570EE34948FB401898760686A8E7DD23 | Vendor.Category.Ammo.Type.Standard.TaggedText.Heavy | changed |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.Heavy].Value.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.TableId | — | /Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor | added |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.Key | ECE22F0F44A5EE10FEC75AA41EB29D9D | Category.Weapon.MachineGun | changed |
| DT_GameplayTagToText_Categories | …TaggedText[Id.Vehicle.WeaponExtension.TNK_01.MachineGun].Value.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | Rows.Id.Vehicle.WeaponExtension.WHL_08.RingTurret | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor","Key":"Category.… | added |
| DT_GameplayTagToText_Categories | Rows.Id.Vehicle.WeaponExtension.TNK_04.Default | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor","Key":"Category.… | added |
| DT_GameplayTagToText_Categories | Rows.Id.Vehicle.WeaponExtension.TNK_04.MachineGun | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor","Key":"Category.… | added |
| DT_GameplayTagToText_Categories | Rows.Id.Vehicle.WeaponExtension.TNK_04.MountedMachineGun | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_Vendor.STRINGS_Vendor","Key":"Category.… | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Gear.VehicleUse | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags","Key… | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Vehicle.CounterMeasures.Flares.Text.TableId | — | /Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Vehicle.CounterMeasures.Flares.Text.Key | 7A4A4877404864E5A53AF589A1BAABC3 | Item.Category.Flares | changed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Vehicle.CounterMeasures.Flares.Text.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Vehicle.CounterMeasures.Smoke | — | {"Text":{"TableId":"/Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags","Key… | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Small.Text.TableId | — | /Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Small.Text.Key | 866E910A4052A8730B66DB9FCE22D2FB | Vendor.Category.Sub.Vehicle.SupplyCrate.Small.Text | changed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Small.Text.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Large.Text.TableId | — | /Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Large.Text.Key | AA83347F478B8911302C99A85FDFDDB9 | Vendor.Category.Sub.Vehicle.SupplyCrate.Large.Text | changed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.SupplyCrate.Large.Text.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.Pallet.Text.TableId | — | /Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTags | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.Pallet.Text.Key | 11746BE44A02C894CAD79DB3314C516A | Vendor.Category.Sub.Vehicle.Logistics.Pallet.Text | changed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.Pallet.Text.Namespace |  | — | removed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.FOB.Text.TableId | — | /Game/UI/StringTables/STRINGS_Map_Legend.STRINGS_Map_Legend | added |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.FOB.Text.Key | 2CAA449A49014B9928817CAE20206735 | Map.Legend.FOB | changed |
| DT_GameplayTagToText_Categories | Rows.Vendor.Category.Sub.Vehicle.Logistics.FOB.Text.Namespace |  | — | removed |

#### DT_AttachmentMarket (26 records, 17 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_AttachmentMarket | Rows.Id.Item.MZL_04.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_07.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.ID.Item.PWSCQB74Muzzle.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_05.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_06.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_08.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_09.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.MZL_10.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.EotechHoloSight.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.OPT_08.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.4xElcanSpectr.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.SniperScope10x.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.10xScopeMoa.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.RK6ForeGrip.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.FGP_02.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.FGP_04.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_AttachmentMarket | Rows.Id.Item.FGP_03.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |

#### DT_LoadingScreenTips (22 records, 22 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_LoadingScreenTips | Rows.Tip.Inventory.Ammo.Consolidate.LoadingScreenText.SourceString | Use the ammo consolidation button in your inventory to combine rounds of the same calibre… | Use the ammo consolidation button in your inventory to combine rounds of the same caliber… | changed |
| DT_LoadingScreenTips | Rows.Tip.Inventory.Ammo.Consolidate.LoadingScreenText.LocalizedString | Use the ammo consolidation button in your inventory to combine rounds of the same calibre… | Use the ammo consolidation button in your inventory to combine rounds of the same caliber… | changed |
| DT_LoadingScreenTips | Rows.Tip.Health.HealthBar.LoadingScreenText.SourceString | Your current health is displayed in a bar at the bottom right of the screen. Keep an eye … | Your current health is displayed in a bar at the bottom right of the screen. Keep an eye … | changed |
| DT_LoadingScreenTips | Rows.Tip.Health.HealthBar.LoadingScreenText.LocalizedString | Your current health is displayed in a bar at the bottom right of the screen. Keep an eye … | Your current health is displayed in a bar at the bottom right of the screen. Keep an eye … | changed |
| DT_LoadingScreenTips | Rows.Tip.Inventory.Ammo.Combine.LoadingScreenText.SourceString | Use the combine ammo button in your inventory to combine rounds of the same calibre, maxi… | Use the combine ammo button in your inventory to combine rounds of the same caliber, maxi… | changed |
| DT_LoadingScreenTips | Rows.Tip.Inventory.Ammo.Combine.LoadingScreenText.LocalizedString | Use the combine ammo button in your inventory to combine rounds of the same calibre, maxi… | Use the combine ammo button in your inventory to combine rounds of the same caliber, maxi… | changed |
| DT_LoadingScreenTips | Rows.Tip.Economy.Armour.WaitForRevive.LoadingScreenText.SourceString | Your armour will likely outlive you. You might be throwing money away by respawning - con… | Your armor will likely outlive you. You might be throwing money away by respawning - cons… | changed |
| DT_LoadingScreenTips | …WaitForRevive.LoadingScreenText.LocalizedString | Your armour will likely outlive you. You might be throwing money away by respawning - con… | Your armor will likely outlive you. You might be throwing money away by respawning - cons… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Ammo.HollowPoint.LoadingScreenText.SourceString | "Flesh Damage" Hollow Point (HP) ammo is particularly effective at damaging non-armoured … | "Flesh Damage" Hollow Point (HP) ammo is particularly effective at damaging non-armored b… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Ammo.HollowPoint.LoadingScreenText.LocalizedString | "Flesh Damage" Hollow Point (HP) ammo is particularly effective at damaging non-armoured … | "Flesh Damage" Hollow Point (HP) ammo is particularly effective at damaging non-armored b… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Ammo.ArmourPiercing.LoadingScreenText.SourceString | Armour Piercing (AP) ammo is effective at penetrating armour. | Armor Piercing (AP) ammo is effective at penetrating armor. | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Ammo.ArmourPiercing.LoadingScreenText.LocalizedString | Armour Piercing (AP) ammo is effective at penetrating armour. | Armor Piercing (AP) ammo is effective at penetrating armor. | changed |
| DT_LoadingScreenTips | Rows.Tip.ControlZone.DrillTowers.Loot.LoadingScreenText.SourceString | Drill towers have randomised helpful equipment that spawn on their roofs - consider looti… | Drill towers have randomized helpful equipment that spawn on their roofs - consider looti… | changed |
| DT_LoadingScreenTips | …Loot.LoadingScreenText.LocalizedString | Drill towers have randomised helpful equipment that spawn on their roofs - consider looti… | Drill towers have randomized helpful equipment that spawn on their roofs - consider looti… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.TargetLimbs.LoadingScreenText.SourceString | Think before you pull the trigger - sometimes it makes sense to shoot unarmoured limbs th… | Think before you pull the trigger - sometimes it makes sense to shoot unarmored limbs tha… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.TargetLimbs.LoadingScreenText.LocalizedString | Think before you pull the trigger - sometimes it makes sense to shoot unarmoured limbs th… | Think before you pull the trigger - sometimes it makes sense to shoot unarmored limbs tha… | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Suppression.LoadingScreenText.SourceString | Suppression can be effective at stopping players peeking angles - consider firing toward … | Suppression can be effective at stopping players peeking angles - consider firing toward … | changed |
| DT_LoadingScreenTips | Rows.Tip.Combat.Suppression.LoadingScreenText.LocalizedString | Suppression can be effective at stopping players peeking angles - consider firing toward … | Suppression can be effective at stopping players peeking angles - consider firing toward … | changed |
| DT_LoadingScreenTips | Rows.Tip.Items.Gear.Armour.LoadingScreenText.SourceString | Helmets and armour reduce damage from gunfire. Superior armor covers more of the body and… | Helmets and armor reduce damage from gunfire. Superior armor covers more of the body and … | changed |
| DT_LoadingScreenTips | Rows.Tip.Items.Gear.Armour.LoadingScreenText.LocalizedString | Helmets and armour reduce damage from gunfire. Superior armor covers more of the body and… | Helmets and armor reduce damage from gunfire. Superior armor covers more of the body and … | changed |
| DT_LoadingScreenTips | Rows.Tip.Items.Weapons.Purchasing.LoadingScreenText.SourceString | Interact with the Equipment Vendor, open the weapons tab, and pick your weapon. Use filte… | Interact with the Equipment Vendor, open the weapons tab, and pick your weapon. Use filte… | changed |
| DT_LoadingScreenTips | Rows.Tip.Items.Weapons.Purchasing.LoadingScreenText.LocalizedString | Interact with the Equipment Vendor, open the weapons tab, and pick your weapon. Use filte… | Interact with the Equipment Vendor, open the weapons tab, and pick your weapon. Use filte… | changed |

#### DT_ExperienceServerBrowserTags (19 records, 19 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.InfantryOnly | — | {"DescriptorTags":["Server.Descriptor.InfantryOnly"],"_aaabmndfbjeemaenllmhj":[],"Tag":{"… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.Hardcore | — | {"DescriptorTags":["Server.Descriptor.Hardcore"],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagN… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.AutoAssignFactions | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.AutoA… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.AutoAssignFirstFaction | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.AutoA… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.ChangeTeamDisabled | — | {"DescriptorTags":["Server.Descriptor.ChangeTeamDisabled"],"_aaabmndfbjeemaenllmhj":[],"T… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.ChatboxDisabled | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.Chatb… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.ControlZoneRequiresTag | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.Contr… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.EnablePresenceJoinOnExperienceLoad | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.Enabl… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.FreeForAll | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.FreeF… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.GiveUpDisabled | — | {"DescriptorTags":["Server.Descriptor.GiveUpDisabled"],"_aaabmndfbjeemaenllmhj":[],"Tag":… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.KillfeedSquadOnly | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.KillfeedSquadOnly"],"_aaabmndfbjeemaenll… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.NoCashFeed | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.CashFeed"],"_aaabmndfbjeemaenllmhj":[],"… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.VaultEnabled | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":[],"Tag":{"TagName":"Experience.Rules.Vault… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.NoDynamicCrosshair | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.DynamicCrosshair"],"_aaabmndfbjeemaenllm… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.NoHudAmmo | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.HudAmmo"],"_aaabmndfbjeemaenllmhj":[],"T… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.NoMinimapHealth | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.MinimapHealth"],"_aaabmndfbjeemaenllmhj"… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.NoQuickSlots | — | {"DescriptorTags":["Server.Descriptor.ReducedHUD.QuickSlots"],"_aaabmndfbjeemaenllmhj":[]… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.RebuyDisabled | — | {"DescriptorTags":["Server.Descriptor.RebuyDisabled"],"_aaabmndfbjeemaenllmhj":[],"Tag":{… | added |
| DT_ExperienceServerBrowserTags | Rows.Experience.Rules.SkipPlayerDeathItemDrop | — | {"DescriptorTags":[],"_aaabmndfbjeemaenllmhj":["Server.Descriptor.PlayerLootingDisabled"]… | added |

#### DT_Settings_Controls (19 records, 19 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_Settings_Controls | …UIData.Description.SourceString | The response curve used to determine the behaviour of the gamepad axis | The response curve used to determine the behavior of the gamepad axis. | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | The response curve used to determine the behaviour of the gamepad axis | The response curve used to determine the behavior of the gamepad axis. | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Multiplier applied to the Aim Assist strength, set to 0 to disable Aim Assist | Multiplier applied to the Aim Assist strength. Set to 0 to disable (Default = 1). | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Multiplier applied to the Aim Assist strength, set to 0 to disable Aim Assist | Multiplier applied to the Aim Assist strength. Set to 0 to disable (Default = 1). | changed |
| DT_Settings_Controls | …UIData.DisplayName.SourceString | Move Stick Centre | Move Stick Center | changed |
| DT_Settings_Controls | …UIData.DisplayName.LocalizedString | Move Stick Centre | Move Stick Center | changed |
| DT_Settings_Controls | …UIData.DisplayName.SourceString | Look Stick Centre | Look Stick Center | changed |
| DT_Settings_Controls | …UIData.DisplayName.LocalizedString | Look Stick Centre | Look Stick Center | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Limits extreme pitch, yaw and collective inputs to keep the aircraft within a safe flight… | Limits extreme pitch, yaw and collective inputs to keep the aircraft within a safe flight… | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Limits extreme pitch, yaw and collective inputs to keep the aircraft within a safe flight… | Limits extreme pitch, yaw and collective inputs to keep the aircraft within a safe flight… | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Ignores small stick movement near centre on the roll axis, so a resting stick stays neutr… | Ignores small stick movement near center on the roll axis, so a resting stick stays neutr… | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Ignores small stick movement near centre on the roll axis, so a resting stick stays neutr… | Ignores small stick movement near center on the roll axis, so a resting stick stays neutr… | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Ignores small stick movement near centre on the pitch axis, so a resting stick stays neut… | Ignores small stick movement near center on the pitch axis, so a resting stick stays neut… | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Ignores small stick movement near centre on the pitch axis, so a resting stick stays neut… | Ignores small stick movement near center on the pitch axis, so a resting stick stays neut… | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Ignores small stick movement near centre on the yaw axis, so a resting stick stays neutra… | Ignores small stick movement near center on the yaw axis, so a resting stick stays neutra… | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Ignores small stick movement near centre on the yaw axis, so a resting stick stays neutra… | Ignores small stick movement near center on the yaw axis, so a resting stick stays neutra… | changed |
| DT_Settings_Controls | …UIData.Description.SourceString | Ignores small stick movement near centre on the collective axis, so a resting lever stays… | Ignores small stick movement near center on the collective axis, so a resting lever stays… | changed |
| DT_Settings_Controls | …UIData.Description.LocalizedString | Ignores small stick movement near centre on the collective axis, so a resting lever stays… | Ignores small stick movement near center on the collective axis, so a resting lever stays… | changed |
| DT_Settings_Controls | Rows.UserSettings.Controls.Vehicle.Air.FreeLookAbsolute | — | {"UIData":{"DisplayName":{"Namespace":"","Key":"3695E1E54B7F1D690D5C5E89CF2A7509","Source… | added |

#### DT_GearMarket (16 records, 13 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_GearMarket | Rows.Id.Item.SmallTacVest.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.MediumTacVest.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.LargeTacVest.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.Pouch.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.SmallBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.BPAK_005.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.MediumBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.LargeBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.MediumSlingBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.BPAK_006.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.LargeSlingBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | Rows.Id.Item.BPAK_007.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |
| DT_GearMarket | …ExtraLargeSlingBackpack.PurchaseCompletedAudioEvent.TagName | None | Audio.Event.UI.InGame.Vendor.Purchase | changed |

#### DT_Settings_Keybindings (16 records, 16 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_Settings_Keybindings | Rows.Input.NamedActions.Player.Focus.UIData.Description.SourceString | The button used to focus / hold breath whilst aiming down sights. | The button used to focus / hold breath while aiming down sights. | changed |
| DT_Settings_Keybindings | …UIData.Description.LocalizedString | The button used to focus / hold breath whilst aiming down sights. | The button used to focus / hold breath while aiming down sights. | changed |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.FireCountermeasures | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | …UIData.Description.SourceString | The button used to fire whilst in control of a a vehicle's weapon. | The button used to fire while in control of a vehicle's weapon. | changed |
| DT_Settings_Keybindings | …UIData.Description.LocalizedString | The button used to fire whilst in control of a a vehicle's weapon. | The button used to fire while in control of a vehicle's weapon. | changed |
| DT_Settings_Keybindings | …UIData.Description.SourceString | The button used to toggle the bipod atttached to the weapon to fold/unfold. | The button used to toggle the bipod attached to the weapon to fold/unfold. | changed |
| DT_Settings_Keybindings | …UIData.Description.LocalizedString | The button used to toggle the bipod atttached to the weapon to fold/unfold. | The button used to toggle the bipod attached to the weapon to fold/unfold. | changed |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.1 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.2 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.3 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.4 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.5 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.WeaponExtension.Change.6 | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Player.ScopeZoom.Increase | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Player.ScopeZoom.Decrease | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | added |
| DT_Settings_Keybindings | Rows.Input.NamedActions.Vehicle.FireFlares | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_Keybindings.S… | — | removed |

#### DT_OnlineRegions (14 records, 14 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_OnlineRegions | Rows.eu-central | — | {"Endpoint":"dynamodb.eu-central-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/Stri… | added |
| DT_OnlineRegions | Rows.eu-east | — | {"Endpoint":"dynamodb.eu-north-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/String… | added |
| DT_OnlineRegions | Rows.eu-west | — | {"Endpoint":"dynamodb.eu-west-2.amazonaws.com","DisplayName":{"TableId":"/Game/UI/StringT… | added |
| DT_OnlineRegions | Rows.eu-south | — | {"Endpoint":"dynamodb.eu-south-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/String… | added |
| DT_OnlineRegions | Rows.na-central | — | {"Endpoint":"dynamodb.us-east-2.amazonaws.com","DisplayName":{"TableId":"/Game/UI/StringT… | added |
| DT_OnlineRegions | Rows.na-north | — | {"Endpoint":"dynamodb.ca-central-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/Stri… | added |
| DT_OnlineRegions | Rows.na-east | — | {"Endpoint":"dynamodb.us-east-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/StringT… | added |
| DT_OnlineRegions | Rows.na-west | — | {"Endpoint":"dynamodb.us-west-2.amazonaws.com","DisplayName":{"TableId":"/Game/UI/StringT… | added |
| DT_OnlineRegions | Rows.south-america | — | {"Endpoint":"dynamodb.sa-east-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/StringT… | added |
| DT_OnlineRegions | Rows.asia-east | — | {"Endpoint":"dynamodb.ap-northeast-2.amazonaws.com","DisplayName":{"TableId":"/Game/UI/St… | added |
| DT_OnlineRegions | Rows.asia-west | — | {"Endpoint":"dynamodb.ap-south-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/String… | added |
| DT_OnlineRegions | Rows.asia-se | — | {"Endpoint":"dynamodb.ap-southeast-1.amazonaws.com","DisplayName":{"TableId":"/Game/UI/St… | added |
| DT_OnlineRegions | Rows.oceania | — | {"Endpoint":"dynamodb.ap-southeast-2.amazonaws.com","DisplayName":{"TableId":"/Game/UI/St… | added |
| DT_OnlineRegions | Rows.south-africa | — | {"Endpoint":"dynamodb.af-south-1.amazonaws.com","DisplayName":{"Namespace":"","Key":"9078… | added |

#### DT_Settings_General (14 records, 14 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_Settings_General | …UIData.DisplayName.TableId | — | /Game/UI/StringTables/STRINGS_Settings_General.STRINGS_Settings_General | added |
| DT_Settings_General | Rows.UserSettings.General.ChatProfanityFilter.UIData.DisplayName.Key | E888F1924F95939028443A9391DCAC82 | DisplayName.ChatProfanityFilter | changed |
| DT_Settings_General | …UIData.DisplayName.Namespace |  | — | removed |
| DT_Settings_General | …UIData.Description.TableId | — | /Game/UI/StringTables/STRINGS_Settings_General.STRINGS_Settings_General | added |
| DT_Settings_General | Rows.UserSettings.General.ChatProfanityFilter.UIData.Description.Key | E32C1A5A466B6070C4546EB917812758 | Description.ChatProfanityFilter | changed |
| DT_Settings_General | …UIData.Description.Namespace |  | — | removed |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.DisplayName.TableId | — | /Game/UI/StringTables/STRINGS_Settings_General.STRINGS_Settings_General | added |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.DisplayName.Key | C5BDA9F241CB107863AB22B358C425B1 | DisplayName.ScoreboardBadge | changed |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.DisplayName.Namespace |  | — | removed |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.Description.TableId | — | /Game/UI/StringTables/STRINGS_Settings_General.STRINGS_Settings_General | added |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.Description.Key | E77C0C144D3E17F1850216A5523F601F | Description.ScoreboardBadge | changed |
| DT_Settings_General | Rows.UserSettings.General.ScoreboardBadge.UIData.Description.Namespace |  | — | removed |
| DT_Settings_General | Rows.UserSettings.General.AdvancedVehicle.PublicVehicleInventoryAccess | — | {"UIData":{"DisplayName":{"TableId":"/Game/UI/StringTables/STRINGS_Settings_General.STRIN… | added |
| DT_Settings_General | Rows.UserSettings.General.CharacterRenderDisabled | — | {"UIData":{"DisplayName":{"Namespace":"","Key":"2001475B4988176448DF39BF226737D0","Source… | added |

#### DT_EntityData_UI_Items (12 records, 12 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_EntityData_UI_Items | …762x54mm.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRou… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | …ArmorPiercing.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_Chamber… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | …Tracer.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | …HollowPoint.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_Chambered… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | …Tracer.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | …Tracer.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | Rows.ID.Item.35x228mm.Description.SourceString | - High-velocity ballistic rounds  / - Optimised for aerial target engagement | - High-velocity ballistic rounds  / - Optimized for aerial target engagement | changed |
| DT_EntityData_UI_Items | Rows.ID.Item.35x228mm.Description.LocalizedString | - High-velocity ballistic rounds  / - Optimised for aerial target engagement | - High-velocity ballistic rounds  / - Optimized for aerial target engagement | changed |
| DT_EntityData_UI_Items | …AdditionalTexts[UI.Tooltip.Layout.ItemDescription].Value.SourceString | - High-velocity ballistic rounds  / - Optimised for aerial target engagement | - High-velocity ballistic rounds  / - Optimized for aerial target engagement | changed |
| DT_EntityData_UI_Items | …AdditionalTexts[UI.Tooltip.Layout.ItemDescription].Value.LocalizedString | - High-velocity ballistic rounds  / - Optimised for aerial target engagement | - High-velocity ballistic rounds  / - Optimized for aerial target engagement | changed |
| DT_EntityData_UI_Items | …Tracer.Icons.TaggedIcons[/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound… | — | {"Key":"/Game/UI/Features/HUD/EquippedItem/Textures/T_UI_ChamberedRound_Bullet.T_UI_Chamb… | added |
| DT_EntityData_UI_Items | Rows.ID.Item.125x570mm | — | {"FriendlyName":{"TableId":"/Game/UI/StringTables/STRINGS_GameplayTags.STRINGS_GameplayTa… | added |

#### DT_ServerBrowserMapTexture (12 records, 12 non-numeric)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_ServerBrowserMapTexture | Rows.Bakurani_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":"Bakurani"},"LightPresetToTexture":[],"DefaultMa… | added |
| DT_ServerBrowserMapTexture | Rows.Madrid_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":"Ozeti"},"LightPresetToTexture":[],"DefaultMapTe… | added |
| DT_ServerBrowserMapTexture | Rows.Detroit_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":"Zestafona"},"LightPresetToTexture":[],"DefaultM… | added |
| DT_ServerBrowserMapTexture | Rows.Moscow_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":"Saburtulo"},"LightPresetToTexture":[],"DefaultM… | added |
| DT_ServerBrowserMapTexture | Rows.Bakurani_SniperShowdown_01 | — | {"DisplayName":{"CultureInvariantString":"Bakurani Outskirts - Jutari"},"LightPresetToTex… | added |
| DT_ServerBrowserMapTexture | Rows.Tanktown | — | {"DisplayName":{"TableId":"/Game/UI/StringTables/Frontend/STRINGS_ServerBrowser.STRINGS_S… | added |
| DT_ServerBrowserMapTexture | Rows.Mindori_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":null},"LightPresetToTexture":[],"DefaultMapTextu… | added |
| DT_ServerBrowserMapTexture | Rows.Tevza_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":null},"LightPresetToTexture":[],"DefaultMapTextu… | added |
| DT_ServerBrowserMapTexture | Rows.Berlin_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":null},"LightPresetToTexture":[],"DefaultMapTextu… | added |
| DT_ServerBrowserMapTexture | Rows.Deathmatch | — | {"DisplayName":{"TableId":"/Game/UI/StringTables/Frontend/STRINGS_ServerBrowser.STRINGS_S… | added |
| DT_ServerBrowserMapTexture | Rows.Paris_KOTH_01 | — | {"DisplayName":{"CultureInvariantString":null},"LightPresetToTexture":[],"DefaultMapTextu… | added |
| DT_ServerBrowserMapTexture | Rows.Bakurani_KOTH_02 | — | {"DisplayName":{"TableId":"/Game/UI/StringTables/Frontend/STRINGS_FindMatch.STRINGS_FindM… | added |

## New in Season 2

12 assets were added. Identification is the type and the file name.

| Asset | Type | Path |
|---|---|---|
| [DT_EntityData_UI_GoldExchange](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/GoldExchange/Data/DT_EntityData_UI_GoldExchange.json) | DataTable | DT_EntityData_UI_GoldExchange.json |
| [DT_SceneData_Match_ShootingRange](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | DataTable | DT_SceneData_Match_ShootingRange.json |
| [DT_SceneData_Match_Wagers](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | DataTable | DT_SceneData_Match_Wagers.json |
| [DT_SquadIntents](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/ContextDrawer/Tabs/Party/Data/DT_SquadIntents.json) | DataTable | DT_SquadIntents.json |
| [D_Decorator_Interactable_HospitalDoor_01a_Left](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Decorator_Interactable_HospitalDoor_01a_Left.json) | BHDestructionBuildingDecoratorDefinitionDataAsset | D_Decorator_Interactable_HospitalDoor_01a_Left.json |
| [D_Decorator_Interactable_HospitalDoor_01a_Right](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Decorator_Interactable_HospitalDoor_01a_Right.json) | BHDestructionBuildingDecoratorDefinitionDataAsset | D_Decorator_Interactable_HospitalDoor_01a_Right.json |
| [D_InteractableDoor_Buisness](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_InteractableDoor_Buisness.json) | BHDestructionBuildingDefinitionDataAsset | D_InteractableDoor_Buisness.json |
| [D_Interactable_Commercial_Door_01a_L](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_Commercial_Door_01a_L.json) | BHDestructionBuildingDefinitionDataAsset | D_Interactable_Commercial_Door_01a_L.json |
| [D_Interactable_Commercial_Door_01a_R](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_Commercial_Door_01a_R.json) | BHDestructionBuildingDefinitionDataAsset | D_Interactable_Commercial_Door_01a_R.json |
| [D_Interactable_Door_Wood_01a](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_Door_Wood_01a.json) | BHDestructionBuildingDefinitionDataAsset | D_Interactable_Door_Wood_01a.json |
| [D_Interactable_HospitalDoor_01a_Left](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_HospitalDoor_01a_Left.json) | BHDestructionBuildingDefinitionDataAsset | D_Interactable_HospitalDoor_01a_Left.json |
| [D_Interactable_HospitalDoor_01a_Right](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_HospitalDoor_01a_Right.json) | BHDestructionBuildingDefinitionDataAsset | D_Interactable_HospitalDoor_01a_Right.json |

## Removed in Season 2

None.

## Moved

None.

## See also

- [Weapon market and tags]({{ '/content/Wardogs_Weapons_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Game mechanics, vendor markets]({{ '/content/Wardogs_GameMechanics_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Rewards and tags]({{ '/game-features/Wardogs_GameFeatures_Rewards_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Destruction]({{ '/content/Wardogs_Destruction_v2.html' | relative_url }}#season-02-update), Season 02 update

Full change browser for this area: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=data-tables-tags&q=

