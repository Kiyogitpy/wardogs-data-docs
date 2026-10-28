---
title: "Gunsmith"
redirect_from: ["/Wardogs_GameFeatures_Gunsmith_v2.html", "/Wardogs_GameFeatures_Gunsmith_v2"]
parent: "Weapons & Ammo"
description: "The Gunsmith weapon customisation screen: its scene, build page, reticles and frontend map."
---

# Wardogs — Gunsmith Game Feature Reference
*Extracted from cooked game data (`Wardogs/Plugins/GameFeatures/Gunsmith`, 18 JSON files, all parsed). Build `++Wardogs+Live-CL-516586`, UE 5.7.*

> **What this is:** the weapon-customisation mode (reticles, optics, attachments, flair) built on the shared **Itemsmith** UI framework, the same base as Vehiclesmith. Almost all of it is UI configuration: pages, browser lists, reticle definitions, accuracy display and textures. The weapon balance numbers (damage, RPM, recoil) are **not** in this plugin. Those live on the weapon items elsewhere.

---

## Season 02 update (2026-10-15)

- **No files added or removed.** The one changed file is the popup table below.
- **Popup options** (`DT_GunsmithPopupOptions`) went from 0 rows to 5:
  - `UI.Popup.SaveBlueprint`: Info, Cancel / OK.
  - `UI.Popup.DeleteBlueprint`: Warning, "Do you wish to permanently delete this blueprint?" ("This cannot be undone"), Cancel / OK.
  - `UI.Popup.RenameItem`: Itemsmith rename type, RENAME / Cancel.
  - `UI.Popup.FullBlueprintItems`: Warning, OK.
  - `UI.Popup.ChangeComponent`: Warning, Apply / Cancel.

Full before/after list: [Season 2 Changes → Weapons & Ammo]({{ '/season-2-changes/weapons-ammo.html' | relative_url }}).

## 1. Plugin Inventory

| Group | Assets | Role |
|---|---|---|
| Root | `Content/Gunsmith.json` (`GameFeatureData` + 2 actions) | Adds the player component and data registry sources |
| Scene | `Content/UI/Data/DA_GunsmithScene`, `Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith` | Gunsmith scene root and frontend entry |
| Build | `Content/UI/Build/Data/DA_Gunsmith_Build` | Build page settings |
| Reticle picker | `Content/UI/ReticleNodeFocus/Data/` (`DA_Gunsmith_ReticleNodeFocus`, `..._BrowserList`, `..._BrowserItem`, `DT_Gunsmith_Reticles`) | Reticle browser and reticle definitions |
| Optics | `Content/UI/OpticAdjust/Data/DA_Gunsmith_OpticAdjust` | Optic rail adjustment slider |
| Sub-nodes | `Content/UI/SubNodeFocus/Data/DA_Gunsmith_SubNodeFocus` | Sight sub-node bindings |
| Stats | `Content/UI/Shared/Stats/Data/DA_Gunsmith_Stats`, `Content/UI/Shared/Stats/ExpandedStats/Data/DA_GunsmithExpandedAccuracy` | Accuracy display and expanded accuracy |
| Entities (UI) | `Content/UI/Data/Entities/` (`DT_Gunsmith_EntityData_UI_DecalTextures`, `..._PaintMaskTextures`, `..._PaintMasteryTextures`, `..._ReticleTextures`, `DT_Gunsmith_DevMenuMaps`) | Texture and map entries |
| Popups | `Content/UI/Data/Popups/DT_GunsmithPopupOptions` | Popup options, **5 rows** |

---

## 2. Root Game Feature

### 2a. Component

| Actor class | Component class |
|---|---|
| `WDGame.WDPlayerController` | `GunsmithRuntime.WDGunsmithPlayerComponent` |

The Gunsmith runtime attaches its controller component to the player controller when the feature loads.

### 2b. Data registry sources

