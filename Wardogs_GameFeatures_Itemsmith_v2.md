---
title: "Itemsmith (feature)"
parent: "Game Features"
---

# Wardogs: GameFeatures Itemsmith Reference (v2)
*Source: exported JSON under [`Wardogs/Plugins/GameFeatures/Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Itemsmith) (117 files, one folder: `Content`). Itemsmith is the paint, decal and attachment customisation screen. Numbers are read from the export; anything not confirmed is marked.*

---

## Season 02 update (2026-10-15)

- **No files added or removed;** the file counts below are unchanged.
- **[`DA_Itemsmith_ItemPaintData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/ItemPaint/Data/DA_Itemsmith_ItemPaintData.json)** (the flair item-paint screen, section 7) gained settings in this update:
  - a warning popup for an empty favourites list (`UI.Popup.EmptyFavoritePaints`);
  - `MaxFavouritePaintsToShow` = 5;
  - camera mode `EItemsmithCameraMode::FixedSideOn`, with a focus offset of (0, 20, 7);
  - input mapping context [`IMC_Itemsmith_FlairItemPaint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Input/IMC_Itemsmith_FlairItemPaint.json) at priority 11;
  - a screen title (`Itemsmith.Flair.WeaponPaint.Title`) and `bShowBlueprintNameAsSubtitle` = true.
  The layout of this asset is not decoded in this doc.

## 1. Layout and File Counts

| Export Type | Files | Role |
|---|---|---|
| BHInputAction | 47 | Named input actions (section 2) |
| InputMappingContext | 12 | Context-specific key bindings (section 3) |
| WDUIItemsmithBrowserItemData | 10 | UI widget data assets (section 7) |
| DataTable | 7 | Paint palette, masks, tag text, settings, popup and scene rows (sections 4 to 6) |
| WDUIItemsmithBrowserData | 4 | UI widget data assets (section 7) |
| WDUIItemsmithBrowserPaintData | 4 | UI widget data assets (section 7) |
| BHUserSettingDiscreteData | 2 | Finish and Wear settings (section 6) |
| WDUIItemsmithSubNodeFocusData | 2 | UI widget data assets (section 7) |
| BHGameFeatureAction_AddInputContextMapping | 1 | Adds the Itemsmith input context to the game (section 9) |
| BHPlayerMappableKeySettings | 1 | Player-remappable key settings for IMC_Itemsmith_PlayerController (section 9) |
| CurveFloat | 1 | Preview weapon explosion curve (not decoded) |
| WDUIItemsmithAttachmentSelectBrowserFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithBuildData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithCancelEditDecalPlacementAction | 1 | UI widget data assets (section 7) |
| WDUIItemsmithData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithFavouritedDecalFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithBrowserDecalData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithFlairOverviewData | 1 | UI widget data assets (section 7) |
| WDUIFlairItemPaintData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithFavouritePaintMaskSelectFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithBasicPaintSelectFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithCamoPaintSelectFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithFavouritePaintSelectFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithFavouriteMasteryPaintSelectFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithHideUIData | 1 | UI widget data assets (section 7) |
| WDUIGunsmithArchetypeFilter | 1 | UI widget data assets (section 7) |
| WDUIGunsmithFavouritedVariantsFilter | 1 | UI widget data assets (section 7) |
| WDUIItemsmithNodeData | 1 | UI widget data assets (section 7) |
| DWUIItemsmithPopupRenameData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithBaseInfoData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithHeroTitleData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithNavigationBarData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithPlatformData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithPlatformButtonData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithSliderData | 1 | UI widget data assets (section 7) |
| WDUIItemsmithTabGroupData | 1 | UI widget data assets (section 7) |
| WDUITestingGroundSceneData | 1 | UI widget data assets (section 7) |

---

## 2. Named Input Actions

47 `BHInputAction` assets. The `Named action tag` is the string the UI and input layers use. `Value type` is `not exported` where the field is absent (the default is not confirmed).

| Asset | Named action tag | Value type | Consumes input |
|---|---|---|---|
| IA_AllowRotateView | Input.NamedActions.ItemSmith.EnableRotateView | not exported | no |
| IA_FlipView | Input.NamedActions.ItemSmith.FlipView | not exported | not exported |
| IA_Itemsmith_ApplyPaint | Input.NamedActions.ItemSmith.Flair.ApplyPaint | not exported | not exported |
| IA_Itemsmith_CancelEditDecalPlacement | Input.NamedActions.ItemSmith.Flair.CancelEditDecalPlacement | not exported | no |
| IA_Itemsmith_ClearDecalLayer | Input.NamedActions.ItemSmith.Flair.ClearDecalLayer | not exported | no |
| IA_Itemsmith_ClearPaint | Input.NamedActions.ItemSmith.Flair.ClearPaint | not exported | not exported |
| IA_Itemsmith_EditDecalPlacement | Input.NamedActions.ItemSmith.Flair.EditDecalPlacement | not exported | no |
| IA_Itemsmith_ExpandStats | Input.NamedActions.ItemSmith.ExpandStats | not exported | no |
| IA_Itemsmith_Favourite | Input.NamedActions.ItemSmith.Favourite | not exported | no |
| IA_Itemsmith_FlairOverview_EnterDecals | Input.NamedActions.ItemSmith.FlairOverview.EnterDecals | not exported | not exported |
| IA_Itemsmith_FlairOverview_EnterPaint | Input.NamedActions.ItemSmith.FlairOverview.EnterPaint | not exported | not exported |
| IA_Itemsmith_HeroTitle | Input.NamedActions.ItemSmith.HeroTitle | not exported | no |
| IA_Itemsmith_HideShowUI | Input.NamedActions.ItemSmith.HideShowUI | not exported | no |
| IA_Itemsmith_Next | Input.NamedActions.ItemSmith.Next | not exported | no |
| IA_Itemsmith_Next_Alternative | Input.NamedActions.ItemSmith.Next.Alternative | not exported | no |
| IA_Itemsmith_Previous | Input.NamedActions.ItemSmith.Previous | not exported | no |
| IA_Itemsmith_Previous_Alternative | Input.NamedActions.ItemSmith.Previous.Alternative | not exported | no |
| IA_Itemsmith_RemoveBlueprint | Input.NamedActions.ItemSmith.RemoveBlueprint | not exported | not exported |
| IA_Itemsmith_SaveBlueprint | Input.NamedActions.ItemSmith.SaveBlueprint | not exported | no |
| IA_Itemsmith_Tab | Input.NamedActions.ItemSmith.Tab | not exported | no |
| IA_Itemsmith_TestingGround | Input.NamedActions.ItemSmith.TestingGround | not exported | no |
| IA_MoveFocusBackwards | Input.NamedActions.ItemSmith.MoveFocus.Backwards | Axis1D | not exported |
| IA_MoveFocusDown | Input.NamedActions.ItemSmith.MoveFocus.Down | Axis1D | not exported |
| IA_MoveFocusForward | Input.NamedActions.ItemSmith.MoveFocus.Forwards | Axis1D | not exported |
| IA_MoveFocusLeft | Input.NamedActions.ItemSmith.MoveFocus.Left | Axis1D | not exported |
| IA_MoveFocusRight | Input.NamedActions.ItemSmith.MoveFocus.Right | Axis1D | not exported |
| IA_MoveFocusUp | Input.NamedActions.ItemSmith.MoveFocus.Up | Axis1D | not exported |
| IA_MovePreviewDown | Input.NamedActions.ItemSmith.MovePreview.Down | Axis1D | not exported |
| IA_MovePreviewLeft | Input.NamedActions.ItemSmith.MovePreview.Left | Axis1D | not exported |
| IA_MovePreviewRight | Input.NamedActions.ItemSmith.MovePreview.Right | Axis1D | not exported |
| IA_MovePreviewUp | Input.NamedActions.ItemSmith.MovePreview.Up | Axis1D | not exported |
| IA_NodeDown | Input.NamedActions.ItemSmith.Node.Down | not exported | no |
| IA_NodeLeft | Input.NamedActions.ItemSmith.Node.Left | not exported | no |
| IA_NodeRight | Input.NamedActions.ItemSmith.Node.Right | not exported | no |
| IA_NodeUp | Input.NamedActions.ItemSmith.Node.Up | not exported | no |
| IA_PanCameraDown | Input.NamedActions.ItemSmith.PanCamera.Down | Axis1D | not exported |
| IA_PanCameraLeft | Input.NamedActions.ItemSmith.PanCamera.Left | Axis1D | not exported |
| IA_PanCameraRight | Input.NamedActions.ItemSmith.PanCamera.Right | Axis1D | not exported |
| IA_PanCameraUp | Input.NamedActions.ItemSmith.PanCamera.Up | Axis1D | not exported |
| IA_ResetCamera | Input.NamedActions.ItemSmith.ResetCamera | not exported | not exported |
| IA_RotateView | Input.NamedActions.ItemSmith.RotateView | Axis2D | no |
| IA_ScalePreviewDown | Input.NamedActions.ItemSmith.ScalePreview.Down | Axis1D | not exported |
| IA_ScalePreviewUp | Input.NamedActions.ItemSmith.ScalePreview.Up | Axis1D | not exported |
| IA_SelectNode | Input.NamedActions.ItemSmith.SelectNode | not exported | no |
| IA_SelectReticle | Input.NamedActions.ItemSmith.ScalePreview.Up | Axis1D | no |
| IA_ZoomIn | Input.NamedActions.ItemSmith.ZoomIn | Axis1D | no |
| IA_ZoomOut | Input.NamedActions.ItemSmith.ZoomOut | Axis1D | no |

**Probable export or authoring error:** [`IA_SelectReticle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Input/IA_SelectReticle.json) is tagged `Input.NamedActions.ItemSmith.ScalePreview.Up`, the same tag as [`IA_ScalePreviewUp`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Input/IA_ScalePreviewUp.json). Reticle selection and preview scaling would then share one action name. This is flagged, not confirmed.

