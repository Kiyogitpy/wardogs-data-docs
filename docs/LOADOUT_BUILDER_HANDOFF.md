# Loadout Builder: handoff

Live page: https://kiyogitpy.github.io/wardogs-data-docs/loadout/ (source `content/loadout-builder.md`).
State as of 2026-10-26, `main` at `574627b5`. Built in rounds 82 and 83.

The page lets a player assemble a build (weapon, attachments, gear) within a class level and see what it does:
handling values, sway, recoil spray, the sight's reticle, and damage per body part and over distance. Every number
comes from data already in this repo; the page computes nothing the Python tools can't reproduce.

## 1. Files

| File | Role |
|---|---|
| `content/loadout-builder.md` | The page: front matter (`permalink: /loadout/`, parent "Weapons & Ammo"), the `#lb` root with the four data URLs and `data-base`, the script tags, the no-JS note |
| `assets/js/loadout-builder.js` | All page UI: tiles, picker dialog, summary, weapon card, handling table, sway, sight, ballistics, recoil hook, URL hash |
| `assets/js/loadout-recoil.js` | Recoil panel, `window.WDRecoil` (and the pure model `WDRecoilCore`) |
| `assets/js/loadout-eval.js` | **Shared, do not fork.** `window.WDLoadout`: the attribute evaluator, browser twin of `_tools/weapon_attributes.py`. Also used by the older Weapon Loadout Calculator |
| `assets/js/spray-viewer.js` | **Shared.** The Spray Viewer page; its pure core `SprayViewerCore` is reused by the recoil panel. Its auto-init is guarded on `#sv`, so loading it here is harmless |
| `_sass/custom/loadout-builder.scss`, `loadout-recoil.scss` | Styles, imported at the end of `_sass/custom/custom.scss` |
| `content/loadout-calculator.md`, `assets/js/loadout-calculator.js` | The older technical calculator (attribute table with every modifier, CLI equivalent). Round 82 added the class gate, reticles and ballistics there first; the builder ported that logic |

## 2. Data and how to regenerate it

| File | Generator | Contents |
|---|---|---|
| `assets/data/weapon-loadouts.json` | `python -I _tools/weapon_attributes.py --json` | Weapons, attachments, sub-slot filters, effects, stance presets: everything the evaluator needs |
| `assets/data/loadout-extras.json` (235 KB) | `python -I _tools/loadout_extras.py` | `unlocks` (class tree gates), `reticles`, `icons`, `ballistics` (per-ammo damage by body part and armor class, drop-off factors, rpm) |
| `assets/data/loadout-builder.json` (95 KB) | `python -I _tools/loadout_builder_data.py` | `slots` (which items go in primary, sidearm, special, helmet, armor, vest, backpack) and `items` (name, price, weight, icon, armor class and coverage, backpack grid, vest quick slots, magazine capacity) |
| `assets/data/scope-reticles.json` + `assets/img/icons/scope-reticles/*.png` | `python -I _tools/scope_reticles.py <dump-dir> <png-dir>` | Through-the-scope reticle images for 5 scopes (needs a WdExtract dump, see section 6) |
| `assets/data/spray-patterns.json` (1.4 MB) | `python -I _tools/spray_patterns.py --write` | Recoil patterns, view kick, Monte Carlo band. Loaded lazily after first paint |

Both new generators take `--check` (exit 1 when the written file is stale). After any change to `data/` or to the
shop or weapon tables, rerun in this order: `weapon_attributes.py --json`, `loadout_extras.py`, `loadout_builder_data.py`.

Sources behind the builder data:

- **Slot membership**: the `Inventory.Slot.*` tag in each item definition's `ItemContext` (`ID_*.json`). Not inferred from names. Spec. Item (`Inventory.Slot.Specialist`) = 4 launchers + 16 tools; grenades and mines are quick-slot items, not here.
- **Class level gates**: `DT_MetaTree_Roles` (Infantry, Medic, Recon, Support, Wardog). An item in no tree is always available. With a class chosen only that class's tree counts; with "Any class" the lowest level across trees.
- **Prices**: the generators behind `game-features/Wardogs_WeaponShop_v1.md` and `Wardogs_ItemShop_v1.md`.
- **Weights**: `BHInventoryFragment_Weight`. **Magazine capacity**: the `Item.Ammo` container's `MaxSlotAmountStackSize` (same rule as `weapon_capacity_tables.py`).
- **Names**: shop FriendlyName. 70 parts have none; they get `nameDerived: true` and a name like "AK74 barrel" (the weapon that starts with the part) or "Alternative barrel 3". Dev codes inside real names (`WEPN_037` and similar) are stripped.

## 3. Page behaviour and decisions