| Registry | Table |
|---|---|
| `DevMenuMapsData` | `DT_Gunsmith_DevMenuMaps` |
| `UISceneData_Frontend` | `DT_SceneData_Frontend_Gunsmith` |

---

## 3. Frontend and Dev Map

| Table | Row | Value |
|---|---|---|
| `DT_SceneData_Frontend_Gunsmith` | `UI.Scene.Frontend.Gunsmith` | Input mode UI; reset focus on enter true; block back false; focusable true; should preload false |
| `DT_Gunsmith_DevMenuMaps` | `DevMaps.Gunsmith` | Map `/Gunsmith/Maps/Gunsmith_Main_P` ("Gunsmith") |

---

## 4. Scene (`DA_GunsmithScene`)

### 4a. Map layers and family

| Field | Value |
|---|---|
| Default item family background | `Id.Item` |
| Layer for `Id.Item` | Background `DL_Gunsmith_Background`; test-ground `DL_Gunsmith_FiringRange` |
| D-pad controls angle | 55 |
| Left scene tab image | `T_UI_Attachments_Icon` |

### 4b. Page-to-widget map (18 page types)

| Page | Widget class | Shared scene widgets shown |
|---|---|---|
| `ItemSelect` | `W_Itemsmith_ItemSelectGrid` | 4 |
| `Variants` | `W_Itemsmith_ItemSelectGrid` | 4 |
| `Build` | `W_Itemsmith_Build` | **6** |
| `AttachmentNodeFocus` | `W_Itemsmith_AttachmentNodeFocus` | 4 |
| `SubNodeFocus` | `W_Itemsmith_SubNodeFocus` | 5 |
| `OpticAdjust` | `W_Gunsmith_OpticAdjust` | 4 |
| `ReticleNodeFocus` | `W_Gunsmith_ReticleNodeFocus` | 4 |
| `FlairNodeFocus` | `W_Itemsmith_FlairNodeFocus` | 4 |
| `FlairOverview` | `W_Itemsmith_FlairOverview` | 5 |
| `FlairItemPaint` | `W_Itemsmith_FlairItemPaint` | 4 |
| `FlairBasicPaint`, `FlairCamoPaint`, `FlairMasteryPaint`, `FlairFavouritePaint` | `W_Itemsmith_PaintSelect` | 2 each |
| `FlairDecalOverview` | `W_ItemSmith_Flair_DecalOverview` | 2 |
| `FlairDecalSelection` | `W_ItemSmith_Flair_DecalSelection` | 2 |
| `FlairPaintMaskSelection` | `W_ItemSmith_Flair_PaintMaskSelect` | 2 |
| `HideUI` | `W_Itemsmith_HideUI` | 0 |

The count is how many shared scene widgets the page asks for. The `Build` page has the most.

### 4c. Node classes

| Node type | Node component |
|---|---|
| `ItemPartNode` | `B_GunsmithNodeComponent` |
| `DecalLayerNode` | `B_GunsmithDecalLayerNodeComponent` |
| `LoadingSpinnerNode` | `B_GunsmithLoadingSpinnerNodeComponent` |

---

## 5. Build Page (`DA_Gunsmith_Build`)

| Field | Value |
|---|---|
| Attachment node page preference | `Item.Attachment.Sight` opens `EWDUIItemsmithPages::SubNodeFocus` |
| Camera mode | `EItemsmithCameraMode::Normal` |
| Input mapping context priority | 11 |

---

## 6. Reticles

### 6a. Reticle definitions (`DT_Gunsmith_Reticles`, 10 rows)
Row type `WDReticleAssetInfo`. Each row has `ExclusivityTags` (scope types that cannot coexist with it), a flair tag, a texture asset, and `bInitiallyLocked` (false on all 10).