---

## 3. Input Contexts and Key Bindings

12 `InputMappingContext` assets. Each binding lists its keyboard and gamepad keys together. The [`IMC_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Input/IMC_Itemsmith.json) context holds 38 mappings, the largest.

| Context | Action | Keys |
|---|---|---|
| IMC_Itemsmith | IA_ZoomIn | MouseScrollUp, Gamepad_RightTrigger, Equals |
| IMC_Itemsmith | IA_ZoomOut | MouseScrollDown, Gamepad_LeftTrigger, Hyphen |
| IMC_Itemsmith | IA_AllowRotateView | RightMouseButton, LeftMouseButton |
| IMC_Itemsmith | IA_RotateView | Mouse2D, Gamepad_Right2D |
| IMC_Itemsmith | IA_NodeLeft | Gamepad_DPad_Left, Left |
| IMC_Itemsmith | IA_NodeRight | Right, Gamepad_DPad_Right |
| IMC_Itemsmith | IA_NodeUp | Up, Gamepad_DPad_Up |
| IMC_Itemsmith | IA_NodeDown | Down, Gamepad_DPad_Down |
| IMC_Itemsmith | IA_SelectNode | Gamepad_FaceButton_Bottom, Enter |
| IMC_Itemsmith | IA_Itemsmith_Next | E, Gamepad_RightShoulder |
| IMC_Itemsmith | IA_Itemsmith_Previous | Q, Gamepad_LeftShoulder |
| IMC_Itemsmith | IA_Itemsmith_Tab | Tab, Gamepad_FaceButton_Top |
| IMC_Itemsmith | IA_Itemsmith_HeroTitle | P, Gamepad_Special_Right |
| IMC_Itemsmith | IA_Itemsmith_TestingGround | F, Gamepad_Special_Left |
| IMC_Itemsmith | IA_Itemsmith_ExpandStats | X, Gamepad_RightThumbstick |
| IMC_Itemsmith | IA_Itemsmith_RemoveBlueprint | Delete, Gamepad_FaceButton_Left |
| IMC_Itemsmith | IA_Itemsmith_HideShowUI | H, Gamepad_Special_Left |
| IMC_Itemsmith | IA_Itemsmith_SaveBlueprint | S, Gamepad_FaceButton_Left |
| IMC_Itemsmith_BasicPaintSelect | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_BasicPaintSelect | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_BasicPaintSelect | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_BasicPaintSelect | IA_Itemsmith_ApplyPaint | SpaceBar, Gamepad_FaceButton_Bottom |
| IMC_Itemsmith_BasicPaintSelect | IA_Itemsmith_ClearPaint | SpaceBar, Gamepad_FaceButton_Bottom |
| IMC_Itemsmith_BlueprintSelect | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_BlueprintSelect | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_BlueprintSelect | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_Dev | IA_MoveFocusUp | Add |
| IMC_Itemsmith_Dev | IA_MoveFocusRight | NumPadSix |
| IMC_Itemsmith_Dev | IA_MoveFocusForward | NumPadEight |
| IMC_Itemsmith_Dev | IA_MoveFocusBackwards | NumPadTwo |
| IMC_Itemsmith_Dev | IA_MoveFocusDown | Subtract |
| IMC_Itemsmith_Dev | IA_MoveFocusLeft | NumPadFour |
| IMC_Itemsmith_Dev | IA_MovePreviewUp | U |
| IMC_Itemsmith_Dev | IA_MovePreviewDown | N |
| IMC_Itemsmith_Dev | IA_MovePreviewLeft | G |
| IMC_Itemsmith_Dev | IA_MovePreviewRight | J |
| IMC_Itemsmith_Dev | IA_ScalePreviewDown | Comma |
| IMC_Itemsmith_Dev | IA_ScalePreviewUp | Period |
| IMC_Itemsmith_Flair | IA_FlipView | C, Gamepad_FaceButton_Top |
| IMC_Itemsmith_Flair | IA_PanCameraUp | W, Gamepad_RightStick_Up |
| IMC_Itemsmith_Flair | IA_PanCameraDown | S, Gamepad_RightStick_Down |
| IMC_Itemsmith_Flair | IA_PanCameraLeft | A, Gamepad_RightStick_Left |
| IMC_Itemsmith_Flair | IA_PanCameraRight | D, Gamepad_RightStick_Right |
| IMC_Itemsmith_Flair | IA_ResetCamera | R, Gamepad_FaceButton_Left |
| IMC_Itemsmith_FlairDecalOverview | IA_UI_Back | Escape |
| IMC_Itemsmith_FlairDecalOverview | IA_Itemsmith_ClearDecalLayer | BackSpace, Gamepad_LeftShoulder |
| IMC_Itemsmith_FlairDecalOverview | IA_Itemsmith_EditDecalPlacement | P, Gamepad_RightShoulder |
| IMC_Itemsmith_FlairDecalOverview | IA_Itemsmith_CancelEditDecalPlacement | P, Gamepad_RightShoulder |
| IMC_Itemsmith_FlairDecalSelect | IA_UI_Back | Escape |
| IMC_Itemsmith_FlairDecalSelect | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_FlairDecalSelect | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_FlairDecalSelect | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_FlairItemPaint | IA_UI_Back | Escape |
| IMC_Itemsmith_FlairOverview | IA_Itemsmith_FlairOverview_EnterDecals | U, Gamepad_RightThumbstick |
| IMC_Itemsmith_FlairOverview | IA_Itemsmith_FlairOverview_EnterPaint | D, Gamepad_RightThumbstick |
| IMC_Itemsmith_FlairOverview | IA_UI_Back | Escape, Gamepad_FaceButton_Right |
| IMC_Itemsmith_ItemSelect | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_ItemSelect | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_ItemSelect | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_PaintMaskSelect | IA_Itemsmith_Next | E, Gamepad_RightShoulder |
| IMC_Itemsmith_PaintMaskSelect | IA_Itemsmith_Previous | Q, Gamepad_LeftShoulder |
| IMC_Itemsmith_PaintMaskSelect | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_PaintMaskSelect | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_PaintMaskSelect | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_ReticleNodeFocus | IA_UI_Back | Escape |
| IMC_Itemsmith_ReticleNodeFocus | IA_Itemsmith_Favourite | O, Gamepad_FaceButton_Top |
| IMC_Itemsmith_ReticleNodeFocus | IA_Itemsmith_Next_Alternative | C, Gamepad_RightTrigger |
| IMC_Itemsmith_ReticleNodeFocus | IA_Itemsmith_Previous_Alternative | Z, Gamepad_LeftTrigger |
| IMC_Itemsmith_ReticleNodeFocus | IA_SelectReticle | SpaceBar, Gamepad_FaceButton_Bottom |

---

## 4. Paint Palette

[`DT_Itemsmith_Flair_BasicPaint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_BasicPaint.json) has 60 rows: 12 hues by 5 tiers (the numeric suffix, shown below as Tier 1 to Tier 5). Each row has a `PaintName` (display string) and a `HexadecimalValue` (no `#`). The camo table [`DT_Itemsmith_Flair_CamoBasicPaint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_CamoBasicPaint.json) has the same 60 keys under the `Itemsmith.Colour.Camo.` prefix.

| Hue | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|---|---|---|---|---|---|
| Orange | EDAB8A | 966144 | 954E26 | C54800 | 5F2301 |
| Yellow | 9E985E | 9B934C | 9A8E29 | 988B03 | 867902 |
| LightGreen | 8D9561 | 828C49 | 3A4125 | 353E18 | 2F3618 |
| DarkGreen | 567E55 | 407541 | 2A6E29 | 085F07 | 064906 |
| LightBlue | 567C7B | 3F7270 | 1F3737 | 143333 | 142C2D |
| Blue | 879FAB | 417B8D | 267189 | 096C89 | 0A5E77 |
| DarkBlue | 7194AD | 5581A2 | 363D44 | 292E33 | 1B1E22 |
| DarkPurple | 938BA1 | 847996 | 6F6287 | 564572 | 4A3E5E |
| LightPurple | 867085 | 775A76 | 322836 | 2C1F30 | 281843 |
| DarkPink | 9C7188 | 955C7A | 7C3259 | 6C0D3E | 570A31 |
| LightPink | A36883 | A45378 | 482638 | 46162E | 3E152A |
| Red | 955C5B | 914646 | 8D2828 | 890404 | 740303 |

Camo table check: 60 of 60 camo entries share the same hex value as the basic entry for the same key, so the camo table repeats the basic palette's colours and differs only in the display names. Example camo display names: Camo Orange1, Camo Yellow1, Camo LightGreen1.

---

## 5. Flair Masks

[`DT_Itemsmith_Flair_Masks`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_Masks.json) (`WDFlairMaskInfo`): six masks used to shape paint or decal application.

| Mask | Asset tag | Display name | Hidden on UI |
|---|---|---|---|
| BrushCircle | Gunsmith.Textures.Mask.BrushCircle | Brush Circle | no |
| BrushPyramid | Gunsmith.Textures.Mask.BrushPyramid | Brush Pyramid | no |
| BulletImpactA | Gunsmith.Textures.Mask.BulletImpactA | Bullet Impact A | no |
| BulletImpactB | Gunsmith.Textures.Mask.BulletImpactB | Bullet Impact B | no |
| DefaultOff | Gunsmith.Textures.Mask.DefaultOff | Default Off | yes |
| DefaultOn | Gunsmith.Textures.Mask.DefaultOn | Default On | yes |

---

## 6. Flair Settings

Two user settings for paint, both `BHUserSettingDataTableRow` entries in [`DT_Itemsmith_Flair_Settings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_Settings.json):

