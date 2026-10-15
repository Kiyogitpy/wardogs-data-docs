# Wardogs — Plugin: BHSpectatorCamera (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/BHSpectatorCamera/` — 6 JSON files under `Content/Inputs/`: 5 input actions and 1 input mapping context.*

---

## 1. What This Plugin Holds

The free-fly spectator camera's input setup. Five input actions define what the camera can do. One input mapping context binds keyboard and mouse keys to those actions.

---

## 2. Input Actions

| Action | Input tag | Value type | Purpose (from name) |
|---|---|---|---|
| `IA_BHSpectatorCameraMove` | `Input.NamedActions.SpectatorCam.Move` | Axis3D | Fly in three dimensions |
| `IA_BHSpectatorCameraRotate` | `Input.NamedActions.SpectatorCam.Rotate` | Axis2D | Look around |
| `IA_BHSpectatorCameraRoll` | `Input.NamedActions.SpectatorCam.Roll` | Axis1D | Roll the camera |
| `IA_BHSpectatorCameraFast` | `Input.NamedActions.SpectatorCam.Fast` | (none set, button) | Speed boost while held |
| `IA_BHSpectatorCameraLockOntoActor` | `Input.NamedActions.SpectatorCam.LockOntoActor` | (none set, button) | Lock the camera onto an actor |

---

## 3. Key Bindings (`IMC_BHSpectatorCamera`)

11 mappings. Each maps one key to one action, with optional triggers and modifiers.

| Action | Key | Triggers | Modifiers |
|---|---|---|---|
| Move | W | Pressed, Released | none |
| Move | S | Pressed, Released | 1 |
| Move | A | Pressed, Released | 2 |
| Move | D | Pressed, Released | 1 |
| Move | SpaceBar | Pressed, Released | 1 |
| Move | LeftControl | Pressed, Released | 2 |
| Rotate | Mouse2D | none | none |
| Roll | E | none | 1 |
| Roll | Q | none | none |
| Fast | LeftShift | Pressed, Released | none |
| LockOntoActor | L | Pressed | none |

Move uses the axis modifiers (Negate and SwizzleAxis) so that each direction key gives the right sign on the 3-axis input. The export has 4 Negate and 4 SwizzleAxis modifiers in total; the swizzle order `ZYX` is set on two of them.

Roll reads E and Q as one axis. E has one modifier and Q has none. Which modifier is on E is not resolved in this pass.

---

## 4. How Values Combine

- Move is a 3-axis input. Its W/S, A/D, Space and Ctrl keys together produce the fly vector.
- Rotate reads the mouse as a 2-axis delta.
- Roll reads E and Q as a single 1-axis value.
- Fast is a held button; while held it changes the speed of Move. The speed factor is not in this folder.
- LockOntoActor is a press that locks the camera to a target actor; the target choice is made in code.

---

## 5. Still not pulled / limitations

- **Modifier per key.** The count per key is given. Which exact modifier (Negate or Swizzle) is on each key was not fully resolved in this pass.
- **Speed values.** The movement and rotation speed multipliers and the Fast factor are in the spectator camera code or Blueprint, not in this folder.
- **Sensitivity.** Mouse sensitivity for rotate comes from the BHFramework settings, not this plugin.
- **Gamepad.** This mapping context covers keyboard and mouse only.