| Reticle | Flair tag | Texture | Exclusive with (abridged) |
|---|---|---|---|
| `10x` | `Gunsmith.Textures.Reticle.10x` | `T_Reticle_10X_Greyscale` | `Id.Item.10xScopeMoa`, `...10xScopeMrad`, `Id.Item.SniperScope10x`, `Id.Item.HybridScope4x` |
| `10xRangeFinder` | `...10x.RangeFinder` | `T_Reticle_10X_RangeFinder_Greyscale` | Same four as `10x`, plus `Id.Item.EotechHoloSight`, `Id.Item.BasicRedDot`, `Id.Item.OPT_06`, `Id.Item.OPT_08`, `Id.Item.4xElcanSpectr` |
| `4xHybrid` | `...4x.Hybrid` | `T_Reticle_4X_Hybrid_Greyscale` | `Id.Item.4xElcanSpectr`, `Id.Item.HybridScope4x`, `Id.Item.10xScopeMoa`, `Id.Item.10xScopeMrad` |
| `AimpointDot` | `...Aimpoint` | `T_Reticle_Aimpoint_Dot_Greyscale` | `Id.Item.BasicRedDot`, `Id.Item.EotechHoloSight`, `Id.Item.OPT_06`, `Id.Item.OPT_08` |
| `EotechHolographic` | `...Eotech.Holographic` | `T_Reticle_Holographic_Greyscale` | `Id.Item.BasicRedDot`, `Id.Item.OPT_06`, `Id.Item.OPT_08`, `Id.Item.4xElcanSpectr` |
| `Infrared` | `...Infrared` | `T_Reticle_Infrared_01` | Same four as `10x` |
| `Kobra` | `...Kobra` | `T_Reticle_KobraSight_Greyscale` | `Id.Item.EotechHoloSight` |
| `LPVOShortDot` | `...LPVO.ShortDot` | `T_Reticle_LPVO_ShortDot_Greyscale` | Same four as `10x` |
| `MicroRedDot` | `...MicroRedDot` | `T_Reticle_MicroRedDot_Greyscale` | `Id.Item.EotechHoloSight`, `Id.Item.BasicRedDot`, `Id.Item.OPT_06`, `Id.Item.OPT_08` |
| `Prism` | `...Prism` | `T_Reticle_Prism_Greyscale` | Same four as `10x` |

Pattern: the 10x-class reticles exclude the 10x and hybrid scopes; the red-dot family excludes the other red dots and the holographic sight.

### 6b. Reticle textures (`DT_Gunsmith_EntityData_UI_ReticleTextures`, 17 rows)
The 10 reticle rows above, plus 4 rows keyed by scope item id and sight state (`Id.Item.SniperScope10x.S_Aim01`, `Id.Item.OPT_08.S_Aim01`, `Id.Item.4xElcanSpectr.S_Aim01`, `Id.Item.HybridScope4x.S_Aim01`).

### 6c. Reticle browser

| Field | Value |
|---|---|
| Base filter | `Item.Archetype.Build.Reticle.Base` ("Base") |
| Favourite filter | `Item.Archetype.Build.Reticle.Favourite` |
| Reticle data | `DT_Gunsmith_Reticles` |
| Entry size (w x h) | 270 x 125 |
| Items per page | 6 |
| Entry icon type | `UI.Icon.Gunsmith.Reticle` |
| Entity data name | `Gunsmith_EntityData_UI` |
| Default persistent action | `Itemsmith.Actions.Persistent.Favourite` |

---

## 7. Sight Sub-Node (`DA_Gunsmith_SubNodeFocus`)

Keyed on `Item.Attachment.Sight`:

| Sub-node | Attach bone |
|---|---|
| `Optic` | `sight_Attach` |
| `Adjust` | `sight_Attach` |
| `Reticle` | `S_Aim01` |

Camera mode `Normal`.

---

## 8. Optic Rail Adjustment (`DA_Gunsmith_OpticAdjust`)