- **Weapon tiles show four slots only: Muzzle, Magazine, Scope, Foregrip** (user decision, 2026-10-26: "for now"). `SHOWN_SLOTS` at the top of `loadout-builder.js` maps slot tag to order and label. Foregrips are the `Item.Attachment.Underbarrel` slot (the "Grip" slot is the pistol grip). The muzzle is a nested slot on the barrel. Barrel, stock, pistol grip and handguard stay on their defaults and still count in every value. To show more slots, add their tags to `SHOWN_SLOTS`.
- **Handling table**: Base vs Fitted from `L.evaluate`. Green/red direction: lower is better for ADS time, recoil and spread; higher for accuracy, equip and holster speed; zoom, zeroing and length are neutral. The accuracy direction is an assumption.
- **Recoil panel**: takes the evaluator's *final* vertical and horizontal recoil multipliers, which already include stance and attachments; stance is only a label inside the panel (never apply the stance ratio twice). Per shot: `kick × (H, V) × focus cut × ViewKickMagnitudeMultiplier`, no recovery, independent of FOV and sensitivity (round 81, `docs/evidence/round81-view-kick-curve.md`). Shot count follows the equipped magazine's capacity (cap 100); the p10–p90 band exists only for the shots the data simulates (at least 40). Default target distance 15 m. Hidden for launchers and the bow.
- **Ballistics**: damage at distance = point-blank damage by location and armor class × falloff curve × drag speed scale (same model as `wiki_ttk.py`). Shotguns assume all pellets hit. 100 HP target. Attachments do not change damage in this data. Target helmet and armor are the enemy's, separate from the player's own gear.
- **Cost**: sum of the shop prices of weapons, gear and *changed* attachments; default attachments are assumed to come with the weapon. Items with no price show "—" and are counted in "+ n without a price"; shop-hidden prices show "· not on sale" and are added.
- **Sight names**: socket names are shown as "Main sight", "Second sight", "Canted sight" (`sightLabel`).
- **URL hash** (only differences from the default AK74 build are written): `p= s= x=` primary, sidearm, special; `p@<slot key>=` an attachment; `p#sight=`, `p#bipod=`; `h= a= v= b=` gear; `on= stance= focus=1 cls= lvl=`; `ammo= th= ta= range=`. Unknown ids fall back to defaults.

## 4. Verification

Run from the repo root:

```
python -I _tools/loadout_extras.py --check
python -I _tools/loadout_builder_data.py --check
node _tools/loadout_recoil_check.js      # AK74M 30 shots: 35.705 deg climb, stance not double applied
node _tools/spray_viewer_check.js
python -I _tools/check_links.py
```

The round 83 independent verifier matched, at the time of merge:

- handling values against `weapon_attributes.py` for three builds;
- 810 damage values against `weapon-damage-falloff.json`, with 0 mismatches;
- shots and time to kill against `wiki_ttk.py`;
- prices and weights against the shop docs;
- the recoil climb scaling with Fitted vertical recoil;
- the hash round trip, plus 26 garbage hashes;
- every picker, at 1440, 1024, 390 and 360 px.

## 5. Deploying: things that broke once

GitHub Pages builds with **Ruby Sass 3.7** (jekyll-sass-converter 1.5.2) and compiles two stylesheets, including `just-the-docs-dark.scss`, where only the tokens at the top of `_sass/custom/custom.scss` exist. The first deploy failed on this. Rules:

- Use only `$ue-*` and `$radius-*` tokens defined at the top of `custom.scss` (not ones defined only in `color_schemes/wardogs.scss`).
- Wrap CSS `min()`, `max()`, `clamp()` in `unquote("...")`.
- Put `@container` blocks at the top level, not nested in a rule, and write `container-name` and `container-type` separately (no `lb / inline-size` shorthand).
- Asset URLs in markup go through `{{ '/...' | relative_url }}`; images in JS are built from the root's `data-base`.

A local strict compile check (libsass, closer to Ruby Sass than Dart Sass) is a good pre-push gate. After a push, watch
`gh run list --branch main --limit 1` until the "pages build and deployment" run completes, then load the live page.

`assets/js/wd-reading.js` (site-wide) now skips tables whose header row is filled in later by JS; both loadout pages
need that.

## 6. Local preview and extraction setup

- **Preview harness**: `E:/Reverse_Engineer/wardogs_analysis/lc_preview_tools/build_preview.py` and `E:/r83/verify-build.py` approximate the Jekyll output and compile the CSS with Dart Sass. Serve with `python -m http.server <port> --bind 127.0.0.1 --directory <out>`. Headless Edge screenshots: `lc_preview_tools/edge.mjs` (puppeteer-core). Harness-only console noise: "Unexpected token '{'" and a favicon 404.
- **Scope reticles** were extracted offline with `round76_icons/bin/WdExtract.exe` (`dump` and `textures` modes) using the mappings file `round8_propertybags_20261019/normal-order.usmap`. The default mappings give empty material parameters. Inputs and outputs are in `E:/Reverse_Engineer/wardogs_analysis/round82_reticles/`. The AES key file lives outside the repo and must never be committed.

## 7. Known gaps and ideas

- **Reticles**: only 9 of 29 sights have a reticle image. The newer scopes (SGHT_026 to 040) draw their reticle procedurally in UMG materials (`M_SGHT_0xx_Reticle`, `MI_UI_Reticle_Modular*`), with no texture to extract; showing them would mean rendering those material graphs.
- **Prices and data**:
  - 176 attachments have no vendor row (no price).
  - 87 have no icon (a letter tile is shown).
  - Many have no weight, so total weight is shown as "at least".
- **Weapons without bullet data**: the bow and the launchers have no damage tables. (The Mosin Nagant was missing until 2026-10-27 only because its item tag is `Id.Item.Mosin`, not `Id.Item.WEPN_017`; `loadout_extras.py` now matches damage rows to `ID_<short name>` first.)
- **Picker**: no arrow-key grid navigation (Tab only).
- **Recoil target view**: the 1.4 m aim height is a presentation choice, not game data. A "zoom to player" toggle would help at long range.
- **Hidden slots in old links**: an old shared link that changed a hidden slot (barrel, stock, grip, handguard) still loads it, but there is no tile to change it back.
- **Housekeeping**: the round 83 worktrees `E:/r83/{data,ui,recoil,int}`, the branches `r83-data`, `r83-ui`, `r83-recoil` and `feature/loadout-builder` are merged and can be removed. A test web server from the round 83 verifier may still be running on port 8731.