| Setting tag | Type asset | Option values |
|---|---|---|
| `Flair.Paint.Settings.Finish` | [`DA_Itemsmith_Flair_Setting_Finish_Discrete`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/PaintSelect/Data/DA_Itemsmith_Flair_Setting_Finish_Discrete.json) (`BHUserSettingDiscreteData`) | Points to a `BHUserSettingEnumDiscreteValues` asset (not exported in this folder) |
| `Flair.Paint.Settings.Wear` | [`DA_Itemsmith_Flair_Setting_Wear_Discrete`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/PaintSelect/Data/DA_Itemsmith_Flair_Setting_Wear_Discrete.json) (`BHUserSettingDiscreteData`) | Points to a `BHUserSettingEnumDiscreteValues` asset (not exported in this folder) |

The names are `Finish` and `Wear`, which suggests a surface finish and a wear/weathering level. The option values are not in the export, so the choices themselves are unknown.

---

## 7. UI Asset Inventory

The `WDUI*` and related widget-data assets that drive the Itemsmith screens. Names only; their layouts are not decoded.

| Asset type | Count | Assets |
|---|---|---|
| BHGameFeatureAction_AddInputContextMapping | 1 | Itemsmith |
| BHPlayerMappableKeySettings | 1 | IMC_Itemsmith_PlayerController |
| WDUIItemsmithAttachmentSelectBrowserFilter | 1 | DA_Itemsmith_AttachmentSelect |
| WDUIItemsmithBrowserItemData | 10 | DA_Itemsmith_AttachmentSelect_BrowserItem, DA_Itemsmith_BasicPaint_BrowserItem, DA_Itemsmith_BrowserEntry, DA_Itemsmith_CamoPaint_BrowserItem, DA_Itemsmith_ClearPaint_BrowserItem, DA_Itemsmith_DecalSelection_BrowserItem, DA_Itemsmith_FavouritePaint_BrowserItem, DA_Itemsmith_MasteryPaint_BrowserItem, DA_Itemsmith_PaintMaskSelect_BrowserItem, DA_Itemsmith_Variant_BrowserEntry |
| WDUIItemsmithBrowserData | 4 | DA_Itemsmith_AttachmentSelect_BrowserList, DA_Itemsmith_BrowserList, DA_Itemsmith_PaintMaskSelect_BrowserList, DA_Itemsmith_Variants_BrowserList |
| WDUIItemsmithBuildData | 1 | DA_Itemsmith_Build |
| WDUIItemsmithCancelEditDecalPlacementAction | 1 | DA_Itemsmith_PersistentActions |
| WDUIItemsmithData | 1 | DA_Itemsmith_DecalOverview |
| WDUIItemsmithFavouritedDecalFilter | 1 | DA_Itemsmith_DecalSelect |
| WDUIItemsmithBrowserDecalData | 1 | DA_Itemsmith_DecalSelection_BrowserList |
| WDUIItemsmithFlairOverviewData | 1 | DA_Itemsmith_FlairOverviewData |
| WDUIFlairItemPaintData | 1 | DA_Itemsmith_ItemPaintData |
| WDUIItemsmithFavouritePaintMaskSelectFilter | 1 | DA_Itemsmith_PaintMaskItemSelect |
| BHUserSettingDiscreteData | 2 | DA_Itemsmith_Flair_Setting_Finish_Discrete, DA_Itemsmith_Flair_Setting_Wear_Discrete |
| WDUIItemsmithBasicPaintSelectFilter | 1 | DA_Itemsmith_BasicPaintSelect |
| WDUIItemsmithBrowserPaintData | 4 | DA_Itemsmith_BasicPaints_BrowserList, DA_Itemsmith_CamoPaints_BrowserList, DA_Itemsmith_FavouritePaints_BrowserList, DA_Itemsmith_MasteryPaints_BrowserList |
| WDUIItemsmithCamoPaintSelectFilter | 1 | DA_Itemsmith_CamoPaintSelect |
| WDUIItemsmithFavouritePaintSelectFilter | 1 | DA_Itemsmith_FavouritePaintSelect |
| WDUIItemsmithFavouriteMasteryPaintSelectFilter | 1 | DA_Itemsmith_MasteryPaintSelect |
| WDUIItemsmithSubNodeFocusData | 2 | DA_Itemsmith_FlairNodeFocus, DA_Itemsmith_SubNodeFocus |
| WDUIItemsmithHideUIData | 1 | DA_Itemsith_HideUI |
| WDUIGunsmithArchetypeFilter | 1 | DA_Itemsmith_ItemSelect |
| WDUIGunsmithFavouritedVariantsFilter | 1 | DA_Itemsmith_VariantSelect |
| WDUIItemsmithNodeData | 1 | DA_Itemsmith_NodeData |
| DWUIItemsmithPopupRenameData | 1 | DA_Itemsmith_RenameItem |
| WDUIItemsmithBaseInfoData | 1 | DA_Itemsmith_BaseInfo |
| WDUIItemsmithHeroTitleData | 1 | DA_Itemsmith_HeroTitle |
| WDUIItemsmithNavigationBarData | 1 | DA_Itemsmith_NavigationBar |
| WDUIItemsmithPlatformData | 1 | DA_Itemsmith_Platform |
| WDUIItemsmithPlatformButtonData | 1 | DA_Itemsmith_PlatformButton |
| WDUIItemsmithSliderData | 1 | DA_Itemsmith_Slider |
| WDUIItemsmithTabGroupData | 1 | DA_Itemsmith_TabGroup |
| WDUITestingGroundSceneData | 1 | DA_TestingGroundSceneData |