| Field | Value |
|---|---|
| Display name | "Receiver Rail Distance" |
| Range min / max | **-2.0 / 10.0** |
| Display range min / max | **-1.0 / 2.0** |
| Slider view model | `WDUIItemsmithSliderViewModel` on an Itemsmith slider data asset (`/Itemsmith/UI/SharedWidgets/Slider/Data/`; full name truncated in export) |

The slider's internal range (-2 to 10) is wider than its display range (-1 to 2), so the UI shows a narrower band than the real travel.

---

## 9. Accuracy Display

### 9a. Accuracy unit labels (`DA_Gunsmith_Stats`)

| Accuracy type | Label |
|---|---|
| `EWDWeaponAccuracyType::Milliradians` | MRAD |
| `EWDWeaponAccuracyType::MinutesOfAngle` | MOA |

Expand and collapse actions: `Input.NamedActions.ItemSmith.ExpandStats` and `...CollapseStats`.

### 9b. Expanded accuracy (`DA_GunsmithExpandedAccuracy`)

| Setting | Value |
|---|---|
| Max MOA value | **25.0** |
| MOA small-value limit | **5.0** |
| Small MOA value bands | 1.0, 2.0, 3.0, 4.0, 5.0 |
| Minimum silhouette scale | **0.3** |
| Max visualizer radius | **0.5** |
| Minimum crosshair offset multiplier | **0.7** |

The large-MOA value bands (extracted in round 39) are 5.0, 10.0, 15.0, 20.0 and 25.0, the small bands being 1.0 to 5.0; `MaxMOAValue` 25 is the top of the large scale. These read as display and crosshair-visualiser settings. The export does not show them feeding weapon accuracy.

---

## 10. Textures and Entries

### 10a. Decals (`DT_Gunsmith_EntityData_UI_DecalTextures`, 5 rows)
`Gunsmith.Textures.Decal.Standard.ReviveHand` ("Revive Hand"), `...Headshot` ("Headshot"), `...DownedMarker` ("Downed Marker"), `...FriendlyMarker` ("Friendly Marker"), `...GRN` ("GRN").

### 10b. Paint masks (`DT_Gunsmith_EntityData_UI_PaintMaskTextures`, 4 rows)
`Gunsmith.Textures.Mask.BrushCircle`, `...BrushPyramid`, `...BulletImpactA`, `...BulletImpactB`. No friendly names.

### 10c. Paint mastery (`DT_Gunsmith_EntityData_UI_PaintMasteryTextures`, 6 rows)
`Gunsmith.Textures.Mastery.Default1` ("Gold"), `Default2` ("pink"), `Default3` ("clouds"), `Default4` ("Normal"), `Default5` ("rainbow"), and `Gunsmith.Textures.Camo` ("Camo").

---

## 11. How Values Combine

- **Reticle exclusivity:** choosing a reticle filters out any reticle whose exclusivity tags clash with the scope already fitted. For example, a 10x scope blocks `10xRangeFinder`.
- **Accuracy display:** the accuracy value is shown in MRAD or MOA. The expanded view uses the MOA settings above for its visualiser and crosshair. The export does not show these settings changing weapon accuracy.
- **Optic rail:** the slider's display range (-1 to 2) is a subset of its internal range (-2 to 10).

---

## 12. Still Not Pulled / Limitations

- **Weapon balance is not here.** Damage, fire rate, recoil and spread live on the weapon items, which are outside this plugin.
- **Texture and widget assets** (`T_Reticle_*`, `W_*`, `DL_Gunsmith_*`, `B_Gunsmith*`) are referenced by name or path only.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Localised strings** are referenced by key. The text is not in this export except where a `SourceString` was exported.
- **Scope and sight item ids** (for example `Id.Item.OPT_08`) are referenced in the exclusivity and texture rows, but the item definitions are outside this plugin.
- **Popup options** (`DT_GunsmithPopupOptions`) hold five popup rows (see the Season 02 update). Popup text is referenced by key, and only some `SourceString` values are exported.