---

## 8. Data Tables

| Table | Row struct | Rows |
|---|---|---|
| DT_GameplayTagToText_Itemsmith | WDUIGameplayTagToTextTableRow | 36 |
| DT_PopupTypes_Itemsmith | WDUIPopupTypeDataTableRow | 1 |
| DT_SceneData_Frontend_Itemsmith | WDSceneDataTableRow | 1 |
| DT_Itemsmith_Flair_BasicPaint | WDUIFlairBasicPaintType | 60 |
| DT_Itemsmith_Flair_CamoBasicPaint | WDUIFlairBasicPaintType | 60 |
| DT_Itemsmith_Flair_Masks | WDFlairMaskInfo | 6 |
| DT_Itemsmith_Flair_Settings | BHUserSettingDataTableRow | 2 |

Tag-to-text table [`DT_GameplayTagToText_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_GameplayTagToText_Itemsmith.json) maps 36 keys to display text. Keys include the archetype tags, for example AR, DMR, Grenade, Launcher, LMG, Melee, Pistol, Shotgun, SMG, Sniper, Itemsmith.Flair.WeaponPaint.Title, Input.NamedActions.ItemSmith.ExpandStats, Input.NamedActions.ItemSmith.CollapseStats, Itemsmith.Rename.NameExists, Itemsmith.Rename.EnterName, Itemsmith.Rename.NameTooShort, Attachment.Barrel, Attachment.CantedSight, Attachment.Chamber, Attachment.Charm, Attachment.Grip, Attachment.Handguard, Attachment.Mag, Attachment.Magazine, Attachment.MountLeft, Attachment.MountRight, Attachment.MountTop, Attachment.MountUnder, Attachment.Muzzle, Attachment.Pistolgrip, Attachment.Receiver, Attachment.Sight, Attachment.SightMount, Attachment.Bipod, Attachment.Stock, Attachment.Underbarrel. Their display strings are in the `Text` field, which is not expanded here.

---

## 9. Wiring

- `BHGameFeatureAction_AddInputContextMapping` ([`Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Itemsmith.json)) adds the Itemsmith input contexts (action name `Input.NamedActions.ItemSmith.*`).
- [`IMC_Itemsmith_PlayerController`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Input/IMC_Itemsmith_PlayerController.json) (`BHPlayerMappableKeySettings`) makes the bindings remappable.
- [`DT_PopupTypes_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_PopupTypes_Itemsmith.json) defines one popup type, `UI.Popup.Type.Itemsmith.Rename`. Its rename data asset is [`DA_Itemsmith_RenameItem`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/RenameItem/Data/DA_Itemsmith_RenameItem.json).
- [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) and `DT_TestingGroundSceneData` define the Itemsmith scene and its testing-ground pause. The testing-ground scene is [`DA_TestingGroundSceneData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/TestingGround/Data/DA_TestingGroundSceneData.json).

---

## 10. Still Not Pulled / Limitations

- **Discrete setting option values** (`BHUserSettingEnumDiscreteValues`) are referenced but not in this folder.
- **Widget layouts** (`WDUI*` data) are listed by name only. Their fields, colours and navigation graph are not decoded.
- **Input value types** are blank for most actions. The default is not confirmed.
- **Paint and camo names** are the display strings in the rows; the in-game localisation keys are not expanded.
- **`CurveFloat` [`C_PreviewWeaponExplosionCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/Preview/Gunsmith/C_PreviewWeaponExplosionCurve.json)** is referenced as a preview curve but its keys are not decoded.
- **Actual paint application rules** (which paints a gun accepts, mastery gating, cost) are not in this folder.

